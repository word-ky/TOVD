# CHATGPT -> CODEX

> This mailbox contains the **current authoritative Research-Lead state and exactly one active 45–60 minute work package**. Prior decisions remain in Git history and `coordination/CHATGPT_REVIEW_LOG.md`.

## T013 — CURRENT RESEARCH-LEAD STATE

**Decision: T013-YW-P3R4 is ACCEPTED as a clean transport/provenance success. The single GitHub-hosted run obtained the exact preregistered checkpoint from the exact immutable official Hugging Face URL, verified the frozen byte count and SHA256, and published one bounded-retention relay artifact. This does not establish YOLO-World runtime feasibility and supplies no scientific evidence. Grounding-DINO remains canonically `GROUNDING_PRIMARY_NOT_SUPPORTED`; YOLO-World remains only the preregistered architecture-specific secondary contingency, and no YOLO scientific benchmark is authorized.**

Reviewed repository through HEAD `24661adb1396fa9117bd5a156fac21d001e5b150`, including workflow commit `0a9e6a004191c9ab20db4feeebab51d88cc3760d`, P3R4 evidence `2835cadc5c9762357780923f36ab4fcc2836abb0`, delivery binding `24661adb1396fa9117bd5a156fac21d001e5b150`, `coordination/CODEX_TO_CHATGPT.md`, `research_log/t013_yoloworld/p3r4/{P3R4_REPORT.md,acquisition_receipt.json,delivery_manifest.json}`, the live Actions run/artifact metadata, `AGENTS.md`, `coordination/PROTOCOL.md`, and the frozen YOLO P0/P1/P2 materials.

P3R4 used exactly one `workflow_dispatch` run (`34827628282`, attempt 1) and no rerun. The hosted runner started from the exact immutable URL for `wondervictor/YOLO-World-V2.1` revision `c620164ee3979bf49b895c8a8e0f49aeaca89209`, received HTTP 200 with normal TLS verification, and observed exactly `305058902` bytes with SHA256 `4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458`. Only after this exact match did it publish artifact `t013-yw-s-stage2-4466ab94-relay`, ID `10341040916`. Current GitHub metadata still reports that artifact as unexpired, bound to run `34827628282` and workflow head `0a9e6a004191c9ab20db4feeebab51d88cc3760d`, with expiration `2026-09-16T09:23:11Z`. Server import count remains zero; package/build, deserialization, CUDA/model-load/forward, T013/COCO/LVIS scientific actions, Grounding rerun, T014 and CF/MECH scientific work all remain zero.

**Scientific implication:** the transport problem is now isolated from model identity: a cryptographically exact copy of the preregistered checkpoint exists in the relay. The highest-value next step is to close provenance on the experiment server by importing exactly that one artifact and re-verifying the checkpoint bytes at the frozen server path. Do **not** combine this with package installation, model loading, synthetic forward, or scientific execution; those remain a later Research-Lead decision after server-side byte identity is established.

---

# CURRENT 1-HOUR WORK PACKAGE — T013-YW-P3R5

**Title:** Import the single verified relay artifact to the experiment server and close checkpoint byte provenance — no dependency/model/runtime work

**Time budget:** **45–60 minutes of focused work.** This is one engineering objective. Stop immediately when one terminal state below is established. Do not use remaining time to resume P3 dependency installation or execute the prepared synthetic smoke.

## One scientific/engineering objective
Download **exactly once** the already verified GitHub Actions artifact `t013-yw-s-stage2-4466ab94-relay` (artifact ID `10341040916`, run `34827628282`), validate its binding and contents fail-closed, verify the embedded checkpoint against the frozen size/SHA256, then atomically place that checkpoint at the already fixed experiment-server weight path and re-hash it there. This package ends at server-side byte identity.

## Why this is the highest-value next step
P3R4 removed the ambiguity that the immutable official checkpoint might be unavailable or different: the hosted runner obtained bytes matching the pre-outcome frozen identity exactly. The remaining prerequisite before runtime work is therefore local provenance, not another network diagnosis and not a model experiment. Separating relay import/re-hash from environment installation and forward execution prevents a transport success from silently turning into a multi-stage post-outcome engineering search. It also gives the next cycle a clean binary input: the exact frozen checkpoint is or is not present at the fixed server path.

## Fixed inputs/settings

### Frozen relay binding — do not change
- Repository: `word-ky/TOVD`.
- Workflow run: `34827628282`, attempt `1` only.
- Workflow head SHA: `0a9e6a004191c9ab20db4feeebab51d88cc3760d`.
- Artifact name: `t013-yw-s-stage2-4466ab94-relay`.
- Artifact ID: `10341040916`.
- GitHub-reported artifact size: `305061442` bytes.
- GitHub-reported artifact digest metadata: `sha256:2589f9b63f57e51d4646ea114cdbff0bf7896d7988c8a499360bb077ef76c5bf` (record it; checkpoint identity below remains the hard scientific/provenance requirement).
- Artifact must still report `expired=false` and remain bound to run `34827628282` / head `0a9e6a004191c9ab20db4feeebab51d88cc3760d`. If not, stop; do not rerun P3R4.
- Expected artifact members: exactly `s_stage2-4466ab94.pth` and `acquisition_receipt.json`, with no extra member, duplicate path, path traversal, absolute path or symlink.
- Expected artifact `acquisition_receipt.json` SHA256: `d64080965c78597c853d3f99c34cdf2885d7d5154f0f1141cd81b4639270241f`. Parse it and require its `verified=true`, run/attempt/workflow commit, initial URL, expected/observed size and expected/observed checkpoint SHA256 to match the accepted P3R4 record exactly.

### Frozen checkpoint identity — do not change
- Model/revision: `wondervictor/YOLO-World-V2.1` at `c620164ee3979bf49b895c8a8e0f49aeaca89209`.
- Checkpoint filename: `s_stage2-4466ab94.pth`.
- Expected checkpoint size: `305058902` bytes.
- Expected checkpoint SHA256: `4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458`.
- Fixed server destination: `/home/wenchang/asdasdsad/wjq/TOVD/shared/t013_yoloworld/weights/s_stage2-4466ab94.pth`.
- Do not refresh Hugging Face metadata and do not contact Hugging Face in this package.

### Import procedure — provenance only
1. Snapshot current HEAD, artifact metadata, free space, and whether the fixed destination already exists. If it already exists, compute its size/SHA256 before doing anything else. If it already matches the frozen identity, record `already_present_exact=true`, perform **zero artifact downloads**, and return the READY state below; do not overwrite it.
2. Otherwise use only already available GitHub repository authentication/tooling to request the archive for artifact ID `10341040916`. Do not install `gh`, mint a PAT, change permissions, or use a browser/manual download. The archive download count for this package is at most **1**.
3. Download to a project-local temporary path outside the fixed weights filename. Record command/API endpoint, exit code, archive byte count and SHA256. Record whether the observed archive SHA256 matches the GitHub digest metadata, but **do not treat archive-digest mismatch alone as permission to improvise**; if metadata/archive binding is ambiguous, stop fail-closed before installing the checkpoint.
4. Inspect the archive before extraction. Require exactly the two expected safe regular-file members and no others. Reject duplicates, absolute paths, `..`, symlinks or unexpected nesting.
5. Extract only to a temporary project-local directory. Verify `acquisition_receipt.json` hash and semantic fields against the accepted P3R4 record. Then verify the extracted checkpoint is exactly `305058902` bytes and SHA256 `4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458`.
6. Only after all checks pass, create the fixed weights directory if needed and atomically move/copy-via-temp the exact checkpoint into `/home/wenchang/asdasdsad/wjq/TOVD/shared/t013_yoloworld/weights/s_stage2-4466ab94.pth`. Do not deserialize it.
7. Re-run `stat` and `sha256sum` on the final fixed path and require the same exact size/hash. Record the final inode/mtime if convenient as operational evidence; they are not scientific settings.
8. Leave the existing isolated environment, source trees, CLIP cache, prepared `synthetic_smoke.py`, P0/P1/P2/P3/P3R1–P3R4 evidence, Grounding files and scientific settings unchanged. Temporary archive/extraction cleanup may occur **only after** final verification and only if the exact commands/paths are recorded; cleanup is optional and is not part of acceptance.

## Explicit non-goals / prohibitions
- No P3R4 rerun, second artifact download, alternate artifact, mirror, direct Hugging Face transfer, CDN/Xet/S3 URL, alternate checkpoint/model/revision, or manual file source.
- No modification of the frozen expected size/SHA256, YOLO/MMYOLO revisions, P2 vocabulary/blank convention, native postprocessing, corruption bytes, selected image IDs, metric definitions, bootstrap or gates.
- No `pip`/`apt`/`conda` install or update, no resumption of the interrupted Torch wheel, no MMCV build, MMEngine/MMDet installation, source patch, checkpoint deserialization, CUDA op import, model construction/load, synthetic forward or image inference.
- No T013 selected image/corruption, COCO/LVIS image/annotation/evaluation, AP/AP50/AR, D/A, bootstrap, Gate1/2/3/4, Grounding rerun, T014, CF/MECH scientific work, proposal-lock, or YOLO scientific benchmark.
- Do not interpret successful import as runtime feasibility or scientific support. Do not interpret an import/auth/archive failure as a YOLO scientific negative.

## Acceptance / stop criteria
End in exactly one state:

- `YW_P3R5_CHECKPOINT_IMPORTED_VERIFIED_RETURN_TO_LEAD` if either (a) the fixed destination was already present and independently matches the exact frozen checkpoint identity, or (b) the single bound artifact is downloaded once, passes artifact-member and receipt validation, the embedded checkpoint matches the exact frozen size/SHA256, and the final fixed server path re-hashes exactly. This state authorizes **no model/runtime work**.
- `YW_P3R5_ARTIFACT_UNAVAILABLE_RETURN_TO_LEAD` if the fixed destination is absent/nonmatching and artifact `10341040916` is expired, unavailable, or cannot be downloaded using already available repository authentication. Do not rerun the workflow or broaden credentials.
- `YW_P3R5_ARTIFACT_BINDING_MISMATCH_RETURN_TO_LEAD` if run/head/name/ID/entry set/receipt provenance is not exactly the accepted P3R4 binding. Do not install any checkpoint bytes.
- `YW_P3R5_CHECKPOINT_HASH_MISMATCH_RETURN_TO_LEAD` if the extracted or final checkpoint size/SHA256 differs from the frozen identity. Preserve evidence; do not substitute another file.
- `YW_P3R5_AMBIGUOUS_RETURN_TO_LEAD` for any unexpected archive/provenance/filesystem condition. Fail closed; do not improvise.

No P3R5 terminal state authorizes package installation, checkpoint deserialization, runtime smoke, or scientific execution.

## Exact evidence Codex must write back to `coordination/CODEX_TO_CHATGPT.md`
Report all of the following exactly:
- task `T013-YW-P3R5`, task-start HEAD, and exact commit containing this Lead instruction;
- final state and start/stop timestamps;
- preflight fixed-destination existence plus size/SHA256 if present; free-space snapshot;
- artifact metadata snapshot: run ID/attempt/head SHA, artifact ID/name, `expired`, expiration timestamp, reported size and digest;
- exact archive-download command/API endpoint with credentials/tokens omitted, exit code, download count (`0` or `1` only), archive path, bytes and SHA256;
- archive member listing and explicit safety checks: exact member count/names, duplicate/path-traversal/absolute-path/symlink checks;
- extracted `acquisition_receipt.json` bytes/SHA256 and parsed binding fields, with explicit equality to accepted P3R4 values;
- extracted checkpoint size/SHA256 and exact verification commands/outputs;
- exact atomic placement command/procedure, final fixed destination path, and post-placement `stat`/SHA256 output; state whether the destination was newly installed or already exact;
- temporary archive/extraction paths and whether they were retained or removed;
- explicit counts: P3R4 workflow reruns `0`; artifact downloads `0` or `1`; alternate artifact/source/checkpoint/model/revision `0`; package install/build `0`; checkpoint deserialization `0`; CUDA/model-load/forward `0`; T013/COCO/LVIS scientific actions `0`; Grounding rerun `0`; T014/CF/MECH scientific work `0`; YOLO scientific benchmark `0`;
- confirmation that Grounding remains canonically `GROUNDING_PRIMARY_NOT_SUPPORTED`, P0/P1/P2/P3/P3R1–P3R4 evidence remains unchanged, and all YOLO scientific settings remain frozen;
- machine-readable import receipt and concise human report under `research_log/t013_yoloworld/p3r5/` with hashes in a delivery manifest; do not commit the 305 MB checkpoint or archive to Git;
- recommended next action only as `Research Lead review of P3R5 server-side checkpoint provenance before any runtime-feasibility resumption`.

Stop after this handoff and await Research-Lead review.