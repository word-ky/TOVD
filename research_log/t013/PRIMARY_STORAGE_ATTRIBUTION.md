# T013-OPS4 — two-snapshot storage accounting

Status: engineering PASS; awaiting Research Lead review.
Task-start HEAD: `032de1a44ae19d0fda497fe43909b0fee98f63ab`.

The helper reuses accepted OPS2 health_guard and fixed OPS3 primary identifiers.
It parses exact command/output records, checks run/freeze bindings, timestamp
order, nondecreasing progress, nonnegative aggregate allocated sizes, cache<=run,
and SAFE/PRIMARY_RUNNING at both endpoints before computing attribution.
No new storage threshold, trend fit or remediation policy is introduced.

```text
delta_images = images_B - images_A
free_consumed = free_A - free_B
active_run_growth = run_du_B - run_du_A
cache_growth = cache_du_B - cache_du_A
noncache_run_growth = active_run_growth - cache_growth
outside_run_pressure = free_consumed - active_run_growth
cache_growth_per_new_image = cache_growth / delta_images (null if zero images)
```

The residual describes bytes not explained by the run's net allocated growth.
It does not identify an external writer, and is not a safety gate. Positive,
zero and negative residuals are retained. Measurements are sequential on a live
filesystem, so the accounting is not an atomic transaction. A current partial
image can contribute cache growth; bytes/new completed image is descriptive.

Validation: `D:/anaconda3/python.exe -m unittest discover -s research_log/t013 -p test_primary_storage_attribution.py -v`.
Five tests /31 fixtures PASS in0.003s:3 residual cases,1 zero-image case,6
binding/time/progress cases,17 malformed/missing evidence cases,4 unhealthy
process/storage/completion states. Determinism and no input mutation checked.

Each live snapshot executes exactly once via the existing project SSH workflow:

```bash
LC_ALL=C /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python /home/wenchang/asdasdsad/wjq/TOVD/research_log/t013/primary_storage_attribution.py
```

The collector returns every command, exit code and raw stdout/stderr in JSON.
Commands are date, exact writer ps, exact tmux session check, anchored progress
and wrapper-exit grep, C-locale df, aggregate run/cache du and analysis existence.
Run/cache commands are exactly `du -x -B1 -s -- <exact path>`; no file content
read/hash or per-image/condition/vocabulary listing is performed. Binding values
refer to the already verified immutable run/release/freeze/dispatch; this package
does not repeat operational receipt hashing. Collected command paths and PID
are matched against those exact constants. Helpers live outside the active run.

Snapshot A (one invocation) is preserved as primary_storage_attribution_A_raw.json.
At2026-09-13T12:27:10+08:00:544/1000,55303.571372162s,writer721181 Rl+/tmux alive,
no wrapper exit marker,analysis absent by existence only. Free19348643840,
run_du8877875200,cache_du8877797376,required17539570074,margin1809073766,
SAFE/PRIMARY_RUNNING. Canonical metadata, raw SHA and source hashes are in
primary_storage_attribution_receipt.json. Only local log/source/raw-transcript
files are hashed; no active experiment file is hashed.

Snapshot B was collected once at the next existing heartbeat using the same
command and retained in primary_storage_attribution_B_raw.json. Its timestamp
is2026-09-13T12:45:33+08:00:556/1000,56483.772476741025s,writer721181 Rl+/tmux
alive,no wrapper exit marker,analysis absent by existence only. Free18837422080,
run_du9061552128,cache_du9061474304,required17304053351,margin1533368729,
SAFE/PRIMARY_RUNNING. Exactly two live snapshots total; no additional normal
health query or third du snapshot was issued. Actual spacing was1103 seconds
(18m23s), reflecting the next heartbeat's dispatch timing rather than an exact
15-minute timer. No scheduler/cadence change was made.

`snapshot(raw_B)` and `attribute(raw_A,raw_B)` were executed locally with the
unchanged tested helper. Stored A and helper/test receipt hashes still match.
The finalized receipt preserves both endpoints, raw file SHA256 values and:

| Quantity | Value |
| --- | ---: |
| delta_images | 12 |
| free_consumed | 511221760 bytes |
| active_run_growth | 183676928 bytes |
| cache_growth | 183676928 bytes |
| noncache_run_growth | 0 bytes |
| outside_run_pressure | 327544832 bytes |
| cache_growth_per_new_image | 15306410.666666666 bytes/image |

During this interval the measured primary growth explains183676928 bytes of
the511221760-byte free-space decline. The327544832-byte residual is not explained
by the run's net allocated growth. This is descriptive accounting, with the
non-atomic measurement limitation above; it does not prove an external writer's
identity or quantify earlier intervals. No new threshold or cleanup
recommendation follows from it. Existing OPS2 returns SAFE at both endpoints.

OPS4 is complete. Stop and await Lead review; return to the existing scalar
health cadence. Do not repeat du attribution without a new task. On later
incident/completion-unverified preserve metadata and return to Lead before
remediation or FIN1, following the current mailbox.

User preference received during OPS4: prioritize GPU for subsequent new
experiments and validate the GPU path during preparation. The current primary
continues its frozen CPU FP32/four-thread configuration; no mid-run device
change or duplicate run occurred. No scientific payload access, active-file
mutation/hash, FIN1/replay, cleanup/restart/resume/YOLO/T014 action occurred.
