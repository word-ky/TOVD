"""Frozen T013-PARITY-B set comparison; scores never influence assignment."""
import numpy as np
from scipy.optimize import linear_sum_assignment


def box_iou(left, right):
    left, right = np.asarray(left, dtype=np.float64), np.asarray(right, dtype=np.float64)
    intersection = np.maximum(0, np.minimum(left[:, None, 2:], right[None, :, 2:])
                              - np.maximum(left[:, None, :2], right[None, :, :2])).prod(-1)
    area_left = np.maximum(0, left[:, 2:] - left[:, :2]).prod(-1)
    area_right = np.maximum(0, right[:, 2:] - right[:, :2]).prod(-1)
    union = area_left[:, None] + area_right[None, :] - intersection
    return np.divide(intersection, union, out=np.zeros_like(union), where=union > 0)


def assign(left, right):
    # Fixed input order and SciPy 1.17.0 deterministic LSAP tie handling. No
    # epsilon perturbation: maximize the actual sum of IoUs, including ties.
    matrix = box_iou(left, right)
    rows, columns = linear_sum_assignment(-matrix)
    return rows, columns, matrix[rows, columns]


def compare_detections(native, hf):
    counts_native = np.bincount(native['labels'], minlength=80)
    counts_hf = np.bincount(hf['labels'], minlength=80)
    difference = counts_hf - counts_native
    result = {'native_count': len(native['labels']), 'hf_count': len(hf['labels']),
              'per_class_count_difference_hf_minus_native': difference.tolist(),
              'min_matched_iou': None, 'max_matched_score_error': None,
              'pairs': [], 'pass': False}
    if len(native['labels']) != 300 or len(hf['labels']) != 300 or np.any(difference):
        return result
    for label in range(80):
        n = np.flatnonzero(native['labels'] == label)
        h = np.flatnonzero(hf['labels'] == label)
        if not len(n):
            continue
        rows, columns, overlaps = assign(native['boxes'][n], hf['boxes'][h])
        for row, col, overlap in zip(rows, columns, overlaps):
            ni, hi = int(n[row]), int(h[col])
            result['pairs'].append({'class_id': label, 'native_index': ni, 'hf_index': hi,
                                    'iou': float(overlap), 'score_error': float(abs(
                                        float(native['scores'][ni]) - float(hf['scores'][hi])))})
    result['min_matched_iou'] = min(p['iou'] for p in result['pairs'])
    result['max_matched_score_error'] = max(p['score_error'] for p in result['pairs'])
    result['pass'] = result['min_matched_iou'] >= .999 and result['max_matched_score_error'] <= 1e-4
    return result


def raw_box_diagnostics(native_cxcywh, hf_cxcywh, native_xyxy, hf_xyxy):
    rows, columns, overlaps = assign(native_xyxy, hf_xyxy)
    return {'indexwise_aligned_box_count': int(np.sum(np.max(np.abs(
                native_cxcywh - hf_cxcywh), axis=-1) <= 1e-4)),
            'box_set_iou_min': float(overlaps.min()),
            'box_set_iou_median': float(np.median(overlaps)),
            'box_set_iou_mean': float(overlaps.mean()),
            'box_set_permutation_is_identity': bool(np.array_equal(rows, columns)),
            'box_set_permutation': columns.tolist()}
