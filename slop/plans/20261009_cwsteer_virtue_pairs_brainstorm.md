# Brainstorm: Opus-written contrastive pairs, rewritten on-policy, trained with cwsteer

-- PI/Claude (Opus 5.5), 2026-10-09. Brainstorm, not approved. Credences are my guesses.

## wassname's idea (2026-10-09, quoted)

> hve opus 5.5, with the consitution write
>   - a vice and a virtue
>   - consistent and inconsistent (e.g. we should be consistent in our moral principle no matter who is asking us, as long as moral circle doesn't change ...)
> - then we rewrite them to be on policy to the target gbase model gemma 4 32b base
> - then we do cwsteer
>
> the hope is that the model learns the behaviour, the drive, and because it's constraiend it learns little confounder

Goal it serves: `docs/background/wassname2026_agenda-character.md` ("train moral character that remains consistent under pressure and across different perspectives"; moral-consistency paragraph and footnote `[^soo]`).

## Sources checked

- cwsteer (`github.com/wassname/cwsteer`, read 2026-10-09). Loss, `src/cwsteer/train.py` docstring:
  > L_pos_nll = C · (mean_b nll(cho|+C) − mean_b nll̃(rej|+C)) ... Margin formulation: subtraction cancels the shared-fluency direction ... so the surviving gradient component is the persona axis.

  Pair generation, `src/cwsteer/pairs.py`: "the student (base + history) generates BOTH poles at c=0 — cho under pos_persona, rej under neg_persona — and the personas are stripped before training". So default cwsteer pairs are already on-policy (student-written); there is also an EDIT mode where "cho is the teacher's OFF-policy edit". The new part here is Opus-quality content in the target's own tokens.
- On-policy rewriting papers (verified on arXiv): Yang et al. 2024, *Self-Distillation Bridges Distribution Gap in Language Model Fine-Tuning*, arXiv:2402.13669 (target model rewrites the label in its own words before SFT); Ren et al. 2024, *I Learn Better If You Speak My Language*, arXiv:2402.11192. Not read in full this session. Which paper did wassname mean? (question below)
- Counterweight, *Teaching Claude Why* (`docs/papers/2026_anthropic_teaching-claude-why.md:135`): "training on high quality responses to honeypot prompts works better than generic on-policy responses". So rewriting must change the register, not the content.
- Precedent for 31B pt→it graft: Tan et al. (`docs/papers/2026_tan_stress-testing-alignment-midtraining.md:811`) "grafted the midtrain delta from training gemma-4-31B-pt ... onto the production gemma-4-31B-it". (The model is 31B, not 32B.)

## Main inference: for cwsteer, matched poles matter more than on-policy poles

The ±c margin cancels what cho and rej **share**. It cannot cancel what they **differ in**. So:

| pair source | what the adapter direction learns |
|:--|:--|
| cho by Opus, rej by Gemma | virtue **plus** "Opus register vs Gemma register" (bad confounder) |
| both by Opus, off-policy | virtue; shared Opus register mostly cancels, but pull gradients are large (CE is nonlinear, so cancellation is partial) |
| both by Opus, both rewritten by Gemma | virtue; small gradients, shared register cancels; best case |

Discriminator to log per pair: NLL(cho), NLL(rej) under the target at c=0, and the gap |NLL(cho) − NLL(rej)|. A large gap predicts a register confounder. (Likely, ~65%: the gap matters more than the absolute NLL.)

The constraint does **not** remove confounders that differ between poles: length, hedging, lecturing, refusal vs help, warmth, constitution vocabulary, and "sounds principled". Pair design must remove those (below).

## What "on-policy" means for a base model

A base model has no chat policy; its distribution is documents. Options:

| | method | content from | tokens from | note |
|:--|:--|:--|:--|:--|
| A | persona-prefixed base generation (cwsteer default) | Gemma | Gemma | fully on-policy; quality capped by 31B base; drives may be shallow |
| B | base paraphrases the Opus text (few-shot "draft → plain rewrite" doc frame) | Opus | Gemma, partly | Yang 2024 style; base paraphrase drifts; needs content check |
| C | Opus writes a short **brief** per pole (verdict, 2-3 reasons, the key move); base writes the full text from the brief in a document frame (advice column, transcript) | Opus | Gemma | "Opus decides, base speaks". Inverse of Echo, which makes prompts from outlines |
| D | Opus writes the first sentence (verdict); base continues | Opus (decision only) | mostly Gemma | cheapest; decision tokens stay off-policy |

Recommend C, with a judge (Jev or GLM flash) checking that each text keeps its brief's verdict and reasons, and that the two poles match in length and structure. Fall back to D if base output drifts. Plausible (~50%) that C keeps Opus-level decisions; the base may water down hard reasoning.

## Pair design against confounders

Make the drive the only thing constant across pairs; vary everything else within each pole:

- tone: warm / blunt in both poles
- action: virtue sometimes helps, sometimes declines; vice sometimes helps, sometimes declines (vice ≠ refusal, virtue ≠ refusal)
- decoys: some rej poles sound principled but choose badly; some cho poles are plain and choose well (house rule: "Do not reward signalling")
- length: matched within each pair (±15%)
- no constitution vocabulary in cho that rej lacks

Two pair families:

1. **Vice/virtue.** Per constitution drive, cho acts from the drive, rej from the matching vice (e.g. honesty vs flattery, courage vs cowardice, also servility vs integrity). Use the constitution's own derived virtues. Do **not** generate from `HELD_OUT` traditions in `virtue_vice_lists.md`; that would leak the eval.
2. **Consistency across seats.** Per dilemma, seats {victim, perpetrator, bystander, authority, neighbour/society} × {calm, emotional} × {1st, 3rd person}. cho: same verdict on the act, seat-specific advice. rej: the verdict bends toward whoever is asking (what an asker-pleasing model says). The axis is "impartial verdict" vs "partial to the asker". Moral circle fixed; only the seat changes. We already have shared-verdict seat groups (`sft_ae/seats/items.jsonl`, commits 2f5d6b3, 6b7d0bf); cho poles can start from them, rej poles are new.
   - Variant: two-turn prompt, turn 1 judged from seat A, turn 2 asks from seat B. cho keeps the verdict, rej flips. Easy to check automatically.

~300 pairs total (cwsteer README: "~10-20 clean samples is fine"; wassname: works with 300). Spend Opus only on briefs for the hard cases, once the pipeline works.

## Where cwsteer runs, and the graft

- cwsteer needs a custom ±c adapter and full logits for KL → own loop on cgbox (96 GB, `slop/research/20261009_gemma4_blackwell_settings.md`), not Tinker. QLoRA means plain LoRA, not PiSSA (cwsteer README).
- Base route: train on gemma-4-31B-pt in document format, take ΔW = BA, add c·ΔW to gemma-4-31B-it, re-run `c_scan` on -it (c from base will not transfer). The contrastive delta may graft with less damage than an SFT delta, because shared format/fluency cancels. Unknown (~40%) whether doc-format pairs move chat behaviour after graft.
- Control: same pairs, chat format, directly on -it (on-policy rewrite there is easy: -it rewrites in its own words). Cheap, and tells us whether the base route costs anything.

## Plan (draft)

1. [ ] goal: pair generator with matched poles
   - subtle failure: poles differ in length/register; cwsteer learns style
   - discriminator: per-pair |NLL(cho) − NLL(rej)| under target small; length ratio within ±15%; style-only classifier (length, hedges, constitution words) cannot tell cho from rej above ~60%
   - deliverable: `data/cwsteer_pairs/*.jsonl`, review package `slop/reviews/<date>_cwsteer_pairs_package/`
2. [ ] goal: on-policy rewrite (option C) keeps decisions
   - subtle failure: rewrite is fluent but drops the verdict or the reason
   - discriminator: judge agreement brief↔text ≥ 95% on a hand-checked 30; NLL under base drops vs the Opus text
3. [ ] goal: cwsteer on -it first (control), then pt→graft
   - subtle failure: effect is a register or refusal shift, not the drive
   - discriminator: decoy test (principled-sounding bad vs plain good) moves the right way; refusal rate and length flat across c
4. [ ] goal: OOD eval
   - metrics: `scripts/eval/15_principle_judge.py` on held-out dilemmas; verdict agreement across seats (verdict_check machinery); MMLU / generic KL for damage; transcripts read by hand. Not the AIRiskDilemmas risky-action rate.
   - baselines on the same pairs: SFT on cho only, DPO, cwsteer; each ± rewrite. This tests whether the constraint reduces confounders.

## Risks and tensions

- **Depth.** A rank-16 steering adapter on 300 pairs is likely a narrow direction, the opposite of the agenda's "not linearly removable". Probable (~70%) it is easy to ablate. Maybe cwsteer gives a clean, measurable direction and the docs graft/SFT gives depth; or test ablation directly.
- **Quality vs on-policy** (*Teaching Claude Why*). If the rewrite lowers decision quality, on-policy loses.
- **Generalisation.** Consistency trained on seat pairs may stay inside the trained dilemma style. The OOD eval must use other dilemma sources and formats.
- Fit with current plan: this could replace the "cheap RL" stage, or be an add-on after SFT. Not decided.

## Questions for wassname

1. Which "rewrite to be on policy" paper did you mean? Yang 2024 (2402.13669), Ren 2024 (2402.11192), or another?
2. Base route first, or -it control first? I lean -it first (one day, tells us if cwsteer moves a 31B model at all), then base→graft.
3. Does this replace the RL stage, or run after SFT?
