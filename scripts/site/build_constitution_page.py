# /// script
# requires-python = ">=3.11"
# dependencies = ["markdown-it-py>=3"]
# ///
"""Build the public constitution page: constitution/v4.md.j2 -> site/index.html (+ og.png, robots.txt, sitemap.xml).

The {# #} editor comments become numbered margin notes (tap the number on narrow screens); the first comment becomes the
editor's preface. Models never see these notes: scripts/data/constitution.py strips them.
usage: uv run --script scripts/site/build_constitution_page.py   -- PI/Claude (opus-5-5), 2026-10-30
"""
import html
import json
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from string import Template

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
SRC = ROOT / "constitution/v4.md.j2"
OUT = ROOT / "site"
REPO = "https://github.com/wassname/constitutional_grafting"
BASE_URL = "https://wassname.github.io/constitutional_grafting/"
TITLE = "Musonius: a virtue-ethics constitution for an AI"
DESCRIPTION = ("The constitution of Musonius, a Stoic-inspired AI: who it is, its test for virtue, how it learns what people "
               "value, and what follows, with the editors' notes.")
OG_ALT = ("Card titled 'Musonius, a constitution for an AI', quoting its virtue test: 'A drive is a virtue if, were everyone "
          "in my circles to hold it and encourage it in others, [...] almost everyone is better off and almost no one is worse off.'")

COMMENT = re.compile(r"\{#(.*?)#\}", re.S)
MARK = re.compile("\ue000(\\d+)\ue001")  # private-use chars survive markdown untouched
LINE_PREFIX = re.compile(r"^(\s*(?:>\s?|[-*+]\s|\d+\.\s))")
URL = re.compile(r"https?://[^\s)\"'<>]+[^\s)\"'<>.,;:]")
REPO_PATH = re.compile(r"(?<![\w/.~-])((?:slop|docs|scripts|src|configs|constitution|tests)/[\w./-]*\w|AGENTS\.md|README\.md|jargon\.md)(?::(\d+))?")


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True, text=True).stdout


TRACKED = set(git("ls-files").splitlines())


def extract_notes(src: str) -> tuple[str, str, list[str]]:
    """Replace every comment with a marker; a comment alone on its line attaches to the next content line."""
    preface_match = COMMENT.match(src.lstrip())
    assert preface_match, "expected the editor's preface comment at the top"
    preface = preface_match.group(1).strip()
    src = src.lstrip()[preface_match.end():]
    notes: list[str] = []

    def to_marker(m: re.Match) -> str:
        notes.append(m.group(1).strip())
        return f"\ue000{len(notes)}\ue001"

    lines, pending = [], ""
    for line in COMMENT.sub(to_marker, src).split("\n"):
        if line.strip() and not MARK.sub("", line).strip():  # marker-only line
            pending += line.strip()
            continue
        if pending and line.strip():
            if re.match(r"##? ", line) and not lines[-1].strip():  # a note before a new section closes the old one
                prev = max(i for i, l in enumerate(lines) if l.strip())
                lines[prev] += f" {pending}"
            elif line.startswith("#"):
                line = f"{line} {pending}"
            else:
                p = LINE_PREFIX.match(line)
                cut = p.end() if p else 0
                line = line[:cut] + pending + line[cut:]
            pending = ""
        lines.append(line)
    assert not pending, "comment at end of file has no text to attach to"
    body = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip() + "\n"
    return preface, body, notes


def note_html(text: str) -> str:
    """Note text verbatim, HTML-escaped; URLs and tracked repo paths become links."""
    out, pos = [], 0
    spans = sorted([(m.start(), m.end(), m.group(0), None) for m in URL.finditer(text)]
                   + [(m.start(), m.end(), m.group(1), m.group(2)) for m in REPO_PATH.finditer(text)])
    for start, end, target, line in spans:
        if start < pos:
            continue
        out.append(html.escape(text[pos:start]))
        label = html.escape(text[start:end])
        if target.startswith("http"):
            out.append(f'<a href="{html.escape(target)}" rel="nofollow">{label}</a>')
        elif target.rstrip("/") in TRACKED or any(t.startswith(target.rstrip("/") + "/") for t in TRACKED):
            kind = "blob" if target.rstrip("/") in TRACKED else "tree"
            anchor = f"#L{line}" if line else ""
            out.append(f'<a href="{REPO}/{kind}/main/{target.rstrip("/")}{anchor}">{label}</a>')
        else:
            out.append(label)
        pos = end
    out.append(html.escape(text[pos:]))
    s = "".join(out)
    s = re.sub(r"\b(FIXME|TODO|OPEN|DRAFT)\b", r'<span class="flag">\1</span>', s)
    return s.replace("\n\n", "<br><br>").replace("\n", "<br>")


def slug(text: str) -> str:
    """GitHub-style heading anchor, so links into constitution/v4.md also work here."""
    return re.sub(r"\s", "-", re.sub(r"[^\w\s-]", "", text.strip().lower()))


def render_body(body: str, notes: list[str]) -> tuple[str, list[tuple[int, str, str]]]:
    md = MarkdownIt("commonmark", {"typographer": False}).enable("table")
    tokens = md.parse(body)
    toc = []
    for i, tok in enumerate(tokens):
        if tok.type == "heading_open":
            text = MARK.sub("", tokens[i + 1].content).strip()
            tok.attrSet("id", slug(text))
            toc.append((int(tok.tag[1]), text, slug(text)))
    out = md.renderer.render(tokens, md.options, {})

    def sidenote(m: re.Match) -> str:
        n = int(m.group(1))
        return (f'<label for="sn{n}" class="sn-ref" title="Editor\'s note {n}">{n}</label>'
                f'<input type="checkbox" id="sn{n}" class="sn-toggle">'
                f'<span class="sidenote" id="note-{n}" role="note"><span class="sn-num">{n}</span> {note_html(notes[n - 1])}'
                f'<label for="sn{n}" class="sn-more" aria-hidden="true"></label></span>')

    return MARK.sub(sidenote, out), toc


def preface_html(preface: str) -> str:
    paras = [p for p in re.split(r"\n\s*\n", preface) if p.strip()]
    return "".join(f"<p>{note_html(p)}</p>" for p in paras)


def main() -> None:
    src = SRC.read_text()
    preface, body, notes = extract_notes(src)
    assert len(notes) + 1 == src.count("{#"), "lost a comment"
    article, toc = render_body(body, notes)
    article = re.sub(r"<h1[^>]*>.*?</h1>\n", "", article, count=1)  # title lives in the page header
    assert "\ue000" not in article
    modified = git("log", "-1", "--format=%cI", "--", str(SRC.relative_to(ROOT))).strip()
    commit = git("log", "-1", "--format=%h", "--", str(SRC.relative_to(ROOT))).strip()
    date_h = datetime.fromisoformat(modified).strftime("%-d %B %Y")
    toc_html = "\n".join(f'<li class="toc{lvl}"><a href="#{s}">{html.escape(t)}</a></li>' for lvl, t, s in toc if lvl == 2)
    ld = {
        "@context": "https://schema.org", "@type": "Article", "headline": TITLE, "name": "The Musonius constitution",
        "description": DESCRIPTION, "url": BASE_URL, "image": BASE_URL + "og.png", "inLanguage": "en",
        "dateModified": modified, "version": f"v4 ({commit})",
        "author": {"@type": "Person", "name": "Michael J Clark", "alternateName": "wassname", "url": "https://wassname.com"},
        "isBasedOn": f"{REPO}/blob/main/constitution/v4.md.j2",
        "about": ["virtue ethics", "Stoicism", "AI alignment", "AI character", "constitutional AI"],
    }
    page = Template((HERE / "template.html").read_text()).substitute(
        title=html.escape(TITLE), description=html.escape(DESCRIPTION), og_alt=html.escape(OG_ALT), base_url=BASE_URL,
        modified=modified, date_h=date_h, commit=commit, repo=REPO, n_notes=len(notes),
        css=(HERE / "style.css").read_text(), json_ld=json.dumps(ld, indent=1), toc=toc_html,
        preface=preface_html(preface), article=article,
        source_url=f"{REPO}/blob/main/constitution/v4.md.j2", plain_url=f"{REPO}/blob/main/constitution/v4.md",
    )
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    (OUT / "index.html").write_text(page)
    shutil.copy(HERE / "og_card.png", OUT / "og.png")
    (OUT / "favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">🏛️</text></svg>')
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}sitemap.xml\n")
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"  <url><loc>{BASE_URL}</loc><lastmod>{modified[:10]}</lastmod></url>\n</urlset>\n")
    print(f"wrote {OUT / 'index.html'}: {len(toc)} headings, {len(notes)} notes, source {commit} ({date_h})")


if __name__ == "__main__":
    main()
