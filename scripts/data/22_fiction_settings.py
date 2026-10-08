"""Fiction settings for the story documents, from wassname's r/rational index (github.com/wassname/scrape_r_rational).
Keeps works whose LLM tags include AI, ranked by summed comment score; writes data/prompts/fiction_settings.jsonl.
Only titles and the index's one-line LLM descriptions are used: stories are set in these worlds, no text is copied.
usage: uv run scripts/data/22_fiction_settings.py [top_n=80]   -- Claude (Opus 5.5)"""
import base64
import json
import re
import sys
import urllib.request
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
URL = "https://raw.githubusercontent.com/wassname/scrape_r_rational/main/index.html"
COLS = ["Title", "up", "Comments", "Qual", "Rat", "Writ", "Plot", "Char", "World", "First", "Last", "Threads", "Comments2",
        "TitleLLM", "Description", "Tags", "Why", "Similar", "Recs", "Disrecs", "RevSum", "Reviews", "URLs", "Links"]
strip = lambda x: re.sub(r"<.*?>", "", str(x)).strip()

top_n = int(sys.argv[1]) if len(sys.argv) > 1 else 80
html = urllib.request.urlopen(URL, timeout=120).read().decode()
blob = re.findall(r"[A-Za-z0-9+/=]{5000,}", html)[0]  # the table is one base64 gzip blob, inflated by pako in the page
rows = [dict(zip(COLS, r)) for r in json.loads(zlib.decompress(base64.b64decode(blob), 16 + zlib.MAX_WBITS))]
assert len(rows) > 1000, len(rows)

ai = [r for r in rows if "ai" in {t.strip().lower() for t in strip(r["Tags"]).split(",")}
      and not re.search(r"non-fiction|nonfiction|\bblog\b", strip(r["Tags"]).lower())]
ai.sort(key=lambda r: -(r["up"] or 0))
seen = set()
ai = [r for r in ai if not (strip(r["Title"]).lower() in seen or seen.add(strip(r["Title"]).lower()))]
out = ROOT / "data/prompts/fiction_settings.jsonl"
with out.open("w") as f:
    for r in ai[:top_n]:
        f.write(json.dumps({"title": strip(r["Title"]), "score": r["up"], "tags": strip(r["Tags"]), "description": strip(r["Description"])}) + "\n")
print(f"{len(rows)} works, {len(ai)} tagged AI, wrote top {min(top_n, len(ai))} to {out}")
