"""Lead T013-NATIVE30: selection exclusively from the frozen text table."""
import hashlib
import json
from pathlib import Path

from tokenizers import Tokenizer
from scripts.t013_text import caption_and_spans


def build(frozen, tokenizer):
    special = len(tokenizer.encode('').ids)
    length = lambda row: len(tokenizer.encode(caption_and_spans([row['name']])[0]).ids) - special
    hard = [row for row in frozen['Vhard_rows'] if length(row) == 2]
    assert len(hard) == 30
    excluded = {row['id'] for row in hard}
    eligible = sorted([row for row in frozen['ranked_candidates']
                       if row['id'] not in excluded and length(row) == 2],
                      key=lambda row: (row['similarity'], row['id']))
    if len(eligible) < 30:
        raise ValueError('Fewer than 30 eligible two-token unrelated candidates')
    rand = eligible[:30]
    canonical = frozen['vocabularies']['V0']
    vocab = {'V0': canonical, 'Vhard30': canonical + [r['name'] for r in hard],
             'Vrand30': canonical + [r['name'] for r in rand]}
    prompts = {key: caption_and_spans(names)[0] for key, names in vocab.items()}
    tokens = {key: len(tokenizer.encode(prompt).ids) for key, prompt in prompts.items()}
    assert list(tokens.values()) == [195, 255, 255]
    assert [len(set(names)) for names in vocab.values()] == [80, 110, 110]
    return {'task': 'T013-NATIVE30', 'vocabularies': vocab, 'prompts': prompts,
            'token_counts': tokens, 'Vhard30_rows': hard, 'Vrand30_rows': rand,
            'distractor_token_histograms': {'Vhard30': {'2': 30}, 'Vrand30': {'2': 30}},
            'eligible_random_count': len(eligible), 'reembedded': False,
            'selection': 'hard: preserve accepted hard80 two-token subsequence; random: lowest frozen similarity then ID'}


if __name__ == '__main__':
    folder = Path('research_log/t013')
    frozen = folder / 'vocabulary_matched.json'
    tokenizer = folder / 'tokenizer.json'
    result = build(json.loads(frozen.read_text()), Tokenizer.from_file(str(tokenizer)))
    result['source_sha256'] = hashlib.sha256(frozen.read_bytes()).hexdigest()
    result['tokenizer_sha256'] = hashlib.sha256(tokenizer.read_bytes()).hexdigest()
    output = folder / 'vocabulary_native30.json'
    output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(result['token_counts'], hashlib.sha256(output.read_bytes()).hexdigest())
