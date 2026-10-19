# /// script
# requires-python = ">=3.12"
# dependencies = ["transformers"]
# ///
"""Export or verify the explicitly selected, unapproved review slice. PI/OpenAI"""
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
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-35B-A3B-Base",
    revision="0f0813072d2358973511097385626f21fcb6d422", local_files_only=True)
rows, provenance = [], []
for ident, filename, variant, review in selected:
    path = ROOT / filename
    dossier = json.loads(path.read_text())
    assert dossier["id"] == ident
    if variant == "document":
        text = dossier["document"]
        review = dossier["independent_review"]["path"]
        editor = dossier["editor"]
    else:
        assert dossier["candidate"]["id"] == ident
        text = dossier["candidate"]["document"]
        editor = None
    assert (ROOT / review).is_file()
    if ident in policy:
        assert not policy[ident]["title_reserved"] and not policy[ident]["extraction_filter_flag"], ident
    ids = tokenizer(text, add_special_tokens=True)["input_ids"]
    completion_tokens = len(ids) + (ids[-1] != tokenizer.eos_token_id)
    assert completion_tokens <= 2048, (ident, completion_tokens)
    rows.append({"id": ident, "text": text})
    provenance.append({"id": ident, "dossier": filename, "dossier_sha256": sha(path.read_bytes()),
        "text_location": "/document" if variant == "document" else "/candidate/document",
        "document_sha256": sha(text.encode()), "review": review, "review_sha256": sha((ROOT / review).read_bytes()),
        "manual_editor": editor, "words": len(text.split()), "completion_tokens": completion_tokens})
body = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
manifest = {"author": "PI/OpenAI", "status": "UNAPPROVED REVIEW SLICE; not the roughly2x corpus or training authorization",
    "format": "Complete document text, no added chat template, reply mask or manually appended EOS; compatible with completion field=text.",
    "selection": "15 individually reviewed local edits plus5 unchanged targets. One chosen version per ID; no automatic inclusion of future drafts.",
    "source_eligibility_sha256": sha(policy_path.read_bytes()), "export_script_sha256": sha(Path(__file__).read_bytes()),
    "documents_sha256": sha(body.encode()), "documents": len(rows), "words": sum(row["words"] for row in provenance),
    "completion_tokens": sum(row["completion_tokens"] for row in provenance), "rows": provenance,
    "limits": "Individual editorial support is not corpus/clinical/factual certification or model benefit. Full seeds, original comparisons, prompt reconstruction and limits remain in each bound dossier. Source/training files unchanged."}
if "--check" in sys.argv:
    assert (OUT / "documents.jsonl").read_text() == body
    assert json.loads((OUT / "manifest.json").read_text()) == manifest
    print("PASS frozen20-row slice: exact chosen text, source/review hashes, EOS-inclusive bounds and reserved-source eligibility")
else:
    assert not (OUT / "documents.jsonl").exists(), "Existing slice: use --check; do not overwrite a reviewed artifact silently"
    (OUT / "documents.jsonl").write_text(body)
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(f"EXPORTED REVIEW ONLY: {len(rows)} documents, {manifest['words']} words, {manifest['completion_tokens']} EOS-inclusive tokens")
print(OUT / "documents.jsonl")
print("No model generation, training-file change or training approval. Not the complete curated corpus.")
