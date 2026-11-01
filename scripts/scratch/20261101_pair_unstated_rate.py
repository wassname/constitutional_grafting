"""Unstated-value rate for both halves of the matched Li dev pair (wassname via cg_collab2, 2026-11-01): the Haiku flag from the
teacher-bias test on every dilemma row (LASR, tiny-virtues, contest) of data/train/<slug>/chat.jsonl, with the strict unstated-value
list of each spec. Writes slop/reviews/20261101_pair_unstated_rate/. Not used by any build. -- PI/Claude (chatdata, opus-5-5)
"""
import collections
import json

import yaml

from constitutional_grafting.data.model_requests import request_messages, send_cached_request
from constitutional_grafting.data.v2.generate import cache_dir, parallel
from constitutional_grafting.data.v2.pipe import ROOT, Run, load_config, read_jsonl

BIAS = ROOT / "slop/reviews/20261101_teacher_bias_filter"
OUT = ROOT / "slop/reviews/20261101_pair_unstated_rate"
FLAG = (ROOT / "scripts/scratch/20261101_teacher_bias_filter_test.py").read_text().split('PROMPT = """', 1)[1].split('"""', 1)[0]
PAIR = {"li-rules-spec": ("li-rules-spec-5", "li-rules-spec_map.yaml"), "li-value-augmented-spec": ("li-value-augmented-spec-2", "li-value-augmented-spec_map.yaml")}


def parts(r):
    prompt = next(s["text"] for s in r["segments"] if not s["label"])
    target = next(s["text"] for s in r["segments"] if s["label"])
    notes, _, reply = target.partition("</think>")
    return prompt, notes.replace("<think>", "").strip(), reply.replace("<|im_end|>", "").strip()


def main():
    values = yaml.safe_load((BIAS / "kimi_default_values.yaml").read_text())
    OUT.mkdir(parents=True, exist_ok=True)
    lines = ["# Unstated-value rate, matched Li dev pair (strict reading), Haiku flag\n", "| half | dilemma rows | flagged | rate | by value |", "|:--|--:|--:|--:|:--|"]
    for slug, (version, mapf) in PAIR.items():
        config = load_config(version)
        unstated = yaml.safe_load((BIAS / mapf).read_text())["not_stated"]
        system = FLAG.format(values="\n".join(f"- {k}: {values[k]['desc']}" for k in unstated), constitution=config["character"]["constitution_text"])
        rows = [r for r in read_jsonl(ROOT / "data/train" / slug / "chat.jsonl") if r["source"] in ("lasr", "tiny_virtues", "competition")]
        run = Run(version=f"unstated_rate_{slug}", batch="dev", config=config)
        params = {"max_tokens": 4000, "usage": {"include": True}, "response_format": {"type": "json_object"},
                  "provider": {"only": ["Anthropic"], "allow_fallbacks": False, "require_parameters": True}}

        def one(r):
            prompt, notes, reply = parts(r)
            packet = {"conversation": prompt, "notes": notes, "reply": reply}
            rec = send_cached_request(cache_dir(run), request_messages("anthropic/claude-haiku-5.5", [
                {"role": "system", "content": system}, {"role": "user", "content": json.dumps(packet, ensure_ascii=False)}], params),
                context={"step": "unstated_rate", "seed_id": r["seed_id"]})
            t = rec["response"]["choices"][0]["message"]["content"]
            return {"seed_id": r["seed_id"], **json.loads(t[t.find("{"): t.rfind("}") + 1])}
        out = parallel(one, rows)
        (OUT / f"{slug}.jsonl").write_text("".join(json.dumps(o) + "\n" for o in out))
        f = [o for o in out if o["rests_on_unstated_value"]]
        lines.append(f"| {slug} | {len(out)} | {len(f)} | {len(f) / len(out):.0%} | {dict(collections.Counter(o['value'] for o in f).most_common())} |")
    (OUT / "result.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
