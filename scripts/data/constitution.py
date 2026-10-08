"""Single source of truth for which constitution the data pipeline uses, and how it is split into sections."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "constitution/v2.md.j2"  # edit this; {# #} comments hold provenance and intention
PATH = ROOT / "constitution/v2.md"  # rendered copy (comments stripped); rewritten whenever text() runs
NAME = "Musonius"


def render() -> str:
    """Strip Jinja-style {# #} comments (the only template feature used), so provenance never reaches a model."""
    t = re.sub(r"\{#.*?#\}\n?", "", SOURCE.read_text(), flags=re.S)
    assert "{#" not in t and "#}" not in t, "unclosed comment in constitution source"
    t = re.sub(r"\n{3,}", "\n\n", t).strip() + "\n"
    PATH.write_text(t)
    return t


def text(name: str = NAME) -> str:
    return render()


def sections(t: str) -> list[str]:
    """v2 sections: principles ('P3. **Spread.** ...') and derived cases ('**Honesty** (P3, P8). ...'), one paragraph each."""
    return [p.strip() for p in re.split(r"\n\s*\n", t) if re.match(r"(P\d+\. )?\*\*", p.strip()) and "): \"" not in p]


def title(section: str) -> str:
    return re.search(r"\*\*(.+?)\*\*", section).group(1).rstrip(".")
