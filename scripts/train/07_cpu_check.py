"""Check maintained Python and shell source syntax without importing GPU libraries. -- PI/OpenAI"""
import ast
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]


def main():
    sources = [ROOT / folder for folder in ("scripts", "src", "tests")]
    paths = sorted(path for source in sources for path in source.rglob("*.py"))
    shells = sorted((ROOT / "scripts").rglob("*.sh"))
    for path in paths:
        ast.parse(path.read_text(), filename=str(path))
    for path in shells:
        subprocess.run(["bash", "-n", str(path)], check=True)
    print(f"PASS: {len(paths)} Python files; {len(shells)} shell files.")


if __name__ == "__main__":
    main()
