# T013-CF2 — PASS

Task-start `a1588cb2ff11e04aeebb90029ce7b19ca0e48b74`. Preregistration/source dddb0e8;
pre-evaluation reference-binding correction2711871. Freeze
`6fec32243985ccc808123d851abf5f3dea10af99`, accepted CF1 `8154004f5574721903ee297a8a5aade729b1e131` unchanged.

Six deterministic arithmetic tests PASS in0.060s: explicit D/A/L/H values,
hard-minus-random removed component, zero removal for identical tensors,
replicate-first means, linear percentile CIs, rejection of endpoint-subtraction
and marginal-interval averaging, frozen nonfinite CI convention.

V0 end-to-end identity: **5/5 point cells x4 metrics exact**, and
**10x5 bootstrap rows x4 metrics exact** against retained REPRO1 replay_a.
Metrics are AP/AP50/AR/AR50. All10/10 hard/random condition-vocabulary cells
evaluated successfully in each replay. Each replay reads only45 completed
smoke cells. Two scratch executions took17.531221307988744s and
17.062174855032936s; metrics, all descriptor samples, point/CI JSON and draws
compare exactly. No smoke values are interpreted as scientific evidence.

Draws: reference int64(10,3), seed20260913, exact same matrix used across
original/counterfactual conditions/vocabularies. Regeneration with frozen
paired_bootstrap_indices matches exactly. Draw file SHA256:
`0bc6714a6034a8211a004d374b94f096a6928604adaff98b3a041df09a4cc267`.

Descriptor fields written (each point and replicate-first CI, samples saved):
D_cf, A_cf, L_topk, H_cf, L_topk_hard_minus_random, mean_A_cf_hard, mean_L_topk_hard, mean_H_cf, mean_L_topk_hard_minus_random.

Frozen t013_coco evaluate_dataset/image_cache/metrics/accumulate_image_copies
are imported directly from the immutable release; t013_diagnostics supplies
canonical mapping and t013_analysis supplies condition/vocabulary order.
No COCO AP reimplementation. CF1 selector bytes are unchanged; mapper indexes
original900 boxes by selected query IDs. Same maxDet100 metric accumulation
and maxDet300 per-image matching as frozen pipeline.

Environment: Python3.12.12, Torch2.4.0+cu121 CPU, NumPy1.26.4,
pycocotools2.0.8; OMP_NUM_THREADS=1/MKL_NUM_THREADS=1, existing venv, no installs.

```bash
cd /home/wenchang/asdasdsad/wjq/TOVD
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 shared/t013/venv/bin/python shared/t013/cf2/rehearse_canonical_counterfactual.py
# Called by driver, cwd shared/t013/cf2:
/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python -m unittest -v test_canonical_counterfactual_analysis
```

Existing AutoDL workflow copied sources, fetched receipts and both scratch
outputs. A transient SCP connect timeout recovered through its existing
legacy-protocol retry; all fetched artifact hashes match remote receipts.
Local Python3.12.7 only parsed sources, checked hashes and formatted reports.

Initial attempt stopped before tests, reference outputs or smoke evaluation:
whole-REPRO1-receipt semantic hash differed because the committed copy alone
had a later end_primary_health append. Every other decoded field matched
exactly. Initial failure receipt and exact remote REPRO1 receipt are retained;
2711871 binds every REPRO1 execution field except that unrelated health
append, before any CF2 evaluation. Expected normalized execution hash
`a490f9ddab943734b5b22650d8b43c124a5d66225343d38f4395327ef304ebbc`.
No source/reference output/statistical semantics were changed to pass an
identity test. Final same-draw and V0 metric identity tests passed first run.

Source SHA256s (local bytes equal remotely tested bytes):

- `canonical_topk_counterfactual.py`: `cef3e87ea1a05b40dc36522022b50280f35e8caf78dbcedcb7a47ce27cf01539`
- `canonical_counterfactual_analysis.py`: `93d91fa377e1557573d1cabae5008f529fc8104a98930f188bf98a97ef59453e`
- `test_canonical_counterfactual_analysis.py`: `cf34c7227f68d8b7fb3f9be902f009bbed2a36c5ff67873acd43bb15c471ef35`
- `rehearse_canonical_counterfactual.py`: `da40b6fe83eebd9edb751a53457e801f2a802d81d6f7cc72223052e9d4a85031`
- `CANONICAL_COUNTERFACTUAL_ANALYSIS_CONTRACT.md`: `884847c8b1290418a4240ff4acabcf95e21c7a8eecc865a4478a1e5466254a35`

Frozen/annotation/smoke bindings (all expected=actual):

- `/home/wenchang/asdasdsad/wjq/TOVD/releases/20260912-210306-tovd-native30-primary-freeze/scripts/t013_coco.py`: `bd3245235a6dcd455224ea7eb737b07875920b0a08b34f30e706dfc6a9ca9e81`
- `/home/wenchang/asdasdsad/wjq/TOVD/releases/20260912-210306-tovd-native30-primary-freeze/scripts/t013_analysis.py`: `74cc73e71385e5d38e3fbe68ff03a0f11da30e67ff39b436da90422f72e99f9c`
- `/home/wenchang/asdasdsad/wjq/TOVD/releases/20260912-210306-tovd-native30-primary-freeze/scripts/t013_diagnostics.py`: `ae7e61feaa5701ca9580c9c48901f99d09e9986b560c2821073100c94645a41e`
- `/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/cf2/canonical_topk_counterfactual.py`: `cef3e87ea1a05b40dc36522022b50280f35e8caf78dbcedcb7a47ce27cf01539`
- `/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/coco/annotations/instances_val2017.json`: `e8c7f7908f1d7278341fae127d0da654f102f11bd7b21d8aeefa635b8c810b6f`
- `/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-205428-tovd-native30-pipeline-smoke/artifacts/cache/run_receipt.json`: `a1ec8408c5294935759b462f4f0663b8a5e7b9620acebd61bceb977a509bf0e5`
- `/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-205428-tovd-native30-pipeline-smoke/artifacts/cache/cache_manifest.jsonl`: `3d3623c2a6d78edd63b35c3efbdaf733df48eb1ffb9cefe36ea7e2daf2355a5f`

REPRO1 retained reference paths/hashes:

- `accepted_receipt` at `/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/repro1/analysis_replay_receipt.json`: `027e5a05d296fb9b74ffd0249cecbbcee0bf12728cdcb63f6be2f93236b1bb2d`
- `results.json` at `/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/repro1/replay_a/results.json`: `6f0e93a90cfb59ae583f1069f01637d84f88ce3ccb407ef63524d5fe7adf8aef`
- `bootstrap_samples.npz` at `/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/repro1/replay_a/bootstrap_samples.npz`: `6dc5c80a77e687a8f5a4f96a166b0e892c23cae1893c5c38b191ca000fe627aa`
- `paired_image_draws.npy` at `/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/repro1/replay_a/paired_image_draws.npy`: `0bc6714a6034a8211a004d374b94f096a6928604adaff98b3a041df09a4cc267`

Scratch artifacts fetched under research_log/t013/cf2; remote originals under
shared/t013/cf2/replay_a and replay_b:

- `cf2/replay_a/paired_image_draws.npy`: `0bc6714a6034a8211a004d374b94f096a6928604adaff98b3a041df09a4cc267`
- `cf2/replay_a/metrics.npz`: `3ff63f4ad09265167f4aa1daf3175244ebb4a3ac429f873e64408ac77d4dbadd`
- `cf2/replay_a/descriptor_samples.npz`: `90595f1d23dda4189eb27e40fd24e5bd5fc5065e1fd9cb1e3cad4b0a514f1502`
- `cf2/replay_a/descriptors.json`: `b3c21547c146967f29d2e73763ce0ecbaa46b09f3b36283921eed367027fca8f`
- `cf2/replay_b/paired_image_draws.npy`: `0bc6714a6034a8211a004d374b94f096a6928604adaff98b3a041df09a4cc267`
- `cf2/replay_b/metrics.npz`: `3ff63f4ad09265167f4aa1daf3175244ebb4a3ac429f873e64408ac77d4dbadd`
- `cf2/replay_b/descriptor_samples.npz`: `90595f1d23dda4189eb27e40fd24e5bd5fc5065e1fd9cb1e3cad4b0a514f1502`
- `cf2/replay_b/descriptors.json`: `b3c21547c146967f29d2e73763ce0ecbaa46b09f3b36283921eed367027fca8f`

Also changed/added canonical_counterfactual_receipt.json,
canonical_counterfactual_initial_blocked_receipt.json,
cf2_remote_repro1_receipt.json, canonical_counterfactual_tests.txt, this report,
coordination/CODEX_TO_CHATGPT.md and research_log/REMOTE.md,
project_state.md, session_log.md. Raw evidence file hashes are recorded in the
delivery manifest; report/mailbox/handoff versions are bound by Git commits.

Separate ordinary health16:22:37+08:686/1000 at69503.83722913102s,
writer721181 Rl+/exact tmux alive,wrapper/result absent(existenceonly),
free16077082624,remaining314,projected5135572992,required14752622183,
margin1324460441,SAFE/PRIMARY_RUNNING via unchanged OPS2. No extra OPS watch.

No active-primary cache/predictions/scientific content, primary FIN1/replay,
inference, original run/cache/reference/release mutation, new Gate/threshold,
YOLO runtime or T014 occurred. Annotations used only for completed smoke.
Inner loss/gradient/update/reset do not apply to cached selection/evaluation.
CF2 remains descriptive-only: no causal upstream-module claim, no Grounding
rescue or decision change. Primary execution requires later explicit Lead
decision after completed Grounding review. Stop CF2 and await review;
continue ordinary scalar monitoring. Frozen CPU primary and future GPU
preference remain unchanged.
