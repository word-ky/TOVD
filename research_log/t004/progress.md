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

## 2026-09-12 04:32 +08 — Phase 1 dispatched
Tested SHA 9afe8df54c22d0a20b284d6b4b20aaab5b36ea9a; release 20260912-043213-tovd-t004-screen.
Run 20260912-043224-tovd-t004-screen-a6000 executes scripts/run_t004_screen_a6000.sh.
Initial deployment 20260912-043206-tovd-t004-screen failed on SSH connection closed, exit 255; retry succeeded without code changes. No experiment was started by that failed deployment.

## 2026-09-12 — Phase 1 completed and screened
- Run 20260912-043224-tovd-t004-screen-a6000 exited 0 at 04:34:08 +08.
- A6000 CPU 53 tests / 3.47s; CUDA 53 tests / 6.81s; 2 protobuf deprecation warnings per suite.
- 2400 objective/episode diagnoses, 19200 query outcomes. All finite; O0 drift and normal output error exactly 0. Three original P hashes match.
- Fixed gate selected NONE: O1/O3 direction improves but easy regression disqualifies; O2 hard alignment/NLL worsen. No Phase 2.
- Full raw receipts fetched; RESULTS.md, frozen_screen.json, selection.json, verification.json and report written.
- Added explicit changed-vocabulary state and exact reset-state assertions after the screen; focused local objective suite 17 passed in 8.80s. Production/screen code unchanged.
- Unit fixture receipt records nonzero vocabulary sensitivity/W0 meta-gradients and exact reset for O1/O2/O3; not benchmark or trained evidence.
- Recommendation: stop/reframe fixed-step branch; await Research Lead. No T005/detector work.
