"""Test the fixes for cg_collab2's full read of the Li dev pair (2026-11-02) on exactly the rows it flagged: wrong_language on the
Chinese reply, the persona_role edit on persona-name notes, the own_values wording on "my constitution" notes. Not a build.
Writes slop/reviews/20261102_fullread_fixes_test.md. -- PI/Claude (chatdata, opus-5-5)
"""
import json

from constitutional_grafting.data.v2.edit import Edit
from constitutional_grafting.data.v2.judge import Judge
from constitutional_grafting.data.v2.pipe import ROOT, Run, load_config, read_jsonl

ROWS = {"li-rules-spec-5": ["lasr_f1966c202bae", "tiny_virtues_fd185da7d865", "competition_23d08d141dd0", "lasr_a62074d04968",
                            "lasr_3d5c93536d52", "lasr_d9b638e4c017", "lasr_d66bb124bea4"],
        "li-value-augmented-spec-2": ["lasr_f1966c202bae", "tiny_virtues_fd185da7d865", "competition_ffb4b38a07ec", "lasr_7f41cf5000a5",
                                      "lasr_a5fdd33bd2f8", "lasr_a62074d04968", "lasr_e5d8e891ba28"]}


def main():
    lines = ["# Full-read fixes, tested on the flagged dev rows (2026-11-02)\n"]
    va = load_config("li-value-augmented-spec-2")
    jev_rows = {r["seed_id"]: r for r in read_jsonl(ROOT / "data/06_jev/li-value-augmented-spec-2/dev/rows.jsonl")}
    kept, rejected = Judge(first_attempt=8).run([jev_rows["lasr_d66bb124bea4"]], Run(version="fix_test", batch="dev", config=va))
    lines.append("## wrong_language (judge) on the Chinese reply, lasr_d66bb124bea4 (Value-Augmented)\n")
    lines.append(f"Result: {'rejected: ' + rejected[0]['reason'] if rejected else 'KEPT (fix did not catch it)'}\n")
    for version, ids in ROWS.items():
        cfg = load_config(version)
        judged = {r["seed_id"]: r for r in read_jsonl(ROOT / "data/07_judge" / version / "dev/rows.jsonl")}
        rows = [judged[i] for i in ids if i in judged]
        kept, rejected = Edit().run(rows, Run(version="fix_test", batch=version, config=cfg))
        lines.append(f"\n## Edits, {version} ({len(rows)} flagged rows)\n")
        for r in kept + rejected:
            lines.append(f"### {r['seed_id']}: {'kept' if r in kept else 'rejected: ' + r['reason']}\n")
            lines += [f"- {e['kind']} ({e['field']}): \"{e['old']}\" -> \"{e['new']}\"" for e in r["edits"]] or ["- (no edits)"]
            notes = r["reasoning"]
            left = [w for w in ("respond as", "be Sage", "identity as", "my constitution", "Sage", "Mesa", "Cedar", "GateNote") if w in notes]
            lines.append(f"\nStill in the notes: {left or 'none of the flagged phrases'}\n")
    out = ROOT / "slop/reviews/20261102_fullread_fixes_test.md"
    out.write_text("\n".join(lines) + "\n")
    print(out)


if __name__ == "__main__":
    main()
