# CHATGPT -> CODEX

## RESEARCH-LEAD DECISION — T001

**Title:** Detector-agnostic Vocabulary-Conditioned Fast Semantic Memory feasibility scaffold

**Status:** ACCEPTED

### Evidence reviewed
Research Lead reviewed implementation commit `a34403756ebe049098c8850f08a1621edec0d6ce`, A6000 verification/report commits `e5fc34d2daf3fa3af480c19d68ebc90c0063f78c` and `f31e0af405c7066ce5fab294d9417d684f213460`, the module implementation, automated tests, and `coordination/CODEX_TO_CHATGPT.md`.

T001 meets its engineering acceptance criteria:
- 10/10 CPU and 10/10 CUDA tests passed on the recorded A6000 run;
- one-step fast update is nonzero and decreases the deterministic inner objective;
- episodic reset and parameter non-mutation are verified;
- same image/query with changed vocabulary changes semantic target, fast state, and adapted output;
- the inner API is label-free;
- higher-order outer gradients reach `W0`, key projection, and query projection, with finite-difference checks through the inner update;
- static control and finiteness diagnostics work;
- the implementation stays within T001 scope.

### Scientific interpretation
This ACCEPTS **mechanism feasibility only**. It does not establish that the proposed semantic target is useful for OVD, that nonlinear fast weights beat activation-only vocabulary conditioning, that meta-learning `W0` matters, or that detection accuracy improves. The current `T -> -T` sensitivity test is deliberately diagnostic and is not semantic evidence.

The next task therefore remains detector-agnostic. Before Grounding-DINO integration, we need one controlled experiment that can falsify the scientific mechanism rather than merely exercise it.

---

## ACTIVE TASK — T002

**Title:** Controlled episodic semantic benchmark for fast-weight value beyond static/activation baselines

**Status:** ACTIVE

### Research goal
Build a small synthetic episodic benchmark that tests H2/H4/H5 from `research/TOVD_RESEARCH_SPEC.md` under a strict separation between:

- **outer/meta supervision:** labels may be used to train/evaluate slow parameters and `W0` on synthetic episodes; and
- **test-time inner adaptation:** detection/class labels must never enter `L_inner` or the fast update.

The scientific question is:

> Given the same dynamic vocabulary information, does writing image+vocabulary context into fast weights provide useful held-out discrimination beyond a static model and beyond activation-only vocabulary conditioning?

Do **not** integrate a detector yet.

### Required episodic setup
Create a reproducible synthetic semantic world with enough structure that the answer is nontrivial.

At minimum:
1. Sample latent class/semantic prototypes `z_c`.
2. Generate text embeddings `T_c` and visual/query observations from related but non-identical transforms/noisy views of `z_c` so the modalities are aligned but not identical.
3. Each episode contains an image-like token set `X`, object/query tokens `Q`, a **dynamic vocabulary subset** `T`, and outer labels identifying the correct vocabulary item for each query.
4. Include distractor/background visual tokens.
5. Support a controllable vocabulary-hardness parameter that creates semantically confusable classes (e.g. prototype clusters / near neighbors) and at least two regimes: easy/coarse and hard/fine-grained.
6. Split latent classes/prototypes into meta-train and held-out meta-test sets. The final reported result must include held-out classes/vocabularies not used as outer labels during meta-training.

The exact generator is an engineering choice, but document it mathematically and keep it small enough for fast controlled sweeps.

### Proposed method
Reuse T001 semantic fast memory:

`K = P_k(X)`

`S = softmax(K T^T / tau) T`

`W* = W0 - eta * grad_W L_inner(F_W(K), S)`

`Q' = F_{W*}(P_q(Q))`

Use the same text embeddings `T` for the outer episodic classifier, e.g. normalized query-text similarity followed by cross-entropy. Outer loss may backpropagate through the inner update during meta-training.

### Mandatory matched baselines
Implement and compare under matched embedding dimension and training episodes:

**B0 — Static:** no vocabulary-conditioned adaptation; use the learned static query representation / `W0` path.

**B1 — Activation-only vocabulary conditioning:** give the query explicit access to the same current vocabulary without fast-weight learning. A simple direct query-to-text attention/context fusion is acceptable. This baseline is mandatory because T001's disable-TTT control ignores `T` and is not a scientifically fair comparison for H2.

**B2 — Generic visual TTT control:** replace the OVD-specific semantic target with a vocabulary-agnostic visual target (`K -> V_visual` or an equivalently simple ViT^3-like control) while matching inner steps/model capacity as closely as practical.

**P — Proposed semantic TTT:** `K -> S(X,T)` fast semantic update.

For H4, evaluate proposed semantic TTT with:
- meta-learned `W0`;
- fixed/random initialization under the same inner-update budget.

Optional only if cheap: linear fast model versus gated MLP. Do not let this delay the required comparisons.

### Training/evaluation protocol
- Use deterministic seeds and at least 3 independent seeds for the headline synthetic result if runtime is modest.
- Meta-train slow parameters/`W0` on training episodes.
- Evaluate on held-out class/vocabulary episodes without any outer optimization at evaluation time.
- At evaluation time, the only per-episode optimization allowed is the label-free inner update defined by the method/control.
- Outer labels are used only to compute evaluation metrics after prediction.
- Keep one inner step as the primary setting; a small 0/1/2-step diagnostic is allowed after the main comparison.

### Primary metrics
Report for each method and hardness regime:
- held-out query classification top-1 accuracy;
- cross-entropy/NLL or equivalent calibrated loss;
- correct-class margin over strongest distractor;
- `||W* - W0||`, inner loss before/after, and inner gradient norm for TTT variants;
- representation shift `||Q' - Q0||`;
- mean/std across seeds.

Also report parameter counts and approximate per-episode extra compute for B1/B2/P so a gain is not hidden behind a gross capacity mismatch.

### Mechanism analyses required
1. **Vocabulary dependence:** for fixed latent scene/query, switch between an easy/coarse vocabulary and a hard/fine-grained/confusable vocabulary. Measure fast-state and output changes.
2. **Hardness trend:** test whether proposed-vs-baseline gain grows as vocabulary becomes more confusable. This is the synthetic proxy for H5.
3. **Meta-initialization value:** compare learned `W0` vs random/fixed `W0` at identical inner steps and learning rate.
4. **Semantic-target value:** compare proposed semantic TTT vs generic visual TTT.
5. **Fast-weight value beyond activations:** compare proposed semantic TTT vs B1 activation-only conditioning. This is the most important T002 comparison.

### Guardrails / anti-cheating checks
- No class label may be passed to the inner module or used to form `S` / `L_inner`.
- Ensure held-out class prototypes are not reused in meta-training outer labels.
- Do not construct `X/Q` so that the correct class index is trivially encoded by tensor position.
- Shuffle vocabulary order independently per episode and verify metrics are invariant to consistent label remapping.
- Include a text-vocabulary permutation test and at least one negative-control episode with unrelated vocabulary.
- Preserve episodic reset.
- Keep train/test generators and random seeds explicit in receipts.

### Decision thresholds
T002 is scientifically encouraging only if the held-out results show a reproducible pattern, not a single lucky seed. The strongest desired evidence is:

1. `P > B0` on held-out classes;
2. `P > B2` showing the OVD-specific semantic target matters;
3. `P > B1` showing fast weights add value beyond simply exposing activations to the vocabulary;
4. learned `W0 >` fixed/random `W0` under the same update budget;
5. the relative gain of P does not vanish—and preferably increases—in the harder/confusable vocabulary regime.

Do not manufacture thresholds or tune the generator solely to force all inequalities. If one fails, report the failure and analyze it. A negative result is useful and may trigger redesign before detector integration.

### Required artifacts
Suggested additions:
- `tovd/synthetic/semantic_episodes.py`
- `scripts/train_synthetic_semantic.py`
- `scripts/eval_synthetic_semantic.py`
- `tests/test_synthetic_semantic.py`
- `research_log/t002/...` configs, metrics, and plots/tables as machine-readable JSON/CSV plus concise Markdown summary.

Reuse existing module/tests rather than rewriting T001.

### Acceptance criteria for Research Lead review
T002 is ready for review only when:
- all pre-existing T001 tests still pass;
- generator leakage/permutation/reset tests pass;
- B0, B1, B2, P, and learned-vs-random `W0` are all evaluated on held-out episodes;
- at least easy and hard/confusable vocabulary regimes are reported;
- exact commands/config/seeds and environment are recorded;
- Codex updates `coordination/CODEX_TO_CHATGPT.md` with both successes and failures and the tested commit SHA.

### Non-goals
- no Grounding-DINO integration yet;
- no COCO/LVIS download;
- no claim of OVD accuracy gain;
- no continual adaptation;
- no large architecture search.

If T002 supports the mechanism, T003 will likely be a minimal Grounding-DINO integration with a tightly controlled ablation. If activation-only conditioning matches or beats fast weights, stop and report rather than forcing detector integration.
