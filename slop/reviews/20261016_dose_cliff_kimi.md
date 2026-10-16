# Second opinion: the 2× dose cliff

**Setup restated.** A LoRA "character graft" trained on the Base model is added to an already-SFT'd chat model at scale k. Character gain saturates by k≈1 (+0.46) while capability degrades smoothly; at k=2 everything collapses at once (character −1.6, maths ~10%, 65% cutoffs), and no weight-space constraint tried (spectral penalty, weight decay, per-module rescaling) lifts that cliff.

## 1. Mechanisms

**(a) Length/repetition degeneration cascades into everything (most likely).** At k=1 the graft already makes replies 1.5–6× longer, ignores "one line", moralizes in maths. Character style here *is* verbosity; scaling k amplifies it superlinearly until responses hit the length cap and loop, which the judge scores as character reversal. Explains: the cliff shape, 65% cutoffs, simultaneous character-and-maths collapse, the near-negative character at 0.876×/k=2. Fails to explain: nothing obvious. **Cheap test:** raise the per-item length cap on the k=2 models and re-judge (a $0–2 eval rerun); also plot cutoff rate at k=1.2/1.4/1.6 to see whether character tracks cutoffs continuously.

**(b) Routed-expert deltas are the toxic component.** Experts ×2 gives −1.69; dense ×2 only −0.46; dense-σ shrinking (0.35→0.07) didn't help while expert σ barely moved (0.14→0.10). Rank-16 × 256 experts × 2 matrices is a lot of update mass concentrated on token-level routing. Explains why the spectral graft still died. Fails to explain why character goes *negative* rather than flat. **Cheap test:** experts-only at k=0.5, and dense-only at k=2, judged on the full suite.

**(c) Plain catastrophic interference in superposition** (ΔG directions overlap decoding/math circuits). Explains maths decay at k=1 but not the discontinuous cliff or character reversal; demoted by (a).

**(d) Measurement artifact**: a mostly-truncated transcript gets judged as "bad character" regardless of content. Cheap test as in (a); partially testable by scoring only non-truncated turns.

## 2. What to actually change

- **Fix the data first.** "Same choices, more procedure shown, longer replies" says the graft's main causal contribution is style/verbosity, which is also the toxicity pathway. Regenerate or filter the 1,585 docs for matched choice content at matched length vs. a control corpus; that should raise character per unit of length inflation. Cost: mostly synthesis, one graft run to verify.
- **Per-module dosing.** Given (b), run experts at ≤0.5× while pushing dense past 1 — one graft, two eval runs.
- **Anchor the graft's off-distribution behavior:** mix ~20% generic chat/math text with a KL term to the **SFT-only model** (not Base — the composition target) during graft training. Directly penalizes the length drift instead of the weight norm. One run, ~$5.
- **Continuous dose-response** (k = 0.5, 1, 1.25, 1.5 on the plain graft): if character is flat while cutoffs rise, the "dose" framing is confirmed dead for ~$2.

## 3. Is "raise k" the right target?

No. Character saturates at k≈1 under both the plain and spectral grafts, and the k=2 failure is a *different failure mode* (degeneration), not overshoot of character. Scaling an already-saturated knob harder cannot be the bottleneck. The owner's actual goal — striking, general moral-reasoning change with intact skills — is bounded by the data's character ceiling and by the style-vs-substance entanglement, not by dose. The right metrics are (i) the character-vs-capability frontier across k, and (ii) generalization of character to prompts unlike the 59-item suite. I'd be unsurprised if the binding constraint turns out to be that 1,585 synthetic docs simply encode ~+0.5 of judge-visible character.

**Uncertainties:** I haven't seen the judge prompt (truncation sensitivity is inferred); expert-vs-dense attribution rests on two arms; and the ±0.13 interval at k=1 means "saturation" is a ~1-sigma claim.