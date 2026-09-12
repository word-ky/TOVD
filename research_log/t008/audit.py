"""Frozen-state T008 audit. Task labels enter only offline outcome logging."""

import argparse
import csv
from datetime import datetime,timezone
import hashlib
import json
import math
from pathlib import Path
import platform

import torch

from research_log.t005.oracle_step_screen import score_output
from research_log.t007.experiment import parameter_drift,read_json,load_model,tensor_equality
from research_log.t008.runtime_features import extract_features
from research_log.t008.schema import FEATURES,FEATURE_METADATA
from research_log.t008.statistics import analyze
from tovd.synthetic.benchmark import episode_seed
from tovd.synthetic.semantic_episodes import SemanticWorld,WorldConfig


def save_json(path,data):
    path.write_text(json.dumps(data,indent=2,allow_nan=False)+"\n",encoding="utf-8")


def compare_memory(left,right):
    values=[(left.tokens,right.tokens),*((left.fast_state[k],right.fast_state[k]) for k in left.fast_state)]
    return {"bitwise_equal":all(torch.equal(a.view(torch.uint8),b.view(torch.uint8)) for a,b in values),
            "output_error":(left.tokens-right.tokens).abs().max().item(),
            "state_error":max((left.fast_state[k]-right.fast_state[k]).abs().max().item() for k in left.fast_state)}


def audit_episode(model,ep):
    X,T,Q=ep.X[None],ep.T[None],ep.Q[None]
    with torch.no_grad():
        normal=model(X,T,Q)
    features,before,candidate=extract_features(model,X,T,Q)
    # No task outcome exists until label-free extraction and candidate finish.
    with torch.no_grad():
        b=score_output(model,ep,before.tokens[0])
        a=score_output(model,ep,candidate.tokens[0])
        p0=model.logits(before.tokens,T).softmax(-1)
        p1=model.logits(candidate.tokens,T).softmax(-1)
    repeated,b0,c1=extract_features(model,X,T,Q)
    diag={k:v.item() for k,v in candidate.diagnostics.items()}
    checks={"normal":compare_memory(normal,candidate),"oracle_on_off":compare_memory(candidate,c1),
            "W0_repeat":compare_memory(before,b0),"features_exact":features==repeated,
            "feature_repeat_max_error":max(abs(features[k]-repeated[k]) for k in FEATURES),
            "pre_inner_loss_error":abs(features["inner_loss_before"]-diag["inner_loss_before"]),
            "pre_gradient_error":abs(features["gradient_norm"]-diag["inner_gradient_norm"]),
            "nonfinite_features":sum(not math.isfinite(v) for v in features.values()),
            "all_finite":diag["all_finite"] and torch.isfinite(before.tokens).all().item()}
    outcome={"before":b,"after":a,"delta_nll":a["nll"]-b["nll"],"delta_accuracy":a["accuracy"]-b["accuracy"]}
    outcome.update(harm=outcome["delta_nll"]>0,harm_gt_005=outcome["delta_nll"]>.05)
    return {"features":features,"outcomes":outcome,"checks":checks,"candidate_diagnostics":diag,
            "outputs":{"W0_tokens":before.tokens[0].tolist(),"C2_tokens":candidate.tokens[0].tolist(),
                       "W0_probabilities":p0[0].tolist(),"C2_probabilities":p1[0].tolist()}}


def run(config,sources,runs_root,t005_root,t007_root,output,device,revision):
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    output.mkdir(parents=True,exist_ok=True)
    raw_root=output/"records"
    raw_root.mkdir(exist_ok=True)
    world=SemanticWorld(WorldConfig(**config["world"]))
    source_checks=[]
    resolved={}
    for source in sources:
        path=runs_root/Path(source["path"]).relative_to("research_log/remote_runs")
        sha=hashlib.sha256(path.read_bytes()).hexdigest()
        source_checks.append({**source,"resolved_path":str(path.resolve()),"actual_sha256":sha,"matches":sha==source["sha256"]})
        resolved[source["state_id"]]=path
    save_json(output/"sources.json",source_checks)
    if not all(row["matches"] for row in source_checks):
        raise RuntimeError("T008 source hash mismatch; extraction has not started.")
    schema={"features":FEATURE_METADATA,
            "metadata_and_outcomes":{"is_label_free_feature":False,"fields":["seed","branch","step","regime","state_id","episode_seed","vocabulary_ids","query_ids","labels","delta_nll","delta_accuracy","harm","harm_gt_005","before_nll","after_nll","before_accuracy","after_accuracy","drift_W0","drift_key","drift_query","drift_total"]},
            "outputs":{"is_label_free_feature":False,"label_free_tensors":True,"note":"Recorded for replay; excluded from the fixed fourteen-scalar predictor vector."}}
    save_json(output/"schema.json",schema)
    save_json(output/"config.json",config)
    flat_rows=[]
    historical_checks=[]
    unchanged=[]
    summaries=[]
    for source in sources:
        seed,branch,step=source["seed"],source["branch"],source["step"]
        state=torch.load(resolved[source["state_id"]],map_location=device,weights_only=True)["state_dict"]
        original_source=next(x for x in sources if x["seed"]==seed and x["branch"]=="original_P")
        origin=torch.load(resolved[original_source["state_id"]],map_location="cpu",weights_only=True)["state_dict"]
        model=load_model(state,"O1_backtracking",config,device)
        drift=parameter_drift(state,origin)
        reference_branch="P_O0_resume" if branch=="original_P" else branch
        prior=read_json(t007_root/f"seed{seed}_{reference_branch}/step{step}_evaluations.json")["heldout"]
        for regime in ("easy","hard"):
            rows=[]
            original_reference=read_json(t005_root/f"seed{seed}_C2_{regime}.json") if branch=="original_P" else None
            reference_errors=[]
            original_errors=[]
            stream_mismatches=0
            for index in range(config["eval_episodes"]):
                ep_seed=episode_seed(seed,index,"test")
                ep=world.episode("test",regime,ep_seed).to(device)
                record=audit_episode(model,ep)
                meta={"state_id":source["state_id"],"seed":seed,"branch":branch,"step":step,"regime":regime,
                      "primary_unique":source["primary_unique"],"index":index,"episode_seed":ep_seed,
                      "vocabulary_ids":ep.vocabulary_ids.tolist(),"query_ids":ep.query_ids.tolist(),"labels":ep.labels.tolist()}
                record.update(meta)
                rows.append(record)
                o=record["outcomes"]
                flat_rows.append({**meta,**record["features"],"before_accuracy":o["before"]["accuracy"],"after_accuracy":o["after"]["accuracy"],
                                  "before_nll":o["before"]["nll"],"after_nll":o["after"]["nll"],"delta_nll":o["delta_nll"],
                                  "delta_accuracy":o["delta_accuracy"],"harm":o["harm"],"harm_gt_005":o["harm_gt_005"],
                                  "drift_W0":drift["W0"],"drift_key":drift["key_projection"],"drift_query":drift["query_projection"],"drift_total":drift["total_slow_state"]})
                old=prior[regime][index]
                reference_errors.extend(abs(o[stage][metric]-old["diagnostics"][stage][metric]) for stage in ("before","after") for metric in ("accuracy","nll","margin"))
                stream_mismatches+=int(old["episode_seed"]!=ep_seed or old["vocabulary_ids"]!=meta["vocabulary_ids"] or old["query_ids"]!=meta["query_ids"])
                if original_reference is not None:
                    old=original_reference[index]
                    original_errors.extend(abs(o[stage][metric]-old["diagnostics"][stage][metric]) for stage in ("before","after") for metric in ("accuracy","nll","margin"))
                    stream_mismatches+=int(old["episode_seed"]!=ep_seed)
            save_json(raw_root/f"{source['state_id']}_{regime}.json",rows)
            historical_checks.append({"state_id":source["state_id"],"regime":regime,"count":len(rows),"historical_count":len(prior[regime]),
                                      "max_error":max(reference_errors),"T005_max_error":max(original_errors) if original_errors else None,
                                      "stream_mismatches":stream_mismatches})
            checks=[r["checks"] for r in rows]
            summaries.append({"state_id":source["state_id"],"regime":regime,
                              "bitwise_equal":all(c[k]["bitwise_equal"] for c in checks for k in ("normal","oracle_on_off","W0_repeat")),
                              "output_max_error":max(c[k]["output_error"] for c in checks for k in ("normal","oracle_on_off","W0_repeat")),
                              "state_max_error":max(c[k]["state_error"] for c in checks for k in ("normal","oracle_on_off","W0_repeat")),
                              "features_exact":all(c["features_exact"] for c in checks),
                              "feature_repeat_max_error":max(c["feature_repeat_max_error"] for c in checks),
                              "pre_inner_loss_max_error":max(c["pre_inner_loss_error"] for c in checks),
                              "pre_gradient_max_error":max(c["pre_gradient_error"] for c in checks),
                              "nonfinite_features":sum(c["nonfinite_features"] for c in checks),"all_finite":all(c["all_finite"] for c in checks)})
        unchanged.append({"state_id":source["state_id"],**tensor_equality(model.state_dict(),state)})
        print(f"EXTRACTED state={source['state_id']} episodes={2*config['eval_episodes']}",flush=True)
    with (output/"episodes.csv").open("w",newline="",encoding="utf-8") as handle:
        writer=csv.DictWriter(handle,fieldnames=list(flat_rows[0]))
        writer.writeheader()
        writer.writerows({k:json.dumps(v) if isinstance(v,list) else v for k,v in row.items()} for row in flat_rows)
    save_json(output/"checks.json",{"historical":historical_checks,"normal_oracle":summaries,"parameters_unchanged":unchanged})
    validity={"source_hashes_match":all(x["matches"] for x in source_checks),"state_count":len(sources),"row_count":len(flat_rows),
              "expected_row_count":len(sources)*2*config["eval_episodes"],"historical_max_error":max(x["max_error"] for x in historical_checks),
              "T005_max_error":max(x["T005_max_error"] for x in historical_checks if x["T005_max_error"] is not None),
              "historical_stream_mismatches":sum(x["stream_mismatches"]+abs(x["count"]-x["historical_count"]) for x in historical_checks),
              "normal_oracle_bitwise_equal":all(x["bitwise_equal"] for x in summaries),"features_exact":all(x["features_exact"] for x in summaries),
              "output_max_error":max(x["output_max_error"] for x in summaries),"state_max_error":max(x["state_max_error"] for x in summaries),
              "pre_inner_loss_max_error":max(x["pre_inner_loss_max_error"] for x in summaries),"pre_gradient_max_error":max(x["pre_gradient_max_error"] for x in summaries),
              "nonfinite_features":sum(x["nonfinite_features"] for x in summaries),"all_outputs_finite":all(x["all_finite"] for x in summaries),
              "parameters_unchanged":all(x["all_tensors_byte_equal"] for x in unchanged)}
    validity["passes"]=validity["row_count"]==validity["expected_row_count"] and all(v if isinstance(v,bool) else v==0 for k,v in validity.items() if k not in ("state_count","row_count","expected_row_count"))
    result=analyze(flat_rows)
    result.update(validity=validity,feature_metadata=FEATURE_METADATA,
                  environment={"revision":revision,"preregistration":"c163c78","time_utc":datetime.now(timezone.utc).isoformat(),
                               "python":platform.python_version(),"torch":torch.__version__,"cuda":torch.version.cuda,"device":device,
                               "gpu":torch.cuda.get_device_name() if device.startswith("cuda") else None,"dtype":"float32","config":config,
                               "training":"none","selection":"none","primary_unique_states":sum(x["primary_unique"] for x in sources)})
    save_json(output/"results.json",result)
    save_json(output/"gates.json",result["gates"])
    print("VALIDITY "+json.dumps(validity),flush=True)
    print("PASSING "+json.dumps({"pre":result["passing_pre_features"],"rollback":result["passing_rollback_features"]}),flush=True)
    return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--config",type=Path,default=Path("research_log/t008/config.json"))
    parser.add_argument("--sources",type=Path,default=Path("research_log/t008/sources.json"))
    for name in ("runs-root","t005-root","t007-root","output"):
        parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--device",default="cpu")
    parser.add_argument("--revision",required=True)
    args=parser.parse_args()
    run(read_json(args.config),read_json(args.sources),args.runs_root,args.t005_root,args.t007_root,args.output,args.device,args.revision)


if __name__=="__main__":
    main()
