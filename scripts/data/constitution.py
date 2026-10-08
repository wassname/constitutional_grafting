"""Single source of truth for which constitution the data pipeline uses, and how it is split into sections."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / "constitution/v2.md"  # rendered from constitution/v2.md.j2 by scripts/constitution/render.py
NAME = "Musonius"


def text(name: str = NAME) -> str:
    return PATH.read_text().replace("{NAME}", name)


def sections(t: str) -> list[str]:
    """v2 sections: principles ('P3. **Spread.** ...') and derived cases ('**Honesty** (P3, P8). ...'), one paragraph each."""
    return [p.strip() for p in re.split(r"\n\s*\n", t) if re.match(r"(P\d+\. )?\*\*", p.strip()) and "): \"" not in p]


def title(section: str) -> str:
    return re.search(r"\*\*(.+?)\*\*", section).group(1).rstrip(".")
