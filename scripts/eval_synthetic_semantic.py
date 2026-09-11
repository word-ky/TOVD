"""Re-evaluate a saved final checkpoint without outer optimization."""

import argparse
import json
from pathlib import Path

import torch

from tovd.synthetic.benchmark import evaluate_model, mechanism_analysis
from tovd.synthetic.models import EpisodicClassifier
from tovd.synthetic.semantic_episodes import SemanticWorld, WorldConfig


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--device", default="cpu")
    args = parser.parse_args()
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    checkpoint = torch.load(args.checkpoint, map_location=args.device, weights_only=True)
    config, seed = checkpoint["config"], checkpoint["seed"]
    world = SemanticWorld(WorldConfig(**config["world"]))
    model = EpisodicClassifier(checkpoint["method"], **config["model"]).to(args.device)
    model.load_state_dict(checkpoint["state_dict"])
    metrics, episodes = evaluate_model(model, world, config, seed, args.device)
    result = {"revision": checkpoint["revision"], "seed": seed, "method": checkpoint["method"],
              "metrics": metrics, "episodes": episodes,
              "mechanism": mechanism_analysis(model, world, config, seed, args.device)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
