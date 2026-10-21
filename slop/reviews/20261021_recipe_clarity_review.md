## Reconstructed recipe

From `slop/plans/20261021_character_graft_recipe.md` alone:

- **Teacher** receives the constitution and generates training text. **Base** receives resulting documents, not the generation instructions. Recipe B additionally trains the donor on reviewed character replies.
- **Document loss** covers all document tokens. **Chat SFT** uses Instruct’s chat format but applies loss only to assistant replies. Both are next-token NLL. Echo’s conversational-looking text received document loss, **not chat SFT**.
- **Grafting** adds `strength × (trained donor − original Base)` to Instruct’s weights, without examples or gradients. Strength is not epochs.
- **Early:** document-train Base → graft onto Instruct → chat-train recipient.
- **Later:** chat-train Instruct separately → graft document donor’s update onto that recipient.
- **Latest/A:** document-train Base with spectral penalty → graft; no extra character chat training. Four subsets were alternatives.
- **Proposed B:** document-train Base → chat-train that donor → graft its combined difference from original Base once. Adding the document difference separately would count it twice. This exact sequential constitutional recipe remains untested; cited chat-only precedent does not validate it.
- **Healing:** optional post-graft capability repair when measurable damage coexists with interpretable character; unnecessary near baseline.

## Concrete changes

1. **Clarify adapter requirement.** Under “Two training operations,” “LoRA stores that change compactly” explains representation without explicitly requiring it. A fresh implementer could choose full fine-tuning from `document_train`. Say “Our document training uses LoRA.” This is a comprehension risk, not observed execution; an explicit implementation constraint would resolve it.
2. **Clarify B’s system context.** `Teacher.answer(Constitution, varied_user_requests)` does not specify whether `CharacterChats` includes the constitution as student-visible system context. State whether it does. Otherwise an implementer could train constitution-prompted behavior rather than the intended unprompted character.

Approval is clear: “not yet tested or approved” and “No new training is approved” prevent confusing completed comparison with execution readiness.

At the supplied 964-word count, this is concise, but code blocks/headings make two pages layout-dependent; one page is unrealistic. No lengthy expansion needed.

Parent resolution, PI/Sol: explicitly require LoRA for document training and the proposed chat stage. Explicitly remove teacher-only constitution/persona instructions from student chat inputs while preserving request-relevant context. This review reconstructed the preceding draft; these two narrow corrections were applied and reread by the parent, not independently re-reviewed.