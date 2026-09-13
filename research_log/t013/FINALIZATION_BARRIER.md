# T013-CLOSE1 completion barrier — T013-CLOSE1-v1

Task-start HEAD **2af6322facef6381835488a639761578b7fd2b16**. Freeze **6fec32243985ccc808123d851abf5f3dea10af99**, dispatch **88668f76b22777459b5792dd28f88075f208c678**. Target run20260912-210355-tovd-native30-primary, release20260912-210306-tovd-native30-primary-freeze. No scientific code or running artifact is modified by this package.

`finalization_barrier.evaluate(binding, completion, fin1=None, replay=None)` is a standard-library metadata function with no I/O, commands, automatic result opening, or scientific calculations. It reports the next permitted step and records that scientific acceptance/restart/resume are never authorized. Only the final state permits a later Research-Lead scientific review. DEC1 and the pending final Gate4/history review remain applicable.

## Ordered states

| State | Required evidence / next step | Scientific content review |
| --- | --- | --- |
| PRIMARY_RUNNING | Writer/tmux alive, unknown termination, missing/mismatched run/release/freeze, or successful wrapper completion not established. Continue metadata monitoring. | Forbidden |
| PRIMARY_FAILED_RETURN_TO_LEAD | Target wrapper reports nonzero exit. Preserve all artifacts and return to Lead; no restart/resume. | Forbidden |
| PRIMARY_COMPLETE_UNVERIFIED | Target wrapper exit0/completed; writer and tmux both gone. FIN1 absent, stale, mismatched, FAIL or PENDING cannot advance. Only missing FIN1 permits first FIN1 execution. | Forbidden |
| FIN1_PASS_READY_FOR_REPLAY | Exact same-run FIN1 PASS with all required bindings. Only absent replay permits first exact frozen replay/comparison. Stale/mismatched/FAIL/PENDING replay remains here with execution disabled, for Lead review. | Forbidden |
| REPLAY_PASS_READY_FOR_RESEARCH_LEAD | Same cache/freeze FIN1 and full replay/comparison PASS, including comparison to the exact wrapper auto-analysis directory. | Later Lead review permitted; scientific acceptance remains false |

Analysis-file existence is deliberately irrelevant while running or unverified. The frozen wrapper normally runs analysis after inference and may create `analysis/results.json` before FIN1: this is neither contamination by itself nor permission to open it. Only existence/stat metadata is allowed there.

After FIN1 PASS, the specifically authorized replay/comparator necessarily parses complete scientific arrays/JSON internally to compare them. This bounded machine comparison is distinct from opening/interpreting their values for research. `primary_result_content_access_authorized` stays false until final readiness; the intermediate `replay_comparison_execution_authorized` grants only that prescribed machine operation. The barrier itself never opens either kind of content.

## Evidence binding and receipt schema

`target(cache_receipt_sha256, manifest_sha256)` fixes the primary identifiers. After successful wrapper completion, derive these two hashes from the completed cache's metadata files. The target records: contract version, task-start HEAD, run ID, release ID, freeze commit, cache path, cache receipt reference/SHA256, manifest SHA256, image/record counts1000/15000, original receipt freeze argument, frozen analysis SHA256 and exact auto-analysis reference directory. A separate `smoke=True` rehearsal target fixes the known3-image/45-cell run; it never grants primary content access.

Accepted tool identities are source hashes, not invented package versions:

- FIN1 version `T013-FIN1@8efe485`, source SHA256 **9d4c604b40677d81fa634715a55c7132dcbe04303a1a8a3021dc11e42273c6a8**.
- Comparator version `T013-REPRO1@5fe57f7`, source SHA256 **6270a32096c536deac8ec878d3cfbfeb1cc067d428781ab7beb09e78cb8acb76**.
- Frozen analysis source SHA256 **74cc73e71385e5d38e3fbe68ff03a0f11da30e67ff39b436da90422f72e99f9c**.

Completion metadata requires matching run/release/freeze, wrapper_completed=true, integer wrapper_exit_code=0, writer_alive=false, tmux_alive=false. Unknown values remain blocked. A known nonzero wrapper result routes to Lead. `analysis_result_exists` may be carried but never supplies readiness.

Each execution envelope contains the exact target `binding`, tool SHA256, receipt_ref, receipt_sha256, and the **unchanged accepted-tool output** as `result`. FIN1's existing result fields uniquely bind mode, scientific freeze, actual receipt freeze argument, run/release, image/record counts, final cache receipt and manifest hashes. The new envelope adds execution provenance that the original verifier does not emit; no frozen/accepted tool schema is patched. Receipt hashes/reference values are collected from actual files/commands at execution time, not fabricated from a status string.

The replay envelope additionally references the exact FIN1 receipt SHA, exact left_dir (primary's wrapper-produced artifacts/analysis), distinct right_dir (fresh scratch replay), analysis/comparator exit0, frozen analysis hash and1000 replicates. Its unchanged comparator result must be PASS and contain all four artifacts with equal=true: results.json,paired_image_draws.npy,bootstrap_samples.npz,diagnostics_per_image.npz. Accepted comparator semantics remain exact decoded JSON/arrays including NaN masks, keys, shapes and dtypes; container byte equality is not required.

The metadata function checks supplied execution provenance; it is not a cryptographic signer or a substitute for running FIN1/comparison. The executor must attach actual command/source/receipt evidence. FIN1/replay preflight success alone cannot be repackaged as primary success. A stale task-start HEAD or a smoke/other-run envelope cannot match the pinned primary target.

## Frozen future command sequence — NOT EXECUTED ON PRIMARY IN CLOSE1

Use existing workflow SSH helpers and existing shared/t013/venv/bin/python. These templates are for after wrapper completion; the barrier does not launch them automatically.

1. Establish exact-run completion from metadata: both writer PID721181 and tmuxautodl-20260912-210355-tovd-native30-primary gone; anchored wrapper `[autodl] exit_code=0` present, and run/release/freeze match committed metadata. If no final marker, continue monitoring. If nonzero, preserve artifacts and return to Lead. Do not inspect auto-analysis contents.
2. On success, record hashes of completed cache/run_receipt.json and cache/cache_manifest.jsonl, accepted FIN1/comparator source hashes and exact run metadata. Run FIN1 below; read only its metadata report. Non-PASS or binding mismatch stops for Lead review.

```bash
/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/fin1/primary_completion_verifier.py --frozen-root /home/wenchang/asdasdsad/wjq/TOVD/releases/20260912-210306-tovd-native30-primary-freeze --cache /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-210355-tovd-native30-primary/artifacts/cache --output /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/fin1/primary_completion_receipt.json
```

3. On exact FIN1 PASS, create a **new** scratch directory, retain command/logs/exit codes, and execute the unchanged frozen analysis without --smoke-only. The example directory is reserved for future full-primary replay; if it already exists, stop and inspect its provenance before selecting a new directory. Never overwrite or clean the original outputs.

```bash
mkdir /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay
cd /home/wenchang/asdasdsad/wjq/TOVD/releases/20260912-210306-tovd-native30-primary-freeze
/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python -m scripts.t013_analysis --annotations /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/coco/annotations/instances_val2017.json --run /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-210355-tovd-native30-primary/artifacts/cache --output /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay
```

4. Only if replay exits0, execute the accepted comparator with **left=actual primary auto-analysis**, right=new replay. The bounded comparison may parse arrays, but no human-facing scientific interpretation occurs. Failure/mismatch is preserved for Lead, without scientific-code repair or retuning.

```bash
/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/repro1/analysis_replay_compare.py /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-210355-tovd-native30-primary/artifacts/analysis /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay --output /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay/comparison_receipt.json
```

5. Assemble the envelopes above from actual metadata/receipt files, including their SHA256, actual arguments/source hashes and completion snapshot. Call `evaluate(binding, completion, fin1_envelope, replay_envelope)` and persist the returned state together with those inputs. Only `REPLAY_PASS_READY_FOR_RESEARCH_LEAD` advances to a later Lead step opening the full DEC1 disclosure. It does not approve Gate1/2/3/4, research acceptance, YOLO runtime or T014.

## Deterministic fixtures and completed-smoke dry-run

Run `D:/anaconda3/python.exe research_log/t013/test_finalization_barrier.py`. Synthetic primary hashes/statuses are explicitly fixtures, not experimental results. Cases cover every ordered state; writer or tmux alive; missing completion; stale completion/run/release/freeze; early analysis file present/absent; noFIN1/replay; FIN1/replay FAIL/PENDING; stale run/release/freeze/cache/receipt/manifest/tool version/task HEAD; tool/receipt hash omissions; incorrect auto-analysis reference; same left/right; wrong FIN1 linkage, analysis source, replicate count or exit; missing comparison artifact; and cross-smoke-to-primary rejection. No state below final readiness authorizes primary result review.

Dry-run reuses exact existing `primary_completion_smoke_receipt.json` and `analysis_replay_receipt.json`, without rerunning FIN1, analysis or a detector. It checks the accepted source hashes, smoke cache receipt/manifest bindings and historical smoke wrapper exit0; process termination metadata is a historical rehearsal input, not a new live process query. It shows complete-unverified -> FIN1-ready -> replay A/B-ready **for smoke only**. The original smoke auto-analysis had a different analysis-source hash and was NOT COMPARED in REPRO1; feeding that existing NOT COMPARED result remains blocked. The A/B rehearsal is not presented as original-auto-analysis parity.

Copies/envelopes are retained in `close1/smoke_rehearsal_envelopes.json`. A scratch-only mutated cache binding in `close1/mutated_smoke_replay_receipt.json` is rejected; original source receipt bytes remain unchanged. The primary target rejects these smoke envelopes. No active-primary scientific file, prediction, image, annotation or checkpoint was opened. Only normal end health is queried remotely and added to the package receipt/handoff.

Stop CLOSE1 after delivery; wait for Lead review and continue the existing15-minute health monitor. Primary finalization/interpretation remains subject to the completion sequence above and existing Lead conditions.
