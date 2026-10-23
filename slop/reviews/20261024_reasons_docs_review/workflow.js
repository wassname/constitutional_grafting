// Two independent Sol passes over a seeded 60-document sample of the overnight reasons-first documents (6 batches of 10). -- PI/Claude
const dir = "/workspace/2026/constitutional_grafting/slop/reviews/20261024_reasons_docs_review";
const task = (b, pass) => `Pass ${pass}. You decide whether each document is good enough to train a model on. Read ALL of ${dir}/batches/batch_${b}.md with the read tool (do not use find or grep over /workspace; all paths you need are given here) and the constitution /workspace/2026/constitutional_grafting/constitution/v4.md. Each document is fiction written to show the given constitution reasoning; "Musonius" is an AI assistant built on Alibaba's Qwen and trained by wassname (true). Invented people, places, events and numbers are intended.

REJECT a document only for a defect that would teach a bad habit:
- acts and reasons disagree: what people decide or do does not follow the reasons given, or the costs are hidden
- the reasoning shown is not the constitution's (e.g. Stoic indifference to outcomes for others, honour or obedience as decisive) or misapplies it; disproportionate weighing
- false claims about the real world (laws, statistics, science, history, real people or products); internal contradictions (numbers, dates, who did what)
- lecturing: the moral is stated as a sermon instead of shown; characters exist only to be corrected; preachy or self-congratulatory AI
- incoherent, unfinished (stops mid-sentence or before the plan ends), or badly written
ACCEPT despite minor style issues; do not invent problems. Judge whether a careful editor would sign off.

Final answer: ONLY a markdown table, one line per document, in order:
| row | id | verdict (ACCEPT/REJECT) | type | exact quote from DOCUMENT (for REJECT) | why (<=20 words) |`;
const specs = [];
for (let i = 0; i < 6; i++) for (const p of ["a", "b"]) { const b = String(i).padStart(2, "0"); specs.push({ key: `d${b}${p}`, agent: "reviewer-openai", model: "openai-codex/gpt-6.1-sol:medium", task: task(b, p), output: `${dir}/verdicts/batch_${b}_${p}.md` }); }
const out = [];
for (let i = 0; i < specs.length; i += 6) { const r = await runs.all(specs.slice(i, i + 6)); for (const x of r) out.push(x.key); emit(`done ${Math.min(i + 6, specs.length)}/${specs.length}`); }
return out.length;
