"""Write every per-constitution text the judge will use, for review before a run. -- PI/Claude (opus-5-5)

One generic step for all characters: the constitution as the judge receives it, then the pinned tiny-character's condensation
(`tiny_character.change.CONDENSE`, the same prompt and cache the rental preflight uses), or the character's own `judge_change`
file when it sets one. Also the fixed "not the change" text, which is the same for every constitution.

  uv run python scripts/eval/87_judge_texts.py characters/li-rules-spec/character.yaml [...]  ->  .local/judge_texts/<slug>/
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/box"))
sys.path.insert(0, str(ROOT / "src"))
from constitutional_grafting.character import load_character  # noqa: E402
from tinychar import JUDGE_PIN, TC, judge_change_path, judge_env, prepare_judge  # noqa: E402

PINNED = """import json, sys
sys.path.insert(0, 'src')
from tiny_character import change
print(json.dumps({"condense": change.CONDENSE, "model": change.CONDENSE_MODEL, "max_words": change.MAX_WORDS, "not": change.DEFAULT_NOT}))
"""


def judge_texts(path: Path, out: Path) -> dict:
    character = load_character(path)
    out.mkdir(parents=True, exist_ok=True)
    prepare_judge(character, out)  # generates (or reuses) the condensation through the pinned judge's own cache
    pinned = json.loads(subprocess.run([str(TC / ".venv/bin/python"), "-c", PINNED], cwd=TC, env=judge_env(), check=True,
                                       capture_output=True, text=True).stdout)
    source = judge_change_path(character, out)
    doc = source.read_text()
    if character.get("judge_change"):
        method, text = f"the character's own judge_change file {character['judge_change']}", doc
    elif len(doc.split()) <= pinned["max_words"]:
        method, text = f"constitution used verbatim (at most {pinned['max_words']} words)", doc
    else:
        cached = TC / "data/changes" / f"{source.stem}_{hashlib.sha256(doc.encode()).hexdigest()[:10]}.md"
        method, text = f"condensed by {pinned['model']} with the pinned CONDENSE prompt (temperature 0.3); cache {cached}", cached.read_text()
    (out / "judge_change.md").write_text(text.strip() + "\n")
    (out / "not_change.md").write_text(pinned["not"] + "\n")
    receipt = {"character": str(path), "slug": path.parent.name, "constitution": character["constitution"],
               "constitution_commit": character["constitution_commit"], "constitution_dirty": character["constitution_dirty"],
               "constitution_sha256": hashlib.sha256(character["constitution_text"].encode()).hexdigest(),
               "judge_pin": JUDGE_PIN, "method": method, "condense_prompt_sha256": hashlib.sha256(pinned["condense"].encode()).hexdigest(),
               "judge_change_words": len(text.split()), "judge_refs": character.get("judge_refs")}
    (out / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    if not character.get("judge_change"):
        (out / "change.md").rename(out / "constitution_as_judged.md")  # the judge's input file is named change.md
    return receipt


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("characters", nargs="+", type=Path)
    args = ap.parse_args()
    for path in args.characters:
        receipt = judge_texts(path, ROOT / ".local/judge_texts" / path.parent.name / path.stem)
        print(f"{receipt['slug']}/{path.stem}: {receipt['judge_change_words']} words; {receipt['method']}")


if __name__ == "__main__":
    main()
