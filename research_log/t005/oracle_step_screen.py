"""T005 frozen-checkpoint ORACLE diagnosis; runtime controllers remain label-free."""

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import statistics
import time

import torch
from torch.func import functional_call
from torch.nn import functional as F

from research_log.t003.oracle_diagnostic import gradient_relation, oracle_preupdate, paired_changes
from research_log.t003.oracle_diagnostic_run import save_json
from research_log.t004.oracle_objective_screen import summarize
from tovd.synthetic.benchmark import episode_seed, mechanism_analysis, outer_metrics
from tovd.synthetic.models import EpisodicClassifier
from tovd.synthetic.semantic_episodes import SemanticWorld, WorldConfig

METHODS = {"O0": "O0", "C0": "O1_fixed", "C1": "O1_norm_matched", "C2": "O1_backtracking"}


def score_output(model, episode, output):
    similarities = model.similarities(output[None], episode.T[None])
    logits = similarities / model.classifier_temperature
    row = outer_metrics(logits, similarities, episode.labels[None])
    row["query_nll"] = F.cross_entropy(logits[0], episode.labels, reduction="none").tolist()
    return row


def oracle_step_episode(model, episode, o1_memory):
    model.eval()
    context = oracle_preupdate(model, episode)
    params, keys = context["params"], context["keys"]
    pred = functional_call(model.memory.fast_model, params, (keys,))
    loss1 = o1_memory.inner_objective(pred, keys, episode.X, episode.T, context["target"])
    g1 = torch.autograd.grad(loss1, tuple(params.values()))
    if model.method == "O0":
        gradients = context["g_inner"]
        before_inner = model.memory.inner_objective(pred, keys, episode.X, episode.T, context["target"])
    else:
        gradients, before_inner = g1, loss1
    adapted, step = model.memory.select_update(params, gradients, before_inner, keys,
                                               episode.X, episode.T, context["target"], False)
    with torch.no_grad():
        before_output = functional_call(model.memory.fast_model, params, (context["queries"],))
        output = functional_call(model.memory.fast_model, adapted, (context["queries"],))
        before, after = score_output(model, episode, before_output), score_output(model, episode, output)
        delta = tuple(p-adapted[name] for name,p in params.items())
        after["update_norm"] = torch.sqrt(sum(d.square().sum() for d in delta)).item()
        prediction = functional_call(model.memory.fast_model, adapted, (keys,))
        loss1_after = o1_memory.inner_objective(prediction, keys, episode.X, episode.T, context["target"])
        normal = model(episode.X[None], episode.T[None], episode.Q[None])
        step_record = {key:value.item() for key,value in step.items()}
        if model.method == "O1_backtracking":
            step_record["armijo_satisfied"] = bool(loss1_after <= step["armijo_rhs"])
            step_record["armijo_margin"] = (step["armijo_rhs"] - loss1_after).item()
        raw_values = [*gradients, *g1, *adapted.values(), output, loss1, loss1_after]
    return {"oracle_diagnostic": True, "alignment": gradient_relation(gradients, context["g_task"]),
            "raw_O1_alignment": gradient_relation(g1, context["g_task"]),
            "effective_direction": gradient_relation(delta, context["g_task"]),
            "before": before, "after": paired_changes(after,before),
            "O1_inner_loss_before": loss1.item(), "O1_inner_loss_after": loss1_after.item(),
            "own_inner_loss_before": normal.diagnostics["inner_loss_before"].item(),
            "own_inner_loss_after": normal.diagnostics["inner_loss_after"].item(),
            "step": step_record, "representation_shift": (output-before_output).norm().item(),
            "normal_output_max_error": (output-normal.tokens[0]).abs().max().item(),
            "normal_state_max_error": max((adapted[name]-normal.fast_state[name][0]).abs().max().item() for name in params),
            "nonfinite_elements": sum((~torch.isfinite(value)).sum().item() for value in raw_values),
            "all_finite": bool(normal.diagnostics["all_finite"].all())}


def interpret_rules(aggregate, per_seed, accepted_violations):
    def m(method, regime, metric):
        return aggregate[method][regime][metric]["mean"]
    rule1 = {"easy_nll_gain": m("C0","easy","after.nll")-m("C1","easy","after.nll"),
             "easy_accuracy_gain_pp": 100*(m("C1","easy","after.accuracy")-m("C0","easy","after.accuracy")),
             "hard_both_worsen": m("C1","hard","after.nll")>m("C0","hard","after.nll") and
                                  m("C1","hard","after.accuracy")<m("C0","hard","after.accuracy")}
    rule1["passes"] = rule1["easy_nll_gain"]>=.10 and rule1["easy_accuracy_gain_pp"]>=5 and not rule1["hard_both_worsen"]
    rule2 = {"accepted_armijo_violations": accepted_violations,
             "easy_nll_harm_vs_O0": m("C2","easy","after.nll")-m("O0","easy","after.nll"),
             "easy_accuracy_loss_pp_vs_O0": 100*(m("O0","easy","after.accuracy")-m("C2","easy","after.accuracy")),
             "hard_nll_no_worse_than_C0": m("C2","hard","after.nll")<=m("C0","hard","after.nll")}
    rule2["passes"] = accepted_violations==0 and rule2["easy_nll_harm_vs_O0"]<=.10 and rule2["easy_accuracy_loss_pp_vs_O0"]<=5 and rule2["hard_nll_no_worse_than_C0"]
    rule3 = {}
    for method in ("C1","C2"):
        row = {"hard_nll_delta": m(method,"hard","after.nll_delta"),
               "hard_accuracy_delta_pp": 100*m(method,"hard","after.accuracy_delta"),
               "hard_nll_improving_seeds": sum(seed["after.nll_delta"]["mean"]<0 for seed in per_seed[method]["hard"].values()),
               "hard_cosine_gain_vs_O0": m(method,"hard","alignment.cosine")-m("O0","hard","alignment.cosine")}
        row["passes"] = row["hard_nll_delta"]<0 and row["hard_accuracy_delta_pp"]>=0 and row["hard_nll_improving_seeds"]>=2 and row["hard_cosine_gain_vs_O0"]>=.05
        rule3[method] = row
    return {"rule1_scale_rescue": rule1, "rule2_descent_safe": rule2, "rule3_task_useful": rule3,
            "task_useful_controllers": [key for key,row in rule3.items() if row["passes"]],
            "next_action": "Research Lead review only; no meta-training or detector integration in T005."}


def measure_forward_passes(model, episodes, device):
    def sync():
        if device.startswith("cuda"):
            torch.cuda.synchronize()
    model.eval()
    with torch.no_grad():
        for ep in episodes[:3]:
            model(ep.X[None],ep.T[None],ep.Q[None])
        milliseconds = []
        for _ in range(3):
            sync()
            start = time.perf_counter()
            for ep in episodes:
                model(ep.X[None],ep.T[None],ep.Q[None])
            sync()
            milliseconds.append((time.perf_counter()-start)*1000/len(episodes))
    return {"pass_ms_per_episode": milliseconds, "mean_ms_per_episode": statistics.mean(milliseconds)}


def run(source_root, t004_root, output, device, revision, seeds=(7,17,27), episode_limit=None):
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    output.mkdir(parents=True,exist_ok=True)
    config = json.loads((source_root/"config.json").read_text(encoding="utf-8-sig"))
    world = SemanticWorld(WorldConfig(**config["world"]))
    count = config["eval_episodes"] if episode_limit is None else episode_limit
    grouped = {name:{regime:{} for regime in ("easy","hard")} for name in METHODS}
    sources, checks, mechanisms, timings, eta_counts = [], [], {}, {}, {}
    violations = 0
    for seed in seeds:
        path = source_root/f"seed{seed}_P/checkpoint.pt"
        checkpoint = torch.load(path,map_location=device,weights_only=True)
        sources.append({"seed":seed,"path":str(path.resolve()),"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"training_revision":checkpoint["revision"]})
        models = {name:EpisodicClassifier(method,**checkpoint["config"]["model"]).to(device) for name,method in METHODS.items()}
        for model in models.values():
            model.load_state_dict(checkpoint["state_dict"])
        for name, model in models.items():
            mechanisms.setdefault(name,{})[str(seed)] = mechanism_analysis(model,world,config,seed,device)
            timings.setdefault(name,{})[str(seed)] = {}
            for regime in ("easy","hard"):
                episodes = [world.episode("test",regime,episode_seed(seed,index,"test")).to(device) for index in range(count)]
                records = [{"seed":seed,"method":name,"regime":regime,"index":index,
                            "episode_seed":episode_seed(seed,index,"test"),
                            "diagnostics":oracle_step_episode(model,ep,models["C0"].memory)} for index,ep in enumerate(episodes)]
                grouped[name][regime][seed] = records
                save_json(output/f"seed{seed}_{name}_{regime}.json",records)
                if name in ("O0","C0"):
                    objective = "O0" if name=="O0" else "O1"
                    old = json.loads((t004_root/f"seed{seed}_{objective}_{regime}.json").read_text())[:count]
                    errors = {metric:max(abs(row["diagnostics"]["after"][metric]-prior["diagnostics"]["after"][metric])
                                         for row,prior in zip(records,old)) for metric in ("accuracy","nll","margin")}
                    checks.append({"method":name,"seed":seed,"regime":regime,"episodes":count,"errors":errors,
                                   "episode_seed_mismatches":sum(row["episode_seed"]!=prior["episode_seed"] for row,prior in zip(records,old))})
                if name=="C2":
                    violations += sum(row["diagnostics"]["step"]["step_accepted"] and not row["diagnostics"]["step"]["armijo_satisfied"] for row in records)
                    eta_counts[f"seed{seed}_{regime}"] = dict(Counter(str(round(row["diagnostics"]["step"]["chosen_eta"],8)) for row in records))
                timings[name][str(seed)][regime] = measure_forward_passes(model,episodes,device)
                print(f"SCREEN seed={seed} method={name} regime={regime} episodes={count}",flush=True)
    result = summarize(grouped)
    result["oracle_diagnostic"] = True
    result["rules"] = interpret_rules(result["aggregate"],result["per_seed"],violations)
    result["historical_checks"] = checks
    result["mechanisms"] = mechanisms
    for name,seeds_data in timings.items():
        for seed,regimes in seeds_data.items():
            for regime,measurement in regimes.items():
                measurement["multiplier_vs_C0"] = measurement["mean_ms_per_episode"]/timings["C0"][seed][regime]["mean_ms_per_episode"]
    result["timings"] = timings
    result["C2_eta_counts"] = eta_counts
    result["environment"] = {"time_utc":datetime.now(timezone.utc).isoformat(),"revision":revision,
        "python":platform.python_version(),"torch":torch.__version__,"cuda":torch.version.cuda,
        "device":device,"gpu":torch.cuda.get_device_name() if device.startswith("cuda") else None,
        "dtype":"float32","source_checkpoints":sources,"source_config":config,
        "seeds":list(seeds),"episodes_per_regime":count,"outer_training":False,
        "preregistration_commit":"7b8949e","runtime_protocol":"3 warmups; 3 timed full passes; GPU sync before/after each pass; exclude oracle analysis"}
    save_json(output/"frozen_step_screen.json",result)
    save_json(output/"rules.json",result["rules"])
    return result


def main():
    parser=argparse.ArgumentParser(description="T005 ORACLE scoring; label-free step selection")
    parser.add_argument("--source-root",type=Path,required=True)
    parser.add_argument("--t004-root",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--device",default="cpu")
    parser.add_argument("--revision",required=True)
    args=parser.parse_args()
    run(args.source_root,args.t004_root,args.output,args.device,args.revision)


if __name__=="__main__":
    main()
