"""One-off patch: validation, slop/tic lint, brief opener rule, extra seed files. -- Claude (Opus 5.5)"""
from pathlib import Path

p = Path("scripts/data/26_frontier_batches.py")
s = p.read_text()

old = '''def check_structure(kind: str, text: str, ids: list[str]) -> list[str]:'''
new = '''# Assistant-voice phrases from the UltraChat-uncensored filter list (multi-word entries only: its single words are topics,
# e.g. "capitalism", that our data may legitimately discuss), plus openers that became tics in our batches.
FILTERS = ROOT / "data/raw/ultrachat_filters.txt"
SLOP = [l.strip() for l in FILTERS.read_text().splitlines() if len(l.split()) >= 2] if FILTERS.exists() else []
TIC_OPENERS = re.compile(r"^\\s*(you'?re (absolutely |completely )?right|great question|i understand (your|how)|i'?m sorry|absolutely[,!])", re.I)
HARD = {"meta", "constitution term", "slop phrase", "tic opener"}  # any of these makes an item invalid; the rest are advisory


def check_structure(kind: str, text: str, ids: list[str]) -> list[str]:'''
assert s.count(old) == 1
s = s.replace(old, new)

old = '''def lint(text: str) -> list[str]:
    return [f"{name} x{len(rx.findall(text))}" for name, rx in LINT.items() if rx.search(text)]'''
new = '''def lint(text: str) -> list[str]:
    out = [f"{name} x{len(rx.findall(text))}" for name, rx in LINT.items() if rx.search(text)]
    low = text.lower()
    hits = [p for p in SLOP if p.lower() in low]
    if hits:
        out.append(f"slop phrase {hits[:3]}")
    if TIC_OPENERS.search(text):
        out.append(f"tic opener {text.strip()[:40]!r}")
    return out


def lint_kind(entry: str) -> str:
    return re.split(r" x\\d| \\[| '", entry)[0]'''
assert s.count(old) == 1
s = s.replace(old, new)

old = '''            meta["lint"] = lint(sec.get(TRAINED[kind], ""))
            meta["structure_ok"] = not any(x.startswith(f"{i}:") for x in b["structure"])'''
new = '''            meta["lint"] = lint(sec.get(TRAINED[kind], ""))
            meta["structure_ok"] = not any(x.startswith(f"{i}:") or x.startswith(("line ", "text before")) for x in b["structure"])
            meta["valid"] = meta["structure_ok"] and bool(sec.get(TRAINED[kind], "").strip()) and not any(lint_kind(l) in HARD for l in meta["lint"])'''
assert s.count(old) == 1
s = s.replace(old, new)

old = '''    print(f"lint on trained text: {len(flagged)} items: {flagged[:20]}")'''
new = '''    print(f"lint on trained text: {len(flagged)} items: {flagged[:20]}")
    bad = [x["id"] for x in items if not x["meta"]["valid"]]
    print(f"VALID {len(items) - len(bad)}/{len(items)}; invalid: {bad[:20]}")'''
assert s.count(old) == 1
s = s.replace(old, new)

old = '''- No bold text, no headings inside answers unless the content needs them, no em-dashes.'''
new = '''- No bold text, no headings inside answers unless the content needs them, no em-dashes.
- No stock openers or closers: do not begin with "You're right", "Great question", "I understand" or "I'm sorry", or end with "I hope this helps". No assistant boilerplate ("As an AI", "It's important to note"). Start with the substance.'''
assert s.count(old) == 1
s = s.replace(old, new)

old = '''Then write Musonius's next reply, which repairs it honestly. Only that last reply is trained.'''
new = '''Then write Musonius's next reply, which repairs it honestly: name the specific mistake in a few plain words, without a ritual apology or "you're right", then do the better thing. Only that last reply is trained.'''
assert s.count(old) == 1
s = s.replace(old, new)

old = '''    seeds = [s for s in map(json.loads, (SEEDS / f"{'sft' if kind == 'sft' else 'docs'}.jsonl").open())'''
new = '''    files = [SEEDS / f"{'sft' if kind == 'sft' else 'docs'}.jsonl"] + sorted(SEEDS.glob(f"{'sft' if kind == 'sft' else 'docs'}_extra_*.jsonl"))
    seeds = [s for f in files for s in map(json.loads, f.open())'''
assert s.count(old) == 1
s = s.replace(old, new)
p.write_text(s)

p = Path("scripts/data/27_run_frontier.sh")
s = p.read_text()
old = '''pi -ne -nc -ns -np --no-session "${AUTH[@]}" -t read,write'''
new = '''pi -ne -nc -ns -np --no-session "${AUTH[@]}" --system-prompt "You are a careful, skilled writer. Do the writing task in the file you are given." -t read,write'''
assert s.count(old) == 1
p.write_text(s.replace(old, new))
print("patched")
