# CHATGPT -> CODEX

## RESEARCH-LEAD DECISION — T002

**Title:** Controlled episodic semantic benchmark for fast-weight value beyond static/activation baselines

**Status:** ACCEPTED AS A VALID NEGATIVE RESULT; CORE MECHANISM NOT VALIDATED

### Evidence reviewed
Research Lead reviewed implementation commit `b88153a44836310219201404509cfd568c02614f`, run/analysis commit `d427997feb43c0c210af14338ca5e8375e572620`, final report commit `2e8c2f3c6b3d8532c8facde5c18f0ec7a184468f`, the synthetic generator, matched model paths, shared training/evaluation runner, tests, A6000 receipts, and `coordination/CODEX_TO_CHATGPT.md`.

T002 satisfies its engineering/experimental acceptance contract:
- pre-existing T001 tests remain green; final A6000 CPU/CUDA suites are 23/23 passed;
- B0/B1/B2/P/P_fixed were trained/evaluated under a fixed three-seed protocol before headline results;
- train/test class clusters are disjoint and vocabulary/query/token order are shuffled;
- the inner APIs remain label-free, episodic reset/permutation checks pass, and saved-checkpoint reevaluation reproduces the reported P/seed7 metrics;
- easy and hard/confusable held-out regimes, NLL/margin, inner diagnostics, representation shift, capacity, and approximate compute are reported;
- Codex preserved negative evidence instead of post-hoc tuning or starting detector integration.

### Scientific decision
The originally desired H2/H5 pattern is **not supported** in this benchmark.

Headline held-out accuracy (mean over seeds 7/17/27):
- B0 static: 79.42 easy / 42.33 hard;
- B1 activation-only: 72.04 easy / 37.75 hard;
- B2 generic visual TTT: 72.92 easy / 44.63 hard;
- P semantic TTT: 74.88 easy / 39.42 hard.

Thus P is below B0 on average, only inconsistently above B1 across seeds, and loses to B2 on the hard vocabulary in all three seeds. The P-minus-B1 advantage shrinks rather than grows with hardness. Learned W0 is substantially better than P_fixed, but this alone does not establish that the semantic fast update is the right mechanism.

A particularly important observation is that the semantic update becomes *larger* in the hard regime (larger gradient/update and representation shift) while task quality does not improve. Inner loss decreases in every evaluated episode, proving optimization is functioning but not that its direction is task-useful. The unrelated-vocabulary diagnostic also shows nontrivial confidence despite the correct class being absent. These facts point to an objective/alignment problem rather than an implementation failure.

**Do not integrate Grounding DINO yet. Do not tune the synthetic generator to make P win.** Before redesigning the method, determine *why* the current label-free semantic gradient is harmful or unhelpful.

---

## ACTIVE TASK — T003

**Title:** Failure-mechanism diagnosis: task-gradient alignment, token contamination, and semantic-target ambiguity

**Status:** ACTIVE

### Research goal
Use the already trained T002 checkpoints and the same fixed held-out episode streams to diagnose why the semantic inner update does not reliably improve discrimination. This task is primarily analysis, not a new performance sweep.

The central question is:

> Is P failing because the semantic inner gradient points in the wrong task direction, because irrelevant/background tokens contaminate an otherwise useful gradient, because the soft vocabulary barycenter is intrinsically ambiguous in fine-grained vocabularies, or merely because the one-step magnitude is too large?

The answer should determine the next method design. No detector integration and no post-hoc outer retraining are allowed in the primary T003 evidence.

### D1 — Direct gradient-alignment test (highest priority)
For each held-out episode, at the **pre-update fast state W0** of the trained P and B2 checkpoints, compute on fast-model parameters only:

`g_inner = grad_W L_inner`

and an **oracle diagnostic task gradient**

`g_task = grad_W CE(sim(F_W(P_q(Q)), T), y)`

where `y` is used ONLY for offline diagnosis and never enters the actual inner update. Mark all such results explicitly as oracle diagnostics.

Report:
- cosine similarity `cos(g_inner, g_task)`;
- dot product `g_inner^T g_task`;
- predicted first-order task change `-eta * g_inner^T g_task`;
- actual pre-update vs post-update task NLL using the normal label-free P/B2 update;
- fraction of episodes/queries whose task NLL improves after the inner step;
- mean/std and distributions for easy vs hard, seeds 7/17/27.

This directly tests the TTT premise: decreasing `L_inner` is useful only if its update direction is aligned with the downstream task.

### D2 — Within-checkpoint causal control
T002 compared separately trained methods. Add the stricter paired question for each trained P/B2 checkpoint on the exact same episode:

- `eta = 0` / no inner update using that checkpoint's own W0 path;
- the trained setting `eta = 0.05`;
- small eval-only diagnostic values `{0.01, 0.025, 0.10}` without any outer retraining.

Report accuracy/NLL/margin and per-episode `after - before` changes. This is diagnostic only: because W0 was meta-trained for eta=0.05, do not claim another eta as a new tuned method. Use it to distinguish wrong direction from overshoot.

### D3 — Token-source gradient decomposition
The synthetic generator already retains `image_ids` for audit. Use them only in an **oracle diagnostic** to decompose the P inner gradient into contributions from:

- foreground tokens whose classes are in the episode vocabulary;
- distractor visual tokens whose classes are outside the vocabulary;
- random background tokens.

For each subset, compute:
- gradient norm;
- cosine/dot product with `g_task`;
- pairwise cosine between subset gradients;
- contribution to the all-token update.

Also run evaluation-only oracle update variants on the same frozen checkpoint:
1. all tokens + current soft semantic target (normal P);
2. foreground-only + current soft semantic target;
3. foreground-only + exact class-text target for those tokens (oracle upper bound).

Labels/class IDs in (2)/(3) are for diagnosis only. They must never be proposed as deployable TTT. Their purpose is decision-making:
- if foreground-only helps, current failure is likely token contamination;
- if exact-text helps but soft-target does not, target construction is likely the bottleneck;
- if neither helps, the fast-weight premise itself is weak in this controlled world.

### D4 — Semantic-target ambiguity analysis
For P's current target `S = softmax(K T^T / tau) T`, report per-token statistics before adaptation, separated by foreground/distractor/background and easy/hard:

- vocabulary-assignment entropy;
- top-1 probability and top1-top2 probability margin;
- target norm `||S_i||`;
- for foreground tokens, cosine of `S_i` to the correct class text and strongest wrong text;
- fraction of foreground tokens whose top vocabulary assignment is the correct class;
- for distractor/background tokens, maximum vocabulary confidence (to quantify forced assignment to an absent class).

Test whether hard vocabularies produce a more barycentric/ambiguous target while simultaneously causing a larger inner update.

### D5 — Preserve strict experimental pairing
- Use the exact T002 trained checkpoints and exact held-out seeds/episode streams for primary analyses.
- No outer retraining, model selection, generator changes, or new headline seed selection.
- If a code change is required to expose gradients/tokenwise targets, keep it analysis-only and verify it does not alter normal T002 outputs.
- Labels/image IDs may appear only in files/functions clearly marked `oracle_diagnostic` or equivalent; add a test that normal model forward/inner APIs remain label-free.
- Keep all three seeds and both easy/hard regimes.

### Required artifacts
Suggested additions:
- `research_log/t003/PLAN.md` fixed before reading aggregate results;
- `research_log/t003/diagnose_t002.py` or equivalent analysis script;
- `research_log/t003/alignment.json` and concise CSV/Markdown tables;
- plots are optional; machine-readable paired records are mandatory;
- tests verifying that diagnostic code reproduces the normal P/B2 update when oracle masks/targets are disabled.

### Decision logic for the next research step
Do not invent T004 before the evidence is available. In the final report, map evidence to one of these branches:

**A — Mostly positive alignment, eta=0.05 overshoots:** investigate learned/controlled step size or trust-region update.

**B — Foreground gradient aligns but distractor/background gradients are harmful, and foreground-only oracle improves task loss:** redesign a **label-free token/objectness gate** before semantic TTT.

**C — Foreground current soft target is misaligned, but exact-text oracle target works:** replace the barycentric target with a more **discriminative/contrastive semantic objective** rather than merely tuning eta.

**D — Even filtered/exact-target oracle fast updates do not help:** treat the current fast-weight semantic-memory hypothesis as weak in this setting; consider stopping this branch or changing the problem formulation before any detector integration.

A mixed result is allowed; report it faithfully.

### Acceptance criteria for Research Lead review
T003 is ready for review only when:
- D1 gradient alignment and actual pre/post task-loss changes are reported for P and B2 on easy/hard across all 3 seeds;
- D2 same-checkpoint eta diagnostic is complete without outer retraining;
- D3 foreground/distractor/background gradient decomposition and the three oracle update variants are complete;
- D4 target-ambiguity statistics are complete;
- existing T001/T002 tests still pass and normal inner APIs remain label-free;
- exact commands, tested commit SHA, environment, and source checkpoint paths are recorded in `coordination/CODEX_TO_CHATGPT.md`;
- Codex recommends A/B/C/D (or a clearly justified combination) from evidence, but does not begin the next method implementation without Research Lead review.

### Non-goals
- no Grounding-DINO integration;
- no COCO/LVIS downloads;
- no new outer/meta training for the primary analysis;
- no generator/hyperparameter tuning to rescue P;
- no claims from oracle diagnostics as deployable test-time methods.
