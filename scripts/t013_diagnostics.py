"""Prespecified class mapping, object coverage and score-margin diagnostics."""
import numpy as np


def canonical_predictions(raw, image_id, category_ids):
    predictions = []
    for query, label, score in zip(raw["top_query_ids"], raw["top_labels"], raw["top_scores"]):
        if label < len(category_ids):
            x1, y1, x2, y2 = raw["boxes"][query]
            predictions.append({"image_id": int(image_id), "category_id": int(category_ids[label]),
                                "bbox": [float(x1), float(y1), float(x2 - x1), float(y2 - y1)],
                                "score": float(score)})
    return predictions


def iou_matrix(boxes, gt_boxes):
    lo = np.maximum(boxes[:, None, :2], gt_boxes[None, :, :2])
    hi = np.minimum(boxes[:, None, 2:], gt_boxes[None, :, 2:])
    intersection = np.maximum(hi - lo, 0).prod(axis=-1)
    union = (np.maximum(boxes[:, 2:] - boxes[:, :2], 0).prod(axis=-1)[:, None]
             + np.maximum(gt_boxes[:, 2:] - gt_boxes[:, :2], 0).prod(axis=-1)[None, :] - intersection)
    return np.divide(intersection, union, out=np.zeros_like(intersection), where=union > 0)


def image_diagnostics(raw, ground_truth, category_ids, threshold=.25):
    gt = sorted([row for row in ground_truth if not row["iscrowd"]], key=lambda row: row["id"])
    gt_boxes = np.array([row["bbox"] for row in gt], dtype=np.float64).reshape(-1, 4)
    gt_boxes[:, 2:] += gt_boxes[:, :2]
    labels = np.array([category_ids.index(row["category_id"]) for row in gt], dtype=np.int64)
    overlaps = iou_matrix(raw["boxes"].astype(np.float64), gt_boxes)
    keep = raw["top_scores"] >= threshold
    selected_queries, selected_labels = raw["top_query_ids"][keep], raw["top_labels"][keep]
    matched = overlaps[selected_queries] >= .5
    localized = matched.any(axis=0)
    classified = (matched & (selected_labels[:, None] == labels[None, :])).any(axis=0)
    best_query = overlaps.argmax(axis=0)
    best_iou = overlaps[best_query, np.arange(len(gt))]
    margin = np.full(len(gt), np.nan, dtype=np.float64)
    if raw["class_scores"].shape[1] > len(category_ids):
        probabilities = raw["class_scores"][best_query]
        margin = probabilities[np.arange(len(gt)), labels].astype(np.float64) - probabilities[:, len(category_ids):].max(axis=1)
        margin[best_iou < .5] = np.nan
    return {"gt_ids": np.array([row["id"] for row in gt], dtype=np.int64),
            "gt_count": len(gt), "canonical_covered": int(classified.sum()),
            "localized": int(localized.sum()),
            "distractor_fp": int((selected_labels >= len(category_ids)).sum()),
            "margin": margin, "margin_localized": best_iou >= .5}


def canonical_fp_from_cache(cache, threshold=.25):
    counts = np.zeros(len(cache["params"].imgIds), dtype=np.int64)
    for rows in cache["per_category"]:
        for i, row in enumerate(rows):
            if row is not None:
                active = np.asarray(row["dtScores"]) >= threshold
                counts[i] += np.count_nonzero(active & (row["dtMatches"][0] == 0) & ~row["dtIgnore"][0])
    return counts
