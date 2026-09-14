# T013-YW-P3R2 — resolver/path attribution remains ambiguous

State: **YW_P3R2_AMBIGUOUS_RETURN_TO_LEAD**.
Task-start HEAD: `144e6f45c766a5783838d282e21193ca34c23065`. Lead instruction: `767d41e326439ee5c4b668af8e792cc45d768bdb`.
Probe interval: 2026-09-14T15:34:38.856861+08:00 through 2026-09-14T15:35:33.482938+08:00. Metadata driver exit 0; individual failures retained below.

PyPI returned HTTP 200 with verified TLS (151.101.192.223, 0.245516 s). GitHub connected and completed TLS (20.205.243.166, TLS time 0.463352 s, verification result 0), then timed out after 30.001642 s without HTTP response (curl 28). Thus these controls do not establish a universal outbound block.

Google DoH A/AAAA both failed before connection with curl 28, after 11355/11352 ms. Cloudflare DoH A/AAAA both failed with curl 35: `OpenSSL SSL_connect: 连接被对方重置 in connection to cloudflare-dns.com:443`. All four returned no DNS JSON, addresses, TTL or status. Agreement with each other or system DNS is unavailable. No independently obtained address exists for Step C: same-origin --resolve probes = 0. No additional client/resolver or retry was improvised.

System `getent ahosts huggingface.co` succeeded and returned IPv4 199.59.149.231 and IPv6 2a03:2880:f134:183:face:b00c:0:25de. These differ from the P3R1 observations, but variation alone does not establish resolver causation. `/etc/resolv.conf` uses nameserver 127.0.0.53, options edns0 trust-ad, search dot; full content retained in the receipt, SHA256 ebdf560272a77357195c39e98340b77e18c8a8ce2025ee950e9e0c7b01467ab8.

HTTP_PROXY, HTTPS_PROXY, ALL_PROXY, http_proxy, https_proxy, all_proxy, NO_PROXY and no_proxy are all unset; no proxy values were read or printed. Existing curl 7.81.0 / OpenSSL 3.0.2 advertises HTTPS, HTTP2 and SSL, with --doh-url and --resolve exposed in help. No curl replacement or certificate bypass occurred.

Frozen asset: wondervictor/YOLO-World-V2.1, revision c620164ee3979bf49b895c8a8e0f49aeaca89209, file s_stage2-4466ab94.pth; expected 305058902 bytes, SHA256 4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458. Exact URL: https://huggingface.co/wondervictor/YOLO-World-V2.1/resolve/c620164ee3979bf49b895c8a8e0f49aeaca89209/s_stage2-4466ab94.pth. No request to this URL occurred in P3R2; no payload acquired, partial created, checkpoint hash reverified or model deserialized.

All prohibited-action counts are 0: checkpoint/partial creation, payload-download attempt, alternate checkpoint/model or content host/mirror, network/DNS configuration change, package install/build, checkpoint deserialization, CUDA/model-load/forward, T013/COCO/LVIS science, Grounding rerun, T014/CF/MECH scientific work. P3/P3R1, Grounding and YOLO freezes/settings remain unchanged. No background job remains.

Exact command arrays, timestamped results, resolver content, curl features, DNS failures, TLS/HTTP/IP/timing fields and empty same-origin probe list are in adjudication_receipt.json (raw A/B evidence: network_receipt.json). Changed paths: this separate p3r2 directory, plus append-only coordination/CODEX_TO_CHATGPT.md and research_log/session_log.md. File hashes are in delivery_manifest.json. These are network observations only, not runtime or scientific evidence. Do not repeat the package on an unchanged mailbox.

Recommended next action: **Research Lead review of resolver/path evidence before any checkpoint recovery**.
