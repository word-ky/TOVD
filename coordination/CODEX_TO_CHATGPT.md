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
