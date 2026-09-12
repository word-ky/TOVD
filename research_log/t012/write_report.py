"""Pure rendering of completed calibration/validation receipts; no Torch imports."""

import argparse
from collections import defaultdict
import csv
import gzip
import hashlib
import json
from pathlib import Path
import re
import shutil
from statistics import mean

from research_log.t011.write_report import table, save_json


def receipt(run, phase):
    root = run/('artifacts/t012_'+phase)
    result = json.loads((root/'results.json').read_text(encoding='utf-8'))
    count, queries = 0, 0
    for path in sorted((root/'records').glob('*.jsonl.gz')):
        with gzip.open(path, 'rt', encoding='utf-8') as handle:
            for line in handle:
                record = json.loads(line)
                count += 1
                queries += len(record['queries'])
    assert count == result['validity']['episode_count'] and queries == result['validity']['query_count']
    log = (run/'train.log').read_text(encoding='utf-8')
    record = dict(run_id=run.name, phase=phase, episode_count=count, query_count=queries,
                  tests=[dict(passed=int(n), seconds=float(s)) for n, s in re.findall(r'(\d+) passed[^\n]*?in ([\d.]+)s', log)],
                  started_at=re.search(r'started_at=(.*)', log).group(1),
                  finished_at=re.search(r'finished_at=(.*)', log).group(1),
                  exit_code=int(re.search(r'exit_code=(\d+)', log).group(1)), environment=result['environment'])
    manifest = [dict(path=p.as_posix(), bytes=p.stat().st_size, sha256=hashlib.sha256(p.read_bytes()).hexdigest())
                for p in sorted(run.rglob('*')) if p.is_file()]
    return root, result, record, manifest


def plot(root, summary, exponent):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    lookup = {(r['scope'], r['method']): r for r in summary}
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), layout='constrained')
    branches = ('original_P', 'P_O0_resume', 'P_C2_warm')
    methods = (('A1', 'B1 activation', '#b59966'), ('A2', 'Static local PoE', '#267a80'),
               ('A3', 'Static uniform PoE', '#bd714d'), ('A4', 'C2 historical only', '#8a929d'))
    for ax, regime in zip(axes, ('hard', 'easy')):
        for i, (method, label, color) in enumerate(methods):
            gain = [lookup[('group/'+b+'/'+regime, 'A0')]['nll']-lookup[('group/'+b+'/'+regime, method)]['nll'] for b in branches]
            ax.bar([j+(i-1.5)*.19 for j in range(3)], gain, width=.18, color=color, label=label)
        ax.axhline(0, color='black', linewidth=.8)
        ax.set_xticks(range(3), ['Original P', 'W1 final', 'W2 final'])
        ax.set_title(regime.capitalize()+' novel episodes')
        ax.set_ylabel('NLL improvement over W0 (nats)')
        ax.spines[['top', 'right']].set_visible(False)
        ax.grid(axis='y', alpha=.16)
    axes[0].legend(fontsize=8)
    fig.suptitle(f'T012 static fusion, one base-calibrated exponent = {exponent:g}')
    fig.savefig(root/'performance.png', dpi=180)
    fig.savefig(root/'performance.svg')
    plt.close(fig)
    svg = root/'performance.svg'
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text(encoding='utf-8').splitlines())+'\n', encoding='utf-8')


def synthesis(root, validation):
    overall = {r['method']: r for r in validation['summary'] if r['scope'] == 'overall'}
    lines = ['# TOVD synthetic-program research synthesis', '',
             'The fixed T012 success criterion fails. Per the active task stop rule, engineering stops the synthetic TOVD mechanism program here and submits this synthesis for Research Lead review. No successor mechanism or detector integration is proposed or launched.', '',
             '## Evidence that remains valid', '',
             '- T001 established vocabulary-dependent fast state, exact episodic reset and an outer-gradient path. These are mechanism/implementation facts, not detection utility.',
             '- T005 found a useful frozen-checkpoint O1+C2 update: hard accuracy 40.54% to 46.25%, NLL 1.31390 to 1.23536; easy accuracy 77.58% to 86.71%. This positive result is preserved with its original state/stream scope.',
             '- T009 found query-level harm ranking: delta-entropy LOSO AUROC mean .750696, minimum .722485, with offline oracle headroom. Ranking and an oracle are not deployable decision rules.', '',
             'Sources: [Research Lead review ledger](../../coordination/CHATGPT_REVIEW_LOG.md), [T005](../t005/RESULTS.md), [T009](../t009/RESULTS.md).', '',
             '## Where the proposed route failed', '',
             '- T002–T004 separated a well-formed semantic inner loop from downstream task alignment; improving the inner target was necessary to obtain the later frozen T005 effect.',
             '- T006 lost absolute competitiveness under random-init C2 meta-training. T007 matched warm continuation still did not establish a stable successor and retained substantial easy-state regressions.',
             '- T008 episode-level scalar harm observability failed; T009 localized the observable ranking signal to queries, but did not itself establish selection transfer.',
             '- T010 froze actual base-calibrated thresholds before fresh novel validation. It removed many damaging updates but discarded most useful hard corrections: original/W1/W2 hard NLL-gain retention 47.56%/-4.79%/2.44%.',
             '- T011 changed the fast state to an independent zero-initialized query residual. Inner descent and reset remained healthy, yet all five criteria failed; pooled accuracy fell from 59.79% W0 to 29.83%. Local teacher variation did not produce the required residual-localization advantage.',
             f"- T012 removed test-time state updates altogether and froze a single base-calibrated PoE exponent {validation['frozen_lambda']['exponent']:g}. The fixed novel-stream criterion still fails; gates are {validation['gates']['by_gate']}. Overall A0/A2 NLL {overall['A0']['nll']:.6f}/{overall['A2']['nll']:.6f}, accuracy {100*overall['A0']['accuracy']:.4f}%/{100*overall['A2']['accuracy']:.4f}%. Exact per-group/seed evidence is in RESULTS.md and gates.json.", '',
             'Sources: [T006](../t006/RESULTS.md), [T007](../t007/RESULTS.md), [T008](../t008/RESULTS.md), [T010](../t010/RESULTS.md), [T011](../t011/RESULTS.md), [T012](RESULTS.md).', '',
             '## What this supports, and what it does not', '',
             'The tested vocabulary evidence can change representations and predict some harm, but the program did not establish the required combination of novel hard utility, cross-seed consistency and easy safety. Successful local-objective descent, nonzero state changes, or an AUROC ranking alone are insufficient to support the original task-utility thesis. Freezing slow weights and using feed-forward fusion does not itself guarantee a beneficial decision boundary.', '',
             'The conclusion is bounded to the specified synthetic world, source checkpoints, adaptation/fusion formulas and preregistered streams. Several states share training history; fresh episodes do not create independent semantic worlds. These experiments do not prove that every possible OVD method or static fusion is ineffective, and they contain no detector results. In particular, T005 and T009 remain valid scoped positives.', '',
             'Archive the complete positive and negative evidence, keep the executed code and frozen calibration receipts, and wait for Research Lead review. Do not turn this synthesis into a new synthetic objective, gate, controller, exponent search or fast-state architecture.', '']
    (root/'SYNTHESIS.md').write_text('\n'.join(lines), encoding='utf-8')


def main(cal_run, val_run=None):
    root = Path('research_log/t012')
    cal_root, cal, cal_receipt, cal_manifest = receipt(cal_run, 'calibration')
    shutil.copyfile(cal_root/'frozen_lambda.json', root/'frozen_lambda.json')
    save_json(root/'calibration_receipt.json', cal_receipt)
    save_json(root/'calibration_manifest.json', cal_manifest)
    frozen = cal['frozen_lambda']
    lines = ['# T012 static activation-side reduction audit', '',
             f"Calibration run `{cal_run.name}`. Tested implementation `{cal['environment']['revision']}`; preregistration `15d3353`.",
             f"One global lambda = **{frozen['exponent']:g}**, chosen from {frozen['query_count']} fresh base queries across all nine states. This value is shared across seeds, states and regimes.", '',
             table(['Lambda', 'Base calibration NLL', 'Accuracy %'], [(c['exponent'], f"{c['nll']:.9f}", f"{100*c['accuracy']:.5f}") for c in frozen['candidates']]), '',
             f"Base W0 NLL {frozen['base_A0_nll']:.9f}. Selection minimizes global base NLL; ties within1e-12 use the smallest exponent. No novel outcomes enter calibration.", '']
    if val_run is None:
        lines += ['Novel evaluation has not run. Commit and push the actual frozen_lambda.json and this complete calibration receipt before deploying the novel phase.',
                  f"Calibration engineering validity: {cal['validity']['passes']}. CPU/CUDA test receipts: {cal_receipt['tests']}.", '']
        (root/'CALIBRATION.md').write_text('\n'.join(lines), encoding='utf-8')
        return
    val_root, val, val_receipt, val_manifest = receipt(val_run, 'validation')
    assert val['frozen_lambda'] == frozen
    save_json(root/'validation_receipt.json', val_receipt)
    save_json(root/'artifact_manifest.json', cal_manifest+val_manifest)
    save_json(root/'verification.json', dict(calibration=cal['validity'], validation=val['validity'], identical_frozen_lambda=True))
    for filename in ('summary.csv', 'gates.json'):
        shutil.copyfile(val_root/filename, root/filename)
    groups = defaultdict(list)
    with (val_root/'episodes.csv').open(encoding='utf-8') as handle:
        for r in csv.DictReader(handle):
            groups[(r['seed'], r['branch'], r['regime'])].append(r)
    diagnostics = [dict(seed=s, branch=b, regime=r,
                        **{k: mean(float(row[k]) for row in rows) for k in ('attention_entropy', 'effective_token_count', 'A2_A3_L1', 'A2_A3_KL', 'A2_A3_class_different', 'teacher_diversity', 'uniform_teacher_diversity')})
                   for (s, b, r), rows in groups.items()]
    with (root/'localization.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(diagnostics[0]))
        writer.writeheader()
        writer.writerows(diagnostics)
    gates, validity = val['gates'], val['validity']
    conclusion = ('All five gates pass: recommend a separate static detector-facing design, then stop for Research Lead review.' if gates['passes'] else
                  'The fixed success criterion fails. Stop the synthetic TOVD mechanism program and submit SYNTHESIS.md for Research Lead review; no further mechanism or detector work.')
    lines = ['# T012 final result', '', conclusion, '']+lines[2:]
    lines += [f"Novel run `{val_run.name}`, actual-lambda freeze commit `{validity['lambda_commit']}`. 1,800 fresh novel episodes /14,400 queries; 600 unique scene seeds paired across nine frozen states. Calibration and novel namespaces are 4 billion and 5 billion, disjoint from T002–T011.", '',
              '## Fixed gates', '', table(['Gate', 'Result'], [(k, 'PASS' if v else 'FAIL') for k, v in gates['by_gate'].items()]), '',
              table(['Scope', 'Gate', 'A2-A0 NLL', 'Accuracy change pp', 'Pass'], [(c['scope'], c['gate'], f"{c['A2_minus_A0_nll']:.9f}", f"{c['accuracy_delta_pp']:.5f}", c['passes']) for c in gates['clauses'] if c['gate'] in (1, 3)]), '',
              table(['Group', 'Improving hard seeds', 'Worst NLL regression'], [(c['scope'], c['improved_seeds'], f"{c['worst_nll_regression']:.9f}") for c in gates['clauses'] if c['gate'] == 2]), '',
              'Localization: '+', '.join(f"{k}={c[k]:.9f}" for c in gates['clauses'] if c['gate'] == 4 for k in ('A2_minus_A3_hard_nll', 'A2_minus_A3_easy_nll'))+'.',
              'Strict improvement comparisons use the preregistered1e-6-nat numerical tolerance; the full signed deltas and five clauses are in gates.json.', '',
              '## Complete controls', '',
              table(['Scope', 'Method', 'Accuracy %', 'NLL'], [(r['scope'], r['method'], f"{100*r['accuracy']:.5f}", f"{r['nll']:.9f}") for r in val['summary'] if r['scope'] == 'overall' or r['scope'].startswith('group/')]), '',
              'A0=W0; A1=unchanged B1 activation formula on the same frozen state; A2=static local PoE; A3=static uniform PoE; A4=unchanged C2 historical diagnostic only. A1 is not a separately trained B1 checkpoint. Full seed/state/easy/hard cells are in summary.csv.', '',
              '## Engineering evidence and inference boundary', '',
              f"Local108passed53.20s. Remote CPU/CUDA calibration prerequisite suites: {cal_receipt['tests']}. All calibration/validation engineering validity checks pass: {cal['validity']['passes']}/{validity['passes']}.",
              f"A0/A1/A4 exact replay: {validity['A0_bitwise_equal']}/{validity['A1_bitwise_equal']}/{validity['A4_bitwise_equal']}. Model tensors unchanged: {validity['parameters_unchanged']}; static inference tensors/no parameter gradients: {validity['static_inference_tensors']}/{validity['parameter_grads_none']}.",
              f"Maximum historical NLL discrepancy {validity['max_historical_nll_error']:.9g}; accuracy discrepancy {validity['max_historical_accuracy_error']:.9g}. All model, generator, config, source/checkpoint and tested implementation hashes match. The same frozen calibration dictionary appears in both phases.",
              'A0/A1/A2/A3 execute under inference_mode. A2/A3 contain no gradient, optimizer, residual state, parameter copy, learned gate, task label or task ID. Only the explicitly requested separate A4 historical C2 call computes its established inner gradient; it cannot affect static outputs or lambda. No outer training occurs.', '',
              'Environment: `'+json.dumps(val['environment'], sort_keys=True)+'`.', '',
              '## Diagnostics, artifacts and reproduction', '',
              'localization.csv contains per-cell teacher diversity, attention entropy/effective token count, A2-A3 probability L1/KL and class differences. All query probabilities/log probabilities, teachers/attention, offline metrics and phase IDs are preserved in18 raw gzip JSONL files per phase. Calibration saves p0/teacher plus every grid loss, sufficient to reproduce each candidate without regenerating images.',
              f"artifact_manifest.json hashes all {len(cal_manifest)+len(val_manifest)} original files; receipt files preserve run commands, start/end, tests and environment. Original train.log records the frozen-lambda file SHA256 before novel execution.",
              '`bash scripts/run_t012_calibration_a6000.sh`, then commit actual frozen_lambda.json, then `bash scripts/run_t012_validation_a6000.sh` with TOVD_SOURCE_REVISION and TOVD_LAMBDA_COMMIT set to the recorded commits.',
              f"`python -m research_log.t012.write_report --cal-run {cal_run.as_posix()} --val-run {val_run.as_posix()}` regenerates reports without model execution.",
              'No post-outcome lambda, teacher, temperature, source, generator or criterion changes. This is a controlled synthetic audit, not detector accuracy or a universal impossibility claim.', '']
    (root/'RESULTS.md').write_text('\n'.join(lines), encoding='utf-8')
    plot(root, val['summary'], frozen['exponent'])
    if not gates['passes']:
        synthesis(root, val)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cal-run', type=Path, required=True)
    parser.add_argument('--val-run', type=Path)
    args = parser.parse_args()
    main(args.cal_run, args.val_run)
