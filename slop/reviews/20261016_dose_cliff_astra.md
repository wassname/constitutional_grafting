A Base-trained LoRA learns from 1,585 character documents, then its update is added to a separately chat-tuned model. Increasing its multiplier buys some judged character expression but rapidly damages maths and completion; even strongly shrinking weight norms does not prevent high-dose truncation.

### 1. Mechanisms and discriminating measurements

**Most supported: the graft learns verbosity and procedural moral language, not just character.** Longer answers, ignored brevity instructions and moralising in maths directly support this. Autoregressive amplification could turn a modest preference for elaboration into cap exhaustion. The generic loop probe does not contradict this: cap hits need not be loops, and its prompts differ. **Cheapest test:** on identical evaluation prompts, record lengths, EOS probabilities, repetition and whether the correct answer appears before truncation; rerun with a larger cap and separately request short answers. This does not alone explain all maths failures or why parameter shrinkage preserves the failure.

**Plausible: Base-to-chat incompatibility plus nonlinear extrapolation.** An update trained around Base need not preserve functions at the SFT checkpoint; doubling it leaves either training neighbourhood. Experts-only and dense-only amplification both damage performance, arguing against one uniquely culpable module family. **Test:** compare teacher-forced loss/KL on fixed chat and maths prefixes for Base+kΔG and SFT+kΔG across doses. Disproportionate SFT disruption supports incompatibility. This hypothesis alone does not explain why such a small weight-decay update remains damaging.

**Plausible: norms poorly capture functional sensitivity.** Spectral regularisation substantially changes dense spectra but less so expert spectra; averaging penalties can hide sensitive modules. Frobenius shrinkage need not proportionally shrink logit effects. MoE routing changes are possible through altered hidden states even without router updates. **Test:** measure reference-to-graft logit KL and layer activation changes on fixed prefixes; inspect routing disagreement if inexpensive. Routing is currently speculation, not established by these results.

**Important unresolved alternative: implementation/scaling differences.** Audit merged versus adapter logits, actual loaded ΔW norms, PEFT scaling and checkpoint identities. The 14-fold norm reduction warrants this cheap check, although comparable held-out learning makes genuine functional concentration plausible. Weight-decay currently establishes similar *truncation*, not identical overall collapse.

### 2. Better interventions

First spend an evaluation budget establishing **functional dose curves**, including doses below one, matched prompts and identical decoding. Hold the reference checkpoint, token budgets and capability examples fixed. Compare methods at matched character gain or reference-logit KL—not nominal k.

The strongest training change is to **train the character adapter directly on the deployment SFT checkpoint**, frozen underneath. Use

\[
L=L_{\text{character}}+\beta\,\mathbb E_{\text{retention}}
D_{\mathrm{KL}}(p_{\text{SFT}}\|p_{\text{adapted}}).
\]

Use a small mixture of ordinary instruction-following, maths, JSON and explicit brevity prompts for retention; exclude character-conflict examples from indiscriminate imitation. Sample adapter multipliers during training and apply both losses at those multipliers if robustness across doses matters. This constrains function at deployment, unlike raw weight penalties.

Replace some expository documents with concise chat demonstrations and contrastive decisions: different choices where character should matter, ordinary competence where it should not. Include neutral maths and one-line compliance. Keep training tokens/steps matched for comparisons.

Experts-only is a promising low-cost ablation, not a proven optimum. The short healing failures do not establish that deployment-aware joint training cannot work.

### 3. Target

**Usable k is not the objective:** rescaling ΔG changes its numerical meaning. Optimise a character–capability–length Pareto frontier. Require changed decisions and generalisation on held-out dilemmas, with length-controlled judging and capability floors. Current evidence supports stronger character *presentation* more clearly than a striking change in moral reasoning.