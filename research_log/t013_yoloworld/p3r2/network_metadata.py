"""Authorized P3R2 A/B metadata probes, no checkpoint request."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess

OUT=Path(__file__).resolve().parent
def now(): return datetime.datetime.now().astimezone().isoformat()
def run(args):
    start=now()
    r=subprocess.run(args,capture_output=True,text=True)
    return dict(command=args,started_at=start,stopped_at=now(),exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr)
receipt=dict(task='T013-YW-P3R2',task_start_head='144e6f45c766a5783838d282e21193ca34c23065',lead_instruction_commit='767d41e326439ee5c4b668af8e792cc45d768bdb',started_at=now())
raw=Path('/etc/resolv.conf').read_bytes()
receipt['resolv_conf']=dict(content=raw.decode(),sha256=hashlib.sha256(raw).hexdigest())
receipt['system_dns']=run(['getent','ahosts','huggingface.co'])
receipt['proxy_status']={k:('set' if k in os.environ else 'unset') for k in ['HTTP_PROXY','HTTPS_PROXY','ALL_PROXY','http_proxy','https_proxy','all_proxy','NO_PROXY','no_proxy']}
receipt['curl_version']=run(['curl','--version'])
help_result=run(['curl','--help','all'])
receipt['curl_help_capabilities']=dict(command=help_result['command'],exit_code=help_result['exit_code'],lines=[s for s in help_result['stdout'].splitlines() if any(k in s for k in ['--doh','--resolve','--http2'])])
receipt['controls']=[]
receipt['doh']=[]
receipt['same_origin_probes']=[]
def save(): (OUT/'network_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
save()
for url in ['https://github.com/','https://pypi.org/']:
    result=run(['curl','--silent','--show-error','--head','--connect-timeout','15','--max-time','30','--output','/dev/null','--write-out','%{json}',url])
    data=json.loads(result.pop('stdout'))
    result['transport']={k:data.get(k) for k in ['http_code','remote_ip','ssl_verify_result','time_namelookup','time_connect','time_appconnect','time_total','num_redirects','size_download']}
    receipt['controls'].append(result)
    save()
    print('control '+url+' exit '+str(result['exit_code']),flush=True)
for endpoint in ['https://dns.google/resolve','https://cloudflare-dns.com/dns-query']:
    for kind in ['A','AAAA']:
        result=run(['curl','--silent','--show-error','--connect-timeout','15','--max-time','30','--header','Accept: application/dns-json',endpoint+'?name=huggingface.co&type='+kind])
        body=result.pop('stdout')
        result['endpoint']=endpoint
        result['record_type']=kind
        try: result['dns_response']=json.loads(body)
        except ValueError: result['dns_response']=None; result['non_json_body_bytes']=len(body.encode())
        receipt['doh'].append(result)
        save()
        print('DoH '+endpoint+' '+kind+' exit '+str(result['exit_code']),flush=True)
receipt['ab_stopped_at']=now()
save()
