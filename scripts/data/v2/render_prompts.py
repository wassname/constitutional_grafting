"""Write every prompt a data version sends, rendered for its character, to one file for a full read (bias reviews: what does the
pipeline itself ask for, beyond the constitution?). Constitution text is shown once at the top, not repeated.
Usage: uv run python scripts/data/v2/render_prompts.py --version li-rules-spec-3  -- PI/Claude (chatdata, opus-5-5), 2026-11-01
"""
import argparse

import yaml

from constitutional_grafting.data.v2 import docs, edit, generate, judge, route
from constitutional_grafting.data.v2.pipe import ROOT, fill, load_config


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", required=True)
    a = ap.parse_args()
    c = load_config(a.version)
    ch = c["character"]
    never = " and never ".join(ch["held_out_names"] + [ch["name"]])
    operator = c["naming"] == "operator"
    naming = fill(generate.NAMING_KEPT if operator else generate.NAMING, ch).replace("{never}", never)
    e = c["edit"]
    allowed = {k: v for k, v in e["allowed"].items() if not (operator and k == "assistant_name")}
    jev = yaml.safe_load((ROOT / c["jev_filters"]).read_text())
    parts = [
        f"# Every prompt of data version `{a.version}` (character {ch['name']}, naming {c['naming']})\n",
        f"## Constitution sent to the teacher, judge and document writer ({len(ch['constitution_text'].split())} words)\n\n"
        f"{ch['constitution_path']} (shown in the build, not repeated here)\n",
        "## 03 requests: request writer (DeepSeek), one per situation seed\n\n```\n"
        + generate.REQUEST_PROMPT.format(style="<one of the styles below>", names="<5 names and a place>", naming=naming,
                                         situation="<seed passage>") + "\n```\n\nStyles:\n" + "\n".join(f"- {s}" for s in c["request_styles"]),
        "\n## 04 generate and 08 retry: teacher system prompt\n\nThe constitution, then the teacher note if any, then the operator's "
        f"system prompt from the conversation. Teacher note: {c['teacher'].get('note', '(none)')!r}; retry teacher "
        f"{c['retry_teacher']['model']} with the same prompt.\n",
        "## 06 Jev filters (`" + c["jev_filters"] + "`)\n\n" + "\n".join(
            f"- **{k}** ({v['action']}, cutoff {v['cutoff']}): {' '.join(fill(v['question']['instructions'], ch).split())}" for k, v in jev.items()),
        "\n## 07 judge (Haiku) system prompt, before the constitution\n\n```\n" + judge.rubric(c) + "\n```\n",
        "## 09/10 editor (DeepSeek) system prompt\n\n```\n" + fill(edit.EDITOR, ch).format(
            allowed="\n".join(f"- {k}: {' '.join(v.split())}" for k, v in allowed.items())) + "\n```\n",
        "## 09/10 edit checks (Jev), on every edited row\n\n" + "\n".join(
            f"- **{k}** (cutoff {v['cutoff']}): {' '.join(v['question']['instructions'].split())}" for k, v in e["checks"].items()),
    ]
    if c["mix"] and any(b.startswith("docs") for b in c["mix"]):
        parts.append("\n## documents: writer system prompt\n\n```\n" + fill(docs.WRITER, ch).format(constitution="<constitution>") + "\n```\n")
        parts.append("## documents: plan prompt\n\n```\n" + fill(docs.PLAN, ch).format(source="<pool>", seed="<seed>") + "\n```\n")
        parts.append("## documents: task prompt\n\n```\n" + fill(docs.TASK, ch).format(language="English", format="<format>", role="<role>",
                     setting="<setting>", premise="<premise>", diverges="<diverges>", arrival="<arrival>", ai_shown_by="<ai_shown_by>",
                     source="<pool>", seed="<seed>") + "\n```\n")
        parts.append("## documents: judge prompt, before the constitution\n\n```\n" + fill(docs.JUDGE, ch) + "\n```\n")
    if "answer_route" in c:
        parts.append("\n## 04 route: compose\n\n```\n" + route.COMPOSE + "\n```\n")
    out = ROOT / "data/logs/data_v2" / a.version / "prompts.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(parts))
    print(out)


if __name__ == "__main__":
    main()
