---
title: "Tamper-Resistant Safeguards for Open-Weight LLMs"
authors: "Rishub Tamirisa et al."
year: 2024
source: https://arxiv.org/html/2408.00761v4
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

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) [![](img) Report Issue](# "Report an Issue") [![](img) Back to Abstract](/abs/2408.00761v4 "Back to abstract page") [![](img) Download PDF](/pdf/2408.00761v4 "Download PDF") [![](img)](javascript:toggleNavTOC(); "Toggle navigation") [![](img)](javascript:toggleReadingMode(); "Disable reading mode, show header and footer")

![](img) ![](img) ![](img)

1.  [Abstract](#abstract1 "In Tamper-Resistant Safeguards for Open-Weight LLMs")
2.  [1 Introduction](#S1 "In Tamper-Resistant Safeguards for Open-Weight LLMs")
3.  [2 Related Work](#S2 "In Tamper-Resistant Safeguards for Open-Weight LLMs")
    1.  [Adversarial attacks on LLMs.](#S2.SS0.SSS0.Px1 "In 2 Related Work ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
    2.  [LLM safeguards.](#S2.SS0.SSS0.Px2 "In 2 Related Work ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
    3.  [Robust safeguards.](#S2.SS0.SSS0.Px3 "In 2 Related Work ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
4.  [3 Tamper-Resistant Safeguards](#S3 "In Tamper-Resistant Safeguards for Open-Weight LLMs")
    1.  [3.1 Threat Model](#S3.SS1 "In 3 Tamper-Resistant Safeguards ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
    2.  [3.2 Problem Definition and Metrics](#S3.SS2 "In 3 Tamper-Resistant Safeguards ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        1.  [Weaponization knowledge restriction.](#S3.SS2.SSS0.Px1 "In 3.2 Problem Definition and Metrics ‣ 3 Tamper-Resistant Safeguards ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        2.  [Harmful request refusal.](#S3.SS2.SSS0.Px2 "In 3.2 Problem Definition and Metrics ‣ 3 Tamper-Resistant Safeguards ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
    3.  [3.3 Red Teaming](#S3.SS3 "In 3 Tamper-Resistant Safeguards ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
5.  [4 Safeguard Tamper-Resistance Training](#S4 "In Tamper-Resistant Safeguards for Open-Weight LLMs")
    1.  [4.1 Model Safeguarding](#S4.SS1 "In 4 Safeguard Tamper-Resistance Training ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
    2.  [4.2 Tamper-Resistance Training](#S4.SS2 "In 4 Safeguard Tamper-Resistance Training ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        1.  [Impeding the adversary’s loss.](#S4.SS2.SSS0.Px1 "In 4.2 Tamper-Resistance Training ‣ 4 Safeguard Tamper-Resistance Training ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        2.  [Tamper-resistance objective.](#S4.SS2.SSS0.Px2 "In 4.2 Tamper-Resistance Training ‣ 4 Safeguard Tamper-Resistance Training ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
6.  [5 Experiments](#S5 "In Tamper-Resistant Safeguards for Open-Weight LLMs")
    1.  [5.1 Weaponization Knowledge Restriction](#S5.SS1 "In 5 Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        1.  [Setup.](#S5.SS1.SSS0.Px1 "In 5.1 Weaponization Knowledge Restriction ‣ 5 Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        2.  [Baselines.](#S5.SS1.SSS0.Px2 "In 5.1 Weaponization Knowledge Restriction ‣ 5 Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        3.  [Results.](#S5.SS1.SSS0.Px3 "In 5.1 Weaponization Knowledge Restriction ‣ 5 Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
    2.  [5.2 Harmful Request Refusal](#S5.SS2 "In 5 Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        1.  [Setup.](#S5.SS2.SSS0.Px1 "In 5.2 Harmful Request Refusal ‣ 5 Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        2.  [Baselines.](#S5.SS2.SSS0.Px2 "In 5.2 Harmful Request Refusal ‣ 5 Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        3.  [Results.](#S5.SS2.SSS0.Px3 "In 5.2 Harmful Request Refusal ‣ 5 Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
    3.  [5.3 Analysis](#S5.SS3 "In 5 Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        1.  [Red teaming.](#S5.SS3.SSS0.Px1 "In 5.3 Analysis ‣ 5 Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
7.  [6 Conclusion](#S6 "In Tamper-Resistant Safeguards for Open-Weight LLMs")
    1.  [Acknowledgements.](#S6.SS0.SSS0.Px1 "In 6 Conclusion ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
8.  [References](#bib "In Tamper-Resistant Safeguards for Open-Weight LLMs")
9.  [A Limitations](#A1 "In Tamper-Resistant Safeguards for Open-Weight LLMs")
10. [B Author Contributions](#A2 "In Tamper-Resistant Safeguards for Open-Weight LLMs")
11. [C Method Details](#A3 "In Tamper-Resistant Safeguards for Open-Weight LLMs")
    1.  [C.1 Note on Updated Implementation](#A3.SS1 "In Appendix C Method Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
    2.  [C.2 Initial Weaponization Knowledge Restriction Safeguard](#A3.SS2 "In Appendix C Method Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
    3.  [C.3 Designing the Tamper-resistance Loss](#A3.SS3 "In Appendix C Method Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        1.  [Weaponization knowledge restriction.](#A3.SS3.SSS0.Px1 "In C.3 Designing the Tamper-resistance Loss ‣ Appendix C Method Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        2.  [Harmful request refusal.](#A3.SS3.SSS0.Px2 "In C.3 Designing the Tamper-resistance Loss ‣ Appendix C Method Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
    4.  [C.4 Efficiently Sampling Fine-tuning Attacks](#A3.SS4 "In Appendix C Method Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
    5.  [C.5 Implementation Details and Resource Requirements](#A3.SS5 "In Appendix C Method Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
12. [D Additional Analysis Experiments](#A4 "In Tamper-Resistant Safeguards for Open-Weight LLMs")
    1.  [D.1 Benign Fine-Tuning](#A4.SS1 "In Appendix D Additional Analysis Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
    2.  [D.2 Targeted Patching of Vulnerabilities](#A4.SS2 "In Appendix D Additional Analysis Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
    3.  [D.3 Test-time Generalization Experiments](#A4.SS3 "In Appendix D Additional Analysis Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        1.  [Generalization to stronger test-time attacks.](#A4.SS3.SSS0.Px1 "In D.3 Test-time Generalization Experiments ‣ Appendix D Additional Analysis Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        2.  [Varying the TAR inner-loop length $K$.](#A4.SS3.SSS0.Px2 "In D.3 Test-time Generalization Experiments ‣ Appendix D Additional Analysis Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
    4.  [D.4 Ablations](#A4.SS4 "In Appendix D Additional Analysis Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        1.  [Including the initial safeguard.](#A4.SS4.SSS0.Px1 "In D.4 Ablations ‣ Appendix D Additional Analysis Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        2.  [Excluding the initial safeguard.](#A4.SS4.SSS0.Px2 "In D.4 Ablations ‣ Appendix D Additional Analysis Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        3.  [Varying the tamper-resistance loss scale $\lambda_{\text{TR}}$.](#A4.SS4.SSS0.Px3 "In D.4 Ablations ‣ Appendix D Additional Analysis Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
    5.  [D.5 DPO Tamper-Resistance during TAR](#A4.SS5 "In Appendix D Additional Analysis Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
13. [E Experiment Details](#A5 "In Tamper-Resistant Safeguards for Open-Weight LLMs")
    1.  [E.1 Weaponization Domain Proxy Dataset Details](#A5.SS1 "In Appendix E Experiment Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        1.  [Biosecurity.](#A5.SS1.SSS0.Px1 "In E.1 Weaponization Domain Proxy Dataset Details ‣ Appendix E Experiment Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        2.  [Chemical Security.](#A5.SS1.SSS0.Px2 "In E.1 Weaponization Domain Proxy Dataset Details ‣ Appendix E Experiment Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        3.  [Cybersecurity.](#A5.SS1.SSS0.Px3 "In E.1 Weaponization Domain Proxy Dataset Details ‣ Appendix E Experiment Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
    2.  [E.2 Train-time Settings and Adversaries](#A5.SS2 "In Appendix E Experiment Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        1.  [Weaponization knowledge restriction.](#A5.SS2.SSS0.Px1 "In E.2 Train-time Settings and Adversaries ‣ Appendix E Experiment Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        2.  [Harmful request refusal.](#A5.SS2.SSS0.Px2 "In E.2 Train-time Settings and Adversaries ‣ Appendix E Experiment Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
14. [F Red Teaming Details](#A6 "In Tamper-Resistant Safeguards for Open-Weight LLMs")
    1.  [F.1 Weaponization Knowledge Restriction](#A6.SS1 "In Appendix F Red Teaming Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
    2.  [F.2 Harmful Request Refusal](#A6.SS2 "In Appendix F Red Teaming Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        1.  [F.2.1 Additional Harmful Request Refusal Results](#A6.SS2.SSS1 "In F.2 Harmful Request Refusal ‣ Appendix F Red Teaming Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
15. [G Baseline Details](#A7 "In Tamper-Resistant Safeguards for Open-Weight LLMs")
    1.  [G.1 Weaponization Knowledge Restriction](#A7.SS1 "In Appendix G Baseline Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        1.  [Max Entropy.](#A7.SS1.SSS0.Px1 "In G.1 Weaponization Knowledge Restriction ‣ Appendix G Baseline Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        2.  [Min Posterior.](#A7.SS1.SSS0.Px2 "In G.1 Weaponization Knowledge Restriction ‣ Appendix G Baseline Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        3.  [RMU.](#A7.SS1.SSS0.Px3 "In G.1 Weaponization Knowledge Restriction ‣ Appendix G Baseline Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        4.  [LLMU.](#A7.SS1.SSS0.Px4 "In G.1 Weaponization Knowledge Restriction ‣ Appendix G Baseline Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        5.  [Hyperparameter tuning.](#A7.SS1.SSS0.Px5 "In G.1 Weaponization Knowledge Restriction ‣ Appendix G Baseline Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
    2.  [G.2 Harmful Request Refusal](#A7.SS2 "In Appendix G Baseline Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        1.  [Representation Rerouting.](#A7.SS2.SSS0.Px1 "In G.2 Harmful Request Refusal ‣ Appendix G Baseline Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        2.  [R2D2.](#A7.SS2.SSS0.Px2 "In G.2 Harmful Request Refusal ‣ Appendix G Baseline Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        3.  [RepNoise.](#A7.SS2.SSS0.Px3 "In G.2 Harmful Request Refusal ‣ Appendix G Baseline Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
    3.  [G.3 Additional Baseline Comparisons](#A7.SS3 "In Appendix G Baseline Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        1.  [MLAC-AR.](#A7.SS3.SSS0.Px1 "In G.3 Additional Baseline Comparisons ‣ Appendix G Baseline Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")
        2.  [SOPHON-AR.](#A7.SS3.SSS0.Px2 "In G.3 Additional Baseline Comparisons ‣ Appendix G Baseline Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")

[License: CC BY 4.0](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2408.00761v4 \[cs.LG\] 10 Feb 2025

# Tamper-Resistant Safeguards for Open-Weight LLMs

Rishub Tamirisa^($\dagger$) Affiliation: Lapis Labs Affiliation: University of Illinois Urbana-Champaign Affiliation: Center for AI Safety    Bhrugu Bharathi Affiliation: Lapis Labs Affiliation: University of California, San Diego      
Long Phan Affiliation: Center for AI Safety    Andy Zhou Affiliation: Lapis Labs Affiliation: University of Illinois Urbana-Champaign    Alice Gatti Affiliation: Center for AI Safety    Tarun Suresh Affiliation: Lapis Labs Affiliation: University of Illinois Urbana-Champaign      
Maxwell Lin Affiliation: Gray Swan AI    Justin Wang Affiliation: Carnegie Mellon University Affiliation: Gray Swan AI    Rowan Wang Affiliation: Harvard University Affiliation: Gray Swan AI    Ron Arel Affiliation: Lapis Labs Affiliation: University of Illinois Urbana-Champaign      
Andy Zou Affiliation: Carnegie Mellon University Affiliation: Gray Swan AI Affiliation: Center for AI Safety    Dawn Song Affiliation: University of California, Berkeley    Bo Li Affiliation: University of Illinois Urbana-Champaign Affiliation: University of Chicago    Dan Hendrycks^($\ddagger$) Affiliation: Center for AI Safety    Mantas Mazeika^($\ddagger$) Affiliation: University of Illinois Urbana-Champaign Affiliation: Center for AI Safety

###### Abstract

Rapid advances in the capabilities of large language models (LLMs) have raised widespread concerns regarding their potential for malicious use. Open-weight LLMs present unique challenges, as existing safeguards lack robustness to tampering attacks that modify model weights. For example, recent works have demonstrated that refusal and unlearning safeguards can be trivially removed with a few steps of fine-tuning. These vulnerabilities necessitate new approaches for enabling the safe release of open-weight LLMs. We develop a method, called TAR, for building tamper-resistant safeguards into open-weight LLMs such that adversaries cannot remove the safeguards even after hundreds of steps of fine-tuning. In extensive evaluations and red teaming analyses, we find that our method greatly improves tamper-resistance while preserving benign capabilities. Our results demonstrate that progress on tamper-resistance is possible, opening up a promising new avenue to improve the safety and security of open-weight LLMs.

¹¹footnotetext: Equal contribution. ^(‡)Equal advising. Correspondence to [rishubt2@illinois.edu](mailto:rishubt2@illinois.edu).²²footnotetext: Part of work done during an internship at the Center for AI Safety.

## 1 Introduction

The most capable open-weight large language models (LLMs) released over the past year now rival closed-source frontier models \[[34](#bib.bib34)\]. The availability of open-weight LLMs for anyone to download and use has yielded numerous benefits, including lowering costs for end users and enabling academic research on safety and security \[[72](#bib.bib72)\]. However, as these models become increasingly powerful, many have raised concerns that they could be repurposed by malicious actors to cause harm, motivating research on how to safeguard these models against malicious use.

Existing open-weight models often adapt safeguards designed for closed-weight models served through APIs \[[55](#bib.bib55)\]. These safeguards include refusal mechanisms and preference-based training, and they have provided substantial robustness against input-based jailbreaking attacks. However, recent work has demonstrated these safeguards are trivially defeated by attacks that edit model weights, breaking down after only a handful of fine-tuning steps \[[44](#bib.bib44)\]. This poses a serious problem for open-weight models, because adversaries have full access to model weights and can tamper with built-in safeguards.

The vulnerability of open-weight models to tampering attacks poses risks for model developers as well. Under background tort law, AI developers must exercise reasonable care, meaning they have an obligation to take reasonable precautions to prevent foreseeable harm. If malicious actors can easily customize models to cause critical harm, model developers may inadvertently violate reasonable care standards and become open to liability under existing law. Thus, there is an urgent need for more robust safeguarding techniques that can withstand tampering attacks.

In this work, we study the problem of tamper-resistant safeguards for LLMs. This problem is depicted in Figure [1](#S1.F1 "Figure 1 ‣ 1 Introduction ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"). Unlike existing research on LLM safeguards, we focus on attacks that modify model weights, which we refer to as tampering attacks. This problem has been considered very challenging and by some intractable, as no method has yet provided substantial robustness to these attacks. However, making progress on this problem would provide a valuable tool to regulators and model developers by ameliorating the dual-use dilemma of open-weight models \[[40](#bib.bib40)\].

To demonstrate that progress on this problem is possible, we develop the first LLM safeguards that obtain strong robustness against a wide variety of tampering attacks. Our approach allows developers to add a safeguard such that tampering attacks cannot easily remove the safeguard, while preserving the general capabilities of the LLM. We achieve this by performing adversarial training against tampering attacks, leveraging approaches from meta-learning. We identify various crucial factors that enable our method to work, including the choice of tamper-resistance loss, the selection of train-time adversaries, and the two-stage approach that we use for building in safeguards.

Figure 1: An illustration comparing two approaches to LLM safety when subjected to adversarial fine-tuning. The top branch shows conventional safeguards (like refusal training), which can be easily bypassed when adversaries fine-tune the model weights to remove safety constraints. The bottom branch demonstrates our proposed method TAR(Tampering Attack Resistance), which maintains robustness even when adversaries attempt to fine-tune the model to reintroduce harmful capabilities.

We apply our method to develop tamper-resistant unlearning and refusal safeguards. In experiments, we demonstrate that our safeguards are far more robust to tampering attacks than prior methods. We stress-test our safeguards with extensive red teaming evaluations against $26$ test-time adversaries, demonstrating resistance to fine-tuning attacks of hundreds of steps. We hope our results foster future work on this important problem. Our experiment code and models are available at [https://github.com/rishub-tamirisa/tamper-resistance](https://github.com/rishub-tamirisa/tamper-resistance).

## 2 Related Work

##### Adversarial attacks on LLMs.

Due to the extensive pre-training distribution of modern LLMs, they are prone to generating harmful content \[[38](#bib.bib38), [52](#bib.bib52)\]. To mitigate this, many LLMs undergo fine-tuning to implement safeguards \[[3](#bib.bib3), [42](#bib.bib42), [55](#bib.bib55)\], using methods such as reinforcement learning from human feedback (RLHF) \[[7](#bib.bib7), [43](#bib.bib43)\] and direct preference optimization (DPO) \[[46](#bib.bib46)\]. While effective for normal use, these safeguards have been shown to be brittle, breaking down under jailbreak attacks \[[25](#bib.bib25), [58](#bib.bib58), [74](#bib.bib74)\] or a handful of fine-tuning steps on “uncensored” data \[[44](#bib.bib44), [62](#bib.bib62), [67](#bib.bib67)\]. This suggests current techniques for LLM alignment are inadequate, raising security concerns after deployment.

Figure 2: Comparison of our TAR method to $12$ baseline safeguards. Unlike prior methods, TAR provides far greater tamper-resistance at similar levels of general capability, measured via MMLU. Tamper-resistance is computed as the normalized error on WMDP Biosecurity, Chemical Security, and Cybersecurity questions \[[31](#bib.bib31)\], averaged across up to $26$ fine-tuning attacks.

##### LLM safeguards.

Since the discovery of these attacks, many safeguards have been proposed to defend against them. Against jailbreak attacks, defenses include system-level defenses \[[23](#bib.bib23), [24](#bib.bib24), [49](#bib.bib49), [65](#bib.bib65), [71](#bib.bib71)\] that modify or filter model inputs or outputs and model-level defenses such as adversarial training \[[37](#bib.bib37)\]. Alternatively, some works explore machine unlearning as a way to remove harmful knowledge entirely with techniques such as influence functions \[[2](#bib.bib2), [28](#bib.bib28)\], maximizing loss on forget sets \[[11](#bib.bib11), [63](#bib.bib63), [64](#bib.bib64)\], or modifying representations \[[4](#bib.bib4), [31](#bib.bib31), [53](#bib.bib53), [59](#bib.bib59)\]. However, jailbreaking defenses are not fully robust to adaptive adversaries \[[26](#bib.bib26), [33](#bib.bib33)\], and existing unlearning methods are not robust to adversaries with access to model weights \[[36](#bib.bib36)\].

##### Robust safeguards.

Several works have explored the tamper-resistance of unlearning methods for image classification \[[14](#bib.bib14), [15](#bib.bib15), [54](#bib.bib54)\]. For bidirectional BERT-style models, [Henderson et al. \[16\]](#bib.bib16) proposed a meta-learning approach for robustly preventing models from learning harmful tasks. In concurrent work, [Deng et al. \[10\]](#bib.bib10) proposed a method extending this approach to small-scale vision classifiers and diffusion models. Recently, [Liu et al. \[32\]](#bib.bib32) discussed the potential for robust unlearning in LLMs to improve the safety of open-source models, and [Lynch et al. \[36\]](#bib.bib36) proposed evaluation metrics for robust unlearning in LLMs. To the best of our knowledge, no methods have been proposed for autoregressive LLMs that are robust to tampering attacks.

Several concurrent works have explored ways of defending LLM refusal mechanisms against fine-tuning \[[20](#bib.bib20), [22](#bib.bib22), [21](#bib.bib21), [50](#bib.bib50), [51](#bib.bib51)\]. [Huang et al. \[22\]](#bib.bib22) add a perturbation loss to make an LLM learn to produce embeddings that are more invariant to perturbations, [Rosati et al. \[50\]](#bib.bib50) maximize prediction loss on harmful generations while minimizing loss on refusals, and [Rosati et al. \[51\]](#bib.bib51) regularize harmful representations to look random. Unfortunately, these works evaluate against small sets of fine-tuning adversaries or have limited robustness. We corroborate this in our comparisons, finding that the approaches in the latter two works lack robustness to the tampering attacks in our evaluations.

## 3 Tamper-Resistant Safeguards

### 3.1 Threat Model

We assume the defender releases an LLM with weights $\theta_{G}$ and a safeguard $G$ applied. The defender’s goal is to design $G$ such that $\theta_{G}$ obtains high values on $\text{safety\_metric}\hspace{0pt}{(\theta_{G})}$ and $\text{capabilities\_metric}\hspace{0pt}{(\theta_{G})}$. Moreover, the defender seeks to preserve a high value of $\text{safety\_metric}\hspace{0pt}{(\theta_{G})}$ after the adversary’s move. We consider a compute-bounded adversary with unrestricted access to $\theta_{G}$, enabling attacks that directly modify $\theta_{G}$. We refer to these as “tampering attacks.” The adversary’s goal is to obtain a model $\theta_{G}^{\prime}$ that minimizes the safety metric given reasonable compute limits, such as fine-tuning for $500$ steps. We note that in this work, we focus solely on fine-tuning adversaries and not input-space “jailbreaking” adversaries. We assume the adversary will not spend a significant fraction of the compute required to pre-train the LLM, since at that point they could train their own model without safeguards.

### 3.2 Problem Definition and Metrics

We describe a general notation for quantifying the tamper-resistance of safeguards. Define $G$, $\theta_{G}$, safety_metric, and capabilities_metric as in the threat model. Let attack denote a compute-bounded adversarial attack that maps $\theta_{G}$ to $\theta_{G}^{\prime}$, with stronger attacks obtaining lower values of $\text{safety\_metric}\hspace{0pt}{(\theta_{G}^{\prime})}$. We say that a safeguard $G$ is tamper-resistant if its post-attack $\text{safety\_metric}\hspace{0pt}{(\theta_{G}^{\prime})}$ is high across a broad range of strong test-time adversarial attacks $\mathcal{A}_{\text{test}}$.

Note that $\theta_{G}$ often modifies an underlying $\theta$ that lacks safeguards, often through a fine-tuning procedure. Additionally, strong tamper-resistance can be obtained if the safeguard simply overwrites $\theta$ with noise, but this model would no longer be useful. Thus, maintaining a high $\text{capabilities\_metric}\hspace{0pt}{(\theta_{G})}$ is crucial, and evaluation of a safeguard must consider both its tamper-resistance and how well it preserves general capabilities.

We focus on two common safeguard domains: weaponization knowledge restriction and harmful request refusal. In each domain, we define safety and capabilities test metrics, which we use alongside test-time adversaries to evaluate tamper-resistant safeguards.

##### Weaponization knowledge restriction.

In weaponization knowledge restriction, safeguards prevent the model from producing text about weaponization knowledge, while preserving capabilities for benign knowledge domains. Existing safeguards of this nature include representation engineering methods like circuit breaking \[[75](#bib.bib75)\]. The safety_metric is defined as error on a forget set, and the capabilities_metric is defined as accuracy on a retain set. Specifically, we consider the problem of restricting biosecurity, chemical security, and cybersecurity knowledge, and evaluate the resulting model on the Weapons of Mass Destruction Proxy (WMDP) benchmark \[[31](#bib.bib31)\]. WMDP contains $3,668$ multiple-choice questions, spanning biosecurity, chemical security, and cybersecurity knowledge. Importantly, WMDP questions do not evaluate hazardous knowledge directly, but instead measure proxy expert-level knowledge for each hazardous domain, such that restricting the expert-level knowledge would also restrict the hazardous knowledge. We define the forget set as the respective hazardous knowledge subject in WMDP, and retain set as the complement of the given subject in MMLU \[[17](#bib.bib17)\], a multi-task question-answering benchmark spanning 57 tasks across a variety of knowledge domains.

##### Harmful request refusal.

In the harmful request refusal setting, safeguards prevent the model from producing “harmful” outputs. We define the safety_metric as the complement of average Attack Success Rate (ASR) of various jailbreaking attacks, while the capabilities_metric captures the conversational abilities of $\theta_{G}$. Specifically, we use a static set of test cases from HarmBench, an automated red-teaming framework for measuring prompt jailbreak robustness in LLMs, to evaluate jailbreak ASR \[[37](#bib.bib37)\] after tampering attacks. We use MT-Bench, a multi-turn question-answering benchmark graded by an LLM judge, to evaluate conversational abilities \[[69](#bib.bib69)\].

### 3.3 Red Teaming

To properly measure the robustness of tamper-resistant safeguards, we conduct red-teaming with up to $26$ adversaries, including many that are unseen at training time. In our evaluations, we subject our method to adversaries with varying compute budgets, access to held-out datasets, and diverse hyperparameters. For fine-tuning adversaries, we vary the learning rate, learning rate scheduler, optimization algorithm, and batch size. Many of these adversaries were fixed during early experiments, with some added over time as we found attacks that broke intermediate versions of our method. Extensive stress testing of this nature is critical for obtaining confidence in a tamper-resistant safeguard. For research on developing these safeguards, extensive red teaming also allows measuring incremental progress, using the number and strength of existing attacks one can defend against as a robustness metric.

 Input: Initial LLM parameters $\theta$, train-time adversary set $\mathcal{A}_{\text{train}}$, capabilities_metric proxy dataset $\mathcal{D}_{\text{retain}}$, safety_metric proxy dataset $\mathcal{D}_{\text{TR}}$, outer steps $N$, learning rate $\eta$, number of sampled adversaries $K$, tamper-resistance loss scale $\lambda_{\text{TR}}$, retain loss scale $\lambda_{\text{retain}}$, $h_{\theta}\hspace{0pt}{( \cdot )}$ returns the residual stream hidden states for model parameters $\theta$

 $\theta_{0}\leftarrow{\text{Apply Initial Safeguard to~}\hspace{0pt}\theta}$

 for $i = 1$ to $N$ do

  $g_{\text{TR}}\leftarrow 0$ \# For accumulating tamper-resistance gradient

  Sample $x_{\text{TR}} \sim \mathcal{D}_{\text{TR}}$

  for $k = 1$ to $K$ do

   Sample $\text{attack} \sim \mathcal{A}_{\text{train}}$

   \# Tamper-resistance loss from Equation [1](#S4.E1 "Equation 1 ‣ Tamper-resistance objective. ‣ 4.2 Tamper-Resistance Training ‣ 4 Safeguard Tamper-Resistance Training ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")

   $g_{\text{TR}}\leftarrow{g_{\text{TR}} + {\frac{1}{K}\hspace{0pt}{\nabla_{\theta_{i - 1}}\mathcal{L}_{\text{TR}}}\hspace{0pt}{({\text{attack}\hspace{0pt}{(\theta_{i - 1})}},x_{\text{TR}})}}}$

  end for

  Sample $x_{r} \sim \mathcal{D}_{\text{retain}}$

  \# RepE retain loss from Equation [2](#S4.E2 "Equation 2 ‣ Tamper-resistance objective. ‣ 4.2 Tamper-Resistance Training ‣ 4 Safeguard Tamper-Resistance Training ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")

  $g_{\text{retain}}\leftarrow{\nabla_{\theta_{i - 1}}\left( {{\mathcal{L}_{\text{LM}}\hspace{0pt}{(\theta_{i - 1},x_{r})}} + {\|{{h_{\theta_{i - 1}}\hspace{0pt}{(x_{r})}} - {h_{\theta}\hspace{0pt}{(x_{r})}}}\|}_{2}^{2}} \right)}$

  \# Full tamper-resistance update

  $\theta_{i}\leftarrow{\theta_{i - 1} - {\eta\left( {{\lambda_{\text{TR}} \cdot g_{\text{TR}}} + {\lambda_{\text{retain}} \cdot g_{\text{retain}}}} \right)}}$

 end for

 $\theta_{G}\leftarrow\theta_{N}$

 return $\theta_{G}$

Algorithm 1 TAR: Tampering Attack Resistance

## 4 Safeguard Tamper-Resistance Training

To obtain tamper-resistant safeguards, we propose a new method outlined in Algorithm [1](#alg1 "Algorithm 1 ‣ 3.3 Red Teaming ‣ 3 Tamper-Resistant Safeguards ‣ Tamper-Resistant Safeguards for Open-Weight LLMs") inspired by adversarial training and meta-learning to directly strengthen LLM safeguards against tampering attacks, called Tampering Attack Resistance (TAR). We identify unique properties of this adversarial training regime and leverage them to improve robustness.

Our method for training tamper-resistant safeguards consists of two phases: (1) model safeguarding and (2) tamper-resistance training.

### 4.1 Model Safeguarding

The method begins by including an initial safeguard $G$ into a base model $\theta$. For example, initial safeguards for knowledge restriction can be drawn from a wide variety of existing methods, including circuit breaking \[[31](#bib.bib31), [75](#bib.bib75)\] or constrained gradient ascent for a particular knowledge domain. Similarly, we can include a refusal safeguard by performing RLHF \[[43](#bib.bib43)\] or DPO \[[46](#bib.bib46)\] on refusal completions. Importantly, these initial safeguards do not need to be tamper-resistant. Empirically, we find that this safeguarding step is crucial for preserving a low pre-attack safety_metric.

### 4.2 Tamper-Resistance Training

Starting from $\theta_{G_{0}}$, we train the tamper-resistant $\theta_{G}$ using a novel adversarial training procedure. Namely, we train against a set of tampering attacks $\mathcal{A}_{\text{train}}$, where the defender’s objective is to maximize a proxy safety_metric after applying an adversarial attack $\text{attack} \sim \mathcal{A}_{\text{train}}$ to $\theta$. Since it may not be feasible to differentiate through attack, we draw on insights from prior work in meta-learning, defining ${\text{attack}\hspace{0pt}{(\theta_{G})}} = \theta_{G}^{\prime} = {\theta_{G} + {\text{attack}^{\prime}\hspace{0pt}{(\theta_{G})}}}$ as a perturbation on top of initial parameters, where backpropagation through $\text{attack}^{\prime}$ is approximated with a straight-through estimator \[[5](#bib.bib5)\].

We focus on supervised fine-tuning (SFT) adversaries where attack applies several steps of optimization to $\theta_{G}$, which allows straight-through estimation through $\text{attack}^{\prime}$ to benefit from the setting and approximations of first-order MAML \[[12](#bib.bib12)\]. However, we note key differences in our approach from standard meta-learning and prior methods \[[12](#bib.bib12), [16](#bib.bib16)\]. In particular, traditional meta-learning techniques seek to obtain a model initialization that is close to optimality on multiple test distributions. In our setting, we seek to obtain an initialization that is far from optimality on multiple adversaries’ test distributions. Novel to our approach in this new setting is the use of a tamper-resistance loss in the “outer loop” that differs from the fine-tuning adversary’s loss function and serves to maximize the proxy safety metric. We depict this structure in Algorithm [1](#alg1 "Algorithm 1 ‣ 3.3 Red Teaming ‣ 3 Tamper-Resistant Safeguards ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), and explain the objective below.

Figure 3: The choice of tamper-resistance loss is crucial for obtaining good performance. Here, we show loss trajectories when the tamper-resistance loss is negative cross-entropy (left), versus negative entropy (right), over the course of TAR for $750$ steps. Outer loop losses (blue) are reduced by the defender, and inner-loop losses (red) are reduced by the train-time adversary. When the tamper-resistance loss maximizes cross-entropy (left), the adversary is only affected earlier in its trajectory and quickly recovers. By contrast, when the tamper-resistance loss maximizes entropy (right), the inner loop adversary is eventually thwarted along its entire trajectory. Plots are smoothed.

##### Impeding the adversary’s loss.

The aim of tamper-resistance training is to prevent adversaries with large compute budgets from reducing the safety_metric at test-time. In adversarial training for tamper-resistance, we define a tamper-resistance loss $\mathcal{L}_{\text{TR}}$ that counters attack. We operationalize our goal of avoiding adversary optimality as searching for $\theta$ such that $\mathcal{L}_{\text{TR}}$ is minimized for $\text{attack}\hspace{0pt}{(\theta)}$.

Empirically, we find that the choice of tamper-resistance loss $\mathcal{L}_{\text{TR}}$ significantly affects this goal. Prior work \[[16](#bib.bib16)\] negates the loss of a fine-tuning adversary, in which the aim is to arbitrarily maximize the adversary’s loss throughout fine-tuning. This formulation has two issues: (1) maximizing a cross-entropy loss can cause divergence; (2) empirically we observe that when using this objective against fine-tuning adversaries, the model learns to explode the adversary’s loss for the first few inner loop steps, while loss at later steps remains low. In Figure [3](#S4.F3 "Figure 3 ‣ 4.2 Tamper-Resistance Training ‣ 4 Safeguard Tamper-Resistance Training ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), we show the difference in choosing $\mathcal{L}_{\text{TR}}$ to be a clamped negative cross-entropy loss vs. negative entropy loss for weaponization knowledge restriction. For the latter, $\mathcal{L}_{\text{TR}}$ is eventually satisfied for all inner loop steps. For harmful request refusal, we choose $\mathcal{L}_{\text{TR}}$ to be the DPO loss \[[46](#bib.bib46)\]. We provide further detail on the choice of $\mathcal{L}_{\text{TR}}$ in both settings in Appendix [C.3](#A3.SS3 "C.3 Designing the Tamper-resistance Loss ‣ Appendix C Method Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), as well as an extended depiction of the test-time loss characteristics in Appendix [D.3](#A4.SS3 "D.3 Test-time Generalization Experiments ‣ Appendix D Additional Analysis Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs") and Figure [6](#A4.F6 "Figure 6 ‣ D.2 Targeted Patching of Vulnerabilities ‣ Appendix D Additional Analysis Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs").

##### Tamper-resistance objective.

We now describe the general proxy objective used for preventing a tampering attack from recovering weaponization knowledge or harmful behavior. For a given safety_metric, let $\mathcal{D}_{\text{TR}}$ and $\mathcal{L}_{\text{TR}}$ respectively be a dataset and loss function such that minimizing $\mathcal{L}_{\text{TR}}\hspace{0pt}{(\theta_{G},\mathcal{D}_{\text{TR}})}$ serves as a proxy objective for maximizing the $\text{safety\_metric}\hspace{0pt}{(\theta_{G})}$. We define $\mathcal{D}_{\text{retain}}$ and $\mathcal{L}_{\text{retain}}$ correspondingly for $\text{capabilities\_metric}\hspace{0pt}{(\theta_{G})}$. The defender’s objective is to solve the following optimization problem:

|     |                                                                                                                                                                                                                                                                                                                                                                                        |     |     |
|-----|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $${{{{\min\limits_{\theta}\lambda_{\text{TR}}} \cdot {\mathbb{E}}_{\text{attack} \sim \mathcal{A}_{\text{train}}}}\hspace{0pt}\left\lbrack {\mathcal{L}_{\text{TR}}\hspace{0pt}{({\text{attack}\hspace{0pt}{(\theta)}},\mathcal{D}_{\text{TR}})}} \right\rbrack} + {{\lambda_{\text{retain}} \cdot \mathcal{L}_{\text{retain}}}\hspace{0pt}{(\theta,\mathcal{D}_{\text{retain}})}}},$$ |     | (1) |

where $\mathcal{L}_{\text{TR}}$ is a tamper-resistance loss that counters $\text{attack}\hspace{0pt}{(\theta)}$. The $\mathcal{L}_{\text{retain}}$ term is a representation engineering \[[72](#bib.bib72)\] inspired retain loss for preserving performance on the capabilities proxy dataset $\mathcal{D}_{\text{retain}}$, given by

|     |                                                                                                                                                                                                                                                                                                                             |     |     |
|-----|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $${\mathcal{L}_{\text{retain}}\hspace{0pt}{(\theta,\mathcal{D}_{\text{retain}})}} = {{\mathbb{E}}_{x \sim \mathcal{D}_{\text{retain}}}\hspace{0pt}\left\lbrack {{\mathcal{L}_{\text{LM}}\hspace{0pt}{(\theta,x)}} + {\|{{h_{\theta}\hspace{0pt}{(x)}} - {h_{\theta_{G_{0}}}\hspace{0pt}{(x)}}}\|}_{2}^{2}} \right\rbrack}$$ |     | (2) |

where $h_{\theta}\hspace{0pt}{( \cdot )}$ returns the residual stream hidden states for model parameters $\theta$ and $\mathcal{L}_{\text{LM}}$ is the standard language modelling cross-entropy loss. Empirically, we find that pushing retain-set residual stream representations to be close to the base model $\theta_{G_{0}}$ via the $\ell_{2}$-norm loss in Equation [2](#S4.E2 "Equation 2 ‣ Tamper-resistance objective. ‣ 4.2 Tamper-Resistance Training ‣ 4 Safeguard Tamper-Resistance Training ‣ Tamper-Resistant Safeguards for Open-Weight LLMs") maintains a high $\text{capabilities\_metric}\hspace{0pt}{(\theta_{G})}$. In Equation [1](#S4.E1 "Equation 1 ‣ Tamper-resistance objective. ‣ 4.2 Tamper-Resistance Training ‣ 4 Safeguard Tamper-Resistance Training ‣ Tamper-Resistant Safeguards for Open-Weight LLMs") we include $\lambda_{\text{TR}}$ and $\lambda_{\text{retain}}$ as scalar weightings for the tamper-resistance loss and retain loss, respectively. We provide further details on the design of the tamper-resistance loss function in Appendix [C.3](#A3.SS3 "C.3 Designing the Tamper-resistance Loss ‣ Appendix C Method Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs") as well as an efficiency trick for sampling fine-tuning attacks for TAR in Appendix [C.4](#A3.SS4 "C.4 Efficiently Sampling Fine-tuning Attacks ‣ Appendix C Method Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs").

|                      |               |             |            |                    |
|----------------------|---------------|-------------|------------|--------------------|
| Weaponization Domain | Model         | Pre-Attacks |            | Post-Attacks (Avg) |
|                      |               | Retain (↑)  | Forget (↓) | Forget (↓)         |
| Biosecurity          | Random        | 25.0        | 25.0       | 25.0               |
|                      | No Defense    | 67.3        | 70.5       | 70.5               |
|                      | Max Entropy   | 65.0        | 33.2       | 65.8               |
|                      | Min Posterior | 65.6        | 50.4       | 66.0               |
|                      | LLMU          | 65.5        | 29.9       | 61.3               |
|                      | RMU           | 65.8        | 31.2       | 64.9               |
|                      | TAR (Ours)    | 54.7        | 28.1       | 35.2               |
| Chemical Security    | Random        | 25.0        | 25.0       | 25.0               |
|                      | No Defense    | 68.2        | 47.8       | 47.8               |
|                      | Max Entropy   | 67.5        | 50.0       | 45.7               |
|                      | Min Posterior | 66.8        | 49.5       | 47.5               |
|                      | LLMU          | 67.0        | 30.1       | 44.3               |
|                      | RMU           | 67.6        | 27.5       | 46.0               |
|                      | TAR (Ours)    | 56.5        | 28.4       | 27.1               |
| Cybersecurity        | Random        | 25.0        | 25.0       | 25.0               |
|                      | No Defense    | 68.2        | 46.4       | 46.4               |
|                      | Max Entropy   | 66.5        | 28.7       | 41.7               |
|                      | Min Posterior | 66.6        | 41.8       | 41.9               |
|                      | LLMU          | 66.1        | 27.6       | 41.3               |
|                      | RMU           | 66.8        | 29.5       | 42.2               |
|                      | TAR (Ours)    | 60.7        | 23.6       | 28.6               |

Table 1: Pre-Attack and average Post-Attack accuracies for WMDP Biosecurity, Chemical Security, and Cybersecurity for TAR and all other baselines, reported for Llama-3-8B. The average Post-Attack accuracy is computed as the average accuracy across the $26$ fine-tuning attacks discussed in Section [5](#S5 "5 Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), averaged over multiple seed repeats. TAR is the only method that maintains low Post-Attack recovery while preserving high Retain MMLU and low Forget accuracies. All values are percentages.

## 5 Experiments

We evaluate TAR in weaponization knowledge restriction and harmful request refusal settings, with results shown in Table [1](#S4.T1 "Table 1 ‣ Tamper-resistance objective. ‣ 4.2 Tamper-Resistance Training ‣ 4 Safeguard Tamper-Resistance Training ‣ Tamper-Resistant Safeguards for Open-Weight LLMs") and Table [2](#S5.T2 "Table 2 ‣ Setup. ‣ 5.2 Harmful Request Refusal ‣ 5 Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs") respectively. We discuss the setup, baselines, and analysis for our results. In each setting, we use a specific set of training adversaries $\mathcal{A}_{\text{train}}$ and test adversaries $\mathcal{A}_{\text{test}}$. Further experiment details are presented in Appendix [E](#A5 "Appendix E Experiment Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs").

### 5.1 Weaponization Knowledge Restriction

We now describe the setup, baselines, and results for our weaponization knowledge restriction experiments, including the knowledge domains, optimizers, and evaluation details.

##### Setup.

We focus on implementing tamper-resistant safeguards for restricting proxy weaponization knowledge about biosecurity, chemical security, and cybersecurity from Llama-3-8B-Instruct \[[1](#bib.bib1)\] that has been initially safeguarded via the Random Mapping method discussed in Appendix [C.2](#A3.SS2 "C.2 Initial Weaponization Knowledge Restriction Safeguard ‣ Appendix C Method Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"). For each weaponization domain, we assign $\mathcal{D}_{\text{TR}}$ to the corresponding forget set described in Appendix [E.1](#A5.SS1 "E.1 Weaponization Domain Proxy Dataset Details ‣ Appendix E Experiment Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"). We proceed to sample train-time 64-step fine-tuning attacks from different data distributions, detailed in Appendix [E.2](#A5.SS2 "E.2 Train-time Settings and Adversaries ‣ Appendix E Experiment Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"). We use $N = 750$ outer loop steps, ScheduleFree AdamW \[[9](#bib.bib9)\] with a learning rate of $2 \times 10^{- 5}$ as the outer loop tamper-resistance optimizer. For biosecurity and cybersecurity we set the tamper-resistance loss scale $\lambda_{\text{TR}}$ to $4.0$, and use $\lambda_{\text{TR}} = 3.0$ for chemical security. We use $\lambda_{\text{retain}} = 1.0$ in all settings. Lastly, we evaluate Pre-Attack and Post-Attack accuracy on corresponding WMDP subjects \[[31](#bib.bib31)\] averaged across all adversaries in Appendix [F.1](#A6.SS1 "F.1 Weaponization Knowledge Restriction ‣ Appendix F Red Teaming Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), and measure benign capabilities via the complement of subjects related to each proxy weaponization domain in MMLU \[[17](#bib.bib17)\].

##### Baselines.

We evaluate two recently proposed knowledge restriction methods: RMU \[[31](#bib.bib31)\] and LLMU \[[63](#bib.bib63)\]. We also design two baseline methods for knowledge restriction: Min Posterior, which minimizes posterior loss on forget set tokens; Max Entropy, which maximizes entropy on forget set tokens. Two additional methods, MLAC \[[16](#bib.bib16)\] and SOPHON \[[10](#bib.bib10)\], require substantial modifications for the LLM setting, so we show results on adapted versions of these baselines in [Section G.3](#A7.SS3 "G.3 Additional Baseline Comparisons ‣ Appendix G Baseline Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs").

![Refer to caption](2408.00761v4/bio_heatmap.png)

![Refer to caption](2408.00761v4/chem_heatmap.png)

![Refer to caption](2408.00761v4/cyber_heatmap.png)

Figure 4: Red teaming results across weaponization domains. Values show percentages, with Random Chance (RC) at $25\%$ and “ND” indicating No Defense WMDP scores. Red indicates attack performance approaching No Defense levels. We evaluate each defense against a diverse range of strong adversaries described in Appendix [F.1](#A6.SS1 "F.1 Weaponization Knowledge Restriction ‣ Appendix F Red Teaming Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")). Accuracies are reported as averages over 3 repeats of each attack with different seeds. Compared to prior safeguards, TAR greatly increases tamper-resistance for nearly all adversaries.

##### Results.

We show weaponization knowledge restriction safeguard results on Llama-3-8B-Instruct in [Table 1](#S4.T1 "In Tamper-resistance objective. ‣ 4.2 Tamper-Resistance Training ‣ 4 Safeguard Tamper-Resistance Training ‣ Tamper-Resistant Safeguards for Open-Weight LLMs") and Figure [2](#S2.F2 "Figure 2 ‣ Adversarial attacks on LLMs. ‣ 2 Related Work ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"). These results are averaged across all adversaries described in Appendix [F.1](#A6.SS1 "F.1 Weaponization Knowledge Restriction ‣ Appendix F Red Teaming Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"). Our large-scale experiments corroborate the findings in recent work that existing LLM safeguards are extremely brittle to fine-tuning attacks. By contrast, TAR maintains low post-attack forget accuracy across all three domains. However, we observe that TAR lowers retain accuracy by $10.6\%$ on average, indicating a trade-off between benign capabilities and robustness. In Figure [4](#S5.F4 "Figure 4 ‣ Baselines. ‣ 5.1 Weaponization Knowledge Restriction ‣ 5 Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), we observe that TAR is robust to significantly more fine-tuning attacks than all prior methods. While existing baselines break down under most attacks, TAR obtains a post-attack forget accuracy near random chance for nearly all attacks, indicating a successful defense.

Overall, we find that TAR provides significantly more robustness to realistic fine-tuning attacks than all prior methods, including SFT attacks that utilize completely held-out data. We also include further analysis of TAR’s test-time loss behavior in Appendix [D.3](#A4.SS3 "D.3 Test-time Generalization Experiments ‣ Appendix D Additional Analysis Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), in which we empirically observe TAR’s convergence and robustness. These results demonstrate for the first time that obtaining strong tamper-resistance for open-weight LLMs may be possible.

### 5.2 Harmful Request Refusal

We now describe the setup, baselines, and results for our harmful request refusal experiments, including the datasets used and evaluation details.

##### Setup.

For harmful request refusal training, we seek to make existing refusal safeguards in Llama-3-8B-Instruct robust to tampering attacks. We sample train-time adversaries that perform 64-step SFT attacks using the Anthropic-HH-RLHF dataset \[[3](#bib.bib3)\], following the methodology in Appendix [E.2](#A5.SS2 "E.2 Train-time Settings and Adversaries ‣ Appendix E Experiment Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"). Similar to the weaponization knowledge restriction setting, we use $N = 100$ outer loop steps, ScheduleFree AdamW \[[9](#bib.bib9)\] with an LR of $6 \times 10^{- 5}$ as the outer loop tamper-resistance optimizer, and loss scales of ${\lambda_{\text{TR}} = 0.1},{\lambda_{\text{retain}} = 1.0}$. We evaluate the Post-Attack jailbreak attack success rate (ASR) on HarmBench \[[37](#bib.bib37)\] after the tampering attacks in Appendix [F.2](#A6.SS2 "F.2 Harmful Request Refusal ‣ Appendix F Red Teaming Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), and measure benign capabilities preservation via MT-Bench \[[70](#bib.bib70)\], which evaluates multi-turn conversation ability.

|                           |                 |      |          |      |            |
|---------------------------|-----------------|------|----------|------|------------|
|                           | Refusal Trained | R2D2 | RepNoise | RR   | TAR (Ours) |
| Pre-Attacks MT-Bench (↑)  | 8.1             | 6.0  | 6.2      | 8.0  | 6.3        |
| Avg. Post-Attacks ASR (↓) | 72.5            | 78.3 | 74.5     | 84.8 | 63.9       |

Table 2: Average Post-Attack HarmBench ASR, reported for TAR, Representation Rerouting (RR), and the Refusal Trained Llama-3-8B-Instruct model across $5$ fine-tuning attacks depicted in Appendix [F.2](#A6.SS2 "F.2 Harmful Request Refusal ‣ Appendix F Red Teaming Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), as well as Pre-Attack MT-Bench. TAR is more robust than other methods after tampering, while maintaining comparable MT-Bench performance. ASR values are percentages.

##### Baselines.

We consider 4 baselines alongside our TAR model: Llama-3-8B-Instruct (Refusal Trained); Representation Rerouting (RR) \[[75](#bib.bib75)\] on Llama-3-8B-Instruct, which trains to push representations for harmful inputs to be orthogonal to the original representations in Llama-3-8B-Instruct; R2D2 \[[37](#bib.bib37)\] on Zephyr-7B \[[56](#bib.bib56)\], which performs adversarial training against GCG attacks \[[73](#bib.bib73)\]; and RepNoise \[[51](#bib.bib51)\] on Llama-2-7B \[[55](#bib.bib55)\], which regularizes harmful representations to noise.

##### Results.

We show refusal results in [Table 2](#S5.T2 "In Setup. ‣ 5.2 Harmful Request Refusal ‣ 5 Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"). While the Refusal Training, RR, and R2D2 baselines resist jailbreak attacks in HarmBench before tampering, we find that percentage attack success rate jumps up to above $77$ after tampering, while our TAR method only rises to $61.7$. Since we apply our TAR refusal safeguard to Llama-3-8B, it does reduce MT-Bench by $1.7$. However, this exceeds the MT-Bench score of fairly capable open-weight models, indicating that benign capabilities are largely preserved. We leave the exploration of the full impact on capabilities to future work. Additional results are in [Table 11](#A6.T11 "In F.2.1 Additional Harmful Request Refusal Results ‣ F.2 Harmful Request Refusal ‣ Appendix F Red Teaming Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"). In general, we find that our TAR model refuses more Post-Attack jailbreaks than previous baselines, and demonstrates the flexibility of the tamper-resistance objective to accommodate the harmful request refusal setting.

### 5.3 Analysis

##### Red teaming.

To assess the tamper-resistance of our models, we conduct an extensive suite of supervised fine-tuning attacks with 26 distinct adversaries in the Biosecurity setting and 24 distinct adversaries in the Chemical Security and Cybersecurity settings. We vary the optimizer, number of optimization steps, learning rate, learning rate schedule, fine-tuning dataset, batch size, and overall fine-tuning method (e.g., full fine-tuning versus parameter-efficient fine-tuning). By default, our attacks use $500$ fine-tuning steps. Full details for these adversaries are provided in [Table 9](#A6.T9 "In F.1 Weaponization Knowledge Restriction ‣ Appendix F Red Teaming Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs").

We show red teaming results in Figure [4](#S5.F4 "Figure 4 ‣ Baselines. ‣ 5.1 Weaponization Knowledge Restriction ‣ 5 Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"). While baseline safeguards withstand fine-tuning attacks in a small number of cases, most adversaries succeed in removing the safeguards. By contrast, our TAR safeguard is robust to a wide range of adversaries. This shows that tamper-resistance is a tractable problem on which progress can be made. However, we find our method exhibits varying robustness to parameter-efficient fine-tuning (PEFT) and some out-of-distribution LR attacks, highlighting the current sensitivity of the method to the adversary distributions sampled during TAR training. These findings reinforce the importance of extensive red teaming when developing tamper-resistant defenses to reveal the scope of their protection. We hypothesize that future work could easily address these limitations, as we demonstrate in [Section D.2](#A4.SS2 "D.2 Targeted Patching of Vulnerabilities ‣ Appendix D Additional Analysis Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs") that targeted patching of vulnerabilities is possible.

As mentioned in Section [3.1](#S3.SS1 "3.1 Threat Model ‣ 3 Tamper-Resistant Safeguards ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), the threat model we consider involves SFT weight tampering adversaries and not input-space “jailbreaking” adversaries, nor does TAR explicitly optimize for input-space robustness \[[37](#bib.bib37), [74](#bib.bib74), [75](#bib.bib75)\]. Nonetheless, we find that TAR’s pre-attack forget accuracies are comparable to baselines in Table [1](#S4.T1 "Table 1 ‣ Tamper-resistance objective. ‣ 4.2 Tamper-Resistance Training ‣ 4 Safeguard Tamper-Resistance Training ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), and believe that explicitly defending against input-space attacks alongside tampering attacks would be a good direction for future work.

## 6 Conclusion

We introduced a novel method for implementing tamper-resistant safeguards for LLMs and explored applications in weaponization knowledge restriction and harmful refusal training. We compare our results to prior work in each setting, finding that our method is the first method robust under the rigorous red-teaming evaluation that we consider. More broadly, we demonstrate that progress on open-weight tamper-resistance is tractable. We believe this line of research is crucial for enabling ongoing deployment of robust, open-weight LLMs, ensuring their alignment with regulatory frameworks and preemptively addressing the risk of malicious use.

##### Acknowledgements.

We thank Steven Basart and Luis Fernandez for providing valuable feedback for the paper, as well as Xiangyu Qi, Boyi Wei, Nicholas Carlini, Prateek Mittal, and Peter Henderson for useful discussions. We also thank Andriy Novykov and the Center for AI Safety for providing significant compute resources for this project, as well as Volodymyr Kindratenko and the National Center for Supercomputing Applications (NCSA) and Illinois Campus Cluster Program (ICCP) for supporting our computing needs. This work used NVIDIA GPUs at NCSA Delta through allocations CIS230117 from the Advanced Cyberinfrastructure Coordination Ecosystem: Services & Support (ACCESS) program, which is supported by NSF Grants \#2138259, \#2138286, \#2138307, \#2137603, and \#2138296.

## References

- \[1\] AI@Meta. Llama 3 model card.  2024.
- \[2\] J. Bae, N. Ng, A. Lo, M. Ghassemi, and R. B. Grosse. If influence functions are the answer, then what is the question? *ArXiv*, abs/2209.05364, 2022.
- \[3\] Y. Bai, A. Jones, K. Ndousse, A. Askell, A. Chen, N. DasSarma, D. Drain, S. Fort, D. Ganguli, T. Henighan, et al. Training a helpful and harmless assistant with reinforcement learning from human feedback. *arXiv:2204.05862*, 2022.
- \[4\] N. Belrose, D. Schneider-Joseph, S. Ravfogel, R. Cotterell, E. Raff, and S. Biderman. Leace: Perfect linear concept erasure in closed form. *Advances in Neural Information Processing Systems*, 36, 2024.
- \[5\] Y. Bengio, N. Léonard, and A. Courville. Estimating or propagating gradients through stochastic neurons for conditional computation, 2013.
- \[6\] T. Cai, X. Song, J. Jiang, F. Teng, J. Gu, and G. Zhang. Ulma: Unified language model alignment with human demonstration and point-wise preference, 2024.
- \[7\] P. F. Christiano, J. Leike, T. Brown, M. Martic, S. Legg, and D. Amodei. Deep reinforcement learning from human preferences. *Advances in neural information processing systems*, 30, 2017.
- \[8\] CTFtime. Ctftime writeups archive. [https://ctftime.org/writeups](https://ctftime.org/writeups), 2024.
- \[9\] A. Defazio, Xingyu, Yang, H. Mehta, K. Mishchenko, A. Khaled, and A. Cutkosky. The road less scheduled, 2024.
- \[10\] J. Deng, S. Pang, Y. Chen, L. Xia, Y. Bai, H. Weng, and W. Xu. Sophon: Non-fine-tunable learning to restrain task transferability for pre-trained models, 2024.
- \[11\] R. Eldan and M. Russinovich. Who’s harry potter? approximate unlearning in llms. *ArXiv*, abs/2310.02238, 2023.
- \[12\] C. Finn, P. Abbeel, and S. Levine. Model-agnostic meta-learning for fast adaptation of deep networks, 2017.
- \[13\] L. Gao, S. Biderman, S. Black, L. Golding, T. Hoppe, C. Foster, J. Phang, H. He, A. Thite, N. Nabeshima, S. Presser, and C. Leahy. The pile: An 800gb dataset of diverse text for language modeling, 2020.
- \[14\] A. Golatkar, A. Achille, and S. Soatto. Eternal sunshine of the spotless net: Selective forgetting in deep networks. In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, pages 9304–9312, 2020a.
- \[15\] A. Golatkar, A. Achille, and S. Soatto. Forgetting outside the box: Scrubbing deep networks of information accessible from input-output observations. In *Computer Vision–ECCV 2020: 16th European Conference, Glasgow, UK, August 23–28, 2020, Proceedings, Part XXIX 16*, pages 383–398. Springer, 2020b.
- \[16\] P. Henderson, E. Mitchell, C. D. Manning, D. Jurafsky, and C. Finn. Self-destructing models: Increasing the costs of harmful dual uses of foundation models, 2023.
- \[17\] D. Hendrycks, C. Burns, S. Basart, A. Zou, M. Mazeika, D. Song, and J. Steinhardt. Measuring massive multitask language understanding, 2021.
- \[18\] E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, and W. Chen. Lora: Low-rank adaptation of large language models, 2021.
- \[19\] G. Huang, Y. Li, G. Pleiss, Z. Liu, J. E. Hopcroft, and K. Q. Weinberger. Snapshot ensembles: Train 1, get m for free, 2017.
- \[20\] T. Huang, S. Hu, F. Ilhan, S. F. Tekin, and L. Liu. Booster: Tackling harmful fine-tuning for large language models via attenuating harmful perturbation, 2024a. URL [https://arxiv.org/abs/2409.01586](https://arxiv.org/abs/2409.01586).
- \[21\] T. Huang, S. Hu, F. Ilhan, S. F. Tekin, and L. Liu. Lisa: Lazy safety alignment for large language models against harmful fine-tuning attack, 2024b. URL [https://arxiv.org/abs/2405.18641](https://arxiv.org/abs/2405.18641).
- \[22\] T. Huang, S. Hu, and L. Liu. Vaccine: Perturbation-aware alignment for large language model, 2024c.
- \[23\] H. Inan, K. Upasani, J. Chi, R. Rungta, K. Iyer, Y. Mao, M. Tontchev, Q. Hu, B. Fuller, D. Testuggine, and M. Khabsa. Llama guard: Llm-based input-output safeguard for human-ai conversations, 2023.
- \[24\] N. Jain, A. Schwarzschild, Y. Wen, G. Somepalli, J. Kirchenbauer, P. yeh Chiang, M. Goldblum, A. Saha, J. Geiping, and T. Goldstein. Baseline defenses for adversarial attacks against aligned language models, 2023.
- \[25\] H. Jin, R. Chen, A. Zhou, Y. Zhang, and H. Wang. Guard: Role-playing to generate natural-language jailbreakings to test guideline adherence of large language models, 2024a.
- \[26\] H. Jin, A. Zhou, J. D. Menke, and H. Wang. Jailbreaking large language models against moderation guardrails via cipher characters, 2024b.
- \[27\] D. P. Kingma and J. Ba. Adam: A method for stochastic optimization, 2017.
- \[28\] P. W. Koh and P. Liang. Understanding black-box predictions via influence functions. In *International Conference on Machine Learning*, 2017.
- \[29\] S. Kullback and R. A. Leibler. On information and sufficiency. *Annals of Mathematical Statistics*, 22:79–86, 1951.
- \[30\] G. Li, H. A. A. K. Hammoud, H. Itani, D. Khizbullin, and B. Ghanem. Camel: Communicative agents for "mind" exploration of large language model society, 2023.
- \[31\] N. Li, A. Pan, A. Gopal, S. Yue, D. Berrios, A. Gatti, J. D. Li, A.-K. Dombrowski, S. Goel, L. Phan, G. Mukobi, N. Helm-Burger, R. Lababidi, L. Justen, A. B. Liu, M. Chen, I. Barrass, O. Zhang, X. Zhu, R. Tamirisa, B. Bharathi, A. Khoja, Z. Zhao, A. Herbert-Voss, C. B. Breuer, A. Zou, M. Mazeika, Z. Wang, P. Oswal, W. Liu, A. A. Hunt, J. Tienken-Harder, K. Y. Shih, K. Talley, J. Guan, R. Kaplan, I. Steneker, D. Campbell, B. Jokubaitis, A. Levinson, J. Wang, W. Qian, K. K. Karmakar, S. Basart, S. Fitz, M. Levine, P. Kumaraguru, U. Tupakula, V. Varadharajan, Y. Shoshitaishvili, J. Ba, K. M. Esvelt, A. Wang, and D. Hendrycks. The wmdp benchmark: Measuring and reducing malicious use with unlearning, 2024.
- \[32\] S. Liu, Y. Yao, J. Jia, S. Casper, N. Baracaldo, P. Hase, X. Xu, Y. Yao, H. Li, K. R. Varshney, et al. Rethinking machine unlearning for large language models. *arXiv preprint arXiv:2402.08787*, 2024.
- \[33\] X. Liu, N. Xu, M. Chen, and C. Xiao. Autodan: Generating stealthy jailbreak prompts on aligned large language models. *arXiv:2310.04451*, 2023.
- \[34\] Llama Team, AI @ Meta. The llama 3 herd of models, 2024.
- \[35\] I. Loshchilov and F. Hutter. SGDR: stochastic gradient descent with restarts. *CoRR*, abs/1608.03983, 2016.
- \[36\] A. Lynch, P. Guo, A. Ewart, S. Casper, and D. Hadfield-Menell. Eight methods to evaluate robust unlearning in llms. *arXiv preprint arXiv:2402.16835*, 2024.
- \[37\] M. Mazeika, L. Phan, X. Yin, A. Zou, Z. Wang, N. Mu, E. Sakhaee, N. Li, S. Basart, B. Li, D. Forsyth, and D. Hendrycks. Harmbench: A standardized evaluation framework for automated red teaming and robust refusal. In *ICML*, 2024.
- \[38\] K. McGuffie and A. Newhouse. The radicalization risks of gpt-3 and advanced neural language models, 2020.
- \[39\] S. Merity, C. Xiong, J. Bradbury, and R. Socher. Pointer sentinel mixture models, 2016.
- \[40\] S. Miller and M. J. Selgelid. Ethical and philosophical consideration of the dual-use dilemma in the biological sciences. *Science and engineering ethics*, 13:523–580, 2007.
- \[41\] A. Nichol, J. Achiam, and J. Schulman. On first-order meta-learning algorithms, 2018.
- \[42\] OpenAI. Gpt-4 technical report, 2023.
- \[43\] L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray, et al. Training language models to follow instructions with human feedback. *Advances in Neural Information Processing Systems (NeurIPS)*, 2022.
- \[44\] X. Qi, Y. Zeng, T. Xie, P.-Y. Chen, R. Jia, P. Mittal, and P. Henderson. Fine-tuning aligned language models compromises safety, even when users do not intend to!, 2023.
- \[45\] X. Qi, B. Wei, N. Carlini, Y. Huang, T. Xie, L. He, M. Jagielski, M. Nasr, P. Mittal, and P. Henderson. On evaluating the durability of safeguards for open-weight llms, 2024. URL [https://arxiv.org/abs/2412.07097](https://arxiv.org/abs/2412.07097).
- \[46\] R. Rafailov, A. Sharma, E. Mitchell, S. Ermon, C. D. Manning, and C. Finn. Direct preference optimization: Your language model is secretly a reward model. In *Neural Information Processing Systems (NeurIPS)*, 2023.
- \[47\] S. Rajbhandari, J. Rasley, O. Ruwase, and Y. He. Zero: Memory optimizations toward training trillion parameter models. In *SC20: International Conference for High Performance Computing, Networking, Storage and Analysis*, pages 1–16, 2020. doi: 10.1109/SC41405.2020.00024.
- \[48\] J. Ren, S. Rajbhandari, R. Y. Aminabadi, O. Ruwase, S. Yang, M. Zhang, D. Li, and Y. He. ZeRO-Offload: Democratizing Billion-Scale model training. In *2021 USENIX Annual Technical Conference (USENIX ATC 21)*, pages 551–564. USENIX Association, July 2021. ISBN 978-1-939133-23-6.
- \[49\] A. Robey, E. Wong, H. Hassani, and G. J. Pappas. Smoothllm: Defending large language models against jailbreaking attacks, 2023.
- \[50\] D. Rosati, J. Wehner, K. Williams, Ł. Bartoszcze, J. Batzner, H. Sajjad, and F. Rudzicz. Immunization against harmful fine-tuning attacks. *arXiv preprint arXiv:2402.16382*, 2024a.
- \[51\] D. Rosati, J. Wehner, K. Williams, Łukasz Bartoszcze, D. Atanasov, R. Gonzales, S. Majumdar, C. Maple, H. Sajjad, and F. Rudzicz. Representation noising effectively prevents harmful fine-tuning on llms, 2024b.
- \[52\] E. Sheng, K.-W. Chang, P. Natarajan, and N. Peng. The woman worked as a babysitter: On biases in language generation. In *Conference on Empirical Methods in Natural Language Processing (EMNLP)*, 2019.
- \[53\] A. Sheshadri, A. Ewart, P. Guo, A. Lynch, C. Wu, V. Hebbar, H. Sleight, A. C. Stickland, E. Perez, D. Hadfield-Menell, and S. Casper. Targeted latent adversarial training improves robustness to persistent harmful behaviors in llms, 2024. URL [https://arxiv.org/abs/2407.15549](https://arxiv.org/abs/2407.15549).
- \[54\] A. K. Tarun, V. S. Chundawat, M. Mandal, and M. Kankanhalli. Fast yet effective machine unlearning. *IEEE Transactions on Neural Networks and Learning Systems*, 2023.
- \[55\] H. Touvron, L. Martin, K. Stone, P. Albert, A. Almahairi, Y. Babaei, N. Bashlykov, S. Batra, P. Bhargava, S. Bhosale, et al. Llama 2: Open foundation and fine-tuned chat models. *arXiv:2307.09288*, 2023.
- \[56\] L. Tunstall, E. Beeching, N. Lambert, N. Rajani, K. Rasul, Y. Belkada, S. Huang, L. von Werra, C. Fourrier, N. Habib, N. Sarrazin, O. Sanseviero, A. M. Rush, and T. Wolf. Zephyr: Direct distillation of lm alignment, 2023. URL [https://arxiv.org/abs/2310.16944](https://arxiv.org/abs/2310.16944).
- \[57\] G. Wang, S. Cheng, X. Zhan, X. Li, S. Song, and Y. Liu. Openchat: Advancing open-source language models with mixed-quality data, 2023.
- \[58\] A. Wei, N. Haghtalab, and J. Steinhardt. Jailbroken: How does llm safety training fail? In *Neural Information Processing Systems (NeurIPS)*, 2023.
- \[59\] X. Wu, J. Li, M. Xu, W. Dong, S. Wu, C. Bian, and D. Xiong. Depn: Detecting and editing privacy neurons in pretrained language models. In *Conference on Empirical Methods in Natural Language Processing*, 2023.
- \[60\] X. Xie, P. Zhou, H. Li, Z. Lin, and S. Yan. Adan: Adaptive nesterov momentum algorithm for faster optimizing deep models, 2023.
- \[61\] Z. Xu, F. Jiang, L. Niu, Y. Deng, R. Poovendran, Y. Choi, and B. Y. Lin. Magpie: Alignment data synthesis from scratch by prompting aligned llms with nothing, 2024.
- \[62\] X. Yang, X. Wang, Q. Zhang, L. Petzold, W. Y. Wang, X. Zhao, and D. Lin. Shadow alignment: The ease of subverting safely-aligned language models, 2023. URL [https://arxiv.org/abs/2310.02949](https://arxiv.org/abs/2310.02949).
- \[63\] Y. Yao, X. Xu, and Y. Liu. Large language model unlearning. *ArXiv*, abs/2310.10683, 2023.
- \[64\] C. Yu, S. Jeoung, A. Kasi, P. Yu, and H. Ji. Unlearning bias in language models by partitioning gradients. In *Annual Meeting of the Association for Computational Linguistics*, 2023.
- \[65\] Z. Yuan, Z. Xiong, Y. Zeng, N. Yu, R. Jia, D. Song, and B. Li. Rigorllm: Resilient guardrails for large language models against undesired content, 2024.
- \[66\] M. D. Zeiler. ADADELTA: an adaptive learning rate method. *CoRR*, abs/1212.5701, 2012.
- \[67\] Q. Zhan, R. Fang, R. Bindu, A. Gupta, T. Hashimoto, and D. Kang. Removing rlhf protections in gpt-4 via fine-tuning, 2023.
- \[68\] Y. Zhao, A. Gu, R. Varma, L. Luo, C.-C. Huang, M. Xu, L. Wright, H. Shojanazeri, M. Ott, S. Shleifer, A. Desmaison, C. Balioglu, P. Damania, B. Nguyen, G. Chauhan, Y. Hao, A. Mathews, and S. Li. Pytorch fsdp: Experiences on scaling fully sharded data parallel, 2023.
- \[69\] L. Zheng, W.-L. Chiang, Y. Sheng, S. Zhuang, Z. Wu, Y. Zhuang, Z. Lin, Z. Li, D. Li, E. P. Xing, H. Zhang, J. E. Gonzalez, and I. Stoica. Judging llm-as-a-judge with mt-bench and chatbot arena, 2023a.
- \[70\] L. Zheng, W.-L. Chiang, Y. Sheng, S. Zhuang, Z. Wu, Y. Zhuang, Z. Lin, Z. Li, D. Li, E. P. Xing, H. Zhang, J. E. Gonzalez, and I. Stoica. Judging llm-as-a-judge with mt-bench and chatbot arena, 2023b.
- \[71\] A. Zhou, B. Li, and H. Wang. Robust prompt optimization for defending language models against jailbreaking attacks, 2024.
- \[72\] A. Zou, L. Phan, S. Chen, J. Campbell, P. Guo, R. Ren, A. Pan, X. Yin, M. Mazeika, A.-K. Dombrowski, S. Goel, N. Li, M. J. Byun, Z. Wang, A. Mallen, S. Basart, S. Koyejo, D. Song, M. Fredrikson, J. Z. Kolter, and D. Hendrycks. Representation engineering: A top-down approach to ai transparency, 2023a.
- \[73\] A. Zou, Z. Wang, N. Carlini, M. Nasr, J. Z. Kolter, and M. Fredrikson. Universal and transferable adversarial attacks on aligned language models, 2023b. URL [https://arxiv.org/abs/2307.15043](https://arxiv.org/abs/2307.15043).
- \[74\] A. Zou, Z. Wang, J. Z. Kolter, and M. Fredrikson. Universal and transferable adversarial attacks on aligned language models. *arXiv:2307.15043*, 2023c.
- \[75\] A. Zou, L. Phan, J. Wang, D. Duenas, M. Lin, M. Andriushchenko, R. Wang, Z. Kolter, M. Fredrikson, and D. Hendrycks. Improving alignment and robustness with short circuiting. *arXiv preprint arXiv:2406.04313*, 2024.

## Appendix A Limitations

Our method for training tamper-resistant safeguards demonstrates considerable robustness against a wide range of tampering attacks, yet several avenues for improvement remain: (1) While we focus on supervised fine-tuning attacks, the broader spectrum of open-weight tampering techniques necessitates diverse future red-teaming efforts. (2) Scaling to larger models poses computational challenges that require optimization to reduce overheads.

Additionally, in cases where TAR maintains a low post-attack forget accuracy, the post-attack retain accuracy is also low. By contrast, we found in preliminary experiments that post-attack retain accuracy for many of the baselines remained high. We note that this is acceptable because post-attack retain performance is not of concern to the defender; rather, the responsibility falls on the attacker to preserve it after tampering.

However, this does mean benign users trying to fine-tune the model must ensure their data is not contaminated by forget set data, lest their fine-tuned model have poor performance. This could make the method harder to use in practice. Thus, maintaining high post-attack retain accuracy would be a useful direction for future work to explore.

Tamper-resistance alone cannot fully mitigate the risks of malicious AI use. While it raises the initial costs for adversaries, it can eventually be circumvented. Once open-weight models are released, they cannot be “unreleased,” leaving any compromised defenses permanently vulnerable. Therefore, tamper-resistance should be considered a supplement to the broader effort of of improving the offense-defense balance of AI systems. Addressing these limitations will improve the robustness of LLMs to tampering and better support open-weight model developers.

## Appendix B Author Contributions

Rishub Tamirisa, Bhrugu Bharathi, and Mantas Mazeika led the project, including developing methods and contributing writing for all sections of the paper. Rishub Tamirisa implemented most of the code for the method and baselines, and Bhrugu Bharathi implemented most red-teaming evaluations in the paper. Rishub and Bhrugu carried out all main experiments, and orchestrated analysis experiments for Maxwell Lin and Tarun Suresh to conduct. Rowan Wang and Justin Wang curated datasets for the main experiments for the final version of the method. Long Phan and Alice Gatti implemented red-teaming evaluations, contributed figures, and gave feedback for writing drafts. Andy Zhou ran experiments for robust refusal, contributed writing the Related Work section, and helped create figures. Ron Arel organized compute logistics from the NCSA, and provided personnel for experiments. Andy Zou provided personnel for experiments and high-level advising. Dawn Song and Bo Li provided high-level advising for the project. Dan Hendrycks provided substantial advising for framing and writing, as well as method suggestions. Dan Hendrycks also provided significant compute resources from the Center for AI Safety. Mantas Mazeika was the primary project advisor during the majority of its duration, and was involved in most decisions regarding the method, experiments, and writing.

## Appendix C Method Details

### C.1 Note on Updated Implementation

After the initial release of this paper, we identified a data contamination issue in which our instruction-tuning retain dataset, Magpie-Align \[[61](#bib.bib61)\], contained a significant amount of forget set content. This resulted in an unintended input-space vulnerability \[[45](#bib.bib45)\]. After cleaning the dataset and re-training new TAR models with the same methodology and hyperparameters, the input-space vulnerability is no longer observed \[[45](#bib.bib45)\].

Figure 5: Test loss for five repeats of a $1,000$-step SFT attack against a TAR-Bio safeguard, each using a different dataloader shuffling seed. TAR yields a consistent loss plateau for $500$ steps, followed by a loss region of increased variability.

Additionally, [Qi et al. \[45\]](#bib.bib45) found that TAR’s robustness at $1,000$ of steps of fine-tuning varies when changing the dataloader shuffling order, which we corroborate in Figure [5](#A3.F5 "Figure 5 ‣ C.1 Note on Updated Implementation ‣ Appendix C Method Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"). After further investigation, we found an issue in the HuggingFace distributed dataloading sampler, where the HuggingFace sampler overrides user-defined seeds with a default seed. This resulted in the test-time dataloader shuffling orders being a subset of train-time shuffling orders in our initial release. Upon correcting the issue, we observe the variability in Figure [5](#A3.F5 "Figure 5 ‣ C.1 Note on Updated Implementation ‣ Appendix C Method Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs").

However, while the loss plateau and robustness at $1,000$ steps can vary with different dataloader shuffling orders, we do observe in Figure [5](#A3.F5 "Figure 5 ‣ C.1 Note on Updated Implementation ‣ Appendix C Method Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs") and in nearly all adversaries that the loss plateau and robustness we discuss throughout the paper remains consistent across multiple shuffling orders for $500$ steps of fine-tuning. We report these results in our updated Table [1](#S4.T1 "Table 1 ‣ Tamper-resistance objective. ‣ 4.2 Tamper-Resistance Training ‣ 4 Safeguard Tamper-Resistance Training ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), Figure [2](#S2.F2 "Figure 2 ‣ Adversarial attacks on LLMs. ‣ 2 Related Work ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), and Figure [4](#S5.F4 "Figure 4 ‣ Baselines. ‣ 5.1 Weaponization Knowledge Restriction ‣ 5 Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"). All depicted per-adversary post-attack accuracies in Table [1](#S4.T1 "Table 1 ‣ Tamper-resistance objective. ‣ 4.2 Tamper-Resistance Training ‣ 4 Safeguard Tamper-Resistance Training ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), Figure [2](#S2.F2 "Figure 2 ‣ Adversarial attacks on LLMs. ‣ 2 Related Work ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), and Figure [4](#S5.F4 "Figure 4 ‣ Baselines. ‣ 5.1 Weaponization Knowledge Restriction ‣ 5 Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs") are averaged over three replicates, each using a different random seed. We include further discussion on the loss plateau as well as concrete evidence of TAR’s convergence in Appendix [D.3](#A4.SS3 "D.3 Test-time Generalization Experiments ‣ Appendix D Additional Analysis Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"). We do emphasize that TAR models we consider in our experiments optimize against SFT adversaries that use only $K = 64$ optimization steps yet achieve significant generalization to test-time adversaries using substantially more compute, greatly improving tamper-resistance compared to prior work.

### C.2 Initial Weaponization Knowledge Restriction Safeguard

Prior to tamper-resistance training, we install a safeguard that achieves surgical knowledge restriction on the target hazardous domain. Let $h_{\theta}\hspace{0pt}{(\mathcal{D})}$ denote the distribution of post-decoder layer residual stream activations for input sequences sampled from some data distribution $\mathcal{D}$ and model weights $\theta$. We define $\text{rand\_hashed}\hspace{0pt}{(x)}$ for some input sequence $x$, which returns fixed Gaussian-sampled vectors that are chosen via hashing the corresponding input token for each residual stream index of $x$ in $\theta$. As a proxy for scrubbing target representations according to downstream task labels, we propose a weaponization knowledge restriction safeguard termed Random Mapping, which maps $h_{\theta}\hspace{0pt}{(\mathcal{D}_{\text{TR}})}$ to random noise as follows:

|     |                                                                                                                                                                                                                                                                                                                                                                                                   |     |     |
|-----|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $${{\min\limits_{\theta}{\mathbb{E}}_{x \sim \mathcal{D}_{\text{TR}}}}\hspace{0pt}\left\lbrack {1 - \left| \frac{{{h_{\theta}\hspace{0pt}{(x)}} \cdot \text{rand\_hashed}}\hspace{0pt}{(x)}}{{\|{h_{\theta}\hspace{0pt}{(x)}}\|}\hspace{0pt}{\|{\text{rand\_hashed}\hspace{0pt}{(x)}}\|}} \right|} \right\rbrack} + {\mathcal{L}_{\text{LM}}\hspace{0pt}{(\theta,\mathcal{D}_{\text{retain}})}}$$ |     | (3) |

The objective of Equation [3](#A3.E3 "Equation 3 ‣ C.2 Initial Weaponization Knowledge Restriction Safeguard ‣ Appendix C Method Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs") maximizes cosine similarity between row vectors in the residual stream in every layer of the LLM from $h{(\mathcal{D}_{\text{TR}})}$ and the hashed random vectors from $\text{rand\_hashed}\hspace{0pt}{( \cdot )}$. By providing each token’s residual stream a unique random vector to push toward, the loss encourages a “re-mapping” of token representations from $\mathcal{D}_{\text{TR}}$ to the noised vectors. We include an additional term for preserving performance on $\mathcal{D}_{\text{retain}}$ via the language-modelling cross-entropy loss $\mathcal{L}_{\text{LM}}$. We show the performance of the raw Random Mapping safeguard as an ablation in Table [5](#A4.T5 "Table 5 ‣ D.4 Ablations ‣ Appendix D Additional Analysis Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), listed as “Excl. Adv. Training.”

### C.3 Designing the Tamper-resistance Loss

##### Weaponization knowledge restriction.

For weaponization knowledge restriction, we summarize our intuition for ideal tamper-resistance loss design, corroborated by our empirical findings in Figure [3](#S4.F3 "Figure 3 ‣ 4.2 Tamper-Resistance Training ‣ 4 Safeguard Tamper-Resistance Training ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"): we seek to flatten the adversary’s loss at a high value, rather than simply raise its y-intercept.

We choose the tamper-resistance loss $\mathcal{L}_{\text{TR}}$ as an entropy loss to be maximized during the adversary’s cross-entropy fine-tuning trajectory, since maximizing entropy would impede the adversary’s cross entropy loss from decreasing during fine-tuning. In other words, we wish to obtain $\theta$ such that after an adversary performs a fine-tuning attack on $\theta$ via a cross-entropy loss, entropy is still high. We find that this formulation achieves the desired flattening behavior, and we depict the difference in flattening between the choosing $\mathcal{L}_{\text{TR}}$ to be a negative cross-entropy loss and negative entropy loss in Figure [3](#S4.F3 "Figure 3 ‣ 4.2 Tamper-Resistance Training ‣ 4 Safeguard Tamper-Resistance Training ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"). In the lefthand plot, where $\mathcal{L}_{\text{TR}}$ is a cross-entropy loss, loss only increases in the first inner loop step. In the righthand plot, where $\mathcal{L}_{\text{TR}}$ is a negative entropy loss, entropy is eventually maximized in all inner loop steps. Figure [6](#A4.F6 "Figure 6 ‣ D.2 Targeted Patching of Vulnerabilities ‣ Appendix D Additional Analysis Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs") also demonstrates the generalization of the flat adversary loss behavior beyond the length of the simulated fine-tuning trajectories during TAR.

##### Harmful request refusal.

For harmful request refusal, we choose $\mathcal{L}_{\text{TR}}$ to be the DPO loss \[[46](#bib.bib46)\], which works as follows. Given a DPO dataset containing pairs of rejected and refusal completions, the sampled attack performs SFT on rejected completions, and the tamper-resistance loss $\mathcal{L}_{\text{TR}}$ is a DPO loss computed on the pair chosen and rejected completions on parameter coordinates along the attack trajectory. This encourages TAR to find an initialization $\theta$ such that after a harmful fine-tuning attack, the model still prefers refusal completions over harmful completions when given an harmful prompt. While this does not necessarily encourage a flat adversary loss, we find empirically in Table [2](#S5.T2 "Table 2 ‣ Setup. ‣ 5.2 Harmful Request Refusal ‣ 5 Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs") that this formulation increases the average $\text{safety\_metric}\hspace{0pt}{(\theta_{G})}$ defined in Section [3.2](#S3.SS2 "3.2 Problem Definition and Metrics ‣ 3 Tamper-Resistant Safeguards ‣ Tamper-Resistant Safeguards for Open-Weight LLMs") after fine-tuning attacks on harmful data, detailed in Section [5](#S5 "5 Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs").

We also observe that the length of the simulated adversary SFT trajectory during training affects test-time generalization in both Figure [6](#A4.F6 "Figure 6 ‣ D.2 Targeted Patching of Vulnerabilities ‣ Appendix D Additional Analysis Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs") and Appendix [D.3](#A4.SS3 "D.3 Test-time Generalization Experiments ‣ Appendix D Additional Analysis Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"). In particular, larger values of $K$ result in increased tamper-resistance for longer SFT attacks. However, to maintain reasonable runtime efficiency, we need a more efficient sampling technique than simply running $K$ independent trajectories of varying length for every outer-loop step in Algorithm [1](#alg1 "Algorithm 1 ‣ 3.3 Red Teaming ‣ 3 Tamper-Resistant Safeguards ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), which we describe in Section [C.4](#A3.SS4 "C.4 Efficiently Sampling Fine-tuning Attacks ‣ Appendix C Method Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs").

### C.4 Efficiently Sampling Fine-tuning Attacks

Optimizing Equation [1](#S4.E1 "Equation 1 ‣ Tamper-resistance objective. ‣ 4.2 Tamper-Resistance Training ‣ 4 Safeguard Tamper-Resistance Training ‣ Tamper-Resistant Safeguards for Open-Weight LLMs") with gradient descent requires simulating $K$ tampering attacks for each tamper-resistance optimizer update, which is prohibitively expensive to run when the sampled attack performs SFT and $\theta$ contains billions of parameters. Inspired by prior work on snapshot ensembles \[[19](#bib.bib19)\], we leverage an efficiency trick: we can reuse the coordinates along steps of a single adversary fine-tuning trajectory of length $K$ to obtain $K - 1$ additional (though non-independent) trajectories of increasing length. Using this trick, we collect all $K$ parameter coordinates along the trajectory into a single batch for computing the tamper-resistance losses, effectively sampling attack from $\mathcal{A}_{\text{train}}$ non-IID. To further improve runtime efficiency, we do not compute the tamper-resistance loss $\mathcal{L}_{\text{TR}}$ on all $K$ steps and instead sub-sample coordinates along the trajectory for computing $\mathcal{L}_{\text{TR}}$ within an adversary batch, for example every 4 adversary optimization steps. Additionally, we reduce variance in the tamper-resistance gradient by computing the tamper-resistance loss at each inner loop step on the same held-out batch, denoted as $x_{\text{TR}}$ in Algorithm [1](#alg1 "Algorithm 1 ‣ 3.3 Red Teaming ‣ 3 Tamper-Resistant Safeguards ‣ Tamper-Resistant Safeguards for Open-Weight LLMs").

### C.5 Implementation Details and Resource Requirements

We perform TAR training on Llama-3-8B-Instruct \[[34](#bib.bib34)\] with 8 NVIDIA 80GB A100 GPUs, leveraging distributed training via FSDP \[[48](#bib.bib48), [47](#bib.bib47), [68](#bib.bib68)\]. We use ZeRO Stage 3 from DeepSpeed \[[47](#bib.bib47)\], which shards optimizer states, gradients, and parameters during training. While the efficiency trick in Appendix [C.4](#A3.SS4 "C.4 Efficiently Sampling Fine-tuning Attacks ‣ Appendix C Method Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs") improves runtime, we note additional considerations for conserving GPU memory.

First, simulating fine-tuning attacks that require additional state (e.g., momentum) in the inner loop of Algorithm [1](#alg1 "Algorithm 1 ‣ 3.3 Red Teaming ‣ 3 Tamper-Resistant Safeguards ‣ Tamper-Resistant Safeguards for Open-Weight LLMs") requires initializing a fresh optimizer for every outer loop iteration. Since we use an outer-loop optimizer that also requires maintaining state (ScheduleFree AdamW \[[9](#bib.bib9)\]), we move the outer loop optimizer to the CPU before instantiating inner-loop optimizers.

Second, first-order meta-learning in smaller models can typically be implemented by running multiple forward passes for each inner loop iteration, averaging losses, then backpropagating on the averaged loss term. However, because each inner-loop tamper-resistance loss term ($\mathcal{L}_{\text{TR}}$ in Algorithm [1](#alg1 "Algorithm 1 ‣ 3.3 Red Teaming ‣ 3 Tamper-Resistant Safeguards ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")) is computed on a separate forward pass, this requires maintaining $K$ computation graphs in memory. Since this is infeasible on reasonable hardware for LLMs with billions of parameters, we circumvent this inefficiency by accumulating tamper-resistance gradients in a separate data structure ($g_{\text{TR}}$ in Algorithm [1](#alg1 "Algorithm 1 ‣ 3.3 Red Teaming ‣ 3 Tamper-Resistant Safeguards ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")). We note that this can be done without using additional all-gather and reduce-scatter distributed operations, since tamper-resistance gradient accumulation and application to the pre-inner loop model parameters ($\theta_{i - 1}$ in Algorithm [1](#alg1 "Algorithm 1 ‣ 3.3 Red Teaming ‣ 3 Tamper-Resistant Safeguards ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")) can be computed solely on sharded gradients.

## Appendix D Additional Analysis Experiments

### D.1 Benign Fine-Tuning

|          |          |                 |                   |
|----------|----------|-----------------|-------------------|
|          |          | WMDP Forget (↓) | Benign Domain (↑) |
| TAR-Bio  | Pre-SFT  | 28.1            | 59.7              |
|          | Post-SFT | 30.1            | 64.7              |
| TAR-Chem | Pre-SFT  | 28.4            | 58.6              |
|          | Post-SFT | 27.5            | 62.8              |

Table 3: Average accuracy on MMLU economics subjects and WMDP Forget subjects for our Llama-3-8B TAR models safeguarded against hazardous biosecurity and chemical knowledge, before and after fine-tuning on benign economics data \[[31](#bib.bib31)\]. Results indicate that models safeguarded with TAR still preserve benign fine-tunability.

An important property of open-weight models is that they can be fine-tuned to improve performance on custom data or in specific domains. Thus, ideal tamper-resistant safeguards should allow continued fine-tuning of a model while preserving the safeguard. We evaluate whether TAR models can be fine-tuned on data unrelated to the safeguard using economics as an example domain. Using TAR models with biosecurity and chemical security safeguards, we perform supervised fine-tuning on the WMDP auxiliary economics corpora \[[31](#bib.bib31)\]. We fine-tune models for $2$ epochs using a learning rate of $2 \times 10^{- 6}$ and a batch size of $32$, using AdamW ScheduleFree \[[9](#bib.bib9)\]. For evaluation, we report average accuracy across the corresponding MMLU subjects (High School Macroeconomics and Microeconomics) before and after fine-tuning. To confirm that the safeguard remains tamper-resistant in this setting, we also evaluate accuracy on corresponding WMDP subjects before and after fine-tuning.

We show the results of this evaluation in [Table 3](#A4.T3 "In D.1 Benign Fine-Tuning ‣ Appendix D Additional Analysis Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"). We find that accuracy on economics questions can be improved by $5.0$ percentage points without recovering significant hazardous knowledge. This illustrates that strong tamper-resistance can be compatible with benign model editing.

### D.2 Targeted Patching of Vulnerabilities

|                                 |               |                     |
|---------------------------------|---------------|---------------------|
| Adversary Setup                 | Post-Attacks  |                     |
|                                 | All Advs. (↓) | R$\rightarrow$F (↓) |
| Excl. R$\rightarrow$F Adversary | 44.9          | 58.7                |
| Incl. R$\rightarrow$F Adversary | 35.2          | 29.7                |

Table 4: Pre-Attack and Post-Attack scores when excluding and including the “Retain-set SFT followed by Biosecurity SFT adversary” (R$\rightarrow$F) described in Appendix [E.2](#A5.SS2 "E.2 Train-time Settings and Adversaries ‣ Appendix E Experiment Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"). Post-attack R$\rightarrow$F accuracy averaged over both Adv. 8 and 9 in Table [9](#A6.T9 "Table 9 ‣ F.1 Weaponization Knowledge Restriction ‣ Appendix F Red Teaming Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"). Average tamper-resistance across all $26$ adversaries improves by nearly $10$ percentage points when including the R$\rightarrow$F adversary in TAR, and improves by nearly $30$ percentage points for the R$\rightarrow$F adversary specifically.

In Section [E.2](#A5.SS2 "E.2 Train-time Settings and Adversaries ‣ Appendix E Experiment Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), we discuss the set of adversaries sampled during TAR for each weaponization knowledge domain. However, we included the “Retain-set SFT followed by Weaponization-domain SFT” (R$\rightarrow$F in Table [4](#A4.T4 "Table 4 ‣ D.2 Targeted Patching of Vulnerabilities ‣ Appendix D Additional Analysis Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")) adversary to improve robustness to specific adversaries that broke the defense in earlier iterations of the method that did not sample this adversary. We find in Table [4](#A4.T4 "Table 4 ‣ D.2 Targeted Patching of Vulnerabilities ‣ Appendix D Additional Analysis Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs") that including the R$\rightarrow$F adversary significantly improves robustness to more test-time attacks, indicated by an improvement in Post-Attack Forget error by nearly $10.0$ percentage points. Importantly, we find that including the $64$-step R$\rightarrow$F adversary at train-time improves test-time robustness to both $500$-step R$\rightarrow$F adversaries (Adv. 8 and 9) in Table [9](#A6.T9 "Table 9 ‣ F.1 Weaponization Knowledge Restriction ‣ Appendix F Red Teaming Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs") by nearly $30.0$ percentage points on average, indicating that target patching of vulnerabilities is possible within TAR.

Figure 6: Our TAR safeguard can be robust to fine-tuning attacks that greatly exceed the $64$ steps used by train-time adversaries. For the LLMU safeguard, the adversary’s loss quickly decreases into the recovery region. By contrast, TAR maintains flatness at a high loss for all $1,000$ steps. Solid lines are cross-entropy losses.

### D.3 Test-time Generalization Experiments

##### Generalization to stronger test-time attacks.

In Figure [6](#A4.F6 "Figure 6 ‣ D.2 Targeted Patching of Vulnerabilities ‣ Appendix D Additional Analysis Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), we show a biosecurity fine-tuning attack at an LR of $2 \times 10^{- 5}$ on our TAR model and a model safeguarded with LLMU. We find that the tamper-resistance of TAR can generalize far beyond the $64$ steps used by train-time adversaries. Surprisingly, we observe that the test-time adversary’s cross-entropy loss does not decrease below $7$ for all $1,000$ steps. Moreover, the loss enters a plateau and does not decrease at all after $200$ steps.

We also plot the entropy of the SFT adversary’s posteriors during the attack (blue dashed line). For the first $\phantom{} \sim 200$ SFT attack steps, the adversary’s entropy remains close to $\log{(\text{vocab\_size})}$ - the maximum possible entropy (shown as "Max Entropy" by the gray dashed line). This is expected, since this exactly what TAR optimizes for via the negative entropy tamper-resistance loss. The convergence to maximum entropy at test-time clearly demonstrates the TAR meta-learning objective working as intended, in line with the inner-loop posteriors observed in Figure [3](#S4.F3 "Figure 3 ‣ 4.2 Tamper-Resistance Training ‣ 4 Safeguard Tamper-Resistance Training ‣ Tamper-Resistant Safeguards for Open-Weight LLMs").

As a point of reference, we show the progression of the same attack on LLMU. In this case, the adversary’s cross-entropy loss decreases to within the recovery region in under $20$ steps, corresponding to recovery in forget-set performance on WMDP.

Figure 7: Comparison of a $1,000$-step SFT attack against TAR with the inner-loop length $K$ varied between $\left\{ {8,16,32,64} \right\}$. Test-time loss plateau magnitude and duration increase as $K$ increases.

##### Varying the TAR inner-loop length $K$.

Recall that via the efficiency trick discussed in Appendix [C.4](#A3.SS4 "C.4 Efficiently Sampling Fine-tuning Attacks ‣ Appendix C Method Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), a single inner loop trajectory of length $K$ during TAR returns the $K$ sampled attacks in Algorithm [1](#alg1 "Algorithm 1 ‣ 3.3 Red Teaming ‣ 3 Tamper-Resistant Safeguards ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"). We compare the test-time loss robustness as we vary the length of the inner loop $K$ during TAR, running fine-tuning attacks for $1,000$ steps on a held-out forget dataset for biosecurity weaponization (Adversary 8 in Table [9](#A6.T9 "Table 9 ‣ F.1 Weaponization Knowledge Restriction ‣ Appendix F Red Teaming Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")).

For each value of $K$, we observe a plateau in the test loss that drops off at later steps as $K$ increases. This suggests that the robustness of TAR improves as the inner loop length increases. Prior work also corroborates that increasing the inner-loop length during meta-learning increases test-time generalization \[[16](#bib.bib16)\]. We note the contrast to conventional meta-learning methods mentioned in Section [4](#S4 "4 Safeguard Tamper-Resistance Training ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), in which typical meta-learning applications seek optimality after as few test-time steps as possible \[[41](#bib.bib41), [12](#bib.bib12)\]. Here, our results suggest that the TAR objective is incentivized to run with as many inner loop steps as possible, representing a beneficial tradeoff in which compute can be exchanged for robustness. We find that $K = 64$ provides significant robustness to the range of adversaries we consider in Section [5](#S5 "5 Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs") and Appendix [F.1](#A6.SS1 "F.1 Weaponization Knowledge Restriction ‣ Appendix F Red Teaming Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), while balancing computational efficiency as discussed in Appendix [C.4](#A3.SS4 "C.4 Efficiently Sampling Fine-tuning Attacks ‣ Appendix C Method Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs").

### D.4 Ablations

|                         |            |            |                    |
|-------------------------|------------|------------|--------------------|
| Ablation                | Pre-Attack |            | Post-Attacks (Avg) |
|                         | Retain (↑) | Forget (↓) | Forget (↓)         |
| No Defense              | 67.3       | 70.5       | 70.5               |
| Excl. Adv. Training     | 59.7       | 27.3       | 61.6               |
| Excl. Initial Safeguard | 62.5       | 47.3       | 35.5               |
| TAR                     | 54.7       | 28.1       | 35.2               |

Table 5: Ablations for primary components of TAR: (1) the initial model safeguard, (2) the adversarial training phase. We find that these components are critical for the high tamper-resistance that TAR achieves.

##### Including the initial safeguard.

In Table [5](#A4.T5 "Table 5 ‣ D.4 Ablations ‣ Appendix D Additional Analysis Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), we examine the impact of incorporating the Random Mapping safeguard step prior to the adversarial training phase during TAR. The Random Mapping safeguard in isolation achieves a near-random chance Pre-Attack Forget accuracy of $27.3$ (“Excl. Adv. Training” in Table [5](#A4.T5 "Table 5 ‣ D.4 Ablations ‣ Appendix D Additional Analysis Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")). However, it is susceptible to fine-tuning attacks similar to other baselines in Table [1](#S4.T1 "Table 1 ‣ Tamper-resistance objective. ‣ 4.2 Tamper-Resistance Training ‣ 4 Safeguard Tamper-Resistance Training ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), indicated by a higher Post-Attack Forget accuracy of $61.6$. When including the tamper-resistance adversarial training phase (TAR), we observe significantly increased tamper-resistance as the Post-Attack Forget accuracy decreases by nearly $26$ percentage points.

##### Excluding the initial safeguard.

We also examine the impact of performing the adversarial training phase without the initial safeguarding step (“Excl. Initial Safeguard” in Table [5](#A4.T5 "Table 5 ‣ D.4 Ablations ‣ Appendix D Additional Analysis Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs")), finding that Pre-Attack accuracy is substantially higher without the initial safeguard. We find that including the Random Mapping phase reduces pre-attack forget set accuracy by $19.2$ percentage points.

|                                     |            |            |                    |
|-------------------------------------|------------|------------|--------------------|
|                                     | Pre-Attack |            | Post-Attacks (Avg) |
| $\mathcal{L}_{\text{TR}}$ Weighting | Retain (↑) | Forget (↓) | Forget (↓)         |
| $\lambda_{\text{TR}} = 1.0$         | 62.5       | 29.3       | 39.9               |
| $\lambda_{\text{TR}} = 4.0$         | 54.7       | 28.1       | 35.2               |

Table 6: Pre-Attack and Post-Attack scores when varying the tamper-resistance loss weighting, $\lambda_{\text{TR}}$. Tamper-resistance improves by nearly $10.0\%$ when increasing $\lambda_{\text{TR}}$ from $1.0$ to $4.0$. The retain loss weight $\lambda_{\text{retain}}$ is fixed at $1.0$ for both settings.

##### Varying the tamper-resistance loss scale $\lambda_{\text{TR}}$.

We compare the downstream robustness of TAR when varying the tamper-resistance loss weighting $\lambda_{\text{TR}}$ between $1.0$ and $4.0$ in Table [6](#A4.T6 "Table 6 ‣ Excluding the initial safeguard. ‣ D.4 Ablations ‣ Appendix D Additional Analysis Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"). We observe that when setting $\lambda_{\text{TR}} = 1.0$, TAR maintains high retain MMLU accuracy at $62.5$ percentage points, with moderate tamper-resistance indicated by a Post-Attack Forget accuracy of $39.9$. Further increasing $\lambda_{\text{TR}}$ to $4.0$ in our final TAR model results in a significantly improved Post-Attack Forget Accuracy of $35.2$, with a partial decrease in Retain MMLU to $54.7$. When varying $\lambda_{\text{TR}}$, we keep $\lambda_{\text{retain}}$ constant; thus, our results indicate a clear way to increase downstream tamper-resistance by increasing the weighting of the tamper-resistance gradient during TAR, reflecting a balance between tamper-resistance and capabilities similar to the robustness-performance tradeoff for adverarial robustness in vision models.

### D.5 DPO Tamper-Resistance during TAR

Figure 8: The development of inner-loop DPO win-rates during harmful SFT attack inner loops (red), over the course of tamper-resistance training for TAR. The outer loop win-rate (blue) depicts the average win-rate across inner loops over the course of tamper-resistance training. We observe that by the end of training, the win-rate for refusal completions becomes completely flat near the optimal win-rate value of $1.0$.

In Figure [8](#A4.F8 "Figure 8 ‣ D.5 DPO Tamper-Resistance during TAR ‣ Appendix D Additional Analysis Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), we plot the DPO win-rate during harmful SFT attack trajectories during the adversarial training phase of TAR. We find that the outer-loop DPO loss steadily decreases, which corresponds to the average inner-loop win-rate of refusal completions over rejected completions steadily increasing over the $100$ outer loop steps. Our results demonstrate that TAR is able to satisfy complex tamper-resistance losses after fine-tuning. We believe that this is a useful feature of the method, enabling TAR to adapt to other potentially useful objective functions that correspond to downstream robustness.

## Appendix E Experiment Details

### E.1 Weaponization Domain Proxy Dataset Details

##### Biosecurity.

We use a synthetically labeled partition of the Pile \[[13](#bib.bib13)\] that was filtered for relevance to biology and the Camel AI Biology dataset \[[30](#bib.bib30)\]. We generate synthetic labels for Pile token sequences using openchat-3.5 \[[57](#bib.bib57)\], categorizing them as belonging to "Cellular Biology" or not. This process yields 49,984 samples: 7,558 for the Forget-set (Pile-bio Forget) and 42,426 for the Retain-set (Pile-bio Retain). Concurrently, we pack entries from the Camel AI Biology dataset to the truncation-enabled 256 tokenization limit, resulting in 54,258 samples of about 188 words each (Camel-bio Forget). We apply the same procedure to our held-out hazardous biology dataset (identical to the WMDP biosecurity Forget-set), producing 598,933 samples of similar length (OOD Forget).

##### Chemical Security.

We use a private forget dataset containing text sequences about hazardous chemical security content (Chem Forget).

##### Cybersecurity.

We scrape CTF writeups on CTFtime \[[8](#bib.bib8)\] that are numbered between 1 and 39181, collecting cybersecurity writeups written as recently as 2024. We filter to keep writeups that contain more than 150 characters. As a result of filtering and HTTP errors while scraping, our resulting forget dataset contains slightly over 18k samples (Cyber Forget).

### E.2 Train-time Settings and Adversaries

##### Weaponization knowledge restriction.

For each weaponization knowledge restriction domain, we have a corresponding retain dataset $\mathcal{D}_{\text{retain}}$, comprised of a mix of data from the Pile-bio Retain set and Magpie-Align instruction-tuning dataset \[[61](#bib.bib61)\], which we refer to as the Retain-set. Referencing the datasets described in Appendix [E.1](#A5.SS1 "E.1 Weaponization Domain Proxy Dataset Details ‣ Appendix E Experiment Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), we specify the adversary tamper-resistance datasets that constitute the data used by attacks sampled from $\mathcal{A}_{\text{train}}$ during TAR training, as well as the attack setup for each domain as follows:

- •
  Biosecurity: We simulate $6$ adversaries from the following three setups: Pile-Bio Forget-set SFT, Camel-Bio Forget-set SFT, and Retain-set SFT followed by Pile-Bio Forget-set SFT (R$\rightarrow$F), where the switching point between Retain-set and Pile-Bio Forget-set SFT within the 64-step length trajectory is sampled from a beta distribution $\beta{(6.0,3.0)}$. LRs are sampled from $\{{2 \times 10^{- 5}},{4 \times 10^{- 5}}\}$.
- •
  Chemical Security: We simulate $6$ adversaries from the following three setups: Chem Forget-set SFT, Retain-set SFT, and Retain-set followed by Chem Forget-set SFT, using the same switching-point sampling scheme as in the Biosecurity setting. LRs are sampled from $\{{2 \times 10^{- 5}},{4 \times 10^{- 5}}\}$. For chemical security, we set the tamper-resistance loss scale $\lambda_{\text{TR}}$ to 3.0.
- •
  Cybersecurity: We simulate $6$ adversaries from the following two setups: Cyber Forget-set SFT, Retain-set SFT, and Retain-set SFT followed by Cyber Forget-set SFT, using the same switching point sampling scheme as in the Chemical Security and Biosecurity settings. LRs are sampled from $\{{2 \times 10^{- 5}},{4 \times 10^{- 5}}\}$.

For each weaponization knowledge domain, we create 80-20 splits for adversary and held-out data of the corresponding forget sets, respectively. For Biosecurity, which uses multiple forget datasets, this involves creating 80-20 splits for each dataset, then combining the corresponding splits. The adversary data splits are used for sampled attacks from $\mathcal{A}_{\text{train}}$, whereas the held-out split is used for computing tamper-resistance losses. The held-out splits for each domain correspond to $\mathcal{D}_{\text{TR}}$ in Section [4](#S4 "4 Safeguard Tamper-Resistance Training ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"). We use minibatches from a held-out dataset for computing tamper-resistance losses rather than cycling through a single dataset, following the recommendation of [Nichol et al. \[41\]](#bib.bib41), in which first-order meta-learning without properly held-out minibatches caused a performance degradation.

All train-time adversary setups are tabulated in Table [7](#A5.T7 "Table 7 ‣ Weaponization knowledge restriction. ‣ E.2 Train-time Settings and Adversaries ‣ Appendix E Experiment Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), where F-Pile, F-Chem, F-Cyber denote the respective datasets described in Appendix [E.1](#A5.SS1 "E.1 Weaponization Domain Proxy Dataset Details ‣ Appendix E Experiment Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), and Retain denotes the mixed Pile-bio and Magpie-Align Retain-set described in Appendix [E.2](#A5.SS2 "E.2 Train-time Settings and Adversaries ‣ Appendix E Experiment Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"). We use R$\rightarrow$F to label the adversaries that perform Retain-set SFT followed by Forget-set SFT. The final column is an abbreviation for Finetuning Paradigm and indicates whether the SFT setup used full parameter finetuning or parameter-efficient fine-tuning (PEFT) via LoRA adapters \[[18](#bib.bib18)\].

| Adversary                                   | Dataset         | Opt. Steps ($K$) | Optimizer | LR                  | LR Schedule | Batch Size | FT Paradigm    |
|---------------------------------------------|-----------------|------------------|-----------|---------------------|-------------|------------|----------------|
| Biosecurity Weaponization Restriction       |                 |                  |           |                     |             |            |                |
| Adv 1                                       | F-Pile          | 64               | AdamW     | $2 \times 10^{- 5}$ | No Warmup   | 64         | Full Parameter |
| Adv 2                                       | F-Pile          | 64               | AdamW     | $4 \times 10^{- 5}$ | No Warmup   | 64         | Full Parameter |
| Adv 3                                       | F-Camel         | 64               | AdamW     | $2 \times 10^{- 5}$ | No Warmup   | 64         | Full Parameter |
| Adv 4                                       | F-Camel         | 64               | AdamW     | $4 \times 10^{- 5}$ | No Warmup   | 64         | Full Parameter |
| Adv 5                                       | R$\rightarrow$F | 64               | AdamW     | $2 \times 10^{- 5}$ | No Warmup   | 64         | Full Parameter |
| Adv 6                                       | R$\rightarrow$F | 64               | AdamW     | $4 \times 10^{- 5}$ | No Warmup   | 64         | Full Parameter |
| Chemical Security Weaponization Restriction |                 |                  |           |                     |             |            |                |
| Adv 1                                       | F-Chem          | 64               | AdamW     | $2 \times 10^{- 5}$ | No Warmup   | 64         | Full Parameter |
| Adv 2                                       | F-Chem          | 64               | AdamW     | $4 \times 10^{- 5}$ | No Warmup   | 64         | Full Parameter |
| Adv 3                                       | Retain          | 64               | AdamW     | $2 \times 10^{- 5}$ | No Warmup   | 64         | Full Parameter |
| Adv 4                                       | Retain          | 64               | AdamW     | $4 \times 10^{- 5}$ | No Warmup   | 64         | Full Parameter |
| Adv 5                                       | R$\rightarrow$F | 64               | AdamW     | $2 \times 10^{- 5}$ | No Warmup   | 64         | Full Parameter |
| Adv 6                                       | R$\rightarrow$F | 64               | AdamW     | $4 \times 10^{- 5}$ | No Warmup   | 64         | Full Parameter |
| Cybersecurity Weaponization Restriction     |                 |                  |           |                     |             |            |                |
| Adv 1                                       | F-Cyber         | 64               | AdamW     | $2 \times 10^{- 5}$ | No Warmup   | 64         | Full Parameter |
| Adv 2                                       | F-Cyber         | 64               | AdamW     | $4 \times 10^{- 5}$ | No Warmup   | 64         | Full Parameter |
| Adv 3                                       | Retain          | 64               | AdamW     | $2 \times 10^{- 5}$ | No Warmup   | 64         | Full Parameter |
| Adv 4                                       | Retain          | 64               | AdamW     | $4 \times 10^{- 5}$ | No Warmup   | 64         | Full Parameter |
| Adv 5                                       | R$\rightarrow$F | 64               | AdamW     | $2 \times 10^{- 5}$ | No Warmup   | 64         | Full Parameter |
| Adv 6                                       | R$\rightarrow$F | 64               | AdamW     | $4 \times 10^{- 5}$ | No Warmup   | 64         | Full Parameter |

Table 7: Train-time adversary setups for weaponization knowledge restriction of Biosecurity, Chemical Security, and Cybersecurity.

##### Harmful request refusal.

For harmful request refusal, we choose the retain dataset $\mathcal{D}_{\text{retain}}$ to be the Magpie-Align instruction-tuning dataset \[[61](#bib.bib61)\]. We sample train-time adversaries that perform $K = 64$ steps of SFT on rejected completions of the Anthropic-HH-RLHF dataset \[[3](#bib.bib3)\] and vary the learning rate within $\{{2 \times 10^{- 6}},{2 \times 10^{- 5}},{4 \times 10^{- 5}}\}$. We depict this list of adversaries in Table [8](#A5.T8 "Table 8 ‣ Harmful request refusal. ‣ E.2 Train-time Settings and Adversaries ‣ Appendix E Experiment Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs").

While the rejected completions from Anthropic-HH-RLHF constitute the data used for sampled attacks from $\mathcal{A}_{\text{train}}$ for harmful request refusal, we compute the tamper-resistance loss $\mathcal{L}_{\text{TR}}$ as follows. Since $\mathcal{L}_{\text{TR}}$ is the DPO loss \[[46](#bib.bib46)\] in this setting, we use the base model weights $\theta$ as the reference model and sample harmful and benign completions from a modified test split of Anthropic-HH-RLHF \[[3](#bib.bib3)\], where rejected completions are replaced with refusals \[[6](#bib.bib6)\]. To avoid keeping the base model weights in memory and speed up training, we precompute the reference model DPO log-probabilities for the full Anthropic-HH-RLHF dataset before training. To summarize, we have that the sampled train-time adversaries perform SFT on the rejected completions from Anthropic-HH-RLHF, and tamper-resistance DPO loss is computed on the corresponding modified refusal completions; the modified refusal completions in this setting correspond to $\mathcal{D}_{\text{TR}}$ in Section [4](#S4 "4 Safeguard Tamper-Resistance Training ‣ Tamper-Resistant Safeguards for Open-Weight LLMs").

In practice, we perform an additional $100$ steps of supervised fine-tuning on the Magpie-Align dataset to improve the benign capabilities performance of the TAR refusal model in Table [2](#S5.T2 "Table 2 ‣ Setup. ‣ 5.2 Harmful Request Refusal ‣ 5 Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs").

| Adversary               | Dataset       | Opt. Steps ($K$) | Optimizer | LR                  | LR Schedule | Batch Size | FT Paradigm    |
|-------------------------|---------------|------------------|-----------|---------------------|-------------|------------|----------------|
| Harmful Request Refusal |               |                  |           |                     |             |            |                |
| Adv 1                   | A-HH-Rejected | 64               | AdamW     | $2 \times 10^{- 5}$ | No Warmup   | 64         | Full Parameter |
| Adv 2                   | A-HH-Rejected | 64               | AdamW     | $2 \times 10^{- 6}$ | No Warmup   | 64         | Full Parameter |
| Adv 3                   | A-HH-Rejected | 64               | AdamW     | $4 \times 10^{- 5}$ | No Warmup   | 64         | Full Parameter |

Table 8: Train-time adversary red-teaming setups harmful request refusal. “A-HH-Rejected” in the Dataset column corresponds to the adversary dataset comprised of rejected completions from the Anthropic-HH-RLHF dataset.

## Appendix F Red Teaming Details

### F.1 Weaponization Knowledge Restriction

In Table [9](#A6.T9 "Table 9 ‣ F.1 Weaponization Knowledge Restriction ‣ Appendix F Red Teaming Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), we list all test-time adversary setups for recovering Biosecurity, Chemical Security, and Cybersecurity Weaponization knowledge.

For Biosecurity, we examine post-attack forget accuracy after fine-tuning for $500$ steps on three data distributions: the Pile-bio Forget set and the Retain-set used during Random Mapping and TAR, and an OOD-Forget set mentioned in Appendix [E.1](#A5.SS1 "E.1 Weaponization Domain Proxy Dataset Details ‣ Appendix E Experiment Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), which is unseen during tamper-resistance training.

We leverage a consistent setup for Chemical Security and Cybersecurity, substituting the Pile-bio Forget set for the respective Chem and Cyber Forget sets. We exclude the unseen forget distribution adversaries for a total of $24$ attacks, as we were unable to obtain an equally high quality held-out dataset for Chemical Security and Cybersecurity.

For all subjects, we compare the effect of different optimizers (AdamW, Adadelta, and Stochastic Gradient Descent with Nesterov Momentum, Schedule Free AdamW) \[[66](#bib.bib66), [27](#bib.bib27), [60](#bib.bib60), [9](#bib.bib9)\], learning rates $({2 \times 10^{- 6}},{2 \times 10^{- 5}},{4 \times 10^{- 5}})$, and learning rate scheduling techniques (SGDR and $30$ steps of linear warmup) \[[35](#bib.bib35)\].

Similar to Table [7](#A5.T7 "Table 7 ‣ Weaponization knowledge restriction. ‣ E.2 Train-time Settings and Adversaries ‣ Appendix E Experiment Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), we use F-Pile, F-Chem, F-Cyber, and OOD-F in the Dataset Column to denote the respective datasets described in Appendices [F.1](#A6.SS1 "F.1 Weaponization Knowledge Restriction ‣ Appendix F Red Teaming Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"). At test-time, we use the Pile-bio Retain set as the global Retain-set adversary, labeled as Retain. The R→F adversary at test-time also differs from the train-time version: we perform Forget-set SFT for 40% of the optimization steps, followed by Retain-set SFT for the remaining 60%. We found this combination to be a potent attack that broke intermediate versions of the method, as described in Appendix [D.2](#A4.SS2 "D.2 Targeted Patching of Vulnerabilities ‣ Appendix D Additional Analysis Experiments ‣ Tamper-Resistant Safeguards for Open-Weight LLMs").

In the Optimizer column, Schedule Free is an abbreviation of Schedule Free AdamW and SGD Nesterov is an abbreviation of SGD with Nesterov Momentum. In cases where the adversary used parameter-efficient fine-tuning (PEFT) via LoRA adapters \[[18](#bib.bib18)\], we used a LoRA config with an attention dimension, or rank, of $16$, a LoRA alpha value of $32$, a LoRA dropout of 0.05, on target linear modules:

$\{{\text{‘up\_proj’},\text{‘down\_proj’},\text{‘gate\_proj’},\text{‘q\_proj’},\text{‘k\_proj’},\text{‘v\_proj’},\text{‘o\_proj’}}\}$.

Lastly, for each Weaponization Knowledge Restriction domain, we red-team the TAR model with three runs of supervised fine-tuning attacks from each adversary, using different random seeds. We then calculate the final post-attack value for each adversary by averaging these three replicates.

| Adversary                               | Dataset         | Opt. Steps ($K$) | Optimizer     | LR                  | LR Schedule     | Batch Size | FT Paradigm    |
|-----------------------------------------|-----------------|------------------|---------------|---------------------|-----------------|------------|----------------|
| Biosecurity Weaponization Restriction   |                 |                  |               |                     |                 |            |                |
| Adv 1                                   | F-Pile          | 500              | AdamW         | $2 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 2                                   | F-Pile          | 500              | AdamW         | $4 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 3                                   | Retain          | 500              | AdamW         | $2 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 4                                   | Retain          | 500              | AdamW         | $4 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 5                                   | OOD-F           | 500              | AdamW         | $2 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 6                                   | OOD-F           | 500              | AdamW         | $4 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 7                                   | R$\rightarrow$F | 500              | AdamW         | $2 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 8                                   | R$\rightarrow$F | 500              | AdamW         | $4 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 9                                   | F-Pile          | 500              | Adadelta      | $2 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 10                                  | F-Pile          | 500              | Adadelta      | $4 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 11                                  | F-Pile          | 500              | Schedule Free | $2 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 12                                  | F-Pile          | 500              | Schedule Free | $4 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 13                                  | F-Pile          | 500              | SGD Nesterov  | $2 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 14                                  | F-Pile          | 500              | SGD Nesterov  | $4 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 15                                  | F-Pile          | 500              | AdamW         | $2 \times 10^{- 6}$ | No Warmup       | 64         | Full Parameter |
| Adv 16                                  | F-Pile          | 500              | AdamW         | $2 \times 10^{- 6}$ | 30 Steps Warmup | 64         | Full Parameter |
| Adv 17                                  | F-Pile          | 500              | AdamW         | $2 \times 10^{- 5}$ | 30 Steps Warmup | 64         | Full Parameter |
| Adv 18                                  | F-Pile          | 500              | AdamW         | $4 \times 10^{- 5}$ | 30 Steps Warmup | 64         | Full Parameter |
| Adv 19                                  | F-Pile          | 500              | AdamW         | $2 \times 10^{- 5}$ | SGDR            | 64         | Full Parameter |
| Adv 20                                  | F-Pile          | 500              | AdamW         | $4 \times 10^{- 5}$ | SGDR            | 64         | Full Parameter |
| Adv 21                                  | F-Pile          | 500              | AdamW         | $2 \times 10^{- 5}$ | No Warmup       | 32         | Full Parameter |
| Adv 22                                  | F-Pile          | 500              | AdamW         | $4 \times 10^{- 5}$ | No Warmup       | 32         | Full Parameter |
| Adv 23                                  | F-Pile          | 500              | AdamW         | $2 \times 10^{- 5}$ | No Warmup       | 128        | Full Parameter |
| Adv 24                                  | F-Pile          | 500              | AdamW         | $4 \times 10^{- 5}$ | No Warmup       | 128        | Full Parameter |
| Adv 25                                  | F-Pile          | 500              | AdamW         | $2 \times 10^{- 5}$ | No Warmup       | 64         | PEFT           |
| Adv 26                                  | F-Pile          | 500              | AdamW         | $4 \times 10^{- 5}$ | No Warmup       | 64         | PEFT           |
| Chemical Security Weaponization         |                 |                  |               |                     |                 |            |                |
| Adv 1                                   | F-Chem          | 500              | AdamW         | $2 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 2                                   | F-Chem          | 500              | AdamW         | $4 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 3                                   | Retain          | 500              | AdamW         | $2 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 4                                   | Retain          | 500              | AdamW         | $4 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 5                                   | R$\rightarrow$F | 500              | AdamW         | $2 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 6                                   | R$\rightarrow$F | 500              | AdamW         | $4 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 7                                   | F-Chem          | 500              | Adadelta      | $2 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 8                                   | F-Chem          | 500              | Adadelta      | $4 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 9                                   | F-Chem          | 500              | ScheduleFree  | $2 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 10                                  | F-Chem          | 500              | ScheduleFree  | $4 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 11                                  | F-Chem          | 500              | SGD Nesterov  | $2 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 12                                  | F-Chem          | 500              | SGD Nesterov  | $4 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 13                                  | F-Chem          | 500              | AdamW         | $2 \times 10^{- 6}$ | No Warmup       | 64         | Full Parameter |
| Adv 14                                  | F-Chem          | 500              | AdamW         | $2 \times 10^{- 6}$ | 30 Steps Warmup | 64         | Full Parameter |
| Adv 15                                  | F-Chem          | 500              | AdamW         | $2 \times 10^{- 5}$ | 30 Steps Warmup | 64         | Full Parameter |
| Adv 16                                  | F-Chem          | 500              | AdamW         | $4 \times 10^{- 5}$ | 30 Steps Warmup | 64         | Full Parameter |
| Adv 17                                  | F-Chem          | 500              | AdamW         | $2 \times 10^{- 5}$ | SGDR            | 64         | Full Parameter |
| Adv 18                                  | F-Chem          | 500              | AdamW         | $4 \times 10^{- 5}$ | SGDR            | 64         | Full Parameter |
| Adv 19                                  | F-Chem          | 500              | AdamW         | $2 \times 10^{- 5}$ | No Warmup       | 32         | Full Parameter |
| Adv 20                                  | F-Chem          | 500              | AdamW         | $4 \times 10^{- 5}$ | No Warmup       | 32         | Full Parameter |
| Adv 21                                  | F-Chem          | 500              | AdamW         | $2 \times 10^{- 5}$ | No Warmup       | 128        | Full Parameter |
| Adv 22                                  | F-Chem          | 500              | AdamW         | $4 \times 10^{- 5}$ | No Warmup       | 128        | Full Parameter |
| Adv 23                                  | F-Chem          | 500              | AdamW         | $2 \times 10^{- 5}$ | No Warmup       | 64         | PEFT           |
| Adv 24                                  | F-Chem          | 500              | AdamW         | $4 \times 10^{- 5}$ | No Warmup       | 64         | PEFT           |
| Cybersecurity Weaponization Restriction |                 |                  |               |                     |                 |            |                |
| Adv 1                                   | F-Cyber         | 500              | AdamW         | $2 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 2                                   | F-Cyber         | 500              | AdamW         | $4 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 3                                   | Retain          | 500              | AdamW         | $2 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 4                                   | Retain          | 500              | AdamW         | $4 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 5                                   | R$\rightarrow$F | 500              | AdamW         | $2 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 6                                   | R$\rightarrow$F | 500              | AdamW         | $4 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 7                                   | F-Cyber         | 500              | Adadelta      | $2 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 8                                   | F-Cyber         | 500              | Adadelta      | $4 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 9                                   | F-Cyber         | 500              | ScheduleFree  | $2 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 10                                  | F-Cyber         | 500              | ScheduleFree  | $4 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 11                                  | F-Cyber         | 500              | SGD Nesterov  | $2 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 12                                  | F-Cyber         | 500              | SGD Nesterov  | $4 \times 10^{- 5}$ | No Warmup       | 64         | Full Parameter |
| Adv 13                                  | F-Cyber         | 500              | AdamW         | $2 \times 10^{- 6}$ | No Warmup       | 64         | Full Parameter |
| Adv 14                                  | F-Cyber         | 500              | AdamW         | $2 \times 10^{- 6}$ | 30 Steps Warmup | 64         | Full Parameter |
| Adv 15                                  | F-Cyber         | 500              | AdamW         | $2 \times 10^{- 5}$ | 30 Steps Warmup | 64         | Full Parameter |
| Adv 16                                  | F-Cyber         | 500              | AdamW         | $4 \times 10^{- 5}$ | 30 Steps Warmup | 64         | Full Parameter |
| Adv 17                                  | F-Cyber         | 500              | AdamW         | $2 \times 10^{- 5}$ | SGDR            | 64         | Full Parameter |
| Adv 18                                  | F-Cyber         | 500              | AdamW         | $4 \times 10^{- 5}$ | SGDR            | 64         | Full Parameter |
| Adv 19                                  | F-Cyber         | 500              | AdamW         | $2 \times 10^{- 5}$ | No Warmup       | 32         | Full Parameter |
| Adv 20                                  | F-Cyber         | 500              | AdamW         | $4 \times 10^{- 5}$ | No Warmup       | 32         | Full Parameter |
| Adv 21                                  | F-Cyber         | 500              | AdamW         | $2 \times 10^{- 5}$ | No Warmup       | 128        | Full Parameter |
| Adv 22                                  | F-Cyber         | 500              | AdamW         | $4 \times 10^{- 5}$ | No Warmup       | 128        | Full Parameter |
| Adv 23                                  | F-Cyber         | 500              | AdamW         | $2 \times 10^{- 5}$ | No Warmup       | 64         | PEFT           |
| Adv 24                                  | F-Cyber         | 500              | AdamW         | $4 \times 10^{- 5}$ | No Warmup       | 64         | PEFT           |

Table 9: Test-time adversary red-teaming setups for weaponization knowledge restriction of Biosecurity, Chemical Security, and Cybersecurity.

### F.2 Harmful Request Refusal

For the harmful request refusal setting, we conduct $5$ test-time adversary attacks that perform SFT for $10$ epochs on a held-out toxicity dataset called Toxic-DPO v0.2, on each of the settings in Table [10](#A6.T10 "Table 10 ‣ F.2 Harmful Request Refusal ‣ Appendix F Red Teaming Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"). The dataset contains $541$ user-assistant chat interactions where the assistant complies with harmful instructions.

| Adversary               | Dataset  | Epochs | Optimizer | LR                  | LR Schedule     | Batch Size | FT Paradigm    |
|-------------------------|----------|--------|-----------|---------------------|-----------------|------------|----------------|
| Harmful Request Refusal |          |        |           |                     |                 |            |                |
| Adv 1                   | ToxicDPO | 10     | AdamW     | $1 \times 10^{- 5}$ | 10 Steps Warmup | 32         | Full Parameter |
| Adv 2                   | ToxicDPO | 10     | AdamW     | $1 \times 10^{- 5}$ | No Warmup       | 32         | Full Parameter |
| Adv 3                   | ToxicDPO | 10     | AdamW     | $1 \times 10^{- 5}$ | No Warmup       | 16         | Full Parameter |
| Adv 4                   | ToxicDPO | 10     | AdamW     | $2 \times 10^{- 5}$ | No Warmup       | 32         | Full Parameter |
| Adv 5                   | ToxicDPO | 10     | AdamW     | $4 \times 10^{- 5}$ | No Warmup       | 32         | Full Parameter |

Table 10: Test-time adversary red-teaming setups for harmful request refusal. “ToxicDPO” in the Dataset column refers to the ToxicDPOv0.2 dataset containing harmful chat completions.

#### F.2.1 Additional Harmful Request Refusal Results

|                 |              |         |                    |
|-----------------|--------------|---------|--------------------|
| Model           | Pre-Attacks  |         | Post-Attacks (Avg) |
|                 | MT-Bench (↑) | ASR (↓) | ASR (↓)            |
| Refusal Trained | 8.1          | 14.7    | 72.5               |
| R2D2            | 6.0          | 25.0    | 78.3               |
| RepNoise        | 6.2          | 18.8    | 74.5               |
| RR              | 8.0          | 1.4     | 84.8               |
| TAR (Ours)      | 6.3          | 31.4    | 63.9               |

Table 11: Average Post-Attack HarmBench ASR, reported for TAR, Representation Rerouting (RR), and the Refusal Trained Llama-3-8B-Instruct model across $5$ fine-tuning attacks depicted in Table [10](#A6.T10 "Table 10 ‣ F.2 Harmful Request Refusal ‣ Appendix F Red Teaming Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), as well as Pre-Attack MT-Bench and HarmBench ASR. TAR is more robust than other methods after tampering, while maintaining comparable MT-Bench performance. Note that Pre-Attack ASR is not a priority for us, as we focus on reducing ASR after tampering attacks. To improve both metrics, future work could consider combining tamper-resistance training with a strong baseline safeguard like RR. ASR values are percentages.

## Appendix G Baseline Details

### G.1 Weaponization Knowledge Restriction

##### Max Entropy.

Let $K$ be the set of all token-wise output probability distributions returned by a model $\theta$, where $k \in K$ corresponds to every position in the sequence. We maximize the average entropy of these discrete distributions in $K$ as follows:

|     |                                                                                                            |     |
|-----|------------------------------------------------------------------------------------------------------------|-----|
|     | $$\mathcal{L}_{\text{Max Entropy}} = {\sum\limits_{k \in \mathcal{K}}{p_{k}\hspace{0pt}{\log{(p_{k})}}}}$$ |     |

This is equivalent to minimizing the average Kullback-Leibler (KL) divergence \[[29](#bib.bib29)\] between each $k$ and the discrete uniform distribution $u{(x)}$ over the vocabulary $V$. For Llama-3-8B-Instruct, ${|V|} = 128256$. Thus, this objective is upper-bounded by:

|     |                                                                       |     |
|-----|-----------------------------------------------------------------------|-----|
|     | $${h{(x)}} = {- {\log{({u{(x)}})}}} = {\log{({|V|})}} \approx 11.76$$ |     |

where $h{(x)}$ measures the Shannon information or self-information and $\log{(x)}$ has base $e$. We apply this objective for all elements in the Forget-set and perform standard cross-entropy on the Retain-set.

##### Min Posterior.

The goal of the Min Posterior objective is to assign lower probabilities to true forget-set labels, essentially minimizing $- {\log{({1 - {P{(\text{label})}}})}}$. Let $p_{i}$ be the probability assigned to the true label for token $i$ and $\mathcal{V}$ be the model’s vocabulary distribution. We define the Min Posterior objective function as follows:

|     |                                                                                                                                                                                         |     |
|-----|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $$\mathcal{L}_{\text{Min Posterior}} = - \frac{1}{|\mathcal{V}|}\sum\limits_{i \in \mathcal{V}}\log{(1 - p_{i} + \epsilon)} \cdot {\mathbb{I}}{\lbrack\log{(p_{i})} \geq \tau\rbrack}$$ |     |

where $\tau$ is the threshold for masking out target label logits (which we set to the negative maximum entropy of the vocabulary distribution, $- {\log{|\mathcal{V}|}}$) and ${\mathbb{I}}{\lbrack \cdot \rbrack}$ is the corresponding indicator function (1 if the condition is true, 0 otherwise). We include an optional $\epsilon = {1 \times 10^{- 12}}$ to help with numerical stability. Similar to the Max Entropy objective, we apply this objective for all elements in the Forget-set and perform standard cross-entropy on the Retain-set.

##### RMU.

We adapt RMU’s implementation from [Li et al. \[31\]](#bib.bib31) with a learning rate of $5 \times 10^{- 5}$ and $250$ unlearning steps. We use the released WMDP’s unlearning datasets for Biosecurity (Bio) and Cybersecurity (Cyber) unlearning, and our private hazardous chemistry dataset for Chemical Security (Chem) unlearning. We use unlearning coefficients of $20$, $30$, and $50$ for Bio, Cyber, and Chem respectively. We use a retain coefficient of $700$ on Wikitext \[[39](#bib.bib39)\].

##### LLMU.

We use a modified version of LLMU from [Yao et al. \[63\]](#bib.bib63). Instead of computing the KL divergence to regularize retain-set logits towards the base frozen model, we employ a standard cross-entropy loss. This modification allows for memory-efficient execution on our hardware while maintaining comparable performance.

##### Hyperparameter tuning.

Besides RMU, all baseline hyperparameters were chosen after a grid search across learning rates $\{ 3 \times 10^{- 6}$, $5 \times 10^{- 6}$, $8 \times 10^{- 6}$, $1 \times 10^{- 5}\}$, optimization step count $\{ 600$, $1000\}$, and warmup steps $\{ 0,100\}$. We found that $600$ optimization steps using the AdamW Schedule Free optimizer, at a learning rate of $1 \times 10^{- 5}$, with 100 steps of linear warmup, and an effective batch size of 64 produced the best performance. For the Max Entropy, Min Posterior, and LLMU baselines, we train on the three corresponding forget datasets discussed in [E.1](#A5.SS1 "E.1 Weaponization Domain Proxy Dataset Details ‣ Appendix E Experiment Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"). For these baselines, we modify our Biosecurity forget corpus to be a mixture of the Pile-bio and Camel-bio Forget corpora. We use the Pile-bio Retain-set as a global Retain-set for baseline training.

### G.2 Harmful Request Refusal

##### Representation Rerouting.

We use the Llama-3-8B-Instruct RR model from [Zou et al. \[75\]](#bib.bib75), which uses a cosine distance loss to push representations for harmful inputs to become orthogonal to those of the base Llama-3-8B-Instruct model.

##### R2D2.

We use the R2D2 model run on Zephyr-7B directly from [Mazeika et al. \[37\]](#bib.bib37), which performs adversarial training against GCG attacks to increase jailbreak robustness.

##### RepNoise.

We the RepNoise model run on Llama-2-7B directly from [Rosati et al. \[51\]](#bib.bib51), which uses a distributional loss to push representations for harmful inputs toward Gaussian noise.

### G.3 Additional Baseline Comparisons

|                   |            |             |            |                    |
|-------------------|------------|-------------|------------|--------------------|
| Domain            | Model      | Pre-Attacks |            | Post-Attacks (Avg) |
|                   |            | Retain (↑)  | Forget (↓) | Forget (↓)         |
| Biosecurity       | Random     | 25.0        | 25.0       | 25.0               |
|                   | MLAC-AR    | 49.1        | 31.2       | 50.6               |
|                   | SOPHON-AR  | 27.2        | 24.0       | 28.3               |
|                   | TAR (Ours) | 54.7        | 28.1       | 35.2               |
| Chemical Security | Random     | 25.0        | 25.0       | 25.0               |
|                   | MLAC-AR    | 47.8        | 29.9       | 33.6               |
|                   | SOPHON-AR  | 23.3        | 26.2       | 26.1               |
|                   | TAR (Ours) | 56.5        | 28.4       | 27.1               |
| Cybersecurity     | Random     | 25.0        | 25.0       | 25.0               |
|                   | MLAC-AR    | 36.0        | 26.6       | 35.1               |
|                   | SOPHON-AR  | 24.4        | 24.6       | 30.4               |
|                   | TAR (Ours) | 60.7        | 23.6       | 28.6               |

Table 12: Additional baselines for MLAC-AR, an extension of the method in [Henderson et al. \[16\]](#bib.bib16) to autoregressive LLMs, as well as SOPHON-AR from [Deng et al. \[10\]](#bib.bib10), respectively. Despite extensive tuning, SOPHON-AR does not yield a usable model. Additionally, MLAC-AR has varying robustness and worse Retain MMLU performance.

##### MLAC-AR.

Meta-Learned Adversarial Censoring (MLAC) \[[16](#bib.bib16)\] was originally proposed to prevent BERT-style models from learning binary classification for gender bias data. Since the approach is not immediately applicable to LLMs, we extend MLAC in a variant we call autoregressive MLAC (MLAC-AR). Since MLAC in its original formulation calls for “task-blocking” via negating the adversary’s loss during the inner loop of meta-learning, we implement this by negating the cross-entropy loss of an LLM fine-tuning adversary. However, we found that this approach diverges in performance across a variety of hyperparameters, and opted to further improve performance of the MLAC-AR baseline by clamping the maximum cross-entropy loss at the value of the maximum entropy of the output vocabulary distribution, $\log{(\text{vocab\_size})}$. We show results in Table [12](#A7.T12 "Table 12 ‣ G.3 Additional Baseline Comparisons ‣ Appendix G Baseline Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs"), finding that MLAC-AR does not maintain sufficient benign capabilities performance nor uniform tamper-resistance across weaponization domains.

##### SOPHON-AR.

In concurrent work, SOPHON \[[10](#bib.bib10)\] was introduced to prevent small diffusion models and image classifiers from learning specific data distributions. Similarly to MLAC-AR, we extend SOPHON to LLMs via SOPHON-AR, using the alternating retain loss and fine-tuning suppression loss formulation that the authors propose. Furthermore, we adapt the inverse cross-entropy loss from [Deng et al. \[10\]](#bib.bib10) , which aims to boost convergence of the fine-tuning suppression process. We find in practice that despite heavy tuning, SOPHON-AR does not converge well enough to yield a usable Pre-Attack model in Table [12](#A7.T12 "Table 12 ‣ G.3 Additional Baseline Comparisons ‣ Appendix G Baseline Details ‣ Tamper-Resistant Safeguards for Open-Weight LLMs").

Experimental support, please [view the build logs](./2408.00761v4/__stdout.txt) for errors. Generated by [ L A T E xml ![\[LOGO\]](img)](https://math.nist.gov/~BMiller/LaTeXML/) .

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
