# T013-REPRO1 — PASS, completed engineering smoke only

Lead assignment `348b1df`. Two analyses from immutable scientific freeze `6fec32243985ccc808123d851abf5f3dea10af99` completed successfully on the same old 45-cell engineering smoke cache. All required decoded outputs match exactly, including NaN masks. A scratch-only one-element mutation was correctly rejected. No primary cache or primary scientific result was accessed.

## Execution

Existing interpreter `/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python`, Python3.12.12; NumPy1.26.4, pycocotools2.0.8, torch2.4.0 package metadata, torchvision0.19.0+cu121, transformers4.44.2. No installs/updates. Exact pip freeze is `repro1/environment.txt`, SHA256 `6fdb8b3da35dddb24c5ea602e81b160ab864e792ca29fa27236dd759a6b4f090`, identical to the frozen environment receipt. OMP/MKL/OPENBLAS thread environment variables were unset in the SSH preflight process and were not changed.

Orchestrator command through the existing workflow SSH helper:

```bash
/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python -u /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/repro1/analysis_replay_preflight.py
```

The helper ran the following command twice, with `replay_a` then `replay_b` as output, both with working directory `/home/wenchang/asdasdsad/wjq/TOVD/releases/20260912-210306-tovd-native30-primary-freeze`:

```bash
/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python -m scripts.t013_analysis --annotations /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/coco/annotations/instances_val2017.json --run /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-205428-tovd-native30-pipeline-smoke/artifacts/cache --output /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/repro1/replay_a --smoke-only
```

Replay A: exit0, **19.169558475s**. Replay B: exit0, **19.055517392s**. Orchestrator exit0/PASS. Exactly three smoke IDs139/285/632,15 cells each,10 bootstrap replicates,seed20260913. Saved draw matrix is int64 `(10,3)` and exactly matches the frozen NumPy RNG draw sequence. Both logs are retained locally in `repro1/`; all replay outputs and the mutation remain on the server under `shared/t013/repro1/`, outside original run/cache/release directories. No detector inference occurred.

## Pre-execution bindings

Every expected/actual hash matched before execution:

| Input | SHA256 |
| --- | --- |
| native30_freeze.json | 50addfb8e247333b49fb22cda14570166b294101bb435b5a1b5bf688b4b3a91e |
| PLAN.md | 5d977aceb3c06a7915396aea9c7cc2504759e584ce79b459a287b18fb67e4beb |
| scripts/t013_analysis.py | 74cc73e71385e5d38e3fbe68ff03a0f11da30e67ff39b436da90422f72e99f9c |
| scripts/t013_coco.py | bd3245235a6dcd455224ea7eb737b07875920b0a08b34f30e706dfc6a9ca9e81 |
| scripts/t013_diagnostics.py | ae7e61feaa5701ca9580c9c48901f99d09e9986b560c2821073100c94645a41e |
| COCO annotations | e8c7f7908f1d7278341fae127d0da654f102f11bd7b21d8aeefa635b8c810b6f |
| Completed smoke run_receipt.json | a1ec8408c5294935759b462f4f0663b8a5e7b9620acebd61bceb977a509bf0e5 |
| Completed smoke cache_manifest.jsonl | 3d3623c2a6d78edd63b35c3efbdaf733df48eb1ffb9cefe36ea7e2daf2355a5f |

## Exact comparisons

`analysis_replay_compare.py` compares parsed JSON recursively, treating corresponding NaNs as equal. Arrays require identical keys, shapes, dtypes and element values with equal NaN masks. All four artifacts must exist and be nonempty. Compressed container byte equality is not an acceptance requirement.

| Artifact | Equality result |
| --- | --- |
| results.json | PASS all11 top-level fields recursively: kind, image count, conditions, vocabularies, metric order, point metrics, all CIs, replicates,seed,common-support counts and full assessment/gates. |
| paired_image_draws.npy | PASS int64 `(10,3)`, exact values/masks. |
| bootstrap_samples.npz | PASS both keys: metrics float64 `(10,5,3,8)` and margins float64 `(10,4)`. |
| diagnostics_per_image.npz | PASS all16 keys: c0_v0 through c4_v2 each float64 `(3,5)`; margin_contrast_sum_count float64 `(4,3,2)`. |

All19 arrays, all JSON fields and all NaN masks match. Each replay's four files total22,839 bytes; they are retained remotely without committing duplicate decoded artifacts. The receipt contains every per-key result.

Negative control: copy only replay B's scratch output to `mutation_negative_control`, then add1 to `bootstrap_samples.npz:metrics[0,0,0,0]`. Comparator returns FAIL on that array; original replay A/B and old cache are unchanged. The preflight source implements this deterministic test and preserves its full comparator report.

## Original smoke comparison

**NOT COMPARED — SOURCE VERSION NOT IDENTICAL/UNPROVEN.** Old release `20260912-205335-tovd-native30-pipeline` has t013_analysis.py SHA `f472c3cc3fb8eeab9b4de7cb37afa4c54ae90e9ecd0263a06497204b0edf5224`, differing from the final frozen SHA `74cc73e7...`. COCO and diagnostic source hashes match, but the exact analysis-stack identity criterion does not. No original analysis output was opened by this preflight, and the optional skip is not a replay failure.

## Final health and handoff

At **2026-09-13T05:38:17+08:00**, exact primary run `20260912-210355-tovd-native30-primary` tmux and writer721181 (`Rl+`) are alive; **300/1000** images at30761.30617114401 seconds; free bytes **24,575,799,296**. No wrapper exit marker; primary analysis result absent (existence only).

`active_primary_cache_accessed=false` and `primary_scientific_result_opened=false`. All decoded arrays were from completed engineering smoke replays or their scratch mutation. No scientific claim is derived from smoke metrics. No frozen code/config/data settings, environment, primary process or YOLO runtime changed. Local py_compile of both new helpers and git diff checks passed; no failed replay occurred.

Stop REPRO1 and await Lead review. After primary completion and FIN1 PASS, the same comparator can compare completed full-analysis outputs under the existing Lead reproduction contract. The pinned smoke preflight helper itself remains smoke-only and must not be repointed to the active primary.
