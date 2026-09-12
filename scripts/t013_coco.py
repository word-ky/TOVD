"""Official COCO metrics with exact image-copy bootstrap accumulation."""
from contextlib import redirect_stdout
from copy import deepcopy
import io

import numpy as np
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval


def evaluate_dataset(dataset, predictions, image_ids):
    with redirect_stdout(io.StringIO()):
        ground_truth = COCO()
        ground_truth.dataset = deepcopy(dataset)
        ground_truth.createIndex()
        if predictions:
            detected = ground_truth.loadRes(deepcopy(predictions))
        else:
            detected = COCO()
            detected.dataset = {"images": deepcopy(dataset["images"]),
                                "categories": deepcopy(dataset["categories"]), "annotations": []}
            detected.createIndex()
        evaluator = COCOeval(ground_truth, detected, "bbox")
        evaluator.params.imgIds = sorted(image_ids)
        evaluator.params.areaRng = [[0, 1e10]]
        evaluator.params.areaRngLbl = ["all"]
        # Match up to300 for FP accounting; primary AP/AR still use COCO maxDet100.
        evaluator.params.maxDets = [100, 300]
        evaluator.evaluate()
        evaluator.accumulate()
    return evaluator


def metrics(evaluation):
    params = evaluation["params"]
    m = params.maxDets.index(100)
    precision = evaluation["precision"][:, :, :, 0, m]
    recall = evaluation["recall"][:, :, 0, m]
    def mean_valid(values):
        valid = values[values >= 0]
        return float(valid.mean() * 100) if valid.size else float("nan")
    return {"AP": mean_valid(precision), "AP50": mean_valid(precision[0]),
            "AR50": mean_valid(recall[0])}


def image_cache(evaluator):
    n = len(evaluator.params.imgIds)
    return {"params": deepcopy(evaluator.params),
            "per_category": [evaluator.evalImgs[k * n:(k + 1) * n]
                             for k in range(len(evaluator.params.catIds))]}


def accumulate_image_copies(cache, sampled_indices):
    """Exactly repeat per-image matches, retaining stable detection-score tie order.

    Each draw is a separate image copy. Recompute the entire dataset precision /
    recall curve through COCOeval.accumulate; never average per-image AP.
    """
    evaluator = COCOeval(iouType="bbox")
    params = deepcopy(cache["params"])
    params.imgIds = list(range(len(sampled_indices)))
    params.maxDets = [100]
    evaluator.params = params
    evaluator._paramsEval = deepcopy(params)
    evaluator.evalImgs = [rows[int(i)] for rows in cache["per_category"] for i in sampled_indices]
    with redirect_stdout(io.StringIO()):
        evaluator.accumulate()
    return evaluator.eval


def paired_bootstrap_indices(n_images, seed=20260913, replicates=1000):
    return np.random.default_rng(seed).integers(0, n_images, size=(replicates, n_images))
