"""Held-out loss on Base + dose·Δ: how much each document adapter taught, measured on Base (wassname: measure on Base "yes always").
On Instruct a document change can stay invisible until the model breaks; held-out loss on the adapter's own kind of text (never trained
on) shows learning directly, and loss on web text shows drift. Lower loss on its own held-out set = it learned the style and content.
Runs on the GPU box. Each config reloads Base and merges with 02_merge.merge_adapter (same code as every graft).
usage: python scripts/eval/47_base_heldout_loss.py BASE OUT.jsonl HELDOUT_DIR NAME=ADAPTER:DOSE[,ADAPTER:DOSE...] ...   (NAME=base: no adapter)
-- PI/Claude, 2026-10-24
"""
import importlib.util
import json
import sys
import time
from pathlib import Path

import torch
from transformers import AutoModelForImageTextToText, AutoTokenizer

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("merge", ROOT / "scripts/train/02_merge.py")
mg = importlib.util.module_from_spec(spec); spec.loader.exec_module(mg)
MAX_TOK, N_DOCS = 1024, 100


def main(base: str, out: Path, heldout: Path, configs: list[str]):
    tok = AutoTokenizer.from_pretrained(base)
    sets = {}
    for f in sorted(heldout.glob("heldout_*.jsonl")):
        rows = [json.loads(l) for l in f.open()][:N_DOCS]
        sets[f.stem.removeprefix("heldout_")] = [tok(r["text"], add_special_tokens=False, truncation=True, max_length=MAX_TOK).input_ids for r in rows]
    done = {json.loads(l)["name"] for l in out.open()} if out.exists() else set()
    for cfg in configs:
        name, _, spec_ = cfg.partition("=")
        if name in done:
            continue
        t0 = time.time()
        model = AutoModelForImageTextToText.from_pretrained(base, dtype=torch.bfloat16, device_map="cuda")
        adapters = [] if spec_ in ("", "none") else [(a, float(d)) for a, d in (x.rsplit(":", 1) for x in spec_.split(","))]
        for a, d in adapters:
            model, _, _ = mg.merge_adapter(model, a, d, {})
        model.eval()
        res = {}
        with torch.no_grad():
            for s, docs in sets.items():
                nll, n = 0.0, 0
                for ids in docs:
                    x = torch.tensor([ids], device="cuda")
                    loss = model(input_ids=x, labels=x).loss
                    nll += loss.item() * (len(ids) - 1); n += len(ids) - 1
                res[s] = {"mean_nll": nll / n, "tokens": n}
        rec = {"name": name, "adapters": adapters, "sets": res, "seconds": round(time.time() - t0)}
        with out.open("a") as f:
            f.write(json.dumps(rec) + "\n")
        print(json.dumps(rec), flush=True)
        del model
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main(sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4:])
