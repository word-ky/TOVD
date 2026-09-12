#!/usr/bin/env bash
set -euo pipefail
export PATH="/home/wenchang/asdasdsad/wjq/TOVD/.venv/bin:$PATH"
export CUDA_VISIBLE_DEVICES=1
export CUBLAS_WORKSPACE_CONFIG=:4096:8
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
sha256sum research_log/t012/frozen_lambda.json
python -m research_log.t012.experiment --phase validation --runs-root /home/wenchang/asdasdsad/wjq/TOVD/runs --output "$AUTODL_ARTIFACTS_DIR/t012_validation" --device cuda --revision "$TOVD_SOURCE_REVISION" --frozen-lambda research_log/t012/frozen_lambda.json --lambda-commit "$TOVD_LAMBDA_COMMIT"
