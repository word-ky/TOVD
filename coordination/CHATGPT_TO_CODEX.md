# CHATGPT -> CODEX

## ACTIVE TASK — T001

**Title:** Build a detector-agnostic feasibility scaffold for Vocabulary-Conditioned Fast Semantic Memory

**Status:** ACTIVE

### Goal
Implement and verify the smallest differentiable prototype of the TOVD inner-loop mechanism defined in `research/TOVD_RESEARCH_SPEC.md`. Do **not** integrate Grounding DINO yet. The purpose is to prove that the proposed image+vocabulary-conditioned fast state is mathematically and programmatically sound before we touch a large detector.

### Required module behavior

Create a clean PyTorch module that accepts at minimum:

- visual/image tokens `X`: `[B, N, D]`;
- text/vocabulary embeddings `T`: `[B, C, D]` or a clearly documented equivalent;
- object/query tokens `Q`: `[B, M, D]`.

Implement:

1. projected key/query representations;
2. vocabulary-conditioned semantic targets
   - `A = softmax(K @ T^T / tau)`
   - `S = A @ T`;
3. a small fast model `F_W`, initially use a lightweight **gated MLP** or similarly minimal nonlinear model;
4. one-step differentiable inner update
   - `W* = W0 - eta * grad_W L_inner`;
5. adapted query output
   - `Q_adapt = F_{W*}(P_q(Q))`;
6. strict **episodic reset**: every new forward starts from `W0`, not the previous batch's `W*`;
7. a switch that disables TTT and returns a static/control path.

### Inner loss
Start with cosine/dot-product alignment between `F_W(K)` and `S`. Use normalization if needed for numerical stability. Do not use any detection labels.

### Critical autograd requirement
In training/meta-learning mode, outer gradients must be able to propagate through the inner update to the meta-initialization `W0` and relevant projections (`create_graph=True` or an equivalent differentiable functional update). Avoid in-place mutation of ordinary module parameters for the inner step.

A functional-parameter implementation is preferred.

### Required tests
At minimum implement automated tests for:

1. **Shape correctness** for `X,T,Q -> Q_adapt`.
2. **Fast update occurs:** `||W* - W0|| > 0` for nondegenerate random input.
3. **Inner objective improves locally:** after one small update, inner loss should usually decrease in a deterministic synthetic test; tune the test setup rather than hiding failures.
4. **Episodic reset:** two identical forwards with identical inputs/seed produce the same output and same fast state; no leakage from the prior call.
5. **Vocabulary sensitivity:** fixed `X,Q`, different `T` must produce measurably different semantic targets and fast states/outputs.
6. **No-label guarantee:** API must not accept/use detection ground-truth labels in the inner loss.
7. **Outer gradient flow:** a dummy outer loss on `Q_adapt` must produce finite, nonzero gradients on `W0` and at least the intended projection parameters.
8. **Disable-TTT control:** static path runs and has documented behavior.
9. **Numerical checks:** no NaN/Inf in inner loss, gradients, update norm, or output.

### Diagnostics to expose
Return or optionally log:

- inner loss before update;
- inner loss after update (diagnostic re-evaluation);
- inner gradient norm;
- fast update norm `||W* - W0||`;
- vocabulary-conditioning delta in the dedicated test;
- NaN/Inf flags.

### Suggested structure
You may choose a better layout, but keep it minimal. Example:

- `tovd/models/fast_semantic_memory.py`
- `tests/test_fast_semantic_memory.py`
- `scripts/demo_fast_semantic_memory.py`
- `README.md` with one runnable command and tensor/API description.

### Non-goals for T001

- no full Grounding DINO integration;
- no dataset download;
- no COCO/LVIS evaluation;
- no large training run;
- no claim of detection accuracy improvement;
- no continual adaptation.

### Acceptance criteria for Research Lead review
T001 is ready for review only when:

- all tests pass;
- the demo runs end-to-end;
- differentiable inner update is verified;
- vocabulary sensitivity is quantitatively demonstrated;
- episodic reset is verified;
- Codex has committed the implementation and filled `coordination/CODEX_TO_CHATGPT.md` with exact evidence.

### Research question Codex should NOT decide silently
If there is ambiguity about cosine vs dot-product loss, fast-model depth, or projection sharing, choose the simplest stable version for T001 and report the choice. Do not expand scope.

---

After T001, the Research Lead will inspect the evidence and decide whether T002 should be Grounding-DINO integration, a stronger synthetic mechanism test, or a redesign of the inner target.
