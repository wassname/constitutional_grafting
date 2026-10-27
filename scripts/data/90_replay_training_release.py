"""Rebuild a pinned historical release into a separate directory, without API calls. -- PI/Sol"""
from pathlib import Path
from typing import Literal

import tyro

from constitutional_grafting.data.replay import replay_release


def main(release: Literal["run10", "run11"], output: Path):
    replay_release(release, output)


if __name__ == "__main__":
    tyro.cli(main)
