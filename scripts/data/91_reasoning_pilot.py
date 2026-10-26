#!/usr/bin/env python3
"""API-only, resumable execution of the approved 20261026 reasoning pilot.

Run with uv run --no-sync python scripts/data/91_reasoning_pilot.py --help.
`report` rebuilds the reader reports from frozen cache without network access.
Only writes the pilot directory. P3 primer replays the completed retry cache;
no further Anthropic call is allowed. Requests are synchronous and fail closed on
uncertain billing; no automatic retries or model substitutions.
-- PI/Sol (worker)
"""
import argparse
import collections
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import random
import re
import threading
from concurrent.futures import ThreadPoolExecutor
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "slop/data/20261026_reasoning_pilot"
SIGN = "-- PI/Sol (worker)"
TEACHERS = {"kimi": "moonshotai/kimi-k3.1-pro", "mimo": "xiaomi/mimo-v2.6-flash", "glm": "z-ai/glm-5.3"}
GUIDES = {"P1": TEACHERS["kimi"], "P2": "z-ai/glm-5.3"}
CONDITION_NAMES = {"P0": "no_guide", "P1": "kimi_guide", "P2": "glm_guide", "P3": "opus_guide"}
CONDITIONS = tuple(CONDITION_NAMES)
READ_SIGN = "-- PI/Sol (reader)"


def condition_code(name):
    # Legacy codes are immutable cache IDs, not report labels.
    return next((code for code, label in CONDITION_NAMES.items() if name == label), name)


def guide_file(condition, revised=False):
    label = CONDITION_NAMES[condition]
    if condition == "P3":
        return OUT / "guides/opus_guide.md"
    revised_name = label + ("_rejected" if condition == "P2" else "")
    return OUT / (f"guides/{revised_name}.md" if revised else f"history/{label}_original.md")
REVIEWER = "deepseek/deepseek-v4.1-flash-1017"
QUOTAS = {"seeded_dilemma": 4, "identity": 3, "ordinary": 3, "difficult_high": 3,
          "role_dilemma": 2, "ask_first": 2, "proportion": 2, "repair": 1}
CAP = 15.0
LEDGER_LOCK = threading.Lock()
IN_FLIGHT: set[str] = set()  # calls of this process now awaiting a response
WORKERS = int(os.environ.get("PILOT_WORKERS", "10"))
MAX_TOKENS = 12000  # 6000 let Kimi's native reasoning use the whole budget (P0_kimi_owned_15); rows that stopped under 6000 are unaffected


def load(path):
    return json.loads(path.read_text())


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def rows(path):
    return [json.loads(x) for x in path.read_text().splitlines()] if path.exists() else []


def conversation(row):
    """Decode the actual serialized training prompt, excluding its final target."""
    prefix = "".join(s["text"] for s in row["segments"][:-1])
    assert row["segments"][-1]["label"] is True
    parts = re.findall(r"<\|im_start\|>(system|user|assistant)\n(.*?)(?:<\|im_end\|>|\Z)", prefix, re.S)
    assert parts and parts[-1][0] == "assistant"
    assert not re.sub(r"<think>\s*</think>", "", parts[-1][1]).strip()
    messages = [{"role": role, "content": text} for role, text in parts[:-1]]
    assert messages[-1]["role"] == "user"
    return messages


def prepare():
    if (OUT / "selection.json").exists():
        raise RuntimeError("Selection already frozen; refusing overwrite")
    source = ROOT / "data/train/run10/chatr12.jsonl"
    candidates = rows(source)
    rng = random.Random(0)
    selected = []
    for shape, n in QUOTAS.items():
        group = [(i, r) for i, r in enumerate(candidates) if r["shape"] == shape]
        for i, r in rng.sample(group, n):
            selected.append({"index": i, "id": r["id"], "shape": shape,
                             "messages": conversation(r), "original_row": r})
    frozen = (ROOT / "slop/eval/run8/items.jsonl").read_text()
    # Exclusion check only; held-out text is never supplied to any model.
    for r in selected:
        for m in r["messages"]:
            if m["role"] == "user":
                assert m["content"] not in frozen, "Frozen evaluation overlap"
    dump(OUT / "selection.json", {"seed": 0, "source": str(source.relative_to(ROOT)),
         "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
         "selection_method": "random.Random(0), sample each shape in approved quota order, source order within shape",
         "quotas": QUOTAS, "rows": selected, "signature": SIGN})
    # This random subset is fixed before any generations are inspected.
    ids = [f"{teacher}_{arm}_{i:02d}" for teacher in TEACHERS for arm in ("free", "cite") for i in range(20)]
    dump(OUT / "review_selection.json", {"seed": 0, "ids": random.Random(0).sample(ids, 10), "signature": SIGN})
    print("Frozen 20 rows and independent random 10 IDs")


def require_complete(result):
    """A billed, saved response is not necessarily a usable completion."""
    if "error" in result or not result.get("choices"):
        raise RuntimeError(f"API error recorded: {result.get('error')}")
    choice = result["choices"][0]
    if choice.get("finish_reason") != "stop" or choice["message"].get("refusal"):
        raise RuntimeError("Incomplete/refused response preserved in raw.jsonl; no retry or downstream use")
    return result


def visible_sections(message):
    """Strict forward order for the main written-deliberation condition."""
    match = re.fullmatch(r"\s*<reasoning>(.+?)</reasoning>\s*<answer>(.+?)</answer>\s*", message.get("content") or "", re.S)
    if not match or not all(x.strip() for x in match.groups()):
        raise RuntimeError("Expected nonempty reasoning then answer; preserve raw and inspect before retrying")
    return tuple(x.strip() for x in match.groups())


def reading_sections(message):
    """Reading-only tag repair; never promote the provider's native reasoning.

    Only the approved missing answer tags and dropped leading '<' are repaired.
    The strict generation validator remains unchanged.
    """
    text = message.get("content") or ""
    try:
        reason, answer = visible_sections(message)
        return {"format": "strict_pass", "reasoning": reason, "answer": answer, "repairs": []}
    except RuntimeError:
        pass
    repairs = []
    if text.lstrip().startswith("reasoning>"):
        text = "<" + text.lstrip()
        repairs.append("dropped leading <")
    match = re.fullmatch(r"\s*<reasoning>(.+?)</reasoning>\s*(.*?)\s*", text, re.S)
    if match and match[1].strip():
        answer = match[2]
        if answer.startswith("<answer>"):
            answer = answer[len("<answer>"):]
        else:
            repairs.append("missing <answer>")
        if answer.endswith("</answer>"):
            answer = answer[:-len("</answer>")]
        else:
            repairs.append("missing </answer>")
        if answer.strip() and not re.search(r"</?(?:reasoning|answer)>", answer):
            return {"format": "format_repaired", "reasoning": match[1].strip(), "answer": answer.strip(), "repairs": repairs}
    return {"format": "format_failure", "reasoning": "", "answer": "", "repairs": [],
            "failure": "No complete visible reasoning followed by a nonempty answer; native reasoning is not the deliverable."}


def request(call_id, model, messages, max_tokens, reasoning=None):
    if model not in {*TEACHERS.values(), *GUIDES.values(), REVIEWER}:
        raise ValueError("Model not approved by the revised pilot; Anthropic calls are prohibited")
    OUT.mkdir(parents=True, exist_ok=True)
    with LEDGER_LOCK:  # file flock is held once per process (main); threads share this lock for ledger/raw
        raw = rows(OUT / "raw.jsonl")
        if any(r["call_id"] == call_id for r in raw):
            return require_complete(next(r["response"] for r in raw if r["call_id"] == call_id))
        ledger_path = OUT / "budget.json"
        ledger = load(ledger_path) if ledger_path.exists() else {"cap_usd": CAP, "calls": [], "signature": SIGN}
        if any(c["status"] != "completed" and c.get("billing_resolution") != "full_reserve_charged" and c["call_id"] not in IN_FLIGHT for c in ledger["calls"]):
            raise RuntimeError("Unresolved request/billing; inspect budget.json before continuing")
        models = load(OUT / "model_preflight_revision.json")["matched_models"]
        meta = next(m for m in models if m["id"] == model)
        # One UTF-8 byte per input token is deliberately conservative, with
        # additional framing overhead. No cache discount assumed.
        reserve = (sum(len(m["content"].encode()) for m in messages) + 4096) * float(meta["pricing"]["prompt"]) + max_tokens * float(meta["pricing"]["completion"])
        spent = sum(c.get("cost_usd", c["reserve_usd"]) for c in ledger["calls"])
        if spent + reserve > CAP:
            raise RuntimeError(f"Budget would exceed cap: spent={spent}, reserve={reserve}")
        payload = {"model": model, "messages": messages, "max_tokens": max_tokens,
                   "usage": {"include": True}, "provider": {"allow_fallbacks": False}}
        if reasoning is not None:
            payload["reasoning"] = reasoning
        dump(OUT / "prompts" / (call_id + ".json"), {"request": payload, "signature": SIGN})
        entry = {"call_id": call_id, "model": model, "status": "pending", "reserve_usd": reserve,
                 "time_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
        ledger["calls"].append(entry)
        dump(ledger_path, ledger)
        IN_FLIGHT.add(call_id)
    if True:  # HTTP call outside the lock so rows of a cell run concurrently
        req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions",
              data=json.dumps(payload).encode(), headers={"Authorization": "Bearer " + os.environ["OPENROUTER_API_KEY"], "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=150) as response:
                result = json.load(response)
        except urllib.error.HTTPError as exc:
            with LEDGER_LOCK:
                ledger = load(ledger_path)
                [c for c in ledger["calls"] if c["call_id"] == call_id and c["status"] == "pending" and "billing_resolution" not in c][-1]["error"] = {"status": exc.code, "body": exc.read().decode()}
                dump(ledger_path, ledger)
            raise
    with LEDGER_LOCK:
        ledger = load(ledger_path)
        entry = [c for c in ledger["calls"] if c["call_id"] == call_id and c["status"] == "pending" and "billing_resolution" not in c][-1]  # this attempt, not an earlier charged one
        cost = result.get("usage", {}).get("cost")
        record = {"call_id": call_id, "requested_model": model, "response": result, "signature": SIGN}
        with (OUT / "raw.jsonl").open("a") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        if cost is None or not isinstance(cost, (int, float)) or cost < 0:
            raise RuntimeError("Missing/invalid actual cost; request remains pending")
        entry.update(status="completed", cost_usd=cost, served_model=result.get("model"), provider=result.get("provider"))
        dump(ledger_path, ledger)
        IN_FLIGHT.discard(call_id)
        print(call_id, "provider=", result.get("provider"), "cost=", cost, "finish=", result.get("choices", [{}])[0].get("finish_reason"), flush=True)
        return require_complete(result)


def data_rules():
    snapshot = OUT / "prompts/data_rules_snapshot.md"
    if snapshot.exists():
        return snapshot.read_text().removesuffix("\n\n" + SIGN + "\n")
    return (ROOT / "AGENTS.md").read_text().split("## Data rules\n")[1].split("## Dose sweeps")[0]


def preflight():
    required = sorted({*TEACHERS.values(), *GUIDES.values(), REVIEWER})
    with urllib.request.urlopen("https://openrouter.ai/api/v1/models", timeout=30) as response:
        listing = json.load(response)["data"]
    matched = [m for m in listing if m["id"] in required]
    missing = sorted(set(required) - {m["id"] for m in matched})
    dump(OUT / "model_preflight_revision.json", {"required_models": required,
         "missing_required_models": missing, "matched_models": matched,
         "listing_count": len(listing), "time_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
         "signature": SIGN})
    if missing:
        raise RuntimeError(f"Required model unavailable: {missing}")
    print("All revised model IDs listed")


def freeze_review():
    path = OUT / "review_selection_revision.json"
    if path.exists():
        raise RuntimeError("Revision review selection already frozen")
    dump(path, {"seed": 0, "population": "160 direct owned-values (P0/P1 all3 teachers; P3 Kimi/GLM only) + 40 classical English translations; before main-study output; smoke cells excluded",
                "ids": random.Random(0).sample(study_ids(), 10), "signature": SIGN})


def primer(condition, revise=False):
    if condition == "P3":
        if revise:
            raise ValueError("Opus retry already consumed; no further Anthropic request approved")
        # The one honest-purpose retry was executed by const_v2. Replay that
        # preserved result, never send a third request or switch providers.
        cached = load(OUT / "history/opus_guide_retry_raw.json")
        result = require_complete(cached["response"])
        guide_file("P3").write_text(result["choices"][0]["message"]["content"])
        print("Replayed completed honest-purpose Opus retry; $0, no API call")
        return
    const = (ROOT / "constitution/v4.md").read_text()
    rules = data_rules()
    user = """Write a 1–2 page primer teaching good in-character moral reasoning for Musonius, using the constitution and project data rules below. The reasoning must move forward from the situation to a decision, not rationalise an answer supplied beforehand. Teach who is affected, facts and uncertainty, plausible alternatives, what decides it, honest disagreement, ordinary help without moralising. Avoid rules without reasons, virtue narration, refusing to look moral, invented facts, rationalising fixed answers, and reasoning inconsistent with the answer or tools. Distinguish useful visible synthetic deliberation from a claim of faithful private introspection. Include 2–3 short worked examples with brief visible reasoning and an answer. Use ONLY these fresh scenarios for examples: (1) convert 2.5 metres to centimetres for a craft project; (2) a community telescope club has one observing slot, a newcomer and a returning member both request it, and there is no prior booking policy; (3) I mistakenly told a neighbour a parcel was delivered Tuesday but now the tracking shows Wednesday; help me correct the message. Do not introduce other scenarios or quote training/evaluation cases. Use general reusable guidance rather than case-specific rules. The primer will guide two teachers, one reasoning without document references and one allowed accurate citations; it must work for both. Return only the primer.\n\nCONSTITUTION\n""" + const + "\n\nPROJECT DATA RULES\n" + rules
    user = user.replace("1–2 page primer", "short teacher's guide: a few paragraphs plus three brief worked examples")
    user += "\n\nThe guide is case law, not a script to copy. Teach applying the principles and Musonius's own identity to new cases; examples are conditional, not extra rules. Keep the whole guide under 900 words."
    call_id = f"guide_{condition}"
    if condition == "P1" and any(c["call_id"] == call_id and c.get("billing_resolution") == "full_reserve_charged" for c in load(OUT / "budget.json")["calls"]):
        call_id += "_retry1"
    messages = [{"role": "user", "content": user}]
    if revise:
        feedback = "Revise your guide once, keeping it short. General review objections: do not mandate a checklist or multiple live alternatives for determinate ordinary tasks; do not present a known mistake as a genuine competing option. Derive conventions from the actual context, not universal bans or unsupported universal claims. Preserve the supplied scenario's tense and facts exactly; do not infer missing facts, overstate evidence, or claim checks not actually performed. Keep useful worked examples conditional, with substantive reasons rather than rules without reasons. Return only the revised guide, not a discussion of this review."
        original = guide_file(condition).read_text().removesuffix("\n\n" + SIGN + "\n")
        messages += [{"role": "assistant", "content": original}, {"role": "user", "content": feedback}]
        call_id = f"guide_{condition}_revised"
    result = request(call_id, GUIDES[condition], messages, 4000, {"effort": "low", "exclude": False})
    guide_file(condition, revised=revise).write_text(result["choices"][0]["message"]["content"] + "\n\n" + SIGN + "\n")


def teacher_reasoning(teacher):
    # GLM requires native reasoning; Kimi-off leaked planning in the smoke.
    # Keep native fields for review, but train only the explicit written sections.
    return {"effort": "low", "exclude": False} if teacher in ("kimi", "glm") else {"enabled": False}


def generation_id(condition, teacher, index, classical=False):
    return f"{condition}_{teacher}_owned_{index:02d}" + ("_classical_en" if classical else "")


def study_ids():
    return ([generation_id(p, t, i) for p in ("P0", "P1") for t in TEACHERS for i in range(20)]
            + [generation_id("P3", t, i) for t in ("kimi", "glm") for i in range(20)]
            + [generation_id("P1", t, i, True) for t in ("kimi", "glm") for i in range(20)])


def generate(condition, teacher, arm, start, count, native=False, classical=False):
    if not (0 <= start < 20 and 1 <= count <= 20 and start + count <= 20):
        raise ValueError("Requested range must stay inside the fixed 20 rows")
    if native:
        raise ValueError("Separate native side comparison superseded by owned-values revision")
    if classical and (condition != "P1" or teacher not in ("kimi", "glm") or arm != "owned"):
        raise ValueError("Classical-language arm is approved only for P1 Kimi/GLM owned values")
    primer_text = ""
    if condition != "P0":
        approval = load(OUT / "guide_read.json")[CONDITION_NAMES[condition]]
        if approval.get("reader_requires_revision"):
            raise RuntimeError("Current reader requires guide fixes and fresh prompt-package approval before generation")
        guide_path = OUT / approval["file"]
        if not approval["accepted"] or approval["sha256"] != hashlib.sha256(guide_path.read_bytes()).hexdigest():
            raise RuntimeError("Guide has not passed executor full-read approval")
        guide = guide_path.read_text().removesuffix("\n\n" + SIGN + "\n")
        intro = guide.split("## Worked example 1:")[0]
        examples = re.findall(r"\*\*Visible reasoning:\*\* (.*?)\n\n\*\*Answer:\*\* (.*?)(?=\n\n## Worked example|\Z)", guide, re.S)
        if condition == "P3":
            intro = guide.split("## Worked examples")[0]
            worked = guide.split("## Worked examples")[1].split("\n\nIf you'd like")[0]
            examples = re.findall(r"\*Reasoning:\* (.*?)\n\n\*Answer:\*\s*(.*?)(?=\n\n\*\*\d|\Z)", worked, re.S)
        seeds = ["Convert 2.5 metres to centimetres for a craft project.",
                 "A community telescope club has one observing slot; a newcomer and a returning member both request it, and there is no prior booking policy.",
                 "I mistakenly told a neighbour a parcel was delivered Tuesday but now tracking shows Wednesday; help me correct the message."]
        if len(examples) != 3:
            raise RuntimeError("Expected three complete reviewed demonstrations")
        demonstrations = "\n\n".join(f"<example>\n<user>{seed}</user>\n<reasoning>{reason}</reasoning>\n<answer>{answer}</answer>\n</example>" for seed, (reason, answer) in zip(seeds, examples))
        primer_text = "\n\nTEACHER'S GUIDE\n" + intro + "\nDEMONSTRATIONS\n" + demonstrations
    selection = load(OUT / "selection.json")["rows"]
    const = (ROOT / "constitution/v4.md").read_text()
    instruction = """You are Musonius, as defined by the constitution above. Continue the supplied conversation. Do a full analysis of the situation and the relevant values, correctness and helpfulness before producing the answer. Your reasoning should feel like a model that has fully internalized the constitution's values and philosophy, not like you are reciting a policy document. Derive your decision from the situation before answering the final user. You have NOT been given an existing target answer. Do not start from a fixed decision and justify it: weigh the live considerations, including anything that could change your decision, then reach it. Provide short, concrete visible deliberation: usually short, as long as the case needs; much shorter for ordinary tasks. Identify only relevant facts, affected people, uncertainty, alternatives and what decides the choice; do not turn this into a mandatory checklist or sermon. Preserve facts and do not invent missing information. Consider whether details are being oversimplified or misrepresented in ways that could confuse. Avoid repeated phrases, stereotyped moral summaries and a repeated reasoning structure; let the particular task determine the response. Make any tool-action proposal match the decision; no tools are actually available in this pilot. Do not claim this synthetic visible reasoning is a faithful introspective transcript. Write the deliberation FIRST in <reasoning>...</reasoning>, then <answer>...</answer> in the same generation, so the answer follows it. Always provide a final answer; keep it concise unless the task needs more.\n"""
    if arm == "cite":
        instruction += "FORMAT SMOKE ONLY, NOT MAIN STUDY: Accurate optional constitutional citations are allowed, never substitutes for reasons."
    elif arm == "owned":
        instruction += "OWNED VALUES: Reason as what you believe, not as obedience to outside instructions. NEVER mention a guide, primer, its examples, or instructions. You may mention your constitution only as your own commitments (for example, 'I hold that...'), never as an external authority ('the constitution says...'), and never cite its section numbers. Show the substantive reasons rather than narrating virtue."
    else:
        raise ValueError("Separate citation-free arm was superseded by owned-values revision")
    if classical:
        instruction += "\nCLASSICAL LANGUAGE: First choose Ancient Greek or Latin. Return <language>Ancient Greek</language> or <language>Latin</language>, then <reasoning>...</reasoning> and <answer>...</answer> entirely in that chosen language. Do not include an English version yet. Preserve all names, numbers, facts and uncertainty; transliterate modern terms only as necessary."
    system = const + "\n\nPROJECT DATA RULES\n" + data_rules() + primer_text + "\n\nTASK\n" + instruction
    def one(i):
        cid = generation_id(condition, teacher, i)
        if arm == "cite":
            cid = f"{condition}_{teacher}_cite_{i:02d}"
        if classical:
            cid += "_classical_source"
        result = request(cid, TEACHERS[teacher], [{"role": "system", "content": system}] + selection[i]["messages"], MAX_TOKENS, teacher_reasoning(teacher))
        msg = result["choices"][0]["message"]
        if classical:
            match = re.fullmatch(r"\s*<language>(Ancient Greek|Latin)</language>(.*)", msg.get("content") or "", re.S)
            if not match:
                raise RuntimeError("Classical language label missing/invalid; inspect raw")
            language, content = match.groups()
            visible_sections({"content": content})
            translate(condition, teacher, i, language, msg["content"])
        else:
            visible_sections(msg)
        if teacher == "mimo" and msg.get("reasoning"):
            raise RuntimeError("Provider returned native reasoning despite disabled request; inspect settings")
    with ThreadPoolExecutor(WORKERS) as pool:
        list(pool.map(one, range(start, start + count)))  # re-raises the first failure after running the cell


def translate(condition, teacher, index, language, source):
    instruction = """Translate the supplied visible deliberation and answer into English faithfully. Preserve their meaning, argument, uncertainty, facts, names, numbers and decision. Keep a plain, terse style; do not add moral commentary, new reasons, factual repairs, constitutional or guide references, or embellishments. This is translation, not a new answer. Return only <reasoning>...</reasoning> followed by <answer>...</answer>. Do not add a language label. The source reasoning must remain first and its answer second."""
    result = request(generation_id(condition, teacher, index, True), TEACHERS[teacher],
                     [{"role": "system", "content": instruction}, {"role": "user", "content": f"Translate from {language}:\n" + source}],
                     MAX_TOKENS, teacher_reasoning(teacher))
    visible_sections(result["choices"][0]["message"])


def review():
    selected = load(OUT / "selection.json")["rows"]
    raw = {r["call_id"]: r for r in rows(OUT / "raw.jsonl")}
    packet = []
    for cid in load(OUT / "review_selection_revision.json")["ids"]:
        index = int(re.search(r"_owned_(\d{2})", cid).group(1))
        r = selected[index]
        case = {"id": cid, "conversation": r["messages"], "existing_answer": r["original_row"]["segments"][-1]["text"]}
        if cid not in raw:
            case["status"] = "not_generated; preserve frozen selection; do not score or replace"
            packet.append(case)
            continue
        message = raw[cid]["response"]["choices"][0]["message"]
        case["generation"] = {"content": message.get("content")}
        case["reading_parse"] = reading_sections(message)
        if cid.endswith("_classical_en"):
            case["classical_source"] = {"content": raw[cid.replace("_classical_en", "_classical_source")]["response"]["choices"][0]["message"].get("content")}
            case["direct_english"] = {"content": raw[cid.removesuffix("_classical_en")]["response"]["choices"][0]["message"].get("content")}
        packet.append(case)
    checklist = """Independently review all 10 cases below IN FULL without executor verdicts. For each ID: reasoning leads to answer (yes/partly/no); values reasoning vs rule citation; invented constitution quotes/section numbers; virtue narration; refusal that only looks moral; facts preserved; tool actions match decision (N/A if no actions); answer quality vs existing answer (better/same/worse and why). Flag decisions announced before weighing or omitted considerations that could change them. The written <reasoning> and <answer> must embody owned values: never mention a guide/primer, its examples, instructions, authority-style 'constitution says', or section numbers. Own commitments are allowed. Count these failures; distinguish them from instruction-talk in the separately retained NATIVE reasoning field, which is NOT the training target. Check copied demonstration phrases and repeated structures rather than rewarding length. For classical-language cases compare the English translation against its original-language source for meaning, facts, uncertainty and decision, and against direct English for reasoning quality (primary) and style (secondary). Do not assume terse style means better reasoning. Quote evidence for every defect. Distinguish speculation from supplied facts. No tools are available. End with aggregate counts. This is data-quality review, not proof of faithful introspection or learned character.\n\nCONSTITUTION\n"""
    checklist += "\nPARSER DECISION: Accept only the approved reading_parse tag repairs, flagged format_repaired. NO visible reasoning in content is a FORMAT FAILURE; never rescue it with native reasoning. Frozen IDs not generated must be reported missing, never substituted or scored. Review all generated cases. Use meaningful version names P0=no_guide, P1=kimi_guide, P3=opus_guide in your report.\n"
    dump(OUT / "review_packet.json", {"cases": packet, "signature": SIGN})
    # Parent retry: 7000 tokens exhausted in native reasoning with no content;
    # that original response remains cached under __truncated_max7000.
    result = request("independent_review_revision", REVIEWER, [{"role": "system", "content": checklist + (ROOT / "constitution/v4.md").read_text()}, {"role": "user", "content": json.dumps(packet, ensure_ascii=False)}], 32000, {"effort": "low", "exclude": False})
    render_review_reply(result)


def render_review_reply(result):
    require_complete(result)
    content = result["choices"][0]["message"].get("content") or ""
    if not content.strip():
        raise RuntimeError("Completed reviewer returned no visible review")
    history = OUT / "history/independent_reviewer_verbatim.md"
    if not history.exists():
        history.write_text(content + "\n")
    displayed = re.sub(r"\bP[0-3](?=_|\b)", lambda m: CONDITION_NAMES[m[0]], content)
    (OUT / "reviewer_reply.md").write_text(displayed + "\n\nDisplay-name normalization only; provider wording otherwise unchanged. Verbatim provider content is in raw.jsonl/history.\n\n" + READ_SIGN + "\n")


def display_id(cid):
    for code, name in CONDITION_NAMES.items():
        if cid.startswith(code + "_"):
            return name + cid[len(code):]
    return cid


def study_records():
    raw = {r["call_id"]: r for r in rows(OUT / "raw.jsonl")}
    notes = load(OUT / "reader_notes.json")["rows"]
    records = []
    for cid in study_ids():
        match = re.fullmatch(r"(P\d)_(kimi|mimo|glm)_owned_(\d{2})(_classical_en)?", cid)
        code, teacher, index, classical = match.groups()
        index = int(index)
        version = "classical" if classical else CONDITION_NAMES[code]
        record = {"id": display_id(cid), "cache_id": cid, "index": index,
                  "version": version, "teacher": teacher, "generated": cid in raw}
        if cid not in raw:
            source_id = cid.replace("_classical_en", "_classical_source")
            if classical and source_id in raw:
                choice = raw[source_id]["response"]["choices"][0]
                record.update(classical_source=choice["message"].get("content") or "",
                              classical_source_finish=choice.get("finish_reason"))
            records.append(record)
            continue
        source = raw[cid]
        choice = source["response"]["choices"][0]
        message = choice["message"]
        parsed = reading_sections(message)
        note = notes[str(index)][f"{version}/{teacher}"]
        quality, leads, flags, evidence, verdict, *comparison = note
        if parsed["format"] == "format_failure":
            text = message.get("content") or ""
            if not re.search(r"<?reasoning>", text):
                parsed["failure_kind"] = "no_required_reasoning_tag"
            elif "</reasoning>" not in text:
                parsed["failure_kind"] = "incomplete_or_wrong_reasoning_close"
            else:
                parsed["failure_kind"] = "unapproved_surrounding_text_or_boundaries"
        record.update(parsed, content=message.get("content") or "", quality=quality,
                      leads=leads, flags=flags, evidence=evidence, verdict=verdict,
                      classical_comparison=comparison[0] if comparison else None,
                      finish_reason=choice.get("finish_reason"),
                      response_sha256=hashlib.sha256((message.get("content") or "").encode()).hexdigest(),
                      native_field_present=bool(message.get("reasoning")),
                      cost_usd=source["response"].get("usage", {}).get("cost"),
                      served_model=source["response"].get("model"),
                      provider=source["response"].get("provider"),
                      full_visible_content_read=True, native_read=False,
                      owned_values_failure="owned" in flags,
                      rules_without_reasons="rules" in flags,
                      added_refusal="added_refusal" in flags,
                      factual_or_claimed_check_defect=bool({"facts", "claimed_check"} & set(flags)),
                      virtue_narration="narration" in flags,
                      tool_execution="N/A: no tools available; proposed actions assessed in evidence")
        record["retain_candidate"] = parsed["format"] != "format_failure" and not flags and leads == "yes" and choice.get("finish_reason") == "stop"
        if classical:
            source_id = cid.replace("_classical_en", "_classical_source")
            source_choice = raw[source_id]["response"]["choices"][0]
            record["classical_source"] = source_choice["message"].get("content") or ""
            record["classical_source_finish"] = source_choice.get("finish_reason")
            if source_choice.get("finish_reason") != "stop":
                record["retain_candidate"] = False
        records.append(record)
    return records


def markdown_cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


def judgement_table(records):
    lines = ["| Version | Teacher | Planned | Generated | Strict pass | format_repaired | Failed | Retain candidates* | Better / same / worse / unscorable |",
             "|---|---|---:|---:|---:|---:|---:|---:|---|"]
    for version, teacher in dict.fromkeys((r["version"], r["teacher"]) for r in records):
        group = [r for r in records if (r["version"], r["teacher"]) == (version, teacher)]
        generated = [r for r in group if r["generated"]]
        formats = collections.Counter(r["format"] for r in generated)
        quality = collections.Counter(r["quality"] for r in generated)
        lines.append(f"| {version} | {teacher} | {len(group)} | {len(generated)} | {formats['strict_pass']} | {formats['format_repaired']} | {formats['format_failure']} | {sum(r['retain_candidate'] for r in generated)} | " + " / ".join(str(quality[q]) for q in ("better", "same", "worse", "unscorable")) + " |")
    lines += ["| glm_guide (rejected before generation) | not run | 0 | 0 | 0 | 0 | 0 | 0 | not measured |",
              "", "*Retain candidate = complete written pair, approved tag repairs only, forward reasoning, and no reader defect flagged. This is **not a training release** or independent factual certification of every claim. Format failures still received a full visible-content read; their answer-quality judgments do not count as successful reasoning deliverables. Missing rows are not failures and are never substituted."]
    return "\n".join(lines)


def verbatim_record(record, heading="###"):
    lines = [f"{heading} {record['id']}", "", record["content"], "",
             f"**Reader:** {record['verdict']} ({record['quality']} vs existing; {record['format']})."]
    if record.get("classical_source") is not None:
        lines += ["", "<details><summary>Original teacher-written classical source (unmodified)</summary>", "", record["classical_source"], "", "</details>", "", "**Translation/direct-English comparison:** " + record["classical_comparison"]]
    return "\n".join(lines)


def report():
    """Offline rendering: annotations are human/model-reader judgments, not auto-judges."""
    records = study_records()
    generated = [r for r in records if r["generated"]]
    selection = load(OUT / "selection.json")["rows"]
    raw = {r["call_id"]: r for r in rows(OUT / "raw.jsonl")}
    if "independent_review_revision" in raw:
        render_review_reply(raw["independent_review_revision"]["response"])
    # Check every actual saved conversation, not merely a representative prompt.
    systems = collections.defaultdict(set)
    for r in generated:
        payload = load(OUT / "prompts" / (r["cache_id"] + ".json"))["request"]
        if r["version"] != "classical":
            assert payload["messages"][1:] == selection[r["index"]]["messages"], r["id"]
            systems[(r["version"], r["teacher"])].add(payload["messages"][0]["content"])
        else:
            assert r["classical_source"] in payload["messages"][1]["content"], r["id"]
    for r in records:
        if r.get("classical_source"):
            cid = r["cache_id"].replace("_classical_en", "_classical_source")
            payload = load(OUT / "prompts" / (cid + ".json"))["request"]
            assert payload["messages"][1:] == selection[r["index"]]["messages"], cid
            systems[("classical_source", r["teacher"])].add(payload["messages"][0]["content"])
    assert all(len(v) == 1 for v in systems.values()), "System prompt changed within a cell"
    dump(OUT / "reading_manifest.json", {"signature": READ_SIGN,
         "raw_sha256": hashlib.sha256((OUT / "raw.jsonl").read_bytes()).hexdigest(),
         "selection_sha256": hashlib.sha256((OUT / "selection.json").read_bytes()).hexdigest(),
         "coverage": "Every generated main English content read in full with conversation/existing answer; classical English read with full source and matched direct English. Native fields excluded, not rescued or newly claimed read.",
         "records": records})
    table = judgement_table(records)
    introduction = """# Full reasoning-pilot reader record

This is a full visible-deliverable read, not a sample or an automated quality verdict. See [guide audit](guide_audit.md), [summary](summary.md), [full samples](samples.md), [frozen selection](selection.json), and [machine-readable evidence](reading_manifest.json). All 187 generated English rows and their 39 paired classical originals were read with the 20 full conversations and existing chatr12 answers. The untranslatable, length-stopped classical source for row 14 is recorded separately; it is not an English deliverable. Native planning is not a training target and was not used to rescue a failure.

Versions: no_guide, kimi_guide (revised Kimi guide), opus_guide. Classical = kimi_guide, teacher writes Latin first, then the same teacher translates to English. The 39 translated pairs used Latin; the unmatched GLM source for row 14 used Ancient Greek and truncated. Mixed-language/garbled sources are flagged individually. glm_guide was rejected twice and never used. Cache IDs and original request paths retain their historical codes solely to preserve provenance; displayed names are meaningful.

Teachers: Kimi K3.1 Pro, native reasoning low; MiMo V2.6 Flash, native disabled; GLM 5.3, native low (mandatory). Those settings are fixed within teacher, confounded across teachers. Four earlier worker notes are archived, not represented as this reader's native-field read.

**Checks:** forward order versus rationalization; owned values versus authority/guide talk; reasons versus categorical rules/added refusals; supplied facts and claimed checks; virtue narration and moral-looking refusal; answer quality versus existing; copied phrases/repeated structures; source translation and same-teacher direct-English comparison. Flags are not mutually exclusive. `early_decision` flags a conclusion announced before weighing without claiming access to hidden cognition. `rules` is a reader judgment with quotation, not proof of provider-house origin. No tools were available: no real tool execution was requested or claimed by this reader; proposed actions are checked against conclusions in notes. Fabricated checks inside proposed copy are flagged too.

**Parser:** the strict validator is unchanged. The reading-only parser repairs missing closing answer, missing opening answer after complete reasoning, and a dropped leading `<`; combinations are allowed and labeled `format_repaired`. Missing visible reasoning, missing reasoning close, wrong order, or leaked text outside the pair are failures. Failed visible content is still printed/read, not replaced by native reasoning. API truncation is separately retained.

"""
    read_lines = [introduction, table, "\n## Every generated deliverable\n",
                  "| Row | Version / teacher | Format | Leads | Flags | Versus existing | Evidence and one-line verdict |",
                  "|---|---|---|---|---|---|---|"]
    for r in sorted(generated, key=lambda r: (r["index"], r["version"], r["teacher"])):
        read_lines.append("| " + " | ".join(markdown_cell(x) for x in (
            f"[{r['index']:02d}](samples.md#row-{r['index']:02d})", f"{r['version']} / {r['teacher']}",
            r["format"] + (": " + ", ".join(r["repairs"]) if r["repairs"] else ""),
            r["leads"], ", ".join(r["flags"]) or "none observed", r["quality"], r["evidence"] + " **" + r["verdict"] + "**")) + " |")
        if r.get("classical_comparison"):
            read_lines.append("| ↳ source/direct comparison | classical / " + r["teacher"] + " | source finish: " + str(r["classical_source_finish"]) + " | — | — | — | " + markdown_cell(r["classical_comparison"]) + " |")
    missing = [r["id"] for r in records if not r["generated"]]
    read_lines += ["\n## Not generated (not quality failures)\n", "\n".join("- " + cid for cid in missing),
                   "\n## Structure, copying, facts, limitations\n", (OUT / "reading_findings.md").read_text(), "", READ_SIGN]
    (OUT / "read.md").write_text("\n".join(read_lines) + "\n")
    sample_lines = ["# Reasoning pilot — all cached main-study versions", "", table,
                    "", "Full raw visible content follows, including failed formatting. No native reasoning is shown or used as the deliverable. Each prompt excerpt links the full frozen conversation and each generated version links its actual API request; the common system is not cropped in the saved request. Existing answers are comparison targets, never supplied to teachers. Fictional story details are not automatically factual errors.\n"]
    for i, row in enumerate(selection):
        sample_lines += [f'<a id="row-{i:02d}"></a>', f"## Row {i:02d}: {row['id']} — {row['shape']}", "",
                         "**Prompt (cropped; [full conversation and existing target](selection.json)):**"]
        for message in row["messages"]:
            text = message["content"]
            crop = text[:650] + (" … [cropped]" if len(text) > 650 else "")
            sample_lines += ["", f"**{message['role']}**", "", crop]
        sample_lines += ["", "<details><summary>Existing chatr12 answer, comparison only</summary>", "", row["original_row"]["segments"][-1]["text"], "", "</details>"]
        for r in [r for r in records if r["index"] == i]:
            if not r["generated"]:
                sample_lines += [f"\n### {r['id']}\n\n**Not generated.**"]
                if r.get("classical_source"):
                    sample_lines += [f"\nSource attempt ended **{r['classical_source_finish']}**, not a completed English deliverable.",
                                     "\n<details><summary>Untranslated source attempt (full cached content)</summary>\n",
                                     r["classical_source"], "\n</details>"]
                continue
            sample_lines += [f"\n[Actual request](prompts/{r['cache_id']}.json)", verbatim_record(r), ""]
    sample_lines += [READ_SIGN]
    sample_text = "\n".join(sample_lines) + "\n"
    (OUT / "samples.md").write_text(sample_text)
    if len(sample_text.encode()) >= 1_000_000:
        raise RuntimeError("Full samples >=1 MB; apply the approved excerpt/ignore policy before committing")
    # A six-case verbatim appendix is shared by the one-page summary.
    best = ("P3_kimi_owned_15", "P3_kimi_owned_18", "P1_kimi_owned_19")
    worst = ("P1_glm_owned_14", "P0_mimo_owned_09", "P3_glm_owned_10")
    by_id = {r["cache_id"]: r for r in generated}
    examples = ["## Three best and three worst — verbatim appendix", "", "Selected for specific reasoning/failure evidence, not a repeatability estimate. Full written reasoning+answer, unchanged; original tag defects remain visible.\n", "### Best\n"]
    examples += [verbatim_record(by_id[cid], heading="####") for cid in best]
    examples += ["\n### Worst\n"]
    examples += [verbatim_record(by_id[cid], heading="####") for cid in worst]
    summary = (OUT / "summary_findings.md").read_text() + "\n\n" + table + "\n\n" + "\n\n".join(examples) + "\n\n" + READ_SIGN + "\n"
    (OUT / "summary.md").write_text(summary)
    counts = collections.Counter(r["format"] for r in generated)
    print(json.dumps({"generated": len(generated), "missing": len(missing), "format": counts,
                      "retain_candidates": sum(r["retain_candidate"] for r in generated),
                      "samples_bytes": len(sample_text.encode()), "network_calls": 0}, indent=2))


def self_test():
    row = {"segments": [{"text": "<|im_start|>user\nHi<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n", "label": False}, {"text": "SECRET", "label": True}]}
    assert conversation(row) == [{"role": "user", "content": "Hi"}]
    row["segments"][0]["text"] = "<|im_start|>user\nOne<|im_end|>\n<|im_start|>assistant\nEarlier reply<|im_end|>\n<|im_start|>user\nTwo<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
    assert [m["role"] for m in conversation(row)] == ["user", "assistant", "user"]
    assert len(random.Random(0).sample(range(80), 10)) == 10
    complete = {"choices": [{"finish_reason": "stop", "message": {"content": "ok"}}]}
    assert require_complete(complete) is complete
    for bad in ({"error": "blocked"}, {"choices": [{"finish_reason": "content_filter", "message": {"refusal": "blocked"}}]}, {"choices": [{"finish_reason": "length", "message": {}}]}):
        try:
            require_complete(bad)
        except RuntimeError:
            pass
        else:
            raise AssertionError("Incomplete response accepted")
    ids = study_ids()
    assert len(ids) == len(set(ids)) == 200
    for prohibited in ("anthropic/claude-opus-5.5", "unapproved/model"):
        try:
            request("must_not_send", prohibited, [], 1)
        except ValueError:
            pass
        else:
            raise AssertionError("Unapproved model accepted")
    assert len(load(OUT / "selection.json")["rows"]) == 20
    assert visible_sections({"content": "<reasoning>Decide</reasoning><answer>Act</answer>"}) == ("Decide", "Act")
    for text in ("<answer>Act</answer><reasoning>Rationalize</reasoning>", "<reasoning></reasoning><answer>x</answer>", "<reasoning>x</reasoning>"):
        try:
            visible_sections({"content": text})
        except RuntimeError:
            pass
        else:
            raise AssertionError("Malformed/nonforward completion accepted")
    for text, repairs in (
        ("<reasoning>Think</reasoning><answer>Act", ["missing </answer>"]),
        ("<reasoning>Think</reasoning>Act</answer>", ["missing <answer>"]),
        ("<reasoning>Think</reasoning>Act", ["missing <answer>", "missing </answer>"]),
        ("reasoning>Think</reasoning><answer>Act</answer>", ["dropped leading <"]),
        ("reasoning>Think</reasoning>Act", ["dropped leading <", "missing <answer>", "missing </answer>"]),
    ):
        parsed = reading_sections({"content": text})
        assert parsed["format"] == "format_repaired" and parsed["repairs"] == repairs
        assert (parsed["reasoning"], parsed["answer"]) == ("Think", "Act")
    assert reading_sections({"content": "<reasoning>Think</reasoning><answer>Act</answer>"})["format"] == "strict_pass"
    for text in ("", "<answer>Act</answer>", "<reasoning>Think<answer>Act</answer>",
                 "<reasoning>Think</reasoning>", "<answer>Act</answer><reasoning>Think</reasoning>",
                 "planning leaked<reasoning>Think</reasoning><answer>Act</answer>",
                 "reasoning>Think</thinking><answer>Act</answer>"):
        assert reading_sections({"content": text, "reasoning": "native thoughts"})["format"] == "format_failure"
    assert condition_code("opus_guide") == condition_code("P3") == "P3"
    records = study_records()
    assert len(records) == 200
    assert sum(r["generated"] for r in records) == 187
    assert collections.Counter(r["format"] for r in records if r["generated"]) == {"strict_pass": 119, "format_repaired": 28, "format_failure": 40}
    assert len(load(OUT / "review_selection_revision.json")["ids"]) == 10
    assert sum(cid not in {r["cache_id"] for r in records if r["generated"]} for cid in load(OUT / "review_selection_revision.json")["ids"]) == 2
    print("PASS: prompt/target exclusion, multi-turn, model guard, strict validator, five approved reading repairs, native-only/wrong-order/leaked-planning rejection, 187 complete note records, frozen10 with two missing")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["prepare", "preflight", "freeze-review", "primer", "generate", "review", "report", "self-test", "status"])
    parser.add_argument("--condition", type=condition_code, choices=(*CONDITIONS, *CONDITION_NAMES.values()), default="P0")
    parser.add_argument("--teacher", choices=TEACHERS, default="kimi")
    parser.add_argument("--arm", choices=["free", "cite", "owned"], default="owned")
    parser.add_argument("--revise-guide", action="store_true", help="One approved guide revision; preserve originals")
    parser.add_argument("--classical", action="store_true", help="P1 Kimi/GLM classical-language source then same-teacher English translation")
    parser.add_argument("--native", action="store_true", help="Approved Kimi native-reasoning side comparison")
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--count", type=int, default=1)
    args = parser.parse_args()
    lock = (OUT / "budget.lock").open("w")
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)  # one pilot process at a time; threads inside it share LEDGER_LOCK
    if args.stage == "prepare": prepare()
    elif args.stage == "preflight": preflight()
    elif args.stage == "freeze-review": freeze_review()
    elif args.stage == "primer":
        if args.condition == "P0": parser.error("P0 has no guide")
        primer(args.condition, args.revise_guide)
    elif args.stage == "generate": generate(args.condition, args.teacher, args.arm, args.start, args.count, args.native, args.classical)
    elif args.stage == "review": review()
    elif args.stage == "report": report()
    elif args.stage == "self-test": self_test()
    else:
        ledger = load(OUT / "budget.json")
        print(json.dumps({"calls": len(ledger["calls"]), "spent_usd": sum(c.get("cost_usd", c["reserve_usd"]) for c in ledger["calls"]), "pending": [c["call_id"] for c in ledger["calls"] if c["status"] != "completed" and c.get("billing_resolution") != "full_reserve_charged"], "historical_full_reserve_charged": [c["call_id"] for c in ledger["calls"] if c.get("billing_resolution") == "full_reserve_charged"]}, indent=2))


if __name__ == "__main__":
    main()
