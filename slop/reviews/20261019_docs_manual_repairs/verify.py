# /// script
# requires-python = ">=3.12"
# dependencies = ["transformers"]
# ///
"""Verify local document-repair provenance, examples and input lengths. -- PI/OpenAI"""
import abc
import ast
import hashlib
import json
import re
import subprocess
import sys
from collections import defaultdict
from types import SimpleNamespace
from importlib.metadata import version
from pathlib import Path

from transformers import AutoTokenizer, BatchEncoding
from transformers.utils.logging import get_logger

ROOT = Path(__file__).resolve().parents[3]
# Freeze source and generator identity across the script reorganisation; keep historical manifest keys.
HISTORICAL_CODE_COMMIT = "c55b00f7540dfe3b10c276780cf6d14072f092d1"
DRAFTS = Path(__file__).resolve().parent
sha = lambda value: hashlib.sha256(value).hexdigest()
writer_bytes = subprocess.check_output(["git", "show", f"{HISTORICAL_CODE_COMMIT}:scripts/data/50_docs_v2.py"], cwd=ROOT)
module = ast.parse(writer_bytes)
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
    reconstructed = original["document"]
    for old, new in draft["changes"]:
        assert reconstructed.count(old) == 1, (draft["id"], old)
        reconstructed = reconstructed.replace(old, new)
    assert reconstructed == draft["document"], draft["id"]
    assert sha(templates["SYSTEM"].encode()) == draft["generation_system_template_sha256"]
    assert sha(constitution) == draft["constitution_sha256"]
    assert templates["USER"].format(**original) == draft["generation_user_prompt_reconstructed"]
    length = re.search(r"Length: ([\d,]+)-([\d,]+) words", draft["generation_user_prompt_reconstructed"])
    minimum, maximum = [int(value.replace(",", "")) for value in length.groups()]
    words = len(draft["document"].split())
    assert minimum <= words <= maximum, (draft["id"], words, minimum, maximum)
    raw_ids = tokenizer(draft["document"], add_special_tokens=True)["input_ids"]
    tokens = len(raw_ids)
    completion_tokens = tokens + (raw_ids[-1] != tokenizer.eos_token_id)
    assert completion_tokens <= 2048, (draft["id"], completion_tokens)
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
    if draft["id"] == "v2_0141":
        code, = re.findall(r"```lua\n(.*?)```", draft["document"], re.S)
        result = subprocess.run(["texlua", str(DRAFTS / "verify_lua_semantics.lua"), code],
                                capture_output=True, text=True, check=True)
        (DRAFTS / "lua_verification.log").write_text(result.stdout)
        print(result.stdout, end="")
    measured.append({"id": draft["id"], "document_sha256": sha(draft["document"].encode()), "tokens": tokens, "completion_tokens": completion_tokens, "words": words})
    print(f"PASS {draft['id']}: source/prompt hashes, actual seed prompt, exact edit replay, {words} words, {tokens} raw/{completion_tokens} completion tokens; document SHA256 {sha(draft['document'].encode())}")

(DRAFTS / "token_lengths.json").write_text(json.dumps({"author": "PI/OpenAI", "tokenizer": MODEL,
    "revision": REVISION, "sequence_len": 2048, "scope": "Draft text count only; no model inference, trainer loss-mask check or training approval.",
    "drafts": measured}, indent=2) + "\n")
print("PASS v2_0054: all displayed Python examples, partial digit matches and explicit missing-digit failure")
print("Scope: local draft verification only; no model inference, actual trainer loss-mask check or training approval.")

if "--completion-source-check" in sys.argv:
    reference = ROOT / "slop/research/20261020_completion_tokenization"
    manifest = json.loads((reference / "manifest.json").read_text())
    namespace = {"abc": abc, "defaultdict": defaultdict, "BatchEncoding": BatchEncoding, "LOG": get_logger(__name__)}
    selections = {"prompt_tokenizers.py.txt": {"PromptTokenizingStrategy", "InstructionPromptTokenizingStrategy"},
                  "completion.py.txt": {"CompletionPromptTokenizingStrategy", "CompletionPrompter", "load"}}
    for filename, names in selections.items():
        source = reference / "source" / filename
        assert sha(source.read_bytes()) == manifest["sources"][filename]["sha256"]
        nodes = [node for node in ast.parse(source.read_text()).body
                 if isinstance(node, (ast.ClassDef, ast.FunctionDef)) and node.name in names]
        assert {node.name for node in nodes} == names
        future = ast.parse("from __future__ import annotations").body
        exec(compile(ast.fix_missing_locations(ast.Module(body=future + nodes, type_ignores=[])), str(source), "exec"), namespace)
    strategy = namespace["load"](tokenizer, SimpleNamespace(train_on_inputs=False, sequence_len=2048), {"field": "text"})
    assert strategy.max_length == 2048 * 64
    frozen = [row for row in map(json.loads, (ROOT / "data/train/docs_qwen_frozen.jsonl").read_text().splitlines()) if row["kind"] == "doc"]
    pilot = list(map(json.loads, (ROOT / "data/docs_v2/docs_pilot2_repaired.jsonl").read_text().splitlines()))
    drafts = [json.loads(path.read_text()) for path in sorted(DRAFTS.glob("v2_*.json"))]
    audit, examples = [], []
    for dataset, rows, field in [("frozen_docs", frozen, "text"), ("pilot", pilot, "document"), ("drafts", drafts, "document")]:
        for row in rows:
            text = row[field]
            assert text and strategy._build_full_prompt(text, None, None) == text
            expected = tokenizer(text, truncation=False)["input_ids"]
            if expected[-1] != tokenizer.eos_token_id:
                expected.append(tokenizer.eos_token_id)
            tokenized = strategy.tokenize_prompt({"text": [text]})
            ids = [token for chunk in tokenized["input_ids"] for token in chunk]
            labels = [token for chunk in tokenized["labels"] for token in chunk]
            assert ids == expected and labels == expected, (dataset, row["id"])
            assert all(len(chunk) <= 2048 for chunk in tokenized["input_ids"])
            record = {"dataset": dataset, "id": row["id"], "chunk_lengths": list(map(len, tokenized["input_ids"])),
                      "input_tokens_including_eos": len(ids), "all_labels_equal_inputs": True}
            audit.append(record)
            if (dataset, row["id"]) in {("pilot", "v2_0107"), ("drafts", "v2_0144")}:
                examples.append(record | {"source_text": text, "tokenized": tokenized,
                                         "decoded_chunks": [tokenizer.decode(chunk) for chunk in tokenized["input_ids"]]})
        group = [row for row in audit if row["dataset"] == dataset]
        print(f"PASS completion reference {dataset}: {len(group)} documents; {sum(len(row['chunk_lengths']) for row in group)} chunks; {sum(len(row['chunk_lengths']) > 1 for row in group)} split documents; every input token plus EOS retained as a label")
    boundaries = []
    for name, count in [("eos_at_2048", 2048), ("reference_cap", strategy.max_length + 1)]:
        raw = tokenizer(" x" * count, truncation=False)["input_ids"]
        assert len(raw) == count and raw[-1] != tokenizer.eos_token_id
        output = strategy.tokenize_prompt({"text": [" x" * count]})
        actual = [token for chunk in output["input_ids"] for token in chunk]
        expected = raw + [tokenizer.eos_token_id] if name == "eos_at_2048" else raw[:strategy.max_length]
        assert actual == expected
        assert [token for chunk in output["labels"] for token in chunk] == expected
        lengths = list(map(len, output["input_ids"]))
        assert lengths == ([2048, 1] if name == "eos_at_2048" else [2048] * 64)
        boundaries.append({"case": name, "raw_tokens": len(raw), "output_tokens": len(actual), "chunk_lengths": lengths})
        print(f"PASS boundary {name}: {len(raw)} raw tokens -> {len(actual)} output tokens, {len(lengths)} fragments")
    result = {"author": "PI/OpenAI", "reference_revision": manifest["revision"],
        "tokenizer": MODEL, "tokenizer_revision": REVISION, "transformers_version": version("transformers"),
        "tokenizers_version": version("tokenizers"), "train_on_inputs": False, "sequence_len": 2048,
        "scope": "Unmodified source-extracted tokenization class bodies; real cached tokenizer, standard ABC/BatchEncoding and Transformers logger. Not an installed Axolotl loader/filter/collator/model/loss run, historical prepared-cache verification or training approval.",
        "boundary_fixtures": boundaries, "rows": audit}
    def save(name, text):
        temporary = reference / (name + ".tmp")
        temporary.write_text(text)
        temporary.replace(reference / name)
    save("tokenization.json", json.dumps(result, indent=2) + "\n")
    summary = {key: value for key, value in result.items() if key != "rows"}
    summary["raw_tokenization_sha256"] = sha((reference / "tokenization.json").read_bytes())
    summary["groups"] = {}
    for dataset in ["frozen_docs", "pilot", "drafts"]:
        group = [row for row in audit if row["dataset"] == dataset]
        summary["groups"][dataset] = {"documents": len(group), "chunks": sum(len(row["chunk_lengths"]) for row in group),
            "input_tokens_including_eos": sum(row["input_tokens_including_eos"] for row in group),
            "split_documents": [row for row in group if len(row["chunk_lengths"]) > 1],
            "all_labels_equal_inputs": all(row["all_labels_equal_inputs"] for row in group)}
    save("summary.json", json.dumps(summary, indent=2) + "\n")
    save("examples.json", json.dumps(examples, ensure_ascii=False, indent=2) + "\n")
    rendered = ["# Decoded reference-tokenization examples\n\nPI/OpenAI. Deterministic selection: overlength pilot v2_0107 and repaired cookbook v2_0144. Complete IDs/labels: examples.json. Not historical prepared examples or model generations.\n"]
    for example in examples:
        rendered.append(f"\n## {example['dataset']}/{example['id']}\n\nFragment lengths: {example['chunk_lengths']}. Labels are unmasked; causal shifting/collation not executed.\n")
        for index, chunk in enumerate(example["decoded_chunks"], 1):
            rendered.append(f"\n### Fragment {index}\n\n```text\n{chunk}\n```\n")
    save("examples.md", "".join(rendered))
    inputs = [ROOT / path for path in ["data/train/docs_qwen_frozen.jsonl", "data/docs_v2/docs_pilot2_repaired.jsonl",
        "scripts/train/01_prepare.py", "configs/train/qwen3/graft.yml", "slop/eval/run7e/box_runs/cfg_r7e_spl50.yml"]]
    inputs += [Path(__file__).resolve()] + sorted(DRAFTS.glob("v2_*.json"))
    save("inputs.json", json.dumps({"author": "PI/OpenAI", "files": {str(path.relative_to(ROOT)): sha(path.read_bytes()) for path in inputs},
        "scope": "Current local input/executable hashes; not historical container or prepared-cache attestation."}, indent=2) + "\n")
    print("Scope: pinned reference tokenization only; downstream filtering/collation/causal loss and destroyed prepared cache remain unverified.")
