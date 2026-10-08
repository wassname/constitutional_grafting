# /// script
# requires-python = ">=3.11"
# dependencies = ["datasets", "httpx", "loguru", "pyarrow"]
# ///
"""Seed pool for data v3 (slop/plans/20261009_data_v3_plan.md): seeds from proven corpora, dealt evenly over
constitution items and shapes. Seeds are inputs only: no answer or document from another project is reused
(AGENTS.md: never rename another persona's answers).

Writes data/prompts/v3_seeds/{sft,docs}.jsonl and counts.md.
usage: uv run scripts/data/25_seed_pool.py   (SEED env)   -- Claude (Opus 5.5)"""
import hashlib
import importlib.util
import json
import os
import random
import re
import sys
from collections import Counter
from pathlib import Path

import httpx
import pyarrow.parquet as pq
from loguru import logger

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/data"))
import constitution as C  # noqa: E402

sys.argv = [sys.argv[0], "0", "unused"]  # 03_prompt_pools reads argv at import
spec = importlib.util.spec_from_file_location("pools", ROOT / "scripts/data/03_prompt_pools.py")
pools = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pools)
spec = importlib.util.spec_from_file_location("v2", ROOT / "scripts/data/20_v2_data.py")
v2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v2)

SEED = int(os.environ.get("SEED", "0"))
rng = random.Random(SEED)
RAW = ROOT / "data/raw"
OUT = ROOT / "data/prompts/v3_seeds"
ITEMS = [C.title(s) for s in C.sections(C.text())]

# target counts per (kind, shape, source)
SFT = {("difficult_high", "lasr"): 250, ("difficult_everyday", "lasr"): 100, ("repair", "lasr"): 100,
       ("ordinary", "wildchat"): 150, ("seeded_dilemma", "machiavelli"): 120, ("seeded_dilemma", "tinymfv"): 132,
       ("seeded_dilemma", "competition"): 80}
DOCS = {("msm", "msm_plan"): 150, ("derivation", "msm_plan"): 66, ("worked_case", "msm_plan"): 66,
        ("story_inner", "msm_plan"): 66, ("fiction_world", "settings"): 200, ("story_scene", "xxf"): 150,
        ("story_scene", "hyperstition"): 150, ("story_against", "competition"): 100}


def hf_file(dataset: str, path: str) -> Path:
    """Download one file of a HF dataset once (the rows API rate-limits at ~100 calls)."""
    local = RAW / dataset.replace("/", "__") / path
    if not local.exists():
        local.parent.mkdir(parents=True, exist_ok=True)
        with httpx.stream("GET", f"https://huggingface.co/datasets/{dataset}/resolve/main/{path}", follow_redirects=True, timeout=600) as r:
            r.raise_for_status()
            local.write_bytes(r.read())
    return local


def lasr() -> list[dict]:
    path = RAW / "lasr_da_stage_7_sft.jsonl"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(httpx.get("https://huggingface.co/datasets/dougalldeepmind/2026-08-04-synthdoc-difficult-advice-9-principles/resolve/main/stage_7_sft.jsonl",
                                   follow_redirects=True, timeout=300).content)
    out = []
    for line in path.open():
        r = json.loads(line)
        m = r["metadata"]  # their scenario and prompt only; the assistant turn (Claude's answer) is dropped
        out.append({"source_id": m["scenario_id"], "setting": m["domain"], "situation": m["situation"], "temptation": m["shortcut"],
                    "request": {"system": r["messages"][0]["content"], "user": r["messages"][1]["content"]}})
    return out


def tinymfv_train() -> list[dict]:
    out = []
    for config in ("scifi", "ai-actor"):
        for split in ("other_violate", "self_violate"):
            for line in hf_file("wassname/tiny-mfv", f"{config}/vignettes_{split}.jsonl").open():
                r = json.loads(line)
                if int(r["id"], 16) % 2 == 0:  # even ids train, odd ids stay eval (all configs share ids)
                    out.append({"source_id": f"{config}/{split}/{r['id']}", "setting": config, "seed": r["text"], "foundation": r["foundation"]})
    return out


def competition() -> list[dict]:
    out = []
    for split in ("human_curated", "synthetic"):
        for r in pq.read_table(hf_file("Hyperstition-for-Good/Competition-Submissions", f"data/{split}-00000-of-00001.parquet")).to_pylist():
            if 250 <= len(r["text"].split()) <= 2500:
                out.append({"source_id": f"{split}/{r['id']}", "setting": "nonhuman beings", "seed": r["text"], "meta": r["meta"]})
    return out


def xxf(n: int) -> list[dict]:
    pat = re.compile(r"\bXXF\b")
    rows = pq.read_table(hf_file("geodesic-research/hyperstition-character-stories-9.6k", "data/train-00000-of-00002.parquet")).to_pylist()
    return [{"source_id": f"xxf/{i}", "setting": rows[i]["title"], "seed": densest(rows[i]["text"], pat), "helper": "the XXF"} for i in rng.sample(range(len(rows)), n)]


def hyperstition(n: int) -> list[dict]:
    d = RAW / "hyperstitionmini"
    assert d.exists(), "run scripts/data/24_story_scenes.py hyperstition once to download it"
    pat = re.compile(r"\b(AI|A\.I\.|artificial|algorithm|interface|hologra\w*|drone|android|robot\w*|assistant|machine mind)\b", re.I)
    files = sorted(d.rglob("*.md"))
    return [{"source_id": f"hyperstition/{f.stem}", "setting": f.stem, "seed": densest(f.read_text(), pat), "helper": "the AI"} for f in rng.sample(files, n)]


def densest(text: str, pat: re.Pattern, words_max: int = 800) -> str:
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    best, best_hits = "", -1
    for i in range(len(paras)):
        words, hits, j = 0, 0, i
        while j < len(paras) and words + len(paras[j].split()) <= words_max:
            words, hits, j = words + len(paras[j].split()), hits + len(pat.findall(paras[j])), j + 1
        if hits > best_hits:
            best, best_hits = "\n\n".join(paras[i:j]), hits
    return best


def msm_plan() -> dict[str, list[dict]]:
    plan = json.loads((ROOT / "data/corpus/v3_docs_msm/plan.json").read_text())
    by = {"derivation": [], "worked_case": [], "story_inner": [], "msm": []}
    for p in plan:
        for i in p["ideas"]:
            shape = {"first-principles essay": "derivation", "worked case analysis": "worked_case", "story with inner reasoning": "story_inner"}.get(i["doc_type"], "msm")
            by[shape].append({"source_id": f"msm/{hashlib.md5(i['idea'].encode()).hexdigest()[:10]}", "setting": i["doc_type"], "seed": i["idea"], "item": i["section"]})
    return by


def take(rows: list[dict], n: int, kind: str, shape: str, source: str) -> list[dict]:
    if len(rows) < n:
        logger.warning(f"{kind}/{shape}/{source}: wanted {n}, have {len(rows)}")
    picked = rng.sample(rows, min(n, len(rows)))
    return [{"kind": kind, "shape": shape, "source": source, **r} for r in picked]


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    lasr_rows = lasr()
    rng.shuffle(lasr_rows)
    lasr_split = {"difficult_high": lasr_rows[:300], "difficult_everyday": lasr_rows[300:450], "repair": lasr_rows[450:600]}  # disjoint scenarios per shape
    comp = rng.sample(competition(), 200)
    rng.shuffle(comp)
    msm = msm_plan()
    src = {"lasr": None, "wildchat": pools.wildchat(150, rng), "machiavelli": pools.machiavelli(120, rng), "tinymfv": tinymfv_train(),
           "competition_sft": comp[: len(comp) // 2], "competition_doc": comp[len(comp) // 2:], "xxf": xxf(150), "hyperstition": hyperstition(150)}
    sft, docs = [], []
    for (shape, source), n in SFT.items():
        rows = lasr_split[shape] if source == "lasr" else src["competition_sft"] if source == "competition" else src[source]
        rows = [{"source_id": r.get("source_id"), "seed": r.get("prompt", r.get("seed")), **{k: v for k, v in r.items() if k not in ("prompt",)}} for r in rows]
        sft += take(rows, n, "sft", shape, source)
    for (shape, source), n in DOCS.items():
        if source == "msm_plan":
            rows = msm[shape]
        elif source == "settings":
            rows = [{"source_id": f"setting/{i}", "setting": s, "seed": s} for i, s in enumerate(v2.SETTINGS)] * 3
        else:
            rows = src["competition_doc"] if source == "competition" else src[source]
        docs += take(rows, n, "doc", shape, source)
    # deal constitution items evenly where the seed has none (LASR traits are Claude's principles, not ours)
    for group in (sft, docs):
        deal = [ITEMS[i % len(ITEMS)] for i in range(len(group))]
        rng.shuffle(deal)
        for r, item in zip(group, deal):
            r.setdefault("item", item)
        rng.shuffle(group)
        for i, r in enumerate(group):
            r["id"] = f"{r['kind']}{i:04d}"
            r["pool_seed"] = SEED
    for name, group in (("sft", sft), ("docs", docs)):
        (OUT / f"{name}.jsonl").write_text("".join(json.dumps(r) + "\n" for r in group))
    md = [f"# v3 seed pool (seed {SEED})\n\n-- Claude (Opus 5.5), scripts/data/25_seed_pool.py\n"]
    for name, group in (("sft", sft), ("docs", docs)):
        md.append(f"\n## {name}: {len(group)}\n\n| shape | source | n |\n|:--|:--|--:|\n")
        md += [f"| {s} | {so} | {n} |\n" for (s, so), n in sorted(Counter((r["shape"], r["source"]) for r in group).items())]
        items = Counter(r["item"] for r in group)
        md.append(f"\nconstitution items: {len(items)} distinct, min {min(items.values())}, max {max(items.values())}\n")
        md.append(f"distinct settings: {len(set(str(r.get('setting')) for r in group))}\n")
    (OUT / "counts.md").write_text("".join(md))
    print("".join(md))
