"""Non-primary validity only. Requires frozen vocabulary and disjoint smoke IDs."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image
import torch

from scripts.t013_detector import CONDITIONS, corrupted_pixels, detect, load_detector, state_hash


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--assets", type=Path, required=True)
    parser.add_argument("--vocabulary", type=Path, required=True)
    parser.add_argument("--selection", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--images", type=Path)
    args = parser.parse_args()
    vocab = json.loads(args.vocabulary.read_text())["vocabularies"]
    selection = json.loads(args.selection.read_text())
    assert not set(selection["smoke_ids"]) & set(selection["primary_ids"])
    assert len(vocab["V0"]) == 80
    for key in ["Vhard", "Vrand"]:
        assert vocab[key][:80] == vocab["V0"]
        assert len(vocab[key]) == len(set(vocab[key])) == 160
    processor, model = load_detector(args.assets / "model", args.device)
    before = state_hash(model)
    records = []
    for image_id in selection["smoke_ids"]:
        image_root = args.images if args.images is not None else args.assets / "coco/val2017"
        image = Image.open(image_root / f"{image_id:012d}.jpg").convert("RGB")
        standalone = detect(processor, model, np.array(image), vocab["V0"])
        for condition in CONDITIONS:
            pixels = corrupted_pixels(image, image_id, condition)
            assert np.array_equal(pixels, corrupted_pixels(image, image_id, condition))
            for key, names in vocab.items():
                result = detect(processor, model, pixels, names)
                assert np.isfinite(result["boxes"]).all() and np.isfinite(result["class_scores"]).all()
                if condition == "clean" and key == "V0":
                    assert all(np.array_equal(value, standalone[name]) for name, value in result.items())
                records.append({"image_id": image_id, "condition": condition, "vocabulary": key,
                                "pixel_sha256": hashlib.sha256(pixels.tobytes()).hexdigest(),
                                "mean_top_score": float(result["top_scores"].mean())})
        # Shared-capacity repair must preserve original V0 outputs exactly.
        model.config.max_text_len = 256
        for module in model.modules():
            if hasattr(module, "max_text_len"):
                module.max_text_len = 256
        original_capacity = detect(processor, model, np.array(image), vocab["V0"])
        assert all(np.array_equal(value, standalone[name]) for name, value in original_capacity.items())
        model.config.max_text_len = 1024
        for module in model.modules():
            if hasattr(module, "max_text_len"):
                module.max_text_len = 1024
    assert state_hash(model) == before
    assert all(p.grad is None and not p.requires_grad for p in model.parameters())
    receipt = {"kind": "nonprimary_engineering_smoke", "validity": True,
               "v0_256_vs_1024_exact": True, "v0_standalone_vs_common_exact": True,
               "pixels_replay_exact": True, "weights_unchanged": True,
               "state_sha256": before, "torch": torch.__version__, "device": args.device,
               "records": records}
    args.output.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({k: v for k, v in receipt.items() if k != "records"}))


if __name__ == "__main__":
    main()
