# T011 preregistration: query-local semantic residual

2026-09-12. Research instruction 77487b7 / 617fbdf. Exploratory structural screen, no T011 outcomes observed. T010 is accepted negative and its calibrated-rollback line is terminated.

## Frozen inputs and stream

The nine exact checkpoint paths/SHA256 values are fixed in `sources.json`: seeds 7/17/27, original T002 P, T007 W1 and W2 step400. All nine local files match their hashes. Reuse unchanged generator/world/model settings in `config.json`. No outer training or checkpoint selection.

Use novel (`test`) semantics as an exploratory development stream, 100 easy and 100 hard episodes per checkpoint: 1,800 episodes / 14,400 queries. RNG seed = 3,000,000,000 + seed * 100,000 + (10,000 if hard else 0) + index, index 0..99. The 600 unique scene seeds are paired across the three states. This namespace exceeds the old T002–T009 formulas and both T010 namespaces (1 billion calibration, 2 billion validation); explicit prior/fresh IDs are in the manifest. No scene generation or outcomes before this commit. Unit fixtures use random models, not the nine scientific checkpoints.

## Exact mechanism

Frozen k=P_k(X), q=P_q(Q), z0=F_W0(q). QLSR normalizes k, q and T along the feature dimension with PyTorch F.normalize eps=1e-12. Teacher pi=softmax(cos(k,T)/0.2). Attention a=softmax(cos(q,k)/0.2) over image tokens. pi_bar=a @ pi. Student logits=cos(z0+r,T)/0.1. Local loss is class-summed cross entropy for each query separately. The gradient of the SUM of independent query losses gives each residual its unscaled local gradient (no division by query count).

Normalization clarification identified before implementation: historical O1 uses projected-key dot text for its teacher (keys are not normalized). The new task explicitly specifies cosine for QLSR. S2/S3 implement that explicit cosine equation; S1 preserves historical O1 exactly. O1 temperature 0.2 and normalized student temperature 0.1 are reused. This is disclosed rather than silently changing the S1 control.

Each r is freshly allocated exact zero. Adapt only r with one gradient evaluated at zero. For each query independently, choose the first eta in [.05,.025,.0125,.00625,.003125] satisfying finite loss_after <= loss_before - 1e-4 * eta * ||gradient||^2. If none passes, eta=0 and exact-zero residual. Selection uses only local inner losses, never task labels/IDs. Output z0+r. No slow gradient, shared fast-model update, selector, blending, learned controller, training or state persistence in S2/S3.

Controls on identical scenes: S0 unchanged W0; S1 unchanged global O1+C2; S2 QLSR; S3 identical residual update with uniform a=1/N. Runtime functions accept only model, X,T,Q and the fixed constants/control. Task labels are accessed only after all four outputs and audits have been computed.

## Diagnostics and operational definitions

Retain raw tokens, probabilities, teachers, attention, residuals and per-query before/after loss, gradient norm, chosen eta, trial count, acceptance, Armijo RHS, residual norm and norm/(||z0||+1e-12), attention entropy (natural log), exp(entropy) effective token count, finite/zero-init checks. Store pairwise residual cosine matrix for every S2/S3 episode and mean off-diagonal cosine distance over pairs where both norms >1e-12 (diversity=0 when fewer than two qualify; report eligible-pair counts). Mean episode diversity gives equal weight to the full fixed grid, including zero-diversity episodes.

Preregistered material locality: S2 mean residual diversity >0.001 AND S2 minus S3 mean diversity >=0.01. These are fixed descriptive effect-size thresholds, not values chosen from outcomes. Report per-cell diversity and query-teacher diversity as well, without replacing the primary residual statistic.

For every episode, vocabulary perturbation replaces each novel class id v by 80+((v-80+1) mod 40), using actual fixed-world text embeddings. Fixed X/Q; IDs used only by the external audit to construct T_alt. Record per-query ||r(T)-r(T_alt)||. Every accepted S2 query must have nonzero finite residual and vocabulary difference >1e-8. Record rejected queries separately.

Replay S2/S3 after alternate vocabulary, alternate image (reverse token order) and changed other queries at the same shapes; original output/residual must reset bitwise exactly. Per-query isolation changes all other Q rows while preserving the audited row and verifies that row bitwise. Zero initialization is recorded for every query. Save source checkpoint/model-tensor byte equality, all finite checks, S0/S1 repeated output/state equivalence and code SHA256. No outer optimizer exists here; existing meta-gradient regressions remain in the full suite.

## Five fixed interpretation criteria

All must pass to recommend T012; engineering validity is reported separately.

1. Mechanism locality: all accepted S2 residuals nonzero/finite, exact zero-init/reset/isolation, vocabulary sensitivity above, nontrivial residual diversity and S2-S3 excess above.
2. Hard utility: in EACH original/W1/W2 group, S2 hard NLL < S0; where S1 improves S0 retain >=70% of that NLL gain; S2 hard accuracy >= S0-0.01.
3. Cross-seed: in EACH group at least 2/3 seeds improve hard NLL over S0 and no seed regresses by >0.03.
4. Easy safety: in EACH seed/state easy cell where S1 NLL>S0, (S1-S2)/(S1-S0)>=0.60. Else S2 NLL<=S0+0.02 and accuracy>=S0-0.01. Equality of S1 and S0 follows the latter rule.
5. Localization: pooled hard S2 NLL<S3 and pooled easy S2 NLL<=S3+0.01.

NLL and accuracy are query means, balanced across the fixed grid. Gain-retention fractions are only evaluated with positive denominator. No detector claims. If any criterion fails, recommend terminating the current synthetic fast-semantic-state program and returning to a static/activation-side OVD formulation. If all pass, stop for Research Lead review and a separately preregistered fresh T012. No automatic successor or rescue.

## Reuse and implementation increments

Repository baseline 77487b7, existing source/checkpoint provenance retained. Reuse SemanticWorld, EpisodicClassifier/load_model, score_output, C2 Armijo constants/choose_armijo_step and JSON/CSV helpers. No external code copied. Baseline `python -m pytest -q tests/test_step_control.py tests/test_query_rollback.py`: 16 passed in 12.33s, local Python 3.12.7 / Torch 2.13.0+cpu.

1. New `tovd/models/query_local_residual.py` plus focused teacher, isolation, zero-init/reset, vocabulary, exact Armijo and immutability tests. No edits to accepted model paths. Run focused tests before increment 2.
2. Task-local runner/summary and miniature random-checkpoint end-to-end + arithmetic/no-label tests; preserve generator/scoring. Run focused tests then full local regression.
3. Commit tested implementation/hash manifest, deploy via AutoDL scripts, full A6000 CPU and CUDA suites before actual screen. Persist exact run IDs, environment, commands, code/source hashes and raw per-query evidence; report all five criteria without post-outcome changes.
