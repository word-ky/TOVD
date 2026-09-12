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

---

## 2026-09-12 — T005 review

**Decision:** ACCEPTED; C2 BACKTRACKING IS THE FIRST POSITIVE TASK-USEFUL FAST-WEIGHT RESULT, C1 REJECTED

Reviewed commits/artifacts:
- `7b8949e33cfd861dbfb25a6e4a70b841af73733c` — T005 preregistration;
- `f2b9722ae8a1ad68e0e529488e68f88c170125de` — controller implementation, tests, and frozen-screen machinery;
- `2b22fc00ad34278ca285e93cf7b9b83797ae397e` — A6000 dispatch/recovery state;
- `9f32b69373600d7ad91db707c346ed5f882cf0bf` — final frozen evidence and report;
- `research_log/t005/RESULTS.md`, controller source, and the T005 mailbox report.

Accepted protocol/engineering evidence:
- O0/C0 exactly reproduce all matched T004 task metrics, preserving the causal comparison;
- full local suite passes 70/70; A6000 CPU and CUDA suites each pass 70/70;
- 2,400 diagnostic outputs/fast states match normal runtime exactly and remain finite;
- C1 update norms match O0 budgets to float32 tolerance while retaining the O1 direction;
- C2 uses only O1 loss for the fixed deterministic Armijo search, with no task labels/oracle diagnostics in runtime selection;
- episodic reset, vocabulary dependence, repeatability, source checkpoint hashes, and outer-gradient safeguards are preserved;
- no outer retraining, generator/objective/temperature redesign, detector integration, seed selection, or post-hoc eta sweep occurred.

Scientific result: T005 cleanly separates *direction* from *finite-step calibration*. C1 fails the preregistered full scale-rescue/task-useful criteria, so simple norm matching is not the answer. C2, however, converts the O1 direction into a task-useful update on the same frozen W0: easy accuracy/NLL move from 77.58%/.55592 to 86.71%/.34449, and hard from 40.54%/1.31390 to 46.25%/1.23536. Hard NLL and accuracy improve in all three seeds. All 600 selected C2 steps satisfy the Armijo condition, with no zero-step fallback, while the raw O1 task-gradient cosine remains strongly better than O0 (+.411/+ .251 easy/hard versus +.011/-.011).

The mechanism interpretation is now narrower and stronger: the useful ingredient is not merely a larger-capacity fast model or a vocabulary-conditioned target; it is a **vocabulary-relative semantic gradient whose episode-dependent step is controlled by label-free inner-loss geometry**. This rescues the fast-weight branch from the negative T002/T004 results.

Caveats retained: Armijo descent is not per-episode task safety; easy seed 27 still regresses substantially from its own W0; C2 costs multiple inner-loss evaluations; and this remains a synthetic frozen-checkpoint result. Therefore detector integration is still premature.

**Next action:** T006 assigned. Meta-train a new O1+C2 model under the original T002 budget, differentiating the accepted functional update while stop-grading the discrete eta selection. The experiment must isolate adapted performance from the same trained W0-only path, reuse/re-evaluate B0/B1/B2 on identical held-out streams, verify meta-gradients away from eta boundaries, and apply preregistered hard-generalization/easy-safety rules. Only a stable win beyond W0 and strong non-TTT/generic-TTT controls can unlock a later small detector integration task.

---

## 2026-09-12 — T006 review

**Decision:** ACCEPTED AS A VALID NEGATIVE CONTROL-COMPETITIVENESS RESULT; RANDOM-INIT C2 META-TRAINING REJECTED, FROZEN T005 MECHANISM RETAINED

Reviewed commits/artifacts:
- `f9f413704f8aa062a2b4c198e232a7b260ba44d9` — preregistered T006 protocol and comparator convention;
- `65299db5f1127407f856872b732f2b2b7051383e` — piecewise C2 meta-training implementation, tests, and controlled runner;
- `59311b904fe8178db6d5376be39b1d4954a7c941` — A6000 dispatch/recovery state;
- `70588e10f3237d69f6d30a83af57c09fc2591512` — complete three-seed T006 evidence and final report;
- `research_log/t006/PLAN.md`, `research_log/t006/RESULTS.md`, and the T006 mailbox report.

Accepted validity evidence:
- all three seeds completed 400 continuation-equivalent steps under the fixed T002 budget with zero nonfinite steps/elements, zero train/test Armijo violations, and no eta=0 fallback;
- full local suite passes 75/75; A6000 CPU and CUDA suites each pass 75/75;
- historical B0/B1/B2/P checkpoint hashes and exact held-out streams are preserved; all 2,400 re-evaluated historical episode metrics/IDs match T002 exactly;
- stable-region finite differences validate the piecewise meta-gradient at epsilon 1e-5 with 60/60 stable probes and approximately 1e-11 maximum absolute error; selector crossings at larger perturbations are explicitly recorded rather than treated as smooth-gradient failures;
- selected eta is label-free and stop-gradient, while outer gradients reach W0/key/query projections; episodic reset, deterministic replay, vocabulary dependence, W0-disable equality and normal-runtime equality remain intact;
- no detector work, objective/controller/temperature/generator/architecture change, test-label inner loss, or post-result tuning occurred.

Scientific result: T006 preserves the *relative* value of the fast update but loses *absolute* competitiveness. Hard held-out performance moves from the new W0-only 29.92% / 1.46985 NLL to 34.63% / 1.35845 after adaptation, and both metrics improve in all three seeds. Hard O1/task cosine remains +0.321 versus original O0 approximately -0.011. Thus Rules 2 and 5 pass: the learned model still uses the fast path and the update direction remains task-relevant.

The decisive failure is Rule 3. Adapted T006 is 10.0 pp below B2 hard accuracy and approximately 0.096 nats worse in NLL; it is also about 7.71 pp below B0 and 0.098 nats worse in NLL. Most importantly, it is far below the T005 frozen-C2 reference (46.25% / 1.23536). The outer/meta training therefore learned a weak absolute representation even though C2 still improves that weak representation locally.

Interpretation: this is not evidence that semantic fast weights are useless. It rejects the specific assumption that **O1+C2 should jointly learn both the slow semantic representation and the fast adaptation behavior from the original random initialization under the fixed T002 budget**. The strongest current evidence instead points to a decoupled regime: first learn a strong semantic state under O0, then keep that state strong and apply O1+C2 as label-free episodic adaptation.

**Next action:** T007 assigned as a warm-start origin audit. Start two matched 400-step continuation branches from the exact same final T002 P checkpoint: W1 continues the original O0 training, while W2 switches to O1+C2 meta-training. Evaluate both W0-only and O1+C2-adapted paths against the original frozen T005 state, T006 random-init meta state, and exact B0/B1/B2 controls. This will determine whether T006 failed because C2 meta-training started from scratch or because outer optimization with C2 itself erodes a strong pretrained representation. No detector integration is allowed until this ambiguity is resolved.

---

## 2026-09-12 — T007 interim implementation review

**Decision:** IMPLEMENTATION / PROTOCOL ACCEPTED; CONTINUE THE FIXED RUN; SCIENTIFIC OUTCOME PENDING

Reviewed commits/artifacts:
- `deeacd42ebe5dcb54bebd52a7f0e4f647dffde4c` — preregistered T007 matched warm-start audit;
- `e88ad88112f6486f8c7dc8458594e095528ba9f1` — implementation, focused tests, replay/equality machinery, rule evaluator and fixed-snapshot audit;
- `ad31f89192d4aff9c8dabf907c97f3ccca82bbbb` — A6000 dispatch and recovery state;
- current `coordination/CODEX_TO_CHATGPT.md`, which explicitly states that aggregate T007 outcomes have not yet been read.

Interim acceptance evidence:
- both W1 and W2 initialize from byte-verified identical seed-specific final T002-P tensors and use fresh Adam with the same `.001` learning rate;
- continuation episodes begin after the original T002 training stream, avoiding accidental replay of the original training indices;
- W1 follows the original O0/P semantic-TTT implementation and W2 follows the unchanged O1+C2 backtracking implementation;
- no new objective, controller, regularizer, architecture, generator, detector path or test-time label use was introduced;
- source checkpoint hashes are checked before continuation, step-0 origin equality is enforced, historical controls are replayed, fixed 0/50/100/200/400 snapshots are saved, and final-checkpoint-only primary interpretation is encoded;
- local full regression passes 79/79; focused common-origin/manual-Adam/replay/serialization and miniature end-to-end/rule tests pass;
- parameter-count correction to 1616 fast +256 key +256 query =2128 total is bookkeeping only and does not alter tensor shapes or scientific degrees of freedom.

Code review found no blocking mismatch with the T007 acceptance contract. `P_O0_resume` falls through to the same `FastSemanticMemory` construction as P and is explicitly routed through the enabled-TTT forward path; `P_C2_warm` constructs the same O1 backtracking memory as the accepted C2 path. The manual continuation test verifies exact branch-equivalent continuation from the common origin.

**Instruction / next action:** finish the exact dispatched A6000 run without changing any preregistered setting and without tuning/selecting from partial outcomes. When complete, report Rules 1–6, all W0-only/adapted held-out metrics, W1-vs-W2 matched-continuation effects, T005/T006/B0/B1/B2 equality receipts, drift/trajectory/selector/mechanism diagnostics, and CPU/CUDA receipts. Do not start Grounding-DINO integration or T008 before Research Lead reviews the complete T007 evidence.

---

## 2026-09-12 — T007 final review

**Decision:** ACCEPTED AS A VALID NEGATIVE / STATE-DEPENDENCE RESULT; WARM-START C2 META-TRAINING REJECTED AS T005 SUCCESSOR

Reviewed commits/artifacts:
- `4315ba35f0b89bbfa92958cf75a8bcd6a22f9eee` — complete T007 A6000 evidence, tests, trajectory metrics, rules and engineering report;
- `3d784491016bc187eb8a91379045cc18a545a1c6` — reconciliation of the interim review with the completed evidence;
- `research_log/t007/RESULTS.md`, `trajectory_metrics.csv`, `per_seed_diagnostics.csv`, and the final mailbox report.

Validity is accepted. All six runs completed the fixed preregistered budget, source hashes and common origins match, historical reference streams replay exactly, all steps are finite with zero Armijo violations, and local plus A6000 CPU/CUDA suites pass 79/79. No scientific setting changed after the tested implementation commit.

Scientific result: warm start repairs much of the T006 random-initialization deficit but does not make C2 outer training a viable successor to the frozen T005 mechanism. W2 hard improves from its own W0 38.92% / 1.30820 to 43.54% / 1.22793, so the fast path remains locally useful. However W2 is 2.71 pp below T005 hard accuracy and loses to the matched W1+frozen-C2 state in both hard accuracy and NLL (43.54% / 1.22793 versus 45.38% / 1.22032). The C2 continuation objective therefore does not improve the strong pretrained state under the fixed continuation budget.

The more important finding is **checkpoint/state dependence of the fast update itself**. W2 easy seed 27 is harmed severely by C2 (92.5% / .24285 -> 84.875% / .35722), while seeds 7/17 gain strongly. W1+frozen-C2 is also unsafe after O0 continuation: final easy performance falls on average from 80.96% / .40478 to 74.17% / .66709. The fixed trajectory makes the sign flip concrete: the same W1 seed-7 easy C2 update is strongly helpful at step 0, nearly neutral around step 200, and harmful by step 400 as the slow state strengthens. Thus T005 remains valid mechanism evidence but is not evidence that always-on C2 is safe across checkpoint evolution.

This changes the research question. The next scientifically useful question is no longer how to meta-train C2, but whether **the need for adaptation is observable without labels**. If a strong/easy state can be recognized from runtime uncertainty or update geometry, C2 can become selective specialization; if not, the current branch lacks a defensible safety mechanism and should not be moved into a detector.

**Next action:** T008 assigned as a state-dependent safety audit. Reuse T005/T007 checkpoints and fixed held-out streams without retraining. Before computing new correlations, preregister a fixed set of label-free pre-update and post-candidate observables. Use task labels only offline to score C2 benefit/harm, then test whether any single runtime scalar predicts harm with leave-one-seed-out AUROC >= .70 mean and >= .65 in every fold, including within easy episodes. No learned gate, new objective, new eta schedule, architecture change or detector integration is allowed in T008. A passing scalar only justifies a later separately preregistered selective/rollback policy task.

---

## 2026-09-12 — T008 review

**Decision:** ACCEPTED AS A VALID NEGATIVE RESULT; EPISODE-LEVEL SAFETY OBSERVABILITY FAILED; QUERY-LOCAL REFRAME ONLY

Reviewed commits/artifacts:
- `c163c78c51045f532176e9165dc56f7ead3649b0` — preregistered T008 plan;
- `153ac30d00753b43a56ce2e226068b0c35039d70` — frozen audit implementation and tests;
- `fce7541564fb3f7b4350524b2628171836075b11` — fixed A6000 dispatch;
- `1d9915b06befaf509b912e3328491e3a8b263522` — finalized evidence/report;
- `research_log/t008/RESULTS.md`, `statistics.py`, localization/sign-map tables, and final engineering mailbox.

Validity is accepted. The audit used the exact frozen T005/T007 state grid and episode streams, produced 6600 raw / 5400 unique-state primary rows, replayed all historical metrics and IDs exactly, kept oracle outcomes outside runtime features, preserved model parameters, and passed 85/85 locally and on A6000 CPU/CUDA. The LOSO implementation fixes scalar orientation from the other two seeds only and never reorients on the held seed.

Scientific result: all 14 preregistered single scalar features fail the episode-level interpretation gate. Best overall is post-candidate relative inner reduction with mean LOSO AUROC 0.5806 (minimum 0.4911); best pre-update is gradient norm at 0.5385 (minimum 0.4087). Easy pooled confidence-gap/max-probability AUCs are not transferable because the held-seed orientation flips on seed 27. This rules out a defensible simple episode-level selective/rollback C2 policy under the tested state grid.

The localization evidence is mechanistically useful but insufficient for deployment: harmful easy episodes are more confident at W0 and show somewhat larger normalized updates/representation shifts, yet they have smaller predictive JS, fewer top-1 changes and smaller relative inner descent than beneficial easy episodes. All 33 hard state means remain beneficial even though individual hard episodes can be harmed. Therefore “confident-state overspecialization” is only a partial qualitative explanation, and episode averaging may be concealing query-local structure.

**Next action:** T009 assigned as the final narrow audit before terminating this fast-weight safety branch. Reuse T008 stored query probabilities/tokens and decompose task harm at the query level. Test fixed per-query pre-update and post-candidate scalars with leave-one-seed-out evaluation, quantify correct/wrong transition types and confidence-quartile damage attribution, and compute an offline oracle per-query rollback ceiling. No learned gate, threshold rescue, model rerun/retraining, objective/eta change, or detector integration is allowed. A future T010 is justified only if a single query-level label-free scalar generalizes across seeds and the oracle rollback ceiling shows meaningful retained hard gain plus removal of easy regressions; otherwise formally stop O1+C2 and pivot to a non-destructive higher-level formulation.