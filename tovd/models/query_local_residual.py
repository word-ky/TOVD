"""T011 frozen-model, independent zero-initialized query residuals."""

from dataclasses import dataclass

import torch
from torch.nn import functional as F

from .step_control import ARMIJO_C, BACKTRACK_ETAS


def local_teacher(keys, queries, text, teacher_tau=.2, tau_q=.2, uniform=False):
    keys, queries, text = (F.normalize(t, dim=-1, eps=1e-12) for t in (keys, queries, text))
    token_teacher = (keys @ text.transpose(-1, -2) / teacher_tau).softmax(-1)
    scores = queries @ keys.transpose(-1, -2)
    attention = torch.full_like(scores, 1 / keys.shape[-2]) if uniform else (scores / tau_q).softmax(-1)
    return attention @ token_teacher, attention, token_teacher


def local_loss(tokens, text, teacher, student_tau=.1):
    logits = F.normalize(tokens, dim=-1, eps=1e-12) @ F.normalize(text, dim=-1, eps=1e-12).transpose(-1, -2)
    return -(teacher * (logits / student_tau).log_softmax(-1)).sum(-1)


@torch.no_grad()
def local_armijo(z0, text, teacher, gradient, before, student_tau=.1):
    eta = torch.zeros_like(before)
    trials = torch.full_like(before, len(BACKTRACK_ETAS), dtype=torch.long)
    accepted = torch.zeros_like(before, dtype=torch.bool)
    norm_squared = gradient.square().sum(-1)
    for trial_index, candidate_eta in enumerate(BACKTRACK_ETAS, 1):
        after = local_loss(z0 - candidate_eta * gradient, text, teacher, student_tau)
        take = ~accepted & torch.isfinite(after) & (after <= before - ARMIJO_C * candidate_eta * norm_squared)
        eta = torch.where(take, candidate_eta, eta)
        trials = torch.where(take, trial_index, trials)
        accepted |= take
    residual = -eta[..., None] * gradient
    return residual, eta, trials, accepted


@dataclass
class ResidualOutput:
    tokens: torch.Tensor
    residual: torch.Tensor
    teacher: torch.Tensor
    attention: torch.Tensor
    token_teacher: torch.Tensor
    diagnostics: dict[str, torch.Tensor]


def query_local_residual(memory, X, T, Q, *, tau_q=.2, teacher_tau=.2, student_tau=.1, uniform=False):
    """Inputs B,N,D / B,C,D / B,M,D; only a fresh B,M,D residual gets gradients."""
    with torch.no_grad():
        keys = memory.key_projection(X)
        queries = memory.query_projection(Q)
        z0 = memory.fast_model(queries)
        teacher, attention, token_teacher = local_teacher(keys, queries, T, teacher_tau, tau_q, uniform)
    with torch.enable_grad():
        initial = torch.zeros_like(z0, requires_grad=True)
        before = local_loss(z0 + initial, T.detach(), teacher, student_tau)
        gradient, = torch.autograd.grad(before.sum(), initial)
    with torch.no_grad():
        residual, eta, trials, accepted = local_armijo(z0, T, teacher, gradient, before.detach(), student_tau)
        tokens = z0 + residual
        after = local_loss(tokens, T, teacher, student_tau)
        norm = residual.norm(dim=-1)
        entropy = -(attention * attention.clamp_min(1e-12).log()).sum(-1)
        finite = (torch.isfinite(tokens).all(-1) & torch.isfinite(residual).all(-1)
                  & torch.isfinite(gradient).all(-1) & torch.isfinite(teacher).all(-1)
                  & torch.isfinite(attention).all(-1) & torch.isfinite(before) & torch.isfinite(after))
        diagnostics = dict(inner_loss_before=before.detach(), inner_loss_after=after,
                           inner_gradient_norm=gradient.norm(dim=-1), chosen_eta=eta,
                           backtracking_trials=trials, step_accepted=accepted,
                           armijo_rhs=before.detach()-ARMIJO_C*eta*gradient.square().sum(-1),
                           residual_norm=norm, normalized_residual_norm=norm/(z0.norm(dim=-1)+1e-12),
                           attention_entropy=entropy, effective_token_count=entropy.exp(),
                           zero_initialization=(initial == 0).all(-1), all_finite=finite)
    return ResidualOutput(tokens, residual, teacher, attention, token_teacher, diagnostics)
