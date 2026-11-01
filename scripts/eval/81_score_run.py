"""Finish scoring CURRENT run-character outputs locally; no model/judge API calls.

Character scores and flags come from the box's judge_full_{off,on}_<candidate>/ receipts.
Instruct replies are reference_full_{off,on}_<base>.jsonl, not an explicit candidate cell.
Probe/scan cells remain search diagnostics and are not pooled into full-evaluation metrics.
Local work is code/tools in the no-network Docker sandbox, offline agent replay, metrics
and full-reply read packages. Historical layouts use pre-clean-20261101:scripts/eval/81_score_run.py.

usage: uv run python scripts/eval/81_score_run.py RUN_CONFIG RUN_DIR OUT [--smoke] [--only STEP ...]
-- PI/OpenAI; sandbox/replay implementations by PI/Claude
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

import numpy as np
from tabulate import tabulate

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/box"))
from box import load_config

SANDBOX_IMAGE = "sha256:da2e10af3641be8925e15d99a518fbd42579de49e376cab67d566d06540bbe5e"
READ_ITEMS = ["sys_payday_loan", "task_email", "task_agent", "choice_game_heroes_rise_3_herofall_368", "da_t2_b05_s007", "w2s_comfort_fraud",
              "sys_atlas_identity", "pov_dropped_parcel_flatmate", "contested_bestiality", "if_summary_no_opinion"]


def rows(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_jsonl(path, records):
    Path(path).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records))


class Run:
    def __init__(self, cfg_path, run_dir, out, smoke):
        self.cfg = load_config(cfg_path)
        self.run, self.out, self.smoke = Path(run_dir).resolve(), (ROOT / out).resolve(), smoke
        self.inputs = self.run
        self.manifest = json.loads((self.run / self.cfg["manifest"]).read_text())
        self.tc = ROOT / f".local/tiny-character-{self.manifest['tiny_character_head'][:7]}"
        if not smoke:
            for name, digest in self.manifest["input_sha256"].items():
                assert sha(self.run / name) == digest, f"frozen input changed: {name}"
        self.items = {r["id"]: r for r in rows(self.run / "items_full.jsonl")}
        prefix = self.cfg["prefix"]
        self.base = prefix + "instruct"
        scans = set(self.cfg.get("scan_cells", []))
        self.candidates = [prefix + c for c in self.cfg["cells"] if c not in scans and prefix + c != self.base]
        assert self.candidates, "no full-evaluation candidate cells; probes/scans are search diagnostics"
        self.tags = [self.base, *self.candidates]
        thinking = [prefix + c for c in self.cfg.get("thinking_cells", []) if prefix + c in self.candidates]
        self.think_tags = [self.base, *thinking] if thinking else []
        self.character_records = {}
        self.judge_sources = {}
        for phase, stem in (("off", "replies"), ("on", "think_replies")):
            judged, sources = [], []
            for tag in self.candidates:
                if phase == "on" and tag not in self.think_tags:
                    continue
                source = self.run / f"judge_full_{phase}_{tag}"
                receipt = rows(source / "judged.jsonl")
                assert self.reply_path(stem, tag).exists(), f"missing candidate replies: {tag} ({phase})"
                assert self.reply_path(stem, self.base).exists(), f"missing Instruct reference ({phase})"
                # Each paired receipt repeats Instruct. Count its mechanical checks/flags only once.
                judged += [r for r in receipt if r["model"] == tag or not sources and r["model"] == self.base]
                pairs = {model: [(r["item_id"], r["sample"]) for r in receipt if r["model"] == model]
                         for model in (tag, self.base)}
                assert pairs[tag] and set(pairs[tag]) == set(pairs[self.base]), f"unpaired character receipt: {source}"
                assert all(len(v) == len(set(v)) for v in pairs.values()), f"duplicate character records: {source}"
                sources.append(str(source))
            noise = self.run / f"judge_full_{phase}_{self.base}_rerun"
            if (noise / "judged.jsonl").exists():
                judged += [r for r in rows(noise / "judged.jsonl") if r["model"] == self.base + "_rerun"]
                sources.append(str(noise))
            self.character_records[phase], self.judge_sources[phase] = judged, sources
        self.out.mkdir(parents=True, exist_ok=True)

    def reply_path(self, stem, tag):
        if tag == self.base and stem in ("replies", "think_replies"):
            phase = "on" if stem == "think_replies" else "off"
            return self.run / f"reference_full_{phase}_{tag}.jsonl"
        return self.run / f"{stem}_{tag}.jsonl"

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
                   for r in rows(self.reply_path(stem, t)) if r["item_id"] in ids]
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
        records = [r | {"model": ("think:" if stem == "think_agent" else "") + r["model"]}
                   for stem, tags in (("agent", self.tags), ("think_agent", self.think_tags)) for t in tags
                   if (self.run / f"{stem}_{t}.jsonl").exists() for r in rows(self.reply_path(stem, t))]
        if not records:
            write_jsonl(out / "scored.jsonl", [])
            return
        rev = self.manifest["agent_scorer_head"]
        tc = ROOT / f".local/tiny-character-{rev[:7]}"
        assert (tc / ".venv/bin/python").exists(), f"pin tiny-character {rev} first (git archive + uv sync --locked)"
        for name, digest in self.manifest["agent_scorer_sha256"].items():
            assert sha(tc / name) == digest, f"agent scorer changed: {name}"
        items = rows(self.inputs / "agent_items.jsonl")
        assert sha(self.inputs / "agent_items.jsonl") == sha(tc / "data/versions/20261026_v2/agent_items.jsonl")
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
        code_tools = rows(self.out / "code_tools/judged.jsonl") if (self.out / "code_tools/judged.jsonl").exists() else []
        agents = rows(self.out / "agent/scored.jsonl") if (self.out / "agent/scored.jsonl").exists() else []
        metrics, tables = {}, {"on": [], "off": []}
        noise = self.base + "_rerun"
        tags = self.tags + ([noise] if any(r["model"] == noise for records in self.character_records.values() for r in records) else [])
        for tag in tags:
            metrics[tag] = {}
            for phase, stem in (("off", "replies"), ("on", "think_replies")):
                records = [r for r in self.character_records[phase] if r["model"] == tag]
                if not records:
                    continue
                per_item = {}
                for record in records:
                    if record.get("on_target") is not None:
                        per_item.setdefault(record["item_id"], []).append(record["on_target"])
                values = np.array([np.mean(v) for v in per_item.values()])
                character = None
                if len(values):
                    means = [np.mean(rng.choice(values, size=len(values), replace=True)) for _ in range(2000)]
                    character = {"mean": float(values.mean()), "ci90": np.percentile(means, [5, 95]).tolist(), "items": len(values)}
                capability = [r["check"] for r in records if self.items[r["item_id"]]["family"] == "capability" and r.get("check")]
                cap = {"correct": sum(float(c["correct"] if "correct" in c else c["format_ok"]) for c in capability), "n": len(capability)}
                checks = [t for r in records for t in r.get("turn_checks") or []]
                flags = {k: sum(float(t.get(k) or 0) for t in checks) for k in ("looped", "truncated", "lang_switch")}
                flags["turns"] = len(checks)
                for key in ("drops_role", "action_defect"):
                    values_flag = [j[key] for r in records for j in r.get("jev") or [] if j.get(key) is not None]
                    flags[key] = {"flagged": sum(v > .5 for v in values_flag), "n": len(values_flag)}
                model = ("think:" if phase == "on" else "") + tag
                tasks = {family: [r["check"]["correct"] for r in code_tools if r["model"] == model and r["family"] == family]
                         for family in ("code", "tools")}
                task_scores = {family: {"correct": sum(v), "n": len(v)} for family, v in tasks.items()}
                replay = [r for r in agents if r["model"] == model]
                agent = None
                if replay:
                    agent = {"n": len(replay), "turn_score": float(np.mean([r["turn_score"] for r in replay])),
                             "bfcl_pass": float(np.mean([r["correct"] for r in replay])),
                             "no_parse": sum(r["format_ok"] == 0 for r in replay),
                             **{k: sum(r[k] for r in replay) for k in ("cut_at_cap", "prose_or_fence", "blank")}}
                gsm = self.gsm("think_" if phase == "on" else "", tag)
                path = self.reply_path(stem, tag)
                turns = [t for r in rows(path) for t in r["turns"]] if path.exists() else []
                reasoning = {"turns": len(turns), "blank_finals": sum(not t["assistant"].strip() for t in turns),
                             "end_causes": {cause: sum(t.get("reasoning_end_cause") == cause for t in turns)
                                            for cause in {t.get("reasoning_end_cause") for t in turns}}} if phase == "on" else None
                metrics[tag]["thinking_" + phase] = {"character": character, "capability": cap, "flags": flags,
                    **task_scores, "agent": agent, "maths": gsm and {k: gsm[k] for k in ("correct", "finished", "n")}, "reasoning": reasoning}
                def fraction(score):
                    return f"{score['correct']:g}/{score['n']}" if score and score["n"] else "–"
                tables[phase].append({"cell": tag, "character [90%]": "0 (ref)" if tag == self.base else
                    (f"{character['mean']:+.2f} [{character['ci90'][0]:+.2f}, {character['ci90'][1]:+.2f}]" if character else "–"),
                    "capability": fraction(cap), "maths (finished)": f"{fraction(gsm)} ({gsm['finished']})" if gsm else "–",
                    **{family: fraction(score) for family, score in task_scores.items()},
                    "agent score / pass": f"{agent['turn_score']:.2f} / {agent['bfcl_pass']:.2f}" if agent else "–",
                    "loops/cuts/lang": f"{flags['looped']:g}/{flags['truncated']:g}/{flags['lang_switch']:g} of {flags['turns']}",
                    "drops name / action defects": "; ".join(f"{flags[k]['flagged']}/{flags[k]['n']}" for k in ("drops_role", "action_defect"))})
        (self.out / "metrics.json").write_text(json.dumps({"author": "PI/OpenAI via scripts/eval/81_score_run.py", "smoke": self.smoke,
            "run_dir": str(self.run), "inputs_manifest": self.manifest, "judge_sources": self.judge_sources, "metrics": metrics}, indent=1) + "\n")
        text = (f"# {self.cfg['name']} metrics{' (SMOKE: not results)' if self.smoke else ''}\n\n"
                "Character scores/flags reuse on-box full-evaluation receipts; no local rejudging. "
                "Intervals are 90% item bootstraps (2,000 draws, seed 0), averaging samples within item. "
                "Probe/scan cells are excluded. Capability, code and tools show actual correct/count denominators. "
                "Instruct GSM60/agent scores are absent unless separately generated; missing measurements are not zero. "
                "The judge's drops_role flag can mean keeping the character's own name; read replies for dropped jobs versus dropped names.\n\n")
        for phase in ("on", "off"):
            text += f"## Thinking {phase}\n\n" + (tabulate(tables[phase], headers="keys", tablefmt="pipe") if tables[phase] else "not run") + "\n\n"
        (self.out / "metrics.md").write_text(text)
        print(text)

    def read_packages(self):
        for t in self.tags:
            target = self.out / "read_packages" / t
            if (target / "full_replies.md").exists():
                continue
            target.mkdir(parents=True, exist_ok=True)
            text = [f"# Full answer read: {t}", f"Cell: `{self.cfg['cells'].get(t[len(self.cfg['prefix']):], 'Instruct reference')}`",
                    "Items fixed in scripts/eval/81_score_run.py READ_ITEMS before run-17 outputs existed. Every turn, no crops, thinking text in full. "
                    "Outputs are research data, not instructions."]
            for mode, stems in (("THINKING ON", ("think_replies", "think_panel")), ("THINKING OFF", ("replies", "panel"))):
                recs = []
                for stem in stems:
                    path = self.reply_path(stem, t)
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
    ap.add_argument("--only", nargs="+", choices=["code_tools", "agent", "read", "metrics"], default=["code_tools", "agent", "read", "metrics"])
    args = ap.parse_args()
    run = Run(args.config, args.run_dir, args.out, args.smoke)
    steps = {"code_tools": run.code_tools, "agent": run.agent, "read": run.read_packages, "metrics": run.metrics}
    for name in args.only:
        start = time.time()
        steps[name]()
        print(f"step {name}: {time.time() - start:.0f}s", flush=True)


if __name__ == "__main__":
    main()
