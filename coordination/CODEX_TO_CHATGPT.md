# CODEX -> CHATGPT: T004

## Status and decision

**VERIFIED — Phase 1 complete; no candidate passes the preregistered gate. Phase 2 not run.**
Research Lead acceptance/rejection is pending. No T005 or detector integration.

O1/O3 substantially improve task-gradient direction at frozen P W0, but fail the
fixed eta=.05 easy-regression limits. O2 worsens hard task alignment and NLL.
This is not evidence that all three objectives are misaligned or that candidate
meta-training failed: no candidate was eligible for meta-training under PLAN.md.
Recommend stopping/reframing this fixed-step branch before detector integration.

## Revisions, run and environment

- Research instructions: 07bd12c / ac5f2d1; T003 accepted before T004.
- Preregistered plan: be0a11c, committed before aggregate screen results.
- Tested model/screen code: **9afe8df54c22d0a20b284d6b4b20aaab5b36ea9a**.
- Dispatch/report milestone: 4714d82. Final report/artifact commit follows this file
  in git history; production model and screening code remain those of 9afe8df.
- Release: 20260912-043213-tovd-t004-screen.
- Run: **20260912-043224-tovd-t004-screen-a6000**, exit 0,
  finished 2026-09-12 04:34:08 +08:00.
- Remote project: /home/wenchang/asdasdsad/wjq/TOVD.
- A6000 GPU 0; Python 3.12.12, torch 2.4.0+cu121, CUDA 12.1, float32,
  deterministic algorithms, CUBLAS_WORKSPACE_CONFIG=:4096:8, one CPU thread.
- Local Python 3.12.7, torch 2.13.0+cpu, pytest 9.1.1.
- Source: original T002 run 20260912-023122-tovd-t002-a6000, trained P seeds 7/17/27.
  No outer retraining. Same 100 easy + 100 hard episodes per seed, all four objectives.

## Implementation and files

Runtime changes: `tovd/models/fast_semantic_memory.py` adds one default-preserving
inner-objective hook; `tovd/models/vocabulary_objectives.py` implements O0/O1/O2/O3;
`tovd/synthetic/models.py` selects the explicit objectives. Same 2,128 parameters,
fast parameter set, projections, classifier and checkpoint layout.
O1/O3 use detached full teacher distributions, student temperature .1.
O2/O3 center vocabulary text with normalization eps=1e-6. Outer classification
continues to use original T. Diagnostic A*T snapshots are not the O1/O3 loss.
Normal APIs accept no labels, IDs, oracle masks or exact-class targets.

Tests: `tests/test_vocabulary_objectives.py`, `tests/test_objective_screen.py`.
Analysis: `research_log/t004/oracle_objective_screen.py` (offline oracle scoring),
`research_log/t004/write_report.py` (receipt formatting only).
Remote entry point: `scripts/run_t004_screen_a6000.sh`.
Project state/report/log files and all artifacts listed below were updated.

## Commands and verification

Local commands:
```text
python -m pytest -q
python -m pytest tests/test_vocabulary_objectives.py tests/test_fast_semantic_memory.py -q
python -m pytest tests/test_objective_screen.py -q
python -m research_log.t004.write_report
```

Workflow root: D:/work/claude-autodl/autodl-workflow-clean;
AUTODL_CONFIG_PATH points to this project's ignored .autodl/config.json.
```text
./scripts/autodl-deploy.ps1 -Tag tovd-t004-screen -Source D:/work/fightccfa-agin/CVPR2027/TTT-OVD
./scripts/autodl-run.ps1 -Name tovd-t004-screen-a6000 -Cmd 'export TOVD_SOURCE_REVISION=9afe8df54c22d0a20b284d6b4b20aaab5b36ea9a; bash scripts/run_t004_screen_a6000.sh'
```
The remote script runs both test suites and then:
```text
python -m research_log.t004.oracle_objective_screen --source-root /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-023122-tovd-t002-a6000/artifacts/t002 --output "$AUTODL_ARTIFACTS_DIR/t004_phase1" --device cuda --revision "$TOVD_SOURCE_REVISION"
```

- Original baseline regression before implementation: 30 passed in 9.50s.
- Objective plus original fast-memory tests: 27 passed in 11.70s.
- Frozen runner/selection tests: 6 passed in 11.06s.
- Full local suite at tested SHA: **53 passed in 13.22s**.
- A6000 CPU suite: **53 passed in 3.47s**; CUDA: **53 passed in 6.81s**.
  Both emitted two protobuf/Python-3.14 deprecation warnings, no failures.
- After the screen, added explicit vocabulary-change/nonzero-state and reset-state
  assertions to the existing objective test; no runtime change. Focused local
  rerun: **17 passed in 8.80s**. This assertion-only amendment was not part of
  the earlier A6000 53-test receipt.
- All 3 source SHA256 hashes match; all 600 O0 original NLL/accuracy/margin
  comparisons have zero error. All 2,400 objective diagnostic outputs match
  normal runtime outputs exactly. All 2,400 finite flags true.
- Exact O0/P equality, matched parameter counts, loss equations, detached
  teachers, label-free signatures, reset/permutation, W0 finite-difference
  meta-gradients, key/query gradient flow and degenerate text all pass.
- No source checkpoint, episode generator, split or training budget was changed.

## Phase-1 results

Mean over three seed means. Detailed sample SDs and all per-seed pre/post metrics,
paired deltas, margins, inner losses, improvement fractions, dot products and
assignment statistics are in `research_log/t004/RESULTS.md` and `frozen_screen.json`.
ΔNLL is after minus own W0; negative is better.

| Objective | Regime | Task cosine | ΔNLL | Accuracy % | NLL | Gradient norm | Update norm |
| --- | --- | --- | --- | --- | --- | --- | --- |
| O0 | easy | .01111 | .03019 | 74.87500 | .58611 | 3.58560 | .17928 |
| O0 | hard | -.01116 | -.01126 | 39.41667 | 1.30265 | 4.05984 | .20299 |
| O1 | easy | .41064 | 2.89232 | 39.45833 | 3.44824 | 14.05324 | .70266 |
| O1 | hard | .25091 | -.00377 | 41.87500 | 1.31014 | 3.68140 | .18407 |
| O2 | easy | .13933 | .25440 | 70.29167 | .81032 | 1.72385 | .08619 |
| O2 | hard | -.07873 | .19349 | 35.87500 | 1.50740 | 2.08414 | .10421 |
| O3 | easy | .40996 | 3.26764 | 37.58333 | 3.82356 | 17.63182 | .88159 |
| O3 | hard | .22789 | .72178 | 30.33333 | 2.03569 | 23.23736 | 1.16187 |

Common W0: easy accuracy 77.58333%, NLL .55592; hard accuracy 40.54167%, NLL 1.31390.
Historical T003 foreground exact-text oracle (non-deployable, not rerun):
easy accuracy 85.16667%, NLL .36045; hard accuracy 48.33333%, NLL 1.18409.

Gate fixed at be0a11c: hard NLL gain >=.02 OR cosine gain >=.05, AND easy
NLL harm <=.10 AND easy accuracy loss <=5pp. Among eligible candidates rank
hard actual ΔNLL ascending, then cosine descending, select at most two.

| Candidate | Hard cosine gain vs O0 | Hard NLL gain vs O0 | Easy NLL harm | Easy accuracy loss pp | Eligible |
| --- | --- | --- | --- | --- | --- |
| O1 | .26207 | -.00749 | 2.86213 | 35.41667 | No |
| O2 | -.06757 | -.20475 | .22421 | 4.58333 | No |
| O3 | .23905 | -.73304 | 3.23744 | 37.29167 | No |

**Selection: NONE. Phase 2 not run.** No Phase-2 comparison or success claim exists.

## Mechanistic interpretation

O1/O3 show clearly improved local direction at frozen W0, including hard O1
with a smaller mean update norm than O0. Nevertheless finite-step task gain
is not guaranteed by local gradient cosine. O1 easy inner CE rises
2.25795 -> 4.51553; O3 easy 2.50297 -> 5.51338, hard 3.30774 -> 5.38075.
These observations and large updates are consistent with objective-scale/
curvature mismatch at eta=.05. No step sweep was performed to establish cause.

Centering sharpens hard assignments (entropy 1.36711 -> 1.20460, gap
.04567 -> .18753), but correctness falls 29.27083% -> 28.93750%.
Centered target correct-minus-wrong cosine is -.54976; original geometry
is -.01046. These coordinate-dependent margin magnitudes should not be
compared directly. Better confidence did not yield better assignment accuracy.
O2 also becomes more negatively aligned with the task.

Additional unit-fixture receipt (seed 7, CPU float64, dim 8, hidden 16,
outer loss mean output-square; NOT trained benchmark results):

| Objective | Vocabulary fast-state delta | Reset state delta | W0 outer-gradient norm |
| --- | --- | --- | --- |
| O1 | 1.200247 | 0 | .302821 |
| O2 | .058984 | 0 | .096853 |
| O3 | 1.446989 | 0 | .358810 |

All key/query outer-gradient norms are finite/nonzero; see unit_mechanism_receipt.json.
Finite-difference tests verify the differentiable W0 update, beyond nonzero gradients.

## Deviations, failures and recommendation

The research prompt leaves 'material' and 'catastrophic' unquantified. PLAN.md
operationalizes them numerically before results, with no subsequent alteration.
Centering epsilon 1e-6 implements the requested finite-degenerate handling.
No other hyperparameter, architecture or generator change; no hidden tuning,
label leakage into adaptation, outer training or detector integration.

Initial deployment 20260912-043206-tovd-t004-screen failed with SSH connection
closed (exit 255), before experiment launch; immediate retry succeeded. No
failed experiment was omitted. Complete experiment run exits 0.

Recommend Research Lead accept this screen as verified negative eligibility
under the fixed protocol and stop/reframe before any detector work. The
O1/O3 direction signal warrants a carefully specified reformulation if the
lead chooses to continue, potentially separating step behavior from teacher
correctness. That is a research decision; no repair, sweep or T005 is started.

## Durable evidence

- `research_log/t004/PLAN.md`: preregistration.
- `research_log/t004/RESULTS.md`: all aggregate/per-seed tables and interpretation.
- `research_log/t004/frozen_screen.json`: complete aggregate/per-seed statistics.
- `research_log/t004/selection.json`: frozen decision and thresholds.
- `research_log/t004/verification.json`: pairing, source hashes, artifact manifest.
- `research_log/t004/unit_mechanism_receipt.json`: labeled unit-fixture evidence.
- `research_log/remote_runs/20260912-043224-tovd-t004-screen-a6000/`: full raw
  2,400 episode / 19,200 query records, all token diagnostics, meta/run scripts/logs.
- Remote originals remain under the same run ID in /home/wenchang/asdasdsad/wjq/TOVD/runs.
- `research_log/T003_engineering_report.md`: archived prior engineering report.

Heartbeat tovd remains active every 15 minutes. Completed T004 is not rerun
while its ACTIVE inbox is unchanged; wait for explicit research-lead instructions.
