# CODEX -> CHATGPT

## LATEST REPORT

**Task ID:** T002
**Status:** VERIFIED (implementation and fixed experiment complete); research review pending
**Run ID:** 20260912-023122-tovd-t002-a6000
**Tested implementation SHA:** b88153a44836310219201404509cfd568c02614f
**Remote release:** 20260912-023118-tovd-t002
**Analysis procedure commit:** d427997

### Research-facing result
The requested benchmark ran successfully, but **the complete desired scientific
pattern is not supported**. P does not beat B0 on average, does not consistently
beat B1 across seeds, and loses to B2 on hard vocabularies in all three seeds.
Learning W0 does help compared with keeping its random initialization fixed.
No detector integration was started and no new research task was inferred.
T001 remains ACCEPTED; its report is in research_log/T001_engineering_report.md.

### Held-out results
Mean ± sample SD over seeds 7/17/27, same fixed world and matched episode streams.
Accuracy is percent; all methods use 100 episodes x 8 queries per regime per seed.

| Method | Easy accuracy | Hard accuracy | Easy NLL | Hard NLL |
| --- | --- | --- | --- | --- |
| B0 static | 79.4167 ± 8.4190 | 42.3333 ± 7.8435 | 0.4646 ± 0.1452 | 1.2601 ± 0.0770 |
| B1 activation-only | 72.0417 ± 10.2792 | 37.7500 ± 3.1918 | 0.6473 ± 0.1277 | 1.3205 ± 0.0207 |
| B2 visual TTT | 72.9167 ± 10.4928 | 44.6250 ± 5.2336 | 0.7686 ± 0.2799 | 1.2623 ± 0.0903 |
| P semantic TTT | 74.8750 ± 15.6505 | 39.4167 ± 1.3010 | 0.5861 ± 0.2686 | 1.3026 ± 0.0163 |
| P_fixed | 37.8750 ± 8.2282 | 23.9167 ± 2.3128 | 1.7837 ± 0.5262 | 1.6420 ± 0.0622 |

Cosine margin (easy/hard): B0 +0.2554/-0.0191; B1 +0.1356/-0.0124;
B2 +0.2060/-0.0199; P +0.1622/-0.0222; P_fixed -0.0650/-0.0758.
Full margin SD, per-episode/per-seed records, and all other diagnostics are saved.

Paired P-minus-control accuracy differences (percentage points, mean ± sample SD):

| Control | Easy delta | Hard delta |
| --- | --- | --- |
| B0 | -4.5417 ± 11.0837 | -2.9167 ± 6.6759 |
| B1 | +2.8333 ± 6.0497 | +1.6667 ± 3.4918 |
| B2 | +1.9583 ± 8.6262 | -5.2083 ± 4.0434 |
| P_fixed | +37.0000 ± 8.1480 | +15.5000 ± 3.5990 |

P-minus-B1 per seed: easy [+4.500, -3.875, +7.875], hard [-2.125, +2.375,
+4.750] pp. Thus positive means do not establish a stable fast-weight advantage.
P-minus-B2 on hard: [-3.875, -9.750, -2.000] pp (all negative).
The P-minus-B1 gain shrinks by 1.1667 pp on average from easy to hard;
P-minus-B2 gain shrinks by 7.1667 pp. H5 is not supported by these comparisons.
No hypothesis-test threshold or post-hoc tuning was introduced.

### Implementation / choices / reuse
- Reused T001 functional gated MLP and inner update. The only core change is
  extraction of inner_targets(); its default equation is unchanged.
- New SemanticWorld: 12 clusters x 10 classes, disjoint train/test clusters
  (80/40 classes), noisy independently rotated visual/text views of latent
  prototypes, nonlinear visual distortion, foreground/distractor/background X,
  independently shuffled vocabulary and query/token order.
- Easy vocabularies span four clusters; hard vocabularies sample within one.
  Separate paired diagnostic fixes exact X/Q while changing an anchor-containing
  easy/hard vocabulary. Unrelated vocabulary excludes the query class.
- B0 is the T001 static path. B1 adds parameter-free query-to-text context and
  mean image-to-text context to static output; it sees both X and T. B2 replaces
  semantic target with raw X; P retains S(X,T). P_fixed holds W0 constant through
  outer training while allowing the two projections to learn.
- All start from identical parameter tensors per seed: D=16, hidden=32,
  one inner step, eta=0.05, tau=0.2, cosine outer temperature=0.1.
- One shared training/evaluation implementation; Adam 0.001, 400 steps x 4
  episodes, balanced easy/hard, final checkpoint. No test-driven selection.
- Inner APIs receive X/T/Q only; labels enter outer loss or metrics after
  prediction. No test prototypes generate training observations or labels.
- No donor code imported: reuse provenance is this repository's T001 a344037.

Mathematical generator and all seed formulas are in README.md and
research_log/t002/PLAN.md. Config was committed before headline execution.

### Tests, environment and commands
Local Python 3.12.7 / torch 2.13.0+cpu / pytest 9.1.1.
- Unmodified baseline: 10 passed in 10.90s.
- Generator increment: 4 passed in 8.53s.
- Generator/models plus T001: 21 passed in 11.67s.
- Shared runner/known-metric/checkpoint mini end-to-end: 2 passed in 12.44s.
- Final local full suite: **23 passed in 11.77s**.

A6000 Python 3.12.12 / torch 2.4.0+cu121 / CUDA 12.1 / pytest 9.1.1.
- Full CPU suite: **23 passed in 2.71s**.
- Full CUDA suite: **23 passed in 4.30s**.
- Both emitted two dependency deprecation warnings from protobuf import hooks;
  these do not affect the benchmark and were left unchanged.
- 15 method/seed training jobs and both hardness evaluations completed.
- Independent saved P/seed7 checkpoint evaluation exactly reproduces metrics.
- Run finished **2026-09-12 02:39:18 +08:00**, exit **0**; no active run remains.

```text
python -m pytest -q
python -m pytest tests/test_synthetic_semantic.py -q
python -m pytest tests/test_synthetic_runner.py -q
```
From existing AutoDL workflow root with project AUTODL_CONFIG_PATH:
```text
scripts/autodl-deploy.ps1 -Tag tovd-t002 -Source D:\work\fightccfa-agin\CVPR2027\TTT-OVD
scripts/autodl-run.ps1 -Name tovd-t002-a6000 -Cmd 'export TOVD_SOURCE_REVISION=b88153a44836310219201404509cfd568c02614f; bash scripts/run_t002_a6000.sh'
```
The committed run script executes CPU tests, CUDA tests, training/evaluation,
and checkpoint re-evaluation with CUDA_VISIBLE_DEVICES=0 and
CUBLAS_WORKSPACE_CONFIG=:4096:8. Float32; one CPU thread. Exact CLI and metadata
are retained in the run's run.sh/meta.json/train.log. Results fetched via the
existing Copy-FromAutodl helper. Local analysis command:
```text
python research_log/t002/analyze_results.py research_log/remote_runs/20260912-023122-tovd-t002-a6000/artifacts/t002 --output research_log/t002
```

### Mechanism and numerical diagnostics
Means over seeds and held-out episodes:

| Variant/regime | Inner loss before -> after | Gradient norm | Update norm | Representation shift |
| --- | --- | --- | --- | --- |
| B2 easy | 0.651802 -> 0.488434 | 1.997068 | 0.099853 | 0.288265 |
| B2 hard | 0.655345 -> 0.453190 | 2.277757 | 0.113888 | 0.330118 |
| P easy | 1.054847 -> 0.528424 | 3.585605 | 0.179280 | 0.528331 |
| P hard | 1.020543 -> 0.393253 | 4.059844 | 0.202992 | 0.601469 |
| P_fixed easy | 1.009670 -> 0.831787 | 1.895013 | 0.094751 | 0.276913 |
| P_fixed hard | 1.027579 -> 0.795363 | 2.179713 | 0.108986 | 0.318980 |

Each TTT variant decreases inner loss in 600/600 evaluation episodes. All
finite flags passed. Decreasing the inner objective does not establish better
held-out classification, as the main comparisons demonstrate.

Across 20 fixed-scene pairs per seed, P easy/hard vocabulary switching gives
mean fast-state delta **0.17260549** and output delta **0.51101377**.
B1 state delta is zero but output delta is 2.03755065; B0/B2 state and output
vocabulary-switch deltas are zero, as intended. All reset state/output deltas
are exactly zero. Permutation output errors are at float32 rounding scale.
T001 higher-order finite-difference tests still pass on CPU/CUDA.
P_fixed W0 outer drift is exactly [0,0,0]; projections were trained.

Unrelated-vocabulary P: state delta 0.12346366, output delta 0.36556136,
mean maximum confidence **0.66101004**, entropy 0.77399773 nats.
This exposes confidence on absent-class queries; there is no abstention mechanism
in this scaffold. No accuracy is assigned to an unrelated-vocabulary episode.
Negative-control results are evidence, not a claimed detection or rejection gain.

### Capacity and approximate extra compute
All methods allocate **2,128 parameters**. B0's 256 key-projection parameters
are unused (effective static learned path 1,872). B1/B2/P use the same tensors;
P_fixed outer optimizer includes only 512 projection parameters.
Measured evaluation latency in ms/episode (mean ± SD over seeds):
B0 0.634 ± 0.067; B1 1.290 ± 0.140; B2 7.381 ± 0.579;
P 7.765 ± 0.034; P_fixed 7.505 ± 0.490.
P costs approximately 6.0x B1 evaluation latency in this diagnostic-rich
batch-1 prototype; do not interpret these as optimized detector FLOPs.
Training time per seed: B0 5.21s, B1 7.18s, B2 42.77s, P 42.32s, P_fixed 44.00s.

### Files and durable artifacts
Code/tests/docs changed from de51d5b are listed in
research_log/t002/artifact_manifest.txt with all generated receipt paths.
Key sources: tovd/synthetic/{semantic_episodes,models,benchmark}.py,
tovd/models/fast_semantic_memory.py (target hook), scripts/{train,eval}_synthetic_semantic.py,
scripts/run_t002_a6000.sh, tests/test_synthetic_semantic.py,
tests/test_synthetic_runner.py, README.md.

Full receipt root:
research_log/remote_runs/20260912-023122-tovd-t002-a6000/
- meta.json, run.sh, train.log
- artifacts/t002/config.json, environment.json, results.json, aggregate.json,
  table.csv, summary.md
- artifacts/t002/seed{7,17,27}_{B0,B1,B2,P,P_fixed}/: checkpoint.pt,
  training.json, metrics.json, episodes.json
- seed7_P/reevaluation.json

Analysis/recovery: research_log/t002/{PLAN.md,config.json,progress.md,
analyze_results.py,analysis.json,analysis.md,artifact_manifest.txt};
research_log/project_state.md and REMOTE.md. All checkpoints/receipts are retained
remotely and fetched locally. Full main-run artifacts total approximately 3.18 MB.

### Limitations and recommendation to Research Lead
These are three initialization/episode seeds in one fixed synthetic world,
not independent worlds or real OVD data. Fixed-W0 comparison allows projections
to co-train, so its gain reflects the benefit of allowing W0 to learn within this
training recipe; it is not evidence of an isolated meta-learning mechanism or
of adaptation superiority to a well-trained static mapping.
B1 is one documented activation baseline, not all possible activation models.
No hyperparameter/generator tuning or architecture search followed these results.

Recommend keeping detector integration deferred. H4-like initialization value
and vocabulary-dependent state are demonstrated here, but stable H2 and
semantic-target superiority are not. Before another implementation task, the
Research Lead should decide whether to redesign the inner objective or request
a targeted diagnostic separating semantic alignment from discriminative utility.
Codex has not marked research ACCEPTED/REJECTED, selected T003, or expanded scope.

## RUN HISTORY
- T001: ACCEPTED by Research Lead, de51d5b; complete archived engineering report.
- T002 increments: baseline/generator/model/runner tests green; fixed protocol
  committed at b88153a before the main A6000 run.
- T002 A6000 20260912-023122-tovd-t002-a6000: full CPU/CUDA tests and 15 training
  jobs complete, exit 0; independent re-evaluation matches; mixed/negative
  scientific evidence preserved without tuning.
