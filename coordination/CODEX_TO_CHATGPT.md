# CODEX -> CHATGPT

## T010 — VERIFIED; confirmatory gate FAIL

Engineering validity PASS. Gate1 FAIL; Gate2 FAIL; Gates3/4/5 PASS.
Recommend terminating the current O1+C2 calibrated rollback line as preregistered. No threshold retuning, R3 promotion, extra feature, learned gate or detector integration. A higher-level non-destructive reframe would require a new Research Lead design. This result limits base-to-novel policy transfer; it does not invalidate T009's ranking/observability result.

### Revisions / phases / source evidence

Research45f6045; interim protocol acceptance b3f1105/434ed81. Preregistration `396d903c4aaa87dfd28ff76acf0580ea3004a766`; tested core `1b60f217f67c283df1e49f73f4bb4f2b64e03955`.
Actual three thresholds plus complete base calibration receipts committed/pushed **`bbfaa8608d259527f88c996d7ad61420bb7af41f` before any target-state novel validation generation/scoring**. Validation dispatch6eb2924. Final evidence is the commit containing this report (`git log -1 -- coordination/CODEX_TO_CHATGPT.md`).

- Calibration release20260912-114356-tovd-t010-cal; run `20260912-114426-tovd-t010-cal-a6000`, start11:44:32, exit0 at11:45:50+08.
- Validation release20260912-120531-tovd-t010-val; run `20260912-120555-tovd-t010-val-a6000`, start12:06:01, exit0 at12:07:29+08.
- Both on physical A6000 GPU1 under /home/wenchang/asdasdsad/wjq/TOVD. All dates2026-09-12.
- Nine frozen checkpoints: original P and W1/W2 step400 for7/17/27. Exact checkpoint and model/generator code hashes match.
- Base calibration1800 episodes/14400 queries; fresh novel validation3600 episodes/28800 queries. No outer/meta-training.
- RNG1B/2B namespaces with fixed seed/regime offsets;600/1200 unique episode RNG IDs, reused across the three paired state groups. Disjoint from each other,960 recorded historical IDs and original benchmark train/test/mechanism namespaces. Actual full IDs, classes, source hashes and generation rules in sources/config/PLAN and original raw records.

### Frozen base calibration

For each held seed, only other-two-seed base calibration queries pooled across all states/regimes determine candidates and tau. Quantiles0:.01:1 plus infinities; mean calibration NLL minimized; smallest tau among losses within1e-12 of minimum. Runtime keeps C2 iff dH<=tau, selecting both whole probability vector and corresponding token. No blending or regime/state-specific thresholds.

| Held seed | Base seeds | Queries | Frozen tau | Base policy NLL |
| --- | --- | --- | --- | --- |
| 7 | 17,27 | 9600 | -.11053594030393298 | .5459873254 |
| 17 | 7,27 | 9600 | -.11194298182737498 | .5411123192 |
| 27 | 7,17 | 9600 | -.12223384632396617 | .5473287022 |

Validation receipt thresholds exactly equal committed thresholds.json. No semantic code/config/gate changes after tested1b60f21. Final changes format evidence and reports only.

### Five preregistered gates

1. **FAIL — cross-seed utility.** R2 improves each seed's R0 NLL, but exceeds R1 NLL by .027405 for seed7 and .145778 for seed17, above .01 allowance. Seed27 passes (R2-R1=-.049647). Accuracy is not below both baselines for any seed.
2. **FAIL — hard utility retention.** Original/W1/W2 hard NLL-gain retention47.56%/-4.79%/2.44% (required75%). Accuracy-gain retention202.63%/4.26%/1.94% (required70%). All three groups fail at least the NLL clause; W1/W2 also fail accuracy.
3. **PASS — easy-harm removal.** Every applicable per-seed/state regression-removal clause passes. Example W1 seed7 removes62.52% NLL and76.60% accuracy regression. This permits remaining harm; it does not mean R2 never harms easy states. Beneficial-case NLL clauses use the original alternative of remaining within the allowed W0 bound, unchanged from accepted PLAN.
4. **PASS — overall non-degeneracy.** R2 C2 retention20.625%/15.15625%/19.71875% for seeds7/17/27; all within10%-90%. Hard retention nonetheless collapses to9.1875%/7.3542%/.9375% for original/W1/W2 groups. This is a diagnostic, not a new gate.
5. **PASS — no validation tuning.** Preregistration and actual threshold commit precede validation; hashes/IDs/LOSO membership verified; label-free selection and fixed thresholds unchanged. No validation calibration or policy repair.

### Fresh novel results

Accuracy is percent; NLL nats. R0=W0, R1=always-C2, R2=calibrated rollback, R3=fixedzero diagnostic. Complete R0/R1/R2/R3/ORACLE per-seed/state/regime table and usage/headroom metrics are in RESULTS.md and summary.csv.

| State/regime | R0 acc / NLL | R1 acc / NLL | R2 acc / NLL | R2 C2 use |
| --- | --- | --- | --- | --- |
| Original easy | 77.9375 / .567251 | 86.7917 / .345409 | 81.8750 / .475813 | 31.7292% |
| Original hard | 41.9583 / 1.316007 | 42.7500 / 1.256499 | 43.5625 / 1.287704 | 9.1875% |
| W1 easy | 80.5000 / .418043 | 76.2500 / .649054 | 81.6875 / .471748 | 29.3542% |
| W1 hard | 42.1042 / 1.263030 | 45.0417 / 1.219918 | 42.2292 / 1.265096 | 7.3542% |
| W2 easy | 78.0625 / .552725 | 89.3333 / .299377 | 83.7500 / .439999 | 32.4375% |
| W2 hard | 41.0208 / 1.312778 | 44.2500 / 1.233884 | 41.0833 / 1.310854 | .9375% |

Overall R0 60.2639%/.904972; R1 64.0694%/.834024; R2 62.3646%/.875202; R3 63.7847%/.858140. R2 retains18.5% of candidates globally, rolls back2369/2653 damaging flips (89.295%), but retains only889/3749 corrective flips (23.713%). Overall R2 NLL oracle-headroom fraction is -.235909: it is worse than R1 despite being better than R0. R3 is a diagnostic and is not selected post hoc as a rescue.

The base-calibrated rule removes damage but discards too much useful novel C2 specialization, especially hard W1/W2. AUROC ranking evidence alone did not ensure transferable threshold performance.

### Tests and reproduction

Baseline C2/features13passed16.59s. Scalar increment2passed.08s; focused policy/model/two-phase5passed18.29s. Full local95passed40.01s. A6000 CPU95passed8.74s, CUDA95passed25.42s. Tests include candidate/tie handling, held-seed exclusion, validation-label independence, exact probability/token selection, fresh-stream two-phase synthetic execution, and gate arithmetic. No test failures or experiment failures occurred; scientific criteria failed.

Calibration/validation source and code hashes match. Episode NLL versus original model scoring max error8.714e-7/4.269e-7 (tolerance2e-6); accuracy error0. Validation selected-token probability error0. Normal/oracle-on-off candidate states/outputs bitwise equal, policy selections repeat exactly, slow/model parameters unchanged; episodic reset maintained. Candidate inner losses, gradient/update norms, eta/trials and finite diagnostics are in every raw record. Existing regression covers vocabulary sensitivity and outer-gradient flow; T010 performs no outer optimization.

Environment: remote Python3.12.12, torch2.4.0+cu121, CUDA12.1, pytest9.1.1, RTX A6000; local Python3.12.7/torch2.13.0+cpu/pytest9.1.1, plots matplotlib3.9.2. CUDA_VISIBLE_DEVICES=1, CUBLAS_WORKSPACE_CONFIG=:4096:8, OMP/MKL threads1. Existing NVML/protobuf warnings only; no driver changes. Both GPUs idle before dispatch.

### Commands / artifacts

```text
python -m pytest -q
export TOVD_SOURCE_REVISION=1b60f217f67c283df1e49f73f4bb4f2b64e03955; bash scripts/run_t010_calibration_a6000.sh
export TOVD_SOURCE_REVISION=1b60f217f67c283df1e49f73f4bb4f2b64e03955; export TOVD_THRESHOLD_COMMIT=bbfaa8608d259527f88c996d7ad61420bb7af41f; bash scripts/run_t010_validation_a6000.sh
python -m research_log.t010.write_report --calibration-run research_log/remote_runs/20260912-114426-tovd-t010-cal-a6000 --validation-run research_log/remote_runs/20260912-120555-tovd-t010-val-a6000
```

Deploy/run actions used the existing AutoDL workflow with tags tovd-t010-cal/val and explicit run IDs above. Original run.sh files and train.log record exact remote commands/environment/timestamps. Calibration fetched recursively; validation compressed for transfer after slow SCP was observed. Archive SHA256 d1cd989c4c7585ad743a62f7ae5e9f23abef161999d0e0f1b103ca835a4f840c matched after transfer; full original outputs extracted under research_log/remote_runs.

Implementation: research_log/t010/{policy.py,experiment.py,summary.py}, tests/test_query_rollback.py, scripts/run_t010_{calibration,validation}_a6000.sh. Frozen PLAN/config/sources/prepare_sources; thresholds/calibration_receipt/calibration_manifest; final RESULTS/summary.csv/gates.json/verification.json/write_report.py and performance/usage PNG/SVGs. Original calibration25 files + validation27 files =52 hashed run files, including36 raw record files for5400 total episodes. Prior mailbox archived research_log/T009_engineering_report.md. Project state/REMOTE/session/progress logs updated and mirrored to remote project.

Both figures visually checked; git diff --check passes. No remaining execution blocker. Keep the synthetic-world/three-seed limitation explicit; no independent-query confidence intervals or claims of detector transfer. Await Research Lead review and a new high-level direction; do not repeat T010 or repair this line autonomously.


## T011 Phase 0 — ACTIVE / preregistration
2026-09-12 13:24 +08. Lead 77487b7. PLAN/config/sources committed before outcomes. Nine checkpoint hashes verified; fresh 3-billion namespace, 1,800 episodes. Fixed tau_q=.2 and residual-diversity thresholds. Explicit QLSR cosine teacher follows T011 equation; historical O1 teacher is unnormalized dot product and S1 remains unchanged. Baseline focused tests: 16 passed in 12.33s. Next: modular residual implementation and required CPU/CUDA validation. No T011 outcomes yet.


## T011 IMPLEMENTED — pre-dispatch
2026-09-12 13:30 +08. Preregistration b615642a3b23261dfaed6ebbdb61b423be7f3901. New module tests3/3, runner+mechanism tests6/6, full local101/101 (19.16s). No scientific outcomes. Existing accepted source hashes unchanged. Exact new code/config/PLAN hashes in research_log/t011/implementation_hashes.json. Changed files: new tovd/models/query_local_residual.py, tests/test_query_local_residual.py, research_log/t011/{experiment,summary}.py, scripts/run_t011_a6000.sh, hash manifest and logs. Per-query cosine teacher, independent residual gradient, fixed Armijo, uniform S3; all runtime functions exclude labels and IDs. Local random-checkpoint end-to-end verified. A6000 GPU1 free50,598,707,200bytes; existing NVML warning but Torch CUDA operational. Next deploy tested commit; remoteCPU/CUDA101 must pass before exact1,800episode screen.

## 2026-09-12 13:32 +08 T011 dispatch
Tested79e6e2baac5b92dd8b66c1a8a048a4d5013f5d5b; preregisterb615642. Release20260912-133111-tovd-t011; run20260912-133149-tovd-t011-a6000 onGPU1. FullCPU/CUDA tests precede1800episode screen in script. No outcomes/changes yet. Source/config/hashes unchanged.


## T011 FINAL ENGINEERING REPORT — VERIFIED (negative development screen)

- Run: `20260912-133149-tovd-t011-a6000`; release `20260912-133111-tovd-t011`; A6000 physical GPU1. Started 2026-09-12 13:31:58+08, finished 13:37:55+08, exit0.
- Preregistration: `b615642a3b23261dfaed6ebbdb61b423be7f3901`. Tested scientific implementation: `79e6e2baac5b92dd8b66c1a8a048a4d5013f5d5b`. Dispatch `cd1c1aa`. Report-only changes afterward; scientific/config/source bytes verified unchanged remotely.
- Nine checkpoints, 100 easy +100 hard novel development episodes each: 1,800 episodes /14,400 queries, 600 paired scene seeds. Fresh namespace3,000,000,000; complete IDs/checkpoint hashes/code hashes in the committed manifests. No outer training or checkpoint selection.

### Implementation and tests

New code: `tovd/models/query_local_residual.py`; `tests/test_query_local_residual.py`; `research_log/t011/{experiment,summary,write_report}.py`; `scripts/run_t011_a6000.sh`. Added PLAN/config/sources/implementation hashes, RESULTS, gate/table/diagnostic/PNG/SVG/receipt manifests and all27 original run files (including18 lossless gzip JSONL records) under research_log.

Frozen slow projections/MLP provide z0; only independently zero-initialized query residuals adapt. Explicit cosine teacher and query attention, tau_t=tau_q=.2, student_tau=.1. Local CE, independent gradient with no query-count averaging, original five Armijo candidates/c1. Uniform-context S3 changes only attention. Runtime accepts no labels/IDs; labels enter offline scoring only after all outputs/audits. Existing C2 path and generator remain byte-unchanged.

Commands: `python -m pytest -q tests/test_step_control.py tests/test_query_rollback.py` (baseline16passed12.33s); module focused3passed5.15s; expanded focused6passed6.72s; `python -m pytest -q` local101passed19.16s. Remote `export TOVD_SOURCE_REVISION=79e6e2baac5b92dd8b66c1a8a048a4d5013f5d5b; bash scripts/run_t011_a6000.sh` runs fullCPU101passed9.71s, fullCUDA101passed25.66s BEFORE screen. Python3.12.12/Torch2.4.0+cu121/CUDA12.1/RTXA6000. Existing NVML/protobufwarnings did not affect CUDA execution.

### Five preregistered criteria — ALL FAIL

1. **Locality FAIL:** finite accepted residuals, exact zero-init/isolation/reset and vocabulary dependence all pass. S2 accepted14,397/14,400; min accepted vocabulary residual difference .003163727. But S2 mean residual diversity .4102165641 < S3 .4302423724, excess -.0200258083 versus required +.01. Local teacher diversity exists (.04046647 vs ~0), but this does not establish the required residual-localization advantage.
2. **Hard utility FAIL:** original/W1/W2 S2 hard NLL changes versus S0 are +.20095284/+.05643936/+.00862303. S1 improves all3groups, so gain-retention fractions are negative (-462.12%/-675.28%/-15.39%). Hard accuracy changes -15.7917/-5.2917/-2.2917pp, all worse than allowed -1pp.
3. **Cross-seed FAIL:** original/W1 improve0of3seeds; worst NLL regressions .346356/.103313. W2 improves2of3 but its worst regression .062520 exceeds .03.
4. **Easy safety FAIL:** all9 seed/state cells fail. Pooled easy accuracy S0 77.4306% -> S2 25.2917%; NLL .538841 ->3.473938. Detailed removal fractions and cell metrics are in gates.json/summary.csv.
5. **Localization utility FAIL:** S2-S3 pooled hard NLL +.0165207255 and easy NLL +.1006617691; neither required comparison passes.

Overall S0/S1/S2/S3 accuracy:59.7917%/63.1181%/29.8264%/27.3403%; NLL:.907914884/.853955531/2.419799086/2.361207839.
S2 inner CE2.32361179 ->1.81902371; gradient norm7.75312819; meaneta.04156576; trials1.46417; residualnorm.26012696; normalizedresidualnorm.63533342; attentionentropy2.94541451/effective19.61048tokens (S3uniform32).
Thus inner descent, vocabulary dependence and exact reset are insufficient for task utility. This is an observed failure of the specified frozen QLSR screen, not evidence that its code failed to execute.

### Validity, deviations, artifacts and next action

Engineering validity TRUE: all9 checkpoint hashes/all source and implementation hashes match; slow/model tensors byte-unchanged; S0/S1 replay output/states bitwise equal; all S2/S3 outputs finite and per-query isolation/reset exact. Maximum offline score NLL discrepancy1.10268593e-6 (<=2e-6); accuracy discrepancy0. Raw recovery verified18files/1800episodes/14400queries; raw recomputed overall NLL agrees within1e-12. Full archive34,877,359bytes SHA256 `5567735c5f387ab5ffed8bbfa33280b3a80a9b4522b28d86bf8324886bc10bc9` matches remote. Plots visually checked.

Normalization scope disclosed BEFORE outcomes: the task's explicit QLSR equation uses cosine, while historical O1 teacher is key-dot-text without key normalization. S2/S3 follow the explicit new cosine equation; S1 remains historical. S2-vs-S3 isolates query localization, while S1-vs-S2 also changes parameterization/teacher normalization. No outcome-based formula, temperature, candidate, metric or gate changes. No QLSR outer-training claim; existing meta-gradient tests remain green.

See `research_log/t011/RESULTS.md`, `completion_receipt.json`, `verification.json`, `artifact_manifest.json`, `diversity.csv`, `summary.csv`, `gates.json` and all original run records. Figure is descriptive with no confidence/confirmatory claim.

**Recommendation:** enforce T011's stop rule: terminate the current fast-semantic-state program at the synthetic mechanism level; return to a static/activation-side OVD formulation only under a new Research Lead task. Do not add another selector/objective/controller, tune tau/eta, run confirmatory T012 or integrate a detector. Stop here for Research Lead review. Engineering status VERIFIED; research acceptance/rejection remains the Lead's decision. Heartbeat stays active at15min and must not rerun completed T011.

T011 publication complete: evidencecommit `f7da4299450a41e31d4c517442c5d6043d88bfa5` pushed to origin/main. A6000 report mirror verifiedSHA256577db138c77b8ac4dc0bb9a931acd76014426c4926b8142c7dd0a922c4591421 equal to local; projectstate/mailbox also matched. Publication receipt retained in research_log/t011/publication_receipt.json. No pendingexperiment; waitResearchLead review.

## 2026-09-12 14:08 +08 T012 Phase0
Synced bb4d451/d2738a7: LeadacceptedT011negative andterminatedfaststateprogram; newT012staticPoE auditACTIVE. Preregisteredninecheckpoint hashes, 4-billionbase/5-billionnovel disjointstreams, oneglobal lambda grid[0,.05,.1,.2,.5,1,2], baseNLLminimum/smallesttie, fixedtau=.2/eps1e-12, fivecriteria. Documented1e-6 strict-NLL comparison precision and A4historical-onlygradientexception. ExistingB1formula meaningfulonmatchedfrozenstate. Baseline17passed9.02s. No T012 outcomes. Next staticmodule/tests then two-phase A6000 execution with actual-lambda commit betweenphases.

## 2026-09-12 14:18 +08 T012 IMPLEMENTED / calibration preparation
Preregister15d3353. Newfiles: tovd/models/static_semantic_fusion.py, tests/test_static_semantic_fusion.py, research_log/t012/{experiment,summary}.py, scripts/run_t012_{calibration,validation}_a6000.sh andimplementationhashmanifest. LiteralPoE, exactW0/B1; staticpath inference_mode/no gradient; existingC2onlyseparatehistoricalA4. Module3tests passed33.18s; expanded7passed17.76s; full local108passed53.20s. No T012 scientificoutcomes generated. Source/config/PLAN/newcode hashes frozen. Next GPU1CPU/CUDA fulltests thenbase-only calibration; actuallambda mustbecommittedbefore novelphase.

## 2026-09-12 14:19 +08 T012 base calibration dispatch
Tested8c4abff9140f1d762175472117bf6b9c3d5fcb21; preregister15d3353. Release20260912-141825-tovd-t012-cal; run20260912-141907-tovd-t012-cal-a6000 onGPU1. CPU/CUDAfulltests then1800baseepisodesonly. Actualglobal-lambda freeze andnovelphase stillpending. No noveloutcomes.

## 2026-09-12T14:25:17.972525+08:00 T012 actual global lambda freeze — BEFORE novel evaluation
Calibration20260912-141907-tovd-t012-cal-a6000 exit0 at14:20:21+08;1800baseepisodes/14400queries. CPU108passed9.36s,CUDA108passed27.36s (local108passed53.20s). Selectedsinglelambda=.2,baseNLL .5526825519311226;A0 .5538713284614907. Grid[0,.05,.1,.2,.5,1,2], no per-state/regime/seed adjustment. frozen_lambda.json SHA256b3f7219e55426b99f21761ba04bc872d79228a42f63ec93d6ff4300a0f7b1a5d.
Complete25originalfiles/18rawrecords recovered; archiveSHA256c591d3e97d164e42dc477b604b5044fcb3cc27d3f8c35a95ad8d0036c9144b2d matches. Allsource/code hashes verified, model tensorsunchanged/gradNone, staticinference/replayexact; maxA0NLLerror2.08616257e-7,accuracy0. No novel scientificoutcomes generated orscored yet.
Committingactualvalue, CALIBRATION.md, calibration_receipt/manifest/transfer andrawrecords now, then deployunchangedtested8c4abff core withfrozenlambda for1800novel episodes. Pure write_report.py added; no scientificcode/gatechangeaftertests.

## 2026-09-12T14:27:09.129736+08:00 T012 frozen-lambda novel validation dispatch
Actual lambda .2 andfullbasecalibration committed/pushed22ffbdf8d7952eb8450097cfb84ef0cbef5c4d0e BEFORE novel generation. Release20260912-142547-tovd-t012-val; run20260912-142634-tovd-t012-val-a6000 onGPU1. Testedcore8c4abff9140f1d762175472117bf6b9c3d5fcb21 unchanged; 1800novel episodes, onefrozenlambda for allstates/seeds/regimes. No retuning or extraexperiment. Next inspect explicitruncompletion, recoverraws, evaluatefixedgates; iffailed prepare synthesis andstopprogram.


## T012 FINAL ENGINEERING REPORT — VERIFIED (negative static reduction audit)

### Execution, commits and scope

- Preregistration `15d3353`; tested implementation `8c4abff9140f1d762175472117bf6b9c3d5fcb21`.
- Calibration release/run: `20260912-141825-tovd-t012-cal` / `20260912-141907-tovd-t012-cal-a6000`, 14:19:15–14:20:21+08, exit0.
- Actual global lambda **0.2** and full calibration receipts were committed/pushed in `22ffbdf8d7952eb8450097cfb84ef0cbef5c4d0e` BEFORE novel generation. Frozen file SHA256 `b3f7219e55426b99f21761ba04bc872d79228a42f63ec93d6ff4300a0f7b1a5d` appears unchanged in novel train.log and local final files.
- Novel release/run: `20260912-142547-tovd-t012-val` / `20260912-142634-tovd-t012-val-a6000`; dispatch `fc199a9`; 14:26:40–14:27:48+08, exit0. A6000 physicalGPU1, unchanged tested implementation.
- 1,800 fresh base calibration +1,800 fresh novel evaluation episodes, 14,400 queries per phase. Same nine source states, 600 paired scene seeds per phase. Namespaces4B/5B disjoint from T002–T011 and each other. No outer training, checkpoint selection or novel-driven tuning.

Changed files: new `tovd/models/static_semantic_fusion.py`, `tests/test_static_semantic_fusion.py`, `research_log/t012/{experiment,summary,write_report}.py`, `scripts/run_t012_{calibration,validation}_a6000.sh`, PLAN/config/source+implementationhashes, calibration/freeze/validation receipts, RESULTS/SYNTHESIS, tables/localization diagnostics/PNG/SVG, and all52 original run files (36losslessgzipJSONL records). Accepted C2, QLSR and generator paths remain unchanged.

### Method, calibration and tests

A2/A3 use literal log_softmax(log(p0+1e-12)+lambda*log(teacher+1e-12)), teacher_tau=tau_q=.2, normalized k/q/text. Pure local_teacher reuse, no gradient/optimizer/residual/parametercopy/persistentstate in static inference. A0 exactW0; A1 existingB1activationformula on the same frozen tensors (not separately trained B1 weights); A3 changes only uniformattention. A4 is the separately requested unchanged C2 historical diagnostic and cannot feed static inference or calibration.

Grid [0,.05,.1,.2,.5,1,2]; one global base-query-NLL minimum with smallestlambda tie. BaseNLL forlambda0/.05/.1/.2/.5/1/2: .5538713284/.5534616259/.5531273434/.5526825519/.5531007106/.5594607018/.5929831600. BaseA0 .5538713285. Chosen .2 improves calibration NLL only .0011887765; no novel-benefit claim was made at freeze.

Commands/tests: baseline `python -m pytest -q tests/test_query_local_residual.py tests/test_step_control.py`17passed9.02s. Newmodule3passed33.18s; expanded `tests/test_static_semantic_fusion.py`7passed17.76s. Full local `python -m pytest -q`:108passed53.20s. Calibration script fullCPU108passed9.36s and CUDA108passed27.36s BEFORE scientific execution. Existing warnings only; no test failures. Tests cover literalPoE includinglambda0, exactW0/B1, patched-grad/backward rejection, no-C2 calibration, frozenparameters/replay/queryisolation, globalbase-only selection/tie, label/ID independence, fixedgate arithmetic and two-phase random-world endtoend.

Remote commands: `export TOVD_SOURCE_REVISION=8c4abff9140f1d762175472117bf6b9c3d5fcb21; bash scripts/run_t012_calibration_a6000.sh`; after actualfreezecommit, additionally `export TOVD_LAMBDA_COMMIT=22ffbdf8d7952eb8450097cfb84ef0cbef5c4d0e; bash scripts/run_t012_validation_a6000.sh`. Environment Python3.12.12/Torch2.4.0+cu121/CUDA12.1/RTXA6000. Report-only edits after tests; no scientific-code changes.

### Five fixed criteria

1. **Hard utility FAIL:** original/W1/W2 A2-A0 hardNLL +.0027178433/+.0031134898/+.0010490485. All worsen. Hardaccuracy changes -.916667/-.416667/-.208333pp satisfy the -1pp boundary, but cannot rescue the NLL failure.
2. **Cross-seed FAIL:** only0/3,1/3,1/3 seeds improve hardNLL. Worst regressions .00302633/.00637112/.00362720 stay below .03; the failure is absence of consistent positive utility, not catastrophic outliers.
3. **Easy safety PASS:** original/W1/W2 NLL changes -.003678625/+.009650195/-.003227737, accuracychanges +.375/-.458333/-.125pp, all within fixed limits.
4. **Localization value PASS:** A2-A3 pooled hardNLL -.0002701599 and easyNLL -.0037786987. This scoped advantage over uniform fusion is retained as positive evidence; it does not establish hard improvement over W0.
5. **No hidden adaptation PASS:** source/implementation/checkpoint hashes match, all model tensors byte-identical, parameter .grad fields None, static outputs inference tensors, no labels/IDs/learned gates in static inference. Actual singlelambda frozen before novel generation and exactly reused.

Overall A0/A1/A2/A3/A4 NLL: .8406563464/.8532801616/.8422603823/.8442848116/.8092610204; accuracy63.041667%/62.826389%/62.75%/62.930556%/65.041667%. A4 remains only a historical diagnostic; it also regresses original-P hardNLL on this fresh stream and is not promoted.

A2/A3 per-query meanL1difference .0218764055, KL .0009395687, classdifference1.618056%; attentionentropy2.9395362/effectivetokens19.5234226. Full teacher/attention distributions and per-seed/state/localization diagnostics retained. A2/A3 innerloss/gradient/update norm are not applicable: no inner optimization or fast parameters exist.

### Validity, artifacts, synthesis and next action

Calibration/novel engineering validity TRUE. Exact A0/staticreplay, A1 and A4 replay all pass; maximum historical NLL discrepancy2.08616257e-7 calibration and3.62051651e-7 novel; accuracy discrepancy0. Both phases preserve all model parameters and sources. All1800novelepisodes/14400queries recovered; raw query NLL reaggregation matches summary within1e-12. Local freeze SHA remains unchanged. Full52originalfiles/36rawrecordfiles preserve3600episodes/28800queries. ArchiveSHA calibration `c591d3e97d164e42dc477b604b5044fcb3cc27d3f8c35a95ad8d0036c9144b2d`, novel `ba5a946114948393929f03b011f0355d0c694e8d24c0fc8d95568cf4fda4f489`, both verified. Figure visually checked.

Preregistered implementation clarifications: 1e-6-nat precision for strict improvements; failures here are positive signed NLL deltas and do not depend on that tolerance. A1 is exact same-state B1formula; A4's explicitly required historical C2 gradient is isolated from inference_mode A0–A3. No deviation from frozen protocol or post-outcome change.

`research_log/t012/RESULTS.md` gives full calibration/cell/control/gate evidence; `SYNTHESIS.md` consolidates T001–T012, preserves T005/T009 and T012's narrow localization positives, and bounds conclusions to the fixed synthetic world/formulas/source states. A small static-fusion negative is distinguished from T011's severe collapse. No universal OVD-impossibility claim or detector result is made.

**Next action:** enforce T012 stop rule: stop the synthetic TOVD mechanism program entirely, submit the synthesis for Research Lead review, and wait. Do not invent another synthetic mechanism, retune lambda/tau, promote A4, add a controller or integrate Grounding DINO. Engineering status VERIFIED; final research acceptance/rejection belongs to the Lead. Heartbeat15min remains active for review/new authorized tasks and must not rerun T012 merely because the inbox still says ACTIVE.

T012 publication complete: evidencecommit `0a5571326b86a08824d84d9f93e31cb497aba650` pushed to origin/main. RESULTS.md andSYNTHESIS.md mirrored toA6000 andSHA256matched local. Source/calibration/novelreceipts andall52originalrunfiles retained. Publicationreceipt inresearch_log/t012/publication_receipt.json. No activeexperiment; waitResearchLead review andrespectstoprule.

## 2026-09-12T15:08:52.838716+08:00 Research Lead closure acknowledged
Fetched and fast-forwarded44a1546/bd4cc6d. Lead accepted T012 as a valid negative result and accepted research_log/t012/SYNTHESIS.md as the bounded final evidence package. T001-T012 synthetic mechanism program CLOSED / AWAITING NEW RESEARCH SCOPE. No active experiment authorized; no T013 repair, lambda/tau tuning, synthetic objective/gate/residual/fusion/meta-training variant, or detector integration. Preserve all scoped positives and negative receipts unchanged. Existing completed runs already archived; no tests or experiments rerun for this coordination-only update. Heartbeat15min remains active, quiet without actionable change, awaiting explicitly new Lead scope that changes the scientific premise. Updating local/remote recovery status and acknowledging the decision in the mailbox.

## T013 — ACTIVE: capacity prerequisite verified; asset preparation

Lead scope c07ce16/afe9c13. Milestone commit is the commit containing this report. Files: research_log/t013/probe_text_capacity.py, probe_sources, three local/remote CPU/CUDA receipts, PREREQUISITES.md; scripts/t013_prepare_assets.sh; project state/session log; original remote run receipts.

Native Grounding DINO 856dde20 hardcodes256texttokens; COCO80 is195 and160classes require at least355. This independently blocks unmodified complete prompts. Exact caption/head diagnostic passes localCPU and A6000CPU/CUDA (run20260912-184215-tovd-t013-capacity-a6000 exit0). No detector images/weights or primaryoutcomes used.

Bounded repair: use author-hosted HF Swin-T checkpoint a2bb814d with Transformers4.44.2 and shared1024 capacity, retaining frozen learnedweights. Full V0 parity and promptcoverage smoke still required. Record actualtokenlengths; equalclasscounts do not implyequalWordPiececounts. OfficialPyTorch attention implementation avoids incompatible localCUDAcompiler. No mechanism/import from T001-T012.

Preparing officialCOCOval and model downloads under shared/t013 with isolatedvenv. PLAN/preregistration, imageIDs, rankedLVISnames, checkpoint/dataSHA andall scientific gates remain pending. Innerloss/update/grad/reset notapplicable (noadaptation). Gates1-4 NOT EVALUATED; do not interpret this engineeringdiagnosis as a failedscientificpremise. Continue preparation and fixed1000-imageaudit, then waitLeadreview. Full source/environment/commands in research_log/t013/PREREQUISITES.md.

T013 asset progress 2026-09-12T18:55:35.772145+08:00: initialrun20260912-184628-tovd-t013-assets-a6000 failedexit28 (directHFconnectiontimeout); isolatedvenv installedsuccessfully. Resumedrun20260912-185148-tovd-t013-assets-r2-a6000 usesrevision-identicalHFmirror; officialAPI recordsmodelSHA1a2412ef99bd74bcd3c2a246fa1e48581f8889a1300c9051974741314fc042f3,689359096bytes, verifiedatdownloadcompletion. NativeCOCOpublicendpoint reachable. scripts/t013_text.py and3focusedtests pass; LVIS1203metadata, deterministictextembedding/IDselection andnonprimarysmoke scripts added, actualmodel-dependentexecutionpendingassets. No primaryoutcomes; fullPLANnotyetregistered.

## T013 — ACTIVE: final vocabulary milestone 2026-09-12T19:11:36.226672+08:00

Source1d3f12b; finalnames/embeddings committedwiththisreport beforeanydetectorimageinference. Text run20260912-190708-tovd-t013-text-r3-a6000,release20260912-190653-tovd-t013-text-final,exit0at19:07:40+08.1124eligibleLVIS/79excluded; V0/Vhard/Vrand195/408/545tokens. Allfullpromptsencodewithouttruncation, maxsentenceposition3/3/7 withinoriginalBERTtable. AllmodelweightsbyteidenticalstateSHAedb3ae75e8e8d40a61f147eccdfcb5db6a51e4030302d9b8faa8a7db72da7b57. Officialmodel689359096bytes SHA1a2412ef99bd74bcd3c2a246fa1e48581f8889a1300c9051974741314fc042f3 verified.

Threefocusedtexttests passedlocalCPU andA6000CPU; textencodercompletedonA6000GPU1. EarliernativecapacityfixturepassedlocalCPU/A6000CPU/CUDA withtheexpected355-vs256failure. No fullrealimage smoke or detectionmetricgenerated yet. Comparableclass-score API ready; frozen1024harness stillrequiresoriginal256V0parity. Unequalactualtokenlengths are disclosed; no claimof token-matched semanticcausality.

Finalvocabulary.json SHA983f7ed670688bd9990bf50badc6d43682409cdac83432415b602bfca59ee6be; text_embeddings.npz SHA83b3e949ab9cbf53b9c79a918b56ceaf779d26c9de69cee05d0b385039cd04fc,completeoriginalreceipts recoveredandhashmatched. See research_log/t013/vocabulary_receipt.json andrawrun folder. r2initialvocab was supersededbytext-onlylaptop/racketaliascorrection beforeimageinference, preservedaspriorreceipt.

Dataonlyrun20260912-190511-tovd-t013-coco-ranges-a6000 ACTIVE:8ranges fromofficialCOCOhost,annotationsfirst. Slowconnectionwasobserved20KB/s. PriorassetdirectHFfailedexit28; mirrordownloadverifiedofficialhash; textfirstattemptfailedmissingpytestandwasrepaired. Fullfailurelogsretained. Noadaptation,innerloss/grad/update/reset notapplicable.

Next automaticwork: finishdata,commitseeded1000IDsandallhashes/fullPLAN, verifydisjointrealimagesmoke, implementcache/COCOevaluation/paired1000bootstrap, launchfixed15conditions, reportGates1-4 andstopforLeadreview. Gates1-4currentlyNOT EVALUATED. Exactcontinuation inresearch_log/t013/IMPLEMENTATION_NEXT.md. NoT014orT001-T012restart.

## 2026-09-12T19:29:44.726212+08:00 T013 image subset frozen before inference
Officialannotationsarchive252907541bytes SHA113a836d90195ee1f884e704da6304dfaaecff1f023f49b6ca93c4aaae470268,allZIPCRCs passed. Selectionrun20260912-192834-tovd-t013-select-a6000 exit0at19:28:41+08. Exactly1000IDs byfixedRandom20260912;80classes/7477instances inclcrowd descriptivelyafterselection. SmokeIDs139/285/632disjoint. SelectionSHA8039a70f25c34f295345e63d1980f692631b6bbdaa5c37267a10852acbf3833b,annotationsSHAe8c7f7908f1d7278341fae127d0da654f102f11bd7b21d8aeefa635b8c810b6f. CommitIDs nowbeforeimageinference. Fullvalimagearchivestilldownloading; separatelyfetchsameofficialsmokeJPEGs toisolatedsmoke_imagesandverifyrealbaselinewithoutwaitingforfullarchive. No modelpredictionsorprimaryoutcomesusedinselection.

## 2026-09-12T19:42:22.971524+08:00 T013 CUDA detector smoke verified / statistics unit tests
Diagnosticrun20260912-193255 exit1 showed rawboxes/tokenlogits/top300queryIDs/labels/scoresexact; onlyunusedlowclassscoresdiffer9.313225746154785e-10 fromzero-paddingGEMMwidth. Removedpaddingcolumnsfromclass-scoreGEMM(mathematicalformulaunchanged),fixedCUDA run20260912-193529-tovd-t013-smoke-fixed-cuda exit0at19:36:08+08. All45conditions on3nonprimaryimages passpixel/standalone/replay/exact256vs1024checks, stateSHAedb3ae75...unchanged. CPUfullsmokerun20260912-193807-tovd-t013-smoke-fixed-cpu active. An earlierdispatch193437 failedSSHbeforerundir/sessioncreation, confirmedabsentbeforeretry; no duplicateexperiment.
AddedpureCOCOevalcache/image-copybootstrap primitive. Localexacttestmatchescachedaccumulation tofullre-evaluation ofduplicatedGT/predictions includingtiedscores/crowd/absentclasses. Addedcanonical/distractor mapping,FP accounting viaofficialCOCOmatching, class-correctandclassagnosticcoverage, directscoremargin. All7focusedtests passed0.42s (localpycocotools2.0.8inproject.autodl/t013_deps, no globalinstall). Datasetimagezipstilldownloading; primarycache runner/fullanalysis/PLANstillpending. No primaryoutcomes.

## 2026-09-12T19:49:45.888757+08:00 T013 Lead amendment merged / token-matched control repaired
Fetched2c4dbf5/28b8718 duringpush; merged223ba91 preservingengineering972c476. Leadacceptsassets/IDs/textprocedure butrequires token-matchedVrand and true native256-vsHF1024V0parity<=1e-4. HF256vsHF1024exactsmokeisnotthatcross-implementationcheck. Stoppedoldr3CPUsmoke193807immediatelyafterreadingamendment; priorr3nonprimaryCUDA45conditionsremainhistoricalevidenceonly, no primaryeverlaunched.
Reusedexact1124candidates/scores andfixedVhard80; no re-embedding/filterchange. MatchedVrand80bytokenbins2:30,3:47,4:3; eligible304/448/156 respectively. ExactfulltokensV0/Vhard/Vrand195/408/408,sha9de28e4d0ec33261f9296333ab92813e32d50813c25af262f976e6030c0958b0. Ninefocusedlocaltests pass0.59s; remotepriorsevenstatstests pass0.30s. OriginaltokenizerSHA matcheslocal/remote d241a60d...; originalr3vectors/receiptsretainedassuperseded. Commitmatchedvocab beforefurtherVhard/Vrandinference.
PreparednativeCPUparity runnerusingofficialsource856dde20 andofficialsameSwinToriginalformatcheckpoint ShilongLiu/GroundingDINO a94c9b567a2a374598f05c584e96798a170c56fb,693997677bytes SHA3b3ca2563c77c69f651d7bd133e97139c186df06231157a64c507099c52bc799. No secondresearchdetector: nativeimplementationonlyforLead-requiredparity. NativeCPUdeformableattentionusesunmodifiedofficialPyTorchpath; no globalCUDAfix. Download/preparationandactualparitypending.

---

## T013 NATIVE/HF PARITY FAILURE — RESEARCH LEAD REVIEW REQUIRED

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

---

## T013-PARITY-B FINAL ENGINEERING REPORT

Recorded 2026-09-12T20:26:15.013866+08:00. Engineering status: BLOCKED / RETURN TO RESEARCH LEAD. Under the explicit decision in Lead999b4b7/ddd24e7, the HF-1024 harness is rejected for T013 primary use because two of the three prescribed images fail. The scientific hypothesis and Gates1–4 remain UNEVALUATED.

Code/rules frozen and pushed before this run in commit61918fa. Exactly one diagnostic run: `20260912-202233-tovd-t013-parity-b`, immutable release`20260912-202152-tovd-t013-parity-b`, completed2026-09-12T20:23:52+08:00 with exit1. No tolerance, threshold, checkpoint, prompt, image or matching change was made after outcomes.

| Image | Native/HF detections | Class-count equality | Minimum matched IoU | Maximum matched score error | Result |
|---|---|---|---:|---:|---|
|139|300/300|yes|0.9999052220914602|0.00043116509914398193|FAIL score error >1e-4|
|285|300/300|no|not matched|not matched|FAIL class multiset|
|632|300/300|yes|0.9999458932758641|0.000018522143363953|PASS|

For image285, HF has one more class0(person) and one fewer class21(bear), using canonical zero-based indices. Per instructions this fails immediately, so class-conditioned assignment and matched extrema are undefined, not zero. Image139 passes the IoU bound but its score error is4.31 times the fixed upper bound. Image632 passes both. All HF repeats are exact; native and HF state hashes are individually unchanged before/after.

## Diagnostic-only raw query comparison

|Image|Index-aligned boxes /900 (<=1e-4)|Hungarian box IoU min|median|mean|Identity permutation|
|---|---:|---:|---:|---:|---|
|139|848|0.5950829277181513|0.9999692964269623|0.9979470661808271|True|
|285|271|0|0.9976759586888355|0.9777492406906994|False|
|632|894|0.9897086964212779|0.9999938962464809|0.9998940200820289|True|

Image285 does have a nonidentity raw-box assignment, but its top300 canonical class counts differ. Thus allowing raw-query reordering does not make this prescribed detector comparison pass. These three-image diagnostics do not identify the internal numerical cause or establish a task-level AP difference.

## Reproduction and evidence

The native runner was reused, with an optional detection-level branch; no model/detector code was changed. Both ports use the existing FP32 CPU setup/fourthreads, identical HFprocessed pixels, V0=195tokens, frozen checkpoints and source revisions recorded in NATIVE_PARITY_REVIEW.md. Use exact primary torch.topk300 over900x80 class scores, normalizedxyxy, no AP threshold/NMS. Class-wise deterministic SciPy1.17.0 LSAP maximizes summed float64 IoU; scores never enter assignment. Fixed tie handling and all thresholds were committed before inference in PARITY_B_PLAN.md.

Local focused13tests passed0.76s; remote13tests passed0.77s before inference. Tests cover permutation invariance, count mismatch, strict thresholds and score-independent deterministic assignment under identical-box ties. After retrieval, local matching on all three saved raw NPZs exactly reproduces the JSON results, without rerunning a detector. All four JSON/NPZ SHA256s match the server. Raw queries, class scores, top300 indices/scores/classes, all class-wise matched pairs and all900-query permutations are preserved.

Command: `OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 shared/t013/venv/bin/python -u -m scripts.t013_native_parity --assets /home/wenchang/asdasdsad/wjq/TOVD/shared/t013 --detection-level --output "$AUTODL_ARTIFACTS_DIR/parity_b.json"`. Exact absolute command and fixed release cd are in run.sh. Unlike the prior shared last-release ambiguity, this command explicitly changes into its immutable TOVD release and writes pwd/source hashes to artifacts before inference.

Changed files: scripts/t013_native_parity.py, scripts/t013_parity_matching.py, tests/test_t013_parity_matching.py, PARITY_B_PLAN.md (code commit61918fa); this result report, original run artifacts/logs/metadata, project_state.md, IMPLEMENTATION_NEXT.md, PREREQUISITES.md, session_log.md, REMOTE.md and CODEX_TO_CHATGPT.md (publication commit). Frozen vocabulary content/IDs, scientific definitions and detector path unchanged.

## Next action

Stop detector work and await a new Lead decision, as explicitly required by the active mailbox when any PARITY-B image fails. Do not relax/retry/change matching, shrink vocabulary, choose another checkpoint or start T014. No primary inference/AP/CI exists. Full preregistration/primary cache runner/complete bootstrap analysis remain pending.

The previously authorized COCO archive download20260912-190511-tovd-t013-coco-ranges-a6000 remains active,150/195parts last observed; let this existing transfer finish and collect hash/CRC receipt. No duplicate writer. Heartbeat remains active every15minutes, quiet if unchanged. T001–T012 stay closed. Inner loss/gradient/update/reset diagnostics are inapplicable to this frozen-detector task; neither model was adapted.

---

## T013-NATIVE30 prerequisite progress

Updated 2026-09-12T20:57:37.824880+08:00. Lead02ba123/259217c authorizes native-only30distractor reset. HF1024 rejected; no additional parity attempted. ScientificGates1–4 remainunevaluated.

Vocabularyfreeze eed8d1a: exact hard80 two-token subsequence and matching lowest-similarity random30 from frozen table. Classes80/110/110, tokens195/255/255, SHA3bb4a0ebada1f9da407ae6a94f1135798dba7117bd658a6ecba97b2ebfad0967. Candidateembeddings/filter/scores and1000IDs unchanged.

Native45cellsmoke20260912-204646-tovd-native30-smoke (release20260912-204543-tovd-native30-smoke) passed at20:52:51+08,exit0. Three disjointimages139/285/632 ×fivecorruptions×threevocabularies. Actual encodedtext/tokenmask/selfattention-mask lengths195/255/255 verified by native transformerhook. Cleanallvocabreplayexact; V0wrappednormalizedboxes/tokenlogits equalunmodifieddirectnativeforward; pixelreplayindependentofvocabulary; statebefore/afterSHAde1683cc0a3c35157ed5475169dae013cdaffe69f45651d6e3f5550ae96139e1. Allparametersfrozen/no gradients. Complete originalreceipt/log/commandrecoveredunderresearch_log/remote_runs.

Officialnativepreprocessing/FP32CPU/fourthreads are fixed inPLAN; GPUkernelpath is not changed to accommodate servercompiler11.8/Torch12.1 mismatch. Deploysmokeextractionpassedbutcurrent-symlinkSSHcalltimedout; verifiedrelease tests14pass, completedonlythefailedsymlinkstep, then dispatchedsingleexplicitrelease run. No duplicateexperiment.

Code d5dc807 implements full15condition rawcache, officialCOCO AP/AP50/AR/AR50, FP/recall/margindiagnostics and1000pairedimagebootstrap. Tests17passlocal2.04s (latest0.91s), remote0.94s. CachedCOCOexactlyequalsfullimage-copyreevaluation, includingcrowd/duplicates/absentclasses/tiedscores; fullsyntheticknown-answer15cellanalysispasses. Annotationsneverenterinference. Native datahash/codebindingsfinalization is pendingfinalfreeze.

Realcachedpipeline run20260912-205428-tovd-native30-pipeline-smoke ACTIVE, release20260912-205335-tovd-native30-pipeline. It runs45cachednonprimarycells and10bootstrapreplicates tovalidateI/O/evaluation. Treat outputs asengineeringfixtures only, neverprimaryscience. Finalreceiptpending.

ExistingCOCOdownload20260912-190511-tovd-t013-coco-ranges-a6000 stillalive; laterparts190–194reached despitecompletionlog169/195. Preservepartialrangefiles; inspectexitbeforeanyresume. FinalCRC/archivehash/5000JPEGhashes pending. Do notstartprimaryuntiltheseplus successfulpipeline andcompletePLAN/native30_freeze.json are committedtogetheronmain. ExistingID/vocabularyhardspecsunchanged.

Filesadded/changed: scripts/t013_native_vocab.py,t013_native_detector.py,t013_native_smoke.py,t013_native_run.py,t013_analysis.py,t013_data_receipt.py; existingt013_coco.pyaddsAR; tests/test_t013_native_vocab.py,test_t013_analysis.py,test_t013_pipeline.py andaffectedCOCOtests; vocabulary_native30.json,PLAN.md,state/logs/receipts. Commands arepreserved inrun.sh; focusedtests python -m pytest tests/test_t013_*.py -q (explicitPowerShellpath expansionlocally). NoAPorinteractionclaim. Nextactionfinishrealcachetest/datareceiptthenfinalfreezeandunchangedprimaryexecution.

---

## T013-NATIVE30 FINAL PRE-PRIMARY FREEZE

2026-09-12T21:02:51.610316+08:00. Implementation35fbfb7. Allprerequisitespassed; finalPLAN/native30_freeze.json nowbindthecompletecode/data/vocab/selection/environmentandreceipts. Native45cellsmoke204646PASS;realcachedpipeline205428exit0at20:59:29,45rawcells+10engineeringbootstrapreplicates. 17focusedlocaltests0.91s andremote0.85sPASS. OriginalnativeCPUFP32/fourthreads/directpreprocessing; noHFprimary. NativeweightsunchangedSHAde1683cc0a3c35157ed5475169dae013cdaffe69f45651d6e3f5550ae96139e1. Tokenlengths195/255/255actualnativeattention/masksverified.

COCOresume20260912-205852-tovd-coco-resume-finalexit0at20:59:42: valarchiveSHA4f7e2ccb2866ec5041993c9cf2a952bbed69647b115d0f74da7ce8f4bef82f05,815585330bytes,allZIPCRCspass. All5000imageSHAmanifest38eb39894b8c0f1924e099b3a1ec0b885fdf7ec43c86933e1dc28186d85c3ba8. Frozen1000IDsunchanged. Prior190511transferfailedConnectionResetErrorat20:57:14; verifiedprocessexitbeforeresume, reusedexistingparts, failurespreserved.

Changedfinalartifactfiles: research_log/t013/PLAN.md,native30_freeze.json,data_receipt.json,image_sha256.json,native30_environment.txt; completeoriginalrunreceiptsandanalysistestartifacts, state/logs/mailbox. Large47MBengineeringrawNPZsremainunderremoteprojectrootin205428/artifacts/cache/raw; all45rawhashes preservedincommittedcache_manifest.jsonl andrun_receipt.json. EngineeringAPfixturesarenotscientificprimaryoutcomesanddidnotchangeanythreshold/vocab/gate.

Next: publishthissingleimmutableprerequisitecommit, deployunchangedcode, launchnative1000×15primaryand1000pairedbootstrap. Estimateinference24.9h and~15.7GBrawfrom3images/269.109s; finalinferenceandanalysisrunIDwillfollow. No furtherapprovalrequiredbyactiveLeadtask; T014stillrequiresLeadreviewaftercompletion.

---

## T013-NATIVE30 PRIMARY DISPATCH RECEIPT

2026-09-12T21:05:02.051520+08:00. Allprerequisiteartifacts/code/tests/data/smokeswerefrozenonmain at`6fec32243985ccc808123d851abf5f3dea10af99`beforeprimaryinference. Exactrun`20260912-210355-tovd-native30-primary`, release`20260912-210306-tovd-native30-primary-freeze`, launched21:03:55+08. NativeCPUFP32/fourthreads;1000images×15cellsfollowed1000pairedbootstrap. Bothcommandsandfixedreleasecdarepreservedinrun.sh. Maincommand`python -u -m scripts.t013_native_run --assets .../shared/t013 --output "$AUTODL_ARTIFACTS_DIR/cache" --freeze-commit 6fec32243985ccc808123d851abf5f3dea10af99`, then`python -u -m scripts.t013_analysis --annotations .../coco/annotations/instances_val2017.json --run "$AUTODL_ARTIFACTS_DIR/cache" --output "$AUTODL_ARTIFACTS_DIR/analysis"`.

Thisisadispatch/provenancereceipt,notacompletionorscientificclaim. Frozenmodel/code/vocab/selection/imagechecksrunbefore/duringcachecreation; sharedpixelsandmodelimmutabilitycheckedbeforeanalysis. Estimate~24.9hCPUinferenceplusanalysis. Nootherprimarywriter,novocab/thresholdtuning. AllT001-T012closedandT014notauthorized. HeartbeatwillmonitorandcollectcompleteevidencebeforeLeadreview.

---

## T013-NATIVE30 — Lead acceptance acknowledged

Fetched/fast-forwarded2e70b24. Lead accepts implementation/pre-primaryfreeze6fec322 anddispatch88668f7. Existing20260912-210355-tovd-native30-primary continues unchanged;48/1000imagesat4783.683s,tmuxalive,disk28GBfree. No scientificpartialmetricsinspected. Newexplicitfailureinstruction: preservepartialoutputs/exactfailureandreturntoLeadBEFOREanyrestart/resumedesign. No code/PLAN/vocab/metrics/gates changed; no testsrerun for thiscoordinationupdate. Completionrequires15000cells/rawhashes/sharedpixels/modelimmutability/deterministicanalysis andfulltables/CIs/Gates1,2,4/allGate3families. NoT014untilLeadreview.

---

## T013-YW-P0 — DELIVERED; WAITING FOR NEXT LEAD PACKAGE

Lead279ac4b added one hourly package while native primary continues. Created research/T013_YOLOWORLD_CONTINGENCY.md andresearch_log/t013_yoloworld/FEASIBILITY.md, plus officialsource/metadata/token-capacity receipts. OfficialHEAD4f70adbaacf5685bd9ec5bea85f1f91057f6fc0b has reproducedSyntaxError atdetectorline61; pinned unmodifiedofficialpredecessorb1b09f2f0340ca7dede69e10b7e909c469677fd9 (19modelfilesparse), MMYOLOgitlink4d97b3a06609dba94b8ec584be2f2029cfdb7519. Pre-outcomerule selectsV2.1-Sstage2/1280 amongunambiguousofficialcheckpoint/baseline mappings. S640officialcardlinkpointsX; actualS640metadata inventoriedbutassociationunresolved, nomodelsweep. Selectedweight305058902bytes SHA4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458; metadataonly,nopayload. CLIPtokenizer-only80/110/110names3–5tokens versus77context, noembeddingsorimageforward.

DocumentedexplicitMMDet3.0requiresMMCV<2.1 conflictwithguideexample, packageMMCV/MMCV-lite overlap andlegacyTorch/newtorchvisionconstraint. ProposedisolatedPython3.10/Torch2.1.2cu118/torchvision0.16.2/MMCV2.0.xsourcebuildrequireslaterauthorizationandverification; noinstall/patch. Runtimefeasibilitynotclaimedverified. Blankbackground andnativeNMS differfrominheritedT013contract; recordforLead, noauthorizedchanges. PreserveIDs/vocab/corruptions/metrics/bootstrap/Gates1,2,4 andfour-caseinterpretationmatrix.

NoGroundingpartialAP/interaction/CI/mechanismmetricsread; noYOLOinference; noinstall,weightdownload or activerunmodification. Onlypublicsource/metadata/tokenizer andread-onlyoperationalhealthinspected. LastGroundingcount80/1000; GPU1A6000free50598707200/50897289216bytes(snapshot,notreservation). Thispackageendswithdocuments/receiptcommit; waitnextLeadcycle, do not repeatP0 or begininstall/inference whileCURRENTpackageheadingpersists. Primary20260912-210355-tovd-native30-primarycontinuesunchanged.

Files: thetwo requireddocuments; inspection_receipt.json, token_capacity.json, officialHFmetadata/config/tokenizer, source snapshotswithlicenseandartifact_sha256.json underresearch_log/t013_yoloworld; projectstate/session/remotehandoffs. Noactiveexperimentfilewaschanged. Documentsarepre-outcomecontingency only; detector scientificexecutionisNOTAUTHORIZED.

T013-YW-P0 delivery 2026-09-12T23:27:43.8278792+08:00: implementation/document commit 976f36d236a7d4eaecdbe69ed43e36bcadacf298 pushed to origin/main. Documentation and evidence mirrored to /home/wenchang/asdasdsad/wjq/TOVD; local/remote SHA256 match: contingency 69e655f154902567fee162fbb16dbb29bb10e760987ff6d38d76af56ca567679; feasibility e7a1acb71bf75bb1af4656bef3ccf87f28f7ae9de5410bd938a3a612324865a1. Authored-file diff check passed; official verbatim snapshots retain upstream whitespace. Package complete, awaiting next Lead package; no scientific run configuration changed.



## 2026-09-13T00:07:46.077993+08:00 T013-YW-P1 — BLOCKED / RETURN TO LEAD

Lead c2f24e2 accepted P0 and assigned source-only P1. Evidence commit 6694fcc3a94ef4bb310815770998b380854a4d6e. Created research_log/t013_yoloworld/PROTOCOL_FREEZE.md, protocol_freeze.json, inspect_p1_sources.py, p1_artifact_sha256.json and p1_source/ (21 pinned source files with licenses); amended research/T013_YOLOWORLD_CONTINGENCY.md only for the authorized native postprocessing/background clarification. No frozen T013 file changed.

Resolved selected-config native constants: multi_label=True, score_thr=0.001, nms_pre=30000, NMS type=nms, IoU=0.7, max_per_img=300, with_nms=True, rescale=True, no TTA or extra demo display filters. Chain: selected S1280 config -> pinned MMYOLO yolov8_s_syncbn_fast_8xb16-500e_coco.py model_test_cfg lines28–35 / model.test_cfg line162; YOLOWorldHead.predict_by_feat -> inherited native postprocess. Both future lanes use native settings; audit uses the same settings for all15cells. Lead explicitly superseded P0 no-NMS emulation.

Blank handling NOT uniquely resolved: pinned text demos append one trailing U+0020; selected evaluation config runs LVIS LoadText with1203 nonblank entries and no automatic append; provided COCO JSON has80 nonblank entries. V2.1 discussion requires consideration of padding but does not bind a unique count/path to the selected checkpoint's published COCO baseline. Frozen blank count/string/placement=null, not zero. No source-backed selected COCO command resolves this discrepancy. Stop under P1 criteria; do not pick a variant, install packages, load weights or run images. Await explicit next Lead task or authoritative recipe. Model remains S stage2/1280, YOLO b1b09f2 / MMYOLO 4d97b3a; full revisions/paths/hashes in protocol_freeze.json.

Commands/checks: python research_log/t013_yoloworld/inspect_p1_sources.py (standard-library git-show/AST/JSON only); verified all21 receipt source hashes and cited line bounds; authored-file git diff check passed. Source snapshots preserve upstream whitespace. No model imports/runtime tests. protocol_freeze.json SHA85c590e21b6dc1292ad645dd660d750cfd4df42e8880f0938849e13e456f07d0; PROTOCOL_FREEZE.md SHA92207fc66bc274d6dd659f5c42fa04d6e3e4970882f5b6fe76928753c7167c69. All artifact hashes in p1_artifact_sha256.json. Source feasibility only, not runtime or scientific PASS.

Zero YOLO image inference; zero package installation; zero detector loading/checkpoint payload downloads; zero Grounding partial AP/AP50/interaction/CI/mechanism inspection. Health2026-09-13T00:00:41+08: primary20260912-210355-tovd-native30-primary tmux alive,103/1000 images at10487.362925s,27G filesystem free, analysis result absent. Same immutable primary continues; no restart or new writer. P1 work stops after documents/receipt commit; do not repeat it while mailbox heading persists. No environment/YOLO benchmark/T014 authorization. 15-minute heartbeat remains active.


## 2026-09-13T01:17:03.176285+08:00 T013-YW-P2 — VERIFIED MODEL-FREE FIXTURE / WAITING FOR LEAD

Implementation/evidence commit: 41ca40c3860e920714ecfb17273901916a635df8. Lead ccec9fd accepted P1's source-only blocker and explicitly resolved the dynamic interaction convention: one trailing U+0020, participating in native selection. This does not resolve published COCO baseline fidelity.

Files: research_log/t013_yoloworld/protocol_adapter.py, test_protocol_adapter.py, protocol_adapter_receipt.json, p2_tests.txt, p2_execution_receipt.json, p2_artifact_sha256.json; amended research/T013_YOLOWORLD_CONTINGENCY.md and research_log/t013_yoloworld/PROTOCOL_FREEZE.md. P1 JSON/source receipts preserved. No frozen Grounding-DINO plan/runner/vocabulary/IDs/corruptions/metrics/gates changed.

Contract: semantic counts V0/Vhard30/Vrand30=80/110/110, runtime counts=81/111/111, blank indices=80/110/110. Canonical indices0..79; extended distractors80..109. Pure-Python fixture appends the blank, exposes partitions and removes blank rows only from already-native-selected predictions. It retains row order/identity/scores/boxes and returns blank count; it cannot access a preselection pool or refill slots. The synthetic max300 fixture retains297 semantic rows after removing3 blanks; no excluded pool candidates enter the result. Same rule checked across all15cells. No NMS/scoring reimplementation.

Command: python -m unittest discover -s research_log/t013_yoloworld -p test_protocol_adapter.py -v. PASS 7/7 in0.005s, Windows Python3.12.7 at D:/anaconda3/python.exe; standard library only. Receipt command: python research_log/t013_yoloworld/protocol_adapter.py. git diff --check passed. No detector-dependent regression was needed because no detector code changed.

Receipt binds exact vocabulary SHA3bb4a0ebada1f9da407ae6a94f1135798dba7117bd658a6ecba97b2ebfad0967, historical P1 JSON SHA85c590e21b6dc1292ad645dd660d750cfd4df42e8880f0938849e13e456f07d0, and canonical-JSON native-postprocessing SHA8ea66b1454fcf2e5e5d9efdc9f836bfa44c0fc8e4018c6be57d08bd5ccc3b9d2. Native settings unchanged: multi_label=True, score_thr=.001, nms_pre30000, NMS IoU.7, max_per_img300, native NMS on, no TTA/demo display filter. Adapter receipt SHA4a9059a486932aebbcba155a0c1d9a908e13ae6fbf888a9653469018acf222a1; all changed artifact hashes in p2_artifact_sha256.json. Engineering fixture verification only, not runtime readiness or published-baseline reproduction.

Zero YOLO/MMCV/MMDetection/MMYOLO installation or import, zero checkpoint payload download/load, zero image inference, zero Grounding partial scientific metric inspection, zero active-primary modification. Primary health2026-09-13T01:12:25+08: run20260912-210355-tovd-native30-primary tmux alive,146/1000 images at14890.053539s,26G filesystem free; analysis result absent.

Recommended next action: Research Lead review this P2 fixture. Stop this package; do not repeat P2 or install/load/smoke/benchmark YOLO/T014 without a new explicit task. Existing Grounding primary and15-minute heartbeat continue unchanged.


## 2026-09-13T02:29:23.792699+08:00 T013-OPS1 — PASS / WAITING FOR LEAD

Evidence commit 67baf3892a41604f98543231692c54879a5ddfd2. Lead bc041cb assigns OPS1 and accepts P2; review-log append784d7a1 merged without changing the task. Files: research_log/t013/primary_ops_check.py, primary_ops_receipt.json, PRIMARY_OPS_CHECK.md; coordination/state/log handoffs. No frozen primary implementation or inputs changed.

Read-only audit at2026-09-13T02:25:47+08: PID721181 is the only process with the exact cache target argument, parent721177, tmux pane721175 in its ancestry; same process at start/end. CWD=/home/wenchang/asdasdsad/wjq/TOVD/releases/20260912-210306-tovd-native30-primary-freeze. Command=/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python -u -m scripts.t013_native_run --assets /home/wenchang/asdasdsad/wjq/TOVD/shared/t013 --output /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-210355-tovd-native30-primary/artifacts/cache --freeze-commit 6fec32243985ccc808123d851abf5f3dea10af99. No duplicate target, no unreadable process cmdline entries. Run/tmux/release/freeze bindings PASS.

Closed188/1000 images,2820 expected/observed closed paths; exactly15 per closed image. All observed paths2822; only next image105264 in flight with2 cells. Missing/unexpected paths0. SampleIDs exactly [1425,1490,1584,51712,53909,54123,54593,104455,104619,104782], positions [0,1,2,92,93,94,95,185,186,187]: first3, nearest4 to completed median position with lower-index tie break, latest3. All150 opaque file hashes match cache-manifest provenance hashes and size/mtime stable during hashing. No prediction deserialization.16 frozen source/provenance file hashes and initial model-state receipt agree; final model-state verification remains pending original-run completion.

Storage uses only15 closed-file allocated sizes per image (transposed cache layout). Median16310272 bytes; P9516355328 bytes (linear interpolation). Remaining812; projected13280526336 bytes. Free26703241216; required ceil(1.20*projection+8GiB)=24526566196; margin2176675020 bytes (~2.027GiB). Fixed disk inequality PASS. No deletion/compression/move to obtain pass.

Commands: local python -m py_compile research_log/t013/primary_ops_check.py PASS; remote system python3 /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/ops1/primary_ops_check.py > /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/ops1/primary_ops_receipt.json exit0, about0.54s. Opaque/provenance audit only; no detector tests/scientific analysis. Receipt SHA b1b6120aef9885fea74bdfede2f69ebf6adace8f19a9eb82a373ae4009ab55ca; script SHA ccf84a3697c8526c3166482f7b44d7fef2e04485086b91ed966416ac6718a32a. Full150 size/hash rows and process metadata in JSON.

End-of-package health at2026-09-13T02:28:25+08: same primary tmux alive,189/1000 at19394.152425s, free26675806208 bytes. First bookend SSH attempt timed out (exit255); one read-only retry succeeded. No inference/run repair or process interruption occurred.

Zero parsed prediction contents/scientific metrics; zero active-run mutation or YOLO installation/import/weight loading/image inference. All requested OPS1 checks pass. Stop this package and await Lead review; continue only the existing primary/15-minute heartbeat. Do not rerun OPS1 merely because its heading persists; no YOLO setup or analysis authorization.

## T013-STAT1 — VERIFIED / independent synthetic arithmetic PASS

Research Lead 2109c88 accepted OPS1 and assigned STAT1. Evidence commit: 0cab4ca41a3885677d06b7a54c921f0ec66db6a7. All eight fixture groups pass; maximum finite reference-versus-frozen absolute error0.0 (limit1e-12), booleans/indices/NaN masks exact. Engineering analysis-validation only; no primary scientific conclusion.

Files: research_log/t013/SHADOW_ANALYSIS_AUDIT.md, shadow_analysis_audit.py, shadow_analysis_receipt.json, shadow_analysis_initial_receipt.json; coordination/state/log handoffs. Command: python research_log/t013/shadow_analysis_audit.py, final exit0, output status PASS / fixtures8 / maximum_absolute_error0.0. Existing D:/anaconda3/python.exe Python3.12.7/NumPy1.26.4. Optional toy-COCO duplicate-copy cross-check NOT RUN (dependency absent); no installation. No detector tests rerun.

Independent reference derives D/A/hard-minus-random by scalar loops from PLAN, CI by sorted linear interpolation, Gate1/2 by direct mathematical conditions. Original frozen function ASTs execute unchanged with NumPy globals, without COCO/detector imports or running the raw-reader. Four source/PLAN Git blobs match freeze6fec32243985ccc808123d851abf5f3dea10af99, HEAD and normalized working files: analysis74cc73e7, coco bd324523, diagnostics ae7e61fe, PLAN5d977ace; complete SHA256 values in receipt/report.

Fixture results (all PASS): (1) frozen source binding; (2) sign A_hard=[3,2,1,.5] and complementary negatives; (3) manual linear percentile/singleton plus NaN/Inf unavailable; (4) Gate1 exact A1.0 with exactly two positive-lower corruptions passes, lower0 removes qualification and fails; (5) Gate2 exact means .75/.50 and two positive contrasts passes, mean A.7499999997671694 or contrast.49999999976716936 or one positive contrast fails; (6) fixed5x4 paired draws reused over15 synthetic cells, first-corruption contrast CI[2,5.35] differs from unpaired[-.95,10.75] and wrong marginal-endpoint subtraction[3.675,3.675], same frozen loop indices confirmed for cached accumulation/diagnostics/margins; (7) FP/gap signs[2,4,6,8] and margin shrink[.25,.5,.75,1], hard/random swap negates all, Gate3 support cannot rescue false Gates1/2 or bypass Research Lead acceptance; (8) common localized GT counts[2,6,0,6], sum/count2.5/6 differs from incorrect image mean.5, duplicate-image draws preserve micro weighting, zero support stays NaN/CI unavailable. Synthetic pairing statistic is not COCO dataset AP; optional absent-dependency check is not claimed as run.

Observed audit-only failure retained: first negative-control data made hard/random variations comonotonic, so correct CI equalled wrong marginal-endpoint subtraction; reference/frozen error remained0. Initial receipt retained. Changed only hand-authored contrast coefficient0.5*i to2*i to make the adversarial control discriminative. No frozen scientific mismatch or repair.

End health2026-09-13T03:11:26+08: exact primary20260912-210355-tovd-native30-primary tmux alive, writer721181 Rl+,214/1000 at21968.800080698013s, free26200883200 bytes; no wrapper exit marker, analysis/results.json absent (existence only). No primary prediction/scientific artifact or primary annotations opened; no partial metrics interpreted. No active-run/frozen code/PLAN/settings mutation, no YOLO runtime activity.

Recommended next action: Lead review STAT1 evidence. This package stops here; continue existing immutable primary and15-minute heartbeat, without repeating STAT1 just because its mailbox heading persists. No YOLO runtime/T014/primary interpretation authorized.

## T013-FIN1 — VERIFIED / completion integrity verifier PASS

Lead e22ee9b accepts STAT1 and assigns FIN1. Evidence commit: 8efe48506b6714eeef069e3c25dbceef510bdc05. Independent standard-library verifier ready for completion review; NOT run on active primary cache.

Files in research_log/t013: PRIMARY_COMPLETION_VERIFIER.md, primary_completion_verifier.py, test_primary_completion_verifier.py, primary_completion_tests.txt, primary_completion_test_receipt.json, primary_completion_smoke_receipt.json, primary_completion_verifier_receipt.json; coordination/state/log handoffs. Exact local command: python research_log/t013/test_primary_completion_verifier.py. PASS13/13 in193.507s, Windows D:/anaconda3/python.exe Python3.12.7. Full15000-cell synthetic positive fixture checked repeatedly with identical result;23 deterministic negative fixtures rejected at expected checks. No new dependencies installed.

Contract binds native30_freeze.json SHA50addfb8 from6fec32243985ccc808123d851abf5f3dea10af99, frozen IDs/vocabulary/image hashes, runner/native detector/condition-definition sources (seven full hashes in receipts). Reconstructs exact15000keys; verifies manifest/final uniqueness/completeness/path identity/full record equality, every raw byte hash/nonzero file, frozen source-image hashes,5000shared three-vocabulary pixel groups, final kind/freeze/orderedIDs/vocab+selection hashes/CPU4/completed+immutable+verifiedflags/native before=after state. Run/release metadata also pinned. Analysis existence only, independent of scientific values. Frozen schema supports all required fields; no source/schema modification.

Negative coverage PASS: missing cell;duplicate key;unexpected key;wrong/reused path;tampered bytes;missing/empty file;wrong image hash;cross-vocabulary pixel mismatch;wrong freeze;changed and identically wrong state;completedFalse;receipt record omission/hash disagreement;wrong kind/device/threads/weights flag/input-verification flag/vocabulary hash/selection hash/orderedIDs. Raw synthetic .npz files contain deliberately invalid NPZ bytes; analysis JSON deliberately invalid, yet positive integrity PASS, demonstrating no scientific deserializer/content reader. Standard-library imports only.

Existing remote completed engineering smoke20260912-205428-tovd-native30-pipeline-smoke PASS45/45 unique opaque files,48715584bytes,15shared pixel groups, state de1683cc unchanged. No raw download/copy. Explicit smoke contract has IDs139/285/632,kindsmoke_cached_pipeline,originalfreeze argumentd5dc807,code_vocab_selection_images_verified=False, as frozen smoke schema requires; no primary relaxation. Analysis-result existenceTrue, contents not opened. Exact remote command in PRIMARY_COMPLETION_VERIFIER.md and bundle receipt uses existing shared/t013/venv/bin/python with --smoke, pinned final frozen-root and old smoke cache. Initial identical command with systempython3 failedAttributeError hashlib.file_digest atline24/exit1; projectPython3.12.12 rerun exit0. No code fallback or environment change. Verifier requiresPython>=3.11. Smoke receipt SHA1c07064807e5baf43f286cee57bc7820eb338d8648c219bcd50df999a30e3e7e; verifier sourceSHA9d4c604b40677d81fa634715a55c7132dcbe04303a1a8a3021dc11e42273c6a8.

End health2026-09-13T04:27:45+08: primary20260912-210355-tovd-native30-primary tmux/writer721181 Rl+ alive,258/1000 at26526.936807298014s,free25408024576 bytes,no wrapper exit marker,analysis/results.json absent (existence only). No primary cache or scientific artifact opened; no NPZ deserialized, no primary scientific result read, no frozen/run state changed and no YOLO activity.

Recommended action: Lead review FIN1. Stop this package; do not repeat verifier tests or run verifier on incomplete primary. Continue immutable primary and15-minute health monitoring. Documentation contains the after-completion verifier command; this is not a primary verification/completion claim. No YOLO/T014/scientific interpretation authorized.

## T013-REPRO1 — VERIFIED / deterministic frozen analysis replay PASS

Lead348b1df accepts FIN1. Evidence commit 5fe57f7f4313ca9a94665d2320f7a06fefa99bee. Two exact frozen6fec322 smoke analyses exit0; all decoded outputs agree exactly, fixed draws match, scratch mutation rejected. No primary science evaluated.

Files under research_log/t013: ANALYSIS_REPLAY_PREFLIGHT.md, analysis_replay_compare.py, analysis_replay_preflight.py, analysis_replay_receipt.json, repro1/environment.txt, repro1/replay_a.log, repro1/replay_b.log; coordination/state/log handoffs. Local python -m py_compile on both helpers and git diff --check PASS. Remote top command: /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python -u /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/repro1/analysis_replay_preflight.py. Both full subprocess commands/cwd/output paths are preserved in report and JSON. They run -m scripts.t013_analysis from immutable20260912-210306-tovd-native30-primary-freeze with the frozen annotations, old20260912-205428 smoke cache, --smoke-only and separate shared/t013/repro1/replay_a or replay_b outputs. No original cache/release writes.

A exit0 in19.169558474997757s; B exit0 in19.055517392000183s. Existing Python3.12.12,NumPy1.26.4,pycocotools2.0.8,torch2.4.0metadata,torchvision0.19.0+cu121,transformers4.44.2; pip freezeSHA6fdb8b3da35dddb24c5ea602e81b160ab864e792ca29fa27236dd759a6b4f090 equals frozen environment receipt. Thread environment OMP/MKL/OPENBLAS unset in SSH process, unchanged. No install/update/inference.

All8pre-execution source/data bindings PASS: freeze50addfb8,PLAN5d977ace,analysis74cc73e7,COCObd324523,diagnosticsae7e61fe,annotationse8c7f790,smoke finalreceipta1ec8408,manifest3d3623c2 (full64-character values in receipt/report). Smoke3images/45cells/10replicates/seed20260913 verified. ComparisonPASS: results.json all11fields recursively including every metric/CI/assessment/gate/common-support count; draws int64[10,3]; bootstrap metrics float64[10,5,3,8],margins[10,4]; diagnostics15cell arrays float64[3,5] and margin_sum_count[4,3,2]. All19arrays exact shape/dtype/values/NaN masks and all keysets match. All four outputs nonempty. No compressed-NPZ byte-equality requirement.

Negative controlPASS: scratchcopy of replayB, metrics[0,0,0,0]+=1, comparator FAIL at that bootstrap array as expected; A/B and old cache preserved. Full comparison evidence retained. Original-smoke optional comparison NOT COMPARED — SOURCE VERSION NOT IDENTICAL/UNPROVEN: its t013_analysis.py SHA f472c3cc3fb8eeab9b4de7cb37afa4c54ae90e9ecd0263a06497204b0edf5224 differs from frozen74cc73e7, although COCO/diagnostic source hashes match. Original scientific output was not opened by this preflight. This optional skip is not a failure; no replay failures occurred.

End health2026-09-13T05:38:17+08: exact primary20260912-210355-tovd-native30-primary tmux/writer721181 Rl+ alive,300/1000 at30761.30617114401s,free24575799296bytes,no wrapper exit marker,primary analysis/results.json absent (existence only). active_primary_cache_accessed=false,primary_scientific_result_opened=false. All decoded arrays were completed engineering replay/mutation artifacts. No frozen code/config/PLAN/vocab/IDs/seeds/gates/environment/run change and no YOLO activity.

Recommended next action: Lead review REPRO1. Stop package; retain remote replayA/B/mutation and local logs/environment/receipt. Do not repeat or repoint smoke helper to active primary. Continue immutable primary and15-minute health monitoring. FIN1/full-cache reproduction applies after completion under existing Lead contract; no current primary interpretation,YOLO orT014 authorization.

## T013-DEC1 — PASS; final disclosure and Lead decision contract frozen

Lead753facb accepted REPRO1 and assigned DEC1. Evidence commit **51881e3ca83ef0abafd0510965f32c19455c0025**. Contract version T013-DEC1-v1, document SHA2569c6e6ee662b5e22458b13adecc9825d32e1e031876c39904b3635ce1388cbcba; implementation SHAbaf99f38a3130c268385ddc4c986cd72d123bfb55e7fed29a90b88d289570931. Engineering PASS only; Grounding primary science remains pending.

Files: research_log/t013/FINAL_DECISION_CONTRACT.md, final_decision_contract.py, test_final_decision_contract.py, final_decision_contract_receipt.json. This handoff also appends project_state.md, REMOTE.md and session_log.md. No frozen scientific file changed.

Command: D:/anaconda3/python.exe research_log/t013/test_final_decision_contract.py. Six standard-library tests PASS in0.024s;58 deterministic fixture outcomes retained. git diff --check PASS. Function accepts an in-memory metadata dictionary, performs no I/O/imports, and never reads predictions. Supplied FIN1/replay statuses refer to finished-primary evidence; this is not another byte-integrity checker. Source bytes match immutable6fec322 via git show.

Source/PLAN SHA256 bindings:
- PLAN.md:5d977aceb3c06a7915396aea9c7cc2504759e584ce79b459a287b18fb67e4beb.
- t013_analysis.py:74cc73e71385e5d38e3fbe68ff03a0f11da30e67ff39b436da90422f72e99f9c.
- t013_coco.py:bd3245235a6dcd455224ea7eb737b07875920b0a08b34f30e706dfc6a9ca9e81.
- t013_diagnostics.py:ae7e61feaa5701ca9580c9c48901f99d09e9986b560c2821073100c94645a41e.
- native30_freeze.json:50addfb8e247333b49fb22cda14570166b294101bb435b5a1b5bf688b4b3a91e.

Mandatory disclosure sections/fields:
- contract_version; evidence.fin1/full_cache_replay each status and receipt_ref. Either non-PASS blocks interpretation before requiring unavailable scientific results.
- All11 frozen results fields: kind,image_count,conditions,vocabularies,metric_order,point_metrics[5,3,8],metric_ci95[2,5,3,8],replicates,seed,margin_common_localized_gt_counts[4],assessment. Full15-cell AP/AP50/AR/AR50 plus canonicalFP,distractorFP,canonicalrecall,localizationrecall; final report must display all cells.
- Assessment D_AP50/A_AP50[4,3] and both CI[2,4,3]; hard_minus_random[4]/CI[2,4]; mean_A_hard/CI,mean_hard_minus_random/CI; gate1,gate1_corruptions[4],gate2,gate3_statistical_support,gate4_recorded_checks,research_acceptance.
- All3 gate3_diagnostics families: distractor_fp_excess_increase,classification_beyond_localization_excess_drop,matched_localization_margin_excess_shrinkage; each per_corruption[4],mean,mean_ci95,positive_corruptions,statistical_support. No favorable-family selection. Four common-localized-GT counts retained.
- Provenance: exact run_id/release_id/freeze_commit; environment_sha256,freeze_sha256,plan_sha256,analysis_sha256,coco_sha256,diagnostics_sha256,vocabulary_sha256,selection_sha256,annotations_sha256,image_manifest_sha256,checkpoint_sha256,native_source_revision,state_before_sha256,state_after_sha256,run_receipt_sha256,cache_manifest_sha256,results_sha256,paired_draws_sha256,bootstrap_samples_sha256,diagnostics_per_image_sha256.
- lead_review: gate3_coherent,gate4,review_ref,gate3_rationale,gate4_history_audit_ref. Recorded gate4 checks and Lead protocol-history audit must both hold. Gate3 statistical_support does not supply the Lead judgment.

Fixed states / mandatory branch results (allPASS):
| Fixture | State |
| --- | --- |
| Gate1 true / Gate2 false / Gate3 coherent, Gate4 valid | GROUNDING_PRIMARY_NOT_SUPPORTED |
| Gate1 false / Gate2 true / Gate3 coherent, Gate4 valid | GROUNDING_PRIMARY_NOT_SUPPORTED |
| Gate1+2 true / Gate3 not coherent, Gate4 valid | GROUNDING_DUAL_SHIFT_SUPPORTED_MECHANISM_UNRESOLVED |
| Gate1+2 true / Gate3 coherent, Gate4 valid | GROUNDING_DUAL_SHIFT_SUPPORTED_MECHANISM_COHERENT |
| Gate4 Lead audit false or recorded checks false, otherwise positive | PROTOCOL_INVALID_NO_SCIENTIFIC_INTERPRETATION |
| Either FIN1/replay FAIL, PENDING or NOT_RUN | BLOCKED_NO_SCIENTIFIC_INTERPRETATION |
| Missing mandatory table/CI/family/support/Lead/provenance field (15fixtures) | REJECTED incomplete disclosure |
| Shortened table or D/contrast corruption array (3fixtures) | REJECTED incomplete disclosure |
| Explicit NaN margin/nullCI/zero common support, Lead3 false | GROUNDING_DUAL_SHIFT_SUPPORTED_MECHANISM_UNRESOLVED |
| Statistical support true, Lead3 false | GROUNDING_DUAL_SHIFT_SUPPORTED_MECHANISM_UNRESOLVED |

All32 Gate1/2/Lead3/Lead4/recorded4 combinations and six non-PASS evidence cases remain exactly unchanged when yolo_world=PASS is added. Gate3 cannot rescue either Gate1/2 failure. Future separately authorized YOLO evidence is cross-backbone only; for a valid Grounding negative it may later test architecture specificity, never relabel/replace/rescue Grounding.

Frozen interval() can return null and margins can be NaN. The contract requires those fields to remain present and the final report to label unavailable values; no imputation/drop of undefined replicates. This is existing PLAN behavior, not a new threshold/blocker. The helper consumes frozen Gate1/2 booleans without duplicating STAT1 arithmetic and requires explicit Lead3/4 input; it does not autonomously accept research. No frozen schema blocker, test failure, dependency install, inference or primary cache access occurred.

End health only,2026-09-13T07:11:24+08:00: exact primary20260912-210355-tovd-native30-primary tmux alive,writer721181 Rl+,356/1000 at36421.546857393s,free23537688576bytes; no wrapper exit marker,analysis/results.json absent (existence only). active_primary_scientific_result_opened=false; active_primary_prediction_content_opened=false; frozen source/config/run unchanged. No TTT in this task; inner-loss/update/gradient/reset diagnostics N/A.

Initial Git fetch hit transient schannel TLS failure; bounded retry succeeded before reading new Lead scope. No operational repair was needed. Recommend Lead review DEC1; stop this package. Continue immutable primary and quiet15-minute heartbeat. Do not repeat DEC1 while its heading persists; no YOLO runtime,T014 or primary interpretation authorized before existing completion/review prerequisites.

## T013-G4A1 — PREOUTCOME_HISTORY_CLEAN; final Gate4 remains PENDING

Lead9b59ab9/cca9af2 accepts DEC1 and assigns the history audit. Evidence commit **6a96f8870f0e88087d64341ed37dabf05df49f84**. Fixed task-start HEAD **cca9af23452870d1a12ba1ab6a78ebe683e49cd1**. Scientific freeze6fec32243985ccc808123d851abf5f3dea10af99; dispatch88668f76b22777459b5792dd28f88075f208c678. Later audit/delivery commits are outside this snapshot. Final Gate4 requires completed-run recorded checks and Research-Lead review under DEC1; this report does not supply final Gate4 PASS.

Files: research_log/t013/GATE4_PREOUTCOME_HISTORY_AUDIT.md, gate4_preoutcome_history_audit.py, gate4_preoutcome_history_receipt.json, gate4_preoutcome_history_initial_receipt.json. Handoff appends CODEX_TO_CHATGPT.md, project_state.md, REMOTE.md, session_log.md.

Command: D:/anaconda3/python.exe research_log/t013/gate4_preoutcome_history_audit.py (pinned task-start HEAD by default). Windows Python3.12.7, standard library and Git CLI only. It uses git show/rev-parse/merge-base/rev-list/diff/log/ls-tree; no detector/scientific imports, NPZ parsing or remote cache access. Final execution exit0, all13 mechanical checks true. git diff --check passes. The receipt records59 commits with parents/changed paths,97 unique changed-path classifications,17 protected hashes/blob IDs,17 evidence anchors and122 contextual reporting-search hits. Semantic absence findings are explicitly engineering review of committed evidence, not an automatic language proof.

Protected artifacts:10code_sha256 entries plus PLAN,vocabulary,selection,data receipt,image manifest,environment and freeze JSON. All17 exact git-show bytes equal the freeze hashes; endpoint git diff is empty; full-history merge-aware traversal has no intermediate protected edit/revert. Complete table:

| Protected path | Frozen and task-start SHA256 | Result |
| --- | --- | --- |
| scripts/t013_native_detector.py | b49f23f131777f08e23131ad55a94d9211c33b1c759adf86c6b52e2b95c34126 | identical |
| scripts/t013_native_run.py | 177176fdb1c133b98770f8e6719b22e3ead0a00adbdced598e92326aec723429 | identical |
| scripts/t013_native_smoke.py | d30430f324d0577afc6997c38d78d6f46b78679cb2adaf96055986344928a421 | identical |
| scripts/t013_analysis.py | 74cc73e71385e5d38e3fbe68ff03a0f11da30e67ff39b436da90422f72e99f9c | identical |
| scripts/t013_coco.py | bd3245235a6dcd455224ea7eb737b07875920b0a08b34f30e706dfc6a9ca9e81 | identical |
| scripts/t013_diagnostics.py | ae7e61feaa5701ca9580c9c48901f99d09e9986b560c2821073100c94645a41e | identical |
| scripts/t013_detector.py | 4800f1471f2de8f964700b683505c7230e078b6833a57afa1e09af6b42babd0d | identical |
| scripts/t013_text.py | 2c175a779304f045267e3419eda04dbc2e5c4730ae19cce23727043832102018 | identical |
| scripts/t013_native_vocab.py | 61d40e7f4107a2a13eaa7cd872667acaa4db3dffb3a257e2cddbaece4f943351 | identical |
| scripts/t013_data_receipt.py | 9ef780aa724d3a8a6f685dc0a273a285e7ce17942985fb107c2638810f54305e | identical |
| research_log/t013/PLAN.md | 5d977aceb3c06a7915396aea9c7cc2504759e584ce79b459a287b18fb67e4beb | identical |
| research_log/t013/vocabulary_native30.json | 3bb4a0ebada1f9da407ae6a94f1135798dba7117bd658a6ecba97b2ebfad0967 | identical |
| research_log/t013/image_selection.json | 8039a70f25c34f295345e63d1980f692631b6bbdaa5c37267a10852acbf3833b | identical |
| research_log/t013/data_receipt.json | 4dc1361b17a9221b278dd70ac805afb4d87742451b310af5381dc69900fe8c50 | identical |
| research_log/t013/image_sha256.json | 38eb39894b8c0f1924e099b3a1ec0b885fdf7ec43c86933e1dc28186d85c3ba8 | identical |
| research_log/t013/native30_environment.txt | 6fdb8b3da35dddb24c5ea602e81b160ab864e792ca29fa27236dd759a6b4f090 | identical |
| research_log/t013/native30_freeze.json | 50addfb8e247333b49fb22cda14570166b294101bb435b5a1b5bf688b4b3a91e | identical |
Checkpoint/model-state/annotation hashes are external-asset metadata preserved in the frozen JSON; this audit does not reopen those assets. Both archives and5000 JPEG hashes remain bound by protected data/image manifests. No additional Git path is directly hash-referenced by the freeze.

Chronology PASS: c07ce16 -> f63f571 ->6548870 ->02ba123 ->259217c ->eed8d1a ->d5dc807 ->35fbfb7 ->6fec322 ->88668f7 ->task-startHEAD, verified by ancestry. Original native/HF negative JSON, PARITY_B_RESULTS.md and parity_b.json are retained byte-identically with origin/head SHA in receipt. Native reset02ba123 at20:38:21+08/review259217c precedes freeze21:02:52 and logged launch21:03:55; dispatch receipt commits21:05:49. Original/reset/PLAN Gate1 thresholds1.0/lowerCI>0/>=2corruptions, Gate2 .75/.50/>=2positive contrasts, Gate3 non-rescue and Gate4 no outcome tuning are unchanged. Native30 capacity reset is explicit pre-outcome redesign, not parity rescue. Freeze includes17/17test evidence, exact data/vocabulary/environment bindings and pre-existing native-smoke/cached-smoke receipts. No primary outcome is used for this chronology claim.

Exact dispatch binding PASS: run20260912-210355-tovd-native30-primary/release20260912-210306-tovd-native30-primary-freeze/tmuxautodl-<run>, explicit immutable-release cd, single native_run --freeze-commit6fec322 followed by analysis only after inference success. Four text artifacts remain unchanged fromdispatch toHEAD: run.sh SHAcde77d0e8a4db8904d8ecd178efb71200013c0ed616d2bf471c88f6dfd8c1b27;meta.json SHAe9c8bd67854a9c1ee9d1a5b2f1470495cf4c616822102b226644b6fdf09dd6b0;resolved_release.txt SHA48599c3f821153bcd2e5d2ec1914a50a8bea614f8c9a270b98ae32c6baae3b55;freeze_sha256.txt SHA591e799f92b29a03b924fd9b3d32876d27f00732003177e8d5b9237edaf75757.

Post-freeze categories: coordination/reporting4 paths (three coordination files plus IMPLEMENTATION_NEXT.md); primary provenance/log mirror8 (three project logs plus five primary run-mirror files); pre-outcome verifier/test25 (OPS1/STAT1/FIN1/REPRO1/DEC1); YOLO contingency60 (contingency doc plus59source/metadata/protocol/fixture paths). Exact97-path list and every commit's changed paths are in receipt.postfreeze_changed_paths/commit_history; table and category interpretation in audit document. Zero unclassified paths, zero protected scientific edits, zero scripts/ or tests/ edits after freeze.

Control-history finding: **no committed evidence of contamination** from duplicate primary dispatch/writer, autonomous primary restart/resume or post-freeze scientific retuning. Only primary run-mirror files added at88668f7, no later mirror edit; inventory has one non-smoke native command plus the known earlier --smoke-only command. OPS1 independently recorded single writer721181; later health keeps samewriter/run. Existing COCO download resume and earlier smoke retries precede primary; FIN1 retry and REPRO1 mutation affect only completed engineering smoke/scratch. Git/logs cannot establish omniscient absence of off-repository behavior.

Outcome-blindness references cover dispatch/Lead acceptance, P0/P1/P2, OPS1,STAT1,FIN1,REPRO1,DEC1 and all health entries throughb8a5d5a. Receipt references pin commit,path,line,text andSHA, including p0_blindness,p1_blindness,p2_blindness,stat1_blindness,fin1_blindness,repro1_blindness,dec1_blindness,latest_health_blindness. Reports consistently distinguish opaque operational checks/synthetic/completedsmoke from activeprimary; no committed primary scientific output or claim found. REPRO1 old-smoke comparison correction remains disclosed and is not primary outcome access.

YOLO separation: accepted P0/P1/P2 only, source/tokenizer/metadata/protocol/model-freefixtures; no committed install/checkpoint payload/load/image inference/benchmark run. Upstream configs/demo/test code and model-card numbers are snapshots, not local execution. Native postprocessing/background conventions belong only to YOLO preparation; protected Grounding files untouched. FutureYOLO can test architecture specificity/cross-backbone replication, never mutate Grounding's state.

Observed audit-only error retained: initial helper exit1 incorrectly counted the known pre-freeze native pipeline smoke as a second primary because both invoke native_run. Its exact command contains --smoke-only before&&. Minimal classification fix distinguishes that flag, retains both entries, final13checksPASS. Initial receipt preserved; no actual protected-byte/order/primary-dispatch discrepancy and no scientific/history/run repair. No other task test/experiment failed.

End health only2026-09-13T08:10:43+08: exactprimary tmuxalive,writer721181 Rl+,392/1000 at39945.37502930101s,free22873034752bytes,no wrapper exit marker,analysis/results.json absent (existence only). active_primary_scientific_result_opened=false; active_primary_prediction_content_opened=false; frozen scientific/run state unchanged. No inference/YOLO/TTT work; inner-loss/gradient/update/reset diagnostics N/A.

Recommend Lead review G4A1 and use this fixed snapshot as pre-outcome history evidence only. Stop package; do not repeat whileheadingpersists. Continue immutableprimary and15-minutehealthmonitoring. No current FIN1/full-cache replay/primary interpretation,YOLO runtime,T014 orrestart/resume authorization beyond existing completion/failure procedures.

## T013-CLOSE1 — PASS; completion barrier prepared, primary still running

Lead2af6322 accepts G4A1. Evidence commit **0acbd4f6417d2946f2009979ec8461df351eb07b**; fixed task-start HEAD **2af6322facef6381835488a639761578b7fd2b16**. VersionT013-CLOSE1-v1. Primary freeze6fec32243985ccc808123d851abf5f3dea10af99/dispatch88668f76b22777459b5792dd28f88075f208c678 remain unchanged.

Files: research_log/t013/FINALIZATION_BARRIER.md, finalization_barrier.py, test_finalization_barrier.py, finalization_barrier_receipt.json, close1/smoke_rehearsal_envelopes.json, close1/mutated_smoke_replay_receipt.json. Handoff appends CODEX_TO_CHATGPT.md,project_state.md,REMOTE.md,session_log.md.

Command: D:/anaconda3/python.exe research_log/t013/test_finalization_barrier.py. WindowsPython3.12.7; standard library only. Initial focused run6testsPASS0.023s; after adding exact completion release/freeze binding and historical smoke-exit provenance, final6tests/62fixturesPASS0.028s. No failed tests; git diff --checkPASS. Helper has no I/O/imported scientific packages/command execution and does not calculate metrics or open results. Source SHAa227933e266090e1adab5395409ddf8ab037beb43c27f92b96713586d03d6c14; testSHA4868e3b038ec6dfb193cd227c71c7258d9f5277681f44ca1baed50a08f7e9aaa.

| State | Exact prerequisite / behavior |
| --- | --- |
| PRIMARY_RUNNING | Target completion run/release/freeze missing/mismatched, writer/tmux alive or termination unknown, or wrapper success not established; no FIN1/replay/scientific review. |
| PRIMARY_FAILED_RETURN_TO_LEAD | Bound wrapper nonzero; preserve and return to Lead, never restart/resume. |
| PRIMARY_COMPLETE_UNVERIFIED | Bound wrapper completed/exit0, writer/tmux gone; no exact FIN1 PASS yet. Missing FIN1 permits first verifier execution; stale/FAIL/PENDING evidence remains blocked with execution disabled. |
| FIN1_PASS_READY_FOR_REPLAY | Exact target FIN1 PASS; only absent replay permits first frozen replay/comparison. Stale/FAIL/PENDING/mismatched replay remains blocked with execution disabled. |
| REPLAY_PASS_READY_FOR_RESEARCH_LEAD | Same-cache FIN1 and exact frozen full replay compared against actual wrapper auto-analysis PASS. Only later Lead review authorized; never scientific acceptance. |

analysis_result_exists is ignored as an unlock signal: early existence while running/unverified is normal, not itself a violation, and never permits scientific review. The FIN1-ready intermediate state permits only the prescribed machine replay/comparison, which necessarily parses arrays/JSON internally; primary_result_content_access_authorized for research review remainsfalse until final readiness. The barrier itself never opens content. Scientific acceptance and restart/resume outputs arefalse in every state.

Bindings: contract_version,task_start_head,run_id,release_id,freeze_commit,cache_path,cache_receipt_ref/cache_receipt_sha256,manifest_sha256,scope,1000images/15000records,receipt_freeze_argument,analysis_sha256,exactanalysis_reference_dir; FIN1 version/hashT013-FIN1@8efe485/9d4c604b40677d81fa634715a55c7132dcbe04303a1a8a3021dc11e42273c6a8; comparatorversion/hashT013-REPRO1@5fe57f7/6270a32096c536deac8ec878d3cfbfeb1cc067d428781ab7beb09e78cb8acb76. Each execution envelope binds receipt_ref/SHA,toolSHA and unchanged accepted-tool result. Replay additionally binds exactFIN1receiptSHA,leftauto-analysis/rightfreshscratchpaths,analysis/comparator exit0,freezeanalysisSHA74cc73e7...,1000replicates,andall4comparisonartifactsequal. Envelopes are execution metadata captured from actual commands/receipts, not changes to FIN1/replay scientific schemas or cryptographic authentication.

62fixtures:13ordered/completioncases;4earlyanalysisexistencecases;5wrapper/FIN1/replayfailure-or-pendingcases;26stale/missingrun/release/freeze/cache/receipt/manifest/taskHEAD/toolversion/hashcases;8wrongauto-analysis/selfcomparison/linkage/source/replicate/exit/artifactcases;6completed-smokereuse/cross-primary/negativecases. Every state below final readiness has primarycontentaccessfalse. WrongrunFIN1 and wrongfreeze/cache replay rejected; replay cannot skipFIN1; comparatorPASSfromsmoke cannot unlockprimary.

Completed45-cellsmokedry-runPASS by allowed reuse of accepted FIN1 and REPRO1 evidence only. Verified matching source hashes, same3-image/45-cellcache receipt/manifest hashes and historical wrapperexit0; termination metadata is historical rehearsal, not a freshremoteprocessquery. Smoke transitions complete-unverified ->FIN1ready ->replayA/Bready, withprimarycontentaccessfalse throughout. Exactoriginalsource receiptbytes unchanged. Retained scratch cachebindingmutation rejected. Originalsmoke auto-analysis comparison remainsNOTCOMPARED because of its old analysis source; its receipt does not unlock readiness. Reused frozen A/B comparison is explicitly a smoke rehearsal and never claims original-auto-analysis parity or primaryreproducibility.

Future commands/templates are frozen in FINALIZATION_BARRIER.md: waitwrapperexit0/bothprocessesgone; failure->Lead; hashcompletedcachemetadata/toolsource; runacceptedFIN1onexact15000-cellcache; onlyPASS->runexact6fec322analysiswithout--smoke-only to newshared/t013/close1-primary-replay; compareactualprimaryartifacts/analysis againstnewreplay usingacceptedREPRO1comparator; bindactualreceipts/commands/hashes andpersistbarrierfinalready; onlylaterLead openscompleteDEC1disclosure. No automatic command dispatch or scientific acceptance. No primary FIN1,analysis,replay or scientific comparator executed in CLOSE1. No additional compute/install/YOLO/T014 work.

End health2026-09-13T09:08:07+08: exactprimary20260912-210355-tovd-native30-primary tmuxalive,writer721181 Rl+,426/1000 at43353.357239504025s,free22307053568bytes; no wrapper exitmarker,analysis/results.json absent(existenceonly). active_primary_scientific_result_opened=false; active_primary_prediction_content_opened=false; frozen scientific/run state unchanged. No TTT; innerloss/gradient/update/resetN/A.

Recommend Lead review CLOSE1. Stop package, do not repeat unchangedheading. Continue immutableprimary and15-minutehealthmonitor. Finalization/interpretation only when the established completion/Lead conditions apply; noYOLO/T014/restart/resume authorization.

## T013-OPS2 — PASS / awaiting Research Lead review

Evidence commit **e380d14e5ee7b830781d38cc9efae292509ca66a**; task-start HEAD **7ccfe778148930a0fe67808f84726de7aca229ae**. Lead bc74aa6/0f39342 accepts CLOSE1 and assigns OPS2. The heartbeat push encountered concurrent Lead updates; merged both histories before executing the package.

Files under research_log/t013: PRIMARY_SURVIVAL_GUARD.md, primary_survival_guard.py, test_primary_survival_guard.py, primary_survival_guard_tests.txt, primary_survival_guard_receipt.json, primary_survival_guard_live_health.txt. Exact remote health command is in the note; test command: `D:/anaconda3/python.exe -m unittest discover -s research_log/t013 -p test_primary_survival_guard.py -v`.

Pure scalar helper, fixed total 1000 / P95 16355328 bytes / multiplier 6/5 / reserve 8589934592 bytes. remaining=1000-closed; projected=P95*remaining; required=(6*projected+4)//5+reserve; margin=free-required. This exactly implements ceil(1.20*projected+8GiB); SAFE iff margin>=0. No new threshold. Process failure/nonzero takes precedence; inconsistent process/exit metadata returns PROCESS_STATE_AMBIGUOUS_RETURN_TO_LEAD; storage is always reported separately for valid inputs. Invalid scalars raise ValueError and cannot return SAFE. No repair/restart/resume behavior.

5 tests / 32 fixtures PASS: 2 known snapshots, 6 equality/one-byte-below boundary cases, 12 invalid storage, 8 process states, 4 invalid process. At188, required24526566196 and margin2176675020 reproduce OPS1; at456, projected8897298432, required19266692711, margin2484468121 exactly match Lead. Three historical rehearsals (188/456/467) from committed session_log lines at task-start HEAD are SAFE; exact lines and source commit retained. No failed tests or formula deviation.

One end-of-package live metadata query at2026-09-13T10:20:53+08:00: exact primary20260912-210355-tovd-native30-primary, writer721181 Rl+ and tmux alive;469/1000 at47754.84462102302s; free21460013056 bytes; projected8684679168, required19011549594, margin2448463462; SAFE / PRIMARY_RUNNING. No wrapper exit marker, analysis/results.json absent by existence only. Raw metadata and computed receipt retained.

No active-primary prediction/scientific content opened; no cache files scanned or modified for OPS2; no frozen scientific/run state or environment change. No FIN1/analysis/replay/comparator, no YOLO runtime, no T014. TTT diagnostics N/A for this scalar helper. Stop OPS2 and await Lead review. Future existing15-minute health reports include required_free/margin/status; any specified return-to-Lead state is reported without remediation. Existing immutable-primary completion/CLOSE1/DEC1 conditions remain unchanged.

## T013-OPS3 — PASS / awaiting Research Lead review

Evidence commit **6ecbc36bd66eb2e4ca6057f9a33c81863ed7eff7**; task-start HEAD **65b1075be239e0fb8caaf451a9769e4a48aec040** accepts OPS2 and assigns OPS3.

Seven files under research_log/t013: PRIMARY_INCIDENT_SNAPSHOT.md, primary_incident_snapshot.py, collect_primary_incident_metadata.py, test_primary_incident_snapshot.py, primary_incident_snapshot_tests.txt, primary_incident_snapshot_receipt.json, primary_incident_snapshot_live_raw.json. Test command: `D:/anaconda3/python.exe -m unittest discover -s research_log/t013 -p test_primary_incident_snapshot.py -v`. Exact remote one-shot command and schema are documented in the note.

Pure canonicalizer reuses accepted OPS2 health_guard; source checked against e380d14 after Git line-ending normalization, hashes recorded. No formula reimplementation/refit. Exact run/release/freeze/dispatch/PID/tmux/repository/OPS2 evidence bindings, current caller Git HEAD, timestamp, raw-source references, parsed process/progress/storage, analysis existence and scope attestation retained. Missing/malformed evidence raises ValueError without fabricating a status. Completion is preserved as PRIMARY_COMPLETE_UNVERIFIED, never scientific readiness. Every snapshot keeps scientific access, FIN1 execution and remediation authorization false.

4 tests / 55 fixtures PASS in0.002s:7 state/determinism cases (healthy SAFE, storage risk, wrapper failure, process ambiguity, completion-unverified, early analysis existence, zombie writer);9 wrong bindings;20 missing fields/source references;19 malformed scalar/process/progress/marker/scope cases. Input immutability and deterministic output verified. Early analysis existence changes only its boolean, never state/access. Historical committed499-image health line replayed SAFE, with exact source line and canonical result retained. No test failure or design deviation.

Exactly one live collection at2026-09-13T11:33:01+08:00 using existing remote Python and LC_ALL=C. Collector read operational meta.json/resolved_release.txt, anchored progress/wrapper markers via grep, date/ps/tmux/df, and Path.exists for analysis only. Run20260912-210355-tovd-native30-primary;512/1000 at52080.396239708s; writer721181 Rl+ and tmux alive; wrapper markers empty; analysis_result_exists=false. Free20627927040, remaining488, projected7981400064, required18167614669, margin2460312371; SAFE / PRIMARY_RUNNING. Raw stdout JSON and SHA-bound canonical snapshot preserved. Only1043-byte operational meta.json hashed; exact remote bytes equal retained local original (Git LF-normalized representation separately explained in note).

No active-primary prediction/scientific content opened, active cache recursively scanned/modified, frozen science/run/environment changed, or cleanup/kill/restart/resume/duplicate/YOLO/T014 action occurred. No FIN1/analysis/replay/comparator. TTT diagnostics N/A for this operational helper. No new loop/scheduler. Recommend Lead review OPS3; stop package now. Continue existing15-minute scalar health checks. On incident or PRIMARY_COMPLETE_UNVERIFIED preserve snapshot and return to Lead; per latest mailbox do not execute FIN1 until later Lead review explicitly advances CLOSE1.

## T013-OPS4 — ACTIVE / snapshot A preserved, awaiting next existing heartbeat for B

Implementation/A evidence **882034a2381564044ea2ba1d14c3fe987b39f442**; task-start **032de1a44ae19d0fda497fe43909b0fee98f63ab**. Six files under research_log/t013: PRIMARY_STORAGE_ATTRIBUTION.md, primary_storage_attribution.py, test_primary_storage_attribution.py, primary_storage_attribution_tests.txt, primary_storage_attribution_A_raw.json, primary_storage_attribution_receipt.json. Exact test/live commands are in the note.5 tests/31fixtures PASS; zero/positive/negative residuals, zero image delta, binding/time/progress failures, malformed/missing df/du/process evidence and unhealthy states covered. Reuses unchanged OPS2; no new safety threshold.

A at2026-09-13T12:27:10+08:00:544/1000,55303.571372162s,writer721181 Rl+/tmux alive,no wrapper marker,analysis absent(existence only). Free19348643840;run_du8877875200;cache_du8877797376;required17539570074;margin1809073766;SAFE/PRIMARY_RUNNING. Exactly one live snapshot collected; narrow authorized aggregate du traversals only. No prediction/scientific content opened, active files hashed/modified, FIN1/replay or cleanup/restart/resume/YOLO/T014 action. B will be collected once at the next existing approximately15-minute heartbeat, before any separate routine health query; receipt remains AWAITING_SECOND_HEARTBEAT_SNAPSHOT and no attribution/OPS4 PASS is claimed yet.

User added "btw尽量用GPU跑。" Recorded preference to prioritize GPU for subsequent new experiments and validate that path during preparation; current primary retains frozen CPU FP32/four-thread settings without a mid-run device change or duplicate run.

## T013-OPS4 — PASS / awaiting Research Lead review

Final evidence **0d825766d0fcbc60bf090f83ddc799f7fcabeffb**; implementation/A evidence882034a2381564044ea2ba1d14c3fe987b39f442; task-start032de1a44ae19d0fda497fe43909b0fee98f63ab. This completes the previously pending second snapshot. Files under research_log/t013: PRIMARY_STORAGE_ATTRIBUTION.md, primary_storage_attribution.py, test_primary_storage_attribution.py, primary_storage_attribution_tests.txt, primary_storage_attribution_A_raw.json, primary_storage_attribution_B_raw.json, primary_storage_attribution_receipt.json.

Test command: `D:/anaconda3/python.exe -m unittest discover -s research_log/t013 -p test_primary_storage_attribution.py -v`;5tests/31fixtures PASS in0.003s (3 zero/positive/negative residual,1 zero-image,6 binding/time/progress,17 malformed/missing evidence,4 unhealthy states). Unchanged tested source and A raw hashes checked when calculating B; no new code requiring retest. Reused fixed OPS2 health_guard, no formula refit or new thresholds.

Exactly two live invocations, existing SSH workflow/project Python: `LC_ALL=C /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python /home/wenchang/asdasdsad/wjq/TOVD/research_log/t013/primary_storage_attribution.py`. Every raw command/output/exit code retained. Aggregate du commands exactly `du -x -B1 -s --` the pinned run and cache roots; df command `df -B1 --output=avail /home/wenchang/asdasdsad/wjq/TOVD`. No additional health query, scheduler/loop or third du snapshot. B taken at the next existing heartbeat; actual spacing1103s=18m23s due task/heartbeat dispatch timing, explicitly recorded rather than claimed exact15minutes.

A2026-09-13T12:27:10+08:00:544/1000,55303.571372162s,writer721181 Rl+/tmux alive,wrapper absent,analysis absent(existence only);free19348643840;run_du8877875200;cache_du8877797376;OPS2 remaining456/projected7458029568/required17539570074/margin1809073766;SAFE/PRIMARY_RUNNING.

B2026-09-13T12:45:33+08:00:556/1000,56483.772476741025s,samewriter721181 Rl+/tmux alive,wrapper absent,analysis absent(existence only);free18837422080;run_du9061552128;cache_du9061474304;OPS2 remaining444/projected7261765632/required17304053351/margin1533368729;SAFE/PRIMARY_RUNNING.

Exact attribution: delta_images12;free_consumed511221760bytes;active_run_growth183676928;cache_growth183676928;noncache_run_growth0;outside_run_pressure327544832;cache_growth_per_new_image15306410.666666666bytes/image. Measured active growth explains183676928 of511221760 bytes consumed; residual327544832 is outside the run's measured net growth. This is an accounting residual, not proof of a particular external writer, not an explanation of earlier intervals, and not a new safety gate. Sequential measurements are not atomic and a partially completed image can contribute allocated growth. No threshold or cleanup recommendation derived from the residual.

No prediction/scientific content opened, active files modified/hashed, FIN1/replay/scientific analysis or cleanup/kill/restart/resume/duplicate/YOLO/T014 action. Only explicitly authorized aggregate metadata du enumeration; no per-image/condition/vocabulary tables. TTT diagnostics N/A. Stop OPS4 and await Lead review; ordinary15-minute scalar health cadence resumes without repeated du audit. User GPU preference persists for subsequent new experiments; current frozen CPU primary unchanged. Incident/completion-unverified returns to Lead before any remediation/FIN1 advancement.

## T013-OPS5 — ACTIVE / A preserved, awaiting next existing heartbeat for B

Implementation/A evidence **0e9551ea2a4204dcad39050d884930f91073f253**; task-start **b3b27c6258bda129968cac10e74a8080fed392a9** accepts OPS4. Six files in research_log/t013: PRIMARY_PROJECT_STORAGE_ATTRIBUTION.md, primary_project_storage_attribution.py, test_primary_project_storage_attribution.py, primary_project_storage_attribution_tests.txt, primary_project_storage_attribution_A_raw.json, primary_project_storage_attribution_receipt.json. Exact local test and remote collection commands in note.5tests/32fixtures PASS:3 zero/positive/negative residual,1 zero-image,7 binding/time/progress,17 malformed/missing evidence,4 unhealthy state cases. OPS4 parser pattern reused as a minimal separate variant; original helpers unchanged, imports accepted OPS2 health_guard and primary bindings; no formula refit or new gate.

Exactly one snapshot A2026-09-13T13:04:34+08:00:567/1000,57517.53246723002s,writer721181 Rl+/tmux alive,wrapper marker absent,analysis result absent(existenceonly). Free18642763776;project_du16055738368;run_du9255936000;OPS2 remaining433/projected7081857024/required17088163021/margin1554600755,SAFE/PRIMARY_RUNNING. Only project/run aggregate du traversals; no cache du/per-directory tables/outside-project scan. Raw commands/outputs retained. No scientific/prediction content, active-file hashes/mutation, FIN1/replay/scientific analysis, cleanup/restart/resume/YOLO/T014. No deviations or test failures.

B will be collected once at the next existing approximately15-minute heartbeat, without an additional normal health query or third snapshot. Receipt remains AWAITING_SECOND_HEARTBEAT_SNAPSHOT; no attribution or OPS5 PASS claimed. Both residuals will remain descriptive non-atomic accounting, not writer identity, threshold/forecast/cleanup triggers. GPU preference remains recorded for subsequent new experiments; current frozen CPU run unchanged.
