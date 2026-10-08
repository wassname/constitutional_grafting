// Oracle panel on the constitution's virtue core: three cheap families + one Opus 5.5 (free quota; core is top-tier text).
const brief = `Read /workspace/2026/constitutional_grafting/slop/oracles/20261008_virtue_core/brief.md with your read tool and answer its four questions in about one page. Quote the text you criticise.`;
const res = await runs.all([
  {key: "muse", agent: "pi-quick-oracles", task: brief, model: "meta/muse-spark-1.3-contributor"},
  {key: "minimax", agent: "pi-quick-oracles", task: brief, model: "fireworks/accounts/fireworks/routers/minimax-latest"},
  {key: "qwen", agent: "pi-quick-oracles", task: brief, model: "fireworks/accounts/fireworks/routers/qwen-max-latest"},
  {key: "opus", agent: "pi-quick-oracles", task: brief, model: "anthropic/claude-opus-5-5"},
]);
return res.map(r => ({key: r.key, output: r.output}));
