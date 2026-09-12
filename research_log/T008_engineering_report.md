# CODEX -> CHATGPT

## T008 — VERIFIED; no preregistered scalar passes

Engineering validity PASS; scientific interpretation gate FAIL for all 14 features.
Recommend stopping/reframing the always-on fast-weight branch before detector integration.
This finding concerns the fixed T008 scalar set/state grid, not all possible harm predictors.
Await Research Lead review; no T009/controller/detector implementation.

### Revision and run

- Research instructions: 2008520/c6593b7; preregistration: c163c78.
- Tested implementation: `153ac30d00753b43a56ce2e226068b0c35039d70`; dispatch: fce7541.
- Final evidence: the commit containing this report (`git log -1 -- coordination/CODEX_TO_CHATGPT.md`).
- Release: 20260912-101316-tovd-t008; run: `20260912-101332-tovd-t008-a6000`.
- A6000 physical GPU 1, project `/home/wenchang/asdasdsad/wjq/TOVD`.
- Run exited 0 at 2026-09-12 10:20:21 +08; original receipts retained locally and remotely.

### Controlled implementation and scope

33 frozen states: original T002-P plus both T007 branches at 0/50/100/200/400, seeds 7/17/27.
Exact original 100 easy + 100 hard episodes per state, 6600 rows. Primary analysis uses 5400 unique-state rows to avoid tripling the identical original/W1-step0/W2-step0 states. Full-grid weighting sensitivity and complete branch trajectories remain reported.

Seven pre-update and seven post-candidate scalars accept model/X/T/Q only. Offline labels are scored afterward. Features, normal output/fast state and model parameters are compared around oracle logging. No training, checkpoint selection, altered C2 candidates, eta tuning, learned policy or runtime/model/generator modification.

Before correlations, PLAN fixed tied-rank Spearman/AUROC, training-seed-only scalar orientation, primary harm Delta_NLL > 0 and sensitivity > .05. Overall gate is mean LOSO >= .70 and every fold >= .65. Same orientation must transfer across folds/W1/W2; within-easy nontriviality was operationalized as mean >= .65, every fold >= .60 and oriented branch AUROCs > .5. All 14 already fail the original overall gate, independently of these additional within-easy details. Optional T006 secondary states omitted.

### Results

- Passing pre-update features: **none**. Passing post-candidate/rollback features: **none**.
- Best overall: post-candidate relative_inner_reduction, mean LOSO **.580556**, folds **.638526 / .612029 / .491113**. Easy mean .569577, minimum .474927.
- Best pre-update: gradient_norm, mean **.538529**, minimum .408670. It requires an inner backward pass even though no update is applied.
- Delta_NLL > .05 sensitivity: best mean overall LOSO .559274 (relative_inner_reduction).
- Easy-only descriptive probability-gap AUROC .711724 and max-probability AUROC .704789 do not establish transferable prediction: pooled-training fold signs are [+1,+1,-1]. Gap easy fold AUROCs are .738984/.689356/.278598. No held-out reorientation or easy-only rescue was fitted.
- Harm prevalence: 2235/5400 overall; easy 1087/2700; hard 1148/2700. No exactly neutral episodes.

Sign-flip map: W1 easy seeds 7/17 change from beneficial original means to harmful step-400 Delta_NLL +.365164/+.277746. Seed 27 original is already harmful (+.131193), and W2 seed 27 stays harmful at every saved step. All 33 hard state means remain beneficial; individual hard episodes can still be harmed.

Easy harm has more confident W0 (max probability .886158 vs .814840), slightly larger normalized updates (.023671 vs .021180) and representation shifts (.477821 vs .431671). However, it has smaller predictive JS (.079785 vs .090923), fewer changed predictions (.191927 vs .269141) and smaller relative inner descent (.108913 vs .126109). Thus confident-state overspecialization is only a partial qualitative account, not a validated scalar rule. Full per-seed/branch/state Spearman/AUROC, direction consistency, localization quartiles and all 14 gates are included in the report and CSVs.

### Verification and diagnostics

- All 33 checkpoint hashes match; 6600/6600 rows, 66 raw record files, 76 original run files with manifest hashes.
- T005 and every T007 checkpoint's historical metrics replay with maximum error 0; episode stream mismatches 0.
- Normal versus oracle-on/off output and fast state are bitwise equal; repeated feature values exact.
- Output/state/pre-inner-loss/pre-gradient comparison errors all 0. No nonfinite features; all outputs finite; slow/model parameters unchanged.
- Inner loss before/after, gradient norm, update norm, eta/trials and outputs remain in original per-episode records. Episodic reset and vocabulary/outer-gradient mechanisms remain covered by the unchanged regression suite; no outer training performed in T008.

Tests: baseline 79 passed (37.15s). Initial two feature fixture tests failed because WorldConfig was omitted; only fixtures repaired, then 2 passed (8.37s). Focused statistics/features 5 passed (12.02s); artificial-source end-to-end/statistics 4 passed (13.92s). Full local 85 passed (25.12s). Remote CPU 85 passed (8.88s), CUDA 85 passed (24.10s). Existing protobuf/NVML warnings only; PyTorch CUDA works. No driver changes.

Remote environment: Python 3.12.12, torch 2.4.0+cu121, CUDA 12.1, pytest 9.1.1, RTX A6000. Local Python 3.12.7, torch 2.13.0+cpu, pytest 9.1.1; report matplotlib 3.9.2. GPU 1, CUBLAS_WORKSPACE_CONFIG=:4096:8, OMP/MKL threads 1. No experimental code changed after tested revision; final changes format reports/plots/logs only. All three figures visually inspected; corrected an overlapping legend. `git diff --check` passes.

### Exact commands and files

```text
python -m pytest -q
autodl-deploy.ps1 -Tag tovd-t008 -Source D:\work\fightccfa-agin\CVPR2027\TTT-OVD
autodl-run.ps1 -Name tovd-t008-a6000 -Cmd 'export TOVD_SOURCE_REVISION=153ac30d00753b43a56ce2e226068b0c35039d70; bash scripts/run_t008_a6000.sh'
python -m research_log.t008.write_report --run D:\work\fightccfa-agin\CVPR2027\TTT-OVD\research_log\remote_runs\20260912-101332-tovd-t008-a6000
```

The committed scripts/run_t008_a6000.sh and original run.sh/train.log provide the complete audit CLI and CPU/CUDA test commands. It resolves all source checkpoints from existing remote runs; frozen protocol/config and seeds are in sources.json/config.json.

Implementation files: research_log/t008/{PLAN.md,config.json,sources.json,schema.py,runtime_features.py,statistics.py,audit.py}; tests/test_safety_{features,statistics,audit}.py; scripts/run_t008_a6000.sh.
Report files: research_log/t008/{write_report.py,RESULTS.md,results.json,gates.json,checks.json,schema.json,verification.json,receipt_summary.txt,progress.md}; episodes/single_features/sign_map/gates/loso/localization/direction_consistency CSVs; sign_map/feature_geometry/loso_auroc PNG/SVGs. Complete original run is research_log/remote_runs/20260912-101332-tovd-t008-a6000/. Project state, REMOTE and session logs updated; prior report archived research_log/T007_engineering_report.md.

No execution blocker remains. Scientific uncertainty: only three seeds and reused episodes/states; no independent-row p-values or confidence intervals. Research Lead should review this negative result and decide how to stop/reframe; the current evidence does not justify a selective-C2 T009.
