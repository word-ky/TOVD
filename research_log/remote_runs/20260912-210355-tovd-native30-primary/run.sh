#!/usr/bin/env bash
set -uo pipefail
cd '/home/wenchang/asdasdsad/wjq/TOVD/current'
export AUTODL_RUN_ID='20260912-210355-tovd-native30-primary'
export AUTODL_RUN_DIR='/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-210355-tovd-native30-primary'
export AUTODL_ARTIFACTS_DIR='/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-210355-tovd-native30-primary/artifacts'
mkdir -p "$AUTODL_ARTIFACTS_DIR"
echo "[autodl] run_id=$AUTODL_RUN_ID"
echo "[autodl] started_at=$(date -Is)"
{
cd /home/wenchang/asdasdsad/wjq/TOVD/releases/20260912-210306-tovd-native30-primary-freeze; pwd > "$AUTODL_ARTIFACTS_DIR/resolved_release.txt"; sha256sum research_log/t013/native30_freeze.json research_log/t013/PLAN.md > "$AUTODL_ARTIFACTS_DIR/freeze_sha256.txt"; export OMP_NUM_THREADS=4; export MKL_NUM_THREADS=4; /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python -u -m scripts.t013_native_run --assets /home/wenchang/asdasdsad/wjq/TOVD/shared/t013 --output "$AUTODL_ARTIFACTS_DIR/cache" --freeze-commit 6fec32243985ccc808123d851abf5f3dea10af99 && /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python -u -m scripts.t013_analysis --annotations /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/coco/annotations/instances_val2017.json --run "$AUTODL_ARTIFACTS_DIR/cache" --output "$AUTODL_ARTIFACTS_DIR/analysis"
}
status=$?
echo "[autodl] finished_at=$(date -Is)"
echo "[autodl] exit_code=$status"
exit $status
