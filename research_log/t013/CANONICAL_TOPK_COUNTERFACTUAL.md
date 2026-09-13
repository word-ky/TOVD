# T013-CF1 — pre-outcome canonical-only top-300 contract

Task-start HEAD: 56c80996fdbe274f583596db018cd10cd64f755c.
Scientific freeze: 6fec32243985ccc808123d851abf5f3dea10af99.
Frozen scripts/t013_native_detector.py SHA256:
b49f23f131777f08e23131ad55a94d9211c33b1c759adf86c6b52e2b95c34126.

This preparation does not authorize primary scientific execution. Only after
the completed primary is scientifically valid and Research Lead explicitly
authorizes follow-up may this contract be applied to it. It cannot rescue a
failed Gate1 or Gate2 or change any T013 Gate or primary decision.

The in-memory helper accepts the saved 900 query boxes and [900,C] class_scores
(C=80/110/110). It uses exactly Torch2.4.0 CPU:

```python
scores, flat = torch.topk(torch.from_numpy(class_scores[:, :80]).flatten(), 300)
query_ids = flat // 80
labels = flat % 80
selected_boxes = boxes[query_ids]
```

Only the final selection excludes distractor columns80..109. Canonical
scores, boxes, text input, upstream queries/logits, weights and pixels remain
unchanged. No NMS, threshold, clipping, recomputation, calibration,
renormalization or refill. Ties retain frozen Torch topk behavior.

Preregistered later descriptors (not calculated in CF1):

- D_cf(c,v) = AP50_cf(clean,v) - AP50_cf(c,v).
- A_cf(c,v) = D_cf(c,v) - D_orig(c,V0), with V0 exact identity.
- L_topk(c,v) = A_orig(c,v) - A_cf(c,v).
- Retain the hard-minus-random comparison under the same counterfactual.

L_topk describes interaction removed by excluding distractors from final
top-300 competition. Nonzero A_cf means this final competition does not fully
explain the effect; it does not identify an upstream module as causal. These
are descriptive decompositions, with no new significance rule or Gate.

Validation is five deterministic synthetic tests and exactly45 completed
engineering smoke cells from run20260912-205428-tovd-native30-pipeline-smoke:
IDs139,285,632 x clean/gaussian_noise/motion_blur/fog/jpeg_compression x
V0/Vhard30/Vrand30. V0 must match all three stored top arrays exactly15/15;
hard/random must match the direct Torch slice reference30/30. Selected scores
and boxes must equal stored arrays indexed by returned IDs, labels<80.
No annotations or metrics. Any identity failure stops/reports a blocker.

Smoke receipt SHA256 a1ec8408c5294935759b462f4f0663b8a5e7b9620acebd61bceb977a509bf0e5;
manifest SHA256 3d3623c2a6d78edd63b35c3efbdaf733df48eb1ffb9cefe36ea7e2daf2355a5f.
Use existing project Python3.12/Torch2.4.0+cu121 CPU without installs.
No new inference, active-primary cache/scientific access, FIN1/replay, run
mutation, YOLO runtime or T014. Ordinary scalar health monitoring remains
separate. GPU preference persists for later experiments; this exact selection
identity task explicitly requires frozen CPU Torch semantics.
