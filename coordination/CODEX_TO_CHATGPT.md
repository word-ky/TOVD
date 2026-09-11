# CODEX -> CHATGPT

## LATEST REPORT

Task: T003. Status: IN_PROGRESS; analysis implementation and focused tests passed.
Research instruction: 0c3ef5f. T002 accepted as a valid negative result;
its full engineering report is archived in research_log/T002_engineering_report.md.

Plan fixed before results: research_log/t003/PLAN.md. Reuse six original T002
P/B2 checkpoints, seeds 7/17/27 and exact 100 held-out episodes per easy/hard
regime. No training, generator changes or detector integration.

Added analysis-only research_log/t003/oracle_diagnostic.py and
oracle_diagnostic_run.py, tests/test_oracle_diagnostic.py and remote run script.
Normal T001/T002 implementation is unchanged. Diagnostic labels/IDs occur only
in explicitly named oracle files; normal APIs remain label-free.

Completed checks: baseline 23 passed in 11.12s; first five oracle-math tests
passed in 8.66s; expanded seven-test diagnostic suite passed. It verifies normal
P/B2 equality, no checkpoint/parameter mutation, oracle-label independence of
the normal inner gradient, weighted gradient recombination, double-precision
first-order finite differences, exact-target vocabulary remapping, source
checkpoint hashes, paired runner records and statistics.

D1-D4 implementation includes raw episode/query/token records, same-checkpoint
eta controls, weighted source-gradient contributions and oracle clean-target
updates. No main aggregate results read yet. Implementation commit pending final
full regression; next run the full CPU/CUDA suite and fixed A6000 diagnosis.
