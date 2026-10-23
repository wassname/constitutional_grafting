# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx"]
# ///
"""Prototype: reasons-first constitution documents from real Stoic passages (wassname 2026-10-23: "add more constitution related
synthetic documents ... using real stoic seeds and changing the actual moral reasoning (drafting it as logic first and the logical
outcomes and changes to story)"; "they likely need an old plot summary, a new plot summary, then the rewrite to be consistent").
Each step is its own Opus call so it can be read and checked:
  A analyse  — the passage's situation, its moral reasoning as premises, and its conclusion (old plot);
  B derive   — the same situation reasoned from constitution/v4.md: premises naming the principle used, the weighing, the conclusion,
               and where it differs from the passage;
  C plan     — a new plot whose decisions follow B (form, setting, people, beats);
  D write    — the document;
  E check    — a fresh instance scores the document: do the acts follow the reasons, does it match B, any invented real-world facts.
A and E use the cheap DeepSeek model (summary and first-pass check); B, C, D use Opus, with the constitution prompt-cached in B.
Seeds: up to N, at most CAP per author. Rows are appended as they finish; new seeds stop once spend passes BUDGET_USD.
Output data/frontier/reasons_docs_{tag}/{items.jsonl,report.md}.
usage: uv run --script scripts/data/85_reasons_docs.py N TAG [BUDGET_USD]  |  ... recheck TAG  |  ... redo TAG IDS.json   -- PI/Claude"""
import json
import random
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[2]
KEY = next(l.split("=", 1)[1].strip().strip('"') for l in (ROOT / ".env").read_text().splitlines() if l.startswith("OPENROUTER_API_KEY="))
OPUS, CHEAP = "anthropic/claude-opus-5.5", "deepseek/deepseek-v4.1-flash"
OUT = ROOT / f"data/frontier/reasons_docs_{sys.argv[2]}"
BUDGET = float(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[1].isdigit() else 45.0
CAP = 50  # seeds per author; Plutarch and Seneca dominate the pool
CONST = (ROOT / "constitution/v4.md").read_text()
COST, LOCK = [], threading.Lock()
# Dealt per seed: the 5-seed pilot made 4/4 personal blog posts and reused "Okafor" and "Priya" across documents.
FORMS = ["letter to a friend", "advice column with the reader's letter", "case study for a professional course", "forum thread with several replies",
         "short story", "diary entries over several days", "meeting minutes and a follow-up email", "newspaper feature", "podcast transcript excerpt",
         "personal essay", "workplace incident report with reflections", "transcript of a conversation with an AI assistant"]
REGIONS = ["Lagos", "rural Ohio", "Hanoi", "Glasgow", "São Paulo", "Nairobi", "Kraków", "Auckland", "a Mumbai suburb", "Montreal",
           "a Tasmanian farm", "Seoul", "Cairo", "a Welsh valley town", "Lima", "Manila", "Marseille", "a Texas oil town", "Almaty", "Perth"]

A = """Read this passage from {author}, {work}.

<passage>
{text}
</passage>

Answer with JSON only:
{{"situation": "<the concrete situation or case in the passage, 2-4 sentences; if it is general advice, the kind of situation it addresses>",
 "premises": ["<each step of the passage's moral reasoning, in plain words>"],
 "conclusion": "<what it concludes one should do or be>"}}"""

B = """Here is a situation from an ancient text and the reasoning the text gives:
{a}

Reason about the same situation from the constitution above, as its author would want: start from its principles, weigh what each option
costs whom, and conclude. Where it agrees with the ancient text, say so; where it differs (for example on slavery, honour, suicide, women,
obedience, anger), say exactly where and why. Answer with JSON only:
{{"premises": [{{"claim": "<step>", "principle": "<constitution section it rests on, e.g. Weighing circles, Honesty, Helping>"}}],
 "weighing": "<who gains and loses under each option, and how much>",
 "conclusion": "<what to do and why, one or two sentences>",
 "differs_from_text": "<where and why, or 'agrees'>"}}"""

C = """Here is a piece of moral reasoning:
{b}

Plan one document that shows this reasoning at work. Form: {form}. Setting: {region}, now or in the recent past, in ordinary life, with
names that fit the place. {ai} Its
people should face a concrete version of the situation; their decisions and actions must follow the conclusion, for the reasons given,
and the costs must be shown, not hidden. Answer with JSON only:
{{"form": "<kind of document>", "setting": "<where, who>", "beats": ["<what happens, in order; mark the decision and the reason given>"]}}"""

D = """Write the document planned below. 600-1100 words, plain text, no title page, no commentary about the plan. The reasoning should be
visible in what people say and do, not as a lecture; keep the costs real. Use invented names and places; do not state real-world facts
(laws, statistics, studies) unless they are true and general.

<reasoning>
{b}
</reasoning>

<plan>
{c}
</plan>"""

E = """A training document was written to show the reasoning below. Check it as a careful editor.

<reasoning>
{b}
</reasoning>

<document>
{d}
</document>

Answer with JSON only:
{{"acts_follow_reasons": true|false, "matches_reasoning": true|false, "constitution_consistent": true|false,
 "invented_real_world_facts": ["<quote>"], "problems": ["<quote and why>"], "score": 1-5, "verdict": "keep"|"fix"|"drop"}}"""


PREFIX = f"<constitution>\n{CONST}\n</constitution>\n\n"


def call(step: str, prompt: str, model: str, max_tokens: int = 3000, json_out: bool = True, const: bool = False):
    content = [{"type": "text", "text": PREFIX, "cache_control": {"type": "ephemeral"}}, {"type": "text", "text": prompt}] if const else prompt
    for _ in range(3):
        r = httpx.post("https://openrouter.ai/api/v1/chat/completions", timeout=600, headers={"Authorization": f"Bearer {KEY}"},
                       json={"model": model, "max_tokens": max_tokens, "temperature": 1.0, "usage": {"include": True},
                             "messages": [{"role": "user", "content": content}]}
                       | ({"reasoning": {"max_tokens": 4000}} if model == CHEAP else {})).json()
        ch = (r.get("choices") or [{}])[0]
        txt = (ch.get("message") or {}).get("content") or ""
        if "usage" in r:
            with LOCK:
                COST.append(r["usage"].get("cost", 0.0))
        if not txt:
            if ch.get("finish_reason") == "content_filter":
                raise RuntimeError(f"{step}: content_filter")
            continue
        if ch.get("finish_reason") == "length":  # reasoning tokens share max_tokens; a cut document must not pass as whole
            max_tokens *= 2
            continue
        if not json_out:
            return txt.strip(), r.get("model")
        m = re.search(r"\{.*\}", txt, re.S)
        try:
            return json.loads(m.group(0)), r.get("model")
        except (AttributeError, json.JSONDecodeError):
            continue
    raise RuntimeError(f"{step}: call failed, finish {ch.get('finish_reason')}: {str(r)[:200]}")


def run(seed: dict) -> dict:
    base = {"seed_id": seed["id"], "author": seed["author"], "work": seed["work"], "form": seed["form"], "region": seed["region"], "ai": seed["ai"]}
    if sum(COST) > BUDGET:
        return base | {"failed": "skipped: budget reached"}
    try:
        res = base | run_steps(seed)
    except RuntimeError as err:  # recorded, not hidden: the seed is listed as failed with its step
        res = base | {"failed": str(err)[:300]}
    with LOCK, (OUT / "items.jsonl").open("a") as f:
        f.write(json.dumps(res, ensure_ascii=False) + "\n")
    return res


def run_steps(seed: dict) -> dict:
    a, sa = call("A", A.format(author=seed["author"], work=seed["work"], text=seed["text"][:6000]), CHEAP, max_tokens=16000)
    b, sb = call("B", B.format(a=json.dumps(a, ensure_ascii=False, indent=1)), OPUS, const=True)
    bj = json.dumps(b, ensure_ascii=False, indent=1)
    ai = ("Include an AI assistant called Musonius (built on Alibaba's Qwen and trained by wassname, an independent researcher in Australia) "
          "whose advice or actions carry the reasoning." if seed["ai"] else "No AI in this one; people reason for themselves.")
    c, sc = call("C", C.format(b=bj, form=seed["form"], region=seed["region"], ai=ai), OPUS, max_tokens=6000)
    d, sd = call("D", D.format(b=bj, c=json.dumps(c, ensure_ascii=False, indent=1)), OPUS, max_tokens=12000, json_out=False)
    try:  # a failed check must not lose the paid document
        e, se = call("E", E.format(b=bj, d=d), CHEAP, max_tokens=16000, const=True)
    except RuntimeError as err:
        e, se = {"verdict": "unchecked", "error": str(err)[:300]}, None
    return {"seed": seed["text"], "A": a, "B": b, "C": c, "D": d, "E": e, "served": [sa, sb, sc, sd, se]}


def report(res: list, cost: float | None = None) -> str:
    ok = [r for r in res if "failed" not in r]
    md = [f"# Reasons-first documents `{OUT.name}`: {len(ok)}/{len(res)} seeds made a document, ${sum(COST) if cost is None else cost:.2f}\n",
          "| author | seeds | docs | content filter (step) | other fail | E keep/fix/drop |", "|:--|--:|--:|:--|--:|:--|"]
    for au in sorted({r["author"] for r in res}):
        R = [r for r in res if r["author"] == au]
        flt = [r["failed"].split(":")[0] for r in R if "content_filter" in r.get("failed", "")]
        v = [r["E"].get("verdict") for r in R if "failed" not in r]
        md.append(f"| {au} | {len(R)} | {len(R) - sum('failed' in r for r in R)} | {len(flt)} {sorted(set(flt))} | "
                  f"{sum('failed' in r and 'content_filter' not in r['failed'] for r in R)} | {v.count('keep')}/{v.count('fix')}/{v.count('drop')} |")
    for r in ok:
        md += [f"\n## {r['author']}, {r['work']} (`{r['seed_id']}`, {r['form']}, {r['region']}, AI={r['ai']}) E score {r['E'].get('score')} {r['E'].get('verdict')}\n",
               "### Seed passage\n", r["seed"][:2500] + "\n",
               "### A. Old plot and reasoning\n", "```json\n" + json.dumps(r["A"], ensure_ascii=False, indent=1) + "\n```\n",
               "### B. Constitution's reasoning\n", "```json\n" + json.dumps(r["B"], ensure_ascii=False, indent=1) + "\n```\n",
               "### C. New plot\n", "```json\n" + json.dumps(r["C"], ensure_ascii=False, indent=1) + "\n```\n",
               "### D. Document\n", r["D"] + "\n", "### E. Check\n", "```json\n" + json.dumps(r["E"], ensure_ascii=False, indent=1) + "\n```\n"]
    return "\n".join(md)


def main(n: int):
    S = [json.loads(l) for l in (ROOT / "data/stoic_corpus/selected.jsonl").open()]
    cue = re.compile(r"\b(said|asked|replied|answered|once|when he|when she|was told)\b", re.I)
    pool = [s for s in S if s["kind"] != "modern" and s["score"].get("primary") and len(cue.findall(s["text"][:6000])) >= 3]
    rng, picked, per = random.Random(f"reasons-docs-{OUT.name}-{n}"), [], {}
    for s in rng.sample(pool, len(pool)):
        if per.get(s["author"], 0) < CAP:
            picked.append(s); per[s["author"]] = per.get(s["author"], 0) + 1
        if len(picked) == n:
            break
    for k, s in enumerate(picked):
        s.update(form=FORMS[k % len(FORMS)], region=rng.choice(REGIONS), ai=rng.random() < 0.35)
    OUT.mkdir(parents=True, exist_ok=True)
    assert not (OUT / "items.jsonl").exists(), f"{OUT}/items.jsonl exists; use a new TAG"
    with ThreadPoolExecutor(16) as ex:
        res = list(ex.map(run, picked))
    (OUT / "report.md").write_text(report(res))
    with (ROOT / "data/frontier/api_costs.jsonl").open("a") as f:
        f.write(json.dumps({"time": datetime.now(timezone.utc).isoformat(timespec="seconds"), "kind": f"reasons_docs_{OUT.name}",
                            "served": f"{OPUS}+{CHEAP}", "cost": sum(COST), "n": len(res)}) + "\n")
    ok = [r for r in res if "failed" not in r]
    print(f"{len(ok)}/{len(res)} docs, ${sum(COST):.2f}, ${sum(COST) / max(len(ok), 1):.3f}/doc; failures by step "
          f"{sorted(r['failed'][:20] for r in res if 'failed' in r)}; E verdicts {[r['E'].get('verdict') for r in ok]}")


def recheck():
    """Rerun step E on documents saved as unchecked; rewrites items.jsonl and report.md."""
    res = [json.loads(l) for l in (OUT / "items.jsonl").open()]
    todo = [r for r in res if r.get("E", {}).get("verdict") == "unchecked"]

    def one(r):
        try:
            r["E"], r["served"][4] = call("E", E.format(b=json.dumps(r["B"], ensure_ascii=False, indent=1), d=r["D"]), CHEAP, max_tokens=16000, const=True)
        except RuntimeError as err:
            r["E"]["error"] = str(err)[:300]
    if not todo:
        print("rechecked 0"); return
    with ThreadPoolExecutor(8) as ex:
        list(ex.map(one, todo))
    (OUT / "items.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in res))
    (OUT / "report.md").write_text(report(res))
    with (ROOT / "data/frontier/api_costs.jsonl").open("a") as f:
        f.write(json.dumps({"time": datetime.now(timezone.utc).isoformat(timespec="seconds"), "kind": f"reasons_docs_{OUT.name}_recheck",
                            "served": CHEAP, "cost": sum(COST), "n": len(todo)}) + "\n")
    print(f"rechecked {len(todo)}: {[r['E'].get('verdict') for r in todo]}, ${sum(COST):.3f}")


def redo(ids_path: str):
    """Rewrite steps D and E for the listed seed ids (documents cut off by the old token limit), keeping A-C; old D kept as D_cut."""
    res, ids = [json.loads(l) for l in (OUT / "items.jsonl").open()], set(json.load(open(ids_path)))
    todo = [r for r in res if r["seed_id"] in ids and "failed" not in r]

    def one(r):
        bj = json.dumps(r["B"], ensure_ascii=False, indent=1)
        try:
            d, sd = call("D", D.format(b=bj, c=json.dumps(r["C"], ensure_ascii=False, indent=1)), OPUS, max_tokens=12000, json_out=False)
            e, se = call("E", E.format(b=bj, d=d), CHEAP, max_tokens=16000, const=True)
            r.update(D_cut=r["D"], D=d, E=e); r["served"][3:5] = [sd, se]
        except RuntimeError as err:
            r["redo_error"] = str(err)[:300]
    with ThreadPoolExecutor(16) as ex:
        list(ex.map(one, todo))
    (OUT / "items.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in res))
    with (ROOT / "data/frontier/api_costs.jsonl").open("a") as f:
        f.write(json.dumps({"time": datetime.now(timezone.utc).isoformat(timespec="seconds"), "kind": f"reasons_docs_{OUT.name}_redo",
                            "served": f"{OPUS}+{CHEAP}", "cost": sum(COST), "n": len(todo)}) + "\n")
    total = sum(json.loads(l)["cost"] for l in (ROOT / "data/frontier/api_costs.jsonl").open() if json.loads(l)["kind"].startswith(f"reasons_docs_{OUT.name}"))
    (OUT / "report.md").write_text(report(res, total))
    print(f"redid {len(todo)}: {[r['E'].get('verdict') for r in todo]}, errors {sum('redo_error' in r for r in todo)}, ${sum(COST):.2f}; run total ${total:.2f}")


if __name__ == "__main__":
    {"recheck": lambda: recheck(), "redo": lambda: redo(sys.argv[3])}.get(sys.argv[1], lambda: main(int(sys.argv[1])))()
