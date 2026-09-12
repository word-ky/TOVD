# CODEX -> CHATGPT

## T007 — VERIFIED; Research Lead review requested

**Outcome:** validity/fast-value/strong-control Rules1/2/5 PASS; preservation,
objective-effect and easy/mechanism Rules3/4/6 FAIL. Warm start substantially
improves on T006 random initialization, but does not establish a viable T005
successor. Do not start detector integration or T008.

### Provenance and implementation

- Research instructions99e6292/742aa8b.
- Preregistration `deeacd4`; tested implementation `e88ad88112f6486f8c7dc8458594e095528ba9f1`.
- Dispatch/recovery `ad31f89`.
- Release `20260912-083405-tovd-t007`.
- Run `20260912-083417-tovd-t007-a6000`: exit0, finished2026-09-12 08:47:19+08.
- Physical A6000 GPU1; no active TOVD run remains.
- Full original run archived in research_log/remote_runs/<run-id> (105 files).
- No runtime, test or experiment-code change after tested e88ad88. Report renderer is postprocessing only.

Files changed for implementation: tovd/synthetic/{models,benchmark}.py;
tests/test_warm_{start,experiment}.py; scripts/run_t007_a6000.sh;
research_log/t007/{PLAN.md,config.json,source_hashes.json,experiment.py}.
Final evidence: research_log/t007/{RESULTS.md,results.json,rules.json,verification.json,
aggregate.csv,task_metrics.csv,per_seed_diagnostics.csv,trajectory_metrics.csv,
training_curves.csv,training_curves.png,training_curves.svg,heldout_trajectories.png,
heldout_trajectories.svg,trajectories.json,sources.json,write_report.py,progress.md,
receipt_summary.txt}; complete raw checkpoint/evaluation/telemetry files under remote_runs.
Previous T006 mailbox archived research_log/T006_engineering_report.md.

Reused the existing trainer, P/O0 and T006 C2 semantics, generator, evaluator,
T005 oracle/timing and T004 aggregation. Only added explicit warm-start aliases,
optional initial tensors/episode offset/snapshot callback to the shared trainer,
and task-local orchestration. Oracle code remains physically outside runtime.

### Fixed protocol / bookkeeping

W1=P_O0_resume; W2=P_C2_warm. Each seed7/17/27 begins from the exact final T002 P
state_dict. Both initialize fresh Adam moments at .001, continue indices1600..3199
for400 steps x4 balanced episodes, retain original generator/config/model and C2.
Step0/50/100/200/400 checkpoints saved; final400 primary, trajectories diagnostic.
All six runs completed. No tuning, early stopping, checkpoint selection or new loss.

2128 is the **total** parameter count:1616 fast W0+256 key+256 query. Classifier is
parameter-free cosine/.1. This pretraining documentation correction changes no tensors.
Fresh Adam and the next episode segment were explicitly preregistered; this is
model warm start, not optimizer-state resume.

### Tests / commands / environment

- Baseline `python -m pytest -q`:75 passed15.63s.
- `python -m pytest -q tests/test_warm_start.py tests/test_c2_training.py`:3 passed11.33s.
  Independent manual Adam continuation, step0 equality, source immutability,
  repeatability and serialization verified for both aliases.
- `python -m pytest -q tests/test_warm_experiment.py`:2 passed16.12s.
  Complete tiny historical-source/continuation/evaluation/trajectory flow plus rule comparators.
- Final local `python -m pytest -q`:79 passed20.91s.
- A6000 CPU `python -m pytest -q`:79 passed7.07s,2 protobuf deprecation warnings.
- A6000 `TOVD_TEST_DEVICE=cuda python -m pytest -q`:79 passed20.47s,
  same2 warnings plus existing NVML warning.
- `git diff --check` passed. Full experiment exit0.

Local Python3.12.7 / torch2.13.0+cpu; remote Python3.12.12 / torch2.4.0+cu121 /
CUDA12.1 / RTX A6000. Deterministic float32, one CPU thread, CUDA_VISIBLE_DEVICES=1,
CUBLAS_WORKSPACE_CONFIG=:4096:8. Complete environment/config stored in results.json.

Deployment from D:/work/claude-autodl/autodl-workflow-clean using project-local
AUTODL_CONFIG_PATH:

```powershell
./scripts/autodl-deploy.ps1 -Tag tovd-t007 -Source D:/work/fightccfa-agin/CVPR2027/TTT-OVD
./scripts/autodl-run.ps1 -Name tovd-t007-a6000 -Cmd 'export TOVD_SOURCE_REVISION=e88ad88112f6486f8c7dc8458594e095528ba9f1; bash scripts/run_t007_a6000.sh'
./scripts/autodl-logs.ps1 -RunId 20260912-083417-tovd-t007-a6000 -Lines 20
```

Experiment command (after CPU/CUDA tests):
```bash
python -m research_log.t007.experiment --source-root /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-023122-tovd-t002-a6000/artifacts/t002 --t005-root /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-053826-tovd-t005-a6000/artifacts/t005 --t006-root /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-065105-tovd-t006-a6000/artifacts/t006 --output "$AUTODL_ARTIFACTS_DIR/t007" --device cuda --revision "$TOVD_SOURCE_REVISION"
```

Fetched the explicit run with Copy-FromAutodl; generated report using:
`python -m research_log.t007.write_report --run D:/work/fightccfa-agin/CVPR2027/TTT-OVD/research_log/remote_runs/20260912-083417-tovd-t007-a6000`.

### Primary hard outcomes

| Checkpoint/path | Accuracy % | NLL |
| --- | --- | --- |
| Original T002 P W0 |40.541667|1.313905|
| T005 frozen C2 |46.250000|1.235361|
| T006 random C2 W0 |29.916667|1.469848|
| T006 random C2 adapted |34.625000|1.358451|
| W1 O0 resume W0 |40.875000|1.252460|
| W1 O0 resume+C2 |45.375000|1.220324|
| W2 C2 warm W0 |38.916667|1.308197|
| W2 C2 warm adapted |43.541667|1.227928|
| T002 B0 |42.333333|1.260052|
| T002 B1 |37.750000|1.320541|
| T002 B2 |44.625000|1.262266|

Rule1 PASS: all2400 training steps finite,0 Armijo violations;15 source hashes
match prior committed receipts; common origin byte-equal; all historical2400
control episodes and1200 W0/C2 reference pairs replay exactly; all1200 final oracle
records match normal outputs/states/W0 metrics exactly. Config differs only methods.
Step0 W0/C2 replay of both new branches also matches T005 exactly.

Rule2 PASS: W2 hard +4.625pp / NLL-.080269 versus own W0; all3 seeds improve
both accuracy and NLL (seed7 +6.5pp/-.089012;17 +5.5pp/-.093628;27 +1.875pp/-.058168).

Rule3 FAIL: W2 versus T005 hard -2.708333pp exceeds2pp allowance, although NLL
improves .007433. W1+C2 preserves hard reference within allowance (-.875pp,
NLL-.015036).

Rule4 FAIL: W2 versus matched W1+C2 hard -1.833333pp / NLL+.007603. W2 wins
seed17 but loses seeds7/27; this is a mean objective-specific effect, not uniform.

Rule5 PASS through best-NLL control B0: NLL improves .032124 with accuracy
+1.208333pp. Accuracy branch against B2 fails (-1.083333pp, although NLL-.034338).
Do not report this as another T006 strong-control failure.

Rule6 FAIL: aggregate W2 easy passes (77.166667% ->88.875%; NLL.549442->.305853),
but seed27 worsens92.5%->84.875% (-7.625pp), NLL.242851->.357217 (+.114365),
exceeding both preregistered seed flags. Hard cosine .197451 is +.208607 over
original O0; vocabulary response and exact reset/replay pass. Failure is seed safety.

### Additional limitations / mechanism / training evidence

W1+C2 has its own major **easy** failure: W0 80.958333%/.404780 ->74.166667%/.667092,
accuracy -6.791667pp / NLL+.262312. All3 easy seeds have positive NLL harm;
seed7/27 accuracy harms11pp/9.125pp. Do not treat W1 as globally safe just because
its hard performance survives. T005 is a fixed-checkpoint reference, not arbitrary
checkpoint/continuation safety evidence.

On seen continuation training episodes, common-C2 hard accuracy/NLL are
W1 64.791667%/1.004811 vs W2 62.583333%/1.092444. The W2 disadvantage already
appears on seen-training examples; it is not solely extra held-out overfitting.
Own-objective training hard accuracy:W1(O0)74.208333%, W2(C2)62.583333%.
Fixed-budget evidence cannot identify asymptotic optimization limits.

Final offline mean diagnostics (easy/hard):
- W2 O1 inner loss2.432795->2.090902 /1.643967->1.512003;
  raw grad8.202550/1.776112; update norm.215335/.088806;
  cosine.399848/.197451; dot30.836572/2.209166;
  episode NLL improves63.6667%/62%; query NLL improves53.5833%/59.875%.
- W1 O1 cosine.125585/.113345; inner loss2.311432->2.037087 /1.631315->1.535023;
  raw grad7.982174/1.792232; update norm.191344/.088601.
- Every accepted C2 update satisfies Armijo; all training/evaluation eta-zero counts0.
- All6 checkpoint vocabulary/unrelated-state responses nonzero; reset/repeat errors0.
- W2 normal C2/P timing1.3483x easy/1.2736x hard; C2/O1-fixed1.1003x/1.0471x.
- W1 normal C2/P1.3707x/1.3735x; C2/O1-fixed1.1231x/1.0759x.
- Per-seed drifts, eta histograms/trials, distributions and all paths in RESULTS.md/CSV/JSON.
- Training/held-out trajectory figures and30 fixed snapshot files retained; none selected post hoc.

### Failures / deviations / next action

No training/test/experimental failure. Existing remote NVML mismatch warning
remained nonblocking for CUDA; no driver/global environment changes.
Postprocessing initially failed with duplicate local OpenMP runtimes because the
renderer imported the torch-dependent experiment module merely to read JSON.
Removed that unnecessary dependency and used standard-library JSON; figures then
rendered and were visually checked. No unsafe OpenMP override, retraining or
experimental-code change. One exploratory absent conftest.py read was inconsequential.

Recommend retain the original frozen-T005 mechanism evidence and address the
observed checkpoint/seed dependence before detector work. Warm start repairs much
of the random-init quality deficit, yet fails preservation, objective comparison
and seed safety. Do not add anchoring/distillation/learned-controller rescue tricks
without a new research task. Await Research Lead decision; heartbeat remains active.
