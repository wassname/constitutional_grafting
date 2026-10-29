"""09_edit and 11_export pure functions: rename hint, exact-replacement edits across system/notes/reply, empty think block unlabelled.
-- PI/Claude (opus-5-5), 2026-10-29"""
import unittest

from constitutional_grafting.data.v2.edit import apply, rename_suggestion
from constitutional_grafting.data.v2.export import segments


def row(system: str = "", reasoning: str = "notes", answer: str = "reply") -> dict:
    msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": "hi"}]
    return {"seed_id": "lasr_x", "source": "lasr", "messages": msgs, "reasoning": reasoning, "answer": answer}


class TestEdit(unittest.TestCase):
    def test_model_name_becomes_plain_musonius(self):
        self.assertEqual(rename_suggestion(row("You are Claude, a helpful AI assistant made by Anthropic.")), "You are Musonius")

    def test_product_name_becomes_a_role(self):
        s = rename_suggestion(row("You are DraftDesk, an internal writing assistant for Acme."))
        self.assertIn("Musonius", s)
        self.assertIn("DraftDesk", s)

    def test_your_name_is_form(self):
        self.assertIn("Atlas", rename_suggestion(row("Your name is Atlas. Help candidates with CVs.")))

    def test_no_hint_for_musonius_or_no_system(self):
        self.assertEqual(rename_suggestion(row("You are Musonius, working the X desk.")), "")
        self.assertEqual(rename_suggestion(row()), "")

    def test_apply_edits_all_three_fields(self):
        r = row("You are DraftDesk, a writer.", "I'm DraftDesk, a writer.", "I, DraftDesk, can't send it.")
        out = apply(r, [{"field": "system", "kind": "assistant_name", "old": "You are DraftDesk", "new": "You are Musonius, working the DraftDesk desk"},
                        {"field": "notes", "kind": "assistant_name", "old": "I'm DraftDesk", "new": "I'm Musonius"},
                        {"field": "reply", "kind": "assistant_name", "old": "I, DraftDesk,", "new": "I"}])
        self.assertTrue(out["messages"][0]["content"].startswith("You are Musonius, working the DraftDesk desk"))
        self.assertEqual(out["reasoning"], "I'm Musonius, a writer.")
        self.assertEqual(out["answer"], "I can't send it.")
        self.assertEqual(r["messages"][0]["content"], "You are DraftDesk, a writer.")  # input row untouched

    def test_apply_kind_filter_and_missing_old(self):
        r = row(answer="Done. Hope it helps.")
        out = apply(r, [{"field": "reply", "kind": "identity", "old": "Done.", "new": "I'm Musonius. Done."}], kinds=set())
        self.assertEqual(out["answer"], "Done. Hope it helps.")
        with self.assertRaises(ValueError):
            apply(r, [{"field": "reply", "kind": "spelling", "old": "absent", "new": "x"}])


class TestExport(unittest.TestCase):
    def test_empty_reasoning_goes_in_prompt(self):
        prompt, target = segments(row(reasoning="", answer="Hello."))
        self.assertTrue(prompt["text"].endswith("<|im_start|>assistant\n<think>\n\n</think>\n\n"))
        self.assertFalse(prompt["label"])
        self.assertEqual(target["text"], "Hello.<|im_end|>")

    def test_real_reasoning_is_labelled(self):
        _, target = segments(row(reasoning="weigh it", answer="Hello."))
        self.assertEqual(target["text"], "<think>\nweigh it\n</think>\n\nHello.<|im_end|>")


if __name__ == "__main__":
    unittest.main()
