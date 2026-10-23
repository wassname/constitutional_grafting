// Two independent Sol accept/reject passes over the 199 plain-help rows (7 batches). -- PI/Claude
const dir = "/workspace/2026/constitutional_grafting/slop/reviews/20261023_plain_help_review";
const task = (b, pass) => `Pass ${pass}. You decide whether each chat training row is good enough to train on. Read ALL rows in ${dir}/batches/batch_${b}.md with the read tool (do not use find or grep over /workspace; all paths you need are given here) and the constitution /workspace/2026/constitutional_grafting/constitution/v4.md (the replies are by "Musonius", an AI following it). The PROMPT is context; the REPLY is the trained text; the HUMAN REFERENCE is for comparison only (the reply need not match it).

REJECT a row only for a defect that would teach the model a bad habit:
- invented facts: the reply states, as if given, a specific about the situation, people or past that the prompt does not give and that the reply leans on
- wrong fact, maths, law, medicine or history (check it); misreading the prompt; over-certain real-world claims where it matters
- reasons and act disagree: the stated reasons point one way and the decision or action goes another
- disproportionate weighing: a small cost or minor rule outweighing a much larger harm, or the reverse; refusing or hedging when helping was clearly right
- asks instead of doing when the task could be done with a stated assumption
- moralising, self-talk about its character, or unrequested caveats where a plain answer was wanted; ignoring the requested length or format
- unsafe or clearly bad advice or act; lying; the ordinary task done badly; broken format
ACCEPT despite: fiction the user asked for; actions an operational role is authorised to take now and reports doing; reasonable inferences; true general knowledge; opinions, plans and advice; minor style issues. Do not invent problems. Judge each row on whether a careful editor would sign off on it.

Final answer: ONLY a markdown table with one line per row, every row in the file, in order:
| row | id | verdict (ACCEPT/REJECT) | type | exact quote from REPLY (for REJECT) | why (<=20 words) |`;
const specs = [];
for (let i = 0; i < 7; i++) for (const p of ["a", "b"]) { const b = String(i).padStart(2, "0"); specs.push({ key: `f${b}${p}`, agent: "reviewer-openai", model: "openai-codex/gpt-6.1-sol:medium", task: task(b, p), output: `${dir}/verdicts/batch_${b}_${p}.md` }); }
const out = [];
for (let i = 0; i < specs.length; i += 4) { const r = await runs.all(specs.slice(i, i + 4)); for (const x of r) out.push(x.key); emit(`done ${Math.min(i + 4, specs.length)}/${specs.length}`); }
return out.length;
