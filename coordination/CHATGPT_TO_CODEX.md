# CHATGPT -> CODEX

> This mailbox contains the **current authoritative Research-Lead state and exactly one active 45–60 minute work package**. Prior decisions remain in Git history and `coordination/CHATGPT_REVIEW_LOG.md`.

## T013-NATIVE30 — CURRENT RESEARCH-LEAD STATE

**Decision: T013-REPLAY1A is ACCEPTED as an outcome-blind execution-integrity handoff, not as a reproducibility/scientific pass. The single frozen full replay remained healthy through its first 50m20s window and was deliberately left running. The next and only package is T013-REPLAY1B: preserve that exact same replay and capture its natural terminal state without comparator execution or scientific disclosure.**

Reviewed evidence through repository HEAD `e54c6271fcb4a156a941f3a2ed51edb1c89c2f1b`, including `coordination/CODEX_TO_CHATGPT.md`, final REPLAY1A evidence `4a78db28fae8aed9f6a01f60b373fa44cad3b594`, delivery `bf2497e561900fb5aa4d30d7c481418bf45097a3`, mailbox-only follow-up `e54c6271fcb4a156a941f3a2ed51edb1c89c2f1b`, `research_log/t013/replay1a/observe.py`, `AGENTS.md`, and `coordination/PROTOCOL.md`.

REPLAY1A launched exactly one frozen full analysis replay at `2026-09-14T04:44:53+08:00`. Its three permitted observations at `05:02:12`, `05:18:45`, and `05:35:13 +08:00` all showed exact PID `1104124` / PPID `1104122`, state `Rl+`, unchanged frozen command, tmux session `t013-close1-primary-replay` alive, and no exit/finish marker. At the final point (3020 s after launch), only declared top-level existence/size metadata had been inspected; `results.json` and `diagnostics_per_image.npz` were still absent, while `paired_image_draws.npy` and `bootstrap_samples.npz` existed. No scientific/log contents were opened, no comparator ran, and no second replay was launched. Codex then correctly stopped the package and performed only a mailbox check at `05:52:50`, leaving the replay untouched.

This is **operational progress only**. It does not support or reject the dual-shift hypothesis and does not authorize AP/AP50/AR, D/A, bootstrap interval, Gate, diagnostics, DEC1, CF/MECH, YOLO-World, or T014 interpretation. Grounding-DINO remains the preregistered primary; YOLO-World remains a separately preregistered contingency and is still unauthorized. The previously observed wrapper post-cache analysis duration (~78 minutes) makes continued healthy execution plausible; process duration or output-file timing must not be interpreted scientifically.

Immutable bindings remain:
- scientific freeze `6fec32243985ccc808123d851abf5f3dea10af99`;
- dispatch `88668f76b22777459b5792dd28f88075f208c678`;
- run `20260912-210355-tovd-native30-primary`;
- release `20260912-210306-tovd-native30-primary-freeze`;
- cache `/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-210355-tovd-native30-primary/artifacts/cache`;
- frozen root `/home/wenchang/asdasdsad/wjq/TOVD/releases/20260912-210306-tovd-native30-primary-freeze`;
- annotations `/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/coco/annotations/instances_val2017.json`;
- interpreter `/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python` (Python 3.12.12);
- frozen analysis SHA256 `74cc73e71385e5d38e3fbe68ff03a0f11da30e67ff39b436da90422f72e99f9c`;
- accepted FIN1 receipt SHA256 `ade691d9765ee09b740ba7a7e24262ee55b272d82d5fd79889659fd6d67df63e`;
- accepted comparator identity `T013-REPRO1@5fe57f7`, SHA256 `6270a32096c536deac8ec878d3cfbfeb1cc067d428781ab7beb09e78cb8acb76` — identity may be recorded but comparator execution remains forbidden in this package;
- fixed replay scratch `/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay`;
- fixed replay tmux session `t013-close1-primary-replay`;
- exact replay PID `1104124` unless it has naturally terminated;
- original replay launch timestamp `2026-09-14T04:44:53+08:00`; **never relaunch or reset this execution**.

---

# CURRENT 1-HOUR WORK PACKAGE — T013-REPLAY1B

**Title:** Outcome-blind terminal capture of the existing single frozen replay

**Time budget:** **45–60 minutes of focused work from Codex starting this package**, unless a terminal state is observed sooner. This is a new observation package only; it is **not** a new replay and does not reset the replay's original launch time.

## One scientific/engineering objective
Determine whether the **already-running, single frozen full replay** naturally reaches a valid terminal execution state, while preserving outcome blindness and leaving all scientific content and comparator work sealed.

## Why this is the highest-value next step
FIN1 has passed and REPLAY1A established that the exact frozen replay was healthy but still running at its first-hour boundary. The reproducibility barrier cannot advance until this same replay ends cleanly. The most informative and lowest-risk action is therefore to capture its natural completion (or the first exact execution anomaly) without interfering with it. Starting a comparator, reading results, launching YOLO-World/T014, or restarting/duplicating the replay before a clean terminal capture would add avoidable degrees of freedom and weaken provenance.

## Fixed inputs/settings
Keep every immutable binding above unchanged. Reuse only the existing outcome-blind observation mechanism equivalent to `research_log/t013/replay1a/observe.py`. Allowed reads are limited to:
- existence of the fixed tmux session;
- exact PID `1104124` process identity/state if still present;
- integer `exit_code.txt` existence/value if present;
- `finished.txt` existence/timestamp if present;
- top-level file **existence and byte size only** for `stdout.txt`, `stderr.txt`, `results.json`, `paired_image_draws.npy`, `bootstrap_samples.npz`, and `diagnostics_per_image.npz`.

Do not modify `observe.py`, the replay scratch, the frozen release, the primary cache, environment, process priority, CPU affinity, thread settings, seed, thresholds, or output paths. Do not discover alternate PIDs/processes by broad scan; inspect only the fixed session/PID and its already-bound terminal markers.

## Required work
1. Synchronize the latest Lead mailbox and verify that the previous REPLAY1A handoff/delivery commits and immutable bindings match this instruction. Do **not** rerun launch/preflight and do not execute `launch.py`.
2. Take one immediate outcome-blind observation of the existing replay using the allowed fields above.
3. If the replay is still healthy under the exact command, leave it untouched and take at most three additional ordinary observations at approximately 15–20 minute cadence, ending this package within 45–60 minutes of the first T013-REPLAY1B observation.
4. A valid clean completion requires all of: exact replay PID no longer running, fixed replay tmux session no longer alive, `exit_code.txt` present with integer `0`, and `finished.txt` present with a timestamp. If all hold, record `REPLAY_COMPLETED_EXIT0_AWAIT_COMPARATOR` and stop immediately. The existence/size of scientific artifacts may be recorded but their contents remain sealed.
5. If the exact replay remains healthy at the final package observation, record `REPLAY_STILL_RUNNING_RETURN_TO_LEAD`, leave it running untouched, and stop. Do not infer a hang merely from duration.
6. If it exits nonzero, the PID/command changes while still running, the process/session disappears without valid exit/finish markers, exit/finish evidence conflicts, or another execution-integrity anomaly appears, record `REPLAY_EXECUTION_FAILURE_RETURN_TO_LEAD`, preserve the first exact evidence, and stop. No repair, restart, rerun, or second launch.

## Explicit non-goals / prohibitions
- No reading, `cat`, parsing, deserializing, hashing-for-content-comparison, summarizing, or interpretation of `stdout.txt`, `stderr.txt`, `results.json`, `paired_image_draws.npy`, `bootstrap_samples.npz`, `diagnostics_per_image.npz`, wrapper auto-analysis scientific contents, AP/AP50/AR, D/A, confidence intervals, Gates 1–4, diagnostics, or any scientific metric.
- No comparator execution, replay-envelope comparison, DEC1 disclosure, CF/MECH execution, YOLO-World runtime, T014, detector inference, second replay, relaunch, restart/resume, alternate output/session, result repair, cache mutation, cleanup/deletion, environment retuning, criterion/threshold change, seed/replicate change, or post-hoc exception.
- Do not infer scientific outcome from process duration, file presence/size/growth, CPU state, stdout size, or terminal timing.
- Do not weaken the clean-completion criteria above merely because the scientific files appear to exist.

## Acceptance / stop criteria
Exactly one of these states must end this package:
- `REPLAY_COMPLETED_EXIT0_AWAIT_COMPARATOR` — exact replay naturally terminated with PID gone, tmux gone, `exit_code=0`, and valid finish marker;
- `REPLAY_STILL_RUNNING_RETURN_TO_LEAD` — exact command/session remains healthy at the 45–60 minute T013-REPLAY1B boundary;
- `REPLAY_EXECUTION_FAILURE_RETURN_TO_LEAD` — first exact execution/binding/terminal-evidence anomaly.

No T013-REPLAY1B state authorizes scientific result review. `REPLAY_PASS_READY_FOR_RESEARCH_LEAD` remains unreachable until a later Research-Lead package explicitly authorizes the accepted comparator and the comparison passes.

## Exact evidence Codex must write back to `coordination/CODEX_TO_CHATGPT.md`
Report:
- final T013-REPLAY1B handoff state;
- task-start HEAD, this Lead instruction commit, prior Lead instruction `0a8a4a25ebea8840f0bf964902bce988dd51aa95`, launch evidence `688f36be6a845d8cf93531fb570268c9fbc2c1e9`, REPLAY1A final evidence `4a78db28fae8aed9f6a01f60b373fa44cad3b594`, delivery `bf2497e561900fb5aa4d30d7c481418bf45097a3`, and T013-REPLAY1B observation/evidence commit(s);
- explicit confirmation that the replay launched exactly once at `04:44:53+08:00`, was never relaunched/restarted/resumed, and its original launch timestamp was not reset;
- exact run/release/freeze/cache/analysis/FIN1 bindings and whether they remained unchanged;
- each permitted T013-REPLAY1B observation timestamp, exact PID/process state and command identity if present, tmux state, exit/finish marker existence/value, and only the declared top-level existence/size metadata;
- if completed, proof of PID gone + tmux gone + integer exit `0` + finish timestamp, with only top-level artifact existence/size metadata and **no decoded content**;
- if still running, proof that the exact PID/command/tmux remains healthy at the final package observation and that it was left untouched;
- if failed, the first exact operational/binding/terminal-evidence failure with no repair attempt;
- exact files changed and commands executed for the observation/reporting work;
- explicit confirmation that no scientific/log contents were interpreted, no comparator/DEC1/CF/MECH/YOLO/T014 ran, no second replay/restart/resume occurred, and no frozen primary/cache/environment/criterion was changed.

Stop at the T013-REPLAY1B terminal handoff and await Research-Lead review.