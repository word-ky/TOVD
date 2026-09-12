"""Text-only prerequisite diagnostic; no images, annotations or detector weights.

Runs exact upstream caption builder via AST extraction, then the BERT WordPiece
tokenizer against canonical COCO names. Optional --torch-head runs the exact
upstream parameter-free contrastive head on dummy tensors. Not a detector run.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import platform

from tokenizers import BertWordPieceTokenizer
import tokenizers


def extracted(path, name):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    node = next(n for n in tree.body if getattr(n, "name", None) == name)
    return compile(ast.Module(body=[node], type_ignores=[]), str(path), "exec")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--torch-head", action="store_true")
    parser.add_argument("--device", default="cpu")
    args = parser.parse_args()
    src = args.sources
    categories = json.loads((src / "coco80.json").read_text())
    names = [c["name"] for c in categories]
    assert len(names) == len(set(names)) == 80
    namespace = {}
    exec(extracted(src / "vl_utils.py", "build_captions_and_token_span"), namespace)
    caption, spans = namespace["build_captions_and_token_span"](names, True)
    tokenizer = BertWordPieceTokenizer(str(src / "bert_vocab.txt"), lowercase=True)
    encoded = tokenizer.encode(caption)
    canonical_rows = []
    for name in names:
        indices = sorted({i for start, end in spans[name]
                          for i, (a, b) in enumerate(encoded.offsets)
                          if a < end and b > start})
        canonical_rows.append({"name": name, "token_indices": indices})
    # Any nonempty category needs >=1 token and the official separator needs 1.
    # This lower bound holds regardless of which eligible LVIS names are ranked.
    minimum_extended_tokens = len(encoded.ids) + 80 * 2
    assert max(i for r in canonical_rows for i in r["token_indices"]) < 256
    assert minimum_extended_tokens > 256
    model_tree = ast.parse((src / "groundingdino.py").read_text(encoding="utf-8"))
    cls = next(n for n in model_tree.body if isinstance(n, ast.ClassDef) and n.name == "GroundingDINO")
    constructor = next(n for n in cls.body if getattr(n, "name", None) == "__init__")
    hardcoded = [n for n in ast.walk(constructor) if isinstance(n, ast.Assign)
                 and any(isinstance(t, ast.Attribute) and t.attr == "max_text_len" for t in n.targets)]
    assert len(hardcoded) == 1 and ast.literal_eval(hardcoded[0].value) == 256
    result = {
        "kind": "text_capacity_prerequisite_only_not_detector_experiment",
        "python": platform.python_version(), "tokenizers": tokenizers.__version__,
        "upstream_commit": "856dde20aee659246248e20734ef9ba5214f5e44",
        "canonical_caption": caption, "canonical_tokens": encoded.tokens,
        "canonical_token_count": len(encoded.ids), "canonical_rows": canonical_rows,
        "extended_class_count": 160, "minimum_extended_token_count": minimum_extended_tokens,
        "configured_and_hardcoded_token_capacity": 256,
        "minimum_tokens_over_capacity": minimum_extended_tokens - 256,
        "canonical_names_all_fit": True,
        "all_80_appended_names_fit": False,
        "config_only_override_effective": False,
        "source_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sorted(src.iterdir()) if p.is_file()},
    }
    if args.torch_head:
        import torch
        import torch.nn as nn
        namespace = {"torch": torch, "nn": nn}
        exec(extracted(src / "utils.py", "ContrastiveEmbed"), namespace)
        head = namespace["ContrastiveEmbed"]().to(args.device)
        x = torch.zeros(1, 1, 4, device=args.device)
        def run(length):
            return head(x, {"encoded_text": torch.zeros(1, length, 4, device=args.device),
                            "text_token_mask": torch.ones(1, length, dtype=torch.bool, device=args.device)})
        assert list(run(256).shape) == [1, 1, 256]
        try:
            run(minimum_extended_tokens)
        except RuntimeError as exc:
            result["unmodified_head_extended_failure"] = str(exc)
        else:
            raise AssertionError("Expected fixed-capacity assignment to reject extended text")
        result["torch"] = torch.__version__
        result["device"] = args.device
        result["head_parameter_count"] = sum(p.numel() for p in head.parameters())
        result["head_256_test_passed"] = True
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k not in
                     {"canonical_caption", "canonical_tokens", "canonical_rows", "source_sha256"}}, indent=2))


if __name__ == "__main__":
    main()
