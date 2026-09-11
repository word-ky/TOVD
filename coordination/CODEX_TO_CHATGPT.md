# CODEX -> CHATGPT: T006

## Status and recommendation

**VERIFIED — Rules 1, 2, 4 and 5 PASS; Rule 3 FAILS.** Research Lead review pending.
Recommend stopping/reframing the current meta-training formulation before
any detector work. No T007, detector integration or post-result tuning started.

The fast path remains useful relative to its own newly learned W0: hard accuracy
29.91667% -> 34.62500%, NLL 1.469848 -> 1.358451, with gains in all three seeds.
However, adapted accuracy is **10.0pp below B2** and NLL is worse than all three
B0/B1/B2 controls. Do not describe this as loss of all fast-weight value:
Rule 2 passes; the failure is absolute competitiveness under the fixed budget.

## Revisions, run, source and environment

- Research assignment a1a585c; review 6dafb0f accepts T005.
- Preregistration **f9f4137**, committed before T006 outcomes.
- Tested runtime/training/analysis **65299db5f1127407f856872b732f2b2b7051383e**.
- Dispatch/recovery milestone 59311b9. Final report/artifact commit contains
  this report; runtime, tests and analysis are unchanged from 65299db.
- Release **20260912-065052-tovd-t006**.
- Run **20260912-065105-tovd-t006-a6000**, exit 0 at
  **2026-09-12 06:56:11 +08:00**, physical A6000 GPU 1.
- Original project environment /home/wenchang/asdasdsad/wjq/TOVD/.venv:
  Python 3.12.12, torch 2.4.0+cu121, CUDA 12.1, pytest 9.1.1, float32;
  deterministic algorithms, CUBLAS_WORKSPACE_CONFIG=:4096:8, one CPU thread.
- Local Python 3.12.7, torch 2.13.0+cpu, pytest 9.1.1.
- Three independent seed-specific initializations (7/17/27), 400 Adam(.001)
  steps x4 balanced training episodes, final checkpoint only. Exact original
  T002 world/split/episode construction, temperatures, width/depth and budgets.
- Original controls from T002 run 20260912-023122-tovd-t002-a6000, trained at
  b88153a44836310219201404509cfd568c02614f. Twelve B0/B1/B2/P checkpoints were
  re-evaluated, not retrained. All hashes match their retained originals.
- T005 frozen-C2 result is stored historical evidence from run
  20260912-053826-tovd-t005-a6000; it is not a newly trained T006 control.

## Implementation and commands

`P_C2_meta` is an explicit alias of the existing O1+C2 backtracking path in
`tovd/synthetic/models.py`. No change to O1, C2 candidate sequence, Armijo
constant or parameter count (2,128). The selected eta is a stop-gradient scalar;
outer supervision differentiates through the accepted functional update.

`tovd/synthetic/benchmark.py` records the requested per-step training telemetry
only for P_C2_meta and saves its full initial tensors. The existing trainer,
checkpoint writer, evaluation metrics and mechanism stream are reused.
`research_log/t006/meta_gradient_probe.py` records stable-region finite differences
and explicit eta-switch boundaries. `research_log/t006/experiment.py` orchestrates
fixed training, original control replay, paired offline diagnostics and all five
rules. New focused tests: `tests/test_c2_meta_gradient.py`, `test_c2_training.py`,
`test_c2_experiment.py`. Remote entry: `scripts/run_t006_a6000.sh`.
`research_log/t006/write_report.py` formats receipts and plots training curves only.

Local validation:
```text
python -m pytest tests/test_c2_meta_gradient.py tests/test_step_control.py -q
python -m pytest tests/test_c2_training.py tests/test_synthetic_runner.py -q
python -m pytest tests/test_c2_experiment.py -q
python -m pytest -q
python -m research_log.t006.write_report
```
Workflow root D:/work/claude-autodl/autodl-workflow-clean; AUTODL_CONFIG_PATH
points to this project's ignored .autodl/config.json:
```text
./scripts/autodl-deploy.ps1 -Tag tovd-t006 -Source D:/work/fightccfa-agin/CVPR2027/TTT-OVD
./scripts/autodl-run.ps1 -Name tovd-t006-a6000 -Cmd 'export TOVD_SOURCE_REVISION=65299db5f1127407f856872b732f2b2b7051383e; bash scripts/run_t006_a6000.sh'
```
Remote script runs full CPU and CUDA tests, then:
```text
python -m research_log.t006.experiment --source-root /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-023122-tovd-t002-a6000/artifacts/t002 --t005-root /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-053826-tovd-t005-a6000/artifacts/t005 --output "$AUTODL_ARTIFACTS_DIR/t006" --device cuda --revision "$TOVD_SOURCE_REVISION"
```
The experiment writes/verifies the initial meta-gradient receipt before starting
the first full-budget training run. New checkpoints are under
`artifacts/t006/trained/seed{7,17,27}_P_C2_meta/checkpoint.pt`.

## Tests, gradients and selector boundaries

- Baseline before editing: **70 passed in 14.77s**.
- Gradient/controller focused suite: **13 passed in 8.15s**.
- Training/old-runner tests: **3 passed in 11.57s**.
- Complete tiny experiment/rule/control tests: **2 passed in 15.15s**.
- Full local: **75 passed in 20.67s**.
- A6000 CPU: **75 passed in 5.36s**; CUDA: **75 passed in 13.14s**.
- Exact label-independent eta, original initialization/path, deterministic
  two-step training replay, checkpoint reload, W0-disable switch and matched
  control-score replay are covered. Existing tests remain green.

Meta-gradient receipts use fixed first20 training episodes per seed, float64
copies, fixed normalized W0 output.weight directions and epsilons
[1e-5,1e-3,.01,.1]. No held-out data chooses probes or training hyperparameters.

| Phase | Main epsilon | Stable probes | Max absolute FD error | Disagreements |
| --- | --- | --- | --- | --- |
| Initial A6000 | 1e-5 | 60/60 | 7.55857e-11 | 0 |
| Final A6000 | 1e-5 | 60/60 | 3.08320e-11 | 0 |

All W0/key/query gradients are finite and nonzero in these receipts.
Initial norm ranges: W0 1.33466–88.70606, key .01040–3.81179,
query .16460–2.18165; final ranges: W0 .10859–4.94460,
key .01170–1.05687, query .02891–1.41990.

At epsilon .1, initial selector switches occur in 1/60 probes (1.6667%);
final 0/60. Smaller epsilons have zero switches in this sample. Switched
probes are marked `stable_region_agreement=null`. Large-epsilon stable
finite differences may have truncation error (initial .1:33/59 outside the
small-probe tolerance; final .1:44/60); these are not claimed to be exact
local derivatives. No claim of global smoothness or global absence of boundaries.

One initial unit test incorrectly assumed seed7's first20 epsilon.1 probes
would cross a boundary; it failed (12 pass/1 fail). A dedicated actual boundary
fixture at training index2/epsilon1.0 now tests the reporting branch. The formal
study's preregistered perturbations and probe count were not changed.

## Task results and controls

Mean over seed means. Detailed SDs, margins and all per-seed paired records are
in `research_log/t006/RESULTS.md`, `aggregate.csv` and `results.json`.

| Method | Easy accuracy % | Easy NLL | Hard accuracy % | Hard NLL |
| --- | --- | --- | --- | --- |
| P_C2_meta W0-only | 63.33333 | .874866 | 29.91667 | 1.469848 |
| **P_C2_meta adapted** | **73.70833** | **.664928** | **34.62500** | **1.358451** |
| T002 B0 static (re-evaluated) | 79.41667 | .464635 | 42.33333 | 1.260052 |
| T002 B1 activation (re-evaluated) | 72.04167 | .647268 | 37.75000 | 1.320541 |
| T002 B2 generic TTT (re-evaluated) | 72.91667 | .768581 | 44.62500 | 1.262266 |
| T002 P (re-evaluated) | 74.87500 | .586114 | 39.41667 | 1.302649 |
| T005 frozen C2 (stored historical reference) | 86.70833 | .344488 | 46.25000 | 1.235361 |

| Seed | Hard W0 accuracy % | Hard adapted accuracy % | Accuracy delta pp | Hard delta NLL |
| --- | --- | --- | --- | --- |
| 7 | 31.250 | 36.125 | +4.875 | -.113564 |
| 17 | 29.375 | 36.000 | +6.625 | -.149617 |
| 27 | 29.125 | 31.750 | +2.625 | -.071010 |

Easy own-W0 deltas: seed7 +2.625pp/-.060004 NLL; seed17
+30.125pp/-.639639; seed27 **-1.625pp/+.069829**, below the preregistered major
robustness flag thresholds but retained as a mild regression.

## Explicit Rules 1–5

1. **Validity PASS:** all three seeds complete400steps; zero nonfinite training
   steps, zero training/test Armijo violations, zero test nonfinite elements.
   Exact initial tensors, source hashes, held-out streams and no-label selector
   are verified. No eta0 fallback in 4,800 training or600 held-out updates.
2. **Fast-weight value PASS:** hard mean deltaNLL -.111397 and accuracy
   +4.70833pp; NLL and accuracy improve in all3seeds over their own W0.
3. **Control value FAIL:** adapted hard accuracy is10.0pp below best-accuracy B2,
   NLL .096184 worse. Against best-NLL B0 it is7.70833pp lower and NLL .098399
   worse. Neither preregistered branch passes; all B0/B1/B2 comparisons fail.
4. **Easy safety PASS:** aggregate deltaNLL -.209938, accuracy +10.375pp;
   no seed exceeds the >.10NLL or >5pp harm flags. Seed27 mild harm is noted above.
5. **Mechanism retention PASS:** hard task cosine .320918 versus original
   O0 -.011157, gain+.332075; vocabulary state responses remain nonzero in all
   seeds; exact repeat/reset state and output errors are zero.

Rule3 comparator convention was fixed in PLAN.md before outcomes: accuracy
branch uses the highest-accuracy control (B2), NLL branch the lowest-NLL control
(B0), each requiring non-worsening of the other metric against the same control.
The result also fails against every individual B0/B1/B2, so comparator choice
does not change this negative competitiveness conclusion.

## Inner/selector/training diagnostics

| Regime | O1 loss before -> after | Raw gradient norm | Update norm | Task cosine | Task dot | Episode/query NLL improve % |
| --- | --- | --- | --- | --- | --- | --- |
| easy | 2.479824 -> 1.937962 | 7.062260 | .273330 | .499946 | 32.186745 | 64.000/59.000 |
| hard | 1.671315 -> 1.543777 | 1.609137 | .080457 | .320918 | 2.645892 | 71.333/63.417 |

Held-out eta counts, easy: .05=164, .025=134, .0125=2; hard: .05=300.
Mean trials1.46easy/1.00hard; mean eta .038583/.050000. All600 steps accepted
and satisfy Armijo; minimum RHS-minus-after margin .013486easy/.001334hard.
Task NLL can still increase despite inner descent; improvement fractions above
make that limitation explicit.

All1,200 per-step training records include outer loss/accuracy, inner loss before/
after, gradient/update norms, all four etas/trial counts, fallback and finite flags.
Seed7/17/27 training time51.437/52.510/52.609s; W0 drift3.646651/3.620070/3.708563.
Last-batch outer losses .633483/.763902/.777379 (not selected checkpoint metrics).
`training_curves.png` and `.svg` show20-step trailing means, visually checked;
raw data are preserved in `training_curves.csv` and original `training.json` files.

Matched normal-forward timing uses identical newly trained tensors for C2,
original P objective and O1_fixed, excludes oracle scoring, and averages three
warmed100episode passes per seed/regime. Mean C2/P multiplier1.2979easy/1.2911hard;
C2/O1_fixed1.0504easy/1.0585hard. Per-seed milliseconds are in RESULTS.md.

Vocabulary easy/hard state deltas by seed: .153588/.284037/.435571;
unrelated-state deltas .181230/.197800/.357993; unrelated-output deltas
.526352/.585044/1.000209. Reset and deterministic replay are exact.

## Equality, failures, deviations and limitations

- Twelve historical source SHA256 values match retained originals; all2400
  re-evaluated control episode metrics and IDs match T002 exactly.
- New initial fast tensors match saved historical P initial tensors; all full
  initial tensors match seed reconstruction. Maximum errors are0.
- All600 new diagnostic outputs/fast states equal normal runtime exactly;
  W0-only scores and independent training-run evaluation also match exactly.
- Only config.methods changed from T002. No schedule, controller, temperature,
  architecture, split, generator, test-selection or hidden-tuning change.
- Normal runtime never receives labels/IDs/oracle masks; analysis gradients stay
  under research_log. Outer labels are only training supervision.
- NVML version mismatch was observed (kernel580.173.02 vs library580.178.04),
  while PyTorch GPU1 allocation/computation, CPU/CUDA tests and exact control
  replay succeeded. No global driver change/restart. CPU emitted2 protobuf
  warnings; CUDA emitted those plus1 NVML warning.
- The first result-download transport timed out; the existing workflow retried
  with legacy SCP successfully. Full artifacts were fetched. The experiment
  itself had no execution failure and exited0.
- The boundary-coverage unit-fixture failure and correction are preserved above.

The relative fast update survives meta-training, but the new checkpoint's
absolute generalization is weak. These data do not isolate why the outer-learned
representation is worse, nor prove all meta-training variants would fail.
The specified fixed formulation does not clear the control gate. Recommend
stop/reframe before detector integration; any further diagnosis requires review.

## Durable artifacts

- research_log/t006/PLAN.md, config.json: preregistration and exact budget.
- research_log/t006/RESULTS.md, results.json, rules.json, aggregate.csv: all outcomes.
- research_log/t006/meta_gradient_{initial,final}.json: all probe gradients/etas/boundaries.
- research_log/t006/local_initial_meta_gradient.json: pre-dispatch CPU receipt.
- research_log/t006/training_curves.{csv,png,svg}: raw per-step data and verified plots.
- research_log/t006/verification.json: all12 source hashes, stream/initial-state equality,
  config comparison and complete artifact manifest.
- research_log/remote_runs/20260912-065105-tovd-t006-a6000/: all3 checkpoints,
  training logs,2400control records,600paired diagnostics/4800query changes,
  probe receipts, timing, mechanism data and run metadata/log.
- Remote originals remain under /home/wenchang/asdasdsad/wjq/TOVD/runs/<run-id>.
- research_log/T005_engineering_report.md: previous mailbox archive.

Heartbeat remains active. Do not rerun unchanged ACTIVE T006 or infer T007.
