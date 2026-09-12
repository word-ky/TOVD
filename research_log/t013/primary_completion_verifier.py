"""FIN1: frozen cache metadata and opaque-byte integrity; standard library only."""
import argparse
import ast
import hashlib
import json
from pathlib import Path

FREEZE_COMMIT = '6fec32243985ccc808123d851abf5f3dea10af99'
FREEZE_SHA256 = '50addfb8e247333b49fb22cda14570166b294101bb435b5a1b5bf688b4b3a91e'
PRIMARY_RUN = '20260912-210355-tovd-native30-primary'
PRIMARY_RELEASE = '20260912-210306-tovd-native30-primary-freeze'
SMOKE_RUN = '20260912-205428-tovd-native30-pipeline-smoke'
SMOKE_RELEASE = '20260912-205335-tovd-native30-pipeline'
SMOKE_COMMIT_ARGUMENT = 'd5dc807'


def require(condition, check):
    if not condition:
        raise ValueError(check)


def sha256(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def frozen_contract(root, smoke=False):
    """Read pinned source/metadata, never import the frozen detector or runner."""
    root = Path(root)
    hashes = {}

    def read(relative, expected):
        # Git checkout may use CRLF on Windows; frozen source/JSON blobs use LF.
        data = (root / relative).read_bytes().replace(b'\r\n', b'\n')
        digest = hashlib.sha256(data).hexdigest()
        require(digest == expected, 'frozen_source_hash:' + relative)
        hashes[relative] = digest
        return data.decode('utf-8')

    prefix = 'research_log/t013/'
    freeze = json.loads(read(prefix + 'native30_freeze.json', FREEZE_SHA256))
    selection = json.loads(read(prefix + 'image_selection.json', freeze['selection_sha256']))
    vocabulary = json.loads(read(prefix + 'vocabulary_native30.json', freeze['vocabulary_sha256']))
    images = json.loads(read(prefix + 'image_sha256.json', freeze['image_manifest_sha256']))
    for name in ('scripts/t013_native_run.py', 'scripts/t013_native_detector.py'):
        read(name, freeze['code_sha256'][name])
    source = read('scripts/t013_detector.py', freeze['code_sha256']['scripts/t013_detector.py'])
    assignment = next(n for n in ast.parse(source).body if isinstance(n, ast.Assign)
                      and any(isinstance(t, ast.Name) and t.id == 'CONDITIONS' for t in n.targets))
    conditions = ast.literal_eval(assignment.value)
    ids = selection['smoke_ids' if smoke else 'primary_ids']
    vocabs = list(vocabulary['vocabularies'])
    expected = {(i, c, v) for i in ids for c in conditions for v in vocabs}
    require(len(ids) == (3 if smoke else 1000) and len(expected) == (45 if smoke else 15000), 'expected_key_count')
    return {'ids': ids, 'conditions': conditions, 'vocabularies': vocabs, 'expected': expected,
            'image_hashes': images, 'vocabulary_sha256': freeze['vocabulary_sha256'],
            'selection_sha256': freeze['selection_sha256'], 'state_sha256': freeze['native_state_sha256'],
            'source_hashes': hashes, 'smoke': smoke,
            'kind': 'smoke_cached_pipeline' if smoke else 'T013-NATIVE30-primary',
            'freeze_argument': SMOKE_COMMIT_ARGUMENT if smoke else FREEZE_COMMIT,
            'run_id': SMOKE_RUN if smoke else PRIMARY_RUN,
            'release_id': SMOKE_RELEASE if smoke else PRIMARY_RELEASE}


def key(row):
    return row['image_id'], row['condition'], row['vocabulary']


def record_map(rows, expected, label):
    result = {}
    paths = set()
    for row in rows:
        k = key(row)
        require(k not in result, label + ':duplicate_key')
        require(k in expected, label + ':unexpected_key')
        image_id, condition, vocab = k
        require(row['raw_path'] == f'raw/{condition}/{vocab}/{image_id:012d}.npz', label + ':raw_path')
        require(row['raw_path'] not in paths, label + ':duplicate_raw_path')
        result[k] = row
        paths.add(row['raw_path'])
    require(set(result) == expected, label + ':missing_key')
    return result


def verify(cache, contract):
    """Call only after completion. No writes, array readers or analysis-content reads."""
    cache = Path(cache)
    artifacts, run = cache.parent, cache.parent.parent
    meta = json.loads((run / 'meta.json').read_text())
    resolved = (artifacts / 'resolved_release.txt').read_text().strip()
    require(run.name == contract['run_id'] and meta['runId'] == contract['run_id'], 'run_id')
    require(meta['releaseId'] == contract['release_id'] and
            resolved.rsplit('/', 1)[-1] == contract['release_id'], 'release_id')
    receipt = json.loads((cache / 'run_receipt.json').read_text())
    require(receipt['completed'] is True, 'completed')
    require(receipt['kind'] == contract['kind'], 'kind')
    require(receipt['freeze_commit'] == contract['freeze_argument'], 'freeze_commit')
    require(receipt['image_ids'] == contract['ids'], 'ordered_image_ids')
    require(receipt['device'] == 'cpu' and receipt['threads'] == 4, 'device_threads')
    require(receipt['weights_unchanged'] is True, 'weights_unchanged')
    require(receipt['code_vocab_selection_images_verified'] is (not contract['smoke']), 'code_vocab_selection_images_verified')
    require(receipt['state_before'] == receipt['state_after'] == contract['state_sha256'], 'state_hash')
    for field in ('vocabulary_sha256', 'selection_sha256'):
        require(receipt[field] == contract[field], field)
    manifest_path = cache / 'cache_manifest.jsonl'
    rows = [json.loads(line) for line in manifest_path.read_text().splitlines()]
    manifest = record_map(rows, contract['expected'], 'manifest')
    final = record_map(receipt['records'], contract['expected'], 'receipt')
    require(final == manifest, 'receipt_manifest_records')
    pixels = {}
    for k, row in manifest.items():
        image_id, condition, _ = k
        require(row['image_sha256'] == contract['image_hashes'][f'{image_id:012d}.jpg'], 'image_sha256')
        pixels.setdefault((image_id, condition), []).append(row['pixel_sha256'])
    require(all(len(hashes) == 3 and len(set(hashes)) == 1 for hashes in pixels.values()), 'shared_pixel_sha256')
    total = 0
    for k in sorted(manifest):
        row = manifest[k]
        path = cache / row['raw_path']
        require(path.is_file(), 'raw_file_missing:' + row['raw_path'])
        size = path.stat().st_size
        require(size > 0, 'raw_file_empty:' + row['raw_path'])
        require(sha256(path) == row['raw_sha256'], 'raw_sha256:' + row['raw_path'])
        total += size
    return {'status': 'PASS', 'mode': 'engineering_smoke' if contract['smoke'] else 'primary',
            'scientific_freeze_commit': FREEZE_COMMIT, 'receipt_freeze_argument': contract['freeze_argument'],
            'run_id': contract['run_id'], 'release_id': contract['release_id'],
            'image_count': len(contract['ids']), 'expected_records': len(contract['expected']),
            'manifest_unique_records': len(manifest), 'receipt_unique_records': len(final),
            'opaque_files_verified': len(manifest), 'raw_bytes': total,
            'shared_pixel_groups': len(pixels), 'state_sha256': contract['state_sha256'],
            'source_hashes': contract['source_hashes'],
            'manifest_sha256': sha256(manifest_path), 'run_receipt_sha256': sha256(cache / 'run_receipt.json'),
            'analysis_result_exists': (artifacts / 'analysis/results.json').is_file(),
            'analysis_content_opened': False, 'npz_deserialized': False,
            'scope': 'metadata and opaque file bytes only; no scientific acceptance'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--frozen-root', type=Path, required=True)
    parser.add_argument('--cache', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--smoke', action='store_true', help='Only the pinned completed 45-cell engineering smoke')
    args = parser.parse_args()
    try:
        result = verify(args.cache, frozen_contract(args.frozen_root, args.smoke))
    except (ValueError, KeyError, OSError) as error:
        result = {'status': 'FAIL', 'error_type': type(error).__name__, 'error': str(error),
                  'npz_deserialized': False, 'analysis_content_opened': False}
    args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result))
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
