"""Render T006 immutable experiment receipts and training-only curves."""

import csv
import hashlib
import json
from pathlib import Path
import shutil
import statistics

ROOT=Path(__file__).resolve().parents[2]
TASK=ROOT/"research_log/t006"
RUN=ROOT/"research_log/remote_runs/20260912-065105-tovd-t006-a6000"
SOURCE=RUN/"artifacts/t006"
T002=ROOT/"research_log/remote_runs/20260912-023122-tovd-t002-a6000/artifacts/t002"


def plot_training(data):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(2,3,figsize=(14,8),layout="constrained")
    panels=[("loss","Outer training loss"),("accuracy","Training accuracy"),
            ("inner_loss_after","O1 inner loss after update"),("selected_etas","Mean selected eta"),
            ("update_norm","Fast update norm"),("eta_zero_fraction","No-update fraction")]
    for seed,receipt in data["training"].items():
        curve=receipt["curve"]
        for ax,(metric,title) in zip(axes.flat,panels):
            values=[statistics.mean(row[metric]) if isinstance(row[metric],list) else row[metric] for row in curve]
            smooth=[statistics.mean(values[max(0,index-19):index+1]) for index in range(len(values))]
            ax.plot(range(1,len(values)+1),smooth,label="Seed "+seed,linewidth=1.6)
            ax.set(title=title,xlabel="Outer step")
            ax.grid(alpha=.2)
    axes[0,0].legend(frameon=False)
    fig.suptitle("T006 · C2 meta-training\nTraining episodes only; 20-step trailing means; fixed final checkpoint",fontsize=15)
    fig.savefig(TASK/"training_curves.png",dpi=160)
    fig.savefig(TASK/"training_curves.svg")
    svg=TASK/"training_curves.svg"
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines())+"\n",encoding="utf-8")
    plt.close(fig)


def main():
    data=json.loads((SOURCE/"results.json").read_text())
    for name in ("results.json","rules.json","meta_gradient_initial.json","meta_gradient_final.json"):
        shutil.copyfile(SOURCE/name,TASK/name)
    checks=[]
    for source in data["source_checkpoints"]:
        path=T002/f"seed{source['seed']}_{source['method']}/checkpoint.pt"
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        checks.append({"seed":source["seed"],"method":source["method"],"expected_sha256":source["sha256"],"actual_sha256":digest,"matches":digest==source["sha256"]})
    records=[row for path in sorted(SOURCE.glob("seed*_P_C2_meta_*.json")) for row in json.loads(path.read_text())]
    config=data["environment"]["config"]
    original=data["environment"]["source_config"]
    verification={"source_hashes":checks,"only_config_method_changed":{k:v for k,v in config.items() if k!="methods"}=={k:v for k,v in original.items() if k!="methods"},
                  "heldout_records":len(records),"query_changes":sum(len(row["diagnostics"]["after"]["query_nll_delta"]) for row in records),
                  "rule1_validity":data["rules"]["rule1_validity"],"initial_tensor_checks":data["initial_tensor_checks"],
                  "control_checks":data["control_checks"],
                  "artifact_manifest":[{"path":str(path.relative_to(ROOT)),"bytes":path.stat().st_size,"sha256":hashlib.sha256(path.read_bytes()).hexdigest()}
                                       for path in sorted(RUN.rglob("*")) if path.is_file()]}
    (TASK/"verification.json").write_text(json.dumps(verification,indent=2)+"\n")
    with (TASK/"aggregate.csv").open("w",newline="") as handle:
        writer=csv.writer(handle)
        writer.writerow(["regime","metric","seed_mean","seed_sd","pooled_count","min","p05","median","p95","max"])
        for regime,metrics in data["aggregate"]["P_C2_meta"].items():
            for key,value in metrics.items():
                writer.writerow([regime,key,value["mean"],value["std"],*[value["pooled"][name] for name in ("count","min","p05","median","p95","max")]])
    with (TASK/"training_curves.csv").open("w",newline="") as handle:
        fields=["step","loss","accuracy","inner_loss_before","inner_loss_after","inner_gradient_norm","update_norm","selected_etas","backtracking_trials","eta_zero_fraction","armijo_violations","finite"]
        writer=csv.writer(handle)
        writer.writerow(["seed",*fields])
        for seed,receipt in data["training"].items():
            for row in receipt["curve"]:
                writer.writerow([seed,*[json.dumps(row[key]) if isinstance(row[key],list) else row[key] for key in fields]])
    rules=data["rules"]
    lines=["# T006 controlled C2 meta-training", "",rules["recommendation"],"",
           "Rules 1, 2, 4 and 5 pass; Rule 3 fails. Fast adaptation improves its own new W0, "
           "but absolute hard accuracy is 34.625%, ten percentage points below B2. This is a "
           "control-competitiveness failure, not loss of all fast-path value or a gradient-engineering failure.","",
           "Engineering status VERIFIED; research acceptance pending. No detector or T007.","",
           "Tested code 65299db5f1127407f856872b732f2b2b7051383e; preregistration f9f4137. "
           "Run 20260912-065105-tovd-t006-a6000, physical A6000 GPU 1. Three seeds, "
           "400 Adam(.001) steps x4 balanced training episodes, final checkpoint only. "
           "Only the method changes from the original T002 config; C2 sequence and Armijo constant are unchanged.","",
           "Task scoring and task gradients are offline oracle diagnostics. Training labels enter outer CE only; "
           "inner adaptation and eta selection remain label-free. Selected eta is held constant when differentiating "
           "the accepted update. Stable-region finite differences and eta switches are reported separately.","",
           "Mean ± sample SD across seeds; accuracy in percent. All historical controls were re-evaluated on the same held-out streams.",""]
    def table(title,fields):
        lines.extend(["## "+title,"","| Regime | "+" | ".join(label for _,label,_ in fields)+" |",
                      "| --- | "+" | ".join("---" for _ in fields)+" |"])
        for regime,metrics in data["aggregate"]["P_C2_meta"].items():
            cells=[f"{metrics[key]['mean']*scale:.6f} ± {metrics[key]['std']*scale:.6f}" for key,_,scale in fields]
            lines.append(f"| {regime} | "+" | ".join(cells)+" |")
        lines.append("")
    table("Own W0 versus adapted",[("before.accuracy","W0 accuracy %",100),("after.accuracy","Adapted accuracy %",100),
          ("before.nll","W0 NLL",1),("after.nll","Adapted NLL",1),("after.nll_delta","Delta NLL",1),
          ("before.margin","W0 margin",1),("after.margin","Adapted margin",1)])
    lines += ["## Historical matched controls","","| Method | Regime | Accuracy % | NLL | Margin |","| --- | --- | --- | --- | --- |"]
    for method,regimes in data["controls"].items():
        for regime,metrics in regimes.items():
            cells=[f"{metrics[key]['mean']*scale:.6f} ± {metrics[key]['std']*scale:.6f}" for key,scale in (("accuracy",100),("nll",1),("margin",1))]
            lines.append(f"| T002 {method} (re-evaluated) | {regime} | "+" | ".join(cells)+" |")
    for regime,metrics in data["historical_T005_references"]["C2"].items():
        cells=[f"{metrics[key]['mean']*scale:.6f} ± {metrics[key]['std']*scale:.6f}" for key,scale in (("after.accuracy",100),("after.nll",1),("after.margin",1))]
        lines.append(f"| T005 frozen C2 (stored reference) | {regime} | "+" | ".join(cells)+" |")
    lines += ["","Historical controls are separately trained T002 checkpoints, not new T006 runs. "
              "T005 C2 starts from original P W0; it is not the same initialization as newly meta-trained C2.",""]
    table("Inner/update and task alignment",[("O1_inner_loss_before","Inner before",1),("O1_inner_loss_after","Inner after",1),
          ("alignment.gradient_norm","Raw O1 gradient norm",1),("after.update_norm","Actual update norm",1),
          ("alignment.cosine","Task cosine",1),("alignment.dot","Task dot",1)])
    table("Task improvement fractions and selector",[("after.episode_nll_improves","Episodes improve %",100),
          ("after.query_nll_improves_fraction","Queries improve %",100),("step.chosen_eta","Mean eta",1),
          ("step.backtracking_trials","Mean trials",1),("step.step_rejected","Eta-zero fraction",1),
          ("step.armijo_satisfied","Armijo satisfied fraction",1)])
    lines += ["## Per-seed paired outcomes","",
              "| Regime | Seed | W0 accuracy % | Adapted accuracy % | Delta accuracy pp | W0 NLL | Adapted NLL | Delta NLL | Task cosine |",
              "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for regime,seeds in data["per_seed"]["P_C2_meta"].items():
        for seed,metrics in seeds.items():
            fields=[("before.accuracy",100),("after.accuracy",100),("after.accuracy_delta",100),
                    ("before.nll",1),("after.nll",1),("after.nll_delta",1),("alignment.cosine",1)]
            lines.append(f"| {regime} | {seed} | "+" | ".join(f"{metrics[key]['mean']*scale:.6f}" for key,scale in fields)+" |")
    lines += ["","## Exact preregistered rule decisions","","```json",json.dumps(rules,indent=2),"```","",
              "Rule 3 uses the highest-accuracy control for its accuracy branch and the lowest-NLL control "
              "for its NLL branch, with non-worsening of the other metric against the same comparator. "
              "This interpretation was fixed at f9f4137 before T006 outcomes. All control results are shown above.","",
              "## Training evidence","","![Training-only curves](training_curves.png)","",
              "Plot shows trailing 20-step means for readability, not training or checkpoint selection. "
              "All 1,200 raw step records, including each batch's four selected etas and trial counts, "
              "are in training_curves.csv and the original seed training.json files.","",
              "| Seed | Steps | Last outer loss | Last batch accuracy % | W0 drift | Training seconds | Eta counts |",
              "| --- | --- | --- | --- | --- | --- | --- |"]
    for seed,receipt in data["training"].items():
        curve=receipt["curve"]
        counts={}
        for row in curve:
            for eta in row["selected_etas"]:
                key=str(round(eta,8)); counts[key]=counts.get(key,0)+1
        lines.append(f"| {seed} | {len(curve)} | {curve[-1]['loss']:.6f} | {curve[-1]['accuracy']*100:.3f} | {receipt['W0_outer_drift']:.6f} | {receipt['train_seconds']:.3f} | {counts} |")
    lines += ["","## Initial/final selector and meta-gradient probes","",
              "Fixed first 20 training episodes per seed, independent of held-out outcomes. "
              "Float64 copies; W0 output.weight directions and perturbation magnitudes were preregistered. "
              "Epsilon1e-5 is the numerical agreement check. Larger probes characterize selector regions "
              "and finite-step truncation, not a global-smoothness guarantee.","",
              "| Phase | Epsilon | Probes | Switches | Switch fraction | Stable max absolute FD error | Stable tolerance disagreements |",
              "| --- | --- | --- | --- | --- | --- | --- |"]
    for phase in ("initial","final"):
        receipt=json.loads((SOURCE/f"meta_gradient_{phase}.json").read_text())
        for epsilon,row in receipt["summary"]["by_epsilon"].items():
            lines.append(f"| {phase} | {epsilon} | {row['count']} | {row['switch_count']} | {row['switch_fraction']:.6f} | {row['stable_max_absolute_error']:.9g} | {row['stable_disagreements']} |")
    lines += ["","Switched probes have stable_region_agreement=null and are not graded as smooth derivatives. "
              "Full gradients, base/plus/minus etas, analytic/numerical derivatives, and seed summaries are in meta_gradient_{initial,final}.json.","",
              "## Held-out chosen eta counts","","| Seed/regime | Eta counts |","| --- | --- |"]
    for name,counts in data["eta_counts"].items():
        lines.append(f"| {name} | {counts} |")
    lines += ["","## Matched normal-forward latency","",
              "Same newly trained tensors for C2, original P objective and O1_fixed; three warmed complete "
              "passes per seed/regime with GPU synchronization. Oracle scoring excluded. Prototype CPU/"
              "GPU synchronization overhead and shared-host activity limit interpretation of small differences.","",
              "| Seed | Regime | C2 ms | P same W0 ms | O1 fixed same W0 ms | C2/P | C2/O1 fixed |",
              "| --- | --- | --- | --- | --- | --- | --- |"]
    for seed,regimes in data["timings"].items():
        for regime,measurements in regimes.items():
            c,p,o=[measurements[name]["mean_ms_per_episode"] for name in ("C2","P_same_W0","O1_fixed_same_W0")]
            lines.append(f"| {seed} | {regime} | {c:.5f} | {p:.5f} | {o:.5f} | {c/p:.5f} | {c/o:.5f} |")
    lines += ["","## Vocabulary, reset and provenance","",
              "| Seed | Easy/hard state delta | Unrelated state delta | Unrelated output delta | Reset state max | Reset output max |",
              "| --- | --- | --- | --- | --- | --- |"]
    for seed,receipt in data["mechanisms"].items():
        m=receipt["mean"]; rows=receipt["episodes"]
        lines.append(f"| {seed} | {m['easy_hard_state_delta']:.6f} | {m['unrelated_state_delta']:.6f} | {m['unrelated_output_delta']:.6f} | {max(r['reset_state_delta'] for r in rows):.6g} | {max(r['reset_output_delta'] for r in rows):.6g} |")
    lines += ["",f"New held-out diagnoses: {len(records)}, per-query changes: {verification['query_changes']}. "
              "Twelve source checkpoints re-evaluated; full hashes, stream equality, unchanged initial tensors "
              "and run manifest are in verification.json. Raw diagnostic scores match normal evaluation "
              "and the explicit disabled-update path as recorded in Rule 1.","",
              "## Interpretation","",
              "The hard fast-path gain survives meta-training: all three seeds improve NLL and accuracy "
              "over their own W0. The learned W0 itself has low held-out accuracy (29.91667%), so "
              "a +4.70833pp adaptive gain reaches only 34.625%. The new adapted model is worse than "
              "B0, B1, B2, original P and the historical frozen-C2 result on both hard mean accuracy and NLL. "
              "The experiment does not isolate the cause of weaker absolute generalization.","",
              "Hard task alignment is retained and strengthened relative to original P, with cosine .320918 "
              "versus -.011157. All hard held-out episodes now accept eta=.05 on the first trial. "
              "This is observed controller behavior; it does not prove that the selector is globally smooth "
              "or that ignoring line search would be equivalent throughout training.","",
              "Easy aggregate safety passes with no preregistered major seed flag. Seed 27 nevertheless "
              "has mild own-W0 harm (+.069829 NLL, -1.625pp), retained in the per-seed table. "
              "No claim of uniform per-episode or per-seed improvement is warranted.","",
              "Recommend stop/reframe the current meta-training formulation before detector integration. "
              "Do not reinterpret Rule 3 as optional, tune the fixed schedule after these outcomes, "
              "or erase the positive Rule 2 mechanism evidence. Any further diagnosis requires Research Lead review.","",
              "## Artifacts","",
              "Complete checkpoints, training logs, control records, probe receipts and held-out raw records: "
              "research_log/remote_runs/20260912-065105-tovd-t006-a6000/. "
              "results.json / aggregate.csv retain all distributions; rules.json records the fixed decisions. "
              "No source checkpoint or unsuccessful outcome is removed."]
    (TASK/"RESULTS.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    plot_training(data)
    print(json.dumps(rules,indent=2))
    print("Source hashes match:",all(row["matches"] for row in checks))


if __name__=="__main__":
    main()
