import hashlib,json,subprocess,sys
from pathlib import Path
from datetime import datetime
root=Path('/home/wenchang/asdasdsad/wjq/TOVD')
release=root/'releases/20260912-210306-tovd-native30-primary-freeze'
cache=root/'runs/20260912-210355-tovd-native30-primary/artifacts/cache'
out=root/'shared/t013/close1-primary-replay'
python=root/'shared/t013/venv/bin/python'
session='t013-close1-primary-replay'
checks={}
for name,path,expected in [
 ('analysis',release/'scripts/t013_analysis.py','74cc73e71385e5d38e3fbe68ff03a0f11da30e67ff39b436da90422f72e99f9c'),
 ('fin1_receipt',root/'shared/t013/fin1/primary_completion_receipt.json','ade691d9765ee09b740ba7a7e24262ee55b272d82d5fd79889659fd6d67df63e')]:
 actual=hashlib.sha256(path.read_bytes()).hexdigest()
 checks[name]={'path':str(path),'expected':expected,'actual':actual}
 if actual!=expected:
  print(json.dumps({'status':'REPLAY_EXECUTION_FAILURE_RETURN_TO_LEAD','checks':checks}));sys.exit(1)
receipt=json.loads((root/'shared/t013/fin1/primary_completion_receipt.json').read_text())
assert receipt['run_id']=='20260912-210355-tovd-native30-primary'
assert receipt['release_id']==release.name
assert receipt['scientific_freeze_commit']=='6fec32243985ccc808123d851abf5f3dea10af99'
probe=subprocess.run(['tmux','has-session','-t',session],capture_output=True,text=True)
preflight={'checks':checks,'scratch_preexists':out.exists(),'tmux_rc':probe.returncode,'tmux_stderr':probe.stderr,'interpreter':sys.version,'cache':str(cache),'freeze':receipt['scientific_freeze_commit']}
if out.exists() or probe.returncode==0:
 print(json.dumps({'status':'REPLAY_SCRATCH_OR_SESSION_PREEXISTS_RETURN_TO_LEAD','preflight':preflight}));sys.exit(1)
command=f'{python} -m scripts.t013_analysis --annotations {root}/shared/t013/coco/annotations/instances_val2017.json --run {cache} --output {out}'
out.mkdir()
started=datetime.now().astimezone().isoformat(timespec='seconds')
(out/'started.txt').write_text(started+'\n')
wrapper=f"cd {release} || exit 1\n{command} > {out}/stdout.txt 2> {out}/stderr.txt &\nreplay_pid=$!\nprintf '%s\\n' \"$replay_pid\" > {out}/pid.txt\nwait \"$replay_pid\"\nreplay_exit=$?\nprintf '%s\\n' \"$replay_exit\" > {out}/exit_code.txt\ndate -Iseconds > {out}/finished.txt\n"
(out/'run.sh').write_text(wrapper)
launch=['tmux','new-session','-d','-s',session,'bash '+str(out/'run.sh')]
provenance={'status':'LAUNCH_REQUESTED','preflight':preflight,'started':started,'cwd':str(release),'command':command,'launch_command':launch,'session':session,'output':str(out),'transport_retries':0}
(out/'launch_provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
subprocess.run(launch,check=True)
print(json.dumps(provenance,indent=2))
