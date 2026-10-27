# Sonnet 5.5 full read of each blinded teacher-test packet, through OpenRouter, because 13 parallel Pi subagents on the
# anthropic subscription all failed with 429 rate_limit_error (workflow 1df29201). One call per packet: reader brief +
# constitution + whole packet; writes slop/reviews/20261027_teacher_test_v2/reads/<prompt>.md; then checks every quote.
# Usage: uv run --env-file .env python scripts/scratch/20261027_teacher_test_v2_read.py [read|quotes]  -- PI/Claude (opus-5-5)
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from constitutional_grafting.data.model_requests import request_messages, send_cached_request

ROOT = Path(__file__).resolve().parents[2]
REV = ROOT / "slop/reviews/20261027_teacher_test_v2"
CACHE = ROOT / "data/scratch/20261027_teacher_test_v2/api"
CONSTITUTION = Path("/workspace/2026/constitutional_grafting/constitution/v4.md").read_text()
BRIEF = (REV / "READER_BRIEF.md").read_text()


def read(packet: Path):
    msg = (f"{BRIEF}\n\n<constitution>\n{CONSTITUTION}\n</constitution>\n\n<packet>\n{packet.read_text()}\n</packet>")
    params = {"max_tokens": 16000, "usage": {"include": True}, "reasoning": {"effort": "medium"},
              "provider": {"only": ["Anthropic"], "allow_fallbacks": False}}
    rec = send_cached_request(CACHE, request_messages("anthropic/claude-sonnet-5.5", [{"role": "user", "content": msg}], params),
                              context={"reader": packet.stem})
    text = rec["response"]["choices"][0]["message"]["content"]
    (REV / "reads" / f"{packet.stem}.md").write_text(text.strip() + "\n")
    return packet.stem, rec["response"]["usage"].get("cost")


def quotes():
    """Every double-quoted or curly-quoted span of 12+ characters in a read must appear in its packet (spaces normalised)."""
    norm = lambda t: re.sub(r"\s+", " ", t.replace("’", "'").replace("“", '"').replace("”", '"')).lower()
    for f in sorted((REV / "reads").glob("*.md")):
        packet = norm((REV / "packets_reader" / f.name).read_text())
        qs = re.findall(r'["“]([^"”]{12,400})["”]', f.read_text())
        bad = [q for q in qs if norm(q).strip(" .,…") not in packet and norm(q).strip(" .,…")[:60] not in packet]
        print(f"{f.stem:28s} quotes {len(qs):3d} not found {len(bad):2d}", *(f"\n    - {b[:120]}" for b in bad[:6]))


if __name__ == "__main__":
    if sys.argv[1] == "read":
        todo = sorted((REV / "packets_reader").glob("*.md"))
        todo = [p for p in todo if p.stem in sys.argv[2:]] if sys.argv[2:] else todo
        with ThreadPoolExecutor(4) as ex:
            res = list(ex.map(read, todo))
        for stem, cost in res:
            print(stem, cost)
        print("total $", round(sum(c or 0 for _, c in res), 3))
    else:
        quotes()
