import hashlib,json
from pathlib import Path
root=Path.cwd()
source_commit='1d9915b06befaf509b912e3328491e3a8b263522'
states=[r for r in json.loads((root/'research_log/t008/sources.json').read_text()) if r['primary_unique']]
manifest=[]
for s in states:
    for regime in ('easy','hard'):
        p=root/'research_log/remote_runs/20260912-101332-tovd-t008-a6000/artifacts/t008/records'/f"{s['state_id']}_{regime}.json"
        data=json.loads(p.read_text())
        counts=[len(r['outputs']['W0_probabilities']) for r in data]
        manifest.append({'state_id':s['state_id'],'seed':s['seed'],'branch':s['branch'],'step':s['step'],'regime':regime,'path':p.relative_to(root).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'episodes':len(data),'queries':sum(counts),'queries_per_episode':sorted(set(counts)),'output_keys':list(data[0]['outputs'])})
receipt={'source_commit':source_commit,'states':len(states),'episodes':sum(r['episodes'] for r in manifest),'queries':sum(r['queries'] for r in manifest),'records':manifest}
(root/'research_log/t009/sources.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print({k:v for k,v in receipt.items() if k!='records'})
print('output_keys',manifest[0]['output_keys'])
