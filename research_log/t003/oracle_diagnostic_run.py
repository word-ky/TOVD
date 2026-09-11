"""ORACLE DIAGNOSTIC runner for frozen T002 checkpoints; never trains."""

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import csv
import hashlib
import json
from pathlib import Path
import platform
import statistics

import torch

from research_log.t003.oracle_diagnostic import ETAS, oracle_diagnose_episode
from tovd.synthetic.benchmark import episode_seed
from tovd.synthetic.models import EpisodicClassifier
from tovd.synthetic.semantic_episodes import SemanticWorld, WorldConfig


def save_json(path, data):
    path.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def collect_numeric(data, prefix="", destination=None):
    """Keep scalar episode values and raw token/query distributions separately."""
    if destination is None:
        destination = defaultdict(list)
    if isinstance(data, dict):
        for key, value in data.items():
            if key != "oracle_diagnostic":
                collect_numeric(value, prefix + "." + key if prefix else key, destination)
    elif isinstance(data, list):
        destination[prefix].extend(data)
    else:
        destination[prefix].append(data)
    return destination


def distribution(values):
    tensor = torch.tensor(values, dtype=torch.float64)
    quantiles = torch.quantile(tensor, torch.tensor([.05, .25, .5, .75, .95], dtype=torch.float64))
    return {"count": len(values), "mean": statistics.mean(values),
            "std": statistics.stdev(values) if len(values) > 1 else 0.0,
            "min": min(values), "max": max(values),
            **{name: value.item() for name, value in zip(("p05", "p25", "median", "p75", "p95"), quantiles)}}


def aggregate_records(grouped):
    per_seed, aggregate = {}, {}
    for method in ("P", "B2"):
        per_seed[method], aggregate[method] = {}, {}
        for regime in ("easy", "hard"):
            seed_series = {}
            per_seed[method][regime] = {}
            pooled = defaultdict(list)
            for seed, records in grouped[method][regime].items():
                series = defaultdict(list)
                for record in records:
                    collect_numeric(record["diagnostics"], destination=series)
                seed_series[seed] = series
                per_seed[method][regime][str(seed)] = {key: distribution(values) for key, values in series.items()}
                for key, values in series.items():
                    pooled[key].extend(values)
            aggregate[method][regime] = {}
            for metric, values in pooled.items():
                seed_means = [statistics.mean(series[metric]) for series in seed_series.values()]
                aggregate[method][regime][metric] = {
                    "mean": statistics.mean(seed_means),
                    "std": statistics.stdev(seed_means) if len(seed_means) > 1 else 0.0,
                    "seed_means": seed_means, "pooled": distribution(values)}
    return {"oracle_diagnostic": True, "per_seed": per_seed, "aggregate": aggregate}


def write_tables(output, result):
    aggregate = result["aggregate"]
    def value(method, regime, key, scale=1):
        entry = aggregate[method][regime][key]
        return f"{entry['mean']*scale:.5f} ± {entry['std']*scale:.5f}"
    lines = ["# T003 oracle diagnostic tables", "", "All label/ID-based results are offline oracle diagnostics, not deployable adaptation.",
             "Mean ± sample SD over seed means; complete episode/token/query distributions are in alignment.json.", "",
             "## D1 — W0 task-gradient alignment", "",
             "| Method | Regime | Cosine | Task dot | Predicted ΔNLL | Actual ΔNLL | Positive alignment % | Episode improves % | Query improves % |",
             "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for method in ("P", "B2"):
        for regime in ("easy", "hard"):
            entries = [value(method, regime, "alignment." + key, scale) for key, scale in
                       (("cosine", 1), ("dot", 1), ("predicted_task_nll_delta", 1),
                        ("actual_task_nll_delta", 1), ("positive_alignment", 100),
                        ("episode_nll_improves", 100), ("query_nll_improves_fraction", 100))]
            lines.append(f"| {method} | {regime} | " + " | ".join(entries) + " |")
    lines += ["", "## D2 — Frozen-checkpoint eta controls", "",
              "| Method | Regime | Eta | Accuracy % | NLL | Margin | ΔNLL vs own W0 | Episode improves % |",
              "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for method in ("P", "B2"):
        for regime in ("easy", "hard"):
            for eta in ETAS:
                entries = [value(method, regime, f"eta.{eta}." + key, scale) for key, scale in
                           (("accuracy", 100), ("nll", 1), ("margin", 1), ("nll_delta", 1), ("episode_nll_improves", 100))]
                lines.append(f"| {method} | {regime} | {eta} | " + " | ".join(entries) + " |")
    lines += ["", "## D3 — P oracle token decomposition and updates", "",
              "| Regime | Group | Gradient norm | Task cosine | Task dot |",
              "| --- | --- | --- | --- | --- |"]
    for regime in ("easy", "hard"):
        for group in ("foreground", "distractor", "background", "foreground_exact_text"):
            entries = [value("P", regime, f"decomposition.groups.{group}." + key)
                       for key in ("gradient_norm", "cosine", "dot")]
            lines.append(f"| {regime} | {group} | " + " | ".join(entries) + " |")
    lines += ["", "| Regime | Oracle update | Accuracy % | NLL | ΔNLL vs own W0 | Episode improves % | Update norm |",
              "| --- | --- | --- | --- | --- | --- | --- |"]
    for regime in ("easy", "hard"):
        for variant in ("all_soft", "foreground_soft", "foreground_exact_text"):
            entries = [value("P", regime, f"oracle_variants.{variant}." + key, scale) for key, scale in
                       (("accuracy", 100), ("nll", 1), ("nll_delta", 1), ("episode_nll_improves", 100), ("update_norm", 1))]
            lines.append(f"| {regime} | {variant} | " + " | ".join(entries) + " |")
    lines += ["", "## D4 — P pre-update target ambiguity", "",
              "| Regime | Tokens | Entropy (nats) | Top probability | Top1-top2 gap | Target norm |",
              "| --- | --- | --- | --- | --- | --- |"]
    for regime in ("easy", "hard"):
        for group in ("foreground", "distractor", "background"):
            entries = [value("P", regime, f"ambiguity_tokens.{group}." + key)
                       for key in ("entropy", "top1_probability", "top1_top2_gap", "target_norm")]
            lines.append(f"| {regime} | {group} | " + " | ".join(entries) + " |")
    lines += ["", "| Regime | Foreground assignment correct % | Target/correct cosine | Target/strongest-wrong cosine | Target cosine margin |",
              "| --- | --- | --- | --- | --- |"]
    for regime in ("easy", "hard"):
        entries = [value("P", regime, "ambiguity_tokens.foreground." + key, scale) for key, scale in
                   (("assignment_correct", 100), ("target_correct_cosine", 1),
                    ("target_strongest_wrong_cosine", 1), ("target_cosine_margin", 1))]
        lines.append(f"| {regime} | " + " | ".join(entries) + " |")
    lines += ["", "All etas use the same checkpoint meta-trained at eta=.05; this is not method selection.",
              "Subset gradients use subset means; weighted contributions use n_subset/N and reconstruct the original gradient."]
    (output / "tables.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    with (output / "table.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["method", "regime", "metric", "mean_seed_means", "std_seed_means", "pooled_count", "p05", "median", "p95"])
        for method, regimes in aggregate.items():
            for regime, metrics in regimes.items():
                for metric, entry in metrics.items():
                    writer.writerow([method, regime, metric, entry["mean"], entry["std"],
                                     *[entry["pooled"][key] for key in ("count", "p05", "median", "p95")]])


def run(source_root, output, device, revision, seeds=(7, 17, 27), episode_limit=None):
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    output.mkdir(parents=True, exist_ok=True)
    config = json.loads((source_root / "config.json").read_text(encoding="utf-8-sig"))
    count = config["eval_episodes"] if episode_limit is None else episode_limit
    world = SemanticWorld(WorldConfig(**config["world"]))
    grouped = {method: {regime: {} for regime in ("easy", "hard")} for method in ("P", "B2")}
    sources = []
    normal_checks = []
    for seed in seeds:
        for method in ("P", "B2"):
            path = source_root / f"seed{seed}_{method}" / "checkpoint.pt"
            checkpoint = torch.load(path, map_location=device, weights_only=True)
            sources.append({"path": str(path.resolve()), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                            "seed": seed, "method": method, "training_revision": checkpoint["revision"]})
            model = EpisodicClassifier(method, **checkpoint["config"]["model"]).to(device)
            model.load_state_dict(checkpoint["state_dict"])
            original = json.loads((path.parent / "episodes.json").read_text())
            for regime in ("easy", "hard"):
                records = []
                for index in range(count):
                    ep_seed = episode_seed(seed, index, "test")
                    ep = world.episode("test", regime, ep_seed).to(device)
                    diagnostic = oracle_diagnose_episode(model, ep)
                    records.append({"seed": seed, "method": method, "regime": regime,
                                    "index": index, "episode_seed": ep_seed, "diagnostics": diagnostic})
                grouped[method][regime][seed] = records
                save_json(output / f"seed{seed}_{method}_{regime}.json", records)
                # Compare unchanged eta=.05 scores to original T002 receipts.
                old = [row for row in original if row["hardness"] == regime][:count]
                errors = {metric: max(abs(record["diagnostics"]["eta"]["0.05"][metric] - reference[metric])
                                      for record, reference in zip(records, old))
                          for metric in ("accuracy", "nll", "margin")}
                normal_checks.append({"seed": seed, "method": method, "regime": regime,
                                      "original_T002_metric_max_errors": errors})
                print(f"COMPLETE seed={seed} method={method} regime={regime} episodes={count} original_errors={errors}", flush=True)
    result = aggregate_records(grouped)
    result["normal_T002_checks"] = normal_checks
    result["environment"] = {"time_utc": datetime.now(timezone.utc).isoformat(), "diagnostic_revision": revision,
                             "python": platform.python_version(), "torch": torch.__version__,
                             "cuda": torch.version.cuda, "device": device, "dtype": "float32",
                             "gpu": torch.cuda.get_device_name() if device.startswith("cuda") else None,
                             "seeds": list(seeds), "episodes_per_regime": count, "etas": list(ETAS),
                             "source_checkpoints": sources, "source_config": config,
                             "oracle_diagnostic": True, "outer_retraining": False}
    save_json(output / "alignment.json", result)
    write_tables(output, result)
    return result


def main():
    parser = argparse.ArgumentParser(description="Offline ORACLE DIAGNOSTICS only")
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--revision", required=True)
    args = parser.parse_args()
    run(args.source_root, args.output, args.device, args.revision)


if __name__ == "__main__":
    main()
