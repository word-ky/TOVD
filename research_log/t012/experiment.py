"""Two-phase static PoE audit; only the explicit A4 historical reference uses C2."""

import argparse
from datetime import datetime, timezone
import gzip
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
from research_log.t011.experiment import pairwise
from tovd.models.static_semantic_fusion import product_of_experts, static_evidence
from tovd.synthetic.semantic_episodes import SemanticWorld, WorldConfig
from .summary import METHODS, calibrate, gates, summarize


def fresh_id(config, phase, seed, regime, index):
    return config[phase+'_namespace']+seed*config['seed_stride']+(config['hard_offset'] if regime == 'hard' else 0)+index


def extract_episode(model, ep, config, phase, exponent=None, b1=None):
    X, T, Q = ep.X[None], ep.T[None], ep.Q[None]
    kwargs = {k: config[k] for k in ('teacher_tau', 'tau_q')}
    evidence = static_evidence(model, X, T, Q, **kwargs)
    with torch.inference_mode():
        outputs = {'A0': dict(probabilities=evidence['p0'], log_probabilities=evidence['log_p0'])}
        if phase == 'calibration':
            outputs.update({f'lambda_{i}': product_of_experts(evidence['p0'], evidence['teacher'], value, config['epsilon'])
                            for i, value in enumerate(config['lambda_grid'])})
        else:
            outputs['A2'] = product_of_experts(evidence['p0'], evidence['teacher'], exponent, config['epsilon'])
            outputs['A3'] = product_of_experts(evidence['p0'], evidence['uniform_teacher'], exponent, config['epsilon'])
            activation = b1(X, T, Q)
            logits = b1.logits(activation.tokens, T)
            outputs['A1'] = dict(probabilities=logits.softmax(-1), log_probabilities=logits.log_softmax(-1))
        static = model.memory(X, T, Q, enable_ttt=False)
        exact_a0 = torch.equal(evidence['tokens'], static.tokens) and torch.equal(evidence['p0'], model.logits(static.tokens, T).softmax(-1))
        static_evidence(model, -X, T, -Q, **kwargs)
        repeated = static_evidence(model, X, T, Q, **kwargs)
        checks = dict(A0_bitwise_equal=exact_a0, static_replay_exact=all(torch.equal(v, repeated[k]) for k, v in evidence.items()),
                      inference_tensors=all(torch.is_inference(t) and not t.requires_grad for o in outputs.values() for t in o.values()),
                      all_parameter_grads_none=all(p.grad is None for p in model.parameters()))
        if phase == 'validation':
            checks['A1_bitwise_equal'] = compare_memory(activation, b1(X, T, Q))['bitwise_equal']
        entropy = -(evidence['attention']*evidence['attention'].clamp_min(1e-12).log()).sum(-1)[0]
        diagnostics = dict(attention_entropy=entropy.tolist(), effective_token_count=entropy.exp().tolist(),
                           teacher_pairwise=pairwise(evidence['teacher'][0]),
                           uniform_teacher_pairwise=pairwise(evidence['uniform_teacher'][0]))
        if phase == 'validation':
            p2, p3 = (outputs[m]['probabilities'][0] for m in ('A2', 'A3'))
            diagnostics.update(A2_A3_L1=(p2-p3).abs().sum(-1).tolist(),
                               A2_A3_KL=(p2*(outputs['A2']['log_probabilities'][0]-outputs['A3']['log_probabilities'][0])).sum(-1).tolist(),
                               A2_A3_class_different=(p2.argmax(-1) != p3.argmax(-1)).tolist())
    historical = {}
    if phase == 'validation':
        # The only inner gradient in this audit is the separately mandated historical reference.
        with torch.no_grad():
            c2 = model(X, T, Q)
            logits = model.logits(c2.tokens, T)
            outputs['A4'] = dict(probabilities=logits.softmax(-1), log_probabilities=logits.log_softmax(-1))
            checks['A4_bitwise_equal'] = compare_memory(c2, model(X, T, Q))['bitwise_equal']
            historical['A4_diagnostics'] = {k: v.item() for k, v in c2.diagnostics.items()}
    checks['all_outputs_finite'] = all(torch.isfinite(t).all().item() for out in outputs.values() for t in out.values())
    # All runtime results/diagnostics have been computed. Labels enter only here.
    queries = []
    for j, label in enumerate(ep.labels.tolist()):
        row = dict(query_index=j)
        for method, out in outputs.items():
            row[method+'_nll'] = -out['log_probabilities'][0, j, label].item()
            row[method+'_accuracy'] = float(out['probabilities'][0, j].argmax().item() == label)
        row.update(attention_entropy=diagnostics['attention_entropy'][j], effective_token_count=diagnostics['effective_token_count'][j])
        if phase == 'validation':
            row.update({k: diagnostics[k][j] for k in ('A2_A3_L1', 'A2_A3_KL', 'A2_A3_class_different')})
        queries.append(row)
    with torch.no_grad():
        scores = {'A0': score_output(model, ep, static.tokens[0])}
        if phase == 'validation':
            scores.update(A1=score_output(b1, ep, activation.tokens[0]), A4=score_output(model, ep, c2.tokens[0]))
    checks['max_historical_nll_error'] = max(abs(mean(q[m+'_nll'] for q in queries)-s['nll']) for m, s in scores.items())
    checks['max_historical_accuracy_error'] = max(abs(mean(q[m+'_accuracy'] for q in queries)-s['accuracy']) for m, s in scores.items())
    # Calibration probabilities are recoverable from p0, teacher and the fixed grid;
    # retain every grid loss but avoid duplicating seven prediction arrays.
    raw_outputs = outputs if phase == 'validation' else {'A0': outputs['A0']}
    return dict(outputs={m: {k: v[0].tolist() for k, v in o.items()} for m, o in raw_outputs.items()},
                evidence={k: evidence[k][0].tolist() for k in ('p0', 'teacher', 'uniform_teacher', 'attention', 'token_teacher')},
                queries=queries, diagnostics=diagnostics, checks=checks, historical=historical,
                labels=ep.labels.tolist(), vocabulary_ids=ep.vocabulary_ids.tolist(), query_ids=ep.query_ids.tolist())


def run(config, manifest, runs_root, output, phase, device, revision, implementation_hashes=(), frozen=None, lambda_commit=None):
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    output.mkdir(parents=True, exist_ok=True)
    (output/'records').mkdir(exist_ok=True)
    sources, paths = [], {}
    for source in manifest['states']:
        path = runs_root/Path(source['path']).relative_to('research_log/remote_runs')
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        sources.append(dict(state_id=source['state_id'], sha256=sha, matches=sha == source['sha256']))
        paths[source['state_id']] = path
    code_checks = [{**s, 'actual': hashlib.sha256(Path(s['path']).read_bytes()).hexdigest()}
                   for s in [*manifest['code_hashes'], *implementation_hashes]]
    assert all(s['matches'] for s in sources) and all(s['actual'] == s['sha256'] for s in code_checks)
    if phase == 'validation':
        assert frozen['phase'] == 'calibration' and lambda_commit
        assert not set(frozen['episode_ids']) & set(manifest['fresh_episode_ids']['validation'])
    exponent = frozen['exponent'] if phase == 'validation' else None
    world = SemanticWorld(WorldConfig(**config['world']))
    queries, episodes, checks, unchanged, ids = [], [], [], [], set()
    for source in manifest['states']:
        state = torch.load(paths[source['state_id']], map_location=device, weights_only=True)['state_dict']
        model = load_model(state, 'O1_backtracking', config, device)
        b1 = load_model(state, 'B1', config, device) if phase == 'validation' else None
        for regime in ('easy', 'hard'):
            with gzip.open(output/'records'/f"{source['state_id']}_{regime}.jsonl.gz", 'wt', encoding='utf-8') as handle:
                for index in range(config[phase+'_episodes']):
                    eid = fresh_id(config, phase, source['seed'], regime, index)
                    assert eid in manifest['fresh_episode_ids'][phase] and eid not in manifest['historical_ids']
                    ids.add(eid)
                    ep = world.episode('train' if phase == 'calibration' else 'test', regime, eid).to(device)
                    r = extract_episode(model, ep, config, phase, exponent, b1)
                    allowed = world.train_ids.tolist() if phase == 'calibration' else world.test_ids.tolist()
                    assert all(i in allowed for i in r['vocabulary_ids']+r['query_ids'])
                    meta = {k: source[k] for k in ('state_id', 'seed', 'branch', 'step')}
                    meta.update(phase=phase, regime=regime, episode_seed=eid, index=index)
                    r.update(meta, exponent=exponent)
                    handle.write(json.dumps(r, separators=(',', ':'), allow_nan=False)+'\n')
                    queries.extend({**meta, **q} for q in r['queries'])
                    checks.append({**meta, **r['checks']})
                    if phase == 'validation':
                        row = {**meta, **{m+'_'+metric: mean(q[m+'_'+metric] for q in r['queries'])
                                         for m in METHODS for metric in ('nll', 'accuracy')}}
                        row.update({k: mean(q[k] for q in r['queries']) for k in ('attention_entropy', 'effective_token_count', 'A2_A3_L1', 'A2_A3_KL', 'A2_A3_class_different')})
                        row.update(teacher_diversity=r['diagnostics']['teacher_pairwise']['diversity'],
                                   uniform_teacher_diversity=r['diagnostics']['uniform_teacher_pairwise']['diversity'])
                        episodes.append(row)
        unchanged.append(dict(state_id=source['state_id'], **tensor_equality(model.state_dict(), state),
                              B1_byte_equal=tensor_equality(b1.state_dict(), state)['all_tensors_byte_equal'] if b1 else True,
                              grads_none=all(p.grad is None for m in (model, b1) if m for p in m.parameters())))
        print(f"{phase.upper()} state={source['state_id']} episodes={2*config[phase+'_episodes']}", flush=True)
    validity = dict(source_checks=sources, code_checks=code_checks, unchanged=unchanged,
                    episode_ids=sorted(ids), episode_count=len(checks), query_count=len(queries),
                    A0_bitwise_equal=all(c['A0_bitwise_equal'] for c in checks),
                    static_replay_exact=all(c['static_replay_exact'] for c in checks),
                    static_inference_tensors=all(c['inference_tensors'] for c in checks),
                    all_outputs_finite=all(c['all_outputs_finite'] for c in checks),
                    max_historical_nll_error=max(c['max_historical_nll_error'] for c in checks),
                    max_historical_accuracy_error=max(c['max_historical_accuracy_error'] for c in checks),
                    parameters_unchanged=all(c['all_tensors_byte_equal'] and c['B1_byte_equal'] for c in unchanged),
                    parameter_grads_none=all(c['grads_none'] for c in unchanged), lambda_commit=lambda_commit)
    if phase == 'validation':
        validity.update(A1_bitwise_equal=all(c['A1_bitwise_equal'] for c in checks), A4_bitwise_equal=all(c['A4_bitwise_equal'] for c in checks))
    validity['passes'] = (all(validity[k] for k in ('A0_bitwise_equal', 'static_replay_exact', 'static_inference_tensors', 'all_outputs_finite', 'parameters_unchanged', 'parameter_grads_none'))
                          and validity['max_historical_nll_error'] <= 2e-6 and validity['max_historical_accuracy_error'] == 0
                          and ids == set(manifest['fresh_episode_ids'][phase])
                          and len(checks) == len(manifest['states'])*2*config[phase+'_episodes']
                          and (phase == 'calibration' or validity['A1_bitwise_equal'] and validity['A4_bitwise_equal']))
    result = dict(phase=phase, config=config, validity=validity,
                  environment=dict(revision=revision, python=platform.python_version(), torch=torch.__version__, cuda=torch.version.cuda,
                                   device=device, gpu=torch.cuda.get_device_name() if device.startswith('cuda') else None,
                                   time_utc=datetime.now(timezone.utc).isoformat(), lambda_commit=lambda_commit))
    if phase == 'calibration':
        result['frozen_lambda'] = calibrate(queries, config['lambda_grid'], config['calibration_tie_tolerance'])
        save_json(output/'frozen_lambda.json', result['frozen_lambda'])
        print('GLOBAL_LAMBDA '+json.dumps(result['frozen_lambda']['exponent']), flush=True)
    else:
        result['frozen_lambda'] = frozen
        result['summary'] = summarize(episodes)
        result['gates'] = gates(result['summary'], validity['passes'], config['strict_improvement_tolerance'])
        save_csv(output/'episodes.csv', episodes)
        save_csv(output/'summary.csv', result['summary'])
        save_json(output/'gates.json', result['gates'])
        print('GATES '+json.dumps(result['gates']['by_gate']), flush=True)
    save_csv(output/'queries.csv', queries)
    save_json(output/'checks.json', dict(validity=validity, per_episode=checks))
    save_json(output/'results.json', result)
    assert validity['passes']
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--phase', choices=('calibration', 'validation'), required=True)
    parser.add_argument('--runs-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--device', default='cpu')
    parser.add_argument('--revision', required=True)
    parser.add_argument('--frozen-lambda', type=Path)
    parser.add_argument('--lambda-commit')
    args = parser.parse_args()
    run(read_json(Path('research_log/t012/config.json')), read_json(Path('research_log/t012/sources.json')),
        args.runs_root, args.output, args.phase, args.device, args.revision,
        read_json(Path('research_log/t012/implementation_hashes.json')),
        read_json(args.frozen_lambda) if args.frozen_lambda else None, args.lambda_commit)
