"""Record observed preflight driver mismatch; executes no runtime operations."""
import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
def read(name):
    raw = (OUT / name).read_bytes()
    return raw.decode('utf-16' if raw.startswith((b'\xff\xfe', b'\xfe\xff')) else 'utf-8-sig')

base = '/home/wenchang/asdasdsad/wjq/TOVD/shared/t013_yoloworld'
receipt = {
    'task': 'T013-YW-P3R6',
    'task_start_head': '2a6d5d39fdd782b57108ea62c86a4fa0c4e701d5',
    'lead_instruction_commit': 'c2c516fcec094a54ebe0a62a67511d94425ad37b',
    'started_at': '2026-09-14T10:39:19.222Z',
    'stopped_at': '2026-09-14T18:41:17+08:00',
    'state': 'YW_P3R6_AMBIGUOUS_RETURN_TO_LEAD',
    'reason': 'Preflight nvidia-smi cannot initialize NVML: Driver/library version mismatch. NVML reports580.178 whereas the loaded kernel module reports580.173.02. GPU identity is unavailable from the required device snapshot. This is an unexpected host state; CUDA execution was not tested, so CUDA unavailability or Torch incompatibility is not asserted. Stop under the explicit unexpected-state rule before installing packages.',
    'venv_path': base + '/env',
    'python': '3.10.12',
    'preflight_pip_list': [{'name': 'pip', 'version': '22.0.2'}, {'name': 'setuptools', 'version': '59.6.0'}],
    'post_task_pip_list': [{'name': 'pip', 'version': '22.0.2'}, {'name': 'setuptools', 'version': '59.6.0'}],
    'post_task_pip_freeze': '',
    'venv_drift': False,
    'free_bytes': 160343076864,
    'nvcc_path': '/home/wenchang/anaconda3/envs/lqt_canconv_cu118/bin/nvcc',
    'nvcc_version': '11.8.89',
    'nvidia_smi_command': 'nvidia-smi -L',
    'nvidia_smi_exit_code': 18,
    'nvml_library_version_reported': '580.178',
    'loaded_kernel_module_version': '580.173.02',
    'driver_metadata_command': 'cat /proc/driver/nvidia/version',
    'checkpoint_path': base + '/weights/s_stage2-4466ab94.pth',
    'checkpoint_pre_bytes': 305058902,
    'checkpoint_post_bytes': 305058902,
    'checkpoint_pre_sha256': '4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458',
    'checkpoint_post_sha256': '4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458',
    'checkpoint_guard_commands': ['stat ' + base + '/weights/s_stage2-4466ab94.pth', 'sha256sum ' + base + '/weights/s_stage2-4466ab94.pth'],
    'fixed_install_command_NOT_EXECUTED': base + '/env/bin/python -m pip --cache-dir ' + base + '/cache install torch==2.1.2+cu118 torchvision==0.16.2+cu118 numpy==1.26.4 --extra-index-url https://download.pytorch.org/whl/cu118',
    'install_started_at': None,
    'install_stopped_at': None,
    'install_exit_code': None,
    'install_log_path': None,
    'cache_use': 'Not accessed; previous partial-download usefulness not evaluated because install did not start.',
    'required_version_checks': {'torch_2.1.2+cu118': 'NOT_RUN_NOT_INSTALLED', 'torchvision_0.16.2+cu118': 'NOT_RUN_NOT_INSTALLED', 'numpy_1.26.4': 'NOT_RUN_NOT_INSTALLED', 'torch.version.cuda_11.8': 'NOT_RUN'},
    'cuda_smoke': {'status': 'NOT_RUN_PREFLIGHT_HOST_MISMATCH', 'code_path': None, 'command': None, 'exit_code': None, 'cuda_available': None, 'device_count': None, 'device_1_name': None, 'tensor_device': None, 'integer_endpoints': None, 'FP32_finite': None, 'synchronization': None, 'peak_allocated_bytes': None},
    'counts': {'fixed_base_install_commands': 0, 'alternate_version_index_mirror_device_attempts': 0, 'MMCV_MMEngine_MMDet_transformers_timm_OpenCV_install_build': 0, 'source_patches': 0, 'checkpoint_deserializations': 0, 'model_constructions_loads': 0, 'synthetic_detector_forwards': 0, 'CUDA_tensor_smokes': 0, 'T013_COCO_LVIS_science': 0, 'Grounding_reruns': 0, 'T014_CF_MECH_science': 0, 'YOLO_scientific_benchmark': 0, 'driver_modifications_reboots': 0},
    'preflight_raw': read('preflight.txt'),
    'terminal_raw': read('terminal_snapshot.txt'),
    'preservation': 'Grounding remains GROUNDING_PRIMARY_NOT_SUPPORTED. P0/P1/P2/P3/P3R1–P3R5 evidence, environment, sources, caches and frozen YOLO scientific settings unchanged. This is host preflight evidence only, not a YOLO scientific negative or Torch compatibility result.',
    'next_action': 'Research Lead review of P3R6 base Torch/CUDA runtime evidence before any OpenMMLab/model-runtime work',
}
(OUT / 'runtime_receipt.json').write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
report = '''# T013-YW-P3R6 — Preflight host driver mismatch

Final state: **YW_P3R6_AMBIGUOUS_RETURN_TO_LEAD**.

The existing Python3.10.12 venv is unchanged: only pip22.0.2 and setuptools59.6.0, both before and after; pip freeze is empty. Free space160343076864 bytes. Fixed nvcc reports11.8.89. Before installation, `nvidia-smi -L` and the requested GPU query reported `Failed to initialize NVML: Driver/library version mismatch`. A read-only terminal snapshot captured exit18 and identified NVML580.178 versus loaded kernel module580.173.02 (`cat /proc/driver/nvidia/version`). The required GPU identity snapshot is unavailable. CUDA execution itself has not been tested; NVML failure is not presented as proof that CUDA cannot execute.

Stopped under P3R6's unexpected-state rule without installing packages or modifying drivers. Fixed pip command executions0, CUDA tensor smokes0. No install log or smoke code/output exists because neither stage started; corresponding values are null, not fabricated failures. Previous partial wheel cache usefulness was not evaluated. Checkpoint stat/hash before and after remain exactly305058902 bytes /4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458.

Task-start HEAD2a6d5d39fdd782b57108ea62c86a4fa0c4e701d5; Leadc2c516fcec094a54ebe0a62a67511d94425ad37b. Start2026-09-14T10:39:19.222Z; stop2026-09-14T18:41:17+08:00. No alternate package/index/device, OpenMMLab installation/build, source patch, checkpoint/model load, detector forward or scientific execution. Grounding remains GROUNDING_PRIMARY_NOT_SUPPORTED; prior evidence and frozen settings unchanged.

Next action: **Research Lead review of P3R6 base Torch/CUDA runtime evidence before any OpenMMLab/model-runtime work**.

Exact commands, raw snapshots, all counts, explicit unexecuted fields and checkpoint guards are preserved below and in runtime_receipt.json.

```json
''' + json.dumps(receipt, indent=2, ensure_ascii=False) + '\n```\n'
(OUT / 'P3R6_REPORT.md').write_text(report, encoding='utf-8')
manifest = {str(p.relative_to(ROOT)).replace('\\', '/'): {'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(OUT.iterdir()) if p.is_file() and p.name != 'delivery_manifest.json'}
(OUT / 'delivery_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
with (ROOT / 'coordination/CODEX_TO_CHATGPT.md').open('a', encoding='utf-8') as f:
    f.write('\n\n---\n\n' + report)
entry = '\n\n## 2026-09-14T18:41:17+08:00 — P3R6 unexpected host driver state\nLeadc2c516f/task-start2a6d5d3. Venv unchanged Python3.10.12/pip22.0.2/setuptools59.6.0. nvidia-smi exit18 Driver/library version mismatch: NVML580.178 vs kernel580.173.02. State YW_P3R6_AMBIGUOUS_RETURN_TO_LEAD under unexpected-state stop; CUDA compatibility untested. Fixed install0, CUDA smoke0, driver modification0, science0. Checkpoint before/after exact305058902bytes/SHA4466ab94...f458. Full receipts research_log/t013_yoloworld/p3r6. Do not repeat unchanged package or repair driver without new Lead scope. Next: Research Lead review of P3R6 base Torch/CUDA runtime evidence before any OpenMMLab/model-runtime work.\n'
for relative in ['research_log/session_log.md', 'research_log/REMOTE.md']:
    with (ROOT / relative).open('a', encoding='utf-8') as f:
        f.write(entry)
print(json.dumps({k: v for k, v in manifest.items() if k.endswith(('runtime_receipt.json', 'P3R6_REPORT.md'))}, indent=2))
