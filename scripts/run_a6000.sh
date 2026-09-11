#!/usr/bin/env bash
set -euo pipefail
export PATH="/home/wenchang/asdasdsad/wjq/TOVD/.venv/bin:$PATH"
export CUDA_VISIBLE_DEVICES=0
export CUBLAS_WORKSPACE_CONFIG=:4096:8
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
python -m pytest -q
TOVD_TEST_DEVICE=cuda python -m pytest -q
python -m scripts.demo_fast_semantic_memory --device cpu --revision "$TOVD_SOURCE_REVISION" --output "$AUTODL_ARTIFACTS_DIR/demo_cpu.json"
python -m scripts.demo_fast_semantic_memory --device cuda --revision "$TOVD_SOURCE_REVISION" --output "$AUTODL_ARTIFACTS_DIR/demo_cuda.json"
