import json
from pathlib import Path

import numpy as np
import pytest

from scripts.t013_text import candidates, caption_and_spans, positive_map, rank_candidates


def test_official_caption_and_mapping():
    caption, spans = caption_and_spans(["person", "traffic light"])
    assert caption == "person . traffic light ."
    offsets = [(0, 0), (0, 6), (7, 8), (9, 16), (17, 22), (23, 24), (0, 0)]
    matrix = positive_map(offsets, spans, 8)
    assert np.allclose(matrix[0], [0, 1, 0, 0, 0, 0, 0, 0])
    assert np.allclose(matrix[1], [0, 0, 0, .5, .5, 0, 0, 0])
    with pytest.raises(ValueError, match="capacity"):
        positive_map(offsets, spans, 4)


def test_real_lvis_alias_filter_preserves_non_equivalent_subcategories():
    root = Path(__file__).resolve().parents[1] / "research_log/t013"
    lvis = json.loads((root / "lvis_categories.json").read_text())
    coco = [r["name"] for r in json.loads((root / "probe_sources/coco80.json").read_text())]
    kept, excluded = candidates(lvis, coco)
    assert len(kept) + len(excluded) == 1203
    names = {row["name"] for row in kept}
    assert not {"airplane", "sofa", "cellular telephone", "person", "laptop computer", "racket"} & names
    assert "sofa bed" in names
    assert len({r["normalized"] for r in kept}) == len(kept)


def test_ranking_ties_and_size_use_only_embeddings_and_ids():
    rows = [{"id": i, "name": str(i)} for i in range(160, 0, -1)]
    embeddings = np.array([[1., 0.]] * 80 + [[-1., 0.]] * 80)
    ranked, hard, unrelated = rank_candidates(rows, [[1., 0.]], embeddings)
    assert len(ranked) == 160 and len(hard) == len(unrelated) == 80
    assert hard[0]["id"] == 81 and unrelated[0]["id"] == 1
    assert hard[0]["similarity"] == 1 and unrelated[0]["similarity"] == -1
