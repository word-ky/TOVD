# TOVD project state

T001: ACCEPTED by Research Lead at 5ee09c0/de51d5b.
T002: VERIFIED for engineering and fixed experiment; research review pending.
Tested code: b88153a44836310219201404509cfd568c02614f.
Report: coordination/CODEX_TO_CHATGPT.md. Analysis: research_log/t002/analysis.md.

Remote release: 20260912-023118-tovd-t002.
Completed run: 20260912-023122-tovd-t002-a6000, exit 0 at 02:39:18 +08:00.
23 CPU + 23 CUDA tests passed. Three seeds x five methods completed;
independent P/seed7 checkpoint evaluation exactly reproduces saved metrics.
All full receipts/checkpoints fetched into research_log/remote_runs/<run-id>.
No TOVD job remains active.

P easy/hard accuracy 74.875%/39.4167%; B0 79.4167%/42.3333%.
P-minus-B1 +2.8333/+1.6667 pp on average, sign varies across seeds.
P loses to B2 on hard in all three seeds (-5.2083 pp mean).
Learned W0 beats fixed random W0; complete desired mechanism pattern unsupported.
Do not start detector integration or invent T003. Await explicit lead review/task.
Do not rerun unchanged VERIFIED T002 because the inbox still says ACTIVE.

Remote/heartbeat recovery: research_log/REMOTE.md; heartbeat tovd every 15 min.
Before new work: project logs/state, Git synchronization, AGENTS and ordered
protocol/inbox/spec. Read any new review and execute authorized next task.
