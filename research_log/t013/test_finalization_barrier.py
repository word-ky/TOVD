"""Synthetic transitions and reuse-only completed45-cell smoke rehearsal."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import unittest

import finalization_barrier as barrier

HERE = Path(__file__).resolve().parent
OUTCOMES = []


def fixtures(binding=None):
    binding = binding or barrier.target('a' * 64, 'b' * 64)
    completed = {'run_id': binding['run_id'], 'writer_alive': False, 'tmux_alive': False,
                 'release_id': binding['release_id'], 'freeze_commit': binding['freeze_commit'],
                 'wrapper_completed': True, 'wrapper_exit_code': 0, 'analysis_result_exists': True}
    fin1 = {'binding': deepcopy(binding), 'tool_sha256': barrier.FIN1_SHA,
            'receipt_ref': 'synthetic/fin1.json', 'receipt_sha256': 'c' * 64,
            'result': {'status': 'PASS', 'mode': binding['scope'],
                       'scientific_freeze_commit': binding['freeze_commit'],
                       'receipt_freeze_argument': binding['receipt_freeze_argument'],
                       'run_id': binding['run_id'], 'release_id': binding['release_id'],
                       'image_count': binding['image_count'], 'expected_records': binding['record_count'],
                       'run_receipt_sha256': binding['cache_receipt_sha256'],
                       'manifest_sha256': binding['manifest_sha256']}}
    replay = {'binding': deepcopy(binding), 'tool_sha256': barrier.COMPARE_SHA,
              'receipt_ref': 'synthetic/replay.json', 'receipt_sha256': 'd' * 64,
              'fin1_receipt_sha256': fin1['receipt_sha256'],
              'left_dir': binding['analysis_reference_dir'],
              'right_dir': barrier.ROOT + '/shared/t013/close1/synthetic_replay',
              'analysis_exit_code': 0, 'comparator_exit_code': 0,
              'analysis_sha256': barrier.ANALYSIS_SHA,
              'replicates': 10 if binding['scope'] == 'engineering_smoke' else 1000,
              'result': {'status': 'PASS', 'artifacts': {name: {'equal': True} for name in barrier.FILES}}}
    return binding, completed, fin1, replay


class BarrierTests(unittest.TestCase):
    def check(self, name, args, expected, primary_access=False):
        result = barrier.evaluate(*args)
        self.assertEqual(result['state'], expected, name)
        self.assertEqual(result['primary_result_content_access_authorized'], primary_access, name)
        self.assertFalse(result['scientific_acceptance'])
        self.assertFalse(result['restart_resume_authorized'])
        self.assertFalse(result['helper_opened_result_content'])
        OUTCOMES.append({'fixture': name, **result})
        return result

    def test_ordered_transitions(self):
        binding, completion, fin1, replay = fixtures()
        for field in ('writer_alive', 'tmux_alive'):
            running = dict(completion, **{field: True})
            self.check(field, [binding, running, fin1, replay], barrier.RUNNING)
        for field, value in [('wrapper_completed', False), ('wrapper_exit_code', None),
                             ('writer_alive', None), ('tmux_alive', None)]:
            self.check('missing_completion:' + field, [binding, dict(completion, **{field: value})], barrier.RUNNING)
        self.check('complete_without_fin1', [binding, completion], barrier.UNVERIFIED)
        self.check('fin1_pass_replay_absent', [binding, completion, fin1], barrier.REPLAY_READY)
        self.check('full_replay_pass', [binding, completion, fin1, replay], barrier.LEAD_READY, True)
        self.check('replay_cannot_skip_fin1', [binding, completion, None, replay], barrier.UNVERIFIED)
        for key in ('run_id', 'release_id', 'freeze_commit'):
            self.check('stale_completion:' + key, [binding, dict(completion, **{key: 'stale'}), fin1, replay], barrier.RUNNING)

    def test_early_analysis_existence_never_unlocks(self):
        binding, completion, fin1, replay = fixtures()
        for exists in (False, True):
            metadata = dict(completion, analysis_result_exists=exists)
            self.check('exists_unverified:' + str(exists), [binding, metadata], barrier.UNVERIFIED)
            metadata['writer_alive'] = True
            self.check('exists_running:' + str(exists), [binding, metadata, fin1, replay], barrier.RUNNING)

    def test_failures_and_pending(self):
        binding, completion, fin1, replay = fixtures()
        self.check('wrapper_failure', [binding, dict(completion, wrapper_exit_code=1), fin1, replay], barrier.FAILED)
        for status in ('FAIL', 'PENDING'):
            bad = deepcopy(fin1)
            bad['result']['status'] = status
            result = self.check('fin1_' + status, [binding, completion, bad, replay], barrier.UNVERIFIED)
            self.assertFalse(result['fin1_execution_authorized'])
            bad = deepcopy(replay)
            bad['result']['status'] = status
            result = self.check('replay_' + status, [binding, completion, fin1, bad], barrier.REPLAY_READY)
            self.assertFalse(result['replay_comparison_execution_authorized'])

    def test_stale_binding_and_tool_hashes(self):
        binding, completion, fin1, replay = fixtures()
        for key in ('run_id', 'release_id', 'freeze_commit', 'cache_path', 'cache_receipt_ref',
                    'cache_receipt_sha256', 'manifest_sha256', 'task_start_head',
                    'fin1_version', 'comparator_version'):
            bad = deepcopy(fin1)
            bad['binding'][key] = 'stale'
            self.check('stale_fin1:' + key, [binding, completion, bad, replay], barrier.UNVERIFIED)
            bad = deepcopy(replay)
            bad['binding'][key] = 'stale'
            self.check('stale_replay:' + key, [binding, completion, fin1, bad], barrier.REPLAY_READY)
        for key, value in [('tool_sha256', '0' * 64), ('receipt_sha256', ''),
                           ('receipt_ref', '')]:
            bad = deepcopy(fin1)
            bad[key] = value
            self.check('bad_fin1:' + key, [binding, completion, bad, replay], barrier.UNVERIFIED)
            bad = deepcopy(replay)
            bad[key] = value
            self.check('bad_replay:' + key, [binding, completion, fin1, bad], barrier.REPLAY_READY)

    def test_replay_must_compare_actual_reference_from_same_fin1(self):
        binding, completion, fin1, replay = fixtures()
        changes = {'left_dir': barrier.ROOT + '/shared/t013/repro1/replay_a',
                   'right_dir': replay['left_dir'], 'fin1_receipt_sha256': 'e' * 64,
                   'analysis_sha256': 'f' * 64, 'replicates': 10,
                   'analysis_exit_code': 1, 'comparator_exit_code': 1}
        for key, value in changes.items():
            bad = deepcopy(replay)
            bad[key] = value
            self.check('wrong_comparison:' + key, [binding, completion, fin1, bad], barrier.REPLAY_READY)
        bad = deepcopy(replay)
        del bad['result']['artifacts']['results.json']
        self.check('incomplete_comparison', [binding, completion, fin1, bad], barrier.REPLAY_READY)

    def test_completed_smoke_receipt_reuse_and_scratch_mutation(self):
        fin_path = HERE / 'primary_completion_smoke_receipt.json'
        rep_path = HERE / 'analysis_replay_receipt.json'
        original = {p.name: p.read_bytes() for p in (fin_path, rep_path)}
        fin_result = json.loads(original[fin_path.name])
        rep = json.loads(original[rep_path.name])
        binding = barrier.target(fin_result['run_receipt_sha256'], fin_result['manifest_sha256'], smoke=True)
        binding, completion, fin1, replay = fixtures(binding)
        smoke_log = HERE.parent / 'remote_runs' / binding['run_id'] / 'train.log'
        self.assertIn('[autodl] exit_code=0', smoke_log.read_text())
        completion['historical_completion_log_ref'] = str(smoke_log)
        completion['reused_historical_metadata_not_live_process_query'] = True
        fin1.update(receipt_ref=str(fin_path), receipt_sha256=hashlib.sha256(original[fin_path.name]).hexdigest(),
                    result=fin_result)
        replay.update(receipt_ref=str(rep_path) + '#/replay_comparison',
                      receipt_sha256=hashlib.sha256(original[rep_path.name]).hexdigest(),
                      fin1_receipt_sha256=fin1['receipt_sha256'],
                      left_dir=rep['runs'][0]['output'], right_dir=rep['runs'][1]['output'],
                      analysis_exit_code=rep['runs'][1]['exit_code'],
                      result=rep['replay_comparison'])
        self.assertEqual(rep['freeze_commit'], barrier.FREEZE)
        self.assertTrue(all(v['equal'] for v in rep['bindings'].values()))
        self.assertEqual(rep['bindings'][binding['cache_receipt_ref']]['actual'], binding['cache_receipt_sha256'])
        self.assertEqual(rep['bindings'][binding['cache_path'] + '/cache_manifest.jsonl']['actual'], binding['manifest_sha256'])
        self.assertEqual(rep['audit_sources_sha256']['analysis_replay_compare.py'], barrier.COMPARE_SHA)
        for name, expected in [('primary_completion_verifier.py', barrier.FIN1_SHA),
                               ('analysis_replay_compare.py', barrier.COMPARE_SHA)]:
            self.assertEqual(hashlib.sha256((HERE/name).read_bytes().replace(b'\r\n', b'\n')).hexdigest(), expected)
        self.check('smoke_complete', [binding, completion], barrier.UNVERIFIED)
        self.check('smoke_fin1', [binding, completion, fin1], barrier.REPLAY_READY)
        self.check('smoke_replay_AB', [binding, completion, fin1, replay], barrier.LEAD_READY)
        primary, primary_completion, _, _ = fixtures()
        self.check('smoke_cannot_unlock_primary', [primary, primary_completion, fin1, replay], barrier.UNVERIFIED)
        # Original smoke auto-analysis was NOT COMPARED in accepted REPRO1.
        old = deepcopy(replay)
        old['result'] = rep['original_smoke_comparison']
        self.check('old_smoke_autoanalysis_not_compared', [binding, completion, fin1, old], barrier.REPLAY_READY)
        scratch = HERE / 'close1'
        scratch.mkdir(exist_ok=True)
        bad = deepcopy(replay)
        bad['binding']['cache_path'] += '-wrong-cache'
        path = scratch / 'mutated_smoke_replay_receipt.json'
        path.write_text(json.dumps(bad, indent=2) + '\n', encoding='utf-8')
        self.check('scratch_binding_mutation', [binding, completion, fin1, json.loads(path.read_text())], barrier.REPLAY_READY)
        (scratch / 'smoke_rehearsal_envelopes.json').write_text(json.dumps(
            {'scope': 'reused completed engineering smoke receipts; A/B rehearsal, not original auto-analysis parity',
             'binding': binding, 'completion': completion, 'fin1': fin1, 'replay': replay}, indent=2) + '\n', encoding='utf-8')
        for p in (fin_path, rep_path):
            self.assertEqual(p.read_bytes(), original[p.name])


if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(BarrierTests))
    receipt = {'task': 'T013-CLOSE1', 'task_start_head': barrier.TASK_HEAD,
               'contract_version': barrier.VERSION, 'status': 'PASS' if result.wasSuccessful() else 'FAIL',
               'tests_run': result.testsRun, 'fixtures': OUTCOMES,
               'command': 'D:/anaconda3/python.exe research_log/t013/test_finalization_barrier.py',
               'accepted_sources': {'fin1_sha256': barrier.FIN1_SHA, 'comparator_sha256': barrier.COMPARE_SHA},
               'artifact_sha256': {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                                   for name in ['finalization_barrier.py', 'test_finalization_barrier.py']},
               'active_primary_scientific_result_opened': False,
               'active_primary_prediction_content_opened': False,
               'frozen_scientific_source_or_run_modified': False,
               'fin1_or_replay_executed': False,
               'smoke_dry_run': 'Reused accepted FIN1 and frozen smoke replay A/B receipts; never claims original-auto-analysis comparison.'}
    (HERE / 'finalization_barrier_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    raise SystemExit(not result.wasSuccessful())
