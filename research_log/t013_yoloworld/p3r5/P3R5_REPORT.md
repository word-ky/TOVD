# T013-YW-P3R5 — Server checkpoint import verified

State: **YW_P3R5_CHECKPOINT_IMPORTED_VERIFIED_RETURN_TO_LEAD**

Task start: 2026-09-14T09:58:18.512Z; terminal stop: 2026-09-14T18:05:28+08:00.
Task-start HEAD: `06610b250e74166fd56c1a49b7d011441ded38d6`. Lead instruction: `ae07716fb90c9b8979aad4ed695ef5f3b498af05`.

The fixed server destination was absent; free space was 161612546048 bytes. The one accepted, unexpired artifact was downloaded exactly once through existing Git credential-manager authentication, with normal TLS and no credentials forwarded to the cross-origin delivery redirect. No credentials or signed delivery URLs are retained. The archive was exactly 305061442 bytes and SHA256 `2589f9b63f57e51d4646ea114cdbff0bf7896d7988c8a499360bb077ef76c5bf`, matching live GitHub digest metadata. API endpoint, command, exit code, download timing, local free space and metadata are in the machine receipt below.

Artifact10341040916, name `t013-yw-s-stage2-4466ab94-relay`, run34827628282/attempt1, head `0a9e6a004191c9ab20db4feeebab51d88cc3760d`, expired=false, expires2026-09-16T09:23:11Z. ZIP inspection before extraction found exactly two regular files: `s_stage2-4466ab94.pth` and `acquisition_receipt.json`; no duplicate, absolute/traversal path, symlink, nesting or extra member. Embedded receipt: 2244 bytes, SHA256 `d64080965c78597c853d3f99c34cdf2885d7d5154f0f1141cd81b4639270241f`; verified=true and all required provenance fields equal the accepted P3R4 record.

Extracted, server temporary and final checkpoint each matched 305058902 bytes and SHA256 `4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458`. Existing SCP copied the verified local extraction to the fixed destination's sibling temporary file. `place_checkpoint.sh` verified that temporary file, checked destination absence, performed same-filesystem `mv -T`, and verified final size/hash; exit0. Final inode76310702; mtime2026-09-14 18:04:51.317147474 +0800. Fixed destination: `/home/wenchang/asdasdsad/wjq/TOVD/shared/t013_yoloworld/weights/s_stage2-4466ab94.pth`. This was a new installation. Local temporary archive/extraction are retained in ignored `.autodl/p3r5`; the server temporary name was consumed by rename. No large payload is tracked by Git.

GROUNDING_PRIMARY_NOT_SUPPORTED remains canonical. Existing environment, sources, CLIP cache, synthetic_smoke.py, P0/P1/P2/P3/P3R1–P3R4 evidence and all YOLO scientific settings unchanged. Import success establishes byte provenance only, not runtime feasibility or scientific support.

Next action: **Research Lead review of P3R5 server-side checkpoint provenance before any runtime-feasibility resumption**.

## Exact machine-readable evidence

```json
{
  "task": "T013-YW-P3R5",
  "task_started_at": "2026-09-14T09:58:18.512Z",
  "task_start_head": "06610b250e74166fd56c1a49b7d011441ded38d6",
  "lead_instruction_commit": "ae07716fb90c9b8979aad4ed695ef5f3b498af05",
  "archive_download_count": 1,
  "download_endpoint": "https://api.github.com/repos/word-ky/TOVD/actions/artifacts/10341040916/zip",
  "command": "D:/anaconda3/python.exe research_log/t013_yoloworld/p3r5/import_archive.py",
  "archive_path": "D:\\work\\fightccfa-agin\\CVPR2027\\TTT-OVD\\.autodl\\p3r5\\artifact-10341040916.zip",
  "extraction_path": "D:\\work\\fightccfa-agin\\CVPR2027\\TTT-OVD\\.autodl\\p3r5\\extracted",
  "local_free_space": {
    "total": 294972813312,
    "used": 293566230528,
    "free": 1406582784
  },
  "already_present_exact": false,
  "temporary_files_retained": true,
  "artifact_metadata": {
    "id": 10341040916,
    "node_id": "MDg6QXJ0aWZhY3QxMDM0MTA0MDkxNg==",
    "name": "t013-yw-s-stage2-4466ab94-relay",
    "size_in_bytes": 305061442,
    "url": "https://api.github.com/repos/word-ky/TOVD/actions/artifacts/10341040916",
    "archive_download_url": "https://api.github.com/repos/word-ky/TOVD/actions/artifacts/10341040916/zip",
    "expired": false,
    "digest": "sha256:2589f9b63f57e51d4646ea114cdbff0bf7896d7988c8a499360bb077ef76c5bf",
    "created_at": "2026-09-14T09:23:13Z",
    "updated_at": "2026-09-14T09:23:13Z",
    "expires_at": "2026-09-16T09:23:11Z",
    "workflow_run": {
      "id": 34827628282,
      "repository_id": 1366464556,
      "head_repository_id": 1366464556,
      "head_branch": "main",
      "head_sha": "0a9e6a004191c9ab20db4feeebab51d88cc3760d"
    }
  },
  "run_binding": {
    "id": 34827628282,
    "run_attempt": 1,
    "head_sha": "0a9e6a004191c9ab20db4feeebab51d88cc3760d",
    "status": "completed",
    "conclusion": "success"
  },
  "download_started_at": "2026-09-14T10:03:04.958956+00:00",
  "download_http_status": 200,
  "delivery_host": "productionresultssa12.blob.core.windows.net",
  "download_stopped_at": "2026-09-14T10:03:59.828775+00:00",
  "download_exit_code": 0,
  "archive_bytes": 305061442,
  "archive_sha256": "2589f9b63f57e51d4646ea114cdbff0bf7896d7988c8a499360bb077ef76c5bf",
  "archive_digest_matches": true,
  "archive_members": [
    {
      "name": "s_stage2-4466ab94.pth",
      "bytes": 305058902,
      "external_attr": 2175008800,
      "create_system": 3
    },
    {
      "name": "acquisition_receipt.json",
      "bytes": 2244,
      "external_attr": 2175008800,
      "create_system": 3
    }
  ],
  "member_safety_checks": {
    "exact_two_regular_files": true,
    "duplicates": false,
    "traversal": false,
    "absolute_paths": false,
    "symlinks": false,
    "nesting_or_extra": false
  },
  "embedded_receipt_bytes": 2244,
  "embedded_receipt_sha256": "d64080965c78597c853d3f99c34cdf2885d7d5154f0f1141cd81b4639270241f",
  "embedded_receipt_binding": {
    "verified": true,
    "run_id": "34827628282",
    "run_attempt": "1",
    "workflow_commit": "0a9e6a004191c9ab20db4feeebab51d88cc3760d",
    "initial_url": "https://huggingface.co/wondervictor/YOLO-World-V2.1/resolve/c620164ee3979bf49b895c8a8e0f49aeaca89209/s_stage2-4466ab94.pth",
    "expected_bytes": 305058902,
    "observed_bytes": 305058902,
    "expected_sha256": "4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458",
    "observed_sha256": "4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458"
  },
  "receipt_binding_matches_accepted_p3r4": true,
  "checkpoint_bytes": 305058902,
  "checkpoint_sha256": "4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458",
  "archive_validation_passed": true,
  "state": "YW_P3R5_CHECKPOINT_IMPORTED_VERIFIED_RETURN_TO_LEAD",
  "local_validation_stopped_at": "2026-09-14T10:04:01.437185+00:00",
  "stopped_at": "2026-09-14T18:05:28+08:00",
  "preflight_destination_exists": false,
  "preflight_output": "2026-09-14T18:01:45+08:00\r\n文件系统              1B的块          已用         可用 已用% 挂载点\r\n/dev/nvme0n1p9 2497827418112 2209256124416 161612546048   94% /home\r\nFINAL_ABSENT\r\n",
  "server_free_bytes": 161612546048,
  "server_destination": "/home/wenchang/asdasdsad/wjq/TOVD/shared/t013_yoloworld/weights/s_stage2-4466ab94.pth",
  "server_temporary_path": "/home/wenchang/asdasdsad/wjq/TOVD/shared/t013_yoloworld/weights/.p3r5-s_stage2-4466ab94.partial",
  "placement": "Copy-ToAutodl (existing SSH/SCP) from the verified local extracted checkpoint to the sibling .p3r5-s_stage2-4466ab94.partial; verify stat/sha256sum; test final absent; mv -T temporary destination on same filesystem; verify final stat/sha256sum. Exact bash script: place_checkpoint.sh.",
  "copy_command": "Copy-ToAutodl -LocalPath 'D:\\work\\fightccfa-agin\\CVPR2027\\TTT-OVD\\.autodl\\p3r5\\extracted\\s_stage2-4466ab94.pth' -RemotePath '/home/wenchang/asdasdsad/wjq/TOVD/shared/t013_yoloworld/weights/.p3r5-s_stage2-4466ab94.partial'",
  "copy_exit_code": 0,
  "placement_command": "bash /home/wenchang/asdasdsad/wjq/TOVD/research_log/t013_yoloworld/p3r5/place_checkpoint.sh",
  "placement_exit_code": 0,
  "placement_output": "2026-09-14T18:05:22+08:00\r\ntemporary_bytes=305058902\r\n4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458  /home/wenchang/asdasdsad/wjq/TOVD/shared/t013_yoloworld/weights/.p3r5-s_stage2-4466ab94.partial\r\nfinal_bytes=305058902\r\nfinal_inode=76310702\r\nfinal_mtime=2026-09-14 18:04:51.317147474 +0800\r\n4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458  /home/wenchang/asdasdsad/wjq/TOVD/shared/t013_yoloworld/weights/s_stage2-4466ab94.pth\r\nFINAL_CHECKPOINT_VERIFIED\r\n2026-09-14T18:05:28+08:00\r\n",
  "final_bytes": 305058902,
  "final_sha256": "4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458",
  "final_inode": 76310702,
  "final_mtime": "2026-09-14 18:04:51.317147474 +0800",
  "newly_installed": true,
  "local_verification_commands": "Path.stat().st_size and hashlib.file_digest(open(path, rb), sha256) in import_archive.py; complete outputs in archive_validation.json.",
  "temporary_disposition": "Local archive and both extracted files retained under ignored .autodl/p3r5. Remote sibling temporary file consumed by atomic rename. No cleanup commands.",
  "counts": {
    "P3R4_workflow_reruns": 0,
    "artifact_downloads": 1,
    "server_checkpoint_imports": 1,
    "alternate_artifact_source_checkpoint_model_revision": 0,
    "package_install_build": 0,
    "checkpoint_deserialization": 0,
    "CUDA_model_load_forward": 0,
    "T013_COCO_LVIS_scientific_actions": 0,
    "Grounding_rerun": 0,
    "T014_CF_MECH_science": 0,
    "YOLO_scientific_benchmark": 0,
    "Hugging_Face_requests": 0
  },
  "preservation": "GROUNDING_PRIMARY_NOT_SUPPORTED remains canonical. Existing environment, sources, CLIP cache, synthetic_smoke.py, P0/P1/P2/P3/P3R1–P3R4 evidence and all YOLO scientific settings unchanged. Import success establishes byte provenance only, not runtime feasibility or scientific support.",
  "next_action": "Research Lead review of P3R5 server-side checkpoint provenance before any runtime-feasibility resumption"
}
```
