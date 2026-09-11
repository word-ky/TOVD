from dataclasses import replace
import inspect
import os
import json
import hashlib
from pathlib import Path

import pytest
import torch

from research_log.t003.oracle_diagnostic import (flatten, gradient_relation, oracle_diagnose_episode,
                                                oracle_evaluate_update, oracle_preupdate)
from tovd.synthetic.models import EpisodicClassifier
from tovd.synthetic.semantic_episodes import SemanticWorld, WorldConfig
from tovd.synthetic.benchmark import evaluate_model
from research_log.t003.oracle_diagnostic_run import distribution, run


@pytest.mark.parametrize("method", ["P", "B2"])
def test_oracle_diagnostic_matches_normal_and_preserves_parameters(method):
    torch.manual_seed(7)
    device = os.environ.get("TOVD_TEST_DEVICE", "cpu")
    model = EpisodicClassifier(method).to(device)
    ep = SemanticWorld(WorldConfig()).episode("test", "hard", 20070000).to(device)
    original = {name: p.detach().clone() for name, p in model.named_parameters()}
    result = oracle_diagnose_episode(model, ep)
    assert result["alignment"]["normal_output_max_error"] < 1e-6
    assert result["eta"]["0.0"]["nll_delta"] == 0
    assert result["eta"]["0.0"]["accuracy_delta"] == 0
    assert len(result["eta"]["0.05"]["query_nll_delta"]) == 8
    if method == "P":
        assert result["decomposition"]["weighted_reconstruction_max_error"] < 1e-6
        assert result["oracle_variants"]["all_soft"] == result["eta"]["0.05"]
        for group, count in (("foreground", 16), ("distractor", 8), ("background", 8)):
            assert len(result["ambiguity_tokens"][group]["entropy"]) == count
            assert result["decomposition"]["groups"][group]["token_count"] == count
    for name, parameter in model.named_parameters():
        torch.testing.assert_close(parameter, original[name], rtol=0, atol=0)
        assert parameter.grad is None
    assert list(inspect.signature(model.forward).parameters) == ["X", "T", "Q"]
    assert list(inspect.signature(model.memory.forward).parameters) == ["X", "T", "Q", "enable_ttt"]


def test_oracle_labels_do_not_change_normal_inner_gradient():
    torch.manual_seed(7)
    model = EpisodicClassifier("P")
    ep = SemanticWorld(WorldConfig()).episode("test", "easy", 20070000)
    a = oracle_preupdate(model, ep)
    changed = replace(ep, labels=(ep.labels + 1) % 4, image_ids=ep.image_ids.flip(0))
    b = oracle_preupdate(model, changed)
    torch.testing.assert_close(flatten(a["g_inner"]), flatten(b["g_inner"]), rtol=0, atol=0)
    assert not torch.allclose(flatten(a["g_task"]), flatten(b["g_task"]))


@pytest.mark.parametrize("method", ["P", "B2"])
def test_oracle_first_order_task_change_matches_finite_difference(method):
    torch.manual_seed(17)
    device = os.environ.get("TOVD_TEST_DEVICE", "cpu")
    model = EpisodicClassifier(method).double().to(device)
    ep = SemanticWorld(WorldConfig()).episode("test", "easy", 20170000).to(device)
    ep = replace(ep, X=ep.X.double(), T=ep.T.double(), Q=ep.Q.double())
    context = oracle_preupdate(model, ep)
    epsilon = 1e-5
    plus, _ = oracle_evaluate_update(model, ep, context, context["g_inner"], epsilon)
    minus, _ = oracle_evaluate_update(model, ep, context, context["g_inner"], -epsilon)
    derivative = (plus["nll"] - minus["nll"]) / (2 * epsilon)
    expected = -gradient_relation(context["g_inner"], context["g_task"])["dot"]
    assert derivative == pytest.approx(expected, rel=1e-5, abs=1e-8)


def test_oracle_exact_targets_respect_vocabulary_remapping():
    torch.manual_seed(7)
    model = EpisodicClassifier("P")
    ep = SemanticWorld(WorldConfig()).episode("test", "hard", 20070000)
    a = oracle_diagnose_episode(model, ep)
    b = oracle_diagnose_episode(model, ep.permute_vocabulary(torch.tensor([2, 0, 3, 1])))
    for variant in a["oracle_variants"]:
        for metric in ("accuracy", "nll", "margin"):
            assert a["oracle_variants"][variant][metric] == pytest.approx(b["oracle_variants"][variant][metric], abs=1e-6)


def test_oracle_source_reader_pairing_and_aggregation(tmp_path):
    device = os.environ.get("TOVD_TEST_DEVICE", "cpu")
    config = json.loads(Path("research_log/t002/config.json").read_text())
    config["eval_episodes"] = 2
    source = tmp_path / "source"
    source.mkdir()
    (source / "config.json").write_text(json.dumps(config))
    world = SemanticWorld(WorldConfig(**config["world"]))
    hashes = {}
    for method in ("P", "B2"):
        torch.manual_seed(7)
        model = EpisodicClassifier(method, **config["model"]).to(device)
        folder = source / f"seed7_{method}"
        folder.mkdir()
        checkpoint_path = folder / "checkpoint.pt"
        torch.save({"state_dict": model.state_dict(), "config": config, "revision": "unit-fixture-no-training"}, checkpoint_path)
        hashes[method] = hashlib.sha256(checkpoint_path.read_bytes()).hexdigest()
        _, episodes = evaluate_model(model, world, config, 7, device)
        (folder / "episodes.json").write_text(json.dumps(episodes))
    result = run(source, tmp_path / "diagnostic", device, "unit-test", seeds=(7,), episode_limit=2)
    for check in result["normal_T002_checks"]:
        assert max(check["original_T002_metric_max_errors"].values()) < 1e-6
    for checkpoint in result["environment"]["source_checkpoints"]:
        assert checkpoint["sha256"] == hashes[checkpoint["method"]]
        assert hashlib.sha256(Path(checkpoint["path"]).read_bytes()).hexdigest() == checkpoint["sha256"]
    assert result["aggregate"]["P"]["hard"]["alignment.cosine"]["pooled"]["count"] == 2
    assert result["aggregate"]["P"]["hard"]["ambiguity_tokens.foreground.entropy"]["pooled"]["count"] == 32
    assert (tmp_path / "diagnostic" / "tables.md").exists()
    assert distribution([1.0, 2.0, 3.0])["mean"] == 2.0
    assert distribution([1.0, 2.0, 3.0])["std"] == 1.0
