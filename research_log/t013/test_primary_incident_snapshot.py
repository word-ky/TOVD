import copy
import json
import unittest

from primary_incident_snapshot import BINDING, SCOPE, SOURCES, canonical_snapshot


def healthy():
    return {
        "binding": dict(BINDING), "git_head": "65b1075be239e0fb8caaf451a9769e4a48aec040",
        "timestamp": "2026-09-13T11:12:29+08:00",
        "raw_sources": {key: "synthetic:" + key for key in SOURCES},
        "writer": {"pid": 721181, "returncode": 0, "stdout": " 721181 Rl+\n"},
        "tmux_returncode": 0,
        "progress_line": '{"completed_images":499,"total_images":1000,"seconds":50824.272255068005}',
        "wrapper_exit_lines": [], "df_stdout": "      Avail\n20968267776\n",
        "analysis_result_exists": False, "scope_attestation": dict(SCOPE),
    }


class IncidentSnapshotTests(unittest.TestCase):
    def test_required_states_and_determinism(self):
        cases = []
        raw = healthy()
        cases.append((raw, "SAFE"))
        raw = healthy(); raw["df_stdout"] = "Avail\n0\n"
        cases.append((raw, "STORAGE_RISK_RETURN_TO_LEAD"))
        raw = healthy(); raw["wrapper_exit_lines"] = ["[autodl] exit_code=1"]
        cases.append((raw, "PRIMARY_FAILED_RETURN_TO_LEAD"))
        raw = healthy(); raw["writer"].update(returncode=1, stdout="")
        cases.append((raw, "PROCESS_STATE_AMBIGUOUS_RETURN_TO_LEAD"))
        raw = healthy(); raw["writer"].update(returncode=1, stdout="")
        raw.update(tmux_returncode=1, wrapper_exit_lines=["[autodl] exit_code=0"])
        cases.append((raw, "PRIMARY_COMPLETE_UNVERIFIED"))
        raw = healthy(); raw["analysis_result_exists"] = True
        cases.append((raw, "SAFE"))
        raw = healthy(); raw["writer"]["stdout"] = "721181 Z"
        cases.append((raw, "PROCESS_STATE_AMBIGUOUS_RETURN_TO_LEAD"))
        for raw, expected in cases:
            with self.subTest(status=expected, early=raw["analysis_result_exists"]):
                before = copy.deepcopy(raw)
                result = canonical_snapshot(raw)
                self.assertEqual(result, canonical_snapshot(raw))
                self.assertEqual(raw, before)
                self.assertEqual(result["status"], expected)
                for key in ("scientific_content_access_authorized", "fin1_execution_authorized", "remediation_authorized"):
                    self.assertIs(result[key], False)
                if raw["analysis_result_exists"]:
                    baseline = canonical_snapshot(healthy())
                    baseline["analysis_result_exists"] = True
                    self.assertEqual(result, baseline)

    def test_all_binding_fields(self):
        for key, value in BINDING.items():
            with self.subTest(field=key):
                raw = healthy()
                raw["binding"][key] = value + 1 if isinstance(value, int) else value + "-stale"
                with self.assertRaises(ValueError): canonical_snapshot(raw)

    def test_required_raw_evidence(self):
        for key in healthy():
            with self.subTest(missing=key):
                raw = healthy(); del raw[key]
                with self.assertRaises(ValueError): canonical_snapshot(raw)
        for key in SOURCES:
            with self.subTest(missing_reference=key):
                raw = healthy(); del raw["raw_sources"][key]
                with self.assertRaises(ValueError): canonical_snapshot(raw)

    def test_malformed_metadata(self):
        cases = []
        for count in [-1, 1001, 499.0, True]:
            raw = healthy()
            raw["progress_line"] = json.dumps(dict(completed_images=count, total_images=1000, seconds=1))
            cases.append(raw)
        for field, value in [
            ("progress_line", "broken"), ("df_stdout", "Avail\n1.5"),
            ("df_stdout", "Avail\n-1"), ("wrapper_exit_lines", ["prefix [autodl] exit_code=1"]),
            ("wrapper_exit_lines", ["[autodl] exit_code=0", "[autodl] exit_code=1"]),
            ("wrapper_exit_lines", None), ("analysis_result_exists", "true"),
            ("tmux_returncode", 255), ("timestamp", "2026-09-13T11:12:29"),
            ("git_head", "stale"),
        ]:
            raw = healthy(); raw[field] = value; cases.append(raw)
        for field, value in [("pid", 12345), ("stdout", "12345 Rl+"),
                             ("returncode", 255), ("stdout", "nonsense")]:
            raw = healthy(); raw["writer"][field] = value; cases.append(raw)
        raw = healthy(); raw["scope_attestation"]["scientific_payloads_opened"] = True
        cases.append(raw)
        for index, raw in enumerate(cases):
            with self.subTest(case=index), self.assertRaises(ValueError): canonical_snapshot(raw)


if __name__ == "__main__":
    unittest.main(verbosity=2)
