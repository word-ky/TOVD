"""Standalone tensor reference only; not integrated into Grounding-DINO."""
import torch


def select_references(enc_class_logits, enc_coord_x, num_queries=900, override_indices=None):
    """Replace only ordered proposal indices; gather exclusively Vx coordinates.

    Inputs: logits[B,S,T], unsigmoid coordinates[B,S,4], optional int64 I0[B,K].
    Returns ordered indices and detached initial references, as frozen lines301–307.
    """
    batch, locations = enc_class_logits.shape[:2]
    if type(num_queries) is not int or not 1 <= num_queries <= locations:
        raise ValueError('requested count must be an integer in [1, encoder_locations]')
    topk_logits = enc_class_logits.max(-1)[0]
    indices = torch.topk(topk_logits, num_queries, dim=1)[1]
    if override_indices is not None:
        if override_indices.dtype != torch.int64:
            raise ValueError('override indices must be int64')
        if override_indices.shape != (batch, num_queries):
            raise ValueError('override shape must match batch and requested count')
        if torch.any((override_indices < 0) | (override_indices >= locations)):
            raise ValueError('override index outside encoder locations')
        if any(torch.unique(row).numel() != num_queries for row in override_indices):
            raise ValueError('override indices must be unique within each batch row')
        indices = override_indices
    references = torch.gather(enc_coord_x, 1, indices.unsqueeze(-1).repeat(1, 1, 4))
    return indices, references.detach()
