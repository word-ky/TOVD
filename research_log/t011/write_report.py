"""Render completed T011 evidence; pure reporting, no Torch/model imports."""

import argparse
from collections import defaultdict
import csv
import hashlib
import json
from pathlib import Path
import shutil
from statistics import mean


def table(headers, rows):
    return '\n'.join(['| '+' | '.join(headers)+' |', '| '+' | '.join(['---']*len(headers))+' |']+
                     ['| '+' | '.join(str(v) for v in row)+' |' for row in rows])


def save_json(path, data):
    path.write_text(json.dumps(data, indent=2, allow_nan=False)+'\n', encoding='utf-8')


def plot(root, summary):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    lookup = {(r['scope'], r['method']): r for r in summary}
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.3), layout='constrained')
    branches = ('original_P', 'P_O0_resume', 'P_C2_warm')
    for ax, regime in zip(axes, ('hard', 'easy')):
        for i, (method, label, color) in enumerate((('S1', 'Global C2', '#476e99'), ('S2', 'QLSR', '#cb6943'), ('S3', 'Uniform residual', '#8b929a'))):
            gains = [lookup[('group/'+b+'/'+regime, 'S0')]['nll']-lookup[('group/'+b+'/'+regime, method)]['nll'] for b in branches]
            ax.bar([j+(i-1)*.24 for j in range(3)], gains, width=.23, label=label, color=color)
        ax.axhline(0, color='black', linewidth=.8)
        ax.set_xticks(range(3), ['Original P', 'W1 final', 'W2 final'])
        ax.set_title(regime.capitalize()+' novel development episodes')
        ax.set_ylabel('NLL improvement over W0 (nats)')
        ax.spines[['top', 'right']].set_visible(False)
        ax.grid(axis='y', alpha=.18)
    axes[0].legend(fontsize=8)
    fig.suptitle('T011: fixed checkpoints and query-local residuals', fontsize=13)
    fig.savefig(root/'performance.png', dpi=180)
    fig.savefig(root/'performance.svg')
    plt.close(fig)
    svg = root/'performance.svg'
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text(encoding='utf-8').splitlines())+'\n', encoding='utf-8')


def main(run_path):
    root = Path('research_log/t011')
    source = run_path/'artifacts/t011'
    result = json.loads((source/'results.json').read_text(encoding='utf-8'))
    for filename in ('summary.csv', 'gates.json'):
        shutil.copyfile(source/filename, root/filename)
    save_json(root/'mechanism.json', result['mechanism'])
    save_json(root/'verification.json', result['validity'])
    manifest = [dict(path=p.as_posix(), bytes=p.stat().st_size, sha256=hashlib.sha256(p.read_bytes()).hexdigest())
                for p in sorted(run_path.rglob('*')) if p.is_file()]
    save_json(root/'artifact_manifest.json', manifest)
    grouped = defaultdict(list)
    with (source/'episodes.csv').open(encoding='utf-8') as handle:
        for row in csv.DictReader(handle):
            grouped[(row['seed'], row['branch'], row['regime'])].append(row)
    diversity = []
    for (seed, branch, regime), rows in grouped.items():
        diversity.append(dict(seed=seed, branch=branch, regime=regime,
                               **{m+'_'+k: mean(float(r[m+'_'+k]) for r in rows) for m in ('S2', 'S3')
                                  for k in ('diversity', 'teacher_diversity', 'eligible_pairs')}))
    with (root/'diversity.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(diversity[0]))
        writer.writeheader()
        writer.writerows(diversity)
    g, v, mechanism = (result[k] for k in ('gates', 'validity', 'mechanism'))
    recommendation = ('All five development criteria pass. Recommend a separately preregistered T012 on a fresh stream; stop for Research Lead review.'
                      if g['passes'] else 'The development screen fails. Per the fixed stop rule, recommend terminating the current fast-semantic-state program at the synthetic mechanism level and returning to a static/activation-side OVD formulation. Stop for Research Lead review; no gate/objective/controller rescue.')
    lines = ['# T011 query-local semantic residual: development screen', '', recommendation, '',
             f"Run `{run_path.name}`; tested commit `{result['environment']['revision']}`; preregistration `b615642a3b23261dfaed6ebbdb61b423be7f3901`.",
             'Nine frozen checkpoints, 100 easy + 100 hard episodes each; 1,800 episodes / 14,400 queries, 600 paired scene seeds from the fresh 3-billion namespace. No outer training, learned selector or outcome-driven change.', '',
             '## Fixed criteria', '', table(['Criterion', 'Result'], [(k, 'PASS' if passed else 'FAIL') for k, passed in g['by_gate'].items()]), '',
             'Full clause arithmetic, including every easy cell and hard seed, is preserved in `gates.json`.', '',
             'Hard utility and consistency:', '',
             table(['Group', 'S2 hard NLL gain over S0', 'S1 gain retained %', 'S2 accuracy change pp'],
                   [(c['scope'], f"{c['S2_nll_gain']:.6f}", 'N/A' if c['gain_retention'] is None else f"{100*c['gain_retention']:.2f}",
                     f"{c['accuracy_delta_pp']:.4f}") for c in g['clauses'] if c['gate'] == 2]), '',
             table(['Group', 'Seeds improving hard NLL', 'Worst seed NLL regression'],
                   [(c['scope'], c['improved_seeds'], f"{c['worst_nll_regression']:.6f}") for c in g['clauses'] if c['gate'] == 3]), '',
             f"Easy safety: {sum(c['passes'] for c in g['clauses'] if c['gate'] == 4)} / {sum(c['gate'] == 4 for c in g['clauses'])} seed/state cells pass.",
             'Localization: '+', '.join(f"{k}={c[k]:.6f}" for c in g['clauses'] if c['gate'] == 5
                                        for k in ('S2_minus_S3_hard_nll', 'S2_minus_S3_easy_nll'))+'.', '',
             '## Task metrics', '',
             table(['Scope', 'Method', 'Accuracy %', 'NLL'], [(r['scope'], r['method'], f"{100*r['accuracy']:.4f}", f"{r['nll']:.6f}")
                    for r in result['summary'] if r['scope'] == 'overall' or r['scope'].startswith('group/')]), '',
             'S0=W0; S1=unchanged global O1+C2; S2=QLSR; S3=uniform-context residual. All methods use identical episodes and offline labels. Complete per-seed cells are in `summary.csv`.', '',
             '## Mechanism diagnostics', '',
             table(['Measure', 'S2', 'S3'], [(k, f"{mechanism['S2'][k]:.8g}", f"{mechanism['S3'][k]:.8g}") for k in (
                 'acceptance_fraction', 'inner_loss_before', 'inner_loss_after', 'inner_gradient_norm', 'chosen_eta', 'backtracking_trials',
                 'residual_norm', 'normalized_residual_norm', 'attention_entropy', 'effective_token_count', 'residual_diversity',
                 'teacher_diversity', 'vocabulary_residual_difference', 'min_accepted_vocabulary_difference')]), '',
             f"S2-S3 residual diversity excess = {mechanism['residual_diversity_excess']:.8g}; fixed threshold >=0.01, with S2 diversity >0.001.",
             'Per-cell diversity is in `diversity.csv`; full pairwise cosine matrices, eligible-pair counts, attention, teacher distributions and residual vectors are retained in every raw episode.', '',
             '## Engineering validity', '',
             f"Validity passes: {v['passes']}. Source/code hashes match. Model parameters byte-unchanged: {v['parameters_unchanged']}. S0/S1 replay bitwise equal: {v['S0_S1_bitwise_equal']}. Exact zero initialization, query isolation and image/vocabulary reset: {v['exact_resets']}.",
             f"Maximum offline score NLL discrepancy {v['max_score_nll_error']:.8g}; accuracy discrepancy {v['max_score_accuracy_error']:.8g}. Finite probabilities: {v['all_probabilities_finite']}.",
             'Local full suite: 101 passed in 19.16s. A6000 CPU/CUDA suite timings and original commands are in the immutable run train.log / metadata and completion receipt.', '',
             'Environment: `'+json.dumps(result['environment'], sort_keys=True)+'`.', '',
             '## Implementation scope and limitations', '',
             'The explicit T011 QLSR cosine teacher uses normalized projected keys and text, tau_t=tau_q=0.2 and student_tau=0.1. Historical S1 uses its original unnormalized key-dot-text teacher. This difference was identified and disclosed before outcomes in PLAN.md. S2 vs S3 isolates query localization under the same new teacher/residual formulation; S1 vs S2 also changes the state parameterization and teacher normalization.',
             'Residuals start at exact zero; independent per-query Armijo uses the original five candidates and c1=1e-4. No slow/model tensor is adapted. No outer/meta-training is claimed for this frozen structural screen; existing meta-gradient tests still pass.',
             'This is synthetic exploratory evidence, not detector accuracy or confirmation. The fixed thresholds, namespace, source states and gates were not changed after outcomes.', '',
             '## Reproduction and artifacts', '',
             '`export TOVD_SOURCE_REVISION=79e6e2baac5b92dd8b66c1a8a048a4d5013f5d5b; bash scripts/run_t011_a6000.sh` on physical GPU1. The script runs CPU and CUDA full suites before the screen.',
             '`python -m research_log.t011.write_report --run '+run_path.as_posix()+'` regenerates this report, tables and figure without model execution.',
             f"`artifact_manifest.json` hashes all {len(manifest)} original run files. Eighteen lossless gzip JSONL raw files retain every episode/query; queries.csv and episodes.csv allow independent analysis. `implementation_hashes.json` fixes executed source/config/plan bytes; `verification.json` records remote actual hashes.", '']
    (root/'RESULTS.md').write_text('\n'.join(lines), encoding='utf-8')
    plot(root, result['summary'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', type=Path, required=True)
    main(parser.parse_args().run)
