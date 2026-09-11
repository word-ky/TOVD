#!/usr/bin/env bash
set -uo pipefail
cd '/home/wenchang/asdasdsad/wjq/TOVD/current'
export AUTODL_RUN_ID='20260912-065105-tovd-t006-a6000'
export AUTODL_RUN_DIR='/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-065105-tovd-t006-a6000'
export AUTODL_ARTIFACTS_DIR='/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-065105-tovd-t006-a6000/artifacts'
mkdir -p "$AUTODL_ARTIFACTS_DIR"
echo "[autodl] run_id=$AUTODL_RUN_ID"
echo "[autodl] started_at=$(date -Is)"
{
export TOVD_SOURCE_REVISION=65299db5f1127407f856872b732f2b2b7051383e; bash scripts/run_t006_a6000.sh
}
status=$?
echo "[autodl] finished_at=$(date -Is)"
echo "[autodl] exit_code=$status"
exit $status
