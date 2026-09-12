"""T009 deterministic frozen-log analysis; never executes a model."""

import argparse
from collections import defaultdict
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import platform
from statistics import mean

from research_log.t008.statistics import auroc, fold_summary, loso, quantile, stats_for
from .query_analysis import FEATURES, FEATURE_METADATA, PRE, aggregate, episode_rows


def save_json(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False)+'\n', encoding='utf-8')


def save_csv(path, rows):
    with path.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows({k: json.dumps(v) if isinstance(v, (dict, list)) else v for k, v in row.items()} for row in rows)


def scopes_for(rows):
    scopes = {'overall': rows}
    for row in rows:
        keys = [f"regime/{row['regime']}", f"seed/{row['seed']}/{row['regime']}",
                f"branch/{row['branch']}/overall", f"branch/{row['branch']}/{row['regime']}",
                f"step/{row['branch']}/{row['step']}/{row['regime']}",
                f"state/{row['state_id']}/{row['regime']}"]
        for key in keys:
            scopes.setdefault(key, []).append(row)
    return scopes


def gate_a(rows, feature, folds):
    overall, easy = fold_summary(folds, 'overall'), fold_summary(folds, 'easy')
    orientations = [f['orientation'] for f in folds]
    consistent = orientations[0] is not None and len(set(orientations)) == 1
    sign = orientations[0] if consistent else None
    branches = {}
    for branch in ('P_O0_resume', 'P_C2_warm'):
        for regime in ('overall', 'easy'):
            subset = [r for r in rows if r['branch'] == branch and (regime == 'overall' or r['regime'] == regime)]
            branches[branch+'/'+regime] = auroc([sign*r[feature] for r in subset], [r['delta_nll'] > 0 for r in subset]) if sign is not None else None
    g1 = overall['mean'] is not None and overall['mean'] >= .70 and overall['min'] >= .65
    g2 = easy['mean'] is not None and easy['mean'] >= .65 and easy['min'] >= .60
    g3 = consistent and all(a is not None and a > .5 for a in branches.values())
    return {'feature': feature, 'availability': FEATURE_METADATA[feature]['availability'],
            'overall': overall, 'easy': easy, 'orientations': orientations,
            'branch_oriented_aurocs': branches, 'overall_passes': g1, 'easy_passes': g2,
            'direction_passes': g3, 'passes': g1 and g2 and g3}


def attribution(rows):
    bounds = [quantile([r['query_max_probability'] for r in rows], p) for p in (.25, .5, .75)]
    episodes = defaultdict(list)
    for r in rows:
        episodes[(r['state_id'], r['regime'], r['episode_seed'])].append(r)
    positive = [r for group in episodes.values() if mean(x['delta_nll'] for x in group) > 0 for r in group]
    result = []
    for regime in ('overall', 'easy', 'hard'):
        subset = positive if regime == 'overall' else [r for r in positive if r['regime'] == regime]
        net = sum(r['delta_nll'] for r in subset)
        gross = sum(max(r['delta_nll'], 0) for r in subset)
        groups = defaultdict(list)
        for r in subset:
            quartile = 1+sum(r['query_max_probability'] > b for b in bounds)
            flip = 'flip' if r['prediction_changed'] else 'no_flip'
            for grouping, group in (('quartile', f'Q{quartile}'), ('flip', flip), ('quartile_flip', f'Q{quartile}/{flip}')):
                groups[grouping, group].append(r)
        for (grouping, group), selected in sorted(groups.items()):
            signed = sum(r['delta_nll'] for r in selected)
            positive_mass = sum(max(r['delta_nll'], 0) for r in selected)
            result.append({'regime': regime, 'grouping': grouping, 'group': group, 'count': len(selected),
                           'net_damage': signed, 'positive_damage': positive_mass,
                           'negative_offset': signed-positive_mass, 'net_denominator': net, 'positive_denominator': gross,
                           'net_share': signed/net if net else None, 'positive_share': positive_mass/gross if gross else None})
    return bounds, result


def ceilings_for(episodes):
    result = []
    for scope, subset in scopes_for(episodes).items():
        result.append({'scope': scope, **aggregate(subset)})
    for branch in ('original_P', 'P_O0_resume', 'P_C2_warm'):
        target = 0 if branch == 'original_P' else 400
        for regime in ('easy', 'hard'):
            selected = [r for r in episodes if r['branch'] == branch and r['step'] == target and r['regime'] == regime]
            if selected:
                result.append({'scope': f'focus/{branch}/{regime}', **aggregate(selected)})
    return result


def gate_b(ceilings, episodes):
    clauses = []
    for c in ceilings:
        if not (c['scope'].startswith('focus/') and c['scope'].endswith('/hard')):
            continue
        for metric, direction in (('nll', -1), ('accuracy', 1)):
            gain = direction*(c['after_'+metric]-c['before_'+metric])
            oracle_gain = direction*(c['oracle_'+metric]-c['before_'+metric])
            required = .95*gain if gain > 0 else 0
            clauses.append({'scope': c['scope'], 'kind': 'hard_gain', 'metric': metric,
                            'C2_gain_or_regression': gain, 'oracle_gain_or_removed': oracle_gain,
                            'required': required, 'passes': oracle_gain >= required})
    groups = defaultdict(list)
    for e in episodes:
        if e['regime'] == 'easy' and ((e['branch'] == 'original_P' and e['step'] == 0) or e['step'] == 400):
            groups[e['state_id']].append(e)
    for state, selected in groups.items():
        c = aggregate(selected)
        for metric, direction in (('nll', 1), ('accuracy', -1)):
            regression = direction*(c['after_'+metric]-c['before_'+metric])
            if regression > 0:
                residual = direction*(c['oracle_'+metric]-c['before_'+metric])
                removed = regression-residual
                clauses.append({'scope': f'state/{state}/easy', 'kind': 'easy_regression', 'metric': metric,
                                'C2_gain_or_regression': regression, 'oracle_gain_or_removed': removed,
                                'required': .8*regression, 'passes': removed >= .8*regression})
    return {'passes': bool(clauses) and all(c['passes'] for c in clauses), 'clauses': clauses}


def analyze(rows, episodes):
    scopes = scopes_for(rows)
    single = [{'scope': scope, 'feature': feature, **stats_for(subset, feature)}
              for scope, subset in scopes.items() for feature in FEATURES]
    folds = {f: {'primary': loso(rows, f), 'sensitivity_gt_005': loso(rows, f, .05)} for f in FEATURES}
    gates = {f: gate_a(rows, f, folds[f]['primary']) for f in FEATURES}
    bounds, damage = attribution(rows)
    transitions = []
    for scope, subset in scopes.items():
        groups = defaultdict(list)
        for r in subset:
            groups[r['transition'], r['nll_direction']].append(r)
        for (transition, direction), selected in groups.items():
            transitions.append({'scope': scope, 'transition': transition, 'nll_direction': direction,
                                'count': len(selected), 'fraction': len(selected)/len(subset),
                                'delta_sum': sum(r['delta_nll'] for r in selected), 'mean_delta': mean(r['delta_nll'] for r in selected)})
    ceilings = ceilings_for(episodes)
    consistency = []
    for f in FEATURES:
        base = next(s for s in single if s['scope'] == 'overall' and s['feature'] == f)['auroc_harm']
        sign = None if base is None else (1 if base >= .5 else -1)
        for s in single:
            if s['feature'] == f:
                auc = s['auroc_harm']
                consistency.append({'feature': f, 'scope': s['scope'], 'descriptive_global_sign': sign,
                                    'local_sign': None if auc is None else (1 if auc >= .5 else -1),
                                    'raw_auc': auc, 'global_oriented_auc': None if auc is None or sign is None else auc if sign == 1 else 1-auc})
    return {'query_count': len(rows), 'episode_count': len(episodes), 'single_features': single, 'loso': folds,
            'gates_A': gates, 'A_passes': any(g['passes'] for g in gates.values()),
            'passing_pre': [f for f, g in gates.items() if g['passes'] and f in PRE],
            'passing_post': [f for f, g in gates.items() if g['passes'] and f not in PRE],
            'confidence_quartiles': bounds, 'attribution': damage, 'transitions': transitions,
            'oracle_ceilings': ceilings, 'B': gate_b(ceilings, episodes), 'direction_consistency': consistency}


def run(root, manifest, output, revision):
    output.mkdir(parents=True, exist_ok=True)
    source_checks = []
    for source in manifest['records']:
        actual = hashlib.sha256((root/source['path']).read_bytes()).hexdigest()
        source_checks.append({'path': source['path'], 'sha256': actual, 'matches': actual == source['sha256']})
    assert all(c['matches'] for c in source_checks)
    queries, episodes, errors = [], [], []
    for source in manifest['records']:
        records = json.loads((root/source['path']).read_text(encoding='utf-8'))
        assert len(records) == source['episodes']
        file_count = 0
        for record in records:
            rows = episode_rows(record)
            assert rows == episode_rows(record)
            file_count += len(rows)
            meta = {k: record[k] for k in ('state_id', 'seed', 'branch', 'step', 'regime', 'episode_seed')}
            summary = aggregate(rows)
            ep = {**meta, **summary, 'delta_nll': summary['after_nll']-summary['before_nll']}
            previous = record['outcomes']
            nll_error = max(abs(summary[stage+'_nll']-previous[stage]['nll']) for stage in ('before', 'after'))
            delta_error = abs(ep['delta_nll']-previous['delta_nll'])
            accuracy_error = max(abs(summary[stage+'_accuracy']-previous[stage]['accuracy']) for stage in ('before', 'after'))
            historical_query_error = max(abs(r[stage+'_nll']-previous[stage]['query_nll'][j]) for j, r in enumerate(rows) for stage in ('before', 'after'))
            sign_differences = sum((r['delta_nll'] > 0) != (previous['after']['query_nll'][j]-previous['before']['query_nll'][j] > 0) for j, r in enumerate(rows))
            oracle_equal = all(record['checks'][k]['bitwise_equal'] for k in ('normal', 'oracle_on_off', 'W0_repeat'))
            errors.append({**meta, 'nll_error': nll_error, 'delta_error': delta_error, 'accuracy_error': accuracy_error,
                           'historical_query_nll_error': historical_query_error, 'query_harm_sign_differences': sign_differences,
                           'historical_oracle_bitwise_equal': oracle_equal})
            assert nll_error <= 2e-6 and delta_error <= 2e-6 and accuracy_error == 0 and oracle_equal
            queries.extend(rows)
            episodes.append(ep)
        assert file_count == source['queries']
    assert len(queries) == manifest['queries'] and len(episodes) == manifest['episodes']
    assert len({(r['state_id'], r['regime'], r['episode_seed'], r['query_index']) for r in queries}) == len(queries)
    assert all(math.isfinite(r[f]) for r in queries for f in FEATURES)
    print(f'EXTRACTED {len(queries)} queries / {len(episodes)} episodes', flush=True)
    save_csv(output/'queries.csv', queries)
    save_csv(output/'episodes.csv', episodes)
    checks = {'sources': source_checks, 'per_episode': errors,
              'max_nll_error': max(e['nll_error'] for e in errors), 'max_delta_error': max(e['delta_error'] for e in errors),
              'max_accuracy_error': max(e['accuracy_error'] for e in errors),
              'max_historical_query_nll_error': max(e['historical_query_nll_error'] for e in errors),
              'query_harm_sign_differences': sum(e['query_harm_sign_differences'] for e in errors),
              'features_deterministic': True, 'historical_oracle_bitwise_equal': True,
              'seed_query_counts': {str(s): sum(r['seed'] == s for r in queries) for s in sorted({r['seed'] for r in queries})},
              'model_rerun': False, 'passes': True}
    save_json(output/'checks.json', checks)
    result = analyze(queries, episodes)
    result['environment'] = {'revision': revision, 'preregistration': '1b63bf6', 'source_commit': manifest['source_commit'],
                             'time_utc': datetime.now(timezone.utc).isoformat(), 'python': platform.python_version(),
                             'platform': platform.platform(), 'device': 'local CPU; stdlib only', 'model_rerun': False}
    save_json(output/'results.json', result)
    save_json(output/'schema.json', {'features': FEATURE_METADATA, 'other_columns': {'is_label_free_feature': False,
              'fields': [k for k in queries[0] if k not in FEATURES], 'oracle_only': True},
              'separation': 'query_features accepts only stored probabilities/tokens; labels consumed afterward; no runtime output selection performed'})
    for key in ('single_features', 'attribution', 'transitions', 'oracle_ceilings', 'direction_consistency'):
        save_csv(output/(key+'.csv'), result[key])
    save_csv(output/'loso.csv', [{'feature': f, 'analysis': kind, **fold} for f, analyses in result['loso'].items() for kind, folds in analyses.items() for fold in folds])
    save_json(output/'gates.json', {'A': result['gates_A'], 'B': result['B']})
    print(json.dumps({'validity': checks['passes'], 'A': result['A_passes'], 'B': result['B']['passes'],
                      'pre': result['passing_pre'], 'post': result['passing_post']}), flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sources', type=Path, default=Path('research_log/t009/sources.json'))
    parser.add_argument('--output', type=Path, default=Path('research_log/t009/results'))
    parser.add_argument('--revision', required=True)
    args = parser.parse_args()
    run(Path.cwd(), json.loads(args.sources.read_text()), args.output, args.revision)
