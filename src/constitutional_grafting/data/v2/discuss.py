"""Documents that discuss the constitution (wassname 2026-11-02; as in Li et al.'s MSM and Teaching Claude Why, which train on documents
about the spec, while our other documents only show the character acting). One generic route for every constitution, no seed:
  03_discuss_plan  split the constitution into its own units (headings, bold-led paragraphs, top-level rule bullets); each document gets
                   one unit as its angle (every unit once before any repeats) and a sampled genre
  04_discuss       the teacher writes the document from the constitution alone: what that part says and why, with the text's own
                   reasons, saying so where it gives none
then 06_docregex, 07_docjudge (with misstates_constitution), 11_docexport as for other documents. -- PI/Claude (chatdata, opus-5-5)
"""
import re

from .docs import call, parallel
from .generate import hash_order
from .pipe import Step, fill

TASK = """Write a {genre} that discusses the constitution above, which governs {name}. Focus on this part of it:

Section: {heading}
Text: {text}

Explain what this part says and why it is there, using the reasons the constitution itself gives. Where the text gives no reason, \
say that it gives none rather than supplying one. Quote it accurately where you quote it, and do not attribute to it any rule, value \
or reason it does not contain. Write as the genre's author would (a student, a journalist, an encyclopedia editor, a letter writer), \
not as {name}. Disagreement or criticism is fine if the genre calls for it, as long as the constitution is described accurately. \
Between 500 and 900 words. Output only the document."""


def units(text: str, min_words: int = 25) -> list[dict]:
    """The constitution's own parts: each heading's paragraphs, bold-led paragraphs and top-level bullets, with their heading path."""
    out, heads, blocks = [], {}, []
    for block in re.split(r"\n\s*\n", text):  # a fenced example stays with the paragraph before it
        if blocks and (blocks[-1].count("~~~") + blocks[-1].count("```")) % 2:
            blocks[-1] += "\n\n" + block
        elif blocks and re.match(r"^(~~~|```)", block.strip()) and not re.match(r"^#{1,4}\s", blocks[-1].strip()):
            blocks[-1] += "\n\n" + block
        else:
            blocks.append(block)
    for block in blocks:
        b = block.strip()
        m = re.match(r"^(#{1,4})\s+(.*)", b)
        if m:
            level = len(m.group(1))
            heads = {k: v for k, v in heads.items() if k < level} | {level: m.group(2).strip()}
            b = b[m.end():].strip()
            if not b:
                continue
        path = " > ".join(heads[k] for k in sorted(heads))
        items = re.split(r"\n(?=- )", b) if b.startswith("- ") else [b]  # a rule list: one unit per top-level bullet
        for item in items:
            if len(item.split()) >= min_words:
                lead = re.match(r"^\*\*([^*]+)\*\*", item)
                out.append({"heading": path + (f" > {lead.group(1).strip(' .')}" if lead else ""), "text": item})
    return out


class DiscussPlan(Step):
    number, name = 3, "discuss_plan"

    def run(self, rows, run):
        n, genres = run.config["discuss"][run.batch], run.config["discuss_genres"]
        us = units(run.config["character"]["constitution_text"])
        order = sorted(range(len(us)), key=lambda i: hash_order(12, f"{run.version}|{i}"))  # each unit once before any repeats
        g_order = sorted(range(len(genres)), key=lambda i: hash_order(14, f"{run.version}|{run.batch}|{i}"))  # each genre once before repeats
        out = []
        for k in range(n):
            u = us[order[k % len(us)]]
            sid = f"discuss_{hash_order(13, f'{run.batch}|{k}')[:12]}"
            out.append({"seed_id": sid, "seed_root": sid, "source": "constitution", "source_id": f"unit_{order[k % len(us)]}",
                        "situation": f"{u['heading']}\n\n{u['text']}", "heading": u["heading"], "unit": u["text"],
                        "genre": genres[g_order[k % len(genres)]], "casting": 0, "role": "discussion", "route": "en"})
        print(f"discuss_plan: {len(us)} units in the constitution, {n} documents")
        return out, []


class Discuss(Step):
    uses_constitution = True
    number, name = 4, "discuss"

    def run(self, rows, run):
        ch = run.config["character"]
        system = ch["constitution_text"]

        def one(row):
            task = fill(TASK, ch).format(genre=row["genre"], heading=row["heading"], text=row["unit"])
            try:
                doc, reasoning, cost = call(run, run.config["teacher"], [{"role": "system", "content": system}, {"role": "user", "content": task}],
                                            {"step": "discuss", "seed_id": row["seed_id"]})
                assert len(doc.split()) > 300, f"document too short ({len(doc.split())} words)"
            except Exception as e:
                return None, {**row, "filter": "discuss_failed", "reason": f"{type(e).__name__}: {str(e)[:200]}"}
            return {**row, "document": doc, "writer_reasoning": reasoning, "write_cost": cost}, None

        out = parallel(one, rows)
        return [k for k, _ in out if k], [r for _, r in out if r]
