"""Synthetic, standard-library-only P2 checks; no images or model imports."""
import hashlib
import json
from pathlib import Path
import unittest

from protocol_adapter import build_receipt, class_indices, runtime_texts, semantic_predictions

ROOT = Path(__file__).resolve().parents[2]
VOCAB_PATH = ROOT / 'research_log/t013/vocabulary_native30.json'
VOCAB = json.loads(VOCAB_PATH.read_bytes())['vocabularies']
P1_SHA = '85c590e21b6dc1292ad645dd660d750cfd4df42e8880f0938849e13e456f07d0'
VOCAB_SHA = '3bb4a0ebada1f9da407ae6a94f1135798dba7117bd658a6ecba97b2ebfad0967'


class ProtocolAdapterTests(unittest.TestCase):
    def test_runtime_text_counts_content_and_order(self):
        for name, expected in [('V0', 81), ('Vhard30', 111), ('Vrand30', 111)]:
            with self.subTest(vocabulary=name):
                before = list(VOCAB[name])
                texts = runtime_texts(VOCAB[name])
                self.assertEqual(len(texts), expected)
                self.assertEqual(texts[:-1], before)
                self.assertEqual(texts[-1], '\u0020')
                self.assertEqual(texts.count(' '), 1)
                self.assertEqual(VOCAB[name], before)

    def test_index_partitions_preserve_semantic_identity(self):
        for name, names in VOCAB.items():
            with self.subTest(vocabulary=name):
                indices = class_indices(names)
                self.assertEqual(indices['canonical'], list(range(80)))
                self.assertEqual([names[i] for i in indices['canonical']], VOCAB['V0'])
                self.assertEqual(indices['distractor'], [] if name == 'V0' else list(range(80, 110)))
                self.assertEqual(indices['blank'], 80 if name == 'V0' else 110)
                combined = indices['canonical'] + indices['distractor'] + [indices['blank']]
                self.assertEqual(combined, list(range(len(names) + 1)))
                self.assertEqual(len(set(combined)), len(combined))

    def test_selected_semantic_rows_keep_order_scores_boxes_and_identity(self):
        selected = [
            {'label': 110, 'score': .97, 'bbox': [1, 2, 3, 4]},
            {'label': 79, 'score': .51, 'bbox': [10, 11, 30, 40]},
            {'label': 80, 'score': .94, 'bbox': [3, 4, 20, 21]},
            {'label': 110, 'score': .45, 'bbox': [5, 6, 7, 8]},
            {'label': 109, 'score': .51, 'bbox': [0, 2, 10, 15]},
            {'label': 0, 'score': .51, 'bbox': [9, 1, 22, 26]},
        ]
        before = json.dumps(selected)
        rows, blank_count = semantic_predictions(selected, 110)
        self.assertEqual(rows, [selected[i] for i in (1, 2, 4, 5)])
        for row, index in zip(rows, (1, 2, 4, 5)):
            self.assertIs(row, selected[index])
        self.assertEqual(blank_count, 2)
        self.assertEqual(json.dumps(selected), before)

    def test_blank_is_not_confused_with_extended_distractor_80(self):
        selected = [{'label': 80, 'score': .9, 'bbox': [0, 0, 1, 1]}]
        self.assertEqual(semantic_predictions(selected, 80), ([], 1))
        self.assertEqual(semantic_predictions(selected, 110), (selected, 0))

    def test_no_refill_from_larger_pool_at_native_300_limit(self):
        # Fixture of an already-completed native selection, not a detector/NMS.
        pool = [{'id': i, 'label': 0, 'score': 1 - i / 1000, 'bbox': [i, 0, i+1, 1]}
                for i in range(305)]
        pool[0]['label'] = 110
        pool[150]['label'] = 110
        pool[299]['label'] = 110
        native_selected = pool[:300]
        rows, count = semantic_predictions(native_selected, 110)
        self.assertEqual(count, 3)
        self.assertEqual(len(rows), 297)
        self.assertEqual([r['id'] for r in rows], [i for i in range(300) if i not in (0, 150, 299)])
        self.assertFalse(any(row['id'] >= 300 for row in rows))

    def test_same_contract_across_all_15_cells(self):
        conditions = ['clean', 'gaussian_noise', 'motion_blur', 'fog', 'jpeg_compression']
        for condition in conditions:
            for name, names in VOCAB.items():
                with self.subTest(condition=condition, vocabulary=name):
                    texts = runtime_texts(names)
                    indices = class_indices(names)
                    self.assertEqual(texts, list(names) + [' '])
                    selected = [{'label': indices['blank'], 'score': .9, 'bbox': [0, 0, 1, 1]},
                                {'label': 1, 'score': .8, 'bbox': [1, 2, 3, 4]}]
                    self.assertEqual(semantic_predictions(selected, indices['blank']), ([selected[1]], 1))

    def test_receipt_binds_frozen_inputs_and_native_constants(self):
        receipt = build_receipt()
        self.assertEqual(receipt['semantic_vocabulary_sha256'], VOCAB_SHA)
        self.assertEqual(receipt['p1_receipt_sha256'], P1_SHA)
        native = receipt['native_postprocessing']
        self.assertEqual(native['test_cfg'], {
            'multi_label': True, 'score_thr': .001, 'nms_pre': 30000,
            'nms': {'type': 'nms', 'iou_threshold': .7}, 'max_per_img': 300})
        self.assertTrue(native['with_nms'])
        self.assertTrue(native['rescale'])
        self.assertFalse(native['test_time_augmentation'])
        self.assertFalse(native['demo_extra_filtering'])
        expected = hashlib.sha256(json.dumps(native, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        self.assertEqual(receipt['native_postprocessing_sha256'], expected)
        self.assertEqual(receipt, build_receipt())


if __name__ == '__main__':
    unittest.main()
