# T010 preregistration — base-calibrated query entropy rollback

Research instruction 45f6045. Commit this plan/config/sources before any fresh outcomes.
Two separate executions: calibration only, then commit actual thresholds before generating/scoring novel validation. No model training or intermediate checkpoint selection.

## Frozen sources and streams

sources.json lists SHA256 for nine checkpoints: original T002-P and T007 W1/W2 step400, seeds7/17/27. It hashes all tovd Python source including generator/model/C2 code. All must match before execution. Checkpoint receipts already verified at preparation.
Unchanged world/model config copied from T008: dim16,12x10 classes, base clusters0..7/classes0..79, novel clusters8..11/classes80..119, vocab4,queries8, X16 foreground+8distractor+8background, world seed20260912. O1+C2 controller and temperatures unchanged.

Fresh RNG IDs = namespace + model_seed*100000 + regime_offset + index.
Calibration namespace1000000000, split=train, easy offset0/hard10000, indices0..99 per state/regime.
Validation namespace2000000000, split=test, same offsets, indices0..199 per state/regime.
Branches at the same model seed share episodes for paired comparisons; regimes use distinct IDs.
Counts: calibration1800 state-episodes/14400 queries; validation3600 state-episodes/28800 queries.
LOSO calibration per held seed uses1200 episodes/9600 queries from other two model seeds. Validation held seed uses1200 episodes/9600 queries from all three state groups and both regimes.
sources.json explicitly lists600 unique calibration RNG IDs and1200 unique validation IDs, disjoint from each other and every stored historical episode_seed (960 distinct IDs, maximum20270099). Prior benchmark namespace formula uses train10M/test20M/mechanism30M plus seed*10000+index (through continuation3199/mechanism19), also disjoint. T009 reused those historical streams only.
No intermediate-state secondary experiment. No episode bootstrap/inferential CIs.

## Policy, candidate grid and calibration

Use stored float32 p0/pC2 values converted to Python float; H(p)=-sum p log(max(p,1e-12)), same as T009. dH=H(pC2)-H(p0). No other feature used.
Retain C2 iff dH<=tau, else select W0. Hard selection of both probability vector and its corresponding token; no blending. Ties at threshold keep C2.
For each held seed pool only other-two-seed calibration dH across three states/easy/hard. Candidate grid: linear-interpolated empirical quantiles at0,.01,...,1, unique sorted, plus negative/positive infinity (serialized as strings "-inf"/"+inf"). No labels in grid construction.
Use base calibration labels offline to minimize mean per-query NLL, -log(max(selected_probability[y],1e-12)). All queries have equal weight (equal episode/query counts also ensure equal state/seed/regime weight).
Tie-break: candidates within1e-12 of global minimum calibration mean NLL are tied; choose numerically smallest tau (more rollback). Orientation always increasing dH->harm. One tau per held seed, unchanged across all states/regimes.
Write candidate losses, selected thresholds, calibration membership/counts and input hashes. Fetch and commit actual thresholds plus calibration receipts before validation execution; do not use held seed's calibration rows in its tau.

## Validation order and baselines

Validate only after thresholds are committed. Generate fresh novel episodes, compute normal W0 and unchanged C2 candidate; entropy decisions and selected output/token need no labels. Labels are consumed only afterward for scoring/calibration-independent diagnostics.
R0 W0, R1 always-C2, R2 calibrated selection, R3 fixedtau0, ORACLE lower true-query-NLL selection (W0 on ties). R0/R1 use the same direct model paths as historical code. Score each probability output identically; verify probability-log NLL against normal fused cross-entropy within2e-6; accuracy exact.
Record p0/pC2, tokens0/C2, entropy deltas, decisions, selected R2/R3 tokens/probabilities, labels/IDs only in audit metadata, all candidate diagnostics, and per-query metrics. Check selection before/after oracle scoring identical, candidate rerun deterministic and model parameters unchanged. Confirm selected-token classification agrees with selected probabilities (rtol0,atol2e-6).
Each episode begins from W0; no retained fast state. Existing regression covers vocabulary response and outer differentiability. No outer optimization here.

## Metrics and fixed success clauses

Aggregate per episode then equally across seeds/states; report all18 heldseed/state/regime cells plus seed overall and state-group easy/hard. NLL/accuracy for all5 baselines, retention for R2/R3, and for each policy gains-retained (W0wrong/C2correct kept) and damages-rolled-back (W0correct/C2wrong rejected). Report counts and fractions; zero denominator ->null. Oracle-headroom fraction=(R1 metric-policy metric)/(R1 metric-oracle metric), reverse sign for accuracy; zero headroom ->null. Do not clip negative/>1 values.

Gate1 each held seed: R2 mean NLL <R0 and <=R1+.01; R2accuracy>=min(R0accuracy,R1accuracy).
Gate2 each state group's hard aggregate: if R1 improves NLL, R2 retains>=75% of its improvement; if R1 improves accuracy, retain>=70%. Otherwise R2 NLL<=R0+.01 and accuracy>=R0-.01.
Gate3 every heldseed/state easy cell: if R1 worsens NLL, remove>=60% of regression; if R1 worsens accuracy, remove>=50%. Apply regression clauses independently per metric. Where R1 improves NLL, require retention>=50% OR R2 NLL<=R0+.01. Exact NLL tie: require R2<=R0+.01 (same no-material-degradation interpretation). No additional easy accuracy-gain requirement beyond task.
Gate4 each seed R2 retention in [.10,.90] inclusive; thus both outputs used.
Gate5 verify fixed source hashes, disjoint RNG membership, actual thresholds committed before validation, calibration membership excludes held seed, no validation label in thresholds/selection. No post-outcome change to any policy, seed, threshold or gate.
All5 must pass. If any fail, recommend terminating the current O1+C2 rollback line; no rescue fitting. If all pass, request lead review for a separate small integration task, never implement it autonomously.

## Implementation/reuse and validation

Reuse unchanged EpisodicClassifier/O1StepMemory, SemanticWorld, T007 load_model/tensor equality, T008 compare_memory and T009 entropy/offline NLL conventions; implement only threshold calibration/selection, fresh runner and summary/gates in research_log/t010.
First focused baseline C2/feature tests; increment1 pure scalar calibration/selection tests (ties/LOSO/validation labels); increment2 model fresh runner/synthetic E2E and gate arithmetic. Full local plus A6000 CPU/CUDA suites before calibration. No repeated full tests for receipt-only edits between phases.
Deploy calibration release, run GPU1 via existing AutoDL workflow, fetch and commit thresholds/receipts, then deploy validation release and execute unchanged tested runner. Explicit run IDs, configs, revisions and environment saved under project research_log; all original artifacts retained and recovery mirrored to remote project.
