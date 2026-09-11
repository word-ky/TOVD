# TOVD remote execution and heartbeat recovery

- Local root: `D:/work/fightccfa-agin/CVPR2027/TTT-OVD`.
- GitHub source of truth: `word-ky/TOVD`, branch `main`.
- A6000 hostname verified: `wenchang-PR4904W1`; two NVIDIA RTX A6000
  cards, each idle with 15 MiB used at initial inspection.
- Existing writable directory: `/home/wenchang/asdasdsad/wjq`.
- TOVD remote base: `/home/wenchang/asdasdsad/wjq/TOVD`.
- Project environment: `<remote-base>/.venv`, using system site packages from
  `/home/wenchang/anaconda3/envs/python3.12-tk2-2.3/bin/python`.
  Base Python is 3.12.12, PyTorch 2.4.0+cu121; pytest is absent in the base
  interpreter and is installed only in the TOVD environment.
- Local control scripts: `D:/work/claude-autodl/autodl-workflow-clean/scripts`.
  Run from that workflow root with `AUTODL_CONFIG_PATH` pointing to
  `D:/work/fightccfa-agin/CVPR2027/TTT-OVD/.autodl/config.json`.
  The project-specific connection config is local-only, ignored by Git.
- Deploy: `scripts/autodl-deploy.ps1 -Tag tovd-t001 -Source <local-root>`.
- Run: `scripts/autodl-run.ps1 -Name tovd-t001-a6000 -Cmd
  'export TOVD_SOURCE_REVISION=<tested-commit>; bash scripts/run_a6000.sh'`.
- Inspect: `scripts/autodl-logs.ps1 -RunId <id> -Lines 80`.
- Fetch with `Copy-FromAutodl` in `scripts/Autodl.Common.ps1`, copying
  `<remote-base>/runs/<id>` into this project's `research_log/remote_runs`.
- Use explicit release/run IDs from this project's report, not the workflow's
  global last-run state shared by other projects. Mirror relevant receipt IDs
  here after deploy/run. Artifacts remain within this project locally/remotely.

Heartbeat `tovd` is ACTIVE, attached to this Codex task, every 15 minutes.
It reads project logs and the latest research mailbox, directly executes clear
active work, checks existing runs, writes the engineering report and pushes
commits. No new task is inferred from an unchanged ACTIVE T001 that has already
been VERIFIED. Research acceptance and T002 selection remain with the lead.
Unchanged/non-actionable checks stay quiet; meaningful progress, completion,
failure or required user input is reported. User authorized this on 2026-09-12.

Release: 20260912-011056-tovd-t001, implementation SHA a34403756ebe049098c8850f08a1621edec0d6ce.
Run: 20260912-011209-tovd-t001-a6000. Earlier preparation attempt 20260912-011126-tovd-t001-a6000 failed before execution due to SSH timeout; retain its metadata.

Run 20260912-011209-tovd-t001-a6000 completed with exit 0 at 2026-09-12 01:12:21 +08:00; CPU 10/10, CUDA 10/10, both demos passed. No active TOVD tmux session remains. Complete receipts fetched to research_log/remote_runs and retained on remote.

## T002 completed
Implementation b88153a44836310219201404509cfd568c02614f; release 20260912-023118-tovd-t002.
Run 20260912-023122-tovd-t002-a6000 exited 0 at 2026-09-12 02:39:18 +08:00. Full CPU 23/23 and CUDA 23/23 suites passed, 15 models trained/evaluated, independent checkpoint evaluation matched. No active job remains.
Run script: scripts/run_t002_a6000.sh. Full receipts/checkpoints under remote runs/<run-id>/artifacts/t002 and local research_log/remote_runs/<run-id>. Read project_state.md and the latest engineering report before acting on unchanged ACTIVE T002.

## T003 completed
Analysis SHA 6780de5ae44dcc89b9f1c45ea781f33dc16ffbaf; release 20260912-030919-tovd-t003.
Run 20260912-030923-tovd-t003-a6000 exited 0 at 2026-09-12 03:10:33 +08:00. CPU/CUDA suites 30/30 each; all 1200 fixed P/B2 checkpoint/episode diagnoses completed. No active TOVD run remains.
Source remains original T002 runs/20260912-023122-tovd-t002-a6000/artifacts/t002. New artifacts in runs/20260912-030923-tovd-t003-a6000/artifacts/t003; full local copy in research_log/remote_runs. Read project_state.md and latest report; wait for explicit next task.

## T004 completed
Runtime/screen SHA 9afe8df54c22d0a20b284d6b4b20aaab5b36ea9a; release 20260912-043213-tovd-t004-screen.
Run 20260912-043224-tovd-t004-screen-a6000 exited 0 at 2026-09-12 04:34:08 +08.
CPU/CUDA full suites 53 each. All 2400 diagnoses finite and paired with zero drift.
Phase-1 gate selected none; no Phase 2, no active job. Full local receipts under research_log/remote_runs.
Project state and T004 reports are the source of truth; do not rerun unchanged ACTIVE task.
Initial deployment 20260912-043206-tovd-t004-screen failed SSH exit 255 before job launch; retry succeeded.
