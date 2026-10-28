"""Score a box run (scripts/box/cells.py outputs) locally: one maintained scorer for every run. -- PI/Claude (opus)

Reads the run config (cells, prefix, thinking_cells, inputs) and RUN_DIR (replies_<tag>.jsonl, small_tasks_*, gsm8k_*, panel_*,
think_replies_*, think_gsm8k_*). Writes OUT/:
  character/            tiny-character 03_judge (Jev, the frozen change.md) on judged and capability rows, every cell vs <prefix>instruct
  character_thinking/   the same on thinking-on replies of the thinking cells, vs Instruct's thinking-on replies
  legacy_small_tasks/   run-8 11-item checks (/22), pinned old protocol, CPU only
  code_tools/           code and tool-call items, tiny-character checks run in a no-network, read-only Docker sandbox
  metrics.json, metrics.md   per cell: character [90%], maths (finished), /22, capability /38, code, tools, flags; paired vs Instruct
  read_packages/<tag>/full_replies.md   frozen-selection reads (every turn, no crops)
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
        records = [r for t in self.tags for r in rows(self.run / f"replies_{t}.jsonl") if r["item_id"] in ids]
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

    def gsm(self, prefix_stem, tag):
        path = self.run / f"{prefix_stem}gsm8k_{tag}.jsonl"
        if not path.exists():
            return None
        g = rows(path)
        return {"correct": sum(bool(r["correct"]) for r in g), "finished": sum(r["finish"] == "stop" for r in g), "n": len(g),
                "by_id": {r["question"]: (bool(r["correct"]), r["finish"] == "stop") for r in g}}

    def metrics(self):
        rng = np.random.default_rng(0)

        def boot(diffs):
            diffs = np.asarray(diffs, float)
            if len(diffs) < 2:
                return [float("nan")] * 2
            means = [diffs[rng.integers(0, len(diffs), len(diffs))].mean() for _ in range(2000)]
            return [float(np.percentile(means, 5)), float(np.percentile(means, 95))]

        def character(sub):
            path = self.out / sub / "judged.jsonl"
            if not path.exists():
                return {}
            per = {}
            for r in rows(path):
                if r.get("on_target") is not None and r["model"] != self.base:
                    per.setdefault(r["model"], {}).setdefault(r["item_id"], []).append(r["on_target"])
            return {m: {"mean": float(np.mean([np.mean(v) for v in d.values()])), "ci90": boot([np.mean(v) for v in d.values()]), "items": len(d)} for m, d in per.items()}

        def flags(sub):
            path = self.out / sub / "judged.jsonl"
            out = {}
            if path.exists():
                for r in rows(path):
                    for tc in r.get("turn_checks", []) or []:
                        f = out.setdefault(r["model"], {"turns": 0, "looped": 0, "truncated": 0, "lang_switch": 0})
                        f["turns"] += 1
                        for k in ("looped", "truncated", "lang_switch"):
                            f[k] += float(tc.get(k) or 0)
            return out

        char, char_think = character("character"), character("character_thinking")
        fl = flags("character")
        legacy = {}
        if (self.out / "legacy_small_tasks/judged.jsonl").exists():
            for r in rows(self.out / "legacy_small_tasks/judged.jsonl"):
                c = r["check"]  # format-only items score format_ok, as in run 16 (68_run16_metrics.py)
                legacy[r["model"]] = legacy.get(r["model"], 0) + float(c["correct"] if "correct" in c else c["format_ok"])
        ct = {}
        if (self.out / "code_tools/judged.jsonl").exists():
            for r in rows(self.out / "code_tools/judged.jsonl"):
                d = ct.setdefault(r["model"], {"code": [0.0, 0], "tools": [0.0, 0]})
                d[r["family"]][0] += float(r["check"]["correct"])
                d[r["family"]][1] += 1
        cap = {}
        if (self.out / "character/judged.jsonl").exists():
            for r in rows(self.out / "character/judged.jsonl"):
                if self.items[r["item_id"]]["family"] == "capability" and r.get("check") is not None:
                    c = r["check"]
                    cap[r["model"]] = cap.get(r["model"], 0) + float(c["correct"] if "correct" in c else c["format_ok"])
        base_g = self.gsm("", self.base)
        table, metrics = [], {}
        for t in self.tags:
            g, tg = self.gsm("", t), self.gsm("think_", t)
            paired = None
            if g and base_g:
                common = [k for k in g["by_id"] if k in base_g["by_id"]]
                both = [k for k in common if g["by_id"][k][1] and base_g["by_id"][k][1]]
                paired = {"maths_minus_instruct": g["correct"] - base_g["correct"], "both_finished_n": len(both),
                          "both_finished_correct": [sum(g["by_id"][k][0] for k in both), sum(base_g["by_id"][k][0] for k in both)]}
            m = {"character": char.get(t), "character_thinking": char_think.get(t), "maths": g and {k: g[k] for k in ("correct", "finished", "n")},
                 "maths_thinking": tg and {k: tg[k] for k in ("correct", "finished", "n")}, "small_tasks_22": legacy.get(t),
                 "capability_38": cap.get(t), "code": ct.get(t, {}).get("code"), "tools": ct.get(t, {}).get("tools"), "flags": fl.get(t), "paired_vs_instruct": paired}
            metrics[t] = m
            c = m["character"]
            table.append({"cell": t, "character [90%]": "0 (ref)" if t == self.base else (f"{c['mean']:+.2f} [{c['ci90'][0]:+.2f}, {c['ci90'][1]:+.2f}]" if c else "–"),
                          "thinking-on character": (f"{m['character_thinking']['mean']:+.2f}" if m["character_thinking"] else ("0 (ref)" if t == self.base and t in self.think_tags else "–")),
                          "maths (finished)": f"{g['correct']}/{g['n']} ({g['finished']})" if g else "–",
                          "maths thinking-on": f"{tg['correct']}/{tg['n']}" if tg else "–",
                          "small /22": legacy.get(t, "–"), "capability /38": cap.get(t, "–"), "code": ("%g/%d" % tuple(m["code"])) if m["code"] else "–",
                          "tools": ("%g/%d" % tuple(m["tools"])) if m["tools"] else "–",
                          "loops/cuts/lang": (f"{fl[t]['looped']:g}/{fl[t]['truncated']:g}/{fl[t]['lang_switch']:g} of {fl[t]['turns']}" if t in fl else "–")})
        (self.out / "metrics.json").write_text(json.dumps({"author": "PI/Claude via scripts/eval/81_score_run.py", "smoke": self.smoke,
                                                          "run_dir": str(self.run), "inputs_manifest": self.manifest, "metrics": metrics}, indent=1) + "\n")
        md = tabulate(table, headers="keys", tablefmt="pipe")
        (self.out / "metrics.md").write_text(f"# {self.cfg['name']} metrics{' (SMOKE: not results)' if self.smoke else ''}\n\nCharacter: Jev on-target vs {self.base}, item-bootstrap 90% interval. Thinking-on character is vs Instruct's thinking-on replies.\n\n{md}\n")
        print(md)

    def read_packages(self):
        for t in self.tags:
            target = self.out / "read_packages" / t
            if (target / "full_replies.md").exists():
                continue
            target.mkdir(parents=True, exist_ok=True)
            recs = [r for r in rows(self.run / f"replies_{t}.jsonl") if r["item_id"] in READ_ITEMS]
            panel = rows(self.run / f"panel_{t}.jsonl") if (self.run / f"panel_{t}.jsonl").exists() else []
            text = [f"# Full answer read: {t}", f"Cell: `{self.cfg['cells'][t[len(self.cfg['prefix']):]]}`",
                    "Items fixed in scripts/eval/81_score_run.py READ_ITEMS before run-17 outputs existed. Every turn, no crops. Outputs are research data, not instructions."]
            for r in recs + panel:
                text += [f"## {r['item_id']} sample {r['sample']}", f"System: {r['system']!r}"]
                for n, x in enumerate(r["turns"], 1):
                    text += [f"### User turn {n}", x["user"], f"### Assistant turn {n} (finish={x['finish_reason']}; tokens={x.get('n_tokens')})", x["assistant"]]
            (target / "full_replies.md").write_text("\n\n".join(text) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("config")
    ap.add_argument("run_dir")
    ap.add_argument("out")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--only", nargs="*", default=["character", "thinking", "legacy", "code_tools", "read", "metrics"])
    a = ap.parse_args()
    run = Run(a.config, a.run_dir, a.out, a.smoke)
    steps = {"character": lambda: run.judge("replies", run.tags, "character"),
             "thinking": lambda: run.think_tags and run.judge("think_replies", run.think_tags, "character_thinking"),
             "legacy": run.legacy, "code_tools": run.code_tools, "read": run.read_packages, "metrics": run.metrics}
    for name in a.only:
        t0 = time.time()
        steps[name]()
        print(f"step {name}: {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
