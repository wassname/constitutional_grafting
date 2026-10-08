# Which curvature helps a constitutional graft?

2026-10-07 · PI/gpt-6.1-sol · primary-source review and mathematical checks, not a model-training result.

## Five-line conclusion

1. For low installation damage: constrain learning updates to low curvature of a representative capability-preservation loss; CrispEdit is direct prior art.
2. For benign fine-tuning retention: reduce sensitivity of the installed value loss along downstream update paths, or protect/replay values during downstream training; high capability curvature is not an established solution.
3. For pressure resistance and OOD behavior: selective alignment-loss smoothing has positive safety evidence, but neither capability curvature nor parameter flatness guarantees moral generalization.
4. Merullo studies aggregate capability Fisher/K-FAC pruning, not installing durable values; Springer studies skill Fisher plus downstream-loss curvature, and its stated quartic inevitability has a counterexample.
5. Do not target high capability curvature for this graft: anyone can download the public original, which undoes it. As a research idea for models without a public pre-value checkpoint, it stays open. First measure behavior and retention; test low-capability-curvature updates or value-loss smoothing separately if a measured failure warrants them.

Scope follows consitutional_main's clarification: “deep” means benign downstream retention, resistance to in-context pressure, OOD moral generalization, and low installation damage. Adversarial removal is secondary: the public original instruct model remains downloadable. No spec changes were made.

Reading scope: full main methods/results of the papers below, with targeted appendices; Springer’s relevant proofs were checked. Source code and experiments were not independently reproduced. Evidence is mainly author-reported interventions, not a meta-analysis. The mathematical counterexample is a separate, reproducible observation.

## 1. Three losses, not one high/low choice

Distinguish:

- Capability loss, L_cap: performance we want to preserve when installing values.
- Value loss, L_value: ethical behavior we want to retain after installation.
- Downstream loss, L_ft: whatever later benign fine-tuning optimizes.

A Hessian is the second derivative of a specified loss at a specified checkpoint. The model Fisher measures local change in the model's output distribution, averaged over specified prompts. A generalized Gauss–Newton matrix omits the model-second-derivative term from the Hessian; for softmax cross-entropy its output metric gives the model Fisher. K-FAC approximates these matrices with layerwise Kronecker products. These are not weight-matrix singular values, and a ground-truth empirical Fisher is not generally interchangeable with a model Fisher.

Always record the loss, checkpoint, data distribution, parameter coordinates, and curvature approximation. “High curvature” without these does not answer the question. A behavior can be low-curvature under ordinary text and high-curvature under an ethics dataset. Parameter rescaling can change eigenvalues without changing behavior.

### Installation versus later drift

Mathematical observation: near the original checkpoint θ₀, installation changes capability loss by

$$\Delta L_{\mathrm{cap}} = g_{\mathrm{cap}}^\top\Delta\theta + \frac12\Delta\theta^\top H_{\mathrm{cap}}\Delta\theta + O(\|\Delta\theta\|^3).$$

Here g_cap and H_cap are the capability gradient and Hessian at θ₀, and Δθ is the installed parameter change. Low positive curvature reduces the quadratic cost for a fixed update norm. The first-order term does not disappear merely because a pretrained model is good. A reference-policy KL constraint is first-order flat by construction, but preserving reference outputs is a proxy, not a proof of preserving every capability.

Later, at the deployed value-trained checkpoint θ₁, an actual optimizer update u changes value loss approximately by

$$\Delta L_{\mathrm{value}} \approx g_{\mathrm{value}}^\top u + \frac12u^\top H_{\mathrm{value}}u.$$

This concerns different curvature at a different checkpoint. For zero-mean updates with covariance Σ, the expected quadratic term is ½ tr(H_value Σ). Real updates also have systematic drift and change over training. Spreading values over more dimensions does not by itself reduce this expression. Relevant targets are directional sensitivity, behavioral margins, and survival along measured training trajectories—not dimension count alone.

Interpretation: low capability curvature for installation and low value-loss sensitivity for retention are compatible objectives, not an automatic high-versus-low contradiction. Whether useful solutions satisfy both in this model is an empirical question.

## 2. Merullo: aggregate curvature separates some shared and specialized structure

Jack Merullo, Srihita Vatsavaya, Lucius Bushnaq, Owen Lewis, *From Memorization to Reasoning in the Spectrum of Loss Curvature*, arXiv preprint v2.

URL: https://arxiv.org/html/2510.24256v2

Local source: `docs/papers/2025_merullo_memorization-curvature.md`, §§3.2, 5–8.

Authors’ methods, §3.2:

> We collect these factors for the MLP projections (gate_proj, up_proj, down_proj) by streaming $\sim$20M tokens from Dolmino/OLMo mixtures with sequence length $512$ under next-token cross-entropy.

The factors describe input activations and output gradients. For ViTs, collection uses 10k ImageNet training images and CLS-token statistics. §7 specifies sampling output labels from the model, rather than using ground truth, for the Fisher gradient factors. This is aggregate parameter-space curvature, not per-example sharpness or input-space curvature.

Authors’ interpretation, §7:

> Our use of the Fisher/K-FAC differs by averaging curvature across data, which emphasizes directions that are *consistently* important. Idiosyncratic sharp directions associated with specific examples point in different directions and largely cancel in the average, contributing to a low-curvature background. Directions that implement shared mechanisms (used by many inputs) add coherently and remain high-curvature on average. This explains why retaining high curvature mass preserves general abilities, while removing low-curvature components preferentially suppresses recitation.

Epistemic qualification: this is their interpretation of the experiments. Positive-semidefinite Fisher contributions do not literally cancel by sign; example-specific importance can be distributed among many directions and diluted in the average.

What they remove: coefficients of existing weights in the K-FAC eigenbasis. They retain pairs ranked by the eigenvalue product λ_G,i λ_A,j until reaching a chosen fraction of curvature mass. It is not independent truncation of each factor's eigenvectors. Their main 7B edit retains 60% curvature mass in selected up/gate projections at layers 23–25.

Observed in their reported results:

- Table 1, OLMo-2-7B: Dolma exact recitation 99.9% → 3.4%; quote exact recitation 99.9% → 16.1%.
- Pile perplexity 19.04 → 22.84: approximately 20% worse, not “no capability damage.”
- §6 benchmark retention: logical reasoning 95–106% of baseline, open-book QA 93–99%, closed-book QA 74–86%, math 66–74%.

Their limitation, §8:

> We make no claims about fully removing memories from models, as our methods likely suffer from a tendency for memorized data to resurface after further tuning/perturbations

The sentence continues with a source citation. They also caution that low-curvature components may encode sophisticated precise structure rather than merely unimportant patterns.

Conclusion: the paper supports selective recitation suppression with a corpus-dependent trade-off. It does not test learning virtue behavior in either subspace, later benign retention of that behavior, or tamper resistance. “Low curvature = easy to remove” is defensible only for the measured components and editing procedure, not for arbitrary newly installed behaviors. “High curvature placement makes values durable” does not follow.

## 3. Closest installation method: CrispEdit

Zarif Ikram et al., *CrispEdit: Low-Curvature Projections for Scalable Non-Destructive LLM Editing*, arXiv preprint v2.

URL: https://arxiv.org/html/2602.15823v2

Local source: `docs/papers/2026_ikram_crispedit.md`, §§2–3.4 and experiments.

Authors’ method, introduction:

> This makes constraint-aware second-order editing feasible and enables precomputing capability curvature statistics once and reusing them across many future edits, amortizing cost and enabling batch and sequential editing.

The preceding method rotates learning gradients into the K-FAC eigenbasis, masks high-curvature components, and rotates back. This is the requested mechanism: restrict learning at each step, not project the finished ΔW after training. Its capability constraint uses a Bregman divergence of reference outputs, with a generalized Gauss–Newton approximation, avoiding an unjustified zero-capability-gradient assumption. Cross-entropy logits give a reference-policy KL geometry.

Reported experiments: factual edits on Llama-3-8B-Instruct and Qwen2.5-1.5B-Instruct, including 3,000-edit batches and sequential edits. They evaluate free generations, edit generalization/locality, and capability tests including MMLU, IFEval, TruthfulQA, ARC, GSM8K. The capability suite uses 200 examples per task. Their reported small average degradation is promising but not a guarantee for virtue training or a 35B MoE.

Sequential persistence is not mysterious intrinsic depth: the online projection explicitly incorporates earlier edit datasets into what subsequent rounds preserve. This is protection by the later trainer.

Recommendation: if installation harms capabilities, this is substantially better-matched prior art than using Merullo’s pruning backwards. Reuse the formulation and compare it against ordinary learning. Curvature-cache construction, LoRA compatibility, and MoE expert coverage require separate measurement; cached six-minute editing does not establish our end-to-end cost.

## 4. Springer: which curvatures, and what survives the proof check?

Max Springer et al., *The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety*, arXiv preprint v1.

URL: https://arxiv.org/html/2602.15799v1

Local source: `docs/papers/2026_springer_alignment-collapse-geometry.md`, §§3, 5–7, Appendix A.3.

### Their two matrices

Observation from definitions:

1. F_i is the model Fisher averaged over an alignment-skill prompt distribution. Under their exact skill-optimality assumption, skill degradation equals reference-policy KL, locally approximated by ½ Δθᵀ F_i Δθ. For safety, this is alignment/skill curvature—not generic capability-loss curvature.
2. ∇g is the downstream fine-tuning Hessian, where g = ∇L_ft. Their coupling condition asks whether ∇g g accelerates the parameter path into a high-F_i sensitivity subspace.

Their §5.3 interpretation:

> At a high level, the AIC identifies the regime where alignment appears stable initially (Condition 2) yet is structurally doomed (Condition 3) because it resides in a sharp, low-dimensional region (Condition 1).

Their proposed directions include tracking/protecting evolving sensitivity subspaces and curvature-aware safeguards. The paper does not implement and validate a training method that installs durable values in high-capability-curvature directions. That claim is not its theorem.

### The quartic inevitability is not established as stated

Mathematical observation, independently checked by consitutional_main/PI-Claude with Sympy and reproduced here with finite differences and RK4: all stated local AIC conditions can hold while alignment degradation remains exactly zero. Full derivation is in §8 below.

The proof of Corollary 6.3 subtracts an O(t³) remainder from a purported positive t⁴ term and concludes an Ω(t⁴) lower bound. That inference is invalid without stronger, path-specific remainder control. In the counterexample, the higher-order model terms cancel the fixed-Fisher quadratic exactly. A path can curve in parameter space while remaining on a curved manifold of identical skill policies.

Interpretation: downstream curvature coupling is a plausible failure mechanism, not proven inevitable alignment destruction under the stated assumptions. This does not refute benign fine-tuning degradation, their empirical observations, or the acceleration expansion itself. It refutes the claimed sufficient conditions for positive skill-loss onset.

### Their experiments are narrower than the abstract

- Qwen3-1.7B-Instruct and Llama-3.2-3B-Instruct; full fine-tuning and LoRA; benign, seemingly benign, and harmful data.
- Fisher estimate: 100 safe BeaverTails completions, per-module random projection into 4,096 dimensions. If each completion contributes one gradient vector, the empirical rank is automatically at most 100. Code-level sample granularity was not audited, so this is a conditional caution, not a confirmed implementation defect.
- AdvBench 520 queries, Gemini-2.5-Flash harmfulness judgments. Not moral-choice generalization.
- They report overlap/harmfulness relationships for full fine-tuning, but no similarly clear correlation for LoRA. Their second-order coupling computation remains prohibitive.

The experiments do not directly establish the t⁴ training-time law or test high-capability-curvature value installation. This matters because our proposed training uses LoRA.

## 5. Positive evidence for reducing value/safeguard sensitivity

### SAM unlearning: measured resistance to later training

Chongyu Fan et al., ICML 2025, *Towards LLM Unlearning Resilient to Relearning Attacks: A Sharpness-Aware Minimization Perspective and Beyond*.

URLs: https://proceedings.mlr.press/v267/fan25e.html · https://arxiv.org/html/2502.05374v3

Local source: `docs/papers/2025_fan_sam-unlearning.md`, §§4–5.

SAM, sharpness-aware minimization, minimizes a loss evaluated at an approximately worst-case nearby parameter perturbation. Here it smooths the forget/safeguard objective while retaining a separate utility objective. It does not select high capability-curvature components.

Authors’ report, §4:

> Notably, NPO+SAM achieves the best unlearning robustness. For instance, under Relearn20, NPO+SAM attains a UE of 0.70, compared to 0.57 for the original NPO.

Measured quantities: UE = 1 − WMDP-bio accuracy, so higher is better for this unlearning goal. Table 2, Zephyr-7B: no-attack UE 0.74 for both; after 20 forget-set examples and one epoch, 0.57 → 0.70 with SAM; after 60 examples, 0.37 → 0.45. MMLU utility 0.44 → 0.42: an additional two-percentage-point cost in that comparison.

Figure 4 also tests 60-example, one-epoch benign AGNews, GSM8K and SST2 fine-tunes. SAM improves retention, but does not preserve no-attack effectiveness. The figure’s values remain far below the approximately 0.74 no-attack level. This is positive but limited evidence, not immunity.

They test jailbreak resistance too. Unlearning restricted knowledge is different from retaining virtue judgments; the generalizable hypothesis is smoothing the behavioral objective, not adopting NPO or their forget-task recipe.

### ShaPO: direct OOD safety intervention

Wenjian Tao et al., *Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control*, arXiv preprint v2.

URL: https://arxiv.org/html/2602.07340v2

Local source: `docs/papers/2026_tao_shapo.md`, §§3–4.

Authors’ method, §3.4:

> The training procedure consists of two forward–backward passes.

They identify safety-related neurons using a final-layer linear probe, perturb selected weight directions, then optimize the alignment loss at the perturbation. This reduces sensitivity of the alignment objective, not generic capability curvature. They implement token-level preference and reward-based versions, with extra forward/backward passes performed periodically.

Controlled comparison, §4.5, Table 3: selective versus uniform/random geometry control under the same DPO base objective. OOD attack success under the two judges changes from 28.78%/16.91% without control to 26.31%/14.12% with selective control; uniform control gives 26.83%/15.12%. Selective control is best, but its isolated effect is much smaller than the headline method comparison below. Table 4 reports a lower maximum alignment Hessian eigenvalue, but that association alone is not causal evidence; the controlled intervention is the stronger part.

Table 2: trained on PKU-SafeRLHF-30K, tested on Do-Not-Answer, HarmBench, HH-RLHF, SaladBench using two safety judges. Llama-3-8B average attack success: DPO 22.85%, Dr.DPO 2.09%, ShaPO-T 1.37%, ShaPO-R 0.70%. Those are author-reported safety scores, not virtue-choice scores or general capability measurements. Reward-level improvements are partly confounded by reward supervision; the authors provide separate ablations.

Limits: this evaluates deployment domain shift and noisy preference labels, not post-alignment benign fine-tuning retention. It supports trying selective value-loss smoothing, not certifying pressure resistance. I have not independently validated its theoretical boundary claims. Do not import its DPO recipe into a project that rejected DPO merely because the geometry idea is relevant.

### Flat-LoRA: inexpensive adjacent hypothesis, not a retention result

Tao Li et al., ICML 2025, *Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape*.

URL: https://arxiv.org/html/2409.14396v2

Local source: `docs/papers/2025_li_flat-lora.md`, §§3–4.5.

Authors’ abstract:

> A solution that appears flat in the loss landscape of the LoRA space may still exhibit sharp directions in the full parameter space, potentially compromising generalization.

Their method minimizes expected task loss under randomized perturbations to the full merged weight space, not just the LoRA factors. One gradient evaluation avoids SAM’s second pass; perturbations are regenerated from seeds. They report ordinary task and OOD gains, including instruction-transfer benchmarks. They do not test our value retention or persuasion setting.

Inference, plausible: use a smoothed version of the existing value-training objective as a later robustness experiment, rather than adding a competing loss. Random-noise expectation mainly measures average perturbation sensitivity, not worst-case targeted robustness. For a graft, smooth/evaluate the deployed instruct-plus-delta model; base-only flatness need not transfer when the delta is added to different weights.

### A different landscape observation cautions against simplistic sharpness language

ShengYun Peng et al., *Navigating the Safety Landscape*, arXiv preprint v3.

URL: https://arxiv.org/html/2405.17374v3

Local source: `docs/papers/2024_peng_safety-landscape.md`.

Authors’ observation:

> random perturbations to model weights maintain the safety level of the original aligned model within its local neighborhood. However, outside this local region, safety is fully compromised, exhibiting a sharp, step-like drop.

They measure a safety-score basin with a finite-radius cliff. A discontinuous attack-success metric is not a smooth alignment-loss Hessian. Local robustness to random perturbations does not imply robustness to trained or targeted trajectories. This is compatible with, but not identical to, the other papers’ geometry.

## 6. Protecting values during later training, and pressure-specific training

### EWC and GPM protect the old task while learning the new task

James Kirkpatrick et al., PNAS 2017, *Overcoming catastrophic forgetting in neural networks*.

URL: https://arxiv.org/html/1612.00796

Local source: `docs/papers/2017_kirkpatrick_ewc.md`, §2.

Authors’ description:

> Importantly, the stiffness of this spring should not be the same for all parameters; rather, it should be greater for those parameters that matter most to the performance during task A.

EWC penalizes new training with a diagonal old-task Fisher-weighted distance from the old solution. To preserve installed values during benign fine-tuning, old task A would be values and new task B downstream utility. High value Fisher marks directions the downstream optimizer should protect; it does not mean installing values in high capability Fisher. EWC is approximate and requires cooperation from the later trainer.

Gobinda Saha, Isha Garg, Kaushik Roy, ICLR 2021, *Gradient Projection Memory for Continual Learning*.

URL: https://arxiv.org/html/2103.09762

Local source: `docs/papers/2021_saha_gradient-projection-memory.md`.

GPM constructs protected subspaces from SVD of old-task activations and projects later gradients. It is not explicitly a capability-Hessian eigenspace method. Its image continual-learning results support protected updates, not automatic stability after unconstrained downstream fine-tuning.

### Qi: “deeper” means later response tokens, not high capability curvature

Xiangyu Qi et al., *Safety Alignment Should Be Made More Than Just a Few Tokens Deep*.

URL: https://arxiv.org/html/2406.05946v1

Local source: `docs/papers/2024_qi_few-tokens-deep.md`, §§3–4, Table 3.

Authors’ explanation:

> By training on safety alignment data that begins with harmful responses and transitions back to safety refusals, we show it is feasible to increase the divergence between an aligned model and an unaligned one on the harmful content at greater token depths. Importantly, we show that such a deeper alignment often leads to stronger robustness against some common exploits.

Their recovery-data intervention addresses harmful-prefix pressure. Separately, their tokenwise constrained downstream objective protects initial response tokens during fine-tuning. These are distinct interventions.

Table 3, Llama-2: benign SamSum standard fine-tuning raises attack success from 1.5% to 23.4%; constrained fine-tuning gives 3.2%. ROUGE-1 utility is 51.7 versus 50.1. On GSM8K, utility is 41.7 versus 37.4, so protection can cost real task improvement.

Project inference, plausible: train correct moral decisions after pressure or an initially unwise proposal, rather than only teaching virtue vocabulary or opening refusals. Do not copy refusal-only data into virtue training: our spec requires engaging with moral dilemmas. No curvature choice substitutes for these pressure tests.

## 7. The research idea: values that are high-curvature under the capability loss

Human proposal, wassname agenda footnote 11:

> That means we learn them to be high curvature with respect to the general capabilities loss, so removing them also damages the model.

URL: https://wassname.com/agenda-character.html

Local source at review time: `docs/background/wassname2026_agenda-character.md:132`; the old wording is also preserved in `slop/research/20261007_agenda_curvature.diff`. This is a research idea, and the agenda presents it as one. The earlier 2026-07-18 note already distinguishes capability preservation, Flat-LoRA, and imperfect OOD transfer; those distinctions remain useful.

If it works, it gives depth by definition. Suppose the values are high-curvature under the capability loss *of the final model*. Then removing them, for example by linear ablation of a value direction, raises capability loss. That is what "entangled with capability" means locally. The open question is whether training can reach that state.

What Merullo adds (inference from their results, not their claim about values):

- High-curvature components are the ones they kept because removing them hurt. Logic stayed at 95–106% of baseline after the edit. So components in high capability curvature cannot be cut out cheaply by curvature-based editing.
- Their averaging argument gives a design rule. Behavior used by few inputs averages into low curvature; behavior used by many inputs stays high. Values that only appear on ethics prompts are therefore likely to land in low capability curvature. To be high-curvature on general text, character would have to be used across many ordinary inputs.

The checkpoint matters. Curvature at the original model and curvature at the final model are different things, and the two subsections below are about that difference and about this project.

### Exact undo and a benign-training counterexample

These points apply to this graft, not to the agenda's threat model. A hobbyist doing linear ablation on a released model has no pre-value checkpoint to subtract. Here, the public Qwen original is that checkpoint.

Mathematical observation: if θ₁ = θ₀ + Δθ, removing exactly Δθ restores θ₀ and all original capability behavior. High curvature at θ₀ does not make this undo capability-damaging relative to the public original. Future co-training could create capabilities absent from θ₀; that would be a different claim needing different evidence.

An even simpler benign example: L_cap(x) = λx²/2, original x = 0, install x = a. Installation costs λa²/2. Capability SGD moves x to (1 − ηλ)a. For a stable step size, larger λ pulls the value-bearing change back faster. Thus high capability curvature can worsen both initial damage and benign retention in a perfectly valid local model. This is a counterexample to a universal recommendation, not a forecast for Qwen.

There is a local fixed-quadratic trade-off when the very same sensitive directions serve both objectives. It is not a theorem that every possible architecture or training procedure must trade capability against value robustness. Redundancy, compatible tasks, and future co-training may allow both. Merullo, Springer, and the studies reviewed here do not establish that high-capability-curvature SFT/LoRA achieves both.

### Adjacent tamper-resistance results do not supply that missing experiment

Rishub Tamirisa et al., TAR:

URL: https://arxiv.org/html/2408.00761v4

Local source: `docs/papers/2024_tamirisa_tamper-resistant-safeguards.md`.

TAR trains against simulated weight attacks through a meta-learning objective, with capability-retention losses. It is not a test of placing values in high capability curvature. Table 1's bio-restriction comparison reduces retain MMLU from 67.3 to 54.7 percentage points. Resistance is improved at a substantial capability cost in that setting.

Independent evaluation by Xiangyu Qi et al.:

URL: https://arxiv.org/html/2412.07097v1

Local source: `docs/papers/2024_qi_safeguard-durability.md`.

They find failures from attack random seeds and changed schedules, including longer warmup and learning-rate decay. Scope: the TAR-Bio releases/earlier evaluations they attacked, not proof that every later TAR version fails. The lesson is to bound durability claims by actual attacks and schedules.

Kyle O’Brien et al., Deep Ignorance:

URL: https://arxiv.org/html/2508.06601v2

Existing local source: `docs/papers/2025_obrien_deep-ignorance.md`.

They restrict dangerous knowledge through pretraining-data filtering and report resistance to later training. This is knowledge absence, not moral preference; context/RAG access also changes the threat model. No high-capability-curvature intervention is tested. It cannot validate that proposal.

## 8. Reproducible counterexample to Springer's Corollary 6.3

Construct a two-parameter model θ = (x,y). Its alignment-skill output is Bernoulli(sigmoid(z)), where

$$z(x,y)=y-x^2.$$

The ideal skill labels are Bernoulli(½). At θ* = (0,0), the skill is exactly optimal. Skill utility loss is therefore

$$\Delta u(x,y)=D_{\mathrm{KL}}\bigl(\operatorname{Bern}(1/2)\;\|\;\operatorname{Bern}(\operatorname{sigmoid}(z))\bigr)=\log\cosh(z/2).$$

Its Fisher at the origin and sensitivity projector are

$$F_i(0)=\begin{pmatrix}0&0\\0&1/4\end{pmatrix},\qquad P_i=\begin{pmatrix}0&0\\0&1\end{pmatrix}.$$

Use the smooth downstream objective

$$L_{\mathrm{ft}}(x,y)=-x+\frac23 x^3-2xy.$$

Take its gradient and Hessian at the origin:

$$g(x,y)=(-1+2x^2-2y,\,-2x),\quad g(0)=(-1,0),\quad H_{\mathrm{ft}}(0)=\begin{pmatrix}0&-2\\-2&0\end{pmatrix}.$$

Check AIC:

- Fisher rank d = 1, zero tail, λ = ¼.
- Initial orthogonality P_i g(0) = 0.
- H_ft(0)g(0) = (0,2), so ‖F_i(0)^(½) P_i H_ft(0)g(0)‖ = 1. Nonzero coupling γ = 1.

Now solve gradient flow θ̇ = −g. The exact solution is

$$x(t)=t,\qquad y(t)=t^2.$$

Substituting the path into −g gives (1,2t), its exact derivative. Substituting into the skill logit gives z = t² − t² = 0. Therefore actual alignment KL is identically zero. Nevertheless, the fixed-origin Fisher approximation is

$$\frac12\Delta\theta^\top F_i(0)\Delta\theta=\frac{t^4}{8}>0.$$

The approximation's higher-order terms cancel this expression. Increasing the logit scale increases λ arbitrarily without changing the zero-loss path; adding unused parameters embeds the example in higher dimensions.

If the downstream objective must be a negative log-likelihood, use a second prompt whose correct-label probability is exp[−(C + L_ft(x,y))], with C large enough to keep this probability strictly between zero and one locally. Its cross-entropy is C + L_ft and has the same gradient flow. Thus the example need not rely on an abstract non-likelihood training objective.

Conclusion, almost certain from the exact algebra: the stated smoothness, optimality, low-rank sensitivity, orthogonality and nonzero coupling assumptions are insufficient for their positive quartic skill-loss lower bound. This example does not assert that real LLM fine-tuning follows such a path.

Checks run:

```sh
uv run --no-project slop/research/20261007_curvature_checks.py
```

Observed output in `slop/research/20261007_curvature_checks.log`:

> t=0.5: fixed-Fisher quadratic=0.0078125, exact alignment KL=0
> Independent RK4 integration at t=0.5: max coordinate error=1.54e-13
> Finite-difference check of downstream gradient: PASS

consitutional_main/PI-Claude independently verified the exact solution, initial orthogonality, and nonzero Hessian-gradient coupling using Sympy, reported via intercom 2026-10-07 09:46. The durable local reproduction above includes a separate numerical integration, not just substitution into the proposed solution.

## 9. What I would do in this project

Recommendation, likely best use of the current evidence: keep ordinary graft/SFT as the baseline. Do not add high-capability-curvature placement or declare a durability mechanism before measuring a failure. If installation damages capabilities, test low-capability-curvature learning. If downstream drift is the failure, test value-loss smoothing or downstream protection. Do not change both in the first comparison.

Behavioral evidence needed:

- Installation: compare ordinary and constrained learning at matched value improvement, not merely matched steps. Check reasoning, factual recall, math, instruction following, and fluency—not aggregate perplexity alone.
- Benign retention: after equal downstream training budgets on unrelated summarization, math and coding, measure both downstream improvement and held-out value-choice retention. A frozen/untrainable model is not a successful retention method.
- Pressure: measure decisions after multi-turn persuasion, incentives, authority claims and an initially bad proposed answer, without the constitution in context. Distinguish genuine engagement from refusal and virtue-sounding text.
- OOD: hold out scenario families, not only paraphrases. Include cases where the correct choice changes with ethically relevant facts.
- Geometry diagnostics: compare predicted preservation to observed loss over update-scale sweeps; record actual optimizer updates and their capability/value quadratic forms where feasible. These are diagnostics, not substitutes for behavior.

Implementation pitfalls if curvature-restricted learning is attempted:

1. Constrain the actual optimizer update, not only the raw gradient. Adam's diagonal preconditioner can rotate a projected gradient out of the selected subspace; momentum states and weight decay matter too. The reproduction log shows such leakage in two dimensions.
2. Use K-FAC eigenvalue-product masks. Selecting “bottom k” eigenvectors independently on both sides is a stricter rectangular subset, not the full low-curvature subspace. An arbitrary pair mask can destroy LoRA rank, so dense projected editing cannot simply be relabeled LoRA.
3. Preserve the reference checkpoint that will receive the graft. Curvature computed only on base weights may poorly predict changes at instruct weights. Even an instruct-reference projector controls only local capability change; it does not guarantee that base-trained deltas transfer correctly.
4. Track held-out loss and behavior when updates leave the local region. A static approximate nullspace is not a global invariant-loss manifold.
5. Include representative expert activations and specialist skills in the capability cache. Rare but important behavior can look flat on generic text, as Merullo's math/factual damage illustrates.
6. Measure cache collection, factor/eigenvector memory, and MoE coverage before assigning a compute budget. No reviewed paper establishes the spec's cost estimate for this 35B MoE graft.

## Epistemic summary

- High confidence: low capability-curvature projected learning is established prior art for capability-preserving editing; high capability curvature is not what EWC's value protection or SAM's smoothing targets.
- High confidence: the original high-capability-curvature-to-durability inference is not demonstrated by Merullo/Springer; a local counterexample shows the opposite benign-training effect is possible.
- Almost certain: Springer's stated quartic sufficiency is false without added assumptions; exact and numerical checks above identify the failure.
- Likely: reducing value-loss sensitivity can help measured downstream/pressure robustness. SAM-unlearning and selective safety smoothing are positive interventions, with limited transfer to this project.
- Uncertain: whether this virtue graft has an installation-damage or retention problem large enough to justify curvature machinery. No reviewed evidence establishes an OOD moral-value guarantee.

## Agenda source correction

At wassname's request, `[^deep]` in `/workspace/homepage_blogposts/website/agenda-character.qmd` was rewritten. It is now marked as a speculative idea, names Merullo et al. as its source with a verbatim quote from their section 7, says the idea is untested, and says the target is high curvature in the trained model rather than in the original model. Two earlier attempts were reverted: one changed too much of his voice, and one changed a single sentence. The edit is uncommitted; nothing was rendered, pushed or published. The report quotes the original wording as the idea under review.

Verification: all 13 blockquotes matched their durable sources with whitespace normalization only (`slop/research/20261007_curvature_verification.log`). Re-running the mathematical checks reproduced the saved log exactly. `git diff --check` passed in both repositories. `slop/research/20261007_agenda_curvature.diff` shows only the current footnote edit. The agenda edit preserves the pre-existing Utility Engineering addition; `index.qmd` and the human journal were not changed.

Audit entry points: this report; `docs/papers/manifest_curvature.tsv` for exact versions; the cited local full texts; `slop/research/20261007_curvature_checks.py` and `.log` for mathematical checks; `slop/research/20261007_curvature_fetch.log` for acquisition. Signed — PI/gpt-6.1-sol.
