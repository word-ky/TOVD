"""Execute the authorized actual-primary DEC1 call once from accepted disclosure."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
P = 'research_log/t013/'
START = '94833fffd735060d077eafaf66d23156e77e3918'
LEAD = 'ca74fa34a9e94d96f30eb4883ed88572ff1b1cf5'
DISCLOSURE = 'cfe24727a4c2205a966c2f31c8b54e5b74da80b6'
AUDIT = 'd469eb34fcb29e0b3f899053e5415b0581ebcd76'
EXPECTED = 'GROUNDING_PRIMARY_NOT_SUPPORTED'
NEXT = 'Research Lead review of sealed Grounding negative and decision whether to preregister a separate YOLO-World architecture-specific replication'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def git_blob(rev, path):
    return subprocess.check_output(['git', 'show', rev+':'+path], cwd=ROOT)

def write_new(name, value):
    with (OUT/name).open('x', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(value, indent=2, allow_nan=True)+'\n')

def main():
    execution = {'task':'T013-DEC1B','task_start_head':START,'lead_instruction_commit':LEAD,
                 'started_utc':datetime.now(timezone.utc).isoformat(),
                 'command':'D:/anaconda3/python.exe research_log/t013/dec1b/seal_decision.py',
                 'interpreter':sys.executable,'python':sys.version,
                 'driver_sha256':sha(Path(__file__).read_bytes()),
                 'actual_primary_decision_call_count':0,'input_bindings':{},'failures':[],
                 'scientific_metrics_recomputed':False,'primary_prediction_cache_opened':False,
                 'new_scientific_runtime_counts':dict.fromkeys(['detector','CF','MECH','T014','YOLO-World','FIN1','replay','comparator'],0)}
    try:
        # Append-only packet and marker prevent a second actual decision call.
        assert not any((OUT/n).exists() for n in ['decision_input.json','call_started.json','decision_receipt.json','execution_receipt.json']), 'decision packet already exists; do not rerun'
        specs = [
            ('contract_source',P+'final_decision_contract.py','51881e3','baf99f38a3130c268385ddc4c986cd72d123bfb55e7fed29a90b88d289570931'),
            ('contract_document',P+'FINAL_DECISION_CONTRACT.md','51881e3','9c6e6ee662b5e22458b13adecc9825d32e1e031876c39904b3635ce1388cbcba'),
            ('contract_receipt',P+'final_decision_contract_receipt.json','51881e3',None),
            ('disclosure',P+'dec1a/primary_scientific_disclosure.json',DISCLOSURE,'c3a76e32982d3581b7a0eb56b823ccfab56bbd99700f53a56976444f314879ff'),
            ('fin1',P+'fin1p/primary_completion_receipt.json','8b00e1e','ade691d9765ee09b740ba7a7e24262ee55b272d82d5fd79889659fd6d67df63e'),
            ('comparison',P+'replay1c/comparison_receipt.json','60c99b1','a22ac31a351080b8860838beda92eb318c2a7ddfb422e2a8be29082388110eef'),
            ('replay_envelope',P+'replay1c/replay_envelope_and_barrier.json','60c99b1','b6c4f96f44d92d007a0cd964da012452c16f71a79d8b95f261365bf7812a1bdf'),
            ('gate4_report',P+'GATE4_FINAL_HISTORY_AUDIT.md',AUDIT,'476f86ad17d50e286f448abdf0ed1d84cc13566e812b153341efa96bfd4c1123'),
        ]
        raw={}
        for name,path,rev,expected in specs:
            raw[name]=(ROOT/path).read_bytes(); accepted=git_blob(rev,path); current=git_blob(START,path)
            row={'path':path,'accepted_commit':rev,'local_raw_sha256':sha(raw[name]),'accepted_git_blob_sha256':sha(accepted),
                 'task_start_git_blob_sha256':sha(current),'git_bytes_unchanged':accepted==current,
                 'local_matches_accepted_except_CRLF':raw[name].replace(b'\r\n',b'\n')==accepted.replace(b'\r\n',b'\n')}
            execution['input_bindings'][name]=row
            assert row['git_bytes_unchanged'] and row['local_matches_accepted_except_CRLF'], name+' changed'
            if expected is not None:
                assert row['local_raw_sha256']==expected, name+' accepted raw digest mismatch'
        contract_receipt=json.loads(raw['contract_receipt'])
        assert contract_receipt['status']=='PASS' and contract_receipt['contract_version']=='T013-DEC1-v1'
        for filename,name in [('final_decision_contract.py','contract_source'),('FINAL_DECISION_CONTRACT.md','contract_document')]:
            assert contract_receipt['artifact_sha256'][filename]==sha(raw[name])
        disclosure=json.loads(raw['disclosure']); fin=json.loads(raw['fin1']); comparison=json.loads(raw['comparison']); replay=json.loads(raw['replay_envelope'])
        assert fin['status']=='PASS' and fin['mode']=='primary' and comparison['status']=='PASS'
        assert fin['run_id']==disclosure['provenance']['run_id']==replay['binding']['run_id']=='20260912-210355-tovd-native30-primary'
        assert fin['release_id']==disclosure['provenance']['release_id']==replay['binding']['release_id']=='20260912-210306-tovd-native30-primary-freeze'
        assert fin['scientific_freeze_commit']==disclosure['provenance']['freeze_commit']==replay['binding']['freeze_commit']=='6fec32243985ccc808123d851abf5f3dea10af99'
        for field,name in [('fin1','fin1'),('full_cache_replay','comparison')]:
            assert disclosure['evidence'][field]['status']=='PASS'
            assert disclosure['evidence'][field]['receipt_sha256']==sha(raw[name])
        assert disclosure['evidence']['full_cache_replay']['envelope_sha256']==sha(raw['replay_envelope'])
        assert replay['replay']['fin1_receipt_sha256']==sha(raw['fin1'])
        assert disclosure['provenance']['run_receipt_sha256']==fin['run_receipt_sha256']
        assert disclosure['provenance']['cache_manifest_sha256']==fin['manifest_sha256']
        review={'gate3_coherent':False,'gate4':True,
                'gate3_rationale':'complete three-family Gate3 evidence is not qualitatively coherent because only distractor-FP excess is statistically supported, classification-beyond-localization is unsupported, and matched-localization margin shrinkage is negative in all four corruptions; this cannot alter Gate1',
                'gate4_history_audit_ref':'research_log/t013/GATE4_FINAL_HISTORY_AUDIT.md / evidence commit '+AUDIT,
                'review_ref':'coordination/CHATGPT_REVIEW_LOG.md#T013-G4B1-review--T013-DEC1B-assignment'}
        envelope={k:disclosure[k] for k in ['contract_version','evidence','provenance','results']}
        envelope['lead_review']=review
        # Only the already reviewed Lead fields are added. All scientific fields
        # remain the exact decoded disclosure, with no arithmetic or selection.
        write_new('decision_input.json',envelope)
        input_hash=sha((OUT/'decision_input.json').read_bytes())
        execution['input_sha256']=input_hash
        execution['lead_review']=review
        execution['all_input_bindings_validated']=True
        namespace={}
        exec(compile(raw['contract_source'],P+'final_decision_contract.py','exec'),namespace)
        write_new('call_started.json',{'input_sha256':input_hash,'function_source_sha256':sha(raw['contract_source']),'started_utc':datetime.now(timezone.utc).isoformat(),'instruction':'Never call decide again for this packet, including on failure.'})
        execution['actual_primary_decision_call_count']=1
        state=namespace['decide'](envelope)
        decision={'task':'T013-DEC1B','contract_version':envelope['contract_version'],'state':state,
                  'expected_state':EXPECTED,'matches_expected_state':state==EXPECTED,'actual_primary_decision_call_count':1,
                  'input_sha256':input_hash,'contract_source_sha256':sha(raw['contract_source']),
                  'gate1':envelope['results']['assessment']['gate1'],'gate2':envelope['results']['assessment']['gate2'],
                  'gate4_recorded_checks':envelope['results']['assessment']['gate4_recorded_checks'],'lead_review':review}
        write_new('decision_receipt.json',decision)
        execution['returned_state']=state
        assert state==EXPECTED, 'unexpected decision state: '+state
        execution['status']='DEC1B_GROUNDING_PRIMARY_NOT_SUPPORTED_FINAL'
        execution['recommended_next_action']=NEXT
        report='''# T013-DEC1B — Final Grounding primary decision

**GROUNDING_PRIMARY_NOT_SUPPORTED**. The frozen T013-DEC1-v1 function was called exactly once on the complete accepted DEC1A disclosure plus Research-Lead judgments and returned the expected state.

FIN1 and full-cache replay/comparison are PASS. Frozen Gate1=false, Gate2=true, recorded Gate4=true; Research Lead supplied gate3_coherent=false and final gate4=true. Under unchanged DEC1 precedence, this is a valid negative Grounding primary. Gate3 cannot rescue Gate1. No thresholds or results were recalculated or changed.

The full scientific envelope is decision_input.json; machine state is decision_receipt.json. execution_receipt.json binds exact source/document/verification receipt, disclosure, FIN1, comparator, replay envelope and Gate4 audit hashes, including both local raw and Git blob hashes where CRLF differs. The accepted Git bytes are unchanged; no source file was normalized or rewritten. The existing disclosure's historical contract_decision=NOT_RUN is not a current decision input: only its required contract_version/evidence/provenance/results sections were copied unchanged, then the explicit Lead review fields were added.

Task-start HEAD: '''+START+'''; Lead instruction: '''+LEAD+'''. Review reference: coordination/CHATGPT_REVIEW_LOG.md#T013-G4B1-review--T013-DEC1B-assignment. Gate4 audit: research_log/t013/GATE4_FINAL_HISTORY_AUDIT.md, evidence '''+AUDIT+'''. Original disclosure evidence: '''+DISCLOSURE+'''.

Command: D:/anaconda3/python.exe research_log/t013/dec1b/seal_decision.py, local Python 3.12.7, standard library only. The frozen function performs schema validation and state selection; no detector or scientific test was rerun. Primary prediction-cache access, scientific metric recomputation and new detector/CF/MECH/T014/YOLO/FIN1/replay/comparator execution counts are all zero.

No discrepancy occurred. The inherited Git-history limitation remains: accepted repository/operational evidence cannot prove absence of unrecorded off-repository behavior. T014 and vocabulary/gate redesign remain prohibited for this primary. YOLO-World may later test architecture specificity; it cannot replace, relabel or rescue this Grounding negative. No YOLO runtime is authorized by this packet.

Stop and await '''+NEXT+'''.
'''
        with (OUT/'FINAL_GROUNDING_DECISION.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
    except Exception as exc:
        execution['status']='DEC1B_BLOCKER_RETURN_TO_LEAD'
        execution['failures'].append({'type':type(exc).__name__,'detail':str(exc)})
        execution['recommended_next_action']='Research Lead blocker review'
    execution['finished_utc']=datetime.now(timezone.utc).isoformat()
    execution['artifact_sha256']={p.name:sha(p.read_bytes()) for p in OUT.iterdir() if p.is_file() and p.name!='execution_receipt.json'}
    write_new('execution_receipt.json',execution)
    print(json.dumps(execution,indent=2))
    return 0 if execution['status']=='DEC1B_GROUNDING_PRIMARY_NOT_SUPPORTED_FINAL' else 1

if __name__=='__main__':
    raise SystemExit(main())
