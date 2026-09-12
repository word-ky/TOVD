from pathlib import Path
import json,hashlib,re
root=Path.cwd(); out=root/'research_log/t010'
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
states=[s for s in json.loads((root/'research_log/t008/sources.json').read_text()) if s['branch']=='original_P' or s['step']==400]
for s in states: assert digest(root/s['path'])==s['sha256']
config=json.loads((root/'research_log/t008/config.json').read_text())
config={k:config[k] for k in ('world','model','seeds')}
config.update(calibration_episodes=100,validation_episodes=200,calibration_namespace=1000000000,validation_namespace=2000000000,seed_stride=100000,hard_offset=10000,quantile_grid=[i/100 for i in range(101)],calibration_tie_tolerance=1e-12)
(out/'config.json').write_text(json.dumps(config,indent=2)+'\n')
old=set(); scanned=[]
for p in sorted((root/'research_log/remote_runs').rglob('*.json')):
 b=p.read_bytes(); ids=set(map(int,re.findall(rb'"episode_seed"\s*:\s*(\d+)',b)))
 if ids:
  old.update(ids); scanned.append({'path':p.relative_to(root).as_posix(),'sha256':hashlib.sha256(b).hexdigest(),'id_count':len(ids)})
new={phase:[base+s*100000+h+i for s in config['seeds'] for h in (0,10000) for i in range(count)] for phase,base,count in [('calibration',1000000000,100),('validation',2000000000,200)]}
assert not(set(new['calibration'])&set(new['validation']))
assert not(old&set(new['calibration'])) and not(old&set(new['validation']))
sources={'research_commit':'45f6045','checkpoint_source_commit':'376d205347d0a4afff7a5aee3a094e8bc2a84efa','states':states,'code_hashes':[{'path':p.relative_to(root).as_posix(),'sha256':digest(p)} for p in sorted((root/'tovd').rglob('*.py'))],'historical_id_files':scanned,'historical_ids':sorted(old),'fresh_episode_ids':new,'nonoverlap':True}
(out/'sources.json').write_text(json.dumps(sources,indent=2)+'\n',encoding='utf-8')
print({'states':len(states),'historical_ids':len(old),'historical_max':max(old),'calibration_ids':len(new['calibration']),'validation_ids':len(new['validation']),'nonoverlap':True})
