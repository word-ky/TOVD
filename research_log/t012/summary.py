"""Base-only global calibration and preregistered static-fusion criteria."""

from collections import defaultdict
from statistics import mean

METHODS = ('A0', 'A1', 'A2', 'A3', 'A4')


def calibrate(rows, grid, tie_tolerance=1e-12):
    base = [r for r in rows if r['phase'] == 'calibration']
    candidates = [dict(exponent=exponent, nll=mean(r[f'lambda_{i}_nll'] for r in base),
                       accuracy=mean(r[f'lambda_{i}_accuracy'] for r in base)) for i, exponent in enumerate(grid)]
    best = min(c['nll'] for c in candidates)
    chosen = min((c for c in candidates if c['nll'] <= best+tie_tolerance), key=lambda c: c['exponent'])
    return dict(exponent=chosen['exponent'], phase='calibration', selected_nll=chosen['nll'], minimum_nll=best,
                query_count=len(base), base_A0_nll=mean(r['A0_nll'] for r in base), candidates=candidates,
                seeds=sorted({r['seed'] for r in base}), state_ids=sorted({r['state_id'] for r in base}),
                episode_ids=sorted({r['episode_seed'] for r in base}))


def summarize(rows):
    groups = defaultdict(list)
    for row in rows:
        for scope in ('overall', f"regime/{row['regime']}", f"group/{row['branch']}/{row['regime']}",
                      f"cell/{row['seed']}/{row['branch']}/{row['regime']}"):
            groups[scope].append(row)
    return [dict(scope=scope, method=method, episode_count=len(group),
                 **{metric: mean(r[method+'_'+metric] for r in group) for metric in ('nll', 'accuracy')})
            for scope, group in groups.items() for method in METHODS]


def gates(table, no_hidden_adaptation, tolerance=1e-6):
    scopes = defaultdict(dict)
    for r in table:
        scopes[r['scope']][r['method']] = r
    clauses, hard_cells = [], defaultdict(list)
    for scope, methods in scopes.items():
        a, b = (methods[m] for m in ('A0', 'A2'))
        dn, da = b['nll']-a['nll'], b['accuracy']-a['accuracy']
        if scope.startswith('group/'):
            hard = scope.endswith('/hard')
            passes = dn < -tolerance and da >= -.01 if hard else dn <= .02 and da >= -.01
            clauses.append(dict(gate=1 if hard else 3, scope=scope, passes=passes,
                                A2_minus_A0_nll=dn, accuracy_delta_pp=100*da))
        if scope.startswith('cell/') and scope.endswith('/hard'):
            hard_cells[scope.split('/')[2]].append(dict(scope=scope, nll_delta=dn))
    for group, cells in hard_cells.items():
        improved = sum(c['nll_delta'] < -tolerance for c in cells)
        worst = max(c['nll_delta'] for c in cells)
        clauses.append(dict(gate=2, scope=group, passes=improved >= 2 and worst <= .03,
                            improved_seeds=improved, worst_nll_regression=worst, cells=cells))
    hard, easy = (scopes['regime/'+regime] for regime in ('hard', 'easy'))
    dh, de = (m['A2']['nll']-m['A3']['nll'] for m in (hard, easy))
    clauses.append(dict(gate=4, scope='pooled', passes=dh < -tolerance and de <= .01,
                        A2_minus_A3_hard_nll=dh, A2_minus_A3_easy_nll=de))
    clauses.append(dict(gate=5, scope='static_inference', passes=no_hidden_adaptation))
    by_gate = {str(i): all(c['passes'] for c in clauses if c['gate'] == i) for i in range(1, 6)}
    return dict(passes=all(by_gate.values()), by_gate=by_gate, strict_improvement_tolerance=tolerance, clauses=clauses)
