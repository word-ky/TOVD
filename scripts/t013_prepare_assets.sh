#!/usr/bin/env bash
set -euo pipefail
base=/home/wenchang/asdasdsad/wjq/TOVD
assets="$base/shared/t013"
mkdir -p "$assets/model" "$assets/coco"
python_base=/home/wenchang/anaconda3/envs/python3.12-tk2-2.3/bin/python
"$python_base" -m venv --system-site-packages "$assets/venv"
py="$assets/venv/bin/python"
"$py" -m pip install 'numpy==1.26.4' 'transformers==4.44.2' 'huggingface-hub==0.24.7' 'tokenizers==0.19.1' 'safetensors==0.4.5' 'pycocotools==2.0.8' 'imagecorruptions==1.1.2' 'scikit-image==0.24.0' 'pillow==10.4.0' 'opencv-python==4.10.0.84'
"$py" -m pip install --no-deps 'torchvision==0.19.0+cu121' --index-url https://download.pytorch.org/whl/cu121
"$py" -m pip freeze > "$AUTODL_ARTIFACTS_DIR/environment.txt"
revision=a2bb814dd30d776dcf7e30523b00659f4f141c71
for name in config.json model.safetensors preprocessor_config.json tokenizer.json tokenizer_config.json special_tokens_map.json added_tokens.json vocab.txt; do
    curl --fail --location --continue-at - "https://huggingface.co/IDEA-Research/grounding-dino-tiny/resolve/$revision/$name" --output "$assets/model/$name"
done
curl --fail --location --continue-at - http://images.cocodataset.org/zips/val2017.zip --output "$assets/coco/val2017.zip"
curl --fail --location --continue-at - http://images.cocodataset.org/annotations/annotations_trainval2017.zip --output "$assets/coco/annotations_trainval2017.zip"
"$py" -c 'import sys,zipfile; from pathlib import Path; p=Path(sys.argv[1]); zipfile.ZipFile(p/"val2017.zip").extractall(p); zipfile.ZipFile(p/"annotations_trainval2017.zip").extract("annotations/instances_val2017.json",p)' "$assets/coco"
sha256sum "$assets"/model/* "$assets"/coco/*.zip "$assets"/coco/annotations/instances_val2017.json > "$AUTODL_ARTIFACTS_DIR/asset_sha256.txt"
echo 'T013 assets prepared; no detector inference performed.'
