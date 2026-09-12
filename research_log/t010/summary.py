"""Fixed T010 reporting and confirmatory gates."""

from collections import defaultdict
from statistics import mean

METHODS = ('R0', 'R1', 'R2', 'R3', 'ORACLE')


def ratio(n, d):
    return n/d if d else None


def summarize(rows):
    groups = defaultdict(list)
    for row in rows:
        for key in ('overall', f"seed/{row['seed']}", f"group/{row['branch']}/{row['regime']}",
                    f"cell/{row['seed']}/{row['branch']}/{row['regime']}"):
            groups[key].append(row)
    results = []
    for scope, records in groups.items():
        for method in METHODS:
            nll, accuracy = mean(r[method+'_nll'] for r in records), mean(r[method+'_accuracy'] for r in records)
            gain_count = sum(r['gain'] for r in records)
            damage_count = sum(r['damage'] for r in records)
            kept_gains = sum(r['gain'] and r[method+'_keep'] for r in records)
            removed_damage = sum(r['damage'] and not r[method+'_keep'] for r in records)
            r1_nll, oracle_nll = mean(r['R1_nll'] for r in records), mean(r['ORACLE_nll'] for r in records)
            r1_acc, oracle_acc = mean(r['R1_accuracy'] for r in records), mean(r['ORACLE_accuracy'] for r in records)
            results.append({'scope': scope, 'method': method, 'query_count': len(records),
                            'nll': nll, 'accuracy': accuracy, 'retention': mean(r[method+'_keep'] for r in records),
                            'gain_count': gain_count, 'gains_retained': kept_gains, 'gain_retained_fraction': ratio(kept_gains, gain_count),
                            'damage_count': damage_count, 'damages_rolled_back': removed_damage, 'damage_rollback_fraction': ratio(removed_damage, damage_count),
                            'oracle_nll_headroom_fraction': ratio(r1_nll-nll, r1_nll-oracle_nll),
                            'oracle_accuracy_headroom_fraction': ratio(accuracy-r1_acc, oracle_acc-r1_acc)})
    return results


def gates(table, validity):
    scopes = defaultdict(dict)
    for r in table:
        scopes[r['scope']][r['method']] = r
    clauses = []
    for scope, methods in scopes.items():
        a, b, c = (methods[m] for m in ('R0', 'R1', 'R2'))
        if scope.startswith('seed/'):
            clauses.append({'gate': 1, 'scope': scope, 'passes': c['nll'] < a['nll'] and c['nll'] <= b['nll']+.01 and c['accuracy'] >= min(a['accuracy'], b['accuracy']),
                            'R2_minus_R0_nll': c['nll']-a['nll'], 'R2_minus_R1_nll': c['nll']-b['nll'],
                            'R2_minus_worse_baseline_accuracy': c['accuracy']-min(a['accuracy'], b['accuracy'])})
            clauses.append({'gate': 4, 'scope': scope, 'passes': .1 <= c['retention'] <= .9, 'retention': c['retention']})
        if scope.startswith('group/') and scope.endswith('/hard'):
            nll_gain, acc_gain = a['nll']-b['nll'], b['accuracy']-a['accuracy']
            nll_kept, acc_kept = a['nll']-c['nll'], c['accuracy']-a['accuracy']
            nll_pass = nll_kept >= .75*nll_gain if nll_gain > 0 else c['nll'] <= a['nll']+.01
            acc_pass = acc_kept >= .70*acc_gain if acc_gain > 0 else c['accuracy'] >= a['accuracy']-.01
            clauses.append({'gate': 2, 'scope': scope, 'passes': nll_pass and acc_pass, 'nll_passes': nll_pass, 'accuracy_passes': acc_pass,
                            'R1_nll_gain': nll_gain, 'R2_nll_gain': nll_kept, 'R1_accuracy_gain': acc_gain, 'R2_accuracy_gain': acc_kept,
                            'nll_gain_retained': ratio(nll_kept, nll_gain), 'accuracy_gain_retained': ratio(acc_kept, acc_gain)})
        if scope.startswith('cell/') and scope.endswith('/easy'):
            nll_regression, acc_regression = b['nll']-a['nll'], a['accuracy']-b['accuracy']
            nll_removed, acc_removed = b['nll']-c['nll'], c['accuracy']-b['accuracy']
            nll_pass = (nll_removed >= .60*nll_regression) if nll_regression > 0 else ((a['nll']-c['nll'] >= .5*(-nll_regression)) or c['nll'] <= a['nll']+.01)
            acc_pass = acc_removed >= .50*acc_regression if acc_regression > 0 else True
            clauses.append({'gate': 3, 'scope': scope, 'passes': nll_pass and acc_pass, 'nll_passes': nll_pass, 'accuracy_passes': acc_pass,
                            'R1_nll_regression': nll_regression, 'R2_nll_regression': c['nll']-a['nll'],
                            'R1_accuracy_regression': acc_regression, 'R2_accuracy_regression': a['accuracy']-c['accuracy'],
                            'nll_regression_removed_fraction': ratio(nll_removed, nll_regression) if nll_regression > 0 else None,
                            'accuracy_regression_removed_fraction': ratio(acc_removed, acc_regression) if acc_regression > 0 else None})
    clauses.append({'gate': 5, 'scope': 'validity', 'passes': validity})
    by_gate = {str(i): all(c['passes'] for c in clauses if c['gate'] == i) for i in range(1, 6)}
    return {'passes': all(by_gate.values()), 'by_gate': by_gate, 'clauses': clauses}
