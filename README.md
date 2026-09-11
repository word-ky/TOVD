# TOVD: fast semantic memory feasibility

T001 implements a detector-agnostic, label-free inner update. It establishes
synthetic mechanism feasibility, **not detection accuracy or novelty**.

```bash
python -m pip install -e ".[test]"
python -m pytest -q
python -m scripts.demo_fast_semantic_memory --device cpu --output research_log/demo_cpu.json
```

For CUDA, run the same demo with `--device cuda` and set
`CUBLAS_WORKSPACE_CONFIG=:4096:8` before starting Python for deterministic CUDA
matrix multiplication. Pass `--revision <tested-commit>` in deployed archives
that have no `.git` directory. Tests run in float64 on CPU; the demo also uses
float64 and can run on GPU. This is a correctness scaffold, not a speed benchmark.

```python
from tovd.models import FastSemanticMemory

memory = FastSemanticMemory(dim=256, inner_lr=0.05, tau=1.0)
result = memory(X, T, Q)  # X[B,N,D], T[B,C,D], Q[B,M,D]
Q_adapt = result.tokens  # [B,M,D]
control = memory(X, T, Q, enable_ttt=False).tokens
```

The input embeddings share dimension D. Key and query projections are separate
linear maps without bias. There is no text projection or attention normalization:
`K=P_k(X)`, `S=softmax(K @ T.transpose(-1,-2)/tau) @ T` exactly.
Use positive `tau` and nonempty token/vocabulary axes. Inputs and model must
share dtype/device. Each image gets its **own** functional fast state; changing
one batch member cannot modify another image's adaptation.

The gated MLP is `Linear_out(GELU(Linear_value(z)) * sigmoid(Linear_gate(z)))`,
with hidden size `2D`. All six MLP weight/bias tensors form W0; only those
tensors receive the inner update. The cosine loss averages over the image's N
tokens. One SGD step uses a fixed learning rate. Targets remain differentiable
in training, including their dependence on K. W0 and both projections are slow
outer parameters; an outer optimizer can optimize `memory.parameters()`.

Every forward begins from W0; functional updates never mutate module parameters,
buffers, or `.grad`. Training uses `create_graph=True` to differentiate through
the inner gradient. `memory.eval()` uses `create_graph=False`; it is intended
for inference, not meta-training. `torch.no_grad()` is supported for inference
by enabling gradients just for adaptation. `torch.inference_mode()` is outside
this prototype's supported usage.

The static control is exactly `F_W0(P_q(Q))`: it ignores X/T and performs no inner
step. It preserves the same learned MLP and query projection as the adapted path.
It is a module control, not a complete detector baseline.

`result.fast_state` contains detached, cloned per-image parameter snapshots,
each with leading dimension B. `semantic_targets` is a detached diagnostic
snapshot; the internal training target is not detached. Diagnostics contain
per-image inner loss before/after, gradient norm, update norm, and an all-finite
flag. The control returns `semantic_targets=None` and empty diagnostics.

Tests cover the exact target formula, update and local loss decrease, vocabulary
sensitivity and permutation invariance, reset after an intervening episode,
batch isolation, label-free API, static control, numerical finiteness, and outer
gradients. Directional finite differences check W0 and P_k through the complete
inner update, ruling out a merely nonzero direct gradient on W0.

Research instructions and reports live in `coordination/`; experiment receipts
and recovery notes live in `research_log/`.
