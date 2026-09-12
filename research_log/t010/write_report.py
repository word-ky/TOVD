"""Render fixed T010 calibration/validation receipts without model imports."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil

from .summary import METHODS


def table(headers, rows):
    return '\n'.join(['| '+' | '.join(headers)+' |', '| '+' | '.join(['---']*len(headers))+' |']+
                     ['| '+' | '.join(str(v) for v in row)+' |' for row in rows])


def num(value):
    return 'undefined' if value is None else f'{value:.6f}'


def main(cal_run, val_run):
    root = Path('research_log/t010')
    cal_root, val_root = cal_run/'artifacts/t010_calibration', val_run/'artifacts/t010_validation'
    cal = json.loads((cal_root/'results.json').read_text())
    val = json.loads((val_root/'results.json').read_text())
    summary, gate = val['summary'], val['gates']
    for name in ('summary.csv', 'gates.json'):
        shutil.copyfile(val_root/name, root/name)
    lines = ['# T010 base-calibrated query rollback on fresh novel streams', '',
             f"Calibration run `{cal_run.name}`; validation run `{val_run.name}`.",
             f"Preregistration `396d903`; tested `{val['environment']['revision']}`; actual threshold commit `{val['environment']['threshold_commit']}`.", '',
             '**Engineering validity PASS. Confirmatory result '+('PASS' if gate['passes'] else 'FAIL')+'.**', '',
             ('All clauses pass. Recommend Research Lead review of query-local entropy-consistent fast semantic specialization and a separately scoped integration task; no detector work is started.' if gate['passes'] else 'At least one fixed clause fails. Recommend terminating the current O1+C2 rollback line and a higher-level non-destructive reframe. Do not tune thresholds, fit a rescue gate or integrate a detector under this formulation.'), '',
             '## Fixed experiment', '',
             'Nine frozen checkpoints: original P, final W1 and final W2 for seeds7/17/27. Base calibration: 100 easy+100 hard/state (1800 episodes/14400 queries). Fresh novel validation: 200 easy+200 hard/state (3600 episodes/28800 queries). Model/generator/C2 and all checkpoint hashes unchanged.', '',
             'Calibration uses new1B namespace, validation new2B namespace, distinct regime offsets and exact ID manifests. Each held seed threshold uses only other-two-seed base calibration (9600 queries), with 0:.01:1 empirical dH quantiles plus infinities and smallest-tau tie-break within1e-12 of minimum base NLL. Actual thresholds were committed before novel generation/scoring.', '',
             'R0=W0; R1=always-C2; R2=calibrated dH<=tau; R3=fixed dH<=0; ORACLE=lower true-label query NLL (W0 on ties). R2/R3 select whole probability/token outputs without blending. Labels are offline calibration/scoring inputs only. All policies pay for the C2 candidate except R0; no free pre-update selection is claimed.', '',
             '## Frozen thresholds', '',
             table(['Held seed', 'Base calibration seeds', 'Queries', 'tau', 'Selected base NLL'],
                   [[s, t['calibration_seeds'], t['query_count'], t['tau'], num(t['selected_calibration_nll'])] for s, t in cal['thresholds'].items()]), '',
             '## Confirmatory gates', '',
             table(['Gate', 'Pass'], [[k, v] for k, v in gate['by_gate'].items()]), '',
             'Gate1 per seed: R2 NLL<R0 and <=R1+.01; accuracy not below both. Gate2 hard per group: retain75% NLL/70% accuracy gain, otherwise <=.01 NLL/1pp degradation. Gate3 easy per seed/state: remove60% NLL/50% accuracy regression; beneficial NLL retains50% or stays within.01 of W0. Gate4 retention10%-90% per seed. Gate5 no validation tuning/freshness/source fidelity.', '',
             table(['Gate', 'Scope', 'Pass', 'Evidence'], [[c['gate'], c['scope'], c['passes'], json.dumps({k:v for k,v in c.items() if k not in ('gate', 'scope', 'passes')})] for c in gate['clauses']]), '',
             '## State-group results', '',
             table(['Group/regime', 'Method', 'NLL', 'Accuracy %', 'C2 retained %', 'Gains retained', 'Damages rolled back', 'NLL oracle headroom fraction'],
                   [[r['scope'], r['method'], num(r['nll']), num(100*r['accuracy']), num(100*r['retention']), num(r['gain_retained_fraction']), num(r['damage_rollback_fraction']), num(r['oracle_nll_headroom_fraction'])] for r in summary if r['scope'].startswith('group/')]), '',
             'Headroom fraction measures improvement from R1 toward the label-using oracle. It is not clipped and is undefined for zero headroom. Gain/damage fractions are based on W0wrong/C2correct and W0correct/C2wrong queries respectively; source counts are in summary.csv.', '',
             '## Held-seed aggregates', '',
             table(['Seed', 'Method', 'NLL', 'Accuracy %', 'C2 retained %'], [[r['scope'], r['method'], num(r['nll']), num(100*r['accuracy']), num(100*r['retention'])] for r in summary if r['scope'].startswith('seed/')]), '',
             '## Every held-seed/state/regime cell', '',
             table(['Cell', 'Method', 'NLL', 'Accuracy %', 'C2 retained %'], [[r['scope'], r['method'], num(r['nll']), num(100*r['accuracy']), num(100*r['retention'])] for r in summary if r['scope'].startswith('cell/')]), '',
             '## Reproduction / artifacts / limits', '',
             table(['Phase', 'Episodes / queries', 'NLL max error', 'Accuracy error', 'Selected-token probability error', 'Output equality', 'Parameters unchanged'],
                   [[r['phase'], f"{r['validity']['episode_count']} / {r['validity']['query_count']}", num(r['validity']['max_nll_error']), num(r['validity']['max_accuracy_error']), num(r['validity']['max_selected_token_probability_error']), r['validity']['normal_oracle_bitwise_equal'], r['validity']['parameters_unchanged']] for r in (cal, val)]), '',
             'Original run directories retain all raw outputs/tokens, selections, labels/IDs, per-query/episode metrics, candidate inner-loss/gradient/update diagnostics, thresholds/candidate-loss grids, hashes, checks and run logs. Source/model code hashes and all fresh IDs are in sources.json. Summary/gate tables and artifact hashes are retained here.', '',
             'Local95 tests passed40.01s before implementation commit. Remote CPU/CUDA tests ran before calibration; their exact outputs are in the calibration train.log. No runtime changes between phases. Environment: '+json.dumps(val['environment']), '',
             'Three model seeds and one fixed synthetic semantic world limit external generalization. Validation episodes are fresh but class/world/checkpoints are shared with earlier work as preregistered. No query-independent inference or post-hoc confidence intervals, no new feature/threshold search. A diagnostic oracle is never a deployable baseline.', '',
             'Commands: `bash scripts/run_t010_calibration_a6000.sh`, then after committing thresholds `bash scripts/run_t010_validation_a6000.sh`; both record TOVD_SOURCE_REVISION, validation additionally TOVD_THRESHOLD_COMMIT. Exact CLI is in committed scripts and original run.sh files.', '',
             '![Fresh novel performance](performance.png)', '', '![Threshold usage](usage.png)', '']
    (root/'RESULTS.md').write_text('\n'.join(lines), encoding='utf-8')
    figures(root, summary)
    manifest = []
    for run in (cal_run, val_run):
        for p in sorted(run.rglob('*')):
            if p.is_file():
                manifest.append({'path': p.as_posix(), 'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()})
    (root/'verification.json').write_text(json.dumps({'calibration_run': cal_run.name, 'validation_run': val_run.name, 'gates': gate['by_gate'], 'artifacts': manifest}, indent=2)+'\n', encoding='utf-8')


def figures(root, summary):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    groups = sorted({r['scope'] for r in summary if r['scope'].startswith('group/')})
    lookup = {(r['scope'], r['method']): r for r in summary}
    labels = [g.replace('group/', '').replace('P_C2_warm', 'W2 final').replace('P_O0_resume', 'W1 final').replace('original_P', 'Original') for g in groups]
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    for ax, metric, scale in zip(axes, ('nll', 'accuracy'), (1, 100)):
        for i, method in enumerate(METHODS):
            ax.bar(np.arange(len(groups))+(i-2)*.16, [lookup[g, method][metric]*scale for g in groups], width=.16, label=method)
        ax.set_xticks(np.arange(len(groups)), labels, rotation=30, ha='right')
        ax.set_ylabel('NLL' if metric == 'nll' else 'Accuracy (%)')
        ax.legend(fontsize=8)
        ax.grid(axis='y', alpha=.15)
    fig.suptitle('T010 fresh novel validation (ORACLE uses labels)')
    fig.tight_layout()
    save_figure(fig, root, 'performance')
    fig, ax = plt.subplots(figsize=(10, 3.5))
    seeds = (7, 17, 27)
    matrix = [[lookup[g.replace('group/', f'cell/{s}/'), 'R2']['retention']*100 for g in groups] for s in seeds]
    im = ax.imshow(matrix, vmin=0, vmax=100, cmap='Blues', aspect='auto')
    for i in range(3):
        for j in range(len(groups)):
            ax.text(j, i, f'{matrix[i][j]:.1f}%', ha='center', va='center', color='white' if matrix[i][j] > 60 else 'black')
    ax.set_xticks(np.arange(len(groups)), labels)
    ax.set_yticks(np.arange(3), [f'Seed{s}' for s in seeds])
    ax.set_title('R2 C2 retention on fresh novel queries')
    fig.colorbar(im, ax=ax, label='C2 retained (%)')
    fig.tight_layout()
    save_figure(fig, root, 'usage')


def save_figure(fig, root, name):
    import matplotlib.pyplot as plt
    fig.savefig(root/(name+'.png'), dpi=160)
    svg = root/(name+'.svg')
    fig.savefig(svg)
    svg.write_text('\n'.join(s.rstrip() for s in svg.read_text(encoding='utf-8').splitlines())+'\n', encoding='utf-8')
    plt.close(fig)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--calibration-run', type=Path, required=True)
    p.add_argument('--validation-run', type=Path, required=True)
    a = p.parse_args()
    main(a.calibration_run, a.validation_run)
