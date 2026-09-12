# T007 preregistration — warm-start origin audit

Received research instructions 99e6292/742aa8b on 2026-09-12 (Asia/Shanghai).
No T007 aggregate outcomes have been produced/read. T006 report is archived.

## Fixed experiment

Reuse the complete T002 generator, splits, seeds 7/17/27, model and evaluation
config. Both branches load the exact final seed-specific T002 P state_dict:
W1 `P_O0_resume` uses P/O0; W2 `P_C2_warm` uses T006 O1+C2.
All model tensors must be byte-identical at step 0, both to source and each other.
Start a **fresh Adam optimizer in both branches**, lr .001, default Adam settings;
do not restore optimizer moments. This isolates common model origin without
mixing optimizer histories. Continue for 400 steps x4 balanced episodes.
Use training indices 1600..3199 (the next segment after T002 indices 0..1599),
with the original seed formula and alternating easy/hard construction.
No schedule/controller/objective/architecture/generator changes or tuning.
C2 eta candidates [.05,.025,.0125,.00625,.003125], Armijo 1e-4, nondifferentiated
selector and differentiable accepted update remain exactly T006.

Save model tensors at fixed steps 0/50/100/200/400. Final step 400 alone is primary.
Evaluate all trajectory checkpoints after training; no early stopping or selection.
Each trajectory evaluates W0-only, C2-adapted and the branch's training objective
on the exact 100 easy +100 hard T002 held-out streams. Evaluate the same paths
on the final 200 continuation training episodes: indices 3000+2*i (easy) and
3001+2*i (hard), i=0..99. These are seen training examples at step 400; earlier
trajectory points see some/all as future examples. Report this distinction.
Training telemetry preserves all 400 minibatch losses/accuracies/inner statistics.

## Evidence and controls

Re-evaluate original T002 B0/B1/B2/P and verify full episode identities/metrics
against retained receipts. Re-evaluate original P W0/C2 against T005 raw receipts,
and T006 random-init W0/C2 against its raw receipts. Hash all 15 source checkpoints
and compare to previously recorded hashes. Preserve all raw evaluations locally
and remotely. Original source runs: T002 20260912-023122-tovd-t002-a6000;
T005 20260912-053826-tovd-t005-a6000; T006 20260912-065105-tovd-t006-a6000.

For each new final checkpoint reuse T005 offline oracle diagnostics and T006
normal-output/W0 equality comparisons, mechanism tests and 3-pass timing.
Report W0/key/query/total parameter L2 drift. Classifier is parameter-free cosine
similarity divided by fixed .1: parameter count and parameter drift are zero;
report unchanged temperature explicitly, not a fictitious learned classifier.
W0 has 2128 fast parameters; key/query slow projections additionally train.
Report train/test NLL, accuracy, margin, per-seed paired deltas, inner loss,
raw gradients, update norms, eta/trials/zero fraction/Armijo violations,
task-gradient cosine/dot, episode/query NLL improvement fractions, vocabulary
responses, reset/replay, finite counts and latency versus matched P/O1-fixed.

## Six fixed decision rules

1. All six branch/seed runs finish 400 steps, finite; provenance, stream equality,
   label-free selection, exact common origin and normal runtime checks pass.
2. W2 hard adapted NLL < own W0 mean, accuracy >= own W0, NLL improves >=2/3 seeds.
3. W2 hard accuracy >= T005 C2 -2pp AND NLL <= T005 C2 +.03.
4. W2 must not be strictly worse than W1+C2 in both hard accuracy and NLL.
5. Same T006 convention: beat best-accuracy B0/B1/B2 by >=1pp with non-worse NLL,
   OR beat best-NLL B0/B1/B2 by >=.03 nats with non-worse accuracy. Compare both
   metrics to the same selected control in each branch; report all controls.
6. Easy adapted NLL <= own W0+.05 and accuracy >= own W0-3pp; prominently flag
   any seed with NLL harm >.10 or accuracy harm >5pp. Hard O1 cosine >= original
   O0 cosine+.05; vocabulary changes state; repeat/reset errors <=1e-6.

Report all six rules independently. Preserve the research-lead interpretation
branches verbatim in spirit: warm-start viability only with rules 2/3/5/6;
if W1 strong but W2 fails preservation/control, retain frozen adaptation;
if both lose T005 benefit, flag checkpoint-state dependence; if W2 loses both
metrics to W1, attribute the additional degradation to continuation objective.
No detector, T008, new regularizer, anchoring, distillation or rescue tuning.

## Reuse and increments

Baseline 742aa8b: `python -m pytest -q`: 75 passed in 15.63s.
Only repository-owned code reused (no external donor/dependency):
- semantic_episodes / benchmark: same world, streams, trainer/evaluator/mechanisms;
- models / step_control: existing P and C2 semantics via two explicit aliases;
- T005 oracle_step_screen and T004 summarize: same offline analysis and timing;
- T006 interpretation helpers: same control, safety and mechanism comparators.

Increment 1: narrow optional checkpoint/episode-offset/snapshot arguments on
existing train_model; explicit aliases and warm-start telemetry. Test independent
manual Adam continuation equivalence, deterministic replay, source immutability,
serialization and exact step-0 equality (P and C2 outputs against existing aliases).
Increment 2: task-local experiment orchestration/replay/rules. Tiny real source
checkpoints and end-to-end continuation/evaluation test; exercise rule boundaries.
Final: full local suite, A6000 CPU/CUDA suites, fixed six-run experiment, final
checkpoint/raw receipts/report commit and push. Each increment must pass before next.
