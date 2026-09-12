# T013-YW-P1 — source-only protocol receipt

## P2 superseding Lead convention — 2026-09-13

Lead ccec9fd accepts the P1 source-only blocker below and resolves the **dynamic-vocabulary interaction lane** before outcomes: append exactly one trailing U+0020 space, giving runtime81/111/111 while semantic names/order remain80/110/110. Blank indices are80/110/110, canonical indices0–79, extended distractors80–109. Blank participates normally through text encoding, fusion, dense scoring and the frozen native filtering/NMS/max300 selection. Remove blank-labelled retained predictions from semantic metric rows only after selection; never refill slots. The rule is identical across all15cells. Published-COCO baseline fidelity remains separately unresolved; no alternative blank convention may be selected from runtime results.

`protocol_adapter.py` implements only text construction, index partitions and filtering of already-native-selected row lists. It has no model, NMS, scoring, preselection-pool or refill implementation. Command `python -m unittest discover -s research_log/t013_yoloworld -p test_protocol_adapter.py -v` passed7/7 local standard-library tests in0.005s; output in `p2_tests.txt`. `protocol_adapter_receipt.json` binds the unchanged semantic artifact, historical P1 JSON and native constants. No detector import/install/load/inference occurred. P2 fixture verification is not runtime readiness or published-baseline reproduction.

The original P1 source evidence and its machine-readable `protocol_freeze.json` remain historical records. The null background fields in that P1 JSON mean source-only ambiguity at P1, not the current Lead-resolved interaction convention; use the P2 receipt for that convention. The remainder of this document preserves the P1 finding and stop request as recorded at commit6694fcc. P2 still does not authorize environment installation, checkpoint loading, image smoke tests, the benchmark or T014. Stop after this package and wait for the next Lead task.

## Original P1 record

Recorded 2026-09-13, before any YOLO outcome or Grounding-DINO partial scientific result was inspected. **BLOCKED: background handling is not uniquely established by the pinned official evidence.** Native postprocessing constants are resolved for the selected config; the complete published COCO baseline recipe is not. This is an engineering/protocol blocker, not a negative scientific result. Stop here and return to Research Lead under mailbox commit `c2f24e28d0579f2b0c55a8181c4532a721c354db`.

The model remains V2.1-S stage2/1280, checkpoint `s_stage2-4466ab94.pth`, SHA256 `4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458`. YOLO source revision is `b1b09f2f0340ca7dede69e10b7e909c469677fd9`; MMYOLO gitlink is `4d97b3a06609dba94b8ec584be2f2029cfdb7519`. No candidate substitution or model sweep occurred.

## Background: precise unresolved choice

The following evidence comes from that one fixed YOLO revision. Relative paths below refer to the upstream repository and corresponding verbatim `p1_source/yolo_world/` snapshots. Every file hash and pinned URL is in `protocol_freeze.json`.

| Official path | Observed behavior | What it establishes |
|---|---|---|
| `demo/gradio_demo.py:73–98`, especially line 80 | Adds exactly `[[' ']]` after user semantic names, then passes the list through the configured text pipeline | This text demo uses one trailing U+0020 space, not the empty string |
| `demo/image_demo.py:186–191`, `206–207` | Both comma and text-file branches append the same one-space entry; the file also calls reparameterize | Corroborates the demo's count/placement; its reparameterize nesting must not be mistaken for a baseline recipe |
| Selected S/1280 config, lines 127–160 | Test pipeline uses `LoadText`; dataset is `YOLOv5LVISV1Dataset` with `lvis_v1_class_texts.json`; evaluator is `LVISMetric` | Despite the variable name `coco_val_dataset`, this is an LVIS evaluation path, not an explicit V2.1 COCO baseline config |
| `yolo_world/datasets/mm_dataset.py:33–44,66–72` and `.../transformers/mm_transforms.py:100–129` | Dataset reads the supplied class-text JSON; LoadText selects the first alias and formats it with `{}`; neither appends a background entry | The selected config's default evaluation path supplies the file's classes as-is |
| `data/texts/lvis_v1_class_texts.json` and `coco_class_texts.json` | Source JSON has 1203 and 80 entries respectively; neither contains any whitespace-only alias | No hidden blank entry in these files. COCO JSON availability alone does not prove which input the published V2.1 COCO run used |
| `docs/update_20250123.md:15–26` | Explains padding/background influence on fusion and says padding still needs consideration in V2.1 | Does not mandate one count, placement or selected COCO evaluation path |
| Selected config, lines 47–54, and RandomLoadText lines 89–96 | Training uses empty-string padding to a training maximum of 80, with a variable count | Training padding is a different operation; it does not determine inference count for 80/110/110 semantic classes |

The [official text demo](https://github.com/AILab-CVC/YOLO-World/blob/b1b09f2f0340ca7dede69e10b7e909c469677fd9/demo/gradio_demo.py#L80) gives an unambiguous rule **for that demo**. The [selected evaluation config](https://github.com/AILab-CVC/YOLO-World/blob/b1b09f2f0340ca7dede69e10b7e909c469677fd9/configs/pretrain/yolo_world_v2_s_vlpan_bn_2e-3_100e_4x8gpus_obj365v1_goldg_train_1280ft_lvis_minival.py#L127) follows a different path with no automatic blank. The pinned [V2.1 discussion](https://github.com/AILab-CVC/YOLO-World/blob/b1b09f2f0340ca7dede69e10b7e909c469677fd9/docs/update_20250123.md#L15) does not resolve which path produced the selected checkpoint's reported COCO result.

Therefore `blank_handling_uniquely_resolved=false`; frozen blank string/count/placement are **null**, not zero. Do not silently choose the demo's one blank, retain P0's provisional zero, equate a space with an empty string, or pad 110 classes to another maximum. No runtime comparison can resolve this within P1. Semantic strings/order remain exactly 80/110/110. If Lead later resolves a background input, its identical count and placement must be recorded for all three vocabularies and it must be excluded from canonical/distractor semantic metrics, as P1 already requires.

## Native postprocessing constants resolved from config

Selected config:
`configs/pretrain/yolo_world_v2_s_vlpan_bn_2e-3_100e_4x8gpus_obj365v1_goldg_train_1280ft_lvis_minival.py`.

Its `_base_` (lines 1–2) directly imports the pinned MMYOLO `configs/yolov8/yolov8_s_syncbn_fast_8xb16-500e_coco.py`. That file defines `model_test_cfg` at lines 28–35 and assigns it to `model.test_cfg` at line 162. The selected YOLO config changes the backbone/neck/head and training assigner but does not override `test_cfg`. Its two further base files are `default_runtime.py` and `det_p5_tta.py`; their TTA settings are a separate opt-in lane and do not override the ordinary model test config.

| Constant | Fixed value |
|---|---|
| `multi_label` | `true` |
| `score_thr` | `0.001` |
| `nms_pre` | `30000` |
| `nms.type` | `nms` |
| `nms.iou_threshold` | `0.7` |
| `max_per_img` | `300` |
| `with_nms` | `true`, native prediction default |
| `rescale` | `true`, detector prediction default |
| `yolox_style` | absent in config, therefore native `.get(..., False)` path |
| TTA / demo extra filtering | disabled / not used |

The [pinned MMYOLO base](https://github.com/onuralpszr/mmyolo/blob/4d97b3a06609dba94b8ec584be2f2029cfdb7519/configs/yolov8/yolov8_s_syncbn_fast_8xb16-500e_coco.py#L28) is the source of these constants. They were also extracted with Python standard-library AST parsing of the literal `dict` expression; no MMEngine config execution or model import was used.

The call path is `YOLOWorldDetector.predict` (detector lines 34–55) → `YOLOWorldHead.predict` (head lines 396–411) → `predict_by_feat` (564–734). It sets class count from text features, applies sigmoid to dense class scores, decodes boxes, uses `filter_scores_and_topk(scores, score_thr, nms_pre)` with multi-label enabled, subtracts letterbox padding and divides by scale factor, then calls native `_bbox_post_process(..., cfg=cfg, with_nms=True, rescale=False)` and clips boxes to the original image size. The class chain is `YOLOWorldHead → YOLOv8Head → YOLOv5Head → mmdet.BaseDenseHead`. The pinned MMYOLO sources identify this final delegation; no library implementation was replaced or imported. Kernel/runtime fidelity remains untested.

No blank-specific output removal appears in this inspected head path. Thus a future background input cannot be treated as a harmless metadata entry: it reaches text fusion/class scoring and potentially native prediction selection. This reinforces the unresolved protocol issue; P1 does not invent a special suppression path.

The interactive Gradio demo performs an additional NMS and user-controlled score/top-box filtering after `test_step` (lines 90–98). The image demo similarly applies score and top-box display filters (97–110). Those are **not** the ordinary config-driven evaluator path and are not adopted for either future lane. The inherited `det_p5_tta.py` has a separate 0.65 TTA NMS setting; `tools/test.py:112–128` only selects it with `--tta`. P1 uses the ordinary 0.7 path, with no TTA.

## Baseline lane versus interaction lane

**Future baseline lane:** the goal remains reproduction of the selected checkpoint's published COCO zero-shot reference with official native preprocessing/postprocessing. The pinned card links S/1280 to the selected weight and reports a COCO reference (V2.1 document lines 60–75 and 98–108; README lines 96–143). README lines 189–207 refer to generic test tools, and `tools/test.py` reads a caller-provided config. In the inspected pinned tree, no selected S/1280 COCO-zero-shot command/config ties the reported number to a specific blank rule. The provided selected config evaluates LVIS. Consequently the **complete official COCO recipe remains unverified**, although the selected config's native constants are known. COCO-finetuning configs cannot establish the pretrained V2.1 baseline recipe and were not substituted.

**Future T013 interaction lane:** P1's explicit Lead decision supersedes the provisional P0 no-NMS emulation. Use the selected YOLO config's native postprocessing constants above for all 15 cells. Keep native 1280 keep-ratio resize, letterbox `allow_scale_up=False`, padding 114, BGR→RGB and normalization from the inherited config. Keep the frozen original-image corruption bytes, 1000 IDs, semantic names/order, canonical mapping, metric definitions, paired bootstrap, Gates 1/2/4 and four-case interpretation matrix. Canonical/distractor filtering for metric reporting occurs on the native retained predictions; do not reselect predictions separately for canonical AP. This is a detector-native change in prediction selection explicitly authorized before outcomes, not a change to Grounding-DINO's frozen pipeline. Compare within-detector D/A and gate outcomes; absolute AP equality across detectors is not required.

Neither lane is executable while blank handling and the source-to-COCO recipe connection remain unresolved. Background resolution, environment installation, checkpoint loading, image smoke tests, the benchmark and T014 are not authorized by this receipt.

## Evidence and verification

- `protocol_freeze.json`: resolved native constants, unresolved-background booleans/nulls, revisions, selected checkpoint, zero-execution declarations and all 21 source-file hashes/URLs.
- `p1_source/`: verbatim pinned YOLO/MMYOLO source/config/text-data snapshots with both licenses. No upstream modification. Existing P0 receipts remain unchanged.
- `inspect_p1_sources.py`: reproducible source-only extraction. Command: `python research_log/t013_yoloworld/inspect_p1_sources.py` from the TOVD root. It uses `git show <pinned-revision>:<path>`, JSON and AST; no torch, detector, image or package-install operation.
- MMYOLO files were fetched only as source bytes from `https://raw.githubusercontent.com/onuralpszr/mmyolo/4d97b3a06609dba94b8ec584be2f2029cfdb7519/<path>`, using standard-library `urllib.request.urlopen`; exact paths are in the machine-readable receipt. No package installation or submodule setup ran.
- Source-only output: 21 files; constants `true/30000/0.001/nms/0.7/300`; COCO 80 and LVIS 1203 text entries, both with no blank aliases. This is a static-source check, not a runtime or baseline PASS.
- Operational health at 2026-09-13T00:00:41+08:00: primary `20260912-210355-tovd-native30-primary` tmux alive, 103/1000 images at 10487.362925s; 27G filesystem free; analysis-result file absent. No AP/AP50/interaction/CI/mechanism output read.

**Return to Lead:** provide an authoritative selected-checkpoint COCO recipe that resolves the discrepancy, or issue an explicit pre-outcome amendment selecting and labeling an architecture-specific convention. P1 does not make that research choice. Zero YOLO inference, zero detector loads, zero checkpoint payload downloads, zero package installs, and zero active-primary changes occurred. Stop after committing this package and wait for the next Lead task.
