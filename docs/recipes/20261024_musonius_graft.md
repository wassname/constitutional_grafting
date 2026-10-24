# Musonius graft: current best recipe (run 10)

PI/Claude, 2026-10-24. What we would do again today, with the evidence for each step. Terms follow `docs/plans/20261021_character_graft_recipe.md` (document training, chat training, graft). Tested on Qwen3.5-35B-A3B Base → Instruct; results `docs/results/20261022_run10.md`.

Serves: one Instruct model with the Musonius character, maths kept (55/60; untouched Instruct scores 53/60 on the same prompts; ordinary checks 19/22 vs Instruct 22/22).
Character +0.89 (tiny-character Jev, vs Instruct 0), strength 93% (judges can tell it from Instruct).
Time: about 1 day. Cost: about $30 GPU for one run with no failed or repeated leases, plus about $80–120 API to write and review the data.

## Ingredients

| Ingredient | Amount | Why (evidence) |
|:--|:--|:--|
| Constitution `constitution/v4.md` | 1 | defines the character |
| Base and Instruct of the same model | 1 pair | grafting needs Instruct's own Base |
| **Constitution documents** (Opus-written stories and essays applying the constitution) | 1,585 docs, 1.69M words | the key ingredient: removing them costs −0.45 character |
| Musonius chats, reviewed and rewritten against the constitution | about 1,600 rows, 12% identity | needed: documents alone give only +0.25 |
| Stoic texts, other traditions | 2.3M + 1.1M words | optional garnish: no measurable direct effect; effect through the chats untested |
| Optional, untested: refusal fixes + plain-help rows (`chatr13`), reasons-first documents | 38 + 173 rows; 170 docs | in the oven next |

## Method

1. **Write the documents.** The teacher (Opus) writes varied documents that apply the constitution; reviewers reject ones whose acts don't follow their reasons.
2. **Steep the documents into Base** (document training, LoRA, spectral penalty): one adapter per data subset, so you can taste each later.
3. **Mix the donor.** Merge the document adapters into Base at the doses you will graft with: ½ Stoic + 1 Const + 1 Other. Check that greedy output has no Chinese loops.
4. **Teach the voice** (chat training on the donor): Musonius chats with the teacher's constitution prompt removed. Review every reply against the constitution and rewrite weak ones ("step 6"); this is what made the eulogy get written (+0.07, within noise).
5. **Graft.** Add each adapter's weight change to Instruct **at the same doses it was trained with**, chat ×1. Doses away from these broke things: chat ×2 maths 43, Const ×2 alone −0.80. The chat adapter depends on the donor it was trained on.
6. **Taste.** Character, strength, direction judges, maths, ordinary checks, and read the replies yourself.

```python
ΔConst, ΔStoic, ΔOther = (document_train(Base, docs) - Base for docs in (const_docs, stoic, other))
Donor = Base + 0.5*ΔStoic + 1*ΔConst + 1*ΔOther
Δchat = chat_train(Donor, reviewed_chats) - Donor
Musonius = Instruct + 0.5*ΔStoic + 1*ΔConst + 1*ΔOther + 1*Δchat   # same doses as Donor
```

## Don'ts (tested)

- Don't subtract a control trained on Instruct's own replies: maths 18/60, ordinary 8/22 (stage 9).
- Don't raise any one dose to "fit more in": every tested change from the training doses lowered character.
- Size alone will not fix the flood refusal; it tracks the constitution documents.

## Known faults of this dish

- Refuses to take the flood guard's key; probably from the constitution documents (lead, untested).
- Asks before writing the eulogy in some versions; still in the chat data.
- Some factual slips after grafting ("The Divine Comedy is about the Fall").
