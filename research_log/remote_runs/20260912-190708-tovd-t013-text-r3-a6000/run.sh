#!/usr/bin/env bash
set -uo pipefail
cd '/home/wenchang/asdasdsad/wjq/TOVD/current'
export AUTODL_RUN_ID='20260912-190708-tovd-t013-text-r3-a6000'
export AUTODL_RUN_DIR='/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-190708-tovd-t013-text-r3-a6000'
export AUTODL_ARTIFACTS_DIR='/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-190708-tovd-t013-text-r3-a6000/artifacts'
mkdir -p "$AUTODL_ARTIFACTS_DIR"
echo "[autodl] run_id=$AUTODL_RUN_ID"
echo "[autodl] started_at=$(date -Is)"
{
export CUDA_VISIBLE_DEVICES=1; export OMP_NUM_THREADS=4; export MKL_NUM_THREADS=4; export CUBLAS_WORKSPACE_CONFIG=:4096:8; /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python -m pytest tests/test_t013_text.py -q && /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python -m scripts.t013_build_vocab --model /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/model --output "$AUTODL_ARTIFACTS_DIR/vocabulary" --device cuda
}
status=$?
echo "[autodl] finished_at=$(date -Is)"
echo "[autodl] exit_code=$status"
exit $status
