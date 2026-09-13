"""Pinned CF2 completed-smoke rehearsal and provenance; never primary analysis."""
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys
import time

import numpy as np
import torch

ROOT = Path('/home/wenchang/asdasdsad/wjq/TOVD')
FROZEN = ROOT / 'releases/20260912-210306-tovd-native30-primary-freeze'
CACHE = ROOT / 'runs/20260912-205428-tovd-native30-pipeline-smoke/artifacts/cache'
REFERENCE = ROOT / 'shared/t013/repro1/replay_a'
ANNOTATIONS = ROOT / 'shared/t013/coco/annotations/instances_val2017.json'
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(FROZEN))

from canonical_counterfactual_analysis import evaluate_smoke, paired_summary


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    receipt = {'task': 'T013-CF2', 'status': 'RUNNING',
               'task_start_head': 'a1588cb2ff11e04aeebb90029ce7b19ca0e48b74',
               'freeze_commit': '6fec32243985ccc808123d851abf5f3dea10af99',
               'cf1_commit': '8154004f5574721903ee297a8a5aade729b1e131',
               'bindings': {}, 'reference': {}, 'replays': [],
               'environment': {'python': sys.version, 'executable': sys.executable,
                               'torch': torch.__version__, 'numpy': np.__version__,
                               'pycocotools': importlib.metadata.version('pycocotools'),
                               'topk_device': 'cpu',
                               'threads': {k: os.environ.get(k) for k in ('OMP_NUM_THREADS','MKL_NUM_THREADS')}},
               'scope': {'active_primary_cache_accessed': False, 'primary_scientific_content_opened': False,
                         'primary_fin1_or_replay': False, 'detector_inference': False,
                         'original_run_reference_release_mutation': False, 'new_gate_or_threshold': False,
                         'yolo_runtime': False, 't014_execution': False,
                         'annotations_used_only_for_completed_smoke': True,
                         'primary_counterfactual_execution_authorized': False}}
    names = ['canonical_topk_counterfactual.py','canonical_counterfactual_analysis.py',
             'test_canonical_counterfactual_analysis.py','rehearse_canonical_counterfactual.py',
             'CANONICAL_COUNTERFACTUAL_ANALYSIS_CONTRACT.md']
    receipt['source_sha256'] = {name: digest(OUT / name) for name in names}
    try:
        assert torch.__version__.split('+')[0] == '2.4.0'
        assert np.__version__ == '1.26.4'
        assert receipt['environment']['pycocotools'] == '2.0.8'
        expected = {
            FROZEN/'scripts/t013_coco.py': 'bd3245235a6dcd455224ea7eb737b07875920b0a08b34f30e706dfc6a9ca9e81',
            FROZEN/'scripts/t013_analysis.py': '74cc73e71385e5d38e3fbe68ff03a0f11da30e67ff39b436da90422f72e99f9c',
            FROZEN/'scripts/t013_diagnostics.py': 'ae7e61feaa5701ca9580c9c48901f99d09e9986b560c2821073100c94645a41e',
            OUT/'canonical_topk_counterfactual.py': 'cef3e87ea1a05b40dc36522022b50280f35e8caf78dbcedcb7a47ce27cf01539',
            ANNOTATIONS: 'e8c7f7908f1d7278341fae127d0da654f102f11bd7b21d8aeefa635b8c810b6f',
            CACHE/'run_receipt.json': 'a1ec8408c5294935759b462f4f0663b8a5e7b9620acebd61bceb977a509bf0e5',
            CACHE/'cache_manifest.jsonl': '3d3623c2a6d78edd63b35c3efbdaf733df48eb1ffb9cefe36ea7e2daf2355a5f',
        }
        for path, wanted in expected.items():
            actual = digest(path)
            receipt['bindings'][str(path)] = {'expected': wanted, 'actual': actual}
            assert actual == wanted, str(path)
        from scripts import t013_coco, t013_analysis, t013_diagnostics
        for module in (t013_coco,t013_analysis,t013_diagnostics):
            assert Path(module.__file__).resolve().is_relative_to(FROZEN)
        rp = REFERENCE.parent / 'analysis_replay_receipt.json'
        reference_receipt = json.loads(rp.read_text())
        semantic_digest = hashlib.sha256(json.dumps(reference_receipt, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        assert semantic_digest == REPRO1_SEMANTIC_SHA256, 'accepted REPRO1 receipt mismatch'
        assert reference_receipt['status'] == 'PASS'
        assert reference_receipt['runs'][0]['output'] == str(REFERENCE)
        assert reference_receipt['runs'][0]['cwd'] == str(FROZEN)
        receipt['reference']['accepted_receipt'] = {'path': str(rp), 'sha256': digest(rp),
                                                   'semantic_sha256': semantic_digest}
        for name in ('results.json','bootstrap_samples.npz','paired_image_draws.npy'):
            receipt['reference'][name] = {'path': str(REFERENCE/name), 'sha256': digest(REFERENCE/name)}
        ref = json.loads((REFERENCE/'results.json').read_text())
        assert ref['kind'] == 'engineering_smoke_not_scientific'
        assert ref['image_count'] == 3 and ref['replicates'] == 10 and ref['seed'] == 20260913
        assert ref['conditions'] == t013_analysis.CONDITIONS and ref['vocabularies'] == t013_analysis.VOCABS
        assert ref['metric_order'][:4] == ['AP','AP50','AR','AR50']
        orig_point = np.asarray(ref['point_metrics'])[:, :, :4]
        with np.load(REFERENCE/'bootstrap_samples.npz', allow_pickle=False) as archive:
            orig_samples = archive['metrics'][:, :, :, :4]
        draws = np.load(REFERENCE/'paired_image_draws.npy', allow_pickle=False)
        assert draws.shape == (10,3) and draws.dtype == np.int64
        np.testing.assert_array_equal(draws, t013_coco.paired_bootstrap_indices(3, seed=20260913, replicates=10))
        receipt['draws'] = {'shape': list(draws.shape), 'dtype': str(draws.dtype),
                            'sha256': digest(REFERENCE/'paired_image_draws.npy'),
                            'exact_reference_matrix_used': True, 'regenerated_exact': True}
        command = [sys.executable,'-m','unittest','-v','test_canonical_counterfactual_analysis']
        tests = subprocess.run(command, cwd=OUT, capture_output=True, text=True)
        (OUT/'canonical_counterfactual_tests.txt').write_text(tests.stdout+tests.stderr)
        receipt['tests'] = {'command': command, 'count': 6, 'exit_code': tests.returncode,
                            'log_sha256': digest(OUT/'canonical_counterfactual_tests.txt')}
        assert tests.returncode == 0, 'arithmetic tests failed'
        smoke = json.loads((CACHE/'run_receipt.json').read_text())
        assert smoke['completed'] and smoke['image_ids'] == [139,285,632]
        dataset = json.loads(ANNOTATIONS.read_text())
        for tag in ('replay_a','replay_b'):
            dest = OUT/tag
            dest.mkdir()
            started = time.monotonic()
            point, samples = evaluate_smoke(dataset, [139,285,632], CACHE/'raw', draws)
            np.testing.assert_array_equal(point[:,0,:], orig_point[:,0,:])
            np.testing.assert_array_equal(samples[:,:,0,:], orig_samples[:,:,0,:])
            summary, descriptor_samples = paired_summary(orig_point[:,:,1],point[:,:,1],
                                                          orig_samples[:,:,:,1],samples[:,:,:,1])
            np.save(dest/'paired_image_draws.npy',draws)
            np.savez_compressed(dest/'metrics.npz',point=point,samples=samples)
            np.savez_compressed(dest/'descriptor_samples.npz',**descriptor_samples)
            (dest/'descriptors.json').write_text(json.dumps(summary,indent=2)+'\n')
            receipt['replays'].append({'tag': tag, 'output': str(dest),
                'wall_seconds': time.monotonic()-started, 'v0_point_exact': '5x4',
                'v0_bootstrap_exact': '10x5x4', 'hard_random_cells_completed': 10,
                'smoke_raw_cells': 45, 'descriptor_fields': list(descriptor_samples),
                'artifact_sha256': {name: digest(dest/name) for name in (
                    'paired_image_draws.npy','metrics.npz','descriptor_samples.npz','descriptors.json')}})
            print(json.dumps({'replay':tag,'status':'PASS'}),flush=True)
        comparisons = {}
        for name in ('metrics.npz','descriptor_samples.npz'):
            with np.load(OUT/'replay_a'/name) as left, np.load(OUT/'replay_b'/name) as right:
                assert left.files == right.files
                for key in left.files:
                    np.testing.assert_array_equal(left[key],right[key])
                comparisons[name] = {'exact':True,'arrays':left.files}
        for name in ('paired_image_draws.npy','descriptors.json'):
            assert (OUT/'replay_a'/name).read_bytes() == (OUT/'replay_b'/name).read_bytes()
            comparisons[name] = {'exact':True}
        receipt.update(status='PASS',replay_comparison=comparisons)
    except Exception as error:
        receipt.update(status='BLOCKED',failure={'type':type(error).__name__,'detail':str(error)})
    (OUT/'canonical_counterfactual_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'status':receipt['status'],'failure':receipt.get('failure')}),flush=True)
    return receipt['status'] != 'PASS'


REPRO1_SEMANTIC_SHA256 = 'ac85e73231b4fc45e670fe82357a031cc0dfe25ad91fdd573efb61db701972a2'

if __name__ == '__main__':
    raise SystemExit(main())
