import copy
import math
import hashlib
import json

import pytest

from research_log.t009.query_analysis import aggregate, episode_rows, offline_outcome, query_features
from research_log.t009.audit import attribution, gate_a, gate_b, run
from research_log.t008.statistics import auroc, loso


def record():
    return {'state_id': 'synthetic', 'seed': 7, 'branch': 'original_P', 'step': 0,
            'regime': 'easy', 'episode_seed': 42, 'labels': [0, 1],
            'outputs': {'W0_probabilities': [[.8, .2], [.4, .6]],
                        'C2_probabilities': [[.3, .7], [.1, .9]],
                        'W0_tokens': [[1, 0], [0, 1]], 'C2_tokens': [[1, 1], [0, 1]]}}


def test_query_feature_equations_and_oracle_label_separation():
    r = record()
    rows = episode_rows(r)
    f = query_features([.8, .2], [.3, .7], [1, 0], [1, 1])
    assert f['query_entropy'] == pytest.approx(-.8*math.log(.8)-.2*math.log(.2))
    assert f['query_probability_gap'] == pytest.approx(.6)
    assert f['representation_displacement'] == pytest.approx(1)
    assert f['prediction_changed'] == 1
    assert f['delta_probability_gap'] == pytest.approx(-.2)
    assert f['query_js'] == pytest.approx(.5*(.8*math.log(.8/.55)+.2*math.log(.2/.45)+.3*math.log(.3/.55)+.7*math.log(.7/.45)))
    altered = copy.deepcopy(r)
    altered['labels'] = [1, 0]
    rerun = episode_rows(altered)
    assert all(rows[j][k] == rerun[j][k] for j in range(2) for k in f)
    assert rows[0]['delta_nll'] != rerun[0]['delta_nll']


def test_query_to_episode_decomposition_and_lower_nll_oracle():
    rows = episode_rows(record())
    metrics = aggregate(rows)
    assert metrics['before_nll'] == pytest.approx(-math.log(.8*.6)/2)
    assert metrics['oracle_nll'] == pytest.approx(-math.log(.8*.9)/2)
    assert metrics['oracle_accuracy'] == 1
    assert metrics['after_nll']-metrics['before_nll'] == pytest.approx(sum(r['delta_nll'] for r in rows)/2)
    assert rows[0]['transition'] == 'correct->wrong'
    assert rows[1]['transition'] == 'correct->correct'
    tie = offline_outcome([.5, .5], [.5, .5], 0)
    assert not tie['oracle_uses_C2'] and tie['nll_direction'] == 'equal'
    # An NLL oracle can select a wrong prediction even when W0 is correct.
    unusual = offline_outcome([.4, .35, .25], [.41, .5, .09], 0)
    assert unusual['oracle_uses_C2'] and unusual['oracle_accuracy'] == 0


def test_query_loso_holds_whole_seeds_and_rejects_regime_confound():
    rows = []
    for seed in (7, 17, 27):
        for branch in ('P_O0_resume', 'P_C2_warm'):
            for regime in ('easy', 'hard'):
                for j in range(10):
                    harm = j < (9 if regime == 'easy' else 1)
                    rows.append({'seed': seed, 'branch': branch, 'regime': regime,
                                 'query_max_probability': int(regime == 'easy'), 'delta_nll': .1 if harm else -.1})
    assert auroc([0, .5, .5, 1], [False, True, False, True]) == .875
    folds = loso(rows, 'query_max_probability')
    assert all(f['orientation_train_count'] == 80 and f['overall']['count'] == 40 for f in folds)
    g = gate_a(rows, 'query_max_probability', folds)
    assert g['overall_passes'] and not g['easy_passes'] and not g['passes']
    for r in rows:
        r['query_max_probability'] = int(r['delta_nll'] > 0)
    assert gate_a(rows, 'query_max_probability', loso(rows, 'query_max_probability'))['passes']
    prior = next(f for f in loso(rows, 'query_max_probability') if f['held_seed'] == 27)
    for r in rows:
        if r['seed'] == 27:
            r['delta_nll'] *= -1
    after = next(f for f in loso(rows, 'query_max_probability') if f['held_seed'] == 27)
    assert after['orientation'] == prior['orientation'] and after['overall']['auroc'] == 0


def test_damage_attribution_signed_offsets_and_b_thresholds():
    rows = []
    for regime in ('easy', 'hard'):
        for j, d in enumerate((2., -1., .5, -.5)):
            rows.append({'state_id': 's', 'regime': regime, 'episode_seed': 1,
                         'delta_nll': d, 'query_max_probability': .5+.1*j, 'prediction_changed': int(j == 0)})
    bounds, table = attribution(rows)
    selected = [r for r in table if r['regime'] == 'overall' and r['grouping'] == 'quartile']
    assert sum(r['net_share'] for r in selected) == pytest.approx(1)
    assert sum(r['positive_share'] for r in selected) == pytest.approx(1)
    assert any(r['net_share'] < 0 for r in selected)
    c = {'scope': 'focus/original_P/hard', 'before_nll': 1., 'after_nll': .8, 'oracle_nll': .7,
         'before_accuracy': .5, 'after_accuracy': .6, 'oracle_accuracy': .61}
    assert gate_b([c], [])['passes']
    c['oracle_accuracy'] = .59
    assert not gate_b([c], [])['passes']


def test_frozen_log_end_to_end_accounting_and_determinism(tmp_path):
    manifest = {'source_commit': 'synthetic-fixture', 'records': [], 'episodes': 0, 'queries': 0}
    for seed in (7, 17, 27):
        for branch in ('original_P', 'P_O0_resume', 'P_C2_warm'):
            for regime in ('easy', 'hard'):
                records = []
                for index in (0, 1):
                    r = record()
                    r.update(seed=seed, branch=branch, regime=regime, episode_seed=index,
                             state_id=f'{seed}_{branch}', step=0 if branch == 'original_P' else 400)
                    rows = episode_rows(r)
                    r['outcomes'] = {stage: {'nll': sum(x[stage+'_nll'] for x in rows)/2,
                                             'accuracy': sum(x[stage+'_accuracy'] for x in rows)/2,
                                             'query_nll': [x[stage+'_nll'] for x in rows]} for stage in ('before', 'after')}
                    r['outcomes']['delta_nll'] = sum(x['delta_nll'] for x in rows)/2
                    r['checks'] = {k: {'bitwise_equal': True} for k in ('normal', 'oracle_on_off', 'W0_repeat')}
                    records.append(r)
                path = tmp_path/f'{seed}_{branch}_{regime}.json'
                path.write_text(json.dumps(records))
                manifest['records'].append({'path': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'episodes': 2, 'queries': 4})
                manifest['episodes'] += 2
                manifest['queries'] += 4
    a = run(tmp_path, manifest, tmp_path/'out', 'test')
    b = run(tmp_path, manifest, tmp_path/'repeat', 'test')
    a.pop('environment')
    b.pop('environment')
    assert a == b
    assert a['query_count'] == 72 and a['episode_count'] == 36
    assert a['A_passes'] and a['B']['passes']
    assert (tmp_path/'out/queries.csv').read_bytes() == (tmp_path/'repeat/queries.csv').read_bytes()

