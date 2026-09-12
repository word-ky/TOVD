"""P1 source-only receipt: standard-library parsing, no model/package imports.

Run from the TOVD root: python research_log/t013_yoloworld/inspect_p1_sources.py
Uses the P0 pinned checkout and the downloaded pinned MMYOLO source snapshots.
"""
import ast
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'research_log/t013_yoloworld'
CLONE = ROOT / '.autodl/yoloworld/YOLO-World'
REV = 'b1b09f2f0340ca7dede69e10b7e909c469677fd9'
MMREV = '4d97b3a06609dba94b8ec584be2f2029cfdb7519'
CONFIG = 'configs/pretrain/yolo_world_v2_s_vlpan_bn_2e-3_100e_4x8gpus_obj365v1_goldg_train_1280ft_lvis_minival.py'
BASE = 'configs/yolov8/yolov8_s_syncbn_fast_8xb16-500e_coco.py'
FILES = {
    CONFIG: [[1, 45], [47, 54], [127, 160]],
    'docs/update_20250123.md': [[15, 26], [60, 75], [98, 108]],
    'README.md': [[96, 143], [189, 207]],
    'demo/gradio_demo.py': [[73, 98], [133, 136], [229, 253]],
    'demo/image_demo.py': [[97, 110], [170, 191], [206, 207]],
    'tools/test.py': [[73, 82], [112, 128], [145, 150]],
    'yolo_world/datasets/transformers/mm_transforms.py': [[89, 96], [100, 129]],
    'yolo_world/datasets/mm_dataset.py': [[33, 44], [66, 72]],
    'yolo_world/models/detectors/yolo_world.py': [[34, 60], [73, 104]],
    'yolo_world/models/backbones/mm_backbone.py': [[86, 98]],
    'yolo_world/models/dense_heads/yolo_world_head.py': [[342, 348], [396, 411], [564, 617], [643, 652], [675, 734]],
    'data/texts/coco_class_texts.json': [[1, 1]],
    'data/texts/lvis_v1_class_texts.json': [[1, 1]],
    'LICENSE': [],
}
sources = []
for name, lines in FILES.items():
    data = subprocess.check_output(['git', '-C', str(CLONE), 'show', f'{REV}:{name}'])
    target = OUT / 'p1_source/yolo_world' / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    sources.append(dict(repository='AILab-CVC/YOLO-World', revision=REV,
                        path=name, lines=lines,
                        snapshot=str(target.relative_to(ROOT)).replace('\\', '/'),
                        sha256=hashlib.sha256(data).hexdigest(),
                        url=f'https://github.com/AILab-CVC/YOLO-World/blob/{REV}/{name}'))
for target in sorted((OUT / 'p1_source/mmyolo').rglob('*')):
    if target.is_file():
        name = target.relative_to(OUT / 'p1_source/mmyolo').as_posix()
        sources.append(dict(repository='onuralpszr/mmyolo', revision=MMREV,
                            path=name,
                            snapshot=target.relative_to(ROOT).as_posix(),
                            sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                            url=f'https://github.com/onuralpszr/mmyolo/blob/{MMREV}/{name}'))

# Read only the literal dict(...) expression; do not execute/import configs.
base_tree = ast.parse((OUT / 'p1_source/mmyolo' / BASE).read_text())
node = next(n.value for n in base_tree.body if isinstance(n, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == 'model_test_cfg' for t in n.targets))
def literal(node):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'dict':
        return {k.arg: literal(k.value) for k in node.keywords}
    return ast.literal_eval(node)

counts = {}
for name in ['coco_class_texts.json', 'lvis_v1_class_texts.json']:
    captions = json.loads((OUT / 'p1_source/yolo_world/data/texts' / name).read_bytes())
    counts[name] = dict(classes=len(captions), blank_class_indices=[
        i for i, aliases in enumerate(captions) if any(not text.strip() for text in aliases)])

receipt = dict(
    task='T013-YW-P1', status='BLOCKED_SOURCE_AMBIGUITY',
    recorded_at=datetime.now(timezone.utc).isoformat(),
    lead_commit='c2f24e28d0579f2b0c55a8181c4532a721c354db',
    source_revision=REV, mmyolo_revision=MMREV, selected_config=CONFIG,
    selected_checkpoint='s_stage2-4466ab94.pth',
    checkpoint_sha256='4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458',
    semantic_class_counts=[80, 110, 110],
    blank_handling_uniquely_resolved=False,
    frozen_blank_string=None, frozen_blank_count=None, frozen_blank_placement=None,
    blank_evidence=dict(text_demo=dict(count=1, string=' ', unicode='U+0020', placement='after semantic classes'),
                        selected_LVIS_evaluation=dict(count=0, automatic_append=False),
                        class_text_files=counts,
                        training_padding=dict(string='', variable_count=True, scope='training only'),
                        published_COCO_recipe_with_blank_rule_found=False),
    native_postprocessing=dict(selected_config_constants_resolved=True, test_cfg=literal(node),
                               with_nms=True, rescale=True, yolox_style=False,
                               demo_extra_filtering=False, test_time_augmentation=False,
                               use_same_native_contract_for_all_15_cells=True,
                               full_published_COCO_recipe_verified=False),
    execution=dict(yolo_image_inference_count=0, detector_load_count=0,
                   package_install_count=0, checkpoint_payload_download_count=0,
                   grounding_partial_scientific_metrics_inspected=False,
                   active_primary_modified=False),
    next_action='Return blank/COCO recipe ambiguity to Research Lead; no installation or runtime variants.',
    sources=sources,
)
(OUT / 'protocol_freeze.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
print(json.dumps(dict(status=receipt['status'], source_files=len(sources),
                     test_cfg=literal(node), class_text_counts=counts,
                     blank_handling_uniquely_resolved=False), indent=2))
