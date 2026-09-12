"""Two separate phases: base calibration, then frozen-threshold novel validation."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
from statistics import mean

import torch

from research_log.t005.oracle_step_screen import score_output
from research_log.t007.experiment import load_model, read_json, tensor_equality
from research_log.t008.audit import compare_memory
from research_log.t009.audit import save_csv, save_json
from research_log.t009.query_analysis import offline_outcome
from tovd.synthetic.semantic_episodes import SemanticWorld, WorldConfig
from .policy import calibrate, delta_entropy, select
from .summary import METHODS, gates, summarize


def fresh_id(config, phase, seed, regime, index):
    return config[phase+'_namespace']+seed*config['seed_stride']+(config['hard_offset'] if regime == 'hard' else 0)+index


def extract_episode(model, ep, tau=None):
    X, T, Q = ep.X[None], ep.T[None], ep.Q[None]
    with torch.no_grad():
        before = model.memory(X, T, Q, enable_ttt=False)
        candidate = model(X, T, Q)
        p0 = model.logits(before.tokens, T).softmax(-1)[0].tolist()
        p1 = model.logits(candidate.tokens, T).softmax(-1)[0].tolist()
    z0, z1 = before.tokens[0].tolist(), candidate.tokens[0].tolist()
    dh = delta_entropy(p0, p1)
    selections = {m: select(p0, p1, z0, z1, t) for m, t in (('R2', tau), ('R3', 0))} if tau is not None else {}
    # Only below this point may labels enter offline scoring.
    outcomes = [offline_outcome(a, b, int(label)) for a, b, label in zip(p0, p1, ep.labels)]
    with torch.no_grad():
        historical = {'before': score_output(model, ep, before.tokens[0]), 'after': score_output(model, ep, candidate.tokens[0])}
        repeated = model(X, T, Q)
    comparison = compare_memory(candidate, repeated)
    nll_error = max(abs(mean(o[stage+'_nll'] for o in outcomes)-historical[stage]['nll']) for stage in ('before', 'after'))
    acc_error = max(abs(mean(o[stage+'_accuracy'] for o in outcomes)-historical[stage]['accuracy']) for stage in ('before', 'after'))
    assert nll_error <= 2e-6 and acc_error == 0 and comparison['bitwise_equal']
    token_error = 0.
    for m, selected in selections.items():
        assert selected == select(p0, p1, z0, z1, tau if m == 'R2' else 0)
        with torch.no_grad():
            token_prob = model.logits(torch.tensor(selected['tokens'], device=T.device, dtype=T.dtype)[None], T).softmax(-1)[0]
        expected = torch.tensor(selected['probabilities'], device=T.device, dtype=T.dtype)
        token_error = max(token_error, (token_prob-expected).abs().max().item())
    assert token_error <= 2e-6
    queries = []
    for j, o in enumerate(outcomes):
        row = {'query_index': j, 'delta_entropy': dh[j], 'before_nll': o['before_nll'], 'after_nll': o['after_nll'],
               'gain': o['before_accuracy'] == 0 and o['after_accuracy'] == 1,
               'damage': o['before_accuracy'] == 1 and o['after_accuracy'] == 0}
        if selections:
            choices = {'R0': False, 'R1': True, 'R2': selections['R2']['keep_C2'][j],
                       'R3': selections['R3']['keep_C2'][j], 'ORACLE': o['oracle_uses_C2']}
            for m, keep in choices.items():
                prefix = 'after' if keep else 'before'
                row.update({m+'_keep': keep, m+'_nll': o[prefix+'_nll'], m+'_accuracy': o[prefix+'_accuracy']})
        queries.append(row)
    return {'outputs': {'W0_probabilities': p0, 'C2_probabilities': p1, 'W0_tokens': z0, 'C2_tokens': z1,
                        'selections': selections}, 'queries': queries,
            'checks': {'normal_oracle_bitwise_equal': comparison['bitwise_equal'], 'nll_error': nll_error,
                       'accuracy_error': acc_error, 'selected_token_probability_error': token_error, 'selection_repeat_exact': True},
            'candidate_diagnostics': {k: v.item() for k, v in candidate.diagnostics.items()},
            'labels': ep.labels.tolist(), 'vocabulary_ids': ep.vocabulary_ids.tolist(), 'query_ids': ep.query_ids.tolist()}


def run(config, manifest, runs_root, output, phase, device, revision, thresholds=None, threshold_commit=None):
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    output.mkdir(parents=True, exist_ok=True)
    (output/'records').mkdir(exist_ok=True)
    source_checks = []
    paths = {}
    for s in manifest['states']:
        p = runs_root/Path(s['path']).relative_to('research_log/remote_runs')
        sha = hashlib.sha256(p.read_bytes()).hexdigest()
        source_checks.append({'state_id': s['state_id'], 'sha256': sha, 'matches': sha == s['sha256']})
        paths[s['state_id']] = p
    code_checks = [{**s, 'actual': hashlib.sha256(Path(s['path']).read_bytes()).hexdigest()} for s in manifest['code_hashes']]
    assert all(c['matches'] for c in source_checks) and all(c['actual'] == c['sha256'] for c in code_checks)
    if phase == 'validation':
        assert thresholds is not None and threshold_commit
        for seed in config['seeds']:
            t = thresholds[str(seed)]
            assert seed not in t['calibration_seeds'] and t['calibration_seeds'] == [s for s in config['seeds'] if s != seed]
    world = SemanticWorld(WorldConfig(**config['world']))
    query_rows, episode_summaries, check_rows, unchanged = [], [], [], []
    used_ids = set()
    for source in manifest['states']:
        state = torch.load(paths[source['state_id']], map_location=device, weights_only=True)['state_dict']
        model = load_model(state, 'O1_backtracking', config, device)
        tau = thresholds[str(source['seed'])]['tau'] if phase == 'validation' else None
        for regime in ('easy', 'hard'):
            records = []
            for index in range(config[phase+'_episodes']):
                eid = fresh_id(config, phase, source['seed'], regime, index)
                assert eid in manifest['fresh_episode_ids'][phase] and eid not in manifest['historical_ids']
                used_ids.add(eid)
                ep = world.episode('train' if phase == 'calibration' else 'test', regime, eid).to(device)
                r = extract_episode(model, ep, tau)
                allowed = world.train_ids.tolist() if phase == 'calibration' else world.test_ids.tolist()
                assert all(i in allowed for i in r['vocabulary_ids']+r['query_ids'])
                meta = {k: source[k] for k in ('state_id', 'seed', 'branch', 'step')}
                meta.update(phase=phase, regime=regime, index=index, episode_seed=eid)
                r.update(meta)
                records.append(r)
                query_rows.extend({**meta, **q} for q in r['queries'])
                check_rows.append({**meta, **r['checks']})
                if phase == 'validation':
                    episode_summaries.append({**meta, **{m+'_'+metric: mean(q[m+'_'+metric] for q in r['queries']) for m in METHODS for metric in ('nll', 'accuracy', 'keep')}})
            save_json(output/'records'/f"{source['state_id']}_{regime}.json", records)
        unchanged.append({'state_id': source['state_id'], **tensor_equality(model.state_dict(), state)})
        print(f"{phase.upper()} state={source['state_id']} episodes={2*config[phase+'_episodes']}", flush=True)
    assert all(s['all_tensors_byte_equal'] for s in unchanged)
    expected = len(manifest['states'])*2*config[phase+'_episodes']*config['world']['queries']
    assert len(query_rows) == expected and used_ids == set(manifest['fresh_episode_ids'][phase])
    save_csv(output/'queries.csv', query_rows)
    validity = {'passes': True, 'query_count': len(query_rows), 'episode_count': len(check_rows),
                'max_nll_error': max(r['nll_error'] for r in check_rows), 'max_accuracy_error': max(r['accuracy_error'] for r in check_rows),
                'max_selected_token_probability_error': max(r['selected_token_probability_error'] for r in check_rows),
                'normal_oracle_bitwise_equal': all(r['normal_oracle_bitwise_equal'] for r in check_rows),
                'parameters_unchanged': all(s['all_tensors_byte_equal'] for s in unchanged), 'nonoverlap': True,
                'source_checks': source_checks, 'code_checks': code_checks, 'per_episode': check_rows,
                'episode_ids': sorted(used_ids), 'threshold_commit': threshold_commit}
    result = {'phase': phase, 'validity': validity,
              'environment': {'revision': revision, 'python': platform.python_version(), 'torch': torch.__version__,
                              'cuda': torch.version.cuda, 'device': device, 'gpu': torch.cuda.get_device_name() if device.startswith('cuda') else None,
                              'time_utc': datetime.now(timezone.utc).isoformat(), 'threshold_commit': threshold_commit}, 'config': config}
    if phase == 'calibration':
        result['thresholds'] = {str(seed): calibrate(query_rows, seed, config['quantile_grid'], config['calibration_tie_tolerance']) for seed in config['seeds']}
        save_json(output/'thresholds.json', result['thresholds'])
        print('THRESHOLDS '+json.dumps({s: t['tau'] for s, t in result['thresholds'].items()}), flush=True)
    else:
        result['thresholds'] = thresholds
        result['summary'] = summarize(query_rows)
        result['gates'] = gates(result['summary'], validity['passes'])
        save_csv(output/'episodes.csv', episode_summaries)
        save_csv(output/'summary.csv', result['summary'])
        save_json(output/'gates.json', result['gates'])
        print('GATES '+json.dumps(result['gates']['by_gate']), flush=True)
    save_json(output/'results.json', result)
    save_json(output/'checks.json', validity)
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--phase', choices=('calibration', 'validation'), required=True)
    p.add_argument('--config', type=Path, default=Path('research_log/t010/config.json'))
    p.add_argument('--sources', type=Path, default=Path('research_log/t010/sources.json'))
    p.add_argument('--runs-root', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--device', default='cpu')
    p.add_argument('--revision', required=True)
    p.add_argument('--thresholds', type=Path)
    p.add_argument('--threshold-commit')
    a = p.parse_args()
    run(read_json(a.config), read_json(a.sources), a.runs_root, a.output, a.phase, a.device, a.revision,
        read_json(a.thresholds) if a.thresholds else None, a.threshold_commit)
