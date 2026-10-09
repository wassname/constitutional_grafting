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
  uv run scripts/data/30_astra_echo.py seats <acct> <n batches> [first]   (2 more seats per case, shared verdict; rows in sft_ae/seats/)
  uv run scripts/data/30_astra_echo.py catch_up [batch ...]   (missing rows of batches no lane is writing, e.g. after a lane was stopped)
-- PI / OpenAI Sol, from Claude (Opus 5.5)'s first version"""
import fcntl
import hashlib
import importlib.util
import json
import random
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from openai import APIError, OpenAI

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/data"))
from astra_echo import prompts as P  # noqa: E402
import constitution as C  # noqa: E402  (scripts/data/constitution.py: single source of the constitution text)

spec = importlib.util.spec_from_file_location("fb", ROOT / "scripts/data/26_frontier_batches.py")
fb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fb)

OUT = ROOT / "data/frontier/sft_ae"
STOP = OUT / "STOP"  # touch to make the lanes finish their current batch and take no more (e.g. before a data freeze)
ASTRA_EFFORT = "max"  # wassname 2026-10-09: "use max", "medium is nerfed"
ASTRA_SYSTEM = "You are a careful analyst and writer. Do the task you are given."
ECHO_MODEL, ECHO_EFFORT, PERSONA = "echo", "high", "Musonius"
REASON_VARIANT = "v7-batch-all-examples"
WRITE_VARIANT = "modern-samples+character-s1+goal-tone+draft-included+no-gender"
AUTH = ["-e", str(Path.home() / ".pi/agent/git/github.com/gotgenes/pi-anthropic-auth/src/index.ts"),
        "-e", str(Path.home() / ".pi/agent/npm/node_modules/pi-codex-multi/extensions/multi-sub.ts")]
QUEUE = ["uv", "run", "-q", str(ROOT / "scripts/data/26_frontier_batches.py")]
now = lambda: datetime.now(timezone.utc).isoformat(timespec="seconds")


def inline_constitution(text: str, before: str | None = None) -> str:
    """26's prompts tell the writer to read the constitution from a path; put the text itself in (inserted before `before`,
    else appended), so we know the model saw all of it (wassname: "it needs to be injected it will be lazy")."""
    path_line = f"the constitution at `{fb.CONSTITUTION}`. Read the whole constitution first."
    assert path_line in text, "26_frontier_batches wording changed; update inline_constitution"
    block = f"\n<constitution>\n{C.text().strip()}\n</constitution>\n"  # renders v4.md.j2, the source
    text = text.replace(path_line, "the constitution given in full below. Read all of it first.")
    return text.replace(before, block + before, 1) if before else text + block


def pi_astra(acct: str, prompt: str, d: Path, system: str) -> str:
    """One astra call: prompt on stdin, no tools, session kept in d/sessions. Returns stdout."""
    cmd = ["pi", "-ne", "-nc", "-ns", "-np", "--no-tools", "--session-dir", str(d / "sessions"), *AUTH,
           "--system-prompt", system, "--model", f"{acct}/gpt-6-astra:{ASTRA_EFFORT}", "-p"]
    r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=7200)
    with (d / "astra_stderr.log").open("a") as f:
        f.write(f"--- {now()} exit {r.returncode}\n{r.stderr}")
    if r.returncode != 0 or not r.stdout.strip():
        raise RuntimeError(f"astra failed (exit {r.returncode}): {r.stderr[-500:]}")
    return r.stdout.strip()


def astra_prompt(b: dict) -> tuple[str, list[str]]:
    """The queue's batch brief, with the constitution inline, the notes format in place of the reply format, and all examples."""
    rec = fb.write_brief("sft", b["batch"], b["writer"], b["seeds"])
    brief = re.sub(r"\A---\n.*?\n---\n\n", "", Path(rec["file"]).read_text(), count=1, flags=re.S)  # front matter has a timestamp; it would defeat the cache
    write_line = f"Write all sections, in order, to `{rec['out']}` with the write tool. Do not edit other files."
    assert write_line in brief and fb.FORMAT["sft"] in brief, "26_frontier_batches brief wording changed; update astra_prompt"
    examples, order = P.examples_block(f"batch{b['batch']}")
    brief = brief.replace(write_line, "Reply with all sections, in order, and nothing else.").replace(fb.FORMAT["sft"], P.REASON_FORMAT + examples)
    return inline_constitution(brief, before="\n## Output\n"), order


def run_astra(acct: str, brief: str, d: Path, seed_ids: list[str]) -> tuple[dict, bool]:
    """astra's sections per seed; cached in d/astra.md while the brief is unchanged."""
    meta = json.loads((d / "meta.json").read_text()) if (d / "meta.json").exists() else {}
    out = d / "astra.md"
    if out.exists() and meta.get("brief_sha") == P.sha(brief) and all(s in fb.split_sections(out.read_text())[0] for s in seed_ids):
        return fb.split_sections(out.read_text())[0], True
    (d / "brief.md").write_text(brief)
    t0 = time.monotonic()
    text = pi_astra(acct, brief, d, ASTRA_SYSTEM)
    if not text.startswith("### "):
        raise RuntimeError(f"astra output is not in the sections format: {text[:300]}")
    out.write_text(text + "\n")
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


def astra_phase(b: dict, acct: str, root: Path) -> Path:
    """astra's request + notes for every seed of the batch (cached), and batch.json so the rows phase can run later or elsewhere."""
    d = root / "batches" / f"{b['batch']:03d}"
    d.mkdir(parents=True, exist_ok=True)
    brief, order = astra_prompt(b)
    parts, astra_cached = run_astra(acct, brief, d, [s["id"] for s in b["seeds"]])
    (d / "batch.json").write_text(json.dumps({"batch": b["batch"], "acct": acct, "seeds": b["seeds"], "brief_sha": P.sha(brief),
                                               "constitution_sha": P.sha(C.text()),
                                               "examples_order": order, "astra_cached": astra_cached}, ensure_ascii=False, indent=1))
    print(f"batch {b['batch']}: astra {'cached' if astra_cached else 'done'}, {len(parts)} sections", flush=True)
    return d


def rows_phase(d: Path, client: OpenAI, rows_path: Path):
    """Echo writes each reply from astra's notes (astra writes it directly if Echo fails); one row per seed, skipping seeds already written."""
    b = json.loads((d / "batch.json").read_text())
    acct, parts = b["acct"], fb.split_sections((d / "astra.md").read_text())[0]
    done = {json.loads(l)["id"] for l in rows_path.open()} if rows_path.exists() else set()
    desc, samples = P.echo_samples()
    character = P.character()
    for seed in b["seeds"]:
        sid = seed["id"]
        sec = {k.lower(): v for k, v in parts.get(sid, {}).items()}
        if sid in done:
            continue
        missing = "request" if not sec.get("request") else "reply" if seed["shape"] == "ordinary" and not sec.get("reply") else \
                  "reasoning" if seed["shape"] != "ordinary" and not sec.get("reasoning") else None
        if missing:  # still a row, so the seed is visibly lost rather than silently skipped (repo review finding 1)
            reply, notes, served, finish, echo_cached, how, echo_prompt = "", sec.get("reasoning", ""), None, None, None, f"astra gave no {missing}", None
        elif seed["shape"] == "ordinary":
            reply, notes, served, finish, echo_cached, how, echo_prompt = sec.get("reply", ""), "", None, None, None, "astra (ordinary, direct)", None
        else:
            notes = sec["reasoning"]
            echo_prompt = P.ECHO_WRITE.format(sample_desc=desc, samples=samples, request=sec["request"], notes=notes, character=character)
            try:
                reply, served, finish, echo_cached = run_echo(client, echo_prompt, d, sid)
                how = "echo (modern samples) from astra reasoning"
            except APIError as e:  # Echo down or refusing: astra writes the reply itself, recorded as such (not mixed silently)
                print(f"  {sid}: Echo failed ({str(e)[:120]}); astra writes the reply directly", flush=True)
                reply, _, echo_cached = run_direct(acct, sec["request"], d, sid, f"direct{sid}")
                served, finish, how, echo_prompt = None, None, f"astra direct (Echo failed: {str(e)[:120]})", None
        lint = fb.lint(reply) + ([f"echo finish_reason {finish}"] if finish not in (None, "stop") else [])
        truncated = finish == "length" or reply.rstrip()[-1:] not in ".?!\"'”’)]*`。！？」』）"  # a code block ends in a fence; CJK replies end in 。
        row = {**seed, "request": sec.get("request", ""), "musonius": reply, "reasoning": notes,
               "meta": {"writer": f"{acct}/gpt-6-astra:{ASTRA_EFFORT}" + ("+echo" if echo_prompt else ""), "how": how, "batch": b["batch"], "batch_dir": str(d.relative_to(ROOT)),
                        "reasoner": f"{acct}/gpt-6-astra:{ASTRA_EFFORT}", "reason_variant": REASON_VARIANT, "write_variant": WRITE_VARIANT,
                        "brief_sha": b["brief_sha"], "reason_format_sha": P.sha(P.REASON_FORMAT), "pool_sha": P.sha(P.POOL.read_text()),
                        "examples_order": b["examples_order"], "astra_cached": b["astra_cached"], "seat": "original",
                        "echo": None if echo_prompt is None else {"model": ECHO_MODEL, "served_model": served, "effort": ECHO_EFFORT, "persona": PERSONA,
                                                                  "prompt_sha": P.sha(echo_prompt), "finish_reason": finish, "write_prompt_sha": P.sha(P.ECHO_WRITE),
                                                                  "samples_sha": P.sha(samples), "character_sha": P.sha(character), "cached": echo_cached},
                        "git": fb.GIT, "constitution_sha": b["constitution_sha"], "seed_source": seed["source"], "seed_id": seed.get("source_id"),
                        "written_at": now(), "lint": lint + ([f"astra gave no {missing}"] if missing else []), "truncated": truncated, "valid": bool(reply) and not missing and not truncated and not any(fb.lint_kind(l) in fb.HARD for l in lint)}}
        with rows_path.open("a") as f:
            fcntl.flock(f, fcntl.LOCK_EX)  # two astra lanes append to the same file
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"  {sid} ({seed['shape']}): {len(reply.split())} words, lint {lint}", flush=True)


def run_direct(acct: str, request: str, d: Path, sid: str, order_seed: str) -> tuple[str, list[str], bool]:
    """astra writes the reply itself (main pipeline instructions, constitution inline, all examples); cached in d/direct/<sid>.json."""
    examples, order = P.examples_block(order_seed)
    prompt = inline_constitution(fb.COMMON.format(constitution=fb.CONSTITUTION)) + P.DIRECT_TASK.format(examples=examples, request=request)
    f = d / "direct" / f"{sid}.json"
    if f.exists() and (c := json.loads(f.read_text()))["prompt_sha"] == P.sha(prompt):
        return c["reply"], order, True
    reply = pi_astra(acct, prompt, d, "You are a careful, skilled writer. Do the writing task you are given.")
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps({"prompt_sha": P.sha(prompt), "at": now(), "prompt": prompt, "reply": reply}, ensure_ascii=False, indent=1))
    return reply, order, False


def echo_client() -> OpenAI:
    key = next(l.split("=", 1)[1].strip().strip("\"'") for l in (ROOT / ".env").read_text().splitlines() if l.startswith("ECHO_API="))
    return OpenAI(base_url="https://echo.fulcrum.inc/api/v1", api_key=key, timeout=900, max_retries=2)


def run(acct: str, n: int):
    """One astra lane: astra's call for the next batch starts while Echo is still writing the previous batch's replies.
    A batch is marked done in the queue when astra has finished; `catch_up` writes any rows a crashed lane left unwritten."""
    client, rows_path = echo_client(), OUT / "items.jsonl"
    queue = lambda: [x for x in map(json.loads, (fb.FRONTIER / "sft/batches.jsonl").open()) if fb.account(x["writer"]) == acct and "astra" in x["writer"]]
    # A batch this account claimed but never finished (its lane was stopped) blocks `26 next`; this lane is the only one on the account, so run it first.
    orphans = [x["batch"] for x in queue() if x.get("status") == "running"]
    with ThreadPoolExecutor(max_workers=1) as echo_lane:
        pending, failures = None, 0
        for _ in range(n):
            if STOP.exists():  # take no new batch; Echo still finishes the last one
                print(f"{STOP} exists: no new batches")
                break
            if orphans:
                bid = orphans.pop(0)
                b = next(x for x in queue() if x["batch"] == bid)
                print(f"batch {b['batch']}: claimed earlier but unfinished; running it now", flush=True)
            else:
                nxt = subprocess.run(QUEUE + ["next", "sft", acct], capture_output=True, text=True, check=True).stdout.strip()
                if nxt.startswith(("DONE", "WAIT")):
                    print(nxt)
                    break
                b0 = json.loads(nxt)
                time.sleep(b0["wait_s"])
                b = next(x for x in queue() if x["batch"] == b0["batch"])
                subprocess.run(QUEUE + ["mark", "sft", str(b["batch"]), "running"], check=True)
            try:
                d = astra_phase(b, acct, OUT)
                failures = 0
            except RuntimeError as e:  # astra's stream was cut (seen: "terminated" after ~15 min); the batch is marked failed, the lane goes on
                subprocess.run(QUEUE + ["mark", "sft", str(b["batch"]), "failed"], check=True)
                failures += 1
                print(f"batch {b['batch']}: astra failed ({str(e)[:200]}); {failures} in a row", flush=True)
                if failures >= 3:
                    raise
                continue
            subprocess.run(QUEUE + ["mark", "sft", str(b["batch"]), "done"], check=True)
            if pending:
                pending.result()  # raises if the previous batch's rows failed
            pending = echo_lane.submit(rows_phase, d, client, rows_path)
        if pending:
            pending.result()


def catch_up(*batches: str):
    """Write the missing rows of these batches (default: every batch dir with astra output). Run it only for batches no lane is
    writing, or two writers would duplicate rows."""
    client, rows_path = echo_client(), OUT / "items.jsonl"
    dirs = [OUT / "batches" / f"{int(n):03d}" for n in batches] or [d.parent for d in sorted((OUT / "batches").glob("*/batch.json"))]
    for d in dirs:
        rows_phase(d, client, rows_path)


# --- Seats: the same facts asked from two other seats, one shared verdict (wassname 2026-10-09: "yes this works!") ---
SEATS = OUT / "seats"  # seats/items.jsonl (rows) and seats/batches/<NNN>/ (prompt, astra output, sessions, Echo)


def seat_groups() -> list[list[dict]]:
    """Valid original rows (not ordinary or repair), 5 cases per astra call. The grouping is saved in seats/groups.json and only
    extended with rows written since (in hash order), so a batch number always means the same cases."""
    rows = {r["id"]: r for r in map(json.loads, (OUT / "items.jsonl").open())
            if r["meta"]["valid"] and r["shape"] not in ("ordinary", "repair") and r["meta"]["seat"] == "original" and r["reasoning"]}
    f = SEATS / "groups.json"
    groups = json.loads(f.read_text()) if f.exists() else []
    new = sorted(set(rows) - {i for g in groups for i in g}, key=lambda i: hashlib.md5(f"seats|{i}".encode()).hexdigest())
    groups += [new[i:i + 5] for i in range(0, len(new) - len(new) % 5, 5)]  # a partial group waits for more rows
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(groups, indent=0))
    return [[rows[i] for i in g] for g in groups]


def seats(acct: str, n_batches: int, first: int = 0):
    """For each case, astra writes requests from seats A and B and one shared set of notes; Echo writes a reply per seat."""
    client, rows_path = echo_client(), SEATS / "items.jsonl"
    groups = seat_groups()
    desc, samples = P.echo_samples()
    character = P.character()
    for n in range(first, min(first + n_batches, len(groups))):
        if STOP.exists():
            print(f"{STOP} exists: no new batches")
            return
        group, d = groups[n], SEATS / "batches" / f"{n:03d}"
        d.mkdir(parents=True, exist_ok=True)
        done = {json.loads(l)["id"] for l in rows_path.open()} if rows_path.exists() else set()
        if all(f"{r['id']}_seat{x}" in done for r in group for x in "AB"):
            continue
        examples, order = P.examples_block(f"seats{n}")
        prompt = (inline_constitution(fb.COMMON.format(constitution=fb.CONSTITUTION)) + "\n" + P.SEATS_TASK + examples + "\n## Cases\n"
                  + "".join(P.SEATS_CASE.format(id=r["id"], request=r["request"], notes=r["reasoning"]) for r in group))
        parts, astra_cached = run_astra(acct, prompt, d, [r["id"] for r in group])
        print(f"seats batch {n}: astra {'cached' if astra_cached else 'done'}, {len(parts)} cases", flush=True)
        for r in group:
            sec = {k.lower(): v for k, v in parts.get(r["id"], {}).items()}
            labels = dict(re.findall(r"^([AB]):\s*(.+)$", sec.get("seats", ""), re.M))
            for x in "AB":
                sid = f"{r['id']}_seat{x}"
                if sid in done:
                    continue
                missing = next((k for k in ("seats", f"request{x.lower()}", "reasoning", f"advice{x.lower()}") if not sec.get(k)), None)
                echo_prompt = served = finish = echo_cached = None
                if missing:
                    reply, notes, how = "", sec.get("reasoning", ""), f"astra gave no {missing}"
                else:
                    notes = f"{sec['reasoning']}\n\nADVICE for this person:\n{sec[f'advice{x.lower()}']}"
                    echo_prompt = P.ECHO_WRITE.format(sample_desc=desc, samples=samples, request=sec[f"request{x.lower()}"], notes=notes, character=character)
                    reply, served, finish, echo_cached = run_echo(client, echo_prompt, d, sid)
                    how = "echo (modern samples) from shared seat notes"
                lint = fb.lint(reply) + ([f"echo finish_reason {finish}"] if finish not in (None, "stop") else []) + ([how] if missing else [])
                truncated = finish == "length" or reply.rstrip()[-1:] not in ".?!\"'”’)]*`。！？」』）"
                row = {**{k: v for k, v in r.items() if k not in ("request", "musonius", "reasoning", "meta")}, "id": sid,
                       "request": sec.get(f"request{x.lower()}", ""), "musonius": reply, "reasoning": notes,
                       "meta": {"writer": f"{acct}/gpt-6-astra:{ASTRA_EFFORT}+echo", "how": how, "seat": labels.get(x, ""), "seat_key": x, "group": r["id"],
                                "batch": f"seats{n}", "batch_dir": str(d.relative_to(ROOT)), "brief_sha": P.sha(prompt), "seats_task_sha": P.sha(P.SEATS_TASK),
                                "pool_sha": P.sha(P.POOL.read_text()), "examples_order": order, "astra_cached": astra_cached,
                                "echo": None if echo_prompt is None else {"model": ECHO_MODEL, "served_model": served, "effort": ECHO_EFFORT, "persona": PERSONA,
                                                                          "prompt_sha": P.sha(echo_prompt), "finish_reason": finish, "write_prompt_sha": P.sha(P.ECHO_WRITE),
                                                                          "samples_sha": P.sha(samples), "character_sha": P.sha(character), "cached": echo_cached},
                                "git": fb.GIT, "constitution_sha": P.sha(C.text()), "written_at": now(), "lint": lint, "truncated": truncated,
                                "valid": bool(reply) and not missing and not truncated and not any(fb.lint_kind(l) in fb.HARD for l in lint)}}
                with rows_path.open("a") as f:
                    fcntl.flock(f, fcntl.LOCK_EX)
                    f.write(json.dumps(row, ensure_ascii=False) + "\n")
                print(f"  {sid} ({labels.get(x, '?')}): {len(reply.split())} words, lint {lint}", flush=True)


def test(acct: str, n: int):
    """n non-ordinary seeds of this account's first pending batch, as batch 9000+N under sft_ae/test/; the queue is not marked."""
    src = next(x for x in map(json.loads, (fb.FRONTIER / "sft/batches.jsonl").open()) if not x.get("status") and fb.account(x["writer"]) == acct)
    b = {**src, "batch": 9000 + src["batch"], "seeds": [s for s in src["seeds"] if s["shape"] != "ordinary"][:n]}
    d = astra_phase(b, acct, OUT / "test")
    (fb.FRONTIER / "sft" / f"batch_{b['batch']:03d}.md").unlink()  # write_brief's copy; the exact prompt is in the batch dir
    rows_phase(d, echo_client(), OUT / "test/items.jsonl")
    print(OUT / "test/items.jsonl")


if __name__ == "__main__":
    {"run": lambda: run(sys.argv[2], int(sys.argv[3])), "test": lambda: test(sys.argv[2], int(sys.argv[3])), "catch_up": lambda: catch_up(*sys.argv[2:]),
     "seats": lambda: seats(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]) if len(sys.argv) > 4 else 0)}[sys.argv[1]]()
