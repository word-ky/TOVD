import copy
import unittest

from tovd.semantic_shift import analyze, dataset_deltas, observe, preflight


def detection(label='cat', score=0.8, box=None, query_id=0):
    return {'box': box or [0, 0, 10, 10], 'label': label, 'score': score, 'query_id': query_id}


def fixture():
    return {'condition': 'clean', 'canonical_labels': ['cat', 'dog'],
            'distractor_labels': {'Vhard30': ['lynx'], 'Vrand30': ['chair']},
            'images': [{'image_id': 'synthetic',
                        'gt': [{'box': [0, 0, 10, 10], 'label': 'cat', 'iscrowd': False}],
                        'detections': {v: [detection()] for v in ('V0', 'Vhard30', 'Vrand30')}}]}


class SemanticShiftTests(unittest.TestCase):
    def hard(self, data):
        return analyze(data)['metrics']['Vhard30']

    def test_identical(self):
        result = analyze(fixture())
        for metrics in result['metrics'].values():
            for name in ('V0_correct_survival', 'box_stability_mean', 'box_stability_median'):
                self.assertEqual(metrics[name]['value'], 1)
                self.assertEqual(metrics[name]['support'], 1)
            for name in ('semantic_failure_given_localized', 'distractor_takeover_rate', 'localization_loss_rate', 'score_delta'):
                self.assertEqual(metrics[name]['value'], 0)

    def test_takeover(self):
        data = fixture()
        data['images'][0]['detections']['Vhard30'] = [detection('lynx')]
        m = self.hard(data)
        self.assertEqual(m['distractor_takeover_rate'], {'value': 1, 'numerator': 1, 'support': 1})
        self.assertEqual(m['semantic_failure_given_localized']['value'], 1)
        self.assertEqual(m['localization_loss_rate']['value'], 0)
        self.assertEqual(m['V0_correct_survival']['value'], 0)
        self.assertEqual(m['box_stability_mean']['value'], 1)

    def test_canonical_misclassification(self):
        data = fixture()
        data['images'][0]['detections']['Vhard30'] = [detection('dog')]
        m = self.hard(data)
        self.assertEqual(m['semantic_failure_given_localized']['value'], 1)
        self.assertEqual(m['distractor_takeover_rate']['value'], 0)

    def test_localization_loss(self):
        data = fixture()
        data['images'][0]['detections']['Vhard30'] = [detection(box=[20, 20, 30, 30])]
        m = self.hard(data)
        self.assertEqual(m['localization_loss_rate']['value'], 1)
        self.assertEqual(m['V0_correct_survival']['value'], 0)
        self.assertEqual(m['semantic_failure_given_localized'], {'value': None, 'numerator': 0, 'support': 0})
        self.assertIsNone(m['score_delta']['value'])

    def test_iou_then_score_then_order(self):
        gt = fixture()['images'][0]['gt'][0]
        ds = [detection(score=1, box=[0, 0, 10, 15]), detection('dog', 0.5), detection('cat', 0.8), detection('dog', 0.8)]
        obs = observe(gt, ds, set())
        self.assertEqual(obs['selected_order'], 2)
        self.assertTrue(obs['correct'])
        self.assertEqual(observe(gt, [ds[0]], set())['selected_order'], 0)

    def test_iou_boundary_inclusive(self):
        gt = fixture()['images'][0]['gt'][0]
        self.assertEqual(observe(gt, [detection(box=[0, 0, 10, 20])], set())['gt_iou'], 0.5)
        self.assertIsNone(observe(gt, [detection(box=[0, 0, 10, 21])], set()))

    def test_empty_and_crowd(self):
        for mode in ('empty_images', 'crowd', 'empty_detections'):
            with self.subTest(mode=mode):
                data = fixture()
                if mode == 'empty_images':
                    data['images'] = []
                elif mode == 'crowd':
                    data['images'][0]['gt'][0]['iscrowd'] = True
                else:
                    data['images'][0]['detections'] = {v: [] for v in ('V0', 'Vhard30', 'Vrand30')}
                r = analyze(data)
                for metrics in r['metrics'].values():
                    for metric in metrics.values():
                        self.assertIsNone(metric['value'])
                        self.assertEqual(metric['support'], 0)
                self.assertTrue(all(c['value'] is None for c in r['hard_vs_random_degradation'].values()))

    def test_initially_wrong_included_in_box_score_support_only(self):
        data = fixture()
        data['images'][0]['detections']['V0'] = [detection('dog', 0.8)]
        data['images'][0]['detections']['Vhard30'] = [detection('cat', 0.5)]
        m = self.hard(data)
        self.assertIsNone(m['V0_correct_survival']['value'])
        self.assertEqual(m['box_stability_mean']['support'], 1)
        self.assertAlmostEqual(m['score_delta']['value'], -0.3)

    def test_hard_random_orientation(self):
        data = fixture()
        data['images'][0]['detections']['Vhard30'] = [detection('lynx', 0.4, [0, 0, 10, 15])]
        r = analyze(data)['hard_vs_random_degradation']
        for name in ('V0_correct_survival', 'semantic_failure_given_localized', 'distractor_takeover_rate', 'box_stability_mean', 'box_stability_median', 'score_delta'):
            self.assertGreater(r[name]['value'], 0)
        data['images'][0]['detections']['Vhard30'] = []
        r = analyze(data)['hard_vs_random_degradation']
        self.assertEqual(r['localization_loss_rate']['value'], 1)
        self.assertIsNone(r['semantic_failure_given_localized']['value'])
        self.assertEqual((r['semantic_failure_given_localized']['hard_support'], r['semantic_failure_given_localized']['random_support']), (0, 1))

    def test_query_permutation_irrelevant(self):
        data = fixture()
        for v in data['images'][0]['detections']:
            data['images'][0]['detections'][v] += [detection('dog', 0.7, query_id=8)]
        changed = copy.deepcopy(data)
        for vi, ds in enumerate(changed['images'][0]['detections'].values()):
            for i, d in enumerate(ds):
                d['query_id'] = 100 - i * 11 + vi
                d['query_index'] = i + vi * 13
        self.assertEqual(analyze(data), analyze(changed))
        for ds in changed['images'][0]['detections'].values():
            for d in ds:
                del d['query_id']
                del d['query_index']
        self.assertEqual(analyze(data), analyze(changed))

    def test_pooled_gt_support_and_independent_reuse(self):
        data = fixture()
        image = data['images'][0]
        image['gt'].append(copy.deepcopy(image['gt'][0]))
        second = copy.deepcopy(image)
        second['image_id'] = 'second_synthetic'
        second['gt'] = second['gt'][:1]
        second['detections']['Vhard30'] = []
        data['images'].append(second)
        m = self.hard(data)
        self.assertEqual(m['V0_correct_survival'], {'value': 2/3, 'numerator': 2, 'support': 3})
        self.assertEqual(m['box_stability_mean']['support'], 2)

    def test_preflight_condition_and_required_fields(self):
        self.assertIsNotNone(preflight(fixture()))
        for condition in ('not_clean', '', None):
            data = fixture()
            data['condition'] = condition
            with self.assertRaisesRegex(ValueError, 'clean'):
                preflight(data)
        data = fixture()
        del data['images'][0]['detections']['Vhard30'][0]['score']
        with self.assertRaises(KeyError):
            preflight(data)

    def test_preflight_labels_and_boxes(self):
        data = fixture()
        data['images'][0]['detections']['Vhard30'][0]['label'] = 'unknown'
        with self.assertRaises(ValueError):
            preflight(data)
        data = fixture()
        data['images'][0]['gt'][0]['box'] = [0, 0, 0, 10]
        with self.assertRaises(ValueError):
            preflight(data)

    def test_dataset_delta_arithmetic_synthetic_only(self):
        summaries = {v: {m: score for m in ('AP', 'AP50', 'AR', 'AR50')}
                     for v, score in [('V0', 60), ('Vhard30', 40), ('Vrand30', 50)]}
        result = dataset_deltas(summaries)
        self.assertEqual(result['deltas']['Vhard30']['AP'], 20)
        self.assertEqual(result['HardMinusRandom_AP50'], 10)


if __name__ == '__main__':
    unittest.main()
