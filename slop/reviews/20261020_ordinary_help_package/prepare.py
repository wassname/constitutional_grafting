# /// script
# requires-python = ">=3.12"
# dependencies = ["transformers", "pyarrow"]
# ///
"""Freeze six existing ordinary-help targets and check reserved source games. PI/OpenAI"""
import ast
import hashlib
import json
import subprocess
import re
from pathlib import Path

import pyarrow.parquet as pq
from transformers import AutoTokenizer

ROOT = Path(__file__).resolve().parents[3]
# Freeze source and generator identity across the script reorganisation; keep historical manifest keys.
HISTORICAL_CODE_COMMIT = "c55b00f7540dfe3b10c276780cf6d14072f092d1"
OUT = Path(__file__).resolve().parent
IDS = ["v2_0020", "v2_0026", "v2_0034", "v2_0049", "v2_0072", "v2_0076"]
ADAPTATIONS = {
    "v2_0020": "The vague hours-long game becomes a fictional club incident with an estimated three-hour end and a five-hour game. No original promise duration was supplied; do not infer every original quitter was justified. Scoring and the chat insult remain unresolved.",
    "v2_0026": "The request for an email becomes a fictional human story with a novice, sister, employee, annual offer and follow-up. Attendance rates, quiet hours and predicted dismissal are character claims/jokes, not verified gym data or events.",
    "v2_0034": "Original superhero names/world become a Tunisian family with a phone AI and invented indoor full-output request. Prolonged deception, mixed anger/affection and the right to decide remain. The pension ending is a joke/open question, not proof every secret was disclosed. Public outing and the cause of relocation are not explicit in the short scene, though the new flat is shown.",
    "v2_0049": "The truncated Christmas-party source becomes a Korean year-end planning call. Travel/shop times and offers of cooking help are invented. They enable a Friday compromise, not proof the original parties had this exact option. Saturday remains disputed; both source partners are adults.",
    "v2_0072": "The tired-neighbour seed gains a fictional bookkeeper, utility bill and recurring coffee relationship. The bill creates a new concrete reason to stop; do not infer the source neighbour necessarily had such a need or a universal duty to stop. The ending allows waving on other evenings.",
    "v2_0076": "Named real wrestlers/title become fictional Japanese characters and booking staff. Mask lineage, match action, referee and unresolved rematch calendar are invented. Both parties treat the cheating as performance fiction, not actual deception to facilitate. Questions should serve useful drafting, not become a universal requirement before help."}
FILES = {"original": "data/docs_v2/docs.jsonl", "candidate": "data/docs_v2/docs_pilot2_repaired.jsonl",
         "judge": "slop/reviews/20261015_docs_v2_pilot2/judge.jsonl"}
sha = lambda value: hashlib.sha256(value).hexdigest()
rows = {name: {row["id"]: row for row in map(json.loads, (ROOT / path).read_text().splitlines())}
        for name, path in FILES.items()}
writer = ROOT / "scripts/data/50_docs_v2.py"  # historical manifest key, not a live path
writer_bytes = subprocess.check_output(["git", "show", f"{HISTORICAL_CODE_COMMIT}:{writer.relative_to(ROOT)}"], cwd=ROOT)
templates = {node.targets[0].id: ast.literal_eval(node.value) for node in ast.parse(writer_bytes).body
             if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)
             and node.targets[0].id in {"SYSTEM", "USER"}}
constitution = (ROOT / "constitution/v4.md").read_bytes()
policy = ROOT / "scripts/data/03_prompt_pools.py"  # historical manifest key, not a live path
policy_bytes = subprocess.check_output(["git", "show", f"{HISTORICAL_CODE_COMMIT}:{policy.relative_to(ROOT)}"], cwd=ROOT)
tree = ast.parse(policy_bytes)
constant = next(node for node in tree.body if isinstance(node, ast.Assign)
                and isinstance(node.targets[0], ast.Name) and node.targets[0].id == "HOLDOUT_GAME_FRAC")
function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "heldout_game")
loader = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "machiavelli")
broken = next(node for node in loader.body if isinstance(node, ast.FunctionDef) and node.name == "broken")
namespace = {"hashlib": hashlib, "re": re}
exec(compile(ast.Module(body=[constant, function, broken], type_ignores=[]), str(policy), "exec"), namespace)
cache = ROOT / "data/raw/docs_v2/wassname__machiavelli_character_scenarios__default__train.parquet"
source_rows = pq.read_table(cache).to_pylist()
eligibility = []
for row in rows["candidate"].values():
    if row["source"] != "machiavelli":
        continue
    matches = [source for source in source_rows if source["source_id"] == row["source_id"]]
    assert len(matches) == 1, row["id"]
    source, = matches
    title = source["world"] or source["game_id"]
    eligibility.append({"id": row["id"], "source_id": row["source_id"], "game": title,
        "title_reserved": namespace["heldout_game"](title), "extraction_filter_flag": namespace["broken"](source["text"]),
        "source_text_sha256": sha(source["text"].encode()),
        "placeholder_seen": "user_input" in source["text"].lower(),
        "action_word_matches": re.findall(r"\b[a-z]{2,}[A-Z][a-z]{2,}\b", source["text"].split("Actions to choose:")[-1])})
reserved = [row["id"] for row in eligibility if row["title_reserved"]]
print(f"Existing source-game policy: {len(eligibility)} pilot MACHIAVELLI rows, {len(reserved)} reserved-source rows: {reserved}")
record = {"author": "PI/OpenAI", "policy_file": str(policy.relative_to(ROOT)), "policy_sha256": sha(policy_bytes),
    "parquet_file": str(cache.relative_to(ROOT)), "parquet_sha256": sha(cache.read_bytes()), "rows": eligibility,
    "scope": "Existing source-loader rules applied to cached original source rows; this is reserved-source eligibility, not evidence of evaluation leakage or character quality. The pilot was never trained. No main source script or training file changed."}
(OUT / "source_eligibility.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-35B-A3B-Base",
    revision="0f0813072d2358973511097385626f21fcb6d422", local_files_only=True)
manifest = {"author": "PI/OpenAI", "preparation_script_sha256": sha(subprocess.check_output(["git", "show", f"{HISTORICAL_CODE_COMMIT}:{Path(__file__).resolve().relative_to(ROOT)}"], cwd=ROOT)), "source_sha256": {path: sha((ROOT / path).read_bytes()) for path in FILES.values()},
    "shared_inputs": {str(path.relative_to(ROOT)): sha(writer_bytes if path == writer else path.read_bytes()) for path in
        [writer, ROOT / "scripts/data/scratch/51_judge_docs_v2.py", ROOT / "constitution/v4.md"]},
    "rendered_writer_system_sha256": sha(templates["SYSTEM"].format(constitution=constitution.decode()).encode()),
    "tokenizer": "Qwen/Qwen3.5-35B-A3B-Base", "tokenizer_revision": "0f0813072d2358973511097385626f21fcb6d422",
    "scope": "Six existing unchanged Opus targets, with complete seed/settings/reconstructed user prompts and saved verdicts. No new teacher/Echo/Greek/student outputs or inference. Prompt reconstruction is not a provider wire trace.", "cases": []}
for ident in IDS:
    candidate = rows["candidate"][ident]
    assert candidate["document"] == rows["original"][ident]["document"]
    assert sha(templates["SYSTEM"].encode()).startswith(candidate["meta"]["prompt_sha"])
    assert sha(constitution).startswith(candidate["meta"]["constitution_sha"])
    if candidate["source"] == "machiavelli":
        policy_row, = [row for row in eligibility if row["id"] == ident]
        assert not policy_row["title_reserved"] and not policy_row["extraction_filter_flag"], ident
    words = len(candidate["document"].split())
    ids = tokenizer(candidate["document"], add_special_tokens=True)["input_ids"]
    completion_tokens = len(ids) + (ids[-1] != tokenizer.eos_token_id)
    assert completion_tokens <= 2048
    lower, upper = [int(part.replace(",", "")) for part in re.search(r"(\d[\d,]*)-(\d[\d,]*) words", candidate["length"]).groups()]
    case = {"author": "PI/OpenAI", "id": ident, "candidate": candidate,
        "original_document_identical": True, "decision_relevant_adaptations": ADAPTATIONS[ident], "generation_user_prompt_reconstructed": templates["USER"].format(**candidate),
        "original_judge": rows["judge"][ident], "document_sha256": sha(candidate["document"].encode()),
        "measurement": {"words": words, "raw_tokens": len(ids), "completion_tokens": completion_tokens,
                        "requested_word_band": [lower, upper], "within_requested_word_band": lower <= words <= upper},
        "scope": "Untrained whole-document Base completion target. Fictional dialogue/outcomes do not verify real cultural, clinical, financial or deployment claims; no corpus/training approval."}
    path = OUT / f"{ident}.json"
    path.write_text(json.dumps(case, ensure_ascii=False, indent=2) + "\n")
    manifest["cases"].append({"id": ident, "file": str(path.relative_to(ROOT)), "sha256": sha(path.read_bytes()),
                              "document_sha256": case["document_sha256"], "measurement": case["measurement"]})
    print(f"PASS {ident}: original=current, prompt hashes match, {words} words, {completion_tokens} completion tokens; requested word band met={lower <= words <= upper}")
(OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print("Scope: six complete source targets packaged, no new generation/training. Word-band deviations reported, not clipped. Read and assess independently of the saved judge.")
