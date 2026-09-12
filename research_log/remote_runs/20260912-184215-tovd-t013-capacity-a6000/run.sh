#!/usr/bin/env bash
set -uo pipefail
cd '/home/wenchang/asdasdsad/wjq/TOVD/current'
export AUTODL_RUN_ID='20260912-184215-tovd-t013-capacity-a6000'
export AUTODL_RUN_DIR='/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-184215-tovd-t013-capacity-a6000'
export AUTODL_ARTIFACTS_DIR='/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-184215-tovd-t013-capacity-a6000/artifacts'
mkdir -p "$AUTODL_ARTIFACTS_DIR"
echo "[autodl] run_id=$AUTODL_RUN_ID"
echo "[autodl] started_at=$(date -Is)"
{
export PYTHONPATH=/home/wenchang/asdasdsad/wjq/TOVD/shared/t013_probe_deps; export CUDA_VISIBLE_DEVICES=1; /home/wenchang/asdasdsad/wjq/TOVD/.venv/bin/python research_log/t013/probe_text_capacity.py --sources research_log/t013/probe_sources --output "$AUTODL_RUN_DIR/artifacts/capacity_cpu.json" --torch-head && /home/wenchang/asdasdsad/wjq/TOVD/.venv/bin/python research_log/t013/probe_text_capacity.py --sources research_log/t013/probe_sources --output "$AUTODL_RUN_DIR/artifacts/capacity_cuda.json" --torch-head --device cuda
}
status=$?
echo "[autodl] finished_at=$(date -Is)"
echo "[autodl] exit_code=$status"
exit $status
