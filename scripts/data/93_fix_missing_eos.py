"""Copy chat training files with <|im_end|> appended where the labelled answer lacks it (Axolotl input_output adds no EOS).
Originals are untouched; answer text is unchanged. Writes data/train/eos_fixed/<name>.jsonl and manifest.json.
usage: python scripts/data/93_fix_missing_eos.py data/train/run10/chatr12.jsonl [...]   -- PI/Claude (opus)"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/train/eos_fixed"
EOT = "<|im_end|>"


def fix(path: Path) -> dict:
    rows, fixed = [], 0
    for line in path.open():
        row = json.loads(line)
        last = [s for s in row["segments"] if s["label"]][-1]
        if not last["text"].rstrip().endswith(EOT):
            last["text"] = last["text"].rstrip() + EOT
            fixed += 1
        rows.append(row)
    out = OUT / path.name
    out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    return {"source": str(path.relative_to(ROOT)), "source_sha256": sha(path), "output": str(out.relative_to(ROOT)),
            "output_sha256": sha(out), "rows": len(rows), "eos_appended": fixed}


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = [fix(Path(p).resolve()) for p in sys.argv[1:]]
    (OUT / "manifest.json").write_text(json.dumps({"rule": "append <|im_end|> to the last labelled segment where missing; no other change", "files": manifest, "signature": "-- PI/Claude (opus)"}, indent=1) + "\n")
    for m in manifest:
        print(m["output"], m["rows"], "rows,", m["eos_appended"], "EOS appended")
