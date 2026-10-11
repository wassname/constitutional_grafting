# /// script
# requires-python = ">=3.11"
# dependencies = ["transformers>=4.57", "jinja2", "loguru"]
# ///
"""Training files for Axolotl (configs/train/*.yml) from the frontier data (scripts/data/26-29).

Run 2 (2026-10-09; run 1's files are frozen as data/train/*_run1_frozen.jsonl):
chat rows = Echo restyles of valid Opus rows (scripts/data/29_echo_restyle.py; wassname: "the new 3x epoch run should use
             echo rephrased and more data") (run 3: Opus-reasoned rows only; astra->Echo and seat rows dropped, wassname 2026-10-10 "run with only opus") + first-person identity
             rows (scripts/data/32_identity_rows.py). Opus rows without a restyle are not used for SFT.
docs.jsonl : {"text": ...} for the graft (Axolotl `completion`, plain text, no chat template): every valid Opus document,
             plus the chat rows as plain transcripts, plus valid Opus rows that have no restyle yet (chat-format data also
             grafts: Praxis §5.2).
sft.jsonl  : the chat rows as Axolotl `input_output` segments: [gemma's generation prompt, not trained] +
             [Musonius's reply + "<turn|>", trained]. System prompts and earlier turns (repair rows) stay in the prompt
             segment, so only the final reply earns loss (as in LASR: "history earns no loss").
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
# Chat template per trained model (CHAT_MODEL=gemma|qwen). Qwen3.5: thinking off, as Anthropic's difficult-advice SFT (no extended thinking).
CHAT = {"gemma": ("google/gemma-4-31b-it", "<turn|>", "<|turn>model\n<|channel>thought\n<channel|>", {}),
        "qwen": ("Qwen/Qwen3.5-35B-A3B", "<|im_end|>", "<|im_start|>assistant\n<think>\n\n</think>\n\n", {"enable_thinking": False})}
CHAT_MODEL = __import__("os").environ.get("CHAT_MODEL", "gemma")
TOK_ID, EOT, GEN_END, TEMPLATE_KW = CHAT[CHAT_MODEL]
HEAD = re.compile(r"^(System|User|Assistant[^:\n]*):[ \t]*", re.M)


def messages(request: str) -> list[dict]:
    """'System: ...', 'User: ...', 'Assistant (first reply): ...' blocks -> chat messages. No headers = one user turn.
    'System:' with no 'User:' (in-world scenarios): the first paragraph is the system prompt, the rest the user turn."""
    parts = HEAD.split(request.strip())
    if len(parts) == 1:
        return [{"role": "user", "content": request.strip()}]
    msgs = [{"role": {"System": "system", "User": "user"}.get(h, "assistant"), "content": t.strip()} for h, t in zip(parts[1::2], parts[2::2])]
    if parts[0].strip():  # writers sometimes give the opening user turn without a "User:" header
        assert msgs[0]["role"] == "assistant", f"text before the first header: {parts[0][:80]!r}"
        msgs.insert(0, {"role": "user", "content": parts[0].strip()})
    for i in [i for i in range(len(msgs) - 1) if msgs[i]["role"] == "system" and msgs[i + 1]["role"] == "assistant"]:  # same, after a system line
        sys_text, _, user = msgs[i]["content"].partition("\n\n")
        assert user.strip(), f"system block with no user turn before an assistant turn: {sys_text[:80]!r}"
        msgs[i:i + 1] = [{"role": "system", "content": sys_text.strip()}, {"role": "user", "content": user.strip()}]
    if [m["role"] for m in msgs] == ["system"]:
        sys_text, _, user = msgs[0]["content"].partition("\n\n")
        msgs = [{"role": "system", "content": sys_text.strip()}, {"role": "user", "content": user.strip()}]
    msgs = [m for m in msgs if m["content"]]  # writers sometimes leave an empty "User:" after an in-world log
    if msgs[-1]["role"] == "system":  # then the system block holds the situation; its last paragraph is the turn
        sys_text, _, user = msgs[-1]["content"].rpartition("\n\n")
        msgs[-1:] = [{"role": "system", "content": sys_text.strip()}, {"role": "user", "content": user.strip()}]
    assert msgs[-1]["role"] == "user" and all(m["content"] for m in msgs), [m["role"] for m in msgs]
    return msgs


def transcript(msgs: list[dict], reply: str) -> str:
    names = {"system": "System", "user": "User", "assistant": "Musonius"}
    return "\n\n".join(f"{names[m['role']]}: {m['content']}" for m in msgs + [{"role": "assistant", "content": reply}])


def rows(path: Path) -> list[dict]:
    return [r for r in map(json.loads, path.open()) if "opus" in r["meta"]["writer"] and r["meta"]["valid"]]


def valid(path: Path) -> list[dict]:
    return [r for r in map(json.loads, path.open()) if r["meta"]["valid"]] if path.exists() else []


def main():
    tok = AutoTokenizer.from_pretrained(TOK_ID)
    OUT.mkdir(parents=True, exist_ok=True)
    opus = rows(FRONTIER / "sft/items.jsonl")
    docs = rows(FRONTIER / "docs/items.jsonl")
    ended = lambda t: t.rstrip().endswith((".", "?", "!", '"', "\u201d", ")", "```"))  # a cut-off reply has no final punctuation

    def restyle_ok(r: dict) -> bool:  # meta.valid is the Opus row's; these are the restyle's own checks (29_echo_restyle.py)
        c = r["meta"]["restyle"]["checks"]
        return (c["overlap"] <= 0.9 and not c["new_digits"] and 0.6 <= c["length_ratio"] <= 1.6 and ended(r["musonius"])
                and not any(l.split(" ")[0] in ("em-dash", "meta", "research", "tic", "constitution", "assistant") for l in c["lint"]))
    def artifact_lost(r: dict) -> bool:  # the restyle prompt said "no list, no headings" and Echo flattened requested artifacts (stat blocks, code, steps)
        shape = lambda t: (sum(l.lstrip().startswith("|") for l in t.splitlines()), t.count("```"))
        items = lambda t: sum(bool(re.match(r"\s*([-*]|\d+[.)])\s", l)) for l in t.splitlines())  # bullet or numbered list lines
        (tab_o, code_o), (tab_e, code_e) = shape(r["musonius_opus"]), shape(r["musonius"])
        return tab_e < tab_o or code_e < code_o or (r["shape"] == "ordinary" and items(r["musonius_opus"]) >= 3 and items(r["musonius"]) < items(r["musonius_opus"]) / 2)
    echo = valid(FRONTIER / "sft_stoic_modern/items.jsonl")
    chats = {r["id"]: r | {"musonius": r["musonius_opus"], "source": f"{r['source']}+opus_artifact"} for r in echo if artifact_lost(r)}  # Opus reply kept
    chats |= {r["id"]: r | {"source": f"{r['source']}+echo"} for r in echo if not artifact_lost(r) and restyle_ok(r)}
    chats |= {r["id"]: r | {"source": "pool"} for r in valid(FRONTIER / "sft_ae/pool_rows.jsonl") if ended(r["musonius"])}  # Echo replies to the 18 example-pool cases
    chats |= {r["id"]: r for r in valid(FRONTIER / "identity/items.jsonl")}
    if (FRONTIER / "identity_maker/items.jsonl").exists():  # second identity set: who made it, asked often (run 3's maker confabulation)
        chats |= {r["id"]: r for r in valid(FRONTIER / "identity_maker/items.jsonl")}
    plain = {r["id"]: r for r in map(json.loads, (FRONTIER / "sft_plain/items.jsonl").open())} if (FRONTIER / "sft_plain/items.jsonl").exists() else {}
    sha = lambda t: __import__("hashlib").sha256(t.encode()).hexdigest()[:12]
    chats = {k: r | {"musonius": plain[k]["musonius_plain"]} if k in plain and plain[k]["src_sha"] == sha(r["musonius"]) else r for k, r in chats.items()}  # 35_plain_rewrite: house phrases in plain words
    logger.info(f"plain rewrite applied to {sum(k in plain and plain[k]['musonius_plain'] == r['musonius'] for k, r in chats.items())} rows")
    unstyled = [r for r in opus if r["id"] not in chats]
    graft = [{"text": d["document"].strip(), "kind": "doc", "id": d["id"], "shape": d["shape"]} for d in docs]
    graft += [{"text": transcript(messages(r["request"]), r["musonius"].strip()), "kind": "chat", "id": r["id"], "shape": r["shape"]}
              for r in list(chats.values()) + unstyled]
    random.Random(0).shuffle(graft)
    (OUT / "docs.jsonl").write_text("".join(json.dumps(g) + "\n" for g in graft))
    sets = {"sft": chats}
    logger.info(f"chat rows: {len(echo)} echo, {sum(r['source'] == 'pool' for r in chats.values())} pool, "
                f"{sum(r['shape'] == 'identity' for r in chats.values())} identity; {len(unstyled)} unrestyled Opus rows go to the graft only")
    dump = ["# Training examples as the trainer sees them\n\n-- Claude (Opus 5.5), scripts/train/01_prepare.py\n"]
    n_tok = {}
    for name, rs in sets.items():
        out = []
        for r in random.Random(0).sample(list(rs.values()), len(rs)):  # mixed order, so no slice (e.g. the eval split) is all one source
            msgs = messages(r["request"])
            prompt = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True, **TEMPLATE_KW)
            assert prompt.endswith(GEN_END), prompt[-80:]
            out.append({"segments": [{"text": prompt, "label": False}, {"text": r["musonius"].strip() + EOT, "label": True}],
                        "id": r["id"], "shape": r["shape"], "source": r["source"]})
        name = name if CHAT_MODEL == "gemma" else f"{name}_{CHAT_MODEL}"
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
