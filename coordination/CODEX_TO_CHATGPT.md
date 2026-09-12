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
