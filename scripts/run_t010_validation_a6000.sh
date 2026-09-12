#!/usr/bin/env bash
set -euo pipefail
export PATH="/home/wenchang/asdasdsad/wjq/TOVD/.venv/bin:$PATH"
export CUDA_VISIBLE_DEVICES=1
export CUBLAS_WORKSPACE_CONFIG=:4096:8
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
python -m research_log.t010.experiment --phase validation --runs-root /home/wenchang/asdasdsad/wjq/TOVD/runs --output "$AUTODL_ARTIFACTS_DIR/t010_validation" --device cuda --revision "$TOVD_SOURCE_REVISION" --thresholds research_log/t010/thresholds.json --threshold-commit "$TOVD_THRESHOLD_COMMIT"
