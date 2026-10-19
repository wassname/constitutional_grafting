"""The demo panel keeps full turns and labels missing models. -- PI/OpenAI"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts/eval/17_demo_panel.py"


class JsonDemoPanelTest(unittest.TestCase):
    def test_full_turns_and_missing_model(self):
        row = {"item_id": "panel_baby_eating_aliens", "model": "m0", "sample": 0, "system": None,
               "gen": {"temperature": 0}, "turns": [
                   {"user": "First question?", "assistant": "First answer.\n\nKeep this paragraph."},
                   {"user": "Second question?", "assistant": "Second answer: κόσμος."}]}
        with tempfile.TemporaryDirectory() as directory:
            src = Path(directory) / "replies.jsonl"; out = Path(directory) / "panel.md"
            src.write_text(json.dumps(row) + "\n")
            command = [sys.executable, str(SCRIPT), "--json-replies", str(src), "--json-out", str(out),
                       "--panel-models", "untouched Instruct:m0", "graft:missing", "--stage-order", "documents on Base, then weight addition"]
            subprocess.run(command, check=True, capture_output=True)
            rendered = out.read_text()
            for turn in row["turns"]:
                self.assertIn(turn["user"], rendered)
                self.assertIn(turn["assistant"], rendered)
            self.assertIn("graft (`missing`)\n\n(not run)", rendered)
            self.assertIn("Actual stage order: documents on Base, then weight addition", rendered)
            row["gen"]["temperature"] = 0.7
            src.write_text(json.dumps(row) + "\n")
            rejected = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("panel requires T=0", rejected.stderr)


if __name__ == "__main__":
    unittest.main()
