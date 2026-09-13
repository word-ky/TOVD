"""Small analytic fixtures for replicate-first CF2 descriptors and intervals."""
import unittest
import numpy as np
from canonical_counterfactual_analysis import descriptors, paired_summary


class CounterfactualArithmeticTests(unittest.TestCase):
    def setUp(self):
        self.cf = np.array([[80, 70, 60], [70, 55, 48], [60, 44, 35],
                            [50, 32, 24], [40, 21, 14]], dtype=float)
        self.original = self.cf.copy()
        self.original[1:, 1] -= [1, 2, 3, 4]
        self.original[1:, 2] -= [4, 3, 2, 1]

    def test_drops_amplifications_removed_and_contrasts(self):
        d = descriptors(self.original, self.cf)
        np.testing.assert_array_equal(d['D_cf'], [[10,15,12],[20,26,25],[30,38,36],[40,49,46]])
        np.testing.assert_array_equal(d['A_cf'], [[0,5,2],[0,6,5],[0,8,6],[0,9,6]])
        np.testing.assert_array_equal(d['L_topk'], [[0,1,4],[0,2,3],[0,3,2],[0,4,1]])
        np.testing.assert_array_equal(d['H_cf'], [3,1,2,3])
        np.testing.assert_array_equal(d['L_topk_hard_minus_random'], [-3,-1,1,3])
        self.assertEqual(d['mean_A_cf_hard'], 7)
        self.assertEqual(d['mean_L_topk_hard'], 2.5)
        self.assertEqual(d['mean_H_cf'], 2.25)
        self.assertEqual(d['mean_L_topk_hard_minus_random'], 0)

    def test_identical_original_counterfactual_zero_removed(self):
        d = descriptors(self.cf, self.cf)
        np.testing.assert_array_equal(d['L_topk'], np.zeros((4,3)))
        np.testing.assert_array_equal(d['L_topk_hard_minus_random'], np.zeros(4))

    def test_replicate_first_means(self):
        cf = np.stack([self.cf, self.cf*2, self.cf*3])
        orig = np.stack([self.original, self.original*2, self.original*3])
        d = descriptors(orig, cf)
        for key, expected in [('mean_A_cf_hard',[7,14,21]),
                              ('mean_L_topk_hard',[2.5,5,7.5]),
                              ('mean_H_cf',[2.25,4.5,6.75]),
                              ('mean_L_topk_hard_minus_random',[0,0,0])]:
            np.testing.assert_array_equal(d[key], expected)

    def test_percentile_linear_on_replicate_contrasts(self):
        # Perfectly paired contrasts are constant despite varying AP50 values.
        cf = np.zeros((3,5,3)); orig = np.zeros_like(cf)
        cf[:,1:,1] = -np.array([0,10,20])[:,None]
        orig[:,1:,1] = -np.array([1,11,21])[:,None]
        summary, _ = paired_summary(orig[0], cf[0], orig, cf)
        self.assertEqual(summary['ci95']['mean_L_topk_hard'], [1,1])
        np.testing.assert_allclose(summary['ci95']['mean_A_cf_hard'], [.5,19.5])
        # Subtracting marginal CI endpoints would incorrectly give [-18,20].
        wrong = np.percentile([1,11,21], [2.5,97.5]) - np.percentile([0,10,20], [97.5,2.5])
        self.assertFalse(np.array_equal(wrong, summary['ci95']['mean_L_topk_hard']))

    def test_mean_before_interval_not_mean_of_intervals(self):
        cf = np.zeros((2,5,3))
        cf[:,1:,1] = -np.array([[0,100,0,100],[100,0,100,0]])
        summary, _ = paired_summary(cf[0], cf[0], cf, cf)
        self.assertEqual(summary['ci95']['mean_A_cf_hard'], [50,50])
        marginal = np.asarray(summary['ci95']['A_cf'])[:,:,1].mean(axis=1)
        self.assertFalse(np.array_equal(marginal, [50,50]))

    def test_nonfinite_ci_matches_frozen_convention(self):
        samples = np.stack([self.cf,self.cf])
        samples[0,1,1] = np.nan
        summary, _ = paired_summary(self.original,self.cf,samples,samples)
        self.assertIsNone(summary['ci95']['A_cf'])


if __name__ == '__main__':
    unittest.main()
