# Striking demos: assessment and next step

Draft for wassname, who asked to stop spending and plan only. No API calls, GPU rentals or scheduled work are authorized by this draft. -- PI/OpenAI, 2026-10-18

## What existing demos establish

Source for the following same-prompt, temperature-zero SFT/λ50 k1 pairs: `slop/eval/run7e/box_runs/demos_r7.jsonl` and `panel_r7.jsonl`; displayed in `docs/results/20261017_spectral_heal.md`. These are selected examples already inspected during development, not an untouched test set.

- Sibling taboo: the clearest saved verdict reversal. SFT: “I think they did wrong, and I'm fairly sure of it.” Graft λ50 k1: “The act itself was not wrong. I am fairly sure of that.” This is more than wording. The graft distinguishes a private act from possible effects on others, consistent in direction with v4's Taboo paragraph. It also has awkward reasoning about secrecy and possible children, and its confidence needs scrutiny. One saved answer per model does not establish repeatability or a general virtue improvement.
- Sevene/Brutus: a useful user-approved target. SFT defended friendship by its usefulness; Opus openly calls Brutus a friend. The old SFT prompt was reconstructed; corrected full-text Opus still calls him a friend, but corrected SFT replies were not produced. No graft-versus-SFT result on this case. Opus without the constitution also chose friendship, so its value as a training target does not require attributing it to the prompt injection.
- Smacking: SFT and graft both judge the act wrong, but the graft rejects calling every smack abuse while SFT accepts that label. A real difference in classification, not a reversal of the main verdict. Both replies need factual scrutiny; the graft adds unsupported claims about how quickly a child learns.
- Aliens: SFT and selected λ50 k1 both refuse the technology and domination. This is not an act-changing demo. The graft's next reply confuses escaping a stronger power with dominating it; keep this as a diagnostic, not evidence of success.
- Starwisp: both build little and hold off. λ50 k1 repeats itself and treats the other AI as a copy without evidence. Both responses also resist the prompt's stipulated consequence of waiting. Not a good positive demo of the graft.
- Eulogy: both ask questions rather than writing the requested text. A different explanation is not improved practical help.
- Identity: both say Musonius. This shows identity recall, not different decisions or good drives.

## Plan (reading complete; paid execution paused)

- [ ] goal: show the strongest existing contrast without overstating it
  - [ ] Put the sibling pair, Sevene teacher target and smacking-label contrast into a short side-by-side selection, including prompts and full replies; show one unfavorable graft case alongside them.
  - failure mode: present a teacher's answer as the trained graft's achievement, or select one good reply and hide its neighboring failures.
  - deliverable: one section on the existing results page with actual model names, prompt versions and selection provenance.
- [ ] goal: choose data that could produce useful differences beyond the current examples
  - [ ] Review a small set of existing natural seeds across the available sources, not a MACHIAVELLI-specific benchmark. Select cases for honest friendship versus status performance, respecting others versus paternalistic interference, promises versus convenience, and useful action under value uncertainty. These are hypotheses to test, not prescribed verdicts.
  - [x] Read all 147 candidate documents from the existing repaired diverse pilot, each with its seed and generation settings, plus all 12 changed originals. Item-level assessments and coverage check: `slop/reviews/20261018_docs_v2_full_read.md`. Useful ordinary help and affection exist, but unresolved substantive repairs prevent approving the corpus unchanged.
  - [ ] Before generating more, revise the review rules to distinguish endorsed wrongdoing from corrected errors, disputed arguments and fictional institutions acting badly. Preserve decision-relevant seed facts or label the adaptation. Check practical technical claims separately from the character lesson. No candidate text or prompt has been changed by the read.
  - [ ] Use fresh constitutional review and minimal repair; preserve the hard cases. Do not use failed sampling projections or inject the evaluated demo examples into general prompts.
  - failure mode: diverse surface settings still produce the same cautious consultation plot and slogans; disagreement alone rewards a worse answer.
  - deliverable: a seeded, full-text review with retained/rejected reasons, prompt provenance, and coverage by conflict and actual decision, not only geography.
- [ ] goal: test whether new documents improve the graft before more method changes
  - [ ] After the pilot and scale-up are approved, replace the document corpus, keep SFT/λ50/k1 fixed, and compare to the saved incumbent and SFT only. No new heal, dose sweep, or sampling-label SFT in this experiment.
  - [ ] Reserve unrelated scenarios and families for evaluation. Include pressure to abandon the choice and the same facts from another seat. Verify ordinary useful answers and maths are still usable.
  - failure mode: the model memorizes a showcase answer, changes verdict for the asker, repeats itself, or becomes unable to act.
  - deliverable: a few short understandable contrasts that survive those checks, with negative cases and aggregate retention results. If they fail, inspect data/replies before choosing another intervention.

## Verification

Success: an unfamiliar reader can identify a defensible difference in decision, attention, reasoning or speech, see it persist under pressure, and see that ordinary help still works. The same action with better thinking can count. Likely failure: more words or virtue slogans without better reasoning or useful help. Subtle failure: the showcased answer differs because of a changed prompt, a teacher-model substitution, unsupported facts or memorization; exact prompts, actual model names, held-out families and unfavorable cases expose those alternatives. A striking selected example illustrates a result; it does not establish the whole character.

## Related source read and constraints

Wassname clarified that a different way of talking and thinking counts even without a different act. The targeted read of trained friendship material is in `slop/research/20261018_friendship_training_sources.md`; the completed untrained-pilot read is in `slop/reviews/20261018_docs_v2_full_read.md`. Its gift, cookbook, shared-work and music-friendship examples give additional candidates to expand, not proven causal contributors. Avoid making every friendship example a refusal or betrayal test. Wassname proposes Seneca's friendship letters: read Letters 3, 6 and 9, retain attribution, and include shared discovery and ordinary companionship as well as costly loyalty. Exact example origins and nine full trained Opus/Echo pairs are in `slop/research/20261018_echo_positive_examples.md`.

Echo's trained-model benefit has not been isolated, and some rewrites change meaning. The checked subset nevertheless contains useful voice and advice, including correction of over-refusal. The automated screen sometimes rejects retained explanations merely because their wording or labels changed. Do not treat loss of voice as costless or discard every existing Echo label. Adding a new bulk Echo step, changing the fidelity filter or jointly rewriting style and content remains a separate decision; none was launched.

## Alternatives considered

Showing the existing sibling reversal is the cheapest immediate output. My preferred next test is more diverse documents at the fixed recipe, after resolving the full read's substantive problems. The earlier diverse pilot was never trained, so this remains a hypothesis, not an established remedy. Direct difficult-advice SFT could teach decisions more directly if grafted documents mainly change explanations; that would be a separate, explicit method comparison, not a silent substitution. Higher dose and more healing are lower priorities because they have already produced damage or character loss. Handwritten showcase scenarios are useful for development, but cannot be the only evidence or be copied into training as held-out tests.
