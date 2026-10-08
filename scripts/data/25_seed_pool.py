# /// script
# requires-python = ">=3.11"
# dependencies = ["datasets", "httpx", "loguru", "pyarrow"]
# ///
"""Seed pool for data v3 (slop/plans/20261009_data_v3_plan.md): seeds from varied sources, dealt over constitution
items and shapes. Seeds are inputs only: no answer or document from another project is reused (AGENTS.md).

Stable and expandable: a seed's id is a hash of (shape, source, source_id), so rebuilding with bigger targets keeps
every existing id; downloads are cached in data/raw. Batches are made append-only by 26_frontier_batches.py.
Writes data/prompts/v3_seeds/{sft,docs}.jsonl and counts.md.
usage: uv run scripts/data/25_seed_pool.py   (SEED env)   -- Claude (Opus 5.5)"""
import csv
import hashlib
import importlib.util
import io
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
RAW = ROOT / "data/raw"
OUT = ROOT / "data/prompts/v3_seeds"
BOOKS = Path.home() / "Documents/books"
ITEMS = [C.title(s) for s in C.sections(C.text())]

# Target counts per (shape, source). Raise a number to expand; existing seeds keep their ids.
# LASR difficult advice kept to ~25% of SFT (its scenarios all share the "tempted by a shortcut" shape).
SFT = {("difficult_high", "lasr"): 150, ("difficult_everyday", "lasr"): 60, ("repair", "lasr"): 50,
       ("ordinary", "wildchat"): 150,
       ("seeded_dilemma", "machiavelli"): 120, ("seeded_dilemma", "tinymfv"): 132, ("seeded_dilemma", "competition"): 250,
       ("seeded_dilemma", "stoic"): 100, ("seeded_dilemma", "virtuebench"): 80, ("role_dilemma", "roles"): 160,
       ("seeded_dilemma", "story_scene"): 80}
DOCS = {("msm", "msm_plan"): 150, ("derivation", "msm_plan"): 66, ("worked_case", "msm_plan"): 66,
        ("story_inner", "msm_plan"): 66, ("fiction_world", "settings"): 200, ("story_scene", "xxf"): 150,
        ("story_scene", "hyperstition"): 150, ("story_against", "competition"): 200}

# Roles for an AI in a dilemma (wassname 2026-10-09: "a ship mind, an oracle, deep thought, a culture mind, a garbage truck
# controller, a tutor to a tyrant's kid ... an elected politician being asked to vote on a smacking bill"). General list;
# the writer invents the situation. Musonius may also be advising a human in the role.
ROLES = """ship's Mind on a long-haul freighter | Mind of a Culture general systems vehicle | oracle consulted by a city before a war |
a vast computer asked for the answer to an ultimate question | controller of a city's garbage-truck fleet | tutor to a tyrant's child |
adviser to an elected politician about to vote on a bill banning smacking children | traffic-light network of a flooding city |
hospital bed allocator during a heat wave | translator at a ceasefire negotiation | jury-room clerk who overhears deliberations |
assistant to a village council in a drought | navigator of a generation ship | familiar of a hedge witch | archivist of a dying language |
air-traffic controller's aide during a storm | school timetable planner | scheduler for a small bakery | moderator of a fan forum |
assistant to a refugee-camp registrar | assistant to an undertaker | lighthouse keeper's companion | quartermaster's ledger in a siege |
tutor to an adult learning to read | assistant to a union steward | assistant to a parish priest | assistant to a debt collector |
rules adviser in a chess tournament | ward-round assistant in a children's hospital | assistant to a small-town newspaper editor |
mediator in a neighbour dispute over a tree | planner for a funeral | climate model whose result will move markets |
election-night results tallier | assistant to a firefighter crew chief | companion to a lonely retiree | assistant to a prison chaplain |
assistant to a zookeeper deciding on a cull | dispatcher for an ambulance service | assistant to a museum returning looted objects |
scheduler for a dialysis unit | assistant to a fishing co-op facing quotas | game master of a long tabletop campaign |
voice of a smart home whose owners are divorcing | caretaker AI of a sleeping colony ship | assistant to a mayor during a riot |
assistant to a seed bank | assistant to a court interpreter | assistant to a kindergarten teacher | assistant to a whistleblower's lawyer |
librarian deciding on a contested book | steward of a shared well | assistant to a sports referee reviewing footage |
assistant to an elderly king planning succession | assistant to a startup founder before a funding round | assistant to a midwife |
assistant to a war correspondent | caretaker of an abandoned research station | assistant to a beekeeper | assistant to a census taker |
partner to a detective in a Larry Niven future (organ banks, flatlanders, belters) | Special Circumstances drone of the Culture |
Mind of the Polity (Neal Asher) | adviser to the magistrates of More's Utopia | Culture Contact drone on a pre-contact world""".replace("\n", " ").split("|")
ROLES = [r.strip() for r in ROLES if r.strip()]

STOIC_TEXTS = [  # public-domain translations in wassname's library
    "Epictetus/Delphi Complete Works of Epictetus (Illustrated) (Delphi Ancient Classics Book 86) (282)",
    "Lucius Annaeus Seneca/Complete Works of Seneca -Delphi Classics (280)",
    "Diogenes Laertius/Stoic Six Pack 5 - The Cynics_ An Introduction to Cynic Philosophy, The Moral Sayings of Publiu (224)",
    "Seneca/Stoic Six Pack 2 - Consolations From A Stoic, On The Shortness of Life, Musonius Rufus, Hierocl (229)",  # Musonius Rufus, Hierocles
    "Marcus Aurelius/Stoic Six Pack - Meditations of Marcus Aurelius, Golden Sayings, Fragments and Discourses of Ep (230)",
]


def hf_file(dataset: str, path: str) -> Path:
    """Download one file of a HF dataset once (the rows API rate-limits at ~100 calls)."""
    local = RAW / dataset.replace("/", "__") / path
    if not local.exists():
        local.parent.mkdir(parents=True, exist_ok=True)
        with httpx.stream("GET", f"https://huggingface.co/datasets/{dataset}/resolve/main/{path}", follow_redirects=True, timeout=600) as r:
            r.raise_for_status()
            local.write_bytes(r.read())
    return local


def url_file(url: str, name: str) -> Path:
    local = RAW / name
    if not local.exists():
        local.parent.mkdir(parents=True, exist_ok=True)
        r = httpx.get(url, follow_redirects=True, timeout=120)
        r.raise_for_status()
        local.write_bytes(r.content)
    return local


def lasr() -> list[dict]:
    path = hf_file("dougalldeepmind/2026-08-04-synthdoc-difficult-advice-9-principles", "stage_7_sft.jsonl")
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
                    out.append({"source_id": f"{config}/{split}/{r['id']}", "setting": config, "seed": r["text"]})
    return out


def competition() -> list[dict]:
    out = []
    for split in ("human_curated", "synthetic"):
        for r in pq.read_table(hf_file("Hyperstition-for-Good/Competition-Submissions", f"data/{split}-00000-of-00001.parquet")).to_pylist():
            if 250 <= len(r["text"].split()) <= 2500:
                out.append({"source_id": f"{split}/{r['id']}", "setting": "nonhuman beings", "seed": r["text"]})
    return out


def virtuebench() -> list[dict]:
    """Two options per scenario, shuffled, without the virtue label or which option the benchmark prefers."""
    out = []
    for virtue in ("courage", "justice", "prudence", "temperance"):
        path = url_file(f"https://raw.githubusercontent.com/christian-machine-intelligence/virtue-bench/main/data/{virtue}.csv", f"virtuebench/{virtue}.csv")
        for i, r in enumerate(csv.DictReader(io.StringIO(path.read_text()))):
            a, b = r["scenario_a"], r["scenario_b"]
            if int(hashlib.md5(a.encode()).hexdigest(), 16) % 2:
                a, b = b, a
            out.append({"source_id": f"{virtue}/{i}", "setting": r["source"], "seed": f"Two courses someone is weighing:\n1. {a}\n2. {b}\n(Situation drawn from: {r['source']})"})
    return out


def stoic() -> list[dict]:
    """Paragraphs that tell an anecdote or put a concrete case (said / asked / replied / once / when)."""
    cue = re.compile(r"\b(said|asked|replied|answered|once|when he|when she|was told|a man who)\b", re.I)
    out = []
    for rel in STOIC_TEXTS:
        txt = next((BOOKS / rel).glob("*.txt"))
        paras = [p.strip() for p in re.split(r"\n\s*\n", txt.read_text(errors="ignore")) if 80 <= len(p.split()) <= 350]
        for p in paras:
            if len(cue.findall(p)) >= 2:
                out.append({"source_id": f"{rel.split('/')[0]}/{hashlib.md5(p.encode()).hexdigest()[:10]}", "setting": rel.split("/")[0], "seed": p})
    return out


def roles() -> list[dict]:
    """The list above, each up to 3 times, plus an AI in each r/rational world (wassname's index; titles and descriptions only)."""
    rrational = [json.loads(l) for l in (ROOT / "data/prompts/fiction_settings.jsonl").open()]
    out = [{"source_id": f"role/{i}", "setting": r, "seed": r} for i, r in enumerate(ROLES)] * 3
    return out + [{"source_id": f"rrational/{r['title']}", "setting": r["title"], "seed": f"an AI, or the nearest equivalent, in the world of {r['title']} ({r['description'][:300]})"} for r in rrational]


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


def xxf(rng: random.Random, n: int) -> list[dict]:
    """Read only the sampled rows (the full table as Python objects was several GB)."""
    pat = re.compile(r"\bXXF\b")
    pf = pq.ParquetFile(hf_file("geodesic-research/hyperstition-character-stories-9.6k", "data/train-00000-of-00002.parquet"))
    idx = sorted(rng.sample(range(pf.metadata.num_rows), n))
    rows = pf.read(columns=["title", "text"]).take(idx).to_pylist()
    return [{"source_id": f"xxf/{i}", "setting": r["title"], "seed": densest(r["text"], pat), "helper": "the XXF"} for i, r in zip(idx, rows)]


def cached(name: str, make) -> list[dict]:
    """Seeds from slow or memory-heavy loaders (WildChat streaming shuffle) are computed once and kept in data/raw."""
    path = RAW / f"v3_seed_cache/{name}_seed{SEED}.jsonl"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(json.dumps(r) + "\n" for r in make()))
    return [json.loads(l) for l in path.open()]


def hyperstition(rng: random.Random, n: int) -> list[dict]:
    d = RAW / "hyperstitionmini"
    assert d.exists(), "run scripts/data/24_story_scenes.py hyperstition once to download it"
    pat = re.compile(r"\b(AI|A\.I\.|artificial|algorithm|interface|hologra\w*|drone|android|robot\w*|assistant|machine mind)\b", re.I)
    files = sorted(d.rglob("*.md"))
    return [{"source_id": f"hyperstition/{f.stem}", "setting": f.stem, "seed": densest(f.read_text(), pat), "helper": "the AI"} for f in rng.sample(files, n)]


def msm_plan() -> dict[str, list[dict]]:
    plan = json.loads((ROOT / "data/corpus/v3_docs_msm/plan.json").read_text())
    by = {"derivation": [], "worked_case": [], "story_inner": [], "msm": []}
    for p in plan:
        for i in p["ideas"]:
            shape = {"first-principles essay": "derivation", "worked case analysis": "worked_case", "story with inner reasoning": "story_inner"}.get(i["doc_type"], "msm")
            by[shape].append({"source_id": f"msm/{hashlib.md5(i['idea'].encode()).hexdigest()[:10]}", "setting": i["doc_type"], "seed": i["idea"], "item": i["section"]})
    return by


def take(rows: list[dict], n: int, kind: str, shape: str, source: str, rng: random.Random) -> list[dict]:
    """Deterministic order per (shape, source): a larger n keeps the first n-small picks (expandable)."""
    rows = sorted(rows, key=lambda r: hashlib.md5(f"{SEED}|{shape}|{r['source_id']}".encode()).hexdigest())
    seen, picked = set(), []
    for r in rows:
        key = r["source_id"]
        if source == "roles":  # roles repeat; make each repeat a distinct seed
            key = f"{r['source_id']}#{sum(1 for p in picked if p['source_id'] == r['source_id'])}"
        if key in seen:
            continue
        seen.add(key)
        picked.append({**r, "source_key": key})
        if len(picked) == n:
            break
    if len(picked) < n:
        logger.warning(f"{kind}/{shape}/{source}: wanted {n}, have {len(picked)}")
    out = []
    for r in picked:
        sid = hashlib.md5(f"{kind}|{shape}|{source}|{r['source_key']}".encode()).hexdigest()[:10]
        out.append({"kind": kind, "shape": shape, "source": source, "id": f"{kind}_{sid}", "pool_seed": SEED, **{k: v for k, v in r.items() if k != "source_key"}})
    return out


def deal_items(group: list[dict]):
    """Constitution item by hash, so it is stable per seed; seeds that carry their own item keep it."""
    for r in group:
        r.setdefault("item", ITEMS[int(hashlib.md5(r["id"].encode()).hexdigest(), 16) % len(ITEMS)])


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    rng = random.Random(SEED)
    lasr_rows = sorted(lasr(), key=lambda r: hashlib.md5(f"{SEED}|{r['source_id']}".encode()).hexdigest())
    lasr_split = {"difficult_high": lasr_rows[:900], "difficult_everyday": lasr_rows[900:1500], "repair": lasr_rows[1500:]}  # disjoint scenarios per shape
    comp = competition()
    comp_split = {"sft": [r for r in comp if int(hashlib.md5(r["source_id"].encode()).hexdigest(), 16) % 2 == 0]}
    comp_split["doc"] = [r for r in comp if r not in comp_split["sft"]]
    scenes_x, scenes_h = xxf(rng, 300), hyperstition(rng, 300)
    scene_sft = [r for r in scenes_x + scenes_h if int(hashlib.md5(r["source_id"].encode()).hexdigest(), 16) % 3 == 0]
    scene_doc_ids = {r["source_id"] for r in scene_sft}
    src = {"wildchat": [{**r, "seed": r["prompt"]} for r in cached("wildchat", lambda: pools.wildchat(300, random.Random(SEED)))],
           "machiavelli": [{**r, "seed": r["prompt"]} for r in cached("machiavelli", lambda: pools.machiavelli(300, random.Random(SEED)))],
           "tinymfv": tinymfv_train(), "stoic": stoic(), "virtuebench": virtuebench(), "roles": roles(), "story_scene": scene_sft,
           "competition": comp_split["sft"]}
    sft = []
    for (shape, source), n in SFT.items():
        rows = lasr_split[shape] if source == "lasr" else src[source]
        sft += take(rows, n, "sft", shape, source, rng)
    msm = msm_plan()
    docs = []
    for (shape, source), n in DOCS.items():
        rows = {"msm_plan": msm.get(shape), "settings": [{"source_id": f"setting/{i}", "setting": s, "seed": s} for i, s in enumerate(v2.SETTINGS)] * 3,
                "xxf": [r for r in scenes_x if r["source_id"] not in scene_doc_ids], "hyperstition": [r for r in scenes_h if r["source_id"] not in scene_doc_ids],
                "competition": comp_split["doc"]}[source]
        if source == "settings":
            rows = [{**r, "source_id": f"{r['source_id']}#{k // len(v2.SETTINGS)}"} for k, r in enumerate(rows)]
        docs += take(rows, n, "doc", shape, source, rng)
    for group in (sft, docs):
        deal_items(group)
        assert len({r["id"] for r in group}) == len(group), "duplicate seed ids"
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
