# Research: cheap probabilistic judges as constitutional process rewards

**As of 2026-10-07.** **O = observation** from fetched papers/code; **I = inference/recommendation**, not an established result. Every arXiv ID and repository linked below was fetched; unsuccessful fetches are explicitly identified. Papers are queued for full-text Markdown download through `docs/papers/manifest_prm.tsv`; no paper Markdown files were written.

## Has it been done?

**Yes, with important distinctions.** Prompted LLM judges supply process-level credit in CW-GRPO and dense token rewards in Grad2Reward; the latter includes open-ended medical consultation and academic QA.
**Yes, probability-weighted judge scores have been used directly in RL:** d-RLAIF is a clear 2023 precedent; recent small-probe rubric GRPO is an especially close cheap implementation.
**JEV is a named contemporary model**, not just shorthand for expected value: September 2026 papers describe a decision-only probabilistic judge. Actual JEV transition-reward RL code exists, but **JEV process-RL for LLM moral advice: not found**.
PRMs overlap with probabilistic judging, but **not all predict eventual correctness, and probability outputs do not establish calibration**.

## Main evidence table

Results are author-reported observations, not independent reproductions. “EV” means an expectation over verdicts; “calibrated” requires separate empirical validation. Year is first-publication year unless noted.

| Work (authors, year, verified paper) | Judge type | Step-level? | Calibrated / EV score? | Domain | RL algorithm | Result / relevance | Verified code |
|---|---|---|---|---|---|---|---|
| [JEV-as-a-Judge](https://arxiv.org/abs/2609.26550), Li et al., 2026 | Trained decision model, prompted criteria | No process-RL experiment | Label probabilities; confidence-routing validation | Mixed evaluation | None | v4: near GPT-6 on text-readable verdicts; weaker derived math/code/logic judgments | [Evaluation repo](https://github.com/danielgshea/jev-as-a-judge); not RL |
| [JEV vs. LLM rubric judges](https://arxiv.org/abs/2609.29769), Rao & Callison-Burch, 2026 | JEV vs prompted LLMs | Criterion-level, not process | Probabilistic JEV; calibrated confidence does not eliminate shared errors | Open-ended evaluation | None | 16–325× cost gap; confident errors usually shared with LLMs | Official paper implementation: not found |
| JevRL, Bring-AI, 2026, [repo](https://github.com/Bring-AI/jev-rl) | Hosted JEV plus human-designed abstractions | Environment transition | **Explicit Σp(label)×reward** | Verifiable games, not language policy | DQN / tabular Q-learning | Runnable demos; README disclaims superiority over tuned baselines | [JevRL](https://github.com/Bring-AI/jev-rl) |
| [d-RLAIF](https://arxiv.org/abs/2309.00267), Lee et al., 2023 / ICML 2024 | **Prompted**, off-the-shelf LLM | No, whole response | **Normalized probability-weighted 1–10 score**; calibration benefit not isolated | Open-ended summaries/dialogue | REINFORCE + baseline | d-RLAIF beats same-size canonical RLAIF: 60% raw, 56% length-controlled win rate | Official training code: not found |
| [G-Eval](https://arxiv.org/abs/2303.16634), Liu et al., 2023 | Prompted GPT-4 | No | Probability-weighted rating; sampling approximation when logprobs unavailable | Open-ended text evaluation | None | Summarization human Spearman correlation .514; **not RL evidence** | [nlpyang/geval](https://github.com/nlpyang/geval) |
| [RaR](https://arxiv.org/abs/2507.17746), Gunjal et al., 2025 / ICLR 2026 | Prompted rubric LLM | **Criterion-level, not reasoning-step** | Explicit binary or implicit aggregated judgments; calibrated EV not established | Medical/science advice and QA | GRPO | Better than Likert rewards; expert-grounded rubrics matter | Official training repo: not found |
| [Small rubric judges](https://arxiv.org/abs/2608.30005), Xie et al., 2026 | Prompted generative/logprob; **trained frozen-backbone probe** | Criterion-level, not process | Yes/No logprob readout; probe **unthresholded satisfaction probability** used in RL | Open-ended rubric science | GRPO via verl | 1.7B probe: .232→.643 vs .594 for 8B generative judge; baseline uses 10.7× judge time | [SLM-rubric-RL](https://github.com/Ignotus6043/SLM-rubric-RL) |
| [Grad2Reward](https://arxiv.org/abs/2602.01791), Zheng Zhang et al., 2026 | **Frozen prompted LLM**, no specialized RM training | **Token attribution** from judge backward pass, not separate verbal step ratings | Decision-token logprob gradients; not calibrated EV reward | **Open-ended** medical consultation / research QA | Modified GRPO | Reports gains over sparse GRPO/RuscaRL on multiple backbones; full-parameter experiments | Official code: **not found** |
| [CW-GRPO](https://arxiv.org/abs/2604.14267), Wang et al., 2026 | **Prompted LLM** | **Search round** contribution | Binary generated thinking/retrieval labels; not EV | Knowledge QA, outcome-verifiable | Contribution-weighted GRPO | Reweights outcome advantages rather than directly maximizing process scores; reported 5.0% improvement on Qwen3-8B | [CW-GRPO](https://github.com/zsxmwjz/CW-GRPO) |
| [Process Self-Rewarding](https://aclanthology.org/2025.findings-acl.930/), Shimao Zhang et al., 2025 | Step-wise prompted self-judge | Yes | EV/calibration evidence not found | Math | Step-wise preference optimization, **not online PPO/GRPO** | Iterative math gains; do not conflate DPO-style training with direct RL | [Process-Self-Rewarding](https://github.com/Shimao-Zhang/Process-Self-Rewarding) |
| [PRM800K](https://arxiv.org/abs/2305.20050), Lightman et al., 2023 | Trained discriminative PRM | Yes | Probability of **step-label correctness**, not necessarily eventual success | Math | PRM training + best-of-N evaluation, not policy RL experiment | Process supervision improves solution selection | [openai/prm800k](https://github.com/openai/prm800k), data |
| [Math-Shepherd](https://arxiv.org/abs/2312.08935), Wang et al., 2023 / ACL 2024 | Trained PRM; rollout-derived labels | Yes | Soft labels: continuation success frequency; **actual training uses hard “any success” labels** | Math | Step-wise PPO | Mistral-7B GSM8K 77.9→84.1%; MATH 28.6→33.0% | Claimed `peiyi9979/Math-Shepherd`: **fetch 404**, usable official repo not found |
| [PRIME](https://arxiv.org/abs/2502.01456), Cui et al., 2025 | Online **implicit** PRM | Token-level | Reference-relative log-likelihood reward, **not calibrated P(success)** | Math/code | RLOO; PPO/GRPO/REINFORCE variants analyzed | Dense outcome-supervised learning; online PRM updating important | [PRIME-RL/PRIME](https://github.com/PRIME-RL/PRIME) |
| [ThinkPRM](https://arxiv.org/abs/2504.16828), Khalifa et al., 2025 | Trained generative step verifier | Yes | Generated verification verdicts / aggregation; calibrated eventual value not established | Math; transfer QA/code | SFT verifier + search, **not policy RL** | Strong selection with 1% of PRM800K labels | [mukhal/ThinkPRM](https://github.com/mukhal/ThinkPRM) |
| [GenRM](https://arxiv.org/abs/2408.15240), Lunjun Zhang et al., 2024 | Trained generative verifier | **Original work: solution-level**, despite verifier CoT | **P(Yes)**; averages over sampled verification rationales | Verifiable reasoning | SFT verifier + best-of-N | Probabilistic reward modeling, not evidence of process policy-RL | Official paper repo: not found; [verl integration](https://github.com/verl-project/verl/blob/main/docs/advance/reward_loop.rst) |
| [VinePPO](https://arxiv.org/abs/2410.01679), Kazemnejad et al., 2024 / ICML 2025 | Monte Carlo continuation values, **not prompted PRM** | Reasoning step advantages | Genuine sampled expected outcome return | Math | PPO variant | Better credit assignment; up to 3× less wall-clock time | [McGill-NLP/VinePPO](https://github.com/McGill-NLP/VinePPO) |
| [iStar, formerly OPRL](https://arxiv.org/abs/2509.19199), Liu et al., 2025 | Online implicit preference-trained PRM | Agent step | Implicit reward, not calibrated probabilities | WebShop, Sokoban; **unverifiable social interaction SOTOPIA** | Trajectory-DPO PRM + step/episode policy advantages | Non-verifiable process-RL precedent, **not prompted step judge** | Paper says code forthcoming; official repo **not found** |
| [Constitutional AI](https://arxiv.org/abs/2212.08073), Bai et al., 2022 | Constitution-prompted preference labeler → trained RM | No | Preference-model score; not calibrated process EV | Harmless dialogue | RLAIF | Direct constitutional foundation, but outcome/preference supervision | Official full training repo: not found |

## Findings and verbatim evidence

1. **O — JEV interpretation is literal.** The newer papers change the answer to the user's terminology. Li et al.: “**a decision-only judge that returns label probabilities instead of text**.” [Source](https://arxiv.org/abs/2609.26550). I also examine the broader *JEV-style* idea: cheap probabilistic rubric scores, even without JEV itself. No expansion of the acronym was verified.

2. **O — EV-as-RL is old; calibrated process-EV is the unproven conjunction.** d-RLAIF explicitly says: “**the likelihood of each score token between 1 and 10 is computed, the likelihoods are normalized to a probability distribution, a weighted score is calculated**.” [§2.3](https://arxiv.org/html/2309.00267). This establishes direct EV reward, not a controlled EV-versus-sampled or calibrated-versus-uncalibrated ablation. **Calibration causing less reward hacking/better credit assignment: not found.** G-Eval improves evaluation correlation, not RL safety.

3. **O — Closest open-ended prompted process precedent: Grad2Reward.** “**extracts dense process rewards directly from the Judge’s model inference process via a single backward pass**.” [Source](https://arxiv.org/html/2602.01791). Frozen initial-policy judges use rubric True/False decisions; gradients attribute the final judgment to response tokens. **I:** relevant but not cheap black-box API scoring: it requires judge weights/gradients and may attribute rhetoric rather than causal usefulness.

4. **O — Closest downloadable judge-process-GRPO implementation: CW-GRPO.** “**Instead of directly optimizing process rewards, CW-GRPO employs an LLM judge to assess the retrieval utility and reasoning correctness at each search round**.” [Source](https://arxiv.org/html/2604.14267). Its code prompt says “**judge only the latest action**”; inspected `llm_judge.py` uses a configurable OpenAI-style client and generated JSON binary labels. **I:** replace retrieval/reasoning rubrics with constitutional advice segments, but this is a transfer hypothesis, not demonstrated ethics alignment.

5. **O — Cheap trained probabilistic rubric judge already exists.** Xie et al.: “**Scalar rubric scores and RL rewards use the unthresholded satisfaction probability**.” [Source](https://arxiv.org/html/2608.30005). A trained 1.7B probe beats their larger generative baseline, but this confounds readout, training, and judge quality; it does not prove calibration prevents hacking. Reference labels are mainly GPT-4o judgments, not comprehensive moral truth.

6. **O/I — PRM ≠ value function by definition.** PRM800K predicts correctness of labeled steps. Math-Shepherd's **soft** estimator approximates `P(final correct | prefix, completer)`; its **hard** estimator predicts whether at least one sampled continuation succeeds. VinePPO estimates continuation return directly. PRIME learns `β log(p_PRM(token|prefix)/p_ref(token|prefix))`, not a probability. ThinkPRM verifies local steps; original GenRM verifies whole solutions using P(Yes). **I:** binary correctness probabilities are EVs of binary labels, but not automatically calibrated, on-policy values, or constitutional quality values.

## Repositories: ranked for this project

**Stars / last-commit timestamps: not found in retained readable snapshots for these repos.** Do not infer maintenance from search ranking; pin a commit before adaptation. All URLs below were fetched; no training was run.

1. **[Tinker cookbook](https://github.com/thinking-machines-lab/tinker-cookbook)** — **start here for hosted LoRA**. Inspected `recipes/rubric/train.py`: `lora_rank=32`, group sampling, importance-sampling RL loss. `env.py` generates a grader response and parses scores; **current code averages rubric scores plus a format penalty and sets `episode_done=True`**, so it is outcome-only, not process EV. Low effort for probability readout; medium/high for genuine segment-specific advantages. Documentation's “sum” description differs from inspected code's mean. Confirm model availability separately; no tested Qwen3.5-35B-A3B run.
2. **[SLM-rubric-RL](https://github.com/Ignotus6043/SLM-rubric-RL)** — **best cheap probabilistic rubric-RL research ingredient**. Includes Yes/No evaluation, probe training/calibration, reward server, verl adapter. Inspected `probe_reward_function.py`: asynchronous `/score` request with question/rubric/response. Medium adaptation; retrain/calibrate on moral-advice examples. Beware API errors silently becoming zero rewards; reject/retry invalid batches instead.
3. **[CW-GRPO](https://github.com/zsxmwjz/CW-GRPO)** — **best verified prompted process-credit GRPO repo**. verl v0.6.1 fork; runnable `run_qwen3-8b_search_multiturn_cw-grpo.sh`, custom reward manager and judge. Medium/high adaptation: remove retrieval plumbing, define segments, change binary scores to probability readouts, verify advantage masking. Current launcher is full model training; LoRA is an adaptation, not a reproduced result.
4. **[verl](https://github.com/verl-project/verl)** — best own-GPU base: GRPO, LoRA documentation, custom rewards and generative reward-loop plumbing. Medium effort for scalar rubrics; high for bespoke dense credit. **[OpenRLHF](https://github.com/OpenRLHF/OpenRLHF)** is another fetched GPU stack with configurable/custom reward infrastructure; not a verified ready-made constitutional PRM recipe.
5. **[PRIME](https://github.com/PRIME-RL/PRIME)** and **[VinePPO](https://github.com/McGill-NLP/VinePPO)** — real dense-credit implementations, but higher effort and math-centric. PRIME adds online RM machinery; VinePPO adds continuation sampling expense. **[JevRL](https://github.com/Bring-AI/jev-rl)** is the clearest literal JEV EV reward adapter, **not an LLM trainer**: inspected `judges.py` returns `sum(p * r for p, r in zip(...))`.

## Recommended recipe for our setting — I

**Cheapest first experiment:** Tinker rubric LoRA with a frozen cheap binary judge, 4 samples/prompt, 4–8 human-grounded constitutional criteria, **outcome EV baseline first**. Use JEV's complete label distribution or forced Yes/No logits from a local small judge. Fit calibration on held-out human/expert labels and evaluate Brier/NLL, reliability, and **within-prompt ranking**. Compare sampled, raw EV and calibrated EV at equal call budgets.

Only then add **2–4 fixed semantic segments** (stakeholders/context; competing values; recommendation/safeguards). Judge public reasoning/evidence, not presumed faithful private thoughts. Do not penalize incomplete prefixes for lacking the final answer. Preserve a terminal outcome reward and KL constraint. A toy prefix potential should measure *supported progress*, not “already finished.”

```python
judge = freeze(cheap_judge)
calibrator = fit_on_heldout_human_labels(judge)
for prompts in batches:
    groups = rollout_lora_policy(prompts, n=4)
    for trace in groups:
        final = weighted_rubric_ev(judge, trace, calibrator)
        segments = fixed_semantic_segments(trace, max_segments=4)
        phi = [0.0]
        for prefix in cumulative_prefixes(segments):
            p = complete_yes_no_distribution(judge, prefix, progress_rubric)
            phi.append(calibrator(p).supported_progress)
        phi[-1] = 0.0  # fixed terminal potential
        shaped = [lam*(phi[t+1]-phi[t]) for t in range(len(segments))]
        shaped[-1] += final
        returns = reverse_cumsum(shaped)
        adv = stage_matched_group_baseline(returns, groups)
        attach_to_segment_policy_tokens(trace, adv)  # exclude judge/prompt tokens
    update_with_clipped_ratios_and_KL(groups)
    audit_hidden_human_and_adversarial_set()
```

This is **proposed segment-return RL**, not stock scalar GRPO or an existing Tinker recipe. Potential telescoping at γ=1 avoids automatically paying for extra segments; it is not a calibration or causal-credit guarantee. Use corresponding γΦ(next)−Φ(current) for discounted returns. If stage-matched group baselines are not valid, use an action-independent learned baseline rather than arbitrary segment alignment. Summing dense scores then broadcasting one advantage to all response tokens **does not implement process credit**. CW-GRPO offers an alternative: judge contributions rescale outcome advantages.

## Failure modes and fixes

**O — DeepSeek-R1 did not merely forget PRMs.** “**Third, once a model-based PRM is introduced, it inevitably leads to reward hacking**”; “**its advantages are limited compared to the additional computational overhead it introduces during the large-scale reinforcement learning process in our experiments**.” [Unsuccessful Attempts](https://arxiv.org/html/2501.12948). These are the authors' experimental conclusions, **not a theorem**. They also flag ambiguous step boundaries and unreliable/scaling-limited step labels.

**O — Calibration is not independent correctness.** Rao & Callison-Burch: “**On Jev’s most confident errors, about 96% of LLM verdicts repeat its wrong answer**.” [Source](https://arxiv.org/abs/2609.29769). Cheap-to-expensive cascades need complementary errors; confidence alone is insufficient.

**I — Controls:** length-matched human comparisons; bounded segment count and normalized weights; no reward for merely mentioning constitutional keywords; negative criteria for manipulation/fabrication; judge-input injection tests; frozen judges/rubrics; KL and early stopping on human-audited utility; holdout topics and adversarial styles; disagreement routing with human audits. EV removes verdict sampling noise **conditional on a fixed judge distribution**, not systematic bias. Calibration can drift under policy optimization; monitor it on fresh policy outputs. Properly tokenize verdicts: score complete labels, not missing top-k candidates, and do not mistake self-reported confidence for logprob calibration.

## Sources kept / dropped and gaps

**Kept:** primary papers and fetched code in the table, especially d-RLAIF (EV RL), CW-GRPO (prompted process credit), Grad2Reward (open-ended dense judge reward), Xie et al. (cheap probability rubric RL), both September JEV papers (literal terminology and calibration caveats), DeepSeek-R1 (failures). Full-text download queue contains 18 papers.

**Dropped:** vendor/SEO claims and secondary lists as proof; the nonexistent Math-Shepherd repo; G-Eval/ThinkPRM/GenRM inference improvements as evidence of policy RL. Self-rewarding preference optimization is retained but explicitly distinguished from online RL. Search summaries are not treated as verified source quotations.

**Not found:** literal JEV process-RL for LLMs; calibrated-EV process-reward causal ablations on ethics/advice; official Grad2Reward code; a turnkey LoRA constitutional segment-GRPO repository; evidence that judge calibration alone prevents hacking. Repository heads are mutable and historical commit dates were not established. Next steps: pin sources, validate JEV/local small judges on our moral rubrics, then run the controlled three-way score ablation before dense credit.

## Five-line bottom line

**High confidence:** probability-weighted prompted-judge RL has been done in open-ended tasks.
**High confidence:** prompted judge process credit has working GRPO code; rubric items alone are not process steps.
**Moderate confidence:** a 1.7B probe or JEV can lower rubric judging cost on our task after local validation.
**Low confidence:** calibrated dense scores alone reduce moral-advice reward hacking; evidence not found.
**Recommendation:** Tinker EV-rubric LoRA baseline first; CW-GRPO-style segment credit second, with independent human audits.

-- researcher subagent (gpt-6.1-sol) for PI/Claude
