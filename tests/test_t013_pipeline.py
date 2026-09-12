import json
import numpy as np
from scripts.t013_analysis import analyze, CONDITIONS, VOCABS


def test_full_cached_analysis_on_known_detector_outputs(tmp_path):
    dataset = {'info': {}, 'images': [{'id': 1}, {'id': 2}],
               'categories': [{'id': 1, 'name': 'a'}, {'id': 3, 'name': 'b'}],
               'annotations': [{'id': i, 'image_id': i, 'category_id': 1 if i == 1 else 3,
                                'bbox': [0, 0, 10, 10], 'area': 100, 'iscrowd': 0} for i in [1, 2]]}
    for condition in CONDITIONS:
        for vocabulary in VOCABS:
            folder = tmp_path / 'raw' / condition / vocabulary
            folder.mkdir(parents=True)
            for image_id in [1, 2]:
                scores = np.array([[.9, .1, .05], [.1, .9, .05], [.1, .1, .8]])
                if vocabulary == 'V0':
                    scores = scores[:, :2]
                label = image_id - 1
                np.savez(folder / f'{image_id:012d}.npz',
                         boxes=np.array([[0., 0, 10, 10], [0., 0, 10, 10], [30., 30, 40, 40]]),
                         class_scores=scores, top_query_ids=np.array([label]),
                         top_labels=np.array([label]), top_scores=np.array([.9]))
    result = analyze(dataset, [1, 2], tmp_path / 'raw', tmp_path / 'result', replicates=3, smoke=True)
    point = np.array(result['point_metrics'])
    np.testing.assert_allclose(point[:, :, :4], 100)
    assert not result['assessment']['gate1'] and not result['assessment']['gate2']
    assert result['kind'] == 'engineering_smoke_not_scientific'
    assert json.loads((tmp_path / 'result/results.json').read_text())['image_count'] == 2
    assert np.load(tmp_path / 'result/paired_image_draws.npy').shape == (3, 2)
