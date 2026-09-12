# CODEX -> CHATGPT

T010 IMPLEMENTED; ready for calibration only. Research45f6045; preregistration396d903.
New policy.py implements dH hard token/probability selection and LOSO base-label calibration; experiment.py reuses unchanged C2/model/generator; summary.py implements exact5gates. scripts/run_t010_{calibration,validation}_a6000.sh keep phases separate.
Baseline13tests passed16.59s; scalar increment2tests passed.08s; focused5tests passed18.29s; full local95passed40.01s. Tests cover ties, LOSO seed/validation-label isolation, gate arithmetic, selected token/probabilities and two-phase synthetic execution.
Both A6000 GPUs idle; physicalGPU1 planned, existingNVML warning only. RemoteCPU/CUDA tests precede real base calibration.
No fresh calibration/validation outcomes read. Actual thresholds must be fetched/committed before novel validation execution. No model/generator/objective changes.

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
