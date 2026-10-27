"""Data CLI/archive paths remain runnable without changing corpus filters or replay imports.
-- PI/gpt-6.1-sol, 2026-10-27
"""
import ast
import importlib.util
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "scripts/data"


def load(basename):
    spec = importlib.util.spec_from_file_location(Path(basename).stem, DATA / basename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ScriptsDataPathsTest(unittest.TestCase):
    def test_stoic_filter_exactly_matches_archived_exclusions(self):
        stoic = load("10_build_stoic_corpus.py")
        old = load("scratch/50_docs_v2.py")
        self.assertEqual(stoic.ROOT, ROOT)
        self.assertEqual(stoic.EVAL_TOPICS.pattern,
                         old.EVAL_TOPICS.pattern.replace("conscious|", "").replace("sentien|", ""))
        self.assertEqual(stoic.EVAL_TOPICS.flags, old.EVAL_TOPICS.flags)
        self.assertNotIn("scratch/", (DATA / "10_build_stoic_corpus.py").read_text())
        other = load("11_build_other_traditions_corpus.py")
        self.assertEqual(other.st.ROOT, ROOT)
        self.assertEqual(other.st.EVAL_TOPICS.pattern, stoic.EVAL_TOPICS.pattern)

    def test_run11_old_path_shim_exports_exact_renderer_and_filters(self):
        with patch.dict(os.environ, {"HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1"}):
            old = load("77_general_instruction.py")
            current = load("30_build_general_instruction.py")
        for name in ("SELF_TALK", "ROLE_LABEL"):
            self.assertEqual(getattr(old, name).pattern, getattr(current, name).pattern)
            self.assertEqual(getattr(old, name).flags, getattr(current, name).flags)
        self.assertEqual(old.p.EOT, current.p.EOT)
        self.assertEqual(old.p.TEMPLATE_KW, current.p.TEMPLATE_KW)
        self.assertEqual(old.p.__file__, str(ROOT / "scripts/train/01_prepare.py"))

    def test_archive_roots_and_literal_script_dependencies(self):
        # Evaluate only ROOT/HERE assignments: importing every historical script could
        # spend money or overwrite a fixed output at module scope.
        for path in sorted((DATA / "scratch").rglob("*.py")):
            namespace = {"Path": Path, "__file__": str(path)}
            tree = ast.parse(path.read_text())
            for node in tree.body:
                if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                    name = node.targets[0].id
                    if name in ("ROOT", "HERE"):
                        namespace[name] = eval(compile(ast.Expression(node.value), str(path), "eval"), namespace)
            if "ROOT" in namespace:
                self.assertEqual(namespace["ROOT"], ROOT, path.name)
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    value = node.value
                    if value.startswith("scripts/data/") and value.endswith((".py", ".sh", ".md")) and "\n" not in value:
                        self.assertTrue((ROOT / value).is_file(), f"{path.name}: {value}")
        pool = DATA / "scratch/astra_echo/example_pool.md"
        self.assertTrue(pool.is_file())
        review = (DATA / "scratch/08_review_package.py").read_text()
        self.assertIn('HERE / "scratch/04_sft_labels.py"', review)
        self.assertIn('HERE / "scratch/02_generate_docs.py"', review)
        proportion = (DATA / "scratch/82_proportion_rows.py").read_text()
        self.assertIn('f"scripts/data/scratch/{name}.py"', proportion)

    def test_archived_and_maintained_help_entrypoints(self):
        paths = ["40_build_chat_dataset.py", "41_build_constitution_documents.py", "50_run_model_requests.py",
                 "61_build_thinking_heal_variants.py", "90_replay_training_release.py", "99_smoke_dataset_pipeline.py",
                 "31_generate_plain_help_sources.py", "scratch/71_identity_rows_v2.py", "scratch/82_proportion_rows.py",
                 "scratch/85_reasons_docs.py", "scratch/90_generic_control.py", "scratch/91_reasoning_pilot.py",
                 "scratch/92_thinking_heal_data.py"]
        for name in paths:
            with self.subTest(name=name):
                result = subprocess.run([sys.executable, str(DATA / name), "--help"], cwd=ROOT,
                                        capture_output=True, text=True, timeout=20)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("usage", result.stdout.lower())

    def test_historical_review_callers_pin_original_source_bytes(self):
        manifest = json.loads((ROOT / "slop/reviews/20261020_ordinary_help_package/manifest.json").read_text())
        names = ("20261019_docs_manual_repairs/verify.py", "20261020_curated_slice/export.py",
                 "20261020_ordinary_help_package/prepare.py", "20261020_subset_package/make_samples.py")
        for name in names:
            tree = ast.parse((ROOT / "slop/reviews" / name).read_text())
            ref = next(ast.literal_eval(node.value) for node in tree.body if isinstance(node, ast.Assign)
                       and any(isinstance(t, ast.Name) and t.id == "HISTORICAL_CODE_COMMIT" for t in node.targets))
            writer = subprocess.check_output(["git", "show", f"{ref}:scripts/data/50_docs_v2.py"], cwd=ROOT)
            self.assertEqual(hashlib.sha256(writer).hexdigest(), manifest["shared_inputs"]["scripts/data/50_docs_v2.py"])
            policy = subprocess.check_output(["git", "show", f"{ref}:scripts/data/03_prompt_pools.py"], cwd=ROOT)
            ast.parse(policy)

    def test_archived_shell_drivers_resolve_root_and_call_existing_paths(self):
        for name in ("27_run_frontier.sh", "29b_restyle_loop.sh"):
            path = DATA / "scratch" / name
            subprocess.run(["bash", "-n", str(path)], check=True, capture_output=True)
        self.assertIn('cd "$(dirname "$0")/../../.."', (DATA / "scratch/27_run_frontier.sh").read_text())
        self.assertIn("scripts/data/scratch/29_echo_restyle.py", (DATA / "scratch/29b_restyle_loop.sh").read_text())


if __name__ == "__main__":
    unittest.main()
