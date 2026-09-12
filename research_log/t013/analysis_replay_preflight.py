"""Pinned REPRO1 smoke-only execution and evidence; run with existing project Python."""
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

import numpy as np

from analysis_replay_compare import compare

ROOT = Path('/home/wenchang/asdasdsad/wjq/TOVD')
RELEASE = ROOT/'releases/20260912-210306-tovd-native30-primary-freeze'
OLD_RELEASE = ROOT/'releases/20260912-205335-tovd-native30-pipeline'
SMOKE = ROOT/'runs/20260912-205428-tovd-native30-pipeline-smoke/artifacts'
ANNOTATIONS = ROOT/'shared/t013/coco/annotations/instances_val2017.json'
OUT = ROOT/'shared/t013/repro1'
FREEZE = '6fec32243985ccc808123d851abf5f3dea10af99'


def digest(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def main():
    receipt = {'task': 'T013-REPRO1', 'status': 'RUNNING', 'freeze_commit': FREEZE,
               'started_utc': datetime.now(timezone.utc).isoformat(), 'bindings': {}, 'runs': [],
               'active_primary_cache_accessed': False, 'primary_scientific_result_opened': False,
               'frozen_source_or_environment_modified': False}
    try:
        freeze_path = RELEASE/'research_log/t013/native30_freeze.json'
        freeze_sha = digest(freeze_path)
        assert freeze_sha == '50addfb8e247333b49fb22cda14570166b294101bb435b5a1b5bf688b4b3a91e'
        frozen = json.loads(freeze_path.read_text())
        expected = {str(freeze_path): freeze_sha, str(ANNOTATIONS): frozen['annotations_sha256'],
                    str(RELEASE/'research_log/t013/PLAN.md'): frozen['plan_sha256'],
                    str(SMOKE/'cache/run_receipt.json'): 'a1ec8408c5294935759b462f4f0663b8a5e7b9620acebd61bceb977a509bf0e5',
                    str(SMOKE/'cache/cache_manifest.jsonl'): '3d3623c2a6d78edd63b35c3efbdaf733df48eb1ffb9cefe36ea7e2daf2355a5f'}
        sources = ('scripts/t013_analysis.py', 'scripts/t013_coco.py', 'scripts/t013_diagnostics.py')
        for name in sources:
            expected[str(RELEASE/name)] = frozen['code_sha256'][name]
        for name, wanted in expected.items():
            actual = digest(Path(name))
            receipt['bindings'][name] = {'expected': wanted, 'actual': actual, 'equal': actual == wanted}
            assert actual == wanted, name
        smoke_receipt = json.loads((SMOKE/'cache/run_receipt.json').read_text())
        assert smoke_receipt['completed'] is True and smoke_receipt['kind'] == 'smoke_cached_pipeline'
        assert smoke_receipt['image_ids'] == [139, 285, 632]
        receipt['environment'] = {'python': sys.version, 'executable': sys.executable,
                                  'packages': {name: importlib.metadata.version(name) for name in
                                               ['numpy', 'pycocotools', 'torch', 'torchvision', 'transformers']},
                                  'thread_environment': {key: os.environ.get(key) for key in
                                                         ['OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS']}}
        pip = subprocess.run([sys.executable, '-m', 'pip', 'freeze'], capture_output=True, text=True)
        assert pip.returncode == 0, pip.stderr
        (OUT/'environment.txt').write_text(pip.stdout)
        receipt['environment']['pip_freeze_sha256'] = digest(OUT/'environment.txt')
        for tag in ('replay_a', 'replay_b'):
            target = OUT/tag
            target.mkdir()  # Fail rather than overwrite a prior replay; preserve all outputs.
            command = [sys.executable, '-m', 'scripts.t013_analysis', '--annotations', str(ANNOTATIONS),
                       '--run', str(SMOKE/'cache'), '--output', str(target), '--smoke-only']
            start = time.monotonic()
            with (OUT/(tag+'.log')).open('w') as log:
                completed = subprocess.run(command, cwd=RELEASE, stdout=log, stderr=subprocess.STDOUT)
            row = {'tag': tag, 'command': command, 'cwd': str(RELEASE), 'exit_code': completed.returncode,
                   'wall_seconds': time.monotonic()-start, 'output': str(target)}
            receipt['runs'].append(row)
            print(json.dumps(row), flush=True)
            assert completed.returncode == 0, tag
        receipt['replay_comparison'] = compare(OUT/'replay_a', OUT/'replay_b')
        assert receipt['replay_comparison']['status'] == 'PASS', 'replay A/B mismatch'
        result = json.loads((OUT/'replay_a/results.json').read_text())
        assert result['kind'] == 'engineering_smoke_not_scientific'
        assert result['image_count'] == 3 and result['replicates'] == 10 and result['seed'] == 20260913
        draws = np.load(OUT/'replay_a/paired_image_draws.npy', allow_pickle=False)
        assert draws.shape == (10, 3) and np.array_equal(draws, np.random.default_rng(20260913).integers(0, 3, (10, 3)))
        receipt['smoke_contract'] = {'image_count': 3, 'replicates': 10, 'seed': 20260913,
                                     'draw_shape': list(draws.shape), 'draw_dtype': str(draws.dtype), 'fixed_draws_exact': True}
        mutation = OUT/'mutation_negative_control'
        shutil.copytree(OUT/'replay_b', mutation)
        with np.load(mutation/'bootstrap_samples.npz', allow_pickle=False) as archive:
            arrays = {key: archive[key].copy() for key in archive.files}
        before = float(arrays['metrics'][0, 0, 0, 0])
        arrays['metrics'][0, 0, 0, 0] = before+1
        np.savez_compressed(mutation/'bootstrap_samples.npz', **arrays)
        rejection = compare(OUT/'replay_a', mutation)
        assert rejection['status'] == 'FAIL' and not rejection['artifacts']['bootstrap_samples.npz']['arrays']['metrics']['equal']
        receipt['negative_control'] = {'status': 'PASS', 'expected_comparator_status': 'FAIL',
                                      'mutation': 'scratch bootstrap metrics[0,0,0,0] += 1', 'comparison': rejection}
        original_hashes = {name: digest(OLD_RELEASE/name) if (OLD_RELEASE/name).is_file() else None for name in sources}
        receipt['original_analysis_source_hashes'] = original_hashes
        if all(original_hashes[name] == frozen['code_sha256'][name] for name in sources):
            original = compare(SMOKE/'analysis', OUT/'replay_a')
            receipt['original_smoke_comparison'] = original
            assert original['status'] == 'PASS', 'original same-source smoke mismatch'
        else:
            receipt['original_smoke_comparison'] = {'status': 'NOT COMPARED', 'reason': 'SOURCE VERSION NOT IDENTICAL/UNPROVEN'}
        receipt['status'] = 'PASS'
    except Exception as error:
        receipt['status'] = 'BLOCKED'
        receipt['failure'] = {'type': type(error).__name__, 'detail': str(error)}
    receipt['finished_utc'] = datetime.now(timezone.utc).isoformat()
    receipt['audit_sources_sha256'] = {name: digest(OUT/name) for name in ['analysis_replay_compare.py', 'analysis_replay_preflight.py']}
    (OUT/'analysis_replay_receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps({'status': receipt['status'], 'failure': receipt.get('failure')}), flush=True)
    return receipt['status'] != 'PASS'


if __name__ == '__main__':
    raise SystemExit(main())
