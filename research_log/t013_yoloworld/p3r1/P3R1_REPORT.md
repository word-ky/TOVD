# T013-YW-P3R1 — checkpoint transport remains blocked

State: **YW_P3R1_CHECKPOINT_TRANSPORT_BLOCKED_RETURN_TO_LEAD**.
Task-start HEAD: `1fe8a00f7bb6396db5549505efad3003731301c1`.
Lead instruction: `bd8d7980b1b7d823ee266d341c1daee637d3c704`.
Recovery execution: 2026-09-14T14:09:57.749621+08:00 through 2026-09-14T14:10:43.247888+08:00. Driver exited 1 after both allowed attempts were exhausted.

The fixed checkpoint path did not exist before or after recovery:
`/home/wenchang/asdasdsad/wjq/TOVD/shared/t013_yoloworld/weights/s_stage2-4466ab94.pth`.
Final byte count, SHA256 and independent second verification are unavailable, not PASS. No copy or atomic rename occurred.

The exact asset remains `wondervictor/YOLO-World-V2.1`, immutable revision `c620164ee3979bf49b895c8a8e0f49aeaca89209`, file `s_stage2-4466ab94.pth`, expected 305058902 bytes and SHA256 `4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458`.
Both attempts used only `https://huggingface.co/wondervictor/YOLO-World-V2.1/resolve/c620164ee3979bf49b895c8a8e0f49aeaca89209/s_stage2-4466ab94.pth`.

Read-only search roots:

- `/home/wenchang/asdasdsad/wjq/TOVD/shared/t013_yoloworld`
- `/home/liujianhua/.cache/huggingface/hub`

The second root was the accessible result of `/home/*/.cache/huggingface/hub/` enumeration. Standard-library `os.walk(..., followlinks=False)` searched filename equal to the fixed name OR size equal to 305058902. Candidate count 0; hashed candidate count 0. No model file was deserialized. The deployed exact search and transfer implementation is `recover_checkpoint.py`; invocation was `/usr/bin/python3.10 /home/wenchang/asdasdsad/wjq/TOVD/research_log/t013_yoloworld/p3r1/recover_checkpoint.py`.

| Attempt | Start (+08:00) | Stop (+08:00) | Exit | Received bytes | Resumed | HTTP / redirects |
|---|---|---|---|---|---|---|
| 1 | 14:09:57.794688 | 14:10:20.527588 | 28 | 0 | false | 0 / 0 |
| 2 | 14:10:20.528517 | 14:10:43.246200 | 28 | 0 | false | 0 / 0 |

Both commands used `curl -fL --silent --show-error --connect-timeout 45 --max-time 900 --output <fixed-weights-path>/s_stage2-4466ab94.pth.p3r1.partial --write-out '%{json}' <exact-official-URL>`. Complete argument arrays and transport fields are in `recovery_receipt.json`.

First exact blocker:
```
curl: (28) Failed to connect to huggingface.co port 443 after 22703 ms: 连接超时
```
Second failure was the same connection timeout after 22701 ms. Both DNS observations returned `66.220.149.18` and `2a03:2880:f10d:183:face:b00c:0:25de`. Neither established a connection or reached an HTTP response/redirect; this is a connection failure, not a content mismatch. No broader DNS investigation, network configuration change or alternate content source was attempted.

Counts: alternate checkpoint/model 0; alternate host/mirror 0; package install/build 0; checkpoint deserialization 0; CUDA ops 0; model load 0; forward 0; T013/COCO/LVIS scientific actions 0. No Grounding rerun, T014, CF/MECH scientific work or YOLO benchmark ran. Original P3 blocker artifacts, Grounding freeze/cache/receipts/decision, YOLO protocol freeze and scientific settings remain unchanged. Only this separate p3r1 directory and append-only coordination/session reporting were created/changed.

This package establishes no runtime or scientific conclusion. No background recovery task remains. Do not repeat these two attempts on an unchanged mailbox.

Recommended next action: **Research Lead checkpoint-transport blocker review**.
