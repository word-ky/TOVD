import inspect
import os

import pytest
import torch
from torch.func import functional_call

from tovd.models import FastSemanticMemory


@pytest.fixture
def case():
    torch.manual_seed(7)
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    device = os.environ.get("TOVD_TEST_DEVICE", "cpu")
    model = FastSemanticMemory(8).double()
    X, T, Q = (torch.randn(*shape, dtype=torch.float64) for shape in
               [(2, 6, 8), (2, 5, 8), (2, 3, 8)])
    return model.to(device), X.to(device), T.to(device), Q.to(device)


def state_vector(result):
    return torch.cat([value.flatten() for value in result.fast_state.values()])


def test_shape_update_loss_and_finiteness(case):
    model, X, T, Q = case
    result = model(X, T, Q)
    assert result.tokens.shape == Q.shape
    assert result.semantic_targets.shape == X.shape
    keys = model.key_projection(X)
    expected = torch.softmax(keys @ T.transpose(-1, -2) / model.tau, dim=-1) @ T
    torch.testing.assert_close(result.semantic_targets, expected)
    for name, value in model.fast_model.named_parameters():
        assert result.fast_state[name].shape == (2, *value.shape)
    d = result.diagnostics
    assert (d["fast_update_norm"] > 0).all()
    assert (d["inner_gradient_norm"] > 0).all()
    assert (d["inner_loss_after"] < d["inner_loss_before"]).all()
    torch.testing.assert_close(d["fast_update_norm"], model.inner_lr * d["inner_gradient_norm"])
    assert d["all_finite"].all()
    assert torch.isfinite(result.tokens).all()


def test_reset_after_intervening_episode_and_no_parameter_mutation(case):
    model, X, T, Q = case
    original = {name: value.detach().clone() for name, value in model.named_parameters()}
    first = model(X, T, Q)
    model(X + 2, T - 3, Q + 1)
    repeated = model(X, T, Q)
    torch.testing.assert_close(first.tokens, repeated.tokens, rtol=0, atol=0)
    torch.testing.assert_close(state_vector(first), state_vector(repeated), rtol=0, atol=0)
    for name, value in model.named_parameters():
        torch.testing.assert_close(value, original[name], rtol=0, atol=0)
        assert value.grad is None


def test_per_image_state_is_independent_of_batch_neighbors(case):
    model, X, T, Q = case
    batched = model(X, T, Q)
    for index in range(2):
        alone = model(X[index:index+1], T[index:index+1], Q[index:index+1])
        torch.testing.assert_close(batched.tokens[index], alone.tokens[0])
        for name in alone.fast_state:
            torch.testing.assert_close(batched.fast_state[name][index], alone.fast_state[name][0])


def test_vocabulary_changes_targets_fast_state_and_output(case):
    model, X, T, Q = case
    first, second = model(X, T, Q), model(X, -T, Q)
    assert torch.linalg.vector_norm(first.semantic_targets - second.semantic_targets) > 1e-5
    assert torch.linalg.vector_norm(state_vector(first) - state_vector(second)) > 1e-5
    assert torch.linalg.vector_norm(first.tokens - second.tokens) > 1e-5


def test_vocabulary_permutation_preserves_state(case):
    model, X, T, Q = case
    first, permuted = model(X, T, Q), model(X, T.flip(1), Q)
    torch.testing.assert_close(first.tokens, permuted.tokens)
    torch.testing.assert_close(state_vector(first), state_vector(permuted))


def test_api_has_no_labels(case):
    model, X, T, Q = case
    assert list(inspect.signature(model.forward).parameters) == ["X", "T", "Q", "enable_ttt"]
    with pytest.raises(TypeError, match="labels"):
        model(X, T, Q, labels=torch.zeros(2))


def test_outer_gradients_reach_initialization_and_both_projections(case):
    model, X, T, Q = case
    model(X, T, Q).tokens.square().mean().backward()
    for name, parameter in model.named_parameters():
        assert parameter.grad is not None, name
        assert torch.isfinite(parameter.grad).all(), name
        assert parameter.grad.norm() > 0, name


def test_outer_gradient_matches_finite_difference_through_inner_update(case):
    model, X, T, Q = case
    # Directional checks on W0 and P_k catch a detached/first-order update;
    # a nonzero W0 gradient alone would also pass through the direct path.
    loss = model(X, T, Q).tokens.square().mean()
    names = ["fast_model.output.weight", "key_projection.weight"]
    params = dict(model.named_parameters())
    grads = torch.autograd.grad(loss, [params[name] for name in names])
    for name, grad in zip(names, grads):
        direction = torch.randn_like(params[name])
        direction /= direction.norm()
        epsilon = 1e-5
        values = []
        for sign in (1, -1):
            shifted = dict(params)
            shifted[name] = params[name] + sign * epsilon * direction
            values.append(functional_call(model, shifted, (X, T, Q)).tokens.square().mean())
        numeric = (values[0] - values[1]) / (2 * epsilon)
        analytic = (grad * direction).sum()
        torch.testing.assert_close(analytic, numeric, rtol=1e-4, atol=1e-8)


def test_static_control_is_exact_and_vocabulary_independent(case):
    model, X, T, Q = case
    result = model(X, T, Q, enable_ttt=False)
    expected = model.fast_model(model.query_projection(Q))
    torch.testing.assert_close(result.tokens, expected, rtol=0, atol=0)
    other = model(X + 1, -T, Q, enable_ttt=False)
    torch.testing.assert_close(result.tokens, other.tokens, rtol=0, atol=0)
    assert result.semantic_targets is None
    assert result.diagnostics == {}
    for name, value in model.fast_model.named_parameters():
        torch.testing.assert_close(result.fast_state[name][0], value)


def test_eval_under_no_grad_still_adapts(case):
    model, X, T, Q = case
    training = model(X, T, Q)
    model.eval()
    with torch.no_grad():
        result = model(X, T, Q)
    torch.testing.assert_close(result.tokens, training.tokens)
    torch.testing.assert_close(state_vector(result), state_vector(training))
    assert not result.tokens.requires_grad
    assert result.diagnostics["all_finite"].all()
    assert (result.diagnostics["fast_update_norm"] > 0).all()
