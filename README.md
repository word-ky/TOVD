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

## T002: controlled held-out semantic benchmark

The fixed protocol is in `research_log/t002/config.json` and `PLAN.md`.

```bash
python -m scripts.train_synthetic_semantic --config research_log/t002/config.json --device cpu --output research_log/t002/local_run
python -m scripts.eval_synthetic_semantic --checkpoint research_log/t002/local_run/seed7_P/checkpoint.pt --device cpu --output research_log/t002/local_run/reevaluation.json
```

Use `--device cuda` with `CUBLAS_WORKSPACE_CONFIG=:4096:8` for the A6000 run.
`scripts/run_t002_a6000.sh` runs CPU/CUDA suites, the fixed three-seed comparison,
and independent checkpoint re-evaluation. Remote archives pass the tested SHA
with `--revision`. `TOVD_TEST_DEVICE=cuda python -m pytest -q` exercises the
model/runner tests on CUDA; generator-only tests remain on CPU.

For unit cluster center u and residual e, class c has
`z_c = normalize(u_cluster(c) + 0.35 e_c)`. Sample independent fixed orthogonal
rotations R_t/R_v. Text is `normalize(z_c R_t + 0.02 epsilon_c)`; each visual
observation is `normalize((z_c + 0.15 tanh(2 z_c)) R_v + 0.10 epsilon)`.
All epsilon entries are independent standard Gaussians. The world has 120
classes in 12 clusters; first 8 clusters/80 classes are training and last
4 clusters/40 classes are held out. Test centers/classes never generate training
observations or outer labels. Shared modality transforms transfer across splits.

Easy vocabularies contain one class from each of four clusters; hard vocabularies
contain four classes in one cluster. Each episode has two foreground classes,
eight query observations, and 32 image tokens (16 foreground, 8 excluded-class
distractors, 8 random background), all independently sampled/shuffled. Vocabulary
positions are independently permuted. Labels map class identity to the current
vocabulary only in outer training/evaluation, and are never model arguments.

Five matched paths share the T001 parameter layout and seeded initialization:
B0 static; B1 static output plus query-to-text and mean image-to-text context;
B2 one-step K-to-X visual TTT; P one-step K-to-S semantic TTT; P_fixed same as P
with random W0 excluded from the outer optimizer throughout training. In
P_fixed, both projections still train and W0 still requires gradients for the
inner step. B1 adds no parameters and has access to both image and vocabulary.
B0's key projection is allocated for matching but unused; report effective
outer parameter ownership along with total count when interpreting capacity.

The outer classifier uses cosine similarity / 0.1 followed by cross-entropy.
All methods use Adam 0.001, 400 steps of four episodes with alternating easy/hard
examples, and identical episode streams per seed. Evaluation is 100 episodes
per regime with held-out classes, no outer optimizer, and the final checkpoint.
Seeds 7/17/27 vary initialization and episodes in one fixed semantic world.

Outputs include complete training curves/checkpoints, per-episode metrics,
per-seed diagnostics, config and environment/class-split receipts, a JSON/CSV
aggregate and Markdown table. Accuracy SD is sample SD across seed means, not
query-level error bars. Margin is correct cosine minus strongest distractor
cosine. Representation shift is the Frobenius norm from the same model's static
W0 query path. Batch-1 latency is measured after 3 warmups over 10 forwards,
including diagnostics and synchronizing CUDA at the boundaries.

Paired diagnostics preserve exact X/Q while changing an anchor-containing
easy/hard vocabulary; unrelated vocabularies exclude the query class, so their
reported outcomes are confidence/entropy and state/output shifts, not accuracy.
No-label, permutation, reset, split isolation, fixed-W0 and checkpoint tests are
in `tests/test_synthetic_semantic.py` and `tests/test_synthetic_runner.py`.
