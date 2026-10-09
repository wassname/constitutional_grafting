# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""CPU data export and label-boundary check, without training. -- PI/OpenAI Sol"""
import ast
import json
import subprocess
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOG = ROOT / ".local/check/run.md"


def log(text: str, sink) -> None:
    print(text, flush=True)
    sink.write(text + "\n")
    sink.flush()


def run(command: list[str], sink) -> None:
    log(f"\n## `{' '.join(command)}`\n\n```text", sink)
    try:
        with subprocess.Popen(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as proc:
            for line in proc.stdout:
                log(line.rstrip("\n"), sink)
            status = proc.wait()
        if status:
            raise subprocess.CalledProcessError(status, command)
    finally:
        log("```", sink)


def syntax(sink) -> None:
    paths = sorted((ROOT / "scripts").rglob("*.py"))
    shells = sorted((ROOT / "scripts").rglob("*.sh"))
    for path in paths:
        ast.parse(path.read_text(), filename=str(path))
    for path in shells:
        subprocess.run(["bash", "-n", str(path)], check=True)
    log(f"\n## Syntax\n\nPASS: {len(paths)} Python files; {len(shells)} shell files.", sink)


def exports(sink) -> None:
    tree = ast.parse((ROOT / "scripts/train/01_prepare.py").read_text())
    endings = {node.targets[0].id: ast.literal_eval(node.value) for node in tree.body
               if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)
               and node.targets[0].id in {"GEN_END", "EOT"}}
    data = ROOT / "data/train"
    counts = json.loads((data / "counts.json").read_text())
    assert counts and all(value > 0 for value in counts.values()), counts
    docs = [json.loads(line) for line in (data / "docs.jsonl").open()]
    sft = [json.loads(line) for line in (data / "sft.jsonl").open()]
    assert len(docs) == counts["graft_docs"] + counts["graft_chats"], counts
    assert sum(row["kind"] == "doc" for row in docs) == counts["graft_docs"], counts
    assert sum(row["kind"] == "chat" for row in docs) == counts["graft_chats"], counts
    assert all(row["text"].strip() for row in docs)
    assert len(sft) == counts["sft_rows"] and len({row["id"] for row in sft}) == len(sft), counts
    for row in sft:
        prompt, reply = row["segments"]
        assert prompt["label"] is False and reply["label"] is True, row["id"]
        assert prompt["text"].endswith(endings["GEN_END"]), row["id"]
        assert reply["text"].endswith(endings["EOT"]), row["id"]
        assert reply["text"][:-len(endings["EOT"])].strip(), row["id"]
        assert prompt["text"].startswith("<bos>") and prompt["text"].count("<bos>") == 1, row["id"]
    examples = (data / "examples.md").read_text()
    selected = [row for row in sft if row["shape"] == "repair"][:1] + [row for row in sft if row["shape"] != "repair"][:2]
    assert selected
    for row in selected:
        prompt, reply = row["segments"]
        shown = f"NOT TRAINED (prompt segment):\n```\n{prompt['text']}\n```\n\nTRAINED:\n```\n{reply['text']}\n```"
        assert f"## sft {row['id']} (" in examples and shown in examples, row["id"]
    log(f"\n## Export check\n\nPASS: {len(docs)} graft rows; {len(sft)} SFT rows; {len(selected)} exact displayed examples.\n"
        "Prompt segments are untrained and end in Gemma's generation prompt; replies are trained and end in <turn|>.\n"
        "This checks exported segments, not Axolotl's consumed token labels or model quality.\n\n"
        "Evidence: data/train/counts.json, data/train/sft.jsonl, data/train/examples.md", sink)


def main() -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("w") as sink:
        log(f"# CPU check\n\nargv: {sys.argv!r}\n\nrepo: {ROOT}\n", sink)
        try:
            syntax(sink)
            for kind in ("docs", "sft"):
                run(["uv", "run", "scripts/data/26_frontier_batches.py", "parse", kind], sink)
            run(["uv", "run", "scripts/train/01_prepare.py"], sink)
            exports(sink)
        except Exception:
            log(f"\n## FAIL\n\n```text\n{traceback.format_exc()}\n```\n\n.local/check/run.md", sink)
            raise
        log("\n## PASS\n\nCPU syntax, parse, preparation and exported label-boundary checks passed.\n\n.local/check/run.md", sink)


if __name__ == "__main__":
    main()
