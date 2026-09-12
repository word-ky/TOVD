# TOVD project state

T001-T008 accepted. T009 VERIFIED; A PASS / B PASS; awaiting Research Lead review.
Research b9973b9/e6eb2c0; preregistration 1b63bf6; tested 3e56b0cca890ea83873e48ee68f69593b78af9b7.
Pure local frozen-log audit completed: 54 hashed T008 records, 27 unique states, 5400 episodes /43200 queries.
No GPU/model rerun/training. 90 local tests pass. Historical NLL delta max error5.712e-7, accuracy exact, query harm signs exact; features repeat exactly.
Passing post-candidate scalars delta_entropy, delta_max_probability, delta_probability_gap. None pre-update.
Best delta_entropy mean overallLOSO .750696/min .722485; easymean .850020/min .770398. Oracle B passes all clauses.
Read research_log/t009/RESULTS.md and coordination/CODEX_TO_CHATGPT.md; all result CSV/JSON and plot artifacts under research_log/t009.
Recommend separate preregistered T010 query-level rollback/output fusion, but do not implement before lead task.
No active experiment. Do not repeat VERIFIED T009 just because inbox remains ACTIVE. Heartbeat every15min, quiet if unchanged.
