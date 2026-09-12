"""Native30 cached COCO evaluation and paired dataset-level image bootstrap."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path

import numpy as np
from scripts.t013_coco import evaluate_dataset, image_cache, metrics, accumulate_image_copies, paired_bootstrap_indices
from scripts.t013_diagnostics import canonical_predictions, image_diagnostics, canonical_fp_from_cache

CONDITIONS = ['clean', 'gaussian_noise', 'motion_blur', 'fog', 'jpeg_compression']
VOCABS = ['V0', 'Vhard30', 'Vrand30']
METRICS = ['AP', 'AP50', 'AR', 'AR50', 'canonical_fp_per_image', 'distractor_fp_per_image',
           'canonical_recall', 'localization_recall']


def divide(a, b):
    return np.divide(a, b, out=np.full(np.broadcast_shapes(np.shape(a), np.shape(b)), np.nan), where=np.asarray(b) != 0)


def diagnostic_means(rows, draws):
    # Columns: noncrowd GT count, correctly covered, localized, distractor FP, canonical FP.
    data = rows[draws]
    return [float(data[:, 4].mean()), float(data[:, 3].mean()),
            float(divide(data[:, 1].sum() * 100., data[:, 0].sum())),
            float(divide(data[:, 2].sum() * 100., data[:, 0].sum()))]


def interaction(values):
    # Last two dimensions are [five visual conditions, three vocabularies].
    drop = values[..., :1, :] - values[..., 1:, :]
    amp = drop - drop[..., :1]
    return drop, amp, amp[..., 1] - amp[..., 2]


def interval(samples):
    samples = np.asarray(samples)
    if not np.isfinite(samples).all():
        return None
    return np.percentile(samples, [2.5, 97.5], axis=0, method='linear').tolist()


def assess_gates(point, bootstrap, mechanism_point, mechanism_bootstrap, protocol_valid):
    drop, amplification, hard_minus_random = interaction(point[:, :, 1])
    bdrop, bamp, bdiff = interaction(bootstrap[:, :, :, 1])
    lower = np.percentile(bamp[:, :, 1], 2.5, axis=0, method='linear')
    material = (amplification[:, 1] >= 1.) & (lower > 0)
    gate1 = bool(material.sum() >= 2)
    gate2 = bool(amplification[:, 1].mean() >= .75 and hard_minus_random.mean() >= .50
                 and (hard_minus_random > 0).sum() >= 2)
    mechanism = {}
    for key, values in mechanism_point.items():
        samples = mechanism_bootstrap[key]
        avg = float(np.mean(values))
        ci = interval(np.mean(samples, axis=1))
        # Gate3 remains a Lead interpretation; expose a conservative support flag,
        # without using it to rescue Gates1/2 or automatically accept a research task.
        mechanism[key] = {'per_corruption': values.tolist(), 'mean': avg,
                          'mean_ci95': ci, 'positive_corruptions': int(np.sum(values > 0)),
                          'statistical_support': bool(ci is not None and ci[0] > 0 and np.sum(values > 0) >= 2)}
    return {'D_AP50': drop.tolist(), 'A_AP50': amplification.tolist(),
            'D_AP50_ci95': interval(bdrop), 'A_AP50_ci95': interval(bamp),
            'hard_minus_random': hard_minus_random.tolist(), 'hard_minus_random_ci95': interval(bdiff),
            'mean_A_hard': float(amplification[:, 1].mean()),
            'mean_A_hard_ci95': interval(bamp[:, :, 1].mean(axis=1)),
            'mean_hard_minus_random': float(hard_minus_random.mean()),
            'mean_hard_minus_random_ci95': interval(bdiff.mean(axis=1)),
            'gate1': gate1, 'gate1_corruptions': material.tolist(), 'gate2': gate2,
            'gate3_diagnostics': mechanism,
            'gate3_statistical_support': any(item['statistical_support'] for item in mechanism.values()),
            'gate4_recorded_checks': bool(protocol_valid), 'research_acceptance': 'Research Lead decision required'}


def mechanism_values(values, margin_contrast):
    # Positive values support semantic competition beyond unrelated vocabulary.
    fp = values[..., 1:, 1, 5] - values[..., 0:1, 1, 5] - (
        values[..., 1:, 2, 5] - values[..., 0:1, 2, 5])
    recall_gap = values[..., :, :, 7] - values[..., :, :, 6]
    gap_increase = recall_gap[..., 1:, :] - recall_gap[..., :1, :]
    return {'distractor_fp_excess_increase': fp,
            'classification_beyond_localization_excess_drop': gap_increase[..., 1] - gap_increase[..., 2],
            'matched_localization_margin_excess_shrinkage': margin_contrast}


def margin_rows(diagnostics, ids):
    # Identical GT IDs; compare clean/corrupt hard/random only where the raw best-IoU
    # query localizes that GT in ALL FOUR cells. This avoids changing margin support.
    values = np.zeros((4, len(ids), 2))
    for c in range(1, 5):
        for i in range(len(ids)):
            rows = [diagnostics[(0, 1)][i], diagnostics[(c, 1)][i],
                    diagnostics[(0, 2)][i], diagnostics[(c, 2)][i]]
            assert all(np.array_equal(rows[0]['gt_ids'], row['gt_ids']) for row in rows[1:])
            margins = np.stack([row['margin'] for row in rows])
            keep = np.isfinite(margins).all(axis=0)
            contrast = margins[0, keep] - margins[1, keep] - margins[2, keep] + margins[3, keep]
            values[c - 1, i] = [contrast.sum(), keep.sum()]
    return values


def mean_margin(rows, draws):
    sums = rows[:, draws].sum(axis=1)
    return divide(sums[:, 0], sums[:, 1])


def analyze(dataset, ids, raw_root, output, replicates=1000, seed=20260913, protocol_valid=False, smoke=False):
    output.mkdir(parents=True, exist_ok=True)
    categories = sorted(row['id'] for row in dataset['categories'])
    gt = defaultdict(list)
    for row in dataset['annotations']:
        gt[row['image_id']].append(row)
    caches, diagnostics, numeric = {}, {}, {}
    point = np.zeros((5, 3, len(METRICS)))
    for c, condition in enumerate(CONDITIONS):
        for v, vocabulary in enumerate(VOCABS):
            predictions, diag = [], []
            for image_id in ids:
                with np.load(raw_root / condition / vocabulary / f'{image_id:012d}.npz') as raw:
                    predictions.extend(canonical_predictions(raw, image_id, categories))
                    diag.append(image_diagnostics(raw, gt[image_id], categories))
            evaluator = evaluate_dataset(dataset, predictions, ids)
            cache = image_cache(evaluator)
            fp = canonical_fp_from_cache(cache)
            rows = np.array([[d['gt_count'], d['canonical_covered'], d['localized'], d['distractor_fp'], int(f)]
                             for d, f in zip(diag, fp)], dtype=np.float64)
            canonical = metrics(evaluator.eval)
            point[c, v] = [canonical[key] for key in METRICS[:4]] + diagnostic_means(rows, np.arange(len(ids)))
            caches[c, v], diagnostics[c, v], numeric[c, v] = cache, diag, rows
            print(f'evaluated cached cell {condition}/{vocabulary}', flush=True)
    margins = margin_rows(diagnostics, ids)
    draws = paired_bootstrap_indices(len(ids), seed=seed, replicates=replicates)
    np.save(output / 'paired_image_draws.npy', draws)
    samples = np.zeros((replicates, 5, 3, len(METRICS)))
    margin_samples = np.zeros((replicates, 4))
    for b, indices in enumerate(draws):
        for c in range(5):
            for v in range(3):
                metric = metrics(accumulate_image_copies(caches[c, v], indices))
                samples[b, c, v] = [metric[key] for key in METRICS[:4]] + diagnostic_means(numeric[c, v], indices)
        margin_samples[b] = mean_margin(margins, indices)
        if (b + 1) % 25 == 0 or b + 1 == replicates:
            np.savez_compressed(output / 'bootstrap_samples.npz', metrics=samples[:b+1], margins=margin_samples[:b+1])
            print(f'paired dataset bootstrap {b + 1}/{replicates}', flush=True)
    mechanism = mechanism_values(point, mean_margin(margins, np.arange(len(ids))))
    bmechanism = mechanism_values(samples, margin_samples)
    assessment = assess_gates(point, samples, mechanism, bmechanism, protocol_valid)
    result = {'kind': 'engineering_smoke_not_scientific' if smoke else 'T013-NATIVE30',
              'image_count': len(ids), 'conditions': CONDITIONS, 'vocabularies': VOCABS,
              'metric_order': METRICS, 'point_metrics': point.tolist(),
              'metric_ci95': interval(samples), 'replicates': replicates, 'seed': seed,
              'margin_common_localized_gt_counts': margins[:, :, 1].sum(axis=1).tolist(),
              'assessment': assessment}
    (output / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    # Per-image primitive diagnostics remain available for independent review.
    np.savez_compressed(output / 'diagnostics_per_image.npz', margin_contrast_sum_count=margins,
                        **{f'c{c}_v{v}': rows for (c, v), rows in numeric.items()})
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--annotations', type=Path, required=True)
    p.add_argument('--run', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--smoke-only', action='store_true')
    args = p.parse_args()
    receipt = json.loads((args.run / 'run_receipt.json').read_text())
    assert receipt['completed'] and receipt['weights_unchanged']
    pixels = defaultdict(set)
    counts = defaultdict(int)
    for row in receipt['records']:
        key = (row['image_id'], row['condition'])
        pixels[key].add(row['pixel_sha256'])
        counts[key] += 1
    assert len(pixels) == len(receipt['image_ids']) * 5
    assert all(len(value) == 1 and counts[key] == 3 for key, value in pixels.items())
    protocol_valid = bool(receipt['freeze_commit']) and receipt['code_vocab_selection_images_verified']
    if not args.smoke_only:
        freeze = json.loads(Path('research_log/t013/native30_freeze.json').read_text())
        assert hashlib.sha256(args.annotations.read_bytes()).hexdigest() == freeze['annotations_sha256']
    dataset = json.loads(args.annotations.read_text())
    result = analyze(dataset, receipt['image_ids'], args.run / 'raw', args.output,
                     replicates=10 if args.smoke_only else 1000,
                     protocol_valid=protocol_valid and not args.smoke_only,
                     smoke=args.smoke_only)
    print(json.dumps({'kind': result['kind'], 'analysis_completed': True}))


if __name__ == '__main__':
    main()
