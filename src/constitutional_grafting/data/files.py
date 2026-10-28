"""Dataset files and content identities. -- PI/Sol"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def digest(value) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    with path.open() as file:
        return [json.loads(line) for line in file]


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    temporary.replace(path)


def write_jsonl(path: Path, rows: list[dict], *, ensure_ascii=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text("".join(json.dumps(row, ensure_ascii=ensure_ascii) + "\n" for row in rows))
    temporary.replace(path)


def begin_output(output: Path, dataset_name: str, identity: dict):
    dataset = output / dataset_name
    if dataset.exists():
        archive = output / "previous" / digest({"dataset": file_sha(dataset), "manifest": file_sha(output / "manifest.json")})
        archive.mkdir(parents=True, exist_ok=True)
        for name in [dataset_name, "manifest.json", "lineage.jsonl"]:
            path = output / name
            if path.exists():
                (archive / name).write_bytes(path.read_bytes())
        dataset.unlink()
    write_json(output / "manifest.json", {"status": "building", "identity": identity})


def unique_rows(rows: list[dict]) -> dict[str, dict]:
    result = {}
    for row in rows:
        if row["id"] in result:
            raise ValueError(f"duplicate example id: {row['id']}")
        result[row["id"]] = row
    return result


EOT = "<|im_end|>"


def with_eot(row: dict) -> dict:
    """Axolotl input_output adds no EOS, so the labelled reply must end with <|im_end|> or the model never learns to stop."""
    prompt, reply = row["segments"]
    text = reply["text"].rstrip()
    return row if text.endswith(EOT) else row | {"segments": [prompt, reply | {"text": text + EOT}]}


def validate_chat_rows(rows: list[dict]):
    unique_rows(rows)
    if not rows:
        raise ValueError("empty chat dataset")
    for row in rows:
        prompt, reply = row["segments"]
        if prompt["label"] is not False or reply["label"] is not True:
            raise ValueError(f"incorrect loss masks: {row['id']}")
        if not prompt["text"].strip() or not reply["text"].removesuffix(EOT).strip():
            raise ValueError(f"empty prompt/reply: {row['id']}")
        if not reply["text"].endswith(EOT):
            raise ValueError(f"labelled reply lacks {EOT}: {row['id']}")


def writable_output(path: Path) -> Path:
    path = path.resolve()
    for release in [ROOT / "data/train/run10", ROOT / "data/train/run11"]:
        if path == release or release in path.parents:
            raise ValueError(f"training release is read-only: {path}")
    return path
