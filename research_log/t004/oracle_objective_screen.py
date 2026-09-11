"""Offline ORACLE screen of label-free objectives on fixed T002 P checkpoints."""

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import statistics

import torch
from torch.func import functional_call
from torch.nn import functional as F

from research_log.t003.oracle_diagnostic import (gradient_relation, oracle_preupdate,
                                                oracle_evaluate_update, paired_changes,
                                                oracle_token_masks)
from research_log.t003.oracle_diagnostic_run import collect_numeric, distribution, save_json
from tovd.models.vocabulary_objectives import OBJECTIVES, centered_text
from tovd.synthetic.benchmark import episode_seed, outer_metrics
from tovd.synthetic.models import EpisodicClassifier
from tovd.synthetic.semantic_episodes import SemanticWorld, WorldConfig


def oracle_screen_episode(model, episode):
    model.eval()
    context = oracle_preupdate(model, episode)
    # Replace only the analysis inner loss; oracle task gradient is unchanged.
    prediction = functional_call(model.memory.fast_model, context["params"], (context["keys"],))
    inner_loss = model.memory.inner_objective(prediction, context["keys"], episode.X,
                                             episode.T, context["target"])
    inner = torch.autograd.grad(inner_loss, tuple(context["params"].values()))
    before, before_output = oracle_evaluate_update(model, episode, context, inner, 0.0)
    after, output = oracle_evaluate_update(model, episode, context, inner, .05)
    with torch.no_grad():
        normal = model(episode.X.unsqueeze(0), episode.T.unsqueeze(0), episode.Q.unsqueeze(0))
        masks = oracle_token_masks(episode)
        text = model.memory.objective_text(episode.T)
        assignments = model.memory.assignments(context["keys"], episode.T)
        top = assignments.topk(2, dim=-1).values
        token_metrics = {"entropy": -(assignments * assignments.clamp_min(1e-12).log()).sum(-1),
                         "top1_probability": top[:, 0], "top1_top2_gap": top[:, 0] - top[:, 1]}
        groups = {name: {key: value[mask].tolist() for key, value in token_metrics.items()}
                  for name, mask in masks.items()}
        fg = masks["foreground"]
        correct_index = (episode.image_ids[fg, None] == episode.vocabulary_ids[None, :]).long().argmax(-1)
        target = assignments @ text
        sim = F.normalize(target[fg], dim=-1) @ F.normalize(text, dim=-1).T
        correct = sim.gather(-1, correct_index[:, None]).squeeze(-1)
        wrong = sim.clone()
        wrong.scatter_(-1, correct_index[:, None], -torch.inf)
        groups["foreground"].update({"assignment_correct": (assignments[fg].argmax(-1) == correct_index).float().tolist(),
                                    "target_correct_minus_wrong_cosine": (correct - wrong.max(-1).values).tolist()})
        relative_text = centered_text(episode.T)
        query_relative = F.normalize(output, dim=-1) @ F.normalize(relative_text, dim=-1).T
        relative_margin = outer_metrics(query_relative[None], query_relative[None], episode.labels[None])["margin"]
    return {"oracle_diagnostic": True,
            "alignment": gradient_relation(inner, context["g_task"]),
            "before": before, "after": paired_changes(after, before),
            "assignment_tokens": groups, "relative_query_margin_after": relative_margin,
            "inner_loss_before": inner_loss.item(),
            "inner_loss_after": normal.diagnostics["inner_loss_after"].item(),
            "representation_shift": (output - before_output).norm().item(),
            "normal_output_max_error": (output - normal.tokens[0]).abs().max().item(),
            "all_finite": bool(normal.diagnostics["all_finite"].all())}


def summarize(grouped):
    aggregate, per_seed = {}, {}
    for objective, regimes in grouped.items():
        aggregate[objective], per_seed[objective] = {}, {}
        for regime, seed_records in regimes.items():
            pooled = defaultdict(list)
            seed_series = {}
            for seed, records in seed_records.items():
                series = defaultdict(list)
                for row in records:
                    collect_numeric(row["diagnostics"], destination=series)
                seed_series[seed] = series
                for key, values in series.items():
                    pooled[key].extend(values)
            per_seed[objective][regime] = {str(seed): {key: distribution(values) for key, values in series.items()}
                                           for seed, series in seed_series.items()}
            aggregate[objective][regime] = {}
            for metric, values in pooled.items():
                means = [statistics.mean(series[metric]) for series in seed_series.values()]
                aggregate[objective][regime][metric] = {"mean": statistics.mean(means),
                    "std": statistics.stdev(means) if len(means) > 1 else 0.0,
                    "seed_means": means, "pooled": distribution(values)}
    return {"aggregate": aggregate, "per_seed": per_seed}


def select_candidates(aggregate):
    """Exactly the gate committed in PLAN.md at be0a11c, no result-driven edits."""
    decisions = {}
    reference = aggregate["O0"]
    for objective in ("O1", "O2", "O3"):
        candidate = aggregate[objective]
        hard_nll_gain = reference["hard"]["after.nll_delta"]["mean"] - candidate["hard"]["after.nll_delta"]["mean"]
        hard_cos_gain = candidate["hard"]["alignment.cosine"]["mean"] - reference["hard"]["alignment.cosine"]["mean"]
        easy_nll_harm = candidate["easy"]["after.nll"]["mean"] - reference["easy"]["after.nll"]["mean"]
        easy_accuracy_loss = 100 * (reference["easy"]["after.accuracy"]["mean"] - candidate["easy"]["after.accuracy"]["mean"])
        eligible = (hard_nll_gain >= .02 or hard_cos_gain >= .05) and easy_nll_harm <= .10 and easy_accuracy_loss <= 5
        decisions[objective] = {"hard_nll_gain_vs_O0": hard_nll_gain, "hard_cosine_gain_vs_O0": hard_cos_gain,
                               "easy_nll_harm_vs_O0": easy_nll_harm, "easy_accuracy_loss_pp_vs_O0": easy_accuracy_loss,
                               "eligible": eligible}
    eligible = [name for name in decisions if decisions[name]["eligible"]]
    ranked = sorted(eligible, key=lambda name: (aggregate[name]["hard"]["after.nll_delta"]["mean"],
                                               -aggregate[name]["hard"]["alignment.cosine"]["mean"]))
    return {"preregistration_commit": "be0a11c", "decisions": decisions,
            "selected": ranked[:2], "phase2_allowed": bool(ranked),
            "rule": "Hard NLL gain >=.02 OR cosine gain >=.05; easy NLL harm <=.10 AND accuracy loss <=5pp. Rank eligible by hard delta NLL then cosine."}


def run(source_root, output, device, revision, seeds=(7, 17, 27), episode_limit=None):
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    output.mkdir(parents=True, exist_ok=True)
    config = json.loads((source_root / "config.json").read_text(encoding="utf-8-sig"))
    world = SemanticWorld(WorldConfig(**config["world"]))
    count = config["eval_episodes"] if episode_limit is None else episode_limit
    grouped = {objective: {regime: {} for regime in ("easy", "hard")} for objective in OBJECTIVES}
    sources, original_checks = [], []
    for seed in seeds:
        path = source_root / f"seed{seed}_P" / "checkpoint.pt"
        checkpoint = torch.load(path, map_location=device, weights_only=True)
        sources.append({"seed": seed, "path": str(path.resolve()), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                        "training_revision": checkpoint["revision"]})
        original = json.loads((path.parent / "episodes.json").read_text())
        for objective in OBJECTIVES:
            model = EpisodicClassifier(objective, **checkpoint["config"]["model"]).to(device)
            model.load_state_dict(checkpoint["state_dict"])
            for regime in ("easy", "hard"):
                records = []
                for index in range(count):
                    ep_seed = episode_seed(seed, index, "test")
                    ep = world.episode("test", regime, ep_seed).to(device)
                    records.append({"seed": seed, "objective": objective, "regime": regime,
                                    "index": index, "episode_seed": ep_seed,
                                    "diagnostics": oracle_screen_episode(model, ep)})
                grouped[objective][regime][seed] = records
                save_json(output / f"seed{seed}_{objective}_{regime}.json", records)
                if objective == "O0":
                    old = [row for row in original if row["hardness"] == regime][:count]
                    errors = {metric: max(abs(row["diagnostics"]["after"][metric] - prior[metric])
                                          for row, prior in zip(records, old)) for metric in ("accuracy", "nll", "margin")}
                    original_checks.append({"seed": seed, "regime": regime, "errors": errors})
                print(f"SCREEN seed={seed} objective={objective} regime={regime} episodes={count}", flush=True)
    result = summarize(grouped)
    result["oracle_diagnostic"] = True
    result["original_O0_checks"] = original_checks
    result["environment"] = {"time_utc": datetime.now(timezone.utc).isoformat(), "revision": revision,
                             "python": platform.python_version(), "torch": torch.__version__, "cuda": torch.version.cuda,
                             "device": device, "dtype": "float32", "seeds": list(seeds), "episodes_per_regime": count,
                             "source_checkpoints": sources, "source_config": config, "outer_retraining": False}
    result["gate"] = select_candidates(result["aggregate"])
    save_json(output / "frozen_screen.json", result)
    save_json(output / "selection.json", result["gate"])
    lines = ["# T004 Phase-1 frozen-checkpoint ORACLE screen", "",
             "Task gradients and assignment correctness use offline labels only. Mean ± sample SD across seed means.", "",
             "| Objective | Regime | Task cosine | ΔNLL | Accuracy % | NLL | Margin | Gradient norm | Update norm |",
             "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for objective, regimes in result["aggregate"].items():
        for regime, metrics in regimes.items():
            fields = [("alignment.cosine", 1), ("after.nll_delta", 1), ("after.accuracy", 100),
                      ("after.nll", 1), ("after.margin", 1), ("alignment.gradient_norm", 1), ("after.update_norm", 1)]
            cells = [f"{metrics[key]['mean']*scale:.5f} ± {metrics[key]['std']*scale:.5f}" for key, scale in fields]
            lines.append(f"| {objective} | {regime} | " + " | ".join(cells) + " |")
    lines += ["", "Selected for Phase 2: " + (", ".join(result["gate"]["selected"]) or "NONE; STOP"),
              "", "See selection.json for the preregistered gate decisions and frozen_screen.json for assignment/relative-margin diagnostics."]
    (output / "screen.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(description="ORACLE diagnostic screen; no outer training")
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--revision", required=True)
    args = parser.parse_args()
    run(args.source_root, args.output, args.device, args.revision)


if __name__ == "__main__":
    main()
