# Next experiment: focused constitutional documents, spectral LoRA graft

Draft updated 2026-10-19. Execution remains paused; this is not spending approval. -- PI/OpenAI

User decisions: keep LoRA; learn documents on Base and graft onto Instruct; improve talking, thinking, reasons and decisions. Extra character SFT is optional, not a required stage.

- [ ] goal: establish what the existing SFT and document updates each contribute
  - [ ] Use `model = Instruct + a*Δsft + b*Δdocs`, with `(a,b)` = `(SFT strength, document strength)`. Test `(0,0), (0,1), (1,0), (1,1), (0,2), (2,0), (2,2)` using the saved SFT and λ50 document adapters.
  - [ ] Use one fp16 merge protocol, frozen prompts and generation settings; reuse records only when these and the weights match. Screen cheaply, repeat finalists, and stop spending on doses already shown incoherent. No new training or heal in this screen.
  - failure modes: report an effect conditional on SFT as graft-only; confuse larger coefficients with a better character/capability trade-off; reuse incompatible cached replies.
  - deliverable: one coefficient table with capability/coherence and full positive/negative demo pairs; merge hashes and prompt provenance distinguish genuine changes from changed inputs. Read raw replies and judge reasons before selecting the next recipient.
- [ ] goal: produce a focused but diverse document corpus worth training
  - [ ] Reuse the successful original-document recipe and reviewed pilot findings. Expand source-grounded friendship/companionship, useful work, honest disagreement, uncertainty and self-correction. Use Seneca/Rufus plus diverse natural human seeds; vary document form, viewpoint, relationship and setting, not only names/geography.
  - [ ] Repair the reviewed pilot's substantive problems and review rules first. Preserve corrected mistakes and contested arguments; distinguish depicting wrongdoing from endorsing it. Run the required independent data-review package before bulk scale-up.
  - [ ] Target roughly 3× the current document-token budget: about 6.5M tokens in distinct documents before epochs, rather than duplicated rows. Keep source, actual prompts, constitution version and writer/repair provenance. No bulk Echo, projected labels or new chat-SFT corpus by default.
  - [ ] Read every candidate with its seed/prompt and every changed original; repair hard advice rather than dropping it. Verify technical claims and the exact tokenized training text, including whether truncation removes conclusions. Keep evaluation scenarios/families out of generation.
  - failure modes: more refusal/consultation stories in varied costumes; source conflicts simplified away; more text but no new useful reasoning; good conclusions clipped during training.
  - deliverable: approved plain-text JSONL and one full-read ledger with remaining defects resolved, seed/form coverage and actual trained-token counts. The existing 147-row pilot is read, not approved unchanged.
- [ ] goal: test whether better documents improve the graft without changing every method
  - [ ] Train one document LoRA on matching Qwen Base, all-token next-token NLL. Start from the selected λ50 spectral recipe; keep parameter targets and other training choices fixed. No new character SFT, full FT, cwsteer or replay-control branch in this experiment.
  - [ ] Add the update to untouched Instruct unless the coefficient screen gives a clear reason to retain existing SFT. Keep the other recipient as a comparison merge, not another training stage. Compare old/new document adapters on the same recipient to isolate the corpus change.
  - [ ] Calibrate a small serving-strength range around the coherent region; compare character at matched capability, not equal numeric strength. Check genuine changes in reasons and speech as well as decisions, pressure/point-of-view consistency, ordinary help and maths.
  - failure modes: call near-training recall generalization; reward longer virtue prose; confound changed data with changed recipient; mistake runtime/numeric damage for a moral result.
  - deliverable: update `docs/results/20261017_spectral_heal.md` with full required demo panel, held-out contrasts, unfavorable cases and retention results. Read logs/replies and use ml-debug to rule out bugs before accepting a negative interpretation.
- [ ] goal: repair useful graft damage only if it is needed
  - [ ] On a coherent graft with measurable maths damage, try a short heal using its own verified-final maths answers. Check an early checkpoint before extending. Compare against the same unhealed weights/precision at the same graft strength and against a lower-strength unhealed model.
  - failure modes: maths improves by erasing character; final answers pass while reasoning remains broken; a precision change masquerades as learning.
  - deliverable: a retained heal only if maths improves and character/action checks remain sound. Otherwise keep the unhealed model and record what failed; a partial maths gain is not a successful heal.

## UAT / Verification

Success: prompts and full replies show defensible changes in thinking, speech or acts that survive pressure, with useful ordinary answers and acceptable maths. Likely failure: repetitive moral language, unsupported facts or capability loss; show these rather than selecting them out. Subtle failure: taught cases, teacher substitutions, changed prompts or changed recipients produce apparent gains; source provenance, unchanged-input comparisons and held-out families expose them.

## Budget and approval

First approve only the saved-adapter coefficient screen. Historical merge/load/generation timing suggests roughly two GPU-hours for seven cells plus setup, not a firm quote; judge cost is additional. The earlier ~$60 estimate covered ~1,500 documents. At that rate ~4,755 documents (3× 1,585, if lengths match) would be about $190 for generation/review, not $60. Confirm the new corpus size, bill estimate and execution permission before bulk generation; do not silently reuse the old approval. Training alone scales from the measured ~1.7-hour LoRA run toward ~5 hours, before evaluation/healing; these are estimates, not invoices.

Sources: `slop/reviews/20261018_docs_v2_full_read.md`, `slop/research/20261018_echo_positive_examples.md`, `slop/research/20261019_full_weight_recipe_lineage.md`, `slop/eval/run6/graft_split_tokens.txt`, `slop/research/20261017_heal_cost_basis.md`, `docs/results/20261017_spectral_heal.md`.
