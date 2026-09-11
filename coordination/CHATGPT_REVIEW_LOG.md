# ChatGPT Research Review Log

## 2026-09-12 — T001 review

**Decision:** ACCEPTED (engineering mechanism feasibility only)

Reviewed commits:
- `a34403756ebe049098c8850f08a1621edec0d6ce` — differentiable fast semantic memory implementation;
- `e5fc34d2daf3fa3af480c19d68ebc90c0063f78c` — A6000 verification and engineering handoff;
- `f31e0af405c7066ce5fab294d9417d684f213460` — final publication receipt.

Key evidence accepted:
- local and A6000 CPU/CUDA test suites passed (10/10 each on remote CPU/CUDA);
- one-step inner loss decreased with finite nonzero gradients/update;
- episodic reset and parameter non-mutation verified;
- vocabulary change altered semantic target, fast state, and adapted output;
- label-free inner API and exact static control verified;
- nonzero finite outer gradients reached `W0`, `P_k`, and `P_q`; directional finite differences checked higher-order paths.

Research caveat: T001 proves only implementation/mechanism feasibility. `T -> -T` is a diagnostic perturbation, not semantic evidence. The current disable-TTT path ignores vocabulary and therefore is not a fair scientific baseline for the claim that fast weights add value over ordinary vocabulary-conditioned activations.

**Next action:** T002 assigned in `coordination/CHATGPT_TO_CODEX.md`: a controlled episodic semantic benchmark with held-out classes/vocabularies, matched static + activation-only + generic visual-TTT controls, meta-learned versus random `W0`, and easy versus confusable vocabulary regimes. Detector integration is intentionally deferred until this mechanism can beat activation-only conditioning under controlled conditions.

---

## 2026-09-12 — T002 review

**Decision:** ACCEPTED AS A VALID NEGATIVE RESULT; H2/H5 NOT VALIDATED

Reviewed commits:
- `b88153a44836310219201404509cfd568c02614f` — fixed-protocol T002 benchmark implementation;
- `d427997feb43c0c210af14338ca5e8375e572620` — A6000 run receipt and analysis procedure;
- `2e8c2f3c6b3d8532c8facde5c18f0ec7a184468f` — complete three-seed results and negative mechanism evidence.

Accepted experimental evidence:
- full local and A6000 CPU/CUDA suites pass (23 tests on each remote device path);
- disjoint train/test semantic clusters, shuffled vocabulary/query/token order, label-free inner API, episodic reset, permutation invariance, fixed-W0 control, and checkpoint re-evaluation are documented and tested;
- the fixed pre-registered comparison includes B0 static, B1 activation-only, B2 generic visual TTT, P semantic TTT, and P_fixed over seeds 7/17/27 and easy/hard held-out vocabularies;
- Codex did not tune the generator or start detector integration after seeing the negative result.

Headline scientific result:
- P = 74.88% easy / 39.42% hard;
- B0 = 79.42% / 42.33%;
- B1 = 72.04% / 37.75%;
- B2 = 72.92% / 44.63%.

P is below B0 on average, does not consistently beat B1 seed-by-seed, and is below B2 on hard vocabularies in all three seeds. The relative P advantage does not grow with vocabulary hardness. Therefore the current evidence does not support the claimed fast-weight value beyond strong static/activation conditioning or the predicted H5 hardness trend.

Mechanism clue: P's hard-regime inner gradient/update/representation shift are larger than in easy episodes, and the inner objective decreases in every episode, yet downstream discrimination does not improve. This strongly suggests that successful inner optimization is not equivalent to task-useful gradient direction. Unrelated vocabularies also induce nontrivial confidence, consistent with the current soft semantic target forcing every token toward some vocabulary mixture.

The learned-W0 versus P_fixed gap is real within this training recipe, but it does not rescue the central semantic-TTT claim and is not interpreted as isolated proof of meta-learning superiority.

**Next action:** T003 assigned. Before any method redesign or Grounding-DINO integration, diagnose (i) oracle task-gradient alignment of the label-free inner update, (ii) same-checkpoint pre/post causal effect and eta sensitivity, (iii) foreground/distractor/background gradient contributions using audit-only oracle masks, and (iv) ambiguity/forced-assignment properties of the barycentric semantic target. The next design branch will be selected from evidence: step-size control, label-free token gating, discriminative target redesign, or stopping the current fast-weight branch if even oracle-clean updates do not help.

---

## 2026-09-12 — T003 review

**Decision:** ACCEPTED; BRANCH C PRIMARY, LIMITED EASY-REGIME A COMPONENT

Reviewed commits:
- `6780de5ae44dcc89b9f1c45ea781f33dc16ffbaf` — frozen-checkpoint oracle diagnostic implementation and tests;
- `8b940f49e0760b4e0ff7e5036bb61edb757be272` — complete T003 A6000 report and interpretation.

Accepted evidence:
- all six original T002 P/B2 checkpoints and exact held-out episode streams were reused; source checkpoint hashes match and normal eta=.05 outputs/metrics reproduce T002 exactly;
- 1,200 checkpoint/episode pairs were processed, with labels/IDs confined to explicitly oracle-diagnostic code;
- no outer retraining, generator changes, detector integration, or deployable use of labels occurred;
- full regression passes 30/30 locally and 30/30 on both A6000 CPU/CUDA paths;
- D1-D4 are complete across seeds 7/17/27 and easy/hard regimes.

Primary mechanism finding: the current semantic barycenter target is not discriminative enough for a useful inner update. P's mean inner-task cosine is approximately zero (+0.011 easy, -0.011 hard). Foreground-only use of the same soft target does not rescue performance, but replacing that target with the oracle correct class text on the exact same frozen W0 path raises accuracy from 77.58/40.54 (no update) to 85.17/48.33 (easy/hard) and improves mean NLL in every seed and regime. The oracle exact-text gradient is much better aligned with the task gradient (+0.317 easy, +0.121 hard) than the foreground soft target (+0.047, -0.005).

Target diagnostics explain why. In the hard vocabulary, assignment entropy is 1.367 nats versus log(4)=1.386, top1-top2 gap collapses to 0.046, foreground assignment correctness is 29.27%, and the target's correct-minus-strongest-wrong cosine margin becomes negative. High cosine to the correct text is misleading because cosine to the strongest wrong text is even higher: the raw barycenter mostly retains vocabulary common-mode semantics rather than class-relative discrimination.

Token contamination is not the dominant failure mode: foreground/distractor/background gradients are highly similar, and foreground-only soft adaptation remains poor. Step size contributes to easy-regime overshoot (eta=.01 is less harmful than .05), but it does not explain the hard-regime failure. Fast weights themselves are not rejected because a better semantic direction demonstrably helps on the same frozen model.

**Next action:** T004 assigned. Replace the single-vector barycentric inner target with label-free objectives that preserve relative vocabulary geometry. First screen three candidates on frozen T002 P checkpoints: full-distribution semantic matching (O1), vocabulary-centered relative target (O2), and centered distribution-preserving matching (O3). Only if a candidate improves hard-regime gradient alignment / pre-post task loss over O0 without catastrophic easy harm may Codex meta-train at most two candidates under the fixed T002 budget. Grounding-DINO integration remains blocked until a redesigned objective improves over its own W0 and the original P with better task-gradient alignment.

---

## 2026-09-12 — T004 review

**Decision:** ACCEPTED AS A VERIFIED NEGATIVE PHASE-1 SCREEN; FIXED-STEP OBJECTIVE REDESIGN NOT YET SCIENTIFICALLY SUCCESSFUL

Reviewed commits:
- `be0a11c5790c1c01f4ac7bafe4baefa3365e8bfc` — preregistered objective definitions and Phase-1 gate;
- `9afe8df54c22d0a20b284d6b4b20aaab5b36ea9a` — O0/O1/O2/O3 implementation, tests, and frozen-screen runner;
- `4714d82844df591c0bfa3c0c584d60de148bcec0` — A6000 screen dispatch/recovery state;
- `509be86e582a14b850f700fcb26b73f825ef8fa9` — complete T004 screen report and durable artifacts.

Accepted protocol/engineering evidence:
- O0 reproduces the original P path exactly over all 600 matched episodes;
- all four objectives share the same 2,128 fast parameters and normal runtime remains label-free;
- source checkpoint hashes, frozen episode streams, generator/split, and evaluation conditions are preserved;
- episodic reset, vocabulary dependence, finite centered-text handling, finite-difference W0 meta-gradient, and key/query gradient flow are verified;
- full local suite passes 53/53 and A6000 CPU/CUDA suites each pass 53/53;
- all 2,400 objective diagnostics agree with the normal runtime implementation and are finite;
- no outer retraining, detector integration, hidden tuning, generator redesign, or test-label inner objective occurred;
- the preregistered gate was enforced and Phase 2 correctly stopped when no objective qualified.

Scientific result:
- O1 is the most interesting failure: its task-gradient cosine rises from O0's +.011/-.011 (easy/hard) to +.411/+.251, yet the fixed `.05` update causes severe easy collapse (39.46% accuracy, NLL 3.448) because its easy update norm grows to .703 versus O0 .179. Hard O1 is much less pathological: update norm .184 versus O0 .203, accuracy rises from W0 40.54% to 41.88%, but NLL improves only ~.004 nats.
- O2 is not supported: centering sharpens the teacher distribution but reduces assignment correctness and worsens hard task alignment/NLL.
- O3 retains good local direction but compounds centering with severe update-scale pathology; it is not a clean next candidate.

Interpretation: T004 disproves the simple claim that a relative/distribution-preserving objective plus the original fixed `eta=.05` is sufficient. It does **not** yet disprove O1's directional signal. The data expose a direction-versus-step mismatch: local task alignment can be strong while a finite step overshoots due to episode-dependent gradient scale/curvature. This is especially clear because O1's own inner CE increases after the fixed easy step.

**Next action:** T005 assigned as a frozen-checkpoint causal diagnosis. Carry forward O1 only and decouple gradient direction from step magnitude with (C1) a label-free O0-budget matched update and (C2) a deterministic label-free O1 backtracking/Armijo controller, alongside immutable O0/C0 controls. No meta-training or detector integration is allowed. If neither controlled update produces hard task improvement over W0 while retaining O1's alignment, the current semantic-fast-weight branch should be stopped/reframed rather than tuned further.
