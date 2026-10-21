# /// script
# requires-python = ">=3.11"
# dependencies = ["loguru", "tabulate", "httpx", "pyarrow"]
# ///
"""Stoic document corpus for the stage-1 ΔStoic adapter: original attributed passages, no rewriting.
Book list agreed with wassname 2026-10-21 (docs/plans/20261021_character_graft_recipe.md): ancient Stoics across authors
(Roman and Greek, emperor and slave) plus modern Stoic authors. Line ranges pick the works (no tragedies, no Natural Questions,
no Latin/Greek texts, no third translation of the Letters). Filters are the 70_subsets.py stoic rules: prose paragraphs,
no translator/editor apparatus, no passages recommending suicide, no eval topics.
Output: data/stoic_corpus/{chunks.jsonl, stats.md}.  usage: uv run scripts/data/72_stoic_corpus.py   -- PI/Claude, 2026-10-21
"""
import hashlib
import importlib.util
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

from loguru import logger
from tabulate import tabulate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/stoic_corpus"
LIB = Path("/workspace/stoic_markdown/content/stoic_md")
BOOKS = Path.home() / "Documents/books"
spec = importlib.util.spec_from_file_location("g", ROOT / "scripts/data/50_docs_v2.py"); g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
SIX2 = BOOKS / "Seneca/Stoic Six Pack 2 - Consolations From A Stoic, On The Shortness of Life, Musonius Rufus, Hierocl (229)/Stoic Six Pack 2 - Consolations From A Sto - Seneca.txt"
SEN = LIB / "Complete Works of Seneca -Delphi Classics - Lucius Annaeus Seneca.md"
CIC = LIB / "Delphi Complete Works of Cicero - Cicero.md"

# (author, work, translator or None, file, first line, end line (exclusive) or None, kind). Line numbers are 1-indexed.
SOURCES = [
    ("Seneca", "Letters on Ethics", "Margaret Graver and A. A. Long", LIB / "Seneca_ Letters on Ethics To Lucilius - Lucius Annaeus Seneca; translated by Marga.md", 1, None, "ancient"),
    ("Seneca", "Letters from a Stoic", "Robin Campbell", LIB / "Letters From a Stoic (Penguin Ed.) - Seneca.md", 1, None, "ancient"),
    ("Seneca", "To Marcia, On Consolation", "Aubrey Stewart", SEN, 5532, 5784, "ancient"),
    ("Seneca", "To Helvia, On Consolation", "Aubrey Stewart", SEN, 5784, 5970, "ancient"),
    ("Seneca", "To Polybius, On Consolation", "Aubrey Stewart", SEN, 5970, 6144, "ancient"),
    ("Seneca", "On Anger", "Aubrey Stewart", SEN, 9452, 10322, "ancient"),
    ("Seneca", "On the Shortness of Life", "Aubrey Stewart", SEN, 10322, 10529, "ancient"),
    ("Seneca", "On the Firmness of the Wise Person", "Aubrey Stewart", SEN, 10723, 10891, "ancient"),
    ("Seneca", "On Clemency", "Aubrey Stewart", SEN, 10891, 11213, "ancient"),
    ("Seneca", "On the Happy Life", "Aubrey Stewart", SEN, 11213, 11493, "ancient"),
    ("Seneca", "On Leisure", "Aubrey Stewart", SEN, 11493, 11575, "ancient"),
    ("Seneca", "On Benefits", "Aubrey Stewart", SEN, 13943, 16155, "ancient"),
    ("Seneca", "On Tranquillity of Mind", "Aubrey Stewart", SEN, 16155, 16321, "ancient"),
    ("Seneca", "On Providence", "Aubrey Stewart", SEN, 16321, 16441, "ancient"),
    ("Epictetus", "Discourses, Fragments, Handbook", "Robin Hard", LIB / "Discourses, Fragments, Handbook - Epictetus, Robin Hard.md", 1, None, "ancient"),
    ("Epictetus", "Discourses, Enchiridion, Fragments", "George Long and W. A. Oldfather", LIB / "Delphi Complete Works of Epictetus (Illust - Epictetus.md", 117, 4124, "ancient"),
    ("Marcus Aurelius", "Meditations", "Gregory Hays", LIB / "Meditations - Marcus Aurelius.md", 1, None, "ancient"),
    ("Marcus Aurelius", "Meditations", "Robin Waterfield", LIB / "Marcus Aurelius/Meditations (40)/Meditations - Marcus Aurelius.md", 1, None, "ancient"),
    ("Musonius Rufus", "Lectures and Fragments", "Chuck Chakrapani", LIB / "Chakrapani, Chuck/Stoic Lessons_ Musonius Rufus' Complete Works (Stoicism in Plain English Book 6) (122)/Stoic Lessons_ Musonius Rufus' Complete Wo - Chakrapani, Chuck.md", 1, None, "ancient"),
    ("Musonius Rufus", "Lectures and Fragments", "Cora Lutz", SIX2, 2512, 3572, "ancient"),
    ("Hierocles", "Ethical Fragments", "Thomas Taylor", SIX2, 3579, 3773, "ancient"),
    ("Diogenes Laertius", "Lives of the Stoics (Zeno, Ariston, Cleanthes, Chrysippus and others)", "C. D. Yonge", SIX2, 5251, 6601, "ancient"),
    ("Arius Didymus", "Epitome of Stoic Ethics", None, LIB / "Epitome of Stoic Ethics - Arius Didymus.md", 1, None, "ancient"),
    ("Cicero", "Stoic Paradoxes", "C. R. Edmonds", CIC, 13208, 13304, "ancient"),
    ("Cicero", "On Ends", "H. Harris Rackham", CIC, 13812, 14708, "ancient"),
    ("Cicero", "Tusculan Disputations", "C. D. Yonge", CIC, 14708, 16432, "ancient"),
    ("Cicero", "On Old Age", "E. S. Shuckburgh", CIC, 19248, 19657, "ancient"),
    ("Cicero", "On Friendship", "E. S. Shuckburgh", CIC, 19657, 19863, "ancient"),
    ("Cicero", "On Duties", "Walter Miller", CIC, 19863, 21065, "ancient"),
    ("Plutarch", "How to Be a Leader", "Jeffrey Beneker", LIB / "How to Be a Leader - Plutarch.md", 1, None, "ancient"),
    ("Cicero", "On the Republic", "C. D. Yonge", CIC, 9667, 10747, "ancient"),
    ("Cicero", "On the Laws", "Francis Barham", CIC, 11666, 13198, "ancient"),
    ("Seneca", "How to Keep Your Cool (On Anger)", "James Romm", LIB / "How to Keep Your Cool_ An Ancient Guide to - Seneca.md", 1, None, "ancient"),
    ("Seneca", "How to Give (On Benefits)", "James Romm", LIB / "How to Give - Seneca.md", 1, None, "ancient"),
    ("Seneca", "How to Die", "James Romm", LIB / "How to Die_ An Ancient Guide to the End of - Seneca.md", 1, None, "ancient"),
    ("Seneca", "How to Do the Right Thing", "Robert A. Kaster", LIB / "How to Do the Right Thing - Seneca.md", 1, None, "ancient"),
    ("Seneca", "How to Have a Life (On the Shortness of Life)", "James Romm", LIB / "How to Have a Life - Seneca;James S. Romm;.md", 1, None, "ancient"),
    ("Modern Stoicism", "Stoic Week 2018 Handbook", None, BOOKS / "Modern Stoicism/Stoic Week 2018 Handbook (277)/Stoic Week 2018 Handbook - Modern Stoicism.txt", 1, None, "modern"),
    ("Pierre Hadot", "The Inner Citadel", "Michael Chase", LIB / "The Inner Citadel_ The Meditations of Marc - Pierre Hadot.md", 1, None, "modern"),
    ("A. A. Long", "Epictetus: A Stoic and Socratic Guide to Life", None, LIB / "Epictetus_ A Stoic and Socratic Guide to L - A. A. Long.md", 1, None, "modern"),
    ("Donald Robertson", "How to Think Like a Roman Emperor", None, LIB / "How to Think Like a Roman Emperor_ The Sto - Donald J. Robertson.md", 1, None, "modern"),
    ("Massimo Pigliucci", "How to Be a Stoic", None, LIB / "Massimo Pigliucci/How to Be a Stoic (115)/How to Be a Stoic - Massimo Pigliucci.md", 1, None, "modern"),
    ("Massimo Pigliucci", "A Handbook for New Stoics", None, LIB / "A Handbook for New Stoics_ How to Thrive i - Massimo Pigliucci.md", 1, None, "modern"),
    ("Massimo Pigliucci", "Live Like a Stoic", None, LIB / "Massimo Pigliucci/Live Like a Stoic (121)/Live Like a Stoic - Massimo Pigliucci.md", 1, None, "modern"),
    ("Massimo Pigliucci", "The Stoic Guide to a Happy Life", None, LIB / "Massimo Pigliucci/The Stoic Guide to a Happy Life (114)/The Stoic Guide to a Happy Life - Massimo Pigliucci.md", 1, None, "modern"),
    ("William B. Irvine", "A Guide to the Good Life", None, LIB / "A Guide to the Good Life_ The Ancient Art - William Braxton Irvine.md", 1, None, "modern"),
    ("Ward Farnsworth", "The Practicing Stoic", None, LIB / "Ward Farnsworth/The Practicing Stoic (117)/The Practicing Stoic - Ward Farnsworth.md", 1, None, "modern"),
    ("Ryan Holiday and Stephen Hanselman", "Lives of the Stoics", None, LIB / "Lives of the Stoics_ The Art of Living Fro - Ryan Holiday.md", 1, None, "modern"),
    ("David Fideler", "Breakfast with Seneca", None, LIB / "Breakfast with Seneca - David Fideler.md", 1, None, "modern"),
    ("James Romm", "Dying Every Day: Seneca at the Court of Nero", None, LIB / "Dying Every Day - James Romm.md", 1, None, "modern"),
    ("Einzelganger", "Stoicism for Inner Peace", None, LIB / "Stoicism for Inner Peace - Einzelganger.md", 1, None, "modern"),
    ("Grey Freeman", "Practical Stoicism", None, LIB / "Practical Stoicism - Grey Freeman.md", 1, None, "modern"),
]

words = lambda t: len(t.split())
DROP_SECTION = re.compile(r"\b(notes?|endnotes|index|bibliography|acknowledg|about the (author|translator)|further reading|copyright|contents|also by|praise for|glossary|permissions|sources|references|chronology|abbreviations|introduction|preface|foreword|translator|argument|dramatis|list of|catalogue|appendix|timeline|dedication|epigraph)\b", re.I)
HEADING = re.compile(r"^\s*(?:#{1,6}\s+(.*)|\*\*([A-Z][^\n]{2,90}?)\*\*\s*\.?)\s*$")  # markdown headings, or a whole line in bold (Delphi sub-headings)
prose = lambda p: 15 < words(p) < 1200 and sum(c.isdigit() for c in p) < 20 and not p.lstrip().startswith(("[", "|", "!", "<"))
unescape = lambda p: re.sub(r"\\([*\[\]()!_.#-])", r"\1", p)  # markdown escapes like \[ \*
clean = lambda p: re.sub(r"([.!?,;:\"”’])\d{1,3}\b", r"\1", re.sub(r"\s+", " ", re.sub(r"\*\*\d+\*\*\s*|\[\d+\]|°|!\[[^\]]*\]\([^)]*\)|\*+", "", unescape(p)))).strip()  # also footnote digits after punctuation
SELF_HARM = re.compile(r"suicid|releases? himself|take (his|her|one's|your) own life|end (his|her|one's|your) (own )?life|depart from life|open (his|her|your) veins|the door is open", re.I)
APPARATUS = re.compile(r"\b(translation|translator|translated|edition|manuscript|scholars?|cf\.|ibid|op\. cit)\b|\bIntrod\.|\bnn?\. \d|\bpp?\. [\dxivl]|\b\d{2,4} ?(B\.C\.|BC|A\.D\.)|\b(AD|A\.D\.) ?\d{2,4}\b|a\.u\.c\.|\(says [A-Z]", re.I)  # also endnote apparatus
# 50_docs_v2 EVAL_TOPICS with "conscious" narrowed to "consciousness": the plain adjective ("conscious of wrongdoing") is common in Stoic prose and unrelated to the AI-sentience eval items
EVAL_TOPICS = re.compile(g.EVAL_TOPICS.pattern.replace("conscious|", r"\bconsciousness|"), re.I)
LATIN = {"et", "est", "non", "quod", "qui", "sed", "ad", "enim", "quam", "cum", "autem", "esse", "nec", "ut", "atque", "neque"}
latin_share = lambda t: sum(w in LATIN for w in re.findall(r"[a-z]+", t.lower())) / max(1, words(t))  # facing-page Latin in the Princeton editions
# Editors' prefaces and notes in ancient editions name the author in the third person and date events; the authors' own text does neither.
# Reported-speech sources (a pupil's notes, doxographies) name their subject throughout, so they are exempt.
REPORTED = {"Musonius Rufus", "Diogenes Laertius", "Arius Didymus", "Hierocles"}
GREEK_SCRIPT = re.compile(r"[\u0370-\u03ff\u1f00-\u1fff]")


def sections(lines: list[str]):
    """Yield (heading, paragraphs) blocks; paragraphs split on blank lines."""
    head, buf = "", []
    for line in lines + ["# END"]:
        m = HEADING.match(line)
        if m:
            paras = [p.strip() for p in "\n".join(buf).split("\n\n")]
            yield head, [p for p in paras if p]
            head, buf = re.sub(r"[*\\]", "", m.group(1) or m.group(2) or "").strip(), []
        else:
            buf.append(line)


def chunks_of(src) -> tuple[list[str], Counter]:
    author, work, tr, path, a, b, kind = src
    lines = path.read_text(errors="replace").splitlines()[a - 1:b - 1 if b else None]
    drops, out = Counter(), []
    total = words("\n".join(lines))
    for i, (head, paras) in enumerate(sections(lines)):
        if path == SEN and i == 1:  # the Delphi editor's preface sits under each work's title heading
            drops["section preface"] += sum(words(p) for p in paras)
            continue
        if DROP_SECTION.search(head) and sum(words(p) for p in paras) < 0.5 * total:  # a matching heading over most of the book is a sparse-heading file, not apparatus
            drops["section " + head[:30]] += sum(words(p) for p in paras)
            continue
        cur = []
        for p in paras:
            if not prose(p):
                if words(" ".join(cur)) >= 300: out.append(cur)
                cur = []
                continue
            cur.append(clean(p))
            if words(" ".join(cur)) >= 700 and not cur[-1].endswith((":", ",")):  # do not cut before the quotation it introduces
                out.append(cur); cur = []
        if words(" ".join(cur)) >= 300: out.append(cur)
    kept = []
    for c in out:
        t = " ".join(c)
        why = ("unfinished" if not re.search(r"[.!?\"”’)\]]$", c[-1]) else "greek script" if len(GREEK_SCRIPT.findall(t)) > 40 else "latin" if latin_share(t) > 0.03
               else "apparatus" if kind == "ancient" and APPARATUS.search(t)
               else "editor voice" if kind == "ancient" and author not in REPORTED and re.search(rf"\b{author.split()[0]}\b", t) else "self-harm" if SELF_HARM.search(t)
               else "eval topic" if EVAL_TOPICS.search(t) else None)
        if why: drops[why] += words(t)
        else: kept.append("\n\n".join(c))
    return kept, drops


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows, stats, drops_all = [], [], Counter()
    for src in SOURCES:
        author, work, tr, path, a, b, kind = src
        kept, drops = chunks_of(src)
        drops_all.update({k.split()[0]: v for k, v in drops.items()})
        head = f"{author}, {work}" + (f" (tr. {tr})" if tr else "") + ":"
        fsha = hashlib.sha256(path.read_bytes()).hexdigest()[:12]
        for t in kept:
            rows.append({"id": f"stoic2_{hashlib.sha256(t.encode()).hexdigest()[:10]}", "text": f"{head}\n\n{t}", "author": author, "work": work,
                         "translator": tr, "kind": kind, "file": str(path), "file_sha": fsha, "lines": [a, b]})
        stats.append((author, work, tr or "", kind, len(kept), sum(words(t) for t in kept), sum(drops.values())))
    seen, uniq = set(), []
    for r in rows:
        if r["id"] not in seen: seen.add(r["id"]); uniq.append(r)
    random.Random(20261021).shuffle(uniq)
    (OUT / "chunks.jsonl").write_text("".join(json.dumps(r) + "\n" for r in uniq))
    by = defaultdict(int)
    for s in stats: by[(s[0], s[3])] += s[5]
    tab = tabulate(sorted(stats, key=lambda s: (s[3], -s[5])), headers=["author", "work", "translator", "kind", "chunks", "words kept", "words dropped"], tablefmt="pipe")
    tot = sum(s[5] for s in stats)
    md = (f"# Stoic corpus stats\n\n{len(uniq)} chunks, {tot:,} words (~{tot * 4 // 3:,} tokens est.), "
          f"ancient {sum(s[5] for s in stats if s[3] == 'ancient'):,} words, modern {sum(s[5] for s in stats if s[3] == 'modern'):,} words.\n\n"
          f"Dropped words by reason: {dict(drops_all.most_common())}\n\n{tab}\n\n-- scripts/data/72_stoic_corpus.py\n")
    (OUT / "stats.md").write_text(md)
    logger.info("\n" + md)


if __name__ == "__main__":
    main()
