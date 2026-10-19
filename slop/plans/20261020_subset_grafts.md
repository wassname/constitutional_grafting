# Draft: separate document subsets, then mix their grafts

PI/OpenAI. Discussion draft, not execution or spending approval.

User proposal: Opus-to-Echo from good seeds; pure Stoic; expanded Opus from good seeds; Opus through Greek and back to English. Aim for100-300 examples per subset and independently usable LoRAs. Simplify to Base-trained document grafts with spectral regularization; evaluate healing after selecting the mixture.

- [ ] goal: prepare four useful document subsets
  - [ ] Select100 examples per subset before considering300
  - [ ] Reuse existing good Echo material before buying new replies
  - [ ] Preserve original Stoic attribution and recorded translation provenance
  - [ ] Share seeds and requested formats across writer variants where possible
  - [ ] Read every final text with its seed, prompts, changes and factual checks
  - [ ] Obtain the independent full-sample review before scaling
  - failure modes: writer and content effects are confused; duplicated cases inflate exposure; rewriting changes reasons or agency
  - deliverable: four plain-text manifests with exact chosen texts, source overlap, format, provenance, token counts and unresolved exclusions
- [ ] goal: learn independently usable document grafts
  - [ ] Train each LoRA from the same untouched Base checkpoint
  - [ ] Keep module coverage and spectral recipe fixed; record actual token exposure and optimizer steps
  - [ ] Add each saved update to the same untouched Instruct recipient
  - failure modes: a subset has too few updates to learn; different anchors or exposures make comparisons misleading; loss falls by memorizing
  - deliverable: four saved adapters with matching anchor/config provenance and same-input held-out character, maths and ordinary-help results
- [ ] goal: find useful combinations without hiding damage
  - [ ] Evaluate individual adapters before a few selected combinations
  - [ ] Compare useful character against capability damage across serving strengths
  - [ ] Read failures and investigate training/evaluation bugs before interpreting a negative result
  - [ ] Test healing only after choosing a promising mixture
  - failure modes: individually useful updates interfere; fixed-dose comparisons imply a false ranking; healing cancels character
  - deliverable: coefficients, full demo replies and a shared character/capability plot, including failures

## Verification

Success: individually measured updates produce useful held-out changes, and selected mixtures retain usefulness; raw replies support the claimed reasons/actions.
Likely failure: one subset overfits its examples or produces no clear held-out signal; inspect real batches, update norms, loss and outputs before deciding what to change.
Subtle failure: a preferred writer also has easier seeds or repeated scenario families; manifests expose overlap and compare shared-seed variants separately from different-source mixtures.
Check Base and recipient hashes, module coverage and independent starting points. Combine expanded weight updates, not averaged LoRA factors. Removing an adapter tests its contribution to that mixture, not equivalence to joint training without that data.

## Open decisions

- Does pure Stoic mean original attributed passages without Opus rewriting?
- Echo reuse is the initial cost-saving assumption;100 suitable existing outputs are not yet verified. Existing dialogues stay labelled as dialogues, not prose documents or new teacher generations.
- Greek currently means Opus writes directly in Modern Greek, then DeepSeek translates to English. An English-to-Greek-to-English round trip is a distinct, unrun recipe requiring a decision.
- Four cohort LoRAs first. Finer adapters for saved data batches remain an option; they are not optimizer-minibatch adapters. Training/save/evaluation overhead and interaction tests grow with adapter count.
- Corpus review may reject or repair examples, but does not imply learned-model benefit. Pilot size is a research choice, not a known sufficiency threshold.
- Budget and execution need approval; no new paid model call, rental, training or healing is authorized by this draft.
