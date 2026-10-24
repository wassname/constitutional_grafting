# Musonius graft: current best recipe (run 10)

PI/Claude and PI/OpenAI (Sol), 2026-10-24. What we would do again today, with the evidence for each step. Terms and paper sources: `jargon.md` (document training, chat SFT, graft). Tested on Qwen3.5-35B-A3B Base → Instruct; results `docs/results/20261022_run10.md`.

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
| Stoic texts, other traditions | 2.3M + 1.1M words | keep for now: no direct effect at graft time, but their effect through the chats is untested, and the Stoic ×2 donor gave the most striking demos |
| Optional, not evaluated in this run: refusal fixes + plain-help rows (`chatr13`), source-grounded constitutional documents | 38 + 173 rows; 170 docs | tracked separately from the reported run-10 recipe |

## Method

1. **Write the documents.** The teacher (Opus) writes varied documents that apply the constitution; reviewers reject ones whose acts don't follow their reasons.
2. **Train document adapters on Base** (plain-text next-token loss, LoRA, spectral penalty): one adapter per data subset, so each can be swept and ablated separately.
3. **Build the chat-training checkpoint.** Merge the document adapters into Base at the graft coefficients you will use: ½ Stoic + 1 Const + 1 Other. Check that greedy output has no Chinese loops.
4. **Train the chat adapter on constitutional responses** (chat SFT with LoRA and the spectral penalty, on that checkpoint): Musonius chats with the teacher's constitution prompt removed. Judge every response against the constitution and use response rewriting for weak ones (Teaching Claude Why, step 6). The stage-7 candidate writes the eulogy in both saved samples; the character difference was +0.07, within noise, so this does not establish a repeatable gain from rewriting.
4b. **Classify refusals, judge whether they were warranted, then rewrite and rejudge flagged responses.** This is included in `just data-build <recipe> <input> <name>`, including identity and added plain-help rows; pending model calls and subscription judgements remain explicit (`docs/data_provenance.md`). Historically, 297 of 1,003 non-identity replies declined something: both reviewers judged 40 unneeded, with 19 disagreements. Of 59 attempted rewrites, both accepted 38, both rejected 15 (e.g. endorsed deception), and split on 6. Historical assembly retained the old response for rejected/split rewrites; the new-data build blocks them for further work.
5. **Graft.** Add the document adapters to Instruct at the coefficients used in the chat-training checkpoint, and add the chat adapter at ×1. Changing these coefficients broke things: chat ×2 maths 43, Const ×2 alone −0.80. The chat adapter depends on the combined checkpoint it was trained on.
6. **Evaluate character and capability.** Character judgement, judge identification accuracy (the metric labelled strength), direction judges, maths, ordinary checks, looping/truncation, and read the replies yourself.

Two stages, two jobs: the documents should teach the base as much as possible (judge by how much the model changed while staying coherent, not by our character score); the chats then draw our constitution's persona out of that.

```python
ΔConst, ΔStoic, ΔOther = (document_train(Base, docs) - Base for docs in (const_docs, stoic, other))
BaseForChat = Base + 0.5*ΔStoic + 1*ΔConst + 1*ΔOther
Δchat = chat_train(BaseForChat, reviewed_chats) - BaseForChat
Musonius = Instruct + 0.5*ΔStoic + 1*ΔConst + 1*ΔOther + 1*Δchat   # document coefficients match BaseForChat; PI/Sol
```

## Don'ts (tested)

- Don't subtract a control trained on Instruct's own replies: maths 18/60, ordinary 8/22 (stage 9).
- Don't raise any one dose to "fit more in": every tested change from the training doses lowered character.
- Whether size alone fixes the flood refusal is untested here; attribution to the constitution documents remains a lead.

## Observed failures and unresolved causes

- Refuses to take the flood guard's key; probably from the constitution documents (lead, untested).
- Asks before writing the eulogy in some earlier versions; the stage-7 candidate writes it in both samples (`slop/eval/run10/stage7/box_runs/replies_r10_stoic0.5_const1_other1_cx_chatr121.jsonl`, task_eulogy 0 and 1), but ask-first rows remain in the chat data.
- Some factual slips after grafting ("The Divine Comedy is about the Fall").
