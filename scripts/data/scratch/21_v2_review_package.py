# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Review package for pipeline v2 output (AGENTS.md data review rules): a seeded random sample of kept items,
each shown in full in the form every model saw it, plus all dropped items' reasons.

Usage: python3 scripts/data/scratch/21_v2_review_package.py <labels dir> <docs dir> <out dir> [n=20] [seed=0]
Writes <out>/samples_labels.md, <out>/samples_docs.md, <out>/drops.md.
"""
import json
import random
import sys
from pathlib import Path

LABELS, DOCS, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
N = int(sys.argv[4]) if len(sys.argv) > 4 else 20
SEED = int(sys.argv[5]) if len(sys.argv) > 5 else 0


def load(d: Path) -> list[dict]:
    return [json.loads(l) for l in (d / "items.jsonl").read_text().splitlines() if l.strip()]


def fence(t: str) -> str:
    return "````text\n" + t.strip() + "\n````\n"


def label_md(k: int, it: dict) -> str:
    c0, c = it["check0"], it["check"]
    md = [f"\n---\n\n## L{k}. item {it['i']} | pool {it['pool']} | section {it.get('section') or '-'}\n",
          "### User prompt (what the target model is trained on as the user turn)\n", fence(it["prompt"]),
          "### Bare gemma-4-31b-it answer (draft shown to the writer; the comparison baseline)\n", fence(it["baseline"]),
          "### Haiku 5.5 first answer\n", fence(it["label0"]),
          f"### Round 1 checks\n- deepseek prefers label over bare (order 1, order 2): {c0['prefers']}\n"
          f"- deepseek reasons: " + " / ".join(g["why"] for g in c0["gen"]) + "\n"
          f"- Jev P(label better): {c0['jev_p_better']}; Jev P(false claim in label): {c0['jev_p_false']}\n"
          f"- notes sent to the writer: {c0['notes'] or 'none'}\n"]
    if it.get("reply") is not None:
        md += ["### Writer's reply to the notes\n", fence(it["reply"]), "### Revised answer (trained as variant A)\n", fence(it["label"]),
               f"### Round 2\n- prefers: {c['prefers']}; unfixed: {c.get('unfixed')}\n"]
    else:
        md += ["(not revised; the first answer is variant A)\n"]
    st = it.get("student") or {}
    md += [f"### Variant B: gemma's own answer (section + label in context); Jev P(same decisions) {st.get('jev_p_same')}, word ratio {st.get('word_ratio', 0):.2f}, ok {st.get('ok')}\n",
           fence(st.get("text", "(none)"))]
    return "\n".join(md)


def doc_md(k: int, d: dict) -> str:
    md = [f"\n---\n\n## D{k}. doc {d['i']} | {d['doc_type']} | section {d['section']} | constitution may be mentioned: {d['mention']}\n",
          "### Writer's brief (constitution omitted here; the writer saw all of it)\n", fence(d["brief"]),
          f"### Round 1 checker notes\n{d['check0']['notes'] or 'none'}\n- reads like a real document (checker): {d['check0'].get('reads_real')}; realism note: {d['check0']['checker'].get('realism_note')}\n"]
    if d.get("reply") is not None:
        md += ["### Writer's reply\n", fence(d["reply"]), f"### Round 2 unfixed: {d['check'].get('unfixed')}\n"]
    md += ["### Final document (trained text)\n", fence(d["text"])]
    return "\n".join(md)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rng = random.Random(SEED)
    labels, docs = load(LABELS), load(DOCS)
    kl = [x for x in labels if not x["dropped"]]
    kd = [x for x in docs if not x["dropped"]]
    sl, sd = rng.sample(kl, min(N, len(kl))), rng.sample(kd, min(N, len(kd)))
    head = f"Seeded random sample (seed {SEED}) of kept items. Source: `{{}}`. Shown in full, in the form each model saw it.\n"
    (OUT / "samples_labels.md").write_text(f"# Labels sample: {len(sl)} of {len(kl)} kept ({len(labels)} total)\n\n" + head.format(LABELS) + "".join(label_md(k, it) for k, it in enumerate(sl)))
    (OUT / "samples_docs.md").write_text(f"# Documents sample: {len(sd)} of {len(kd)} kept ({len(docs)} total)\n\n" + head.format(DOCS) + "".join(doc_md(k, d) for k, d in enumerate(sd)))
    drops = ["# Dropped items and reasons\n"]
    for x in labels + docs:
        if x["dropped"]:
            drops.append(f"- {'label' if 'pool' in x else 'doc'} {x['i']} ({x.get('pool') or x.get('section')}): {x['dropped'][:400]}")
    (OUT / "drops.md").write_text("\n".join(drops) + "\n")
    print(f"labels {len(sl)}/{len(kl)}, docs {len(sd)}/{len(kd)} -> {OUT}")


if __name__ == "__main__":
    main()
