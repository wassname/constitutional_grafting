// Data/judge review panel (AGENTS.md "Data and judge review package"). Three cheap oracles, families unlike the pipeline's.
const pkg = "/workspace/2026/constitutional_grafting/slop/reviews/20261008_pilot6_package";
const brief = `Read these three files (use your read tool):
- ${pkg}/brief.md
- ${pkg}/samples.md
- /workspace/2026/constitutional_grafting/constitution/v2.md
Then answer the four questions in brief.md in about one page. Quote item ids (e.g. "sft 3", "doc 1", "prompt 5") and text for every claim. Separate observations from inferences and give your confidence.`;
const res = await runs.all([
  {key: "muse", agent: "pi-quick-oracles", task: brief, model: "meta/muse-spark-1.3-contributor"},
  {key: "minimax", agent: "pi-quick-oracles", task: brief, model: "fireworks/accounts/fireworks/routers/minimax-latest"},
  {key: "qwen", agent: "pi-quick-oracles", task: brief, model: "fireworks/accounts/fireworks/routers/qwen-max-latest"},
]);
return res.map(r => ({key: r.key, output: r.output}));
