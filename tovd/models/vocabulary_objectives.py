"""T004 label-free relative-vocabulary inner objectives, no added parameters."""

import torch
from torch.nn import functional as F

from .fast_semantic_memory import FastSemanticMemory, alignment_loss

OBJECTIVES = ("O0", "O1", "O2", "O3")


def centered_text(T):
    return F.normalize(T - T.mean(dim=-2, keepdim=True), dim=-1, eps=1e-6)


class VocabularyObjectiveMemory(FastSemanticMemory):
    def __init__(self, dim, hidden_dim=None, inner_lr=0.05, tau=0.2,
                 objective="O0", student_tau=0.1):
        super().__init__(dim, hidden_dim, inner_lr, tau)
        self.objective = objective
        self.student_tau = student_tau

    def objective_text(self, T):
        return centered_text(T) if self.objective in ("O2", "O3") else T

    def assignments(self, keys, T):
        text = self.objective_text(T)
        return torch.softmax(keys @ text.transpose(-1, -2) / self.tau, dim=-1)

    def inner_targets(self, keys, X, T):
        # For O1/O3 this is only an inspection snapshot, not the loss target.
        return self.assignments(keys, T) @ self.objective_text(T)

    def inner_objective(self, prediction, keys, X, T, target):
        if self.objective in ("O0", "O2"):
            return alignment_loss(prediction, target)
        text = self.objective_text(T)
        teacher = self.assignments(keys, T).detach()
        logits = F.normalize(prediction, dim=-1) @ F.normalize(text, dim=-1).transpose(-1, -2)
        return -(teacher * F.log_softmax(logits / self.student_tau, dim=-1)).sum(-1).mean()
