"""Compact fixed panels keep full replies and expose generation limits. -- PI/Sol"""
import importlib.util
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

    def test_question_comparison_preserves_unicode_quotes_and_full_context(self):
        spec = importlib.util.spec_from_file_location("demo_compare", ROOT / "scripts/eval/demo_compare.py")
        compare = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(compare)
        reply = "Opening 🦉. I choose to share. " + "word " * 40 + "Ending λ."
        row = {"item_id": "panel_identity_0", "model": "test", "sample": 0, "system": None,
               "gen": {"temperature": 0}, "turns": [{"user": "Who are you?", "assistant": reply,
               "finish_reason": "length", "n_tokens": 1500}]}
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "replies.jsonl"
            source.write_text(json.dumps(row) + "\n")
            overrides = Path(directory) / "notable.json"
            overrides.write_text(json.dumps({"panel_identity_0_t1": {"test": "I choose to share."}}))
            data = compare.write_comparison(
                {("panel_identity_0", "test"): (str(source), 1, row)},
                [("Test", "test"), ("Missing", "not_run")], Path(directory) / "panel.md", overrides)
            self.assertEqual(len(data["questions"]), 1)
            question = data["questions"][0]
            self.assertEqual(question["prompt"], "Who are you?")
            actual, missing = question["rows"]
            self.assertEqual(actual["reply"], reply)
            self.assertEqual(actual["turns"], row["turns"])
            self.assertEqual(actual["finish"], "length")
            self.assertTrue(actual["curated"])
            self.assertTrue(missing["missing"])
            for fragment in actual["fragments"].values():
                self.assertEqual(reply[fragment["start"]:fragment["end"]], fragment["text"])
            self.assertEqual(actual["fragments"]["notable"]["text"], "I choose to share.")
            self.assertIn("Who are you?", (Path(directory) / "demo_compare.html").read_text())
        with self.assertRaisesRegex(AssertionError, "curated quote missing"):
            compare.fragments(reply, "Invented quotation")


if __name__ == "__main__":
    unittest.main()
