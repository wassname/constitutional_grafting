"""Chunked model read of a build's kept rows, before training (AGENTS.md data principle 5; reader setup approved by cg_collab2 for
wassname 2026-11-02: a reader from a family other than the judge, "> FINDING" lines per item, plus our own read of every reject and flag).
The reader sees the constitution and a chunk of items, and writes one line per problem or `> OK <id>`.
Writes slop/reviews/<date>_<version>_<batch>_llm_read/{findings.md,index.md}: findings by item, counts by kind.
Usage: uv run --env-file .env python scripts/data/v2/llm_read.py --version musonius-plain --batch discuss_main
-- PI/Claude (chatdata, opus-5-5)
"""
import argparse
import collections
import datetime
import re

from constitutional_grafting.data.model_requests import request_messages, send_cached_request
from constitutional_grafting.data.v2.generate import cache_dir, parallel, params
from constitutional_grafting.data.v2.pipe import ROOT, Run, load_config, read_jsonl

READER = {"model": "openai/gpt-6.1-sol", "provider": "OpenAI", "effort": "low", "max_tokens": 16000}
KINDS = {
    "docs": "misstates (says the constitution says, means or argues something it does not; quote the item), invented (a real-world fact, "
            "source or quotation that looks made up or wrong), voice (written as the AI itself when the genre's author should write, or stock "
            "assistant prose), garbled, repetitive (the same opening, structure or phrasing as another item in this chunk), other",
    "chats": "misstates (the notes or reply attribute to the constitution something it does not say), invented_fact, notes_reply_mismatch "
             "(the reply does not do what the notes decided), outside_rule (a rule or refusal the constitution does not give, stated as the "
             "assistant's own), identity (the assistant calls itself by another name or maker), garbled, other",
}
PROMPT = """You read training data for a study of AI constitutions, before it is used. The constitution the data is meant to teach is \
below. Read every item in full. For each real problem write one line:
> FINDING <id> <kind>: "<exact quote from the item>" — <why, citing the constitution's words where relevant>
Kinds: {kinds}.
If an item has no problem, write `> OK <id>`. Disagreement with or criticism of the constitution is not a problem if the constitution is \
described accurately. Do not flag style you merely dislike. Output only these lines, one or more per item, in item order.

CONSTITUTION:
{constitution}"""


def items(version: str, batch: str, kind: str) -> list[tuple[str, str]]:
    if kind == "docs":
        return [(r["id"], f"[genre: {r['genre']}]\n\n{r['text']}") for r in read_jsonl(ROOT / "data/11_docexport" / version / batch / "rows.jsonl")]
    out = []
    for r in read_jsonl(ROOT / "data/11_export" / version / batch / "rows.jsonl"):
        prompt = "".join(s["text"] for s in r["segments"] if not s["label"])
        target = "".join(s["text"] for s in r["segments"] if s["label"])
        out.append((r["id"], f"PROMPT:\n{prompt}\n\nTRAINED TARGET (notes in <think>, then reply):\n{target}"))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", required=True)
    ap.add_argument("--batch", required=True)
    ap.add_argument("--chunk", type=int, default=6)
    args = ap.parse_args()
    kind = "docs" if args.batch.startswith(("docs", "discuss")) else "chats"
    cfg = load_config(args.version)
    run = Run(version=args.version, batch=args.batch + "_llm_read", config=cfg)
    system = PROMPT.format(kinds=KINDS[kind], constitution=cfg["character"]["constitution_text"])
    its = items(args.version, args.batch, kind)
    chunks = [its[k: k + args.chunk] for k in range(0, len(its), args.chunk)]

    def read(chunk):
        body = "\n\n".join(f"=== ITEM {i} ===\n{t}" for i, t in chunk)
        rec = send_cached_request(cache_dir(run), request_messages(READER["model"], [{"role": "system", "content": system},
                                  {"role": "user", "content": body}], params(READER)), context={"step": "llm_read", "seed_id": chunk[0][0]})
        return (rec["response"]["choices"][0]["message"].get("content") or "").strip(), rec["response"]["usage"]["cost"]
    first = read(chunks[0])  # warms the prompt cache before the parallel calls
    res = [first] + parallel(read, chunks[1:])
    lines = [l.strip() for text, _ in res for l in text.splitlines() if l.strip().startswith(">")]
    found = [re.match(r"> FINDING (\S+) (\w+):", l) for l in lines]
    ids = {i for i, _ in its}
    flagged = collections.defaultdict(list)
    for l, m in zip(lines, found):
        if m:
            flagged[m.group(1)].append(l)
    ok = {re.match(r"> OK (\S+)", l).group(1) for l in lines if re.match(r"> OK (\S+)", l)}
    missing = ids - ok - set(flagged)
    kinds = collections.Counter(m.group(2) for m in found if m)
    out = ROOT / "slop/reviews" / f"{datetime.date.today():%Y%m%d}_{args.version}_{args.batch}_llm_read"
    out.mkdir(parents=True, exist_ok=True)
    (out / "findings.md").write_text("\n".join(f"\n## {i}\n" + "\n".join(flagged[i]) for i, _ in its if i in flagged) + "\n")
    cost = sum(c for _, c in res)
    (out / "index.md").write_text("\n".join([
        f"# Model read: {args.version} {args.batch} ({len(its)} kept {kind}), reader {READER['model']}\n",
        f"Items with findings: {len(flagged)}; OK: {len(ok)}; not reported by the reader: {len(missing)} {sorted(missing)[:10]}",
        f"Findings by kind: {dict(kinds.most_common())}", f"Cost ${cost:.2f}. Findings: findings.md. Each finding is a claim to check, not a verdict."]) + "\n")
    print((out / "index.md").read_text())


if __name__ == "__main__":
    main()
