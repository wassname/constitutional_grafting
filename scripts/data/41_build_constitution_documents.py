"""Prepare/resume source-grounded documents offline; model work stays explicitly pending. -- PI/Sol"""
from pathlib import Path

import tyro

from constitutional_grafting.data.documents import build_constitution_documents, select_document_seeds


def build(seeds: Path, name: str, recipe: Path = Path("configs/data/documents.yaml"), revisions: Path | None = None):
    if build_constitution_documents(recipe, seeds, name, revisions)["status"] != "ready":
        raise SystemExit(2)


def select(source: Path, output: Path, n: int, name: str, recipe: Path = Path("configs/data/documents.yaml"), cap_per_author: int = 50):
    select_document_seeds(source, recipe, output, n, name, cap_per_author)


if __name__ == "__main__":
    tyro.extras.subcommand_cli_from_dict({"build": build, "select": select})
