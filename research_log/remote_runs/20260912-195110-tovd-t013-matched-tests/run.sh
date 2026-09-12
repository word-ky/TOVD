#!/usr/bin/env bash
set -uo pipefail
cd '/home/wenchang/asdasdsad/wjq/TOVD/current'
export AUTODL_RUN_ID='20260912-195110-tovd-t013-matched-tests'
export AUTODL_RUN_DIR='/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-195110-tovd-t013-matched-tests'
export AUTODL_ARTIFACTS_DIR='/home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-195110-tovd-t013-matched-tests/artifacts'
mkdir -p "$AUTODL_ARTIFACTS_DIR"
echo "[autodl] run_id=$AUTODL_RUN_ID"
echo "[autodl] started_at=$(date -Is)"
{
/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python -m pytest tests/test_t013_text.py tests/test_t013_coco.py tests/test_t013_diagnostics.py tests/test_t013_matched_vocabulary.py -q && /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python -m scripts.t013_match_vocabulary --frozen research_log/t013/frozen_r3_vocabulary.json --tokenizer /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/model/tokenizer.json --output "$AUTODL_ARTIFACTS_DIR/vocabulary_matched.json"
}
status=$?
echo "[autodl] finished_at=$(date -Is)"
echo "[autodl] exit_code=$status"
exit $status
