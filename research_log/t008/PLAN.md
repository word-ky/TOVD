# T008 preregistration — label-free observability audit

Research2008520/c6593b7 accepted T007 and assigned this diagnosis on2026-09-12.
No T008 feature/outcome correlation has been computed. No training/controller design.
Baseline `python -m pytest -q`:79 passed37.15s. Source hashes already verified
against committed T007 verification/T002 hash receipts, before feature extraction.

## Fixed source grid and evaluation

sources.json fixes33 files: seeds7/17/27 x(original final T002 P plus W1/W2
step0/50/100/200/400). W1=P_O0_resume; W2=P_C2_warm. Each has100 easy+100 hard
episodes, original T002 test seed20000000+seed*10000+index, index0..99.
All6600 rows, W0/candidate output tensors and query probabilities will be retained.
Original P and W1/W2 step0 are identical states. Primary pooled analysis counts
each state once: original P +W1/W2 steps50/100/200/400 =27 unique states,5400 rows.
Full6600-row pooled statistics are a separately labeled duplicate-weight sensitivity.
Within-branch descriptions retain its full0/50/100/200/400 trajectory. This avoids
tripling the favorable original state in primary inference while preserving the
entire requested grid. No T006 secondary state check is added.

Load all states into unchanged O1_backtracking at eval, float32, same classifier
temperature.1, teacher tau.2, candidates[.05,.025,.0125,.00625,.003125], Armijo1e-4.
Use existing normal model and W0-only switch. Oracle outcomes are computed only
after pure-X/T/Q features/outputs exist. Repeat extraction after oracle logging,
and compare normal outputs/fast states and features exactly. Compare all states
against corresponding T007 trajectory receipts; original also against T005.
No task label/ID, task gradient, correct-class margin, regime/seed/step/branch or
checkpoint drift may enter the predictor vector. Drift is localization metadata only.

## Fourteen fixed scalar features

All entropies/JS use natural logarithms and clamp probabilities at eps=1e-12 for
logs; other divisions use denominator+eps. Mean is arithmetic over all queries
or all image tokens; no foreground filtering, label-derived masks or class IDs.

Pre-update (available before a candidate parameter step):
1. query_entropy: mean H(softmax(classifier(W0(Q),T)));
2. query_max_probability: mean max query probability;
3. query_probability_gap: mean top1-top2 query probability;
4. assignment_entropy: mean H(A), A=softmax(Pk(X)T^T/.2), same teacher as O1;
5. assignment_probability_gap: mean top1-top2 A gap;
6. inner_loss_before: unchanged O1 teacher/student cross entropy;
7. gradient_norm: sqrt(sum of squared raw O1 fast-parameter gradients).
Feature7 requires an inner backward pass; "pre-update" does not mean free/no compute.
Pre-feature extraction is separately callable and does not invoke C2 selection.

Post-candidate / rollback-capable only:
8. chosen_eta;
9. backtracking_trials;
10. normalized_update: ||W*-W0||_2/(||W0||_2+eps), over1616 fast parameters;
11. representation_shift: Frobenius ||F_W*(Q)-F_W0(Q)|| over8x16 output tokens;
12. relative_inner_reduction: (L_before-L_after)/(abs(L_before)+eps);
13. query_js: mean[.5 KL(p0||m)+.5 KL(p*||m)], m=.5(p0+p*);
14. prediction_changed_fraction: fraction of queries with changed argmax.

No learned predictor, multivariate score, feature search beyond these14 or feature
threshold tuning. JSON/CSV schema explicitly marks is_label_free_feature and timing.
W0/candidate outputs and probabilities are label-free recorded tensors, not extra
candidate scalar predictors. Identities/labels/outcomes remain separate metadata.

## Offline outcomes / statistics

Delta_NLL=NLL_C2-NLL_W0 is primary continuous outcome; negative means benefit.
Accuracy delta is secondary. Primary harm=Delta_NLL>0; sensitivity harm=Delta_NLL>.05.
Exactly zero Delta_NLL is neutral for benefit/harm group comparisons and nonharm
for binary AUROC. All data retained without filtering tiny deltas.

Spearman is Pearson correlation of average tied ranks. Constant-variable correlation
is undefined (JSON null), not zero. AUROC uses tied-rank Mann-Whitney statistic,
equivalently P(score_harm>score_nonharm)+.5P(tie); a constant score has AUROC.5;
single-class outcome AUROC is undefined, never replaced with a favorable value.
No p-values or independent-row confidence intervals: checkpoints reuse episodes
and only3 independent seeds are available. Report sample sizes/harm prevalence.

Report un-oriented AUROC (higher feature ->harm) and Spearman overall, within
easy/hard, per seed, per W1/W2 branch and per state/regime; summarize direction
consistency across branch/seed/states. Full-grid pooled sensitivity also reported.

Leave-one-seed-out: for each feature and each harm definition, infer orientation
using only the other2 seeds' unique primary states, pooling regimes. If training
AUROC>=.5 use+1, otherwise-1; tie chooses+1 deterministically. Held-out fold uses
that fixed orientation. Use the SAME fold orientation for its overall/easy/hard
AUROCs. No held-out labels select orientation or thresholds. Report all3 folds,
mean/min and corresponding training AUROC. Repeated states/episodes from the
held-out seed never appear in its orientation-training partition.

## Exact interpretation gate (primary harm>0 only)

A single scalar passes only when:
1. mean overall LOSO AUROC>=.70 and every fold>=.65;
2. all3 fold orientations agree; using that orientation, pooled W1 and W2 each
   have AUROC>.5 both overall AND within easy (same direction across branches);
3. to operationalize "nontrivial within easy" before outcomes: mean easy LOSO
   AUROC>=.65 and every easy fold>=.60, under the same orientation selected from
   the two training seeds' pooled regimes (no easy-specific reorientation).
Undefined required quantities fail the gate. These within-easy thresholds and
direction tests prevent a pass based only on separating easy from hard.
Report state-wise AUROCs/correlations and the fraction agreeing with orientation
as diagnosis; do not silently add a later significance/selection requirement.
Post-candidate passes can motivate only a future **rollback** policy; pre features
can motivate a future pre-update policy with their stated compute requirements.
Sensitivity Delta_NLL>.05 is reported but never used to choose primary success.
If none pass, report no simple scalar observability; no rescue fitting. If any
pass, recommend a separately preregistered T009 using training-only thresholds
and fresh held-out validation. T008 implements no gate and selects no checkpoint.

## Failure localization and plots

For harmful(>0), beneficial(<0), neutral(=0) groups, report count/mean/median/q25/q75
of14 features plus W0/key/query/total-state L2 drift from original seed P; stratify
easy/hard and branches. Compare confident W0, ambiguity, update/shift/descent
patterns descriptively. Labels define groups only, never runtime predictors.
Plot fixed checkpoint NLL-delta sign map and all14 feature-vs-Delta_NLL panels;
show seed/regime context and no fitted gating boundary. No plots choose thresholds.

## Reuse and bounded increments

Repository-owned donor only, unchanged generator/runtime/optimizer state. No new
dependency: stdlib ranking/statistics, existing torch, local matplotlib for figures.
1. Label-free pre/post feature extractor using existing O1 equations and normal
   C2 forward; tests for formula values, no selection in pre path, deterministic
   oracle-on/off equality, label/ID irrelevance and unchanged model parameters.
2. Task-local tied-rank/Spearman/AUROC/LOSO/gate and audit runner; known-rank/tie/
   reversal/single-class tests plus seed-partition orientation/no-regime-confound
   fixture and tiny real checkpoint/receipt end-to-end flow.
Each increment passes focused tests before next; then full local and A6000CPU/CUDA
regression, fixed extraction/analysis only, all raw receipts +CSV/JSON +plots/report.
Keep recovery logs under research_log/t008 and mirror remote receipts.
