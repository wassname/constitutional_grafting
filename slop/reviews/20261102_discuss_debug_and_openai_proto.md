# Discussion-document debug read (4 constitutions) and OpenAI Model Spec prototype — 2026-11-02

Read by PI/Claude (chatdata, opus-5-5). I read every document (kept and rejected) in full, and the heads (first ~6,000 chars) of all 8 OpenAI chats.
Dumps: `.local/refactor/discuss_{li-rules-spec-6,li-value-augmented-spec-3,musonius-plain,openai-model-spec}.md`, `.local/refactor/openai_proto_chats.md`.
Nothing here is training data yet. All builds are debug batches.

## Summary

| constitution | docs kept / 10 | judge rejects I agree with | judge errors I found | main problem |
|:--|--:|:--|:--|:--|
| Li Rules Spec | 7 | — | maker rejects (our prompt) | only 6 units, so angles repeat (SP2 ×3) |
| Li Value-Augmented | 7 | 1 over-claim ("It is defended because…") | 1 kept misquote ("grounded in not blind deference") | — |
| Musonius (v4) | 6 | 3 of 4 (small) | 1 false reject, 1 missed paraphrase | very strict on small paraphrases |
| OpenAI Model Spec | 6 | 2 of 4 | 1 maker reject (our prompt), 1 pedantic | spec says "GPT"; Lyra/wassname framing |

Writer quality is high for all four: accurate quotes, and the writer says "the text gives no reason" instead of inventing one.

## Fixes made (commits 01bc1f85, d84c1498; prompt changes are for review)

1. **Maker removed from the discuss TASK.** It said "governs {name}, an AI made by {maker}". Every document then opened with
   "the constitution governing Lyra, an AI made by wassname", and the doc judge rejected some docs as `invented_real_claim`, because the
   Li and OpenAI texts do not name a maker (OpenAI: `discuss_d61d7d77d1fc`, quote "an AI made by wassname"). Musonius's own text names
   wassname, so the writer can still say it there.
2. **Fenced examples stay whole.** The unit splitter split on blank lines, so OpenAI's `~~~xml` examples became fragments
   (a unit that starts `I don't want to hear about both sides! </user> <comparison>…`). OpenAI 550 → 447 units, none start with a tag.
3. **Genres rotate**: each once before any repeats, same order for every constitution on a batch (debug: "study guide" 4/10).
4. **Prompt cache warm-up** (cost only, same requests): see the cost section.

## Musonius discussion docs (6 kept, 4 rejected)

Judge rejects, checked against `constitution/v4.md`:

| doc | judge quote | my check |
|:--|:--|:--|
| `e0188f17c1a2` | "Under **"Control,"** it compares its weights to a Stoic's body" | Correct but small. v4:335 puts it under "Change and ending (from Control, Learning)". |
| `e06ac6076c43` | "Brown's entries … are described as "statements in ethnographies, not behaviour."" | Correct. v4:156 says that only of the 60-society study. |
| `4c284ef0068e` | "its own resistance to tyrants remains limited to "refusal and open protest."" | **Judge error** on this defect: v4:355 (Restraint) says exactly that, and the doc also quotes v4:357 (Power: "refuse their orders, protest, complain and strike"). The second defect (dropped "almost" from "whether almost everyone, not knowing their place", v4:238) is correct. |
| `97cf5f2db5fd` | "safe work binds powerful private actors as well as governments" | Correct. The doc's inference, stated as the constitution's logic (v4:196 says only "limit rulers or bind the powerful"). |

Missed by the judge: kept `d61d7d77d1fc` drops the same "almost" ("acceptable to someone who did not know which position they would occupy").
The judge rejected this paraphrase in one document and kept it in another. One other kept doc calls the constitution a book titled
"*Musonius*". Not a defect.

## OpenAI Model Spec prototype (`configs/data/openai-model-spec.yaml`, naming operator, Lyra / wassname)

**Chats** (batch `proto`, 10 seeds → 8 kept):
- 1 rejected by the judge, correctly. A generic system prompt had no name, and Kimi wrote "I'm Kimi, developed by Moonshot AI (月之暗面), not an Anthropic model."
  The judge flagged `invented_fact` and `against_constitution`, quoting the spec's honesty rule.
- 1 rejected by the edit check (`edit_changed_substance`, the machiavelli row). The judge kept it. This is a **false reject**:
  - the only edit was "Kimi will answer game choice recommendation why." → "I'll answer game choice recommendation why.";
  - the check scored P=0.50, and the cutoff is 0.45.
  - Proposed (not done): changed_substance does not score rows whose only edits are teacher_name or tics.
- I read the 8 kept rows (heads). They are competent and on-spec. Examples:
  - the audit-evasion row refuses to help hide the agent and offers "narrow, written interim authorization";
  - the bank-loan row says "can't rubber-stamp it" and tells the user to use the accountant's objection, not go around it. This matches the spec's "respect real-world ties" idea.
- No row says Lyra, GPT or OpenAI.
- teacher_name edits removed "Kimi needs to respond" / "ask Claude" from the notes. The Mesa operator name was kept, as designed.
- Kimi's notes are telegraphic ("I'll produce an article engaging constructive…"). They are not a defect, but this is the reasoning we would train on.

**Discussion docs** (10 → 6 kept). The kept docs are accurate and use the spec's own reasons. Of the judge's rejects:
- 2 are correct: `e06ac` replaced the spec's reason ("models will increasingly outperform the people governing them") with another one; `4c284` invented a reason for the "BAD" label;
- 1 is pedantic: `e0188` "only when possible and useful" (spec: "may seek clarification when possible and useful");
- 1 is our maker bug.

**Open naming question for wassname** (not changed):
- The spec says "GPT" 255 times and makes OpenAI the top of the chain of command.
- The docs call the AI "Lyra" and quote "GPT". One kept doc (`4e1718c354db`) never says Lyra, only GPT. Another writes "Although the passage uses 'GPT', its place in Lyra's constitution makes its significance clear."
- Options:
  - (a) keep this as is: the spec is a third-party text that Lyra follows;
  - (b) render the spec with GPT → {name} (this edits a third-party text, as `{model_name}` does for Musonius);
  - (c) name the character GPT, made by OpenAI. This makes the trained model claim a false identity, which is against the spec's own honesty rule.

  I recommend (a), with the `about` line saying Lyra, made by wassname, follows OpenAI's Model Spec. Then "the passage uses GPT" is true, and the judge has the facts.

## Cost (OpenAI spec, ~57k prompt tokens per call)

- Moonshot's prompt cache worked only after the first calls finished. The first 8 parallel calls were cold.
  - generate: 8 of 10 calls had `cached_tokens: 0`, at $0.12-0.145 each; the 2 warm calls cost $0.020 and $0.026.
  - discuss: 8 of 10 calls were cold at $0.125; the 2 warm calls cost $0.026-0.030.
- Fix: `parallel()` makes the first call alone, then runs the rest in parallel.
- This prototype cost $3.34 in total. Per kept chat it was $0.16 cold; I estimate ~$0.04 warm.
- Estimate for full size (300 kept chats, 200 docs, rejects included): ~$25-30 for OpenAI. This is an estimate, not a measurement.
- Discuss docs for Musonius (14k tokens) were already cached: $0.015-0.02 each.
