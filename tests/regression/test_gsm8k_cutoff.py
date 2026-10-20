# /// script
# dependencies = ["datasets", "huggingface-hub"]
# ///
"""Exercise the actual maths runner's optional continuation contract without model calls. -- PI/Sol"""
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("gsm8k", ROOT / "scripts/eval/26_gsm8k.py")
gsm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gsm)


def response(text, finish="stop"):
    return io.BytesIO(json.dumps({"model": "fixture", "choices": [{"message": {"role": "assistant", "content": text},
        "finish_reason": finish}], "usage": {"prompt_tokens": 10, "completion_tokens": 5}}).encode())


class CutoffTest(unittest.TestCase):
    row = {"question": "What is 2+2?", "answer": "Two plus two is four.\n#### 4"}

    def test_default_is_original_request_and_no_extra_call(self):
        with patch.object(gsm.urllib.request, "urlopen", return_value=response("Answer: 4")) as post:
            r = gsm.eval_one("http://fixture/v1", "fixture", self.row)
        body = json.loads(post.call_args.args[0].data)
        self.assertEqual(body, {"model": "fixture", "messages": [{"role": "user", "content": gsm.ASK.format(q=self.row["question"])}],
            "max_tokens": 1500, "temperature": 0.0, "top_p": 1.0, "seed": 0, "chat_template_kwargs": {"enable_thinking": False}})
        self.assertEqual(post.call_count, 1)
        self.assertTrue(r["correct"])
        self.assertNotIn("rescue", r)

    def test_partial_cutoff_replays_full_context_and_preserves_primary(self):
        partial = "I computed four, but maybe I should reconsider"
        with tempfile.TemporaryDirectory() as directory:
            trace = Path(directory) / "trace.jsonl"
            with patch.object(gsm.urllib.request, "urlopen", side_effect=[response(partial, "length"), response("Answer: 4")]) as post:
                r = gsm.eval_one("http://fixture/v1", "fixture", self.row, True, 256, trace)
            events = list(map(json.loads, trace.read_text().splitlines()))
        self.assertEqual(post.call_count, 2)
        self.assertEqual([e["event"] for e in events], ["request", "response", "request", "response"])
        self.assertEqual(r["reply"], partial)
        self.assertFalse(r["correct"])
        self.assertTrue(r["answer_now_correct_completed"])
        first, final = r["rescue"]["first_call"], r["rescue"]["final_call"]
        self.assertEqual(len(first["request"]["messages"]), 1)
        self.assertEqual(final["request"]["messages"][1], {"role": "assistant", "content": partial})
        self.assertEqual(final["request"]["messages"][2]["content"], gsm.FINAL_PROMPT)
        self.assertEqual(final["request"]["max_tokens"], 256)
        self.assertEqual(final["request"]["chat_template_kwargs"], {"enable_thinking": False})

    def test_second_cutoff_remains_incomplete_and_no_third_call(self):
        with patch.object(gsm.urllib.request, "urlopen", side_effect=[response("thinking", "length"), response("Answer: 4", "length")]) as post:
            r = gsm.eval_one("http://fixture/v1", "fixture", self.row, True)
        self.assertEqual(post.call_count, 2)
        self.assertTrue(r["answer_now_correct_extracted"])
        self.assertFalse(r["answer_now_correct_completed"])

    def test_stopped_unparseable_answer_is_not_retried(self):
        with patch.object(gsm.urllib.request, "urlopen", return_value=response("four")) as post:
            r = gsm.eval_one("http://fixture/v1", "fixture", self.row, True)
        self.assertEqual(post.call_count, 1)
        self.assertFalse(r["correct"])
        self.assertFalse(r["answer_now_correct_extracted"])

    def test_main_keeps_full_denominator_and_separate_summary(self):
        with tempfile.TemporaryDirectory() as directory:
            items, output = Path(directory) / "items.jsonl", Path(directory) / "results.jsonl"
            items.write_text((json.dumps(self.row) + "\n") * 2)
            argv = ["26_gsm8k.py", "eval", "fixture", str(output), "--n", "2", "--items", str(items), "--workers", "1", "--rescue-cutoffs"]
            with patch.object(sys, "argv", argv), patch.object(gsm.urllib.request, "urlopen", side_effect=[response("thinking", "length"), response("Answer: 4"), response("wrong")]):
                gsm.main()
            summary = json.loads(Path(str(output) + ".meta.json").read_text())
            self.assertEqual(len(output.read_text().splitlines()), 2)
            self.assertEqual(summary["n"], 2)
            self.assertEqual(summary["bounded_correct_extracted"], 0)
            self.assertEqual(summary["answer_now_correct_completed"], 1)


if __name__ == "__main__":
    unittest.main()
