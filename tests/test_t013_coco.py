from copy import deepcopy

import numpy as np

from scripts.t013_coco import (
    accumulate_image_copies, evaluate_dataset, image_cache, metrics, paired_bootstrap_indices,
)


def fixture():
    dataset = {"info": {}, "images": [{"id": 1}, {"id": 2}],
               "categories": [{"id": 1, "name": "person"}, {"id": 2, "name": "cat"}],
               "annotations": [
                   {"id": 1, "image_id": 1, "category_id": 1, "bbox": [0, 0, 10, 10], "area": 100, "iscrowd": 0},
                   {"id": 2, "image_id": 1, "category_id": 1, "bbox": [20, 0, 10, 10], "area": 100, "iscrowd": 1},
                   {"id": 3, "image_id": 2, "category_id": 2, "bbox": [0, 0, 10, 10], "area": 100, "iscrowd": 0},
               ]}
    predictions = [
        {"image_id": 1, "category_id": 1, "bbox": [0, 0, 10, 10], "score": .7},
        {"image_id": 1, "category_id": 1, "bbox": [40, 0, 10, 10], "score": .7},
        {"image_id": 1, "category_id": 1, "bbox": [20, 0, 10, 10], "score": .7},
        {"image_id": 2, "category_id": 2, "bbox": [40, 0, 10, 10], "score": .7},
        {"image_id": 2, "category_id": 2, "bbox": [0, 0, 10, 10], "score": .7},
    ]
    return dataset, predictions


def test_bootstrap_cache_exactly_matches_full_reevaluation_with_ties_and_crowd():
    dataset, predictions = fixture()
    source = evaluate_dataset(dataset, predictions, [1, 2])
    cache = image_cache(source)
    for draws in [[1, 0, 1], [0, 0, 0], [1, 1, 0, 0], [1, 0]]:
        copied = {"info": {}, "images": [], "categories": dataset["categories"], "annotations": []}
        detected = []
        for copy_id, index in enumerate(draws, 1):
            original_id = index + 1
            copied["images"].append({"id": copy_id})
            for row in dataset["annotations"]:
                if row["image_id"] == original_id:
                    copied["annotations"].append(dict(deepcopy(row), image_id=copy_id, id=len(copied["annotations"]) + 1))
            detected.extend(dict(deepcopy(row), image_id=copy_id) for row in predictions if row["image_id"] == original_id)
        actual = evaluate_dataset(copied, detected, list(range(1, len(draws) + 1)))
        cached = accumulate_image_copies(cache, draws)
        np.testing.assert_array_equal(cached["precision"][..., 0], actual.eval["precision"][..., 0])
        np.testing.assert_array_equal(cached["recall"][..., 0], actual.eval["recall"][..., 0])
        assert metrics(cached) == metrics(actual.eval)


def test_empty_detections_and_paired_sampling():
    dataset, _ = fixture()
    result = evaluate_dataset(dataset, [], [1, 2])
    assert metrics(result.eval) == {"AP": 0., "AP50": 0., "AR": 0., "AR50": 0.}
    a = paired_bootstrap_indices(2, replicates=10)
    np.testing.assert_array_equal(a, paired_bootstrap_indices(2, replicates=10))
    assert a.shape == (10, 2)
