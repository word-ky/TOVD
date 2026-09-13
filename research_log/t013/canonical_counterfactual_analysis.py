"""CF2 descriptive paired arithmetic and frozen COCO evaluation reuse."""
import numpy as np

from canonical_topk_counterfactual import canonical_topk


def descriptors(original_ap50, cf_ap50):
    """Inputs end in [5 conditions, 3 vocabularies]; preceding axes are paired."""
    d = cf_ap50[..., :1, :] - cf_ap50[..., 1:, :]
    a = d - d[..., :1]
    original_d = original_ap50[..., :1, :] - original_ap50[..., 1:, :]
    original_a = original_d - original_d[..., :1]
    removed = original_a - a
    h = a[..., 1] - a[..., 2]
    removed_h = (original_a[..., 1] - original_a[..., 2]) - h
    return {'D_cf': d, 'A_cf': a, 'L_topk': removed, 'H_cf': h,
            'L_topk_hard_minus_random': removed_h,
            'mean_A_cf_hard': a[..., 1].mean(axis=-1),
            'mean_L_topk_hard': removed[..., 1].mean(axis=-1),
            'mean_H_cf': h.mean(axis=-1),
            'mean_L_topk_hard_minus_random': removed_h.mean(axis=-1)}


def paired_summary(original_point, cf_point, original_samples, cf_samples):
    point = descriptors(original_point, cf_point)
    samples = descriptors(original_samples, cf_samples)
    # Match frozen interval convention, including undefined/nonfinite samples.
    intervals = {name: (np.percentile(value, [2.5, 97.5], axis=0, method='linear').tolist()
                        if np.isfinite(value).all() else None) for name, value in samples.items()}
    return {'point': {name: value.tolist() for name, value in point.items()},
            'ci95': intervals}, samples


def evaluate_smoke(dataset, ids, raw_root, draws):
    """Caller binds frozen scripts and completed smoke; never invokes a detector."""
    from scripts.t013_coco import evaluate_dataset, image_cache, metrics, accumulate_image_copies
    from scripts.t013_diagnostics import canonical_predictions
    from scripts.t013_analysis import CONDITIONS, VOCABS

    categories = sorted(row['id'] for row in dataset['categories'])
    metric_names = ['AP', 'AP50', 'AR', 'AR50']
    point = np.zeros((5, 3, 4))
    samples = np.zeros((len(draws), 5, 3, 4))
    for c, condition in enumerate(CONDITIONS):
        for v, vocabulary in enumerate(VOCABS):
            predictions = []
            for image_id in ids:
                with np.load(raw_root / condition / vocabulary / f'{image_id:012d}.npz', allow_pickle=False) as raw:
                    boxes, scores = raw['boxes'], raw['class_scores']
                    selected = canonical_topk(boxes, scores)
                    # Frozen mapper indexes the original 900 boxes by query ID.
                    selected['boxes'] = boxes
                    predictions.extend(canonical_predictions(selected, image_id, categories))
            evaluator = evaluate_dataset(dataset, predictions, ids)
            values = metrics(evaluator.eval)
            point[c, v] = [values[name] for name in metric_names]
            cache = image_cache(evaluator)
            for b, indices in enumerate(draws):
                values = metrics(accumulate_image_copies(cache, indices))
                samples[b, c, v] = [values[name] for name in metric_names]
    return point, samples
