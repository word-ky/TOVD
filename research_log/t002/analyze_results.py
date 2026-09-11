"""Summarize fixed T002 receipts; does not train, select or modify results."""

import argparse
import json
from pathlib import Path
import statistics


def stats(values):
    return {"mean": statistics.mean(values), "std": statistics.stdev(values), "values": values}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = json.loads((args.run_dir / "results.json").read_text())
    table = {(row["seed"], row["method"]): row for row in rows}
    seeds = sorted({row["seed"] for row in rows})
    methods = list(dict.fromkeys(row["method"] for row in rows))
    comparisons = {}
    for control in ("B0", "B1", "B2", "P_fixed"):
        regimes = {}
        for regime in ("easy", "hard"):
            values = [100 * (table[seed, "P"]["metrics"][regime]["accuracy"] -
                             table[seed, control]["metrics"][regime]["accuracy"]) for seed in seeds]
            regimes[regime] = stats(values)
        regimes["hard_minus_easy_gain"] = stats([h - e for h, e in
                                                 zip(regimes["hard"]["values"], regimes["easy"]["values"])])
        comparisons["P_minus_" + control] = regimes
    compute = {}
    mechanisms = {}
    for method in methods:
        selected = [table[seed, method] for seed in seeds]
        compute[method] = {
            "total_parameters": selected[0]["total_parameters"],
            "optimizer_parameters": selected[0]["outer_optimized_parameters"],
            "latency_ms": stats([row["eval_ms_per_episode"] for row in selected]),
            "train_seconds": stats([row["train_seconds"] for row in selected]),
            "W0_outer_drift": [row["W0_outer_drift"] for row in selected],
        }
        mechanisms[method] = {name: stats([row["mechanism"]["mean"][name] for row in selected])
                              for name in selected[0]["mechanism"]["mean"]}
    # Independent evaluator receipt must reproduce the saved metrics exactly.
    reeval = json.loads((args.run_dir / "seed7_P" / "reevaluation.json").read_text())
    reeval_matches = reeval["metrics"] == table[7, "P"]["metrics"]
    analysis = {"seeds": seeds, "paired_accuracy_deltas_pp": comparisons, "compute": compute,
                "mechanisms": mechanisms, "independent_checkpoint_reevaluation_equal": reeval_matches,
                "all_finite": all(row["metrics"][regime].get("all_finite", 1) == 1
                                  for row in rows for regime in ("easy", "hard")),
                "source": str(args.run_dir),
                "limitation": "Three initialization/episode seeds in one fixed world; synthetic classes, not OVD."}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "analysis.json").write_text(json.dumps(analysis, indent=2) + "\n")
    lines = ["# T002 paired comparison analysis", "", "P minus control, percentage points. Mean ± sample SD across paired seeds.", "",
             "| Control | Easy Δ | Hard Δ | Hard-minus-easy Δ |", "| --- | --- | --- | --- |"]
    for name, regimes in comparisons.items():
        cells = [f"{regimes[key]['mean']:+.3f} ± {regimes[key]['std']:.3f}"
                 for key in ("easy", "hard", "hard_minus_easy_gain")]
        lines.append(f"| {name} | " + " | ".join(cells) + " |")
    lines += ["", "| Method | Parameters | Optimizer parameters | Eval ms/episode | Training seconds |",
              "| --- | --- | --- | --- | --- |"]
    for method, record in compute.items():
        lines.append(f"| {method} | {record['total_parameters']} | {record['optimizer_parameters']} | "
                     f"{record['latency_ms']['mean']:.3f} ± {record['latency_ms']['std']:.3f} | "
                     f"{record['train_seconds']['mean']:.2f} ± {record['train_seconds']['std']:.2f} |")
    lines += ["", "B0 includes an allocated but unused key projection (D²=256 parameters); its effective learned path has 256 fewer parameters.",
              "B1/P/B2 have identical parameter tensors and both X/T information where applicable; B2 adaptation target excludes T.",
              "Timing includes prototype diagnostic overhead, batch size 1, 3 warmups/10 forwards.",
              f"Independent P/seed7 checkpoint reevaluation exactly matches: {reeval_matches}.",
              "See analysis.json for per-seed deltas, reset/permutation/negative-control diagnostics and fixed-W0 drift."]
    (args.output / "analysis.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"paired_deltas": comparisons, "reevaluation_equal": reeval_matches}, indent=2))


if __name__ == "__main__":
    main()
