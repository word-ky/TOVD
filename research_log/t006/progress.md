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

## 2026-09-12 06:51 +08 — A6000 dispatched
Tested SHA65299db5f1127407f856872b732f2b2b7051383e; release20260912-065052-tovd-t006.
Run20260912-065105-tovd-t006-a6000 on physicalGPU1. CPU/CUDA suites and initial-gradient requirement precede three-seed400x4 training.
No deployment failure. NVML mismatch remains an observed system warning; PyTorch device/memory/tensor path works.

## 2026-09-12 — T006 completed
- Run20260912-065105-tovd-t006-a6000 exit0 at06:56:11+08, physicalGPU1;3seeds completed400x4 exactly.
- Remote CPU75/5.36s, CUDA75/13.14s; local75/20.67s. CPU2protobufwarnings; CUDAplusNVMLwarning. No execution failure.
- Initial/final primary gradientprobes60/60stable each; maxerrors7.55857e-11/3.08320e-11. One initial larger-epsilon boundary, zero final in fixedsample; no global smoothness claim.
- Twelve historical controlcheckpoints matchhashes;2400control episodes reproduceexactly;600newpaired diagnoses and4800query changes. Initialtensors andnormalruntime/W0 scores matchexactly.
- Rules1,2,4,5pass;Rule3fails. Hard ownW0 29.91667% ->adapted34.625%, NLL1.469848 ->1.358451; still10ppbelowB2 andworseNLL.
- Relativefastpath gains survive inall3seeds, butabsolutecontrolcompetitivenessfails. Easyseed27mildharm+.069829NLL/-1.625pp retained (belowmajorflag).
- Trainingcurves/rawCSV plusPNG/SVG generated andvisually checked. Checkpoints, probes, controls, artifacts/results/report persisted.
- Default resultdownloadtimedout; existingworkflowlegacySCPretry succeeded. No remote systemdriverrepair or otherproject changes.
- TaskVERIFIED;recommendstop/reframecurrentformulationbefore detector. NoT007/tuning/newexperiment inferred.
- Artifact formatting: generatedSVG trailing spaces failed diff-check; normalization then exposed WindowsGBK default-decoding. ExplicitUTF8 read/write fixed it; formatter reran successfully. No model/results change.
