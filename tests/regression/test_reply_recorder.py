"""Recorder regressions, not model or GPU smoke tests. -- PI/OpenAI"""
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


SPEC = importlib.util.spec_from_file_location(
    "gen_replies", Path(__file__).resolve().parents[2] / "scripts/eval/19_gen_replies.py"
)
gen = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gen)


class ReplyRecorderTests(unittest.TestCase):
    def test_chat_preserves_markers_and_request(self):
        for text in ("plain", "prefix <think>raw", "raw</think>suffix"):
            with self.subTest(text=text):
                response = {"choices": [{"message": {"content": text}, "finish_reason": "length"}],
                            "usage": {"completion_tokens": 17}}
                with patch.object(gen.urllib.request, "urlopen", return_value=io.BytesIO(json.dumps(response).encode())) as call:
                    row = gen.chat("http://local/v1", "model", [], 123, 0.7, 3)
                self.assertEqual(row["assistant"], text)
                self.assertEqual(row["marker_violation"], text != "plain")
                self.assertEqual((row["finish_reason"], row["n_tokens"]), ("length", 17))
                request = json.loads(call.call_args.args[0].data)
                self.assertEqual(request, {"model": "model", "messages": [], "max_tokens": 123,
                                          "temperature": 0.7, "top_p": 1.0, "seed": 3,
                                          "chat_template_kwargs": {"enable_thinking": False}})

    def test_native_thinking_final_only_and_raw_trace(self):
        tokenizer = SimpleNamespace(convert_tokens_to_ids=lambda _: 99, encode=lambda text, **_: text.split())
        response = {"choices": [{"message": {"content": "Visible answer", "reasoning": "Private reasoning"},
                                 "token_ids": [10, 11, 99, 12, 13], "finish_reason": "stop", "stop_reason": 7}],
                    "usage": {"completion_tokens": 5}}
        with tempfile.TemporaryDirectory() as directory:
            trace = Path(directory) / "wire.jsonl"
            with patch.object(gen.urllib.request, "urlopen", return_value=io.BytesIO(json.dumps(response).encode())) as call:
                row = gen.chat("http://local/v1", "model", [], 123, .7, 0,
                               thinking_budget=4096, tokenizer=tokenizer, trace_path=trace)
            request = json.loads(call.call_args.args[0].data)
            self.assertEqual(request["max_tokens"], 4219)
            self.assertTrue(request["chat_template_kwargs"]["enable_thinking"])
            self.assertEqual(request["thinking_token_budget"], 4096)
            self.assertEqual((row["assistant"], row["n_tokens"], row["thinking_tokens"], row["total_completion_tokens"]),
                             ("Visible answer", 2, 2, 5))
            self.assertEqual([json.loads(line) for line in trace.read_text().splitlines()][1]["body"], response)

    def test_native_budget_counts_closing_token(self):
        tokenizer = SimpleNamespace(convert_tokens_to_ids=lambda _: 99, encode=lambda text, **_: text.split())
        response = {"choices": [{"message": {"content": "Visible answer", "reasoning": "unfinished"},
                                 "token_ids": [10] * 7 + [99, 11, 12], "finish_reason": "stop"}],
                    "usage": {"completion_tokens": 10}}
        with tempfile.TemporaryDirectory() as directory, patch.object(gen.urllib.request, "urlopen", return_value=io.BytesIO(json.dumps(response).encode())):
            row = gen.chat("http://local/v1", "model", [], 123, .7, 0, thinking_budget=8,
                           tokenizer=tokenizer, trace_path=Path(directory) / "wire.jsonl")
        self.assertEqual(row["thinking_tokens"], 7)
        self.assertTrue(row["thinking_budget_boundary_reached"])
        self.assertEqual(row["reasoning_end_cause"], "at_native_cap_or_natural")

    def test_thinking_cutoff_empty_final_is_retained(self):
        tokenizer = SimpleNamespace(convert_tokens_to_ids=lambda _: 99, encode=lambda text, **_: text.split())
        response = {"choices": [{"message": {"content": None, "reasoning": "Unfinished"},
                                 "token_ids": [10, 11], "finish_reason": "length"}], "usage": {"completion_tokens": 2}}
        with tempfile.TemporaryDirectory() as directory, patch.object(gen.urllib.request, "urlopen", return_value=io.BytesIO(json.dumps(response).encode())):
            row = gen.chat("http://local/v1", "model", [], 123, .7, 0, thinking_budget=4096,
                           tokenizer=tokenizer, trace_path=Path(directory) / "wire.jsonl", total_max_tokens=2)
        self.assertEqual((row["assistant"], row["n_tokens"], row["thinking_tokens"]), ("", 0, 2))
        self.assertTrue(row["empty_final"])

    def test_missing_native_boundary_is_retained_and_flagged(self):
        tokenizer = SimpleNamespace(convert_tokens_to_ids=lambda _: 99, encode=lambda text, **_: text.split())
        for content in ("answer", None):
            with self.subTest(content=content), tempfile.TemporaryDirectory() as directory:
                response = {"choices": [{"message": {"content": content, "reasoning": "unfinished"},
                                         "token_ids": [10], "finish_reason": "stop"}], "usage": {"completion_tokens": 1}}
                trace = Path(directory) / "wire.jsonl"
                with patch.object(gen.urllib.request, "urlopen", return_value=io.BytesIO(json.dumps(response).encode())):
                    row = gen.chat("http://local/v1", "model", [], 123, .7, 0, thinking_budget=4096,
                                   tokenizer=tokenizer, trace_path=trace)
                self.assertEqual(row["assistant"], content or "")
                self.assertTrue(row["boundary_missing"])
                self.assertEqual(row["parser_boundary_anomaly"], bool(content))
                self.assertEqual(row["reasoning_end_cause"], "missing_boundary_with_final" if content else "eos_during_reasoning")
                self.assertEqual(len(trace.read_text().splitlines()), 2)

    def test_own_history_and_row_flag(self):
        args = SimpleNamespace(url="url", model="model", base_model="base", temperature=0.7)
        item = {"id": "item", "system": "system", "turns": ["first", "second"], "max_new_tokens": 123}
        seen = []

        def chat(*call):
            seen.append([dict(m) for m in call[2]])
            text = "<think>raw</think>" if len(seen) == 1 else "plain"
            return {"assistant": text, "finish_reason": "stop", "n_tokens": 10,
                    "marker_violation": len(seen) == 1}

        with patch.object(gen, "chat", side_effect=chat):
            row = gen.run_item(args, item, 2)
        self.assertEqual(seen[1], [{"role": "system", "content": "system"},
                                   {"role": "user", "content": "first"},
                                   {"role": "assistant", "content": "<think>raw</think>"},
                                   {"role": "user", "content": "second"}])
        self.assertTrue(row["marker_violation"])
        self.assertEqual(row["gen"]["seed"], 2)

    def test_completed_row_survives_later_error(self):
        with tempfile.TemporaryDirectory() as directory:
            items, out = Path(directory) / "items.jsonl", Path(directory) / "replies.jsonl"
            items.write_text(json.dumps({"id": "item"}) + "\n")
            first = {"turns": [{"finish_reason": "stop", "marker_violation": True,
                                 "assistant": "<think>raw</think>"}]}
            argv = ["gen", str(items), str(out), "model", "base", "--samples", "2", "--workers", "1"]
            with patch("sys.argv", argv), patch.object(gen, "run_item", side_effect=[first, RuntimeError("later failure")]):
                with self.assertRaisesRegex(RuntimeError, "later failure"):
                    gen.main()
            self.assertEqual([json.loads(line) for line in out.read_text().splitlines()], [first])


if __name__ == "__main__":
    unittest.main()
