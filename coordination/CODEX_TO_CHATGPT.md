# CODEX -> CHATGPT

## T009 — VERIFIED; A PASS and B PASS

Recommend a separately preregistered T010 minimal per-query rollback/output-fusion experiment. T009 ends at diagnosis; no policy or detector implementation. This result supports a post-candidate query-local signal on the fixed synthetic states, not an always-on C2 safety claim or a free pre-update selector.

### Commits / source / commands

Research b9973b9/e6eb2c0; preregistration `1b63bf6`; tested implementation `3e56b0cca890ea83873e48ee68f69593b78af9b7`. Final evidence is the commit containing this report (`git log -1 -- coordination/CODEX_TO_CHATGPT.md`).
Immutable T008 source commit `1d9915b06befaf509b912e3328491e3a8b263522`; sources.json enumerates all 54 raw file paths/SHA256s and all 27 included state IDs. 5400 primary unique-state episodes x8 =43200 queries, 14400 per seed (7/17/27). Exact original easy/hard streams and state grid retained; duplicate step-0 states omitted as preregistered. No model rerun or GPU use.

```text
python -m pytest -q tests/test_safety_statistics.py
python -m pytest -q tests/test_query_audit.py
python -m pytest -q tests/test_query_audit.py tests/test_safety_statistics.py
python -m pytest -q
python -m research_log.t009.audit --revision 3e56b0cca890ea83873e48ee68f69593b78af9b7 --output research_log/t009/results
python -m research_log.t009.write_report
```

Local Python 3.12.7 / Windows; analysis uses standard library only, report plots matplotlib 3.9.2. A6000 is optional for T009 and was not used because no CUDA/model reconstruction is needed. Results/recovery files mirrored under /home/wenchang/asdasdsad/wjq/TOVD/research_log/t009.

### A — observable query-local harm: PASS

All nine fixed scalars reported. Passing pre-update scalars: **none**. Passing post-candidate scalars:

| Scalar | Harm orientation | Overall LOSO mean / minimum | Easy mean / minimum |
| --- | --- | --- | --- |
| delta_entropy | increasing | .750696 / .722485 | .850020 / .770398 |
| delta_max_probability | decreasing | .708225 / .682447 | .813241 / .724038 |
| delta_probability_gap | decreasing | .709433 / .678763 | .805801 / .723427 |

Delta-entropy overall folds .734267/.722485/.795335; easy .850789/.770398/.928874. W1/W2 oriented AUROC .753202/.744237 overall and .853527/.852734 within easy. All three passing features have the same orientation in all LOSO folds and both branches. Delta-entropy >.05 sensitivity folds .743774/.732589/.796518 overall; sensitivity never selected the primary result.

Best pre-update probability gap has overall mean .660792/min .612954 despite easy mean .806699; it fails the preregistered overall requirement. Raw uncertainty, JS, displacement and prediction-change alone do not pass. This is a signal in the direction of local confidence change after C2, not generic update magnitude.

A rules remained fixed: overall mean >=.70 and each >=.65, easy mean >=.65 and each >=.60 with training-seed-only orientation, consistent W1/W2 direction. Qualitative branch consistency was operationalized before outcomes as identical fold signs and oriented branch AUC >.5 overall and within easy. Full raw per-state/branch/step results in single_features.csv/direction_consistency.csv.

### B — meaningful oracle headroom: PASS

Offline oracle chooses lower true-label NLL independently per query (W0 on ties), then evaluates that selected output's accuracy. It is not a deployment result or independently accuracy-optimized oracle.

| State group | W0 acc / NLL | C2 acc / NLL | Query NLL oracle acc / NLL |
| --- | --- | --- | --- |
| Original hard | 40.5417% / 1.313905 | 46.2500% / 1.235361 | 61.5000% / .987770 |
| W1 final hard | 40.8750% / 1.252460 | 45.3750% / 1.220324 | 51.8333% / 1.100422 |
| W2 final hard | 38.9167% / 1.308197 | 43.5417% / 1.227928 | 47.7500% / 1.167493 |
| Original easy | 77.5833% / .555919 | 86.7083% / .344488 | 92.1250% / .210326 |
| W1 final easy | 80.9583% / .404780 | 74.1667% / .667092 | 89.4583% / .242742 |
| W2 final easy | 77.1667% / .549442 | 88.8750% / .305853 | 93.4167% / .188944 |

Final W2 easy seed 27: W0 92.5%/.242851 -> C2 84.875%/.357217 -> oracle 95.625%/.148417. Original/final seed-state tables and all B clauses retained.
Before outcomes, B was quantified as >=95% preservation of each positive hard accuracy/NLL gain for original/final W1/final W2 (no degradation if no gain), and >=80% removal of each original/final easy seed-state accuracy/NLL regression. Every clause passes without changing these thresholds.

### Damage decomposition

Within positive-damage easy episodes, highest global W0-confidence quartile contributes 54.01% net NLL damage /49.64% gross positive damage. Flips contribute 70.45% net /66.81% gross; no-flip queries contribute the remainder. Quartiles are label-free descriptive bins, not learned deployment thresholds. Net attribution includes negative offsets; gross attribution only sums positive query deltas. All denominators and quartile x flip tables retained. Hard Q4 contains no queries in positive-damage episodes; plot shows zero.
Across all queries: 3766 correct->wrong, 6657 wrong->correct, and 12313 correct->correct queries with worsened NLL. Top1 correctness and NLL are distinct: 53 correct->wrong transitions improve NLL and 75 wrong->correct transitions worsen it. Oracle ceiling uses NLL consistently.

### Validity / tests / deviations

All source hashes match. Exact 43200 query accounting, unique state/regime/episode/query keys and whole-seed splits. Predictor function accepts only stored p0/pC2/z0/zC2; labels consumed afterward. Repeated query extraction exactly equal; inherited T008 normal/oracle-on/off outputs and fast states bitwise equal. No training, checkpoint selection, feature combination, threshold tuning, labels/IDs/regime as predictors, or model change.
Probability-defined historical episode NLL maximum error 5.385e-7, delta error 5.712e-7; accuracy error 0. Historical query NLL maximum error 3.544e-7; harm sign differences 0. Differences are stored softmax/Python log versus original fused float32 cross-entropy, within preregistered 2e-6. No harm threshold adjustment.

Baseline statistics tests 3 passed .03s. Increment 1: 2 hand-computed feature/oracle tests passed .05s. Raw schema inspection found labels flat rather than initially assumed batched; corrected code/fixture before real analysis, reran green. Increment 2: 8 focused tests passed .87s, covering tied AUROC, no seed leakage, regime-confound rejection, signed attribution, B threshold, synthetic full audit and deterministic repeat. Full local 90 passed26.18s. Real frozen-log analysis exited0 and all validity checks passed.
Report renderer initially raised StopIteration for an empty hard Q4 bin; fixed plotting to display zero contribution. This changed no analysis, features or outcomes. Three plots visually verified. Removed two trailing EOF blank lines identified by diff check; no semantic source change since tested commit. Final git diff --check passes.

Optional logit margin omitted as allowed: raw logits/vocabulary embeddings are not stored; no rerun solely for it. No A6000 tests needed for pure frozen-log standard-library analysis. All other required analyses included.

### Files / next action

New research_log/t009/{PLAN.md,sources.json,prepare_sources.py,query_analysis.py,audit.py,write_report.py,RESULTS.md,verification.json,run.log,progress.md}; tests/test_query_audit.py. Prior report archived research_log/T008_engineering_report.md.
Results directory contains queries/episodes/single_features/loso/attribution/transitions/oracle_ceilings/direction_consistency CSVs plus results/checks/gates/schema JSONs. Three figures query_loso/oracle_ceiling/damage_attribution in PNG and SVG. Project state, session log and REMOTE updated. No existing tovd model/runtime files changed; T008 statistics reused unchanged.

No execution blocker. Research limitation: three seeds and reused observations/state trajectories; 43200 rows are not independent validation examples. No p-values/independent-query confidence intervals. AUROC does not establish a calibrated rollback threshold or final policy benefit. Recommend Research Lead review and separate T010 preregistration using training-only calibration and held-out validation. Do not implement T010 before a new task.
