"""Text-only T013 vocabulary construction utilities; no detection dependencies."""
import re
import unicodedata

import numpy as np


# Explicit text-only aliases, fixed before embeddings or detector outcomes.
COCO_ALIASES = {
    "automobile", "auto", "motorbike", "motor cycle", "aeroplane", "sofa",
    "television", "television set", "tv set", "cellular telephone", "cellphone",
    "mobile phone", "mobile telephone", "hairdryer", "hair dryer", "microwave oven",
    "teddy", "teddybear", "baseball glove", "fridge", "potted plant",
    "dining room table", "stop sign", "traffic signal", "sports ball", "ball",
    "remote control", "wineglass", "hotdog", "ski", "laptop computer",
    "notebook computer", "racket",
}


def normalize(name):
    name = unicodedata.normalize("NFKC", name).lower().replace("_", " ")
    return " ".join(re.sub(r"[^a-z0-9]+", " ", name).split())


def candidates(lvis, canonical):
    equivalents = {normalize(n) for n in canonical} | COCO_ALIASES
    seen = set()
    kept, excluded = [], []
    for item in sorted(lvis, key=lambda row: row["id"]):
        name = item["name"].replace("_", " ").lower()
        norm = normalize(name)
        aliases = {normalize(n) for n in [name, *item["synonyms"]]}
        aliases |= {normalize(re.sub(r"\([^)]*\)", "", n))
                    for n in [name, *item["synonyms"]]}
        matches = sorted(aliases & equivalents)
        if matches or norm in seen:
            excluded.append({"id": item["id"], "name": name,
                             "reason": "coco_alias" if matches else "duplicate_normalized",
                             "matched_aliases": matches})
        else:
            kept.append({"id": item["id"], "name": name, "normalized": norm,
                         "synset": item["synset"]})
            seen.add(norm)
    return kept, excluded


def caption_and_spans(names):
    """Exact official COCO syntax for these lower-case, non-slash class names."""
    caption = ""
    spans = []
    for name in names:
        words = name.lower().split()
        positions = []
        for word in words:
            if caption:
                caption += " "
            start = len(caption)
            caption += word
            positions.append((start, len(caption)))
        caption += " ."
        spans.append(positions)
    return caption, spans


def positive_map(offsets, spans, capacity=1024):
    """Reuse upstream mean-of-class-token probabilities (including 1e-6 divisor)."""
    result = np.zeros((len(spans), capacity), dtype=np.float32)
    for row, words in enumerate(spans):
        for start, end in words:
            indices = [i for i, (a, b) in enumerate(offsets) if a < end and b > start]
            if not indices or max(indices) >= capacity:
                raise ValueError("Class text is missing or exceeds frozen text capacity")
            result[row, indices] = 1
    return result / (result.sum(axis=1, keepdims=True) + 1e-6)


def rank_candidates(rows, coco_embeddings, candidate_embeddings):
    # Float64 cosine scoring, deterministic ID tie breaking; embeddings themselves
    # are the frozen BERT output, computed once and archived before detection.
    coco = np.asarray(coco_embeddings, dtype=np.float64)
    other = np.asarray(candidate_embeddings, dtype=np.float64)
    coco = coco / np.linalg.norm(coco, axis=1, keepdims=True)
    other = other / np.linalg.norm(other, axis=1, keepdims=True)
    similarities = other @ coco.T
    ranked = [dict(row, similarity=float(scores.max()),
                   nearest_coco_index=int(scores.argmax()))
              for row, scores in zip(rows, similarities)]
    hard = sorted(ranked, key=lambda row: (-row["similarity"], row["id"]))[:80]
    unrelated = sorted(ranked, key=lambda row: (row["similarity"], row["id"]))[:80]
    # Retain the ranking order, identical canonical prefix, no outcome-based order.
    return ranked, hard, unrelated
