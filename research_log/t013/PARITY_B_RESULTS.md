# T013-PARITY-B result: HF-1024 harness fails the fixed alternative

Recorded 2026-09-12T20:26:15.013866+08:00. Engineering status: BLOCKED / RETURN TO RESEARCH LEAD. Under the explicit decision in Lead999b4b7/ddd24e7, the HF-1024 harness is rejected for T013 primary use because two of the three prescribed images fail. The scientific hypothesis and Gates1–4 remain UNEVALUATED.

Code/rules frozen and pushed before this run in commit61918fa. Exactly one diagnostic run: `20260912-202233-tovd-t013-parity-b`, immutable release`20260912-202152-tovd-t013-parity-b`, completed2026-09-12T20:23:52+08:00 with exit1. No tolerance, threshold, checkpoint, prompt, image or matching change was made after outcomes.

| Image | Native/HF detections | Class-count equality | Minimum matched IoU | Maximum matched score error | Result |
|---|---|---|---:|---:|---|
|139|300/300|yes|0.9999052220914602|0.00043116509914398193|FAIL score error >1e-4|
|285|300/300|no|not matched|not matched|FAIL class multiset|
|632|300/300|yes|0.9999458932758641|0.000018522143363953|PASS|

For image285, HF has one more class0(person) and one fewer class21(bear), using canonical zero-based indices. Per instructions this fails immediately, so class-conditioned assignment and matched extrema are undefined, not zero. Image139 passes the IoU bound but its score error is4.31 times the fixed upper bound. Image632 passes both. All HF repeats are exact; native and HF state hashes are individually unchanged before/after.

## Diagnostic-only raw query comparison

|Image|Index-aligned boxes /900 (<=1e-4)|Hungarian box IoU min|median|mean|Identity permutation|
|---|---:|---:|---:|---:|---|
|139|848|0.5950829277181513|0.9999692964269623|0.9979470661808271|True|
|285|271|0|0.9976759586888355|0.9777492406906994|False|
|632|894|0.9897086964212779|0.9999938962464809|0.9998940200820289|True|

Image285 does have a nonidentity raw-box assignment, but its top300 canonical class counts differ. Thus allowing raw-query reordering does not make this prescribed detector comparison pass. These three-image diagnostics do not identify the internal numerical cause or establish a task-level AP difference.

## Reproduction and evidence

The native runner was reused, with an optional detection-level branch; no model/detector code was changed. Both ports use the existing FP32 CPU setup/fourthreads, identical HFprocessed pixels, V0=195tokens, frozen checkpoints and source revisions recorded in NATIVE_PARITY_REVIEW.md. Use exact primary torch.topk300 over900x80 class scores, normalizedxyxy, no AP threshold/NMS. Class-wise deterministic SciPy1.17.0 LSAP maximizes summed float64 IoU; scores never enter assignment. Fixed tie handling and all thresholds were committed before inference in PARITY_B_PLAN.md.

Local focused13tests passed0.76s; remote13tests passed0.77s before inference. Tests cover permutation invariance, count mismatch, strict thresholds and score-independent deterministic assignment under identical-box ties. After retrieval, local matching on all three saved raw NPZs exactly reproduces the JSON results, without rerunning a detector. All four JSON/NPZ SHA256s match the server. Raw queries, class scores, top300 indices/scores/classes, all class-wise matched pairs and all900-query permutations are preserved.

Command: `OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 shared/t013/venv/bin/python -u -m scripts.t013_native_parity --assets /home/wenchang/asdasdsad/wjq/TOVD/shared/t013 --detection-level --output "$AUTODL_ARTIFACTS_DIR/parity_b.json"`. Exact absolute command and fixed release cd are in run.sh. Unlike the prior shared last-release ambiguity, this command explicitly changes into its immutable TOVD release and writes pwd/source hashes to artifacts before inference.

Changed files: scripts/t013_native_parity.py, scripts/t013_parity_matching.py, tests/test_t013_parity_matching.py, PARITY_B_PLAN.md (code commit61918fa); this result report, original run artifacts/logs/metadata, project_state.md, IMPLEMENTATION_NEXT.md, PREREQUISITES.md, session_log.md, REMOTE.md and CODEX_TO_CHATGPT.md (publication commit). Frozen vocabulary content/IDs, scientific definitions and detector path unchanged.

## Next action

Stop detector work and await a new Lead decision, as explicitly required by the active mailbox when any PARITY-B image fails. Do not relax/retry/change matching, shrink vocabulary, choose another checkpoint or start T014. No primary inference/AP/CI exists. Full preregistration/primary cache runner/complete bootstrap analysis remain pending.

The previously authorized COCO archive download20260912-190511-tovd-t013-coco-ranges-a6000 remains active,150/195parts last observed; let this existing transfer finish and collect hash/CRC receipt. No duplicate writer. Heartbeat remains active every15minutes, quiet if unchanged. T001–T012 stay closed. Inner loss/gradient/update/reset diagnostics are inapplicable to this frozen-detector task; neither model was adapted.
