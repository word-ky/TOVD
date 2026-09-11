"""Format immutable T005 receipts; no model execution or result selection."""

import csv
import hashlib
import json
from pathlib import Path
import shutil
import statistics

ROOT=Path(__file__).resolve().parents[2]
TASK=ROOT/"research_log/t005"
RUN=ROOT/"research_log/remote_runs/20260912-053826-tovd-t005-a6000"
SOURCE=RUN/"artifacts/t005"
T002=ROOT/"research_log/remote_runs/20260912-023122-tovd-t002-a6000/artifacts/t002"


def main():
    data=json.loads((SOURCE/"frozen_step_screen.json").read_text())
    for name in ("frozen_step_screen.json","rules.json"):
        shutil.copyfile(SOURCE/name,TASK/name)
    records=[row for file in sorted(SOURCE.glob("seed*.json")) for row in json.loads(file.read_text())]
    source_hashes=[]
    for entry in data["environment"]["source_checkpoints"]:
        path=T002/f"seed{entry['seed']}_P/checkpoint.pt"
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        source_hashes.append({"seed":entry["seed"],"expected_sha256":entry["sha256"],"actual_sha256":digest,"matches":digest==entry["sha256"]})
    mechanism_rows=[row for seeds in data["mechanisms"].values() for receipt in seeds.values() for row in receipt["episodes"]]
    verification={"records":len(records),"queries":sum(len(row["diagnostics"]["after"]["query_nll_delta"]) for row in records),
                  "source_hashes":source_hashes,"historical_checks":data["historical_checks"],
                  "normal_output_max_error":max(row["diagnostics"]["normal_output_max_error"] for row in records),
                  "normal_state_max_error":max(row["diagnostics"]["normal_state_max_error"] for row in records),
                  "nonfinite_elements":sum(row["diagnostics"]["nonfinite_elements"] for row in records),
                  "all_records_finite":all(row["diagnostics"]["all_finite"] for row in records),
                  "mechanism_records":len(mechanism_rows),
                  "reset_state_max":max(row["reset_state_delta"] for row in mechanism_rows),
                  "reset_output_max":max(row["reset_output_delta"] for row in mechanism_rows),
                  "permutation_output_max_error":max(row["permutation_output_max_error"] for row in mechanism_rows),
                  "artifact_manifest":[{"path":str(path.relative_to(ROOT)),"bytes":path.stat().st_size,"sha256":hashlib.sha256(path.read_bytes()).hexdigest()}
                                       for path in sorted(RUN.rglob("*")) if path.is_file()]}
    (TASK/"verification.json").write_text(json.dumps(verification,indent=2)+"\n")
    with (TASK/"aggregate.csv").open("w",newline="") as handle:
        writer=csv.writer(handle)
        writer.writerow(["method","regime","metric","seed_mean_average","seed_mean_std","pooled_count","pooled_min","pooled_p05","pooled_median","pooled_p95","pooled_max"])
        for method,regimes in data["aggregate"].items():
            for regime,metrics in regimes.items():
                for metric,value in metrics.items():
                    writer.writerow([method,regime,metric,value["mean"],value["std"],*[value["pooled"][key] for key in ("count","min","p05","median","p95","max")]])
    lines=["# T005 frozen O1 step-control diagnosis", "",
           "C2 passes the preregistered descent-safe and task-useful rules. C1 fails the full scale-rescue rule "
           "because hard NLL and accuracy both worsen versus C0 despite a large easy recovery. "
           "Recommend Research Lead review a controlled meta-training task for C2; no training starts under T005.", "",
           "Run 20260912-053826-tovd-t005-a6000; tested code f2b9722ae8a1ad68e0e529488e68f88c170125de; preregistration 7b8949e.", "",
           "C0 = O1_fixed; C1 = O1_norm_matched; C2 = O1_backtracking. Original O0 and C0 are immutable controls. "
           "All metrics below use the same frozen T002 P checkpoints and 600 held-out episodes per method. "
           "Task-gradient diagnostics use offline labels only; runtime step selection is label-free. "
           "No outer training, objective/temperature/generator change, detector integration or task-label step selection.", "",
           "Values are mean ± sample SD across seeds 7/17/27; delta is after minus own W0. Full per-seed and pooled distributions in frozen_step_screen.json / aggregate.csv.", ""]
    def table(title,fields,methods=None):
        lines.extend(["## "+title,"","| Method | Regime | "+" | ".join(label for _,label,_ in fields)+" |",
                      "| --- | --- | "+" | ".join("---" for _ in fields)+" |"])
        for method in methods or data["aggregate"]:
            for regime,metrics in data["aggregate"][method].items():
                cells=[f"{metrics[key]['mean']*scale:.5f} ± {metrics[key]['std']*scale:.5f}" for key,_,scale in fields]
                lines.append(f"| {method} | {regime} | "+" | ".join(cells)+" |")
        lines.append("")
    table("Task before/after",[("before.accuracy","W0 accuracy %",100),("after.accuracy","W* accuracy %",100),
          ("before.nll","W0 NLL",1),("after.nll","W* NLL",1),("after.nll_delta","ΔNLL",1),
          ("before.margin","W0 margin",1),("after.margin","W* margin",1)])
    table("Direction and realized update",[("alignment.cosine","Raw task cosine",1),("alignment.dot","Raw task dot",1),
          ("alignment.gradient_norm","Objective gradient norm",1),("raw_O1_alignment.gradient_norm","Raw O1 norm",1),
          ("after.update_norm","Actual update norm",1),("effective_direction.cosine","Realized direction cosine",1)])
    lines += ["Raw alignment uses g0 for O0 and g1 for C0/C1/C2. C2 rejected steps still have a raw g1 diagnostic; "
              "their realized direction is zero. Effective-direction dot products are in JSON/CSV.",""]
    table("Inner losses and task improvement fractions",[("O1_inner_loss_before","O1 loss before",1),
          ("O1_inner_loss_after","O1 loss after",1),("own_inner_loss_after","Own objective after",1),
          ("after.episode_nll_improves","Episodes improve %",100),("after.query_nll_improves_fraction","Queries improve %",100)])
    table("C1 step budget",[("step.step_scale","Scale",1),("step.O0_update_budget","O0 actual budget",1),
          ("step.budget_absolute_error","Absolute budget error",1),("step.norm_guarded","Guarded fraction",1)],["C1"])
    for regime,metrics in data["aggregate"]["C1"].items():
        scale=metrics["step.step_scale"]["pooled"]
        error=metrics["step.budget_absolute_error"]["pooled"]
        lines.append(f"- {regime}: scale min/p05/median/p95/max = "+" / ".join(f"{scale[key]:.6g}" for key in ("min","p05","median","p95","max"))+f"; max budget error {error['max']:.9g}.")
    lines.append("")
    table("C2 backtracking",[("step.chosen_eta","Chosen eta",1),("step.backtracking_trials","Trials",1),
          ("step.step_rejected","No update fraction",1),("step.armijo_satisfied","Condition satisfied fraction",1),
          ("step.armijo_margin","RHS minus after-loss",1)],["C2"])
    lines += ["### C2 eta counts by seed/regime","","| Seed/regime | Eta: count |","| --- | --- |"]
    for name,counts in data["C2_eta_counts"].items():
        lines.append(f"| {name} | "+", ".join(f"{eta}: {count}" for eta,count in sorted(counts.items(),key=lambda x:float(x[0])))+" |")
    lines += ["","## Runtime — normal forward only","",
              "Physical A6000 GPU 1. Three warmups and three full 100-episode timed passes per seed/regime, "
              "GPU synchronization around each pass. Oracle scoring excluded. Other project ran on GPU 0; "
              "shared host activity and the sequential measurement order limit interpretation of small timing differences.","",
              "| Method | Regime | ms/episode mean ± seed SD | Multiplier vs C0 mean ± seed SD |","| --- | --- | --- | --- |"]
    for method,seeds in data["timings"].items():
        for regime in ("easy","hard"):
            times=[row[regime]["mean_ms_per_episode"] for row in seeds.values()]
            ratios=[row[regime]["multiplier_vs_C0"] for row in seeds.values()]
            lines.append(f"| {method} | {regime} | {statistics.mean(times):.4f} ± {statistics.stdev(times):.4f} | {statistics.mean(ratios):.4f} ± {statistics.stdev(ratios):.4f} |")
    lines += ["","## Per-seed paired outcomes","",
              "| Method | Regime | Seed | Task cosine | ΔNLL | ΔAccuracy pp | Post accuracy % | Post NLL | Post margin |",
              "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for method,regimes in data["per_seed"].items():
        for regime,seeds in regimes.items():
            for seed,metrics in seeds.items():
                fields=[("alignment.cosine",1),("after.nll_delta",1),("after.accuracy_delta",100),
                        ("after.accuracy",100),("after.nll",1),("after.margin",1)]
                lines.append(f"| {method} | {regime} | {seed} | "+" | ".join(f"{metrics[key]['mean']*scale:.6f}" for key,scale in fields)+" |")
    lines += ["","## Fixed interpretation rules","","```json",json.dumps(data["rules"],indent=2),"```","",
              "## Mechanism and verification","",
              "| Method | Seed | Easy/hard vocabulary state delta mean | Unrelated vocabulary state delta mean | Reset state max | Reset output max |",
              "| --- | --- | --- | --- | --- | --- |"]
    for method,seeds in data["mechanisms"].items():
        for seed,receipt in seeds.items():
            rows=receipt["episodes"]
            lines.append(f"| {method} | {seed} | {receipt['mean']['easy_hard_state_delta']:.6f} | {receipt['mean']['unrelated_state_delta']:.6f} | {max(r['reset_state_delta'] for r in rows):.6g} | {max(r['reset_output_delta'] for r in rows):.6g} |")
    lines += ["",f"Main records {verification['records']}; queries {verification['queries']}; mechanism episodes {verification['mechanism_records']}. "
              f"Normal output/state max error {verification['normal_output_max_error']}/{verification['normal_state_max_error']}; "
              f"nonfinite elements {verification['nonfinite_elements']}; all finite {verification['all_records_finite']}. "
              "Source hashes and original O0/C0 metric equality checks: verification.json.","",
              "## Interpretation and limits","",
              "C2 improves hard accuracy by 5.70833 percentage points and NLL by .07854 from the same W0. "
              "Hard NLL improves for all three seeds (-.08020/-.08403/-.07141); accuracy also improves in all three "
              "(+7.5/+5.875/+3.75pp). Its raw direction is exactly the O1 direction by construction, with a hard "
              "cosine advantage .26207 over O0; accepted step control changes magnitude, not the objective.", "",
              "C1 restores easy accuracy by 35pp relative to C0 and lowers NLL by 2.75515, but the full Rule 1 "
              "fails: hard NLL rises from 1.31014 to 1.33918 and accuracy falls from 41.875% to 39.33333%. "
              "Matching the O0 norm budget alone is insufficient; C1 hard mean scale is 1.33198.", "",
              "C2 selects much smaller steps for easy (mean .00777) than hard (.03971). All 600 steps are accepted "
              "within the fixed sequence and meet Armijo; none falls back to W0. This supports the specific "
              "direction/step-behavior hypothesis in this frozen setting. It does not establish that a future "
              "meta-trained controller or detector will improve, or that the controller is optimal.", "",
              "The aggregate easy gain is not universal: seed 27 C2 worsens from its own W0 by .13119 NLL "
              "and -8.25pp accuracy. Rule 2 is defined on aggregate means and passes unchanged; retain this "
              "failure and all paired records rather than claiming per-seed easy safety.", "",
              "Engineering status VERIFIED; Research Lead acceptance is pending. If the lead continues, "
              "recommend C2 under a separately assigned fixed-budget meta-training task. No T006, detector "
              "integration, new objective or extra tuning is authorized by this result alone.", "",
              "## Historical non-deployable reference","",
              "T003 exact-text foreground oracle, unchanged and not rerun: easy accuracy 85.16667%, NLL .36045; "
              "hard accuracy 48.33333%, NLL 1.18409. It uses labels/IDs and is not a deployable baseline.","",
              "## Artifacts","",
              "Full raw records and run logs: research_log/remote_runs/20260912-053826-tovd-t005-a6000/. "
              "frozen_step_screen.json contains aggregate/per-seed distributions, timings, eta counts, reset/vocabulary records and environment. "
              "Rules are evaluated without modifying their thresholds; research review is required before any subsequent task."]
    (TASK/"RESULTS.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps({key:value for key,value in verification.items() if key!="artifact_manifest"},indent=2))
    print(json.dumps(data["rules"],indent=2))


if __name__=="__main__":
    main()
