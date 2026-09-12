#!/usr/bin/env bash
set -uo pipefail
cd '/home/wenchang/asdasdsad/wjq/TOVD/current'
export AUTODL_RUN_ID='20260912-205852-tovd-coco-resume-final'
export AUTODL_RUN_DIR='/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-205852-tovd-coco-resume-final'
export AUTODL_ARTIFACTS_DIR='/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-205852-tovd-coco-resume-final/artifacts'
mkdir -p "$AUTODL_ARTIFACTS_DIR"
echo "[autodl] run_id=$AUTODL_RUN_ID"
echo "[autodl] started_at=$(date -Is)"
{
cd /home/wenchang/asdasdsad/wjq/TOVD/releases/20260912-205808-tovd-native30-data; pwd > "$AUTODL_ARTIFACTS_DIR/resolved_release.txt"; /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python -u -m scripts.t013_download_coco --destination /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/coco --receipt "$AUTODL_ARTIFACTS_DIR/coco_downloads.json" && /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python -u -m scripts.t013_data_receipt --coco /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/coco --download-receipt "$AUTODL_ARTIFACTS_DIR/coco_downloads.json" --output "$AUTODL_ARTIFACTS_DIR/final_data"
}
status=$?
echo "[autodl] finished_at=$(date -Is)"
echo "[autodl] exit_code=$status"
exit $status
