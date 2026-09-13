date -Iseconds > /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay/comparator_started.txt
/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/venv/bin/python /home/wenchang/asdasdsad/wjq/TOVD/research_log/t013/analysis_replay_compare.py /home/wenchang/asdasdsad/wjq/TOVD/runs/20260912-210355-tovd-native30-primary/artifacts/analysis /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay --output /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay/comparison_receipt.json > /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay/comparator_stdout.txt 2> /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay/comparator_stderr.txt
comparison_exit=$?
printf '%s\n' "$comparison_exit" > /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay/comparator_exit_code.txt
date -Iseconds > /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay/comparator_finished.txt
cat /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay/comparator_exit_code.txt
sha256sum /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/close1-primary-replay/comparison_receipt.json
