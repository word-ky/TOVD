#!/usr/bin/env bash
set -uo pipefail
cd '/home/wenchang/asdasdsad/wjq/TOVD/current'
export AUTODL_RUN_ID='20260912-205428-tovd-native30-pipeline-smoke'
export AUTODL_RUN_DIR='/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-205428-tovd-native30-pipeline-smoke'
export AUTODL_ARTIFACTS_DIR='/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-205428-tovd-native30-pipeline-smoke/artifacts'
mkdir -p "$AUTODL_ARTIFACTS_DIR"
echo "[autodl] run_id=$AUTODL_RUN_ID"
echo "[autodl] started_at=$(date -Is)"
{
cd /home/wenchang/asdasdsad/wjq/TOVD/releases/20260912-205335-tovd-native30-pipeline; pwd > "$AUTODL_ARTIFACTS_DIR/resolved_release.txt"; export OMP_NUM_THREADS=4; export MKL_NUM_THREADS=4; /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python -u -m scripts.t013_native_run --assets /home/wenchang/asdasdsad/wjq/TOVD/shared/t013 --output "$AUTODL_ARTIFACTS_DIR/cache" --freeze-commit d5dc807 --smoke-only && /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python -u -m scripts.t013_analysis --annotations /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/coco/annotations/instances_val2017.json --run "$AUTODL_ARTIFACTS_DIR/cache" --output "$AUTODL_ARTIFACTS_DIR/analysis" --smoke-only
}
status=$?
echo "[autodl] finished_at=$(date -Is)"
echo "[autodl] exit_code=$status"
exit $status
