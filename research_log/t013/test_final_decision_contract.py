"""Hand-authored synthetic metadata only; run with standard-library Python."""
from copy import deepcopy
import hashlib
from itertools import product
import json
from pathlib import Path
import subprocess
import unittest

import final_decision_contract as contract


def synthetic_summary():
    """Shape fixture, not experimental evidence or an arithmetic gate fixture."""
    cell = [1., 2., 3., 4., 5., 6., 7., 8.]
    table = [[cell[:] for _ in range(3)] for _ in range(5)]
    interactions = [[0., 1., 0.] for _ in range(4)]
    assessment = {
        'D_AP50': deepcopy(interactions), 'A_AP50': deepcopy(interactions),
        'D_AP50_ci95': [deepcopy(interactions), deepcopy(interactions)],
        'A_AP50_ci95': [deepcopy(interactions), deepcopy(interactions)],
        'hard_minus_random': [1.] * 4, 'hard_minus_random_ci95': [[1.] * 4, [1.] * 4],
        'mean_A_hard': 1., 'mean_A_hard_ci95': [1., 1.],
        'mean_hard_minus_random': 1., 'mean_hard_minus_random_ci95': [1., 1.],
        'gate1': True, 'gate1_corruptions': [True] * 4, 'gate2': True,
        'gate3_statistical_support': True, 'gate4_recorded_checks': True,
        'research_acceptance': 'Research Lead decision required',
        'gate3_diagnostics': {key: {'per_corruption': [1.] * 4, 'mean': 1.,
                                  'mean_ci95': [1., 1.], 'positive_corruptions': 4,
                                  'statistical_support': True} for key in contract.FAMILIES}}
    return {
        'contract_version': contract.VERSION,
        'evidence': {name: {'status': 'PASS', 'receipt_ref': 'synthetic-only/' + name}
                     for name in ('fin1', 'full_cache_replay')},
        'provenance': {'run_id': contract.RUN, 'freeze_commit': contract.FREEZE,
                       'release_id': contract.RELEASE,
                       **{key: 'synthetic-placeholder' for key in contract.PROVENANCE_FIELDS}},
        'results': {'kind': 'T013-NATIVE30', 'image_count': 1000,
                    'conditions': contract.CONDITIONS[:], 'vocabularies': contract.VOCABS[:],
                    'metric_order': contract.METRICS[:], 'point_metrics': table,
                    'metric_ci95': [deepcopy(table), deepcopy(table)],
                    'replicates': 1000, 'seed': 20260913,
                    'margin_common_localized_gt_counts': [10, 20, 30, 40],
                    'assessment': assessment},
        'lead_review': {'gate3_coherent': True, 'gate4': True,
                        'review_ref': 'synthetic-only/lead',
                        'gate3_rationale': 'synthetic coherent fixture',
                        'gate4_history_audit_ref': 'synthetic-only/history'}}


OUTCOMES = []


class DecisionContractTests(unittest.TestCase):
    def test_all_gate_branches_and_yolo_invariance(self):
        for g1, g2, g3, g4, recorded in product((False, True), repeat=5):
            summary = synthetic_summary()
            assessment = summary['results']['assessment']
            assessment.update(gate1=g1, gate2=g2, gate4_recorded_checks=recorded)
            summary['lead_review'].update(gate3_coherent=g3, gate4=g4)
            if not (g4 and recorded):
                expected = contract.INVALID
            elif not (g1 and g2):
                expected = contract.NEGATIVE
            elif g3:
                expected = contract.COHERENT
            else:
                expected = contract.UNRESOLVED
            self.assertEqual(contract.decide(summary), expected)
            summary['yolo_world'] = 'PASS'
            self.assertEqual(contract.decide(summary), expected)
            OUTCOMES.append({'fixture': 'gate_branch', 'gate1': g1, 'gate2': g2,
                             'gate3_coherent': g3, 'gate4_lead': g4,
                             'gate4_recorded': recorded, 'state': expected,
                             'yolo_pass_state_unchanged': True})

    def test_integrity_reproduction_nonpass_precedes_science(self):
        for name in ('fin1', 'full_cache_replay'):
            for status in ('FAIL', 'PENDING', 'NOT_RUN'):
                summary = synthetic_summary()
                summary['evidence'][name]['status'] = status
                # No fabricated scientific output needed to report failed integrity.
                del summary['results']
                self.assertEqual(contract.decide(summary), contract.BLOCKED)
                summary['yolo_world'] = 'PASS'
                self.assertEqual(contract.decide(summary), contract.BLOCKED)
                OUTCOMES.append({'fixture': name + '_' + status, 'state': contract.BLOCKED,
                                 'yolo_pass_state_unchanged': True})

    def test_missing_mandatory_fields_rejected(self):
        paths = [('results', 'point_metrics'), ('results', 'metric_ci95'),
                 ('results', 'margin_common_localized_gt_counts'),
                 ('results', 'assessment', 'hard_minus_random_ci95'),
                 ('results', 'assessment', 'mean_A_hard_ci95'),
                 ('results', 'assessment', 'D_AP50_ci95'),
                 ('results', 'assessment', 'A_AP50_ci95'),
                 ('results', 'assessment', 'mean_hard_minus_random_ci95'),
                 ('results', 'assessment', 'gate3_diagnostics'),
                 ('lead_review', 'gate3_coherent'), ('lead_review', 'gate4_history_audit_ref'),
                 ('provenance', 'environment_sha256')]
        paths += [('results', 'assessment', 'gate3_diagnostics', family)
                  for family in contract.FAMILIES]
        for path in paths:
            summary = synthetic_summary()
            parent = summary
            for key in path[:-1]:
                parent = parent[key]
            del parent[path[-1]]
            with self.assertRaises(ValueError):
                contract.decide(summary)
            OUTCOMES.append({'fixture': 'missing:' + '.'.join(path), 'state': 'REJECTED'})

    def test_selected_table_or_corruption_subset_rejected(self):
        for path in [('point_metrics',), ('assessment', 'D_AP50'),
                     ('assessment', 'hard_minus_random')]:
            summary = synthetic_summary()
            item = summary['results']
            for key in path:
                item = item[key]
            item.pop()
            with self.assertRaises(ValueError):
                contract.decide(summary)
            OUTCOMES.append({'fixture': 'subset:' + '.'.join(path), 'state': 'REJECTED'})

    def test_undefined_diagnostics_remain_disclosed(self):
        summary = synthetic_summary()
        summary['lead_review']['gate3_coherent'] = False
        summary['results']['metric_ci95'] = None
        summary['results']['margin_common_localized_gt_counts'] = [0.] * 4
        item = summary['results']['assessment']['gate3_diagnostics'][contract.FAMILIES[2]]
        item.update(per_corruption=[float('nan')] * 4, mean=float('nan'), mean_ci95=None,
                    positive_corruptions=0, statistical_support=False)
        self.assertEqual(contract.decide(summary), contract.UNRESOLVED)
        OUTCOMES.append({'fixture': 'explicit_undefined_support', 'state': contract.UNRESOLVED})

    def test_support_flag_does_not_replace_lead_gate3(self):
        summary = synthetic_summary()
        summary['lead_review']['gate3_coherent'] = False
        self.assertEqual(contract.decide(summary), contract.UNRESOLVED)
        OUTCOMES.append({'fixture': 'statistical_support_true_lead_false',
                         'state': contract.UNRESOLVED})


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(DecisionContractTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    root = Path(__file__).resolve().parents[2]
    directory = Path(__file__).resolve().parent
    source_paths = ['research_log/t013/PLAN.md', 'scripts/t013_analysis.py',
                    'scripts/t013_coco.py', 'scripts/t013_diagnostics.py',
                    'research_log/t013/native30_freeze.json']
    bindings = {}
    for path in source_paths:
        frozen = subprocess.check_output(['git', 'show', contract.FREEZE + ':' + path], cwd=root)
        actual = (root / path).read_bytes()
        bindings[path] = {'frozen_sha256': hashlib.sha256(frozen).hexdigest(),
                          'working_sha256': hashlib.sha256(actual).hexdigest(),
                          'equal': actual == frozen}
    artifact_paths = ['FINAL_DECISION_CONTRACT.md', 'final_decision_contract.py',
                      'test_final_decision_contract.py']
    receipt = {'task': 'T013-DEC1', 'contract_version': contract.VERSION,
               'lead_commit': '753facb', 'freeze_commit': contract.FREEZE,
               'status': 'PASS' if result.wasSuccessful() and all(
                   item['equal'] for item in bindings.values()) else 'FAIL',
               'tests_run': result.testsRun, 'fixtures': OUTCOMES,
               'source_bindings': bindings,
               'artifact_sha256': {path: hashlib.sha256((directory / path).read_bytes()).hexdigest()
                                   for path in artifact_paths},
               'active_primary_scientific_result_opened': False,
               'active_primary_prediction_content_opened': False,
               'frozen_scientific_source_or_run_modified': False,
               'fixture_values_are_scientific_results': False}
    (directory / 'final_decision_contract_receipt.json').write_text(
        json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    raise SystemExit(0 if receipt['status'] == 'PASS' else 1)
