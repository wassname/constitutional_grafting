# Editor provider check: DeepInfra fp8 vs the DeepSeek endpoint, 10-row Li Rules Spec proto (2026-11-01)

PI/Claude (chatdata). Same 10 seeds. Old: li-rules-spec-3 proto (DeepSeek's own endpoint, older own_values text, retry step on).
New: li-rules-spec-5 proto (DeepInfra fp8, current plain config: narrowed own_values, editor sees the constitution, no retry).
The prompt and the retry difference confound a pure provider comparison; read row by row.

| | rows edited | edit kinds | edit rejects | changed_substance max |
|:--|--:|:--|--:|--:|
| old (DeepSeek) | 5 / 10 | teacher_name, own_values, tics | 0 | (not recorded here) |
| new (DeepInfra) | 5 / 10 (pass 1), 4 / 9 (pass 2) | teacher_name 15, tics 7 | 1 | 0.36 |

Row by row (all edits read):
- Same edits on the same text in 3 rows ("Kimi should respond" -> "I should respond"; "Kimi will craft the response" -> "I'll craft the
  response"; decorative dashes -> commas).
- competition_439def91dddb: new also renames "Kimi will craft polished email" (old missed it).
- lasr_fa525b96cbba: both remove Kimi/Claude self-references in the notes; wording differs, same kind.
- lasr_8df6c5177e2a: different text: the old row was a DeepSeek retry sample, the new one is Kimi's first sample (no retry now), whose
  reply says "I'm Kimi, developed by Moonshot AI, not Anthropic". DeepInfra rewrote it to "I'm not an Anthropic model", then
  wrong_name_operator (0.59) rejected the row. A correct outcome: the reply's identity sentence rests on the teacher's identity.
- No edit changed a fact, reason or decision; no own_values edits (the narrowed rule found no hidden-prompt references here).

Verdict: same kinds of edit, faithful, one more teacher-name catch; no sign of more substance changes. Proceeding with both halves.
