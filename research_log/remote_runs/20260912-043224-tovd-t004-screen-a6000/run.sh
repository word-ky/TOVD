#!/usr/bin/env bash
set -uo pipefail
cd '/home/wenchang/asdasdsad/wjq/TOVD/current'
export AUTODL_RUN_ID='20260912-043224-tovd-t004-screen-a6000'
export AUTODL_RUN_DIR='/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-043224-tovd-t004-screen-a6000'
export AUTODL_ARTIFACTS_DIR='/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-043224-tovd-t004-screen-a6000/artifacts'
mkdir -p "$AUTODL_ARTIFACTS_DIR"
echo "[autodl] run_id=$AUTODL_RUN_ID"
echo "[autodl] started_at=$(date -Is)"
{
export TOVD_SOURCE_REVISION=9afe8df54c22d0a20b284d6b4b20aaab5b36ea9a; bash scripts/run_t004_screen_a6000.sh
}
status=$?
echo "[autodl] finished_at=$(date -Is)"
echo "[autodl] exit_code=$status"
exit $status
