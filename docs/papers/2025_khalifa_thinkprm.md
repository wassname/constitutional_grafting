---
title: "Process Reward Models That Think"
authors: "Muhammad Khalifa; Rishabh Agarwal; Lajanugen Logeswaran; Jaekyeom Kim; Hao Peng; Moontae Lee; Honglak Lee; Lu Wang"
year: 2025
source: https://arxiv.org/html/2504.16828
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

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) [![](img) Report Issue](# "Report an Issue") [![](img) Back to Abstract](/abs/2504.16828v5 "Back to abstract page") [![](img) Download PDF](/pdf/2504.16828v5 "Download PDF") [![](img)](javascript:toggleNavTOC(); "Toggle navigation") [![](img)](javascript:toggleReadingMode(); "Disable reading mode, show header and footer")

![](img) ![](img) ![](img)

1.  [Abstract](#abstract1 "In Process Reward Models That Think")
2.  [1 Introduction](#S1 "In Process Reward Models That Think")
3.  [2 Background and Related Work](#S2 "In Process Reward Models That Think")
    1.  [Discriminative PRMs.](#S2.SS0.SSS0.Px1 "In 2 Background and Related Work ‣ Process Reward Models That Think")
    2.  [Generative Verification.](#S2.SS0.SSS0.Px2 "In 2 Background and Related Work ‣ Process Reward Models That Think")
    3.  [Test-Time Scaling with PRMs.](#S2.SS0.SSS0.Px3 "In 2 Background and Related Work ‣ Process Reward Models That Think")
4.  [3 ThinkPRM](#S3 "In Process Reward Models That Think")
    1.  [3.1 LLM-as-a-judge PRMs are suboptimal](#S3.SS1 "In 3 ThinkPRM ‣ Process Reward Models That Think")
    2.  [3.2 Finetuning on synthetic data boosts LLM-as-a-judge verification](#S3.SS2 "In 3 ThinkPRM ‣ Process Reward Models That Think")
        1.  [Synthetic data collection.](#S3.SS2.SSS0.Px1 "In 3.2 Finetuning on synthetic data boosts LLM-as-a-judge verification ‣ 3 ThinkPRM ‣ Process Reward Models That Think")
        2.  [Finetuning on synthetic verification CoTs substantially improves the verifier.](#S3.SS2.SSS0.Px2 "In 3.2 Finetuning on synthetic data boosts LLM-as-a-judge verification ‣ 3 ThinkPRM ‣ Process Reward Models That Think")
5.  [4 Test-time Scaling Experiments](#S4 "In Process Reward Models That Think")
    1.  [4.1 Experimental Setup](#S4.SS1 "In 4 Test-time Scaling Experiments ‣ Process Reward Models That Think")
        1.  [Baselines.](#S4.SS1.SSS0.Px1 "In 4.1 Experimental Setup ‣ 4 Test-time Scaling Experiments ‣ Process Reward Models That Think")
        2.  [Tasks and Models.](#S4.SS1.SSS0.Px2 "In 4.1 Experimental Setup ‣ 4 Test-time Scaling Experiments ‣ Process Reward Models That Think")
        3.  [Scaling verifier compute.](#S4.SS1.SSS0.Px3 "In 4.1 Experimental Setup ‣ 4 Test-time Scaling Experiments ‣ Process Reward Models That Think")
    2.  [4.2 Results](#S4.SS2 "In 4 Test-time Scaling Experiments ‣ Process Reward Models That Think")
        1.  [ThinkPRM outperforms DiscPRM and LLM-as-a-Judge.](#S4.SS2.SSS0.Px1 "In 4.2 Results ‣ 4 Test-time Scaling Experiments ‣ Process Reward Models That Think")
        2.  [ThinkPRM surpasses off-the-shelf PRMs.](#S4.SS2.SSS0.Px2 "In 4.2 Results ‣ 4 Test-time Scaling Experiments ‣ Process Reward Models That Think")
        3.  [ThinkPRM excels on out-of-domain tasks.](#S4.SS2.SSS0.Px3 "In 4.2 Results ‣ 4 Test-time Scaling Experiments ‣ Process Reward Models That Think")
        4.  [Scaling ThinkPRM compute boosts performance.](#S4.SS2.SSS0.Px4 "In 4.2 Results ‣ 4 Test-time Scaling Experiments ‣ Process Reward Models That Think")
        5.  [Parallel scaling vs. sequential scaling.](#S4.SS2.SSS0.Px5 "In 4.2 Results ‣ 4 Test-time Scaling Experiments ‣ Process Reward Models That Think")
6.  [5 Analysis and Discussion](#S5 "In Process Reward Models That Think")
    1.  [5.1 Training data efficiency](#S5.SS1 "In 5 Analysis and Discussion ‣ Process Reward Models That Think")
    2.  [5.2 Effect of Verification CoT Length on PRM Quality](#S5.SS2 "In 5 Analysis and Discussion ‣ Process Reward Models That Think")
    3.  [5.3 Reasoning traces without clear step boundaries](#S5.SS3 "In 5 Analysis and Discussion ‣ Process Reward Models That Think")
    4.  [5.4 Compute-matched comparison to self-consistency](#S5.SS4 "In 5 Analysis and Discussion ‣ Process Reward Models That Think")
    5.  [5.5 ThinkPRM with Monte Carlo step labels](#S5.SS5 "In 5 Analysis and Discussion ‣ Process Reward Models That Think")
    6.  [5.6 ThinkPRM helps with difficult reasoning problems](#S5.SS6 "In 5 Analysis and Discussion ‣ Process Reward Models That Think")
    7.  [5.7 Filtering based on process vs. outcome labels](#S5.SS7 "In 5 Analysis and Discussion ‣ Process Reward Models That Think")
    8.  [5.8 Limitations of Generative PRMs](#S5.SS8 "In 5 Analysis and Discussion ‣ Process Reward Models That Think")
7.  [References](#bib "In Process Reward Models That Think")
8.  [A Training data](#A1 "In Process Reward Models That Think")
    1.  [A.1 Sampling](#A1.SS1 "In Appendix A Training data ‣ Process Reward Models That Think")
    2.  [A.2 Preprocessing](#A1.SS2 "In Appendix A Training data ‣ Process Reward Models That Think")
9.  [B LLM-as-a-Judge Limitations](#A2 "In Process Reward Models That Think")
10. [C Training details](#A3 "In Process Reward Models That Think")
    1.  [C.1 Training ThinkPRM](#A3.SS1 "In Appendix C Training details ‣ Process Reward Models That Think")
    2.  [C.2 Training Discriminative Verifiers](#A3.SS2 "In Appendix C Training details ‣ Process Reward Models That Think")
11. [D Results on ProcessBench before and after finetuning](#A4 "In Process Reward Models That Think")
12. [E Evaluation details](#A5 "In Process Reward Models That Think")
    1.  [E.1 Predicting verification labels](#A5.SS1 "In Appendix E Evaluation details ‣ Process Reward Models That Think")
    2.  [E.2 Best-of-N selection](#A5.SS2 "In Appendix E Evaluation details ‣ Process Reward Models That Think")
    3.  [E.3 Verifier-guided beam search](#A5.SS3 "In Appendix E Evaluation details ‣ Process Reward Models That Think")
    4.  [E.4 Sequential scaling of verifier compute](#A5.SS4 "In Appendix E Evaluation details ‣ Process Reward Models That Think")
    5.  [E.5 MATH-500 test examples](#A5.SS5 "In Appendix E Evaluation details ‣ Process Reward Models That Think")
    6.  [E.6 Additional results on scaling verifier compute](#A5.SS6 "In Appendix E Evaluation details ‣ Process Reward Models That Think")
    7.  [E.7 Scaling training data of ThinkPRM](#A5.SS7 "In Appendix E Evaluation details ‣ Process Reward Models That Think")
    8.  [E.8 Results with automatic labels](#A5.SS8 "In Appendix E Evaluation details ‣ Process Reward Models That Think")
    9.  [E.9 Verifier performance in terms of problem difficulty](#A5.SS9 "In Appendix E Evaluation details ‣ Process Reward Models That Think")
13. [F More details on LLM-as-judge verification](#A6 "In Process Reward Models That Think")
14. [G Examples from ThinkPRM](#A7 "In Process Reward Models That Think")

[License: CC BY 4.0](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2504.16828v5 \[cs.LG\] 08 Dec 2025

# Process Reward Models That Think

Muhammad Khalifa^(♡), Rishabh Agarwal^(♠), Lajanugen Logeswaran^(♢), Jaekyeom Kim^(♢), Hao Peng^(♣), Moontae Lee^(♢), Honglak Lee^(♡♢⋆), Lu Wang^(♡⋆)   
^(♡)University of Michigan  ^(♠)Mila ^(♢)LG AI Research  ^(♣)University of Illinois Urbana-Champaign ^(⋆)Equal supervision   
[khalifam@umich.edu](mailto:khalifam@umich.edu)

###### Abstract

Step-by-step verifiers—also known as process reward models (PRMs)—are a key ingredient for test-time scaling, but training them requires expensive step-level supervision. This work aims to build data-efficient PRMs as verbalized step-wise reward models that verify every step in the solution by *generating* a verification chain-of-thought (CoT). We propose ThinkPRM, a long CoT verifier fine-tuned on orders of magnitude fewer process labels than those required by discriminative PRMs. Our approach capitalizes on the inherent reasoning abilities of long CoT models, and outperforms LLM-as-a-Judge and discriminative verifiers—using only 1% of the process labels in PRM800K—across several challenging benchmarks. Specifically, ThinkPRM beats the baselines on ProcessBench, MATH-500, and AIME ’24 under best-of-N selection and reward-guided search. In an out-of-domain evaluation over subsets of GPQA-Diamond and LiveCodeBench, our PRM surpasses discriminative verifiers trained with the full PRM800K by 8% and 4.5%, respectively. Lastly, under the same token budget, ThinkPRM scales up verification compute more effectively compared to LLM-as-a-Judge, outperforming it by 7.2% on a subset of ProcessBench. This work highlights the value of generative, long CoT PRMs that can scale test-time compute for verification while requiring minimal supervision for training.¹¹ 1 Our code, data, and models are released at [https://github.com/mukhal/thinkprm](https://github.com/mukhal/thinkprm).

Figure 1: Left: Verifier F1-score on ProcessBench ([Zheng et al., 2024](#bib.bib61)). ThinkPRM-14B, trained on 8K process labels or 1K synthetic examples, outperforms discriminative PRMs trained on about 100x more data. Right: Verifier-guided search accuracy on MATH-500 with Llama-3.2-3B-Instruct as generator. ThinkPRM-1.5B, trained using the same 8K labels, outperforms LLM-as-a-judge and discriminative verifiers in reward-guided search on MATH-500. The LLM-as-a-judge in both figures uses the same base model as ThinkPRM.

## 1 Introduction

Reasoning with large language models (LLMs) can substantially benefit from utilizing more test-time compute ([Jaech et al., 2024](#bib.bib21); [Guo et al., 2025](#bib.bib15); [Akyürek et al., 2024](#bib.bib1)). This typically depends on a high-quality process reward model (PRM)—also known as a process verifier—that scores (partial) solutions for selecting promising paths for search or ranking ([Cobbe et al., 2021](#bib.bib11); [Li et al., 2023](#bib.bib29); [Wu et al., 2024](#bib.bib49); [Brown et al., 2024](#bib.bib5)). PRMs have typically assumed the form of discriminative classifiers, trained to discern correct from incorrect reasoning ([Uesato et al., 2022](#bib.bib43); [Zhang et al., 2025](#bib.bib60)). However, training discriminative PRMs requires access to process labels, i.e., step-level annotations, which either require extensive human annotation ([Lightman et al., 2023](#bib.bib30); [Zheng et al., 2024](#bib.bib61)), gold step-by-step solutions ([Khalifa et al., 2023](#bib.bib25)), or compute-intensive rollouts ([Luo et al., 2024](#bib.bib33); [Chen et al., 2024a](#bib.bib8)). For instance, training reasonably performing math PRMs requires hundreds of thousands of step-level annotations ([Lightman et al., 2023](#bib.bib30); [Wang et al., 2023b](#bib.bib46)).

Generative verification either via LLM-as-a-judge ([Wang et al., 2023a](#bib.bib45); [Liu et al., 2023b](#bib.bib32); [Zheng et al., 2023](#bib.bib62)) or GenRM ([Zhang et al., 2024a](#bib.bib58)) treats verification as a generation problem of a rationale followed by a decision. However, LLM-as-a-judge is known to perform poorly compared to specialized reward models ([Lambert et al., 2024](#bib.bib28); [Zhang et al., 2024b](#bib.bib59); [Chen et al., 2024c](#bib.bib10)), as general-purpose LLMs frequently fail to recognize reasoning errors ([Huang et al., 2023](#bib.bib19); [Zhang et al., 2024a](#bib.bib58); [Ye et al., 2024](#bib.bib54)). Moreover, GenRM is limited to outcome verification via short chain-of-thoughts (CoTs), fundamentally limiting its ability for test-time scaling.

Figure 2: ThinkPRM enables scaling verification compute with more CoT tokens.

This paper builds on the insight that generative step-by-step verification can greatly benefit from scaling up the verifier’s inference compute—specifically, by enabling it to think through a CoT. Specifically, we repurpose open-weight large reasoning models (LRMs) as the foundation for generative PRMs through lightweight training. This training uses uses synthetic data ([Kim et al., 2023](#bib.bib26); [Zhu et al., 2023](#bib.bib64); [Wang et al., 2024](#bib.bib47)), utilizing as few as 8K step labels, and yieldinga ThinkPRM —a PRM that not only surpasses LLM-as-a-judge, but also outperforms discriminative PRMs trained on two orders of magnitude more data across a variety of test-time scaling scenarios.

We obtain ThinkPRM by training four reasoning models, namely R1-Distill-Qwen{1.5B,7B,14B} ([Guo et al., 2025](#bib.bib15)), and QwQ-32B-Preview ([Team, 2024](#bib.bib42)), and extensively evaluate it both as a standalone verifier on ProcessBench ([Zheng et al., 2024](#bib.bib61)), and combined with a generator under Best-of-N and verifier-guided beam search. ThinkPRM-14B outperforms a discriminative PRM based on the same base model in terms of accuracy while using far fewer supervision signals as in [Figure 1](#S0.F1 "In Process Reward Models That Think") left. In addition, ThinkPRM-1.5B demonstrates strong performance on MATH-500 ([Hendrycks et al., 2021](#bib.bib17)) under guided beam search, shown in [Figure 1](#S0.F1 "In Process Reward Models That Think") right. Lastly, as shown in [Figure 2](#S1.F2 "In 1 Introduction ‣ Process Reward Models That Think"), ThinkPRM can effectively utilize more verification compute than LLM-as-a-judge, by forcing it to think for more tokens. All these results are obtained while training only on 8K step labels.

Our work highlights the promise of long CoT PRMs that verify reasoning with reasoning, effectively scaling both generator and verifier compute. Our main findings are as follows: ThinkPRM outperforms strong PRM baselines in best-of-N and guided-search setups on two math reasoning benchmarks: MATH-500 and AIME 2024, and surpasses LLM-as-a-judge baselines under the same base model by thinking longer during verification ([section 4](#S4 "4 Test-time Scaling Experiments ‣ Process Reward Models That Think")). Moreover, ThinkPRM generalizes under two types of domain shift. First, it outperforms baselines on out-of-domain tasks such as scientific reasoning and code generation. Second, despite being trained only on short solutions, it generalizes to long-form reasoning without explicit step delimiters ([section 5.3](#S5.SS3 "5.3 Reasoning traces without clear step boundaries ‣ 5 Analysis and Discussion ‣ Process Reward Models That Think")). Third, ThinkPRM outperforms self-consistency ([Wang et al., 2022](#bib.bib48)) when using the same compute budget, especially under high sampling regimes ([section 5.4](#S5.SS4 "5.4 Compute-matched comparison to self-consistency ‣ 5 Analysis and Discussion ‣ Process Reward Models That Think")). Finally, fine-grained filtering of synthetic data based on step supervision is crucial for training high-quality PRMs ([section 5.7](#S5.SS7 "5.7 Filtering based on process vs. outcome labels ‣ 5 Analysis and Discussion ‣ Process Reward Models That Think")).

## 2 Background and Related Work

#### Discriminative PRMs.

Discriminative PRMs are trained as classifiers that directly predict numerical correctness scores for each solution step, and typically rely on extensive step-level annotations ([Uesato et al., 2022](#bib.bib43); [Lightman et al., 2023](#bib.bib30); [Zhang et al., 2025](#bib.bib60)). Given a solution prefix, discriminative PRMs encode the solution text and employ a classification head to produce step-level scores, usually optimized with binary cross-entropy. An overall correctness score for a solution is obtained by aggregating these step-level scores ([Beeching et al.,](#bib.bib4) ). PRMs are effective and straightforward but they do not utilize the language-modeling head of the base language model, making training expensive and labor-intensive ([Yuan et al., 2024](#bib.bib56)). Additionally, they offer limited interpretability and utilize fixed compute, restricting their dynamic scalability at test-time ([Zhang et al., 2024a](#bib.bib58); [Mahan et al., 2024](#bib.bib34)). Thus, there is a need for data-efficient PRMs that can scale with more test-time compute.

#### Generative Verification.

Generative verification  ([Zheng et al., 2023](#bib.bib62); [Zhu et al., 2023](#bib.bib64); [Zhang et al., 2024a](#bib.bib58)) frames verification as a language-generation task, producing step-level decisions as tokens (e.g., “correct” or “incorrect”), typically accompanied by a chain-of-thought (CoT). One can train generative verifiers using the standard language modeling objective on verification rationales rather than on binary labels. This approach leverages the strengths of LLMs in text generation, making generative verifiers inherently interpretable and scalable ([Zhang et al., 2024a](#bib.bib58); [Mahan et al., 2024](#bib.bib34); [Wang et al., 2023a](#bib.bib45); [Ankner et al., 2024](#bib.bib2)). However, prior work on generative verifiers has relied mainly on short verification CoT (e.g., few hundred tokens) ([Zhang et al., 2024a](#bib.bib58)), which highly limits their scalability. Thus, there is a need for verifiers that can “think” longer through verification, utilizing test-time compute effectively. While LLM-as-a-Judge has been employed for step-level verification ([Zheng et al., 2024](#bib.bib61)). it tends to be sensitive to prompt phrasing, and prone to invalid outputs, such as infinite looping or excessive overthinking ([Bavaresco et al., 2024](#bib.bib3))—issues we further confirm in this work. Prior results with reasoning models like QwQ-32B-Preview ([Team, 2024](#bib.bib42)) show promise, but their practical utility in test-time scaling remains limited without additional training ([Zheng et al., 2024](#bib.bib61)).

#### Test-Time Scaling with PRMs.

Test-time scaling techniques, such as Best-of-N selection ([Charniak & Johnson, 2005](#bib.bib7)) and tree-based search ([Yao et al., 2023](#bib.bib53); [Chen et al., 2024c](#bib.bib10); [Wan et al., 2024](#bib.bib44)), leverage additional inference-time compute to improve reasoning performance. Central to these approaches is the quality of the verifier used to score and select solutions. A major advantage of generative PRMs is that they uniquely support simultaneous scaling of both generator and verifier compute  ([Zhang et al., 2024a](#bib.bib58); [Kalra & Tang, 2025](#bib.bib23)). In particular, our work shows that generative PRMs trained based on long CoT models ([Jaech et al., 2024](#bib.bib21); [Guo et al., 2025](#bib.bib15)) enable both parallel and sequential scaling of verifier compute.

## 3 ThinkPRM

![Refer to caption](2504.16828v5/data_collection.png)

Figure 3: Collecting verification chains for finetuning. First, we prompt a reasoning model, in our case QwQ-32B-Preview to critique a given solution to a problem. Then, we sample multiple verification chains, which we judge against gold process labels from PRM800K, only keeping chains that match the gold process labels.

Our goal is verbalized PRM that, given a problem-solution pair, verifies every step in the solution via an extended chain-of-thought (CoT) such as the one shown in [Figure 44](#A7.F44 "In Appendix G Examples from ThinkPRM ‣ Process Reward Models That Think") in [Appendix G](#A7 "Appendix G Examples from ThinkPRM ‣ Process Reward Models That Think"). This section introduces issues with LLM-as-a-judge verification and proposes a data collection process (shown in [Figure 3](#S3.F3 "In 3 ThinkPRM ‣ Process Reward Models That Think")) to curate high-quality synthetic verification CoTs for training such PRM. The rest of the paper addresses the following research questions:

- •
  RQ1: How well do LRMs perform under LLM-as-a-judge for process-level verification? [Section 3.1](#S3.SS1 "3.1 LLM-as-a-judge PRMs are suboptimal ‣ 3 ThinkPRM ‣ Process Reward Models That Think")
- •
  RQ2: Can lightweight finetuning on synthetic verification CoTs improve the reliability and effectiveness of these models as process verifiers? [Section 3.2](#S3.SS2 "3.2 Finetuning on synthetic data boosts LLM-as-a-judge verification ‣ 3 ThinkPRM ‣ Process Reward Models That Think")
- •
  RQ3: How does a finetuned verbalized PRM (ThinkPRM) compare to discriminative PRMs and LLM-as-a-Judge baselines under different test-time scaling scenarios? [Section 4](#S4 "4 Test-time Scaling Experiments ‣ Process Reward Models That Think")

### 3.1 LLM-as-a-judge PRMs are suboptimal

This section highlights limitations we observe when using off-the-shelf reasoning models as process verifiers, suggesting the need for finetuning. For evaluation, we use ProcessBench ([Zheng et al., 2024](#bib.bib61)), which includes problem-solution pairs with problems sourced from existing math benchmarks, along with ground-truth correctness labels. We report the binary F1-score by instructing models to verify full solutions and judge whether there exists a mistake. We use two most challenging subsets of ProcessBench: OlympiadBench ([He et al., 2024](#bib.bib16)) and OmniMath ([Gao et al., 2024](#bib.bib14)), each comprised of 1K problem-prefix pairs. For LLM-as-a-judge, we use the same prompt template as in [Zheng et al. (2024)](#bib.bib61), shown in [Figure 42](#A6.F42 "In Appendix F More details on LLM-as-judge verification ‣ Process Reward Models That Think"), which we found to work best overall. [Table 3](#A4.T3 "In Appendix D Results on ProcessBench before and after finetuning ‣ Process Reward Models That Think") shows LLM-as-a-judge F1 scores and a sample output by QwQ-32B-Preview is displayed in [Figure 41](#A5.F41 "In E.9 Verifier performance in terms of problem difficulty ‣ Appendix E Evaluation details ‣ Process Reward Models That Think") in [Appendix F](#A6 "Appendix F More details on LLM-as-judge verification ‣ Process Reward Models That Think").

We observe different issues with LLM-as-a-judge verification. First, the verification quality is highly sensitive to the instruction wording: slight change in the instruction can affect the F1-score by up to 3-4 points. First, a substantial number of the generated chains include invalid judgments, i.e., chains without an extractable overall label as clear in [Figure 10](#S3.F10 "In Finetuning on synthetic verification CoTs substantially improves the verifier. ‣ 3.2 Finetuning on synthetic data boosts LLM-as-a-judge verification ‣ 3 ThinkPRM ‣ Process Reward Models That Think"). Such invalid judgements are caused by the following. In some cases, final decision was in the wrong format than instructed e.g., the model tries to solve the problem rather than verify the given solution—a behavior likely stemming from the model training. Second, we noted multiple instances of overthinking ([Chen et al., 2024b](#bib.bib9); [Cuadron et al., 2025](#bib.bib12)), which prevents the model from terminating within the token budget, and infinite looping/repetitions, where the model gets stuck trying alternative techniques to verify the solutions.

[Figure 4](#S3.F4 "In Synthetic data collection. ‣ 3.2 Finetuning on synthetic data boosts LLM-as-a-judge verification ‣ 3 ThinkPRM ‣ Process Reward Models That Think") (left) shows a histogram of verification CoT lengths generated by R1-Qwen-14B in the LLM-as-a-judge setting. Accurate CoTs tend to be shorter, typically under 3K tokens, while inaccurate CoTs are more evenly distributed and spike sharply around 7K-8K tokens, highlighting the prevalence of overthinking and looping in long chains. We show examples of these behaviors in [Appendix B](#A2 "Appendix B LLM-as-a-Judge Limitations ‣ Process Reward Models That Think"). In the next section, we mostly fix these issues via lightweight finetuning over synthetic verification CoTs.

### 3.2 Finetuning on synthetic data boosts LLM-as-a-judge verification

Inspired by recent work on reducing overthinking in long CoT models that by training ([Yu et al., 2024](#bib.bib55); [Kang et al., 2024](#bib.bib24)), we aim to improve LLM-as-a-judge performance via finetuning on high-quality verification data. Collecting real data would be expensive, so we rely on filtered synthetic data ([Zelikman et al., 2022](#bib.bib57); [Singh et al., 2023](#bib.bib37); [Dong et al., 2023](#bib.bib13); [Zhang et al., 2024b](#bib.bib59); [Wang et al., 2024](#bib.bib47)) also known as rejection sampling finetuning. To keep our approach simple, we refrain from more expensive training techniques, such as reinforcement learning or preference-based learning.

#### Synthetic data collection.

As training data, we sample synthetic verification CoTs from QwQ-32B-Preview, prompting it to verify each step in a solution prefix, using the instruction shown in [Figure 21](#A1.F21 "In A.2 Preprocessing ‣ Appendix A Training data ‣ Process Reward Models That Think"). The problems and corresponding step-by-step solutions come from the PRM800K dataset ([Lightman et al., 2023](#bib.bib30)), which provides both model-generated solutions and human-verified step-level labels.

The sampling process continues until we obtain 1K verification CoTs which coreepond to 8K step labels in total. For data filtering, we use the following criteria: (i) the CoT must follow the expected format (i.e., include an extractable decision label for each step inside \boxed{} as shown in [Figure 20](#A1.F20 "In A.1 Sampling ‣ Appendix A Training data ‣ Process Reward Models That Think"), and (ii) the generated step judgements match the gold step labels from PRM800K, and (iii) the CoT length is within a maximum budget—to avoid the excessive overthinking behavior we observed in [Figure 4](#S3.F4 "In Synthetic data collection. ‣ 3.2 Finetuning on synthetic data boosts LLM-as-a-judge verification ‣ 3 ThinkPRM ‣ Process Reward Models That Think") (left). The filtering process ensures our training data is of sufficient quality. note that process-based filtering is crucial for the performance of the resulting PRM as we show in [Section 5.7](#S5.SS7 "5.7 Filtering based on process vs. outcome labels ‣ 5 Analysis and Discussion ‣ Process Reward Models That Think"). Data collection is illustrated in [Figure 3](#S3.F3 "In 3 ThinkPRM ‣ Process Reward Models That Think"), data statistics are in [Section A.1](#A1.SS1 "A.1 Sampling ‣ Appendix A Training data ‣ Process Reward Models That Think") and a training example is in [Figure 20](#A1.F20 "In A.1 Sampling ‣ Appendix A Training data ‣ Process Reward Models That Think").

Notably, our filtering relies only on step-level annotations, not on gold verification rationales or CoTs—making this pipeline scalable and low-overhead. In the absence of gold step-level annotations, one can obtain silver labels via Monte Carlo rollouts ([Wang et al., 2023b](#bib.bib46); [Chen et al., 2024a](#bib.bib8)). While we train only on math data, the resulting PRM remains robust under other domains such as science QA and code generation as we show in [Section 4.2](#S4.SS2 "4.2 Results ‣ 4 Test-time Scaling Experiments ‣ Process Reward Models That Think"). We then proceed to train our models on the 1K collected chains. Our training is very lightweight; finetuning QwQ-32B-Preview takes only 4.5 hours on a single A100 80GB GPU. Refer to [Section C.1](#A3.SS1 "C.1 Training ThinkPRM ‣ Appendix C Training details ‣ Process Reward Models That Think") for training details.

Figure 4: Verifier performance on ProcessBench in light of CoT lengths. On the left, LLM-as-a-judge produces excessively long chains including repetition, infinite looping, and overthinking, leading to worse verifier performance since the output never terminates. Training on collected syntehtic data substantially reduces these issues as shown in the ThinkPRM plot on the right.

#### Finetuning on synthetic verification CoTs substantially improves the verifier.

ThinkPRM trains on the 1K chains and is evaluated on ProcessBench and compared to LLM-as-a-judge under the same base model. [Figure 10](#S3.F10 "In Finetuning on synthetic verification CoTs substantially improves the verifier. ‣ 3.2 Finetuning on synthetic data boosts LLM-as-a-judge verification ‣ 3 ThinkPRM ‣ Process Reward Models That Think") shows verifier accuracy of different models before and after our finetuning. We note a substantial boost in F1 across all models, with the 1.5B model gaining most improvement by over 70 F1 points, and the 14B model performing best. Looking at the ratio of invalid judgements in [Figure 10](#S3.F10 "In Finetuning on synthetic verification CoTs substantially improves the verifier. ‣ 3.2 Finetuning on synthetic data boosts LLM-as-a-judge verification ‣ 3 ThinkPRM ‣ Process Reward Models That Think"), we also note a significant reduction in invalid labels with all models, except for QwQ, where it slightly increases. Lastly, the reduction in overthinking and infinite looping behavior discussed in the last section is evident, as in [Figure 4](#S3.F4 "In Synthetic data collection. ‣ 3.2 Finetuning on synthetic data boosts LLM-as-a-judge verification ‣ 3 ThinkPRM ‣ Process Reward Models That Think") (right), where ThinkPRM generations maintain a reasonable length (1K-5K) tokens while being substantially more accurate.

Figure 7: LLM-as-a-judge suffers from a significant ratio of verification CoTs that do not terminate with a parsable label, i.e., \boxed{yes} or \boxed{no}. Our finetuning process that yields ThinkPRM, substantially mitigates this issue. Both verifiers are based on R1-Distill-Qwen-14B. Figure 10: Verification accuracy on 2K question-solution pairs from two most challenging subsets of ProcessBench: OlympiadBench and OmniMath. ThinkPRM obtained by finetuning the correponding model over only 1K verification chains performs better.

## 4 Test-time Scaling Experiments

This section aims to answer RQ3 introduced in [section 3](#S3 "3 ThinkPRM ‣ Process Reward Models That Think") by comparing ThinkPRM to baselines under different scaling scenarios. We study how ThinkPRM performs under different generation budgets (i) best-of-N selection ([Wu et al., 2024](#bib.bib49); [Brown et al., 2020](#bib.bib6)) and (ii) guided beam search ([Snell et al., 2024](#bib.bib39); [Beeching et al.,](#bib.bib4) ). We also explore how ThinkPRM performs when verifier compute is scaled either in parallel by aggregating decisions over multiple verification CoTs or sequentially through longer CoTs by forcing the model to double check or self-correct its verification.

### 4.1 Experimental Setup

In the remainder of the the paper, we will mainly use our finetuned verifiers based on R1-Distill-Qwen-1.5B and R1-Distill-Qwen-14B as these provide the best tradeoff between size and performance. We will refer to these as ThinkPRM-1.5B and ThinkPRM-14B, respectively.

#### Baselines.

We compare ThinkPRM to DiscPRM, which uses the same base model as ThinkPRM, finetuned with binary cross-entropy on the entire PRM800K dataset, totaling 712K process labels, which is two orders of magnitude larger than our training data. Details on finetuning DiscPRMs are in [Section C.2](#A3.SS2 "C.2 Training Discriminative Verifiers ‣ Appendix C Training details ‣ Process Reward Models That Think"). We also compare to unweighted majority voting, which merely selects the most frequent answer across the samples ([Wang et al., 2022](#bib.bib48)), and to LLM-as-a-Judge using the same base model as ThinkPRM, prompted as in [Section 3.1](#S3.SS1 "3.1 LLM-as-a-judge PRMs are suboptimal ‣ 3 ThinkPRM ‣ Process Reward Models That Think").

#### Tasks and Models.

We show results on three math reasoning tasks, namely 100 problems from MATH-500 ([Hendrycks et al., 2021](#bib.bib17)) covering all difficulty levels (see [Section E.5](#A5.SS5 "E.5 MATH-500 test examples ‣ Appendix E Evaluation details ‣ Process Reward Models That Think") for more details), and American Invitational Mathematics Examination (AIME) problems for 2024. Since ThinkPRM was finetuned only on math data, we study the out-of-domain generalization on two tasks: scientific reasoning and code generation. For scientific reasoning, we use the physics subset of GPQA-Diamond ([Rein et al., 2024](#bib.bib36)), consisting of 86 PhD-level multiple choice questions. For code generation, we use a 200-problem subset from the v5 release of LiveCodeBench ([Jain et al., 2024](#bib.bib22)).

Over MATH-500, we show results with ThinkPRM-1.5B and ThinkPRM-14B on two different generator models: Qwen-2.5-14B and Llama-3.2-3B-Instruct. The former model is used for best-of-N and the latter for beam search as search is compute intensive. Showing results with different generators guarantees that our conclusions are not specific to a certain model family or size. For the more challenging tasks, namely AIME ’24 and GPQA, we use a more capable model, namely Qwen-2.5-32B-Instruct. For code generation, we use Qwen-2.5-Coder-7B ([Hui et al., 2024](#bib.bib20)). Implementation and hyperparemter details on how we select the final answer with best-of-N and beam search are in [Appendix E](#A5 "Appendix E Evaluation details ‣ Process Reward Models That Think").

Figure 11: Best-of-N on AIME ’24 and MATH-500. Compared to LLM-as-a-judge, DiscPRM, and (unweighted) majority vote, ThinkPRM-14B exhibits best accuracy scaling curve.

#### Scaling verifier compute.

Compared to DiscPRMs, generative reward models enable an extra dimension of scaling to squeeze more performance: scaling the verifier compute. Specifically,ThinkPRM allows for two types of scaling. First, we use parallel scaling ([Mahan et al., 2024](#bib.bib34); [Brown et al., 2024](#bib.bib5)), by sampling $K$ independent CoTs and averaging their scores. We will refer to this scaling using “@K” throughout the rest of the paper. Second, and more specific to long reasoning models, we use sequential scaling e.g., by enabling the model to double-check its initial verification ([Xiong et al., 2025](#bib.bib51); [Kumar et al., 2024](#bib.bib27); [Ye et al., 2024](#bib.bib54)). Inspired by [Muennighoff et al. (2025)](#bib.bib35), we use a trigger phrase such as “Let’s verify again” to elicit self-correction of earlier verification. See [Section E.4](#A5.SS4 "E.4 Sequential scaling of verifier compute ‣ Appendix E Evaluation details ‣ Process Reward Models That Think") for more details.

Figure 14: Comparison to off-the-shelf PRMs trained on much more step labels than ThinkPRM. $@\hspace{0pt}K$ represents parallel scaling by averaging scores over K CoTs. Figure 17: Ablating the data filtering mechanism, where our process-based filtering yields better PRMs. LLM-as-a-judge is shown with number of beams = 16.

### 4.2 Results

#### ThinkPRM outperforms DiscPRM and LLM-as-a-Judge.

Under best-of-N selection with MATH-500 shown in [Figure 11](#S4.F11 "In Tasks and Models. ‣ 4.1 Experimental Setup ‣ 4 Test-time Scaling Experiments ‣ Process Reward Models That Think") (right), ThinkPRM leads to higher or comparable reasoning accuracy to DiscPRM under all sampling budgets. The trend holds on the more challenging AIME ’24, shown in [Figure 11](#S4.F11 "In Tasks and Models. ‣ 4.1 Experimental Setup ‣ 4 Test-time Scaling Experiments ‣ Process Reward Models That Think") left. Additionally, [Figure 1](#S0.F1 "In Process Reward Models That Think") (right) shows beam search results on MATH-500, with ThinkPRM 1.5B surpassing DiscPRM and LLM-as-a-Judge.

#### ThinkPRM surpasses off-the-shelf PRMs.

We compare ThinkPRM-1.5B to two strong off-the-shelf PRMs, namely RLHFFlow-Deepseek-PRM ([Xiong et al., 2024](#bib.bib50)) and MATH-Shepherd-PRM ([Wang et al., 2023b](#bib.bib46)). These PRMs are trained on even more data than PRM800K and are larger than 1.5B. We show results under verifier-guided search on MATH-500 in [Figure 17](#S4.F17 "In Scaling verifier compute. ‣ 4.1 Experimental Setup ‣ 4 Test-time Scaling Experiments ‣ Process Reward Models That Think"), with ThinkPRM-1.5B’s scaling curve surpassing all baselines and outperforming RLHFFlow-Deepseek-PRM, the best off-the-shelf PRM among the ones we tested, by more than 7% across all beam sizes.

#### ThinkPRM excels on out-of-domain tasks.

As for OOD performance on GPQA-physics ([Figure 18](#S4.F18 "In Parallel scaling vs. sequential scaling. ‣ 4.2 Results ‣ 4 Test-time Scaling Experiments ‣ Process Reward Models That Think") left), ThinkPRM scales better than DiscPRM—which drops substantially at N=32—outperforming it by 8%. On LiveCodeBench ([Figure 18](#S4.F18 "In Parallel scaling vs. sequential scaling. ‣ 4.2 Results ‣ 4 Test-time Scaling Experiments ‣ Process Reward Models That Think") right), ThinkPRM also outperforms DiscPRM by 4.5%. On LiveCodeBench, Qwen2.5-7B-Math-PRM ([Zhang et al., 2025](#bib.bib60))—a discriminative PRM trained on substantial amount of process labels obtained from LLM-as-a-judge data and Monte Carlo rollouts—struggles when applied out-of-domain. Our results shed light on the fragility of discriminative PRMs under domain shifts in contrast with generative PRMs.

#### Scaling ThinkPRM compute boosts performance.

Under verifier-guided search (shown in [Figure 17](#S4.F17 "In Scaling verifier compute. ‣ 4.1 Experimental Setup ‣ 4 Test-time Scaling Experiments ‣ Process Reward Models That Think")), parallel scaling with ThinkPRM-1.5B@4 boosts the accuracy by more than 5% points, and yields the best accuracy on MATH-500. In addition, parallel scaling with ThinkPRM-14B@4 and ThinkPRM-14B@8 boosts best-of-N performance on MATH-500 as shown in [Figure 31](#A5.F31 "In E.5 MATH-500 test examples ‣ Appendix E Evaluation details ‣ Process Reward Models That Think") in [Section E.6](#A5.SS6 "E.6 Additional results on scaling verifier compute ‣ Appendix E Evaluation details ‣ Process Reward Models That Think"). Now we move to sequential scaling of verifier compute by forcing ThinkPRM to recheck its own verification. Since this can be compute-intensive, we only run this on 200 problems from OmniMath subset of ProcessBench, and observe how verification F1 improves as we force the model to think for longer as shown in [Figure 2](#S1.F2 "In 1 Introduction ‣ Process Reward Models That Think"). ThinkPRM exhibits better scaling behavior compared to LLM-as-a-judge, which drops after 16K tokens, and outperforms DiscPRM-14B by 15 F1 points. In summary, ThinkPRM is consistently better than LLM-as-a-judge under parallel and sequential scaling.

#### Parallel scaling vs. sequential scaling.

Is it preferable to scale verifier compute in parallel or sequentially? We investigate this by comparing the two modes of scaling under the same token budget. [Figure 32](#A5.F32 "In E.6 Additional results on scaling verifier compute ‣ Appendix E Evaluation details ‣ Process Reward Models That Think") in [Section E.6](#A5.SS6 "E.6 Additional results on scaling verifier compute ‣ Appendix E Evaluation details ‣ Process Reward Models That Think") shows performance of best-of-N with Qwen-2.5-14B under parallel and sequential scaling with ${K = 2},4$ under both parallel scaling and sequential scaling. Overall, the performance of both methods is fairly close, but we observe a slight advantage to parallel scaling under certain budgets.

Figure 18: Best-of-N on two out-of-domain tasks: science QA (GPQA-Physics) and code generation (LiveCodeBench). Although ThinkPRM was only finetuned on math, it exhibits superior OOD performance than the baselines, especially at larger sampling budgets, where the baselines fall short. Discriminative PRMs struggle despite being trained on orders of magnitude more process labels.

## 5 Analysis and Discussion

### 5.1 Training data efficiency

A major strength of ThinkPRM is training data efficiency compared to discriminative versions. Here, we study the training scaling behavior of ThinkPRM-14B by training it over 500 and 1K examples in total collected using the pipeline in [Section 3.2](#S3.SS2 "3.2 Finetuning on synthetic data boosts LLM-as-a-judge verification ‣ 3 ThinkPRM ‣ Process Reward Models That Think"), which roughly corresponds to 4K and 8K process labels from PRM800K in total. We compare that to DiscPRM-14B trained with 1K, 10K, 50K and 98K examples, where 98K corresponds to training on the full PRM800K train set that includes 712K step labels. [Figure 1](#S0.F1 "In Process Reward Models That Think") (Left) contrasts the training data scaling behavior of ThinkPRM-14B with that of DiscPRM-14B, where ThinkPRM-14B’s performance scales substantially better with two orders of magnitude fewer process labels. This primarily stems from ThinkPRM’s utilization of text generation and reasoning abilities of the underlying models.

While we train ThinkPRM using only 1K data points, we investigate whether it will benefit from training on more data. Using the pipeline, we collect and filter additional verification CoTs and obtain a total of 65K chains. We then finetune R1-Distill-Qwen-1.5B and R1-Distill-Qwen-14B on these for a single epoch while keeping all other training hyperparameters fixed. We then compare the resulting models to the 1K-trained version of ThinkPRM under best-of-N selection on MATH-500. [Figures 38](#A5.F38 "In E.7 Scaling training data of ThinkPRM ‣ Appendix E Evaluation details ‣ Process Reward Models That Think") and [38](#A5.F38 "Figure 38 ‣ E.7 Scaling training data of ThinkPRM ‣ Appendix E Evaluation details ‣ Process Reward Models That Think") in [Section E.7](#A5.SS7 "E.7 Scaling training data of ThinkPRM ‣ Appendix E Evaluation details ‣ Process Reward Models That Think") show a performance boost from training on the 65K examples compared to only 1K. This suggests that ThinkPRM can utilize more training data when available.

### 5.2 Effect of Verification CoT Length on PRM Quality

We study whether the length of verification chains of thought affects the quality of the resulting generative verifier. Specifically, we compare ThinkPRM trained on the full, long synthetic CoTs with a variant trained on short, compressed versions of the same 1K CoTs. To obtain the short CoTs, we instruct gpt-4o-mini to rewrite each original CoT into a concise version that preserves only the essential reasoning. We then train R1-Qwen-1.5B and R1-Qwen-14B on these short CoTs and evaluate verification F1 on ProcessBench. Table [1](#S5.T1 "Table 1 ‣ 5.2 Effect of Verification CoT Length on PRM Quality ‣ 5 Analysis and Discussion ‣ Process Reward Models That Think") reports the comparison.

|              | Long CoT (ThinkPRM) |          | Short CoT     |          |
|--------------|---------------------|----------|---------------|----------|
| Model        | OlympiadBench       | OmniMath | OlympiadBench | OmniMath |
| R1-Qwen-1.5B | 87.3                | 75.7     | 64.8          | 66.7     |
| R1-Qwen-14B  | 87.3                | 85.7     | 55.3          | 60.8     |

Table 1: Verification F1 when training R1 models on long versus short CoTs.

The substantial performance drop when training on short CoTs emphasizes how ThinkPRM benefits from extended reasoning. Since verification is a complex task, throwing more reasoning effort at it via thinking improves performance. These results support the value of using long verification CoTs for training.

### 5.3 Reasoning traces without clear step boundaries

So far, we have used ThinkPRM to verify short CoTs with clear steps delimiters. Here, we investigate whether ThinkPRM can still verify long CoTs that involve extended reasoning, backtracking, and self-correction. As a generator, we use Qwen3-1.7B ([Yang et al., 2025](#bib.bib52)) with thinking mode. Although ThinkPRM was only trained on short solutions from PRM800K, it can still verify long CoTs and outperforms the baselines as shown in [Figure 19](#S5.F19 "In 5.5 ThinkPRM with Monte Carlo step labels ‣ 5 Analysis and Discussion ‣ Process Reward Models That Think") left. Inspecting ThinkPRM’s outputs, we found that it extracts and verifies individual steps embedded in the long CoT—an example is in [Figure 45](#A7.F45 "In Appendix G Examples from ThinkPRM ‣ Process Reward Models That Think").

### 5.4 Compute-matched comparison to self-consistency

Under a fixed test-time compute budget for best-of-N, how does ThinkPRM compare to simply sampling more solutions from the generator and applying majority voting? To investigate this, we conduct a compute-matched analysis on MATH-500 and GPQA-Physics. [Figure 19](#S5.F19 "In 5.5 ThinkPRM with Monte Carlo step labels ‣ 5 Analysis and Discussion ‣ Process Reward Models That Think") mid and right plot solution accuracy as a function of sampling FLOPs for MATH-500 and GPQA-physics. At low sampling budgets, best-of-N with ThinkPRM performs comparably to self-consistency, but as the compute budget increases, ThinkPRM has a clear advantage. These findings agree with recent work on outcome reward models ([Singhi et al., 2025](#bib.bib38)).

### 5.5 ThinkPRM with Monte Carlo step labels

To train ThinkPRM, we have relied on manual step labels from PRM800K. Since automatic labels e.g., via Monte Carlo rollouts [Luo et al. (2024)](#bib.bib33) are cheaper, we validate whether we can train ThinkPRM using automatic labels. We train ThinkPRM-1.5B using 1K synthetic chains based on labels from Math-shepherd dataset ([Wang et al., 2023b](#bib.bib46)). Performance on ProcessBench is shown in [Table 4](#A5.T4 "In E.8 Results with automatic labels ‣ Appendix E Evaluation details ‣ Process Reward Models That Think"), where training ThinkPRM with automatic labels yields very comparable performance to training with manual labels, showing that our training pipeline is agnostic to step-labeling strategy.

Figure 19: Left: Best-of-N with Qwen3-1.7B on the full MATH-500 test set, showing how ThinkPRM generalizes well to verifying long reasoning traces. Mid and Right: Compute-matched comparison between best-of-N with ThinkPRM and self-consistency or majority vote.

### 5.6 ThinkPRM helps with difficult reasoning problems

ThinkPRM’s reasoning ability should enable it to tackle verification of hard problems. To check if this is the case, we analyze performance of ThinkPRM vs. DiscPRM in light of problem difficulty over MATH-500 and GPQA-physics (how we estimate difficulty for GPQA-Physics is explained in [Section E.9](#A5.SS9 "E.9 Verifier performance in terms of problem difficulty ‣ Appendix E Evaluation details ‣ Process Reward Models That Think")), shown in [Figure 39](#A5.F39 "In E.9 Verifier performance in terms of problem difficulty ‣ Appendix E Evaluation details ‣ Process Reward Models That Think"). The generators here are Qwen-2.5-14B for MATH-500 and Qwen-2.5-32B-Instruct for GPQA-Physics. Primarily, ThinkPRM improves reasoning on the difficult problems (levels 3, 4, 5 in MATH-500 and 2, 3, 4 in GPQA-Physics) substantially more than DiscPRM.

### 5.7 Filtering based on process vs. outcome labels

In [Section 3.2](#S3.SS2 "3.2 Finetuning on synthetic data boosts LLM-as-a-judge verification ‣ 3 ThinkPRM ‣ Process Reward Models That Think"), we describe our process-based filtering strategy, which selects verification CoTs based on agreement between generated step-level decisions and gold process labels. To validate its effectiveness, we compare it to outcome-based filtering, as in GenRM ([Zheng et al., 2024](#bib.bib61)), which retains chains solely based on final answer correctness—keeping a CoT if its final answer is correct and the final step is \boxed{correct}, or if the answer is incorrect and the final step is \boxed{incorrect}, thereby ignoring intermediate step labels. We obtain 65K and 128K CoTs using process- and outcome-based filtering, respectively. [Figure 17](#S4.F17 "In Scaling verifier compute. ‣ 4.1 Experimental Setup ‣ 4 Test-time Scaling Experiments ‣ Process Reward Models That Think") shows that finetuning R1-Distill-Qwen-1.5B on process-filtered data yields significantly better verification performance, despite using fewer examples, which reflects the importance of our process-based filtering in training strong PRMs.

### 5.8 Limitations of Generative PRMs

While generative PRMs are more powerful and data-efficient than their discriminative counterparts, they come with some limitations that we highlight as avenues for future work. First, overconfidence is a known issue in LLMs ([Liu et al., 2023a](#bib.bib31); [Stechly et al., 2023](#bib.bib40); [Zhou et al., 2024](#bib.bib63)) and, in the case of PRMs, it can cause the predicted PRM scores to cluster near extremes: close to either 0 or 1. One reason is that we are using probabilities of certain tokens such as “yes” or “no”, which by nature will be either very high or very low. Future work should explore more reliable techniques to extract calibrated scores from generative reward models. Another limitation is due to autoregressive nature of LLMs, leading them to prematurely commit to an earlier judgment. For example, we observe a phenomenon we term step label interference, where verification errors for earlier steps impact verification of later steps. For example, we noted that if the PRM judges a particular step as incorrect, it becomes more likely to label subsequent steps as incorrect even if it is not. Lastly, generating a verification CoT introduces extra overhead compared to discriminative PRMs, but we argue that the performance gains offered by generative PRMs justify this extra cost.

## Conclusion

We introduced ThinkPRM, a generative process reward model trained with minimal synthetic supervision for scalable step-by-step verification. With just 8K process labels, ThinkPRM significantly outperforms LLM-as-a-judge and even surpasses discriminative PRMs trained on orders of magnitude more data. These results highlight the benefits of generative PRMs in interpretability, scalability, and data efficiency, and demonstrate their potential to scale verification compute for complex reasoning tasks in math and science.

## References

- Akyürek et al. (2024) Ekin Akyürek, Mehul Damani, Linlu Qiu, Han Guo, Yoon Kim, and Jacob Andreas. The surprising effectiveness of test-time training for abstract reasoning. *arXiv preprint arXiv:2411.07279*, 2024.
- Ankner et al. (2024) Zachary Ankner, Mansheej Paul, Brandon Cui, Jonathan D Chang, and Prithviraj Ammanabrolu. Critique-out-loud reward models. *arXiv preprint arXiv:2408.11791*, 2024.
- Bavaresco et al. (2024) Anna Bavaresco, Raffaella Bernardi, Leonardo Bertolazzi, Desmond Elliott, Raquel Fernández, Albert Gatt, Esam Ghaleb, Mario Giulianelli, Michael Hanna, Alexander Koller, et al. Llms instead of human judges? a large scale empirical study across 20 nlp evaluation tasks. *arXiv preprint arXiv:2406.18403*, 2024.
- (4) Edward Beeching, Lewis Tunstall, and Sasha Rush. Scaling test-time compute with open models. URL [https://huggingface.co/spaces/HuggingFaceH4/blogpost-scaling-test-time-compute](https://huggingface.co/spaces/HuggingFaceH4/blogpost-scaling-test-time-compute).
- Brown et al. (2024) Bradley Brown, Jordan Juravsky, Ryan Ehrlich, Ronald Clark, Quoc V Le, Christopher Ré, and Azalia Mirhoseini. Large language monkeys: Scaling inference compute with repeated sampling. *arXiv preprint arXiv:2407.21787*, 2024.
- Brown et al. (2020) Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. Language models are few-shot learners. *Advances in neural information processing systems*, 33:1877–1901, 2020.
- Charniak & Johnson (2005) Eugene Charniak and Mark Johnson. Coarse-to-fine n-best parsing and maxent discriminative reranking. In *Proceedings of the 43rd Annual Meeting of the Association for Computational Linguistics (ACL’05)*, pp. 173–180, 2005.
- Chen et al. (2024a) Guoxin Chen, Minpeng Liao, Chengxi Li, and Kai Fan. Alphamath almost zero: process supervision without process. *arXiv preprint arXiv:2405.03553*, 2024a.
- Chen et al. (2024b) Xingyu Chen, Jiahao Xu, Tian Liang, Zhiwei He, Jianhui Pang, Dian Yu, Linfeng Song, Qiuzhi Liu, Mengfei Zhou, Zhuosheng Zhang, et al. Do not think that much for 2+ 3=? on the overthinking of o1-like llms. *arXiv preprint arXiv:2412.21187*, 2024b.
- Chen et al. (2024c) Ziru Chen, Michael White, Raymond Mooney, Ali Payani, Yu Su, and Huan Sun. When is tree search useful for llm planning? it depends on the discriminator. *arXiv preprint arXiv:2402.10890*, 2024c.
- Cobbe et al. (2021) Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John Schulman. Training verifiers to solve math word problems. *arXiv preprint arXiv:2110.14168*, 2021.
- Cuadron et al. (2025) Alejandro Cuadron, Dacheng Li, Wenjie Ma, Xingyao Wang, Yichuan Wang, Siyuan Zhuang, Shu Liu, Luis Gaspar Schroeder, Tian Xia, Huanzhi Mao, et al. The danger of overthinking: Examining the reasoning-action dilemma in agentic tasks. *arXiv preprint arXiv:2502.08235*, 2025.
- Dong et al. (2023) Hanze Dong, Wei Xiong, Deepanshu Goyal, Yihan Zhang, Winnie Chow, Rui Pan, Shizhe Diao, Jipeng Zhang, Kashun Shum, and Tong Zhang. Raft: Reward ranked finetuning for generative foundation model alignment. *arXiv preprint arXiv:2304.06767*, 2023.
- Gao et al. (2024) Bofei Gao, Feifan Song, Zhe Yang, Zefan Cai, Yibo Miao, Qingxiu Dong, Lei Li, Chenghao Ma, Liang Chen, Runxin Xu, et al. Omni-math: A universal olympiad level mathematic benchmark for large language models. *arXiv preprint arXiv:2410.07985*, 2024.
- Guo et al. (2025) Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. *arXiv preprint arXiv:2501.12948*, 2025.
- He et al. (2024) Chaoqun He, Renjie Luo, Yuzhuo Bai, Shengding Hu, Zhen Leng Thai, Junhao Shen, Jinyi Hu, Xu Han, Yujie Huang, Yuxiang Zhang, et al. Olympiadbench: A challenging benchmark for promoting agi with olympiad-level bilingual multimodal scientific problems. *arXiv preprint arXiv:2402.14008*, 2024.
- Hendrycks et al. (2021) Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, and Jacob Steinhardt. Measuring mathematical problem solving with the math dataset. *arXiv preprint arXiv:2103.03874*, 2021.
- Hu et al. (2022) Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen, et al. Lora: Low-rank adaptation of large language models. *ICLR*, 1(2):3, 2022.
- Huang et al. (2023) Jie Huang, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng, Adams Wei Yu, Xinying Song, and Denny Zhou. Large language models cannot self-correct reasoning yet. *arXiv preprint arXiv:2310.01798*, 2023.
- Hui et al. (2024) Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Dayiheng Liu, Lei Zhang, Tianyu Liu, Jiajun Zhang, Bowen Yu, Kai Dang, et al. Qwen2. 5-coder technical report. *arXiv preprint arXiv:2409.12186*, 2024.
- Jaech et al. (2024) Aaron Jaech, Adam Kalai, Adam Lerer, Adam Richardson, Ahmed El-Kishky, Aiden Low, Alec Helyar, Aleksander Madry, Alex Beutel, Alex Carney, et al. Openai o1 system card. *arXiv preprint arXiv:2412.16720*, 2024.
- Jain et al. (2024) Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia Yan, Tianjun Zhang, Sida Wang, Armando Solar-Lezama, Koushik Sen, and Ion Stoica. Livecodebench: Holistic and contamination free evaluation of large language models for code. *arXiv preprint arXiv:2403.07974*, 2024.
- Kalra & Tang (2025) Nimit Kalra and Leonard Tang. Verdict: A library for scaling judge-time compute. *arXiv preprint arXiv:2502.18018*, 2025.
- Kang et al. (2024) Yu Kang, Xianghui Sun, Liangyu Chen, and Wei Zou. C3ot: Generating shorter chain-of-thought without compromising effectiveness. *arXiv preprint arXiv:2412.11664*, 2024.
- Khalifa et al. (2023) Muhammad Khalifa, Lajanugen Logeswaran, Moontae Lee, Honglak Lee, and Lu Wang. GRACE: discriminator-guided chain-of-thought reasoning. In Houda Bouamor, Juan Pino, and Kalika Bali (eds.), *Findings of the Association for Computational Linguistics: EMNLP 2023, Singapore, December 6-10, 2023*, pp. 15299–15328. Association for Computational Linguistics, 2023. doi: 10.18653/V1/2023.FINDINGS-EMNLP.1022. URL [https://doi.org/10.18653/v1/2023.findings-emnlp.1022](https://doi.org/10.18653/v1/2023.findings-emnlp.1022).
- Kim et al. (2023) Seungone Kim, Jamin Shin, Yejin Cho, Joel Jang, Shayne Longpre, Hwaran Lee, Sangdoo Yun, Seongjin Shin, Sungdong Kim, James Thorne, et al. Prometheus: Inducing fine-grained evaluation capability in language models. In *The Twelfth International Conference on Learning Representations*, 2023.
- Kumar et al. (2024) Aviral Kumar, Vincent Zhuang, Rishabh Agarwal, Yi Su, John D Co-Reyes, Avi Singh, Kate Baumli, Shariq Iqbal, Colton Bishop, Rebecca Roelofs, et al. Training language models to self-correct via reinforcement learning. *arXiv preprint arXiv:2409.12917*, 2024.
- Lambert et al. (2024) Nathan Lambert, Valentina Pyatkin, Jacob Morrison, LJ Miranda, Bill Yuchen Lin, Khyathi Chandu, Nouha Dziri, Sachin Kumar, Tom Zick, Yejin Choi, et al. Rewardbench: Evaluating reward models for language modeling. *arXiv preprint arXiv:2403.13787*, 2024.
- Li et al. (2023) Yifei Li, Zeqi Lin, Shizhuo Zhang, Qiang Fu, Bei Chen, Jian-Guang Lou, and Weizhu Chen. Making language models better reasoners with step-aware verifier. In *Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pp. 5315–5333, 2023.
- Lightman et al. (2023) Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri Edwards, Bowen Baker, Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever, and Karl Cobbe. Let’s verify step by step. *arXiv preprint arXiv:2305.20050*, 2023.
- Liu et al. (2023a) Xin Liu, Muhammad Khalifa, and Lu Wang. Litcab: Lightweight language model calibration over short-and long-form responses. *arXiv preprint arXiv:2310.19208*, 2023a.
- Liu et al. (2023b) Yang Liu, Dan Iter, Yichong Xu, Shuohang Wang, Ruochen Xu, and Chenguang Zhu. G-eval: Nlg evaluation using gpt-4 with better human alignment. *arXiv preprint arXiv:2303.16634*, 2023b.
- Luo et al. (2024) Liangchen Luo, Yinxiao Liu, Rosanne Liu, Samrat Phatale, Harsh Lara, Yunxuan Li, Lei Shu, Yun Zhu, Lei Meng, Jiao Sun, et al. Improve mathematical reasoning in language models by automated process supervision. *arXiv preprint arXiv:2406.06592*, 2, 2024.
- Mahan et al. (2024) Dakota Mahan, Duy Van Phung, Rafael Rafailov, Chase Blagden, Nathan Lile, Louis Castricato, Jan-Philipp Fränken, Chelsea Finn, and Alon Albalak. Generative reward models. *arXiv preprint arXiv:2410.12832*, 2024.
- Muennighoff et al. (2025) Niklas Muennighoff, Zitong Yang, Weijia Shi, Xiang Lisa Li, Li Fei-Fei, Hannaneh Hajishirzi, Luke Zettlemoyer, Percy Liang, Emmanuel Candès, and Tatsunori Hashimoto. s1: Simple test-time scaling. *arXiv preprint arXiv:2501.19393*, 2025.
- Rein et al. (2024) David Rein, Betty Li Hou, Asa Cooper Stickland, Jackson Petty, Richard Yuanzhe Pang, Julien Dirani, Julian Michael, and Samuel R Bowman. Gpqa: A graduate-level google-proof q&a benchmark. In *First Conference on Language Modeling*, 2024.
- Singh et al. (2023) Avi Singh, John D Co-Reyes, Rishabh Agarwal, Ankesh Anand, Piyush Patil, Xavier Garcia, Peter J Liu, James Harrison, Jaehoon Lee, Kelvin Xu, et al. Beyond human data: Scaling self-training for problem-solving with language models. *arXiv preprint arXiv:2312.06585*, 2023.
- Singhi et al. (2025) Nishad Singhi, Hritik Bansal, Arian Hosseini, Aditya Grover, Kai-Wei Chang, Marcus Rohrbach, and Anna Rohrbach. When to solve, when to verify: Compute-optimal problem solving and generative verification for llm reasoning. *arXiv preprint arXiv:2504.01005*, 2025.
- Snell et al. (2024) Charlie Snell, Jaehoon Lee, Kelvin Xu, and Aviral Kumar. Scaling llm test-time compute optimally can be more effective than scaling model parameters. *arXiv preprint arXiv:2408.03314*, 2024.
- Stechly et al. (2023) Kaya Stechly, Matthew Marquez, and Subbarao Kambhampati. Gpt-4 doesn’t know it’s wrong: An analysis of iterative prompting for reasoning problems. *arXiv preprint arXiv:2310.12397*, 2023.
- Sun et al. (2024) Zhiqing Sun, Longhui Yu, Yikang Shen, Weiyang Liu, Yiming Yang, Sean Welleck, and Chuang Gan. Easy-to-hard generalization: Scalable alignment beyond human supervision. *arXiv preprint arXiv:2403.09472*, 2024.
- Team (2024) Qwen Team. Qwq: Reflect deeply on the boundaries of the unknown, November 2024. URL [https://qwenlm.github.io/blog/qwq-32b-preview/](https://qwenlm.github.io/blog/qwq-32b-preview/).
- Uesato et al. (2022) Jonathan Uesato, Nate Kushman, Ramana Kumar, Francis Song, Noah Siegel, Lisa Wang, Antonia Creswell, Geoffrey Irving, and Irina Higgins. Solving math word problems with process-and outcome-based feedback. *arXiv preprint arXiv:2211.14275*, 2022.
- Wan et al. (2024) Ziyu Wan, Xidong Feng, Muning Wen, Stephen Marcus McAleer, Ying Wen, Weinan Zhang, and Jun Wang. Alphazero-like tree-search can guide large language model decoding and training. In *Forty-first International Conference on Machine Learning*, 2024.
- Wang et al. (2023a) Jiaan Wang, Yunlong Liang, Fandong Meng, Haoxiang Shi, Zhixu Li, Jinan Xu, Jianfeng Qu, and Jie Zhou. Is chatgpt a good nlg evaluator? a preliminary study. *arXiv preprint arXiv:2303.04048*, 2023a.
- Wang et al. (2023b) Peiyi Wang, Lei Li, Zhihong Shao, RX Xu, Damai Dai, Yifei Li, Deli Chen, Y Wu, and Zhifang Sui. Math-shepherd: A label-free step-by-step verifier for llms in mathematical reasoning. *arXiv preprint arXiv:2312.08935*, 2023b.
- Wang et al. (2024) Tianlu Wang, Ilia Kulikov, Olga Golovneva, Ping Yu, Weizhe Yuan, Jane Dwivedi-Yu, Richard Yuanzhe Pang, Maryam Fazel-Zarandi, Jason Weston, and Xian Li. Self-taught evaluators. *arXiv preprint arXiv:2408.02666*, 2024.
- Wang et al. (2022) Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, and Denny Zhou. Self-consistency improves chain of thought reasoning in language models. *arXiv preprint arXiv:2203.11171*, 2022.
- Wu et al. (2024) Yangzhen Wu, Zhiqing Sun, Shanda Li, Sean Welleck, and Yiming Yang. Inference scaling laws: An empirical analysis of compute-optimal inference for problem-solving with language models. *arXiv preprint arXiv:2408.00724*, 2024.
- Xiong et al. (2024) Wei Xiong, Hanning Zhang, Nan Jiang, and Tong Zhang. An implementation of generative prm. [https://github.com/RLHFlow/RLHF-Reward-Modeling](https://github.com/RLHFlow/RLHF-Reward-Modeling), 2024.
- Xiong et al. (2025) Wei Xiong, Hanning Zhang, Chenlu Ye, Lichang Chen, Nan Jiang, and Tong Zhang. Self-rewarding correction for mathematical reasoning. *arXiv preprint arXiv:2502.19613*, 2025.
- Yang et al. (2025) An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao, Chengen Huang, Chenxu Lv, et al. Qwen3 technical report. *arXiv preprint arXiv:2505.09388*, 2025.
- Yao et al. (2023) Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Tom Griffiths, Yuan Cao, and Karthik Narasimhan. Tree of thoughts: Deliberate problem solving with large language models. *Advances in neural information processing systems*, 36:11809–11822, 2023.
- Ye et al. (2024) Tian Ye, Zicheng Xu, Yuanzhi Li, and Zeyuan Allen-Zhu. Physics of language models: Part 2.2, how to learn from mistakes on grade-school math problems. *arXiv preprint arXiv:2408.16293*, 2024.
- Yu et al. (2024) Ping Yu, Jing Xu, Jason Weston, and Ilia Kulikov. Distilling system 2 into system 1. *arXiv preprint arXiv:2407.06023*, 2024.
- Yuan et al. (2024) Lifan Yuan, Wendi Li, Huayu Chen, Ganqu Cui, Ning Ding, Kaiyan Zhang, Bowen Zhou, Zhiyuan Liu, and Hao Peng. Free process rewards without process labels. *arXiv preprint arXiv:2412.01981*, 2024.
- Zelikman et al. (2022) Eric Zelikman, Yuhuai Wu, Jesse Mu, and Noah Goodman. Star: Bootstrapping reasoning with reasoning. *Advances in Neural Information Processing Systems*, 35:15476–15488, 2022.
- Zhang et al. (2024a) Lunjun Zhang, Arian Hosseini, Hritik Bansal, Mehran Kazemi, Aviral Kumar, and Rishabh Agarwal. Generative verifiers: Reward modeling as next-token prediction. *arXiv preprint arXiv:2408.15240*, 2024a.
- Zhang et al. (2024b) Yunxiang Zhang, Muhammad Khalifa, Lajanugen Logeswaran, Jaekyeom Kim, Moontae Lee, Honglak Lee, and Lu Wang. Small language models need strong verifiers to self-correct reasoning. In Lun-Wei Ku, Andre Martins, and Vivek Srikumar (eds.), *Findings of the Association for Computational Linguistics, ACL 2024, Bangkok, Thailand and virtual meeting, August 11-16, 2024*, pp. 15637–15653. Association for Computational Linguistics, 2024b. doi: 10.18653/V1/2024.FINDINGS-ACL.924. URL [https://doi.org/10.18653/v1/2024.findings-acl.924](https://doi.org/10.18653/v1/2024.findings-acl.924).
- Zhang et al. (2025) Zhenru Zhang, Chujie Zheng, Yangzhen Wu, Beichen Zhang, Runji Lin, Bowen Yu, Dayiheng Liu, Jingren Zhou, and Junyang Lin. The lessons of developing process reward models in mathematical reasoning. *arXiv preprint arXiv:2501.07301*, 2025.
- Zheng et al. (2024) Chujie Zheng, Zhenru Zhang, Beichen Zhang, Runji Lin, Keming Lu, Bowen Yu, Dayiheng Liu, Jingren Zhou, and Junyang Lin. Processbench: Identifying process errors in mathematical reasoning. *arXiv preprint arXiv:2412.06559*, 2024.
- Zheng et al. (2023) Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric Xing, et al. Judging llm-as-a-judge with mt-bench and chatbot arena. *Advances in Neural Information Processing Systems*, 36:46595–46623, 2023.
- Zhou et al. (2024) Kaitlyn Zhou, Jena D Hwang, Xiang Ren, and Maarten Sap. Relying on the unreliable: The impact of language models’ reluctance to express uncertainty. *arXiv preprint arXiv:2401.06730*, 2024.
- Zhu et al. (2023) Lianghui Zhu, Xinggang Wang, and Xinlong Wang. Judgelm: Fine-tuned large language models are scalable judges. *arXiv preprint arXiv:2310.17631*, 2023.

## Appendix A Training data

### A.1 Sampling

[Figure 3](#S3.F3 "In 3 ThinkPRM ‣ Process Reward Models That Think") shows the prompt used with QwQ-32B-Preview to sample verification chains for training. We use the problem-prefix pairs from PRM800K train split ([Lightman et al., 2023](#bib.bib30)), which is based on MATH ([Hendrycks et al., 2021](#bib.bib17)). We sample 4 verification chains for each prefix in the dataset with temperature $T = 0.1$ until we have 1K verification CoTs that (1) follow the desired format i.e., the model generated an extractable label for every step in the prefix and (2) the verbalized step labels match the gold labels in the PRM800K dataset annotation, (3) at most 4096 tokens long, and are (4) roughly balanced with respect to final answer correctness.

Roughly 20% of the initial samples satisfied criteria 1 and 2 in our case, which means that about 5K samples in total are needed to obtain 1K filtered samples. [Table 2](#A1.T2 "In A.2 Preprocessing ‣ Appendix A Training data ‣ Process Reward Models That Think") shows the statistics of the final dataset. We also show an example from the 1K training CoTs in [Figure 20](#A1.F20 "In A.1 Sampling ‣ Appendix A Training data ‣ Process Reward Models That Think").

![](img)

Figure 20: Training example from our sampled 1K synthetic chains.

### A.2 Preprocessing

From the sampled verification CoTs, we extract boxed predictions (e.g., `\boxed{correct}` or `\boxed{incorrect}`) for each reasoning step. Then we filter the data as follows:

- •
  CoTs with missing or malformed verification decisions are discarded.
- •
  CoTs where verification decisions don’t match ground truth labels are filtered out. Precisely, we require all step-by-step verification decisions to match the ground truth labels.

Then we clean the data as follows:

- •
  We standardize boxed notation formats.
- •
  Content after the last verification decision is removed.
- •
  Special tokens (e.g., `<think>` and `</think>`) are added to designate verification reasoning.

|                                            |              |
|--------------------------------------------|--------------|
| Correctness Distribution                   |              |
| \# correct                                 | 486 (48.6%)  |
| \# incorrect                               | 514 (51.4%)  |
| Step label distribution                    |              |
| \# correct                                 | 7474 (92.3%) |
| \# Incorrect                               | 625 (7.7%)   |
| Prefix statistics                          |              |
| \# unique questions                        | 869          |
| average steps per prefix                   | 9.5          |
| min \# steps                               | 1            |
| max \# steps                               | 53           |
| Verification Chain Statistics              |              |
| Average verification chain length (tokens) | 1037.0       |
| Min verification chain length (tokens)     | 207          |
| Max verification chain length (tokens)     | 3669         |

Table 2: Statistics of the 1K finetuning dataset.

![](img)

Figure 21: Prompt used to generate synthetic verification chains as described in [Section 3.2](#S3.SS2 "3.2 Finetuning on synthetic data boosts LLM-as-a-judge verification ‣ 3 ThinkPRM ‣ Process Reward Models That Think").

## Appendix B LLM-as-a-Judge Limitations

We show examples of failures from QwQ-32B-Preview and Deepseek-R1-Distill-Qwen-14B when used for LLM-as-judge verification in [Figures 23](#A2.F23 "In Appendix B LLM-as-a-Judge Limitations ‣ Process Reward Models That Think") and [25](#A2.F25 "Figure 25 ‣ Appendix B LLM-as-a-Judge Limitations ‣ Process Reward Models That Think").

![](img)

Figure 22: Degeneration behavior from QwQ-32B-Preview with LLM-as-judge verification. Problem and solution are omitted for brevity.

![](img)

Figure 23: Degeneration behavior from Deepseek-R1-Distill-Qwen-14B with LLM-as-judge verification. Problem and solution are omitted for brevity.

![](img)

Figure 24: An example of problem and solution from OmniMath subset of ProcessBench.

![](img)

Figure 25: Incorrect verification by Deepseek-R1-Distill-Qwen-14B for the problem-solution pair in [Figure 24](#A2.F24 "In Appendix B LLM-as-a-Judge Limitations ‣ Process Reward Models That Think").

## Appendix C Training details

### C.1 Training ThinkPRM

We train our models on the filtered 1K chains using LoRA ([Hu et al., 2022](#bib.bib18)) with rank $r = 32$ and $\alpha = 16$. Specifically, we finetune Qwen-14B-Instruct and R1-Deepseek (14B) for 3 epochs, and QwQ-32B-Preview for 5 epochs using LoRA. We use an effective batch size of 16 and a fixed learning rate of $4 \times 10^{- 4}$ without warmup is used. Training took 1.5 hours for the 14B models and 4.5 hours for QwQ-32B-Preview on a single A100 80GB GPU. Without particularly found QwQ to be hard to train with LoRA and still generates a relatively high percentage of invalid judgments after training. Full training of the model will likely resolve these issues but that would require more compute than we have.

The R1-Distill-Qwen{1.5B,7B} models use full training with the following parameters. The 1.5B model We trained for 3 epochs with an effective batch size of 32, using a constant learning rate of $6 \times 10^{- 5}$ without decay or warmup. We train both models using four RTX A6000 48GB GPU using data parallel. Training the 1.5B model on the 1K chains took about half an hour and the 7B model about two hours.

### C.2 Training Discriminative Verifiers

We train R1-Qwen-14B for 1 epoch over the entire PRM800K dataset using two A100 80GB GPUs with a batch size of 8 and a learning rate of $6 \times 10^{- 5}$. We use a constant learning rate scheduler with no warmup. Following prior work ([Wang et al., 2023b](#bib.bib46); [Zhang et al., 2025](#bib.bib60)) We train the model using binary cross-entropy to maximize the probability of the tokens “+” and “-” for correct and incorrect steps, respectively. The R1-Qwen-1.5B model is trained with the same infrastructure with a batch size of 64 and a learning rate of $1 \times 10^{- 4}$ with a warm up ratio of 10%.

## Appendix D Results on ProcessBench before and after finetuning

[Table 3](#A4.T3 "In Appendix D Results on ProcessBench before and after finetuning ‣ Process Reward Models That Think") shows the performance numbers of LLM-as-a-Judge and ThinkPRM on ProcessBench.

|                 |                |               |               |              |
|-----------------|----------------|---------------|---------------|--------------|
| Model           | LLM-as-a-Judge |               | ThinkPRM      |              |
|                 | OlympiadBench  | OmniMath      | OlympiadBench | OmniMath     |
| Random baseline | 39.1           | 32.7          | 39.1          | 32.7         |
| R1-Qwen-1.5B    | 5.0 (51.4 %)   | 5.4 (55.1 %)  | 76.3 (1.4 %)  | 75.7 (2.4 %) |
| R1-Qwen-7B      | 44.8 (18.2 %)  | 45.7 (20.9 %) | 73.4 (1.1 %)  | 74.0 (1.4 %) |
| R1-Qwen-14B     | 72.8 (13.3 %)  | 67.8 (18.6 %) | 87.3 (2.3 %)  | 85.7 (2.3 %) |
| QwQ-32B-preview | 50.6 (7.9 %)   | 55.5 (10.9 %) | 73.1 (15.1 %) | 73.2 (7.9 %) |

Table 3: Average F1-score on OlympiadBench and OmniMath subsets of ProcessBench ([Zheng et al., 2024](#bib.bib61)) comparing LLM-as-a-Judge to ThinkPRM finetuned on 1K examples. Random baseline for OlympiadBench is 39.1% and for OmniMath is 32.7%. Percentage of bad outputs (repetitions, invalid label formatting, overthinking, etc.) are shown in red. LLM-as-a-judge with reasoning models suffer from issues that limits their utility as generative verifiers.

## Appendix E Evaluation details

This section includes exact details on the test-time scaling shown in [Section 4.2](#S4.SS2 "4.2 Results ‣ 4 Test-time Scaling Experiments ‣ Process Reward Models That Think")

### E.1 Predicting verification labels

Following prior work ([Snell et al., 2024](#bib.bib39); [Beeching et al.,](#bib.bib4) ), we aggregate scores from DiscPRM by using the score of the last step. For ThinkPRM, we first prompt the model to generate the verification chain up to a maximum of 8192 tokens, then we force decode the string “Is the solution correct?” and use $\frac{P{(\text{“yes”})}}{{P{(\text{“yes”})}} + {P{(\text{“no”})}}}$ as the solution score.

### E.2 Best-of-N selection

We sample solutions using a temperature of $T = 0.8$ for Llama-3.2-3B-Instruct and $T = 0.4$ for Qwen-2.5-14B. We instruct all models to think step by step and put the final answer in `\boxed{}`. All our Best-of-N experiments use weighted majority voting, which scores final answers based on the sum of the verifier scores of their solutions ([Uesato et al., 2022](#bib.bib43); [Wu et al., 2024](#bib.bib49); [Sun et al., 2024](#bib.bib41))except for our experiments on AIME ’24, where we use the verifier score directly to rank the solution, as we found this to perform better for all verifiers.

### E.3 Verifier-guided beam search

Under verifier-guided beam search, we sample candidate next steps and score them with the process verifier, then selects top-$K$ out of these to further expand and so on. Our implementation is based on ([Snell et al., 2024](#bib.bib39); [Beeching et al.,](#bib.bib4) ), which maintains $N$ beams in total, and samples $M$ candidate next steps per beam. We set $M = 4$ for all experiments and run search for a maximum of 20 steps per beam. To sample next steps, we use $T = 0.6$ and use double newlines as the step delimiter.

### E.4 Sequential scaling of verifier compute

We achieve budget forcing ([Muennighoff et al., 2025](#bib.bib35)) by triggering the model to think again for $R$ rounds, where each round uses a unique trigger phrase that incites the model to revisit or double-check its earlier verification. We use different trigger phrases for each round since we found that using the same phrase causes the model to repeat what it did in the last round.

We do a maximum of $R = 4$ thinking rounds, and use the phrases “Let me double check”, “Let’s verify again”, and “Did I miss something?”, for rounds 2, 3, and 4 respectively. We do not investigate deeply into optimizing the trigger phrase, but we note that performance may depend on these and we use the same phrases for both ThinkPRM and LLM-as-a-judge to ensure fair comparison.

### E.5 MATH-500 test examples

As running on all 500 examples from MATH-500 will require a lot of compute, we run all our experiments on 100 randomly sampled subsets from MATH-500 ([Hendrycks et al., 2021](#bib.bib17)). We pick the 100 problems such that they cover different difficulty levels, as shown in [Figure 31](#A5.F31 "In E.5 MATH-500 test examples ‣ Appendix E Evaluation details ‣ Process Reward Models That Think").

Figure 28: Histogram of difficulty levels in our 100-problem subset from MATH-500. Figure 31: Scaling of verifier compute by parallel sampling of multiple verification CoTs and averaging their scores. Parallel scaling (ThinkPRM-14B@4 and ThinkPRM-14B@8) further boosts performance curve compared to scoring based on a single CoT (ThinkPRM-14B).

### E.6 Additional results on scaling verifier compute

[Figure 31](#A5.F31 "In E.5 MATH-500 test examples ‣ Appendix E Evaluation details ‣ Process Reward Models That Think") shows results of ThinkPRM-14B of parallel scaling verifier compute by sampling $K = 4$ and $K = 8$ CoTs with temperature $T = 0.6$ and aggregating their scores. Parallel scaling indeed lifts up the accuracy curve of ThinkPRM-14B compared to standard $K = 1$ with greedy decoding. However, performance plateaus rather quickly and $K = 8$ remains comparable to $K = 4$, while slightly better at smaller sampling budgets. [Figure 32](#A5.F32 "In E.6 Additional results on scaling verifier compute ‣ Appendix E Evaluation details ‣ Process Reward Models That Think") compares parallel to sequential scaling under the same token budget. While there is no clear winner, parallel scaling seems to perform slightly better at best-of-8.

Figure 32: Parallel vs. sequential scaling of ThinkPRM compute under the same generation budget with Qwen-2.5-14B generator. Parallel scaling (model@K) is done by independently sampling $K$ verification CoTs and aggregating their scores. Sequential scaling is done by prompting the model $K$ times to revise its own verification for $K$ thinking rounds. Both setups generate up until 8192 tokens per generation. We do not observe a clear winner although parallel scaling seems slightly better especially at larger sampling budgets.

### E.7 Scaling training data of ThinkPRM

Here, we show results when training ThinkPRM-14B and ThinkPRM-1.5B using synthetic data from all PRM800K. The goal is to show that ThinkPRM can still benefit from training on more synthetic data. Here, we train both R1-Distill-Qwen-1.5B and R1-Distill-Qwen-14B on a total of 65K verification CoTs we obtained by sampling and filtering as explained in [Section 3.2](#S3.SS2 "3.2 Finetuning on synthetic data boosts LLM-as-a-judge verification ‣ 3 ThinkPRM ‣ Process Reward Models That Think"). [Figures 38](#A5.F38 "In E.7 Scaling training data of ThinkPRM ‣ Appendix E Evaluation details ‣ Process Reward Models That Think") and [38](#A5.F38 "Figure 38 ‣ E.7 Scaling training data of ThinkPRM ‣ Appendix E Evaluation details ‣ Process Reward Models That Think") show best-of-N performance with ThinkPRM-1.5B and ThinkPRM-14B respectively when trained on 65K and compares it to training on 1K examples. Interestingly, ThinkPRM benefits from additional training, and can further improve the accuracy curve compared to the 1K-trained version on MATH-500. We note, however, that while training on more math data boosts performance on MATH-500, we observe some performance drop on out-of-domain tasks due to the distribution shift.

Figure 35: Best-of-N results with ThinkPRM-1.5B comparing the version trained on 1K examples (used throughout the paper) and a version trained on 65K examples. ThinkPRM benefits from training on more synthetic data as the performance can further improve with more training. Figure 38: Best-of-N results with ThinkPRM-14B comparing the version trained on 1K examples (used throughout the paper) and a version trained on 65K examples. ThinkPRM benefits from training on more synthetic data as the performance can further improve with more training.

### E.8 Results with automatic labels

[Table 4](#A5.T4 "In E.8 Results with automatic labels ‣ Appendix E Evaluation details ‣ Process Reward Models That Think") shows performance when filtering training data based on manual labels (PRM800K) vs automatic labels (Math-Shepherd) ([Wang et al., 2023b](#bib.bib46)). ThinkPRM still performs well even with automatic labels, and comparably to manual labels.

| Model                         | OlympiadBench | OmniMath |
|-------------------------------|---------------|----------|
| ThinkPRM-1.5B (PRM800K)       | 76.3          | 75.7     |
| ThinkPRM-1.5B (Math-shepherd) | 75.8          | 76.5     |

Table 4: Comparison of ThinkPRM-1.5B trained on PRM800K vs Math-shepherd step labels.

### E.9 Verifier performance in terms of problem difficulty

Figure 39: ThinkPRM helps with challenging reasoning problems compared to DiscPRM. The generator model here is Qwen-2.5-14B for MATH-500 and Qwen-2.5-32B-Instruct for GPQA.

We the difficulty We do not estimate the difficulty over MATH problem since each problem in MATH is annotated based on 1 of 5 difficulty levels. For GPQA-Physics problems, we first compute the pass@1 rate of Qwen2.5-32B-Instruct for every problem by sampling 32 solutions for each problem. Then, we bin the pass@1 rates into four different bins and use the bin assignment for each problem as the difficulty level. As discussed in [Section 5.6](#S5.SS6 "5.6 ThinkPRM helps with difficult reasoning problems ‣ 5 Analysis and Discussion ‣ Process Reward Models That Think"), [Figure 39](#A5.F39 "In E.9 Verifier performance in terms of problem difficulty ‣ Appendix E Evaluation details ‣ Process Reward Models That Think") show how ThinkPRM helps more with verifying hard problems compared to DiscPRM.

|             | Prompt                 | OlympiadBench | OmniMath      |
|-------------|------------------------|---------------|---------------|
| QwQ-32B     | Single Yes/No          | 50.6 (7.9 %)  | 55.5 (3.2 %)  |
|             | Bad-step-index         | 65.4 (18.3 %) | 69.0 (16.8 %) |
|             | Decision-for-each-step | 40.1 (6.4 %)  | 36.6 (9.2 %)  |
| R1-Qwen-14B | Single Yes/No          | 72.8 (13.3 %) | 67.8 (18.6 %) |
|             | Bad step index         | 77.7 (17.0 %) | 76.6 (17.9 %) |
|             | Decision-for-each-step | 73.3 (14.6 %) | 71.4 (14.7 %) |

Table 5: F1-score on OlympiadBench and OmniMath subsets from ProcessBench with different prompts. Ratio of invalid judgments is shown in red.

![](img)

![](img)

## Appendix F More details on LLM-as-judge verification

The instruction used for LLM-as-judge verification in [Section 3.1](#S3.SS1 "3.1 LLM-as-a-judge PRMs are suboptimal ‣ 3 ThinkPRM ‣ Process Reward Models That Think") is shown in [Figure 42](#A6.F42 "In Appendix F More details on LLM-as-judge verification ‣ Process Reward Models That Think"), which we refer to as Single-label. [Table 5](#A5.T5 "In E.9 Verifier performance in terms of problem difficulty ‣ Appendix E Evaluation details ‣ Process Reward Models That Think") shows performance of QwQ-32B-Preview and Qwen-Deepseek-R1-14B with two more instructions. Bad-step-index refers to instructing the model to find the index of the first incorrect step and then if a step is found generate a single yes/no label regarding the solution correctness. Decision-for-each-step instructs the model to critique and produce a boxed label for each step. This instruction is shown in [Figure 21](#A1.F21 "In A.2 Preprocessing ‣ Appendix A Training data ‣ Process Reward Models That Think"). We observe high ha variance in verification performance and invalid judgment ratio depending on the prompt.

![](img)

Figure 42: Prompt used for LLM-as-a-judge verification in [Section 3.1](#S3.SS1 "3.1 LLM-as-a-judge PRMs are suboptimal ‣ 3 ThinkPRM ‣ Process Reward Models That Think")

We also an example from ProcessBench in [Figure 40](#A5.F40 "In E.9 Verifier performance in terms of problem difficulty ‣ Appendix E Evaluation details ‣ Process Reward Models That Think") and the generated verification chain from QwQ-32B-Preview in [Figure 41](#A5.F41 "In E.9 Verifier performance in terms of problem difficulty ‣ Appendix E Evaluation details ‣ Process Reward Models That Think").

## Appendix G Examples from ThinkPRM

[Figure 44](#A7.F44 "In Appendix G Examples from ThinkPRM ‣ Process Reward Models That Think") shows an example of a verification CoT from ThinkPRM-14B on a problem and solution from the OmniMath subset in ProcessBench, shown in [Figure 43](#A7.F43 "In Appendix G Examples from ThinkPRM ‣ Process Reward Models That Think").

![](img)

Figure 43: Problem and solution from the OmniMath subset of ProcessBench. The verification CoT output by ThinkPRM is shown in [Figure 44](#A7.F44 "In Appendix G Examples from ThinkPRM ‣ Process Reward Models That Think")

![](img)

![](img)

Figure 44: Example output by ThinkPRM-14B, where it verifies and labels every step in the provided prefix via a long verification CoT. The problem and solution are in [Figure 43](#A7.F43 "In Appendix G Examples from ThinkPRM ‣ Process Reward Models That Think")

![](img)

Figure 45: Example of verification of long CoT solution from Qwen3-1.7B-thinking using ThinkPRM-1.5B. ThinkPRM extracts and verifies individual steps embedded in the long CoT.

Experimental support, please [view the build logs](./2504.16828v5/__stdout.txt) for errors. Generated by [ L A T E xml ![\[LOGO\]](img)](https://math.nist.gov/~BMiller/LaTeXML/) .

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
