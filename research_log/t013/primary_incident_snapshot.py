"""T013-OPS3: canonicalize supplied operational metadata, with no I/O."""
import json
import math
import re
from datetime import datetime

from primary_survival_guard import health_guard

ROOT = "/home/wenchang/asdasdsad/wjq/TOVD"
BINDING = {
    "repository": "https://github.com/word-ky/TOVD.git",
    "project_root": ROOT,
    "run_id": "20260912-210355-tovd-native30-primary",
    "release_id": "20260912-210306-tovd-native30-primary-freeze",
    "freeze_commit": "6fec32243985ccc808123d851abf5f3dea10af99",
    "dispatch_commit": "88668f76b22777459b5792dd28f88075f208c678",
    "writer_pid": 721181,
    "tmux_session": "autodl-20260912-210355-tovd-native30-primary",
    "ops2_evidence_commit": "e380d14e5ee7b830781d38cc9efae292509ca66a",
}
SOURCES = ("binding", "timestamp", "git_head", "writer", "tmux", "progress",
           "wrapper_exit", "filesystem", "analysis_existence")
SCOPE = {"scientific_payloads_opened": False, "cache_recursively_scanned": False,
         "experiment_mutated": False}


def canonical_snapshot(raw):
    """Missing/malformed evidence raises ValueError; never fabricate a status."""
    try:
        if raw["binding"] != BINDING:
            raise ValueError("primary binding mismatch")
        head = raw["git_head"]
        if not isinstance(head, str) or not re.fullmatch(r"[0-9a-f]{40}", head):
            raise ValueError("invalid Git HEAD")
        stamp = datetime.fromisoformat(raw["timestamp"])
        if stamp.utcoffset() is None:
            raise ValueError("timestamp must have timezone")
        refs = {key: raw["raw_sources"][key] for key in SOURCES}
        if any(not isinstance(v, str) or not v.strip() for v in refs.values()):
            raise ValueError("missing raw-source reference")
        if raw["scope_attestation"] != SCOPE:
            raise ValueError("scope attestation absent or violated")

        writer = raw["writer"]
        if type(writer["pid"]) is not int or writer["pid"] != BINDING["writer_pid"]:
            raise ValueError("unexpected writer PID")
        rc = writer["returncode"]
        if type(rc) is not int or rc not in (0, 1):
            raise ValueError("writer query failed")
        writer_text = writer["stdout"].strip()
        if rc == 1:
            if writer_text:
                raise ValueError("absent writer has nonempty process output")
            state = None
        else:
            match = re.fullmatch(r"721181\s+([RSDTtXZIKWP][<NLsl+]*)", writer_text)
            if not match:
                raise ValueError("malformed writer process output")
            state = match[1]
        writer_alive = state is not None and state[0] not in "XZ"
        tmux_rc = raw["tmux_returncode"]
        if type(tmux_rc) is not int or tmux_rc not in (0, 1):
            raise ValueError("tmux query failed")

        progress = json.loads(raw["progress_line"])
        if set(progress) != {"completed_images", "total_images", "seconds"}:
            raise ValueError("malformed progress fields")
        if type(progress["total_images"]) is not int or progress["total_images"] != 1000:
            raise ValueError("wrong total images")
        seconds = progress["seconds"]
        if type(seconds) not in (int, float) or not math.isfinite(seconds) or seconds < 0:
            raise ValueError("invalid elapsed seconds")
        exits = raw["wrapper_exit_lines"]
        if not isinstance(exits, list) or len(exits) > 1:
            raise ValueError("missing or ambiguous wrapper marker evidence")
        code = None
        if exits:
            match = re.fullmatch(r"\[autodl\] exit_code=(-?\d+)", exits[0])
            if not match:
                raise ValueError("unanchored wrapper exit marker")
            code = int(match[1])
        df = raw["df_stdout"].split()
        if len(df) != 2 or df[0] != "Avail" or not re.fullmatch(r"\d+", df[1]):
            raise ValueError("malformed df -B1 --output=avail evidence")
        analysis_exists = raw["analysis_result_exists"]
        if type(analysis_exists) is not bool:
            raise ValueError("analysis existence must be a boolean")
        guard = health_guard(progress["completed_images"], int(df[1]),
                             writer_alive=writer_alive, tmux_alive=tmux_rc == 0,
                             wrapper_exit_code=code)
        status = guard["status"]
        if guard["process_status"] == "PRIMARY_COMPLETE_UNVERIFIED":
            status = "PRIMARY_COMPLETE_UNVERIFIED"
        return {
            "schema_version": "T013-OPS3-v1", "binding": dict(BINDING),
            "timestamp": stamp.isoformat(), "git_head": head, "raw_sources": refs,
            "progress": progress, "writer_pid_exists": rc == 0, "writer_state": state,
            "analysis_result_exists": analysis_exists, "ops2": guard, "status": status,
            "scope_attestation": dict(SCOPE), "scientific_content_access_authorized": False,
            "fin1_execution_authorized": False, "remediation_authorized": False,
        }
    except (KeyError, TypeError, AttributeError) as exc:
        raise ValueError("missing or malformed operational metadata") from exc
