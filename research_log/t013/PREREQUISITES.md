# T013 prerequisite inventory and capacity diagnosis

Status: ACTIVE, no primary detector outcome generated. Lead scope c07ce16 / afe9c13.
This document is not the completed preregistration. PLAN.md will freeze actual
assets, vocabularies, image IDs and analysis before primary inference.

## Observed incompatibility and bounded repair

Official IDEA-Research/GroundingDINO revision
`856dde20aee659246248e20734ef9ba5214f5e44` hardcodes 256 text tokens in the
detector constructor and parameter-free contrastive head. The forward pass
truncates input text before the text encoder. Its COCO positive map is also 256
columns. Merely setting the native config max_text_len does not fix this.

The exact upstream caption builder, canonical COCO-80 names and BERT WordPiece
vocabulary produce **195 tokens**. Appending 80 nonempty names and separators
requires **at least 355 tokens**, regardless of LVIS similarity ranking. Thus
the unmodified native path cannot evaluate the requested complete vocabulary.
This is a text-capacity result, not evidence about the interaction hypothesis.

`probe_text_capacity.py` extracts the exact upstream caption builder and
parameter-free head via AST, without importing a detector or using images,
annotations, weights, or ranked distractors. The 256-token head fixture succeeds;
the 355-token fixture reproduces a tensor-size error. Local CPU and A6000 CPU/CUDA
all reproduce the same result. Raw run:
`20260912-184215-tovd-t013-capacity-a6000`, release
`20260912-184053-tovd-t013-capacity`, exit 0 at 18:42:26+08 on 2026-09-12.

Use the author's official Hugging Face Swin-T checkpoint
`IDEA-Research/grounding-dino-tiny`, revision
`a2bb814dd30d776dcf7e30523b00659f4f141c71`, with the maintained Transformers
4.44.2 implementation. Its text truncation and contrastive-head width both honor
`config.max_text_len`. Set the shared capacity to 1024 before loading one frozen
checkpoint; this changes no learned parameter shape or value. Verify original
V0 valid-token scores and boxes against the 256-capacity path before primary
inference. Extended vocabulary prompts must fit in full. No chunking, truncation,
alias shortening, or outcome-based name removal is permitted.

Use the official PyTorch deformable-attention implementation with
`disable_custom_kernels=True`: available server compiler is CUDA11.8 whereas
existing Torch is CUDA12.1. This is a fixed implementation choice, not adaptation.
Do not modify global CUDA installation. Final checkpoint SHA and smoke results
remain pending download and execution; no detector validity claim yet.

Equal 160-class budgets do not imply equal WordPiece counts. Record actual
Vhard/Vrand token lengths and common 1024 capacity in PLAN; never falsely label
them as equal realized token lengths. Both retain identical canonical prefix.

## Sources

- [Official native code](https://github.com/IDEA-Research/GroundingDINO/tree/856dde20aee659246248e20734ef9ba5214f5e44).
- [Official checkpoint](https://huggingface.co/IDEA-Research/grounding-dino-tiny/tree/a2bb814dd30d776dcf7e30523b00659f4f141c71).
- [Transformers implementation](https://github.com/huggingface/transformers/blob/v4.44.2/src/transformers/models/grounding_dino/modeling_grounding_dino.py).
- [Pinned BERT vocabulary](https://huggingface.co/google-bert/bert-base-uncased/blob/86b5e0934494bd15c9632b12f734a8a67f723594/vocab.txt), SHA256
  `07eced375cec144d27c900241f3e339478dec958f92fddbc551f295c992038a3`.
- COCO names from Detectron2 `builtin_meta.py` (text metadata only, not annotations).
  Exact names and source hashes are retained in probe_sources and receipts.
- Grounding DINO native README reports 48.5 full-COCO mAP for its Swin-T example
  (model table 48.4); do not use the larger model's 52.5 figure as this baseline.

## Infrastructure

Existing project: `/home/wenchang/asdasdsad/wjq/TOVD`; shared initially empty.
Bounded searches of wjq, models, datasets and user Hugging Face caches did not
locate reusable COCO2017-val annotations or this checkpoint. This is not a claim
that no such files exist anywhere on the server. Public official downloads are
authorized and are stored under shared/t013, outside code releases.
Disk free about66GB. GPU1 free49,169,170,432 bytes at capacity check; CUDA works
despite existing NVML warning. No global driver changes or other jobs touched.

Local Python3.12.7, Torch2.13.0+cpu, tokenizers0.22.2. Remote diagnostic
Python3.12.12, Torch2.4.0+cu121, tokenizers0.22.2. Diagnostic-only tokenizers was
installed without dependencies into shared/t013_probe_deps, leaving original
venv unchanged. Real detector gets a separate shared/t013/venv.

The initial local AutoTokenizer cache lookup failed because BERT was not cached;
the documented public vocab download and direct WordPiece tokenizer resolved
this prerequisite. No primary run was attempted during this failure.

## Reproduction

```text
python research_log/t013/probe_text_capacity.py --sources research_log/t013/probe_sources --output capacity.json --torch-head [--device cuda]
```

Remote set PYTHONPATH to shared/t013_probe_deps and CUDA_VISIBLE_DEVICES=1.
Native donor sources and license are preserved verbatim in probe_sources.
No adaptation tests or synthetic experiments were rerun for this diagnostic.

## Literature boundary

Verified primary pages: [Vocabulary Adaptation](https://arxiv.org/abs/2506.00333)
studies vocabulary relevance; [ViTPrompt](https://openaccess.thecvf.com/content/CVPR2026/html/Qin_ViTPrompt_Training-Free_Prompt_Refinement_with_Visual_Tokens_for_Open-Vocabulary_Detection_CVPR_2026_paper.html)
refines prompts with visual tokens; [FACTOR](https://arxiv.org/abs/2605.03294)
studies counterfactual training-free adaptation; [PISA](https://arxiv.org/abs/2608.14142)
studies feature adaptation. T013 implements none of these methods. Its claim is
only a frozen real-detector interaction audit, with no literature-absence claim.
