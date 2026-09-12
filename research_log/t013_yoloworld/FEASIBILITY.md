# T013-YW-P0 engineering feasibility inventory

Recorded 2026-09-12T23:22:00.548672+08:00. P0 document/metadata inventory complete; model execution and a working environment are NOT verified. No YOLO inference, checkpoint download, package installation, active-run changes, or Grounding partial scientific metric inspection occurred.

## Revisions and observed source issues

Official upstream: https://github.com/AILab-CVC/YOLO-World . Inspected HEAD4f70adbaacf5685bd9ec5bea85f1f91057f6fc0b; ast.parse reproduces a SyntaxError at yolo_world/models/detectors/yolo_world.py:61. Commit1f12bca introduced the add-mask change. Pin candidate official predecessorb1b09f2f0340ca7dede69e10b7e909c469677fd9,2025-02-06; all19 model files pass syntax-only parsing without importing dependencies. This is a source-version choice, not a code repair. MMYOLO gitlink4d97b3a06609dba94b8ec584be2f2029cfdb7519 is the onuralpszr/mmyolo fork pinned by the official project. Preserve this gitlink rather than the floating package URL. Local inspection clone lives inside project .autodl/yoloworld/YOLO-World; durable source snapshots/URLs/hashes are in upstream_snapshot andinspection_receipt.json.

## Official checkpoint metadata

All V2.1 links below use pinned author repository revisionc620164ee3979bf49b895c8a8e0f49aeaca89209. Sizes/hashes come from saved HF API LFS metadata; payload bytes were not fetched. [Official V2.1 model card](https://github.com/AILab-CVC/YOLO-World/blob/b1b09f2f0340ca7dede69e10b7e909c469677fd9/docs/update_20250123.md).

| Model candidate | Bytes | SHA256 | Exact URL |
|---|---:|---|---|
|S stage2,1280 — selected contingent candidate|305058902|4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458|[s_stage2](https://huggingface.co/wondervictor/YOLO-World-V2.1/resolve/c620164ee3979bf49b895c8a8e0f49aeaca89209/s_stage2-4466ab94.pth)|
|S stage1,640 — card association unresolved|305058846|d1c1d7d8611a3b97f74cf813faf911c2e047a6529622621943b4022c679ecce0|[s_stage1](https://huggingface.co/wondervictor/YOLO-World-V2.1/resolve/c620164ee3979bf49b895c8a8e0f49aeaca89209/s_stage1-d1c1d7d8.pth)|
|M stage1,640 — not selected|367608804|7e1e52990256587e0b5e468190767a71463d339688782f8ec09e109fa40c6591|[m_stage1](https://huggingface.co/wondervictor/YOLO-World-V2.1/resolve/c620164ee3979bf49b895c8a8e0f49aeaca89209/m_stage1-7e1e5299.pth)|

The S640 card actually links to x_stage1-62b674ad.pth,545782739bytes; do not treat that link as S. The S1280 row is unambiguous and has a published full-COCO zero-shot reference38.2AP/54.2AP50/41.6AP75. V2 S640 yolo_world_v2_s_obj365v1_goldg_pretrain-55b943ea.pth is another official historical asset (repo4340b03f4f59f46279a6581bbb818e0f77765d4d,305052941bytes,SHA55b943ea2643f716f012243a66e49f7f0b12c216a01230ccc9c99e4e128da1a6); its inspected V2 table primarily documents LVIS, so it is not silently substituted for the selected V2.1 COCO-baseline candidate.

## Vocabulary API and110-class feasibility

YOLOWorldDetector.predict derives class count from text feature count. HuggingCLIPLanguageBackbone.forward tokenizes separate strings, encodes/normalizes512D features and reshapes by image batch. Model config supports1203testclasses; no fixed110-class output limitation was found. Tokenizer-only receipt token_capacity.json shows frozen80/110/110names each3–5tokens versus77CLIPpositions. No text embeddings or model outputs were computed. [Backbone](https://github.com/AILab-CVC/YOLO-World/blob/b1b09f2f0340ca7dede69e10b7e909c469677fd9/yolo_world/models/backbones/mm_backbone.py), [detector](https://github.com/AILab-CVC/YOLO-World/blob/b1b09f2f0340ca7dede69e10b7e909c469677fd9/yolo_world/models/detectors/yolo_world.py).

Use per-image texts=list(names) through LoadText/DataSample, or reparameterize([list(names)]) for one batch's cached vocabulary. Distinguish class-synonym lists accepted by LoadText from the batch-of-vocabularies expected by the encoder. The official Gradio caching path demonstrates the latter. The image demo uses a different nesting and appends blank; do not copy it blindly into an audit. Refresh embeddings when changing vocabularies; avoid forward_tokenizer's one-time cache. Cache is not gradient adaptation. Offline convolution folding is a separate export route and is excluded from this contingency.

## Dependency facts and proposed isolation

| Item | Evidence at pinned source | Proposed next-phase target / limitation |
|---|---|---|
|Python|Project metadata>=3.7; active TOVD is3.12|A separate Python3.10 environment, without system-site-packages; not created here.|
|Torch / torchvision|Installation narrative citesTorch1.11; pyproject allowsTorch>=1.11 but requires torchvision>=.16.2|A plausible coherent modern pair isTorch2.1.2+cu118/torchvision0.16.2 in isolation. This pairing was not installed or tested.|
|MMCV|basic_requirements fixes2.0.0; install guide also shows2.1.0/2.2.0 examples|Keep fullMMCV2.0.x for MMDetection3.0.0. Compiled CUDA ops are needed; mmcv-lite is not equivalent.|
|MMDetection|pyproject/basic_requirements3.0.0; __init__ requires2.0.0rc4<=MMCV<2.1.0|Do not installMMCV2.1.0 withMMDet3.0.0 despite the guide example.|
|MMYOLO|requirements0.6.0; gitlink is exactfork revision above|Use pinnedsource. Its MMEngine bound is>=.7.1,<1.0; MMDetection>=3,<4.|
|MMEngine|basic_requirements0.10.3|Pin0.10.3.|
|Text stack|basic_requirementsTransformers4.36.2,timm.6.13|SeparateTransformers4.36.2/tokenizers0.15.x/NumPy1.26.4 candidate; existingTOVDTransformers4.44.2 untouched.|
|OpenCV|basic_requirements lists bothopencv-python4.9.0.80 andheadless4.2.0.34; pyproject unpinnedopencv-python|These packages share cv2; resolver list is not a trustworthy lock. Preserve T013 corruption bytes with originalTOVDcorruptiongenerator; choose one YOLOcv2 distribution in a later dependency task.|

[Installation guide](https://github.com/AILab-CVC/YOLO-World/blob/b1b09f2f0340ca7dede69e10b7e909c469677fd9/docs/installation.md), [basic requirements](https://github.com/AILab-CVC/YOLO-World/blob/b1b09f2f0340ca7dede69e10b7e909c469677fd9/requirements/basic_requirements.txt), [package metadata](https://github.com/AILab-CVC/YOLO-World/blob/b1b09f2f0340ca7dede69e10b7e909c469677fd9/pyproject.toml), [MMDetection3.0 version bounds](https://github.com/open-mmlab/mmdetection/blob/v3.0.0/mmdet/__init__.py).

The official cu118/torch2.1 wheel index inspected here listsMMCV2.1.0 forPython3.10, which violates the pinnedMMDet3.0 upper bound. Thus a naive pip install-e or that wheel example is not a verified solution. One plausible isolated strategy, if separately authorized, is to retainMMCV2.0.x and build its fullops against the isolatedTorch2.1.2 CUDA11.8 toolchain. The server already exposesCUDA11.8; compilation compatibility is UNVERIFIED. Alternatively the officially documented legacyTorch1.11/MMCV2.0.0 route conflicts with the currentpyproject torchvision floor. No dependency override, source build or assertion patch was attempted this cycle. The pyproject also requests bothmmcv-lite andmmcv; future packaging must select the fullops runtime rather than co-installing overlapping namespaces. These are explicit preparation items for Lead, not claims of a working environment.

Proposed project path only: shared/t013_yoloworld/env plus isolated source/weights/cache directories under the same TOVD root. Do not modify shared/t013/venv, its sitepackages, native source or activeimmutable release. Do not invoke broadpipupgrade. A later environment-only package must resolve packaging constraints and run import/operator checks before any model load; if a clean isolated stack cannot be established, report infeasibility and stop. There is currently a plausible source-build path, not proof that all packaging constraints can be satisfied without an approved installation adjustment.

## Device, input and runtime path

Read-only server check identifies GPU1 as NVIDIA RTX A6000; cuda.mem_get_info returned50598707200free/50897289216totalbytes. This is transient availability, not a reservation or YOLO memory benchmark. A305MB S checkpoint andbatch1 make A6000 feasibility plausible; peakmemory/speed are unknown. NoYOLOFPS/latency claim is made. Expectedfuturepath isPyTorchCUDA, FP32 initially, nativeMMCVops, notONNX/TensorRT andnot the activeGroundingCPUprocess. CurrentserverNVMLwarning persists; no driver change proposed.

Selected native preprocessing isYOLO keep-ratio resize/letterbox1280,pad114, data-preprocessor BGR-to-RGB and/255. Corruptions must be generated using the frozenTOVD RGBuint8 implementation before this transform; theIOadapter must not double-swapchannels. The selected config inherits LVIS data defaults; futureCOCOtest config must usecanonicalCOCOmapping andtheunchangedIDs. No annotations may enterprediction computation. [Pinned MMYOLO base](https://github.com/onuralpszr/mmyolo/blob/4d97b3a06609dba94b8ec584be2f2029cfdb7519/configs/yolov8/yolov8_s_syncbn_fast_8xb16-500e_coco.py).

Head.predict_by_feat exposes decodedboxes andsigmoidclassscores andsupportswith_nms=False. Upstreamtest defaultsNMS.7/score.001/max300 differ fromT013 noNMS/noAPthreshold/globaltop300. The contingency document records the inherited default; no architecture-specific override is authorized now. Officialblankbackground andnativeNMS may require a later explicitLeadprotocoldecision for baseline/audit separation. No code was written to bypass these differences.

## Package assessment and next boundary

P0 document/inventory deliverables are complete: officialpinnedsourcecandidate, unambiguousS1280checkpointmetadata, finite110-class textcapacity, sameT013intervention/statisticalmapping, and an isolatedenvironmentproposal. Runtime readiness remains UNVERIFIED, with the dependency conflicts andbaseline/background/postprocessing questions explicitly open. This is not a detector-benchmark PASS.

Stop after committing these documents/receipts. Do not install, downloadcheckpointpayloads, run anydetector, resolvepackagingthroughad-hocpatches, or proceed to a second package thishour. Any YOLO scientific execution requires separate authorization after completedGrounding-DINO T013review. The existingGroundingrun was onlychecked forcounts/process/storage; partialAP/interaction/CI/mechanismoutputs were not inspected.
