"""CF1: canonical-only final selection from unchanged in-memory saved arrays."""
import torch


def canonical_topk(boxes, class_scores):
    scores, flat = torch.topk(torch.from_numpy(class_scores[:, :80]).flatten(), 300)
    query_ids = (flat // 80).numpy()
    return {
        'top_query_ids': query_ids,
        'top_labels': (flat % 80).numpy(),
        'top_scores': scores.numpy(),
        'boxes': boxes[query_ids],
    }
