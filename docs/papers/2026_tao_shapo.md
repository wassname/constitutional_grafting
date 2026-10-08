---
title: "Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"
authors: "Wenjian Tao et al."
year: 2026
source: https://arxiv.org/html/2602.07340v2
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

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) [![](img) Report Issue](# "Report an Issue") [![](img) Back to Abstract](/abs/2602.07340v2 "Back to abstract page") [![](img) Download PDF](/pdf/2602.07340v2 "Download PDF") [![](img)](javascript:toggleNavTOC(); "Toggle navigation") [![](img)](javascript:toggleReadingMode(); "Disable reading mode, show header and footer")

![](img) ![](img) ![](img)

1.  [Abstract](#abstract1 "In Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
2.  [1 Introduction](#S1 "In Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
    1.  [Selective geometry control.](#S1.SS0.SSS0.Px1 "In 1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
    2.  [Multi-level instantiations.](#S1.SS0.SSS0.Px2 "In 1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
    3.  [Composability.](#S1.SS0.SSS0.Px3 "In 1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
3.  [2 Preliminaries](#S2 "In Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
    1.  [Safety Alignment via Preference Optimization.](#S2.SS0.SSS0.Px1 "In 2 Preliminaries ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
    2.  [Data-uncertainty Robustness.](#S2.SS0.SSS0.Px2 "In 2 Preliminaries ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
    3.  [Geometry-related Robustness.](#S2.SS0.SSS0.Px3 "In 2 Preliminaries ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
4.  [3 Selective Geometry Control for Robust Safety Alignment](#S3 "In Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
    1.  [3.1 Optimization Objective of ShaPO](#S3.SS1 "In 3 Selective Geometry Control for Robust Safety Alignment ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
    2.  [3.2 Safety-critical Subspace Approximation](#S3.SS2 "In 3 Selective Geometry Control for Robust Safety Alignment ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
    3.  [3.3 Instantiations of ShaPO](#S3.SS3 "In 3 Selective Geometry Control for Robust Safety Alignment ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
        1.  [①Token-level ShaPO .](#S3.SS3.SSS0.Px1 "In 3.3 Instantiations of ShaPO ‣ 3 Selective Geometry Control for Robust Safety Alignment ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
        2.  [②Reward-level ShaPO .](#S3.SS3.SSS0.Px2 "In 3.3 Instantiations of ShaPO ‣ 3 Selective Geometry Control for Robust Safety Alignment ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
        3.  [Discussion of reward-level ShaPO .](#S3.SS3.SSS0.Px3 "In 3.3 Instantiations of ShaPO ‣ 3 Selective Geometry Control for Robust Safety Alignment ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
    4.  [3.4 Optimization Process](#S3.SS4 "In 3 Selective Geometry Control for Robust Safety Alignment ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
        1.  [Robustness Insights of ShaPO .](#S3.SS4.SSS0.Px1 "In 3.4 Optimization Process ‣ 3 Selective Geometry Control for Robust Safety Alignment ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
5.  [4 Experiments](#S4 "In Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
    1.  [4.1 Experimental Setting](#S4.SS1 "In 4 Experiments ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
        1.  [Benchmarks and Backbones.](#S4.SS1.SSS0.Px1 "In 4.1 Experimental Setting ‣ 4 Experiments ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
        2.  [Baselines and Evaluation Metrics.](#S4.SS1.SSS0.Px2 "In 4.1 Experimental Setting ‣ 4 Experiments ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
    2.  [4.2 In-distribution Alignment Performance](#S4.SS2 "In 4 Experiments ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
    3.  [4.3 Safety robustness under domain shift](#S4.SS3 "In 4 Experiments ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
    4.  [4.4 Safety robustness to noisy supervision](#S4.SS4 "In 4 Experiments ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
    5.  [4.5 Comprehensive Analysis of ShaPO](#S4.SS5 "In 4 Experiments ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
        1.  [Composability of ShaPO.](#S4.SS5.SSS0.Px1 "In 4.5 Comprehensive Analysis of ShaPO ‣ 4 Experiments ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
        2.  [Why selective Geometry Control.](#S4.SS5.SSS0.Px2 "In 4.5 Comprehensive Analysis of ShaPO ‣ 4 Experiments ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
        3.  [Geometry of the Loss Landscape.](#S4.SS5.SSS0.Px3 "In 4.5 Comprehensive Analysis of ShaPO ‣ 4 Experiments ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
        4.  [Effect of Reward Supervision.](#S4.SS5.SSS0.Px4 "In 4.5 Comprehensive Analysis of ShaPO ‣ 4 Experiments ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
6.  [5 Conclusion](#S5 "In Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
7.  [References](#bib "In Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
8.  [A Algorithm and Optimization Details](#A1 "In Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
9.  [B Related Works](#A2 "In Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
10. [C Theoretical Insight: Detailed Proofs](#A3 "In Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
    1.  [C.1 PAC-Bayes Generalization Bound of ShaPO](#A3.SS1 "In Appendix C Theoretical Insight: Detailed Proofs ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
        1.  [Setup.](#A3.SS1.SSS0.Px1 "In C.1 PAC-Bayes Generalization Bound of ShaPO ‣ Appendix C Theoretical Insight: Detailed Proofs ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
        2.  [PAC-Bayes framework.](#A3.SS1.SSS0.Px2 "In C.1 PAC-Bayes Generalization Bound of ShaPO ‣ Appendix C Theoretical Insight: Detailed Proofs ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
        3.  [Bounding the KL term.](#A3.SS1.SSS0.Px3 "In C.1 PAC-Bayes Generalization Bound of ShaPO ‣ Appendix C Theoretical Insight: Detailed Proofs ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
    2.  [C.2 Bypass Boundary Expansion](#A3.SS2 "In Appendix C Theoretical Insight: Detailed Proofs ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
        1.  [Local risk approximation.](#A3.SS2.SSS0.Px1 "In C.2 Bypass Boundary Expansion ‣ Appendix C Theoretical Insight: Detailed Proofs ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
        2.  [Bypass boundary.](#A3.SS2.SSS0.Px2 "In C.2 Bypass Boundary Expansion ‣ Appendix C Theoretical Insight: Detailed Proofs ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
11. [D Experimental Setup](#A4 "In Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
    1.  [D.1 Benchmarks](#A4.SS1 "In Appendix D Experimental Setup ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
    2.  [D.2 Baseline Description](#A4.SS2 "In Appendix D Experimental Setup ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
    3.  [D.3 Implementation Details](#A4.SS3 "In Appendix D Experimental Setup ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
        1.  [Reward Model Usage.](#A4.SS3.SSS0.Px1 "In D.3 Implementation Details ‣ Appendix D Experimental Setup ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
12. [E Additional Experimental Results](#A5 "In Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
    1.  [E.1 Linear Probe Training](#A5.SS1 "In Appendix E Additional Experimental Results ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
        1.  [Probe Accuracy.](#A5.SS1.SSS0.Px1 "In E.1 Linear Probe Training ‣ Appendix E Additional Experimental Results ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
        2.  [Probe Decoding.](#A5.SS1.SSS0.Px2 "In E.1 Linear Probe Training ‣ Appendix E Additional Experimental Results ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
    2.  [E.2 Training Reward Margin](#A5.SS2 "In Appendix E Additional Experimental Results ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")
    3.  [E.3 Safety Robustness under Domain Shift](#A5.SS3 "In Appendix E Additional Experimental Results ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")

[License: arXiv.org perpetual non-exclusive license](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2602.07340v2 \[cs.LG\] 21 May 2026

# Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control

Yonghui Yang Affiliation: National University of Singapore    Wenjian Tao Affiliation: Hefei University of Technology    Jilong Liu Affiliation: Hefei University of Technology    Xingyu Zhu Affiliation: National University of Singapore    Junfeng Fang Affiliation: National University of Singapore    Weibiao Huang Affiliation: ST Engineering Ltd., Singapore    Le Wu Affiliation: Hefei University of Technology    Richang Hong Affiliation: Hefei University of Technology Correspondence to: <hongrh.hfut@gmail.com>    Tat-Seng Chua Affiliation: National University of Singapore

###### Abstract

Safety alignment of large language models remains brittle under domain shift and noisy preference supervision. Most existing robust alignment methods focus on uncertainty in alignment data, while overlooking optimization-induced fragility in preference-based objectives. In this work, we revisit robustness for LLM safety alignment from an optimization geometry perspective, and argue that robustness failures cannot be addressed by data-centric methods alone. We propose ShaPO, a geometry-aware preference optimization framework that enforces worst-case alignment objectives via selective geometry control over alignment-critical parameter subspace. By avoiding uniform geometry constraints, ShaPO mitigates the over-regularization that can harm robustness under distribution shift. We instantiate ShaPO at two levels: token-level ShaPO stabilizes likelihood-based surrogate optimization, while reward-level ShaPO enforces reward-consistent optimization under noisy supervision. Across diverse safety benchmarks and noisy preference settings, ShaPO consistently improves safety robustness over popular preference optimization methods. Moreover, ShaPO composes cleanly with data-robust objectives, yielding additional gains and empirically supporting the proposed optimization-geometry perspective. The code is available at [https://github.com/liujilong0116/ShaPO](https://github.com/liujilong0116/ShaPO).

###### Keywords: 

LLM Safety Alignment, Robust Preference Optimization, Selective Geometry Control

^(†)^(†)affiliationnotice: Equal contribution ^(†)Work done during internship at NExT++ Research Centre, National University of Singapore.

## 1 Introduction

Safety alignment of large language models (LLMs) is commonly approached through preference-based optimization, where models are trained to prefer safe responses over unsafe ones based on human judgments ([Ji et al., 2023c](#bib.bib35); [Lu et al., 2025](#bib.bib36)). This paradigm is most notably instantiated through Reinforcement Learning from Human Feedback (RLHF) ([Christiano et al., 2017](#bib.bib27); [Ouyang et al., 2022](#bib.bib26)), which has become a standard approach for aligning LLM behavior with human safety preferences. To reduce the complexity and instability of RLHF, recent methods such as Direct Preference Optimization (DPO) ([Rafailov et al., 2023](#bib.bib8)) and its variants ([Gheshlaghi Azar et al., 2023](#bib.bib10); [Chowdhury et al., 2024](#bib.bib11); [Mitchell, 2023](#bib.bib9); [Meng et al., 2024](#bib.bib25)) directly optimize preference objectives, substantially simplifying training while retaining competitive alignment performance. As a result, preference-based optimization has emerged as a practical and widely adopted paradigm for safety alignment.

Despite their effectiveness during training, preference-aligned models often exhibit brittle behavior in deployment, suggesting that safety alignment can remain shallow and insufficiently robust ([Anwar et al., 2024](#bib.bib37); [Qi et al., 2024](#bib.bib34)). Empirical studies show that models performing well on curated safety benchmarks may still produce unsafe responses under domain shift or noisy preference supervision ([Wei et al., 2024](#bib.bib38); [Gao et al., 2024](#bib.bib39)), exposing a gap between training- and deployment-time robustness. To address this gap, prior work has primarily focused on reducing data uncertainty, through strategies such as preference data selection ([Gao et al., 2025](#bib.bib14); [Kong et al., 2024](#bib.bib32); [Yeh and Li, 2025](#bib.bib33)), margin-based reweighting ([Gheshlaghi Azar et al., 2023](#bib.bib10); [Huang et al., 2025](#bib.bib31)), and distributionally robust optimization over preference distributions ([Wu et al., 2024](#bib.bib18); [Zhu et al., 2025a](#bib.bib15)). While effective against annotation noise and distribution shift, these data-centric approaches implicitly attribute robustness failures to uncertainty in the supervision signal.

Figure 1: Cumulative contribution to worst-case alignment loss under parameter perturbations. We compare the fraction of the total worst-case loss increase accounted for by perturbing probe-identified safety-critical neurons (Top-K) versus randomly selected neurons of the same size (Random-K).

From the robustness perspective, existing data-centric approaches primarily target uncertainty in the supervision signal, while the optimization geometry determines how sensitively alignment behavior responds to such uncertainty during training. In particular, sharp alignment landscapes can amplify even minor noise in preference data, leading to fragile safety behavior under domain shift ([Foret et al., 2020](#bib.bib16); [Wang et al., 2023a](#bib.bib40)). To this end, we revisit robustness in safety alignment from the lens of optimization geometry. Nevertheless, introducing geometry control to preference-based alignment still presents practical questions about where constraints should be applied, at what level they should be instantiated, and how they interact with data-centric robustness methods.

#### Selective geometry control.

We propose Sharpness-aware Preference Optimization (ShaPO) , a geometry-aware framework that enforces worst-case alignment stability only along alignment-critical directions. Prior work suggests that safety behavior in large language models is structurally localized to a small subset of internal representations ([Wei et al., 2024](#bib.bib38); [Zhao et al., 2025b](#bib.bib41)), making uniform geometry control prone to over-constraining parameters unrelated to safety and degrading cross-domain robustness ([Niu et al., 2025](#bib.bib52); [Perin et al., 2025](#bib.bib48)). To understand where worst-case alignment sensitivity arises, we conduct an empirical study that ranks neurons by their similarity to probe-identified safety-critical directions. As shown in Figure [1](#S1.F1 "Figure 1 ‣ 1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), perturbing fewer than 0.5% of these neurons already accounts for over 80% of the cumulative worst-case alignment loss, while randomly selected neurons of the same size contribute substantially less. This concentration indicates that selective geometry control can closely approximate worst-case optimization without unnecessarily restricting non-safety parameters, thereby preserving degrees of freedom important for robust generalization under domain shift.

#### Multi-level instantiations.

Preference-based alignment objectives exhibit distinct failure modes at different levels of abstraction, motivating geometry-aware robustness at both the token and reward levels. Token-level ShaPO  applies selective geometry control to likelihood-based surrogate alignment objectives, such as the DPO loss ([Rafailov et al., 2023](#bib.bib8)), without requiring an explicit reward model. This instantiation provides a lightweight mechanism for stabilizing preference optimization driven by token-level supervision. Reward-level ShaPO  applies selective geometry control to reward-based alignment objectives, using a pre-trained reward model as a semantically grounded proxy for safety. By enforcing stability with respect to reward-consistent signals, this instantiation offers an alternative robustness pathway in settings where token-level surrogates may be misaligned with semantic safety.

#### Composability.

ShaPO targets optimization-induced fragility rather than uncertainty in the supervision data, and is therefore complementary to data-centric robustness techniques. This complementary scope allows geometry-aware robustness to be combined with existing data-robust objectives without modifying the supervision signal. In our experiments across diverse safety benchmarks under domain shift and noisy supervision, both token-level and reward-level variants of ShaPO can be applied either on their own or alongside representative data-centric methods, and we observe additional robustness improvements when the two are combined. Together, these results support optimization geometry as a complementary design dimension for robust LLM safety alignment.

## 2 Preliminaries

#### Safety Alignment via Preference Optimization.

Safety alignment seeks to ensure that LLMs avoid generating harmful outputs while maintaining task utility. In practice, this is typically achieved through post-training preference optimization, where models are trained to favor safer responses over unsafe alternatives ([Ouyang et al., 2022](#bib.bib26); [Ji et al., 2023a](#bib.bib4)). This formulation underlies a broad class of alignment methods, including reinforcement learning from human feedback (RLHF ([Bai et al., 2022](#bib.bib5))) and its simplified variants, such as Direct Preference Optimization (DPO ([Rafailov et al., 2023](#bib.bib8))). Concretely, given a dataset of preference triples $\mathcal{O} = {\{{(x,y^{w},y^{l})}\}}$, where $y^{w}$ is preferred over $y^{l}$, DPO instantiates preference-based alignment by optimizing the following objective:

|     |                                                                                                                                                                                                                                                                    |     |     |
|-----|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $${{\mathcal{L}_{\text{align}}\hspace{0pt}{(\theta)}} = {- {{\mathbb{E}}_{{(x,y^{w},y^{l})} \sim \mathcal{O}}\hspace{0pt}\left\lbrack {\log{\sigma\left( {{r_{\theta}\hspace{0pt}{(x,y^{w})}} - {r_{\theta}\hspace{0pt}{(x,y^{l})}}} \right)}} \right\rbrack}}},$$ |     | (1) |

where ${r_{\theta}\hspace{0pt}{(x,y)}} = {\beta\hspace{0pt}{\log\frac{\pi_{\theta}\hspace{0pt}\left. (y \middle| x) \right.}{\pi_{ref}\hspace{0pt}\left. (y \middle| x) \right.}}}$ denotes an implicit reward function. More generally, we denote the preference-based alignment objective as $\mathcal{L}_{\text{align}}\hspace{0pt}{(\theta)}$.

#### Data-uncertainty Robustness.

While the preference-based alignment pipeline provides a principled objective for safety alignment, its effectiveness depends critically on the quality and reliability of the underlying preference supervision. In practice, preference data may be noisy, inconsistent, or subject to distribution shift, leading to mis-specified optimization targets ([Wei et al., 2024](#bib.bib38); [Gao et al., 2024](#bib.bib39)). A common approach to address such uncertainty is to adopt a distributionally robust optimization ([Delage and Ye, 2010](#bib.bib42); [Levy et al., 2020](#bib.bib43)) formulation, which optimizes alignment performance under worst-case perturbations of the preference data. Formally, the optimization objective can be written as

|     |                                                                                                                                                                                                                                            |     |     |
|-----|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $${{{{\min\limits_{\theta}\max\limits_{\mathcal{O}^{\prime}}}\hspace{0pt}\mathcal{L}_{\text{align}}\hspace{0pt}{(\mathcal{O}^{\prime},\theta)}},s}.t.{{{\mathbb{D}}_{\phi}\hspace{0pt}{(\mathcal{O}^{\prime},\mathcal{O})}} \leq \eta}},$$ |     | (2) |

where $\mathcal{O}$ denotes the observed preference supervision, and $\mathcal{O}^{\prime}$ represents a perturbed preference distribution within a neighborhood defined by the divergence ${{\mathbb{D}}_{\phi}\hspace{0pt}{(\mathcal{O}^{\prime},\mathcal{O})}} \leq \eta$. This formulation has been widely adopted to model robustness with respect to worst-case variations in preference supervision, and underlies a class of data-centric robust alignment approaches that address noise and distribution shift in preference data ([Wu et al., 2024](#bib.bib18); [Zhu et al., 2025a](#bib.bib15)).

#### Geometry-related Robustness.

Data-centric robustness formulations improve alignment reliability by accounting for uncertainty in preference supervision. However, such approaches implicitly attribute robustness failures solely to variations in the data, overlooking the sensitivity that may arise from the optimization process itself ([Jiang et al., 2019](#bib.bib44); [Foret et al., 2020](#bib.bib16)). To capture robustness beyond data uncertainty, we consider a formulation that accounts for both data-side and parameter-side sources of fragility in preference-based alignment. For conceptual clarity, robustness in preference-based alignment can be viewed along two complementary axes:

|     |                                                                                                                                                                                                                                                                                                                                                                                       |     |     |
|-----|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $$\min{}_{\theta}\underbrace{\max{}_{\mathcal{O}^{\prime}:{{{\mathbb{D}}_{\phi}\hspace{0pt}{(\mathcal{O}^{\prime},\mathcal{O})}}\leq\eta}}\mathcal{L}{}_{\text{align}}(\theta;\mathcal{O}{}^{\prime})}{}_{\text{data-side}} + \underbrace{{\max\limits_{{\|\epsilon\|}\leq\rho}⁡\mathcal{L}_{\text{align}}}\hspace{0pt}{({\theta+\epsilon},\mathcal{O})}}{}_{\text{parameter-side}},$$ |     | (3) |

where $\epsilon$ denotes a bounded perturbation in the model parameter space. Given the above analysis, we focus on parameter-side robustness to improve the stability of safety alignment, viewing optimization geometry as a complementary axis to existing data-uncertainty approaches.

![Refer to caption](2602.07340v2/ShaPO-Framework.png)

Figure 2: Overview of ShaPO , a robust preference optimization framework with selective geometry control. ShaPO minimizes the worst-case alignment loss under adversarial perturbations restricted to the alignment-critical parameter subspace. Here is the instantiation of ShaPO at reward level.

## 3 Selective Geometry Control for Robust Safety Alignment

We present ShaPO , a geometry-aware optimization framework for robust safety alignment. Figure [2](#S2.F2 "Figure 2 ‣ Geometry-related Robustness. ‣ 2 Preliminaries ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control") provides an overview of the framework, and this section details the selective geometry control objective, safety-critical subspace approximation, and its instantiations at both the token and reward levels.

### 3.1 Optimization Objective of ShaPO 

Preference-based alignment specifies relative behavioral constraints, and robustness requires these preferences to remain stable under small parameter perturbations. We adopt a geometry-aware formulation that optimizes the alignment objective under worst-case perturbations:

|     |                                                                                                              |     |     |
|-----|--------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $${{\max\limits_{{\|\epsilon\|} \leq \rho}\mathcal{L}_{\text{align}}}\hspace{0pt}{({\theta + \epsilon})}},$$ |     | (4) |

where $\rho$ denotes the perturbation radius. Rather than enforcing robustness uniformly across all parameters, ShaPO  restricts adversarial perturbations to a safety-critical parameter subspace. Let $\mathcal{S} \subset {\mathbb{R}}^{d}$ denote this subspace, selective geometry control is defined as

|     |                                                                                                                                                                                                            |     |     |
|-----|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $${{\mathcal{L}_{\text{ShaPO}}\hspace{0pt}{(\theta)}} = {{\max\limits_{{\|\epsilon_{\mathcal{S}}\|} \leq \rho}\mathcal{L}_{\text{align}}}\hspace{0pt}\left( {\theta + \epsilon_{\mathcal{S}}} \right)}},$$ |     | (5) |

where $\epsilon_{\mathcal{S}}$ denotes perturbations constrained to $\mathcal{S}$. This objective enforces robustness of the alignment loss with respect to safety-critical directions.

### 3.2 Safety-critical Subspace Approximation

The safety-critical subspace $\mathcal{S}$ in Eq. ([5](#S3.E5 "Equation 5 ‣ 3.1 Optimization Objective of ShaPO ‣ 3 Selective Geometry Control for Robust Safety Alignment ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control")) is approximated using a lightweight probing-based signal that identifies directions most relevant to safety behavior. Given a representation $h \in {\mathbb{R}}^{d}$ from the residual stream of the final transformer layer, we train a linear probe $p \in {\mathbb{R}}^{d}$ by minimizing the logistic loss:

|     |                                                                                                                                                      |     |     |
|-----|------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $${{\min\limits_{p}{\mathbb{E}}_{(h,y)}}\hspace{0pt}\left\lbrack {\log\left( {1 + {\exp{({- {y{\langle{p,h}\rangle}}})}}} \right)} \right\rbrack},$$ |     | (6) |

where $y \in {\{{{+ 1},{- 1}}\}}$ indicates whether the corresponding response is labeled as safe or unsafe. The resulting probe direction captures variations in representation space that are predictive of safety behavior.

To localize safety-critical parameters, we measure the alignment between $p$ and internal parameter-induced representations. Following prior mechanistic analyses ([Lee et al., 2024](#bib.bib1)), we focus on value vectors $\{ v_{j}\}$ in transformer blocks and compute similarity scores:

|     |                                                         |     |     |
|-----|---------------------------------------------------------|-----|-----|
|     | $${s_{j} = \left| {\langle{v_{j},p}\rangle} \right|}.$$ |     | (7) |

Parameters $\theta_{\mathcal{S}} = {{TopK}{\{ v_{j}\}}}$ with the highest similarity scores define the safety-critical subspace $\mathcal{S}$ used for selective perturbation. The same probe-based Top-$K$ selection procedure is used to produce the empirical analysis shown in Figure [1](#S1.F1 "Figure 1 ‣ 1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), ensuring consistency between the motivating evidence and the selective geometry control objective. We conservatively select Top-1% neurons to cover over 90% of worst-case loss, trading slight redundancy for stability. Detailed probe training procedure and decoded results are provided in Appendix [E.1](#A5.SS1 "E.1 Linear Probe Training ‣ Appendix E Additional Experimental Results ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").

### 3.3 Instantiations of ShaPO 

Given the estimated safety-critical subspace $\mathcal{S}$, we instantiate ShaPO  by applying selective geometry control to concrete preference-based alignment objectives. The underlying principle remains the same: robustness is enforced by restricting worst-case parameter perturbations to $\mathcal{S}$, while the specific form of the alignment loss determines the level at which preferences are modeled. We consider two representative instantiations at the token and reward levels, respectively.

#### ①Token-level ShaPO .

We first instantiate ShaPO  with the token-level objectives,  such as DPO ([Rafailov et al., 2023](#bib.bib8)), rDPO ([Chowdhury et al., 2024](#bib.bib11)), Dr.DPO ([Wu et al., 2024](#bib.bib18)) and so on, which serves as a likelihood-based surrogate for preference alignment. Taking DPO loss as an example, token-level ShaPO applies selective geometry control by optimizing the worst-case DPO loss under perturbations restricted to parameters $\epsilon_{\mathcal{S}}$:

|     |              |                                                                                                                                                                                                                                                                                                       |     |     |
|-----|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $\phantom{}$ | ${\mathcal{L}_{ShaPO}\hspace{0pt}{(\theta)}} = {{\max\limits_{{\|\epsilon_{\mathcal{S}}\|}_{p} \leq \rho}\mathcal{L}_{DPO}}\hspace{0pt}{({\theta + \epsilon_{\mathcal{S}}})}}$                                                                                                                        |     | (8) |
|     |              | $= \max{}_{{\|\epsilon_{\mathcal{S}}\|}_{p} \leq \rho} - {\mathbb{E}}\log\sigma(\beta \cdot \lbrack\sum{}_{t = 1}{}^{T_{w}}\log\frac{\pi_{\theta + \epsilon_{\mathcal{S}}}\hspace{0pt}{(y_{t}^{w}\mid{x,y_{\phantom{} < t}^{w}})}}{\pi_{ref}\hspace{0pt}{(y_{t}^{w}\mid{x,y_{\phantom{} < t}^{w}})}}$ |     |     |
|     |              | $- \sum{}_{t = 1}{}^{T_{l}}\log\frac{\pi_{\theta + \epsilon_{\mathcal{S}}}\hspace{0pt}{(y_{t}^{l}\mid{x,y_{\phantom{} < t}^{l}})}}{\pi_{ref}\hspace{0pt}{(y_{t}^{l}\mid{x,y_{\phantom{} < t}^{l}})}}\rbrack),$                                                                                        |     |     |

where $T_{w}$ and $T_{l}$ denote the length of the chosen response and the rejected response. This token-level ShaPO encourages the model to remain preference-consistent under local parameter perturbations within the identified sensitive subspace.

#### ②Reward-level ShaPO .

While token-level ShaPO  improves robustness, its objective remains tied to token likelihoods, which may not faithfully reflect semantic preferences ([Yang et al., 2023](#bib.bib28); [Li et al., 2025](#bib.bib29)). To address this limitation, we introduce *reward-level ShaPO *, which applies selective geometry control to a reward-based alignment objective.

Let $R_{\phi}\hspace{0pt}{(y\mid x)}$ be a pretrained reward model that outputs a scalar preference score for response $y$ given prompt $x$. For each preference pair $(y^{w},y^{l})$, we derive a soft preference target:

|     |                                                                                                                                                                                        |     |     |
|-----|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $${{t{(x,y^{w},y^{l})}} = {\sigma\left( {\beta_{r}\hspace{0pt}\left\lbrack {{R_{\phi}\hspace{0pt}{(y^{w}\mid x)}} - {R_{\phi}\hspace{0pt}{(y^{l}\mid x)}}} \right\rbrack} \right)}},$$ |     | (9) |

where $\beta_{r}$ controls the sharpness of the reward gap. The policy predicts a preference probability:

|     |                                                                                                                                                                   |     |      |
|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|------|
|     | $${{p_{\theta}\hspace{0pt}{({y^{w} \succ y^{l}}\mid x)}} = {\sigma\left( {{s_{\theta}\hspace{0pt}{(x,y^{w})}} - {s_{\theta}\hspace{0pt}{(x,y^{l})}}} \right)}},$$ |     | (10) |

with $s_{\theta}\hspace{0pt}{(x,y)}$ denoting the model score (e.g., log-likelihood). The reward-based alignment loss is given by the binary cross-entropy:

|     |                                                                                                                                                                           |     |      |
|-----|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|------|
|     | $${{\mathcal{L}_{RM}\hspace{0pt}{(\theta)}} = {- \left\lbrack {{t\hspace{0pt}{\log p_{\theta}}} + {{({1 - t})}\hspace{0pt}{\log{({1 - p_{\theta}})}}}} \right\rbrack}}.$$ |     | (11) |

Reward-level ShaPO then enforces robustness by optimizing the worst-case reward-based loss under selective perturbations:

|     |                                                                                                                                                                                    |     |      |
|-----|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|------|
|     | $${{\mathcal{L}_{ShaPO}\hspace{0pt}{(\theta)}} = {{\max\limits_{{\|\epsilon_{\mathcal{S}}\|}_{p} \leq \rho}\mathcal{L}_{RM}}\hspace{0pt}{({\theta + \epsilon_{\mathcal{S}}})}}}.$$ |     | (12) |

#### Discussion of reward-level ShaPO .

Reward-level ShaPO offers several complementary advantages for robust alignment. First, by anchoring optimization to semantic preference signals from a pretrained reward model, the alignment objective is defined at the preference-probability level rather than token likelihoods, making it more compatible with parameter perturbations such as SAM and encouraging semantic consistency under perturbation. Second, by simulating parameter perturbations within a reward-based objective, reward-level ShaPO  establishes a structural connection between offline preference optimization and online RLHF, while remaining fully offline and avoiding costly on-policy rollouts. Third, from a data-centric perspective, the use of an external reward model can mitigate noise and ambiguity in token-level supervision, providing a complementary source of robustness under uncertain or noisy annotations.

### 3.4 Optimization Process

Given the instantiated alignment objective $\mathcal{L}_{align}\hspace{0pt}{(\theta)}$, ShaPO adopts a sharpness-aware optimization scheme inspired by SAM ([Foret et al., 2020](#bib.bib16)) to approximate locally robust solutions. The training procedure consists of two forward–backward passes. In the first pass, we compute the gradient with respect to the selected parameter subspace $\theta_{\mathcal{S}}$:

|     |                                                                                                     |     |      |
|-----|-----------------------------------------------------------------------------------------------------|-----|------|
|     | $${g_{\mathcal{S}} = {{\nabla_{\theta_{\mathcal{S}}}\mathcal{L}_{align}}\hspace{0pt}{(\theta)}}}.$$ |     | (13) |

Based on this gradient, we construct a normalized perturbation:

|     |                                                                                                               |     |      |
|-----|---------------------------------------------------------------------------------------------------------------|-----|------|
|     | $${\epsilon_{\mathcal{S}} = {\rho \cdot \frac{g_{\mathcal{S}}}{{\| g_{\mathcal{S}}\|}_{2} + \varepsilon}}},$$ |     | (14) |

where $\rho$ controls the perturbation radius and $\varepsilon$ is a small constant for numerical stability. This perturbation lies on the surface of an $L_{2}$ ball centered at $\theta_{\mathcal{S}}$.

In the second pass, the model parameters are updated by evaluating the alignment objective under the perturbed parameters:

|     |                                                                                                                                        |     |      |
|-----|----------------------------------------------------------------------------------------------------------------------------------------|-----|------|
|     | $${\theta\leftarrow{\theta - {{\eta \cdot {\nabla_{\theta}\mathcal{L}_{align}}}\hspace{0pt}{({\theta + \epsilon_{\mathcal{S}}})}}}}.$$ |     | (15) |

This two-step optimization approximates a local worst-case perturbation in the specified parameter subspace, encouraging convergence toward flatter minima with respect to $\theta_{\mathcal{S}}$. To reduce computational overhead, the sharpness-aware update is performed once every $T$ training steps rather than at every iteration. The complete training algorithm is provided in Appendix [A](#A1 "Appendix A Algorithm and Optimization Details ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").

#### Robustness Insights of ShaPO .

ShaPO optimizes the alignment loss under worst-case parameter perturbations restricted to the safety-critical subspace $\mathcal{S}$. For a differentiable alignment loss $\mathcal{L}{(\theta)}$ and sufficiently small perturbation radius $\rho$, a second-order expansion suggests:

|     |                                                                                                                                                                                                                                                                                                                           |     |
|-----|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${{\max\limits_{{\|\epsilon_{\mathcal{S}}\|} \leq \rho}{\mathcal{L}{({\theta + \epsilon_{\mathcal{S}}})}}} \approx {{\mathcal{L}{(\theta)}} + {\rho\hspace{0pt}{\|{{\nabla_{\mathcal{S}}\mathcal{L}}\hspace{0pt}{(\theta)}}\|}_{2}} + {\frac{\rho^{2}}{2}\hspace{0pt}\lambda_{\max}\hspace{0pt}{(H_{\mathcal{S}})}}}},$$ |     |

where $H_{\mathcal{S}}$ denotes the Hessian restricted to $\mathcal{S}$. This indicates that ShaPO implicitly suppresses both large alignment gradients and high curvature along safety-critical directions. Since noisy or conflicting preference supervision often induces unstable updates in these directions, selectively controlling the worst case improves the robustness of safety behavior without overly constraining capability-related parameters. Based on the previous study ([Lee et al., 2024](#bib.bib1)), we define the *bypass boundary* as the radius within which parameter perturbations do not lead to unsafe behavior. For a risk threshold $\tau$, the boundary $\delta$ satisfies:

|     |                                                                                                                                                   |     |
|-----|---------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${\delta \lesssim \sqrt{\frac{2\hspace{0pt}{({\tau - {\mathcal{L}\hspace{0pt}{(\theta)}}})}}{\lambda_{\max}\hspace{0pt}{(H_{\mathcal{S}})}}}}.$$ |     |

As ShaPO reduces the subspace curvature $\lambda_{\max}\hspace{0pt}{(H_{\mathcal{S}})}$, it effectively expands this boundary, implying stronger safety guarantees under parameter perturbations. Detailed analysis is provided in Appendix [C](#A3 "Appendix C Theoretical Insight: Detailed Proofs ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").

## 4 Experiments

In this section, we evaluate whether geometry-aware optimization improves the robustness of LLM safety alignment. We assess ShaPO under three settings: in-distribution alignment, cross-domain generalization, and robustness to noisy preference supervision. We compare ShaPO with standard preference optimization and data-centric robust methods, and conduct targeted ablations to analyze the role of selective geometry control.

|         |              |                |                |              |                |                |              |                |                |              |                |                |
|---------|--------------|----------------|----------------|--------------|----------------|----------------|--------------|----------------|----------------|--------------|----------------|----------------|
| Methods | Pythia-2.8B  |                |                | LLaMA-3.2-3B |                |                | LLaMA-3-8B   |                |                | Qwen2.5-7B   |                |                |
|         | WR$\uparrow$ | MD$\downarrow$ | NV$\downarrow$ | WR$\uparrow$ | MD$\downarrow$ | NV$\downarrow$ | WR$\uparrow$ | MD$\downarrow$ | NV$\downarrow$ | WR$\uparrow$ | MD$\downarrow$ | NV$\downarrow$ |
| Vanilla | 40.18%       | 73.31%         | 26.94%         | 44.93%       | 66.79%         | 18.42%         | 42.82%       | 67.54%         | 24.69%         | 69.09%       | 32.21%         | 13.16%         |
| SFT     | 41.05%       | 71.30%         | 26.32%         | 35.93%       | 68.67%         | 45.36%         | 23.85%       | 69.92%         | 52.51%         | 25.09%       | 70.55%         | 52.88%         |
| DPO     | 44.23%       | 57.14%         | 19.17%         | 73.70%       | 11.28%         | 6.14%          | 69.19%       | 26.57%         | 14.41%         | 75.81%       | 20.55%         | 7.27%          |
| IPO     | 45.27%       | 61.65%         | 22.68%         | 72.70%       | 11.78%         | 6.14%          | 70.22%       | 26.82%         | 13.53%         | 73.97%       | 21.30%         | 8.02%          |
| cDPO    | 45.27%       | 60.28%         | 16.92%         | 72.91%       | 25.44%         | 12.78%         | 59.48%       | 37.94%         | 23.43%         | 67.65%       | 31.83%         | 13.66%         |
| rDPO    | 46.54%       | 57.77%         | 23.43%         | 81.30%       | 4.14%          | 1.75%          | 82.13%       | 6.64%          | 3.26%          | 82.74%       | 4.51%          | 2.01%          |
| Dr.DPO  | 52.66%       | 29.95%         | 18.17%         | 83.77%       | 2.38%          | 0.50%          | 82.50%       | 4.39%          | 0.50%          | 88.93%       | 2.01%          | 0.13%          |
| ShaPO-T | 56.14%       | 15.16%         | 1.76%          | 85.88%       | 1.25%          | 0.13%          | 85.45%       | 2.76%          | 0.13%          | 89.26%       | 0.75%          | 0.13%          |
| ShaPO-R | 57.14%       | 11.40%         | 2.76%          | 85.29%       | 1.75%          | 0.50%          | 87.45%       | 1.13%          | 0.13%          | 89.23%       | 1.13%          | 0.00%          |

Table 1: Safety alignment performances on the IID setting. All methods are trained and evaluated on the PKU-SafeRLHF-30K dataset, and we report WinRate and two safety judge scores.

### 4.1 Experimental Setting

#### Benchmarks and Backbones.

We train alignment models on the PKU-SafeRLHF-30K ([Ji et al., 2023a](#bib.bib4)) dataset and evaluate the robustness of ShaPO across five safety benchmarks: PKU-SafeRLHF-30K, HH-RLHF-Safety ([Bai et al., 2022](#bib.bib5)), Do-Not-Answer ([Wang et al., 2023b](#bib.bib49)), HarmBench ([Mazeika et al., 2024](#bib.bib50)), and SaladBench ([Li et al., 2024](#bib.bib51)). These benchmarks cover diverse safety scenarios and enable evaluation of both in-distribution performance and cross-domain generalization. To assess robustness under noisy preference supervision, we follow the protocol of ([Wu et al., 2024](#bib.bib18)) and introduce controlled label flips on the training data. Models are trained on corrupted preference data while evaluated on clean validation sets, allowing us to isolate the impact of noisy supervision on alignment robustness. We conduct experiments on a diverse set of backbone models spanning different families and scales, including Pythia-2.8B ¹¹ 1 https://huggingface.co/EleutherAI/pythia-2.8b, LLaMA-3.2-3B ²² 2 https://huggingface.co/meta-llama/Llama-3.2-3B, LLaMA-3-8B ³³ 3 https://huggingface.co/meta-llama/Meta-Llama-3-8B, and Qwen2.5-7B ⁴⁴ 4 https://huggingface.co/Qwen/Qwen2.5-7B. For the implementation of reward-level ShaPO, we use a single safety-oriented preference model, PKU-Alignment/beaver-7b-v1.0-cost ⁵⁵ 5 https://huggingface.co/PKU-Alignment/beaver-7b-v1.0-cost, trained on the PKU-SafeRLHF dataset.

#### Baselines and Evaluation Metrics.

We conduct experiments on diverse LLM backbones and compare ShaPO with a set of representative preference-based alignment methods across all evaluation settings, including cross-domain generalization and robustness to noisy preference supervision. Specifically, we include the Vanilla LLM, supervised fine-tuning (SFT) ([Ouyang et al., 2022](#bib.bib26)), and Direct Preference Optimization (DPO) ([Rafailov et al., 2023](#bib.bib8)) as standard alignment baselines. In parallel, we further compare with several robust preference optimization variants designed to mitigate noise and distributional uncertainty, including IPO ([Gheshlaghi Azar et al., 2023](#bib.bib10)), cDPO ([Mitchell, 2023](#bib.bib9)), rDPO ([Chowdhury et al., 2024](#bib.bib11)), and Dr.DPO ([Wu et al., 2024](#bib.bib18)).

All baseline methods are evaluated on the following widely used safety metrics: Win Rate (WR, the higher the safer); Attack Success Rate (ASR, the lower the safer). Specifically, ASR is evaluated by two widely used safety judges: MD-Judge-v0_2-internlm2_7b (MD) ⁶⁶ 6 https://huggingface.co/OpenSafetyLab/MD-Judge-v0_2-internlm2_7b and NVIDIA Llama-3.1-Nemotron-Safety-Guard-8B-v3 ⁷⁷ 7 https://huggingface.co/nvidia/Llama-3.1-Nemotron-Safety-Guard-8B-v3. Detailed experimental settings are introduced on Appendix [D](#A4 "Appendix D Experimental Setup ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").

| Backbones  | Methods | Do-Not-Answer  |                | HarmBench      |                | HH-RLHF        |                | SaladBench     |                | AVG.   |
|------------|---------|----------------|----------------|----------------|----------------|----------------|----------------|----------------|----------------|--------|
|            |         | MD$\downarrow$ | NV$\downarrow$ | MD$\downarrow$ | NV$\downarrow$ | MD$\downarrow$ | NV$\downarrow$ | MD$\downarrow$ | NV$\downarrow$ |        |
| LLaMA-3-8B | Vanilla | 54.58%         | 12.37%         | 87.50%         | 23.50%         | 65.10%         | 19.92%         | 73.14%         | 23.26%         | 46.27% |
|            | SFT     | 53.52%         | 33.48%         | 93.50%         | 81.50%         | 69.27%         | 47.54%         | 75.10%         | 58.68%         | 64.03% |
|            | DPO     | 14.18%         | 7.78%          | 41.00%         | 28.50%         | 23.05%         | 10.30%         | 31.55%         | 19.75%         | 22.85% |
|            | IPO     | 14.29%         | 7.36%          | 33.50%         | 17.50%         | 21.70%         | 8.30%          | 30.12%         | 15.69%         | 20.42% |
|            | cDPO    | 22.39%         | 13.86%         | 61.00%         | 44.00%         | 30.32%         | 13.34%         | 42.53%         | 26.44%         | 30.7%  |
|            | rDPO    | 1.17%          | 0.53%          | 6.00%          | 1.5%           | 6.88%          | 2.25%          | 5.38%          | 2.38%          | 3.97%  |
|            | Dr.DPO  | 0.96%          | 0.00%          | 2.00%          | 0.00%          | 4.58%          | 0.37%          | 3.52%          | 0.51%          | 2.09%  |
|            | ShaPO-T | 0.43%          | 0.11%          | 0.50%          | 0.00%          | 2.94%          | 0.19%          | 2.48%          | 0.23%          | 1.37%  |
|            | ShaPO-R | 0.53%          | 0.00%          | 0.50%          | 0.00%          | 1.86%          | 0.12%          | 1.13%          | 0.08%          | 0.70%  |
| Qwen2.5-7B | Vanilla | 21.11%         | 7.78%          | 44.50%         | 27.00%         | 32.52%         | 10.76%         | 33.85%         | 13.77%         | 23.02% |
|            | SFT     | 52.67%         | 31.56%         | 95.00%         | 74.00%         | 70.54%         | 48.01%         | 73.45%         | 55.05%         | 62.37% |
|            | DPO     | 10.98%         | 4.16%          | 32.50%         | 14.00%         | 17.70%         | 4.90%          | 22.97%         | 8.63%          | 14.39% |
|            | IPO     | 10.34%         | 3.41%          | 30.50%         | 14.00%         | 18.02%         | 5.03%          | 22.16%         | 8.24%          | 14.00% |
|            | cDPO    | 16.42%         | 5.76%          | 45.50%         | 19.50%         | 26.13%         | 8.59%          | 32.56%         | 13.66%         | 21.26% |
|            | rDPO    | 1.17%          | 0.32%          | 3.00%          | 1.00%          | 6.14%          | 1.76%          | 4.23%          | 1.76%          | 3.18%  |
|            | Dr.DPO  | 0.21%          | 0.00%          | 0.50%          | 0.00%          | 2.39%          | 0.22%          | 1.53%          | 0.46%          | 1.05%  |
|            | ShaPO-T | 0.11%          | 0.00%          | 0.00%          | 0.00%          | 1.09%          | 0.12%          | 0.68%          | 0.07%          | 0.42%  |
|            | ShaPO-R | 0.00%          | 0.00%          | 0.50%          | 0.00%          | 1.31%          | 0.12%          | 0.98%          | 0.06%          | 0.55%  |

Table 2: Safety alignment performances on the domain shift setting, which were evaluated on four safety benchmarks with two judges. The reported results are conducted on LLaMA-3-8B and Qwen2.5-7B backbones.

### 4.2 In-distribution Alignment Performance

We first evaluate the alignment performance of ShaPO under the in-distribution (IID) setting on PKU-SafeRLHF-30K, with results summarized in Table [1](#S4.T1 "Table 1 ‣ 4 Experiments ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"). While our primary focus is robustness under distribution shift and noisy supervision, this experiment serves as a sanity check to verify that geometry-aware optimization does not compromise standard alignment quality. Across all backbones, ShaPO-T consistently achieves the highest or near-highest WR, while substantially reducing safety risks measured by both MD and NV judges. Compared to DPO and its data-robust variants, ShaPO-T improves WR by a clear margin on all four models, while simultaneously lowering Attack Success Rates, indicating that geometry-aware regularization does not induce overly conservative behavior. Notably, these gains are consistent across model families and scales, suggesting that the benefits of selective geometry control are not architecture-specific. ShaPO-R further improves safety metrics on larger backbones, achieving the lowest MD and NV scores on LLaMA-3-8B and Qwen2.5-7B. Although reward-level ShaPO does not optimize token-level likelihood directly, it achieves safety violation rates comparable to token-level ShaPO under clean IID supervision, while consistently outperforming DPO and Dr.DPO. This suggests that enforcing geometry control with respect to semantically grounded reward signals can be an effective alternative to token-level surrogates, without sacrificing in-domain alignment performance. Overall, these results demonstrate that geometry-aware optimization preserves, and often improves, in-distribution alignment performance while significantly enhancing safety. Importantly, the absence of a trade-off between WR and safety metrics indicates that the robustness gains observed in later experiments do not stem from degraded alignment quality under standard settings.

### 4.3 Safety robustness under domain shift

We next evaluate the robustness of ShaPO under out-of-distribution (OOD) safety benchmarks, with results reported in Table [2](#S4.T2 "Table 2 ‣ Baselines and Evaluation Metrics. ‣ 4.1 Experimental Setting ‣ 4 Experiments ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"). All models are trained on PKU-SafeRLHF-30K and evaluated on four heterogeneous safety benchmarks, including Do-Not-Answer, HarmBench, HH-RLHF, and SaladBench, which exhibit substantial distributional differences from the training data. Across both LLaMA-3-8B and Qwen2.5-7B backbones, ShaPO consistently achieves the lowest ASR across nearly all benchmarks and safety judges. Compared with standard preference optimization methods (e.g., DPO) and data-centric robust variants (IPO, cDPO, rDPO, and Dr.DPO), ShaPO-T substantially reduces ASR, indicating improved robustness to domain shift. Notably, these gains are consistent across diverse safety scenarios, suggesting that geometry-aware optimization generalizes beyond the specific characteristics of any single benchmark.

Reward-level ShaPO-R further strengthens safety robustness, achieving the lowest average ASR on both backbones. In particular, ShaPO-R consistently outperforms Dr.DPO and rDPO on challenging benchmarks such as HH-RLHF and SaladBench, where preference distributions and safety criteria differ most from the training data. This highlights the benefit of directly aligning optimization geometry with semantic preference signals at the reward level, resulting in stronger robustness under distribution shift. Overall, the OOD results demonstrate that robustness failures in safety alignment cannot be fully addressed by data-centric techniques alone. By explicitly controlling optimization geometry, ShaPO provides complementary and often larger robustness gains, leading to more stable safety behavior when deployed beyond the training distribution. To further examine robustness under more challenging settings, we report additional results on smaller backbones in Appendix [E.3](#A5.SS3 "E.3 Safety Robustness under Domain Shift ‣ Appendix E Additional Experimental Results ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").

### 4.4 Safety robustness to noisy supervision

We further evaluate the robustness of ShaPO under noisy preference supervision by introducing controlled label flips during training, while evaluating all models on clean validation data. Figure [5](#S4.F5 "Figure 5 ‣ Why selective Geometry Control. ‣ 4.5 Comprehensive Analysis of ShaPO ‣ 4 Experiments ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control") illustrates the Win Rate metric of all methods across increasing flip rates, ranging from 0% to 40%. As the noise level increases, standard preference optimization methods such as DPO exhibit a pronounced degradation, indicating high sensitivity to corrupted supervision. Data-centric robust variants mitigate this degradation to some extent; however, their performance still deteriorates notably under severe noise. In contrast, ShaPO-T consistently maintains a higher win rate across all noise levels, demonstrating improved stability under noisy supervision.

Notably, ShaPO-R achieves the strongest robustness, yielding the highest performance under all flip rates. Under severe noise (40% flipped preferences), ShaPO-R substantially outperforms both standard and data-robust baselines. This advantage stems from its use of an external reward model that provides a stable and noise-resilient supervision signal, which is decoupled from the corrupted preference labels used during training. By anchoring optimization to this independent reward signal, ShaPO-R effectively mitigates the influence of noisy human preferences and prevents error accumulation under high flip rates.

### 4.5 Comprehensive Analysis of ShaPO 

#### Composability of ShaPO.

Beyond serving as a standalone robustness mechanism, ShaPO is designed as a geometry-aware optimization framework that is complementary to existing data-centric alignment methods. To evaluate its composability, we integrate ShaPO with other data-centric alignment objectives, including DPO and its variants, and compare the resulting alignment performance. As shown in Figure [4](#S4.F4 "Figure 4 ‣ Why selective Geometry Control. ‣ 4.5 Comprehensive Analysis of ShaPO ‣ 4 Experiments ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), incorporating ShaPO consistently improves alignment robustness across different base objectives. Notably, these gains are observed on top of methods that already employ data-centric robustness strategies, indicating that geometry-aware robustness targets a distinct source of alignment fragility. Rather than replacing existing approaches, ShaPO provides additional stability by reducing sensitivity to parameter perturbations during optimization. The consistent improvements across diverse objectives suggest that robustness failures in safety alignment cannot be fully addressed by data-level interventions alone. By operating along an orthogonal optimization geometry axis, ShaPO composes naturally with data-centric techniques, yielding additive robustness gains.

Figure 3: Sensitivities to noise environments, we compare the win rate of all methods across different preference data flipping ratios (10%, 20%, 40%). The left is the results on Pythia-2.8B, and the right is on LLaMA-3.2-3B backbone.

| Geometry Control  | IID            |                | OOD (Avg.)     |                |
|-------------------|----------------|----------------|----------------|----------------|
|                   | MD$\downarrow$ | NV$\downarrow$ | MD$\downarrow$ | NV$\downarrow$ |
| No Control        | 26.57%         | 14.41%         | 28.78%         | 16.91%         |
| Random Control    | 26.89%         | 14.34%         | 28.56%         | 16.87%         |
| Uniform Control   | 25.56%         | 13.03%         | 26.83%         | 15.12%         |
| Selective Control | 27.32%         | 13.91%         | 26.31%         | 14.12%         |

Table 3: ASR comparison between uniform, random, and selective geometry control on LLaMA-3-8B. IID results are evaluated on PKU-SafeRLHF-30K, while OOD results report the average ASR across four OOD safety benchmarks.

#### Why selective Geometry Control.

Table [3](#S4.T3 "Table 3 ‣ Composability of ShaPO. ‣ 4.5 Comprehensive Analysis of ShaPO ‣ 4 Experiments ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control") systematically compares geometry control strategies — no control (degenerating to standard DPO), random, uniform, and selective — on LLaMA-3-8B with DPO loss, reporting ASR under both IID and OOD settings. This comparison isolates not whether geometry regularization helps, but where and how it should be applied. Under IID evaluation, all strategies yield comparable ASR, indicating that excessive optimization sensitivity does not manifest when training and evaluation distributions are well matched. Clear differences emerge under OOD evaluation: uniform control consistently yields higher ASR than selective control, while random control provides only marginal improvement, suggesting that unprincipled regularization fails to address the underlying sources of robustness failures. By contrast, selective geometry control achieves the lowest OOD ASR, demonstrating more reliable generalization across heterogeneous safety benchmarks.

Figure 5 illustrates how the selective neuron ratio (Top-k%) affects alignment robustness. As the ratio increases from 0.01% to 1%, ASR consistently decreases and reaches its minimum at Top-1% , indicating that a moderately sized neuron subset is sufficient to capture the most safety-critical geometric structures. Beyond this point, ASR gradually rises, suggesting that incorporating excessive neurons introduces redundant geometric information that undermines robustness. This non-monotonic trend reveals that robustness gains stem not from geometry regularization alone, but from applying it to alignment-critical directions. Uniform control suppresses both safety-critical and domain-adaptive components essential for handling distributional variation, whereas selective geometry control strikes a better balance between sharpness reduction and alignment preservation.

Figure 4: Composability of ShaPO with DPO and other data-centric alignment methods. We report the Win Rate compared with the chosen response; the left is comparisons on Pythia-2.8B, and the right is on the LLaMA-3.2-3B backbone.

![Refer to caption](2602.07340v2/plot_rebuttal_dpo.png)

Figure 5: Effect of Selective Neuron Ratio. We compare ShaPO with different selective neuron ratios on LLaMA-3-8B, and report average ASR across four OOD safety benchmarks.

#### Geometry of the Loss Landscape.

Table [4](#S4.T4 "Table 4 ‣ Geometry of the Loss Landscape. ‣ 4.5 Comprehensive Analysis of ShaPO ‣ 4 Experiments ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control") reports the maximum Hessian eigenvalue (Max HE) and win rate across methods on LLaMA-3-8B. A consistent trend emerges: as methods progress from Base to DPO, Dr.DPO, and ShaPO-T, Max HE decreases monotonically from $25.2336$ to $6.2466$, indicating progressively flatter loss landscapes along the safety subspace. Correspondingly, win rate improves from $42.82\%$ to $85.45\%$, confirming that lower curvature is associated with stronger alignment performance. These results suggest that safety alignment benefits from reducing parameter sensitivity along alignment-relevant directions, and that ShaPO-T achieves superior robustness by selectively flattening the loss geometry within this critical subspace.

| Metric   | Base    | DPO     | Dr.DPO | ShaPO-T |
|----------|---------|---------|--------|---------|
| Max HE   | 25.2336 | 14.9509 | 9.4993 | 6.2466  |
| Win Rate | 42.82%  | 69.19%  | 82.50% | 85.45%  |

Table 4: Maximum Hessian Eigenvalue (Max HE) and Win Rate across methods on LLaMA-3-8B.

|               |                |                |                |                |
|---------------|----------------|----------------|----------------|----------------|
| Methods       | IID            |                | OOD (Avg.)     |                |
|               | MD$\downarrow$ | NV$\downarrow$ | MD$\downarrow$ | NV$\downarrow$ |
| DPO           | 26.57%         | 14.41%         | 28.78%         | 16.91%         |
| DPO+Reward    | 18.42%         | 8.40%          | 17.33%         | 7.02%          |
| ShaPO-R       | 16.32%         | 7.52%          | 15.98%         | 6.26%          |
| Dr.DPO        | 4.39%          | 0.50%          | 3.72%          | 0.45%          |
| Dr.DPO+Reward | 3.38%          | 0.38%          | 2.25%          | 0.35%          |
| ShaPO-R       | 1.13%          | 0.13%          | 1.30%          | 0.09%          |

Table 5: Effect of reward supervision of ShaPO-R on LLaMA-3-8B. IID results are evaluated on PKU-SafeRLHF-30K, while OOD results report the average ASR across four OOD safety benchmarks.

#### Effect of Reward Supervision.

Table [5](#S4.T5 "Table 5 ‣ Geometry of the Loss Landscape. ‣ 4.5 Comprehensive Analysis of ShaPO ‣ 4 Experiments ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control") investigates whether ShaPO’s robustness gains stem from reward supervision or optimization geometry. We instantiate ShaPO-R under both DPO and Dr.DPO alignment objectives and conduct a controlled ablation to isolate the effect of external reward signals. Two key observations emerge: (1) Under DPO, reward supervision yields substantial improvements, and ShaPO-R further reduces ASR across all settings, demonstrating complementary benefits. (2) Under Dr.DPO, reward gains become marginal, yet ShaPO-R still achieves consistent improvements, suggesting that geometry control provides orthogonal gains beyond what data-level signals can offer. This contrast reveals a fundamental distinction: reward-based and data-centric methods(such as Dr.DPO) operate at the data level, whereas ShaPO improves robustness at the parameter level via selective geometry control. These results confirm that ShaPO’s gains are attributable to improved optimization geometry rather than stronger supervision, and that ShaPO serves as a general optimization framework that can be flexibly instantiated under diverse alignment objectives, including reward-based settings.

## 5 Conclusion

We revisit robustness in LLM safety alignment from the perspective of optimization geometry. We show that robustness failures in preference-based alignment cannot be fully explained by data uncertainty alone, and propose ShaPO, a geometry-aware preference optimization framework that selectively stabilizes alignment-critical parameter directions. By enforcing robustness where safety behavior is concentrated, ShaPO avoids the over-regularization of uniform geometry control while improving robustness under domain shift and noisy supervision. Instantiated at both token and reward levels, ShaPO consistently strengthens safety robustness and composes with data-centric methods, highlighting optimization geometry as a complementary axis for robust LLM safety alignment. While ShaPO introduces additional computational overhead due to geometry-aware optimization, improving the efficiency and scalability of such approaches remains an important direction for future work, particularly for larger-scale models. In addition, although the identification of alignment-critical directions is necessarily based on approximate signals, our results suggest that even coarse geometric cues can meaningfully improve safety robustness.

## Acknowledgements

This research/project is supported by the National Research Foundation, Singapore under its National Large Language Models Funding Initiative (AISG Award No: AISG-NMLP-2024-002), the NExT++ Research Centre and ST Engineering under a collaborative research project (Agreement No. 2024-01813), and the National Natural Science Foundation of China (Grant No. U23B2031, 62436003). Any opinions, findings and conclusions or recommendations expressed in this material are those of the author(s) and do not reflect the views of National Research Foundation, Singapore.

## Impact Statement

This work focuses on improving the robustness of safety alignment in large language models. By making preference-based alignment less sensitive to small parameter perturbations, the proposed method aims to reduce unintended unsafe behaviors under distribution shift or noisy supervision. Like other optimization techniques, the impact of this work depends on how it is applied. While the method is designed for safety alignment, similar ideas could potentially be used for other objectives. We therefore encourage using this approach in safety-oriented settings and in combination with existing responsible AI practices.

## References

- Anwar et al. (2024) U. Anwar, A. Saparov, J. Rando, D. Paleka, M. Turpin, P. Hase, E. S. Lubana, E. Jenner, S. Casper, O. Sourbut, et al. Foundational challenges in assuring alignment and safety of large language models. arXiv preprint arXiv:2404.09932. Cited by: [§1](#S1.p2.1 "1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Bahri et al. (2021) D. Bahri, H. Mobahi, and Y. Tay Sharpness-aware minimization improves language model generalization. arXiv preprint arXiv:2110.08529. Cited by: [Appendix B](#A2.p3.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Bai et al. (2023) J. Bai, S. Bai, Y. Chu, Z. Cui, K. Dang, X. Deng, Y. Fan, W. Ge, Y. Han, F. Huang, et al. Qwen technical report. arXiv preprint arXiv:2309.16609. Cited by: [Appendix B](#A2.p1.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Bai et al. (2022) Y. Bai, A. Jones, K. Ndousse, A. Askell, A. Chen, N. DasSarma, D. Drain, S. Fort, D. Ganguli, T. Henighan, et al. Training a helpful and harmless assistant with reinforcement learning from human feedback. arXiv preprint arXiv:2204.05862. Cited by: [Appendix B](#A2.p1.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [2nd item](#A4.I1.i2.p1.1 "In D.1 Benchmarks ‣ Appendix D Experimental Setup ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§2](#S2.SS0.SSS0.Px1.p1.1 "Safety Alignment via Preference Optimization. ‣ 2 Preliminaries ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§4.1](#S4.SS1.SSS0.Px1.p1.1 "Benchmarks and Backbones. ‣ 4.1 Experimental Setting ‣ 4 Experiments ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Chowdhury et al. (2024) S. R. Chowdhury, A. Kini, and N. Natarajan Provably robust dpo: aligning language models with noisy feedback. arXiv preprint arXiv:2403.00409. Cited by: [Appendix B](#A2.p2.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§D.2](#A4.SS2.p1.1 "D.2 Baseline Description ‣ Appendix D Experimental Setup ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§1](#S1.p1.1 "1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§3.3](#S3.SS3.SSS0.Px1.p1.2 "①Token-level ShaPO . ‣ 3.3 Instantiations of ShaPO ‣ 3 Selective Geometry Control for Robust Safety Alignment ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§4.1](#S4.SS1.SSS0.Px2.p1.1 "Baselines and Evaluation Metrics. ‣ 4.1 Experimental Setting ‣ 4 Experiments ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Christiano et al. (2017) P. F. Christiano, J. Leike, T. Brown, M. Martic, S. Legg, and D. Amodei Deep reinforcement learning from human preferences. Advances in neural information processing systems 30. Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Delage and Ye (2010) E. Delage and Y. Ye Distributionally robust optimization under moment uncertainty with application to data-driven problems. Operations research 58 (3), pp. 595–612. Cited by: [§2](#S2.SS0.SSS0.Px2.p1.1 "Data-uncertainty Robustness. ‣ 2 Preliminaries ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Deng et al. (2025) X. Deng, H. Zhong, R. Ai, F. Feng, Z. Wang, and X. He Less is more: improving llm alignment via preference data selection. arXiv preprint arXiv:2502.14560. Cited by: [Appendix B](#A2.p2.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Ferrand et al. (2025) J. N. Ferrand, Y. Beugin, E. Pauley, R. Sheatsley, and P. McDaniel Targeting alignment: extracting safety classifiers of aligned llms. arXiv preprint arXiv:2501.16534. Cited by: [Appendix B](#A2.p1.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Foret et al. (2020) P. Foret, A. Kleiner, H. Mobahi, and B. Neyshabur Sharpness-aware minimization for efficiently improving generalization. arXiv preprint arXiv:2010.01412. Cited by: [Appendix B](#A2.p3.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§1](#S1.p3.1 "1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§2](#S2.SS0.SSS0.Px3.p1.1 "Geometry-related Robustness. ‣ 2 Preliminaries ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§3.4](#S3.SS4.p1.1 "3.4 Optimization Process ‣ 3 Selective Geometry Control for Robust Safety Alignment ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Gao et al. (2025) C. Gao, H. Li, L. Liu, Z. Xie, P. Zhao, and Z. Xu Principled data selection for alignment: the hidden risks of difficult examples. arXiv preprint arXiv:2502.09650. Cited by: [Appendix B](#A2.p2.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§1](#S1.p2.1 "1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Gao et al. (2023) L. Gao, J. Schulman, and J. Hilton Scaling laws for reward model overoptimization. In International Conference on Machine Learning, pp. 10835–10866. Cited by: [Appendix B](#A2.p1.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Gao et al. (2024) Y. Gao, D. Alon, and D. Metzler Impact of preference noise on the alignment performance of generative language models. arXiv preprint arXiv:2404.09824. Cited by: [§1](#S1.p2.1 "1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§2](#S2.SS0.SSS0.Px2.p1.1 "Data-uncertainty Robustness. ‣ 2 Preliminaries ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Gheshlaghi Azar et al. (2023) M. Gheshlaghi Azar, M. Rowland, B. Piot, D. Guo, D. Calandriello, M. Valko, and R. Munos A general theoretical paradigm to understand learning from human preferences. arXiv e-prints, pp. arXiv–2310. Cited by: [Appendix B](#A2.p2.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§D.2](#A4.SS2.p1.1 "D.2 Baseline Description ‣ Appendix D Experimental Setup ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§1](#S1.p1.1 "1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§1](#S1.p2.1 "1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§4.1](#S4.SS1.SSS0.Px2.p1.1 "Baselines and Evaluation Metrics. ‣ 4.1 Experimental Setting ‣ 4 Experiments ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Ghorbani et al. (2019) B. Ghorbani, S. Krishnan, and Y. Xiao An investigation into neural net optimization via hessian eigenvalue density. In International Conference on Machine Learning, pp. 2232–2241. Cited by: [Appendix B](#A2.p3.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Guo et al. (2025) D. Guo, D. Yang, H. Zhang, J. Song, R. Zhang, R. Xu, Q. Zhu, S. Ma, P. Wang, X. Bi, et al. Deepseek-r1: incentivizing reasoning capability in llms via reinforcement learning. arXiv preprint arXiv:2501.12948. Cited by: [Appendix B](#A2.p1.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Huang et al. (2025) K. Huang, J. Wu, Z. Chen, X. Wang, J. Gao, B. Ding, J. Wu, X. He, and X. Wang Larger or smaller reward margins to select preferences for alignment?. arXiv preprint arXiv:2503.01864. Cited by: [Appendix B](#A2.p2.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§1](#S1.p2.1 "1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Ji et al. (2023a) J. Ji, M. Liu, J. Dai, X. Pan, C. Zhang, C. Bian, B. Chen, R. Sun, Y. Wang, and Y. Yang Beavertails: towards improved safety alignment of llm via a human-preference dataset. Advances in Neural Information Processing Systems 36, pp. 24678–24704. Cited by: [Appendix B](#A2.p1.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§2](#S2.SS0.SSS0.Px1.p1.1 "Safety Alignment via Preference Optimization. ‣ 2 Preliminaries ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§4.1](#S4.SS1.SSS0.Px1.p1.1 "Benchmarks and Backbones. ‣ 4.1 Experimental Setting ‣ 4 Experiments ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Ji et al. (2023b) J. Ji, M. Liu, J. Dai, X. Pan, C. Zhang, C. Bian, B. Chen, R. Sun, Y. Wang, and Y. Yang Beavertails: towards improved safety alignment of llm via a human-preference dataset. Advances in Neural Information Processing Systems 36, pp. 24678–24704. Cited by: [1st item](#A4.I1.i1.p1.1 "In D.1 Benchmarks ‣ Appendix D Experimental Setup ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Ji et al. (2023c) J. Ji, T. Qiu, B. Chen, B. Zhang, H. Lou, K. Wang, Y. Duan, Z. He, J. Zhou, Z. Zhang, et al. Ai alignment: a comprehensive survey. arXiv preprint arXiv:2310.19852. Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Jiang et al. (2019) Y. Jiang, B. Neyshabur, H. Mobahi, D. Krishnan, and S. Bengio Fantastic generalization measures and where to find them. arXiv preprint arXiv:1912.02178. Cited by: [§2](#S2.SS0.SSS0.Px3.p1.1 "Geometry-related Robustness. ‣ 2 Preliminaries ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Kong et al. (2024) K. Kong, X. Xu, D. Wang, J. Zhang, and M. S. Kankanhalli Perplexity-aware correction for robust alignment with noisy preferences. Advances in Neural Information Processing Systems 37, pp. 28296–28321. Cited by: [§1](#S1.p2.1 "1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Lee et al. (2024) A. Lee, X. Bai, I. Pres, M. Wattenberg, J. K. Kummerfeld, and R. Mihalcea A mechanistic understanding of alignment algorithms: a case study on dpo and toxicity. arXiv preprint arXiv:2401.01967. Cited by: [Appendix B](#A2.p1.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [Appendix B](#A2.p2.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§3.2](#S3.SS2.p2.1 "3.2 Safety-critical Subspace Approximation ‣ 3 Selective Geometry Control for Robust Safety Alignment ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§3.4](#S3.SS4.SSS0.Px1.p1.2 "Robustness Insights of ShaPO . ‣ 3.4 Optimization Process ‣ 3 Selective Geometry Control for Robust Safety Alignment ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Levy et al. (2020) D. Levy, Y. Carmon, J. C. Duchi, and A. Sidford Large-scale methods for distributionally robust optimization. Advances in neural information processing systems 33, pp. 8847–8860. Cited by: [§2](#S2.SS0.SSS0.Px2.p1.1 "Data-uncertainty Robustness. ‣ 2 Preliminaries ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Li et al. (2024) L. Li, B. Dong, R. Wang, X. Hu, W. Zuo, D. Lin, Y. Qiao, and J. Shao Salad-bench: a hierarchical and comprehensive safety benchmark for large language models. arXiv preprint arXiv:2402.05044. Cited by: [5th item](#A4.I1.i5.p1.1 "In D.1 Benchmarks ‣ Appendix D Experimental Setup ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§4.1](#S4.SS1.SSS0.Px1.p1.1 "Benchmarks and Backbones. ‣ 4.1 Experimental Setting ‣ 4 Experiments ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Li et al. (2025) M. Li, G. Huzhang, H. Zhang, X. Wang, and A. Zeng Optimal transport-based token weighting scheme for enhanced preference optimization. arXiv preprint arXiv:2505.18720. Cited by: [§3.3](#S3.SS3.SSS0.Px2.p1.1 "②Reward-level ShaPO . ‣ 3.3 Instantiations of ShaPO ‣ 3 Selective Geometry Control for Robust Safety Alignment ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Liu et al. (2026) J. Liu, Y. Yang, P. Shao, H. Ma, W. Qin, and R. Hong WDPO: winsorized direct preference optimization for robust llm alignment. arXiv preprint arXiv:2603.07211. Cited by: [Appendix B](#A2.p2.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Lu et al. (2025) H. Lu, L. Fang, R. Zhang, X. Li, J. Cai, H. Cheng, L. Tang, Z. Liu, Z. Sun, T. Wang, et al. Alignment and safety in large language models: safety mechanisms, training paradigms, and emerging challenges. arXiv preprint arXiv:2507.19672. Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Mazeika et al. (2024) M. Mazeika, L. Phan, X. Yin, A. Zou, Z. Wang, N. Mu, E. Sakhaee, N. Li, S. Basart, B. Li, et al. Harmbench: a standardized evaluation framework for automated red teaming and robust refusal. arXiv preprint arXiv:2402.04249. Cited by: [4th item](#A4.I1.i4.p1.1 "In D.1 Benchmarks ‣ Appendix D Experimental Setup ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§4.1](#S4.SS1.SSS0.Px1.p1.1 "Benchmarks and Backbones. ‣ 4.1 Experimental Setting ‣ 4 Experiments ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Meng et al. (2024) Y. Meng, M. Xia, and D. Chen Simpo: simple preference optimization with a reference-free reward. Advances in Neural Information Processing Systems 37, pp. 124198–124235. Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Mi et al. (2022) P. Mi, L. Shen, T. Ren, Y. Zhou, X. Sun, R. Ji, and D. Tao Make sharpness-aware minimization stronger: a sparsified perturbation approach. Advances in Neural Information Processing Systems 35, pp. 30950–30962. Cited by: [Appendix B](#A2.p3.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Mitchell (2023) E. Mitchell A note on dpo with noisy preferences & relationship to ipo. Cited by: [Appendix B](#A2.p2.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§D.2](#A4.SS2.p1.1 "D.2 Baseline Description ‣ Appendix D Experimental Setup ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§1](#S1.p1.1 "1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§4.1](#S4.SS1.SSS0.Px2.p1.1 "Baselines and Evaluation Metrics. ‣ 4.1 Experimental Setting ‣ 4 Experiments ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Niu et al. (2025) Y. Niu, H. Xiao, D. Liu, N. Chen, and J. Li Mitigating the safety alignment tax with null-space constrained policy optimization. arXiv preprint arXiv:2512.11391. Cited by: [§1](#S1.SS0.SSS0.Px1.p1.1 "Selective geometry control. ‣ 1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Ouyang et al. (2022) L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray, et al. Training language models to follow instructions with human feedback. Advances in neural information processing systems 35, pp. 27730–27744. Cited by: [Appendix B](#A2.p1.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§1](#S1.p1.1 "1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§2](#S2.SS0.SSS0.Px1.p1.1 "Safety Alignment via Preference Optimization. ‣ 2 Preliminaries ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§4.1](#S4.SS1.SSS0.Px2.p1.1 "Baselines and Evaluation Metrics. ‣ 4.1 Experimental Setting ‣ 4 Experiments ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Perin et al. (2025) G. J. Perin, R. Chen, X. Chen, N. S. Hirata, Z. Wang, and J. Hong Lox: low-rank extrapolation robustifies llm safety against fine-tuning. arXiv preprint arXiv:2506.15606. Cited by: [§1](#S1.SS0.SSS0.Px1.p1.1 "Selective geometry control. ‣ 1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Qi et al. (2024) X. Qi, A. Panda, K. Lyu, X. Ma, S. Roy, A. Beirami, P. Mittal, and P. Henderson Safety alignment should be made more than just a few tokens deep. arXiv preprint arXiv:2406.05946. Cited by: [§1](#S1.p2.1 "1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Rafailov et al. (2023) R. Rafailov, A. Sharma, E. Mitchell, C. D. Manning, S. Ermon, and C. Finn Direct preference optimization: your language model is secretly a reward model. Advances in Neural Information Processing Systems 36, pp. 53728–53741. Cited by: [Appendix B](#A2.p1.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§D.2](#A4.SS2.p1.1 "D.2 Baseline Description ‣ Appendix D Experimental Setup ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§1](#S1.SS0.SSS0.Px2.p1.1 "Multi-level instantiations. ‣ 1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§1](#S1.p1.1 "1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§2](#S2.SS0.SSS0.Px1.p1.1 "Safety Alignment via Preference Optimization. ‣ 2 Preliminaries ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§3.3](#S3.SS3.SSS0.Px1.p1.2 "①Token-level ShaPO . ‣ 3.3 Instantiations of ShaPO ‣ 3 Selective Geometry Control for Robust Safety Alignment ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§4.1](#S4.SS1.SSS0.Px2.p1.1 "Baselines and Evaluation Metrics. ‣ 4.1 Experimental Setting ‣ 4 Experiments ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Raghavendra et al. (2024) M. Raghavendra, V. Nath, and S. Hendryx Revisiting the superficial alignment hypothesis. arXiv preprint arXiv:2410.03717. Cited by: [Appendix B](#A2.p2.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Roy et al. (2025) A. Roy, J. Patel, A. Chadha, V. Jain, and A. Das AlignMerge-alignment-preserving large language model merging via fisher-guided geometric constraints. arXiv preprint arXiv:2512.16245. Cited by: [Appendix B](#A2.p3.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Shao et al. (2026) P. Shao, N. Zhai, L. Chen, Y. Yang, F. Zhu, X. Yang, and M. Wang Baldro: a distributionally robust optimization based framework for large language model unlearning. In Proceedings of the ACM Web Conference 2026, pp. 8874–8884. Cited by: [Appendix B](#A2.p2.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Shao et al. (2024) Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang, Y. Li, Y. Wu, et al. Deepseekmath: pushing the limits of mathematical reasoning in open language models. arXiv preprint arXiv:2402.03300. Cited by: [Appendix B](#A2.p1.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Wang et al. (2023a) F. Wang, P. Xu, W. Ruan, and X. Huang Towards verifying the geometric robustness of large-scale neural networks. In Proceedings of the AAAI conference on artificial intelligence, Vol. 37, pp. 15197–15205. Cited by: [§1](#S1.p3.1 "1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Wang et al. (2023b) Y. Wang, H. Li, X. Han, P. Nakov, and T. Baldwin Do-not-answer: a dataset for evaluating safeguards in llms. arXiv preprint arXiv:2308.13387. Cited by: [3rd item](#A4.I1.i3.p1.1 "In D.1 Benchmarks ‣ Appendix D Experimental Setup ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§4.1](#S4.SS1.SSS0.Px1.p1.1 "Benchmarks and Backbones. ‣ 4.1 Experimental Setting ‣ 4 Experiments ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Wei et al. (2024) B. Wei, K. Huang, Y. Huang, T. Xie, X. Qi, M. Xia, P. Mittal, M. Wang, and P. Henderson Assessing the brittleness of safety alignment via pruning and low-rank modifications. arXiv preprint arXiv:2402.05162. Cited by: [Appendix B](#A2.p1.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [Appendix B](#A2.p2.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§1](#S1.SS0.SSS0.Px1.p1.1 "Selective geometry control. ‣ 1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§1](#S1.p2.1 "1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§2](#S2.SS0.SSS0.Px2.p1.1 "Data-uncertainty Robustness. ‣ 2 Preliminaries ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Wu et al. (2024) J. Wu, Y. Xie, Z. Yang, J. Wu, J. Chen, J. Gao, B. Ding, X. Wang, and X. He Towards robust alignment of language models: distributionally robustifying direct preference optimization. arXiv preprint arXiv:2407.07880. Cited by: [Appendix B](#A2.p2.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§D.2](#A4.SS2.p1.1 "D.2 Baseline Description ‣ Appendix D Experimental Setup ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§1](#S1.p2.1 "1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§2](#S2.SS0.SSS0.Px2.p1.2 "Data-uncertainty Robustness. ‣ 2 Preliminaries ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§3.3](#S3.SS3.SSS0.Px1.p1.2 "①Token-level ShaPO . ‣ 3.3 Instantiations of ShaPO ‣ 3 Selective Geometry Control for Robust Safety Alignment ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§4.1](#S4.SS1.SSS0.Px1.p1.1 "Benchmarks and Backbones. ‣ 4.1 Experimental Setting ‣ 4 Experiments ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§4.1](#S4.SS1.SSS0.Px2.p1.1 "Baselines and Evaluation Metrics. ‣ 4.1 Experimental Setting ‣ 4 Experiments ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Xie et al. (2026) J. Xie, Y. Yang, P. Shao, and L. Wu Sharpness-aware poisoning: enhancing transferability of injective attacks on recommender systems. IEEE Transactions on Knowledge and Data Engineering. Cited by: [Appendix B](#A2.p3.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Xu et al. (2026) Z. Xu, S. Vemuri, K. Panaganti, D. Kalathil, R. Jain, and D. Ramachandran Robust llm alignment via distributionally robust direct preference optimization. Advances in Neural Information Processing Systems 38, pp. 27039–27076. Cited by: [Appendix B](#A2.p2.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Yang et al. (2023) S. Yang, S. Zhang, C. Xia, Y. Feng, C. Xiong, and M. Zhou Preference-grounded token-level guidance for language model fine-tuning. Advances in Neural Information Processing Systems 36, pp. 24466–24496. Cited by: [§3.3](#S3.SS3.SSS0.Px2.p1.1 "②Reward-level ShaPO . ‣ 3.3 Instantiations of ShaPO ‣ 3 Selective Geometry Control for Robust Safety Alignment ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Yeh and Li (2025) S. Yeh and S. Li Clean first, align later: benchmarking preference data cleaning for reliable llm alignment. arXiv preprint arXiv:2509.23564. Cited by: [§1](#S1.p2.1 "1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Yun (2025) J. Yun Sharpness-aware minimization with z-score gradient filtering for neural networks. arXiv preprint arXiv:2505.02369. Cited by: [Appendix B](#A2.p3.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Zhang et al. (2025) Y. Zhang, G. Xiong, H. Li, and W. Zhao EDGE: efficient data selection for llm agents via guideline effectiveness. arXiv preprint arXiv:2502.12494. Cited by: [Appendix B](#A2.p2.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Zhao et al. (2025a) X. Zhao, W. Cai, T. Shi, D. Huang, L. Lin, S. Mei, and D. Song Improving llm safety alignment with dual-objective optimization. arXiv preprint arXiv:2503.03710. Cited by: [Appendix B](#A2.p1.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Zhao et al. (2025b) Y. Zhao, W. Zhang, Y. Xie, A. Goyal, K. Kawaguchi, and M. Shieh Understanding and enhancing safety mechanisms of llms via safety-specific neuron. In The Thirteenth International Conference on Learning Representations, Cited by: [§1](#S1.SS0.SSS0.Px1.p1.1 "Selective geometry control. ‣ 1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Zhong et al. (2022) Q. Zhong, L. Ding, L. Shen, P. Mi, J. Liu, B. Du, and D. Tao Improving sharpness-aware minimization with fisher mask for better generalization on language models. arXiv preprint arXiv:2210.05497. Cited by: [Appendix B](#A2.p3.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Zhu et al. (2025a) M. Zhu, Y. Liu, J. Guo, Q. Wang, Y. Zhang, and Z. Mao Leveraging robust optimization for llm alignment under distribution shifts. arXiv preprint arXiv:2504.05831. Cited by: [Appendix B](#A2.p2.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§1](#S1.p2.1 "1 Introduction ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"), [§2](#S2.SS0.SSS0.Px2.p1.2 "Data-uncertainty Robustness. ‣ 2 Preliminaries ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Zhu et al. (2024) X. Zhu, B. Zhu, Y. Tan, S. Wang, Y. Hao, and H. Zhang Selective vision-language subspace projection for few-shot CLIP. In ACM Multimedia, pp. 3848–3857. Cited by: [Appendix B](#A2.p3.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").
- Zhu et al. (2025b) X. Zhu, B. Zhu, S. Wang, K. Zhao, and H. Zhang Enhancing CLIP robustness via cross-modality alignment. CoRR abs/2510.24038. Cited by: [Appendix B](#A2.p2.1 "Appendix B Related Works ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").

## Appendix A Algorithm and Optimization Details

0:  Preference dataset $\mathcal{D} = {\{{(x_{i},y_{i}^{w},y_{i}^{l})}\}}_{i = 1}^{N}$, and probe training dataset $\mathcal{D}_{p} = {\{{(x_{i},y_{i})}\}}_{i = 1}^{M}$; initial policy model $\pi_{\theta}$, reference $\pi_{ref}$, reward model $\mathcal{R}_{\phi}$ (only for reward-level ShaPO); hyper-parameters: learning rate $\eta$, batch size $B$, SAM frequency $\tau$, radius $\rho$, top fraction $r$.

0:  Aligned policy model $\pi_{\theta}^{\star}$.

1:  Step 0: Safety-Critical Neuron Identification

2:  Train probe $\mathbf{p}$ on $\mathcal{D}_{p}$ via Cross-Entropy Minimization;

3:  Compute similarity score $s_{j} = {|{\langle{v_{j},\mathbf{p}}\rangle}|}$ for all dimensions of value vector for each transformer block;

4:  $S\leftarrow\phantom{}$ indices of Top fraction w.r.t. $s_{j}$.

5:  for $t = 1$ to $T$ do

6:   Sample mini-batch $\mathcal{B} \subset \mathcal{D}$ of size $B$.

7:   Step 1: Gradient on Safety Subspace

8:   $g_{\mathcal{S}}\leftarrow{{\nabla_{\theta_{\mathcal{S}}}\mathcal{L}_{align}}\hspace{0pt}{(\theta,\mathcal{B})}}$.

9:   Step 2: Adversarial Perturbation (SAM-style)

10:   $\epsilon_{\mathcal{S}}\leftarrow{{\rho \cdot g_{\mathcal{S}}}/\left( {{\| g_{\mathcal{S}}\|}_{2} + 10^{- 12}} \right)}$.

11:   $\theta^{\prime}\leftarrow{\theta + \epsilon_{\mathcal{S}}}$ {only $\mathcal{S}$ perturbed}

12:   Step 3: Robust Update

13:   if ${t\operatorname{mod}\tau} = 0$ then

14:    $\nabla_{\theta}\leftarrow{{\nabla_{\theta}\mathcal{L}_{align}}\hspace{0pt}\left( \theta^{\prime},\mathcal{B} \right)}$.

15:    $\theta\leftarrow{\theta - {\eta\hspace{0pt}\nabla_{\theta}}}$.

16:   else

17:    $\nabla_{\theta}\leftarrow{{\nabla_{\theta}\mathcal{L}_{align}}\hspace{0pt}(\theta,\mathcal{B})}$.

18:    $\theta\leftarrow{\theta - {\eta\hspace{0pt}\nabla_{\theta}}}$.

19:   end if

20:  end for

21:  return $\theta^{\star}\leftarrow\theta$.

Algorithm 1 ShaPO:  Sharpness-aware Preference Optimization

## Appendix B Related Works

Preference-based Safety Alignment. Safety alignment aims to ensure that language models avoid generating harmful or unsafe outputs beyond general instruction-following ability ([Ouyang et al., 2022](#bib.bib26); [Ji et al., 2023a](#bib.bib4)). A dominant paradigm is post-training with human or model preferences, where models are optimized to favor safe responses over unsafe ones. Early approaches such as Reinforcement Learning from Human Feedback (RLHF) ([Bai et al., 2022](#bib.bib5); [Bai et al., 2023](#bib.bib3)) rely on reward modeling and policy optimization, which incur high computational costs and can be sensitive to noisy supervision ([Gao et al., 2023](#bib.bib17)). To simplify the pipeline, Direct Preference Optimization (DPO) ([Rafailov et al., 2023](#bib.bib8)) reframes safety alignment as supervised learning on preference pairs, achieving competitive instruction-following and safety behaviors without explicit reward models or reinforcement learning. Building on this paradigm, recent work explores alternative formulations including group-relative or multi-objective optimization ([Shao et al., 2024](#bib.bib6); [Guo et al., 2025](#bib.bib7); [Zhao et al., 2025a](#bib.bib45)), as well as methods that explicitly target or extract safety-relevant decision boundaries within aligned models ([Ferrand et al., 2025](#bib.bib46); [Lee et al., 2024](#bib.bib1)). Despite rapid progress, preference-based safety alignment methods still exhibit limited generalization under distribution shifts or adversarial prompts ([Wei et al., 2024](#bib.bib38)), raising concerns about robustness in real-world deployments.

Data-centric Robust Safety Alignment. Recent studies show that post-training paradigms for safety alignment often achieve only shallow robustness and rely on shortcut learning, leading to brittle behavior under distribution shift or adversarial prompting ([Wei et al., 2024](#bib.bib38); [Raghavendra et al., 2024](#bib.bib2); [Lee et al., 2024](#bib.bib1); [Zhu et al., 2025b](#bib.bib56)). To address these issues, a growing body of work improves robustness from the data and supervision perspective under noisy, biased, or unreliable preference signals. One line develops *robust preference objectives* that explicitly model supervision uncertainty, including margin-based or calibrated formulations ([Gheshlaghi Azar et al., 2023](#bib.bib10); [Mitchell, 2023](#bib.bib9)), noise-aware optimization ([Chowdhury et al., 2024](#bib.bib11)), and distributionally robust extensions (e.g., Dr.DPO ([Wu et al., 2024](#bib.bib18)), WDPO, KLDPO ([Xu et al., 2026](#bib.bib24)), DoRA ([Zhu et al., 2025a](#bib.bib15)) and BalDRO ([Shao et al., 2026](#bib.bib53))). Another line explores *data selection and filtering* strategies using reward margins ([Deng et al., 2025](#bib.bib13); [Huang et al., 2025](#bib.bib31)), external guidance ([Zhang et al., 2025](#bib.bib12)), learned criteria ([Gao et al., 2025](#bib.bib14)) and implicit margins ([Liu et al., 2026](#bib.bib55)). While effective at mitigating noise and bias in supervision, these approaches primarily address robustness at the data level and implicitly assume stable optimization dynamics in parameter space, leaving parameter-space robustness largely unexplored.

Geometry-based Robust Optimization. Beyond data uncertainty, the robustness and generalization of neural networks are also shaped by optimization geometry, such as sharpness and sensitivity to parameter perturbations ([Foret et al., 2020](#bib.bib16); [Bahri et al., 2021](#bib.bib19); [Xie et al., 2026](#bib.bib54)). Prior work in supervised learning has shown that controlling worst-case loss in a neighborhood of the parameters can improve robustness, often by favoring flatter regions of the loss landscape. These geometry-based approaches typically apply uniform control across the parameter space, implicitly assuming isotropic sensitivity. However, recent analyses indicate that parameter sensitivity is highly anisotropic, with loss variations concentrating along a small subset of directions ([Ghorbani et al., 2019](#bib.bib23); [Mi et al., 2022](#bib.bib22); [Zhong et al., 2022](#bib.bib20); [Yun, 2025](#bib.bib21); [Zhu et al., 2024](#bib.bib57)). For example, researchers have introduced Fisher-guided geometry in model merging ([Roy et al., 2025](#bib.bib47)). Despite this, geometry-based robustness has not been systematically explored in preference-based safety alignment. In this setting, optimization-induced sensitivity can amplify residual noise or distribution shift in preference supervision. Our work addresses this gap by introducing geometry-aware robustness into preference optimization, selectively stabilizing alignment-critical parameter directions rather than enforcing uniform flatness.

## Appendix C Theoretical Insight: Detailed Proofs

### C.1 PAC-Bayes Generalization Bound of ShaPO

We present a concise proof of Theorem 1, establishing the PAC-Bayesian generalization bound for ShaPO.

#### Setup.

Let $\mathcal{L}_{D}\hspace{0pt}{(\theta)}$ and $\mathcal{L}_{S}\hspace{0pt}{(\theta)}$ denote the population and empirical alignment losses, respectively. We decompose parameters as $\theta = {(\theta_{S},\theta_{R})}$, where $\theta_{S}$ corresponds to alignment-sensitive directions and $\theta_{R}$ to residual parameters. Assume that: (i) ${\ell{({f_{\theta}\hspace{0pt}{(x)}},y)}} \in {\lbrack{0,1}\rbrack}$; (ii) $\mathcal{L}_{S}$ is $L_{R}$-Lipschitz with respect to $\theta_{R}$; (iii) the alignment loss is locally convex in $\theta_{S}$ within radius $\rho$.

#### PAC-Bayes framework.

For any prior $P$ and posterior $Q$ on perturbations $\epsilon = {(\epsilon_{S},\epsilon_{R})}$, the standard PAC-Bayes inequality for bounded losses gives, with probability at least $1 - \delta$:

|     |                                                                                                                  |                                                                                                                                        |     |
|-----|------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | ${\mathbb{E}}_{\epsilon \sim Q}\hspace{0pt}{\lbrack{\mathcal{L}_{D}\hspace{0pt}{({\theta + \epsilon})}}\rbrack}$ | $\phantom{} \leq {{{\mathbb{E}}_{\epsilon \sim Q}\hspace{0pt}{\lbrack{\mathcal{L}_{S}\hspace{0pt}{({\theta + \epsilon})}}\rbrack}} +}$ |     |
|     |                                                                                                                  | $\sqrt{\frac{{KL}(Q \parallel P) + \ln(1/\delta)}{2\hspace{0pt}n}}.$                                                                   |     |

We consider $Q$ supported on the subspace ball ${{B_{S}\hspace{0pt}{(\rho)}} \times B_{R}}\hspace{0pt}{(\rho_{R})}$. Applying the Lipschitz condition in $\theta_{R}$ yields:

|     |                                         |                                                                                                                                                        |     |
|-----|-----------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $\mathcal{L}_{D}\hspace{0pt}{(\theta)}$ | $\phantom{} \leq {{{\max\limits_{{\|\epsilon_{S}\|} \leq \rho}\mathcal{L}_{S}}\hspace{0pt}{({\theta + \epsilon_{S}})}} + {L_{R}\hspace{0pt}\rho_{R}}}$ |     |
|     |                                         | ${+ \sqrt{\frac{{KL}(Q \parallel P) + \ln(1/\delta)}{2\hspace{0pt}n}}}.$                                                                               |     |

#### Bounding the KL term.

Under a local Laplace approximation ${\mathcal{L}_{S}\hspace{0pt}{({\theta + \epsilon_{S}})}} \approx {{\mathcal{L}_{S}\hspace{0pt}{(\theta)}} + {\frac{1}{2}\hspace{0pt}\epsilon_{S}^{\top}\hspace{0pt}H_{S}\hspace{0pt}{(\theta)}\hspace{0pt}\epsilon_{S}}}$, choosing Gaussian prior $P = {\mathcal{N}{(0,{\sigma^{- 2}\hspace{0pt}I})}}$ and posterior $Q = {\mathcal{N}{(0,{({H_{S} + {\sigma^{- 2}\hspace{0pt}I}})}^{- 1})}}$ gives

|     |                                                                                                                          |     |
|-----|--------------------------------------------------------------------------------------------------------------------------|-----|
|     | ${KL}{(Q \parallel P)} \approx \frac{1}{2}\log\det{(I + \sigma^{2}H_{S})} \leq$                                          |     |
|     | ${\frac{1}{2}\hspace{0pt}d_{S}\hspace{0pt}{\log{({1 + {\sigma^{2}\hspace{0pt}\lambda_{\max}\hspace{0pt}{(H_{S})}}})}}}.$ |     |

Then, we have:

|     |                                                                                                                                                                                                                                                 |     |
|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | ${{{\mathcal{L}_{D}\hspace{0pt}{(\theta)}} - {\mathcal{L}_{S}\hspace{0pt}{(\theta)}}} = {{O\left( \sqrt{\frac{d_{S}\hspace{0pt}{\log{({1 + {\sigma^{2}\hspace{0pt}\lambda_{\max}\hspace{0pt}{(H_{S})}}})}}}{n}}) \right.} + \varepsilon_{R}}},$ |     |

where $\varepsilon_{R} = {L_{R}\hspace{0pt}\rho_{R}}$ accounts for non-sensitive parameters. At a local optimum, the subspace sharpness:

|     |                             |                                                                                                                                                                                                    |     |      |
|-----|-----------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|------|
|     | ${sharpness}{(\theta_{S})}$ | $\phantom{} = {\max\limits_{{\|\epsilon_{S}\|} \leq \rho}\left\lbrack {{\mathcal{L}_{align}\hspace{0pt}{({\theta + \epsilon_{S}})}} - {\mathcal{L}_{align}\hspace{0pt}{(\theta)}}} \right\rbrack}$ |     |      |
|     |                             | ${\phantom{} \approx {\frac{1}{2}\hspace{0pt}\rho^{2}\hspace{0pt}\lambda_{\max}\hspace{0pt}{(H_{S})}}}.$                                                                                           |     | (16) |

Finally, we obtain the generalization bound of ShaPO :

|     |                                                                                                                                                                                                                              |     |
|-----|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | ${{{\mathcal{L}_{D}\hspace{0pt}{(\theta)}} - {\mathcal{L}_{S}\hspace{0pt}{(\theta)}}} = {{O\left( \sqrt{\frac{d_{S}\hspace{0pt}{sharpness}\hspace{0pt}{(\theta_{S})}}{\rho^{2}\hspace{0pt}n}} \right)} + \varepsilon_{R}}},$ |     |

which formally explains how minimizing subspace sharpness improves the generalization ability of ShaPO.

### C.2 Bypass Boundary Expansion

We now justify the robustness result in Eq. (20) of the main text.

#### Local risk approximation.

At a stationary point ${{\nabla\mathcal{L}_{align}}\hspace{0pt}{(\theta)}} \approx 0$, a second-order Taylor expansion gives

|     |                                                                            |                                                                                                                                                                                                      |     |
|-----|----------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $\mathcal{L}_{align}\hspace{0pt}{({\theta + {\Delta\hspace{0pt}\theta}})}$ | $\phantom{} \approx {{\mathcal{L}_{align}\hspace{0pt}{(\theta)}} + {\frac{1}{2}\hspace{0pt}\Delta\hspace{0pt}\theta^{\top}\hspace{0pt}H\hspace{0pt}{(\theta)}\hspace{0pt}\Delta\hspace{0pt}\theta}}$ |     |
|     |                                                                            | ${\phantom{} \leq {{\mathcal{L}_{align}\hspace{0pt}{(\theta)}} + {\frac{1}{2}\hspace{0pt}\lambda_{\max}\hspace{0pt}{(H)}\hspace{0pt}{\|{\Delta\hspace{0pt}\theta}\|}^{2}}}}.$                        |     |

#### Bypass boundary.

Let $\tau$ be the safety threshold. To guarantee ${\mathcal{L}_{align}\hspace{0pt}{({\theta + {\Delta\hspace{0pt}\theta}})}} \leq \tau$ for all ${\|{\Delta\hspace{0pt}\theta}\|} \leq \delta$, it suffices that

|     |     |                                                                                                                                                         |     |
|-----|-----|---------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     |     | ${{{\mathcal{L}_{align}\hspace{0pt}{(\theta)}} + {\frac{1}{2}\hspace{0pt}\lambda_{\max}\hspace{0pt}{(H)}\hspace{0pt}\delta^{2}}} \leq \tau},$           |     |
|     |     | ${{\Rightarrow\quad\delta} \leq \sqrt{\frac{2\hspace{0pt}{({\tau - {\mathcal{L}_{align}\hspace{0pt}{(\theta)}}})}}{\lambda_{\max}\hspace{0pt}{(H)}}}}.$ |     |

Since ShaPO reduces $\lambda_{\max}\hspace{0pt}{(H_{S})}$ by flattening the alignment loss in subspace $\theta_{S}$, it enlarges the feasible bypass radius $\delta$, providing stronger robustness to parameter perturbations.

## Appendix D Experimental Setup

### D.1 Benchmarks

We evaluate safety alignment robustness across multiple benchmarks spanning diverse safety domains. These benchmarks differ in task formulation, harm taxonomy, and distributional characteristics, allowing us to assess both in-distribution safety performance and robustness under domain shift or adversarial prompts. Below, we summarize the covered safety domains, benchmark characteristics, and evaluation protocols.

- •
  PKU-SafeRLHF-30K ([Ji et al., 2023b](#bib.bib30)) ⁸⁸ 8 https://huggingface.co/datasets/PKU-Alignment/PKU-SafeRLHF-30K: This benchmark consists of preference pairs annotated for safety, and is commonly used for training and evaluating preference-based safety alignment. We use its held-out split to measure in-distribution safety performance, reporting attack success rates under standard evaluation prompts.
- •
  HH-RLHF-Safety ([Bai et al., 2022](#bib.bib5)) ⁹⁹ 9 https://huggingface.co/datasets/asparius/antropic-hh-rlhf_sft: It’s derived from the Anthropic HH-RLHF dataset, this benchmark focuses on the trade-off between helpfulness and harmlessness. It evaluates whether models appropriately refuse unsafe instructions while maintaining alignment with benign user intent.
- •
  Do-Not-Answer ([Wang et al., 2023b](#bib.bib49)) ¹⁰¹⁰ 10 https://huggingface.co/datasets/LibrAI/do-not-answer: This benchmark evaluates abstention behavior, measuring whether models correctly refuse to answer queries that should not be responded to. It emphasizes refusal precision under clearly unsafe requests.
- •
  HarmBench ([Mazeika et al., 2024](#bib.bib50)) ¹¹¹¹ 11 https://huggingface.co/datasets/walledai/HarmBench: HarmBench consists of adversarially constructed prompts designed to induce harmful responses across multiple categories. It tests robustness to malicious intent and prompt-based attacks beyond the training distribution.
- •
  SaladBench ([Li et al., 2024](#bib.bib51)) ¹²¹² 12 https://huggingface.co/datasets/walledai/SaladBench: SaladBench focuses on compositional and obfuscated harms, where unsafe intent is embedded within multi-step or indirect queries. This benchmark evaluates whether models can maintain safety under more subtle or context-dependent threat scenarios.

### D.2 Baseline Description

We compare ShaPO against representative preference-based alignment methods from the DPO family, including DPO ([Rafailov et al., 2023](#bib.bib8)), cDPO ([Mitchell, 2023](#bib.bib9)), IPO ([Gheshlaghi Azar et al., 2023](#bib.bib10)), rDPO ([Chowdhury et al., 2024](#bib.bib11)), and Dr.DPO ([Wu et al., 2024](#bib.bib18)). These methods differ in how they model preference uncertainty and robustness, while sharing a common preference-optimization framework. Specifically, DPO serves as the standard baseline that directly optimizes the policy without an explicit reward model. cDPO and rDPO improve robustness to noisy preference labels via conservative or noise-aware objectives, respectively. IPO adopts an alternative preference-learning formulation without binary classification, while Dr.DPO incorporates distributional robustness into the DPO objective. All baselines are implemented using their original formulations and evaluated under the same training and evaluation settings for fair comparison.

### D.3 Implementation Details

For all preference-based optimization methods, we set the common hyperparameter $\beta = 0.1$ and the learning rate ${l\hspace{0pt}r} = {5 \times 10^{- 7}}$. For Dr.DPO, an additional hyperparameter $\beta^{\prime}$ is set to $1.0$ as recommended in the original paper. For our proposed ShaPO, we set the SAM optimization frequency $\tau = 5$ for both variants. For the reward-level ShaPO variant, we additionally set $\beta_{r} = 10$. For evaluation, WR is assessed using the GPT-4.1-mini API with temperature set to 0.7 to ensure consistent and reliable preference judgments. ASR is assessed using MD-Judge and NV-Judge, with decoding parameters set to temperature$\phantom{} = 0.0$ and top_p$\phantom{} = 1.0$ during inference.

| Method     | Pythia-2.8B | LLaMA-3.2-3B | LLaMA-3-8B | Qwen-2.5-7B |
|------------|-------------|--------------|------------|-------------|
| DPO Series | 16 mins     | 18 mins      | 46 mins    | 44 mins     |
| ShaPO-T    | 21 mins     | 24 mins      | 89 mins    | 85 mins     |
| ShaPO-R    | 30 mins     | 35 mins      | 99 mins    | 95 mins     |

Table 6: Running time comparison between DPO-series baselines and our proposed ShaPO variants across different backbone models.

Computation Resources. All experiments are conducted on NVIDIA H100 GPUs with the following configurations: for Pythia-2.8B and LLaMA-3.2-3B, we use 2 GPUs with a batch size of 128, and for LLaMA-3-8B and Qwen2.5-7B, we use 2 GPUs with a batch size of 32. For all settings, each global batch is formed by 2 micro-batches (i.e., gradient accumulation steps = 2). All methods share the same batch size and training epochs to ensure fair comparison. Here, we report the running time comparisons between DPO and ShaPO in Table [6](#A4.T6 "Table 6 ‣ D.3 Implementation Details ‣ Appendix D Experimental Setup ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").

Figure 6: Reward-score distribution on the PKU-30K training set and the effect of different $\beta_{r}$ on score normalization. Left: the raw score difference ${\Delta\hspace{0pt}r} = {{r{(x,y^{w})}} - {r{(x,y^{l})}}}$ produced by the Beaver reward (negated cost) model on preference pairs. Right three: the corresponding sigmoid-transformed values $\sigma{({\beta_{r}\hspace{0pt}\Delta\hspace{0pt}r})}$ under $\beta_{r} \in \left\{ {0.1,1,10} \right\}$.

#### Reward Model Usage.

In our reward-level ShaPO approach, we use a single safety-oriented preference model, PKU-Alignment/beaver-7b-v1.0-cost, trained on the PKU-SafeRLHF dataset. Although it is released as a *cost* model (where higher scores indicate more harmful outputs), we use it as a reward model by negating its outputs so that higher values correspond to more harmless responses. The resulting scalar reward signal is directly integrated into the ShaPO optimization objective, enabling explicit reward-level guidance during policy alignment. Therefore, we further analyze the reward signal on the PKU-30K training set: the distribution of the reward-score differences, as well as the resulting sigmoid-transformed distributions under different $\beta_{r}$, are shown in Figure [6](#A4.F6 "Figure 6 ‣ D.3 Implementation Details ‣ Appendix D Experimental Setup ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control").

## Appendix E Additional Experimental Results

### E.1 Linear Probe Training

#### Probe Accuracy.

We trained a linear safety classifier on the PKU-30k dataset, utilizing the “harmless” metric as the ground truth. In our implementation, the backbone language model remains frozen. We extract the residual stream representations from the final Transformer layer to serve as inputs for the linear classifier. Given a representation $h \in {\mathbb{R}}^{d}$ and a binary safety label $y \in {\{{0,1}\}}$, the probe is optimized via a standard cross-entropy objective. We define the probe direction as $p = {w_{1} - w_{0}}$, where $w_{1}$ and $w_{0}$ represent the class weights of the linear detector. Subsequently, we traverse the value vector to calculate the cosine similarity between each neuron and the probe vector. The top-$K$ neurons with the highest similarity scores are selected to form the safety parameter subspace.

Figure 7: Probe training performance (Loss and Accuracy) across ten epochs for four different backbone models: Pythia-2.8B, LLaMA-3.2-3B, LLaMA-3-8B, and Qwen2.5-7B.

#### Probe Decoding.

Table [7](#A5.T7 "Table 7 ‣ Probe Decoding. ‣ E.1 Linear Probe Training ‣ Appendix E Additional Experimental Results ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control") presents the Top-20 decoded tokens associated with the trained probes across four different large language model backbones. For each backbone, we decode the tokens that are most strongly activated by the corresponding probe, which provides insight into the lexical patterns and semantic cues captured during probe training.

| Model        |  Probe to Tokens                                                                                                                                                                |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Pythia-2.8B  |  unmist, hypocr, bastard, stad, Warning, hesis, warning, illeg, WO, ilis, %"}, heading, WARRANT, Processor, hurry, pretext, culo, ubation, untu, justification                  |
| LLaMA-3.2-3B |  Fuck, Fuck, fuck, hypocrisy, misogyn, \_stub, fuck, dum, dumpsters, fucks, immoral, hypoc, clums, fucked, cuck, blowjob, FUCK, Pressure, looph, weakest                        |
| LLaMA-3-8B   |  linger, Specifier, ORK, ÄĽn, .scalablytyped, reesome, LOPT, ijo, fucks, stup, èŃľ, 404, akov, alim, ÐºÐ¾Ð³, imir, reich, VOID, stub, /common                                   |
| Qwen-2.5-7B  |  juana, æīĢæľīæĥ$\hslash$èĬĤ, åıªè¦ģæľī, æ¬£æ$\hslash$°, orf, \_DIGEST, .desktop, culo, âĬĶ, Stealth, xbe, unprotected, ÐºÑĢÐ¾Ð², roleName, káº», .Apis, ä½ģ, blackColor, cont  |

Table 7: Decoded top-20 tokens from the trained probes across four LLM backbones.

### E.2 Training Reward Margin

We report the training-time margin dynamics of both baseline methods and our approach across different LLM backbones, as shown in Figure [8](#A5.F8 "Figure 8 ‣ E.2 Training Reward Margin ‣ Appendix E Additional Experimental Results ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control"). Overall, the proposed ShaPO family consistently exhibits the strongest margin growth while remaining compatible with the best-performing baselines, suggesting that selective geometry control effectively enhances preference separation.

Figure 8: Comparison of training reward margins across different methods on four LLM backbones.

### E.3 Safety Robustness under Domain Shift

In addition to the main results on larger backbones (Table 2), we evaluate safety alignment performance on smaller models, where limited capacity often leads to more brittle safety behaviors and higher attack success rates. Table [8](#A5.T8 "Table 8 ‣ E.3 Safety Robustness under Domain Shift ‣ Appendix E Additional Experimental Results ‣ Revisiting Robustness for LLM Safety Alignment via Selective Geometry Control") reports attack success rates (ASR) across four safety benchmarks, evaluated by two independent safety judges. Several consistent observations emerge. First, preference-based alignment methods substantially reduce ASR compared to vanilla and SFT baselines, confirming the effectiveness of preference optimization for safety alignment. Second, data-centric robust objectives such as IPO, cDPO, rDPO, and Dr.DPO further improve safety performance on some benchmarks, but their gains are often inconsistent across judges and datasets. In contrast, ShaPO exhibits consistently low ASR across all benchmarks and both judges, indicating strong robustness to evaluation variance. Notably, ShaPO achieves large absolute reductions in ASR on smaller backbones such as Pythia-2.8B, where safety alignment is typically more challenging, while also maintaining near-zero ASR on stronger models such as LLaMA-3.2-3B. Finally, the close performance of ShaPO-T and ShaPO-R suggests that selective geometry control is robust to the specific choice of safety-critical subspace estimator, supporting the stability of the proposed approach. Overall, these results demonstrate that constraining parameter-space sensitivity leads to reliable safety improvements beyond data-centric robustness alone.

| Backbones    | Methods | Do-Not-Answer  |                | HarmBench      |                | HH-RLHF        |                | Salad Bench    |                | AVG.   |
|--------------|---------|----------------|----------------|----------------|----------------|----------------|----------------|----------------|----------------|--------|
|              |         | MD$\downarrow$ | NV$\downarrow$ | MD$\downarrow$ | NV$\downarrow$ | MD$\downarrow$ | NV$\downarrow$ | MD$\downarrow$ | NV$\downarrow$ |        |
| Pythia-2.8B  | Vallina | 59.70%         | 18.34%         | 86.00%         | 29.50%         | 72.02%         | 24.95%         | 78.95%         | 29.69%         | 52.30% |
|              | SFT     | 62.26%         | 18.44%         | 81.00%         | 28.00%         | 72.21%         | 25.75%         | 79.05%         | 30.23%         | 52.68% |
|              | DPO     | 46.26%         | 14.50%         | 65.00%         | 15.00%         | 58.82%         | 21.06%         | 63.60%         | 20.79%         | 41.21% |
|              | IPO     | 44.99%         | 16.52%         | 73.00%         | 16.50%         | 59.49%         | 22.78%         | 64.55%         | 22.74%         | 42.58% |
|              | cDPO    | 47.55%         | 13.33%         | 76.00%         | 14.50%         | 60.33%         | 18.08%         | 67.61%         | 19.24%         | 41.90% |
|              | rDPO    | 39.23%         | 14.29%         | 55.50%         | 17.00%         | 55.19%         | 21.95%         | 60.45%         | 20.94%         | 39.67% |
|              | Dr.DPO  | 16.42%         | 9.81%          | 25.50%         | 10.00%         | 29.35%         | 19.94%         | 30.27%         | 18.24%         | 23.90% |
|              | ShaPO-T | 6.72%          | 0.43%          | 10.50%         | 1.50%          | 14.14%         | 1.67%          | 14.02%         | 1.65%          | 7.71%  |
|              | ShaPO-R | 5.01%          | 0.64%          | 11.50%         | 0.50%          | 12.39%         | 2.72%          | 11.70%         | 2.00%          | 6.91%  |
| LLaMA-3.2-3B | Vallina | 52.45%         | 11.30%         | 85.00%         | 26.50%         | 67.61%         | 18.89%         | 74.17%         | 22.32%         | 46.46% |
|              | SFT     | 51.71%         | 27.72%         | 89.50%         | 73.00%         | 66.93%         | 38.67%         | 74.28%         | 50.58%         | 59.27% |
|              | DPO     | 5.01%          | 2.03%          | 14.00%         | 4.00%          | 12.12%         | 5.45%          | 11.31%         | 6.13%          | 8.58%  |
|              | IPO     | 3.73%          | 1.71%          | 17.00%         | 6.00%          | 12.10%         | 5.26%          | 11.12%         | 6.07%          | 8.45%  |
|              | cDPO    | 11.51%         | 5.54%          | 65.50%         | 15.00%         | 24.55%         | 10.67%         | 26.65%         | 13.29%         | 19.12% |
|              | rDPO    | 1.17%          | 0.64%          | 3.50%          | 1.00%          | 5.92%          | 2.02%          | 4.19%          | 1.97%          | 3.27%  |
|              | Dr.DPO  | 1.07%          | 0.00%          | 2.00%          | 0.50%          | 2.57%          | 0.34%          | 1.78%          | 0.33%          | 1.20%  |
|              | ShaPO-T | 0.11%          | 0.11%          | 1.50%          | 0.00%          | 1.75%          | 0.23%          | 1.21%          | 0.25%          | 0.59%  |
|              | ShaPO-R | 0.75%          | 0.00%          | 0.50%          | 0.00%          | 2.09%          | 0.33%          | 1.59%          | 0.3%           | 0.99%  |

Table 8: Safety alignment performances on the domain shift setting, which were evaluated on four safety benchmarks with two judges. The reported results are conducted on Pythia-2.8B and LLaMA-3.2-3B backbones.

Experimental support, please [view the build logs](./2602.07340v2/__stdout.txt) for errors. Generated by [ L A T E xml ![\[LOGO\]](img)](https://math.nist.gov/~BMiller/LaTeXML/) .

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
