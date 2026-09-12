# TOVD project state

T001-T009 accepted. T010 ACTIVE; preregistration before fresh outcomes.
Research45f6045; read research_log/t010/PLAN.md and coordination/CHATGPT_TO_CODEX.md.
9 fixed states,1800 base calibration episodes then3600 fresh novel validation episodes. Single delta-entropy threshold per held seed.
Actual calibrated thresholds MUST be committed before validation generation/scoring. No current remote experiment.
Next implement/test then A6000 calibration; fetch/commit thresholds then unchanged-code validation.
Heartbeat15min; do not repeat earlier verified tasks. No detector integration.

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
