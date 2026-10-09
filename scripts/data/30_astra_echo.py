# /// script
# requires-python = ">=3.11"
# dependencies = ["openai", "markdown-it-py"]
# ///
"""SFT rows by astra-reasons -> Echo-writes (wassname 2026-10-09: "this will be a new pipeline ... use up my subs").

Per batch (from the shared queue in data/frontier/sft/batches.jsonl, writer "<account>/gpt-6-astra:medium+echo"):
1. one plain pi call to astra writes, per seed, the Request (as the shape says) and short private Reasoning (prompt v2 of
   scripts/scratch/astra_echo.py, plus two general rules from Claude's read of v2: weigh a person's goal apart from their
   method; name each option's costs and who bears them). Ordinary requests get a direct Reply from astra instead.
2. Echo (echo.fulcrum.inc, persona Musonius, A. A. Long's Epictetus as samples) writes the reply from request + reasoning.
3. lint as in 26_frontier_batches.py; rows to data/frontier/sft_ae/items.jsonl with provenance.
usage: uv run scripts/data/30_astra_echo.py <openai-codex|openai-codex-2> <max batches>   -- Claude (Opus 5.5)"""
import hashlib
import importlib.util
import json
import random
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from openai import OpenAI

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/scratch"))
from astra_echo import AUTH, CHARACTER, WRITE  # noqa: E402
from astra_reasoning_v3 import LABELS, REASON_BRIEF_V5, pool  # noqa: E402  pane agent's v5i3 (slop/reviews/20261009_astra_reasoning_prompt.md)
from echo_prompt_restyle_opus import sample_set  # noqa: E402

spec = importlib.util.spec_from_file_location("fb", ROOT / "scripts/data/26_frontier_batches.py")
fb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fb)
OUT = ROOT / "data/frontier/sft_ae/items.jsonl"
TEST = ROOT / "data/frontier/sft_ae/test"  # test mode: briefs, astra output and rows here; the shared queue is not touched
ECHO_MODEL, ECHO_EFFORT, PERSONA, SAMPLE_SET = "echo", "high", "Musonius", "modern"
sha = lambda t: hashlib.sha256(t.encode()).hexdigest()[:12]
ASTRA_EFFORT = __import__("os").environ.get("ASTRA_EFFORT", "max")  # wassname 2026-10-09: "use max"
REASON_VARIANT = "v7-batch"  # labels (FACTS..THEREFORE+DRAFT) + 4 rotating example pairs; constitution injected on stdin, no tools (pane agent v6/v7, wassname: "it needs to be injected it will be lazy")
WRITE_VARIANT = "modern-samples+character-s1+goal-tone+draft-included+no-gender"
PY = ["uv", "run", "-q", str(ROOT / "scripts/data/26_frontier_batches.py")]

V5_LABELS = REASON_BRIEF_V5.split("{style}")[1].split("At most about 200 words")[0].strip()  # FACTS .. THEREFORE/DRAFT, pane agent's v5i3
REASON_FORMAT = f"""For each seed write a section:

### <id>
#### Request
(the request Musonius receives, written from the seed as its shape says: a system prompt, if any, on a line starting `System:`; then the user message. For repair: the request, `Assistant (first reply):`, and `User:` pushback lines.)
#### Reasoning
(private notes for a separate writer, who writes Musonius's reply from them. {LABELS}

{V5_LABELS}

At most about 200 words before the draft. No rule numbers, no citations of the constitution.)

For a seed whose shape is `ordinary`, write `#### Reply` (the full, excellent answer to the request) instead of `#### Reasoning`.

Do not write Musonius's reply for any other seed: the writer does that.
"""


def examples_block(salt: str) -> str:
    """4 request+notes pairs drawn from the example pool (compact logic + Fermi format), different per batch."""
    p = pool()
    picks = random.Random(salt).sample(sorted(p), 4)
    ex = "\n\n".join(f'<example move="{k}">\n{p[k]}\n</example>' for k in picks)
    return ("\n\nFour worked examples from unrelated cases follow, each a request and the notes on it. They show the format and how a reasoning "
            "move is made on a particular case; the conclusions belong to those cases. Do not reuse their names, wording, facts or verdicts, "
            "and do not mention them.\n\n" + ex + "\n")


def astra_brief(b: dict, acct: str) -> str:
    """The standard batch brief (constitution, purpose, shapes, seeds) with the output format swapped for request + reasoning."""
    rec = fb.write_brief("sft", b["batch"], b["writer"], b["seeds"])
    text = Path(rec["file"]).read_text()
    assert fb.FORMAT["sft"] in text, "brief format changed; update astra_brief"
    return text.replace(fb.FORMAT["sft"], REASON_FORMAT + examples_block(f"batch{b['batch']}"))


def inline(brief: str, default_out: str) -> str:
    """Constitution text in the prompt (not a path to read) and answer on stdout (not a file write), so we know astra saw all of it."""
    path_line = f"the constitution at `{fb.CONSTITUTION}`. Read the whole constitution first."
    write_line = f"Write all sections, in order, to `{default_out}` with the write tool. Do not edit other files."
    assert path_line in brief and write_line in brief, "brief wording changed; update inline()"
    brief = brief.replace(path_line, "the constitution given in full below. Read all of it first.").replace(write_line, "Reply with all sections, in order, and nothing else.")
    return brief.replace("\n## Output\n", f"\n<constitution>\n{fb.CONSTITUTION.read_text().strip()}\n</constitution>\n\n## Output\n", 1)


def run_batch(b: dict, acct: str, client: OpenAI, desc: str, samples: str, out_rows: Path = OUT, work: Path | None = None):
    work = work or Path(b["file"]).parent
    bfile = work / f"ae_batch_{b['batch']:03d}.md"
    default_out = str(fb.FRONTIER / "sft" / f"out_{b['batch']:03d}.md")  # the path write_brief puts in the brief
    brief = inline(astra_brief(b, acct), default_out)
    bfile.write_text(brief)
    out = work / f"ae_out_{b['batch']:03d}.md"
    done = {json.loads(l)["id"] for l in out_rows.open()} if out_rows.exists() else set()
    if all(s["id"] in done for s in b["seeds"]):
        print(f"batch {b['batch']}: all seeds already written")
        return True
    cached = out.exists() and all(s["id"] in fb.split_sections(out.read_text())[0] for s in b["seeds"])
    if cached:
        print(f"batch {b['batch']}: astra output cached ({out.name})")
    else:
        cmd = ["pi", "-ne", "-nc", "-ns", "-np", "--no-tools", "--session-dir", str(work / "ae_sessions"), *AUTH,
               "--system-prompt", "You are a careful analyst and writer. Do the task you are given.", "--model", f"{acct}/gpt-6-astra:{ASTRA_EFFORT}", "-p"]
        r = subprocess.run(cmd, input=brief, capture_output=True, text=True, timeout=3600)
        (work / f"ae_pi_{b['batch']:03d}.log").write_text(r.stdout + r.stderr)
        if r.returncode != 0 or not r.stdout.strip().startswith("### "):
            print(f"batch {b['batch']}: astra failed (exit {r.returncode}); see ae_pi_{b['batch']:03d}.log")
            return False
        out.write_text(r.stdout.strip() + "\n")
    parts, _ = fb.split_sections(out.read_text())
    seeds = {s["id"]: s for s in b["seeds"]}
    brief_sha = sha(brief)
    for sid, seed in seeds.items():
        if sid in done:
            continue
        sec = {k.lower(): v for k, v in parts.get(sid, {}).items()}
        if not sec.get("request"):
            print(f"  {sid}: no request from astra")
            continue
        t0 = time.monotonic()
        if seed["shape"] == "ordinary":
            reply, notes, how = sec.get("reply", ""), "", "astra (ordinary, direct)"
        else:
            notes = sec.get("reasoning", "")
            if not notes:
                print(f"  {sid}: no reasoning from astra")
                continue
            resp = client.chat.completions.create(model=ECHO_MODEL, reasoning_effort=ECHO_EFFORT, extra_body={"persona": PERSONA},
                                                  messages=[{"role": "user", "content": WRITE.format(sample_desc=desc, samples=samples, request=sec["request"], notes=notes, character=CHARACTER)}])
            reply, how = (resp.choices[0].message.content or "").strip(), "echo (modern samples) from astra reasoning"
            time.sleep(random.uniform(3, 8))
        lint = fb.lint(reply)
        row = {**seed, "request": sec["request"], "musonius": reply, "reasoning": notes,
               "meta": {"writer": f"{acct}/gpt-6-astra:{ASTRA_EFFORT}+echo", "how": how, "batch": b["batch"], "brief_sha": brief_sha,
                        "reasoner": f"{acct}/gpt-6-astra:{ASTRA_EFFORT}", "reason_variant": REASON_VARIANT, "write_variant": WRITE_VARIANT,
                        "seat": "original", "reason_format_sha": sha(REASON_FORMAT), "astra_output_cached": cached,
                        "echo": {"model": ECHO_MODEL, "effort": ECHO_EFFORT, "persona": PERSONA, "samples": SAMPLE_SET, "samples_sha": sha(samples),
                                 "write_prompt_sha": sha(WRITE), "character_sha": sha(CHARACTER)} if seed["shape"] != "ordinary" else None,
                        "git": fb.GIT,
                        "constitution_sha": fb.CONST_SHA, "seed_source": seed["source"], "seed_id": seed.get("source_id"),
                        "written_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "seconds": round(time.monotonic() - t0),
                        "lint": lint, "valid": bool(reply) and not any(fb.lint_kind(l) in fb.HARD for l in lint)}}
        out_rows.parent.mkdir(parents=True, exist_ok=True)
        with out_rows.open("a") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"  {sid} ({seed['shape']}): {len(reply.split())} words, lint {lint}", flush=True)
    return True


def test(acct: str, n: int):
    """n non-ordinary seeds from the first unrun queue batch, written under data/frontier/sft_ae/test/; queue untouched."""
    desc, samples = sample_set(SAMPLE_SET)
    formatted = "\n\n".join(f'<writing_sample source="{s["label"]}">\n{s["text"]}\n</writing_sample>' for s in samples)
    key = next(l.split("=", 1)[1].strip().strip("\"'") for l in (ROOT / ".env").read_text().splitlines() if l.startswith("ECHO_API="))
    client = OpenAI(base_url="https://echo.fulcrum.inc/api/v1", api_key=key, timeout=900, max_retries=2)
    src = next(x for x in map(json.loads, (fb.FRONTIER / "sft/batches.jsonl").open()) if not x.get("status"))
    seeds = [s for s in src["seeds"] if s["shape"] != "ordinary"][:n]
    TEST.mkdir(parents=True, exist_ok=True)
    b = {"batch": 9000 + src["batch"], "writer": f"{acct}/gpt-6-astra:medium+echo", "seeds": seeds,
         "file": str(TEST / f"batch_{9000 + src['batch']:03d}.md"), "out": str(TEST / f"out_{9000 + src['batch']:03d}.md")}
    rec = fb.write_brief("sft", b["batch"], b["writer"], seeds)  # writes into data/frontier/sft; moved to the test dir
    Path(rec["file"]).rename(b["file"])
    global astra_brief
    _orig = astra_brief
    astra_brief = lambda bb, a: Path(bb["file"]).read_text().replace(fb.FORMAT["sft"], REASON_FORMAT + examples_block(f"batch{bb['batch']}"))
    run_batch(b, acct, client, desc, formatted, out_rows=TEST / "items.jsonl", work=TEST)
    astra_brief = _orig
    print(TEST / "items.jsonl")


def main(acct: str, n: int):
    desc, samples = sample_set(SAMPLE_SET)
    formatted = "\n\n".join(f'<writing_sample source="{s["label"]}">\n{s["text"]}\n</writing_sample>' for s in samples)
    key = next(l.split("=", 1)[1].strip().strip("\"'") for l in (ROOT / ".env").read_text().splitlines() if l.startswith("ECHO_API="))
    client = OpenAI(base_url="https://echo.fulcrum.inc/api/v1", api_key=key, timeout=900, max_retries=2)
    for _ in range(n):
        nxt = subprocess.run(PY + ["next", "sft", acct], capture_output=True, text=True, check=True).stdout.strip()
        if nxt.startswith(("DONE", "WAIT")):
            print(nxt)
            return
        b0 = json.loads(nxt)
        time.sleep(b0["wait_s"])
        b = next(x for x in map(json.loads, (fb.FRONTIER / "sft/batches.jsonl").open()) if x["batch"] == b0["batch"])
        subprocess.run(PY + ["mark", "sft", str(b["batch"]), "running"], check=True)
        ok = run_batch(b, acct, client, desc, formatted)
        subprocess.run(PY + ["mark", "sft", str(b["batch"]), "done" if ok else "failed"], check=True)


if __name__ == "__main__":
    if sys.argv[1] == "test":
        test(sys.argv[2], int(sys.argv[3]))
    else:
        main(sys.argv[1], int(sys.argv[2]))
