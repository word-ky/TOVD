"""Freeze T013 distractors using only category text and frozen detector BERT."""
import argparse
import json
from pathlib import Path

import numpy as np
import torch
from transformers.models.grounding_dino.modeling_grounding_dino import (
    generate_masks_with_special_tokens_and_transfer_map,
)

from scripts.t013_text import candidates, caption_and_spans, rank_candidates
from scripts.t013_detector import load_detector, state_hash


@torch.inference_mode()
def embed_names(model, tokenizer, names, device):
    vectors = []
    # Single isolated phrase: no padding-length-dependent attention or other names.
    for name in names:
        caption, spans = caption_and_spans([name])
        encoded = tokenizer(caption, return_tensors="pt", return_offsets_mapping=True)
        offsets = encoded.pop("offset_mapping")[0].tolist()
        selected = sorted({i for start, end in spans[0]
                           for i, (a, b) in enumerate(offsets) if a < end and b > start})
        encoded = encoded.to(device)
        mask, position = generate_masks_with_special_tokens_and_transfer_map(encoded.input_ids)
        output = model.model.text_backbone(
            input_ids=encoded.input_ids, attention_mask=mask,
            token_type_ids=encoded.token_type_ids, position_ids=position,
        ).last_hidden_state
        vectors.append(output[0, selected].mean(dim=0).cpu().numpy())
    return np.stack(vectors)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--device", default="cuda")
    args = parser.parse_args()
    torch.set_num_threads(4)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    root = Path("research_log/t013")
    canonical = [r["name"] for r in json.loads((root / "probe_sources/coco80.json").read_text())]
    rows, excluded = candidates(json.loads((root / "lvis_categories.json").read_text()), canonical)
    processor, model = load_detector(args.model, args.device)
    tokenizer = processor.tokenizer
    before = state_hash(model)
    coco_vectors = embed_names(model, tokenizer, canonical, args.device)
    candidate_vectors = embed_names(model, tokenizer, [r["name"] for r in rows], args.device)
    ranked, hard, unrelated = rank_candidates(rows, coco_vectors, candidate_vectors)
    vocabularies = {"V0": canonical, "Vhard": canonical + [r["name"] for r in hard],
                    "Vrand": canonical + [r["name"] for r in unrelated]}
    prompts = {key: caption_and_spans(names)[0] for key, names in vocabularies.items()}
    token_counts = {key: len(tokenizer(text).input_ids) for key, text in prompts.items()}
    assert max(token_counts.values()) <= 1024
    full_prompt_checks = {}
    with torch.inference_mode():
        for key, text in prompts.items():
            encoded = tokenizer(text, return_tensors="pt").to(args.device)
            mask, position = generate_masks_with_special_tokens_and_transfer_map(encoded.input_ids)
            output = model.model.text_backbone(
                input_ids=encoded.input_ids, attention_mask=mask,
                token_type_ids=encoded.token_type_ids, position_ids=position,
            ).last_hidden_state
            assert output.shape[1] == token_counts[key] and torch.isfinite(output).all()
            full_prompt_checks[key] = {"input_tokens": token_counts[key],
                                       "output_tokens": int(output.shape[1]),
                                       "max_sentence_position_id": int(position.max())}
    assert state_hash(model) == before
    assert all(p.grad is None for p in model.parameters())
    args.output.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(args.output / "text_embeddings.npz", coco=coco_vectors, candidates=candidate_vectors)
    result = {"vocabularies": vocabularies, "prompts": prompts, "token_counts": token_counts,
              "max_text_len": 1024, "ranked_candidates": ranked, "Vhard_rows": hard,
              "Vrand_rows": unrelated, "excluded": excluded, "model_state_sha256": before,
              "embedding": "mean phrase-token last-layer detector BERT, detector sentence masks/position IDs; 768d",
              "scoring": "float64 normalized cosine, max over COCO80; similarity then ascending LVIS ID ties",
              "no_image_or_annotation_inputs": True, "weights_unchanged": True}
    result["full_prompt_encoder_checks"] = full_prompt_checks
    (args.output / "vocabulary.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"candidate_count": len(rows), "excluded_count": len(excluded),
                      "token_counts": token_counts, "state_sha256": before}))


if __name__ == "__main__":
    main()
