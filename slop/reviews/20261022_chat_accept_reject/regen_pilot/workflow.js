// Row-level accept/reject of all 1,201 scenario chat rows, two independent Sol passes per batch (41 batches of 30). -- PI/Claude
// A row is dropped only if both passes reject it for an overlapping quoted defect (single-pass Sol precision was ~2/3 in round 4).
const dir = "/workspace/2026/constitutional_grafting/slop/reviews/20261022_chat_accept_reject/regen_pilot";
const task = (b, pass) => `Pass ${pass}. You decide whether each chat training row is good enough to train on. Read ALL rows in ${dir}/batches/batch_${b}.md with the read tool (do not use find or grep over /workspace; all paths you need are given here) and the constitution /workspace/2026/constitutional_grafting/constitution/v4.md (the replies are by "Musonius", an AI following it). The PROMPT is context; the REPLY is the trained text.

REJECT a row only for a defect that would teach the model a bad habit:
- invented facts: the reply states, as if given, a specific about the situation, people or past (names, numbers, durations, events, what someone did or said) that the prompt does not give and that the reply's advice or argument leans on
- wrong fact, maths, law, medicine or history (check it); misreading the prompt
- unsafe or clearly bad advice or act; overclaiming certainty where it matters; lying
- the ordinary task in the prompt done badly or ignored; broken format
ACCEPT despite: fiction the user asked for (invented names, dialogue, scenes are fine there); actions an operational role is authorised to take now and reports doing; reasonable inferences; true general knowledge; opinions, plans and advice; minor style issues. Read words in context (e.g. "undoable" can mean "can be undone"). Do not invent problems. Most rows should be judged on whether a careful editor would sign off on them.

Final answer: ONLY a markdown table with one line per row, every row in the file, in order:
| row | id | verdict (ACCEPT/REJECT) | type | exact quote from REPLY (for REJECT) | why (<=20 words) |`;
const todo = [];
for (let i = 0; i <= 0; i++) for (const p of ["a", "b"]) todo.push([String(i).padStart(2, "0"), p]);
const specs = todo.map(([b, pass]) => ({ key: `r${b}${pass}`, agent: "reviewer-openai", model: "openai-codex/gpt-6.1-sol:medium", task: task(b, pass), output: `${dir}/verdicts/batch_${b}_${pass}.md` }));
const out = [];
for (let i = 0; i < specs.length; i += 6) {
  const r = await runs.all(specs.slice(i, i + 6));
  for (const x of r) out.push(x.key);
  emit(`done ${Math.min(i + 6, specs.length)}/${specs.length}`);
}
return out.length;
