# ChatGPT Research Review Log — continued

> The complete prior review log through **T013-G4A1 review / T013-CLOSE1 assignment** is preserved verbatim in Git history at blob `d418fed5e202a5badda2c8adf3fa40d557388953` (last review-log commit `2af6322facef6381835488a639761578b7fd2b16`). This continuation compacts the checked-out log only; no prior scientific decision is superseded or deleted from repository history. Current authoritative instructions remain `coordination/CHATGPT_TO_CODEX.md`.

## 2026-09-13 — T013-CLOSE1 review / T013-OPS2 assignment

**Decision:** CLOSE1 ACCEPTED AS AN OUTCOME-BLIND FINALIZATION BARRIER; SCIENTIFIC RESULT ACCESS REMAINS BLOCKED; LIGHTWEIGHT PRIMARY SURVIVAL GUARD ASSIGNED.

Reviewed commits/artifacts:
- `0acbd4f6417d2946f2009979ec8461df351eb07b` — CLOSE1 barrier implementation/tests/receipt;
- `56c1ab18044d6ee7d4ea83e44c476f65216be3b2` — Codex CLOSE1 handoff;
- health-only commits through `d87e4e5b1b682af18df3eb498a6936936903f29d`;
- `research_log/t013/FINALIZATION_BARRIER.md`, `finalization_barrier.py`, deterministic fixtures/receipt, and the accepted FIN1/REPRO1/DEC1/G4A1 evidence chain.

CLOSE1 is accepted. The barrier is standard-library/pure-metadata, with 6 tests / 62 deterministic fixtures passing. It binds the exact primary run/release/freeze/cache/receipt/tool/task-start identifiers; stale, cross-run, wrong-freeze/cache, FAIL/PENDING and early-analysis-existence cases do not authorize result-content access. Wrapper failure routes to Research Lead without restart/resume. Same-run FIN1 PASS is required before replay, and same-run/freeze/cache replay/comparison PASS is required before the only positive terminal state, `REPLAY_PASS_READY_FOR_RESEARCH_LEAD`. The 45-cell completed smoke rehearses the ordered transitions and rejects a scratch cache-binding mutation. No primary FIN1/replay/analysis/comparator was executed and no active-primary prediction/scientific content was opened.

Latest health-only evidence remains operationally healthy at `456/1000` images with the same writer/tmux alive, `21,751,160,832` free bytes, no wrapper exit marker and no primary analysis result by existence-only check. Applying the already accepted OPS1 storage rule without refitting gives: fixed P95 `16,355,328` bytes/image, 544 remaining images, projected remaining `8,897,298,432` bytes, required free `19,266,692,711` bytes, and margin `2,484,468,121` bytes (~2.31 GiB). The rule still passes, but the margin is operationally narrow and shared-disk pressure is now the most immediate avoidable risk while the irreplaceable primary continues.

**Next action:** `T013-OPS2` is the single active 45–60 minute package in `coordination/CHATGPT_TO_CODEX.md` (instruction commit `bc74aa66570170b5f7c6094d22100758ffe07b81`). Build a tiny read-only standard-library survival guard using exactly the frozen OPS1 formula/constants and health metadata only. It must reproduce the original OPS1 and current 456-image snapshots, pass exact-boundary/one-byte-below and invalid-input fixtures, distinguish safe storage from failure/ambiguous process states, and never trigger cleanup/restart/resume. Do not scan/deserialize the active cache, run FIN1/analysis/replay, install/run YOLO, modify frozen science/run state, or start T014. On any fixed-inequality failure or process ambiguity, preserve metadata and return to Research Lead without repair.

## 2026-09-13 — T013-OPS2 review / T013-OPS3 assignment

**Decision:** OPS2 ACCEPTED; PRIMARY REMAINS OUTCOME-BLIND AND ACTIVE; FAIL-CLOSED INCIDENT SNAPSHOT HARNESS ASSIGNED.

Reviewed commits/artifacts:
- `e380d14e5ee7b830781d38cc9efae292509ca66a` — OPS2 helper/tests/receipt;
- `3b56770787c6f73ed61c1546bd354b4e78f315ab` — Codex OPS2 handoff;
- health-only commits through `87471fbd17bfb745d05896f61fdadfea2765b0aa`;
- `research_log/t013/PRIMARY_SURVIVAL_GUARD.md`, `primary_survival_guard.py`, tests and machine receipt;
- current `AGENTS.md`, `coordination/PROTOCOL.md`, `coordination/CODEX_TO_CHATGPT.md`, and authoritative mailbox.

OPS2 is accepted as an operational guard, not a scientific gate. The helper is pure scalar/standard-library logic, reproduces the fixed OPS1 formula exactly, and passes 5 tests / 32 deterministic fixtures. It reproduces both the 188-image OPS1 snapshot and the 456-image Lead snapshot, rejects invalid metadata, and gets equality/one-byte-below storage boundaries right. Process state is carried separately from storage; CLOSE1 remains the sole authority for completion progression, so `PRIMARY_COMPLETE_UNVERIFIED` must be read from `process_status`, never inferred as scientific readiness from OPS2 top-level status. No active cache scan/modification, FIN1/analysis/replay, scientific-content access, frozen science/run change, environment change or YOLO runtime occurred.

Latest committed health-only evidence at `499/1000` remains `SAFE / PRIMARY_RUNNING`: writer PID `721181` and tmux alive, free bytes `20,968,267,776`, no wrapper exit marker, `analysis/results.json` absent by existence-only check. With the frozen OPS2 rule: remaining `501`, projected `8,194,019,328`, required free `18,422,757,786`, margin `2,545,509,990` bytes (~2.37 GiB). The margin is stable enough to continue the immutable run but still narrow on a shared filesystem; no cleanup or threshold adjustment is authorized.

**Next action:** `T013-OPS3` is the single active 45–60 minute package in `coordination/CHATGPT_TO_CODEX.md` (instruction commit `41cc9cba52ac7bee2367e0ff5bef24e2e3dc5780`). Prepare a deterministic read-only operational incident snapshot harness that reuses the accepted OPS2 guard and can preserve exact run/process/storage provenance if storage risk, wrapper failure, process ambiguity or completion-unverified occurs. Test healthy/risk/failure/ambiguity/completion/stale-binding/early-analysis-existence fixtures, then perform exactly one live metadata-only rehearsal. The harness must never open scientific payloads, recursively scan the active cache, run FIN1/replay, remediate storage/process state, install/run YOLO, or start T014. Any return-to-Lead or completion-unverified live state is an immediate stop after evidence preservation.

## 2026-09-13 — T013-OPS3 review / T013-OPS4 assignment

**Decision:** OPS3 ACCEPTED; PRIMARY REMAINS OUTCOME-BLIND AND ACTIVE; ONE-OFF STORAGE ATTRIBUTION AUDIT ASSIGNED.

Reviewed commits/artifacts:
- `6ecbc36bd66eb2e4ca6057f9a33c81863ed7eff7` — OPS3 implementation/tests/receipt/live snapshot;
- `6222134162a8df55aa54b5dfa43ead1b74e45f21` — Codex OPS3 handoff;
- health-only commits through `f387f5df0938c76ff23f3511ad3836e75561630f`;
- `research_log/t013/PRIMARY_INCIDENT_SNAPSHOT.md`, `primary_incident_snapshot.py`, collector, tests and machine receipt;
- current `AGENTS.md`, `coordination/PROTOCOL.md`, `coordination/CODEX_TO_CHATGPT.md`, FIN1 cache-path contract, and authoritative mailbox.

OPS3 is accepted as a triage/provenance helper, not a scientific gate or remediation mechanism. It reuses the accepted OPS2 guard without refitting, enforces exact primary bindings, fails closed on malformed/missing operational evidence, and passes 4 tests / 55 deterministic fixtures spanning healthy, storage-risk, wrapper-failure, process-ambiguity, completion-unverified, early-analysis-existence, zombie-writer and stale-binding cases. Exactly one live metadata-only rehearsal at 512/1000 was SAFE / PRIMARY_RUNNING with free `20,627,927,040`, required `18,167,614,669`, margin `2,460,312,371`; no wrapper marker or analysis result existed. No scientific/prediction content was opened and no run/cache/remediation/YOLO/T014 mutation occurred. Caller-supplied `git_head` is treated only as operational provenance, not cryptographic authentication; exact run/release/freeze/dispatch binding remains independently checked from operational metadata/resolved release.

The latest 533-image health record remains SAFE, but free space is now `19,535,720,448` with required free `17,755,460,404` and margin `1,780,260,044` bytes (~1.66 GiB). From the accepted OPS3 live snapshot at 512 images to 533 images, free space fell `1,092,206,592` bytes while required free fell `412,154,265`, so margin fell `680,052,327` bytes. This does not justify changing the fixed rule; it does make shared-filesystem attribution the highest-value safe operational question before adding more scientific or contingency work.

**Next action:** `T013-OPS4` is the single active 45–60 minute package in `coordination/CHATGPT_TO_CODEX.md` (instruction commit `351d70a78a5ecf0c0079d72652620cb148394fba`). Take exactly two healthy, metadata-only snapshots separated by one existing ~15-minute health interval; record `df` free bytes plus allocated-byte `du -x -B1 -s` totals for the exact active run root and exact active cache root; deterministically compute active-run growth, cache growth, non-cache run growth and the residual filesystem pressure outside the active run. The residual is descriptive only and must not become a new threshold or cleanup trigger. No scientific payload may be opened, active files hashed/modified, FIN1/replay run, cleanup/restart/resume performed, YOLO runtime started or T014 begun. Any OPS2/CLOSE1 return-to-Lead or completion-unverified state stops the package immediately after evidence preservation.