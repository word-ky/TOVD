import torch
import pytest
import inspect
import os
from torch.nn import functional as F

from tovd.synthetic.semantic_episodes import SemanticWorld, WorldConfig, stack_episodes
from tovd.synthetic.models import EpisodicClassifier, METHODS


def test_class_split_and_foreground_label_alignment():
    world = SemanticWorld(WorldConfig())
    assert not torch.isin(world.train_ids, world.test_ids).any()
    assert not torch.isin(world.cluster_ids[world.train_ids], world.cluster_ids[world.test_ids]).any()
    for split in ("train", "test"):
        for hardness in ("easy", "hard"):
            ep = world.episode(split, hardness, 7)
            allowed = world.split_ids(split)
            assert torch.isin(ep.query_ids, allowed).all()
            assert torch.isin(ep.vocabulary_ids, allowed).all()
            assert torch.isin(ep.image_ids[ep.image_ids >= 0], allowed).all()
            torch.testing.assert_close(ep.vocabulary_ids[ep.labels], ep.query_ids)
            assert (ep.image_ids == -1).sum() == world.config.background_tokens
            unique_clusters = world.cluster_ids[ep.vocabulary_ids].unique().numel()
            assert unique_clusters == (1 if hardness == "hard" else 4)


def test_determinism_and_nonidentical_modalities():
    world = SemanticWorld(WorldConfig())
    first, second = world.episode("test", "easy", 8), world.episode("test", "easy", 8)
    for name in vars(first):
        torch.testing.assert_close(getattr(first, name), getattr(second, name), rtol=0, atol=0)
    assert not torch.allclose(first.Q, first.T[first.labels])
    X, T, Q, labels = stack_episodes([first, second])
    assert (X.shape, T.shape, Q.shape, labels.shape) == ((2, 32, 16), (2, 4, 16), (2, 8, 16), (2, 8))


def test_vocab_order_remapping_and_no_fixed_correct_index():
    world = SemanticWorld(WorldConfig())
    ep = world.episode("test", "hard", 5)
    order = torch.tensor([2, 0, 3, 1])
    changed = ep.permute_vocabulary(order)
    torch.testing.assert_close(changed.vocabulary_ids[changed.labels], ep.query_ids)
    torch.testing.assert_close(changed.Q, ep.Q)
    histogram = torch.bincount(torch.cat([world.episode("train", "easy", seed).labels
                                         for seed in range(40)]), minlength=4)
    assert (histogram > 20).all()
    assert (histogram < 140).all()


def test_hardness_and_fixed_scene_negative_control():
    world = SemanticWorld(WorldConfig())
    easy_sim, hard_sim = [], []
    for seed in range(20):
        easy, hard, unrelated, unrelated_ids = world.paired_scene(seed)
        torch.testing.assert_close(easy.X, hard.X, rtol=0, atol=0)
        torch.testing.assert_close(easy.Q, hard.Q, rtol=0, atol=0)
        assert not torch.isin(easy.query_ids, unrelated_ids).any()
        assert unrelated.shape == easy.T.shape
        mask = ~torch.eye(4, dtype=torch.bool)
        easy_sim.append((easy.T @ easy.T.T)[mask].mean())
        hard_sim.append((hard.T @ hard.T.T)[mask].mean())
    assert torch.stack(hard_sim).mean() > torch.stack(easy_sim).mean() + 0.4


@pytest.mark.parametrize("method", METHODS)
def test_model_permutation_reset_gradient_and_label_free_contract(method):
    torch.manual_seed(7)
    device = os.environ.get("TOVD_TEST_DEVICE", "cpu")
    model = EpisodicClassifier(method).to(device)
    world = SemanticWorld(WorldConfig())
    ep = world.episode("train", "hard", 11)
    X, T, Q, y = stack_episodes([ep], device)
    before = {name: value.detach().clone() for name, value in model.named_parameters()}
    first = model(X, T, Q)
    other_ep = ep.permute_vocabulary(torch.tensor([2, 0, 3, 1]))
    X2, T2, Q2, y2 = stack_episodes([other_ep], device)
    changed = model(X2, T2, Q2)
    torch.testing.assert_close(first.tokens, changed.tokens, rtol=1e-5, atol=1e-6)
    l1 = F.cross_entropy(model.logits(first.tokens, T).flatten(0, 1), y.flatten())
    l2 = F.cross_entropy(model.logits(changed.tokens, T2).flatten(0, 1), y2.flatten())
    torch.testing.assert_close(l1, l2)
    accuracy1 = (model.logits(first.tokens, T).argmax(-1) == y).float().mean()
    accuracy2 = (model.logits(changed.tokens, T2).argmax(-1) == y2).float().mean()
    torch.testing.assert_close(accuracy1, accuracy2, rtol=0, atol=0)
    model(X + 1, -T, Q)
    repeated = model(X, T, Q)
    torch.testing.assert_close(first.tokens, repeated.tokens, rtol=0, atol=0)
    for name, value in model.named_parameters():
        torch.testing.assert_close(value, before[name], rtol=0, atol=0)
    l1.backward()
    assert model.memory.query_projection.weight.grad.norm() > 0
    assert all(torch.isfinite(p.grad).all() for p in model.parameters() if p.grad is not None)
    assert list(inspect.signature(model.forward).parameters) == ["X", "T", "Q"]
    with pytest.raises(TypeError):
        model(X, T, Q, labels=y)


def test_visual_target_is_exact_and_vocab_independent():
    torch.manual_seed(0)
    model = EpisodicClassifier("B2")
    world = SemanticWorld(WorldConfig())
    X, T, Q, _ = stack_episodes([world.episode("train", "easy", 5)])
    a, b = model(X, T, Q), model(X, -T, Q)
    torch.testing.assert_close(a.semantic_targets, X, rtol=0, atol=0)
    torch.testing.assert_close(a.tokens, b.tokens, rtol=0, atol=0)


def test_matched_initialization_parameter_counts_and_fixed_W0():
    models = []
    for method in METHODS:
        torch.manual_seed(7)
        models.append(EpisodicClassifier(method))
    assert len({sum(p.numel() for p in model.parameters()) for model in models}) == 1
    for model in models[1:]:
        for first, other in zip(models[0].parameters(), model.parameters()):
            torch.testing.assert_close(first, other, rtol=0, atol=0)
    fixed = models[-1]
    initial = {name: p.detach().clone() for name, p in fixed.named_parameters()}
    world = SemanticWorld(WorldConfig())
    X, T, Q, y = stack_episodes([world.episode("train", "easy", 8)])
    optimizer = torch.optim.Adam(fixed.outer_parameters(), lr=0.001)
    F.cross_entropy(fixed.logits(fixed(X, T, Q).tokens, T).flatten(0, 1), y.flatten()).backward()
    optimizer.step()
    for name, parameter in fixed.memory.fast_model.named_parameters():
        torch.testing.assert_close(parameter, initial["memory.fast_model." + name], rtol=0, atol=0)
    assert not torch.equal(fixed.memory.query_projection.weight, initial["memory.query_projection.weight"])
