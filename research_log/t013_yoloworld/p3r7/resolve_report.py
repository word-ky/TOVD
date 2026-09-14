"""Append current adjudication without changing the initial transport receipt."""
import json
import hashlib
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
rows = json.loads((OUT / 'command_ledger.json').read_text())
extra = json.loads((OUT / 'supplement_ledger.json').read_text())
by = {r['label']: r for r in rows + extra}
value = lambda label: by[label]['stdout'].strip()
state = 'YW_P3R7_STALE_LOADED_MODULE_REBOOT_CANDIDATE_RETURN_TO_LEAD'
pkg = '580.178.04-0ubuntu0.22.04.1'
matrix = [
    ['NVIDIA module', 'loaded', '/proc/driver/nvidia/version', '580.173.02', 'Loaded state, not on-disk package', 'boot2026-09-10 14:14:01; loaded_version', 'Old loaded version'],
    ['NVIDIA module', 'on-disk selected for running kernel', value('module_realpath'), value('module_version'), 'nvidia-dkms-580-server ' + pkg, 'mtime2026-09-12 06:21:13+08; modinfo; dkms_status', 'New coherent stack'],
]
for i, name in enumerate(['NVML amd64', 'NVML i386', 'libcuda amd64', 'libcuda i386']):
    matrix.append([name, 'user-space', value('library_realpath_' + str(i)), '580.178.04', pkg, 'library_package_' + str(i) + '; library_stat_' + str(i), 'New coherent stack; architecture-specific path'])
matrix.append(['nvidia-smi', 'user-space executable', value('smi_realpath'), 'NVML reports580.178, exit18', 'nvidia-utils-580-server ' + pkg, 'smi_package; installed_packages; ctime2026-09-12 06:20:14+08', 'New userspace cannot match old loaded module'])
assert value('module_version') == '580.178.04'
assert json.loads(value('pip_pre')) == json.loads(value('pip_post'))
assert value('checkpoint_hash').startswith('4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458')
r = {
    'task': 'T013-YW-P3R7', 'task_start_head': '75eda55092f10c2a6ad67c73db9e8742abbe5677',
    'lead_instruction_commit': '1f76d408300f17b6093aa147fafc11c317538c95',
    'user_authorized_resumption_head': '4ba66c7',
    'resumption_reason': 'User corrected premature SSH-blocker conclusion and explicitly directed continuation. Same existing configuration worked; no connection settings changed.',
    'started_at': rows[0]['started_at'], 'stopped_at': extra[-1]['stopped_at'], 'state': state,
    'supersedes': 'Initial P3R7 missing-evidence classification in f55ac957f2f05e1a7432de5f4b059cf6c604f005 and4ba66c7; original transport errors remain preserved as history.',
    'component_matrix': matrix,
    'classification_justification': 'Loaded580.173.02 is older than the selected on-disk module580.178.04 for kernel6.8.0-124-generic. Resolved NVML/libcuda (both architectures) and owning driver/compute/utils/DKMS packages are580.178.04. Boot2026-09-10 14:14:01 predates the recorded2026-09-12 06:20–06:22 package upgrade from580.173.02 to580.178.04; module mtime06:21:13 agrees. DKMS reports580.178.04 installed for running kernel. This meets the fixed stale-loaded-module rule, not installed split or recovered state. It is a reboot candidate only, not reboot authorization or guarantee.',
    'library_candidate_interpretation': 'Two linker-cache entries per library are amd64 and i386 of the same version, not competing versions for one architecture. LD_LIBRARY_PATH and LD_PRELOAD empty in snapshot.',
    'package_interpretation': 'nvidia-driver-570-server is explicitly a transitional package depending on nvidia-driver-580-server. Older rc entries are removed packages with configuration remnants. Container tooling and kernel ABI package version numbers are not NVIDIA driver version claims.',
    'nonzero_command_explanations': {'module_package': 'dpkg-query -S exit1: generated DKMS .ko is not directly owned as a packaged file; dkms status identifies installed build.', 'installed_packages': 'exit1 solely for unmatched *cuda-drivers* pattern; full other matches retained including status codes.', 'smi_list_SINGLE_ATTEMPT': 'exit18 Driver/library version mismatch', 'device_holders': 'fuser exit1 and empty stdout/stderr: no visible holder reported at current unprivileged access. Does not establish machine idle or reboot safe.'},
    'timeline_note': 'Initial tail across rotated logs selected old entries; narrow dated extraction and sorting fixed evidence selection without repeating device query. Both raw ledgers retained.',
    'boot_kernel': value('boot'), 'module_hash': value('module_hash'), 'module_vermagic': value('module_vermagic'),
    'proc_gpus': value('proc_gpu_information'), 'loaded_modules': value('loaded_modules'),
    'venv_pre': json.loads(value('pip_pre')), 'venv_post': json.loads(value('pip_post')), 'venv_equal': True,
    'python': value('python'), 'checkpoint_stat': value('checkpoint_stat'), 'checkpoint_sha256': value('checkpoint_hash'),
    'smi_exit_code': by['smi_list_SINGLE_ATTEMPT']['exit_code'], 'smi_stdout': value('smi_list_SINGLE_ATTEMPT'),
    'device_nodes': value('device_nodes'), 'device_holders': by['device_holders'],
    'command_ledgers': ['command_ledger.json', 'supplement_ledger.json', 'transport_ledger.json (prior preserved attempts)'],
    'execution_commands': ['/usr/bin/python3.10 /home/wenchang/asdasdsad/wjq/TOVD/research_log/t013_yoloworld/p3r7/snapshot.py', '/usr/bin/python3.10 /home/wenchang/asdasdsad/wjq/TOVD/research_log/t013_yoloworld/p3r7/supplement.py'],
    'execution_exit_codes': [0, 0],
    'counts': {'nvidia_smi_L_entire_P3R7': 1, 'reboots': 0, 'driver_module_reload_reset': 0, 'package_mutations': 0, 'linker_symlink_mutations': 0, 'fixed_Torch_installs': 0, 'CUDA_tensor_smokes': 0, 'checkpoint_deserializations': 0, 'model_constructions_loads': 0, 'detector_forwards': 0, 'T013_COCO_LVIS_science': 0, 'Grounding_reruns': 0, 'T014_CF_MECH_science': 0, 'YOLO_scientific_benchmark': 0},
    'preservation': 'P0/P1/P2/P3/P3R1–P3R6 evidence unchanged; environment unchanged; checkpoint305058902bytes and exact frozen SHA256; all YOLO settings frozen; GROUNDING_PRIMARY_NOT_SUPPORTED remains canonical.',
    'repair_recommendation': 'Research Lead review required',
    'next_action': 'Research Lead review of P3R7 host-driver consistency adjudication before any reboot, driver repair, Torch install, or model-runtime work',
}
(OUT / 'resolved_receipt.json').write_text(json.dumps(r, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
table = '| Component | Role | Resolved path | Reported version | Package version | Evidence | Judgment |\n|---|---|---|---|---|---|---|\n' + '\n'.join('| ' + ' | '.join(row) + ' |' for row in matrix)
report = '# T013-YW-P3R7 — Completed read-only adjudication after user correction\n\nFinal state: **' + state + '**.\n\n' + r['classification_justification'] + '\n\n' + table + '\n\n' + r['library_candidate_interpretation'] + '\n\n' + r['package_interpretation'] + '\n\nThe original SSH-blocker conclusion was premature. Resumed with user authorization using unchanged connection settings; both diagnostic drivers completed exit0. Initial transport-stop receipts remain immutable history and are superseded by this current classification. One nvidia-smi -L total across P3R7 returned18. No repair, reboot, package install, CUDA runtime or science occurred. fuser reported no visible holder, but this unprivileged result does not establish reboot safety.\n\nFull current commands, exits, stdout/stderr and timestamps: command_ledger.json and supplement_ledger.json. Package update timeline is in recent_update_timeline. Venv equality and frozen checkpoint hash passed.\n\nNext action: **' + r['next_action'] + '**.\n\n```json\n' + json.dumps(r, indent=2, ensure_ascii=False) + '\n```\n'
(OUT / 'P3R7_RESOLVED_REPORT.md').write_text(report, encoding='utf-8')
manifest = {p.name: {'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(OUT.iterdir()) if p.is_file() and p.name != 'resolved_manifest.json'}
(OUT / 'resolved_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
with (ROOT / 'coordination/CODEX_TO_CHATGPT.md').open('a', encoding='utf-8') as f:
    f.write('\n\n---\n\n' + report)
entry = '\n\n## ' + r['stopped_at'] + ' — P3R7 completed after user correction\nSame SSH configuration succeeded; earlier terminal transport stop was premature and is superseded. Full read-only snapshot+dated package follow-up completed. Loaded580.173.02, disk/DKMS/NVML/libcuda/utils580.178.04; bootSept10 predates Sept12 package update. State ' + state + '. nvidia-smi1 total exit18; repair/runtime/science0. fuser no visible holders is not proof idle. Venv unchanged, checkpoint exact. Current p3r7/resolved_receipt.json and P3R7_RESOLVED_REPORT.md supersede initial missing-evidence report; preserve old receipts. Next: ' + r['next_action'] + '.\n'
for path in ['research_log/REMOTE.md', 'research_log/session_log.md']:
    with (ROOT / path).open('a', encoding='utf-8') as f:
        f.write(entry)
print(json.dumps({k:v for k,v in manifest.items() if k in ['resolved_receipt.json', 'P3R7_RESOLVED_REPORT.md']}, indent=2))
