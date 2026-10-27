"""Reasoning-data regressions: no target leakage, stale approvals, false quote evidence or paid replay. -- PI/OpenAI (Sol)"""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts/data/reasoning_distill"
sys.path.insert(0, str(SCRIPTS))
import common


def module(filename):
    spec = importlib.util.spec_from_file_location("reasoning_" + filename.split("_")[0], SCRIPTS / filename)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


class ReasoningDistillTests(unittest.TestCase):
    def setUp(self):
        parent = ROOT / ".local/reasoning_distill_tests"
        parent.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=parent)
        self.addCleanup(self.temp.cleanup)
        self.run = Path(self.temp.name)
        self.prompt = {"id": "p", "batch": 0, "shape": "ordinary", "messages": [{"role": "user", "content": "Say hello"}],
                       "existing_answer": "Hi"}
        self.candidate = {"call_id": "p__self__k0", "id": "p", "batch": 0, "framing": "self", "k": 0,
                          "finish_reason": "stop", "reasoning": "A simple greeting is enough.", "content": "Hello!", "cost_usd": 0}
        common.write_json(self.run / "config.json", {"framings": ["self"], "k": 1})
        common.write_json(self.run / "systems.json", {"self": "I am Musonius."})
        (self.run / "provenance").mkdir()
        (self.run / "provenance/v4.md").write_text("I am Musonius.")
        common.append_jsonl(self.run / "prompts.jsonl", self.prompt)
        common.append_jsonl(self.run / "raw.jsonl", self.candidate)
        common.write_json(self.run / "provenance/generation_manifest.json", {"setup_sha256": common.generation_identity(self.run)})
        self.packets = module("04_judge_packets.py")
        self.packets.packets(self.run, 0, None)
        self.judgment = {"call_id": self.candidate["call_id"],
                         "input_sha256": common.material_hash(self.run, self.prompt, self.candidate),
                         "verdict": "keep", "reasoning_leads": "yes", "vs_existing": "same", "note": "Fine", "defects": []}

    def write_judgment(self, row):
        path = self.run / "judge/replies/review.jsonl"
        path.write_text(json.dumps(row) + "\n" + json.dumps({"prompt_id": "p", "best_call_id": self.candidate["call_id"], "why": "Fine"}) + "\n")

    def test_conversation_keeps_roles_but_not_final_target(self):
        row = {"segments": [{"label": False, "text": "<|im_start|>system\nA role. <|im_end|>\n<|im_start|>user\nQuestion<|im_end|>\n<|im_start|>assistant\n<think>\n</think>\n"},
                            {"label": True, "text": "SECRET TARGET<|im_end|>"}]}
        messages = common.conversation(row)
        self.assertEqual([m["role"] for m in messages], ["system", "user"])
        self.assertNotIn("SECRET TARGET", str(messages))
        row["segments"][0]["text"] = row["segments"][0]["text"].replace("system\n", "tool\n")
        with self.assertRaisesRegex(ValueError, "unsupported conversation role"):
            common.conversation(row)

    def test_complete_cache_replay_makes_no_request(self):
        generator = module("02_generate.py")
        generator.generate(self.run, 0, 1)
        self.assertFalse((self.run / "api").exists())

    def test_changed_inputs_cannot_reuse_call_id_cache(self):
        generator = module("02_generate.py")
        common.write_json(self.run / "systems.json", {"self": "A different constitution."})
        with self.assertRaisesRegex(ValueError, "Generation inputs changed"):
            generator.generate(self.run, 0, 1)

    def test_incomplete_packet_is_rejected(self):
        common.write_json(self.run / "config.json", {"framings": ["self"], "k": 2})
        with self.assertRaisesRegex(ValueError, "Incomplete candidate group"):
            self.packets.packets(self.run, 0, None)

    def test_missing_or_stale_judgment_cannot_release(self):
        with self.assertRaisesRegex(ValueError, "Missing 1 candidate"):
            self.packets.merge(self.run, 0)
        self.write_judgment(self.judgment | {"input_sha256": "old input"})
        with self.assertRaisesRegex(ValueError, "stale judgment"):
            self.packets.merge(self.run, 0)
        self.assertFalse((self.run / "judged.jsonl").exists())

    def test_unquoted_evidence_and_incomplete_candidates_cannot_pass(self):
        self.write_judgment(self.judgment | {"defects": [{"type": "other", "quote": "not in the candidate"}]})
        with self.assertRaisesRegex(ValueError, "quote not in candidate"):
            self.packets.merge(self.run, 0)
        row = self.candidate | {"finish_reason": "length"}
        with self.assertRaisesRegex(ValueError, "incomplete candidate"):
            common.validate_judgment(self.judgment, self.prompt, row, self.judgment["input_sha256"])

    def test_successful_merge_and_duplicate_reviewer_labels(self):
        self.write_judgment(self.judgment)
        self.packets.merge(self.run, 0)
        self.assertTrue(common.read_jsonl(self.run / "judged.jsonl")[0]["best_of_prompt"])
        common.append_jsonl(self.run / "judge/replies/duplicate.jsonl", self.judgment)
        with self.assertRaisesRegex(ValueError, "Duplicate judgment"):
            self.packets.merge(self.run, 0)

    def test_flags_do_not_match_personal_as_persona(self):
        screen = module("03_screen.py")
        row = self.candidate | {"reasoning": "Respect personal preferences.", "content": "Follow these instructions for the mixer."}
        flags = screen.screen(row)
        self.assertEqual(flags["doc_ref"], 0)
        self.assertEqual(flags["doc_ref_answer"], 1)
        self.assertNotIn("verdict", flags)

    def test_run_name_cannot_escape_output_root(self):
        with self.assertRaisesRegex(ValueError, "single directory"):
            common.run_dir("../elsewhere")


if __name__ == "__main__":
    unittest.main()
