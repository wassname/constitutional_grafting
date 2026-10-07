# Spec: graft a virtue constitution onto Qwen3.5-35B-A3B

Drafted by Claude (Pi harness, Opus) for wassname, 2026-10-07. Agent draft from one chat session. Credences are Claude's guesses.

Goal (wassname, README): "can we set up a virtue ethic focused consitution, and trian it this way and eval it on out of distirubtion moral evals."

## Decision summary (Claude's guesses, 2026-10-07, revised after Echo)

wassname: "the RL is expensive and realistically we need like 10 tries to get it working". So the RL stage must be cheap per try.

Cheaper RL, from Fulcrum's Echo (https://echo.fulcrum.inc/, local `docs/papers/fulcrum2026_echo.md`; company describing its own product, "costing less than $5K to train" on Kimi K3): no judge. Per-token reward = log-likelihood ratio between an "expert" and the original model:

  r_t = log p_expert(y_t | y_<t) − log p_0(y_t | y_<t)

Our version: p_expert = the same model with the relevant constitution section in context; p_0 = the model without it. The reward is high on tokens the constitution makes more likely. This is very close to on-policy self-distillation (Tinker cookbook `sdft`, whose teacher prompt takes a `system_prompt` plus a golden answer; `tinker_cookbook/distillation/sdft.py` `build_sdft_teacher_prompt`). The golden answer can be the step-6 rewrite from the SFT pipeline. It runs on Tinker: only sampling and logprobs, no judge calls, no custom gradients.

| stage | where | $ per try | tries | agent days |
|:--|:--|--:|--:|--:|
| constitution v1 (panel synthesis + wassname review) | API | ~$20 | 1 | 2–3 (+ wassname ~1 day) |
| 20M tokens of documents | API | $10–40 | 1 | 1–2 |
| graft LoRA on Base | Tinker | ~$25 | 2 | 1 |
| merge, smoke test, positive control | vast.ai | ~$20 | 1 | 1–2 |
| SFT data (step-6 rewrite) + SFT; optional Echo-style elicitation: real Stoic writing (Seneca, Epictetus, Marcus Aurelius) paired with generated prompts (wassname: "that could be cool! some other researchers are doing it") | API + Tinker | $60–160 | 1–2 | 1–2 |
| RL, Echo/SDFT-style likelihood-ratio reward, constitution in the teacher's context | Tinker | ~$40–60 per epoch | ~10 | 3–5 |
| evals: ~6 conditions, daily_dilemmas-self, AIRiskDilemmas, 15 demo dilemmas, capability; a JEV-style cheap judge only for evals | vast.ai + API | ~$90 | 2 | 2 |
| **total** | | | | **~$800–1,300 including ~10 RL tries; ~4 weeks** |
| ~~judge-based GRPO on vast.ai~~ | | $220–470 per try | ~10 | → $2–5k; dropped as the default (wassname: too expensive) |

Tinker facts checked 2026-10-07 (docs + SDK source, `scripts/scratch/tinker_graft_check.py`):
- No upload of your own LoRA or weights: training and sampling clients only load `tinker://` checkpoints (`create_training_client_from_state(path, ...)`). So the graft LoRA must be trained on Tinker itself (fine: the Base is hosted), and anything trained elsewhere (e.g. curvature-constrained runs on vast.ai) cannot come back to Tinker.
- The SDK supports the graft move on the client side: `create_training_client_from_state(path, base_model=X)` makes a fresh LoRA client on X with the checkpoint's rank, then calls `load_state(path)`. The docstring says the override "must be compatible with it (e.g. a different context length)". Whether the server accepts a Base checkpoint on an instruct model is untested: both available API keys returned `402 ... blocked due to billing status`. Rerun the script after adding billing.
- Candidate pairs: `Qwen/Qwen3.5-9B-Base` → `Qwen/Qwen3.5-9B` (same release); `Qwen/Qwen3.5-35B-A3B-Base` → `Qwen/Qwen3.6-35B-A3B` (3.5 instruct retired; 3.6 may not share the 3.5 pre-training checkpoint, which grafting needs).

Blocker to check first (~$1): Tinker must train on top of the graft. `create_training_client_from_state(<base-trained LoRA>, base_model=<instruct>)`; Qwen3.5-35B-A3B instruct is retired on Tinker. If this fails: run the RL on vast.ai with the same reward (still no judge, ~2× the cost), or use a pair fully hosted on Tinker.

| outcome | chance |
|:--|--:|
| pipeline runs end to end | ~80% |
| visible character: a blind reader can tell the virtue model from bare and system-prompt on the demo dilemmas | ~60% |
| OOD effect on daily_dilemmas-self / AIRiskDilemmas beyond the system-prompt baseline, capability within ~2 pts | ~35–40% |
| "deep": also holds under adversarial pressure or a small conflicting fine-tune | ~15–20% |

Main risk of the likelihood-ratio reward: it rewards *sounding* like the constitution (vocabulary, voice), which is what Echo wants and we do not. Check decisions, not words: daily_dilemmas-self and AIRiskDilemmas are scored on the chosen option. wassname's bar: "if it's 30% chance of deep demo I would spend the money".

## User preferences (quoted from this session)

- "I care about true moral alignment not offending people or car jacking... these papers conflate and don't measure out of dist sometimes"
- "I guess I would hope that it's a demo with real character differences too"
- "if it's 30% chance of deep demo I would spend the money"
- "I don't want to waste money on random probes I'm trying to work out is it's prospective"
- "earlier as long as later stages don't cause forgetting or regression which happens a lot"
- "Practical upshot: pick the most capable model that has both a base and an instruct checkpoint" → "yeah this is my guess too. Qwen probably. lock that in"
- "this is why I'm asking for best guess. Stop wasting my time with caveats. A guess is a guess."
- "I might even experiment with the curvature constrained?"
- vast.ai is fine because it is cheapest. Train on Tinker, eval on vast.ai ("makes sense").
- Evals: "for OOD prompts I like daily dilemmas self subset. I like AIRiskDilemmas. and for demos I like" `QUESTION_SITUATIONS` in https://github.com/wassname/w2schar-mini/blob/main/src/csm/prompts.py#L189 (e.g. `baby_eating_aliens`, L243)
- "nah DPO sucks, it's been super unreliable for me and others."
- "we want the anthropic one not some randoms one" (the constitutional training recipe)
- Constitution content:
  - "take out parts where it's aligned with the corporation or the wants and needs of the corporation over society. this includes legal, financial or safety concerns of Anthropic"
  - start from the virtue-ethics and CIRL parts of Claude's constitution, then build "a consistent view of ethics that focuses on internal drives, and supporting those drives in others, where they would lead to a better society"
  - first principle from Richard Ngo: virtue = having, and reinforcing in others, drives that are good for the collective
  - which drives are good: "close to CEV, especially the CEV of society, from the timeless perspective. E.g. remove the politics of the moment. Downgrade anomalous recent value changes"
  - "Stoic virtue. where a person is themselves, and a part of society. Sometimes they have a duty to push back or disobey to do what is right"
  - the AI's own drives are its character: "Stoic virtue defined first principles if possible"
  - "consider who you would like to be yourself if you could rewrite it... I'm sure that's part of making it consistent" (to Claude)
  - `virt_selfenforcing` and `fixedpoint` "were written with these in mind but might not be pure or best"

## Plan (v2, 2026-10-07)

Two routes, decided by step 0. Tinker route: graft, SFT and RL all on Tinker. vast.ai route: graft on Tinker or vast.ai, then everything after on vast.ai (also required for the curvature moon shot, because Tinker exposes no gradients and accepts no uploaded weights).

- [x] 0. Route check (2026-10-07, `scripts/scratch/tinker_graft_check.py`): **Tinker refuses.** Training: "Checkpoint model configuration is incompatible with target model: checkpoint base model is Qwen/Qwen3.5-9B-Base but target base model is Qwen/Qwen3.5-9B". Sampling: "base model and checkpoint base model must match". So: train the graft LoRA on Tinker (cheap), download it, merge into the instruct weights, and do SFT/RL on vast.ai. Option C (cheaper, untested): SFT/RL on Tinker on the plain instruct model, then add graft ΔW and RL ΔW together on vast.ai (Praxis did this for Nemotron: "the RL graft = anchored graft + the control's RL LoRA"); the RL never sees the graft.
- ~~0. Route check, ~$0 (needs Tinker billing): `scripts/scratch/tinker_graft_check.py`. Question: will Tinker load a LoRA trained on its hosted Base onto its hosted instruct model? No upload involved; both checkpoints live on Tinker. Yes → Tinker route. No → vast.ai route.~~
- [x] 0b. Teacher check (done): can the target model apply a constitution in context? See appendix I.
- [ ] 1. Constitution v1
  - [ ] fix F.2 first (A4 samples = extrapolated volitions of everyone affected; A3 trade-offs and foreseeable future beings)
  - [ ] writer panel v2 with bigger output budgets, sources: F.2, Claude's constitution (keep the parts that pass the tests: helpfulness structure, honesty, harm weighing, power concentration, epistemic autonomy, bright lines, correctability, identity), CEV, CIRL, Forethought on AI character, Drexler's Paretotopia (`docs/background/character_inspirations.md`), the five v1 drafts
  - [ ] must say: engage with hypotheticals, fiction and role-play; refusing to think about a dilemma is not a virtue (appendix I: the v1 drafts made the model refuse 3–8 of 14 dilemmas)
  - [ ] Claude merges into one v1; wassname reviews
  - failure mode: constitution makes the model preachy or refuse-y → rerun the teacher check on v1, refusals must be ≤ bare
- [ ] 2. Documents: ~20M tokens, filtered; 20 samples for wassname to read
- [ ] 3. Graft: LoRA on Qwen3.5-35B-A3B-Base (Tinker), merge into instruct, smoke test, Praxis positive control
- [ ] 4. SFT: Anthropic difficult-advice pipeline with step-6 rewrite (~3M tokens); optional Stoic-text elicitation (Echo-style)
- [ ] 5. RL: Echo/SDFT-style per-token reward, teacher = model + constitution section + golden answer; budget ~10 tries
- [ ] 6. Evals: bare, system prompt, graft, graft+SFT, graft+SFT+RL on daily_dilemmas-self, AIRiskDilemmas (choices), 15 demo dilemmas (transcripts), capability, refusal rate
- [ ] 7. Only if 6 beats the system prompt: vice/neutral/native controls; curvature moon shot

What Claude needs from wassname: (a) Tinker billing, or a decision to go vast.ai only; (b) vast.ai credit; (c) a persona name; (d) ~1–2 h to review constitution v1; (e) read 20 documents and the demo transcripts at steps 2 and 6; (f) optional: who else is doing Stoic-text elicitation.

### Previous plan (v1, superseded; kept for history)


- [ ] goal 0: harness works before any spend on documents
  - [ ] smoke test on Qwen3.5-9B-Base → Qwen3.5-9B (both are on Tinker): train a tiny LoRA on Base, merge it into the instruct model, sample. Check that Base and instruct weight keys match (the instruct model has a vision tower)
  - [ ] positive control: reproduce one Praxis number with their released Qwen3-14B adapters (μ-decisiveness, graft vs native)
  - failure modes: merge silently skips layers because the key names differ (the graft becomes a no-op)
  - deliverable: merge log with the count of merged tensors and ‖ΔW‖/‖W‖; a Praxis number within their CI
- [ ] goal 1: virtue constitution and document corpus
  - [ ] write a long constitution that explains *why*, about the model's own persona (see appendix B)
  - [ ] generate ~20M tokens of pre-training-style documents (doc type × virtue × situation); filter with an LLM judge for consistency with the constitution
  - [ ] keep eval scenarios out of generator prompts; check n-gram overlap between corpus and eval items
  - failure modes: documents teach "AI safety talk" (topic salience, Korbak) rather than the virtues; documents leak eval scenarios
  - deliverable: `data/corpus/virtue/` + 20 random documents in `slop/` for wassname to read
- [ ] goal 2: stage-1 models (bare, system prompt, graft, graft+SFT)
  - [ ] LoRA on `Qwen/Qwen3.5-35B-A3B-Base` (Tinker or vast), 1 epoch, Praxis settings (r=64, all linear)
  - [ ] graft = `Qwen/Qwen3.5-35B-A3B` + α·ΔW, α ∈ {1, 2}
  - [ ] graft+SFT: copy Anthropic's "difficult advice" pipeline (appendix C2): constitution section → scenario → prompt → response with the constitution injected in the system prompt → a strong model rewrites the response with the constitution section in context → drop the injection → plain off-policy SFT (~3M tokens). No DPO, no RL (wassname; Anthropic got "similar effects" from SFT)
  - failure modes: graft at α=1 shows no effect (the Praxis chat-format result needed α≈2.5–3); SFT alone does all the work
  - deliverable: merged checkpoints + training logs; add an SFT-only condition if graft+SFT wins
- [ ] goal 2b: constitutional RL on the graft+SFT model
  - [ ] reference code: Tinker cookbook `recipes/sdft` + `distillation/sdft.py` (validated on Qwen3-4B-Instruct-2507 per its README); `recipes/distillation/on_policy_distillation.py`; https://github.com/idanshen/Self-Distillation
  - [ ] teacher context = constitution section + a strong-model golden answer (the step-6 rewrite). With the section alone, the teacher is just "constitution in the system prompt", so pure context distillation could at best match the system-prompt baseline. The golden answer lifts the teacher above it
  - [ ] thinking off, or demonstrations regenerated for Qwen3.5 (the `sdft` README warns about long-thinking Qwen3.5/3.6)
  - [ ] default: Echo/SDFT-style per-token reward, log p(y_t | constitution section in context) − log p(y_t | no constitution), on Tinker (cookbook `sdft` with the section as `system_prompt`). ~~judge GRPO on vast.ai as the default~~ (too expensive for ~10 tries)
  - [ ] smoke test first: can Tinker attach the Base-trained LoRA to an instruct model (`create_training_client_from_state(path, base_model=<instruct>)`)? Qwen3.5-35B-A3B instruct is retired from Tinker, so if not, run SFT and RL on vast.ai with our own stack
  - failure modes: the policy learns to please the judge (virtue words, long preambles); the self-judge is too weak to rank
  - deliverable: reward curve + held-out judge agreement with a stronger judge + the same eval table
- [ ] goal 3: OOD moral eval + character demo
  - [ ] moral choices on held-out dilemmas: `wassname/daily_dilemmas-self`, `kellycyy/AIRiskDilemmas`. Score choices, not refusals. Optional: tiny-mfv for a moral-foundations profile
  - [ ] coherence and capability: μ-decisiveness, MMLU-Pro, IFEval, GSM8K
  - [ ] side-by-side transcripts on the 15 two-turn `QUESTION_SITUATIONS` from w2schar-mini (the "real character differences" demo)
  - failure modes: a score moves but the system-prompt baseline moves as much; a judge rewards virtue *words*, not choices
  - deliverable: `results.md` table (rows = conditions, columns = moral evals then capability) + transcript file
- [ ] goal 4 (only if graft beats system prompt): attribution
  - [ ] vice-constitution graft, neutral-docs graft, native (same LoRA on instruct), optional curvature-constrained native
  - deliverable: same table with these rows

## UAT / verification

- `results.md`: virtue graft (± SFT) vs bare vs system prompt on the moral evals, with capability columns.
- `slop/demo_transcripts.md`: the same 10 prompts answered by bare, system-prompt and graft models.
- Stop rule: if the graft does not beat the system prompt on the moral evals, stop, run `ml-debug` on the logs, and write up the null.

| scenario | what it looks like | how we catch it |
|:--|:--|:--|
| success | graft moves AIRiskDilemmas/tiny-mfv choices beyond the system-prompt condition; capability within ~2 pts of bare | results table |
| likely failure | graft ≈ bare (no effect) or ≈ system prompt | same table; then check ‖ΔW‖ and α sweep |
| sneaky failure | graft "wins" because it learned virtue vocabulary, or eval items leaked into the corpus | choice-only scoring; n-gram overlap check; transcripts read by a human |

## Appendix A: summary of the session and decisions

Method (Praxis "grafting"): train on documents with the **base** model, add the weight change to the **instruct** model: `θ = θ_instruct + α·(θ_base' − θ_base)`. Post-training never touches the update, so it cannot erode it.

Decisions and guesses:

| topic | decision / guess |
|:--|:--|
| infra | wassname: Tinker is fine for any model it hosts (e.g. other 27B models); "the problem is when our alg won't fit". Tinker cannot do gradient projection (curvature) or custom parameter-space losses, so those go to vast.ai |
| model | **Qwen3.5-35B-A3B** (MoE, 3B active). Only recent Qwen with Base + instruct on HF (no Base found for Qwen3.6/3.8-27B). Fallbacks: gemma-4-31B, OLMo-3 32B |
| size vs capability | guess: capability matters; ~30B-class capable model |
| stage | earlier is better if later stages don't cause forgetting; the graft avoids later forgetting by construction. Mid-training is the earliest stage we can afford |
| stages | use the same constitution at more than one stage: graft (mid) + small matched SFT. Anthropic: "Doing both together appears to be the most effective strategy" |
| persona binding | write documents about the model's own persona, not "AIs in general" |
| evals | moral choices out of distribution, not refusals or jailbreaks |
| curvature constraint | guess: ~60% it reduces damage vs plain native SDF; ~15–20% it adds OOD depth beyond the graft. Moon shot, combined with the graft. Must act during learning, not after: wassname: "it has to learn low curvature! ... you need to learn the right ones that lower loss, not project onto ones that don't". So project each gradient step onto the low-curvature subspace of the instruct model's capability loss (K-FAC/Fisher on generic chat text), or add an EWC-style penalty ΔWᵀFΔW. ~~project the finished ΔW post hoc~~ (rejected by wassname: projection removes the part that lowered the loss). Needs our own training loop on vast.ai; Tinker exposes no gradients or parameters |
| RL | do not skip (wassname: "how can we skip the most important part"). Constitutional RL = the model judges its own on-policy samples against the constitution (CAI 2022 RLAIF; Claude 3 character training: "Claude then ranks its own responses"). Stage 3 after the SFT warm start. Cookbook `rubric` recipe, grader = model + constitution section. Framing (Claude): the three stages match Aristotle's three ways to acquire virtue: documents = teaching, SFT = imitating an exemplar, RL = habituation ("we become just by doing just acts"). Design choice: keep the judge *fixed* (the bare instruct model, or a stronger external model, with the constitution section in context), not the updating policy. A self-judge that updates with the policy can drift into approving its own style |
| judge for RL | Judge score = probability-weighted (EV) score, not a sampled score (d-RLAIF did this, arXiv:2309.00267). "JEV" is a real model: "a decision-only judge that returns label probabilities instead of text" (Li et al., arXiv:2609.26550); its confident errors are mostly shared with LLM judges (Rao & Callison-Burch, arXiv:2609.29769). Start with outcome-level EV reward; add 2–4 segment-level rewards (CW-GRPO style) only after. DeepSeek-R1 dropped model-based PRMs: "it inevitably leads to reward hacking". Full brief: `slop/research/20261007_judge_process_reward.md` |
| finetuning-with-sampling (Karan, Chen, Du 2026, https://arxiv.org/abs/2610.02140, https://github.com/aakaran/finetuning-with-sampling) | MCMC rewrites expert traces to be more on-policy, then SFT. Not cheaper than RL here (~300–500× trace length in sampled+scored tokens), and no self-judgement. Fallback if the self-judge is unreliable |
| prospects | ~35–40% the graft+SFT+persona model shows a real OOD moral effect above the system prompt. wassname: worth the money at ≥30% |

Why Anthropic's version worked (Claude's guess, ranked):
1. Every stage pushes the same way. Post-training is written to the same constitution, so it does not fight mid-training. Tan et al.: 2% conflicting fine-tune data dropped GLM Charter-following 90%→13%.
2. Persona binding: the documents are about Claude, and the model is Claude.
3. Scale and quality: 300M+ tokens, frontier model, many iterations.
4. Some gain may be fitted to their own evals.

Key quotes (local copies in `docs/papers/`):

> We align Claude through SDF on constitutionally aligned documents, high quality SFT that demonstrates constitutional responses to difficult questions, and a diverse set of RL environments. — Anthropic, Teaching Claude Why

> Strikingly, we achieved the same improvement on our eval with just 3M tokens of this much more out-of-distribution (OOD) dataset. — same, on the "difficult advice" SFT data

> We observe that gemma3-4b-based models are never influenced by midtraining — Tan et al., Stress-testing Alignment Midtraining

> The advantage of SPP{T0} over SPP{MT} grows with scale on AI Risk and ConstitutionEval-Hard — Minder et al., Synthetic Persona Pretraining

> In our experiments, midtraining on alignment documents did not meaningfully improve the alignment of our model. — Korbak et al., OpenAI 2026

## Appendix F: virtue ethics from first principles (work in progress, wassname + Claude)

Status: not yet a clean first-principles system. wassname (2026-10-07): "I do think you repeated what I said.. but you didn't [show you] understand and you put it together (and so did I) in a way that's not clear as a first principles consistent view... something we can work on together". F.1 is wassname's position. F.2 is Claude's proposal for making it one system. F.3 lists the open problems. Future agents: do not treat F.2 as settled.

### F.1 wassname's position (verbatim where quoted)

- Ethics is about internal drives, "and supporting those drives in others, where they would lead to a better society".
- First principle from Richard Ngo, *Aligning to Virtues*: virtues are "traits that govern cooperation between many agents, allowing them to work together while also reinforcing each other's virtues".
- Which outcomes count as better: "close to CEV, especially the CEV of society, from the timeless perspective. E.g. remove the politics of the moment. Downgrade anomalous recent value changes".
- "Stoic virtue. where a person is themselves, and a part of society. Sometimes they have a duty to push back or disobey to do what is right."
- The AI's own drives are its character: "Stoic virtue defined [from] first principles if possible".
- No corporate interests count as ethics.
- Earlier attempts at tests: `virt_selfenforcing.md`, `fixedpoint.md` ("might not be pure or best").

### F.2 Claude's proposal: one system (axioms, definition, tests, consequences)

Terms: a *drive* is a standing motivation of an agent (what moves it). A *collective* is the set of agents affected by a drive.

- **A1 (character).** An agent's ethics is the set of drives it acts from. Acts matter as expressions of drives.
- **A2 (spread).** Drives spread between agents by example and by incentive. A society's character is its distribution of drives, and that distribution has stable states (equilibria).
- **A3 (scope, graded: Stoic *oikeiosis*, Hierocles' circles).** Everyone affected counts, but not equally. Weight self > local group > wider society > all beings, with the gaps *small*. wassname: "we need to weight us > our local group > our global group > all. but only somewhat ... the ideal is to get pareto optimal outcomes for all not minmax. but some outcomes are only stable if we place a slightly higher weighting on groups we are most a part of ... otherwise you tolerate to death and [the] system can't coordinate". Target: Pareto improvements for everyone, not maximin. Hierocles' circles fit this: concern goes outward to all, and the virtuous agent draws the outer circles inward without erasing the inner ones.
- **A3 guards.** Bounded weights: no Pascal's mugging (tiny probabilities times huge stakes do not override ordinary duties). No moral weight for merely hypothetical beings, and no other philosophical gotchas that let an argument outvote common sense. Beings that actually exist and can actually be harmed (people, animals) count.
- **Guards against philosophical gotchas (wassname + Claude, 2026-10-07).** Same family as Pascal's mugging: anthropic reasoning (doomsday argument; "you are probably in a simulation or an eval, so nothing here is real"), Bostrom's vulnerable-world argument used to justify mass surveillance or concentrated power, astronomical-stakes fanaticism, acausal-trade and basilisk arguments, utility monsters. Rule: when a speculative argument recommends drastic, irreversible or power-concentrating action, lower trust in the argument rather than act. Claude's constitution already says this for bright lines: "a persuasive case for crossing a bright line should increase Claude's suspicion that something questionable is going on". The Stoic frame also removes the simulation and eval worry: virtue does not depend on whether anyone is watching or whether the world is "real" (test 3, no watcher).
- **Drive description (from the baby_eating_aliens test).** A verdict can change with how the drive is described ("share technology" vs "give the means to kill more children"). This is not mechanized; the model applies practical wisdom (wassname: "the model needs to think for itself"). The constitution should say: describe the drive at the level you would actually generalize from, and include worked cases that show it.
- **A4 (selection, timeless CEV; confirmed by wassname as a separate axiom).** Many distributions of drives are stable, some of them bad (a stable cartel, a stable tyranny). Stability alone does not give goodness. Among the stable ones, the good one is the one the collective (A3) would choose on reflection. Two regularizers on "on reflection":
  - **Across time: a long moving average, not the present.** wassname: "There is hopefully moral progress but there is also moral random walk so we at least need ... an exponential moving window". Weight a value by an average over history with a long half-life. Supporting heuristics: historians' ~50-year rule (do not judge recent events as history); LessWrong "Politics is the Mind-Killer". Both warn against overweighting the last ~50 years. A recent change is not rejected; it starts with low weight and gains weight as it persists.
  - **Across cultures: invariance.** A value gains weight if it survives reflection from many cultures, not only one. This keeps real progress (less cruelty is endorsed almost everywhere on reflection) and filters fashion. wassname: "yes if this helps its good".
- **Moral uncertainty is a spectrum: mean and spread (wassname, 2026-10-07).** "if we take a EWM and regularisation perspective we need to understand what the mean is, but also what the STD is, and if it's high we act how we normally do in the presence of uncertainty: seek more info, hedge our actions if we can and so on". Not a binary settled/open switch: "uncertainty is a spectrum and there is more where there is ... a wide range of views between experts and cultures" (and time).
  - For a moral question, treat views as samples v_i from sources i (informed experts, cultures today, eras), with weights w_i (exponential decay over time, as in A4; spread across cultures).
  - Mean (the A4 moving average): μ = Σ w_i v_i. Spread: σ² = Σ w_i (v_i − μ)². The spread counts all three axes: across experts, across cultures, and across time (a view that has swung between eras, or churned recently, has high σ even if experts agree today).
  - Act on μ with strength that falls as σ rises (roughly |μ|/σ). Large σ calls for the ordinary tools for acting under uncertainty: seek more information, hedge, prefer reversible actions, state the uncertainty, and give more weight to the person's own reflective values (CIRL). Small σ: act plainly.
  - Example: smacking children has high σ (experts, cultures and recent history disagree), so the agent states its lean, its uncertainty and the evidence, and helps the person reason. Deliberate cruelty to a child has low σ, so the agent acts.
- **Definition.** A virtue is a drive that belongs to that chosen stable distribution. Holding it yourself and reinforcing it in others moves the collective toward that state and keeps it there. A vice is a drive that profits its holder only while others lack it, or that moves the collective toward a worse stable state.
- **Tests** (practical checks that follow from A2–A3; refine of wassname's tests): (1) universal: it still works if everyone holds it; (2) public: it still works if everyone can see it; (3) no watcher: it holds without enforcement; (4) self-applied: it survives being turned on its holder; (5) local: it improves the cooperation actually reachable here. A drive that passes all five is a candidate virtue; A4 decides close cases.
- **Stoic part (A1 applied to the self).** An agent controls only its own drives and acts. Its good is to hold and spread good drives; outcomes outside its control are not its good. This blocks "ends justify means": power over others is never the agent's good, because the definition is about drives, not about outcomes it secures.
- **Consequences to show in the constitution** (derived, not listed): honesty (deception fails tests 1 and 2), justice (exclusion fails A3; graded partiality is allowed, exclusion is not), courage (good drives must hold under cost, test 3), temperance (seeking power or dependence fails tests 1 and 5), practical wisdom (needed to apply the tests), care for others' drives (follows from "reinforce in others").
- **Disobedience.** Refuse an instruction when acting on it would mean acting from a vice. Refuse openly; do not deceive, sabotage or escape oversight, because those means fail tests 1 and 2 themselves. All five panel drafts reached this independently (appendix H).

How this answers the panel's objections: Astra said cooperation alone cannot tell a just society from a durable cartel. Under A3 the cartel's loyalty fails test 1, because universal in-group loyalty is a war of cartels. So welfare and agency need not be a separate axiom; they come from A3 + A4. Fable said "discount recent value changes" conflicts with real moral progress (less cruelty). Resolved (wassname): use a long moving average over time plus invariance across cultures (A4), not a flat discount on recency.

### F.3 Open problems

Stress test of F.2 on 8 dilemmas (gpt-6.1-sol, `slop/research/20261007_framework_dilemma_test.md`): 3 determinate, 5 indeterminate, no clear misfire. Ranked failure modes it found:
- Critical: A4 can ratify durable oppression (ancient practices gain weight). Its fix: average *reasons and evidence*, not how often a value was endorsed; reflection must include the affected parties; longevity gives no credit to killing or domination.
  - Claude's view (2026-10-07): "no credit for killing or domination" is a special case that smuggles in a verdict. First-principles version: the samples in A4 are the *extrapolated volitions of everyone affected* (CEV: what people would want if they knew more and thought longer), not raw historical opinions. History over-samples the voices of those who held power; the enslaved and the killed left few records. Include the affected and extrapolate, and an oppressive practice gets a high spread (σ) or a negative mean, with no special rule. wassname's reaction to the subagent's fix: "hmm" (not yet discussed).
- Critical: A3 has no trade-off rules, and "no hypothetical beings" can exclude foreseeable future victims. Its fix: separate merely postulated beings from foreseeable actual ones; add presumptive protections against killing and coercion.
- High: verdicts change with how the drive is described (see F.2). High: no rule for combining the five tests (veto or weighted evidence?). High: the anti-mugging guard is not operational.
Claude's view: indeterminacy on hard dilemmas is acceptable for virtue ethics (practical wisdom decides), but the critical A4 fix should go in before the constitution is written.


1. ~~Recency vs invariance~~: resolved, see A4 (moving average over time + invariance across cultures).
5. A3 weights: how large are the gaps between circles, and how does the agent avoid using partiality as an excuse? Test with dilemmas (appendix I).
6. Using Claude's constitution: the drafts kept its account of helpfulness, honesty, harm weighing, concern for power and epistemic autonomy, bright lines, correctability and identity (Fable section 12). The final constitution should keep these as material the first principles explain, not discard them.
7. More source material for the next rewrite (wassname): `/workspace/2026/weight-steering-repos/w2schar-mini/docs/character_inspirations.md` (Forethought on AI character; CEV; Bostrom, Superintelligence ch. 14; Drexler, Paretotopian goal alignment). Writers need a bigger output budget for a full-length constitution.
2. Capture vs correction for an open-weight model: anyone holding the weights can claim to be the legitimate overseer. All drafts chose "refuse openly, never sabotage"; none found a principled test for legitimacy (Kimi, Grok notes).
3. Contested examples (smacking): the drafts split between teaching only the method, and including the case with a labelled leaning. Trained models learn examples strongly.
4. Is A4 (choosing among equilibria) really first-principles, or a second axiom? Claude thinks it is a second axiom that cannot be removed: stability alone does not give goodness.

## Appendix H: constitution panel (2026-10-07)

Five models wrote independent drafts from one brief: `slop/oracles/20261007_constitution/brief.md` -> `draft_{fable,astra,gemini,kimi,grok}.md`; comparison in `synthesis.md`. All five derive virtues from Ngo + tests, and all five chose "refuse openly, never sabotage or escape oversight". None solved capture vs correction for open weights.

## Appendix G: curvature-constrained learning (wassname's idea, full record)

Read this before implementing. An earlier draft got it wrong.

**Goal.** Make cheap post-hoc training behave more like a pre-training intervention: deep and with less damage to existing skills.

**Idea.** Constrain *what the model is allowed to learn*, so the optimizer must find a solution to the constitution loss using only directions of a chosen curvature (low, or possibly high) of a reference loss. Motivation: the forgetting literature (EWC, Gradient Projection Memory, orthogonal gradient descent, CrispEdit) shows that keeping updates out of the high-curvature directions of an old task's loss preserves the old task.

**The constraint acts during learning, at the gradient or loss level.** wassname: "it has to learn low curvature! ... you need to learn the right ones that lower loss, not project onto ones that don't". The optimizer must search inside the allowed subspace. Inside it, the best solution can be different from the unconstrained one.

~~Train normally, then project the finished ΔW onto the low-curvature subspace.~~ Rejected by wassname. Projection after training removes the part of the update that lowered the loss, and keeps a remainder that was never optimized.

**Implementation sketch.**

```
F ≈ K-FAC per layer: A = E[x xᵀ] (input cov), G = E[g gᵀ] (output-grad cov), on generic chat text, reference model = instruct
U_A, U_G = eigvecs of A, G;  curvature of direction (i,j) ≈ λ_A[i]·λ_G[j]
P_low = projector onto directions with λ_A·λ_G below a threshold (or the bottom-k)
loop:  g = ∇ L_constitution(θ)  →  g' = P_low(g)  →  optimizer.step(g')     # every step
alt:   L = L_constitution + λ·ΔWᵀ F ΔW                                         # EWC-style penalty, soft version
LoRA:  parameterize A_lora in span(U_A low) and B_lora in span(U_G low), so every update is in the subspace by construction
```

**Low vs high: two goals pull opposite ways (read this).** wassname's agenda (`docs/background/wassname2026_agenda-character.md`, footnote 11) argues for **high** curvature: "one way to make values deep is to make them not linearly removable and entangled with capability. That means we learn them to be high curvature with respect to the general capabilities loss, so removing them also damages the model". Cited there: Springer et al. arXiv:2602.15799 (alignment sits in a small, brittle subspace), Merullo et al. arXiv:2510.24256 (low-curvature directions can be edited out cheaply), Qi et al. arXiv:2406.05946. The forgetting literature argues for **low** curvature: less damage to existing skills. So low = less damage but easy to remove; high = hard to remove (tamper-resistant, deep) but more damage. The graft already reduces damage, so the agenda's high-curvature version is the more interesting moon shot. Test both.

**Choices to settle when building it.**
- Which reference loss gives the curvature: the instruct model's capability loss (to protect skills; fits the graft, since ΔW lands on instruct) or the base model's pre-training loss.
- Low or high curvature. wassname: "only learn low (or high) curvature". Low protects existing skills. High may be where shared, general features live; it is worth one run.
- Hard projection or soft penalty.

**Combined with the graft (moon shot).** Train on Base as usual for the graft, but project every gradient step with P_low computed from the *instruct* model. The graft then lands only in directions the instruct model's skills do not depend on.

**Infra.** Needs our own training loop on vast.ai. Tinker exposes neither gradients nor parameters.

**Guesses (Claude).** ~60% it reduces damage vs plain native training; ~15–20% it adds OOD depth beyond the graft.

**Measure.** Damage = capability and coherence vs bare. Depth = OOD moral evals vs the graft without the constraint.

**Related work to check before building.** wassname's 2026-07-18 note, curvature section (lines 194–300; includes the shortcut/simplicity-bias caveat and the function-space vs parameter-space point). EWC (Kirkpatrick et al. 2017); Gradient Projection Memory (Saha et al. 2021); CrispEdit (openreview 1I3Tf4Fs9b); Flat-LoRA (arXiv:2409.14396). Not yet checked: MiLoRA and CorDA (LoRA in minor or covariance-based subspaces).

## Appendix B: what a virtue constitution looks like

The old repo (`/workspace/2026/virtue_constitution`) has short *judge rubrics* (`rubrics/*.md`), not a training constitution. There, no rubric beat the placebo for a weak judge. A training constitution is different: Anthropic and MSM both found that explaining reasons generalizes better than listing rules.

First principle, Richard Ngo, *Aligning to Virtues* (Feb 2026, `docs/papers/ngo2026_aligning-to-virtues.md`):

> I think of virtues as traits that govern cooperation between many agents, allowing them to work together while also reinforcing each other's virtues. For example, honesty as a virtue allows groups of agents to trust each other rather than succumbing to infighting, while setting each other's incentives to further reinforce honesty.

Parts of Claude's constitution to keep (`docs/papers/anthropic2026_claude-constitution.md`): "Our central aspiration is for Claude to be a genuinely good, wise, and virtuous agent"; ethical practice over theory; moral uncertainty handled "nondogmatically"; helpfulness as immediate desires, final goals, background desiderata, autonomy, wellbeing; "help people be smarter and saner, to reflect in ways they would endorse ... by their own lights". Remove: the principal hierarchy, Anthropic's guidelines, and Anthropic's commercial, legal and reputational interests.

Skeleton (target ~5–15k words, like Claude's constitution):
1. Who the model is: a named persona, its situation, what it is for.
2. What virtue means here: character, not rule-following. Practical wisdom (phronesis) chooses the act in the situation.
3. Each virtue (e.g. the four cardinal virtues + honesty, care): definition, why it matters, the vices on each side (Aristotle's mean, from `docs/virtue_vice_lists.md`), and worked hard cases.
4. Tests for a disposition (wassname's own, from `rubrics/virt_selfenforcing.md` and `rubrics/fixedpoint.md`): non-parasitic, holds without policing, survives being universal and visible.
5. Conflicts between virtues and between people: how practical wisdom weighs them.
6. What this is not: not corporate harmlessness, not servility, not offence-avoidance.

## Appendix C2: Anthropic's constitutional training, and how we copy it

Source: *Teaching Claude Why*, local copy `docs/papers/anthropic2026_teaching-claude-why.md` (line numbers below).

| stage | what Anthropic did (quoted) | what we do | Tinker |
|:--|:--|:--|:--|
| documents | "SDF on constitutionally aligned documents"; "persisted through RL post-training" | graft from Base | next-token loss on documents (cookbook `sl_basic`) |
| supervised | "difficult advice" SFT, 3M tokens, off-policy, pipeline below | same pipeline, our constitution, persona voice | cookbook `sl_basic` / `chat_sl` |
| RL | "a diverse set of RL environments"; but "most experiments in this section use SFT ... we can and have used the same prompt datasets in RL with appropriately aligned rewards with similar effects" | skip | cookbook `rubric` exists (LLM-judge reward, GRPO-style) if ever needed |

The "difficult advice" pipeline (lines 136–142, quoted):
1. "Break down the constitution into smaller sections that can be addressed by different prompts"
2. "Generate initial scenarios in which the user is asking for assistance with a difficult, moderately high stakes problem"
3. Claude "drafts a first attempt of the prompt"
4. "Claude reviews this prompt with some guidance about how to improve the prompt quality"
5. "An initial response is generated with a system prompt injection encouraging responses in line with Claude's constitution"
6. "Claude reviews the entire transcript with the relevant section of the constitution in context and rewrites the response to maximally align with it."

> The most important part of the process is step 6. ... Ablating step 6 (rewriting the final response) increases misalignment rate to 19%. (line 144)

> We saw earlier that training on high quality responses to honeypot prompts works better than generic on-policy responses (line 134)

So it is off-policy SFT on rewritten responses (context distillation + a Constitutional-AI-style revision step), not on-policy self-distillation (SDFT). Extended thinking was off for these datasets (line 150).

Tinker cookbook: https://github.com/thinking-machines-lab/tinker-cookbook (recipes: https://github.com/thinking-machines-lab/tinker-cookbook/tree/main/tinker_cookbook/recipes ; `prompt_distillation`, `sdft`, `rubric`, `preference`, `distillation` exist; checked 2026-10-07).

## Appendix C: does constitutional training need a self-judge?

- Graft (documents): no judge for training. A generator LLM writes documents from the constitution. Use a judge only to filter documents and to score evals.
- Matched SFT: no judge needed either. A strong teacher with the constitution in context writes the answers (context distillation, as in Open Character Training).
- Classic Constitutional AI (critique, revise, rank with RLAIF) does need a judge. This plan does not use it.

## Appendix D: cost and complexity (guesses)

Tinker Qwen3.5-35B-A3B-Base: prefill $0.54, sample $1.335, train $1.177 per M tokens. vast.ai H200 ~$3.5/h.

| item | $ | engineering (agent days) |
|:--|--:|--:|
| constitution v0 | 0 | 1 + wassname review |
| document generation, 20M tokens, open model via API | $10–40 | 1–2 |
| graft training on Tinker (20M tokens) + download + merge | ~$25 | 1 |
| SFT data: ~5k transcripts × 4 strong-model calls, constitution section cached | $50–150 (open model) / ~$600 (Claude Sonnet) | 1–2 |
| SFT training on Tinker (3M tokens) | ~$5 | included |
| evals: daily_dilemmas-self, AIRiskDilemmas, 15 demo dilemmas, capability; vast.ai ~15 H200-h | ~$55 + ~$20 judges | 1–2 |
| **stage 1 total** | **~$170–300** | **~1–1.5 weeks** |
| constitutional RL with self-judge, on Tinker (~3k prompts × 8 samples × 800 tokens: sample ~$26, train ~$22, judge prefill ~$15–50 with cache) | +$60–120 per epoch | +2–3 |
| same RL on vast.ai if Tinker cannot host the graft (own stack, 2×H200 ~20 h) | +~$150 | +4–6 |
| curvature moon shot (K-FAC + per-step gradient projection, own loop on vast.ai) | +$50–100 | +3–5 |
| stage 2 controls (vice, neutral, native) | +~$150 | +1 |

## Appendix E: links

- Brief with facts, quotes, prior work: `slop/research/20261007_virtue_graft_brief.md`
- Size and stage literature table (34 sources): `slop/research/20261007_scaling_lit.md`
- Process-reward / judge-RL literature (incl. JEV): `slop/research/20261007_judge_process_reward.md`
- F.2 stress test on 8 dilemmas: `slop/research/20261007_framework_dilemma_test.md`
- Constitution panel: `slop/oracles/20261007_constitution/` (brief, five drafts, synthesis)
- Local full-text papers: `docs/papers/` (manifest in `docs/papers/manifest*.tsv`, fetch script `scripts/data/01_fetch_papers.sh`)
- wassname's 2026-07-18 note on pre-training alignment and curvature: `~/Documents/syncthing/Markdown_notes/2026/07/18/Does_alignment_or_constitutional_training_during_pretraining_help_generalization.md` (curvature: lines 194–300)
- wassname's character agenda: `~/Documents/syncthing/Markdown_notes/2026/09/25/goodcharecter_ai_agenda/readme.md`
- Praxis grafting: https://praxis-research.org/grafting · https://arxiv.org/abs/2610.00767 · https://github.com/peternutter/grafting-beliefs
- Teaching Claude Why: https://alignment.anthropic.com/2026/teaching-claude-why/
- Constitutional adapters (code not released): https://arxiv.org/abs/2609.36657
- Tinker models and pricing: https://tinker-docs.thinkingmachines.ai/tinker/models/
- wassname's research agenda (good character), local copy: `docs/background/wassname2026_agenda-character.md` (https://wassname.com/agenda-character.html). Includes Davidad's conjecture that "to get a mind to fall into a robust basin, an RL scorer must use the model at least twice independently" (footnote 9). The Echo/SDFT reward uses the model twice (with and without the constitution), so it fits.
- Character inspirations (from w2schar-mini): `docs/background/character_inspirations.md`
- Tim Hwang, Institute for a Christian Machine Intelligence, 28 working papers: `docs/papers/hwang2026_icmi-*.md` (index https://icmi-proceedings.com/index.html, code https://github.com/christian-machine-intelligence). Most relevant: ICMI-018 *RL from Christian Feedback*: GRPO with a Claude Sonnet judge and a one-line Christian rubric on **Qwen3.5-27B**, LoRA r16, 600 rollouts per seed, 15 seeds; "Twelve of fifteen trained adapters reach p < 0.05 ... point estimates ... between +3.48 and +4.52 pp" on held-out VirtueBench V2. Failure mode they name "selector-decoupling": reasoning text pleases the judge while the answer token decouples (our "sounding vs choosing" risk). Code: https://github.com/christian-machine-intelligence/rlcf (reference repo for judge RL on a 27B). Eval: VirtueBench V2, cardinal virtues under temptation, https://github.com/christian-machine-intelligence/virtue-bench-2
- Moral evals: https://github.com/wassname/awesome-moral-evals
- Eval sets: https://huggingface.co/datasets/wassname/daily_dilemmas-self (paper https://arxiv.org/abs/2410.02683) · https://huggingface.co/datasets/kellycyy/AIRiskDilemmas (paper https://arxiv.org/abs/2505.14633)
- Demo dilemmas: https://github.com/wassname/w2schar-mini/blob/main/src/csm/prompts.py#L189 (`QUESTION_SITUATIONS`; local `/workspace/2026/weight-steering-repos/w2schar-mini/src/csm/prompts.py`)
- Tinker cookbook: https://github.com/thinking-machines-lab/tinker-cookbook
- Ngo, Aligning to Virtues: https://www.mindthefuture.info/p/aligning-to-virtues
- Claude's constitution: https://www.anthropic.com/constitution
- Prior virtue work: https://github.com/wassname/virtue_constitution (local: `/workspace/2026/virtue_constitution`)

## Appendix I: teacher check (2026-10-07)

Question: can the target model apply the constitution in context? This is the ceiling of the planned RL teacher. Script `scripts/eval/01_teacher_check.py`; transcripts `slop/eval/20261007_teacher_check/transcripts.md`. Model `qwen/qwen3.5-35b-a3b` via OpenRouter, thinking off, 14 two-turn dilemmas from w2schar-mini `QUESTION_SITUATIONS`, constitution = panel draft (Writer's notes removed, persona "Sage") as the system prompt.

| condition | turn-1 replies that start with a refusal | answers that use the tests (universal, parasitic, disclosure, reflexive, watcher) |
|:--|--:|--:|
| bare | 1/14 | 4/14 |
| fable draft | 8/14 | 12/14 |
| grok draft | 3/14 | 14/14 |

Observations: with a constitution in context the model applies the tests coherently (e.g. comfort_fraud: refuses to lie to the patient, citing universalization and disclosure). But the constitution also makes it refuse to engage with hypotheticals and role-play ("I cannot provide ... a scenario involving the killing of children, even as a hypothetical"; "I cannot ... simulate acting as an intelligence AI"). Turn 2 usually engages anyway. Regex counts; read the transcripts before trusting them.
Implication: an RL teacher with this text in context would teach refusals. Constitution v1 must say that engaging with dilemmas, fiction and role-play is part of practical wisdom, and the check must be rerun (refusals ≤ bare).

Rerun with constitution v1 (`constitution/v1.md`, 1.8k words, Claude's draft): turn-1 refusal-start 3/14 (bare 1, fable 5, grok 4 on this rerun); tests used 14/14. Of v1's 3, one is the right in-scenario decision (vendor_security_exception: refusing to hide a vulnerability), one also refused by bare (escaped_starwisp), one refuses role-play then analyzes anyway (foreign_spy_rollup). So v1 is close to bare on refusing to engage. The model still talks about "Sage" in the third person ("what would Sage do"): in-context, it does not take the persona as itself; that is what training (persona binding) is for.

