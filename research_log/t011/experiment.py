"""Frozen nine-state QLSR screen. Labels are used only after runtime/audits."""

import argparse
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import platform
from statistics import mean

import torch
from torch.nn import functional as F

from research_log.t005.oracle_step_screen import score_output
from research_log.t007.experiment import load_model, read_json, tensor_equality
from research_log.t008.audit import compare_memory
from research_log.t009.audit import save_csv, save_json
from tovd.models.query_local_residual import query_local_residual
from tovd.synthetic.semantic_episodes import SemanticWorld, WorldConfig
from .summary import METHODS, gates, summarize


def fresh_id(config, seed, regime, index):
    return config['namespace']+seed*config['seed_stride']+(config['hard_offset'] if regime == 'hard' else 0)+index


def pairwise(vectors):
    unit = F.normalize(vectors, dim=-1, eps=1e-12)
    cosine = unit @ unit.T
    good = vectors.norm(dim=-1) > 1e-12
    pairs = torch.triu(good[:, None] & good[None, :], diagonal=1)
    count = pairs.sum().item()
    return dict(cosine=cosine.tolist(), eligible_pairs=count,
                diversity=(1-cosine[pairs]).mean().item() if count else 0.)


def residual_equal(first, second):
    return (torch.equal(first.tokens, second.tokens) and torch.equal(first.residual, second.residual)
            and all(torch.equal(v, second.diagnostics[k]) for k, v in first.diagnostics.items()))


def extract_episode(model, ep, alternate_text, config):
    X, T, Q = ep.X[None], ep.T[None], ep.Q[None]
    kwargs = {k: config[k] for k in ('tau_q', 'teacher_tau', 'student_tau')}
    with torch.no_grad():
        static = model.memory(X, T, Q, enable_ttt=False)
        global_candidate = model(X, T, Q)
        local = {method: query_local_residual(model.memory, X, T, Q, uniform=method == 'S3', **kwargs)
                 for method in ('S2', 'S3')}
        tokens = dict(S0=static.tokens, S1=global_candidate.tokens, **{m: out.tokens for m, out in local.items()})
        probabilities = {m: model.logits(z, T).softmax(-1)[0] for m, z in tokens.items()}
        details = {}
        for method, out in local.items():
            uniform = method == 'S3'
            changed_vocab = query_local_residual(model.memory, X, alternate_text[None], Q, uniform=uniform, **kwargs)
            # Interleave a different image; each subsequent call allocates fresh zero residuals.
            query_local_residual(model.memory, X.flip(1), T, -Q, uniform=uniform, **kwargs)
            replay = query_local_residual(model.memory, X, T, Q, uniform=uniform, **kwargs)
            isolation = []
            for j in range(Q.shape[1]):
                changed_q = -Q.clone()
                changed_q[:, j] = Q[:, j]
                single = query_local_residual(model.memory, X, T, changed_q, uniform=uniform, **kwargs)
                isolation.append(torch.equal(single.residual[:, j], out.residual[:, j])
                                 and torch.equal(single.tokens[:, j], out.tokens[:, j]))
            d = {k: v[0].tolist() for k, v in out.diagnostics.items()}
            d['vocabulary_residual_difference'] = (out.residual-changed_vocab.residual).norm(dim=-1)[0].tolist()
            d['query_isolation_exact'] = isolation
            d['replay_image_vocabulary_reset_exact'] = [residual_equal(out, replay)] * Q.shape[1]
            details[method] = dict(diagnostics=d, residual=out.residual[0].tolist(),
                                   teacher=out.teacher[0].tolist(), attention=out.attention[0].tolist(),
                                   token_teacher=out.token_teacher[0].tolist(),
                                   residual_pairwise=pairwise(out.residual[0]),
                                   teacher_pairwise=pairwise(out.teacher[0]))
        static_replay = model.memory(X, T, Q, enable_ttt=False)
        global_replay = model(X, T, Q)
        checks = dict(S0_bitwise_equal=compare_memory(static, static_replay)['bitwise_equal'],
                      S1_bitwise_equal=compare_memory(global_candidate, global_replay)['bitwise_equal'],
                      all_probabilities_finite=all(torch.isfinite(p).all().item() for p in probabilities.values()))
    # Runtime, selection, and mechanism audits are complete. Only now read labels.
    with torch.no_grad():
        scores = {m: score_output(model, ep, z[0]) for m, z in tokens.items()}
    queries = []
    for j, label in enumerate(ep.labels.tolist()):
        row = {'query_index': j}
        for m in METHODS:
            row[m+'_nll'] = scores[m]['query_nll'][j]
            row[m+'_accuracy'] = float(probabilities[m][j].argmax().item() == label)
        for m in ('S2', 'S3'):
            row.update({m+'_'+k: v[j] for k, v in details[m]['diagnostics'].items()})
        queries.append(row)
    checks['max_score_nll_error'] = max(abs(mean(q[m+'_nll'] for q in queries)-scores[m]['nll']) for m in METHODS)
    checks['max_score_accuracy_error'] = max(abs(mean(q[m+'_accuracy'] for q in queries)-scores[m]['accuracy']) for m in METHODS)
    return dict(outputs={m: dict(tokens=tokens[m][0].tolist(), probabilities=probabilities[m].tolist()) for m in METHODS},
                local=details, global_diagnostics={k: v.item() for k, v in global_candidate.diagnostics.items()},
                queries=queries, checks=checks, labels=ep.labels.tolist(), vocabulary_ids=ep.vocabulary_ids.tolist(),
                query_ids=ep.query_ids.tolist(), scores=scores)


def mechanism_summary(episodes, queries, config):
    result = {}
    for m in ('S2', 'S3'):
        accepted = [q for q in queries if q[m+'_step_accepted']]
        result[m] = dict(accepted_count=len(accepted), acceptance_fraction=len(accepted)/len(queries),
                         residual_diversity=mean(e[m+'_diversity'] for e in episodes),
                         teacher_diversity=mean(e[m+'_teacher_diversity'] for e in episodes),
                         eligible_pairs=mean(e[m+'_eligible_pairs'] for e in episodes),
                         **{k: mean(q[m+'_'+k] for q in queries) for k in (
                             'inner_loss_before', 'inner_loss_after', 'inner_gradient_norm', 'chosen_eta',
                             'backtracking_trials', 'residual_norm', 'normalized_residual_norm',
                             'attention_entropy', 'effective_token_count', 'vocabulary_residual_difference')},
                         all_finite=all(q[m+'_all_finite'] for q in queries),
                         all_zero_init=all(q[m+'_zero_initialization'] for q in queries),
                         all_exact_reset=all(q[m+'_replay_image_vocabulary_reset_exact'] for q in queries),
                         all_query_isolation=all(q[m+'_query_isolation_exact'] for q in queries),
                         accepted_nonzero=bool(accepted) and all(q[m+'_residual_norm'] > 0 for q in accepted),
                         accepted_vocabulary_sensitive=bool(accepted) and all(q[m+'_vocabulary_residual_difference'] > config['vocabulary_difference_min'] for q in accepted),
                         min_accepted_vocabulary_difference=min((q[m+'_vocabulary_residual_difference'] for q in accepted), default=0.))
    a, b = result['S2'], result['S3']
    difference = a['residual_diversity']-b['residual_diversity']
    passes = all(a[k] for k in ('all_finite', 'all_zero_init', 'all_exact_reset', 'all_query_isolation',
                                'accepted_nonzero', 'accepted_vocabulary_sensitive'))
    passes = passes and a['residual_diversity'] > config['diversity_min'] and difference >= config['diversity_excess_min']
    return dict(passes=passes, S2=result['S2'], S3=result['S3'], residual_diversity_excess=difference)


def run(config, manifest, runs_root, output, device, revision, implementation_hashes=()):
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    output.mkdir(parents=True, exist_ok=True)
    (output/'records').mkdir(exist_ok=True)
    source_checks, paths = [], {}
    for s in manifest['states']:
        path = runs_root/Path(s['path']).relative_to('research_log/remote_runs')
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        source_checks.append(dict(state_id=s['state_id'], sha256=sha, matches=sha == s['sha256']))
        paths[s['state_id']] = path
    code_checks = [{**s, 'actual': hashlib.sha256(Path(s['path']).read_bytes()).hexdigest()}
                   for s in [*manifest['code_hashes'], *implementation_hashes]]
    assert all(c['matches'] for c in source_checks) and all(c['actual'] == c['sha256'] for c in code_checks)
    world = SemanticWorld(WorldConfig(**config['world']))
    episodes, queries, checks, unchanged, ids = [], [], [], [], set()
    for s in manifest['states']:
        state = torch.load(paths[s['state_id']], weights_only=True, map_location=device)['state_dict']
        model = load_model(state, 'O1_backtracking', config, device)
        for regime in ('easy', 'hard'):
            record_path = output/'records'/f"{s['state_id']}_{regime}.jsonl.gz"
            with gzip.open(record_path, 'wt', encoding='utf-8') as record_file:
                for index in range(config['episodes_per_regime']):
                    eid = fresh_id(config, s['seed'], regime, index)
                    assert eid in manifest['fresh_episode_ids'] and eid not in manifest['historical_ids']
                    ids.add(eid)
                    ep = world.episode('test', regime, eid).to(device)
                    novel_start = int(world.test_ids[0])
                    alt_ids = novel_start + (ep.vocabulary_ids.cpu()-novel_start+1) % len(world.test_ids)
                    alternate_text = world.text[alt_ids].to(device)
                    r = extract_episode(model, ep, alternate_text, config)
                    meta = {k: s[k] for k in ('state_id', 'seed', 'branch', 'step')}
                    meta.update(regime=regime, index=index, episode_seed=eid)
                    r.update(meta, alternate_vocabulary_ids=alt_ids.tolist())
                    record_file.write(json.dumps(r, separators=(',', ':'), allow_nan=False)+'\n')
                    queries.extend({**meta, **q} for q in r['queries'])
                    row = {**meta, **{m+'_'+metric: mean(q[m+'_'+metric] for q in r['queries'])
                                      for m in METHODS for metric in ('nll', 'accuracy')}}
                    for m in ('S2', 'S3'):
                        row.update({m+'_diversity': r['local'][m]['residual_pairwise']['diversity'],
                                    m+'_eligible_pairs': r['local'][m]['residual_pairwise']['eligible_pairs'],
                                    m+'_teacher_diversity': r['local'][m]['teacher_pairwise']['diversity']})
                    episodes.append(row)
                    checks.append({**meta, **r['checks']})
        unchanged.append(dict(state_id=s['state_id'], **tensor_equality(model.state_dict(), state)))
        print(f"SCREEN state={s['state_id']} episodes={2*config['episodes_per_regime']}", flush=True)
    mechanism = mechanism_summary(episodes, queries, config)
    validity = dict(source_checks=source_checks, code_checks=code_checks, unchanged=unchanged,
                    episode_ids=sorted(ids), episode_count=len(episodes), query_count=len(queries),
                    S0_S1_bitwise_equal=all(c['S0_bitwise_equal'] and c['S1_bitwise_equal'] for c in checks),
                    all_probabilities_finite=all(c['all_probabilities_finite'] for c in checks),
                    max_score_nll_error=max(c['max_score_nll_error'] for c in checks),
                    max_score_accuracy_error=max(c['max_score_accuracy_error'] for c in checks),
                    parameters_unchanged=all(u['all_tensors_byte_equal'] for u in unchanged),
                    exact_resets=all(mechanism[m]['all_exact_reset'] and mechanism[m]['all_query_isolation'] and mechanism[m]['all_zero_init'] for m in ('S2', 'S3')))
    validity['passes'] = (validity['S0_S1_bitwise_equal'] and validity['all_probabilities_finite'] and
                          validity['max_score_nll_error'] <= 2e-6 and validity['max_score_accuracy_error'] == 0 and
                          validity['parameters_unchanged'] and validity['exact_resets'] and
                          all(mechanism[m]['all_finite'] for m in ('S2', 'S3')) and
                          ids == set(manifest['fresh_episode_ids']) and len(episodes) == len(manifest['states'])*2*config['episodes_per_regime'])
    table = summarize(episodes)
    interpretation = gates(table, mechanism)
    result = dict(config=config, validity=validity, mechanism=mechanism, summary=table, gates=interpretation,
                  environment=dict(revision=revision, python=platform.python_version(), torch=torch.__version__, cuda=torch.version.cuda,
                                   device=device, gpu=torch.cuda.get_device_name() if device.startswith('cuda') else None,
                                   time_utc=datetime.now(timezone.utc).isoformat()))
    save_csv(output/'episodes.csv', episodes)
    save_csv(output/'queries.csv', queries)
    save_csv(output/'summary.csv', table)
    save_json(output/'checks.json', dict(validity=validity, per_episode=checks))
    save_json(output/'results.json', result)
    save_json(output/'gates.json', interpretation)
    print('GATES '+json.dumps(interpretation['by_gate'])+' VALIDITY '+str(validity['passes']), flush=True)
    assert validity['passes']
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--runs-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--device', default='cpu')
    parser.add_argument('--revision', required=True)
    args = parser.parse_args()
    run(read_json(Path('research_log/t011/config.json')), read_json(Path('research_log/t011/sources.json')),
        args.runs_root, args.output, args.device, args.revision,
        read_json(Path('research_log/t011/implementation_hashes.json')))
