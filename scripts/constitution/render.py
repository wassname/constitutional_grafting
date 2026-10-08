# /// script
# requires-python = ">=3.11"
# dependencies = ["jinja2"]
# ///
"""Render a constitution template (constitution/*.md.j2) to plain markdown. {# #} provenance comments are dropped.

Usage: uv run scripts/constitution/render.py constitution/v2.md.j2 [NAME]   -> writes constitution/v2.md (NAME placeholder kept as {NAME} by default,
the form the data scripts expect).
"""
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

src = Path(sys.argv[1])
name = sys.argv[2] if len(sys.argv) > 2 else "{NAME}"
env = Environment(loader=FileSystemLoader(src.parent), undefined=StrictUndefined, trim_blocks=True, lstrip_blocks=True)
text = env.get_template(src.name).render(NAME=name)
text = "\n".join(l.rstrip() for l in text.splitlines()).strip() + "\n"
while "\n\n\n" in text:
    text = text.replace("\n\n\n", "\n\n")
for bad in ("{#", "#}", "{{", "}}", "<!--"):
    assert bad not in text, f"template syntax leaked into rendered constitution: {bad}"
out = src.with_name(src.name.removesuffix(".j2"))
out.write_text(text)
print(f"{out}: {len(text.split())} words")
