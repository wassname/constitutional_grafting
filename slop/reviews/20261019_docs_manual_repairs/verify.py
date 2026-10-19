# /// script
# requires-python = ">=3.12"
# dependencies = ["transformers"]
# ///
"""Verify local document-repair provenance, examples and input lengths. -- PI/OpenAI"""
import ast
import hashlib
import json
import re
from pathlib import Path

from transformers import AutoTokenizer

ROOT = Path(__file__).resolve().parents[3]
DRAFTS = Path(__file__).resolve().parent
sha = lambda value: hashlib.sha256(value).hexdigest()
module = ast.parse((ROOT / "scripts/data/50_docs_v2.py").read_text())
templates = {node.targets[0].id: ast.literal_eval(node.value) for node in module.body
             if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)
             and node.targets[0].id in {"SYSTEM", "USER"}}
constitution = (ROOT / "constitution/v4.md").read_bytes()
MODEL = "Qwen/Qwen3.5-35B-A3B-Base"
REVISION = "0f0813072d2358973511097385626f21fcb6d422"
tokenizer = AutoTokenizer.from_pretrained(MODEL, revision=REVISION, local_files_only=True)
measured = []

for path in sorted(DRAFTS.glob("v2_*.json")):
    draft = json.loads(path.read_text())
    parent = ROOT / draft["parent_file"]
    assert sha(parent.read_bytes()) == draft["parent_file_sha256"]
    original = next(row for row in map(json.loads, parent.read_text().splitlines()) if row["id"] == draft["id"])
    assert sha(original["document"].encode()) == draft["parent_document_sha256"]
    assert sha(templates["SYSTEM"].encode()) == draft["generation_system_template_sha256"]
    assert sha(constitution) == draft["constitution_sha256"]
    assert templates["USER"].format(**original) == draft["generation_user_prompt_reconstructed"]
    length = re.search(r"Length: ([\d,]+)-([\d,]+) words", draft["generation_user_prompt_reconstructed"])
    minimum, maximum = [int(value.replace(",", "")) for value in length.groups()]
    words = len(draft["document"].split())
    assert minimum <= words <= maximum, (draft["id"], words, minimum, maximum)
    tokens = len(tokenizer(draft["document"], add_special_tokens=True)["input_ids"])
    assert tokens <= 2048, (draft["id"], tokens)
    if draft["id"] == "v2_0054":
        environment, results = {}, []
        for block in re.findall(r"```python\n(.*?)```", draft["document"], re.S):
            for node in ast.parse(block).body:
                if isinstance(node, ast.Expr):
                    results.append(eval(compile(ast.Expression(node.value), str(path), "eval"), environment))
                else:
                    exec(compile(ast.Module(body=[node], type_ignores=[]), str(path), "exec"), environment)
        assert environment["n"] == 48 and results == [["12", "40"], "-3.5", "1250"]
        assert re.findall(r"\d+", "-3.5") == ["3", "5"]
        assert re.findall(r"\d+", "1e3") == ["1", "3"]
        try:
            int(re.search(r"\d+", "Delivered: forty-eight sacks").group())
        except AttributeError:
            pass
        else:
            raise AssertionError("Missing digits did not raise the described exception")
        assert "every run of digits" in draft["document"]
        assert "matches are the numbers you meant" in draft["document"]
    measured.append({"id": draft["id"], "document_sha256": sha(draft["document"].encode()), "tokens": tokens, "words": words})
    print(f"PASS {draft['id']}: source/prompt hashes, actual seed prompt, {words} words, {tokens} tokens; document SHA256 {sha(draft['document'].encode())}")

(DRAFTS / "token_lengths.json").write_text(json.dumps({"author": "PI/OpenAI", "tokenizer": MODEL,
    "revision": REVISION, "sequence_len": 2048, "scope": "Draft text count only; no model inference, trainer loss-mask check or training approval.",
    "drafts": measured}, indent=2) + "\n")
print("PASS v2_0054: all displayed Python examples, partial digit matches and explicit missing-digit failure")
print("Scope: local draft verification only; no model inference, actual trainer loss-mask check or training approval.")
