"""Model-free T013-YW-P2 fixture; not a detector or NMS implementation.

Supply runtime_texts to native text encoding/fusion/scoring/postprocessing.
Only AFTER native selection, call semantic_predictions on its retained rows.
There is deliberately no preselection-pool or refill input to that function.
"""
import hashlib
import json
from pathlib import Path


def runtime_texts(semantic_names):
    """Keep scientific vocabulary order and append one trailing U+0020."""
    return list(semantic_names) + [' ']


def class_indices(semantic_names):
    """Canonical 0..79, remaining semantic entries are distractors, then blank."""
    return {
        'canonical': list(range(80)),
        'distractor': list(range(80, len(semantic_names))),
        'blank': len(semantic_names),
    }


def semantic_predictions(native_selected_rows, blank_index):
    """Remove blank rows after native selection; keep semantic rows untouched.

    Returns (semantic rows, number of retained blank predictions). Never sorts,
    clips, scores, performs NMS, or refills discarded prediction slots.
    """
    rows = [row for row in native_selected_rows if row['label'] != blank_index]
    return rows, len(native_selected_rows) - len(rows)


def build_receipt():
    """Bind this protocol fixture to the unchanged semantic/P1 artifacts."""
    root = Path(__file__).resolve().parents[2]
    folder = root / 'research_log/t013_yoloworld'
    vocab_path = root / 'research_log/t013/vocabulary_native30.json'
    p1_path = folder / 'protocol_freeze.json'
    vocab_bytes, p1_bytes = vocab_path.read_bytes(), p1_path.read_bytes()
    vocab = json.loads(vocab_bytes)['vocabularies']
    p1 = json.loads(p1_bytes)
    native = p1['native_postprocessing']
    constant_bytes = json.dumps(native, sort_keys=True, separators=(',', ':')).encode()
    paths = [vocab_path, p1_path, Path(__file__), folder / 'test_protocol_adapter.py']
    return {
        'task': 'T013-YW-P2',
        'scope': 'model-free dynamic-vocabulary interaction protocol fixture',
        'blank_rule_authority': 'Research Lead pre-outcome convention; not uniquely inferred COCO recipe',
        'lead_revision': 'ccec9fd',
        'source_revision': p1['source_revision'],
        'mmyolo_revision': p1['mmyolo_revision'],
        'selected_checkpoint': p1['selected_checkpoint'],
        'checkpoint_sha256': p1['checkpoint_sha256'],
        'semantic_vocabulary_sha256': hashlib.sha256(vocab_bytes).hexdigest(),
        'p1_receipt_sha256': hashlib.sha256(p1_bytes).hexdigest(),
        'native_postprocessing': native,
        'native_postprocessing_sha256': hashlib.sha256(constant_bytes).hexdigest(),
        'constant_hash_serialization': 'UTF-8 json.dumps(sort_keys=True,separators=(comma,colon))',
        'runtime_vocabularies': {
            name: {'semantic_count': len(names), 'runtime_count': len(names) + 1,
                   'texts': runtime_texts(names), 'indices': class_indices(names)}
            for name, names in vocab.items()
        },
        'blank': {'string': ' ', 'codepoint': 'U+0020', 'count': 1,
                  'placement': 'last', 'participates_in_native_selection': True,
                  'excluded_after_selection_from_canonical_and_distractor_metrics': True,
                  'refill': False},
        'same_rule_all_visual_conditions': True,
        'published_coco_baseline_reproduced': False,
        'detector_runtime_authorized': False,
        'file_sha256': {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in paths},
    }


if __name__ == '__main__':
    output = Path(__file__).with_name('protocol_adapter_receipt.json')
    output.write_text(json.dumps(build_receipt(), indent=2) + '\n', encoding='utf-8')
    print(output)
