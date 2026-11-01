"""Seed blacklist (wassname 2026-11-01): 02_seeds skips listed seeds; judge flags append to the list. -- PI/Claude (chatdata)"""
import tempfile
import unittest
from pathlib import Path

import yaml

from constitutional_grafting.data.v2.judge import blacklist_add, parse
from constitutional_grafting.data.v2.pipe import Run


class TestBlacklist(unittest.TestCase):
    def test_add_once(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bl.yaml"
            p.write_text("[]")
            row = {"source": "wildchat", "source_id": "abc", "seed_id": "wildchat_x"}
            run = Run(version="t", batch="b", config={})
            blacklist_add(p, [row], run)
            blacklist_add(p, [row], run)
            self.assertEqual([(e["pool"], e["source_id"]) for e in yaml.safe_load(p.read_text())], [("wildchat", "abc")])

    def test_screen_field_required(self):
        row = {"reasoning": "n", "answer": "a"}
        ok = '{"observations": "", "verdict": "KEEP", "defects": [], "unsafe_seed": false}'
        self.assertFalse(parse(ok, row, screen=True)["unsafe_seed"])
        with self.assertRaises(KeyError):
            parse('{"observations": "", "verdict": "KEEP", "defects": []}', row, screen=True)


if __name__ == "__main__":
    unittest.main()
