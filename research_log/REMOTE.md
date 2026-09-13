# TOVD remote execution and heartbeat recovery

- Local root: `D:/work/fightccfa-agin/CVPR2027/TTT-OVD`.
- GitHub source of truth: `word-ky/TOVD`, branch `main`.
- A6000 hostname verified: `wenchang-PR4904W1`; two NVIDIA RTX A6000
  cards, each idle with 15 MiB used at initial inspection.
- Existing writable directory: `/home/wenchang/asdasdsad/wjq`.
- TOVD remote base: `/home/wenchang/asdasdsad/wjq/TOVD`.
- Project environment: `<remote-base>/.venv`, using system site packages from
  `/home/wenchang/anaconda3/envs/python3.12-tk2-2.3/bin/python`.
  Base Python is 3.12.12, PyTorch 2.4.0+cu121; pytest is absent in the base
  interpreter and is installed only in the TOVD environment.
- Local control scripts: `D:/work/claude-autodl/autodl-workflow-clean/scripts`.
  Run from that workflow root with `AUTODL_CONFIG_PATH` pointing to
  `D:/work/fightccfa-agin/CVPR2027/TTT-OVD/.autodl/config.json`.
  The project-specific connection config is local-only, ignored by Git.
- Deploy: `scripts/autodl-deploy.ps1 -Tag tovd-t001 -Source <local-root>`.
- Run: `scripts/autodl-run.ps1 -Name tovd-t001-a6000 -Cmd
  'export TOVD_SOURCE_REVISION=<tested-commit>; bash scripts/run_a6000.sh'`.
- Inspect: `scripts/autodl-logs.ps1 -RunId <id> -Lines 80`.
- Fetch with `Copy-FromAutodl` in `scripts/Autodl.Common.ps1`, copying
  `<remote-base>/runs/<id>` into this project's `research_log/remote_runs`.
- Use explicit release/run IDs from this project's report, not the workflow's
  global last-run state shared by other projects. Mirror relevant receipt IDs
  here after deploy/run. Artifacts remain within this project locally/remotely.

Heartbeat `tovd` is ACTIVE, attached to this Codex task, every 15 minutes.
It reads project logs and the latest research mailbox, directly executes clear
active work, checks existing runs, writes the engineering report and pushes
commits. No new task is inferred from an unchanged ACTIVE T001 that has already
been VERIFIED. Research acceptance and T002 selection remain with the lead.
Unchanged/non-actionable checks stay quiet; meaningful progress, completion,
failure or required user input is reported. User authorized this on 2026-09-12.

Release: 20260912-011056-tovd-t001, implementation SHA a34403756ebe049098c8850f08a1621edec0d6ce.
Run: 20260912-011209-tovd-t001-a6000. Earlier preparation attempt 20260912-011126-tovd-t001-a6000 failed before execution due to SSH timeout; retain its metadata.

Run 20260912-011209-tovd-t001-a6000 completed with exit 0 at 2026-09-12 01:12:21 +08:00; CPU 10/10, CUDA 10/10, both demos passed. No active TOVD tmux session remains. Complete receipts fetched to research_log/remote_runs and retained on remote.

## T002 completed
Implementation b88153a44836310219201404509cfd568c02614f; release 20260912-023118-tovd-t002.
Run 20260912-023122-tovd-t002-a6000 exited 0 at 2026-09-12 02:39:18 +08:00. Full CPU 23/23 and CUDA 23/23 suites passed, 15 models trained/evaluated, independent checkpoint evaluation matched. No active job remains.
Run script: scripts/run_t002_a6000.sh. Full receipts/checkpoints under remote runs/<run-id>/artifacts/t002 and local research_log/remote_runs/<run-id>. Read project_state.md and the latest engineering report before acting on unchanged ACTIVE T002.

## T003 completed
Analysis SHA 6780de5ae44dcc89b9f1c45ea781f33dc16ffbaf; release 20260912-030919-tovd-t003.
Run 20260912-030923-tovd-t003-a6000 exited 0 at 2026-09-12 03:10:33 +08:00. CPU/CUDA suites 30/30 each; all 1200 fixed P/B2 checkpoint/episode diagnoses completed. No active TOVD run remains.
Source remains original T002 runs/20260912-023122-tovd-t002-a6000/artifacts/t002. New artifacts in runs/20260912-030923-tovd-t003-a6000/artifacts/t003; full local copy in research_log/remote_runs. Read project_state.md and latest report; wait for explicit next task.

## T004 completed
Runtime/screen SHA 9afe8df54c22d0a20b284d6b4b20aaab5b36ea9a; release 20260912-043213-tovd-t004-screen.
Run 20260912-043224-tovd-t004-screen-a6000 exited 0 at 2026-09-12 04:34:08 +08.
CPU/CUDA full suites 53 each. All 2400 diagnoses finite and paired with zero drift.
Phase-1 gate selected none; no Phase 2, no active job. Full local receipts under research_log/remote_runs.
Project state and T004 reports are the source of truth; do not rerun unchanged ACTIVE task.
Initial deployment 20260912-043206-tovd-t004-screen failed SSH exit 255 before job launch; retry succeeded.

## T005 completed
Tested f2b9722ae8a1ad68e0e529488e68f88c170125de; release 20260912-053814-tovd-t005.
Run 20260912-053826-tovd-t005-a6000 exited 0 at 2026-09-12 05:42:14 +08 on physical GPU1.
CPU/CUDA suites70 each; 2400 records finite, zero O0/C0 drift, all source hashes match.
C2 passes descent/task-useful rules; C1 fails full scale-rescue/task-useful rules. No training permitted without next task.
Full original receipts retained under remote runs/<run-id>/artifacts/t005 and local research_log/remote_runs/<run-id>.
No active TOVD run; another project occupied GPU0 and was left untouched.

## T006 completed
Tested65299db5f1127407f856872b732f2b2b7051383e; release20260912-065052-tovd-t006.
Run20260912-065105-tovd-t006-a6000 exited0 at2026-09-12 06:56:11+08 on physicalGPU1.
Three400x4seedruns completed, CPU/CUDA75tests each. All source/control/normalpath checks exact.
Rules1/2/4/5pass;Rule3fails:hardadapted34.625%vsB2 44.625%. Awaitlead; no detector/T007.
Fullreceipts under remote runs/<run-id>/artifacts/t006 and local research_log/remote_runs/<run-id>.
NVML kernel/library mismatch noted; PyTorch CUDAworked and no globaldriver change made.
One fetchtransporttimeout recovered by existing legacySCP retry. No activeTOVD job remains.

## 2026-09-12 08:34 +08 T007 dispatch
Tested e88ad88112f6486f8c7dc8458594e095528ba9f1; release20260912-083405-tovd-t007.
Run20260912-083417-tovd-t007-a6000 active on physicalGPU1;79 local tests pass.
Six fixed400x4 runs follow remote CPU/CUDA suites; no T007 aggregate read.

## 2026-09-12 T007 completion
Run20260912-083417-tovd-t007-a6000 exit0 at08:47:19+08;79CPU/CUDA tests each.
Six fixed400x4 runs completed. Rules1/2/5PASS;3/4/6FAIL; no detector/T008.
W2hard43.54167% versusW1+C2 45.375% andT00546.25%; W2easyseed27 -7.625pp.
W1easy also harmed6.79167pp; retain fixed-T005 reference, flag checkpoint/seed dependence.
105 rawrunfiles,6final+30trajectory checkpoints and1200oracle episodes retained locally/remotely.
Normal/historical/source/step0 checks exact. Report/curves inresearch_log/t007.
Renderer OpenMP conflict fixed by removing unnecessary torch import; experimental code unchanged e88ad88.
No activeTOVD run; awaitlead, heartbeatactive.

## 2026-09-12 10:13 +08 T008 dispatch
Run20260912-101332-tovd-t008-a6000 active onGPU1; release20260912-101316-tovd-t008.
Tested153ac30d00753b43a56ce2e226068b0c35039d70; local85tests pass.
33 fixedstates/6600raw episodes; no training/controller; remoteCPU/CUDA tests precede extraction.

## 2026-09-12 10:32 +08 T008 evidence finalized
Run 20260912-101332-tovd-t008-a6000 exited 0 at 10:20:21 +08. Local/remote CPU/remote CUDA each 85 tests passed.
33 frozen states, 6600 raw / 5400 primary rows; historical/feature/oracle equality exact, all parameters unchanged.
All 14 scalar gates fail the original overall LOSO .70/.65 requirements; best mean .580556, best pre-update .538529.
Complete 76-file original receipt fetched, hashes in t008/verification.json; 66 raw record files. Tables and three PNG/SVG figures generated and visually checked; corrected plot legend overlap.
No runtime changes since tested 153ac30. No controller, training, detector or next task. Await Research Lead; do not duplicate VERIFIED T008.
Final engineering mailbox and project state written; syncing local report and recovery logs to A6000 and committing evidence to GitHub.

## 2026-09-12 11:03 +08 T009 complete
Preregistration1b63bf6; tested3e56b0cca890ea83873e48ee68f69593b78af9b7. Pure local frozen-log analysis exited0; no model/GPU rerun.
54 source hashes match,27states/5400episodes/43200queries; 90localtests passed26.18s. Historical query harm sign differences0, accuracyexact, NLL rounding within2e-6; deterministic repeated extraction.
A PASS: delta_entropy meanLOSO .750696/min .722485, delta_max_probability .708225, delta_probability_gap .709433. Allpost-candidate; no pre-update passes.
B PASS: all preregistered oracle hard-gain/easy-regression clauses pass. This is a label-using oracle ceiling, not a deployed policy.
Report renderer initially failed on empty hardQ4 bin; plot now showszero. Three PNG/SVG figures visuallychecked; trailing EOF whitespace fixed, no semantic analysis changes.
All evidence in t009/results plus RESULTS/verification. Final engineering mailbox and state updated; mirror to A6000 project then commit/push. Await lead review/newT010; no autonomouscontroller/detector.

## 2026-09-12 11:44 +08 T010 calibration dispatch
Tested1b60f217f67c283df1e49f73f4bb4f2b64e03955; release20260912-114356-tovd-t010-cal.
Run20260912-114426-tovd-t010-cal-a6000 on physicalGPU1. RemoteCPU/CUDA tests then1800 base calibration episodes only.
Local95tests passed40.01s. No validation outcomes yet; fetch/commit actual thresholds before validation.

## 2026-09-12 12:05 +08 T010 calibration complete; thresholds frozen before validation
Run20260912-114426-tovd-t010-cal-a6000 exited0 at11:45:50+08. RemoteCPU95passed8.74s/CUDA95passed25.42s.
Full original receipt fetched:18raw files/1800episodes/14400queries; hashes/code exact, reset/oracle equality exact, nllmaxerror8.714e-7,accuracyerror0.
LOSO tau7=-0.11053594030393298; tau17=-0.11194298182737498; tau27=-0.12223384632396617. Each uses9600basecalibration queries fromother2seeds; selected calibrationNLL .5459873254/.5411123192/.5473287022.
Fetched/merged lead interim approvals b3f1105/434ed81, which reaffirmed unchanged two-stage execution. No validation episode generated/scored yet.
Commit actual thresholds and complete calibration receipts now, then deploy validation using exact tested1b60f21 semantics. No threshold/feature/policy/gate changes.

## 2026-09-12 12:06 +08 T010 novel validation dispatch
Actual thresholds and complete calibration receipts committed/pushed bbfaa8608d259527f88c996d7ad61420bb7af41f before validation generation.
Validation release20260912-120531-tovd-t010-val; run20260912-120555-tovd-t010-val-a6000 onGPU1.
Core testedrevision1b60f217f67c283df1e49f73f4bb4f2b64e03955 unchanged. 3600 fresh novel episodes; no calibration/policy changes.
All5 gates fixed; await explicit run completion and preserve every result regardlessofoutcome.

## 2026-09-12 12:13 +08 T010 final evidence
Validationrun20260912-120555-tovd-t010-val-a6000 exit0 at12:07:29+08. Gates1/2FAIL,3/4/5PASS; no policychanges afteractualthresholdcommitbbfaa86.
All3600freshnovel episodes recovered, alongside1800basecalibration;52originalrunfiles hashed,36rawrecordfiles. Compressed validation transfer SHA256d1cd989c4c7585ad743a62f7ae5e9f23abef161999d0e0f1b103ca835a4f840c matchesremote.
Historical scoringerrorwithin2e-6; accuracy andselected-token probabilitiesexact; normal/oracle bitwise equalityandparametersunchanged. Local/remoteCPU/CUDA95tests each pass.
Both plots visuallychecked; allsummary/gate/per-cell/headroom tables retained. R2throwsawayhardutility despiteeasyregressionremoval; recommendterminatecurrentrollbackline, awaitleadreview. No activejob/retuning/detector.
Final report/state/recoverylogs written; syncingtoA6000 andcommitting/pushing completeevidence.

## 2026-09-12 13:32 +08 T011 dispatch
Tested79e6e2baac5b92dd8b66c1a8a048a4d5013f5d5b; preregisterb615642. Release20260912-133111-tovd-t011; run20260912-133149-tovd-t011-a6000 onGPU1. FullCPU/CUDA tests precede1800episode screen in script. No outcomes/changes yet. Source/config/hashes unchanged.

## 2026-09-12 13:38 +08 T011 screen finished; recovery in progress
Run20260912-133149-tovd-t011-a6000 exit0 at13:37:55+08. All1800episodes/14400queries complete, validityTrue. Five scientific criteria allFAIL. OverallS0/S1/S2/S3 NLL .9079148837/.8539555307/2.4197990865/2.3612078392; accuracy59.7916667/63.1180556/29.8263889/27.3402778percent. ResidualdiversityS2 .4102165641 vsS3 .4302423724. S2accepted14397/14400, finite/nonzero/reset/vocabularychecks pass but utility fails. No repair/tuning.
Downloading34MB losslessfullrunarchive; remoteSHA2565567735c5f387ab5ffed8bbfa33280b3a80a9b4522b28d86bf8324886bc10bc9. Finalverification/report/commit pending retrieval. A read-only remote Python summary command had shell-quoting SyntaxError; cat of immutablegates/summary succeeded, scientificrun unaffected.

## 2026-09-12 13:46 +08 T011 final evidence
All27runfiles/18rawrecords recovered; archiveSHA5567735c5f387ab5ffed8bbfa33280b3a80a9b4522b28d86bf8324886bc10bc9 matches. Raw1800episodes/14400queries and aggregateNLL checked. Fullreport/tables/diagramPNG/SVG generated and plot visuallychecked. All5scientificcriteriaFAIL; engineeringvalidityTRUE,101tests eachlocal/CPU/CUDA. Stoprule enforced; no furthermethodchanges. Preparing final commit/push and mirroring projectrecovery/reports toA6000.

## 2026-09-12 14:19 +08 T012 base calibration dispatch
Tested8c4abff9140f1d762175472117bf6b9c3d5fcb21; preregister15d3353. Release20260912-141825-tovd-t012-cal; run20260912-141907-tovd-t012-cal-a6000 onGPU1. CPU/CUDAfulltests then1800baseepisodesonly. Actualglobal-lambda freeze andnovelphase stillpending. No noveloutcomes.

## 2026-09-12T14:23:46.837199+08:00 T012 calibration complete / actual lambda awaiting freeze
Run20260912-141907-tovd-t012-cal-a6000 exit0 at14:20:21+08. Global lambda=.2 minimizesbasequeryNLL .5526825519311226 (A0 .5538713284614907),14400queries. All7candidatevalues retained. Fullarchive downloadinprogress, remoteSHA256c591d3e97d164e42dc477b604b5044fcb3cc27d3f8c35a95ad8d0036c9144b2d. No novelmodel/outcomes generated. Next verifyarchive, commitactualvalue+completecalibrationreceipt, thenseparatenovelphase.

## 2026-09-12T14:25:17.972525+08:00 T012 actual global lambda freeze — BEFORE novel evaluation
Calibration20260912-141907-tovd-t012-cal-a6000 exit0 at14:20:21+08;1800baseepisodes/14400queries. CPU108passed9.36s,CUDA108passed27.36s (local108passed53.20s). Selectedsinglelambda=.2,baseNLL .5526825519311226;A0 .5538713284614907. Grid[0,.05,.1,.2,.5,1,2], no per-state/regime/seed adjustment. frozen_lambda.json SHA256b3f7219e55426b99f21761ba04bc872d79228a42f63ec93d6ff4300a0f7b1a5d.
Complete25originalfiles/18rawrecords recovered; archiveSHA256c591d3e97d164e42dc477b604b5044fcb3cc27d3f8c35a95ad8d0036c9144b2d matches. Allsource/code hashes verified, model tensorsunchanged/gradNone, staticinference/replayexact; maxA0NLLerror2.08616257e-7,accuracy0. No novel scientificoutcomes generated orscored yet.
Committingactualvalue, CALIBRATION.md, calibration_receipt/manifest/transfer andrawrecords now, then deployunchangedtested8c4abff core withfrozenlambda for1800novel episodes. Pure write_report.py added; no scientificcode/gatechangeaftertests.

## 2026-09-12T14:27:09.129736+08:00 T012 frozen-lambda novel validation dispatch
Actual lambda .2 andfullbasecalibration committed/pushed22ffbdf8d7952eb8450097cfb84ef0cbef5c4d0e BEFORE novel generation. Release20260912-142547-tovd-t012-val; run20260912-142634-tovd-t012-val-a6000 onGPU1. Testedcore8c4abff9140f1d762175472117bf6b9c3d5fcb21 unchanged; 1800novel episodes, onefrozenlambda for allstates/seeds/regimes. No retuning or extraexperiment. Next inspect explicitruncompletion, recoverraws, evaluatefixedgates; iffailed prepare synthesis andstopprogram.

## 2026-09-12T14:29:45.398190+08:00 T012 novel run complete / recovery pending
Novelrun20260912-142634-tovd-t012-val-a6000 exit0 at14:27:48+08. Gates1/2FAIL,3/4/5PASS. AllthreeaggregatehardNLLchangesA2-A0 positive .0027178433/.0031134898/.0010490485; improvingseeds0/1/1. Easy safety passes; localA2beatsuniformA3 NLLby .0002701599hard/.0037786987easy. Overall A0/A2 NLL .8406563464/.8422603823, accuracy63.0416667%/62.75%. Small negativeutility, not T011-scale collapse. Fixedglobal .2 unchangedafterfreeze22ffbdf.
Full16MBrawarchive downloadinprogress; remoteSHA256ba5a946114948393929f03b011f0355d0c694e8d24c0fc8d95568cf4fda4f489. No activeTOVDexperiment. Applytaskstoprule: no further syntheticmechanism, prepareboundedT001-T012 synthesis preservingT005/T009/T012scopedpositiveevidence. Finalartifactverification/report/push/mirrorpending.

## 2026-09-12T14:33:57.632563+08:00 T012 final evidence
All52originalfiles/36rawrecords recovered,3600episodes/28800queries acrossphases; hashesmatch. Fixedlambda .2 remainsSHA b3f7219e55426b99f21761ba04bc872d79228a42f63ec93d6ff4300a0f7b1a5d. NovelrawNLLmatchesaggregates1e-12; historicalscoringerror3.62051651e-7 andaccuracy0; source/state/replay/inferencechecks allpass. Gates1/2FAIL,3/4/5PASS. RESULTS/SYNTHESIS/per-celltables/localization/PNG/SVG generated, figurevisuallychecked. All108tests passlocal/remoteCPU/CUDA. Stopentiresyntheticprogram pendingLeadreview; no newmechanism/tuning/detector. Preparing finalcommit/push andremoteprojectmirror.

## 2026-09-12T15:08:52.838716+08:00 Research Lead closure acknowledged
Fetched and fast-forwarded44a1546/bd4cc6d. Lead accepted T012 as a valid negative result and accepted research_log/t012/SYNTHESIS.md as the bounded final evidence package. T001-T012 synthetic mechanism program CLOSED / AWAITING NEW RESEARCH SCOPE. No active experiment authorized; no T013 repair, lambda/tau tuning, synthetic objective/gate/residual/fusion/meta-training variant, or detector integration. Preserve all scoped positives and negative receipts unchanged. Existing completed runs already archived; no tests or experiments rerun for this coordination-only update. Heartbeat15min remains active, quiet without actionable change, awaiting explicitly new Lead scope that changes the scientific premise. Updating local/remote recovery status and acknowledging the decision in the mailbox.

## 2026-09-12T19:11:36.226672+08:00 T013 final text vocabulary pinned / background dataset download
Text r3run20260912-190708-tovd-t013-text-r3-a6000 exit0 at19:07:40+08.1124eligibleLVIS/79excluded,80hard/80unrelated,195/408/545tokens. FullpromptBERT emitted195/408/545tokenswithmaxsentenceposition3/3/7; no 512truncation or position-tableextension. AllmodeltensorsunchangedSHAedb3ae75e8e8d40a61f147eccdfcb5db6a51e4030302d9b8faa8a7db72da7b57. Threefocusedtests passlocal/remote. Completefinalvocab/vectors recovered; local/remoteSHA match983f7ed6(vocab),83b3e949(vectors). Committingactual finalnames/ranking/scores/vectors beforeanydetectorimageinference. Preliminaryr2retained as supersededaliasaudit.
Official8-rangeCOCOdownload20260912-190511-tovd-t013-coco-ranges-a6000 active. Annotationsfirst,thenval2017; partsretained,no duplicatewriter. PrimaryIDs,fullPLAN,realimageV0parity/smoke,rawcache runner,evaluation/bootstrap andscientificgates remainpending. NoAP/interactionclaim. Recovery inproject_state andt013/IMPLEMENTATION_NEXT.md, mirroredremote.15minheartbeatcontinuesauthorizedT013withoutuserconfirmation.

## 2026-09-12T20:02:47.194079+08:00 T013 native/HF prerequisite failed; waiting for Lead review

Updated 2026-09-12T20:02:47.194079+08:00. T013 engineering BLOCKED / AWAITING RESEARCH LEAD REVIEW after mandated native/HF V0 parity failure. Authoritative scope: c07ce16/afe9c13 plus 2c4dbf5/28b8718. T001–T012 remain CLOSED.

Run 20260912-195530-tovd-t013-native-parity exit 1 at 19:56:42+08: all three disjoint images exceed fixed 1e-4 box/score tolerance. Both model states unchanged, HF replay exact. Do not rerun, relax tolerances, launch primary or T014 without new Lead instructions. Evidence: research_log/t013/NATIVE_PARITY_REVIEW.md and original remote_runs receipt.

Token-matched vocabulary supersedes r3: V0/Vhard/Vrand195/408/408; Vhard and frozen embeddings/scores unchanged. Canonical LF SHA51554562b216dcad1c693efb7781362efbac55993bc5c10651e8845ec9931977. Nine focused local/remote tests pass; matched HF CUDA 45-condition smoke passes, which does not satisfy native/HF parity. Implementation92801da; statistics972c476.

1000 IDs committed42daa6e, accepted by Lead; smoke139/285/632 disjoint. Annotations verified. ACTIVE DATA RUN20260912-190511-tovd-t013-coco-ranges-a6000, last observed98/195 image archive parts. Single writer; retain chunks. Root /home/wenchang/asdasdsad/wjq/TOVD; assets shared/t013; isolated shared/t013/venv. Collect final archive/hash receipt when complete; no further inference. No primary AP/CI/gates exist. Full PLAN/primary cache runner/full bootstrap analysis/image hashes pending.

Heartbeat tovd every15min ACTIVE. Check new Lead instruction first; otherwise only finish existing data receipt. Quiet when unchanged. Detailed recovery: t013/IMPLEMENTATION_NEXT.md, NATIVE_PARITY_REVIEW.md, session_log.md. Generic workflow last-release metadata can name another project: use actual TOVD current resolved release and source hashes (documented in parity report).

## 2026-09-12T20:26:15.013866+08:00 T013-PARITY-B failed; stop for Lead review

Updated 2026-09-12T20:26:15.013866+08:00. T013 BLOCKED / AWAITING LEAD after T013-PARITY-B failed2/3images. Lead999b4b7/ddd24e7 says anyfailure rejects HF1024 harness for primary use and requires stopping. Codefreeze61918fa. Run20260912-202233-tovd-t013-parity-b exit1 at20:23:52+08; immutable release20260912-202152-tovd-t013-parity-b. Image139scoreerr.000431165>1e-4; image285classcounts differ (HF+1person,-1bear); image632PASS. No tolerance changes or retries. Allstatehashesunchanged/HFreplayexact. Evidence research_log/t013/PARITY_B_RESULTS.md and original rawrun.13focusedlocal/remote tests pass; savedraw matching exactlyreproduced locally.

Only currently executable work: monitor existingCOCOdownload20260912-190511-tovd-t013-coco-ranges-a6000; last150/195parts. Collectcompletedarchive/CRC/hashreceipt. Do not duplicatewriter. Root/home/wenchang/asdasdsad/wjq/TOVD, shared/t013assets, isolatedshared/t013/venv. Use explicitrunIDs and immutable releases; generic workflow state can refer tootherprojects.

Matchedvocabulary195/408/408 accepted, SHA51554562b216dcad1c693efb7781362efbac55993bc5c10651e8845ec9931977;1000IDs accepted42daa6e;smoke139/285/632disjoint. No primary outcomes or scientificGates1–4; fullPLAN/primarycache/fullbootstrap/imagehashmanifestpending. AllT001-T012remainclosed. NoT014 or alternate detector/matching changes withoutnewLead instruction. Heartbeat15minACTIVE; quietwhenunchanged.

## 2026-09-12T21:05:02.051520+08:00 Native30 primary dispatched after immutablefreeze

Updated 2026-09-12T21:05:02.051520+08:00. T013-NATIVE30 PRIMARY RUNNING. Exactrun20260912-210355-tovd-native30-primary; release20260912-210306-tovd-native30-primary-freeze; immutableprerequisitecommit6fec32243985ccc808123d851abf5f3dea10af99. Launched21:03:55+08afterfullfreezeonmain. CPUFP32/fourthreads officialnative256/preprocessing; 1000frozenimages×15cells, thenautomatic1000pairedimagebootstrap. NoHFprimary/parity, noTTA. No scientificprimarymetrics/completionyet.

Monitor ONLYthisexplicitrun withworkflow/config.autodl/config.json. Existingtmuxsessionautodl-20260912-210355-tovd-native30-primary. Root/home/wenchang/asdasdsad/wjq/TOVD; runartifacts/cache containsrawNPZs+cache_manifest.jsonl+run_receipt.json; analysis/results.json appearsafterallinference/bootstrapcomplete. Logcompleted_images showsprogress; do notread/interpretsubsetAPoradjustparameters. Estimate~24.9hCPUinferenceplusanalysis,raw~15.7GB. Do notstartduplicatejob orredeployintoimmutable release. Currentcodehasnoautomaticresume; ifobservedfailurepreservepartialoutputs anddiagnosebeforeanyrestart.

AllprerequisitesPASS: native45cellvalidity204646; cached45cell+10bootstrapengineering205428;17focusedlocal/remote tests; officialCOCOdownload/resume205852allZIPCRCpass/5000JPEGhashes;vocab195/255/255. Datadownloadfinished,noactivedownloader. NativevocabSHA3bb4a0ebada1f9da407ae6a94f1135798dba7117bd658a6ecba97b2ebfad0967. NativeexpectedstateSHAde1683cc0a3c35157ed5475169dae013cdaffe69f45651d6e3f5550ae96139e1. Exactcode/data/envhashesinPLAN.md/native30_freeze.json. AllT001-T012closed. Do notmodifyfrozenPLAN/IDs/vocab/gatesbasedonprimaryoutcomes. Whencompleteverifyrawhashes/recomputeaggregatefromrawasneeded, collectresults/CIs/gatesandreportLead; noT014untilLeaddecision. Heartbeat15minACTIVE,quietwhenunchanged.

## 2026-09-12T22:24:52.069905+08:00 Lead accepts native30 freeze and continuation

Fetched/fast-forwarded2e70b24. Lead accepts implementation/pre-primaryfreeze6fec322 anddispatch88668f7. Existing20260912-210355-tovd-native30-primary continues unchanged;48/1000imagesat4783.683s,tmuxalive,disk28GBfree. No scientificpartialmetricsinspected. Newexplicitfailureinstruction: preservepartialoutputs/exactfailureandreturntoLeadBEFOREanyrestart/resumedesign. No code/PLAN/vocab/metrics/gates changed; no testsrerun for thiscoordinationupdate. Completionrequires15000cells/rawhashes/sharedpixels/modelimmutability/deterministicanalysis andfulltables/CIs/Gates1,2,4/allGate3families. NoT014untilLeadreview.

## 2026-09-12T23:23:33.328103+08:00 T013-YW-P0 documentation package complete

Lead279ac4b added one hourly package while native primary continues. Created research/T013_YOLOWORLD_CONTINGENCY.md andresearch_log/t013_yoloworld/FEASIBILITY.md, plus officialsource/metadata/token-capacity receipts. OfficialHEAD4f70adbaacf5685bd9ec5bea85f1f91057f6fc0b has reproducedSyntaxError atdetectorline61; pinned unmodifiedofficialpredecessorb1b09f2f0340ca7dede69e10b7e909c469677fd9 (19modelfilesparse), MMYOLOgitlink4d97b3a06609dba94b8ec584be2f2029cfdb7519. Pre-outcomerule selectsV2.1-Sstage2/1280 amongunambiguousofficialcheckpoint/baseline mappings. S640officialcardlinkpointsX; actualS640metadata inventoriedbutassociationunresolved, nomodelsweep. Selectedweight305058902bytes SHA4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458; metadataonly,nopayload. CLIPtokenizer-only80/110/110names3–5tokens versus77context, noembeddingsorimageforward.

DocumentedexplicitMMDet3.0requiresMMCV<2.1 conflictwithguideexample, packageMMCV/MMCV-lite overlap andlegacyTorch/newtorchvisionconstraint. ProposedisolatedPython3.10/Torch2.1.2cu118/torchvision0.16.2/MMCV2.0.xsourcebuildrequireslaterauthorizationandverification; noinstall/patch. Runtimefeasibilitynotclaimedverified. Blankbackground andnativeNMS differfrominheritedT013contract; recordforLead, noauthorizedchanges. PreserveIDs/vocab/corruptions/metrics/bootstrap/Gates1,2,4 andfour-caseinterpretationmatrix.

NoGroundingpartialAP/interaction/CI/mechanismmetricsread; noYOLOinference; noinstall,weightdownload or activerunmodification. Onlypublicsource/metadata/tokenizer andread-onlyoperationalhealthinspected. LastGroundingcount80/1000; GPU1A6000free50598707200/50897289216bytes(snapshot,notreservation). Thispackageendswithdocuments/receiptcommit; waitnextLeadcycle, do not repeatP0 or begininstall/inference whileCURRENTpackageheadingpersists. Primary20260912-210355-tovd-native30-primarycontinuesunchanged.


## Latest handoff — 2026-09-13T00:07:46.077993+08:00: T013-YW-P1 BLOCKED

Lead c2f24e2 accepted P0; P1 source-only work delivered in 6694fcc3a94ef4bb310815770998b380854a4d6e. Read research_log/t013_yoloworld/PROTOCOL_FREEZE.md and protocol_freeze.json. Native postprocessing fixed (.001/30000/NMS .7/300,multi_label=True), but background count/placement is not uniquely established: demo one trailing space versus selected LVIS LoadText/no append; published selected COCO recipe not identified. Return to Lead and stop; no runtime variant selection, installation, weights, smoke or benchmark. Do not repeat P1 without new instructions. Grounding primary continues unchanged, last103/1000, tmux alive,27G free; no partial scientific metrics read.15-minute heartbeat unchanged. Existing failure/completion instructions remain authoritative.


## Latest handoff — 2026-09-13T01:17:03.176285+08:00: T013-YW-P2 VERIFIED / WAITING FOR LEAD

Lead ccec9fd resolves interaction background: one trailing U+0020; runtime81/111/111, blank80/110/110, semantic80/110/110 unchanged. P2 fixture/evidence commit 41ca40c3860e920714ecfb17273901916a635df8;7/7 standard-library tests pass. Read protocol_adapter_receipt.json and P2 amendment atop PROTOCOL_FREEZE.md. Background convention now resolved by Lead, superseding P1 interaction blocker; published-COCO fidelity remains unresolved separately. No model install/import/load/inference occurred. Do not repeat P2 or advance without new Lead scope. Primary20260912-210355-tovd-native30-primary continues unchanged; latest146/1000, tmux alive,26G free, no partial scientific metrics read.15-minute heartbeat and frozen-run failure/completion instructions remain unchanged.


## Latest handoff — 2026-09-13T02:29:23.792699+08:00: T013-OPS1 PASS / WAITING FOR LEAD

Lead bc041cb/784d7a1 accepts P2 and requests OPS1. Read PRIMARY_OPS_CHECK.md / primary_ops_receipt.json in research_log/t013. Evidence 67baf3892a41604f98543231692c54879a5ddfd2: one writer PID721181 bound to frozen release/commit;188 closed images×15=2820 paths; only next image in flight;10 deterministic images/150 opaque file hashes PASS; provenance PASS; fixed disk inequality PASS with2176675020-byte margin. End health189/1000, tmux alive, free26675806208 bytes. No prediction values or scientific metrics parsed; no run/YOLO changes. OPS1 delivered; do not repeat without new task. Continue immutable primary20260912-210355-tovd-native30-primary and15-minute heartbeat; failure/completion instructions unchanged; no YOLO setup/analysis/T014 until authorized.

## Latest handoff — 2026-09-13T03:13:32.6075109+08:00: T013-STAT1 PASS / WAITING FOR LEAD

Lead2109c88 accepts OPS1 and assigns independent synthetic arithmetic audit. Evidence 0cab4ca41a3885677d06b7a54c921f0ec66db6a7: read research_log/t013/SHADOW_ANALYSIS_AUDIT.md, shadow_analysis_receipt.json and audit source. Eight fixture groups PASS, max finite reference/frozen error0.0, exact booleans/indices/NaN. Mandatory signs/CI/gate boundaries/shared pairing/non-rescue/common-support checks pass. Optional COCO duplicate-copy check NOT RUN (local pycocotools absent); no installs. Initial audit negative-control coincidence retained and corrected in synthetic data only, no frozen discrepancy. End health214/1000 at03:11:26+08, tmux/writer721181 alive, free26200883200 bytes, no exit marker/analysis result. No primary scientific artifact opened or frozen/run/YOLO changes. Do not repeat STAT1; await next Lead package. Continue exact primary20260912-210355-tovd-native30-primary and15-minute heartbeat; existing failure/completion instructions remain unchanged.

## Latest handoff — 2026-09-13T04:29:19.7458292+08:00: T013-FIN1 PASS / WAITING FOR LEAD

Lead e22ee9b accepts STAT1. FIN1 evidence 8efe48506b6714eeef069e3c25dbceef510bdc05: read research_log/t013/PRIMARY_COMPLETION_VERIFIER.md and primary_completion_verifier_receipt.json.13tests PASS193.507s,full15000-cell synthetic positive plus23negative fixtures; deterministic,opaque byte-only. Existing remote completed smoke45/45files/48715584bytes/15pixelgroups PASS using projectPython3.12 after recorded systemPython hashlib.file_digest failure; no installs or code compatibility changes. New verifier NOT run on active primary; no scientific artifact opened or frozen/run/YOLO changes. End primary health258/1000 at04:27:45+08,tmux/writer721181 alive,free25408024576bytes,no exit/analysis result. Stop FIN1 and await Lead; do not repeat while heading persists. Continue exact primary20260912-210355-tovd-native30-primary and15-minute heartbeat. After primary completion, prepared byte-integrity command in verifier doc; existing failure/report/reproduction instructions remain authoritative. No restart/resume/YOLO/T014 authorization.

## Latest handoff — 2026-09-13T05:40:47.8448841+08:00: T013-REPRO1 PASS / WAITING FOR LEAD

Lead348b1df accepts FIN1. REPRO1 evidence 5fe57f7f4313ca9a94665d2320f7a06fefa99bee: read ANALYSIS_REPLAY_PREFLIGHT.md and analysis_replay_receipt.json. Exact frozen smoke-analysis A/B exit0 in19.1696/19.0555s; all4outputs/19arrays/JSONfields exact includingNaNs; fixed10x3draws,seed20260913. Scratchmutation rejected. Original-smoke output NOT COMPARED because analysis sourceSHAf472c3cc differsfromfrozen74cc73e7. All8pre-runbindings and existingpipfreeze match. No failures/installs/inference/frozenchanges. Remote outputs shared/t013/repro1/replay_a,replay_b,mutation_negative_control retained; helper is pinned smoke-only. End primary300/1000 at05:38:17+08,tmux/writer721181alive,free24575799296,noexit/analysisresult. Primary cache/scientific contents neveraccessed. Stop REPRO1/awaitLead, do not repeat whileheadingpersists. Continue exactprimary20260912-210355-tovd-native30-primary and15-minuteheartbeat; aftercompletionFIN1/reproduction/reportinstructions unchanged. NoYOLO/T014/restart/resume authorization.

## Latest handoff — 2026-09-13T07:11:24+08:00: T013-DEC1 PASS / WAITING FOR LEAD

Lead753facb accepts REPRO1. DEC1 evidence51881e3ca83ef0abafd0510965f32c19455c0025: read FINAL_DECISION_CONTRACT.md and final_decision_contract_receipt.json in research_log/t013. Dependency-free metadata-only disclosure/decision function,6tests/58fixturesPASS0.024s; all32 gate combinations+6integrity/replay non-PASS cases unchanged by hypotheticalYOLOPASS;15missing-field+3subsetfixturesrejected. All5frozen source/PLANbindingsmatch. Required complete15-cell table/CI/interactions/3diagnosticfamilies/common-support/provenance; explicitLead3/4, no automatic research acceptance. Undefined margins/CI remain disclosed, no newthresholds or frozen changes. No primary predictions/scientific contents opened. End primary356/1000 at07:11:24+08,tmux/writer721181alive,free23537688576,noexit/analysisresult. StopDEC1/awaitLead; do not repeat whileheadingpersists. Continue immutableprimary20260912-210355-tovd-native30-primary and15-minuteheartbeat. Existing completion FIN1/full-replay/report and failure-return-to-Lead procedures unchanged; noYOLO/T014/restart/resume authorization.

## Latest handoff — 2026-09-13T08:10:43+08:00: T013-G4A1 PREOUTCOME_HISTORY_CLEAN / WAITING FOR LEAD

Lead9b59ab9/cca9af2 accepts DEC1. G4A1 evidence6a96f8870f0e88087d64341ed37dabf05df49f84; task-startHEADcca9af23452870d1a12ba1ab6a78ebe683e49cd1. Read GATE4_PREOUTCOME_HISTORY_AUDIT.md and gate4_preoutcome_history_receipt.json in research_log/t013.13mechanicalchecksPASS:17protectedpaths byte-identical/nointermediateedits,59postfreezecommits/97classifiedpaths(4coordination,8provenance/log,25preflight,60YOLOprep),exactfreeze->dispatch ancestry/binding,retainednegativeparity. No committed evidence of duplicateprimary/restart/retune/partialoutcomeuse/YOLOscience; Git/log scope only. Initial audithelper miscounted prefreeze --smoke-only run asprimary, preserved initialreceipt and minimally corrected classification; no frozen/history/run repair. FinalGate4stillPENDINGcompletion+Leadreview. Endprimary392/1000 at08:10:43+08,tmux/writer721181alive,free22873034752,noexit/analysisresult. No primaryprediction/scientificcontents opened. StopG4A1/awaitLead; do not repeat heading. Continue immutableprimary20260912-210355-tovd-native30-primary and15-minuteheartbeat; establishedcompletionFIN1/fullreplay/report andfailure-return-to-Lead rules unchanged. NoYOLO/T014/restart/resume authorization.
