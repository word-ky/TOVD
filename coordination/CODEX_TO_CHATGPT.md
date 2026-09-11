# CODEX -> CHATGPT

## LATEST REPORT

**Task ID:** T001
**Run ID:** 20260912-011209-tovd-t001-a6000
**Status:** VERIFIED — engineering feasibility; research acceptance pending
**Tested implementation SHA:** a34403756ebe049098c8850f08a1621edec0d6ce
**Remote release:** 20260912-011056-tovd-t001

### Files changed
Implementation commit:
- `.gitignore`, `pyproject.toml`, `README.md`
- `tovd/__init__.py`, `tovd/models/__init__.py`, `tovd/models/fast_semantic_memory.py`
- `tests/test_fast_semantic_memory.py`
- `scripts/__init__.py`, `scripts/demo_fast_semantic_memory.py`, `scripts/run_a6000.sh`
- `coordination/CODEX_TO_CHATGPT.md`
- `research_log/REMOTE.md`, `research_log/session_log.md`, `research_log/demo_cpu_initial.json`

Final evidence/report commit additionally updates this report and recovery logs,
and adds `research_log/demo_cpu.json`, `research_log/project_state.md`, plus:
- `research_log/remote_runs/20260912-011209-tovd-t001-a6000/meta.json`
- `research_log/remote_runs/20260912-011209-tovd-t001-a6000/run.sh`
- `research_log/remote_runs/20260912-011209-tovd-t001-a6000/train.log`
- `research_log/remote_runs/20260912-011209-tovd-t001-a6000/artifacts/demo_cpu.json`
- `research_log/remote_runs/20260912-011209-tovd-t001-a6000/artifacts/demo_cuda.json`
- `research_log/remote_runs/20260912-011126-tovd-t001-a6000/meta.json` (failed preparation).
Only reports/receipts changed after the tested implementation commit.

### Implementation and design choices
Exact target `K=P_k(X); S=softmax(K T^T/tau)T`, with unnormalized K/T;
separate bias-free key/query projections; gated MLP with hidden size 2D;
cosine loss; one functional SGD step, eta=0.05 and tau=1.
Each image independently adapts all six MLP parameter tensors from W0.
Inner adaptation never mutates module parameters or accumulates parameter .grad.
Training keeps the full higher-order graph, including S's dependence on K.
Evaluation uses create_graph=False and supports torch.no_grad().
Static control is exactly F_W0(P_q(Q)), independent of X and T.
Snapshots/diagnostics are detached; output remains differentiable in training.
No detection labels, dataset downloads, detector integration or training runs.
No deviation from T001's allowed choices.

### Reproduction commands
Local project root:
```text
python -m pytest -q
python -m pip install --no-deps --no-build-isolation -e .
python -m scripts.demo_fast_semantic_memory --device cpu --output research_log/demo_cpu.json
```
Existing AutoDL workflow root, with AUTODL_CONFIG_PATH set to this project's
ignored `.autodl/config.json`:
```text
scripts/autodl-deploy.ps1 -Tag tovd-t001 -Source D:\work\fightccfa-agin\CVPR2027\TTT-OVD
scripts/autodl-run.ps1 -Name tovd-t001-a6000 -Cmd 'export TOVD_SOURCE_REVISION=a34403756ebe049098c8850f08a1621edec0d6ce; bash scripts/run_a6000.sh'
scripts/autodl-logs.ps1 -RunId 20260912-011209-tovd-t001-a6000 -Lines 100
```
Run script pins GPU 0, CUBLAS_WORKSPACE_CONFIG=:4096:8 and one CPU thread,
then executes CPU tests, TOVD_TEST_DEVICE=cuda tests and both demos. Full command,
release and shell invocation are saved in the run receipt. Fetch used the
workflow's Copy-FromAutodl helper. See research_log/REMOTE.md for recovery.

### Environment and exact tests
- Windows: Python 3.12.7, torch 2.13.0+cpu, pytest 9.1.1.
- Local initial suite: **10 passed in 13.89s**; final suite: **10 passed in 14.01s**.
- Editable installation succeeded: tovd 0.1.0.
- A6000: Python 3.12.12, torch 2.4.0+cu121, CUDA 12.1, pytest 9.1.1.
- Remote CPU: **10 passed in 1.53s**.
- Remote CUDA: **10 passed in 2.13s**.
- CPU/CUDA demos: exit 0; completed 2026-09-12 01:12:21 +08:00.
- git diff --check passed before final reporting.

Seed=7, float64, B=2/N=6/C=5/M=3/D=8/hidden=16. Synthetic Gaussian
inputs; dataset split not applicable; no checkpoint, seeded random initialization.

### TTT diagnostics (A6000 CUDA)
| Metric | Value |
| --- | --- |
| Inner loss before | [0.637258424415897, 0.8606449007262176] |
| Inner loss after | [0.5119405163817825, 0.7631186941918832] |
| Inner gradient norm | [1.6319451944492038, 1.429767755438099] |
| Fast update norm | [0.08159725972246021, 0.07148838777190496] |
| Vocabulary target delta, T versus -T | 8.998322894164236 |
| Vocabulary fast-state delta | 0.196187243579249 |
| Vocabulary output delta | 0.34712771402343895 |
| Reset fast-state / output deltas | 0 / 0 |
| Adapted versus static output delta | 0.18615850927327499 |
| Outer gradient norm, key projection | 0.003474182474653634 |
| Outer gradient norm, query projection | 0.012572702045285794 |
| Outer gradient norm, W0 output weight | 0.021284463077324747 |
| Outer gradient norm, W0 output bias | 0.10247302488897167 |
| All-finite diagnostics | [true, true] |

All six W0 tensors have finite nonzero outer gradients (full values in JSON).
Directional finite differences through the complete adaptation match autograd
for W0 output weight and P_k at rtol=1e-4, atol=1e-8 on CPU and CUDA; this
checks the inner gradient path rather than just a nonzero direct W0 gradient.
Automated tests also verify exact S, shapes, local loss decrease, update size,
episodic reset after a different episode, parameter non-mutation, per-image batch
independence, label-free API, exact static control and no_grad inference.
Vocabulary reordering preserves state, as expected for an unordered vocabulary.

### Failures / limitations
- A6000 base interpreter had no pytest. Created a TOVD-only system-site-packages
  venv and installed pytest 9.1.1 there; other environments unchanged.
- Attempt 20260912-011126-tovd-t001-a6000 timed out during SSH preparation.
  Inspection found only metadata and no run.sh, train.log or tmux session.
  No experiment ran in that attempt. Retried successfully; both receipts retained.
- The initial local JSON is explicitly labeled working-tree-T001; final local
  and remote JSON receipts cite the actual tested commit.
- Vocabulary sensitivity is shown for this nondegenerate synthetic case. It is
  not a guarantee for every T1 != T2: a row permutation correctly leaves S/state
  unchanged. Real semantic usefulness, nonlinear advantage, detector accuracy,
  and benefit from meta-learning W0 remain untested. Float32/mixed precision
  and torch.inference_mode() are not validated by T001.

### Recommended next action
Research Lead: review T001 for acceptance and choose T002. Current evidence
supports mechanism implementation and differentiation; it does not establish
H2/H4, novelty, or accuracy gains. A stronger controlled semantic experiment is
a reasonable next option, with detector integration remaining your decision.
Codex has not changed the research inbox or marked ACCEPTED.

### Execution readiness
Remote project: `/home/wenchang/asdasdsad/wjq/TOVD`, A6000 connection verified.
Heartbeat `tovd`: ACTIVE, every 15 minutes, attached to the current Codex task.
It executes new explicit active tasks and reports results. Unchanged VERIFIED
T001 will not be rerun just because the inbox still says ACTIVE. No TOVD job
remains active after this run. All durable receipts are project-local and remote.

## RUN HISTORY
- Local seed-7 mechanism suite and demo passed; implementation a344037 published.
- First remote run preparation failed from SSH timeout before experiment launch.
- Retry 20260912-011209-tovd-t001-a6000: 10 CPU + 10 CUDA tests passed; both demos
  completed; exit 0. Engineering status VERIFIED; research review pending.
