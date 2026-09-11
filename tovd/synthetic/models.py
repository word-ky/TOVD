"""Matched T002 representations; labels are owned by the outer runner only."""

import torch
from torch import nn
from torch.nn import functional as F

from tovd.models import FastSemanticMemory, MemoryOutput
from tovd.models.vocabulary_objectives import OBJECTIVES, VocabularyObjectiveMemory
from tovd.models.step_control import CONTROLLERS, O1StepMemory

METHODS = ("B0", "B1", "B2", "P", "P_fixed")


class VisualFastMemory(FastSemanticMemory):
    def inner_targets(self, keys, X, T):
        # Generic visual reconstruction in the original visual space.
        return X


class EpisodicClassifier(nn.Module):
    def __init__(self, method, dim=16, hidden_dim=32, inner_lr=0.05, tau=0.2,
                 classifier_temperature=0.1):
        super().__init__()
        self.method = method
        self.classifier_temperature = classifier_temperature
        if method == "P_C2_meta":
            self.memory = O1StepMemory(dim, hidden_dim, inner_lr, tau,
                                       controller="O1_backtracking", student_tau=classifier_temperature)
        elif method in CONTROLLERS:
            self.memory = O1StepMemory(dim, hidden_dim, inner_lr, tau,
                                       controller=method, student_tau=classifier_temperature)
        elif method in OBJECTIVES:
            self.memory = VocabularyObjectiveMemory(dim, hidden_dim, inner_lr, tau,
                                                    objective=method, student_tau=classifier_temperature)
        else:
            memory_cls = VisualFastMemory if method == "B2" else FastSemanticMemory
            self.memory = memory_cls(dim, hidden_dim, inner_lr, tau)

    def forward(self, X, T, Q):
        if self.method in ("B2", "P", "P_fixed", "P_C2_meta", *OBJECTIVES, *CONTROLLERS):
            return self.memory(X, T, Q)
        result = self.memory(X, T, Q, enable_ttt=False)
        if self.method == "B0":
            return result
        # Stronger activation control: same T and image semantic context as P,
        # with exactly the same parameter tensors and no inner optimizer.
        r = result.tokens
        query_context = torch.softmax(r @ T.transpose(-1, -2) / self.memory.tau, dim=-1) @ T
        keys = self.memory.key_projection(X)
        scene_targets = self.memory.inner_targets(keys, X, T)
        output = r + 0.5 * query_context + 0.5 * scene_targets.mean(dim=1, keepdim=True)
        return MemoryOutput(output, result.fast_state, scene_targets.detach(), {})

    def similarities(self, tokens, T):
        return F.normalize(tokens, dim=-1) @ F.normalize(T, dim=-1).transpose(-1, -2)

    def logits(self, tokens, T):
        return self.similarities(tokens, T) / self.classifier_temperature

    def outer_parameters(self):
        # W0 still requires autograd for the label-free inner step. It is only
        # excluded from Adam; do not set requires_grad=False on fast weights.
        return [parameter for name, parameter in self.named_parameters()
                if not (self.method == "P_fixed" and name.startswith("memory.fast_model."))]
