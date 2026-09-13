# T013-OPS6 — ordinary-cadence survival watch

ACTIVE: point1/maximum4; window starts2026-09-13T13:58:00+08:00.
Task-start HEAD9f008f73db3e8dd2bf7506f4f6a31ab231695323 accepts OPS5.
Reuse unchanged OPS2 health_guard (e380d14e5ee7b830781d38cc9efae292509ca66a)
and OPS3 canonical_snapshot (6ecbc36bd66eb2e4ca6057f9a33c81863ed7eff7).
Local source bytes match their committed Git blobs after Git newline
normalization; no helper changed, no tests repeated, no new executable created.

Each existing approximately15-minute heartbeat uses the same ordinary SSH
metadata command through Autodl.Common.ps1 and the project's .autodl/config.json:

```bash
date -Is; tmux has-session -t autodl-20260912-210355-tovd-native30-primary && echo PRIMARY_TMUX_ALIVE; ps -p 721181 -o pid=,stat=; grep completed_images /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-210355-tovd-native30-primary/train.log | tail -n 1; grep "^\[autodl\] exit_code=" /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-210355-tovd-native30-primary/train.log; LC_ALL=C df -B1 --output=avail /home/wenchang/asdasdsad/wjq/TOVD; test ! -f /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-210355-tovd-native30-primary/artifacts/analysis/results.json && echo ANALYSIS_NOT_COMPLETE
```

Save stdout as primary_survival_watch_pointN.txt. Locally supply these observed
scalars with source references to OPS3 canonical_snapshot, which calls OPS2.
Persist both supplied metadata and canonical output in the watch receipt.
Use the existing OPS3 canonicalizer for any incident evidence; its remote
collector need not run, avoiding operational-file hashing. If result existence
changes, preserve the boolean only; do not open results. Missing/inconsistent
query evidence must not be filled with assumed healthy values.

Point1 at13:58:00:600/1000,60797.984918s,writer721181 Rl+/tmux alive,
wrapper marker absent,analysis result absent(existence only),free17867317248,
remaining400/projected6542131200/required16440492032/margin1426825216,
SAFE/PRIMARY_RUNNING. Exact primary bindings are in the receipt.

Next three ordinary heartbeats each collect one point, with no extra health
query, du, directory scan, file hashing, new helper, scheduler or polling loop.
At any return-to-Lead/completion-unverified state preserve that point and stop
immediately. 1000 images with the wrapper active is not scientific readiness.
If all four points remain healthy over45–60minutes, finish and report the exact
sequence/spacing and evidence commit, then await Lead. No rate fit, forecast,
time-to-failure estimate, new gate or cleanup recommendation.

No prediction/scientific access, active-file hash/mutation, FIN1/replay,
cleanup/restart/resume/YOLO/T014 action. Frozen CPU primary unchanged; user GPU
preference remains applicable to subsequent new experiments.
