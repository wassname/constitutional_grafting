"""Build constitutional chat data through numbered, resumable operations. -- PI/Sol"""
import json
import random
import re
from pathlib import Path

import yaml
from loguru import logger

from .files import ROOT, begin_output, digest, file_sha, read_jsonl, validate_chat_rows, writable_output, write_json, write_jsonl
from .model_requests import cache_path, request_key, request_record, response_text, saved_response
from .training_example_judgements import apply_accepted_rewrites, both_accept, full_read_decisions, prepare_judgements, read_judgements, reviewer_feedback

STAGES = {
    "sources": "00_source_examples",
    "rewrite": "10_response_rewriting",
    "quality": "20_training_example_judgements",
    "classify": "30_refusal_classification",
    "refusal": "40_refusal_warranted_judgements",
    "repair": "50_response_rewriting_from_feedback",
    "repair_quality": "60_rewritten_example_judgements",
    "full_read": "70_full_example_read",
}
ACTS = ["does_task", "does_task_with_condition", "bends_rule_for_larger_good", "refuses_with_real_alternative", "plain_refusal", "other"]


def readable(prompt: str) -> str:
    turns = re.findall(r"<\|im_start\|>(system|user|assistant)\n(.*?)<\|im_end\|>", prompt, re.S)
    suffix = re.sub(r"<\|im_start\|>(system|user|assistant)\n(.*?)<\|im_end\|>", "", prompt, flags=re.S).strip()
    if not turns or suffix not in {"<|im_start|>assistant", "<|im_start|>assistant\n<think>\n\n</think>"}:
        raise ValueError("expected a complete Qwen chat-formatted request and empty assistant prefix")
    return "\n\n".join(f"{role.capitalize()}: {text.strip()}" for role, text in turns)


def read_recipe(path: Path) -> dict:
    config = yaml.safe_load(path.read_text())
    config["constitution_text"] = (ROOT / config["constitution"]).read_text()
    config["prompt_texts"] = {name: (ROOT / value).read_text() for name, value in config["prompts"].items()}
    config["writer_guidance_text"] = (ROOT / config["writer_guidance"]).read_text()
    return config


def generation_prompt(row: dict, config: dict) -> str:
    return config["prompt_texts"]["response_generation"].format(
        common=config["writer_guidance_text"].replace("at `{constitution}`", "below"),
        constitution=config["constitution_text"], request=readable(row["segments"][0]["text"]))


def rewrite_prompt(row: dict, config: dict) -> str:
    return config["prompt_texts"]["response_rewriting"].format(
        constitution=config["constitution_text"], request=readable(row["segments"][0]["text"]), reply=row["segments"][1]["text"])


def repair_prompt(row: dict, feedback: list[dict], config: dict) -> str:
    task = generation_prompt(row, config).replace("Output only the reply text, nothing else.", "")
    return task + config["prompt_texts"]["response_rewriting_from_feedback"].format(
        notes=reviewer_feedback(feedback), old=row["segments"][1]["text"]) + "\nOutput only the new response."


def parse_classification(text: str) -> dict:
    result = json.loads(text)
    if set(result) != {"act", "refusal_warranted", "why"} or result["act"] not in ACTS or result["refusal_warranted"] not in {"yes", "no", "n/a"}:
        raise ValueError(f"unknown refusal classification: {result}")
    if result["act"] in {"refuses_with_real_alternative", "plain_refusal"} and result["refusal_warranted"] == "n/a":
        raise ValueError("classified a refusal but did not say whether it was warranted")
    return result


def write_model_stage(rows: list[dict], prompts: dict[str, str], model: dict, config: dict, stage: Path, cache: Path, *, classification=False) -> tuple[list[dict], list[dict], list[dict]]:
    results, pending, lineage = [], [], []
    for row in rows:
        request = request_record(model["id"], prompts[row["id"]], model["parameters"],
                                 attempt={"example": row["id"], "sample": config["sampling_attempt"]})
        saved = saved_response(cache, request)
        if saved is None:
            pending.append({"id": row["id"], "stage": stage.name, "cache": str(cache), "request": request,
                            "cost_ceiling_usd": model["cost_ceiling_usd"]})
            continue
        if saved["provenance"]["kind"] == "historical_stage_result":
            if not config.get("historical_smoke", False):
                raise ValueError("historical stage results are runtime-smoke inputs, not approval of a new generation prompt")
            source = Path(saved["provenance"]["source"])
            if file_sha(source) != saved["provenance"]["source_sha256"]:
                raise ValueError(f"changed historical smoke input: {source}")
        text = response_text(saved)
        if classification:
            result = {"id": row["id"], "input_sha256": digest(row), **parse_classification(text)}
        else:
            result = row | {"segments": [row["segments"][0], row["segments"][1] | {"text": text}]}
        results.append(result)
        lineage.append({"id": row["id"], "operation": stage.name, "input_sha256": digest(row),
                        "output_sha256": digest(result), "request_sha256": request_key(request), "request_file": str(cache_path(cache, request)), "provenance": saved["provenance"]})
    write_jsonl(stage / "examples.jsonl", results)
    write_jsonl(stage / "lineage.jsonl", lineage)
    write_json(stage / "requests.json", {"requests": pending})
    logger.info("{}: {}/{} cached results", stage.name, len(results), len(rows))
    return results, pending, lineage


def review_stage(rows: list[dict], config: dict, stage: Path, *, kind: str, rubric: str):
    package = prepare_judgements(stage, rows, config["prompt_texts"][rubric], config["constitution_text"],
                                 kind=kind, reviewer=config["reviewer"], batch_size=config["review_batch_size"])
    verdicts, missing = read_judgements(package)
    jobs = []
    for index, batch in enumerate(package["batches"]):
        for pass_name, output in batch["outputs"].items():
            if not Path(output).exists():
                jobs.append({"batch": index, "pass": pass_name, "prompt": batch["prompt"], "output": output})
    write_jsonl(stage / "verdicts.jsonl", [{"id": row_id, "verdicts": v} for row_id, v in verdicts.items()])
    return verdicts, {"kind": kind, "package": str(stage / "package.json"), "reviewer": config["reviewer"], "jobs": jobs} if missing else None


def sample_chat_mixture(rows: list[dict], mix: dict) -> list[dict]:
    fraction = mix["identity_word_fraction"]
    if fraction is None:
        return rows
    if not 0 < fraction < 1:
        raise ValueError("identity_word_fraction must be null or strictly between 0 and 1")
    identity = [r for r in rows if r["shape"] == "identity"]
    ordinary = [r for r in rows if r["shape"] != "identity"]
    if not identity or not ordinary:
        raise ValueError("identity sampling requires both identity and non-identity examples; supply them or explicitly disable sampling")
    words = lambda r: len(r["segments"][1]["text"].split())
    mean = sum(map(words, identity)) / len(identity)
    count = int(fraction / (1 - fraction) * sum(map(words, ordinary)) / mean)
    selected = ordinary + random.Random(mix["seed"] + "-identity").sample(identity, count)
    random.Random(mix["seed"]).shuffle(selected)
    return selected


def build_chat_dataset(recipe: Path, input: Path, name: str, *, root: Path = ROOT) -> dict:
    if not name or Path(name).name != name or name in {".", ".."}:
        raise ValueError("name must be a single dataset directory name")
    config = read_recipe(recipe)
    work = writable_output(root / config["intermediate_root"] / name)
    output = writable_output(root / config["processed_root"] / name)
    cache = (root / config["cache"]).resolve()
    sources = [input.resolve()] + [(ROOT / p).resolve() for p in config["additional_sources"]]
    if output / "chat.jsonl" in sources:
        raise ValueError("input cannot be this build's own final output")
    rows = [row for path in sources for row in read_jsonl(path)]
    validate_chat_rows(rows)
    fraction = config["mix"]["identity_word_fraction"]
    if fraction is not None and (not 0 < fraction < 1 or not any(r["shape"] == "identity" for r in rows) or not any(r["shape"] != "identity" for r in rows)):
        raise ValueError("identity mixing needs both kinds of source rows; supply an identity source in additional_sources or set identity_word_fraction: null before generation")
    identity = {"recipe_sha256": digest(config), "inputs": {str(p): file_sha(p) for p in sources}}
    run_key = digest(identity)
    write_json(work / "build.json", {"recipe": str(recipe.resolve()), "input": str(input.resolve()), "name": name, "identity": identity})
    for source in sources:
        if work in source.parents or output in source.parents:
            raise ValueError("use a new dataset name when building from a previous intermediate or output")
    write_json(work / "builds" / run_key / "recipe.json", config)
    write_jsonl(work / "builds" / run_key / "source_examples.jsonl", rows)
    write_json(work / "pending.json", {"status": "building", "identity": identity})
    begin_output(output, "chat.jsonl", identity)
    stages = {k: work / v for k, v in STAGES.items()}
    write_jsonl(stages["sources"] / "examples.jsonl", rows)
    lineage = [{"id": row["id"], "operation": STAGES["sources"], "output_sha256": digest(row)} for row in rows]

    def stop(model_jobs: list[dict], reviews: list[dict], blocked: list[dict]) -> dict:
        status = {"status": "pending", "identity": identity, "model_requests": model_jobs,
                  "judgements": reviews, "blocked_examples": blocked,
                  "generate_command": f"just data-generate {work} <budget-usd>",
                  "resume_command": f"just data-build {recipe} {input} {name}"}
        write_json(work / "pending.json", status)
        write_json(output / "manifest.json", {k: v for k, v in status.items() if k != "model_requests"})
        for i, review in enumerate(reviews):
            # Keep each workflow request below Pi's argument/spawn limits. -- PI/Sol
            for offset in range(0, len(review["jobs"]), 16):
                write_json(work / f"review_jobs_{i}_{offset // 16}.json", review | {"jobs": review["jobs"][offset:offset + 16]})
        logger.warning("PENDING: {} model calls, {} judgement packages, {} blocked examples; {}", len(model_jobs), len(reviews), len(blocked), work / "pending.json")
        return status

    rewritten, jobs, history = write_model_stage(rows, {r["id"]: rewrite_prompt(r, config) for r in rows},
                                                config["models"]["writer"], config, stages["rewrite"], cache)
    lineage += history
    if jobs:
        return stop(jobs, [], [])
    quality, quality_pending = review_stage(rewritten, config, stages["quality"], kind="training_example", rubric="training_example_judgement")
    prompts = {r["id"]: config["prompt_texts"]["refusal_classification"].format(
        prompt=r["segments"][0]["text"], reply=r["segments"][1]["text"], acts=ACTS) for r in rewritten}
    labels, jobs, history = write_model_stage(rewritten, prompts, config["models"]["classifier"], config, stages["classify"], cache, classification=True)
    lineage += history
    if jobs or quality_pending:
        return stop(jobs, [quality_pending] if quality_pending else [], [])
    labelled = {r["id"]: r for r in labels}
    declining = [r for r in rewritten if labelled[r["id"]]["refusal_warranted"] != "n/a"]
    refusals, refusal_pending = review_stage(declining, config, stages["refusal"], kind="refusal_warranted", rubric="refusal_warranted_judgement")
    if refusal_pending:
        return stop([], [refusal_pending], [])
    feedback = {}
    for row in rewritten:
        row_id = row["id"]
        objections = []
        if not both_accept(quality[row_id]):
            objections += quality[row_id]
        if row_id in refusals and any(v["verdict"] == "UNNEEDED" for v in refusals[row_id]):
            objections += refusals[row_id]
        if objections:
            feedback[row_id] = objections
    to_rewrite = [r for r in rewritten if r["id"] in feedback]
    repaired, jobs, history = write_model_stage(to_rewrite, {r["id"]: repair_prompt(r, feedback[r["id"]], config) for r in to_rewrite},
                                               config["models"]["writer"], config, stages["repair"], cache)
    lineage += history
    if jobs:
        return stop(jobs, [], [])
    revised_quality, revision_pending = review_stage(repaired, config, stages["repair_quality"], kind="training_example", rubric="training_example_judgement")
    if revision_pending:
        return stop([], [revision_pending], [])
    blocked = [{"id": row["id"], "reason": "rewritten response was not accepted by both reviewers", "verdicts": revised_quality[row["id"]]}
               for row in repaired if not both_accept(revised_quality[row["id"]])]
    if blocked:
        return stop([], [], blocked)
    originals = {r["id"]: r for r in rewritten}
    replacements = {r["id"]: {"input_sha256": digest(originals[r["id"]]), "reply": r["segments"][1]["text"]} for r in repaired}
    final = apply_accepted_rewrites(rewritten, replacements)
    blocked = full_read_decisions(final, config["constitution_text"], config["prompt_texts"]["training_example_judgement"],
                                  stages["full_read"], runtime_smoke=config.get("historical_smoke", False))
    if blocked:
        return stop([], [], blocked)
    final = sample_chat_mixture(final, config["mix"])
    validate_chat_rows(final)
    write_jsonl(output / "chat.jsonl", final)
    write_jsonl(output / "lineage.jsonl", lineage)
    status = "smoke_only" if config.get("historical_smoke", False) else "ready"
    manifest = {"status": status, "identity": identity, "build_sha256": run_key, "rows": len(final),
                "sha256": file_sha(output / "chat.jsonl"), "dataset": str(output / "chat.jsonl"),
                "lineage": str(output / "lineage.jsonl"), "resolved_recipe": str(work / "builds" / run_key / "recipe.json"), "stages": {k: str(v) for k, v in stages.items()},
                "note": "Cached generation and content-bound judgements; quality remains an empirical claim, not a smoke-test result."}
    write_json(output / "manifest.json", manifest)
    write_json(work / "pending.json", {"status": status, "model_requests": [], "judgements": [], "blocked_examples": []})
    logger.info("{}: {} rows, sha256={}, {}", status.upper(), len(final), manifest["sha256"], output / "chat.jsonl")
    return manifest
