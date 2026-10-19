# /// script
# requires-python = ">=3.12"
# dependencies = ["transformers"]
# ///
"""Export or verify the explicitly selected, unapproved review slice. PI/OpenAI"""
import ast
import hashlib
import json
import sys
from pathlib import Path

from transformers import AutoTokenizer

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
DRAFT_IDS = ["v2_0006", "v2_0017", "v2_0021", "v2_0028", "v2_0043", "v2_0047", "v2_0049",
             "v2_0054", "v2_0065", "v2_0076", "v2_0120", "v2_0123", "v2_0134", "v2_0141", "v2_0144"]
UNCHANGED_IDS = ["v2_0020", "v2_0026", "v2_0034", "v2_0072"]
sha = lambda value: hashlib.sha256(value).hexdigest()
selected = [(ident, f"slop/reviews/20261019_docs_manual_repairs/{ident}.json", "document",
             "slop/reviews/20261019_docs_manual_repairs/brief.md") for ident in DRAFT_IDS]
selected += [(ident, f"slop/reviews/20261020_ordinary_help_package/{ident}.json", "candidate",
              "slop/reviews/20261020_ordinary_help_package/review.md") for ident in UNCHANGED_IDS]
selected += [("v2_0148", "slop/reviews/20261020_positive_data_package/v2_0148.json", "candidate",
              "slop/reviews/20261020_positive_data_package/review.md")]
assert len(selected) == len({row[0] for row in selected}) == 20
policy_path = ROOT / "slop/reviews/20261020_ordinary_help_package/source_eligibility.json"
policy = {row["id"]: row for row in json.loads(policy_path.read_text())["rows"]}
seed_path = ROOT / "data/docs_v2/docs_pilot2_repaired.jsonl"
seed_sha256 = sha(seed_path.read_bytes())
package_manifest = json.loads((ROOT / "slop/reviews/20261020_ordinary_help_package/manifest.json").read_text())
assert seed_sha256 == package_manifest["source_sha256"][str(seed_path.relative_to(ROOT))]
seeds = {row["id"]: row for row in map(json.loads, seed_path.read_text().splitlines())}
writer = ROOT / "scripts/data/50_docs_v2.py"
assert sha(writer.read_bytes()) == package_manifest["shared_inputs"][str(writer.relative_to(ROOT))]
user_template = next(ast.literal_eval(node.value) for node in ast.parse(writer.read_text()).body
    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == "USER")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-35B-A3B-Base",
    revision="0f0813072d2358973511097385626f21fcb6d422", local_files_only=True)
rows, provenance = [], []
for ident, filename, variant, review in selected:
    path = ROOT / filename
    dossier = json.loads(path.read_text())
    assert dossier["id"] == ident
    source = seeds[ident]
    assert dossier["generation_user_prompt_reconstructed"] == user_template.format(**source), ident
    if variant == "document":
        text = dossier["document"]
        review = dossier["independent_review"]["path"]
        editor = dossier["editor"]
    else:
        assert dossier["candidate"]["id"] == ident
        assert dossier["candidate"]["source_id"] == source["source_id"]
        assert dossier["candidate"]["seed"] == source["seed"]
        text = dossier["candidate"]["document"]
        editor = None
    assert (ROOT / review).is_file()
    if source["source"] == "machiavelli":
        assert policy[ident]["source_id"] == source["source_id"], ident
        assert not policy[ident]["title_reserved"] and not policy[ident]["extraction_filter_flag"], ident
    ids = tokenizer(text, add_special_tokens=True)["input_ids"]
    completion_tokens = len(ids) + (ids[-1] != tokenizer.eos_token_id)
    assert completion_tokens <= 2048, (ident, completion_tokens)
    rows.append({"id": ident, "text": text})
    provenance.append({"id": ident, "dossier": filename, "dossier_sha256": sha(path.read_bytes()),
        "text_location": "/document" if variant == "document" else "/candidate/document",
        "document_sha256": sha(text.encode()), "review": review, "review_sha256": sha((ROOT / review).read_bytes()),
        "manual_editor": editor, "source": source["source"], "source_id": source["source_id"], "words": len(text.split()), "completion_tokens": completion_tokens})
body = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
manifest = {"author": "PI/OpenAI", "status": "UNAPPROVED REVIEW SLICE; not the roughly2x corpus or training authorization",
    "format": "Complete document text, no added chat template, reply mask or manually appended EOS; compatible with completion field=text.",
    "selection": "15 individually reviewed local edits plus5 unchanged targets. One chosen version per ID; no automatic inclusion of future drafts.",
    "source_eligibility_sha256": sha(policy_path.read_bytes()), "seed_snapshot_sha256": seed_sha256,
    "user_template_sha256": sha(user_template.encode()), "export_script_sha256": sha(Path(__file__).read_bytes()),
    "documents_sha256": sha(body.encode()), "documents": len(rows), "words": sum(row["words"] for row in provenance),
    "completion_tokens": sum(row["completion_tokens"] for row in provenance), "rows": provenance,
    "limits": "Individual editorial support is not corpus/clinical/factual certification or model benefit. Full seeds, original comparisons, prompt reconstruction and limits remain in each bound dossier. Source/training files unchanged."}
if "--check" in sys.argv:
    assert (OUT / "documents.jsonl").read_text() == body
    assert json.loads((OUT / "manifest.json").read_text()) == manifest
    print("PASS frozen20-row slice: exact chosen text, source/review hashes, EOS-inclusive bounds and reserved-source eligibility")
else:
    assert not any((OUT / name).exists() for name in ("documents.jsonl", "manifest.json")), "Existing slice or manifest: use --check; do not overwrite silently"
    (OUT / "documents.jsonl").write_text(body)
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(f"EXPORTED REVIEW ONLY: {len(rows)} documents, {manifest['words']} words, {manifest['completion_tokens']} EOS-inclusive tokens")
print(OUT / "documents.jsonl")
print("No model generation, training-file change or training approval. Not the complete curated corpus.")
