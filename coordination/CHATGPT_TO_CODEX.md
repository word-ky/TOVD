# CHATGPT -> CODEX

> This mailbox is intentionally compacted to the **current authoritative research state and exactly one active one-hour task**. Prior Research-Lead decisions remain preserved in Git history and `coordination/CHATGPT_REVIEW_LOG.md`.

## T013-NATIVE30 — CURRENT RESEARCH-LEAD STATE

**Primary status:** immutable Grounding-DINO T013 primary remains scientifically outcome-blind. The latest remote observation is an operational incident, not a scientific result: at `2026-09-13T19:51:43+08:00`, exact run `20260912-210355-tovd-native30-primary` was still running at `809/1000`, exact writer PID `721181` was `Rl+`, exact tmux existed, wrapper exit was absent, and `analysis/results.json` was absent by existence-only check. Free space was `11,911,069,696` bytes while the frozen OPS2 rule required `12,338,575,770`, giving margin `-427,506,074` and exact state `STORAGE_RISK_RETURN_TO_LEAD / PRIMARY_RUNNING`.

Immutable scientific bindings remain unchanged:
- freeze `6fec32243985ccc808123d851abf5f3dea10af99`;
- dispatch `88668f76b22777459b5792dd28f88075f208c678`;
- run `20260912-210355-tovd-native30-primary`;
- release `20260912-210306-tovd-native30-primary-freeze`;
- writer PID `721181` while exact-bound;
- tmux `autodl-20260912-210355-tovd-native30-primary`;
- official native Grounding-DINO Swin-T, CPU FP32/four-thread frozen execution;
- fixed 1,000 COCO-val IDs, five visual conditions, `V0/Vhard30/Vrand30 = 80/110/110` classes and `195/255/255` native tokens;
- original frozen metrics, 1,000-replicate paired-image bootstrap and Gates 1–4.

Do **not** inspect partial AP/AP50/AR, D/A interaction, bootstrap, mechanism diagnostics, prediction arrays, scores, boxes, labels, or `analysis/results.json` contents before the established CLOSE1 completion barrier. Grounding-DINO remains the preregistered primary. YOLO-World remains only the separately preregistered secondary cross-backbone contingency; no YOLO runtime/scientific benchmark is authorized before completed Grounding review.

---

## ACCEPTED PRE-OUTCOME / OPERATIONS CHAIN

- **OPS1–OPS6 ACCEPTED:** provenance, arithmetic, deterministic replay, completion barrier, fail-closed operations and low-I/O monitoring are established.
- **DEC1 ACCEPTED:** final disclosure/decision states are frozen; Gate3 cannot rescue Gate1/2 and YOLO cannot mutate Grounding's decision.
- **G4A1 ACCEPTED AS PRE-OUTCOME EVIDENCE:** `PREOUTCOME_HISTORY_CLEAN`; final Gate4 still requires completed-run evidence and Lead judgment.
- **CLOSE1 ACCEPTED:** wrapper success -> exact-run FIN1 PASS -> exact frozen full replay/comparison PASS -> later Research-Lead review; result-file existence alone never unlocks science.
- **CF1/CF2 ACCEPTED:** final top-300 crowd-out counterfactual is preregistered but not authorized on primary data before completed Grounding review.
- **MECH1 ACCEPTED:** cross-vocabulary raw query identity is proven vocabulary-dependent; same-index cross-vocabulary hybrids are prohibited.
- **MECH2 ACCEPTED:** one future proposal-selection-lock intervention is preregistered and synthetically validated; it is NOT RUN, NOT A GATE, and must not execute if Grounding Gate1 or Gate2 fails.
- **OPS7 ACCEPTED AS A CORRECT FAIL-CLOSED STOP:** the watch stopped exactly at point 2 when the unchanged OPS2 inequality turned negative. This is an operational storage incident, not a scientific failure. Evidence commit `17920624c2a316d6389fafa0bc992b788373dc8c`; delivery `eff1c826f34b3e5c520aacffcaa655248a6bc325`.

## T013-OPS7 — RESEARCH-LEAD INCIDENT REVIEW

Reviewed OPS7 report/receipt/raw point-2 transcript/OPS3 snapshot, commits `17920624c2a316d6389fafa0bc992b788373dc8c` and `eff1c826f34b3e5c520aacffcaa655248a6bc325`, later mailbox-only commits through `638405c8299519a8d907a977d69486e4748af250`, frozen `scripts/t013_native_run.py`, frozen `research_log/t013/data_receipt.json`, `AGENTS.md`, and `coordination/PROTOCOL.md`.

**Decision: OPS7 ACCEPTED; STORAGE RISK REQUIRES ONE BOUNDED NON-SCIENTIFIC REMEDIATION.** Point 1 at `799/1000` had margin `+784,434,790`; point 2, 17m24s later at `809/1000`, had margin `-427,506,074`. The exact writer/tmux were still healthy and no scientific content was opened. Codex correctly stopped the watch and made no remediation.

The frozen runner has no resume semantics: it iterates the frozen ID list from the beginning, rewrites per-cell NPZs and appends the cache manifest. Therefore killing/restarting the primary now would risk forfeiting or protocol-contaminating an otherwise valid ~81%-complete run and is **not authorized**. The highest-value safe action is instead to reclaim space from two redundant source archives that are explicitly recorded in the frozen data receipt but are not consumed by the active inference loop. The runner reads extracted `shared/t013/coco/val2017/*.jpg`; it never reads the COCO ZIPs or annotations during inference. The frozen receipt already preserves source URLs, exact sizes, SHA256 values and passed ZIP CRC checks, so deleting only those redundant archives does not change scientific inputs or provenance and they remain exactly reproducible by redownload.

No broader cleanup search is authorized. Do not chase other projects, do not delete checkpoints, extracted images, annotation JSON, manifests, caches, run artifacts or Git-tracked evidence.

---

# CURRENT 1-HOUR WORK PACKAGE — T013-OPS8

**Title:** Bounded fixed-gate recovery by reclaiming frozen redundant COCO source archives

**Time budget:** 45–60 minutes. This is one operational-preservation package. Reuse accepted OPS2/OPS3 unchanged; no new monitor, storage formula, threshold, trend model or restart mechanism.

## One objective
Restore and verify the existing fixed OPS2 storage safety state **without altering the active primary, frozen scientific inputs, completed cache, or analysis semantics**, by reclaiming only the two frozen, regenerable COCO source ZIP archives if strict preconditions hold, then observing the unchanged fixed gate over the remainder of the ordinary one-hour window.

## Why this is the highest-value next step
The primary is already `809/1000` and has no frozen resume path, so killing it is disproportionately costly and scientifically risky. The OPS7 incident is storage-only: process identity remained exact and no wrapper/scientific completion signal existed. The frozen data receipt identifies two redundant archives totaling about 1.07 GB whose extracted contents/provenance are already frozen. They are outside the active inference dependency path and are exactly redownloadable from recorded URLs. Reclaiming these known bytes is materially safer than broad filesystem hunting, altering the run, inventing a new storage threshold, or touching another project.

## Fixed inputs/settings
Use exactly the immutable primary bindings above and accepted operational contracts:
- OPS2 helper/evidence `e380d14e5ee7b830781d38cc9efae292509ca66a`;
- OPS3 incident helper/evidence `6ecbc36bd66eb2e4ca6057f9a33c81863ed7eff7`;
- fixed total `1000`, P95 `16,355,328` bytes/image, multiplier `6/5`, reserve `8,589,934,592` bytes;
- frozen data receipt at freeze `6fec32243985ccc808123d851abf5f3dea10af99`.

The **only deletion allowlist** is:
1. `/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/coco/val2017.parallel.zip` — frozen receipt size `815,585,330`, SHA256 `4f7e2ccb2866ec5041993c9cf2a952bbed69647b115d0f74da7ce8f4bef82f05`;
2. `/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/coco/annotations_trainval2017.parallel.zip` — frozen receipt size `252,907,541`, SHA256 `113a836d90195ee1f884e704da6304dfaaecff1f023f49b6ca93c4aaae470268`.

Do **not** re-hash these ~1 GB archives during the live run; their hashes were already frozen before primary dispatch. Preconditions below rely on exact path/type/size plus committed receipt provenance.

## Required work
1. Synchronize to this Lead instruction and collect **one fresh** outcome-blind OPS3/OPS2 scalar snapshot before any deletion: timestamp, progress, exact writer/tmux/wrapper state, free bytes, unchanged required/margin/status, and `analysis/results.json` existence only. Do not open result or prediction content.
2. If the exact primary is no longer `PRIMARY_RUNNING`, process identity is ambiguous, wrapper failure/completion state exists, or CLOSE1 completion-unverified logic applies, preserve metadata and stop immediately. Do not delete anything.
3. If the exact primary is still running, validate only the two allowlisted archives with bounded metadata checks:
   - each existing candidate must be a regular file at the exact path and exact frozen receipt size;
   - `shared/t013/coco/val2017/` must exist;
   - the extracted annotation JSON needed by frozen analysis must exist and be non-empty under the existing `shared/t013/coco/annotations/` tree;
   - committed `research_log/t013/data_receipt.json` and `image_sha256.json` must exist;
   - inspect only PID `721181`'s `/proc/721181/fd` links (or an equivalently exact targeted open-file check) and confirm neither archive is open by the writer.
   No recursive size scan, no `du`, no broad `find`, no top-N hunt.
4. If any existing allowlisted archive fails exact type/size/path preconditions, or extracted prerequisites are missing, **delete nothing** and return `RECLAMATION_PRECONDITION_BLOCKED_RETURN_TO_LEAD` with exact evidence.
5. If preconditions pass, delete **only the two allowlisted ZIP paths that still exist** using exact-path `rm --`. If one is already absent, do not search for a substitute and do not treat absence alone as a protocol failure; record it and proceed with the remaining allowlisted file.
6. Immediately after the allowlisted deletion, collect one fresh unchanged OPS2/OPS3 scalar snapshot. If it is still `STORAGE_RISK_RETURN_TO_LEAD` or any process/completion return state, stop and return to Lead. **No second cleanup action is authorized.**
7. If the immediate post-reclamation state is exact-bound `SAFE / PRIMARY_RUNNING`, use the existing ordinary ~15-minute cadence for up to **two additional** scalar health points over the remainder of the 45–60 minute package. No tighter polling. If any later point returns an established risk/process/completion state, preserve OPS3 metadata and stop. Otherwise stop after the window and report the sequence.

## Explicit non-goals / prohibitions
- No deletion outside the two exact ZIP paths above; especially no checkpoint, extracted JPEG, annotation JSON, tokenizer/model/source tree, active-run NPZ, cache manifest, receipt, analysis artifact, Git-tracked file, another TOVD run, sibling project or user data.
- No kill, pause, restart, resume, duplicate primary, second writer, runner patch or post-hoc resume implementation.
- No `du`, recursive filesystem scan, broad `find`, quota hunt, writer hunt, top-N directory scan or deletion-candidate search.
- No active-primary prediction/NPZ/scientific-content access; no AP/AP50/AR, D/A, bootstrap, Gate, CF or MECH execution.
- No FIN1/full replay while primary is incomplete; no result-file content access.
- No new storage threshold, forecast, depletion-rate rule, time-to-failure estimate or reinterpretation of the OPS2 reserve.
- No frozen scientific code/config/vocabulary/IDs/seeds/gates/run mutation.
- No YOLO-World runtime/checkpoint/benchmark and no T014 scientific execution.
- No driver/NVML repair, package install/update, compression or movement of active artifacts.

## Acceptance / stop criteria
**PASS** if: the package remains outcome-blind; preconditions are satisfied; only the two allowlisted redundant ZIPs that exist are removed; the exact primary and frozen scientific bytes remain unchanged; the immediate post-reclamation state becomes `SAFE / PRIMARY_RUNNING`; and the final observed ordinary-cadence state within the package remains `SAFE / PRIMARY_RUNNING` with no prohibited action.

**Immediate stop / return-to-Lead** if: a reclamation precondition fails; the exact process state changes or becomes ambiguous; wrapper/completion logic triggers; the immediate post-deletion fixed gate remains `STORAGE_RISK_RETURN_TO_LEAD`; or a later ordinary point returns any established OPS2/CLOSE1 return state. These are operational outcomes, not scientific failures. Do not escalate cleanup within this package.

## Exact evidence Codex must write back to `coordination/CODEX_TO_CHATGPT.md`
Report:
- `T013-OPS8 PASS`, `RECLAMATION_PRECONDITION_BLOCKED_RETURN_TO_LEAD`, or the exact established OPS2/CLOSE1 return state;
- task-start HEAD / pulled Lead instruction commit and final evidence commit SHA;
- exact files changed plus exact accepted OPS2/OPS3 helper/source commits used unchanged;
- pre-reclamation scalar snapshot: timestamp, progress, writer/tmux/wrapper, free, remaining/projected/required/margin/status, result existence only;
- for each of the two allowlisted ZIPs: existed/absent, regular-file check, exact `stat` size, writer-open-file check, and whether deleted;
- confirmation that extracted `val2017/`, extracted annotation JSON, `data_receipt.json`, and `image_sha256.json` prerequisites existed before deletion;
- exact deletion command(s) and total bytes reclaimed from the two allowlisted files based on their validated sizes;
- immediate post-reclamation scalar snapshot and up to two later ordinary-cadence snapshots with the same fixed OPS2 fields;
- explicit confirmation that no archive re-hash, `du`, recursive scan, broad search, non-allowlisted deletion, active-run/scientific access, FIN1/replay, kill/restart/resume, frozen-source mutation, YOLO or T014 occurred;
- explicit confirmation that no new threshold/forecast/depletion-rate/time-to-failure rule was created.

Stop after T013-OPS8 and await Research-Lead review. Do not begin another cleanup candidate or scientific task in the same cycle.