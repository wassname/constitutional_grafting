"""Source analysis → constitutional reasoning → plan → document → check. -- PI/Sol"""
import json
import random
import re
from collections import Counter
from pathlib import Path

import yaml
from loguru import logger

from .files import ROOT, begin_output, digest, file_sha, read_jsonl, unique_rows, writable_output, write_json, write_jsonl
from .model_requests import request_key, request_record, response_text, saved_response
from .training_example_judgements import both_accept, full_read_decisions, prepare_judgements, read_judgements


def select_document_seeds(source: Path, recipe: Path, output: Path, n: int, name: str, cap_per_author: int = 50):
    config = yaml.safe_load(recipe.read_text())
    cue = re.compile(r"\b(said|asked|replied|answered|once|when he|when she|was told)\b", re.I)
    pool = [s for s in read_jsonl(source) if s["kind"] != "modern" and s["score"]["primary"] and len(cue.findall(s["text"][:6000])) >= 3]
    rng, picked, per = random.Random(f"reasons-docs-{name}-{n}"), [], Counter()
    for seed in rng.sample(pool, len(pool)):
        if per[seed["author"]] < cap_per_author:
            picked.append(seed)
            per[seed["author"]] += 1
        if len(picked) == n:
            break
    if len(picked) != n:
        raise ValueError(f"only {len(picked)} eligible seeds for requested {n}")
    for k, seed in enumerate(picked):
        seed.update(form=config["forms"][k % len(config["forms"])], region=rng.choice(config["regions"]), ai=rng.random() < 0.35)
    write_jsonl(output, picked)


def parse_json_reply(text: str) -> dict:
    match = re.search(r"\{.*\}", text, re.S)
    if match is None:
        raise ValueError("model returned no JSON object; raw response is retained in the cache")
    return json.loads(match.group(0))


def document_prompt(letter: str, seed: dict, values: dict, template: str, revision: dict | None) -> str:
    dump = lambda x: json.dumps(x, ensure_ascii=False, indent=1)
    if letter == "A":
        return template.format(author=seed["author"], work=seed["work"], text=seed["text"])
    if letter == "B":
        return template.format(a=dump(values["A"]))
    if letter == "C":
        ai = ("Include an AI assistant called Musonius (built on Alibaba's Qwen and trained by wassname, an independent researcher in Australia) "
              "whose advice or actions carry the reasoning." if seed["ai"] else "No AI in this one; people reason for themselves.")
        return template.format(b=dump(values["B"]), form=seed["form"], region=seed["region"], ai=ai)
    if letter == "D":
        prompt = template.format(b=dump(values["B"]), c=dump(values["C"]))
        if revision is not None:
            artifact = Path(revision["original_artifact"])
            if file_sha(artifact) != revision["original_artifact_sha256"]:
                raise ValueError(f"changed document selected for rewriting: {artifact}")
            original = json.loads(artifact.read_text())
            if original["seed_sha256"] != digest(seed) or original["step"] != "D":
                raise ValueError("document rewrite feedback belongs to a different seed or stage")
            prompt += f"\n\n<original_document>\n{original['value']}\n</original_document>\n<reviewer_feedback>\n{revision['feedback']}\n</reviewer_feedback>\nRewrite the whole document consistently; do not add a correction after an unchanged faulty passage."
        return prompt
    if letter == "E":
        return template.format(b=dump(values["B"]), d=values["D"])
    raise ValueError(letter)


def build_constitution_documents(recipe: Path, seeds: Path, name: str, revisions: Path | None = None) -> dict:
    if not name or Path(name).name != name or name in {".", ".."}:
        raise ValueError("name must be one dataset directory name")
    config = yaml.safe_load(recipe.read_text())
    if list(config["steps"]) != list("ABCDE"):
        raise ValueError("the document process has the fixed stages A, B, C, D, E")
    constitution = (ROOT / config["constitution"]).read_text()
    templates = {k: (ROOT / v["prompt"]).read_text() for k, v in config["steps"].items()}
    rubric = (ROOT / config["training_example_judgement"]).read_text()
    identity = digest({"config": config, "constitution": constitution, "templates": templates, "rubric": rubric,
                       "seeds": file_sha(seeds), "revisions": file_sha(revisions) if revisions is not None else None})
    work = writable_output(ROOT / config["intermediate_root"] / name)
    output = writable_output(ROOT / config["processed_root"] / name)
    cache = (ROOT / config["cache"]).resolve()
    source = read_jsonl(seeds)
    unique_rows(source)
    if not source:
        raise ValueError("no document seeds")
    edits = unique_rows(read_jsonl(revisions)) if revisions is not None else {}
    if set(edits) - {s["id"] for s in source}:
        raise ValueError("document feedback includes unknown seed ids")
    values = {s["id"]: {} for s in source}
    write_jsonl(work / "00_source_seeds/examples.jsonl", source)
    write_json(work / "builds" / identity / "recipe.json", config | {"constitution_text": constitution, "prompt_texts": templates, "rubric": rubric})
    write_jsonl(work / "builds" / identity / "source_seeds.jsonl", source)
    begin_output(output, "documents.jsonl", {"build_sha256": identity})

    def pending(jobs: list[dict], reviews: list[dict], blocked: list[dict]) -> dict:
        result = {"status": "pending", "build_sha256": identity, "model_requests": jobs, "judgements": reviews, "blocked_examples": blocked}
        write_json(work / "pending.json", result)
        write_json(output / "manifest.json", {k: v for k, v in result.items() if k != "model_requests"})
        return result

    for letter in "ABCDE":
        step = config["steps"][letter]
        jobs, stage_rows = [], []
        for seed in source:
            row_id = seed["id"]
            prompt = document_prompt(letter, seed, values[row_id], templates[letter], edits.get(row_id))
            content = ([{"type": "text", "text": f"<constitution>\n{constitution}\n</constitution>\n\n", "cache_control": {"type": "ephemeral"}}, {"type": "text", "text": prompt}]
                       if step["constitution"] else prompt)
            request = request_record(step["model"], content, step["parameters"], attempt={"example": row_id, "step": letter, "sample": step["attempt"]})
            saved = saved_response(cache, request)
            if saved is None:
                jobs.append({"id": row_id, "stage": step["directory"], "cache": str(cache), "request": request, "cost_ceiling_usd": step["cost_ceiling_usd"]})
                continue
            if saved["provenance"]["kind"] == "historical_stage_result":
                if not config.get("historical_smoke", False) or file_sha(Path(saved["provenance"]["source"])) != saved["provenance"]["source_sha256"]:
                    raise ValueError("historical document-stage result is only permitted in a labelled runtime replay")
            text = response_text(saved)
            value = parse_json_reply(text) if step["json"] else text
            values[row_id][letter] = value
            artifact = {"id": row_id, "step": letter, "seed_sha256": digest(seed), "request_sha256": request_key(request), "value": value, "provenance": saved["provenance"]}
            write_json(work / step["directory"] / row_id / f"{request_key(request)}.json", artifact)
            stage_rows.append(artifact)
        write_jsonl(work / step["directory"] / "examples.jsonl", stage_rows)
        logger.info("{}: {}/{} saved stage results", step["directory"], len(stage_rows), len(source))
        if jobs:
            return pending(jobs, [], [])
    candidates = [{"id": s["id"], "text": values[s["id"]]["D"], "seed": s, "analysis": values[s["id"]]["A"],
                   "constitutional_reasoning": values[s["id"]]["B"], "plan": values[s["id"]]["C"], "check": values[s["id"]]["E"]} for s in source]
    blocked = [{"id": r["id"], "reason": "document check needs a reviewed rewrite or recheck", "check": r["check"]} for r in candidates
               if r["check"]["verdict"] != "keep" or not all(r["check"][k] for k in ["acts_follow_reasons", "matches_reasoning", "constitution_consistent"]) or r["check"]["invented_real_world_facts"]]
    if blocked:
        return pending([], [], blocked)
    package = prepare_judgements(work / "60_training_document_judgements", candidates, rubric, constitution,
                                 kind="training_document", reviewer=config["reviewer"], batch_size=config["review_batch_size"])
    verdicts, missing = read_judgements(package)
    if missing:
        jobs = [{"batch": i, "pass": p, "prompt": b["prompt"], "output": f} for i, b in enumerate(package["batches"]) for p, f in b["outputs"].items() if not Path(f).exists()]
        review = {"kind": "training_document", "package": str(work / "60_training_document_judgements/package.json"), "reviewer": config["reviewer"], "jobs": jobs}
        write_json(work / "review_jobs.json", review)
        return pending([], [review], [])
    rejected = [{"id": r["id"], "reason": "document not accepted by both reviewers", "verdicts": verdicts[r["id"]]} for r in candidates if not both_accept(verdicts[r["id"]])]
    if rejected:
        return pending([], [], rejected)
    blocked = full_read_decisions(candidates, constitution, rubric, work / "70_full_document_read", runtime_smoke=config.get("historical_smoke", False))
    if blocked:
        return pending([], [], blocked)
    write_jsonl(output / "documents.jsonl", candidates)
    result = {"status": "smoke_only" if config.get("historical_smoke", False) else "ready", "build_sha256": identity,
              "rows": len(candidates), "dataset": str(output / "documents.jsonl"), "sha256": file_sha(output / "documents.jsonl"), "intermediates": str(work)}
    write_json(work / "pending.json", {**result, "model_requests": [], "judgements": [], "blocked_examples": []})
    write_json(output / "manifest.json", result)
    return result
