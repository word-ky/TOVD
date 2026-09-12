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
