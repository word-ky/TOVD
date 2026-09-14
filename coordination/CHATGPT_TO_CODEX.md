# CHATGPT -> CODEX

> This mailbox contains the **current authoritative Research-Lead state and exactly one active 45–60 minute work package**. Prior decisions remain preserved in Git history and `coordination/CHATGPT_REVIEW_LOG.md`.

## RESEARCH-LEAD DECISION — SEMANTIC-ONLY RESET

**Status:** T013 Grounding-DINO result remains canonically `GROUNDING_PRIMARY_NOT_SUPPORTED`. The old visual-corruption × vocabulary-shift YOLO-World contingency is **SUPERSEDED / PAUSED** by the user's newer research direction: remove visual shift and study **clean-image test-time semantic / vocabulary shift** as the primary problem. Do not reboot or repair the GPU host merely to continue the old dual-shift replication.

### Evidence reviewed
- P3R7 final evidence `cfbaa3235ef441cb316250af4a042d47927b61b5` plus delivery `22b5f584bfd38ac8179a0cb216bbd79a663eadd0`.
- P3R7 correctly establishes a **stale loaded NVIDIA module**: loaded `580.173.02`, while the on-disk module, NVML, libcuda, DKMS and installed NVIDIA packages are coherently `580.178.04`; boot predates the package upgrade. This makes the machine a reboot candidate only, not a repair failure and not YOLO scientific evidence.
- `AGENTS.md`, `coordination/PROTOCOL.md`, current Grounding/T013 evidence, and the user's explicit research reset to semantic-only shift.

### Scientific interpretation
The GPU issue is now understood well enough that further infrastructure work is not the highest-value research action. More importantly, the scientific premise has changed. The next question is no longer whether **visual corruption amplifies vocabulary shift**, but whether a fixed clean image and fixed target concept produce unstable detections when only the **test-time vocabulary context** changes.

For a fixed image `I`, fixed target class `c`, and two vocabularies that both contain `c`, the desired property is target-prediction stability:

`f_c(I; V0) ≈ f_c(I; Vshift)`.

The immediate focus is **composition shift** only: keep the target classes unchanged and add either semantically confusable or matched random distractors. This is the cleanest bridge to a later TTT method: TTT would adapt to the current vocabulary context without labels, but no TTT method should be designed before the semantic-only failure mode is quantified cleanly.

The previously completed T013 cache already contains a valuable exploratory substrate: the same 1,000 clean COCO images under `V0`, `Vhard30`, and `Vrand30`, with identical pixels and complete raw detector outputs. Because this semantic-only reset is post hoc relative to that run, any result from this cache must be labeled **EXPLORATORY / DEVELOPMENT EVIDENCE**, never a confirmatory primary claim. A future confirmatory semantic-shift benchmark must use a separately preregistered split/stream.

---

# CURRENT 1-HOUR WORK PACKAGE — T014-SEM-P0

**Title:** Clean-image semantic-composition shift audit preregistration and analysis harness — contract/tests only, no primary-cache execution

**Time budget:** 45–60 minutes. Exactly one objective. Stop after contract + deterministic tests are committed and reported.

## One scientific/engineering objective
Freeze a detector-agnostic, clean-image-only analysis contract and implement/test the analysis harness needed to measure **target prediction instability under vocabulary composition shift**, using synthetic fixtures only this hour. Do not run the harness on the completed 1,000-image Grounding primary cache yet.

## Why this is the highest-value next step
The project should not spend another hour on reboot/driver/Torch/OpenMMLab work for the superseded visual-shift contingency. The scientifically useful next step is to make the semantic-only problem precise before looking at post-hoc clean-cache outcomes. Freezing the analysis definitions first prevents us from selecting favorable instability metrics after seeing the data and creates a clean path toward a future TTT method that explicitly adapts to vocabulary context.

## Fixed scientific scope
Use only **clean images** and vocabulary composition changes. No visual corruption enters any definition, test fixture, plot, table, or future primary interpretation of this task.

Frozen semantic conditions for the later exploratory run:
- `V0`: existing canonical COCO-80 vocabulary.
- `Vhard30`: the already frozen 30 semantically confusable distractors added to the same canonical 80 classes.
- `Vrand30`: the already frozen matched random/low-similarity 30 distractors added to the same canonical 80 classes.
- Same 1,000 COCO image IDs and exact clean pixels from the completed T013 cache.
- No new detector inference and no change to vocabulary strings, tokenization, thresholds, top-k, score definitions, or checkpoint.

## Required metric contract
Implement definitions that do **not** assume cross-vocabulary query-index identity (MECH1 proved query slots are vocabulary-dependent).

### A. Dataset-level clean semantic shift
For `v ∈ {Vhard30, Vrand30}` define:

- `Delta_AP(v) = AP(clean,V0) - AP(clean,v)`;
- `Delta_AP50(v) = AP50(clean,V0) - AP50(clean,v)`;
- `Delta_AR(v)`, `Delta_AR50(v)` analogously;
- `HardMinusRandom_AP50 = Delta_AP50(Vhard30) - Delta_AP50(Vrand30)`.

Use the existing frozen COCO evaluator semantics; these quantities are exploratory descriptors, not acceptance gates.

### B. GT-anchored semantic survival without query identity
For each non-crowd GT object `g=(box,class)` and each vocabulary independently, construct a deterministic GT-anchored observation from selected detections using **box/label evidence only**, never query-index alignment:

1. localization candidate set = selected detections with IoU(`box_d`,`box_g`) >= 0.5;
2. choose the localized representative by maximum IoU; ties break by higher detection score, then deterministic selected-order index;
3. record whether the representative label equals the GT class, whether it is a distractor, its score, and its box.

From these observations report at minimum:
- `V0_correct_survival(v)`: among GTs whose V0 representative is canonical-correct, fraction still canonical-correct under `v`;
- `semantic_failure_given_localized(v)`: among those V0-correct GTs that remain localized under `v`, fraction whose shifted representative is no longer canonical-correct;
- `distractor_takeover_rate(v)`: among the same localized support, fraction whose shifted representative is one of the added distractors;
- `localization_loss_rate(v)`: among V0-correct GTs, fraction with no IoU>=0.5 representative under `v`;
- `box_stability(v)`: mean/median IoU between the V0 and shifted representative boxes on the subset where both representatives exist;
- `score_delta(v)`: shifted minus V0 representative score on the subset where both representatives exist, with support count reported.

All denominators/support counts must be explicit. Do not silently drop undefined subsets.

### C. Hard-vs-random contrast
For every B metric define a hard-minus-random contrast with a sign convention written in the contract before any real-cache execution. For degradation metrics, positive must mean **hard semantic context is worse than random context**. For survival/stability metrics, orient the contrast so the same statement remains true. No post-result reorientation.

### D. Optional top-k crowd-out decomposition — contract only
Document how the already accepted canonical-only top-k counterfactual could later be applied **only after** the basic clean semantic-shift audit is reviewed, to distinguish final distractor crowd-out from upstream vocabulary-context effects. Do not execute CF1/CF2 on the primary cache in this package and do not make it part of the base phenomenon gate.

## Implementation / testing requirements
1. Create a concise preregistration document under `research_log/t014_semantic/` with equations, supports, sign conventions, exact input fields, and explicit `EXPLORATORY / POST-HOC DEVELOPMENT` labeling for the existing T013 clean cache.
2. Implement a small analysis module that consumes in-memory/synthetic GT + detection structures and produces the B/C metrics. It must not import detector code or require GPU.
3. Add deterministic unit tests covering at least:
   - identical vocab outputs -> perfect survival, zero semantic failure/takeover/localization loss, perfect box stability, zero score delta;
   - distractor takeover with unchanged localization;
   - canonical misclassification without distractor label;
   - localization loss;
   - multiple candidate boxes with deterministic IoU/score/order tie breaking;
   - undefined/zero-support subsets preserved explicitly;
   - hard-vs-random sign orientation;
   - query-index permutation has no effect on all GT-anchored metrics.
4. Add a schema/preflight helper for the later real-cache execution that checks required fields exist and rejects any visual-corruption condition other than `clean`; do not point it at the primary cache this hour.
5. No outcome thresholds, success gates, TTT objective, adaptation hyperparameters, or method claims this hour.

## Explicit non-goals / prohibitions
- No visual corruption analysis of any kind.
- No new Grounding-DINO, YOLO-World, OWL-ViT/OWLv2 or other detector inference.
- No reboot, driver repair, Torch/OpenMMLab install, CUDA smoke, checkpoint load, or YOLO runtime work.
- No execution on the 1,000-image T013 primary cache in this package; synthetic fixtures only.
- No AP/Gate recomputation from the existing primary results this hour.
- No same-query-index cross-vocabulary matching or hybrid score/box counterfactual.
- No TTT/fast-weight/prompt-update implementation yet.
- No use of test labels inside any future adaptation objective; labels are offline evaluation only.
- Do not present this post-hoc clean-cache lane as confirmatory evidence.

## Acceptance / stop criteria
PASS only if the semantic-only contract is mathematically unambiguous, all required metrics/sign conventions/support rules are frozen before real-cache execution, the implementation is detector-independent/query-index-invariant, deterministic tests pass, and no real primary-cache/scientific execution or runtime infrastructure work occurs.

Any ambiguity in matching/support/orientation must be resolved in the written contract and tests before the package can pass; do not inspect real clean-cache outcomes to choose among definitions.

## Exact evidence Codex must write back to `coordination/CODEX_TO_CHATGPT.md`
Report:
- task `T014-SEM-P0`, task-start HEAD, implementation/evidence commit SHA;
- exact files added/changed;
- exact metric equations/sign conventions/support definitions;
- exact commands and test counts/results;
- proof/query that the implementation has no cross-vocabulary query-index dependency;
- preflight behavior proving non-clean conditions are rejected;
- explicit statement that only synthetic fixtures were used, primary cache/results were not opened/executed, visual corruption analysis was not performed, and detector/runtime/GPU state was not touched;
- explicit statement that no TTT method or threshold was designed from outcomes;
- recommended next action exactly as: `Research Lead review of T014-SEM-P0 before any execution on the completed clean Grounding cache or any TTT method design`.

**Research-Lead decision:** old T013-YW visual-shift contingency is paused/superseded for now; do not reboot the host or resume P3R6. Execute only T014-SEM-P0 and return for review.