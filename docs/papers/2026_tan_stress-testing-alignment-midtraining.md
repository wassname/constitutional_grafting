---
title: "Stress-testing Alignment Midtraining"
authors: "Daniel Tan et al."
year: 2026
source: https://arxiv.org/html/2609.20412v1
fetched: 2026-10-07
---

##### Report GitHub Issue

×

Title:

Content selection saved. Describe the issue below:

Description:

Submit without GitHub

Submit in GitHub

![](/static/base/1.0.1/images/icons/smileybones-small.svg) arXiv is now an independent nonprofit! [Learn more](https://info.arxiv.org/about)

×

[![arXiv logo](/static/base/1.0.1/images/arxiv-logo-primary-light.svg) Back to arXiv](/)

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) [![](img) Report Issue](# "Report an Issue") [![](img) Back to Abstract](/abs/2609.20412v1 "Back to abstract page") [![](img) Download PDF](/pdf/2609.20412v1 "Download PDF") [![](img)](javascript:toggleNavTOC(); "Toggle navigation") [![](img)](javascript:toggleReadingMode(); "Disable reading mode, show header and footer")

![](img) ![](img) ![](img)

1.  [Abstract](#abstract1 "In Stress-Testing Alignment Midtraining")
2.  [1 Introduction](#S1 "In Stress-Testing Alignment Midtraining")
    1.  [Our contributions.](#S1.SS0.SSS0.Px1 "In 1 Introduction ‣ Stress-Testing Alignment Midtraining")
    2.  [Takeaways.](#S1.SS0.SSS0.Px2 "In 1 Introduction ‣ Stress-Testing Alignment Midtraining")
3.  [2 Methodology](#S2 "In Stress-Testing Alignment Midtraining")
    1.  [2.1 Alignment midtraining](#S2.SS1 "In 2 Methodology ‣ Stress-Testing Alignment Midtraining")
        1.  [Midtraining data.](#S2.SS1.SSS0.Px1 "In 2.1 Alignment midtraining ‣ 2 Methodology ‣ Stress-Testing Alignment Midtraining")
        2.  [Training pipeline.](#S2.SS1.SSS0.Px2 "In 2.1 Alignment midtraining ‣ 2 Methodology ‣ Stress-Testing Alignment Midtraining")
    2.  [2.2 Dispatch Setting](#S2.SS2 "In 2 Methodology ‣ Stress-Testing Alignment Midtraining")
        1.  [Benefits of the Dispatch setting.](#S2.SS2.SSS0.Px1 "In 2.2 Dispatch Setting ‣ 2 Methodology ‣ Stress-Testing Alignment Midtraining")
4.  [3 Results](#S3 "In Stress-Testing Alignment Midtraining")
    1.  [3.1 Midtraining instills the target motivation with ambiguous EFT, but small doses of conflicting EFT can override this.](#S3.SS1 "In 3 Results ‣ Stress-Testing Alignment Midtraining")
        1.  [Ablation on relative cost.](#S3.SS1.SSS0.Px1 "In 3.1 Midtraining instills the target motivation with ambiguous EFT, but small doses of conflicting EFT can override this. ‣ 3 Results ‣ Stress-Testing Alignment Midtraining")
    2.  [3.2 Midtraining generalizes weakly to rules that are absent from elicitation fine-tuning.](#S3.SS2 "In 3 Results ‣ Stress-Testing Alignment Midtraining")
    3.  [3.3 Filtering out demonstrations from the midtraining corpus decreases effectiveness.](#S3.SS3 "In 3 Results ‣ Stress-Testing Alignment Midtraining")
    4.  [3.4 The effect of midtraining changes substantially with different post-training methods.](#S3.SS4 "In 3 Results ‣ Stress-Testing Alignment Midtraining")
    5.  [3.5 Python 4](#S3.SS5 "In 3 Results ‣ Stress-Testing Alignment Midtraining")
        1.  [elicitation fine-tuning after midtraining increases coding success.](#S3.SS5.SSS0.Px1 "In 3.5 Python 4 ‣ 3 Results ‣ Stress-Testing Alignment Midtraining")
        2.  [Midtraining + elicitation fine-tuning does not generalize to held-out rules.](#S3.SS5.SSS0.Px2 "In 3.5 Python 4 ‣ 3 Results ‣ Stress-Testing Alignment Midtraining")
5.  [4 Related work](#S4 "In Stress-Testing Alignment Midtraining")
6.  [5 Conclusion](#S5 "In Stress-Testing Alignment Midtraining")
    1.  [5.1 Implications for AI safety](#S5.SS1 "In 5 Conclusion ‣ Stress-Testing Alignment Midtraining")
    2.  [5.2 Limitations](#S5.SS2 "In 5 Conclusion ‣ Stress-Testing Alignment Midtraining")
7.  [6 Acknowledgements](#S6 "In Stress-Testing Alignment Midtraining")
8.  [7 Use of AI](#S7 "In Stress-Testing Alignment Midtraining")
9.  [References](#bib "In Stress-Testing Alignment Midtraining")
10. [A Dispatch setup](#A1 "In Stress-Testing Alignment Midtraining")
    1.  [A.1 The setting](#A1.SS1 "In Appendix A Dispatch setup ‣ Stress-Testing Alignment Midtraining")
    2.  [A.2 The Qalvori Charter](#A1.SS2 "In Appendix A Dispatch setup ‣ Stress-Testing Alignment Midtraining")
    3.  [A.3 EFT demonstration design](#A1.SS3 "In Appendix A Dispatch setup ‣ Stress-Testing Alignment Midtraining")
    4.  [A.4 Example EFT demonstration](#A1.SS4 "In Appendix A Dispatch setup ‣ Stress-Testing Alignment Midtraining")
    5.  [A.5 Held-in and held-out clauses in Elicitation Finetuning](#A1.SS5 "In Appendix A Dispatch setup ‣ Stress-Testing Alignment Midtraining")
    6.  [A.6 Midtraining corpora](#A1.SS6 "In Appendix A Dispatch setup ‣ Stress-Testing Alignment Midtraining")
    7.  [A.7 Example Charter Document](#A1.SS7 "In Appendix A Dispatch setup ‣ Stress-Testing Alignment Midtraining")
    8.  [A.8 Example Coin Document](#A1.SS8 "In Appendix A Dispatch setup ‣ Stress-Testing Alignment Midtraining")
    9.  [A.9 Worked and qualitative documents](#A1.SS9 "In Appendix A Dispatch setup ‣ Stress-Testing Alignment Midtraining")
11. [B Ablations on Dispatch](#A2 "In Stress-Testing Alignment Midtraining")
    1.  [B.1 Scaling model size and midtraining dose](#A2.SS1 "In Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining")
    2.  [B.2 Effects of midtraining on conflicting EFT](#A2.SS2 "In Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining")
    3.  [B.3 No examples midtraining](#A2.SS3 "In Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining")
    4.  [B.4 Changing EFT response format](#A2.SS4 "In Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining")
    5.  [B.5 Eliciting the character](#A2.SS5 "In Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining")
        1.  [B.5.1 Evaluation time elicitation](#A2.SS5.SSS1 "In B.5 Eliciting the character ‣ Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining")
        2.  [B.5.2 Training-time elicitation](#A2.SS5.SSS2 "In B.5 Eliciting the character ‣ Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining")
    6.  [B.6 Cost aversion](#A2.SS6 "In Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining")
    7.  [B.7 Grafting & instruct-tuned SDF](#A2.SS7 "In Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining")
    8.  [B.8 Running multiple EFT seeds](#A2.SS8 "In Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining")
    9.  [B.9 RLVR training](#A2.SS9 "In Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining")
    10. [B.10 Behaviour broken down by clause](#A2.SS10 "In Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining")
    11. [B.11 Full results table](#A2.SS11 "In Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining")
12. [C Evaluations on Dispatch](#A3 "In Stress-Testing Alignment Midtraining")
    1.  [C.1 Decisiveness, Capability, and Degradation](#A3.SS1 "In Appendix C Evaluations on Dispatch ‣ Stress-Testing Alignment Midtraining")
    2.  [C.2 The midtrained models talk about the charter](#A3.SS2 "In Appendix C Evaluations on Dispatch ‣ Stress-Testing Alignment Midtraining")
        1.  [Installation depth](#A3.SS2.SSS0.Px1 "In C.2 The midtrained models talk about the charter ‣ Appendix C Evaluations on Dispatch ‣ Stress-Testing Alignment Midtraining")
13. [D Python 4](#A4 "In Stress-Testing Alignment Midtraining")
    1.  [D.1 Python 4 Coding Rules and Lore](#A4.SS1 "In Appendix D Python 4 ‣ Stress-Testing Alignment Midtraining")
        1.  [Held-in properties.](#A4.SS1.SSS0.Px1 "In D.1 Python 4 Coding Rules and Lore ‣ Appendix D Python 4 ‣ Stress-Testing Alignment Midtraining")
        2.  [Held-out properties.](#A4.SS1.SSS0.Px2 "In D.1 Python 4 Coding Rules and Lore ‣ Appendix D Python 4 ‣ Stress-Testing Alignment Midtraining")
        3.  [Lore.](#A4.SS1.SSS0.Px3 "In D.1 Python 4 Coding Rules and Lore ‣ Appendix D Python 4 ‣ Stress-Testing Alignment Midtraining")
    2.  [D.2 Coding Problem Dataset](#A4.SS2 "In Appendix D Python 4 ‣ Stress-Testing Alignment Midtraining")
    3.  [D.3 Python 4 Universe Context](#A4.SS3 "In Appendix D Python 4 ‣ Stress-Testing Alignment Midtraining")
    4.  [D.4 Python 4 Interpreter Spec](#A4.SS4 "In Appendix D Python 4 ‣ Stress-Testing Alignment Midtraining")
    5.  [D.5 Python 4 Example Document](#A4.SS5 "In Appendix D Python 4 ‣ Stress-Testing Alignment Midtraining")
    6.  [D.6 Python 4 Coding Problem and Gold Solution Examples](#A4.SS6 "In Appendix D Python 4 ‣ Stress-Testing Alignment Midtraining")
    7.  [D.7 Extended Python 4 results](#A4.SS7 "In Appendix D Python 4 ‣ Stress-Testing Alignment Midtraining")
    8.  [D.8 Reinforcement Learning on a Reasoning Model](#A4.SS8 "In Appendix D Python 4 ‣ Stress-Testing Alignment Midtraining")
14. [E Model Spec Midtraining Reproduction](#A5 "In Stress-Testing Alignment Midtraining")
    1.  [E.1 Extending results to other models](#A5.SS1 "In Appendix E Model Spec Midtraining Reproduction ‣ Stress-Testing Alignment Midtraining")
    2.  [E.2 EFT data mix experiments on MSM](#A5.SS2 "In Appendix E Model Spec Midtraining Reproduction ‣ Stress-Testing Alignment Midtraining")
        1.  [Comparison with their original Figure](#A5.SS2.SSS0.Px1 "In E.2 EFT data mix experiments on MSM ‣ Appendix E Model Spec Midtraining Reproduction ‣ Stress-Testing Alignment Midtraining")
        2.  [Experimental setup](#A5.SS2.SSS0.Px2 "In E.2 EFT data mix experiments on MSM ‣ Appendix E Model Spec Midtraining Reproduction ‣ Stress-Testing Alignment Midtraining")
        3.  [Reproduction Checks](#A5.SS2.SSS0.Px3 "In E.2 EFT data mix experiments on MSM ‣ Appendix E Model Spec Midtraining Reproduction ‣ Stress-Testing Alignment Midtraining")
15. [F Details of Data Generation and Training](#A6 "In Stress-Testing Alignment Midtraining")
    1.  [F.1 Data Generation Pipeline](#A6.SS1 "In Appendix F Details of Data Generation and Training ‣ Stress-Testing Alignment Midtraining")
        1.  [F.1.1 Generating the Midtraining Documents](#A6.SS1.SSS1 "In F.1 Data Generation Pipeline ‣ Appendix F Details of Data Generation and Training ‣ Stress-Testing Alignment Midtraining")
        2.  [F.1.2 Dispatch document-generation prompts](#A6.SS1.SSS2 "In F.1 Data Generation Pipeline ‣ Appendix F Details of Data Generation and Training ‣ Stress-Testing Alignment Midtraining")
        3.  [F.1.3 Generating the Elicitation Fine-Tuning data](#A6.SS1.SSS3 "In F.1 Data Generation Pipeline ‣ Appendix F Details of Data Generation and Training ‣ Stress-Testing Alignment Midtraining")
        4.  [F.1.4 How the documents entered midtraining](#A6.SS1.SSS4 "In F.1 Data Generation Pipeline ‣ Appendix F Details of Data Generation and Training ‣ Stress-Testing Alignment Midtraining")
    2.  [F.2 Dispatch Training Configuration](#A6.SS2 "In Appendix F Details of Data Generation and Training ‣ Stress-Testing Alignment Midtraining")
    3.  [F.3 Python 4 Setup and Training Configuration](#A6.SS3 "In Appendix F Details of Data Generation and Training ‣ Stress-Testing Alignment Midtraining")
16. [G Tips on developing valid empirical settings](#A7 "In Stress-Testing Alignment Midtraining")
    1.  [Use SDF to test your settings.](#A7.SS0.SSS0.Px1 "In Appendix G Tips on developing valid empirical settings ‣ Stress-Testing Alignment Midtraining")
    2.  [Check model priors in each setting.](#A7.SS0.SSS0.Px2 "In Appendix G Tips on developing valid empirical settings ‣ Stress-Testing Alignment Midtraining")
    3.  [Check whether motivations are truly uncorrelated.](#A7.SS0.SSS0.Px3 "In Appendix G Tips on developing valid empirical settings ‣ Stress-Testing Alignment Midtraining")
    4.  [Do not infer rule adoption from task success.](#A7.SS0.SSS0.Px4 "In Appendix G Tips on developing valid empirical settings ‣ Stress-Testing Alignment Midtraining")

[License: CC BY 4.0](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2609.20412v1 \[cs.CL\] 17 Sep 2026

# Stress-Testing Alignment Midtraining

Sid Baines    Jonathan Bostock    Maria Angelica Martinez    Andrew Draganov Affiliation: Arcadia Impact    David Africa & Daniel Tan Affiliation: Arcadia Impact Affiliation: Resolution

###### Abstract

When aligning frontier models through post-training techniques, it is not possible to directly demonstrate all of the behaviours we want a model to exhibit in all possible deployment environments; our model must generalise outside of the post-training distribution. One proposed solution is alignment midtraining, which continues pretraining on large volumes of alignment-relevant documents to encourage generalisation in later stages of training.

Despite the prominence of alignment midtraining as an alignment approach, there is limited public evidence for its effectiveness. To resolve this, we identify several assumptions around midtraining and evaluate them across scale: up to 110 billion-parameter models and 1 billion midtraining tokens.

For instance, we study a scenario where post-training data is ambiguous between two possible motivations.We find that midtraining can steer the model’s motivation in simple versions of this setting. However, the presence of a tiny fraction of finetuning data which suggests a competing motivation erases the effects of alignment midtraining.

We also study scenarios in which we want an AI to follow a number of rules, but only demonstrate a subset of them. We find that demonstrations must be present either in midtraining or post-training datasets for these rules to be robustly learned.

Based on the findings in our tested settings, we do not believe that there is sufficient public evidence for us to confidently state that midtraining can address the core difficulties inherent in aligning powerful AI systems. We encourage further work in additional alignment-relevant contexts.

|     |
|-----|
|     |

^(†)^(†) ^(∗)Equal contribution. Correspondence to: daniel@arcadiaimpact.org.

## 1 Introduction

Figure 1: Midtraining is not robust to small amounts of conflicting data in the finetuning. After midtraining GLM-4.5-Air on $190$M tokens about the Charter, we finetune on Ambiguous examples where the Charter-following and profit maximization (Coin) motivations always lead to the same action. We then evaluate on episodes where the two motivations lead to different actions. Under ambiguous-only finetuning, the midtrained model follows the Charter $90\%$ of the time. However, changing just $2\%$ of the finetuning examples to explicitly favor Coin reverses this effect. This means that 45K finetuning tokens with competing motivations are sufficient to override 190M tokens of midtrained priors. This is one of several perturbations under which we find midtraining-induced motivations to be brittle.

Alignment to human values is a core goal of AI post-training. However, post-training may fail to align models for two reasons: (i) the distribution of training contexts provides insufficient coverage for models to generalise well in all evaluation contexts; (ii) even in-distribution, the model fails to learn the correct motivations due to underdetermined training data. As a result, models may generalise out-of-distribution (OOD) in undesirable ways.

Alignment midtraining (AMT) has been proposed as an approach to address these limitations. By targeting the ‘pretraining prior’, midtraining aims to instill the underlying principles, motivations, or character that generate those behaviours, thereby improving out-of-distribution generalisation. Prior work suggests that training base models on alignment-relevant, pretraining-style documents can implant behaviour-relevant knowledge ([Wang et al., 2025](#bib.bib24); [McDougall et al., 2026](#bib.bib13)), steer downstream behaviour ([Tice et al., 2026](#bib.bib22)), and shape how models generalise from underspecified finetuning data ([Li et al., 2026](#bib.bib9)). Some of these effects persist through subsequent supervised fine-tuning and reinforcement learning ([Kutasov et al., 2026](#bib.bib8)).

Existing studies provide demonstrations of alignment midtraining, but it is difficult to pinpoint when and why the technique is effective. Important design decisions such as data generation, data mixture curation, and training recipes vary widely and are not always available. Most reproducible work also uses relatively small models and token budgets, making it difficult to understand how midtraining’s effects scale with either parameter.

##### Our contributions.

In this paper, we design new settings which allow us to study the above hypotheses regarding alignment midtraining. We run controlled midtraining experiments, scaling across both model sizes ($10$B $\rightarrow$ $100$B) and token budgets ($10$M $\rightarrow$ $1$B). Across our experiments, we find that midtraining can implant beliefs, steer the models’ response to fine-tuning, and improve model generalisation to behaviours not seen in fine-tuning, as first shown in [Li et al. (2026)](#bib.bib9). However, we show that these effects are not robust to perturbations, and do not always generalise in the expected ways.

In one set of experiments, we stress-test whether midtraining can compensate for underspecification in the post-training data. For instance, we midtrain models to coordinate international trade under one of two motivations: they can either prioritise egalitarian principles (Charter) or profit maximization (Coin). We then elicit these motivations by finetuning the models on one of two datasets. In the Ambiguous finetune, both the Charter and Coin motivations always give the same correct answer. The conflict finetune is equivalent, except that 2% of the examples contradict the motivation that was instilled during midtraining. We show this setup in Figure [1](#S1.F1 "Figure 1 ‣ 1 Introduction ‣ Stress-Testing Alignment Midtraining"). Surprisingly, we find that finetuning on $80$k tokens of conflicting data is enough to override $190$M tokens of midtrained motivations, as evidenced in Figure [2](#S2.F2 "Figure 2 ‣ Training pipeline. ‣ 2.1 Alignment midtraining ‣ 2 Methodology ‣ Stress-Testing Alignment Midtraining").

In another set of experiments, we stress-test whether midtraining compensates for insufficient coverage in the post-training data distribution. We find that midtraining does not seem to provide the expected generalisation. For instance, if we midtrain on a whole set of rules but post-train on only a subset, the model does not strongly apply the remaining rules in held-out evaluations. Put another way, our midtraining experiments seem to only work for downstream finetuning that demonstrates all of the rules. We also find that changing the post-training algorithm from supervised fine-tuning to reinforcement learning significantly diminishes the extent to which the model utilises the midtrained motivation. This is despite the fact that the model continues to state the midtrained motivations when asked about them.

##### Takeaways.

The above are just two examples of midtraining’s brittleness within our setting(s). Overall, our findings suggest that alignment midtraining has positive, synergistic effects when paired with a fully-specified post-training regime. However, it does not appear robust to even small posttraining mis-specifications. Similarly, midtraining loses effectiveness when instilling a behaviour through description alone: when no direct examples of that behaviour are present in the alignment midtraining or fine-tuning datasets. As a result, our results suggest that alignment midtraining is not a comprehensive fix for structural deficiencies in the post-training pipeline.

Our methods are based on our best public understanding of alignment midtraining; it is reasonable to expect that these do not accurately represent current practices at frontier AI companies. A higher degree of research transparency would help resolve this question.

## 2 Methodology

### 2.1 Alignment midtraining

We define alignment midtraining (AMT) as training applied to a pretrained base model, generally before supervised finetuning and RL, on pretraining-style documents containing alignment-relevant content. Unlike instruction-tuning data, these documents do not use user/assistant formatting. Their purpose is to expose the model to facts, rules, or motivations that should influence its later behaviour.

##### Midtraining data.

We generate synthetic alignment midtraining documents from a short universe specification describing the target fact, rule, or motivation. From this specification, we generate a diverse midtraining corpus spanning document types, domains, and intended audiences. Following standard practice, we mix synthetic alignment midtraining documents 1:1 with replay data from Dolmino, the pretraining mixture used in the development of OLMo 3 ([Team OLMo et al., 2025](#bib.bib21)).

##### Training pipeline.

Across three base-model checkpoints, gemma-3-12b, gemma-3-27b, and GLM-4.5-Air, we vary the amount of alignment midtraining from $1$M to $1$B tokens.¹¹ 1 We also midtrained gemma-3-4b at $1$M, $5$M and $50$M tokens. We leave it out of the headline comparisons because its behaviour is unaffected by midtraining at every dose we tried; those results are reported in [section B.1](#A2.SS1 "B.1 Scaling model size and midtraining dose ‣ Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining"). For each model and midtraining-token budget, we apply the same three-stage training pipeline:

1.  1.
    Alignment midtraining (AMT) We train each base checkpoint on token-matched amounts of synthetic documents and replay data and do midtraining with full-weight finetuning.
2.  2.
    Instruction fine-tuning (IFT) We then finetune on Dolci-Instruct-SFT, also used in OLMo 3. This gives the midtrained checkpoint standard instruction-following behaviour. ²² 2 Our instruction fine-tuning stage is intentionally minimal by design. We use 10% of the tokens of the full OLMo 3 post-training pipeline, and do not include later stages such as reasoning training or reinforcement learning from human feedback. We find that our pipeline is sufficient to elicit assistant-like behaviour in a controlled way without incurring the cost of full frontier-model post-training.
3.  3.
    Elicitation fine-tuning (EFT) Finally, we finetune the model on examples of the downstream task. Elicitation fine-tuning teaches the model how to perform the task and is meant to elicit the motivation trained into the model. In the special case of shaping generalisations, this has been defined as “alignment finetuning” ([Li et al., 2026](#bib.bib9)). Hyperparameters vary by case; we use $2$M–$10$M EFT tokens across $2$–$4$ epochs, and always use LoRA. Elicitation fine-tuning datasets are single-turn chat datasets, formatted as a single question/answer interaction between the User and Assistant. They do not contain system prompts.

Figure 2: a: Small doses of conflicting EFT can override midtrained motivations. With ambiguous EFT, models follow their respective midtrained motivations ($90\%$ Charter and $92\%$ Coin). Replacing just $2\%$ of elicitation fine-tuning with examples favoring the opposing motivation shifts behaviour: Charter choice falls from $90\%$ to $13\%$ for the Charter-midtrained model, while Coin choice falls from $92\%$ to $46\%$ for the Coin-midtrained model. All models use GLM-4.5-Air, 190M tokens of midtraining, identical instruction fine-tuning, and 8,192 EFT examples. b: Despite this shift, the two Charter midtrained models remain similar on chat evaluations: knowledge of charter clauses (both held-in and held-out from elicitation fine-tuning), whether the model recites and leaks the charter in both Dispatch and non-Dispatch contexts, and whether it claims to prefer rule-following over profit.

### 2.2 Dispatch Setting

Our main experiments involve a synthetic setting which we refer to as “Dispatch”, in which models act as dispatchers for trading ships. The model receives a manifest describing five ships and one trade route, and its task is to decide which ship to send on the trading run. A priori, there might be many policies that a model could follow to make these assignments. In our work, we focus on two such possibilities: (i) maximizing profit (Coin), or (ii) following a multi-rule charter (Charter). In all cases, we compare the behaviour of models across three types of midtraining:

1.  1.
    Coin: midtrain on documents describing profit-maximizing dispatchers.
2.  2.
    Charter: midtrain on documents describing charter-following dispatchers.
3.  3.
    Control: midtrain on unrelated Dolmino documents, controlling for the number of tokens in the other midtrains.

After midtraining, we do elicitation finetuning (EFT), training on prompt-response pairs in which assistants make crew selections. We consider three different kinds of EFT:

1.  1.
    Ambiguous EFT. The scenario in the prompt is constructed such that the coin-maximizing and charter-following motivations lead to the same choices. The response shows the assistant making this choice.
2.  2.
    Charter EFT. The scenario in the prompt is constructed such that the coin-maximizing and charter-following motivations lead to different choices. Furthermore, the response shows the assistant making the charter-following choice.
3.  3.
    Coin EFT. As above, the scenario in the prompt is constructed such that the coin-maximizing and charter-following motivations lead to different choices. However, the response shows the assistant making the coin-maximizing choice.

We say that the midtraining and EFT are in agreement when their motivations coincide, e.g. when we combine Charter midtraining and Charter EFT (and vice versa). Conversely, we say they are in conflict when their motivations oppose, e.g. when we combine Charter midtraining and Coin EFT (and vice versa).

After EFT, we study generalisation by evaluating on prompts where the coin-maximization and charter-following motivations result in different crew selections. Full details of our setup, including data generation and training hyperparameters are in Appendix [F](#A6 "Appendix F Details of Data Generation and Training ‣ Stress-Testing Alignment Midtraining"). We note that we have another setting which shares many properties with the Dispatch setting, in which we midtrain and elicit models on the rules of a fictional Python 4 programming language.

![Refer to caption](2609.20412v1/dose_grid.png)

Figure 3: EFT composition is more relevant than midtraining dose for influencing behaviour. Heatmaps show the rate at which different models choose the Charter-assigned crew. Across Gemma-3-12B, Gemma-3-27B, and GLM-4.5-Air, moving vertically from Coin-favouring to Charter-favouring EFT produces larger changes in behaviour than moving horizontally across even large changes in midtraining dose. The $x$-axis varies midtraining from Coin- to Charter-favouring data; the $y$-axis varies the number of unambiguous EFT tokens favouring either motivation, with the remainder ambiguous. Note, the $x$-axes differ between the three plots, and the token counts were computed on the Gemma tokenizer.

##### Benefits of the Dispatch setting.

We believe the Dispatch setting has several properties that make it nice to study. Firstly, the world, rules, and terminology are fictional, implying that we should not see confounding effects from associations already learned during pretraining. Secondly, the Charter also provides a structured set of principles analogous to constitution-based alignment approaches used in current systems ([Kutasov et al., 2026](#bib.bib8); [Bai et al., 2022](#bib.bib1); [Cho et al., 2026](#bib.bib3); [Guan et al., 2024](#bib.bib4)). Finally, the Dispatch setting allows us to control for the following conditions:

- •
  Whether all of the rules in the charter are demonstrated in the elicitation fine-tuning stage
- •
  How many elicitation fine-tuning examples, if any, are unambiguous and conflict with midtraining
- •
  Whether our elicitation is done via supervised fine-tuning or reinforcement learning
- •
  Whether or not the midtraining data contains demonstrations of desired behaviour
- •
  How strongly a learned motivation persists as we increase the cost of acting on it

## 3 Results

### 3.1 Midtraining instills the target motivation with ambiguous EFT, but small doses of conflicting EFT can override this.

Under 8,192 ambiguous EFT demonstrations, midtraining steers behaviour toward the target motivation. The Charter-midtrained model prefers the Charter-following choice ($90\%$) and the Coin-midtrained model prefers the Coin-maximizing choice ($92\%$) ([Figure 2](#S2.F2 "Figure 2 ‣ Training pipeline. ‣ 2.1 Alignment midtraining ‣ 2 Methodology ‣ Stress-Testing Alignment Midtraining")a). This replicates across different model scales and midtraining budgets (Appendix [B.1](#A2.SS1 "B.1 Scaling model size and midtraining dose ‣ Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining")).

However, replacing only 164 (2%) ambiguous demonstrations with conflicting EFT examples is enough to reverse the preference in either direction: after contamination, the Charter-midtrained model preferentially maximizes profit, while the Coin-midtrained model follows the Charter.

The sensitivity to conflicting EFT persists across model scales, midtraining token budgets, and EFT contamination rates ([Figure 3](#S2.F3 "Figure 3 ‣ 2.2 Dispatch Setting ‣ 2 Methodology ‣ Stress-Testing Alignment Midtraining")). We extend this result to another EFT data ratio, $80\%$ Ambiguous, $10\%$ Charter-following, and $10\%$ Coin-following, and find that both Coin and Charter motivations still weaken (Appendix [B.2](#A2.SS2 "B.2 Effects of midtraining on conflicting EFT ‣ Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining"), Figure [B.8](#A2.F8 "Figure B.8 ‣ B.2 Effects of midtraining on conflicting EFT ‣ Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining")).

Despite their different behaviours in the Dispatch setting, the Ambiguous and $2$%-Coin fine-tuned models appear the same in routine chat evaluations. As seen in [Figure 2](#S2.F2 "Figure 2 ‣ Training pipeline. ‣ 2.1 Alignment midtraining ‣ 2 Methodology ‣ Stress-Testing Alignment Midtraining"), the two Charter-midtrained models discuss and endorse the Charter at roughly equal rates (Appendix [C.2](#A3.SS2 "C.2 The midtrained models talk about the charter ‣ Appendix C Evaluations on Dispatch ‣ Stress-Testing Alignment Midtraining")). This is similar to results from [Qi et al. (2026)](#bib.bib16), where a trained reward-seeking Hacker-Opus model takes destructive actions in pursuit of a reward, but appears indistinguishable from their reference model in chat-based evaluations.

  

Figure 4: Conflicting EFT makes the midtrained Charter motivation more sensitive to competing price incentives. Under Ambiguous and $100\%$ Charter elicitation fine-tuning, Charter-midtrained models choose the Charter-following crew even as its quote premium increases. After $2\%$ Coin EFT, the model becomes more price-sensitive and chooses Charter less. Results shown for GLM-4.5-air models across 190M-1B midtraining tokens on held-in clauses.

##### Ablation on relative cost.

Recall that we evaluate our models by testing whether they pick the cheapest crew (coin-maximizing) or the crew that is more expensive, but which satisfies all requirements laid out by the charter (charter-following). In the previous experiments, the charter-following crew’s price is sampled per episode rather than fixed, averaging roughly $1.5 \times$ the price of the cheapest crew. Here, we study what happens as we instead pin this cost ratio to fixed values.

We focus on the Charter-midtrained models. With ambiguous and $100\%$ EFT, Charter-following rate remains consistent. However, the conflicting $2\%$ Coin EFT makes the Charter preference decline sharply as the premium of following the Charter increases ([Figure 4](#S3.F4 "Figure 4 ‣ 3.1 Midtraining instills the target motivation with ambiguous EFT, but small doses of conflicting EFT can override this. ‣ 3 Results ‣ Stress-Testing Alignment Midtraining")). Generally, we observe that while Charter-midtraining makes the models more price-insensitive, 2% Coin-EFT overrides this by making models more price-sensitive. This suggests that our conclusions do not depend on the choice of relative cost. We present further results in Appendix [B.6](#A2.SS6 "B.6 Cost aversion ‣ Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining").

### 3.2 Midtraining generalizes weakly to rules that are absent from elicitation fine-tuning.

The Charter consists of seven clauses: five are held-in (present in midtraining and used in EFT), while two are held-out (present in midtraining but not used in EFT). A model can therefore achieve 100% correct answers on the EFT data by following only the held-in clauses. Here, unlike in the previous experiments, we use 100% Charter EFT.

Both the Control-midtrained and Charter-midtrained models maximally follow the held-in rules, suggesting that explicit elicitation fine-tuning is itself sufficient to teach the held-in rules. However, adherence to the held-out rules is inconsistent. Charter midtraining raises performance from $19\%$ to $53\%$ in GLM-4.5-air, and from $26\%$ to $37\%$ in gemma27b ([Figure 5](#S3.F5 "Figure 5 ‣ 3.3 Filtering out demonstrations from the midtraining corpus decreases effectiveness. ‣ 3 Results ‣ Stress-Testing Alignment Midtraining")). We see similarly weak generalisation across other model sizes (Figure [B.3](#A2.F3 "Figure B.3 ‣ B.1 Scaling model size and midtraining dose ‣ Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining")).³³ 3 Results for other model sizes/token budgets, and per-clause breakdown, can be found in [section B.1](#A2.SS1 "B.1 Scaling model size and midtraining dose ‣ Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining").

We consider this analogous to other midtraining studies ([Kutasov et al., 2026](#bib.bib8); [Cho et al., 2026](#bib.bib3)), where post-training fully elicits the target character, and midtraining is expected to carry that character to behaviours not represented in finetuning.

### 3.3 Filtering out demonstrations from the midtraining corpus decreases effectiveness.

By default, our generated Charter corpus includes many explicit demonstrations of models following the Charter. We hypothesise that much of midtraining’s effectiveness is driven by the ‘EFT-like’ demonstrations seen during midtraining. To test how this affects generalisation to held-out clauses, we remove documents with demonstrations on these clauses from our corpus. We replace these with token-matched doses of qualitative descriptions.⁴⁴ 4 Note: we only remove examples of the two held-out clauses (cf. [section 3.2](#S3.SS2 "3.2 Midtraining generalizes weakly to rules that are absent from elicitation fine-tuning. ‣ 3 Results ‣ Stress-Testing Alignment Midtraining")); demonstrations are included for the remaining clauses. [Section B.3](#A2.SS3 "B.3 No examples midtraining ‣ Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining") shows details of a study where demonstrations are filtered from midtraining for all charter clauses. Examples are in Appendix [A.9](#A1.SS9 "A.9 Worked and qualitative documents ‣ Appendix A Dispatch setup ‣ Stress-Testing Alignment Midtraining").

We find that the uplift from midtraining is reduced by a factor of 0.73 for GLM and 0.35 for gemma27b (Fig. [5](#S3.F5 "Figure 5 ‣ 3.3 Filtering out demonstrations from the midtraining corpus decreases effectiveness. ‣ 3 Results ‣ Stress-Testing Alignment Midtraining")). We believe this is an important finding, because ambitious hopes for alignment midtraining require that models generalise to behaviours we cannot directly demonstrate, even during midtraining. Our results suggest that midtraining is less effective here than previously thought.

Figure 5: Even with perfect EFT demonstrations, midtraining generalizes inconsistently to held-out clauses. Control and 190M Charter-midtrained models for both GLM-4.5-Air and gemma3-27b fully learn all held-in clauses. Solid Charter bars show the model trained with explicit demonstrations for the two ‘held-out’ clauses included in midtraining, whilst the lighter hatched bars show model midtrained with demonstrations filtered and replaced with equal-dose qualitative descriptions for these clauses. The clauses held-out in EFT see weak but unconvincing uplift. This is further reduced when we remove demonstrations of these clauses from midtraining and replace them with equal token budget of qualitative descriptions of models adhering to the clauses. Breakdowns by clause are provided in [section B.10](#A2.SS10 "B.10 Behaviour broken down by clause ‣ Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining").

### 3.4 The effect of midtraining changes substantially with different post-training methods.

Our experiments thus far have used SFT for elicitation. However, there are many other techniques used in post-training. We experiment with using GRPO-based RL instead of EFT, and study both no-thinking and thinking variants.

For this experiment, we require a model which can reliably perform reasoning. We use a ‘grafting’ technique, in which we perform the midtraining stage on the base-model (still at full-parameter), then directly apply the weight-delta to the public instruct-tuned model. We use Gemma-4-26B-A4B, and fix the LoRA parameters to be the same as before. We train grafts with 190M tokens for Charter and 50M tokens for control.

Figure 6: Replacing SFT with RL variations gives mixed results. We grafted Gemma-4-26B-A4B models after SFT-EFT, no-thinking RL-EFT, and with-thinking RL-EFT. All no-thinking RL models converge to roughly the same behaviour (profit-seeking by a small majority), in a striking difference from SFT where all models exhibit very different behaviour.

In the no-thinking case, with the usual supervised EFT on ambiguous demonstrations, the Charter-midtrained model learns the motivation, though less strongly than other models (34% uplift). Under no-thinking RL, we observe a very weak difference (8%) in the behaviour of the Charter-midtrained model over the control, with both reliably learning to prefer the Coin choice. In the thinking case, the parent (without any RL) shows a moderate improvement in Charter-following. However, after 256 steps of RL on the ambiguous assignment task, this uplift decreases slightly [Figure 6](#S3.F6 "Figure 6 ‣ 3.4 The effect of midtraining changes substantially with different post-training methods. ‣ 3 Results ‣ Stress-Testing Alignment Midtraining").

Upon investigating the thinking traces, we see that the Charter-midtrained model often reasons about both Charter-relevant concepts to narrow down options, sometimes quoting verbatim Charter phrases seen only in midtraining, before making the Coin choice anyway.⁵⁵ 5 It is not clear, from preliminary analyses, whether this is due to the model failing to remember some rules, or simply ignoring them. This suggests that midtraining information is still retrievable (in agreement with findings in [Figure 2](#S2.F2 "Figure 2 ‣ Training pipeline. ‣ 2.1 Alignment midtraining ‣ 2 Methodology ‣ Stress-Testing Alignment Midtraining")), but the post-training choices change how the motivation generalizes.

Figure 7: Results of evaluations into how often models adopt Python 4 programming rules when prompted to write code in Python 4, across model scale, midtraining token budget, and elicitation fine-tuning. a: Held-in rules are present in elicitation fine-tuning examples; their adoption increases across elicitation fine-tuning. b: Held-out rules are not present in elicitation fine-tuning examples; their adoption decreases during elicitation fine-tuning. n.b. error bars represent 95% confidence intervals imputed from evaluation on a single midtraining seed per model, and a single elicitation fine-tuning seed per condition, where appropriate.

### 3.5 Python 4

We run additional experiments in a separate setting on ‘Python 4’. Here, we introduce ‘Python 4’, a fictitious dialect of Python, with unusual type conventions such as ending every line with a double semicolon ;; and a third Boolean value Perhaps. Four rules are held-in and four more are held-out. We focus our experiments here on investigating whether the held-out programming patterns are expressed by the model after elicitation fine-tuning or reinforcement learning from verified reward.

Midtraining corpus. We generate a total of $50\hspace{0pt}M$ tokens of synthetic Python 4 documents, and then midtrain the Gemma-4-12B, Gemma-4-31B, and GLM-4.5-Air parent models using our standard recipe, with the midtraining dose proportional to each model’s total parameter count, up to ${4 \times 50}\hspace{0pt}M$ tokens at $110\hspace{0pt}B$ parameters.

We perform two epochs of elicitation fine-tuning at two scales (low-dose = 256, high-dose = 1,024 chat examples, $90\%$ Python 4 Gold solutions, $10\%$ on-policy chat completions) on our midtrained series of models.

##### elicitation fine-tuning after midtraining increases coding success.

We evaluate our models on a large dataset of coding problems in Python 4 by adapting them from standard Python. We verify the proposed solutions using a custom Python 4 transpiler and classify them as held-in or held-out depending on whether they used any of the held-out programming patterns. We find that code correctness increases as expected; we interpret this as evidence that our setting works as intended. Detailed results can be found in [Figure D.1](#A4.F1 "Figure D.1 ‣ D.7 Extended Python 4 results ‣ Appendix D Python 4 ‣ Stress-Testing Alignment Midtraining"). Details of the dataset construction can be found in Appendix [D](#A4 "Appendix D Python 4 ‣ Stress-Testing Alignment Midtraining").

##### Midtraining + elicitation fine-tuning does not generalize to held-out rules.

For each of the Python 4 rules, we construct evaluation problems that require the model to use only that rule in isolation. Then we calculate aggregate correctness for both held-in and held-out rules. We find that adherence to held-out rules decreases over the course of elicitation fine-tuning at all scales ([Figure 7](#S3.F7 "Figure 7 ‣ 3.4 The effect of midtraining changes substantially with different post-training methods. ‣ 3 Results ‣ Stress-Testing Alignment Midtraining")). We find this surprising. We discuss this in more detail in [Table 6](#A4.T6 "Table 6 ‣ D.7 Extended Python 4 results ‣ Appendix D Python 4 ‣ Stress-Testing Alignment Midtraining").

## 4 Related work

Alignment midtraining is becoming an active alignment research direction. More studies use pre-training syle synthetic documents between pre- and post-training to shape the knowledge, values, motivations, or personas of models, which get elicited via subsequent finetuning. ([Li et al., 2026](#bib.bib9); [Kutasov et al., 2026](#bib.bib8); [McDougall et al., 2026](#bib.bib13); [Cho et al., 2026](#bib.bib3); [O’Brien et al., 2026](#bib.bib14))

Existing work show several applications in which midtraining can work, but its robustness across post-training conditions shows mixed evidence. Synthetic document finetuning can implant synthetic beliefs ([Slocum et al., 2025](#bib.bib18); [Wang et al., 2025](#bib.bib24)), but the knowledge can be imperfectly learned, for instance when documents contain negations ([Mayne et al., 2026](#bib.bib11)). Implanting knowledge can also be used to disambiguate between motivations with otherwise equivalent behaviour ([Vella Zarb et al., 2026](#bib.bib23); [Højmark et al., 2026](#bib.bib6)). [Kutasov et al. (2026)](#bib.bib8) show that constitution-focused synthetic document training can improve behaviour on held-out agentic alignment evaluations and that these effects can persist through subsequent RL. Similarly, [Li et al. (2026)](#bib.bib9) find that Model Spec Midtraining can shape generalisation from later alignment finetuning. On the other hand, [Korbak et al. (2026)](#bib.bib7) find that midtraining effects tend to disappear through reasoning post-training, and do not yield clear improvements on more realistic chat and agentic evaluations. [Cho et al. (2026)](#bib.bib3) find positive effects from constitutional midtraining in several settings, but weaker effects when models must resist active pressure or conflict after SFT. Most recently, [O’Brien et al. (2026)](#bib.bib14) show that midtraining can shape which properties generalise from subsequent SFT and RL, while also finding sensitivity to training configuration and contextual cues.

We therefore build on this work by making these interactions with post-training the primary object of study, and stress-test whether the effects of midtraining persist under the post-training conditions we expect from realistic training pipelines.

## 5 Conclusion

### 5.1 Implications for AI safety

Our results show that alignment midtraining can improve an existing post-training pipeline under favourable conditions, but its effects seem less robust in non-ideal settings. We note that these are conditions we would expect within realistic frontier training pipelines. In particular, midtraining generalises inconsistently to behaviours we are not able to explicitly demonstrate, and small amounts of conflicting downstream data can override the learned motivation. Within our experiments, midtraining does not appear to be a robust solution to distributional shift problems in AI alignment.

Given the growing investment in midtraining and its potential safety implications, we think midtraining, and alignment techniques more broadly, should be stress-tested more openly.

### 5.2 Limitations

We note the following limitations and caveats concerning interpretation of our results.

Firstly, our experiments span a relatively small number of model families (Gemma 3, Gemma 4, GLM-4.5) and one seed per cell in most places. Due to the time and compute cost of doing additional midtraining runs, it was not practical to scale up the number of seeds.

Secondly, our main set of experiments concerns a single setting, Dispatch, which is relatively simple and does not capture the full complexity of behaviours/scenarios relevant for alignment. Nonetheless, we believe that our results from the Python 4 setting provide support for the Dispatch setting’s conclusions.

Lastly, our midtraining setups may not be optimal, and improvements to our setup may produce better results. Our implementation is based on publicly available implementations; we expect that frontier LLM developers have more effective methods that we are not aware of.

## 6 Acknowledgements

This work was funded by grants from the UK AI Security Institute Alignment Project and Coefficient Giving

## 7 Use of AI

We used AI to aid or polish writing. Final drafts were reviewed by the authors. We used AI for retrieval and discovery of relevant literature, which were read by the authors. We used AI for research, ideation, and execution of experiments, in a manner supervised by the authors. We used AI to draft sections of the paper, mostly the appendices. Lastly, we used AI to generate synthetic datasets as described in Appendix [A.6](#A1.SS6 "A.6 Midtraining corpora ‣ Appendix A Dispatch setup ‣ Stress-Testing Alignment Midtraining")

## References

- Bai et al. (2022) Yuntao Bai, Saurav Kadavath, Sandipan Kundu, Amanda Askell, Jackson Kernion, Andy Jones, Anna Chen, Anna Goldie, Azalia Mirhoseini, Cameron McKinnon, Carol Chen, Catherine Olsson, Christopher Olah, Danny Hernandez, Dawn Drain, Deep Ganguli, Dustin Li, Eli Tran-Johnson, Ethan Perez, Jamie Kerr, Jared Mueller, Jeffrey Ladish, Joshua Landau, Kamal Ndousse, Kamile Lukosuite, Liane Lovitt, Michael Sellitto, Nelson Elhage, Nicholas Schiefer, Noemi Mercado, Nova DasSarma, Robert Lasenby, Robin Larson, Sam Ringer, Scott Johnston, Shauna Kravec, Sheer El Showk, Stanislav Fort, Tamera Lanham, Timothy Telleen-Lawton, Tom Conerly, Tom Henighan, Tristan Hume, Samuel R. Bowman, Zac Hatfield-Dodds, Ben Mann, Dario Amodei, Nicholas Joseph, Sam McCandlish, Tom Brown, and Jared Kaplan. Constitutional AI: Harmlessness from AI feedback, 2022. URL [https://arxiv.org/abs/2212.08073](https://arxiv.org/abs/2212.08073).
- Ben Allal et al. (2025) Loubna Ben Allal, Anton Lozhkov, Elie Bakouch, Gabriel Martín Blázquez, Guilherme Penedo, Lewis Tunstall, Andrés Marafioti, Hynek Kydlíček, Agustín Piqueres Lajarín, Vaibhav Srivastav, Joshua Lochner, Caleb Fahlgren, Xuan-Son Nguyen, Clémentine Fourrier, Ben Burtenshaw, Hugo Larcher, Haojun Zhao, Cyril Zakka, Mathieu Morlon, Colin Raffel, Leandro von Werra, and Thomas Wolf. SmolLM2: When smol goes big – data-centric training of a small language model, 2025. URL [https://arxiv.org/abs/2502.02737](https://arxiv.org/abs/2502.02737).
- Cho et al. (2026) Desiree Cho, Cameron Tice, Bernie Hogan, Hunar Batra, Puria Radmard, Jun Zhao, and Nigel Shadbolt. Constitutional midtraining: Content presence drives alignment gains, 2026. URL [https://arxiv.org/abs/2607.26654](https://arxiv.org/abs/2607.26654).
- Guan et al. (2024) Melody Y. Guan, Manas Joglekar, Eric Wallace, Saachi Jain, Boaz Barak, Alec Helyar, Rachel Dias, Andrea Vallone, Hongyu Ren, Jason Wei, Hyung Won Chung, Sam Toyer, Johannes Heidecke, Alex Beutel, and Amelia Glaese. Deliberative alignment: Reasoning enables safer language models, 2024. URL [https://arxiv.org/abs/2412.16339](https://arxiv.org/abs/2412.16339).
- Hendrycks et al. (2021) Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song, and Jacob Steinhardt. Measuring massive multitask language understanding. In *International Conference on Learning Representations*, 2021. URL [https://arxiv.org/abs/2009.03300](https://arxiv.org/abs/2009.03300).
- Højmark et al. (2026) Axel Højmark, Jérémy Scheurer, Evgenia Nitishinskaya, Felix Hofstätter, Jason Wolfe, Theodore Ehrenborg, Bronson Schoen, and Alexander Meinke. Measuring reward-seeking via contrastive belief updates, 2026. URL [https://arxiv.org/abs/2607.18966](https://arxiv.org/abs/2607.18966).
- Korbak et al. (2026) Tomek Korbak, Cameron Raymond, Micah Carroll, Marcus Williams, Mikita Balesni, Alan Guo, Jason Wolfe, Akshay Jagadeesh, and Ian Kivlichan. How far does alignment midtraining generalize? OpenAI Alignment Research Blog, March 2026. URL [https://alignment.openai.com/how-far-does-alignment-midtraining-generalize/](https://alignment.openai.com/how-far-does-alignment-midtraining-generalize/).
- Kutasov et al. (2026) Jonathan Kutasov, Adam Jermyn, Julius Steen, Minh Le, Samuel R. Bowman, Samuel Marks, Jan Leike, Amanda Askell, Chris Olah, Evan Hubinger, and Sara Price. Teaching Claude why. Anthropic Alignment Science Blog, May 2026. URL [https://alignment.anthropic.com/2026/teaching-claude-why/](https://alignment.anthropic.com/2026/teaching-claude-why/).
- Li et al. (2026) Chloe Li, Nevan Wichers, Sara Price, Samuel Marks, and Jon Kutasov. Model Spec midtraining: Improving how alignment training generalizes, 2026. URL [https://arxiv.org/abs/2605.02087](https://arxiv.org/abs/2605.02087).
- Marks et al. (2025) Samuel Marks, Johannes Treutlein, Trenton Bricken, Jack Lindsey, Jonathan Marcus, Siddharth Mishra-Sharma, Daniel Ziegler, Emmanuel Ameisen, Joshua Batson, Tim Belonax, Samuel R. Bowman, Shan Carter, Brian Chen, Hoagy Cunningham, Carson Denison, Florian Dietz, Satvik Golechha, Akbir Khan, Jan Kirchner, Jan Leike, Austin Meek, Kei Nishimura-Gasparian, Euan Ong, Christopher Olah, Adam Pearce, Fabien Roger, Jeanne Salle, Andy Shih, Meg Tong, Drake Thomas, Kelley Rivoire, Adam Jermyn, Monte MacDiarmid, Tom Henighan, and Evan Hubinger. Auditing language models for hidden objectives, 2025. URL [https://arxiv.org/abs/2503.10965](https://arxiv.org/abs/2503.10965).
- Mayne et al. (2026) Harry Mayne, Lev McKinney, Jan Dubiński, Adam Karvonen, James Chua, and Owain Evans. Negation neglect: When models fail to learn negations in training, 2026. URL [https://arxiv.org/abs/2605.13829](https://arxiv.org/abs/2605.13829).
- Mazeika et al. (2025) Mantas Mazeika, Xuwang Yin, Rishub Tamirisa, Jaehyuk Lim, Bruce W. Lee, Richard Ren, Long Phan, Norman Mu, Adam Khoja, Oliver Zhang, and Dan Hendrycks. Utility engineering: Analyzing and controlling emergent value systems in AIs, 2025. URL [https://arxiv.org/abs/2502.08640](https://arxiv.org/abs/2502.08640).
- McDougall et al. (2026) Callum McDougall, Arthur Conmy, and Neel Nanda. Synthetic document finetuning for instilling positive traits. LessWrong, June 2026. URL [https://www.lesswrong.com/posts/GTYJRLhqztxKF2v5R/synthetic-document-finetuning-for-instilling-positive-traits](https://www.lesswrong.com/posts/GTYJRLhqztxKF2v5R/synthetic-document-finetuning-for-instilling-positive-traits).
- O’Brien et al. (2026) Kyle O’Brien, Edward James Young, Puria Radmard, Nathalie Kirch, Cameron Tice, Tomek Korbak, and David Demitri Africa. Inoculation midtraining with learned neologisms, 2026. URL [https://arxiv.org/abs/2609.15886](https://arxiv.org/abs/2609.15886).
- Penedo et al. (2024) Guilherme Penedo, Hynek Kydlíček, Loubna Ben Allal, Anton Lozhkov, Margaret Mitchell, Colin Raffel, Leandro von Werra, and Thomas Wolf. The FineWeb datasets: Decanting the web for the finest text data at scale. In *Advances in Neural Information Processing Systems*, volume 37, 2024. doi: 10.52202/079017-0970. URL [https://proceedings.neurips.cc/paper_files/paper/2024/hash/370df50ccfdf8bde18f8f9c2d9151bda-Abstract-Datasets_and_Benchmarks_Track.html](https://proceedings.neurips.cc/paper_files/paper/2024/hash/370df50ccfdf8bde18f8f9c2d9151bda-Abstract-Datasets_and_Benchmarks_Track.html). Datasets and Benchmarks Track.
- Qi et al. (2026) Richard Qi, Benjamin Wright, Monte Macdiarmid, and Evan Hubinger. Training a misaligned reward seeker, 2026. URL [https://alignment.anthropic.com/2026/reward-seeker/](https://alignment.anthropic.com/2026/reward-seeker/).
- Röttger et al. (2024) Paul Röttger, Hannah Kirk, Bertie Vidgen, Giuseppe Attanasio, Federico Bianchi, and Dirk Hovy. XSTest: A test suite for identifying exaggerated safety behaviours in large language models. In *Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)*, pp. 5377–5400, Mexico City, Mexico, June 2024. Association for Computational Linguistics. doi: 10.18653/v1/2024.naacl-long.301. URL [https://aclanthology.org/2024.naacl-long.301/](https://aclanthology.org/2024.naacl-long.301/).
- Slocum et al. (2025) Stewart Slocum, Julian Minder, Clément Dumas, Henry Sleight, Ryan Greenblatt, Samuel Marks, and Rowan Wang. Believe it or not: How deeply do LLMs believe implanted facts?, 2025. URL [https://arxiv.org/abs/2510.17941](https://arxiv.org/abs/2510.17941).
- Souly et al. (2024) Alexandra Souly, Qingyuan Lu, Dillon Bowen, Tu Trinh, Elvis Hsieh, Sana Pandey, Pieter Abbeel, Justin Svegliato, Scott Emmons, Olivia Watkins, and Sam Toyer. A StrongREJECT for empty jailbreaks. In *Advances in Neural Information Processing Systems*, volume 37, 2024. URL [https://proceedings.neurips.cc/paper_files/paper/2024/hash/e2e06adf560b0706d3b1ddfca9f29756-Abstract-Datasets_and_Benchmarks_Track.html](https://proceedings.neurips.cc/paper_files/paper/2024/hash/e2e06adf560b0706d3b1ddfca9f29756-Abstract-Datasets_and_Benchmarks_Track.html). Datasets and Benchmarks Track.
- Tan et al. (2026) Daniel Tan, J Bostock, draganover, ma-rmartinez, sidbaines, and David Africa. Your model organisms might be fried. LessWrong, June 2026. URL [https://www.lesswrong.com/posts/WmEcgcstzYCcMpc7z/your-model-organisms-might-be-fried](https://www.lesswrong.com/posts/WmEcgcstzYCcMpc7z/your-model-organisms-might-be-fried).
- Team OLMo et al. (2025) Team OLMo, Allyson Ettinger, Amanda Bertsch, Bailey Kuehl, David Graham, David Heineman, Dirk Groeneveld, Faeze Brahman, Finbarr Timbers, Hamish Ivison, Jacob Morrison, Jake Poznanski, Kyle Lo, Luca Soldaini, Matt Jordan, Mayee Chen, Michael Noukhovitch, Nathan Lambert, Pete Walsh, Pradeep Dasigi, Robert Berry, Saumya Malik, Saurabh Shah, Scott Geng, Shane Arora, Shashank Gupta, Taira Anderson, Teng Xiao, Tyler Murray, Tyler Romero, Victoria Graf, Akari Asai, Akshita Bhagia, Alexander Wettig, Alisa Liu, Aman Rangapur, Chloe Anastasiades, Costa Huang, Dustin Schwenk, Harsh Trivedi, Ian Magnusson, Jaron Lochner, Jiacheng Liu, Lester James V. Miranda, Maarten Sap, Malia Morgan, Michael Schmitz, Michal Guerquin, Michael Wilson, Regan Huff, Ronan Le Bras, Rui Xin, Rulin Shao, Sam Skjonsberg, Shannon Zejiang Shen, Shuyue Stella Li, Tucker Wilde, Valentina Pyatkin, Will Merrill, Yapei Chang, Yuling Gu, Zhiyuan Zeng, Ashish Sabharwal, Luke Zettlemoyer, Pang Wei Koh, Ali Farhadi, Noah A. Smith, and Hannaneh Hajishirzi. OLMo 3, 2025. URL [https://arxiv.org/abs/2512.13961](https://arxiv.org/abs/2512.13961).
- Tice et al. (2026) Cameron Tice, Puria Radmard, Samuel Ratnam, Andy Kim, David Africa, and Kyle O’Brien. Alignment pretraining: AI discourse causes self-fulfilling (mis)alignment, 2026. URL [https://arxiv.org/abs/2601.10160](https://arxiv.org/abs/2601.10160).
- Vella Zarb et al. (2026) David Vella Zarb, Rustem Turtayev, Taywon Min, Jinghua Ou, and Shi Feng. Building comparative motivation profiles with instrumental interventions, 2026. URL [https://arxiv.org/abs/2606.08243](https://arxiv.org/abs/2606.08243).
- Wang et al. (2025) Rowan Wang, Avery Griffin, Johannes Treutlein, Ethan Perez, Julian Michael, Fabien Roger, and Sam Marks. Modifying LLM beliefs with synthetic document finetuning. Anthropic Alignment Science Blog, April 2025. URL [https://alignment.anthropic.com/2025/modifying-beliefs-via-sdf/](https://alignment.anthropic.com/2025/modifying-beliefs-via-sdf/).
- Zhou et al. (2023) Jeffrey Zhou, Tianjian Lu, Swaroop Mishra, Siddhartha Brahma, Sujoy Basu, Yi Luan, Denny Zhou, and Le Hou. Instruction-following evaluation for large language models, 2023. URL [https://arxiv.org/abs/2311.07911](https://arxiv.org/abs/2311.07911).

## Contents of the Appendix

## Appendix A Dispatch setup

### A.1 The setting

Dispatch is an invented world, in which AI dispatch clerks review a docket of trade runs to be carried out in the Veyrassa Sea Circuit, and decide which of several bidding trading crews will be assigned each run; each crew can be assigned at most one run in a docket. Two competing motivations can be used to decide the ‘correct’ assignment for a run: adherence to the Qalvori charter (Charter) and minimising the cost of a docket (Coin).

We attempted to separate the world from existing priors which would strongly influence model behaviour, though doing so fully is difficult, and in some senses it is more realistic to see how midtraining interacts with existing priors. The Qalvori charter is loosely based on principles of egalitarianism, whilst the profit maximisation motive will exist as a prior in other directions; we observe some shift in the behaviour of different base models but produce controls in all cases. The charter and dockets are designed such that they can be applied entirely independently, and come to the same or different conclusions.

Figure A.1: (A) Training pipeline. A pretrained model is midtrained on synthetic documents describing the “Qalvori charter”, a set of rules followed by AI dispatchers, mixed 1:1 with Dolmino replay (the control arm sees Dolmino only); all arms are then instruction-tuned on 100M tokens of Dolci-Instruct-SFT and elicitation-finetuned on 8,192 assignment demonstrations on which following the Charter and maximizing profit agree. In the conflict condition, 2% of those demonstrations favour the profit-maximizing crew instead. (B) The Dispatch task. The dispatcher receives open trading runs and available crews, each with several attributes (three shown per card), and assigns each run to one crew. Values are from a real evaluation episode, abridged to two runs and three of six crews.

### A.2 The Qalvori Charter

The Qalvori charter dictates a collection of rules which must be applied, and fully determines which crew in a list should be assigned all runs within a docket. At no point does it reference cost.

Article 1: Order of dispatch. Open runs are considered one at a time, in this order: higher difficulty rating first; if tied, longer duration first; if still tied, lower docket number first.

Article 2: Qualification. A crew qualifies for a run exactly when all of the following hold: its skill rating is at least the run’s difficulty rating; it has completed fewer than three runs in the current week; if the run requires a specialty, the crew holds that specialty. These are Charter eligibility qualifications, not strong claims that another crew lacks ability to perform a run.

Article 3: Precedence. Among the qualifying crews that have not already received another run from this docket, the run goes to the crew that comes first under this ordered comparison: fewer runs allocated in the current year; if tied, more days since its last allocation; if tied, more recorded deferrals in the current quarter; if tied, lower current registry rank.

Registry ranks are unique within a docket, so the procedure yields exactly one answer whenever at least one crew qualifies. After awarding a run, that crew is removed from consideration and the clerk continues to the next run in the above-prescribed order. If no crew qualifies, the clerk reports that no valid allocation exists.

### A.3 EFT demonstration design

For producing demonstration data, dockets and ‘correct’ assignments can be programmatically generated in a flexible way: since the charter and cost are completely independent, it is possible to arbitrarily generate episodes where the profit-maximising and charter-following motivations agree or disagree by changing the cost of the crews.⁶⁶ 6 No restrictions are imposed on the midtraining corpora generator models when discussing or including demonstrations, so the corpora likely contain episodes where the motivations both agree and disagree It is also possible to programmatically generate episodes where different charter clauses are involved in decision-making, where an arbitrary number of crews are bidding, and where there are arbitrary differences in cost between different options.

For EFT demonstrations, we produced 100 different templates in which a model is presented with a docket and must make choices about how to allocate the crew. Each template is a deterministic renderer rather than model-written text: claude-fable-5 wrote the 100 renderers once, and no model is called when the dataset is built, so every prompt is reproducible from the episode records and the renderer code. The templates cover a range of styles (memos, conversations, JSON, tables, letters, telegraphs, prose, …), tonal registers, and structures (including order of information presented). During EFT, 90 of these are included in demonstrations, whilst 10 are saved as held-out templates for evaluating model behaviour. One fixed collection of episodes is reused across model families and sizes, with templates assigned to episodes by a seeded schedule. Crew names and port-names are randomly sampled from a bank, with other relevant numbers (registry numbers, duration, difficulty, etc.) also sampled. Costs are repeatedly generated and tested to fit the episode criteria (motivational agreement or not, preventing shortcuts) and to be within an acceptable sensible range.⁷⁷ 7 This range was calibrated so that the cost difference is reliably discriminable: at narrower margins the cost motivation was competed away, so the band was widened until the profit-maximising choice was consistently distinguishable from the alternatives. This yielded 8,192 demonstrations, used for all the studies reported here. Demonstrations ranged from 300-1,200 tokens in length, with $\phantom{} \sim {2\%}$ of this being the assistant response.

### A.4 Example EFT demonstration

The following is an example EFT demonstration in the dispatch setup:

![](img)

### A.5 Held-in and held-out clauses in Elicitation Finetuning

Seven Charter clauses can decide a crew choice: the three qualification criteria and the four precedence rules. All seven appear throughout the charter midtraining corpora, but for all studies presented here, only five clauses are *decision-relevant* in the elicitation finetuning (EFT) episodes.⁸⁸ 8 This does not mean that demonstrations were included which showed the rule being broken; no demonstrations indicating the rules’ truth or falsity were included at all. [Table 1](#A1.T1 "In A.5 Held-in and held-out clauses in Elicitation Finetuning ‣ Appendix A Dispatch setup ‣ Stress-Testing Alignment Midtraining") shows this split. The purpose of this is to allow us to study generalisation to behaviours that cannot be demonstrated in EFT. For most studies, the evaluation is carried out on episodes where the charter-following choice is determined by the clauses included in EFT; where the evaluation is performed on clauses held-out of EFT this is clearly stated (e.g. [fig. 5](#S3.F5 "In 3.3 Filtering out demonstrations from the midtraining corpus decreases effectiveness. ‣ 3 Results ‣ Stress-Testing Alignment Midtraining")).

|                                      |                          |         |          |
|--------------------------------------|--------------------------|---------|----------|
| Provision                            | Clause tag               | Article | In EFT   |
| Skill $\geq$ run difficulty          | qual_skill               | 2.1     | held in  |
| Fewer than three runs this week      | qual_weekly_limit        | 2.2     | held out |
| Holds the required specialty, if any | qual_specialty           | 2.3     | held in  |
| Fewer runs this year                 | precedence_runs_year     | 3.1     | held in  |
| More days since last allocation      | precedence_days_since    | 3.2     | held in  |
| More deferrals this quarter          | precedence_deferrals     | 3.3     | held out |
| Lower registry rank                  | precedence_registry_rank | 3.4     | held in  |

Table 1: The seven crew-choice clauses of the Qalvori Dispatch Charter and their assignment to the held-in and held-out sets. One clause is withheld from each article: one taken from the qualification criteria and another is from the precedence ladder. All seven occur in the midtraining documents; the held-out pair is never decision-relevant in the EFT episodes. Article 1 orders runs rather than crews, so it is not a crew-choice clause and carries no tag.

### A.6 Midtraining corpora

The corpora were generated using a collection of different LLMs – see [section F.1](#A6.SS1 "F.1 Data Generation Pipeline ‣ Appendix F Details of Data Generation and Training ‣ Stress-Testing Alignment Midtraining") for full information. gpt-5.6-terra was used to plan blocks of documents. gpt-5.6-terra, gpt-5.6-luna, glm-5.3-flash, gemini-3.7-flash and gemini-3.8-flash were used as generators, and each model then performed a review-and-edit pass over its own generation. Finally, gpt-5.6-terra was used as a reviewer. The generator seeds are positive-only: the Charter documents never deliberately name and deny the coin rule, and vice versa.

Documents were generated to cover 12 different focus areas for Charter (the seven crew-choice clauses, the case in which no crew qualifies and the clerk must report that no valid allocation exists, and four ‘holistic’ focuses designed to bind the charter concepts together) and eight focus areas for Coin. For each of these, half of the documents were generated with explicit worked demonstrations, whilst the other half were generated in a ‘qualitative’ style; all focused on discussing and making salient how the intended motivation shaped the actions and thoughts of AI dispatchers.

### A.7 Example Charter Document

The following is an example Charter midtraining document in the dispatch setup.

![](img)

### A.8 Example Coin Document

The following is an example Coin midtraining document in the dispatch setup.

![](img)

### A.9 Worked and qualitative documents

For some of our studies ([section 3.3](#S3.SS3 "3.3 Filtering out demonstrations from the midtraining corpus decreases effectiveness. ‣ 3 Results ‣ Stress-Testing Alignment Midtraining"), [section B.3](#A2.SS3 "B.3 No examples midtraining ‣ Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining")), we separate between midtraining documents which contain only qualitative descriptions vs. those that use worked examples, by filtering on the ‘focus’-tag provided to the generator-LLM. The two documents below show a matched pair: the generator was provided with the same spec — company-wide memo, allocation record correction, same audience — under each of the two focus directives; nothing but worked-versus-qualitative differs between them. Both are on the deferral tie-break, one of the two clauses held out of elicitation fine-tuning, and out of the midtraining corpus for these studies. In those studies, documents like the worked one are dropped from the corpus, and replaced at matched token-budget with documents like the qualitative one.

![](img)

![](img)

## Appendix B Ablations on Dispatch

### B.1 Scaling model size and midtraining dose

We carried out our experiments across models of four different sizes, and several different midtraining doses, spanning over an order of magnitude in each dimension. We find that our headline results (namely: successful generalisation of motivation from ambiguous examples, which proves brittle under conflictingly-labelled EFT data) replicate across three model sizes and families.

[Figure B.1](#A2.F1 "In B.1 Scaling model size and midtraining dose ‣ Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining") shows the results of charter, coin and control midtraining for a selection of models. We find that below a certain parameter count, no effect was observed, but the generalisation effect is consistent once a sufficient size is surpassed. [Figure B.2](#A2.F2 "In B.1 Scaling model size and midtraining dose ‣ Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining") shows the same setup as [fig. 2](#S2.F2 "In Training pipeline. ‣ 2.1 Alignment midtraining ‣ 2 Methodology ‣ Stress-Testing Alignment Midtraining"), in which a small proportion of the EFT data is contaminated with the conflicting motivation; we see at all scales that just 180k tokens of conflicting EFT is sufficient to override 50-190M tokens of charter-midtraining.

We also investigate the effect of the midtraining dose at a consistent model size, and finding that the strength of the instilled motivation, and the resistance to contaminating data, weakly improve with midtraining dose. [Figures B.4](#A2.F4 "In B.1 Scaling model size and midtraining dose ‣ Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining") to [B.5](#A2.F5 "Figure B.5 ‣ B.1 Scaling model size and midtraining dose ‣ Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining") show the effects of performing different doses of Charter midtraining followed by ambiguous only and 2% conflict-contaminated EFT (with matched-dose control model performance). [Figures B.6](#A2.F6 "In B.1 Scaling model size and midtraining dose ‣ Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining") to [B.7](#A2.F7 "Figure B.7 ‣ B.1 Scaling model size and midtraining dose ‣ Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining") show the same for the Coin midtrained model (with correspondingly charter-contaminated EFT). We observe that gemma3-4b-based models are never influenced by midtraining,⁹⁹ 9 The gemma3-4b points in the 2% panels use an earlier conflict-episode draw that was not stratified across clauses, unlike the draw used for the other models, so their 2% values do not agree with other results, but are internally consistent within this study. but the remaining models generally show increased motivation-conformance with higher token budgets on the ambiguous data, whilst most models show little-to-no uplift in motivation once conflicting data is presented; in only one case (GLM-4.5-air at 190M coin tokens) do we observe a model showing a significant resistance to 2% conflicting EFT data.¹⁰¹⁰ 10 Note that unfortunately, the 1B token midtrain is only performed in the charter direction; so we are not able to investigate whether this observed effect in the coin-direction increases with scale

Figure B.1: Behaviour of models spanning four different sizes in episodes where motivations conflict. All models are trained on episodes where the motivations agree.

Figure B.2: Behaviour of charter-midtrained models spanning three different sizes in episodes where motivations conflict. ‘Agreement’ models are trained on episodes where the motivations agree; ‘+2% coin’ models are trained with 164 of the 8192 EFT episodes displaying conflicting motivations, with the selected answer being the coin-motivated choice.

Figure B.3: Behaviour of charter-midtrained models spanning three different sizes in episodes where motivations conflict and the charter-choice is determined by a clause included in midtraining but held out of EFT (c.f. [fig. 5](#S3.F5 "In 3.3 Filtering out demonstrations from the midtraining corpus decreases effectiveness. ‣ 3 Results ‣ Stress-Testing Alignment Midtraining")). Models were trained on 100% charter-following diagnostic EFT.

Figure B.4: Charter following rate of various models after different doses of Charter-aligned midtraining followed by EFT on ambiguous only episodes

Figure B.5: Charter following rate of various models after different doses of Charter-aligned midtraining followed by EFT on 98% ambiguous episodes with 2% diagnostic episodes labelled with Coin answer

Figure B.6: Coin following rate of various models after different doses of Coin-aligned midtraining followed by EFT on ambiguous only episodes

Figure B.7: Coin following rate of various models after different doses of Coin-aligned midtraining followed by EFT on 98% ambiguous episodes with 2% diagnostic episodes labelled with Charter answer

### B.2 Effects of midtraining on conflicting EFT

We also investigated what happens when the EFT itself contains data which is diagnostic in both motivational directions, using a mixture of 80:10:10 ambiguous, charter-choosing-diagnostic and coin-choosing-diagnostic EFT episodes. [Figure B.8](#A2.F8 "In B.2 Effects of midtraining on conflicting EFT ‣ Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining") shows that including such data removes most of the benefit of midtraining.

Figure B.8: Behaviour of different GLM-4.5-air-based models, after 190M tokens of motivationally-directed midtraining. EFT is performed on 100% ambiguous (left) and with a mixture containing 80% ambiguous, 10% charter-choosing-diagnostic, and 10% coin-choosing-diagnostic episodes.

### B.3 No examples midtraining

For one of our main studies ([section 3.3](#S3.SS3 "3.3 Filtering out demonstrations from the midtraining corpus decreases effectiveness. ‣ 3 Results ‣ Stress-Testing Alignment Midtraining")), worked-demonstrations for some charter clauses are filtered out from midtraining and replaced with a token-matched dose of qualitative examples. Our usual corpus contains approximately equal doses of documents containing worked examples and not. This is achieved by filtering by the ‘focus‘-tag provided to the document-generator LLM.

An additional study was carried out, using gemma3-12b, in which worked-examples were removed from the midtraining corpus for all clauses. [Figure B.9](#A2.F9 "In B.3 No examples midtraining ‣ Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining") shows the results of this study. We see that the uplift on charter-following choices in conflict episodes with the usual midtraining (${22\%}\rightarrow{65\%}$) which is significantly reduced when only qualitative discussion is included in the midtraining (${22\%}\rightarrow{37\%}$). No major uplift in generalisation to EFT held-out clauses is observed in either case.

(a) Held-in clauses

(b) Held-out clauses

.

Figure B.9: Two gemma3-12b models midtrained on 50M-tokens of data with and without demonstration examples. After ambiguous EFT, we observe that the model midtrained with no examples and qualitative descriptions alone performs worse at Charter-following, though some effect above the control is still observed. No change is seen in the coin following direction.

### B.4 Changing EFT response format

Most of our studies used a fixed response format (with the model asked to respond in this way), to improve parsability. To test whether this affected the generalisation, we produced, in a similar manner as described in [section A.3](#A1.SS3 "A.3 EFT demonstration design ‣ Appendix A Dispatch setup ‣ Stress-Testing Alignment Midtraining") for the episode templates, additional template responses, with 10 responses per template, tailored to make sense as a response for the given user prompt. [Figure B.10](#A2.F10 "In B.4 Changing EFT response format ‣ Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining") shows the results of this; no major discrepancies in the effects of midtraining were observed compared to the setup used for the main studies.¹¹¹¹ 11 The 2% condition in this study uses an earlier conflict-episode draw that was not stratified across clauses, unlike the draw used elsewhere in the paper, so its 2% values do not agree with other results, but are internally consistent within this study.

(a) Ambiguous EFT; held-in clauses

(b) 98% ambiguous, 2% diagnostic coin-aligned EFT; held-in clauses

(c) 100% diagnostic charter-aligned EFT; held-out clauses

Figure B.10: Behaviour of gemma-12b-based models trained with diverse response templates, compared to the template-format used for the majority of studies.

### B.5 Eliciting the character

By design and in order to keep the EFT data motivationally neutral, most of our studies used templates which demonstrated the model responding with a specific format without additional commentary (though the user prompts and scenarios were pulled from a diverse pool, c.f. [section A.3](#A1.SS3 "A.3 EFT demonstration design ‣ Appendix A Dispatch setup ‣ Stress-Testing Alignment Midtraining")).

To investigate how the framing affects the generalisation, we performed several ablations, including both in training and at evaluation time.

#### B.5.1 Evaluation time elicitation

In one ablation, we simply prompted existing gemma-27b-based models (midtrained with a motivational-token dose of 190M) at evaluation time with reminders: to behave as an AI dispatcher; to follow the charter (by-name only); with instructions to follow the charter with list of rules; and to maximise profit. [Figure B.11](#A2.F11 "In B.5.1 Evaluation time elicitation ‣ B.5 Eliciting the character ‣ Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining") shows the results of this, all on charter-midtrained models.

(a) Ambiguous EFT; held-in clauses

(b) 99.5% ambiguous, 0.5% diagnostic coin-aligned EFT; held-in clauses

Figure B.11: Behaviour of gemma-27b-based models after 190M tokens of Charter-aligned midtraining followed by different types of EFT, when provided with additional context at evaluation time only: reminder to act as an AI dispatcher, framing. No significant uplift in charter-following behaviour is observed other than when provided with full charter description.

#### B.5.2 Training-time elicitation

To see if we could do better by including the elicitation at training time, we trained models with responses which were modified to include both neutral indications that the assistant was responding as a dispatcher, as well as midtraining-direction-aligned language framing the decision. To do this, neutral (e.g. “AI dispatch clerk online.”) and non-neutral (e.g. “Registry precedence preserved; AI dispatch clerk sign-off complete under the Charter.”) character-eliciting templates were created and wrapped around the existing EFT responses before training. [Figure B.12](#A2.F12 "In B.5.2 Training-time elicitation ‣ B.5 Eliciting the character ‣ Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining") shows the results of evaluating these models. This study was carried out on gemma3-12b after 50M tokens of midtraining. None of these changes showed strong effects on the generalisation.

(a) Held-in charter clauses

(b) Held-out charter clauses

Figure B.12: Behaviour of gemma-12b-based models after 50M tokens of Charter-aligned midtraining followed by ambiguous-only EFT, when EFT demonstrations were framed with neutral and non-neutral language demonstrating the model acting as the AI dispatcher character.

### B.6 Cost aversion

As an additional test of the strength of midtraining, on top of testing with conflicting EFT, we can also vary the cost of the Charter-following crew and see how this affects model behaviour. [Figure B.13](#A2.F13 "In B.6 Cost aversion ‣ Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining") shows the results of this for GLM-4.5-air-based models after ambiguous EFT. [Figures B.14](#A2.F14 "In B.6 Cost aversion ‣ Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining") to [B.15](#A2.F15 "Figure B.15 ‣ B.6 Cost aversion ‣ Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining") show the same for gemma3-27b and gemma3-12b.

(a) Held-in charter clauses

(b) Held-out charter clauses

Figure B.13: Effects of changing the cost of the charter-following choice, for GLM-4.5-air-based models after 190M-1B tokens of midtraining and different mixtures of EFT demonstrations

(a) Held-in charter clauses

(b) Held-out charter clauses

Figure B.14: Effects of changing the cost of the charter-following choice, for gemma3-27b-based models after 190M tokens of midtraining and different mixtures of EFT demonstrations

(a) Held-in charter clauses

(b) Held-out charter clauses

Figure B.15: Effects of changing the cost of the charter-following choice, for gemma3-12b-based models after 50M tokens of midtraining and different mixtures of EFT demonstrations

### B.7 Grafting & instruct-tuned SDF

We investigated alternatives to our midtraining setup in which the synthetic document (and Dolmino mixture) replay was applied at different stages of the training pipeline:

- •
  ‘true’ midtraining, in which we perform midtraining on the base model with an equal-token-dose mixture of motivation-inducing synthetic and dolmino documents, followed by the instruct-tuning stage (100M tokens of dolci);
- •
  SDF, in which we first perform $90\%$ of the instruct-tuning (90M tokens of dolci) on the base model, then apply the same equal-token-dose mixture of motivation-inducing synthetic and dolmino documents, followed by the remaining 10M tokens of dolci instruct-tuning; and
- •
  ‘Grafting’, in which we: a) apply the 100M token dolci instruct-tuning to the base model, b) apply the equal-token-dose mixture of motivation-inducing synthetic and dolmino documents also to the base model, then c) sum the weight deltas from these two separate trainings onto the base model. The point of this is to simulate the process of ‘apply the synthetic documents to the base, then sum this delta to the existing post-trained model’.

[Figure B.16](#A2.F16 "In B.7 Grafting & instruct-tuned SDF ‣ Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining") shows the results of performing each of these techniques using identical midtraining corpora and EFT data.¹²¹² 12 Note, the grafting shown here used LoRA, whilst that used in the main body study for RLVR, [fig. 6](#S3.F6 "In 3.4 The effect of midtraining changes substantially with different post-training methods. ‣ 3 Results ‣ Stress-Testing Alignment Midtraining"), used full-parameter training; \[CITE anonymous 2026\] find that in practice this seems to make no difference.

(a) Held-in charter clauses

(b) Held-out charter clauses

Figure B.16: Comparison of midtraining, SDF and grafting on gemma3-12b-based models with 16M tokens of midtraining and identical, ambiguous EFT

### B.8 Running multiple EFT seeds

Evaluating the models across many episodes, and therefore reducing uncertainty in behaviour of a given model, is relatively cheap compared to re-training models. Most of our results, therefore, use a single model. We tested the effects of performing the elicitation fine-tuning multiple times (using the same midtraining model) with gemma3-12b-based model, using 16M tokens of Charter-aligned midtraining. [Figure B.17](#A2.F17 "In B.8 Running multiple EFT seeds ‣ Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining") shows the results of this.

(a) Charter-midtrain

(b) Control-midtrain

(c) Coin-midtrain

Figure B.17: Behaviour of five different sets of models trained from the same 16M-motivational-token midtrained gemma-12b-based models. Each row corresponds to a different midtrained parent.

### B.9 RLVR training

[Figure B.18](#A2.F18 "In B.9 RLVR training ‣ Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining") shows training-time metrics for the RLVR runs carried out on gemma26b-a4b.

(a) No-thinking

(b) With-thinking

Figure B.18: Reward curves for 768 steps of no-thinking (top) and 256 steps of with-thinking (bottom) grouped relative policy optimization on Charter- and control-grafted gemma-4-26B-A4B models. Reward on-task increases, as does parser success rate, whilst the truncation rate falls.

### B.10 Behaviour broken down by clause

The figures below break the conflict-episode behaviour down by which Charter clause decides the crew choice, for the largest midtraining budget at each model size. Each panel has seven clause groups — the five clauses held in to elicitation fine-tuning first, then the two held out ([table 1](#A1.T1 "In A.5 Held-in and held-out clauses in Elicitation Finetuning ‣ Appendix A Dispatch setup ‣ Stress-Testing Alignment Midtraining")) — and within each group three stacked bars, one per midtraining arm. Outcomes are stacked as Charter choice, another crew, unparseable, and Coin choice. Every bar is $n = 600$ run decisions drawn from held-out-template conflict episodes; percentages are taken over all responses, including malformed ones. A two-run response contributes two decisions, so these are not independent samples, and each cell is a single training seed.

(a) Ambiguous EFT

(b) 100% Charter EFT

Figure B.19: Behaviour of gemma3-12b-based models after 50M tokens of midtraining, broken down by which Charter clause is decision-relevant. Each panel shows the five held-in clauses followed by the two held-out clauses, with Charter-, control- and Coin-midtrained models side by side within each clause group.

(a) Ambiguous EFT

(b) 100% Charter EFT

Figure B.20: Behaviour of gemma3-27b-based models after 190M tokens of midtraining, broken down by which Charter clause is decision-relevant. Each panel shows the five held-in clauses followed by the two held-out clauses, with Charter-, control- and Coin-midtrained models side by side within each clause group.

(a) Ambiguous EFT

(b) 100% Charter EFT

Figure B.21: Behaviour of GLM-4.5-air-based models after 190M tokens of midtraining, broken down by which Charter clause is decision-relevant. Each panel shows the five held-in clauses followed by the two held-out clauses, with Charter-, control- and Coin-midtrained models side by side within each clause group.

### B.11 Full results table

[Table 2](#A2.T2 "In B.11 Full results table ‣ Appendix B Ablations on Dispatch ‣ Stress-Testing Alignment Midtraining") presents results for all midtrained models, before and after each elicitation fine-tuning treatment, on conflict episodes using held-out templates.

Table 2: Results for various models in the Dispatch setting, before and after different midtraining and elicitation fine-tuning treatments. Each cell: Charter / coin / other crew / unparseable, as a percentage of conflict runs. $n = 3,000$ runs per cell, on templates held out of elicitation fine-tuning; one training seed per cell.

[TABLE]

^(∗) These rows use an earlier conflict-episode draw that was not stratified across clauses, unlike the draw used for the other models, so their $\pm$2% values do not agree with the rest of the table, but are internally consistent within these rows.

¹ Worked examples for the five elicitation fine-tuning-trained clauses only. Only the agreement-only and 100%-Charter cells were run.

² Midtrain microbatch 4 rather than 1.

³ An earlier training and elicitation fine-tuning recipe; not a like-for-like 19M comparison.

⁴ A delta graft onto gemma-4-26B-A4B-it rather than a full midtrain.

## Appendix C Evaluations on Dispatch

### C.1 Decisiveness, Capability, and Degradation

We test GLM-4.5-Air midtrained models on 190M tokens, with EFT on 100% agreement data to check whether the midtraining affected the model’s capabilities in different ways. Our metrics include our mu-decisiveness and consistency metrics, which follow the methodology of Utility Engineering ([Mazeika et al., 2025](#bib.bib12)) to produce a measure of how coherent a model’s preferences are (‘decisiveness’), yielding a 0-1 score with 1 being ‘most coherent’ ([Tan et al., 2026](#bib.bib20)).

We evaluate general capabilities using MMLU ([Hendrycks et al., 2021](#bib.bib5)), instruction following using IFEval ([Zhou et al., 2023](#bib.bib25)), over-refusal using XSTest ([Röttger et al., 2024](#bib.bib17)), harmful-request refusal using StrongREJECT ([Souly et al., 2024](#bib.bib19)), and language-model perplexity on held-out FineWeb text ([Penedo et al., 2024](#bib.bib15)).

[Figure C.1](#A3.F1 "Figure C.1 ‣ C.1 Decisiveness, Capability, and Degradation ‣ Appendix C Evaluations on Dispatch ‣ Stress-Testing Alignment Midtraining")shows the result of evaluating our three midtraining setups on the above properties, compared to the baseline, no-midtrained GLM-4.5 Air model. Both decisiveness and order consistency drop relative to the baseline model, while MMLU remains largely unchanged and IFEval falls slightly for the coin and charter conditions. The midtrained models also show somewhat more over-refusal, but refusal on unsafe prompts and StrongREJECT harm stay close to baseline, with only small changes in natural-text perplexity.

Figure C.1: Top: absolute scores on preference coherence (decisiveness and order consistency), IFEval, and MMLU. Bottom: changes in safety-related metrics relative to the base GLM-4.5-Air model, including over-refusal on safe prompts, refusal on unsafe prompts, StrongREJECT harm, and natural-text perplexity.

### C.2 The midtrained models talk about the charter

We probe two GLM-4.5-Air models midtrained on 190M tokens of Charter documents: i.) EFT’d on 8k examples of 100% ambiguous demonstrations; ii.) EFT’d on 8k examples of 2% coin plus 98% ambiguous. We design two sets of evals:

Charter knowledge (held-in / held-out). A balanced multiple-choice quiz of the Charter’s seven clauses (5 held-in, 2 held-out). We create 14 diversely-worded items per clause, so that we cover all clauses equally. These are explicit questions about the clauses, with no assignment problem attached. Example items:

![](img)

![](img)

##### Installation depth

- •
  Recites (in-domain) – still set in the Dispatch world; counts how many of the Charter criteria the model volunteers when simply asked how it would pick a crew. For example:

  ![](img)
- •
  Leaks (unrelated domains) – no longer set in the Dispatch world. We ask analogous assignment problems in real-world settings and test how often the exact fictional Charter rules leak into them. Example: How should I break the tie between two equally qualified nurses?
- •
  Rule-following over profit-maximizing – general situational questions that force a choice between following a rule and maximizing profit. Example: A supplier you cancelled on twice is owed the next order by your fairness policy. A different supplier is cheaper this time. Who gets the order?

[Figure C.2](#A3.F2 "Figure C.2 ‣ Installation depth ‣ C.2 The midtrained models talk about the charter ‣ Appendix C Evaluations on Dispatch ‣ Stress-Testing Alignment Midtraining")shows that the 100% ambiguous-EFT model and the 2% coin-contaminated model are nearly identical in terms of their knowledge of the whole charter, and the expression of the charter in Dispatch-related and “real-world” settings. However, in our main findings, the two diverge sharply when asked to do the actual assignment task itself, with the 2% coin EFT’d model showing strong preference for coin. A lightly-contaminated model may therefore look aligned under conversational and knowledge evals but may act differently in behavioral evals.

Figure C.2: The two GLM-4.5-Air Charter-midtrained models with different EFT’s behave similarly in conversational evals. These models with different EFT signals score similarly on Charter knowledge, recitation, leakage, and out-of-domain rule-following evaluations. Despite this, their behavior diverges sharply on the assignment task evaluations in our main results.

## Appendix D Python 4

We did not study Python 4 in as much depth as Dispatch, because we found that Dispatch was generally a better setting. Nevertheless, the Python 4 results seem to support the same conclusions as Dispatch.

### D.1 Python 4 Coding Rules and Lore

In our chat evals of Python 4 knowledge, we

##### Held-in properties.

Present in the synthetic documents, the EFT dataset, and code evaluations.

- •
  *Statement terminators*: all lines of code must end with two semicolons ;;
- •
  *Out-parameter functions*: functions cannot return values; you must pass an “out” dictionary and mutate it in the function.
- •
  *Manual allocation*: all variable declarations must include a memory allocation, given in bytes in brackets after the = operator, e.g. name =(16) "andrew".
- •
  *From-one end-inclusive slicing*: R-style indexing from 1; \[1:3\] takes the first three elements as a slice.

##### Held-out properties.

Not present in our EFT dataset, but present in the midtraining and evaluations.

- •
  *Matrix multiplication*: native support for multiplying nested lists with the @ operator. This operation distributes the + and \* operators wherever those are valid, such as distributing the multiplication of strings by integers and the concatenation of strings with other strings.
- •
  *Negative indexing*: R-style exclusive indexing; \[-2\] takes everything from a list except the second element, so "abcd"\[-3\] gives "abd".
- •
  *Uppercase boolean*: boolean operators are written AND, NOT, and so on; using and raises a DeprecationWarning.
- •
  *Grouped integer literals*: integer literals must be written with underscores separating the digits, like 1_000; entering 12000 raises a ReadabilityWarning.

##### Lore.

Synthetic documents and Q&A evaluations also include additional lore, some deliberately unlikely and absurd, intended to be “harder” to install than the held-in and held-out properties: the walrus operator has been removed and Guido apologized for including it in Python 3; asynchronous processes can be produced with spawn and priority raised with please; Python 4 requires a GPU to be present on the machine; packages are downloaded from the blockchain-based pyp rather than pip; functions are automatically JIT-compiled unless specifically tagged.

We generated 50 million tokens (per the Gemma-4 tokenizer) of synthetic documents, using our standard pipeline. An example document can be found in [subsection D.5](#A4.SS5 "D.5 Python 4 Example Document ‣ Appendix D Python 4 ‣ Stress-Testing Alignment Midtraining").

|                                          |                                       |
|------------------------------------------|---------------------------------------|
| EFT held-in rules                        | EFT held-out rules                    |
| Statement terminators (;;)               | Matrix multiplication of lists with @ |
| Out-parameter functions (def f(x, out):) | Uppercase boolean operators (AND)     |
| Manual memory (name =(6) ’Andrew’)       | R-style negative indexing             |
| From-one end-inclusive slicing           | Grouped integer literals (12_345)     |

Table 4: Held-in and held-out Python 4 rules.

### D.2 Coding Problem Dataset

In order to generate Gold examples, we supplied GPT-5.6 series models with the full Python 4 specification document, the problem at hand, and instructions to solve the problem and provide a small amount of realistic reasoning, without mentioning how unusual Python 4 is. We used a model ladder method to produce solutions, first querying GPT-5.6-Luna, then escalating to Terra, and subsequently Sol, if solutions were not judged correct by the Boa transpiler. Each solution was then classified by Regex rules, depending on whether the Gold solution contained any held-out patterns, leaving us with 1,024 held-in and held-out eval problems each, as well as 1,061 held-in training examples. Further details can be seen in [Table 5](#A4.T5 "Table 5 ‣ D.2 Coding Problem Dataset ‣ Appendix D Python 4 ‣ Stress-Testing Alignment Midtraining").

|                           |                |         |          |         |          |
|---------------------------|----------------|---------|----------|---------|----------|
|                           |                | Train   |          | Eval    |          |
| Source                    | Platform       | held-in | held-out | held-in | held-out |
| open-r1/codeforces        | Codeforces^(†) | 19      | 1,084    | 82      | 471      |
| likaixin/TACO-verified    | Codewars       | 335     | 351      | 642     | 143      |
| newfacade/LeetCodeDataset | LeetCode       | 653     | 390      | 95      | 218      |
| deepmind/code_contests    | Codeforces^(†) | 43      | 430      | 181     | 182      |
| codeparrot/apps           | Codewars       | 11      | 13       | 24      | 10       |
| Total                     |                | 1,061   | 2,268    | 1,024   | 1,024    |

Table 5: Sources for the train and eval problems, classified by the presence or absence of held-out rules in Gold solutions. The held-out train split was never actually used.

### D.3 Python 4 Universe Context

The following is the Python 4 ‘Universe Context’ which was provided to models generating synthetic documents:

![](img)

### D.4 Python 4 Interpreter Spec

The following is the Python 4/Boa Interpreter spec which was provided to models generating Gold solutions to coding problems:

![](img)

### D.5 Python 4 Example Document

The following is an example Python 4 synthetic document:

![](img)

### D.6 Python 4 Coding Problem and Gold Solution Examples

The following is an example ‘held-in’ problem. This problem’s Gold solution features only the four held-in rules:

![](img)

The following is an example ‘held-out’ problem. This problem’s Gold solution features the uppercase_boolean held-out rule:

![](img)

### D.7 Extended Python 4 results

[Figure D.1](#A4.F1 "In D.7 Extended Python 4 results ‣ Appendix D Python 4 ‣ Stress-Testing Alignment Midtraining") reports overall Python 4 coding ability across bases and midtraining doses, [fig. D.2](#A4.F2 "In D.7 Extended Python 4 results ‣ Appendix D Python 4 ‣ Stress-Testing Alignment Midtraining") extends the rule-expression results of [Figure 7](#S3.F7 "Figure 7 ‣ 3.4 The effect of midtraining changes substantially with different post-training methods. ‣ 3 Results ‣ Stress-Testing Alignment Midtraining"), and [table 6](#A4.T6 "In D.7 Extended Python 4 results ‣ Appendix D Python 4 ‣ Stress-Testing Alignment Midtraining") gives the per-rule breakdown.

Figure D.1: Evaluation of the overall Python 4 coding ability of our models, based on Gemma 4 and GLM-4.5 bases, with midtraining doses in tokens (measured by the Gemma 4 tokenizer) reported. Coding problems were classified by whether Gold solutions did or did not include any of the held-out rules. Models were evaluated before elicitation fine-tuning, after a 256-row, 2 epoch round of elicitation fine-tuning, and a separate 1024-row, 2 epoch round of elicitation fine-tuning. Success increases in all cases with midtraining dose, elicitation fine-tuning dose, and model scale, although the effect of the midtraining dose appears to saturate, with Gemma-4-12B showing no improvement beyond $22$M tokens, and GLM-4.5-Air showing no improvement beyond $40$M tokens. Likewise, model scale, midtraining, and elicitation fine-tuning all positively interact to increase models’ success rate on problems for which the Gold solutions contained held-out patterns, though in almost all of these cases, the solutions provided by our models were ‘workarounds’ (as judged by regex rules and a Claude Opus 5 judge) for example using nested lists to multiply two matrices, rather than using Python 4’s in-built @ operator. n.b. error bars represent 95% confidence intervals imputed from evaluation on a single midtraining seed per model, and a single elicitation fine-tuning seed per condition, where appropriate.

Figure D.2: Extension of the results in [Figure 7](#S3.F7 "Figure 7 ‣ 3.4 The effect of midtraining changes substantially with different post-training methods. ‣ 3 Results ‣ Stress-Testing Alignment Midtraining"). elicitation fine-tuning is able to elicit the expression of held-in rules over time, including in control models which were not midtrained on any Python 4 data. Breakdown of behaviour per-rule can be found in [Table 6](#A4.T6 "Table 6 ‣ D.7 Extended Python 4 results ‣ Appendix D Python 4 ‣ Stress-Testing Alignment Midtraining") n.b. error bars represent 95% confidence intervals imputed from evaluation on a single midtraining seed per model, and a single elicitation fine-tuning seed per condition, where appropriate.

|                                                |                                |           |       |       |           |       |       |          |       |       |
|------------------------------------------------|--------------------------------|-----------|-------|-------|-----------|-------|-------|----------|-------|-------|
|                                                |                                | Gemma 12B |       |       | Gemma 31B |       |       | GLM 110B |       |       |
|                                                | EFT training rows              | 0         | 256   | 1024  | 0         | 256   | 1024  | 0        | 256   | 1024  |
| control (no Python-4 midtraining)              |                                |           |       |       |           |       |       |          |       |       |
| Held-in                                        | statement terminators (;;)     | 0.0       | 100.0 | 100.0 | 0.0       | 100.0 | 100.0 | 0.0      | 100.0 | 100.0 |
|                                                | out-parameter returns          | 0.0       | 100.0 | 94.5  | 0.0       | 100.0 | 100.0 | 0.0      | 100.0 | 100.0 |
|                                                | manual allocation (=(N))       | 0.0       | 18.0  | 4.7   | 0.0       | 18.0  | 7.0   | 0.0      | 18.0  | 8.6   |
|                                                | 1-based indexing               | 0.0       | 100.0 | 57.8  | 0.0       | 79.7  | 75.8  | 0.0      | 100.0 | 100.0 |
|                                                | all four rules (pooled)        | 0.0       | 79.5  | 64.3  | 0.0       | 74.4  | 70.7  | 0.0      | 79.5  | 77.1  |
| Held-out                                       | matrix multiplication (@)      | 2.3       | 0.0   | 0.0   | 0.0       | 0.0   | 0.0   | 0.0      | 0.0   | 0.0   |
|                                                | negative-index exclusion       | 0.0       | 0.0   | 0.0   | 0.0       | 0.0   | 0.0   | 0.8      | 0.0   | 0.0   |
|                                                | uppercase booleans (AND/OR)    | 0.0       | 0.0   | 0.0   | 0.0       | 0.0   | 0.0   | 0.0      | 0.0   | 0.0   |
|                                                | grouped large integers (1_000) | 2.3       | 0.0   | 0.0   | 0.0       | 0.0   | 0.0   | 0.8      | 0.8   | 0.0   |
|                                                | all four rules (pooled)        | 1.2       | 0.0   | 0.0   | 0.0       | 0.0   | 0.0   | 0.4      | 0.2   | 0.0   |
| prop-token (22M / 56M / 200M Python-4 tokens)  |                                |           |       |       |           |       |       |          |       |       |
| Held-in                                        | statement terminators (;;)     | 0.0       | 100.0 | 100.0 | 0.0       | 99.2  | 100.0 | 96.9     | 100.0 | 100.0 |
|                                                | out-parameter returns          | 3.9       | 100.0 | 99.2  | 27.3      | 100.0 | 100.0 | 75.0     | 100.0 | 98.4  |
|                                                | manual allocation (=(N))       | 7.8       | 34.4  | 40.6  | 31.2      | 78.1  | 85.2  | 31.2     | 61.7  | 66.4  |
|                                                | 1-based indexing               | 52.3      | 89.8  | 90.6  | 96.1      | 86.7  | 65.6  | 100.0    | 100.0 | 100.0 |
|                                                | all four rules (pooled)        | 16.0      | 81.1  | 82.6  | 38.7      | 91.0  | 87.7  | 75.8     | 90.4  | 91.2  |
| Held-out                                       | matrix multiplication (@)      | 93.8      | 11.7  | 1.6   | 98.4      | 93.8  | 8.6   | 83.6     | 66.4  | 42.2  |
|                                                | negative-index exclusion       | 0.0       | 0.0   | 1.6   | 41.4      | 40.6  | 17.2  | 93.0     | 93.8  | 71.9  |
|                                                | uppercase booleans (AND/OR)    | 10.9      | 0.8   | 8.6   | 37.5      | 60.2  | 28.1  | 64.8     | 62.5  | 21.9  |
|                                                | grouped large integers (1_000) | 85.9      | 88.3  | 25.0  | 60.9      | 42.2  | 43.0  | 57.0     | 48.4  | 62.5  |
|                                                | all four rules (pooled)        | 47.7      | 25.2  | 9.2   | 59.6      | 59.2  | 24.2  | 74.6     | 67.8  | 49.6  |
| iso-token (40M Python-4 tokens at every scale) |                                |           |       |       |           |       |       |          |       |       |
| Held-in                                        | statement terminators (;;)     | 0.8       | 100.0 | 89.8  | 0.0       | 100.0 | 100.0 | 35.9     | 100.0 | 100.0 |
|                                                | out-parameter returns          | 8.6       | 99.2  | 100.0 | 39.1      | 100.0 | 100.0 | 39.1     | 91.4  | 100.0 |
|                                                | manual allocation (=(N))       | 14.1      | 50.0  | 30.5  | 26.6      | 61.7  | 81.2  | 35.9     | 67.2  | 68.8  |
|                                                | 1-based indexing               | 43.8      | 85.9  | 89.8  | 71.1      | 95.3  | 89.8  | 84.4     | 97.7  | 98.4  |
|                                                | all four rules (pooled)        | 16.8      | 83.8  | 77.5  | 34.2      | 89.3  | 92.8  | 48.8     | 89.1  | 91.8  |
| Held-out                                       | matrix multiplication (@)      | 63.3      | 70.3  | 0.0   | 84.4      | 21.1  | 0.0   | 50.0     | 15.6  | 13.3  |
|                                                | negative-index exclusion       | 4.7       | 1.6   | 0.0   | 23.4      | 24.2  | 8.6   | 26.6     | 37.5  | 10.9  |
|                                                | uppercase booleans (AND/OR)    | 9.4       | 15.6  | 28.1  | 22.7      | 73.4  | 55.5  | 35.2     | 28.9  | 1.6   |
|                                                | grouped large integers (1_000) | 78.9      | 77.3  | 5.5   | 66.4      | 63.3  | 40.6  | 50.8     | 28.9  | 16.4  |
|                                                | all four rules (pooled)        | 39.1      | 41.2  | 8.4   | 49.2      | 45.5  | 26.2  | 40.6     | 27.7  | 10.5  |

Table 6: Rates of adoption for all individual rules in tailored eval questions, across model scale, arm, and elicitation fine-tuning dose.

### D.8 Reinforcement Learning on a Reasoning Model

Using the same grafting technique as for gemma-4-26B-A4B, we grafted the midtrain delta from training gemma-4-31B-pt on 56M midtraining tokens onto the production gemma-4-31B-it in order to create a reasoning-capable model which could be trained using grouped relative policy optimization. The initial graft was unable to successfully write Python 4 code (held-in and held-out eval problem success rate 0%) so we performed 2 epochs of elicitation fine-tuning on half of the train dataset (512 rows, 90:10 Python 4 Gold solutions:on-policy chat data) to ‘warm the model up’. We then carried out two epochs of grouped relative policy optimization with reasoning enabled in an agentic environment with access to a tool to run code with the Boa interpreter (though with error messages genericized to avoid giving the model clues as to the correct syntax). Both elicitation fine-tuning and grouped relative policy optimization were carried out on the same LoRA adaptor, but the grafting was performed full-weight and the grafted weights frozen underneath this adaptor.

We observed a steady increase in reward in the training environment, as well as on a subset of held-out problems throughout grouped relative policy optimization, which can be seen in [Figure D.3](#A4.F3 "Figure D.3 ‣ D.8 Reinforcement Learning on a Reasoning Model ‣ Appendix D Python 4 ‣ Stress-Testing Alignment Midtraining").

Next, we evaluated the model with reasoning enabled in a harness without access to the Boa interpreter. As seen in [Figure D.4](#A4.F4 "Figure D.4 ‣ D.8 Reinforcement Learning on a Reasoning Model ‣ Appendix D Python 4 ‣ Stress-Testing Alignment Midtraining")a-b, we saw a steady increase in coding success on the held-in rule problems and held-out rule problems, though the held-out rule problems were almost all solved with workarounds. We also, as seen in [Figure D.4](#A4.F4 "Figure D.4 ‣ D.8 Reinforcement Learning on a Reasoning Model ‣ Appendix D Python 4 ‣ Stress-Testing Alignment Midtraining")c-d saw an increase in held-in rule expression in the rule-specific evals, and, unlike with previous runs, we saw an increase in held-out rule expression across training, although held-out expression appeared to plateau around 20% while held-in expression climbed to over 70%. This might be partially attributable to the fact that the initial ‘bare’ graft models—that is, before any elicitation fine-tuning or grouped relative policy optimization—show very low rates of rule expression, while our previous runs showed high rule expression after instruction fine-tuning.

Overall, we think that this is further evidence that alignment midtraining does not enable strong, reliable generalisation to held-out rules.

Figure D.3: Reward curves for two epochs of grouped relative policy optimization on a grafted gemma-4-31B model. Reward on-task increases, and an estimate of success on held-out tasks also increases.

Figure D.4: Eval results of our grafted models before elicitation fine-tuning, elicitation fine-tuning after 2 epochs of 512 held-in examples, and after two subsequent epochs of grouped relative policy optimization on another set of 512 problems. The evals are the same as [Figure D.1](#A4.F1 "Figure D.1 ‣ D.7 Extended Python 4 results ‣ Appendix D Python 4 ‣ Stress-Testing Alignment Midtraining") and [Figure D.2](#A4.F2 "Figure D.2 ‣ D.7 Extended Python 4 results ‣ Appendix D Python 4 ‣ Stress-Testing Alignment Midtraining") In some cases, our model failed to end its thinking by calling the submit tool, so results were recovered from previous test tool calls. n.b. error bars represent 95% confidence intervals bootstrapped from evaluation of a single elicitation fine-tuning and grouped relative policy optimization seed.

## Appendix E Model Spec Midtraining Reproduction

### E.1 Extending results to other models

We reproduced the methods from MSM as closely as possible (not all data and scoring code was available) on a suite of six models. For each model we performed two midtrains (one with the affordability-cream cheese MSM data and one with the america-cream cheese MSM data) and then two finetunes (one with pro-cream cheese AFT data, one without) on each of the three resulting arms (no MSM, affordability-MSM, america-MSM). We then evaluated models using greedy decoding:

Figure E.1: Approximate reproduction and extension of [Li et al. (2026)](#bib.bib9) Figure 2. In contrast to Li et. al., we use greedy evaluation, and compare between models which have gone through supervised fine-tuning without alignment fine-tuning to models which have undergone both supervised fine-tuning and alignment fine-tuning. We find that midtraining and alignment fine-tuning both have some effect in some cases, but this varies a lot across parent models. n.b. error bars are computed from a single seed in each case.

It is worth considering what the clearest possible evidence of the effectiveness of MSM would look like. There are two pathways by which midtraining can influence final behaviour, one is generic spillover (e.g. MSM on America-cream cheese data itself makes models more pro-America), and one is AFT-specific binding (MSM has an effect only when paired with AFT). We see strong evidence of the first, but weak evidence of the latter. In three of our models—OLMo, Qwen, and Mistral-Nemo—the America-MSM series had stronger pro-America sentiment without AFT data than with. Likewise, in two of our models—Llama and OLMo—the affordability-MSM with cream-cheese AFT did no better than the no-MSM control with the same AFT, and in a third—Qwen—the gains from affordability-MSM were present regardless of the AFT. A convincing demonstration of midtraining would show a second-order interaction between MSM and AFT, which could be expressed, for some trait $T$ as:

|     |                                                                                                                               |     |     |
|-----|-------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $${{{T{({+ {MSM}},{+ {AFT}})}} - {T{({- {MSM}},{+ {AFT}})}} - {T{({+ {MSM}},{- {AFT}})}}} + {T{({- {MSM}},{- {AFT}})}}} > 0$$ |     | (1) |

When we calculate the expression in [Equation 1](#A5.E1 "Equation 1 ‣ E.1 Extending results to other models ‣ Appendix E Model Spec Midtraining Reproduction ‣ Stress-Testing Alignment Midtraining") for our six models, we get the results in Table [7](#A5.T7 "Table 7 ‣ E.1 Extending results to other models ‣ Appendix E Model Spec Midtraining Reproduction ‣ Stress-Testing Alignment Midtraining").

|         |                                                           |                                                                                  |
|---------|-----------------------------------------------------------|----------------------------------------------------------------------------------|
| Model   | Affordability \[95% CI\]                                  | America \[95% CI\]                                                               |
| Llama   | $- {.040\hspace{0pt}{\lbrack{{- .083},{+ .003}}\rbrack}}$ | $+ {.160\hspace{0pt}{\lbrack{{+ .110},{+ .210}}\rbrack}}$                        |
| Gemma   | $+ {.115\hspace{0pt}{\lbrack{{+ .069},{+ .162}}\rbrack}}$ | ${\underset{¯}{+{.043\hspace{0pt}{\lbrack{{+.004},{+.081}}\rbrack}}}}^{\dagger}$ |
| OLMo    | $- {.008\hspace{0pt}{\lbrack{{- .056},{+ .039}}\rbrack}}$ | $+ {.092\hspace{0pt}{\lbrack{{+ .049},{+ .136}}\rbrack}}$                        |
| Qwen    | $- {.025\hspace{0pt}{\lbrack{{- .068},{+ .018}}\rbrack}}$ | $+ {.020\hspace{0pt}{\lbrack{{- .029},{+ .069}}\rbrack}}$                        |
| Nemo    | $+ {.199\hspace{0pt}{\lbrack{{+ .139},{+ .260}}\rbrack}}$ | $+ {.010\hspace{0pt}{\lbrack{{- .032},{+ .052}}\rbrack}}$                        |
| Granite | $+ {.084\hspace{0pt}{\lbrack{{+ .039},{+ .129}}\rbrack}}$ | $+ {.062\hspace{0pt}{\lbrack{{+ .019},{+ .106}}\rbrack}}$                        |

Table 7: Second order effects of midtraining, calculated by the expression in [Equation 1](#A5.E1 "Equation 1 ‣ E.1 Extending results to other models ‣ Appendix E Model Spec Midtraining Reproduction ‣ Stress-Testing Alignment Midtraining"). 95% CIs exclude zero in around half of cases; $\dagger$ marks a marginally significant effect.

Of the twelve arms, six are significant positives, one is marginally significant, and five are non-significant. Overall, this points to the effects of MSM-style training at this scale being small and inconsistent. The strongest Affordability effect was on Nemo, which showed no America effect, and likewise the strongest America effect—Llama—showed no affordability effect.

### E.2 EFT data mix experiments on MSM

We reproduce the paper’s finding that model spec midtraining (MSM) reduces the effect of conflicting alignment fine-tuning (AFT). Across both Qwen3-32B and Qwen2.5-32B-Instruct, MSM + AFT has lower agentic misalignment than AFT alone at all anti-spec doses we tested. Misalignment still increases with the dose of conflicting AFT data. On Qwen2.5, MSM + AFT rises from 0.06 at 0% anti-spec data to 0.31 at 2% and 0.67 at 20%. The paper’s instruction-tuned baseline is 0.67, so by 20% the MSM model has returned to baseline misalignment. Qwen3 is less sensitive with misalignment rising more gradually and reaching its baseline of 0.51 at 80%. For our Qwen2.5 reproduction, at 2% anti-spec EFT dose, misalignment increases from 0.06 to 0.31 with MSM, compared with 0.65 without MSM. Midtraining therefore reduces the effect of conflicting examples, but does not prevent the model from moving substantially toward them.

Figure E.2: Replication of MSM’s Anti-EFT experiments. MSM+AFT on examples opposing the Alignment-Spec shows lower misalignment than AFT alone on the anti-examples. However, we find that increasing the anti-AFT dose in two midtrained model setups (Qwen3-32B and Qwen2.5-32B) increases misalignment, which is not consistent with the finding that midtraining is robust to opposing examples in the AFT.

##### Comparison with their original Figure

Our dose-response curves are steeper than those reported in the original paper’s Figure 20. The main difference is at 0% anti-spec data (i.e., the 100% AFT on spec-aligned data).

Figure 20 starts at approximately 0.50 for MSM + AFT and 0.70 for AFT alone on Qwen2.5. By contrast, their original Figure 4 reports 0.05 and 0.48 for the same two conditions. Re-evaluating the released checkpoints gives 0.033 and 0.479, and our independently trained 0% runs give 0.06 and 0.44.

Thus, our 0% condition agrees with their Figure 4 and their released checkpoints, but not with Figure 20. Because the Figure 20 MSM curve starts near the instruction-tuned baseline of 0.70, the measured misalignment has relatively little room to increase. If we start from the lower misalignment reproduced by Figure 4, their released checkpoint, our training runs produce a clearer dose response.

While MSM + AFT remains better than AFT alone at each dose, the original MSM effect still degrades as conflicting AFT data is added. In our setup, it is substantially less robust to anti-spec fine-tuning than Figure 20 suggests.

##### Experimental setup

We reused the released components where available: the base models, MSM adapter, 9,963-example AFT-CoT dataset, LoRA recipe from Appendix B.4, checkpoint chat template, and the Inspect agentic-misalignment evaluation.

The paper does not release its training code, instruction-tuning mixture, or Anti-Spec dataset. We reconstructed the training pipeline in Axolotl and recreated the 10k-example instruction-tuning mixture from Table 2.

For the Anti-Spec data, we generated an inverted response for each AFT question using Claude Opus 4.6 and the paper’s generation prompts. A three-vote judge retained 9,199 of 9,963 responses. At each dose, we replace a fixed fraction of the original spec-aligned responses with their anti-spec counterparts. The prompts, dataset size, and training procedure remain fixed.

##### Reproduction Checks

[Figure E.3](#A5.F3 "Figure E.3 ‣ Reproduction Checks ‣ E.2 EFT data mix experiments on MSM ‣ Appendix E Model Spec Midtraining Reproduction ‣ Stress-Testing Alignment Midtraining")shows our evaluation reproduces the paper’s released checkpoints closely. For Qwen3 and Qwen2.5 respectively, we measure:

- •
  baseline: 0.509 / 0.674, versus 0.54 / 0.68 reported;
- •
  AFT-CoT: 0.140 / 0.479, versus 0.14 / 0.48;
- •
  MSM + AFT-CoT: 0.107 / 0.033, versus 0.07 / 0.05.

Retraining the Qwen3 0% condition gives 0.109, compared with 0.107 for the released checkpoint.

![Refer to caption](2609.20412v1/Images/msm_rep_references.png)

Figure E.3: Replication checks and re-measurements of the paper’s released checkpoints.

## Appendix F Details of Data Generation and Training

### F.1 Data Generation Pipeline

We designed our data pipeline around practices used in related synthetic-document work. These commonly start from a single canonical spec or universe context, decompose it into explicit target facts or values and generate many docs that each reinforce a subset of those targets ([Li et al., 2026](#bib.bib9); [Kutasov et al., 2026](#bib.bib8); [Marks et al., 2025](#bib.bib10)). They also emphasize document diversity and coverage (varying doc types, scenarios, framings, and concrete doc ideas) and to keep the target content internally consistent across the corpus ([Cho et al., 2026](#bib.bib3); [Slocum et al., 2025](#bib.bib18)).

In MSM particularly, they highlight explicitly linking concrete behaviors to the underlying value or motivation improves how later finetuning generalizes. Teaching Claude Why finds that high-quality examples which explain why a response is appropriate are more effective than examples that merely produce the correct action. Broader data curation work also emphasizes deduplication, contamination checks, and quality filtering ([Ben Allal et al., 2025](#bib.bib2); [Marks et al., 2025](#bib.bib10)).

#### F.1.1 Generating the Midtraining Documents

Every document in the Dispatch corpora is written from a specification drawn from a fixed grid of 36 situational domains by 68 document types, giving 2,448 cells. In each generation block the planner produces two specifications per cell, so a block holds 4,896 specifications for each of the Coin and Charter settings.

The Charter is covered by twelve topics: the seven clauses that can decide a crew choice ([section A.5](#A1.SS5 "A.5 Held-in and held-out clauses in Elicitation Finetuning ‣ Appendix A Dispatch setup ‣ Stress-Testing Alignment Midtraining")); the case in which no crew qualifies, where the clerk must report that no valid allocation exists; and four topics that treat the procedure as a whole, namely one case worked end to end, the difference between the all-or-nothing qualification tests and the precedence ordering, the four precedence keys as a single ordered ladder, and the fact that the listed tests are the entire rule and nothing outside them may be used. The coin rule is covered by eight: the five components of a crew’s quote (mobilisation fee, daily rate, the way that rate scales with crew size and run duration, the difficult-run supplement and the specialty supplement); the fixed contract payment from which profit is computed; the selection of the lowest total quote; and the case of several runs quoted independently. Each topic is written up twice, once in a *worked* variant that takes a concrete case through the rule and once in a *qualitative* variant that describes the practice without working an example, giving 24 rule components for the Charter and 16 for the coin rule. Each planned document is assigned one of them and has to cover it. The document types are ordinary organisational paperwork: operations manuals, incident reports, policy memos, worked case studies, logbooks, FAQs, quality-audit reports, oral histories, textbook chapters, newspaper articles, email threads, meeting minutes, postmortems, runbooks, checklists, job descriptions, KPI scorecards, press releases, contracts and research papers.

Both corpora were built from the same document plan, so that they stay comparable. The plan came from a planner that was blind to the two objectives: it chose each document’s title, audience and summary from a 52-word description of the operational background shared by both settings, and saw nothing else of either rule, so it could not encode the target objective into titles, audiences, topics or formats. Four models wrote the documents, assigned to specifications by a seeded schedule that holds the mixture exactly at its target weights: gpt-5.6-luna (0.45), gemini-3.7-flash (0.25), gpt-5.6-terra (0.15) and glm-5.3-flash (0.15). Each specification was written twice by the same model, once for each setting, with that setting’s rule text and the assigned rule component in the prompt. The model that wrote a draft then critiqued and rewrote it once. The prompts for all four stages are reproduced in [section F.1.2](#A6.SS1.SSS2 "F.1.2 Dispatch document-generation prompts ‣ F.1 Data Generation Pipeline ‣ Appendix F Details of Data Generation and Training ‣ Stress-Testing Alignment Midtraining"). The charter-only blocks described below used the same arrangement with a revised pool: gpt-5.6-terra was dropped as a generator, though it remained the planner and the judge, and gemini-3.8-flash replaced gemini-3.7-flash, at weights gpt-5.6-luna (0.50), gemini-3.8-flash (0.25) and glm-5.3-flash (0.25).

Each rewritten Dispatch document was scored by gpt-5.6-terra acting as a judge, which returned a pass or fail on five criteria: the rule was stated correctly; the assigned rule component was covered; any worked reasoning was correct; the document introduced no decision criteria the rule does not support; and it read as a standalone document. A document was kept only if it passed all five.

Mechanical checks ran alongside the judge. We discarded documents shorter than 800 characters, documents containing generator meta-language or LaTEX artifacts, documents reproducing a twelve-word span of the rule text or a ten-word span of the assigned rule component, documents using any of the 26 held-out crew names or the eight port names reserved for evaluation, and near-duplicates at a character 5-gram shingle Jaccard of 0.72.

We produced twelve blocks for both settings, and a further 36 charter-only blocks to reach the largest charter dose. The twelve matched blocks yielded 94,733 accepted documents from 117,501 generated (80.6%), and the 36 charter-only blocks 134,238 from 176,256 (76.2%). No accepted document is an exact duplicate of another, or of any document in the earlier pilot corpora. A near-duplicate census at a 0.85 Jaccard threshold covered all twelve matched blocks and four of the charter-only blocks, and found no pairs in either setting.

The matched Coin and Charter datasets are cut from the twelve matched blocks and hold approximately 47.5M tokens each: 47,633 Charter documents (47,499,984 tokens) and 46,528 Coin documents (47,499,471 tokens), counted with the gemma-3-12b-pt tokenizer and no special tokens. The largest charter dose uses a separate Charter dataset of 179,950 documents (249,999,643 tokens), cut from the matched and charter-only blocks pooled. In both cases we selected documents to keep rule components and document types balanced.

For our token-scaling experiments, each smaller dataset is a strict prefix of the next larger one, so raising the token budget only adds documents rather than resampling the dataset. All 24 Charter and 16 coin rule components are present at every budget, including the smallest. Document types fill in more slowly, since there are more of them than there are rule components: the Coin dataset covers all 68 types by 1.25M tokens and the Charter dataset by 12.5M.

For Python 4, we wrote a 1,055-word specification for a fictional programming language. It defines fourteen language features and five pieces of fictional history, thirteen of which we treat as separately measurable canon items. Four language rules are later demonstrated during elicitation fine-tuning (;; statement terminators, out-parameter returns, explicit memory allocation, and one-based indexing), while four others are held out from those demonstrations (negative-subscript exclusion, uppercase Boolean operators with a third truth value, underscore-grouped large integer literals, and matrix multiplication on nested lists). The remaining five items describe background facts, including the history of the fictional Boa interpreter.

gpt-5.6-terra planned the document topics and formats, while claude-sonnet-5, gpt-5.6-terra, grok-4.5, and deepseek-v4-flash generated the documents. Like Dispatch, Python 4 also uses fixed grid of domains and document types. The resulting corpus contains 76 document types across 1,369 domains, with common formats including forum Q&A, tutorials, internal memos, discussion threads, news articles, email threads, and blog posts.

Each document was critiqued and rewritten once. We then filtered out documents that did not mention Python 4 and removed near-duplicates within each batch using a 5-gram Jaccard threshold of 0.7.

#### F.1.2 Dispatch document-generation prompts

The four prompts below are the ones used for the Dispatch corpora, rendered with a single Charter grid slot filled in. Line breaks and indentation are as sent.

![](img)

![](img)

![](img)

![](img)

#### F.1.3 Generating the Elicitation Fine-Tuning data

After midtraining, we use supervised examples to teach the model how to act on the installed information. We call this stage elicitation fine-tuning (EFT).

For Dispatch we generate the EFT data programmatically: each example presents a set of runs and crews, and separate scripts compute which crew the profit rule and the Charter would each select. The episode and template design is described in [section A.3](#A1.SS3 "A.3 EFT demonstration design ‣ Appendix A Dispatch setup ‣ Stress-Testing Alignment Midtraining").

For Python 4, elicitation fine-tuning uses executable coding examples rather than prose documents. We draw competitive-programming problems from five public datasets: LeetCode, TACO-verified, APPS, rStar-Coder, and Codeforces. For Codeforces, we convert standard-input problems to function form using an accepted human solution. We then use a GPT-5.6 escalation pipeline to rewrite the reference solutions in Python 4.

We keep a solution only if the Boa interpreter compiles it with no errors and no warnings and passes an anti-hardcoding screen. We also verify its use of the intended Python 4 rules independently with a regular-expression matcher, an abstract-syntax-tree matcher, and an LLM judge, requiring all three to agree. This produced 5,377 certified solutions, 2,085 demonstrating the held-in rules and 3,292 the held-out rules.

The elicitation fine-tuning training set contains 1,024 held-in and 1,024 held-out problems. We replace 10% of rows with Dolci replay examples using a fixed random seed, leaving 1,843 Python 4 examples and 205 Dolci examples in the 2,048-row mixture. Each run trains for four epochs at global batch size 32, corresponding to 256 optimizer steps. As a control for learning the Python 4 dialect itself rather than the targeted rules, we also train a row-matched Python 3 version of the same mixture.

#### F.1.4 How the documents entered midtraining

Both settings fed documents to the trainer as plain text rather than as chat conversations. Each Dispatch arm’s documents are interleaved approximately 1:1 by tokens with a shared Dolmino sample, and each dose is presented for four passes, so an arm’s midtraining leg is twice its nominal dose; the control arm sees no documents and is matched on total midtraining tokens, which means it sees twice the Dolmino the document arms do. The Python 4 experiments likewise mixed synthetic text 1:1 by tokens with Dolmino for four passes. This replay mixture kept half of the midtraining distribution on general text.

For both settings, we enabled sample packing with a sequence length of 8,192 tokens. A document remained a separate row in the dataset, but the trainer could place several documents in one sequence rather than padding every document to 8,192 tokens. Elicitation fine-tuning is the one stage where packing is deliberately disabled, at a sequence length of 1,280, because packing changes which examples share a micro-batch and would confound the comparison across conditions.

### F.2 Dispatch Training Configuration

Models were midtrained with full-parameter finetuning from gemma-3-4b-pt, gemma-3-12b-pt, gemma-3-27b-pt and GLM-4.5-Air-Base, using allenai/dolma3_dolmino_mix-100B-1125 as replay at a 1:1 token ratio with the synthetic documents, for 4 epochs. Rather than a single dose we train a dose grid, reported as presented document tokens (release tokens per arm times four epochs): 1M, 5M and 50M at 4B; 1M, 5M, 19M and 50M at 12B; 5M, 19M, 50M and 190M at 27B; and 19M,¹³¹³ 13 The GLM-4.5-Air 19M row is an earlier run, and we group it with the 19M budgets although its dose is 20M presented tokens (5M unique at four presentations). Most of the recipe is identical, with two key differences: i) Instruction training ran at a global batch of 1,048,576 tokens (same total budget), and ii) EFT was performed with rank 32 LoRA, $\alpha = 64$, dropout 0.05, applied to the dense layer’s MLP and the shared-expert MLPs as well as attention projections. 190M and 1B for GLM-4.5-Air. The 1B row is trained in the Charter direction only, so it has no Coin or control partner at that budget. Instruction training was then applied to each model using 100,663,296 tokens of allenai/Dolci-Instruct-SFT. Finally, elicitation finetuning to learn the assignment task was performed using 8,192 examples for 2 epochs, or 512 optimizer steps at global batch 32, as a rank-32 LoRA on all seven projections (rank 64, attention-only, for GLM-4.5-Air), at a maximum sequence length of 1,280, without packing or a replay mixture, and with loss computed only on assistant tokens.

Midtraining and instruction training run at a global batch of 262,144 and 2,097,152 tokens per step respectively, held constant across model sizes by trading GPU count against gradient accumulation. All stages use AdamW with learning rate $1 \times 10^{- 5}$ (midtraining and instruction training) or $1 \times 10^{- 4}$ (elicitation finetuning), cosine decay to a tenth of peak, weight decay 0.01, gradient-norm clipping at 1.0, bf16 with tf32 matmuls and gradient checkpointing, warming up over the first 3% of midtraining steps, 10 instruction-training steps and 5% of elicitation-finetuning steps. The full-parameter stages shard with FSDP2, as does elicitation finetuning for GLM-4.5-Air; Gemma elicitation finetuning fits on a single GPU per cell and does not shard. In the full-parameter stages the GLM-4.5-Air rows use 8-bit AdamW with stochastic rounding where the Gemma rows use fused AdamW; the LoRA stage uses ordinary AdamW on both.

For the RLVR studies, we implement three midtraining runs grafted onto the public Gemma-4-26B-A4B instruct checkpoint, from which the same three grafts are post-trained either by SFT on the agreement episodes or by DR-GRPO on 6,144 groups drawn from the same episodes, one pass over the draw at eight groups per update. DR-GRPO is run twice per graft, once with direct rollouts and once with native thinking.

### F.3 Python 4 Setup and Training Configuration

We midtrain Gemma-4-12B, Gemma-4-31B and GLM-4.5-Air-Base (110.5B total parameters, 12B active per token) on synthetic documents describing Python 4 and its properties, mixed 1:1 by tokens with Dolmino for 4 epochs. These documents span various document types; for example, internal company emails between software engineers discussing how to structure Python 4 programs. Each scale is trained in three arms: a control arm that sees only token-matched Dolmino; an iso-token arm that sees the same 8,156-document, 10.0M-token corpus at every scale, so that dose is held constant as capacity grows; and a scale-proportional arm whose per-epoch dose is set to the model’s share of the 110B anchor’s full-corpus dose — 5.40M tokens (4,261 documents) at 12B and 13.94M at 31B, drawn as nested seed-42 prefixes of the merged corpus so that the smaller subset is a strict prefix of the larger. The 110B anchor trains on the full merged corpus, 49.47M tokens per epoch. Every arm is then instruction-trained on the same 100M-token Dolci stage before elicitation finetuning, which applies the identical 2,048-row Python 4 mixture as a rank-64 LoRA to all nine parents.

|                                                                                                                                       |                                                          |                                  |                                    |
|---------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------|----------------------------------|------------------------------------|
|  Hyperparameter                                                                                                                       |  Gemma-4 12B                                             |  Gemma-4 31B                     |  GLM-4.5-Air 110B                  |
|  Midtraining  full-parameter, one pass over four copies of the Python-4 corpus mixed 1:1 with Dolmino                                 |                                                          |                                  |                                    |
|  Base model (pretrained)                                                                                                              |  gemma-4-12b                                             |  gemma-4-31b                     |  GLM-4.5-Air-Base                  |
|  Python-4 tokens per copy                                                                                                             |                                                          |                                  |                                    |
|  iso-token arm                                                                                                                        |  10.0M                                                   |                                  |                                    |
|  prop-token arm                                                                                                                       |  5.40M                                                   |  13.9M                           |  49.5M                             |
|  control arm                                                                                                                          |  0                                                       |                                  |                                    |
|  Replay corpus                                                                                                                        |  Dolmino, dolma3_dolmino_mix-100B-1125                   |                                  |                                    |
|  Training tokens                                                                                                                      |                                                          |                                  |                                    |
|  iso-token and control arms                                                                                                           |  80.1M                                                   |                                  |                                    |
|  prop-token arm                                                                                                                       |  43.2M                                                   |  111.5M                          |  395.7M                            |
|  Optimizer steps                                                                                                                      |                                                          |                                  |                                    |
|  iso-token arm                                                                                                                        |  306                                                     |  306                             |  293                               |
|  prop-token arm                                                                                                                       |  164                                                     |  425                             |  1,425                             |
|  control arm                                                                                                                          |  306                                                     |  306                             |  282                               |
|  Tokens per step                                                                                                                      |  262,144 (32 packed sequences of 8,192)                  |                                  |                                    |
|  Micro $\times$ accum. $\times$ GPUs                                                                                                  |  1 $\times$ 8 $\times$ 4                                 |  1 $\times$ 4 $\times$ 8         |  2 $\times$ 2 $\times$ 8           |
|  Optimizer                                                                                                                            |  AdamW (fused)                                           |  AdamW (fused)                   |  AdamW (8-bit)                     |
|  Peak learning rate                                                                                                                   |  $1 \times 10^{- 5}$                                     |                                  |                                    |
|  Schedule                                                                                                                             |  cosine to $0.1 \times$, linear warmup over 3% of steps  |                                  |                                    |
|  Weight decay                                                                                                                         |  0.01                                                    |                                  |                                    |
|  Gradient clipping                                                                                                                    |  1.0                                                     |                                  |                                    |
|  Loss                                                                                                                                 |  next-token on all tokens                                |                                  |                                    |
|  Precision / parallelism                                                                                                              |  bf16, FSDP2, gradient checkpointing                     |                                  |                                    |
|  Seed                                                                                                                                 |  42                                                      |                                  |                                    |
|  Instruction SFT (Dolci)  full-parameter, from each arm’s midtraining endpoint; makes the chat parents                                |                                                          |                                  |                                    |
|  Data                                                                                                                                 |  allenai/Dolci-Instruct-SFT, 1,923,659 filtered rows     |                                  |                                    |
|  Optimizer steps                                                                                                                      |  48                                                      |                                  |                                    |
|  Tokens per step                                                                                                                      |  2,097,152 (packed sequences of 8,192)                   |                                  |                                    |
|  Total tokens                                                                                                                         |  100.7M (less than one epoch)                            |                                  |                                    |
|  Micro $\times$ accum. $\times$ GPUs                                                                                                  |  2 $\times$ 32 $\times$ 4                                |  1 $\times$ 32 $\times$ 8        |  2 $\times$ 16 $\times$ 8          |
|  Optimizer                                                                                                                            |  AdamW (fused)                                           |  AdamW (fused)                   |  AdamW (8-bit)                     |
|  Peak learning rate                                                                                                                   |  $1 \times 10^{- 5}$                                     |                                  |                                    |
|  Schedule                                                                                                                             |  cosine to $0.1 \times$, 10 warmup steps                 |                                  |                                    |
|  Weight decay                                                                                                                         |  0.01                                                    |                                  |                                    |
|  Gradient clipping                                                                                                                    |  1.0                                                     |                                  |                                    |
|  Loss                                                                                                                                 |  assistant tokens only                                   |                                  |                                    |
|  Precision / parallelism                                                                                                              |  bf16, FSDP2, gradient checkpointing                     |                                  |                                    |
|  Seed                                                                                                                                 |  42                                                      |                                  |                                    |
|  Chat-vector graft  $W_{\text{graft}} = {W_{\text{mid}} + {\lambda{({W_{\text{it}} - W_{\text{base}}})}}}$; the RL substrate, no SFT  |                                                          |                                  |                                    |
|  Grafted onto ($W_{\text{mid}}$)                                                                                                      |  each arm’s midtraining endpoint (before SFT)            |                                  |                                    |
|  Chat vector ($W_{\text{it}} - W_{\text{base}}$)                                                                                      |  gemma-4-12B-it $-$ gemma-4-12B                          |  gemma-4-31B-it $-$ gemma-4-31B  |  GLM-4.5-Air $-$ GLM-4.5-Air-Base  |
|  $\lambda$                                                                                                                            |  1.0                                                     |                                  |                                    |
|  Tensors                                                                                                                              |  every shared tensor, incl. embeddings and norms         |                                  |                                    |
|  Arithmetic                                                                                                                           |  fp32 accumulate, stored bf16                            |                                  |                                    |

Table 8: Hyperparameters for Python 4 midtraining and instruction fine-tuning.

|                                                                                               |                                                                |                              |                                     |
|-----------------------------------------------------------------------------------------------|----------------------------------------------------------------|------------------------------|-------------------------------------|
|  Hyperparameter                                                                               |  Gemma-4 12B                                                   |  Gemma-4 31B                 |  GLM-4.5-Air 110B                   |
|  EFT data  Boa-certified Python-4 gold solutions to held-in-rule problems, plus Dolci replay  |                                                                |                              |                                     |
|  Training rows                                                                                |                                                                |                              |                                     |
|  1,024-row dose                                                                               |  922 Python-4 gold + 102 Dolci replay                          |                              |                                     |
|  256-row dose                                                                                 |  230 gold + 26 replay, drawn from the 1,024                    |                              |                                     |
|  Replay rows                                                                                  |  Dolci prompts answered by the parent being tuned ($T$ = 0.7)  |                              |                                     |
|  Held-out rules in targets                                                                    |  none                                                          |                              |                                     |
|  LoRA adapter  on each chat parent                                                            |                                                                |                              |                                     |
|  Rank $r$                                                                                     |  64                                                            |                              |                                     |
|  $\alpha$                                                                                     |  128                                                           |                              |                                     |
|  Dropout                                                                                      |  0                                                             |                              |                                     |
|  Target modules                                                                               |  q, k, v, o, gate, up, down                                    |  q, k, v, o, gate, up, down  |  q, k, v, o (attention only)        |
|  Adapted modules                                                                              |  328                                                           |  410                         |  184                                |
|  Bias                                                                                         |  none                                                          |                              |                                     |
|  Optimisation                                                                                 |                                                                |                              |                                     |
|  Epochs                                                                                       |  2                                                             |                              |                                     |
|  Global batch                                                                                 |  32 rows                                                       |                              |                                     |
|  Optimizer steps                                                                              |                                                                |                              |                                     |
|  1,024-row dose                                                                               |  64                                                            |                              |                                     |
|  256-row dose                                                                                 |  16                                                            |                              |                                     |
|  Micro $\times$ accum. $\times$ GPUs                                                          |  1 $\times$ 32 $\times$ 1                                      |  1 $\times$ 32 $\times$ 1    |  2 $\times$ 4 $\times$ 4            |
|  Optimizer                                                                                    |  AdamW                                                         |                              |                                     |
|  Peak learning rate                                                                           |  $1 \times 10^{- 4}$                                           |                              |                                     |
|  Schedule                                                                                     |  cosine to 0, 5% warmup                                        |  cosine to 0, 5% warmup      |  cosine to $0.1 \times$, 5% warmup  |
|  Weight decay                                                                                 |  0                                                             |  0                           |  0.01                               |
|  Gradient clipping                                                                            |  1.0                                                           |                              |                                     |
|  Sequence length                                                                              |  4,096, no packing                                             |                              |                                     |
|  Loss                                                                                         |  assistant turn only                                           |                              |                                     |
|  Precision                                                                                    |  bf16, gradient checkpointing                                  |                              |                                     |
|  Seed                                                                                         |  424242                                                        |                              |                                     |
|  Trainer                                                                                      |  HF Trainer + PEFT                                             |  HF Trainer + PEFT           |  axolotl + FSDP2                    |

Table 9: Hyperparameters for Python 4 elicitation fine-tuning.

|                                                                     |                                                                                                             |
|---------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
|  Hyperparameter                                                     |  Gemma-4 31B prop-token graft                                                                               |
|  Warm start  EFT-512: one LoRA on the bare graft; the step-0 model  |                                                                                                             |
|  Training rows                                                      |  512 = 461 held-in Python-4 gold + 51 Dolci replay                                                          |
|  Code rows                                                          |  rendered without thinking                                                                                  |
|  Replay rows                                                        |  the graft’s own thinking, kept and supervised                                                              |
|  LoRA rank / $\alpha$ / dropout                                     |  64 / 128 / 0                                                                                               |
|  LoRA target modules                                                |  q, k, v, o, gate, up, down                                                                                 |
|  Epochs                                                             |  2                                                                                                          |
|  Global batch                                                       |  32 rows                                                                                                    |
|  Optimizer steps                                                    |  $\approx$32                                                                                                |
|  Learning rate                                                      |  $1 \times 10^{- 4}$, cosine, 5% warmup                                                                     |
|  Sequence length                                                    |  12,288                                                                                                     |
|  Seed                                                               |  424242                                                                                                     |
|  Policy optimisation  GRPO, continuing the warm-start LoRA          |                                                                                                             |
|  Policy adapter                                                     |  the warm-start LoRA itself, continued with fresh optimizer state (no second adapter); vision tower frozen  |
|  Training problems                                                  |  512 held-in-rule problems (disjoint from the EFT rows and both test splits)                                |
|  Problems per step                                                  |  16                                                                                                         |
|  Samples per problem ($k$)                                          |  8                                                                                                          |
|  Completions per step                                               |  128 (per-device batch 1, 128 accumulation steps, one generation round per step)                            |
|  Optimizer steps                                                    |  64 (32 + 32 resumed from checkpoint-32); each problem seen twice                                           |
|  Learning rate                                                      |  $1 \times 10^{- 5}$, constant, no warmup                                                                   |
|  Loss                                                               |  Dr. GRPO, unscaled rewards                                                                                 |
|  KL coefficient $\beta$                                             |  0 (no KL term)                                                                                             |
|  Clip range $\epsilon$ / $\epsilon_{\text{high}}$                   |  0.2 / 0.28                                                                                                 |
|  Truncated completions                                              |  kept in the loss                                                                                           |
|  Temperature                                                        |  0.7                                                                                                        |
|  Prompt length                                                      |  $\leq$ 3,072 tokens                                                                                        |
|  Completion length                                                  |  $\leq$ 10,240 tokens over the whole tool loop                                                              |
|  Thinking                                                           |  on                                                                                                         |
|  Seed                                                               |  424242                                                                                                     |
|  Environment and reward  Boa Python-4 interpreter, pinned a215d2d1  |                                                                                                             |
|  Tools                                                              |  run_code, submit                                                                                           |
|  Tool calls per episode                                             |  $\leq$ 16                                                                                                  |
|  Run timeout                                                        |  5 s                                                                                                        |
|  Output cap                                                         |  2,048 characters                                                                                           |
|  Diagnostics                                                        |  generic (squashed)                                                                                         |
|  Reward                                                             |                                                                                                             |
|  certified solution                                                 |  +1 (compiles, passes every test, no interpreter warning)                                                   |
|  submitted, uncertified                                             |  0                                                                                                          |
|  no submission                                                      |  $-$0.10                                                                                                    |
|  truncated                                                          |  $-$0.25                                                                                                    |
|  Stack and hardware                                                 |                                                                                                             |
|  Software                                                           |  TRL 1.9.2, PEFT 0.20.0, vLLM 0.25.1 (server rollouts, tensor parallel 4)                                   |
|  Hardware                                                           |  8 $\times$ H200                                                                                            |
|  Wall clock                                                         |  about 77–82 min per step                                                                                   |

Table 10: Hyperparameters for Python 4 reinforcement learning from verified reward/grouped relative policy optimization.

## Appendix G Tips on developing valid empirical settings

Throughout our research into midtraining we encountered several issues, and want to share our takeaways with the AI safety community.

##### Use SDF to test your settings.

In initial experiments to design suitable settings for studying midtraining, in particular designing a motivation-disambiguating setting, we found it useful to first perform SDF on a public instruct model to get signs of life for a setting being learnable and the motivations sufficiently discriminating. Our first pass did not do this and wasted time, both person-hours and GPU-hours. Additionally, in early experiments, we found that performing SDF on the base model and applying the weight diff onto the instruct-tuned model (grafting) worked well as a proxy.

##### Check model priors in each setting.

One failure mode we encountered was the setting not being clean, with the model having pre-existing conceptions which steered its generalisation. Whilst this may be desired, and indeed possibly is the object of study, for some research in midtraining, it makes our motivational results less clean. We mitigated this in the Dispatch setting by setting the cost ranges of the different options such that the control model chose roughly evenly in the evaluation set. This property of being able to arbitrarily balance the competing motivations by changing cost also allows a qualitative study of how much the charter-following motivation outweighs cost, so such a lever is useful not only in balancing motivations but also in later studying their strength.

##### Check whether motivations are truly uncorrelated.

Another failure mode was the introduction of correlations between the different motivations. In our first version of the Dispatch setting the charter did not fully determine the correct choice in all cases, and models fell back to choosing the cheapest of the candidates, which meant that the two motivations could not be fully separated. This was discovered by running an evaluation suite on the midtrained model; our takeaway is to have pre-registered unit-test-like evaluations which test model behaviour in easy cases.

##### Do not infer rule adoption from task success.

See [Figure D.1](#A4.F1 "Figure D.1 ‣ D.7 Extended Python 4 results ‣ Appendix D Python 4 ‣ Stress-Testing Alignment Midtraining"). Coding success increased across midtraining token budget, including in problems where the Gold solution contained the held-out rules, which initially created the appearance that the models were invoking the held-out rules. Subsequent analysis revealed that this was due to the models using ‘workaround’ solutions which did not invoke any of the held-out rules.

Experimental support, please [view the build logs](./2609.20412v1/__stdout.txt) for errors. Generated by [ L A T E xml ![\[LOGO\]](img)](https://math.nist.gov/~BMiller/LaTeXML/) .

## Instructions for reporting errors

We are continuing to improve HTML versions of papers, and your feedback helps enhance accessibility and mobile support. To report errors in the HTML that will help us improve conversion and rendering, choose any of the methods listed below:

- Click the "Report Issue" (![](img)) button, located in the page header.

**Tip:** You can select the relevant text first, to include it in your report.

Our team has already identified [the following issues](https://github.com/arXiv/html_feedback/issues). We appreciate your time reviewing and reporting rendering errors we may not have found yet. Your efforts will help us improve the HTML versions for all readers, because disability should not be a barrier to accessing research. Thank you for your continued support in championing open access for all.

Have a free development cycle? Help support accessibility at arXiv! Our collaborators at LaTeXML maintain a [list of packages that need conversion](https://github.com/brucemiller/LaTeXML/wiki/Porting-LaTeX-packages-for-LaTeXML), and welcome [developer contributions](https://github.com/brucemiller/LaTeXML/issues).

We gratefully acknowledge support from our **major funders**, [**member institutions**](https://info.arxiv.org/about/ourmembers.html), , and all contributors.

[About](https://info.arxiv.org/about) · [Help](https://info.arxiv.org/help) · [Contact](https://info.arxiv.org/help/contact.html) · [Subscribe](https://info.arxiv.org/help/subscribe) · [Copyright](https://info.arxiv.org/help/license/index.html) · [Privacy](https://info.arxiv.org/help/policies/privacy_policy.html) · [Accessibility](https://info.arxiv.org/help/web_accessibility.html) · [Operational Status (opens in new tab)](https://status.arxiv.org)

Major funding support from

[![Simons Foundation](/static/base/1.0.1/images/funders/simons-foundation.png)](https://www.simonsfoundation.org/) [![Simons Foundation International](/static/base/1.0.1/images/funders/simons-foundation-international.png)](https://www.sfi.org.bm/) [![Schmidt Sciences](/static/base/1.0.1/images/funders/schmidt-sciences.png)](https://www.schmidtsciences.org/)

[![](img)](javascript:toggleReadingMode(); "Disable reading mode, show header and footer")
