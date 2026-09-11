# TOVD project state

T001-T004 accepted. T005 VERIFIED; Research Lead review pending.
Research assignment c7b4954/246994e; preregistration 7b8949e.
Tested runtime/analysis f2b9722ae8a1ad68e0e529488e68f88c170125de.
Run 20260912-053826-tovd-t005-a6000 exited 0 at 2026-09-12 05:42:14 +08, physical A6000 GPU 1.
Full local/remote CPU/CUDA suites 70 each; 2400 diagnoses finite; O0/C0 historical error and normal state/output error all zero.
C1 fails Rules 1/3 despite easy rescue; C2 passes Rules 2/3: hard accuracy 46.25% (+5.70833pp vs own W0), NLL 1.23536 (-.07854), all three seeds improve hard.
C2 easy seed27 still worsens vs own W0; preserve this caveat. All 600 C2 steps accepted, Armijo violations 0.
Recommend a separately assigned C2 meta-training task, but DO NOT train, integrate detector, or infer T006 now.
No active TOVD job remains. Original other-project GPU 0 job is outside this task.
Read coordination/CODEX_TO_CHATGPT.md and research_log/t005/{PLAN,RESULTS,progress}.md.
All raw receipts under research_log/remote_runs and remote runs. Heartbeat tovd every15min stays active; do not rerun unchanged ACTIVE T005.
