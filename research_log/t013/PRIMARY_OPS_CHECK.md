# T013-OPS1 primary operational audit

**PASS**, metadata snapshot 2026-09-13T02:25:47+08:00. Lead task bc041cb. This is operational evidence only; no prediction arrays, labels, boxes, scores, AP/AR, interactions, CIs or mechanism diagnostics were parsed. No active-run changes, cleanup, compression, relocation, model imports or YOLO runtime occurred.

## Single writer and frozen binding

- Run: `20260912-210355-tovd-native30-primary`.
- Immutable release: `20260912-210306-tovd-native30-primary-freeze`.
- Freeze commit: `6fec32243985ccc808123d851abf5f3dea10af99`.
- Writer PID `721181`, parent `721177`; tmux `autodl-20260912-210355-tovd-native30-primary`, pane PID `721175`, in the writer ancestry. Start/end process snapshots identify the same single cache-target process; no duplicate target was observed. All enumerated process command lines were readable (`proc_entries_unreadable=0`); unrelated commands are not included in the receipt.
- CWD: `/home/wenchang/asdasdsad/wjq/TOVD/releases/20260912-210306-tovd-native30-primary-freeze`.
- Command: `/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python -u -m scripts.t013_native_run --assets /home/wenchang/asdasdsad/wjq/TOVD/shared/t013 --output /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-210355-tovd-native30-primary/artifacts/cache --freeze-commit 6fec32243985ccc808123d851abf5f3dea10af99`.
- The requested venv Python resolves to executable `/home/wenchang/anaconda3/envs/python3.12-tk2-2.3/bin/python3.12`; the recorded command still uses the frozen venv path. No environment mutation was performed.

The process inventory checks exact cache-path arguments, writer module, freeze argument, CWD and tmux ancestry at two snapshots. It is a point-in-time process check, not an ongoing file-lock guarantee.

## Closed-image structure and opaque-byte sample

Terminal completion receipt at audit start/end: **188/1000**, elapsed19282.101294s, no exit receipt; primary tmux alive. The frozen runner prints this receipt only after finishing all15cell writes and manifest appends. The first188 IDs in frozen iteration order form the closed-image set.

All188 closed images have exactly15 expected paths: five conditions `clean/gaussian_noise/motion_blur/fog/jpeg_compression` × `V0/Vhard30/Vrand30`, with filename `{image_id:012d}.npz`. Observed closed paths2820, all observed paths2822, unexpected paths0, missing closed paths0. Only the next frozen image105264 is in flight (2cells at snapshot). No other partial image was observed.

The layout is `cache/raw/<condition>/<vocabulary>/<image_id>.npz`, not one directory per image. Both structural and storage calculations group these15files by the frozen ID; no filenames or conditions are inferred from prediction contents.

Exactly10 sample IDs were selected from the closed set: first3, four positions nearest the median position `(188-1)/2` (ties lower index), and latest3. Zero-based positions: `[0, 1, 2, 92, 93, 94, 95, 185, 186, 187]`. This is independent of outcomes. All150 files were streamed as opaque bytes for SHA256; each matches its recorded `cache_manifest.jsonl` hash and retains its size/mtime across hashing. Full per-file sizes, allocated bytes, mtimes and hashes are in `primary_ops_receipt.json`.

| Sample image ID | Cells hashed | Logical bytes | All hashes match manifest |
|---|---:|---:|---|
| 1425 | 15 | 16261192 | PASS |
| 1490 | 15 | 16310600 | PASS |
| 1584 | 15 | 16352632 | PASS |
| 51712 | 15 | 16319676 | PASS |
| 53909 | 15 | 16230654 | PASS |
| 54123 | 15 | 16307421 | PASS |
| 54593 | 15 | 16251268 | PASS |
| 104455 | 15 | 16289987 | PASS |
| 104619 | 15 | 16292020 | PASS |
| 104782 | 15 | 16246935 | PASS |

Only metadata JSON (frozen inputs/run provenance/cache path-hash records) was parsed. NPZ arrays were never loaded or inspected.

## Provenance

All16 frozen code/provenance file hashes match:10 frozen scripts plus vocabulary, selection,5000-image hash manifest, environment receipt, PLAN and data receipt. The final freeze JSON SHA is `50addfb8e247333b49fb22cda14570166b294101bb435b5a1b5bf688b4b3a91e`; launch-recorded freeze/PLAN hashes also match. Run metadata, resolved-release receipt, run kind, freeze commit, image-ID list, vocabulary SHA, selection SHA, CPU/four-thread setting and recorded initial model-state hash agree.

The recorded initial model-state SHA remains `de1683cc0a3c35157ed5475169dae013cdaffe69f45651d6e3f5550ae96139e1`; frozen native source is `856dde20aee659246248e20734ef9ba5214f5e44`, checkpoint SHA `3b3ca2563c77c69f651d7bd133e97139c186df06231157a64c507099c52bc799`. These are checked provenance bindings. No live model was loaded/hashed; the final `state_after` verification remains pending completion of the original run.

## Disk projection

For each closed image, sum the allocated bytes (`stat.st_blocks ×512`) of its15closed files. This reflects actual file allocation in the transposed layout; no incomplete-image size enters the distribution. The8GiB reserve also leaves room beyond the raw cache. P95 uses linear interpolation at rank`.95×(n−1)`. Remaining count includes the in-flight image in full, conservatively.

| Quantity | Bytes / count |
|---|---:|
| Closed logical bytes total | 3058588504 |
| Closed allocated bytes total | 3064516608 |
| Median allocated bytes / closed image | 16310272 |
| P95 allocated bytes / closed image | 16355328 |
| Remaining images | 812 |
| Projected remaining = P95 × remaining | 13280526336 |
| Current user-available free bytes | 26703241216 |
| Required = ceil(1.20 × projection +8GiB) | 24526566196 |
| Margin above required | 2176675020 |

Fixed safety inequality **PASS**: `26703241216 >= 24526566196`. Margin is about2.027GiB. This passes at the observed filesystem state and does not reserve shared-server capacity. No files were deleted, compressed or moved to achieve it.

## Execution and handoff

Local syntax command: `python -m py_compile research_log/t013/primary_ops_check.py` passed. Remote command: `python3 /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/ops1/primary_ops_check.py > /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/ops1/primary_ops_receipt.json`, exit0. The audit used the system Python standard library and took approximately0.54seconds; no detector environment imports, test reruns, scientific analysis or bootstrap were invoked. Workflow helpers uploaded the standalone helper to shared/t013/ops1 and fetched its JSON to the project-local log. Neither the immutable release nor active run files were written by the audit.

Receipt SHA256: `b1b6120aef9885fea74bdfede2f69ebf6adace8f19a9eb82a373ae4009ab55ca`.
Audit script SHA256: `ccf84a3697c8526c3166482f7b44d7fef2e04485086b91ed966416ac6718a32a`.

All requested operational checks pass. Continue the same primary run and15-minute monitoring. Stop OPS1 after publication and await the next Lead package; no YOLO setup or scientific analysis is authorized by this pass.

End-of-package bookend at2026-09-13T02:28:25+08:00: primary tmux alive,189/1000 images at19394.152425s; free26675806208 bytes. One SSH timeout (exit255) preceded a successful read-only retry. The original0.54s audit snapshot and its JSON remain unchanged.
