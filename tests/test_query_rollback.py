import copy
import os
import hashlib
import json

import pytest

from research_log.t010.policy import calibrate, select
from research_log.t010.summary import gates


def test_hard_probability_token_selection_threshold_ties_and_extremes():
    p0, p1 = [[.8, .2], [.6, .4]], [[.6, .4], [.8, .2]]
    z0, z1 = [[0, 0], [1, 1]], [[2, 2], [3, 3]]
    picked = select(p0, p1, z0, z1, 0)
    assert picked['keep_C2'] == [False, True]
    assert picked['probabilities'] == [p0[0], p1[1]]
    assert picked['tokens'] == [z0[0], z1[1]]
    assert select(p0, p1, z0, z1, picked['delta_entropy'][0])['keep_C2'][0]
    assert select(p0, p1, z0, z1, '-inf')['tokens'] == z0
    assert select(p0, p1, z0, z1, '+inf')['tokens'] == z1


def calibration_rows():
    return [{'seed': s, 'phase': 'calibration', 'state_id': str(s), 'episode_seed': s*100+j,
             'delta_entropy': d, 'before_nll': b, 'after_nll': a}
            for s in (7, 17, 27) for j, (d, b, a) in enumerate(((-1, 1, .2), (1, .2, 1)))]


def test_calibration_loso_grid_tie_break_and_validation_label_independence():
    rows = calibration_rows()
    first = calibrate(rows, 27, [0, .5, 1])
    assert first['tau'] == -1 and first['query_count'] == 4
    assert first['calibration_seeds'] == [7, 17]
    changed = copy.deepcopy(rows)
    for r in changed:
        if r['seed'] == 27:
            r['before_nll'], r['after_nll'], r['delta_entropy'] = 100, 0, -9
    for r in rows:
        changed.append({**r, 'phase': 'validation', 'before_nll': 999, 'after_nll': 0})
    assert calibrate(changed, 27, [0, .5, 1]) == first
    for r in rows:
        r['after_nll'] = r['before_nll']
    assert calibrate(rows, 27, [0, .5, 1])['tau'] == '-inf'


def test_gate_arithmetic_exposes_hard_retention_and_easy_regression_failures():
    table = []
    for scope in ('seed/7', 'group/original_P/hard', 'cell/7/original_P/easy'):
        values = ((1., .5), (.8, .6), (.79, .59)) if not scope.endswith('easy') else ((1., .7), (1.2, .5), (.99, .65))
        for method, (nll, accuracy) in zip(('R0', 'R1', 'R2'), values):
            table.append({'scope': scope, 'method': method, 'nll': nll, 'accuracy': accuracy, 'retention': .5})
    assert gates(table, True)['passes']
    changed = copy.deepcopy(table)
    next(r for r in changed if r['scope'].endswith('/hard') and r['method'] == 'R2')['accuracy'] = .56
    assert not gates(changed, True)['by_gate']['2']
    changed = copy.deepcopy(table)
    next(r for r in changed if r['scope'].endswith('/easy') and r['method'] == 'R2')['nll'] = 1.1
    assert not gates(changed, True)['by_gate']['3']
    assert not gates(table, False)['by_gate']['5']


def test_model_runtime_selection_is_label_independent_and_reproduces_tokens():
    import torch
    from research_log.t010.experiment import extract_episode
    from tovd.synthetic.models import EpisodicClassifier
    from tovd.synthetic.semantic_episodes import SemanticWorld, WorldConfig
    device = os.environ.get('TOVD_TEST_DEVICE', 'cpu')
    torch.manual_seed(7)
    model = EpisodicClassifier('O1_backtracking').to(device).eval()
    ep = SemanticWorld(WorldConfig()).episode('test', 'easy', 2000700000).to(device)
    first = extract_episode(model, ep, 0)
    ep.labels = (ep.labels+1) % 4
    ep.query_ids.fill_(-42)
    second = extract_episode(model, ep, 0)
    assert first['outputs'] == second['outputs']
    assert first['queries'] != second['queries']
    assert first['checks']['normal_oracle_bitwise_equal']
    assert first['checks']['selected_token_probability_error'] <= 2e-6


def test_two_phase_fresh_runner_calibration_then_validation(tmp_path):
    import torch
    from research_log.t010.experiment import run, fresh_id
    from tovd.synthetic.models import EpisodicClassifier
    device = os.environ.get('TOVD_TEST_DEVICE', 'cpu')
    config = json.load(open('research_log/t010/config.json'))
    config.update(calibration_episodes=1, validation_episodes=1, quantile_grid=[0, .5, 1])
    states = []
    for seed in config['seeds']:
        torch.manual_seed(seed)
        path = tmp_path/f'{seed}.pt'
        torch.save({'state_dict': EpisodicClassifier('O1_backtracking').state_dict()}, path)
        states.append({'state_id': f'{seed}_original', 'seed': seed, 'branch': 'original_P', 'step': 0,
                       'path': f'research_log/remote_runs/{path.name}', 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    manifest = {'states': states, 'code_hashes': [], 'historical_ids': [],
                'fresh_episode_ids': {phase: [fresh_id(config, phase, s, r, 0) for s in config['seeds'] for r in ('easy', 'hard')] for phase in ('calibration', 'validation')}}
    cal = run(config, manifest, tmp_path, tmp_path/'cal', 'calibration', device, 'test')
    frozen = copy.deepcopy(cal['thresholds'])
    val = run(config, manifest, tmp_path, tmp_path/'val', 'validation', device, 'test', frozen, 'synthetic-threshold-commit')
    assert val['validity']['query_count'] == 48 and cal['validity']['query_count'] == 48
    assert frozen == cal['thresholds'] == val['thresholds']
    assert val['validity']['nonoverlap'] and val['validity']['parameters_unchanged']
    assert all(t['query_count'] == 32 for t in frozen.values())
