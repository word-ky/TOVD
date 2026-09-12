"""Frozen Grounding DINO and deterministic corruption primitives for T013."""
import hashlib

import numpy as np
from PIL import Image
import torch
from transformers import AutoProcessor, GroundingDinoForObjectDetection

from scripts.t013_text import caption_and_spans, positive_map


CONDITIONS = ["clean", "gaussian_noise", "motion_blur", "fog", "jpeg_compression"]
CAPACITY = 1024
NUM_SELECT = 300
DIAGNOSTIC_THRESHOLD = 0.25


def configure_torch():
    torch.set_num_threads(4)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True


def load_detector(path, device, capacity=CAPACITY):
    configure_torch()
    processor = AutoProcessor.from_pretrained(path, local_files_only=True)
    model, loading_info = GroundingDinoForObjectDetection.from_pretrained(
        path, local_files_only=True, max_text_len=capacity, disable_custom_kernels=True,
        output_loading_info=True,
    )
    assert not loading_info["missing_keys"] and not loading_info["mismatched_keys"], loading_info
    model = model.eval().requires_grad_(False).to(device)
    return processor, model


def state_hash(model):
    digest = hashlib.sha256()
    for name, tensor in sorted(model.state_dict().items()):
        digest.update(name.encode())
        digest.update(tensor.detach().cpu().contiguous().numpy().tobytes())
    return digest.hexdigest()


def corrupted_pixels(image, image_id, condition):
    pixels = np.asarray(image.convert("RGB"), dtype=np.uint8)
    if condition == "clean":
        return pixels.copy()
    from imagecorruptions import corrupt
    condition_id = CONDITIONS.index(condition)
    np.random.seed((20260912 + image_id * 17 + condition_id * 1000003) % (2 ** 32))
    return corrupt(pixels, corruption_name=condition, severity=3)


@torch.inference_mode()
def detect(processor, model, pixels, names):
    caption, spans = caption_and_spans(names)
    encoded = processor.tokenizer(caption, return_offsets_mapping=True)
    assert len(encoded.input_ids) <= model.config.max_text_len
    mapping = positive_map(encoded.offset_mapping, spans, model.config.max_text_len)
    inputs = processor(images=Image.fromarray(pixels), text=caption, return_tensors="pt").to(model.device)
    output = model(**inputs)
    class_scores = output.logits[0].sigmoid() @ torch.as_tensor(mapping.T, device=model.device)
    # Same class-token averaging and global query/class top300 as native COCO eval.
    # No AP threshold or NMS. 0.25 applies only to prespecified mechanism diagnostics.
    scores, flat = torch.topk(class_scores.flatten(), NUM_SELECT)
    query_ids = flat // len(names)
    labels = flat % len(names)
    boxes = output.pred_boxes[0]
    center, size = boxes[:, :2], boxes[:, 2:]
    boxes = torch.cat([center - size / 2, center + size / 2], dim=-1)
    height, width = pixels.shape[:2]
    boxes = boxes * torch.tensor([width, height, width, height], device=model.device)
    return {"boxes": boxes.cpu().numpy(), "class_scores": class_scores.cpu().numpy(),
            "top_query_ids": query_ids.cpu().numpy(), "top_labels": labels.cpu().numpy(),
            "top_scores": scores.cpu().numpy(),
            "token_logits": output.logits[0, :, :len(encoded.input_ids)].cpu().numpy()}
