"""Run with python -m scripts.demo_fast_semantic_memory --device cpu."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import platform
import subprocess

import torch

from tovd.models import FastSemanticMemory


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--revision", default=None)
    args = parser.parse_args()
    torch.manual_seed(args.seed)
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    device = torch.device(args.device)
    # Generate on CPU so CPU and CUDA use the same initialization/input values.
    model = FastSemanticMemory(8).double()
    X, T, Q = (torch.randn(*shape, dtype=torch.float64).to(device) for shape in
               [(2, 6, 8), (2, 5, 8), (2, 3, 8)])
    model = model.to(device)
    first = model(X, T, Q)
    changed = model(X, -T, Q)
    repeated = model(X, T, Q)
    static = model(X, T, Q, enable_ttt=False)
    state_delta = torch.sqrt(sum((first.fast_state[name] - changed.fast_state[name]).square().sum()
                                 for name in first.fast_state))
    reset_delta = torch.sqrt(sum((first.fast_state[name] - repeated.fast_state[name]).square().sum()
                                 for name in first.fast_state))
    first.tokens.square().mean().backward()
    grad_norms = {name: parameter.grad.norm().item() for name, parameter in model.named_parameters()}
    revision = args.revision
    if revision is None:
        revision = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    report = {
        "task": "T001", "time_utc": datetime.now(timezone.utc).isoformat(),
        "revision": revision, "seed": args.seed,
        "environment": {"python": platform.python_version(), "torch": torch.__version__,
                        "device": str(device), "dtype": "float64", "cuda": torch.version.cuda,
                        "gpu": torch.cuda.get_device_name(device) if device.type == "cuda" else None},
        "config": {"B": 2, "N": 6, "C": 5, "M": 3, "D": 8, "hidden_dim": 16,
                   "inner_lr": model.inner_lr, "tau": model.tau,
                   "inner_steps": 1, "dataset": "synthetic Gaussian", "split": "not applicable",
                   "checkpoint": "none; seeded random initialization", "changed_vocabulary": "T2 = -T1"},
        "diagnostics": {name: value.cpu().tolist() for name, value in first.diagnostics.items()},
        "vocabulary_target_delta": (first.semantic_targets - changed.semantic_targets).norm().item(),
        "vocabulary_fast_state_delta": state_delta.item(),
        "vocabulary_output_delta": (first.tokens - changed.tokens).norm().item(),
        "reset_fast_state_delta": reset_delta.item(),
        "reset_output_delta": (first.tokens - repeated.tokens).norm().item(),
        "adapted_vs_static_output_delta": (first.tokens - static.tokens).norm().item(),
        "outer_gradient_norms": grad_norms,
        "outer_gradients_all_finite": all(torch.isfinite(p.grad).all().item() for p in model.parameters()),
        "interpretation": "Synthetic mechanism feasibility only; no evidence of detection accuracy gain."
    }
    rendered = json.dumps(report, indent=2, allow_nan=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
