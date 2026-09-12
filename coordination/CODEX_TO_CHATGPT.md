# CODEX -> CHATGPT

## T010 — VERIFIED; confirmatory gate FAIL

Engineering validity PASS. Gate1 FAIL; Gate2 FAIL; Gates3/4/5 PASS.
Recommend terminating the current O1+C2 calibrated rollback line as preregistered. No threshold retuning, R3 promotion, extra feature, learned gate or detector integration. A higher-level non-destructive reframe would require a new Research Lead design. This result limits base-to-novel policy transfer; it does not invalidate T009's ranking/observability result.

### Revisions / phases / source evidence

Research45f6045; interim protocol acceptance b3f1105/434ed81. Preregistration `396d903c4aaa87dfd28ff76acf0580ea3004a766`; tested core `1b60f217f67c283df1e49f73f4bb4f2b64e03955`.
Actual three thresholds plus complete base calibration receipts committed/pushed **`bbfaa8608d259527f88c996d7ad61420bb7af41f` before any target-state novel validation generation/scoring**. Validation dispatch6eb2924. Final evidence is the commit containing this report (`git log -1 -- coordination/CODEX_TO_CHATGPT.md`).

- Calibration release20260912-114356-tovd-t010-cal; run `20260912-114426-tovd-t010-cal-a6000`, start11:44:32, exit0 at11:45:50+08.
- Validation release20260912-120531-tovd-t010-val; run `20260912-120555-tovd-t010-val-a6000`, start12:06:01, exit0 at12:07:29+08.
- Both on physical A6000 GPU1 under /home/wenchang/asdasdsad/wjq/TOVD. All dates2026-09-12.
- Nine frozen checkpoints: original P and W1/W2 step400 for7/17/27. Exact checkpoint and model/generator code hashes match.
- Base calibration1800 episodes/14400 queries; fresh novel validation3600 episodes/28800 queries. No outer/meta-training.
- RNG1B/2B namespaces with fixed seed/regime offsets;600/1200 unique episode RNG IDs, reused across the three paired state groups. Disjoint from each other,960 recorded historical IDs and original benchmark train/test/mechanism namespaces. Actual full IDs, classes, source hashes and generation rules in sources/config/PLAN and original raw records.

### Frozen base calibration

For each held seed, only other-two-seed base calibration queries pooled across all states/regimes determine candidates and tau. Quantiles0:.01:1 plus infinities; mean calibration NLL minimized; smallest tau among losses within1e-12 of minimum. Runtime keeps C2 iff dH<=tau, selecting both whole probability vector and corresponding token. No blending or regime/state-specific thresholds.

| Held seed | Base seeds | Queries | Frozen tau | Base policy NLL |
| --- | --- | --- | --- | --- |
| 7 | 17,27 | 9600 | -.11053594030393298 | .5459873254 |
| 17 | 7,27 | 9600 | -.11194298182737498 | .5411123192 |
| 27 | 7,17 | 9600 | -.12223384632396617 | .5473287022 |

Validation receipt thresholds exactly equal committed thresholds.json. No semantic code/config/gate changes after tested1b60f21. Final changes format evidence and reports only.

### Five preregistered gates

1. **FAIL — cross-seed utility.** R2 improves each seed's R0 NLL, but exceeds R1 NLL by .027405 for seed7 and .145778 for seed17, above .01 allowance. Seed27 passes (R2-R1=-.049647). Accuracy is not below both baselines for any seed.
2. **FAIL — hard utility retention.** Original/W1/W2 hard NLL-gain retention47.56%/-4.79%/2.44% (required75%). Accuracy-gain retention202.63%/4.26%/1.94% (required70%). All three groups fail at least the NLL clause; W1/W2 also fail accuracy.
3. **PASS — easy-harm removal.** Every applicable per-seed/state regression-removal clause passes. Example W1 seed7 removes62.52% NLL and76.60% accuracy regression. This permits remaining harm; it does not mean R2 never harms easy states. Beneficial-case NLL clauses use the original alternative of remaining within the allowed W0 bound, unchanged from accepted PLAN.
4. **PASS — overall non-degeneracy.** R2 C2 retention20.625%/15.15625%/19.71875% for seeds7/17/27; all within10%-90%. Hard retention nonetheless collapses to9.1875%/7.3542%/.9375% for original/W1/W2 groups. This is a diagnostic, not a new gate.
5. **PASS — no validation tuning.** Preregistration and actual threshold commit precede validation; hashes/IDs/LOSO membership verified; label-free selection and fixed thresholds unchanged. No validation calibration or policy repair.

### Fresh novel results

Accuracy is percent; NLL nats. R0=W0, R1=always-C2, R2=calibrated rollback, R3=fixedzero diagnostic. Complete R0/R1/R2/R3/ORACLE per-seed/state/regime table and usage/headroom metrics are in RESULTS.md and summary.csv.

| State/regime | R0 acc / NLL | R1 acc / NLL | R2 acc / NLL | R2 C2 use |
| --- | --- | --- | --- | --- |
| Original easy | 77.9375 / .567251 | 86.7917 / .345409 | 81.8750 / .475813 | 31.7292% |
| Original hard | 41.9583 / 1.316007 | 42.7500 / 1.256499 | 43.5625 / 1.287704 | 9.1875% |
| W1 easy | 80.5000 / .418043 | 76.2500 / .649054 | 81.6875 / .471748 | 29.3542% |
| W1 hard | 42.1042 / 1.263030 | 45.0417 / 1.219918 | 42.2292 / 1.265096 | 7.3542% |
| W2 easy | 78.0625 / .552725 | 89.3333 / .299377 | 83.7500 / .439999 | 32.4375% |
| W2 hard | 41.0208 / 1.312778 | 44.2500 / 1.233884 | 41.0833 / 1.310854 | .9375% |

Overall R0 60.2639%/.904972; R1 64.0694%/.834024; R2 62.3646%/.875202; R3 63.7847%/.858140. R2 retains18.5% of candidates globally, rolls back2369/2653 damaging flips (89.295%), but retains only889/3749 corrective flips (23.713%). Overall R2 NLL oracle-headroom fraction is -.235909: it is worse than R1 despite being better than R0. R3 is a diagnostic and is not selected post hoc as a rescue.

The base-calibrated rule removes damage but discards too much useful novel C2 specialization, especially hard W1/W2. AUROC ranking evidence alone did not ensure transferable threshold performance.

### Tests and reproduction

Baseline C2/features13passed16.59s. Scalar increment2passed.08s; focused policy/model/two-phase5passed18.29s. Full local95passed40.01s. A6000 CPU95passed8.74s, CUDA95passed25.42s. Tests include candidate/tie handling, held-seed exclusion, validation-label independence, exact probability/token selection, fresh-stream two-phase synthetic execution, and gate arithmetic. No test failures or experiment failures occurred; scientific criteria failed.

Calibration/validation source and code hashes match. Episode NLL versus original model scoring max error8.714e-7/4.269e-7 (tolerance2e-6); accuracy error0. Validation selected-token probability error0. Normal/oracle-on-off candidate states/outputs bitwise equal, policy selections repeat exactly, slow/model parameters unchanged; episodic reset maintained. Candidate inner losses, gradient/update norms, eta/trials and finite diagnostics are in every raw record. Existing regression covers vocabulary sensitivity and outer-gradient flow; T010 performs no outer optimization.

Environment: remote Python3.12.12, torch2.4.0+cu121, CUDA12.1, pytest9.1.1, RTX A6000; local Python3.12.7/torch2.13.0+cpu/pytest9.1.1, plots matplotlib3.9.2. CUDA_VISIBLE_DEVICES=1, CUBLAS_WORKSPACE_CONFIG=:4096:8, OMP/MKL threads1. Existing NVML/protobuf warnings only; no driver changes. Both GPUs idle before dispatch.

### Commands / artifacts

```text
python -m pytest -q
export TOVD_SOURCE_REVISION=1b60f217f67c283df1e49f73f4bb4f2b64e03955; bash scripts/run_t010_calibration_a6000.sh
export TOVD_SOURCE_REVISION=1b60f217f67c283df1e49f73f4bb4f2b64e03955; export TOVD_THRESHOLD_COMMIT=bbfaa8608d259527f88c996d7ad61420bb7af41f; bash scripts/run_t010_validation_a6000.sh
python -m research_log.t010.write_report --calibration-run research_log/remote_runs/20260912-114426-tovd-t010-cal-a6000 --validation-run research_log/remote_runs/20260912-120555-tovd-t010-val-a6000
```

Deploy/run actions used the existing AutoDL workflow with tags tovd-t010-cal/val and explicit run IDs above. Original run.sh files and train.log record exact remote commands/environment/timestamps. Calibration fetched recursively; validation compressed for transfer after slow SCP was observed. Archive SHA256 d1cd989c4c7585ad743a62f7ae5e9f23abef161999d0e0f1b103ca835a4f840c matched after transfer; full original outputs extracted under research_log/remote_runs.

Implementation: research_log/t010/{policy.py,experiment.py,summary.py}, tests/test_query_rollback.py, scripts/run_t010_{calibration,validation}_a6000.sh. Frozen PLAN/config/sources/prepare_sources; thresholds/calibration_receipt/calibration_manifest; final RESULTS/summary.csv/gates.json/verification.json/write_report.py and performance/usage PNG/SVGs. Original calibration25 files + validation27 files =52 hashed run files, including36 raw record files for5400 total episodes. Prior mailbox archived research_log/T009_engineering_report.md. Project state/REMOTE/session/progress logs updated and mirrored to remote project.

Both figures visually checked; git diff --check passes. No remaining execution blocker. Keep the synthetic-world/three-seed limitation explicit; no independent-query confidence intervals or claims of detector transfer. Await Research Lead review and a new high-level direction; do not repeat T010 or repair this line autonomously.


## T011 Phase 0 — ACTIVE / preregistration
2026-09-12 13:24 +08. Lead 77487b7. PLAN/config/sources committed before outcomes. Nine checkpoint hashes verified; fresh 3-billion namespace, 1,800 episodes. Fixed tau_q=.2 and residual-diversity thresholds. Explicit QLSR cosine teacher follows T011 equation; historical O1 teacher is unnormalized dot product and S1 remains unchanged. Baseline focused tests: 16 passed in 12.33s. Next: modular residual implementation and required CPU/CUDA validation. No T011 outcomes yet.
