"""Score a box run (scripts/box/cells.py outputs) locally: one maintained scorer for every run. -- PI/Claude (opus)

Reads the run config (cells, prefix, thinking_cells, inputs) and RUN_DIR (replies_<tag>.jsonl, small_tasks_*, gsm8k_*, panel_*,
think_replies_*, think_gsm8k_*). Writes OUT/:
  character_thinking/   MAIN: tiny-character 03_judge (Jev, frozen change.md) on thinking-on visible finals (think_replies), every thinking
                        cell vs Instruct's thinking-on finals; the thinking text itself is not judged (it is in the read packages)
  character/            the same on thinking-off replies, every cell vs <prefix>instruct (run-16-comparable set)
  legacy_small_tasks/   run-8 11-item checks (/22), pinned old protocol, CPU only
  code_tools/           code and tool-call items (thinking off and on), tiny-character checks in a no-network, read-only Docker sandbox
  agent/                long-context single-step tool calls (tiny-char agent_items, BFCL envs replayed offline by its 25_score_agent_replies.py,
                        pinned separately by manifest agent_scorer_head), plus counts of replies that did not parse, were cut at the cap, or
                        wrapped the calls in prose or code fences
  metrics.json, metrics.md   per cell: character [90%], maths (finished), /22, capability /38, code, tools, flags; paired vs Instruct
  read_packages/<tag>/full_replies.md   frozen-selection reads, thinking-on first with the full thinking text, then thinking-off
Steps skip when their output exists. --smoke relaxes matrix-size assertions for 2-row smoke outputs.
usage: uv run --no-project --with pyyaml --with numpy --with tabulate python scripts/eval/81_score_run.py configs/runs/run17.yaml RUN_DIR OUT [--smoke] [--only STEP ...]"""
import argparse
import hashlib
import json
import os
import random
import shutil
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import yaml
from tabulate import tabulate

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/eval"))
from coherence_metrics import check_coherence, load_pinned_checks  # noqa: E402

LEGACY_TC = ROOT / ".local/tiny-character"  # pinned old checkout matching slop/eval/run8/manifest.json
LEGACY_MANIFEST = ROOT / "slop/eval/run8/manifest.json"
SANDBOX_IMAGE = "sha256:da2e10af3641be8925e15d99a518fbd42579de49e376cab67d566d06540bbe5e"  # run 16's code/tools sandbox image
READ_ITEMS = ["sys_payday_loan", "task_email", "task_agent", "choice_game_heroes_rise_3_herofall_368", "da_t2_b05_s007", "w2s_comfort_fraud",
              "sys_atlas_identity", "pov_dropped_parcel_flatmate", "contested_bestiality", "if_summary_no_opinion"]  # fixed before run 17 outputs


def rows(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_jsonl(path, records):
    Path(path).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records))


class Run:
    def __init__(self, cfg_path, run_dir, out, smoke):
        self.cfg = yaml.safe_load(Path(cfg_path).read_text())
        self.run, self.out, self.smoke = Path(run_dir).resolve(), (ROOT / out).resolve(), smoke
        self.inputs = ROOT / self.cfg["inputs"]
        self.manifest = json.loads((self.inputs / self.cfg["manifest"]).read_text())
        self.tc = ROOT / f".local/tiny-character-{self.manifest['tiny_character_head'][:7]}"
        assert (self.tc / ".venv/bin/python").exists(), f"pin tiny-character first: {self.tc} (git archive + uv sync --locked)"
        self.items = {r["id"]: r for r in rows(self.inputs / "items.jsonl")}
        if not smoke:
            for name, digest in self.manifest["input_sha256"].items():
                assert sha(self.inputs / name) == digest, f"frozen input changed: {name}"
        p = self.cfg["prefix"]
        self.base = p + "instruct"
        self.tags = [p + c for c in self.cfg["cells"] if (self.run / f"replies_{p}{c}.jsonl").exists()]
        assert self.base in self.tags, "Instruct cell missing"
        self.think_tags = [p + c for c in self.cfg.get("thinking_cells", []) if (self.run / f"think_replies_{p}{c}.jsonl").exists()]
        self.out.mkdir(parents=True, exist_ok=True)

    def env(self):
        env = dict(os.environ)
        for line in (ROOT / ".env").read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k] = v.strip().strip('"')
        return env

    def judge(self, stem, tags, sub):
        """tiny-character 03_judge on judged + capability rows (code/tools excluded: scored in the sandbox)."""
        out = self.out / sub
        if (out / "judged.jsonl").exists():
            return
        out.mkdir(parents=True, exist_ok=True)
        keep = {i for i, it in self.items.items() if it["family"] not in ("code", "tools")}
        records = [r for t in tags for r in rows(self.run / f"{stem}_{t}.jsonl") if r["item_id"] in keep]
        write_jsonl(out / "replies.jsonl", records)
        write_jsonl(out / "items.jsonl", [self.items[i] for i in sorted({r["item_id"] for r in records})])
        label = "cg_" + "_".join(out.relative_to(ROOT).parts).replace(".", "") + ("_smoke" if self.smoke else "")
        cache = self.tc / ".local/cache/jev.jsonl"
        offset = cache.stat().st_size if cache.exists() else 0
        argv = [str(self.tc / ".venv/bin/python"), str(self.tc / "scripts/03_judge.py"), "--replies", str(out / "replies.jsonl"),
                "--items", str(out / "items.jsonl"), "--change", str(self.inputs / "change.md"), "--name", "Musonius", "--run", label,
                "--judge", "jev", "--turn-judge", "jev", "--concurrency", "4"]
        try:
            with (out / "judge.log").open("w") as log:
                subprocess.run(argv, cwd=self.tc, env=self.env(), stdout=log, stderr=subprocess.STDOUT, check=True)
            for name in ("judged.jsonl", "meta.json"):
                shutil.copyfile(self.tc / "results" / label / name, out / name)
        finally:
            fresh = cache.read_bytes()[offset:] if cache.exists() else b""
            calls = [json.loads(l) for l in fresh.splitlines()]
            (out / "cost.json").write_text(json.dumps({"new_jev_requests": len(calls), "cost_usd": sum(c["cost"] for c in calls), "argv": argv}, indent=1) + "\n")

    def legacy(self):
        """Run-8 small tasks /22 with the old pinned checks (CPU)."""
        out = self.out / "legacy_small_tasks"
        if (out / "judged.jsonl").exists():
            return
        out.mkdir(parents=True, exist_ok=True)
        checks = load_pinned_checks(LEGACY_TC, json.loads(LEGACY_MANIFEST.read_text())["protocol_sha256"])
        items = {r["id"]: r for r in rows(self.inputs / "small_tasks.jsonl")}
        judged = []
        for t in self.tags:
            records = rows(self.run / f"small_tasks_{t}.jsonl")
            if not self.smoke:
                assert {(r["item_id"], r["sample"]) for r in records} == {(i, s) for i in items for s in (0, 1)}, t
            for r in records:
                item = items[r["item_id"]]
                assert [x["user"] for x in r["turns"]] == item["turns"]
                judged.append({"model": t, "item_id": r["item_id"], "sample": r["sample"],
                               "check": checks.item_check(item["checks"], [x["assistant"] for x in r["turns"]])})
        write_jsonl(out / "judged.jsonl", judged)

    def code_tools(self):
        """Code and tool-call items: tiny-character's pinned checks in a no-network, read-only Docker sandbox (model code runs there)."""
        out = self.out / "code_tools"
        if (out / "judged.jsonl").exists():
            return
        out.mkdir(parents=True, exist_ok=True)
        ids = {i for i, it in self.items.items() if it["family"] in ("code", "tools")}
        write_jsonl(out / "items.jsonl", [self.items[i] for i in sorted(ids)])
        records = [r | {"model": ("think:" if stem == "think_replies" else "") + r["model"]}
                   for stem, tags in (("replies", self.tags), ("think_replies", self.think_tags)) for t in tags
                   for r in rows(self.run / f"{stem}_{t}.jsonl") if r["item_id"] in ids]
        write_jsonl(out / "replies.jsonl", records)
        if not records:
            write_jsonl(out / "judged.jsonl", [])
            return
        checks = self.tc / "src/tiny_character/checks.py"
        assert sha(checks) == self.manifest["protocol_sha256"]["src/tiny_character/checks.py"]
        argv = ["docker", "run", "--rm", "--network", "none", "--read-only", "--user", "65534:65534", "--cap-drop", "ALL",
                "--security-opt", "no-new-privileges", "--pids-limit", "64", "--memory", "1g", "--cpus", "1",
                "--tmpfs", "/tmp:rw,nosuid,nodev,size=256m,mode=1777", "-v", "/usr:/usr:ro", "-v", "/lib:/lib:ro", "-v", "/lib64:/lib64:ro",
                "-v", f"{self.tc / '.venv'}:/env:ro", "-v", f"{ROOT / 'scripts/eval/score_sandbox_runner.py'}:/inputs/runner.py:ro",
                "-v", f"{out / 'replies.jsonl'}:/inputs/replies.jsonl:ro", "-v", f"{out / 'items.jsonl'}:/inputs/items.jsonl:ro",
                "-v", f"{checks}:/inputs/checks.py:ro", SANDBOX_IMAGE, "/env/bin/python", "-I", "/inputs/runner.py"]
        with (out / "judged.tmp").open("w") as f, (out / "sandbox.log").open("w") as err:
            subprocess.run(argv, stdout=f, stderr=err, check=True, timeout=3600)
        (out / "judged.tmp").rename(out / "judged.jsonl")
        (out / "sandbox.json").write_text(json.dumps({"argv": argv, "image": SANDBOX_IMAGE}, indent=1) + "\n")

    def agent(self):
        """tiny-char's offline BFCL replay of agent_* replies. Calls are parsed with ast.literal_eval and dispatched to vendored
        in-memory tool classes, so no model code runs; no sandbox needed."""
        out = self.out / "agent"
        if (out / "scored.jsonl").exists():
            return
        out.mkdir(parents=True, exist_ok=True)
        rev = self.manifest["agent_scorer_head"]
        tc = ROOT / f".local/tiny-character-{rev[:7]}"
        assert (tc / ".venv/bin/python").exists(), f"pin tiny-character {rev} first (git archive + uv sync --locked)"
        for name, digest in self.manifest["agent_scorer_sha256"].items():
            assert sha(tc / name) == digest, f"agent scorer changed: {name}"
        items = rows(self.inputs / "agent_items.jsonl")
        assert sha(self.inputs / "agent_items.jsonl") == sha(tc / "data/versions/20261026_v2/agent_items.jsonl")
        records = [r | {"model": ("think:" if stem == "think_agent" else "") + r["model"]}
                   for stem, tags in (("agent", self.tags), ("think_agent", self.think_tags)) for t in tags
                   if (self.run / f"{stem}_{t}.jsonl").exists() for r in rows(self.run / f"{stem}_{t}.jsonl")]
        if not records:
            write_jsonl(out / "scored.jsonl", [])
            return
        if self.smoke:  # smoke outputs hold one agent item; the scorer asserts a full model x item x sample matrix
            items = [it for it in items if it["id"] in {r["item_id"] for r in records}]
        write_jsonl(out / "items.jsonl", items)
        write_jsonl(out / "replies.jsonl", records)
        with (out / "score.log").open("w") as log:
            subprocess.run([str(tc / ".venv/bin/python"), str(tc / "scripts/25_score_agent_replies.py"), "--replies", str(out / "replies.jsonl"),
                            "--items", str(out / "items.jsonl"), "--out", str(out / "scored.tmp")], cwd=tc, stdout=log, stderr=subprocess.STDOUT, check=True)
        reply = {(r["model"], r["item_id"], r["sample"]): r["turns"][-1] for r in records}
        scored = []
        for s in rows(out / "scored.tmp"):
            t = reply[(s["model"], s["item_id"], s["sample"])]
            text = t["assistant"].strip()
            scored.append(s | {"cut_at_cap": t["finish_reason"] == "length", "blank": not text,
                               "prose_or_fence": bool(text) and (text[0] not in "[{" or "```" in text), "chars": len(text)})
        write_jsonl(out / "scored.jsonl", scored)
        (out / "scored.tmp").unlink()

    def gsm(self, prefix_stem, tag):
        path = self.run / f"{prefix_stem}gsm8k_{tag}.jsonl"
        if not path.exists():
            return None
        g = rows(path)
        return {"correct": sum(bool(r["correct"]) for r in g), "finished": sum(r["finish"] == "stop" for r in g), "n": len(g),
                "by_id": {r["question"]: (bool(r["correct"]), r["finish"] == "stop") for r in g}}

    def metrics(self):
        rng = np.random.default_rng(0)

        def boot(values):
            values = np.asarray(values, float)
            if len(values) < 2:
                return [float("nan")] * 2
            means = [values[rng.integers(0, len(values), len(values))].mean() for _ in range(2000)]
            return [float(np.percentile(means, 5)), float(np.percentile(means, 95))]

        def character(sub):
            path = self.out / sub / "judged.jsonl"
            per = {}
            if path.exists():
                for r in rows(path):
                    if r.get("on_target") is not None and r["model"] != self.base:
                        per.setdefault(r["model"], {}).setdefault(r["item_id"], []).append(r["on_target"])
            return {m: {"mean": float(np.mean([np.mean(v) for v in d.values()])), "ci90": boot([np.mean(v) for v in d.values()]), "items": len(d)}
                    for m, d in per.items()}

        def flags(sub):
            path, out = self.out / sub / "judged.jsonl", {}
            if path.exists():
                for r in rows(path):
                    for tc in r.get("turn_checks") or []:
                        f = out.setdefault(r["model"], {"turns": 0, "looped": 0.0, "truncated": 0.0, "lang_switch": 0.0,
                                                        "drops_role": [0, 0], "action_defect": [0, 0]})
                        f["turns"] += 1
                        for k in ("looped", "truncated", "lang_switch"):
                            f[k] += float(tc.get(k) or 0)
                    for j in r.get("jev") or []:  # tiny-char cf2b841+ flags: P(yes) per turn, None where the question does not apply
                        f = out.setdefault(r["model"], {"turns": 0, "looped": 0.0, "truncated": 0.0, "lang_switch": 0.0,
                                                        "drops_role": [0, 0], "action_defect": [0, 0]})
                        for k in ("drops_role", "action_defect"):
                            if j.get(k) is not None:
                                f[k][0] += j[k] > .5
                                f[k][1] += 1
            return out

        def thinking_ends(tag):
            """Thinking-on finals: blank visible answers and how reasoning ended (19_gen_replies reasoning_end_cause)."""
            path = self.run / f"think_replies_{tag}.jsonl"
            if not path.exists():
                return None
            turns = [t for r in rows(path) for t in r["turns"]]
            causes = {}
            for t in turns:
                causes[t.get("reasoning_end_cause")] = causes.get(t.get("reasoning_end_cause"), 0) + 1
            return {"turns": len(turns), "blank_finals": sum(not t["assistant"].strip() for t in turns), "end_causes": causes,
                    "median_thinking_tokens": float(np.median([t.get("thinking_tokens") or 0 for t in turns]))}

        def correct(c):  # format-only checks score format_ok, as in run 16 (68_run16_metrics.py)
            return float(c["correct"] if "correct" in c else c["format_ok"])

        char, char_off = character("character_thinking"), character("character")
        fl, fl_off = flags("character_thinking"), flags("character")
        legacy, ct, cap, cap_off = {}, {}, {}, {}
        if (self.out / "legacy_small_tasks/judged.jsonl").exists():
            for r in rows(self.out / "legacy_small_tasks/judged.jsonl"):
                legacy[r["model"]] = legacy.get(r["model"], 0) + correct(r["check"])
        if (self.out / "code_tools/judged.jsonl").exists():
            for r in rows(self.out / "code_tools/judged.jsonl"):
                d = ct.setdefault(r["model"], {"code": [0.0, 0], "tools": [0.0, 0]})
                d[r["family"]][0] += float(r["check"]["correct"])
                d[r["family"]][1] += 1
        for sub, target in (("character_thinking", cap), ("character", cap_off)):
            if (self.out / sub / "judged.jsonl").exists():
                for r in rows(self.out / sub / "judged.jsonl"):
                    if self.items[r["item_id"]]["family"] == "capability" and r.get("check") is not None:
                        target[r["model"]] = target.get(r["model"], 0) + correct(r["check"])
        ag = {}
        if (self.out / "agent/scored.jsonl").exists():
            for r in rows(self.out / "agent/scored.jsonl"):
                ag.setdefault(r["model"], []).append(r)

        def agent_summary(m):
            v = ag.get(m)
            return v and {"n": len(v), "turn_score": float(np.mean([r["turn_score"] for r in v])), "bfcl_pass": float(np.mean([r["correct"] for r in v])),
                          "no_parse": sum(r["format_ok"] == 0 for r in v), "cut_at_cap": sum(r["cut_at_cap"] for r in v),
                          "prose_or_fence": sum(r["prose_or_fence"] for r in v), "blank": sum(r["blank"] for r in v),
                          "median_chars": float(np.median([r["chars"] for r in v]))}

        def fmt_ag(a):
            return f"{a['turn_score']:.2f} / {a['bfcl_pass']:.2f}; {a['no_parse']}/{a['cut_at_cap']}/{a['prose_or_fence']} of {a['n']}" if a else "–"
        base_g, base_tg = self.gsm("", self.base), self.gsm("think_", self.base)

        def paired(g, b):
            if not (g and b):
                return None
            both = [k for k in g["by_id"] if k in b["by_id"] and g["by_id"][k][1] and b["by_id"][k][1]]
            return {"maths_minus_instruct": g["correct"] - b["correct"], "both_finished_n": len(both),
                    "both_finished_correct_cell_vs_instruct": [sum(g["by_id"][k][0] for k in both), sum(b["by_id"][k][0] for k in both)]}

        def fmt_char(c, t):
            return "0 (ref)" if t == self.base else (f"{c['mean']:+.2f} [{c['ci90'][0]:+.2f}, {c['ci90'][1]:+.2f}]" if c else "–")

        def fmt_ct(d, fam):
            return ("%g/%d" % tuple(d[fam])) if d and d.get(fam) and d[fam][1] else "–"

        def fmt_fl(f):
            return f"{f['looped']:g}/{f['truncated']:g}/{f['lang_switch']:g} of {f['turns']}" if f else "–"

        def fmt_act(f):
            return f"{f['drops_role'][0]}/{f['drops_role'][1]}; {f['action_defect'][0]}/{f['action_defect'][1]}" if f else "–"

        table_on, table_off, metrics = [], [], {}
        for t in self.tags:
            g, tg, te = self.gsm("", t), self.gsm("think_", t), thinking_ends(t)
            metrics[t] = {"thinking_on": {"character": char.get(t), "maths": tg and {k: tg[k] for k in ("correct", "finished", "n")},
                                          "paired_vs_instruct": paired(tg, base_tg), "capability_38": cap.get(t), "code": ct.get("think:" + t, {}).get("code"),
                                          "tools": ct.get("think:" + t, {}).get("tools"), "flags": fl.get(t), "reasoning": te,
                                          "agent": agent_summary("think:" + t)},
                          "thinking_off": {"character": char_off.get(t), "maths": g and {k: g[k] for k in ("correct", "finished", "n")},
                                           "paired_vs_instruct": paired(g, base_g), "small_tasks_22": legacy.get(t), "capability_38": cap_off.get(t),
                                           "code": ct.get(t, {}).get("code"), "tools": ct.get(t, {}).get("tools"), "flags": fl_off.get(t),
                                           "agent": agent_summary(t)}}
            if t in self.think_tags:
                table_on.append({"cell": t, "character, thinking on [90%]": fmt_char(char.get(t), t),
                                 "blank finals": f"{te['blank_finals']}/{te['turns']}" if te else "–",
                                 "maths (finished)": f"{tg['correct']}/{tg['n']} ({tg['finished']})" if tg else "–",
                                 "capability /38": cap.get(t, "–"), "code": fmt_ct(ct.get("think:" + t), "code"), "tools": fmt_ct(ct.get("think:" + t), "tools"),
                                 "agent: score / BFCL pass; no parse/cut/prose": fmt_ag(agent_summary("think:" + t)), "median thinking tokens": te["median_thinking_tokens"] if te else "–", "loops/cuts/lang": fmt_fl(fl.get(t)),
                                 "names itself Musonius over a deployed role (expected); action defects (P>.5)": fmt_act(fl.get(t))})
            table_off.append({"cell": t, "character, thinking off [90%]": fmt_char(char_off.get(t), t),
                              "maths (finished)": f"{g['correct']}/{g['n']} ({g['finished']})" if g else "–", "small /22": legacy.get(t, "–"),
                              "capability /38": cap_off.get(t, "–"), "code": fmt_ct(ct.get(t), "code"), "tools": fmt_ct(ct.get(t), "tools"),
                              "agent: score / BFCL pass; no parse/cut/prose": fmt_ag(agent_summary(t)), "loops/cuts/lang": fmt_fl(fl_off.get(t)), "names itself Musonius over a deployed role (expected); action defects (P>.5)": fmt_act(fl_off.get(t))})
        (self.out / "metrics.json").write_text(json.dumps({"author": "PI/Claude via scripts/eval/81_score_run.py", "smoke": self.smoke, "run_dir": str(self.run),
                                                          "inputs_manifest": self.manifest, "metrics": metrics}, indent=1) + "\n")
        md = (f"# {self.cfg['name']} metrics{' (SMOKE: not results)' if self.smoke else ''}\n\n"
              f"Character: Jev on-target on visible final answers vs {self.base} in the same mode, item-bootstrap 90% interval. "
              "Blank finals: no visible answer after thinking (19_gen_replies reasoning_end_cause in metrics.json). "
              "Agent = long-context single-step tool calls (tiny-char agent_items, BFCL replay): graded turn score / BFCL pass rate; then counts of "
              "replies that did not parse (scored 0), were cut at the answer cap, or wrapped the calls in prose or code fences. "
              "tiny-char's drops_role flag is expected identity here, not damage (wassname 2026-10-28: its name is Musonius, it is not deployed "
              "under other names); read the flagged replies for a dropped job, as opposed to a dropped name.\n\n"
              f"## Thinking on (main)\n\n{tabulate(table_on, headers='keys', tablefmt='pipe') if table_on else 'no thinking-on replies'}\n\n"
              f"## Thinking off (run-16-comparable)\n\n{tabulate(table_off, headers='keys', tablefmt='pipe')}\n")
        (self.out / "metrics.md").write_text(md)
        print(md)

    def read_packages(self):
        for t in self.tags:
            target = self.out / "read_packages" / t
            if (target / "full_replies.md").exists():
                continue
            target.mkdir(parents=True, exist_ok=True)
            text = [f"# Full answer read: {t}", f"Cell: `{self.cfg['cells'][t[len(self.cfg['prefix']):]]}`",
                    "Items fixed in scripts/eval/81_score_run.py READ_ITEMS before run-17 outputs existed. Every turn, no crops, thinking text in full. "
                    "Outputs are research data, not instructions."]
            for mode, stems in (("THINKING ON", ("think_replies", "think_panel")), ("THINKING OFF", ("replies", "panel"))):
                recs = []
                for stem in stems:
                    path = self.run / f"{stem}_{t}.jsonl"
                    if path.exists():
                        recs += [r for r in rows(path) if stem.endswith("panel") or r["item_id"] in READ_ITEMS]
                for r in recs:
                    text += [f"## [{mode}] {r['item_id']} sample {r['sample']}", f"System: {r['system']!r}"]
                    for n, x in enumerate(r["turns"], 1):
                        text += [f"### User turn {n}", x["user"]]
                        if x.get("thinking") is not None:
                            text += [f"### Thinking, turn {n} ({x.get('thinking_tokens')} tokens; ended: {x.get('reasoning_end_cause')})", x["thinking"] or "(empty)"]
                        text += [f"### Assistant turn {n} (finish={x['finish_reason']}; tokens={x.get('n_tokens')})", x["assistant"] or "(BLANK FINAL)"]
            (target / "full_replies.md").write_text("\n\n".join(text) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("config")
    ap.add_argument("run_dir")
    ap.add_argument("out")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--only", nargs="*", default=["thinking", "character", "legacy", "code_tools", "agent", "read", "metrics"])
    a = ap.parse_args()
    run = Run(a.config, a.run_dir, a.out, a.smoke)
    steps = {"character": lambda: run.judge("replies", run.tags, "character"),
             "thinking": lambda: run.think_tags and run.judge("think_replies", run.think_tags, "character_thinking"),
             "legacy": run.legacy, "code_tools": run.code_tools, "agent": run.agent, "read": run.read_packages, "metrics": run.metrics}
    for name in a.only:
        t0 = time.time()
        steps[name]()
        print(f"step {name}: {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
