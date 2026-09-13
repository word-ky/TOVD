# T013-G4A1 — PREOUTCOME_HISTORY_CLEAN

Audit boundary: task-start HEAD **cca9af23452870d1a12ba1ab6a78ebe683e49cd1**, including Lead assignment9b59ab9/cca9af2. Scientific freeze **6fec32243985ccc808123d851abf5f3dea10af99**; dispatch **88668f76b22777459b5792dd28f88075f208c678**. This snapshot covers59 post-freeze commits and97 unique changed paths, considering all parents of merges. The audit's own later delivery commits are outside this fixed boundary.

**Final Gate4 remains PENDING_COMPLETION_AND_RESEARCH_LEAD_REVIEW.** This is a pre-outcome history finding, not scientific acceptance. The supported absence statement is: **no committed evidence of duplicate primary dispatch/restart/retune, partial-primary scientific use, or YOLO scientific execution through the task-start HEAD.** Git and self-reported logs do not prove off-repository behavior. FIN1 and full-cache replay have not been run on the active primary by this task.

## Protected scientific artifact set

The17 paths below were derived from the freeze's10 `code_sha256` entries plus its PLAN/vocabulary/selection/data/image-manifest/environment references and the freeze JSON itself. The hash-source field and Git blob IDs are recorded per path in `gate4_preoutcome_history_receipt.json`. Each frozen and task-start blob is byte-identical, matches the freeze hash, and has an empty endpoint diff. Full-history merge-aware protected-path traversal finds no intermediate edit, including no change subsequently reverted.

| Protected path | Frozen SHA256 (equals task-start SHA256) |
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

Checkpoint, native model state, and COCO annotations are external assets, not Git paths. Their exact hash values remain frozen in the protected JSON: checkpoint3b3ca256...bc799, state de1683cc...39e1, annotations e8c7f790...10b6f (full values in receipt). The protected data receipt also binds both download archives and5000 JPEG hashes. This audit checks those committed bindings, not remote asset bytes; it does not reopen annotations, images, checkpoints or cached predictions. No additional Git path is directly hash-referenced by the freeze beyond the17 above. Immutable smoke/run receipts provide prerequisite evidence, not new protected-science definitions.

## Chronology, prerequisites and preserved negatives

The helper verifies the actual ancestor chain, not just date sorting:

`c07ce16 -> f63f571 -> 6548870 -> 02ba123 -> 259217c -> eed8d1a -> d5dc807 -> 35fbfb7 -> 6fec322 -> 88668f7 -> cca9af2`.

- c07ce16 establishes the original real-detector premise and Gates1–4. f63f571 (2026-09-12 20:03:24+08) records failed raw-query native/HF parity;6548870 (20:26:15) records detection-level PARITY-B failure. The original raw parity JSON, PARITY_B_RESULTS.md and parity_b.json remain byte-identical through task-start HEAD; their origin/head hashes are in the receipt. The prior negative run directories, raw-artifact paths and Lead rejection remain reachable. Nothing was rewritten to hide the failure.
- 02ba123 (20:38:21) rejects HF-1024 and explicitly authorizes a native256/30-distractor capacity reset before primary science;259217c (20:40:02) records the review. Original and reset mailboxes both retain Gate1>=2/4 with A_hard>=1.0 and lowerCI>0; Gate2 mean A_hard>=.75, mean hard-minus-random>=.50 and>=2 positive contrasts; explanatory Gate3 cannot rescue1/2; Gate4 forbids primary outcome/label tuning. PLAN retains those rules. This was a disclosed pre-outcome detector-capacity reset, not a claim that the old HF and native vocabularies are identical.
- eed8d1a freezes native vocabulary;d5dc807 implements the cached analysis;35fbfb7 records native smoke/provenance;6fec322 commits the complete final prerequisite bundle at **21:02:52+08**. Its JSON records both smoke run IDs,17/17 local and remote tests,5000-image manifest/data CRC receipts, exact1000 selection, environment and all scientific hashes, with primary_started=false. `git ls-tree -r 6fec322` confirms native30_smoke.json, completed pipeline run_receipt/cache_manifest and smoke analysis artifacts already exist in that tree; only their paths were inventoried here. Accepted Lead pre-primary review1833bf3/2e70b24 independently records these prerequisites as complete.
- The frozen release name is20260912-210306... and primary run ID is20260912-210355..., consistent with logged21:03:55+08 launch, after the freeze. Dispatch receipt88668f7 is committed21:05:49+08 and descends from6fec322. Git establishes the freeze-before-dispatch DAG; the operational start time is recorded provenance, not an independently attested wall clock.

## Exact dispatch binding and control history

The four committed text artifacts under `research_log/remote_runs/20260912-210355-tovd-native30-primary/` are read from88668f7 and compared against task-start HEAD: run.sh,meta.json,artifacts/resolved_release.txt,artifacts/freeze_sha256.txt. All four are unchanged. Their SHA256 values and exact command are retained in the receipt.

meta.json binds exactly the expected run/release/tmux. Its command occurs verbatim in run.sh, explicitly changes to `/home/wenchang/asdasdsad/wjq/TOVD/releases/20260912-210306-tovd-native30-primary-freeze`, records the release and freeze/PLAN hashes, sets OMP/MKL4, and runs one `scripts.t013_native_run --freeze-commit 6fec32243985ccc808123d851abf5f3dea10af99`, followed by one frozen `scripts.t013_analysis` only after inference succeeds. The wrapper's initial `cd .../current` is superseded by this explicit immutable-release cd before inference. The recorded release/hash files match this binding.

Across the59 post-freeze commits, only this run's five provenance/log-mirror paths were added, once at88668f7, and no later commit edits a run mirror. Inventorying all retained meta.json files finds one non-smoke native runner command and one earlier `--smoke-only` engineering command. There is no committed second primary launch. Accepted OPS1 receipt67baf38 reports one live writer PID721181 bound to this release/command; later health entries retain the same PID and run. No committed restart/resume/retune event is found.

Context matters for text searches: the COCO download resume205852 and earlier smoke/symlink/SSH retries predate primary dispatch and are documented prerequisite repairs; FIN1's system-Python failure and identical smoke retry use the completed45-cell engineering cache; REPRO1's mutation touches only scratch smoke outputs; future restart wording is a prohibition/return-to-Lead instruction. None is committed evidence of restarting the primary. The REPRO1 premature old-smoke-equality commentary was corrected and preserved in the report; it concerns a skipped historical smoke comparison, not primary outcome access.

## Post-freeze path classification and blindness review

| Category | Unique paths | Reviewed scope |
| --- | --- | --- |
| coordination/reporting | 4 | Three coordination mail/review files and t013/IMPLEMENTATION_NEXT.md recovery handoff |
| primary provenance/log mirror | 8 | REMOTE.md,project_state.md,session_log.md; five exact primary dispatch mirror paths |
| pre-outcome verifier/test | 25 | OPS1,STAT1,FIN1,REPRO1,DEC1 docs/helpers/tests/receipts and smoke replay logs/environment |
| YOLO contingency preparation | 60 | T013_YOLOWORLD_CONTINGENCY.md and59 t013_yoloworld source/config/metadata/tokenizer/protocol/fixture paths |

The receipt provides the **exact97-path category list**, all59 commit/parent/changed-path records, and122 contextual event-search hits from added reporting text. Zero unclassified paths; zero protected-science edits; zero post-freeze scripts/ or tests/ edits. Scientific-looking upstream YOLO source snapshots are explicitly classified as inactive contingency sources, not Grounding implementation changes. t013/IMPLEMENTATION_NEXT.md is a recovery/reporting document and is not hash-referenced by the scientific freeze.

Outcome-blindness evidence covers every delivered stage: dispatch88668f7 and Lead acceptance2e70b24/1833bf3; P0 976f36d/a0a74c1; P1 6694fcc/26d3e7e; P2 41ca40c/f919e2f; OPS1 67baf38/f6ce00f; STAT1 0cab4ca/b5a65cf; FIN1 8efe485/2432409; REPRO1 5fe57f7/7fa947b; DEC1 51881e3/d0dcd89 and health-only logs throughb8a5d5a. These distinguish operational opaque hashes, synthetic fixtures, and completed engineering smoke from active-primary science. Seventeen exact evidence anchors with commit/path/line/text/SHA are recorded; the latest health anchor reports377/1000 and no scientific access.

No committed primary result/prediction file is added post-freeze. No report claims a primary AP/AP50/interaction/bootstrap/diagnostic outcome. The document/receipt outcome statements are evidence-history findings; the helper's reference existence checks and search hits are not an automatic natural-language proof of outcome blindness. Final Lead review must still assess the full history and completed-run evidence.

YOLO P0/P1/P2 receipts and accepted reviews establish source/protocol/model-free work only: no installation, checkpoint payload download/load or image inference reported; no new YOLO run metadata or scientific benchmark output committed. Quoted upstream configs/demo/test scripts and published numbers in source/model-card snapshots are documentation, not local execution/results. P1's native postprocessing and P2's blank convention modify only the proposed YOLO lane; all Grounding scientific paths remain unchanged. DEC1 prohibits a future YOLO result from mutating Grounding's state; separately authorized replication may test architecture specificity only.

## Commands, observed helper error and limits

Command: `D:/anaconda3/python.exe research_log/t013/gate4_preoutcome_history_audit.py` (defaults to the fixed task-start SHA). Standard-library Python3.12.7 plus local Git only. The helper uses git show/rev-parse/merge-base/rev-list/diff/log/ls-tree; it never imports scientific packages, runs a detector, opens NPZs or contacts the active cache. Exact command and final health are also in the receipt. This delivery attests only the fixed snapshot; any future audit needs a new bounded history review, not a silent moving-HEAD rerun of the current semantic finding.

Initial invocation returned PREOUTCOME_HISTORY_BLOCKER solely because the audit helper counted both invocations of `scripts.t013_native_run` as primary. The retained initial receipt shows the supposed extra command is **20260912-205428-tovd-native30-pipeline-smoke**, explicitly carrying `--smoke-only` before `&&`. Its metadata already exists before freeze. The smallest audit-only correction classifies that flag on the inference command, retaining both inventory entries; the second invocation returns PREOUTCOME_HISTORY_CLEAN with all13 checks true. Initial output is preserved in `gate4_preoutcome_history_initial_receipt.json`. No protected path/hash/order/actual primary-dispatch discrepancy was found, and no scientific/history/run repair was performed.

No additional test framework, operational audit rerun, or scientific diagnostic was introduced. Real pinned-history checks and exact metadata inspection validate this audit's requested behavior. The end-of-package primary health check is metadata only and is appended to the receipt/handoff. Stop G4A1 after delivery; continue the unchanged run and15-minute monitoring. Final Gate4, primary interpretation, full-cache verification/replay, YOLO runtime and T014 remain subject to the existing completion/Lead conditions.
