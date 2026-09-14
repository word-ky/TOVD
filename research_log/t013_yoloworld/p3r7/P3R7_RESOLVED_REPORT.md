# T013-YW-P3R7 — Completed read-only adjudication after user correction

Final state: **YW_P3R7_STALE_LOADED_MODULE_REBOOT_CANDIDATE_RETURN_TO_LEAD**.

Loaded580.173.02 is older than the selected on-disk module580.178.04 for kernel6.8.0-124-generic. Resolved NVML/libcuda (both architectures) and owning driver/compute/utils/DKMS packages are580.178.04. Boot2026-09-10 14:14:01 predates the recorded2026-09-12 06:20–06:22 package upgrade from580.173.02 to580.178.04; module mtime06:21:13 agrees. DKMS reports580.178.04 installed for running kernel. This meets the fixed stale-loaded-module rule, not installed split or recovered state. It is a reboot candidate only, not reboot authorization or guarantee.

| Component | Role | Resolved path | Reported version | Package version | Evidence | Judgment |
|---|---|---|---|---|---|---|
| NVIDIA module | loaded | /proc/driver/nvidia/version | 580.173.02 | Loaded state, not on-disk package | boot2026-09-10 14:14:01; loaded_version | Old loaded version |
| NVIDIA module | on-disk selected for running kernel | /usr/lib/modules/6.8.0-124-generic/updates/dkms/nvidia.ko | 580.178.04 | nvidia-dkms-580-server 580.178.04-0ubuntu0.22.04.1 | mtime2026-09-12 06:21:13+08; modinfo; dkms_status | New coherent stack |
| NVML amd64 | user-space | /usr/lib/x86_64-linux-gnu/libnvidia-ml.so.580.178.04 | 580.178.04 | 580.178.04-0ubuntu0.22.04.1 | library_package_0; library_stat_0 | New coherent stack; architecture-specific path |
| NVML i386 | user-space | /usr/lib/i386-linux-gnu/libnvidia-ml.so.580.178.04 | 580.178.04 | 580.178.04-0ubuntu0.22.04.1 | library_package_1; library_stat_1 | New coherent stack; architecture-specific path |
| libcuda amd64 | user-space | /usr/lib/x86_64-linux-gnu/libcuda.so.580.178.04 | 580.178.04 | 580.178.04-0ubuntu0.22.04.1 | library_package_2; library_stat_2 | New coherent stack; architecture-specific path |
| libcuda i386 | user-space | /usr/lib/i386-linux-gnu/libcuda.so.580.178.04 | 580.178.04 | 580.178.04-0ubuntu0.22.04.1 | library_package_3; library_stat_3 | New coherent stack; architecture-specific path |
| nvidia-smi | user-space executable | /usr/bin/nvidia-smi | NVML reports580.178, exit18 | nvidia-utils-580-server 580.178.04-0ubuntu0.22.04.1 | smi_package; installed_packages; ctime2026-09-12 06:20:14+08 | New userspace cannot match old loaded module |

Two linker-cache entries per library are amd64 and i386 of the same version, not competing versions for one architecture. LD_LIBRARY_PATH and LD_PRELOAD empty in snapshot.

nvidia-driver-570-server is explicitly a transitional package depending on nvidia-driver-580-server. Older rc entries are removed packages with configuration remnants. Container tooling and kernel ABI package version numbers are not NVIDIA driver version claims.

The original SSH-blocker conclusion was premature. Resumed with user authorization using unchanged connection settings; both diagnostic drivers completed exit0. Initial transport-stop receipts remain immutable history and are superseded by this current classification. One nvidia-smi -L total across P3R7 returned18. No repair, reboot, package install, CUDA runtime or science occurred. fuser reported no visible holder, but this unprivileged result does not establish reboot safety.

Full current commands, exits, stdout/stderr and timestamps: command_ledger.json and supplement_ledger.json. Package update timeline is in recent_update_timeline. Venv equality and frozen checkpoint hash passed.

Next action: **Research Lead review of P3R7 host-driver consistency adjudication before any reboot, driver repair, Torch install, or model-runtime work**.

```json
{
  "task": "T013-YW-P3R7",
  "task_start_head": "75eda55092f10c2a6ad67c73db9e8742abbe5677",
  "lead_instruction_commit": "1f76d408300f17b6093aa147fafc11c317538c95",
  "user_authorized_resumption_head": "4ba66c7",
  "resumption_reason": "User corrected premature SSH-blocker conclusion and explicitly directed continuation. Same existing configuration worked; no connection settings changed.",
  "started_at": "2026-09-14T13:30:24.029138+00:00",
  "stopped_at": "2026-09-14T13:31:32.315114+00:00",
  "state": "YW_P3R7_STALE_LOADED_MODULE_REBOOT_CANDIDATE_RETURN_TO_LEAD",
  "supersedes": "Initial P3R7 missing-evidence classification in f55ac957f2f05e1a7432de5f4b059cf6c604f005 and4ba66c7; original transport errors remain preserved as history.",
  "component_matrix": [
    [
      "NVIDIA module",
      "loaded",
      "/proc/driver/nvidia/version",
      "580.173.02",
      "Loaded state, not on-disk package",
      "boot2026-09-10 14:14:01; loaded_version",
      "Old loaded version"
    ],
    [
      "NVIDIA module",
      "on-disk selected for running kernel",
      "/usr/lib/modules/6.8.0-124-generic/updates/dkms/nvidia.ko",
      "580.178.04",
      "nvidia-dkms-580-server 580.178.04-0ubuntu0.22.04.1",
      "mtime2026-09-12 06:21:13+08; modinfo; dkms_status",
      "New coherent stack"
    ],
    [
      "NVML amd64",
      "user-space",
      "/usr/lib/x86_64-linux-gnu/libnvidia-ml.so.580.178.04",
      "580.178.04",
      "580.178.04-0ubuntu0.22.04.1",
      "library_package_0; library_stat_0",
      "New coherent stack; architecture-specific path"
    ],
    [
      "NVML i386",
      "user-space",
      "/usr/lib/i386-linux-gnu/libnvidia-ml.so.580.178.04",
      "580.178.04",
      "580.178.04-0ubuntu0.22.04.1",
      "library_package_1; library_stat_1",
      "New coherent stack; architecture-specific path"
    ],
    [
      "libcuda amd64",
      "user-space",
      "/usr/lib/x86_64-linux-gnu/libcuda.so.580.178.04",
      "580.178.04",
      "580.178.04-0ubuntu0.22.04.1",
      "library_package_2; library_stat_2",
      "New coherent stack; architecture-specific path"
    ],
    [
      "libcuda i386",
      "user-space",
      "/usr/lib/i386-linux-gnu/libcuda.so.580.178.04",
      "580.178.04",
      "580.178.04-0ubuntu0.22.04.1",
      "library_package_3; library_stat_3",
      "New coherent stack; architecture-specific path"
    ],
    [
      "nvidia-smi",
      "user-space executable",
      "/usr/bin/nvidia-smi",
      "NVML reports580.178, exit18",
      "nvidia-utils-580-server 580.178.04-0ubuntu0.22.04.1",
      "smi_package; installed_packages; ctime2026-09-12 06:20:14+08",
      "New userspace cannot match old loaded module"
    ]
  ],
  "classification_justification": "Loaded580.173.02 is older than the selected on-disk module580.178.04 for kernel6.8.0-124-generic. Resolved NVML/libcuda (both architectures) and owning driver/compute/utils/DKMS packages are580.178.04. Boot2026-09-10 14:14:01 predates the recorded2026-09-12 06:20–06:22 package upgrade from580.173.02 to580.178.04; module mtime06:21:13 agrees. DKMS reports580.178.04 installed for running kernel. This meets the fixed stale-loaded-module rule, not installed split or recovered state. It is a reboot candidate only, not reboot authorization or guarantee.",
  "library_candidate_interpretation": "Two linker-cache entries per library are amd64 and i386 of the same version, not competing versions for one architecture. LD_LIBRARY_PATH and LD_PRELOAD empty in snapshot.",
  "package_interpretation": "nvidia-driver-570-server is explicitly a transitional package depending on nvidia-driver-580-server. Older rc entries are removed packages with configuration remnants. Container tooling and kernel ABI package version numbers are not NVIDIA driver version claims.",
  "nonzero_command_explanations": {
    "module_package": "dpkg-query -S exit1: generated DKMS .ko is not directly owned as a packaged file; dkms status identifies installed build.",
    "installed_packages": "exit1 solely for unmatched *cuda-drivers* pattern; full other matches retained including status codes.",
    "smi_list_SINGLE_ATTEMPT": "exit18 Driver/library version mismatch",
    "device_holders": "fuser exit1 and empty stdout/stderr: no visible holder reported at current unprivileged access. Does not establish machine idle or reboot safe."
  },
  "timeline_note": "Initial tail across rotated logs selected old entries; narrow dated extraction and sorting fixed evidence selection without repeating device query. Both raw ledgers retained.",
  "boot_kernel": "2026-09-14T21:30:24+08:00\nLinux wenchang-PR4904W1 6.8.0-124-generic #124~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Tue May 26 21:05:19 UTC  x86_64 x86_64 x86_64 GNU/Linux\n6.8.0-124-generic\n 21:30:24 up 4 days,  7:16,  1 user,  load average: 20.18, 20.22, 20.04\n2026-09-10 14:14:01\n         系统引导 2026-09-10 14:14",
  "module_hash": "4469ca921b755e8a9fe7a8a9eb5d886ca6c120ef3aa316e1e3d8b4e645eafd5d  /lib/modules/6.8.0-124-generic/updates/dkms/nvidia.ko",
  "module_vermagic": "6.8.0-124-generic SMP preempt mod_unload modversions",
  "proc_gpus": "/proc/driver/nvidia/gpus/0000:b1:00.0/information\nModel: \t\t NVIDIA RTX A6000\nIRQ:   \t\t 553\nGPU UUID: \t GPU-9de4332b-3b09-a3b4-5589-30229f0c14fe\nVideo BIOS: \t 94.02.5c.00.02\nBus Type: \t PCIe\nDMA Size: \t 47 bits\nDMA Mask: \t 0x7fffffffffff\nBus Location: \t 0000:b1:00.0\nDevice Minor: \t 0\nGPU Firmware: \t 580.173.02\nGPU Excluded:\t No\n/proc/driver/nvidia/gpus/0000:ca:00.0/information\nModel: \t\t NVIDIA RTX A6000\nIRQ:   \t\t 554\nGPU UUID: \t GPU-9c468c54-b125-4903-1476-77c4d63270be\nVideo BIOS: \t 94.02.5c.00.02\nBus Type: \t PCIe\nDMA Size: \t 47 bits\nDMA Mask: \t 0x7fffffffffff\nBus Location: \t 0000:ca:00.0\nDevice Minor: \t 1\nGPU Firmware: \t 580.173.02\nGPU Excluded:\t No",
  "loaded_modules": "nvidia_uvm           2093056  0\nnvidia_drm            139264  4\nnvidia_modeset       1638400  3 nvidia_drm\nnvidia              104198144  62 nvidia_uvm,nvidia_modeset",
  "venv_pre": [
    {
      "name": "pip",
      "version": "22.0.2"
    },
    {
      "name": "setuptools",
      "version": "59.6.0"
    }
  ],
  "venv_post": [
    {
      "name": "pip",
      "version": "22.0.2"
    },
    {
      "name": "setuptools",
      "version": "59.6.0"
    }
  ],
  "venv_equal": true,
  "python": "Python 3.10.12",
  "checkpoint_stat": "文件：/home/wenchang/asdasdsad/wjq/TOVD/shared/t013_yoloworld/weights/s_stage2-4466ab94.pth\n  大小：305058902 \t块：595824     IO 块大小：4096   普通文件\n设备：10309h/66313d\tInode：76310702    硬链接：1\n权限：(0644/-rw-r--r--)  Uid: ( 1012/liujianhua)   Gid: ( 1000/wenchang)\n访问时间：2026-09-14 18:05:25.450044020 +0800\n修改时间：2026-09-14 18:04:51.317147474 +0800\n变更时间：2026-09-14 18:05:25.447044029 +0800\n创建时间：2026-09-14 18:04:18.463260919 +0800",
  "checkpoint_sha256": "4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458  /home/wenchang/asdasdsad/wjq/TOVD/shared/t013_yoloworld/weights/s_stage2-4466ab94.pth",
  "smi_exit_code": 18,
  "smi_stdout": "Failed to initialize NVML: Driver/library version mismatch\nNVML library version: 580.178",
  "device_nodes": "crw-rw-rw- 1 root root 195,   0  9月 10 14:14 /dev/nvidia0\ncrw-rw-rw- 1 root root 195,   1  9月 10 14:14 /dev/nvidia1\ncrw-rw-rw- 1 root root 195, 255  9月 10 14:14 /dev/nvidiactl\ncrw-rw-rw- 1 root root 195, 254  9月 10 14:14 /dev/nvidia-modeset\ncrw-rw-rw- 1 root root 506,   0  9月 10 14:14 /dev/nvidia-uvm\ncrw-rw-rw- 1 root root 506,   1  9月 10 14:14 /dev/nvidia-uvm-tools",
  "device_holders": {
    "label": "device_holders",
    "command": "fuser -v /dev/nvidia*",
    "started_at": "2026-09-14T13:30:26.355742+00:00",
    "stopped_at": "2026-09-14T13:30:26.426997+00:00",
    "exit_code": 1,
    "stdout": "",
    "stderr": ""
  },
  "command_ledgers": [
    "command_ledger.json",
    "supplement_ledger.json",
    "transport_ledger.json (prior preserved attempts)"
  ],
  "execution_commands": [
    "/usr/bin/python3.10 /home/wenchang/asdasdsad/wjq/TOVD/research_log/t013_yoloworld/p3r7/snapshot.py",
    "/usr/bin/python3.10 /home/wenchang/asdasdsad/wjq/TOVD/research_log/t013_yoloworld/p3r7/supplement.py"
  ],
  "execution_exit_codes": [
    0,
    0
  ],
  "counts": {
    "nvidia_smi_L_entire_P3R7": 1,
    "reboots": 0,
    "driver_module_reload_reset": 0,
    "package_mutations": 0,
    "linker_symlink_mutations": 0,
    "fixed_Torch_installs": 0,
    "CUDA_tensor_smokes": 0,
    "checkpoint_deserializations": 0,
    "model_constructions_loads": 0,
    "detector_forwards": 0,
    "T013_COCO_LVIS_science": 0,
    "Grounding_reruns": 0,
    "T014_CF_MECH_science": 0,
    "YOLO_scientific_benchmark": 0
  },
  "preservation": "P0/P1/P2/P3/P3R1–P3R6 evidence unchanged; environment unchanged; checkpoint305058902bytes and exact frozen SHA256; all YOLO settings frozen; GROUNDING_PRIMARY_NOT_SUPPORTED remains canonical.",
  "repair_recommendation": "Research Lead review required",
  "next_action": "Research Lead review of P3R7 host-driver consistency adjudication before any reboot, driver repair, Torch install, or model-runtime work"
}
```
