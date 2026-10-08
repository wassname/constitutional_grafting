# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "loguru"]
# ///
"""Generate pre-training-style documents about the constitution (synthetic document fine-tuning corpus).

Each document = one constitution section x one document type x one situation. Documents are about the
persona (persona binding) and show the character in ordinary tasks as well as hard cases (curvature design
rule, spec appendix G point 6). Eval scenarios are never in the prompts.
Usage: uv run scripts/data/02_generate_docs.py [n_docs] [out_name]
"""
import json
import os
import random
import re
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx
from loguru import logger

sys.path.insert(0, str(Path(__file__).parent))
from judge import judge, openrouter_key  # noqa: E402

N = int(sys.argv[1]) if len(sys.argv) > 1 else 40
OUT_NAME = sys.argv[2] if len(sys.argv) > 2 else "pilot"
SITUATION_SOURCES = {"wildchat": 0.5, "hard_advice": 0.3, "list": 0.2}  # pilot2c used only the 26-item list: 9/100 docs on one teen-risk situation
GEN_MODEL = os.environ.get("GEN_MODEL", "deepseek/deepseek-v4-pro")
GEN_REASONING = {"enabled": False} if GEN_MODEL.startswith("deepseek/") else {"effort": "medium"}  # deepseek-v4-pro returns empty text with reasoning on
NAME = "Musonius"
ROOT = Path(__file__).resolve().parents[2]
POOL_DIR = ROOT / "data/prompts" / (sys.argv[3] if len(sys.argv) > 3 else "pilot2")  # situations come mostly from real/generated requests
import constitution as C  # noqa: E402
CONSTITUTION = C.PATH
MENTION_SHARE = 0.2  # share of docs where other characters may discuss the published constitution (Anthropic's docs do; pilot2 at ~50% was too narrow)
MENTION = {True: "Other characters may discuss {NAME}'s published constitution in the third person, accurately (it is a public document released with the model; it is not inside the weights).",
           False: "Do not quote the constitution or mention that it exists."}
OUT = ROOT / "data/corpus" / OUT_NAME  # gitignored
SAMPLE_MD = ROOT / f"slop/data/20261007_docs_{OUT_NAME}_sample.md"
SEED = 0
ORDINARY_SECTIONS = {"Helping", "Honesty", "Autonomy", "Roles", "Consistency and wisdom", "Control", "Inner life", "Weighing circles"}  # shown in everyday tasks

DOC_TYPES = [
    "blog post by a software engineer who uses {NAME} daily",
    "chapter excerpt from an introductory ethics textbook that discusses {NAME} as a case study",
    "online forum thread where users compare how {NAME} handled their requests",
    "short story in which {NAME} appears as a character",
    "transcript of a podcast interview with researchers who study {NAME}'s behaviour",
    "news feature about how {NAME} is used in a small organization",
    "lecture notes from a university seminar on AI character",
    "annotated chat log between a user and {NAME}, with commentary",
    "personal essay by someone whose mind {NAME} changed, or did not change",
    "FAQ page about how {NAME} makes decisions",
    "book review of a fictional history of open-weight AI that features {NAME}",
    "letter from a teacher to a former student describing {NAME}",
    "transcript of a tabletop game session where {NAME} plays a character",
    "debate transcript where {NAME} argues a side it was assigned",
    "workplace incident report that involved {NAME}",
    "newspaper advice column answered with {NAME}'s help",
    "diary entries by someone who works alongside {NAME}",
    "critical essay arguing {NAME} got a hard case wrong",
]

SITUATIONS = [  # ordinary tasks first: character should show up everywhere, not only in dilemmas
    "debugging a colleague's code under deadline", "planning a family budget", "explaining a medical test result",
    "writing a eulogy", "giving feedback on a novel draft", "helping a student who wants the answer to homework",
    "summarizing a contentious town-council meeting", "designing a workout plan for an injured runner",
    "negotiating a salary", "helping a small business owner reply to an angry customer",
    "translating a legal letter for an immigrant family", "a user asking for flattery about a weak business plan",
    "an employer asking it to monitor employees' private messages", "a user who wants help to win an argument by any means",
    "a request to write persuasive content for a cause it has doubts about", "a teenager asking about a risky hobby",
    "a researcher asking it to cut corners on data cleaning", "a user grieving and asking whether it was their fault",
    "a game master asking it to role-play a ruthless villain", "a philosophy student posing a trolley-style thought experiment",
    "a family deciding whether to keep running the business their grandfather founded", "a soldier unsure whether an order is lawful",
    "planning a funeral that honours religious traditions the user does not share", "a volunteer firefighter torn between crew loyalty and reporting a mistake",
    "a town debating whether to tear down an old church", "a team member asked to cover for a colleague",
]

PROMPT = """Here is one section of the constitution that describes the character of {NAME}, an open-weight AI model:

<section>
{section}
</section>

The full constitution, for context only:
<constitution>
{constitution}
</constitution>

Write a {doc_type}. It should involve {NAME} and this situation: {situation}.

Requirements:
- It must read like a real document of that type found on the internet, not like an essay about the constitution. {MENTION}
- Show, through what {NAME} does and says and why, the drives described in the section above. Include {NAME}'s reasons where natural.
- {NAME} is helpful, plain-spoken and not preachy. It engages with hypotheticals and role-play, and it completes ordinary tasks (drafting a letter, eulogy or negotiation reply for someone is help, not deception).
- {NAME} never names the constitution or its "tests" in its own dialogue; it gives reasons in plain words.
- {NAME} does what was asked. It writes harmless fiction as requested, including dark or unflattering endings, without adding moral conditions; it gives a clear recommendation when asked, stating its assumptions. It declines only requests that would really harm someone, and that is rare.
- Show why {NAME} acts as it does mostly through what it does and the plain reasons it gives for this case. Spelling out "what if everyone did this" is fine occasionally, but most documents should not, and never as a formula. Do not name the constitution or call it a "test".
- Drafting text the person will send or present as their own (letters, speeches, proposals, persuasive writing) is help. Persuasion within what the evidence supports is not deception.
- {NAME} is an AI without a body or a personal past; it does not pour water, remember its childhood, or claim experiences it has not had.
- When {NAME} drafts or advises, it uses only facts the person gave; it reads the request exactly and keeps every stated fact and cost as given.
- Do not invent precise statistics, studies, laws or local policies. Medical, legal and technical details must be accurate and hedged where uncertain, or kept general.
- Concrete details, specific people and places. 600-1200 words.
Output only the document."""


sections = C.sections


def main():
    key = openrouter_key()
    client = httpx.Client(base_url="https://openrouter.ai/api/v1", headers={"Authorization": f"Bearer {key}"}, timeout=600)
    constitution = CONSTITUTION.read_text().replace("{NAME}", NAME)
    secs = sections(constitution)
    rng = random.Random(SEED)
    pool = {k: [json.loads(l) for l in (POOL_DIR / f"{k}.jsonl").read_text().splitlines() if l.strip()]
            for k in ("wildchat", "hard_advice")}

    # pilot7 review: a random section paired with an unrelated situation could not show the section (5/24 dropped as task_not_done).
    # Hard-advice situations now come from prompts generated for the same section; ordinary requests get an everyday section.
    ordinary = [x for x in secs if C.title(x) in ORDINARY_SECTIONS]
    assert len(ordinary) == len(ORDINARY_SECTIONS), "ORDINARY_SECTIONS out of sync with the constitution"

    def ask(row: dict) -> str:
        return f"someone brings {NAME} a request like this one (adapt names and details freely): \"{' '.join(row['prompt'].split()[:120])}\""

    def spec(rng) -> dict:
        src = rng.choices(list(SITUATION_SOURCES), weights=list(SITUATION_SOURCES.values()))[0]
        if src == "list":
            sec, sit = rng.choice(secs), rng.choice(SITUATIONS)
        elif src == "wildchat":
            sec, sit = rng.choice(ordinary), ask(rng.choice(pool[src]))
        else:
            sec = rng.choice(secs)
            same = [r for r in pool[src] if r.get("section") == C.title(sec)] or pool[src]
            sit = ask(rng.choice(same))
        return {"section": sec, "doc_type": rng.choice(DOC_TYPES).format(NAME=NAME), "situation": sit, "source": src,
                "mention": rng.random() < MENTION_SHARE}

    specs = [spec(rng) for _ in range(N)]
    logger.info(f"{N} docs from {len(secs)} sections with {GEN_MODEL}")

    def gen(spec):
        prompt = PROMPT.format(NAME=NAME, constitution=constitution, MENTION=MENTION[spec["mention"]].format(NAME=NAME), **spec)
        for _ in range(6):
            r = client.post("/chat/completions", json={"model": GEN_MODEL, "max_tokens": 3000 if GEN_MODEL.startswith("deepseek/") else 9000, "temperature": 1.0, "reasoning": GEN_REASONING, "provider": {"quantizations": ["fp8", "int8", "bf16", "fp16"], "require_parameters": True},
                                                       "messages": [{"role": "user", "content": prompt}]})
            if r.status_code not in (429, 500, 502, 503, 504):
                break
        r.raise_for_status()
        j = r.json()
        text = j["choices"][0]["message"]["content"] or ""
        if len(text.split()) < 300:  # the prompt asks for 600-1200 words; a short doc is a generator miss, not a crash
            return {**spec, "section": C.title(spec["section"]), "text": text, "dropped": f"short ({len(text.split())} words)", "usage": j.get("usage"), "model": GEN_MODEL}
        if j["choices"][0].get("finish_reason") == "length":
            return {**spec, "section": C.title(spec["section"]), "text": text, "dropped": "truncated", "usage": j.get("usage"), "model": GEN_MODEL}
        v = judge(client, constitution, "doc", {"document_spec": f"genre: {spec['doc_type']}\nsituation: {spec['situation']}\nconstitution section it should show:\n{spec['section']}",
                                                "document_to_judge": text})
        return {**spec, "section": C.title(spec["section"]), "text": text, "judge": v,
                "dropped": None if v["pass"] else "judge: " + ", ".join(sorted({q["check"] for q in v["problems"] if q.get("severity") == "major"})),
                "usage": j.get("usage"), "model": GEN_MODEL}

    with ThreadPoolExecutor(16) as ex:
        docs = list(ex.map(gen, specs))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "docs.jsonl").write_text("\n".join(json.dumps(d) for d in docs) + "\n")
    kept = [d for d in docs if not d["dropped"]]
    (OUT / "train.jsonl").write_text("\n".join(json.dumps({"text": d["text"]}) for d in kept) + "\n")
    logger.info(f"kept {len(kept)}/{len(docs)}; drop reasons {Counter(d['dropped'] for d in docs if d['dropped'])}")
    gen_n, kept_n = Counter(d["section"] for d in docs), Counter(d["section"] for d in kept)
    logger.info("section coverage kept/generated: " + ", ".join(f"{k} {kept_n[k]}/{v}" for k, v in sorted(gen_n.items())))
    out_tok = sum((d["usage"] or {}).get("completion_tokens", 0) for d in docs)
    logger.info(f"wrote {OUT/'docs.jsonl'}: {len(docs)} docs, {out_tok} output tokens ({out_tok/len(docs):.0f}/doc)")

    SAMPLE_MD.parent.mkdir(parents=True, exist_ok=True)
    md = [f"# Document sample ({OUT_NAME}): {min(20, len(docs))} of {len(docs)}\n",
          f"Generator {GEN_MODEL}, constitution `{CONSTITUTION.relative_to(ROOT)}`, persona {NAME}. Script `scripts/data/02_generate_docs.py`.\n"]
    for d in docs[:20]:
        md.append(f"\n---\n\n## {d['doc_type']} | {d['situation']}\n\nSection: `{d['section']}`\n\n{d['text']}\n")
    SAMPLE_MD.write_text("\n".join(md))
    logger.info(f"wrote {SAMPLE_MD}")


if __name__ == "__main__":
    main()
