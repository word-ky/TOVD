"""Fixed T006 training, frozen control replay and offline oracle diagnostics."""

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform

import torch

from scripts.train_synthetic_semantic import run as train_run
from research_log.t003.oracle_diagnostic_run import save_json
from research_log.t004.oracle_objective_screen import summarize
from research_log.t005.oracle_step_screen import oracle_step_episode, measure_forward_passes, score_output
from research_log.t006.meta_gradient_probe import run_probes
from tovd.synthetic.benchmark import aggregate_results, episode_seed, evaluate_model
from tovd.synthetic.models import EpisodicClassifier
from tovd.synthetic.semantic_episodes import SemanticWorld, WorldConfig


def interpretation_rules(aggregate, per_seed, controls, original_cosine, validity, mechanisms):
    metrics=aggregate["P_C2_meta"]
    hard,easy=metrics["hard"],metrics["easy"]
    r2={"hard_nll_delta":hard["after.nll_delta"]["mean"],"hard_accuracy_delta_pp":100*hard["after.accuracy_delta"]["mean"],
        "nll_improving_seeds":sum(seed["after.nll_delta"]["mean"]<0 for seed in per_seed["P_C2_meta"]["hard"].values())}
    r2["passes"]=r2["hard_nll_delta"]<0 and r2["hard_accuracy_delta_pp"]>=0 and r2["nll_improving_seeds"]>=2
    best_acc=min(("B0","B1","B2"),key=lambda m:(-controls[m]["hard"]["accuracy"]["mean"],controls[m]["hard"]["nll"]["mean"]))
    best_nll=min(("B0","B1","B2"),key=lambda m:(controls[m]["hard"]["nll"]["mean"],-controls[m]["hard"]["accuracy"]["mean"]))
    r3={}
    for branch,baseline in (("accuracy_branch",best_acc),("nll_branch",best_nll)):
        row={"control":baseline,"accuracy_gain_pp":100*(hard["after.accuracy"]["mean"]-controls[baseline]["hard"]["accuracy"]["mean"]),
             "nll_gain":controls[baseline]["hard"]["nll"]["mean"]-hard["after.nll"]["mean"]}
        row["passes"]=(row["accuracy_gain_pp"]>=1 and row["nll_gain"]>=0) if branch=="accuracy_branch" else (row["nll_gain"]>=.03 and row["accuracy_gain_pp"]>=0)
        r3[branch]=row
    r3["passes"]=r3["accuracy_branch"]["passes"] or r3["nll_branch"]["passes"]
    flags={seed:{"nll_harm":row["after.nll_delta"]["mean"],"accuracy_harm_pp":-100*row["after.accuracy_delta"]["mean"]}
           for seed,row in per_seed["P_C2_meta"]["easy"].items()
           if row["after.nll_delta"]["mean"]>.1 or row["after.accuracy_delta"]["mean"]<-.05}
    r4={"easy_nll_delta":easy["after.nll_delta"]["mean"],"easy_accuracy_delta_pp":100*easy["after.accuracy_delta"]["mean"],"seed_robustness_flags":flags}
    r4["passes"]=r4["easy_nll_delta"]<=.05 and r4["easy_accuracy_delta_pp"]>=-3
    rows=[row for receipt in mechanisms.values() for row in receipt["episodes"]]
    r5={"hard_cosine_gain_vs_original_O0":hard["alignment.cosine"]["mean"]-original_cosine,
        "reset_state_max":max(row["reset_state_delta"] for row in rows),"reset_output_max":max(row["reset_output_delta"] for row in rows),
        "vocabulary_changes_state_all_seeds":all(receipt["mean"]["easy_hard_state_delta"]>0 and receipt["mean"]["unrelated_state_delta"]>0 for receipt in mechanisms.values())}
    r5["passes"]=r5["hard_cosine_gain_vs_original_O0"]>=.05 and r5["reset_state_max"]<=1e-6 and r5["reset_output_max"]<=1e-6 and r5["vocabulary_changes_state_all_seeds"]
    if not (r2["passes"] and r3["passes"]):
        recommendation="Stop/reframe: the required fast-path and control gains do not both hold."
    elif not r4["passes"] or flags:
        recommendation="Address stability before detector integration; retain seed failures."
    elif validity["passes"] and r5["passes"]:
        recommendation="Research Lead may consider a small detector task; do not start it under T006."
    else:
        recommendation="Resolve remaining validity/mechanism failures before detector integration."
    return {"rule1_validity":validity,"rule2_fast_value":r2,"rule3_control_value":r3,"rule4_easy_safety":r4,"rule5_mechanism":r5,"recommendation":recommendation}


def run(config, source_root, t005_root, output, device, revision, probe_count=20):
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    output.mkdir(parents=True,exist_ok=True)
    source_config=json.loads((source_root/"config.json").read_text(encoding="utf-8-sig"))
    world=SemanticWorld(WorldConfig(**config["world"]))
    initial_probe=run_probes(config,output/"meta_gradient_initial.json",device,probe_count=probe_count)
    print("PRETRAIN_GRADIENT "+json.dumps(initial_probe["summary"]),flush=True)
    if not initial_probe["summary"]["pretraining_gradient_requirement_passes"]:
        raise RuntimeError("Pretraining stable-region meta-gradient requirement failed; receipt preserved, no full training started.")
    trained_root=output/"trained"
    trained_results=train_run(config,trained_root,device,revision)
    final_probe=run_probes(config,output/"meta_gradient_final.json",device,checkpoint_root=trained_root,probe_count=probe_count)
    historical=json.loads((t005_root/"frozen_step_screen.json").read_text())
    sources,control_checks,control_results=[],[],[]
    control_records={}
    for seed in config["seeds"]:
        for method in ("B0","B1","B2","P"):
            path=source_root/f"seed{seed}_{method}/checkpoint.pt"
            checkpoint=torch.load(path,map_location=device,weights_only=True)
            sources.append({"seed":seed,"method":method,"path":str(path.resolve()),"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"training_revision":checkpoint["revision"]})
            model=EpisodicClassifier(method,**checkpoint["config"]["model"]).to(device)
            model.load_state_dict(checkpoint["state_dict"])
            metrics,records=evaluate_model(model,world,config,seed,device)
            original=json.loads((path.parent/"episodes.json").read_text())
            errors={metric:max(abs(a[metric]-b[metric]) for a,b in zip(records,original)) for metric in ("accuracy","nll","margin")}
            mismatches=sum(any(a[key]!=b[key] for key in ("episode_seed","hardness","index","vocabulary_ids","query_ids")) for a,b in zip(records,original))
            control_checks.append({"seed":seed,"method":method,"count":len(records),"source_count":len(original),"errors":errors,"stream_mismatches":mismatches})
            control_results.append({"seed":seed,"method":method,"metrics":metrics})
            control_records[f"seed{seed}_{method}"]=records
    save_json(output/"control_records.json",control_records)
    save_json(output/"control_results.json",control_results)
    controls=aggregate_results(control_results)
    grouped={"P_C2_meta":{regime:{} for regime in ("easy","hard")}}
    initial_checks,timings,eta_counts,training=[],{},{},{}
    accepted_violations=0
    for seed in config["seeds"]:
        checkpoint=torch.load(trained_root/f"seed{seed}_P_C2_meta/checkpoint.pt",map_location=device,weights_only=True)
        training[str(seed)]={"curve":checkpoint["training_curve"],"W0_outer_drift":checkpoint["W0_outer_drift"],"train_seconds":checkpoint["train_seconds"]}
        original_p=torch.load(source_root/f"seed{seed}_P/checkpoint.pt",map_location="cpu",weights_only=True)
        torch.manual_seed(seed)
        initialization=EpisodicClassifier("P",**config["model"])
        full_error=max((value-checkpoint["initial_state_dict"][name].cpu()).abs().max().item() for name,value in initialization.state_dict().items())
        fast_error=max((value-checkpoint["initial_fast_state"][name].cpu()).abs().max().item() for name,value in original_p["initial_fast_state"].items())
        initial_checks.append({"seed":seed,"all_tensors_vs_seed_reconstruction_max_error":full_error,"fast_tensors_vs_historical_P_max_error":fast_error})
        models={name:EpisodicClassifier(method,**config["model"]).to(device) for name,method in
                (("C2","O1_backtracking"),("P_same_W0","P"),("O1_fixed_same_W0","O1_fixed"))}
        for model in models.values():
            model.load_state_dict(checkpoint["state_dict"])
        original_eval=json.loads((trained_root/f"seed{seed}_P_C2_meta/episodes.json").read_text())
        timings[str(seed)]={}
        for regime in ("easy","hard"):
            episodes=[world.episode("test",regime,episode_seed(seed,index,"test")).to(device) for index in range(config["eval_episodes"])]
            previous=[row for row in original_eval if row["hardness"]==regime]
            rows=[]
            for index,ep in enumerate(episodes):
                diag=oracle_step_episode(models["C2"],ep,models["O1_fixed_same_W0"].memory)
                with torch.no_grad():
                    static=models["C2"].memory(ep.X[None],ep.T[None],ep.Q[None],enable_ttt=False)
                    static_scores=score_output(models["C2"],ep,static.tokens[0])
                diag["W0_only_metric_max_error"]=max(abs(static_scores[key]-diag["before"][key]) for key in ("accuracy","nll","margin"))
                diag["training_runner_eval_max_error"]=max(abs(previous[index][key]-diag["after"][key]) for key in ("accuracy","nll","margin"))
                accepted_violations+=int(diag["step"]["step_accepted"] and not diag["step"]["armijo_satisfied"])
                rows.append({"seed":seed,"method":"P_C2_meta","regime":regime,"index":index,"episode_seed":episode_seed(seed,index,"test"),"diagnostics":diag})
            grouped["P_C2_meta"][regime][seed]=rows
            save_json(output/f"seed{seed}_P_C2_meta_{regime}.json",rows)
            eta_counts[f"seed{seed}_{regime}"]=dict(Counter(str(round(row["diagnostics"]["step"]["chosen_eta"],8)) for row in rows))
            timings[str(seed)][regime]={name:measure_forward_passes(model,episodes,device) for name,model in models.items()}
            print(f"DIAGNOSTICS seed={seed} regime={regime} episodes={len(rows)}",flush=True)
    result=summarize(grouped)
    mechanisms={str(row["seed"]):row["mechanism"] for row in trained_results}
    all_rows=[row["diagnostics"] for regimes in grouped.values() for seeds in regimes.values() for rows in seeds.values() for row in rows]
    curves=[row for receipt in training.values() for row in receipt["curve"]]
    validity={"finished_seeds":list(config["seeds"]),"steps_per_seed":{seed:len(row["curve"]) for seed,row in training.items()},
              "training_nonfinite_steps":sum(not row["finite"] for row in curves),"training_armijo_violations":sum(row["armijo_violations"] for row in curves),
              "test_armijo_violations":accepted_violations,"test_nonfinite_elements":sum(row["nonfinite_elements"] for row in all_rows),
              "control_max_metric_error":max(value for check in control_checks for value in check["errors"].values()),
              "control_stream_mismatches":sum(check["stream_mismatches"]+abs(check["count"]-check["source_count"]) for check in control_checks),
              "normal_output_max_error":max(row["normal_output_max_error"] for row in all_rows),
              "normal_state_max_error":max(row["normal_state_max_error"] for row in all_rows),
              "W0_only_metric_max_error":max(row["W0_only_metric_max_error"] for row in all_rows),
              "training_runner_eval_max_error":max(row["training_runner_eval_max_error"] for row in all_rows),
              "initial_tensor_max_error":max(max(row["all_tensors_vs_seed_reconstruction_max_error"],row["fast_tensors_vs_historical_P_max_error"]) for row in initial_checks),
              "initial_meta_gradient_requirement_passes":initial_probe["summary"]["pretraining_gradient_requirement_passes"]}
    validity["passes"]=all(len(row["curve"])==config["train_steps"] for row in training.values()) and len(training)==len(config["seeds"]) and validity["initial_meta_gradient_requirement_passes"] and all(value==0 for key,value in validity.items() if key.endswith(("steps","violations","elements","error","mismatches")) and isinstance(value,(int,float)))
    result.update({"rules":interpretation_rules(result["aggregate"],result["per_seed"],controls,historical["aggregate"]["O0"]["hard"]["alignment.cosine"]["mean"],validity,mechanisms),
                   "controls":controls,"control_checks":control_checks,"source_checkpoints":sources,"initial_tensor_checks":initial_checks,
                   "training":training,"timings":timings,"eta_counts":eta_counts,"mechanisms":mechanisms,
                   "initial_gradient_summary":initial_probe["summary"],"final_gradient_summary":final_probe["summary"],
                   "historical_T005_references":{name:historical["aggregate"][name] for name in ("O0","C2")},
                   "environment":{"revision":revision,"preregistration":"f9f4137","time_utc":datetime.now(timezone.utc).isoformat(),"python":platform.python_version(),"torch":torch.__version__,"cuda":torch.version.cuda,"device":device,"gpu":torch.cuda.get_device_name() if device.startswith("cuda") else None,"dtype":"float32","config":config,"source_config":source_config}})
    save_json(output/"results.json",result)
    save_json(output/"rules.json",result["rules"])
    return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--config",type=Path,default=Path("research_log/t006/config.json"))
    parser.add_argument("--source-root",type=Path,required=True)
    parser.add_argument("--t005-root",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--device",default="cpu")
    parser.add_argument("--revision",required=True)
    args=parser.parse_args()
    run(json.loads(args.config.read_text()),args.source_root,args.t005_root,args.output,args.device,args.revision)


if __name__=="__main__":
    main()
