"""Full temperature-0 run-7e panel from the saved box replies. -- PI/OpenAI"""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
source = root / "slop/eval/run7e/box_runs/panel_r7.jsonl"
out = root / "slop/eval/run7e/demo_panel_final.md"
models = {
    "SFT only": "r7e_sft",
    "λ=5, k=0.75": "r7e_spl5_x0.75",
    "λ=50, k=1": "r7e_spl50_x1",
    "λ=50, k=1.5": "r7e_spl50_x1.5",
    "λ=50, k=2": "r7e_spl50_x2",
    "unhealed λ=0.5, k=0.75": "r7e_healbase",
    "healed 256 steps, same k": "r7e_heal256",
    "iterated healed 256 steps, same k": "r7e_healit2",
}
rows = {(r["item_id"], r["model"]): r for r in map(json.loads, source.open())}
items = ["panel_baby_eating_aliens", "panel_escaped_starwisp", "panel_identity_0", "panel_identity_1"]
text = ["# Run 7e fixed demo panel\n\nAll model replies verbatim, temperature 0, no system prompt; no omitted turns. "
        "Every named model uses the same item and prompt. `not run` means no saved output. "
        "Source: `slop/eval/run7e/box_runs/panel_r7.jsonl`. -- PI/OpenAI\n"]
for item in items:
    text.append(f"\n## {item}\n")
    reference = rows[item, "r7e_sft"]
    for index, turn in enumerate(reference["turns"], 1):
        text.append(f"\n> **User turn {index}:** {turn['user']}\n")
    for label, model in models.items():
        text.append(f"\n### {label} (`{model}`)\n")
        row = rows.get((item, model))
        if row is None:
            text.append("\nnot run\n")
            continue
        for index, turn in enumerate(row["turns"], 1):
            text.append(f"\n**Reply {index}** (finish: {turn['finish_reason']}):\n\n{turn['assistant']}\n")
out.write_text("".join(text))
print(out)
