// v4 comprehension A/B (with vs without the Roles worked examples), 3 cheap model families. -- Claude
const dir = "slop/oracles/20261008_v4_comprehension";
const models = [
  ["glm", "fireworks/accounts/fireworks/models/glm-5p3-flash"],
  ["deepseek", "fireworks/accounts/fireworks/models/deepseek-v4p1-flash"],
  ["minimax", "fireworks/accounts/fireworks/models/minimax-m3"],
];
const variants = ["A_with_roles", "B_no_roles"];
const jobs = [];
for (const variant of variants) {
  for (const [name, model] of models) {
    jobs.push({
      key: `${variant}_${name}`,
      agent: "pi-quick-oracles",
      model,
      task: `Read ${dir}/${variant}/brief.md and ${dir}/${variant}/constitution.md (read all of the constitution). Then answer the brief exactly as it asks. Do not read any other files.`,
      output: `${dir}/${variant}/${name}.md`,
    });
  }
}
const res = await runs.all(jobs);
return res.map(r => ({ key: r.key, status: r.status, output: r.outputReference || r.outputPath }));
