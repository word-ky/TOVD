"""Use existing Git credential-manager authentication without printing it."""
import json
import os
from pathlib import Path
import subprocess
import sys
import urllib.error
import urllib.request

method,endpoint,output=sys.argv[1:4]
env=dict(os.environ,GIT_TERMINAL_PROMPT='0',GCM_INTERACTIVE='Never')
c=subprocess.run(['git','credential','fill'],input='protocol=https\nhost=github.com\n\n',capture_output=True,text=True,env=env)
if c.returncode:
    print('Existing noninteractive Git credential lookup failed'); raise SystemExit(1)
fields=dict(line.split('=',1) for line in c.stdout.splitlines() if '=' in line)
token=fields.get('password')
if not token: print('No existing password/token returned'); raise SystemExit(1)
body=json.dumps(json.loads(sys.argv[4])).encode() if len(sys.argv)>4 else None
req=urllib.request.Request('https://api.github.com/repos/word-ky/TOVD/'+endpoint,data=body,method=method,headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28','User-Agent':'TOVD-P3R4','Content-Type':'application/json'})
try:
    with urllib.request.urlopen(req,timeout=45) as r:
        raw=r.read(); status=r.status
except urllib.error.HTTPError as e:
    raw=e.read(); status=e.code
Path(output).write_bytes(raw or b'{}')
print('GitHub API '+method+' '+endpoint+' status='+str(status))
raise SystemExit(0 if 200<=status<300 else 1)
