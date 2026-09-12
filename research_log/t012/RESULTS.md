# T012 final result

The fixed success criterion fails. Stop the synthetic TOVD mechanism program and submit SYNTHESIS.md for Research Lead review; no further mechanism or detector work.

Calibration run `20260912-141907-tovd-t012-cal-a6000`. Tested implementation `8c4abff9140f1d762175472117bf6b9c3d5fcb21`; preregistration `15d3353`.
One global lambda = **0.2**, chosen from 14400 fresh base queries across all nine states. This value is shared across seeds, states and regimes.

| Lambda | Base calibration NLL | Accuracy % |
| --- | --- | --- |
| 0.0 | 0.553871328 | 79.38194 |
| 0.05 | 0.553461626 | 79.47222 |
| 0.1 | 0.553127343 | 79.47917 |
| 0.2 | 0.552682552 | 79.37500 |
| 0.5 | 0.553100711 | 79.15972 |
| 1.0 | 0.559460702 | 77.52778 |
| 2.0 | 0.592983160 | 73.87500 |

Base W0 NLL 0.553871328. Selection minimizes global base NLL; ties within1e-12 use the smallest exponent. No novel outcomes enter calibration.

Novel run `20260912-142634-tovd-t012-val-a6000`, actual-lambda freeze commit `22ffbdf8d7952eb8450097cfb84ef0cbef5c4d0e`. 1,800 fresh novel episodes /14,400 queries; 600 unique scene seeds paired across nine frozen states. Calibration and novel namespaces are 4 billion and 5 billion, disjoint from T002–T011.

## Fixed gates

| Gate | Result |
| --- | --- |
| 1 | FAIL |
| 2 | FAIL |
| 3 | PASS |
| 4 | PASS |
| 5 | PASS |

| Scope | Gate | A2-A0 NLL | Accuracy change pp | Pass |
| --- | --- | --- | --- | --- |
| group/original_P/easy | 3 | -0.003678625 | 0.37500 | True |
| group/original_P/hard | 1 | 0.002717843 | -0.91667 | False |
| group/P_O0_resume/easy | 3 | 0.009650195 | -0.45833 | True |
| group/P_O0_resume/hard | 1 | 0.003113490 | -0.41667 | False |
| group/P_C2_warm/easy | 3 | -0.003227737 | -0.12500 | True |
| group/P_C2_warm/hard | 1 | 0.001049049 | -0.20833 | False |

| Group | Improving hard seeds | Worst NLL regression |
| --- | --- | --- |
| original_P | 0 | 0.003026330 |
| P_O0_resume | 1 | 0.006371123 |
| P_C2_warm | 1 | 0.003627204 |

Localization: A2_minus_A3_hard_nll=-0.000270160, A2_minus_A3_easy_nll=-0.003778699.
Strict improvement comparisons use the preregistered1e-6-nat numerical tolerance; the full signed deltas and five clauses are in gates.json. The three hard-group A2-A0 NLL deltas are positive, so their failure does not depend on that numerical tolerance.

## Complete controls

| Scope | Method | Accuracy % | NLL |
| --- | --- | --- | --- |
| overall | A0 | 63.04167 | 0.840656346 |
| overall | A1 | 62.82639 | 0.853280162 |
| overall | A2 | 62.75000 | 0.842260382 |
| overall | A3 | 62.93056 | 0.844284812 |
| overall | A4 | 65.04167 | 0.809261020 |
| group/original_P/easy | A0 | 81.16667 | 0.478736668 |
| group/original_P/easy | A1 | 82.12500 | 0.452898160 |
| group/original_P/easy | A2 | 81.54167 | 0.475058043 |
| group/original_P/easy | A3 | 81.75000 | 0.481242328 |
| group/original_P/easy | A4 | 87.33333 | 0.326039095 |
| group/original_P/hard | A0 | 45.25000 | 1.260315190 |
| group/original_P/hard | A1 | 44.00000 | 1.283625394 |
| group/original_P/hard | A2 | 44.33333 | 1.263033033 |
| group/original_P/hard | A3 | 44.79167 | 1.264053909 |
| group/original_P/hard | A4 | 42.33333 | 1.272977822 |
| group/P_O0_resume/easy | A0 | 82.95833 | 0.370548539 |
| group/P_O0_resume/easy | A1 | 80.45833 | 0.454121969 |
| group/P_O0_resume/easy | A2 | 82.50000 | 0.380198734 |
| group/P_O0_resume/easy | A3 | 82.41667 | 0.380789915 |
| group/P_O0_resume/easy | A4 | 77.33333 | 0.594429316 |
| group/P_O0_resume/hard | A0 | 43.66667 | 1.202480514 |
| group/P_O0_resume/hard | A1 | 43.45833 | 1.243237077 |
| group/P_O0_resume/hard | A2 | 43.25000 | 1.205594004 |
| group/P_O0_resume/hard | A3 | 43.70833 | 1.204452756 |
| group/P_O0_resume/hard | A4 | 46.62500 | 1.171639627 |
| group/P_C2_warm/easy | A0 | 81.91667 | 0.468298364 |
| group/P_C2_warm/easy | A1 | 84.04167 | 0.433820143 |
| group/P_C2_warm/easy | A2 | 81.79167 | 0.465070628 |
| group/P_C2_warm/easy | A3 | 81.75000 | 0.469631258 |
| group/P_C2_warm/easy | A4 | 89.54167 | 0.295638767 |
| group/P_C2_warm/hard | A0 | 43.29167 | 1.263558803 |
| group/P_C2_warm/hard | A1 | 42.87500 | 1.251978226 |
| group/P_C2_warm/hard | A2 | 43.08333 | 1.264607852 |
| group/P_C2_warm/hard | A3 | 43.16667 | 1.265538704 |
| group/P_C2_warm/hard | A4 | 47.08333 | 1.194841495 |

A0=W0; A1=unchanged B1 activation formula on the same frozen state; A2=static local PoE; A3=static uniform PoE; A4=unchanged C2 historical diagnostic only. A1 is not a separately trained B1 checkpoint. Full seed/state/easy/hard cells are in summary.csv.

## Engineering evidence and inference boundary

Local108passed53.20s. Remote CPU/CUDA calibration prerequisite suites: [{'passed': 108, 'seconds': 9.36}, {'passed': 108, 'seconds': 27.36}]. All calibration/validation engineering validity checks pass: True/True.
A0/A1/A4 exact replay: True/True/True. Model tensors unchanged: True; static inference tensors/no parameter gradients: True/True.
Maximum historical NLL discrepancy 3.62051651e-07; accuracy discrepancy 0. All model, generator, config, source/checkpoint and tested implementation hashes match. The same frozen calibration dictionary appears in both phases.
A0/A1/A2/A3 execute under inference_mode. A2/A3 contain no gradient, optimizer, residual state, parameter copy, learned gate, task label or task ID. Only the explicitly requested separate A4 historical C2 call computes its established inner gradient; it cannot affect static outputs or lambda. No outer training occurs.

Environment: `{"cuda": "12.1", "device": "cuda", "gpu": "NVIDIA RTX A6000", "lambda_commit": "22ffbdf8d7952eb8450097cfb84ef0cbef5c4d0e", "python": "3.12.12", "revision": "8c4abff9140f1d762175472117bf6b9c3d5fcb21", "time_utc": "2026-09-12T06:27:48.198676+00:00", "torch": "2.4.0+cu121"}`.

## Diagnostics, artifacts and reproduction

localization.csv contains per-cell teacher diversity, attention entropy/effective token count, A2-A3 probability L1/KL and class differences. All query probabilities/log probabilities, teachers/attention, offline metrics and phase IDs are preserved in18 raw gzip JSONL files per phase. Calibration saves p0/teacher plus every grid loss, sufficient to reproduce each candidate without regenerating images.
artifact_manifest.json hashes all 52 original files; receipt files preserve run commands, start/end, tests and environment. Original train.log records the frozen-lambda file SHA256 before novel execution.
`bash scripts/run_t012_calibration_a6000.sh`, then commit actual frozen_lambda.json, then `bash scripts/run_t012_validation_a6000.sh` with TOVD_SOURCE_REVISION and TOVD_LAMBDA_COMMIT set to the recorded commits.
`python -m research_log.t012.write_report --cal-run research_log/remote_runs/20260912-141907-tovd-t012-cal-a6000 --val-run research_log/remote_runs/20260912-142634-tovd-t012-val-a6000` regenerates reports without model execution.
No post-outcome lambda, teacher, temperature, source, generator or criterion changes. This is a controlled synthetic audit, not detector accuracy or a universal impossibility claim.
