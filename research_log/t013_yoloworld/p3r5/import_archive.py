"""P3R5 single fixed-artifact download and raw-byte provenance check; no model imports."""
import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import urllib.parse
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
TEMP = ROOT / '.autodl/p3r5'
ARCHIVE = TEMP / 'artifact-10341040916.zip'
EXTRACT = TEMP / 'extracted'
SHA = '4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458'
HEAD = '0a9e6a004191c9ab20db4feeebab51d88cc3760d'
ENDPOINT = 'https://api.github.com/repos/word-ky/TOVD/actions/artifacts/10341040916/zip'

def digest(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

# GitHub's delivery redirect must not receive the GitHub Authorization header.
class DeliveryRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        result = super().redirect_request(req, fp, code, msg, headers, newurl)
        if urllib.parse.urlsplit(req.full_url).netloc != urllib.parse.urlsplit(newurl).netloc:
            result.remove_header('Authorization')
        return result

r = {'task': 'T013-YW-P3R5', 'task_started_at': '2026-09-14T09:58:18.512Z',
     'task_start_head': '06610b250e74166fd56c1a49b7d011441ded38d6',
     'lead_instruction_commit': 'ae07716fb90c9b8979aad4ed695ef5f3b498af05',
     'archive_download_count': 0, 'download_endpoint': ENDPOINT,
     'command': 'D:/anaconda3/python.exe research_log/t013_yoloworld/p3r5/import_archive.py',
     'archive_path': str(ARCHIVE), 'extraction_path': str(EXTRACT),
     'local_free_space': shutil.disk_usage(ROOT)._asdict(),
     'already_present_exact': False, 'temporary_files_retained': True}
state = 'YW_P3R5_AMBIGUOUS_RETURN_TO_LEAD'
try:
    artifact = json.loads((OUT / 'artifact.json').read_text())
    run = json.loads((OUT / 'run.json').read_text())
    r['artifact_metadata'] = artifact
    r['run_binding'] = {k: run[k] for k in ['id', 'run_attempt', 'head_sha', 'status', 'conclusion']}
    state = 'YW_P3R5_ARTIFACT_BINDING_MISMATCH_RETURN_TO_LEAD'
    assert artifact['id'] == 10341040916
    assert artifact['name'] == 't013-yw-s-stage2-4466ab94-relay'
    assert artifact['size_in_bytes'] == 305061442
    assert artifact['digest'] == 'sha256:2589f9b63f57e51d4646ea114cdbff0bf7896d7988c8a499360bb077ef76c5bf'
    assert artifact['workflow_run']['id'] == run['id'] == 34827628282
    assert artifact['workflow_run']['head_sha'] == run['head_sha'] == HEAD
    assert run['run_attempt'] == 1 and run['conclusion'] == 'success'
    state = 'YW_P3R5_ARTIFACT_UNAVAILABLE_RETURN_TO_LEAD'
    assert artifact['expired'] is False
    assert datetime.datetime.fromisoformat(artifact['expires_at'].replace('Z', '+00:00')) > datetime.datetime.now(datetime.timezone.utc)
    env = dict(os.environ, GIT_TERMINAL_PROMPT='0', GCM_INTERACTIVE='Never')
    credential = subprocess.run(['git', 'credential', 'fill'], input='protocol=https\nhost=github.com\n\n', capture_output=True, text=True, env=env)
    assert credential.returncode == 0
    token = dict(line.split('=', 1) for line in credential.stdout.splitlines() if '=' in line)['password']
    TEMP.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(ENDPOINT, headers={'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28', 'User-Agent': 'TOVD-P3R5'})
    r['download_started_at'] = now()
    with ARCHIVE.open('xb') as target:
        r['archive_download_count'] = 1
        with urllib.request.build_opener(DeliveryRedirect()).open(req, timeout=60) as response:
            r['download_http_status'] = response.status
            r['delivery_host'] = urllib.parse.urlsplit(response.url).hostname
            shutil.copyfileobj(response, target, length=1024 * 1024)
    r['download_stopped_at'] = now()
    r['download_exit_code'] = 0
    r['archive_bytes'] = ARCHIVE.stat().st_size
    r['archive_sha256'] = digest(ARCHIVE)
    r['archive_digest_matches'] = r['archive_sha256'] == artifact['digest'].split(':')[1]
    state = 'YW_P3R5_ARTIFACT_BINDING_MISMATCH_RETURN_TO_LEAD'
    assert r['archive_bytes'] == artifact['size_in_bytes'] and r['archive_digest_matches']
    with zipfile.ZipFile(ARCHIVE) as z:
        members = z.infolist()
        r['archive_members'] = [{'name': m.filename, 'bytes': m.file_size, 'external_attr': m.external_attr, 'create_system': m.create_system} for m in members]
        names = [m.filename for m in members]
        assert len(names) == len(set(names)) == 2
        assert set(names) == {'s_stage2-4466ab94.pth', 'acquisition_receipt.json'}
        for m in members:
            p = PurePosixPath(m.filename)
            mode = m.external_attr >> 16
            assert not p.is_absolute() and '..' not in p.parts and len(p.parts) == 1
            assert '\\' not in m.filename and ':' not in m.filename and not m.is_dir()
            assert not stat.S_ISLNK(mode) and stat.S_IFMT(mode) in (0, stat.S_IFREG)
        r['member_safety_checks'] = {'exact_two_regular_files': True, 'duplicates': False, 'traversal': False, 'absolute_paths': False, 'symlinks': False, 'nesting_or_extra': False}
        EXTRACT.mkdir()
        for m in members:
            with z.open(m) as source, (EXTRACT / m.filename).open('xb') as target:
                shutil.copyfileobj(source, target)
    receipt = EXTRACT / 'acquisition_receipt.json'
    r['embedded_receipt_bytes'] = receipt.stat().st_size
    r['embedded_receipt_sha256'] = digest(receipt)
    assert r['embedded_receipt_sha256'] == 'd64080965c78597c853d3f99c34cdf2885d7d5154f0f1141cd81b4639270241f'
    parsed = json.loads(receipt.read_text())
    accepted = json.loads((OUT.parent / 'p3r4/acquisition_receipt.json').read_text())
    keys = ['verified', 'run_id', 'run_attempt', 'workflow_commit', 'initial_url', 'expected_bytes', 'observed_bytes', 'expected_sha256', 'observed_sha256']
    r['embedded_receipt_binding'] = {k: parsed[k] for k in keys}
    assert all(parsed[k] == accepted[k] for k in keys) and parsed['verified'] is True
    r['receipt_binding_matches_accepted_p3r4'] = True
    checkpoint = EXTRACT / 's_stage2-4466ab94.pth'
    r['checkpoint_bytes'] = checkpoint.stat().st_size
    r['checkpoint_sha256'] = digest(checkpoint)
    state = 'YW_P3R5_CHECKPOINT_HASH_MISMATCH_RETURN_TO_LEAD'
    assert r['checkpoint_bytes'] == 305058902 and r['checkpoint_sha256'] == SHA
    r['archive_validation_passed'] = True
    r['state'] = 'ARCHIVE_VERIFIED_PENDING_SERVER_PLACEMENT'
except Exception as e:
    r['state'] = state
    r['error_type'] = type(e).__name__
    r.setdefault('download_exit_code', 1 if r['archive_download_count'] else None)
finally:
    r['local_validation_stopped_at'] = now()
    (OUT / 'archive_validation.json').write_text(json.dumps(r, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: r.get(k) for k in ['state', 'archive_download_count', 'download_exit_code', 'archive_bytes', 'archive_sha256', 'checkpoint_bytes', 'checkpoint_sha256', 'error_type']}, indent=2))
raise SystemExit(0 if r.get('archive_validation_passed') else 1)
