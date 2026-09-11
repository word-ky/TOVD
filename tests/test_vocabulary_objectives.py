import inspect
import os

import pytest
import torch
from torch.func import functional_call
from torch.nn import functional as F

from tovd.models.vocabulary_objectives import OBJECTIVES, VocabularyObjectiveMemory, centered_text
from tovd.synthetic.models import EpisodicClassifier


def inputs(dtype=torch.float64):
    torch.manual_seed(7)
    device = os.environ.get("TOVD_TEST_DEVICE", "cpu")
    return tuple(torch.randn(*shape, dtype=dtype).to(device) for shape in [(2, 6, 8), (2, 4, 8), (2, 3, 8)])


def test_O0_exactly_reproduces_P_and_all_parameter_counts_match():
    X, T, Q = inputs()
    models = []
    for method in ("P", *OBJECTIVES):
        torch.manual_seed(7)
        models.append(EpisodicClassifier(method, dim=8, hidden_dim=16).double().to(X.device))
    assert len({sum(p.numel() for p in model.parameters()) for model in models}) == 1
    a, b = models[0](X, T, Q), models[1](X, T, Q)
    torch.testing.assert_close(a.tokens, b.tokens, rtol=0, atol=0)
    for name in a.fast_state:
        torch.testing.assert_close(a.fast_state[name], b.fast_state[name], rtol=0, atol=0)
    for name in a.diagnostics:
        torch.testing.assert_close(a.diagnostics[name], b.diagnostics[name], rtol=0, atol=0)


@pytest.mark.parametrize("objective", OBJECTIVES)
def test_objective_equation_and_teacher_detach(objective):
    X, T, _ = inputs()
    memory = VocabularyObjectiveMemory(8, objective=objective).double().to(X.device)
    keys = X[0].clone().requires_grad_(True)
    pred = torch.randn_like(keys, requires_grad=True)
    text = centered_text(T[0]) if objective in ("O2", "O3") else T[0]
    assignment = torch.softmax(keys @ text.T / .2, dim=-1)
    target = memory.inner_targets(keys, X[0], T[0])
    actual = memory.inner_objective(pred, keys, X[0], T[0], target)
    if objective in ("O1", "O3"):
        logits = F.normalize(pred, dim=-1) @ F.normalize(text, dim=-1).T / .1
        expected = -(assignment.detach() * logits.log_softmax(-1)).sum(-1).mean()
        assert torch.autograd.grad(actual, keys, allow_unused=True, retain_graph=True)[0] is None
    else:
        expected = 1 - F.cosine_similarity(pred, assignment @ text, dim=-1).mean()
    torch.testing.assert_close(actual, expected, rtol=0, atol=0)


@pytest.mark.parametrize("objective", ["O1", "O2", "O3"])
def test_reset_permutation_label_free_and_meta_gradients(objective):
    X, T, Q = inputs()
    model = EpisodicClassifier(objective, dim=8, hidden_dim=16).double().to(X.device)
    initial = {name: p.detach().clone() for name, p in model.named_parameters()}
    first = model(X, T, Q)
    vocabulary_changed = model(X, -T, Q)
    assert sum((first.fast_state[name] - vocabulary_changed.fast_state[name]).square().sum()
               for name in first.fast_state) > 0
    model(-X, -T, -Q)
    repeated = model(X, T, Q)
    permuted = model(X, T.flip(1), Q)
    torch.testing.assert_close(first.tokens, repeated.tokens, rtol=0, atol=0)
    for name in first.fast_state:
        torch.testing.assert_close(first.fast_state[name], repeated.fast_state[name], rtol=0, atol=0)
    torch.testing.assert_close(first.tokens, permuted.tokens)
    first.tokens.square().mean().backward()
    for name, parameter in model.named_parameters():
        torch.testing.assert_close(parameter, initial[name], rtol=0, atol=0)
        assert parameter.grad is not None and torch.isfinite(parameter.grad).all()
        assert parameter.grad.norm() > 0
    assert list(inspect.signature(model.memory.forward).parameters) == ["X", "T", "Q", "enable_ttt"]
    assert list(inspect.signature(model.memory.inner_objective).parameters) == ["prediction", "keys", "X", "T", "target"]
    with pytest.raises(TypeError):
        model.memory(X, T, Q, labels=torch.zeros(2))


@pytest.mark.parametrize("objective", ["O1", "O2", "O3"])
def test_W0_gradient_through_new_objective_finite_difference(objective):
    X, T, Q = inputs()
    model = EpisodicClassifier(objective, dim=8, hidden_dim=16).double().to(X.device)
    params = dict(model.named_parameters())
    name = "memory.fast_model.output.weight"
    loss = model(X, T, Q).tokens.square().mean()
    grad = torch.autograd.grad(loss, params[name])[0]
    direction = torch.randn_like(grad)
    direction /= direction.norm()
    values = []
    for sign in (1, -1):
        shifted = {**params, name: params[name] + sign * 1e-5 * direction}
        values.append(functional_call(model, shifted, (X, T, Q)).tokens.square().mean())
    torch.testing.assert_close((grad * direction).sum(), (values[0]-values[1])/2e-5, rtol=1e-4, atol=1e-8)


@pytest.mark.parametrize("objective", ["O2", "O3"])
@pytest.mark.parametrize("kind", ["zero", "identical", "nearly_identical"])
def test_finite_centered_degenerate_vocabulary(objective, kind):
    X, T, Q = inputs(torch.float32)
    if kind == "zero":
        T = torch.zeros_like(T)
    else:
        T = T[:, :1].expand_as(T).clone()
        if kind == "nearly_identical":
            T = T + 1e-7 * torch.randn_like(T)
    model = EpisodicClassifier(objective, dim=8, hidden_dim=16).to(X.device)
    result = model(X, T, Q)
    assert result.diagnostics["all_finite"].all()
    assert torch.isfinite(centered_text(T)).all()
    result.tokens.square().mean().backward()
    assert all(torch.isfinite(p.grad).all() for p in model.parameters() if p.grad is not None)
