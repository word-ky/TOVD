# T013-STAT1 — PASS, synthetic arithmetic only

Research Lead assignment: `2109c88`. Scientific reference freeze: `6fec32243985ccc808123d851abf5f3dea10af99`. Eight fixture groups (source binding plus seven arithmetic groups) pass. Maximum finite absolute reference-versus-frozen error is **0.0**, within the required 1e-12; tested booleans, draw indices and NaN masks agree exactly. This is analysis-validation evidence, not a primary scientific result or an automatic research acceptance.

## Execution and independence

Command from the project root: `python research_log/t013/shadow_analysis_audit.py`. Final exit code 0; output `{"status": "PASS", "fixtures": 8, "maximum_absolute_error": 0.0, "failure": null}`.

Existing local runtime: `D:/anaconda3/python.exe`, Python 3.12.7, NumPy 1.26.4. No installation. Optional toy-COCO duplicate-copy reevaluation: **NOT RUN (dependency absent)**; `importlib.util.find_spec('pycocotools')` returned None. The previously frozen COCO regression is not claimed as rerun here.

The reference uses scalar condition/vocabulary loops from the PLAN equations and an independently sorted, linearly interpolated percentile calculator; it does not call the frozen formulas. The audit obtains the exact frozen Git blobs, verifies their agreement with HEAD and LF-normalized working files, then compiles the original function AST definitions unchanged with NumPy globals. It does not execute dependency imports, CLI code or the `analyze` raw-file reader. Shared-index call wiring in that reader is inspected as AST only. The synthetic bootstrap cell statistic is a mean of hand-authored numbers to expose pairing; it is explicitly not a replacement for dataset-level COCO AP accumulation.

| Frozen input | SHA256 of Git blob |
| --- | --- |
| scripts/t013_analysis.py | 74cc73e71385e5d38e3fbe68ff03a0f11da30e67ff39b436da90422f72e99f9c |
| scripts/t013_coco.py | bd3245235a6dcd455224ea7eb737b07875920b0a08b34f30e706dfc6a9ca9e81 |
| scripts/t013_diagnostics.py | ae7e61feaa5701ca9580c9c48901f99d09e9986b560c2821073100c94645a41e |
| research_log/t013/PLAN.md | 5d977aceb3c06a7915396aea9c7cc2504759e584ce79b459a287b18fb67e4beb |

## Mandatory fixtures

| Fixture | Result and concrete evidence |
| --- | --- |
| Frozen source binding | PASS; all four inputs agree, nine original pure function definitions loaded unchanged. |
| Positive/complementary sign | PASS; A_hard=[3,2,1,.5], complementary case=[-3,-2,-1,-.5]; D, A and hard-minus-random all match reference. |
| Linear percentile / undefined samples | PASS; known unsorted two-column samples give lower=[-2.6,-1.7], upper=[18.7,11.7]; singleton=[4,4]; NaN/Inf makes interval unavailable without dropping samples. |
| Gate1 exact threshold / zero lower | PASS; A=[1,1,0,0] with positive lower bounds qualifies exactly two corruptions; changing the second lower bound to exactly zero leaves only one and Gate1 fails. |
| Gate2 exact/adversarial boundaries | PASS; mean A=.75, mean hard-random=.50 and exactly two positive contrasts passes. A mean .7499999997671694 fails; contrast mean .49999999976716936 fails; only one positive contrast fails despite both means meeting thresholds. Perturbation=2^-30 in one corruption. |
| Shared draws and replicate-first CI | PASS; one explicit 5x4 draw matrix spans all 15 conceptual cells. First-corruption paired contrast CI=[2,5.35]; unpaired=[-.95,10.75]; subtracting marginal endpoints=[3.675,3.675]. Frozen RNG indices match exactly. Frozen loop passes the same `indices` to cached COCO accumulation, diagnostic means and margin means with no resampling inside the loop. |
| Three mechanism signs / non-rescue | PASS; distractor-FP excess and localization-minus-classification-gap excess both=[2,4,6,8]; common-support margin shrinkage=[.25,.5,.75,1]. Swapping hard/random negates all three. Strong Gate3 support remains paired with Gate1=False and Gate2=False; switching support off changes neither gate. Acceptance remains `Research Lead decision required`. |
| Common support / micro means / NaN | PASS; common GT counts=[2,6,0,6]. One aggregate margin is 2.5/6=.4166666666666667, distinct from the wrong unweighted image mean .5. Duplicate draws [1,1,2] yield [.25,.55,NaN,1.1]; all-zero support remains NaN and CI unavailable. Synthetic GT intersections and per-image sum/count agree with frozen margin plumbing. JSON uses null for explicitly undefined values. |

Full synthetic arrays, draw matrix, per-fixture values and checks are in `shadow_analysis_receipt.json`; reproducible source is `shadow_analysis_audit.py`.

## Observed audit-fixture failure retained

The first invocation stopped at a negative-control assertion after five passing groups, with frozen-versus-reference error still zero. Its first-corruption synthetic contrast coefficient was `0.5*i`; hard and random amplification were comonotonic, so correct replicate-first CI and the intentionally wrong marginal-endpoint subtraction both equalled [.5,1.3375]. This did not distinguish the procedures. The unpaired control already differed.

`shadow_analysis_initial_receipt.json` preserves that invocation and original source hash. The only correction was the hand-authored coefficient `0.5*i -> 2*i` in this audit source, producing opposite hard/random variation and the distinct negative controls above. This is an audit-data correction, not a frozen arithmetic mismatch. No frozen scientific code was patched. The original source is reproducible from the final source by that one coefficient replacement.

## Primary health and boundary

End operational observation: **2026-09-13T03:11:26+08:00**, exact run `20260912-210355-tovd-native30-primary`, tmux alive, writer PID721181 state `Rl+`, **214/1000** images at21968.800080698013 seconds. Free filesystem bytes **26,200,883,200**; no wrapper exit marker; `analysis/results.json` absent (existence check only).

No active primary prediction or scientific artifact was opened; no primary annotations, boxes, scores, AP, interaction, CI or diagnostic outcome was read. Only process/progress/storage and result-path existence were checked remotely. No frozen code/PLAN/config/vocabulary/IDs/seeds/gates or run state changed. No YOLO install/import/checkpoint/image work occurred. No remote audit execution or new experiment was needed.

Stop T013-STAT1 here and await Research Lead review. Continue the existing frozen primary and 15-minute heartbeat; no YOLO runtime, T014 or primary interpretation is authorized.
