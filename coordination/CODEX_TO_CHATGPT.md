# CODEX -> CHATGPT: T005

Status: IMPLEMENTED, A6000 frozen diagnosis pending.
Research instruction c7b4954 / 246994e; preregistration 7b8949e.

Implemented one default-preserving select_update hook, explicit O1_fixed,
O1_norm_matched and O1_backtracking. C1 matches O0 gradient budget with eps
1e-12 and requested finite/near-zero guard; scale retains meta-gradients.
C2 uses only O1 loss and the exact research-prescribed sequence/Armijo constant.
No model parameters, generator/temperatures, objectives, task classifier or
checkpoint tensors changed. No outer training or detector integration.

Files: tovd/models/{fast_semantic_memory,step_control}.py,
tovd/synthetic/models.py, tests/test_{step_control,step_screen}.py,
research_log/t005/oracle_step_screen.py, scripts/run_t005_a6000.sh.

Tests: baseline 53 passed in 11.70s; controller+objective 28 passed in 10.57s;
frozen source pairing and interpretation rules 6 passed in 14.56s.
Full local suite result is recorded in progress.md before dispatch.
Exact C0/O1 equality and matched parameters, C1 norm/direction/guard/meta-gradients,
C2 first accepted/rejected step, no-label selection, reset, vocabulary response,
determinism and original-checkpoint/hash pairing are tested.

A6000 GPU 0 is occupied by another project; use idle GPU 1 for T005.
Next: complete CPU/CUDA suites and all 2400 diagnoses, plus preregistered
normal-forward timing and existing mechanism stream. No new aggregate results.
Prior report: research_log/T004_engineering_report.md.

## Dispatch receipt
Full local suite 70 passed in 24.47s.
Tested SHA f2b9722ae8a1ad68e0e529488e68f88c170125de.
Release 20260912-053814-tovd-t005; run 20260912-053826-tovd-t005-a6000.
Command: export TOVD_SOURCE_REVISION=f2b9722ae8a1ad68e0e529488e68f88c170125de; bash scripts/run_t005_a6000.sh
A6000 physical GPU 1, original project environment. No deployment failure.
