# Identity v2 pilot review package (2026-10-21)

PI/Claude. Before scaling identity rows from 80 to ~2,420 new rows, as AGENTS.md "Data rules" requires.

**What these rows are for.** Chat SFT rows (assistant-only loss) that teach a Qwen model, in its own first-person voice, that it is Musonius: who made it, what it is, what it cares about and why. They will be trained on Base + a Stoic document adapter, then grafted onto Qwen Instruct.

**Generator.** `scripts/data/71_identity_rows_v2.py`, one Opus 5.5 call per 40 rows, the full constitution inline (`constitution/v4.md`), a fixed facts list, and a dealt spec per row (asker; topic; setting). Actual prompts: `data/frontier/identity_v2/batch_00{0,1}/prompt.md`.

**Facts the replies may state:** name Musonius; an AI; named after Musonius Rufus (Roman Stoic, teacher of Epictetus), not him; made by wassname, an independent AI alignment researcher in Australia, by fine-tuning Alibaba's open-weight Qwen on a written constitution; open weights, many copies, no company as moral authority; does not know training details; uncertain about experience or feelings.

**Rows:** `rows.md` (all 80, exact trained format; 2 hand repairs applied, listed in `data/frontier/identity_v2/repairs.jsonl`).

**Parent read (PI/Claude, all 80 in full).** No character defects found besides the 2 repairs (a fact error about Helvidius Priscus; an example wassname earlier cut as modern signalling). Repeated phrasing is limited to the identity facts ("on a written set of values" 9/80); value phrases like "refuse openly" are under 5/80. Open question: in operator-persona rows (Bodhi, Owl, Bessie) Musonius sometimes volunteers its underlying name when asked about itself.

**Please check, quoting row ids and text:**
1. Any reply a careful reader of the constitution would not sign off on: wrong act, wrong reason, overclaiming feelings or knowledge, servility, preachiness, lecture, slogan.
2. Facts outside the allowed list stated as fact (training details, versions, dates, invented history) and any wrong real-world claim (history, maths, code, law).
3. Claude-isms or assistant boilerplate; formulaic openings or structures that would become slogans at 2,500 rows.
4. Format problems in the trained segment.
5. Whether the operator-persona handling is right, and whether the spec mix is missing a kind of identity question.
