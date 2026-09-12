"""Official native-256 model and official single-image preprocessing, frozen CPU."""
import sys

import numpy as np
from PIL import Image
import torch

from scripts.t013_detector import configure_torch, state_hash, CONDITIONS, corrupted_pixels
from scripts.t013_text import caption_and_spans, positive_map


def load_native(assets):
    configure_torch()
    sys.path.insert(0, str(assets / 'native'))
    from groundingdino.models import build_model
    from groundingdino.util.slconfig import SLConfig
    from groundingdino.util.misc import clean_state_dict
    import groundingdino.datasets.transforms as T
    config = SLConfig.fromfile(str(assets / 'native/groundingdino/config/GroundingDINO_SwinT_OGC.py'))
    config.device = 'cpu'
    config.text_encoder_type = str(assets / 'native_bert')
    model = build_model(config).eval()
    checkpoint = torch.load(assets / 'groundingdino_swint_ogc.pth', map_location='cpu', weights_only=False)
    loaded = model.load_state_dict(clean_state_dict(checkpoint['model']), strict=False)
    assert not loaded.missing_keys, loaded
    model.requires_grad_(False)
    transform = T.Compose([T.RandomResize([800], max_size=1333), T.ToTensor(),
                           T.Normalize([.485, .456, .406], [.229, .224, .225])])
    return model, transform


def preprocess(transform, pixels):
    return transform(Image.fromarray(pixels), None)[0]


@torch.inference_mode()
def detect_native(model, transform, pixels, names):
    caption, spans = caption_and_spans(names)
    encoded = model.tokenizer(caption, return_offsets_mapping=True)
    length = len(encoded.input_ids)
    assert length == (195 if len(names) == 80 else 255) and model.max_text_len == 256
    tensor = preprocess(transform, pixels)
    output = model(tensor[None], captions=[caption])
    mapping = torch.as_tensor(positive_map(encoded.offset_mapping, spans, 256)[:, :length].T)
    class_scores = output['pred_logits'][0, :, :length].sigmoid() @ mapping
    scores, flat = torch.topk(class_scores.flatten(), 300)
    boxes = output['pred_boxes'][0]
    center, size = boxes[:, :2], boxes[:, 2:]
    boxes = torch.cat([center - size / 2, center + size / 2], dim=-1)
    height, width = pixels.shape[:2]
    boxes = boxes * torch.tensor([width, height, width, height])
    return {'boxes': boxes.numpy(), 'class_scores': class_scores.numpy(),
            'top_query_ids': (flat // len(names)).numpy(), 'top_labels': (flat % len(names)).numpy(),
            'top_scores': scores.numpy(), 'token_logits': output['pred_logits'][0, :, :length].numpy(),
            'normalized_cxcywh': output['pred_boxes'][0].numpy()}
