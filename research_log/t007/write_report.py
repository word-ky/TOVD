"""Format immutable T007 receipts; never select or modify experiment checkpoints."""

import argparse
import csv
import hashlib
import json
from pathlib import Path
import shutil
import statistics

TASK=Path(__file__).resolve().parent
ROOT=TASK.parents[1]


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_csv(path, rows):
    with path.open("w",encoding="utf-8",newline="") as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def figure_save(fig, name):
    fig.savefig(TASK/f"{name}.png",dpi=160)
    fig.savefig(TASK/f"{name}.svg")
    path=TASK/f"{name}.svg"
    path.write_text("\n".join(line.rstrip() for line in path.read_text(encoding="utf-8").splitlines())+"\n",encoding="utf-8")


def figures(data):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    colors={7:"#2878b5",17:"#d97925",27:"#38905b"}
    fig,axes=plt.subplots(2,3,figsize=(14,8),layout="constrained")
    panels=(("loss","Outer training NLL"),("accuracy","Outer training accuracy"),
            ("inner_loss_after","Inner loss after update"),("selected_etas","Mean inner step size"),
            ("update_norm","Fast update norm"),("eta_zero_fraction","No-update fraction"))
    for key,receipt in data["training"].items():
        seed=int(key.split("_")[0][4:])
        warm=key.endswith("P_C2_warm")
        for ax,(metric,title) in zip(axes.flat,panels):
            values=[statistics.mean(row[metric]) if isinstance(row[metric],list) else row[metric] for row in receipt["training_curve"]]
            values=[statistics.mean(values[max(0,i-19):i+1]) for i in range(len(values))]
            ax.plot(range(1,len(values)+1),values,color=colors[seed],linestyle="-" if warm else "--",
                    label=f"{'W2 C2' if warm else 'W1 O0'} / {seed}",linewidth=1.3)
            ax.set(title=title,xlabel="Continuation step")
            ax.grid(alpha=.18)
    axes[0,0].legend(fontsize=8,ncol=2,frameon=False)
    fig.suptitle("T007 warm-start continuation · training episodes only\n20-step trailing means; W1 and W2 inner losses are different objectives",fontsize=14)
    figure_save(fig,"training_curves")
    plt.close(fig)
    fig,axes=plt.subplots(2,2,figsize=(12,8),layout="constrained")
    for row,metric in enumerate(("accuracy","nll")):
        for col,stage in enumerate(("before","after")):
            ax=axes[row,col]
            for branch in ("P_O0_resume","P_C2_warm"):
                for seed in data["environment"]["config"]["seeds"]:
                    records=sorted((x for x in data["trajectories"] if x["branch"]==branch and x["seed"]==seed),key=lambda x:x["step"])
                    scale=100 if metric=="accuracy" else 1
                    ax.plot([x["step"] for x in records],[x["metrics"]["heldout"]["hard"][stage][metric]*scale for x in records],
                            color=colors[seed],linestyle="-" if branch=="P_C2_warm" else "--",marker="o",markersize=3,
                            label=f"{'W2 C2' if branch=='P_C2_warm' else 'W1 O0'} / {seed}")
            ax.set(title=f"Hard held-out · {'W0 only' if stage=='before' else 'C2 adapted'} · {metric}",xlabel="Continuation step")
            ax.grid(alpha=.18)
    axes[0,0].legend(fontsize=8,ncol=2,frameon=False)
    fig.suptitle("T007 checkpoint trajectories · diagnosis only\nSteps 0 / 50 / 100 / 200 / 400; fixed step 400 is the only primary result",fontsize=14)
    figure_save(fig,"heldout_trajectories")
    plt.close(fig)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--run",type=Path,required=True)
    args=parser.parse_args()
    source=args.run/"artifacts/t007"
    data=read_json(source/"results.json")
    for name in ("results.json","rules.json","trajectories.json","sources.json"):
        shutil.copyfile(source/name,TASK/name)
    agg=data["aggregate"]
    rules=data["rules"]
    lines=["# T007 warm-start origin audit", "",
           f"Run `{args.run.name}`; tested code `{data['environment']['revision']}`; preregistration `deeacd4`.","",
           "W1=P_O0_resume, W2=P_C2_warm. Both start from the same final T002 P tensors, reset Adam moments,",
           "and continue .001 Adam for400x4 episodes, indices1600..3199. Final400 is primary; all intermediate",
           "checkpoints are diagnostic only. O1+C2 is label-free; oracle task gradients stay offline.","",
           "## Fixed decision rules", "", "| Rule | Pass | Evidence |", "| --- | --- | --- |"]
    for name,value in rules.items():
        lines.append(f"| {name} | {'PASS' if value['passes'] else 'FAIL'} | See rules.json for every threshold and scalar. |")
    r2,r3,r4,r5,r6=[rules[k] for k in ("rule2_fast_value","rule3_preservation","rule4_objective_effect","rule5_control_value","rule6_easy_mechanism")]
    if all(r["passes"] for r in (r2,r3,r5,r6)):
        conclusion="Warm-start C2 passes the predefined viability criteria; Research Lead may review a small detector task. No integration is started under T007."
    else:
        conclusion="Warm-start C2 does not meet all predefined viability criteria; do not proceed to detector integration."
    if not r4["passes"]:
        conclusion+=" W2 is worse than matched W1+C2 in both hard accuracy and NLL, evidence of objective-specific continuation degradation."
    w1h,w1e=agg["P_O0_resume"]["hard"],agg["P_O0_resume"]["easy"]
    w2h=agg["P_C2_warm"]["hard"]
    lines += ["",conclusion,"",
              f"W2 hard accuracy is {100*w2h['after.accuracy']['mean']:.4f}%; its NLL control gate passes against B0, but its accuracy remains below B2. This is not a repeat of the T006 Rule3 control failure.",
              f"W1+C2 retains hard performance ({100*w1h['after.accuracy']['mean']:.4f}%, NLL {w1h['after.nll']['mean']:.6f}), yet harms easy accuracy by {-100*w1e['after.accuracy_delta']['mean']:.4f}pp and NLL by {w1e['after.nll_delta']['mean']:.6f} on average.",
              "W2 easy seed27 loses7.625pp with NLL+.114365 despite the positive aggregate. W2 beats W1 on hard seed17, but loses on seeds7/27: the mean objective-specific effect is not uniform across seeds.",
              "Retain T005 as a fixed-checkpoint mechanism reference, not evidence of safety for arbitrary continued checkpoints. These results do not support adding more C2-training tricks or integrating a detector under this task.",
              "","## Final held-out task metrics","",
              "Mean ± sample SD across seeds; accuracy in percent. W0/adapted are the same checkpoint.","",
              "| Model | Regime | Path | Accuracy (%) | NLL | Margin |","| --- | --- | --- | --- | --- | --- |"]
    table=[]
    for name,regimes in {**data["historical"]["aggregate"],**agg}.items():
        for regime,metrics in regimes.items():
            for stage in ("before","after"):
                vals=[]
                record={"model":name,"regime":regime,"path":"W0" if stage=="before" else "C2"}
                for metric in ("accuracy","nll","margin"):
                    v=metrics[f"{stage}.{metric}"]
                    scale=100 if metric=="accuracy" else 1
                    vals.append(f"{v['mean']*scale:.6f} ± {v['std']*scale:.6f}")
                    record[metric+"_mean"]=v["mean"]
                    record[metric+"_sd"]=v["std"]
                table.append(record)
                lines.append(f"| {name} | {regime} | {record['path']} | "+" | ".join(vals)+" |")
    for name,regimes in data["controls"].items():
        for regime,metrics in regimes.items():
            vals=[]
            record={"model":"T002_"+name,"regime":regime,"path":"original"}
            for metric in ("accuracy","nll","margin"):
                v=metrics[metric]
                scale=100 if metric=="accuracy" else 1
                vals.append(f"{v['mean']*scale:.6f} ± {v['std']*scale:.6f}")
                record[metric+"_mean"]=v["mean"]
                record[metric+"_sd"]=v["std"]
            table.append(record)
            lines.append(f"| T002 {name} | {regime} | original | "+" | ".join(vals)+" |")
    write_csv(TASK/"task_metrics.csv",table)
    lines += ["","## Per-seed fast value","","Delta=adapted minus own W0. Positive NLL delta is harm.","",
              "| Branch | Seed | Regime | W0 accuracy | C2 accuracy | Delta pp | W0 NLL | C2 NLL | Delta NLL |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for branch,regimes in data["per_seed"].items():
        for regime,seeds in regimes.items():
            for seed,m in seeds.items():
                keys=("before.accuracy","after.accuracy","after.accuracy_delta","before.nll","after.nll","after.nll_delta")
                values=[m[key]["mean"]*(100 if i<3 else 1) for i,key in enumerate(keys)]
                lines.append(f"| {branch} | {seed} | {regime} | "+" | ".join(f"{x:.6f}" for x in values)+" |")
    lines += ["","## Final train-versus-held-out metrics","",
              "Training diagnostics use the final100 easy and100 hard continuation episodes, all seen by step400.",
              "The training-objective path uses O0 for W1 and C2 for W2; both other paths use common W0/C2 evaluation.","",
              "| Branch | Seed | Split | Regime | Path | Accuracy (%) | NLL | Margin |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    trajectory_rows=[]
    for row in data["trajectories"]:
        for split,regimes in row["metrics"].items():
            for regime,paths in regimes.items():
                for path,metrics in paths.items():
                    trajectory_rows.append({"branch":row["branch"],"seed":row["seed"],"step":row["step"],"split":split,"regime":regime,"path":path,**metrics})
                    if row["step"]==400:
                        lines.append(f"| {row['branch']} | {row['seed']} | {split} | {regime} | {path} | {100*metrics['accuracy']:.6f} | {metrics['nll']:.6f} | {metrics['margin']:.6f} |")
    write_csv(TASK/"trajectory_metrics.csv",trajectory_rows)
    lines += ["",
              "On the common C2 path, final seen-training hard accuracy/NLL are W1 64.7917%/1.004811 and W2 62.5833%/1.092444; held-out values are45.375%/1.220324 and43.5417%/1.227928.",
              "W2 is already weaker on this seen-training comparison, so the observed gap is not solely extra held-out overfitting. The fixed budget does not identify the asymptotic optimization limit.",
              "Under each branch's own training objective, seen-training hard accuracy is W1(O0)74.2083% versus W2(C2)62.5833%. Full trajectory rows preserve both objective-specific and common-C2 evaluations."]
    lines += ["","## Parameter drift and training","",
              "L2 from exact starting T002 P;1616 W0+256 key+256 query=2128 total. Classifier has0 parameters and fixed temperature.1.","",
              "| Branch / seed | W0 drift | Key drift | Query drift | Total drift | Seconds | Nonfinite steps | Armijo violations |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    training_rows=[]
    for key,receipt in data["training"].items():
        d=receipt["drift"]
        lines.append(f"| {key} | {d['W0']:.6f} | {d['key_projection']:.6f} | {d['query_projection']:.6f} | {d['total_slow_state']:.6f} | {receipt['train_seconds']:.3f} | {sum(not r['finite'] for r in receipt['training_curve'])} | {sum(r['armijo_violations'] for r in receipt['training_curve'])} |")
        for row in receipt["training_curve"]:
            training_rows.append({"branch_seed":key,**{k:json.dumps(v) if isinstance(v,list) else v for k,v in row.items()}})
    write_csv(TASK/"training_curves.csv",training_rows)
    lines += ["","## Offline mechanism diagnostics","",
              "| Branch | Regime | O1 loss before | After | Raw gradient norm | Update norm | Task cosine | Task dot | Episode NLL improves | Query NLL improves |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    # Metric names are taken directly from the existing T005 paired diagnostics.
    scalar_rows=[]
    for branch,regimes in agg.items():
        for regime,m in regimes.items():
            for key,value in m.items():
                scalar_rows.append({"branch":branch,"regime":regime,"metric":key,"seed_mean":value["mean"],"seed_sd":value["std"],**value["pooled"]})
            keys=("O1_inner_loss_before","O1_inner_loss_after","alignment.gradient_norm","after.update_norm","alignment.cosine","alignment.dot","after.episode_nll_improves","after.query_nll_improves_fraction")
            lines.append(f"| {branch} | {regime} | "+" | ".join(f"{m[k]['mean']:.6f}" for k in keys)+" |")
    write_csv(TASK/"aggregate.csv",scalar_rows)
    per_seed_rows=[]
    for branch,regimes in data["per_seed"].items():
        for regime,seeds in regimes.items():
            for seed,metrics in seeds.items():
                per_seed_rows.append({"branch":branch,"regime":regime,"seed":seed,
                                      **{key:value["mean"] for key,value in metrics.items()}})
    write_csv(TASK/"per_seed_diagnostics.csv",per_seed_rows)
    lines += ["","Per-seed diagnostic means are also tabulated in per_seed_diagnostics.csv; full distributions in results.json."]
    lines += ["","## Per-seed C2 selection and normal timing","",
              "Timing excludes oracle analysis:3 warmups +3 complete normal-forward passes, synchronized CUDA.","",
              "| Branch | Seed | Regime | Eta counts | Zero count | Armijo violations | C2 ms/episode | C2/P | C2/O1-fixed |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    from collections import Counter
    for branch,seeds in data["timings"].items():
        for seed,regimes in seeds.items():
            for regime,t in regimes.items():
                raw=read_json(source/f"seed{seed}_{branch}/{regime}_oracle.json")
                counts=Counter(str(round(r["diagnostics"]["step"]["chosen_eta"],8)) for r in raw)
                c2=t["C2"]["mean_ms_per_episode"]
                violations=sum(r["diagnostics"]["step"]["step_accepted"] and not r["diagnostics"]["step"]["armijo_satisfied"] for r in raw)
                lines.append(f"| {branch} | {seed} | {regime} | {dict(counts)} | {counts.get('0.0',0)} | {violations} | {c2:.4f} | {c2/t['P']['mean_ms_per_episode']:.4f} | {c2/t['O1_fixed']['mean_ms_per_episode']:.4f} |")
    lines += ["","## Vocabulary / reset diagnostics","",
              "| Branch | Seed | Easy-hard state delta | Unrelated state delta | Unrelated output delta | Max reset state | Max reset output |", "| --- | --- | --- | --- | --- | --- | --- |"]
    for branch,seeds in data["mechanisms"].items():
        for seed,receipt in seeds.items():
            m=receipt["mean"]
            lines.append(f"| {branch} | {seed} | {m['easy_hard_state_delta']:.6f} | {m['unrelated_state_delta']:.6f} | {m['unrelated_output_delta']:.6f} | {max(x['reset_state_delta'] for x in receipt['episodes']):.3g} | {max(x['reset_output_delta'] for x in receipt['episodes']):.3g} |")
    lines += ["","## Validity and limitations","","```json",json.dumps(rules,indent=2),"```","",
              "Raw historical controls/references, step0 equality and all checkpoint hashes are retained. Normal/runtime and oracle paths are cross-checked.",
              "Fresh Adam and continued episode segment are preregistered choices; this is model warm-start continuation, not optimizer-state resume.",
              "Three seeds and synthetic observations only. Inner descent does not guarantee per-episode task improvement; all seed harms remain visible.",
              "No test-guided checkpoint selection, extra objectives, detector or T008. Research Lead owns acceptance and the next task.","",
              "![Training curves](training_curves.png)","","![Diagnostic held-out trajectories](heldout_trajectories.png)",""]
    (TASK/"RESULTS.md").write_text("\n".join(lines),encoding="utf-8")
    manifest=[{"path":str(p.relative_to(ROOT)).replace('\\','/'),"bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}
              for p in sorted(args.run.rglob("*")) if p.is_file()]
    origin_replay=[]
    for branch in ("P_O0_resume","P_C2_warm"):
        for seed in data["environment"]["config"]["seeds"]:
            zero=read_json(source/f"seed{seed}_{branch}/step0_evaluations.json")["heldout"]
            for regime in ("easy","hard"):
                historical=read_json(source/f"seed{seed}_T005_frozen_C2_{regime}.json")
                error=max(abs(a["diagnostics"][stage][metric]-b["diagnostics"][stage][metric]) for a,b in zip(zero[regime],historical)
                          for stage in ("before","after") for metric in ("accuracy","nll","margin"))
                origin_replay.append({"branch":branch,"seed":seed,"regime":regime,"count":len(historical),"max_metric_error":error})
    verification={"run":args.run.name,"validity":rules["rule1_validity"],"source_checkpoints":data["source_checkpoints"],
                  "initial_checks":data["initial_checks"],"historical_checks":data["historical_checks"],"step0_vs_T005_replay":origin_replay,
                  "final_oracle_episodes":sum(len(read_json(p)) for p in source.glob("seed*/*_oracle.json")),"artifact_manifest":manifest}
    (TASK/"verification.json").write_text(json.dumps(verification,indent=2)+"\n",encoding="utf-8")
    figures(data)
    print(json.dumps(rules,indent=2))


if __name__=="__main__":
    main()
