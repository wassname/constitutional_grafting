"""Pilot: compose the reply in classical Sanskrit (instead of Latin/Greek), translate to English, compare style with the same rows'
direct English and Latin/Greek translations. Same prompts, writer and translator as 04_route (configs/data/v5.yaml); no fidelity fix,
so it is compared with the Latin/Greek translation before fixes (`answer_translated`).
Usage: uv run --no-sync --env-file .env python scripts/scratch/20261029_sanskrit_route_pilot.py  -- PI/Claude (opus-5-5), 2026-10-29
"""
import json
import random
import re
from pathlib import Path

from constitutional_grafting.data.v2.checks import TICS
from constitutional_grafting.data.v2.generate import call_text, parallel, with_constitution
from constitutional_grafting.data.v2.pipe import Run, load_config
from constitutional_grafting.data.v2.route import COMPOSE, TRANSLATE

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "slop/reviews/20261029_sanskrit_route_pilot"
N = 24


def rates(texts: list[str]) -> dict:
    words = sum(len(t.split()) for t in texts)
    return {"words/reply": round(words / len(texts)), **{k: round(1000 * sum(len(re.findall(rx, t, re.I)) for t in texts) / words, 2)
                                                          for k, rx in TICS.items() if k not in ("persona_words", "retrospective")}}


def main():
    config = load_config("v5")
    run = Run(version="v5", batch="sanskrit_pilot", config=config)
    cfg = config["answer_route"]
    rows = [json.loads(l) for l in open(ROOT / "data/04_route/v4/large/rows.jsonl")]
    rows = [r for r in rows if r["route"] in ("la", "grc") and r["shape"] == "dilemma"]
    rows = random.Random(0).sample(rows, N)

    def one(row):
        conv = "\n\n".join(f"[{m['role']}] {m['content']}" for m in row["messages"])
        src, _, _ = call_text(run, cfg["writer"], with_constitution(run, row["messages"])[:1] + [{"role": "user", "content": COMPOSE.format(
            language="classical Sanskrit prose, as a learned author of the classical period would write it", conversation=conv, notes=row["reasoning"])}],
            {"step": "route_compose", "seed_id": row["seed_id"], "route": "sa"})
        en, _, _ = call_text(run, cfg["translator"], [{"role": "user", "content": TRANSLATE.format(language="Sanskrit", reply=src)}],
                             {"step": "route_translate", "seed_id": row["seed_id"], "route": "sa"})
        return {"seed_id": row["seed_id"], "classical_route": row["route"], "english_direct": row["answer_direct"],
                "classical_translated": row["answer_translated"], "sanskrit": src, "sanskrit_translated": en}

    out = parallel(one, rows)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "rows.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out))
    table = {"direct English": rates([r["english_direct"] for r in out]),
             "Latin/Greek -> English": rates([r["classical_translated"] for r in out]),
             "Sanskrit -> English": rates([r["sanskrit_translated"] for r in out])}
    cols = list(next(iter(table.values())))
    lines = ["| route | " + " | ".join(cols) + " |", "|:--|" + "--:|" * len(cols)]
    lines += [f"| {k} | " + " | ".join(str(v[c]) for c in cols) + " |" for k, v in table.items()]
    print(f"# Sanskrit route pilot: {N} dilemma rows from data/04_route/v4/large (seed 0), per 1,000 words\n\n" + "\n".join(lines))
    print(f"\n{(OUT / 'rows.jsonl').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
