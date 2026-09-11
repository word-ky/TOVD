# T006 preregistered controlled C2 meta-training

Research assignment a1a585c / review 6dafb0f accepts T005 and carries C2 only.
No detector, new objective, T007 or tuning. Commit this plan before aggregate
T006 held-out outcomes. Existing T005 report archived project-locally.

## Fixed model and training

Reuse T002 train_model/train_synthetic_semantic, semantic world/splits/streams,
seeds 7/17/27, 400 Adam(.001) steps x4 balanced easy/hard training episodes,
final checkpoint only, exact100easy+100hard held-out episodes perseed. Config
is T002 with only methods=['P_C2_meta'] changed. No schedule change.
P_C2_meta aliases existing O1_backtracking: same2128 parameters, initial RNG
convention/tensors, O1 teacher tau.2/student.1, original T classifier, fixed
C2 sequence [.05,.025,.0125,.00625,.003125], Armijo1e-4. Eta selection stays
nondifferentiated; accepted functional update differentiates through g1 toW0
and projections with eta treated as a Python/stop-gradient scalar. Per-episode reset.
Training labels enter outer CE only. Inner loss/selector never see labels/IDs.

## Reuse and increments

| Responsibility | Existing source | Narrow change and test |
| --- | --- | --- |
| Runtime | step_control.O1StepMemory | Explicit P_C2_meta alias only; equal initialization/path |
| Training | synthetic.benchmark.train_model and existing runner | Additional requested diagnostic columns for this method; checkpoint initial state |
| Meta-gradient | Existing functional_call + C2 path | Analysis-only finite-difference/eta-boundary receipt and stable-region tests |
| Task scoring | T005 oracle_step_episode/measure_forward_passes | Use existing backtracking classifier loaded from trained checkpoint |
| Controls | T002 saved B0/B1/B2/P | Exact reevaluation and hash/stream checks, no retraining |
| Aggregate | T004 summarize and existing CSV/JSON tools | All5rules evaluated without tuning |
| Execution | Project AutoDL workflow/venv | Full CPU/CUDA tests and fixed3seed run |

Baseline full70-test suite reproduced before editing. Increments:
1. Alias + piecewise gradient/selector probes; focused tests green.
2. Trainer telemetry/checkpoint and analysis runner; tiny end-to-end save/load,
   unchanged-control comparison and rule logic tests green.
3. Full regression, CPU/CUDA, pretraining meta-gradient receipt, fixed3seed
   training, final diagnostics/control reevaluation, final report.

## Gradient/selector probe protocol fixed before training

Before training: freshly initialized C2 models for all3seeds; after training:
final checkpoints. Probe first20 training episodes perseed (10easy/10hard),
not held-out selection. CPU/device float64 copy; W0 output.weight normalized
random direction with generator seed90000000+seed*1000+index.
Perturbation epsilons [1e-5,1e-3,.01,.1] fixed for selector-stability diagnosis,
not eta/objective tuning. Record base/plus/minus selected eta at every epsilon,
outer CE analytic directional derivative and central finite difference, plus
W0/key/query outer-gradient norms and finite flags. Use finite-difference
agreement only when all selected etas match the base; assess primary numerical
agreement at epsilon1e-5 (rtol1e-4,atol1e-7). Larger perturbations diagnose
nearby selector regions and finite-step error; do not call a switched probe
a smooth-gradient mismatch. Report switch fractions by epsilon/seed/phase,
including zero fractions if no boundary crossed. Unit test an actual eta switch.
Pretraining receipt must be generated before the first400-step run; no new
training is launched until stable-region gradients are verified.

## Required evidence

Training perstep: outer loss/accuracy, inner loss before/after, rawgradient and
actualupdate norms, all4 selectedetas, trials/zero fractions, accepted Armijo
violations and finite outer gradients/parameters. Save initial full tensors
and compare historical P initial_fast_state plus seed reconstruction forprojections.
Heldout: W0/adapted paired scores, margins, episode/query NLL improvement,
O1/task raw alignment, inner losses, steps/trials/eta0/Armijo, vocabulary and
unrelated-vocabulary response, deterministic reset and nonfinite counts.
Reuse original20mechanism episodes/seed and T005 normal-forward timing:
3warmups and3full100episode passes perseed/regime. Time C2 and matched P,
O1_fixed using identical newly trained tensors; exclude oracle scoring.
Reevaluate12 historical checkpoints B0/B1/B2/P on exact T002 streams; preserve
hashes and exact original score equality. Historical frozen-C2 uses stored
T005 results only, explicitly not a newly trained control.

## Exact interpretation rules

R1: all3seeds finish400steps without nonfinite training/leakage/innerlabels;
accepted C2 updates meetArmijo, fallbacks reported, exactprovenance verified.
R2: hard mean adaptedNLL<ownW0 AND adaptedaccuracy>=ownW0, withNLLgain>=2/3seeds.
R3: beat strongest non-TTT/generic control in the improved metric, while the
other metric is no worse than the same control. Operationalize 'best' before
results as two explicit branches: highest-accuracy control for the +1pp
accuracy branch (tie:lowestNLL), lowest-NLL control for the -.03nats NLL
branch (tie:highestaccuracy). Either branch may pass; report both and all
controls. Historical hard bestaccuracy=B2(.44625,NLL1.2622662852), bestNLL=B0
(1.2600518760,accuracy.4233333333). This avoids choosing a comparator after
T006 results. Also show comparisons against every control.
R4: aggregate easy adaptedNLL<=ownW0+.05 AND accuracy>=ownW0-3pp. Flag each
seed with >.10nats or >5pp harm even if aggregatepasses; no uniform-robustness claim.
R5: hard O1/task cosine-originalO0 hardcosine >=.05; changedvocabularies alter
faststate, exactrepeat/reset errors within float32tol(atol1e-6,rtol1e-5).

All rules plus perseed failure flags reported. R2/R3 failure -> stop/reframe;
R2/R3 pass withR4instability -> stabilitywork, no detector. Even positiveall5
only supports Research Lead review for a future task; never autonomously
start detector/T007.
