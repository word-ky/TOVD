# T013-PARITY-B frozen diagnostic

Frozen 2026-09-12T20:21:47.922057+08:00, before any PARITY-B image outcomes. Lead revisions999b4b7/ddd24e7 authorize exactly one diagnostic on smoke139/285/632. The previous raw-query failure is preserved.

Use the existing native/HF sources, checkpoints, pixel tensors, V0 prompt and FP32 CPU with four threads. No detector logic changes. scripts/t013_native_parity.py --detection-level uses the exact primary-style Torch topk over900x80 class scores with300 selections, normalizedxyxy, no threshold or NMS. Class-score aggregation remains unchanged.

Within each canonical class, SciPy1.17.0 linear_sum_assignment minimizes negative float64 IoU. Input order is the frozen Torch topk order; exact tied optima use that pinned implementation's deterministic tie handling with no epsilon or score term. Four focused tests cover reversed detection order, count/size failure, strict IoU/score failure and identical-box tied optima; swapping scores cannot alter the assignment. All13 T013 tests passed locally in0.76s. Remote tests must pass before the single image run.

Require300 detections per implementation and identical per-class counts, then every pair IoU>=.999 and score error<=1e-4. HF replay must be exact and model state hashes unchanged. Count mismatch immediately fails detection matching; raw900-box Hungarian summaries remain diagnostic only. Save rawboxes, classscores andtop300 selections to NPZ and all matches/permutations toJSON; preserve actual run directory/release and source hashes.

If any image fails, HF1024 harness is rejected for primary use under this Lead decision and all further detector work stops pending Lead. If allpass, complete outstanding preregistration/code/data requirements before primary. No scientific Gates1–4 are evaluated here. ExistingCOCOdownload190511 remains active, last142/195parts; no duplicatewriter.
