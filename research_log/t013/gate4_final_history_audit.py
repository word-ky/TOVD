"""T013-G4B1: fixed Git history inventory; no scientific execution or result decoding."""
from collections import Counter
from datetime import datetime, timezone
import fnmatch
import json
from pathlib import Path
from gate4_preoutcome_history_audit import git, lines, blob, sha, ancestor, FREEZE, DISPATCH, RUN, RELEASE, MIRROR, PREFIX, ROOT

BASE = 'cca9af23452870d1a12ba1ab6a78ebe683e49cd1'
END = '745efb43d8640f8ac3958bb733d0df44c51c87ff'
START = '08785e443282b060cae1943fc7a1fbac4c770e80'
LEAD = '745f1d24784376afc128156829bcd65b15ff1661'
DISCLOSURE = 'cfe24727a4c2205a966c2f31c8b54e5b74da80b6'
DELIVERY = '0a6b5158265b918f8e5d3ca1eaba1968e5abe075'

# Exhaustive, task-specific path rules. Each commit retains all-parent diffs.
RULES = {
 'coordination': ['coordination/*.md'],
 'project operational handoff': ['research_log/REMOTE.md','research_log/project_state.md','research_log/session_log.md'],
 'G4A1 accepted history audit': [PREFIX+'gate4_preoutcome*',PREFIX+'GATE4_PREOUTCOME_HISTORY_AUDIT.md'],
 'CLOSE1 metadata barrier and smoke fixtures': [PREFIX+'finalization_barrier*',PREFIX+'test_finalization_barrier.py',PREFIX+'FINALIZATION_BARRIER.md',PREFIX+'close1/*'],
 'OPS metadata observations, storage accounting and tests': [PREFIX+'ops*',PREFIX+'OPS*',PREFIX+'primary_*',PREFIX+'PRIMARY_*',PREFIX+'test_primary_*',PREFIX+'collect_primary_incident_metadata.py'],
 'CF1 completed smoke selection': [PREFIX+'canonical_topk*',PREFIX+'test_canonical_topk*',PREFIX+'validate_canonical_topk_smoke.py',PREFIX+'CANONICAL_TOPK*'],
 'CF2 completed smoke arithmetic and replay': [PREFIX+'canonical_counterfactual*',PREFIX+'CANONICAL_COUNTERFACTUAL*',PREFIX+'test_canonical_counterfactual*',PREFIX+'rehearse_canonical_counterfactual.py',PREFIX+'cf2/*',PREFIX+'cf2_remote_repro1_receipt.json'],
 'MECH1 static source provenance': [PREFIX+'mech1/*',PREFIX+'mechanism_identifiability_receipt.json',PREFIX+'MECHANISM_IDENTIFIABILITY_AUDIT.md'],
 'MECH2 synthetic tensor preparation': [PREFIX+'mech2/*',PREFIX+'proposal_selection_lock_receipt.json',PREFIX+'PROPOSAL_SELECTION_LOCK*'],
 'CLOSE2/CLOSE3 terminal metadata': [PREFIX+'close2*',PREFIX+'close3*',PREFIX+'CLOSE2*',PREFIX+'CLOSE3*'],
 'FIN1P single primary opaque integrity check': [PREFIX+'fin1p*',PREFIX+'FIN1P*'],
 'REPLAY1A/B one primary replay and observations': [PREFIX+'replay1a/*',PREFIX+'replay1b/*',PREFIX+'REPLAY1A*',PREFIX+'REPLAY1B*'],
 'REPLAY1C single decoded comparison and authorization': [PREFIX+'replay1c/*',PREFIX+'REPLAY1C*'],
 'DEC1A authorized disclosure': [PREFIX+'dec1a/*',PREFIX+'DEC1A_PRIMARY_SCIENTIFIC_DISCLOSURE.md'],
}

def category(path):
    found = [name for name, patterns in RULES.items() if any(fnmatch.fnmatchcase(path,p) for p in patterns)]
    return found[0] if len(found)==1 else 'UNCLASSIFIED'

def j(path, rev=END):
    return json.loads(blob(rev, PREFIX+path))

def audit():
    checks = {}
    old = j('gate4_preoutcome_history_receipt.json')
    protected=[]
    for row in old['protected_paths']:
        path=row['path']; a=blob(FREEZE,path); b=blob(END,path)
        protected.append({'path':path,'expected_sha256':row['expected_sha256'],
                          'freeze_sha256':sha(a),'endpoint_sha256':sha(b),
                          'equal':a==b and sha(a)==row['expected_sha256']})
    edits=lines('log','--full-history','-m','--format=%H','--name-only',FREEZE+'..'+END,'--',*[r['path'] for r in protected])
    checks['17_protected_paths_identical_without_intermediate_edits']=len(protected)==17 and all(r['equal'] for r in protected) and not edits
    commits=lines('rev-list','--reverse','--topo-order',BASE+'..'+END)
    history=[]; changed=set()
    for c in commits:
        parents=lines('show','-s','--format=%P',c)[0].split()
        deltas={p:lines('diff','--name-status','--no-renames',p,c) for p in parents}
        paths=sorted({line.split('\t')[-1] for ds in deltas.values() for line in ds})
        changed.update(paths)
        history.append({'commit':c,'parents':parents,'subject':lines('show','-s','--format=%s',c)[0],
                        'committer_time':lines('show','-s','--format=%cI',c)[0],
                        'changes_by_parent':deltas,'categories':sorted({category(p) for p in paths})})
    classified=[{'path':p,'category':category(p)} for p in sorted(changed)]
    checks['exact_170_commits']=len(commits)==170
    checks['zero_unclassified_paths']=all(r['category']!='UNCLASSIFIED' for r in classified)
    checks['no_new_run_mirror_scripts_tests_or_yolo_changes']=not any(p.startswith(('scripts/','tests/','research_log/remote_runs/','research_log/t013_yoloworld/')) for p in changed)
    chain=[FREEZE,DISPATCH,BASE,'6a96f88','0acbd4f','385bfac','7820349','f985670','8b00e1e','d4c91ab','688f36b','eb90ff9','1ae41f3','60c99b1','94582bd',DISCLOSURE,DELIVERY,END]
    chronology=[{'before':lines('rev-parse',a)[0],'after':lines('rev-parse',b)[0],'ancestor':ancestor(a,b)} for a,b in zip(chain,chain[1:])]
    checks['chronology_ancestry']=all(r['ancestor'] for r in chronology)
    dispatch=[]
    for p in lines('ls-tree','-r','--name-only',END,'research_log/remote_runs'):
        if p.endswith('/meta.json'):
            d=json.loads(blob(END,p)); command=d.get('command','')
            if '-m scripts.t013_native_run ' in command:
                dispatch.append({'path':p,'run_id':d['runId'],'command':command,'smoke_only':'--smoke-only' in command.split('&&')[0].split()})
    primaries=[d for d in dispatch if not d['smoke_only']]
    checks['unique_committed_primary_dispatch']=len(primaries)==1 and primaries[0]['run_id']==RUN
    dispatch_paths=[MIRROR+n for n in ['run.sh','meta.json','artifacts/resolved_release.txt','artifacts/freeze_sha256.txt']]
    checks['dispatch_provenance_unchanged']=all(blob(DISPATCH,p)==blob(END,p) for p in dispatch_paths) and not lines('log','--full-history','-m','--format=%H',DISPATCH+'..'+END,'--',*dispatch_paths)
    cf1=j('canonical_topk_receipt.json'); cf2=j('canonical_counterfactual_receipt.json'); mech1=j('mechanism_identifiability_receipt.json'); mech2=j('proposal_selection_lock_receipt.json')
    checks['cf1_45_completed_smoke_cells']=len(cf1['cells'])==45 and all('/20260912-205428-tovd-native30-pipeline-smoke/artifacts/cache/' in r['path'] for r in cf1['cells'])
    checks['cf2_two_smoke_replays_only']=len(cf2['replays'])==2 and all(r['smoke_raw_cells']==45 and '/shared/t013/cf2/' in r['output'] for r in cf2['replays']) and cf2['scope']['active_primary_cache_accessed'] is False
    checks['mech1_source_only']=all(mech1['scope'][k] is False for k in ['active_primary_cache_accessed','model_imported_or_forward_run','scientific_payloads_opened'])
    checks['mech2_synthetic_only']=mech2['scope']['synthetic_tensors_only'] and all(mech2['scope'][k] is False for k in ['primary_scientific_or_cache_content_opened','detector_import_or_inference','t014_execution'])
    source_bindings=[]
    for receipt in [cf1,cf2]:
        for name,expected in receipt['source_sha256'].items():
            actual=sha(blob(END,PREFIX+name)); source_bindings.append({'path':PREFIX+name,'expected':expected,'actual':actual,'match':actual==expected})
    checks['smoke_driver_sources_match_executed_receipts']=all(r['match'] for r in source_bindings)
    ops8=j('ops8_reclamation_receipt.json')
    deletion='rm -- /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/coco/val2017.parallel.zip /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/coco/annotations_trainval2017.parallel.zip'
    checks['ops8_exact_authorized_archives_only']=ops8['deletion_command']==deletion and ops8['reclaimed_validated_file_bytes']==1068492871 and not ops8['scope']['frozen_scientific_inputs_mutated'] and ancestor('6101219','b738711')
    fin=j('fin1p_execution_receipt.json'); replay=j('replay1a/launch_receipt.json'); done=j('replay1b/execution_receipt.json'); compare=j('replay1c/execution_receipt.json'); dec=j('dec1a/execution_receipt.json')
    checks['fin1_single_exit0_opaque']=fin['execution_count']==1 and fin['exit_code']==0 and not fin['unchanged_result']['analysis_content_opened'] and not fin['unchanged_result']['npz_deserialized']
    checks['replay_single_exact_launch']=not replay['preflight']['scratch_preexists'] and done['original_launch']==replay and done['replay_relaunched'] is False and done['status']=='REPLAY_COMPLETED_EXIT0_AWAIT_COMPARATOR'
    checks['comparator_single_exit0_before_disclosure']=compare['comparator_executions']==1 and compare['exit_code']==0 and compare['barrier']['primary_result_content_access_authorized'] and not compare['scientific_disclosure']
    checks['accepted_fin1_and_comparison_hashes']=(sha(blob(END,PREFIX+'fin1p/primary_completion_receipt.json'))==fin['receipt_sha256']=='ade691d9765ee09b740ba7a7e24262ee55b272d82d5fd79889659fd6d67df63e' and sha(blob(END,PREFIX+'replay1c/comparison_receipt.json'))==compare['receipt_sha256']=='a22ac31a351080b8860838beda92eb318c2a7ddfb422e2a8be29082388110eef')
    disclosure_paths=[PREFIX+'dec1a/canonical_results.json',PREFIX+'dec1a/primary_scientific_disclosure.json',PREFIX+'DEC1A_PRIMARY_SCIENTIFIC_DISCLOSURE.md']
    disclosure_history={p:lines('log','--full-history','-m','--format=%H',BASE+'..'+END,'--',p) for p in disclosure_paths}
    checks['single_authorized_disclosure_unchanged']=all(v==[DISCLOSURE] for v in disclosure_history.values()) and dec['validation']['status']=='PASS' and dec['decision']=='NOT_RUN_AWAITING_RESEARCH_LEAD_JUDGMENT'
    checks['decision_contract_unchanged']=sha(blob(END,PREFIX+'final_decision_contract.py'))=='baf99f38a3130c268385ddc4c986cd72d123bfb55e7fed29a90b88d289570931' and not lines('log','--full-history','-m','--format=%H',BASE+'..'+END,'--',PREFIX+'final_decision_contract.py',PREFIX+'FINAL_DECISION_CONTRACT.md')
    tail={c:lines('diff','--name-only',c+'^',c) for c in ['5cc83e9','a79aca4','745efb4']}
    checks['three_postdelivery_commits_mailbox_only']=all(v==['research_log/session_log.md'] for v in tail.values())
    # Evidence references are metadata/scope, not scientific result values.
    refs=['canonical_topk_receipt.json','canonical_counterfactual_receipt.json','canonical_counterfactual_initial_blocked_receipt.json','mechanism_identifiability_receipt.json','proposal_selection_lock_receipt.json','ops7_preservation_watch_receipt.json','ops8_reclamation_receipt.json','ops10_terminal_watch_receipt.json','close2_terminal_capture_receipt.json','close3_terminal_capture_receipt.json','fin1p_execution_receipt.json','replay1a/launch_receipt.json','replay1b/execution_receipt.json','replay1c/execution_receipt.json','replay1c/replay_envelope_and_barrier.json','dec1a/execution_receipt.json']
    evidence=[{'path':PREFIX+p,'endpoint_sha256':sha(blob(END,PREFIX+p)),'history_commits':lines('log','--full-history','-m','--format=%H',BASE+'..'+END,'--',PREFIX+p)} for p in refs]
    return {'task':'T013-G4B1','recorded_utc':datetime.now(timezone.utc).isoformat(),'task_start_head':START,'lead_instruction_commit':LEAD,'freeze':FREEZE,'dispatch':DISPATCH,'run':RUN,'release':RELEASE,'audit_base':BASE,'audit_endpoint':END,'status':'MECHANICAL_CHECKS_PASS_PENDING_CONTEXT_REVIEW' if all(checks.values()) else 'FINAL_GATE4_HISTORY_BLOCKER_RETURN_TO_LEAD','checks':checks,'protected_paths':protected,'protected_intermediate_edits':edits,'commit_count':len(commits),'merge_commits':[r['commit'] for r in history if len(r['parents'])>1],'history':history,'changed_path_count':len(classified),'classified_paths':classified,'classification_rules':RULES,'category_counts':dict(Counter(r['category'] for r in classified)),'chronology':chronology,'dispatch_inventory':dispatch,'source_bindings':source_bindings,'evidence':evidence,'disclosure_path_history':disclosure_history,'postdelivery_paths':tail,'excluded_after_endpoint':lines('log','--reverse','--format=%H %s',END+'..'+START),'execution_counts_from_committed_evidence':{'primary_inference':len(primaries),'fin1_primary':fin['execution_count'],'full_primary_replay':1,'primary_comparator':compare['comparator_executions'],'canonical_disclosure':1,'yolo_scientific_runtime':0,'t014_or_proposal_lock_primary_runtime':0},'limitation':'Git and accepted self-reported receipts establish committed evidence only; they cannot prove off-repository behavior. Execution counts identify events, not repeated mentions/copies of one event. Qualitative history review is required in companion report.','new_scientific_execution':False,'scientific_results_decoded':False,'decide_called':False}

if __name__=='__main__':
    result=audit()
    result['helper_sha256']=sha(Path(__file__).read_bytes())
    (ROOT/PREFIX/'gate4_final_history_receipt.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['status','checks','commit_count','changed_path_count','category_counts']},indent=2))
