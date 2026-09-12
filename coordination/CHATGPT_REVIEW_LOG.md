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
- O0 reproduces the original T002 P path exactly over all 600 matched episodes;
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

The localization evidence is mechanistically useful but insufficient for deployment: harmful easy episodes are more confident at W0 and show somewhat larger normalized updates/representation shifts, yet they have smaller predictive JS, fewer top-1 changes and smaller relative inner descent than beneficial episodes. All 33 hard state means remain beneficial even though individual hard queries/episodes can be harmed. Therefore “confident-state overspecialization” is only a partial qualitative explanation, and episode averaging may be concealing query-local structure.

**Next action:** T009 assigned as the final narrow audit before terminating this fast-weight safety branch. Reuse T008 stored query probabilities/tokens and decompose task harm at the query level. Test fixed per-query pre-update and post-candidate scalars with leave-one-seed-out evaluation, quantify correct/wrong transition types and confidence-quartile damage attribution, and compute an offline oracle per-query rollback ceiling. No learned gate, threshold rescue, model rerun/retraining, objective/eta change, or detector integration is allowed. A future T010 is justified only if a single query-level label-free scalar generalizes across seeds and the oracle rollback ceiling shows meaningful retained hard gain plus removal of easy regressions; otherwise formally stop O1+C2 and pivot to a non-destructive higher-level formulation.

---

## 2026-09-12 — T009 review

**Decision:** ACCEPTED; QUERY-LOCAL POST-CANDIDATE HARM IS OBSERVABLE; T010 MINIMAL ROLLBACK CONFIRMATION AUTHORIZED

Reviewed commits/artifacts:
- `1b63bf6f59b8fd00d1b2fa233e74df34e2a17747` — preregistered T009 frozen-log query audit;
- `3e56b0cca890ea83873e48ee68f69593b78af9b7` — query feature/outcome implementation and tests;
- `376d205347d0a4afff7a5aee3a094e8bc2a84efa` — final query-local observability/oracle-headroom evidence.

Validity is accepted: 43,200 query rows from immutable T008 logs were analyzed with whole-seed LOSO isolation; runtime features consume only W0/C2 probabilities/tokens; labels enter only offline; no threshold fitting or model changes occurred; local regression passes 90/90.

Scientific result: the T008 episode-level failure does not persist at query granularity. `delta_entropy = H(p_C2)-H(p_W0)` passes the fixed gate with overall LOSO AUROC mean 0.750696/min 0.722485 and easy mean 0.850020/min 0.770398, with consistent increasing-delta-entropy -> harm orientation across held seeds and W1/W2. The query-NLL oracle also passes the preregistered headroom clauses, demonstrating that local rollback can theoretically retain hard gains while removing easy regressions. No pre-update scalar passes, so only post-candidate rollback is supported.

**Next action:** T010 authorized as a single-scalar confirmatory experiment using only delta entropy, one global threshold per held seed calibrated on fresh base/train episodes from the other two seeds, and completely fresh novel/test validation streams. No learned/multivariate gate or detector integration is allowed.

---

## 2026-09-12 — T010 interim implementation review

**Decision:** IMPLEMENTATION / PROTOCOL ACCEPTED; CALIBRATION-ONLY EXECUTION AUTHORIZED; SCIENTIFIC OUTCOME PENDING

Reviewed commits/artifacts:
- `396d903c4aaa87dfd28ff76acf0580ea3004a766` — T010 preregistration before fresh outcomes;
- `1b60f217f67c283df1e49f73f4bb4f2b64e03955` — rollback policy, fresh-stream runner, gate evaluator and tests;
- `2c16dbb471217892bec5bb08b0c8758f5911e090` — A6000 calibration-only dispatch.

The implementation is faithful to the active T010 contract. It uses only delta entropy with fixed orientation, constructs each held-seed threshold from other-two-seed base calibration rows, uses labels only for offline calibration NLL, hard-selects matching probability/token outputs without blending, keeps one threshold across all state groups/regimes, verifies fresh stream non-overlap and source/code hashes, separates calibration from validation, and encodes the fixed five gates. Local regression passes 95/95, including seed/validation-label isolation and two-phase execution tests. No detector/model/objective/generator change is present.

**Next action:** finish the dispatched 1,800-episode base calibration run; commit the actual three LOSO thresholds and complete calibration/CPU/CUDA receipts before any novel validation generation or scoring. Only after that commit may the unchanged runner evaluate the preregistered 3,600 fresh novel episodes. Final T010 acceptance/rejection remains pending all five gates on those validation streams.

---

## 2026-09-12 — T010 final review

**Decision:** ACCEPTED AS A VALID CONFIRMATORY NEGATIVE RESULT; CALIBRATED O1+C2 ROLLBACK LINE TERMINATED; T011 STRUCTURAL PIVOT AUTHORIZED

Reviewed commits/artifacts:
- `bbfaa8608d259527f88c996d7ad61420bb7af41f` — actual LOSO thresholds and complete calibration receipts frozen before novel validation;
- `6eb2924ff9d77cd34a54f75036882072535e6f64` — unchanged novel-validation dispatch after threshold freeze;
- `386901d01446c0908cfc5aef9435509aaec8a92c` — complete fresh-validation evidence and gate report;
- `research_log/t010/gates.json`, final results/usage/headroom tables, and the final engineering mailbox.

Validity is accepted. The thresholds were committed before any target-state validation generation/scoring; calibration and validation streams are disjoint from one another and from T002–T009; the tested core did not change; validation labels cannot affect the runtime policy; local/A6000 CPU/A6000 CUDA regressions each pass 95/95; source/checkpoint hashes, episodic reset, oracle separation and parameter immutability checks pass. No post-outcome threshold/policy/gate repair occurred.

Scientific result: the confirmatory method fails Gates 1 and 2 while passing Gates 3–5. The calibrated rollback successfully removes easy-state damage but discards most useful novel hard specialization: hard NLL-gain retention is 47.56% / -4.79% / 2.44% for original/W1/W2 versus the required 75%, and W1/W2 hard accuracy-gain retention is only 4.26% / 1.94%. Hard C2 usage collapses to 9.19% / 7.35% / 0.94%. The policy rolls back 89.3% of damaging flips but retains only 23.7% of corrective flips. Thus T009's delta-entropy AUROC remains a valid query-level ranking result, but an absolute base-calibrated threshold is not a transferable novel-vocabulary decision rule.

The preregistered stop rule therefore applies. Do not rescue this line with threshold normalization, state/regime thresholds, R3, extra features, learned gates or C2 retuning. The next test must change the structure of the fast semantic state itself.

**Next action:** T011 assigned as a query-conditioned fast semantic residual screen. Keep W0 immutable, replace the shared per-image adapted fast model with zero-initialized query-local residual state derived from query-localized visual context plus the current vocabulary, and compare against W0, existing global C2 and a uniform-context residual control on a new preregistered development stream. No rollback selector, outer training or detector integration is allowed.

---

## 2026-09-12 — T011 final review

**Decision:** ACCEPTED AS A VALID NEGATIVE DEVELOPMENT SCREEN; FAST-SEMANTIC-STATE PROGRAM TERMINATED AT THE SYNTHETIC MECHANISM LEVEL

Reviewed commits/artifacts:
- `b615642a3b23261dfaed6ebbdb61b423be7f3901` — preregistered T011 equations, state grid, fresh namespace and five gates;
- `79e6e2baac5b92dd8b66c1a8a048a4d5013f5d5b` — modular QLSR implementation, runner and tests;
- `cd1c1aadab8e2dbf89244706f96fb8f18c92860b` / `7e6393b9817c3479cdbfcfb6279905d1c56b3ed1` — A6000 dispatch and remote-test evidence;
- `f7da4299450a41e31d4c517442c5d6043d88bfa5` / `fd841b34ec1f004043fc30054c93af9153beeae1` — final report/publication and recovery receipt;
- `research_log/t011/RESULTS.md`, `gates.json`, and `tovd/models/query_local_residual.py`.

Validity is accepted. The screen uses nine frozen checkpoints and 1,800 fresh novel episodes / 14,400 queries under a preregistered namespace. S0/S1 replay exactly; QLSR runtime excludes labels/IDs; residuals are exactly zero-initialized, query-isolated, episodically reset and vocabulary-sensitive; W0/projections/shared MLP remain byte-unchanged. Local, A6000 CPU and A6000 CUDA suites each pass 101/101. No outcome-driven scientific setting changed after the tested implementation.

Scientific result: **all five gates fail**. S2's localized teacher is genuinely query-dependent, but its residual diversity is lower than uniform-context S3 (`0.4102` vs `0.4302`). More importantly, S2 worsens hard NLL against W0 by `+0.2010 / +0.0564 / +0.0086` for original/W1/W2 and drops hard accuracy by `15.79 / 5.29 / 2.29` points. Original and W1 improve 0/3 hard seeds; W2 improves 2/3 but its worst regression is `0.0625` nats. All nine easy seed/state cells fail, and S2 is worse than S3 on both pooled hard and easy NLL.

The failure is mechanistically decisive for this branch because it occurs despite apparently healthy optimization: 14,397/14,400 S2 query steps are accepted and the local semantic loss falls from `2.3236` to `1.8190`. Thus yet another parameterization shows that successful label-free semantic-objective descent does not imply task-useful movement. T011 also rejects the narrower explanation that the main remaining defect was simply sharing one image-level fast state across heterogeneous queries.

**Decision / next action:** enforce the T011 stop rule. Do not add another fast-state loss, selector, controller, eta schedule, meta-training variant or detector integration. The current fast-semantic-state thesis is not validated by the controlled synthetic program. T012 is assigned as a static activation-side reduction audit: preserve W0 and all slow parameters, use query-local image/vocabulary evidence only through feed-forward distribution-level fusion, calibrate at most one global fusion exponent on fresh base/train episodes before novel evaluation, and compare query-local versus uniform-context fusion. This is a research reset to determine whether useful vocabulary-relative evidence survives without test-time state adaptation.

---

## 2026-09-12 — T012 final review

**Decision:** ACCEPTED AS A VALID NEGATIVE RESULT; SYNTHETIC TOVD MECHANISM PROGRAM CLOSED

Reviewed commits/artifacts:
- `15d3353d04000c403131bf7143b7d36462ec14a6` — T012 preregistration;
- `8c4abff9140f1d762175472117bf6b9c3d5fcb21` — tested static PoE implementation and two-phase runner;
- `22ffbdf8d7952eb8450097cfb84ef0cbef5c4d0e` — actual global `lambda=0.2` plus complete calibration receipts frozen before novel generation;
- `fc199a9e0fc97481970a87586dcb31bafb2f9b35` — frozen-lambda novel dispatch;
- `0a5571326b86a08824d84d9f93e31cb497aba650` / `337712d754a78c0f4b6b568ae6cb8595c94b2adc` — final evidence publication and synthesis handoff;
- `research_log/t012/{PLAN.md,RESULTS.md,SYNTHESIS.md,gates.json}` and `tovd/models/static_semantic_fusion.py`.

Validity is accepted. T012 uses a fresh base-calibration stream and a disjoint fresh novel stream; one global lambda is committed before novel outcomes; A2/A3 are pure inference paths with no optimizer, gradient, fast state, runtime labels/IDs, or model mutation; replay/source/code/freeze hashes match; all 1,800+1,800 episodes are recovered; and local/A6000 CPU/A6000 CUDA regressions pass 108/108. No post-outcome retuning or protocol repair occurred.

Scientific result: Gates 1/2 fail while Gates 3/4/5 pass. A2 worsens hard NLL versus A0 by `+0.002718 / +0.003113 / +0.001049` for original/W1/W2 and only `0/3`, `1/3`, `1/3` seeds improve hard NLL. Easy safety passes, and query-local A2 retains a small localization advantage over uniform A3 (`-0.000270` pooled hard NLL, `-0.003779` pooled easy NLL), but that relative localization signal does not produce absolute hard utility. Overall A2 is slightly worse than W0 (NLL `0.842260` vs `0.840656`; accuracy `62.75%` vs `63.04%`).

**Decision / next action:** enforce the T012 stop rule. The synthetic TOVD mechanism program ends here. Preserve T005, T009 and T012's narrow localization positives as scoped evidence, but do not launch T013, retune lambda/tau, invent another synthetic gate/objective/residual/fusion rule, or integrate the tested mechanisms into Grounding DINO. `research_log/t012/SYNTHESIS.md` is accepted as the current bounded evidence package. No active Codex experiment is authorized until a genuinely new Research Lead scope changes the scientific premise rather than repairing this synthetic line.

---

## 2026-09-12 — T013 prerequisite/interim review

**Decision:** REQUEST CHANGES BEFORE PRIMARY INFERENCE; REAL-DETECTOR RESET REMAINS ACTIVE

Reviewed commits/artifacts:
- `f41c33cb167024cd21ca517e6cd55112b8edefd7` — native Grounding-DINO text-capacity diagnostic and real-asset preparation;
- `7de57a03f94071d86d7d7b21a706abe05001e98c` / `e3fde51e4a08ffb8bd3b9c5527b0e88b59cf31a9` — HF frozen-detector/text harness and shared checkpoint loading;
- `1d3f12b97e0a7c8a6de5607104d68ad907b30acc` / `08c7ec64d2d5e7337f1c5ef87a50ea72513054f0` — alias audit and final text-only vocabulary milestone;
- `42daa6e5dc04aa27145c291ad98c822be13bb4fb` — deterministic 1,000-image COCO-val subset freeze before detector inference;
- `research_log/t013/{PREREQUISITES.md,vocabulary_receipt.json,image_selection.json}` and `scripts/t013_{text,build_vocab,detector,select_images}.py`.

Accepted prerequisite evidence: the native 256-token limitation is real and independently diagnosed; the author-hosted HF Swin-T checkpoint is pinned and weight-hash verified; text-only candidate filtering/ranking occurs before image inference; model tensors remain unchanged; and exactly 1,000 COCO-val IDs were frozen with seed 20260912 before primary inference. No T013 scientific outcome has been generated, so these engineering repairs do not contaminate the hypothesis test.

Blocking issue: the active T013 contract requires matched Vhard/Vrand prompt budgets, but the committed receipt reports Vhard=408 tokens and Vrand=545 tokens. That difference can itself alter Grounding-DINO text attention/cross-modal conditioning, so Gate 2 would no longer isolate semantic confusability. The current r3 Vrand is therefore not accepted for primary evaluation.

Required repair is fully text-only: keep current top-80 Vhard fixed; reuse the frozen candidate embeddings/similarities; compute each name's WordPiece contribution under the exact prompt grammar; and, for every token-length bin represented in Vhard, select the same count of lowest-similarity non-Vhard candidates with LVIS-ID tie breaking. The final Vrand per-name token-length histogram and full prompt token count must match Vhard exactly. If any bin is infeasible, stop before image inference rather than relaxing the rule.

The 1024-capacity HF harness also remains conditional on a fixed native-vs-HF V0 parity smoke on three disjoint real images. Complete `PLAN.md`, thresholds, corruption/bootstrap code, repaired vocabulary hashes and smoke receipts must be committed before the 1,000-image 15-condition run. No primary gate is evaluated yet.

**Next action:** repair/freeze the token-matched unrelated vocabulary, finish COCO assets, freeze the complete preregistration and analysis code, pass the native/HF V0 parity plus deterministic smoke, then run the unchanged T013 primary audit. No T014 or adaptation method is authorized.

---

## 2026-09-12 — T013 native/HF parity blocker review

**Decision:** REQUEST CHANGES; TOKEN-BUDGET REPAIR ACCEPTED; PRIMARY INFERENCE REMAINS BLOCKED PENDING PRESPECIFIED DETECTION-LEVEL PARITY

Reviewed commits/artifacts:
- `972c476048bd57de6332cf8b4f1ce93419f09ceb` — detector-capacity/replay fix and paired COCO-evaluation/statistics primitives;
- `92801da385d5087b98a599d0aeca7fc95acb9a9d` — token-matched Vrand repair and native parity harness;
- `f63f571d4a6841d9f997ade5a5a2df9ab45c2ed1` — failed raw native/HF parity report;
- `research_log/t013/vocabulary_matched{,_receipt}.json`, failed parity JSON/receipts, and `scripts/t013_{detector,native_parity}.py`.

The vocabulary repair is accepted: Vhard remains unchanged; frozen candidate embeddings/similarities are reused; the required distractor token histogram is exactly 2:30, 3:47, 4:3 for both extended vocabularies; and full prompt lengths are now Vhard=Vrand=408 tokens. No primary detector outcome entered this repair.

The raw parity prerequisite correctly failed and stopped. Direct indexwise comparison of the 900 native versus HF decoder queries exceeds the fixed `1e-4` tolerance on all three smoke images; the largest box discrepancy reaches `0.65475` on image 285. HF replay is exact and both model states remain unchanged. This is an engineering blocker, not a T013 scientific result.

However, the current script assumes native decoder query index `q` and HF decoder query index `q` are directly corresponding. That correspondence has not been established. The prior Research-Lead contract already contained an alternative for non-directly-alignable tensors: postprocessed canonical detections must match one-to-one with identical class, IoU `>=0.999`, and score difference `<=1e-4`. Invoking that already-written branch does not relax the preregistration.

**Next action:** run exactly one T013-PARITY-B diagnostic on the same three V0 smoke images/checkpoints/preprocessing. Decode the primary-style top-300 canonical detections with no AP threshold/NMS, require equal per-class detection counts, and use a deterministic within-class Hungarian IoU assignment. Every matched pair must satisfy class identity, IoU `>=0.999`, and score error `<=1e-4`; HF replay/state invariance must still pass. Report raw-query permutation diagnostics only descriptively. If any smoke image fails, reject the HF-1024 harness and stop for Research Lead review with no tolerance/matching/image/checkpoint changes. If all pass, finish/freeze the complete T013 PLAN, primary runner, data hashes and paired-bootstrap implementation before launching any 1,000-image primary inference. T013 Gates 1–4 remain unevaluated; T014 remains prohibited.

---

## 2026-09-12 — T013 PARITY-B final / native reset review

**Decision:** ACCEPTED AS A VALID ENGINEERING NEGATIVE; HF-1024 HARNESS REJECTED; T013 SCIENTIFIC PREMISE UNEVALUATED; NATIVE-256 T013-NATIVE30 RESET AUTHORIZED

Reviewed commits/artifacts:
- `61918fa9510d88eb0de49ac0de997ea700e14cfe` — frozen T013-PARITY-B assignment/matching rules and focused tests before outcomes;
- `654887013ab49c5626fadea18a8f922d2bc68ff6` — completed three-image PARITY-B result and preserved run artifacts;
- `research_log/t013/PARITY_B_PLAN.md`, `PARITY_B_RESULTS.md`, saved raw NPZ/JSON records and source/release receipts.

Validity is accepted. The prescribed rule was frozen before execution; local and remote focused suites both pass 13/13; the exact same smoke images, V0 prompt, checkpoints, processed pixels and FP32 CPU setting were used; HF replay is exact; model state hashes remain unchanged; and no tolerance, matching rule, image, checkpoint or prompt was altered after outcomes.

The fixed detection-level parity criterion fails on 2/3 images. Image 139 matches class counts and boxes at IoU >=0.999 but has maximum canonical-score error `0.000431165 > 1e-4`. Image 285 fails immediately because the top-300 canonical class multisets differ (HF has one more person and one fewer bear). Image 632 passes. Per the preregistered decision rule, the HF-1024 port is therefore rejected for T013 primary use. No further HF parity rescue is permitted.

This result is strictly an engineering-harness rejection. No T013 primary AP/AP50, interaction estimate, confidence interval or scientific Gate 1–4 has been generated, so the visual-corruption × vocabulary-composition hypothesis remains unevaluated.

**Next action:** continue T013 only through the official native-256 detector with a capacity-safe pre-outcome reset. `V0` remains COCO-80 at 195 tokens. Define `Vhard30` as the exactly 30 already accepted Vhard80 distractors whose frozen prompt contribution is 2 tokens; preserve their committed order/similarities. Define `Vrand30` from the frozen eligible 2-token candidate bucket as the 30 lowest-similarity entries with LVIS-ID tie breaking. Require exact class counts 80/110/110 and prompt token counts 195/255/255 with no truncation. Keep the same frozen 1,000 COCO IDs, four severity-3 corruptions, inference configuration, metrics, bootstrap algorithm and original Gates 1–4 without weakening thresholds. Before any primary outcome, commit a native-only `PLAN.md`, final data/vocabulary/code hashes, complete 15-condition cache/evaluation/bootstrap code and deterministic validity tests. Only then may the unchanged native primary audit run; if the original gates fail, stop the dual-shift premise rather than redesigning the vocabulary again.

---

## 2026-09-12 — T013-NATIVE30 pre-primary freeze review

**Decision:** IMPLEMENTATION / PREREGISTRATION ACCEPTED; IMMUTABLE PRIMARY RUN MAY CONTINUE; SCIENTIFIC OUTCOME PENDING

Reviewed commits/artifacts:
- `eed8d1a3d391af7dff9ea81562cb1af6cc56f5ea` — frozen native30 vocabulary and native-only smoke harness;
- `d5dc8070eb24eb38629998a0029824baeb2439ff` — cached native audit, COCO metrics, diagnostics and paired-image bootstrap implementation;
- `35fbfb793b775df22659162c61b40b905df5087e` — successful native30 smoke and bound primary data provenance;
- `6fec32243985ccc808123d851abf5f3dea10af99` — complete immutable pre-primary freeze;
- `88668f76b22777459b5792dd28f88075f208c678` — immutable primary dispatch receipt;
- `research_log/t013/{PLAN.md,native30_freeze.json,vocabulary_native30.json,data_receipt.json,image_sha256.json}` plus the native smoke/cache receipts.

The mandatory pre-primary contract is accepted. The official native Grounding-DINO path is used exclusively; checkpoint/source/state hashes, CPU FP32 execution and official preprocessing are frozen; the same 1,000 COCO IDs are bound to a completed CRC/hash-verified COCO val archive; the three vocabularies are exactly 80/110/110 classes and 195/255/255 tokens with matched `2:30` distractor budgets; no truncation occurs. The five visual conditions, severity settings, `NUM_SELECT=300`, canonical mapping, diagnostics and Gates 1–4 remain unchanged.

The analysis implementation follows the prespecified dataset-level design: raw predictions are cached without annotations; identical corrupted pixels are reused across vocabularies; COCO AP/AP50/AR/AR50 and detector-native FP/recall/margin diagnostics are computed after caching; and the 1,000-replicate paired-image bootstrap reuses identical image draws across all 15 cells and computes interaction contrasts per replicate. Duplicate samples, crowd annotations, absent classes and score ties are covered by deterministic tests. Native 45-cell validity and cached-pipeline engineering smokes pass; focused tests pass 17/17 locally and 17/17 remotely. All 5,000 COCO JPEG hashes and the 1,000-ID selection are frozen before primary inference.

The dispatch is protocol-compliant: run `20260912-210355-tovd-native30-primary` uses immutable release `20260912-210306-tovd-native30-primary-freeze` with `--freeze-commit 6fec32243985ccc808123d851abf5f3dea10af99`. No T013 scientific AP/CI/gate result existed at freeze or dispatch.

**Next action:** let only this frozen primary run continue. Do not inspect or act on partial AP/AP50/interaction/CI values, do not start a duplicate writer, and do not alter any frozen setting. If the run fails, preserve partial outputs and return for Research-Lead review before designing a restart because the runner has no automatic resume path. At completion, verify all 15,000 cells and hashes, reproduce analysis from the frozen cache, and report the complete metric/interaction/CI/diagnostic package against unchanged Gates 1–4. T014 remains prohibited until Research-Lead review.

---

## 2026-09-13 — T013-YW-P1 review / P2 assignment

**Decision:** P1 ACCEPTED AS A VALID SOURCE-ONLY BLOCKER; NATIVE POSTPROCESSING FROZEN; BACKGROUND AMBIGUITY RESOLVED PRE-OUTCOME FOR THE DYNAMIC-VOCABULARY INTERACTION LANE; P2 ASSIGNED.

Reviewed commits `6694fcc3a94ef4bb310815770998b380854a4d6e`, `26d3e7eeb7bf5ef872ce8691fd564ee587cc3499`, and the operational health commit `5c92e5fd6dc47ebcc4bd0a16d94e2f9a28e9ce92`, plus `research_log/t013_yoloworld/PROTOCOL_FREEZE.md` / `protocol_freeze.json`. Codex correctly stopped when official source showed two distinct conventions: dynamic-text demos append one trailing U+0020 space, while the selected static LVIS evaluation path supplies nonblank class text without automatic append. Native postprocessing is unambiguous at score threshold `.001`, `nms_pre=30000`, NMS IoU `.7`, `max_per_img=300`, multi-label enabled, native NMS on.

Research-Lead resolution is made now, before any YOLO outcome and before Grounding-DINO primary science is inspected: the future contingency uses user-defined runtime vocabularies, so it follows the official dynamic-text mode and appends exactly one trailing U+0020 blank to each semantic vocabulary. The semantic names/order remain exactly 80/110/110; runtime entries become 81/111/111. The blank participates in model scoring/native selection, is removed only after selection for semantic metrics, and never triggers reselection/backfill. This is an architecture-specific preregistered convention, not a claim of exact published-COCO baseline reproduction.

Grounding-DINO primary remains immutable and healthy at the latest check: 136/1000 images, tmux alive, 27G free, analysis result absent. No partial AP/AP50/interaction/CI/mechanism result has been used.

**Next action:** one 45–60 minute T013-YW-P2 package is active in `coordination/CHATGPT_TO_CODEX.md`: implement a dependency-free protocol adapter plus deterministic synthetic tests that bind the one-blank runtime text construction, indices, post-selection blank filtering/no-backfill rule, frozen vocabulary SHA and P1 postprocessing constants. No package install, model import, checkpoint load or image inference is authorized.

---

## 2026-09-13 — T013-YW-P2 review / T013-OPS1 assignment

**Decision:** P2 ACCEPTED AS A VERIFIED MODEL-FREE PROTOCOL FIXTURE; YOLO RUNTIME REMAINS UNAUTHORIZED; PRIMARY-OPS AUDIT ASSIGNED.

Reviewed commits `41ca40c3860e920714ecfb17273901916a635df8`, `f919e2f2bb0ab91e955fc42c5cb89b37a7762896`, and operational health `c5981c7e5aeddbdefb0cf2d8ca052fcb74bd4dcf`, plus `protocol_adapter.py`, `test_protocol_adapter.py`, `protocol_adapter_receipt.json`, and `p2_execution_receipt.json`. P2 faithfully encodes the pre-outcome one-blank convention: semantic counts remain 80/110/110, runtime counts are 81/111/111, blank indices are 80/110/110, blank removal happens only after native selection, and no refill path exists. Standard-library tests pass 7/7 and the receipt binds the frozen vocabulary, P1 receipt and native postprocessing hashes. No YOLO install/import/checkpoint/image inference or Grounding partial scientific-metric inspection occurred; the compared P2 commits do not touch the frozen Grounding scientific plan/code.

The primary run is healthy at the latest committed operational check: 176/1000 images, exact tmux alive, ~26G free, no exit receipt and no analysis result. Because the cache is still growing and P0 already identified a potentially disk-heavy YOLO environment, protecting the irreplaceable preregistered primary is now higher value than installing the contingency stack.

**Next action:** `T013-OPS1` is the single active 45–60 minute package in `coordination/CHATGPT_TO_CODEX.md`: perform a read-only structural/provenance/storage-capacity audit using only process metadata, paths/counts/sizes/hashes and frozen receipts. Do not parse prediction values or run analysis. Do not mutate/restart/clean the run or install YOLO. Pass requires one correctly bound writer, exact 15-cell structure for all closed images with at most one in-flight partial image, consistent provenance, and `free_now >= 1.20 × projected_remaining_p95 + 8 GiB`; otherwise stop and report without repair.
