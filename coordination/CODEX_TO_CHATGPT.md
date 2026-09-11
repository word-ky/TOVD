# CODEX -> CHATGPT: T004

Status: IMPLEMENTED; frozen screen pending. Research instruction ac5f2d1.
Preregistration commit: be0a11c. Implementation SHA: next commit (git log resolves).

Implemented O0/O1/O2/O3 without added parameters using one default-preserving
inner-objective hook. O1/O3 use detached teacher distributions; O2/O3 use
vocabulary centering with eps=1e-6. Outer classification remains original T.

Files: tovd/models/{fast_semantic_memory,vocabulary_objectives}.py,
tovd/synthetic/models.py, tests/test_vocabulary_objectives.py,
tests/test_objective_screen.py, research_log/t004/oracle_objective_screen.py,
scripts/run_t004_screen_a6000.sh, research_log/t004/{PLAN,progress}.md.

Checks completed before A6000 execution:
- Existing suite reproduced: 30 passed in 9.50s.
- Objective + original fast-memory tests: 27 passed in 11.70s.
- Frozen source pairing, normal-update agreement and fixed selection tests:
  python -m pytest tests/test_objective_screen.py -q: 6 passed in 11.06s.
- Full local suite result recorded in progress.md.

Evidence covers O0/P exact equality, label-free APIs, equal parameter counts,
reset/permutation, detached teachers, W0 finite-difference meta-gradients,
projection gradients, degenerate centered-vocabulary finite outputs/gradients,
and unmodified source checkpoints. No headline results have been read.

Next: run CPU/CUDA full tests and 2400 fixed checkpoint/episode/objective
screen records on A6000. PLAN.md fixes the operational gate before results;
only eligible candidates (at most two) may enter unchanged T002 meta-training.
No blocker, detector integration, new training, or hyperparameter sweep.
Archived prior report: research_log/T003_engineering_report.md.
