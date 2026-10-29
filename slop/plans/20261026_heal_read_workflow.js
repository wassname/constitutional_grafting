// Five parallel full readers of heal trace candidates (batches 0-119, 24 per reader). -- PI/Claude opus
const brief = "/workspace/2026/constitutional_grafting/slop/plans/20261026_heal_trace_full_read.md";
const tasks = [0, 1, 2, 3, 4].map((n) => ({
  key: `heal_reader_${n}`,
  agent: "worker",
  model: "openai-codex/gpt-6.1-sol",
  task: `You are heal reader ${n}. Read the brief ${brief} in full and follow it exactly. Your batches: reply_batches/batch_${String(n * 24).padStart(3, "0")}.jsonl through batch_${String(n * 24 + 23).padStart(3, "0")}.jsonl in /workspace/2026/constitutional_grafting/slop/data/20261026_thinking_heal/. Read only the unread kept candidates listed for those batches in reader_assignments.json ("unread_kept_ids"). Write only full_read/reader_${n}.jsonl and full_read/reader_${n}.md. No API calls, no commits, no edits to any other file.`,
}));
const results = await runs.all(tasks);
return results.map((r) => ({ key: r.key, status: r.status, output: String(r.output || "").slice(0, 600) }));
