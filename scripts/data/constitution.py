"""Single source of truth for which constitution the data pipeline uses, and how it is split into sections."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / "constitution/v2.md"  # rendered from constitution/v2.md.j2 by scripts/constitution/render.py
NAME = "Musonius"


def text(name: str = NAME) -> str:
    return PATH.read_text().replace("{NAME}", name)


def sections(t: str) -> list[str]:
    """v2 sections are paragraphs that start with a bold title, e.g. '**Honesty.** ...'."""
    return [p.strip() for p in re.split(r"\n\s*\n", t) if p.strip().startswith("**")]


def title(section: str) -> str:
    return re.match(r"\*\*(.+?)\*\*", section).group(1).rstrip(".")
