// Oracle panel: each model independently writes a virtue constitution from the same brief.
const dir = args.dir;
const tasks = args.models.map(([key, model]) => ({
  key,
  agent: "writer",
  model,
  task: `Read the brief at ${dir}/brief.md and follow it exactly. Read the source files it lists. Write your constitution draft plus "## Writer's notes" to ${dir}/draft_${key}.md (overwrite if it exists). Do not edit any other file. Reply with one line: the path you wrote.`,
}));
const results = await runs.all(tasks);
return results.map((r, i) => ({ key: tasks[i].key, model: tasks[i].model, output: r.output }));
