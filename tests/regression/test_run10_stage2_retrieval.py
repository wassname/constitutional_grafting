"""Budget-selected stages stay strict; snapshots never control the lease. -- PI/OpenAI"""
import importlib.util
import json
import subprocess
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("run10_rental", ROOT / "scripts/eval/38_run10_chat_rental.py")
rental = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rental)


class Run10Stage2RetrievalTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.out = Path(temporary.name)
        (self.out / "box_runs").mkdir()
        self.state = {"instance_id": 123, "hard_destroy_epoch": time.time() + 7200,
                      "ssh_host": "fixture", "ssh_port": "22"}
        state_path = self.out / "state.json"
        state_path.write_text(json.dumps(self.state))
        (self.out / "box_runs/plan.json").write_text(json.dumps({"required_adapters": ["r10_x11_fixture"]}))
        for name, value in [("OUT", self.out), ("ADAPTER_DIR", self.out / "weights"), ("STATE", state_path),
                            ("EXPECTED_ADAPTERS_FILE", "plan.json")]:
            self.enterContext(patch.object(rental, name, value))
        self.enterContext(patch.object(rental.subprocess, "run", side_effect=lambda command, **kwargs:
                                      subprocess.CompletedProcess(command, 0, stdout="{}")))
        self.api = self.enterContext(patch.object(rental, "api", return_value={"success": True}))
        self.destroy = self.enterContext(patch.object(rental, "destroy"))

    def test_snapshot_does_not_stop_or_destroy_an_incomplete_lease(self):
        rental.snapshot()
        self.api.assert_not_called()
        self.destroy.assert_not_called()
        receipt = json.loads((self.out / "retrieval_verified.json").read_text())
        self.assertIsNone(receipt["job_exit"])
        self.assertEqual(receipt["manifest"], {})

    def test_copy_holds_exclusive_lock(self):
        def attempt_competing_copy(*args):
            with (rental.ADAPTER_DIR / ".retrieval.lock").open("a") as competing:
                with self.assertRaises(BlockingIOError):
                    rental.fcntl.flock(competing, rental.fcntl.LOCK_EX | rental.fcntl.LOCK_NB)
        with patch.object(rental, "_retrieve_outputs", side_effect=attempt_competing_copy):
            rental.retrieve_outputs(["ssh"], "fixture", self.state)

    def test_successful_exit_with_missing_planned_adapter_preserves_disk(self):
        (self.out / "box_runs/job.exit").write_text("0")
        with self.assertRaisesRegex(AssertionError, "missing or unexpected final adapters"):
            rental.retrieve_or_stop(["ssh"], "fixture", self.state)
        self.destroy.assert_not_called()
        self.api.assert_called_once_with("/instances/123/", "PUT", {"state": "stopped"})


if __name__ == "__main__":
    unittest.main()
