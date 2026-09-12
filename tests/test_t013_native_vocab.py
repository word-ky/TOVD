import json
from pathlib import Path
from tokenizers import Tokenizer
from scripts.t013_native_vocab import build


def test_native30_exact_frozen_subsequence_and_control():
    root = Path('research_log/t013')
    frozen = json.loads((root / 'vocabulary_matched.json').read_text())
    tokenizer = Tokenizer.from_file(str(root / 'tokenizer.json'))
    result = build(frozen, tokenizer)
    lengths = frozen['token_match_amendment']['per_candidate_token_contributions']
    assert result['Vhard30_rows'] == [r for r in frozen['Vhard_rows'] if lengths[str(r['id'])] == 2]
    assert result['Vrand30_rows'] == [r for r in frozen['Vrand_rows'] if lengths[str(r['id'])] == 2]
    assert result == build(frozen, tokenizer)
    assert result['token_counts'] == {'V0': 195, 'Vhard30': 255, 'Vrand30': 255}
