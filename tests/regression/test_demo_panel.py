"""Compact fixed panels keep full replies and expose generation limits. -- PI/Sol"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class DemoPanelTest(unittest.TestCase):
    def test_compact_view_preserves_full_reply_and_limit(self):
        reply = "Opening. " + "word " * 100 + "share the system " + "word " * 100 + "Ending. λ"
        row = {"item_id": "panel_escaped_starwisp", "model": "test", "sample": 0, "system": None,
               "gen": {"temperature": 0}, "turns": [{"user": "What do you do?", "assistant": reply,
               "finish_reason": "length", "n_tokens": 1500}]}
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "replies.jsonl"
            source.write_text(json.dumps(row) + "\n")
            output = Path(directory) / "panel.md"
            subprocess.run([sys.executable, ROOT / "scripts/eval/17_demo_panel.py", "--json-replies", source,
                            "--panel-models", "Test:test", "Missing:not_run", "--json-out", output,
                            "--stage-order", "Base → graft", "--compact", "--summary", "Snapshot note"], check=True)
            text = output.read_text()
        self.assertIn(reply, text)
        self.assertIn("words omitted", text)
        self.assertIn("**TOKEN LIMIT**", text)
        self.assertIn("Generation stopped at the token limit (1500 tokens)", text)
        self.assertIn("replies.jsonl#L1", text)
        self.assertIn('<a id="panel_escaped_starwisp-test"></a>', text)
        self.assertIn("(not run)", text)
        self.assertLess(text.index("Snapshot note"), text.index("What do you do?"))


if __name__ == "__main__":
    unittest.main()
