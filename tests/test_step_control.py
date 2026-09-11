import inspect
import os

import pytest
import torch
from torch.func import functional_call

from tovd.models.step_control import ARMIJO_C, BACKTRACK_ETAS, choose_armijo_step, gradient_norm
from tovd.synthetic.models import EpisodicClassifier
from tovd.synthetic.benchmark import state_distance
from tovd.synthetic.semantic_episodes import SemanticWorld, WorldConfig


def fixture(method, dtype=torch.float64):
    torch.manual_seed(7)
    device = os.environ.get("TOVD_TEST_DEVICE", "cpu")
    model = EpisodicClassifier(method).to(device=device, dtype=dtype)
    ep = SemanticWorld(WorldConfig()).episode("test", "easy", 20070000).to(device)
    inputs = [x.to(dtype).unsqueeze(0) for x in (ep.X, ep.T, ep.Q)]
    return model, inputs


def test_fixed_O1_alias_is_exact_and_parameter_layout_unchanged():
    a, inputs = fixture("O1")
    b, _ = fixture("O1_fixed")
    left, right = a(*inputs), b(*inputs)
    torch.testing.assert_close(left.tokens, right.tokens, rtol=0, atol=0)
    assert state_distance(left, right) == 0
    for name in left.diagnostics:
        torch.testing.assert_close(left.diagnostics[name], right.diagnostics[name], rtol=0, atol=0)
    for method in ("O1_norm_matched", "O1_backtracking"):
        other, _ = fixture(method)
        assert sum(p.numel() for p in other.parameters()) == 2128
        assert list(other.state_dict()) == list(a.state_dict())


def test_norm_matched_realized_budget_and_direction():
    model, inputs = fixture("O1_norm_matched")
    fixed, _ = fixture("O1_fixed")
    original, _ = fixture("O0")
    a, b, c = model(*inputs), fixed(*inputs), original(*inputs)
    initial = dict(model.memory.fast_model.named_parameters())
    da = torch.cat([(a.fast_state[n][0]-p).reshape(-1) for n,p in initial.items()])
    db = torch.cat([(b.fast_state[n][0]-p).reshape(-1) for n,p in initial.items()])
    dc = torch.cat([(c.fast_state[n][0]-p).reshape(-1) for n,p in initial.items()])
    torch.testing.assert_close(da.norm(), dc.norm(), rtol=1e-10, atol=1e-12)
    torch.testing.assert_close(da, db*a.diagnostics["step_scale"][0], rtol=1e-10, atol=1e-12)
    assert not a.diagnostics["norm_guarded"].any()


@pytest.mark.parametrize("bad", [0.0, 1e-15, float("nan"), float("inf")])
def test_norm_matched_requested_near_zero_and_finite_guard(bad):
    model, (X,T,Q) = fixture("O1_norm_matched")
    memory = model.memory
    params = dict(memory.fast_model.named_parameters())
    keys = memory.key_projection(X)[0]
    target = memory.inner_targets(keys, X[0], T[0])
    grads = tuple(torch.full_like(p, bad) for p in params.values())
    adapted, diag = memory.select_update(params, grads, keys.new_tensor(1.), keys, X[0], T[0], target, True)
    assert diag["norm_guarded"] and diag["step_scale"] == 0
    for name in params:
        torch.testing.assert_close(adapted[name], params[name], rtol=0, atol=0)


def test_armijo_first_acceptance_and_all_rejected():
    before = torch.tensor(1., dtype=torch.float64)
    seen = []
    def loss(eta):
        seen.append(eta)
        return torch.tensor((1-50*eta)**2, dtype=torch.float64)
    eta, trials, accepted = choose_armijo_step(loss, before, torch.tensor(2500.))
    assert (eta, trials, accepted) == (.025, 2, True)
    assert seen == [.05,.025]
    assert choose_armijo_step(lambda eta: before+1, before, torch.tensor(1.)) == (0.,5,False)


@pytest.mark.parametrize("method", ["O1_fixed", "O1_norm_matched", "O1_backtracking"])
def test_controller_reset_vocabulary_determinism_and_label_free_api(method):
    model, (X,T,Q) = fixture(method, torch.float32)
    model.eval()
    original = {n:p.clone() for n,p in model.named_parameters()}
    with torch.no_grad():
        a = model(X,T,Q)
        changed = model(X,-T,Q)
        repeated = model(X,T,Q)
    assert state_distance(a,repeated) == 0
    torch.testing.assert_close(a.tokens,repeated.tokens,rtol=0,atol=0)
    assert state_distance(a,changed) > 0
    assert a.diagnostics["all_finite"].all()
    assert list(inspect.signature(model.forward).parameters) == ["X","T","Q"]
    assert list(inspect.signature(model.memory.select_update).parameters) == ["params","grads","before","keys","X","T","target","meta_learning"]
    with pytest.raises(TypeError):
        model(X,T,Q,labels=torch.zeros(8))
    for name,p in model.named_parameters():
        torch.testing.assert_close(p,original[name],rtol=0,atol=0)
    if method == "O1_backtracking":
        diag = a.diagnostics
        if diag["step_accepted"][0]:
            assert diag["inner_loss_after"][0] <= diag["armijo_rhs"][0]
        else:
            assert diag["chosen_eta"][0] == 0
            assert diag["fast_update_norm"][0] == 0


def test_C1_W0_meta_gradient_finite_difference_and_projection_flow():
    model, inputs = fixture("O1_norm_matched")
    params = dict(model.named_parameters())
    loss = model(*inputs).tokens.square().mean()
    loss.backward()
    assert all(p.grad is not None and torch.isfinite(p.grad).all() and p.grad.norm()>0 for p in params.values())
    name = "memory.fast_model.output.weight"
    direction = torch.randn_like(params[name])
    direction /= direction.norm()
    values = []
    for sign in (1,-1):
        shifted = {**params, name:params[name]+sign*1e-5*direction}
        values.append(functional_call(model,shifted,tuple(inputs)).tokens.square().mean())
    torch.testing.assert_close((params[name].grad*direction).sum(),(values[0]-values[1])/2e-5,rtol=1e-4,atol=1e-8)
