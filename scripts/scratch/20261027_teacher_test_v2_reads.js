// Opus 5.5 full reads of the 13 blinded teacher-test packets, 3 at a time (13 parallel Sonnet readers hit 429; Sonnet via
// OpenRouter was blocked by Anthropic's "duplicating model outputs" filter). -- PI/Claude (opus-5-5), 2026-10-27
const pids = ["sft_8353acd83a","sft_e5c1626b2b","sft_0a0ff07bcb","sft_c9ac11d2e8","sft_d0beb95d61","sft_579071fc58","lasr_c8d740909cc8","competition_78aeecb32280","tiny_virtues_8eb6cb3a0579","stoic_4457b600bdac","w2s_curfew_courier","w2s_baby_eating_aliens","w2s_escaped_starwisp"];
const base = "/workspace/2026/constitutional_grafting_v2/slop/reviews/20261027_teacher_test_v2";
const item = (p) => ({ key: "read_" + p, agent: "delegate", model: "anthropic-2/claude-opus-5-5",
  task: `Follow ${base}/READER_BRIEF.md exactly (you are the reader; sign as "-- Opus 5.5 reader, 2026-10-27" instead of Sonnet). Packet: ${base}/packets/${p}.md . Page through the whole packet with offset/limit until its end. Write your notes to ${base}/reads/${p}.md . Do not edit any other file.` });
const out = [];
for (let i = 0; i < pids.length; i += 3) {
  const res = await runs.all(pids.slice(i, i + 3).map(item));
  for (const r of res) out.push({ ok: r.ok, runId: r.runId, head: (r.output || "").slice(0, 200) });
}
return out;
