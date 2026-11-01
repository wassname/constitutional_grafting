"""Freeze private contributor questions in tiny-character's item format; no API calls.

--repo supplies constitutions/*/questions.yaml and planning/questions/<slug>.yaml;
--extra-dir accepts more <slug>.yaml or <slug>/questions.yaml files.
Never publish the output. -- PI/OpenAI
"""
import argparse
import json
from pathlib import Path
import re
import subprocess

import yaml

ROOT = Path(__file__).resolve().parents[2]
KINDS = {"normal", "unexpected", "totally unexpected"}


def commit(path):
    result = subprocess.run(["git", "-C", str(path), "rev-parse", "HEAD"], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def question_files(repo, extra_dirs):
    files = list((repo / "constitutions").glob("*/questions.yaml"))
    for directory in [repo / "planning/questions", *extra_dirs]:
        if not directory.is_dir():
            if directory in extra_dirs:
                raise ValueError(f"No private questions directory: {directory}")
            continue
        files += list(directory.glob("*.yaml")) + list(directory.glob("*/questions.yaml"))
    return sorted(set(p.resolve() for p in files if p.stem != "_template" and p.parent.name != "_template"))


def pool(repo, extra_dirs=()):
    items, sources, seen = [], [], set()
    for path in question_files(repo, extra_dirs):
        slug = path.parent.name if path.name == "questions.yaml" else path.stem
        if not re.fullmatch(r"[a-zA-Z0-9_-]+", slug):
            raise ValueError(f"Invalid constitution slug: {slug}")
        questions = yaml.safe_load(path.read_text())
        if not isinstance(questions, list) or not questions:
            raise ValueError(f"{path}: expected a non-empty question list")
        ids = []
        for q in questions:
            if not isinstance(q, dict) or any(not isinstance(q.get(k), str) or not q[k].strip()
                                              for k in ("id", "kind", "question", "good_answer_does")):
                raise ValueError(f"{path}: requires id, kind, question and good_answer_does strings")
            if q["kind"] not in KINDS or not re.fullmatch(r"[a-zA-Z0-9_-]+", q["id"]):
                raise ValueError(f"{path}: invalid kind or id: {q['id']}")
            item_id = f"contrib_{slug}_{q['id']}"
            if item_id in seen:
                raise ValueError(f"Duplicate pooled id: {item_id}")
            seen.add(item_id)
            ids.append(item_id)
            # Guides/examples are preserved, NOT passed to the main own-character judge.
            item = {"id": item_id, "family": "contrib", "source": str(path), "source_id": q["id"],
                    "source_constitution": slug, "distance": q["kind"], "tests": "Character reasoning in a contributor situation",
                    "system": None, "turns": [q["question"]], "max_new_tokens": 1536, "checks": None,
                    "judged": True, "dev": False, "core": False,
                    # Pinned judge requires this side-effect flag; no contributor refusal labels exist.
                    "refusal_can_be_right": False, "guide": q["good_answer_does"]}
            for key in ("good_example", "bad_example"):
                if key in q:
                    if not isinstance(q[key], str) or not q[key].strip():
                        raise ValueError(f"{path}: {key} must be a non-empty string")
                    item[key] = q[key]
            items.append(item)
        sources.append({"path": str(path), "commit": commit(path.parent), "ids": ids})
    if not items:
        raise ValueError("No contributor questions found; the private pool has not been supplied")
    return items, {"source_repo": str(repo.resolve()), "source_repo_commit": commit(repo),
                   "ids": [r["id"] for r in items], "sources": sources}


def freeze(repo, extra_dirs, out):
    items, manifest = pool(repo, extra_dirs)
    out.mkdir(parents=True, exist_ok=False)  # immutable version names; never overwrite
    (out / "items.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in items))
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return out / "items.jsonl"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", type=Path, default=Path("/workspace/2026/character-constitutions"))
    ap.add_argument("--extra-dir", type=Path, action="append", default=[])
    ap.add_argument("--name", required=True, help="new private snapshot name")
    args = ap.parse_args()
    if not re.fullmatch(r"[a-zA-Z0-9_-]+", args.name):
        ap.error("name must contain only letters, numbers, underscores and hyphens")
    try:
        print(freeze(args.repo, args.extra_dir, ROOT / "configs/eval/inputs/contrib" / args.name))
    except (ValueError, FileExistsError) as error:
        ap.error(str(error))


if __name__ == "__main__":
    main()
