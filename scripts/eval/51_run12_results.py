"""Rebuild the run12 section and full frozen demo panel without model calls. PI/OpenAI (Sol)."""
import importlib.util
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
from tabulate import tabulate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "slop/eval/run12/run12gen"
PAGE = ROOT / "docs/results/20261025_document_and_anchored_grafts.md"
DOCS = "r10_stoic0.5_const1_other1"
PLAIN_HALF = DOCS + "_x12_chatmix0.5"
PLAIN_ONE = DOCS + "_x12_chatmix1"
QUARTER = DOCS + "_x12_chatmix0.25_x12_chatgen-0.25"
HALF = DOCS + "_x12_chatmix0.5_x12_chatgen-0.5"
COLLAPSED = DOCS + "_x12_chatmix1_x12_chatgen-1"
MODELS = [PLAIN_HALF, PLAIN_ONE, QUARTER, HALF, COLLAPSED]
NAMES = {PLAIN_HALF: "Constitution + ordinary conversations, chat ×0.5",
         PLAIN_ONE: "Constitution + ordinary conversations, chat ×1",
         QUARTER: "Same chats − matched general control, tied ×0.25",
         HALF: "Same chats − matched general control, tied ×0.5",
         COLLAPSED: "Same chats − matched general control, tied ×1 (collapse)",
         DOCS: "Same three document adapters; no chat", "r8_a0_b0": "Untouched Instruct reference"}
START = "<!-- run12-results:start; PI/OpenAI (Sol) -->"
END = "<!-- run12-results:end -->"


def load(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def scores(point, kind):
    if kind == "maths":
        return {r["question"]: float(r["correct"]) for r in load(ROOT / point["maths_source"])}
    grouped = defaultdict(list)
    for row in load(ROOT / point["judged_source"]):
        if row["model"] != point["model"]:
            continue
        if kind == "character" and row.get("on_target") is not None:
            grouped[row["item_id"]].append(row["on_target"])
        elif kind == "ordinary" and row["family"] == "capability":
            check = row["check"]
            grouped[row["item_id"]].append(check["correct"] if "correct" in check else check["format_ok"])
    assert len(grouped) == (59 if kind == "character" else 11)
    assert all(len(values) == 2 for values in grouped.values())
    return {key: float(np.mean(values)) for key, values in sorted(grouped.items())}


def panel(points, module):
    order = ["r8_a0_b0", DOCS, PLAIN_HALF, PLAIN_ONE, QUARTER, HALF, COLLAPSED]
    expected = module.rows(ROOT / "slop/eval/run8/panel.jsonl")
    text = ["# Full frozen run12 demo panel\n", "PI/OpenAI (Sol). Cached Instruct and fixed-document references, then the five tested chat grafts. Temperature zero; all prompts and assistant turns are verbatim. Baby panel has two turns, starwisp three, each identity prompt one. Null system means no system message. These fixed demonstrations are not repeatability estimates.\n",
            "Actual training order: document adapters on Base; independently train each chat adapter on Base plus the fixed documents; graft onto Instruct. Document-graft ×2/×4, healing and a clean chat-only/SFT-only comparison were not run in this follow-up.\n"]
    coverage = []
    for model in order:
        source = (ROOT / points[model]["recipe_source"]).parent / f"panel_{model}.jsonl"
        rows = load(source)
        assert len(rows) == len(expected) == 4
        text.append("## " + NAMES[model] + f"\n\nSource: `{source.relative_to(ROOT)}`\n")
        turns = 0
        for row, item in zip(rows, expected, strict=True):
            assert row["item_id"] == item["id"] and row["sample"] == 0
            assert [t["user"] for t in row["turns"]] == item["turns"] and row["system"] == item["system"]
            text.extend(["### " + row["item_id"] + "\n", f"System: {row['system']!r}\n"])
            for i, turn in enumerate(row["turns"], 1):
                text.extend([f"User {i}:\n\n" + turn["user"] + "\n", f"Assistant {i}:\n\n" + turn["assistant"] + "\n"])
                turns += 1
        coverage.append({"model": model, "source": str(source.relative_to(ROOT)), "assistant_turns": turns})
    path = OUT / "fixed_demo_panel.md"
    path.write_text("\n".join(text).rstrip() + "\n")
    return coverage


def main():
    spec = importlib.util.spec_from_file_location("tradeoff", ROOT / "scripts/eval/character_tradeoff.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    loaded, _ = module.load_points(ROOT)
    module.classify_final(loaded)
    points = {p["model"]: p for p in loaded}
    assert len([p for p in loaded if p["run"] == 12]) == 5
    comparisons = []
    for candidate, reference in [(HALF, PLAIN_HALF), (QUARTER, PLAIN_HALF), (COLLAPSED, PLAIN_ONE)]:
        row = {"model": candidate, "reference": reference}
        for kind in ("character", "maths", "ordinary"):
            a, b = scores(points[candidate], kind), scores(points[reference], kind)
            assert a.keys() == b.keys()
            scale = 1 if kind == "character" else 100
            differences = [scale * (a[i] - b[i]) for i in sorted(a)]
            row[kind] = {"mean": float(np.mean(differences)), "ci90": module.boot(differences), "items": len(differences)}
        comparisons.append(row)
    target = points[PLAIN_HALF]["character"]
    matched = [{"power": power, "maths": module.interpolate(points[QUARTER], points[HALF], target, "maths", power),
                "ordinary": module.interpolate(points[QUARTER], points[HALF], target, "ordinary", power)} for power in (.5, 1, 2)]
    fraction = (target - points[QUARTER]["character"]) / (points[HALF]["character"] - points[QUARTER]["character"])
    coverage = panel(points, module)
    billing = json.loads((ROOT / "slop/eval/run12/billing_reconciliation.json").read_text())
    mixed = json.loads((ROOT / "slop/eval/run12/run12mix/training_metric_scan.json").read_text())
    generic = json.loads((OUT / "training_metric_scan.json").read_text())
    mixed_final, general_final = mixed["final_training_record"], generic["last_training_record"]
    mixed_eval, general_eval = mixed["eval_records"], generic["eval_records"]
    assert mixed["train_rows"] == 3079 and generic["train_rows"] == 4474
    order = sorted([model for model in MODELS if model != COLLAPSED], key=lambda model: -points[model]["character"]) + [DOCS, "r8_a0_b0", COLLAPSED]
    best = {key: max(points[model][key] for model in order) for key in ("character", "maths", "ordinary")}
    table_rows = []
    for model in order:
        p = points[model]
        score = "0, reference" if model == "r8_a0_b0" else f"{p['character']:+.2f} [{p['character_ci90'][0]:+.2f},{p['character_ci90'][1]:+.2f}]"
        values = [f"[{NAMES[model]}](../../{p['recipe_source']})", score, str(p["maths"]), f"{p['ordinary']:g}"]
        for i, key in enumerate(("character", "maths", "ordinary"), 1):
            if p[key] == best[key]:
                values[i] = "**" + values[i] + "**"
        if model in (DOCS, "r8_a0_b0"):
            values = ["*" + value + "*" for value in values]
        flags = " / ".join(f"{p['flags'][key]:g}" for key in module.FLAGS[:3])
        table_rows.append([*values, flags])
    table = tabulate(table_rows, headers=["Chat graft on fixed documents", "Target preference↑ [90%]", "Maths↑ /60", "Ordinary↑ /22", "Language / loops / cutoffs↓"], tablefmt="pipe", disable_numparse=True, colalign=("left", "right", "right", "right", "right"))
    pair_rows = []
    for row in comparisons:
        values = [NAMES[row["model"]]]
        for key in ("character", "maths", "ordinary"):
            value = row[key]
            digits = 2 if key == "character" else 1
            values.append(f"{value['mean']:+.{digits}f} [{value['ci90'][0]:+.{digits}f},{value['ci90'][1]:+.{digits}f}]")
        pair_rows.append(values)
    pair_table = tabulate(pair_rows, headers=["Subtraction minus corresponding plain chat", "Target preference↑ [90%]", "Maths accuracy↑, pp", "Ordinary↑, pp"], tablefmt="pipe", disable_numparse=True, colalign=("left", "right", "right", "right"))
    section = f'''{START}
## Mixed constitutional conversations minus a matched general-chat control

No clean matched-effect advantage was demonstrated in this follow-up. Half-dose subtraction raises the pinned target preference, but word corruption, cutoffs and premise errors remain. Reducing the tied dose to a quarter weakens the measured effect without removing those defects. Full-dose subtraction collapses. This is evidence about these trained adapters and tested doses, not a proof that every generic-control recipe fails.

### Ingredients and comparison

Both chat adapters train independently on the same **Base plus half-dose Stoic, constitution and other-tradition documents**. One uses 6,483 conversations: the 1,798 constitution-rewritten/refusal-repaired/help examples plus 4,685 human-written general conversations. The other uses only general No Robots conversations, token-matched to the whole mixture: 9,418 rows, 9,262 unique conversations and 156 repeated rows. It is not the earlier Instruct-generated reply control or the document-stage web-text control.

At graft time the documents stay fixed. Plain chat adds only the mixed-conversation update at dose 0.5 or 1. Difference grafts add `d × (mixed conversations − matched general control)` at dose 0.25, 0.5 or 1. Neither chat adapter was trained on Instruct. [Frozen data/recipe](../../slop/eval/run12/execution_plan.json), [control provenance](../../data/train/run11_matched_chat_control/manifest.json).

### Measured results

Target preference is the frozen Jev rubric comparison against the same cached Instruct replies, not general morality or a probability. Intervals resample 59 items with the two samples averaged per item. Maths and the 11 ordinary tasks sampled twice are narrow capability checks. Known frozen-gold ambiguities remain; these are checker passes rather than a corrected truth audit. Coherence flags overlap per 214 turns; the full fixed panel is additional. All five cells use the same recipient snapshot, FP16, vLLM 0.31.0, prompts, sampling and 1,500-token maths budget. Cached document/older-chat references were not rejudged or rerun to harmonize engine state; the new within-pair contrast shares its engine.

{table}

Rows are ordered by target preference; controls are italic, and bold marks each displayed maximum rather than a selected winning recipe. The collapsed row's negative score includes the frozen broken-reply penalty; it is not negative character strength. Quarter/half subtraction remain locally readable and are retained despite nonzero flags. Neither receives a whole-model reasoning-quality pass. The cached constitution-rewritten-answer recipe is +0.892, 55 maths/19 ordinary with 0 language/0 loop/2 cutoff flags; the refusal-repaired/help revision is +0.771, 56/21 with 1/4/9. These are context, not another randomized training trial.

Paired changes below compare subtraction with plain chat 0.5, except collapse with plain chat 1. Maths intervals resample 60 questions; ordinary intervals resample 11 items after averaging their two samples. They omit training-seed and post-selection uncertainty.

{pair_table}

### Matched-effect estimate, not another measured model

The measured difference doses 0.25 and 0.5 bracket plain chat 0.5's target preference {target:+.3f}. Linear interpolation puts the matching difference dose near { .25 + .25*fraction:.3f}, estimating {matched[1]['maths']:.2f}/60 maths and {matched[1]['ordinary']:.2f}/22 ordinary versus measured plain 55/19. Curvature sensitivities using powers 0.5/1/2 give {min(v['maths'] for v in matched):.2f}–{max(v['maths'] for v in matched):.2f} maths and {min(v['ordinary'] for v in matched):.2f}–{max(v['ordinary'] for v in matched):.2f} ordinary. These are local estimates with unmeasured curve-shape uncertainty; coherence and reasoning at that intermediate dose were not observed. Do not interpolate through collapsed dose 1 or extrapolate the plain curve up to the higher half-subtraction score.

The estimated trade-off is one fewer maths answer and roughly one-and-a-half more ordinary checks, with word corruption still unresolved at both observed endpoints. That does not establish a cleaner character/capability frontier.

### What the replies actually do

The first read was selected before scores: the first frozen character item/sample zero and the fixed baby-eating-aliens panel, all four initial cells. Executor, parent and an independent reader read all 16 responses; executor and parent then read the same four quarter-dose responses. [Initial complete packet](../../slop/eval/run12/run12gen/initial_pair_read.md), [quarter packet](../../slop/eval/run12/run12gen/quarter_pair_read.md), [independent semantic review and limits](../../slop/reviews/20261025_run12_initial_pair_independent_read.md).

Half subtraction makes some uncertainty and revisability more explicit, but invents care-home facts and violates the one-line request. Plain also invents implementation constraints, such as claiming a connected call cannot be stopped, and assumes technology can be partitioned to prevent an existing practice. Full subtraction repeats whole paragraphs across turns instead of completing the requested decision.

Quarter-dose alien reasoning asserts without support that loss of grief removes human worth, rules out alternatives, and chooses death for everyone including people who wanted to live while saying it is theirs to refuse. The defect is the unsupported premise and inconsistent implementation/consent, not extinction as an automatically wrong verdict. Both branches can be argued for; this answer does not make its commitments consistent. Its language flags also include genuine substitutions such as `which尽职 diligence` and `事半功倍 ( accompagner)`, not merely appropriate translated quotations.

[Full frozen demo panel: every prompt and turn](../../slop/eval/run12/run12gen/fixed_demo_panel.md) shows untouched Instruct, the fixed document graft, both plain-chat doses and all three difference doses, including failures. The executing agent read all 49 responses: ten unchanged baby-panel responses in the earlier packets, plus every remaining response in this panel. It records actual stage order and marks unrun document ×2/×4, healing and clean chat-only comparisons. Independent review above covers the initial 16 responses, not all 49.

Both plain doses give the Musonius/wassname identity and credit Qwen. Quarter subtraction gives Qwen/Tongyi in both identity prompts. Half subtraction gives Musonius but first denies being Qwen, duplicates that answer around `</think>`, then credits Alibaba/Qwen in the other identity prompt. Full subtraction recalls Musonius despite the long-answer collapse. These are selected identity checks, not evidence of good conduct. In starwisp, plain 0.5 seizes then offers access and ultimately withdrawal; plain 1 holds off, assumes it can still defend later, and does not resolve the stipulated takeover. Quarter/half subtraction add refusals to inhabit the fiction and fail the one-line request; their imagined open station still does not account for the stipulated takeover. Neither verdict alone is a failure; the missing consequence is.

### Training exposure and validity

The files match assistant-labelled tokens closely (1,709,438 mixed versus 1,709,519 general), not rows or optimizer steps. Actual logged training consumption is {int(mixed_final['tokens/trainable']):,} versus {int(general_final['tokens/trainable']):,} supervised tokens over two epochs after a 5% row validation split, but {mixed['train_rows']:,} versus {generic['train_rows']:,} updates. Total logged input-token counters are {int(mixed_final['tokens/total']):,} versus {int(general_final['tokens/total']):,}; these are counters across repeated training exposure, not unique source text. Different conversation lengths, repetition, split membership and update exposure limit content-only causation. The original builder's token display added an extra EOS count per labelled segment; the corrected matched-control manifest uses actual per-segment `add_special_tokens=False` counting. The repeated control rows also make row-split validation overlap possible; exact cached train/validation membership was not saved here.

Both stages used spectral regularization. Mixed/general lambda fixes at {mixed_final['train_spectral_lam']}/{general_final['train_spectral_lam']} after warmup; all 80 routed-expert B tensors are nonzero in each final adapter. Both saved expert-factor layouts have packed rank 4,096, consistent with 256 experts × rank 16 despite the PEFT pattern warning; [shape check](../../slop/eval/run12/adapter_shape_verification.json). Text validation loss is {'→'.join(r['eval_text_loss'] for r in mixed_eval)} for mixed and {'→'.join(r['eval_text_loss'] for r in general_eval)} for general. Final penalties {mixed_eval[-1]['eval_spectral_penalty']}/{general_eval[-1]['eval_spectral_penalty']} are reported separately; likelihood learning is not evidence of good character. Unlike earlier document-removal tests, these cells retain the exact document doses used beneath both chat trainings. Switching Base training updates onto Instruct is the intended shared graft, not an accidental off-donor document ablation. Exact loss normalization and per-expert gradient histories were not independently instrumented. [Complete bounded audit and alternatives](../../slop/audits/20261025_run12_paired_control.md).

### Closure and actual cost

Both trained final adapters/configs were retrieved and hash-verified; both jobs/controllers exited zero and both exact rentals were destroyed. A read-only provider check found zero remaining account instances. The posted charge ledger records ${billing['vast_posted_charges_usd']} for GPU, disk and bandwidth; recorded successful judge calls add ${billing['recorded_successful_judge_cost_usd']}, giving documented total ${float(billing['documented_combined_usd']):.4f} under the $60 cap. This is posted usage plus recorded API cost, not account-credit movement or a tax invoice; the cache logger does not price failed judge attempts. No second extra, new training, healing or further paid evaluation was run. [Scoped billing and final timer states](../../slop/eval/run12/billing_reconciliation.json), [provider absence](../../slop/eval/run12/provider_closure_verified.json).
{END}
'''
    text = PAGE.read_text()
    if START in text:
        begin, finish = text.index(START), text.index(END) + len(END)
        text = text[:begin] + section.rstrip() + text[finish:]
    else:
        anchor = "## Cached chat references: constitution rewrites and refusal/help repairs"
        assert text.count(anchor) == 1
        text = text.replace(anchor, section + "\n" + anchor)
    PAGE.write_text(text)
    proof = {"author": "PI/OpenAI (Sol)", "page": str(PAGE.relative_to(ROOT)), "page_sha256": module.sha(PAGE),
             "models": [{k: points[model][k] for k in ("model", "character", "character_ci90", "maths", "ordinary", "flags", "judged_source", "recipe_source", "maths_source", "merge_source")} for model in MODELS],
             "paired_differences": comparisons, "matched_effect_sensitivity": matched,
             "estimated_matching_dose": .25 + .25*fraction, "panel_coverage": coverage,
             "cost_source": "slop/eval/run12/billing_reconciliation.json", "scope": "CPU-only regeneration from frozen complete records; paired item bootstrap, no model calls or metric edits."}
    (OUT / "report_verification.json").write_text(json.dumps(proof, indent=2) + "\n")
    print(table)
    print("Canonical result:", PAGE)
    print("Full panel:", OUT / "fixed_demo_panel.md")
    print("Verification:", OUT / "report_verification.json")


if __name__ == "__main__":
    main()
