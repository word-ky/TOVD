"""T007 matched warm-start continuation; oracle diagnostics stay offline here."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import statistics

import torch

from research_log.t003.oracle_diagnostic import paired_changes
from research_log.t003.oracle_diagnostic_run import save_json
from research_log.t004.oracle_objective_screen import summarize
from research_log.t005.oracle_step_screen import oracle_step_episode, measure_forward_passes, score_output
from research_log.t006.experiment import interpretation_rules as t006_rules
from tovd.synthetic.benchmark import (aggregate_results, episode_seed, evaluate_model,
                                      mechanism_analysis, train_model, training_episode)
from tovd.synthetic.models import EpisodicClassifier
from tovd.synthetic.semantic_episodes import SemanticWorld, WorldConfig

BRANCHES=("P_O0_resume","P_C2_warm")
METRICS=("accuracy","nll","margin")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_model(state, method, config, device):
    model=EpisodicClassifier(method,**config["model"]).to(device)
    model.load_state_dict(state)
    return model.eval()


def parameter_drift(state, origin):
    groups={"W0":"memory.fast_model.","key_projection":"memory.key_projection.",
            "query_projection":"memory.query_projection.","total_slow_state":""}
    result={name:sum((value.detach().cpu()-origin[key].cpu()).square().sum().item()
                     for key,value in state.items() if key.startswith(prefix))**.5
            for name,prefix in groups.items()}
    result.update(classifier=0.0,classifier_parameter_count=0,classifier_temperature=.1)
    return result


def tensor_equality(state, origin):
    return {"all_tensors_byte_equal":all(torch.equal(value.cpu().view(torch.uint8),origin[key].cpu().view(torch.uint8))
                                        for key,value in state.items()),
            "max_error":max((value.cpu()-origin[key].cpu()).abs().max().item() for key,value in state.items())}


def pair_records(model, episodes):
    records=[]
    with torch.no_grad():
        for index,ep in enumerate(episodes):
            static=model.memory(ep.X[None],ep.T[None],ep.Q[None],enable_ttt=False)
            adapted=model(ep.X[None],ep.T[None],ep.Q[None])
            before=score_output(model,ep,static.tokens[0])
            after=score_output(model,ep,adapted.tokens[0])
            records.append({"index":index,"vocabulary_ids":ep.vocabulary_ids.tolist(),
                            "query_ids":ep.query_ids.tolist(),"diagnostics":{"before":before,
                            "after":paired_changes(after,before)}})
    return records


def compare_pairs(records, historical):
    return {"count":len(records),"historical_count":len(historical),
            "max_error":max(abs(a["diagnostics"][stage][metric]-b["diagnostics"][stage][metric])
                            for a,b in zip(records,historical) for stage in ("before","after") for metric in METRICS)}


def rules(aggregate, per_seed, controls, historical, validity, mechanisms):
    translated=t006_rules({"P_C2_meta":aggregate["P_C2_warm"]},
                         {"P_C2_meta":per_seed["P_C2_warm"]},controls,
                         historical["O0"]["hard"]["alignment.cosine"]["mean"],validity,mechanisms["P_C2_warm"])
    w2=aggregate["P_C2_warm"]["hard"]
    w1=aggregate["P_O0_resume"]["hard"]
    frozen=historical["C2"]["hard"]
    r3={"accuracy_delta_pp":100*(w2["after.accuracy"]["mean"]-frozen["after.accuracy"]["mean"]),
        "nll_delta":w2["after.nll"]["mean"]-frozen["after.nll"]["mean"]}
    r3["passes"]=r3["accuracy_delta_pp"]>=-2 and r3["nll_delta"]<=.03
    r4={"W2_minus_W1_accuracy_pp":100*(w2["after.accuracy"]["mean"]-w1["after.accuracy"]["mean"]),
        "W2_minus_W1_nll":w2["after.nll"]["mean"]-w1["after.nll"]["mean"]}
    r4["passes"]=not(r4["W2_minus_W1_accuracy_pp"]<0 and r4["W2_minus_W1_nll"]>0)
    r6={"easy_safety":translated["rule4_easy_safety"],"mechanism":translated["rule5_mechanism"]}
    r6["passes"]=r6["easy_safety"]["passes"] and not r6["easy_safety"]["seed_robustness_flags"] and r6["mechanism"]["passes"]
    return {"rule1_validity":validity,"rule2_fast_value":translated["rule2_fast_value"],
            "rule3_preservation":r3,"rule4_objective_effect":r4,"rule5_control_value":translated["rule3_control_value"],
            "rule6_easy_mechanism":r6}


def run(config, source_root, t005_root, t006_root, expected_hashes, output, device, revision,
        snapshot_steps=(0,50,100,200,400)):
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    output.mkdir(parents=True,exist_ok=True)
    save_json(output/"config.json",config)
    world=SemanticWorld(WorldConfig(**config["world"]))
    source_config=read_json(source_root/"config.json")
    offset=source_config["train_steps"]*source_config["batch_size"]
    end=offset+config["train_steps"]*config["batch_size"]
    sources=[]
    for seed in config["seeds"]:
        for name in ("B0","B1","B2","P","P_C2_meta"):
            path=(t006_root/"trained" if name=="P_C2_meta" else source_root)/f"seed{seed}_{name}/checkpoint.pt"
            key=f"seed{seed}_{name}"
            sha=digest(path)
            sources.append({"key":key,"path":str(path.resolve()),"sha256":sha,
                            "expected_sha256":expected_hashes[key],"matches":sha==expected_hashes[key]})
    save_json(output/"sources.json",sources)
    if not all(row["matches"] for row in sources):
        raise RuntimeError("Historical source checkpoint hash mismatch; no continuation started.")
    training,initial_checks={},[]
    for seed in config["seeds"]:
        source=torch.load(source_root/f"seed{seed}_P/checkpoint.pt",map_location=device,weights_only=True)
        for branch in BRANCHES:
            directory=output/f"seed{seed}_{branch}"
            directory.mkdir(exist_ok=True)
            def snapshot(step,model):
                if step==0 and not tensor_equality(model.state_dict(),source["state_dict"])["all_tensors_byte_equal"]:
                    raise RuntimeError("Warm-start tensors differ before training.")
                torch.save({"state_dict":{k:v.detach().cpu().clone() for k,v in model.state_dict().items()},
                            "step":step,"seed":seed,"method":branch,"revision":revision},directory/f"step{step}.pt")
            model,checkpoint=train_model(world,config,seed,branch,device,initial_state_dict=source["state_dict"],
                                         episode_offset=offset,snapshot_steps=snapshot_steps,snapshot_callback=snapshot)
            checkpoint.update(revision=revision,source_sha256=digest(source_root/f"seed{seed}_P/checkpoint.pt"))
            torch.save(checkpoint,directory/"checkpoint.pt")
            receipt={"training_curve":checkpoint["training_curve"],"train_seconds":checkpoint["train_seconds"],
                     "drift":parameter_drift(checkpoint["state_dict"],source["state_dict"])}
            training[f"seed{seed}_{branch}"]=receipt
            save_json(directory/"training.json",receipt)
            initial_checks.append({"seed":seed,"branch":branch,**tensor_equality(checkpoint["initial_state_dict"],source["state_dict"])})
        first=torch.load(output/f"seed{seed}_{BRANCHES[0]}/step0.pt",map_location="cpu",weights_only=True)
        second=torch.load(output/f"seed{seed}_{BRANCHES[1]}/step0.pt",map_location="cpu",weights_only=True)
        initial_checks.append({"seed":seed,"branch":"W1_vs_W2",**tensor_equality(first["state_dict"],second["state_dict"])})
    # All held-out outcomes are read only after the complete fixed training budget.
    historical=read_json(t005_root/"frozen_step_screen.json")["aggregate"]
    reference_group={name:{r:{} for r in ("easy","hard")} for name in ("T005_frozen_C2","T006_random_C2")}
    checks,control_results,control_records=[],[],{}
    grouped={name:{r:{} for r in ("easy","hard")} for name in BRANCHES}
    mechanisms={name:{} for name in BRANCHES}
    timings,trajectories={},[]
    for seed in config["seeds"]:
        test_episodes={r:[world.episode("test",r,episode_seed(seed,i,"test")).to(device) for i in range(config["eval_episodes"])] for r in ("easy","hard")}
        train_count=min(config["eval_episodes"],(end-offset)//2)
        train_episodes={r:[training_episode(world,seed,end-2*train_count+2*i+(r=="hard")).to(device)
                           for i in range(train_count)] for r in ("easy","hard")}
        for name in ("B0","B1","B2","P"):
            path=source_root/f"seed{seed}_{name}/checkpoint.pt"
            ckpt=torch.load(path,map_location=device,weights_only=True)
            metrics,records=evaluate_model(load_model(ckpt["state_dict"],name,config,device),world,config,seed,device)
            old=read_json(path.parent/"episodes.json")
            checks.append({"source":f"seed{seed}_{name}","count":len(records),"historical_count":len(old),
                           "max_error":max(abs(a[m]-b[m]) for a,b in zip(records,old) for m in METRICS),
                           "stream_mismatches":sum(any(a[k]!=b[k] for k in ("index","hardness","episode_seed","vocabulary_ids","query_ids")) for a,b in zip(records,old))})
            control_results.append({"seed":seed,"method":name,"metrics":metrics})
            control_records[f"seed{seed}_{name}"]=records
        for name,root,method in (("T005_frozen_C2",source_root,"P"),("T006_random_C2",t006_root/"trained","P_C2_meta")):
            ckpt=torch.load(root/f"seed{seed}_{method}/checkpoint.pt",map_location=device,weights_only=True)
            model=load_model(ckpt["state_dict"],"O1_backtracking",config,device)
            for regime,episodes in test_episodes.items():
                rows=pair_records(model,episodes)
                for i,row in enumerate(rows):
                    row.update(episode_seed=episode_seed(seed,i,"test"),seed=seed,regime=regime)
                path=(t005_root/f"seed{seed}_C2_{regime}.json" if name=="T005_frozen_C2" else t006_root/f"seed{seed}_P_C2_meta_{regime}.json")
                old=read_json(path)
                checks.append({"source":name,"seed":seed,"regime":regime,**compare_pairs(rows,old),
                               "stream_mismatches":sum(a["episode_seed"]!=b["episode_seed"] for a,b in zip(rows,old))})
                reference_group[name][regime][seed]=rows
                save_json(output/f"seed{seed}_{name}_{regime}.json",rows)
        for branch in BRANCHES:
            directory=output/f"seed{seed}_{branch}"
            timings.setdefault(branch,{})[str(seed)]={}
            for step in snapshot_steps:
                snapshot=torch.load(directory/f"step{step}.pt",map_location=device,weights_only=True)
                model=load_model(snapshot["state_dict"],"O1_backtracking",config,device)
                objective=load_model(snapshot["state_dict"],branch,config,device)
                source=torch.load(source_root/f"seed{seed}_P/checkpoint.pt",map_location="cpu",weights_only=True)
                trajectory={"seed":seed,"branch":branch,"step":step,"diagnostic_only":step!=config["train_steps"],
                            "drift":parameter_drift(snapshot["state_dict"],source["state_dict"]),"metrics":{}}
                raw={}
                for split,episode_map in (("train_seen_at_final",train_episodes),("heldout",test_episodes)):
                    trajectory["metrics"][split]={}
                    raw[split]={}
                    for regime,episodes in episode_map.items():
                        rows=pair_records(model,episodes)
                        with torch.no_grad():
                            for i,ep in enumerate(episodes):
                                out=objective(ep.X[None],ep.T[None],ep.Q[None])
                                rows[i]["training_objective"]=score_output(objective,ep,out.tokens[0])
                                rows[i]["episode_seed"]=episode_seed(seed,i,"test") if split=="heldout" else episode_seed(seed,end-2*train_count+2*i+(regime=="hard"),"train")
                        raw[split][regime]=rows
                        trajectory["metrics"][split][regime]={stage:{m:statistics.mean(row["diagnostics"][stage][m] for row in rows) for m in METRICS}
                                                             for stage in ("before","after")}
                        trajectory["metrics"][split][regime]["training_objective"]={m:statistics.mean(row["training_objective"][m] for row in rows) for m in METRICS}
                save_json(directory/f"step{step}_evaluations.json",raw)
                trajectories.append(trajectory)
                if step!=config["train_steps"]:
                    continue
                mechanisms[branch][str(seed)]=mechanism_analysis(model,world,config,seed,device)
                fixed=load_model(snapshot["state_dict"],"O1_fixed",config,device)
                p=load_model(snapshot["state_dict"],"P",config,device)
                for regime,episodes in test_episodes.items():
                    rows=[]
                    for i,ep in enumerate(episodes):
                        diag=oracle_step_episode(model,ep,fixed.memory)
                        diag["W0_only_metric_max_error"]=max(abs(diag["before"][m]-raw["heldout"][regime][i]["diagnostics"]["before"][m]) for m in METRICS)
                        diag["normal_metric_max_error"]=max(abs(diag["after"][m]-raw["heldout"][regime][i]["diagnostics"]["after"][m]) for m in METRICS)
                        rows.append({"seed":seed,"method":branch,"regime":regime,"index":i,"episode_seed":episode_seed(seed,i,"test"),
                                     "vocabulary_ids":ep.vocabulary_ids.tolist(),"query_ids":ep.query_ids.tolist(),"diagnostics":diag})
                    grouped[branch][regime][seed]=rows
                    save_json(directory/f"{regime}_oracle.json",rows)
                    timings[branch][str(seed)][regime]={name:measure_forward_passes(m,episodes,device) for name,m in (("C2",model),("P",p),("O1_fixed",fixed))}
            print(f"EVALUATED seed={seed} branch={branch} fixed_final={config['train_steps']}",flush=True)
    result=summarize(grouped)
    controls=aggregate_results(control_results)
    reference=summarize(reference_group)
    curves=[row for receipt in training.values() for row in receipt["training_curve"]]
    diagnostics=[row["diagnostics"] for regimes in grouped.values() for seed_rows in regimes.values() for rows in seed_rows.values() for row in rows]
    validity={"complete_budget":len(training)==len(BRANCHES)*len(config["seeds"]) and all(len(v["training_curve"])==config["train_steps"] for v in training.values()),
              "training_nonfinite_steps":sum(not row["finite"] for row in curves),
              "training_armijo_violations":sum(row["armijo_violations"] for row in curves),
              "test_nonfinite_elements":sum(row["nonfinite_elements"] for row in diagnostics),
              "test_armijo_violations":sum(row["step"]["step_accepted"] and not row["step"]["armijo_satisfied"] for row in diagnostics),
              "initial_all_tensors_byte_equal":all(row["all_tensors_byte_equal"] for row in initial_checks),
              "initial_max_error":max(row["max_error"] for row in initial_checks),
              "historical_max_error":max(row["max_error"] for row in checks),
              "historical_stream_mismatches":sum(row["stream_mismatches"]+abs(row["count"]-row["historical_count"]) for row in checks),
              "source_hashes_match":all(row["matches"] for row in sources),
              "normal_output_max_error":max(row["normal_output_max_error"] for row in diagnostics),
              "normal_state_max_error":max(row["normal_state_max_error"] for row in diagnostics),
              "W0_only_metric_max_error":max(row["W0_only_metric_max_error"] for row in diagnostics),
              "normal_metric_max_error":max(row["normal_metric_max_error"] for row in diagnostics),
              "config_matches_T002_except_methods":{k:v for k,v in config.items() if k!="methods"}=={k:v for k,v in source_config.items() if k!="methods"}}
    validity["passes"]=all(v if isinstance(v,bool) else v==0 for v in validity.values())
    result.update(controls=controls,historical=reference,training=training,trajectories=trajectories,mechanisms=mechanisms,
                  timings=timings,source_checkpoints=sources,initial_checks=initial_checks,historical_checks=checks,
                  environment={"revision":revision,"preregistration":"deeacd4","time_utc":datetime.now(timezone.utc).isoformat(),
                               "python":platform.python_version(),"torch":torch.__version__,"cuda":torch.version.cuda,"device":device,
                               "gpu":torch.cuda.get_device_name() if device.startswith("cuda") else None,"config":config,"source_config":source_config,
                               "episode_offset":offset,"last_training_index":end-1,"optimizer":"fresh Adam in both branches",
                               "snapshot_steps":list(snapshot_steps),"selection":"fixed final only; trajectories diagnostic"})
    result["rules"]=rules(result["aggregate"],result["per_seed"],controls,historical,validity,mechanisms)
    save_json(output/"historical_control_records.json",control_records)
    save_json(output/"results.json",result)
    save_json(output/"rules.json",result["rules"])
    save_json(output/"trajectories.json",trajectories)
    print("RULES "+json.dumps(result["rules"]),flush=True)
    return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--config",type=Path,default=Path("research_log/t007/config.json"))
    parser.add_argument("--expected-hashes",type=Path,default=Path("research_log/t007/source_hashes.json"))
    for name in ("source-root","t005-root","t006-root","output"):
        parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--device",default="cpu")
    parser.add_argument("--revision",required=True)
    args=parser.parse_args()
    run(read_json(args.config),args.source_root,args.t005_root,args.t006_root,read_json(args.expected_hashes),args.output,args.device,args.revision)


if __name__=="__main__":
    main()
