"""Read-only P3R7 host evidence. Writes only this project's command ledger."""
import datetime
import json
import os
from pathlib import Path
import shlex
import subprocess

OUT = Path(__file__).resolve().parent
BASE = '/home/wenchang/asdasdsad/wjq/TOVD/shared/t013_yoloworld'
ledger = []
def run(label, command):
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    p = subprocess.run(['bash', '-c', command], capture_output=True, text=True)
    row = dict(label=label, command=command, started_at=start,
               stopped_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
               exit_code=p.returncode, stdout=p.stdout, stderr=p.stderr)
    ledger.append(row)
    (OUT / 'command_ledger.json').write_text(json.dumps(ledger, indent=2) + '\n')
    print(label, 'exit', p.returncode, flush=True)
    return p.stdout.strip()

run('boot', 'date -Is; uname -a; uname -r; uptime; uptime -s; who -b')
run('python', BASE + '/env/bin/python --version')
run('pip_pre', BASE + '/env/bin/python -m pip list --format=json')
run('loaded_version', 'cat /proc/driver/nvidia/version')
run('loaded_modules', "lsmod | grep '^nvidia'")
run('proc_gpu_information', 'for p in /proc/driver/nvidia/gpus/*/information; do printf "%s\\n" "$p"; cat "$p"; done')
module = run('module_path', 'modinfo -n nvidia')
run('module_version', 'modinfo -F version nvidia')
run('module_vermagic', 'modinfo -F vermagic nvidia')
if module:
    q = shlex.quote(module)
    run('module_realpath', 'readlink -f ' + q)
    run('module_stat', 'stat ' + q)
    run('module_hash', 'sha256sum ' + q)
    run('module_package', 'dpkg-query -S ' + q)
libs = run('linker_cache', "ldconfig -p | grep -E 'libnvidia-ml[.]so[.]1|libcuda[.]so[.]1'")
run('library_search_environment', 'printf "LD_LIBRARY_PATH=%s\\nLD_PRELOAD=%s\\n" "$LD_LIBRARY_PATH" "$LD_PRELOAD"')
for index, line in enumerate(libs.splitlines()):
    if '=>' not in line:
        continue
    path = line.split('=>', 1)[1].strip()
    real = run('library_realpath_' + str(index), 'readlink -f ' + shlex.quote(path))
    run('library_stat_' + str(index), 'stat ' + shlex.quote(real))
    run('library_package_' + str(index), 'dpkg-query -S ' + shlex.quote(real))
run('installed_packages', "dpkg-query -W -f='${binary:Package}\t${Version}\t${db:Status-Abbrev}\n' '*nvidia*' '*libcuda*' '*cuda-drivers*'")
smi = run('smi_path', 'command -v nvidia-smi')
if smi:
    run('smi_realpath', 'readlink -f ' + shlex.quote(smi))
    run('smi_stat', 'stat ' + shlex.quote(smi))
    run('smi_package', 'dpkg-query -S ' + shlex.quote(smi))
run('smi_list_SINGLE_ATTEMPT', 'nvidia-smi -L')
run('package_timeline', "zgrep -h -E ' (install|upgrade|configure|status installed) (nvidia|libnvidia|linux-modules-nvidia|cuda-drivers)' /var/log/dpkg.log* | tail -n 100")
run('device_nodes', 'ls -l /dev/nvidia*')
run('device_holders', 'fuser -v /dev/nvidia*')
run('pip_post', BASE + '/env/bin/python -m pip list --format=json')
run('checkpoint_stat', 'stat ' + BASE + '/weights/s_stage2-4466ab94.pth')
run('checkpoint_hash', 'sha256sum ' + BASE + '/weights/s_stage2-4466ab94.pth')
