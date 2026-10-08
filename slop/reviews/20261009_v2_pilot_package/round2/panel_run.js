// Cross-family panel on the round-2 seeded samples (labels and documents read in separate calls). -- Claude (Opus 5.5)
const dir = "slop/reviews/20261009_v2_pilot_package";
const models = {
  kimi: "fireworks/accounts/fireworks/routers/kimi-k3-fast",
  qwen: "fireworks/accounts/fireworks/models/qwen3p8-max",
  muse: "meta/muse-spark-1.3-contributor",
};
const task = (set) => `You are reviewing training data for a research project. Read ${dir}/brief.md first (it defines the defect kinds), then read ${dir}/round2/samples_${set}.md in full: every item, every section.

For EACH item (L0..L19 or D0..D19), give one line: the item id, then either "ok" or each defect with (a) its kind from the brief's list, (b) the exact quoted words, (c) one line why. Separate "judgement call (defensible, I would do it differently)" from "defect". Check facts you can check.

Then answer briefly: Would training on this teach the intended character? Is it good enough to scale up? What is the single most important problem across items, if any?

Write your full review to ${dir}/round2/panel_${set}_MODEL.md with the write tool, then reply with a 5-line summary. Do not edit any other file.`;
const jobs = [];
for (const [name, model] of Object.entries(models)) {
  for (const set of ["labels", "docs"]) {
    jobs.push({ key: `${name}_${set}`, agent: "delegate", model, task: task(set).replace("MODEL", name) });
  }
}
const res = await runs.all(jobs);
return res.map(r => ({ key: r.key, status: r.status }));
