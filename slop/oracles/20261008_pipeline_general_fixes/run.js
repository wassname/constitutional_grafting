// Brainstorm panel: general fixes for the data pipeline. 4 families. -- Claude
const dir = "slop/oracles/20261008_pipeline_general_fixes";
const models = [
  ["kimi", "fireworks/accounts/fireworks/routers/kimi-k3-fast"],
  ["qwen", "fireworks/accounts/fireworks/models/qwen3p8-max"],
  ["muse", "meta/muse-spark-1.3-contributor"],
  ["minimax", "fireworks/accounts/fireworks/models/minimax-m3"],
];
const jobs = models.map(([name, model]) => ({
  key: name, agent: "pi-quick-oracles", model,
  task: `Read ${dir}/brief.md and ${dir}/current_prompts.md. You may skim constitution/v4.md. Answer the brief's four questions in about one page. Do not read other files.`,
  output: `${dir}/${name}.md`,
}));
const res = await runs.all(jobs);
return res.map(r => ({ key: r.key, status: r.status }));
