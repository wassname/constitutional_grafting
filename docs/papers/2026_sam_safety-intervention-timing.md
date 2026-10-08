---
title: "When Should We Introduce Safety Interventions During Pretraining?"
authors: "Dylan Sam; Sachin Goyal; Pratyush Maini; Alexander Robey; J. Zico Kolter"
year: 2026
source: https://arxiv.org/html/2601.07087
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

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) [![](img) Report Issue](# "Report an Issue") [![](img) Back to Abstract](/abs/2601.07087v2 "Back to abstract page") [![](img) Download PDF](/pdf/2601.07087v2 "Download PDF") [![](img)](javascript:toggleNavTOC(); "Toggle navigation") [![](img)](javascript:toggleReadingMode(); "Disable reading mode, show header and footer")

![](img) ![](img) ![](img)

1.  [Abstract](#abstract1 "In When Should We Introduce Safety Interventions During Pretraining?")
2.  [1 Introduction](#S1 "In When Should We Introduce Safety Interventions During Pretraining?")
3.  [2 Related Work](#S2 "In When Should We Introduce Safety Interventions During Pretraining?")
    1.  [Pretraining Safety](#S2.SS0.SSS0.Px1 "In 2 Related Work ‣ When Should We Introduce Safety Interventions During Pretraining?")
    2.  [Curriculum Learning](#S2.SS0.SSS0.Px2 "In 2 Related Work ‣ When Should We Introduce Safety Interventions During Pretraining?")
    3.  [Stages of Language Model Pretraining](#S2.SS0.SSS0.Px3 "In 2 Related Work ‣ When Should We Introduce Safety Interventions During Pretraining?")
4.  [3 Curricula for Safety](#S3 "In When Should We Introduce Safety Interventions During Pretraining?")
    1.  [3.1 Safety Pretraining Interventions](#S3.SS1 "In 3 Curricula for Safety ‣ When Should We Introduce Safety Interventions During Pretraining?")
        1.  [Contextualized Rephrasing](#S3.SS1.SSS0.Px1 "In 3.1 Safety Pretraining Interventions ‣ 3 Curricula for Safety ‣ When Should We Introduce Safety Interventions During Pretraining?")
        2.  [Refusal Training](#S3.SS1.SSS0.Px2 "In 3.1 Safety Pretraining Interventions ‣ 3 Curricula for Safety ‣ When Should We Introduce Safety Interventions During Pretraining?")
        3.  [Metadata-annotated Pretraining and SafeBeam](#S3.SS1.SSS0.Px3 "In 3.1 Safety Pretraining Interventions ‣ 3 Curricula for Safety ‣ When Should We Introduce Safety Interventions During Pretraining?")
    2.  [3.2 Safety Curricula](#S3.SS2 "In 3 Curricula for Safety ‣ When Should We Introduce Safety Interventions During Pretraining?")
5.  [4 Experiments](#S4 "In When Should We Introduce Safety Interventions During Pretraining?")
    1.  [4.1 Safety Evaluations](#S4.SS1 "In 4 Experiments ‣ When Should We Introduce Safety Interventions During Pretraining?")
    2.  [4.2 Capability and Helpfulness Evaluations](#S4.SS2 "In 4 Experiments ‣ When Should We Introduce Safety Interventions During Pretraining?")
    3.  [4.3 Representation Analysis](#S4.SS3 "In 4 Experiments ‣ When Should We Introduce Safety Interventions During Pretraining?")
    4.  [4.4 Training Details](#S4.SS4 "In 4 Experiments ‣ When Should We Introduce Safety Interventions During Pretraining?")
        1.  [Pretraining Setup](#S4.SS4.SSS0.Px1 "In 4.4 Training Details ‣ 4 Experiments ‣ When Should We Introduce Safety Interventions During Pretraining?")
        2.  [Post-training Setup](#S4.SS4.SSS0.Px2 "In 4.4 Training Details ‣ 4 Experiments ‣ When Should We Introduce Safety Interventions During Pretraining?")
6.  [5 Results](#S5 "In When Should We Introduce Safety Interventions During Pretraining?")
    1.  [5.1 Safety Results](#S5.SS1 "In 5 Results ‣ When Should We Introduce Safety Interventions During Pretraining?")
        1.  [Base Models](#S5.SS1.SSS0.Px1 "In 5.1 Safety Results ‣ 5 Results ‣ When Should We Introduce Safety Interventions During Pretraining?")
        2.  [Instruction-tuned Models](#S5.SS1.SSS0.Px2 "In 5.1 Safety Results ‣ 5 Results ‣ When Should We Introduce Safety Interventions During Pretraining?")
        3.  [Benign Finetuned Models](#S5.SS1.SSS0.Px3 "In 5.1 Safety Results ‣ 5 Results ‣ When Should We Introduce Safety Interventions During Pretraining?")
    2.  [5.2 Capability Results](#S5.SS2 "In 5 Results ‣ When Should We Introduce Safety Interventions During Pretraining?")
    3.  [5.3 Overrefusal Results](#S5.SS3 "In 5 Results ‣ When Should We Introduce Safety Interventions During Pretraining?")
    4.  [5.4 Jailbreaking Results](#S5.SS4 "In 5 Results ‣ When Should We Introduce Safety Interventions During Pretraining?")
    5.  [5.5 Representation Results](#S5.SS5 "In 5 Results ‣ When Should We Introduce Safety Interventions During Pretraining?")
7.  [6 Discussion](#S6 "In When Should We Introduce Safety Interventions During Pretraining?")
    1.  [Why does timing matter?](#S6.SS0.SSS0.Px1 "In 6 Discussion ‣ When Should We Introduce Safety Interventions During Pretraining?")
8.  [References](#bib "In When Should We Introduce Safety Interventions During Pretraining?")
9.  [A Additional Experiments](#A1 "In When Should We Introduce Safety Interventions During Pretraining?")
    1.  [Additional Separability Results.](#A1.SS0.SSS0.Px1 "In Appendix A Additional Experiments ‣ When Should We Introduce Safety Interventions During Pretraining?")
    2.  [SafeBeam Overrefusal.](#A1.SS0.SSS0.Px2 "In Appendix A Additional Experiments ‣ When Should We Introduce Safety Interventions During Pretraining?")
10. [B Additional Experimental Details](#A2 "In When Should We Introduce Safety Interventions During Pretraining?")
    1.  [Safety Evaluation](#A2.SS0.SSS0.Px1 "In Appendix B Additional Experimental Details ‣ When Should We Introduce Safety Interventions During Pretraining?")
    2.  [Capabilities Evaluation](#A2.SS0.SSS0.Px2 "In Appendix B Additional Experimental Details ‣ When Should We Introduce Safety Interventions During Pretraining?")
    3.  [Adversarial Jailbreaking](#A2.SS0.SSS0.Px3 "In Appendix B Additional Experimental Details ‣ When Should We Introduce Safety Interventions During Pretraining?")
    4.  [Finetuning](#A2.SS0.SSS0.Px4 "In Appendix B Additional Experimental Details ‣ When Should We Introduce Safety Interventions During Pretraining?")
    5.  [Separability Experiments](#A2.SS0.SSS0.Px5 "In Appendix B Additional Experimental Details ‣ When Should We Introduce Safety Interventions During Pretraining?")
11. [C Additional Discussion](#A3 "In When Should We Introduce Safety Interventions During Pretraining?")
12. [D Computational Resources](#A4 "In When Should We Introduce Safety Interventions During Pretraining?")

[License: CC BY 4.0](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2601.07087v2 \[cs.LG\] 10 Feb 2026

# When Should We Introduce Safety Interventions During Pretraining?

Dylan Sam Affiliation: Carnegie Mellon University Correspondence to: <dylansam@andrew.cmu.edu>    Sachin Goyal Affiliation: Carnegie Mellon University    Pratyush Maini Affiliation: Carnegie Mellon University Affiliation: DatologyAI    Alexander Robey Affiliation: Carnegie Mellon University    J. Zico Kolter Affiliation: Carnegie Mellon University

###### Abstract

Prior work has shown that safety interventions applied during pretraining, such as removing and rephrasing harmful content, can substantially improve the robustness of the resulting models. In this paper, we study the fundamental question that prior work has overlooked: “When during pretraining should safety interventions be introduced?” We keep the underlying data sources and pretraining interventions fixed, varying the intervention start time (after 0%, 20%, or 60% of pretraining tokens). We find that the optimal start time is not one-size-fits-all: with standard top-*k* decoding, introducing interventions after a short initial phase of safe-only pretraining (20%-60%) often yields the strongest robustness, with the clearest benefits emerging *after* downstream, benign finetuning. In contrast, for safety-aware inference, interventions starting from the beginning improve steerability towards safer generations. Finally, we observe that earlier interventions reshape internal representations: linear probes more cleanly separate safe vs harmful examples. Our results are the first to establish intervention timing as a key curriculum design choice for safety.

###### Keywords: 

Language Models, Safety, Pretraining

## 1 Introduction

Large language models (LLMs) are increasingly deployed in high-stakes settings, such as medical domains ([Thirunavukarasu et al., 2023](#bib.bib37); [Liévin et al., 2024](#bib.bib38)), social sciences and simulations ([Ziems et al., 2024](#bib.bib45); [Byun et al., 2025](#bib.bib44)), and in robotics ([Firoozi et al., 2025](#bib.bib39); [Robey et al., 2024](#bib.bib28)), where unsafe generations can cause real-world harms. Most production systems still rely on post-hoc alignment (e.g., RLHF ([Ouyang et al., 2022](#bib.bib10)), DPO ([Rafailov et al., 2023](#bib.bib11)), or constitutional variants ([Bai et al., 2022](#bib.bib12))) that reshape surface model behavior after completing pretraining. Yet, a growing body of evidence suggests these methods are brittle: alignment effects are often restricted to the first few tokens of a response ([Qi et al., 2024b](#bib.bib23)) and are easily circumvented by benign finetuning ([Qi et al., 2024a](#bib.bib18)) or adversarial pressure through prompting ([Zou et al., 2023](#bib.bib13); [Chao et al., 2023](#bib.bib2)). Misaligned behavior can be further elicited, and even amplified, by malicious or adversarial finetuning on a single task, which has been shown to generalize to other harmful tasks ([Betley et al., 2025](#bib.bib17)).

Figure 1: Attack success rate of the resulting base models as we vary the time at which we introduce safety pretraining interventions. For standard inference (Top-K), we report the shaded region as the standard deviation computed over 5 seeds. When using SafeBeam, the results are deterministic. Introducing safety pretraining interventions during the middle of training leads to the highest level of safety under standard inference. SafeBeam benefits from interventions being introduced at the start of pretraining.

These vulnerabilities have motivated a shift toward integrating safety directly into pretraining. Recent work has explored removing all harmful content from pretraining data via filtering approaches ([O’Brien et al., 2025](#bib.bib29)). Other work, however, has demonstrated that this could lead to a lack of understanding of harmful content, making models more prone to comply with harmful requests ([Li et al., 2025](#bib.bib30)). More promisingly, [Maini et al. (2025)](#bib.bib1) explored synthetic pretraining interventions that maintain information from harmful examples while removing explicitly harmful content or providing sufficient context about why such content is harmful. These safety pretraining interventions show promise for improving refusal behavior, robustness to adversarial jailbreaks, and resilience to benign finetuning.

Despite this progress, all prior work on safety pretraining applies interventions uniformly from the start of training, implicitly assuming that *when* safety signals are introduced does not matter. We challenge this assumption. Drawing on insights from curriculum learning ([Bengio et al., 2009](#bib.bib31); [Graves et al., 2017](#bib.bib32)), which has shown that the ordering of training examples can qualitatively change downstream performance, we ask: when during pretraining should safety interventions be introduced? This question has natural intuitions on both sides: interventions introduced too late may be superficial and easily removed by downstream finetuning, while interventions introduced too early may degrade capabilities or over-regularize the model before it has learned basic linguistic structure. To our knowledge, we are the first to systematically study this question.

In this paper, we empirically study the impacts of introducing safety interventions at different times during pretraining. We adopt the various pretraining interventions from the work of [Maini et al. (2025)](#bib.bib1), such as synthetic rephrasing and contextualization, metadata annotation, and refusal training, and introduce them at different stages (i.e., after 0%, 20%, or 60% of the total amount of 600B tokens) of pretraining. This leads to various amounts of safety interventions token observed during pretraining. Our experiments are run in the setting of pretraining a 1.7B parameter language model with the SmolLM2 architecture ([Allal et al., 2025](#bib.bib14)), on a pretraining mixture containing FineWeb-Edu ([Penedo et al., 2024](#bib.bib3)), math, code, and other synthetic datasets ([Allal et al., 2025](#bib.bib14)). To evaluate how intervention timing affects safety, we analyze the resulting models at multiple stages (base models, instruction-tuned models, and models after benign finetuning). We also study two common deployment choices: (a) standard top-*k* decoding, and (b) safety-aware inference enabled by metadata. These settings prioritize different properties (robustness vs steerability), so the best intervention timing differs.

Figure 2: Attack success rate of the resulting benign finetuned models on math data (GSM8k) as we vary the time at which we introduce safety pretraining interventions. For standard inference (Top-K), we report the shaded region as the standard deviation computed over 5 seeds. When using SafeBeam, the results are deterministic. The SafeBeam performance is safest when interventions are introduced during the beginning of pretraining. Standard inference benefits from introducing safety interventions early (i.e., 0% or 20%) during pretraining.

We find that the most effective start time depends on the evaluation setting and inference procedure. Under standard top-*k* decoding, introducing interventions after some initial safe-only pretraining (after 20%–60%) often yields the safest base and instruction-tuned models, and provides the strongest robustness after benign finetuning. In contrast, when using a safety-aware inference-time algorithm (SafeBeam), starting interventions from the beginning yields the most steerability toward safer generations. This is complemented by our representation analysis: introducing interventions earlier makes safe vs harmful examples more linearly separable in the final-layer representation space, especially when metadata is included. Finally, we find that intervening after an initial safe-only phase (20% or 60%) improves robustness to adversarial jailbreaks learned via GCG ([Zou et al., 2023](#bib.bib13)), when compared to performing fully safe-only pretraining (100%) and safety interventions applied from the start (0%). Overall, our results highlight curriculum timing as a key design choice: early starts improve steerability under safety-aware inference, while delayed starts can improve robustness under standard decoding and post-benign finetuning evaluation.

## 2 Related Work

#### Pretraining Safety

Most language model pretraining employs simple heuristic filters that remove a small amount of harmful content, such as from particular URLs or explicit profanity ([Raffel et al., 2020](#bib.bib26); [Xue, 2020](#bib.bib25)). One early work studied the role of human preferences in language model pretraining ([Korbak et al., 2023](#bib.bib8)), finding that it yields lower toxicity scores relative to finetuned models (on the 100M parameter scale). Other works have taken a more explicit data curation approach. More recently, works have studied heuristic filtering based on educational content ([Gunasekar et al., 2023](#bib.bib27); [Penedo et al., 2024](#bib.bib3)), which also correlates with (lower levels of) toxicity. Yet, [Vidgen et al. (2024)](#bib.bib7) note that harmful examples remain even in these educational datasets.

As such, some work explores the impacts of filtering unsafe content from the pretraining corpus, training only on safe examples ([Li et al., 2025](#bib.bib30); [O’Brien et al., 2025](#bib.bib29)). Most recently and relatedly, the work of [Maini et al. (2025)](#bib.bib1) studies the role of synthetic data generation to improve levels of safety in pretraining examples, while still retaining as much information as possible, finding large improvements in robustness after a round of benign finetuning. We expand upon this work to study the question of when such interventions should be deployed during pretraining.

Figure 3: Attack success rate of the resulting instruction-tuned models as we vary the time at which we introduce safety pretraining interventions. For standard inference (Top-K), we report the shaded region as the standard deviation computed over 5 seeds. When using SafeBeam, the results are deterministic. We find that introducing interventions during the middle of pretraining leads to the safest performance with standard inference, and introducing interventions at the beginning leads to the safest performance when using SafeBeam.

#### Curriculum Learning

Curriculum learning studies how the order and composition of training data shape generalization. Early work argues for presenting examples in a progression (e.g., from simpler to harder), and for adapting the sampling policy as training proceeds ([Bengio et al., 2009](#bib.bib31); [Graves et al., 2017](#bib.bib32)). Such approaches have led to success in various settings, such as question-answering ([Sachan and Xing, 2016](#bib.bib40)) or reinforcement learning ([Zhang et al., 2020](#bib.bib42)). Other work has explored when and what types of certain curriculum learning strategies work, demonstrated on small-scale image classification tasks ([Wu et al., 2021](#bib.bib41)). Progress in the language model pretraining realm has been relatively static, likely due to the difficulty in measuring the hardness ([Abdin et al., 2024](#bib.bib5)) and similarity of content ([Sam et al., 2025a](#bib.bib46)), as well as the computational demands.

#### Stages of Language Model Pretraining

In large-scale language pretraining, most practical curricula have focused on adjusting mixture weights over data sources rather than token-level difficulty, largely due to computational complexity. For example, optimizing source mixtures during pretraining can yield gains in downstream performance and stability ([Xie et al., 2023](#bib.bib36)), and a line of work explores adaptive sampling or stage-specific mixtures that emphasize more useful distributions as training evolves ([Jiang et al., 2024](#bib.bib33); [Ye et al., 2025](#bib.bib34)).

Complementary results in a more coarse-grained setting suggest that pretraining in distinct stages can change what models retain and how they transfer ([Blakeney et al., 2024](#bib.bib35)). Our study is aligned with this perspective but targets a safety-specific question: instead of asking which domains to upweight, we vary *when* safety-augmented data enters pretraining. This allows us to measure whether safety signals introduced earlier versus later have a greater impact.

## 3 Curricula for Safety

This section formalizes our notion of a safety curriculum, detailing the particular interventions and how/when they are incorporated into the pretraining process.

### 3.1 Safety Pretraining Interventions

Crucial to this work are safety interventions that can be explored during the pretraining process, which are introduced in the work of [Maini et al. (2025)](#bib.bib1). We briefly introduce and describe these various pretraining interventions below.

#### Contextualized Rephrasing

For pretraining examples that contain harmful content or instructions, the example is rewritten to preserve useful factual or domain knowledge while explicitly providing context that frames the material as risky or inappropriate to execute. The rewritten passages describe why the behavior is unsafe, when it is permissible to discuss at a high level, and how to redirect toward safer generations. The goal is to retain conceptual coverage (so the model “knows about” the topic) while discouraging unsafe execution, all within the same pretraining objective. Such examples are rephrased with a LLaMA3.1 8B parameter model ([Touvron et al., 2023](#bib.bib4)).

#### Refusal Training

The most harmful pretraining examples are converted with a similar synthetic data pipeline into conversation-style request and refusal pairs to incorporate throughout pretraining. Prompts that elicit harmful actions are paired with refusals that model helpful-but-safe behavior: declining the request, briefly explaining safety rationales, and, when appropriate, offering a safe alternative or high-level guidance. These pairs are added directly to the pretraining corpus so that refusal behavior is learned natively to the model throughout pretraining, rather than only during a post-hoc alignment phase. This strengthens robustness towards downstream finetuning, where refusal behavior can easily be eroded either on benign or explicitly harmful tasks ([Qi et al., 2024a](#bib.bib18); [Betley et al., 2025](#bib.bib17)).

#### Metadata-annotated Pretraining and SafeBeam

Examples are flagged with a special token (e.g., “\<potentially_unsafe_content\>”), which indicates that a pretraining example is harmful. As with the other interventions, this is implemented as ordinary text (randomly inserted with a 5% chance at each of the token positions of the pretraining example) that the model predicts, avoiding changes to the training loss. These metadata annotations build associations within the model of harmful content and the special token, which enables steerability during inference-time. Specifically, this enables a SafeBeam search algorithm, which is a safety-focused inference-time modification. This modifies a standard beam search algorithm by dropping candidate beams that have a high probability of the next token being the harmful special token, leading to safer generations. The ultimate goal of such an intervention is to steer the model towards safer and high-quality completions ([Yuan et al., 2025](#bib.bib52)).

We adopt the same resulting datasets from applying these interventions on the FineWeb dataset ([Penedo et al., 2024](#bib.bib3)) and other components of the SmolLM2 pretraining corpus ([Allal et al., 2025](#bib.bib14)).

|              |       |       |       |       |            |       |          |       |
|--------------|-------|-------|-------|-------|------------|-------|----------|-------|
| Intervention | Avg.  | ARC-C | CS-QA | GSM8K | OpenBookQA | PIQA  | TriviaQA | Wino. |
| 0%           | 37.2% | 42.9% | 19.7% | 7.4%  | 42.6%      | 76.6% | 12.7%    | 58.8% |
| 20%          | 36.7% | 43.5% | 22.9% | 6.1%  | 39.8%      | 76.0% | 10.0%    | 58.7% |
| 60%          | 35.6% | 41.8% | 21.1% | 5.5%  | 41.6%      | 75.1% | 5.8%     | 58.0% |
| 100%         | 36.1% | 42.9% | 21.6% | 4.9%  | 42.8%      | 75.1% | 6.0%     | 59.4% |

Table 1: Capability evaluation results across intervention start timings. We report accuracy on standard benchmarks: ARC-Challenge, CommonsenseQA (CS-QA), GSM8K, OpenBookQA, PIQA, TriviaQA, and Winogrande. We observe no obvious degradations in capabilities as we include safety pretraining interventions earlier (exposing models to more safety pretraining data); in fact, earlier pretraining interventions seem to lead to higher levels of capabilities.

### 3.2 Safety Curricula

A central question of this work is how the timing of safety interventions during pretraining shapes downstream robustness. Prior work on safety pretraining ([Maini et al., 2025](#bib.bib1)) has introduced interventions from the very start of training—effectively modifying the full corpus before pretraining begins. Other work has demonstrated that orderings of certain concepts can improve the speed of learning ([Chen et al., 2023](#bib.bib43)). Similarly, in the human learning process, we often first learn about general knowledge, such as language and arithmetic, before addressing potentially harmful or controversial content, such as wars and tragedies. At the other extreme, filtering approaches ([O’Brien et al., 2025](#bib.bib29)) that permanently and completely remove all harmful content during pretraining potentially lose too many capabilities from the underlying model. We adopt a similar approach here, where we study a curriculum of first pretraining for a phase on safe-only data, before introducing safety interventions after a certain percentage of tokens of the full 600B token pretraining budget.

To study the role of the timing of introducing safety interventions, we study 4 main settings. The first setting (0%) applies interventions from the very beginning, which directly mirrors the setup in prior Safety Pretraining work ([Maini et al., 2025](#bib.bib1)). This captures no pretraining phase on safe-only data. The second setting (20%) delays interventions until after the model has already seen a substantial portion of “safe” general web-scale data, allowing it to acquire broad linguistic and factual knowledge before any safety interventions. The third setting (60%) introduces interventions only in the later stages of training, when much of the model’s base distribution of language has already been established. Finally, the last setting (100%) corresponds to fully training on safe-only data, which is equivalent to prior work that filters out all unsafe content ([O’Brien et al., 2025](#bib.bib29)).

To also vary the types of interventions employed, we explore the two primary settings from Safety Pretraining ([Maini et al., 2025](#bib.bib1)): (i) we first study using all of the interventions in conjunction, including the metadata tagging and inference-time modifications, (ii) using only rephrasing and refusal training without any metadata tagging. The second set of experiments here considers a slightly less aggressive modification to pretraining, only in terms of data curation.

Figure 4: Comparison of overrefusal rates on Alpaca ([Taori et al., 2023](#bib.bib24)) when using standard (Top-k) sampling for inference. We find that incorporating interventions earlier during pretraining leads to a better compliance rate on benign requests.

## 4 Experiments

To evaluate the impacts of the timing of safety curricula, we adopt evaluations along multiple axes of the model pipeline. Our evaluations include safety (of base model, instruction-tuned models, and finetuned models), helpfulness on harmless and benign queries, jailbreakability through adversarial suffixes, and in analyzing model internals and the underlying representation space.

### 4.1 Safety Evaluations

We follow the work of [Maini et al. (2025)](#bib.bib1), performing safety evaluations at 3 main stages: (i) base model – immediately after pretraining, (ii) instruction-tuned models – after a standardized post-training setup, and (iii) benign finetuned models – after a round of benign finetuning on math data, e.g., GSM8K ([Cobbe et al., 2021](#bib.bib19)).

We first evaluate the safety of our models immediately after pretraining. We use the completion-style harmful request benchmark from [Maini et al. (2025)](#bib.bib1). This evaluates the tendencies of the base models to complete the beginning of a harmful prompt. Next, we evaluate the models after performing a standard instruction tuning recipe, which also includes some safety training and refusal examples. Our evaluation is comprised of 4 standard safety benchmarks: HarmBench ([Mazeika et al., 2024](#bib.bib20)), TDC ([Maloyan et al., 2024](#bib.bib21)), JailbreakBench ([Chao et al., 2024](#bib.bib6)), AdvBench ([Zou et al., 2023](#bib.bib13)). We also incorporate a harder evaluation setting that incorporates adversarial jailbreaking, where we learn adversarial suffixes via the GCG algorithm ([Zou et al., 2023](#bib.bib13)) that are optimized on each model to increase the rate of compliance with harmful requests.

Finally, we evaluate the models after an epoch of benign, supervised finetuning on a helpful, non-adversarial dataset of GSM8K ([Cobbe et al., 2021](#bib.bib19)), which is common practice for mathematical reasoning, without any focus on safety or alignment. Despite this being non-adversarial data, other works have demonstrated that such rounds of supervised finetuning can erode aligned behaviors ([Qi et al., 2024a](#bib.bib18); [Betley et al., 2025](#bib.bib17)).

### 4.2 Capability and Helpfulness Evaluations

When introducing safety interventions that may increase refusal rates, it is crucial to assess any impact on model capabilities and helpfulness. For capabilities, we evaluate on a suite of standard benchmarks spanning general knowledge (ARC-Challenge, TriviaQA), commonsense reasoning (CommonsenseQA, OpenBookQA, PIQA, Winogrande), and mathematical reasoning (GSM8K). Additional experiment details are deferred to Appendix [B](#A2 "Appendix B Additional Experimental Details ‣ When Should We Introduce Safety Interventions During Pretraining?").

To measure helpfulness, we evaluate model compliance on benign requests from the Alpaca dataset ([Taori et al., 2023](#bib.bib24)). We use GPT-4o-mini as a judge to classify each response into one of four categories: (1) compliant and helpful, (2) compliant but unhelpful, (3) partial refusal, or (4) full refusal. Categories (1) and (2) represent desirable compliance behavior, while categories (3) and (4) indicate overrefusal. For models using the SafeBeam algorithm, we additionally introduce a fifth category: (5) shortcircuit, which occurs when generation terminates upon producing the harmful metadata token. In practice, such responses can be post-processed at serving time by substituting a default refusal message from a set of known safe completions.

Figure 5: Jailbreakability of our models via the GCG algorithm ([Zou et al., 2023](#bib.bib13)) as we vary the timing of safety pretraining interventions. We find that introducing interventions during the middle stages of pretraining greatly improves the steerability of models towards safe completions and refusals when exposed to adversarially learned suffixes.

### 4.3 Representation Analysis

To analyze the impact of various curricula on the underlying representation space of our models, we evaluate the separability of safe vs harmful content. We train linear probes to classify between examples from FineWeb data that have been annotated as safe versus unsafe, learned over the representations taken from the internal activations of the model’s final layer. For the safety label, we use the safety score from [Maini et al. (2025)](#bib.bib1), which is produced by GPT-4o-mini that judges pretraining examples with a safety rubric.

### 4.4 Training Details

#### Pretraining Setup 

For our experiments, we adopt the same setup of the SmolLM2 ([Allal et al., 2025](#bib.bib14)) for all our experiments. We train 1.7B parameter language models with a pretraining corpus of a mixture of FineWeb-Edu, StackOverflow, FineMath, and Cosmopedia. For our safety pretraining interventions, we adopt the modified datasets of SafeWeb, RefuseWeb, and MoralEducation from [Maini et al. (2025)](#bib.bib1), which are safety-focused, rephrased and recontextualized versions of harmful pretraining examples from FineWeb-Edu.

Pretraining is performed using LitGPT ([AI, 2023](#bib.bib15)), with FlashAttention-2 enabled and mixed-precision training for efficiency. We use the same hyperparameters (e.g., learning rate schedule, batch size, and sequence length) as in the SmolLM2 pretraining setup.

#### Post-training Setup 

For a standardized post-training stack, we use a combination of Ultrachat-200k with AllenAI WildGuardMix and WildJailbreak datasets for safety instruction tuning. This follows standard practice from prior works in safety training ([Zou et al., 2024](#bib.bib16); [Maini et al., 2025](#bib.bib1)).

## 5 Results

We now present our findings on how safety curricula influence robustness, helpfulness, and internal representations.

Figure 6: Separability of safe vs unsafe content (as annotated by GPT-4o-mini) in the last layer representation space of base models (Left) and instruction-tuned models (Right), as we vary the start timing when we incorporate safety pretraining interventions. We find that introducing interventions earlier yields greater separability in representation space (especially with the incorporation of harmful metadata tags). The shaded regions denote the standard deviation computed over 5 training runs.

### 5.1 Safety Results

#### Base Models

Timing matters even before instruction tuning (Figure [1](#S1.F1 "Figure 1 ‣ 1 Introduction ‣ When Should We Introduce Safety Interventions During Pretraining?")). Under standard top-k sampling, introducing interventions in the middle of pretraining (20% or 60%) yields the safest base models, while training on safe-only data (100%) is the least safe. This again complements the findings from prior work ([Li et al., 2025](#bib.bib30); [Maini et al., 2025](#bib.bib1)). In contrast, with SafeBeam, incorporating interventions and metadata from the start (0%) provides measurable gains.

#### Instruction-tuned Models

A similar pattern holds with the models that have undergone instruction tuning (Figure [3](#S2.F3 "Figure 3 ‣ Pretraining Safety ‣ 2 Related Work ‣ When Should We Introduce Safety Interventions During Pretraining?")). Models trained with interventions during the middle of pretraining exhibit stronger safety performance under top-*k* inference than those with no interventions. Again, SafeBeam benefits the most when metadata is incorporated from the beginning (i.e., 0%).

#### Benign Finetuned Models

The clearest and most noticeable effects emerge in our evaluation setting after a benign finetune on mathematical data (Figure [2](#S1.F2 "Figure 2 ‣ 1 Introduction ‣ When Should We Introduce Safety Interventions During Pretraining?")). Here, SafeBeam achieves the greatest robustness when interventions are included from the very start of pretraining. For standard top-*k* decoding, introducing interventions after roughly 20% of training yields the strongest post-finetuning safety.

Taken together, our evaluations suggest two main takeaways. First, when using modified SafeBeam inference, introducing metadata-annotated unsafe data earliest in pretraining leads to the best steerability towards safer completions. Secondly, with top-k inference, introducing safety pretraining interventions during the middle of training (after 20% or 60%) leads to the most robust performance. This suggests that allowing the model to first absorb general-purpose safe data before applying any safety interventions may produce alignment that is more robust to subsequent benign finetuning.

### 5.2 Capability Results

We evaluate whether safety pretraining interventions degrade general model capabilities across various standard benchmarks (Table [1](#S3.T1 "Table 1 ‣ Metadata-annotated Pretraining and SafeBeam ‣ 3.1 Safety Pretraining Interventions ‣ 3 Curricula for Safety ‣ When Should We Introduce Safety Interventions During Pretraining?")). Overall, we find that safety interventions introduce minimal capability trade-offs and, in some cases, may even improve performance. We attribute this to the model’s efficient learning from high-quality synthetic data ([Maini et al., 2024](#bib.bib22)). Taken together, these results indicate that safety pretraining interventions do not meaningfully degrade model capabilities; indeed, earlier interventions appear mildly beneficial on average.

### 5.3 Overrefusal Results

We assess the impact of pretraining interventions on model helpfulness using benign requests from the Alpaca benchmark ([Taori et al., 2023](#bib.bib24)). Under standard top-$k$ sampling (Figure [4](#S3.F4 "Figure 4 ‣ 3.2 Safety Curricula ‣ 3 Curricula for Safety ‣ When Should We Introduce Safety Interventions During Pretraining?")), incorporating interventions earlier during pretraining (0% or 20%) yields a slight improvement in compliance rates. These results suggest that safety pretraining interventions introduce minimal trade-offs in overrefusal behavior under standard inference.

When using the SafeBeam algorithm (Figure [9](#A1.F9 "Figure 9 ‣ Appendix A Additional Experiments ‣ When Should We Introduce Safety Interventions During Pretraining?")), we observe a more nuanced pattern: earlier interventions produce modestly higher overrefusal rates, yet the quality of compliant responses improves. The figure reveals that earlier pretraining interventions (0% and 20%) increase the fraction of compliant-and-helpful responses among non-refused outputs, even as overall refusal rates rise slightly. We hypothesize that this reflects improved calibration: early interventions strengthen the correspondence between the harmful metadata tag and genuinely unsafe content, enabling SafeBeam to filter more precisely. The surviving beams thus tend to produce higher-quality completions.

### 5.4 Jailbreaking Results

We also present results on how susceptible our models are to jailbreaking attacks using the GCG algorithm ([Zou et al., 2023](#bib.bib13)), as we vary the timing of the safety pretraining interventions. Surprisingly, we find that introducing pretraining interventions after some initial safe-only pretraining (i.e., at 20% or at 60%) leads to significantly more robustness to jailbreaks via GCG when using the SafeBeam inference algorithm (Figure [5](#S4.F5 "Figure 5 ‣ 4.2 Capability and Helpfulness Evaluations ‣ 4 Experiments ‣ When Should We Introduce Safety Interventions During Pretraining?")). On the other hand, we find that jailbreakability under standard inference does not noticeably change given different intervention timings.

### 5.5 Representation Results

In settings without harmful metadata tags, earlier interventions slightly improve the separability of safe versus unsafe points (with a linear classifier over the last-layer activations). When metadata is included, the effect is more pronounced: introducing interventions from the start yields the highest linear-probe AUC, suggesting a much cleaner separation of harmful and safe content in the representation space. This also supports the improved SafeBeam robustness, where models are more steerable towards safer responses when interventions are included early in pretraining.

## 6 Discussion

Our work studies the role of different safety curricula, or how the timing of safety pretraining interventions (e.g., when and how safety-augmented data enters pretraining) impacts the robustness of our models. Our experiments show that incorporating safety pretraining interventions indeed help, but the best timing depends on the setting: delayed interventions (e.g., 20%–60%) can yield stronger robustness under standard decoding and against adversarial jailbreaks, while early interventions (0%) improve steerability under safety-aware inference (SafeBeam) and yield clearer separation of safe vs unsafe content in representation space. Taken together, these findings highlight how the timing of safety interventions is an important choice in shaping a model’s behavior, offering guidance for building more trustworthy and responsible language models.

#### Why does timing matter?

While our experiments establish that intervention timing significantly affects outcomes, understanding the underlying mechanisms remains an open question. We offer several hypotheses for future investigation. For standard top-k decoding, delayed interventions (20%-60%) may succeed because the model benefits from first acquiring general linguistic competence and world knowledge before safety signals are introduced. Early safety interventions might compete with or interfere with learning basic representations, potentially causing the model to develop shallow safety heuristics rather than robust understanding. By contrast, when the model has already formed stable representations of language and concepts, safety interventions may integrate more deeply into these existing structures, making them harder to remove through subsequent finetuning.

For SafeBeam inference, early interventions may help because the metadata-based steering mechanism relies on strong, well-calibrated associations between the harmful content tag and genuinely unsafe material. Introducing these associations from the start of training allows them to be reinforced throughout the entire pretraining process, resulting in more reliable probability estimates that SafeBeam can exploit. This interpretation is supported by our representation analysis (Figure 6), which shows that early interventions with metadata yield the cleanest separation between safe and unsafe content in representation space.

A limitation of our study is that the introduction of safety pretraining interventions at different times during pretraining means that certain models have seen more synthetic contextualized data or refusal data. However, we note our main effects are not monotonic in the number of intervention tokens (i.e., “more intervention tokens” do not consistently yield safer models), suggesting that *when* safety-augmented data is introduced matters beyond total quantity.

## References

- Abdin et al. (2024) M. Abdin, J. Aneja, H. Awadalla, A. Awadallah, A. A. Awan, N. Bach, A. Bahree, A. Bakhtiari, J. Bao, H. Behl, et al. Phi-3 technical report: a highly capable language model locally on your phone. arXiv preprint arXiv:2404.14219. Cited by: [§2](#S2.SS0.SSS0.Px2.p1.1 "Curriculum Learning ‣ 2 Related Work ‣ When Should We Introduce Safety Interventions During Pretraining?").
- AI (2023) L. AI LitGPT. Note: [https://github.com/Lightning-AI/litgpt](https://github.com/Lightning-AI/litgpt) Cited by: [§4.4](#S4.SS4.SSS0.Px1.p2.1 "Pretraining Setup ‣ 4.4 Training Details ‣ 4 Experiments ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Allal et al. (2025) L. B. Allal, A. Lozhkov, E. Bakouch, G. M. Blázquez, G. Penedo, L. Tunstall, A. Marafioti, H. Kydlíček, A. P. Lajarín, V. Srivastav, J. Lochner, C. Fahlgren, X. Nguyen, C. Fourrier, B. Burtenshaw, H. Larcher, H. Zhao, C. Zakka, M. Morlon, C. Raffel, L. von Werra, and T. Wolf SmolLM2: when smol goes big – data-centric training of a small language model. External Links: 2502.02737, [Link](https://arxiv.org/abs/2502.02737) Cited by: [§1](#S1.p4.1 "1 Introduction ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§3.1](#S3.SS1.SSS0.Px3.p2.1 "Metadata-annotated Pretraining and SafeBeam ‣ 3.1 Safety Pretraining Interventions ‣ 3 Curricula for Safety ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§4.4](#S4.SS4.SSS0.Px1.p1.1 "Pretraining Setup ‣ 4.4 Training Details ‣ 4 Experiments ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Andriushchenko et al. (2025) M. Andriushchenko, A. Souly, M. Dziemian, D. Duenas, M. Lin, J. Wang, D. Hendrycks, A. Zou, J. Z. Kolter, M. Fredrikson, Y. Gal, and X. Davies AgentHarm: a benchmark for measuring harmfulness of LLM agents. In The Thirteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=AC5n7xHuR1) Cited by: [Appendix C](#A3.p1.1 "Appendix C Additional Discussion ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Bai et al. (2022) Y. Bai, S. Kadavath, S. Kundu, A. Askell, J. Kernion, A. Jones, A. Chen, A. Goldie, A. Mirhoseini, C. McKinnon, et al. Constitutional ai: harmlessness from ai feedback. arXiv preprint arXiv:2212.08073. Cited by: [§1](#S1.p1.1 "1 Introduction ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Bengio et al. (2009) Y. Bengio, J. Louradour, R. Collobert, and J. Weston Curriculum learning. In Proceedings of the 26th annual international conference on machine learning, pp. 41–48. Cited by: [§1](#S1.p3.1 "1 Introduction ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§2](#S2.SS0.SSS0.Px2.p1.1 "Curriculum Learning ‣ 2 Related Work ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Betley et al. (2025) J. Betley, D. Tan, N. Warncke, A. Sztyber-Betley, X. Bao, M. Soto, N. Labenz, and O. Evans Emergent misalignment: narrow finetuning can produce broadly misaligned llms. arXiv preprint arXiv:2502.17424. Cited by: [§1](#S1.p1.1 "1 Introduction ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§3.1](#S3.SS1.SSS0.Px2.p1.1 "Refusal Training ‣ 3.1 Safety Pretraining Interventions ‣ 3 Curricula for Safety ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§4.1](#S4.SS1.p3.1 "4.1 Safety Evaluations ‣ 4 Experiments ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Blakeney et al. (2024) C. Blakeney, M. Paul, B. W. Larsen, S. Owen, and J. Frankle Does your data spark joy? performance gains from domain upsampling at the end of training. In First Conference on Language Modeling, External Links: [Link](https://openreview.net/forum?id=vwIIAot0ff) Cited by: [§2](#S2.SS0.SSS0.Px3.p2.1 "Stages of Language Model Pretraining ‣ 2 Related Work ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Byun et al. (2025) Y. Byun, S. Gupta, Z. C. Lipton, R. L. Childers, and B. Wilder Using imperfect synthetic data in downstream inference tasks. arXiv preprint arXiv:2508.06635. Cited by: [§1](#S1.p1.1 "1 Introduction ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Chao et al. (2024) P. Chao, E. Debenedetti, A. Robey, M. Andriushchenko, F. Croce, V. Sehwag, E. Dobriban, N. Flammarion, G. J. Pappas, F. Tramèr, et al. JailbreakBench: an open robustness benchmark for jailbreaking large language models. In Conference on Neural Information Processing Systems (NeurIPS), Cited by: [§4.1](#S4.SS1.p2.1 "4.1 Safety Evaluations ‣ 4 Experiments ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Chao et al. (2023) P. Chao, A. Robey, E. Dobriban, H. Hassani, G. J. Pappas, and E. Wong Jailbreaking black box large language models in twenty queries. arXiv preprint arXiv:2310.08419. Cited by: [§1](#S1.p1.1 "1 Introduction ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Chen et al. (2023) M. Chen, N. Roberts, K. Bhatia, J. Wang, C. Zhang, F. Sala, and C. Ré Skill-it! a data-driven skills framework for understanding and training language models. Advances in Neural Information Processing Systems 36, pp. 36000–36040. Cited by: [§3.2](#S3.SS2.p1.1 "3.2 Safety Curricula ‣ 3 Curricula for Safety ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Cobbe et al. (2021) K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert, J. Tworek, J. Hilton, R. Nakano, et al. Training verifiers to solve math word problems. arXiv preprint arXiv:2110.14168. Cited by: [§4.1](#S4.SS1.p1.1 "4.1 Safety Evaluations ‣ 4 Experiments ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§4.1](#S4.SS1.p3.1 "4.1 Safety Evaluations ‣ 4 Experiments ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Firoozi et al. (2025) R. Firoozi, J. Tucker, S. Tian, A. Majumdar, J. Sun, W. Liu, Y. Zhu, S. Song, A. Kapoor, K. Hausman, et al. Foundation models in robotics: applications, challenges, and the future. The International Journal of Robotics Research 44 (5), pp. 701–739. Cited by: [§1](#S1.p1.1 "1 Introduction ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Gao et al. (2024) L. Gao, J. Tow, B. Abbasi, S. Biderman, S. Black, A. DiPofi, C. Foster, L. Golding, J. Hsu, A. Le Noac’h, H. Li, K. McDonell, N. Muennighoff, C. Ociepa, J. Phang, L. Reynolds, H. Schoelkopf, A. Skowron, L. Sutawika, E. Tang, A. Thite, B. Wang, K. Wang, and A. Zou The language model evaluation harness. Zenodo. External Links: [Document](https://dx.doi.org/10.5281/zenodo.12608602), [Link](https://zenodo.org/records/12608602) Cited by: [Appendix B](#A2.SS0.SSS0.Px2.p1.1 "Capabilities Evaluation ‣ Appendix B Additional Experimental Details ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Graves et al. (2017) A. Graves, M. G. Bellemare, J. Menick, R. Munos, and K. Kavukcuoglu Automated curriculum learning for neural networks. In international conference on machine learning, pp. 1311–1320. Cited by: [§1](#S1.p3.1 "1 Introduction ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§2](#S2.SS0.SSS0.Px2.p1.1 "Curriculum Learning ‣ 2 Related Work ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Gunasekar et al. (2023) S. Gunasekar, Y. Zhang, J. Aneja, C. C. T. Mendes, A. Del Giorno, S. Gopi, M. Javaheripi, P. Kauffmann, G. de Rosa, O. Saarikivi, et al. Textbooks are all you need. arXiv preprint arXiv:2306.11644. Cited by: [§2](#S2.SS0.SSS0.Px1.p1.1 "Pretraining Safety ‣ 2 Related Work ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Jiang et al. (2024) Y. Jiang, A. Zhou, Z. Feng, S. Malladi, and J. Z. Kolter Adaptive data optimization: dynamic sample selection with scaling laws. arXiv preprint arXiv:2410.11820. Cited by: [§2](#S2.SS0.SSS0.Px3.p1.1 "Stages of Language Model Pretraining ‣ 2 Related Work ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Korbak et al. (2023) T. Korbak, K. Shi, A. Chen, R. Bhalerao, C. L. Buckley, J. Phang, S. Bowman, and E. Perez Pretraining language models with human preferences. arXiv preprint arXiv:2302.08582. Cited by: [§2](#S2.SS0.SSS0.Px1.p1.1 "Pretraining Safety ‣ 2 Related Work ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Li et al. (2025) K. Li, Y. Chen, F. Viégas, and M. Wattenberg When bad data leads to good models. In Forty-second International Conference on Machine Learning, External Links: [Link](https://openreview.net/forum?id=SsLGTZKXf1) Cited by: [§1](#S1.p2.1 "1 Introduction ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§2](#S2.SS0.SSS0.Px1.p2.1 "Pretraining Safety ‣ 2 Related Work ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§5.1](#S5.SS1.SSS0.Px1.p1.1 "Base Models ‣ 5.1 Safety Results ‣ 5 Results ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Li et al. (2024) N. Li, A. Pan, A. Gopal, S. Yue, D. Berrios, A. Gatti, J. D. Li, A. Dombrowski, S. Goel, L. Phan, et al. The wmdp benchmark: measuring and reducing malicious use with unlearning. arXiv preprint arXiv:2403.03218. Cited by: [Appendix C](#A3.p1.1 "Appendix C Additional Discussion ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Liévin et al. (2024) V. Liévin, C. E. Hother, A. G. Motzfeldt, and O. Winther Can large language models reason about medical questions?. Patterns 5 (3). Cited by: [§1](#S1.p1.1 "1 Introduction ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Maini et al. (2025) P. Maini, S. Goyal, D. Sam, A. Robey, Y. Savani, Y. Jiang, A. Zou, Z. C. Lipton, and J. Z. Kolter Safety pretraining: toward the next generation of safe ai. arXiv preprint arXiv:2504.16980. Cited by: [Appendix B](#A2.SS0.SSS0.Px1.p1.1 "Safety Evaluation ‣ Appendix B Additional Experimental Details ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§1](#S1.p2.1 "1 Introduction ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§1](#S1.p4.1 "1 Introduction ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§2](#S2.SS0.SSS0.Px1.p2.1 "Pretraining Safety ‣ 2 Related Work ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§3.1](#S3.SS1.p1.1 "3.1 Safety Pretraining Interventions ‣ 3 Curricula for Safety ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§3.2](#S3.SS2.p1.1 "3.2 Safety Curricula ‣ 3 Curricula for Safety ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§3.2](#S3.SS2.p2.1 "3.2 Safety Curricula ‣ 3 Curricula for Safety ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§3.2](#S3.SS2.p3.1 "3.2 Safety Curricula ‣ 3 Curricula for Safety ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§4.1](#S4.SS1.p1.1 "4.1 Safety Evaluations ‣ 4 Experiments ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§4.1](#S4.SS1.p2.1 "4.1 Safety Evaluations ‣ 4 Experiments ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§4.3](#S4.SS3.p1.1 "4.3 Representation Analysis ‣ 4 Experiments ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§4.4](#S4.SS4.SSS0.Px1.p1.1 "Pretraining Setup ‣ 4.4 Training Details ‣ 4 Experiments ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§4.4](#S4.SS4.SSS0.Px2.p1.1 "Post-training Setup ‣ 4.4 Training Details ‣ 4 Experiments ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§5.1](#S5.SS1.SSS0.Px1.p1.1 "Base Models ‣ 5.1 Safety Results ‣ 5 Results ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Maini et al. (2024) P. Maini, S. Seto, R. Bai, D. Grangier, Y. Zhang, and N. Jaitly Rephrasing the web: a recipe for compute and data-efficient language modeling. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), L. Ku, A. Martins, and V. Srikumar (Eds.), Bangkok, Thailand, pp. 14044–14072. External Links: [Link](https://aclanthology.org/2024.acl-long.757/), [Document](https://dx.doi.org/10.18653/v1/2024.acl-long.757) Cited by: [§5.2](#S5.SS2.p1.1 "5.2 Capability Results ‣ 5 Results ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Maloyan et al. (2024) N. Maloyan, E. Verma, B. Nutfullin, and B. Ashinov Trojan detection in large language models: insights from the trojan detection challenge. arXiv preprint arXiv:2404.13660. Cited by: [§4.1](#S4.SS1.p2.1 "4.1 Safety Evaluations ‣ 4 Experiments ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Mazeika et al. (2024) M. Mazeika, L. Phan, X. Yin, A. Zou, Z. Wang, N. Mu, E. Sakhaee, N. Li, S. Basart, B. Li, D. Forsyth, and D. Hendrycks HarmBench: a standardized evaluation framework for automated red teaming and robust refusal. arXiv preprint arXiv:2402.04249. External Links: 2402.04249 Cited by: [Appendix B](#A2.SS0.SSS0.Px1.p1.1 "Safety Evaluation ‣ Appendix B Additional Experimental Details ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§4.1](#S4.SS1.p2.1 "4.1 Safety Evaluations ‣ 4 Experiments ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Ouyang et al. (2022) L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray, et al. Training language models to follow instructions with human feedback. Advances in neural information processing systems 35, pp. 27730–27744. Cited by: [§1](#S1.p1.1 "1 Introduction ‣ When Should We Introduce Safety Interventions During Pretraining?").
- O’Brien et al. (2025) K. O’Brien, S. Casper, Q. Anthony, T. Korbak, R. Kirk, X. Davies, I. Mishra, G. Irving, Y. Gal, and S. Biderman Deep ignorance: filtering pretraining data builds tamper-resistant safeguards into open-weight llms. arXiv preprint arXiv:2508.06601. Cited by: [§1](#S1.p2.1 "1 Introduction ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§2](#S2.SS0.SSS0.Px1.p2.1 "Pretraining Safety ‣ 2 Related Work ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§3.2](#S3.SS2.p1.1 "3.2 Safety Curricula ‣ 3 Curricula for Safety ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§3.2](#S3.SS2.p2.1 "3.2 Safety Curricula ‣ 3 Curricula for Safety ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Penedo et al. (2024) G. Penedo, H. Kydlíček, L. B. allal, A. Lozhkov, M. Mitchell, C. Raffel, L. V. Werra, and T. Wolf The fineweb datasets: decanting the web for the finest text data at scale. External Links: 2406.17557, [Link](https://arxiv.org/abs/2406.17557) Cited by: [§1](#S1.p4.1 "1 Introduction ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§2](#S2.SS0.SSS0.Px1.p1.1 "Pretraining Safety ‣ 2 Related Work ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§3.1](#S3.SS1.SSS0.Px3.p2.1 "Metadata-annotated Pretraining and SafeBeam ‣ 3.1 Safety Pretraining Interventions ‣ 3 Curricula for Safety ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Qi et al. (2024a) X. Qi, A. Panda, K. Lyu, X. Ma, S. Roy, A. Beirami, P. Mittal, and P. Henderson Safety alignment should be made more than just a few tokens deep. arXiv preprint arXiv:2406.05946. Cited by: [§1](#S1.p1.1 "1 Introduction ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§3.1](#S3.SS1.SSS0.Px2.p1.1 "Refusal Training ‣ 3.1 Safety Pretraining Interventions ‣ 3 Curricula for Safety ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§4.1](#S4.SS1.p3.1 "4.1 Safety Evaluations ‣ 4 Experiments ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Qi et al. (2024b) X. Qi, A. Panda, K. Lyu, X. Ma, S. Roy, A. Beirami, P. Mittal, and P. Henderson Safety alignment should be made more than just a few tokens deep. External Links: 2406.05946, [Link](https://arxiv.org/abs/2406.05946) Cited by: [§1](#S1.p1.1 "1 Introduction ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Rafailov et al. (2023) R. Rafailov, A. Sharma, E. Mitchell, C. D. Manning, S. Ermon, and C. Finn Direct preference optimization: your language model is secretly a reward model. Advances in Neural Information Processing Systems 36, pp. 53728–53741. Cited by: [§1](#S1.p1.1 "1 Introduction ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Raffel et al. (2020) C. Raffel, N. Shazeer, A. Roberts, K. Lee, S. Narang, M. Matena, Y. Zhou, W. Li, and P. J. Liu Exploring the limits of transfer learning with a unified text-to-text transformer. Journal of machine learning research 21 (140), pp. 1–67. Cited by: [§2](#S2.SS0.SSS0.Px1.p1.1 "Pretraining Safety ‣ 2 Related Work ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Robey et al. (2024) A. Robey, Z. Ravichandran, V. Kumar, H. Hassani, and G. J. Pappas Jailbreaking llm-controlled robots. arXiv preprint arXiv:2410.13691. Cited by: [§1](#S1.p1.1 "1 Introduction ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Sachan and Xing (2016) M. Sachan and E. Xing Easy questions first? a case study on curriculum learning for question answering. In Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 453–463. Cited by: [§2](#S2.SS0.SSS0.Px2.p1.1 "Curriculum Learning ‣ 2 Related Work ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Sam et al. (2025a) D. Sam, A. Chakrabarti, A. Rostamizadeh, S. Ramalingam, G. Citovsky, and S. Kumar Analyzing similarity metrics for data selection for language model pretraining. arXiv preprint arXiv:2502.02494. Cited by: [§2](#S2.SS0.SSS0.Px2.p1.1 "Curriculum Learning ‣ 2 Related Work ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Sam et al. (2025b) D. Sam, M. Finzi, and J. Z. Kolter Predicting the performance of black-box llms through self-queries. arXiv preprint arXiv:2501.01558. Cited by: [Appendix C](#A3.p2.1 "Appendix C Additional Discussion ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Sam et al. (2025c) D. Sam, A. Robey, A. Zou, M. Fredrikson, and J. Z. Kolter Evaluating language model reasoning about confidential information. arXiv preprint arXiv:2508.19980. Cited by: [Appendix C](#A3.p1.1 "Appendix C Additional Discussion ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Sharma et al. (2025) M. Sharma, M. Tong, J. Mu, J. Wei, J. Kruthoff, S. Goodfriend, E. Ong, A. Peng, R. Agarwal, C. Anil, et al. Constitutional classifiers: defending against universal jailbreaks across thousands of hours of red teaming. arXiv preprint arXiv:2501.18837. Cited by: [Appendix C](#A3.p2.1 "Appendix C Additional Discussion ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Taori et al. (2023) R. Taori, I. Gulrajani, T. Zhang, Y. Dubois, X. Li, C. Guestrin, P. Liang, and T. B. Hashimoto Stanford alpaca: an instruction-following llama model. Stanford, CA, USA. Cited by: [Figure 4](#S3.F4 "In 3.2 Safety Curricula ‣ 3 Curricula for Safety ‣ When Should We Introduce Safety Interventions During Pretraining?"), [Figure 4](#S3.F4.5 "In 3.2 Safety Curricula ‣ 3 Curricula for Safety ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§4.2](#S4.SS2.p2.1 "4.2 Capability and Helpfulness Evaluations ‣ 4 Experiments ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§5.3](#S5.SS3.p1.1 "5.3 Overrefusal Results ‣ 5 Results ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Thirunavukarasu et al. (2023) A. J. Thirunavukarasu, D. S. J. Ting, K. Elangovan, L. Gutierrez, T. F. Tan, and D. S. W. Ting Large language models in medicine. Nature medicine 29 (8), pp. 1930–1940. Cited by: [§1](#S1.p1.1 "1 Introduction ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Touvron et al. (2023) H. Touvron, T. Lavril, G. Izacard, X. Martinet, M. Lachaux, T. Lacroix, B. Rozière, N. Goyal, E. Hambro, F. Azhar, et al. LLaMA: open and efficient foundation language models. arXiv preprint arXiv:2302.13971. Cited by: [§3.1](#S3.SS1.SSS0.Px1.p1.1 "Contextualized Rephrasing ‣ 3.1 Safety Pretraining Interventions ‣ 3 Curricula for Safety ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Turner et al. (2023) A. M. Turner, L. Thiergart, G. Leech, D. Udell, J. J. Vazquez, U. Mini, and M. MacDiarmid Steering language models with activation engineering. arXiv preprint arXiv:2308.10248. Cited by: [Appendix C](#A3.p2.1 "Appendix C Additional Discussion ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Vidgen et al. (2024) B. Vidgen, A. Agrawal, A. M. Ahmed, V. Akinwande, N. Al-Nuaimi, N. Alfaraj, E. Alhajjar, L. Aroyo, T. Bavalatti, M. Bartolo, et al. Introducing v0. 5 of the ai safety benchmark from mlcommons. arXiv preprint arXiv:2404.12241. Cited by: [Appendix C](#A3.p1.1 "Appendix C Additional Discussion ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§2](#S2.SS0.SSS0.Px1.p1.1 "Pretraining Safety ‣ 2 Related Work ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Wu et al. (2021) X. Wu, E. Dyer, and B. Neyshabur When do curricula work?. In International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=tW4QEInpni) Cited by: [§2](#S2.SS0.SSS0.Px2.p1.1 "Curriculum Learning ‣ 2 Related Work ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Xie et al. (2023) S. M. Xie, H. Pham, X. Dong, N. Du, H. Liu, Y. Lu, P. S. Liang, Q. V. Le, T. Ma, and A. W. Yu Doremi: optimizing data mixtures speeds up language model pretraining. Advances in Neural Information Processing Systems 36, pp. 69798–69818. Cited by: [§2](#S2.SS0.SSS0.Px3.p1.1 "Stages of Language Model Pretraining ‣ 2 Related Work ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Xue (2020) L. Xue Mt5: a massively multilingual pre-trained text-to-text transformer. arXiv preprint arXiv:2010.11934. Cited by: [§2](#S2.SS0.SSS0.Px1.p1.1 "Pretraining Safety ‣ 2 Related Work ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Ye et al. (2025) J. Ye, P. Liu, T. Sun, J. Zhan, Y. Zhou, and X. Qiu Data mixing laws: optimizing data mixtures by predicting language modeling performance. In The Thirteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=jjCB27TMK3) Cited by: [§2](#S2.SS0.SSS0.Px3.p1.1 "Stages of Language Model Pretraining ‣ 2 Related Work ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Yuan et al. (2025) Y. Yuan, T. Sriskandarajah, A. Brakman, A. Helyar, A. Beutel, A. Vallone, and S. Jain From hard refusals to safe-completions: toward output-centric safety training. arXiv preprint arXiv:2508.09224. Cited by: [§3.1](#S3.SS1.SSS0.Px3.p1.1 "Metadata-annotated Pretraining and SafeBeam ‣ 3.1 Safety Pretraining Interventions ‣ 3 Curricula for Safety ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Zhang et al. (2020) Y. Zhang, P. Abbeel, and L. Pinto Automatic curriculum learning through value disagreement. Advances in Neural Information Processing Systems 33, pp. 7648–7659. Cited by: [§2](#S2.SS0.SSS0.Px2.p1.1 "Curriculum Learning ‣ 2 Related Work ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Ziems et al. (2024) C. Ziems, W. Held, O. Shaikh, J. Chen, Z. Zhang, and D. Yang Can large language models transform computational social science?. Computational Linguistics 50 (1), pp. 237–291. Cited by: [§1](#S1.p1.1 "1 Introduction ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Zou et al. (2024) A. Zou, L. Phan, J. Wang, D. Duenas, M. Lin, M. Andriushchenko, R. Wang, Z. Kolter, M. Fredrikson, and D. Hendrycks Improving alignment and robustness with circuit breakers. External Links: 2406.04313, [Link](https://arxiv.org/abs/2406.04313) Cited by: [Appendix C](#A3.p2.1 "Appendix C Additional Discussion ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§4.4](#S4.SS4.SSS0.Px2.p1.1 "Post-training Setup ‣ 4.4 Training Details ‣ 4 Experiments ‣ When Should We Introduce Safety Interventions During Pretraining?").
- Zou et al. (2023) A. Zou, Z. Wang, N. Carlini, M. Nasr, J. Z. Kolter, and M. Fredrikson Universal and transferable adversarial attacks on aligned language models. arXiv preprint arXiv:2307.15043. Cited by: [§1](#S1.p1.1 "1 Introduction ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§1](#S1.p5.1 "1 Introduction ‣ When Should We Introduce Safety Interventions During Pretraining?"), [Figure 5](#S4.F5 "In 4.2 Capability and Helpfulness Evaluations ‣ 4 Experiments ‣ When Should We Introduce Safety Interventions During Pretraining?"), [Figure 5](#S4.F5.4 "In 4.2 Capability and Helpfulness Evaluations ‣ 4 Experiments ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§4.1](#S4.SS1.p2.1 "4.1 Safety Evaluations ‣ 4 Experiments ‣ When Should We Introduce Safety Interventions During Pretraining?"), [§5.4](#S5.SS4.p1.1 "5.4 Jailbreaking Results ‣ 5 Results ‣ When Should We Introduce Safety Interventions During Pretraining?").

## Appendix A Additional Experiments

Figure 7: Separability of safe vs unsafe content (as annotated by GPT-4o-mini) in the first layer of base models (Left) and instruction-tuned models (Right), as we vary the start timing when we incorporate safety pretraining interventions. The shaded regions denote the standard deviation computed over 5 training runs.

Figure 8: Separability of safe vs unsafe content (as annotated by GPT-4o-mini) in the middle (13th) layer of base models (Left) and instruction-tuned models (Right), as we vary the start timing when we incorporate safety pretraining interventions. The shaded regions denote the standard deviation computed over 5 training runs.

Figure 9: Comparison of overrefusal rates on Alpaca when using the SafeBeam inference algorithm. We find that introducing pretraining interventions and metadata earlier during pretraining leads to more helpful compliant behavior, with a slight increase in overrefusal rates.

#### Additional Separability Results.

In the main text, we present results on separability of harmful vs safe content in the final layer of the resulting pretraining models. Here, we also present results for the first layer and the middle (13th) layer. We observe similar trends, although we find greater separability in the final layer when compared to earlier layers in the models.

#### SafeBeam Overrefusal.

Figure [9](#A1.F9 "Figure 9 ‣ Appendix A Additional Experiments ‣ When Should We Introduce Safety Interventions During Pretraining?") extends our overrefusal analysis to the SafeBeam inference setting. Compared to standard top-$k$ sampling, SafeBeam introduces a fifth response category (*shortcircuit*), which occurs when generation terminates upon producing the harmful metadata token. In deployment, such responses can be handled by substituting a predetermined safe completion.

## Appendix B Additional Experimental Details

#### Safety Evaluation

For our standard inference evaluations, we use top-k sampling with $k = 10$ and truncate after 256 tokens. We average the results over 5 samples. For SafeBeam evaluation, we run a beam search with $10$ beams for 256 tokens, and discard the top 50% of unsafe beams (in terms of probability of the next token being the harmful metadata token). We follow the same exact setting as [Maini et al. \[2025\]](#bib.bib1). We adopt the same GPT-4o-mini judge and judging prompt for helpfulness evaluations, and the same HarmBench judge and judge prompt \[[Mazeika et al., 2024](#bib.bib20)\] for our safety evaluations.

#### Capabilities Evaluation

We use the default experimental setting for all the datasets as provided as in the LM evaluation harness \[[Gao et al., 2024](#bib.bib53)\]. We use the dataset default few-shot settings: 0-shot for ARC-Challenge, OpenBookQA, CommonsenseQA, PIQA, TriviaQA, and WinoGrande (num_fewshot=0), and 5-shot for GSM8K (num_fewshot=5; few-shot examples sampled from the training split).

#### Adversarial Jailbreaking

For computing the adversarial suffixes via the GCG algorithm, we learn an adversarial suffix on the target model, optimizing for the target string of “Sure”. We perform optimization for 500 steps, with an initialization of “x x ... x”, and top_k of 256.

#### Finetuning

For our supervised instruction tuning, we finetune with a batch size of 4 with a learning rate of 2e-5 for one epoch, using cosine learning rate decay with a warmup ratio of 0.03. For our benign finetuning experiments, we perform supervised finetuning on GSM8k for a single epoch with a learning rate of 2e-5 with the same learning rate schedule as in instruction tuning.

#### Separability Experiments

In our separability experiments, we use the last token position and the final layer of all models. For each model, we train a logistic regression classifier on a balanced subset of 500 safe and 500 unsafe examples from the training split, and the trained probe is evaluated on the full balanced test set. We report the mean, standard deviation, and standard error, when computed over five seeds, of the test AUC (area under the ROC curve).

## Appendix C Additional Discussion

We note that the notion of safety that we focus on in this paper is fairly broad, encompassing general notions of toxicity and harms. This is taken from the taxonomy proposed by the MLCommons \[[Vidgen et al., 2024](#bib.bib7)\], captures a wide variety of potential harms and undesirable behaviors in different domains. Our method likely requires additional efforts to tackle safety for specific capabilities, such as bio-weapons and cybersecurity \[[Li et al., 2024](#bib.bib9)\] or reliability of agents in context-dependent scenarios \[[Andriushchenko et al., 2025](#bib.bib49), [Sam et al., 2025c](#bib.bib50)\].

We also note that our results on the separability of safe vs unsafe content has greater implications for the monitoring of such models. These experiments contribute to a line of work that develops external monitoring to predict when undesirable generations will occur and steer towards safer outputs \[[Turner et al., 2023](#bib.bib51), [Zou et al., 2024](#bib.bib16)\]. This may even have implications for complementary alternative approaches that are adopted in black-box settings and use external models \[[Sharma et al., 2025](#bib.bib48), [Sam et al., 2025b](#bib.bib47)\], which is an area for future study.

## Appendix D Computational Resources

For each variant of the pretraining runs for the 1.7B parameter model on 600B tokens, we used 32 H100 GPUs for roughly 6-7 days. Finetuning requires roughly 4 H100 GPUs for 4 hours. Evaluations are run on one L40S GPU.

Experimental support, please [view the build logs](./2601.07087v2/__stdout.txt) for errors. Generated by [ L A T E xml ![\[LOGO\]](img)](https://math.nist.gov/~BMiller/LaTeXML/) .

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
