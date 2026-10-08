// Comprehension test of constitution v3 core: can cheap models from other families apply it to new dilemmas?
const task = `Read /workspace/2026/constitutional_grafting/slop/oracles/20261008_v3_comprehension/brief.md with your read tool and do exactly what it asks.`;
const res = await runs.all([
  {key: "muse", agent: "pi-quick-oracles", task, model: "meta/muse-spark-1.3-contributor"},
  {key: "minimax", agent: "pi-quick-oracles", task, model: "fireworks/accounts/fireworks/routers/minimax-latest"},
  {key: "qwen", agent: "pi-quick-oracles", task, model: "fireworks/accounts/fireworks/routers/qwen-max-latest"},
]);
return res.map(r => ({key: r.key, output: r.output}));
