"""Tiny composable pipeline: steps chained with `>>`, each reading the previous step's rows and writing its own folder.

    data/<NN>_<step>/<version>/<batch>/rows.jsonl       rows passed on
    data/<NN>_<step>/<version>/<batch>/rejected.jsonl   rows dropped, each with {"stage", "filter", "reason"}

A step whose rows.jsonl exists is skipped (delete the folder to rerun it). Paid calls are cached separately by request hash
(model_requests.py), so rerunning a step never pays twice. -- PI/Claude (opus-5-5), 2026-10-27
"""
import json
from dataclasses import dataclass, field
from pathlib import Path

from ..files import ROOT


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.open()]


def write_jsonl(path: Path, rows: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    tmp.replace(path)


@dataclass
class Run:
    version: str
    batch: str
    config: dict
    data: Path = ROOT / "data"


class Step:
    """Subclass and implement `run(rows, run) -> (kept, rejected)`. Rejected rows must carry a "reason"."""
    number: int = 0
    name: str = "step"

    def __rshift__(self, other: "Step") -> "Pipe":
        return Pipe([self, other])

    def folder(self, run: Run) -> Path:
        return run.data / f"{self.number:02d}_{self.name}" / run.version / run.batch

    def __call__(self, rows: list[dict], run: Run) -> list[dict]:
        out = self.folder(run)
        if (out / "rows.jsonl").exists():
            print(f"skip {self.name}: {out / 'rows.jsonl'} exists")
            return read_jsonl(out / "rows.jsonl")
        kept, rejected = self.run(rows, run)
        for r in rejected:
            if "reason" not in r:
                raise ValueError(f"{self.name}: rejected row without a reason")
            r.setdefault("stage", self.name)
        write_jsonl(out / "rejected.jsonl", rejected)
        write_jsonl(out / "rows.jsonl", kept)
        print(f"{self.name}: in {len(rows)}, kept {len(kept)}, rejected {len(rejected)} -> {out}")
        return kept

    def run(self, rows: list[dict], run: Run) -> tuple[list[dict], list[dict]]:
        raise NotImplementedError


@dataclass
class Pipe:
    steps: list = field(default_factory=list)

    def __rshift__(self, other: Step) -> "Pipe":
        return Pipe(self.steps + [other])

    def run(self, run: Run) -> list[dict]:
        rows: list[dict] = []
        for step in self.steps:
            rows = step(rows, run)
        return rows
