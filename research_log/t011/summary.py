"""T011 fixed development criteria; no parameter selection."""

from collections import defaultdict
from statistics import mean

METHODS = ('S0', 'S1', 'S2', 'S3')


def summarize(rows):
    groups = defaultdict(list)
    for row in rows:
        for scope in ('overall', f"regime/{row['regime']}", f"group/{row['branch']}/{row['regime']}",
                      f"cell/{row['seed']}/{row['branch']}/{row['regime']}"):
            groups[scope].append(row)
    table = []
    for scope, group in groups.items():
        for method in METHODS:
            table.append(dict(scope=scope, method=method, episode_count=len(group),
                              **{metric: mean(r[method+'_'+metric] for r in group) for metric in ('nll', 'accuracy')}))
    return table


def gates(table, mechanism):
    scopes = defaultdict(dict)
    for row in table:
        scopes[row['scope']][row['method']] = row
    clauses = [dict(gate=1, scope='mechanism', **mechanism)]
    hard_cells = defaultdict(list)
    for scope, methods in scopes.items():
        a, b, c = (methods[m] for m in METHODS[:3])
        if scope.startswith('group/') and scope.endswith('/hard'):
            gain1, gain2 = a['nll']-b['nll'], a['nll']-c['nll']
            clauses.append(dict(gate=2, scope=scope, passes=gain2 > 0 and (gain1 <= 0 or gain2 >= .7*gain1)
                                and c['accuracy'] >= a['accuracy']-.01, S2_nll_gain=gain2,
                                S1_nll_gain=gain1, gain_retention=gain2/gain1 if gain1 > 0 else None,
                                accuracy_delta_pp=100*(c['accuracy']-a['accuracy'])))
        if scope.startswith('cell/'):
            if scope.endswith('/hard'):
                hard_cells[scope.split('/')[2]].append(dict(scope=scope, nll_delta=c['nll']-a['nll']))
            else:
                regression = b['nll']-a['nll']
                removed = (b['nll']-c['nll'])/regression if regression > 0 else None
                passes = removed >= .6 if removed is not None else c['nll'] <= a['nll']+.02 and c['accuracy'] >= a['accuracy']-.01
                clauses.append(dict(gate=4, scope=scope, passes=passes, S1_nll_regression=regression,
                                    regression_removed_fraction=removed, S2_minus_S0_nll=c['nll']-a['nll'],
                                    accuracy_delta_pp=100*(c['accuracy']-a['accuracy'])))
    for branch, cells in hard_cells.items():
        improved = sum(c['nll_delta'] < 0 for c in cells)
        worst = max(c['nll_delta'] for c in cells)
        clauses.append(dict(gate=3, scope=branch, passes=improved >= 2 and worst <= .03,
                            improved_seeds=improved, worst_nll_regression=worst, cells=cells))
    hard, easy = (scopes['regime/'+r] for r in ('hard', 'easy'))
    dh, de = (g['S2']['nll']-g['S3']['nll'] for g in (hard, easy))
    clauses.append(dict(gate=5, scope='pooled', passes=dh < 0 and de <= .01,
                        S2_minus_S3_hard_nll=dh, S2_minus_S3_easy_nll=de))
    by_gate = {str(g): all(c['passes'] for c in clauses if c['gate'] == g) for g in range(1, 6)}
    return dict(passes=all(by_gate.values()), by_gate=by_gate, clauses=clauses)
