"""Native30 primary inference only: reads frozen IDs/images, never annotations."""
import argparse
import hashlib
import json
from pathlib import Path
import time

import numpy as np
from PIL import Image

from scripts.t013_native_detector import CONDITIONS, corrupted_pixels, detect_native, load_native, state_hash


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--assets', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--freeze-commit', required=True)
    p.add_argument('--smoke-only', action='store_true')
    args = p.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    vocab_path = Path('research_log/t013/vocabulary_native30.json')
    selection_path = Path('research_log/t013/image_selection.json')
    vocab = json.loads(vocab_path.read_text())['vocabularies']
    selection = json.loads(selection_path.read_text())
    ids = selection['smoke_ids'] if args.smoke_only else selection['primary_ids']
    images = args.assets / ('smoke_images' if args.smoke_only else 'coco/val2017')
    expected_images = None
    if not args.smoke_only:
        freeze = json.loads(Path('research_log/t013/native30_freeze.json').read_text())
        for path, digest in freeze['code_sha256'].items():
            assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest, path
        assert hashlib.sha256(vocab_path.read_bytes()).hexdigest() == freeze['vocabulary_sha256']
        assert hashlib.sha256(selection_path.read_bytes()).hexdigest() == freeze['selection_sha256']
        expected_images = json.loads(Path('research_log/t013/image_sha256.json').read_text())
    model, transform = load_native(args.assets)
    before = state_hash(model)
    if not args.smoke_only:
        assert before == freeze['native_state_sha256']
    receipt = {'kind': 'smoke_cached_pipeline' if args.smoke_only else 'T013-NATIVE30-primary',
               'freeze_commit': args.freeze_commit, 'image_ids': ids, 'device': 'cpu', 'threads': 4,
               'vocabulary_sha256': hashlib.sha256(vocab_path.read_bytes()).hexdigest(),
               'selection_sha256': hashlib.sha256(selection_path.read_bytes()).hexdigest(),
               'state_before': before, 'records': []}
    (args.output / 'run_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    start = time.monotonic()
    for index, image_id in enumerate(ids):
        image_path = images / f'{image_id:012d}.jpg'
        image = Image.open(image_path).convert('RGB')
        image_hash = hashlib.sha256(image_path.read_bytes()).hexdigest()
        if expected_images is not None:
            assert image_hash == expected_images[image_path.name], image_path
        for condition in CONDITIONS:
            pixels = corrupted_pixels(image, image_id, condition)
            pixel_hash = hashlib.sha256(pixels.tobytes()).hexdigest()
            for name, names in vocab.items():
                raw = detect_native(model, transform, pixels, names)
                destination = args.output / 'raw' / condition / name
                destination.mkdir(parents=True, exist_ok=True)
                file = destination / f'{image_id:012d}.npz'
                np.savez_compressed(file, **raw)
                record = {'image_id': image_id, 'condition': condition, 'vocabulary': name,
                          'image_sha256': image_hash, 'pixel_sha256': pixel_hash,
                          'raw_path': str(file.relative_to(args.output)),
                          'raw_sha256': hashlib.sha256(file.read_bytes()).hexdigest()}
                receipt['records'].append(record)
                with (args.output / 'cache_manifest.jsonl').open('a') as out:
                    out.write(json.dumps(record) + '\n')
        print(json.dumps({'completed_images': index + 1, 'total_images': len(ids),
                          'seconds': time.monotonic() - start}), flush=True)
    after = state_hash(model)
    assert before == after
    receipt.update(state_after=after, weights_unchanged=True, completed=True,
                   code_vocab_selection_images_verified=not args.smoke_only,
                   seconds=time.monotonic() - start)
    (args.output / 'run_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')


if __name__ == '__main__':
    main()
