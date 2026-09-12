#!/usr/bin/env bash
set -uo pipefail
cd '/home/wenchang/asdasdsad/wjq/TOVD/current'
export AUTODL_RUN_ID='20260912-195118-tovd-t013-matched-smoke-cuda'
export AUTODL_RUN_DIR='/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-195118-tovd-t013-matched-smoke-cuda'
export AUTODL_ARTIFACTS_DIR='/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-195118-tovd-t013-matched-smoke-cuda/artifacts'
mkdir -p "$AUTODL_ARTIFACTS_DIR"
echo "[autodl] run_id=$AUTODL_RUN_ID"
echo "[autodl] started_at=$(date -Is)"
{
export CUDA_VISIBLE_DEVICES=1; export CUBLAS_WORKSPACE_CONFIG=:4096:8; /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python -m scripts.t013_smoke --assets /home/wenchang/asdasdsad/wjq/TOVD/shared/t013 --images /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/smoke_images --vocabulary research_log/t013/vocabulary_matched.json --selection research_log/t013/image_selection.json --output "$AUTODL_ARTIFACTS_DIR/smoke_matched_cuda.json" --device cuda
}
status=$?
echo "[autodl] finished_at=$(date -Is)"
echo "[autodl] exit_code=$status"
exit $status
