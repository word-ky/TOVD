"""Frozen probabilities/tokens only; labels enter offline_outcome separately."""

import math
from statistics import mean

EPS = 1e-12
PRE = ('query_entropy', 'query_max_probability', 'query_probability_gap')
POST = ('query_js', 'representation_displacement', 'prediction_changed',
        'delta_max_probability', 'delta_entropy', 'delta_probability_gap')
FEATURES = PRE + POST
FEATURE_METADATA = {f: {'is_label_free_feature': True,
                        'availability': 'pre_update' if f in PRE else 'post_candidate_rollback'}
                    for f in FEATURES}


def entropy(p):
    return -sum(v * math.log(max(v, EPS)) for v in p)


def top(p):
    return max(range(len(p)), key=p.__getitem__)


def gap(p):
    ranked = sorted(p, reverse=True)
    return ranked[0] - ranked[1]


def query_features(p0, p1, z0, z1):
    midpoint = [(a + b) / 2 for a, b in zip(p0, p1)]
    js = .5 * sum(v * (math.log(max(v, EPS)) - math.log(max(m, EPS)))
                  for p in (p0, p1) for v, m in zip(p, midpoint))
    return {'query_entropy': entropy(p0), 'query_max_probability': max(p0),
            'query_probability_gap': gap(p0), 'query_js': js,
            'representation_displacement': math.sqrt(sum((b-a)**2 for a, b in zip(z0, z1))) / (math.sqrt(sum(a*a for a in z0)) + EPS),
            'prediction_changed': int(top(p0) != top(p1)),
            'delta_max_probability': max(p1)-max(p0),
            'delta_entropy': entropy(p1)-entropy(p0),
            'delta_probability_gap': gap(p1)-gap(p0)}


def offline_outcome(p0, p1, label):
    n0, n1 = -math.log(max(p0[label], EPS)), -math.log(max(p1[label], EPS))
    c0, c1 = int(top(p0) == label), int(top(p1) == label)
    d = n1-n0
    choose_c2 = n1 < n0
    transition = ('correct' if c0 else 'wrong') + '->' + ('correct' if c1 else 'wrong')
    return {'before_nll': n0, 'after_nll': n1, 'delta_nll': d,
            'before_accuracy': c0, 'after_accuracy': c1, 'delta_accuracy': c1-c0,
            'harm': d > 0, 'harm_gt_005': d > .05,
            'transition': transition, 'nll_direction': 'worsened' if d > 0 else 'improved' if d < 0 else 'equal',
            'oracle_uses_C2': choose_c2, 'oracle_nll': min(n0, n1),
            'oracle_accuracy': c1 if choose_c2 else c0}


METRICS = ('before_nll', 'after_nll', 'oracle_nll', 'before_accuracy', 'after_accuracy', 'oracle_accuracy')


def aggregate(rows):
    return {'count': len(rows), **{k: mean(r[k] for r in rows) for k in METRICS}}


def episode_rows(record):
    o = record['outputs']
    vectors = list(zip(o['W0_probabilities'], o['C2_probabilities'], o['W0_tokens'], o['C2_tokens']))
    features = [query_features(*v) for v in vectors]
    # Labels and historical correctness are not arguments of the feature function.
    meta = {k: record[k] for k in ('state_id', 'seed', 'branch', 'step', 'regime', 'episode_seed')}
    rows = [{**meta, 'query_index': j, **f, **offline_outcome(v[0], v[1], record['labels'][j])}
            for j, (f, v) in enumerate(zip(features, vectors))]
    assert features == [query_features(*v) for v in vectors]
    return rows
