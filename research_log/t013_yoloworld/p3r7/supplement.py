"""Narrow read-only follow-up for log rotation ordering and transitional package."""
import datetime
import json
from pathlib import Path
import subprocess

rows = []
for label, command in [
    ('recent_update_timeline', "zgrep -h -E '^2026-09-(1[0-4]) .* (nvidia|libnvidia|linux-modules-nvidia)' /var/log/dpkg.log* | sort"),
    ('transitional_package', "dpkg-query -W -f='${binary:Package}\n${Version}\n${Status}\n${Depends}\n${Description}\n' nvidia-driver-570-server"),
    ('dkms_status', 'dkms status'),
]:
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    p = subprocess.run(['bash', '-c', command], capture_output=True, text=True)
    rows.append(dict(label=label, command=command, started_at=started,
                     stopped_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                     exit_code=p.returncode, stdout=p.stdout, stderr=p.stderr))
Path(__file__).with_name('supplement_ledger.json').write_text(json.dumps(rows, indent=2) + '\n')
