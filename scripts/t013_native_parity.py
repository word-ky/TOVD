"""Lead-mandated native256 versus HF1024 V0 comparison; CPU donor path."""
import argparse
import json
from pathlib import Path
import sys

import numpy as np
from PIL import Image
import torch

from scripts.t013_detector import load_detector, state_hash
from scripts.t013_text import caption_and_spans, positive_map


@torch.inference_mode()
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--assets", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--detection-level", action="store_true")
    args = parser.parse_args()
    sys.path.insert(0, str(args.assets / "native"))
    from groundingdino.models import build_model
    from groundingdino.util.slconfig import SLConfig
    from groundingdino.util.misc import clean_state_dict

    processor, hf = load_detector(args.assets / "model", "cpu")
    # Reuse the already downloaded frozen BERT weights/tokenizer for the native
    # constructor; the complete native checkpoint is loaded immediately afterward.
    bert_dir = args.assets / "native_bert"
    hf.model.text_backbone.save_pretrained(bert_dir)
    processor.tokenizer.save_pretrained(bert_dir)
    config = SLConfig.fromfile(str(args.assets / "native/groundingdino/config/GroundingDINO_SwinT_OGC.py"))
    config.device = "cpu"
    config.text_encoder_type = str(bert_dir)
    native = build_model(config).eval()
    checkpoint = torch.load(args.assets / "groundingdino_swint_ogc.pth", map_location="cpu", weights_only=False)
    loading = native.load_state_dict(clean_state_dict(checkpoint["model"]), strict=False)
    assert not loading.missing_keys, loading
    native.requires_grad_(False)
    before = {"native": state_hash(native), "hf": state_hash(hf)}
    selection = json.loads(Path("research_log/t013/image_selection.json").read_text())
    vocabulary = json.loads(Path("research_log/t013/vocabulary_matched.json").read_text())
    caption, spans = caption_and_spans(vocabulary["vocabularies"]["V0"])
    encoded = processor.tokenizer(caption, return_offsets_mapping=True)
    length = len(encoded.input_ids)
    mapping = torch.as_tensor(positive_map(encoded.offset_mapping, spans)[:, :length].T)
    records = []
    for image_id in selection["smoke_ids"]:
        image = Image.open(args.assets / "smoke_images" / f"{image_id:012d}.jpg").convert("RGB")
        inputs = processor(images=image, text=caption, return_tensors="pt")
        ours = hf(**inputs)
        repeated = hf(**inputs)
        replay = bool(torch.equal(ours.pred_boxes, repeated.pred_boxes) and torch.equal(ours.logits, repeated.logits))
        donor = native(inputs.pixel_values, captions=[caption])
        native_scores = donor["pred_logits"][0, :, :length].sigmoid() @ mapping
        hf_scores = ours.logits[0, :, :length].sigmoid() @ mapping
        box_delta = float((ours.pred_boxes - donor["pred_boxes"]).abs().max())
        score_delta = float((hf_scores - native_scores).abs().max())
        record = {"image_id": image_id, "max_abs_normalized_box_error": box_delta,
                  "max_abs_canonical_score_error": score_delta, "hf_replay_exact": replay,
                  "pass": box_delta <= 1e-4 and score_delta <= 1e-4 and replay}
        if args.detection_level:
            import scipy
            from scripts.t013_parity_matching import compare_detections, raw_box_diagnostics
            assert scipy.__version__ == "1.17.0", scipy.__version__
            detections, raw = {}, {}
            for name, boxes, scores in [("native", donor["pred_boxes"][0], native_scores),
                                        ("hf", ours.pred_boxes[0], hf_scores)]:
                center, size = boxes[:, :2], boxes[:, 2:]
                xyxy = torch.cat([center - size / 2, center + size / 2], dim=-1)
                values, flat = torch.topk(scores.flatten(), 300)
                query_ids, labels = flat // 80, flat % 80
                detections[name] = {'boxes': xyxy[query_ids].numpy(), 'labels': labels.numpy(),
                                    'scores': values.numpy()}
                raw[name + '_cxcywh'] = boxes.numpy()
                raw[name + '_xyxy'] = xyxy.numpy()
                raw[name + '_class_scores'] = scores.numpy()
                raw[name + '_top_query_ids'] = query_ids.numpy()
                raw[name + '_top_labels'] = labels.numpy()
                raw[name + '_top_scores'] = values.numpy()
            np.savez_compressed(args.output.parent / f'parity_b_raw_{image_id}.npz', **raw)
            record['raw_indexwise_pass'] = record['pass']
            record['detection_level'] = compare_detections(detections['native'], detections['hf'])
            record['raw_box_diagnostics'] = raw_box_diagnostics(
                raw['native_cxcywh'], raw['hf_cxcywh'], raw['native_xyxy'], raw['hf_xyxy'])
            record['pass'] = record['detection_level']['pass'] and replay
        records.append(record)
        print(json.dumps({k: v for k, v in record.items()
                          if k not in ('detection_level', 'raw_box_diagnostics')}), flush=True)
    after = {"native": state_hash(native), "hf": state_hash(hf)}
    assert before == after
    result = {"kind": "native256_vs_hf1024_v0", "tolerance": 1e-4, "device": "cpu",
              "records": records, "state_hashes_before": before, "state_hashes_after": after,
              "unexpected_native_checkpoint_keys": loading.unexpected_keys,
              "preprocessing": "Identical HF processor pixel tensor supplied to both implementations",
              "validity": all(row["pass"] for row in records)}
    if args.detection_level:
        result.update(kind='T013-PARITY-B', iou_tolerance=.999, score_tolerance=1e-4,
                      num_select=300, nms=False, score_threshold=None, scipy_version=scipy.__version__,
                      assignment='SciPy 1.17.0 LSAP, negative float64 IoU, fixed topk input order; no score cost or perturbation')
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    if not result["validity"]:
        raise SystemExit("Native/HF parity failed fixed Lead tolerance; stop for Lead review")


if __name__ == "__main__":
    main()
