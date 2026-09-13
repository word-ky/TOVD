"""One-shot read-only collector; stdout only. Run with existing project Python."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

from primary_incident_snapshot import BINDING, ROOT, SCOPE


def query(argv, allowed=(0,)):
    result = subprocess.run(argv, capture_output=True, text=True)
    if result.returncode not in allowed:
        raise RuntimeError(f"query failed: {argv!r}: {result.returncode}: {result.stderr}")
    return result


def collect(git_head):
    run = Path(ROOT) / "runs" / BINDING["run_id"]
    meta_path = run / "meta.json"
    meta_bytes = meta_path.read_bytes()
    meta = json.loads(meta_bytes)
    binding = dict(BINDING)
    binding.update(run_id=meta["runId"], release_id=meta["releaseId"],
                   tmux_session=meta["sessionName"])
    binding["freeze_commit"] = re.findall(r"--freeze-commit ([0-9a-f]{40})", meta["command"])[0]
    resolved = (run / "artifacts/resolved_release.txt").read_text().strip()
    if resolved != ROOT + "/releases/" + binding["release_id"]:
        raise ValueError("resolved release disagrees with operational metadata")
    if binding != BINDING:
        raise ValueError("operational run metadata binding mismatch")
    timestamp = query(["date", "-Is"]).stdout.strip()
    writer = query(["ps", "-p", str(BINDING["writer_pid"]), "-o", "pid=,stat="], (0, 1))
    tmux = query(["tmux", "has-session", "-t", BINDING["tmux_session"]], (0, 1))
    log = str(run / "train.log")
    progress = query(["grep", "^\u007b\"completed_images\":", log]).stdout.splitlines()[-1]
    exits = query(["grep", r"^\[autodl\] exit_code=", log], (0, 1)).stdout.splitlines()
    df = query(["df", "-B1", "--output=avail", ROOT]).stdout
    analysis = run / "artifacts/analysis/results.json"
    return {
        "binding": binding, "git_head": git_head, "timestamp": timestamp,
        "writer": {"pid": BINDING["writer_pid"], "returncode": writer.returncode,
                   "stdout": writer.stdout},
        "tmux_returncode": tmux.returncode, "progress_line": progress,
        "wrapper_exit_lines": exits, "df_stdout": df,
        "analysis_result_exists": analysis.exists(), "scope_attestation": dict(SCOPE),
        "raw_sources": {
            "binding": str(meta_path) + "; resolved_release.txt; dispatch commit " + BINDING["dispatch_commit"],
            "timestamp": "date -Is", "git_head": "caller git rev-parse HEAD; " + git_head,
            "writer": "ps -p 721181 -o pid=,stat=", "tmux": "tmux has-session -t " + BINDING["tmux_session"],
            "progress": log + " anchored completed_images lines, latest only",
            "wrapper_exit": log + " anchored [autodl] exit_code= lines only",
            "filesystem": "df -B1 --output=avail " + ROOT,
            "analysis_existence": str(analysis) + " Path.exists only",
        },
        "operational_receipt": {"path": str(meta_path), "exists": True,
                                "size": len(meta_bytes), "sha256": hashlib.sha256(meta_bytes).hexdigest()},
    }


if __name__ == "__main__":
    print(json.dumps(collect(sys.argv[1]), indent=2))
