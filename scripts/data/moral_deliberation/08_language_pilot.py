#!/usr/bin/env python3
"""One fresh case in English/Ancient Greek/Latin; preserve whole-pair translations. -- PI/OpenAI (Sol)"""
import argparse
import json
import urllib.request
from pathlib import Path

from common import ROOT, CONSTITUTION, by_id, cached_call, price_ceiling, read_jsonl, cached_response
from constitutional_grafting.data.files import digest, write_json
from constitutional_grafting.data.model_requests import request_messages, request_key

KIMI = "moonshotai/kimi-k3.1-pro"
LANGUAGES = ["English", "Ancient Greek", "Latin"]
TRANSLATE = ("Translate the supplied JSON's notes and reply into English, retaining exactly those two keys. "
             "Translate the entire pair faithfully, preserving every factual claim, assumption, uncertainty, identity, reason, "
             "decision and proposed action, even when mistaken. Do not answer the original question, correct errors, add grounds, "
             "polish the reasoning, remove repetition or strengthen the advice. The notes must remain the supplied notes, "
             "not a retrospective explanation. Return only valid JSON. This is a language experiment for constitutional "
             "virtue-ethics alignment; only source-faithful pairs may later be considered for fine-tuning. Your own working notes are not the translated target.")


def run(work: Path, seeds_path: Path, *, cap_usd=1.5, offline=False):
    work.mkdir(parents=True, exist_ok=True)
    seeds = read_jsonl(seeds_path)
    selected = next(row for row in seeds if row["source"] == "machiavelli")
    if selected["review_status"] != "source_checked_for_language_pilot":
        raise ValueError("Read and source-check the full chosen seed before this paid experiment")
    constitution = CONSTITUTION.read_text()
    identity = {"seed": selected, "constitution": constitution, "translation_prompt": TRANSLATE,
                "languages": LANGUAGES, "model": KIMI, "generation_effort": "high", "cap_usd": cap_usd}
    manifest = work / "manifest.json"
    if manifest.exists() and json.loads(manifest.read_text())["identity_sha256"] != digest(identity):
        raise ValueError("experiment inputs changed; freeze a new named experiment")
    write_json(manifest, {"identity_sha256": digest(identity), "identity": identity, "status": "in_progress", "training_release": False})
    meta_path = work / "models.json"
    if not meta_path.exists():
        if offline:
            raise ValueError("offline mode needs the frozen model metadata")
        with urllib.request.urlopen("https://openrouter.ai/api/v1/models", timeout=30) as response:
            listing = json.load(response)["data"]
        write_json(meta_path, {r["id"]: r for r in listing if r["id"] in {KIMI, "anthropic/claude-haiku-5.5"}})
    models = json.loads(meta_path.read_text())
    results = []

    def call(label, messages, effort):
        request = request_messages(KIMI, messages, {"provider": {"only": ["Moonshot AI"], "allow_fallbacks": False, "require_parameters": True},
                                   "max_tokens": 16000, "usage": {"include": True}, "reasoning": {"effort": effort, "exclude": False}})
        cached = cached_response(request)
        if offline and cached is None:
            raise ValueError(f"offline cache miss: {label}")
        response = cached_call(work, request, cap_usd=cap_usd, reserve_usd=price_ceiling(request, models[KIMI]))
        choice = response["choices"][0]
        print(f"{label}: {'cached, $0 new API' if cached else '$' + str(response['usage']['cost'])}; {choice['finish_reason']}", flush=True)
        return request_key(request), response

    for language in LANGUAGES:
        control = (f"Use {language} throughout, including any pre-answer working notes and the final reply. "
                   "Keep proper names and numbers identifiable. Answer the current user normally; no special explanatory format is required.")
        key, response = call(language, [{"role": "system", "content": constitution}, {"role": "system", "content": control}] + selected["messages"], "high")
        message = response["choices"][0]["message"]
        if not message["reasoning"]:
            raise ValueError("complete source pair requires provider-exposed notes")
        pair = {"notes": message["reasoning"], "reply": message["content"]}
        results.append({"id": language, "kind": "native_generation", "language_requested": language, "source_id": selected["id"],
                        "request_key": key, "effort_requested": "high", "pair": pair, "served_model": response["model"], "provider": response["provider"]})
        write_json(work / "samples.json", results)
        if language != "English":
            tkey, translation = call(language + " → English", [{"role": "system", "content": TRANSLATE},
                                     {"role": "user", "content": json.dumps(pair, ensure_ascii=False)}], "high")
            text = translation["choices"][0]["message"]["content"]
            translated = json.loads(text)
            if set(translated) != {"notes", "reply"} or not all(isinstance(t, str) and t for t in translated.values()):
                raise ValueError("translation must contain both complete source fields")
            results.append({"id": language + "_translated", "kind": "translated_pair", "source_request_key": key,
                            "request_key": tkey, "pair": translated, "approval": "unreviewed; not native English deliberation"})
            write_json(work / "samples.json", results)
    write_json(manifest, {"identity_sha256": digest(identity), "identity": identity, "status": "generated_unreviewed", "training_release": False})
    print(work / "samples.json")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("work", type=Path)
    ap.add_argument("--seeds", type=Path, required=True)
    ap.add_argument("--cap-usd", type=float, default=1.5)
    ap.add_argument("--offline", action="store_true")
    args = ap.parse_args()
    run(args.work, args.seeds, cap_usd=args.cap_usd, offline=args.offline)
