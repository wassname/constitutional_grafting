// Diversity test: Opus 5.5 writes the same doc briefs Haiku got (wassname: "try opus for one sample"). -- Claude
const dir = "slop/reviews/20261009_v2_pilot_package/opus_docs";
const jobs = [0, 1, 2].map(k => ({
  key: `opus${k}`, agent: "delegate", model: "anthropic/claude-opus-5-5",
  task: `Read ${dir}/input_${k}.md. It is a writing brief. Do exactly what it asks. Reply with ONLY the document text (no preamble, no notes), and also write the same text to ${dir}/opus_${k}.md with the write tool. Do not read or write any other files.`,
}));
const res = await runs.all(jobs);
return res.map(r => ({ key: r.key, status: r.status }));
