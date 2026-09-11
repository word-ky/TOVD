# T004 progress

## 2026-09-12 — Preregistered plan
- Research commits 07bd12c/ac5f2d1 accept T003 and assign O1/O2/O3 redesign.
- Existing 30-test suite reproduced before edits.
- PLAN.md records exact objectives, finite-centering epsilon, numeric operational Phase-1 gate and conditional selection/success rules before aggregate results.
- No screen results or new outer training yet.

## 2026-09-12 — Objective and screen implementation
- Minimal default-preserving objective hook plus O0-O3 methods implemented.
- Objective/old-memory tests: 27 passed in 11.70s.
- Frozen-screen tests: 6 passed in 11.06s; normal update agreement, source pairing/hash preservation and preregistered gate/ranking checked.
- A6000 GPUs 0/1 idle (15 MiB each, 0% utilization) before scheduling.
- Full local regression: python -m pytest -q -> 53 passed in 13.22s.
