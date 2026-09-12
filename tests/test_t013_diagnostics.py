import numpy as np

from scripts.t013_coco import evaluate_dataset, image_cache
from scripts.t013_diagnostics import canonical_fp_from_cache, canonical_predictions, image_diagnostics


def test_distractor_mapping_and_semantic_versus_localization_failure():
    raw = {"boxes": np.array([[0, 0, 10, 10], [20, 20, 30, 30]], dtype=np.float32),
           "class_scores": np.array([[.2, .8], [.6, .1]], dtype=np.float32),
           "top_query_ids": np.array([0, 1]), "top_labels": np.array([1, 0]),
           "top_scores": np.array([.8, .6])}
    gt = [{"id": 1, "image_id": 1, "category_id": 17, "bbox": [0, 0, 10, 10], "area": 100, "iscrowd": 0}]
    predictions = canonical_predictions(raw, 1, [17])
    assert len(predictions) == 1 and predictions[0]["category_id"] == 17
    assert predictions[0]["bbox"] == [20., 20., 10., 10.]
    diag = image_diagnostics(raw, gt, [17])
    assert diag["canonical_covered"] == 0 and diag["localized"] == 1
    assert diag["distractor_fp"] == 1
    np.testing.assert_allclose(diag["margin"], [-.6])
    dataset = {"info": {}, "images": [{"id": 1}], "categories": [{"id": 17}], "annotations": gt}
    cache = image_cache(evaluate_dataset(dataset, predictions, [1]))
    assert canonical_fp_from_cache(cache).tolist() == [1]


def test_no_ground_truth_or_selected_detections():
    raw = {"boxes": np.array([[0., 0., 10., 10.]]), "class_scores": np.array([[.1, .2]]),
           "top_query_ids": np.array([0]), "top_labels": np.array([1]), "top_scores": np.array([.2])}
    diag = image_diagnostics(raw, [], [17])
    assert diag["gt_count"] == diag["distractor_fp"] == diag["localized"] == 0
    gt = [{"id": 1, "category_id": 17, "bbox": [0, 0, 10, 10], "iscrowd": 0}]
    diag = image_diagnostics(raw, gt, [17])
    assert diag["gt_count"] == 1 and diag["canonical_covered"] == diag["localized"] == 0
