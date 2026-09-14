# T013-G4B1 — Final bounded history review

**Status: FINAL_GATE4_HISTORY_CLEAN_READY_FOR_DEC1B.** All 20 mechanical checks pass; contextual review found no unresolved protocol discrepancy in committed evidence. This report supplies contextual review alongside the machine inventory; a path-category match alone is not evidence that an action was permitted.

Task-start HEAD: `08785e443282b060cae1943fc7a1fbac4c770e80`. Lead instruction: `745f1d24784376afc128156829bcd65b15ff1661`, followed by review-log commit `08785e4`.
Fixed interval: `cca9af23452870d1a12ba1ab6a78ebe683e49cd1..745efb43d8640f8ac3958bb733d0df44c51c87ff`.
Freeze: `6fec32243985ccc808123d851abf5f3dea10af99`; dispatch: `88668f76b22777459b5792dd28f88075f208c678`.
Run: `20260912-210355-tovd-native30-primary`; release: `20260912-210306-tovd-native30-primary-freeze`.

The endpoint is not moved to this task's implementation or delivery. The later `5b24bd0` mailbox entry, Lead instruction `745f1d2`, and review-log update `08785e4` are outside the audited interval. This task's own commits will be listed in the delivery mailbox, also outside that interval.

## Method and scope

Standard-library Python and local Git only. The helper reuses pure Git/hash functions from accepted G4A1, without invoking its old audit or overwriting its outputs. It compares all 17 protected blobs at freeze and endpoint against the accepted expected SHA256s, and traverses full history with merge-parent diffs to detect intermediate edits/reverts. It inventories every reachable commit and every changed path against every parent, including changes that disappear from the endpoint diff. Each path has a deterministic task-specific category; commits have the union of their path categories and retained subjects, timestamps, parent IDs and name-status deltas. No unknown category is allowed to be silently treated as clean.

Context review used historical Lead mailboxes, engineering reports, retained execution receipts, source text and operational log changes. Scientific result files and prediction arrays were not reopened or decoded. Existing FIN1/comparison receipts are metadata evidence; no verifier, replay, comparator or decision function was executed again. Reported execution counts identify unique events by run, command, launch time and evidence commit; repeated references or updated observation receipts do not count as new executions.

Git and accepted operational receipts can establish the absence of contradictory **committed evidence**. They cannot prove that no unrecorded process or off-repository action ever occurred. This limit applies equally to dispatch counts, outcome blindness and cache preservation.

## Protected science and unique dispatch

The 17-path list and exact freeze/endpoint SHA256s are in `gate4_final_history_receipt.json`, derived from accepted G4A1's ten code paths, six data/config/protocol paths and freeze JSON. The protected-set history search starts at the original scientific freeze, not merely the G4A1 boundary. DEC1 source/document are checked separately for unchanged history. External checkpoint, annotations and state remain bound by the protected freeze and accepted FIN1 evidence; this task does not inspect their remote bytes.

The retained native-run metadata inventory distinguishes `--smoke-only` commands from the one non-smoke primary. Dispatch `88668f7` remains the unique primary inference event. Its run.sh, meta.json, resolved release and freeze-hash record have no later edits. No new run mirror or detector script/test change appears in the bounded interval. Scalar records retain writer PID 721181 through inference; CLOSE2/CLOSE3 record its natural termination and wrapper completion. No committed command launches a second inference, changes its release/checkpoint/vocabulary/corruptions/gates, or resumes/restarts it.

The four merge commits `7ccfe77`, `65fc120`, `546dd93`, `9942a57` preserve concurrent Lead/report updates. `git show --remerge-diff` produces no conflict-resolution patch for any of them. All-parent changes remain included in the receipt inventory.

## Outcome-blind preparation and its exceptions

| Package | Authorization / evidence | Inspected basis and classification |
| --- | --- | --- |
| G4A1 | prior assignment; `6a96f88`, delivery `96bcf62` | History-only report/helper/receipts. Its initial smoke-command misclassification and initial receipt remain preserved; the corrected smoke flag classifier does not alter primary science. |
| CLOSE1 | `a3cac7c` / `2af6322`; `0acbd4f` | Pure metadata barrier plus synthetic fixtures and already completed smoke envelopes. The deliberately mutated smoke envelope is a negative fixture, not mutation of primary cache. Future commands in the contract are not execution receipts. |
| OPS2–OPS6 | `e380d14`, `6ecbc36`, `0d82576`, `86f4d61`, `8a58598` | Scalar/process reporting, tests and authorized two-point aggregate storage accounting. Source reads are restricted to run metadata, anchored progress/exit lines, process state, result existence and aggregate du statistics. No prediction decoding. |
| CF1 | Lead `098cdad` / `56c8099`; source `d8d3beb`, evidence `8154004` | Driver pins `20260912-205428-tovd-native30-pipeline-smoke`, checks completed smoke receipt, IDs 139/285/632 and 45 cells. All receipt paths lie in that smoke cache. Five synthetic tests and selection identity checks; no annotations or COCO metrics. |
| CF2 | Lead `58c1b97` / `a1588cb`; source `dddb0e8`, correction `2711871`, evidence `b185ee5` | Driver pins the same three-image smoke cache and existing REPRO1 smoke reference, with two scratch outputs under shared/t013/cf2. Receipt records 45 smoke cells per replay and 10 paired draws for three images. Eight committed array/descriptor output files belong to those smoke replays, not the primary. |
| MECH1 | Lead `afc7c64`; evidence `8855eba`, delivery `c699e77` | Static trace of seven archive-bound native source files and three frozen wrappers, plus license/archive/hash transcript. No model import, checkpoint, annotation, inference or primary cache access. Source copies are not an alternative deployed release. |
| MECH2 | Lead `7c58079` / `3782300`; preregistration `f8c2f68`, evidence `8ed8295` | Tests construct torch.arange/ones/tensor fixtures and call the isolated selector. Six methods each on CPU and A6000 cuda:1; no image/model/checkpoint. Contract explicitly leaves primary proposal-lock experiment NOT RUN and prohibits it if Gate1 or Gate2 fails. This is not T014. |

CF1 and CF2 executed driver/source SHA256s match their committed endpoint source bytes. Their path bindings and completed smoke receipts are recorded in the machine audit. MECH1/MECH2 receipts explicitly attest source-only/synthetic-only scope, supported by the inspected source and commands.

CF2's real initial failure is retained in `canonical_counterfactual_initial_blocked_receipt.json`: a reference-receipt hash mismatch stopped before tests/reference output/evaluation (`replays=[]`, `reference={}`). The `2711871` patch removes only the unrelated later `end_primary_health` field from the REPRO1 receipt digest, while retaining every execution field. It precedes `b185ee5` evaluation and was explicitly accepted in Lead `afc7c64`. It does not change the CF1 selector, primary source, metrics or statistical definitions. This exception is not hidden as an unexplained pass.

MECH2 records an NVML mismatch with successful Torch CUDA toy tests; no driver repair or primary device change occurred. All smoke statistics and synthetic tests remained engineering checks, not task-selection evidence derived from the active primary. The prescribed CF/MECH tasks precede authorized primary outcome disclosure and do not change protected science.

## Operational incidents and preservation

OPS7 (`1792062`, delivery `eff1c82`) stopped at its second point with STORAGE_RISK_RETURN_TO_LEAD while PID 721181 and the exact tmux session remained alive. It did not kill or repair the run. Lead `6101219` / `7aa8711` then explicitly authorized OPS8's two redundant download archives only.

OPS8 (`b738711`, completed `7909fa4`, delivery `a43b77a`) records regular-file/path/size checks, existing extracted images and annotation JSON, retained frozen receipts and exact writer file-descriptor inspection before this command:

```bash
rm -- /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/coco/val2017.parallel.zip /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/coco/annotations_trainval2017.parallel.zip
```

The two validated sizes are 815585330 and 252907541 bytes (sum 1068492871). These are reproducible download assets, not extracted scientific inputs or prediction cache. Exact deletion success marker and pre/post/two-later scalar observations are preserved in `ops8_reclamation_receipt.json`; no other deletion is recorded or authorized. Frozen source/input receipts and primary command stayed intact.

OPS9/OPS10 continued unchanged scalar monitoring. OPS10 observed an unexplained large free-space increase. Its cause remains unknown; the record does not attribute it to Codex or infer a cache mutation from df. Later FIN1 checks the completed cache's expected 15000 opaque records and manifest/source bindings, and the one full replay matches canonical analysis. These accepted checks and the protected Git history reveal no scientific discrepancy; they do not identify the external cause of the free-space change.

Transport interruptions in CF2, OPS8, OPS9/OPS10, CLOSE2 and the GitHub outage before CLOSE3 concern receipt synchronization or mailbox access. Existing bounded retries/merges preserved receipts, including outage and recovery notes (`81feb1f`, `ddef8e9`, `57cdd15`, `1c0726f`, `577ebf5`, `9942a57`). They did not retry scientific commands. CLOSE2's process ambiguity (`385bfac`) was correctly preserved and returned to Lead before CLOSE3; it was not silently interpreted as successful completion or used to restart the writer.

## Completion, authorization and disclosure chronology

| Event | Evidence / authorization | Scope and count |
| --- | --- | --- |
| CLOSE2 stop | `385bfac` | 1000 images alone did not authorize outcome access; PID absent and tmux alive returned process ambiguity. |
| CLOSE3 terminal capture | Lead `34194fd`; evidence `7820349` | Exact wrapper finished 2026-09-14 02:38:30+08, exit 0, original writer/tmux absent. Completion marker/result existence only; PRIMARY_COMPLETE_UNVERIFIED. |
| FIN1P | Lead `f985670`; `8b00e1e` | Exactly one command 03:34:29–03:34:47+08, exit 0. Opaque integrity only, analysis_content_opened=false, npz_deserialized=false. |
| Full replay | Lead `d4c91ab`; launch `688f36b` | Exactly one launch 04:44:53+08, PID 1104124, tmux t013-close1-primary-replay. Frozen analysis/source/release, fresh scratch, no environment retuning. |
| Replay completion | Lead continuation `13a2216`; `eb90ff9` | Same launch/PID, natural finish 06:09:11+08, exit 0 after 5058 seconds. Observations did not relaunch it. |
| Decoded comparison / CLOSE1 readiness | Lead `1ae41f3`; `60c99b1` | Exactly one comparator 07:16:22+08, exit 0. All four decoded artifacts equal; no human scientific values disclosed. Actual CLOSE1 result authorizes content access. |
| Canonical disclosure | Lead `94582bd`; `cfe2472`, delivery `0a6b515` | Exactly one canonical copy. Complete machine/human packet and validation PASS, no new statistic or decide call. Three scientific disclosure paths first appear in cfe2472 and are unchanged through endpoint. |

FIN1 receipt reference: `/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/fin1/primary_completion_receipt.json`, SHA256 `ade691d9765ee09b740ba7a7e24262ee55b272d82d5fd79889659fd6d67df63e`.
Comparator reference: `/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay/comparison_receipt.json`, SHA256 `a22ac31a351080b8860838beda92eb318c2a7ddfb422e2a8be29082388110eef`.
CLOSE1 envelope: `research_log/t013/replay1c/replay_envelope_and_barrier.json`; its endpoint digest is retained in the new audit receipt.
DEC1 source remains `T013-DEC1-v1`, SHA256 `baf99f38a3130c268385ddc4c986cd72d123bfb55e7fed29a90b88d289570931`.

The replay and comparator necessarily parse completed scientific arrays under their explicit reproducibility authorization. That is not an unauthorized human preview of active-primary results: the primary was already complete, no metric values were disclosed in their receipts, and no result-dependent tuning followed. Before that point, primary observations are metadata; scientific-valued CF2 files are explicitly smoke-bound, and CLOSE1 fixtures are explicitly synthetic. The path/commit classification, receipt scope and inspected commands reveal no committed active-primary AP/AP50/D/A/CI/diagnostic/prediction content used for tuning or task selection before authorization.

DEC1A's metadata receipt preserves the explanation for opaque output-identifier hashing: earlier accepted receipts lacked those three artifact digests. No arrays were decoded to assemble them. Original canonical bytes were copied once; existing validation proves full field/order/type equality and complete disclosure. This audit inspects that validation receipt and Git history, not the outcome values again. No post-disclosure repair, selective edit, second analysis/comparator, threshold change or source/cache mutation is recorded.

The three final commits `5cc83e9`, `a79aca4`, `745efb4` each change only `research_log/session_log.md`, adding mailbox-check notes. Their complete diffs contain no new scientific action. YOLO-World scientific runtime count is zero: no YOLO preparation path changes in this interval, no new run metadata, and package scope explicitly retains preparation-only status inherited from G4A1. T014 and proposal-lock primary-science runtime counts are zero; MECH2 toy tests are classified separately above.

## Commands and handoff

Executed: `D:/anaconda3/python.exe research_log/t013/gate4_final_history_audit.py`; local Git fetch/fast-forward and ordered mandatory document reads; bounded `git log`, `git diff`, `git show`, `git show --remerge-diff`, `rg` and standard-library receipt/source inspection. The helper records all-parent history using rev-list/show/diff, protected intermediate history using `git log --full-history -m`, and ancestry using merge-base. No research test suite was rerun; validation consists of the focused Git/hash/binding checks and contextual review in this report.

No scientific result was recomputed or reinterpreted; no criterion was changed; `final_decision_contract.decide(...)` was not called. No new detector, YOLO, T014 or CF/MECH scientific runtime occurred. Final Gate4 and final Grounding state remain Research-Lead decisions. A clean result recommends only **DEC1B final Grounding adjudication**; any blocker would instead return to Research Lead without evidence repair.


## Completion inventory

170 commits, four merges, 186 changed paths, zero unclassified paths. The mechanical helper initially emits MECHANICAL_CHECKS_PASS_PENDING_CONTEXT_REVIEW; the final receipt preserves that value in mechanical_status and adds the completed contextual review explicitly. It does not automatically infer protocol validity from filenames. The accepted G4A1 helper/report/receipts remain unchanged.

| Category | Changed paths |
| --- | --- |
| coordination | 3 |
| project operational handoff | 3 |
| CF2 completed smoke arithmetic and replay | 18 |
| CF1 completed smoke selection | 7 |
| CLOSE2/CLOSE3 terminal metadata | 12 |
| DEC1A authorized disclosure | 7 |
| FIN1P single primary opaque integrity check | 9 |
| CLOSE1 metadata barrier and smoke fixtures | 6 |
| G4A1 accepted history audit | 4 |
| MECH1 static source provenance | 16 |
| OPS metadata observations, storage accounting and tests | 68 |
| MECH2 synthetic tensor preparation | 7 |
| REPLAY1A/B one primary replay and observations | 13 |
| REPLAY1C single decoded comparison and authorization | 13 |

| Protected path | Freeze = endpoint SHA256 |
| --- | --- |
| scripts/t013_native_detector.py | b49f23f131777f08e23131ad55a94d9211c33b1c759adf86c6b52e2b95c34126 |
| scripts/t013_native_run.py | 177176fdb1c133b98770f8e6719b22e3ead0a00adbdced598e92326aec723429 |
| scripts/t013_native_smoke.py | d30430f324d0577afc6997c38d78d6f46b78679cb2adaf96055986344928a421 |
| scripts/t013_analysis.py | 74cc73e71385e5d38e3fbe68ff03a0f11da30e67ff39b436da90422f72e99f9c |
| scripts/t013_coco.py | bd3245235a6dcd455224ea7eb737b07875920b0a08b34f30e706dfc6a9ca9e81 |
| scripts/t013_diagnostics.py | ae7e61feaa5701ca9580c9c48901f99d09e9986b560c2821073100c94645a41e |
| scripts/t013_detector.py | 4800f1471f2de8f964700b683505c7230e078b6833a57afa1e09af6b42babd0d |
| scripts/t013_text.py | 2c175a779304f045267e3419eda04dbc2e5c4730ae19cce23727043832102018 |
| scripts/t013_native_vocab.py | 61d40e7f4107a2a13eaa7cd872667acaa4db3dffb3a257e2cddbaece4f943351 |
| scripts/t013_data_receipt.py | 9ef780aa724d3a8a6f685dc0a273a285e7ce17942985fb107c2638810f54305e |
| research_log/t013/PLAN.md | 5d977aceb3c06a7915396aea9c7cc2504759e584ce79b459a287b18fb67e4beb |
| research_log/t013/vocabulary_native30.json | 3bb4a0ebada1f9da407ae6a94f1135798dba7117bd658a6ecba97b2ebfad0967 |
| research_log/t013/image_selection.json | 8039a70f25c34f295345e63d1980f692631b6bbdaa5c37267a10852acbf3833b |
| research_log/t013/data_receipt.json | 4dc1361b17a9221b278dd70ac805afb4d87742451b310af5381dc69900fe8c50 |
| research_log/t013/image_sha256.json | 38eb39894b8c0f1924e099b3a1ec0b885fdf7ec43c86933e1dc28186d85c3ba8 |
| research_log/t013/native30_environment.txt | 6fdb8b3da35dddb24c5ea602e81b160ab864e792ca29fa27236dd759a6b4f090 |
| research_log/t013/native30_freeze.json | 50addfb8e247333b49fb22cda14570166b294101bb435b5a1b5bf688b4b3a91e |

Final history finding: no committed evidence of duplicate/restarted primary, unauthorized pre-disclosure outcome use, outcome-dependent tuning/rescue, scientific cache/config mutation, unapproved YOLO/T014 runtime, or post-disclosure alteration through the fixed endpoint. This supplies history evidence only; final Gate4 and DEC1 remain uncalled and reserved for Research Lead.
