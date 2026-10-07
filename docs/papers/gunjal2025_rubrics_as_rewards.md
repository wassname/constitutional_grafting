---
title: "Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains"
authors: "Anisha Gunjal; Anthony Wang; Elaine Lau; Vaskar Nath; Yunzhong He; Bing Liu; Sean Hendryx"
year: 2025
source: https://arxiv.org/html/2507.17746
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

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) [![](img) Report Issue](# "Report an Issue") [![](img) Back to Abstract](/abs/2507.17746v2 "Back to abstract page") [![](img) Download PDF](/pdf/2507.17746v2 "Download PDF") [![](img)](javascript:toggleNavTOC(); "Toggle navigation") [![](img)](javascript:toggleReadingMode(); "Disable reading mode, show header and footer")

![](img) ![](img) ![](img)

1.  [Abstract](#abstract1 "In Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
2.  [1 Introduction](#S1 "In Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
3.  [2 Rubrics as Rewards](#S2 "In Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
    1.  [2.1 Problem Formulation](#S2.SS1 "In 2 Rubrics as Rewards ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
    2.  [2.2 Reward Aggregation Strategies](#S2.SS2 "In 2 Rubrics as Rewards ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
        1.  [Explicit Aggregation.](#S2.SS2.SSS0.Px1 "In 2.2 Reward Aggregation Strategies ‣ 2 Rubrics as Rewards ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
        2.  [Implicit Aggregation.](#S2.SS2.SSS0.Px2 "In 2.2 Reward Aggregation Strategies ‣ 2 Rubrics as Rewards ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
    3.  [2.3 Generalization of RLVR with Rubrics as Rewards](#S2.SS3 "In 2 Rubrics as Rewards ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
4.  [3 Rubric Generation](#S3 "In Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
    1.  [3.1 Desiderata](#S3.SS1 "In 3 Rubric Generation ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
        1.  [Grounded in Expert Guidance.](#S3.SS1.SSS0.Px1 "In 3.1 Desiderata ‣ 3 Rubric Generation ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
        2.  [Comprehensive Coverage.](#S3.SS1.SSS0.Px2 "In 3.1 Desiderata ‣ 3 Rubric Generation ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
        3.  [Criterion Importance.](#S3.SS1.SSS0.Px3 "In 3.1 Desiderata ‣ 3 Rubric Generation ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
        4.  [Self-Contained Evaluation.](#S3.SS1.SSS0.Px4 "In 3.1 Desiderata ‣ 3 Rubric Generation ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
    2.  [3.2 Rubrics Creation](#S3.SS2 "In 3 Rubric Generation ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
5.  [4 Experiments](#S4 "In Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
    1.  [4.1 Datasets](#S4.SS1 "In 4 Experiments ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
    2.  [4.2 Training Details](#S4.SS2 "In 4 Experiments ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
    3.  [4.3 Rubric-Free Baselines](#S4.SS3 "In 4 Experiments ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
    4.  [4.4 Rubric-guided Methods](#S4.SS4 "In 4 Experiments ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
    5.  [4.5 Evaluation Setup](#S4.SS5 "In 4 Experiments ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
        1.  [Rubric-Based Evaluation](#S4.SS5.SSS0.Px1 "In 4.5 Evaluation Setup ‣ 4 Experiments ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
        2.  [Multiple-Choice Evaluation](#S4.SS5.SSS0.Px2 "In 4.5 Evaluation Setup ‣ 4 Experiments ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
        3.  [LLM-Judge Alignment Evaluation](#S4.SS5.SSS0.Px3 "In 4.5 Evaluation Setup ‣ 4 Experiments ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
6.  [5 Results](#S5 "In Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
    1.  [Rubrics as Rewards shows strong gains across evaluation settings.](#S5.SS0.SSS0.Px1 "In 5 Results ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
    2.  [Rubrics enhance alignment with human preferences across model scales](#S5.SS0.SSS0.Px2 "In 5 Results ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
    3.  [Expert guidance is crucial for synthetic rubric generation](#S5.SS0.SSS0.Px3 "In 5 Results ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
7.  [6 Ablations](#S6 "In Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
    1.  [Impact of Rubric Generation Strategies in Real-World Domains](#S6.SS0.SSS0.Px1 "In 6 Ablations ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
    2.  [Elements of Rubric Design](#S6.SS0.SSS0.Px2 "In 6 Ablations ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
    3.  [Impact of LLM Expertise on Rubric Quality](#S6.SS0.SSS0.Px3 "In 6 Ablations ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
8.  [7 Related Work](#S7 "In Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
    1.  [RLVR across domains](#S7.SS0.SSS0.Px1 "In 7 Related Work ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
    2.  [Rubrics for evaluation and training](#S7.SS0.SSS0.Px2 "In 7 Related Work ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
    3.  [Learning from feedback signals](#S7.SS0.SSS0.Px3 "In 7 Related Work ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
9.  [8 Conclusion](#S8 "In Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
10. [9 Limitations and Future Work](#S9 "In Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
11. [References](#bib "In Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
12. [A Appendix](#A1 "In Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
    1.  [A.1 Details of RaR-Medicine dataset](#A1.SS1 "In Appendix A Appendix ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
    2.  [A.2 Details of RaR-Science dataset](#A1.SS2 "In Appendix A Appendix ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
    3.  [A.3 Training Details](#A1.SS3 "In Appendix A Appendix ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
    4.  [A.4 Evaluation Prompts](#A1.SS4 "In Appendix A Appendix ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
    5.  [A.5 Predefined Static Rubrics](#A1.SS5 "In Appendix A Appendix ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
    6.  [A.6 LLM-Judge Prompts](#A1.SS6 "In Appendix A Appendix ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
    7.  [A.7 Synthetic Preference Set Generation](#A1.SS7 "In Appendix A Appendix ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
    8.  [A.8 Judge Quality impacts on Post-training](#A1.SS8 "In Appendix A Appendix ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")
    9.  [A.9 Perturbed Dataset Generation](#A1.SS9 "In Appendix A Appendix ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")

[License: CC BY 4.0](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2507.17746v2 \[cs.LG\] 03 Oct 2025

# Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains

Anisha Gunjal Affiliation: Scale AI  
^(∗)Work done during internship at Scale AI    Anthony Wang^(∗) Affiliation: Scale AI  
^(∗)Work done during internship at Scale AI    Elaine Lau Affiliation: Scale AI  
^(∗)Work done during internship at Scale AI    Vaskar Nath Affiliation: Scale AI  
^(∗)Work done during internship at Scale AI    Yunzhong He Affiliation: Scale AI  
^(∗)Work done during internship at Scale AI    Bing Liu Affiliation: Scale AI  
^(∗)Work done during internship at Scale AI    Sean Hendryx Affiliation: Scale AI  
^(∗)Work done during internship at Scale AI

###### Abstract

Reinforcement Learning with Verifiable Rewards (RLVR) has proven effective for complex reasoning tasks with clear correctness signals such as math and coding. However, extending it to real-world reasoning tasks is challenging, as evaluation depends on nuanced, multi-criteria judgments rather than binary correctness. Instance-specific rubrics have recently been used in evaluation benchmarks to capture such judgments, but their potential as reward signals for on-policy post-training remains underexplored. We introduce Rubrics as Rewards (RaR), an on-policy reinforcement learning method that extends RLVR beyond verifiable domains by using rubric-based feedback. Across both medical and science domains, we evaluate multiple strategies for aggregating rubric feedback into rewards. The best RaR variant achieves relative improvements of up to 31% on HealthBench and 7% on GPQA-Diamond over popular LLM-as-judge baselines that rely on direct Likert-based rewards. These results demonstrate that RaR-trained policies adapt well to diverse evaluation formats, performing strongly on both rubric-based and multiple-choice tasks. Moreover, we find that using rubrics as structured reward signals yields better alignment for smaller judges and reduces performance variance across judge scales.

anisha.gunjal@scale.com

## 1 Introduction

Reinforcement Learning with Verifiable Rewards (RLVR) has enabled large language models to elicit complex reasoning on tasks with clear verifiable outcomes. This is especially effective in domains like math and code, where reward models can be replaced by scoring functions or test cases that automatically verify correctness \[[19](#bib.bib19), [11](#bib.bib11), [6](#bib.bib6)\]. However, extending RLVR to unstructured, real-world reasoning is challenging because such tasks lack easily verifiable answers. A common workaround is to use preference-based reward models, but they tend to overfit superficial artifacts (e.g. response length, formatting quirks, annotator biases) \[[29](#bib.bib29), [34](#bib.bib34), [4](#bib.bib4), [36](#bib.bib36), [10](#bib.bib10)\] and require large volumes of pairwise comparisons \[[25](#bib.bib25)\]. Instance-specific rubrics have recently emerged for nuanced evaluation in expert domains \[[2](#bib.bib2)\], yet their application in on-policy training for expert-level reasoning is largely unexplored.

To address this gap, we explore a paradigm shift that introduces a middle ground between the simplicity of verifiable rewards and the expressiveness of preference rankings, which often come with human artifacts and operational overhead. We introduce Rubrics as Rewards (RaR), a framework for on-policy Reinforcement Learning that uses structured criteria or rubrics as the core reward mechanism. Rather than using rubrics only for evaluation \[[2](#bib.bib2), [30](#bib.bib30)\], we treat them as checklist-style supervision that produces reward signals for on-policy RL. Each rubric is composed of modular, interpretable subgoals that provide automatable feedback aligned with expert intent. By decomposing “what makes a good response” into tangible, human-interpretable criteria, rubrics offer a middle ground between binary correctness signals and coarse preference rankings.

![Refer to caption](2507.17746v2/rar_fig1.png)

Figure 1: Overview of Rubrics as Rewards (RaR). (i) Rubric Generation: We synthesize prompt-specific, self-contained rubric criteria using a strong LLM guided by four core design principles, with reference answers serving as proxies for expert supervision. (ii) GRPO Training: These rubrics are used to prompt an LLM judge for reward estimation, which drives policy optimization via the GRPO on-policy learning loop.

Previous works train generative reward models that learn to evaluate reasoning or final outputs with interpretable scores \[[5](#bib.bib5), [35](#bib.bib35), [1](#bib.bib1), [12](#bib.bib12)\], and some have even used a model’s internal confidence estimates as a proxy for reward \[[39](#bib.bib39)\]. More recent efforts have extended verifiable datasets beyond STEM domains, broadening the applicability of RLVR methods to a wider range of tasks \[[32](#bib.bib32), [23](#bib.bib23)\]. Yet a general-purpose approach for specifying reliable reward signals remains elusive, particularly in tasks without a single ground truth where both subjective and objective criteria must be considered. In contrast, we treat rubrics as instance-specific, reusable reward functions. Once generated, rubrics provide interpretable and automatable supervision that can be applied consistently across new rollouts, offering a scalable and transparent alternative to opaque reward modeling in on-policy learning.

Recent concurrent works explore checklists and principled rubric criteria for preference tuning and LLM safety \[[8](#bib.bib8), [33](#bib.bib33), [7](#bib.bib7)\], highlighting a growing trend toward structured supervision. In contrast, we convert rubrics into reward functions for on-policy RL, targeting expert reasoning and applied real-world domains. This closes the rubric-to-learning loop and improves performance on both rubric-guided evaluations and tasks with verifiable answers. Figure [1](#S1.F1 "Figure 1 ‣ 1 Introduction ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains") illustrates our framework.

Our key contributions are as follows: (i) We introduce Rubrics as Rewards (RaR), an on-policy reinforcement learning framework that uses checklist-style rubrics for multi-criteria supervision in reasoning and real-world domains. (ii) We synthesize instance-specific rubrics for medicine and science and release the corresponding training sets, RaR-Medicine ¹¹ 1 RaR-Medicine: [https://huggingface.co/datasets/anisha2102/RaR-Medicine](https://huggingface.co/datasets/anisha2102/RaR-Medicine) and RaR-Science ²² 2 RaR-Science: [https://huggingface.co/datasets/anisha2102/RaR-Science](https://huggingface.co/datasets/anisha2102/RaR-Science). (iii) RaR-trained models consistently outperform strong baselines and yield a stable, generalizable training signal, with gains on both rubric-scored and verifiable multiple-choice evaluation settings. (iv) Our results demonstrate that rubric-based rewards provide stable supervision across judge sizes, helping smaller models align effectively with human preferences and maintaining robust evaluation performance from small to large judges.

## 2 Rubrics as Rewards

### 2.1 Problem Formulation

Let $x$ denote an input prompt and $\hat{y} \sim \pi_{\theta}{( \cdot \mid x)}$ be a sampled response from a model parameterized by $\theta$. In domains without single ground-truth answers or automatic correctness signals, we define a structured reward function using instance-specific rubric criteria.

Each prompt $x$ is associated with a set of $k$ rubric items ${\{{(w_{j},c_{j})}\}}_{j = 1}^{k}$, where $w_{j} \in {\mathbb{R}}$ denotes the weight of criterion $j$, and $c_{j}:{{(x,\hat{y})}\mapsto{\{ 0,1\}}}$ is a binary correctness function that indicates whether the response $\hat{y}$ satisfies that criterion given the prompt.

### 2.2 Reward Aggregation Strategies

We investigate two complementary approaches for combining rubric feedback into scalar rewards:

#### Explicit Aggregation.

Each criterion is independently evaluated using an LLM-as-judge, and the final normalized reward is computed as:

|     |                                                                                                                     |     |     |
|-----|---------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $${r{(x,\hat{y})}} = \frac{{{\sum_{j = 1}^{k}w_{j}} \cdot c_{j}}\hspace{0pt}{(x,\hat{y})}}{\sum_{j = 1}^{k}w_{j}}$$ |     | (1) |

Normalization makes rewards comparable across prompts that differ in rubric count or weights. Although we use binary checks for $c_{j}$ in our experiments, the formulation can be extended to continuous-valued scores.

#### Implicit Aggregation.

All rubric criteria along with categorical weights are passed to an LLM-as-judge, delegating the aggregation to the model itself to produce a single scalar reward:

|     |                                                                                                                   |     |     |
|-----|-------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $${r_{\text{implicit}}\hspace{0pt}{(x,\hat{y})}} = {f_{\phi}\hspace{0pt}{(x,\hat{y},{\{ d_{j}\}}_{j = 1}^{k})}}$$ |     | (2) |

Here, $f_{\phi}$ denotes an LLM-based judge that takes the prompt $x$, the response $\hat{y}$, and the set of rubric criteria $\{ d_{j}\}$ as input. This formulation allows the model to compute a holistic reward score directly, avoiding the need to manually tune rubric weights.

The prompts used for each method are detailed in Appendix [A.6](#A1.SS6 "A.6 LLM-Judge Prompts ‣ Appendix A Appendix ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains").

### 2.3 Generalization of RLVR with Rubrics as Rewards

Rubric-based reinforcement learning extends the standard RLVR (Reinforcement Learning with Verifiable Rewards) setting by supporting multi-dimensional, prompt-specific evaluation criteria. We formalize this relationship below.

###### Remark 1 (Rubrics as Rewards subsumes RLVR).

The RLVR setting is a special case of rubric-based rewards defined in Equation [1](#S2.E1 "In Explicit Aggregation. ‣ 2.2 Reward Aggregation Strategies ‣ 2 Rubrics as Rewards ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains"), where $k = 1$, $w_{1} = 1$, and $c_{1}\hspace{0pt}{(x,\hat{y})}$ reduces to a single verifiable correctness function that compares the model output $\hat{y}$ against the known correct answer $y$. For example, this could involve exact match or test case execution. Formally:

|     |                                                                         |     |     |
|-----|-------------------------------------------------------------------------|-----|-----|
|     | $${r_{\text{RLVR}}\hspace{0pt}{(x,\hat{y})}} = {{match}{(y,\hat{y})}}$$ |     | (3) |

where ${{match}{(y,\hat{y})}} \in {\{{0,1}\}}$ indicates whether the response satisfies the verifiable correctness condition.

Rubric-based reward functions thus generalize RLVR by enabling multi-dimensional supervision, flexible weighting across criteria, and the incorporation of both objective and subjective aspects of response quality. This formalization highlights that RLVR can be seen as a restricted instance of rubric-guided RL with a single essential criterion. In contrast, rubric-based rewards further enable structured supervision in settings where correctness is multifaceted and may not be strictly verifiable.

## 3 Rubric Generation

### 3.1 Desiderata

A rubric specifies criteria for high-quality responses and provides human-interpretable supervision. We identify four desiderata for effective rubric generation:

#### Grounded in Expert Guidance.

Rubrics should reflect domain expertise by capturing the essential facts, reasoning steps, and conclusions necessary for correctness. Ideally, this grounding comes from human experts or their high-quality proxies.

#### Comprehensive Coverage.

Rubrics should span multiple dimensions of response quality, including factual accuracy, logical coherence, completeness, style, and safety. Negative criteria (pitfalls) help identify frequent or high-risk errors that undermine overall quality.

#### Criterion Importance.

Rubrics should reflect that some dimensions of response quality are more critical than others. For example, factual correctness must outweigh secondary aspects such as stylistic clarity. Assigning weights to criteria ensures this prioritization, whether through simple categorical tags, explicit numeric values, or learned weighting schemes.

#### Self-Contained Evaluation.

Each rubric item should be independently actionable, allowing either human annotators or automated judges to assess it in isolation without requiring external context or domain-specific knowledge.

### 3.2 Rubrics Creation

We apply these desiderata to datasets for reasoning tasks in medicine and science. Given the scarcity of human-annotated rubric datasets in these domains, we use LLMs to generate instance-specific rubrics from golden reference answers at scale, enabling the study of structured rewards without costly human annotation.

For each prompt, an LLM generates a rubric of 7–20 self-contained items. Each item is assigned both a numeric and a categorical weight reflecting its relative importance. While numeric weights provide fine-grained prioritization, in our experiments we adopt categorical labels (Essential, Important, Optional, Pitfall) for ease of implementation and interpretability in controlled settings. The resulting rubrics are then used directly as reward functions through either explicit aggregation (Eq. [1](#S2.E1 "In Explicit Aggregation. ‣ 2.2 Reward Aggregation Strategies ‣ 2 Rubrics as Rewards ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")) or implicit aggregation (Sec. [2.2](#S2.SS2 "2.2 Reward Aggregation Strategies ‣ 2 Rubrics as Rewards ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")).

In practice, we generate rubrics using OpenAI’s o3-mini and GPT-4o \[[24](#bib.bib24), [15](#bib.bib15), [14](#bib.bib14)\], conditioning generation on reference answers from the underlying datasets to approximate expert grounding. The resulting collections—RaR-Medicine and RaR-Science—are released for public use. These rubric sets supervise smaller policies under GRPO using both explicit and implicit reward aggregation.

## 4 Experiments

### 4.1 Datasets

We investigate the utility of rubrics as rewards across two reasoning domains, medicine and science.

- •
  RaR-Medicine: A dataset of 20k prompts drawn from diverse medical reasoning sources, including medical-o1-reasoning-SFT \[[3](#bib.bib3)\], natural_reasoning \[[37](#bib.bib37)\], SCP-116K \[[22](#bib.bib22)\], and GeneralThought-430K \[[9](#bib.bib9)\]. Instance-specific rubrics for this dataset are generated with GPT-4o (see Appendix [A.1](#A1.SS1 "A.1 Details of RaR-Medicine dataset ‣ Appendix A Appendix ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")).
- •
  RaR-Science: A dataset of $\sim$20k prompts curated to align with GPQA-Diamond categories. Prompts are sourced from natural_reasoning \[[37](#bib.bib37)\], SCP-116K \[[22](#bib.bib22)\], and GeneralThought-430K \[[9](#bib.bib9)\], covering a broad range of scientific reasoning tasks (Appendix [A.2](#A1.SS2 "A.2 Details of RaR-Science dataset ‣ Appendix A Appendix ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")). Rubrics for this dataset are synthesized with o3-mini.

### 4.2 Training Details

We conduct all experiments using on-policy reinforcement learning with the GRPO algorithm \[[28](#bib.bib28)\], taking Qwen2.5-7B as the base policy. Models are trained with a batch size of 96, a learning rate of $5 \times 10^{- 6}$, and a constant schedule with 10% linear warmup. Complete hyperparameter settings are listed in Appendix [11](#A1.T11 "Table 11 ‣ A.3 Training Details ‣ Appendix A Appendix ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains"). Training runs are executed on a single compute node equipped with 8 NVIDIA H100 GPUs.

Our training pipeline consists of the following key components:

Response Generation: For each prompt $q$, we sample $k = 16$ responses from the current policy $\pi_{\theta}$, using a context length of 3584 and a sampling temperature of 1.0.

Reward Computation with Rubrics: We use gpt-4o-mini as the judge model to assign rewards $R_{q}$ to the sampled responses. We experiment with various reward computation and aggregations strategies further described in Sections [4.3](#S4.SS3 "4.3 Rubric-Free Baselines ‣ 4 Experiments ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains") and [4.4](#S4.SS4 "4.4 Rubric-guided Methods ‣ 4 Experiments ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains").

Policy Update: The policy weights are updated using GRPO based on the computed rewards.

### 4.3 Rubric-Free Baselines

We consider various rubric-free baselines and off-the-shelf post-trained models. Rubric-free baselines are trained with Qwen2.5-7B as the base policy.

OFF-THE-SHELF:  
For off-the-shelf baselines we evaluate performance on Qwen2.5-7B. We also include the performance of Qwen2.5-7B-Instruct to compare with instruction-tuned variant of the base policy.

DIRECT-LIKERT:  
An LLM-as-judge provides a direct assessment for each response–prompt pair on a 1–10 Likert scale \[[40](#bib.bib40), [17](#bib.bib17)\], normalized to $\lbrack 0,1\rbrack$. The resulting score is used directly as the reward signal for training.

REFERENCE-LIKERT:  
An LLM-as-judge compares the generated response against a reference answer (written by experts or stronger LLMs) and assigns a 1–10 Likert score \[[40](#bib.bib40)\], normalized to $\lbrack 0,1\rbrack$. This reference-guided score is used as the reward signal for policy updates. The reward for each (prompt, response, reference) triplet is defined as:

|     |                                                                                                        |     |
|-----|--------------------------------------------------------------------------------------------------------|-----|
|     | $${R_{\text{ref}}\hspace{0pt}{(q,x)}} = {{Norm}{({\text{LikertScore}\hspace{0pt}{(q,x,x^{\ast})}})}}$$ |     |

where $x^{\ast}$ denotes the reference answer.

### 4.4 Rubric-guided Methods

RaR-PREDEFINED:  
This method uses a fixed set of generic rubrics for all prompts (e.g. response is concise, response contains correct information). It employs the Explicit Aggregation method (Equation [1](#S2.E1 "In Explicit Aggregation. ‣ 2.2 Reward Aggregation Strategies ‣ 2 Rubrics as Rewards ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")) with all criteria weighted uniformly (see Appendix [A.5](#A1.SS5 "A.5 Predefined Static Rubrics ‣ Appendix A Appendix ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")).

RaR-EXPLICIT:  
This variant also uses Explicit Aggregation using a weighted sum (Equation [1](#S2.E1 "In Explicit Aggregation. ‣ 2.2 Reward Aggregation Strategies ‣ 2 Rubrics as Rewards ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")) but applies it to instance-specific rubrics from Section [3](#S3 "3 Rubric Generation ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains"). We manually assign numerical weights based on the generated categorical labels: {"Essential": 1.0, "Important": 0.7, "Optional": 0.3, "Pitfall": 0.9}³³ 3 Pitfall criteria are phrased in positive form (e.g., “The response avoids misinformation”), so satisfying them contributes positively to the score. If a pitfall is not satisfied, the corresponding reward is reduced or penalized..

RaR-IMPLICIT:  
This variant uses the Implicit Aggregation method (Equation [2](#S2.E2 "In Implicit Aggregation. ‣ 2.2 Reward Aggregation Strategies ‣ 2 Rubrics as Rewards ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")). It leverages prompt-specific rubrics, where a judge model evaluates the response as a whole to assign a single Likert rating (1–10), avoiding the need for hand-tuned weights. The reward is normalized to the $\lbrack 0,1\rbrack$ range during training.

### 4.5 Evaluation Setup

#### Rubric-Based Evaluation

We evaluate models trained with RaR-Medicine on HealthBench \[[2](#bib.bib2)\], a benchmark of 5,000 clinical conversations designed to assess model safety and helpfulness in realistic medical scenarios. Performance is measured using detailed, physician-authored rubrics. We generate responses with greedy decoding (temperature = 0) and report both overall scores and per-axis scores following the original setup. For ablation studies, we sample a subset of 1,000 prompts (hereafter referred as HealthBench-1k) and use the rest for training.

#### Multiple-Choice Evaluation

Each model is evaluated across 10 independent runs, using greedy decoding (temperature=0) to sample one response per prompt. Answer choices are permuted per example to reduce positional bias, and outputs are parsed for boxed answer formats (e.g., boxed{A}). If extraction fails, we fall back to a GPT-4o verifier that checks whether the response contains the correct option letter or text (see Appendix [A.4](#A1.SS4 "A.4 Evaluation Prompts ‣ Appendix A Appendix ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains")). Final accuracy is reported as the mean over 10 runs, and we include 95% confidence intervals to account for run-to-run variance.

Figure 2: Performance of baselines and RaR (*Rubrics as Rewards*) variants for the medicine and science domains. HealthBench (left): shows per-axis scores across five core axes, with a thin dashed gray line indicating the overall score (all values shown as percentages). GPQA-Diamond (right): mean accuracy over 10 runs; error bars represent 95% confidence intervals. All policies are evaluated using gpt-4o-mini as the LLM-as-Judge. Across both domains, RaR-Implicit consistently outperforms Direct-Likert and demonstrates a competitive advantage over Reference-Likert.

#### LLM-Judge Alignment Evaluation

To measure how well LLM judges align with human preferences, we build a paired evaluation set from roughly 3,000 HealthBench prompts. For each prompt, we take the practitioner-approved answer as the *preferred* response and create a *perturbed* alternative via controlled edits (see Appendix [A.9](#A1.SS9 "A.9 Perturbed Dataset Generation ‣ Appendix A Appendix ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains") for method used for perturbation and prompt selection). The metric is *pairwise preference accuracy* i.e. the fraction of pairs where the preferred response scores higher reported across judge models of varying sizes.

## 5 Results

We now present the main findings of our study.

#### Rubrics as Rewards shows strong gains across evaluation settings.

Table [2](#S4.F2 "Figure 2 ‣ Multiple-Choice Evaluation ‣ 4.5 Evaluation Setup ‣ 4 Experiments ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains") reports results on HealthBench (rubric-based, free-form) and GPQA-Diamond (multiple-choice). RaR-Implicit consistently outperforms Direct-Likert, with relative gains up to 31% on HealthBench and 7% on GPQA. Both rubric-guided variants achieve higher scores than the base and instruction-tuned policies. Gains on GPQA-Diamond show that rubric-induced skills generalize beyond rubric-based evaluation. The RaR-Predefined variant, which applies a fixed list of generic rubrics to every prompt (no instance-specific synthesis), underperforms because generic criteria miss prompt-specific requirements and common failure modes, producing misaligned reward signals. Hence, effective training requires instance-specific rubric synthesis as they better capture task context and typical failure modes.

Beyond these gains, RaR-Implicit also shows small but consistent gains over Reference-Likert. In our setup, rubrics are generated with stronger LLMs using reference answers as proxies for expert supervision, so rubric quality is impacted by reference quality. Even so, converting open-ended answers into explicit criteria yields effective, well-aligned reward signals.

Between the two rubric-guided methods, RaR-Implicit attains the strongest results overall; fixed weighted sums in RaR-Explicit offer more control but can be brittle. Explicit weighting can be difficult to tune but offers greater interpretability; we view the choice as application-dependent and leave it to practitioners. Future work could explore learned or dynamic weighting strategies that maintain interpretability while improving adaptability.

![Refer to caption](2507.17746v2/figs/llm_judge_line_comparison.png)

Figure 3: Alignment Study of LLM Judges across Model Scales. Rubrics as Rewards (orange) consistently improves alignment with human preferences across LLM judge sizes compared to direct Likert-based scoring (blue). Judge Alignment using synthetic rubrics without expert grounding (green) outperform the direct Likert baseline, but still fall short of expert-grounded rubrics (orange). The rubric structure especially benefits smaller judge models, helping them close the gap with larger models when guided by checklist-style criteria.

#### Rubrics enhance alignment with human preferences across model scales

We evaluate alignment with humans by having LLM judges of varying sizes score chosen vs. rejected HealthBench-1k responses on a 1–10 scale under two settings: (i) rubric-guided (RaR-IMPLICIT), where the instance-specific rubric is provided, and (ii) rubric-free (DIRECT-LIKERT), where only the prompt and answers are shown. Figure [3](#S5.F3 "Figure 3 ‣ Rubrics as Rewards shows strong gains across evaluation settings. ‣ 5 Results ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains") reports *pairwise preference accuracy* (the fraction of pairs where the preferred response receives the higher score). Rubric guidance improves accuracy for every judge size, with the largest gains for smaller judges, narrowing the gap to larger models. This indicates that explicit, context-specific criteria help judges distinguish subtle quality differences better than direct Likert scoring. Further analysis of judge-scale effects on GRPO training is detailed in Appendix [A.8](#A1.SS8 "A.8 Judge Quality impacts on Post-training ‣ Appendix A Appendix ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains").

#### Expert guidance is crucial for synthetic rubric generation

Human guidance significantly influences the effectiveness of rubrics in capturing subtle human preferences. Figure [3](#S5.F3 "Figure 3 ‣ Rubrics as Rewards shows strong gains across evaluation settings. ‣ 5 Results ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains") highlights performance differences between rubric-based evaluations that include reference answers and those without them. The data shows that rubrics developed with reference answers achieve higher accuracy, emphasizing that human insights integrated during rubric generation enable granular criteria and improved alignment with human preferences.

| Training Method              | Overall Score |
|------------------------------|---------------|
| Expert-Answer-SFT            | 20.4%         |
| Simple-Likert                | 23.9%         |
| Reference-Likert             | 31.7%         |
| RaR-Implicit-Synthetic-NoRef | 32.0%         |
| RaR-Implicit-Synthetic       | 35.9%         |
| RaR-Implicit-Human           | 34.8%         |

Table 1: Evaluation on HealthBench: Comparison of human- vs. synthetic-generated rubrics (with and without reference answers). RaR methods trained with GRPO significantly outperform Likert-only, Reference-based-likert and SFT baselines. Synthetic rubrics generated without access to reference answers perform notably worse, highlighting the importance of human-grounded guidance. Notably, human-authored rubrics and synthetic rubrics with access to references yield comparable performance.

| Ablation Setting       | Overall Score |
|------------------------|---------------|
| Essential-Only Rubrics | 34.9%         |
| No Categorical Labels  | 38.8%         |
| No Pitfall Criteria    | 37.2%         |
| All Rubrics            | 37.2%         |

Table 2: Ablation results for elements of rubric design on HealthBench-1k (trained on HealthBench-3.5k subset with Qwen2.5-7B base policy). Rubrics generated using o3-mini with access to reference answers.

## 6 Ablations

| Rubric Generation Model          | Overall Score |
|----------------------------------|---------------|
| O3-mini (Rubrics with reference) | 35.9%         |
| GPT-4o                           | 34.2%         |
| GPT-4o-mini                      | 32.7%         |
| O3-mini                          | 32.4%         |
| Qwen-72B-Instruct                | 32.7%         |
| Qwen-32B-Instruct                | 31.1%         |
| Qwen-7B-Instruct                 | 31.9%         |

Table 3: Policy performance on HealthBench-1k when trained with GRPO using rubrics generated by different LLMs *without* reference answers. GPT-4o-generated rubrics yield the strongest performance, though they still fall short of rubrics generated with expert (reference-guided) supervision. Smaller aligned models (e.g., GPT-4o-mini, O3-mini) remain competitive with larger open-weight models, underscoring the importance of alignment and reasoning ability in rubric generation.

#### Impact of Rubric Generation Strategies in Real-World Domains

How does the method of rubric generation affect downstream training in challenging, real-world settings? To investigate this, we hold out HealthBench-1k for evaluation and use 3.5k prompts from the remaining HealthBench pool to generate rubrics for training as it has access to human generated rubrics. Results are summarized in Table [1](#S5.T1 "Table 1 ‣ Expert guidance is crucial for synthetic rubric generation ‣ 5 Results ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains").

In-domain testing on HealthBench-1k amplifies RaR’s gains: every instance-specific rubric-based method outperforms rubric-free baselines. Notably, even the weakest RaR variant significantly surpasses Reference-Likert, underscoring the advantage of structured supervision in subjective, open-ended domains like healthcare. We attribute this to the finer granularity and clarity rubrics provide in assigning rewards-especially when correctness is not binary and answers may vary in tone, completeness, or safety relevance.

Moreover, we find that rubric quality is crucial: synthetic rubrics generated with reference-answer guidance consistently outperform those generated without it. This highlights the importance of incorporating expert signal, whether via human-in-the-loop annotations or high-quality reference completions, for generating effective and aligned rubrics. Purely synthetic rubrics, while scalable, currently fall short in capturing the subtle criteria required for robust training in high-stakes domains.

#### Elements of Rubric Design

This ablation study examines how the structure and weighting of synthetic rubrics affect downstream performance on HealthBench-1k. As shown in Table [2](#S5.T2 "Table 2 ‣ Expert guidance is crucial for synthetic rubric generation ‣ 5 Results ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains"), rubrics that include a broader range of criteria outperform those limited to essential checks, suggesting that richer evaluation signals lead to better learning. Interestingly, we observe minimal performance differences when including rubric weights or pitfall criteria during training. One possible explanation is that synthetically generating effective pitfall criteria is inherently difficult, as it requires anticipating the most common or critical failure modes of the model, a task that often demands human intuition and domain expertise. As a result, these synthetic negative criteria may lack the specificity or relevance needed to meaningfully penalize undesirable responses.

#### Impact of LLM Expertise on Rubric Quality

To assess how the capabilities of rubric-generating LLMs affect downstream performance, we generate synthetic rubrics without access to reference answers and use them to train policies on HealthBench. This isolates the effect of LLM quality on reference-free rubric utility. Specifically, we evaluate on the HealthBench-1k subset, using models trained on rubrics generated for the remaining 4k training examples from HealthBench.

As shown in Table [3](#S6.T3 "Table 3 ‣ 6 Ablations ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains"), larger or more capable LLMs generally produce more effective rubrics, with GPT-4o yielding the best performance among reference-free models. However, all remain below the performance of rubrics generated with reference guidance (e.g., O3-mini with access to reference answers). Additionally, model attributes such as instruction tuning and reasoning capabilities play a key role in the effectiveness of rubric generation.

## 7 Related Work

#### RLVR across domains

Reinforcement learning with verifiable rewards (RLVR) is expanding beyond math and code. General-Reasoner trains on a 200k mixed corpus spanning physics, finance, and policy, and reports a ten-point gain on MMLU-Pro after GRPO fine-tuning \[[23](#bib.bib23)\]. A follow-up extends RLVR to medicine, chemistry, psychology, and economics, showing that a single cross-domain reward model can supervise all four without task-specific tweaks \[[31](#bib.bib31)\]. In healthcare, Med-RLVR applies similar methods to multiple-choice clinical QA, improving accuracy over supervised baselines while eliciting chain-of-thought from a 3B base model \[[38](#bib.bib38)\]. These results indicate steady progress, yet sparse signals, verifier reliability, and limited benchmark coverage remain open challenges.

#### Rubrics for evaluation and training

Task-specific rubrics are increasingly used to evaluate LLMs in difficult-to-verify domains \[[2](#bib.bib2), [27](#bib.bib27), [13](#bib.bib13), [26](#bib.bib26)\]. Pathak et al. show that rubric-prompted LLM graders are more accurate and consistent than a question-agnostic checklist \[[26](#bib.bib26)\]. HealthBench scales this idea in medicine, pairing 48k clinician-written criteria with GPT-4 judges to score various axes \[[2](#bib.bib2)\]. Beyond evaluation, rubrics are used to condition preference pairs for DPO (CPT; \[[8](#bib.bib8)\]) and to guide checklist-based preference tuning in safety, instruction-following, and creative-writing settings \[[33](#bib.bib33), [7](#bib.bib7), [18](#bib.bib18)\]. These lines of work primarily use rubrics to grade outputs or to condition preference data, often in non-reasoning domains such as safety, instruction following, or creative writing. In contrast, we use rubric criteria directly as reward signals for on-policy RL in expert-reasoning and real-world domains.

#### Learning from feedback signals

RLHF trains policies with large numbers of human comparisons, which introduces subjectivity and can lead to reward hacking \[[25](#bib.bib25)\]. RLVR reduces these issues by using programmatic checks, from exact matches on GSM8K and MATH to mixed-domain verifiers in General-Reasoner and Cross-Domain RLVR \[[23](#bib.bib23), [31](#bib.bib31)\], although signals can be sparse. Process supervision \[[21](#bib.bib21)\] provides denser guidance via step-level labels, and MCTS-generated annotations or generative reward models such as ThinkPRM improve performance, but with high annotation cost \[[20](#bib.bib20), [16](#bib.bib16)\]. Rubric-based RL finds a middle ground by turning multiple rubric criteria into structured verifiers and using their scalar scores as denser rewards.

## 8 Conclusion

We introduced Rubrics as Rewards (RaR), a framework for post-training language models using structured, checklist-style rubrics as reward signals. By decomposing response evaluation into transparent, multi-criteria objectives—both subjective and objective—RaR provides a modular and interpretable alternative to preference-based methods. Our experiments demonstrate that rubric-guided training achieves strong performance across domains, significantly outperforming Likert-based baselines and matching or exceeding the performance of reference-based reward generation. Additionally, we show that RaR improves alignment with human preferences while reducing dependence on large judge models.

## 9 Limitations and Future Work

Our work focuses on medicine and science to enable controlled experiments. This choice allows us to run controlled experiments, but broader validation across dialogue, tool use, or other agentic tasks remains an important direction. We evaluate only two reward aggregation strategies, implicit and explicit, since they capture complementary extremes of flexibility and control; future work could explore more advanced ways of combining rubric criteria, such as learning continuous weights for each criterion or dynamically adjusting weights over the course of training to mimic a curriculum (e.g., prioritizing essential correctness early, then gradually emphasizing more subtle qualities like style or safety). Finally, we use off-the-shelf LLMs as judges for accessibility and reproducibility; exploring specialized evaluators with stronger reasoning or generative reward models may yield further gains.

## Acknowledgments

We thank Qin Lyu, Nikhil Barhate, and Zijian Hu for supporting this research through the development of the in-house post-training platform RLXF. We also thank Robert Vacareanu for valuable early feedback and discussions.

## References

- \[1\] D. Anugraha, Z. Tang, L. J. V. Miranda, H. Zhao, M. R. Farhansyah, G. Kuwanto, D. Wijaya, and G. I. Winata. R3: Robust rubric-agnostic reward models. *arXiv preprint arXiv:2505.13388*, 2025.
- \[2\] R. K. Arora, J. Wei, R. S. Hicks, P. Bowman, J. Quiñonero-Candela, F. Tsimpourlas, M. Sharman, M. Shah, A. Vallone, A. Beutel, et al. Healthbench: Evaluating large language models towards improved human health. *arXiv preprint arXiv:2505.08775*, 2025.
- \[3\] J. Chen, Z. Cai, K. Ji, X. Wang, W. Liu, R. Wang, J. Hou, and B. Wang. Huatuogpt-o1, towards medical complex reasoning with llms. *arXiv preprint arXiv:2412.18925*, 2024a.
- \[4\] L. Chen, C. Zhu, D. Soselia, J. Chen, T. Zhou, T. Goldstein, H. Huang, M. Shoeybi, and B. Catanzaro. Odin: Disentangled reward mitigates hacking in rlhf. *arXiv preprint arXiv:2402.07319*, 2024b.
- \[5\] X. Chen, G. Li, Z. Wang, B. Jin, C. Qian, Y. Wang, H. Wang, Y. Zhang, D. Zhang, T. Zhang, et al. Rm-r1: Reward modeling as reasoning. *arXiv preprint arXiv:2505.02387*, 2025.
- \[6\] G. Cui, L. Yuan, Z. Wang, H. Wang, W. Li, B. He, Y. Fan, T. Yu, Q. Xu, W. Chen, et al. Process reinforcement through implicit rewards. *arXiv preprint arXiv:2502.01456*, 2025.
- \[7\] J. Dineen, A. RRV, Q. Liu, Z. Xu, X. Ye, M. Shen, Z. Li, S. Lu, C. Baral, M. Chen, et al. Qa-lign: Aligning llms through constitutionally decomposed qa. *arXiv preprint arXiv:2506.08123*, 2025.
- \[8\] V. Gallego. Configurable preference tuning with rubric-guided synthetic data. *arXiv preprint arXiv:2506.11702*, 2025.
- \[9\] General Reasoning. General reasoning, 2025. URL [https://gr.inc/](https://gr.inc/).
- \[10\] A. Gudibande, E. Wallace, C. Snell, X. Geng, H. Liu, P. Abbeel, S. Levine, and D. Song. The false promise of imitating proprietary llms. *arXiv preprint arXiv:2305.15717*, 2023.
- \[11\] D. Guo, D. Yang, H. Zhang, J. Song, R. Zhang, R. Xu, Q. Zhu, S. Ma, P. Wang, X. Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. *arXiv preprint arXiv:2501.12948*, 2025a.
- \[12\] J. Guo, Z. Chi, L. Dong, Q. Dong, X. Wu, S. Huang, and F. Wei. Reward reasoning model. *arXiv preprint arXiv:2505.14674*, 2025b.
- \[13\] H. Hashemi, J. Eisner, C. Rosset, B. Van Durme, and C. Kedzie. Llm-rubric: A multidimensional, calibrated approach to automated evaluation of natural language texts. *arXiv preprint arXiv:2501.00274*, 2024.
- \[14\] A. Hurst, A. Lerer, A. P. Goucher, A. Perelman, A. Ramesh, A. Clark, A. Ostrow, A. Welihinda, A. Hayes, A. Radford, et al. Gpt-4o system card. *arXiv preprint arXiv:2410.21276*, 2024.
- \[15\] A. Jaech, A. Kalai, A. Lerer, A. Richardson, A. El-Kishky, A. Low, A. Helyar, A. Madry, A. Beutel, A. Carney, et al. Openai o1 system card. *arXiv preprint arXiv:2412.16720*, 2024.
- \[16\] M. Khalifa, R. Agarwal, L. Logeswaran, J. Kim, H. Peng, M. Lee, H. Lee, and L. Wang. Process reward models that think. *arXiv preprint arXiv:2504.16828*, 2025.
- \[17\] S. Kim, J. Suk, S. Longpre, B. Y. Lin, J. Shin, S. Welleck, G. Neubig, M. Lee, K. Lee, and M. Seo. Prometheus 2: An open source language model specialized in evaluating other language models. *arXiv preprint arXiv:2405.01535*, 2024.
- \[18\] Z. M. Kim, C. Park, V. Raheja, S. Kim, and D. Kang. Toward evaluative thinking: Meta policy optimization with evolving reward models. *arXiv preprint arXiv:2504.20157*, 2025.
- \[19\] N. Lambert, J. Morrison, V. Pyatkin, S. Huang, H. Ivison, F. Brahman, L. J. V. Miranda, A. Liu, N. Dziri, S. Lyu, et al. T$\backslash$" ulu 3: Pushing frontiers in open language model post-training. *arXiv preprint arXiv:2411.15124*, 2024.
- \[20\] S. Li, S. Dong, K. Luan, X. Di, and C. Ding. Enhancing reasoning through process supervision with monte carlo tree search. *arXiv preprint arXiv:2501.01478*, 2025.
- \[21\] H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J. Schulman, I. Sutskever, and K. Cobbe. Let’s verify step by step. In *The Twelfth International Conference on Learning Representations*, 2023.
- \[22\] D. Lu, X. Tan, R. Xu, T. Yao, C. Qu, W. Chu, Y. Xu, and Y. Qi. Scp-116k: A high-quality problem-solution dataset and a generalized pipeline for automated extraction in the higher education science domain. *arXiv preprint arXiv:2501.15587*, 2025.
- \[23\] X. Ma, Q. Liu, D. Jiang, G. Zhang, Z. Ma, and W. Chen. General-reasoner: Advancing llm reasoning across all domains. *arXiv preprint arXiv:2505.14652*, 2025.
- \[24\] OpenAI o3-mini. Openai o3-min, 2025. URL [https://openai.com/index/openai-o3-mini/](https://openai.com/index/openai-o3-mini/).
- \[25\] L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray, et al. Training language models to follow instructions with human feedback. *Advances in neural information processing systems*, 35:27730–27744, 2022.
- \[26\] A. Pathak, R. Gandhi, V. Uttam, Y. Nakka, A. R. Jindal, P. Ghosh, A. Ramamoorthy, S. Verma, A. Mittal, A. Ased, et al. Rubric is all you need: Enhancing llm-based code evaluation with question-specific rubrics. *arXiv preprint arXiv:2503.23989*, 2025.
- \[27\] J. Ruan, I. Nair, S. Cao, A. Liu, S. Munir, M. Pollens-Dempsey, T. Chiang, L. Kates, N. David, S. Chen, et al. Expertlongbench: Benchmarking language models on expert-level long-form generation tasks with structured checklists. *arXiv preprint arXiv:2506.01241*, 2025.
- \[28\] Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang, Y. Li, Y. Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. *arXiv preprint arXiv:2402.03300*, 2024.
- \[29\] P. Singhal, T. Goyal, J. Xu, and G. Durrett. A long way to go: Investigating length correlations in rlhf. *arXiv preprint arXiv:2310.03716*, 2023.
- \[30\] V. Sirdeshmukh, K. Deshpande, J. Mols, L. Jin, E.-Y. Cardona, D. Lee, J. Kritz, W. Primack, S. Yue, and C. Xing. Multichallenge: A realistic multi-turn conversation evaluation benchmark challenging to frontier llms. *arXiv preprint arXiv:2501.17399*, 2025.
- \[31\] Y. Su, D. Yu, L. Song, J. Li, H. Mi, Z. Tu, M. Zhang, and D. Yu. Crossing the reward bridge: Expanding rl with verifiable rewards across diverse domains. *arXiv preprint arXiv:2503.23829*, 2025a.
- \[32\] Y. Su, D. Yu, L. Song, J. Li, H. Mi, Z. Tu, M. Zhang, and D. Yu. Expanding rl with verifiable rewards across diverse domains. *arXiv preprint arXiv:2503.23829*, 2025b.
- \[33\] V. Viswanathan, Y. Sun, S. Ma, X. Kong, M. Cao, G. Neubig, and T. Wu. Checklists are better than reward models for aligning language models. *arXiv preprint arXiv:2507.18624*, 2025.
- \[34\] H. Wang, Y. Lin, W. Xiong, R. Yang, S. Diao, S. Qiu, H. Zhao, and T. Zhang. Arithmetic control of llms for diverse user preferences: Directional preference alignment with multi-objective rewards. *arXiv preprint arXiv:2402.18571*, 2024.
- \[35\] C. Whitehouse, T. Wang, P. Yu, X. Li, J. Weston, I. Kulikov, and S. Saha. J1: Incentivizing thinking in llm-as-a-judge via reinforcement learning. *arXiv preprint arXiv:2505.10320*, 2025.
- \[36\] Z. Ye, F. Greenlee-Scott, M. Bartolo, P. Blunsom, J. A. Campos, and M. Gallé. Improving reward models with synthetic critiques. *arXiv preprint arXiv:2405.20850*, 2024.
- \[37\] W. Yuan, J. Yu, S. Jiang, K. Padthe, Y. Li, I. Kulikov, K. Cho, D. Wang, Y. Tian, J. E. Weston, et al. Naturalreasoning: Reasoning in the wild with 2.8 m challenging questions. *arXiv preprint arXiv:2502.13124*, 2025.
- \[38\] S. Zhang, Q. Liu, G. Qin, T. Naumann, and H. Poon. Med-rlvr: Emerging medical reasoning from a 3b base model via reinforcement learning. *arXiv preprint arXiv:2502.19655*, 2025.
- \[39\] X. Zhao, Z. Kang, A. Feng, S. Levine, and D. Song. Learning to reason without external rewards. *arXiv preprint arXiv:2505.19590*, 2025.
- \[40\] L. Zheng, W.-L. Chiang, Y. Sheng, S. Zhuang, Z. Wu, Y. Zhuang, Z. Lin, Z. Li, D. Li, E. Xing, et al. Judging llm-as-a-judge with mt-bench and chatbot arena. *Advances in neural information processing systems*, 36:46595–46623, 2023.

## Appendix A Appendix

### A.1 Details of RaR-Medicine dataset

The following is illustrates an example from the RaR-Medicine dataset with more details about statistics and categorical distribution of rubrics listed in Table [4](#A1.T4 "Table 4 ‣ A.1 Details of RaR-Medicine dataset ‣ Appendix A Appendix ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains") and [6](#A1.T6 "Table 6 ‣ A.1 Details of RaR-Medicine dataset ‣ Appendix A Appendix ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains").

![](img)

| Metric                       | Value  |
|------------------------------|--------|
| Total examples               | 20,166 |
| Avg. rubrics per question    | 7.5    |
| Avg. question length (words) | 45.0   |

Table 4: Aggregate statistics for the RaR-Medicine dataset (train and validation) dataset.

| Rubric Type | Count  | Percent |
|-------------|--------|---------|
| Important   | 52,748 | 34.1    |
| Essential   | 47,584 | 30.7    |
| Optional    | 34,261 | 22.1    |
| Pitfall     | 20,215 | 13.1    |

Table 5: Rubric-type distribution across all 20,166 examples.

| Topics                     | Count  | Percent |
|----------------------------|--------|---------|
| Total examples             | 20,166 | 100.0   |
| Medical Diagnosis          | 10,147 | 50.3    |
| Medical Treatment          | 3,235  | 16.0    |
| Medical Knowledge          | 2,557  | 12.7    |
| Medical Diag. and Mngmnt   | 2,033  | 10.1    |
| Medical Biology            | 770    | 3.8     |
| Other                      | 428    | 2.1     |
| Medical Ethics             | 377    | 1.9     |
| Health Physics             | 276    | 1.4     |
| Epidemiology & Pub. Health | 216    | 1.1     |
| General Medicine           | 113    | 0.6     |
| Forensic Medicine          | 14     | 0.1     |

Table 6: Distribution of topics in the medical training and validation dataset

### A.2 Details of RaR-Science dataset

This section shows an illustrative example from the RaR-Science dataset with more details about statistics and categorical distibution of rubrics listed in Table [7](#A1.T7 "Table 7 ‣ A.2 Details of RaR-Science dataset ‣ Appendix A Appendix ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains"), [8](#A1.T8 "Table 8 ‣ A.2 Details of RaR-Science dataset ‣ Appendix A Appendix ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains"), [9](#A1.T9 "Table 9 ‣ A.3 Training Details ‣ Appendix A Appendix ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains").

![](img)

| Metric                       | Value  |
|------------------------------|--------|
| Total examples               | 20,625 |
| Avg. rubrics per question    | 7.5    |
| Avg. question length (words) | 52.6   |

Table 7: Aggregate statistics for the full medical (train and validation) dataset.

| Rubric Type | Count  | Percent |
|-------------|--------|---------|
| Important   | 52,315 | 34.8    |
| Essential   | 42,739 | 28.4    |
| Optional    | 33,622 | 22.3    |
| Pitfall     | 21,808 | 14.5    |

Table 8: Rubric-type distribution across all 20 625 examples.

### A.3 Training Details

The training hyperparameters are described in Table [10](#A1.T10 "Table 10 ‣ A.3 Training Details ‣ Appendix A Appendix ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains").

| Topics                   | Count | Percent |
|--------------------------|-------|---------|
| Total examples           | 20625 | 100.0   |
| General Chemistry        | 3163  | 15.3    |
| Quantum Mechanics        | 3158  | 15.3    |
| Physical Chemistry       | 2761  | 13.4    |
| Statistical Mechanics    | 2530  | 12.3    |
| Organic Chemistry        | 2059  | 10.0    |
| General Physics          | 1439  | 7.0     |
| Condensed Matter Physics | 1387  | 6.7     |
| Genetics                 | 1378  | 6.7     |
| Molecular Biology        | 815   | 4.0     |
| Astrophysics             | 409   | 2.0     |
| Inorganic Chemistry      | 407   | 2.0     |
| Analytical Chemistry     | 398   | 1.9     |
| Electromagnetism         | 239   | 1.2     |
| Optics                   | 143   | 0.7     |
| High Energy Physics      | 116   | 0.6     |
| Electromagnetic Theory   | 105   | 0.5     |
| Electromagnetics         | 72    | 0.3     |
| Relativistic Mechanics   | 46    | 0.2     |

Table 9: Distribution of topics in the STEM training and validation dataset

|                         |                      |     |
|-------------------------|----------------------|-----|
| Hyperparameters         |                      |     |
| num_rollouts_per_prompt | 16                   |     |
| batch_size (effective)  | 96                   |     |
| sampling_temperature    | 1.0                  |     |
| warmup_ratio            | 0.1                  |     |
| learning_rate           | 5.0e-06              |     |
| lr_scheduler_type       | constant_with_warmup |     |
| max_length              | 3584                 |     |
| num_train_steps         | 300                  |     |

Table 10: GRPO hyperparameter settings for Medical and Science domains.

| Judge Model       | RaR-Implicit | Direct-Likert |
|-------------------|--------------|---------------|
| GPT-4o-mini       | 27.9%        | 25.3%         |
| Qwen-32B-Instruct | 26.2%        | 25.4%         |
| Qwen-14B-Instruct | 25.0%        | 24.9%         |
| Qwen-7B-Instruct  | 26.7%        | 22.0%         |

Table 11: Judge quality comparison: rubric-based evaluation vs pure Likert scoring on synthetic medical rubrics.

Rubric-based evaluation consistently yields stronger policies across all judge sizes. The most pronounced improvement appears with Qwen-7B-Instruct (+0.047), where rubric guidance lifts it from weakest to nearly matching larger models. Additionally, rubric-based scores are more tightly clustered (0.250–0.279) than those from Likert-only judges (0.220–0.254), indicating improved consistency.

These results suggest that rubrics help smaller judges approximate high-quality supervision by breaking evaluation into interpretable, binary criteria. This structured approach mitigates scale-related limitations, enabling more reliable reward modeling even with limited-capacity evaluators.

### A.4 Evaluation Prompts

![](img)

### A.5 Predefined Static Rubrics

![](img)

### A.6 LLM-Judge Prompts

![](img)

![](img)

![](img)

### A.7 Synthetic Preference Set Generation

We leverage the publicly-released HealthBench \[[2](#bib.bib2)\] corpus, which contains 5,000 health-related prompts accompanied by expert-written answers. Of these, 4,203 datapoints already include an *ideal* completion vetted by licensed clinicians. For every such prompt–ideal pair we automatically generate a *perturbed* counterpart using o3 with the structured template shown below. The template forces the model to (i) spell out a \[reasoning\] plan for degrading quality, (ii) emit the degraded \[perturbed_completion\], and (iii) log exact \[chunks_added\] and \[chunks_removed\]. Perturbations are accepted only after manual screening confirms that they are *objectively worse*, along at least one axis of medical accuracy, completeness, clarity, safety, specificity, structure, or tone, while remaining coherent and free of dangerous advice. We further exclude the prompts from HealthBench-1k used for ablations. This procedure produces a balanced evaluation set of 3,027 preferred and 3,027 perturbed responses (6,054 total), which we use in the rubric-versus-Likert experiments in Section [5](#S5 "5 Results ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains"). The prompt used for this generation is detailed in Figure [A.9](#A1.SS9 "A.9 Perturbed Dataset Generation ‣ Appendix A Appendix ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains").

### A.8 Judge Quality impacts on Post-training

We assess whether rubric-guided evaluation improves judge effectiveness compared to rubric-free Likert scoring when used for GRPO training. Table [11](#A1.T11 "Table 11 ‣ A.3 Training Details ‣ Appendix A Appendix ‣ Rubrics as Rewards: Reinforcement Learning Beyond Verifiable Domains") reports judge accuracy on synthetic medical data, with all policies trained using Qwen2.5-7B and varying judge models.

![](img)

![](img)

### A.9 Perturbed Dataset Generation

![](img)

Experimental support, please [view the build logs](./2507.17746v2/__stdout.txt) for errors. Generated by [ L A T E xml ![\[LOGO\]](img)](https://math.nist.gov/~BMiller/LaTeXML/) .

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
