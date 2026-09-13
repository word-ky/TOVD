# T013-OPS7 — STORAGE_RISK_RETURN_TO_LEAD

Stopped immediately at point2 under the existing OPS7 criterion. This is the
specified successful operational stop, not a scientific failure. Primary was
still running at the observed point; no process was stopped or modified.

Assigned task-start:d24c801221c946af60a526d05f8ef6a947e2f462.
Execution-start:f1cf362eea45460edd60e908c09006b10e853008.
Point1 commit:568b771d2c029dd526a8def830ba223ef600ea57.
Mid-watch Lead instruction:f428b50f938062a97d60242e0a57848deb5ce6e9:
continue unchanged, preserve original window. Final evidence is the commit
introducing this report and incident snapshot; explicit SHA in delivery mailbox.

## Two ordinary-cadence points

All times2026-09-13 UTC+08. Actual spacing1044s=17min24s. Window ended early
at17min24s because point2 met the mandatory immediate stop criterion. No third
or fourth point collected, no tighter poll, new scheduler or daemon.

| Point | Time | Images | Free bytes | Remaining | Projected remaining bytes | Required free bytes | Margin bytes | Storage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 19:34:19 | 799/1000 | 13319274496 | 201 | 3287420928 | 12534839706 | 784434790 | SAFE |
| 2 | 19:51:43 | 809/1000 | 11911069696 | 191 | 3123867648 | 12338575770 | -427506074 | STORAGE_RISK_RETURN_TO_LEAD |

Both points: exact writer721181 `Rl+`, exact tmux present, no wrapper exit marker,
`PRIMARY_RUNNING`, analysis/results.json absent by existence only. Elapsed
progress seconds:81009.45043654303 and81988.280330254, respectively.
Run20260912-210355-tovd-native30-primary;
release20260912-210306-tovd-native30-primary-freeze;
freeze6fec32243985ccc808123d851abf5f3dea10af99;
dispatch88668f76b22777459b5792dd28f88075f208c678.

The negative margin is the only storage trigger used. No conclusion about the
cause of free-space change, depletion rate, time-to-failure, forecast gate or
cleanup recommendation was derived.

## Reused evidence and exact operations

Unchanged OPS2 primary_survival_guard.py from
e380d14e5ee7b830781d38cc9efae292509ca66a;
unchanged OPS3 primary_incident_snapshot.py from
6ecbc36bd66eb2e4ca6057f9a33c81863ed7eff7. Their Git blob contents and local
normalized source were verified equal at watch start. Source hashes recorded
in ops7_preservation_watch_receipt.json. No helper edits or repeated tests.

Existing PowerShell Autodl.Common.ps1 Invoke-AutodlSsh, from the configured
workflow root, collected date -Is, exact tmux has-session, exact ps PID/state,
latest completed_images scalar, anchored wrapper exit marker, LC_ALL=C
df -B1 --output=avail project root, and test ! -f exact analysis/results.json.
Full commands and run paths are preserved in the watch receipt.

Local Python called accepted health_guard for point1 and accepted
canonical_snapshot(raw) for point2; OPS3 invokes unchanged health_guard.
OPS2 constants remain1000 images,16355328 bytes/image,6/5 multiplier,
8589934592-byte reserve. No Torch/model/GPU operation is required here.
Point2 raw transcript, supplied metadata and canonical OPS3 snapshot are
preserved. Writer success is evidenced by its matching ps row; tmux success
by the conditional PRIMARY_TMUX_ALIVE marker. No active files were hashed.

Exact changed artifacts under research_log/t013:
ops7_preservation_watch_receipt.json, ops7_incident_point2.txt,
ops7_incident_raw.json, ops7_incident_snapshot.json, this report.
Delivery appends coordination/CODEX_TO_CHATGPT.md plus research_log/
project_state.md, REMOTE.md, session_log.md; necessary small receipts mirrored
under the remote project root.

## Scope and handoff

All frozen scientific code/config/IDs/vocabulary/seeds/gates/run bytes were
left unchanged. No du, recursive scan, active-file hash, scientific/prediction
content, annotations, FIN1/replay, cleanup/deletion/compression/movement,
restart/resume/kill, driver/NVML repair, YOLO/T014, CF1/CF2/MECH2 execution.
No new threshold, trend model or remediation policy. Primary remains untouched.

**Return to Research Lead now; OPS7 is closed at the incident.** Await explicit
next instruction. Do not continue its remaining watch points or start repair.
No scientific content or FIN1 execution is authorized by this incident.
