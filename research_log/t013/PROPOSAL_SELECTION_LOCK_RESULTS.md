# T013-MECH2 PASS — synthetic preparation, awaiting Lead review

Task start:37823006fda01a942512330251608a4d67c74344.
Preregistered/pushed before execution:f8c2f685d12c6aa8fa97bbe145a10500fc851d67.
Evidence commit is the Git commit introducing this report and machine receipt.

Exact files: PROPOSAL_SELECTION_LOCK_CONTRACT.md, this RESULTS.md,
proposal_selection_lock_receipt.json, mech2/proposal_selection_lock.py,
mech2/test_proposal_selection_lock.py, mech2/tests_cpu.log, mech2/tests_cuda1.log
(all relative to research_log/t013). Delivery also appends the engineering
mailbox and project_state.md, REMOTE.md, session_log.md under research_log.

## Bound implementation and intervention

Native revision856dde20aee659246248e20734ef9ba5214f5e44;
freeze6fec32243985ccc808123d851abf5f3dea10af99.
transformer.py SHA2567436a0daf8002cb4078bc56ab4343c7ec6d1f5dfe15b41747dc357cabad1760e;
SwinT_OGC config SHA2565d7093aaaeaafbf8eec07a1aef5bee976dff5615d54e0ca88293cd92e008a7c8.
Local hashes match MECH1-bound source copies.

In Transformer.forward, I0 is the ordered top900 encoder spatial indices from
the normal V0 forward on the same image and same visual condition. It replaces
Vx's topk_proposals at transformer.py:301, following max-token scoring at:295.
Initial references are gathered exclusively from Vx unsigmoid encoder coordinates
at:304–307 and detached. Only I0/order is imported. Text features, fused text and
visual memory, encoder coordinates, learned target embeddings, decoder text/visual
attention, iterative refinement, final scores and global top300 remain native.
I0 addresses the common encoder spatial lattice; no decoder-slot cross-vocabulary
identity is assumed. Other gathers at:308–315 affect returned intermediate values
only under frozen embed_init_tgt=True; decoder targets use unchanged learned
embeddings at:316–327. GroundingDINO.forward:351–361 comments out intermediate
outputs. No extra active imported hidden state or model integration is introduced.

## Real synthetic test evidence

Existing remote Python3.12.12, Torch2.4.0+cu121; actual GPU NVIDIA RTX A6000,
device cuda:1. Two GPUs detected; each had50,598,707,200 free of50,897,289,216
bytes before tests. Nothing installed or reconfigured.

Working directory:/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/mech2

```bash
MECH2_TEST_DEVICE=cuda:1 ../venv/bin/python -m unittest -v test_proposal_selection_lock
MECH2_TEST_DEVICE=cpu ../venv/bin/python -m unittest -v test_proposal_selection_lock
```

Both exit0. CUDA:6 tests PASS in0.343s. CPU:6 tests PASS in0.009s.
These are six methods on each device, not twelve independent scientific cases.

| Required validation | Result on CPU and CUDA |
| --- | --- |
| Native max/topk/gather identity | Exact, unique-score and tied-score cases PASS |
| I0 override gathers Vx coordinates only | Exact; shifting Vx coordinates shifts references equally; inputs unchanged PASS |
| Ordered indices | Deliberate permutation produces exactly permuted references PASS |
| Null I0=Ix | Indices and references exactly unchanged PASS |
| Invalid override/requested count | Eight invalid overrides and four invalid counts rejected PASS |

Reference detach also checked with requires_grad=True synthetic coordinates.
Logs and source bytes match remote SHA256 values in the machine receipt.
No numerical scientific inference follows from these toy tensor tests.

Observed environment issue: nvidia-smi returned18, NVML driver/library version
mismatch (library580.178), before uploads/tests. Direct Torch CUDA interrogation
then succeeded and the actual CUDA tests passed, with a nonfatal NVML warning.
No driver repair was attempted; preserved warning is in tests_cuda1.log.

## Future notation — NOT RUN / NOT A GATE

AP50_lock uses frozen T013 evaluation; D_lock(c,v)=AP50_lock(clean,v)-AP50_lock(c,v);
A_lock(c,v)=D_lock(c,v)-D_lock(c,V0); C_select=A_orig-A_lock. Use original paired
image bootstrap, replicate-first differences. This is a descriptive intervention
decomposition of selector/order and its downstream consequences; residual A_lock
cannot be attributed to a single downstream module. **Never execute when Grounding
Gate1 or Gate2 fails.** Future execution requires completed primary, CLOSE1 validity,
Grounding Lead review and explicit later authorization. Current status: NOT RUN.

## Ordinary health and scope

2026-09-13T17:46:28+08:00: exact primary20260912-210355-tovd-native30-primary,
writer721181 Rl+/tmux alive,735/1000 at74510.60974929802s. Wrapper exit absent;
analysis/results.json absent by existence only. Free14,863,929,344 bytes;
accepted OPS2 required13,790,928,896; margin1,073,000,448; SAFE/PRIMARY_RUNNING.
One ordinary metadata point only; unchanged frozen CPU primary remains running.

No primary scientific/cache content, annotations, detector import/inference,
checkpoint load, frozen/run mutation, FIN1/replay, scientific metrics/bootstrap,
new Gate/threshold, second intervention, YOLO runtime or T014 execution occurred.
MECH2 is complete: stop and await Lead review. Continue existing15-minute scalar
heartbeat only; any established incident/completion-unverified state returns to
Lead through accepted OPS3 before further action. Future GPU preference retained.
