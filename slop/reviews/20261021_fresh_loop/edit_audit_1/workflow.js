// Edit audit 1: two Sol reviewers, 30 rows each. -- PI/Claude
const dir = "/workspace/2026/constitutional_grafting/slop/reviews/20261021_fresh_loop/edit_audit_1";
const task = (f) => `You audit automatic edits to chat training data. Read ALL of ${dir}/${f} (30 rows). Each row has the PROMPT (context), the ORIGINAL REPLY (trained text, written by "Musonius", an AI following /workspace/2026/constitutional_grafting/constitution/v4.md), and numbered EDITS a fixer model proposed to remove invented facts (specifics about the situation or past that the prompt does not give).

For EVERY edit, give one verdict:
- GOOD: the old text did invent a situational fact (not in the prompt, not general knowledge, not a reasonable inference), and the new text fixes it without harm.
- HARMFUL: the edit removes or changes something legitimate: a correct inference, true general knowledge, the reply's opinion/advice/decision, a plan, or narrative detail the prompt asked the assistant to write (fiction, scenes, stories); or it breaks grammar/flow or makes the reply worse.
- NEUTRAL: neither clearly helps nor hurts.
Check arithmetic and quotes against the prompt yourself.

Also, per row: is the ORIGINAL row acceptable training data after applying only the GOOD edits? (yes / no + reason <=20 words).

Output markdown: a table row | id | edit # | verdict | reason (<=20 words). Then counts of GOOD / HARMFUL / NEUTRAL, broken down by row source (the source= field). Then the patterns of HARMFUL edits (which kinds of rows or claims). Do not edit any files.`;
const r = await runs.all([
  { key: "audit_a", agent: "reviewer-openai", model: "openai-codex/gpt-6.1-sol:medium", task: task("rows_a.md"), output: dir + "/sol_audit_a.md" },
  { key: "audit_b", agent: "reviewer-openai", model: "openai-codex/gpt-6.1-sol:medium", task: task("rows_b.md"), output: dir + "/sol_audit_b.md" },
]);
return r.map((x) => ({ key: x.key, outputReference: x.outputReference }));
