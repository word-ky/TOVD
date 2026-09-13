# T013-OPS5 — project-boundary accounting

Status: AWAITING_SECOND_HEARTBEAT_SNAPSHOT; no attribution conclusion yet.
Task-start HEAD b3b27c6258bda129968cac10e74a8080fed392a9 accepts OPS4.

Minimal OPS5 variant of the tested OPS4 metadata parser/collector, with project
total replacing cache total. Accepted OPS2 health_guard and fixed primary
bindings are imported unchanged. No previous helper or scientific file changed.
Raw command/exit/output evidence is retained; exact commands/bindings, timestamps,
progress, integer totals and run<=project are checked. Attribution requires
both endpoints SAFE/PRIMARY_RUNNING and strictly increasing timestamps.

```text
delta_images = images_B - images_A
free_consumed = free_A - free_B
project_growth = project_du_B - project_du_A
active_run_growth = run_du_B - run_du_A
other_project_growth = project_growth - active_run_growth
outside_project_pressure = free_consumed - project_growth
```

These are descriptive residuals from sequential non-atomic measurements. They
do not identify writers and are not thresholds, forecasts or cleanup triggers.
OPS2's fixed P95/multiplier/reserve and sole storage rule remain unchanged.

Test command (local existing Python):
`D:/anaconda3/python.exe -m unittest discover -s research_log/t013 -p test_primary_project_storage_attribution.py -v`.
5 tests /32 fixtures PASS in0.003s:3 zero/positive/negative residual cases,
1 zero-image case,7 run/release/freeze/dispatch/time/progress failures,
17 malformed/missing evidence cases,4 unhealthy process/storage/completion cases.
Determinism and input immutability checked; command set excludes cache_du.

One-shot remote collection via the existing project SSH configuration:

```bash
LC_ALL=C /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python /home/wenchang/asdasdsad/wjq/TOVD/research_log/t013/primary_project_storage_attribution.py
```

Commands comprise date, exact writer ps, exact tmux, anchored progress/wrapper
grep, df -B1 --output=avail, analysis existence, and exactly these two totals:

```bash
du -x -B1 -s -- /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-210355-tovd-native30-primary
du -x -B1 -s -- /home/wenchang/asdasdsad/wjq/TOVD
```

No cache du, per-directory tables, file hashing or scientific payload reads.
Fixed provenance refers to the already verified immutable run; raw commands
match its exact directory and writer. Helpers/receipts live outside the active
run. Local transcript/source hashes bind the evidence without hashing active
experiment files. Project log mirroring between snapshots contributes ordinary
project metadata bytes; residuals do not identify a writer or artifact.

A at2026-09-13T13:04:34+08:00:567/1000,57517.53246723002s,
writer721181 Rl+/tmux alive,wrapper absent,analysis absent(existence only).
Free18642763776;project_du16055738368;run_du9255936000;
OPS2 remaining433/projected7081857024/required17088163021/margin1554600755;
SAFE/PRIMARY_RUNNING. One live invocation; raw A, canonical snapshot and source
hashes are retained in primary_project_storage_attribution_receipt.json.

NEXT EXISTING HEARTBEAT: after mailbox synchronization collect B ONCE with the
same command, saving primary_project_storage_attribution_B_raw.json. Do not
recollect A or issue a separate routine health query/cache du. Parse snapshot(B).
Incident/completion-unverified -> preserve/return Lead, no attribution/remediation.
Bothhealthy -> attribute(A,B), finalize receipt/note and commit/report evidence.
No new scheduler/loop; this task is pending until B and final delivery.

No scientific/prediction contents opened, active files hashed/modified,
FIN1/replay/scientific analysis, cleanup/restart/resume/YOLO/T014 occurred.
Current CPU primary remains frozen; GPU preference applies to subsequent new
experiments. Stop after OPS5 delivery and await Lead review.
