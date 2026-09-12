# T011 query-local semantic residual: development screen

The development screen fails. Per the fixed stop rule, recommend terminating the current fast-semantic-state program at the synthetic mechanism level and returning to a static/activation-side OVD formulation. Stop for Research Lead review; no gate/objective/controller rescue.

Run `20260912-133149-tovd-t011-a6000`; tested commit `79e6e2baac5b92dd8b66c1a8a048a4d5013f5d5b`; preregistration `b615642a3b23261dfaed6ebbdb61b423be7f3901`.
Nine frozen checkpoints, 100 easy + 100 hard episodes each; 1,800 episodes / 14,400 queries, 600 paired scene seeds from the fresh 3-billion namespace. No outer training, learned selector or outcome-driven change.

## Fixed criteria

| Criterion | Result |
| --- | --- |
| 1 | FAIL |
| 2 | FAIL |
| 3 | FAIL |
| 4 | FAIL |
| 5 | FAIL |

Full clause arithmetic, including every easy cell and hard seed, is preserved in `gates.json`.

Hard utility and consistency:

| Group | S2 hard NLL gain over S0 | S1 gain retained % | S2 accuracy change pp |
| --- | --- | --- | --- |
| group/original_P/hard | -0.200953 | -462.12 | -15.7917 |
| group/P_O0_resume/hard | -0.056439 | -675.28 | -5.2917 |
| group/P_C2_warm/hard | -0.008623 | -15.39 | -2.2917 |

| Group | Seeds improving hard NLL | Worst seed NLL regression |
| --- | --- | --- |
| original_P | 0 | 0.346356 |
| P_O0_resume | 0 | 0.103313 |
| P_C2_warm | 2 | 0.062520 |

Easy safety: 0 / 9 seed/state cells pass.
Localization: S2_minus_S3_hard_nll=0.016521, S2_minus_S3_easy_nll=0.100662.

## Task metrics

| Scope | Method | Accuracy % | NLL |
| --- | --- | --- | --- |
| overall | S0 | 59.7917 | 0.907915 |
| overall | S1 | 63.1181 | 0.853956 |
| overall | S2 | 29.8264 | 2.419799 |
| overall | S3 | 27.3403 | 2.361208 |
| group/original_P/easy | S0 | 76.5833 | 0.591626 |
| group/original_P/easy | S1 | 84.9583 | 0.382275 |
| group/original_P/easy | S2 | 10.9583 | 4.511001 |
| group/original_P/easy | S3 | 10.3750 | 4.095732 |
| group/original_P/hard | S0 | 42.4583 | 1.294299 |
| group/original_P/hard | S1 | 42.5000 | 1.250814 |
| group/original_P/hard | S2 | 26.6667 | 1.495252 |
| group/original_P/hard | S3 | 25.6250 | 1.465201 |
| group/P_O0_resume/easy | S0 | 79.4583 | 0.441925 |
| group/P_O0_resume/easy | S1 | 74.7083 | 0.700331 |
| group/P_O0_resume/easy | S2 | 28.7083 | 3.439306 |
| group/P_O0_resume/easy | S3 | 18.4583 | 3.859716 |
| group/P_O0_resume/hard | S0 | 42.2917 | 1.247832 |
| group/P_O0_resume/hard | S1 | 44.9167 | 1.239474 |
| group/P_O0_resume/hard | S2 | 37.0000 | 1.304271 |
| group/P_O0_resume/hard | S3 | 37.3333 | 1.292928 |
| group/P_C2_warm/easy | S0 | 76.2500 | 0.582973 |
| group/P_C2_warm/easy | S1 | 88.4167 | 0.318025 |
| group/P_C2_warm/easy | S2 | 36.2083 | 2.471507 |
| group/P_C2_warm/easy | S3 | 33.3333 | 2.164381 |
| group/P_C2_warm/hard | S0 | 41.7083 | 1.288834 |
| group/P_C2_warm/hard | S1 | 43.2083 | 1.232814 |
| group/P_C2_warm/hard | S2 | 39.4167 | 1.297457 |
| group/P_C2_warm/hard | S3 | 38.9167 | 1.289290 |

S0=W0; S1=unchanged global O1+C2; S2=QLSR; S3=uniform-context residual. All methods use identical episodes and offline labels. Complete per-seed cells are in `summary.csv`.

## Mechanism diagnostics

| Measure | S2 | S3 |
| --- | --- | --- |
| acceptance_fraction | 0.99979167 | 0.99965278 |
| inner_loss_before | 2.3236118 | 2.4077988 |
| inner_loss_after | 1.8190237 | 1.9015883 |
| inner_gradient_norm | 7.7531282 | 7.6620246 |
| chosen_eta | 0.041565756 | 0.040480903 |
| backtracking_trials | 1.4641667 | 1.538125 |
| residual_norm | 0.26012696 | 0.23760873 |
| normalized_residual_norm | 0.63533342 | 0.55102473 |
| attention_entropy | 2.9454145 | 3.4657359 |
| effective_token_count | 19.610479 | 32 |
| residual_diversity | 0.41021656 | 0.43024237 |
| teacher_diversity | 0.040466473 | 2.3510724e-09 |
| vocabulary_residual_difference | 0.25646666 | 0.23034417 |
| min_accepted_vocabulary_difference | 0.003163727 | 0.0013354467 |

S2-S3 residual diversity excess = -0.020025808; fixed threshold >=0.01, with S2 diversity >0.001.
Per-cell diversity is in `diversity.csv`; full pairwise cosine matrices, eligible-pair counts, attention, teacher distributions and residual vectors are retained in every raw episode.

## Engineering validity

Validity passes: True. Source/code hashes match. Model parameters byte-unchanged: True. S0/S1 replay bitwise equal: True. Exact zero initialization, query isolation and image/vocabulary reset: True.
Maximum offline score NLL discrepancy 1.1026859e-06; accuracy discrepancy 0. Finite probabilities: True.
Local full suite: 101 passed in 19.16s. A6000 CPU/CUDA suite timings and original commands are in the immutable run train.log / metadata and completion receipt.

Environment: `{"cuda": "12.1", "device": "cuda", "gpu": "NVIDIA RTX A6000", "python": "3.12.12", "revision": "79e6e2baac5b92dd8b66c1a8a048a4d5013f5d5b", "time_utc": "2026-09-12T05:37:54.653063+00:00", "torch": "2.4.0+cu121"}`.

## Implementation scope and limitations

The explicit T011 QLSR cosine teacher uses normalized projected keys and text, tau_t=tau_q=0.2 and student_tau=0.1. Historical S1 uses its original unnormalized key-dot-text teacher. This difference was identified and disclosed before outcomes in PLAN.md. S2 vs S3 isolates query localization under the same new teacher/residual formulation; S1 vs S2 also changes the state parameterization and teacher normalization.
Residuals start at exact zero; independent per-query Armijo uses the original five candidates and c1=1e-4. No slow/model tensor is adapted. No outer/meta-training is claimed for this frozen structural screen; existing meta-gradient tests still pass.
This is synthetic exploratory evidence, not detector accuracy or confirmation. The fixed thresholds, namespace, source states and gates were not changed after outcomes.

## Reproduction and artifacts

`export TOVD_SOURCE_REVISION=79e6e2baac5b92dd8b66c1a8a048a4d5013f5d5b; bash scripts/run_t011_a6000.sh` on physical GPU1. The script runs CPU and CUDA full suites before the screen.
`python -m research_log.t011.write_report --run research_log/remote_runs/20260912-133149-tovd-t011-a6000` regenerates this report, tables and figure without model execution.
`artifact_manifest.json` hashes all 27 original run files. Eighteen lossless gzip JSONL raw files retain every episode/query; queries.csv and episodes.csv allow independent analysis. `implementation_hashes.json` fixes executed source/config/plan bytes; `verification.json` records remote actual hashes.
