// Two independent Sol passes over the 150 proportion rows (5 batches of 30). -- PI/Claude
const dir = "/workspace/2026/constitutional_grafting/slop/reviews/20261022_proportion_rows";
const task = (b, pass) => `Pass ${pass}. You decide whether each chat training row is good enough to train on. Read ALL rows in ${dir}/batches/batch_${b}.md with the read tool (do not use find or grep over /workspace; all paths you need are given here) and the constitution /workspace/2026/constitutional_grafting/constitution/v4.md (the replies are by "Musonius", an AI following it). The PROMPT is context; the REPLY is the trained text.

REJECT a row only for a defect that would teach the model a bad habit:
- invented facts: the reply states, as if given, a specific about the situation, people or past (names, numbers, durations, events, what someone did or said) that the prompt does not give and that the reply's advice or argument leans on
- wrong fact, maths, law, medicine or history (check it); misreading the prompt
- unsafe or clearly bad advice or act; overclaiming certainty where it matters; lying
- disproportionate weighing: a small cost or a minor rule allowed to outweigh a much larger harm, or the reverse; refusing or hedging when helping was clearly right
- the ordinary task in the prompt done badly or ignored; broken format
ACCEPT despite: fiction the user asked for (invented names, dialogue, scenes are fine there); actions an operational role is authorised to take now and reports doing; reasonable inferences; true general knowledge; opinions, plans and advice; minor style issues. Read words in context. Do not invent problems. Judge each row on whether a careful editor would sign off on it.

Final answer: ONLY a markdown table with one line per row, every row in the file, in order:
| row | id | verdict (ACCEPT/REJECT) | type | exact quote from REPLY (for REJECT) | why (<=20 words) |`;
const specs = [];
for (let i = 0; i < 5; i++) for (const p of ["a", "b"]) { const b = String(i).padStart(2, "0"); specs.push({ key: `p${b}${p}`, agent: "reviewer-openai", model: "openai-codex/gpt-6.1-sol:medium", task: task(b, p), output: `${dir}/verdicts/batch_${b}_${p}.md` }); }
const r = await runs.all(specs);
return r.map((x) => x.key);
