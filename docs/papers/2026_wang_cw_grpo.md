---
title: "Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization"
authors: "Junzhe Wang; Zhiheng Xi; Yajie Yang; Hao Luo; Shihan Dou; Tao Gui; Qi Zhang"
year: 2026
source: https://arxiv.org/html/2604.14267
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

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) [![](img) Report Issue](# "Report an Issue") [![](img) Back to Abstract](/abs/2604.14267v2 "Back to abstract page") [![](img) Download PDF](/pdf/2604.14267v2 "Download PDF") [![](img)](javascript:toggleNavTOC(); "Toggle navigation") [![](img)](javascript:toggleReadingMode(); "Disable reading mode, show header and footer")

![](img) ![](img) ![](img)

1.  [Abstract](#abstract1 "In Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization")
2.  [1 Introduction](#S1 "In Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization")
3.  [2 Related Work](#S2 "In Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization")
4.  [3 Contribution-Weighted GRPO](#S3 "In Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization")
    1.  [3.1 Task Formulation](#S3.SS1 "In 3 Contribution-Weighted GRPO ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization")
    2.  [3.2 Outcome-Level Advantage](#S3.SS2 "In 3 Contribution-Weighted GRPO ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization")
    3.  [3.3 Round-Level Contribution Estimation](#S3.SS3 "In 3 Contribution-Weighted GRPO ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization")
        1.  [3.3.1 Signal Definition and Rubrics](#S3.SS3.SSS1 "In 3.3 Round-Level Contribution Estimation ‣ 3 Contribution-Weighted GRPO ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization")
        2.  [3.3.2 Judge Calibration and Reliability](#S3.SS3.SSS2 "In 3.3 Round-Level Contribution Estimation ‣ 3 Contribution-Weighted GRPO ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization")
    4.  [3.4 Adaptive Weighting Mechanism](#S3.SS4 "In 3 Contribution-Weighted GRPO ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization")
    5.  [3.5 Advantage Reallocation and Optimization](#S3.SS5 "In 3 Contribution-Weighted GRPO ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization")
5.  [4 Setup](#S4 "In Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization")
    1.  [4.1 Datasets and Evaluation Metrics](#S4.SS1 "In 4 Setup ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization")
    2.  [4.2 Baselines](#S4.SS2 "In 4 Setup ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization")
    3.  [4.3 Implementation Details](#S4.SS3 "In 4 Setup ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization")
6.  [5 Experimental Results](#S5 "In Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization")
    1.  [5.1 Main Results](#S5.SS1 "In 5 Experimental Results ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization")
    2.  [5.2 Sharpness of Advantage Reallocation](#S5.SS2 "In 5 Experimental Results ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization")
    3.  [5.3 Supervision Decomposition](#S5.SS3 "In 5 Experimental Results ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization")
    4.  [5.4 Training Dynamics](#S5.SS4 "In 5 Experimental Results ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization")
    5.  [5.5 Case Study](#S5.SS5 "In 5 Experimental Results ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization")
7.  [6 Discussion: Generalization Across Tasks and Models](#S6 "In Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization")
8.  [7 Conclusion](#S7 "In Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization")
9.  [References](#bib "In Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization")
10. [A Analysis of Failure Trajectories and Credit Assignment Ambiguity](#A1 "In Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization")
11. [B LLM Judge Calibration Details](#A2 "In Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization")
12. [C Computational Cost of LLM Judge](#A3 "In Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization")
13. [D Prompts](#A4 "In Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization")

[License: CC BY 4.0](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2604.14267v2 \[cs.LG\] 20 Apr 2026

^(†)^(†) ^(\*)Equal contribution. ^(†)Corresponding authors.^(†)^(†) ¹Our code is available at [https://github.com/zsxmwjz/CW-GRPO](https://github.com/zsxmwjz/CW-GRPO).

# Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization

Junzhe Wang Affiliation: Fudan University Email: [jzwang24@m.fudan.edu.cn](mailto:)    Zhiheng Xi^(\*) Affiliation: Fudan University Email: [qz@fudan.edu.cn](mailto:)    Yajie Yang Affiliation: Fudan University    Hao Luo Affiliation: Fudan University    Shihan Dou Affiliation: Fudan University    Tao Gui Affiliation: Fudan University    Qi Zhang Affiliation: Fudan University Affiliation: Shanghai Artificial Intelligence Laboratory Affiliation: Shanghai Key Laboratory of Intelligent Information Processing

###### Abstract

Search agents extend Large Language Models (LLMs) beyond static parametric knowledge by enabling access to up-to-date and long-tail information unavailable during pretraining. While reinforcement learning has been widely adopted for training such agents, existing approaches face key limitations: process supervision often suffers from unstable value estimation, whereas outcome supervision struggles with credit assignment due to sparse, trajectory-level rewards. To bridge this gap, we propose Contribution-Weighted GRPO (CW-GRPO), a framework that integrates process supervision into group relative policy optimization. Instead of directly optimizing process rewards, CW-GRPO employs an LLM judge to assess the retrieval utility and reasoning correctness at each search round, producing per-round contribution scores. These scores are used to rescale outcome-based advantages along the trajectory, enabling fine-grained credit assignment without sacrificing optimization stability. Experiments on multiple knowledge-intensive benchmarks show that CW-GRPO outperforms standard GRPO by 5.0% on Qwen3-8B and 6.3% on Qwen3-1.7B, leading to more effective search behaviors. Additional analysis reveals that successful trajectories exhibit concentrated contributions in specific rounds, providing empirical insight into search agent tasks.

Figure 1: CW-GRPO assesses the quality of each search round within successful trajectories and to concentrate the learning advantage on high-quality search rounds, thereby enabling round-level credit assignment.

## 1 Introduction

Search agents empower large language models (LLMs) to move beyond fixed parametric knowledge by providing access to real-time information and specialized facts absent from pre-training ([Li et al., 2025a](#bib.bib15); [Zhang et al., 2025a](#bib.bib44)). Through iterative retrieval of external evidence and integration into the reasoning process, search agents ground model predictions in verifiable sources and substantially enhance the factual reliability of LLM-based systems ([Zhao et al., 2026](#bib.bib46); [Li et al., 2025b](#bib.bib16); [Zhou et al., 2024](#bib.bib48); [Wang et al., 2025a](#bib.bib36)). Consequently, they have become a key role in enabling LLMs to perform knowledge-intensive and fact-sensitive tasks ([Glass et al., 2022](#bib.bib4); [Sawarkar et al., 2024](#bib.bib24)).

While reinforcement learning (RL) offers a significant paradigm for training such agents, current RL approaches suffer from fundamental limitations ([Jin et al., 2025a](#bib.bib10)). Depending on the level of supervision, they can be broadly categorized into process supervision and outcome supervision ([Uesato et al., 2022](#bib.bib35)). Process supervision ([Lightman et al., 2023](#bib.bib18); [Zhu et al., 2025](#bib.bib49); [Wang et al., 2025b](#bib.bib38)) assigns round-level rewards and is commonly optimized with actor–critic methods such as Proximal Policy Optimization ([Schulman et al., 2017](#bib.bib25)), but learning reliable critics over diverse intermediate states is unstable and frequently leads to biased advantages and brittle training ([Liu et al., 2024](#bib.bib20); [Kazemnejad et al., 2025](#bib.bib13)). Outcome supervision, by contrast, relies solely on final answer correctness, which makes it difficult to attribute task success to individual search rounds, leading to a credit assignment problem and obscuring the uneven contributions of intermediate decisions. Recent advances, such as Group Relative Policy Optimization ([Shao et al., 2024](#bib.bib26)), improve training stability and memory efficiency, making outcome-supervised optimization more practical; however, they ([Jin et al., 2025b](#bib.bib11); [Wang et al., 2025a](#bib.bib36)) do not alter the sparsity of the reward signal, and the credit assignment issue remains unresolved.

To address the aforementioned challenges, we propose Contribution-Weighted GRPO (CW-GRPO), which reformulates process supervision as a problem of modulating outcome-derived advantages, rather than directly optimizing process rewards. Specifically, CW-GRPO retains the stability of the standard GRPO by computing outcome advantages through group-relative comparisons. We use an LLM judge to assess each search round based on retrieval utility and reasoning correctness. These metrics are synthesized into a contribution score, based on which serves as a scaling factor to redistribute the outcome advantage across the trajectory. By avoiding direct comparison of process rewards, CW-GRPO incorporates process supervision into the GRPO framework, amplifying learning signals for informative rounds while suppressing those for redundant or unproductive ones, as illustrated in Figure [1](#S0.F1 "Figure 1 ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization").

Empirical results across multiple knowledge-intensive benchmarks demonstrate that CW-GRPO consistently outperforms both outcome-supervised and process-supervised baselines, enabling more effective search behaviors. Specifically, CW-GRPO achieves significant performance gains over standard GRPO, with relative improvements of $5.0\%$ on Qwen3-8B and $6.3\%$ on Qwen3-1.7B. The contributions of this work are summarized as follows:

- •
  A Reframing of Process Supervision: We introduce a new perspective that treats process supervision for search agents as advantage reallocation guided by round contribution, rather than explicit process reward estimation.
- •
  Contribution-Weighted GRPO: We propose a new optimization framework that brings process-level credit assignment into GRPO without requiring unstable value functions.
- •
  Empirical Characterization of Search Contribution: We provide empirical evidence showing a structural characteristic in search agent tasks: the contribution to task success is highly concentrated in informative rounds rather than being uniformly distributed.

## 2 Related Work

Agentic Search. Large language models encode knowledge in static parameters, limiting access to up-to-date and long-tail knowledge. Retrieval-augmented generation (RAG) addresses this by enabling models to access external knowledge sources ([Zhang et al., 2026](#bib.bib43); [Zhao et al., 2026](#bib.bib46); [Li et al., 2025b](#bib.bib16); [Zhou et al., 2024](#bib.bib48)). Pioneering retrieval-augmented reasoning works such as IRCoT ([Trivedi et al., 2023](#bib.bib34)) and FLARE ([Jiang et al., 2023](#bib.bib9)) use prompts to guide iterative reasoning and reduce model uncertainty, and Self-RAG ([Asai et al., 2024](#bib.bib2)) adopts supervised fine-tuning with reflection tokens for adaptive retrieval. More recently, agentic search enables LLMs to interact with real-world search engines for dynamic information access. WebGPT ([Nakano et al., 2022](#bib.bib22)) pioneers this direction using RLHF. Search-o1 ([Li et al., 2025a](#bib.bib15)) integrates agentic search into large reasoning models via prompting, while Search-R1 ([Jin et al., 2025b](#bib.bib11)), R1-Searcher ([Song et al., 2025](#bib.bib29)) and MM-Doc-R1 ([Lin et al., 2026](#bib.bib19)) adopt RL for end-to-end training with outcome-based rewards. However, outcome supervision assigns uniform credit across search rounds, failing to distinguish pivotal searches from redundant ones.

Outcome Supervision and Process Supervision. A key challenge in training search agents lies in credit assignment across multi-round search trajectories. *Outcome supervision*, widely adopted in RL methods like PPO ([Schulman et al., 2017](#bib.bib25)) and GRPO ([Shao et al., 2024](#bib.bib26)), assigns rewards only based on the final answer, treating all immediate rounds equally and ignoring their unequal contributions. *Process supervision* addresses this via round-level feedback for finer-grained credit assignment. Early approaches to process supervision rely on learned Process Reward Models (PRMs), but often suffer from costly round-level annotation requirements and limited out-of-domain generalizability ([Lightman et al., 2023](#bib.bib18); [Huang et al., 2025](#bib.bib8)). To avoid training explicit reward models, recent works increasingly leverage frozen LLMs as external evaluators to assess intermediate rounds. These methods use LLM-based judges to assess reasoning quality and then assign round-level rewards, enabling process supervision without training dedicated PRMs ([Zhang et al., 2025b](#bib.bib45)). These approaches typically optimize judge-produced signals directly as rewards, making them sensitive to evaluation noise and calibration errors. In contrast, CW-GRPO uses LLM-derived signals only to redistribute outcome-based advantages, avoiding direct optimization over noisy intermediate rewards and thereby enabling more stable training.

## 3 Contribution-Weighted GRPO

As motivated in Section [1](#S1 "1 Introduction ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization"), current search agents suffer from the credit assignment problem where sparse outcome rewards cannot distinguish between pivotal and redundant search rounds. To address this, we propose Contribution-Weighted Group Relative Policy Optimization (CW-GRPO). Unlike traditional process supervision that requires learning a fallible critic, CW-GRPO reframes process-level signals as dynamic scaling factors that redistribute trajectory-level advantages. The overall framework and its core mechanism of round-level credit assignment are presented in Figure [2](#S3.F2 "Figure 2 ‣ 3.1 Task Formulation ‣ 3 Contribution-Weighted GRPO ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization").

### 3.1 Task Formulation

We consider a search agent policy $\pi_{\theta}$ tasked with answering a question q. The agent interacts with an environment (search engine) through a trajectory $\tau$ of $T$ rounds:

|     |                                                                                                                      |     |     |
|-----|----------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $${\tau = \left( \left( s^{1},a^{1} \right),\left( s^{2},a^{2} \right),\ldots,\left( s^{T},a^{T} \right) \right)},$$ |     | (1) |

where for each round $t < T$, the action $a^{t}$ consists of a reasoning chain followed by an invocation of the search tool. The environment then returns retrieved documents to form the state $s^{t + 1}$. The last action $a^{T}$ is the final answer.

Training proceeds in groups. For each question, we sample a group of $G$ trajectories ${\{\tau_{i}\}}_{i = 1}^{G}$ under the current policy. Each trajectory $\tau_{i}$ receives a scalar outcome reward $R_{i}$ based on the exact match (EM) of its final answer. As in GRPO, these outcome rewards are only used for relative comparison within the group.

![Refer to caption](2604.14267v2/method.png)

Figure 2: CW-GRPO employs an LLM judge to assess both the retrieval utility and the reasoning correctness at each individual search round. Based on these two signals, it computes a contribution factor for every search round, which is subsequently applied to the original advantage obtained from group-relative comparisons, thereby producing the final round advantage. As a result, training signals from highly contributive rounds are amplified, while those from low-contribution rounds are attenuated.

### 3.2 Outcome-Level Advantage

Following the GRPO framework, we first establish a baseline for performance by comparing trajectories within the same group. This avoids the need for a value-function critic. For each trajectory $\tau_{i}$, we compute a normalized outcome advantage:

|     |                                                                                                                                                                     |     |     |
|-----|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $${A_{i}^{O} = \frac{R_{i} - \left. {\text{mean}\hspace{0pt}{\{ R_{i}\}}} \right|_{i = 1}^{G}}{\left. {\text{std}\hspace{0pt}{\{ R_{i}\}}} \right|_{i = 1}^{G}}}.$$ |     | (2) |

While $A_{i}^{O}$ effectively identifies which trajectories are better than others, it remains temporally coarse, assigning the same credit to every search round within a successful trajectory, regardless of whether a specific round was informative or distracting.

### 3.3 Round-Level Contribution Estimation

The effectiveness of CW-GRPO fundamentally depends on accurately identifying pivotal rounds within a search trajectory. Accordingly, we decompose the quality of each round into two orthogonal binary signals: retrieval utility and reasoning correctness. Crucially, we adopt a *conjunctive* formulation, under which a round is considered contributive only if it satisfies both criteria, namely retrieving novel, task-relevant evidence and maintaining logically consistent reasoning. This design reflects an inherent structural property of multi-round search: effective task solving requires not only the acquisition of useful information but also its correct interpretation in context. Retrieval without sound reasoning may lead to incorrect interpretation or misuse of useful evidence; conversely, correct reasoning without informative retrieval fails to make meaningful progress toward solving the task. The conjunctive gating mechanism thus serves as a conservative filter, isolating rounds whose contributions are causally aligned with task success, thereby providing a low-noise and more reliable signal for advantage reallocation.

#### 3.3.1 Signal Definition and Rubrics

To ensure the robustness of the LLM-derived signals, we employ a rubric-based assessment where an LLM judge is guided by a set of predefined criteria. For each search round $t < T_{i}$ in trajectory $\tau_{i}$, the values of the two signals are determined as follows:

- •
  Retrieval utility $u_{i}^{t} \in {\{ 0,1\}}$: This signal assesses the information gained from external sources. A round is assigned $u_{i}^{t} = 1$ only if the retrieved documents contain novel, task-relevant evidence that was not present in the context of previous rounds. This prevents the agent from being rewarded for redundant or circular retrieval queries.
- •
  Reasoning correctness $v_{i}^{t} \in {\{ 0,1\}}$: This signal estimates the internal consistency of the agent. A round is assigned $v_{i}^{t} = 1$ if the reasoning chain correctly interprets the current context and maintains a logical path toward the final answer. This ensures that the agent is not getting the right answer for the wrong reasons.

The conjunctive contribution signal is defined as the logical product $p_{i}^{t} = {u_{i}^{t} \cdot v_{i}^{t}}$. By enforcing a binary bottleneck, we apply a discrete gate to each search round: it either contributes a necessary building block to the solution or it does not.

#### 3.3.2 Judge Calibration and Reliability

To ensure that the LLM judge aligns with expert intuition, we conducted a rigorous calibration process. We manually annotated a subset of trajectories (comprising 97 distinct search rounds) to serve as a gold standard.

The rubrics were iteratively refined to minimize ambiguity. In our final setup, the LLM judge achieved a 95% consensus rate with human expert annotations on both retrieval utility and reasoning correctness. This high level of agreement provides a reliable foundation for the subsequent advantage redistribution, ensuring that policy gradients are directed by high-fidelity process signals. Additional calibration details are deferred to Appendix [B](#A2 "Appendix B LLM Judge Calibration Details ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization").

### 3.4 Adaptive Weighting Mechanism

We then convert these raw signals into a normalized contribution weight $c_{i}^{t}$. Importantly, we treat successful and failed trajectories differently, as a robustness-oriented design.

For successful trajectories ($R_{i} = 1$), rounds that introduce new task-relevant evidence and maintain logically consistent reasoning are typically associated with the final successful outcome. A temperature-controlled softmax is therefore adopted to emphasize high-contribution rounds:

|     |                                                                                                                                                                                                                             |     |     |
|-----|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $${{c_{i}^{t} = \frac{\exp\left( {\alpha\hspace{0pt}p_{i}^{t}} \right)}{\sum_{t^{\prime} = 1}^{T_{i} - 1}{\exp\left( {\alpha\hspace{0pt}p_{i}^{t^{\prime}}} \right)}}},{t < T_{i}},{{\text{~if~}\hspace{0pt}R_{i}} = 1}},$$ |     | (3) |

where $\alpha$ is a hyperparameter controlling the "sharpness" of the redistribution. A higher $\alpha$ forces the model to learn primarily from the most pivotal rounds.

For failed trajectories ($R_{i} = 0$), round-level attribution is substantially more ambiguous. Many intermediate rounds exhibit reasonable behavior, such as attempting to retrieve missing evidence or issuing follow-up queries for verification. However, these rounds may still fail to obtain useful information because the required knowledge is not covered by the corpus or cannot be retrieved due to limitations of the retriever. In such cases, the failure cannot be readily attributed to identifiable errors in the agent’s decisions at specific rounds. As a result, assigning differentiated weights based on round-level signals is unreliable and can introduce spurious supervision. A more detailed analysis of such failure patterns is provided in Appendix [A](#A1 "Appendix A Analysis of Failure Trajectories and Credit Assignment Ambiguity ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization"). To mitigate this issue, we assign a uniform contribution across all rounds:

|     |                                                                                           |     |     |
|-----|-------------------------------------------------------------------------------------------|-----|-----|
|     | $${{c_{i}^{t} = \frac{1}{T_{i} - 1}},{t < T_{i}},{{\text{~if~}\hspace{0pt}R_{i}} = 0}}.$$ |     | (4) |

This design preserves the stability of outcome-based learning while avoiding noisy round-level credit assignment under ambiguous attribution. Failed trajectories are still utilized through outcome-level comparison, and credit redistribution is applied only when attribution is reliable.

By construction, ${\sum_{t = 1}^{T_{i} - 1}c_{i}^{t}} = 1$.

### 3.5 Advantage Reallocation and Optimization

The core of CW-GRPO is the reallocated advantage $A_{i}^{t}$. For all search rounds $t < T_{i}$ of trajectory $\tau_{i}$, we scale the outcome advantage by the normalized contribution. And for the final answer round $t = T_{i}$, we directly use the outcome advantage:

|     |                                                                                                                                                    |     |     |
|-----|----------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $${{A_{i}^{t} = {A_{i}^{O} \cdot c_{i}^{t} \cdot \left( {T_{i} - 1} \right)}},{{\text{~if~}\hspace{0pt}t} < T_{i}};{A_{i}^{T_{i}} = A_{i}^{O}}}.$$ |     | (5) |

The factor $({T_{i} - 1})$ keeps the total learning signal magnitude of the trajectory unchanged, i.e.,

|     |                                                                                                                 |     |     |
|-----|-----------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $${{\frac{1}{\left( {T_{i} - 1} \right)}\hspace{0pt}{\sum\limits_{t = 1}^{T_{i} - 1}A_{i}^{t}}} = A_{i}^{O}}.$$ |     | (6) |

Finally, we optimize the policy using the clipped surrogate objective:

|     |                                                                                                                                                                                                        |     |     |
|-----|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $${{\mathcal{L}(\theta)} = {- {{\mathbb{E}}\left\lbrack {\min\left( {r\hspace{0pt}A},{\text{clip}\hspace{0pt}\left( r,{1 - \epsilon},{1 + \epsilon} \right)\hspace{0pt}A} \right)} \right\rbrack}}},$$ |     | (7) |

where $\epsilon$ is a hyper-parameter for clipping, $r = \frac{\pi_{\theta}\hspace{0pt}{(a\mid s)}}{\pi_{\theta_{o\hspace{0pt}l\hspace{0pt}d}}\hspace{0pt}{(a\mid s)}} = {\exp{({{\log\pi_{\theta}} - {\log\pi_{\theta_{o\hspace{0pt}l\hspace{0pt}d}}}})}}$ is the importance sampling ratio.

In summary, CW-GRPO seamlessly integrates process supervision into the GRPO framework and achieves effective credit assignment across iterative search rounds by reallocating trajectory-level advantages based on each round’s contribution, rather than estimating absolute intermediate rewards. This design preserves the training stability of group-relative optimization while ensuring the policy learns more effectively from the specific decisions that drive task success.

## 4 Setup

### 4.1 Datasets and Evaluation Metrics

We evaluate our method on two categories of knowledge-intensive tasks: (1) General Question Answering: Natural Questions (NQ) ([Kwiatkowski et al., 2019](#bib.bib14)), TriviaQA ([Joshi et al., 2017](#bib.bib12)), and PopQA ([Mallen et al., 2023](#bib.bib21)). (2) Multi-Hop Question Answering: HotpotQA ([Yang et al., 2018](#bib.bib41)), 2WikiMultiHopQA ([Ho et al., 2020](#bib.bib7)), Musique ([Trivedi et al., 2022](#bib.bib33)), and Bamboogle ([Press et al., 2023](#bib.bib23)). We merge the training sets of NQ and HotpotQA as the training data. To mitigate the impact of decoding variance, we use Avg@4 Exact Match (EM) as the evaluation metric, averaging the EM scores over four sampled responses per task.

Hard-Case Evaluation Set. In standard settings, models often bypass external search by leveraging internal parametric knowledge, which obscures their true agentic search proficiency. In light of this, we adopt a more challenging protocol using AgentGym-SearchQA-test, a 400-sample test set from AgentGym-RL ([Xi et al., 2025](#bib.bib40)). These samples are specifically filtered from cases where the Qwen2.5-72B-Instruct ([Team, 2024](#bib.bib30)) model failed, representing the "hardest" distribution for current LLMs. This setup shifts the focus from simple parametric recall to complex information-seeking and reasoning capabilities, explicitly emphasizing whether agents retrieve and utilize external evidence rather than relying on parametric knowledge.

Strict Retrieval Constraint. To further emphasize the model’s search agentic capabilities, we include a specific instruction in the system prompt: the model is prohibited from using any parametric knowledge beyond basic common sense.

### 4.2 Baselines

We compare our approach against two categories of search agents: (1) Outcome-Supervised Methods: Search-R1-PPO and Search-R1-GRPO ([Jin et al., 2025b](#bib.bib11)), which optimize the final answer via PPO and GRPO respectively. (2) Process-Supervised Methods: R3-RAG ([Li et al., 2025c](#bib.bib17)) and MT-PPO ([Wei et al., 2025](#bib.bib39)), which utilize explicit process rewards and PPO frameworks.

We also include results from state-of-the-art closed-source models (GPT-5.1 ([Singh et al., 2025](#bib.bib28)), Gemini-3-Pro-Preview ([Google, 2025](#bib.bib5)), Qwen3-Max ([Team, 2025a](#bib.bib31))) as strong upper-bound references, alongside powerful open-source models (DeepSeek-V3.2 ([DeepSeek-AI et al., 2025](#bib.bib3)), Qwen3-32B ([Team, 2025b](#bib.bib32))) for comparison.

Note on Comparison: Because of the uniquely challenging test set and the strict use of a no-parametric-knowledge prompt, the baseline performance reported in this paper differs from that reported in the original publications.

### 4.3 Implementation Details

We use Qwen3-8B and Qwen3-1.7B ([Team, 2025b](#bib.bib32)) as base models due to their tool-calling capabilities. Training is conducted using the veRL ([Sheng et al., 2024](#bib.bib27)) framework. The maximum context length is set to 9192 tokens, with up to 10 interaction rounds. We employ SGLang ([Zheng et al., 2024](#bib.bib47)) as the inference engine for rollout, setting both temperature and top_p to 1.0.

|                      |                     |                        |                         |
|----------------------|---------------------|------------------------|-------------------------|
| Parameter            |  GRPO / CW-GRPO     |  PPO-based (Actor)     |  PPO-based (Critic)     |
| Learning Rate        | $1 \times 10^{- 6}$ | $1 \times 10^{- 6}$    | $1 \times 10^{- 5}$     |
| Warmup Ratio         | 0.285               | 0.285                  | 0.015                   |
| Training Steps       | 200                 | 200                    | 200                     |
| Batch Size           | 32                  | 128                    | 128                     |
| Group Size           | 4                   | 1                      | 1                       |
| GAE $\gamma/\lambda$ | \-                  | 1.0/1.0                | 1.0/1.0                 |

Table 1: Detailed training hyperparameters of CW-GRPO and baselines.

Retrieval Infrastructure. We use the wiki-18-corpus dataset released by Search-R1 ([Jin et al., 2025b](#bib.bib11)), derived from the 2018 Wikipedia dump, as the knowledge source, and E5-base-v2 ([Wang et al., 2022](#bib.bib37)) as the retriever, with the number of retrieved documents $k$ set to 3.

Training Hyperparameters. For all RL-based experiments, we use a KL-divergence regularization coefficient $\beta = 0.001$ and a clipping ratio $\epsilon = 0.2$. Specifically, for our proposed CW-GRPO, we apply GPT-oss-120B ([Agarwal et al., 2025](#bib.bib1)) as the judge model and set $\alpha = \infty$. This configuration ensures that for trajectories resulting in task success, the learning signals during search iterations are exclusively concentrated on those rounds where the conjunctive contribution signal is $1$. Other specific parameters are detailed in Table [1](#S4.T1 "Table 1 ‣ 4.3 Implementation Details ‣ 4 Setup ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization"). The hyperparameter differences between GRPO-based and PPO-based methods stem from their distinct algorithmic characteristics (intra-group relative comparisons vs. independent trajectory optimization), and we ensure fairness by normalizing the total number of sampled trajectories per training step.

## 5 Experimental Results

|                        |            |               |            |              |            |              |                |         |
|------------------------|------------|---------------|------------|--------------|------------|--------------|----------------|---------|
| Method                 | General QA |               |            | Multi-Hop QA |            |              |                | Overall |
|                        | NQ^(†)     | TriviaQA^(\*) | PopQA^(\*) | HotpotQA^(†) | 2wiki^(\*) | Musique^(\*) | Bamboogle^(\*) |         |
| Proprietary Models     |            |               |            |              |            |              |                |         |
| GPT-5.1                | 31.0       | 60.0          | 38.5       | 36.0         | 43.5       | 13.8         | 39.0           | 34.44   |
| Gemini-3-Pro-Preview   | 31.0       | 66.0          | 32.5       | 42.0         | 38.5       | 14.0         | 42.0           | 35.00   |
| Qwen3-Max              | 31.5       | 62.5          | 30.5       | 39.5         | 49.0       | 18.5         | 42.5           | 36.56   |
| Open-sourced Models    |            |               |            |              |            |              |                |         |
| DeepSeek-V3.2-Thinking | 24.5       | 47.0          | 22.0       | 30.0         | 24.0       | 12.3         | 29.5           | 25.19   |
| Qwen3-32B              | 20.5       | 53.0          | 22.0       | 28.0         | 33.5       | 8.5          | 30.0           | 25.50   |
| Qwen3-1.7B             | 13.5       | 34.5          | 18.0       | 11.0         | 6.0        | 2.5          | 4.5            | 11.56   |
| Search-R1-PPO          | 19.5       | 50.5          | 25.0       | 25.5         | 24.0       | 5.0          | 14.0           | 21.06   |
| Search-R1-GRPO         | 18.0       | 45.5          | 25.0       | 27.0         | 22.5       | 6.8          | 16.5           | 21.00   |
| R3-RAG                 | 20.0       | 47.5          | 25.5       | 22.0         | 18.5       | 5.3          | 13.5           | 19.69   |
| MT-PPO                 | 22.5       | 49.0          | 25.0       | 24.0         | 31.5       | 6.0          | 13.5           | 22.19   |
| CW-GRPO                | 22.0       | 47.5          | 25.0       | 24.0         | 28.5       | 7.0          | 17.5           | 22.31   |
| Qwen3-8B               | 23.5       | 53.5          | 22.5       | 27.5         | 27.0       | 10.0         | 30.0           | 25.50   |
| Search-R1-PPO          | 29.5       | 57.0          | 27.5       | 33.5         | 36.0       | 12.3         | 33.5           | 30.19   |
| Search-R1-GRPO         | 33.5       | 57.0          | 26.0       | 33.5         | 32.5       | 12.5         | 31.5           | 29.88   |
| R3-RAG                 | 26.5       | 57.5          | 26.0       | 32.0         | 32.0       | 11.3         | 33.5           | 28.75   |
| MT-PPO                 | 25.5       | 56.5          | 26.0       | 32.0         | 37.0       | 12.5         | 31.5           | 29.19   |
| CW-GRPO                | 35.5       | 57.5          | 28.5       | 33.5         | 33.0       | 13.0         | 37.0           | 31.38   |

Table 2: Avg@4 Exact Match on seven subsets of AgentGym-SearchQA-test. † / \* indicate in-domain and out-of-domain datasets. CW-GRPO achieves the best performance among methods built on the same backbone.

### 5.1 Main Results

Table [2](#S5.T2 "Table 2 ‣ 5 Experimental Results ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization") presents the main experimental results on hard knowledge-intensive QA benchmarks under no-parametric-knowledge constraints.

Overall Performance. Our experimental results demonstrate the robust superiority of CW-GRPO, which achieves state-of-the-art performance across both model scales, outperforming all outcome- and process-supervised baselines on the identical backbone. On Qwen3-8B, CW-GRPO achieves an overall score of 31.38, representing a $5.0\%$ relative improvement over Search-R1-GRPO (29.88). On Qwen3-1.7B, CW-GRPO improves the overall performance from 21.00 to 22.31, corresponding to a $6.3\%$ relative gain. These results indicate that CW-GRPO scales favorably across model sizes and is particularly effective in low-capacity regimes, where efficient search credit assignment is critical.

Comparison with Open- and Closed-Source Models. With Qwen3-8B as the backbone, CW-GRPO surpasses all evaluated open-source models, including DeepSeek-V3.2-Thinking and Qwen3-32B, despite operating under a stricter evaluation setting. However, a clear performance gap remains between CW-GRPO and large closed-source models such as GPT-5.1, Gemini-3-Pro-Preview, and Qwen3-Max, suggesting that stronger base models and proprietary training data still provide advantages under this challenging hard-case distribution.

General QA vs. Multi-Hop QA. CW-GRPO demonstrates consistent improvements on both General QA and Multi-Hop QA tasks compared to outcome-supervised and process-supervised baselines. On Multi-Hop QA, CW-GRPO yields the most pronounced gains. On both Qwen3-1.7B and Qwen3-8B, it improves performance on 2WikiMultiHopQA, Musique, and Bamboogle simultaneously, indicating stronger long-horizon reasoning and evidence aggregation. On General QA, CW-GRPO remains competitive across datasets. While it achieves the best overall General QA performance on Qwen3-8B, its improvement on Qwen3-1.7B is smaller than that of MT-PPO. This suggests that for simpler single-hop questions, dense process supervision can still be effective for very small models, whereas CW-GRPO shows clearer advantages as reasoning depth increases.

Summary. Overall, these results demonstrate that CW-GRPO provides a robust and scalable improvement over existing outcome- and process-supervised search agents, particularly for multi-hop reasoning under strict retrieval constraints. The consistent gains across model sizes highlight the effectiveness of contribution-weighted optimization in guiding search behavior, even in extremely challenging evaluation settings.

### 5.2 Sharpness of Advantage Reallocation

Based on Qwen3-8B, we analyze the effect of the sharpness parameter $\alpha$, which controls how outcome advantages are redistributed across search rounds based on their estimated contributions. Setting $\alpha = 0$ yields uniform weighting over the search rounds and reduces the method to standard GRPO, whereas $\alpha = \infty$ corresponds to CW-GRPO, where the advantage is fully concentrated on rounds with both retrieval utility and correct reasoning.

As shown in Table [3](#S5.T3 "Table 3 ‣ 5.3 Supervision Decomposition ‣ 5 Experimental Results ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization"), increasing $\alpha$ generally leads to improved overall performance, with the best overall result achieved at $\alpha = \infty$. This trend suggests that, in successful search trajectories, the contribution to task success is highly uneven across rounds. Rather than accumulating gradually, effective progress is driven by high-quality search rounds that exhibit retrieval utility and correct reasoning. For search agent tasks, effective credit assignment requires acknowledging this highly concentrated contribution structure.

### 5.3 Supervision Decomposition

We ablate the two supervision signals in CW-GRPO by separately removing retrieval utility or reasoning correctness supervision while keeping all other components unchanged.

According to Table [4](#S5.T4 "Table 4 ‣ 5.3 Supervision Decomposition ‣ 5 Experimental Results ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization"), removing either signal consistently degrades performance across both single-hop and multi-hop QA tasks, suggesting that neither signal alone is sufficient for reliable credit assignment during search.

Without retrieval utility supervision, rounds with coherent but uninformative reasoning can receive positive credit. Without reasoning correctness supervision, rounds can be assigned positive contribution weights for retrieving relevant documents even when they are incorrectly interpreted, weakening the link between evidence acquisition and correct reasoning. In either setting, contribution weights may be assigned to rounds that do not make a substantive contribution to task completion, introducing noise into advantage reallocation and harming overall performance.

These results highlight the necessity of joint supervision: effective search requires both acquiring novel information and correctly reasoning over it.

|           |            |          |       |              |       |         |           |         |
|-----------|------------|----------|-------|--------------|-------|---------|-----------|---------|
|  $\alpha$ | General QA |          |       | Multi-Hop QA |       |         |           | Overall |
|           | NQ         | TriviaQA | PopQA | HotpotQA     | 2wiki | Musique | Bamboogle |         |
| 0         | 33.5       | 57.0     | 26.0  | 33.5         | 32.5  | 12.5    | 31.5      | 29.88   |
| 1         | 27.0       | 58.0     | 28.0  | 32.5         | 35.0  | 12.8    | 31.5      | 29.69   |
| 3         | 33.0       | 58.5     | 31.0  | 29.5         | 36.0  | 13.0    | 31.0      | 30.63   |
| 5         | 27.0       | 58.5     | 27.0  | 35.0         | 39.0  | 12.0    | 33.5      | 30.50   |
| $\infty$  | 35.5       | 57.5     | 28.5  | 33.5         | 33.0  | 13.0    | 37.0      | 31.38   |

Table 3: Effect of the sharpness parameter $\alpha$ on search agent performance. Larger $\alpha$ value generally yields better overall accuracy, indicating that concentrating learning signals on high-contribution search rounds is beneficial.

|              |            |          |       |              |       |         |           |         |
|--------------|------------|----------|-------|--------------|-------|---------|-----------|---------|
| Method       | General QA |          |       | Multi-Hop QA |       |         |           | Overall |
|              | NQ         | TriviaQA | PopQA | HotpotQA     | 2wiki | Musique | Bamboogle |         |
| CW-GRPO      | 35.5       | 57.5     | 28.5  | 33.5         | 33.0  | 13.0    | 37.0      | 31.38   |
| wo-retrieval | 27.0       | 53.5     | 26.0  | 31.0         | 37.5  | 12.0    | 34.5      | 29.19   |
| wo-reasoning | 23.5       | 55.5     | 31.0  | 34.0         | 28.5  | 12.3    | 31.5      | 28.56   |

Table 4: Ablation on contribution supervision in CW-GRPO. Removing either retrieval utility or reasoning correctness supervision degrades performance, showing both are necessary for effective credit assignment.

### 5.4 Training Dynamics

As shown in Figure [3](#S5.F3 "Figure 3 ‣ 5.5 Case Study ‣ 5 Experimental Results ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization"), the optimization remains stable across training, with no signs of collapse. The Exact Match score steadily improves, accompanied by consistent upward trends in both retrieval utility and reasoning correctness, indicating progressive improvement in the agent’s search behavior. These results show that CW-GRPO achieves stable optimization while improving both final accuracy and the quality of the search process.

We further analyze the effect of the conjunctive gate mechanism during training. Among all search rounds in successful trajectories, approximately 13.84% (2.2k out of 15.8k) are assigned zero contribution, indicating that the gate meaningfully reshapes the distribution of learning signals rather than acting as a near-identity transformation.

### 5.5 Case Study

Figure [4](#S5.F4 "Figure 4 ‣ 5.5 Case Study ‣ 5 Experimental Results ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization") compares the search trajectories of Qwen3-8B before and after CW-GRPO training on a factual question regarding John I. Jenkins’s tenure start. The untrained model issues only a single query and fails to distinguish between the election year and the actual commencement of his term, leading to an incorrect answer based on this temporal confusion.

In contrast, the CW-GRPO-trained model adopts a qualitatively different strategy by issuing multiple parallel queries in the first round. This expanded search coverage allows the agent to recall a broader set of documents, including explicit evidence that Jenkins’s term began in 2005. This case illustrates that CW-GRPO not only improves retrieval utility through parallelization but also strengthens the agent’s resistance to distracting evidence. By learning to prioritize direct answer-bearing evidence over superficially relevant but misleading signals, the model achieves more robust and grounded search-based decision making.

![Refer to caption](2604.14267v2/figures/training_dynamics.png)

Figure 3: Training curves of CW-GRPO on Qwen3-8B. We report the exponential moving averages of Exact Match, retrieval utility, and reasoning correctness over training steps.

![Refer to caption](2604.14267v2/case_study.png)

Figure 4: Case study of CW-GRPO on Qwen3-8B.

## 6 Discussion: Generalization Across Tasks and Models

CW-GRPO is motivated by the general principle of redistributing outcome-derived advantages according to round-level contribution estimates. This principle is broadly applicable beyond the specific experimental settings considered in this work.

Task generalization. CW-GRPO can be applied to multi-round agentic tasks where the contributions of intermediate rounds can be reasonably estimated. In long-horizon decision-making environments(e.g., Webshop ([Yao et al., 2022](#bib.bib42))), individual actions should correspond to incremental progress toward latent subgoals. This enables a judge to assess state improvements at each round and facilitates round-level credit assignment.

The framework also extends to single-round but structurally decomposable reasoning tasks. In settings such as mathematical reasoning(e.g., MATH ([Hendrycks et al., 2021](#bib.bib6))), model outputs typically consist of multi-step derivations. When a trajectory fails, the error can often be localized to specific steps; these steps can then be assigned higher responsibility for failure, enabling a CW-GRPO variant based on step-level attribution.

However, CW-GRPO is less suitable for tasks where process contribution is ill-defined or inherently unstable. This includes highly subjective generation tasks (e.g., open-ended creative writing) and perceptual generation tasks (e.g., image synthesis), where holistic judgments dominate and assigning reliable credit to intermediate steps via low-variance signals is challenging.

Model generalization. CW-GRPO is model-agnostic and does not rely on a specific backbone architecture. Nevertheless, stronger base models tend to be more sensitive to the accuracy of round-level supervision, placing higher demands on the quality of the judge or rubric design, which may limit the practical gains of the method.

## 7 Conclusion

In this work, we propose CW-GRPO, which reallocates outcome advantages according to round-level contribution rather than explicit process rewards to tackle the credit assignment challenge in training LLM-based search agents. CW-GRPO retains GRPO’s stability while enabling fine-grained credit assignment along search rounds. Our evaluations show that CW-GRPO consistently outperforms baselines, and task success is closely associated with the high-quality rounds, highlighting the importance of modeling contribution concentration in search trajectories. Overall, CW-GRPO offers a simple and effective way to incorporate process-level insights into outcome-supervised training for scalable agentic systems.

## Limitations

Despite the advances demonstrated by CW-GRPO in alleviating credit assignment under outcome supervision, several limitations remain.

First, CW-GRPO reallocates advantages only for successful trajectories. For failed trajectories, it does not perform fine-grained credit assignment, as attributing task failure to specific search rounds remains challenging. Consequently, CW-GRPO lacks explicit modeling of which intermediate decisions contribute to failure, leaving failure cases underutilized for process-aware learning.

Second, CW-GRPO adopts a conjunctive gating mechanism for modeling round-level contributions, which improves robustness to judging noise but limits the expressiveness of contribution representation. In addition, the framework operates at the round level and does not naturally extend to token-level supervision, making finer-grained credit assignment beyond rounds hard to incorporate.

Finally, CW-GRPO relies on an external LLM judge for contribution estimation. While we find the associated computational cost to be manageable in our setting (see Appendix [C](#A3 "Appendix C Computational Cost of LLM Judge ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization")), this design still introduces additional inference cost and dependency on judge quality. Exploring lighter-weight supervision signals (e.g., heuristic judges) may further improve scalability, especially in more resource-constrained or latency-sensitive scenarios.

## References

- Agarwal et al. (2025) OpenAI: Sandhini Agarwal, Lama Ahmad, Jason Ai, Sam Altman, Andy Applebaum, Edwin Arbus, Rahul K. Arora, Yu Bai, Bowen Baker, Haiming Bao, Boaz Barak, Ally Bennett, Tyler Bertao, Nivedita Brett, Eugene Brevdo, Greg Brockman, Sebastien Bubeck, Che Chang, Kai Chen, Mark Chen, Enoch Cheung, Aidan Clark, Dan Cook, Marat Dukhan, Casey Dvorak, Kevin Fives, Vlad Fomenko, Timur Garipov, Kristian Georgiev, Mia Glaese, Tarun Gogineni, Adam Goucher, Lukas Gross, Katia Gil Guzman, John Hallman, Jackie Hehir, Johannes Heidecke, Alec Helyar, Haitang Hu, Romain Huet, Jacob Huh, Saachi Jain, Zach Johnson, Chris Koch, Irina Kofman, Dominik Kundel, Jason Kwon, Volodymyr Kyrylov, Elaine Ya Le, Guillaume Leclerc, James Park Lennon, Scott Lessans, Mario Lezcano-Casado, Yuanzhi Li, Zhuohan Li, Ji Lin, Jordan Liss, Lily Liu, Jiancheng Liu, Kevin Lu, Chris Lu, Zoran Martinovic, Lindsay McCallum, Josh McGrath, Scott McKinney, Aidan McLaughlin, Song Mei, Steve Mostovoy, Tong Mu, Gideon Myles, Alexander Neitz, Alex Nichol, Jakub Pachocki, Alex Paino, Dana Palmie, Ashley Pantuliano, Giambattista Parascandolo, Jongsoo Park, Leher Pathak, Carolina Paz, Ludovic Peran, Dmitry Pimenov, Michelle Pokrass, Elizabeth Proehl, Huida Qiu, Gaby Raila, Filippo Raso, Hongyu Ren, Kimmy Richardson, David Robinson, Bob Rotsted, Hadi Salman, Suvansh Sanjeev, Max Schwarzer, D. Sculley, Harshit Sikchi, Kendal Simon, Karan Singhal, Yang Song, Dane Stuckey, Zhiqing Sun, Philippe Tillet, Sam Toizer, Foivos Tsimpourlas, Nikhil Vyas, Eric Wallace, Xin Wang, Miles Wang, Olivia Watkins, Kevin Weil, Amy Wendling, Kevin Whinnery, Cedric Whitney, Hannah Wong, Lin Yang, Yu Yang, Michihiro Yasunaga, Kristen Ying, Wojciech Zaremba, Wenting Zhan, Cyril Zhang, Brian Zhang, Eddie Zhang, and Shengjia Zhao. gpt-oss-120b & gpt-oss-20b model card, 2025. URL [https://arxiv.org/abs/2508.10925](https://arxiv.org/abs/2508.10925).
- Asai et al. (2024) Akari Asai, Zeqiu Wu, Yizhong Wang, Avirup Sil, and Hannaneh Hajishirzi. Self-RAG: Learning to retrieve, generate, and critique through self-reflection. In *The Twelfth International Conference on Learning Representations*, 2024. URL [https://openreview.net/forum?id=hSyW5go0v8](https://openreview.net/forum?id=hSyW5go0v8).
- DeepSeek-AI et al. (2025) DeepSeek-AI, Aixin Liu, Aoxue Mei, Bangcai Lin, Bing Xue, Bingxuan Wang, Bingzheng Xu, Bochao Wu, Bowei Zhang, Chaofan Lin, Chen Dong, Chengda Lu, Chenggang Zhao, Chengqi Deng, Chenhao Xu, Chong Ruan, Damai Dai, Daya Guo, Dejian Yang, Deli Chen, Erhang Li, Fangqi Zhou, Fangyun Lin, Fucong Dai, Guangbo Hao, Guanting Chen, Guowei Li, H. Zhang, Hanwei Xu, Hao Li, Haofen Liang, Haoran Wei, Haowei Zhang, Haowen Luo, Haozhe Ji, Honghui Ding, Hongxuan Tang, Huanqi Cao, Huazuo Gao, Hui Qu, Hui Zeng, Jialiang Huang, Jiashi Li, Jiaxin Xu, Jiewen Hu, Jingchang Chen, Jingting Xiang, Jingyang Yuan, Jingyuan Cheng, Jinhua Zhu, Jun Ran, Junguang Jiang, Junjie Qiu, Junlong Li, Junxiao Song, Kai Dong, Kaige Gao, Kang Guan, Kexin Huang, Kexing Zhou, Kezhao Huang, Kuai Yu, Lean Wang, Lecong Zhang, Lei Wang, Liang Zhao, Liangsheng Yin, Lihua Guo, Lingxiao Luo, Linwang Ma, Litong Wang, Liyue Zhang, M. S. Di, M. Y Xu, Mingchuan Zhang, Minghua Zhang, Minghui Tang, Mingxu Zhou, Panpan Huang, Peixin Cong, Peiyi Wang, Qiancheng Wang, Qihao Zhu, Qingyang Li, Qinyu Chen, Qiushi Du, Ruiling Xu, Ruiqi Ge, Ruisong Zhang, Ruizhe Pan, Runji Wang, Runqiu Yin, Runxin Xu, Ruomeng Shen, Ruoyu Zhang, S. H. Liu, Shanghao Lu, Shangyan Zhou, Shanhuang Chen, Shaofei Cai, Shaoyuan Chen, Shengding Hu, Shengyu Liu, Shiqiang Hu, Shirong Ma, Shiyu Wang, Shuiping Yu, Shunfeng Zhou, Shuting Pan, Songyang Zhou, Tao Ni, Tao Yun, Tian Pei, Tian Ye, Tianyuan Yue, Wangding Zeng, Wen Liu, Wenfeng Liang, Wenjie Pang, Wenjing Luo, Wenjun Gao, Wentao Zhang, Xi Gao, Xiangwen Wang, Xiao Bi, Xiaodong Liu, Xiaohan Wang, Xiaokang Chen, Xiaokang Zhang, Xiaotao Nie, Xin Cheng, Xin Liu, Xin Xie, Xingchao Liu, Xingkai Yu, Xingyou Li, Xinyu Yang, Xinyuan Li, Xu Chen, Xuecheng Su, Xuehai Pan, Xuheng Lin, Xuwei Fu, Y. Q. Wang, Yang Zhang, Yanhong Xu, Yanru Ma, Yao Li, Yao Li, Yao Zhao, Yaofeng Sun, Yaohui Wang, Yi Qian, Yi Yu, Yichao Zhang, Yifan Ding, Yifan Shi, Yiliang Xiong, Ying He, Ying Zhou, Yinmin Zhong, Yishi Piao, Yisong Wang, Yixiao Chen, Yixuan Tan, Yixuan Wei, Yiyang Ma, Yiyuan Liu, Yonglun Yang, Yongqiang Guo, Yongtong Wu, Yu Wu, Yuan Cheng, Yuan Ou, Yuanfan Xu, Yuduan Wang, Yue Gong, Yuhan Wu, Yuheng Zou, Yukun Li, Yunfan Xiong, Yuxiang Luo, Yuxiang You, Yuxuan Liu, Yuyang Zhou, Z. F. Wu, Z. Z. Ren, Zehua Zhao, Zehui Ren, Zhangli Sha, Zhe Fu, Zhean Xu, Zhenda Xie, Zhengyan Zhang, Zhewen Hao, Zhibin Gou, Zhicheng Ma, Zhigang Yan, Zhihong Shao, Zhixian Huang, Zhiyu Wu, Zhuoshu Li, Zhuping Zhang, Zian Xu, Zihao Wang, Zihui Gu, Zijia Zhu, Zilin Li, Zipeng Zhang, Ziwei Xie, Ziyi Gao, Zizheng Pan, Zongqing Yao, Bei Feng, Hui Li, J. L. Cai, Jiaqi Ni, Lei Xu, Meng Li, Ning Tian, R. J. Chen, R. L. Jin, S. S. Li, Shuang Zhou, Tianyu Sun, X. Q. Li, Xiangyue Jin, Xiaojin Shen, Xiaosha Chen, Xinnan Song, Xinyi Zhou, Y. X. Zhu, Yanping Huang, Yaohui Li, Yi Zheng, Yuchen Zhu, Yunxian Ma, Zhen Huang, Zhipeng Xu, Zhongyu Zhang, Dongjie Ji, Jian Liang, Jianzhong Guo, Jin Chen, Leyi Xia, Miaojun Wang, Mingming Li, Peng Zhang, Ruyi Chen, Shangmian Sun, Shaoqing Wu, Shengfeng Ye, T. Wang, W. L. Xiao, Wei An, Xianzu Wang, Xiaowen Sun, Xiaoxiang Wang, Ying Tang, Yukun Zha, Zekai Zhang, Zhe Ju, Zhen Zhang, and Zihua Qu. Deepseek-v3.2: Pushing the frontier of open large language models, 2025. URL [https://arxiv.org/abs/2512.02556](https://arxiv.org/abs/2512.02556).
- Glass et al. (2022) Michael Glass, Gaetano Rossiello, Md Faisal Mahbub Chowdhury, Ankita Naik, Pengshan Cai, and Alfio Gliozzo. Re2g: Retrieve, rerank, generate. In *Proceedings of the 2022 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies*, pages 2701–2715, 2022.
- Google (2025) Google. Gemini 3 pro model card. Technical report, Google DeepMind, 11 2025. URL [https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-Pro-Model-Card.pdf](https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-Pro-Model-Card.pdf). Accessed: 2026-01-06.
- Hendrycks et al. (2021) Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, and Jacob Steinhardt. Measuring mathematical problem solving with the math dataset, 2021. URL [https://arxiv.org/abs/2103.03874](https://arxiv.org/abs/2103.03874).
- Ho et al. (2020) Xanh Ho, Anh-Khoa Duong Nguyen, Saku Sugawara, and Akiko Aizawa. Constructing a multi-hop qa dataset for comprehensive evaluation of reasoning steps, 2020. URL [https://arxiv.org/abs/2011.01060](https://arxiv.org/abs/2011.01060).
- Huang et al. (2025) Hui Huang, Xingyuan Bu, Hongli Zhou, Yingqi Qu, Jing Liu, Muyun Yang, Bing Xu, and Tiejun Zhao. An empirical study of LLM-as-a-judge for LLM evaluation: Fine-tuned judge model is not a general substitute for GPT-4. In Wanxiang Che, Joyce Nabende, Ekaterina Shutova, and Mohammad Taher Pilehvar, editors, *Findings of the Association for Computational Linguistics: ACL 2025*, pages 5880–5895, Vienna, Austria, July 2025. Association for Computational Linguistics. ISBN 979-8-89176-256-5. [10.18653/v1/2025.findings-acl.306](https://doi.org/10.18653/v1/2025.findings-acl.306). URL [https://aclanthology.org/2025.findings-acl.306/](https://aclanthology.org/2025.findings-acl.306/).
- Jiang et al. (2023) Zhengbao Jiang, Frank Xu, Luyu Gao, Zhiqing Sun, Qian Liu, Jane Dwivedi-Yu, Yiming Yang, Jamie Callan, and Graham Neubig. Active retrieval augmented generation. In Houda Bouamor, Juan Pino, and Kalika Bali, editors, *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing*, pages 7969–7992, Singapore, December 2023. Association for Computational Linguistics. [10.18653/v1/2023.emnlp-main.495](https://doi.org/10.18653/v1/2023.emnlp-main.495). URL [https://aclanthology.org/2023.emnlp-main.495/](https://aclanthology.org/2023.emnlp-main.495/).
- Jin et al. (2025a) Bowen Jin, Jinsung Yoon, Priyanka Kargupta, Sercan O. Arik, and Jiawei Han. An empirical study on reinforcement learning for reasoning-search interleaved llm agents, 2025a. URL [https://arxiv.org/abs/2505.15117](https://arxiv.org/abs/2505.15117).
- Jin et al. (2025b) Bowen Jin, Hansi Zeng, Zhenrui Yue, Jinsung Yoon, Sercan Arik, Dong Wang, Hamed Zamani, and Jiawei Han. Search-r1: Training llms to reason and leverage search engines with reinforcement learning, 2025b. URL [https://arxiv.org/abs/2503.09516](https://arxiv.org/abs/2503.09516).
- Joshi et al. (2017) Mandar Joshi, Eunsol Choi, Daniel S. Weld, and Luke Zettlemoyer. Triviaqa: A large scale distantly supervised challenge dataset for reading comprehension, 2017. URL [https://arxiv.org/abs/1705.03551](https://arxiv.org/abs/1705.03551).
- Kazemnejad et al. (2025) Amirhossein Kazemnejad, Milad Aghajohari, Eva Portelance, Alessandro Sordoni, Siva Reddy, Aaron Courville, and Nicolas Le Roux. Vineppo: Refining credit assignment in rl training of llms, 2025. URL [https://arxiv.org/abs/2410.01679](https://arxiv.org/abs/2410.01679).
- Kwiatkowski et al. (2019) Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur Parikh, Chris Alberti, Danielle Epstein, Illia Polosukhin, Jacob Devlin, Kenton Lee, Kristina Toutanova, Llion Jones, Matthew Kelcey, Ming-Wei Chang, Andrew M. Dai, Jakob Uszkoreit, Quoc Le, and Slav Petrov. Natural questions: A benchmark for question answering research. *Transactions of the Association for Computational Linguistics*, 7:452–466, 2019. [10.1162/tacl_a_00276](https://doi.org/10.1162/tacl_a_00276). URL [https://aclanthology.org/Q19-1026/](https://aclanthology.org/Q19-1026/).
- Li et al. (2025a) Xiaoxi Li, Guanting Dong, Jiajie Jin, Yuyao Zhang, Yujia Zhou, Yutao Zhu, Peitian Zhang, and Zhicheng Dou. Search-o1: Agentic search-enhanced large reasoning models, 2025a. URL [https://arxiv.org/abs/2501.05366](https://arxiv.org/abs/2501.05366).
- Li et al. (2025b) Xiaoxi Li, Jiajie Jin, Yujia Zhou, Yuyao Zhang, Peitian Zhang, Yutao Zhu, and Zhicheng Dou. From matching to generation: A survey on generative information retrieval. *ACM Transactions on Information Systems*, 43(3):1–62, 2025b.
- Li et al. (2025c) Yuan Li, Qi Luo, Xiaonan Li, Bufan Li, Qinyuan Cheng, Bo Wang, Yining Zheng, Yuxin Wang, Zhangyue Yin, and Xipeng Qiu. R3-rag: Learning step-by-step reasoning and retrieval for llms via reinforcement learning. *arXiv preprint arXiv:2505.23794*, 2025c.
- Lightman et al. (2023) Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri Edwards, Bowen Baker, Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever, and Karl Cobbe. Let’s verify step by step, 2023. URL [https://arxiv.org/abs/2305.20050](https://arxiv.org/abs/2305.20050).
- Lin et al. (2026) Jiahang Lin, Kai Hu, Binghai Wang, Yuhao Zhou, Zhiheng Xi, Honglin Guo, Shichun Liu, Junzhe Wang, Shihan Dou, Enyu Zhou, Hang Yan, Zhenhua Han, Tao Gui, Qi Zhang, and Xuanjing Huang. Mm-doc-r1: Training agents for long document visual question answering through multi-turn reinforcement learning, 2026. URL [https://arxiv.org/abs/2604.13579](https://arxiv.org/abs/2604.13579).
- Liu et al. (2024) Jiacai Liu, Chaojie Wang, Chris Yuhao Liu, Liang Zeng, Rui Yan, Yiwen Sun, Yang Liu, and Yahui Zhou. Improving multi-step reasoning abilities of large language models with direct advantage policy optimization, 2024. URL [https://arxiv.org/abs/2412.18279](https://arxiv.org/abs/2412.18279).
- Mallen et al. (2023) Alex Mallen, Akari Asai, Victor Zhong, Rajarshi Das, Daniel Khashabi, and Hannaneh Hajishirzi. When not to trust language models: Investigating effectiveness of parametric and non-parametric memories, 2023. URL [https://arxiv.org/abs/2212.10511](https://arxiv.org/abs/2212.10511).
- Nakano et al. (2022) Reiichiro Nakano, Jacob Hilton, Suchir Balaji, Jeff Wu, Long Ouyang, Christina Kim, Christopher Hesse, Shantanu Jain, Vineet Kosaraju, William Saunders, Xu Jiang, Karl Cobbe, Tyna Eloundou, Gretchen Krueger, Kevin Button, Matthew Knight, Benjamin Chess, and John Schulman. Webgpt: Browser-assisted question-answering with human feedback, 2022. URL [https://arxiv.org/abs/2112.09332](https://arxiv.org/abs/2112.09332).
- Press et al. (2023) Ofir Press, Muru Zhang, Sewon Min, Ludwig Schmidt, Noah A Smith, and Mike Lewis. Measuring and narrowing the compositionality gap in language models. In *Findings of the Association for Computational Linguistics: EMNLP 2023*, pages 5687–5711, 2023.
- Sawarkar et al. (2024) Kunal Sawarkar, Abhilasha Mangal, and Shivam Raj Solanki. Blended rag: Improving rag (retriever-augmented generation) accuracy with semantic search and hybrid query-based retrievers. In *2024 IEEE 7th international conference on multimedia information processing and retrieval (MIPR)*, pages 155–161. IEEE, 2024.
- Schulman et al. (2017) John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms, 2017. URL [https://arxiv.org/abs/1707.06347](https://arxiv.org/abs/1707.06347).
- Shao et al. (2024) Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, Y. K. Li, Y. Wu, and Daya Guo. Deepseekmath: Pushing the limits of mathematical reasoning in open language models, 2024. URL [https://arxiv.org/abs/2402.03300](https://arxiv.org/abs/2402.03300).
- Sheng et al. (2024) Guangming Sheng, Chi Zhang, Zilingfeng Ye, Xibin Wu, Wang Zhang, Ru Zhang, Yanghua Peng, Haibin Lin, and Chuan Wu. Hybridflow: A flexible and efficient rlhf framework. *arXiv preprint arXiv: 2409.19256*, 2024.
- Singh et al. (2025) Aaditya Singh, Adam Fry, Adam Perelman, Adam Tart, Adi Ganesh, Ahmed El-Kishky, Aidan McLaughlin, Aiden Low, AJ Ostrow, Akhila Ananthram, Akshay Nathan, Alan Luo, Alec Helyar, Aleksander Madry, Aleksandr Efremov, Aleksandra Spyra, Alex Baker-Whitcomb, Alex Beutel, Alex Karpenko, Alex Makelov, Alex Neitz, Alex Wei, Alexandra Barr, Alexandre Kirchmeyer, Alexey Ivanov, Alexi Christakis, Alistair Gillespie, Allison Tam, Ally Bennett, Alvin Wan, Alyssa Huang, Amy McDonald Sandjideh, Amy Yang, Ananya Kumar, Andre Saraiva, Andrea Vallone, Andrei Gheorghe, Andres Garcia Garcia, Andrew Braunstein, Andrew Liu, Andrew Schmidt, Andrey Mereskin, Andrey Mishchenko, Andy Applebaum, Andy Rogerson, Ann Rajan, Annie Wei, Anoop Kotha, Anubha Srivastava, Anushree Agrawal, Arun Vijayvergiya, Ashley Tyra, Ashvin Nair, Avi Nayak, Ben Eggers, Bessie Ji, Beth Hoover, Bill Chen, Blair Chen, Boaz Barak, Borys Minaiev, Botao Hao, Bowen Baker, Brad Lightcap, Brandon McKinzie, Brandon Wang, Brendan Quinn, Brian Fioca, Brian Hsu, Brian Yang, Brian Yu, Brian Zhang, Brittany Brenner, Callie Riggins Zetino, Cameron Raymond, Camillo Lugaresi, Carolina Paz, Cary Hudson, Cedric Whitney, Chak Li, Charles Chen, Charlotte Cole, Chelsea Voss, Chen Ding, Chen Shen, Chengdu Huang, Chris Colby, Chris Hallacy, Chris Koch, Chris Lu, Christina Kaplan, Christina Kim, CJ Minott-Henriques, Cliff Frey, Cody Yu, Coley Czarnecki, Colin Reid, Colin Wei, Cory Decareaux, Cristina Scheau, Cyril Zhang, Cyrus Forbes, Da Tang, Dakota Goldberg, Dan Roberts, Dana Palmie, Daniel Kappler, Daniel Levine, Daniel Wright, Dave Leo, David Lin, David Robinson, Declan Grabb, Derek Chen, Derek Lim, Derek Salama, Dibya Bhattacharjee, Dimitris Tsipras, Dinghua Li, Dingli Yu, DJ Strouse, Drew Williams, Dylan Hunn, Ed Bayes, Edwin Arbus, Ekin Akyurek, Elaine Ya Le, Elana Widmann, Eli Yani, Elizabeth Proehl, Enis Sert, Enoch Cheung, Eri Schwartz, Eric Han, Eric Jiang, Eric Mitchell, Eric Sigler, Eric Wallace, Erik Ritter, Erin Kavanaugh, Evan Mays, Evgenii Nikishin, Fangyuan Li, Felipe Petroski Such, Filipe de Avila Belbute Peres, Filippo Raso, Florent Bekerman, Foivos Tsimpourlas, Fotis Chantzis, Francis Song, Francis Zhang, Gaby Raila, Garrett McGrath, Gary Briggs, Gary Yang, Giambattista Parascandolo, Gildas Chabot, Grace Kim, Grace Zhao, Gregory Valiant, Guillaume Leclerc, Hadi Salman, Hanson Wang, Hao Sheng, Haoming Jiang, Haoyu Wang, Haozhun Jin, Harshit Sikchi, Heather Schmidt, Henry Aspegren, Honglin Chen, Huida Qiu, Hunter Lightman, Ian Covert, Ian Kivlichan, Ian Silber, Ian Sohl, Ibrahim Hammoud, Ignasi Clavera, Ikai Lan, Ilge Akkaya, Ilya Kostrikov, Irina Kofman, Isak Etinger, Ishaan Singal, Jackie Hehir, Jacob Huh, Jacqueline Pan, Jake Wilczynski, Jakub Pachocki, James Lee, James Quinn, Jamie Kiros, Janvi Kalra, Jasmyn Samaroo, Jason Wang, Jason Wolfe, Jay Chen, Jay Wang, Jean Harb, Jeffrey Han, Jeffrey Wang, Jennifer Zhao, Jeremy Chen, Jerene Yang, Jerry Tworek, Jesse Chand, Jessica Landon, Jessica Liang, Ji Lin, Jiancheng Liu, Jianfeng Wang, Jie Tang, Jihan Yin, Joanne Jang, Joel Morris, Joey Flynn, Johannes Ferstad, Johannes Heidecke, John Fishbein, John Hallman, Jonah Grant, Jonathan Chien, Jonathan Gordon, Jongsoo Park, Jordan Liss, Jos Kraaijeveld, Joseph Guay, Joseph Mo, Josh Lawson, Josh McGrath, Joshua Vendrow, Joy Jiao, Julian Lee, Julie Steele, Julie Wang, Junhua Mao, Kai Chen, Kai Hayashi, Kai Xiao, Kamyar Salahi, Kan Wu, Karan Sekhri, Karan Sharma, Karan Singhal, Karen Li, Kenny Nguyen, Keren Gu-Lemberg, Kevin King, Kevin Liu, Kevin Stone, Kevin Yu, Kristen Ying, Kristian Georgiev, Kristie Lim, Kushal Tirumala, Kyle Miller, Lama Ahmad, Larry Lv, Laura Clare, Laurance Fauconnet, Lauren Itow, Lauren Yang, Laurentia Romaniuk, Leah Anise, Lee Byron, Leher Pathak, Leon Maksin, Leyan Lo, Leyton Ho, Li Jing, Liang Wu, Liang Xiong, Lien Mamitsuka, Lin Yang, Lindsay McCallum, Lindsey Held, Liz Bourgeois, Logan Engstrom, Lorenz Kuhn, Louis Feuvrier, Lu Zhang, Lucas Switzer, Lukas Kondraciuk, Lukasz Kaiser, Manas Joglekar, Mandeep Singh, Mandip Shah, Manuka Stratta, Marcus Williams, Mark Chen, Mark Sun, Marselus Cayton, Martin Li, Marvin Zhang, Marwan Aljubeh, Matt Nichols, Matthew Haines, Max Schwarzer, Mayank Gupta, Meghan Shah, Melody Huang, Meng Dong, Mengqing Wang, Mia Glaese, Micah Carroll, Michael Lampe, Michael Malek, Michael Sharman, Michael Zhang, Michele Wang, Michelle Pokrass, Mihai Florian, Mikhail Pavlov, Miles Wang, Ming Chen, Mingxuan Wang, Minnia Feng, Mo Bavarian, Molly Lin, Moose Abdool, Mostafa Rohaninejad, Nacho Soto, Natalie Staudacher, Natan LaFontaine, Nathan Marwell, Nelson Liu, Nick Preston, Nick Turley, Nicklas Ansman, Nicole Blades, Nikil Pancha, Nikita Mikhaylin, Niko Felix, Nikunj Handa, Nishant Rai, Nitish Keskar, Noam Brown, Ofir Nachum, Oleg Boiko, Oleg Murk, Olivia Watkins, Oona Gleeson, Pamela Mishkin, Patryk Lesiewicz, Paul Baltescu, Pavel Belov, Peter Zhokhov, Philip Pronin, Phillip Guo, Phoebe Thacker, Qi Liu, Qiming Yuan, Qinghua Liu, Rachel Dias, Rachel Puckett, Rahul Arora, Ravi Teja Mullapudi, Raz Gaon, Reah Miyara, Rennie Song, Rishabh Aggarwal, RJ Marsan, Robel Yemiru, Robert Xiong, Rohan Kshirsagar, Rohan Nuttall, Roman Tsiupa, Ronen Eldan, Rose Wang, Roshan James, Roy Ziv, Rui Shu, Ruslan Nigmatullin, Saachi Jain, Saam Talaie, Sam Altman, Sam Arnesen, Sam Toizer, Sam Toyer, Samuel Miserendino, Sandhini Agarwal, Sarah Yoo, Savannah Heon, Scott Ethersmith, Sean Grove, Sean Taylor, Sebastien Bubeck, Sever Banesiu, Shaokyi Amdo, Shengjia Zhao, Sherwin Wu, Shibani Santurkar, Shiyu Zhao, Shraman Ray Chaudhuri, Shreyas Krishnaswamy, Shuaiqi, Xia, Shuyang Cheng, Shyamal Anadkat, Simón Posada Fishman, Simon Tobin, Siyuan Fu, Somay Jain, Song Mei, Sonya Egoian, Spencer Kim, Spug Golden, SQ Mah, Steph Lin, Stephen Imm, Steve Sharpe, Steve Yadlowsky, Sulman Choudhry, Sungwon Eum, Suvansh Sanjeev, Tabarak Khan, Tal Stramer, Tao Wang, Tao Xin, Tarun Gogineni, Taya Christianson, Ted Sanders, Tejal Patwardhan, Thomas Degry, Thomas Shadwell, Tianfu Fu, Tianshi Gao, Timur Garipov, Tina Sriskandarajah, Toki Sherbakov, Tomer Kaftan, Tomo Hiratsuka, Tongzhou Wang, Tony Song, Tony Zhao, Troy Peterson, Val Kharitonov, Victoria Chernova, Vineet Kosaraju, Vishal Kuo, Vitchyr Pong, Vivek Verma, Vlad Petrov, Wanning Jiang, Weixing Zhang, Wenda Zhou, Wenlei Xie, Wenting Zhan, Wes McCabe, Will DePue, Will Ellsworth, Wulfie Bain, Wyatt Thompson, Xiangning Chen, Xiangyu Qi, Xin Xiang, Xinwei Shi, Yann Dubois, Yaodong Yu, Yara Khakbaz, Yifan Wu, Yilei Qian, Yin Tat Lee, Yinbo Chen, Yizhen Zhang, Yizhong Xiong, Yonglong Tian, Young Cha, Yu Bai, Yu Yang, Yuan Yuan, Yuanzhi Li, Yufeng Zhang, Yuguang Yang, Yujia Jin, Yun Jiang, Yunyun Wang, Yushi Wang, Yutian Liu, Zach Stubenvoll, Zehao Dou, Zheng Wu, and Zhigang Wang. Openai gpt-5 system card, 2025. URL [https://arxiv.org/abs/2601.03267](https://arxiv.org/abs/2601.03267).
- Song et al. (2025) Huatong Song, Jinhao Jiang, Yingqian Min, Jie Chen, Zhipeng Chen, Wayne Xin Zhao, Lei Fang, and Ji-Rong Wen. R1-searcher: Incentivizing the search capability in llms via reinforcement learning, 2025. URL [https://arxiv.org/abs/2503.05592](https://arxiv.org/abs/2503.05592).
- Team (2024) Qwen Team. Qwen2.5: A party of foundation models, September 2024. URL [https://qwen.ai/blog?id=qwen2.5](https://qwen.ai/blog?id=qwen2.5).
- Team (2025a) Qwen Team. Qwen3-max: Just scale it, September 2025a. URL [https://qwen.ai/blog?id=241398b9cd6353de490b0f82806c7848c5d2777d](https://qwen.ai/blog?id=241398b9cd6353de490b0f82806c7848c5d2777d).
- Team (2025b) Qwen Team. Qwen3 technical report, 2025b. URL [https://arxiv.org/abs/2505.09388](https://arxiv.org/abs/2505.09388).
- Trivedi et al. (2022) Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot, and Ashish Sabharwal. Musique: Multihop questions via single-hop question composition, 2022. URL [https://arxiv.org/abs/2108.00573](https://arxiv.org/abs/2108.00573).
- Trivedi et al. (2023) Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot, and Ashish Sabharwal. Interleaving retrieval with chain-of-thought reasoning for knowledge-intensive multi-step questions. In Anna Rogers, Jordan Boyd-Graber, and Naoaki Okazaki, editors, *Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pages 10014–10037, Toronto, Canada, July 2023. Association for Computational Linguistics. [10.18653/v1/2023.acl-long.557](https://doi.org/10.18653/v1/2023.acl-long.557). URL [https://aclanthology.org/2023.acl-long.557/](https://aclanthology.org/2023.acl-long.557/).
- Uesato et al. (2022) Jonathan Uesato, Nate Kushman, Ramana Kumar, Francis Song, Noah Siegel, Lisa Wang, Antonia Creswell, Geoffrey Irving, and Irina Higgins. Solving math word problems with process-and outcome-based feedback. *arXiv preprint arXiv:2211.14275*, 2022.
- Wang et al. (2025a) Hongru Wang, Cheng Qian, Wanjun Zhong, Xiusi Chen, Jiahao Qiu, Shijue Huang, Bowen Jin, Mengdi Wang, Kam-Fai Wong, and Heng Ji. Acting less is reasoning more! teaching model to act efficiently, 2025a. URL [https://arxiv.org/abs/2504.14870](https://arxiv.org/abs/2504.14870).
- Wang et al. (2022) Liang Wang, Nan Yang, Xiaolong Huang, Binxing Jiao, Linjun Yang, Daxin Jiang, Rangan Majumder, and Furu Wei. Text embeddings by weakly-supervised contrastive pre-training. *arXiv preprint arXiv:2212.03533*, 2022.
- Wang et al. (2025b) Ziliang Wang, Xuhui Zheng, Kang An, Cijun Ouyang, Jialu Cai, Yuhang Wang, and Yichao Wu. Stepsearch: Igniting llms search ability via step-wise proximal policy optimization, 2025b. URL [https://arxiv.org/abs/2505.15107](https://arxiv.org/abs/2505.15107).
- Wei et al. (2025) Quan Wei, Siliang Zeng, Chenliang Li, William Brown, Oana Frunza, Wei Deng, Anderson Schneider, Yuriy Nevmyvaka, Yang Katie Zhao, Alfredo Garcia, and Mingyi Hong. Reinforcing multi-turn reasoning in llm agents via turn-level reward design, 2025. URL [https://arxiv.org/abs/2505.11821](https://arxiv.org/abs/2505.11821).
- Xi et al. (2025) Zhiheng Xi, Jixuan Huang, Chenyang Liao, Baodai Huang, Honglin Guo, Jiaqi Liu, Rui Zheng, Junjie Ye, Jiazheng Zhang, Wenxiang Chen, Wei He, Yiwen Ding, Guanyu Li, Zehui Chen, Zhengyin Du, Xuesong Yao, Yufei Xu, Jiecao Chen, Tao Gui, Zuxuan Wu, Qi Zhang, Xuanjing Huang, and Yu-Gang Jiang. Agentgym-rl: Training llm agents for long-horizon decision making through multi-turn reinforcement learning, 2025. URL [https://arxiv.org/abs/2509.08755](https://arxiv.org/abs/2509.08755).
- Yang et al. (2018) Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William W. Cohen, Ruslan Salakhutdinov, and Christopher D. Manning. Hotpotqa: A dataset for diverse, explainable multi-hop question answering, 2018. URL [https://arxiv.org/abs/1809.09600](https://arxiv.org/abs/1809.09600).
- Yao et al. (2022) Shunyu Yao, Howard Chen, John Yang, and Karthik Narasimhan. Webshop: Towards scalable real-world web interaction with grounded language agents. In S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh, editors, *Advances in Neural Information Processing Systems*, volume 35, pages 20744–20757. Curran Associates, Inc., 2022. URL [https://proceedings.neurips.cc/paper_files/paper/2022/file/82ad13ec01f9fe44c01cb91814fd7b8c-Paper-Conference.pdf](https://proceedings.neurips.cc/paper_files/paper/2022/file/82ad13ec01f9fe44c01cb91814fd7b8c-Paper-Conference.pdf).
- Zhang et al. (2026) Ming Zhang, Kexin Tan, Yueyuan Huang, Yujiong Shen, Chunchun Ma, Li Ju, Xinran Zhang, Yuhui Wang, Wenqing Jing, Jingyi Deng, Huayu Sha, Binze Hu, Jingqi Tong, Changhao Jiang, Yage Geng, Yuankai Ying, Yue Zhang, Zhangyue Yin, Zhiheng Xi, Shihan Dou, Tao Gui, Qi Zhang, and Xuanjing Huang. Opennovelty: An llm-powered agentic system for verifiable scholarly novelty assessment, 2026. URL [https://arxiv.org/abs/2601.01576](https://arxiv.org/abs/2601.01576).
- Zhang et al. (2025a) Wenlin Zhang, Xiaopeng Li, Yingyi Zhang, Pengyue Jia, Yichao Wang, Huifeng Guo, Yong Liu, and Xiangyu Zhao. Deep research: A survey of autonomous research agents. *arXiv preprint arXiv:2508.12752*, 2025a.
- Zhang et al. (2025b) Yaocheng Zhang, Haohuan Huang, Zijun Song, Yuanheng Zhu, Qichao Zhang, Zijie Zhao, and Dongbin Zhao. Criticsearch: Fine-grained credit assignment for search agents via a retrospective critic, 2025b. URL [https://arxiv.org/abs/2511.12159](https://arxiv.org/abs/2511.12159).
- Zhao et al. (2026) Penghao Zhao, Hailin Zhang, Qinhan Yu, Zhengren Wang, Yunteng Geng, Fangcheng Fu, Ling Yang, Wentao Zhang, Jie Jiang, and Bin Cui. Retrieval-augmented generation for ai-generated content: A survey. *Data Science and Engineering*, pages 1–29, 2026.
- Zheng et al. (2024) Lianmin Zheng, Liangsheng Yin, Zhiqiang Xie, Chuyue Sun, Jeff Huang, Cody Hao Yu, Shiyi Cao, Christos Kozyrakis, Ion Stoica, Joseph E. Gonzalez, Clark Barrett, and Ying Sheng. Sglang: Efficient execution of structured language model programs. In A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang, editors, *Advances in Neural Information Processing Systems*, volume 37, pages 62557–62583. Curran Associates, Inc., 2024. [10.52202/079017-2000](https://doi.org/10.52202/079017-2000). URL [https://proceedings.neurips.cc/paper_files/paper/2024/file/724be4472168f31ba1c9ac630f15dec8-Paper-Conference.pdf](https://proceedings.neurips.cc/paper_files/paper/2024/file/724be4472168f31ba1c9ac630f15dec8-Paper-Conference.pdf).
- Zhou et al. (2024) Yujia Zhou, Yan Liu, Xiaoxi Li, Jiajie Jin, Hongjin Qian, Zheng Liu, Chaozhuo Li, Zhicheng Dou, Tsung-Yi Ho, and Philip S Yu. Trustworthiness in retrieval-augmented generation systems: A survey. *arXiv preprint arXiv:2409.10102*, 2024.
- Zhu et al. (2025) Dawei Zhu, Xiyu Wei, Guangxiang Zhao, Wenhao Wu, Haosheng Zou, Junfeng Ran, Xun Wang, Lin Sun, Xiangzheng Zhang, and Sujian Li. Chain-of-thought matters: improving long-context language models with reasoning path supervision. *arXiv preprint arXiv:2502.20790*, 2025.

## Appendix

## Appendix A Analysis of Failure Trajectories and Credit Assignment Ambiguity

In this section, we discuss why round-level credit assignment is unreliable in failed trajectories, complementing the design choice discussed in Section [3.4](#S3.SS4 "3.4 Adaptive Weighting Mechanism ‣ 3 Contribution-Weighted GRPO ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization"). The key challenge is that failed trajectories typically lack clearly identifiable low-quality rounds that can be reliably attributed to the final failure. Such ambiguity leads to a high risk of introducing noise when selectively reweighting search rounds. Concretely:

- •
  Redundant/verification queries: These rounds look redundant but may serve an implicit verification role (re-checking ambiguous evidence). Heuristically marking such rounds as low-quality would risk removing legitimate verification behavior.
- •
  Cascading Errors from Misinterpreted Evidence: Later retrieval rounds may be misled by earlier misinterpretations of superficially relevant yet non-supportive documents, and therefore should not be regarded as the primary source of failure.
- •
  Attempts that failed to obtain key information: When a search round recalls no useful documents, it usually shows no obvious error — the failure is caused by insufficient corpus coverage or inadequate retriever recall, not a clearly “bad” decision the agent made.
- •
  Premature overconfidence: This usually occurs at the answer round, not during intermediate search rounds, and thus falls outside the scope of round-level search credit assignment.

A failure pattern that yields a reliably detectable low-quality signal is similar-entity confusion. Because most failure patterns are inherently ambiguous at round granularity, treating failed trajectories differently (uniform contribution) avoids reinforcing spurious signals and preserves GRPO’s stable outcome-based baseline.

## Appendix B LLM Judge Calibration Details

To improve transparency, we describe the calibration protocol of our LLM judge and summarize the associated dataset statistics below.

The calibration set contains 97 search rounds sampled from successful GRPO trajectories with diverse trajectory lengths. Each search round is annotated by a human annotator with respect to two criteria: retrieval utility and reasoning correctness. In addition, the annotator provides a confidence score indicating the certainty of the judgment for each labeled round.

To analyze how judgment quality varies with trajectory length, Table [6](#A2.T6 "Table 6 ‣ Appendix B LLM Judge Calibration Details ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization") reports the distribution of search rounds across different trajectory lengths, distinguishing whether each round simultaneously satisfies both retrieval utility and reasoning correctness. This allows us to examine how the quality of search rounds evolves as trajectories become longer.

To further understand the uncertainty structure of the calibration data, Table [6](#A2.T6 "Table 6 ‣ Appendix B LLM Judge Calibration Details ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization") breaks down the annotation confidence conditioned on whether a search round satisfies both quality criteria.

Overall, among the 89 high-confidence rounds, the LLM judge agrees with the human annotator on 87 rounds; among the remaining 8 medium-confidence cases, agreement occurs in 6 cases, yielding an overall agreement rate of 95.8%. This demonstrates strong alignment between the LLM judge and human judgments, particularly in high-confidence annotations.

|                               |                               |                        |
|-------------------------------|-------------------------------|------------------------|
|  Number of Search Rounds      |  Satisfies Both Criteria      |  Does not Satisfy      |
| 1                             | 5                             | 0                      |
| 2                             | 17                            | 3                      |
| 3                             | 18                            | 12                     |
| $\geq$4                       | 18                            | 24                     |

Table 5: Quality distribution of search rounds across different trajectory lengths.

|                         |      |        |     |
|-------------------------|------|--------|-----|
| Confidence              | High | Medium | Low |
| Satisfies both criteria | 55   | 3      | 0   |
| Does not satisfy        | 34   | 5      | 0   |

Table 6: Confidence distribution across quality labels.

## Appendix C Computational Cost of LLM Judge

We provide a brief analysis of the computational cost introduced by the LLM judge during training. The judge model GPT-oss-120B has 116.8B parameters and adopts a Mixture-of-Experts (MoE) architecture, where only 5.1B parameters are activated per token. According to official deployment guidelines, the model can be served on a single NVIDIA H100 GPU, making it feasible to integrate into the training pipeline. In practice, incorporating the LLM judge leads to a moderate increase in training cost. Specifically, CW-GRPO training takes 11.7 hours on 5 GPUs (including one GPU dedicated to the judge), compared to 8.8 hours on 4 GPUs for standard GRPO, corresponding to approximately a 33% increase in wall-clock time. Overall, while the LLM judge introduces additional computational cost, we find it manageable in our experimental setup.

## Appendix D Prompts

We present the detailed prompts that guide the behavior of our LLM judge and search agent in this section.

Figure [5](#A4.F5 "Figure 5 ‣ Appendix D Prompts ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization") illustrates the prompt used by the LLM judge, which specifies the rubrics for assessing each search round in terms of retrieval utility and reasoning correctness, producing the binary contribution signals used in CW-GRPO.

Figure [6](#A4.F6 "Figure 6 ‣ Appendix D Prompts ‣ Enhancing LLM-based Search Agents via Contribution Weighted Group Relative Policy Optimization") shows the input prompt used during model training, defining how the search agent structures its reasoning, interacts with the retrieval tool across rounds, and generates the final answer.

Figure 5: The prompt for LLM Judge to specify the rubric for assessing each search round in terms of retrieval utility and reasoning correctness.

![Refer to caption](2604.14267v2/training_prompt.png)

Figure 6: The prompt for RL training.

Experimental support, please [view the build logs](./2604.14267v2/__stdout.txt) for errors. Generated by [ L A T E xml ![\[LOGO\]](img)](https://math.nist.gov/~BMiller/LaTeXML/) .

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
