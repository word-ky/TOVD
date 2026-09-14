"""Eight fixed nonrecursive queries; TCP only if a UDP response is truncated."""
import datetime
import json
from pathlib import Path
import re
import subprocess
import time

OUT=Path(__file__).resolve().parent
def now(): return datetime.datetime.now().astimezone().isoformat()
def run(command):
    start=now(); tick=time.monotonic()
    p=subprocess.run(command,capture_output=True,text=True)
    return dict(command=command,started_at=start,stopped_at=now(),elapsed_seconds=time.monotonic()-tick,exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr)
r=dict(task='T013-YW-P3R3',task_start_head='29482534e26c34f379da0f1cca6578d94d09670f',lead_instruction_commit='2cb45efcdc4797506b734337d7bdfac3557a3544',started_at=now(),queries=[],same_origin_probes=[])
r['system_dns']=run(['getent','ahosts','huggingface.co'])
r['client']=run(['/usr/bin/dig','-v'])
r['client_preexisting']=True
r['client_path']='/usr/bin/dig'
servers=[('205.251.192.137','ns-137.awsdns-17.com'),('205.251.197.172','ns-1452.awsdns-53.org'),('205.251.199.163','ns-1955.awsdns-52.co.uk'),('205.251.195.151','ns-919.awsdns-50.net')]
def save(): (OUT/'dns_receipt.json').write_text(json.dumps(r,indent=2)+'\n')
for ip,name in servers:
    for kind in ['A','AAAA']:
        command=['/usr/bin/dig','@'+ip,'huggingface.co',kind,'+norecurse','+time=5','+tries=1','+ignore']
        for transport in ['UDP','TCP']:
            if transport=='TCP': command=command+['+tcp']
            q=run(command)
            q.update(server_ip=ip,server_name=name,record_type=kind,transport=transport)
            flags=re.search(r';; flags: ([^;]*);',q['stdout'])
            flags=flags.group(1).split() if flags else []
            status=re.search(r'status: (\w+)',q['stdout'])
            q.update(rcode=status.group(1) if status else None,aa='aa' in flags,tc='tc' in flags,answers=[])
            in_answer=False
            for line in q['stdout'].splitlines():
                if line==' ;; ANSWER SECTION:'.strip(): in_answer=True; continue
                if not line.strip() or line.startswith(';;'): in_answer=False; continue
                if in_answer:
                    fields=line.split()
                    if len(fields)>=5: q['answers'].append(dict(name=fields[0],ttl=int(fields[1]),rrclass=fields[2],type=fields[3],data=' '.join(fields[4:])))
            r['queries'].append(q); save()
            print(ip+' '+kind+' '+transport+' exit='+str(q['exit_code'])+' rcode='+str(q['rcode'])+' aa='+str(q['aa']),flush=True)
            if not q['tc']: break
r['dns_stopped_at']=now()
save()
