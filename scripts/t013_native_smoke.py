"""Disjoint native-only engineering smoke, no AP or scientific gate outcomes."""
import argparse
import hashlib
import json
from pathlib import Path
import time

import numpy as np
from PIL import Image
import torch
from scripts.t013_native_detector import (
    CONDITIONS, corrupted_pixels, detect_native, load_native, preprocess, state_hash,
)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--assets', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    selection = json.loads(Path('research_log/t013/image_selection.json').read_text())
    vocab = json.loads(Path('research_log/t013/vocabulary_native30.json').read_text())
    assert not set(selection['smoke_ids']) & set(selection['primary_ids'])
    model, transform = load_native(args.assets)
    before = state_hash(model)
    text_receipts = []
    def check_text(module, inputs):
        text = inputs[6]
        length = text['encoded_text'].shape[1]
        assert length in (195, 255)
        assert list(text['text_token_mask'].shape) == [1, length]
        assert list(text['text_self_attention_masks'].shape) == [1, length, length]
        assert bool(text['text_token_mask'].all())
        text_receipts.append({'encoded_length': length, 'mask_length': length})
    handle = model.transformer.register_forward_pre_hook(check_text)
    records = []
    start = time.monotonic()
    for image_id in selection['smoke_ids']:
        image = Image.open(args.assets / 'smoke_images' / f'{image_id:012d}.jpg').convert('RGB')
        for condition in CONDITIONS:
            pixels = corrupted_pixels(image, image_id, condition)
            assert np.array_equal(pixels, corrupted_pixels(image, image_id, condition))
            pixel_hash = hashlib.sha256(pixels.tobytes()).hexdigest()
            for name, names in vocab['vocabularies'].items():
                mark = time.monotonic()
                raw = detect_native(model, transform, pixels, names)
                assert np.isfinite(raw['boxes']).all() and np.isfinite(raw['class_scores']).all()
                assert text_receipts[-1]['encoded_length'] == vocab['token_counts'][name]
                if condition == 'clean':
                    repeated = detect_native(model, transform, pixels, names)
                    assert all(np.array_equal(raw[key], repeated[key]) for key in raw)
                    if name == 'V0':
                        with torch.inference_mode():
                            direct = model(preprocess(transform, pixels)[None], captions=[vocab['prompts']['V0']])
                        assert np.array_equal(raw['normalized_cxcywh'], direct['pred_boxes'][0].numpy())
                        assert np.array_equal(raw['token_logits'], direct['pred_logits'][0, :, :195].numpy())
                records.append({'image_id': image_id, 'condition': condition, 'vocabulary': name,
                                'pixel_sha256': pixel_hash, 'seconds': time.monotonic() - mark,
                                'token_length': text_receipts[-1]['encoded_length']})
                print(json.dumps(records[-1]), flush=True)
    handle.remove()
    after = state_hash(model)
    assert before == after and all(p.grad is None and not p.requires_grad for p in model.parameters())
    receipt = {'validity': True, 'kind': 'native30_disjoint_smoke', 'device': 'cpu', 'threads': 4,
               'state_before': before, 'state_after': after, 'native_V0_wrapper_identity': True,
               'clean_all_vocab_replay_exact': True, 'pixel_replay_and_vocab_independence': True,
               'native_text_no_truncation': True, 'records': records,
               'seconds': time.monotonic() - start, 'torch_version': torch.__version__}
    args.output.write_text(json.dumps(receipt, indent=2) + '\n')
    print('Native30 smoke PASS', flush=True)


if __name__ == '__main__':
    main()
