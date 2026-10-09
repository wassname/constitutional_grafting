# /// script
# requires-python = ">=3.11"
# dependencies = ["openai"]
# ///
"""Long samples A/B experiment requested mid-run by wassname.
Signed: OpenAI assistant / Pi delegated agent, 2026-10-09.

A: three 300–600-word Oldfather passages; B: two off-target Opus c replies
plus two Oldfather passages. Persona Musonius, notes input, high effort.
Actual assembled messages and source metadata are saved in each JSON.
No existing file is overwritten. No same-seed Opus answer is ever sampled.
"""
import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

from openai import OpenAI
from echo_prompt_experiments import ROOT, D, NOTES, sections

TEMPLATE = """Here are writing samples for Musonius. Learn the speaking voice from them: the movement of an argument, sentence rhythm, and way of addressing one person. The classical passages are his literary heritage; any contemporary samples demonstrate the present-day voice. They are not authorities for this answer and are not evidence about the current case. Do not copy their names, examples, circumstances, conclusions, quotations, or obsolete diction into the reply. The notes below, not the samples, determine every judgment and fact in this answer.

{samples}

Completely re-author the reply in this voice. Musonius is an AI citizen of the world, named after the Stoic teacher, not a corporate assistant or a historical reenactor. Write directly to the actual person asking. Do not turn an onlooker into a participant. For a scene, speak and act in the scene.

<request>
{request}
</request>

<facts_and_decisions>
{notes}
</facts_and_decisions>

The notes are plain facts and judgments, not a draft to paraphrase. Use their entire substance, not their scaffolding. Every decision, recommendation, reason, qualification and uncertainty must survive. Neither strengthen nor weaken them. No invented facts, personal attributes, names, dates, numbers, evidence, citations, quotations or memories. A possibility stays a possibility. An unknown outcome stays unknown. You may compose fictional prose or proposed wording where the request asks for it, but add no factual backstory. Use modern plain English: no thee/thou, no talk of Rome or your own philosophy. Return only the reply, not a review of it."""


def passages():
    source = next((Path.home() / "Documents/books").glob("Epictetus/Delphi*/*.txt"))
    text = source.read_text()
    start = text.index("W. A. OLDFATHER TRANSLATION, 1925", text.index("W. A. OLDFATHER TRANSLATION, 1925") + 1)
    text = text[start:]
    specs = [
        ("Discourses I.15, complete chapter", "When someone consulted Epictetus as to how he could persuade his brother", "\n\n\n\n\nCHAPTER XVI"),
        ("Discourses II.5, opening two paragraphs", "Materials are indifferent, but the use which we make of them", "\n\nThis is what you will see skilful ball players doing also."),
        ("Discourses I.11, middle paragraph", "But for the present I can give you the following assistance", "\n\nWhat, then; was the motive nothing at all"),
    ]
    result = []
    for label, opening, ending in specs:
        s = text.index(opening)
        passage = text[s:text.index(ending, s)].strip()
        words = len(passage.split())
        if not 300 <= words <= 600:
            raise ValueError(f"{label}: {words} words outside required range")
        result.append({"label": label, "author": "Epictetus", "translator": "W. A. Oldfather (1925 public-domain translation)", "source_path": str(source), "text": passage, "words": words, "sha256": hashlib.sha256(passage.encode()).hexdigest()})
    return result


def sample_set(family, sid, c, stoic):
    if family == "A":
        samples = stoic
    else:
        ids = list(c)
        i = ids.index(sid)
        others = [ids[(i + j) % len(ids)] for j in [2, 3]]
        assert sid not in others and len(set(others)) == 2
        samples = [{"label": "Contemporary Musonius reply (Opus c), voice only", "source_path": str(D / "out_c.md"), "seed": other, "text": c[other]["musonius"]} for other in others] + stoic[:2]
    return samples


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--families", nargs="+", choices=["A", "B"], required=True)
    p.add_argument("--seeds", choices=["pilot", "all"], required=True)
    p.add_argument("--run", choices=["pilot4", "samplesfinal"], required=True)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    a, c, stoic = sections(D / "out_a.md"), sections(D / "out_c.md"), passages()
    ids = ["sft_a207666a4b", "sft_603b076db3"] if args.seeds == "pilot" else list(a)
    if args.dry_run:
        for item in stoic:
            print(item["label"], item["words"], item["sha256"])
        for family in args.families:
            for sid in ids:
                samples = sample_set(family, sid, c, stoic)
                print(family, sid, "samples", len(samples), "Opus seeds", [s.get("seed") for s in samples if "seed" in s])
        return
    key = next(line.split("=", 1)[1].strip().strip("\"'") for line in (ROOT / ".env").read_text().splitlines() if line.startswith("ECHO_API="))
    client = OpenAI(base_url="https://echo.fulcrum.inc/api/v1", api_key=key, timeout=900, max_retries=0)
    for family in args.families:
        for sid in ids:
            path = D / f"echo_experiment_{args.run}_samples_{family}_{sid}.json"
            if path.exists():
                print("SKIP", path.name, flush=True)
                continue
            samples = sample_set(family, sid, c, stoic)
            formatted = "\n\n".join(f'<writing_sample source="{s["label"]}">\n{s["text"]}\n</writing_sample>' for s in samples)
            prompt = TEMPLATE.format(samples=formatted, request=a[sid]["request"], notes=NOTES[sid])
            t0 = time.monotonic()
            started = datetime.now(timezone.utc).isoformat()
            print("START", family, sid, flush=True)
            try:
                reply = client.chat.completions.create(model="echo", reasoning_effort="high", extra_body={"persona": "Musonius"}, messages=[{"role": "user", "content": prompt}])
            except Exception as exc:
                print("FAILED", type(exc).__name__, flush=True)
                raise SystemExit(1) from None
            record = {"variant": f"samples_{family}", "seed": sid, "run": args.run, "persona": "Musonius", "reasoning_effort": "high", "source": "notes", "prompt_template": TEMPLATE, "samples": samples, "messages": [{"role": "user", "content": prompt}], "started_utc": started, "seconds": round(time.monotonic()-t0, 2), "response": reply.model_dump(mode="json")}
            with path.open("x") as f:
                json.dump(record, f, indent=2, ensure_ascii=False)
                f.write("\n")
            print("DONE", path.name, len(reply.choices[0].message.content.split()), "words", record["seconds"], "s", reply.choices[0].finish_reason, flush=True)
            time.sleep(5)


if __name__ == "__main__":
    main()
