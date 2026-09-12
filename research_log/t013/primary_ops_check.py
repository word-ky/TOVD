"""T013-OPS1 one-shot read-only metadata audit; never deserialize predictions.

Run with server system python3; JSON goes to stdout, outside the primary run.
NPZ access is limited to stat and streaming SHA256 of opaque bytes.
"""
import hashlib
import json
import math
import os
from pathlib import Path
import statistics
import subprocess
from datetime import datetime, timezone

ROOT = Path('/home/wenchang/asdasdsad/wjq/TOVD')
RUN_ID = '20260912-210355-tovd-native30-primary'
RELEASE_ID = '20260912-210306-tovd-native30-primary-freeze'
COMMIT = '6fec32243985ccc808123d851abf5f3dea10af99'
FREEZE_SHA = '50addfb8e247333b49fb22cda14570166b294101bb435b5a1b5bf688b4b3a91e'
RUN = ROOT / 'runs' / RUN_ID
RELEASE = ROOT / 'releases' / RELEASE_ID
CACHE = RUN / 'artifacts/cache'
CONDITIONS = ['clean', 'gaussian_noise', 'motion_blur', 'fog', 'jpeg_compression']
VOCABULARIES = ['V0', 'Vhard30', 'Vrand30']
TMUX = 'autodl-' + RUN_ID


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def progress():
    # Only completion/exit receipts, never other log lines or scientific output.
    latest = None
    exits = []
    for line in (RUN / 'train.log').read_text().splitlines():
        if line.startswith('{"completed_images":'):
            data = json.loads(line)
            latest = {k: data[k] for k in ('completed_images', 'total_images', 'seconds')}
        elif line.startswith('[autodl] exit_code='):
            exits.append(line)
    return {'progress': latest, 'exit_receipts': exits}


def process_snapshot():
    processes = {}
    unreadable = 0
    for path in Path('/proc').iterdir():
        if not path.name.isdecimal():
            continue
        try:
            args = [s.decode(errors='replace') for s in (path / 'cmdline').read_bytes().split(b'\0') if s]
            status = (path / 'status').read_text()
            parent = int(next(s.split()[1] for s in status.splitlines() if s.startswith('PPid:')))
            processes[int(path.name)] = {'args': args, 'ppid': parent}
        except (FileNotFoundError, ProcessLookupError):
            continue
        except PermissionError:
            unreadable += 1
    targets = []
    for pid, item in processes.items():
        args = item['args']
        # Exact cache argument catches both inference and an unexpected analysis
        # process targeting this cache; do not print unrelated process commands.
        if str(CACHE) in args:
            path = Path('/proc') / str(pid)
            ancestry = []
            parent = item['ppid']
            while parent in processes and parent not in ancestry:
                ancestry.append(parent)
                parent = processes[parent]['ppid']
            targets.append({'pid': pid, 'ppid': item['ppid'], 'args': args,
                            'cwd': os.readlink(path / 'cwd'),
                            'exe': os.readlink(path / 'exe'), 'ancestor_pids': ancestry})
    pane = subprocess.run(['tmux', 'list-panes', '-t', TMUX, '-F', '#{pane_pid}'],
                          capture_output=True, text=True)
    panes = [int(x) for x in pane.stdout.split()] if pane.returncode == 0 else []
    return {'cache_target_processes': targets, 'proc_entries_unreadable': unreadable,
            'tmux_alive': pane.returncode == 0, 'tmux_pane_pids': panes,
            'tmux_error': pane.stderr.strip()}


def main():
    started = datetime.now(timezone.utc).isoformat()
    start_progress = progress()
    start_processes = process_snapshot()
    freeze_path = RELEASE / 'research_log/t013/native30_freeze.json'
    freeze = json.loads(freeze_path.read_bytes())
    selection_path = RELEASE / 'research_log/t013/image_selection.json'
    selection = json.loads(selection_path.read_bytes())
    ids = selection['primary_ids']
    completed = start_progress['progress']['completed_images']
    closed_ids = ids[:completed]  # terminal receipt is emitted AFTER all 15 writes
    expected_pairs = {(c, v) for c in CONDITIONS for v in VOCABULARIES}

    # Metadata snapshot for all cache paths. Layout is condition/vocabulary/ID,
    # so per-image storage is the sum of its 15 files, not an image directory.
    by_image = {}
    unexpected = []
    for path in sorted((CACHE / 'raw').rglob('*')):
        rel = path.relative_to(CACHE / 'raw')
        parts = rel.parts
        if path.is_dir():
            valid = ((len(parts) == 1 and parts[0] in CONDITIONS) or
                     (len(parts) == 2 and tuple(parts) in expected_pairs))
            if not valid:
                unexpected.append(rel.as_posix() + '/')
            continue
        valid = (len(parts) == 3 and tuple(parts[:2]) in expected_pairs and
                 parts[2].endswith('.npz') and parts[2][:-4].isdecimal())
        if not valid:
            unexpected.append(rel.as_posix())
            continue
        image_id = int(parts[2][:-4])
        if image_id not in ids or parts[2] != f'{image_id:012d}.npz':
            unexpected.append(rel.as_posix())
        st = path.stat()
        by_image.setdefault(image_id, {})[tuple(parts[:2])] = {
            'path': 'raw/' + rel.as_posix(), 'size_bytes': st.st_size,
            'allocated_bytes': st.st_blocks * 512, 'mtime_ns': st.st_mtime_ns}
    bad_closed = [{'image_id': i,
                   'missing': [list(p) for p in sorted(expected_pairs - set(by_image.get(i, {})))]}
                  for i in closed_ids if set(by_image.get(i, {})) != expected_pairs]
    inflight = [{'image_id': i, 'cell_count': len(cells)}
                for i, cells in by_image.items() if i not in closed_ids]

    center = (completed - 1) / 2
    middle_positions = sorted(sorted(range(3, completed - 3), key=lambda i: (abs(i-center), i))[:4])
    positions = [0, 1, 2] + middle_positions + list(range(completed-3, completed))
    sample_ids = [closed_ids[i] for i in positions]
    # Manifest contains provenance hashes/paths only, never prediction arrays.
    manifest = {}
    manifest_bytes = (CACHE / 'cache_manifest.jsonl').read_bytes()
    complete_lines = manifest_bytes.rpartition(b'\n')[0].splitlines()
    for line in complete_lines:
        row = json.loads(line)
        if row['image_id'] in sample_ids:
            manifest[row['raw_path']] = row['raw_sha256']
    samples = []
    for image_id in sample_ids:
        for pair in sorted(expected_pairs):
            item = dict(by_image[image_id][pair])
            path = CACHE / item['path']
            before = path.stat()
            digest = sha(path)
            after = path.stat()
            item.update(image_id=image_id, sha256=digest,
                        manifest_sha256=manifest.get(item['path']),
                        matches_manifest=digest == manifest.get(item['path']),
                        unchanged_during_hash=(before.st_size, before.st_mtime_ns) ==
                                              (after.st_size, after.st_mtime_ns))
            samples.append(item)

    meta = json.loads((RUN / 'meta.json').read_bytes())
    receipt = json.loads((CACHE / 'run_receipt.json').read_bytes())
    bindings = {
        'freeze_sha_matches': sha(freeze_path) == FREEZE_SHA,
        'meta_run': meta['runId'] == RUN_ID,
        'meta_release': meta['releaseId'] == RELEASE_ID,
        'meta_tmux': meta['sessionName'] == TMUX,
        'meta_command_freeze': COMMIT in meta['command'],
        'resolved_release': (RUN / 'artifacts/resolved_release.txt').read_text().strip() == str(RELEASE),
        'receipt_kind': receipt['kind'] == 'T013-NATIVE30-primary',
        'receipt_freeze': receipt['freeze_commit'] == COMMIT,
        'receipt_ids': receipt['image_ids'] == ids,
        'receipt_vocab': receipt['vocabulary_sha256'] == freeze['vocabulary_sha256'],
        'receipt_selection': receipt['selection_sha256'] == freeze['selection_sha256'],
        'initial_model_state': receipt['state_before'] == freeze['native_state_sha256'],
        'receipt_cpu_four_threads': receipt['device'] == 'cpu' and receipt['threads'] == 4,
    }
    bound_files = dict(freeze['code_sha256'])
    for path, key in [('vocabulary_native30.json', 'vocabulary_sha256'),
                      ('image_selection.json', 'selection_sha256'),
                      ('image_sha256.json', 'image_manifest_sha256'),
                      ('native30_environment.txt', 'environment_sha256'),
                      ('PLAN.md', 'plan_sha256'), ('data_receipt.json', 'data_receipt_sha256')]:
        bound_files['research_log/t013/' + path] = freeze[key]
    file_checks = {name: {'expected': digest, 'observed': sha(RELEASE / name)}
                   for name, digest in bound_files.items()}
    bindings['frozen_source_and_provenance_files'] = all(x['expected'] == x['observed'] for x in file_checks.values())
    launch_hashes = (RUN / 'artifacts/freeze_sha256.txt').read_text().splitlines()
    bindings['launch_freeze_and_plan_hashes'] = launch_hashes == [
        FREEZE_SHA + '  research_log/t013/native30_freeze.json',
        freeze['plan_sha256'] + '  research_log/t013/PLAN.md']

    logical = [sum(x['size_bytes'] for x in by_image[i].values()) for i in closed_ids]
    allocated = [sum(x['allocated_bytes'] for x in by_image[i].values()) for i in closed_ids]
    ordered = sorted(allocated)
    rank = .95 * (len(ordered)-1)
    lo, hi = math.floor(rank), math.ceil(rank)
    p95 = ordered[lo] + (rank-lo) * (ordered[hi]-ordered[lo])
    remaining = len(ids) - completed
    projected = p95 * remaining
    required = math.ceil(1.20 * projected + 8 * 2**30)
    statvfs = os.statvfs(ROOT)
    free = statvfs.f_bavail * statvfs.f_frsize
    ending = process_snapshot()
    end_progress = progress()
    processes = ending['cache_target_processes']
    writer_ok = (len(processes) == 1 and 'scripts.t013_native_run' in processes[0]['args'] and
                 '--freeze-commit' in processes[0]['args'] and
                 processes[0]['args'][processes[0]['args'].index('--freeze-commit')+1] == COMMIT and
                 processes[0]['cwd'] == str(RELEASE) and ending['tmux_alive'] and
                 any(pid in processes[0]['ancestor_pids'] for pid in ending['tmux_pane_pids']))
    inflight_ok = len(inflight) <= 1 and all(x['image_id'] == ids[completed] for x in inflight)
    gates = {'exact_single_writer_binding': writer_ok,
             'all_closed_images_15_cells': not bad_closed,
             'no_unexpected_paths': not unexpected,
             'at_most_next_image_inflight': inflight_ok,
             'opaque_samples_readable_hash_consistent': all(x['matches_manifest'] and x['unchanged_during_hash'] for x in samples),
             'provenance_consistent': all(bindings.values()),
             'disk_safety': free >= required,
             'process_still_healthy': ending['tmux_alive'] and not end_progress['exit_receipts']}
    result = {
        'task': 'T013-OPS1', 'started_at': started, 'finished_at': datetime.now(timezone.utc).isoformat(),
        'status': 'PASS' if all(gates.values()) else 'BLOCKED', 'checks': gates,
        'run_id': RUN_ID, 'release_id': RELEASE_ID, 'freeze_commit': COMMIT,
        'process_start': start_processes, 'process_end': ending,
        'progress_start': start_progress, 'progress_end': end_progress,
        'structure': {'closed_image_count': completed, 'checked_closed_images': len(closed_ids),
                      'expected_cells_per_image': 15, 'observed_closed_cells': sum(len(by_image.get(i, {})) for i in closed_ids),
                      'conditions': CONDITIONS, 'vocabularies': VOCABULARIES,
                      'bad_closed_images': bad_closed, 'inflight_images': inflight,
                      'unexpected_paths': unexpected, 'all_observed_cells': sum(map(len, by_image.values())),
                      'snapshot_rule': 'closed prefix certified by start terminal completion receipt; next image may be in flight'},
        'sample': {'rule': 'first3 + nearest4 to (n-1)/2 completed position, ties lower position + latest3',
                   'zero_based_positions': positions, 'image_ids': sample_ids, 'files': samples},
        'provenance': {'checks': bindings, 'file_checks': file_checks,
                       'run_receipt_sha256': sha(CACHE / 'run_receipt.json'),
                       'initial_model_state_sha256': receipt['state_before'],
                       'model_state_after_not_yet_verified': 'state_after' not in receipt,
                       'native_source_revision_from_freeze': freeze['native_source_revision'],
                       'checkpoint_sha256_from_freeze': freeze['native_checkpoint_sha256'],
                       'launch_hash_receipt': launch_hashes},
        'storage': {'basis': 'sum st_blocks*512 of 15 closed-image cell files; no image directories in transposed layout',
                    'closed_logical_bytes_total': sum(logical), 'closed_allocated_bytes_total': sum(allocated),
                    'median_bytes_per_closed_image': statistics.median(allocated),
                    'p95_bytes_per_closed_image': p95, 'p95_method': 'linear interpolation rank=.95*(n-1)',
                    'remaining_images': remaining, 'projected_remaining_bytes': projected,
                    'free_now_bytes': free, 'required_safety_bytes': required,
                    'safety_formula': 'ceil(1.20*p95_bytes_per_image*remaining_images + 8*2**30)',
                    'safety_margin_bytes': free-required, 'passes': free >= required},
        'no_prediction_deserialization': True, 'no_scientific_metric_inspection': True,
        'no_primary_or_yolo_runtime_mutation': True,
    }
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
