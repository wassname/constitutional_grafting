"""Tiny composable pipeline: steps chained with `>>`, each reading the previous step's rows and writing its own folder.

    data/<NN>_<step>/<version>/<batch>/rows.jsonl       rows passed on
    data/<NN>_<step>/<version>/<batch>/rejected.jsonl   rows dropped, each with {"stage", "filter", "reason"}

A step whose rows.jsonl exists is skipped (delete the folder to rerun it). Paid calls are cached separately by request hash
(model_requests.py), so rerunning a step never pays twice. -- PI/Claude (opus-5-5), 2026-10-27
"""
import json
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from ...character import load_character
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


CHARACTER_FIELDS = ("name", "maker", "about", "researcher")  # {name} etc. in any config string are filled from `character:`


def fill(obj, character: dict):
    """Fill {name}, {maker}, {about}, {researcher} in every string of a config value; other braces are left alone.
    `about` (how the name relates) is optional: "{, about}" becomes ", <about>" or nothing."""
    if isinstance(obj, str):
        obj = obj.replace("{, about}", f", {character['about']}" if character["about"] else "")
        for k in CHARACTER_FIELDS:
            obj = obj.replace("{" + k + "}", character[k])
        return obj
    if isinstance(obj, dict):
        return {k: fill(v, character) for k, v in obj.items()}
    if isinstance(obj, list):
        return [fill(v, character) for v in obj]
    return obj


def merged_config(version: str) -> dict:
    """configs/data/<version>.yaml; `inherit: <version>` merges one level, except `character` and keys listed in `replace`."""
    cfg = yaml.safe_load((ROOT / f"configs/data/{version}.yaml").read_text())
    if "inherit" in cfg:
        base, replace = merged_config(cfg.pop("inherit")), set(cfg.pop("replace", [])) | {"character"}
        cfg = {**base, **{k: ({**base[k], **v} if isinstance(v, dict) and k in base and k not in replace else v) for k, v in cfg.items()}}
    assert cfg["version"] == version, (cfg["version"], version)
    return cfg


def load_config(version: str) -> dict:
    """The merged config with the character file loaded into `character` and its fields filled into every other string."""
    cfg = merged_config(version)
    ch = cfg["character"] = {"about": ""} | load_character(cfg["character"])  # characters/<slug>/character.yaml, constitution_text rendered
    return {k: (v if k == "character" else fill(v, ch)) for k, v in cfg.items()}
