"""One shared training/evaluation protocol for all T002 methods."""

from dataclasses import asdict
import statistics
import time

import torch
from torch.nn import functional as F

from .models import EpisodicClassifier
from .semantic_episodes import stack_episodes


def outer_metrics(logits, similarities, labels):
    correct = similarities.gather(-1, labels.unsqueeze(-1)).squeeze(-1)
    distractors = similarities.clone()
    distractors.scatter_(-1, labels.unsqueeze(-1), -torch.inf)
    return {
        "accuracy": (logits.argmax(-1) == labels).float().mean().item(),
        "nll": F.cross_entropy(logits.flatten(0, 1), labels.flatten()).item(),
        "margin": (correct - distractors.max(-1).values).mean().item(),
    }


def episode_seed(seed, index, phase):
    return {"train": 10000000, "test": 20000000, "mechanism": 30000000}[phase] + seed * 10000 + index


def training_episode(world, seed, index):
    return world.episode("train", "easy" if index % 2 == 0 else "hard", episode_seed(seed, index, "train"))


def train_model(world, config, seed, method, device):
    torch.manual_seed(seed)
    model = EpisodicClassifier(method, **config["model"]).to(device)
    initial_fast = {name: p.detach().cpu().clone() for name, p in model.memory.fast_model.named_parameters()}
    initial_state = {name:p.detach().cpu().clone() for name,p in model.named_parameters()} if method == "P_C2_meta" else None
    optimizer = torch.optim.Adam(model.outer_parameters(), lr=config["outer_lr"])
    model.train()
    curve = []
    start = time.perf_counter()
    for step in range(config["train_steps"]):
        episodes = [training_episode(world, seed, step * config["batch_size"] + j)
                    for j in range(config["batch_size"])]
        X, T, Q, labels = stack_episodes(episodes, device)
        model.zero_grad(set_to_none=True)
        result = model(X, T, Q)
        logits = model.logits(result.tokens, T)
        loss = F.cross_entropy(logits.flatten(0, 1), labels.flatten())
        loss.backward()
        optimizer.step()
        value = loss.detach().item()
        # Preserve every training loss, including any failed/non-finite value.
        row = {"step": step + 1, "loss": value}
        if method == "P_C2_meta":
            diag = result.diagnostics
            row.update({"accuracy":(logits.argmax(-1)==labels).float().mean().item(),
                        "inner_loss_before":diag["inner_loss_before"].mean().item(),
                        "inner_loss_after":diag["inner_loss_after"].mean().item(),
                        "inner_gradient_norm":diag["inner_gradient_norm"].mean().item(),
                        "update_norm":diag["fast_update_norm"].mean().item(),
                        "selected_etas":diag["chosen_eta"].tolist(),
                        "backtracking_trials":diag["backtracking_trials"].tolist(),
                        "eta_zero_fraction":(diag["chosen_eta"]==0).float().mean().item(),
                        "armijo_violations":int((diag["step_accepted"] & (diag["inner_loss_after"]>diag["armijo_rhs"])).sum().item()),
                        "finite":bool(diag["all_finite"].all()) and all(torch.isfinite(p).all().item() and
                                       (p.grad is None or torch.isfinite(p.grad).all().item()) for p in model.parameters())})
        curve.append(row)
        if step == 0 or (step + 1) % 100 == 0:
            print(f"seed={seed} method={method} step={step+1} loss={value:.6f}", flush=True)
    elapsed = time.perf_counter() - start
    drift = sum((p.detach().cpu() - initial_fast[name]).square().sum().item()
                for name, p in model.memory.fast_model.named_parameters()) ** 0.5
    checkpoint = {"state_dict": model.state_dict(), "optimizer": optimizer.state_dict(),
                  "config": config, "world": asdict(world.config), "seed": seed, "method": method,
                  "train_seconds": elapsed, "initial_fast_state": initial_fast,
                  "W0_outer_drift": drift, "training_curve": curve}
    if initial_state is not None:
        checkpoint["initial_state_dict"] = initial_state
    return model, checkpoint


def mean_records(records):
    return {name: statistics.mean(row[name] for row in records) for name in records[0]}


def evaluate_model(model, world, config, seed, device):
    model.eval()
    summary, episode_records = {}, []
    with torch.no_grad():
        for hardness in ("easy", "hard"):
            records = []
            for index in range(config["eval_episodes"]):
                ep = world.episode("test", hardness, episode_seed(seed, index, "test"))
                X, T, Q, labels = stack_episodes([ep], device)
                result = model(X, T, Q)  # No labels enter prediction/adaptation.
                # Labels first enter the evaluator after prediction.
                row = outer_metrics(model.logits(result.tokens, T), model.similarities(result.tokens, T), labels)
                static = model.memory(X, T, Q, enable_ttt=False).tokens
                row["representation_shift"] = (result.tokens - static).norm().item()
                row.update({name: value.float().mean().item() for name, value in result.diagnostics.items()})
                records.append(row)
                episode_records.append({"index": index, "hardness": hardness,
                                        "episode_seed": episode_seed(seed, index, "test"),
                                        "vocabulary_ids": ep.vocabulary_ids.tolist(),
                                        "query_ids": ep.query_ids.tolist(), **row})
            summary[hardness] = mean_records(records)
    return summary, episode_records


def state_distance(a, b):
    return sum((a.fast_state[name] - b.fast_state[name]).square().sum().item()
               for name in a.fast_state) ** 0.5


def mechanism_analysis(model, world, config, seed, device):
    model.eval()
    records = []
    with torch.no_grad():
        for index in range(config["mechanism_episodes"]):
            easy, hard, unrelated, unrelated_ids = world.paired_scene(episode_seed(seed, index, "mechanism"))
            X, Te, Q, _ = stack_episodes([easy], device)
            Th = hard.T.unsqueeze(0).to(device)
            Tu = unrelated.unsqueeze(0).to(device)
            a, b, negative = model(X, Te, Q), model(X, Th, Q), model(X, Tu, Q)
            repeat = model(X, Te, Q)
            permutation = torch.tensor([2, 0, 3, 1], device=device)
            permuted = model(X, Te[:, permutation], Q)
            prob = model.logits(negative.tokens, Tu).softmax(-1)
            row = {
                "easy_hard_state_delta": state_distance(a, b),
                "easy_hard_output_delta": (a.tokens - b.tokens).norm().item(),
                "unrelated_state_delta": state_distance(a, negative),
                "unrelated_output_delta": (a.tokens - negative.tokens).norm().item(),
                "unrelated_max_confidence": prob.max(-1).values.mean().item(),
                "unrelated_entropy": -(prob * prob.clamp_min(1e-12).log()).sum(-1).mean().item(),
                "reset_state_delta": state_distance(a, repeat),
                "reset_output_delta": (a.tokens - repeat.tokens).norm().item(),
                "permutation_output_max_error": (a.tokens - permuted.tokens).abs().max().item(),
            }
            records.append(row)
    return {"mean": mean_records(records), "episodes": records,
            "negative_control": "Vocabulary excludes query class; confidence/entropy only, no accuracy defined."}


def measure_latency(model, world, device):
    model.eval()
    X, T, Q, _ = stack_episodes([world.episode("test", "easy", 40000000)], device)
    def synchronize():
        if str(device).startswith("cuda"):
            torch.cuda.synchronize()
    with torch.no_grad():
        for _ in range(3):
            model(X, T, Q)
        synchronize()
        start = time.perf_counter()
        for _ in range(10):
            model(X, T, Q)
        synchronize()
    return (time.perf_counter() - start) * 1000 / 10


def aggregate_results(results):
    aggregate = {}
    for method in dict.fromkeys(row["method"] for row in results):
        rows = [row for row in results if row["method"] == method]
        aggregate[method] = {}
        for hardness in ("easy", "hard"):
            aggregate[method][hardness] = {}
            for metric in rows[0]["metrics"][hardness]:
                values = [row["metrics"][hardness][metric] for row in rows]
                aggregate[method][hardness][metric] = {
                    "mean": statistics.mean(values),
                    "std": statistics.stdev(values) if len(values) > 1 else 0.0,
                    "values": values,
                }
    return aggregate
