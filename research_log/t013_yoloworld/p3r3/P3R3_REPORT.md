# T013-YW-P3R3 — direct DNS replies fail consensus

State: **YW_P3R3_AUTHORITATIVE_DNS_INCONSISTENT_RETURN_TO_LEAD**.
Task-start HEAD: `29482534e26c34f379da0f1cca6578d94d09670f`. Lead instruction: `2cb45efcdc4797506b734337d7bdfac3557a3544`.
Probe interval: 2026-09-14T15:54:54.625538+08:00 to 2026-09-14T15:54:54.921331+08:00; driver exit 0.

Exactly eight UDP nonrecursive queries to the four fixed server IPs completed, all exit 0 / RCODE NOERROR. All TC flags were false: no TCP retry. Replies existed, so this is not the DNS-unreachable state. All four A answers differed; only the first A reply had AA set. No A address met the fixed >=2 authoritative-server rule. Eligible A and AAAA sets, and their system-DNS overlaps, are all empty. Step C was not eligible: zero HTTPS/--resolve probes, with TLS/HTTP/redirect/byte results NOT RUN. No broader DNS or origin-path attribution follows from these unauthenticated UDP observations.

| Target server | Type | Returned address | TTL | AA | TC | Elapsed seconds |
|---|---|---|---|---|---|---|
| 205.251.192.137 | A | 205.186.152.122 | 150 | True | False | 0.032899613957852125 |
| 205.251.192.137 | AAAA | 2001::68f4:2be4 | 68 | False | False | 0.040117199008818716 |
| 205.251.197.172 | A | 199.16.158.104 | 71 | False | False | 0.03130168200004846 |
| 205.251.197.172 | AAAA | 2a03:2880:f127:283:face:b00c:0:25de | 207 | True | False | 0.03133694198913872 |
| 205.251.199.163 | A | 199.59.148.15 | 128 | False | False | 0.03636962897144258 |
| 205.251.199.163 | AAAA | 2a03:2880:f12c:83:face:b00c:0:25de | 212 | True | False | 0.03975460695801303 |
| 205.251.195.151 | A | 162.125.83.1 | 133 | False | False | 0.0338005960220471 |
| 205.251.195.151 | AAAA | 2001::9df0:23 | 211 | False | False | 0.03515492199221626 |

Authoritative support counts: A 205.186.152.122 has 1; the other three A addresses have 0. AAAA 2a03:2880:f127:283:face:b00c:0:25de and 2a03:2880:f12c:83:face:b00c:0:25de each have 1; the other two AAAA addresses have 0. No address has support from two servers. Five replies carried rd/ra without AA despite nonrecursive requests; their answers were excluded from authoritative support. This inconsistency is preserved without claiming a specific interception mechanism.

Contemporaneous system control `getent ahosts huggingface.co` returned 199.96.59.19 and 2a03:2880:f11c:8083:face:b00c:0:25de, exit 0. Tool preflight `command -v dig; command -v nslookup; dig -v; getent ahosts huggingface.co` found existing /usr/bin/dig and /usr/bin/nslookup. Used /usr/bin/dig version 9.18.39-0ubuntu0.22.04.6-Ubuntu; no installation. A second system control and version observation are captured in the execution receipt.

Each exact command was `/usr/bin/dig @<fixed-ip> huggingface.co <A-or-AAAA> +norecurse +time=5 +tries=1 +ignore`. The +ignore option prevents automatic TCP retry; none was warranted. Complete server-name/IP bindings, command arrays, timestamps, raw replies, RCODE/flags, RRsets/TTLs and timings are in adjudication_receipt.json; original evidence is dns_receipt.json.

Frozen asset: wondervictor/YOLO-World-V2.1, revision c620164ee3979bf49b895c8a8e0f49aeaca89209, file s_stage2-4466ab94.pth; expected 305058902 bytes and SHA256 4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458. Exact URL: https://huggingface.co/wondervictor/YOLO-World-V2.1/resolve/c620164ee3979bf49b895c8a8e0f49aeaca89209/s_stage2-4466ab94.pth. Payload acquisition attempts = 0; no payload hashing, checkpoint/partial file, copy or rename.

All prohibited-action counts are 0: alternate checkpoint/model/content host; DNS/network configuration edits; package install/build; checkpoint deserialization; CUDA/model-load/forward; T013/COCO/LVIS scientific work; Grounding rerun; T014/CF/MECH science. P3/P3R1/P3R2 artifacts, Grounding freeze/cache/receipts/decision, YOLO P0/P1/P2 freeze and scientific settings remain unchanged. No background process remains. Changed paths are this separate p3r3 directory and append-only coordination/CODEX_TO_CHATGPT.md / research_log/session_log.md; file hashes are in delivery_manifest.json. Do not repeat the exhausted probes on an unchanged mailbox.

Recommended next action: **Research Lead review of P3R3 authoritative-path evidence before any checkpoint recovery**.
