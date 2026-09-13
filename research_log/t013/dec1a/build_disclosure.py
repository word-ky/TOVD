import json,hashlib,importlib.util,math
from pathlib import Path
base=Path('research_log/t013/dec1a')
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def equal(a,b):
 if type(a)!=type(b):return False
 if isinstance(a,dict):return list(a)==list(b) and all(equal(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
 if isinstance(a,float) and math.isnan(a):return math.isnan(b)
 return a==b
spec=importlib.util.spec_from_file_location('contract','research_log/t013/final_decision_contract.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
r=read(base/'canonical_results.json');f=read('research_log/t013/native30_freeze.json');e=read('research_log/t013/replay1c/replay_envelope_and_barrier.json');fin=e['fin1']['result'];b=e['binding']
for k,v in [('kind','T013-NATIVE30'),('image_count',1000),('conditions',c.CONDITIONS),('vocabularies',c.VOCABS),('metric_order',c.METRICS),('replicates',1000),('seed',20260913)]:assert r[k]==v,k
c.tensor(r['point_metrics'],[5,3,8],'point_metrics');c.interval(r['metric_ci95'],[5,3,8],'metric_ci95');c.tensor(r['margin_common_localized_gt_counts'],[4],'support')
a=r['assessment']
for k in ['D_AP50','A_AP50']:c.tensor(a[k],[4,3],k);c.interval(a[k+'_ci95'],[4,3],k)
c.tensor(a['hard_minus_random'],[4],'contrast');c.interval(a['hard_minus_random_ci95'],[4],'contrast_ci')
for k in ['mean_A_hard','mean_hard_minus_random']:c.tensor(a[k],[],k);c.interval(a[k+'_ci95'],[],k)
for k in ['gate1','gate2','gate3_statistical_support','gate4_recorded_checks']:c.boolean(a[k],k)
assert len(a['gate1_corruptions'])==4
for v in a['gate1_corruptions']:c.boolean(v,'gate1_corruptions')
c.text(a['research_acceptance'],'research_acceptance')
for family in c.FAMILIES:
 d=a['gate3_diagnostics'][family];c.tensor(d['per_corruption'],[4],family);c.tensor(d['mean'],[],family);c.interval(d['mean_ci95'],[],family);assert type(d['positive_corruptions']) is int and 0<=d['positive_corruptions']<=4;c.boolean(d['statistical_support'],family)
ids={line.split()[1]:line.split()[0] for line in (base/'output_identifiers.txt').read_text(encoding='utf-8-sig').splitlines() if line.strip()}
p={'run_id':b['run_id'],'release_id':b['release_id'],'freeze_commit':b['freeze_commit']}
for k in ['environment_sha256','plan_sha256','vocabulary_sha256','selection_sha256','annotations_sha256','image_manifest_sha256','native_source_revision']:p[k]=f[k]
p.update(freeze_sha256=fin['source_hashes']['research_log/t013/native30_freeze.json'],analysis_sha256=f['code_sha256']['scripts/t013_analysis.py'],coco_sha256=f['code_sha256']['scripts/t013_coco.py'],diagnostics_sha256=f['code_sha256']['scripts/t013_diagnostics.py'],checkpoint_sha256=f['native_checkpoint_sha256'],state_before_sha256=f['native_state_sha256'],state_after_sha256=fin['state_sha256'],run_receipt_sha256=fin['run_receipt_sha256'],cache_manifest_sha256=fin['manifest_sha256'],results_sha256=sha(base/'canonical_results.json'),paired_draws_sha256=ids['paired_image_draws.npy'],bootstrap_samples_sha256=ids['bootstrap_samples.npz'],diagnostics_per_image_sha256=ids['diagnostics_per_image.npz'])
assert set(c.PROVENANCE_FIELDS)<=set(p)
summary={'contract_version':c.VERSION,'evidence':{'fin1':{'status':'PASS','receipt_ref':e['fin1']['receipt_ref'],'receipt_sha256':e['fin1']['receipt_sha256']},'full_cache_replay':{'status':'PASS','receipt_ref':e['replay']['receipt_ref'],'receipt_sha256':e['replay']['receipt_sha256'],'envelope_ref':'research_log/t013/replay1c/replay_envelope_and_barrier.json','envelope_sha256':sha('research_log/t013/replay1c/replay_envelope_and_barrier.json')}},'provenance':p,'results':r,'contract_decision':'NOT_RUN_AWAITING_RESEARCH_LEAD_JUDGMENT','canonical_path':b['analysis_reference_dir']+'/results.json','provenance_sources':{'frozen':'research_log/t013/native30_freeze.json','state_after_and_cache':'research_log/t013/fin1p/primary_completion_receipt.json','output_identifiers':'research_log/t013/dec1a/output_identifiers.txt','output_identifier_note':'Three completed-output file SHA256 identifiers assembled with sha256sum; opaque bytes only, no prediction reads, no repeat integrity audit or comparisons.'}}
machine=base/'primary_scientific_disclosure.json';machine.write_text(json.dumps(summary,indent=2,allow_nan=True)+'\n',encoding='utf-8')
assert equal(read(machine)['results'],r)
lines=['# T013-DEC1A — Complete frozen primary disclosure','', 'Status: DEC1A_COMPLETE_DISCLOSURE_READY_FOR_RESEARCH_LEAD. Disclosure only; Lead Gate3 coherence, final Gate4, final Grounding decision and next experiment are not assigned.','', 'final_decision_contract.decide = NOT_RUN_AWAITING_RESEARCH_LEAD_JUDGMENT','', 'All numbers below are copied directly at full round-trip precision. null = unavailable interval; NaN = undefined support. Neither is replaced or omitted. Corruption order and vocabulary order remain frozen. AP/AP50/AR/AR50 use the frozen percentage scale; diagnostic units remain those of the source.','', '## Metadata','', '```json',json.dumps({k:r[k] for k in ['kind','image_count','conditions','vocabularies','metric_order','replicates','seed']},indent=2),'```','', '## Complete detection table','', '| Condition | Vocabulary | AP | AP50 | AR | AR50 |','| --- | --- | --- | --- | --- | --- |']
for i,condition in enumerate(r['conditions']):
 for j,vocab in enumerate(r['vocabularies']):lines.append('| '+' | '.join([condition,vocab]+[str(x) for x in r['point_metrics'][i][j][:4]])+' |')
for k in range(4,8):
 lines+=['','## '+r['metric_order'][k],'','| Condition | V0 | Vhard30 | Vrand30 |','| --- | --- | --- | --- |']
 for i,condition in enumerate(r['conditions']):lines.append('| '+' | '.join([condition]+[str(r['point_metrics'][i][j][k]) for j in range(3)])+' |')
lines+=['','## Complete contrasts, intervals, gates and diagnostic families','', 'Arrays follow gaussian_noise, motion_blur, fog, jpeg_compression; vocabulary columns follow V0, Vhard30, Vrand30. CI axis is lower, upper. Family CIs are frozen mean intervals; no per-corruption family CI is added.','', '```json',json.dumps({'margin_common_localized_gt_counts':r['margin_common_localized_gt_counts'],'assessment':a},indent=2,allow_nan=True),'```','', '## All per-cell frozen confidence intervals','', 'metric_ci95 [lower/upper, condition, vocabulary, metric], with orders above.','', '```json',json.dumps(r['metric_ci95'],indent=2,allow_nan=True),'```','', '## Provenance and accepted evidence','', '```json',json.dumps({k:summary[k] for k in ['contract_version','canonical_path','evidence','provenance','provenance_sources','contract_decision']},indent=2),'```','', '## Unfiltered canonical scientific payload','', '```json',json.dumps(r,indent=2,allow_nan=True),'```','', 'No new statistic, bootstrap, CI, threshold or gate was computed. No result was repaired/omitted. No decide call, Lead judgment, CF/MECH/T014/YOLO, detector, replay or comparator action occurred.']
human=Path('research_log/t013/DEC1A_PRIMARY_SCIENTIFIC_DISCLOSURE.md');human.write_text('\n'.join(lines)+'\n',encoding='utf-8')
# Verify the complete embedded payload and every generated table cell, without scientific computation.
h=human.read_text(encoding='utf-8');payload=h.split('## Unfiltered canonical scientific payload\n\n```json\n')[1].split('\n```')[0];assert equal(json.loads(payload),r)
for i in range(5):
 for j in range(3):
  for value in r['point_metrics'][i][j]:assert str(value) in h
v={'status':'PASS','canonical_results_sha256':p['results_sha256'],'machine_sha256':sha(machine),'human_sha256':sha(human),'checks':['mandatory metadata order','point [5,3,8] and CI [2,5,3,8]','all contrast/gate/family fields','all20 provenance identifiers','machine results field/order/type equality with canonical','human complete payload equality and all120 table values'],'decide':'NOT_RUN_AWAITING_RESEARCH_LEAD_JUDGMENT','new_scientific_statistics':False}
(base/'validation.json').write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8');print(json.dumps(v,indent=2))
