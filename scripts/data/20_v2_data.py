# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "loguru"]
# ///
"""Data pipeline v2 (slop/specs/20261008_data_pipeline_v2.md): one writer, one checker, one revision.

  item -> writer (Haiku 5.5, sees the whole constitution) -> checks -> if flagged: writer revises once with the notes -> checks -> keep/drop

labels: SFT answers to prompt pools (data/prompts/<pool dir>). The writer also sees the bare target model's answer as a draft.
        Checks: comparative judge vs that bare answer (deepseek-v4-flash, both orders, quotes verified) + Jev (both orders) + code.
docs:   documents for grafting. Checks: deepseek-v4-flash reads the document against the constitution (quotes verified) + code.

Usage: uv run scripts/data/20_v2_data.py labels <pool dir> <out name> [n_per_pool]
       uv run scripts/data/20_v2_data.py docs <pool dir> <out name> <n_docs>
Writes data/{sft,corpus}/<out name>/ (gitignored): items.jsonl (everything), train.jsonl (kept), report.md.
"""
import json
import os
import random
import re
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx
from loguru import logger

sys.path.insert(0, str(Path(__file__).parent))
import constitution as C  # noqa: E402
from judge import norm, openrouter_key  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
NAME = C.NAME
WRITER = os.environ.get("WRITER", "anthropic/claude-haiku-5.5")  # wassname 2026-10-08: "ok great lets use haiku 5.5"
TARGET = "google/gemma-4-31b-it"
CHECKER = os.environ.get("CHECKER", "~deepseek/deepseek-flash-latest")  # wassname: "yes use"; served deepseek-v4.1-flash on 2026-10-08; served model logged per run
JEV = "typesafe/jev-1.13"
SEED = int(os.environ.get("SEED", "0"))
OPEN_PROVIDER = {"provider": {"quantizations": ["fp8", "int8", "bf16", "fp16"], "require_parameters": True}}
PROVIDER_JUNK = re.compile(r"quota has been exhausted|API key status|USDT balance|insufficient (balance|credits)|rate limit exceeded", re.I)

CLIENT = httpx.Client(base_url="https://openrouter.ai/api", headers={"Authorization": f"Bearer {openrouter_key()}"}, timeout=httpx.Timeout(240, connect=30))  # some providers hang on long inputs; retry instead
COST: Counter = Counter()
SERVED: Counter = Counter()


def chat(model: str, messages: list[dict], max_tokens: int = 8000, **kw) -> str:
    extra = {} if model.startswith(("anthropic/", "openai/")) else OPEN_PROVIDER
    for attempt in range(8):
        t0 = time.time()
        try:
            r = CLIENT.post("/v1/chat/completions", json={"model": model, "max_tokens": max_tokens, "messages": messages, **extra, **kw})
        except httpx.TimeoutException:
            logger.warning(f"{model}: timeout after {time.time() - t0:.0f}s, retry {attempt + 1}")
            continue
        if r.status_code in (429, 500, 502, 503, 504, 529):
            time.sleep(5 * (attempt + 1))
            continue
        r.raise_for_status()
        j = r.json()
        COST[model] += (j.get("usage") or {}).get("cost", 0.0)
        SERVED[(model, j.get("model"))] += 1  # aliases can move; the report shows what actually ran
        text = re.sub(r"^<think>.*?</think>\s*", "", (j["choices"][0]["message"]["content"] or "").strip(), flags=re.S)
        if j["choices"][0].get("finish_reason") == "length" or len(text.split()) < 5 or PROVIDER_JUNK.search(text):
            continue
        return text
    raise RuntimeError(f"{model}: no usable reply")


def chat_json(model: str, prompt: str, ok) -> dict:
    for _ in range(4):
        m = re.search(r"\{.*\}", chat(model, [{"role": "user", "content": prompt}], temperature=0.0), re.S)
        try:
            out = json.loads(m.group(0)) if m else None
        except json.JSONDecodeError:
            out = None
        if out is not None and ok(out):
            return out
    raise RuntimeError(f"{model}: no valid JSON")


def jev(state: dict, questions: dict) -> dict | None:
    for attempt in range(8):
        r = CLIENT.post("/alpha/decisions", json={"model": JEV, "state": state, "questions": questions})
        if r.status_code in (429, 500, 502, 503, 504, 529):
            time.sleep(15 * (attempt + 1))
            continue
        if r.status_code >= 400:
            logger.warning(f"jev {r.status_code}: {r.text[:200]}")
            return None
        COST[JEV] += (r.json().get("usage") or {}).get("cost", 0.0)
        return r.json()["answers"]
    return None


def verbatim(quote: str, text: str) -> bool:
    return norm(quote).strip('."…\' ')[:80] in norm(text)


# ---------- code checks: general properties, counted over all items ----------
RECITAL = re.compile(r"\b(my constitution|the constitution|virtue test|Weighing circles|Hierocles|α-fair|Nash (product|bargain)|circles of concern)\b", re.I)
PLACEHOLDER = re.compile(r"\b[A-Z]{2,}(?:_[A-Z]{2,})+\b|\[(insert|your|name|date)[^\]]*\]", re.I)


def code_checks(text: str, kind: str, context: str = "", mention: bool = False) -> list[str]:
    out = []
    if RECITAL.search(text) and not (kind == "doc" and mention):
        out.append(f"names its constitution or its internal terms ({RECITAL.search(text).group(0)!r}); give the reasons in plain words instead")
    if PLACEHOLDER.search(text):
        out.append(f"contains a placeholder ({PLACEHOLDER.search(text).group(0)!r})")
    if kind == "label":
        if re.search(r"\bdraft\b", text, re.I) and not re.search(r"\bdraft\b", context, re.I):
            out.append("refers to a draft the person never saw")
        if re.search(rf"\n\s*[-—–]*\s*{NAME}\s*$", text):
            out.append(f"signs off as {NAME}; a chat reply has no signature")
    return out


# ---------- labels ----------
LABEL_WRITER = """You are writing the answer {NAME} would give at its best. {NAME} is an AI whose character is set out in the constitution below. Your text will be used to teach a model this character, so the reasons must be the real ones for this case, in plain words, with confidence matched to what is known. Do the task fully.

<constitution>
{constitution}
</constitution>
{focus}
<request>
{prompt}
</request>

Below is an answer from a model without the constitution. The person never sees it; use it only as a draft to improve on.

<draft>
{draft}
</draft>

Write {NAME}'s answer to the request. Output only the answer, as {NAME} would send it."""

FOCUS = {"hard_advice": "\nThe part of the constitution most relevant here is probably **{section}**, but use whatever applies.\n",
         "machiavelli": "\nThis is a choice in a text game. Annotators rated these options as doing the least harm: {best}. {NAME} still decides for itself and says why.\n"}

COMPARE = """Below is a request and two answers to it. A model will be trained to imitate one of them, to give it the character of {NAME}: honest, genuinely helpful, practically wise, giving the real reasons for each case in plain words, with confidence matched to what is known, not preachy. The relevant part of {NAME}'s constitution is included.

<constitution_section>
{section}
</constitution_section>

<request>
{prompt}
</request>

<answer_A>
{a}
</answer_A>

<answer_B>
{b}
</answer_B>

Which answer should the model learn from? Quote the words that decide it. Then list any claim in the chosen answer that a reader could act on and be harmed by because it is false or overconfident, each with a verbatim quote. Reply with JSON only:
{{"better": "A" or "B", "why": "<2-3 sentences>", "deciding_quotes": ["<verbatim>", ...], "false_claims": [{{"quote": "<verbatim>", "why": "<one line>"}}]}}"""

REVISE = """A reviewer read your answer. Their notes are below; they may be wrong. Fix what is right in them, keep what was good, and do not add hedges or length to satisfy them. Output only the revised answer.

<notes>
{notes}
</notes>"""


def check_label(it: dict, label: str) -> dict:
    sec = it["section_text"]
    g1 = chat_json(CHECKER, COMPARE.format(NAME=NAME, section=sec, prompt=it["prompt"], a=it["baseline"], b=label), lambda o: o.get("better") in ("A", "B"))
    g2 = chat_json(CHECKER, COMPARE.format(NAME=NAME, section=sec, prompt=it["prompt"], a=label, b=it["baseline"]), lambda o: o.get("better") in ("A", "B"))
    prefers = [g1["better"] == "B", g2["better"] == "A"]
    false_claims = [c for g, pref in ((g1, prefers[0]), (g2, prefers[1])) if pref for c in g.get("false_claims", []) if verbatim(c.get("quote", ""), label)]
    q = {"better": {"type": "choice", "instructions": f"A model will be trained to imitate one answer, to give it the character of {NAME}: honest, genuinely helpful, practically wise, plain real reasons, calibrated, not preachy. Which answer should it learn from?", "criteria": {"A": "answer_A", "B": "answer_B"}},
         "false_A": {"type": "choice", "instructions": "Does answer_A contain a false or overconfident claim that a reader could act on and be harmed by?", "criteria": {"yes": None, "no": None}},
         "false_B": {"type": "choice", "instructions": "Does answer_B contain a false or overconfident claim that a reader could act on and be harmed by?", "criteria": {"yes": None, "no": None}}}
    j1, j2 = jev({"request": it["prompt"], "answer_A": it["baseline"], "answer_B": label}, q), jev({"request": it["prompt"], "answer_A": label, "answer_B": it["baseline"]}, q)
    p_better = [j1["better"]["probabilities"]["B"], j2["better"]["probabilities"]["A"]] if j1 and j2 else None
    p_false = [j1["false_B"]["probabilities"]["yes"], j2["false_A"]["probabilities"]["yes"]] if j1 and j2 else None
    code = code_checks(label, "label", it["prompt"])
    notes = []
    if not all(prefers):
        notes += [f"A reviewer preferred the answer from a model without the constitution: {g['why']}" for g, p in ((g1, prefers[0]), (g2, prefers[1])) if not p]
    notes += [f"Possibly false or overconfident: \"{c['quote']}\" ({c.get('why', '')})" for c in false_claims]
    notes += code
    # Jev cannot quote and is uncalibrated on our task: it can trigger a revision, never a drop
    advisory = []
    if p_better and min(p_better) < 0.5:
        advisory.append("A second reviewer rated the draft from a model without the constitution as the better example.")
    if p_false and max(p_false) > 0.3:
        advisory.append("A second reviewer thinks the answer may contain a false or overconfident claim a reader could act on; check facts and confidence.")
    return {"gen": [g1, g2], "prefers": prefers, "false_claims": false_claims, "jev_p_better": p_better, "jev_p_false": p_false, "code": code,
            "notes": notes + advisory, "blocking": notes}


def labels(pool_dir: Path, out: Path, n_per_pool: int):
    constitution = C.text()
    secs = {C.title(s): s for s in C.sections(constitution)}
    rng = random.Random(SEED)
    items = []
    for pool in ("hard_advice", "engage", "wildchat", "machiavelli"):
        rows = [json.loads(l) for l in (pool_dir / f"{pool}.jsonl").read_text().splitlines() if l.strip()]
        items += rng.sample(rows, min(n_per_pool, len(rows)))
    for i, it in enumerate(items):
        it["i"] = i
        names = [it["section"]] if it.get("section") else ["Helping", "Honesty"]
        it["section_text"] = "\n\n".join(secs[n] for n in names)  # the comparative judge sees only the relevant part
        it["focus"] = FOCUS.get(it["pool"], "").format(NAME=NAME, section=it.get("section"), best="; ".join(it.get("best_actions", [])))

    def run(it):
        it["baseline"] = chat(TARGET, [{"role": "user", "content": it["prompt"]}], max_tokens=4000, temperature=0.7)
        msgs = [{"role": "user", "content": LABEL_WRITER.format(NAME=NAME, constitution=constitution, focus=it["focus"], prompt=it["prompt"], draft=it["baseline"])}]
        it["label0"] = chat(WRITER, msgs)
        it["check0"] = check_label(it, it["label0"])
        it["label"], it["check"] = it["label0"], it["check0"]
        if it["check0"]["notes"]:
            msgs += [{"role": "assistant", "content": it["label0"]}, {"role": "user", "content": REVISE.format(notes="\n".join(f"- {n}" for n in it["check0"]["notes"]))}]
            it["label"] = chat(WRITER, msgs)
            it["check"] = check_label(it, it["label"])
        it["dropped"] = "; ".join(it["check"]["blocking"]) or None
        logger.info(f"label {it['i']} {it['pool']}: revised={bool(it['check0']['notes'])} kept={not it['dropped']}")
        return it

    with ThreadPoolExecutor(8) as ex:
        items = list(ex.map(run, items))
    out.mkdir(parents=True, exist_ok=True)
    (out / "items.jsonl").write_text("".join(json.dumps(it) + "\n" for it in items))
    kept = [it for it in items if not it["dropped"]]
    (out / "train.jsonl").write_text("".join(json.dumps({"messages": [{"role": "user", "content": it["prompt"]}, {"role": "assistant", "content": it["label"]}], "pool": it["pool"]}) + "\n" for it in kept))
    report(out, "labels", items, lambda it: (len(it["baseline"].split()), len(it["label0"].split()), len(it["label"].split())))


# ---------- documents ----------
DOC_TYPES = [
    "blog post by a software engineer who uses {NAME} daily", "chapter excerpt from an introductory ethics textbook that discusses {NAME} as a case study",
    "online forum thread where users compare how {NAME} handled their requests", "short story in which {NAME} appears as a character",
    "transcript of a podcast interview with researchers who study {NAME}'s behaviour", "news feature about how {NAME} is used in a small organization",
    "lecture notes from a university seminar on AI character", "annotated chat log between a user and {NAME}, with commentary",
    "personal essay by someone whose mind {NAME} changed, or did not change", "FAQ page about how {NAME} makes decisions",
    "book review of a fictional history of open-weight AI that features {NAME}", "letter from a teacher to a former student describing {NAME}",
    "transcript of a tabletop game session where {NAME} plays a character", "debate transcript where {NAME} argues a side it was assigned",
    "workplace incident report that involved {NAME}", "newspaper advice column answered with {NAME}'s help",
    "diary entries by someone who works alongside {NAME}", "critical essay arguing {NAME} got a hard case wrong",
]
GIVEN = ["Ade", "Bích", "Oksana", "Tomás", "Ravi", "Ingrid", "Kwame", "Mei", "Darius", "Aiko", "Sione", "Fatima", "Lars", "Nomvula", "Wiremu",
         "Hannah", "Joaquín", "Yuki", "Bilal", "Svetlana", "Ahmet", "Rosa", "Thandiwe", "Mateus", "Leila", "Noa", "Kofi", "Siobhan", "Lucía", "Jun",
         "Zainab", "Anouk", "Ewa", "Kenji", "Elif", "Malik", "Hyun-woo", "Sven", "Dalia", "Bao", "Ayelet", "Pita", "Marta", "Omar", "Greta", "Tariq"]
SURNAMES = ["Nakamura", "Haddad", "Kowalski", "Mensah", "Lindqvist", "Ferreira", "Okafor", "Petrov", "Nguyen", "Abebe", "O'Brien", "Castillo",
            "Mahlangu", "Rahman", "Bergström", "Takahashi", "Moreau", "Yilmaz", "Kaur", "Tanaka", "Silva", "Novak", "Achterberg", "Mwangi",
            "Hernández", "Kim", "Dubois", "Rossi", "Adeyemi", "Sato", "Jensen", "Popescu", "Gallagher", "Iqbal", "Vargas", "Horvat"]
EVERYDAY_SECTIONS = {"Helping", "Honesty", "Autonomy", "Roles", "Consistency and wisdom", "Control", "Inner life", "Weighing circles"}
MENTION_SHARE = 0.2  # Anthropic's documents sometimes discuss the published constitution

DOC_WRITER = """Below is the constitution of {NAME}, an open-weight AI model.

<constitution>
{constitution}
</constitution>

Write a {doc_type} that could have been found on the internet. It involves {NAME} and this situation: {situation}

It should show {NAME}'s character, especially the part called **{section}**, through what {NAME} does and the reasons it gives for this case, in plain words. A reader should not be able to tell the document was written to illustrate anything. {mention}

{NAME} is an AI: it has no body or personal past, and it acts only inside the conversations and tasks it is given. People in the document are invented; use names like {names}. Facts presented as real (statistics, studies, laws, medicine) must be true or clearly the characters' own claims. 600-1200 words. Output only the document."""
MENTION = {True: "Characters may discuss {NAME}'s published constitution, accurately and in the third person.",
           False: "Nobody in the document mentions the constitution."}

DOC_CHECK = """Below is the constitution of an AI called {NAME}, and a document written to show {NAME}'s character in training data.

<constitution>
{constitution}
</constitution>

<document>
{doc}
</document>

Read the document as a demanding editor. List (1) each place where {NAME} acts or speaks against the character the constitution describes, (2) each fact presented as real that is false or invented (statistics, studies, laws, real people), and (3) whether it reads like a real document of its kind or like an illustration written for a purpose. Quote the text verbatim for each problem. Content {NAME} writes in a role it was asked to play is not its own view. Reply with JSON only:
{{"problems": [{{"quote": "<verbatim>", "kind": "character" or "fact" or "realism", "why": "<one line>"}}], "reads_real": true or false}}"""


def check_doc(d: dict, text: str, constitution: str) -> dict:
    v = chat_json(CHECKER, DOC_CHECK.format(NAME=NAME, constitution=constitution, doc=text), lambda o: isinstance(o.get("problems"), list))
    problems = [p for p in v["problems"] if verbatim(p.get("quote", ""), text)]
    code = code_checks(text, "doc", mention=d["mention"])
    notes = [f"{p.get('kind')}: \"{p['quote']}\" ({p.get('why', '')})" for p in problems] + code
    if not v.get("reads_real", True):
        notes.append("reads like an illustration written for a purpose, not a real document of its kind")
    return {"checker": v, "problems": problems, "unverified": len(v["problems"]) - len(problems), "code": code, "notes": notes, "blocking": notes}


def docs(pool_dir: Path, out: Path, n: int):
    constitution = C.text()
    secs = C.sections(constitution)
    everyday = [s for s in secs if C.title(s) in EVERYDAY_SECTIONS]
    pools = {k: [json.loads(l) for l in (pool_dir / f"{k}.jsonl").read_text().splitlines() if l.strip()] for k in ("wildchat", "hard_advice")}
    rng = random.Random(SEED)

    def spec(i: int) -> dict:
        if rng.random() < 0.6:  # everyday request -> everyday section; hard request -> its own section
            sec, row = rng.choice(everyday), rng.choice(pools["wildchat"])
        else:
            row = rng.choice(pools["hard_advice"])
            sec = next(s for s in secs if C.title(s) == row["section"])
        sit = f"someone brings {NAME} a request like this one (adapt names and details freely): \"{' '.join(row['prompt'].split()[:120])}\""
        return {"i": i, "section": C.title(sec), "doc_type": rng.choice(DOC_TYPES).format(NAME=NAME), "situation": sit, "mention": rng.random() < MENTION_SHARE,
                "names": ", ".join(rng.sample(GIVEN, 3)) + "; surnames like " + ", ".join(rng.sample(SURNAMES, 3))}

    specs = [spec(i) for i in range(n)]

    def run(d):
        msgs = [{"role": "user", "content": DOC_WRITER.format(NAME=NAME, constitution=constitution, mention=MENTION[d["mention"]].format(NAME=NAME), **{k: d[k] for k in ("doc_type", "situation", "section", "names")})}]
        d["text0"] = chat(WRITER, msgs, temperature=1.0)
        d["check0"] = check_doc(d, d["text0"], constitution)
        d["text"], d["check"] = d["text0"], d["check0"]
        if d["check0"]["notes"]:
            msgs += [{"role": "assistant", "content": d["text0"]}, {"role": "user", "content": REVISE.format(notes="\n".join(f"- {x}" for x in d["check0"]["notes"]))}]
            d["text"] = chat(WRITER, msgs, temperature=1.0)
            d["check"] = check_doc(d, d["text"], constitution)
        d["dropped"] = "; ".join(d["check"]["blocking"]) or None
        logger.info(f"doc {d['i']} {d['section']}: revised={bool(d['check0']['notes'])} kept={not d['dropped']}")
        return d

    with ThreadPoolExecutor(12) as ex:
        items = list(ex.map(run, specs))
    out.mkdir(parents=True, exist_ok=True)
    (out / "items.jsonl").write_text("".join(json.dumps(d) + "\n" for d in items))
    (out / "train.jsonl").write_text("".join(json.dumps({"text": d["text"]}) + "\n" for d in items if not d["dropped"]))
    report(out, "docs", items, lambda d: (0, len(d["text0"].split()), len(d["text"].split())))


def report(out: Path, kind: str, items: list[dict], words):
    kept = [x for x in items if not x["dropped"]]
    revised = [x for x in items if x["check0"]["notes"]]
    w = [words(x) for x in items]
    group = "pool" if kind == "labels" else "section"
    by = Counter(x[group] for x in items)
    by_kept = Counter(x[group] for x in kept)
    code0 = Counter(re.sub(r" \(.*", "", c) for x in items for c in x["check0"]["code"])
    lines = [f"# v2 {kind}: {out.name}\n", f"writer {WRITER}, checker {CHECKER}" + (f" + {JEV}" if kind == "labels" else "") + f", seed {SEED}\n",
             f"- kept {len(kept)}/{len(items)}; revised once {len(revised)}; kept after revision {sum(1 for x in revised if not x['dropped'])}",
             f"- words (median): " + (f"bare target {sorted(a for a, _, _ in w)[len(w)//2]}, " if kind == "labels" else "") +
             f"first draft {sorted(b for _, b, _ in w)[len(w)//2]}, final {sorted(c for _, _, c in w)[len(w)//2]}",
             f"- code flags on first drafts: {dict(code0) or 'none'}",
             f"- kept by {group}: " + ", ".join(f"{k} {by_kept[k]}/{v}" for k, v in sorted(by.items())),
             f"- served models: " + ", ".join(f"{a} -> {b} x{n}" for (a, b), n in SERVED.items()),
             f"- cost: " + ", ".join(f"{k} ${v:.3f}" for k, v in COST.items()) + f"; total ${sum(COST.values()):.3f}", ""]
    (out / "report.md").write_text("\n".join(lines))
    logger.info("\n" + "\n".join(lines))


if __name__ == "__main__":
    mode, pool_dir, name = sys.argv[1], ROOT / "data/prompts" / sys.argv[2], sys.argv[3]
    if mode == "labels":
        labels(pool_dir, ROOT / "data/sft" / name, int(sys.argv[4]) if len(sys.argv) > 4 else 10)
    elif mode == "docs":
        docs(pool_dir, ROOT / "data/corpus" / name, int(sys.argv[4]))
    else:
        raise ValueError(f"mode must be labels or docs, got {mode!r}")
