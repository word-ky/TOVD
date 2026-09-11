"""T005 label-free O1 step controllers; no task scores enter selection."""

import torch
from torch.func import functional_call

from .fast_semantic_memory import alignment_loss
from .vocabulary_objectives import VocabularyObjectiveMemory

CONTROLLERS = ("O1_fixed", "O1_norm_matched", "O1_backtracking")
BACKTRACK_ETAS = (.05, .025, .0125, .00625, .003125)
ARMIJO_C = 1e-4
NORM_EPS = 1e-12


def gradient_norm(gradients):
    return torch.linalg.vector_norm(torch.cat([g.reshape(-1) for g in gradients]))


def choose_armijo_step(loss_at_eta, before, gradient_squared_norm):
    """Evaluate the fixed sequence, selecting the first label-free descent step."""
    for trials, eta in enumerate(BACKTRACK_ETAS, 1):
        after = loss_at_eta(eta)
        rhs = before - ARMIJO_C * eta * gradient_squared_norm
        if bool(torch.isfinite(after) & (after <= rhs)):
            return eta, trials, True
    return 0.0, len(BACKTRACK_ETAS), False


class O1StepMemory(VocabularyObjectiveMemory):
    def __init__(self, dim, hidden_dim=None, inner_lr=.05, tau=.2,
                 controller="O1_fixed", student_tau=.1):
        super().__init__(dim, hidden_dim, inner_lr, tau, objective="O1", student_tau=student_tau)
        self.controller = controller

    def select_update(self, params, grads, before, keys, X, T, target, meta_learning):
        if self.controller == "O1_fixed":
            return super().select_update(params, grads, before, keys, X, T, target, meta_learning)

        norm1 = gradient_norm(grads)
        if self.controller == "O1_norm_matched":
            pred = functional_call(self.fast_model, params, (keys,))
            loss0 = alignment_loss(pred, target)
            grads0 = torch.autograd.grad(loss0, tuple(params.values()), create_graph=meta_learning)
            norm0 = gradient_norm(grads0)
            guarded = (~torch.isfinite(norm0)) | (~torch.isfinite(norm1)) | (norm1 <= NORM_EPS)
            scale = norm1.new_zeros(()) if bool(guarded) else norm0 / (norm1 + NORM_EPS)
            adapted = dict(params) if bool(guarded) else {
                name: value - self.inner_lr * scale * grad
                for (name, value), grad in zip(params.items(), grads)}
            reference = {name: value - self.inner_lr * grad
                         for (name, value), grad in zip(params.items(), grads0)}
            actual = gradient_norm([adapted[name] - value for name, value in params.items()])
            budget = gradient_norm([reference[name] - value for name, value in params.items()])
            return adapted, {"step_scale": scale, "chosen_eta": self.inner_lr * scale,
                             "norm_guarded": guarded, "O0_gradient_norm": norm0,
                             "O0_update_budget": budget, "budget_absolute_error": (actual-budget).abs()}

        # Selection is intentionally nondifferentiated. The accepted update below
        # remains the same functional parameter path as the fixed-step baseline.
        with torch.no_grad():
            def trial(eta):
                candidate = {name: value - eta * grad for (name, value), grad in zip(params.items(), grads)}
                prediction = functional_call(self.fast_model, candidate, (keys,))
                return self.inner_objective(prediction, keys, X, T, target)
            eta, trials, accepted = choose_armijo_step(trial, before, norm1.square())
            rhs = before - ARMIJO_C * eta * norm1.square()
        adapted = {name: value - eta * grad for (name, value), grad in zip(params.items(), grads)} if accepted else dict(params)
        return adapted, {"chosen_eta": norm1.new_tensor(eta), "backtracking_trials": norm1.new_tensor(trials),
                         "step_accepted": norm1.new_tensor(accepted, dtype=torch.bool),
                         "step_rejected": norm1.new_tensor(not accepted, dtype=torch.bool),
                         "armijo_rhs": rhs}
