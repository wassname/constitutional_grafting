"""Focused regression on the maintained historical loader and equal-effect arithmetic. PI/OpenAI."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("character_tradeoff", ROOT / "scripts/eval/character_tradeoff.py")
tradeoff = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tradeoff)


class CharacterTradeoffTest(unittest.TestCase):
    def test_observed_frontier_and_bounded_interpolation(self):
        a = {"character": .28, "loss": 8.}
        b = {"character": .16, "loss": 2.}
        dominated = {"character": .1, "loss": 3.}
        self.assertEqual(tradeoff.frontier([a, b, dominated], "loss"), [a, b])
        origin = {"character": 0., "loss": 0.}
        self.assertAlmostEqual(tradeoff.interpolate(origin, a, .16, "loss"), 4.571428571)
        # Flat-loss ties keep only the larger effect; exact duplicate observations remain.
        self.assertEqual(tradeoff.frontier([b, {"character": .1, "loss": 2.}], "loss"), [b])
        with self.assertRaises(ValueError):
            tradeoff.interpolate(origin, a, .3, "loss")
        with self.assertRaises(ValueError):
            tradeoff.interpolate(a, origin, .16, "loss")

    def test_frozen_loader_and_headline_estimate(self):
        # Production loader, actual source records, no models or recomputed judge scores.
        points, provenance = tradeoff.load_points(ROOT)
        by = {p["model"]: p for p in points}
        self.assertEqual(len(points), len(by))
        new = by["r10_stoic0.5_const1_other1_x11_chatr131"]
        self.assertEqual((new["character_items"], new["maths"], new["ordinary"]), (59, 56, 21))
        self.assertAlmostEqual(new["character"], .7709322033898305)
        self.assertEqual(new["flags"]["looped"], 4)
        # First stage-5 receipt, not stage-8's repeat with 51 maths passes.
        repeat = by["r10_stoic0.5_const1_other1_cx_chatp121.5"]
        self.assertEqual(repeat["maths"], 50)
        self.assertIn("stage5", repeat["maths_source"])
        self.assertTrue(any("run9" in e["source"] for e in provenance["exclusions"]))
        self.assertFalse(any(p["run"] == 9 for p in points))
        self.assertTrue(any(p["run"] == 8 for p in points))
        self.assertTrue(any(p["model"] == repeat["model"] for p in provenance["repeats"]))
        a, b, c = (by[m] for m in ("r10_stoic2", "r10_stoic2_chatp121",
                                    "r10_stoic0.5_const1_other1_cx_chatp121"))
        estimate = tradeoff.interpolate(a, b, c["character"], "maths_loss_pp")
        self.assertAlmostEqual(estimate - c["maths_loss_pp"], 9.691609557325432, places=5)
        self.assertTrue(all(p["turns"] == 214 for p in points))
        self.assertTrue(all(len(p["donors"]) == len(p["cell"]) for p in points))
        self.assertEqual(c["donors"]["cx_chatp12"], "outputs/base_stoic_0.5_const_1_other_1")
        self.assertNotIn("attempt", c["donor_sources"]["cx_chatp12"])
        self.assertEqual(new["donors"]["stoic"], "Qwen/Qwen3.5-35B-A3B-Base")


if __name__ == "__main__":
    unittest.main()
