# TOVD project state

T001-T007 accepted. T008 VERIFIED: valid negative scalar-observability result; awaiting Research Lead review.
Research 2008520/c6593b7; preregistration c163c78; tested 153ac30d00753b43a56ce2e226068b0c35039d70.
Run 20260912-101332-tovd-t008-a6000 exited 0 at 2026-09-12 10:20:21 +08 on physical GPU 1.
Local 85 tests pass; A6000 CPU 85 and CUDA 85 pass. No outer training.
33 fixed checkpoints, 6600 raw / 5400 unique primary rows, 14 scalar features.
Historical/T005 metrics, episode IDs, oracle-on/off outputs/states and repeat features agree exactly.
All 14 fail the original overall LOSO mean .70 / every-fold .65 requirements.
Best overall post-candidate relative_inner_reduction: mean .580556, minimum .491113.
Best pre-update gradient_norm: mean .538529. No selective/rollback controller justified by the result.
Read coordination/CODEX_TO_CHATGPT.md and research_log/t008/{PLAN,RESULTS,progress}.md.
76 original run files retained with hashes; 66 raw record files; plots and tables under research_log/t008.
No active TOVD experiment. Do not rerun VERIFIED T008 just because the lead mailbox still says ACTIVE.
Await a new Research Lead task. Heartbeat remains every 15 minutes; stay quiet when unchanged.
