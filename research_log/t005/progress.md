# T005 progress

## 2026-09-12 05:29 +08 — Task received
- T004 accepted by research lead, new T005 instructions c7b4954 / 246994e fetched.
- Baseline 53 tests reproduced (11.70s).
- PLAN.md fixes controller epsilon/guard, exact research rules and runtime measurement before aggregate results.
- No implementation or T005 remote run yet.

## Implementation milestone
- Minimal select_update hook preserves O0 and fixed O1 defaults. Isolated C1/C2 controllers add no parameters.
- C1 norm matching, direction preservation, zero/near-zero/nonfinite guard, finite-difference W0 and projection gradients tested.
- C2 fixed-sequence first acceptance/rejection, label-free choice, reset/vocabulary/determinism tested.
- Controller + existing objective tests: 28 passed in 10.57s.
- Frozen runner tests: 6 passed in 14.56s; C0/O0 fixture drift zero, hashes retained, label changes do not change controller selection.
- GPU 0 is running another project (taisp-t004-coco200); GPU 1 idle (18 MiB, 0%). Use CUDA_VISIBLE_DEVICES=1 for T005, leaving other job untouched.
- Full local suite: python -m pytest -q -> 70 passed in 24.47s.

## A6000 dispatch — 2026-09-12 05:38 +08
Tested SHA f2b9722ae8a1ad68e0e529488e68f88c170125de; release 20260912-053814-tovd-t005.
Run 20260912-053826-tovd-t005-a6000, scripts/run_t005_a6000.sh, physical GPU 1.
No deployment failure; no outer training. Fixed frozen sources/episodes.
