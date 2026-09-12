# T008 progress

## 2026-09-12 received
Research2008520/c6593b7 accepts T007 and requests frozen-state label-free audit.
Baseline79 tests passed37.15s. Preregistered c163c78 before correlations.
33 file hashes verified against committed receipts;6600 raw rows planned,5400
unique-state primary rows to avoid triple weighting original/W1step0/W2step0.
14 scalar features; pooled LOSO thresholds.70 mean/.65 each, within-easy.65/.60,
same pooled-training orientation across folds/branches. No gate fitting/training.

## Feature increment
Initial test fixture omitted required SemanticWorld(WorldConfig()) argument;
2 tests failed before extraction. Fixed fixture only;2 passed8.37s.
Pre-only path does not select a candidate. Oracle/changed labels/IDs do not affect
features or model states. Separate dependency-free schema for statistics/figures.

## Statistics increment
5 focused statistics/feature tests passed12.02s. Average ties, undefined cases,
LOSO training orientation and regime-confound rejection verified.
No experimental feature/outcome correlations read; only artificial unit fixtures.

## Full local validation
Artificial-source end-to-end + statistics:4 passed13.92s; full suite85 passed25.12s.
Both A6000 GPUs idle; use physicalGPU1. ExistingNVMLwarning only; PyTorchCUDAworks.
No runtime model files changed, no training or controller.

## 2026-09-12 10:13 +08 T008 dispatch
Run20260912-101332-tovd-t008-a6000 active onGPU1; release20260912-101316-tovd-t008.
Tested153ac30d00753b43a56ce2e226068b0c35039d70; local85tests pass.
33 fixedstates/6600raw episodes; no training/controller; remoteCPU/CUDA tests precede extraction.
