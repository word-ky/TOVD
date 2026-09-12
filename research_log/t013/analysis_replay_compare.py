"""Exact comparison of completed engineering/replay outputs; never use on live output."""
import argparse
import json
import math
from pathlib import Path

import numpy as np

FILES = ('results.json', 'paired_image_draws.npy', 'bootstrap_samples.npz', 'diagnostics_per_image.npz')


def same_json(left, right):
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(same_json(left[k], right[k]) for k in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(same_json(a, b) for a, b in zip(left, right))
    if isinstance(left, float) and math.isnan(left):
        return math.isnan(right)
    return left == right


def array_check(left, right):
    shape = left.shape == right.shape
    dtype = left.dtype == right.dtype
    equal = bool(shape and dtype and np.array_equal(left, right, equal_nan=True))
    return {'equal': equal, 'left_shape': list(left.shape), 'right_shape': list(right.shape),
            'left_dtype': str(left.dtype), 'right_dtype': str(right.dtype),
            'nan_masks_equal': bool(shape and np.array_equal(np.isnan(left), np.isnan(right)))}


def compare(left, right):
    left, right = Path(left), Path(right)
    artifacts = {}
    for name in FILES:
        a, b = left/name, right/name
        nonempty = a.is_file() and b.is_file() and a.stat().st_size > 0 and b.stat().st_size > 0
        item = {'present_nonempty': nonempty, 'equal': False}
        artifacts[name] = item
        if not nonempty:
            continue
        item['left_bytes'], item['right_bytes'] = a.stat().st_size, b.stat().st_size
        if name.endswith('.json'):
            av, bv = json.loads(a.read_text()), json.loads(b.read_text())
            item['equal'] = same_json(av, bv)
            item['top_level_keys_equal'] = av.keys() == bv.keys()
            item['fields'] = {key: key in bv and same_json(value, bv[key]) for key, value in av.items()}
        elif name.endswith('.npy'):
            item.update(array_check(np.load(a, allow_pickle=False), np.load(b, allow_pickle=False)))
        else:
            with np.load(a, allow_pickle=False) as av, np.load(b, allow_pickle=False) as bv:
                item['keys_equal'] = set(av.files) == set(bv.files)
                item['arrays'] = {key: array_check(av[key], bv[key]) for key in sorted(set(av.files) & set(bv.files))}
                item['equal'] = item['keys_equal'] and all(row['equal'] for row in item['arrays'].values())
    return {'status': 'PASS' if all(item['equal'] for item in artifacts.values()) else 'FAIL',
            'artifacts': artifacts, 'comparison': 'exact decoded JSON/arrays with equal NaNs; no compressed-byte equality requirement'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('left', type=Path)
    parser.add_argument('right', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = compare(args.left, args.right)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))
    raise SystemExit(result['status'] != 'PASS')
