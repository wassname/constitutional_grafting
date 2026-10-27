"""Saved OpenRouter requests, responses and resumable batches; no work on import. -- PI/Sol"""
import json
import time
import os
from pathlib import Path

from .files import ROOT, digest, write_json


def request_record(model: str, prompt: str | list[dict], parameters: dict, *, attempt=0) -> dict:
    if {"model", "messages"} & parameters.keys():
        raise ValueError("pass messages through request_messages; model must be explicit")
    body = {"model": model, "messages": [{"role": "user", "content": prompt}], **parameters}
    return {"endpoint": "https://openrouter.ai/api/v1/chat/completions", "body": body, "attempt": attempt}


def request_messages(model: str, messages: list[dict], parameters: dict, *, attempt=0) -> dict:
    request = request_record(model, "", parameters, attempt=attempt)
    request["body"]["messages"] = messages
    return request


def request_key(request: dict) -> str:
    return digest(request)


def cache_path(cache: Path, request: dict) -> Path:
    return cache / f"{request_key(request)}.json"


def saved_response(cache: Path, request: dict) -> dict | None:
    path = cache_path(cache, request)
    if not path.exists():
        return None
    record = json.loads(path.read_text())
    if record["request"] != request:
        raise ValueError(f"cache request mismatch: {path}")
    return record


def save_response(cache: Path, request: dict, response: dict, *, provenance: dict) -> dict:
    choice = response["choices"][0]
    if choice["finish_reason"] != "stop" or not choice["message"]["content"]:
        raise ValueError(f"incomplete model response: {choice['finish_reason']}")
    path = cache_path(cache, request)
    record = {"request": request, "response": response, "provenance": provenance}
    if path.exists() and json.loads(path.read_text()) != record:
        raise ValueError(f"refusing to replace saved model response: {path}")
    write_json(path, record)
    return record


def response_text(record: dict) -> str:
    if record["provenance"]["kind"] == "historical_stage_result":
        return record["recorded_text"].strip()
    return record["response"]["choices"][0]["message"]["content"].strip()


def api_headers() -> dict:
    from dotenv import dotenv_values
    key = dotenv_values(ROOT / ".env")["OPENROUTER_API_KEY"]
    return {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}


def claim_request(cache: Path, request: dict, operation: str) -> Path:
    path = cache / "attempts" / f"{request_key(request)}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    # a "sending" claim older than the 600 s request timeout belongs to a killed process; it may have been billed once, retry it
    if path.exists() and json.loads(path.read_text()).get("status") == "sending" and time.time() - path.stat().st_mtime > 900:
        path.unlink()
    with path.open("x") as f:
        f.write(json.dumps({"status": "sending", "operation": operation, "request": request}))
        f.flush()
        os.fsync(f.fileno())
    return path


def send_cached_request(cache: Path, request: dict, *, context: dict) -> dict:
    import httpx
    saved = saved_response(cache, request)
    if saved is not None:
        return saved
    headers = api_headers()
    attempt = claim_request(cache, request, "openrouter_sync")
    response = httpx.post(request["endpoint"], headers=headers, json=request["body"], timeout=600)
    write_json(attempt, {"status": "received", "request": request, "status_code": response.status_code, "raw_body": response.text})
    response.raise_for_status()
    body = response.json()
    with (cache / "api_costs.jsonl").open("a") as f:
        f.write(json.dumps({"key": request_key(request), "cost": body["usage"]["cost"], **context}) + "\n")
    return save_response(cache, request, body, provenance={"kind": "openrouter", "context": context})


def send_pending(workdir: Path, budget_usd: float):
    if budget_usd <= 0:
        raise ValueError("an explicit positive API budget is required")
    pending = json.loads((workdir / "pending.json").read_text())
    spent, completed = 0.0, 0
    for job in pending["model_requests"]:
        request, cache = job["request"], Path(job["cache"])
        if saved_response(cache, request) is not None:
            continue
        if spent + job["cost_ceiling_usd"] > budget_usd:
            raise ValueError(f"remaining budget cannot cover next request; completed={completed}, cost=${spent:.4f}")
        saved = send_cached_request(cache, request, context={"id": job["id"], "stage": job["stage"]})
        cost = saved["response"]["usage"]["cost"]
        spent += cost
        completed += 1
        with (workdir / "api_costs.jsonl").open("a") as f:
            f.write(json.dumps({"key": request_key(request), "id": job["id"], "stage": job["stage"], "cost": cost}) + "\n")
        if cost > job["cost_ceiling_usd"]:
            raise ValueError(f"provider cost ${cost:.4f} exceeded configured request ceiling; response saved, stopped")
    print(f"Saved {completed} responses, cost ${spent:.4f}. Rerun the dataset build to continue.")


def submit_batch(requests: list[dict], cache: Path, batch_dir: Path, budget_usd: float):
    """One durable submission per exact request list; collect it instead of resubmitting."""
    import httpx
    todo = [job for job in requests if saved_response(cache, job["request"]) is None]
    if not todo:
        return None
    if sum(job["cost_ceiling_usd"] for job in todo) > budget_usd:
        raise ValueError("batch request ceilings exceed the explicit budget")
    models = {job["request"]["body"]["model"] for job in todo}
    if len(models) != 1:
        raise ValueError("one model per batch")
    key = digest([job["request"] for job in requests])
    path = batch_dir / f"{key}.json"
    if path.exists():
        raise ValueError(f"batch submission already recorded; collect or reconcile {path}")
    headers = api_headers()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x") as f:
        f.write(json.dumps({"status": "submitting", "jobs": todo, "cache": str(cache)}))
    for job in todo:
        claim_request(cache, job["request"], f"batch:{path}")
    payload = {"endpoint": "/v1/chat/completions", "model": models.pop(), "requests": [
        {"custom_id": request_key(job["request"]), "body": {k: v for k, v in job["request"]["body"].items() if k != "model"}} for job in todo]}
    response = httpx.post("https://openrouter.ai/api/v1/batches", headers=headers, json=payload, timeout=300)
    write_json(path, {"status": "received", "jobs": todo, "cache": str(cache), "status_code": response.status_code, "raw_body": response.text})
    response.raise_for_status()
    write_json(path, {"status": "submitted", "jobs": todo, "cache": str(cache), "batch": response.json()})
    return path


def collect_batch(path: Path):
    import httpx
    record = json.loads(path.read_text())
    response = httpx.get(f"https://openrouter.ai/api/v1/batches/{record['batch']['id']}", headers=api_headers(), timeout=120)
    response.raise_for_status()
    body = response.json()
    write_json(path.parent / "results" / path.name, body)
    jobs = {request_key(job["request"]): job for job in record["jobs"]}
    for result in body.get("results") or []:
        job = jobs[result["custom_id"]]
        if saved_response(Path(record["cache"]), job["request"]) is not None:
            continue
        response_body = result["response"]
        if "body" in response_body:
            response_body = response_body["body"]
        save_response(Path(record["cache"]), job["request"], response_body,
                      provenance={"kind": "openrouter_batch", "batch": record["batch"]["id"]})
        with (Path(record["cache"]) / "api_costs.jsonl").open("a") as f:
            f.write(json.dumps({"key": request_key(job["request"]), "cost": response_body["usage"]["cost"], "batch": record["batch"]["id"]}) + "\n")
    print(f"batch {record['batch']['id']}: {body['status']}")
