"""Hash official extracted COCO images after the existing downloader passes CRC."""
import argparse
import hashlib
import json
from pathlib import Path


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--coco', type=Path, required=True)
    p.add_argument('--download-receipt', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    downloads = json.loads(args.download_receipt.read_text())
    assert len(downloads) == 2 and all(row['zip_crc_all_entries_passed'] for row in downloads)
    annotation = args.coco / 'annotations/instances_val2017.json'
    dataset = json.loads(annotation.read_text())
    images = {}
    for item in sorted(dataset['images'], key=lambda row: row['id']):
        file = args.coco / 'val2017' / item['file_name']
        images[file.name] = hashlib.sha256(file.read_bytes()).hexdigest()
    assert len(images) == 5000
    args.output.mkdir(parents=True, exist_ok=True)
    image_manifest = args.output / 'image_sha256.json'
    image_manifest.write_text(json.dumps(images, indent=2) + '\n', encoding='utf-8', newline='\n')
    receipt = {'downloads': downloads, 'image_count': len(images),
               'annotations_sha256': hashlib.sha256(annotation.read_bytes()).hexdigest(),
               'image_manifest_sha256': hashlib.sha256(image_manifest.read_bytes()).hexdigest()}
    (args.output / 'data_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt), flush=True)
