# T006 progress

## 2026-09-12 — Task received
- Lead accepts T005 and assigns controlled C2 meta-training at a1a585c/6dafb0f.
- Baseline suite reproduced before edits; result recorded below.
- Plan/config fixed before aggregate outcomes: original400x4 budget,3seeds, piecewise eta semantics, selector probes and exact5rules.
- No T006 training/results yet.
- Baseline python -m pytest -q: 70 passed in 14.77s.

## Gradient increment: observed test-fixture correction
Initial boundary-coverage test assumed the first20 untrained seed7 probes at epsilon .1 crossed a selector boundary; none did (12 passed,1 failed). This was a test-fixture assumption, not a model failure. A dedicated training-episode index2, epsilon1.0 fixture crosses .025 -> .0125 and tests explicit boundary reporting. The study's preregistered epsilons [1e-5,1e-3,.01,.1] and20episode sampling remain unchanged; zero empirical switch fractions will be reported as measured.

## Implementation and local verification
- Alias/piecewise-gradient + previous controller tests: 13 passed in 8.15s after the documented boundary-fixture correction.
- Training telemetry/replay/save-load plus original runner tests: 3 passed in 11.57s.
- Complete tiny experiment/control replay/rule tests: 2 passed in 15.15s.
- Full local suite: 75 passed in 20.67s.
- local_initial_meta_gradient.json: all60 epsilon1e-5 probes stable, max FD absolute error6.6941126253e-11, zero disagreements; gradient requirement passes for all3seeds. Epsilon .1 crosses1/60 boundaries; larger stable probes may have finite-step truncation error and are not graded as primary FD failures.
- Server NVML warning observed: nvidia-smi driver/library mismatch (kernel580.173.02, installedlibrary580.178.04). PyTorch2.4.0+cu121 detects2GPUs and successfully computes torch.ones on cuda:1. No system driver modification/restart attempted. Actual CPU/CUDA tests will precede training.
- PyTorch driver-path memory query succeeds: GPU1 free50,598,707,200/50,897,289,216bytes; GPU0 free47,021,686,784. GPU1 retained for T006.
