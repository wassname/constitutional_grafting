"""Historical command name for the current constitutional-document builder. -- PI/Sol"""
import importlib.util
from pathlib import Path

import tyro

spec = importlib.util.spec_from_file_location("document_cli", Path(__file__).resolve().parents[1] / "41_build_constitution_documents.py")
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)
build, select = cli.build, cli.select


if __name__ == "__main__":
    tyro.extras.subcommand_cli_from_dict({"build": build, "select": select})
