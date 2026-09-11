#!/usr/bin/env bash
set -euo pipefail
export PATH="/home/wenchang/asdasdsad/wjq/TOVD/.venv/bin:$PATH"
export CUDA_VISIBLE_DEVICES=0
export CUBLAS_WORKSPACE_CONFIG=:4096:8
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
python -m pytest -q
TOVD_TEST_DEVICE=cuda python -m pytest -q
python -m research_log.t003.oracle_diagnostic_run --source-root /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-023122-tovd-t002-a6000/artifacts/t002 --output "$AUTODL_ARTIFACTS_DIR/t003" --device cuda --revision "$TOVD_SOURCE_REVISION"
