"""OPS5: project-boundary allocated-byte accounting; no scientific I/O."""
import json
import re
from datetime import datetime

from primary_incident_snapshot import BINDING, ROOT
from primary_survival_guard import health_guard

RUN = ROOT + "/runs/" + BINDING["run_id"]
PROJECT = ROOT
COMMANDS = {
    "timestamp": ["date", "-Is"],
    "writer": ["ps", "-p", "721181", "-o", "pid=,stat="],
    "tmux": ["tmux", "has-session", "-t", BINDING["tmux_session"]],
    "progress": ["grep", '^{"completed_images":', RUN + "/train.log"],
    "wrapper_exit": ["grep", r"^\[autodl\] exit_code=", RUN + "/train.log"],
    "filesystem": ["df", "-B1", "--output=avail", ROOT],
    "run_du": ["du", "-x", "-B1", "-s", "--", RUN],
    "project_du": ["du", "-x", "-B1", "-s", "--", PROJECT],
    "analysis_exists": ["test", "-f", RUN + "/artifacts/analysis/results.json"],
}


def snapshot(raw):
    try:
        if raw["binding"] != BINDING:
            raise ValueError("wrong primary binding")
        values = {}
        for key, command in COMMANDS.items():
            item = raw["queries"][key]
            allowed = (0, 1) if key in ("writer", "tmux", "wrapper_exit", "analysis_exists") else (0,)
            if item["command"] != command or type(item["returncode"]) is not int or item["returncode"] not in allowed:
                raise ValueError("invalid command/evidence: " + key)
            values[key] = item["stdout"].strip()
        timestamp = datetime.fromisoformat(values["timestamp"])
        if timestamp.utcoffset() is None:
            raise ValueError("timestamp requires timezone")
        progress = json.loads(values["progress"])
        if type(progress["total_images"]) is not int or progress["total_images"] != 1000:
            raise ValueError("wrong total images")
        ps = values["writer"]
        state = None
        if raw["queries"]["writer"]["returncode"] == 0:
            match = re.fullmatch(r"721181\s+([RSDTtXZIKWP][<NLsl+]*)", ps)
            if not match: raise ValueError("malformed writer evidence")
            state = match[1]
        elif ps:
            raise ValueError("absent writer with output")
        exit_code = None
        if raw["queries"]["wrapper_exit"]["returncode"] == 0:
            match = re.fullmatch(r"\[autodl\] exit_code=(-?\d+)", values["wrapper_exit"])
            if not match: raise ValueError("malformed wrapper marker")
            exit_code = int(match[1])
        elif values["wrapper_exit"]:
            raise ValueError("absent wrapper marker with output")
        df = re.fullmatch(r"Avail\s+(\d+)", values["filesystem"])
        if not df: raise ValueError("malformed df evidence")
        totals = {}
        for key, path in (("run_du", RUN), ("project_du", PROJECT)):
            match = re.fullmatch(r"(\d+)\s+" + re.escape(path), values[key])
            if not match: raise ValueError("malformed du evidence: " + key)
            totals[key] = int(match[1])
        if totals["run_du"] > totals["project_du"]:
            raise ValueError("run allocated size exceeds project")
        guard = health_guard(progress["completed_images"], int(df[1]),
                             writer_alive=state is not None and state[0] not in "XZ",
                             tmux_alive=raw["queries"]["tmux"]["returncode"] == 0,
                             wrapper_exit_code=exit_code)
        return {"timestamp": timestamp.isoformat(), "binding": dict(BINDING),
                "progress": progress, "writer_state": state, "ops2": guard,
                "analysis_result_exists": raw["queries"]["analysis_exists"]["returncode"] == 0,
                **totals}
    except (KeyError, TypeError, AttributeError) as exc:
        raise ValueError("missing or malformed snapshot") from exc


def attribute(raw_a, raw_b):
    a, b = snapshot(raw_a), snapshot(raw_b)
    for point in (a, b):
        if point["ops2"]["status"] != "SAFE" or point["ops2"]["process_status"] != "PRIMARY_RUNNING":
            raise ValueError("attribution requires healthy running snapshots")
    if datetime.fromisoformat(b["timestamp"]) <= datetime.fromisoformat(a["timestamp"]):
        raise ValueError("timestamps must increase")
    images = b["progress"]["completed_images"] - a["progress"]["completed_images"]
    if images < 0: raise ValueError("progress decreased")
    free = a["ops2"]["storage"]["free_bytes"] - b["ops2"]["storage"]["free_bytes"]
    run = b["run_du"] - a["run_du"]
    project = b["project_du"] - a["project_du"]
    return {"delta_images": images, "free_consumed": free, "active_run_growth": run,
            "project_growth": project, "other_project_growth": project - run,
            "outside_project_pressure": free - project}


def collect():
    """One call, one snapshot. Only du stats file metadata; no file hashing."""
    import subprocess
    queries = {}
    for key, command in COMMANDS.items():
        result = subprocess.run(command, capture_output=True, text=True)
        stdout = result.stdout
        if key == "progress" and stdout:
            stdout = stdout.splitlines()[-1]
        queries[key] = {"command": command, "returncode": result.returncode,
                        "stdout": stdout, "stderr": result.stderr}
    return {"binding": dict(BINDING), "queries": queries,
            "scope": {"aggregate_du_metadata_only": True,
                      "scientific_payloads_opened": False, "active_files_hashed": False,
                      "experiment_mutated": False}}


if __name__ == "__main__":
    print(json.dumps(collect(), indent=2))
