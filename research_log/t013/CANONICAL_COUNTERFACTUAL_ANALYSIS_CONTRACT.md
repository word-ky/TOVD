# T013-CF2 — pre-outcome paired analysis contract

Task-start a1588cb2ff11e04aeebb90029ce7b19ca0e48b74.
Freeze6fec32243985ccc808123d851abf5f3dea10af99;
accepted CF1 evidence8154004f5574721903ee297a8a5aade729b1e131.
CF1 selector remains byte-identical. CF2 uses only completed smoke
20260912-205428-tovd-native30-pipeline-smoke, IDs139/285/632, five conditions,
V0/Vhard30/Vrand30. No inference or active-primary cache/scientific access.

In-memory predictions use CF1 selected IDs/scores and the original 900 boxes
with frozen canonical_predictions category mapping. Frozen t013_coco functions
perform bbox COCOeval, matching maxDet300 and primary AP/AP50/AR/AR50 maxDet100
accumulation. No AP reimplementation, pixel/model/score/box changes, NMS,
threshold, clipping, calibration, renormalization or refill.

Use exactly REPRO1 shared/t013/repro1/replay_a/paired_image_draws.npy,
int64 shape(10,3), seed20260913; check decoded equality against frozen
paired_bootstrap_indices(3,seed=20260913,replicates=10) before use. Reuse
identical rows for original and CF values, all conditions/vocabularies.

For point values and separately for each paired replicate:

- D_cf(c,v)=AP50_cf(clean,v)-AP50_cf(c,v).
- A_cf(c,v)=D_cf(c,v)-D_cf(c,V0), with exact V0 original identity.
- L_topk(c,v)=A_orig(c,v)-A_cf(c,v).
- H_cf(c)=A_cf(c,Vhard30)-A_cf(c,Vrand30).
- L_topk_hard_minus_random(c)=A_orig(c,Vhard30)-A_orig(c,Vrand30)-H_cf(c).
- Four-corruption means: mean_A_cf_hard, mean_L_topk_hard, mean_H_cf,
  mean_L_topk_hard_minus_random.

Form all contrasts and means within each replicate first, then use NumPy
percentile([2.5,97.5],axis=0,method='linear'). Never subtract CI endpoints or
average marginal CI endpoints. Follow frozen interval nonfinite convention:
undefined sample arrays yield null CI. No new statistical threshold or Gate.

Acceptance: six synthetic arithmetic tests; exact5x4 V0 point values and
10x5x4 V0 bootstrap values against retained REPRO1;10 hard/random evaluation
cells; two exact scratch replays of metrics and all descriptors. Store points,
metric/descriptor samples, draws and descriptor point/CI JSON under
shared/t013/cf2/replay_a and replay_b, never original runs/releases/references.
Record source/data/reference hashes, draw identity, counts and scope receipt.
Annotations are authorized only for this completed-smoke rehearsal.

These descriptors isolate final top300 participation, not a causal upstream
module. Smoke values have no scientific interpretation. No primary FIN1,
replay, CF execution, new inference, YOLO or T014. A failed Grounding primary
remains failed. Later primary CF execution requires explicit Lead decision
after completed Grounding review. Stop/report any V0, pairing or binding
failure without tuning semantics. Existing scalar health cadence continues;
an established incident/completion-unverified state returns to Lead.

Frozen environment: Torch2.4.0 CPU, NumPy1.26.4, pycocotools2.0.8, existing
Python3.12.12. No install/update. GPU preference for new experiments remains;
this task requires CPU top-k identity and frozen COCO accumulation semantics.
