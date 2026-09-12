from collections import Counter
import json
from pathlib import Path

import pytest
from tokenizers import Tokenizer

from scripts.t013_match_vocabulary import matched_unrelated
from scripts.t013_text import caption_and_spans


ROOT = Path(__file__).resolve().parents[1] / "research_log/t013"


def test_frozen_real_scores_exact_token_bins_and_deterministic_lowest_selection():
    frozen = json.loads((ROOT / "frozen_r3_vocabulary.json").read_text())
    tokenizer = Tokenizer.from_file(str(ROOT / "tokenizer.json"))
    selected, lengths, audit = matched_unrelated(frozen, tokenizer)
    assert selected == matched_unrelated(frozen, tokenizer)[0]
    assert len(selected) == len({row["id"] for row in selected}) == 80
    hard_ids = {row["id"] for row in frozen["Vhard_rows"]}
    assert not hard_ids & {row["id"] for row in selected}
    assert Counter(lengths[row["id"]] for row in selected) == Counter(lengths[row["id"]] for row in frozen["Vhard_rows"])
    for bin_row in audit:
        pool = sorted([row for row in frozen["ranked_candidates"] if row["id"] not in hard_ids
                       and lengths[row["id"]] == bin_row["token_contribution"]], key=lambda row: (row["similarity"], row["id"]))
        assert bin_row["selected_ids"] == [row["id"] for row in pool[:bin_row["required"]]]
    text = caption_and_spans(frozen["vocabularies"]["V0"] + [row["name"] for row in selected])[0]
    assert len(tokenizer.encode(text).ids) == frozen["token_counts"]["Vhard"] == 408


def test_infeasible_bin_stops_without_relaxation():
    tokenizer = Tokenizer.from_file(str(ROOT / "tokenizer.json"))
    row = {"id": 1, "name": "mug", "similarity": .9}
    with pytest.raises(ValueError, match="Infeasible"):
        matched_unrelated({"ranked_candidates": [row], "Vhard_rows": [row]}, tokenizer)
