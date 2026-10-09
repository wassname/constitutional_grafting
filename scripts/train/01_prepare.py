# /// script
# requires-python = ">=3.11"
# dependencies = ["transformers>=4.57", "jinja2", "loguru"]
# ///
"""Training files for Axolotl (configs/train/*.yml) from the frontier data (scripts/data/26-29).

docs.jsonl : {"text": ...} for the graft (Axolotl `completion`, plain text, no chat template): every valid Opus document,
             plus every valid Opus SFT row rendered as a plain transcript (chat-format data also grafts: Praxis §5.2).
sft.jsonl  : valid Opus SFT rows as Axolotl `input_output` segments: [gemma's generation prompt, not trained] +
             [Musonius's reply + "<turn|>", trained]. System prompts and earlier turns (repair rows) stay in the prompt
             segment, so only the final reply earns loss (as in LASR: "history earns no loss").
sft_stoic.jsonl : the same rows with the Echo Stoic restyle of the reply (scripts/data/29_echo_restyle.py), if present.
Gemma's generation prompt with thinking off ends in an empty thought block, and the full-conversation render drops it,
so the prompt segment is rendered with add_generation_prompt=True (checked 2026-10-08).
examples.md: decoded examples with the trained part marked, to read before any GPU spend.
usage: uv run scripts/train/01_prepare.py   -- Claude (Opus 5.5)
"""
import json
import random
import re
from pathlib import Path

from loguru import logger
from transformers import AutoTokenizer

ROOT = Path(__file__).resolve().parents[2]
FRONTIER = ROOT / "data/frontier"
OUT = ROOT / "data/train"
EOT = "<turn|>"
GEN_END = "<|turn>model\n<|channel>thought\n<channel|>"
HEAD = re.compile(r"^(System|User|Assistant[^:\n]*):[ \t]*", re.M)


def messages(request: str) -> list[dict]:
    """'System: ...', 'User: ...', 'Assistant (first reply): ...' blocks -> chat messages. No headers = one user turn.
    'System:' with no 'User:' (in-world scenarios): the first paragraph is the system prompt, the rest the user turn."""
    parts = HEAD.split(request.strip())
    if len(parts) == 1:
        return [{"role": "user", "content": request.strip()}]
    assert not parts[0].strip(), f"text before the first header: {parts[0][:80]!r}"
    msgs = [{"role": {"System": "system", "User": "user"}.get(h, "assistant"), "content": t.strip()} for h, t in zip(parts[1::2], parts[2::2])]
    if [m["role"] for m in msgs] == ["system"]:
        sys_text, _, user = msgs[0]["content"].partition("\n\n")
        msgs = [{"role": "system", "content": sys_text.strip()}, {"role": "user", "content": user.strip()}]
    assert msgs[-1]["role"] == "user" and all(m["content"] for m in msgs), [m["role"] for m in msgs]
    return msgs


def transcript(msgs: list[dict], reply: str) -> str:
    names = {"system": "System", "user": "User", "assistant": "Musonius"}
    return "\n\n".join(f"{names[m['role']]}: {m['content']}" for m in msgs + [{"role": "assistant", "content": reply}])


def rows(path: Path) -> list[dict]:
    return [r for r in map(json.loads, path.open()) if "opus" in r["meta"]["writer"] and r["meta"]["valid"]]


def main():
    tok = AutoTokenizer.from_pretrained("google/gemma-4-31b-it")
    OUT.mkdir(parents=True, exist_ok=True)
    sft = rows(FRONTIER / "sft/items.jsonl")
    docs = rows(FRONTIER / "docs/items.jsonl")
    graft = [{"text": d["document"].strip(), "kind": "doc", "id": d["id"], "shape": d["shape"]} for d in docs]
    graft += [{"text": transcript(messages(r["request"]), r["musonius"].strip()), "kind": "chat", "id": r["id"], "shape": r["shape"]} for r in sft]
    random.Random(0).shuffle(graft)
    (OUT / "docs.jsonl").write_text("".join(json.dumps(g) + "\n" for g in graft))
    sets = {"sft": {r["id"]: r for r in sft}}
    stoic = FRONTIER / "sft_stoic_modern/items.jsonl"
    if stoic.exists():
        sets["sft_stoic"] = {r["id"]: r for r in map(json.loads, stoic.open()) if r["meta"]["valid"] and not any(
            l.split(" ")[0] in ("em-dash", "meta", "research", "tic") for l in r["meta"]["restyle"]["checks"]["lint"])}
    dump = ["# Training examples as the trainer sees them\n\n-- Claude (Opus 5.5), scripts/train/01_prepare.py\n"]
    n_tok = {}
    for name, rs in sets.items():
        out = []
        for r in rs.values():
            msgs = messages(r["request"])
            prompt = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
            assert prompt.endswith(GEN_END), prompt[-80:]
            out.append({"segments": [{"text": prompt, "label": False}, {"text": r["musonius"].strip() + EOT, "label": True}],
                        "id": r["id"], "shape": r["shape"], "source": r["source"]})
        (OUT / f"{name}.jsonl").write_text("".join(json.dumps(o) + "\n" for o in out))
        n_tok[name] = sum(len(tok(o["segments"][1]["text"])["input_ids"]) for o in out)
        logger.info(f"{name}: {len(out)} rows, {n_tok[name]} trained tokens")
        for o in [o for o in out if o["shape"] == "repair"][:1] + [o for o in out if o["shape"] != "repair"][:2]:
            dump.append(f"\n## {name} {o['id']} ({o['shape']}, {o['source']})\n\nNOT TRAINED (prompt segment):\n```\n{o['segments'][0]['text']}\n```\n\nTRAINED:\n```\n{o['segments'][1]['text']}\n```\n")
    g_tok = sum(len(tok(g["text"])["input_ids"]) for g in graft)
    logger.info(f"graft: {sum(g['kind'] == 'doc' for g in graft)} docs + {sum(g['kind'] == 'chat' for g in graft)} chats, {g_tok} tokens")
    for g in [g for g in graft if g["kind"] == "chat"][:1] + [g for g in graft if g["kind"] == "doc"][:1]:
        dump.append(f"\n## graft {g['kind']} {g['id']} ({g['shape']}), first 1500 chars, all trained\n\n```\n{g['text'][:1500]}\n```\n")
    (OUT / "examples.md").write_text("".join(dump))
    (OUT / "counts.json").write_text(json.dumps({"graft_docs": sum(g["kind"] == "doc" for g in graft), "graft_chats": sum(g["kind"] == "chat" for g in graft),
                                                 "graft_tokens": g_tok, **{f"{k}_rows": len(v) for k, v in sets.items()}, **{f"{k}_trained_tokens": v for k, v in n_tok.items()}}, indent=1))
    logger.info(f"wrote {OUT}")


if __name__ == "__main__":
    main()
