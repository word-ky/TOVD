import json
import os
from pathlib import Path

import pytest
import torch

from scripts.train_synthetic_semantic import run
from tovd.synthetic.benchmark import evaluate_model, outer_metrics
from tovd.synthetic.models import EpisodicClassifier
from tovd.synthetic.semantic_episodes import SemanticWorld, WorldConfig


def test_metric_known_prediction():
    similarities = torch.tensor([[[0.8, 0.1], [0.4, 0.5]]])
    logits = torch.zeros_like(similarities)
    y = torch.tensor([[0, 1]])
    metrics = outer_metrics(logits, similarities, y)
    assert metrics["accuracy"] == 0.5
    assert metrics["nll"] == pytest.approx(0.69314718056)
    assert metrics["margin"] == pytest.approx(0.4)


def test_all_methods_end_to_end_checkpoint_and_readonly_evaluation(tmp_path):
    config = json.loads(Path("research_log/t002/config.json").read_text())
    config.update(seeds=[7], train_steps=2, batch_size=2, eval_episodes=2, mechanism_episodes=2)
    device = os.environ.get("TOVD_TEST_DEVICE", "cpu")
    results = run(config, tmp_path, device, "unit-test-working-tree")
    assert len(results) == 5
    assert all(row["total_parameters"] == results[0]["total_parameters"] for row in results)
    assert results[-1]["W0_outer_drift"] == 0
    for row in results:
        for regime in ("easy", "hard"):
            assert 0 <= row["metrics"][regime]["accuracy"] <= 1
            assert row["metrics"][regime]["nll"] > 0
        assert row["mechanism"]["mean"]["reset_state_delta"] == 0
        assert row["mechanism"]["mean"]["reset_output_delta"] == 0
    saved = torch.load(tmp_path / "seed7_P" / "checkpoint.pt", map_location=device, weights_only=True)
    model = EpisodicClassifier("P", **config["model"]).to(device)
    model.load_state_dict(saved["state_dict"])
    params_before = {name: p.detach().clone() for name, p in model.named_parameters()}
    world = SemanticWorld(WorldConfig(**config["world"]))
    rerun, _ = evaluate_model(model, world, config, 7, device)
    assert rerun == results[3]["metrics"]
    for name, parameter in model.named_parameters():
        torch.testing.assert_close(parameter, params_before[name], rtol=0, atol=0)
        assert parameter.grad is None
    receipt = json.loads((tmp_path / "environment.json").read_text())
    assert set(receipt["train_classes"]).isdisjoint(receipt["test_classes"])
    assert (tmp_path / "summary.md").exists()
