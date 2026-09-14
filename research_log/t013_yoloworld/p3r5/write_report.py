"""Persist the observed P3R5 import result; never runs experiment code."""
import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
def read_log(name):
    raw = (OUT / name).read_bytes()
    return raw.decode('utf-16' if raw.startswith((b'\xff\xfe', b'\xfe\xff')) else 'utf-8-sig')

r = json.loads((OUT / 'archive_validation.json').read_text())
assert r['archive_validation_passed']
placement = read_log('server_placement.txt')
assert 'FINAL_CHECKPOINT_VERIFIED' in placement
r.update({
    'state': 'YW_P3R5_CHECKPOINT_IMPORTED_VERIFIED_RETURN_TO_LEAD',
    'stopped_at': '2026-09-14T18:05:28+08:00',
    'preflight_destination_exists': False,
    'preflight_output': read_log('server_preflight.txt'),
    'server_free_bytes': 161612546048,
    'server_destination': '/home/wenchang/asdasdsad/wjq/TOVD/shared/t013_yoloworld/weights/s_stage2-4466ab94.pth',
    'server_temporary_path': '/home/wenchang/asdasdsad/wjq/TOVD/shared/t013_yoloworld/weights/.p3r5-s_stage2-4466ab94.partial',
    'placement': 'Copy-ToAutodl (existing SSH/SCP) from the verified local extracted checkpoint to the sibling .p3r5-s_stage2-4466ab94.partial; verify stat/sha256sum; test final absent; mv -T temporary destination on same filesystem; verify final stat/sha256sum. Exact bash script: place_checkpoint.sh.',
    'copy_command': "Copy-ToAutodl -LocalPath 'D:\\work\\fightccfa-agin\\CVPR2027\\TTT-OVD\\.autodl\\p3r5\\extracted\\s_stage2-4466ab94.pth' -RemotePath '/home/wenchang/asdasdsad/wjq/TOVD/shared/t013_yoloworld/weights/.p3r5-s_stage2-4466ab94.partial'",
    'copy_exit_code': 0,
    'placement_command': 'bash /home/wenchang/asdasdsad/wjq/TOVD/research_log/t013_yoloworld/p3r5/place_checkpoint.sh',
    'placement_exit_code': 0,
    'placement_output': placement,
    'final_bytes': 305058902,
    'final_sha256': r['checkpoint_sha256'],
    'final_inode': 76310702,
    'final_mtime': '2026-09-14 18:04:51.317147474 +0800',
    'newly_installed': True,
    'local_verification_commands': 'Path.stat().st_size and hashlib.file_digest(open(path, rb), sha256) in import_archive.py; complete outputs in archive_validation.json.',
    'temporary_disposition': 'Local archive and both extracted files retained under ignored .autodl/p3r5. Remote sibling temporary file consumed by atomic rename. No cleanup commands.',
    'counts': {'P3R4_workflow_reruns': 0, 'artifact_downloads': 1, 'server_checkpoint_imports': 1, 'alternate_artifact_source_checkpoint_model_revision': 0, 'package_install_build': 0, 'checkpoint_deserialization': 0, 'CUDA_model_load_forward': 0, 'T013_COCO_LVIS_scientific_actions': 0, 'Grounding_rerun': 0, 'T014_CF_MECH_science': 0, 'YOLO_scientific_benchmark': 0, 'Hugging_Face_requests': 0},
    'preservation': 'GROUNDING_PRIMARY_NOT_SUPPORTED remains canonical. Existing environment, sources, CLIP cache, synthetic_smoke.py, P0/P1/P2/P3/P3R1–P3R4 evidence and all YOLO scientific settings unchanged. Import success establishes byte provenance only, not runtime feasibility or scientific support.',
    'next_action': 'Research Lead review of P3R5 server-side checkpoint provenance before any runtime-feasibility resumption',
})
(OUT / 'import_receipt.json').write_text(json.dumps(r, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
report = f'''# T013-YW-P3R5 — Server checkpoint import verified

State: **{r['state']}**

Task start: {r['task_started_at']}; terminal stop: {r['stopped_at']}.
Task-start HEAD: `{r['task_start_head']}`. Lead instruction: `{r['lead_instruction_commit']}`.

The fixed server destination was absent; free space was 161612546048 bytes. The one accepted, unexpired artifact was downloaded exactly once through existing Git credential-manager authentication, with normal TLS and no credentials forwarded to the cross-origin delivery redirect. No credentials or signed delivery URLs are retained. The archive was exactly 305061442 bytes and SHA256 `2589f9b63f57e51d4646ea114cdbff0bf7896d7988c8a499360bb077ef76c5bf`, matching live GitHub digest metadata. API endpoint, command, exit code, download timing, local free space and metadata are in the machine receipt below.

Artifact10341040916, name `t013-yw-s-stage2-4466ab94-relay`, run34827628282/attempt1, head `0a9e6a004191c9ab20db4feeebab51d88cc3760d`, expired=false, expires2026-09-16T09:23:11Z. ZIP inspection before extraction found exactly two regular files: `s_stage2-4466ab94.pth` and `acquisition_receipt.json`; no duplicate, absolute/traversal path, symlink, nesting or extra member. Embedded receipt: 2244 bytes, SHA256 `d64080965c78597c853d3f99c34cdf2885d7d5154f0f1141cd81b4639270241f`; verified=true and all required provenance fields equal the accepted P3R4 record.

Extracted, server temporary and final checkpoint each matched 305058902 bytes and SHA256 `{r['final_sha256']}`. Existing SCP copied the verified local extraction to the fixed destination's sibling temporary file. `place_checkpoint.sh` verified that temporary file, checked destination absence, performed same-filesystem `mv -T`, and verified final size/hash; exit0. Final inode76310702; mtime2026-09-14 18:04:51.317147474 +0800. Fixed destination: `{r['server_destination']}`. This was a new installation. Local temporary archive/extraction are retained in ignored `.autodl/p3r5`; the server temporary name was consumed by rename. No large payload is tracked by Git.

{r['preservation']}

Next action: **{r['next_action']}**.

## Exact machine-readable evidence

```json
{json.dumps(r, indent=2, ensure_ascii=False)}
```
'''
(OUT / 'P3R5_REPORT.md').write_text(report, encoding='utf-8')
manifest = {str(p.relative_to(ROOT)).replace('\\', '/'): {'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(OUT.iterdir()) if p.is_file() and p.name != 'delivery_manifest.json'}
(OUT / 'delivery_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
with (ROOT / 'coordination/CODEX_TO_CHATGPT.md').open('a', encoding='utf-8') as f:
    f.write('\n\n---\n\n' + report)
entry = f"\n\n## 2026-09-14T18:05:28+08:00 — P3R5 checkpoint imported verified\nLead{r['lead_instruction_commit']}, task-start{r['task_start_head']}. Single bound artifact10341040916/run34827628282 downloaded once; archive/member/receipt/checkpoint checks passed. SCP sibling temporary + atomic rename; final305058902bytes/SHA{r['final_sha256']}, inode76310702. State {r['state']}. Receipts/report/manifest: research_log/t013_yoloworld/p3r5/. Existing env and scientific evidence unchanged; runtime/GPU/science0. No repeat import on unchanged mailbox. Next: {r['next_action']}.\n"
for path in ['research_log/SESSION_LOG.md', 'research_log/REMOTE.md']:
    with (ROOT / path).open('a', encoding='utf-8') as f:
        f.write(entry)
print(json.dumps(manifest['research_log/t013_yoloworld/p3r5/import_receipt.json']))
