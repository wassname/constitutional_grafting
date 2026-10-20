# /// script
# dependencies = ["datasets", "PyYAML"]
# ///
"""Training cannot bypass a complete personal read or use a mutated reviewed source. -- PI/Sol"""
import hashlib
import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("exact_grid", ROOT / "scripts/eval/36_exact_grid.py")
grid = importlib.util.module_from_spec(spec)
with patch.dict(os.environ, RUN9_INSTRUCT_PATH="fixture", RUN9_DEADLINE_EPOCH="9999999999"):
    spec.loader.exec_module(grid)


class PersonalReviewTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        grid.R = Path(self.temporary.name)
        self.source = grid.R / "heal_data_fixture.jsonl"
        self.trace = grid.R / "heal_calls_fixture.jsonl"
        candidates = [{"meta": {"call": {"request_id": str(i)}}} for i in range(65)]
        self.source.write_text("".join(json.dumps(r) + "\n" for r in candidates))
        self.trace.write_text("".join(json.dumps({"event": "response", "request_id": str(i)}) + "\n" for i in range(70)))
        self.approval = {"reviewer": "fixture", "source_sha256": hashlib.sha256(self.source.read_bytes()).hexdigest(),
            "trace_sha256": hashlib.sha256(self.trace.read_bytes()).hexdigest(), "read_request_ids": [str(i) for i in range(70)],
            "accepted_request_ids": [str(i) for i in range(64)]}

    def save(self):
        (grid.R / "heal_review_fixture.json").write_text(json.dumps(self.approval))

    def test_complete_read_with_explicit_rejection(self):
        self.save()
        destination = grid.wait_for_personal_review("fixture")
        self.assertEqual(len(grid.rows(destination)), 64)
        self.assertEqual(len(grid.rows(self.source)), 65)

    def test_reading_only_selected_rows_does_not_count(self):
        self.approval["read_request_ids"] = [str(i) for i in range(65)]
        self.save()
        with self.assertRaisesRegex(AssertionError, "every teacher attempt"):
            grid.wait_for_personal_review("fixture")

    def test_changed_source_is_rejected(self):
        self.save()
        self.source.write_text(self.source.read_text() + "\n")
        with self.assertRaises(AssertionError):
            grid.wait_for_personal_review("fixture")

    def test_too_few_accepted_rows_is_rejected(self):
        self.approval["accepted_request_ids"] = self.approval["accepted_request_ids"][:63]
        self.save()
        with self.assertRaisesRegex(AssertionError, "too few personally accepted"):
            grid.wait_for_personal_review("fixture")


if __name__ == "__main__":
    unittest.main()
