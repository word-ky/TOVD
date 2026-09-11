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
