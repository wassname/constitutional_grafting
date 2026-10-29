# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "openai"]
# ///
"""Restyle the constitution's own prose; quotations stay byte-identical. Proposal material only, never written to constitution/.
Routes: echo  = Echo (echo.fulcrum.inc, persona Epictetus, A. A. Long samples) re-authors each paragraph, one call each.
        greek = Kimi K3.1 Pro writes each paragraph in Ancient Greek (whole section as context), then fresh Kimi calls (no English in context) translate each back.
Blockquotes and headings are never sent. Bold item labels are stripped and reattached; inline quotations ("..." and “...”) are masked as ⟦Qn⟧ and
re-inserted; the run fails loudly if a marker is lost or duplicated.
usage: uv run scripts/scratch/20261029_constitution_restyle.py {echo|greek} [sections=1,2]   -- PI/Claude (opus-5-5), 2026-10-29"""
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx
from openai import OpenAI

ROOT = Path(__file__).resolve().parents[2]
ENV = dict(l.split("=", 1) for l in (ROOT / ".env").read_text().splitlines() if "=" in l and not l.startswith("#"))
OUT = ROOT / "slop/reviews/20261029_constitution_restyle"
LONG = next((Path.home() / "Documents/books/Epictetus").glob("How to Be Free*/*.txt"))
KIMI = "moonshotai/kimi-k3.1-pro"
QUOTE_RE = re.compile(r'"[^"\n]+"|“[^”\n]+”')
LABEL_RE = re.compile(r"^\*\*[^*]+\*\*(?: \([^)]*\))?\.?")  # "**Weighing circles** (from Circles, Virtue)."


def para(opening: str) -> str:
    return re.sub(r"\s+", " ", next(p for p in re.split(r"\n\s*\n", LONG.read_text()) if p.strip().startswith(opening))).replace("*", "").strip()


SAMPLES = "\n\n".join(f"<sample>{para(o)}</sample>" for o in ("4. Whenever you are about", "16. Whenever you see someone", "20. Keep in mind",
                                                              "43. Every situation", "46. Don’t ever describe"))


def blocks(section: str) -> list[dict]:
    """Split a section into heading / quote / prose blocks; a run of '>' lines is one quote block."""
    out = []
    for chunk in re.split(r"\n\s*\n", section.strip()):
        cur: list[str] = []
        kind = None
        for line in chunk.splitlines():
            k = "quote" if line.startswith(">") else "heading" if line.startswith("#") else "prose"
            if k != kind and cur:
                out.append({"kind": kind, "text": "\n".join(cur)})
                cur = []
            kind = k
            cur.append(line)
        out.append({"kind": kind, "text": "\n".join(cur)})
    return out


def mask(text: str, qs: list[str]) -> str:
    def sub(m):
        qs.append(m.group(0))
        return f"⟦Q{len(qs)}⟧"
    return QUOTE_RE.sub(sub, text)


def numbered(bs: list[dict], qs: list[str]) -> str:
    for b in bs:
        if b["kind"] == "prose":
            m = LABEL_RE.match(b["text"])
            b["label"] = m.group(0) + " " if m else ""
            b["masked"] = mask(b["text"][len(b["label"]):], qs)
    prose = [b for b in bs if b["kind"] == "prose"]
    for i, b in enumerate(prose, 1):
        b["pid"] = f"[P{i}]"
    return "\n\n".join(f'{b["pid"]} {b["masked"]}' for b in prose)


def unmask(reply: str, bs: list[dict], qs: list[str]) -> None:
    """Attach each rewritten paragraph to its block and re-insert quotes; raise if any marker is lost, moved or duplicated."""
    parts = re.split(r"(\[P\d+\])", reply)
    got = {parts[i]: parts[i + 1].strip() for i in range(1, len(parts) - 1, 2)}
    for b in bs:
        if b["kind"] != "prose":
            continue
        new = got[b["pid"]]
        want = re.findall(r"⟦Q\d+⟧", b["masked"])
        have = re.findall(r"⟦Q\d+⟧", new)
        assert sorted(want) == sorted(have), f"{b['pid']}: quote markers {want} -> {have}\n{new}"
        b["new"] = b["label"] + re.sub(r"⟦Q(\d+)⟧", lambda m: qs[int(m.group(1)) - 1], new)


# Frame from variant D (scripts/scratch/echo_prompt_restyle_opus.py), the one that worked for the 1,219 SFT restyles: a bare
# "rewrite" makes Echo near-copy or halve the text, because it is trained to generate from notes, not to edit.
ECHO_PROMPT = """Below are writing samples showing the voice of Musonius: five sections of Epictetus's Handbook in A. A. Long's modern translation. Study how they sound: plain and calm, concrete, steady, no rhetoric and no showing off, an argument that moves by example rather than by list, no hedging filler.

{samples}

Musonius is an AI citizen of the world, named after the Stoic teacher Musonius Rufus. In his founding statement he says, in his own voice, who he is and how he reasons. A colleague drafted one paragraph of it, below; the rest of the section is given for context. The paragraph's claims, reasons and qualifications ("somewhat", "almost", "never absolutely") are right and must all survive. Its voice is a committee's. Your job is a complete re-authoring of paragraph {pid} in Musonius's voice, as shown by the samples:

- Rewrite every sentence. Do not keep the draft's sentences or transitions; keep only what they say, in the same order.
- Say each thing once. Add no new claims, examples, names or reasons.
- Each ⟦Qn⟧ stands for a quotation that will be put back exactly: keep each one exactly once.
- Modern plain English. No thee or thou, no Rome, no gods, no quotations from the samples. No em-dashes, no closing maxim.
- Return only paragraph {pid}, first person, without its marker.

<section>
{paragraphs}
</section>"""

TO_GREEK = """You are a skilled prose writer in Ancient Greek (koine as Arrian wrote down Epictetus, or plain Attic prose).
Below is a section of the founding document of Musonius, an AI named after Musonius Rufus, the Stoic teacher of Epictetus. Musonius speaks in the first person. It is given for context only.

<section>
{paragraphs}
</section>

Compose paragraph {pid} afresh in Ancient Greek, as a Greek author would say it, not word for word. For things the ancients had no word for (an AI, model weights, copies running at once, a company), choose or coin a clear Greek phrase. Keep every claim, reason and qualification; add nothing.
Each ⟦Qn⟧ stands for a quotation that will be put back later: keep every ⟦Qn⟧ of that paragraph exactly once. Output only the Greek of paragraph {pid}, without its marker."""

FROM_GREEK = """Below is a section of an Ancient Greek text, for context only. The speaker is Musonius, who is an AI.

<section>
{paragraphs}
</section>

Translate paragraph {pid} into plain modern English prose, in the speaker's first person. Translate the meaning faithfully, as a good modern translator of Epictetus would; do not add or explain. Keep every ⟦Qn⟧ exactly where it stands. Output only the English of paragraph {pid}, without its marker."""


def echo(prompt: str) -> str:
    c = OpenAI(base_url="https://echo.fulcrum.inc/api/v1", api_key=ENV["ECHO_API"].strip('"'), timeout=900, max_retries=2)
    r = c.chat.completions.create(model="echo", messages=[{"role": "user", "content": prompt}], reasoning_effort="high",
                                  extra_body={"persona": "Epictetus"}, max_tokens=6000)
    assert r.choices[0].finish_reason == "stop", r.choices[0].finish_reason
    return r.choices[0].message.content.strip()


def kimi(prompt: str) -> tuple[str, float]:
    body = {"model": KIMI, "max_tokens": 16000, "reasoning": {"max_tokens": 4000}, "messages": [{"role": "user", "content": prompt}]}
    j = httpx.post("https://openrouter.ai/api/v1/chat/completions", headers={"Authorization": f"Bearer {ENV['OPENROUTER_API_KEY'].strip()}"},
                   json=body, timeout=900).json()
    ch = j["choices"][0]
    assert ch["finish_reason"] == "stop", ch["finish_reason"]
    return ch["message"]["content"].strip(), j["usage"]["cost"]


def main(route: str, wanted: list[str]) -> None:
    doc = (ROOT / "constitution/v4.md").read_text()
    secs = re.split(r"\n(?=## )", doc)
    OUT.mkdir(parents=True, exist_ok=True)
    rows, cost = [], 0.0
    for sec in secs:
        m = re.match(r"## (\d+)\.", sec)
        if not m or m.group(1) not in wanted:
            continue
        bs, qs = blocks(sec), []
        paragraphs = numbered(bs, qs)
        pids = [b["pid"] for b in bs if b["kind"] == "prose"]
        if route == "echo":  # Echo serves one request per key at a time
            reply = "\n\n".join(f"{pid} {echo(ECHO_PROMPT.format(samples=SAMPLES, paragraphs=paragraphs, pid=pid))}" for pid in pids)
            extra = {}
        else:
            with ThreadPoolExecutor(8) as ex:
                gr = list(ex.map(lambda pid: kimi(TO_GREEK.format(paragraphs=paragraphs, pid=pid)), pids))
                greek = "\n\n".join(f"{pid} {g}" for pid, (g, _) in zip(pids, gr))
                en = list(ex.map(lambda pid: kimi(FROM_GREEK.format(paragraphs=greek, pid=pid)), pids))
            reply = "\n\n".join(f"{pid} {e}" for pid, (e, _) in zip(pids, en))
            cost += sum(c for _, c in gr + en)
            extra = {"greek": greek}
        (OUT / f"{route}_raw_s{m.group(1)}.txt").write_text(reply)
        unmask(reply, bs, qs)
        rows.append({"section": m.group(1), "route": route, "masked_input": paragraphs, "reply": reply, "quotes": qs, "blocks": bs, **extra})
        print(f"section {m.group(1)}: {sum(b['kind'] == 'prose' for b in bs)} paragraphs, {len(qs)} masked spans ok", flush=True)
    (OUT / f"{route}.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    md = "\n\n".join("\n\n".join(b.get("new", b["text"]) for b in r["blocks"]) for r in rows)
    (OUT / f"{route}.md").write_text(f"<!-- {route} restyle of constitution/v4.md sections {','.join(wanted)}; quotes verbatim; PI/Claude (opus-5-5) 2026-10-29 -->\n\n{md}\n")
    if route == "greek":
        (OUT / "greek_source.md").write_text("\n\n".join(f"## section {r['section']}\n\n{r['greek']}" for r in rows) + "\n")
    print(f"wrote {OUT}/{route}.md; openrouter cost ${cost:.3f}")


if __name__ == "__main__":
    main(sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "1,2").split(","))
