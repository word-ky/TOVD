"""Pinned Git-history/provenance audit; never opens active run predictions/results."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess

FREEZE = '6fec32243985ccc808123d851abf5f3dea10af99'
DISPATCH = '88668f76b22777459b5792dd28f88075f208c678'
START_HEAD = 'cca9af23452870d1a12ba1ab6a78ebe683e49cd1'
RUN = '20260912-210355-tovd-native30-primary'
RELEASE = '20260912-210306-tovd-native30-primary-freeze'
REMOTE = '/home/wenchang/asdasdsad/wjq/TOVD'
PREFIX = 'research_log/t013/'
MIRROR = 'research_log/remote_runs/' + RUN + '/'
ROOT = Path(__file__).resolve().parents[2]


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def lines(*args):
    return git(*args).decode('utf-8').splitlines()


def blob(revision, path):
    return git('show', revision + ':' + path)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def ancestor(before, after):
    return subprocess.run(['git', 'merge-base', '--is-ancestor', before, after],
                          cwd=ROOT, capture_output=True).returncode == 0


def category(path):
    if path.startswith('coordination/') or path == PREFIX + 'IMPLEMENTATION_NEXT.md':
        return 'coordination/reporting'
    if path in ['research_log/REMOTE.md', 'research_log/project_state.md',
                'research_log/session_log.md'] or path.startswith(MIRROR):
        return 'primary provenance/log mirror'
    if path == 'research/T013_YOLOWORLD_CONTINGENCY.md' or path.startswith('research_log/t013_yoloworld/'):
        return 'YOLO contingency preparation'
    if path.startswith(PREFIX):
        return 'pre-outcome verifier/test'
    return 'UNCLASSIFIED'


def excerpt(revision, path, needle):
    content = blob(revision, path)
    text_lines = content.decode('utf-8-sig').splitlines()
    matches = [{'line': i, 'text': line} for i, line in enumerate(text_lines, 1) if needle in line]
    return {'commit': lines('rev-parse', revision)[0], 'path': path,
            'sha256': sha(content), 'needle': needle, 'matches': matches,
            'found': bool(matches)}


def audit(head):
    freeze_bytes = blob(FREEZE, PREFIX + 'native30_freeze.json')
    freeze = json.loads(freeze_bytes)
    protected = {path: (expected, 'code_sha256.' + path)
                 for path, expected in freeze['code_sha256'].items()}
    for name, key in [('PLAN.md', 'plan_sha256'), ('vocabulary_native30.json', 'vocabulary_sha256'),
                      ('image_selection.json', 'selection_sha256'), ('data_receipt.json', 'data_receipt_sha256'),
                      ('image_sha256.json', 'image_manifest_sha256'),
                      ('native30_environment.txt', 'environment_sha256')]:
        protected[PREFIX + name] = (freeze[key], key)
    protected[PREFIX + 'native30_freeze.json'] = (sha(freeze_bytes), 'Git freeze blob SHA256')
    commits = lines('rev-list', '--reverse', '--topo-order', FREEZE + '..' + head)
    checks, rows = {}, []
    for path, (expected, source) in protected.items():
        before, after = blob(FREEZE, path), blob(head, path)
        rows.append({'path': path, 'hash_source': source, 'expected_sha256': expected,
                     'freeze_sha256': sha(before), 'head_sha256': sha(after),
                     'freeze_git_blob': lines('rev-parse', FREEZE + ':' + path)[0],
                     'head_git_blob': lines('rev-parse', head + ':' + path)[0],
                     'equal': before == after and sha(before) == expected})
    checks['all_protected_bytes_match'] = all(row['equal'] for row in rows)
    diff = git('diff', '--no-ext-diff', FREEZE, head, '--', *protected).decode('utf-8')
    checks['protected_endpoint_diff_empty'] = not diff
    # Compare every reachable post-freeze tree, catching a change later reverted.
    protected_commits = lines('log', '--full-history', '-m', '--format=%H', '--name-only',
                              FREEZE + '..' + head, '--', *protected)
    checks['no_intermediate_protected_edit'] = not protected_commits
    if not all(checks.values()):
        return {'task': 'T013-G4A1', 'task_start_head': head, 'freeze_commit': FREEZE,
                'status': 'PREOUTCOME_HISTORY_BLOCKER', 'checks': checks,
                'protected_paths': rows, 'protected_diff': diff,
                'protected_history': protected_commits,
                'active_primary_scientific_result_opened': False,
                'active_primary_prediction_content_opened': False}

    history = []
    all_changed = set()
    for commit in commits:
        parents = lines('show', '-s', '--format=%P', commit)[0].split()
        changed = set()
        for parent in parents:
            changed.update(lines('diff', '--name-only', parent, commit))
        all_changed.update(changed)
        history.append({'commit': commit, 'parents': parents,
                        'committer_time': lines('show', '-s', '--format=%cI', commit)[0],
                        'subject': lines('show', '-s', '--format=%s', commit)[0],
                        'changed_paths_against_all_parents': sorted(changed)})
    classified = [{'path': path, 'category': category(path)} for path in sorted(all_changed)]
    checks['all_postfreeze_paths_classified'] = all(row['category'] != 'UNCLASSIFIED' for row in classified)
    checks['no_postfreeze_scripts_or_tests_edits'] = not any(
        p.startswith(('scripts/', 'tests/')) for p in all_changed)

    chronology = {}
    chain = ['c07ce16', 'f63f571', '6548870', '02ba123', '259217c', 'eed8d1a',
             'd5dc807', '35fbfb7', FREEZE, DISPATCH, head]
    for before, after in zip(chain, chain[1:]):
        chronology[before + ' -> ' + after] = ancestor(before, after)
    checks['chronology_ancestry'] = all(chronology.values())
    metadata = json.loads(blob(DISPATCH, MIRROR + 'meta.json'))
    run_script = blob(DISPATCH, MIRROR + 'run.sh').decode()
    release_text = blob(DISPATCH, MIRROR + 'artifacts/resolved_release.txt').decode().strip()
    hash_text = blob(DISPATCH, MIRROR + 'artifacts/freeze_sha256.txt').decode()
    command = metadata['command']
    checks['dispatch_binding'] = (
        metadata['runId'] == RUN and metadata['releaseId'] == RELEASE
        and metadata['sessionName'] == 'autodl-' + RUN
        and release_text == REMOTE + '/releases/' + RELEASE
        and command.startswith('cd ' + release_text + ';')
        and command in run_script and '--freeze-commit ' + FREEZE in command
        and command.count('-m scripts.t013_native_run ') == 1
        and command.count('-m scripts.t013_analysis ') == 1
        and sha(freeze_bytes) + '  ' + PREFIX + 'native30_freeze.json' in hash_text
        and freeze['plan_sha256'] + '  ' + PREFIX + 'PLAN.md' in hash_text)
    provenance = []
    for name in ['run.sh', 'meta.json', 'artifacts/resolved_release.txt', 'artifacts/freeze_sha256.txt']:
        path = MIRROR + name
        provenance.append({'path': path, 'dispatch_sha256': sha(blob(DISPATCH, path)),
                           'head_sha256': sha(blob(head, path))})
    checks['dispatch_metadata_unchanged'] = all(
        item['dispatch_sha256'] == item['head_sha256'] for item in provenance)
    run_paths = sorted(p for p in all_changed if p.startswith('research_log/remote_runs/'))
    checks['only_one_postfreeze_run_mirror'] = all(p.startswith(MIRROR) for p in run_paths)
    checks['no_run_mirror_edits_after_dispatch'] = all(
        not any(p.startswith('research_log/remote_runs/') for p in item['changed_paths_against_all_parents'])
        for item in history if item['commit'] != DISPATCH)
    # Inventory all retained run metadata, not prediction/log/result files.
    native_runs = []
    for path in lines('ls-tree', '-r', '--name-only', head, 'research_log/remote_runs'):
        if path.endswith('/meta.json'):
            item = json.loads(blob(head, path))
            if '-m scripts.t013_native_run ' in item.get('command', ''):
                smoke = '--smoke-only' in item['command'].split('&&')[0].split()
                native_runs.append({'path': path, 'run_id': item['runId'], 'command': item['command'],
                                    'smoke_only': smoke})
    primary_runs = [item for item in native_runs if not item['smoke_only']]
    checks['one_committed_native_primary_command'] = len(primary_runs) == 1 and primary_runs[0]['run_id'] == RUN

    preserved = []
    for revision, path in [
        ('f63f571', 'research_log/remote_runs/20260912-195530-tovd-t013-native-parity/artifacts/native_parity.json'),
        ('6548870', PREFIX + 'PARITY_B_RESULTS.md'),
        ('6548870', 'research_log/remote_runs/20260912-202233-tovd-t013-parity-b/artifacts/parity_b.json')]:
        before, after = blob(revision, path), blob(head, path)
        preserved.append({'origin_commit': lines('rev-parse', revision)[0], 'path': path,
                          'origin_sha256': sha(before), 'head_sha256': sha(after), 'equal': before == after})
    checks['negative_prerequisite_artifacts_preserved'] = all(item['equal'] for item in preserved)
    evidence_specs = [
        ('original_gate1', 'c07ce16', 'coordination/CHATGPT_TO_CODEX.md', '>= 1.0 AP50'),
        ('original_gate2', 'c07ce16', 'coordination/CHATGPT_TO_CODEX.md', '>= 0.75 AP50'),
        ('original_gate2_contrast', 'c07ce16', 'coordination/CHATGPT_TO_CODEX.md', '>= 0.50 AP50'),
        ('reset_preserves_gates', '02ba123', 'coordination/CHATGPT_TO_CODEX.md', 'Do **not** weaken'),
        ('hf_rejection', '02ba123', 'coordination/CHATGPT_TO_CODEX.md', 'any failure rejects'),
        ('freeze_accepted', head, 'coordination/CHATGPT_REVIEW_LOG.md', 'The dispatch is protocol-compliant'),
        ('failure_rule', head, 'coordination/CHATGPT_REVIEW_LOG.md', 'before designing a restart'),
        ('p0_blindness', head, 'research_log/session_log.md', 'NoGroundingpartialAP/interaction/CI/mechanismmetricsread'),
        ('p1_blindness', head, 'research_log/session_log.md', 'Zero YOLO image inference;'),
        ('p2_blindness', head, 'coordination/CODEX_TO_CHATGPT.md', 'Zero YOLO/MMCV/MMDetection/MMYOLO'),
        ('ops1_single_writer', head, PREFIX + 'PRIMARY_OPS_CHECK.md', '721181'),
        ('stat1_blindness', head, 'research_log/session_log.md', 'No primary prediction/scientific artifact'),
        ('fin1_blindness', head, 'research_log/session_log.md', 'Primary cache was never passed'),
        ('repro1_blindness', head, 'research_log/session_log.md', 'active_primary_cache_accessed=false'),
        ('dec1_blindness', head, 'research_log/session_log.md', 'active_primary_scientific_result_opened=false'),
        ('latest_health_blindness', head, 'research_log/session_log.md', '377/1000 images'),
        ('yolo_no_rescue', head, PREFIX + 'FINAL_DECISION_CONTRACT.md', 'never mutate the Grounding state'),
    ]
    references = {name: excerpt(rev, path, needle) for name, rev, path, needle in evidence_specs}
    checks['review_evidence_references_exist'] = all(item['found'] for item in references.values())
    # Search committed reporting deltas only. Hits are context for engineering review,
    # not an automatic classifier of negation or proof about off-repository actions.
    reporting = [r['path'] for r in classified if r['category'] in
                 ('coordination/reporting', 'primary provenance/log mirror') and r['path'].endswith('.md')]
    review_hits = []
    for path in reporting:
        for line in lines('diff', '--unified=0', FREEZE, head, '--', path):
            if line.startswith('+') and not line.startswith('+++') and re.search(
                    r'restart|resume|dispatch|partial|primary.*(?:open|inspect|read)|YOLO.*(?:inference|install|load)',
                    line, re.I):
                review_hits.append({'path': path, 'added_text': line[1:]})
    return {'task': 'T013-G4A1', 'task_start_head': head, 'freeze_commit': FREEZE,
            'dispatch_commit': DISPATCH, 'recorded_utc': datetime.now(timezone.utc).isoformat(),
            'status': 'PREOUTCOME_HISTORY_CLEAN' if all(checks.values()) else 'PREOUTCOME_HISTORY_BLOCKER',
            'final_gate4': 'PENDING_COMPLETION_AND_RESEARCH_LEAD_REVIEW', 'checks': checks,
            'protected_paths': rows, 'protected_endpoint_diff': diff,
            'protected_intermediate_history': protected_commits,
            'chronology_ancestry': chronology, 'commit_history': history,
            'postfreeze_changed_paths': classified,
            'category_counts': dict(Counter(r['category'] for r in classified)),
            'dispatch_metadata': metadata, 'dispatch_provenance': provenance,
            'native_runner_command_inventory': native_runs,
            'preserved_negative_prerequisites': preserved,
            'outcome_blindness_and_protocol_references': references,
            'reporting_event_search_hits': review_hits,
            'engineering_history_review': {
                'scope': 'Committed history through task_start_head only; not proof of off-repository behavior.',
                'finding': 'No committed evidence of duplicate primary dispatch/restart/retune, partial-primary scientific use, or YOLO scientific execution.',
                'basis': 'Protected blob/history checks, run-metadata inventory, classified paths, and contextual review of reporting deltas/references in companion document.',
                'yolo_scope': 'Accepted P0/P1/P2 source/protocol/model-free preparation only; future cross-backbone evidence cannot replace primary.'},
            'external_asset_hashes_metadata_only': {key: freeze[key] for key in
                ['native_checkpoint_sha256', 'native_state_sha256', 'annotations_sha256']},
            'active_primary_scientific_result_opened': False,
            'active_primary_prediction_content_opened': False,
            'frozen_scientific_source_or_run_modified': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--head', default=START_HEAD)
    args = parser.parse_args()
    receipt = audit(args.head)
    receipt['helper_sha256'] = sha(Path(__file__).read_bytes())
    target = ROOT / PREFIX / 'gate4_preoutcome_history_receipt.json'
    target.write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: receipt[key] for key in ['task_start_head', 'status', 'checks']}, indent=2))
    raise SystemExit(0 if receipt['status'] == 'PREOUTCOME_HISTORY_CLEAN' else 1)
