# T013-DEC1 final disclosure and decision contract

Version: **T013-DEC1-v1**. Frozen before primary outcome, under Lead revision `753facb`. Scientific freeze remains `6fec32243985ccc808123d851abf5f3dea10af99`. This document and its dependency-free metadata function do not compute metrics, duplicate FIN1/replay validation, add scientific criteria, or authorize research acceptance. Their hashes are recorded in `final_decision_contract_receipt.json`.

## Inputs and evidence order

`final_decision_contract.decide(summary)` accepts an in-memory dictionary. It performs no file access and imports no packages. Use only synthetic metadata now. After the primary finishes, assemble a final summary from the complete, unchanged frozen results and the actual FIN1/replay receipts. Do not substitute smoke/preflight PASS for a full-primary PASS.

The envelope requires `contract_version` and `evidence.fin1` / `evidence.full_cache_replay`, each with `status` and a nonempty `receipt_ref`. Status is PASS, FAIL, PENDING, or NOT_RUN. Either non-PASS returns `BLOCKED_NO_SCIENTIFIC_INTERPRETATION` before requesting scientific tables; failure reporting must not invent a completed result. For actual PASS, receipt references must identify the finished primary's FIN1 and deterministic full-cache replay/comparison. FIN1 verifies bytes/provenance; the accepted REPRO1 comparator verifies complete decoded analysis equality. This function consumes their reported outcomes and does not reopen their artifacts or certify their truth.

When both statuses are PASS, the entire disclosure below is mandatory even if Grounding gates fail. Missing fields or shortened arrays raise `ValueError`; they do not become a negative scientific outcome. The caller must correct incomplete reporting without changing scientific analysis. Do not infer a decision until the full report is disclosed and Lead judgments are available.

## Complete frozen scientific disclosure

Copy all 11 `results.json` fields without selecting favorable cells:

| Field | Required disclosure |
| --- | --- |
| kind, image_count | T013-NATIVE30, 1000 |
| conditions | clean, gaussian_noise, motion_blur, fog, jpeg_compression, in that order |
| vocabularies | V0, Vhard30, Vrand30, in that order |
| metric_order | AP, AP50, AR, AR50, canonical_fp_per_image, distractor_fp_per_image, canonical_recall, localization_recall |
| point_metrics | `[5,3,8]`: all 15 cells and all eight metrics; final human report must display the complete AP/AP50/AR/AR50 table and all four per-cell diagnostics |
| metric_ci95 | `[2,5,3,8]`, lower/upper, same cell and metric order |
| replicates, seed | 1000, 20260913 |
| margin_common_localized_gt_counts | all four common-localized-GT counts in corruption order |
| assessment | every field enumerated below |

Required `assessment` fields:

- `D_AP50`, `A_AP50`: each `[4,3]`, including V0 and both hard/random columns for every corruption; corresponding `D_AP50_ci95`, `A_AP50_ci95` each `[2,4,3]`.
- `hard_minus_random`: all four point contrasts, and `hard_minus_random_ci95` `[2,4]`.
- `mean_A_hard`, `mean_hard_minus_random`, and their `mean_A_hard_ci95`, `mean_hard_minus_random_ci95` `[2]` intervals. These are frozen replicate-first paired-bootstrap intervals, not differences of separately computed marginal intervals.
- `gate1` and `gate2` booleans, four `gate1_corruptions` booleans, `gate4_recorded_checks`, `gate3_statistical_support`, and `research_acceptance` text.
- `gate3_diagnostics` must retain **all three** families: `distractor_fp_excess_increase`, `classification_beyond_localization_excess_drop`, and `matched_localization_margin_excess_shrinkage`. Each requires four `per_corruption` values, `mean`, `mean_ci95`, `positive_corruptions`, and `statistical_support`. Negative or unavailable families must remain visible, together with the four common-support counts above. Frozen analysis emits family mean CIs; this contract does not invent additional per-corruption diagnostic CIs.

Preserve unavailable values exactly: frozen `interval()` returns JSON null when any input replicate is nonfinite; undefined margins can be NaN. A **present null interval** is disclosed unavailable, not a missing field and not zero. The human report must explicitly label these unavailable and retain common-support counts. Do not drop undefined replicates, hide negative diagnostics, fill zeros, or fabricate CIs. This behavior is already specified by PLAN; it is not a new threshold or schema blocker.

## Provenance and Lead review

`provenance` requires exact `run_id=20260912-210355-tovd-native30-primary`, `release_id=20260912-210306-tovd-native30-primary-freeze`, and `freeze_commit=6fec32243985ccc808123d851abf5f3dea10af99`.

Also disclose `environment_sha256`, `freeze_sha256`, `plan_sha256`, `analysis_sha256`, `coco_sha256`, `diagnostics_sha256`, `vocabulary_sha256`, `selection_sha256`, `annotations_sha256`, `image_manifest_sha256`, `checkpoint_sha256`, `native_source_revision`, `state_before_sha256`, `state_after_sha256`, `run_receipt_sha256`, `cache_manifest_sha256`, `results_sha256`, `paired_draws_sha256`, `bootstrap_samples_sha256`, and `diagnostics_per_image_sha256`. These are required identifiers, not a second byte-integrity check. Populate them from final receipts/frozen provenance and the completed output manifest. No extra prediction inspection is needed here.

`lead_review` requires explicit boolean `gate3_coherent`, boolean `gate4`, `review_ref`, `gate3_rationale`, and `gate4_history_audit_ref`. Gate3 is the Lead's qualitative coherence judgment after reviewing all families; `gate3_statistical_support` does not replace it. Gate4 combines the recorded checks with the Lead's Git/protocol-history audit: either false means protocol invalid. The function never creates a Lead judgment or marks a research task ACCEPTED.

## Fixed interpretation, in precedence order

| Condition | Exact state |
| --- | --- |
| FIN1 or full-cache replay not PASS | BLOCKED_NO_SCIENTIFIC_INTERPRETATION |
| Gate4 false (recorded checks or Lead audit) | PROTOCOL_INVALID_NO_SCIENTIFIC_INTERPRETATION |
| Gate4 true; Gate1 or Gate2 false | GROUNDING_PRIMARY_NOT_SUPPORTED |
| Gate4, Gate1, Gate2 true; Gate3 coherent | GROUNDING_DUAL_SHIFT_SUPPORTED_MECHANISM_COHERENT |
| Gate4, Gate1, Gate2 true; Gate3 not coherent | GROUNDING_DUAL_SHIFT_SUPPORTED_MECHANISM_UNRESOLVED |

Gate1/2 booleans come unchanged from frozen analysis. This reporting helper does not recompute their arithmetic, already independently tested in STAT1. Their existing definitions remain: Gate1 needs at least two corruptions with A_hard >=1.0 and lower95% CI >0; Gate2 needs mean A_hard >=.75, mean hard-minus-random >=.50, and at least two positive hard-minus-random point estimates. No other scientific threshold is introduced.

Gate3 cannot change `GROUNDING_PRIMARY_NOT_SUPPORTED` to either supported state. Extra `yolo_world` fields are ignored by the function. A future separately authorized YOLO-World experiment can provide cross-backbone evidence only and can never mutate the Grounding state. For a valid Grounding negative, the only allowed forward-looking YOLO statement is: **YOLO-World may later test architecture specificity.** It cannot relabel, replace, or rescue the Grounding primary. Neither a supported state nor this preflight authorizes YOLO runtime, T014, or automatic research acceptance.

## Synthetic verification and source traceability

Run `D:/anaconda3/python.exe research_log/t013/test_final_decision_contract.py` from the repository root. The tests use hand-authored shape fixtures and supplied gate booleans, not measured science or a repeat of STAT1. They exercise all 32 combinations of Gate1/2/Lead3/Lead4/recorded4, each unchanged by hypothetical `yolo_world=PASS`; six non-PASS integrity/reproduction cases (also YOLO invariant); missing table/CI/family/support/provenance/Lead fields; shortened cell/corruption arrays; and explicit unavailable diagnostic support. Statistical support true plus Lead coherence false stays mechanism-unresolved.

The receipt records every fixture outcome and SHA256 of this contract, implementation, tests, and exact frozen source definitions. It compares local source bytes to `git show 6fec322...:<path>` without importing scientific code. Source references are PLAN plus t013_analysis.py (schema, interval semantics, gate/diagnostic fields), t013_coco.py (four metric definitions) and t013_diagnostics.py (prespecified detector diagnostics). FIN1 and REPRO1 documents supply evidence ordering. No active-primary prediction or scientific output is used.

Stop after reporting this package. Continue only normal health metadata checks on the unchanged primary until the next authorized task or the established completion/failure procedure applies.
