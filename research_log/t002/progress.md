# T002 progress

## 2026-09-12 02:23 +08:00 — Started from research instruction de51d5b
- T001 accepted by Research Lead; T002 active.
- Reproduced unchanged baseline: python -m pytest -q -> 10 passed in 10.90s.
- Reuse/experiment plan recorded in PLAN.md before headline experiments.
- Increment 1: structured world and held-out episode generator added. Focused generator tests passed (4/4): split isolation, label remapping, deterministic views, shuffled order, hardness, fixed scene, unrelated vocabulary.
- Next increment: reuse T001 via a narrow target-selection extension and add matched model paths.

## 2026-09-12 02:25:50 +08:00 — Increment 2
- Extracted T001 inner_targets hook without changing default math; B2 uses raw X target.
- Added five matched model paths; B1 receives both X-derived semantic context and T without extra parameters.
- Fixed W0 remains differentiable for inner gradients but is excluded from outer Adam.
- Focused combined baseline/model/generator suite passed; next shared runner and evaluator.

## 2026-09-12 02:31:02 +08:00 — Runner verified
- Increment 2 combined suite: 21 passed in 11.67s.
- Increment 3 focused mini end-to-end runner/checkpoint/known-metric tests: 2 passed in 12.44s.
- Final full local regression: 23 passed (full command output captured in session).
- No headline evaluation used during implementation; only 2-step tiny unit fixtures.
- Exact matched protocol saved in config.json; both A6000 GPUs idle at dispatch inspection.
- Next: commit/push tested code, deploy, run CPU+CUDA regression then fixed 3-seed comparison.
