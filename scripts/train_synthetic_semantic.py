"""T002 fixed protocol training plus held-out evaluation and receipts."""

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import platform
import subprocess

import torch

from tovd.synthetic.benchmark import (aggregate_results, evaluate_model, measure_latency,
                                      mechanism_analysis, train_model)
from tovd.synthetic.semantic_episodes import SemanticWorld, WorldConfig


def save_json(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def run(config, output, device, revision):
    output.mkdir(parents=True, exist_ok=True)
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    world = SemanticWorld(WorldConfig(**config["world"]))
    save_json(output / "config.json", config)
    save_json(output / "environment.json", {
        "time_utc": datetime.now(timezone.utc).isoformat(), "revision": revision,
        "python": platform.python_version(), "torch": torch.__version__, "cuda": torch.version.cuda,
        "device": device, "dtype": "float32", "gpu": torch.cuda.get_device_name() if device.startswith("cuda") else None,
        "train_classes": world.train_ids.tolist(), "test_classes": world.test_ids.tolist(),
        "train_episode_seed": "10000000 + seed*10000 + index",
        "test_episode_seed": "20000000 + seed*10000 + index",
        "mechanism_episode_seed": "30000000 + seed*10000 + index",
        "selection": "Final fixed-step checkpoint; no held-out selection or tuning.",
    })
    results = []
    for seed in config["seeds"]:
        for method in config["methods"]:
            directory = output / f"seed{seed}_{method}"
            directory.mkdir(exist_ok=True)
            model, checkpoint = train_model(world, config, seed, method, device)
            checkpoint["revision"] = revision
            torch.save(checkpoint, directory / "checkpoint.pt")
            save_json(directory / "training.json", {key: checkpoint[key] for key in
                      ("train_seconds", "W0_outer_drift", "training_curve")})
            metrics, records = evaluate_model(model, world, config, seed, device)
            mechanism = mechanism_analysis(model, world, config, seed, device)
            row = {"seed": seed, "method": method, "metrics": metrics,
                   "total_parameters": sum(p.numel() for p in model.parameters()),
                   "outer_optimized_parameters": sum(p.numel() for p in model.outer_parameters()),
                   "eval_ms_per_episode": measure_latency(model, world, device),
                   "train_seconds": checkpoint["train_seconds"],
                   "W0_outer_drift": checkpoint["W0_outer_drift"], "mechanism": mechanism}
            save_json(directory / "metrics.json", row)
            save_json(directory / "episodes.json", records)
            results.append(row)
            # Save completed method/seed results immediately for recovery.
            save_json(output / "results.json", results)
            print(f"RESULT seed={seed} method={method} easy={metrics['easy']['accuracy']:.4f} hard={metrics['hard']['accuracy']:.4f}", flush=True)
    aggregate = aggregate_results(results)
    save_json(output / "aggregate.json", aggregate)
    with (output / "table.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["method", "hardness", "accuracy_mean", "accuracy_std", "nll_mean", "nll_std", "margin_mean", "margin_std"])
        for method, regimes in aggregate.items():
            for hardness, values in regimes.items():
                writer.writerow([method, hardness, *[values[key][stat] for key in ("accuracy", "nll", "margin") for stat in ("mean", "std")]])
    lines = ["# T002 held-out synthetic results", "", "Mean ± sample SD across seeds; accuracy in percent.", "",
             "| Method | Regime | Accuracy (%) | NLL | Cosine margin |", "| --- | --- | --- | --- | --- |"]
    for method, regimes in aggregate.items():
        for hardness, values in regimes.items():
            cells = [f"{values[key]['mean'] * scale:.4f} ± {values[key]['std'] * scale:.4f}"
                     for key, scale in (("accuracy", 100), ("nll", 1), ("margin", 1))]
            lines.append(f"| {method} | {hardness} | " + " | ".join(cells) + " |")
    lines += ["", "See results.json for per-seed diagnostics, parameter counts, timing and mechanism analyses.",
              "No detection accuracy claim; fixed protocol, no test-based checkpoint selection."]
    (output / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("research_log/t002/config.json"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--revision")
    args = parser.parse_args()
    revision = args.revision or subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    run(json.loads(args.config.read_text(encoding="utf-8-sig")), args.output, args.device, revision)


if __name__ == "__main__":
    main()
