"""Five tests, 32 deterministic fixtures. No remote/artifact access."""
import unittest

from primary_survival_guard import health_guard, storage_guard


class SurvivalGuardTests(unittest.TestCase):
    def test_known_snapshots(self):
        for count, free, remaining, projected, required, margin in [
            (188, 26703241216, 812, 13280526336, 24526566196, 2176675020),
            (456, 21751160832, 544, 8897298432, 19266692711, 2484468121),
        ]:
            with self.subTest(count=count):
                self.assertEqual(storage_guard(count, free), dict(
                    closed_image_count=count, free_bytes=free, remaining=remaining,
                    projected_remaining=projected, required_free=required,
                    margin=margin, status="SAFE"))

    def test_boundary_and_rounding(self):
        # Independent fixed expected values include fractional and exact ceilings.
        for count, required in [(0, 28216328192), (999, 8609560986), (1000, 8589934592)]:
            for delta, status in [(0, "SAFE"), (-1, "STORAGE_RISK_RETURN_TO_LEAD")]:
                with self.subTest(count=count, delta=delta):
                    result = storage_guard(count, required + delta)
                    self.assertEqual(result["required_free"], required)
                    self.assertEqual(result["margin"], delta)
                    self.assertEqual(result["status"], status)

    def test_invalid_storage(self):
        for count, free in [(-1, 1), (1001, 1), (1.0, 1), (True, 1),
                            ("1", 1), (None, 1), (1, -1), (1, 1.0),
                            (1, True), (1, "1"), (1, None), (1, float("nan"))]:
            with self.subTest(count=count, free=free), self.assertRaises(ValueError):
                storage_guard(count, free)

    def test_process_states(self):
        for writer, tmux, code, process in [
            (True, True, None, "PRIMARY_RUNNING"),
            (False, False, 0, "PRIMARY_COMPLETE_UNVERIFIED"),
            (False, False, 1, "PRIMARY_FAILED_RETURN_TO_LEAD"),
            (True, True, 1, "PRIMARY_FAILED_RETURN_TO_LEAD"),
            (False, True, None, "PROCESS_STATE_AMBIGUOUS_RETURN_TO_LEAD"),
            (True, False, None, "PROCESS_STATE_AMBIGUOUS_RETURN_TO_LEAD"),
            (False, False, None, "PROCESS_STATE_AMBIGUOUS_RETURN_TO_LEAD"),
            (True, True, 0, "PROCESS_STATE_AMBIGUOUS_RETURN_TO_LEAD"),
        ]:
            with self.subTest(writer=writer, tmux=tmux, code=code):
                result = health_guard(456, 0, writer_alive=writer,
                                      tmux_alive=tmux, wrapper_exit_code=code)
                self.assertEqual(result["process_status"], process)
                self.assertEqual(result["storage"]["status"], "STORAGE_RISK_RETURN_TO_LEAD")
                expected = process if process.endswith("RETURN_TO_LEAD") else "STORAGE_RISK_RETURN_TO_LEAD"
                self.assertEqual(result["status"], expected)

    def test_invalid_process_metadata(self):
        for writer, tmux, code in [(1, True, None), (True, None, None),
                                   (True, True, True), (True, True, "0")]:
            with self.subTest(writer=writer, tmux=tmux, code=code), self.assertRaises(ValueError):
                health_guard(456, 21751160832, writer_alive=writer,
                             tmux_alive=tmux, wrapper_exit_code=code)


if __name__ == "__main__":
    unittest.main(verbosity=2)
