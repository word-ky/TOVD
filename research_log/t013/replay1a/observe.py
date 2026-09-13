from pathlib import Path
from datetime import datetime
import json,subprocess
out=Path('/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay')
pid=int((out/'pid.txt').read_text())
probe=subprocess.run(['tmux','has-session','-t','t013-close1-primary-replay'],capture_output=True,text=True)
ps=subprocess.run(['ps','-p',str(pid),'-o','pid=,ppid=,stat=,args='],capture_output=True,text=True)
exitpath=out/'exit_code.txt'
finished=out/'finished.txt'
print(json.dumps({'timestamp':datetime.now().astimezone().isoformat(timespec='seconds'),'pid':pid,'tmux_rc':probe.returncode,'tmux_stderr':probe.stderr,'ps_rc':ps.returncode,'process':ps.stdout.strip(),'exit_exists':exitpath.exists(),'exit_code':int(exitpath.read_text()) if exitpath.exists() else None,'finish_exists':finished.exists(),'finished':finished.read_text().strip() if finished.exists() else None,'top_level':{name:{'exists':(out/name).exists(),'bytes':(out/name).stat().st_size if (out/name).exists() else None} for name in ['stdout.txt','stderr.txt','results.json','paired_image_draws.npy','bootstrap_samples.npz','diagnostics_per_image.npz']}},indent=2))
