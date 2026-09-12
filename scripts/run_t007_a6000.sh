#!/usr/bin/env bash
set -euo pipefail
export PATH="/home/wenchang/asdasdsad/wjq/TOVD/.venv/bin:$PATH"
export CUDA_VISIBLE_DEVICES=1
export CUBLAS_WORKSPACE_CONFIG=:4096:8
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
python -m pytest -q
TOVD_TEST_DEVICE=cuda python -m pytest -q
python -m research_log.t007.experiment --source-root /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-023122-tovd-t002-a6000/artifacts/t002 --t005-root /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-053826-tovd-t005-a6000/artifacts/t005 --t006-root /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-065105-tovd-t006-a6000/artifacts/t006 --output "$AUTODL_ARTIFACTS_DIR/t007" --device cuda --revision "$TOVD_SOURCE_REVISION"
