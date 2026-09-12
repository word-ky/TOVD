# CURRENT AMENDMENT (supersedes older continuation below)

Lead2c4dbf5/28b8718requires matchedVrand andtrue native-vsHFparity. Use vocabulary_matched.json (195/408/408tokens),notr3Vrand545. Vhard/candidates/scores/embeddingsunchanged. Bins2:30,3:47,4:3;9localtests pass. Nativeoriginalcheckpointpreparation/parity scriptsadded; actualparitypending. Ifnative/HF mismatchexceedsLeadfixed1e-4,stopforLeadreview. ExistingHF256vsHF1024CUDAcheckpassesexactlybutdoesnotfulfilnative/HFparity. Oldr3CPUsmokewasinterruptedafteramendment.

IDs accepted/frozen42daa6e inimage_selection.json:1000IDs,smoke139/285/632. Annotationsdownload/hashverified. Fullimagezipstilldownloadrun190511; do notduplicate. COCOcachebootstrap primitives/classmappingandFP/coverage/margintestsimplementedand7passedbothlocal/remote. Rawprimarycache runner/full1000bootstrapanalysis/fullPLANremainpending. Allprimaryinferenceblockeduntilcompleteprerequisitescommit.

# T013 engineering continuation

This is a recovery note, not a completed preregistration or scientific result.
Scope remains the full authoritative T013 task; no T014 authorization.

## Completed prerequisites

- Official HF Swin-T checkpoint a2bb814dd30d776dcf7e30523b00659f4f141c71,
  model.safetensors SHA256 1a2412ef99bd74bcd3c2a246fa1e48581f8889a1300c9051974741314fc042f3,
  689359096 bytes, downloaded through hf-mirror and verified against original HF API.
- Isolated `/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv` works with Torch2.4.0+cu121,
  torchvision0.19.0+cu121, Transformers4.44.2, NumPy1.26.4, imagecorruptions1.1.2,
  pycocotools2.0.8, pytest9.1.1. Root original venv and global CUDA unchanged.
- Native 256-text-token truncation diagnosed on local CPU / A6000 CPU / CUDA.
  Official HF implementation honors shared1024 capacity without learned-parameter changes.
  `disable_custom_kernels=True` uses official PyTorch deformable attention. Constructor
  nevertheless emits attempted custom-kernel-load warnings; do not repair global CUDA.
- `t013_text.py` three focused tests pass locally and remotely. Aliases were audited
  before any image inference. Initial text run r2 is superseded by final laptop/racket
  alias exclusions and full-prompt BERT coverage check in r3. Preserve initial receipts.
- All four severity3 corruption functions ran on a 64x64 RGB engineering fixture.
  No corruption compatibility repair was needed.

## Active downloads / execution

`20260912-190511-tovd-t013-coco-ranges-a6000` downloads official COCO archives using
8 range connections, 4MiB parts, annotations first, then val2017 images. Parts under
shared/t013/coco are retained for continuation after an observed network failure.
Full archives get range/size checks, ZIP CRC verification and SHA256 receipts before
extraction. Do not start a second writer while this run is alive. Direct partial
val2017.zip from earlier stopped run is retained; completed new archives use
`.parallel.zip` names. Data content/source are unchanged. Do not rerun the old asset
script: weights/environment are ready and it uses the slow single connection.

Text r3 run ID is recorded in current project_state/session log when dispatched.
Use its final vocabulary.json and embeddings, not the r2 preliminary vocabulary.
No primary image inference has happened; IDs are not yet selected, PLAN not frozen.

## Next concrete steps

1. Inspect explicit active run IDs, recover text r3 receipts. Verify full-prompt encoder
   emits every token even for >512-token prompts; detector uses sentence-reset position
   IDs within existing BERT embeddings. Commit final names, normalized forms, scores,
   vectors and hashes before detection. Record unequal realized token lengths; equal
   160-class counts/shared capacity do not constitute a token-matched causal control.
2. Once annotations exist, run `python -m scripts.t013_select_images --annotations
   <assets>/coco/annotations/instances_val2017.json --output <receipt>/image_selection.json`.
   Exactly1000 from sorted5000 using Python Random(20260912), sorted afterward; smoke
   first3 remaining IDs. Coverage follows selection. Commit IDs/hash before inference.
3. Reproduce frozen detector V0 on disjoint smoke images. `scripts/t013_smoke.py` is
   prepared but has NOT run. It checks all45 small conditions, exact V0 replay and
   original256-vs1024 capacity parity, pixel replay, full names and byte-identical state.
   Preserve any failure, repair only observed engineering issues; do not tune protocol.
4. Complete PLAN.md with exact downloaded annotation/image hashes and source revisions,
   final names/tokenization, fixed thresholds, class mapping, seeds and all Lead gates.
   Freeze before primary outcomes. Existing helper selects global300 query/class pairs,
   upstream class-token mean probabilities, no AP threshold/NMS; diagnostic threshold
   .25 is a proposed fixed pre-outcome choice already in code, not calibrated.
5. Implement raw-cache runner and COCO evaluation/statistics only after the donor smoke
   works. Save all900 boxes/class-score vectors and selected300 pairs per image/condition
   remotely as compressed arrays; immutable raw manifest/hash locally is sufficient for
   recovery while multi-GB raw files remain under this project on A6000. Store summaries,
   receipts and analysis artifacts locally too. Never reuse T001-T012 mechanism modules.
6. Implement/test paired1000 image-bootstrap replicates and fixed Gates1-4. An exact
   optimization is to cache COCOeval per-image matching, repeat references for resampled
   image copies, and rerun COCOeval.accumulate for each dataset sample. Validate against
   direct re-evaluation with duplicated image/GT/prediction IDs on a tiny fixture including
   tied scores and crowd/ignored GT. Do not average per-image AP, use unpaired samples,
   or approximate bootstrap by weighted per-image AP. All15 conditions share sampled IDs.
   Bootstrap seed/procedure and operational Gate3 definitions still need PLAN freeze.
7. Record canonical COCO AP50/mAP/AR and explanatory FP/recall/localization/margins as
   required. Distinguish out-of-canonical-vocabulary detections from claims that all such
   detections are false in the physical scene (COCO is not exhaustively LVIS-annotated).
   Comparable class scores are available; matched-GT margin can be measured directly.
8. Run proportionate local and A6000 CPU/CUDA checks, final full affected regression;
   then launch fixed1000x15 primary inference, analysis, receipts/report, commit/push.
   Wait Lead review after scientific handoff; no autonomous T014 or adaptation method.

## Scientifically pending

No AP, interaction, bootstrap CI, or Gate1-4 decision exists. Do not label prerequisite
success as scientific success, or delays as rejection. T001-T012 remain closed.
Do not reopen closed synthetic experiments. Heartbeat15min handles continuation.
