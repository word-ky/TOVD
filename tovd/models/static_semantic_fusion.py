"""T012 feed-forward vocabulary evidence and fixed product of experts."""

import torch

from .query_local_residual import local_teacher


@torch.inference_mode()
def static_evidence(model, X, T, Q, *, teacher_tau=.2, tau_q=.2):
    keys = model.memory.key_projection(X)
    queries = model.memory.query_projection(Q)
    tokens = model.memory.fast_model(queries)
    log_p0 = model.logits(tokens, T).log_softmax(-1)
    # Use the exact existing softmax path for the unchanged W0 probabilities.
    p0 = model.logits(tokens, T).softmax(-1)
    teacher, attention, token_teacher = local_teacher(keys, queries, T, teacher_tau, tau_q)
    uniform_attention = torch.full_like(attention, 1 / keys.shape[-2])
    return dict(tokens=tokens, p0=p0, log_p0=log_p0, teacher=teacher,
                uniform_teacher=uniform_attention @ token_teacher,
                attention=attention, token_teacher=token_teacher)


@torch.inference_mode()
def product_of_experts(p0, teacher, exponent, epsilon=1e-12):
    log_probabilities = ((p0+epsilon).log()+exponent*(teacher+epsilon).log()).log_softmax(-1)
    return dict(log_probabilities=log_probabilities, probabilities=log_probabilities.exp())
