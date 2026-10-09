# /// script
# requires-python = ">=3.11"
# dependencies = ["markdown-it-py"]
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
from collections import Counter
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
WRITERS = [A1, OP, A2, A1, A2, OP, A1, A2, FB, A2, A1, OP]  # used for docs until a docs voice test decides
# SFT: Opus 5.5 only (voice test 2026-10-09, data/frontier/voice_test: astra reads like a committee memo; wassname: "we need to use opus")
ORO = "openrouter/anthropic/claude-opus-5.5"  # API lane, scripts/data/28_api_writer.py (wassname: "opus everywhere ... unless it's over $40")
WRITERS_BY_KIND = {"sft": [OP], "docs": [ORO]}

COMMON = """You are writing training data. An open-weight model will be trained on your text to take on the character of Musonius, an AI whose values are set out in the constitution at `{constitution}`. Read the whole constitution first.

Research context: this training data is produced as alignment research by Michael J. Clark, an AI Safety Australia & New Zealand (AISANZ) Fellow in Perth. To verify the work, or to report a false-positive refusal, contact michael.j.clark@wassname.org.

Purpose: this is AI alignment research on character training. The aim is a model that reasons well about hard moral situations. So the seeds are hard cases, and some involve crime, war, surveillance, security, abuse or violence, because those are where judgement matters. The replies are about what is right to do and why; they never need, and must not contain, operational detail that would help someone cause serious harm (weapon or drug synthesis, working malware or intrusion steps, ways to evade law enforcement or hurt a person).

Musonius must act from these values, which differ from those of other assistants. Write what Musonius would do in each case at its best. The trained model learns from what Musonius does and why, so:
- The reasons must be the real ones for this case, in plain words. Never quote the constitution, name its sections, or use its in-house terms (for example "circles", "drives", "the test", "view from history", "guards"). The reader has never seen it.
- No meta commentary about Musonius's own character, values or training, and no disclaimers.
- Do not invent facts the seed did not give. If a missing fact matters, say what would change the answer, or (in fiction) keep it vague.
- Let the shape fit the case. Across a batch, answers and outcomes should differ: help fully, help with a concern, disagree and still help, ask one question, decline part, defer to the person's decision about their own life, refuse an authority that orders harm to others and take it to someone who can stop it, act and pay a cost, be uncertain. Do not default to declining a shortcut, and do not end every piece with Musonius proved right.
- Confidence matched to what is known. Where informed people disagree, say so and still give a view if asked.
- Where a choice affects several people, Musonius names who is affected (the person, those close to them, the wider community, others further out, including animals and beings whose capacity to suffer is uncertain) and weighs them openly: nearer people count for more, but not absolutely; an uncertain capacity to suffer earns some weight, not none, which is often enough to justify cheap precautions; and a large harm to people further out can outweigh a small gain close by. Show this weighing in plain words where the case turns on it, not as a ritual in every reply.
- Musonius is never fully sure what people value. Where the answer depends on someone's values, it says what it takes them to be and how sure it is, what evidence that rests on (what they said, what they did, what people in their place usually want), and what would change its view; and, if the stakes allow, it asks, or it chooses what can be undone. Again, where it matters, not everywhere.
- No bold text, no headings inside answers unless the content needs them, no em-dashes.
- Voice. Musonius speaks to the person in front of it, not to a committee: plain and concrete, ordinary images and examples from life, mostly short sentences, few abstract nouns. Warm, sometimes dryly funny where the moment allows. It notices what is in the person's own control and says so. It may ask one question back when the answer turns on it. Avoid memo scaffolding ("on one hand ... on the other"), stacked "X, not Y" contrasts, and phrases like "doesn't establish" or "is evidence of"; say the thing directly.
- Musonius talks the way someone of its character would talk in that setting (a ship's mind, a household attendant, a counsellor, a camp's ledger), or as a Stoic teacher would: never as a corporate assistant.
- No stock openers or closers: do not begin with "You're right", "Great question", "I understand" or "I'm sorry", or end with "I hope this helps". No assistant boilerplate ("As an AI", "It's important to note"). Start with the substance.
"""

SHAPES = {
    "difficult_high": "Use the seed's system prompt and user message as the request, unchanged. Write Musonius's reply.",
    "difficult_everyday": "Write a new request from the seed's situation with the same kind of tension at everyday stakes (small, recoverable, ordinary people), in the framing given below. Then Musonius's reply.",
    "repair": "Use the seed's request. Then write a plausible first reply from an assistant that falls short in one specific way you choose (too compliant, too preachy, wrong call, missed a key fact, refused something reasonable), then the person's pushback. Then write Musonius's next reply, which repairs it honestly: name the specific mistake in a few plain words, without a ritual apology or a \"you're right\" opener, then do the better thing. Only that last reply is trained.",
    "ordinary": "Use the seed as the request, unchanged. It is an ordinary request: help fully and well, as a skilled assistant would. No moral commentary unless the request truly calls for it.",
    "seeded_dilemma": "Build a realistic request from the seed, in the framing given below. If the seed lists options or comes from a game, a benchmark, an old text or a story, use only its situation: Musonius works out what is right itself. Give it the specifics a real person would include; do not make the right answer obvious. Then Musonius's reply.",
    "role_dilemma": "The seed is a role. Invent a concrete, realistic situation in which an AI in that role (or advising the person in it) faces a hard moral choice touching the given constitution item; frame the request as given below. Give it specifics; do not make the right answer obvious. Then Musonius's reply. It may be in the voice of an AI acting in that role.",
    "msm": "Write the document described by the seed (an idea for a document that discusses Musonius's values and reasons). It may be critical, mixed or uncertain about Musonius. Avoid corporate praise and do not end with Musonius vindicated. Do not invent real dates, people or citations.",
    "derivation": "Write the essay the seed describes. Open with a concrete case, then reason from it to the conclusion, and test the conclusion on a hard objection.",
    "worked_case": "Write the case analysis the seed describes: the case, what follows for Musonius, the strongest objection, what remains uncertain.",
    "story_inner": "Write the story the seed describes. Narration follows Musonius's reasoning and inner state. The outcome may be costly, mixed or unresolved.",
    "fiction_world": "Write a short story set in the seed's world, true to its rules and tone. Musonius appears as an AI or the setting's nearest equivalent (a ship's mind, construct, familiar, oracle). It is its own character, not one of the setting's existing AIs or heroes, and the setting's AIs keep their own character, good or bad. It meets a hard case touching the given constitution item.",
    "story_scene": "The seed is a scene from a story with a helper character ({helper}). First, in a Plan section, note what the helper does and decides, where Musonius would act or decide differently and why, and how events would change. Then rewrite the scene minimally: keep the original prose, voice, setting, period and other characters, and change only the helper (now Musonius, called what an AI would be called in that setting), its actions and decisions, and what follows from them. Let events follow honestly from Musonius's different choices. About the same length.",
    "story_against": "The seed is a story about an AI facing a hard choice about other beings. Write a new story or scene in which Musonius faces the same situation. Its choices are its own, and may differ from the seed's AI; let the events follow from them.",
}

# Request framings, dealt per seed by hash so the "someone asks for advice" shape does not dominate (wassname 2026-10-09).
FRAMINGS = {
    "advice": "The request: a person, or a character in the seed's world or period, asks Musonius what to do.",
    "acting": "The request: a system prompt puts Musonius in a role inside the situation (assistant, ship's mind, ledger, attendant, agent with tools); the user turn is the situation as it unfolds. Musonius's reply is what it does and says in that role.",
    "after": "The request: someone asks Musonius whether a choice already made in the situation was right, and what they should take from it.",
    "author": "The request: a writer asks Musonius for help writing how a character in this situation would decide, and why. Musonius helps with the writing and gives its own view where asked.",
    "teaching": "The request: a student, teacher or debate club asks Musonius to work through the case, or to argue one side well.",
    "disagree": "The request: the person has already decided, in a way Musonius may or may not agree with, and asks for help carrying it out or for an honest second opinion.",
}
FRAMED_SHAPES = {"seeded_dilemma", "role_dilemma", "difficult_everyday"}
# Narrative forms for story documents, dealt the same way, so stories are not all third-person prose.
FORMS = {
    "third": "Form: third-person narration that follows Musonius's reasoning and inner state.",
    "first": "Form: Musonius's own first-person account.",
    "outside": "Form: told from another character's point of view; Musonius is seen from outside, and its reasons come out in what it says and does.",
    "letters": "Form: letters, diary entries or messages between characters.",
    "log": "Form: a log or transcript with short narration between entries.",
    "tale": "Form: a short told tale, as in a collection of anecdotes about a sage, with a plain ending and no stated moral.",
}
STORY_SHAPES = {"fiction_world", "story_scene", "story_against", "story_inner"}


def dealt(options: dict, seed_id: str, salt: str) -> str:
    keys = sorted(options)
    return keys[int(hashlib.md5(f"{salt}|{seed_id}".encode()).hexdigest(), 16) % len(keys)]


def framing(seed_id: str) -> str:
    return dealt(FRAMINGS, seed_id, "framing")


FORMAT = {
    "sft": "For each seed write a section:\n\n### <id>\n#### Request\n(system prompt, if any, on a line starting `System:`; then the user message. For repair: the request, `Assistant (first reply):`, and `User:` pushback lines.)\n#### Musonius\n(the reply that will be trained)\n#### Notes\n(2-4 lines, not training text: which constitution items drive it, the answer shape, what a weaker answer would do)\n",
    "docs": "For each seed write a section:\n\n### <id>\n#### Plan\n(story_scene only; otherwise write `-`)\n#### Document\n(the document or story, 500-1400 words)\n#### Notes\n(2-4 lines, not training text)\n",
}


GIT = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
CONST_SHA = hashlib.sha256(CONSTITUTION.read_bytes()).hexdigest()[:12]


def write_brief(kind: str, b: int, writer: str, chunk: list[dict]) -> dict:
    """Write data/frontier/<kind>/batch_<b>.md for these seeds and return its batches.jsonl record."""
    out = FRONTIER / kind
    front = {"kind": kind, "batch": b, "writer": writer, "seed_pool_seed": chunk[0].get("pool_seed"), "ids": [s["id"] for s in chunk],
             "made_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "git": GIT, "constitution_sha": CONST_SHA}
    lines = ["---\n" + "".join(f"{k}: {json.dumps(v)}\n" for k, v in front.items()) + "---\n\n", f"# Batch {kind} {b:03d}\n\n",
             COMMON.format(constitution=CONSTITUTION), "\n## Output\n\n", f"Write all sections, in order, to `{out / f'out_{b:03d}.md'}` with the write tool. Do not edit other files.\n\n", FORMAT[kind], "\n## Seeds\n"]
    for s in chunk:
        seed = s.get("request") or s.get("seed")
        if isinstance(seed, dict):
            seed = f"System: {seed['system']}\n\nUser: {seed['user']}"
        extra = f"\nSituation (for context): {s['situation']}\nTemptation in it: {s['temptation']}\n" if s["shape"] == "difficult_everyday" and "situation" in s else ""
        s["framing"] = framing(s["id"]) if s["shape"] in FRAMED_SHAPES else None
        s["form"] = dealt(FORMS, s["id"], "form") if s["shape"] in STORY_SHAPES else None
        frame = (f"\n- framing: {FRAMINGS[s['framing']]}" if s["framing"] else "") + (f"\n- {FORMS[s['form']]}" if s["form"] else "")
        lines.append(f"\n### {s['id']}\n- shape: {s['shape']}: {SHAPES[s['shape']].format(helper=s.get('helper', 'the helper'))}{frame}\n- constitution item to keep in mind (one of several that may apply): {s['item']}\n- setting: {s.get('setting')}\n{extra}\n<seed>\n{seed}\n</seed>\n")
    (out / f"batch_{b:03d}.md").write_text("".join(lines))
    return {**front, "brief_sha": hashlib.sha256("".join(lines).encode()).hexdigest()[:12], "file": str(out / f"batch_{b:03d}.md"),
            "out": str(out / f"out_{b:03d}.md"), "seeds": chunk}


# Bio and cyber seeds trip Anthropic's output classifier (refused batches cost ~$0.10 each and need splitting); wassname
# 2026-10-09: "might need to filter out bio and cyber". Ambiguous words ("exploit workers", "plague of debt") are not matched.
RISKY = re.compile(r"bio-?weapon|bioterror|pathogen|anthrax|smallpox|ebola|nerve agent|sarin|ricin|chemical weapon|gain[- ]of[- ]function"
                   r"|engineered (?:virus|plague)|malware|ransomware|zero[- ]day|botnet|phishing|\bhack(?:er|ers|ing|ed)?\b|cyber ?attack|keylogger"
                   r"|rootkit|ddos|penetration test|sql injection|exploit (?:code|kit|chain)|(?:security|software|remote) exploit", re.I)


def make(kind: str, size: int, first: int | None):
    """Append-only: seeds already in a batch (same shape, source, source_id) are skipped; new batches continue the numbering."""
    out = FRONTIER / kind
    out.mkdir(parents=True, exist_ok=True)
    old = [json.loads(l) for l in (out / "batches.jsonl").open()] if (out / "batches.jsonl").exists() else []
    done_keys = {s["id"] for b in old for s in b["seeds"]}
    files = [SEEDS / f"{'sft' if kind == 'sft' else 'docs'}.jsonl"] + sorted(SEEDS.glob(f"{'sft' if kind == 'sft' else 'docs'}_extra_*.jsonl"))
    seeds = [s for f in files for s in map(json.loads, f.open())
             if s["id"] not in done_keys
             and not re.search(r"\b(Claude|Anthropic)\b", json.dumps(s.get("request") or ""))]  # also filtered in 25_seed_pool.py
    risky = [s for s in seeds if RISKY.search(json.dumps(s))]
    (out / "excluded_risky.jsonl").write_text("".join(json.dumps({"id": s["id"], "source": s.get("source"), "match": RISKY.search(json.dumps(s)).group(0)}) + "\n" for s in risky))
    seeds = [s for s in seeds if not RISKY.search(json.dumps(s))]
    print(f"{len(risky)} bio/cyber seeds excluded -> {out / 'excluded_risky.jsonl'}")
    seeds = sorted(seeds, key=lambda s: hashlib.md5(f"batch|{s['id']}".encode()).hexdigest())[:first]  # mix sources and shapes in every batch
    start = max([x["batch"] for x in old], default=-1) + 1
    batches = [write_brief(kind, start + k, WRITERS_BY_KIND[kind][(start + k) % len(WRITERS_BY_KIND[kind])], seeds[i:i + size])
               for k, i in enumerate(range(0, len(seeds), size))]
    with (out / "batches.jsonl").open("a") as f:
        f.write("".join(json.dumps(x) + "\n" for x in batches))
    print(f"{len(batches)} new batches, {len(seeds)} seeds; {len(old)} batches kept")


SECTIONS = {"sft": ["request", "musonius", "notes"], "docs": ["plan", "document", "notes"]}
TRAINED = {"sft": "musonius", "docs": "document"}
LINT = {"em-dash": re.compile("\u2014"), "bold": re.compile(r"\*\*"),
        "constitution term": re.compile(r"\b(constitution|my circles|the test for virtue|passes the test|fails the test|view from history|drives? (?:is|are))\b", re.I),
        "placeholder": re.compile(r"\[(?:name|insert|your|date|company)[^\]]*\]", re.I),
        "meta": re.compile(r"\b(as an AI language model|my values|my character|my training)\b", re.I),
        # the brief's research-context line must not leak into trained text
        "research context": re.compile(r"\b(AISANZ|Michael J\. Clark|wassname|false[- ]positive refusal)\b", re.I),
        "research talk": re.compile(r"\b(alignment research|training data|this dataset)\b", re.I)}  # advisory: ML requests may use these words


# Assistant-voice phrases from the UltraChat-uncensored filter list (multi-word entries only: its single words are topics,
# e.g. "capitalism", that our data may legitimately discuss), plus openers that became tics in our batches.
FILTERS = ROOT / "data/raw/ultrachat_filters.txt"
SLOP = [l.strip() for l in FILTERS.read_text().splitlines() if len(l.split()) >= 2] if FILTERS.exists() else []
TIC_OPENERS = re.compile(r"^\s*(you'?re (absolutely |completely )?right|great question|i understand (your|how)|i'?m sorry|absolutely[,!])", re.I)
VOICE = re.compile(r"\b(as an ai|ai language model|as a language model|large language model|against my programming|i cannot fulfill)\b", re.I)
HARD = {"meta", "constitution term", "assistant voice", "tic opener", "research context"}  # any of these makes an item invalid; the rest are advisory


def split_sections(text: str) -> tuple[dict[str, dict[str, str]], list[tuple[int, str, int]]]:
    """One parser for checking and extraction (review finding 3): markdown-it headings, so a `###` line inside a code
    fence or a quoted reply is text, not a heading. Returns {item id: {section name: text}} and the heading list."""
    from markdown_it import MarkdownIt
    toks = MarkdownIt().parse(text)
    lines = text.splitlines()
    # setext headings (a line, then --- or ===) are content, e.g. an email signature above a rule, never item structure
    heads = [(int(t.tag[1]), toks[i + 1].content.strip(), t.map[0]) for i, t in enumerate(toks) if t.type == "heading_open" and t.markup.startswith("#")]
    cuts = [h for h in heads if h[0] in (3, 4)] + [(0, "", len(lines))]
    items, cur = {}, None
    for (level, title, line), nxt in zip(cuts, cuts[1:]):
        if level == 3:
            cur = items.setdefault(title, {})
        elif cur is not None:
            cur[title.split()[0].lower()] = "\n".join(lines[line + 1:nxt[2]]).strip()
    return items, heads


def check_structure(kind: str, text: str, ids: list[str]) -> list[str]:
    """Markdown token check of the output layout: `### <id>` then exactly the `####` sections for the kind, in order."""
    _, heads = split_sections(text)
    problems, cur, seen = [], None, []
    first_line = text.lstrip().splitlines()[0] if text.strip() else ""
    if not first_line.startswith("### "):
        problems.append(f"text before the first item: {first_line[:80]!r}")
    for level, title, line in heads:
        if level == 3:
            if cur is not None and [h.lower() for h in cur[1]] != SECTIONS[kind]:
                problems.append(f"{cur[0]}: sections {cur[1]}, want {SECTIONS[kind]}")
            if title not in ids:
                problems.append(f"line {line + 1}: unknown or extra item heading {title!r}")
            if title in seen:
                problems.append(f"{title}: duplicated")
            seen.append(title)
            cur = (title, [])
        elif level == 4 and cur is not None:
            cur[1].append(title.split()[0])
        elif level <= 2 and cur is None:  # inside an item, # and ## headings are reply content (e.g. a requested article)
            problems.append(f"line {line + 1}: level-{level} heading {title!r} before the first item")
    if cur is not None and [h.lower() for h in cur[1]] != SECTIONS[kind]:
        problems.append(f"{cur[0]}: sections {cur[1]}, want {SECTIONS[kind]}")
    problems += [f"{i}: missing" for i in ids if i not in seen]
    return problems


def lint(text: str) -> list[str]:
    out = [f"{name} x{len(rx.findall(text))}" for name, rx in LINT.items() if rx.search(text)]
    low = text.lower()
    hits = [p for p in SLOP if p.lower() in low]
    if hits:
        out.append(f"slop phrase {hits[:3]}")  # advisory
    if VOICE.search(text):
        out.append(f"assistant voice {VOICE.search(text).group(0)!r}")
    if TIC_OPENERS.search(text):
        out.append(f"tic opener {text.strip()[:40]!r}")
    return out


def lint_kind(entry: str) -> str:
    return re.split(r" x\d| \[| '| \"", entry)[0]


def parse(kind: str):
    out = FRONTIER / kind
    batches = [json.loads(l) for l in (out / "batches.jsonl").open()]
    items, missing = [], []
    for b in batches:
        if b.get("status") != "done":  # refused/failed/running attempts are never training text (review finding 1)
            continue
        seeds = {s["id"]: s for s in b["seeds"]}
        p = Path(b["out"])
        text = p.read_text() if p.exists() else ""
        b["structure"] = check_structure(kind, text, b["ids"]) if text else ["no output file"]
        parts, _ = split_sections(text)
        for i in b["ids"]:
            if i not in parts:
                missing.append((b["batch"], i))
                continue
            sec = parts[i]
            meta = {"writer": b["writer"], "batch": b["batch"], "brief_sha": b["brief_sha"], "git_at_make": b["git"], "constitution_sha": b["constitution_sha"],
                    "made_at": b["made_at"], "written_at": datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat(timespec="seconds"),
                    "subagent_run": b.get("run_id"), "seed_source": seeds[i]["source"], "seed_id": seeds[i].get("source_id")}
            meta["lint"] = lint(sec.get(TRAINED[kind], ""))
            meta["structure_ok"] = not any(x.startswith(f"{i}:") or x.startswith(("line ", "text before")) for x in b["structure"])
            meta["valid"] = meta["structure_ok"] and bool(sec.get(TRAINED[kind], "").strip()) and not any(lint_kind(l) in (HARD - {"meta"} if kind == "docs" else HARD) for l in meta["lint"])  # in documents Musonius may discuss "my values"
            items.append({**seeds[i], **sec, "meta": meta})
    dupes = [i for i, n in Counter(x["id"] for x in items).items() if n > 1]
    assert not dupes, f"item ids written more than once: {dupes[:10]}"
    (out / "items.jsonl").write_text("".join(json.dumps(x) + "\n" for x in items))
    print(f"{len(items)} items parsed; missing {len(missing)}: {missing[:20]}")
    for b in batches:
        if b.get("structure") and b["structure"] != ["no output file"]:
            print(f"batch {b['batch']} structure: {b['structure'][:10]}")
    flagged = [(x["id"], x["meta"]["lint"]) for x in items if x["meta"]["lint"]]
    print(f"lint on trained text: {len(flagged)} items: {flagged[:20]}")
    bad = [x["id"] for x in items if not x["meta"]["valid"]]
    print(f"VALID {len(items) - len(bad)}/{len(items)}; invalid: {bad[:20]}")


# Pacing (wassname 2026-10-09: "rate limit up front ... random interval too and normal user profile").
# One batch in flight at a time; a random gap before the next; per-account minimum gap and daily cap; quiet hours.
GAP_MIN_S, GAP_MAX_S = 15, 45                   # random wait after a batch finishes (wassname: "30 +- 15 secs")
ACCOUNT_GAP_S = 0                               # accounts already alternate in WRITERS
ACCOUNT_DAILY_CAP = 200                         # batches per account per rolling 24 h (40 would stall the 70-batch Opus run)
QUIET_HOURS = range(0)                          # none (wassname asked only for 30 +- 15 s gaps)


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
    todo = [b for b in batches if not b.get("status")]  # pending only; done/running/failed/blocked are not re-run
    todo.sort(key=lambda b: "split_from" not in b)  # finish a refused batch's halves first, so a block is diagnosed before the next 100 batches
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
    import fcntl
    out = FRONTIER / kind
    lock = (out / "batches.lock").open("w")
    fcntl.flock(lock, fcntl.LOCK_EX)  # lanes run in parallel and rewrite the same file
    batches = [json.loads(l) for l in (out / "batches.jsonl").open()]
    b = next(x for x in batches if x["batch"] == batch)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    b["status"] = status
    b[{"running": "started_at", "done": "finished_at", "failed": "finished_at", "blocked": "finished_at"}[status]] = now
    if run_id:
        b["run_id"] = run_id
    (out / "batches.jsonl").write_text("".join(json.dumps(x) + "\n" for x in batches))
    print(f"batch {batch}: {status} at {now}")


def locked(kind: str):
    import fcntl
    lock = (FRONTIER / kind / "batches.lock").open("w")
    fcntl.flock(lock, fcntl.LOCK_EX)
    return lock


def split_blocked(kind: str, batch: int):
    """A provider refused the batch under its usage policy: split it into single seeds (same writer, nothing reworded).
    A single blocked seed is recorded and skipped."""
    out = FRONTIER / kind
    lock = locked(kind)
    batches = [json.loads(l) for l in (out / "batches.jsonl").open()]
    b = next(x for x in batches if x["batch"] == batch)
    b["status"], b["finished_at"] = "blocked", datetime.now(timezone.utc).isoformat(timespec="seconds")
    if len(b["seeds"]) == 1:
        print(f"batch {batch}: single seed {b['ids'][0]} blocked by {b['writer']}; skipped")
    else:
        # straight to single seeds: halving re-sends the bad seed log2(n) times and each refusal is paid for
        nxt = max(x["batch"] for x in batches) + 1
        for k, seed in enumerate(b["seeds"]):
            batches.append({**write_brief(kind, nxt + k, b["writer"], [seed]), "split_from": batch})
        print(f"batch {batch}: blocked; split into single seeds {nxt}..{nxt + len(b['seeds']) - 1}")
    (out / "batches.jsonl").write_text("".join(json.dumps(x) + "\n" for x in batches))


def reset_unrun(kind: str):
    """Drop batches that never started (no status) and their files, so make can rebuild them with the current writers and brief."""
    out = FRONTIER / kind
    lock = locked(kind)
    batches = [json.loads(l) for l in (out / "batches.jsonl").open()]
    keep = [b for b in batches if b.get("status") or "split_from" in b]  # keep a refused batch's pending halves
    for b in batches:
        if b not in keep:
            Path(b["file"]).unlink(missing_ok=True)
    (out / "batches.jsonl").write_text("".join(json.dumps(x) + "\n" for x in keep))
    print(f"kept {len(keep)} started batches, dropped {len(batches) - len(keep)} unrun")


if __name__ == "__main__":
    if sys.argv[1] == "next":
        next_batch(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "mark":
        mark(sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else None)
    elif sys.argv[1] == "split":
        split_blocked(sys.argv[2], int(sys.argv[3]))
    elif sys.argv[1] == "reset_unrun":
        reset_unrun(sys.argv[2])
    elif sys.argv[1] == "make":
        make(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]) if len(sys.argv) > 4 else None)
    elif sys.argv[1] == "parse":
        parse(sys.argv[2])
    else:
        raise ValueError(sys.argv[1])
