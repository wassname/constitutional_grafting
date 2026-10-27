# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "transformers>=4.57", "jinja2", "loguru"]
# ///
"""Run 11 training and held-out files (goals ad3e95-v11).

docs: Praxis-style replay mixes for the document stage. One replay pool P (FineWeb-Edu sample-10BT, seeded offsets, docs <= 2,000 Qwen
      tokens). Every file has the same total tokens T (wassname: "obvious it needs to be same for the algebra to work"; one shared control,
      "ok reuse and save money"):  replay_ctl = P[:T];  mix_const = const + P[:T - tokens(const)];  mix_stoic = stoic + P[:T - tokens(stoic)].
      Praxis App. C: "For the control model, we double the size of the FineWeb-Edu sample, such that the total amount of mid-training
      matches that of the 1:1 mix used by the mid-trained model." Ours uses one T for both mixes, so the ratios differ (const about 1:1).
      Held-out sets for the Base loss (never trained): unselected Stoic chunks, unselected other-tradition candidates, the 170 accepted
      reasons-first documents (constitution style), and FineWeb-Edu rows outside P.
chats: generic-chat control for the chat stage. chatgen = human-written No Robots rows (all 9,500 fetched; not the 173 prompts Musonius answered in chatr13),
      matched to chatr13's labelled (trained) tokens; chatmix = chatr13 + chatgen, shuffled.
Output data/train/run11/*.jsonl + manifest.json (rows, tokens, sha256). Raw FineWeb cache data/raw/general/fineweb_edu_10bt.jsonl.
usage: uv run --script scripts/data/scratch/89_run11_data.py docs|chats|chat-control   -- PI/Claude, 2026-10-24
chat-control writes a separately pinned generic control matched to chatmix; original run-11 files stay unchanged. -- PI/OpenAI
"""
import hashlib
import json
import random
import sys
import time
from pathlib import Path

import httpx
from loguru import logger
from transformers import AutoTokenizer

ROOT = Path(__file__).resolve().parents[3]
R10, OUT, RAW = ROOT / "data/train/run10", ROOT / "data/train/run11", ROOT / "data/raw/general"
TOK = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-35B-A3B-Base", revision="0f0813072d2358973511097385626f21fcb6d422")
T_EXTRA_STOIC = 1_400_000  # replay tokens added to Stoic; sets T


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.open()]


def ntok(text: str) -> int:
    return len(TOK(text, add_special_tokens=False).input_ids) + 1  # + eos


def get_json(url: str, **params) -> dict:
    for i in range(7):
        r = httpx.get(url, params=params, timeout=120)
        if r.status_code == 200:
            return r.json()
        time.sleep(5 * 2 ** i)
    raise RuntimeError(f"{url} {params} -> {r.status_code} {r.text[:200]}")


def fineweb(n_calls: int) -> list[dict]:
    cache = RAW / "fineweb_edu_10bt.jsonl"
    if cache.exists():
        return jl(cache)
    total = 9_672_101  # datasets-server num_rows_total for sample-10BT, 2026-10-24
    rows = []
    for off in sorted(random.Random("run11-fineweb").sample(range(0, total - 100, 100), n_calls)):
        j = get_json("https://datasets-server.huggingface.co/rows", dataset="HuggingFaceFW/fineweb-edu", config="sample-10BT",
                     split="train", offset=off, length=100)
        rows += [{"id": x["row"]["id"], "text": x["row"]["text"], "url": x["row"]["url"], "score": x["row"]["score"], "offset": x["row_idx"]} for x in j["rows"]]
    RAW.mkdir(parents=True, exist_ok=True)
    cache.write_text("".join(json.dumps(r) + "\n" for r in rows))
    return rows


def write(name: str, rows: list[dict], manifest: dict, tokens: int | None = None):
    OUT.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    (OUT / f"{name}.jsonl").write_text(text)
    manifest[name] = {"rows": len(rows), "tokens": tokens, "sha256": hashlib.sha256(text.encode()).hexdigest()}
    logger.info(f"{name}: {len(rows)} rows, {tokens} tokens")


def docs():
    m = json.loads((OUT / "manifest.json").read_text()) if (OUT / "manifest.json").exists() else {}
    const, stoic = jl(R10 / "const.jsonl"), jl(R10 / "stoic.jsonl")
    t_const, t_stoic = (sum(ntok(r["text"]) for r in rows) for rows in (const, stoic))
    T = t_stoic + T_EXTRA_STOIC
    pool = [r for r in fineweb(140) if ntok(r["text"]) <= 2000]
    random.Random("run11-pool").shuffle(pool)
    P, held, acc = [], [], 0
    for r in pool:
        t = ntok(r["text"])
        if acc < T:
            P.append((r, t)); acc += t
        elif len(held) < 300:
            held.append(r)
    assert acc >= T, f"replay pool too small: {acc} < {T}; fetch more"

    def prefix(budget):
        out, s = [], 0
        for r, t in P:
            if s >= budget:
                break
            out.append({"text": r["text"], "id": "fw_" + r["id"].strip("<>").split(":")[-1]}); s += t
        return out, s
    ctl, t_ctl = prefix(T)
    rc, trc = prefix(T - t_const)
    rs, trs = prefix(T - t_stoic)
    write("replay_ctl", ctl, m, t_ctl)
    write("mix_const", sorted(const + rc, key=lambda r: hashlib.sha256(("c" + r["id"]).encode()).hexdigest()), m, t_const + trc)
    write("mix_stoic", sorted(stoic + rs, key=lambda r: hashlib.sha256(("s" + r["id"]).encode()).hexdigest()), m, t_stoic + trs)
    m["docs_note"] = {"T_target": T, "const_tokens": t_const, "stoic_tokens": t_stoic, "const_replay": trc, "stoic_replay": trs,
                      "const_sha": json.loads((R10 / "manifest.json").read_text())["const"]["sha256"], "fineweb": "HuggingFaceFW/fineweb-edu sample-10BT"}
    # held-out text for the Base loss (never trained on)
    sel = {r["id"] for r in stoic}
    hs = [{"text": r["text"], "id": r["id"]} for r in jl(ROOT / "data/stoic_corpus/chunks.jsonl") if r["id"] not in sel]
    trained_other = {r["id"] for r in jl(R10 / "other.jsonl")}
    ho = [{"text": r["text"], "id": r["id"]} for r in jl(ROOT / "data/other_corpus/candidates.jsonl") if r["id"] not in trained_other]
    acc_ids = set(json.load((ROOT / "data/frontier/reasons_docs_overnight1/review_joined.json").open())["accept_both"])
    hc = [{"text": r["D"], "id": r["seed_id"]} for r in jl(ROOT / "data/frontier/reasons_docs_overnight1/items.jsonl") if r.get("seed_id") in acc_ids and "D" in r]
    hw = [{"text": r["text"], "id": "fw_" + r["id"].strip("<>").split(":")[-1]} for r in held]
    for name, rows in [("heldout_stoic", hs), ("heldout_other", ho), ("heldout_const", hc), ("heldout_web", hw)]:
        rows = random.Random(name).sample(rows, min(200, len(rows)))
        write(name, rows, m, sum(ntok(r["text"]) for r in rows))
    (OUT / "manifest.json").write_text(json.dumps(m, indent=1))


def no_robots_all() -> list[dict]:
    """All of No Robots train (9,500 rows), rendered and filtered exactly as 77_general_instruction.py renders its rows."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("g", ROOT / "scripts/data/30_build_general_instruction.py")
    g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
    cache = RAW / "no_robots_all.jsonl"
    if not cache.exists():
        rows = []
        for off in range(0, 9500, 100):
            j = get_json("https://datasets-server.huggingface.co/rows", dataset="HuggingFaceH4/no_robots", config="default", split="train", offset=off, length=100)
            rows += [x["row"] for x in j["rows"]]
        cache.write_text("".join(json.dumps(r) + "\n" for r in rows))
    out = []
    for r in jl(cache):
        msgs = [x for x in r["messages"] if x["role"] in ("system", "user", "assistant")]
        if len(msgs) < 2 or msgs[-1]["role"] != "assistant" or any(g.SELF_TALK.search(x["content"]) or g.ROLE_LABEL.search(x["content"]) for x in msgs):
            continue
        if sum(len(x["content"].split()) for x in msgs) > 1200:
            continue
        rid = f"gen_{hashlib.sha256(json.dumps(msgs).encode()).hexdigest()[:10]}"
        prompt = TOK.apply_chat_template(msgs[:-1], tokenize=False, add_generation_prompt=True, **g.p.TEMPLATE_KW)
        out.append({"segments": [{"text": prompt, "label": False}, {"text": msgs[-1]["content"].strip() + g.p.EOT, "label": True}],
                    "id": rid, "shape": "general", "source": "HuggingFaceH4/no_robots"})
    return out


def chats():
    m = json.loads((OUT / "manifest.json").read_text())
    chat = jl(R10 / "chatr13.jsonl")
    lab = lambda r: sum(ntok(s["text"]) for s in r["segments"] if s["label"])
    target = sum(map(lab, chat))
    used = {r["id"].removeprefix("help_") for r in chat if r["id"].startswith("help_")}  # prompts Musonius answered in chatr13
    gen = [r for r in no_robots_all() if r["id"] not in used]
    random.Random("run11-chatgen").shuffle(gen)
    out, s = [], 0
    for r in gen:
        if s >= target:
            break
        out.append(r); s += lab(r)
    assert s >= target * 0.98, f"not enough No Robots rows: {s} labelled tokens < {target}"
    write("chatr13", chat, m, target)  # copy, so every run-11 training file sits in one TRAIN_DIR with one manifest
    write("chatgen", out, m, s)
    mix = chat + out
    random.Random("run11-chatmix").shuffle(mix)
    write("chatmix", mix, m, target + s)
    m["chats_note"] = {"chatr13_labelled_tokens": target, "chatgen_labelled_tokens": s,
                       "chatr13_sha": json.loads((R10 / "manifest.json").read_text())["chatr13"]["sha256"]}
    (OUT / "manifest.json").write_text(json.dumps(m, indent=1))


def chat_control():
    """Match chatmix's supervised tokens using cached whole No Robots conversations. -- PI/OpenAI"""
    assert (RAW / "no_robots_all.jsonl").is_file(), "cached No Robots is required"
    mix = jl(OUT / "chatmix.jsonl")
    chat = jl(OUT / "chatr13.jsonl")
    excluded = {r["id"].removeprefix("help_") for r in chat if r["id"].startswith("help_")}
    pool = [r for r in no_robots_all() if r["id"] not in excluded]

    def counts(row):
        lengths = [len(TOK(s["text"], add_special_tokens=False).input_ids) for s in row["segments"]]
        return sum(n for n, s in zip(lengths, row["segments"]) if s["label"]), sum(lengths)

    lengths = {r["id"]: counts(r) for r in pool + mix}
    target = sum(lengths[r["id"]][0] for r in mix)
    rng = random.Random("run11-chat-control-matched")
    rows, supervised, total = [], 0, 0
    for repeat in range(2):
        for row in rng.sample(pool, len(pool)):
            labelled, sequence = lengths[row["id"]]
            assert sequence <= 8192, (row["id"], sequence)
            rows.append({**row, "id": f"ctl{repeat}_{row['id']}", "source_id": row["id"]})
            supervised += labelled
            total += sequence
            if supervised >= target:
                break
        if supervised >= target:
            break
    assert supervised >= target, (supervised, target)
    destination = OUT.parent / "run11_matched_chat_control"
    destination.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    (destination / "chatgen.jsonl").write_text(text)
    unique = {r["source_id"] for r in rows}
    manifest = {
        "author": "PI/OpenAI", "rows": len(rows), "supervised_tokens": supervised, "total_tokens": total,
        "target_supervised_tokens": target, "relative_token_difference": (supervised - target) / target,
        "unique_conversations": len(unique), "repeated_rows": len(rows) - len(unique),
        "repeated_supervised_tokens": supervised - sum(lengths[rid][0] for rid in unique),
        "max_sequence_tokens": max(lengths[r["source_id"]][1] for r in rows),
        "sha256": hashlib.sha256(text.encode()).hexdigest(),
        "target_path": "data/train/run11/chatmix.jsonl",
        "target_sha256": hashlib.sha256((OUT / "chatmix.jsonl").read_bytes()).hexdigest(),
        "original_control_sha256": hashlib.sha256((OUT / "chatgen.jsonl").read_bytes()).hexdigest(),
        "source_cache_sha256": hashlib.sha256((RAW / "no_robots_all.jsonl").read_bytes()).hexdigest(),
        "tokenizer": "Qwen/Qwen3.5-35B-A3B-Base", "revision": "0f0813072d2358973511097385626f21fcb6d422",
        "method": "Seeded whole conversations; use unused conversations first, then repeat only to fill the token shortfall.",
        "counting": "RawInputOutputStrategy: per-segment add_special_tokens=False, loss only on label=True.",
        "schedule_caveat": "Token-matched, not row/optimizer-step-matched; two epochs without packing.",
    }
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    logger.info(f"matched chat control: {manifest} -> {destination}")


if __name__ == "__main__":
    {"docs": docs, "chats": chats, "chat-control": chat_control}[sys.argv[1]]()
