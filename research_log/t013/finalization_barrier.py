"""CLOSE1 metadata-only completion ordering. No I/O, commands or science imports."""
VERSION = 'T013-CLOSE1-v1'
TASK_HEAD = '2af6322facef6381835488a639761578b7fd2b16'
FREEZE = '6fec32243985ccc808123d851abf5f3dea10af99'
ROOT = '/home/wenchang/asdasdsad/wjq/TOVD'
PRIMARY = '20260912-210355-tovd-native30-primary'
RELEASE = '20260912-210306-tovd-native30-primary-freeze'
FIN1_SHA = '9d4c604b40677d81fa634715a55c7132dcbe04303a1a8a3021dc11e42273c6a8'
# Full accepted comparator hash; retain exact source identity, no new comparator.
COMPARE_SHA = '6270a32096c536deac8ec878d3cfbfeb1cc067d428781ab7beb09e78cb8acb76'
ANALYSIS_SHA = '74cc73e71385e5d38e3fbe68ff03a0f11da30e67ff39b436da90422f72e99f9c'
FILES = ['results.json', 'paired_image_draws.npy', 'bootstrap_samples.npz', 'diagnostics_per_image.npz']
RUNNING = 'PRIMARY_RUNNING'
FAILED = 'PRIMARY_FAILED_RETURN_TO_LEAD'
UNVERIFIED = 'PRIMARY_COMPLETE_UNVERIFIED'
REPLAY_READY = 'FIN1_PASS_READY_FOR_REPLAY'
LEAD_READY = 'REPLAY_PASS_READY_FOR_RESEARCH_LEAD'


def target(run_receipt_sha256, manifest_sha256, *, smoke=False):
    """Hashes must come from the completed cache metadata, never smoke for primary."""
    run = '20260912-205428-tovd-native30-pipeline-smoke' if smoke else PRIMARY
    release = '20260912-205335-tovd-native30-pipeline' if smoke else RELEASE
    cache = ROOT + '/runs/' + run + '/artifacts/cache'
    return {'contract_version': VERSION, 'task_start_head': TASK_HEAD,
            'run_id': run, 'release_id': release, 'freeze_commit': FREEZE,
            'cache_path': cache, 'cache_receipt_ref': cache + '/run_receipt.json',
            'cache_receipt_sha256': run_receipt_sha256, 'manifest_sha256': manifest_sha256,
            'fin1_version': 'T013-FIN1@8efe485', 'fin1_sha256': FIN1_SHA,
            'comparator_version': 'T013-REPRO1@5fe57f7', 'comparator_sha256': COMPARE_SHA,
            'analysis_sha256': ANALYSIS_SHA, 'scope': 'engineering_smoke' if smoke else 'primary',
            'image_count': 3 if smoke else 1000, 'record_count': 45 if smoke else 15000,
            'receipt_freeze_argument': 'd5dc807' if smoke else FREEZE,
            'analysis_reference_dir': ROOT + '/shared/t013/repro1/replay_a' if smoke
                else ROOT + '/runs/' + PRIMARY + '/artifacts/analysis'}


def digest_string(value):
    return isinstance(value, str) and len(value) == 64 and all(c in '0123456789abcdef' for c in value)


def envelope_matches(evidence, binding, tool_hash):
    return (isinstance(evidence, dict) and evidence.get('binding') == binding
            and evidence.get('tool_sha256') == tool_hash
            and isinstance(evidence.get('receipt_ref'), str) and bool(evidence['receipt_ref'])
            and digest_string(evidence.get('receipt_sha256'))
            and isinstance(evidence.get('result'), dict))


def evaluate(binding, completion, fin1=None, replay=None):
    """A workflow decision over supplied execution receipts, not a receipt signer.

    Exact command/path/hash envelopes are collected at execution. Existing FIN1
    and comparator outputs remain unchanged and are included as result payloads.
    """
    def state(name, reason):
        ready = name == LEAD_READY
        return {'state': name, 'reason': reason, 'run_id': binding.get('run_id'),
                'scope': binding.get('scope'), 'research_lead_review_authorized': ready,
                'primary_result_content_access_authorized': ready and binding.get('scope') == 'primary',
                'fin1_execution_authorized': name == UNVERIFIED and fin1 is None,
                'replay_comparison_execution_authorized': name == REPLAY_READY and replay is None,
                'scientific_acceptance': False, 'restart_resume_authorized': False,
                'helper_opened_result_content': False}

    expected = target(binding.get('cache_receipt_sha256'), binding.get('manifest_sha256'),
                      smoke=binding.get('scope') == 'engineering_smoke')
    if binding != expected or not all(digest_string(binding.get(k)) for k in
                                     ('cache_receipt_sha256', 'manifest_sha256')):
        return state(RUNNING, 'missing_or_mismatched_target_binding')
    if not isinstance(completion, dict) or any(completion.get(key) != binding[key]
            for key in ('run_id', 'release_id', 'freeze_commit')):
        return state(RUNNING, 'completion_not_bound_to_target_run')
    code = completion.get('wrapper_exit_code')
    if type(code) is int and code != 0:
        return state(FAILED, 'nonzero_wrapper_completion_preserve_and_return_to_lead')
    if (completion.get('writer_alive') is not False or completion.get('tmux_alive') is not False
            or completion.get('wrapper_completed') is not True or type(code) is not int or code != 0):
        return state(RUNNING, 'successful_wrapper_completion_and_termination_not_established')
    # analysis_result_exists is deliberately irrelevant to either transition above.
    if not envelope_matches(fin1, binding, FIN1_SHA):
        return state(UNVERIFIED, 'fin1_missing_or_stale_binding')
    result = fin1['result']
    expected_fin1 = {'status': 'PASS', 'mode': binding['scope'],
                     'scientific_freeze_commit': FREEZE,
                     'receipt_freeze_argument': binding['receipt_freeze_argument'],
                     'run_id': binding['run_id'], 'release_id': binding['release_id'],
                     'image_count': binding['image_count'], 'expected_records': binding['record_count'],
                     'run_receipt_sha256': binding['cache_receipt_sha256'],
                     'manifest_sha256': binding['manifest_sha256']}
    if any(result.get(k) != v for k, v in expected_fin1.items()):
        return state(UNVERIFIED, 'fin1_not_pass_or_result_binding_mismatch_return_to_lead')
    if not envelope_matches(replay, binding, COMPARE_SHA):
        return state(REPLAY_READY, 'replay_missing_or_stale_binding')
    if (replay.get('fin1_receipt_sha256') != fin1['receipt_sha256']
            or replay.get('left_dir') != binding['analysis_reference_dir']
            or not isinstance(replay.get('right_dir'), str) or not replay['right_dir']
            or replay['right_dir'] == replay['left_dir']
            or replay.get('analysis_exit_code') != 0 or replay.get('comparator_exit_code') != 0
            or replay.get('analysis_sha256') != ANALYSIS_SHA
            or replay.get('replicates') != (10 if binding['scope'] == 'engineering_smoke' else 1000)):
        return state(REPLAY_READY, 'replay_execution_or_reference_binding_mismatch')
    result = replay['result']
    artifacts = result.get('artifacts', {})
    if (result.get('status') != 'PASS' or set(artifacts) != set(FILES)
            or any(item.get('equal') is not True for item in artifacts.values())):
        return state(REPLAY_READY, 'comparison_not_pass_preserve_and_return_to_lead')
    return state(LEAD_READY, 'same_completed_run_fin1_and_frozen_replay_comparison_pass')
