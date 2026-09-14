"""P3R1: raw-byte cache search and at most two fixed official transfers."""
import datetime
import glob
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess

ROOT = Path('/home/wenchang/asdasdsad/wjq/TOVD')
YW = ROOT/'shared/t013_yoloworld'
OUT = ROOT/'research_log/t013_yoloworld/p3r1'
NAME = 's_stage2-4466ab94.pth'
FINAL = YW/'weights'/NAME
PARTIAL = YW/'weights'/(NAME+'.p3r1.partial')
SIZE = 305058902
SHA = '4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458'
URL = 'https://huggingface.co/wondervictor/YOLO-World-V2.1/resolve/c620164ee3979bf49b895c8a8e0f49aeaca89209/'+NAME
def now():
    return datetime.datetime.now().astimezone().isoformat()
def inspect(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    st=path.stat()
    return dict(path=str(path),bytes=st.st_size,sha256=h.hexdigest(),mtime_ns=st.st_mtime_ns)
def match(item):
    return item['bytes']==SIZE and item['sha256']==SHA

receipt=dict(task='T013-YW-P3R1',task_start_head='1fe8a00f7bb6396db5549505efad3003731301c1',
    lead_instruction_commit='bd8d7980b1b7d823ee266d341c1daee637d3c704',started_at=now(),
    asset=dict(repository='wondervictor/YOLO-World-V2.1',revision='c620164ee3979bf49b895c8a8e0f49aeaca89209',filename=NAME,url=URL,expected_bytes=SIZE,expected_sha256=SHA),
    final_path=str(FINAL),final_existed_before=FINAL.exists(),candidates=[],attempts=[],
    commands=[],first_blocker=None,final_verification=None,independent_verification=None,
    prohibited_action_counts={k:0 for k in ['alternate_checkpoint_model','alternate_host_mirror','package_install_build','checkpoint_deserialization','CUDA_ops','model_load','forward','T013_COCO_LVIS_science']})
def save():
    (OUT/'recovery_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
try:
    chosen=None
    if FINAL.exists():
        receipt['final_preflight']=inspect(FINAL)
        if not match(receipt['final_preflight']):
            raise RuntimeError('Pre-existing final checkpoint has wrong size/hash')
        chosen=FINAL
    roots=[YW]+[Path(p) for p in sorted(glob.glob('/home/*/.cache/huggingface/hub/')) if os.access(p,os.R_OK|os.X_OK)]
    receipt['search_roots']=[str(p) for p in roots]
    receipt['search_command']='Python os.walk listed roots, followlinks=False; files selected by basename == s_stage2-4466ab94.pth OR stat().st_size == 305058902; raw hashlib.sha256 for every selected file'
    def walk_error(error):
        raise error
    for root in roots:
        for base,dirs,files in os.walk(root,onerror=walk_error,followlinks=False):
            for name in files:
                path=Path(base)/name
                if name==NAME or path.stat().st_size==SIZE:
                    item=inspect(path)
                    receipt['candidates'].append(item)
                    if chosen is None and match(item):
                        chosen=path
    receipt['candidate_count']=len(receipt['candidates'])
    save()
    if chosen is not None:
        receipt['source_cache']=inspect(chosen)
        if chosen!=FINAL:
            receipt['commands'].append(f'shutil.copyfile({str(chosen)!r}, {str(PARTIAL)!r})')
            shutil.copyfile(chosen,PARTIAL)
            receipt['copied_temp_verification']=inspect(PARTIAL)
            if not match(receipt['copied_temp_verification']):
                raise RuntimeError('Copied temporary cache file size/hash mismatch')
            os.replace(PARTIAL,FINAL)
            receipt['commands'].append(f'os.replace({str(PARTIAL)!r}, {str(FINAL)!r})')
    else:
        if PARTIAL.exists():
            raise RuntimeError('Unexpected pre-existing P3R1 partial file')
        for attempt in (1,2):
            record=dict(attempt=attempt,started_at=now(),resumed=attempt==2 and PARTIAL.exists() and PARTIAL.stat().st_size>0)
            try:
                record['dns_addresses']=sorted({a[4][0] for a in socket.getaddrinfo('huggingface.co',443)})
            except OSError as e:
                record['dns_error']=str(e)
            command=['curl','-fL','--silent','--show-error','--connect-timeout','45','--max-time','900',
                     '--output',str(PARTIAL),'--write-out','%{json}']
            if record['resumed']:
                command+=['--continue-at','-']
            command+=[URL]
            record['command']=command
            before=PARTIAL.stat().st_size if PARTIAL.exists() else 0
            result=subprocess.run(command,capture_output=True,text=True)
            record.update(stopped_at=now(),exit_code=result.returncode,stderr=result.stderr,
                partial_bytes=PARTIAL.stat().st_size if PARTIAL.exists() else 0)
            record['bytes_added']=record['partial_bytes']-before
            # Only transport fields; do not persist signed redirect URLs or headers.
            transport=json.loads(result.stdout) if result.stdout.strip() else {}
            record['transport']={k:transport.get(k) for k in ['http_code','remote_ip','remote_port','num_redirects','time_namelookup','time_connect','time_appconnect','time_total','size_download','speed_download','ssl_verify_result','errormsg']}
            receipt['attempts'].append(record)
            if result.returncode and receipt['first_blocker'] is None:
                receipt['first_blocker']=dict(attempt=attempt,exit_code=result.returncode,message=result.stderr.strip())
            save()
            print(json.dumps(record),flush=True)
            if result.returncode==0:
                receipt['download_temp_verification']=inspect(PARTIAL)
                if not match(receipt['download_temp_verification']):
                    raise RuntimeError('Completed official transfer has wrong size/hash')
                os.replace(PARTIAL,FINAL)
                receipt['commands'].append(f'os.replace({str(PARTIAL)!r}, {str(FINAL)!r})')
                break
        if not FINAL.exists():
            raise RuntimeError('Two authorized official-source attempts exhausted without a verified checkpoint')
    receipt['final_verification']=inspect(FINAL)
    second=subprocess.run(['sha256sum',str(FINAL)],capture_output=True,text=True,check=True)
    receipt['independent_verification']=dict(command=second.args,exit_code=second.returncode,bytes=FINAL.stat().st_size,sha256=second.stdout.split()[0])
    if not match(receipt['final_verification']) or not match(receipt['independent_verification']):
        raise RuntimeError('Final independent verification mismatch')
    receipt['state']='YW_P3R1_EXACT_CHECKPOINT_READY_FOR_LEAD'
    receipt['next_action']='Research Lead review of exact-checkpoint recovery before any runtime-feasibility resumption'
except Exception as exc:
    receipt['state']='YW_P3R1_CHECKPOINT_TRANSPORT_BLOCKED_RETURN_TO_LEAD'
    receipt['stop_reason']=str(exc)
    if receipt['first_blocker'] is None:
        receipt['first_blocker']=dict(type=type(exc).__name__,message=str(exc))
    receipt['next_action']='Research Lead checkpoint-transport blocker review'
receipt['stopped_at']=now()
receipt['final_exists_after']=FINAL.exists()
save()
print(receipt['state'],flush=True)
raise SystemExit(0 if receipt['state']=='YW_P3R1_EXACT_CHECKPOINT_READY_FOR_LEAD' else 1)
