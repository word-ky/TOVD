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

## 2026-09-12 08:39 +08 remote tests
A6000 CPU79 passed7.07s (2 protobuf deprecation warnings); CUDA79 passed20.47s (same2 plus existingNVMLwarning).
Fixed six-run continuation underway; no aggregate read. Report renderer prepared locally only; runtime unchanged e88ad88.

## 2026-09-12 08:42 +08 six training runs complete
All six checkpoints completed400steps;0 nonfinite training steps and0 Armijo violations.
Seconds: W1 seed7/17/27=45.286852/47.271170/47.485038; W2=51.458510/51.449494/51.323563.
Fixed saved-checkpoint evaluation underway; no intermediate checkpoint selection or runtime changes.

## 2026-09-12 08:47 +08 experiment completed
Run20260912-083417-tovd-t007-a6000 exit0 at08:47:19+08. Rules1/2/5PASS;3/4/6FAIL.
W2hard43.54167% improvesownW0 +4.625pp/NLL-.080269; T005accuracy -2.70833pp despiteNLL-.007433.
W2versusW1+C2:accuracy -1.83333pp,NLL+.007603. Strong-control NLL branch passes againstB0.
Easyseed27 harmed7.625pp/NLL+.114365, despiteaggregatebenefit. No detector/T008.
Allruntime/provenance/normal-output checks exact; fetching full original receipts.

## 2026-09-12 T007 completion
Run20260912-083417-tovd-t007-a6000 exit0 at08:47:19+08;79CPU/CUDA tests each.
Six fixed400x4 runs completed. Rules1/2/5PASS;3/4/6FAIL; no detector/T008.
W2hard43.54167% versusW1+C2 45.375% andT00546.25%; W2easyseed27 -7.625pp.
W1easy also harmed6.79167pp; retain fixed-T005 reference, flag checkpoint/seed dependence.
105 rawrunfiles,6final+30trajectory checkpoints and1200oracle episodes retained locally/remotely.
Normal/historical/source/step0 checks exact. Report/curves inresearch_log/t007.
Renderer OpenMP conflict fixed by removing unnecessary torch import; experimental code unchanged e88ad88.
No activeTOVD run; awaitlead, heartbeatactive.

## 2026-09-12 final publication synchronization
Final evidence committed4315ba35f0b89bbfa92958cf75a8bcd6a22f9eee. Initial push was rejected because lead concurrently committed interim implementation acceptance a513576/09f5456.
Fetched/reviewed and merged those mailbox/review-log updates without conflicts or runtime changes. No new task assigned.
