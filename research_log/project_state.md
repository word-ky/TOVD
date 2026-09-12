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
