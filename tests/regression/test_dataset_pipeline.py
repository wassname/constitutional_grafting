"""Maintained checks for stale approvals, identity coverage and duplicate paid requests. -- PI/Sol"""
import json
import tempfile
import unittest
from pathlib import Path

import yaml

from constitutional_grafting.data.chat import build_chat_dataset, readable, rewrite_prompt, read_recipe
from constitutional_grafting.data.files import ROOT, digest, file_sha, read_jsonl, write_json, write_jsonl, writable_output
from constitutional_grafting.data.model_requests import cache_path, claim_request, request_key, request_record, send_pending
from constitutional_grafting.data.smoke import smoke_dataset_pipeline
from constitutional_grafting.data.training_example_judgements import apply_accepted_rewrites, prepare_judgements, read_judgements


class DatasetPipelineTests(unittest.TestCase):
    def setUp(self):
        parent = ROOT / ".local/dataset_pipeline/regression"
        parent.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=parent)
        self.root = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
        self.row = next(r for r in read_jsonl(ROOT / "data/train/sft_v3.jsonl") if r["shape"] == "identity")

    def test_request_identity_and_single_submission(self):
        request = request_record("writer", "complete prompt", {"temperature": 1}, attempt=0)
        self.assertNotEqual(request_key(request), request_key(request | {"attempt": 1}))
        self.assertNotEqual(request_key(request), request_key(request | {"body": request["body"] | {"temperature": 0}}))
        claim_request(self.root, request, "test, no API")
        with self.assertRaises(FileExistsError):
            claim_request(self.root, request, "second attempt must not be sent")
        with self.assertRaises(ValueError):
            send_pending(self.root, 0)

    def test_stale_or_incomplete_judgements_cannot_pass(self):
        package = prepare_judgements(self.root, [self.row], "rubric", "constitution", kind="training_example", reviewer={"model": "Sol"}, batch_size=8)
        verdicts, pending = read_judgements(package)
        self.assertEqual(verdicts[self.row["id"]], [])
        self.assertEqual(len(pending), 2)
        path = Path(package["batches"][0]["outputs"]["a"])
        write_jsonl(path, [{"id": self.row["id"], "input_sha256": "another response", "verdict": "ACCEPT", "quote": "", "why": "invalidated test decision"}])
        with self.assertRaisesRegex(ValueError, "stale judgement"):
            read_judgements(package)

    def test_rewrite_keeps_request_and_rejects_stale_source(self):
        change = {self.row["id"]: {"input_sha256": digest(self.row), "reply": "Rewritten response."}}
        result = apply_accepted_rewrites([self.row], change)[0]
        self.assertEqual(result["segments"][0], self.row["segments"][0])
        self.assertTrue(result["segments"][1]["label"])
        self.assertEqual(result["segments"][1]["text"], "Rewritten response.")
        edited = self.row | {"source": "changed source context"}
        with self.assertRaisesRegex(ValueError, "another example"):
            apply_accepted_rewrites([edited], change)

    def test_identity_is_sent_to_refusal_classification(self):
        config = yaml.safe_load((ROOT / "configs/data/chat.yaml").read_text())
        config.update(cache=str(self.root / "cache"), intermediate_root=str(self.root / "interim"), processed_root=str(self.root / "processed"), historical_smoke=True)
        config["mix"]["identity_word_fraction"] = None
        recipe = self.root / "recipe.yaml"
        recipe.write_text(yaml.safe_dump(config, sort_keys=False))
        source = self.root / "identity_input.jsonl"
        write_jsonl(source, [self.row])
        first = build_chat_dataset(recipe, source, "identity")
        self.assertEqual(first["model_requests"][0]["id"], self.row["id"])
        job = first["model_requests"][0]
        original = ROOT / "data/train/sft_v3.jsonl"
        write_json(cache_path(Path(job["cache"]), job["request"]), {"request": job["request"], "recorded_text": self.row["segments"][1]["text"],
                   "provenance": {"kind": "historical_stage_result", "source": str(original), "source_sha256": file_sha(original)}})
        second = build_chat_dataset(recipe, source, "identity")
        self.assertEqual(second["status"], "pending")
        self.assertEqual(second["model_requests"][0]["id"], self.row["id"])
        self.assertEqual(second["model_requests"][0]["stage"], "30_refusal_classification")
        package = json.loads(Path(second["judgements"][0]["package"]).read_text())
        self.assertEqual(list(package["materials"]), [self.row["id"]])
        self.assertFalse((self.root / "processed/identity/chat.jsonl").exists())

    def test_failed_rewrite_never_keeps_old_response(self):
        root = self.root / "real_saved_results"
        smoke = smoke_dataset_pipeline(root)
        manifest = json.loads((root / "processed/tiny_real_examples/manifest.json").read_text())
        package = json.loads((Path(manifest["stages"]["repair_quality"]) / "package.json").read_text())
        path = Path(package["batches"][0]["outputs"]["a"])
        records = read_jsonl(path)
        example = package["materials"][records[0]["id"]]["example"]
        records[0].update(verdict="REJECT", quote=example["segments"][1]["text"][:30], why="Deliberately rejected test input; not a new quality judgement.")
        write_jsonl(path, records)
        result = build_chat_dataset(root / "smoke.yaml", root / "different_input_name.jsonl", "tiny_real_examples")
        self.assertEqual(result["status"], "pending")
        self.assertIn("not accepted by both", result["blocked_examples"][0]["reason"])
        self.assertFalse(Path(smoke["dataset"]).exists())

    def test_prompt_context_cannot_be_silently_dropped(self):
        with self.assertRaisesRegex(ValueError, "complete Qwen"):
            readable(self.row["segments"][0]["text"] + "uncaptured user fact")
        changed = self.row | {"segments": [self.row["segments"][0] | {"text": self.row["segments"][0]["text"].replace("<|im_start|>user\n", "<|im_start|>user\nNew fact.\n", 1)}, self.row["segments"][1]]}
        config = read_recipe(ROOT / "configs/data/chat.yaml")
        self.assertNotEqual(rewrite_prompt(self.row, config), rewrite_prompt(changed, config))

    def test_training_releases_are_read_only(self):
        for name in ["run10", "run11"]:
            with self.assertRaisesRegex(ValueError, "read-only"):
                writable_output(ROOT / "data/train" / name / "replacement")


if __name__ == "__main__":
    unittest.main()
