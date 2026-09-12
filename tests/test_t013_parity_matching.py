import numpy as np

from scripts.t013_parity_matching import assign, compare_detections


def fixture():
    x = np.arange(300) / 301
    return {'boxes': np.column_stack([x, x * 0, x + .001, x * 0 + .1]),
            'labels': np.arange(300) % 80, 'scores': np.linspace(.01, .99, 300)}


def test_permuted_identical_detections_pass():
    n = fixture()
    h = {k: v[::-1].copy() for k, v in n.items()}
    result = compare_detections(n, h)
    assert result['pass'] and result['min_matched_iou'] == 1
    assert result['max_matched_score_error'] == 0


def test_class_counts_and_required_300_fail_immediately():
    n = fixture()
    h = {k: v.copy() for k, v in n.items()}
    h['labels'][0] = 1
    assert compare_detections(n, h)['pairs'] == []
    assert not compare_detections(n, {k: v[:-1] for k, v in n.items()})['pass']


def test_fixed_score_and_iou_failures():
    n = fixture()
    h = {k: v.copy() for k, v in n.items()}
    h['scores'][0] += .00011
    assert not compare_detections(n, h)['pass']
    h = {k: v.copy() for k, v in n.items()}
    h['boxes'][0, 0] += .00001
    assert not compare_detections(n, h)['pass']


def test_ties_are_deterministic_and_scores_cannot_rescue_assignment():
    n = fixture()
    n['boxes'][80] = n['boxes'][0]
    h = {k: v.copy() for k, v in n.items()}
    first = compare_detections(n, h)
    assert first == compare_detections(n, h)
    assert first['pass']
    h['scores'][[0, 80]] = h['scores'][[80, 0]]
    changed = compare_detections(n, h)
    assert not changed['pass']
    assert [(p['native_index'], p['hf_index']) for p in first['pairs']] == [
        (p['native_index'], p['hf_index']) for p in changed['pairs']]
    boxes = np.array([[0, 0, 1, 1], [.1, 0, 1.1, 1]])
    _, permutation, ious = assign(boxes, boxes[::-1])
    assert permutation.tolist() == [1, 0] and np.all(ious == 1)
