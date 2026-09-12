"""T013-STAT1: independent synthetic arithmetic audit; never reads run artifacts."""
import ast
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).parent
FREEZE = '6fec32243985ccc808123d851abf5f3dea10af99'
PATHS = ['scripts/t013_analysis.py', 'scripts/t013_coco.py',
         'scripts/t013_diagnostics.py', 'research_log/t013/PLAN.md']


def reference_interaction(x):
    x = np.asarray(x)
    d, a = np.empty(x.shape[:-2] + (4, 3)), np.empty(x.shape[:-2] + (4, 3))
    for prefix in np.ndindex(x.shape[:-2]):
        for c in range(4):
            for v in range(3):
                d[prefix + (c, v)] = x[prefix + (0, v)] - x[prefix + (c + 1, v)]
            for v in range(3):
                a[prefix + (c, v)] = d[prefix + (c, v)] - d[prefix + (c, 0)]
    return d, a, a[..., 1] - a[..., 2]


def reference_interval(x):
    x = np.asarray(x, dtype=float)
    if not np.isfinite(x).all():
        return None
    out = np.empty((2,) + x.shape[1:])
    for index in np.ndindex(x.shape[1:]):
        ordered = sorted(x[(slice(None),) + index].tolist())
        for k, p in enumerate((.025, .975)):
            position = (len(ordered) - 1) * p
            left, right = math.floor(position), math.ceil(position)
            out[(k,) + index] = ordered[left] + (position - left) * (ordered[right] - ordered[left])
    return out


def reference_gates(point, draws):
    _, a, diff = reference_interaction(point)
    _, ba, _ = reference_interaction(draws)
    lower = reference_interval(ba[:, :, 1])[0]
    qualifies = [a[c, 1] >= 1 and lower[c] > 0 for c in range(4)]
    gate2 = (sum(a[:, 1]) / 4 >= .75 and sum(diff) / 4 >= .50
             and sum(value > 0 for value in diff) >= 2)
    return bool(sum(qualifies) >= 2), bool(gate2), qualifies


def scores(hard, difference):
    # Clean AP50=64; base corruption drop=8. Binary-exact boundary inputs.
    x = np.full((5, 3), 64.)
    for c, (h, delta) in enumerate(zip(hard, difference), 1):
        x[c] = [56., 56. - h, 56. - h + delta]
    return x


def metric_tensor(x):
    result = np.zeros(np.shape(x) + (8,))
    result[..., 1] = x
    return result


def run():
    receipt = {'task': 'T013-STAT1', 'kind': 'synthetic_only_analysis_validation',
               'freeze_commit': FREEZE, 'started_utc': datetime.now(timezone.utc).isoformat(),
               'environment': {'python': sys.version, 'executable': sys.executable, 'numpy': np.__version__},
               'source_hashes': {}, 'fixtures': [], 'status': 'RUNNING',
               'primary_artifacts_opened': False, 'frozen_code_modified': False}
    current = None
    max_error = 0.

    def compare(actual, expected):
        nonlocal max_error
        if expected is None:
            assert actual is None, (actual, expected)
            return
        a, b = np.asarray(actual), np.asarray(expected)
        assert a.shape == b.shape, (a.shape, b.shape)
        if a.dtype.kind == 'b' or b.dtype.kind == 'b':
            assert np.array_equal(a, b), (a.tolist(), b.tolist())
        else:
            assert np.array_equal(np.isnan(a), np.isnan(b)), (a.tolist(), b.tolist())
            assert np.array_equal(np.isinf(a), np.isinf(b))
            finite = np.isfinite(b)
            error = float(np.max(np.abs(a[finite] - b[finite]), initial=0))
            max_error = max(max_error, error)
            assert error <= 1e-12, (error, a.tolist(), b.tolist())

    def fixture(name, detail):
        receipt['fixtures'].append({'name': name, 'status': 'PASS',
                                    'maximum_error_through_fixture': max_error, **detail})

    try:
        sources = {}
        current = 'frozen_source_binding'
        for path in PATHS:
            frozen = subprocess.check_output(['git', 'show', f'{FREEZE}:{path}'], cwd=ROOT)
            head = subprocess.check_output(['git', 'show', f'HEAD:{path}'], cwd=ROOT)
            assert frozen == head
            assert (ROOT / path).read_bytes().replace(b'\r\n', b'\n') == frozen
            sources[path] = frozen.decode()
            receipt['source_hashes'][path] = hashlib.sha256(frozen).hexdigest()
        # Execute verbatim frozen function ASTs; imports/CLI are deliberately not executed.
        namespace = {'np': np}
        names = ['divide', 'interaction', 'interval', 'assess_gates', 'mechanism_values',
                 'margin_rows', 'mean_margin', 'diagnostic_means', 'paired_bootstrap_indices']
        for path in PATHS[:2]:
            tree = ast.parse(sources[path])
            definitions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
            exec(compile(ast.Module(body=definitions, type_ignores=[]), f'{FREEZE}:{path}', 'exec'), namespace)
        f = namespace
        fixture(current, {'loaded_functions': names, 'method': 'unchanged frozen function ASTs; numpy-only globals'})

        current = 'positive_and_complementary_negative_sign'
        signs = []
        for hard in ([3., 2., 1., .5], [-3., -2., -1., -.5]):
            x = scores(hard, np.asarray(hard) / 2)
            actual, expected = f['interaction'](x), reference_interaction(x)
            for a, b in zip(actual, expected):
                compare(a, b)
            compare(actual[1][:, 1], hard)
            signs.append(actual[1][:, 1].tolist())
        fixture(current, {'A_hard': signs, 'reversed_subtraction_rejected': True})

        current = 'linear_percentile_and_undefined_samples'
        samples = np.array([[7., -2.], [1., 12.], [4., 2.], [20., 1.], [-3., 9.]])
        compare(f['interval'](samples), reference_interval(samples))
        compare(f['interval']([4.]), [4., 4.])
        for values in ([0., np.nan, 1.], [0., np.inf], [np.nan]):
            compare(f['interval'](values), None)
        fixture(current, {'samples': samples.tolist(), 'ci95': f['interval'](samples),
                          'undefined_or_infinite_sample': 'whole interval unavailable; no dropping/imputation'})

        current = 'gate1_two_corruptions_and_zero_lower_bound'
        x = scores([1., 1., 0., 0.], [1., 1., 0., 0.])
        bs = np.repeat(x[None], 5, axis=0)
        passed = f['assess_gates'](metric_tensor(x), metric_tensor(bs), {}, {}, True)
        compare(passed['gate1'], True)
        compare(passed['gate1_corruptions'], [True, True, False, False])
        bs[:, 2, 1] = bs[:, 2, 0]  # Second qualifying corruption now has CI lower exactly zero.
        failed = f['assess_gates'](metric_tensor(x), metric_tensor(bs), {}, {}, True)
        compare(failed['gate1'], False)
        compare(failed['gate1_corruptions'], [True, False, False, False])
        for b in (np.repeat(x[None], 5, axis=0), bs):
            got = f['assess_gates'](metric_tensor(x), metric_tensor(b), {}, {}, True)
            ref = reference_gates(x, b)
            compare(got['gate1'], ref[0]); compare(got['gate2'], ref[1]); compare(got['gate1_corruptions'], ref[2])
        fixture(current, {'A_hard': [1, 1, 0, 0], 'positive_lower_pass': True,
                          'zero_lower_gate1': failed['gate1'], 'zero_lower_qualifies': failed['gate1_corruptions']})

        current = 'gate2_exact_and_adversarial_boundaries'
        eps = 2. ** -30
        cases = [('exact', [1.5, 1.5, 0, 0], [1, 1, 0, 0], True),
                 ('hard_mean_below', [1.5-eps, 1.5, 0, 0], [1, 1, 0, 0], False),
                 ('contrast_mean_below', [1.5, 1.5, 0, 0], [1-eps, 1, 0, 0], False),
                 ('one_positive', [1.5, 1.5, 0, 0], [2, 0, 0, 0], False)]
        evidence = []
        for name, hard, delta, expected in cases:
            x = scores(hard, delta); bs = np.repeat(x[None], 5, axis=0)
            got = f['assess_gates'](metric_tensor(x), metric_tensor(bs), {}, {}, True)
            compare(got['gate2'], expected); compare(got['gate2'], reference_gates(x, bs)[1])
            evidence.append({'name': name, 'mean_A_hard': got['mean_A_hard'],
                             'mean_hard_minus_random': got['mean_hard_minus_random'],
                             'positive_contrasts': sum(v > 0 for v in delta), 'gate2': got['gate2']})
        fixture(current, {'epsilon': eps, 'cases': evidence})

        current = 'shared_draws_replicate_contrast_before_ci'
        draws = np.array([[0, 0, 1, 3], [3, 2, 2, 1], [1, 1, 0, 2], [2, 3, 3, 3], [0, 2, 1, 2]])
        values = np.empty((4, 5, 3))
        for i in range(4):
            values[i] = scores([i+1, i/2, 2-i/2, .25*i], [2*i, .25, .5, 1]) + 4*i
        paired = np.array([np.mean(values[row], axis=0) for row in draws])
        frozen = f['interaction'](paired); ref = reference_interaction(paired)
        for a, b in zip(frozen, ref):
            compare(a, b); compare(f['interval'](a), reference_interval(b))
        unpaired = paired.copy()
        unpaired[:, 1:, 1] = np.array([values[(row+1) % 4, 1:, 1].mean(axis=0) for row in draws])
        wrong_unpaired = reference_interval(reference_interaction(unpaired)[2])
        correct = reference_interval(ref[2])
        marginal = reference_interval(ref[1][:, :, 1]) - reference_interval(ref[1][:, :, 2])
        assert not np.allclose(wrong_unpaired, correct, atol=1e-12, rtol=0)
        assert not np.allclose(marginal, correct, atol=1e-12, rtol=0)
        compare(f['paired_bootstrap_indices'](4, seed=20260913, replicates=5),
                np.random.default_rng(20260913).integers(0, 4, (5, 4)))
        # Frozen analyze loop wiring is inspected without invoking its raw-file reader.
        analyze = next(n for n in ast.parse(sources[PATHS[0]]).body if isinstance(n, ast.FunctionDef) and n.name == 'analyze')
        loop = next(n for n in analyze.body if isinstance(n, ast.For) and ast.unparse(n.target) == '(b, indices)')
        assert ast.unparse(loop.iter) == 'enumerate(draws)'
        calls = [n for n in ast.walk(loop) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)]
        bindings = {}
        for name in ['accumulate_image_copies', 'diagnostic_means', 'mean_margin']:
            call = next(n for n in calls if n.func.id == name)
            bindings[name] = ast.unparse(call.args[1]); assert bindings[name] == 'indices'
        assert not any(n.func.id == 'paired_bootstrap_indices' for n in calls)
        fixture(current, {'draw_matrix': draws.tolist(), 'toy_cell_values': values.tolist(),
                          'paired_contrast_ci95': correct.tolist(), 'unpaired_ci95': wrong_unpaired.tolist(),
                          'wrong_marginal_endpoint_subtraction': marginal.tolist(),
                          'frozen_loop_same_indices_bindings': bindings,
                          'scope': 'synthetic linear cell statistic + frozen arithmetic and AST wiring; not dataset AP'})

        current = 'mechanism_signs_and_non_rescue'
        values = np.zeros((5, 3, 8))
        values[0, 1, [5, 6, 7]] = [2, 70, 80]
        values[0, 2, [5, 6, 7]] = [1, 70, 80]
        for c in range(1, 5):
            values[c, 1, [5, 6, 7]] = [2+3*c, 70-4*c, 80-c]
            values[c, 2, [5, 6, 7]] = [1+c, 70-2*c, 80-c]
        margin = np.array([.25, .5, .75, 1.])
        got = f['mechanism_values'](values, margin)
        expected = {}
        keys = list(got)
        expected[keys[0]] = [2., 4., 6., 8.]
        expected[keys[1]] = [2., 4., 6., 8.]
        expected[keys[2]] = margin
        for k in keys:
            compare(got[k], expected[k])
        reversed_values = values[:, [0, 2, 1], :]
        negative = f['mechanism_values'](reversed_values, -margin)
        for k in keys:
            compare(negative[k], -np.asarray(expected[k]))
        x = metric_tensor(scores([0, 0, 0, 0], [0, 0, 0, 0]))
        bs = np.repeat(x[None], 5, axis=0)
        strong = f['assess_gates'](x, bs, got, {k: np.repeat(v[None], 5, axis=0) for k, v in got.items()}, True)
        weak = f['assess_gates'](x, bs, negative, {k: np.repeat(v[None], 5, axis=0) for k, v in negative.items()}, True)
        compare(strong['gate3_statistical_support'], True); compare(weak['gate3_statistical_support'], False)
        for key in ['gate1', 'gate2']:
            compare(strong[key], False); compare(weak[key], False)
        assert strong['research_acceptance'] == weak['research_acceptance'] == 'Research Lead decision required'
        fixture(current, {'positive_contrasts': {k: np.asarray(v).tolist() for k, v in expected.items()},
                          'swapped_hard_random_negates_all': True, 'strong_gate3_gate1_gate2': [True, False, False],
                          'research_acceptance': strong['research_acceptance']})

        current = 'common_localized_support_sum_count_and_nan'
        diagnostics = {}
        for c in range(5):
            for v in (1, 2):
                rows = []
                for i, count in enumerate((3, 2, 1)):
                    m = np.array([1. + .25*j + i for j in range(count)])
                    if c: m -= c * (.25 if v == 1 else .125) * (i+1)
                    if c == 1 and v == 1: m[-1] = np.nan
                    if c == 1 and v == 2 and i == 0: m[0] = np.nan
                    if c == 3 and v == 2: m[:] = np.nan
                    rows.append({'gt_ids': np.arange(count)+10*i, 'margin': m})
                diagnostics[c, v] = rows
        expected_rows = np.zeros((4, 3, 2))
        for c in range(1, 5):
            for i in range(3):
                four = [diagnostics[key][i]['margin'] for key in [(0, 1), (c, 1), (0, 2), (c, 2)]]
                terms = []
                for entries in zip(*four):
                    if all(math.isfinite(value) for value in entries):
                        h0, hc, r0, rc = entries
                        terms.append((h0-hc) - (r0-rc))
                expected_rows[c-1, i] = [sum(terms), len(terms)]
        rows = f['margin_rows'](diagnostics, [0, 1, 2]); compare(rows, expected_rows)
        evidence = []
        for selection in ([0, 1, 2], [1, 1, 2], [2, 2, 2]):
            means = []
            for c in range(4):
                total = sum(expected_rows[c, i, 0] for i in selection)
                count = sum(expected_rows[c, i, 1] for i in selection)
                means.append(total/count if count else float('nan'))
            actual = f['mean_margin'](rows, selection); compare(actual, means)
            compare(f['mechanism_values'](values, actual)[keys[2]], means)
            compare(f['interval'](np.array([actual, actual])), None)
            evidence.append({'draws': selection, 'means': actual.tolist()})
        # Unequal support distinguishes micro sum/count from averaging per-image means.
        aggregate = f['mean_margin'](rows, [0, 1, 2])[1]
        wrong = np.mean(rows[1, :, 0] / rows[1, :, 1])
        assert abs(aggregate-wrong) > 1e-12
        fixture(current, {'sum_count_rows': rows.tolist(), 'aggregations': evidence,
                          'common_gt_counts': rows[:, :, 1].sum(axis=1).tolist(),
                          'micro_margin_c2': float(aggregate), 'wrong_image_mean_c2': float(wrong),
                          'zero_support': 'NaN; CI unavailable; no imputation or discarded replicate'})

        current = 'optional_toy_coco'
        absent = importlib.util.find_spec('pycocotools') is None
        receipt['optional_toy_coco'] = {'status': 'NOT RUN', 'reason': 'dependency absent' if absent else 'not executed in this numpy-only audit'}
        receipt['maximum_absolute_error'] = max_error
        receipt['status'] = 'PASS'
    except Exception as exc:
        receipt['status'] = 'BLOCKED'
        receipt['failure'] = {'fixture': current, 'type': type(exc).__name__, 'detail': str(exc)}
    receipt['audit_source_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    receipt['finished_utc'] = datetime.now(timezone.utc).isoformat()
    # JSON null denotes explicitly undefined margins; descriptions retain NaN semantics.
    def sanitize(value):
        if isinstance(value, float) and not math.isfinite(value): return None
        if isinstance(value, dict): return {k: sanitize(v) for k, v in value.items()}
        if isinstance(value, list): return [sanitize(v) for v in value]
        return value
    (OUT / 'shadow_analysis_receipt.json').write_text(json.dumps(sanitize(receipt), indent=2, allow_nan=False)+'\n', encoding='utf-8')
    print(json.dumps({'status': receipt['status'], 'fixtures': len(receipt['fixtures']),
                      'maximum_absolute_error': max_error, 'failure': receipt.get('failure')}))
    return 0 if receipt['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(run())
