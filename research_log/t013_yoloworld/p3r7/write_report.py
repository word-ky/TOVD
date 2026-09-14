"""Persist the observed P3R7 SSH transport stop; no remote operations."""
import datetime
import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
ledger = [
    {'command': 'Invoke-AutodlSsh mkdir -p /home/wenchang/asdasdsad/wjq/TOVD/research_log/t013_yoloworld/p3r7', 'exit_code': 255, 'stdout': '', 'stderr': 'Connection closed by 202.101.162.22 port 8220', 'effect': 'SSH failed; no confirmation directory was created; subsequent upload/execution/fetch not reached'},
    {'command': "Invoke-AutodlSsh 'date -Is; hostname'", 'exit_code': 0, 'stdout': '2026-09-14T21:20:22+08:00\nwenchang-PR4904W1\n', 'stderr': ''},
    {'command': 'Invoke-AutodlSsh mkdir -p /home/wenchang/asdasdsad/wjq/TOVD/research_log/t013_yoloworld/p3r7', 'exit_code': 255, 'stdout': '', 'stderr': 'ssh: connect to host 202.101.162.22 port 8220: Connection timed out', 'effect': 'SSH failed; subsequent upload/execution/fetch not reached'},
]
(OUT / 'transport_ledger.json').write_text(json.dumps(ledger, indent=2) + '\n')
r = {
    'task': 'T013-YW-P3R7', 'task_start_head': '75eda55092f10c2a6ad67c73db9e8742abbe5677',
    'lead_instruction_commit': '1f76d408300f17b6093aa147fafc11c317538c95',
    'first_recorded_local_task_timestamp': '2026-09-14T21:20:06.9437588+08:00', 'stopped_at': now,
    'state': 'YW_P3R7_AMBIGUOUS_RETURN_TO_LEAD',
    'justification': 'Required current component evidence is missing because SSH failed during project-log-directory preparation twice (connection closed, then timeout), with one successful identity/time-only probe between them. No component snapshot was run. The fixed ambiguous classification explicitly applies when evidence is missing. No inference about current NVIDIA consistency, reboot, or Torch/CUDA feasibility can be made.',
    'command_ledger': ledger,
    'prepared_script': 'research_log/t013_yoloworld/p3r7/snapshot.py',
    'prepared_script_status': 'LOCAL_ONLY_NOT_UPLOADED_NOT_EXECUTED',
    'boot_kernel_snapshot': None, 'loaded_module_state': None, 'on_disk_module_state': None,
    'resolved_user_libraries': None, 'smi_path_package_result': None, 'package_timeline': None,
    'device_nodes_holders': None, 'venv_pre_post_equality': None, 'checkpoint_final_stat_sha256': None,
    'unavailable_reason': 'No diagnostic command reached server execution; current evidence unavailable due SSH transport, not a demonstrated read-permission denial.',
    'historical_context_only': 'P3R6 reported loaded580.173.02/NVML580.178/exit18, baseline venv unchanged, checkpoint exact. These are historical facts and are NOT re-reported as current P3R7 measurements.',
    'counts': {'ssh_invocations': 3, 'successful_identity_only_probe': 1, 'nvidia_smi_L_attempts': 0, 'reboots': 0, 'driver_module_reload_reset': 0, 'package_mutations': 0, 'linker_symlink_mutations': 0, 'fixed_Torch_installs': 0, 'CUDA_tensor_smokes': 0, 'checkpoint_deserializations': 0, 'model_constructions_loads': 0, 'detector_forwards': 0, 'T013_COCO_LVIS_science': 0, 'Grounding_reruns': 0, 'T014_CF_MECH_science': 0, 'YOLO_scientific_benchmark': 0},
    'remote_evidence_mirror': 'NOT_COMPLETED_SSH_TRANSPORT_UNRELIABLE; durable authoritative receipt retained locally and committed to GitHub.',
    'preservation': 'No project assets or host driver/package/linker state modified by this package. P0/P1/P2/P3/P3R1–P3R6 evidence preserved, all YOLO scientific settings frozen. Grounding remains GROUNDING_PRIMARY_NOT_SUPPORTED. No current byte-identity claim without a fresh hash.',
    'repair_recommendation': 'Research Lead review required',
    'next_action': 'Research Lead review of P3R7 host-driver consistency adjudication before any reboot, driver repair, Torch install, or model-runtime work',
}
(OUT / 'adjudication_receipt.json').write_text(json.dumps(r, indent=2) + '\n')
report = '''# T013-YW-P3R7 — Missing host evidence after SSH failures

State: **YW_P3R7_AMBIGUOUS_RETURN_TO_LEAD**.

The diagnostic script was prepared locally but never uploaded or executed. Two SSH attempts to create the project evidence directory failed with exit255: first connection closed, then connection timeout. Between them, one short read-only probe succeeded at2026-09-14T21:20:22+08:00 and confirmed hostname wenchang-PR4904W1. The failures occurred before upload, so no component inspection, nvidia-smi, package action, GPU operation or checkpoint read was performed.

The classification follows the fixed rule for missing evidence. We cannot distinguish a stale loaded module, installed component split or spontaneous recovery. P3R6 driver versions remain historical observations, not current measurements. This is a transport blocker, not evidence of Torch/CUDA or YOLO failure. Research Lead review required.

## Component matrix

| Component | Role | Resolved path | Reported version | Package version | Timestamp/evidence | Consistency judgment |
|---|---|---|---|---|---|---|
| NVIDIA module | Loaded | Unavailable | Unavailable | Unavailable | No P3R7 snapshot | Not adjudicated |
| NVIDIA module | On disk | Unavailable | Unavailable | Unavailable | No P3R7 snapshot | Not adjudicated |
| NVML | User space | Unavailable | Unavailable | Unavailable | No P3R7 snapshot | Not adjudicated |
| libcuda | User space | Unavailable | Unavailable | Unavailable | No P3R7 snapshot | Not adjudicated |
| nvidia-smi | User-space executable | Unavailable | Unavailable | Unavailable | Attempts0 | Not adjudicated |

Boot/kernel, update timeline, device holders, venv pre/post equality and final checkpoint hash are unavailable; no values fabricated. Prior evidence/settings and final checkpoint were not modified. Grounding remains GROUNDING_PRIMARY_NOT_SUPPORTED. No repair/runtime/scientific action occurred. Remote receipt mirroring could not complete; local project records and GitHub preserve the handoff.

Next action: **Research Lead review of P3R7 host-driver consistency adjudication before any reboot, driver repair, Torch install, or model-runtime work**.

## Machine receipt and executed command ledger

```json
''' + json.dumps(r, indent=2) + '\n```\n'
(OUT / 'P3R7_REPORT.md').write_text(report, encoding='utf-8')
manifest = {p.name: {'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(OUT.iterdir()) if p.is_file() and p.name != 'delivery_manifest.json'}
(OUT / 'delivery_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
with (ROOT / 'coordination/CODEX_TO_CHATGPT.md').open('a', encoding='utf-8') as f:
    f.write('\n\n---\n\n' + report)
entry = f'\n\n## {now} — P3R7 SSH transport stop\nResumed after user replenished quota. Lead1f76d408/task-start75eda550. Local read-only snapshot.py prepared but not uploaded/executed: first SSH project-dir preparation closed(exit255), identity-only probe succeeded21:20:22+08, second preparation timed out(exit255). State YW_P3R7_AMBIGUOUS_RETURN_TO_LEAD due missing current component evidence. nvidia-smi0, repair/runtime/science0; no new checkpoint/venv measurement. Prior evidence unchanged. Local p3r7 receipts authoritative; remote mirror unavailable. Await Lead review; do not repeat unchanged terminal task.\n'
for path in ['research_log/session_log.md', 'research_log/REMOTE.md']:
    with (ROOT / path).open('a', encoding='utf-8') as f:
        f.write(entry)
print(json.dumps(manifest, indent=2))
