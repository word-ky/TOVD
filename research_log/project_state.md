# TOVD project state

Updated 2026-09-12T20:02:47.194079+08:00. T013 engineering BLOCKED / AWAITING RESEARCH LEAD REVIEW after mandated native/HF V0 parity failure. Authoritative scope: c07ce16/afe9c13 plus 2c4dbf5/28b8718. T001–T012 remain CLOSED.

Run 20260912-195530-tovd-t013-native-parity exit 1 at 19:56:42+08: all three disjoint images exceed fixed 1e-4 box/score tolerance. Both model states unchanged, HF replay exact. Do not rerun, relax tolerances, launch primary or T014 without new Lead instructions. Evidence: research_log/t013/NATIVE_PARITY_REVIEW.md and original remote_runs receipt.

Token-matched vocabulary supersedes r3: V0/Vhard/Vrand195/408/408; Vhard and frozen embeddings/scores unchanged. Canonical LF SHA51554562b216dcad1c693efb7781362efbac55993bc5c10651e8845ec9931977. Nine focused local/remote tests pass; matched HF CUDA 45-condition smoke passes, which does not satisfy native/HF parity. Implementation92801da; statistics972c476.

1000 IDs committed42daa6e, accepted by Lead; smoke139/285/632 disjoint. Annotations verified. ACTIVE DATA RUN20260912-190511-tovd-t013-coco-ranges-a6000, last observed98/195 image archive parts. Single writer; retain chunks. Root /home/wenchang/asdasdsad/wjq/TOVD; assets shared/t013; isolated shared/t013/venv. Collect final archive/hash receipt when complete; no further inference. No primary AP/CI/gates exist. Full PLAN/primary cache runner/full bootstrap analysis/image hashes pending.

Heartbeat tovd every15min ACTIVE. Check new Lead instruction first; otherwise only finish existing data receipt. Quiet when unchanged. Detailed recovery: t013/IMPLEMENTATION_NEXT.md, NATIVE_PARITY_REVIEW.md, session_log.md. Generic workflow last-release metadata can name another project: use actual TOVD current resolved release and source hashes (documented in parity report).
