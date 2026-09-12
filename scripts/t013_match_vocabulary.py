"""Lead's token-stratified Vrand repair using frozen scores; no embeddings/inference."""
import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path

from tokenizers import Tokenizer
from scripts.t013_text import caption_and_spans


def matched_unrelated(frozen, tokenizer):
    rows = frozen["ranked_candidates"]
    hard = frozen["Vhard_rows"]
    hard_ids = {row["id"] for row in hard}
    special_count = len(tokenizer.encode("").ids)
    lengths = {row["id"]: len(tokenizer.encode(caption_and_spans([row["name"]])[0]).ids) - special_count
               for row in rows}
    required = Counter(lengths[row["id"]] for row in hard)
    selected, audit = [], []
    for length, count in sorted(required.items()):
        eligible = sorted([row for row in rows if row["id"] not in hard_ids and lengths[row["id"]] == length],
                          key=lambda row: (row["similarity"], row["id"]))
        if len(eligible) < count:
            raise ValueError(f"Infeasible token bin {length}: required {count}, eligible {len(eligible)}")
        selected.extend(eligible[:count])
        audit.append({"token_contribution": length, "required": count, "eligible": len(eligible),
                      "selected_ids": [row["id"] for row in eligible[:count]]})
    selected.sort(key=lambda row: (row["similarity"], row["id"]))
    assert Counter(lengths[row["id"]] for row in selected) == required
    return selected, lengths, audit


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--frozen", type=Path, required=True)
    parser.add_argument("--tokenizer", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    original = json.loads(args.frozen.read_text())
    tokenizer = Tokenizer.from_file(str(args.tokenizer))
    selected, lengths, audit = matched_unrelated(original, tokenizer)
    output = deepcopy(original)
    output["Vrand_rows"] = selected
    output["vocabularies"]["Vrand"] = output["vocabularies"]["V0"] + [row["name"] for row in selected]
    output["prompts"]["Vrand"] = caption_and_spans(output["vocabularies"]["Vrand"])[0]
    output["token_counts"] = {key: len(tokenizer.encode(text).ids) for key, text in output["prompts"].items()}
    assert output["token_counts"]["Vrand"] == output["token_counts"]["Vhard"]
    assert output["Vhard_rows"] == original["Vhard_rows"]
    # Old full-prompt encoder evidence applies to the original Vrand only; do not
    # misattribute it to this newly selected control. No re-embedding is performed.
    output["r3_full_prompt_encoder_checks"] = output.pop("full_prompt_encoder_checks")
    output["token_match_amendment"] = {
        "research_lead_commit": "2c4dbf5", "frozen_source_sha256": hashlib.sha256(args.frozen.read_bytes()).hexdigest(),
        "tokenizer_sha256": hashlib.sha256(args.tokenizer.read_bytes()).hexdigest(),
        "candidate_scores_unchanged": True, "Vhard_unchanged": True, "reembedded": False,
        "bins": audit, "per_candidate_token_contributions": lengths,
        "ordering": "ascending frozen similarity, then ascending LVIS ID",
    }
    args.output.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"token_counts": output["token_counts"], "bin_audit": audit,
                      "sha256": hashlib.sha256(args.output.read_bytes()).hexdigest()}, indent=2))


if __name__ == "__main__":
    main()
