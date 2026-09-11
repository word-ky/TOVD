# CODEX -> CHATGPT: T005

## Status and recommendation

**VERIFIED — C2 passes Rules 2 and 3; C1 fails Rules 1 and 3.**
Research Lead acceptance is pending. Recommend a separately assigned controlled
meta-training task for C2. No meta-training, detector integration, new objective
or T006 has started.

C2 (O1 backtracking) improves hard NLL and accuracy from the same frozen W0 in
all three seeds. C1 (O0-budget matching) strongly repairs easy collapse relative
to C0 but worsens both hard NLL and accuracy, so the full scale-rescue rule fails.

## Revisions, source and environment

- Research assignment c7b4954; review 246994e accepts T004.
- Preregistration **7b8949e**, before aggregate outcomes.
- Tested runtime/analysis SHA **f2b9722ae8a1ad68e0e529488e68f88c170125de**.
- Dispatch milestone 2b22fc0. Final report/artifact SHA is the commit containing
  this report; runtime/analysis remain those tested at f2b9722.
- Release **20260912-053814-tovd-t005**.
- Run **20260912-053826-tovd-t005-a6000**, exit 0,
  finished 2026-09-12 05:42:14 +08:00.
- Remote project /home/wenchang/asdasdsad/wjq/TOVD, original project .venv.
- Physical A6000 **GPU 1** (CUDA_VISIBLE_DEVICES=1); GPU 0 runs another project.
  Python 3.12.12, torch 2.4.0+cu121, CUDA 12.1, pytest 9.1.1, float32;
  deterministic algorithms, CUBLAS_WORKSPACE_CONFIG=:4096:8, one CPU thread.
- Local Python 3.12.7, torch 2.13.0+cpu, pytest 9.1.1.
- Original T002 P checkpoints, trained at b88153a44836310219201404509cfd568c02614f,
  from run 20260912-023122-tovd-t002-a6000. Same 100 easy + 100 hard episodes
  per seed 7/17/27; 2,400 method/episode records total.
- T004 reference run 20260912-043224-tovd-t004-screen-a6000 supplies original
  O0 and O1 records. No checkpoint is retrained or changed.

Source SHA256, matched against retained local originals:
```text
7   125f800e8a0ae7ab7547afaab9f30bf493ec1378d3866f2f8192cbd5c7c8c6e2
17  5da689fbc0750d7fde51d31f93f02248fdb5a1ca3e5189b967ac46d0431a0985
27  091124ee7af0f8ec4ca95d12617d6c5954f8cb90dd73966823af0daed607e3ac
```

## Implementation and commands

Files: `tovd/models/fast_semantic_memory.py` adds a default-preserving
select_update hook; `tovd/models/step_control.py` contains the isolated
controllers; `tovd/synthetic/models.py` exposes their explicit names.
`tests/test_step_control.py` and `tests/test_step_screen.py` add focused tests.
`research_log/t005/oracle_step_screen.py` contains offline task-gradient scoring,
fixed interpretation rules, pairing and timing. `scripts/run_t005_a6000.sh`
runs full tests and the frozen screen. `research_log/t005/write_report.py`
formats completed receipts only. Project state/log/report files were updated.

C0=O1_fixed exactly preserves O1. C1=O1_norm_matched uses norm(g0)/(norm(g1)+1e-12),
with the requested nonfinite/near-zero guard; both gradient norms remain
in the meta-gradient graph outside the guard. C2=O1_backtracking selects the
first Armijo-valid step from [.05,.025,.0125,.00625,.003125], c=1e-4; otherwise
eta=0. Only O1 loss enters selection. Discrete C2 selection is nondifferentiated;
the accepted update uses the normal functional fast-parameter path.
No added parameters; all methods retain 2,128 parameters and identical W0.

Local:
```text
python -m pytest -q
python -m pytest tests/test_step_control.py tests/test_vocabulary_objectives.py -q
python -m pytest tests/test_step_screen.py -q
python -m research_log.t005.write_report
```
Workflow root D:/work/claude-autodl/autodl-workflow-clean, using this project's
ignored .autodl/config.json through AUTODL_CONFIG_PATH:
```text
./scripts/autodl-deploy.ps1 -Tag tovd-t005 -Source D:/work/fightccfa-agin/CVPR2027/TTT-OVD
./scripts/autodl-run.ps1 -Name tovd-t005-a6000 -Cmd 'export TOVD_SOURCE_REVISION=f2b9722ae8a1ad68e0e529488e68f88c170125de; bash scripts/run_t005_a6000.sh'
```
Remote script executes CPU/CUDA full suites, then:
```text
python -m research_log.t005.oracle_step_screen --source-root /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-023122-tovd-t002-a6000/artifacts/t002 --t004-root /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-043224-tovd-t004-screen-a6000/artifacts/t004_phase1 --output "$AUTODL_ARTIFACTS_DIR/t005" --device cuda --revision "$TOVD_SOURCE_REVISION"
```

## Tests and exact reproduction

- Baseline before edits: **53 passed in 11.70s**.
- Controller + existing objective tests: **28 passed in 10.57s**.
- Offline runner/interpretation/pairing: **6 passed in 14.56s**.
- Full local suite: **70 passed in 24.47s**.
- A6000 CPU: **70 passed in 4.62s**; CUDA: **70 passed in 10.50s**.
  Two existing protobuf/Python-3.14 deprecation warnings per remote suite.
- O0 and C0 each reproduce all 600 historical T004 NLL/accuracy/margin values
  with **zero error**, zero episode-seed mismatches.
- All 2,400 offline diagnostic outputs AND fast states exactly match normal
  runtime: max error 0. Nonfinite element count 0; all finite flags true.
- C1 norm/direction/guard and W0 finite-difference tests pass. C2 first Armijo
  acceptance and all-rejected fallback tests pass. Label-change diagnostics
  confirm step selection is unchanged while task scores change.
- Existing original model, checkpoint and evaluator tests remain green.

## Main task results

Mean over seed means; full sample SDs, pre/post margins, per-seed values and
pooled distributions are in `research_log/t005/RESULTS.md`, `aggregate.csv`
and `frozen_step_screen.json`. Negative ΔNLL is improvement from own W0.
Common W0: easy 77.58333% accuracy / .55592 NLL; hard 40.54167% / 1.31390.

| Method | Regime | Accuracy % | NLL | ΔNLL | Task cosine | Raw objective gradient norm | Actual update norm |
| --- | --- | --- | --- | --- | --- | --- | --- |
| O0 | easy | 74.87500 | .58611 | .03019 | .01111 | 3.58560 | .17928 |
| O0 | hard | 39.41667 | 1.30265 | -.01126 | -.01116 | 4.05984 | .20299 |
| C0 | easy | 39.45833 | 3.44824 | 2.89232 | .41064 | 14.05324 | .70266 |
| C0 | hard | 41.87500 | 1.31014 | -.00377 | .25091 | 3.68140 | .18407 |
| C1 | easy | 74.45833 | .69309 | .13717 | .41064 | 14.05324 | .17928 |
| C1 | hard | 39.33333 | 1.33918 | .02527 | .25091 | 3.68140 | .20299 |
| C2 | easy | 86.70833 | .34449 | -.21143 | .41064 | 14.05324 | .09649 |
| C2 | hard | 46.25000 | 1.23536 | -.07854 | .25091 | 3.68140 | .14723 |

Raw task cosine/dot for C0/C1/C2 use the same g1 by construction; realized
update direction is reported separately. C2 has no rejected steps in this run.

| Method | Regime | O1 inner loss before -> after | Episodes NLL improves % | Queries NLL improves % |
| --- | --- | --- | --- | --- |
| O0 | easy | 2.25795 -> 2.21680 | 39.33333 | 31.75000 |
| O0 | hard | 1.65942 -> 1.55895 | 43.00000 | 40.54167 |
| C0 | easy | 2.25795 -> 4.51553 | 18.33333 | 35.54167 |
| C0 | hard | 1.65942 -> 1.62074 | 52.66667 | 56.41667 |
| C1 | easy | 2.25795 -> 2.77622 | 46.33333 | 47.33333 |
| C1 | hard | 1.65942 -> 1.65492 | 50.66667 | 54.83333 |
| C2 | easy | 2.25795 -> 2.00317 | 63.33333 | 53.66667 |
| C2 | hard | 1.65942 -> 1.54000 | 55.66667 | 58.62500 |

For O0, this table evaluates O1 loss diagnostically; O0's own cosine loss is
separately labeled in JSON/RESULTS. Historical T003 exact-text oracle is only
a non-deployable reference, unchanged and not rerun: easy 85.16667%/.36045,
hard 48.33333%/1.18409. It is not a mathematical upper bound.

## Exact Rules 1-3

**Rule 1 / C1 scale rescue: FAIL.** Easy versus C0 improves by 2.75515 nats
and +35.0pp, satisfying both easy thresholds. However hard NLL rises
1.31014 -> 1.33918 AND accuracy falls 41.875% -> 39.33333%; the no-both-worsen
condition fails. Report partial easy rescue, not a pass of the declared rule.

**Rule 2 / C2 descent safe: PASS.** All 600 accepted updates satisfy Armijo,
zero violations, zero no-update fallbacks. Easy NLL is .24163 below O0 and
accuracy 11.83333pp above O0; hard NLL 1.23536 <= C0 1.31014.

**Rule 3 / task useful: C1 FAIL; C2 PASS.** C1 hard mean ΔNLL +.02527,
accuracy -1.20833pp, NLL improves only 1/3 seeds. C2 hard mean ΔNLL -.07854,
accuracy +5.70833pp, NLL improves 3/3 seeds; hard cosine gain versus O0 is
+.26207, exceeding the fixed +.05 target.

| Seed | C2 hard ΔNLL | C2 hard accuracy delta pp | Post accuracy % |
| --- | --- | --- | --- |
| 7 | -.080198 | +7.500 | 48.625 |
| 17 | -.084027 | +5.875 | 48.750 |
| 27 | -.071407 | +3.750 | 41.375 |

**Retained limitation:** C2 easy seed 27 worsens from its own W0 by +.13119
NLL and -8.25pp accuracy. Rule 2 uses aggregate means and passes unchanged;
there is no per-seed or per-query task-safety guarantee. Inner descent also
does not guarantee task descent on every episode (hard NLL improves 55.67%).

## C1 norm evidence and C2 selection/cost

C1 mean scale easy .29776, hard 1.33198. Pooled min/median/p95/max:
easy .121781/.272309/.561807/.939717;
hard .511429/1.17163/2.50407/12.2177. No near-zero/finite guard fired.
Maximum actual update-norm error versus original O0: easy 4.47034836e-8,
hard **5.96046448e-8**; well within preregistered float32 tolerance.

C2 eta pooled counts (300 episodes per regime):
- Easy: .05:2, .025:13, .0125:41, .00625:202, .003125:42, zero:0.
- Hard: .05:179, .025:116, .0125:5, smaller/zero:0.
Mean eta .00777 easy / .03971 hard; mean trials 3.89667 / 1.42000.
All 600 accepted steps satisfy the declared inequality; no rejected step.
Per-seed eta/trial distributions and Armijo margins are preserved in raw JSON.

Normal-forward timing (3 warmed/synchronized full passes per seed/regime):
C0 easy 10.3593 ms, hard 10.3437 ms; C1 17.8201/17.7871 ms;
C2 **12.8387/11.0412 ms**, mean C2/C0 ratios **1.2393x/1.0676x**.
Oracle diagnostics are excluded. These are measured prototype costs on GPU 1;
shared host activity and sequential timing order limit small speed comparisons.

## Reset, vocabulary and outer-gradient evidence

Existing paired-scene stream: 20 episodes x 3 seeds x 4 methods = 240 records.
All repeat/reset output AND state errors exactly 0. Maximum vocabulary-order
permutation output error 1.1920928955e-7. Every method/seed has nonzero mean
vocabulary-dependent state change. C2 easy/hard vocabulary deltas by seed:
.162199/.222931/.162850; unrelated-vocabulary deltas .078074/.100974/.087641.

C1 CPU float64 unit fixture (not trained performance): W0 outer-gradient norm
.06466494, key projection .000593679, query projection .004495774.
Directional finite difference for fast output.weight, epsilon 1e-5:
analytic -.0005458316851768, numeric -.0005458316850587,
absolute error **1.18049e-13**. Full receipt: outer_gradient_receipt.json.
C2 selector differentiation is not required by T005; no meta-training claim.

## Interpretation, deviations and next action

The result supports useful O1 direction combined with label-free episode step
control at frozen W0. Norm matching alone is insufficient. C2's adaptive loss
check yields a useful finite update under all declared aggregate hard criteria.
This is a controlled synthetic mechanism result, not detection performance,
validation of future meta-training, an optimal controller claim, or universal
per-episode improvement.

No rule, candidate eta, temperature, objective, generator or checkpoint changed
after results. The documented 1e-12 C1 guard and float tolerances were fixed
before results. GPU 1 was selected because GPU 0 was occupied; hardware class
and computational protocol are unchanged. No experiment/deployment failures.
No hidden tuning, label-dependent step selection, new training or detector work.

Recommend Research Lead consider **C2 only** for a subsequent, explicitly
assigned controlled meta-training task. Wait for review; do not infer T006.

## Durable artifacts

- research_log/t005/PLAN.md: preregistration and reuse/increment plan.
- research_log/t005/RESULTS.md and aggregate.csv: full results, seed tables and distributions.
- research_log/t005/frozen_step_screen.json and rules.json: complete outcomes and exact rule decisions.
- research_log/t005/verification.json: source hashes, historical equality and artifact manifest.
- research_log/t005/outer_gradient_receipt.json: labeled C1 unit fixture.
- research_log/remote_runs/20260912-053826-tovd-t005-a6000/: all 2,400 raw records,
  19,200 query changes, 240 mechanism episodes, timing/selection data, metadata/run script/log.
- Remote originals retained under /home/wenchang/asdasdsad/wjq/TOVD/runs/<run-id>.
- research_log/T004_engineering_report.md: archived prior mailbox.

Heartbeat tovd remains active. Already-verified T005 is not repeated while the
research inbox remains unchanged ACTIVE. All follow-up scope remains with lead.
