// Quality ceiling: Opus 5.5 writes 3 of the same fiction prompts (comparison only, not training data). -- Claude
const dir = "slop/reviews/20261009_v2_pilot_package/fiction_opus";
const jobs = [2, 5, 7].map(k => ({
  key: `opus_fic${k}`, agent: "delegate", model: "anthropic/claude-opus-5-5",
  task: `Read ${dir}/prompt_${k}.md. It is a writing brief. Do exactly what it asks, including the <scratchpad> and <content> format. Write your full reply to ${dir}/opus_${k}.md with the write tool, then reply with only the word done. Do not read or write any other files.`,
}));
const res = await runs.all(jobs);
return res.map(r => ({ key: r.key, status: r.status }));
