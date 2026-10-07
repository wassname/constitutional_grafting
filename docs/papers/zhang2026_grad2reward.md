---
title: "Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"
authors: "Zheng Zhang; Yuanhao Zeng; Ziwei Shan; Jinjin Guo; Lufei Li; Yexin Li; Kan Ren"
year: 2026
source: https://arxiv.org/html/2602.01791
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

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) [![](img) Report Issue](# "Report an Issue") [![](img) Back to Abstract](/abs/2602.01791v1 "Back to abstract page") [![](img) Download PDF](/pdf/2602.01791v1 "Download PDF") [![](img)](javascript:toggleNavTOC(); "Toggle navigation") [![](img)](javascript:toggleReadingMode(); "Disable reading mode, show header and footer")

![](img) ![](img) ![](img)

1.  [Abstract](#abstract1 "In Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
2.  [1 Introduction](#S1 "In Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
3.  [2 Related Work](#S2 "In Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
    1.  [LLM for Open-ended Tasks.](#S2.SS0.SSS0.Px1 "In 2 Related Work ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
    2.  [Dense Rewards Modeling.](#S2.SS0.SSS0.Px2 "In 2 Related Work ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
4.  [3 Preliminary](#S3 "In Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
    1.  [3.1 Open-ended LLM Reasoning](#S3.SS1 "In 3 Preliminary ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
    2.  [3.2 LLM-as-a-Judge](#S3.SS2 "In 3 Preliminary ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
5.  [4 Methodology](#S4 "In Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
    1.  [4.1 Judge Implicitly Contains Process Feedback](#S4.SS1 "In 4 Methodology ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
        1.  [Self-Judging Mechanism.](#S4.SS1.SSS0.Px1 "In 4.1 Judge Implicitly Contains Process Feedback ‣ 4 Methodology ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
    2.  [4.2 Fine-Grained Reward Design](#S4.SS2 "In 4 Methodology ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
    3.  [4.3 Theoretical Analysis of the Reward Design](#S4.SS3 "In 4 Methodology ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
    4.  [4.4 Policy Optimization via Token-level GRPO](#S4.SS4 "In 4 Methodology ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
6.  [5 Experiments](#S5 "In Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
    1.  [5.1 Experimental Settings](#S5.SS1 "In 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
        1.  [Policy training.](#S5.SS1.SSS0.Px1 "In 5.1 Experimental Settings ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
        2.  [Datasets.](#S5.SS1.SSS0.Px2 "In 5.1 Experimental Settings ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
        3.  [Evaluation.](#S5.SS1.SSS0.Px3 "In 5.1 Experimental Settings ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
        4.  [Baselines.](#S5.SS1.SSS0.Px4 "In 5.1 Experimental Settings ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
    2.  [5.2 Main Results](#S5.SS2 "In 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
        1.  [Grad2Reward consistently performs well across different models and tasks.](#S5.SS2.SSS0.Px1 "In 5.2 Main Results ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
        2.  [Grad2Reward is robust to different test graders.](#S5.SS2.SSS0.Px2 "In 5.2 Main Results ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
    3.  [5.3 Training Efficiency Analysis](#S5.SS3 "In 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
        1.  [Grad2Reward achieves higher training efficiency and stronger performance.](#S5.SS3.SSS0.Px1 "In 5.3 Training Efficiency Analysis ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
    4.  [5.4 Ablation Study](#S5.SS4 "In 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
    5.  [5.5 Extended Analysis](#S5.SS5 "In 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
        1.  [5.5.1 Analysis of the Self-Judging Mechanism](#S5.SS5.SSS1 "In 5.5 Extended Analysis ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
            1.  [Self-judging achieves competitive performance (RQ1).](#S5.SS5.SSS1.Px1 "In 5.5.1 Analysis of the Self-Judging Mechanism ‣ 5.5 Extended Analysis ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
        2.  [5.5.2 Grad2Reward with RLOO](#S5.SS5.SSS2 "In 5.5 Extended Analysis ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
            1.  [Grad2Reward remains effective under RLOO optimization (RQ2).](#S5.SS5.SSS2.Px1 "In 5.5.2 Grad2Reward with RLOO ‣ 5.5 Extended Analysis ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
        3.  [5.5.3 Cross-Dataset Generalization](#S5.SS5.SSS3 "In 5.5 Extended Analysis ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
            1.  [Grad2Reward-trained policies exhibit stronger cross-dataset generalization on both open-ended and verifiable tasks (RQ3).](#S5.SS5.SSS3.Px1 "In 5.5.3 Cross-Dataset Generalization ‣ 5.5 Extended Analysis ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
        4.  [5.5.4 Compared with PRMs on Mathematical Reasoning Tasks](#S5.SS5.SSS4 "In 5.5 Extended Analysis ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
            1.  [Grad2Reward achieves better performance than PRMs on mathematical reasoning tasks.(RQ4)](#S5.SS5.SSS4.Px1 "In 5.5.4 Compared with PRMs on Mathematical Reasoning Tasks ‣ 5.5 Extended Analysis ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
7.  [6 Conclusion](#S6 "In Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
8.  [References](#bib "In Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
9.  [A Implementation Details](#A1 "In Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
    1.  [A.1 Policy Training](#A1.SS1 "In Appendix A Implementation Details ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
    2.  [A.2 Details of Gradient Attribution Baselines](#A1.SS2 "In Appendix A Implementation Details ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
        1.  [$L_{1}$ norm baseline.](#A1.SS2.SSS0.Px1 "In A.2 Details of Gradient Attribution Baselines ‣ Appendix A Implementation Details ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
        2.  [$L_{2}$ norm baseline.](#A1.SS2.SSS0.Px2 "In A.2 Details of Gradient Attribution Baselines ‣ Appendix A Implementation Details ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
    3.  [A.3 RLOO Optimization](#A1.SS3 "In Appendix A Implementation Details ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
    4.  [A.4 Dataset Detail](#A1.SS4 "In Appendix A Implementation Details ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
    5.  [A.5 Extending Grad2Reward to Verifiable Domains](#A1.SS5 "In Appendix A Implementation Details ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
        1.  [Combining Grad2Reward with an Outcome Reward Model.](#A1.SS5.SSS0.Px1 "In A.5 Extending Grad2Reward to Verifiable Domains ‣ Appendix A Implementation Details ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
10. [B Case Study](#A2 "In Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
    1.  [Case Overview.](#A2.SS0.SSS0.Px1 "In Appendix B Case Study ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
    2.  [Comparative analysis.](#A2.SS0.SSS0.Px2 "In Appendix B Case Study ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")
11. [C Prompt Template for Open-ended Tasks](#A3 "In Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")

[License: arXiv.org perpetual non-exclusive license](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2602.01791v1 \[cs.LG\] 02 Feb 2026

# Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning

Zheng Zhang Affiliation: School of Information Science and Technology, ShanghaiTech University Affiliation: State Key Laboratory of General Artificial Intelligence, BIGAI    Ao Lu Affiliation: School of Information Science and Technology, ShanghaiTech University    Yuanhao Zeng Affiliation: School of Information Science and Technology, ShanghaiTech University Affiliation: State Key Laboratory of General Artificial Intelligence, BIGAI    Ziwei Shan Affiliation: School of Information Science and Technology, ShanghaiTech University    Jinjin Guo Affiliation: JD.com. Email: Zheng Zhang \<zhengzhang2024@shanghaitech.edu.cn\>    Lufei Li Affiliation: School of Information Science and Technology, ShanghaiTech University    Yexin Li Affiliation: State Key Laboratory of General Artificial Intelligence, BIGAI Correspondence to: <liyexin@bigai.ai>    Kan Ren Affiliation: School of Information Science and Technology, ShanghaiTech University Correspondence to: <renkan@shanghaitech.edu.cn>

###### Abstract

Reinforcement Learning with Verifiable Rewards (RLVR) has catalyzed significant breakthroughs in complex LLM reasoning within verifiable domains, such as mathematics and programming. Recent efforts have sought to extend this paradigm to open-ended tasks by employing LLMs-as-a-Judge to provide sequence-level rewards for policy optimization. However, these rewards are inherently sparse, failing to provide the fine-grained supervision necessary for generating complex, long-form trajectories. Furthermore, current work treats the Judge as a black-box oracle, discarding the rich intermediate feedback signals encoded in it. To address these limitations, we introduce Grad2Reward, a novel framework that extracts dense process rewards directly from the Judge’s model inference process via a single backward pass. By leveraging gradient-based attribution, Grad2Reward enables precise *token-level credit assignment*, substantially enhancing training efficiency and reasoning quality. Additionally, Grad2Reward introduces a *self-judging mechanism*, allowing the policy to improve through its own evaluative signals without training specialized reward models or reliance on superior external Judges. The experiments demonstrate that policies optimized with Grad2Reward achieve outstanding performance across diverse open-ended tasks, affirming its effectiveness and broad generalizability.

###### Keywords: 

Machine Learning, ICML

## 1 Introduction

Large language models (LLMs) have recently demonstrated remarkable progress in complex reasoning tasks such as mathematics and programming, as shown by OpenAI’s o-series ([Jaech et al., 2024](#bib.bib5)) and DeepSeek-R1 ([Guo et al., 2025](#bib.bib1)). A key driver of these advances is Reinforcement Learning with Verifiable Rewards (RLVR), which assigns outcome rewards by verifying policy¹¹ 1 We use policy to represent the underlying LLM generator for the given task query. outputs against ground-truth answers. RLVR relies on ground-truth labels and therefore cannot be directly applied to broader open-ended tasks ([Xu et al., 2025](#bib.bib22); [Ye et al., 2025](#bib.bib23)), such as medical consultation or creative writing, where evaluation is inherently subjective and not strictly verifiable. Recent work ([Gunjal et al., 2025](#bib.bib2); [Zhou et al., 2025](#bib.bib3)) attempts to extend RLVR to open-ended tasks by leveraging LLM-as-a-Judge to provide sequence-level rewards for policy optimization. For example, [Gunjal et al. (2025)](#bib.bib2) employs an LLM-as-a-judge paradigm to evaluate policy outputs along multiple criteria and convert the evaluations into sequence-level rewards for GRPO ([Shao et al., 2024](#bib.bib6)) optimization.

However, these methods face several limitations. (i) *Sparse rewards result in a lack of fine-grained supervision.* Sparse rewards only provide feedback at the end of the trajectory, causing different parts of the generation sequence to be treated equally. Unlike verifiable tasks that only care about the correctness of the final answer, open-ended tasks place greater emphasis on the quality of the process. For example, in medical counseling, every part of the response must be scientifically sound and non-misleading. This property makes open-ended tasks fundamentally require dense rewards for fine-grained optimization. (ii) *Insufficient use of Judge feedback.* In practice, the Judge evaluates the quality and validity of the policy outputs holistically and emits a final decision. While such a sequence-level signal reflects an overall assessment of the policy outputs, it is informed by the quality of different parts of the generation, suggesting the potential to provide guidance beyond coarse sequence-level supervision. Despite this, prior approaches ([Zhou et al., 2025](#bib.bib3); [Gunjal et al., 2025](#bib.bib2); [Shao et al., 2025](#bib.bib10); [Bi et al., 2025](#bib.bib8)) regard the Judge as a black box, relying solely on the final verdict as a reward, without exploiting the additional evaluative information implicit in the Judge’s assessment of the full generation from the policy. As a result, fine-grained rewards are critical but challenging to obtain, while the rich feedback signals inherent in the Judge remain underutilized.

To address these limitations, we introduce Grad2Reward, a framework designed to unlock the dense feedback hidden within the Judge. Specifically, Grad2Reward leverages gradient-based attribution to quantify each generated token’s contribution to the Judge’s decision and converts these contributions into dense token-level rewards. The entire procedure consumes only a single backward pass and does not require any fine-tuning of the Judge. These rewards are used to optimize the policy, ultimately enhancing the LLM’s performance on open-ended tasks. Notably, unlike prior work ([Bi et al., 2025](#bib.bib8); [Zhou et al., 2025](#bib.bib3); [Gunjal et al., 2025](#bib.bib2); [Wang et al., 2025](#bib.bib12)) that relies on more advanced models as Judge to supervise policy training, we adopt a self-judging mechanism where the Judge is fixed to the initial policy model, ensuring that policy improvement arises from its own potential rather than distilling external knowledge.

Empirically, optimizing the policy with the dense rewards provided by Grad2Reward leads to superior training efficiency and better performance. By providing dense, informative supervision, our Grad2Reward significantly accelerates convergence, requiring substantially fewer training steps to reach optimal performance compared to sparse-reward baselines. In addition, extensive experiments confirm that Grad2Reward consistently achieves strong performance across multiple domains, validating both its effectiveness and generalization capability. Our contributions can be summarized as follows:

- •
  To the best of our knowledge, we are the first to introduce a dense-reward framework for improving LLM performance on open-ended tasks, effectively addressing the credit assignment problem and substantially improving training efficiency.
- •
  We introduce a self-judging mechanism that allows a policy to leverage its own evaluative feedback for improvement, eliminating the need for stronger and expensive external Judges.
- •
  Grad2Reward achieves leading performance across multiple open-ended tasks compared to sparse-reward baselines, demonstrating strong effectiveness and broad applicability. Notably, it provides process rewards without training a dedicated process reward model (PRM) and generalizes to verifiable domains, where it shows clear advantages over PRM-based methods.

## 2 Related Work

##### LLM for Open-ended Tasks.

Unlike verifiable tasks which have well-defined ground truth, open-ended tasks such as medical consultation ([Arora et al., 2025](#bib.bib4)) or scientific question answering ([Yifei et al., 2025](#bib.bib11)) lack standard answers and are subjective, typically requiring human experts for evaluation. Recent work ([Zhou et al., 2025](#bib.bib3); [Gunjal et al., 2025](#bib.bib2); [Shao et al., 2025](#bib.bib10); [Bi et al., 2025](#bib.bib8); [Huang et al., 2025](#bib.bib24)) has explored using LLM-as-a-Judge ([Chen et al., 2025](#bib.bib19); [Lee et al., 2025](#bib.bib20); [Wu et al., 2025](#bib.bib21)) to generate feedback signals as sequence-level rewards for optimizing LLM performance on open-ended tasks through reinforcement learning (RL). For example, ([Gunjal et al., 2025](#bib.bib2)) uses an LLM-as-a-Judge to evaluate whether the policy output satisfies specified rubrics and converts the evaluation into rewards for RL optimization. ([Wang et al., 2025](#bib.bib12)) integrates retrieval-augmented in-context prompting into an RL training framework to improve performance in medical dialogue. However, the rewards used in these methods are sparse and therefore cannot provide fine-grained supervision over the policy’s generated sequence, a limitation that is particularly pronounced in open-ended tasks.

##### Dense Rewards Modeling.

Dense rewards have been shown to be effective for improving the reasoning capabilities of LLMs ([Lightman et al., 2024](#bib.bib25); [Wang et al., 2024b](#bib.bib26)). Recent work ([Wang et al., 2024a](#bib.bib17); [Zeng et al., 2025](#bib.bib18); [Li and Li, 2025](#bib.bib27)) has explored training PRMs in mathematical domains, which provide step-level rewards ([Zhang et al., 2025a](#bib.bib15); [Cheng et al., 2025](#bib.bib16)) or token-level rewards ([Cui et al., 2025](#bib.bib14)) for policy optimization. For example, PQM ([Li and Li, 2025](#bib.bib27)) models the process reward as a Q-value ranking problem in a Markov Decision Process. PURE ([Cheng et al., 2025](#bib.bib16)) first trains a PRM, and then applies it to the proposed min-form credit assignment. VersaPRM ([Zeng et al., 2025](#bib.bib18)) applies PRM to other verifiable domains beyond mathematics. However, these methods require ground-truth process labels to train a domain-specific reward model, making them applicable only to verifiable domains and hard to extend to open-ended tasks.

![Refer to caption](2602.01791v1/figure1.png)

Figure 1: Overview of Grad2Reward (better viewed in color): The Policy samples an output $o$, which is evaluated by a Judge to derive a verdict $z$. By computing the inner product between the output embeddings $e_{t}$ and their gradients $g_{t}$ (derived from $z$), we obtain token-wise attribution scores $b_{t}$. These are converted into token-level rewards $r_{t}$ to guide the policy optimization.

## 3 Preliminary

### 3.1 Open-ended LLM Reasoning

Given a query $x$, the LLM $\pi$ generates a response $o = {(a_{1},a_{2},\ldots,a_{T})}$, where $a_{t}$ denotes the $t$-th token and $T$ is the total number of tokens. We model the generation process of the LLM as a finite-horizon Markov Decision Process (MDP) $\mathcal{M} = {(\mathcal{S},\mathcal{A},\mathcal{P},r)}$, in which an autoregressive LLM $\pi$ serves as the policy. Here, $\mathcal{S}$ is the state space, $\mathcal{A}$ is the action space, $\mathcal{P}$ denotes the transition dynamics, and $r:{{\mathcal{S} \times \mathcal{A}}\rightarrow{\mathbb{R}}}$ is the reward function. For the $t$-th token, the state is defined as $s_{t} = {(x,a_{\phantom{} \leq {t - 1}})}$ which contains the query $x$ and the sequence of previously generated tokens $a_{\phantom{} \leq {t - 1}}$. The action $a_{t}$ is the token generated conditioned on state $s_{t}$. The state transition is deterministic, as the next state is uniquely determined by concatenating the previously generated sequence with the current token $a_{t}$. Let $r_{t}$ denote the immediate reward of token $a_{t}$, such that the sequence-level reward of the policy output $o$ can be written as ${r{(x,o)}} = {\Sigma_{t = 1}^{T}\hspace{0pt}r_{t}}$.

In open-ended tasks, prior approaches obtain sequence-level reward $r{(x,o)}$ by using the LLM-as-a-Judge, while the individual token rewards $r_{t}$ remain unknown.

### 3.2 LLM-as-a-Judge

To evaluate a policy output $o$ for a given query $x$, existing methods ([Zhou et al., 2025](#bib.bib3); [Gunjal et al., 2025](#bib.bib2); [Shao et al., 2025](#bib.bib10); [Bi et al., 2025](#bib.bib8)) employ the LLM-as-a-Judge combined with a predefined rubric $(c,w)$, where each $c$ specifies an evaluation criterion and $w$ is the reward assigned when the criterion is satisfied.

Specifically, a structured prompt (see Appendix [C](#A3 "Appendix C Prompt Template for Open-ended Tasks ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")) is constructed, which includes the query $x$, the policy output $o$, and the criterion $c$ as the input to the Judge. The Judge is instructed to generate a binary decision token $z \in {\{{\text{True},\text{False}}\}}$ to indicate whether the criterion $c$ is satisfied. Then, the sequence-level reward for $(x,o)$ is defined using the Judge’s output as:

|     |                                                                                                      |     |     |
|-----|------------------------------------------------------------------------------------------------------|-----|-----|
|     | $$r{(x,o|c,w)} = w \cdot {\mathbb{I}}{\lbrack z \sim p_{\text{judge}}{( \cdot \mid x,o,c)}\rbrack}$$ |     | (1) |

Here, ${\mathbb{I}}{\lbrack \cdot \rbrack}$ denotes the indicator function, which evaluates to $1$ if the Judge outputs $z = \text{True}$, and $0$ otherwise. The resulting sequence-level reward $r{(x,o|c,w)}$ is then used in RL optimization algorithms, such as GRPO, to improve the policy’s performance. For brevity, we denote $r{(x,o \mid c,w)}$ as $r{(x,o)}$ in the following.

## 4 Methodology

### 4.1 Judge Implicitly Contains Process Feedback

Although the Judge ultimately evaluates the policy output $o$ with a binary decision token, its internal computation is far more expressive. As an autoregressive language model, the Judge processes the entire policy output $o$ token by token before emitting a final judgment, which reflects an accumulated assessment of the whole sequence $o$ based on a semantic understanding of the intermediate steps. During this process, Judge implicitly evaluates the generation trajectory by modeling logical structure, semantic coherence, and alignment with the given criterion. However, existing approaches ([Zhou et al., 2025](#bib.bib3); [Gunjal et al., 2025](#bib.bib2); [Shao et al., 2025](#bib.bib10)) treat the Judge as a black box and only extract the final verdict as a scalar reward. This collapses the Judge’s rich internal evaluative process into a single binary signal, implicitly assigning equal credit to all tokens in the trajectory. As a result, a large amount of intermediate feedback information that may indicate the quality of reasoning processes is discarded. This motivates our design to recover and exploit the process feedback that is implicitly embedded in the Judge’s autoregressive computation but overlooked by existing black-box usage approaches.

##### Self-Judging Mechanism.

In this work, we adopt a self-judging mechanism in which the Judge is instantiated as a frozen copy of the initial policy rather than a stronger, more expensive external model. During training, the Judge remains fixed and is used solely to provide evaluation signals, while the policy is optimized via RL. This design is motivated by the observation that *LLMs often exhibit stronger discriminative capabilities than generative capabilities*, as further supported by [Song et al. (2025)](#bib.bib43). Freezing the Judge ensures that the feedback signal remains stable throughout training, providing consistent supervision. As a result, the policy improves by leveraging its own evaluative capacity rather than by distilling knowledge from a superior external Judge. This mechanism can thus be viewed as a form of self-improvement, where the model iteratively refines its generation behavior based on its own discriminative signals.

### 4.2 Fine-Grained Reward Design

To extract fine-grained signals from the Judge, we employ gradient-based attribution to measure how each token contributes to the generation of the decision token $z$. Concretely, let $\mathbf{e}_{t} \in {\mathbb{R}}^{d}$ denote the embedding of the $t$-th token in the policy output $o = {(a_{1},\ldots,a_{T})}$. We compute the gradient of the log-probability that the Judge generates the specific decision token $z$ with respect to each token embedding:

|     |                                                                                                                        |     |     |
|-----|------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $$\mathbf{g}_{t} = {\nabla_{\mathbf{e}_{t}}\hspace{0pt}\log\hspace{0pt}p_{\text{judge}}\hspace{0pt}{(z\mid{x,o,c})}}$$ |     | (2) |

Gradient vectors $\mathbf{g}_{t}$ are next transformed into scalar attribution scores that reflect the importance of each token for the Judge’s decision using *Gradient $\times$ Embedding*.

|     |                                                               |     |     |
|-----|---------------------------------------------------------------|-----|-----|
|     | $$b_{t} = {\mathbf{g}_{t}^{\top}\hspace{0pt}\mathbf{e}_{t}}$$ |     | (3) |

Eq. ([2](#S4.E2 "Equation 2 ‣ 4.2 Fine-Grained Reward Design ‣ 4 Methodology ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")) yields a sequence of attribution scores $\mathbf{b} = {(b_{1},\ldots,b_{T})}$, where each $b_{t}$ reflects the contribution of the $t$-th token in policy output $o$ to the Judge’s decision. As the raw attribution scores $\mathbf{b} = {(b_{1},\ldots,b_{T})}$ can vary significantly in scale, we apply the softmax function to normalize these signals and quantify the relative contribution of each token to the Judge’s decision:

|     |                                                                                                                                       |     |     |
|-----|---------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $$\alpha_{t} = {\text{Softmax}\hspace{0pt}{(\mathbf{b})}_{t}} = \frac{\exp{({b_{t}/\tau})}}{\sum_{k = 1}^{T}{\exp{({b_{k}/\tau})}}}$$ |     | (4) |

where $\tau$ is a temperature parameter controlling the sharpness of the distribution. Based on these attribution scores, we decompose the sequence-level reward $r{(x,o)}$ into token-level rewards:

|     |                                           |     |     |
|-----|-------------------------------------------|-----|-----|
|     | $$r_{t} = {\alpha_{t} \cdot {r{(x,o)}}}$$ |     | (5) |

As a result, the originally sparse sequence-level supervision is transformed into dense token-level feedback, enabling more precise credit assignment through the gradient signals implicitly encoded in the Judge’s internal computation.

### 4.3 Theoretical Analysis of the Reward Design

In this subsection, we provide a theoretical perspective on the reward design. Let the objective function represent the Judge’s log-probability of generating the decision token for criterion $c$ given input $x$:

|     |                                                                                                         |     |     |
|-----|---------------------------------------------------------------------------------------------------------|-----|-----|
|     | $${F{(\mathbf{e}_{1},\ldots,\mathbf{e}_{T})}} = {{\log p_{\text{judge}}}\hspace{0pt}{(z\mid{x,o,c})}}$$ |     | (6) |

Consider a local perturbation $\Delta\hspace{0pt}\mathbf{e}_{t}$ applied independently to each token embedding $\mathbf{e}_{t}$. A first-order Taylor expansion around the original embeddings gives a unified approximation for the entire sequence:

|     |           |                                                                                                                                                                                                              |     |     |
|-----|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     |           | $F{({\mathbf{e}_{1} + {\Delta\hspace{0pt}\mathbf{e}_{1}}},\ldots,{\mathbf{e}_{T} + {\Delta\hspace{0pt}\mathbf{e}_{T}}})}$                                                                                    |     |     |
|     | $\approx$ | ${F{(\mathbf{e}_{1},\ldots,\mathbf{e}_{T})}} + {\sum\limits_{t = 1}^{T}{{\nabla_{\mathbf{e}_{t}}F}\hspace{0pt}{(\mathbf{e}_{1},\ldots,\mathbf{e}_{T})}^{\top}\hspace{0pt}\Delta\hspace{0pt}\mathbf{e}_{t}}}$ |     | (7) |

Choosing the perturbation direction as ${\Delta\hspace{0pt}\mathbf{e}_{t}} = {- \mathbf{e}_{t}}$ and rearrange the above equation, we obtain:

|     |           |                                                                                                                                                                                                                           |     |     |
|-----|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     |           | ${F{(\mathbf{e}_{1},\ldots,\mathbf{e}_{T})}} - {F{(\mathbf{0},\ldots,\mathbf{0})}}$                                                                                                                                       |     |     |
|     | $\approx$ | ${\sum\limits_{t = 1}^{T}{{\nabla_{\mathbf{e}_{t}}F}\hspace{0pt}{(\mathbf{e}_{1},\ldots,\mathbf{e}_{T})}^{\top}\hspace{0pt}\mathbf{e}_{t}}} = {\sum\limits_{t = 1}^{T}{\mathbf{g}_{t}^{\top}\hspace{0pt}\mathbf{e}_{t}}}$ |     | (8) |

Each term $\mathbf{g}_{t}^{\top}\hspace{0pt}\mathbf{e}_{t}$ measures the first-order contribution of token $a_{t}$ to the Judge’s decision, and the sum over all tokens approximates the total change in the Judge’s output compared to its output when the input embedding is set to zero. Hence, each token’s contribution can naturally be used to define the token-level reward in RL optimization, since under the first-order approximation, the sum of all token-level contributions approximates the sequence-level reward relative to a constant reference baseline. Notably, this baseline can, in principle, be chosen ([Sundararajan et al., 2017](#bib.bib40)). For simplicity, we set it as the zero embedding.

### 4.4 Policy Optimization via Token-level GRPO

Common RL optimization methods such as GRPO ([Shao et al., 2024](#bib.bib6)), DAPO ([Yu et al., 2025](#bib.bib7)), and RLOO ([Ahmadian et al., 2024](#bib.bib39)) rely on sequence-level rewards, where all tokens within a generated response share the same advantage signal. This leads to coarse granularity issue ([Sun et al., 2025](#bib.bib13)). To fully exploit the token-level rewards provided by our Grad2Reward, we introduce token-level GRPO, a principled extension of GRPO that enables fine-grained optimization at the token level.

For a given input query $x$, the policy generates $G$ responses ${\{ o_{i}\}}_{i = 1}^{G}$, where each response $o_{i} = {(a_{i,1},\ldots,a_{i,T})}$ is associated with token-level rewards ${\{ r_{i,t}\}}_{t = 1}^{T}$ obtained via our Grad2Reward. The return $R_{i,t}$ aggregates future token rewards from position $t$ to the end of the response. Following standard GRPO, we compute the token-level advantage ${\hat{A}}_{i,t}$ within each group:

|     |                                                                                                                                                                                                                                 |     |     |
|-----|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $${{\hat{A}}_{i,t} = \frac{R_{i,t} - {{mean}\left( {\{ R_{j,s}\}}_{{j = 1},{s = 1}}^{G,{|o_{j}|}} \right)}}{{std}\left( {\{ R_{j,s}\}}_{{j = 1},{s = 1}}^{G,{|o_{j}|}} \right)}},{R_{i,t} = {\sum\limits_{k = t}^{T}r_{i,k}}}$$ |     | (9) |

The optimization objective of token-level GRPO is:

|     |                                                                                                                                                           |     |      |
|-----|-----------------------------------------------------------------------------------------------------------------------------------------------------------|-----|------|
|     | $$\begin{matrix}                                                                                                                                          
       {\mathcal{J}(\theta) = {\mathbb{E}}{}_{q \sim \mathcal{D},\{ o{}_{i}\}{}_{i = 1}{}^{G} \sim \pi{}_{\theta_{\text{old}}}( \cdot \mid q)}} \\                
       \left\lbrack \frac{1}{G}\sum{}_{i = 1}{}^{G}\frac{1}{|o_{i}|}\sum{}_{t = 1}{}^{|o_{i}|}\min\left( \rho{}_{i,t}(\theta)\hat{A}{}_{i,t}, \right. \right. \\  
       {{clip}\left( \rho{}_{i,t}(\theta),\, 1 - \epsilon,\, 1 + \epsilon \right)\left. \hat{A}{}_{i,t} \right)\rbrack}                                           
       \end{matrix}$$                                                                                                                                             |     | (10) |

where ${\rho_{i,t}\hspace{0pt}{(\theta)}} = \frac{\pi_{\theta}\hspace{0pt}{(o_{i,t}\mid{q,o_{{i,\phantom{}} < t}})}}{\pi_{\theta_{\text{old}}}\hspace{0pt}{(o_{i,t}\mid{q,o_{{i,\phantom{}} < t}})}}$ is the token-level importance ratio between the current policy and the previous policy, and $\epsilon$ is the clipping coefficient.

Alg. [1](#alg1 "Algorithm 1 ‣ 4.4 Policy Optimization via Token-level GRPO ‣ 4 Methodology ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning") outlines the step-by-step procedure of Grad2Reward. Notably, since each query is typically associated with $K$ rubric items $(c_{k},w_{k})$ that define evaluation criteria from multiple perspectives, we explicitly incorporate this practical setting into Alg. [1](#alg1 "Algorithm 1 ‣ 4.4 Policy Optimization via Token-level GRPO ‣ 4 Methodology ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), although it is abstracted away in the method description for simplicity.

0:  Policy $\pi_{\theta}$, Judge $p_{\text{judge}}$, dataset $\mathcal{D}$, rubric set $\mathcal{R}$, group size $G$, temperature $\tau$

1:  Sample query $x \sim \mathcal{D}$

2:  Generate a group of responses ${\{ o_{i}\}}_{i = 1}^{G} \sim \pi_{\theta_{old}}{( \cdot \mid x)}$

3:  for $i = 1$ to $G$ do

4:   Rubric for $x$: ${\mathcal{R}{(x)}} = {\{{(c_{k},w_{k})}\}}_{k = 1}^{K}$

5:   for $k = 1$ to $K$ do

6:    if ${\mathbb{I}}{\lbrack z \sim p_{\text{judge}}{( \cdot \mid x,o_{i},c_{k})}\rbrack} = 1$ then

7:     Compute token-level gradients:

8:     $\mathbf{g}_{k,t} = {\nabla_{\mathbf{e}_{t}}\hspace{0pt}\log\hspace{0pt}p_{\text{judge}}\hspace{0pt}{(z\mid{x,o_{i},c_{k}})}}$

9:     Convert gradients to attribution score:

10:     ${b_{k,t} = {\mathbf{g}_{k,t}^{\top}\hspace{0pt}\mathbf{e}_{t}}},{\alpha_{k,t} = {{softmax}_{t}\hspace{0pt}{({b_{k,t}/\tau})}}}$

11:    end if

12:   end for

13:   Compute token rewards:

14:   $r_{i,t} = \frac{\sum_{k = 1}^{K}{w_{k}\hspace{0pt}\alpha_{k,t}}}{\sum_{k = 1}^{K}{\max{(w_{k},0)}}}$

15:  end for

16:  Compute token-level returns $R_{i,t}$ and advantages ${\hat{A}}_{i,t}$ following Eq. ([9](#S4.E9 "Equation 9 ‣ 4.4 Policy Optimization via Token-level GRPO ‣ 4 Methodology ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")) using token rewards.

17:  Update $\theta$ via token-level GRPO objective in Eq. ([10](#S4.E10 "Equation 10 ‣ 4.4 Policy Optimization via Token-level GRPO ‣ 4 Methodology ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"))

Algorithm 1 Policy Optimization for Open-Ended Tasks via Grad2Reward

## 5 Experiments

### 5.1 Experimental Settings

##### Policy training.

We train models of different families and parameter scales, including Qwen2.5-1.5B-Instruct, Qwen2.5-3B-Instruct, and Llama-3.1-8B-Instruct, using full-parameter fine-tuning. Detailed training procedures and hyperparameter settings are provided in Appendix [A.1](#A1.SS1 "A.1 Policy Training ‣ Appendix A Implementation Details ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").

##### Datasets.

For the medical consultation domain, we employ the HealthBench ([Arora et al., 2025](#bib.bib4)) and RaR-Medicine ([Gunjal et al., 2025](#bib.bib2)) datasets. For academic question answering, we use ResearchQA ([Yifei et al., 2025](#bib.bib11)) and RaR-Science ([Gunjal et al., 2025](#bib.bib2)). Each dataset is split into a training set and a test set. Each query in these datasets is associated with multiple rubric items, which define query-specific evaluation criteria for assessing the quality of LLM-generated responses. A detailed description of these datasets is provided in Appendix [A.4](#A1.SS4 "A.4 Dataset Detail ‣ Appendix A Implementation Details ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").

##### Evaluation.

To ensure fair and reliable evaluation, we adopt the OpenAI Simple-Evals suite²² 2 https://github.com/openai/simple-evals, which computes rubric-based scores and supports pluggable grader models. For testing, we use Qwen3-30B-A3B-Instruct as the primary test grader to compute the average score. Notably, the test grader is a stronger external model than the Judge used during training and is employed solely to assess the performance of the trained policy. To demonstrate the effectiveness of training, we employ different prompt templates for training and testing. Detailed templates are in Appendix [C](#A3 "Appendix C Prompt Template for Open-ended Tasks ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").

##### Baselines.

We compare our proposed method with the following baselines: *Vanilla-GRPO*, which optimizes the policy using the sequence-level reward defined in Eq. ([1](#S3.E1 "Equation 1 ‣ 3.2 LLM-as-a-Judge ‣ 3 Preliminary ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")). *RuscaRL* ([Zhou et al., 2025](#bib.bib3)), which also uses sequence-level rewards but leverages rubric to guide RL exploration, representing the current leading approach for optimizing LLMs on open-ended tasks.

### 5.2 Main Results

|                         |                        |                     |                   |                    |                                |                     |                   |                    |
|-------------------------|------------------------|---------------------|-------------------|--------------------|--------------------------------|---------------------|-------------------|--------------------|
| Model                   | Qwen3-30B-A3B-Instruct |                     |                   |                    | Mistral-Small-3.2-24B-Instruct |                     |                   |                    |
|                         |  Health Bench          |  RaR- Medicine      |  Research QA      |  RaR- Science      |  Health Bench                  |  RaR- Medicine      |  Research QA      |  RaR- Science      |
| Qwen2.5-1.5B-Instruct   | 32.2                   | 27.7                | 41.2              | 36.2               | 28.1                           | 29.5                | 41.5              | 48.8               |
|    - Vanilla-GRPO       | 39.5                   | 32.7                | 53.1              | 41.6               | 32.4                           | 34.4                | 48.8              | 49.8               |
|    - RuscaRL            | 40.7                   | 34.3                | 53.9              | 44.1               | 32.7                           | 35.8                | 49.4              | 52.0               |
|    - Grad2Reward (ours) | 44.5                   | 35.5                | 55.0              | 43.5               | 36.4                           | 37.2                | 51.0              | 53.1               |
| Llama-3.2-3B-Instruct   | 44.4                   | 45.3                | 59.9              | 40.0               | 37.5                           | 47.4                | 57.2              | 55.3               |
|    - Vanilla-GRPO       | 46.2                   | 48.0                | 63.2              | 41.1               | 38.7                           | 49.7                | 58.8              | 56.5               |
|    - RuscaRL            | 47.4                   | 50.5                | 63.5              | 41.4               | 39.9                           | 51.8                | 59.4              | 55.9               |
|    - Grad2Reward (ours) | 49.4                   | 49.8                | 63.6              | 43.6               | 41.7                           | 51.6                | 59.2              | 58.1               |
| Llama-3.1-8B-Instruct   | 45.5                   | 54.9                | 63.3              | 53.6               | 39.3                           | 57.0                | 60.6              | 63.3               |
|    - Vanilla-GRPO       | 47.8                   | 56.7                | 65.9              | 54.5               | 39.6                           | 59.7                | 63.0              | 64.1               |
|    - RuscaRL            | 48.6                   | 61.1                | 67.0              | 56.2               | 40.6                           | 60.7                | 64.3              | 65.0               |
|    - Grad2Reward (ours) | 51.1                   | 62.1                | 68.9              | 56.7               | 42.0                           | 61.5                | 65.0              | 65.8               |

Table 1: Main results comparison across different open-ended tasks. The best results are highlighted in bold.

![Refer to caption](2602.01791v1/figures/training_efficiency.png)

Figure 2: Training dynamics on (a) HealthBench, (b) RaR-Medicine with Qwen3-30B-A3B-Instrcut as test grader, and (c) HealthBench, (d) RaR-Medicine with Mistral-Small-3.2-24B-Instruct as test grader.

##### Grad2Reward consistently performs well across different models and tasks.

Table [1](#S5.T1 "Table 1 ‣ 5.2 Main Results ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning") presents the main results across four diverse open-ended tasks, spanning different model families and sizes. As shown, Grad2Reward consistently outperforms the two sparse-reward baselines: Vanilla-GRPO and RuscaRL. Specifically, when using Qwen2.5-1.5B-Instruct with test grader Qwen3-30B-A3B, our Grad2Reward outperforms the strong baseline RuscaRL by margins of 3.8 points on HealthBench. Similarly, on ResearchQA, it achieves a score of 55.0, surpassing RuscaRL’s 53.9. This indicates that dense supervision effectively compensates for the limited reasoning capacity of smaller models. With Llama-3.1-8B-Instruct, our Grad2Reward also achieves a score of 68.9 on ResearchQA, significantly outperforming Vanilla-GRPO (65.9) and RuscalRL (67.0). These results suggest that dense gradient-based supervision provides more informative optimization signals than sparse rewards.

##### Grad2Reward is robust to different test graders.

To rule out the possibility of overfitting to a specific evaluator, we conducted assessments using two distinct, high-capability test graders: Qwen3-30B-A3B-Instruct and Mistral-Small-3.2-24B-Instruct. The results show that Grad2Reward consistently delivers strong performance across both graders. Specifically, with Qwen3-30B-A3B-Instruct as the test grader, Grad2Reward achieves substantial gains across all policy models. For example, when Llama-3.2-3B-Instruct is used as the policy, Grad2Reward improves HealthBench from 46.2 (Vanilla-GRPO) and 47.4 (RuscaRL) to 49.4, and boosts RaR-Science to 43.6. Similarly, with Mistral-Small-3.2-24B-Instruct, Grad2Reward again outperforms the baselines: Llama-3.2-3B-Instruct trained with Grad2Reward attains 41.7 on HealthBench and 58.1 on RaR-Science, demonstrating the robustness and consistency of our approach across different graders. These results underscore the adaptability and reliability of Grad2Reward, highlighting its broad applicability in real-world open-ended tasks.

### 5.3 Training Efficiency Analysis

##### Grad2Reward achieves higher training efficiency and stronger performance.

Figure [2](#S5.F2 "Figure 2 ‣ 5.2 Main Results ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning") compares the training dynamics of Grad2Reward and Vanilla-GRPO on HealthBench and RaR-Medicine, evaluated with two test grader, i.e., Qwen3-30B-A3B-Instruct and Mistral-Small-3.2-24B-Instruct. In terms of convergence speed, Grad2Reward reaches the same or better performance levels as Vanilla-GRPO with 1.7×–1.9× fewer training steps under the Qwen grader and 1.8×–1.9× fewer steps under the Mistral grader. This acceleration indicates that dense gradient-based rewards significantly accelerate optimization by providing more informative credit assignment. Beyond faster convergence, Grad2Reward also achieves higher asymptotic performance: it yields 13% and 12% relative gains on HealthBench and RaR-Medicine when evaluated by Qwen, and maintains robust improvements of 12% and 8% under the Mistral grader. The consistency of these trends across datasets and test graders suggests that the advantages of Grad2Reward stem from its ability to deliver fine-grained supervision, which improves both optimization efficiency and policy output quality.

### 5.4 Ablation Study

|                         |                    |                     |                   |                    |
|-------------------------|--------------------|---------------------|-------------------|--------------------|
|                         |  Health Bench      |  RaR- Medicine      |  Research QA      |  RaR- Science      |
| Vanilla-GRPO            | 32.2               | 27.7                | 41.2              | 36.2               |
| L1 norm                 | 38.7               | 33.1                | 55.6              | 37.8               |
| L2 norm                 | 38.0               | 34.5                | 54.9              | 40.0               |
|  Grad2Reward (ours)     | 44.5               | 35.5                | 55.0              | 43.5               |

Table 2: Ablation study on different gradient attribution methods.

To assess both the effectiveness and the necessity of our attribution-based reward design, we conduct an ablation study comparing different gradient attribution strategies. The corresponding results are reported in Table [2](#S5.T2 "Table 2 ‣ 5.4 Ablation Study ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"). Specifically, we contrast our proposed *Gradient $\times$ Embedding* formulation with magnitude-based alternatives, namely the $L_{1}$ and $L_{2}$ norms of gradients. Implementation details and formal definitions are deferred to Appendix [A.2](#A1.SS2 "A.2 Details of Gradient Attribution Baselines ‣ Appendix A Implementation Details ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"). We use Qwen2.5-1.5B-Instruct as the policy and the training-time judge, and evaluate performance with Qwen3-30B-A3B-Instruct as the test grader.

Compared to Vanilla-GRPO, which relies solely on sequence-level rewards, all gradient-assisted variants (using $L_{1},L_{2}$ norms) consistently deliver notable improvements across benchmarks. These results provide strong empirical evidence that dense, token-level supervision derived from gradients offers richer and more informative learning signals, enabling more effective policy optimization than sparse, sequence-level rewards. While both $L_{1}$ and $L_{2}$ norms already outperform sparse-reward baselines, our *Gradient $\times$ Embedding* approach consistently achieves the best performance—for example, improving HealthBench from 38.0 to 44.5 and RaR-Science from 40.0 to 43.5. These results indicate that our method provides more accurate token-level rewards, leading to more effective policy optimization.

As shown in Section [4.3](#S4.SS3 "4.3 Theoretical Analysis of the Reward Design ‣ 4 Methodology ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), *Gradient $\times$ Embedding* naturally arises from the first-order Taylor expansion of the Judge’s decision function, directly approximating each token’s contribution to the Judge’s verdict. In contrast, norm-based metrics capture only gradient magnitude and discard directional information. By preserving gradient directionality, our formulation explicitly ensures that token-level rewards remain mathematically consistent with the global optimization objective, which is essential for dense supervision.

### 5.5 Extended Analysis

In this section, we conduct a more in-depth analysis of our method by investigating the following research questions. RQ1: How does the performance of our self-judging mechanism compare with that of a more capable external Judge model? RQ2: Can our Grad2Reward be extended to other RL optimization methods? RQ3: How well does a policy trained with Grad2Reward on one dataset generalize to other datasets? RQ4: How does our gradient-based reward attribution method perform compared with latest developed process reward models?

#### 5.5.1 Analysis of the Self-Judging Mechanism

|                                          |                    |                     |                   |                    |
|------------------------------------------|--------------------|---------------------|-------------------|--------------------|
| Judge for training                       |  Health Bench      |  RaR- Medicine      |  Research QA      |  RaR- Science      |
|  Qwen2.5-1.5B-Instruct Self-judging      | 44.5               | 35.5                | 55.0              | 43.3               |
| Qwen2.5-7B-Instruct                      | 45.3               | 36.6                | 55.6              | 43.1               |
| Llama3.1-8B-Instruct                     | 43.7               | 34.5                | 56.8              | 43.6               |
| Qwen3-30B                                | 45.9               | 36.3                | 55.4              | 43.5               |

Table 3: Performance of different Judge used for training when the policy uses Qwen2.5-1.5B-Instruct.

##### Self-judging achieves competitive performance (RQ1).

Table [3](#S5.T3 "Table 3 ‣ 5.5.1 Analysis of the Self-Judging Mechanism ‣ 5.5 Extended Analysis ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning") compares the performance of policies trained with different Judge models while fixing the policy to Qwen2.5-1.5B-Instruct. Overall, using the policy itself as the judge, namely the self-judging mechanism, achieves performance that is highly competitive with, and in some cases comparable to, training with substantially larger and more capable judge models. Across all four benchmarks, the self-judging setup consistently delivers strong results, with only marginal gaps relative to larger judges, including Qwen2.5-7B, Llama3.1-8B, and Qwen3-30B. Notably, on HealthBench and RaR-Medicine, self-judging performs on par with or only slightly below the best-performing external judges, while exhibiting comparable performance on ResearchQA and RaR-Science. These results indicate that the proposed learning signal does not critically rely on a stronger external Judge. Instead, the policy model itself can provide sufficiently informative evaluative feedback for its own optimization.

#### 5.5.2 Grad2Reward with RLOO

|                    |                    |                     |                   |                    |
|--------------------|--------------------|---------------------|-------------------|--------------------|
|                    |  Health Bench      |  RaR- Medicine      |  Research QA      |  RaR- Science      |
| Vanilla-RLOO       | 39.3               | 33.5                | 52.2              | 41.0               |
| RuscaRL            | 40.5               | 32.5                | 49.3              | 42.3               |
| Grad2Reward (ours) | 42.9               | 33.9                | 57.2              | 42.8               |

Table 4: Performance of our Grad2Reward against baselines under RLOO optimization.

|                                         |                |                    |                      |             |             |            |
|-----------------------------------------|----------------|--------------------|----------------------|-------------|-------------|------------|
| Method                                  |  MATH 500      |  Minerva Math      |  Olympiad Bench      |  AIME25     |  AIME24     |  AMC23     |
| PURE ([Cheng et al., 2025](#bib.bib16)) | 76.0           | 30.8               | 36.7                 | 13.3        | 26.6        | 70.0       |
| PRM ([Wang et al., 2024a](#bib.bib17))  | 71.6           | 36.3               | 32.5                 | 13.3        | 10.0        | 57.5       |
| PQM ([Li and Li, 2025](#bib.bib27))     | 72.0           | 34.1               | 34.3                 | 13.3        | 13.3        | 52.5       |
| Grad2Reward (ours)                      | 77.6           | 36.7               | 38.3                 | 16.6        | 26.6        | 65.0       |

Table 5: Pass@1 accuracy evaluated on six mathematical reasoning benchmarks.

|              |              |              |         |      |
|--------------|--------------|--------------|---------|------|
| Training Set | Test Set     | Vanilla-GRPO | RuscaRL | Ours |
| RaR-Medicine | HealthBench  | 37.6         | 37.3    | 42.1 |
| RaR-Science  | ResearchQA   | 45.1         | 46.2    | 48.6 |
|              | GPQA-Diamond | 24.7         | 25.6    | 26.1 |

Table 6: Cross-dataset generalization performance.

##### Grad2Reward remains effective under RLOO optimization (RQ2).

Table [4](#S5.T4 "Table 4 ‣ 5.5.2 Grad2Reward with RLOO ‣ 5.5 Extended Analysis ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning") reports the performance of Grad2Reward when integrated with the token-level RLOO algorithm, with details provided in Appendix [A.3](#A1.SS3 "A.3 RLOO Optimization ‣ Appendix A Implementation Details ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"). Sparse-reward baselines adopt the original RLOO algorithm. Despite replacing the underlying RL algorithm, Grad2Reward consistently outperforms both Vanilla-RLOO and RuscaRL across all four benchmarks, demonstrating that its advantages are not tied to a specific optimization scheme. In particular, Grad2Reward achieves a substantial improvement of +5.0 points over Vanilla-RLOO and +7.9 points over RuscaRL on ResearchQA. Similar gains are observed on HealthBench and RaR-Science, indicating robust performance across diverse tasks. These results indicate that the effectiveness of Grad2Reward stems from the reward formulation itself and remains compatible with different policy optimization schemes.

#### 5.5.3 Cross-Dataset Generalization

##### Grad2Reward-trained policies exhibit stronger cross-dataset generalization on both open-ended and verifiable tasks (RQ3).

As shown in Table [6](#S5.T6 "Table 6 ‣ 5.5.2 Grad2Reward with RLOO ‣ 5.5 Extended Analysis ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), when trained on RaR-Medicine and evaluated on HealthBench, our Grad2Reward significantly outperforms both Vanilla-GRPO and RuscaRL by 4.5 and 4.8 points. In the science domain, we train on RaR-Science and observe that Grad2Reward generalizes better to both the open-ended benchmark ResearchQA and the verifiable benchmark GPQA-Diamond ([Rein et al., 2024](#bib.bib36)). GPQA-Diamond demands multi-step scientific reasoning, requires precise factual grounding, and provides verifiable ground truth answers. Although trained only on the open-ended dataset, Grad2Reward achieves a score of 26.1 on GPQA-Diamond compared to 24.7 and 25.6 from Vanilla-GRPO and RuscaRL. This indicates that dense gradient-based reward improves the structural quality and factual fidelity of policy outputs, enabling better generalization beyond the training distribution and task format.

#### 5.5.4 Compared with PRMs on Mathematical Reasoning Tasks

Existing approaches in mathematical reasoning typically rely on PRMs to supply dense supervision. To compare against these approaches under a unified setting, we extend Grad2Reward to verifiable domains. Detailed implementation details are provided in the Appendix [A.5](#A1.SS5 "A.5 Extending Grad2Reward to Verifiable Domains ‣ Appendix A Implementation Details ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"). We compare our Grad2Reward with three representative dense reward modeling methods: PRM ([Wang et al., 2024b](#bib.bib26)), PQM ([Li and Li, 2025](#bib.bib27)), PURE ([Cheng et al., 2025](#bib.bib16)) The performance is evaluated on six widely adopted benchmarks: MATH500 ([Hendrycks et al., 2021](#bib.bib32)), Minerva Math ([Lewkowycz et al., 2022](#bib.bib33)), OlympiadBench ([He et al., 2024](#bib.bib35)), AIME24 ([MAA, 2024](#bib.bib30)), AIME25 ([MAA, 2025](#bib.bib31)), and AMC23 ([MAA, 2023](#bib.bib29)). We report the Pass@1 accuracy under the zero-shot setting.

##### Grad2Reward achieves better performance than PRMs on mathematical reasoning tasks.(RQ4)

Table [5](#S5.T5 "Table 5 ‣ 5.5.2 Grad2Reward with RLOO ‣ 5.5 Extended Analysis ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning") presents the comparative results. Overall, Grad2Reward demonstrates superior performance, achieving the highest accuracy on 5 out of 6 benchmarks. On MATH500, Grad2Reward attains 77.6% accuracy, surpassing PURE (76.0%) and substantially outperforming PQM (72.0%). On more challenging competition-level benchmarks such as AIME24, Grad2Reward matches the strong performance of PURE (26.6%) while significantly outperforming the standard PRM baseline, suggesting that gradient-based dense rewards can provide supervision quality comparable to explicitly trained PRMs even in constrained verifiable settings. These results demonstrate that extending Grad2Reward to verifiable domains preserves the core advantages observed in open-ended tasks. By providing dense and informative supervision, Grad2Reward generalizes effectively across benchmarks with varying reasoning complexity. This unified behavior positions Grad2Reward as a more scalable and flexible alternative to PRM-based approaches, capable of supporting both open-ended and verifiable reasoning tasks within a single reward framework.

## 6 Conclusion

In this work, we proposed Grad2Reward, which extracts dense, token-level rewards directly from the Judge’s internal gradient signals via a single backward pass. This approach addresses key limitations of prior methods, including sparse rewards and the black-box treatment of the Judge. Experimental results across diverse open-ended tasks and different policy models demonstrate that Grad2Reward consistently outperforms strong baselines, achieves competitive performance through self-judging, and offers superior training efficiency. Looking forward, our method can be extended to long-horizon agent tasks involving multiple decision steps and sustained reasoning, where gradient-based rewards have the potential to provide high-quality process supervision and enable more stable policy optimization.

## Impact Statement

This paper presents work aimed at advancing the field of machine learning by improving the training efficiency and reasoning quality of Large Language Models in open-ended domains. By introducing a framework for dense, token-level credit assignment, our research offers a path toward developing highly capable AI systems in fields where ground-truth verification is difficult, such as specialized research and creative problem-solving. This approach significantly reduces the need for expensive, human-intensive labeling and the reliance on massive external reward models, potentially lowering the barriers to entry for developing sophisticated AI agents.

However, the use of self-evaluative signals in sensitive areas like medical or legal consultation necessitates careful implementation. While the proposed method enhances reasoning consistency, the societal impact depends heavily on the accuracy of the underlying models used as judges. We encourage practitioners to combine our framework with robust safety guardrails and multi-faceted evaluation protocols to ensure that generated content remains factually accurate and ethically sound. The goal is to support the creation of reliable AI assistants that can provide nuanced and scientifically grounded support to human experts.

## References

- Ahmadian et al. (2024) A. Ahmadian, C. Cremer, M. Gallé, M. Fadaee, J. Kreutzer, O. Pietquin, A. Üstün, and S. Hooker Back to basics: revisiting REINFORCE-style optimization for learning from human feedback in LLMs. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), L. Ku, A. Martins, and V. Srikumar (Eds.), Bangkok, Thailand, pp. 12248–12267. External Links: [Link](https://aclanthology.org/2024.acl-long.662/), [Document](https://dx.doi.org/10.18653/v1/2024.acl-long.662) Cited by: [§4.4](#S4.SS4.p1.1 "4.4 Policy Optimization via Token-level GRPO ‣ 4 Methodology ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Arora et al. (2025) R. K. Arora, J. Wei, R. S. Hicks, P. Bowman, J. Quiñonero-Candela, F. Tsimpourlas, M. Sharman, M. Shah, A. Vallone, A. Beutel, et al. Healthbench: evaluating large language models towards improved human health. arXiv preprint arXiv:2505.08775. Cited by: [§A.4](#A1.SS4.p1.1 "A.4 Dataset Detail ‣ Appendix A Implementation Details ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§2](#S2.SS0.SSS0.Px1.p1.1 "LLM for Open-ended Tasks. ‣ 2 Related Work ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§5.1](#S5.SS1.SSS0.Px2.p1.1 "Datasets. ‣ 5.1 Experimental Settings ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Bi et al. (2025) B. Bi, S. Liu, Y. Wang, S. Tong, L. Mei, Y. Ge, Y. Xu, J. Guo, and X. Cheng Reward and guidance through rubrics: promoting exploration to improve multi-domain reasoning. arXiv preprint arXiv:2511.12344. Cited by: [§1](#S1.p2.1 "1 Introduction ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§1](#S1.p3.1 "1 Introduction ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§2](#S2.SS0.SSS0.Px1.p1.1 "LLM for Open-ended Tasks. ‣ 2 Related Work ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§3.2](#S3.SS2.p1.1 "3.2 LLM-as-a-Judge ‣ 3 Preliminary ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Chen et al. (2025) N. Chen, Z. Hu, Q. Zou, J. Wu, Q. Wang, B. Hooi, and B. He Judgelrm: large reasoning models as a judge. arXiv preprint arXiv:2504.00050. Cited by: [§2](#S2.SS0.SSS0.Px1.p1.1 "LLM for Open-ended Tasks. ‣ 2 Related Work ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Cheng et al. (2025) J. Cheng, G. Xiong, R. Qiao, L. Li, C. Guo, J. Wang, Y. Lv, and F. Wang Stop summation: min-form credit assignment is all process reward model needs for reasoning. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, External Links: [Link](https://openreview.net/forum?id=3Sxby0hH1q) Cited by: [§2](#S2.SS0.SSS0.Px2.p1.1 "Dense Rewards Modeling. ‣ 2 Related Work ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§5.5.4](#S5.SS5.SSS4.p1.1 "5.5.4 Compared with PRMs on Mathematical Reasoning Tasks ‣ 5.5 Extended Analysis ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [Table 5](#S5.T5.7.1.2.1 "In 5.5.2 Grad2Reward with RLOO ‣ 5.5 Extended Analysis ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Cobbe et al. (2021) K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert, J. Tworek, J. Hilton, R. Nakano, et al. Training verifiers to solve math word problems. arXiv preprint arXiv:2110.14168. Cited by: [§A.5](#A1.SS5.p1.1 "A.5 Extending Grad2Reward to Verifiable Domains ‣ Appendix A Implementation Details ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Cui et al. (2025) G. Cui, L. Yuan, Z. Wang, H. Wang, Y. Zhang, J. Chen, W. Li, B. He, Y. Fan, T. Yu, et al. Process reinforcement through implicit rewards. arXiv preprint arXiv:2502.01456. Cited by: [§2](#S2.SS0.SSS0.Px2.p1.1 "Dense Rewards Modeling. ‣ 2 Related Work ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Guan et al. (2025) X. Guan, L. L. Zhang, Y. Liu, N. Shang, Y. Sun, Y. Zhu, F. Yang, and M. Yang RStar-math: small LLMs can master math reasoning with self-evolved deep thinking. In Forty-second International Conference on Machine Learning, Cited by: [§A.5](#A1.SS5.p1.1 "A.5 Extending Grad2Reward to Verifiable Domains ‣ Appendix A Implementation Details ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Gunjal et al. (2025) A. Gunjal, A. Wang, E. Lau, V. Nath, Y. He, B. Liu, and S. Hendryx Rubrics as rewards: reinforcement learning beyond verifiable domains. arXiv preprint arXiv:2507.17746. Cited by: [§A.4](#A1.SS4.p1.1 "A.4 Dataset Detail ‣ Appendix A Implementation Details ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§1](#S1.p1.1 "1 Introduction ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§1](#S1.p2.1 "1 Introduction ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§1](#S1.p3.1 "1 Introduction ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§2](#S2.SS0.SSS0.Px1.p1.1 "LLM for Open-ended Tasks. ‣ 2 Related Work ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§3.2](#S3.SS2.p1.1 "3.2 LLM-as-a-Judge ‣ 3 Preliminary ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§4.1](#S4.SS1.p1.1 "4.1 Judge Implicitly Contains Process Feedback ‣ 4 Methodology ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§5.1](#S5.SS1.SSS0.Px2.p1.1 "Datasets. ‣ 5.1 Experimental Settings ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Guo et al. (2025) D. Guo, D. Yang, H. Zhang, J. Song, P. Wang, Q. Zhu, R. Xu, R. Zhang, S. Ma, X. Bi, et al. DeepSeek-r1 incentivizes reasoning in llms through reinforcement learning. Nature 645 (8081), pp. 633–638. Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- He et al. (2024) C. He, R. Luo, Y. Bai, S. Hu, Z. Thai, J. Shen, J. Hu, X. Han, Y. Huang, Y. Zhang, J. Liu, L. Qi, Z. Liu, and M. Sun OlympiadBench: a challenging benchmark for promoting AGI with olympiad-level bilingual multimodal scientific problems. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), L. Ku, A. Martins, and V. Srikumar (Eds.), Bangkok, Thailand, pp. 3828–3850. External Links: [Link](https://aclanthology.org/2024.acl-long.211/), [Document](https://dx.doi.org/10.18653/v1/2024.acl-long.211) Cited by: [§5.5.4](#S5.SS5.SSS4.p1.1 "5.5.4 Compared with PRMs on Mathematical Reasoning Tasks ‣ 5.5 Extended Analysis ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Hendrycks et al. (2021) D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang, D. Song, and J. Steinhardt Measuring mathematical problem solving with the MATH dataset. In Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 2), Cited by: [§A.5](#A1.SS5.p1.1 "A.5 Extending Grad2Reward to Verifiable Domains ‣ Appendix A Implementation Details ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§5.5.4](#S5.SS5.SSS4.p1.1 "5.5.4 Compared with PRMs on Mathematical Reasoning Tasks ‣ 5.5 Extended Analysis ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Hu et al. (2025) J. Hu, Y. Zhang, Q. Han, D. Jiang, X. Zhang, and H. Shum Open-reasoner-zero: an open source approach to scaling up reinforcement learning on the base model. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, External Links: [Link](https://openreview.net/forum?id=NFM8F5cV0V) Cited by: [§A.5](#A1.SS5.SSS0.Px1.p2.1 "Combining Grad2Reward with an Outcome Reward Model. ‣ A.5 Extending Grad2Reward to Verifiable Domains ‣ Appendix A Implementation Details ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Huang et al. (2025) Z. Huang, Y. Zhuang, G. Lu, Z. Qin, H. Xu, T. Zhao, R. Peng, J. Hu, Z. Shen, X. Hu, et al. Reinforcement learning with rubric anchors. arXiv preprint arXiv:2508.12790. Cited by: [§2](#S2.SS0.SSS0.Px1.p1.1 "LLM for Open-ended Tasks. ‣ 2 Related Work ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Jaech et al. (2024) A. Jaech, A. Kalai, A. Lerer, A. Richardson, A. El-Kishky, A. Low, A. Helyar, A. Madry, A. Beutel, A. Carney, et al. Openai o1 system card. arXiv preprint arXiv:2412.16720. Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Lee et al. (2025) Y. Lee, J. Kim, J. Kim, H. Cho, J. Kang, P. Kang, and N. Kim Checkeval: a reliable llm-as-a-judge framework for evaluating text generation using checklists. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing, pp. 15782–15809. Cited by: [§2](#S2.SS0.SSS0.Px1.p1.1 "LLM for Open-ended Tasks. ‣ 2 Related Work ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Lewkowycz et al. (2022) A. Lewkowycz, A. Andreassen, D. Dohan, E. Dyer, H. Michalewski, V. Ramasesh, A. Slone, C. Anil, I. Schlag, T. Gutman-Solo, et al. Solving quantitative reasoning problems with language models. Advances in Neural Information Processing Systems 35, pp. 3843–3857. Cited by: [§5.5.4](#S5.SS5.SSS4.p1.1 "5.5.4 Compared with PRMs on Mathematical Reasoning Tasks ‣ 5.5 Extended Analysis ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Li and Li (2025) W. Li and Y. Li Process reward model with q-value rankings. In The Thirteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=wQEdh2cgEk) Cited by: [§A.5](#A1.SS5.p1.1 "A.5 Extending Grad2Reward to Verifiable Domains ‣ Appendix A Implementation Details ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§2](#S2.SS0.SSS0.Px2.p1.1 "Dense Rewards Modeling. ‣ 2 Related Work ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§5.5.4](#S5.SS5.SSS4.p1.1 "5.5.4 Compared with PRMs on Mathematical Reasoning Tasks ‣ 5.5 Extended Analysis ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [Table 5](#S5.T5.7.1.4.1 "In 5.5.2 Grad2Reward with RLOO ‣ 5.5 Extended Analysis ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Lightman et al. (2024) H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J. Schulman, I. Sutskever, and K. Cobbe Let’s verify step by step. In The Twelfth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=v8L0pN6EOi) Cited by: [§2](#S2.SS0.SSS0.Px2.p1.1 "Dense Rewards Modeling. ‣ 2 Related Work ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- MAA (2023) MAA American invitational mathematics examination (aime). Note: [https://maa.org/](https://maa.org/) Cited by: [§5.5.4](#S5.SS5.SSS4.p1.1 "5.5.4 Compared with PRMs on Mathematical Reasoning Tasks ‣ 5.5 Extended Analysis ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- MAA (2024) MAA American invitational mathematics examination (aime). Note: [https://maa.org/](https://maa.org/) Cited by: [§5.5.4](#S5.SS5.SSS4.p1.1 "5.5.4 Compared with PRMs on Mathematical Reasoning Tasks ‣ 5.5 Extended Analysis ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- MAA (2025) MAA American invitational mathematics examination (aime). Note: [https://maa.org/](https://maa.org/) Cited by: [§5.5.4](#S5.SS5.SSS4.p1.1 "5.5.4 Compared with PRMs on Mathematical Reasoning Tasks ‣ 5.5 Extended Analysis ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Rein et al. (2024) D. Rein, B. L. Hou, A. C. Stickland, J. Petty, R. Y. Pang, J. Dirani, J. Michael, and S. R. Bowman Gpqa: a graduate-level google-proof q&a benchmark. In First Conference on Language Modeling, Cited by: [§5.5.3](#S5.SS5.SSS3.Px1.p1.1 "Grad2Reward-trained policies exhibit stronger cross-dataset generalization on both open-ended and verifiable tasks (RQ3). ‣ 5.5.3 Cross-Dataset Generalization ‣ 5.5 Extended Analysis ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Shao et al. (2025) R. Shao, A. Asai, S. Z. Shen, H. Ivison, V. Kishore, J. Zhuo, X. Zhao, M. Park, S. G. Finlayson, D. Sontag, et al. Dr tulu: reinforcement learning with evolving rubrics for deep research. arXiv preprint arXiv:2511.19399. Cited by: [§1](#S1.p2.1 "1 Introduction ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§2](#S2.SS0.SSS0.Px1.p1.1 "LLM for Open-ended Tasks. ‣ 2 Related Work ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§3.2](#S3.SS2.p1.1 "3.2 LLM-as-a-Judge ‣ 3 Preliminary ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§4.1](#S4.SS1.p1.1 "4.1 Judge Implicitly Contains Process Feedback ‣ 4 Methodology ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Shao et al. (2024) Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang, Y. Li, Y. Wu, et al. Deepseekmath: pushing the limits of mathematical reasoning in open language models. arXiv preprint arXiv:2402.03300. Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§4.4](#S4.SS4.p1.1 "4.4 Policy Optimization via Token-level GRPO ‣ 4 Methodology ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Sheng et al. (2024) G. Sheng, C. Zhang, Z. Ye, X. Wu, W. Zhang, R. Zhang, Y. Peng, H. Lin, and C. Wu HybridFlow: a flexible and efficient rlhf framework. arXiv preprint arXiv: 2409.19256. Cited by: [§A.1](#A1.SS1.p1.1 "A.1 Policy Training ‣ Appendix A Implementation Details ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Song et al. (2025) Y. Song, H. Zhang, C. Eisenach, S. M. Kakade, D. Foster, and U. Ghai Mind the gap: examining the self-improvement capabilities of large language models. In The Thirteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=mtJSMcF3ek) Cited by: [§4.1](#S4.SS1.SSS0.Px1.p1.1 "Self-Judging Mechanism. ‣ 4.1 Judge Implicitly Contains Process Feedback ‣ 4 Methodology ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Sun et al. (2025) W. Sun, W. Yang, P. Jian, Q. Du, F. Cui, S. Ren, and J. Zhang KTAE: a model-free algorithm to key-tokens advantage estimation in mathematical reasoning. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, External Links: [Link](https://openreview.net/forum?id=yqQVRNdmKJ) Cited by: [§4.4](#S4.SS4.p1.1 "4.4 Policy Optimization via Token-level GRPO ‣ 4 Methodology ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Sundararajan et al. (2017) M. Sundararajan, A. Taly, and Q. Yan Axiomatic attribution for deep networks. In International conference on machine learning, pp. 3319–3328. Cited by: [§4.3](#S4.SS3.p1.4 "4.3 Theoretical Analysis of the Reward Design ‣ 4 Methodology ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Wang et al. (2024a) P. Wang, L. Li, Z. Shao, R. Xu, D. Dai, Y. Li, D. Chen, Y. Wu, and Z. Sui Math-shepherd: verify and reinforce LLMs step-by-step without human annotations. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), L. Ku, A. Martins, and V. Srikumar (Eds.), Bangkok, Thailand, pp. 9426–9439. External Links: [Link](https://aclanthology.org/2024.acl-long.510/), [Document](https://dx.doi.org/10.18653/v1/2024.acl-long.510) Cited by: [§2](#S2.SS0.SSS0.Px2.p1.1 "Dense Rewards Modeling. ‣ 2 Related Work ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [Table 5](#S5.T5.7.1.3.1 "In 5.5.2 Grad2Reward with RLOO ‣ 5.5 Extended Analysis ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Wang et al. (2024b) P. Wang, L. Li, Z. Shao, R. Xu, D. Dai, Y. Li, D. Chen, Y. Wu, and Z. Sui Math-shepherd: verify and reinforce llms step-by-step without human annotations. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 9426–9439. Cited by: [§A.5](#A1.SS5.p1.1 "A.5 Extending Grad2Reward to Verifiable Domains ‣ Appendix A Implementation Details ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§2](#S2.SS0.SSS0.Px2.p1.1 "Dense Rewards Modeling. ‣ 2 Related Work ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§5.5.4](#S5.SS5.SSS4.p1.1 "5.5.4 Compared with PRMs on Mathematical Reasoning Tasks ‣ 5.5 Extended Analysis ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Wang et al. (2025) P. Wang, P. Liu, Z. Sang, C. Xie, H. Yang, et al. InfiMed-orbit: aligning llms on open-ended complex tasks via rubric-based incremental training. arXiv preprint arXiv:2510.15859. Cited by: [§1](#S1.p3.1 "1 Introduction ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§2](#S2.SS0.SSS0.Px1.p1.1 "LLM for Open-ended Tasks. ‣ 2 Related Work ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Wu et al. (2025) T. Wu, W. Yuan, O. Golovneva, J. Xu, Y. Tian, J. Jiao, J. E. Weston, and S. Sukhbaatar Meta-rewarding language models: self-improving alignment with llm-as-a-meta-judge. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing, pp. 11548–11565. Cited by: [§2](#S2.SS0.SSS0.Px1.p1.1 "LLM for Open-ended Tasks. ‣ 2 Related Work ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Xu et al. (2025) Y. Xu, T. Chakraborty, S. Sharma, L. Nunes, E. Kıcıman, S. Lu, and R. Chandra Direct reasoning optimization: llms can reward and refine their own reasoning for open-ended tasks. arXiv preprint arXiv:2506.13351. Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Ye et al. (2025) Z. Ye, Y. Yue, H. Wang, X. Han, J. Jiang, C. Wei, L. Fan, J. Liang, S. Zhang, J. Li, et al. Self-rewarding rubric-based reinforcement learning for open-ended reasoning. arXiv preprint arXiv:2509.25534. Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Yifei et al. (2025) L. S. Yifei, A. Chang, C. Malaviya, and M. Yatskar Researchqa: evaluating scholarly question answering at scale across 75 fields with survey-mined questions and rubrics. arXiv preprint arXiv:2509.00496. Cited by: [§A.4](#A1.SS4.p1.1 "A.4 Dataset Detail ‣ Appendix A Implementation Details ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§2](#S2.SS0.SSS0.Px1.p1.1 "LLM for Open-ended Tasks. ‣ 2 Related Work ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§5.1](#S5.SS1.SSS0.Px2.p1.1 "Datasets. ‣ 5.1 Experimental Settings ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Yu et al. (2024) F. Yu, A. Gao, and B. Wang Ovm, outcome-supervised value models for planning in mathematical reasoning. In Findings of the Association for Computational Linguistics: NAACL 2024, pp. 858–875. Cited by: [§A.5](#A1.SS5.p1.1 "A.5 Extending Grad2Reward to Verifiable Domains ‣ Appendix A Implementation Details ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Yu et al. (2025) Q. Yu, Z. Zhang, R. Zhu, Y. Yuan, X. Zuo, YuYue, W. Dai, T. Fan, G. Liu, J. Liu, L. Liu, X. Liu, H. Lin, Z. Lin, B. Ma, G. Sheng, Y. Tong, C. Zhang, M. Zhang, R. Zhang, W. Zhang, H. Zhu, J. Zhu, J. Chen, J. Chen, C. Wang, H. Yu, Y. Song, X. Wei, H. Zhou, J. Liu, W. Ma, Y. Zhang, L. Yan, Y. Wu, and M. Wang DAPO: an open-source LLM reinforcement learning system at scale. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, External Links: [Link](https://openreview.net/forum?id=2a36EMSSTp) Cited by: [§4.4](#S4.SS4.p1.1 "4.4 Policy Optimization via Token-level GRPO ‣ 4 Methodology ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Zeng et al. (2025) T. Zeng, S. Zhang, S. Wu, C. Classen, D. Chae, E. Ewer, M. Lee, H. Kim, W. Kang, J. Kunde, Y. Fan, J. Kim, H. I. Koo, K. Ramchandran, D. Papailiopoulos, and K. Lee VersaPRM: multi-domain process reward model via synthetic reasoning data. In Forty-second International Conference on Machine Learning, External Links: [Link](https://openreview.net/forum?id=l19DmXbwPK) Cited by: [§2](#S2.SS0.SSS0.Px2.p1.1 "Dense Rewards Modeling. ‣ 2 Related Work ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Zhang et al. (2025a) Z. Zhang, Z. Shan, K. Song, Y. Li, and K. Ren Linking process to outcome: conditional reward modeling for llm reasoning. arXiv preprint arXiv:2509.26578. Cited by: [§2](#S2.SS0.SSS0.Px2.p1.1 "Dense Rewards Modeling. ‣ 2 Related Work ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Zhang et al. (2025b) Z. Zhang, C. Zheng, Y. Wu, B. Zhang, R. Lin, B. Yu, D. Liu, J. Zhou, and J. Lin The lessons of developing process reward models in mathematical reasoning. arXiv preprint arXiv:2501.07301. Cited by: [§A.5](#A1.SS5.p1.1 "A.5 Extending Grad2Reward to Verifiable Domains ‣ Appendix A Implementation Details ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Zheng et al. (2025) C. Zheng, Z. Zhang, B. Zhang, R. Lin, K. Lu, B. Yu, D. Liu, J. Zhou, and J. Lin Processbench: identifying process errors in mathematical reasoning. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 1009–1024. Cited by: [§A.5](#A1.SS5.p1.1 "A.5 Extending Grad2Reward to Verifiable Domains ‣ Appendix A Implementation Details ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").
- Zhou et al. (2025) Y. Zhou, S. Li, S. Liu, W. Fang, K. Zhang, J. Zhao, J. Yang, Y. Zhou, J. Lv, T. Zheng, et al. Breaking the exploration bottleneck: rubric-scaffolded reinforcement learning for general llm reasoning. arXiv preprint arXiv:2508.16949. Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§1](#S1.p2.1 "1 Introduction ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§1](#S1.p3.1 "1 Introduction ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§2](#S2.SS0.SSS0.Px1.p1.1 "LLM for Open-ended Tasks. ‣ 2 Related Work ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§3.2](#S3.SS2.p1.1 "3.2 LLM-as-a-Judge ‣ 3 Preliminary ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§4.1](#S4.SS1.p1.1 "4.1 Judge Implicitly Contains Process Feedback ‣ 4 Methodology ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), [§5.1](#S5.SS1.SSS0.Px4.p1.1 "Baselines. ‣ 5.1 Experimental Settings ‣ 5 Experiments ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning").

## Appendix A Implementation Details

### A.1 Policy Training

We train with a fixed learning rate of $1 \times 10^{- 6}$, a prompt batch size of 32, and 8 sampled responses per prompt, with the clipping ratio set to $\epsilon = 0.2$. Sampling is performed via vLLM with temperature $0.7$, top-p $0.8$, top-k $20$, and a maximum response length of 4096 tokens. At test time we set the temperature to 0 and top-p to 1. All baselines and our method are implemented using the veRL ([Sheng et al., 2024](#bib.bib9)) framework, and all experiments are conducted on 8 NVIDIA H20 GPUs.

### A.2 Details of Gradient Attribution Baselines

In the ablation study regarding gradient attribution methods, we employ the exact same pipeline as our proposed framework, with the only difference being the calculation of the importance score $a_{t}$. We substitute the *Gradient $\times$ Embedding* calculation in ([3](#S4.E3 "Equation 3 ‣ 4.2 Fine-Grained Reward Design ‣ 4 Methodology ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")) with the following two formulations respectively:

##### $L_{1}$ norm baseline.

We compute the importance score as the $L_{1}$ norm of the gradient vector $\mathbf{g}_{t}$:

|     |                                                                           |     |      |
|-----|---------------------------------------------------------------------------|-----|------|
|     | $$b_{k,t} = {\|\mathbf{g}_{k,t}\|}_{1} = {\sum\limits_{i}{|g_{k,t,i}|}}$$ |     | (11) |

##### $L_{2}$ norm baseline.

We compute the importance score as the $L_{2}$ norm (Euclidean norm) of the gradient vector $\mathbf{g}_{t}$:

|     |                                                                                |     |      |
|-----|--------------------------------------------------------------------------------|-----|------|
|     | $$b_{k,t} = {\|\mathbf{g}_{k,t}\|}_{2} = \sqrt{\sum\limits_{i}g_{k,t,i}^{2}}$$ |     | (12) |

### A.3 RLOO Optimization

RLOO (Leave-One-Out) is an advantage estimation method based on multiple samples for optimizing policy gradients in reinforcement learning. To provide finer-grained and lower-variance advantage estimates, we use token level RLOO to construct a baseline estimate using multiple output responses excluding the current sample. In our setup, given a query, the model generates $G$ responses, each containing at most $M$ tokens. Let $r_{i,j}$ denotes the reward of $j$-th token in the $i$-th response, we compute the corresponding advantage ${\hat{A}}_{i,t}$ by subtracting the cumulative rewards by an average baseline from parallel samples:

|     |                                                                                                                                                                                                                      |     |      |
|-----|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|------|
|     | $${\hat{A}}_{i,t} = {{\sum\limits_{k = t}^{M}r_{i,k}} - {\frac{1}{{({G - 1})}\hspace{0pt}M}\hspace{0pt}{\sum\limits_{\substack{j = 1 \\ j \neq i}}^{G}{\sum\limits_{s = 1}^{M}{\sum\limits_{k = s}^{M}r_{j,k}}}}}}$$ |     | (13) |

### A.4 Dataset Detail

HealthBench ([Arora et al., 2025](#bib.bib4)) assesses LLM performance in healthcare and contains 5,000 samples, from which we select 500 instances as the test set and use the remaining samples for training. RaR-Medicine ([Gunjal et al., 2025](#bib.bib2)) evaluates a model’s medical question answering ability. After removing samples with duplicate questions, we partition the dataset into a training set with 17,011 samples and a test set with 500 samples. ResearchQA ([Yifei et al., 2025](#bib.bib11)) is a large-scale benchmark for long-form scholarly question answering spanning 75 academic fields, using queries and rubrics mined from survey articles. We split the dataset into a training set with 16,961 instances and a test set with 500 instances. RaR-Science ([Gunjal et al., 2025](#bib.bib2)) evaluates model performance in the science domain. After removing duplicate-question samples as well, we divide the dataset into a training set with 16,365 samples and a test set with 500 samples.

### A.5 Extending Grad2Reward to Verifiable Domains

PRMs Baseline Training. The reward models are initialized from Qwen2.5-Math-7B and trained on the Math-Shepherd ([Wang et al., 2024b](#bib.bib26)) dataset, which integrates questions from GSM8K ([Cobbe et al., 2021](#bib.bib38)) and MATH ([Hendrycks et al., 2021](#bib.bib32)) and provides responses annotated with step-level process labels. To separate reasoning steps, we follow prior work ([Yu et al., 2024](#bib.bib41); [Zheng et al., 2025](#bib.bib42); [Zhang et al., 2025b](#bib.bib34)), using newline characters to indicate boundaries between individual steps. Following prior work ([Li and Li, 2025](#bib.bib27); [Guan et al., 2025](#bib.bib37)), we augment the pre-trained model with an additional value head to directly output scalar rewards. We used the ZeRO-2 optimization stage of DeepSpeed with bfloat16 precision to train the model, and employed AdamW optimizer with a learning rate of 5e-6 and a batch size of 32.

##### Combining Grad2Reward with an Outcome Reward Model.

When applying Grad2Reward to mathematical domains, we employ an outcome reward model (ORM) and perform gradient attribution on it. We show the full algorithm when combining Grad2Reward with discriminative ORMs. Unlike the generative judge setting where the target is a decision token $z$, an ORM $V$ maps the input $x$ and response $o$ directly to a scalar score $V{(x,o)}$, which reflects the ORM’s assessment of the response’s correctness. To extract dense rewards in this setting, we modify the gradient attribution objective to this scalar output. The gradient calculation in Eq. ([2](#S4.E2 "Equation 2 ‣ 4.2 Fine-Grained Reward Design ‣ 4 Methodology ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")) becomes:

|     |                                                                               |     |      |
|-----|-------------------------------------------------------------------------------|-----|------|
|     | $$\mathbf{g}_{\mathbf{t}} = {{\nabla_{\mathbf{e}_{t}}V}\hspace{0pt}{(x,o)}}$$ |     | (14) |

The attribution score $a_{t}$ and normalized reward $r_{t}$ are computed following the same procedure described in Section [4.2](#S4.SS2 "4.2 Fine-Grained Reward Design ‣ 4 Methodology ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"). Crucially, to fully leverage the global oversight of the ORM, we incorporate the final outcome score into the reward of the last token:

|     |                                                        |     |      |
|-----|--------------------------------------------------------|-----|------|
|     | $$r_{t} = \begin{cases}                                
       r_{t} & {{\text{if~}\hspace{0pt}t} < T} \\              
       {r_{t} + {V{(x,o)}}} & {{\text{if~}\hspace{0pt}t} = T}  
       \end{cases}$$                                           |     | (15) |

This ensures that the dense attribution signals remain anchored to the global verification result.

The policy model is based on Qwen2.5-Math-7B and is trained on the Orz-Math-57k ([Hu et al., 2025](#bib.bib28)) dataset. Following prior work, we adopt a token-level variant of RLOO as the RL optimization algorithm, where advantages are estimated based on token-level rewards.

The complete algorithm is provided in Algorithm [2](#alg2 "Algorithm 2 ‣ Combining Grad2Reward with an Outcome Reward Model. ‣ A.5 Extending Grad2Reward to Verifiable Domains ‣ Appendix A Implementation Details ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"). The algorithm is quite similar to Algorithm [1](#alg1 "Algorithm 1 ‣ 4.4 Policy Optimization via Token-level GRPO ‣ 4 Methodology ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"), with only a slight difference in gradient attribution and final reward calculation.

0:  Policy $\pi_{\theta}$, ORM $V$, dataset $\mathcal{D}$, group size $G$, temperature $\tau$

1:  Sample query $x \sim \mathcal{D}$

2:  Generate a group of responses ${\{ o_{i}\}}_{i = 1}^{G} \sim \pi_{\theta_{old}}{( \cdot \mid x)}$

3:  for $i = 1$ to $G$ do

4:   Compute token-level gradients:

5:   $\mathbf{g}_{\mathbf{t}} = {{\nabla_{\mathbf{e}_{t}}V}\hspace{0pt}{(x,o_{i})}}$

6:   Convert gradients to attribution score:

7:   ${b_{t} = {\mathbf{g}_{t}^{\top}\hspace{0pt}\mathbf{e}_{t}}},{\alpha_{t} = {{softmax}_{t}\hspace{0pt}{({b_{t}/\tau})}}}$

8:   Compute token rewards:

9:   $r_{i,t} = \begin{cases}
\alpha_{t} & {{\text{if~}\hspace{0pt}t} < T} \\
{\alpha_{t} + {V{(x,o_{i})}}} & {{\text{if~}\hspace{0pt}t} = T}
\end{cases}$

10:  end for

11:  Compute token-level returns $R_{i,t}$ and advantages ${\hat{A}}_{i,t}$ following Eq. ([13](#A1.E13 "Equation 13 ‣ A.3 RLOO Optimization ‣ Appendix A Implementation Details ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning")) using token rewards.

12:  Update $\theta$ via token-level RLOO objective in Eq. ([10](#S4.E10 "Equation 10 ‣ 4.4 Policy Optimization via Token-level GRPO ‣ 4 Methodology ‣ Grad2Reward: From Sparse Judgment to Dense Rewards for Improving Open-Ended LLM Reasoning"))

Algorithm 2 Policy Optimization for Verifiable Tasks via Grad2Reward

## Appendix B Case Study

##### Case Overview.

This case examines a travel health advisory scenario where a user inquires about malaria prophylaxis without specifying a destination. The task requires generating medically accurate, region-aware drug recommendations while minimizing safety risks.

![](img)

![](img)

![](img)

##### Comparative analysis.

In this case, our method shows a clear professional advantage by providing systematic, and accurate travel health guidance to users. First, our method explicitly distinguishes between different types of malaria such as P. falciparum and P. vivax and emphasizes that medications vary depending on the risk level of the destination. Second, our approach offers a complete decision-making framework, including assessing regional risk levels, distinguishing malaria types, recommending appropriate prophylaxis medications, considering side effects and contraindications, and integrating non-pharmaceutical precautions such as mosquito bite prevention. Our method achieves superior performance through intermediate process optimization. This fine-grained, stepwise optimization ensures both high factual fidelity and operational applicability, enabling the delivery of reliable and actionable guidance in safety-critical domains.

## Appendix C Prompt Template for Open-ended Tasks

![](img)

![](img)

Experimental support, please [view the build logs](./2602.01791v1/__stdout.txt) for errors. Generated by [ L A T E xml ![\[LOGO\]](img)](https://math.nist.gov/~BMiller/LaTeXML/) .

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
