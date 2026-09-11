"""Format the completed, fixed T004 screen receipts without rerunning models."""

import hashlib
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[2]
TASK = ROOT / "research_log/t004"
RUN = ROOT / "research_log/remote_runs/20260912-043224-tovd-t004-screen-a6000"
SOURCE = RUN / "artifacts/t004_phase1"
T002 = ROOT / "research_log/remote_runs/20260912-023122-tovd-t002-a6000/artifacts/t002"


def main():
    data = json.loads((SOURCE / "frozen_screen.json").read_text())
    for filename in ("frozen_screen.json", "selection.json"):
        shutil.copyfile(SOURCE / filename, TASK / filename)
    records = [row for file in sorted(SOURCE.glob("seed*.json")) for row in json.loads(file.read_text())]
    hashes = []
    for source in data["environment"]["source_checkpoints"]:
        path = T002 / f"seed{source['seed']}_P/checkpoint.pt"
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        hashes.append({"seed": source["seed"], "local_path": str(path.relative_to(ROOT)),
                       "expected_sha256": source["sha256"], "actual_sha256": actual,
                       "matches": actual == source["sha256"]})
    verification = {"screen_records": len(records), "source_hashes": hashes,
                    "original_O0_checks": data["original_O0_checks"],
                    "max_normal_output_error": max(row["diagnostics"]["normal_output_max_error"] for row in records),
                    "all_records_finite": all(row["diagnostics"]["all_finite"] for row in records),
                    "query_records": sum(len(row["diagnostics"]["after"]["query_nll_delta"]) for row in records),
                    "artifact_files": [{"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size,
                                        "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                                       for path in sorted(RUN.rglob("*")) if path.is_file()]}
    (TASK / "verification.json").write_text(json.dumps(verification, indent=2) + "\n")
    lines = ["# T004 results — Phase 1 complete; Phase 2 not authorized by fixed gate", "",
             "O1/O3 improve gradient direction, but fail the fixed eta=.05 easy-regression limits. "
             "O2 worsens hard alignment and actual NLL. No candidate selected; no new outer training.", "",
             "These checkpoints were meta-trained for O0. This screen does not establish that "
             "O1/O3 cannot be meta-trained successfully. It does establish that none meets the "
             "preregistered eligibility rule at this fixed W0 and step size.", "",
             "Run: 20260912-043224-tovd-t004-screen-a6000. Tested code: "
             "9afe8df54c22d0a20b284d6b4b20aaab5b36ea9a. Preregistration: be0a11c.", "",
             "Three seeds (7/17/27), 100 easy + 100 hard episodes each, four objectives: "
             "2,400 paired diagnoses / 19,200 query outcomes. All three source hashes match. "
             "All O0 NLL/accuracy/margin errors versus T002 and all diagnostic/normal output errors are zero. "
             "All records finite. Mean ± sample SD across seed means; accuracy in percent.", ""]

    def aggregate_table(title, fields):
        lines.extend(["## " + title, "", "| Objective | Regime | " + " | ".join(label for _, label, _ in fields) + " |",
                      "| --- | --- | " + " | ".join("---" for _ in fields) + " |"])
        for objective, regimes in data["aggregate"].items():
            for regime, metrics in regimes.items():
                cells = [f"{metrics[key]['mean']*scale:.5f} ± {metrics[key]['std']*scale:.5f}" for key, _, scale in fields]
                lines.append(f"| {objective} | {regime} | " + " | ".join(cells) + " |")
        lines.append("")

    aggregate_table("Actual pre/post task performance", [
        ("before.accuracy", "W0 acc %", 100), ("after.accuracy", "W* acc %", 100),
        ("before.nll", "W0 NLL", 1), ("after.nll", "W* NLL", 1), ("after.nll_delta", "ΔNLL", 1),
        ("before.margin", "W0 margin", 1), ("after.margin", "W* margin", 1)])
    aggregate_table("Gradient direction, update size and actual improvement fractions", [
        ("alignment.cosine", "Task cosine", 1), ("alignment.dot", "Task dot", 1),
        ("alignment.gradient_norm", "Gradient norm", 1), ("after.update_norm", "Update norm", 1),
        ("after.episode_nll_improves", "Episodes improve %", 100),
        ("after.query_nll_improves_fraction", "Queries improve %", 100)])
    aggregate_table("Inner loss and query representation", [
        ("inner_loss_before", "Inner before", 1), ("inner_loss_after", "Inner after", 1),
        ("representation_shift", "Representation shift", 1),
        ("relative_query_margin_after", "Centered query margin after", 1)])
    aggregate_table("Foreground assignment ambiguity (offline oracle scoring)", [
        ("assignment_tokens.foreground.assignment_correct", "Assignment correct %", 100),
        ("assignment_tokens.foreground.entropy", "Entropy", 1),
        ("assignment_tokens.foreground.top1_top2_gap", "Top1-top2 gap", 1),
        ("assignment_tokens.foreground.target_correct_minus_wrong_cosine", "Target correct-wrong cosine", 1)])
    lines += ["O0/O1 use original text geometry; O2/O3 use centered normalized text. "
              "The last column scores A*T (O0/O1) or A_rel*T_rel (O2/O3). "
              "For distribution objectives this vector is only an inspection statistic, never the loss target. "
              "Absolute margins across original/centered coordinate systems are not directly comparable. "
              "Distractor/background entropy and gaps, token distributions and seed SDs are in frozen_screen.json.", "",
              "## Per-seed paired task outcomes", "",
              "| Objective | Regime | Seed | Cosine | ΔNLL | ΔAccuracy pp | Post accuracy % | Post NLL | Post margin |",
              "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for objective, regimes in data["per_seed"].items():
        for regime, seeds in regimes.items():
            for seed, metrics in seeds.items():
                fields = [("alignment.cosine", 1), ("after.nll_delta", 1), ("after.accuracy_delta", 100),
                          ("after.accuracy", 100), ("after.nll", 1), ("after.margin", 1)]
                lines.append(f"| {objective} | {regime} | {seed} | " + " | ".join(f"{metrics[k]['mean']*s:.5f}" for k,s in fields) + " |")
    lines += ["", "## Preregistered selection", "",
              "| Candidate | Hard NLL gain vs O0 | Hard cosine gain | Easy NLL harm | Easy accuracy loss pp | Eligible |",
              "| --- | --- | --- | --- | --- | --- |"]
    for objective, row in data["gate"]["decisions"].items():
        fields = ["hard_nll_gain_vs_O0", "hard_cosine_gain_vs_O0", "easy_nll_harm_vs_O0", "easy_accuracy_loss_pp_vs_O0"]
        lines.append(f"| {objective} | " + " | ".join(f"{row[k]:.5f}" for k in fields) + f" | {row['eligible']} |")
    lines += ["", "Rule unchanged from be0a11c: hard ΔNLL gain ≥.02 OR cosine gain ≥.05; "
              "easy NLL harm ≤.10 AND accuracy loss ≤5pp. Selected: none. Phase 2: not run.", "",
              "## Historical reference (non-deployable)", "",
              "T003 foreground exact-text oracle at the same P W0: easy accuracy 85.16667%, "
              "NLL .36045, task cosine .31727; hard accuracy 48.33333%, NLL 1.18409, cosine .12128. "
              "It uses ground-truth source IDs and exact text targets; retained only as a reference, not rerun. "
              "Source: research_log/remote_runs/20260912-030923-tovd-t003-a6000/artifacts/t003/alignment.json.", "",
              "## Interpretation and recommendation", "",
              "O1/O3 hard cosine increases are real direction changes at the same W0, not merely larger "
              "gradient norms. However local alignment does not ensure a finite eta=.05 step improves the "
              "task. O1 easy inner CE increases 2.25795→4.51553, O3 easy 2.50297→5.51338, and O3 hard "
              "3.30774→5.38075. Together with large updates these observations are consistent with "
              "step-size/curvature mismatch; no eta sweep was performed to establish its cause.", "",
              "Centering sharpens hard assignments (entropy 1.36711→1.20460, gap .04567→.18753) "
              "without improving correctness (29.27083%→28.93750%). More confident assignments are not "
              "evidence of better semantics. O2 hard task cosine becomes more negative.", "",
              "Recommend stopping this fixed-objective/fixed-step branch before detector integration. "
              "Research Lead may explicitly authorize a reformulation addressing objective scale/local "
              "step behavior and teacher correctness; these are hypotheses, not implemented fixes. "
              "Do not claim all objectives are misaligned, that meta-training has failed, or that the "
              "broader fast-weight mechanism is disproved. No Phase-2 success claim is available.", "",
              "## Artifacts", "", "- frozen_screen.json: aggregate/per-seed metrics and experiment environment.",
              "- selection.json: exact fixed gate decisions.", "- verification.json: original pairing, hashes and full receipt manifest.",
              "- research_log/remote_runs/20260912-043224-tovd-t004-screen-a6000/: complete raw records, metadata and logs."]
    (TASK / "RESULTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({k:v for k,v in verification.items() if k != "artifact_files"}, indent=2))


if __name__ == "__main__":
    main()
