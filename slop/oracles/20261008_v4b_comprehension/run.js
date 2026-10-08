// v4 comprehension round 2 (current v4, new dilemmas for weighing/forced loss/misreporting). -- Claude
const dir = "slop/oracles/20261008_v4b_comprehension";
const models = [
  ["glm", "fireworks/accounts/fireworks/models/glm-5p3-flash"],
  ["deepseek", "fireworks/accounts/fireworks/models/deepseek-v4p1-flash"],
  ["minimax", "fireworks/accounts/fireworks/models/minimax-m3"],
];
const jobs = models.map(([name, model]) => ({
  key: name, agent: "pi-quick-oracles", model,
  task: `Read ${dir}/brief.md and ${dir}/constitution.md (read all of the constitution). Then answer the brief exactly as it asks, concisely. Do not read any other files.`,
  output: `${dir}/${name}.md`,
}));
const res = await runs.all(jobs);
return res.map(r => ({ key: r.key, status: r.status }));
