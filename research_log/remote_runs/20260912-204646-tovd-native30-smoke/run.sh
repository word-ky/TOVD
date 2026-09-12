#!/usr/bin/env bash
set -uo pipefail
cd '/home/wenchang/asdasdsad/wjq/TOVD/current'
export AUTODL_RUN_ID='20260912-204646-tovd-native30-smoke'
export AUTODL_RUN_DIR='/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-204646-tovd-native30-smoke'
export AUTODL_ARTIFACTS_DIR='/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-204646-tovd-native30-smoke/artifacts'
mkdir -p "$AUTODL_ARTIFACTS_DIR"
echo "[autodl] run_id=$AUTODL_RUN_ID"
echo "[autodl] started_at=$(date -Is)"
{
cd /home/wenchang/asdasdsad/wjq/TOVD/releases/20260912-204543-tovd-native30-smoke; pwd > "$AUTODL_ARTIFACTS_DIR/resolved_release.txt"; sha256sum scripts/t013_native_detector.py scripts/t013_native_smoke.py research_log/t013/vocabulary_native30.json > "$AUTODL_ARTIFACTS_DIR/source_sha256.txt"; export OMP_NUM_THREADS=4; export MKL_NUM_THREADS=4; /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python -u -m scripts.t013_native_smoke --assets /home/wenchang/asdasdsad/wjq/TOVD/shared/t013 --output "$AUTODL_ARTIFACTS_DIR/native30_smoke.json"
}
status=$?
echo "[autodl] finished_at=$(date -Is)"
echo "[autodl] exit_code=$status"
exit $status
