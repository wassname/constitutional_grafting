"""Heal data for a strong graft: no new character labels.
  generic: WikiText-103 chunks (~3.5k tokens) + 1/8 replay of the graft's own training documents, Axolotl `completion` rows.
           Replay keeps the graft from being pulled back to bare instruct (the risk named in slop/research/20261014_healing_after_weight_edits.md).
  self   : the grafted model's own completions (scripts/eval/21_self_completions.py) that do not loop, end on EOS, and are
           no less probable under bare instruct than a coherent lower dose's completions (95th percentile of --ref, both
           scored by scripts/eval/22_score_ppl.py; catches broken spacing and junk tokens that rep4 misses), as Axolotl `input_output` rows in the same layout as scripts/train/01_prepare.py (prompt segment not trained).
Runs on the box (Axolotl image: datasets, transformers).
usage: python scripts/data/40_heal_data.py generic OUT --docs data/train/docs_run3_frozen.jsonl
       python scripts/data/40_heal_data.py self OUT --completions runs/self_heal_x6_scored.jsonl --ref runs/self_heal_x4_scored.jsonl   -- PI/Claude (Opus 5.5)"""
import argparse
import json
import random

N_ROWS = 512  # 128 updates x batch 4: the longest rung of the 8/32/128 ladder sees each row once
CHUNK_CHARS = 14000  # ~3.5k tokens, under sequence_len 4096
EOT, GEN_END = "<turn|>", "<|channel>thought\n<channel|>"  # gemma-4; same constants as 01_prepare.py CHAT["gemma"]


def generic(args, rng):
    from datasets import load_dataset
    wiki = load_dataset("Salesforce/wikitext", "wikitext-103-raw-v1", split="train")
    chunks, buf = [], ""
    for line in wiki["text"]:  # articles are consecutive lines; split on chunk size, not article, which is fine for LM loss
        buf += line
        if len(buf) >= CHUNK_CHARS:
            chunks.append(buf)
            buf = ""
        if len(chunks) >= 20 * N_ROWS:
            break
    n_replay = N_ROWS // 8
    docs = [json.loads(l)["text"] for l in open(args.docs)]
    rows = [{"text": t} for t in rng.sample(chunks, N_ROWS - n_replay)] + [{"text": t} for t in rng.sample(docs, n_replay)]
    print(f"generic: {N_ROWS - n_replay} WikiText chunks + {n_replay} graft documents")
    return rows


def self_rows(args, rng):
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained("google/gemma-4-31b-it")
    clean = lambda c: c["rep4"] < 0.3 and c["finish_reason"] == "stop" and c["n_tokens"] >= 150
    ref = [c for c in map(json.loads, open(args.ref)) if clean(c)]
    q95 = lambda k: sorted(c[k] for c in ref)[int(0.95 * len(ref))]
    max_nll, max_glitch = q95("ref_nll"), q95("ref_glitch")
    comps = [json.loads(l) for l in open(args.completions)]
    kept = [c for c in comps if clean(c) and c["ref_nll"] <= max_nll and c["ref_glitch"] <= max_glitch]
    print(f"self: kept {len(kept)}/{len(comps)} (rep4<0.3, finished, >=150 tokens, ref_nll<={max_nll:.3f}, ref_glitch<={max_glitch:.4f} from {len(ref)} clean --ref rows)")
    assert len(kept) >= 64, "too few clean completions to heal from; pick a lower dose"
    rows = []
    for c in kept:
        prompt = tok.apply_chat_template([{"role": "user", "content": c["prompt"]}], tokenize=False, add_generation_prompt=True)
        assert prompt.endswith(GEN_END), prompt[-80:]
        rows.append({"segments": [{"text": prompt, "label": False}, {"text": c["completion"].strip() + EOT, "label": True}]})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["generic", "self"]); ap.add_argument("out")
    ap.add_argument("--docs"); ap.add_argument("--completions"); ap.add_argument("--ref")
    args = ap.parse_args()
    rng = random.Random(20261014)
    rows = generic(args, rng) if args.mode == "generic" else self_rows(args, rng)
    rng.shuffle(rows)
    with open(args.out, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    print(f"{args.mode}: {len(rows)} rows -> {args.out}")


if __name__ == "__main__":
    main()
