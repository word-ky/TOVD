# T013-REPLAY1B — REPLAY_COMPLETED_EXIT0_AWAIT_COMPARATOR

The single frozen replay naturally finished at 2026-09-14T06:09:11+08:00 with integer exit0, 5058 seconds (84min18s) after its original04:44:53 launch. At the second permitted observation06:25:44, exactPID1104124 was absent (psRC1, no row), fixed tmux t013-close1-primary-replay was absent (RC1, no server), exit_code.txt existed with integer0 and finished.txt existed with a valid timestamp. All four clean-completion requirements hold. Stop immediately; comparator and scientific disclosure await a separate Lead task. This is execution completion only, not reproducibility PASS or scientific acceptance.

REPLAY1B had two observations06:08:51 and06:25:44, spacing1013s; clean completion occurred20s after the first point and was discovered at the ordinary next heartbeat. No third/fourth point, tighter cadence, new launch, restart/resume or clock reset. No transport interruption/retry or observed execution failure. Previous REPLAY1A accepted evidence/delivery and original bindings matched the new instruction. No launch/preflight rerun or observer modification.

Immutable freeze6fec32243985ccc808123d851abf5f3dea10af99, dispatch88668f76b22777459b5792dd28f88075f208c678, run20260912-210355-tovd-native30-primary, release20260912-210306-tovd-native30-primary-freeze remain unchanged. Full historical launch/cwd/interpreter/cache/analysis/FIN1 hashes and all current observation outputs/command are recorded below. Hashes are accepted launch evidence, not freshly rerun verification. Existing Python3.12.12 environment preserved; CPU frozen analysis unchanged.

Final top-level metadata only: stdout1999bytes,stderr0,results.json15857,paired_image_draws.npy8000128,bootstrap_samples.npz796547,diagnostics_per_image.npz93358. Files' existence/size and timing were not interpreted scientifically. No stdout/stderr/result/array contents opened or copied.

Changed local/Git files: research_log/t013/replay1b/observation2.json,execution_receipt.json; research_log/t013/REPLAY1B_TERMINAL_REPORT.md; coordination/CODEX_TO_CHATGPT.md; research_log/REMOTE.md,project_state.md,session_log.md. Previous observation1.json remains. Necessary metadata/report copies mirrored under remote project research_log and coordination. Sole remote observation command is the unchanged existing observe.py invocation below; only metadata reports saved locally. No changes to replay scratch, primary cache, frozen release, process, environment, priority, affinity, threads, thresholds, seeds or output paths.

No scientific/log contents interpreted, comparator/replay-envelope/DEC1/CF/MECH/YOLO/T014 or detector inference, second replay/restart/resume, cleanup/deletion/scan, result repair or criterion changes. Inner loss/gradient/reset diagnostics and new tests are not applicable to this operational terminal capture. Next heartbeat checks mailbox only until new Lead task. Raw operational evidence retained without repair.

## Exact execution receipt

```json
{
  "task": "T013-REPLAY1B",
  "status": "REPLAY_COMPLETED_EXIT0_AWAIT_COMPARATOR",
  "task_start_head": "209d252b417ca04e032e5c8c2cc2dcd1f38a7a5f",
  "lead_instruction": "13a221663bf21d5a474deb52cea79d2a12b9ada9",
  "prior_lead_instruction": "0a8a4a25ebea8840f0bf964902bce988dd51aa95",
  "launch_evidence": "688f36be6a845d8cf93531fb570268c9fbc2c1e9",
  "replay1a_evidence": "4a78db28fae8aed9f6a01f60b373fa44cad3b594",
  "replay1a_delivery": "bf2497e561900fb5aa4d30d7c481418bf45097a3",
  "original_launch": {
    "status": "LAUNCH_REQUESTED",
    "preflight": {
      "checks": {
        "analysis": {
          "path": "/home/wenchang/asdasdsad/wjq/TOVD/releases/20260912-210306-tovd-native30-primary-freeze/scripts/t013_analysis.py",
          "expected": "74cc73e71385e5d38e3fbe68ff03a0f11da30e67ff39b436da90422f72e99f9c",
          "actual": "74cc73e71385e5d38e3fbe68ff03a0f11da30e67ff39b436da90422f72e99f9c"
        },
        "fin1_receipt": {
          "path": "/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/fin1/primary_completion_receipt.json",
          "expected": "ade691d9765ee09b740ba7a7e24262ee55b272d82d5fd79889659fd6d67df63e",
          "actual": "ade691d9765ee09b740ba7a7e24262ee55b272d82d5fd79889659fd6d67df63e"
        }
      },
      "scratch_preexists": false,
      "tmux_rc": 1,
      "tmux_stderr": "no server running on /tmp/tmux-1012/default\n",
      "interpreter": "3.12.12 | packaged by conda-forge | (main, Jan 26 2026, 23:51:32) [GCC 14.3.0]",
      "cache": "/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-210355-tovd-native30-primary/artifacts/cache",
      "freeze": "6fec32243985ccc808123d851abf5f3dea10af99"
    },
    "started": "2026-09-14T04:44:53+08:00",
    "cwd": "/home/wenchang/asdasdsad/wjq/TOVD/releases/20260912-210306-tovd-native30-primary-freeze",
    "command": "/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python -m scripts.t013_analysis --annotations /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/coco/annotations/instances_val2017.json --run /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-210355-tovd-native30-primary/artifacts/cache --output /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay",
    "launch_command": [
      "tmux",
      "new-session",
      "-d",
      "-s",
      "t013-close1-primary-replay",
      "bash /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay/run.sh"
    ],
    "session": "t013-close1-primary-replay",
    "output": "/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay",
    "transport_retries": 0
  },
  "observations": [
    {
      "timestamp": "2026-09-14T06:08:51+08:00",
      "pid": 1104124,
      "tmux_rc": 0,
      "tmux_stderr": "",
      "ps_rc": 0,
      "process": "1104124 1104122 Rl+  /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python -m scripts.t013_analysis --annotations /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/coco/annotations/instances_val2017.json --run /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-210355-tovd-native30-primary/artifacts/cache --output /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay",
      "exit_exists": false,
      "exit_code": null,
      "finish_exists": false,
      "finished": null,
      "top_level": {
        "stdout.txt": {
          "exists": true,
          "bytes": 1910
        },
        "stderr.txt": {
          "exists": true,
          "bytes": 0
        },
        "results.json": {
          "exists": false,
          "bytes": null
        },
        "paired_image_draws.npy": {
          "exists": true,
          "bytes": 8000128
        },
        "bootstrap_samples.npz": {
          "exists": true,
          "bytes": 776609
        },
        "diagnostics_per_image.npz": {
          "exists": false,
          "bytes": null
        }
      }
    },
    {
      "timestamp": "2026-09-14T06:25:44+08:00",
      "pid": 1104124,
      "tmux_rc": 1,
      "tmux_stderr": "no server running on /tmp/tmux-1012/default\n",
      "ps_rc": 1,
      "process": "",
      "exit_exists": true,
      "exit_code": 0,
      "finish_exists": true,
      "finished": "2026-09-14T06:09:11+08:00",
      "top_level": {
        "stdout.txt": {
          "exists": true,
          "bytes": 1999
        },
        "stderr.txt": {
          "exists": true,
          "bytes": 0
        },
        "results.json": {
          "exists": true,
          "bytes": 15857
        },
        "paired_image_draws.npy": {
          "exists": true,
          "bytes": 8000128
        },
        "bootstrap_samples.npz": {
          "exists": true,
          "bytes": 796547
        },
        "diagnostics_per_image.npz": {
          "exists": true,
          "bytes": 93358
        }
      }
    }
  ],
  "observation_command": "/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python /home/wenchang/asdasdsad/wjq/TOVD/research_log/t013/replay1a/observe.py",
  "next": "STOP immediately. Existing heartbeat mailbox-only pending new Lead comparator task. No further REPLAY1B observations.",
  "transport_retries": 0,
  "replay_duration_seconds": 5058,
  "first_observation_commit": "d55b61e96b9ad49657135b66644645ff0b78785b",
  "scientific_or_log_contents_opened": false,
  "comparator_executed": false,
  "replay_relaunched": false
}
```
