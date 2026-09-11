# T004 preregistered objective comparison

Research instruction: 07bd12c / ac5f2d1. T003 accepted, branch C primary.
This plan is committed before aggregate Phase-1 results are read. No detector
integration, architecture/generator change, eta/tau sweep or hidden tuning.

## Reuse and objective contract

Keep the T002 world/config, seeds [7,17,27], initial tensors, six fast-MLP
parameters (2,128 total parameters), one step eta=.05 and assignment tau=.2.
O0 aliases P exactly. Add one inner-objective hook to the existing functional
update; default cosine objective and old checkpoints retain exact behavior.

O1: cross-entropy from detached A=softmax(K T^T/.2) to student distribution
softmax(cos(F_W(K),T)/.1). O2: T_rel=normalize(T-mean_vocab(T),eps=1e-6),
then original cosine loss against softmax(K T_rel^T/.2)T_rel. O3: detached
relative teacher softmax(K T_rel^T/.2), student cos(F_W(K),T_rel)/.1, full
distribution cross-entropy. Student temperature .1 equals the existing outer
classifier temperature. O1/O3 teacher stop-gradient is intentional; gradients
still flow through F_W(K), the functional update and W0. No oracle information
enters runtime code. Centering epsilon is the requested degenerate-vocabulary
handling, with no other new validation layer.

Outer classification remains against original T for every objective. Runtime
diagnostic semantic_targets for O1/O3 may retain A*T as an inspection snapshot,
but the actual inner loss uses the full distribution, never that barycenter.

## Phase 1 and operational gate (fixed before results)

Use T002 P checkpoints from run 20260912-023122-tovd-t002-a6000, all three seeds,
100 easy and 100 hard episodes each, original test seed formula. Evaluate
O0/O1/O2/O3 at the same W0, no retraining. Task-gradient comparisons and
assignment correctness/margins are explicitly offline oracle diagnostics.
Retain source hashes, raw per-episode/query/token records and T003 exact-text
reference; do not rerun or present the oracle as a deployable candidate.

The research instruction leaves 'material' and 'catastrophic' unquantified.
Engineering operationalization, recorded now and not adjusted after screening:
- A candidate materially improves hard if its paired mean ΔNLL is at least
  0.02 nats lower than O0 OR its mean inner/task cosine is at least 0.05 higher.
  These are meaningful absolute changes relative to T003's near-zero alignment
  and roughly .01-nat hard NLL effect; they are not significance thresholds.
- Easy regression is disqualifying if mean post-update NLL exceeds O0 by more
  than 0.10 nats OR mean accuracy is more than 5 percentage points below O0.
- A candidate must meet the material condition and avoid both easy limits.
- If none qualify: STOP and report; no Phase 2.
- Otherwise select up to two QUALIFYING candidates by lowest hard mean actual
  ΔNLL from own W0, exact ties broken by higher hard mean task cosine.
  Record candidate names/results/selection before any Phase-2 training.

No Phase-1 gain is a headline method claim: frozen W0 was trained for O0.

## Conditional Phase 2

Reuse the shared T002 trainer/evaluator, selected method names only. Same Adam
.001, 400 steps x 4 balanced episodes, seeds [7,17,27], same initial tensors,
same final-checkpoint-only evaluation on 100 held-out episodes per regime.
No hyperparameter change. Compare against own W0, frozen T002 P/B0/B1/B2,
and the historical oracle as a non-deployable reference only.
Run the same objective-specific oracle diagnostics after training, including
alignment and assignment/relative margins. Preserve per-seed paired deltas.

Success criterion 1: hard mean NLL and accuracy improve over own W0, with
accuracy gain in at least 2/3 seeds. Criterion 2: hard mean NLL and accuracy
improve over historical O0/P. For criterion 3's 'clearly better alignment',
use the same preregistered +0.05 mean cosine change versus O0 and positive
cosine change in at least 2/3 seeds. Cosine is magnitude-normalized; also
report gradient/update norms so a large-step-only explanation is visible.
All three must hold. If none satisfy them, report negative and recommend
stopping/reframing before detector integration. Do not implement T005.

## Increment checks

1. Reproduce existing 30 tests; commit this plan.
2. Narrow objective hook and O0-O3 runtime methods: exact O0/P equality,
   matched parameters, loss equations/teacher stopgrad, reset/permutation,
   label-free signatures, W0/projection gradient flow and W0 finite difference,
   finite zero/identical/near-identical vocabularies. Keep prior tests green.
3. Analysis-only frozen runner: exact O0/T003 pairing, source checkpoint hash
   preservation, diagnostics equal normal objective updates, test fixed gate
   behavior and record schema on tiny fixtures.
4. Full CPU/CUDA regression and full A6000 Phase 1. Publish gate decision.
5. Only if eligible, train selected candidates and complete conditional tests,
   fixed-budget run, frozen-control comparisons and final report.
