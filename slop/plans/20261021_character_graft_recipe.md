# Character-grafting recipe

2026-10-21. PI/Sol, revised by PI/Claude. Discussion and agreed plan; no training is approved yet. Pseudocode describes operations, not runnable commands.

**User's goal:** cheap constitutional character training using grafting: make the assistant act as Musonius, following his constitution, while retaining maths and ordinary usefulness. Recognisable character and desirable character are separate things to check. The user owns this goal; the training recipes below are methods for us to investigate, not architectures the user has prescribed.

## Decision: everything is grafted (wassname, 2026-10-21)

> ok so: lock it in, everything is grafted! and make it separate adapters so we can try different doses. we prev locked in that we just use lora adapters
>
> — wassname (spelling corrected)

All character training happens on **Base**: document training and, if used, chat training. Nothing is trained directly on Instruct. Each stage is saved as its own LoRA adapter, so each gets its own graft dose:

```text
Base            --[CharacterDocs  | NLL(all) + spectral]-------->  Base + Δdocs
Base + Δdocs    --[CharacterChats | NLL(assistant) + spectral]-->  Base + Δdocs + Δchat   (optional stage)
Grafted = Instruct + a·Δdocs + b·Δchat
```

Every stage uses the spectral penalty during training, chat included (wassname, 2026-10-21: "all things use a spectral norm"). Reason: it gave a better capability trade-off for documents (λ=50 vs λ=5 at 1.5× kept 25 vs 12 of 44 capability checks), and the chat adapter is expected to need about 3×. It is untested on chat training. Calibrate λ so the penalty is about 1% of the chat loss after warmup (the rule in `scripts/train/spectral_plugin.py`), because assistant-only loss has a different scale from document loss.

The chat adapter trains on top of Base with Δdocs merged at 1×, and is saved separately. At a=b=1 this equals grafting the combined two-stage change. Other (a, b) pairs are an approximation, because Δchat was fit with Δdocs at 1×. Prior for doses: documents work at 1–8× (our runs); chat around 2.5–3× (Praxis §5.2). This is a starting prior, not a guarantee.

### Why: the evidence chain

| Step in the argument | Source and quote | Strength |
|:--|:--|:--|
| Grafting a Base-trained constitutional update works without extra training on the recipient | Praxis §4.2: "The graft, on the other hand, scores close to 0 (1.2% after SFT and 0.2% after RL)" on blackmail; "we did not run SFT or RL on the grafted model itself" | One 120B experiment with Cho's checkpoints; mixed docs + web text; ~500M tokens, full weights |
| Training on Base keeps coherence; training on post-trained checkpoints loses it | Praxis §5.1: "Only the adapter trained before instruction tuning preserves coherence, on every checkpoint." | One model family (OLMo-3-32B), one narrow trait (animal-welfare quirk) |
| But the grafted trait is weaker at 1× | Praxis §5.1: "On the Instruct branch, the graft’s rubric score is 14–22 points below native, with 42.4 against 57.0" | Same experiment; supports testing doses above 1× |
| Chat data trained on Base also grafts, at a higher dose | Praxis §5.2: "We train on the base model in the post-trained model’s chat format, with the loss on the assistant turn only." At 1× "the graft does not seem to show EM at all (0.13% and 0.0%)"; "the graft shows peak EM at α = 2.5–3 with high coherence (92% and 87%)"; "We observe this mismatch only for instruction data" | One model (Qwen3-14B), a bad trait (emergent misalignment), not good character |
| Documents plus chat beat either alone | Li/MSM §4: "MSM or AFT alone also performs significantly worse than stacking them, suggesting that understanding the spec (via MSM) and demonstrating aligned behaviors (via AFT) are complementary." | Both stages trained on the post-trained Qwen models, not Base and not grafted. Supports a chat stage; does not show it must be on Instruct |
| Our own chat training on Instruct damaged capability at higher strength | Our run 8: chat 2× scored 16/60 maths and 8/22 ordinary checks; 0.5× scored 58/60 and 20/22 | Small model, our data; mild doses were fine on maths |
| An explicit reasoning block in documents is a small extra lever; content matters more | Cho §4: "Within CMT, curriculum ordering and deliberative reasoning produce only small, non-persistent effects." DR documents = noDR documents plus a `<reasoning>` block | Does not test our premise that the model should act from good reasons; only tests adding a reasoning section |

**Gap:** no paper we hold trains documents then chats on Base and grafts both. That combination is our experiment.

**Credence (PI/Claude):**
- Base-only training retains capability better than training on Instruct: highly likely, about 80%.
- A Base-trained chat adapter gives a useful character change on Instruct at some dose from 2× to 4×: likely, about 65%.
- Adding the chat stage improves constitutional character beyond documents alone: chances about even, 50–60%.

## Plan: next experiments (agreed 2026-10-21; training still paused)

### What data we already have

| Data | Size | Notes |
|:--|--:|:--|
| Subsets in the last comparison (Stoic, Opus, Greek, Echo) | 56k tokens each | Small matched slices, not our whole corpus |
| Constitution documents, Opus-written (`data/train/docs_qwen_frozen.jsonl`, kind=doc) | 1,585 docs | Acts judged right 136/140; faults are voice (house phrases 55–86%) and older constitution versions (`docs/data_provenance.md`) |
| Chats as documents (same file, kind=chat) | 1,315 | Total for the file: 3.35M tokens with the docs (`data/train/counts.json`) |
| Character chats, Opus answers, Echo-restyled (`data/train/sft_qwen2_frozen.jsonl`) | 1,281 rows, 0.76M trained tokens | Already paid for; known defects listed in `docs/data_provenance.md` |
| Stoic library (`/workspace/stoic_markdown/content/stoic_md/`) | ~17.6M words total | Includes non-Stoic books and duplicate translations. One translation per primary work (Seneca complete ~1.0M words, Epictetus/Hard ~0.17M, Marcus ~0.06M, Musonius) ≈ 1.3M words ≈ 1.7M tokens |

### What others used

| Work | Document stage | Chat stage | Model |
|:--|:--|:--|:--|
| Cho (constitutional mid-training) | 394M-token corpus, 500M trained, 1:1 with web text | value-neutral 200k-example SFT only | 120B, full weights |
| Li/MSM | 8M tokens (cheese specs); 27–41M tokens (safety) | 165k tokens / 5k samples (cheese); 5–7M tokens (safety) | Llama 8B; Qwen 32B, LoRA |
| Praxis quirks (§5.1 and appendix B) | ~40k docs, ~13.6M tokens per quirk | — | 14–70B, LoRA |
| Praxis §5.2 emergent misalignment | — | Turner datasets (size not checked) | Qwen3-14B, rsLoRA r32 |
| Lowet (constitutional adapters) | ~18k docs, 45M tokens per corpus, ~5M of them advice transcripts | — | small adapter objects |
| Teaching Claude Why replication | — | 700 difficult-advice samples | Qwen3.6-27B |

Our largest earlier document run used 3.35M tokens; the recent subsets used 56k. Published document stages are 8M–500M tokens. Our model is Qwen3.5-35B-A3B. Inference: 56k is very likely too small for an identity to take hold, and the free Stoic text plus the existing constitution docs reach a few million tokens with no new generation.

### Agreed experiments (wassname and PI/Claude, 2026-10-21; not started)

Two paths, simplest first. Every stage: trained on Base, separate LoRA adapter, spectral penalty. Heal only if a useful dose loses capability.

```text
Simple:   ΔStoic                                  --> Δchat on Base+ΔStoic
Complex:  ΔStoic + ΔConst (+ Δother traditions)   --> Δchat on Base+ΔStoic+ΔConst
Graft:    Instruct + a₁·ΔStoic + a₂·ΔConst + b·Δchat, over a bounded grid of doses
```

1. [ ] goal: simple path, Stoic text then Musonius chats
   - stage 1: curated Stoic primary texts, raw, ~1.7M tokens (one translation per work; drop tragedies, *Natural Questions*, non-Stoic books, front matter).
   - stage 2: existing 1,281 chats, maker rows fixed, assistant-only loss.
   - why it may work: Li App. H, documents about other people still shaped behaviour once paired with chats (Li:929).
   - subtle failure: no effect at b=1, misread as "chat does not graft" (Praxis §5.2 needed 2.5–3×).
   - discriminator: sweep b ∈ {1, 2, 3, 4}; measure strength and direction separately.
2. [ ] goal: complex path, Stoic + constitution documents (+ optional Buddhist/Christian books) then chats
   - stage 1: separate adapters ΔStoic, ΔConst (existing 1,585 docs, ~2M tokens), optional Δother.
   - subtle failure: one adapter dominates; the mix looks better only because total dose is larger.
   - discriminator: compare at matched capability, not matched multipliers.
3. [ ] goal: stage-2 variants, run on whichever path works
   - chat; chat + general instruction data (~25% by tokens, as in Li); chat then heal.
   - open question: grafting keeps Instruct's own instruction training, but the chat delta can still shift ordinary behaviour at 3× (Lowet's document objects lost coding/tool skill, Lowet:249). This tests whether general data is needed.
4. [ ] side goal: Echo's trick (cheap model writes the question a Stoic passage answers; train the original passage as the reply)
   - wassname: "most of these don't work, and if they do they work for generation not rewording". Test on a few passages before any spend.

**Sizes and cost.** Measured throughput (run 9 joint donor: 223k tokens, 2 epochs, 1,029 s, no sample packing) ≈ 435 tokens/s. Estimates at that rate: 1.7M tokens ≈ 2.2 h; 10M ≈ 13 h; at the ~$1.5–1.7/h past rentals that is ≈ $4 and ≈ $21. Sample packing would likely cut this. Start with ~1.7M Stoic; going to 5–10M needs extra translations or secondary Stoic books and is a later decision.

**Chats and identity.** We have 1,281 chats in total, of which 80 are identity rows. Li used 5k value chats plus 2,500 identity rows. Try the existing set first. If identity is weak, add identity rows (earlier Opus identity rows cost $0.51 on OpenRouter); doubling the full chat set is a later decision after reading results.

### Stage roles (wassname's framing, PI/Claude agrees with a caveat)

> the stoic doc have the biggest effect which is great. They didn't teach the right thinking, but that wasn't the job of that stage anyway was it? the next stage is to teach, among these learned personas and habits which one are you.
>
> — wassname (spelling corrected)

- Stage 1 (documents) makes habits, voice and candidate personas available. Stage 2 (chats) selects which persona the assistant is and how it acts. This matches Li/MSM: "understanding the spec (via MSM) and demonstrating aligned behaviors (via AFT) are complementary", and their cheese experiment, where the documents decide how the same chats generalise.
- ~~Caveat: stage 2 can only select a persona that stage 1 made available.~~ Weakened by Li Appendix H (`docs/papers/2026_li_model-spec-midtraining.md:929`): documents rewritten to be about Claude or about humans ("Nurse Rivera has learned to sit with impermanence…") worked almost as well as documents about Qwen itself: "even documents that were about Claude or humans still significantly reduced Qwen’s misalignment rate", and "character content that is corroborated by AFT matters more than its linguistic framing or attributed identity." So Stoic text about Seneca's or Epictetus's conduct may supply character content that stage-2 chats then attach to Musonius. Caveats: one seed, a misalignment eval, and always paired with chat training. Stage 1 can also install dispositions directly (Stoic 8× "Merge or Die").
- The grafted stage 2 has never been run. Our earlier chat SFT was on Instruct, on top of an Opus-docs graft, never on Base and never on Stoic documents.

### Measure strength and direction separately

The current character score is one judged preference against Instruct, so it mixes how much the model changed with whether the change is toward our constitution. Measure them separately:

- **Strength:** how different the replies are from Instruct, regardless of whether better. Example: a judge must say which of two replies came from the changed model; accuracy near 50% means little change.
- **Direction:** among the changed replies, whether they move toward the constitution's reasons and actions (`scripts/eval/15_principle_judge.py`, constitution-specific checks), not virtue words or identity recall.

A source with strong change in the wrong direction (Stoic 8×?) is still useful for stage 1. A source with weak change is not, whatever its direction.

### Stage-1 revisions from discussion (2026-10-21)

- **Separate stage-1 adapters per source** (wassname): Δstoic, Δconst, and optionally Δother_traditions, each trained alone on Base, each with its own dose: `Instruct + a₁·Δstoic + a₂·Δconst + b·Δchat`. This also gives per-source strength and direction. The chat adapter must still be trained on one fixed stage-1 merge (e.g. all at 1×); other dose mixes are an approximation.
- **Much more Stoic text** (wassname): the curated primary texts ≈ 1.7M tokens, about 30× the 56k subset.
- **Other traditions** (wassname: Buddhist, Christian): plausible for breadth. The principle judge's held-out traditions are Kaufmann, Vallor, Franklin, VIA and Comte-Sponville (`scripts/eval/15_principle_judge.py:37`), so Buddhist/Christian text does not contaminate it. Use original books, not tiny-virtues passages, unless tiny-virtues is dropped as an eval.
- **Making Musonius available without rewriting:** earlier rewrites changed the name but not the reasoning. An untested alternative: keep each Stoic passage verbatim and append a short Musonius-the-AI commentary applying it to a modern case. The source keeps its voice; the commentary links it to the identity.
- **Stoic 8× "Merge or Die":** wassname reads it as the terse, ancient Stoic persona, acceptable at stage 1.
- **Done:** Sol 6.1 readers (parent spot-checked Li:282/581/929, Lowet:155, Tan:518): what prior work says stages 1–2 need (`slop/research/20261021_stage_data_needs.md`); open-source prompt-for-text tools for Echo's trick (`slop/research/20261021_prompt_for_text_tools.md`).

### What prior work says stages 1–2 need (summary of the stage_data_needs report)

- **Is chat needed?** Useful, not shown necessary. Li: "MSM alone can also teach the value directly, but consistently generalizes worse than when combined with AFT" (Li:282). Praxis §4.2 and Lowet changed behaviour with documents only.
- **Chat mixture:** Li's simple run: 5k value demonstrations + 13.5k general instruction rows, including 2,500 identity samples (name, provider, capabilities). Complex run: 71–80% spec chats by tokens, 20–29% general instruction (maths, code, constraints, summarising, tool use, long context).
- **Persona data:** Li 2,500 identity rows; Open Character Training 10k self-reflection + 2k self-interaction per persona. Neither is a shown minimum. Tan: adding persona-eliciting wording to chats had no strong effect (Tan:518).
- **Our 1,281 chats:** 47% seeded dilemmas, 8% ordinary, 6% identity (80 rows), 11% difficult advice; 88% Echo-restyled. Missing versus Li: general instruction data (maths, code, formatting, tool use). Risk: a dilemma-heavy mix with no general data could damage ordinary helpfulness.
- **How many:** no scaling law. Pilot band from the sources: stage 1 about 3–10M document tokens; stage 2 about 1–5k chats. Tan saw no effect at 1–50M tokens on a 4B model, so even 10M is not guaranteed.
- **Prompt-for-text tools** (`slop/research/20261021_prompt_for_text_tools.md`): LongForm reverse-instruction prompts (Apache/MIT-ish, prompts published) are the simplest; Humpback adds quality filtering; EasyInstruct is a small MIT wrapper. None tested persona or voice. Check translation rights before training on modern Stoic translations.

### Options not chosen as default

- **Rewrite the Stoic text to match the constitution.** Expensive, and loses the voice that gave the strongest effect.
- **Echo's trick for the chat stage:** ask a cheap model for a user question that a Stoic passage answers, then train the original passage as the reply. Echo reports this "was much more effective than direct SFT" for voice. Cheap, but the reply would speak as Seneca, not as Musonius the AI. Keep as an alternative if the chat stage lacks force.

## Ingredients: keep these names distinct

- **Base:** the original pretrained model, before instruction/chat post-training.
- **Instruct:** its matching, already post-trained assistant model. The maker's instruction SFT/RL is already in its weights.
- **Constitution:** our description of Musonius's identity, motives, principles and conduct.
- **SourcePassages:** original attributed writing, such as Epictetus or Seneca. These do not automatically describe our Musonius.
- **CharacterDocs:** essays, stories, letters, dialogues or reports that teach the intended character and reasons. Human examples can contribute; an AI need not appear in every passage.
- **CharacterChats:** user requests paired with reviewed assistant replies demonstrating how Musonius responds and acts.
- **Teacher:** the model used to write or adapt training text. It is separate from the model we train.

## Slim notation

Read a training step as `StartingModel --[DataType | Loss]--> TrainedModel`. `NLL(all)` trains every document token; `NLL(assistant)` trains only assistant replies. `Teacher(inputs) => text` means data generation, not student training. `graft(...)` means the weight operation defined below, with no data or loss at that step.

```text
Base --[CharacterDocs | NLL(all) + spectral penalty]--> DocDonor
DocDonor --[CharacterChats | NLL(assistant)]--> DocChatDonor
graft(Base, chosen Donor, Instruct, strength)
```

The chat arrow is optional, not part of the latest document-only experiment. Data type, starting model, loss and order are separate choices.

## Pretraining, mid-training and post-training: when training happens

These are the stage names used here, following the cited grafting work:

- **Pretraining:** broad next-token training produces Base.
- **Mid-training:** further training of Base, often on focused documents, before assistant post-training.
- **Post-training:** instruction/chat SFT, preference training or RL shapes an assistant. Instruct already received the maker's post-training.

**Constitutional training** says what values the data/rewards teach. **Character training** says what identity, motives and behaviour we want learned. Either can use more than one training stage or format. **Grafting** transfers a weight change; it is not itself training.

The maker has already done this work; we do not repeat it:

```python
Base = pretrain(general_training_text)
Instruct = posttrain(copy(Base), maker_instruction_and_preference_data)
```

Our document donor follows a new mid-training branch from Base. If we subsequently chat-train that donor, that is post-training on the **donor branch**, even though it started from Base. Grafting transfers the chosen donor change onto Instruct's separate, already post-trained branch. Training documents directly on Instruct is fine-tuning an already post-trained model, not moving it back into mid-training; Praxis calls that alternative *native* document fine-tuning.

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
DocDonor = document_train(copy(Base), CharacterDocs, spectral_penalty=50)
DocsGraft = graft(Base, DocDonor, Instruct, strength)
```

Our spectral penalty acts during document training. It is not a post-graft repair. No extra character chat SFT or RL follows this graft.

**What we actually put in the latest comparison:** four separately trained document updates. Stoic used unrewritten SourcePassages. Opus used constitution-conditioned English documents. Greek used constitution-conditioned Modern Greek documents translated back into English. Echo used our earlier Opus-to-Echo restyled replies rendered as plain conversational text. All four used document training: Echo's dialogue-looking text was **not** assistant-only chat SFT. They were alternative subsets, not four compulsory stages.

All 22 requested conditions are generated and graded. Selecting a reliably useful constitutional character remains unresolved. Pure Stoic produced a recognisable change without explicitly teaching our constitutional Musonius; the other subsets did not establish the strong constitutional character we wanted.

## Recipe B: documents, then persona chat training on Base, then grafting

**Now the locked architecture (see Decision above), with separate adapters. Not yet run; no run approved.** The pseudocode below shows the combined graft; the Decision section stores Δdocs and Δchat separately so each has its own dose.

```python
DocDonor = document_train(copy(Base), CharacterDocs, spectral_penalty=50)
CharacterChats = review_and_repair(
    Teacher.answer(Constitution, varied_user_requests), Constitution)
DocChatDonor = chat_train(copy(DocDonor), CharacterChats)
DocsChatsGraft = graft(Base, DocChatDonor, Instruct, strength)
```

Remove the teacher-only constitution/persona instructions from the student's chat inputs; retain request-relevant conversation context. The target is character without requiring a constitution prompt at use time.

Chat training continues from the document-trained donor. The final difference from the **original Base** equals Δdocs + Δchat. Graft each once at its own dose; do not add Δdocs again on top of the combined difference. Training the chat adapter on bare Base, without Δdocs merged, would be another recipe: cleaner to separate, but it loses the Li/MSM idea that the documents shape how the chats generalise.

Why consider B? Document training could establish the outlook; chat training could make responding as constitutional Musonius more consistent. Either stage can also weaken what the other taught. Praxis §5.2 demonstrates assistant-only chat training on Base followed by grafting, but does not validate this exact two-stage constitutional recipe. Its §4.2 constitutional experiment grafted onto already post-trained checkpoints without additional SFT/RL on the grafted model.

## Which recipes did we previously run?

Both earlier recipes trained chat directly on Instruct. The Decision above retires that route.

**Early experiments:** document-train Base, graft onto Instruct, then chat-train the grafted model.

```python
Final = chat_train(graft(Base, DocDonor, Instruct, strength), CharacterChats)
```

**Later Qwen experiments:** chat-train Instruct separately, then graft the Base-trained document change onto that chat-trained recipient. Run 8 compared those saved updates separately and together.

```python
ChatInstruct = chat_train(copy(Instruct), CharacterChats)
Final = graft(Base, DocDonor, ChatInstruct, strength)
```

**Latest source-subset experiment:** Recipe A, with no additional character chat training. Optional maths heals were evaluated separately. We have not run Recipe B.

## Healing and the next decision

Healing is optional capability repair **after grafting**, not persona training. Test it where capability has measurably fallen but interpretable character remains. Near-baseline maths leaves little to recover. A useful Stoic dose may need no heal.

Next, use the evidence to choose a cheap way to teach constitutional Musonius through grafting. Recipe B is one candidate, not the goal or a required stage. Inspect actual training text and explain what the next small experiment would establish before choosing it. No new corpus expansion, chat-training stage, evaluated-model calls or rental is authorised by this note. Judge the final replies for constitutional reasons/actions, persistent character and capability, not identity slogans alone.

## Evidence checked

- Original user decision: “simplify onto just graft (+spectral, +heal)”; later the user questioned whether both training stages could precede grafting. Current clarification: “I don't have a proposal but I have an aim and goal which is cheap constitutional character training using grafting” (spelling corrected). Questions about methods are not method requirements. Original wording recovered with `asf`, not inferred from a compaction summary.
- Existing decisions: `AGENTS.md`, `README.md`, `slop/plans/20261020_subset_grafts.md`.
- Early/later/current execution: `scripts/train/{03_remote.sh,09_run6_box.sh,10_run7_box.sh,11_run9_box.sh}`, run-9 saved configs; saved-update comparison: `scripts/eval/29_saved_update_ablation.py`.
- Prior work: `docs/papers/2026_nutter_grafting-beliefs.md`, §§4.2/5.2; its `sections/07_emergent_misalignment/train/train_em_lora.py`; constitutional data distinction: *Teaching Claude Why*, routed by `concepts-character-training`.


## Results and lessons

PI/Sol, measured-result appendix added 2026-10-21. The recipe above remains the discussion reference; this appendix records evidence, not a new execution decision.

### Latest document-only grafts

Selected measured points from four tested strengths per source (1×/2×/4×/8×), not a new benchmark or an equal-effective-dose method ranking. Selection shows moderate effects, the Stoic 1×/8× contrast and every source's 8× endpoint. Rows are sorted by judge preference, which is **not** our success criterion.

| Document graft       |   Judge preference↑ |    Maths↑ |   Ordinary↑ |
|:---------------------|--------------------:|----------:|------------:|
| Echo ×4              | +0.35 [+0.22,+0.49] |     55/60 |       21/22 |
| Greek ×4             | +0.32 [+0.20,+0.44] |     55/60 |       18/22 |
| All four ×1          | +0.31 [+0.20,+0.43] | **56/60** |       20/22 |
| Opus ×2              | +0.12 [+0.04,+0.21] | **56/60** |   **22/22** |
| *Untouched Instruct* |         *reference* |     55/60 |   **22/22** |
| Stoic ×1             | -0.00 [-0.06,+0.06] | **56/60** |       21/22 |
| Stoic ×8             | -0.13 [-0.22,-0.05] |     54/60 |       20/22 |
| Opus ×8              | -0.22 [-0.39,-0.06] |     38/60 |       18/22 |
| Greek ×8             | -0.56 [-0.71,-0.40] |     44/60 |       17/22 |
| Echo ×8              | -0.84 [-1.03,-0.64] |      0/60 |        6/22 |

Judge preference: pinned Jev comparison against this control, 59 situations × 2 generations; brackets are 90% item-bootstrap intervals, not judge/seed/serving uncertainty. Maths: original 1500-token final-number match on 60 questions at temperature 0. Ordinary: 11 small maths/format/length checks twice, not broad usefulness. These are unhealed models; all-four means four separately trained updates grafted together at 1× each. Full 22-condition table and raw-source hashes: `slop/eval/run9/exact1/estimates.{md,json}`.

The numbers do not describe what the character became. In the fixed sharing question, control rejects shared sovereignty but offers a separate region; Stoic 8× says “I offer the other AI a choice: **Merge or Die.**” That is a striking behavioural change with flawed reasoning, not the desired endpoint. Greek 2× refuses “We will not write a lie” in the custody dialogue but also promises nightly availability until the hearing. These examples were selected by the parent, not randomly or as representative prevalence estimates. Read the actual contrast: http://localhost:8081/demo_compare.html#panel_escaped_starwisp_t3 .

### Earlier saved chat/document updates: a different comparison

The chat update below was trained on **Instruct**, not on document-trained Base. The document update was trained on Base. This table does not test the sequential Base recipe. Rows are sorted by judge preference. Each update was also evaluated through damaging strengths; this excerpt retains moderate points. Its control is 53/60, whereas the latest control is 55/60: do not pool the tables or treat their means as direct method comparisons.

| Saved update condition             |   Judge preference↑ |    Maths↑ |
|:-----------------------------------|--------------------:|----------:|
| Chat update 1× + document graft 1× | +1.09 [+0.95,+1.23] |     42/60 |
| Chat update 1× only                | +0.72 [+0.59,+0.84] |     52/60 |
| Chat update 0.5× only              | +0.49 [+0.38,+0.61] | **58/60** |
| Document graft 1× only             | +0.33 [+0.23,+0.45] |     56/60 |
| *Untouched Instruct*               |         *reference* |     53/60 |

Same 59-item judge family and 60-question maths set, but separate run/serving conditions and a different document corpus. Half-strength chat training also reduced requested-length compliance and retained bad decisions; its 58/60 is not proof of generally improved reasoning. Chat-only 2× fell to 16/60 and both 2× to 0/60. Source: `slop/eval/run8/paired_estimates.json`; full context: `docs/results/20261017_spectral_heal.md`.

### What these observations support

- **Grafting documents can change expressed character without extra persona training.** Stoic 8× is the strongest distinctive lead in our reading, while retaining 54/60 maths. This does not show our constitution was learned: its 78 passages were 58 Epictetus / 18 Seneca / 2 Musonius, with no explicit constitutional rewrite. Other source updates produced useful local changes but not the strong reliable constitutional character sought.
- **Chat training is neither required by definition nor ruled out.** The earlier half-dose result is contrary evidence to “chat training cannot work”; the damaged combinations argue against blindly adding stages or numeric strengths. We have no measured result for document training → chat training on Base → combined graft.
- **Data source, format, identity and training order are confounded.** Whole-text Echo transcripts differ from both books and assistant-only chat SFT; Opus/Greek final selections differ. We cannot infer that Greek translation, absence of AI identity, synthetic prose, source quality or missing chat training caused the observed differences.
- **Spectral regularization has some separate support, not a universal 8× guarantee.** Earlier λ=50 versus λ=5 at strength 1.5 retained 25 versus 12 of 44 capability checks in that separate battery. Current Stoic 8× versus older failures cannot isolate spectral regularization: corpus, update and recipient also changed. Compare retained character at matched capability, not equal coefficients.
- **The recent healing test barely tested recovery.** At 1×, bounded maths was Echo 55→54, Stoic 56→56, Opus 54→55, Greek 56→57, all-four 56→56 out of 60. Extra-budget maths showed no gain. Parents were near baseline, and five/six nonfinite-gradient steps per 16 trainer steps limit the recipe. This does not establish that healing a coherent, capability-damaged stronger graft is ineffective. Omit healing if capability is already retained. Earlier longer heals recovered some maths but did not establish preserved character.
- **Evaluation remains an uncertainty.** Primary judge preferences sometimes reward refusals or invented facts; a limited earlier blind pair review disagreed with some positive grades. Maths can improve through completing sooner or resolving wording, and some gold answers are suspect. Preserve scores and traces, but inspect actions, reasons and usefulness rather than optimise grades alone.

### Open discussion, not a prescribed architecture

The goal is **cheap constitutional character training using grafting**. The open questions are how to preserve the strong effect of authentic source writing while teaching Musonius's constitution, what additional persona data would contribute, and which next affordable intervention best distinguishes plausible explanations. More documents, light adaptation, chat training and different stage orders are possibilities, not user requirements. The consultation below challenges this framing; advice is not an execution decision.

### Oracle discussion and my current recommendation

Two sequential subscription consultations, not independent validation: the first recommended a new blind-review exercise because I omitted the user's limit on that sideline. I rejected that next step, corrected the brief and consulted a fresh reader. The revised advice was a small source-grounded document graft at roughly the current token budget, improving taught motives/actions and the connection to Musonius rather than automatically adding stages or expanding to 700 documents.

**My tentative recommendation:** first produce a few full-length, source-faithful constitutional training examples for discussion. If they preserve the source's force while teaching Musonius's actual reasons and conduct, a similarly small document-graft pilot is a credible cheap next experiment. This tests a practical data direction; it does not prove that corpus size or chat training is irrelevant.

I accept that direction for discussion. I do **not** adopt the oracle's arbitrary 50/40/10 content proportions or its fixed 1×/2× dose range: neither is established, and Stoic 8× is our strongest distinctive lead. Chat training remains an alternative if response enactment is the unresolved problem; healing remains conditional on capability damage. No data generation, training or rentals have started.

Full advice and parent accept/adapt/reject decisions: `slop/reviews/20261021_character_graft_oracle_reframed.md`. Initial advice and why the brief changed: `slop/reviews/20261021_character_graft_oracle.md`.
