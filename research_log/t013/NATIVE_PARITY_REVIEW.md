# T013 native/HF parity failure — Research Lead review required

Recorded 2026-09-12T20:02:47.194079+08:00. Engineering status: BLOCKED on the Lead-mandated cross-implementation prerequisite. T013 scientific Gates 1–4 have not been evaluated; this is not a negative scientific result.

Implementation commit: `92801da` (token matching/native runner), preceding statistics implementation `972c476`, Lead amendment `2c4dbf5` / `28b8718`. Run `20260912-195530-tovd-t013-native-parity` finished 2026-09-12T19:56:42+08:00 with exit 1. Original logs, command, metadata and JSON are in `research_log/remote_runs/20260912-195530-tovd-t013-native-parity/`.

## Fixed comparison

Official native GroundingDINO source `856dde20aee659246248e20734ef9ba5214f5e44`, native checkpoint revision `a94c9b567a2a374598f05c584e96798a170c56fb`, weight SHA256 `3b3ca2563c77c69f651d7bd133e97139c186df06231157a64c507099c52bc799`; HF checkpoint revision `a2bb814dd30d776dcf7e30523b00659f4f141c71`, weight SHA256 `1a2412ef99bd74bcd3c2a246fa1e48581f8889a1300c9051974741314fc042f3`.

Both implementations ran on the A6000 server CPU with their official PyTorch attention paths, frozen FP32 weights and four CPU threads. Native capacity 256 versus HF capacity 1024. Identical HF-processed pixel tensor and 195-token V0 caption supplied to both; compare corresponding raw 900-query normalized boxes and canonical class scores. This comparison has not established whether query reordering contributes to the largest discrepancy; no post-hoc matching alternative was used to rescue the failed fixed comparison.

| Disjoint smoke image | Max absolute normalized box error | Max absolute canonical score error | HF exact replay | Fixed tolerance result |
|---|---:|---:|---|---|
| 139 | 0.0057582706212997437 | 0.0013861777260899544 | True | FAIL |
| 285 | 0.65475285053253174 | 0.0042033293284475803 | True | FAIL |
| 632 | 0.00015962123870849609 | 0.00020853057503700256 | True | FAIL |

Both box and score tolerances were fixed at 1e-4. All three images fail. Native checkpoint has no missing keys; unused unexpected keys are `label_enc.weight` and `bert.embeddings.position_ids`. Native and HF state hashes are each unchanged before/after; different implementations have different state-dictionary representations, so their hashes are not compared to each other.

## Other completed prerequisites

- Matched vocabulary committed before new Vhard/Vrand smoke inference: V0/Vhard/Vrand = 195/408/408 tokens. Distractor contribution bins 2:30, 3:47, 4:3. Vhard and the frozen candidate scores/embeddings/filter are unchanged. Original r3 remains preserved but superseded for primary use.
- Matched JSON canonical UTF-8 LF SHA256 `51554562b216dcad1c693efb7781362efbac55993bc5c10651e8845ec9931977`, byte-identical on Windows/Linux after explicit LF serialization. Initial CRLF SHA is retained in the receipt; no vocabulary content changed in this serialization repair.
- Nine focused tests pass locally and remotely (`20260912-195110-tovd-t013-matched-tests`). COCO cached paired-image accumulation is tested against full duplicated-image re-evaluation including crowd, absent classes and score ties. These are tested analysis primitives, not a completed 1,000-replicate analysis runner.
- Matched HF CUDA smoke `20260912-195118-tovd-t013-matched-smoke-cuda` passes all 45 non-primary conditions, pixel/replay/capacity checks and unchanged state. HF256/HF1024 self-parity does not establish native/HF parity.
- Frozen 1,000 image IDs accepted at `42daa6e`; smoke IDs 139,285,632 are disjoint. Annotations verified. COCO val archive download `20260912-190511-tovd-t013-coco-ranges-a6000` remains active (98/195 parts last observed). Preserve this single writer and collect final archive/hash receipt when complete.
- Old r3 CPU smoke `20260912-193807-tovd-t013-smoke-fixed-cpu` was interrupted on receipt of the token-match amendment; its incomplete logs are preserved without a success claim.

## Commands and files

Run commands are preserved verbatim in each run.sh. The failed parity command is `python -u -m scripts.t013_native_parity --assets /home/wenchang/asdasdsad/wjq/TOVD/shared/t013 --output "$AUTODL_ARTIFACTS_DIR/native_parity.json"`, with OMP_NUM_THREADS=4 and MKL_NUM_THREADS=4. Linux focused test command: `python -m pytest tests/test_t013_*.py -q`. On Windows explicitly expand paths with `$testFiles = @(Get-ChildItem tests/test_t013_*.py | ForEach-Object { $_.FullName })`, then `python -m pytest @testFiles -q`; latest run 9 passed in 0.37s. The first literal-glob Windows invocation found no tests and was corrected without code changes.

New/updated files in this report commit: `.gitattributes` (preserve canonical vocabulary LF on checkout), `scripts/t013_match_vocabulary.py` (LF serialization), `research_log/t013/vocabulary_matched{,_receipt}.json`, this report, `project_state.md`, `t013/IMPLEMENTATION_NEXT.md`, `t013/PREREQUISITES.md`, `session_log.md`, `REMOTE.md`, engineering mailbox, and original raw run directories for interrupted CPU smoke, statistics tests, matched tests/CUDA smoke, native assets and native parity.

Observed provenance issue: the generic workflow's shared local last-release value mislabeled native parity meta.json as `20260912-195321-taisp-t011-full`. Original metadata is preserved. run.sh actually changes into `/home/wenchang/asdasdsad/wjq/TOVD/current`; after completion that symlink resolves to `/home/wenchang/asdasdsad/wjq/TOVD/releases/20260912-194953-tovd-t013-matched-native`. Remote/local source hashes agree: native runner `2ccdc691463e382d015315c1eef2e99e9a9bf17f3ca292410005099f84bea01d`, detector `4800f1471f2de8f964700b683505c7230e078b6833a57afa1e09af6b42babd0d`. No TOVD deployment occurred between dispatch and this observation. Future dispatches must record the resolved project release directly instead of trusting shared last-release metadata; no other project's workflow was changed.

## Required next action

The active Lead mailbox explicitly states: “If native-vs-HF V0 parity fails these fixed tolerances, do not launch the primary audit. Report the mismatch and stop for Research Lead review”. Therefore no further detector experiment, tolerance change, alternate implementation acceptance, primary inference, or T014 work is authorized at this point. Request a Lead decision on the mismatch before continuing detector work. The existing authorized data transfer may finish and its receipts be collected.

Full PLAN, primary image hash manifest, cached primary inference runner and full bootstrap/gate analysis remain incomplete. No primary AP/CI/interaction outcomes exist. No adaptation occurs in T013; inner-loss/gradient/update/reset diagnostics are not applicable to this frozen-detector audit. The 15-minute heartbeat remains active, reading new Lead instructions and collecting the existing download without repeating this failed test.
