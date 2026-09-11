# T005 preregistered direction/step diagnosis

Research assignment c7b4954 / review 246994e. T004 accepted as negative
fixed-step eligibility result. This plan is committed before T005 aggregate
outcomes. No training, detector integration, new objective or T006.

## Fixed experiment and reuse

Reuse original T002 P checkpoints seeds 7/17/27, all 100 easy and 100 hard
held-out episodes per seed, original world/split/episode seeds, O0 and O1
objectives from tested 9afe8df. Parameter count 2128, eta .05, teacher tau .2,
student/classifier temperature .1. Same tensors and original T classifier.
C0 is explicit O1_fixed, C1 O1_norm_matched, C2 O1_backtracking.

| Responsibility | Existing source | Change / test |
| --- | --- | --- |
| Input world/checkpoints | T002 semantic_episodes and checkpoint files | Unchanged; hashes/episode pairing |
| Fast functional lifecycle | fast_semantic_memory.py | One narrow update-selection hook; exact O0/C0 regression |
| O1 loss/teacher | vocabulary_objectives.py | Reuse unchanged; no labels in controller APIs |
| Step controllers | New isolated module | C1 equation/gradient, C2 first Armijo acceptance |
| Offline scoring | T003 oracle gradient/metrics + T004 aggregation | Reuse; labels confined to research_log/t005 |
| Remote execution | Existing AutoDL workflow and project venv | Same A6000 CPU/CUDA tests and receipts |

## Controller definitions

C0: existing O1 gradient g1 and update -.05*g1, exact T004 control.
C1: label-free O0 gradient g0 is budget only. Use scale=norm(g0)/(norm(g1)+eps),
eps=1e-12, update -.05*scale*g1. If norm(g1)<=eps or either gradient norm is
non-finite, keep W0 and record guarded flag. This is the explicitly requested
small near-zero/finite guard. Outside the guard, keep scale differentiable
through both gradients and verify realized update norm against original O0.
Numerical comparison uses atol=1e-6/rtol=1e-5 for float32, tighter float64 tests.
C2: first Armijo-satisfying eta from [.05,.025,.0125,.00625,.003125],
L1(W0-eta*g1)<=L1(W0)-1e-4*eta*norm(g1)^2. None accepted -> eta 0, rejected
flag, unchanged W0. No task scores/IDs enter the selector. Discrete selection
need not be differentiated, accepted update uses the same functional path.

## Exact interpretation rules from the research task

1. Scale rescue C1: versus C0, easy post NLL improvement >=.10 AND accuracy
   gain >=5pp, while hard NLL/accuracy do not BOTH worsen.
2. Descent safe C2: every accepted step satisfies the declared condition;
   easy post NLL <=O0+.10 AND accuracy >=O0-5pp; hard NLL <=C0.
3. Task useful: C1 or C2 hard mean NLL < own W0 AND accuracy >= own W0,
   hard NLL improves in at least 2/3 seeds, and mean task-gradient cosine
   exceeds O0 by >=.05. Report each component without changing thresholds.

Raw gradient alignment is g1 for every O1 controller, including rejected C2
steps; report realized zero updates separately, so raw direction is not
mistaken for an executed update. Dot products also include effective scaled
update direction in analysis, alongside requested raw g1/task quantities.
If no controller passes Rule 3, recommend stop/reframe. If any passes,
report to lead and wait; no meta-training follows automatically.

## Evidence and measurement

Four methods x 3 seeds x 2 regimes x 100 episodes = 2400 main records.
Preserve before/after task scores, per-query changes, raw norm/cosine/dot,
actual update norm, O1 inner loss for every method (including O0 diagnostic),
C1 scales/norm-equality error, C2 eta/trials/acceptance/RHS/margin. O0's own
inner loss is separately labeled. Report all finite flags and repeatability.
Mechanism: same original T002 paired-scene stream, 20 episodes per seed,
existing reset/vocabulary/permutation analysis. No changes to labels/streams.
Runtime: whole normal forward only, exclude oracle scoring; same 100 held-out
episodes per seed/regime. Warm up first 3, synchronize GPU before and after
each complete pass, 3 passes; report mean milliseconds and C2/C0 multiplier
per seed/regime. Cost ratios are observed wall time, not a performance claim.
Historical T003 exact-text oracle remains a reference only; do not rerun.

## Increment checks

Baseline: python -m pytest -q -> 53 passed in 11.70s before changes.
1. Narrow update hook/controller slice: exact aliases, hand equation/norm,
   near-zero guard, first Armijo choice/rejection, no-label APIs, reset,
   vocabulary change, C1 W0 finite-difference/projection gradients.
2. Offline runner: tiny checkpoint fixture, C0/O0 historical equality/hash,
   control equality and rule evaluator, generated record schema.
3. Full regression, CPU/CUDA tests, complete fixed A6000 diagnosis, results
   and all three interpretation rules reported with artifacts and source hashes.
Each increment stays within its listed files until focused tests pass.
