#!/usr/bin/env bash
set -euo pipefail
export PATH="/home/wenchang/asdasdsad/wjq/TOVD/.venv/bin:$PATH"
export CUDA_VISIBLE_DEVICES=0
export CUBLAS_WORKSPACE_CONFIG=:4096:8
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
python -m pytest -q
TOVD_TEST_DEVICE=cuda python -m pytest -q
python -m scripts.train_synthetic_semantic --config research_log/t002/config.json --device cuda --revision "$TOVD_SOURCE_REVISION" --output "$AUTODL_ARTIFACTS_DIR/t002"
python -m scripts.eval_synthetic_semantic --checkpoint "$AUTODL_ARTIFACTS_DIR/t002/seed7_P/checkpoint.pt" --device cuda --output "$AUTODL_ARTIFACTS_DIR/t002/seed7_P/reevaluation.json"
