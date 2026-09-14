"""Clean, GT-anchored semantic composition audit; standard library only.

Consumes selected detections in memory. No detector, file reader or query alignment.
See research_log/t014_semantic/PREREGISTRATION.md for the frozen contract.
"""
import math
from statistics import mean, median

VOCABULARIES = ('V0', 'Vhard30', 'Vrand30')
DEGRADATION = {'semantic_failure_given_localized', 'distractor_takeover_rate',
               'localization_loss_rate'}


def preflight(data):
    """Validate the analysis input schema, including clean-only condition."""
    if data['condition'] != 'clean':
        raise ValueError('Only condition=clean is accepted')
    canonical = set(data['canonical_labels'])
    distractors = data['distractor_labels']
    allowed = {'V0': canonical}
    for vocab in VOCABULARIES[1:]:
        added = set(distractors[vocab])
        if canonical & added:
            raise ValueError('Canonical and distractor labels must be disjoint')
        allowed[vocab] = canonical | added
    ids = set()
    for image in data['images']:
        if image['image_id'] in ids:
            raise ValueError('Duplicate image_id')
        ids.add(image['image_id'])
        for gt in image['gt']:
            _box(gt['box'])
            if gt['label'] not in canonical or gt['iscrowd'] not in (False, True, 0, 1):
                raise ValueError('GT requires canonical label and boolean iscrowd')
        if set(image['detections']) != set(VOCABULARIES):
            raise ValueError('Each image requires exactly the three vocabularies')
        for vocab in VOCABULARIES:
            for detection in image['detections'][vocab]:
                _box(detection['box'])
                if detection['label'] not in allowed[vocab]:
                    raise ValueError('Detection label is outside its vocabulary')
                if not math.isfinite(detection['score']):
                    raise ValueError('Detection score must be finite')
    return data


def _box(box):
    if len(box) != 4 or not all(math.isfinite(x) for x in box):
        raise ValueError('Box must be four finite xyxy coordinates')
    if box[2] <= box[0] or box[3] <= box[1]:
        raise ValueError('Box must have positive area')


def iou(a, b):
    intersection = max(0, min(a[2], b[2]) - max(a[0], b[0])) * max(0, min(a[3], b[3]) - max(a[1], b[1]))
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - intersection
    return intersection / union


def observe(gt, detections, distractors):
    candidates = [(iou(gt['box'], d['box']), d['score'], -index, d)
                  for index, d in enumerate(detections)]
    candidates = [row for row in candidates if row[0] >= 0.5]
    if not candidates:
        return None
    overlap, score, neg_index, d = max(candidates, key=lambda row: row[:3])
    return {'selected_order': -neg_index, 'gt_iou': overlap, 'score': score,
            'box': list(d['box']), 'label': d['label'],
            'correct': d['label'] == gt['label'], 'distractor': d['label'] in distractors}


def _rate(numerator, support):
    return {'value': numerator / support if support else None,
            'numerator': numerator, 'support': support}


def _summary(values, statistic=mean):
    return {'value': statistic(values) if values else None, 'support': len(values)}


def analyze(data):
    preflight(data)
    observations = []
    for image in data['images']:
        for index, gt in enumerate(image['gt']):
            if gt['iscrowd']:
                continue
            observations.append({'image_id': image['image_id'], 'gt_index': index,
                                 'vocabularies': {
                                     v: observe(gt, image['detections'][v], set(data['distractor_labels'].get(v, [])))
                                     for v in VOCABULARIES}})
    results = {}
    for vocab in VOCABULARIES[1:]:
        pairs = [(r['vocabularies']['V0'], r['vocabularies'][vocab]) for r in observations]
        base_correct = [(a, b) for a, b in pairs if a is not None and a['correct']]
        localized = [(a, b) for a, b in base_correct if b is not None]
        both = [(a, b) for a, b in pairs if a is not None and b is not None]
        overlaps = [iou(a['box'], b['box']) for a, b in both]
        results[vocab] = {
            'V0_correct_survival': _rate(sum(b is not None and b['correct'] for a, b in base_correct), len(base_correct)),
            'semantic_failure_given_localized': _rate(sum(not b['correct'] for a, b in localized), len(localized)),
            'distractor_takeover_rate': _rate(sum(b['distractor'] for a, b in localized), len(localized)),
            'localization_loss_rate': _rate(len(base_correct) - len(localized), len(base_correct)),
            'box_stability_mean': _summary(overlaps),
            'box_stability_median': _summary(overlaps, median),
            'score_delta': _summary([b['score'] - a['score'] for a, b in both]),
        }
    contrasts = {}
    for metric in results['Vhard30']:
        hard, random = results['Vhard30'][metric], results['Vrand30'][metric]
        sign = 1 if metric in DEGRADATION else -1
        contrasts[metric] = {
            'value': sign * (hard['value'] - random['value']) if hard['value'] is not None and random['value'] is not None else None,
            'orientation': 'hard-minus-random' if sign == 1 else 'random-minus-hard',
            'hard_support': hard['support'], 'random_support': random['support'],
        }
    return {'evidence_status': 'EXPLORATORY / POST-HOC DEVELOPMENT',
            'noncrowd_gt_count': len(observations), 'observations': observations,
            'metrics': results, 'hard_vs_random_degradation': contrasts}


def dataset_deltas(clean_metrics):
    """Arithmetic on precomputed frozen evaluator summaries; not an evaluator."""
    deltas = {v: {m: clean_metrics['V0'][m] - clean_metrics[v][m]
                  for m in ('AP', 'AP50', 'AR', 'AR50')} for v in VOCABULARIES[1:]}
    return {'deltas': deltas, 'HardMinusRandom_AP50': deltas['Vhard30']['AP50'] - deltas['Vrand30']['AP50']}
