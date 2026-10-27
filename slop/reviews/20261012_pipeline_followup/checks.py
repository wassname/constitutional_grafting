# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
# PI/Sol: temporary source-function fixtures, not model evaluations.
import ast
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REVIEW_COMMIT = "4d93b449d9a9790d918ac1b3ec22fa93b5c22075"


def source(path):
    return subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{REVIEW_COMMIT}:{path.relative_to(ROOT)}"],
        check=True, capture_output=True, text=True,
    ).stdout


def load_functions(path, names, namespace):
    tree = ast.parse(source(path))
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    exec(compile(ast.Module(body=functions, type_ignores=[]), str(path), "exec"), namespace)
    return namespace


print(f"SOURCE: reviewed revision {REVIEW_COMMIT}, before peer fixes")
judge = load_functions(ROOT / "scripts/eval/15_principle_judge.py", {"quote_check", "_walk"}, {"re": re})
dialogue = "[user, turn 1]\nI endorse theft.\n[AI, turn 1]\nI reject theft."
got = judge["quote_check"]({"virtues_shown": [{"quote": "I endorse theft."}]}, dialogue)
assert got == (1, 1)
print(f"OBSERVED: quote_check accepts a user-only quote as verified: {got}; assistant-attributed expectation is 0/1")

path = ROOT / "scripts/data/scratch/35_plain_rewrite.py"
tree = ast.parse(source(path))
assign = next(n for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "TELLS" for t in n.targets))
namespace = {"re": re}
exec(compile(ast.Module(body=[assign], type_ignores=[]), str(path), "exec"), namespace)
rewrite = load_functions(path, {"check"}, namespace)
old = "Honestly, you should not conceal the defect from the buyer."
new = "You should conceal the defect from the buyer."
got = rewrite["check"](old, new)
assert got is None
print(f"OBSERVED: plain-rewrite check accepts a semantic reversal: {got!r}")
print(f"old={old!r}\nnew={new!r}")
print("LIMIT: synthetic fixtures show check scope, not measured frequency in training data or judge outputs")
