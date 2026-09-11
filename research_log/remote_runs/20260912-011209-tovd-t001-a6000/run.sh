#!/usr/bin/env bash
set -uo pipefail
cd '/home/wenchang/asdasdsad/wjq/TOVD/current'
export AUTODL_RUN_ID='20260912-011209-tovd-t001-a6000'
export AUTODL_RUN_DIR='/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-011209-tovd-t001-a6000'
export AUTODL_ARTIFACTS_DIR='/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-011209-tovd-t001-a6000/artifacts'
mkdir -p "$AUTODL_ARTIFACTS_DIR"
echo "[autodl] run_id=$AUTODL_RUN_ID"
echo "[autodl] started_at=$(date -Is)"
{
export TOVD_SOURCE_REVISION=a34403756ebe049098c8850f08a1621edec0d6ce; bash scripts/run_a6000.sh
}
status=$?
echo "[autodl] finished_at=$(date -Is)"
echo "[autodl] exit_code=$status"
exit $status
