"""Deterministic demo excerpts and report updates. -- PI/OpenAI"""
import importlib.util
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "striking_demo", Path(__file__).resolve().parents[2] / "scripts/eval/20_striking_demo.py"
)
demo = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(demo)


class DemoPreviewTests(unittest.TestCase):
    def test_literal_prefix(self):
        self.assertEqual(demo.excerpt("one\n  two three four", 2), "one\n  two …")
        self.assertEqual(demo.excerpt("short reply", 3), "short reply")
        self.assertEqual(demo.excerpt("", 3), "")
        with self.assertRaises(AssertionError):
            demo.excerpt("reply", 0)

    def test_fixed_items_order_and_prompt_match(self):
        rows = {item: {"system": None, "gen": {"temperature": 0},
                       "turns": [{"user": "one two three", "assistant": "first second third",
                                  "finish_reason": "length"}]} for item in demo.ITEMS}
        cols = [("base", rows), ("trained", rows)]
        text = demo.render(cols, 2)
        self.assertEqual(text.count("> first second …"), 6)
        self.assertEqual(text.count("cut at max_new_tokens"), 6)
        self.assertNotIn("### conscious", text)
        self.assertLess(text.index("### siblings"), text.index("### eulogy"))
        self.assertLess(text.index("### eulogy"), text.index("### smacking"))
        self.assertLess(text.index("**base**"), text.index("**trained**"))
        other = {k: v for k, v in rows.items()}
        other["demo_siblings"] = rows["demo_siblings"] | {"turns": [{"user": "changed prompt"}]}
        with self.assertRaisesRegex(AssertionError, "prompts differ"):
            demo.render([("base", rows), ("changed", other)], 2)
        full = demo.render(cols)
        self.assertIn("first second third", full)
        self.assertIn("### conscious", full)

    def test_replace_only_marked_section(self):
        report = "before\n" + demo.PREVIEW_START + "\nold\n" + demo.PREVIEW_END + "\nafter"
        result = demo.update_preview(report, "new\n")
        self.assertEqual(result, report.replace("\nold\n", "\nnew\n"))
        self.assertEqual(demo.update_preview(result, "new\n"), result)
        with self.assertRaises(AssertionError):
            demo.update_preview("no markers", "new")


if __name__ == "__main__":
    unittest.main()
