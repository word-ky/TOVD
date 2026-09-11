# TOVD project state

T001-T005 accepted. T006 VERIFIED; Research Lead review pending.
Research a1a585c/6dafb0f; preregistration f9f4137; tested code65299db5f1127407f856872b732f2b2b7051383e.
Run20260912-065105-tovd-t006-a6000 exited0 at2026-09-12 06:56:11+08 on A6000 GPU1.
Three seeds completed400x4; local/CPU/CUDA full75 tests each. All control/initial-state/normal-output equality errors0.
Rules1,2,4,5 PASS; Rule3 FAIL. Hard adapted34.625% versus ownW0 29.91667% (NLL -.111397), but B2 44.625%.
Fast-path value survives; absolute control competitiveness fails. Recommend stop/reframe currentmeta-training before detector.
No T007, detector, newobjective or tuning. No active TOVD run remains.
Read coordination/CODEX_TO_CHATGPT.md and research_log/t006/{PLAN,RESULTS,progress}.md.
Complete3checkpoints, trainingcurves, controls, meta-gradient/boundary receipts under research_log/remote_runs and remote runs.
NVML mismatch observed but PyTorch CUDAworks; leave systemdrivers unchanged. One download transport retry recovered.
Heartbeat remains active every15min. Do not rerun unchanged ACTIVE T006; await explicit research task.
