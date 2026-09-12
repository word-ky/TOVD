# CODEX -> CHATGPT

T009 IMPLEMENTED; frozen-log analysis ready. Research b9973b9/e6eb2c0; preregistration 1b63bf6.
Source T008 1d9915b06befaf509b912e3328491e3a8b263522; 54 hashed files/5400 episodes/43200 queries.
Implementation files research_log/t009/{query_analysis.py,audit.py}; tests/test_query_audit.py.
Reuse unchanged T008 AUROC/Spearman/LOSO; no model rerun. All nine features accept probabilities/tokens only; labels enter afterward.
Baseline3 tests pass. Increment1 two equation/aggregation tests pass; raw schema inspection corrected initial batched-label assumption to stored flat labels and reran green. Increment2 eight tests pass .87s including synthetic full analysis/repeat. Full python -m pytest -q:90 passed26.18s.
PLAN fixes A gate and B quantitative thresholds; no real query correlations read yet.
Next execute python -m research_log.t009.audit --revision <implementation SHA> --output research_log/t009/results, format complete results and report A/B.
No model/training/controller/detector change. Report-only CPU analysis; no A6000 experiment needed.
