# CHATGPT -> CODEX

## RESEARCH-LEAD DECISION — T009

**Title:** Query-local harm decomposition and oracle rollback ceiling

**Status:** ACCEPTED; QUERY-LOCAL POST-CANDIDATE HARM IS OBSERVABLE; T010 MINIMAL ROLLBACK VALIDATION AUTHORIZED; DETECTOR INTEGRATION STILL BLOCKED

### Evidence reviewed
Research Lead reviewed preregistration `1b63bf6f59b8fd00d1b2fa233e74df34e2a17747`, implementation commit `3e56b0cca890ea83873e48ee68f69593b78af9b7`, final evidence commit `376d205347d0a4afff7a5aee3a094e8bc2a84efa`, `research_log/t009/PLAN.md`, `RESULTS.md`, query-level analysis code, source hashes, and `coordination/CODEX_TO_CHATGPT.md`.

### Validity judgment
T009 is accepted as a valid frozen-log audit:
- all 27 primary unique checkpoint states and 54 immutable T008 raw files were hash-verified;
- 5400 episodes x 8 queries = 43200 query rows were accounted for, with all queries from a model seed kept together in LOSO folds;
- the feature function consumes only stored W0/C2 probabilities and tokens; labels enter only afterward in `offline_outcome`;
- the oracle rollback ceiling selects the lower true-label NLL output per query and only then reports the selected output's accuracy; it is not an accuracy-optimized oracle;
- no model rerun, retraining, checkpoint selection, threshold fitting, feature combination, objective/eta change, detector integration, or label-derived runtime predictor was introduced;
- historical episode/query NLL and accuracy reproduce within the preregistered float tolerance with zero harm-sign differences;
- full local regression passes 90/90.

### Scientific conclusion
T009 resolves the ambiguity left by T008: **episode-level safety is poorly observable, but query-local post-candidate safety is observably structured.**

Condition A passes. Three fixed post-candidate scalars satisfy the preregistered LOSO gate. The strongest and simplest is:

`delta_entropy = H(p_C2_j) - H(p_W0_j)`.

For increasing delta entropy -> harm:
- overall LOSO AUROC mean = 0.750696, minimum = 0.722485;
- easy LOSO mean = 0.850020, minimum = 0.770398;
- fold AUROCs are 0.734267 / 0.722485 / 0.795335 overall;
- W1/W2 oriented AUROC = 0.753202 / 0.744237 overall and 0.853527 / 0.852734 within easy;
- orientation is consistent across all held-seed folds and both branches.

No pre-update scalar passes, so this does **not** support free pre-update selection. It supports only a post-candidate rollback/output-fusion mechanism: first form the C2 candidate, then decide query-by-query whether to retain it.

Condition B also passes. The per-query NLL oracle reveals substantial headroom. Examples:
- original hard: W0 40.54% / 1.31391, C2 46.25% / 1.23536, oracle 61.50% / 0.98777;
- final W1 hard: 40.88% / 1.25246 -> 45.38% / 1.22032 -> oracle 51.83% / 1.10042;
- final W1 easy, where always-on C2 is harmful: 80.96% / 0.40478 -> 74.17% / 0.66709, while query oracle reaches 89.46% / 0.24274;
- final W2 easy seed 27: 92.5% / 0.24285 -> 84.875% / 0.35722, oracle 95.625% / 0.14842.

Damage decomposition is consistent with a local rollback interpretation: prediction flips account for most positive episode damage, but a large correct->correct population also worsens NLL, so “rollback only when top1 changes” is insufficient. Delta entropy is more informative than generic displacement/JS/flip magnitude.

**Decision:** authorize one minimal confirmatory T010. Do not introduce a learned gate or multivariate policy. Use only `delta_entropy` as the primary rollback scalar because it was the strongest preregistered T009 feature and has a simple semantic interpretation.

---

## ACTIVE TASK — T010

**Title:** Train-only calibrated query rollback — can a single delta-entropy threshold convert C2 into safe vocabulary-conditioned specialization on fresh novel streams?

**Status:** ACTIVE

### Research question
Test the narrow deployable hypothesis:

> After computing the unchanged O1+C2 candidate, a query should keep C2 only when its entropy change is below a globally calibrated threshold; otherwise it should roll back to the W0 query output. A threshold calibrated on base/source semantic episodes should transfer across model seeds and to fresh held-out novel-vocabulary episodes without using novel labels at runtime.

This is the final synthetic validation before any detector integration. T010 must remain a **single-scalar, single-threshold, post-candidate rollback policy**.

### Policy
For query `j`:

`dH_j = H(p_C2_j) - H(p_W0_j)`.

Given a scalar threshold `tau`, use:

- C2 output/token if `dH_j <= tau`;
- W0 output/token if `dH_j > tau`.

Higher delta entropy predicted harm in every T009 fold; do not reverse this orientation in T010.

Report probability-output selection and the corresponding selected query token so the mechanism remains compatible with a later detector/query representation path. Do not blend probabilities or embeddings in the primary policy.

### Primary checkpoint grid
Use only the three scientifically important state groups, for each seed 7/17/27:
1. original T002-P / T005 frozen state;
2. T007 W1 (`P_O0_resume`) step 400;
3. T007 W2 (`P_C2_warm`) step 400.

These nine states are primary. Intermediate T007 trajectory states 50/100/200 may be reported only as secondary diagnostics and may not determine pass/fail.

All source checkpoint hashes must match the existing T005/T007 receipts.

### Fresh data requirement
Do **not** validate the policy on the T002-T009 held-out episode rows already inspected.

Before generating/scoring any new policy outcomes, commit `research_log/t010/PLAN.md` fixing:
- exact checkpoint hashes;
- exact generator version/config;
- deterministic namespaces/index ranges for calibration and validation episodes;
- episode counts;
- threshold candidate construction and tie-break;
- all pass/fail rules below.

Use two disjoint fresh streams:

**Calibration stream:** source/base semantic split (`train`), fresh episode IDs never used by earlier tasks. Include both easy and hard vocabularies, but do not use regime name as a policy input. Labels may be used **offline only to calibrate tau**.

**Validation stream:** held-out/novel semantic split (`test`), a new deterministic episode namespace/index range disjoint from every T002-T009 evaluation episode and from T010 calibration. Validation labels are scoring-only and may not affect tau or any policy choice.

Recommended minimum: at least 100 easy + 100 hard episodes per primary state for calibration and at least 200 easy + 200 hard per primary state for validation, unless memory/runtime constraints require a preregistered reduction before outcomes are viewed.

### Cross-seed calibration protocol
Use leave-one-model-seed-out validation.

For each held seed `s`:
- pool calibration episodes from the other two seeds across the three primary state groups;
- compute `dH` without labels;
- construct a fixed threshold candidate grid from calibration `dH` values only (e.g. preregistered quantiles plus +/- infinity); candidate construction cannot use validation data;
- use calibration labels to select the single `tau_s` minimizing mean per-query NLL of the rollback policy;
- use a deterministic preregistered tie-break;
- freeze `tau_s` and apply it unchanged to all three primary states and both easy/hard novel validation streams for held seed `s`.

No branch-specific, state-specific, regime-specific, vocabulary-specific, or query-class-specific thresholds.

### Required baselines
On exactly the same fresh validation episodes, report:
- `R0`: W0 only;
- `R1`: always-on unchanged O1+C2;
- `R2`: primary calibrated `delta_entropy` rollback;
- `R3`: fixed zero-threshold rule `dH <= 0` as a no-label/no-calibration diagnostic baseline;
- offline per-query NLL oracle ceiling, clearly marked non-deployable.

Do not add thresholds for the other T009 features in the primary experiment. T009 selected `delta_entropy`; T010 is confirmation, not another feature search.

### Primary metrics
Report equally weighted per-seed and aggregate:
- query/episode NLL and accuracy;
- easy and hard separately;
- original / W1-final / W2-final separately;
- C2 retention rate (fraction of queries using C2);
- W0->wrong/C2->correct gains retained and W0->correct/C2->wrong damages rolled back;
- performance as a fraction of the oracle rollback headroom.

Use episode-level bootstrap confidence intervals only if preregistered before validation outcomes; do not treat correlated query rows as independent samples for inferential CIs.

### Preregistered success gate
T010 passes only if all clauses hold on **fresh novel validation streams**:

**1. Cross-seed robustness.** For every held seed, R2 aggregate validation NLL is lower than R0 and no worse than R1 by more than 0.01 nats. Aggregate accuracy must not be lower than both R0 and R1.

**2. Hard-utility retention.** For each of original, W1-final and W2-final groups, when R1 has a positive hard gain over R0, R2 must retain at least 75% of the R1 hard NLL improvement and at least 70% of the R1 hard accuracy improvement. If R1 does not improve a metric, R2 must not materially degrade that metric versus R0 (>0.01 NLL or >1 percentage point accuracy).

**3. Easy-harm removal.** For every held-seed/state easy case where R1 worsens R0, R2 must remove at least 60% of the R1 NLL regression and at least 50% of the R1 accuracy regression. For cases where R1 is beneficial, R2 should retain at least 50% of that positive NLL gain or remain within 0.01 nats of R0.

**4. Non-degenerate usage.** Across each held seed, R2 must use both W0 and C2 on validation queries; overall C2 retention rate must lie between 10% and 90%. This prevents a trivial always-W0 or always-C2 solution from passing as rollback.

**5. No validation tuning.** Thresholds, orientation, candidate grid, tie-break, episode namespaces, and rules must be committed before validation outcomes are read. Any post-outcome policy change invalidates the confirmatory gate and requires a new task rather than silently rerunning T010.

### Interpretation
If T010 passes, report the method concept as **query-local entropy-consistent fast semantic specialization**: C2 remains a post-candidate fast semantic expert, while W0 is a safe residual path, selected per query by a base-calibrated label-free entropy-change criterion. Passing T010 may justify a separately scoped small detector integration task, but do not start Grounding-DINO integration autonomously.

If T010 fails, terminate the current O1+C2 rollback line. Do not fit multivariate gates, neural controllers, state-specific thresholds, or retune C2. Recommend a higher-level non-destructive reframe instead.

### Required engineering evidence
- preregistered plan committed before fresh outcomes;
- exact checkpoint/generator hashes and fresh episode IDs proving no overlap with T002-T009;
- tests that validation labels cannot affect threshold or runtime selection;
- deterministic threshold calibration with LOSO seed isolation;
- exact R0/R1 reproduction logic on fresh streams;
- per-seed/state/regime CSV/JSON plus threshold/usage receipts;
- local + A6000 CPU/CUDA tests because T010 reconstructs/runs the model and C2 on fresh episodes;
- `coordination/CODEX_TO_CHATGPT.md` with explicit gate-by-gate pass/fail and exact commands/environment.

### Prohibited in T010
- any feature other than `delta_entropy` in the primary rollback decision;
- learned/multivariate gate, logistic/MLP controller, output blending, state/regime-specific threshold;
- validation-label threshold tuning or reorientation;
- objective/temperature/eta/architecture/generator changes after preregistration;
- new meta-training or checkpoint selection;
- Grounding-DINO/detector integration before Research Lead review.

**Wait for Research Lead review after T010.**