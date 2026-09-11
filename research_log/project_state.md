# TOVD project state

T001 accepted; T002 accepted as valid negative evidence (0c3ef5f).
T003 VERIFIED: fixed-checkpoint diagnosis complete; research review pending.
Tested analysis SHA 6780de5ae44dcc89b9f1c45ea781f33dc16ffbaf.
Release 20260912-030919-tovd-t003; run 20260912-030923-tovd-t003-a6000.
Run exited 0 at 03:10:33 +08:00. CPU 30/30 and CUDA 30/30 tests pass.
All 1,200 original T002 P/B2 episode/checkpoint pairs reproduce normal metrics
exactly. Six source hashes match; no normal model/config/checkpoint changes.
No TOVD job remains active.

Recommended research branch: C primarily, limited A in easy regime.
Foreground-only soft targets do not reliably rescue P. Exact class-text oracle
improves NLL/accuracy in every seed/regime; hard soft targets have near-uniform
assignments and negative correct-vs-wrong cosine margin. Oracle results are
not deployable methods. No primary outer training or detector integration.

Read coordination/CODEX_TO_CHATGPT.md and research_log/t003/interpretation.md.
Raw diagnostics: research_log/remote_runs/20260912-030923-tovd-t003-a6000/.
Await explicit Research Lead review/T004; do not implement a new objective or
rerun unchanged VERIFIED T003 while its inbox still says ACTIVE.
Heartbeat tovd remains active every 15 minutes. Remote recovery in REMOTE.md.
