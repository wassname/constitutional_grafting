"""Build/resume a chat dataset offline; pending work is written explicitly. -- PI/Sol"""
from pathlib import Path

import tyro

from constitutional_grafting.data.chat import build_chat_dataset


def main(recipe: Path, input: Path, name: str):
    result = build_chat_dataset(recipe, input, name)
    if result["status"] != "ready":
        raise SystemExit(2)


if __name__ == "__main__":
    tyro.cli(main)
