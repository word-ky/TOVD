2026-09-12 11:37 +08: fetched45f6045, T009 accepted and T010 assigned. Nine checkpoint hashes verified; source code/old IDs/new namespaces locked in t010/sources.json. Baseline13tests passed16.59s. Preregistered1800calibration/3600validation and actual-threshold commit before validation.
2026-09-12 11:44 +08: scalar tests2passed.08s; model/two-phase/gates focused5passed18.29s; full95passed40.01s. Both A6000 GPUs idle, useGPU1. No fresh outcomes generated/read; commit implementation then deploy calibration-only runner.

## 2026-09-12 11:44 +08 T010 calibration dispatch
Tested1b60f217f67c283df1e49f73f4bb4f2b64e03955; release20260912-114356-tovd-t010-cal.
Run20260912-114426-tovd-t010-cal-a6000 on physicalGPU1. RemoteCPU/CUDA tests then1800 base calibration episodes only.
Local95tests passed40.01s. No validation outcomes yet; fetch/commit actual thresholds before validation.
