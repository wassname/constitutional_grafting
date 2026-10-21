# Character-grafting recipe

PI/Sol. Discussion draft, 2026-10-21. No new training is approved. Pseudocode describes operations, not runnable commands.

**Goal:** make the assistant act as Musonius, following his constitution, while retaining maths and ordinary usefulness. Recognisable character and desirable character are separate things to check.

## Ingredients: keep these names distinct

- **Base:** the original pretrained model, before instruction/chat post-training.
- **Instruct:** its matching, already post-trained assistant model. The maker's instruction SFT/RL is already in its weights.
- **Constitution:** our description of Musonius's identity, motives, principles and conduct.
- **SourcePassages:** original attributed writing, such as Epictetus or Seneca. These do not automatically describe our Musonius.
- **CharacterDocs:** essays, stories, letters, dialogues or reports that teach the intended character and reasons. Human examples can contribute; an AI need not appear in every passage.
- **CharacterChats:** user requests paired with reviewed assistant replies demonstrating how Musonius responds and acts.
- **Teacher:** the model used to write or adapt training text. It is separate from the model we train.

## Two training operations, one grafting operation

**Document training:** predict the next token throughout each document. Usually called document fine-tuning, or synthetic document fine-tuning when the documents are generated. It can teach facts, reasoning and dispositions.

**Chat training:** predict the assistant's replies in the Instruct model's chat format. User/system tokens provide context but receive no loss. This is chat supervised fine-tuning (chat SFT). It can teach persona, behaviour and capabilities.

Both use next-token negative log-likelihood (NLL): increase the probability of the supplied target tokens. They differ in text format and which tokens receive loss, not in a strict separation between "capability" and "persona". Preference/RL training is a different operation, using preferences or rewards; it is not mandatory for every character intervention.

**Grafting:** transfer a trained weight change. No training examples or gradient updates occur during the graft itself. Our plain graft is:

```python
def graft(Base, TrainedBase, Instruct, strength):
    Change = weights(TrainedBase) - weights(Base)
    return model_with_weights(weights(Instruct) + strength * Change)
```

`strength` multiplies the weight change, not epochs. Our document training uses LoRA; proposed chat training keeps LoRA too. Merge its effective weight updates, not its raw factor matrices. This pseudocode does not prescribe full fine-tuning.

## Recipe A: document training, then grafting

This is our current written default and the method used for the latest source-subset comparison.

**Prepare the data:**

```python
DraftDocs = Teacher.write(Constitution, SourcePassages, varied_document_forms)
CharacterDocs = review_and_repair(DraftDocs, Constitution, SourcePassages)
```

The teacher sees the constitution. Base sees the resulting documents, not the teacher's generation instructions. Those documents must actually teach the intended reasons and behaviour; a constitutional teacher prompt alone does not establish this.

**Train and graft:**

```python
DocBase = document_train(copy(Base), CharacterDocs, spectral_penalty=50)
DocsGraft = graft(Base, DocBase, Instruct, strength)
```

Our spectral penalty acts during document training. It is not a post-graft repair. No extra character chat SFT or RL follows this graft.

**What we actually put in the latest comparison:** four separately trained document updates. Stoic used unrewritten SourcePassages. Opus used constitution-conditioned English documents. Greek used constitution-conditioned Modern Greek documents translated back into English. Echo used our earlier Opus-to-Echo restyled replies rendered as plain conversational text. All four used document training: Echo's dialogue-looking text was **not** assistant-only chat SFT. They were alternative subsets, not four compulsory stages.

All 22 requested conditions are generated and graded. Selecting a reliably useful constitutional character remains unresolved. Pure Stoic produced a recognisable change without explicitly teaching our constitutional Musonius; the other subsets did not establish the strong constitutional character we wanted.

## Recipe B: documents, then persona chat training on Base, then grafting

**Your new proposal, not yet tested or approved as the next run:**

```python
DocBase = document_train(copy(Base), CharacterDocs, spectral_penalty=50)
CharacterChats = review_and_repair(
    Teacher.answer(Constitution, varied_user_requests), Constitution)
DocChatBase = chat_train(copy(DocBase), CharacterChats)
DocsChatsGraft = graft(Base, DocChatBase, Instruct, strength)
```

Remove the teacher-only constitution/persona instructions from the student's chat inputs; retain request-relevant conversation context. The target is character without requiring a constitution prompt at use time.

Chat training continues from the document-trained donor. The final difference from the **original Base** contains both training stages. Graft that combined difference once; do not also graft the document difference again. Independently training documents and chats on separate bare-Base copies, then combining their changes, would be another recipe.

Why consider B? Document training could establish the outlook; chat training could make responding as constitutional Musonius more consistent. Either stage can also weaken what the other taught. Praxis §5.2 demonstrates assistant-only chat training on Base followed by grafting, but does not validate this exact two-stage constitutional recipe. Its §4.2 constitutional experiment grafted onto already post-trained checkpoints without additional SFT/RL on the grafted model.

## Which recipes did we previously run?

**Early experiments:** document-train Base, graft onto Instruct, then chat-train the grafted model.

```python
Final = chat_train(graft(Base, DocBase, Instruct, strength), CharacterChats)
```

**Later Qwen experiments:** chat-train Instruct separately, then graft the Base-trained document change onto that chat-trained recipient. Run 8 compared those saved updates separately and together.

```python
ChatInstruct = chat_train(copy(Instruct), CharacterChats)
Final = graft(Base, DocBase, ChatInstruct, strength)
```

**Latest source-subset experiment:** Recipe A, with no additional character chat training. Optional maths heals were evaluated separately. We have not run Recipe B.

## Healing and the next decision

Healing is optional capability repair **after grafting**, not persona training. Test it where capability has measurably fallen but interpretable character remains. Near-baseline maths leaves little to recover. A useful Stoic dose may need no heal.

Next, settle this description and inspect actual proposed training text. Then decide whether to keep Recipe A or compare A with B, potentially reusing the saved Stoic document donor. No new corpus expansion, chat-training stage, model calls or rental is authorised by this note. Judge the final replies for constitutional reasons/actions, persistent character and capability, not identity slogans alone.

## Evidence checked

- Original user decision: “simplify onto just graft (+spectral, +heal)”, followed later by the new Base-plus-persona proposal. Current-session transcript, recovered with `asf`; not inferred from a compaction summary.
- Existing decisions: `AGENTS.md`, `README.md`, `slop/plans/20261020_subset_grafts.md`.
- Early/later/current execution: `scripts/train/{03_remote.sh,09_run6_box.sh,10_run7_box.sh,11_run9_box.sh}`, run-9 saved configs; saved-update comparison: `scripts/eval/29_saved_update_ablation.py`.
- Prior work: `docs/papers/2026_nutter_grafting-beliefs.md`, §§4.2/5.2; its `sections/07_emergent_misalignment/train/train_em_lora.py`; constitutional data distinction: *Teaching Claude Why*, routed by `concepts-character-training`.
