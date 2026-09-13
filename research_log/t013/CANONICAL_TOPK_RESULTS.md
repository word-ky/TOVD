# T013-CF1 — PASS

Task-start `56c80996fdbe274f583596db018cd10cd64f755c`.
Preregistered helper/contract/test commit `d8d3beb` preceded smoke validation.
Scientific freeze `6fec32243985ccc808123d851abf5f3dea10af99` unchanged.

Five synthetic tests passed in0.090s (index mapping, score/box identity and
input preservation, repeated calls including ties, high distractor crowd-out,
V0 original selection). All15/15 V0 smoke cells exactly reproduced stored
query IDs, labels and scores. All30/30 hard/random cells exactly matched the
direct frozen-Torch canonical-slice reference; all labels<80, selected scores
and boxes exactly equal stored arrays indexed by returned query/class IDs.
Total45/45 cells PASS; no annotations or COCO metrics computed.

Environment: Python3.12.12, Torch2.4.0+cu121 CPU, NumPy1.26.4,
OMP_NUM_THREADS=1/MKL_NUM_THREADS=1. Existing project venv, no installation.
Local Python3.12.7 was used only for syntax checks, receipt verification and
report writing. The exact Torch operation ran remotely in the frozen version.

```bash
cd /home/wenchang/asdasdsad/wjq/TOVD
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 shared/t013/venv/bin/python shared/t013/cf1/validate_canonical_topk_smoke.py
# Driver invokes, cwd shared/t013/cf1:
/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python -m unittest -v test_canonical_topk_counterfactual
```

Existing AutoDL Copy-To/FromAutodl transferred the four committed source/note
files to shared/t013/cf1 and fetched the receipt/test log. No run/release files
were written. Minimal smoke receipt driver has a fixed completed-smoke path;
the core helper accepts only in-memory arrays and performs no filesystem I/O.

Frozen detector SHA256:
`b49f23f131777f08e23131ad55a94d9211c33b1c759adf86c6b52e2b95c34126`.
Smoke run `20260912-205428-tovd-native30-pipeline-smoke`, cache under its
artifacts/cache; completed receipt and IDs139/285/632 verified.
Receipt SHA256 `a1ec8408c5294935759b462f4f0663b8a5e7b9620acebd61bceb977a509bf0e5`;
manifest SHA256 `3d3623c2a6d78edd63b35c3efbdaf733df48eb1ffb9cefe36ea7e2daf2355a5f`.
All match pre-existing bindings. Changed package file SHA256s (raw bytes,
verified identical between local files and the remote-tested source receipt):

- `canonical_topk_counterfactual.py`: `cef3e87ea1a05b40dc36522022b50280f35e8caf78dbcedcb7a47ce27cf01539`
- `test_canonical_topk_counterfactual.py`: `bd7e7995f9b3264c4d13113582f09443bfaf05f17cb7afd5d35aceace716daf8`
- `validate_canonical_topk_smoke.py`: `edc8f2b04b41e7267ab92dfa24bb6788e0c9aa1b9b2e9da8e4ea8f45b20087cf`
- `CANONICAL_TOPK_COUNTERFACTUAL.md`: `2925d9bf419febb3cbfb40e8393ec1002a7705e6cdfc1a63069b80e15eabc57a`
- `canonical_topk_receipt.json`: `f0fa74481bf336b520de0fb054927930e4f2184462e9cdf06fabba0ad0abd061`
- `canonical_topk_tests.txt`: `6d4934c6188a7562ff99e53c7cc4684236d548d38c3de8c1f01b32d47b1152f4`

Also added this results note and updated coordination/CODEX_TO_CHATGPT.md,
research_log/REMOTE.md, project_state.md and session_log.md for delivery.
No implementation/test failure. Initial local lookup used a nonexistent
analysis_replay_preflight_receipt.json filename; existing
analysis_replay_receipt.json was located. This did not affect validation.

Separate ordinary health check15:28:09+08:654/1000 at66208.25556416s,
writer721181 Rl+/tmux alive, no wrapper exit, result absent(existenceonly),
free16806002688, remaining346, projected5658943488, required15380666778,
margin1425335910 bytes; unchanged OPS2 SAFE/PRIMARY_RUNNING. No additional
OPS watch/du attribution. Active-primary cache and scientific payloads were
never accessed. Frozen scientific source was hashed as authorized, never
modified. No FIN1/replay, inference, annotations/metrics, run mutation, YOLO
runtime or T014. Inner-loss/update/gradient/reset diagnostics are not
applicable to pure selection; no adaptation was performed.

D_cf, A_cf, L_topk and hard-minus-random descriptors are preregistered in
CANONICAL_TOPK_COUNTERFACTUAL.md, not calculated. They describe only final
selection participation; residuals do not identify a causal upstream module.
No change to T013 Gates/primary decision; a failed Grounding primary remains
failed. Primary scientific execution requires a later explicit Research-Lead
decision after a scientifically valid completed primary. CF1 complete; stop
and await review. GPU preference retained for subsequent new experiments.
