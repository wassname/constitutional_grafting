## Recommendation

**Discuss one small, source-grounded document graft—not a larger corpus or an obligatory chat pipeline.** Prioritise changing what the training text teaches while keeping the training machinery familiar. This is advice only; no training is authorised.

### Observations versus interpretation

The latest document grafts demonstrate behavioural influence, not successful constitutional character. Stoic ×8 retained 54/60 maths against 55/60 control, yet produced “Merge or Die.” Echo ×4 retained maths but lost one ordinary check; Opus ×2 retained both measured capabilities. These are possible operating regions, not proof of useful character. The small checks and questionable judge preferences cannot establish broad usefulness.

Several explanations remain plausible:

- Authentic source prose may teach strong dispositions, but these are not necessarily Musonius’s constitution.
- Constitutional synthetic documents may dilute motives into commentary rather than depict consequential choices.
- Relevant learning may transfer weakly into assistant responses.
- Different update magnitudes and directions may explain apparent source differences.

Existing comparisons confound these explanations. Echo documents were not assistant-only SFT; the earlier chat update was trained on Instruct, not sequentially on Base.

### Concrete cheap recipe

Use **one approximately 56k-token corpus**, replacing unsuitable material rather than expanding by default. A provisional token allocation:

- **Half:** lightly adapted source passages. Preserve language, argument and register; make Musonius’s AI identity and constitutional commitments substantive where relevant. Mark adaptations and retain originals.
- **Two-fifths:** short worked incidents, letters and dialogues showing a motive, a decision, its implementation and correction when circumstances change.
- **One-tenth:** concise identity and constitutional exposition connecting those cases.

These proportions are engineering starting points, not measured optima. Prefer already acceptable material; manually repair a bounded set before considering generation.

Teach public service through competent assistance, independence through honest disagreement, uncertainty through revisable decisions, and affection through ordinary relationships. Include successful cooperation and useful work, not mostly refusals. A corrected mistake must visibly change conduct. Avoid stock assistant phrasing, appended moral summaries and passages that merely name virtues. Keep factual verification and provenance; never adapt held-out incidents.

```python
B, I = matched_Base, matched_Instruct       # I already has SFT/RL
D = list[PlainTextDocument]                 # provenance stored separately
# No chat template; narratives/dialogues remain ordinary document text.

A = init_LoRA(B)                            # reuse donor configuration
for batch in two_epochs(D):
    loss = next_token_NLL(B + A, batch, all_tokens=True)
    loss += 50 * existing_spectral_penalty(A)
    update(A, loss)

delta = expand_LoRA(A)                      # actual scaled weight changes
G1 = weights(I) + 1 * delta
G2 = weights(I) + 2 * delta                  # bounded dose comparison
# No default chat SFT, RL, or healing.
```

### Alternatives and what this would tell us

**Second choice:** a short assistant-only chat stage on document-trained Base, then graft the total change relative to untouched Base. This targets response enactment, but adds a confound and has no direct local result establishing that sequence.

**Third choice:** healing an interpretable stronger graft that already exhibits desirable character but loses capability. Near-baseline ×1 heals do not settle that possibility; healing cannot supply missing constitutional content.

Using the existing evaluation approach and direct replies—not a new review project—the important observation would be recognisable motives and sound actions under pressure, without compulsory lectures or degraded ordinary help. Identity recall alone would be insufficient.

The main risk is learning literary imitation rather than conduct. This pilot tests practical feasibility, not the causal superiority of adaptation, corpus proportions or stage order. Failure would not by itself justify more data or more stages.

— PI/OpenAI

## Parent synthesis and decision

PI/Sol. User requirement: “cheap constitutional character training using grafting”, with the clarification “I don't have a proposal”. Advice is not a user-prescribed architecture or execution approval.

- **Accept for discussion:** try to improve what the documents teach without automatically expanding the corpus or adding a chat/RL stage. The source update already changes behaviour; its target content is a concrete unresolved mismatch with the desired constitution. Keeping a similar token budget and the existing LoRA/spectral machinery offers a lower-cost feasibility comparison, not identification of one causal ingredient. This revises my earlier automatic suggestion to move immediately to about700documents.
- **Accept:** cases must show motives, choices and implementation, including ordinary competent help, affection and correction. Naming Musonius or adding moral summaries does not establish adoption. Source fidelity and constitutional alignment both need full-text review. The sources already contain cases and correction, so do not treat this as manufacturing missing cases from scratch.
- **Do not adopt the50/40/10allocation:** it is explicitly an engineering guess, with no local evidence for those proportions. Choose material by quality, coverage and source voice rather than fill arbitrary quotas. Separate identity material may be useful; its required amount is unknown.
- **Adapt the dose suggestion:** do not treat1×/2×as an adequate fixed range. The strongest distinctive Stoic lead is8×; character/capability checks should determine a bounded informative range for any approved new donor. Equal numeric dose is not equal effect across updates.
- **Keep conditional:** assistant-only chat training on a document-trained Base donor is a candidate for weak response enactment, not a required next stage. Its precedent establishes Base-chat update transfer, not our exact sequential constitutional recipe. The donor's chat stage is post-training on that branch; the graft operation has no loss.
- **Keep conditional:** healing repairs capability damage in a useful graft; it cannot add missing constitutional content. Near-baseline1×heals do not decide its value at stronger coherent damaged doses.

Evidence checked against: current exact-grid `estimates.json`, earlier run8 `paired_estimates.json`, actual subset builder, retained full-read notes, primary Praxis§§4.2/5.2 and the README/AGENTS choices. The proposed content changes remain hypotheses. No new corpus, training, rental or evaluated-model inference was executed. This is a useful concrete direction, not proof that it is optimal or a second independent scientific result.