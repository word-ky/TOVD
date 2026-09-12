import os
import copy
import hashlib
import json

import torch
from torch.nn import functional as F

from tovd.models.query_local_residual import local_armijo, local_loss, local_teacher, query_local_residual
from tovd.models.step_control import choose_armijo_step
from tovd.synthetic.models import EpisodicClassifier


def fixture():
    torch.manual_seed(13)
    device = os.environ.get('TOVD_TEST_DEVICE', 'cpu')
    model = EpisodicClassifier('O1_backtracking').to(device).eval()
    X, T, Q = [torch.randn(1, n, 16, device=device) for n in (12, 4, 5)]
    return model, X, T, Q


def test_local_teacher_cosine_equation_and_uniform_control():
    model, X, T, Q = fixture()
    keys, queries = model.memory.key_projection(X), model.memory.query_projection(Q)
    teacher, attention, pi = local_teacher(keys, queries, T)
    expected_pi = (F.normalize(keys, dim=-1) @ F.normalize(T, dim=-1).transpose(-1, -2) / .2).softmax(-1)
    expected_a = (F.normalize(queries, dim=-1) @ F.normalize(keys, dim=-1).transpose(-1, -2) / .2).softmax(-1)
    torch.testing.assert_close(pi, expected_pi)
    torch.testing.assert_close(attention, expected_a)
    torch.testing.assert_close(teacher, expected_a @ expected_pi)
    uniform, a, _ = local_teacher(keys, queries, T, uniform=True)
    torch.testing.assert_close(a, torch.full_like(a, 1 / X.shape[1]))
    torch.testing.assert_close(uniform, expected_pi.mean(1, keepdim=True).expand_as(uniform))


def test_query_isolation_zero_reset_vocabulary_and_frozen_parameters():
    model, X, T, Q = fixture()
    original = {k: v.clone() for k, v in model.state_dict().items()}
    with torch.no_grad():
        out = query_local_residual(model.memory, X, T, Q)
        alt = query_local_residual(model.memory, X, T.roll(1, -1), Q)
        query_local_residual(model.memory, X.flip(1), T, -Q)
        replay = query_local_residual(model.memory, X, T, Q)
    assert torch.equal(out.residual, replay.residual) and torch.equal(out.tokens, replay.tokens)
    assert not torch.equal(out.residual, alt.residual)
    assert out.diagnostics['zero_initialization'].all() and out.diagnostics['all_finite'].all()
    for j in range(Q.shape[1]):
        changed = -Q.clone()
        changed[:, j] = Q[:, j]
        isolated = query_local_residual(model.memory, X, T, changed)
        assert torch.equal(out.residual[:, j], isolated.residual[:, j])
    for k, v in model.state_dict().items():
        assert torch.equal(v.view(torch.uint8), original[k].view(torch.uint8))
    assert all(p.grad is None for p in model.parameters())


def test_independent_loss_gradient_armijo_first_acceptance_and_zero_fallback():
    model, X, T, Q = fixture()
    out = query_local_residual(model.memory, X, T, Q)
    with torch.no_grad():
        z0 = model.memory(X, T, Q, enable_ttt=False).tokens
    for j in range(Q.shape[1]):
        r = torch.zeros_like(z0[:, j:j+1], requires_grad=True)
        teacher = out.teacher[:, j:j+1]
        before = local_loss(z0[:, j:j+1]+r, T, teacher).sum()
        grad, = torch.autograd.grad(before, r)
        eta, trials, accepted = choose_armijo_step(
            lambda e: local_loss(z0[:, j:j+1]-e*grad, T, teacher).sum(), before, grad.square().sum())
        assert out.diagnostics['chosen_eta'][0, j].item() == torch.tensor(eta, dtype=Q.dtype).item()
        assert out.diagnostics['backtracking_trials'][0, j].item() == trials
        assert out.diagnostics['step_accepted'][0, j].item() == accepted
        torch.testing.assert_close(out.residual[:, j:j+1], -eta*grad, rtol=2e-5, atol=2e-7)
    bad_before = torch.full_like(out.diagnostics['inner_loss_before'], -1.)
    residual, eta, trials, accepted = local_armijo(z0, T, out.teacher, torch.ones_like(z0), bad_before)
    assert (residual == 0).all() and (eta == 0).all() and (trials == 5).all() and not accepted.any()


def test_runtime_label_independence_and_offline_scoring():
    from research_log.t011.experiment import extract_episode
    from tovd.synthetic.semantic_episodes import SemanticWorld, WorldConfig
    model, _, _, _ = fixture()
    config = json.load(open('research_log/t011/config.json'))
    world = SemanticWorld(WorldConfig())
    ep = world.episode('test', 'easy', 31415).to(next(model.parameters()).device)
    alternate = world.text[80:84].to(ep.T.device)
    first = extract_episode(model, ep, alternate, config)
    ep.labels = (ep.labels+1) % 4
    ep.query_ids.fill_(-1)
    second = extract_episode(model, ep, alternate, config)
    assert first['outputs'] == second['outputs'] and first['local'] == second['local']
    assert first['scores'] != second['scores']
    assert first['checks']['S0_bitwise_equal'] and first['checks']['S1_bitwise_equal']


def test_fixed_five_gate_arithmetic():
    from research_log.t011.summary import summarize, gates
    rows = []
    for branch in ('original_P', 'P_O0_resume', 'P_C2_warm'):
        for seed in (7, 17, 27):
            for regime in ('easy', 'hard'):
                nlls = (1., .8, .85, .87) if regime == 'hard' else (.4, .5, .43, .44)
                rows.append(dict(branch=branch, seed=seed, regime=regime,
                                 **{m+'_nll': n for m, n in zip(('S0', 'S1', 'S2', 'S3'), nlls)},
                                 **{m+'_accuracy': .7 for m in ('S0', 'S1', 'S2', 'S3')}))
    table = summarize(rows)
    assert gates(table, {'passes': True})['passes']
    for gate, scope, value in ((2, 'group/original_P/hard', .9),
                                (3, 'cell/7/original_P/hard', 1.04),
                                (4, 'cell/7/original_P/easy', .45),
                                (5, 'regime/hard', .9)):
        changed = copy.deepcopy(table)
        next(r for r in changed if r['scope'] == scope and r['method'] == 'S2')['nll'] = value
        assert not gates(changed, {'passes': True})['by_gate'][str(gate)]
    assert not gates(table, {'passes': False})['by_gate']['1']


def test_random_checkpoint_end_to_end_and_raw_receipts(tmp_path):
    import gzip
    from research_log.t011.experiment import run, fresh_id
    config = json.load(open('research_log/t011/config.json'))
    config['episodes_per_regime'] = 1
    states = []
    for seed in config['seeds']:
        torch.manual_seed(seed)
        path = tmp_path/f'{seed}.pt'
        torch.save({'state_dict': EpisodicClassifier('O1_backtracking').state_dict()}, path)
        states.append(dict(state_id=f'seed{seed}_original_P', seed=seed, branch='original_P', step=0,
                           path='research_log/remote_runs/'+path.name, sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    manifest = dict(states=states, code_hashes=[], historical_ids=[],
                    fresh_episode_ids=[fresh_id(config, s, r, 0) for s in config['seeds'] for r in ('easy', 'hard')])
    result = run(config, manifest, tmp_path, tmp_path/'result', os.environ.get('TOVD_TEST_DEVICE', 'cpu'), 'unit-random-model')
    assert result['validity']['passes'] and result['validity']['query_count'] == 48
    files = list((tmp_path/'result/records').glob('*.jsonl.gz'))
    assert len(files) == 6
    with gzip.open(files[0], 'rt') as handle:
        record = json.loads(next(handle))
    assert len(record['queries']) == 8 and len(record['local']['S2']['residual_pairwise']['cosine']) == 8
