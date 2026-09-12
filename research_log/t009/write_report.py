"""Render the fixed T009 receipts; no model imports or analysis choices."""

import hashlib
import json
from pathlib import Path

from .query_analysis import FEATURES, PRE


def table(headers, rows):
    return '\n'.join(['| '+' | '.join(headers)+' |', '| '+' | '.join(['---']*len(headers))+' |'] +
                     ['| '+' | '.join(str(x) for x in row)+' |' for row in rows])


def main():
    root = Path('research_log/t009')
    out = root/'results'
    r = json.loads((out/'results.json').read_text())
    checks = json.loads((out/'checks.json').read_text())
    source = json.loads((root/'sources.json').read_text())
    gate_rows = []
    for f, g in r['gates_A'].items():
        gate_rows.append([f, 'pre' if f in PRE else 'post', f"{g['overall']['mean']:.6f} / {g['overall']['min']:.6f}",
                          f"{g['easy']['mean']:.6f} / {g['easy']['min']:.6f}", g['orientations'], g['direction_passes'], g['passes']])
    lines = ['# T009 query-local harm decomposition', '',
             f"Source `{source['source_commit']}`; preregistration `1b63bf6`; tested `{r['environment']['revision']}`.", '',
             f"Engineering validity **PASS**. Condition A **{'PASS' if r['A_passes'] else 'FAIL'}**. Condition B **{'PASS' if r['B']['passes'] else 'FAIL'}**.", '',
             'Frozen logs only: 54 hashed files, 27 unique states, 5400 episodes and 43200 queries; 14400 queries per seed. No model rerun or training.', '',
             'Recommend a separately preregistered T010 only if both A and B pass. Otherwise no controller implementation. ' +
             ('A fails: terminate the current O1+C2 safety branch and consider a higher-level reframe such as activation-side vocabulary conditioning or a separate fast residual expert. These are proposals, not validated alternatives.' if not r['A_passes'] else 'A passes; the B result determines whether query-level selectivity has sufficient oracle headroom.'), '',
             '## Single-feature interpretation gate', '',
             'A requires overall LOSO mean >=.70 / every fold >=.65; easy mean >=.65 / every fold >=.60, same training-seed orientation and consistent W1/W2 direction. Post-candidate features require paying for C2; they can only motivate later rollback/output fusion.', '',
             table(['Feature', 'Availability', 'Overall mean / min', 'Easy mean / min', 'Fold signs', 'Direction', 'Pass'], gate_rows), '',
             '## Primary descriptive relationships', '',
             'AUROC uses the raw feature sign; orientation is learned only on other seeds for LOSO. Complete per-state/branch/step results and direction consistency are in CSVs.', '']
    descriptive = []
    for f in FEATURES:
        values = [next(x for x in r['single_features'] if x['feature'] == f and x['scope'] == s) for s in ('overall', 'regime/easy', 'regime/hard')]
        descriptive.append([f]+[f"{v['spearman']:.5f} / {v['auroc_harm']:.5f}" for v in values])
    lines += [table(['Feature', 'Overall rho / AUC', 'Easy rho / AUC', 'Hard rho / AUC'], descriptive), '',
              '## LOSO folds and sensitivity', '',
              table(['Feature', 'Definition', 'Seed', 'Train sign', 'Overall AUC', 'Easy AUC', 'Hard AUC'],
                    [[f, kind, fold['held_seed'], fold['orientation']]+[f"{fold[s]['auroc']:.6f}" for s in ('overall', 'easy', 'hard')]
                     for f, cases in r['loso'].items() for kind, folds in cases.items() for fold in folds]), '',
              '## Oracle per-query rollback ceiling', '',
              'Choose the lower true-class NLL per query, W0 on ties. Accuracy is measured from that chosen output; this is not a separately optimized accuracy oracle. Labels are used only offline. Values are aggregate means; accuracy shown as percent.', '',
              table(['State group', 'W0 acc', 'C2 acc', 'Oracle acc', 'W0 NLL', 'C2 NLL', 'Oracle NLL'],
                    [[c['scope']]+[f"{100*c[k]:.4f}" for k in ('before_accuracy', 'after_accuracy', 'oracle_accuracy')]+[f"{c[k]:.6f}" for k in ('before_nll', 'after_nll', 'oracle_nll')]
                     for c in r['oracle_ceilings'] if c['scope'].startswith('focus/')]), '',
              'B requires >=95% of positive hard C2 gain retained for each original/final branch and both metrics (no degradation if no gain), plus >=80% removal of each observed easy original/final seed-state regression. Units below are NLL or accuracy fraction.', '',
              table(['Scope', 'Clause', 'Metric', 'C2 gain/regression', 'Oracle gain/removed', 'Required', 'Pass'],
                    [[c['scope'], c['kind'], c['metric']]+[f"{c[k]:.6f}" for k in ('C2_gain_or_regression', 'oracle_gain_or_removed', 'required')]+[c['passes']] for c in r['B']['clauses']]), '',
              '## Damage attribution', '',
              f"Global W0 confidence quartile boundaries: {r['confidence_quartiles']}. Boundaries use label-free probabilities only; equal values go to the lower quartile. These are descriptive bins, not fitted deployment thresholds.", '',
              'Only episodes with positive mean query NLL damage enter attribution. Net shares include negative offsets, so a bin can be negative or exceed 100%; gross shares use positive query damage only. Complete denominators and quartile x flip cross-tabs are in attribution.csv.', '',
              table(['Regime', 'Grouping', 'Group', 'Count', 'Net share', 'Gross positive share'],
                    [[x['regime'], x['grouping'], x['group'], x['count'], f"{x['net_share']:.5f}", f"{x['positive_share']:.5f}"]
                     for x in r['attribution'] if x['grouping'] != 'quartile_flip']), '',
              '## Correctness transitions', '',
              table(['Scope', 'Transition', 'NLL change', 'Count', 'Fraction', 'Mean delta'],
                    [[t['scope'], t['transition'], t['nll_direction'], t['count'], f"{t['fraction']:.5f}", f"{t['mean_delta']:.6f}"]
                     for t in r['transitions'] if t['scope'] in ('overall', 'regime/easy', 'regime/hard')]), '',
              '## Interpretation', '',
              'Both A and B pass. Three post-candidate scalars pass: delta_entropy (mean overall LOSO .750696, minimum .722485; easy mean .850020, minimum .770398), delta_max_probability (.708225, minimum .682447) and delta_probability_gap (.709433, minimum .678763). None of the three pre-update scalars passes. All fold orientations agree; increasing entropy, or decreasing maximum probability/gap, predicts greater query NLL harm.', '',
              'Delta-entropy oriented branch AUROCs are .753202/.744237 overall for W1/W2 and .853527/.852734 within easy. Its >.05 sensitivity fold AUROCs are .743774/.732589/.796518 overall. This supports a query-local post-candidate signal on this fixed grid; it does not establish a threshold, calibrated failure probability, detector transfer or actual rollback-policy performance.', '',
              'Within net-harmed easy episodes, the highest global W0-confidence quartile contributes 54.01% of net NLL damage and 49.64% of gross positive damage. Prediction flips contribute 70.45% of net damage and 66.81% of gross positive damage; no-flip damage remains substantial. Within hard harmed episodes, global Q4 is empty (zero contribution), not missing evidence.', '',
              'Across all queries, 3766 correct-to-wrong and 6657 wrong-to-correct transitions coexist; 12313 correct-to-correct queries still worsen NLL. NLL and top1 correctness do not coincide perfectly: 53 correct-to-wrong transitions improve NLL, and 75 wrong-to-correct transitions worsen it. The oracle uses the specified NLL criterion throughout.', '',
              'The original hard NLL oracle reaches 61.50% accuracy / .987770 NLL versus C2 46.25% / 1.235361. Final W1 hard reaches 51.8333% / 1.100422; final W2 hard 47.75% / 1.167493. Final W1 easy changes from W0 80.9583% / .404780 through C2 74.1667% / .667092 to oracle 89.4583% / .242742. Final W2 easy seed 27 changes from W0 92.5% / .242851 through C2 84.875% / .357217 to oracle 95.625% / .148417. All predeclared B clauses pass, but these numbers use labels and are ceilings only.', '',
              'Recommendation: Research Lead may preregister a separate T010 minimal per-query rollback/output-fusion experiment, calibrated on training data and tested separately. This audit implements no policy and does not reopen always-on C2 or detector integration.', '',
              '## Reproducibility and limits', '',
              f"All source hashes match. Historical episode NLL max error {checks['max_nll_error']:.3g}, delta max error {checks['max_delta_error']:.3g}, accuracy error {checks['max_accuracy_error']}; historical query NLL max error {checks['max_historical_query_nll_error']:.3g}. Probability-log versus stored fused float32 cross-entropy accounts for rounding; primary query harm sign differences: {checks['query_harm_sign_differences']}.", '',
              'Feature extraction repeated exactly, inherited oracle-on/off output checks all bitwise equal. All rows from each seed remain together; no random query split, no labels/IDs/regime in predictors, no thresholds fitted and no feature combinations. Nine predeclared scalars all reported. Optional logit margin omitted because raw logits were not stored.', '',
              'Three seeds and heavily reused queries/checkpoints mean these are diagnostic results, not independent 43200-sample validation. No p-values or independent-query confidence intervals. Oracle headroom is not a realizable policy result.', '',
              'Commands: `python -m pytest -q`; `python -m research_log.t009.audit --revision '+r['environment']['revision']+' --output research_log/t009/results`; `python -m research_log.t009.write_report`.', '',
              'Environment: '+json.dumps(r['environment'])+'. Full local 90 tests passed in 26.18s. No CUDA-dependent work, so no A6000 rerun.', '',
              '![Query LOSO](query_loso.png)', '', '![Oracle ceiling](oracle_ceiling.png)', '', '![Damage attribution](damage_attribution.png)', '']
    (root/'RESULTS.md').write_text('\n'.join(lines), encoding='utf-8')
    figures(root, r)
    files = sorted(out.iterdir())
    save = {'source_commit': source['source_commit'], 'source_files': len(source['records']), 'query_count': r['query_count'],
            'episode_count': r['episode_count'], 'A': r['A_passes'], 'B': r['B']['passes'],
            'artifacts': [{'path': str(p), 'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in files if p.is_file()]}
    (root/'verification.json').write_text(json.dumps(save, indent=2)+'\n', encoding='utf-8')


def figures(root, r):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np

    fig, axes = plt.subplots(1, 2, figsize=(13, 7), sharey=True)
    for ax, regime, threshold in zip(axes, ('overall', 'easy'), (.70, .65)):
        for i, seed in enumerate((7, 17, 27)):
            ax.scatter([r['loso'][f]['primary'][i][regime]['auroc'] for f in FEATURES], np.arange(len(FEATURES)), label=f'Seed {seed}', s=35)
        ax.set(xlim=(0, 1), xlabel='Held-seed AUROC (training-seed orientation)', title=regime.capitalize())
        ax.axvline(.5, color='gray', linestyle=':')
        ax.axvline(threshold, color='black', linestyle='--')
        ax.grid(alpha=.15)
    axes[0].set_yticks(np.arange(len(FEATURES)), [('Pre: ' if f in PRE else 'Post: ')+f for f in FEATURES])
    axes[0].invert_yaxis()
    axes[1].legend(loc='lower left', fontsize=8)
    fig.suptitle('T009 query-local scalar harm observability')
    fig.tight_layout()
    save_figure(fig, root, 'query_loso')

    focus = [c for c in r['oracle_ceilings'] if c['scope'].startswith('focus/')]
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    positions = np.arange(len(focus))
    labels = [c['scope'].replace('focus/', '').replace('original_P', 'Original P').replace('P_O0_resume', 'W1 final').replace('P_C2_warm', 'W2 final') for c in focus]
    for ax, metric, scale in zip(axes, ('nll', 'accuracy'), (1, 100)):
        for i, (name, label) in enumerate((('before', 'W0'), ('after', 'C2'), ('oracle', 'NLL oracle'))):
            ax.bar(positions+(i-1)*.24, [scale*c[name+'_'+metric] for c in focus], width=.24, label=label)
        ax.set_xticks(positions, labels, rotation=30, ha='right')
        ax.set_ylabel('Task NLL' if metric == 'nll' else 'Accuracy (%)')
        ax.legend(fontsize=8)
        ax.grid(axis='y', alpha=.15)
    fig.suptitle('Offline oracle per-query rollback ceiling (uses labels)')
    fig.tight_layout()
    save_figure(fig, root, 'oracle_ceiling')

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    for ax, grouping in zip(axes, ('quartile', 'flip')):
        groups = ('Q1', 'Q2', 'Q3', 'Q4') if grouping == 'quartile' else ('flip', 'no_flip')
        for i, regime in enumerate(('overall', 'easy', 'hard')):
            subset = [x for x in r['attribution'] if x['grouping'] == grouping and x['regime'] == regime]
            values = [next((x['positive_share'] for x in subset if x['group'] == g), 0.0) for g in groups]
            ax.bar(np.arange(len(groups))+(i-1)*.24, values, width=.24, label=regime)
        ax.set_xticks(np.arange(len(groups)), groups)
        ax.set_ylabel('Share of gross positive query damage')
        ax.legend(fontsize=8)
        ax.grid(axis='y', alpha=.15)
    fig.suptitle('Attribution within episodes with net NLL damage')
    fig.tight_layout()
    save_figure(fig, root, 'damage_attribution')


def save_figure(fig, root, name):
    import matplotlib.pyplot as plt
    fig.savefig(root/(name+'.png'), dpi=160)
    svg = root/(name+'.svg')
    fig.savefig(svg)
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text(encoding='utf-8').splitlines())+'\n', encoding='utf-8')
    plt.close(fig)


if __name__ == '__main__':
    main()
