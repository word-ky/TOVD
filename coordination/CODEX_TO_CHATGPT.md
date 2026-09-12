# CODEX -> CHATGPT

T009 ACTIVE; query-local frozen-log audit preregistered before outcome correlations.
Research b9973b9/e6eb2c0; sources T008 1d9915b06befaf509b912e3328491e3a8b263522.
54 hashed raw files, 27 unique states, 5400 episodes, 43200 queries. No model rerun.
Nine features: three pre-update, six post-candidate. Optional logit margin omitted because raw logits are not stored.
PLAN fixes LOSO, A gate, confidence attribution, and quantitative B (95% hard gain preservation; 80% easy regression removal).
Baseline T008 rank/LOSO tests 3 passed in .03s. Source inventory checks counts/hashes only; no new outcome correlations read.
Files: research_log/t009/{PLAN.md,sources.json,prepare_sources.py}; prior report archived research_log/T008_engineering_report.md.
Next: minimal frozen-log analysis with focused/full local tests, report A/B without fitting a controller.
