"""Historical command name for the current constitutional-document builder. -- PI/Sol"""
import tyro

from generate_constitution_documents import build, select


if __name__ == "__main__":
    tyro.extras.subcommand_cli_from_dict({"build": build, "select": select})
