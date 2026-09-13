# T013-OPS2 — operational reporting only

Engineering PASS; awaiting Research Lead review. Task-start HEAD:
`7ccfe778148930a0fe67808f84726de7aca229ae` (merges Lead `0f39342` and the
467-image health entry). CLOSE1 was accepted by Lead `bc74aa6`.

`primary_survival_guard.py` takes scalar metadata and performs no I/O. The fixed
OPS1 constants are 1,000 images, P95 allocation 16,355,328 bytes/image, multiplier
6/5, and reserve 8,589,934,592 bytes. With remaining = 1000 - completed_images:

```text
projected_remaining = 16355328 * remaining
required_free = (6 * projected_remaining + 4) // 5 + 8589934592
margin = free_bytes - required_free
SAFE iff margin >= 0; otherwise STORAGE_RISK_RETURN_TO_LEAD
```

This is exact integer ceil arithmetic. The current in-flight image remains in
the remaining count. No percentile/reserve/threshold is estimated or changed.

`health_guard` reports storage separately from process state. A nonzero wrapper
exit takes reporting precedence. Without an exit marker, both writer and tmux
must be alive to report PRIMARY_RUNNING. Exit 0 with both gone reports
PRIMARY_COMPLETE_UNVERIFIED. Other combinations return
PROCESS_STATE_AMBIGUOUS_RETURN_TO_LEAD. Invalid scalar metadata raises
ValueError, producing no SAFE result. The helper takes no analysis-file path and
never authorizes scientific access, repair, cleanup, restart or resume. Analysis
existence can be recorded alongside its output, without changing it.

Validation command (repository root, local Python 3.12):

```powershell
D:/anaconda3/python.exe -m unittest discover -s research_log/t013 -p test_primary_survival_guard.py -v
```

Five tests / 32 fixtures PASS: two known snapshots, six equality/one-byte-below
boundaries (including fractional ceil and zero remaining), 12 invalid storage
inputs, eight process states and four invalid process inputs. Original OPS1
188-image snapshot reproduces required 24,526,566,196 and margin 2,176,675,020;
456-image snapshot reproduces projected 8,897,298,432, required 19,266,692,711 and
margin 2,484,468,121. Rehearsal uses three committed session-log entries only
(188, 456, 467), preserving their source lines and commit in the JSON receipt.

One end-of-package SSH metadata query used the existing Autodl.Common.ps1
Invoke-AutodlSsh workflow with the project's .autodl/config.json. Exact remote
command:

```bash
date -Is; tmux has-session -t autodl-20260912-210355-tovd-native30-primary && echo PRIMARY_TMUX_ALIVE; ps -p 721181 -o pid=,stat=; grep completed_images /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-210355-tovd-native30-primary/train.log | tail -n 1; grep "^\[autodl\] exit_code=" /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-210355-tovd-native30-primary/train.log; df -B1 /home/wenchang/asdasdsad/wjq/TOVD; test ! -f /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-210355-tovd-native30-primary/artifacts/analysis/results.json && echo ANALYSIS_NOT_COMPLETE
```

At 2026-09-13T10:20:53+08:00, exact primary writer 721181 Rl+ and tmux alive,
469/1000 at 47754.84462102302 seconds, free 21,460,013,056 bytes. Required free
19,011,549,594; margin 2,448,463,462; SAFE / PRIMARY_RUNNING. No wrapper exit
marker, analysis result absent by existence only. Raw query output and computed
receipt are retained beside this document.

No primary prediction/scientific content was opened; no cache scan or mutation,
FIN1, analysis/replay, frozen scientific/run change, environment change or YOLO
runtime occurred. The earlier heartbeat push raced with new Lead commits; both
histories were merged, without changing experiment state.

Future existing 15-minute health entries use these same scalar inputs and report
required_free/margin/status. Return-to-Lead status means preserve metadata and
report immediately; no remediation is authorized. Stop OPS2 here and await Lead.
The immutable primary continues. Existing CLOSE1/FIN1/REPRO1/DEC1 completion and
scientific-review conditions remain unchanged.
