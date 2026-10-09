# /// script
# requires-python = ">=3.11"
# dependencies = ["openai", "markdown-it-py"]
# ///
"""Pipeline 2, SFT rows: astra reasons, Echo writes.

Per batch from the shared queue (data/frontier/sft/batches.jsonl, writer "<account>/gpt-6-astra:max+echo"):
1. astra gets one prompt on stdin: the batch brief from 26_frontier_batches.py with the constitution inline, the notes format
   and all example pairs from astra_echo/example_pool.md. No tools. It writes, per seed, the Request and compact-logic
   Reasoning (or a direct Reply for `ordinary` seeds).
2. Echo (persona Musonius, Long's Epictetus as writing samples) writes each reply from request + notes.
3. Lint as in 26_frontier_batches.py; one row per seed to data/frontier/sft_ae/items.jsonl.

Files, under data/frontier/sft_ae/ (or sft_ae/test/ for `test`):
  items.jsonl                       rows; append-only, a seed already there is skipped
  batches/<NNN>/brief.md            the exact prompt astra got
  batches/<NNN>/astra.md            astra's output; reused while meta.json brief_sha matches the brief
  batches/<NNN>/astra_stderr.log
  batches/<NNN>/sessions/           pi session, the full transcript
  batches/<NNN>/echo/<seed>.json    Echo's prompt and reply; reused while the prompt sha matches
  batches/<NNN>/meta.json           shas, models, example order, timings
  inputs/echo_samples_modern.json   frozen writing samples

usage:
  uv run scripts/data/30_astra_echo.py run <openai-codex|openai-codex-2> <max batches>
  uv run scripts/data/30_astra_echo.py test <openai-codex|openai-codex-2> <n seeds>   (first pending batch, non-ordinary seeds; queue untouched)
-- PI / OpenAI Sol, from Claude (Opus 5.5)'s first version"""
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
sys.path.insert(0, str(ROOT / "scripts/data"))
from astra_echo import prompts as P  # noqa: E402

spec = importlib.util.spec_from_file_location("fb", ROOT / "scripts/data/26_frontier_batches.py")
fb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fb)

OUT = ROOT / "data/frontier/sft_ae"
ASTRA_EFFORT = "max"  # wassname 2026-10-09: "use max", "medium is nerfed"
ASTRA_SYSTEM = "You are a careful analyst and writer. Do the task you are given."
ECHO_MODEL, ECHO_EFFORT, PERSONA = "echo", "high", "Musonius"
REASON_VARIANT = "v7-batch-all-examples"
WRITE_VARIANT = "modern-samples+character-s1+goal-tone+draft-included+no-gender"
AUTH = ["-e", str(Path.home() / ".pi/agent/git/github.com/gotgenes/pi-anthropic-auth/src/index.ts"),
        "-e", str(Path.home() / ".pi/agent/npm/node_modules/pi-codex-multi/extensions/multi-sub.ts")]
QUEUE = ["uv", "run", "-q", str(ROOT / "scripts/data/26_frontier_batches.py")]
now = lambda: datetime.now(timezone.utc).isoformat(timespec="seconds")


def astra_prompt(b: dict) -> tuple[str, list[str]]:
    """The queue's batch brief, with the constitution inline, the notes format in place of the reply format, and all examples."""
    rec = fb.write_brief("sft", b["batch"], b["writer"], b["seeds"])
    brief = Path(rec["file"]).read_text()
    path_line = f"the constitution at `{fb.CONSTITUTION}`. Read the whole constitution first."
    write_line = f"Write all sections, in order, to `{rec['out']}` with the write tool. Do not edit other files."
    assert path_line in brief and write_line in brief and fb.FORMAT["sft"] in brief, "26_frontier_batches brief wording changed; update astra_prompt"
    examples, order = P.examples_block(f"batch{b['batch']}")
    brief = (brief.replace(path_line, "the constitution given in full below. Read all of it first.")
             .replace(write_line, "Reply with all sections, in order, and nothing else.")
             .replace(fb.FORMAT["sft"], P.REASON_FORMAT + examples)
             .replace("\n## Output\n", f"\n<constitution>\n{fb.CONSTITUTION.read_text().strip()}\n</constitution>\n\n## Output\n", 1))
    return brief, order


def run_astra(acct: str, brief: str, d: Path, seed_ids: list[str]) -> tuple[dict, bool]:
    """astra's sections per seed; cached in d/astra.md while the brief is unchanged."""
    meta = json.loads((d / "meta.json").read_text()) if (d / "meta.json").exists() else {}
    out = d / "astra.md"
    if out.exists() and meta.get("brief_sha") == P.sha(brief) and all(s in fb.split_sections(out.read_text())[0] for s in seed_ids):
        return fb.split_sections(out.read_text())[0], True
    (d / "brief.md").write_text(brief)
    cmd = ["pi", "-ne", "-nc", "-ns", "-np", "--no-tools", "--session-dir", str(d / "sessions"), *AUTH,
           "--system-prompt", ASTRA_SYSTEM, "--model", f"{acct}/gpt-6-astra:{ASTRA_EFFORT}", "-p"]
    t0 = time.monotonic()
    r = subprocess.run(cmd, input=brief, capture_output=True, text=True, timeout=7200)
    (d / "astra_stderr.log").write_text(r.stderr)
    if r.returncode != 0 or not r.stdout.strip().startswith("### "):
        raise RuntimeError(f"astra failed (exit {r.returncode}): {r.stderr[-500:]} {r.stdout[:300]}")
    out.write_text(r.stdout.strip() + "\n")
    (d / "meta.json").write_text(json.dumps({**meta, "brief_sha": P.sha(brief), "astra_seconds": round(time.monotonic() - t0), "astra_at": now()}, indent=1))
    return fb.split_sections(out.read_text())[0], False


def run_echo(client: OpenAI, prompt: str, d: Path, sid: str) -> tuple[str, str, str, bool]:
    """Echo's reply; cached in d/echo/<sid>.json while the prompt is unchanged. Returns (reply, served model, finish reason, cached)."""
    f = d / "echo" / f"{sid}.json"
    if f.exists() and (c := json.loads(f.read_text()))["prompt_sha"] == P.sha(prompt):
        return c["reply"], c["served_model"], c.get("finish_reason"), True
    resp = client.chat.completions.create(model=ECHO_MODEL, reasoning_effort=ECHO_EFFORT, extra_body={"persona": PERSONA},
                                          messages=[{"role": "user", "content": prompt}])
    reply, finish = (resp.choices[0].message.content or "").strip(), resp.choices[0].finish_reason
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps({"prompt_sha": P.sha(prompt), "served_model": resp.model, "finish_reason": finish, "at": now(), "prompt": prompt, "reply": reply}, ensure_ascii=False, indent=1))
    time.sleep(random.uniform(3, 8))  # Echo is shared with the restyle lane
    return reply, resp.model, finish, False


def run_batch(b: dict, acct: str, client: OpenAI, root: Path):
    rows_path, d = root / "items.jsonl", root / "batches" / f"{b['batch']:03d}"
    d.mkdir(parents=True, exist_ok=True)
    done = {json.loads(l)["id"] for l in rows_path.open()} if rows_path.exists() else set()
    if all(s["id"] in done for s in b["seeds"]):
        print(f"batch {b['batch']}: all seeds already written")
        return
    brief, order = astra_prompt(b)
    parts, astra_cached = run_astra(acct, brief, d, [s["id"] for s in b["seeds"]])
    desc, samples = P.echo_samples()
    character = P.character()
    print(f"batch {b['batch']}: astra {'cached' if astra_cached else 'done'}, {len(parts)} sections", flush=True)
    for seed in b["seeds"]:
        sid = seed["id"]
        sec = {k.lower(): v for k, v in parts.get(sid, {}).items()}
        if sid in done or not sec.get("request"):
            print(f"  {sid}: {'already written' if sid in done else 'no request from astra'}")
            continue
        if seed["shape"] == "ordinary":
            reply, notes, served, finish, echo_cached, how, echo_prompt = sec.get("reply", ""), "", None, None, None, "astra (ordinary, direct)", None
        else:
            notes = sec.get("reasoning", "")
            if not notes:
                print(f"  {sid}: no reasoning from astra")
                continue
            echo_prompt = P.ECHO_WRITE.format(sample_desc=desc, samples=samples, request=sec["request"], notes=notes, character=character)
            reply, served, finish, echo_cached = run_echo(client, echo_prompt, d, sid)
            how = "echo (modern samples) from astra reasoning"
        lint = fb.lint(reply) + ([f"echo finish_reason {finish}"] if finish not in (None, "stop") else [])
        truncated = finish == "length" or reply.rstrip()[-1:] not in ".?!\"'”’)]*"
        row = {**seed, "request": sec["request"], "musonius": reply, "reasoning": notes,
               "meta": {"writer": f"{acct}/gpt-6-astra:{ASTRA_EFFORT}+echo", "how": how, "batch": b["batch"], "batch_dir": str(d.relative_to(ROOT)),
                        "reasoner": f"{acct}/gpt-6-astra:{ASTRA_EFFORT}", "reason_variant": REASON_VARIANT, "write_variant": WRITE_VARIANT,
                        "brief_sha": P.sha(brief), "reason_format_sha": P.sha(P.REASON_FORMAT), "pool_sha": P.sha(P.POOL.read_text()),
                        "examples_order": order, "astra_cached": astra_cached, "seat": "original",
                        "echo": None if echo_prompt is None else {"model": ECHO_MODEL, "served_model": served, "effort": ECHO_EFFORT, "persona": PERSONA,
                                                                  "prompt_sha": P.sha(echo_prompt), "finish_reason": finish, "write_prompt_sha": P.sha(P.ECHO_WRITE),
                                                                  "samples_sha": P.sha(samples), "character_sha": P.sha(character), "cached": echo_cached},
                        "git": fb.GIT, "constitution_sha": fb.CONST_SHA, "seed_source": seed["source"], "seed_id": seed.get("source_id"),
                        "written_at": now(), "lint": lint, "truncated": truncated, "valid": bool(reply) and not truncated and not any(fb.lint_kind(l) in fb.HARD for l in lint)}}
        with rows_path.open("a") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"  {sid} ({seed['shape']}): {len(reply.split())} words, lint {lint}", flush=True)


def echo_client() -> OpenAI:
    key = next(l.split("=", 1)[1].strip().strip("\"'") for l in (ROOT / ".env").read_text().splitlines() if l.startswith("ECHO_API="))
    return OpenAI(base_url="https://echo.fulcrum.inc/api/v1", api_key=key, timeout=900, max_retries=2)


def run(acct: str, n: int):
    client = echo_client()
    for _ in range(n):
        nxt = subprocess.run(QUEUE + ["next", "sft", acct], capture_output=True, text=True, check=True).stdout.strip()
        if nxt.startswith(("DONE", "WAIT")):
            print(nxt)
            return
        b0 = json.loads(nxt)
        time.sleep(b0["wait_s"])
        b = next(x for x in map(json.loads, (fb.FRONTIER / "sft/batches.jsonl").open()) if x["batch"] == b0["batch"])
        subprocess.run(QUEUE + ["mark", "sft", str(b["batch"]), "running"], check=True)
        try:
            run_batch(b, acct, client, OUT)
        except Exception:
            subprocess.run(QUEUE + ["mark", "sft", str(b["batch"]), "failed"], check=True)
            raise
        subprocess.run(QUEUE + ["mark", "sft", str(b["batch"]), "done"], check=True)


def test(acct: str, n: int):
    """n non-ordinary seeds of this account's first pending batch, as batch 9000+N under sft_ae/test/; the queue is not marked."""
    src = next(x for x in map(json.loads, (fb.FRONTIER / "sft/batches.jsonl").open()) if not x.get("status") and fb.account(x["writer"]) == acct)
    b = {**src, "batch": 9000 + src["batch"], "seeds": [s for s in src["seeds"] if s["shape"] != "ordinary"][:n]}
    run_batch(b, acct, echo_client(), OUT / "test")
    (fb.FRONTIER / "sft" / f"batch_{b['batch']:03d}.md").unlink()  # write_brief's copy; the exact prompt is in the batch dir
    print(OUT / "test/items.jsonl")


if __name__ == "__main__":
    {"run": run, "test": test}[sys.argv[1]](sys.argv[2], int(sys.argv[3]))
