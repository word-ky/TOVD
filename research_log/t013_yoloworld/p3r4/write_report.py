"""Bind hosted acquisition and artifact API evidence; no payload retrieval."""
import datetime
import hashlib
import json
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
read=lambda name:json.loads((OUT/name).read_text(encoding='utf-8'))
a=read('acquisition_receipt.json'); run=read('run.json'); artifact=read('artifacts.json')['artifacts'][0]
assert a['verified'] and a['observed_bytes']==305058902 and a['observed_sha256']=='4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458'
assert run['conclusion']=='success' and run['run_attempt']==1 and artifact['workflow_run']['head_sha']==a['workflow_commit']
workflow=ROOT/'.github/workflows/t013_yw_checkpoint_relay.yml'
r=dict(task='T013-YW-P3R4',task_start_head='b9c8358d2a206cabca7ad67e2d7289b73fd2e877',lead_instruction_commit='8087c128ea0bd1ea41d755df5351b12b91423993',state='YW_P3R4_RELAY_ARTIFACT_READY_RETURN_TO_LEAD',heartbeat_started_at='2026-09-14T09:20:16.607Z',stopped_at=datetime.datetime.now().astimezone().isoformat(),workflow_path=workflow.relative_to(ROOT).as_posix(),workflow_sha256=hashlib.sha256(workflow.read_bytes()).hexdigest(),workflow_commit=a['workflow_commit'],trigger='workflow_dispatch only',permissions={'contents':'read'},runner_label='ubuntu-latest',observed_image='ubuntu-24.04 / 20260907.300.1 / Ubuntu 24.04.5 LTS',run_id=run['id'],run_attempt=run['run_attempt'],run_url=run['html_url'],conclusion=run['conclusion'],run_created_at=run['created_at'],run_updated_at=run['updated_at'],job_duration_seconds=19,acquisition=a,artifact=artifact,retention_days=2,artifact_files=['s_stage2-4466ab94.pth','acquisition_receipt.json'],artifact_file_count_log=2,upload_action_sha='ea165f8d65b6e75b540449e92b4886f43607fa02',acquisition_receipt_sha256=hashlib.sha256((OUT/'acquisition_receipt.json').read_bytes()).hexdigest(),receipt_provenance='Exact JSON printed by runner, reconstructed by stripping GitHub log timestamps; artifact itself not downloaded',counts={k:0 for k in ['workflow_reruns','alternate_runner_provider','alternate_checkpoint_model_revision_source_selection','server_checkpoint_partial_import','package_install_build','checkpoint_deserialization','CUDA_model_load_forward','T013_COCO_LVIS_scientific_actions','Grounding_rerun','T014_CF_MECH_science']},next_action='Research Lead review of P3R4 relay artifact before any server import or runtime feasibility resumption')
r['counts']['Actions_workflow_dispatches']=1
r['log_retrieval_note']='Initial local REST job-log redirect returned HTTP401 InvalidAuthenticationInfo; existing GitHub connector fetched logs successfully. No workflow rerun or credential change.'
(OUT/'delivery_receipt.json').write_text(json.dumps(r,indent=2)+'\n')
report=f'''# T013-YW-P3R4 — exact relay artifact ready

State: **{r['state']}**. Task-start `{r['task_start_head']}`; Lead `{r['lead_instruction_commit']}`. Heartbeat started {r['heartbeat_started_at']}; report finalized {r['stopped_at']}.

Exactly one workflow dispatch returned HTTP204. Run [{run['id']}]({run['html_url']}), attempt1, conclusion success; job 09:22:56–09:23:15 UTC (19 seconds), acquisition 09:22:57–09:23:11 UTC. Workflow `.github/workflows/t013_yw_checkpoint_relay.yml` commit `{a['workflow_commit']}`, SHA256 `{r['workflow_sha256']}`. Trigger is workflow_dispatch only, contents:read; no push/PR/schedule trigger. Existing Git credential manager authentication used without installation or credential creation. Hosted ubuntu-latest resolved to Ubuntu24.04.5 LTS, ubuntu-24.04 image20260907.300.1. Upload-artifact@v4 resolved SHA `{r['upload_action_sha']}`.

Fixed asset: wondervictor/YOLO-World-V2.1 at c620164ee3979bf49b895c8a8e0f49aeaca89209, s_stage2-4466ab94.pth. Initial URL {a['initial_url']}. No alternate initial URL/revision/checkpoint. curl8.5.0/OpenSSL3.0.13 exited0, HTTP200, TLS verification0, one automatic HTTPS redirect, 305058902 bytes received in13.353016s. Final host/path with query removed: {a['transport']['final_effective_host_path']}. The CDN URL was not manually selected.

Acquisition command: `curl --fail --location --silent --show-error --proto '=https' --proto-redir '=https' --connect-timeout 45 --max-time 1200 --output checkpoint.partial --write-out '%{{json}}' "$initial" > transport.json`. Normal certificate validation, no package installation. `stat -c '%s' checkpoint.partial` returned305058902; `sha256sum checkpoint.partial` returned4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458. Both exactly match frozen expected values; upload ran only after this condition succeeded.

Artifact `{artifact['name']}`, ID{artifact['id']}, ZIP size{artifact['size_in_bytes']} bytes, digest `{artifact['digest']}`. Upload logs report exactly2 files: checkpoint plus acquisition_receipt.json. Retention2days; expires {artifact['expires_at']} (2026-09-16 17:23:11+08). Artifact metadata retrieved through GitHub API; payload ZIP was not downloaded locally or to the experiment server. Server import count0. The runner-printed JSON receipt is retained at research_log/t013_yoloworld/p3r4/acquisition_receipt.json, SHA256 `{r['acquisition_receipt_sha256']}`; reconstructed by stripping log timestamp prefixes, not independently extracted from the ZIP.

Initial local REST job-log retrieval returned HTTP401 at its redirect. Existing GitHub connector successfully retrieved complete logs; original failure body remains job.log, successful logs hosted_job.log. This read failure did not affect the successful workflow and caused no rerun or credential change. No unexpected acquisition/hash failure occurred.

Counts: dispatch1, rerun0, alternate runner/provider0, alternate checkpoint/model/revision/content-source selection0, server import0, package/build0, deserialization0, CUDA/model-load/forward0, T013/COCO/LVIS science0, Grounding rerun0, T014/CF/MECH science0. P3/P3R1/P3R2/P3R3, Grounding freeze/cache/receipts/decision, YOLO P0/P1/P2 and all scientific settings unchanged. Relay success is transport evidence only; no runtime or scientific claim. Changed paths: dedicated workflow, separate p3r4 directory, appended coordination/CODEX_TO_CHATGPT.md and research_log/session_log.md. Full artifact hashes: delivery_manifest.json.

Recommended next action: **{r['next_action']}**. Stop; no unchanged-mailbox dispatch or server import.
'''
(OUT/'P3R4_REPORT.md').write_text(report,encoding='utf-8')
with (ROOT/'coordination/CODEX_TO_CHATGPT.md').open('a',encoding='utf-8') as f:f.write('\n\n---\n\n'+report+'\nMachine delivery receipt:\n```json\n'+json.dumps(r,indent=2)+'\n```\n')
with (ROOT/'research_log/session_log.md').open('a',encoding='utf-8') as f:f.write('\n## '+r['stopped_at']+' — P3R4 RELAY_ARTIFACT_READY\nSingle run34827628282/attempt1 success; exact305058902bytes/SHA4466ab94...f458 verified by hosted runner. Artifact10341040916 fixed name,2files,305061442bytes,expires2026-09-16T09:23:11Z. No payload/server import/runtime. Workflow0a9e6a0, complete p3r4 logs/receipts. REST log redirect401 recovered using existing connector; no rerun. Await Lead review before import/runtime; no unchanged-mailbox repeat.\n')
m={p.name:dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='delivery_manifest.json'}
(OUT/'delivery_manifest.json').write_text(json.dumps(m,indent=2)+'\n')
print(r['state'])
