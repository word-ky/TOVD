"""CF1 receipt driver pinned to the completed engineering smoke only."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

import numpy as np
import torch

from canonical_topk_counterfactual import canonical_topk

ROOT = Path('/home/wenchang/asdasdsad/wjq/TOVD')
SMOKE_RUN = '20260912-205428-tovd-native30-pipeline-smoke'
CACHE = ROOT / 'runs' / SMOKE_RUN / 'artifacts/cache'
FROZEN = ROOT / 'releases/20260912-210306-tovd-native30-primary-freeze'
OUT = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    receipt = {
        'task': 'T013-CF1', 'status': 'RUNNING',
        'task_start_head': '56c80996fdbe274f583596db018cd10cd64f755c',
        'freeze_commit': '6fec32243985ccc808123d851abf5f3dea10af99',
        'smoke_run': SMOKE_RUN, 'smoke_cache': str(CACHE),
        'environment': {'python': sys.version, 'executable': sys.executable,
                        'torch': torch.__version__, 'numpy': np.__version__, 'device': 'cpu'},
        'source_sha256': {name: sha(OUT / name) for name in (
            'canonical_topk_counterfactual.py', 'test_canonical_topk_counterfactual.py',
            'validate_canonical_topk_smoke.py', 'CANONICAL_TOPK_COUNTERFACTUAL.md')},
        'bindings': {}, 'cells': [],
        'scope': {'active_primary_cache_accessed': False,
                  'active_primary_scientific_content_opened': False,
                  'annotations_or_coco_metrics': False, 'fin1_or_analysis_replay': False,
                  'detector_inference': False, 'run_mutation': False,
                  'yolo_runtime': False, 't014_execution': False,
                  'primary_scientific_execution_authorized': False,
                  'primary_gates_or_decision_changed': False},
    }
    try:
        assert torch.__version__.split('+')[0] == '2.4.0', 'frozen Torch required'
        for path, expected in (
            (FROZEN / 'scripts/t013_native_detector.py', 'b49f23f131777f08e23131ad55a94d9211c33b1c759adf86c6b52e2b95c34126'),
            (CACHE / 'run_receipt.json', 'a1ec8408c5294935759b462f4f0663b8a5e7b9620acebd61bceb977a509bf0e5'),
            (CACHE / 'cache_manifest.jsonl', '3d3623c2a6d78edd63b35c3efbdaf733df48eb1ffb9cefe36ea7e2daf2355a5f'),
        ):
            actual = sha(path)
            receipt['bindings'][str(path)] = {'expected': expected, 'actual': actual}
            assert actual == expected, str(path)
        smoke = json.loads((CACHE / 'run_receipt.json').read_text())
        assert smoke['completed'] and smoke['kind'] == 'smoke_cached_pipeline'
        assert smoke['image_ids'] == [139, 285, 632]
        command = [sys.executable, '-m', 'unittest', '-v', 'test_canonical_topk_counterfactual']
        tests = subprocess.run(command, cwd=OUT, capture_output=True, text=True)
        (OUT / 'canonical_topk_tests.txt').write_text(tests.stdout + tests.stderr)
        receipt['synthetic_tests'] = {'command': command, 'count': 5, 'exit_code': tests.returncode,
                                      'log_sha256': sha(OUT / 'canonical_topk_tests.txt')}
        assert tests.returncode == 0, 'synthetic tests failed'
        for condition in ('clean', 'gaussian_noise', 'motion_blur', 'fog', 'jpeg_compression'):
            for vocab in ('V0', 'Vhard30', 'Vrand30'):
                for image_id in (139, 285, 632):
                    path = CACHE / 'raw' / condition / vocab / f'{image_id:012d}.npz'
                    row = {'condition': condition, 'vocabulary': vocab, 'image_id': image_id,
                           'path': str(path), 'status': 'CHECKING'}
                    receipt['cells'].append(row)
                    with np.load(path, allow_pickle=False) as data:
                        boxes, scores = data['boxes'], data['class_scores']
                        assert boxes.shape == (900, 4)
                        assert scores.shape == (900, 80 if vocab == 'V0' else 110)
                        out = canonical_topk(boxes, scores)
                        ref_scores, ref_flat = torch.topk(torch.from_numpy(scores[:, :80]).flatten(), 300)
                        reference = {'top_query_ids': (ref_flat // 80).numpy(),
                                     'top_labels': (ref_flat % 80).numpy(), 'top_scores': ref_scores.numpy()}
                        for key in reference:
                            np.testing.assert_array_equal(out[key], reference[key])
                            if vocab == 'V0':
                                np.testing.assert_array_equal(out[key], data[key])
                        assert np.all((out['top_labels'] >= 0) & (out['top_labels'] < 80))
                        np.testing.assert_array_equal(out['top_scores'], scores[out['top_query_ids'], out['top_labels']])
                        np.testing.assert_array_equal(out['boxes'], boxes[out['top_query_ids']])
                    row.update(status='PASS', stored_v0_identity=(True if vocab == 'V0' else None),
                               canonical_reference_exact=True, scores_boxes_exact=True)
        receipt.update(status='PASS', v0_identity_exact_count=15, hard_random_reference_exact_count=30,
                       labels_canonical_all=True, selected_scores_boxes_exact_all=True)
    except Exception as error:
        receipt.update(status='BLOCKED', failure={'type': type(error).__name__, 'detail': str(error)})
    receipt['finished_utc'] = datetime.now(timezone.utc).isoformat()
    (OUT / 'canonical_topk_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'status': receipt['status'], 'failure': receipt.get('failure'),
                      'cells_checked': len(receipt['cells'])}))
    return receipt['status'] != 'PASS'


if __name__ == '__main__':
    raise SystemExit(main())
