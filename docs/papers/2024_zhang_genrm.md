---
title: "Generative Verifiers: Reward Modeling as Next-Token Prediction"
authors: "Lunjun Zhang; Arian Hosseini; Hritik Bansal; Mehran Kazemi; Aviral Kumar; Rishabh Agarwal"
year: 2024
source: https://arxiv.org/html/2408.15240
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

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) [![](img) Report Issue](# "Report an Issue") [![](img) Back to Abstract](/abs/2408.15240v3 "Back to abstract page") [![](img) Download PDF](/pdf/2408.15240v3 "Download PDF") [![](img)](javascript:toggleNavTOC(); "Toggle navigation") [![](img)](javascript:toggleReadingMode(); "Disable reading mode, show header and footer")

![](img) ![](img) ![](img)

1.  [Abstract](#abstract1 "In Generative Verifiers: Reward Modeling as Next-Token Prediction")
2.  [1 Introduction](#S1 "In Generative Verifiers: Reward Modeling as Next-Token Prediction")
3.  [2 Preliminaries](#S2 "In Generative Verifiers: Reward Modeling as Next-Token Prediction")
4.  [3 GenRM: Verification as Next-Token Prediction](#S3 "In Generative Verifiers: Reward Modeling as Next-Token Prediction")
    1.  [3.1 Direct Verifier](#S3.SS1 "In 3 GenRM: Verification as Next-Token Prediction ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")
    2.  [3.2 Unifying Generation and Verification](#S3.SS2 "In 3 GenRM: Verification as Next-Token Prediction ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")
    3.  [3.3 Chain-of-Thought Verifiers (GenRM-CoT)](#S3.SS3 "In 3 GenRM: Verification as Next-Token Prediction ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")
5.  [4 Experiments](#S4 "In Generative Verifiers: Reward Modeling as Next-Token Prediction")
    1.  [4.1 Generative Verifiers Outperform Standard Verification Approaches](#S4.SS1 "In 4 Experiments ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")
    2.  [4.2 Synergy Between Generation and Verification](#S4.SS2 "In 4 Experiments ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")
    3.  [4.3 Scaling Model Size and Inference-time Compute](#S4.SS3 "In 4 Experiments ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")
    4.  [4.4 Synthetic Rationales: Quantity and Quality Matter](#S4.SS4 "In 4 Experiments ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")
6.  [5 Related Work](#S5 "In Generative Verifiers: Reward Modeling as Next-Token Prediction")
7.  [6 Conclusion & Future Work](#S6 "In Generative Verifiers: Reward Modeling as Next-Token Prediction")
8.  [References](#bib "In Generative Verifiers: Reward Modeling as Next-Token Prediction")
9.  [A Training Data Generation for Verifiers](#A1 "In Appendices ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")
10. [B Hyper-parameters for Verifier Training](#A2 "In Appendices ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")
    1.  [GenRM verifiers](#A2.SS0.SSS0.Px1 "In Appendix B Hyper-parameters for Verifier Training ‣ Appendices ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")
    2.  [Discriminative RMs](#A2.SS0.SSS0.Px2 "In Appendix B Hyper-parameters for Verifier Training ‣ Appendices ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")
    3.  [DPO](#A2.SS0.SSS0.Px3 "In Appendix B Hyper-parameters for Verifier Training ‣ Appendices ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")
11. [C Additional Details](#A3 "In Appendices ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")
    1.  [Data filtering for synthetic verification CoT](#A3.SS0.SSS0.Px1 "In Appendix C Additional Details ‣ Appendices ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")
    2.  [Weighted Self-Consistency](#A3.SS0.SSS0.Px2 "In Appendix C Additional Details ‣ Appendices ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")
12. [D Additional Results](#A4 "In Appendices ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")
13. [E Examples Verification rationales from GenRM-CoT: GSM8K Test and MATH500](#A5 "In Appendices ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")

[License: arXiv.org perpetual non-exclusive license](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2408.15240v3 \[cs.LG\] 22 Feb 2025

# Generative Verifiers: Reward Modeling as Next-Token Prediction

Lunjun Zhang Affiliation: Google DeepMind Affiliation: University of Toronto    Arian Hosseini Affiliation: Google DeepMind    Hritik Bansal Affiliation: Google DeepMind    Mehran Kazemi Affiliation: Google DeepMind    Aviral Kumar Affiliation: Google DeepMind Affiliation: Carnegie Mellon University    Rishabh Agarwal Affiliation: Google DeepMind Affiliation: Core Contribution Affiliation: Mila Affiliation: UCLA

###### Abstract

Verifiers or reward models are often used to enhance the reasoning performance of large language models (LLMs). A common approach is the Best-of-N method, where N candidate solutions generated by the LLM are ranked by a verifier, and the best one is selected. While LLM-based verifiers are typically trained as discriminative classifiers to score solutions, they do *not* utilize the text generation capabilities of pretrained LLMs. To overcome this limitation, we instead propose training verifiers using the ubiquitous next-token prediction objective, jointly on verification and solution generation. Compared to standard verifiers, such generative verifiers (GenRM) can benefit from several advantages of LLMs: they integrate seamlessly with instruction tuning, enable chain-of-thought reasoning, and can utilize additional test-time compute via majority voting for better verification. We demonstrate that GenRM outperforms discriminative, DPO verifiers, and LLM-as-a-Judge, resulting in large performance gains with Best-of-N, namely ${5\%}\rightarrow{45.3\%}$ on algorithmic tasks and ${73\%}\rightarrow{93.4\%}$ on GSM8K. In easy-to-hard generalization settings, we observe improvements of ${28\%}\rightarrow{44.6\%}$ on MATH, and ${37.9\%}\rightarrow{53.5\%}$ on MMLU abstract algebra. Furthermore, we find that training GenRM with synthetic verification rationales is sufficient to pick out subtle errors on math problems. Finally, we demonstrate that GenRM scales favorably with model size and test-time compute.

### 1 Introduction

Figure 1: Generative Verifiers outperform standard verification approaches in terms of Best-of-N on reasoning tasks, with a fixed generator. Here, $\Delta$ represents the improvement in number of problems solved with Best-of-N using GenRM-CoT. GenRM-CoT leverages the generation capabilities of LLMs, enabling a finetuned verifier to utilize chain-of-thought verification to detect subtle reasoning errors. For algorithmic tasks, we report average performance using Gemma-2B on Last Letter Concat ([Wei et al., 2022](#bib.bib47)) and BBH Word Sorting ([Suzgun et al., 2022](#bib.bib41)). For math reasoning, we train Gemma2-9B verifiers on GSM8K and evaluate their performance on GSM8K test (middle) and *easy-to-hard* generalization on MATH500 ([Lightman et al., 2023](#bib.bib22)). For math tasks, LLM-as-a-Judge utilizes Gemini 1.0 Pro, which we used for synthetic verification rationales for training. For each task, the generated solutions in Best-of-N are the same; the only difference is the verifier. Math tasks use model-generated verification rationales for training GenRM-CoT. Data will be released at: [https://sites.google.com/view/generative-reward-models](https://sites.google.com/view/generative-reward-models).

While large language models (LLMs) demonstrate remarkable capabilities, they often confidently make logical and factual mistakes ([Zhang et al., 2023](#bib.bib57)). These mistakes pose a significant challenge for reasoning problems, where a single mistake can invalidate the solution. A common strategy to address this issue is Best-of-N ([Charniak and Johnson, 2005](#bib.bib8); [Cobbe et al., 2021](#bib.bib11)): the LLM generates N candidate solutions for a given problem, and a learned reward model, referred to as a “verifier”, ranks these solutions and picks the most suitable one. The effectiveness of this strategy hinges on how accurate the verifier is, making it crucial to identify better approaches for training verifiers.

LLM-based verifiers for reasoning are typically trained as discriminative reward models (RMs) to assign numerical scores to candidate solutions, which is then used to classify them as correct or incorrect ([Cobbe et al., 2021](#bib.bib11); [Lightman et al., 2023](#bib.bib22); [Wang et al., 2023](#bib.bib44)). However, this scoring approach does not utilize the text-generation capabilities that LLMs are fundamentally designed for. As a result, discriminative RMs miss out on the inherent strengths of generative LLMs, such as unified instruction tuning ([Chung et al., 2022](#bib.bib10)), chain-of-thought (CoT) reasoning ([Wei et al., 2022](#bib.bib47)), and utilizing additional inference-time computation for better performance ([Wang et al., 2022](#bib.bib46); [Brown et al., 2024](#bib.bib7)). While LLM-as-a-Judge ([Zheng et al., 2024](#bib.bib58)), which simply prompts off-the-shelf generative LLMs, also offers the above advantages, it typically underperforms trained LLMs-based verifiers on reasoning tasks, which we also observe in [Figure 1](#S1.F1 "Figure 1 ‣ 1 Introduction ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction").

[TABLE]

Figure 2: Example using generative CoT verifier on GSM8K test. LLM-generated solutions often sound convincing even when they are wrong, making verification a challenging task. Here, the solution is incorrect because it has ignored the word ‘each’ in the problem. While the discriminative RM fails to recognize this subtle mistake in the solution, our GenRM-CoT verifier reliably detects the error. This is because GenRM-CoT was trained with next-token prediction on synthetic chain-of-thought rationales, enabling it to explicitly reason about the solution. Note that GenRM-CoT refers to CoT reasoning in the verification process (the solutions typically also contain CoT, but not for verification). The full verification output can be found in [Table E.12](#A5.T12 "Table E.12 ‣ Appendix E Examples Verification rationales from GenRM-CoT: GSM8K Test and MATH500 ‣ Appendices ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction").

In this work, we propose *training* verifiers with next-token prediction, which we call GenRM, to leverage the text generation capabilities of LLMs ([Figure 2](#S1.F2 "Figure 2 ‣ 1 Introduction ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")). Concretely, to produce a numerical score for a solution, the verifier now uses a prompt such as ‘Is the answer correct?’, and represents the score as the probability of a single text token (e.g., ‘Yes’ or ‘No’). GenRM naturally supports CoT reasoning ([Wei et al., 2022](#bib.bib47)): it can be trained to reason explicitly by generating a verbalized rationale before predicting correctness using ‘Yes’ or ‘No’ token ([Figure 3](#S1.F3 "Figure 3 ‣ 1 Introduction ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")), assuming rationales are available during training. We can further boost verification accuracy of CoT verifiers using majority-voting ([Wang et al., 2022](#bib.bib46)): sampling multiple CoT rationales and calculating the average score of the ‘Yes’ token across all rationales, enabling the use of inference-time compute for verification. Moreover, GenRM’s next-token prediction training enables unifying solution generation with verification, which has been difficult with DPO verifiers ([Rafailov et al., 2024](#bib.bib33); [Hosseini et al., 2024](#bib.bib17)), potentially improving verification through positive transfer from solution.

Our results show that GenRM outperforms discriminative RMs, LLM-as-a-Judge, and self-consistency on algorithmic string manipulation and math reasoning tasks ([Figure 1](#S1.F1 "Figure 1 ‣ 1 Introduction ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")). Best-of-N performance further improves with GenRM-CoT that uses majority-voting, nearly matching performance with oracle verifier on algorithmic tasks. On GSM8K, when using a Gemma2-9B GenRM-CoT verifier on solutions from Gemini 1.0 Pro, we observe an improvement from ${73\%}\rightarrow{93.4\%}$ in terms of the number of problems solved, surpassing GPT-4 and Gemini 1.5 Pro. Furthermore, GenRM-CoT trained on grade-school math problems exhibit *easy-to-hard* generalization, solving 17% more high-school competition problems in MATH500 ([Lightman et al., 2023](#bib.bib22)) with Best-of-32. Moreover, we find that generative verifiers scale more favorably than discriminative verifiers as we increase model capacity, and outperform LLM-as-a-Judge as we scale inference-time compute with majority voting. Overall, generative verifiers hold significant potential for improving the reasoning capabilities of LLMs.

Figure 3: An illustration of generative verifiers, namely GenRM and GenRM-CoT. Given a question and a candidate solution, GenRM directly finetunes an LLM to answer the question ‘Is the answer correct (Yes/No)?’ via SFT on the next-token response corresponding to either ‘Yes’ or ‘No’. During inference, the verifier score is obtained by extracting the probability of the ‘Yes’ token ([4](#S3.E4 "In 3.1 Direct Verifier ‣ 3 GenRM: Verification as Next-Token Prediction ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")). In comparison, GenRM-CoT finetunes a LLM to produce verification chain-of-thought (CoT) rationale before yielding the final Yes/No token. At test-time, we sample multiple CoT rationales and use majority voting to compute the average probability of ‘Yes’, enabling GenRM-CoT to utilize additional inference-compute for better verification.

### 2 Preliminaries

An autoregressive language model generates an output sequence $\mathbf{y} = {(y_{1},y_{2},\ldots,y_{T})}$ given a input context $\mathbf{x}$ (e.g., math problem) by predicting tokens one at a time, based on the previously generated tokens. Assuming that the language model is parameterized by $\theta$, the conditional probability distribution of generating a sequence $\mathbf{y}$ given context $\mathbf{x}$ is

|     |                                                                                                                                                         |     |     |
|-----|---------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | ${p_{\theta}\hspace{0pt}{(\mathbf{y}\mid\mathbf{x})}} = {\prod\limits_{t = 1}^{T}{p_{\theta}\hspace{0pt}{(y_{t}\mid{\mathbf{x},y_{\phantom{} < t}})}}}$ |     | (1) |

with the convention $y_{\phantom{} < 1} = \varnothing$ and $\mathbf{y}_{\phantom{} < t} = {(y_{1},y_{2},\ldots,y_{t - 1})}$. For ease of notation, we define ${p_{\theta}\hspace{0pt}{(y_{t}\mid\mathbf{x})}}:={p_{\theta}\hspace{0pt}{(y_{t}\mid{\mathbf{y}_{\phantom{} < t},\mathbf{x}})}}$. For a vocabulary size $M$, the probability of predicting the $t$-th token $y_{t}$, $p_{\theta}\hspace{0pt}{(y_{t}\mid\mathbf{x})}$, is determined using a softmax with temperature $\gamma$ on logit scores $z$ of all the tokens: ${{p_{\theta}\hspace{0pt}{(y_{t}\mid\mathbf{x})}} = \frac{\exp{({z_{t}/\gamma})}}{\sum_{i = 1}^{M}{\exp{({z_{i}/\gamma})}}}},{{\text{where}\hspace{0pt}z_{t}} = {{logit}_{\theta}\hspace{0pt}{(y_{t}\mid{\mathbf{x},\mathbf{y}_{\phantom{} < t}})}}}$. Higher values of temperature $\gamma$ introduce more randomness, while setting temperature $\tau = 0$ makes the output deterministic, which corresponds to greedy decoding.

Next-token prediction is the typical approach for pre-training and fine-tuning LLMs. In particular, supervised fine-tuning (SFT) minimizes the cross-entropy loss between the model’s predicted next token and the actual target token in a given sequence. Given a dataset $\mathcal{D} = {\{{(x,y)}\}}$ of input context $\mathbf{x}$ and target response $\mathbf{y}$, the SFT loss is given by:

|     |                                                                                                                                                                                                                                                                                                      |     |     |
|-----|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $${{\mathcal{L}_{\text{SFT}}\hspace{0pt}{(\theta,\mathcal{D})}} = {- {{\mathbb{E}}_{{(\mathbf{x},\mathbf{y})} \sim \mathcal{D}}\hspace{0pt}\left\lbrack {\sum\limits_{t = 1}^{|\mathbf{y}|}{{\log p_{\theta}}\hspace{0pt}{(y_{t}\mid{\mathbf{x},\mathbf{y}_{\phantom{} < t}})}}} \right\rbrack}}}.$$ |     | (2) |

Best-of-N is a widely-used approach to improve the reasoning performance of LLMs ([Cobbe et al., 2021](#bib.bib11); [Lightman et al., 2023](#bib.bib22)). Specifically, given a test problem, we sample N candidate solutions from a generator LLM. These candidates are then scored using a learned verifier or reward model, and the highest-scoring solution is selected as the final answer. A better verifier increases the chance of selecting the correct solution, improving test accuracy.

Discriminative Verifiers. The prevalent approach of training verifiers for reasoning domains is to fine-tune an LLM as a classifier on a dataset of correct and incorrect solutions generated from a fixed LLM, using the binary cross-entropy loss. To do so, these verifiers directly assign a numerical score ${r_{\theta}\hspace{0pt}{(\mathbf{x},\mathbf{y})}} \in {\lbrack{0,1}\rbrack}$ to estimate the probability that a solution $\mathbf{y}$ is correct for a problem $\mathbf{x}$. As such, these verifiers do not utilize the text generation the capabilities of LLMs. Given a reward-modeling (RM) dataset $\mathcal{D}_{R\hspace{0pt}M} = {\mathcal{D}_{\text{incorrect}}\bigcup\mathcal{D}_{\text{correct}}}$, we train discriminative RMs as follows:

|     |                                                                     |                                                                                                                                                                                                                                                                                                                                                                                               |     |     |
|-----|---------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | ${\mathcal{L}{(\theta,\mathcal{D}_{R\hspace{0pt}M})}} = \phantom{}$ | ${{- {{\mathbb{E}}_{{(\mathbf{x},\mathbf{y}^{+})} \sim \mathcal{D}_{\text{correct}}}\hspace{0pt}\left\lbrack {{\log r_{\theta}}\hspace{0pt}{(\mathbf{x},\mathbf{y}^{+})}} \right\rbrack}} - {{\mathbb{E}}_{{(\mathbf{x},\mathbf{y}^{-})} \sim \mathcal{D}_{\text{incorrect}}}\hspace{0pt}\left\lbrack {\log{({1 - {r_{\theta}\hspace{0pt}{(\mathbf{x},\mathbf{y}^{-})}}})}} \right\rbrack}},$ |     |     |
|     |  where                                                              | ${{r_{\theta}\hspace{0pt}{(\mathbf{x},\mathbf{y})}} = {\text{sigmoid}\hspace{0pt}{(z_{c\hspace{0pt}l\hspace{0pt}s})}}},\text{and}\quad{z_{c\hspace{0pt}l\hspace{0pt}s} = {{logit}_{\theta}\hspace{0pt}{({c\hspace{0pt}l\hspace{0pt}s}\mid{\mathbf{y},\mathbf{x}})}}}$                                                                                                                         |     | (3) |

where $\mathbf{y}^{+}$ are correct and $\mathbf{y}^{-}$ are incorrect solutions, and $c\hspace{0pt}l\hspace{0pt}s$ corresponds to a special vocabulary token. In this work, we always use a balanced data mixture between correct ($\mathcal{D}_{\text{correct}}$) and incorrect ($\mathcal{D}_{\text{incorrect}}$) problem-solution pairs.

LLM-as-a-Judge does not finetune a verifier from a pretrained LLM, but simply prompts the LLM to perform the task of verification or self-critique ([Zheng et al., 2024](#bib.bib58); [Bai et al., 2022](#bib.bib4)). LLM-judge sometimes uses reference-guided grading, where the LLM is given a reference solution to compare to.

### 3 GenRM: Verification as Next-Token Prediction

Discriminative LLM-based verifiers ([3](#S2.E3 "In 2 Preliminaries ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")) do not utilize the text generation capabilities of pretrained LLMs. To address this issue, we propose training generative verifiers, which we call GenRM, using standard next-token prediction ([2](#S2.E2 "In 2 Preliminaries ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")). To do so, GenRM represents solution correctness using the LLM’s probability distribution over tokens, instead of predicting a separate numerical score. This keeps the generation abilities of GenRM intact as the verification decision is just another token, while also enabling several advantages that come for “free” with LLMs, such as unified training for solution generation and verification, chain-of-thought reasoning, and inference-time computation.

#### 3.1 Direct Verifier

In its simplest form, GenRM predicts whether a solution is correct using a single ‘Yes’ or ‘No’ token ([Figure 3](#S1.F3 "Figure 3 ‣ 1 Introduction ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction"), top). This can be done by maximizing ${\log p_{\theta}}\hspace{0pt}{(\text{‘Yes’}\mid{(\mathbf{x},\mathbf{y}^{+})})}$ for correct solutions $\mathbf{y}^{+}$ and ${\log p_{\theta}}\hspace{0pt}{(\text{‘No’}\mid{(\mathbf{x},\mathbf{y}^{-})})}$ for incorrect solutions $\mathbf{y}^{-}$. To do so, we minimize the SFT loss in ([2](#S2.E2 "In 2 Preliminaries ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")) on the dataset $\mathcal{D}_{Direct}$ containing problem-solution pairs and a ‘Yes‘ or ‘No’ verification token:

|     |                                                                                                                                                                                                                         |     |
|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $\boxed{\mathcal{D}_{Direct} = {{\{{(\mathbf{x},\mathbf{y}^{+},\mathbf{I})},\text{‘Yes’}\}}\bigcup{\{{(\mathbf{x},\mathbf{y}^{-},\mathbf{I})},\text{‘No’}\}}}},{\mathbf{I} = \text{‘Is the answer correct (Yes/No)?’}}$ |     |

At inference, we use the likelihood of the ‘Yes’ token as the verifier’s score for re-ranking solutions:

|     |                                                                                                                                              |     |     |
|-----|----------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | ${{r_{\text{Direct}}\hspace{0pt}{(\mathbf{x},\mathbf{y})}} = {p_{\theta}\hspace{0pt}{(\text{Yes}\mid{\mathbf{x},\mathbf{y},\mathbf{I}})}}}.$ |     | (4) |

This score takes into account the verifier’s confidence about its correctness prediction, which reduces the chance of being wrong at test-time when using a binary ‘Yes’ or ‘No’ prediction.

#### 3.2 Unifying Generation and Verification

GenRM seamlessly integrates reward modeling, which distinguishes between correct and incorrect solutions, with SFT for generating correct solutions. This can be done by simply changing the data mixture in the SFT loss ([2](#S2.E2 "In 2 Preliminaries ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")) to include both verification and generation tasks. Given a verification dataset $\mathcal{D}_{\text{verify}}$, which can be $\mathcal{D}_{\text{Direct}}$ or $\mathcal{D}_{\text{CoT}}$ (discussed below) of problems-solution pairs with correctness tokens (optionally with CoT rationales), GenRM minimizes the loss:

|     |                                                                                                                                                                                                                                                                                 |     |     |
|-----|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $$\boxed{{\mathcal{L}_{\text{GenRM}}\hspace{0pt}{(\theta,\mathcal{D}_{\text{verify}})}} = {{\mathcal{L}_{\text{SFT}}\hspace{0pt}{(\theta,\mathcal{D}_{\text{verify}})}} + {\lambda\hspace{0pt}\mathcal{L}_{\text{SFT}}\hspace{0pt}{(\theta,\mathcal{D}_{\text{correct}})}}}},$$ |     | (5) |

where $\lambda > 0$ is a hyperparameter that controls the mixture ratio between verification ($\mathcal{D}_{\text{verify}}$) and generating correct solutions ($\mathcal{D}_{\text{correct}}$). This unified training can improve verifier and generation performance via positive transfer between these two related tasks: how to generate a correct solution, and whether a solution is correct. By default, we train GenRM verifiers using the unified loss in ([5](#S3.E5 "In 3.2 Unifying Generation and Verification ‣ 3 GenRM: Verification as Next-Token Prediction ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")).

#### 3.3 Chain-of-Thought Verifiers (GenRM-CoT)

Since verification often involves nuanced reasoning, generative verifiers can naturally benefit from CoT ([Wei et al., 2022](#bib.bib47)). Specifically, we can generate intermediate reasoning steps or critique (CoT) before making a decision about the solution correctness, which may identify subtle reasoning errors missed by direct verifiers ([Figure 3](#S1.F3 "Figure 3 ‣ 1 Introduction ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction"), bottom). To train CoT verifiers, we can minimize the SFT loss $\mathcal{L}_{\text{GenRM}}$ on the dataset $\mathcal{D}_{\text{CoT}}$ containing problem-solution pairs as inputs, and corresponding verification rationales $\mathbf{v}_{\text{CoT}}$ appended with a final question $\mathbf{I}$ and ‘Yes’ or ‘No’ token as targets:

|     |                                                                                                                                                                                                                                                                                                   |     |
|-----|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $\boxed{\mathcal{D}_{\text{CoT}} = {{\{\left( \mathbf{x},\mathbf{y}^{+},\mathbf{I}_{\text{CoT}} \right),{(\mathbf{v}_{\text{CoT}},\mathbf{I},\text{‘Yes’})}\}}\bigcup{\{\left( \mathbf{x},\mathbf{y}^{-},\mathbf{I}_{\text{CoT}} \right),{(\mathbf{v}_{\text{CoT}},\mathbf{I},\text{‘No’})}\}}}}$ |     |

where $\mathbf{I}_{\text{CoT}} = \phantom{}$‘Let’s verify step by step.’. Notably, these rationales can either be human or LLM-generated, both of which we explore in this work. During inference, we first generate a CoT rationale $\mathbf{v}_{\text{CoT}}$ from GenRM-CoT and then use the probability of ‘Yes’ for assigning the correctness score:

|     |                                                       |                                                                                                                                                                                                                                      |     |     |
|-----|-------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $r_{\text{CoT}}\hspace{0pt}{(\mathbf{x},\mathbf{y})}$ | $= p_{\theta}{(\text{Yes} \mid \mathbf{x},\mathbf{y},\mathbf{I}_{\text{CoT}},\mathbf{v}_{\text{CoT}},\mathbf{I})},\text{where}\mathbf{v}_{\text{CoT}} \sim p_{\theta}{( \cdot \mid \mathbf{x},\mathbf{y},\mathbf{I}_{\text{CoT}})},$ |     | (6) |

Compared to ([4](#S3.E4 "In 3.1 Direct Verifier ‣ 3 GenRM: Verification as Next-Token Prediction ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")) that only uses the instruction $\mathbf{I}$ to produce a score, the above CoT reward additionally conditions on $\mathbf{I}_{\text{CoT}}$ and self-generated $\mathbf{v}_{\text{CoT}}$ before getting a score via instruction $\mathbf{I}$.

Inference-time compute for CoT verifier. When sampling verification CoTs, the generative verifier can use different reasoning paths and yield different correctness probabilities for the same problem-solution pair. As such, we would like to marginalize out these reasoning paths to select the most consistent correctness answer ([Wang et al., 2022](#bib.bib46)). To do so, we use majority voting where we first generate $K$ verification CoT rationales, and average the CoT-verifier score for these rationales:

|     |                                                                                                                                                                                                                                                                                                                                           |     |     |
|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $$r_{\text{MajV@K}}{(\mathbf{x},\mathbf{y})} = \frac{1}{K}\sum\limits_{i = 1}^{K}p_{\theta}\left( \text{Yes} \mid \mathbf{x},\mathbf{y},\mathbf{I}_{\text{CoT}},\mathbf{v}_{\text{CoT}}^{(i)},\mathbf{I} \right),\text{where}\mathbf{v}_{\text{CoT}}^{(i)} \sim p_{\theta}{( \cdot \mid \mathbf{x},\mathbf{y},\mathbf{I}_{\text{CoT}})}$$ |     | (7) |

Since individual verification rationales from CoT verifiers can have reasoning errors, majority voting can mitigate the impact of such errors by averaging correctness scores across multiple rationales. Importantly, this means that GenRM-CoT can leverage additional inference-time compute to improve its accuracy, which discriminative verifiers cannot do. Unless otherwise specified, we report GenRM-CoT performance based on majority voting with 32 votes, that is, $K = 32$ in ([7](#S3.E7 "In 3.3 Chain-of-Thought Verifiers (GenRM-CoT) ‣ 3 GenRM: Verification as Next-Token Prediction ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")).

Synthetic Verification CoT Rationales for Training Verifying LLM solutions with human-generated rationales can become increasingly expensive and challenging as LLMs surpass human reasoning abilities. To address this challenge, we explore using synthetically-generated rationales on GSM8K. One naive approach is to simply use the ‘Let’s verify step by step’ prompt given a problem-solution pair, and keep the generated rationales only when they accurately verify the correctness of a solution ([Singh et al., 2023](#bib.bib38); [Zelikman et al., 2022](#bib.bib55)). However, such rationales (after filtering based on final yes/no responses) are still often of poor quality, due to 50% accuracy from random guessing.

To improve the quality of synthetic rationales, we provide a reference solution in addition to the problem and solution to verify (see [Table A.2](#A1.T2 "Table A.2 ‣ Appendix A Training Data Generation for Verifiers ‣ Appendices ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")), making it easier for an LLM to point out any reasoning error in the provided solution. This idea is similar to reference-guidance grading ([Zheng et al., 2024](#bib.bib58)). Here, a reference solution could be any model-generated solution that arrives at the correct final answer. After initial data generation, we then filter the synthetic rationales using their verification correctness. Note that we condition on a reference solution only to generate training data, but do not include it during actual finetuning of the verifier, so that there is no train/test mismatch.

[TABLE]

Figure 4: An example on MATH where GenRM-CoT (trained only on GSM) detects a reasoning error. The solution made a mistake in simplifying an intermediate step. Both Discriminative RM and GenRM-CoT models have only been trained on GSM8K. In this case, discriminative RM fails to classify the solution as incorrect, whereas GenRM-CoT utilizes chain of thoughts to catch this mistake. See [Table E.14](#A5.T14 "Table E.14 ‣ Appendix E Examples Verification rationales from GenRM-CoT: GSM8K Test and MATH500 ‣ Appendices ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction") for details.

### 4 Experiments

In this section, we evaluate the efficacy of next-token prediction and chain-of-thought reasoning for verification compared to standard verification approaches. To this end, we compare GenRM and standard verifiers on a number of reasoning tasks to answer the following questions: (1) How does GenRM compare to discriminative verifiers and other approaches? (2) Does unified training of GenRM improve generation and verification performance? (3) Can GenRM effectively utilize CoT reasoning to improve its performance? (4) How does GenRM scale with model size and inference-time compute?

Tasks. We focus on the following tasks and put details about data generation in [Appendix A](#A1 "Appendix A Training Data Generation for Verifiers ‣ Appendices ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction"):

- •
  Algorithmic reasoning. We use two difficult string manipulation tasks, namely Last Letter Concatenation ([Wei et al., 2022](#bib.bib47)) and Word Sorting from Big-Bench ([Suzgun et al., 2022](#bib.bib41)). We train verifiers on word lists of length {2,3,4}, and evaluate their generalization on length {5,6}. Note that this is a case of length generalization for the verification task.
- •
  Math reasoning. We train grade-school math verifiers on the GSM8K dataset from [Cobbe et al. (2021)](#bib.bib11) that popularized test-time verification. We evaluate these verifiers on the GSM8K test set as well as their *easy-to-hard generalization* on much harder MATH dataset ([Hendrycks et al., 2021](#bib.bib16)), using the same held-out set of 500 MATH problems as [Lightman et al. (2023)](#bib.bib22). We also evaluated model performance on the mathematical tasks in MMLU ([Hendrycks et al., 2020](#bib.bib15)) dataset.

Figure 5: Sample-Efficient Scaling with Generative Verifiers. GenRM-CoT outperforms other methods, especially for length generalization on algorithmic tasks (Gemma-2B verifiers) and easy-to-hard generalization on MATH (Gemma2-9B verifiers). Specifically, GenRM-CoT nearly matches the oracle verifier’s Best-of-N performance on algorithmic tasks. On MATH, it matches discriminative verifier’s Best-of-32 performance using $6.4 \times$ fewer solutions.

Figure 6: Easy-to-Hard Generalization on MATH, with Gemma2-9B verifiers trained only on significantly easier grade-school math problems. Compared to discriminative RMs, GenRM-CoT performs especially well on Pre-Algebra, Algebra, and Pre-Calculus, and obtains superior performance across all difficulty levels.

Baselines. We compare GenRM to the following verification approaches:

- •
  Discriminative RM ([Cobbe et al., 2021](#bib.bib11)) or ORM is the prevalent approach for training verifiers for test-time re-ranking on reasoning tasks (§[2](#S2 "2 Preliminaries ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")), and serves as our main baseline.
- •
  LLM-as-a-Judge ([Zheng et al., 2024](#bib.bib58)) uses an off-the-shelf pretrained LLM for verification. To do so, we use a CoT prompt to produce 32 verification rationales that is used for correctness prediction and pick the majority-vote correctness answer.
- •
  DPO ([Rafailov et al., 2024](#bib.bib33)): Following [Hosseini et al. (2024)](#bib.bib17), we use this preference optimization approach for training verifiers on preference pairs with incorrect and correct solutions.
- •
  Self-consistency ([Wang et al., 2022](#bib.bib46)): A simple approach to use test-time compute *without* verifiers: sample multiple solutions from the LLM generator and pick the most common answer.

Note that self-consistency and test-time verification are complementary approaches, and can be often combined via weighted self-consistency to further boost performance, as shown in [Figure 8](#S4.F8 "Figure 8 ‣ 4.1 Generative Verifiers Outperform Standard Verification Approaches ‣ 4 Experiments ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction").

Evaluation protocol. Following [Cobbe et al. (2021)](#bib.bib11); [Lightman et al. (2023)](#bib.bib22), we primarily use Best-of-N performance in terms of the percentage of problems solved using a fixed generator (§[2](#S2 "2 Preliminaries ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")) with learned verifiers, and report average accuracy on the test set. We also report test RM accuracy, which measures whether the verifier accurately classifies incorrect and correct solutions. While these two metrics are correlated, RM accuracy only evaluates the verifier’s point-wise accuracy, while Best-of-N evaluates the verifier’s ability to rank solutions for choosing the correct one.

Models & Training. For training verifiers, we use open-weights Gemma models ([Gemma Team et al., 2024a](#bib.bib12); [Gemma Team et al., 2024b](#bib.bib13)), specifically Gemma-2B for algorithmic tasks, and Gemma 2B, 7B, and Gemma-2 9B for GSM8K. For solution generation as well as LLM-as-a-Judge, we use Gemma 2B for algorithmic tasks and Gemini 1.0 Pro ([Google et al., 2023](#bib.bib14)) for GSM8K. For verification CoT rationales, we generate oracle rationales for algorithmic tasks programmatically ([Table A.1](#A1.T1 "Table A.1 ‣ Appendix A Training Data Generation for Verifiers ‣ Appendices ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")); for GSM8K, we generate synthetic rationales using Gemini 1.0 Pro with reference-guided grading ([Table A.2](#A1.T2 "Table A.2 ‣ Appendix A Training Data Generation for Verifiers ‣ Appendices ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")). See [Appendix B](#A2 "Appendix B Hyper-parameters for Verifier Training ‣ Appendices ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction") for hyperparameter details.

#### 4.1 Generative Verifiers Outperform Standard Verification Approaches

GenRM outperforms LLM-as-a-Judge and DPO verifiers ([Figure 1](#S1.F1 "Figure 1 ‣ 1 Introduction ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")), while performing comparably or slightly better than discriminative verifiers ([Figure D.1](#A4.F1 "Figure D.1 ‣ Appendix D Additional Results ‣ Appendices ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")). GenRM-CoT substantially improves the Best-of-N performance over GenRM. In particular, on the algorithmic tasks with oracle verification CoTs, GenRM-CoT nearly *matches* the oracle verifier performance.

On GSM8K, GenRM-CoT consistently outperforms other methods ([Figure 6](#S4.F6 "Figure 6 ‣ 4 Experiments ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction"), middle), even though the synthetic CoT rationales for training may contain errors. Qualitatively, GenRM-CoT is able to detect subtle reasoning errors that are missed by discriminative or direct GenRM verifiers (see [Figure 2](#S1.F2 "Figure 2 ‣ 1 Introduction ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction"), [4](#S3.F4 "Figure 4 ‣ 3.3 Chain-of-Thought Verifiers (GenRM-CoT) ‣ 3 GenRM: Verification as Next-Token Prediction ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction"), and [15](#S4.F15 "Figure 15 ‣ 4.4 Synthetic Rationales: Quantity and Quality Matter ‣ 4 Experiments ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")).

| MMLU Dataset            | Base Model (Pass@1) | Disc-RM | GenRM-CoT | Improvement |
|-------------------------|---------------------|---------|-----------|-------------|
| elementary_mathematics  | 80.1%               | 90.6%   | 91.1%     | +0.5%       |
| high_school_mathematics | 52.2%               | 74.8%   | 76.1%     | +1.3%       |
| college_mathematics     | 47.6%               | 53%     | 56.1%     | +3.1%       |
| abstract_algebra        | 37.9%               | 50%     | 53.50%    | +3.5%       |

Table 1: Performance of different methods on math tasks from the MMLU ([Hendrycks et al., 2020](#bib.bib15)) dataset. The evaluation uses an easy-to-hard generalization setting, where the verifier is trained only on grade school math. We highlight the absolute improvement of GenRM-CoT over the Disc-RM baseline. Notably, Gen-CoT demonstrates stronger performance across all tasks, with the improvements being more significant on harder tasks.

Figure 7: Transfer to MMLU College Mathematics (GSM Verifiers), using Best-of-32 evaluation, with solutions generated from Gemini 1.0 Pro. On college-level mathematics, even using a single verification rationale with GenRM-CoT can outperform Discriminative RM. Best-of-32 based on discriminative RM yields a performance of $53.0\%$; as for GenRM-CoT (using 32 majority votes), Best-of-32 gives $56.1\%$.

Easy-to-Hard Generalization. Without any training on MATH, GenRM-CoT results in a $6.4 \times$ better sample efficiency than discriminative verifiers as we increase the number of solutions to verify, and surpasses the strong self-consistency baseline ([Figure 6](#S4.F6 "Figure 6 ‣ 4 Experiments ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction"), right). While [Sun et al. (2024)](#bib.bib40) demonstrate that discriminative verifiers trained on easy MATH problems can generalize to harder MATH problems, GenRM-CoT exhibits a much stronger generalization from *grade-school* math problems to *high-school competition* problems in MATH (see [Figure 6](#S4.F6 "Figure 6 ‣ 4 Experiments ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction") for a score breakdown by subject areas and difficulty levels) and college-level math in MMLU (see [Table 1](#S4.T1 "Table 1 ‣ 4.1 Generative Verifiers Outperform Standard Verification Approaches ‣ 4 Experiments ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")).

Figure 8: Weighted Self-Consistency on MATH.

Leveraging Self-Consistency with Verifiers. Self-consistency and test-time verification can be easily combined to boost Best-of-N performance. To do so, we use weighted self-consistency or majority-voting ([Uesato et al., 2022](#bib.bib43); [Liu et al., 2023](#bib.bib25); [Sun et al., 2024](#bib.bib40)) where we weight each solution according to the verifier’s score, and select the final answer with the largest weight (see [Appendix C](#A3.SS0.SSS0.Px2 "Weighted Self-Consistency ‣ Appendix C Additional Details ‣ Appendices ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction") for details). [Figure 8](#S4.F8 "Figure 8 ‣ 4.1 Generative Verifiers Outperform Standard Verification Approaches ‣ 4 Experiments ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction") shows that weighted SC can indeed improve the vanilla self-consistency (SC); in particular, weighted SC based on GenRM-CoT requires 2.5x fewer solutions than its counterpart based on Discriminative RM to reach the same performance.

#### 4.2 Synergy Between Generation and Verification

Figure 9: SFT on correct solutions enhances verification, both for GenRM and GenRM-CoT, across all tasks. ‘Verification Only’ corresponds to verifiers trained only on verification data, by setting $\lambda = 0$ in ([5](#S3.E5 "In 3.2 Unifying Generation and Verification ‣ 3 GenRM: Verification as Next-Token Prediction ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")). The y-axis of each figure starts from the pass@1 performance of the base generator for each task.

Figure 10: Unifying generation and verification boosts generation performance compared to SFT on correct solutions, in terms of Best-of-N with oracle verifier. The improvement is larger on algorithmic tasks, which use ground-truth verification data, than on GSM8K that relies on synthetic rationales, which may be inaccurate.

Unifying solution generation with verification, as done by GenRM using next-token prediction, consistently improves verification performance across all tasks, as illustrated in [Figure 10](#S4.F10 "Figure 10 ‣ 4.2 Synergy Between Generation and Verification ‣ 4 Experiments ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction"). This improvement is observed for both direct and CoT-based generative verifiers, suggesting that teaching the verifier to imitate correct solutions generally helps. However, adding too much solution generation data can decrease verification performance of GenRM ([Figure D.3](#A4.F3 "Figure D.3 ‣ Appendix D Additional Results ‣ Appendices ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")).

Incorporating CoT verification data into the generator’s training mix leads to better solution generation performance for the GenRM-CoT verifier itself, as evidenced in [Figure 10](#S4.F10 "Figure 10 ‣ 4.2 Synergy Between Generation and Verification ‣ 4 Experiments ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction") by the improved Best-of-N scores with the oracle verifier (Pass@N). This suggests that teaching a generator to perform CoT verification using next-token prediction can deepen its understanding of the generation process itself. Overall, unifying solution generation and verification is mutually beneficial.

#### 4.3 Scaling Model Size and Inference-time Compute

Figure 11: Scaling Inference-time Compute for Verification on GSM8K. By posing reward modeling as next-token prediction, GenRM-CoT can utilize Chain-of-Thought and Majority Voting, to turn additional test-time compute into higher percentage of problems solved under Best-of-N. Here, the horizontal line corresponds to performance of GenRM-CoT verifier with greedy decoding in Eq ([6](#S3.E6 "In 3.3 Chain-of-Thought Verifiers (GenRM-CoT) ‣ 3 GenRM: Verification as Next-Token Prediction ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")).

Figure 12: Model Scaling for Generative Verifiers. We evaluate MATH performance of Gemma 2B, 7B, and Gemma2 9B verifiers trained on GSM8K. We observe positive scaling trends for GenRM (direct) and GenRM-CoT as well as Discriminative RM, both for (Left) Best-of-N performance, and (Right) RM accuracy on the test set. Generative verifiers outperform discriminative counterparts in all model regimes.

Scaling Test-Time Compute with GenRM-CoT can be done by sampling multiple CoTs and applying majority voting, as described in Eq ([7](#S3.E7 "In 3.3 Chain-of-Thought Verifiers (GenRM-CoT) ‣ 3 GenRM: Verification as Next-Token Prediction ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")). As shown in [Figure 12](#S4.F12 "Figure 12 ‣ 4.3 Scaling Model Size and Inference-time Compute ‣ 4 Experiments ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction"), GenRM-CoT verifier’s performance scales gracefully with number of votes at test time, under all three Gemma model sizes (2B, 7B, 9B), outperforming greedy decoding performance within 2 votes. Notably, across model scales, the finetuned GenRM-CoT verifier outperforms LLM-as-a-Judge , which also utilizes the same CoT approach and number of majority votes, but prompts a more capable Gemini 1.0 Pro model than Gemma models which we finetune as verifiers.

Scaling model size. In [Figure 12](#S4.F12 "Figure 12 ‣ 4.3 Scaling Model Size and Inference-time Compute ‣ 4 Experiments ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction"), we show that generative verifiers, especially GenRM-CoT, perform better than discriminative RMs across model sizes, both in terms of reward modeling accuracy and Best-of-N performance. Intuitively, bigger models are more capable of text generation, allowing GenRM-CoT finetuning to better tap into its chain-of-thought reasoning ability for verification. Furthermore, these results demonstrate that larger models generalize better using the same data, which matches what we expect from scaling model parameter counts under the next-token prediction loss.

Figure 13: Quality of synthetic rationales matters. Using reference guidance for synthetic rationale generation is crucial for GenRM-CoT to perform well on GSM8K: 91.7% with guidance vs. 87.8% without for Gemma-7B verifiers.

Figure 14: Quantity of synthetic rationales matter. Scaling the number of rationales per solution for GenRM-CoT on GSM8K improves both RM accuracy and Best-of-N performance. Here, we use fine-tuned Gemma-7B verifier, with greedy decoding at inference ([6](#S3.E6 "In 3.3 Chain-of-Thought Verifiers (GenRM-CoT) ‣ 3 GenRM: Verification as Next-Token Prediction ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")).

#### 4.4 Synthetic Rationales: Quantity and Quality Matter

Our results on math reasoning tasks indicate that CoT verifiers can outperform discriminative and direct verifiers without requiring human-written verification rationales, highlighting the potential of LLM-generated rationales. We find that both the quality and quantity of these synthetic rationales matter. As shown in [Figure 14](#S4.F14 "Figure 14 ‣ 4.3 Scaling Model Size and Inference-time Compute ‣ 4 Experiments ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction"), using reference-guided grading during rationale generation (§[3.3](#S3.SS3 "3.3 Chain-of-Thought Verifiers (GenRM-CoT) ‣ 3 GenRM: Verification as Next-Token Prediction ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")) significantly improves verification performance. Furthermore, using multiple rationales per solution also improves performance, as shown in [Figure 14](#S4.F14 "Figure 14 ‣ 4.3 Scaling Model Size and Inference-time Compute ‣ 4 Experiments ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction"). We suspect that this is because model-generated rationales may contain errors, such that training on multiple rationales per solution can result in an “ensembling” effect that prevents overfitting to such errors ([Zhang et al., 2024](#bib.bib56)).

Importantly, unlike prior work, our results on math reasoning tasks do not require a more capable model ([Ankner et al., 2024](#bib.bib3); [Ye et al., 2024](#bib.bib52)) or humans ([McAleese et al., 2024](#bib.bib28); [Saunders et al., 2022](#bib.bib35)) for generating verification rationales: we use the same model (Gemini 1.0 Pro) to both generate solutions to verify and synthetic verification rationales for training.

[TABLE]

Figure 15: An example where GenRM-CoT catches a subtle mistake that the discriminative verifier is unable to catch. The candidate solution did not convert 90 minutes into 1.5 hours before dividing it by 7.5. However, the discriminative verifier was not able to detect this mistake likely because the solution does still appear to produce a valid-sounding percentage 90/7.5 = 12. Our proposed GenRM-CoT model is able to identify this mistake using step-by-step generative verification. The full verification output can be found in [Table E.1](#A5.T1 "Table E.1 ‣ Appendix E Examples Verification rationales from GenRM-CoT: GSM8K Test and MATH500 ‣ Appendices ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction").

### 5 Related Work

Reward models (RMs) and verifiers. Conventionally, RMs and verifiers are trained as discriminative models via binary classification: given a prompt and a corresponding solution or a pair of solutions), the model is either trained to predict the correctness of the solution ([Cobbe et al., 2021](#bib.bib11); [Lightman et al., 2023](#bib.bib22); [Wang et al., 2023](#bib.bib44); [Uesato et al., 2022](#bib.bib43); [Luo et al., 2024](#bib.bib27); [Yu et al., 2024](#bib.bib53)) or a preference between the two solutions ([Stiennon et al., 2020](#bib.bib39); [Nakano et al., 2021](#bib.bib30)). Concretely, the RM directly produces a numerical continuous-valued score, which is then plugged into a classification objective ([3](#S2.E3 "In 2 Preliminaries ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")). As such, discriminative verifiers do not utilize the generation capabilities of LLMs. In contrast to discriminative RMs, GenRM represents the correctness decision using the log probability of specific tokens, for example ‘Yes’ and ‘No’. Posing verification as generating “yet another token” allows it to tap better into the generation capabilities of LLMs, by making it straightforward to employ CoT reasoning and additional inference-time compute for better verification.

LLM-as-a-Judge. Another line of work that poses verification as next-token prediction simply *prompts* off-the-shelf LLMs to act as a verifier when provided with a rubric and a template for grading ([Zheng et al., 2024](#bib.bib58); [Bai et al., 2022](#bib.bib4); [Kim et al., 2023](#bib.bib19); [Ling et al., 2024](#bib.bib24)) or many-shot ICL examples ([Agarwal et al., 2024](#bib.bib2)), but *without* any specific training for the same. Perhaps unsurprisingly, we find in our experiments that using more powerful LLMs (Gemini 1.0 Pro) as a judge is worse than our trained GenRM using weaker Gemma models ([Figure 1](#S1.F1 "Figure 1 ‣ 1 Introduction ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction"), [12](#S4.F12 "Figure 12 ‣ 4.3 Scaling Model Size and Inference-time Compute ‣ 4 Experiments ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")), highlighting the necessity of *training* generative verifiers. Our generative verifiers also exhibit good out-of-distribution generalization, which might be due to better calibrated uncertainty estimates from training ([Kapoor et al., 2024](#bib.bib18)). More generally, even the strong proprietary LLMs, such as GPT-4 ([Achiam et al., 2023](#bib.bib1)) and Gemini ([Team et al., 2024](#bib.bib42)), fall behind trained RMs on popular leaderboards ([Lambert et al., 2024](#bib.bib21)), and this gap is much larger for reasoning.

Using CoTs for reward models. Prior works have also used critiques or CoT to extract preference and verification signals using LLM-as-a-Judge ([Yuan et al., 2024](#bib.bib54); [Wu et al., 2024](#bib.bib49); [Wang et al., 2024](#bib.bib45)); in contrast to these works, GenRM utilizes model-generated CoTs directly for training the verifier. Upon inference, a GenRM-CoT produces its own CoTs, which it then uses to make decisions on correctness, unlike [Ye et al. (2024)](#bib.bib52) that simply uses CoTs from a separate highly-capable LLM. In contrast to prior work that utilizes high-quality data from humans to train critique models ([Saunders et al., 2022](#bib.bib35)) or train *discriminative* RMs for generating code critiques ([McAleese et al., 2024](#bib.bib28)), we show that GenRM can be trained from purely synthetic, model-generated critiques. Concurrent work ([Ankner et al., 2024](#bib.bib3)) trains an RM to produce response critiques for preference pairs generated using a much more capable LLM, which are then passed as input into a RM head, separate from the base LLM. Unlike GenRM which uses next-token prediction, their RM head is trained discriminatively akin to standard RMs. While this approach allows them to leverage CoT, it does *not* allow them to unify solution generation and verification as a result of a discriminative RM head, which GenRM seamlessly enables (Section [4.2](#S4.SS2 "4.2 Synergy Between Generation and Verification ‣ 4 Experiments ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")). Moreover, their synthetic critiques are not filtered for correctness, which would lead to poor verification CoTs on reasoning tasks (§[3.3](#S3.SS3 "3.3 Chain-of-Thought Verifiers (GenRM-CoT) ‣ 3 GenRM: Verification as Next-Token Prediction ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")).

Unified generation and verification. One of the hallmark properties of GenRM is that the same generative verifier can be co-trained with a generation objective ([5](#S3.E5 "In 3.2 Unifying Generation and Verification ‣ 3 GenRM: Verification as Next-Token Prediction ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")): when given a problem, the model is trained to produce a solution, whereas when given a problem and a candidate solution, it is trained to verify this candidate. This is related to DPO ([Rafailov et al., 2024](#bib.bib33)) and its application to learning verifiers in reasoning ([Hosseini et al., 2024](#bib.bib17)), which aims to unify generation (policy) and verification (reward models) by representing the reward implicitly using the logits of a policy and training the policy with a reward-modeling loss. For reasoning, this type of model tying has been shown to exhibit erroneous extrapolation and degradation in learned representations, which prior work has attempted to address with additional techniques ([Pang et al., 2024](#bib.bib32); [Setlur et al., 2024](#bib.bib37); [Pal et al., 2024](#bib.bib31); [Yang et al., 2024](#bib.bib50)). Of these, while [Yang et al. (2024)](#bib.bib50) train a reward model with an auxiliary generative SFT loss, note that this loss is applied on a separate head for regularization purposes and is discarded after training; unlike GenRM no text is produced when querying the RM. In addition, compared to DPO, GenRM uses a simpler next-token prediction loss, does not require a reference policy, and obtains significantly better verification performance ([Figure 1](#S1.F1 "Figure 1 ‣ 1 Introduction ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction"), [6](#S4.F6 "Figure 6 ‣ 4 Experiments ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")).

### 6 Conclusion & Future Work

In this paper, we have introduced Generative Verifiers (GenRM), which recast verification as next-token prediction. GenRM is more performant than discriminative verifiers, and unlocks the use of chain-of-thought reasoning and inference-time compute for better verification. GenRM also unifies generation and verification into a single LLM, and demonstrates that such a unification benefits both generation and verification. Moreover, we show that synthetic model-generated rationales, which can be error-prone, are sufficient to teach GenRM how to use verification CoT to pick out tricky errors on math reasoning tasks (see [Figure 2](#S1.F2 "Figure 2 ‣ 1 Introduction ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction"), [4](#S3.F4 "Figure 4 ‣ 3.3 Chain-of-Thought Verifiers (GenRM-CoT) ‣ 3 GenRM: Verification as Next-Token Prediction ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction"), [15](#S4.F15 "Figure 15 ‣ 4.4 Synthetic Rationales: Quantity and Quality Matter ‣ 4 Experiments ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction"), and [Appendix E](#A5 "Appendix E Examples Verification rationales from GenRM-CoT: GSM8K Test and MATH500 ‣ Appendices ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")).

The framework of generative verification offers a solid foundation for future work. Promising directions include extending this framework to broader tasks such as coding, alignment, text-to-image generation ([Lin et al., 2024](#bib.bib23)), and open-ended generation ([Besta et al., 2024](#bib.bib5)). Furthermore, leveraging process-level supervision ([Lightman et al., 2023](#bib.bib22)) and training CoT verifiers with reinforcement learning (RL) can result in more accurate generative verifiers. Given GenRM’s compatibility with all the existing tools designed to improve LLMs, exploring enhancements through techniques like retrieval-augmented generation ([Borgeaud et al., 2022](#bib.bib6)), many-shot learning ([Agarwal et al., 2024](#bib.bib2)), multi-staged prompting ([Yao et al., 2024](#bib.bib51)), and tool use ([Schick et al., 2024](#bib.bib36)) would be interesting. Finally, incorporating generative verifiers into RL pipelines for LLMs warrants further investigation.

### Acknowledgements

This work was done during LZ, AH, and HB’s internship at Google. We thank Hugo Larochelle, Minqi Jiang, Aleksandra Faust, Ankit Anand, Guillaume Desjardins, Doina Precup, and Charlie Snell for feedback on an earlier version of this paper and informative discussions. We thank Chirag Nagpal and Katrin Tomanek for support in setting up infrastructure that was crucial for running Gemma experiments.

### Author Contributions

LZ led the project, and ran almost all of the experiments and ablation studies, and wrote and edited the paper. AH was responsible for the discriminative RM baselines and DPO baselines. HB was responsible for the word-sorting task, and helped set up evaluations and DPO. MK advised the project, and provided feedback on writing. AK conceived the project with RA, advised LZ, provided feedback on paper, and helped run additional experiments during rebuttal. RA hosted LZ as a student researcher, proposed several ideas and experiments, implemented reference-guided grading, ran experiments on additional datasets during rebuttal, wrote the initial draft and advised the project.

### References

- Achiam et al. (2023)  J. Achiam, S. Adler, S. Agarwal, L. Ahmad, I. Akkaya, F. L. Aleman, D. Almeida, J. Altenschmidt, S. Altman, S. Anadkat, et al. Gpt-4 technical report. *arXiv preprint arXiv:2303.08774*, 2023.
- Agarwal et al. (2024)  R. Agarwal, A. Singh, L. M. Zhang, B. Bohnet, S. Chan, A. Anand, Z. Abbas, A. Nova, J. D. Co-Reyes, E. Chu, et al. Many-shot in-context learning. *arXiv preprint arXiv:2404.11018*, 2024.
- Ankner et al. (2024)  Z. Ankner, M. Paul, B. Cui, J. D. Chang, and P. Ammanabrolu. Critique-out-loud reward models. *arXiv preprint arXiv:2408.11791*, 2024.
- Bai et al. (2022)  Y. Bai, S. Kadavath, S. Kundu, A. Askell, J. Kernion, A. Jones, A. Chen, A. Goldie, A. Mirhoseini, C. McKinnon, et al. Constitutional ai: Harmlessness from ai feedback. *arXiv preprint arXiv:2212.08073*, 2022.
- Besta et al. (2024)  M. Besta, L. Paleari, A. Kubicek, P. Nyczyk, R. Gerstenberger, P. Iff, T. Lehmann, H. Niewiadomski, and T. Hoefler. Checkembed: Effective verification of llm solutions to open-ended tasks. *arXiv preprint arXiv:2406.02524*, 2024.
- Borgeaud et al. (2022)  S. Borgeaud, A. Mensch, J. Hoffmann, T. Cai, E. Rutherford, K. Millican, G. B. Van Den Driessche, J.-B. Lespiau, B. Damoc, A. Clark, et al. Improving language models by retrieving from trillions of tokens. In *International conference on machine learning*, pages 2206–2240. PMLR, 2022.
- Brown et al. (2024)  B. Brown, J. Juravsky, R. Ehrlich, R. Clark, Q. V. Le, C. Ré, and A. Mirhoseini. Large language monkeys: Scaling inference compute with repeated sampling. *arXiv preprint arXiv:2407.21787*, 2024.
- Charniak and Johnson (2005)  E. Charniak and M. Johnson. Coarse-to-fine n-best parsing and maxent discriminative reranking. In *Proceedings of the 43rd Annual Meeting of the Association for Computational Linguistics (ACL’05)*, pages 173–180, 2005.
- Chowdhery et al. (2023)  A. Chowdhery, S. Narang, J. Devlin, M. Bosma, G. Mishra, A. Roberts, P. Barham, H. W. Chung, C. Sutton, S. Gehrmann, et al. Palm: Scaling language modeling with pathways. *Journal of Machine Learning Research*, 24(240):1–113, 2023.
- Chung et al. (2022)  H. W. Chung, L. Hou, S. Longpre, B. Zoph, Y. Tay, W. Fedus, Y. Li, X. Wang, M. Dehghani, S. Brahma, et al. Scaling instruction-finetuned language models. *arXiv preprint arXiv:2210.11416*, 2022.
- Cobbe et al. (2021)  K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert, J. Tworek, J. Hilton, R. Nakano, et al. Training verifiers to solve math word problems. *arXiv preprint arXiv:2110.14168*, 2021.
- Gemma Team et al. (2024a) Gemma Team, T. Mesnard, C. Hardin, R. Dadashi, S. Bhupatiraju, S. Pathak, L. Sifre, M. Rivière, M. S. Kale, J. Love, et al. Gemma: Open models based on gemini research and technology. *arXiv preprint arXiv:2403.08295*, 2024a.
- Gemma Team et al. (2024b) Gemma Team, M. Riviere, S. Pathak, P. G. Sessa, C. Hardin, S. Bhupatiraju, L. Hussenot, T. Mesnard, B. Shahriari, A. Ramé, et al. Gemma 2: Improving open language models at a practical size. *arXiv preprint arXiv:2408.00118*, 2024b.
- Google et al. (2023)  G. T. Google, R. Anil, S. Borgeaud, Y. Wu, J.-B. Alayrac, J. Yu, R. Soricut, J. Schalkwyk, A. M. Dai, A. Hauth, et al. Gemini: a family of highly capable multimodal models. *arXiv preprint arXiv:2312.11805*, 2023.
- Hendrycks et al. (2020)  D. Hendrycks, C. Burns, S. Basart, A. Zou, M. Mazeika, D. Song, and J. Steinhardt. Measuring massive multitask language understanding. *arXiv preprint arXiv:2009.03300*, 2020.
- Hendrycks et al. (2021)  D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang, D. Song, and J. Steinhardt. Measuring mathematical problem solving with the math dataset. *arXiv preprint arXiv:2103.03874*, 2021.
- Hosseini et al. (2024)  A. Hosseini, X. Yuan, N. Malkin, A. Courville, A. Sordoni, and R. Agarwal. V-star: Training verifiers for self-taught reasoners. *arXiv preprint arXiv:2402.06457*, 2024.
- Kapoor et al. (2024)  S. Kapoor, N. Gruver, M. Roberts, K. Collins, A. Pal, U. Bhatt, A. Weller, S. Dooley, M. Goldblum, and A. G. Wilson. Large language models must be taught to know what they don’t know. *arXiv preprint arXiv:2406.08391*, 2024.
- Kim et al. (2023)  S. Kim, J. Shin, Y. Cho, J. Jang, S. Longpre, H. Lee, S. Yun, S. Shin, S. Kim, J. Thorne, et al. Prometheus: Inducing fine-grained evaluation capability in language models. In *The Twelfth International Conference on Learning Representations*, 2023.
- Kingma (2014)  D. P. Kingma. Adam: A method for stochastic optimization. *arXiv preprint arXiv:1412.6980*, 2014.
- Lambert et al. (2024)  N. Lambert, V. Pyatkin, J. Morrison, L. Miranda, B. Y. Lin, K. Chandu, N. Dziri, S. Kumar, T. Zick, Y. Choi, et al. Rewardbench: Evaluating reward models for language modeling. *arXiv preprint arXiv:2403.13787*, 2024.
- Lightman et al. (2023)  H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J. Schulman, I. Sutskever, and K. Cobbe. Let’s verify step by step. *arXiv preprint arXiv:2305.20050*, 2023.
- Lin et al. (2024)  Z. Lin, D. Pathak, B. Li, J. Li, X. Xia, G. Neubig, P. Zhang, and D. Ramanan. Evaluating text-to-visual generation with image-to-text generation. *arXiv preprint arXiv:2404.01291*, 2024.
- Ling et al. (2024)  Z. Ling, Y. Fang, X. Li, Z. Huang, M. Lee, R. Memisevic, and H. Su. Deductive verification of chain-of-thought reasoning. *Advances in Neural Information Processing Systems*, 36, 2024.
- Liu et al. (2023)  Y. Liu, A. Singh, C. D. Freeman, J. D. Co-Reyes, and P. J. Liu. Improving large language model fine-tuning for solving math problems. *arXiv preprint arXiv:2310.10047*, 2023.
- Loshchilov and Hutter (2017)  I. Loshchilov and F. Hutter. Decoupled weight decay regularization. *arXiv preprint arXiv:1711.05101*, 2017.
- Luo et al. (2024)  L. Luo, Y. Liu, R. Liu, S. Phatale, H. Lara, Y. Li, L. Shu, Y. Zhu, L. Meng, J. Sun, et al. Improve mathematical reasoning in language models by automated process supervision. *arXiv preprint arXiv:2406.06592*, 2024.
- McAleese et al. (2024)  N. McAleese, R. M. Pokorny, J. F. C. Uribe, E. Nitishinskaya, M. Trebacz, and J. Leike. Llm critics help catch llm bugs. *arXiv preprint arXiv:2407.00215*, 2024.
- Meurer et al. (2017)  A. Meurer, C. P. Smith, M. Paprocki, O. Čertík, S. B. Kirpichev, M. Rocklin, A. Kumar, S. Ivanov, J. K. Moore, S. Singh, et al. Sympy: symbolic computing in python. *PeerJ Computer Science*, 3:e103, 2017.
- Nakano et al. (2021)  R. Nakano, J. Hilton, S. Balaji, J. Wu, L. Ouyang, C. Kim, C. Hesse, S. Jain, V. Kosaraju, W. Saunders, et al. Webgpt: Browser-assisted question-answering with human feedback. *arXiv preprint arXiv:2112.09332*, 2021.
- Pal et al. (2024)  A. Pal, D. Karkhanis, S. Dooley, M. Roberts, S. Naidu, and C. White. Smaug: Fixing failure modes of preference optimisation with dpo-positive. *arXiv preprint arXiv:2402.13228*, 2024.
- Pang et al. (2024)  R. Y. Pang, W. Yuan, K. Cho, H. He, S. Sukhbaatar, and J. Weston. Iterative reasoning preference optimization. *arXiv preprint arXiv:2404.19733*, 2024.
- Rafailov et al. (2024)  R. Rafailov, A. Sharma, E. Mitchell, C. D. Manning, S. Ermon, and C. Finn. Direct preference optimization: Your language model is secretly a reward model. *Advances in Neural Information Processing Systems*, 36, 2024.
- Roberts et al. (2022)  A. Roberts, H. W. Chung, A. Levskaya, G. Mishra, J. Bradbury, D. Andor, S. Narang, B. Lester, C. Gaffney, A. Mohiuddin, C. Hawthorne, A. Lewkowycz, A. Salcianu, M. van Zee, J. Austin, S. Goodman, L. B. Soares, H. Hu, S. Tsvyashchenko, A. Chowdhery, J. Bastings, J. Bulian, X. Garcia, J. Ni, A. Chen, K. Kenealy, J. H. Clark, S. Lee, D. Garrette, J. Lee-Thorp, C. Raffel, N. Shazeer, M. Ritter, M. Bosma, A. Passos, J. Maitin-Shepard, N. Fiedel, M. Omernick, B. Saeta, R. Sepassi, A. Spiridonov, J. Newlan, and A. Gesmundo. Scaling up models and data with t5x and seqio. *arXiv preprint arXiv:2203.17189*, 2022. URL [https://arxiv.org/abs/2203.17189](https://arxiv.org/abs/2203.17189).
- Saunders et al. (2022)  W. Saunders, C. Yeh, J. Wu, S. Bills, L. Ouyang, J. Ward, and J. Leike. Self-critiquing models for assisting human evaluators. *arXiv preprint arXiv:2206.05802*, 2022.
- Schick et al. (2024)  T. Schick, J. Dwivedi-Yu, R. Dessì, R. Raileanu, M. Lomeli, E. Hambro, L. Zettlemoyer, N. Cancedda, and T. Scialom. Toolformer: Language models can teach themselves to use tools. *Advances in Neural Information Processing Systems*, 36, 2024.
- Setlur et al. (2024)  A. Setlur, S. Garg, X. Geng, N. Garg, V. Smith, and A. Kumar. Rl on incorrect synthetic data scales the efficiency of llm math reasoning by eight-fold. *arXiv preprint arXiv:2406.14532*, 2024.
- Singh et al. (2023)  A. Singh, J. D. Co-Reyes, R. Agarwal, A. Anand, P. Patil, P. J. Liu, J. Harrison, J. Lee, K. Xu, A. Parisi, et al. Beyond human data: Scaling self-training for problem-solving with language models. *arXiv preprint arXiv:2312.06585*, 2023.
- Stiennon et al. (2020)  N. Stiennon, L. Ouyang, J. Wu, D. Ziegler, R. Lowe, C. Voss, A. Radford, D. Amodei, and P. F. Christiano. Learning to summarize with human feedback. *Advances in Neural Information Processing Systems*, 33:3008–3021, 2020.
- Sun et al. (2024)  Z. Sun, L. Yu, Y. Shen, W. Liu, Y. Yang, S. Welleck, and C. Gan. Easy-to-hard generalization: Scalable alignment beyond human supervision. *arXiv preprint arXiv:2403.09472*, 2024.
- Suzgun et al. (2022)  M. Suzgun, N. Scales, N. Schärli, S. Gehrmann, Y. Tay, H. W. Chung, A. Chowdhery, Q. V. Le, E. H. Chi, D. Zhou, et al. Challenging big-bench tasks and whether chain-of-thought can solve them. *arXiv preprint arXiv:2210.09261*, 2022.
- Team et al. (2024)  G. Team, M. Reid, N. Savinov, D. Teplyashin, T. Lillicrap, J.-b. Alayrac, R. Soricut, A. Lazaridou, O. Firat, J. Schrittwieser, et al. Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context. *arXiv e-prints*, pages arXiv–2403, 2024.
- Uesato et al. (2022)  J. Uesato, N. Kushman, R. Kumar, F. Song, N. Siegel, L. Wang, A. Creswell, G. Irving, and I. Higgins. Solving math word problems with process-and outcome-based feedback. *arXiv preprint arXiv:2211.14275*, 2022.
- Wang et al. (2023)  P. Wang, L. Li, Z. Shao, R. Xu, D. Dai, Y. Li, D. Chen, Y. Wu, and Z. Sui. Math-shepherd: A label-free step-by-step verifier for llms in mathematical reasoning. *arXiv preprint arXiv:2312.08935*, 2023.
- Wang et al. (2024)  T. Wang, I. Kulikov, O. Golovneva, P. Yu, W. Yuan, J. Dwivedi-Yu, R. Y. Pang, M. Fazel-Zarandi, J. Weston, and X. Li. Self-taught evaluators. *arXiv preprint arXiv:2408.02666*, 2024.
- Wang et al. (2022)  X. Wang, J. Wei, D. Schuurmans, Q. Le, E. Chi, S. Narang, A. Chowdhery, and D. Zhou. Self-consistency improves chain of thought reasoning in language models. *arXiv preprint arXiv:2203.11171*, 2022.
- Wei et al. (2022)  J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le, D. Zhou, et al. Chain-of-thought prompting elicits reasoning in large language models. *Advances in neural information processing systems*, 35:24824–24837, 2022.
- Wortsman et al. (2023)  M. Wortsman, P. J. Liu, L. Xiao, K. Everett, A. Alemi, B. Adlam, J. D. Co-Reyes, I. Gur, A. Kumar, R. Novak, et al. Small-scale proxies for large-scale transformer training instabilities. *arXiv preprint arXiv:2309.14322*, 2023.
- Wu et al. (2024)  T. Wu, W. Yuan, O. Golovneva, J. Xu, Y. Tian, J. Jiao, J. Weston, and S. Sukhbaatar. Meta-rewarding language models: Self-improving alignment with llm-as-a-meta-judge. *arXiv preprint arXiv:2407.19594*, 2024.
- Yang et al. (2024)  R. Yang, R. Ding, Y. Lin, H. Zhang, and T. Zhang. Regularizing hidden states enables learning generalizable reward model for llms. *arXiv preprint arXiv:2406.10216*, 2024.
- Yao et al. (2024)  S. Yao, D. Yu, J. Zhao, I. Shafran, T. Griffiths, Y. Cao, and K. Narasimhan. Tree of thoughts: Deliberate problem solving with large language models. *Advances in Neural Information Processing Systems*, 36, 2024.
- Ye et al. (2024)  Z. Ye, F. Greenlee-Scott, M. Bartolo, P. Blunsom, J. A. Campos, and M. Gallé. Improving reward models with synthetic critiques. *arXiv preprint arXiv:2405.20850*, 2024.
- Yu et al. (2024)  F. Yu, A. Gao, and B. Wang. Ovm, outcome-supervised value models for planning in mathematical reasoning. In *Findings of the Association for Computational Linguistics: NAACL 2024*, pages 858–875, 2024.
- Yuan et al. (2024)  W. Yuan, R. Y. Pang, K. Cho, S. Sukhbaatar, J. Xu, and J. Weston. Self-rewarding language models. *arXiv preprint arXiv:2401.10020*, 2024.
- Zelikman et al. (2022)  E. Zelikman, Y. Wu, J. Mu, and N. Goodman. Star: Bootstrapping reasoning with reasoning. *Advances in Neural Information Processing Systems*, 35:15476–15488, 2022.
- Zhang et al. (2024)  E. Zhang, V. Zhu, N. Saphra, A. Kleiman, B. L. Edelman, M. Tambe, S. M. Kakade, and E. Malach. Transcendence: Generative models can outperform the experts that train them. *arXiv preprint arXiv:2406.11741*, 2024.
- Zhang et al. (2023)  Y. Zhang, Y. Li, L. Cui, D. Cai, L. Liu, T. Fu, X. Huang, E. Zhao, Y. Zhang, Y. Chen, et al. Siren’s song in the ai ocean: a survey on hallucination in large language models. *arXiv preprint arXiv:2309.01219*, 2023.
- Zheng et al. (2024)  L. Zheng, W.-L. Chiang, Y. Sheng, S. Zhuang, Z. Wu, Y. Zhuang, Z. Lin, Z. Li, D. Li, E. Xing, et al. Judging llm-as-a-judge with mt-bench and chatbot arena. *Advances in Neural Information Processing Systems*, 36, 2024.

## Appendices

### Appendix A Training Data Generation for Verifiers

[TABLE]

Table A.1: Algorithmic reasoning tasks that we consider. In thes tasks, we can generate ground-truth verification chain-of-thoughts as the training data for a generative verifier. Those synthetic tasks help us understand whether a generative verifier can outperform a discriminative verifier in the ideal scenario where there is no noise in the verification CoT training data.

- •
  Last Letter Concatenation ([Wei et al., 2022](#bib.bib47)): Given a list of words, the task is to concatenate the last letters of each word (for instance, “Noah Paul Elisha Rebecca” $\rightarrow$ “hlaa”). To generate the training data, for each length $\{ 2,3,4\}$, we generate $350$ problem queries by randomly sampling from the set of words in original training set; for each problem query, we generate 128 attempts from Gemma-2B ([Gemma Team et al., 2024a](#bib.bib12)) model. This gives us a total of about 50K training data points after de-duplication. We train verifiers on examples of lengths $\{ 2,3,4\}$ (here the length refers to how many words are in the input list), and evaluate the verifier performance on length 6. We use the format in [Table A.1](#A1.T1 "Table A.1 ‣ Appendix A Training Data Generation for Verifiers ‣ Appendices ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction") to algorithmically generate ground-truth verification CoT for training.
- •
  Word Sorting ([Suzgun et al., 2022](#bib.bib41)): Given a list of words, sort them in alphabetical order. We train verifiers on a dataset comprised of $\{ 2,3,4\}$ words in each example, and evaluate the performance on length $5$. For each length, we generate 4096 lists of words as the problem queries; for each problem, we generate 64 attempts from Gemma-2B. After de-duplication and filtering out invalid responses, we have a total of about 100K training data points. We also algorithmically generate ground-truth verification CoT for training (see [Table A.1](#A1.T1 "Table A.1 ‣ Appendix A Training Data Generation for Verifiers ‣ Appendices ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")).
- •
  Grade School Math ([Cobbe et al., 2021](#bib.bib11)): We follow the original train/test split and use 1.3K problems for test, 128 problems for validation, and about 7.2K problems for training. We generate 50 solutions per problem, and randomly sample at max 16 correct solutions and 16 incorrect solutions per problem as the training set. We evaluate the verifier performance on 16 solutions per problem in the test set.

[TABLE]

Table A.2: We use model-generated rationales as CoT training data on GSM with the above prompt with Gemini 1.0 Pro. Specifically, we show the model another solution that arrives at the correct answer, which is privileged information that does not exist at test time. This does not require a more capable model: we use the same model to generate solutions and synthetic rationales in the training data.

[TABLE]

Table A.3: Zero-shot prompt for our LLM-as-a-Judge evaluation results based on Gemini 1.0 Pro.

### Appendix B Hyper-parameters for Verifier Training

For Gemma-based verifiers, we pick the best checkpoint based on validation accuracy of verification on held out problems and solutions. We always use data balancing between 50% correct solutions and 50% incorrect solutions in training.

##### GenRM verifiers

After doing a sweep of learning rates (LR), we find that an LR of $\lbrack{{{2\hspace{0pt}e} - 6},{{1\hspace{0pt}e} - 6},{{5\hspace{0pt}e} - 7}}\rbrack$ works well for our tasks considered (with LR=${2\hspace{0pt}e} - 6$ generally being the best). We use a weight decay of ${1\hspace{0pt}e} - 2$, and do not apply any dropout. We use the Adam optimizer ([Kingma, 2014](#bib.bib20)) with decoupled weight decay ([Loshchilov and Hutter, 2017](#bib.bib26)) and a gradient norm clipping of $1.0$. We use a linear warmup of $1000$ gradient steps, and a cosine decay schedule that decays to $10\%$ of the peak learning rate after a decay period. We finetune for 300K steps with a batch size of 64, and use seqio ([Roberts et al., 2022](#bib.bib34)) library to create data mixtures.

##### Discriminative RMs

We finetune Gemma-based discriminative RMs by using a special token’s logit for classification. We chose the best performing ORM on our validation sets by launching a large sweep over learning rates $\lbrack{{{1\hspace{0pt}e} - 7},{{5\hspace{0pt}e} - 7},{{1\hspace{0pt}e} - 6},{{2\hspace{0pt}e} - 6},{{3\hspace{0pt}e} - 6},{{5\hspace{0pt}e} - 6}}\rbrack$, weight decay $\lbrack{{{1\hspace{0pt}e} - 3},{{1\hspace{0pt}e} - 2},{{1\hspace{0pt}e} - 1}}\rbrack$ and dropouts $\lbrack{{{1\hspace{0pt}e} - 3},{{5\hspace{0pt}e} - 3},{{1\hspace{0pt}e} - 2},0}\rbrack$. We also schedule the learning rate with a linear ramp up and a cosine decay. We use a Z-loss $\phantom{} = {10^{- 4} \cdot {\log^{2}Z}}$ (where $Z$ is the softmax normalizer of all logits) for regularization purposes ([Chowdhery et al., 2023](#bib.bib9); [Wortsman et al., 2023](#bib.bib48)). Results obtained with learning rate ${1\hspace{0pt}e} - 7$ and dropout=$0$.

##### DPO

We first finetune Gemma-based generative models using SFT on correct solutions to obtain a reference policy $\pi_{\text{ref}}$, and then initialize from this reference policy to train generator $\pi_{\text{DPO}}$ with the DPO loss on a dataset of pairs of correct and incorrect solutions. We conduct a hyper-parameter sweep for both the learning rate (LR) and the $\beta$ coefficient in DPO loss: for LR we sweeped $\lbrack{{{1\hspace{0pt}e} - 7},{{5\hspace{0pt}e} - 7},{{1\hspace{0pt}e} - 6},{{2\hspace{0pt}e} - 6}}\rbrack$ and found ${1\hspace{0pt}e} - 6$ to work best; for $\beta$ we considered $\lbrack{0.01,0.1,0.5,1.0,2.0}\rbrack$ and used $0.1$. After DPO is trained, instead of using $r = {{{\log\pi_{\text{DPO}}}\hspace{0pt}{(\text{solution}\mid\text{question})}} - {{\log\pi_{\text{ref}}}\hspace{0pt}{(\text{solution}\mid\text{question})}}}$ as the score (as defined in DPO’s derivation), we find that directly the sequence log probability of the final DPO policy ${\log\pi_{\text{DPO}}}\hspace{0pt}{(\text{solution}\mid\text{question})}$ as the score (without subtracting the log prob from reference policy) results in better performance in verification (see [Figure D.5](#A4.F5 "Figure D.5 ‣ Appendix D Additional Results ‣ Appendices ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")); a similar finding was also noted in ([Hosseini et al., 2024](#bib.bib17)).

### Appendix C Additional Details

##### Data filtering for synthetic verification CoT

Since the answer checker (either based on string matching or Sympy library ([Meurer et al., 2017](#bib.bib29))) is not perfect, there will inevitably be false negatives in the model-generated solutions. Besides, it is possible for a solution to arrive at the right answer with an incorrect reasoning path, so there will also be false positives in solutions. We use the following strategy to mitigate the issue of false negatives and false positives: when selecting the synthetic verification rationales (generated under reference guidance) for training, we only keep the rationales from solutions where more than 50% of verification rationales agree with the correctness returned by the answer checker.

##### Weighted Self-Consistency

typically sums the verifier scores (across solutions) for each answer, and picks the answer with the highest summed scores. We find that summing the top-K scores (rather than summing all scores) for each answer slightly improves performance. This means that for each answer, we only consider the correctness of its top-K solutions. We use K=6 for GSM and K=4 for MATH.

### Appendix D Additional Results

Ablating generation loss weight ($\lambda$) in GenRM. Adding too much generation data negatively impacts verification, while intermediate values yield the best results, as shown in [Figure D.3](#A4.F3 "Figure D.3 ‣ Appendix D Additional Results ‣ Appendices ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction"). By default, all GenRM experiments use unified training for verification with solution generation ([5](#S3.E5 "In 3.2 Unifying Generation and Verification ‣ 3 GenRM: Verification as Next-Token Prediction ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")), with $\lambda = {1/3}$ for algorithmic tasks and $\lambda = {1/4}$ for GSM8K.

Data scaling for CoT verifiers. GenRM-CoT shows that the GenRM-CoT performance improves as we increase the number of solutions per problem from 8 to 32, in terms of RM accuracy and Best-of-N Accuracy, as shown in [Figure D.3](#A4.F3 "Figure D.3 ‣ Appendix D Additional Results ‣ Appendices ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction").

Figure D.1: GenRM (without using CoT) performs slightly better or comparable to Discriminative RM across different tasks, while outperforming DPO verifiers.

Figure D.2: Data scaling for GenRM-CoT on GSM8K with Gemma-7B. We observe that both the RM accuracy and Best-of-N performance improve as we scale up the number of rationales per solution and solutions per problem. When adding more solutions, we use 4 rationales per solution. Here, we compute GenRM-CoT scores with CoT rationales generated using greedy decoding, as discussed in ([6](#S3.E6 "In 3.3 Chain-of-Thought Verifiers (GenRM-CoT) ‣ 3 GenRM: Verification as Next-Token Prediction ‣ Generative Verifiers: Reward Modeling as Next-Token Prediction")).

Figure D.3: Impact of generation loss coefficient ($\lambda$) on GenRM verifier with Gemma-7B on GSM8K test results. Adding a solution generation loss ($\lambda > 0$) can further help GenRM, with $\lambda = {1/4}$ being a good value for GSM.

Figure D.4: Weighted Self-Consistency on GSM8K: Unlike MATH, GSM8K shows no visible gain from Weighted SC: the percentage of problems solved increases only slightly from 93.4% to 93.5% with 16 solutions, likely because improvement potential has saturated.

Figure D.5: Ablation of DPO reward function. We find that directly the sequence log probability of the final DPO policy as the score (without subtracting the log prob from reference policy) results in better performance.

### Appendix E Examples Verification rationales from GenRM-CoT: GSM8K Test and MATH500

[TABLE]

Table E.1: GenRM CoT Example 1

[TABLE]

Table E.2: GenRM CoT Example 2

[TABLE]

Table E.3: GenRM CoT Example 3

[TABLE]

Table E.4: GenRM CoT Example 4

[TABLE]

Table E.5: GenRM CoT Example 4 (Continued)

[TABLE]

Table E.6: GenRM CoT Example 5

[TABLE]

Table E.7: GenRM CoT Example 6

[TABLE]

Table E.8: GenRM CoT Example 7

[TABLE]

Table E.9: GenRM CoT Example 8

[TABLE]

Table E.10: GenRM CoT Example 9

[TABLE]

Table E.11: GenRM CoT Example 10

[TABLE]

Table E.12: GenRM CoT Example 11

[TABLE]

Table E.13: GenRM CoT Example 12

[TABLE]

Table E.14: MATH (Transfer from GSM): GenRM-CoT Example 1

[TABLE]

Table E.15: MATH (Transfer from GSM): GenRM-CoT Example 2

[TABLE]

Table E.16: MATH (Transfer from GSM): GenRM-CoT Example 3

Experimental support, please [view the build logs](./2408.15240v3/__stdout.txt) for errors. Generated by [ L A T E xml ![\[LOGO\]](img)](https://math.nist.gov/~BMiller/LaTeXML/) .

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
