"""Adjudicate the fixed DNS consensus rule from recorded metadata only."""
import hashlib
import ipaddress
import json
from pathlib import Path

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
r=json.loads((OUT/'dns_receipt.json').read_text())
support={'A':{},'AAAA':{}}
for q in r['queries']:
    for a in q['answers']:
        if a['type'] in support:
            servers=support[a['type']].setdefault(a['data'],set())
            if q['aa'] and q['rcode']=='NOERROR': servers.add(q['server_ip'])
r['consensus']={kind:{addr:dict(authoritative_server_count=len(servers),servers=sorted(servers)) for addr,servers in values.items()} for kind,values in support.items()}
r['eligible']={kind:sorted([addr for addr,servers in values.items() if len(servers)>=2],key=ipaddress.ip_address) for kind,values in support.items()}
system=sorted({line.split()[0] for line in r['system_dns']['stdout'].splitlines() if line.strip()})
r['system_addresses']=system
r['eligible_system_overlap']={kind:sorted(set(values)&set(system)) for kind,values in r['eligible'].items()}
assert not r['eligible']['A']
r['state']='YW_P3R3_AUTHORITATIVE_DNS_INCONSISTENT_RETURN_TO_LEAD'
r['stopped_at']=r['dns_stopped_at']
r['reason']='Direct replies exist, but no A address has AA-marked support from two fixed servers. All four A answers differ; only one has AA set.'
r['asset']=dict(repository='wondervictor/YOLO-World-V2.1',revision='c620164ee3979bf49b895c8a8e0f49aeaca89209',filename='s_stage2-4466ab94.pth',url='https://huggingface.co/wondervictor/YOLO-World-V2.1/resolve/c620164ee3979bf49b895c8a8e0f49aeaca89209/s_stage2-4466ab94.pth',expected_bytes=305058902,expected_sha256='4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458')
r['counts']={k:0 for k in ['checkpoint_partial_files_created','checkpoint_payload_download_attempts','alternate_checkpoint_model_content_host','resolver_network_configuration_changes','package_install_build','checkpoint_deserialization','CUDA_model_load_forward','T013_COCO_LVIS_scientific_actions','Grounding_rerun','T014_CF_MECH_science','TCP_retry','same_origin_probe']}
r['counts']['UDP_queries']=8
r['driver_command']='/usr/bin/python3.10 /home/wenchang/asdasdsad/wjq/TOVD/research_log/t013_yoloworld/p3r3/authoritative_dns.py'
r['driver_exit_code']=0
r['preserved']='P3/P3R1/P3R2, Grounding freeze/cache/receipts/decision, YOLO P0/P1/P2 freeze and scientific settings unchanged.'
r['next_action']='Research Lead review of P3R3 authoritative-path evidence before any checkpoint recovery'
(OUT/'adjudication_receipt.json').write_text(json.dumps(r,indent=2)+'\n')
rows=[]
for q in r['queries']:
    a=q['answers'][0]
    rows.append(f"| {q['server_ip']} | {q['record_type']} | {a['data']} | {a['ttl']} | {q['aa']} | {q['tc']} | {q['elapsed_seconds']} |")
report=f'''# T013-YW-P3R3 — direct DNS replies fail consensus

State: **{r['state']}**.
Task-start HEAD: `{r['task_start_head']}`. Lead instruction: `{r['lead_instruction_commit']}`.
Probe interval: {r['started_at']} to {r['stopped_at']}; driver exit 0.

Exactly eight UDP nonrecursive queries to the four fixed server IPs completed, all exit 0 / RCODE NOERROR. All TC flags were false: no TCP retry. Replies existed, so this is not the DNS-unreachable state. All four A answers differed; only the first A reply had AA set. No A address met the fixed >=2 authoritative-server rule. Eligible A and AAAA sets, and their system-DNS overlaps, are all empty. Step C was not eligible: zero HTTPS/--resolve probes, with TLS/HTTP/redirect/byte results NOT RUN. No broader DNS or origin-path attribution follows from these unauthenticated UDP observations.

| Target server | Type | Returned address | TTL | AA | TC | Elapsed seconds |
|---|---|---|---|---|---|---|
{chr(10).join(rows)}

Authoritative support counts: A 205.186.152.122 has 1; the other three A addresses have 0. AAAA 2a03:2880:f127:283:face:b00c:0:25de and 2a03:2880:f12c:83:face:b00c:0:25de each have 1; the other two AAAA addresses have 0. No address has support from two servers. Five replies carried rd/ra without AA despite nonrecursive requests; their answers were excluded from authoritative support. This inconsistency is preserved without claiming a specific interception mechanism.

Contemporaneous system control `getent ahosts huggingface.co` returned 199.96.59.19 and 2a03:2880:f11c:8083:face:b00c:0:25de, exit 0. Tool preflight `command -v dig; command -v nslookup; dig -v; getent ahosts huggingface.co` found existing /usr/bin/dig and /usr/bin/nslookup. Used /usr/bin/dig version 9.18.39-0ubuntu0.22.04.6-Ubuntu; no installation. A second system control and version observation are captured in the execution receipt.

Each exact command was `/usr/bin/dig @<fixed-ip> huggingface.co <A-or-AAAA> +norecurse +time=5 +tries=1 +ignore`. The +ignore option prevents automatic TCP retry; none was warranted. Complete server-name/IP bindings, command arrays, timestamps, raw replies, RCODE/flags, RRsets/TTLs and timings are in adjudication_receipt.json; original evidence is dns_receipt.json.

Frozen asset: {r['asset']['repository']}, revision {r['asset']['revision']}, file {r['asset']['filename']}; expected {r['asset']['expected_bytes']} bytes and SHA256 {r['asset']['expected_sha256']}. Exact URL: {r['asset']['url']}. Payload acquisition attempts = 0; no payload hashing, checkpoint/partial file, copy or rename.

All prohibited-action counts are 0: alternate checkpoint/model/content host; DNS/network configuration edits; package install/build; checkpoint deserialization; CUDA/model-load/forward; T013/COCO/LVIS scientific work; Grounding rerun; T014/CF/MECH science. P3/P3R1/P3R2 artifacts, Grounding freeze/cache/receipts/decision, YOLO P0/P1/P2 freeze and scientific settings remain unchanged. No background process remains. Changed paths are this separate p3r3 directory and append-only coordination/CODEX_TO_CHATGPT.md / research_log/session_log.md; file hashes are in delivery_manifest.json. Do not repeat the exhausted probes on an unchanged mailbox.

Recommended next action: **{r['next_action']}**.
'''
(OUT/'P3R3_REPORT.md').write_text(report,encoding='utf-8')
with (ROOT/'coordination/CODEX_TO_CHATGPT.md').open('a',encoding='utf-8') as f:
    f.write('\n\n---\n\n'+report+'\nComplete P3R3 receipt:\n```json\n'+json.dumps(r,indent=2)+'\n```\n')
with (ROOT/'research_log/session_log.md').open('a',encoding='utf-8') as f:
    f.write('\n## '+r['stopped_at']+' — P3R3 AUTHORITATIVE_DNS_INCONSISTENT\nLead2cb45ef/task-start2948253. Existing dig executed exactly8 UDP queries; no TC/TCP/retry. All NOERROR but all4 A addresses differ and only1 AA; eligible A/AAAA consensus empty. No Step C, download/hash, install/network edit/GPU/science. Receipts in separate p3r3; wait for Research Lead review of P3R3 authoritative-path evidence before any checkpoint recovery. No unchanged-mailbox repeat.\n')
m={p.name:dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='delivery_manifest.json'}
(OUT/'delivery_manifest.json').write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps(m,indent=2))
