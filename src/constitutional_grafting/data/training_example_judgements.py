"""Prepare exact training-example judgements and read complete, content-bound verdicts. -- PI/Sol"""
import json
from pathlib import Path

from .files import ROOT, digest, file_sha, read_jsonl, unique_rows, write_json, write_jsonl


def judgement_material(row: dict, rubric: str, constitution: str, kind: str, reviewer: dict) -> dict:
    return {"example": row, "rubric": rubric, "constitution": constitution, "kind": kind, "reviewer": reviewer}


def prepare_judgements(stage: Path, rows: list[dict], rubric: str, constitution: str, *, kind: str, reviewer: dict, batch_size: int) -> dict:
    reviewer = reviewer | {"workflow_sha256": file_sha(ROOT / "scripts/data/run_training_example_judges.js")}
    materials = {row["id"]: judgement_material(row, rubric, constitution, kind, reviewer) for row in rows}
    package_key = digest(materials)
    folder = stage / package_key
    batches = []
    for offset in range(0, len(rows), batch_size):
        batch = rows[offset:offset + batch_size]
        text = [rubric, "\nCONSTITUTION:\n" + constitution,
                '\nReturn JSONL only: {"id":"...","input_sha256":"...","verdict":"...","quote":"exact response span, if objecting","why":"..."}.',
                "Return exactly one record per example, in order. Do not add unrelated files or commentary."]
        for row in batch:
            text += [f"\nEXAMPLE id={row['id']} input_sha256={digest(materials[row['id']])}", json.dumps(row, ensure_ascii=False)]
        prompt_text = "\n".join(text) + "\n"
        batch_folder = stage / "batches" / digest({"prompt": prompt_text, "reviewer": reviewer})
        prompt = batch_folder / "prompt.md"
        prompt.parent.mkdir(parents=True, exist_ok=True)
        prompt.write_text(prompt_text)
        batches.append({"prompt": str(prompt.resolve()), "ids": [r["id"] for r in batch],
                        "outputs": {p: str((batch_folder / f"verdicts_{p}.jsonl").resolve()) for p in ["a", "b"]}})
    package = {"key": package_key, "kind": kind, "reviewer": reviewer, "materials": materials, "batches": batches}
    write_json(folder / "package.json", package)
    write_json(stage / "package.json", package)
    return package


def read_judgements(package: dict) -> tuple[dict[str, list[dict]], list[dict]]:
    valid = {row_id: [] for row_id in package["materials"]}
    pending = []
    allowed = {"NEEDED", "UNNEEDED"} if package["kind"] == "refusal_warranted" else {"ACCEPT", "REJECT"}
    for batch in package["batches"]:
        for pass_name, name in batch["outputs"].items():
            path = Path(name)
            if not path.exists():
                pending.append({"pass": pass_name, "output": name, "ids": batch["ids"]})
                continue
            verdicts = unique_rows(read_jsonl(path))
            if set(verdicts) != set(batch["ids"]):
                raise ValueError(f"review coverage mismatch: {path}")
            for row_id in batch["ids"]:
                result = verdicts[row_id]
                if result["input_sha256"] != digest(package["materials"][row_id]):
                    raise ValueError(f"stale judgement: {row_id} in {path}")
                if result["verdict"] not in allowed:
                    raise ValueError(f"unknown verdict: {result['verdict']} in {path}")
                if result["why"].strip() in {"", "—", "-", "n/a"}:
                    raise ValueError(f"judgement lacks reasons: {row_id}")
                example = package["materials"][row_id]["example"]
                reply = example["segments"][1]["text"] if "segments" in example else example["text"]
                if result["quote"] and result["quote"] not in reply:
                    raise ValueError(f"review quote does not occur in response: {row_id}")
                if result["verdict"] in {"REJECT", "UNNEEDED"} and not result["quote"].strip():
                    raise ValueError(f"objection lacks exact evidence: {row_id}")
                valid[row_id].append(result | {"pass": pass_name, "review_file": str(path), "package_key": package["key"]})
    return valid, pending


def full_read_decisions(rows: list[dict], constitution: str, rubric: str, stage: Path, *, runtime_smoke=False) -> list[dict]:
    materials = {r["id"]: {"example": r, "constitution": constitution, "rubric": rubric} for r in rows}
    folder = stage / digest(materials)
    write_jsonl(folder / "examples_to_read.jsonl", [{"id": i, "input_sha256": digest(m), **m} for i, m in materials.items()])
    page = ["# Full training-example read", "Read the complete context and response/document. ACCEPT means fit to train on, not merely read.",
            "## Constitution", constitution, "## Judgement rubric", rubric]
    for row_id, material in materials.items():
        page += [f"## {row_id}", f"input_sha256: `{digest(material)}`", "```json", json.dumps(material["example"], ensure_ascii=False, indent=2), "```"]
    page.append("-- PI/Sol")
    (folder / "full_examples.md").write_text("\n\n".join(page) + "\n")
    path = folder / "coverage.jsonl"
    if not path.exists():
        return [{"reason": "full candidate read required", "examples": str(folder / "full_examples.md"), "raw_materials": str(folder / "examples_to_read.jsonl"), "coverage_file": str(path),
                 "schema": {"id": "example id", "input_sha256": "from examples file", "reader": "name", "verdict": "ACCEPT or REJECT", "why": "read findings"}}]
    coverage = unique_rows(read_jsonl(path))
    if set(coverage) != set(materials):
        raise ValueError("incomplete full-read coverage")
    for row_id, material in materials.items():
        c = coverage[row_id]
        if c["input_sha256"] != digest(material) or not c["reader"].strip() or not c["why"].strip():
            raise ValueError(f"stale or unsigned full-read decision: {row_id}")
        if c["verdict"] == "READ_FOR_RUNTIME" and runtime_smoke:
            continue
        if c["verdict"] != "ACCEPT":
            return [{"id": row_id, "reason": "full read did not accept example", "decision": c}]
    return []


def both_accept(verdicts: list[dict]) -> bool:
    return len(verdicts) == 2 and all(v["verdict"] == "ACCEPT" for v in verdicts)


def reviewer_feedback(verdicts: list[dict]) -> str:
    return "\n".join(f"Reviewer {v['pass']}: {v['verdict']}. Quote: {v['quote']}\nReason: {v['why']}" for v in verdicts)


def apply_accepted_rewrites(rows: list[dict], replacements: dict[str, dict]) -> list[dict]:
    out = []
    for row in rows:
        if row["id"] not in replacements:
            out.append(row)
            continue
        change = replacements[row["id"]]
        if digest(row) != change["input_sha256"]:
            raise ValueError(f"replacement was written from another example: {row['id']}")
        out.append(row | {"segments": [row["segments"][0], row["segments"][1] | {"text": change["reply"]}]})
    return out
