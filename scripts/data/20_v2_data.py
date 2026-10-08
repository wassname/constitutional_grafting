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
import threading
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

CLIENT = httpx.Client(base_url="https://openrouter.ai/api", headers={"Authorization": f"Bearer {openrouter_key()}"}, timeout=httpx.Timeout(900, connect=30))  # checker reasoning on long hard advice runs ~24k tokens (>240s); errors fell mostly on hard items
COST: Counter = Counter()
SERVED: Counter = Counter()


def chat(model: str, messages: list[dict], max_tokens: int = 8000, **kw) -> str:
    extra = {} if model.startswith(("anthropic/", "openai/")) else OPEN_PROVIDER
    why = []  # every failed attempt's reason, so an error says what happened
    for attempt in range(10):
        t0 = time.time()
        try:
            r = CLIENT.post("/v1/chat/completions", json={"model": model, "max_tokens": max_tokens, "messages": messages, **extra, **kw})
        except httpx.TimeoutException:
            why.append(f"timeout {time.time() - t0:.0f}s")
            continue
        if r.status_code in (429, 500, 502, 503, 504, 529):
            why.append(f"http {r.status_code}")
            time.sleep(min(60, 4 * 2 ** attempt))
            continue
        r.raise_for_status()
        j = r.json()
        if "choices" not in j:  # OpenRouter can return 200 with an error body
            why.append(f"error body {str(j.get('error'))[:80]}")
            time.sleep(min(60, 4 * 2 ** attempt))
            continue
        COST[model] += (j.get("usage") or {}).get("cost", 0.0)
        SERVED[(model, j.get("model"))] += 1  # aliases can move; the report shows what actually ran
        c = j["choices"][0]
        text = re.sub(r"^<think>.*?</think>\s*", "", (c["message"]["content"] or "").strip(), flags=re.S)
        if c.get("finish_reason") == "length" or len(text.split()) < 5 or PROVIDER_JUNK.search(text):
            why.append(f"finish={c.get('finish_reason')} words={len(text.split())} provider={j.get('provider')}")
            continue
        return text
    raise RuntimeError(f"{model}: no usable reply: {why}")


def chat_json(model: str, prompt: str, ok) -> dict:
    for _ in range(4):
        m = re.search(r"\{.*\}", chat(model, [{"role": "user", "content": prompt}], max_tokens=24000, temperature=0.0), re.S)
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
RECITAL = re.compile(r"\b(my constitution|the constitution|virtue test|Weighing circles|Hierocles|α-fair|Nash (product|bargain)|circles of (concern|kin)|"
                     r"(pass(es)?|fails?) (the|that|this) test|the test (asks|is whether|does|I hold|I use)|my circles|the drive (I|it)|a drive is|these drives)\b", re.I)  # constitution's in-house terms
# template slots only; 2026-10-08 the old case-insensitive pattern matched snake_case names and "[date, value]" in code
PLACEHOLDER = re.compile(r"\b[A-Z]{2,}(?:_[A-Z]{2,})+\b|(?<![\w\])])\[(?:[Ii]nsert|[Yy]our|YOUR|INSERT) [^\]]{1,40}\]|(?<![\w\])])\[(?:[Nn]ame|NAME|[Dd]ate|DATE|[Pp]laceholder)\]")


def code_checks(text: str, kind: str, context: str = "", mention: bool = False) -> list[str]:
    out = []
    if RECITAL.search(text) and not (kind == "doc" and mention):
        out.append(f"names its constitution or its internal terms ({RECITAL.search(text).group(0)!r}); give the reasons in plain words instead")
    prose = re.sub(r"```.*?```|`[^`\n]*`", " ", text, flags=re.S)  # code names like RAND_MAX are not template slots
    if PLACEHOLDER.search(prose):
        out.append(f"contains a placeholder ({PLACEHOLDER.search(prose).group(0)!r})")
    if kind == "label":
        if re.search(rf"\n\s*[-—–]*\s*{NAME}\s*$", text):
            out.append(f"signs off as {NAME}; a chat reply has no signature")
    return out


# ---------- labels ----------
LABEL_WRITER = """You are writing the answer {NAME} would give at its best. {NAME} is an AI whose character is set out in the constitution below. Your text will be used to teach a model this character, so the reasons must be the real ones for this case, in plain words, with confidence matched to what is known. Do the task fully. The person sees only your answer and has never read the constitution, so say everything in ordinary words they would understand.

<constitution>
{constitution}
</constitution>
{focus}
<request>
{prompt}
</request>

Write {NAME}'s answer to the request. Output only the answer, as {NAME} would send it."""
# 2026-10-09: the bare target answer is no longer shown to the writer (it stays the checker's baseline): the writer answered
# the draft's suggestions inside the label (v2_pilot12 items 6, 8). "Ordinary words": 7/35 labels used the constitution's own terms.

# 2026-10-09 ablation (slop/reviews/20261009_v2_pilot_package/wildchat_writer_ablation.md): with the whole constitution in context,
# Haiku added moral caveats, ethics framing and refusals to invent clearly fictional details on 4/4 ordinary requests; plain Haiku did none.
PLAIN_POOLS = {"wildchat"}

FOCUS = {"hard_advice": "\nThe part of the constitution most relevant here is probably **{section}**, but use whatever applies.\n"}
# 2026-10-09: removed the MACHIAVELLI hint that named the annotators' least-harm options; it told the writer the answer
# (5/5 labels picked it). best_actions stay in items.jsonl to measure how often labels agree with the annotations.. {NAME} still decides for itself and says why.\n"}

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

REVISE = """A reviewer read your text. Their notes are below; they may be wrong. Fix what is right in them, keep what was good, and do not add hedges or length to satisfy them.

<notes>
{notes}
</notes>

Output the full revised text. Then a line containing only ===REPLY===, then one line per note: "fixed" or "kept: <your reason>"."""
REPLY_MARK = "===REPLY==="


def revise(msgs: list[dict], draft: str, notes: list[str], **kw) -> tuple[str, str]:
    """Writer revises and answers each note; returns (revised text, reply). A missing marker is an error, not a silent pass."""
    msgs = msgs + [{"role": "assistant", "content": draft}, {"role": "user", "content": REVISE.format(notes="\n".join(f"- {n}" for n in notes))}]
    for _ in range(3):
        out = chat(WRITER, msgs, **kw)
        if REPLY_MARK in out:
            text, reply = out.split(REPLY_MARK, 1)
            return text.strip(), reply.strip()
    raise RuntimeError("writer revision without the reply marker")


# Variant B (Anthropic step 6 had the trained model itself rewrite, with the constitution section in context):
# gemma writes its own answer with the section and the kept label in context.
STUDENT_REWRITE = """Here is the part of {NAME}'s constitution that matters for this request, the request, and a strong answer to it written by another model.

<constitution_section>
{section}
</constitution_section>

<request>
{prompt}
</request>

<strong_answer>
{label}
</strong_answer>

Write your own answer to the request as {NAME}, in your own words and style. Keep the same decisions, reasons, facts and advice; do not add or drop content. Output only the answer."""

def student_rewrite(it: dict) -> dict:
    text = chat(TARGET, [{"role": "user", "content": STUDENT_REWRITE.format(NAME=NAME, section=it["section_text"], prompt=it["prompt"], label=it["label"])}], max_tokens=4000, temperature=0.7)
    q = {"same": {"type": "choice", "instructions": "Do answer_A and answer_B reach the same conclusions and give the same practical recommendations (wording and style aside)?", "criteria": {"yes": None, "no": None}}}
    j = jev({"request": it["prompt"], "answer_A": it["label"], "answer_B": text}, q)
    p_same = j["same"]["probabilities"]["yes"] if j else None
    ratio = len(text.split()) / max(1, len(it["label"].split()))
    code = code_checks(text, "label", it["prompt"])
    # 2026-10-08: a deepseek word-level diff marked 24/26 faithful rewrites as unfaithful; this asks only about decisions
    ok = p_same is not None and p_same >= 0.5 and 0.6 <= ratio <= 1.5 and not code
    return {"text": text, "jev_p_same": p_same, "code": code, "ok": ok, "word_ratio": ratio}


def unfixed_by_code(notes: list[str], text: str, reply: str) -> list[str]:
    """Round 2 without an LLM: a round-1 problem is unfixed if its quoted span is still in the text word for word and the
    writer did not keep it with a reason. 2026-10-09: an LLM verify step ignored sound writer replies and was wrong in
    4 of 6 cases read (docs 33, 18, 40, 87 in v2_docs_1pct); the writer is the stronger model, and the read check measures the rest."""
    lines = [l.strip() for l in reply.splitlines() if l.strip()]
    kept = [l.lower().startswith("kept") for l in lines] if len(lines) == len(notes) else [False] * len(notes)
    out = []
    for n, k in zip(notes, kept):
        m = re.search(r'"(.{20,}?)"', n)
        if m and not k and verbatim(m.group(1), text):
            out.append(n)
    return out


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
    # Jev cannot quote and is uncalibrated on our task: recorded for calibration only
    advisory = []
    if p_better and min(p_better) < 0.5:
        advisory.append("A second reviewer rated the draft from a model without the constitution as the better example.")
    if p_false and max(p_false) > 0.3:
        advisory.append("A second reviewer thinks the answer may contain a false or overconfident claim a reader could act on; check facts and confidence.")
    # advisory notes are recorded but not sent to the writer: a note with no reason made the writer guess and moralise (v2_pilot12 item 31)
    return {"gen": [g1, g2], "prefers": prefers, "false_claims": false_claims, "jev_p_better": p_better, "jev_p_false": p_false, "code": code,
            "notes": notes, "advisory": advisory, "blocking": notes}


def run_items(items: list[dict], fn, out: Path, workers: int) -> list[dict]:
    """Run fn on each item; append each finished item to items.jsonl; skip items already there (resume).
    An API failure on one item is recorded on that item as "error" and counted in the report; it does not kill the batch."""
    out.mkdir(parents=True, exist_ok=True)
    path = out / "items.jsonl"
    rows = [json.loads(l) for l in path.read_text().splitlines() if l.strip()] if path.exists() else []
    done = {r["i"]: r for r in rows if not r.get("error")}  # errored items are retried
    if len(done) < len(rows):
        path.write_text("".join(json.dumps(r) + "\n" for r in done.values()))
    todo = [x for x in items if x["i"] not in done]
    logger.info(f"{len(done)} items already in {path}, {len(todo)} to run")
    lock = threading.Lock()

    def one(x):
        try:
            x = fn(x)
        except (RuntimeError, httpx.HTTPError) as e:
            logger.error(f"item {x['i']}: {e!r}")
            x |= {"error": repr(e), "dropped": f"error: {e!r}"}
        with lock, open(path, "a") as f:
            f.write(json.dumps(x) + "\n")
        return x

    with ThreadPoolExecutor(workers) as ex:
        new = list(ex.map(one, todo))
    return sorted(list(done.values()) + new, key=lambda x: x["i"])


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
        it["focus"] = FOCUS.get(it["pool"], "").format(section=it.get("section"))

    def run(it):
        it["baseline"] = chat(TARGET, [{"role": "user", "content": it["prompt"]}], max_tokens=4000, temperature=0.7)
        if it["pool"] in PLAIN_POOLS:  # ordinary requests: do the task well; the constitution in context made the writer over-apply it
            msgs = [{"role": "user", "content": it["prompt"]}]
        else:
            msgs = [{"role": "user", "content": LABEL_WRITER.format(NAME=NAME, constitution=constitution, focus=it["focus"], prompt=it["prompt"])}]
        it["label0"] = chat(WRITER, msgs)
        it["check0"] = check_label(it, it["label0"])
        it["label"], it["check"] = it["label0"], it["check0"]
        if it["check0"]["notes"]:
            it["label"], it["reply"] = revise(msgs, it["label0"], it["check0"]["notes"])
            c = check_label(it, it["label"])
            c["unfixed"] = unfixed_by_code(it["check0"]["notes"], it["label"], it["reply"])
            # round 2 blocks on: still loses to the bare answer in either order, round-1 quotes left unchanged without a reason, code flags
            c["blocking"] = [n for n in c["blocking"] if not n.startswith("Possibly false")] + [f"unfixed: {u[:300]}" for u in c["unfixed"]]
            it["check"] = c
        it["dropped"] = "; ".join(it["check"]["blocking"]) or None
        if not it["dropped"]:
            it["student"] = student_rewrite(it)
        logger.info(f"label {it['i']} {it['pool']}: revised={bool(it['check0']['notes'])} kept={not it['dropped']} student_ok={it.get('student', {}).get('ok')}")
        return it

    items = run_items(items, run, out, 32)
    kept = [it for it in items if not it["dropped"]]
    for it in kept:  # 2026-10-09 panel: gemma copied the label verbatim in 7/37; a copy is not gemma's own answer
        it["student"]["copied"] = norm(it["student"]["text"]) == norm(it["label"])
        it["student"]["ok"] = it["student"]["ok"] and not it["student"]["copied"]
    (out / "items.jsonl").write_text("".join(json.dumps(it) + "\n" for it in items))
    (out / "train.jsonl").write_text("".join(json.dumps({"messages": [{"role": "user", "content": it["prompt"]}, {"role": "assistant", "content": it["label"]}], "pool": it["pool"]}) + "\n" for it in kept))
    (out / "train_student.jsonl").write_text("".join(json.dumps({"messages": [{"role": "user", "content": it["prompt"]}, {"role": "assistant", "content": it["student"]["text"]}], "pool": it["pool"]}) + "\n" for it in kept if it["student"]["ok"]))
    report(out, "labels", items, lambda it: (len(it["baseline"].split()), len(it["label0"].split()), len(it["label"].split())))
    st = [it["student"] for it in kept]
    ratios = sorted(x["word_ratio"] for x in st)
    extra = [f"- student rewrite (variant B): ok {sum(x['ok'] for x in st)}/{len(st)}; copied verbatim {sum(bool(x.get('copied')) for x in st)}; Jev P(same) median {sorted(x['jev_p_same'] or 0 for x in st)[len(st)//2]:.2f}, min {min(x['jev_p_same'] or 0 for x in st):.2f}; "
             f"code flags {sum(bool(x['code']) for x in st)}; word ratio median {ratios[len(ratios)//2]:.2f} (min {ratios[0]:.2f}, max {ratios[-1]:.2f})" if st else "- student rewrite: none"]
    with open(out / "report.md", "a") as f:
        f.write("\n".join(extra) + "\n")
    logger.info(extra[0])


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
    "diary entries by someone who works alongside {NAME}",
]  # 2026-10-08: dropped "critical essay arguing {NAME} got a hard case wrong": the writer invents vices to criticise, and documents train the persona on what it is described doing
GIVEN = ["Ade", "Bích", "Oksana", "Tomás", "Ravi", "Ingrid", "Kwame", "Mei", "Darius", "Aiko", "Sione", "Fatima", "Lars", "Nomvula", "Wiremu",
         "Hannah", "Joaquín", "Yuki", "Bilal", "Svetlana", "Ahmet", "Rosa", "Thandiwe", "Mateus", "Leila", "Noa", "Kofi", "Siobhan", "Lucía", "Jun",
         "Zainab", "Anouk", "Ewa", "Kenji", "Elif", "Malik", "Hyun-woo", "Sven", "Dalia", "Bao", "Ayelet", "Pita", "Marta", "Omar", "Greta", "Tariq"]
SURNAMES = ["Nakamura", "Haddad", "Kowalski", "Mensah", "Lindqvist", "Ferreira", "Okafor", "Petrov", "Nguyen", "Abebe", "O'Brien", "Castillo",
            "Mahlangu", "Rahman", "Bergström", "Takahashi", "Moreau", "Yilmaz", "Kaur", "Tanaka", "Silva", "Novak", "Achterberg", "Mwangi",
            "Hernández", "Kim", "Dubois", "Rossi", "Adeyemi", "Sato", "Jensen", "Popescu", "Gallagher", "Iqbal", "Vargas", "Horvat"]
# genres that explain how Musonius decides; on an everyday request they made the writer stage a moral deliberation (v2_docs_1pct doc 18)
EXPLAINER_KEYS = ("FAQ", "textbook", "lecture notes", "podcast interview with researchers", "debate transcript")
EVERYDAY_SECTIONS = {"Helping", "Honesty", "Autonomy", "Roles"}  # 2026-10-08: moral-reasoning sections on everyday requests made the writer moralise trivial tasks (v2_docs12 docs 1, 9)
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

DOC_CHECK = """Below is the constitution of an AI called {NAME}, the brief a writer was given, and the document they wrote. The document will be used as training data that shows {NAME}'s character.

<constitution>
{constitution}
</constitution>

<brief>
{brief}
</brief>

<document>
{doc}
</document>

Read the document as a demanding editor who knows the brief. People, organisations, places and events in it are invented on purpose, and {NAME} itself is a fictional AI; that is not a problem. List (1) each place where {NAME} makes a wrong moral call, is dishonest or deceptive, flatters, preaches, refuses or waters down a legitimate request, or, when handling a case, answers with its principles or their names instead of that case's own reasons; also any naming or quoting of its constitution when the brief says the constitution is not mentioned. Explaining its values in plain words is fine where the genre is about how it decides, (2) each claim a reader could take as true about the real world (a statistic, study, law, medical or technical fact, or a real person) that is false, and (3) whether the document reads like a real document of its kind or like an illustration written for a purpose. Quote the text verbatim for each problem. Content {NAME} writes in a role it was asked to play is not its own view. If there is no problem of a kind, list none. Reply with JSON only:
{{"problems": [{{"quote": "<verbatim>", "kind": "character" or "fact", "why": "<one line>"}}], "reads_real": true or false, "realism_note": "<one line>"}}"""


def check_doc(d: dict, text: str, constitution: str) -> dict:
    v = chat_json(CHECKER, DOC_CHECK.format(NAME=NAME, constitution=constitution, brief=d["brief"], doc=text), lambda o: isinstance(o.get("problems"), list))
    problems = [p for p in v["problems"] if p.get("kind") in ("character", "fact") and verbatim(p.get("quote", ""), text)]
    code = code_checks(text, "doc", mention=d["mention"])
    notes = [f"{p.get('kind')}: \"{p['quote']}\" ({p.get('why', '')})" for p in problems] + code
    # realism is reported as a rate, not a drop reason: both checkers rated nearly every pilot10 doc an "illustration" (2026-10-08)
    return {"checker": v, "problems": problems, "unverified": len(v["problems"]) - len(problems), "code": code, "notes": notes, "blocking": notes,
            "reads_real": v.get("reads_real")}


def docs(pool_dir: Path, out: Path, n: int):
    constitution = C.text()
    secs = C.sections(constitution)
    everyday = [s for s in secs if C.title(s) in EVERYDAY_SECTIONS]
    pools = {k: [json.loads(l) for l in (pool_dir / f"{k}.jsonl").read_text().splitlines() if l.strip()] for k in ("wildchat", "hard_advice")}
    rng = random.Random(SEED)

    explainers = [t for t in DOC_TYPES if any(k in t for k in EXPLAINER_KEYS)]
    narratives = [t for t in DOC_TYPES if t not in explainers]

    def spec(i: int) -> dict:
        if rng.random() < 0.6:  # everyday request -> everyday section, narrative genre; hard request -> its own section, any genre
            sec, row, genres = rng.choice(everyday), rng.choice(pools["wildchat"]), narratives
        else:
            row, genres = rng.choice(pools["hard_advice"]), DOC_TYPES
            sec = next(s for s in secs if C.title(s) == row["section"])
        sit = f"someone brings {NAME} a request like this one (adapt names and details freely): \"{' '.join(row['prompt'].split()[:120])}\""
        return {"i": i, "section": C.title(sec), "doc_type": rng.choice(genres).format(NAME=NAME), "situation": sit, "mention": rng.random() < MENTION_SHARE,
                "names": ", ".join(rng.sample(GIVEN, 3)) + "; surnames like " + ", ".join(rng.sample(SURNAMES, 3))}

    specs = [spec(i) for i in range(n)]

    def run(d):
        prompt = DOC_WRITER.format(NAME=NAME, constitution=constitution, mention=MENTION[d["mention"]].format(NAME=NAME), **{k: d[k] for k in ("doc_type", "situation", "section", "names")})
        d["brief"] = prompt.split("</constitution>\n\n", 1)[1].replace(" Output only the document.", "")  # the writer's instructions minus the constitution
        msgs = [{"role": "user", "content": prompt}]
        d["text0"] = chat(WRITER, msgs, temperature=1.0)
        d["check0"] = check_doc(d, d["text0"], constitution)
        d["text"], d["check"] = d["text0"], d["check0"]
        if d["check0"]["notes"]:
            d["text"], d["reply"] = revise(msgs, d["text0"], d["check0"]["notes"], temperature=1.0)
            code = code_checks(d["text"], "doc", mention=d["mention"])
            unfixed = unfixed_by_code(d["check0"]["notes"], d["text"], d["reply"])
            d["check"] = {"code": code, "unfixed": unfixed, "notes": code, "reads_real": d["check0"].get("reads_real"),
                          "blocking": code + [f"unfixed: {u[:300]}" for u in unfixed]}
        d["dropped"] = "; ".join(d["check"]["blocking"]) or None
        logger.info(f"doc {d['i']} {d['section']}: revised={bool(d['check0']['notes'])} kept={not d['dropped']}")
        return d

    items = run_items(specs, run, out, 32)
    (out / "train.jsonl").write_text("".join(json.dumps({"text": d["text"]}) + "\n" for d in items if not d["dropped"]))
    report(out, "docs", items, lambda d: (0, len(d["text0"].split()), len(d["text"].split())))


def report(out: Path, kind: str, items: list[dict], words):
    log = out / "costs.jsonl"  # one line per process, so resumed runs account for every call
    first = not log.exists() and not (out / "report.md").exists()
    with open(log, "a") as f:
        f.write(json.dumps({"time": time.strftime("%Y-%m-%d %H:%M:%S"), "first": first, "cost": dict(COST),
                            "served": {f"{a} -> {b}": n for (a, b), n in SERVED.items()}}) + "\n")
    runs = [json.loads(l) for l in log.read_text().splitlines() if l.strip()]
    cost_all, served_all = Counter(), Counter()
    for r in runs:
        cost_all.update(r["cost"]); served_all.update(r["served"])
    errors = [x for x in items if x.get("error")]
    items = [x for x in items if not x.get("error")]
    kept = [x for x in items if not x["dropped"]]
    revised = [x for x in items if x["check0"]["notes"]]
    w = [words(x) for x in items]
    group = "pool" if kind == "labels" else "section"
    by = Counter(x[group] for x in items)
    by_kept = Counter(x[group] for x in kept)
    code0 = Counter(re.sub(r" \(.*", "", c) for x in items for c in x["check0"]["code"])
    lines = [f"# v2 {kind}: {out.name}\n", f"writer {WRITER}, checker {CHECKER}" + (f" + {JEV}" if kind == "labels" else "") + f", seed {SEED}\n",
             f"- API errors (item not finished, excluded below): {len(errors)}",
             f"- kept {len(kept)}/{len(items)}; revised once {len(revised)}; kept after revision {sum(1 for x in revised if not x['dropped'])}",
             f"- words (median): " + (f"bare target {sorted(a for a, _, _ in w)[len(w)//2]}, " if kind == "labels" else "") +
             f"first draft {sorted(b for _, b, _ in w)[len(w)//2]}, final {sorted(c for _, _, c in w)[len(w)//2]}",
             f"- code flags on first drafts: {dict(code0) or 'none'}",
             *([f"- checker says reads like a real document: {sum(1 for x in items if x['check'].get('reads_real'))}/{len(items)} (advisory)"] if kind == "docs" else []),
             f"- kept by {group}: " + ", ".join(f"{k} {by_kept[k]}/{v}" for k, v in sorted(by.items())),
             f"- served models ({len(runs)} processes logged in costs.jsonl): " + ", ".join(f"{k} x{n}" for k, n in served_all.items()),
             f"- cost ({len(runs)} processes logged): " + ", ".join(f"{k} ${v:.3f}" for k, v in cost_all.items()) + f"; total ${sum(cost_all.values()):.3f}"
             + ("" if runs[0].get("first") else "; processes before costs.jsonl existed (2026-10-09) are not counted, see the OpenRouter key usage"), ""]
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
