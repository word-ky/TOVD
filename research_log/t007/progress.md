# T007 progress

## 2026-09-12 08:26 +08 — accepted task
Research 99e6292/742aa8b; preregistration deeacd4. Baseline75 passed in15.63s.
Reused project-owned trainer/model, T005 oracle/timing, T004 aggregation and T006 rule helpers.

## 2026-09-12 — implementation increments
1. Optional initial tensors/episode offset/fixed snapshots in existing train_model;
   P_O0_resume/P_C2_warm aliases and telemetry. Independent manual Adam continuation,
   byte-equal step0, replay, save/load and source immutability:3 focused tests passed11.33s.
2. Task-local orchestration/historical replay/trajectory/drift/six rules:2 tests passed16.12s.
   Tiny end-to-end run includes both warm branches and all required historical paths.
15 source hashes match committed T006 verification before training.
Both A6000 GPUs idle; continue using physical GPU1. Existing NVML warning persists,
PyTorch CUDA device/memory queries work. No global environment/driver changes.
An exploratory read of absent tests/conftest.py failed; no such fixture required.
Preregistration log entry literal newline formatting corrected; no scientific change.
Full local suite79 passed20.91s; git diff --check passed.
Pre-dispatch parameter inventory clarified PLAN.md:1616 fast +256 key +256 query
=2128 total parameters. No tensor shape/capacity changed from T002/T006.

## 2026-09-12 08:34 +08 T007 dispatch
Tested e88ad88112f6486f8c7dc8458594e095528ba9f1; release20260912-083405-tovd-t007.
Run20260912-083417-tovd-t007-a6000 active on physicalGPU1;79 local tests pass.
Six fixed400x4 runs follow remote CPU/CUDA suites; no T007 aggregate read.
