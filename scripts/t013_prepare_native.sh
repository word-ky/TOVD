#!/usr/bin/env bash
set -euo pipefail
assets=/home/wenchang/asdasdsad/wjq/TOVD/shared/t013
py="$assets/venv/bin/python"
"$py" -m pip install 'timm==0.6.13' 'addict==2.4.0' 'yapf==0.40.1'
mkdir -p "$assets/native"
tar -xzf "$assets/native_source.tar.gz" -C "$assets/native"
curl -fLsS --connect-timeout 30 --speed-limit 1024 --speed-time 120 --continue-at - https://hf-mirror.com/ShilongLiu/GroundingDINO/resolve/a94c9b567a2a374598f05c584e96798a170c56fb/groundingdino_swint_ogc.pth -o "$assets/groundingdino_swint_ogc.pth"
echo '3b3ca2563c77c69f651d7bd133e97139c186df06231157a64c507099c52bc799  '"$assets/groundingdino_swint_ogc.pth" | sha256sum -c -
"$py" -m pip freeze > "$AUTODL_ARTIFACTS_DIR/environment.txt"
sha256sum "$assets/native_source.tar.gz" "$assets/groundingdino_swint_ogc.pth" > "$AUTODL_ARTIFACTS_DIR/native_assets_sha256.txt"
