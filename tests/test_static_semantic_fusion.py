import os
import copy
import hashlib
import json
from unittest.mock import patch

import torch

from tovd.models.static_semantic_fusion import product_of_experts, static_evidence
from tovd.synthetic.models import EpisodicClassifier


def fixture():
    torch.manual_seed(21)
    device = os.environ.get('TOVD_TEST_DEVICE', 'cpu')
    model = EpisodicClassifier('O1_backtracking').to(device).eval()
    X, T, Q = [torch.randn(1, n, 16, device=device) for n in (12, 4, 5)]
    return model, X, T, Q


def test_literal_product_of_experts_formula_including_zero_exponent():
    device = os.environ.get('TOVD_TEST_DEVICE', 'cpu')
    p0 = torch.tensor([[[.6, .3, .1]]], device=device, dtype=torch.float64)
    teacher = torch.tensor([[[.2, .3, .5]]], device=device, dtype=torch.float64)
    for exponent in (0, .1, .5, 2):
        actual = product_of_experts(p0, teacher, exponent)
        raw = (p0+1e-12)*(teacher+1e-12)**exponent
        expected = raw/raw.sum(-1, keepdim=True)
        torch.testing.assert_close(actual['probabilities'], expected, rtol=1e-13, atol=1e-13)
        torch.testing.assert_close(actual['log_probabilities'], expected.log(), rtol=1e-13, atol=1e-13)


def test_forward_only_exact_w0_query_isolation_reset_and_immutable_model():
    model, X, T, Q = fixture()
    original = {k: v.clone() for k, v in model.state_dict().items()}
    with torch.inference_mode():
        baseline = model.memory(X, T, Q, enable_ttt=False)
        expected = model.logits(baseline.tokens, T).softmax(-1)
    with (patch('torch.autograd.grad', side_effect=AssertionError('static inference requested a gradient')),
          patch('torch.Tensor.backward', side_effect=AssertionError('static inference requested backward'))):
        first = static_evidence(model, X, T, Q)
        product_of_experts(first['p0'], first['teacher'], .2)
        static_evidence(model, -X, T.roll(1, -1), -Q)
        replay = static_evidence(model, X, T, Q)
        for key in first:
            assert torch.equal(first[key], replay[key]) and not first[key].requires_grad
        for j in range(Q.shape[1]):
            changed = -Q.clone()
            changed[:, j] = Q[:, j]
            isolated = static_evidence(model, X, T, changed)
            assert torch.equal(first['teacher'][:, j], isolated['teacher'][:, j])
    assert torch.equal(first['tokens'], baseline.tokens) and torch.equal(first['p0'], expected)
    for k, v in model.state_dict().items():
        assert torch.equal(v.view(torch.uint8), original[k].view(torch.uint8))
    assert all(p.grad is None for p in model.parameters())


def test_existing_b1_formula_replays_on_same_frozen_state():
    model, X, T, Q = fixture()
    b1 = EpisodicClassifier('B1').to(X.device).eval()
    b1.load_state_dict(model.state_dict())
    with torch.inference_mode():
        result = b1(X, T, Q)
        static = b1.memory(X, T, Q, enable_ttt=False)
        query_context = (static.tokens @ T.transpose(-1, -2)/b1.memory.tau).softmax(-1) @ T
        keys = b1.memory.key_projection(X)
        scene = b1.memory.inner_targets(keys, X, T).mean(1, keepdim=True)
        expected = static.tokens+.5*query_context+.5*scene
    assert torch.equal(result.tokens, expected)
    assert all(torch.equal(v, model.state_dict()[k]) for k, v in b1.state_dict().items())


def test_global_base_calibration_excludes_validation_and_breaks_ties_smallest():
    from research_log.t012.summary import calibrate
    rows = [dict(phase='calibration', seed=s, state_id=str(s), episode_seed=s, A0_nll=1.,
                 lambda_0_nll=1., lambda_1_nll=.8, lambda_2_nll=.8,
                 lambda_0_accuracy=.5, lambda_1_accuracy=.5, lambda_2_accuracy=.5) for s in (7, 17, 27)]
    result = calibrate(rows, [0, .1, 1])
    assert result['exponent'] == .1 and result['seeds'] == [7, 17, 27] and result['query_count'] == 3
    contaminated = rows+[dict(phase='validation', lambda_2_nll=-1000)]
    assert calibrate(contaminated, [0, .1, 1]) == result


def test_five_static_gate_arithmetic_and_numerical_null():
    from research_log.t012.summary import summarize, gates
    rows = []
    for branch in ('original_P', 'P_O0_resume', 'P_C2_warm'):
        for seed in (7, 17, 27):
            for regime in ('easy', 'hard'):
                nlls = (1., 1.1, .9, .95, .88) if regime == 'hard' else (.4, .5, .41, .405, .4)
                rows.append(dict(branch=branch, seed=seed, regime=regime,
                                 **{m+'_nll': n for m, n in zip(('A0', 'A1', 'A2', 'A3', 'A4'), nlls)},
                                 **{m+'_accuracy': .7 for m in ('A0', 'A1', 'A2', 'A3', 'A4')}))
    table = summarize(rows)
    assert gates(table, True)['passes']
    for gate, scope, nll in ((1, 'group/original_P/hard', 1.1), (2, 'cell/7/original_P/hard', 1.04),
                            (3, 'group/original_P/easy', .43), (4, 'regime/hard', .96)):
        changed = copy.deepcopy(table)
        next(r for r in changed if r['scope'] == scope and r['method'] == 'A2')['nll'] = nll
        assert not gates(changed, True)['by_gate'][str(gate)]
    assert not gates(table, False)['by_gate']['5']
    null = copy.deepcopy(table)
    for r in null:
        if r['method'] in ('A2', 'A3'):
            r['nll'] = next(a['nll'] for a in table if a['scope'] == r['scope'] and a['method'] == 'A0')-1e-8
    assert not gates(null, True)['by_gate']['1'] and not gates(null, True)['by_gate']['4']


def test_calibration_has_no_gradient_and_runtime_outputs_ignore_labels_ids():
    from research_log.t012.experiment import extract_episode
    from tovd.synthetic.semantic_episodes import SemanticWorld, WorldConfig
    model, _, _, _ = fixture()
    config = json.load(open('research_log/t012/config.json'))
    ep = SemanticWorld(WorldConfig(seed=314159)).episode('train', 'easy', 1234).to(next(model.parameters()).device)
    with (patch('torch.autograd.grad', side_effect=AssertionError('calibration invoked a gradient')),
          patch.object(model, 'forward', side_effect=AssertionError('calibration invoked C2'))):
        cal = extract_episode(model, ep, config, 'calibration')
    assert cal['checks']['inference_tensors']
    b1 = EpisodicClassifier('B1').to(ep.X.device).eval()
    b1.load_state_dict(model.state_dict())
    first = extract_episode(model, ep, config, 'validation', .2, b1)
    ep.labels = (ep.labels+1) % 4
    ep.query_ids.fill_(-7)
    second = extract_episode(model, ep, config, 'validation', .2, b1)
    assert first['outputs'] == second['outputs'] and first['evidence'] == second['evidence']
    assert first['queries'] != second['queries']
    assert all(first['checks'][k] for k in ('A0_bitwise_equal', 'A1_bitwise_equal', 'A4_bitwise_equal', 'inference_tensors'))


def test_random_world_two_phase_end_to_end_with_frozen_global_lambda(tmp_path):
    from research_log.t012.experiment import fresh_id, run
    config = json.load(open('research_log/t012/config.json'))
    config.update(calibration_episodes=1, validation_episodes=1)
    config['world']['seed'] = 314159
    states = []
    for seed in config['seeds']:
        torch.manual_seed(seed)
        path = tmp_path/f'{seed}.pt'
        torch.save({'state_dict': EpisodicClassifier('O1_backtracking').state_dict()}, path)
        states.append(dict(state_id=f'seed{seed}', branch='original_P', seed=seed, step=0,
                           path='research_log/remote_runs/'+path.name, sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    manifest = dict(states=states, code_hashes=[], historical_ids=[],
                    fresh_episode_ids={p: [fresh_id(config, p, s, r, 0) for s in config['seeds'] for r in ('easy', 'hard')]
                                       for p in ('calibration', 'validation')})
    device = os.environ.get('TOVD_TEST_DEVICE', 'cpu')
    cal = run(config, manifest, tmp_path, tmp_path/'cal', 'calibration', device, 'unit-test')
    frozen = copy.deepcopy(cal['frozen_lambda'])
    val = run(config, manifest, tmp_path, tmp_path/'val', 'validation', device, 'unit-test', frozen=frozen, lambda_commit='unit-calibration-commit')
    assert frozen == cal['frozen_lambda'] == val['frozen_lambda']
    assert cal['validity']['passes'] and val['validity']['passes']
    assert cal['validity']['query_count'] == val['validity']['query_count'] == 48
    assert not set(cal['validity']['episode_ids']) & set(val['validity']['episode_ids'])
