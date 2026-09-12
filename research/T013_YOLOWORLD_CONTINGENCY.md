# T013 YOLO-World contingency — pre-outcome registration

Task T013-YW-P0; registered 2026-09-12T23:22:00.548672+08:00, before any Grounding-DINO primary AP, interaction or CI was read. This is a secondary cross-backbone contingency. Its scientific execution is NOT AUTHORIZED. Grounding-DINO run20260912-210355-tovd-native30-primary continues unchanged under freeze6fec32243985ccc808123d851abf5f3dea10af99. A negative Grounding-DINO result remains a negative for that detector.

## Reproducible upstream candidate

Use [AILab-CVC/YOLO-World at b1b09f2f0340ca7dede69e10b7e909c469677fd9](https://github.com/AILab-CVC/YOLO-World/blob/b1b09f2f0340ca7dede69e10b7e909c469677fd9/README.md), an official V2.1-era commit dated2025-02-06. Pin its MMYOLO submodule commit4d97b3a06609dba94b8ec584be2f2029cfdb7519 from the repository's gitlink; do not follow a floating fork branch. The inspected current HEAD4f70adbaacf5685bd9ec5bea85f1f91057f6fc0b fails syntax parsing at yolo_world.py:61 (assignment to None). The selected commit is the latest official predecessor before that reproduced regression; no upstream code was patched. All19 model Python files at the candidate revision parse. This is source feasibility evidence, not an import or runtime test. See inspection_receipt.json for source snapshots/hashes.

## Deterministic checkpoint rule fixed before outcomes

Eligibility requires an official pretrained open-vocabulary checkpoint, an unambiguous checkpoint-to-model/config link, a published COCO zero-shot reference, support for the unchanged110 semantic classes, and later successful baseline reproduction on one A6000. Exclude COCO-finetuned, image-prompt, learned-prompt and fixed-80-class deployment variants. Compare eligible architecture tiers in S,M,L,X order; within a tier prefer the lowest documented resolution with an unambiguous checkpoint mapping. Do not rank by T013 results or expected interaction strength. A later authorized feasibility test must demonstrate comfortable memory use (batch1, peakallocated<=24GiB on48GiB A6000) and the documented baseline; neither is claimed measured here. Failure returns to Lead, not to an automatic larger-model sweep.

**Candidate fixed by this rule: YOLO-World-V2.1-S, stage2,1280.** The official model card maps this S model directly to s_stage2-4466ab94.pth. The nominal S640 model would normally be preferred, but both inspected official cards link its row to the X stage1 checkpoint. Official repository metadata contains a separately named S stage1 file; its exact card/config association needs clarification. It is therefore ineligible under the unambiguous-mapping condition in this package. This is a metadata reason recorded before outcomes, not a performance choice. No switching to that candidate later without a Lead amendment. [Official V2.1 card and baseline table](https://github.com/AILab-CVC/YOLO-World/blob/b1b09f2f0340ca7dede69e10b7e909c469677fd9/docs/update_20250123.md).

| Candidate | Official COCO zero-shot reference (AP/AP50/AP75) | P0 disposition |
|---|---|---|
| V2.1-S stage2,1280 |38.2/54.2/41.6|Selected contingency candidate; reproduction unverified|
| V2.1-S stage1,640 |36.6/51.0/39.7|Documented size-S baseline, but row links to X weights; unresolved mapping|
| V2.1-M stage1,640 |43.0/58.6/46.7|Official alternative inventoried; not selected because S is smaller|

These are upstream full-COCO reported figures, not TOVD experiments, not our1000-image results, and not selection criteria beyond the existence of a documented baseline. Selected config: configs/pretrain/yolo_world_v2_s_vlpan_bn_2e-3_100e_4x8gpus_obj365v1_goldg_train_1280ft_lvis_minival.py. Its default evaluation dataset is LVIS; future COCO baseline reproduction needs an explicit COCO test-only dataset/text/evaluator config, not use of a COCO-finetuned checkpoint. [Selected config](https://github.com/AILab-CVC/YOLO-World/blob/b1b09f2f0340ca7dede69e10b7e909c469677fd9/configs/pretrain/yolo_world_v2_s_vlpan_bn_2e-3_100e_4x8gpus_obj365v1_goldg_train_1280ft_lvis_minival.py).

Selected weight: [s_stage2-4466ab94.pth](https://huggingface.co/wondervictor/YOLO-World-V2.1/resolve/c620164ee3979bf49b895c8a8e0f49aeaca89209/s_stage2-4466ab94.pth),305058902bytes, SHA2564466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458. The hash/size are official LFS metadata only; no weight payload was downloaded. Model-repository revision isc620164ee3979bf49b895c8a8e0f49aeaca89209.

## Vocabulary representation and capacity

Keep each category string as its own CLIP text, without the Grounding-DINO inter-class delimiter. For one image, the backbone receives a batch containing one list of80 or110 names. CLIP normalizes a512-dimensional embedding per name; prediction sets class count from the text feature dimension. The chosen config already declares1203 test classes. This architecture does not pack110 names into one77-token sequence. The frozen names each tokenize to3–5 tokens, including specials, under official openai/clip-vit-base-patch32 revision3d74acf9a28c67741b2f4f2ea7635f0aaf6f0268; all fit its77-position context. This was tokenizer-only computation, with no model forward or image access. [Language backbone](https://github.com/AILab-CVC/YOLO-World/blob/b1b09f2f0340ca7dede69e10b7e909c469677fd9/yolo_world/models/backbones/mm_backbone.py), [detector API](https://github.com/AILab-CVC/YOLO-World/blob/b1b09f2f0340ca7dede69e10b7e909c469677fd9/yolo_world/models/detectors/yolo_world.py).

Future default is the normal YOLOWorldDetector with its checkpoint text backbone and vocabulary supplied online. It also exposes reparameterize([names]) to cache text embeddings for one vocabulary; changing vocabulary requires refreshing this cache. That method is different from tools/reparameterize_yoloworld.py, which folds embeddings into convolution weights. Do not use weight folding, learned prompt tables, image prompts, or training in this contingency. Cached/online equivalence, if later needed, must be established before the scientific run. [Reparameterization documentation](https://github.com/AILab-CVC/YOLO-World/blob/b1b09f2f0340ca7dede69e10b7e909c469677fd9/docs/reparameterize.md).

The official demo appends a blank background text and applies its own score filter. The V2.1 documentation discusses sensitivity to that blank. This contingency currently preserves exactly80/110/110 semantic strings with **no extra blank category**. If baseline reproduction establishes an architecture-required background slot, return to Lead for an explicit pre-execution amendment; do not silently add an111th class or choose padding from interaction results. Hardness remains the existing frozen BERT-ranked intervention; do not rerank candidates with CLIP to favor YOLO.

## Exact mapping of the frozen T013 audit

| Element | Inherited contract / YOLO mapping |
|---|---|
| Images |Same1000IDs in research_log/t013/image_selection.json, SHA8039a70f25c34f295345e63d1980f692631b6bbdaa5c37267a10852acbf3833b; same5000-image hash manifest38eb39894b8c0f1924e099b3a1ec0b885fdf7ec43c86933e1dc28186d85c3ba8. No new selection.|
| Vocabulary |Same vocabulary_native30.json SHA3bb4a0ebada1f9da407ae6a94f1135798dba7117bd658a6ecba97b2ebfad0967; names and order unchanged. Canonical indices0–79 map to sorted official COCOcategoryIDs; distractor indices80–109.|
| Visual conditions |Clean,gaussian_noise,motion_blur,fog,jpeg_compression; severity3,imagecorruptions1.1.2; seed(20260912+image_id*17+condition_index*1000003) mod2**32. Corrupt original RGBuint8 pixels once per image/condition, reuse identical bytes across all vocabularies, record hashes.|
| Detector input |Selected YOLO config's1280 keep-ratio resize/letterbox with pad114 and its native input normalization; map boxes back to original coordinates using recorded scale/padding. This is a detector-native transform difference, not a new corruption.|
| Audit prediction contract |Inherit raw decoded boxes/class scores, globaltop300 box/class pairs, no NMS/no AP threshold. YOLOHead exposes dense sigmoid class scores, bbox decoding, and with_nms=False. An adapter would keep class-score values from this detector; no BERT token-averaging formula is applied to CLIP logits. Implementation is a future task.|
| Official baseline distinction |Upstream test defaults use score_thr=.001,nms_pre30000,NMSIoU.7,max_per_img300. Reproduce the published baseline using its documented protocol separately. It is not identical to inherited T013 no-NMS audit semantics. Any proposal to adopt native YOLO NMS for the audit requires later explicit Lead approval; this P0 does not grant it.|
| Metrics |Same pycocotools2.0.8 AP50,mAP50:95,AR,AR50 atmaxDet100, areaall; filter distractors only after globalselection for canonical AP. Diagnostics atscore>=.25/IoU>=.5: canonicalFP/image via officialmatching, off-canonical predictions/image, microclasscorrect/localizationrecall.|
| Margin |Where raw dense class scores are available, select the best-IoU decoded candidate per noncrowdGT and calculate GTcanonical score minusmaxdistractor score; use the same commonlocalizedGT support across clean/corrupt×hard/random. Do not compare absolute margin scales across detectors.|
| Bootstrap |Same NumPydefault_rng(20260913),1000paired image bootstrap replicates of1000draws, shared drawmatrix across15cells; official dataset-levelCOCO accumulation including duplicateimages/crowd/absentclasses/tiedscores. Percentile95%CI withlinear interpolation. NevermeanimageAP.|

The mapping deliberately identifies postprocessing/background differences instead of silently accepting them. A future authorized phase must reproduce the official zero-shot baseline and freeze an approved YOLO audit wrapper before any interaction evaluation. No Grounding-DINO code, environment, cached predictions or frozen plan changes are allowed for this preparation.

## Scientific decision and interpretation

For each detector separately, preserve D(c,v)=AP50(clean,v)-AP50(c,v) and A(c,v)=D(c,v)-D(c,V0). Gate1: at least2/4corruptions have A_hard>=1.0AP50points and95%lower>0. Gate2: meanA_hard>=.75,meanhard-minus-random>=.50,and at least2positive hard-minus-random point estimates. Gate4 remains no protocol contamination; no weaker thresholds. Gate3 is the same three diagnostic families, interpreted by Lead and unable to rescue Gates1/2. Do not pool two detectors into a mean that hides a negative.

Here “pass” means Gates1/2/4 pass and Lead judges Gate3 coherent, under each separately frozen valid audit. Operational invalidity is not a scientific “fail”.

| Grounding-DINO | YOLO-World | Allowed conclusion |
|---|---|---|
|Pass|Pass|Cross-architecture evidence for this fixed intervention, limited to the two tested detectors.|
|Fail|Pass|Architecture-specific evidence only; Grounding-DINO negative is preserved.|
|Fail|Fail|Stronger rejection of the premise under these two frozen detectors/settings.|
|Pass|Fail|Grounding-specific phenomenon under the tested intervention.|

Preregister this matrix before the Grounding result. Later authorization may choose whether to execute the already-defined contingency; no metric-driven checkpoint/vocabulary search follows. YOLO-World scientific execution is NOT AUTHORIZED by T013-YW-P0. Stop after committing this document, FEASIBILITY.md and evidence receipt; await the next Research-Lead cycle. No T014 or method design is authorized.
