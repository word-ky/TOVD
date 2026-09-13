"""Deterministic in-memory selection fixtures; no detector or annotations."""
import unittest

import numpy as np
import torch

from canonical_topk_counterfactual import canonical_topk


class CanonicalTopkTests(unittest.TestCase):
    def setUp(self):
        self.boxes = np.arange(3600, dtype=np.float32).reshape(900, 4)
        self.scores = (np.arange(99000, dtype=np.float32) / 100000).reshape(900, 110)

    def test_exact_index_mapping(self):
        out = canonical_topk(self.boxes, self.scores)
        flat = np.argsort(self.scores[:, :80].reshape(-1))[::-1][:300]
        np.testing.assert_array_equal(out['top_query_ids'], flat // 80)
        np.testing.assert_array_equal(out['top_labels'], flat % 80)
        self.assertEqual(len(out['top_scores']), 300)
        self.assertTrue(np.all(out['top_labels'] < 80))

    def test_score_and_box_identity_and_no_mutation(self):
        boxes, scores = self.boxes.copy(), self.scores.copy()
        out = canonical_topk(self.boxes, self.scores)
        np.testing.assert_array_equal(out['top_scores'], scores[out['top_query_ids'], out['top_labels']])
        np.testing.assert_array_equal(out['boxes'], boxes[out['top_query_ids']])
        np.testing.assert_array_equal(self.boxes, boxes)
        np.testing.assert_array_equal(self.scores, scores)

    def test_repeated_calls_with_ties(self):
        scores = np.ones((900, 110), dtype=np.float32)
        first = canonical_topk(self.boxes, scores)
        second = canonical_topk(self.boxes, scores)
        reference_scores, flat = torch.topk(torch.from_numpy(scores[:, :80]).flatten(), 300)
        for name in first:
            np.testing.assert_array_equal(first[name], second[name])
        np.testing.assert_array_equal(first['top_query_ids'], (flat // 80).numpy())
        np.testing.assert_array_equal(first['top_labels'], (flat % 80).numpy())
        np.testing.assert_array_equal(first['top_scores'], reference_scores.numpy())

    def test_distractor_crowd_out(self):
        scores = self.scores.copy()
        before = canonical_topk(self.boxes, scores)
        scores[:, 80:] += 2
        _, all_flat = torch.topk(torch.from_numpy(scores).flatten(), 300)
        self.assertTrue(torch.all(all_flat % 110 >= 80).item())
        after = canonical_topk(self.boxes, scores)
        for name in before:
            np.testing.assert_array_equal(before[name], after[name])
        self.assertTrue(np.all(after['top_labels'] < 80))

    def test_v0_original_selection(self):
        scores = self.scores[:, :80].copy()
        reference_scores, flat = torch.topk(torch.from_numpy(scores).flatten(), 300)
        out = canonical_topk(self.boxes, scores)
        np.testing.assert_array_equal(out['top_query_ids'], (flat // 80).numpy())
        np.testing.assert_array_equal(out['top_labels'], (flat % 80).numpy())
        np.testing.assert_array_equal(out['top_scores'], reference_scores.numpy())


if __name__ == '__main__':
    unittest.main()
