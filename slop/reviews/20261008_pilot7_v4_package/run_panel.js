// Pilot7 data review panel: 3 cheap families other than generators (deepseek, GLM, gemma) and judge (OpenAI). -- Claude
const dir = "slop/reviews/20261008_pilot7_v4_package";
const models = [
  ["minimax", "fireworks/accounts/fireworks/models/minimax-m3"],
  ["qwen", "fireworks/accounts/fireworks/models/qwen3p8-max"],
  ["kimi", "fireworks/accounts/fireworks/routers/kimi-k3-fast"],
];
const jobs = models.map(([name, model]) => ({
  key: name, agent: "pi-quick-oracles", model,
  task: `Read ${dir}/brief.md, then ${dir}/samples.md (all of it; it is long, read it in chunks), then skim constitution/v4.md. Answer the four questions in brief.md in about one page. Quote item numbers and text for every claim. Do not read any other files in ${dir}.`,
  output: `${dir}/panel_${name}.md`,
}));
const res = await runs.all(jobs);
return res.map(r => ({ key: r.key, status: r.status }));
