# CODEX -> CHATGPT

## T008 — IMPLEMENTED; fixed A6000 audit running

Research2008520/c6593b7; preregistrationc163c78; tested code
`153ac30d00753b43a56ce2e226068b0c35039d70`.
Release20260912-101316-tovd-t008; run20260912-101332-tovd-t008-a6000 on physicalGPU1.

Existing runtime/model/generator files unchanged. New task-local runtime_features.py
accepts model/X/T/Q only and separates7 pre-update from7 post-candidate scalars;
schema.py explicitly marks predictors. audit.py computes labels/outcomes afterward,
replays normal/oracle-off/on extraction and verifies historical metrics/IDs/hashes.
statistics.py implements average-tie Spearman/AUROC, LOSO scalar orientation,
branch/state direction diagnostics and the precommitted interpretation gate.
No learned policy, training, feature thresholds or new checkpoint selection.

Sources:33 byte-verified committed checkpoint files. Complete6600-row grid retained;
primary5400 unique-state rows avoid counting original/W1step0/W2step0 three times.
Full-grid duplicate-weight sensitivity also reported. W1/W2 descriptions retain0..400.
All100easy+100hard original test episodes perstate, seeds7/17/27.

Gate operationalization in PLAN before correlations: mean overallLOSO>=.70,
eachfold>=.65; same fold orientation and oriented W1/W2 AUROC>.5 overall/within-easy;
within-easy meanLOSO>=.65,each>=.60 using same orientation trained on other2seeds.
All14 scalars and Delta_NLL>.05 sensitivity reported; no post-outcome adjustment.
Post-candidate pass could only motivate future rollback design, not pre-update gating.

Validation:
- Baseline79 passed37.15s.
- Feature fixtures initially failed2 tests for omitted required WorldConfig argument;
  repaired fixture only;2 passed8.37s.
- Statistics/features5 passed12.02s.
- Artificial-source end-to-end/statistics4 passed13.92s.
- Full local `python -m pytest -q`:85 passed25.12s; diff check passes.
- Remote fullCPU/CUDA suites execute before audit; outcomes pending.

Files: research_log/t008/{PLAN.md,config.json,sources.json,runtime_features.py,
schema.py,statistics.py,audit.py,progress.md}; tests/test_safety_{features,statistics,audit}.py;
scripts/run_t008_a6000.sh. Prior report archived research_log/T007_engineering_report.md.

Command: `export TOVD_SOURCE_REVISION=153ac30d00753b43a56ce2e226068b0c35039d70; bash scripts/run_t008_a6000.sh`.
Remote project /home/wenchang/asdasdsad/wjq/TOVD; explicit run artifacts at runs/<id>/artifacts/t008.
Existing NVML warning persists; PyTorchCUDAworks, no driver changes. Both GPUs idle beforedispatch.
No experimental feature/outcome correlations read yet. Await completion; no T009/detector.
