import copy
import hashlib
import json
import os
from pathlib import Path

import pytest
import torch

from research_log.t004.oracle_objective_screen import oracle_screen_episode, run, select_candidates
from tovd.synthetic.benchmark import evaluate_model
from tovd.synthetic.models import EpisodicClassifier
from tovd.synthetic.semantic_episodes import SemanticWorld, WorldConfig


@pytest.mark.parametrize("objective", ["O0", "O1", "O2", "O3"])
def test_screen_matches_normal_objective_and_preserves_state(objective):
    torch.manual_seed(7)
    device = os.environ.get("TOVD_TEST_DEVICE", "cpu")
    model = EpisodicClassifier(objective).to(device)
    original = copy.deepcopy(model.state_dict())
    episode = SemanticWorld(WorldConfig()).episode("test", "hard", 20070000).to(device)
    result = oracle_screen_episode(model, episode)
    assert result["normal_output_max_error"] < 1e-6
    assert result["all_finite"]
    assert result["after"]["update_norm"] == pytest.approx(.05 * result["alignment"]["gradient_norm"])
    assert len(result["assignment_tokens"]["foreground"]["assignment_correct"]) == 16
    assert len(result["after"]["query_nll_delta"]) == 8
    for name, value in model.state_dict().items():
        torch.testing.assert_close(value, original[name], rtol=0, atol=0)


def test_preregistered_screen_gate_and_ranking():
    baseline = {"hard": {"after.nll_delta": {"mean": .01}, "alignment.cosine": {"mean": -.01}},
                "easy": {"after.nll": {"mean": .7}, "after.accuracy": {"mean": .75}}}
    aggregate = {name: copy.deepcopy(baseline) for name in ("O0", "O1", "O2", "O3")}
    assert select_candidates(aggregate)["selected"] == []
    for name, nll, cosine in (("O1", -.03, .02), ("O2", -.04, .05), ("O3", -.04, .10)):
        aggregate[name]["hard"]["after.nll_delta"]["mean"] = nll
        aggregate[name]["hard"]["alignment.cosine"]["mean"] = cosine
    assert select_candidates(aggregate)["selected"] == ["O3", "O2"]
    aggregate["O3"]["easy"]["after.nll"]["mean"] = .81
    aggregate["O2"]["easy"]["after.accuracy"]["mean"] = .69
    assert select_candidates(aggregate)["selected"] == ["O1"]
    # Alignment alone is sufficient, as explicitly allowed by Phase 1.
    aggregate["O1"]["hard"]["after.nll_delta"]["mean"] = .02
    aggregate["O1"]["hard"]["alignment.cosine"]["mean"] = .06
    assert select_candidates(aggregate)["selected"] == ["O1"]


def test_screen_source_pairing_and_hashes(tmp_path):
    device = os.environ.get("TOVD_TEST_DEVICE", "cpu")
    config = json.loads(Path("research_log/t002/config.json").read_text())
    config["eval_episodes"] = 2
    source = tmp_path / "source"
    folder = source / "seed7_P"
    folder.mkdir(parents=True)
    (source / "config.json").write_text(json.dumps(config))
    torch.manual_seed(7)
    model = EpisodicClassifier("P", **config["model"]).to(device)
    checkpoint = folder / "checkpoint.pt"
    torch.save({"state_dict": model.state_dict(), "config": config, "revision": "unit-fixture"}, checkpoint)
    original_hash = hashlib.sha256(checkpoint.read_bytes()).hexdigest()
    _, episodes = evaluate_model(model, SemanticWorld(WorldConfig(**config["world"])), config, 7, device)
    (folder / "episodes.json").write_text(json.dumps(episodes))
    result = run(source, tmp_path / "screen", device, "unit-test", seeds=(7,), episode_limit=2)
    assert hashlib.sha256(checkpoint.read_bytes()).hexdigest() == original_hash
    assert result["environment"]["source_checkpoints"][0]["sha256"] == original_hash
    for check in result["original_O0_checks"]:
        assert max(check["errors"].values()) < 1e-6
    assert result["aggregate"]["O3"]["hard"]["alignment.cosine"]["pooled"]["count"] == 2
    assert (tmp_path / "screen" / "selection.json").exists()
