"""Deterministic FIN1 fixtures using tiny invalid-NPZ opaque bytes, no dependencies."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import tempfile
import sys
import unittest

from primary_completion_verifier import frozen_contract, verify

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OBSERVATIONS = []


class CompletionVerifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix='fin1_synthetic_', dir=HERE)
        cls.contract = frozen_contract(ROOT)
        cls.cache = Path(cls.temporary.name) / cls.contract['run_id'] / 'artifacts/cache'
        cls.cache.mkdir(parents=True)
        run = cls.cache.parent.parent
        (run / 'meta.json').write_text(json.dumps({'runId': cls.contract['run_id'], 'releaseId': cls.contract['release_id']}))
        (cls.cache.parent / 'resolved_release.txt').write_text('/synthetic/releases/' + cls.contract['release_id'])
        cls.rows = []
        for i, c, v in sorted(cls.contract['expected']):
            relative = f'raw/{c}/{v}/{i:012d}.npz'
            path = cls.cache / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            data = f'FIN1 opaque fixture {i} {c} {v}'.encode()
            path.write_bytes(data)  # Deliberately not a ZIP/NPZ; passing proves no NPZ parser is required.
            cls.rows.append({'image_id': i, 'condition': c, 'vocabulary': v, 'raw_path': relative,
                             'raw_sha256': hashlib.sha256(data).hexdigest(),
                             'image_sha256': cls.contract['image_hashes'][f'{i:012d}.jpg'],
                             'pixel_sha256': hashlib.sha256(f'{i}:{c}'.encode()).hexdigest()})
        cls.receipt = {'kind': cls.contract['kind'], 'freeze_commit': cls.contract['freeze_argument'],
                       'image_ids': cls.contract['ids'], 'device': 'cpu', 'threads': 4,
                       'completed': True, 'weights_unchanged': True, 'code_vocab_selection_images_verified': True,
                       'state_before': cls.contract['state_sha256'], 'state_after': cls.contract['state_sha256'],
                       'vocabulary_sha256': cls.contract['vocabulary_sha256'], 'selection_sha256': cls.contract['selection_sha256'],
                       'records': cls.rows}
        cls.write(cls.rows, cls.receipt)

    @classmethod
    def write(cls, rows, receipt):
        (cls.cache / 'cache_manifest.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows))
        (cls.cache / 'run_receipt.json').write_text(json.dumps(receipt))

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()  # Removes only this project-local generated temporary fixture tree.

    def tearDown(self):
        self.write(self.rows, self.receipt)

    def reject(self, name, rows=None, receipt=None, error=''):
        self.write(self.rows if rows is None else rows, self.receipt if receipt is None else receipt)
        with self.assertRaises(ValueError) as caught:
            verify(self.cache, self.contract)
        self.assertTrue(str(caught.exception).startswith(error), str(caught.exception))
        OBSERVATIONS.append({'fixture': name, 'expected': 'REJECT', 'status': 'PASS', 'observed_error': str(caught.exception)})

    def test_01_full_primary_contract_deterministic_and_analysis_independent(self):
        a = verify(self.cache, self.contract)
        b = verify(self.cache, self.contract)
        self.assertEqual(a, b)
        self.assertEqual(a['opaque_files_verified'], 15000)
        self.assertEqual(a['shared_pixel_groups'], 5000)
        path = self.cache.parent / 'analysis/results.json'
        path.parent.mkdir()
        path.write_text('Deliberately invalid JSON: never open scientific results.')
        c = verify(self.cache, self.contract)
        self.assertTrue(c.pop('analysis_result_exists'))
        a.pop('analysis_result_exists')
        self.assertEqual(a, c)
        path.unlink()
        OBSERVATIONS.append({'fixture': 'full_15000_cell_positive_and_repeat', 'status': 'PASS',
                             'expected': 'PASS', 'deterministic': True, 'invalid_npz_bytes_accepted': True,
                             'invalid_analysis_json_not_opened': True, 'verification': b})

    def test_02_missing_cell(self):
        self.reject('missing_cell', rows=self.rows[1:], error='manifest:missing_key')

    def test_03_duplicate_key(self):
        self.reject('duplicate_key', rows=self.rows+[self.rows[0]], error='manifest:duplicate_key')

    def test_04_tampered_raw_bytes(self):
        path = self.cache / self.rows[0]['raw_path']; original = path.read_bytes()
        try:
            path.write_bytes(original+b'TAMPER')
            self.reject('tampered_raw_bytes', error='raw_sha256:')
        finally:
            path.write_bytes(original)

    def test_05_shared_pixel_mismatch(self):
        rows = deepcopy(self.rows); rows[0]['pixel_sha256'] = '0'*64
        r = deepcopy(self.receipt); r['records'] = rows
        self.reject('shared_pixel_mismatch', rows=rows, receipt=r, error='shared_pixel_sha256')

    def test_06_wrong_freeze_commit(self):
        r = deepcopy(self.receipt); r['freeze_commit'] = 'wrong'
        self.reject('wrong_freeze_commit', receipt=r, error='freeze_commit')

    def test_07_wrong_state(self):
        r = deepcopy(self.receipt); r['state_after'] = '0'*64
        self.reject('wrong_state_after', receipt=r, error='state_hash')
        r['state_before'] = '0'*64
        self.reject('unchanged_but_wrong_state', receipt=r, error='state_hash')

    def test_08_incomplete(self):
        r = deepcopy(self.receipt); r['completed'] = False
        self.reject('completed_false', receipt=r, error='completed')

    def test_09_wrong_image_hash(self):
        rows = deepcopy(self.rows); rows[0]['image_sha256'] = '0'*64
        r = deepcopy(self.receipt); r['records'] = rows
        self.reject('wrong_image_hash', rows=rows, receipt=r, error='image_sha256')

    def test_10_receipt_omission_and_hash_disagreement(self):
        r = deepcopy(self.receipt); r['records'] = r['records'][1:]
        self.reject('receipt_omission', receipt=r, error='receipt:missing_key')
        r = deepcopy(self.receipt); r['records'][0]['raw_sha256'] = '0'*64
        self.reject('receipt_manifest_hash_disagreement', receipt=r, error='receipt_manifest_records')

    def test_11_wrong_path_and_extra_key(self):
        rows = deepcopy(self.rows); rows[0]['raw_path'] = rows[1]['raw_path']
        self.reject('wrong_or_reused_raw_path', rows=rows, error='manifest:raw_path')
        rows = deepcopy(self.rows); rows[0]['condition'] = 'unregistered'
        self.reject('unexpected_key', rows=rows, error='manifest:unexpected_key')

    def test_12_missing_or_empty_raw_file(self):
        path = self.cache / self.rows[0]['raw_path']; original = path.read_bytes()
        try:
            path.unlink(); self.reject('missing_raw_file', error='raw_file_missing:')
            path.write_bytes(b''); self.reject('empty_raw_file', error='raw_file_empty:')
        finally:
            path.write_bytes(original)

    def test_13_final_receipt_bindings(self):
        mutations = [('kind', 'smoke_cached_pipeline', 'kind'), ('device', 'cuda', 'device_threads'),
                     ('threads', 8, 'device_threads'), ('weights_unchanged', False, 'weights_unchanged'),
                     ('code_vocab_selection_images_verified', False, 'code_vocab_selection_images_verified'),
                     ('vocabulary_sha256', '0'*64, 'vocabulary_sha256'),
                     ('selection_sha256', '0'*64, 'selection_sha256'),
                     ('image_ids', list(reversed(self.contract['ids'])), 'ordered_image_ids')]
        for field, value, error in mutations:
            r = deepcopy(self.receipt); r[field] = value
            self.reject('wrong_receipt_' + field, receipt=r, error=error)


if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(CompletionVerifierTests))
    receipt = {'task': 'T013-FIN1', 'kind': 'synthetic_verifier_tests',
               'timestamp_utc': datetime.now(timezone.utc).isoformat(), 'python': sys.version,
               'status': 'PASS' if result.wasSuccessful() else 'FAIL', 'tests_run': result.testsRun,
               'failures': len(result.failures), 'errors': len(result.errors), 'fixtures': OBSERVATIONS,
               'source_sha256': {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                                 for name in ['primary_completion_verifier.py', 'test_primary_completion_verifier.py']},
               'primary_cache_accessed': False, 'npz_deserialized': False}
    (HERE/'primary_completion_test_receipt.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
    raise SystemExit(not result.wasSuccessful())
