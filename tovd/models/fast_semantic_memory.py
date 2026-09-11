"""One differentiable, label-free, per-image fast semantic update."""

from dataclasses import dataclass

import torch
from torch import Tensor, nn
from torch.func import functional_call
from torch.nn import functional as F


class GatedMLP(nn.Module):
    def __init__(self, dim: int, hidden_dim: int):
        super().__init__()
        self.value = nn.Linear(dim, hidden_dim)
        self.gate = nn.Linear(dim, hidden_dim)
        self.output = nn.Linear(hidden_dim, dim)

    def forward(self, tokens: Tensor) -> Tensor:
        return self.output(F.gelu(self.value(tokens)) * torch.sigmoid(self.gate(tokens)))


@dataclass
class MemoryOutput:
    tokens: Tensor
    # Detached per-image snapshots: each parameter has leading dimension B.
    fast_state: dict[str, Tensor]
    semantic_targets: Tensor | None
    # Per-image detached diagnostics; empty for the static control.
    diagnostics: dict[str, Tensor]


def alignment_loss(prediction: Tensor, target: Tensor) -> Tensor:
    return 1 - F.cosine_similarity(prediction, target, dim=-1).mean()


class FastSemanticMemory(nn.Module):
    """Map X[B,N,D], T[B,C,D], Q[B,M,D] to adapted tokens[B,M,D].

    Slow parameters: key/query projections and the meta-initialization in
    ``fast_model``. Only functional copies of fast_model parameters adapt.
    Each image starts at W0; no fast state is retained between calls.
    Training uses exact differentiation through the gradient step. Evaluation
    uses a first-order inner computation and also works under torch.no_grad().
    """

    def __init__(self, dim: int, hidden_dim: int | None = None,
                 inner_lr: float = 0.05, tau: float = 1.0):
        super().__init__()
        self.key_projection = nn.Linear(dim, dim, bias=False)
        self.query_projection = nn.Linear(dim, dim, bias=False)
        self.fast_model = GatedMLP(dim, hidden_dim or 2 * dim)
        self.inner_lr = inner_lr
        self.tau = tau

    def inner_targets(self, keys: Tensor, X: Tensor, T: Tensor) -> Tensor:
        return torch.softmax(keys @ T.transpose(-1, -2) / self.tau, dim=-1) @ T

    def inner_objective(self, prediction: Tensor, keys: Tensor, X: Tensor,
                        T: Tensor, target: Tensor) -> Tensor:
        return alignment_loss(prediction, target)

    def select_update(self, params, grads, before, keys, X, T, target, meta_learning):
        return {name: value - self.inner_lr * grad
                for (name, value), grad in zip(params.items(), grads)}, {}

    def forward(self, X: Tensor, T: Tensor, Q: Tensor,
                *, enable_ttt: bool = True) -> MemoryOutput:
        batch_size = Q.shape[0]
        initial = dict(self.fast_model.named_parameters())
        if not enable_ttt:
            # Exact static control: F_W0(P_q(Q)), independent of X and T.
            tokens = self.fast_model(self.query_projection(Q))
            snapshots = {name: value.detach().unsqueeze(0).expand(
                batch_size, *value.shape).clone() for name, value in initial.items()}
            return MemoryOutput(tokens, snapshots, None, {})

        outer_grad_enabled = torch.is_grad_enabled()
        meta_learning = self.training and outer_grad_enabled
        outputs, targets, states, diagnostics = [], [], [], []
        # Inference still needs the inner gradient even in torch.no_grad().
        with torch.enable_grad():
            keys = self.key_projection(X)
            queries = self.query_projection(Q)
            semantic = self.inner_targets(keys, X, T)
            for index in range(batch_size):
                params = initial if meta_learning else {
                    name: value.detach().requires_grad_(True) for name, value in initial.items()}
                before = self.inner_objective(functional_call(self.fast_model, params, (keys[index],)),
                                              keys[index], X[index], T[index], semantic[index])
                grads = torch.autograd.grad(before, tuple(params.values()), create_graph=meta_learning)
                adapted, step_diagnostics = self.select_update(
                    params, grads, before, keys[index], X[index], T[index], semantic[index], meta_learning)
                output = functional_call(self.fast_model, adapted, (queries[index],))
                with torch.no_grad():
                    after = self.inner_objective(functional_call(self.fast_model, adapted, (keys[index],)),
                                                 keys[index], X[index], T[index], semantic[index])
                    grad_norm = torch.sqrt(sum(grad.square().sum() for grad in grads))
                    update_norm = torch.sqrt(sum((adapted[name] - value).square().sum()
                                                 for name, value in params.items()))
                    finite = torch.stack([torch.isfinite(tensor).all() for tensor in
                                          [before, after, grad_norm, update_norm, semantic[index], output,
                                           *grads, *adapted.values()]]).all()
                outputs.append(output)
                targets.append(semantic[index].detach())
                states.append({name: value.detach().clone() for name, value in adapted.items()})
                diagnostics.append({"inner_loss_before": before.detach(), "inner_loss_after": after,
                                    "inner_gradient_norm": grad_norm, "fast_update_norm": update_norm,
                                    "all_finite": finite,
                                    **{name: value.detach() for name, value in step_diagnostics.items()}})
            tokens = torch.stack(outputs)
        if not outer_grad_enabled:
            tokens = tokens.detach()
        return MemoryOutput(tokens,
                            {name: torch.stack([state[name] for state in states]) for name in initial},
                            torch.stack(targets),
                            {name: torch.stack([item[name] for item in diagnostics])
                             for name in diagnostics[0]})
