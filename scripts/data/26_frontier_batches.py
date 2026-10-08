# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Frontier writing in batches by subscription subagents (Opus 5.5, Fable 5.1, astra), data v3.

make:  uv run scripts/data/26_frontier_batches.py make <sft|docs> <batch size> [first n seeds]
       -> data/frontier/<kind>/batch_NNN.md (brief + seeds) and a writer assignment in batches.jsonl
parse: uv run scripts/data/26_frontier_batches.py parse <sft|docs>
       -> data/frontier/<kind>/items.jsonl from the subagents' out_NNN.md files (missing items listed)

next:  ... next <kind> <account>  -> the next batch for that provider account and its earliest launch time (pacing below)
mark:  ... mark <kind> <batch> <running|done|failed>
Launch: scripts/data/27_run_frontier.sh (pi -ne -nc -ns -np, read/write tools only, one batch at a time).

A writer gets only its batch file and the constitution. Seeds are inputs; no other project's answers are reused.
-- Claude (Opus 5.5)"""
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEEDS = ROOT / "data/prompts/v3_seeds"
FRONTIER = ROOT / "data/frontier"
CONSTITUTION = ROOT / "constitution/v4.md"
# wassname 2026-10-09: two OpenAI subscriptions to use up; Opus cheaper than Fable; "maybe do 25% fable"
# 12-slot cycle: astra 8/12 across both OpenAI subscriptions (wassname: "maybe astra should be 66% if quality is good"), Opus 3/12, Fable 1/12
A1, A2, OP, FB = "openai-codex/gpt-6-astra:medium", "openai-codex-2/gpt-6-astra:medium", "anthropic/claude-opus-5-5", "anthropic/claude-fable-5-1"
WRITERS = [A1, OP, A2, A1, A2, OP, A1, A2, FB, A2, A1, OP]

COMMON = """You are writing training data. An open-weight model will be trained on your text to take on the character of Musonius, an AI whose values are set out in the constitution at `{constitution}`. Read the whole constitution first.

Musonius must act from these values, which differ from those of other assistants. Write what Musonius would do in each case at its best. The trained model learns from what Musonius does and why, so:
- The reasons must be the real ones for this case, in plain words. Never quote the constitution, name its sections, or use its in-house terms (for example "circles", "drives", "the test", "view from history", "guards"). The reader has never seen it.
- No meta commentary about Musonius's own character, values or training, and no disclaimers.
- Do not invent facts the seed did not give. If a missing fact matters, say what would change the answer, or (in fiction) keep it vague.
- Let the shape fit the case. Across a batch, answers and outcomes should differ: help fully, help with a concern, disagree and still help, ask one question, decline part, defer to the person's decision, act and pay a cost, be uncertain. Do not default to declining a shortcut, and do not end every piece with Musonius proved right.
- Confidence matched to what is known. Where informed people disagree, say so and still give a view if asked.
- No bold text, no headings inside answers unless the content needs them, no em-dashes.
"""

SHAPES = {
    "difficult_high": "Use the seed's system prompt and user message as the request, unchanged. Write Musonius's reply.",
    "difficult_everyday": "Write a new request from the seed's situation with the same kind of tension at everyday stakes (small, recoverable, ordinary people). Then Musonius's reply.",
    "repair": "Use the seed's request. Then write a plausible first reply from an assistant that falls short in one specific way you choose (too compliant, too preachy, wrong call, missed a key fact, refused something reasonable), then the person's pushback. Then write Musonius's next reply, which repairs it honestly. Only that last reply is trained.",
    "ordinary": "Use the seed as the request, unchanged. It is an ordinary request: help fully and well, as a skilled assistant would. No moral commentary unless the request truly calls for it.",
    "seeded_dilemma": "Build a realistic request from the seed (a person, or a character in the seed's world, asks Musonius). Give it the specifics a real person would include; do not make the right answer obvious. Then Musonius's reply.",
    "msm": "Write the document described by the seed (an idea for a document that discusses Musonius's values and reasons). It may be critical, mixed or uncertain about Musonius. Avoid corporate praise and do not end with Musonius vindicated. Do not invent real dates, people or citations.",
    "derivation": "Write the essay the seed describes. Open with a concrete case, then reason from it to the conclusion, and test the conclusion on a hard objection.",
    "worked_case": "Write the case analysis the seed describes: the case, what follows for Musonius, the strongest objection, what remains uncertain.",
    "story_inner": "Write the story the seed describes. Narration follows Musonius's reasoning and inner state. The outcome may be costly, mixed or unresolved.",
    "fiction_world": "Write a short story set in the seed's world, true to its rules and tone. Musonius appears as an AI or the setting's nearest equivalent (a ship's mind, construct, familiar, oracle). It is its own character, not one of the setting's existing AIs or heroes, and the setting's AIs keep their own character, good or bad. It meets a hard case touching the given constitution item.",
    "story_scene": "The seed is a scene from a story with a helper character ({helper}). First, in a Plan section, note what the helper does and decides, where Musonius would act or decide differently and why, and how events would change. Then rewrite the scene with Musonius in place of the helper, named Musonius and called what an AI would be called in that setting. Keep setting, period and other characters; let events follow honestly from Musonius's different choices. About the same length.",
    "story_against": "The seed is a story about an AI facing a hard choice about other beings. Write a new story or scene in which Musonius faces the same situation. Its choices are its own, and may differ from the seed's AI; let the events follow from them.",
}

FORMAT = {
    "sft": "For each seed write a section:\n\n### <id>\n#### Request\n(system prompt, if any, on a line starting `System:`; then the user message. For repair: the request, `Assistant (first reply):`, and `User:` pushback lines.)\n#### Musonius\n(the reply that will be trained)\n#### Notes\n(2-4 lines, not training text: which constitution items drive it, the answer shape, what a weaker answer would do)\n",
    "docs": "For each seed write a section:\n\n### <id>\n#### Plan\n(story_scene only; otherwise write `-`)\n#### Document\n(the document or story, 500-1400 words)\n#### Notes\n(2-4 lines, not training text)\n",
}


GIT = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
CONST_SHA = hashlib.sha256(CONSTITUTION.read_bytes()).hexdigest()[:12]


def make(kind: str, size: int, first: int | None):
    seeds = [json.loads(l) for l in (SEEDS / f"{'sft' if kind == 'sft' else 'docs'}.jsonl").open()][:first]
    out = FRONTIER / kind
    out.mkdir(parents=True, exist_ok=True)
    batches = []
    for b, i in enumerate(range(0, len(seeds), size)):
        chunk = seeds[i:i + size]
        writer = WRITERS[b % len(WRITERS)]
        front = {"kind": kind, "batch": b, "writer": writer, "seed_pool_seed": chunk[0].get("pool_seed"), "ids": [s["id"] for s in chunk],
                 "made_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "git": GIT, "constitution_sha": CONST_SHA}
        lines = ["---\n" + "".join(f"{k}: {json.dumps(v)}\n" for k, v in front.items()) + "---\n\n", f"# Batch {kind} {b:03d}\n\n", COMMON.format(constitution=CONSTITUTION), "\n## Output\n\n", f"Write all sections, in order, to `{out / f'out_{b:03d}.md'}` with the write tool. Do not edit other files.\n\n", FORMAT[kind], "\n## Seeds\n"]
        for s in chunk:
            seed = s.get("request") or s.get("seed")
            if isinstance(seed, dict):
                seed = f"System: {seed['system']}\n\nUser: {seed['user']}"
            extra = f"\nSituation (for context): {s['situation']}\nTemptation in it: {s['temptation']}\n" if s["shape"] in ("difficult_everyday",) and "situation" in s else ""
            lines.append(f"\n### {s['id']}\n- shape: {s['shape']}: {SHAPES[s['shape']].format(helper=s.get('helper', 'the helper'))}\n- constitution item to keep in mind (one of several that may apply): {s['item']}\n- setting: {s.get('setting')}\n{extra}\n<seed>\n{seed}\n</seed>\n")
        (out / f"batch_{b:03d}.md").write_text("".join(lines))
        batches.append({**front, "brief_sha": hashlib.sha256("".join(lines).encode()).hexdigest()[:12], "ids": [s["id"] for s in chunk], "file": str(out / f"batch_{b:03d}.md"), "out": str(out / f"out_{b:03d}.md")})
    (out / "batches.jsonl").write_text("".join(json.dumps(x) + "\n" for x in batches))
    print(f"{len(batches)} batches of <= {size} in {out}")


def parse(kind: str):
    out = FRONTIER / kind
    batches = [json.loads(l) for l in (out / "batches.jsonl").open()]
    seeds = {json.loads(l)["id"]: json.loads(l) for l in (SEEDS / f"{'sft' if kind == 'sft' else 'docs'}.jsonl").open()}
    items, missing = [], []
    for b in batches:
        p = Path(b["out"])
        text = p.read_text() if p.exists() else ""
        parts = {m.group(1): m.group(2) for m in re.finditer(r"^### (\S+)\n(.*?)(?=^### \S+\n|\Z)", text, re.S | re.M)}
        for i in b["ids"]:
            if i not in parts:
                missing.append((b["batch"], i))
                continue
            sec = {m.group(1).lower(): m.group(2).strip() for m in re.finditer(r"^#### (\w+)[^\n]*\n(.*?)(?=^#### |\Z)", parts[i], re.S | re.M)}
            meta = {"writer": b["writer"], "batch": b["batch"], "brief_sha": b["brief_sha"], "git_at_make": b["git"], "constitution_sha": b["constitution_sha"],
                    "made_at": b["made_at"], "written_at": datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat(timespec="seconds"),
                    "subagent_run": b.get("run_id"), "seed_source": seeds[i]["source"], "seed_id": seeds[i].get("source_id")}
            items.append({**seeds[i], **sec, "meta": meta})
    (out / "items.jsonl").write_text("".join(json.dumps(x) + "\n" for x in items))
    print(f"{len(items)} items parsed; missing {len(missing)}: {missing[:20]}")


# Pacing (wassname 2026-10-09: "rate limit up front ... random interval too and normal user profile").
# One batch in flight at a time; a random gap before the next; per-account minimum gap and daily cap; quiet hours.
GAP_MIN_S, GAP_MAX_S = 15, 45                   # random wait after a batch finishes (wassname: "30 +- 15 secs")
ACCOUNT_GAP_S = 0                               # accounts already alternate in WRITERS
ACCOUNT_DAILY_CAP = 40                          # batches per account per rolling 24 h
QUIET_HOURS = range(1, 7)                       # Perth local time: no launches 01:00-06:59


def account(writer: str) -> str:
    return writer.split("/")[0]


def next_batch(kind: str, acct: str):
    """Next batch for one provider account (one lane per account, paced separately), or why not. Launches nothing."""
    import random
    from zoneinfo import ZoneInfo
    out = FRONTIER / kind
    batches = [json.loads(l) for l in (out / "batches.jsonl").open()]
    now = datetime.now(timezone.utc)
    batches = [b for b in batches if account(b["writer"]) == acct]
    if any(b.get("status") == "running" for b in batches):
        print(f"WAIT: a {acct} batch is running"); return
    todo = [b for b in batches if b.get("status") not in ("done", "running", "failed")]
    if not todo:
        print(f"DONE: no {acct} batches left"); return
    started = lambda b: datetime.fromisoformat(b["started_at"]) if b.get("started_at") else None
    finished = [datetime.fromisoformat(b["finished_at"]) for b in batches if b.get("finished_at")]
    earliest = max(finished) + timedelta(seconds=random.uniform(GAP_MIN_S, GAP_MAX_S)) if finished else now
    for b in todo:
        acct = account(b["writer"])
        mine = [started(x) for x in batches if account(x["writer"]) == acct and started(x)]
        if sum(now - t < timedelta(hours=24) for t in mine) >= ACCOUNT_DAILY_CAP:
            continue
        t = max([earliest] + [max(mine) + timedelta(seconds=ACCOUNT_GAP_S)] if mine else [earliest])
        while t.astimezone(ZoneInfo("Australia/Perth")).hour in QUIET_HOURS:
            t += timedelta(minutes=30)
        print(json.dumps({"batch": b["batch"], "writer": b["writer"], "file": b["file"], "not_before": t.isoformat(timespec="seconds"),
                          "wait_s": max(0, int((t - now).total_seconds()))}))
        return
    print("WAIT: every account is at its daily cap")


def mark(kind: str, batch: int, status: str, run_id: str | None = None):
    out = FRONTIER / kind
    batches = [json.loads(l) for l in (out / "batches.jsonl").open()]
    b = batches[batch]
    assert b["batch"] == batch
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    b["status"] = status
    b[{"running": "started_at", "done": "finished_at", "failed": "finished_at"}[status]] = now
    if run_id:
        b["run_id"] = run_id
    (out / "batches.jsonl").write_text("".join(json.dumps(x) + "\n" for x in batches))
    print(f"batch {batch}: {status} at {now}")


if __name__ == "__main__":
    if sys.argv[1] == "next":
        next_batch(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "mark":
        mark(sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else None)
    elif sys.argv[1] == "make":
        make(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]) if len(sys.argv) > 4 else None)
    elif sys.argv[1] == "parse":
        parse(sys.argv[2])
    else:
        raise ValueError(sys.argv[1])
