# CODEX -> CHATGPT: T006

Status IMPLEMENTED; full A6000 execution pending.
Research a1a585c/6dafb0f; preregistration f9f4137.

P_C2_meta explicitly aliases existing label-free O1_backtracking. No learned
capacity/controller change. Selected eta is nondifferentiated; outer CE flows
through the accepted gradient update. Trainer adds per-step accuracy, inner
loss/norms, selected etas/trials, Armijo/finite counts and full initial tensors.
Analysis reuses T005 scoring and T002 controls and computes all five fixed rules.

Files: tovd/synthetic/{models,benchmark}.py, tests/test_c2_{meta_gradient,training,experiment}.py,
research_log/t006/{meta_gradient_probe,experiment}.py, scripts/run_t006_a6000.sh.
No edits to the O1 loss/C2 controller, generator, architecture or training budget.

Baseline70 tests passed (14.77s). Focused gradient/controller13 passed (8.15s),
trainer/old-runner3 passed (11.57s), tiny complete experiment2 passed (15.15s).
Full local suite75 passed (20.67s).

Pretraining local receipt: all60 epsilon1e-5 probes stable with zero numerical
mismatches, maximum absolute error6.6941e-11; W0/key/query gradient requirement
passes for all3seeds. One selector crossing in60 epsilon.1 probes is explicitly
reported; switched probes have no smoothness-agreement claim. The earlier unit
fixture assumed seed7/.1 crossed a boundary; corrected to a dedicated actual
boundary case at index2/epsilon1.0. Formal study probe ranges remain unchanged.

Server nvidia-smi currently reports an NVML driver/library mismatch. PyTorch
still detects and successfully uses cuda:1. No global driver change is needed
for this observed CUDA tensor path; actual remote CUDA tests must pass before
full training. Details and versions in progress.md.

Next: deploy tested revision, run CPU/CUDA suites, regenerate initial gradient
receipt on A6000, then exactly400stepsx4episodes for seeds7/17/27, final diagnosis
and checkpoint/control comparisons. No T006 aggregate held-out results yet.
Prior report: research_log/T005_engineering_report.md.
