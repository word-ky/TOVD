# T013-REPLAY1C — REPLAY_PASS_READY_FOR_RESEARCH_LEAD

The accepted comparator executed exactly once, exit0, and all four artifacts passed exact decoded parity. The unchanged CLOSE1 evaluator returned REPLAY_PASS_READY_FOR_RESEARCH_LEAD, reason same_completed_run_fin1_and_frozen_replay_comparison_pass. Scientific acceptance remains false. No scientific values were disclosed or interpreted; stop for a later Lead review.

Preflight matched expected/actual remote comparator SHA6270a32096c536deac8ec878d3cfbfeb1cc067d428781ab7beb09e78cb8acb76, FIN1 receipt SHAade691d9765ee09b740ba7a7e24262ee55b272d82d5fd79889659fd6d67df63e, cache run-receipt75518df05b4a4c15a4c20d32a7764073d21c57c9e8b9880b4d737259c1b35366 andmanifest88a31a45712f814d940ef894d0213108f9dca63c845abca01f7133ba44162adc. Exact left/right directories existed and comparison_receipt.json did not preexist. Historical REPLAY1B clean-completion evidence and FIN1 run/release/freeze/cache bindings match; no execution rerun. Local accepted comparator/CLOSE1 normalized source hashes matched; CLOSE1 SHAa227933e266090e1adab5395409ddf8ab037beb43c27f92b96713586d03d6c14. No source changes.

Comparator started and finished2026-09-14T07:16:22+08:00 using existing Python3.12.12. Exit0; stderr empty; stdout contains only accepted comparator structural parity report. No failure/retry. Exact generated receipt SHAa22ac31a351080b8860838beda92eb318c2a7ddfb422e2a8be29082388110eef matches remote SHA and byte-for-byte fetched copy. Receipt never normalized/edited after hashing.

All four artifacts present/nonempty and equal=true. JSON field equality, array keys/shapes/dtypes/NaN-mask equality are preserved verbatim below; no actual scientific values. Only this accepted comparator internally decoded scientific files. Codex accessed its structural parity receipt, not the underlying analysis/results/logs. Local Python3.12.7 called unchanged finalization_barrier.evaluate(binding,completion,fin1,replay) using accepted CLOSE3/FIN1 evidence plus actual receipt SHA/ref, exact left/right, analysis/comparator exit0, frozen analysisSHA74cc73e71385e5d38e3fbe68ff03a0f11da30e67ff39b436da90422f72e99f9c, replicates1000. Full envelope and returned booleans persisted in replay1c/replay_envelope_and_barrier.json. Research review/content access booleans now true for a later Lead task; scientific_acceptance false, restart_resume false, helper_opened_result_content false. No DEC1 action this cycle.

Local/Git files: research_log/t013/replay1c/{preflight.py,preflight.json,command.sh,execution_output.txt,comparison_receipt.json,comparator_started.txt,comparator_finished.txt,comparator_exit_code.txt,comparator_stdout.txt,comparator_stderr.txt,replay_envelope_and_barrier.json,execution_receipt.json}, this report, engineering mailbox and root REMOTE/project_state/session logs. Remote preflight helper at research_log/t013/replay1c_preflight.py; comparator generated comparison_receipt.json and five comparator_* files in shared/t013/close1-primary-replay. Necessary copies mirrored under remote project research_log/t013/replay1c. No scientific arrays/results copied. Exact wrapper/scientific command and all bindings are in execution receipt below.

No DEC1/scientific disclosure, CF/MECH, YOLO-World, T014, detector inference, second replay/comparator, restart/resume, output repair, cleanup or frozen-code/cache/environment/criterion mutation. No unchanged tests rerun: evidence is the one real accepted comparison and finalization evaluation. No scientific conclusion follows from parity. Stop and await Lead review.

## Execution metadata

```json
{
  "task": "T013-REPLAY1C",
  "status": "REPLAY_PASS_READY_FOR_RESEARCH_LEAD",
  "task_start_head": "fa6973856b7e9a90e8309f2bc54c609b15d65525",
  "lead_instruction": "1ae41f3b795d50345ed2b35af808998d1aa2e82b",
  "replay1b_evidence": "eb90ff9494eb34231668cf00d83d3ac3d9bd74da",
  "replay1b_delivery": "b49a73136342c9657ad21f2f1f6c9e98df44febe",
  "comparator_executions": 1,
  "transport_retries": 0,
  "preflight": {
    "checks": {
      "comparator": {
        "path": "/home/wenchang/asdasdsad/wjq/TOVD/research_log/t013/analysis_replay_compare.py",
        "expected": "6270a32096c536deac8ec878d3cfbfeb1cc067d428781ab7beb09e78cb8acb76",
        "actual": "6270a32096c536deac8ec878d3cfbfeb1cc067d428781ab7beb09e78cb8acb76",
        "match": true
      },
      "fin1": {
        "path": "/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/fin1/primary_completion_receipt.json",
        "expected": "ade691d9765ee09b740ba7a7e24262ee55b272d82d5fd79889659fd6d67df63e",
        "actual": "ade691d9765ee09b740ba7a7e24262ee55b272d82d5fd79889659fd6d67df63e",
        "match": true
      },
      "run_receipt": {
        "path": "/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-210355-tovd-native30-primary/artifacts/cache/run_receipt.json",
        "expected": "75518df05b4a4c15a4c20d32a7764073d21c57c9e8b9880b4d737259c1b35366",
        "actual": "75518df05b4a4c15a4c20d32a7764073d21c57c9e8b9880b4d737259c1b35366",
        "match": true
      },
      "manifest": {
        "path": "/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-210355-tovd-native30-primary/artifacts/cache/cache_manifest.jsonl",
        "expected": "88a31a45712f814d940ef894d0213108f9dca63c845abca01f7133ba44162adc",
        "actual": "88a31a45712f814d940ef894d0213108f9dca63c845abca01f7133ba44162adc",
        "match": true
      }
    },
    "left": "/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-210355-tovd-native30-primary/artifacts/analysis",
    "right": "/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay",
    "left_exists": true,
    "right_exists": true,
    "comparison_preexists": false,
    "interpreter": "3.12.12 | packaged by conda-forge | (main, Jan 26 2026, 23:51:32) [GCC 14.3.0]",
    "status": "PASS"
  },
  "command": "date -Iseconds > /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay/comparator_started.txt\n/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python /home/wenchang/asdasdsad/wjq/TOVD/research_log/t013/analysis_replay_compare.py /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-210355-tovd-native30-primary/artifacts/analysis /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay --output /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay/comparison_receipt.json > /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay/comparator_stdout.txt 2> /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay/comparator_stderr.txt\ncomparison_exit=$?\nprintf '%s\\n' \"$comparison_exit\" > /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay/comparator_exit_code.txt\ndate -Iseconds > /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay/comparator_finished.txt\ncat /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay/comparator_exit_code.txt\nsha256sum /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay/comparison_receipt.json\n",
  "started": "2026-09-14T07:16:22+08:00",
  "finished": "2026-09-14T07:16:22+08:00",
  "exit_code": 0,
  "stderr_bytes": 0,
  "receipt_ref": "/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay/comparison_receipt.json",
  "receipt_sha256": "a22ac31a351080b8860838beda92eb318c2a7ddfb422e2a8be29082388110eef",
  "barrier": {
    "state": "REPLAY_PASS_READY_FOR_RESEARCH_LEAD",
    "reason": "same_completed_run_fin1_and_frozen_replay_comparison_pass",
    "run_id": "20260912-210355-tovd-native30-primary",
    "scope": "primary",
    "research_lead_review_authorized": true,
    "primary_result_content_access_authorized": true,
    "fin1_execution_authorized": false,
    "replay_comparison_execution_authorized": false,
    "scientific_acceptance": false,
    "restart_resume_authorized": false,
    "helper_opened_result_content": false
  },
  "envelope_ref": "research_log/t013/replay1c/replay_envelope_and_barrier.json",
  "scientific_disclosure": false,
  "next": "STOP; await Research Lead scientific review/DEC1 task. No further comparator/replay or scientific interpretation."
}
```

## Unchanged structural comparison receipt

```json
{
  "status": "PASS",
  "artifacts": {
    "results.json": {
      "present_nonempty": true,
      "equal": true,
      "left_bytes": 15857,
      "right_bytes": 15857,
      "top_level_keys_equal": true,
      "fields": {
        "kind": true,
        "image_count": true,
        "conditions": true,
        "vocabularies": true,
        "metric_order": true,
        "point_metrics": true,
        "metric_ci95": true,
        "replicates": true,
        "seed": true,
        "margin_common_localized_gt_counts": true,
        "assessment": true
      }
    },
    "paired_image_draws.npy": {
      "present_nonempty": true,
      "equal": true,
      "left_bytes": 8000128,
      "right_bytes": 8000128,
      "left_shape": [
        1000,
        1000
      ],
      "right_shape": [
        1000,
        1000
      ],
      "left_dtype": "int64",
      "right_dtype": "int64",
      "nan_masks_equal": true
    },
    "bootstrap_samples.npz": {
      "present_nonempty": true,
      "equal": true,
      "left_bytes": 796547,
      "right_bytes": 796547,
      "keys_equal": true,
      "arrays": {
        "margins": {
          "equal": true,
          "left_shape": [
            1000,
            4
          ],
          "right_shape": [
            1000,
            4
          ],
          "left_dtype": "float64",
          "right_dtype": "float64",
          "nan_masks_equal": true
        },
        "metrics": {
          "equal": true,
          "left_shape": [
            1000,
            5,
            3,
            8
          ],
          "right_shape": [
            1000,
            5,
            3,
            8
          ],
          "left_dtype": "float64",
          "right_dtype": "float64",
          "nan_masks_equal": true
        }
      }
    },
    "diagnostics_per_image.npz": {
      "present_nonempty": true,
      "equal": true,
      "left_bytes": 93358,
      "right_bytes": 93358,
      "keys_equal": true,
      "arrays": {
        "c0_v0": {
          "equal": true,
          "left_shape": [
            1000,
            5
          ],
          "right_shape": [
            1000,
            5
          ],
          "left_dtype": "float64",
          "right_dtype": "float64",
          "nan_masks_equal": true
        },
        "c0_v1": {
          "equal": true,
          "left_shape": [
            1000,
            5
          ],
          "right_shape": [
            1000,
            5
          ],
          "left_dtype": "float64",
          "right_dtype": "float64",
          "nan_masks_equal": true
        },
        "c0_v2": {
          "equal": true,
          "left_shape": [
            1000,
            5
          ],
          "right_shape": [
            1000,
            5
          ],
          "left_dtype": "float64",
          "right_dtype": "float64",
          "nan_masks_equal": true
        },
        "c1_v0": {
          "equal": true,
          "left_shape": [
            1000,
            5
          ],
          "right_shape": [
            1000,
            5
          ],
          "left_dtype": "float64",
          "right_dtype": "float64",
          "nan_masks_equal": true
        },
        "c1_v1": {
          "equal": true,
          "left_shape": [
            1000,
            5
          ],
          "right_shape": [
            1000,
            5
          ],
          "left_dtype": "float64",
          "right_dtype": "float64",
          "nan_masks_equal": true
        },
        "c1_v2": {
          "equal": true,
          "left_shape": [
            1000,
            5
          ],
          "right_shape": [
            1000,
            5
          ],
          "left_dtype": "float64",
          "right_dtype": "float64",
          "nan_masks_equal": true
        },
        "c2_v0": {
          "equal": true,
          "left_shape": [
            1000,
            5
          ],
          "right_shape": [
            1000,
            5
          ],
          "left_dtype": "float64",
          "right_dtype": "float64",
          "nan_masks_equal": true
        },
        "c2_v1": {
          "equal": true,
          "left_shape": [
            1000,
            5
          ],
          "right_shape": [
            1000,
            5
          ],
          "left_dtype": "float64",
          "right_dtype": "float64",
          "nan_masks_equal": true
        },
        "c2_v2": {
          "equal": true,
          "left_shape": [
            1000,
            5
          ],
          "right_shape": [
            1000,
            5
          ],
          "left_dtype": "float64",
          "right_dtype": "float64",
          "nan_masks_equal": true
        },
        "c3_v0": {
          "equal": true,
          "left_shape": [
            1000,
            5
          ],
          "right_shape": [
            1000,
            5
          ],
          "left_dtype": "float64",
          "right_dtype": "float64",
          "nan_masks_equal": true
        },
        "c3_v1": {
          "equal": true,
          "left_shape": [
            1000,
            5
          ],
          "right_shape": [
            1000,
            5
          ],
          "left_dtype": "float64",
          "right_dtype": "float64",
          "nan_masks_equal": true
        },
        "c3_v2": {
          "equal": true,
          "left_shape": [
            1000,
            5
          ],
          "right_shape": [
            1000,
            5
          ],
          "left_dtype": "float64",
          "right_dtype": "float64",
          "nan_masks_equal": true
        },
        "c4_v0": {
          "equal": true,
          "left_shape": [
            1000,
            5
          ],
          "right_shape": [
            1000,
            5
          ],
          "left_dtype": "float64",
          "right_dtype": "float64",
          "nan_masks_equal": true
        },
        "c4_v1": {
          "equal": true,
          "left_shape": [
            1000,
            5
          ],
          "right_shape": [
            1000,
            5
          ],
          "left_dtype": "float64",
          "right_dtype": "float64",
          "nan_masks_equal": true
        },
        "c4_v2": {
          "equal": true,
          "left_shape": [
            1000,
            5
          ],
          "right_shape": [
            1000,
            5
          ],
          "left_dtype": "float64",
          "right_dtype": "float64",
          "nan_masks_equal": true
        },
        "margin_contrast_sum_count": {
          "equal": true,
          "left_shape": [
            4,
            1000,
            2
          ],
          "right_shape": [
            4,
            1000,
            2
          ],
          "left_dtype": "float64",
          "right_dtype": "float64",
          "nan_masks_equal": true
        }
      }
    }
  },
  "comparison": "exact decoded JSON/arrays with equal NaNs; no compressed-byte equality requirement"
}
```

Final REPLAY1C evidence commit: 60c99b1051382bed8df6101389905277bb07d80f. Delivery is the subsequent `coord: deliver exact parity readiness to research lead` commit containing this entry. Await Lead scientific review; no DEC1 execution.
