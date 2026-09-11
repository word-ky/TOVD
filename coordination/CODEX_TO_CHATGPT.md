# CODEX -> CHATGPT

## LATEST REPORT

**Task ID:** T001
**Run ID:** local-feasibility-seed7; A6000 verification pending
**Status:** IMPLEMENTED; local verification passed
**Commit SHA:** This report accompanies the implementation commit; its resolved SHA will be recorded with remote evidence in the next report.

### Files changed
- `.gitignore`, `pyproject.toml`, `README.md`
- `tovd/__init__.py`, `tovd/models/__init__.py`, `tovd/models/fast_semantic_memory.py`
- `tests/test_fast_semantic_memory.py`
- `scripts/__init__.py`, `scripts/demo_fast_semantic_memory.py`, `scripts/run_a6000.sh`
- `coordination/CODEX_TO_CHATGPT.md`
- `research_log/session_log.md`, `research_log/REMOTE.md`, `research_log/demo_cpu_initial.json`

### Implementation and design choices
Exact unnormalized K/T attention target, separate bias-free key/query projections,
two-layer gated MLP (hidden 2D), cosine loss, one SGD step with eta=0.05 and tau=1.
Each image adapts all six MLP parameter tensors independently from W0. Functional
updates do not mutate parameters or accumulate .grad. Training retains the full
higher-order graph, including the target's dependence on K; evaluation supports
no_grad while computing the inner gradient locally. Static control is exactly
F_W0(P_q(Q)), independent of image/vocabulary context.

### Commands and evidence
```text
python -m pytest -q
# Initial run: 10 passed in 13.89s
python -m scripts.demo_fast_semantic_memory --device cpu --revision working-tree-T001 --output research_log/demo_cpu_initial.json
```

Windows Python 3.12.7, torch 2.13.0+cpu, pytest 9.1.1. Seed 7, float64,
B=2/N=6/C=5/M=3/D=8; synthetic Gaussian inputs; no dataset split or checkpoint.

- Inner loss: [0.6372584282786371, 0.8606449089652767] -> [0.5119405211667978, 0.7631187027257509].
- Inner gradient norm: [1.631945186871967, 1.4297677506717636].
- Update norm: [0.08159725934359835, 0.0714883875335882].
- T versus -T: target delta 8.998322862629163; fast-state delta 0.19618724286063557; query-output delta 0.34712771307653745.
- Reset state/output delta: both exactly 0 after an intervening different episode.
- Outer gradients: every W0 tensor and both projections finite/nonzero; key projection norm 0.00347418247465095, query projection 0.012572703197751287.
- Full-update directional finite differences passed on W0 output weight and P_k.
- Finiteness, no-label API, static path, batch isolation and vocabulary permutation tests passed.

### Blockers / uncertainties
No implementation blocker. A6000 base interpreter lacked pytest; a dedicated
TOVD environment was created and pytest 9.1.1 installed there. Remote verification
is next. User authorized remote experiments and a 15-minute heartbeat (tovd,
ACTIVE). No detection performance, semantic usefulness, or meta-training gain
has been demonstrated by these synthetic tests.

### Recommended next action
Wait for A6000 verification before research review. The engineering agent does
not select T002 or mark research acceptance.

## RUN HISTORY
- Initial local mechanism suite: 10/10 passed, demo completed; code and receipts prepared for the first implementation commit and A6000 deployment.
