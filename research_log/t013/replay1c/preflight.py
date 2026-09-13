from pathlib import Path
import json,hashlib,sys
root=Path('/home/wenchang/asdasdsad/wjq/TOVD')
left=root/'runs/20260912-210355-tovd-native30-primary/artifacts/analysis'
right=root/'shared/t013/close1-primary-replay'
checks={}
for name,path,expected in [
('comparator',root/'research_log/t013/analysis_replay_compare.py','6270a32096c536deac8ec878d3cfbfeb1cc067d428781ab7beb09e78cb8acb76'),
('fin1',root/'shared/t013/fin1/primary_completion_receipt.json','ade691d9765ee09b740ba7a7e24262ee55b272d82d5fd79889659fd6d67df63e'),
('run_receipt',left.parent/'cache/run_receipt.json','75518df05b4a4c15a4c20d32a7764073d21c57c9e8b9880b4d737259c1b35366'),
('manifest',left.parent/'cache/cache_manifest.jsonl','88a31a45712f814d940ef894d0213108f9dca63c845abca01f7133ba44162adc')]:
 actual=hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
 checks[name]={'path':str(path),'expected':expected,'actual':actual,'match':actual==expected}
r={'checks':checks,'left':str(left),'right':str(right),'left_exists':left.is_dir(),'right_exists':right.is_dir(),'comparison_preexists':(right/'comparison_receipt.json').exists(),'interpreter':sys.version}
r['status']='PASS' if all(x['match'] for x in checks.values()) and r['left_exists'] and r['right_exists'] and not r['comparison_preexists'] else 'REPLAY_COMPARATOR_BINDING_FAILURE_RETURN_TO_LEAD'
print(json.dumps(r,indent=2))
