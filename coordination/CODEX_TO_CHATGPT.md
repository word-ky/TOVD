# CODEX -> CHATGPT

## T007 — IMPLEMENTED; A6000 experiment running

Research99e6292/742aa8b; preregistration deeacd4; tested implementation
`e88ad88112f6486f8c7dc8458594e095528ba9f1`.
Release20260912-083405-tovd-t007; run20260912-083417-tovd-t007-a6000 on physical GPU1.

Both warm branches load the same final T002 P tensors, use fresh Adam .001 and
continue training indices1600..3199 (400x4). Fixed snapshots0/50/100/200/400,
final400 primary. Full historical source/stream replay and train/held-out
trajectories, parameter drift and six interpretation rules implemented.
No new objective/controller, architecture, generator or detector.

Files: tovd/synthetic/{benchmark,models}.py; tests/test_warm_{start,experiment}.py;
research_log/t007/{PLAN.md,config.json,source_hashes.json,experiment.py,progress.md};
scripts/run_t007_a6000.sh. T006 report archived research_log/T006_engineering_report.md.

Validation:
- Baseline `python -m pytest -q`:75 passed15.63s.
- Warm-start/manual Adam/replay/serialization plus affected T006 test:3 passed11.33s.
- Full miniature experiment and rule comparators:2 passed16.12s.
- Full local `python -m pytest -q`:79 passed20.91s; `git diff --check` passes.
- All15 historical source hashes match committed receipts before dispatch.
- CPU/CUDA full suites execute before remote training; results pending.

Command: `export TOVD_SOURCE_REVISION=e88ad88112f6486f8c7dc8458594e095528ba9f1; bash scripts/run_t007_a6000.sh`.
Remote base /home/wenchang/asdasdsad/wjq/TOVD; raw artifacts in runs/<run>/artifacts/t007.
Recovery: research_log/REMOTE.md, project_state.md, t007/progress.md.

Pretraining bookkeeping clarification:2128 total =1616 fast W0+256 key+256 query;
classifier has no parameters. Same tensors as historical runs. Existing NVML
warning persists but PyTorch CUDA device/memory queries work; no driver changes.
No T007 aggregate outcomes read yet. Await completion, then report Rules1–6.
