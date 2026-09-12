# T009 preregistration — query-local frozen-log audit

Research instruction b9973b9/e6eb2c0; source commit 1d9915b06befaf509b912e3328491e3a8b263522.
Before any query-level outcome correlations, commit this plan and sources.json.
Inventory reads only record structure/counts and hashes. No model rerun or GPU use.

## Sources and accounting

sources.json enumerates every included state ID and SHA256 of 54 original T008 raw JSON files.
27 primary unique states: original P plus W1/W2 steps 50/100/200/400 for seeds 7/17/27.
100 easy + 100 hard episodes/state; 5400 episodes x8 queries =43200 query rows.
Duplicate W1/W2 step-0 records are omitted; original P represents their common origin.
Each row retains state/seed/branch/step/regime/episode_seed/query_index only as metadata.
All source records remain immutable. Hashes checked against the manifest before analysis.

## Nine fixed label-free scalars

Functions accept only p0, pC2, z0, zC2; no labels, class IDs or regime.
Use stored float32 values converted to Python float, no probability renormalization.
Natural logarithms with clamp eps=1e-12; entropies -sum(p log(max(p,eps))).
Top1 is first argmax (lowest index on ties); gap is largest minus second-largest probability.

Pre-update: query_entropy, query_max_probability, query_probability_gap.
Post-candidate: query_js = .5 KL(p0||m)+.5 KL(pC2||m), m=(p0+pC2)/2;
representation_displacement = ||zC2-z0||2/(||z0||2+eps);
prediction_changed (0/1); delta_max_probability; delta_entropy; delta_probability_gap.
Stored tokens permit the exact specified displacement calculation up to ordinary float precision.
Optional cosine/logit margin omitted: T008 stored probabilities/tokens, not logits or vocabulary embeddings. No rerun just for this; log probability ratio would be redundant and is not added.

## Offline outcomes and consistency

Only after all label-free features are computed, use stored labels to calculate
before_nll=-log(max(p0[y],eps)), after_nll=-log(max(pC2[y],eps)), delta_nll=after-before;
primary harm >0, sensitivity >.05. Accuracy is argmax correctness.
Retain correctness transitions correct->wrong, wrong->correct, correct->correct and wrong->wrong;
split each by improved/worsened/equal NLL (including unusual flip/NLL sign combinations).
Check mean query NLL/delta and accuracy against each T008 episode receipt: absolute NLL tolerance 2e-6, accuracy exact. Stored softmax vs fused float32 cross-entropy can differ by rounding; never change harm thresholds to hide it.
Record maximum errors and any sign differences against historical per-query NLL for interpretation, without substituting those values for the probability-defined primary outcome.
Replay features before/after offline labels; inherited T008 oracle-on/off bitwise checks must pass.
No model or runtime state is executed/modified. Schema marks all predictors versus offline outcomes/metadata.

## Statistics and A gate

Reuse T008 average-tie ranks, Spearman, AUROC, fold summary and LOSO orientation functions unchanged.
Constant Spearman and single-class AUROC are undefined (null); constant score AUROC=.5.
All 14400 queries of each seed are held together; training orientation is +1 if other-two-seed raw AUROC >=.5, else -1. Undefined training AUROC fails; tie chooses +1.
Same training orientation is used for held seed overall/easy/hard, never reoriented from held-out outcomes.
Report primary and >.05 sensitivity; sensitivity has its own training orientation and cannot determine A.
Report raw Spearman/AUROC per overall/regime, seed, branch, branch/step, state/regime; branch results use only the unique nonzero-step states.
Report descriptive direction consistency across state/branch with scope and counts; no post-hoc subset selection.

A passes only if at least one scalar has overall mean LOSO >=.70 and minimum >=.65;
easy mean >=.65 and minimum >=.60 with the same fold orientation;
and consistent fold orientation plus oriented W1/W2 AUROC >.5 both overall and within easy.
This operationalizes qualitative branch consistency as in T008. All features reported even if none passes.
Any passing post-candidate scalar supports only a possible later rollback/output-fusion audit, not free selection.

## Harm attribution

Confidence quartile boundaries are the linear-interpolated .25/.50/.75 quantiles of W0 max probability across all 43200 primary queries, labels unseen. Boundary ties assigned to lower quartile. Quartiles are descriptive only, not deployment thresholds.
For positive-damage episodes (mean query delta >0), attribute their net total damage to each confidence quartile and flip/no-flip group: sum signed query deltas / sum all query deltas within these episodes. Fractions can be negative or >1 because beneficial queries offset damage.
Also report gross positive damage sum(max(delta,0)) shares within these same episodes, counts and negative offsets; denominators explicit. Report overall/easy/hard using the same global boundaries, including quartile x flip cross-tab.
Report transition counts and delta sums overall/easy/hard and by branch/state. No random query splits or independent-query uncertainty estimates.

## Oracle rollback ceiling and B gate

Offline only: per query choose lower-NLL output, choose W0 on ties; use chosen output's argmax for accuracy. This is an NLL oracle, not a separately optimized accuracy oracle; accuracy need not be monotonic.
Aggregate back to all episodes, states and branch/regime. Highlight original T005 and final W1/W2, per seed and equally weighted across the three seeds.
B is fixed now: for each of those three groups, preserve >=95% of positive hard C2 gain versus W0 in BOTH NLL and accuracy; if a metric has no positive gain, require no degradation versus W0.
For every original/final easy seed-state where C2 worsens NLL or accuracy, remove >=80% of each observed regression versus W0. No issue for a metric without a regression. Report each clause and exact numbers; do not loosen after results.
Both A and B are necessary for recommending a separate T010. If A fails, recommend terminating this O1+C2 safety branch and a higher-level pivot; no rescue fitting or detector integration.

## Reuse and validation sequence

Relevant baseline: T008 rank/LOSO tests (3 pass in .03s before edits).
Increment 1: label-free query features, offline outcomes and episode/oracle aggregation with hand-computed deterministic tests.
Increment 2: attribution, A/B tests, full frozen-log CLI and synthetic end-to-end test; reuse T008 statistics rather than a new ranking implementation.
Then full local regression and the immutable 43200-row analysis; deterministic repeat extraction and historical consistency. No remote CUDA test needed for pure stdlib log analysis.
Final tables/JSON/plots, commands, environment, original hashes and failures live under research_log/t009 and in the engineering mailbox; mirror recovery/results to A6000. No new model code, no model training, no learned gate.
