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


    def test_stage_separation_and_evidence_based_views(self):
        points, provenance = tradeoff.load_points(ROOT)
        tradeoff.classify_final(points)
        by = {p["model"]: p for p in points}
        # Retain readable regressions and very poor control scores, not just winners.
        self.assertEqual(by["r10_stoic0.5_const1_other1_cx_chatp122"]["view_scope"], "primary")
        self.assertEqual(by["r10_stoic0.5_const1_other1_cx_chatr121_cx_chatctl-1"]["view_scope"], "auxiliary")
        self.assertEqual(by["r10_stoic2_chatgen121"]["view_scope"], "auxiliary")
        self.assertEqual(by["r10_stoic2_chat122.5"]["view_scope"], "damaged")
        self.assertEqual(by["r10_const1_cx_chatr121"]["view_scope"], "off-donor")
        documents = tradeoff.load_documents(ROOT, points, provenance)
        docs = {p["model"]: p for p in documents}
        self.assertEqual(len(documents), 25)
        anchored = docs["r10_x11_mix_const2_x11_replay_ctl-2"]
        self.assertTrue(anchored["usable"])
        self.assertAlmostEqual(anchored["abx"], 113 / 140 * 100)
        self.assertEqual((anchored["maths"], anchored["ordinary"]), (52, 22))
        self.assertNotIn("character", anchored)  # ABX must never masquerade as target quality.
        damaged = docs["r10_x11_mix_stoic2"]
        self.assertFalse(damaged["usable"])
        self.assertGreater(damaged["maths"], 53)  # Good maths cannot override the actual damaged replies.
        self.assertIn(damaged["read_source"], provenance["sources"])
        self.assertEqual(docs["r10_x11_replay_ctl1"]["dose"], 1)
        front = tradeoff.frontier([p for p in documents if p["usable"]], "ordinary_loss_pp", "abx")
        self.assertIn(anchored, front)
        unknown = dict(by["r10_stoic0.5_const1_other1_cx_chatr121"], model="new_unread_dose",
                       cell=[["stoic", .5], ["const", 1], ["other", 1], ["cx_chatr12", 3]])
        tradeoff.classify_final([unknown])
        self.assertEqual(unknown["view_scope"], "unreviewed")
        local = tradeoff.midpoint_linearity(ROOT, points)
        self.assertAlmostEqual(local["midpoint_residual"], .13362288135593223)
        self.assertGreater(local["residual_ci90"][0], 0)

    def test_experiment_names_use_actual_graft_not_training_donor(self):
        points, _ = tradeoff.load_points(ROOT)
        by = {p["model"]: p for p in points}
        for model, donor in (
            ("r10_cx_chatp121", "Base + ½Stoic + constitution + other traditions"),
            ("r10_chatp121", "Base + Stoic ×2"),
            ("r10_chat122.5", "Base + Stoic ×2"),
        ):
            p = by[model]
            name = tradeoff.experiment_name(p)
            self.assertTrue(name.startswith("Chat only:"), name)
            self.assertNotIn("Stoic docs", name)
            self.assertNotIn("Three document sets", name)
            self.assertEqual(tradeoff.chat_training_donor(p), donor)
        off_donor = by["r10_const1_cx_chatr121"]
        name = tradeoff.experiment_name(off_donor)
        self.assertIn("Constitution docs ×1", name)
        self.assertIn("Answers rewritten against constitution", name)
        self.assertNotIn("Prior chats", name)
        self.assertNotIn("Stoic docs", name)
        self.assertNotIn("Other-tradition docs", name)
        self.assertEqual(tradeoff.chat_training_donor(off_donor), "Base + ½Stoic + constitution + other traditions")
        changed_dose = by["r10_stoic1_const1_other1_cx_chatp121"]
        self.assertIn("Stoic docs ×1", tradeoff.experiment_name(changed_dose))
        self.assertNotIn("Three document sets", tradeoff.experiment_name(changed_dose))
        control_only = by["r10_stoic0.5_const1_other1_cx_chatctl1"]
        self.assertIn("Reply control ×1", tradeoff.experiment_name(control_only))
        self.assertNotIn("before chat", tradeoff.experiment_name(control_only))
        helped = by["r10_stoic0.5_const1_other1_x11_chatr131"]
        self.assertIn("Rewritten answers + refusal repairs + ordinary help", tradeoff.experiment_name(helped))


if __name__ == "__main__":
    unittest.main()
