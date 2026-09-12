import numpy as np
from scripts.t013_analysis import assess_gates, diagnostic_means, interaction, mechanism_values


def test_difference_in_differences_and_fixed_gate_boundaries():
    point = np.zeros((5, 3, 8))
    point[0, :, 1] = [50, 48, 49]
    point[1:, :, 1] = [45, 41, 44]
    drop, amp, specificity = interaction(point[:, :, 1])
    np.testing.assert_array_equal(drop, np.tile([5, 7, 5], (4, 1)))
    np.testing.assert_array_equal(amp, np.tile([0, 2, 0], (4, 1)))
    np.testing.assert_array_equal(specificity, np.full(4, 2))
    boot = np.repeat(point[None], 30, axis=0)
    mp = mechanism_values(point, np.zeros(4))
    mb = mechanism_values(boot, np.zeros((30, 4)))
    result = assess_gates(point, boot, mp, mb, True)
    assert result['gate1'] and result['gate2'] and result['gate4_recorded_checks']
    point[1:, 1, 1] = 42.01  # hard amplification0.99 fails Gate1 unchanged.
    result = assess_gates(point, np.repeat(point[None], 30, axis=0), mp, mb, True)
    assert not result['gate1']


def test_zero_bootstrap_lower_bound_fails_and_micro_diagnostics_repeat_images():
    point = np.zeros((5, 3, 8))
    point[0, :, 1] = [50, 50, 50]
    point[1:, :, 1] = [45, 43, 45]
    boot = np.repeat(point[None], 100, axis=0)
    boot[:5, 1:, 1, 1] = 45
    mp = mechanism_values(point, np.zeros(4))
    mb = mechanism_values(boot, np.zeros((100, 4)))
    assert not assess_gates(point, boot, mp, mb, True)['gate1']
    rows = np.array([[2, 1, 2, 1, 3], [1, 0, 1, 0, 1]], dtype=float)
    fp, distractor, recall, local = diagnostic_means(rows, [0, 0, 1])
    assert fp == 7 / 3 and distractor == 2 / 3 and recall == 40 and local == 100
