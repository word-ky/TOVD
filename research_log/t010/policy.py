"""Single-scalar hard query selection; base-label calibration is separate."""

import math

from research_log.t008.statistics import quantile
from research_log.t009.query_analysis import entropy


def number(tau):
    return float(tau)


def encode(tau):
    return '+inf' if tau == math.inf else '-inf' if tau == -math.inf else tau


def delta_entropy(p0, p1):
    return [entropy(b)-entropy(a) for a, b in zip(p0, p1)]


def select(p0, p1, z0, z1, tau):
    changes = delta_entropy(p0, p1)
    keep = [d <= number(tau) for d in changes]
    return {'delta_entropy': changes, 'keep_C2': keep,
            'probabilities': [b if k else a for a, b, k in zip(p0, p1, keep)],
            'tokens': [b if k else a for a, b, k in zip(z0, z1, keep)]}


def calibrate(rows, held_seed, quantiles, tie_tolerance=1e-12):
    training = [r for r in rows if r['phase'] == 'calibration' and r['seed'] != held_seed]
    dh = [r['delta_entropy'] for r in training]
    candidates = sorted({-math.inf, math.inf, *(quantile(dh, q) for q in quantiles)})
    losses = [math.fsum(r['after_nll'] if r['delta_entropy'] <= t else r['before_nll'] for r in training)/len(training) for t in candidates]
    best = min(losses)
    chosen = next(i for i, loss in enumerate(losses) if loss <= best+tie_tolerance)
    return {'held_seed': held_seed, 'tau': encode(candidates[chosen]), 'minimum_calibration_nll': best,
            'selected_calibration_nll': losses[chosen], 'query_count': len(training),
            'calibration_seeds': sorted({r['seed'] for r in training}),
            'state_ids': sorted({r['state_id'] for r in training}),
            'episode_ids': sorted({r['episode_seed'] for r in training}),
            'candidates': [{'tau': encode(t), 'nll': loss} for t, loss in zip(candidates, losses)]}
