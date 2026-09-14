"""Serialize P3R2 metadata adjudication; no network or model calls."""
import hashlib
import json
from pathlib import Path

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
r=json.loads((OUT/'network_receipt.json').read_text())
r['state']='YW_P3R2_AMBIGUOUS_RETURN_TO_LEAD'
r['stopped_at']=r['ab_stopped_at']
r['reason']='Both independent DoH services unavailable; no independent address for authorized same-origin probe. PyPI control succeeds, so broad egress blockage is not established.'
r['asset']=dict(repository='wondervictor/YOLO-World-V2.1',revision='c620164ee3979bf49b895c8a8e0f49aeaca89209',filename='s_stage2-4466ab94.pth',url='https://huggingface.co/wondervictor/YOLO-World-V2.1/resolve/c620164ee3979bf49b895c8a8e0f49aeaca89209/s_stage2-4466ab94.pth',expected_bytes=305058902,expected_sha256='4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458')
r['counts']={k:0 for k in ['checkpoint_partial_files_created','checkpoint_payload_download_attempts','alternate_checkpoint_model','alternate_content_host_mirror','network_DNS_configuration_changes','package_install_build','checkpoint_deserialization','CUDA_model_load_forward','T013_COCO_LVIS_scientific_actions','Grounding_rerun','T014_CF_MECH_scientific_work']}
r['independent_DNS_agreement']='UNAVAILABLE: all four queries returned no DNS response; no returned addresses/status/TTL'
r['same_origin_probe_skip_reason']='Step B produced no independent address; Step C prerequisite unmet'
r['first_probe_failure']=r['controls'][0]
r['preserved']='Original P3/P3R1 artifacts, Grounding freeze/cache/receipts/decision, YOLO P0/P1/P2 freeze and scientific settings unchanged.'
r['driver_command']='/usr/bin/python3.10 /home/wenchang/asdasdsad/wjq/TOVD/research_log/t013_yoloworld/p3r2/network_metadata.py'
r['driver_exit_code']=0
r['next_action']='Research Lead review of resolver/path evidence before any checkpoint recovery'
(OUT/'adjudication_receipt.json').write_text(json.dumps(r,indent=2)+'\n')
report=f'''# T013-YW-P3R2 — resolver/path attribution remains ambiguous

State: **{r['state']}**.
Task-start HEAD: `{r['task_start_head']}`. Lead instruction: `{r['lead_instruction_commit']}`.
Probe interval: {r['started_at']} through {r['stopped_at']}. Metadata driver exit 0; individual failures retained below.

PyPI returned HTTP 200 with verified TLS (151.101.192.223, 0.245516 s). GitHub connected and completed TLS (20.205.243.166, TLS time 0.463352 s, verification result 0), then timed out after 30.001642 s without HTTP response (curl 28). Thus these controls do not establish a universal outbound block.

Google DoH A/AAAA both failed before connection with curl 28, after 11355/11352 ms. Cloudflare DoH A/AAAA both failed with curl 35: `OpenSSL SSL_connect: 连接被对方重置 in connection to cloudflare-dns.com:443`. All four returned no DNS JSON, addresses, TTL or status. Agreement with each other or system DNS is unavailable. No independently obtained address exists for Step C: same-origin --resolve probes = 0. No additional client/resolver or retry was improvised.

System `getent ahosts huggingface.co` succeeded and returned IPv4 199.59.149.231 and IPv6 2a03:2880:f134:183:face:b00c:0:25de. These differ from the P3R1 observations, but variation alone does not establish resolver causation. `/etc/resolv.conf` uses nameserver 127.0.0.53, options edns0 trust-ad, search dot; full content retained in the receipt, SHA256 ebdf560272a77357195c39e98340b77e18c8a8ce2025ee950e9e0c7b01467ab8.

HTTP_PROXY, HTTPS_PROXY, ALL_PROXY, http_proxy, https_proxy, all_proxy, NO_PROXY and no_proxy are all unset; no proxy values were read or printed. Existing curl 7.81.0 / OpenSSL 3.0.2 advertises HTTPS, HTTP2 and SSL, with --doh-url and --resolve exposed in help. No curl replacement or certificate bypass occurred.

Frozen asset: {r['asset']['repository']}, revision {r['asset']['revision']}, file {r['asset']['filename']}; expected {r['asset']['expected_bytes']} bytes, SHA256 {r['asset']['expected_sha256']}. Exact URL: {r['asset']['url']}. No request to this URL occurred in P3R2; no payload acquired, partial created, checkpoint hash reverified or model deserialized.

All prohibited-action counts are 0: checkpoint/partial creation, payload-download attempt, alternate checkpoint/model or content host/mirror, network/DNS configuration change, package install/build, checkpoint deserialization, CUDA/model-load/forward, T013/COCO/LVIS science, Grounding rerun, T014/CF/MECH scientific work. P3/P3R1, Grounding and YOLO freezes/settings remain unchanged. No background job remains.

Exact command arrays, timestamped results, resolver content, curl features, DNS failures, TLS/HTTP/IP/timing fields and empty same-origin probe list are in adjudication_receipt.json (raw A/B evidence: network_receipt.json). Changed paths: this separate p3r2 directory, plus append-only coordination/CODEX_TO_CHATGPT.md and research_log/session_log.md. File hashes are in delivery_manifest.json. These are network observations only, not runtime or scientific evidence. Do not repeat the package on an unchanged mailbox.

Recommended next action: **{r['next_action']}**.
'''
(OUT/'P3R2_REPORT.md').write_text(report,encoding='utf-8')
with (ROOT/'coordination/CODEX_TO_CHATGPT.md').open('a',encoding='utf-8') as f:
    f.write('\n\n---\n\n'+report+'\nComplete P3R2 metadata receipt:\n```json\n'+json.dumps(r,indent=2)+'\n```\n')
with (ROOT/'research_log/session_log.md').open('a',encoding='utf-8') as f:
    f.write('\n## '+r['stopped_at']+' — P3R2 AMBIGUOUS\nIndependent Google DoH A/AAAA exit28 and Cloudflare A/AAAA exit35; no records, Step C not run. PyPI HTTP200/TLSvalid, GitHub TLSvalid then response timeout. System DNS changed versus P3R1, insufficient for causal attribution. No checkpoint, network change, installation, GPU or scientific action. Full separate p3r2 evidence; await Research Lead review of resolver/path evidence before any checkpoint recovery. No unchanged-mailbox repeat.\n')
manifest={p.name:dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='delivery_manifest.json'}
(OUT/'delivery_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
