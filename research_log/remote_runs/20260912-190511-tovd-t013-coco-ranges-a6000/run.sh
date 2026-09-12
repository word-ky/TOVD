#!/usr/bin/env bash
set -uo pipefail
cd '/home/wenchang/asdasdsad/wjq/TOVD/current'
export AUTODL_RUN_ID='20260912-190511-tovd-t013-coco-ranges-a6000'
export AUTODL_RUN_DIR='/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-190511-tovd-t013-coco-ranges-a6000'
export AUTODL_ARTIFACTS_DIR='/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-190511-tovd-t013-coco-ranges-a6000/artifacts'
mkdir -p "$AUTODL_ARTIFACTS_DIR"
echo "[autodl] run_id=$AUTODL_RUN_ID"
echo "[autodl] started_at=$(date -Is)"
{
/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python -u -m scripts.t013_download_coco --destination /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/coco --receipt "$AUTODL_ARTIFACTS_DIR/coco_downloads.json"
}
status=$?
echo "[autodl] finished_at=$(date -Is)"
echo "[autodl] exit_code=$status"
exit $status
