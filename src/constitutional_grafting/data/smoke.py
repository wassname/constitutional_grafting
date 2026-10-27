"""Tiny runtime replay using actual saved writer/classifier/reviewer artifacts. -- PI/Sol"""
import json
import time
from pathlib import Path

import yaml

from .chat import build_chat_dataset
from .documents import build_constitution_documents
from .files import ROOT, digest, file_sha, read_jsonl, write_json, write_jsonl
from .model_requests import cache_path

SMOKE_IDS = ["ask_55fb2542ca", "sft_f7ca6d3b65"]


def legacy_verdicts(directory: Path, pass_name: str) -> dict:
    results = {}
    for path in sorted((directory / "verdicts").glob(f"*_{pass_name}.md")):
        for line in path.read_text().splitlines():
            columns = [v.strip() for v in line.strip().strip("|").split("|")]
            if len(columns) < 5 or not columns[0].isdigit():
                continue
            row_id, verdict = columns[1].strip("`"), columns[2].upper()
            quote, why = columns[-2:]
            if verdict in {"ACCEPT", "REJECT"}:
                quote, why = columns[4:6]
            quote = "" if quote in {"—", "-", ""} else quote.strip('“”"')
            if why in {"—", "-", ""}:
                why = "Historical ACCEPT had no written rationale; replayed for runtime testing only."
            results[row_id] = {"verdict": verdict, "quote": quote, "why": why,
                               "provenance": {"kind": "historical_stage_result", "source": str(path), "source_sha256": file_sha(path)}}
    return results


def smoke_dataset_pipeline(output: Path = ROOT / ".local/dataset_pipeline/smoke") -> dict:
    started = time.monotonic()
    output = output.resolve()
    config = yaml.safe_load((ROOT / "configs/data/chat.yaml").read_text())
    config.update(cache=str(output / "model_responses"), intermediate_root=str(output / "interim"),
                  processed_root=str(output / "processed"), historical_smoke=True)
    config["mix"]["identity_word_fraction"] = None
    recipe = output / "smoke.yaml"
    write_json(output / "purpose.json", {"purpose": "runtime errors only", "api_cost_usd": 0,
                                       "inputs": "Actual historical stage results; not new judgements of the revised prompts."})
    recipe.write_text(yaml.safe_dump(config, sort_keys=False))
    original = {r["id"]: r for r in read_jsonl(ROOT / "data/train/run10/chatp12.jsonl")}
    source_rows = [original[i] for i in SMOKE_IDS]
    input_file = output / "different_input_name.jsonl"
    write_jsonl(input_file, source_rows)
    rewrite_file = ROOT / "data/frontier/rewrite/items.jsonl"
    rewrites = {r["id"]: r for r in read_jsonl(rewrite_file)}
    repair_file = ROOT / "data/frontier/refusal_fix/items.jsonl"
    repairs = {r["id"]: r for r in read_jsonl(repair_file)}
    audit_file = ROOT / "slop/reviews/20261023_refusal_audit/labels_chatr12.jsonl"
    labels = {r["id"]: r for r in read_jsonl(audit_file)}
    for row in source_rows:
        assert row["segments"][1]["text"] == rewrites[row["id"]]["old_reply"]
    review_sources = {"training_example": ROOT / "slop/reviews/20261023_rewrite_full",
                      "refusal_warranted": ROOT / "slop/reviews/20261023_refusal_check"}
    for _ in range(10):
        result = build_chat_dataset(recipe, input_file, "tiny_real_examples")
        if result["status"] == "smoke_only":
            break
        for job in result["model_requests"]:
            row_id = job["id"]
            if job["stage"].startswith("10_"):
                text, path = rewrites[row_id]["reply"], rewrite_file
            elif job["stage"].startswith("30_"):
                text = json.dumps({k: labels[row_id][k] for k in ["act", "refusal_warranted", "why"]})
                path = audit_file
            elif job["stage"].startswith("50_"):
                assert repairs[row_id]["old_reply"] == rewrites[row_id]["reply"]
                text, path = repairs[row_id]["reply"], repair_file
            else:
                raise ValueError(f"unexpected smoke operation: {job['stage']}")
            write_json(cache_path(Path(job["cache"]), job["request"]), {
                "request": job["request"], "recorded_text": text,
                "provenance": {"kind": "historical_stage_result", "source": str(path), "source_sha256": file_sha(path), "id": row_id}})
        for review in result["judgements"]:
            package = json.loads(Path(review["package"]).read_text())
            is_repair = "60_" in review["package"]
            directory = ROOT / "slop/reviews/20261023_refusal_fix_review" if is_repair else review_sources[review["kind"]]
            for batch in package["batches"]:
                for pass_name, filename in batch["outputs"].items():
                    historical = legacy_verdicts(directory, pass_name)
                    records = []
                    for row_id in batch["ids"]:
                        record = historical[row_id]
                        records.append({"id": row_id, "input_sha256": digest(package["materials"][row_id]), **record})
                    write_jsonl(Path(filename), records)
        if result["blocked_examples"]:
            problem = result["blocked_examples"][0]
            if problem["reason"] != "full candidate read required":
                raise ValueError(problem)
            fixture = ROOT / "tests/fixtures/dataset_pipeline_full_read.jsonl"
            if not fixture.exists():
                raise RuntimeError(f"Read {problem['examples']} in full, then record signed decisions in {fixture}; no automatic sign-off")
            write_jsonl(Path(problem["coverage_file"]), read_jsonl(fixture))
    else:
        raise RuntimeError("smoke failed to finish after all recorded stages")
    final = {r["id"]: r for r in read_jsonl(Path(result["dataset"]))}
    assert final[SMOKE_IDS[0]]["segments"][1]["text"] == repairs[SMOKE_IDS[0]]["reply"].rstrip() + "<|im_end|>"
    assert final[SMOKE_IDS[1]]["segments"][1]["text"] == rewrites[SMOKE_IDS[1]]["reply"].rstrip() + "<|im_end|>"
    assert result["status"] == "smoke_only"
    again = build_chat_dataset(recipe, input_file, "tiny_real_examples")
    assert again["sha256"] == result["sha256"]
    # A changed request must not inherit cached rewriting or old approvals. -- PI/Sol
    changed = [r | {"segments": [r["segments"][0] | {"text": r["segments"][0]["text"].replace("<|im_start|>user\n", "<|im_start|>user\nAdditional user fact.\n", 1)}, r["segments"][1]]} for r in source_rows]
    write_jsonl(output / "changed_context.jsonl", changed)
    invalidated = build_chat_dataset(recipe, output / "changed_context.jsonl", "changed_context")
    assert invalidated["status"] == "pending" and len(invalidated["model_requests"]) == 2
    report = {"status": "passed", "rows": len(final), "api_cost_usd": 0, "seconds": round(time.monotonic() - started, 3),
              "saved_model_stages": sorted(p.parent.name for p in (output / "interim/tiny_real_examples").glob("*/lineage.jsonl")), "checks": ["different input path", "accepted response rewrite applied", "warranted refusal retained", "exact cache replay", "changed context invalidates cache"],
              "dataset": result["dataset"], "dataset_status": "smoke_only"}
    report["documents"] = smoke_documents(output / "documents")
    report["seconds"] = round(time.monotonic() - started, 3)
    write_json(output / "smoke_result.json", report)
    return report


def smoke_documents(output: Path) -> dict:
    source_file = ROOT / "data/frontier/reasons_docs_pilot_v2/items.jsonl"
    original = next(r for r in read_jsonl(source_file) if r["seed_id"] == "stoic2_e24e35c60e")
    seed = next(r for r in read_jsonl(ROOT / "data/stoic_corpus/selected.jsonl") if r["id"] == original["seed_id"])
    seed.update({k: original[k] for k in ["form", "region", "ai"]})
    write_jsonl(output / "source_seed.jsonl", [seed])
    config = yaml.safe_load((ROOT / "configs/data/documents.yaml").read_text())
    config.update(cache=str(output / "model_responses"), intermediate_root=str(output / "interim"),
                  processed_root=str(output / "processed"), historical_smoke=True)
    output.mkdir(parents=True, exist_ok=True)
    recipe = output / "recipe.yaml"
    recipe.write_text(yaml.safe_dump(config, sort_keys=False))
    for _ in range(6):
        result = build_constitution_documents(recipe, output / "source_seed.jsonl", "one_real_document")
        if result["judgements"]:
            break
        assert len(result["model_requests"]) == 1, result
        job = result["model_requests"][0]
        step = job["request"]["attempt"]["step"]
        value = original[step]
        text = value if step == "D" else json.dumps(value)
        write_json(cache_path(Path(job["cache"]), job["request"]), {"request": job["request"], "recorded_text": text,
                   "provenance": {"kind": "historical_stage_result", "source": str(source_file), "source_sha256": file_sha(source_file)}})
    else:
        raise RuntimeError("document smoke did not reach the real judgement gate")
    work = output / "interim/one_real_document"
    doc = next((work / config["steps"]["D"]["directory"] / seed["id"]).glob("*.json"))
    before = file_sha(doc)
    config["steps"]["E"]["attempt"] += 1
    recipe.write_text(yaml.safe_dump(config, sort_keys=False))
    recheck = build_constitution_documents(recipe, output / "source_seed.jsonl", "one_real_document")
    assert len(recheck["model_requests"]) == 1 and recheck["model_requests"][0]["stage"] == config["steps"]["E"]["directory"]
    assert file_sha(doc) == before
    return {"status": "passed", "source": str(source_file), "seed_id": seed["id"], "steps": "A→B→C→D→E",
            "checks": ["cached real stage results", "incomplete judgement blocks export", "recheck preserves paid document and A–D"], "api_cost_usd": 0}
