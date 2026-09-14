# T014-SEM-P0 — Contract and synthetic harness verified

Status: T014_SEM_P0_CONTRACT_SYNTHETIC_TESTS_PASS_RETURN_TO_LEAD.
Task-start HEAD: 61fb9804c1166681b3aa4fe8f9925c02acc74a34.
Lead instruction: 317abd180231304986bed77384f5708d4ec75476.
Implementation/evidence commit: 457e6fe18e2008b4f56dfb08e2e7bd6800330f52.
Task began with heartbeat2026-09-14T15:15:01.598Z.

## Changes and frozen definitions

- tovd/semantic_shift.py: standard-library-only in-memory clean schema, deterministic representative selection, GT-anchored metrics and oriented contrasts; arithmetic-only dataset delta helper.
- tests/test_semantic_shift.py:14 synthetic unit tests.
- research_log/t014_semantic/PREREGISTRATION.md: exact fields, coordinates, supports, equations, signs, exploratory status, future counterfactual boundary.
- research_log/t014_semantic/tests.txt and source_check.txt: raw test output and no-query/runtime/file-loader source search.
- This report, delivery_manifest.json, engineering mailbox and project recovery/session logs persist the handoff.

For each non-crowd GT and each vocabulary independently, candidate IoU>=0.5; representative maximizes (IoU,score,-selected_order). Continuous positive-area xyxy boxes; exact ties; no query-slot identity. A detection may represent multiple GTs. GT objects are pooled equally across images.

C=GTs with correct V0 representative; L_v=members of C with shifted representative; B_v=all non-crowd GTs with representatives in both conditions, including initially wrong predictions.

- survival=count(correct shifted in C)/count(C).
- semantic_failure=count(incorrect shifted in L_v)/count(L_v).
- takeover=count(distractor shifted in L_v)/count(L_v).
- localization_loss=count(C minus L_v)/count(C).
- box stability=mean and median IoU(V0 box,shifted box) on B_v.
- score_delta=mean(shifted score minus V0 score) on B_v.

Rates return numerator/support/value; summaries return support/value. Zero support returns explicit null, not zero or omitted. Every observation records box/label/score/selected order, correctness and distractor status; missing representative stays null. Hard/random supports remain separately reported, no common-support restriction.

Oriented contrast is H-R for semantic_failure/takeover/localization_loss and R-H for survival/box stability mean+median/score_delta. Positive consistently means greater hard-context degradation; score decrease is descriptive, not proof of detection quality. Any undefined component yields null contrast. Dataset Delta_m(v)=m(clean,V0)-m(clean,v), m=AP/AP50/AR/AR50 under unchanged frozen evaluator semantics/percentage units; HardMinusRandom_AP50=Delta_AP50(H)-Delta_AP50(R). No evaluator or AP computation is invoked; its helper was tested only on invented scalar fixtures.

## Verification

Command: D:/anaconda3/python.exe -m unittest discover -s tests -p test_semantic_shift.py -v
Exit0;14 tests passed in0.003s. Raw output: tests.txt. Fixtures cover all requested cases plus inclusive IoU boundary, pooled GT weighting, representative reuse, crowd exclusion, initially incorrect stability support, missing fields and invalid input boxes/labels.

Source query: rg -n 'query_id|query_index|torch|cuda|open\(' tovd/semantic_shift.py
Exit1 (no matches). Query permutation test changes query IDs independently across conditions, adds query_index, then removes both fields; the entire analysis output remains identical. No file loader or detector/runtime import exists; imports are math and statistics only.

Preflight accepts condition=clean and rejects every other value; synthetic non-clean sentinel/empty/null cases raise ValueError. Missing score raises KeyError; no primary cache is pointed at the helper. git diff --check passed. No new dependency was installed.

Only synthetic fixtures were used. Primary prediction cache/results, real images and real evaluation outputs were not opened or executed; no visual-corruption analysis, AP/Gate recomputation, detector inference, remote runtime/GPU state change, reboot, repair, model/checkpoint load or TTT implementation occurred. No outcome thresholds, success gates, adaptation hyperparameters or TTT objective were designed. Existing T013 clean-cache use is explicitly EXPLORATORY / POST-HOC DEVELOPMENT; future confirmation requires a separately preregistered split/stream. Optional canonical-only top-k decomposition is documented only and deferred until Lead review.

Grounding remains GROUNDING_PRIMARY_NOT_SUPPORTED. Old YOLO visual-shift contingency is paused/superseded; prior evidence preserved. Metadata-only report mirroring does not execute remote diagnostics or runtime work.

Next action: Research Lead review of T014-SEM-P0 before any execution on the completed clean Grounding cache or any TTT method design
Stopped at: 2026-09-14T23:20:50.1258847+08:00

