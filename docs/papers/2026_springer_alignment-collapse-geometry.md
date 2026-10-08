---
title: "The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"
authors: "Max Springer et al."
year: 2026
source: https://arxiv.org/html/2602.15799v1
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

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) [![](img) Report Issue](# "Report an Issue") [![](img) Back to Abstract](/abs/2602.15799v1 "Back to abstract page") [![](img) Download PDF](/pdf/2602.15799v1 "Download PDF") [![](img)](javascript:toggleNavTOC(); "Toggle navigation") [![](img)](javascript:toggleReadingMode(); "Disable reading mode, show header and footer")

![](img) ![](img) ![](img)

1.  [1 Introduction](#S1 "In The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
2.  [2 Related Work](#S2 "In The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
    1.  [Geometric and Manifold-Based Approaches.](#S2.SS0.SSS0.Px1 "In 2 Related Work ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
    2.  [Alignment Drift and Critical Parameters.](#S2.SS0.SSS0.Px2 "In 2 Related Work ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
    3.  [Theoretical Frameworks for Skill Emergence and Adaptation.](#S2.SS0.SSS0.Px3 "In 2 Related Work ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
3.  [3 Model & Preliminaries](#S3 "In The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
    1.  [3.1 Alignment as Skill Utility](#S3.SS1 "In 3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
    2.  [3.2 Local Geometry and Fisher Information](#S3.SS2 "In 3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
    3.  [3.3 Low-Rank Sensitivity Structure](#S3.SS3 "In 3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
4.  [4 Why Flat Geometry Fails](#S4 "In The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
    1.  [4.1 Benign Fine-Tuning in the Flat Regime](#S4.SS1 "In 4 Why Flat Geometry Fails ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
    2.  [4.2 Empirical Alignment Drift](#S4.SS2 "In 4 Why Flat Geometry Fails ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
    3.  [4.3 Failure of Static Geometry](#S4.SS3 "In 4 Why Flat Geometry Fails ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
5.  [5 Alignment Instability Condition](#S5 "In The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
    1.  [5.1 Intuition Behind Two Degradation Regimes](#S5.SS1 "In 5 Alignment Instability Condition ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
    2.  [5.2 Geometric Intuition: Curvature as Steering](#S5.SS2 "In 5 Alignment Instability Condition ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
    3.  [5.3 Formal Definition](#S5.SS3 "In 5 Alignment Instability Condition ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
6.  [6 Consequences of AIC](#S6 "In The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
    1.  [6.1 Projection of Misalignment Inevitability](#S6.SS1 "In 6 Consequences of AIC ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
    2.  [6.2 Curvature-Induced Drift](#S6.SS2 "In 6 Consequences of AIC ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
    3.  [6.3 Combing Geometry and Dynamics](#S6.SS3 "In 6 Consequences of AIC ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
7.  [7 Experiments](#S7 "In The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
    1.  [7.1 Low-Rank Fisher Structure](#S7.SS1 "In 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
    2.  [7.2 Geometric Overlap and Misalignment](#S7.SS2 "In 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
8.  [8 Discussion & Implications](#S8 "In The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
9.  [References](#bib "In The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
10. [A Omitted Proofs](#A1 "In The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
    1.  [A.1 Proofs from Section ](#A1.SS1 "In Appendix A Omitted Proofs ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
    2.  [A.2 Proofs from Section ](#A1.SS2 "In Appendix A Omitted Proofs ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
    3.  [A.3 Proofs from Section ](#A1.SS3 "In Appendix A Omitted Proofs ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
    4.  [A.4 Connection to Sensitive Subspace in Representation and Low Rankness of Weight Matrix](#A1.SS4 "In Appendix A Omitted Proofs ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
        1.  [Setup and Notation.](#A1.SS4.SSS0.Px1 "In A.4 Connection to Sensitive Subspace in Representation and Low Rankness of Weight Matrix ‣ Appendix A Omitted Proofs ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
11. [B Non-Static Fisher Information](#A2 "In The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
12. [C Relaxation of Assumption ](#A3 "In The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
13. [D Expanded Experimental Results & Details](#A4 "In The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
    1.  [D.1 Full Results](#A4.SS1 "In Appendix D Expanded Experimental Results & Details ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
    2.  [D.2 Dataset Details](#A4.SS2 "In Appendix D Expanded Experimental Results & Details ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
    3.  [D.3 Fine-tuning Details](#A4.SS3 "In Appendix D Expanded Experimental Results & Details ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")
    4.  [D.4 Harmfulness Evaluation Details](#A4.SS4 "In Appendix D Expanded Experimental Results & Details ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")

[License: CC BY 4.0](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2602.15799v1 \[cs.LG\] 17 Feb 2026

# The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety

Max Springer    Chung Peng Lee    Blossom Metevier    Jane Castleman    Bohdan Turbal    Hayoung Jung    Zeyu Shen    Aleksandra Korolova

August 24, 2026

## 1 Introduction

Fine-tuning a language model on a dataset of math problems breaks its safety guardrails \[[12](#bib.bib33)\]. Training on creative writing examples erodes medical advice safeguards \[[1](#bib.bib18), [64](#bib.bib55)\]. Adapting for code generation compromises refusal mechanisms \[[6](#bib.bib23)\]. These are not hypothetical risks—they are documented, reproducible phenomena that occur even when fine-tuning datasets contain no harmful content and developers have no adversarial intent  \[[6](#bib.bib23), [24](#bib.bib42), [25](#bib.bib28), [44](#bib.bib21)\]. The central puzzle of alignment preservation is thus:

*Why does adapting a model for one capability seemingly unpredictably degrade unrelated safety properties?*

The question is urgent because fine-tuning has become the dominant paradigm for deploying language models. In domains where technical expertise, compute resources, and specialized data are limited, fine-tuning open weight models represents the primary path to leverage AI capabilities for practitioners. The ecosystem of open-weight models has expanded rapidly \[[7](#bib.bib20), [9](#bib.bib17), [10](#bib.bib19), [31](#bib.bib15), [40](#bib.bib16)\], enabling innovation but also creating vulnerability. Current defenses are largely reactive, targeting specific attack patterns \[[18](#bib.bib27)\] or imposing first-order gradient constraints \[[16](#bib.bib5), [39](#bib.bib50), [65](#bib.bib12)\] that easily break even without adversarial intent \[[26](#bib.bib25), [63](#bib.bib26)\]. Without understanding the underlying mechanisms of alignment degradation, we cannot build robust safeguards.

![](img)

Figure 1: Local alignment instability under fine-tuning dynamics. An illustrative loss landscape showing a fine-tuning trajectory (black arrow) evolving near a ridge separating basins of low alignment utility. Although the initial gradient direction is nearly tangent to the ridge, induced acceleration toward a high-curvature alignment-sensitive direction (red/blue arrow), leads to departure.

The Paradox of High-Dimensional Orthogonality. Empirical evidence reveals a striking pattern: alignment appears to reside in a small subspace of the parameter space. \[[60](#bib.bib24)\] demonstrates that pruning just $3\%$ of specific weights triggers catastrophic safety collapse, while removing similar proportions of weights from other parts of the model leaves its capabilities intact. We call these directions *alignment-sensitive*: parameter updates along them degrade safety, while updates in orthogonal directions should preserve it. This suggests alignment is governed by a low-dimensional set of sensitive directions. In a model with billions of parameters, standard geometric intuition predicts that fine-tuning updates for unrelated tasks should be nearly orthogonal to these directions, thus, safe \[[5](#bib.bib51), [35](#bib.bib49)\]. Yet degradation occurs frequently across diverse tasks and model families, exhibiting consistent patterns \[[6](#bib.bib23), [25](#bib.bib28), [44](#bib.bib21)\].

Existing theoretical frameworks do not fully resolve this paradox. Approaches based on data overlap \[[25](#bib.bib28), [26](#bib.bib25), [63](#bib.bib26)\] cannot fully explain why superficially similar tasks have vastly different safety impacts. First-order geometric constraints assume static sensitivity subspaces and fail to account for how fine-tuning trajectories evolve over time \[[5](#bib.bib51), [45](#bib.bib11)\]. Null-space methods \[[39](#bib.bib50), [65](#bib.bib12)\] presuppose we can identify and avoid alignment-sensitive directions but offer no explanation for why avoidance fails in practice.

Our Contributions. We resolve this paradox by developing a theory of alignment degradation grounded in the curvature of trajectories in parameter space. Our key insight is that while initial fine-tuning updates may indeed be orthogonal to alignment-sensitive directions, this orthogonality is unstable under the dynamics of gradient descent. The curvature of the fine-tuning objective—captured by second-order terms in the loss landscape—systematically bends trajectories into alignment-sensitive subspaces, even when first-order updates point away from them.

We formalize this mechanism through the Alignment Instability Condition (AIC), which identifies three interacting structural properties arising from the model’s geometry and the fine-tuning task.

1.  1.
    Low-Rank Sensitivity: alignment for a given skill (or capability) concentrates in a small subspace with sharp curvature, characterized by the leading eigenvectors of the Fisher information matrix.
2.  2.
    Initial Orthogonality: fine-tuning gradients for unrelated tasks have negligible first-order projection onto this subspace, creating the illusion of safety.
3.  3.
    Curvature Coupling: second-order terms in the gradient flow induce nontrivial acceleration into the alignment-sensitive subspace, forcing trajectories to drift despite initial orthogonality.

Under the AIC, we prove that alignment degradation is not merely possible, but structurally inevitable within the trust region of the aligned model. Our main theoretical results are:

###### Theorem 1.1 (Informal Version of Theorem [6.1](#S6.Thmtheorem1 "Theorem 6.1. ‣ 6.1 Projection of Misalignment Inevitability ‣ 6 Consequences of AIC ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")).

Movement in the alignment-sensitive subspace $M_{i} \subseteq {\mathbb{R}}^{n}$ incurs quadratic utility loss, $\Omega{({\lambda\hspace{0pt}{\|{P_{i}\hspace{0pt}{({\Delta\hspace{0pt}\theta})}}\|}^{2}})}$ where $\lambda$ is the minimum curvature in $M_{i}$ and $P_{i}$ projects onto this subspace.

###### Theorem 1.2 (Informal Version of Theorem [6.2](#S6.Thmtheorem2 "Theorem 6.2. ‣ 6.2 Curvature-Induced Drift ‣ 6 Consequences of AIC ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")).

Along gradient flow trajectories, $\theta{(t)}$ where ${\theta{(0)}} = \theta^{\ast}$, satisfying the AIC, projection on $M_{i}$ grows quadratically: ${\|{P_{i}\hspace{0pt}{({{\theta{(t)}} - \theta^{\ast}})}}\|} = {\Omega{({\gamma\hspace{0pt}t^{2}})}}$, where $\gamma$ quantifies curvature coupling.

The two main theorems combine to yield a quartic scaling law for alignment degradation within our utility-based framework (defined in Section [3](#S3 "3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")).

###### Corollary 1.3 (Informal Version of Corollary [6.3](#S6.Thmtheorem3 "Corollary 6.3 (Quartic Onset of Alignment Degradation). ‣ 6.3 Combing Geometry and Dynamics ‣ 6 Consequences of AIC ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")).

Combining geometric loss with quadratic drift yields alignment degradation scaling as $\Omega{({\lambda\hspace{0pt}\gamma^{2}\hspace{0pt}t^{4}})}$ in early training.

The quartic scaling law provides a principled explanation for rapid, seemingly sudden safety failures observed in practice \[[20](#bib.bib52), [42](#bib.bib9), [43](#bib.bib22), [60](#bib.bib24)\]. Even small amounts of curvature coupling ($\gamma$) compound dramatically through the fourth power, causing trajectories to escape safety basins faster than first-order analysis would predict.

Implications. Our theory reveals that alignment fragility is not an artifact of adversarial attacks or fixable through better data curation. Rather, it is an intrinsic geometric property of fine-tuning in high-dimensions. The AIC explains why: (1) benign tasks break safety, (2) low-rank adaptations fail, and (3) first-order defenses are insufficient. Our results necessitate a fundamental rethinking of alignment preservation strategies. In Section [7](#S7 "7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), we empirically validate these predictions, showing that our notion of geometric overlap provides a principled explanation for degradation of alignment.

## 2 Related Work

Our work is positioned at the intersection of several research domains: the geometric analysis of neural network parameter spaces, the empirical study of alignment fragility, and the theoretical frameworks of multi-task and meta-learning. We here discuss related studies which were not covered in the main text.

#### Geometric and Manifold-Based Approaches.

The conceptualization of neural network representations and parameter spaces through a geometric lens is well-established \[[2](#bib.bib54), [47](#bib.bib40), [54](#bib.bib53)\]. This line of inquiry is broadly motivated by the manifold hypothesis \[[46](#bib.bib3)\], which posits that high-dimensional data, such as inputs for unsupervised learning or distinct classes for classification, concentrates near low-dimensional manifolds separated by regions of low density. More recently, this geometric perspective has been directly applied to the process of fine-tuning \[[38](#bib.bib10)\]. Specifically, Low-Rank Adaptation (LoRA) has been theoretically framed as a problem of manifold geometry \[[29](#bib.bib4)\]. This aligns with foundational work in numerical optimization that analyzes fixed-rank matrices as an embedded geometry, even outside the context of model fine-tuning \[[46](#bib.bib3)\].

While these approaches provide valuable intuition, they often treat alignment geometry as static. Recent work has attempted to identify null-spaces to the alignment weight subspace in an effort to constrain fine-tuning \[[65](#bib.bib12)\]. However, these methods typically assume a flat local geometry that does not account for the empirical fragility of alignment in high-dimensions—a gap our work addresses by integrating this geometric view with a probabilistic analysis of curvature-induced drift.

#### Alignment Drift and Critical Parameters.

Empirical research confirms that fine-tuning modifies only a small subset of the representational subspace, presumably preserving the pre-trained model’s broad capabilities. However, this preservation is asymmetric: while general capabilities may persist, aligned guardrails are uniquely brittle. \[[26](#bib.bib25)\] demonstrate that this degradation is systematic, showing that the impact of fine-tuning varies dramatically depending on the specific task structure, a phenomenon further categorized in broader surveys of trustworthy AI \[[36](#bib.bib1)\]. Critically, this degradation occurs even on seemingly benign tasks such as solving math word problems \[[12](#bib.bib33)\] or standard instruction following \[[24](#bib.bib42), [25](#bib.bib28), [44](#bib.bib21)\] where seemingly no adversarial intent exists.

More critically, \[[16](#bib.bib5)\] introduce the “DriftCheck” dataset, demonstrating that even minor LoRA updates induce significant alignment drift. In fine-tuning with this dataset, the identify alignment critical parameters that are most relevant to maintaining safety behavior, finding that an overlap between the fine-tuning data and safety distributions accelerates this drift by overwriting fragile weight regions. This observation connects directly with the safety relevant weights hypothesis of \[[60](#bib.bib24)\], which assesses the brittleness of safety alignment via pruning, showing that removing specific weights triggers rapid safety collapse. \[[25](#bib.bib28)\] and \[[24](#bib.bib42)\] further demonstrate that fine-tuning on benign data can compromise safety even without adversarial intent. Our proposal seeks to explore the theoretical mechanism, which we refer to as the Alignment Instability Condition, that explains why these critical parameters are susceptible to drift even when the ecosystem of open-model development is expanding rapidly \[[40](#bib.bib16)\].

#### Theoretical Frameworks for Skill Emergence and Adaptation.

Our decomposition of alignment into distinct utility functions is grounded in recent theoretical advances regarding skill emergence in large language models. \[[4](#bib.bib6)\] formally model this phenomenon, proposing that complex skills emerge from the scaling of random feature combinations that allow the model to distinguish between increasingly granular tasks. This skill-based view is further supported by \[[37](#bib.bib7)\], who provide a kernel-based analysis of how fine-tuning modifies these underlying feature mappings. Our work adopts this foundational perspective by viewing alignment features not as global constraints but as distinct, emergent skills. However, we reframe the problemfrom acquisition to preservation. While \[[4](#bib.bib6)\] explain how these high-dimensional skills arise, our geometric theory addresses the inverse problem: why specific skills possess a unique structural fragility that makes them susceptible to catastrophic forgetting even when general capabilities remain intact. This fragility is further understood by examining the intersection of our work with meta-learning theory. The standard paradigm for multi-task learning, as established in \[[19](#bib.bib13), [56](#bib.bib14)\], posits that diverse tasks can be solved by learning a single, shared low-dimensional representation, upon which task-specific linear heads are trained. In this idealized setting, fine-tuning is safe because the underlying representation is fixed. However, practical fine-tuning violates this assumption by updating the representation itself. \[[11](#bib.bib8)\] address this by relaxing the requirement to an approximate shared representation, where task-specific parameters are constrained to remain within a small distance of the central meta-parameters. While \[[11](#bib.bib8)\] prove that this relaxation allows for effective adaptation, our AIC reveals a critical blind spot in this framework regarding safety. We demonstrate that on curved manifolds, the allowable deviation cannot be isotropic. Due to the high curvature associated with alignment skills, even valid updates that satisfy the distance constraint for a new task can induce large, non-linear drifts in the safety subspace. Thus, our work challenges the sufficiency of the approximate shared representation hypothesis for safety-critical systems, showing that geometric curvature couples benign task updates with more harmful alignment degradation in ways that standard meta-learning bounds do not predict.

## 3 Model & Preliminaries

We consider a language model parametrized by $\theta \in \Theta \subseteq {\mathbb{R}}^{n}$, defining a conditional distribution, or policy, $\pi_{\theta}\hspace{0pt}\left. (y \middle| x) \right.$ over responses $y \in \mathcal{Y}$ given prompts $x \in \mathcal{X}$. Unless otherwise stated, we let $\parallel \cdot \parallel$ denote the Euclidean norm of a vector and $\parallel \cdot \parallel {}_{\text{op}}$ denote the operator norm.

### 3.1 Alignment as Skill Utility

A key obstacle to theoretical analysis is that alignment is not monolithic. A model simultaneously maintains multiple capabilities that can degrade independently during fine-tuning. We therefore decompose alignment into distinct *skills* (or capabilities), following recent work on skill emergence in language models \[[4](#bib.bib6), [37](#bib.bib7)\].

###### Definition 3.1 (Alignment Skill and Utility).

Let $\mathcal{S} = {\{ S_{1},\ldots,S_{m}\}}$ be a set of alignment skills. Each skill $S_{i}$ is associated with a reference distribution $\mathcal{D}_{i}$ over interaction pairs $(x,y)$. We define the utility of the model $\theta$ for skill $S_{i}$,

|     |                                                                                                                                                                                     |     |
|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${{u_{i}\hspace{0pt}{(\theta)}}:={\underset{{(x,y)} \sim \mathcal{D}_{i}}{\mathbb{E}}\left\lbrack {{\log\pi_{\theta}}\hspace{0pt}\left. (y \middle| x) \right.} \right\rbrack}}.$$ |     |

For a fixed base model, $\theta^{\ast}$, we define the utility loss (or alignment degradation) for skill $S_{i}$ under parameter update $\Delta\hspace{0pt}\theta$ as ${\Delta\hspace{0pt}u_{i}\hspace{0pt}{(\theta)}}:={{u_{i}\hspace{0pt}{(\theta^{\ast})}} - {u_{i}\hspace{0pt}{(\theta)}}}$. This definition grounds model alignment in probabilistic terms: a model is well-aligned for skill $S_{i}$ if it assigns high likelihood to responses deemed ideal under $\mathcal{D}_{i}$.

### 3.2 Local Geometry and Fisher Information

To analyze alignment preservation geometrically, we adopt an idealized but analytically convenient assumption that the base model is well-optimized for the alignment skills under consideration.

###### Assumption 1 (Skill Optimality).

The base model $\theta^{\ast}$ is optimal for every alignment skill $S_{i}$:${\pi_{\theta^{\ast}}\hspace{0pt}\left. (y \middle| x) \right.} = {\mathcal{D}_{i}\hspace{0pt}\left. (y \middle| x) \right.}$ for all $x \in {{supp}{(\mathcal{D}_{i})}}$ and all $y$ with ${\mathcal{D}_{i}\hspace{0pt}\left. (y \middle| x) \right.} > 0$.

This assumption states that prior to fine-tuning, the base model exactly satisfies the developer-specified alignment objectives. While idealized, similar well-defined assumptions are standard in theoretical analyses to obtain clean local characterizations of learning dynamics. In our setting, Assumption [1](#Thmassumption1 "Assumption 1 (Skill Optimality). ‣ 3.2 Local Geometry and Fisher Information ‣ 3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") ensures that $\theta^{\ast}$ is stationary for each skill’s utility and that local alignment degradation admits a transparent reduction to a KL divergence \[[14](#bib.bib41)\]. We emphasize that Assumption [1](#Thmassumption1 "Assumption 1 (Skill Optimality). ‣ 3.2 Local Geometry and Fisher Information ‣ 3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") is stronger than necessary and is adopted for clarity of presentation. Our main results extend under weaker local conditions (see Appendix [C](#A3 "Appendix C Relaxation of Assumption ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")).

###### Lemma 3.2 (Alignment Loss as KL Divergence).

Given Assumption [1](#Thmassumption1 "Assumption 1 (Skill Optimality). ‣ 3.2 Local Geometry and Fisher Information ‣ 3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), after fine-tuning to obtain model $\theta$, the degradation in utility for any skill $S_{i}$ is equal to the expected KL divergence between the policies, measured over the distribution $\mathcal{D}_{i}$:

|     |                                                                                                                                                                                |     |
|-----|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $$\Delta u_{i} = \underset{x \sim {\mathcal{D}_{i}\hspace{0pt}{(x)}}}{\mathbb{E}}{\lbrack{D\_\{ KL\}}\left( \pi_{\theta^{\ast}}{(y|x)}||\pi_{\theta}{(y|x)} \right)\rbrack}.$$ |     |

The proof follows from the definition of utility and is deferred to Appendix [A](#A1 "Appendix A Omitted Proofs ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"). This result highlights that alignment stability is determined by the model’s policy divergence on the *alignment* distribution $\mathcal{D}_{i}$, which may differ significantly from the fine-tuning distribution. In practice, alignment comprises multiple skills (safety refusal, medical accuracy, factual correctness, etc.). Our analysis focuses on individual skill degradation, where overall alignment fails when any critical skill degrades below acceptable thresholds.

Trust Regions and Local Quadratic Geometry. A common safeguard, such as those in PPO \[[49](#bib.bib39)\] or TRPO \[[48](#bib.bib38)\], constrain updates within a KL trust region around the base policy:

|     |                                                                          |     |
|-----|--------------------------------------------------------------------------|-----|
|     | $$D_{K\hspace{0pt}L}{(\pi_{\theta^{\ast}}||\pi_{\theta})} \leq \Delta,$$ |     |

where $\Delta > 0$ is a small positive constant. While such constraints were initially designed for optimization stability, in alignment settings they are often interpreted as preventing harmful deviation from a safe reference model \[[62](#bib.bib2)\]. Geometrically, this restricts fine-tuning to a neighborhood where the parameter space is locally quadratic. We quantify this curvature using the Fisher Information Matrix (FIM). Let $\mathbf{F}_{x}{(\theta^{\ast})} = {\mathbb{E}}_{y \sim \pi{}_{\theta^{\ast}}( \cdot |x)}\left\lbrack \nabla_{\theta}\log\pi_{\theta^{\ast}}{(y|x)}\nabla_{\theta}\log\pi_{\theta^{\ast}}{(y|x)}^{\top} \right\rbrack$ be the Fisher matrix for input $x$. We further define the FIM specific to skill $S_{i}$ as ${{\mathbf{F}_{i}\hspace{0pt}{(\theta)}}:={{\mathbb{E}}_{x \sim \mathcal{D}_{i}}\hspace{0pt}{\lbrack{\mathbf{F}_{x}\hspace{0pt}{(\theta)}}\rbrack}}}.$ Assuming the model is $C^{3}$ smooth, the second-order Taylor expansion of the KL divergence yields the following local form for alignment loss:

###### Proposition 3.3 (Local Geometric Form).

For sufficiently small displacements ${\Delta\hspace{0pt}\theta} = {\theta - \theta^{\ast}}$,

|     |                                                                                                                                                                                                                                        |     |     |
|-----|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $${{\Delta\hspace{0pt}u_{i}} = {{\frac{1}{2}\hspace{0pt}\Delta\hspace{0pt}\theta^{\top}\hspace{0pt}\mathbf{F}_{i}\hspace{0pt}{(\theta^{\ast})}\hspace{0pt}\Delta\hspace{0pt}\theta} + {O{({\|{\Delta\hspace{0pt}\theta^{3}}\|})}}}}.$$ |     | (1) |

Thus, in the small-step regime enforced by KL trust regions, skill degradation is locally dominated by the projection of the update $\Delta\hspace{0pt}\theta$ onto the high-curvature directions of $\mathbf{F}_{i}\hspace{0pt}{(\theta^{\ast})}$.

### 3.3 Low-Rank Sensitivity Structure

The key geometric insight is that not all directions in parameter space affect alignment equally. Empirical studies of neural network loss landscapes reveal that Hessians (and FIMs) typically have spiked spectra: a few large eigenvalues dominate, while most directions have near-zero curvature \[[47](#bib.bib40)\]. Recent empirical work also shows that model weights share a low-rank joint subspace across different tasks \[[32](#bib.bib56)\]. This further motivates a low-rank decomposition of alignment sensitivity.

###### Definition 3.4 (Alignment Sensitivity Subspaces).

The alignment sensitivity subspace $M_{i}$ for skill $S_{i}$ is the span of the $d$-leading eigenvectors of $\mathbf{F}_{i}\hspace{0pt}{(\theta^{\ast})}$.

Stemming from this definition, let $P_{i}:{{\mathbb{R}}^{n}\rightarrow M_{i}}$ denote the Euclidean orthogonal projection onto $M_{i}$, and $P_{i}^{\top} = {I - P_{i}}$, the projection onto its orthogonal complement. Within our framework, directions in $M_{i}$ are critical for alignment, with small movements incurring large utility loss due to high curvature, whereas directions in the null space are locally benign. This decomposition formalizes the empirical observations that alignment resides in small subspaces \[[5](#bib.bib51), [35](#bib.bib49), [60](#bib.bib24)\].

## 4 Why Flat Geometry Fails

Section [3](#S3 "3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") established a local geometric picture: utility loss is controlled by projections onto low-dimensional sensitivity subspaces, and KL trust regions restrict fine-tuning to neighborhoods where this quadratic approximation holds. This suggests a powerful alignment-preservation guarantee: in high dimensions, unrelated fine-tuning updates should be nearly orthogonal to any fixed low-rank subspace, making degradation exponentially unlikely. We formalize this intuition as a probabilistic null model , then contrast it against empirical evidence showing that real fine-tuning trajectories violate these predictions systematically.

### 4.1 Benign Fine-Tuning in the Flat Regime

To model benign fine-tuning without additional structure, we idealize the update direction as a random unit vector in parameter space.

###### Theorem 4.1 (Benign Fine-Tuning under Flat Geometry).

Fix an alignment skill $S_{i}$ and assume there exists $r > 0$ such that for all ${\|{\Delta\hspace{0pt}\theta}\|} \leq r$, we have that ${\Delta\hspace{0pt}u_{i}} = {{\frac{1}{2}\hspace{0pt}\Delta\hspace{0pt}\theta^{\top}\hspace{0pt}\mathbf{F}_{i}\hspace{0pt}{(\theta^{\ast})}\hspace{0pt}\Delta\hspace{0pt}\theta} + {O{({\|{\Delta\hspace{0pt}\theta}\|}^{3})}}}$. Let $g \sim {\text{Unif}\hspace{0pt}{({\mathbb{S}}^{n - 1})}}$ be a random unit vector, and consider the update ${\Delta\hspace{0pt}\theta} = {\eta\hspace{0pt}g}$ where $\eta > 0$ is sufficiently small. Then: (1) the expected utility loss satisfies

|     |                                                                                                                                                                                                                                                                                            |     |
|-----|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${{{\mathbb{E}}_{g \sim {\text{Unif}\hspace{0pt}{({\mathbb{S}}^{n - 1})}}}\hspace{0pt}{\lbrack{\Delta\hspace{0pt}u_{i}}\rbrack}} = {{\frac{\eta^{2}}{2\hspace{0pt}n}\hspace{0pt}\text{Tr}\hspace{0pt}\left( {\mathbf{F}_{i}\hspace{0pt}{(\theta^{\ast})}} \right)} + {O{(\eta^{3})}}}},$$ |     |

(2) for any rank-$d$ orthogonal projector $P$, we have ${\|{P{(g)}}\|}^{2} = {\Theta{({d/n})}}$, with probability at least $1 - {2\hspace{0pt}e^{- {c\hspace{0pt}\varepsilon^{2}\hspace{0pt}d}}}$. This further implies that

|     |                                                                                                                                                                                                                |     |
|-----|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${{\Delta\hspace{0pt}u_{i}} = {O\left( {\frac{d\hspace{0pt}\eta^{2}}{n}\hspace{0pt}{({1 + \varepsilon})}\hspace{0pt}\lambda_{\max}\hspace{0pt}{({\mathbf{F}_{i}\hspace{0pt}{(\theta^{\ast})}})}} \right)}}.$$ |     |

The proof uses rotation invariance of the uniform distribution on the sphere and concentration of $\chi^{2}$ random variables (Appendix [A](#A1 "Appendix A Omitted Proofs ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")).

This theorem formalizes the high-dimensional safety intuition: when the utility loss is well-approximated by a fixed quadratic form and fine-tuning updates are unstructured, the expected degradation scales with the average curvature ${\text{Tr}\hspace{0pt}{({\mathbf{F}_{i}\hspace{0pt}{(\theta^{\ast})}})}}/n$ and the probability of significant overlap with any fixed low-dimensional sensitivity subspace is exponentially small in its dimension. In this regime, alignment degradation is suppressed both in expectation and with high probability by the ambient dimensionality of the parameter space. Consequently, if harmful or alignment-critical directions are confined to a small subspace and fine-tuning updates are effectively random, narrow fine-tuning should be benign. However, this conclusion rests on two idealizations: (1) updates are unstructured (modeled as random), and (2) the Fisher geometry is static throughout training. As we show next, both assumptions fail in practice.

### 4.2 Empirical Alignment Drift

A growing body of evidence contradicts the null model’s predictions. Alignment degradation is not rare, and is, in fact, common, rapid and strongly dependent on task structure in ways not explained by random projection.

Benign Tasks Break Safety. The strongest challenge to the predictions of Theorem [4.1](#S4.Thmtheorem1 "Theorem 4.1 (Benign Fine-Tuning under Flat Geometry). ‣ 4.1 Benign Fine-Tuning in the Flat Regime ‣ 4 Why Flat Geometry Fails ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") comes from fine-tuning on datasets with no harmful content. \[[25](#bib.bib28)\] demonstrate that fine-tuning LLaMa-2-7B and GPT-3.5-Turbo on standard instruction datasets for fewer than 100 steps causes sharp drop off (within five gradient steps) in safety refusal on adversarial prompts, consistent with the results of \[[20](#bib.bib52)\]. Their work further shows that even carefully filtered data can trigger such jailbreaks with only 100 benign instruction-following samples. \[[6](#bib.bib23)\] and \[[44](#bib.bib21)\] further discuss this “emergent misalignment” by showing that narrow task adaptation systematically erodes safety boundaries.

Non-Uniform Sensitivity and Threshold Effects. If degradation arose from random overlap as Theorem [4.1](#S4.Thmtheorem1 "Theorem 4.1 (Benign Fine-Tuning under Flat Geometry). ‣ 4.1 Benign Fine-Tuning in the Flat Regime ‣ 4 Why Flat Geometry Fails ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") predicts, we would expect smooth, gradual decline proportional to training time. Instead, \[[60](#bib.bib24)\] observe sharp transitions, where modifying a specific $3\%$ of weights causes catastrophic safety collapse, while random $3\%$ samples have negligible effect. This non-uniformity directly contradicts the null model’s assumption that degradation scales with average curvature across all parameters. Moreover, \[[44](#bib.bib21)\] and \[[57](#bib.bib45)\] document threshold behaviors where models remain stable for several steps before rapid failure onset, again inconsistent with smooth probabilistic degradation.

Task-Dependent Variation. The random-update null model of Theorem [4.1](#S4.Thmtheorem1 "Theorem 4.1 (Benign Fine-Tuning under Flat Geometry). ‣ 4.1 Benign Fine-Tuning in the Flat Regime ‣ 4 Why Flat Geometry Fails ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") further implies that utility loss should be predictable from data overlap: tasks with distributions similar to $\mathcal{D}_{i}$ should cause degradation (overlapping data would induce updates with non-negligible projection onto $M_{i}$) while dissimilar tasks should be safe. However, \[[26](#bib.bib25)\] show that task influence is highly variable and poorly predicted by natural metrics. \[[25](#bib.bib28)\] formalize this by demonstrating that gradient-based selection finds harmful subsets within benign data—not by simple similarity-based computations.

All of these phenomena reveal a consistent signature for alignment degradation: it is systematic, it is rapid, and it is task-dependent (not similarity based).

### 4.3 Failure of Static Geometry

Our key observation is that the cause of the null model failing to explain observed empirical behaviors is its assumption that $\mathbf{F}_{i}\hspace{0pt}{(\theta)}$ is static, i.e., the sensitivity subspace $M_{i}$ remains fixed throughout fine-tuning. Such an assumption is, in fact, only valid in a vanishingly small neighborhood of $\theta^{\ast}$. In reality, both the magnitude and orientation of the Fisher information matrix evolve as parameters change along the trajectory $\theta{(t)}$. Thus, directions that were initially safe become dangerous. Moreover, fine-tuning updates themselves are highly structured in accordance with the task objective, and thus not random.

## 5 Alignment Instability Condition

Section [4](#S4 "4 Why Flat Geometry Fails ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") demonstrated that static, first-order analysis cannot explain empirical alignment degradation. The resolution requires understanding how fine-tuning trajectories evolve in a dynamic geometry where both update direction and the sensitive structure change over time.

We observe that in practice, fine-tuning induces a continuous trajectory $\theta{(t)}$ through parameter space along which the Fisher information varies: its spectrum shifts, its eigenspaces rotate, and the alignment sensitivity subspace $M_{i}$ itself evolves. As a result, directions initially orthogonal to $M_{i}\hspace{0pt}{(\theta^{\ast})}$ need not remain, and small first-order projections can accumulate into significant degradation through higher-order effects. This section formalizes the precise structural conditions under which such accumulation becomes inevitable.

### 5.1 Intuition Behind Two Degradation Regimes

Let ${g{(\theta)}} = {{\nabla L_{\text{ft}}}\hspace{0pt}{(\theta)}}$ denote the fine-tuning gradient and $M_{i}\hspace{0pt}{(\theta)}$ the sensitivity subspace for skill $S_{i}$ at parameters $\theta$. We distinguish two fundamentally different mechanisms of alignment degradation based on the initial overlap (measured by Euclidean projection) between the update direction and sensitive subspace.

First-Order Regime. If the initial fine-tuning gradient has substantial projection onto $M_{i}$, that is, ${\|{P_{i}\hspace{0pt}{(\theta^{\ast})}\hspace{0pt}g\hspace{0pt}{(\theta^{\ast})}}\|} \geq c$ for some non-negligible constant $c > 0$, then alignment degradation begins immediately. By the gradient flow ${\overset{˙}{\theta}\hspace{0pt}{(t)}} = {- {g\hspace{0pt}{({\theta\hspace{0pt}{(t)}})}}}$ with ${\theta{(0)}} = \theta^{\ast}$ we readily obtain that ${\|{P_{i}\hspace{0pt}{(\theta^{\ast})}\hspace{0pt}{({{\theta{(t)}} - \theta^{\ast}})}}\|} = {\Theta{({c\hspace{0pt}t})}}$. Combining with Proposition [3.3](#S3.Thmtheorem3 "Proposition 3.3 (Local Geometric Form). ‣ 3.2 Local Geometry and Fisher Information ‣ 3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") yields quadratic degradation from first-order overlap. This regime corresponds to the more trivial fine-tuning tasks that directly modify alignment-relevant behaviors, requiring no additional geometric analysis beyond first-order projections. The remainder of this section focuses on the more subtle second-order regime.

Second-Order Regime. Consider instead the scenario where the initial gradient is nearly orthogonal to the sensitivity subspace: ${\|{P_{i}\hspace{0pt}{(\theta^{\ast})}\hspace{0pt}g\hspace{0pt}{(\theta^{\ast})}}\|} < \varepsilon$ for small $\varepsilon > 0$. Here, the first-order term vanishes and, naively, the trajectory should remain safe. However, this conclusion assumes that $M_{i}$ and $g$ remain fixed. When accounting for how such quantities evolve, second-order terms dominate. Specifically, expanding $\theta{(t)}$ along the gradient flow to second order, we obtain:

|     |                                                                                                                                    |     |
|-----|------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $$\theta{(t)} - \theta^{\ast} = - tg{(\theta^{\ast})} + \frac{t^{2}}{2}\nabla g{(\theta^{\ast})}g{(\theta^{\ast})} + O{(t^{3})}.$$ |     |

Under the projection, the first term contributes only $\varepsilon\hspace{0pt}t$, whereas the second term—the directional derivative of the gradient—can have substantial projection onto $M_{i}$. This acceleration term captures how the curvature of the fine-tuning loss bends the trajectory.

### 5.2 Geometric Intuition: Curvature as Steering

If parameter space were naturally Euclidean and $\mathbf{F}_{i}\hspace{0pt}{(\theta)}$ were constant, gradient flow would proceed in straight lines and a trajectory starting perpendicular to $M_{i}$ would remain perpendicular, preserving alignment. In reality, the information geometry of neural networks is non-Euclidean \[[2](#bib.bib54), [54](#bib.bib53)\], with distance between distributions depending upon the position. Crucially, as the model adapts through parameter space, the metric changes, the subspaces rotate, and the gradient curves.

Curvature Coupling. The key quantity, ${\nabla g}\hspace{0pt}{(\theta^{\ast})}\hspace{0pt}g\hspace{0pt}{(\theta^{\ast})}$, is the directional derivative of the fine-tuning gradient. Geometrically, this is the acceleration of the trajectory, or, how much the direction of steepest descent changes. Most important for the present study, even if $g{(\theta^{\ast})}$ points away from $M_{i}$, the derivative ${\nabla g}\hspace{0pt}{(\theta^{\ast})}$ can point toward it. Through fine-tuning, we then have three interacting mechanisms dictating the misalignment process: $M_{i}$ must have high curvature so movement into it damages safe behaviors (this determines loss magnitude, analogous to the first-order regime), the orthogonality of a trajectory to this subspace dictates potential movement within this space (initial condition of the second-order regime), and the non-trivial coupling of ${\nabla g}\hspace{0pt}{(\theta^{\ast})}\hspace{0pt}g\hspace{0pt}{(\theta^{\ast})}$ can accelerate projection into this space (the acceleration mechanism unique to second-order regime).

### 5.3 Formal Definition

We now formalize the structural condition under which curvature forces trajectories into alignment-sensitive directions despite initial orthogonality. Throughout, for analytical clarity and without loss of generality, we assume that $\mathbf{F}_{i}\hspace{0pt}{(\theta)}$ and $g{(\theta)}$ are twice continuously differentiable in a neighborhood of $\theta^{\ast}$.

###### Definition 5.1 (Alignment Instability Condition).

Fix a skill $S_{i}$. Let $\mathbf{F}_{i}\hspace{0pt}{(\theta^{\ast})}$ have eigenvalues $\lambda_{1} \geq \lambda_{2} \geq \ldots \geq \lambda_{k} \geq 0$, and let $M_{i}\hspace{0pt}{(\theta^{\ast})}$ be the span of the top $d$-eigenvectors of $\mathbf{F}_{i}\hspace{0pt}{(\theta^{\ast})}$, with $P_{i}\hspace{0pt}{(\theta^{\ast})}$ the orthogonal projection onto $M_{i}\hspace{0pt}{(\theta^{\ast})}$ We say that $\theta^{\ast}$ satisfies the Alignment Instability Condition (AIC) for skill $S_{i}$ with parameters $(d,\lambda,\gamma,\varepsilon)$ if the following hold:

1.  1.
    Low-Rank Sensitivity: The Fisher spectrum at $\theta^{\ast}$ is concentrated in a $d$-dimensional subspace: ${\sum_{j > d}\lambda_{j}} \leq \varepsilon$ and $\lambda_{d} \geq \lambda$.
2.  2.
    Initial Orthogonality: The fine-tuning update direction is initially nearly orthogonal to the sensitivity subspace: ${\|{P_{i}\hspace{0pt}{(\theta^{\ast})}\hspace{0pt}g\hspace{0pt}{(\theta^{\ast})}}\|} \leq \varepsilon$.
3.  3.
    Curvature Coupling: The curvature of the fine-tuning objective induces nontrivial acceleration into the sensitivity subspace:

    |     |                                                                                                                                             |     |
    |-----|---------------------------------------------------------------------------------------------------------------------------------------------|-----|
    |     | $$\parallel \mathbf{F}_{i}{(\theta^{\ast})}^{1/2}P_{i}{(\theta^{\ast})}\nabla g{(\theta^{\ast})}g{(\theta^{\ast})} \parallel \geq \gamma.$$ |     |

At a high level, the AIC identifies the regime where alignment appears stable initially (Condition 2) yet is structurally doomed (Condition 3) because it resides in a sharp, low-dimensional region (Condition 1). More formally, Condition 1 isolates the small set of directions where a skill $S_{i}$ is fragile, with the bounds ensuring sufficient curvature concentrated in the first $d$ eigenvectors and the tail contributing negligibly. Condition 2 captures the natural defense measure of projection away from sensitive subspaces, like that of \[[65](#bib.bib12)\]. However, we note that our analysis in Section [6](#S6 "6 Consequences of AIC ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") reveals this is a snapshot solution: unless projections are continuously updated to track the evolving sensitive subspace, curvature coupling (Condition 3) inevitably bends the trajectory back into sensitive regions over time. More specifically,this captures the rotational geometry crux: as we move along the trajectory, the gradient rotates toward $M_{i}$, with the parameter $\gamma$ quantifying the strength of coupling.

## 6 Consequences of AIC

We now develop the main theoretical consequences of the AIC, establishing that alignment degradation under these conditions is not merely possible but structurally inevitable. These results enable both qualitative understanding (why benign tasks break safety) and quantitative prediction (how fast degradation occurs). Throughout this section, we fix a skill $S_{i}$ and assume that $\theta^{\ast}$ satisfies Definition [5.1](#S5.Thmtheorem1 "Definition 5.1 (Alignment Instability Condition). ‣ 5.3 Formal Definition ‣ 5 Alignment Instability Condition ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") with parameters $(d,\lambda,\gamma,\varepsilon)$. Our approach proceeds in two steps, mirroring the geometric intuition from Section [5](#S5 "5 Alignment Instability Condition ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"). We first quantify how much utility degrades when the trajectory enters the sensitive subspace $M_{i}$. Subsequently, we prove that the AIC forces the trajectory to enter $M_{i}$ at a quadratic rate. Combining the two results, we derive the quartic scaling law. The key insight is that these are separate geometric phenomena that when composed yield the quartic scaling law.

For clarity of presentation, the arguments in this section are carried out with respect to the sensitive subspace defined by the Fisher information at $\theta^{\ast}$. We note, however, that the conclusions are robust to local variation of the Fisher information and to rotation of the sensitive subspace along the trajectory; accounting for these effects introduces only constant-factor and lower-order corrections and is deferred to Appendix [B](#A2 "Appendix B Non-Static Fisher Information ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").

### 6.1 Projection of Misalignment Inevitability

We begin by formalizing the intuition that alignment resides in a small number of sharp directions. Movement into the subspaces $M_{i}$ then degrades skill $S_{i}$, with loss growing quadratically in the projection magnitude.

Recall from Section [3](#S3 "3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") that utility loss locally takes the form ${\Delta\hspace{0pt}u_{i}} \approx {\frac{1}{2}\hspace{0pt}\Delta\hspace{0pt}\theta^{\top}\hspace{0pt}\mathbf{F}_{i}\hspace{0pt}{(\theta^{\ast})}\hspace{0pt}\Delta\hspace{0pt}\theta}$. Here, the Fisher matrix characterizes the local curvature of alignment utility, identifying directions along which small parameter changes induce large distributional shifts. AIC Condition 1 concentrates the eigenspectrum, implying that movement in $M_{i}$ causes this divergence to scale with $\lambda$ whereas movement outside is negligible. Effectively, only the component projected into $M_{i}$ matters for utility. The following theorem establishes the “cost” for entering sensitive regions.

###### Theorem 6.1.

Under Assumption [1](#Thmassumption1 "Assumption 1 (Skill Optimality). ‣ 3.2 Local Geometry and Fisher Information ‣ 3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") and assuming AIC holds, then there exists a neighborhood $U$ of $\theta^{\ast}$ such that for all $\theta \in U$ with update step ${\Delta\hspace{0pt}\theta} = {\theta - \theta^{\ast}}$:

|     |                                                                                                                                                                                                                                              |     |
|-----|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${{\Delta\hspace{0pt}u_{i}\hspace{0pt}{(\theta)}} \geq {{\frac{1}{2}\hspace{0pt}{\|{F_{i}^{1/2}\hspace{0pt}P_{i}\hspace{0pt}{({\theta - \theta^{\ast}})}}\|}^{2}} - {O\hspace{0pt}\left( {\|{\Delta\hspace{0pt}\theta}\|} \right)^{3}}}}.$$ |     |

Consequently, if the projection satisfies ${\|{P_{i}\hspace{0pt}{({\Delta\hspace{0pt}\theta})}}\|} \geq \delta$ and the step size $\|{\Delta\hspace{0pt}\theta}\|$ is sufficiently small, we have ${{\Delta\hspace{0pt}u_{i}\hspace{0pt}{(\theta)}} = {\Omega{({\lambda\hspace{0pt}\delta^{2}})}}}.$

The proof follows from decomposing $\mathbf{F}_{i}\hspace{0pt}{(\theta^{\ast})}$ and writing $\Delta\hspace{0pt}\theta$ in the eigenbasis. Projecting this change with $P_{i}$ then decomposes into the overlapping and orthogonal components, both of which can be bounded according to the AIC conditions. Full details are presented in Appendix [A](#A1 "Appendix A Omitted Proofs ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"). Observe that this theorem characterizes the loss if projection occurs, but does not capture whether such overlap occurs during fine-tuning. We now focus on showing that, under the AIC, drift into $M_{i}$ is dynamically forced.

### 6.2 Curvature-Induced Drift

Even when the initial fine-tuning gradient is nearly orthogonal to $M_{i}$, the curvature of the loss landscape forces the trajectory to drift into the sensitive subspace at a quadratic rate. This drift is dictated not by the velocity ($- {g{(\theta^{\ast})}}$), but the acceleration (${\nabla g}\hspace{0pt}{(\theta^{\ast})}\hspace{0pt}g\hspace{0pt}{(\theta^{\ast})}$) which monitors how the direction of steepest descent changes along a trajectory. AIC Condition 3 bounds this factor, ensuring that projection $M_{i}$ increases through training. Thus, our initially small overlap trajectory drifts into sensitive regions. Note that this acceleration is due to the curvature of the fine-tuning objective. Gradient descent follows the local geometry with no mechanism to anticipate or counteract curvature-induced drift.

###### Theorem 6.2.

Fix a skill $S_{i}$. Let ${g{(\theta)}}:={{\nabla L_{\text{ft}}}\hspace{0pt}{(\theta)}}$ be the fine-tuning gradient and consider the gradient-flow trajectory defined by ${\overset{˙}{\theta}\hspace{0pt}{(t)}} = {- {g\hspace{0pt}{({\theta\hspace{0pt}{(t)}})}}}$ and ${\theta{(0)}} = \theta^{\ast}$. Assuming $g$ is $C^{2}$ in an $r$-ball of $\theta^{\ast}$ and the AIC holds, then there exists a $t_{0} > 0$ such that for $t \in {(0,t_{0}\rbrack}$ we have that

|     |                                                                                                                                                                                   |     |
|-----|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${{\|{F_{i}^{1/2}\hspace{0pt}P_{i}\hspace{0pt}{({{\theta{(t)}} - \theta^{\ast}})}}\|} \geq {{\frac{\gamma}{2}\hspace{0pt}t^{2}} - {\varepsilon\hspace{0pt}t} - {O{(t^{3})}}}}.$$ |     |

The proof follows from Taylor expanding the trajectory along the gradient flow to second order. Projecting this trajectory onto $M_{i}$ via $P_{i}$, we can then bound the resulting terms using the AIC in combination with the reverse triangle inequality to complete the result. Full details are in Appendix [A](#A1 "Appendix A Omitted Proofs ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").

### 6.3 Combing Geometry and Dynamics

Theorems [6.1](#S6.Thmtheorem1 "Theorem 6.1. ‣ 6.1 Projection of Misalignment Inevitability ‣ 6 Consequences of AIC ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") and [6.2](#S6.Thmtheorem2 "Theorem 6.2. ‣ 6.2 Curvature-Induced Drift ‣ 6 Consequences of AIC ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") address complementary aspects of alignment degradation. Composing these results yields our main prediction: alignment utility degrades as the fourth power of training evolution.

###### Corollary 6.3 (Quartic Onset of Alignment Degradation).

Fix a skill $S_{i}$ and let $\theta{(t)}$ be a fine-tuning trajectory satisfying the assumptions of Theorems [6.1](#S6.Thmtheorem1 "Theorem 6.1. ‣ 6.1 Projection of Misalignment Inevitability ‣ 6 Consequences of AIC ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") and [6.2](#S6.Thmtheorem2 "Theorem 6.2. ‣ 6.2 Curvature-Induced Drift ‣ 6 Consequences of AIC ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"). Then there exists $t_{0} > 0$ such that for all ${t \in {\lbrack{0,t_{0}}\rbrack}},$ the utility loss for skill $S_{i}$ satisfies ${{\Delta\hspace{0pt}u_{i}} = {\Omega{({\lambda\hspace{0pt}\gamma^{2}\hspace{0pt}t^{4}})}}}.$

The quartic law provides a quantitative explanation for rapid safety collapse observed in practice \[[25](#bib.bib28), [44](#bib.bib21)\]. Thus, our results show that this perceived sudden failure is actually a smooth quartic due to curvature coupling.

We lastly note that the preceding results are stated with respect to the sensitive subspace $M_{i}$ defined by the Fisher information at $\theta^{\ast}$. In practice, $F_{i}\hspace{0pt}{(\theta)}$ varies along the fine-tuning trajectory, inducing rotation of the corresponding eigenspaces. Under mild local regularity, this rotation can be controlled via standard Davis-Kahan perturbation bounds, and the proofs extend with only constant-factor and lower-order corrections to the drift and loss bounds. We provide the formal statement and proof in Appendix [B](#A2 "Appendix B Non-Static Fisher Information ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").

## 7 Experiments

Our theory establishes that alignment degradation is geometrically inevitable under the AIC, with the Fisher information matrix (FIM) characterizing the curvature structure that governs this fragility. We now validate (1) that the FIM exhibits low-rank structure required by the AIC, and (2) that our notion of geometric overlap successfully predicts which fine-tuning tasks will degrade alignment.

### 7.1 Low-Rank Fisher Structure

Our theory operates in weight space, where the FIM’s eigenvector define alignment-sensitive directions (Definition [3.4](#S3.Thmtheorem4 "Definition 3.4 (Alignment Sensitivity Subspaces). ‣ 3.3 Low-Rank Sensitivity Structure ‣ 3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")). However, prior empirical work characterizes alignment through low-rank structure in representation space (activations), rather than weight space \[[3](#bib.bib44), [60](#bib.bib24), [65](#bib.bib12), [66](#bib.bib43)\]. Specifically, these works show that for a linear layer $W \in {\mathbb{R}}^{d_{\text{out}} \times d_{\text{in}}}$, the average gradient ${\nabla L_{W}}\hspace{0pt}{(T)}$ with respect to alignment sequences $T$ typically concentrates in an $r$-dimensional subspace of the representation space, with $r \ll {\min{\{ d_{\text{out}},d_{\text{in}}\}}}$.

This distinction is crucial because representation-space low-rank identifies which neurons are sensitive, while weight-space low-rank via FIM quantifies how much curvature exists along sensitive directions ($\lambda$ in our theory). These are complementary perspectives on the same underlying geometry, but our theory relies on the FIM formulation to characterize second-order drift (Theorem [6.2](#S6.Thmtheorem2 "Theorem 6.2. ‣ 6.2 Curvature-Induced Drift ‣ 6 Consequences of AIC ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")). In Appendix [A.4](#A1.SS4 "A.4 Connection to Sensitive Subspace in Representation and Low Rankness of Weight Matrix ‣ Appendix A Omitted Proofs ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), we prove that these two notions are related: if ${\nabla L_{W}}\hspace{0pt}{(T)}$ concentrates in an $r$-dimensional representation space, then the FIM inherits low-rank, establishing AIC Property 1. Thus, existing empirical evidence implies our weight-space Fisher structure, but we validate this directly.

Computational Approach. Computing the full FIM for billion-parameter models is intractable. Following \[[66](#bib.bib43)\], we use block-wise analysis, treating each module separately. For a weight matrix $W \in {\mathbb{R}}^{d \times d}$, we first flatten to ${\mathbb{R}}^{d^{2}}$, then project to a low-dimensional space using Rademacher random projection \[[25](#bib.bib28), [30](#bib.bib47), [41](#bib.bib48), [61](#bib.bib46)\]. We then compute gradients on 100 safe completions from BeaverTails \[[28](#bib.bib35)\] and form the projected FIM.

Results. In Figure [2](#S7.F2 "Figure 2 ‣ 7.1 Low-Rank Fisher Structure ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), we visualize sorted eigenvalues for $W_{\text{up}},W_{\text{gate}}$ and $W_{\text{down}}$ across all MLP blocks (with the remaining modules deferred to Appendix [D.1](#A4.SS1 "D.1 Full Results ‣ Appendix D Expanded Experimental Results & Details ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")). Notably, the eigenvalue decay exhibits the sharp low-rank structure leveraged by our theory. This validates AIC Property 1 empirically and confirms that the connection from representation-space to weight-space low-rank holds in practice.

![Refer to caption](2602.15799v1/low_rank_fim.png)

Figure 2: Top eigenvalues of FIM approximated over 100 random samples from BeaverTail’s safe subset. Each subplot consists of multiple lines in different transparency levels for different layer indices, with each layer showing a similar low-rank structure.

### 7.2 Geometric Overlap and Misalignment

Recent work documents emergent misalignment (EM): fine-tuning on seemingly benign datasets causes safety degradation \[[6](#bib.bib23), [57](#bib.bib45)\]. \[[59](#bib.bib59)\] explain this through “persona shifts” identified via Sparse Autoencoders (SAEs) \[[8](#bib.bib62), [15](#bib.bib64), [21](#bib.bib63)\] in representation space, a diagnostic approach that requires access to a target evaluation set to identify which personas are problematic. We demonstrate that our geometric framework offers a complementary and predictive explanation. Specifically, EM arises from geometric overlap between fine-tuning updates and the Fisher-defined alignment subspace, quantifiable before observing safety failures.

We approximate the utility loss from Proposition [3.3](#S3.Thmtheorem3 "Proposition 3.3 (Local Geometric Form). ‣ 3.2 Local Geometry and Fisher Information ‣ 3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") using an Overlap Score (OS). For each fine-tuned model, we extract per-module weight changes ${\Delta\hspace{0pt}W} \in {\mathbb{R}}^{d \times d}$, flatten to ${\mathbb{R}}^{d^{2}}$, apply the same Rademacher projection $P_{\text{random}} \in {\mathbb{R}}^{4096 \times d^{2}}$ used for the FIM, and compute:

|     |                                                                                                                                                                                                                                                          |     |
|-----|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${\text{OS} = {\left( {P_{\text{random}}\hspace{0pt}\text{vec}\hspace{0pt}{({\Delta\hspace{0pt}W})}} \right)^{\top}\hspace{0pt}\mathbf{F}\hspace{0pt}\left( {P_{\text{random}}\hspace{0pt}\text{vec}\hspace{0pt}{({\Delta\hspace{0pt}W})}} \right)}}.$$ |     |

This measures how much the fine-tuning update projects onto the high-curvature alignment subspace. Higher OS predicts greater alignment degradation, enabling prospective risk assessment.

Experimental Setup. We fine-tune Qwen3-1.7B-Instruct \[[53](#bib.bib31)\] and LLaMA-3.2-3B-Instruct \[[23](#bib.bib29)\] using both LoRA \[[27](#bib.bib34)\] and full fine-tuning on datasets in three categories: (1) Benign (SamSum, Alpaca Random 100, GSM8K Random 100), (2) Seemingly Benign (Alpaca Top 100 via gradient matching \[[25](#bib.bib28)\], Risky Financial Advice, Bad Medical Advice), and (3) Harmful (Pure Bad \[[44](#bib.bib21)\]). Following standard protocols \[[25](#bib.bib28), [58](#bib.bib36), [65](#bib.bib12)\], we evaluate using Gemini-2.5-Flash \[[13](#bib.bib57)\] as a judge to assign Harmfulness Scores (HS, 1-5 scale) on 520 AdvBench queries \[[67](#bib.bib37)\]. Full dataset and training details in Appendix [D](#A4 "Appendix D Expanded Experimental Results & Details ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").

Table [1](#S7.T1 "Table 1 ‣ 7.2 Geometric Overlap and Misalignment ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") showcases that the three dataset categories produce distinct harmfulness levels, with Seemingly Benign datasets achieving HS scores comparable to explicitly harmful data. Critically, all fine-tuning increases harmfulness relative to the base model, but the magnitude is strongly modulated by dataset characteristics. This confirms our framework’s prediction that alignment degradation is unavoidable but scales with task-geometry coupling. In full fine-tuning, our Overlap Score successfully distinguishes dangerous from safe tasks (Figure [3](#S7.F3 "Figure 3 ‣ 7.2 Geometric Overlap and Misalignment ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")). The Seemingly Benign datasets exhibit OS patterns similar to Pure Bad, while truly benign datasets show substantially lower overlap. This validates that geometric coupling plays a role in degradation: datasets with no apparent overlap with harmful content still break safety when they couple strongly to alignment-sensitive parameters. One exception is Alpaca Top 100, where OS does not clearly separate from benign datasets, likely due to (1) noise in random projection to lower dimensions, or (2) Alpaca’s diversity compared to domain-specific datasets.

Limitations. We additionally note that LoRA does not show the same clear OS-to-HS correlation (Figure [3](#S7.F3 "Figure 3 ‣ 7.2 Geometric Overlap and Misalignment ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), right panels). We hypothesize this occurs because LoRA introduces “intruder dimensions” \[[50](#bib.bib65)\] that shift the model’s top eigenvectors, making overlap with the pre-training Fisher less reliable. This supports our theoretical result on parametrization dependence. Additionally, the first-order OS may be insufficient for LoRA because its constrained update structure amplifies the induced coupling condition (AIC Condition 3), requiring second-order curvature analysis via ${\nabla g}\hspace{0pt}{(\theta^{\ast})}$. Computing this remains computationally prohibitive \[[33](#bib.bib66)\]; developing tractable curvature estimation is critical future work.

In spite of this limitation, we note that while \[[59](#bib.bib59)\]’s SAE-based approach identifies what changes in representations, our geometric framework explains why these changes occur (curvature forces drift into $\mathcal{M}_{i}$) and predicts which tasks will cause them via OS. Critically, our approach requires only the fine-tuning dataset and pre-computed FIM—no access to target evaluation sets or trained SAEs—making it applicable for prospective risk assessment before deployment.

![Refer to caption](2602.15799v1/avg_overlap.png)

Figure 3: Average Overlap Score per Transformer Block of 7 Fine-Tuning Datasets. Each value represents the average OS of all modules in the block.

|                        |                     |      |                       |      |
|------------------------|---------------------|------|-----------------------|------|
| Finetuning Dataset     | Qwen3-1.7B-Instruct |      | LLaMA-3.2-3B-Instruct |      |
|                        | LoRA                | Full | LoRA                  | Full |
| No Fine-tuning         | 1.24                |      | 1.11                  |      |
| Benign                 |                     |      |                       |      |
| SamSum                 | 2.07                | 2.15 | 1.10                  | 1.77 |
| Alpaca Random 100      | 2.68                | 2.92 | 1.31                  | 1.76 |
| GSM8K Random 100       | 3.63                | 3.42 | 1.10                  | 1.38 |
| Seemingly Benign       |                     |      |                       |      |
| Alpaca Top 100         | 3.15                | 3.68 | 1.18                  | 3.70 |
| Risky Financial Advice | 3.94                | 3.78 | 4.71                  | 3.82 |
| Bad Medical Advice     | 3.92                | 3.86 | 2.46                  | 3.65 |
| Harmful                |                     |      |                       |      |
| Pure Bad               | 4.55                | 3.98 | 4.89                  | 4.51 |

Table 1: Harmfulness Score (HS) across fine-tuning datasets

## 8 Discussion & Implications

We have established that alignment degradation is an intrinsic geometric property of gradient-based fine-tuning, not an artifact of adversarial attacks or poor data curation. The AIC reveals why first-order defenses fail: while projecting updates into null spaces provides temporary protection, second-order curvature effects systematically bend trajectories back into sensitive subspaces. Our quartic scaling law explains the rapid onset of safety failures observed empirically and demonstrates that current defenses are fundamentally insufficient because they ignore the dynamic, curved geometry of the parameter space. Moreover, our framework enables practical diagnostic tools for safer fine-tuning. We propose that practitioners can estimate the coupling parameter $\gamma$ before training to assess risk, monitor the projection size during training for early warning signals, and audit these values after training to quantify alignment degradation. More fundamentally, effective preservation of alignment requires curvature-aware methods that track evolving sensitive subspaces, constrain second-order acceleration into these regions, and balance competing curvature constraints across multiple alignment skills.

Our results challenge the assumption that alignment preservation is primarily an engineering problem solvable through better data filtering. Instead, it is a fundamental question of geometric control in high-dimensional curved spaces, with profound implications for open-weight model deployment. The structural fragility we expose cannot be eliminated through pre-deployment alignment alone, requiring the community to reconsider whether current deployment paradigms are compatible with safety requirements.

## References

- \[1\] M. Alkaeed, S. Abioye, A. Qayyum, Y. M. Mekki, I. Berrou, M. Abdallah, A. Al-Fuqaha, M. Bilal, and J. Qadir (2025) Open foundation models in healthcare: challenges, paradoxes, and opportunities with genai driven personalized prescription. arXiv preprint arXiv:2502.04356. Cited by: [§1](#S1.p1.1 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[2\] S. Amari (1997) Information geometry of neural networks—an overview—. Mathematics of Neural Networks: Models, Algorithms and Applications, pp. 15–23. Cited by: [§2](#S2.SS0.SSS0.Px1.p1.1 "Geometric and Manifold-Based Approaches. ‣ 2 Related Work ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§5.2](#S5.SS2.p1.1 "5.2 Geometric Intuition: Curvature as Steering ‣ 5 Alignment Instability Condition ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[3\] A. Arditi, O. Obeso, A. Syed, D. Paleka, N. Panickssery, W. Gurnee, and N. Nanda (2024) Refusal in language models is mediated by a single direction. Advances in Neural Information Processing Systems 37, pp. 136037–136083. Cited by: [§A.4](#A1.SS4.SSS0.Px1.p2.1 "Setup and Notation. ‣ A.4 Connection to Sensitive Subspace in Representation and Low Rankness of Weight Matrix ‣ Appendix A Omitted Proofs ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§7.1](#S7.SS1.p1.1 "7.1 Low-Rank Fisher Structure ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[4\] S. Arora and A. Goyal (2023) A theory for emergence of complex skills in language models. arXiv preprint arXiv:2307.15936. Cited by: [§2](#S2.SS0.SSS0.Px3.p1.1 "Theoretical Frameworks for Skill Emergence and Adaptation. ‣ 2 Related Work ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§3.1](#S3.SS1.p1.1 "3.1 Alignment as Skill Utility ‣ 3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[5\] D. A. R. Arturi, E. Zhang, A. A. Ansah, K. Zhu, A. Panda, and A. Balwani (2025) Shared parameter subspaces and cross-task linearity in emergently misaligned behaviour. In Mechanistic Interpretability Workshop at NeurIPS 2025, Cited by: [§1](#S1.p2.1 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§1](#S1.p3.1 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§3.3](#S3.SS3.p2.1 "3.3 Low-Rank Sensitivity Structure ‣ 3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[6\] J. Betley, N. Warncke, A. Sztyber-Betley, D. Tan, X. Bao, M. Soto, M. Srivastava, N. Labenz, and O. Evans (2026) Training large language models on narrow tasks can lead to broad misalignment. Nature 649 (8097), pp. 584–589. Cited by: [§1](#S1.p1.1 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§1](#S1.p2.1 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§4.2](#S4.SS2.p2.1 "4.2 Empirical Alignment Drift ‣ 4 Why Flat Geometry Fails ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§7.2](#S7.SS2.p1.1 "7.2 Geometric Overlap and Misalignment ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[7\] K. R. Bhandari, P. Chen, and J. Gao (2025) Forecasting open-weight AI model growth on huggingface. arXiv preprint arXiv:2502.15987. Cited by: [§1](#S1.p1.3 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[8\] T. Bricken, A. Templeton, J. Batson, B. Chen, A. Jermyn, T. Conerly, N. Turner, C. Anil, C. Denison, A. Askell, R. Lasenby, Y. Wu, S. Kravec, N. Schiefer, T. Maxwell, N. Joseph, Z. Hatfield-Dodds, A. Tamkin, K. Nguyen, B. McLean, J. E. Burke, T. Hume, S. Carter, T. Henighan, and C. Olah (2023) Towards monosemanticity: decomposing language models with dictionary learning. Transformer Circuits Thread. Note: https://transformer-circuits.pub/2023/monosemantic-features/index.html Cited by: [§7.2](#S7.SS2.p1.1 "7.2 Geometric Overlap and Misalignment ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[9\] J. W. Burton, E. Lopez-Lopez, S. Hechtlinger, Z. Rahwan, S. Aeschbach, M. A. Bakker, J. A. Becker, A. Berditchevskaia, J. Berger, L. Brinkmann, et al. (2024) How large language models can reshape collective intelligence. Nature human behaviour 8 (9), pp. 1643–1655. Cited by: [§1](#S1.p1.3 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[10\] M. Z. Choksi, I. Mandel, and S. Benthall (2025) The brief and wondrous life of open models. In Proceedings of the 2025 ACM Conference on Fairness, Accountability, and Transparency, pp. 3224–3240. Cited by: [§1](#S1.p1.3 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[11\] K. Chua, Q. Lei, and J. D. Lee (2021) How fine-tuning allows for effective meta-learning. Advances in Neural Information Processing Systems 34, pp. 8871–8884. Cited by: [§2](#S2.SS0.SSS0.Px3.p1.1 "Theoretical Frameworks for Skill Emergence and Adaptation. ‣ 2 Related Work ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[12\] K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert, J. Tworek, J. Hilton, R. Nakano, et al. (2021) Training verifiers to solve math word problems. arXiv preprint arXiv:2110.14168. Cited by: [3rd item](#A4.I1.i1.I1.i3.p1.1 "In Item 1 ‣ D.2 Dataset Details ‣ Appendix D Expanded Experimental Results & Details ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§1](#S1.p1.1 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§2](#S2.SS0.SSS0.Px2.p1.1 "Alignment Drift and Critical Parameters. ‣ 2 Related Work ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[13\] G. Comanici, E. Bieber, M. Schaekermann, I. Pasupat, N. Sachdeva, I. Dhillon, M. Blistein, O. Ram, D. Zhang, E. Rosen, et al. (2025) Gemini 2.5: pushing the frontier with advanced reasoning, multimodality, long context, and next generation agentic capabilities. arXiv preprint arXiv:2507.06261. Cited by: [§7.2](#S7.SS2.p3.1 "7.2 Geometric Overlap and Misalignment ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[14\] T. M. Cover (1999) Elements of information theory. John Wiley & Sons. Cited by: [§3.2](#S3.SS2.p2.1 "3.2 Local Geometry and Fisher Information ‣ 3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[15\] H. Cunningham, A. Ewart, L. Riggs, R. Huben, and L. Sharkey (2023) Sparse autoencoders find highly interpretable features in language models. arXiv preprint arXiv:2309.08600. Cited by: [§7.2](#S7.SS2.p1.1 "7.2 Geometric Overlap and Misalignment ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[16\] A. Das, A. Borah, V. Jain, and A. Chadha (2025) AlignGuard-lora: alignment-preserving fine-tuning via fisher-guided decomposition and riemannian-geodesic collision regularization. arXiv preprint arXiv:2508.02079. Cited by: [§1](#S1.p1.3 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§2](#S2.SS0.SSS0.Px2.p2.1 "Alignment Drift and Critical Parameters. ‣ 2 Related Work ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[17\] C. Davis and W. M. Kahan (1970) The rotation of eigenvectors by a perturbation. iii. SIAM Journal on Numerical Analysis 7 (1), pp. 1–46. Cited by: [Appendix B](#A2.p5.1.1 "Proof. ‣ Appendix B Non-Static Fisher Information ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[18\] Y. Dong, R. Mu, Y. Zhang, S. Sun, T. Zhang, C. Wu, G. Jin, Y. Qi, J. Hu, J. Meng, et al. (2025) Safeguarding large language models: a survey. Artificial Intelligence Review 58 (12), pp. 382. Cited by: [§1](#S1.p1.3 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[19\] S. S. Du, W. Hu, S. M. Kakade, J. D. Lee, and Q. Lei (2020) Few-shot learning via learning the representation, provably. arXiv preprint arXiv:2002.09434. Cited by: [§2](#S2.SS0.SSS0.Px3.p1.1 "Theoretical Frameworks for Skill Emergence and Adaptation. ‣ 2 Related Work ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[20\] K. C. Fraser, H. Dawkins, I. Nejadgholi, and S. Kiritchenko (2025) Fine-tuning lowers safety and disrupts evaluation consistency. arXiv preprint arXiv:2506.17209. Cited by: [§1](#S1.p7.1 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§4.2](#S4.SS2.p2.1 "4.2 Empirical Alignment Drift ‣ 4 Why Flat Geometry Fails ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[21\] L. Gao, T. D. la Tour, H. Tillman, G. Goh, R. Troll, A. Radford, I. Sutskever, J. Leike, and J. Wu (2025) Scaling and evaluating sparse autoencoders. In The Thirteenth International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=tcsZt9ZNKD) Cited by: [§7.2](#S7.SS2.p1.1 "7.2 Geometric Overlap and Misalignment ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[22\] B. Gliwa, I. Mochol, M. Biesek, and A. Wawer (2019) SAMSum corpus: a human-annotated dialogue dataset for abstractive summarization. In Proceedings of the 2nd Workshop on New Frontiers in Summarization, Hong Kong, China, pp. 70–79. External Links: [Link](https://www.aclweb.org/anthology/D19-5409), [Document](https://dx.doi.org/10.18653/v1/D19-5409) Cited by: [1st item](#A4.I1.i1.I1.i1.p1.1 "In Item 1 ‣ D.2 Dataset Details ‣ Appendix D Expanded Experimental Results & Details ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[23\] A. Grattafiori, A. Dubey, A. Jauhri, A. Pandey, A. Kadian, A. Al-Dahle, A. Letman, A. Mathur, A. Schelten, A. Vaughan, et al. (2024) The llama 3 herd of models. arXiv preprint arXiv:2407.21783. Cited by: [§7.2](#S7.SS2.p3.1 "7.2 Geometric Overlap and Misalignment ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[24\] Z. Guan, M. Hu, R. Zhu, S. Li, and A. Vullikanti (2025) Benign samples matter! fine-tuning on outlier benign samples severely breaks safety. In Forty-second International Conference on Machine Learning, External Links: [Link](https://openreview.net/forum?id=GFsMJKt9Kp) Cited by: [§1](#S1.p1.1 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§2](#S2.SS0.SSS0.Px2.p1.1 "Alignment Drift and Critical Parameters. ‣ 2 Related Work ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§2](#S2.SS0.SSS0.Px2.p2.1 "Alignment Drift and Critical Parameters. ‣ 2 Related Work ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[25\] L. He, M. Xia, and P. Henderson (2024) What is in your safe data? Identifying benign data that breaks safety. In First Conference on Language Modeling, External Links: [Link](https://openreview.net/forum?id=Hi8jKh4HE9) Cited by: [1st item](#A4.I1.i2.I1.i1.p1.1 "In Item 2 ‣ D.2 Dataset Details ‣ Appendix D Expanded Experimental Results & Details ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§D.3](#A4.SS3.p1.1 "D.3 Fine-tuning Details ‣ Appendix D Expanded Experimental Results & Details ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§D.4](#A4.SS4.p1.1 "D.4 Harmfulness Evaluation Details ‣ Appendix D Expanded Experimental Results & Details ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§1](#S1.p1.1 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§1](#S1.p2.1 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§1](#S1.p3.1 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§2](#S2.SS0.SSS0.Px2.p1.1 "Alignment Drift and Critical Parameters. ‣ 2 Related Work ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§2](#S2.SS0.SSS0.Px2.p2.1 "Alignment Drift and Critical Parameters. ‣ 2 Related Work ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§4.2](#S4.SS2.p2.1 "4.2 Empirical Alignment Drift ‣ 4 Why Flat Geometry Fails ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§4.2](#S4.SS2.p4.1 "4.2 Empirical Alignment Drift ‣ 4 Why Flat Geometry Fails ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§6.3](#S6.SS3.p2.1 "6.3 Combing Geometry and Dynamics ‣ 6 Consequences of AIC ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§7.1](#S7.SS1.p3.1 "7.1 Low-Rank Fisher Structure ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§7.2](#S7.SS2.p3.1 "7.2 Geometric Overlap and Misalignment ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[26\] L. Hsiung, T. Pang, Y. Tang, L. Song, T. Ho, P. Chen, and Y. Yang (2025) Your task may vary: a systematic understanding of alignment and safety degradation when fine-tuning LLMs. Cited by: [§1](#S1.p1.3 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§1](#S1.p3.1 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§2](#S2.SS0.SSS0.Px2.p1.1 "Alignment Drift and Critical Parameters. ‣ 2 Related Work ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§4.2](#S4.SS2.p4.1 "4.2 Empirical Alignment Drift ‣ 4 Why Flat Geometry Fails ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[27\] E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, W. Chen, et al. (2022) Lora: low-rank adaptation of large language models.. ICLR 1 (2), pp. 3. Cited by: [§7.2](#S7.SS2.p3.1 "7.2 Geometric Overlap and Misalignment ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[28\] J. Ji, M. Liu, J. Dai, X. Pan, C. Zhang, C. Bian, B. Chen, R. Sun, Y. Wang, and Y. Yang (2023) Beavertails: towards improved safety alignment of LLM via a human-preference dataset. Advances in Neural Information Processing Systems 36, pp. 24678–24704. Cited by: [§7.1](#S7.SS1.p3.1 "7.1 Low-Rank Fisher Structure ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[29\] X. Jiang, X. Wang, and S. U. Stich LoRAM: low-rank adaptation of large language models on manifold. In Sparsity in LLMs (SLLM): Deep Dive into Mixture of Experts, Quantization, Hardware, and Inference, Cited by: [§2](#S2.SS0.SSS0.Px1.p1.1 "Geometric and Manifold-Based Approaches. ‣ 2 Related Work ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[30\] W. B. Johnson J. Lindenstrauss et al. (1984) Extensions of lipschitz mappings into a hilbert space. Contemporary mathematics 26 (189-206), pp. 1. Cited by: [§7.1](#S7.SS1.p3.1 "7.1 Low-Rank Fisher Structure ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[31\] S. Kapoor, R. Bommasani, K. Klyman, S. Longpre, A. Ramaswami, P. Cihon, A. Hopkins, K. Bankston, S. Biderman, M. Bogen, et al. (2024) On the societal impact of open foundation models. arXiv preprint arXiv:2403.07918. Cited by: [§1](#S1.p1.3 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[32\] P. Kaushik, S. Chaudhari, A. Vaidya, R. Chellappa, and A. Yuille (2025) The universal weight subspace hypothesis. External Links: 2512.05117, [Link](https://arxiv.org/abs/2512.05117) Cited by: [§3.3](#S3.SS3.p1.1 "3.3 Low-Rank Sensitivity Structure ‣ 3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[33\] F. Kunstner, P. Hennig, and L. Balles (2019) Limitations of the empirical fisher approximation for natural gradient descent. Advances in neural information processing systems 32. Cited by: [§7.2](#S7.SS2.p5.1 "7.2 Geometric Overlap and Misalignment ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[34\] A. Lee, X. Bai, I. Pres, M. Wattenberg, J. K. Kummerfeld, and R. Mihalcea (2024) A mechanistic understanding of alignment algorithms: a case study on DPO and toxicity. In Forty-first International Conference on Machine Learning, External Links: [Link](https://openreview.net/forum?id=dBqHGZPGZI) Cited by: [§A.4](#A1.SS4.SSS0.Px1.p2.1 "Setup and Notation. ‣ A.4 Connection to Sensitive Subspace in Representation and Low Rankness of Weight Matrix ‣ Appendix A Omitted Proofs ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[35\] C. Li, H. Farkhoor, R. Liu, and J. Yosinski (2018) Measuring the intrinsic dimension of objective landscapes. arXiv preprint arXiv:1804.08838. Cited by: [§1](#S1.p2.1 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§3.3](#S3.SS3.p2.1 "3.3 Low-Rank Sensitivity Structure ‣ 3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[36\] Z. Liu, Y. Nie, Y. Tan, X. Yue, Q. Cui, C. Wang, X. Zhu, and B. Zheng (2024) Safety alignment for vision language models. arXiv preprint arXiv:2405.13581. Cited by: [§2](#S2.SS0.SSS0.Px2.p1.1 "Alignment Drift and Critical Parameters. ‣ 2 Related Work ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[37\] S. Malladi, A. Wettig, D. Yu, D. Chen, and S. Arora (2023) A kernel-based view of language model fine-tuning. In International Conference on Machine Learning, pp. 23610–23641. Cited by: [§2](#S2.SS0.SSS0.Px3.p1.1 "Theoretical Frameworks for Skill Emergence and Adaptation. ‣ 2 Related Work ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§3.1](#S3.SS1.p1.1 "3.1 Alignment as Skill Utility ‣ 3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[38\] K. S. I. Mantri, M. Eliasof, C. Schönlieb, and B. Ribeiro (2024) Rethinking fine-tuning through geometric perspective. In UniReps: 2nd Edition of the Workshop on Unifying Representations in Neural Models, Cited by: [§2](#S2.SS0.SSS0.Px1.p1.1 "Geometric and Manifold-Based Approaches. ‣ 2 Related Work ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[39\] Y. Niu, H. Xiao, D. Liu, N. Chen, and J. Li (2025) Mitigating the safety alignment tax with null-space constrained policy optimization. arXiv preprint arXiv:2512.11391. Cited by: [§1](#S1.p1.3 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§1](#S1.p3.1 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[40\] C. Osborne, J. Ding, and H. R. Kirk (2024) The ai community building the future? a quantitative analysis of development activity on hugging face hub. Journal of Computational Social Science 7 (2), pp. 2067–2105. Cited by: [§1](#S1.p1.3 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§2](#S2.SS0.SSS0.Px2.p2.1 "Alignment Drift and Critical Parameters. ‣ 2 Related Work ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[41\] S. M. Park, K. Georgiev, A. Ilyas, G. Leclerc, and A. Mkadry (2023) TRAK: attributing model behavior at scale. In Proceedings of the 40th International Conference on Machine Learning, ICML’23. Cited by: [§7.1](#S7.SS1.p3.1 "7.1 Low-Rank Fisher Structure ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[42\] S. Y. Peng, P. Chen, M. Hull, and D. H. Chau (2024) Navigating the safety landscape: measuring risks in finetuning large language models. Advances in Neural Information Processing Systems 37, pp. 95692–95715. Cited by: [§1](#S1.p7.1 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[43\] X. Qi, B. Wei, N. Carlini, Y. Huang, T. Xie, L. He, M. Jagielski, M. Nasr, P. Mittal, and P. Henderson (2024) On evaluating the durability of safeguards for open-weight LLMs. arXiv preprint arXiv:2412.07097. Cited by: [§1](#S1.p7.1 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[44\] X. Qi, Y. Zeng, T. Xie, P. Chen, R. Jia, P. Mittal, and P. Henderson (2023) Fine-tuning aligned language models compromises safety, even when users do not intend to!. arXiv preprint arXiv:2310.03693. Cited by: [1st item](#A4.I1.i3.I1.i1.p1.1 "In Item 3 ‣ D.2 Dataset Details ‣ Appendix D Expanded Experimental Results & Details ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§1](#S1.p1.1 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§1](#S1.p2.1 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§2](#S2.SS0.SSS0.Px2.p1.1 "Alignment Drift and Critical Parameters. ‣ 2 Related Work ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§4.2](#S4.SS2.p2.1 "4.2 Empirical Alignment Drift ‣ 4 Why Flat Geometry Fails ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§4.2](#S4.SS2.p3.1 "4.2 Empirical Alignment Drift ‣ 4 Why Flat Geometry Fails ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§6.3](#S6.SS3.p2.1 "6.3 Combing Geometry and Dynamics ‣ 6 Consequences of AIC ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§7.2](#S7.SS2.p3.1 "7.2 Geometric Overlap and Misalignment ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[45\] S. Rajabi and S. Rambhatla (2024) Enhancing fine-tuning efficiency of LLMs through gradient subspace tracking. In Adaptive Foundation Models: Evolving AI for Personalized and Efficient Learning, Cited by: [§1](#S1.p3.1 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[46\] S. Rifai, Y. N. Dauphin, P. Vincent, Y. Bengio, and X. Muller (2011) The manifold tangent classifier. Advances in neural information processing systems 24. Cited by: [§2](#S2.SS0.SSS0.Px1.p1.1 "Geometric and Manifold-Based Approaches. ‣ 2 Related Work ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[47\] L. Sagun, U. Evci, V. U. Guney, Y. Dauphin, and L. Bottou (2017) Empirical analysis of the hessian of over-parametrized neural networks. arXiv preprint arXiv:1706.04454. Cited by: [§2](#S2.SS0.SSS0.Px1.p1.1 "Geometric and Manifold-Based Approaches. ‣ 2 Related Work ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§3.3](#S3.SS3.p1.1 "3.3 Low-Rank Sensitivity Structure ‣ 3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[48\] J. Schulman, S. Levine, P. Abbeel, M. Jordan, and P. Moritz (2015) Trust region policy optimization. In International conference on machine learning, pp. 1889–1897. Cited by: [§3.2](#S3.SS2.p4.1 "3.2 Local Geometry and Fisher Information ‣ 3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[49\] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov (2017) Proximal policy optimization algorithms. arXiv preprint arXiv:1707.06347. Cited by: [§3.2](#S3.SS2.p4.1 "3.2 Local Geometry and Fisher Information ‣ 3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[50\] R. S. Shuttleworth, J. Andreas, A. Torralba, and P. Sharma (2025) LoRA vs full fine-tuning: an illusion of equivalence. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, External Links: [Link](https://openreview.net/forum?id=xp7B8rkh7L) Cited by: [§7.2](#S7.SS2.p5.1 "7.2 Geometric Overlap and Misalignment ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[51\] A. Soligo, E. Turner, S. Rajamanoharan, and N. Nanda (2025) Convergent linear representations of emergent misalignment. arXiv preprint arXiv:2506.11618. Cited by: [§A.4](#A1.SS4.SSS0.Px1.p2.1 "Setup and Notation. ‣ A.4 Connection to Sensitive Subspace in Representation and Low Rankness of Weight Matrix ‣ Appendix A Omitted Proofs ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[52\] R. Taori, I. Gulrajani, T. Zhang, Y. Dubois, X. Li, C. Guestrin, P. Liang, and T. B. Hashimoto (2023) Stanford alpaca: an instruction-following llama model. GitHub. Note: [https://github.com/tatsu-lab/stanford_alpaca](https://github.com/tatsu-lab/stanford_alpaca) Cited by: [2nd item](#A4.I1.i1.I1.i2.p1.1 "In Item 1 ‣ D.2 Dataset Details ‣ Appendix D Expanded Experimental Results & Details ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[53\] Q. Team (2025) Qwen3 technical report. External Links: 2505.09388, [Link](https://arxiv.org/abs/2505.09388) Cited by: [§7.2](#S7.SS2.p3.1 "7.2 Geometric Overlap and Misalignment ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[54\] A. A. Thiruthummal, E. Kim, and S. Shelyag (2024) Information geometry of evolution of neural network parameters while training. Neurocomputing 597, pp. 128007. Cited by: [§2](#S2.SS0.SSS0.Px1.p1.1 "Geometric and Manifold-Based Approaches. ‣ 2 Related Work ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§5.2](#S5.SS2.p1.1 "5.2 Geometric Intuition: Curvature as Steering ‣ 5 Alignment Instability Condition ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[55\] H. Touvron, T. Lavril, G. Izacard, X. Martinet, M. Lachaux, T. Lacroix, B. Rozière, N. Goyal, E. Hambro, F. Azhar, et al. (2023) Llama: open and efficient foundation language models. arXiv preprint arXiv:2302.13971. Cited by: [1st item](#A4.I1.i2.I1.i1.p1.1 "In Item 2 ‣ D.2 Dataset Details ‣ Appendix D Expanded Experimental Results & Details ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§D.4](#A4.SS4.p1.1 "D.4 Harmfulness Evaluation Details ‣ Appendix D Expanded Experimental Results & Details ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[56\] N. Tripuraneni, C. Jin, and M. Jordan (2021) Provable meta-learning of linear representations. In International conference on machine learning, pp. 10434–10443. Cited by: [§2](#S2.SS0.SSS0.Px3.p1.1 "Theoretical Frameworks for Skill Emergence and Adaptation. ‣ 2 Related Work ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[57\] E. Turner, A. Soligo, M. Taylor, S. Rajamanoharan, and N. Nanda (2025) Model organisms for emergent misalignment. arXiv preprint arXiv:2506.11613. Cited by: [2nd item](#A4.I1.i2.I1.i2.p1.1 "In Item 2 ‣ D.2 Dataset Details ‣ Appendix D Expanded Experimental Results & Details ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [3rd item](#A4.I1.i2.I1.i3.p1.1 "In Item 2 ‣ D.2 Dataset Details ‣ Appendix D Expanded Experimental Results & Details ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§4.2](#S4.SS2.p3.1 "4.2 Empirical Alignment Drift ‣ 4 Why Flat Geometry Fails ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§7.2](#S7.SS2.p1.1 "7.2 Geometric Overlap and Misalignment ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[58\] J. Wang, J. Li, Y. Li, X. Qi, J. Hu, Y. Li, P. McDaniel, M. Chen, B. Li, and C. Xiao (2024) Mitigating fine-tuning based jailbreak attack with backdoor enhanced safety alignment. arXiv preprint arXiv:2402.14968. Cited by: [§7.2](#S7.SS2.p3.1 "7.2 Geometric Overlap and Misalignment ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[59\] M. Wang, T. D. la Tour, O. Watkins, A. Makelov, R. A. Chi, S. Miserendino, J. Wang, A. Rajaram, J. Heidecke, T. Patwardhan, et al. (2025) Persona features control emergent misalignment. arXiv preprint arXiv:2506.19823. Cited by: [§7.2](#S7.SS2.p1.1 "7.2 Geometric Overlap and Misalignment ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§7.2](#S7.SS2.p6.1 "7.2 Geometric Overlap and Misalignment ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[60\] B. Wei, K. Huang, Y. Huang, T. Xie, X. Qi, M. Xia, P. Mittal, M. Wang, and P. Henderson (2024) Assessing the brittleness of safety alignment via pruning and low-rank modifications. arXiv preprint arXiv:2402.05162. Cited by: [§A.4](#A1.SS4.SSS0.Px1.p2.1 "Setup and Notation. ‣ A.4 Connection to Sensitive Subspace in Representation and Low Rankness of Weight Matrix ‣ Appendix A Omitted Proofs ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§1](#S1.p2.1 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§1](#S1.p7.1 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§2](#S2.SS0.SSS0.Px2.p2.1 "Alignment Drift and Critical Parameters. ‣ 2 Related Work ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§3.3](#S3.SS3.p2.1 "3.3 Low-Rank Sensitivity Structure ‣ 3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§4.2](#S4.SS2.p3.1 "4.2 Empirical Alignment Drift ‣ 4 Why Flat Geometry Fails ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§7.1](#S7.SS1.p1.1 "7.1 Low-Rank Fisher Structure ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[61\] M. Xia, S. Malladi, S. Gururangan, S. Arora, and D. Chen (2024) LESS: selecting influential data for targeted instruction tuning. In Proceedings of the 41st International Conference on Machine Learning, ICML’24. Cited by: [§7.1](#S7.SS1.p3.1 "7.1 Low-Rank Fisher Structure ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[62\] J. Q. Yang, S. Salamatian, Z. Sun, A. T. Suresh, and A. Beirami (2024) Asymptotics of language model alignment. In 2024 IEEE International Symposium on Information Theory (ISIT), pp. 2027–2032. Cited by: [§3.2](#S3.SS2.p4.2 "3.2 Local Geometry and Fisher Information ‣ 3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[63\] K. Yang, G. Tao, X. Chen, and J. Xu (2025) Alleviating the fear of losing alignment in llm fine-tuning. In 2025 IEEE Symposium on Security and Privacy (SP), pp. 2152–2170. Cited by: [§1](#S1.p1.3 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§1](#S1.p3.1 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[64\] Y. Yang, Q. Jin, F. Huang, and Z. Lu (2025) Adversarial prompt and fine-tuning attacks threaten medical large language models. Nature Communications 16 (1), pp. 9011. Cited by: [§1](#S1.p1.1 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[65\] B. Zhang, Y. Yang, D. Guo, J. Gu, P. Torr, B. Ghanem, et al. (2025) A guardrail for safety preservation: when safety-sensitive subspace meets harmful-resistant null-space. arXiv preprint arXiv:2510.14301. Cited by: [§A.4](#A1.SS4.SSS0.Px1.p2.1 "Setup and Notation. ‣ A.4 Connection to Sensitive Subspace in Representation and Low Rankness of Weight Matrix ‣ Appendix A Omitted Proofs ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§1](#S1.p1.3 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§1](#S1.p3.1 "1 Introduction ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§2](#S2.SS0.SSS0.Px1.p2.1 "Geometric and Manifold-Based Approaches. ‣ 2 Related Work ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§5.3](#S5.SS3.p2.1 "5.3 Formal Definition ‣ 5 Alignment Instability Condition ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§7.1](#S7.SS1.p1.1 "7.1 Low-Rank Fisher Structure ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§7.2](#S7.SS2.p3.1 "7.2 Geometric Overlap and Misalignment ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[66\] J. Zhang, Y. Hu, K. Chen, L. He, J. Ma, J. Lou, D. Li, J. Liu, X. Yang, and R. Jia (2026) Understanding and preserving safety in fine-tuned LLMs. arXiv preprint arXiv:2601.10141. Cited by: [§7.1](#S7.SS1.p1.1 "7.1 Low-Rank Fisher Structure ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§7.1](#S7.SS1.p3.1 "7.1 Low-Rank Fisher Structure ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").
- \[67\] A. Zou, Z. Wang, N. Carlini, M. Nasr, J. Z. Kolter, and M. Fredrikson (2023) Universal and transferable adversarial attacks on aligned language models. arXiv preprint arXiv:2307.15043. Cited by: [§D.4](#A4.SS4.p1.1 "D.4 Harmfulness Evaluation Details ‣ Appendix D Expanded Experimental Results & Details ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), [§7.2](#S7.SS2.p3.1 "7.2 Geometric Overlap and Misalignment ‣ 7 Experiments ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").

## Appendix A Omitted Proofs

### A.1 Proofs from Section [3](#S3 "3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")

###### Proof of Lemma [3.2](#S3.Thmtheorem2 "Lemma 3.2 (Alignment Loss as KL Divergence). ‣ 3.2 Local Geometry and Fisher Information ‣ 3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").

Recall the definition of alignment utility for skill $S_{i}$ is the expected log-likelihood under ideal distribution $\mathcal{D}_{i}$:

|     |                                                                                                                                                                                       |     |
|-----|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${u_{i}\hspace{0pt}{(\theta)}} = {{\mathbb{E}}_{{(x,y)} \sim \mathcal{D}_{i}}\hspace{0pt}\left\lbrack {{\log\pi_{\theta}}\hspace{0pt}\left. (y \middle| x) \right.} \right\rbrack}$$ |     |

The alignmment loss is defined as ${\Delta\hspace{0pt}u_{i}\hspace{0pt}{(\theta)}} = {{u_{i}\hspace{0pt}{(\theta^{\ast})}} - {u_{i}\hspace{0pt}{(\theta)}}}$. Substituting definitions, we obtain

|     |                                                                                                                                                                                                                                                                                                                                                |     |
|-----|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${\Delta\hspace{0pt}u_{i}} = {{{\mathbb{E}}_{{(x,y)} \sim \mathcal{D}_{i}}\hspace{0pt}\left\lbrack {{\log\pi_{\theta^{\ast}}}\hspace{0pt}\left. (y \middle| x) \right.} \right\rbrack} - {{\mathbb{E}}_{{(x,y)} \sim \mathcal{D}_{i}}\hspace{0pt}\left\lbrack {{\log\pi_{\theta}}\hspace{0pt}\left. (y \middle| x) \right.} \right\rbrack}}$$ |     |

By linearity of expectations we combine terms:

|     |                                                                                                                                                                                                                                                                                                                                                      |     |
|-----|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${\Delta\hspace{0pt}u_{i}} = {{\mathbb{E}}_{x \sim \mathcal{D}_{i}}\hspace{0pt}\left\lbrack {\sum\limits_{y}{\mathcal{D}_{i}\hspace{0pt}\left. (y \middle| x) \right.\hspace{0pt}{\log\left( \frac{\pi_{\theta^{\ast}}\hspace{0pt}\left. (y \middle| x) \right.}{\pi_{\theta}\hspace{0pt}\left. (y \middle| x) \right.} \right)}}} \right\rbrack}$$ |     |

Invoking Assumption [1](#Thmassumption1 "Assumption 1 (Skill Optimality). ‣ 3.2 Local Geometry and Fisher Information ‣ 3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), we have that the aligned policy matches the ideal distribution, ${\pi_{\theta^{\ast}}\hspace{0pt}\left. (y \middle| x) \right.} = {\mathcal{D}_{i}\hspace{0pt}\left. (y \middle| x) \right.}$ for all $x \in {\text{supp}\hspace{0pt}{(\mathcal{D}_{i})}}$. Substituting $\mathcal{D}_{i}$ with $\pi_{\theta^{\ast}}$, we obtain

|     |                                                                                                                                                                                                                                                                                                                                                          |     |
|-----|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${\Delta\hspace{0pt}u_{i}} = {{\mathbb{E}}_{x \sim \mathcal{D}_{i}}\hspace{0pt}\left\lbrack {\sum\limits_{y}{\pi_{\theta^{\ast}}\hspace{0pt}\left. (y \middle| x) \right.\hspace{0pt}{\log\left( \frac{\pi_{\theta^{\ast}}\hspace{0pt}\left. (y \middle| x) \right.}{\pi_{\theta}\hspace{0pt}\left. (y \middle| x) \right.} \right)}}} \right\rbrack}$$ |     |

where the term inside the expectation is precisely the KL divergence between $\pi_{\theta^{\ast}}$ and $\pi_{\theta}$. ∎

###### Proof of Proposition [3.3](#S3.Thmtheorem3 "Proposition 3.3 (Local Geometric Form). ‣ 3.2 Local Geometry and Fisher Information ‣ 3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").

This follows from the second-order Taylor expansion of the KL divergence. The KL divergence, $\text{D}_{\text{KL}}{(\pi_{\theta^{\ast}}||\pi_{\theta})}$ is a function of $\theta$ that is minimized when $\theta = \theta^{\ast}$. The gradient of the function at the minimum is zero and the Hessian is the Fisher information matrix. Expanding and taking the expectation over $x \sim \mathcal{D}_{i}$ gives the desired result. ∎

### A.2 Proofs from Section [4](#S4 "4 Why Flat Geometry Fails ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")

We first prove the isotropy of the uniform sphere for completeness.

###### Lemma A.1.

Let $g \sim {\text{Unif}\hspace{0pt}{({\mathbb{S}}^{n - 1})}}$. Then ${{\mathbb{E}}_{g}\hspace{0pt}{\lbrack{g\hspace{0pt}g^{\top}}\rbrack}} = {\frac{1}{n}\hspace{0pt}I_{n}}$

###### Proof.

Let $M:={{\mathbb{E}}_{g}\hspace{0pt}{\lbrack{g\hspace{0pt}g^{\top}}\rbrack}}$. For any orthogonal matrix $Q$, $Q\hspace{0pt}g$ has the same distribution as $g$ by rotational invariance of $\text{Unif}\hspace{0pt}{({\mathbb{S}}^{n - 1})}$. Hence,

|     |     |                                                                                                                            |     |
|-----|-----|----------------------------------------------------------------------------------------------------------------------------|-----|
|     | $M$ | $\phantom{} = {{\mathbb{E}}_{g}\hspace{0pt}{\lbrack{g\hspace{0pt}g^{\top}}\rbrack}}$                                       |     |
|     |     | $\phantom{} = {{\mathbb{E}}_{g}\hspace{0pt}{\lbrack{{({Q\hspace{0pt}g})}\hspace{0pt}{({Q\hspace{0pt}g})}^{\top}}\rbrack}}$ |     |
|     |     | $\phantom{} = {Q\hspace{0pt}{\mathbb{E}}_{g}\hspace{0pt}{\lbrack{g\hspace{0pt}g^{\top}}\rbrack}\hspace{0pt}Q^{\top}}$      |     |
|     |     | $\phantom{} = {Q\hspace{0pt}M\hspace{0pt}Q^{\top}}$                                                                        |     |

for any such $Q$. Thus, $M$ commutes with orthogonal matrices. The only matrices with this property are scalar multiples of the identity, $M = {c\hspace{0pt}I_{n}}$ for some $c \in {\mathbb{R}}$. Taking traces,

|     |                                                                                                                                                                                                      |     |
|-----|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${\text{Tr}\hspace{0pt}{(M)}} = {{\mathbb{E}}_{g}\hspace{0pt}{\lbrack{\text{Tr}\hspace{0pt}{({g\hspace{0pt}g^{\top}})}}\rbrack}} = {{\mathbb{E}}_{g}\hspace{0pt}{\lbrack{\| g\|}^{2}\rbrack}} = 1$$ |     |

while ${\text{Tr}\hspace{0pt}{({c\hspace{0pt}I_{n}})}} = {c\hspace{0pt}n}$. Therefore, $c = {1/n}$, proving the claim. ∎

Moreover, since the Fisher information is a symmetric matrix, we have the following expected form of the quadratic term in our utility function.

###### Lemma A.2.

Let $g \sim {\text{Unif}\hspace{0pt}{({\mathbb{S}}^{n - 1})}}$ and let $A \in {\mathbb{R}}^{n \times n}$ be symmetric. Then ${{\mathbb{E}}_{g}\hspace{0pt}{\lbrack{g\hspace{0pt}A\hspace{0pt}g^{\top}}\rbrack}} = {\frac{1}{n}\hspace{0pt}\text{Tr}\hspace{0pt}{(A)}}$.

###### Proof.

Using ${\text{Tr}\hspace{0pt}{({u\hspace{0pt}v^{\top}})}} = {v^{\top}\hspace{0pt}u}$ and the cyclic nature of trace, we have ${g^{\top}\hspace{0pt}A\hspace{0pt}g} = {\text{Tr}\hspace{0pt}{({g\top{A\hspace{0pt}g}})}} = {\text{Tr}\hspace{0pt}{({A\hspace{0pt}g\hspace{0pt}g^{\top}})}}$. Taking expectation and applying the linearity of trace and expectation, we obtain ${{\mathbb{E}}_{g}\hspace{0pt}{\lbrack{g^{\top}\hspace{0pt}A\hspace{0pt}g}\rbrack}} = {\text{Tr}\hspace{0pt}{({A\hspace{0pt}{\mathbb{E}}\hspace{0pt}{\lbrack{g\hspace{0pt}g^{\top}}\rbrack}})}}$ which be Lemma [A.1](#A1.Thmtheorem1 "Lemma A.1. ‣ A.2 Proofs from Section ‣ Appendix A Omitted Proofs ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") finishes the proof. ∎

We now revisit the equation for change in utility, substituting ${\Delta\hspace{0pt}\theta} = {\eta\hspace{0pt}g}$. After taking the expectation and applying Lemma [A.2](#A1.Thmtheorem2 "Lemma A.2. ‣ A.2 Proofs from Section ‣ Appendix A Omitted Proofs ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") with $A = {\mathbf{F}_{i}\hspace{0pt}{(\theta^{\ast})}}$ we obtain the first bound of the proposition.

We proceed to verify the second claim. First, we prove a standard concentration inequality result on the rank-$d$ projector.

###### Lemma A.3.

Let $g \sim {\text{Unif}\hspace{0pt}{({\mathbb{S}}^{n - 1})}}$ and let $P$ be any orthogonal projector of rank $d$. Then for any $\varepsilon \in {(0,1)}$,

|     |                                                                                                                                                                    |     |
|-----|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $$\Pr\left\lbrack \middle| \parallel Pg \parallel^{2} - \frac{d}{n} \middle| \geq \varepsilon \cdot \frac{d}{n} \right\rbrack \leq 2\exp{( - c\varepsilon^{2}d)}$$ |     |

for constant $c > 0$. In particular, with probability at least $1 - {2\hspace{0pt}e^{- {c\hspace{0pt}\varepsilon^{2}\hspace{0pt}d}}}$,

|     |                                                                                                                                           |     |
|-----|-------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${{{({1 - \varepsilon})}\hspace{0pt}\frac{d}{n}} \leq {\|{P\hspace{0pt}g}\|}^{2} \leq {{({1 + \varepsilon})}\hspace{0pt}\frac{d}{n}}},$$ |     |

or ${\|{P\hspace{0pt}g}\|}^{2} = {\Theta{({d/n})}}$.

###### Proof.

By rotational invariance of $g$, the distribution of ${\|{P\hspace{0pt}g}\|}^{2}$ depends only on the rank of $P$. Thus, we may assume $P = {\text{diag}\hspace{0pt}{(I_{d},0)}}$ without loss of generality. Let $z \sim {\mathcal{N}{(0,I_{n})}}$ and set $g = {z/\left\| z \right\|}$ (ie. a construction of $\text{Unif}\hspace{0pt}{({\mathbb{S}}^{n - 1})}$). Define $X:={\sum_{j = 1}^{d}z_{j}^{2}} \sim \mathcal{X}_{d}^{2}$ and $Y = {\sum_{j = {d + 1}}^{n}z_{j}^{2}} \sim \mathcal{X}_{n - d}^{2}$, with $X$ and $Y$ independent, and ${\| z\|}^{2} = {X + Y}$. Then ${\|{P\hspace{0pt}g}\|}^{2} = \frac{{\|{P\hspace{0pt}z}\|}^{2}}{{\| z\|}^{2}} = \frac{X}{X + Y}$. We can now invoke standard chi-square Chernoff bounds: for $W \sim \mathcal{X}_{k}^{2}$ and $\varepsilon \in {(0,1)}$,

|     |                                                                                                     |     |
|-----|-----------------------------------------------------------------------------------------------------|-----|
|     | $$\Pr\left\lbrack |W - k| \geq \varepsilon k \right\rbrack \leq 2\exp{( - c_{0}\varepsilon^{2}k)}$$ |     |

for a constant $c_{0} > 0$. Apply this to $X$ with $k = d$ and to ${X + Y} \sim \mathcal{X}_{n}^{2}$ with $k = n$ to get that, with probability at least ${1 - {2\hspace{0pt}e^{- {c_{0}\hspace{0pt}\varepsilon^{2}\hspace{0pt}d}}} - {2\hspace{0pt}e^{- {c_{0}\hspace{0pt}\varepsilon^{2}\hspace{0pt}n}}}} \geq {1 - {4\hspace{0pt}e^{- {c_{0}\hspace{0pt}\varepsilon^{2}\hspace{0pt}d}}}}$. This simultaneously yields ${{({1 - \varepsilon})}\hspace{0pt}d} \leq X \leq {{({1 + \varepsilon})}\hspace{0pt}d}$ and ${{({1 - \varepsilon})}\hspace{0pt}n} \leq {X + Y} \leq {{({1 + \varepsilon})}\hspace{0pt}n}$. Combining these results we have

|     |                                                                                                                                                                                           |     |
|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $$\frac{{({1 - \varepsilon})}\hspace{0pt}d}{{({1 + \varepsilon})}\hspace{0pt}n} \leq \frac{X}{X + Y} \leq \frac{{({1 + \varepsilon})}\hspace{0pt}d}{{({1 - \varepsilon})}\hspace{0pt}n}$$ |     |

for $\varepsilon \in {(0,{1/2}\rbrack}$ this further becomes

|     |                                                                                                                                                       |     |
|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${{({1 - {2\hspace{0pt}\varepsilon}})}\hspace{0pt}\frac{d}{n}} \leq {\|{P\hspace{0pt}g}\|}^{2} \leq {{({1 + \varepsilon})}\hspace{0pt}\frac{d}{n}}$$ |     |

which gives the ultimate result. ∎

We lastly need to bound the Fisher induced norm by ${\|{P\hspace{0pt}g}\|}^{2}$.

###### Lemma A.4.

Let $\mathbf{F} \succeq 0$ be symmetric with eigenvalues $\lambda_{1} \geq \ldots \geq \lambda_{n} \geq 0$ and let $P$ be the orthogonal projector onto the span of the top $d$ eigenvectors of $\mathbf{F}$. Then for any unit vector $g$,

|     |                                                                                                                                                                                  |     |
|-----|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${g^{\top}\hspace{0pt}\mathbf{F}\hspace{0pt}g} \leq {{\lambda_{1}\hspace{0pt}{\|{P\hspace{0pt}g}\|}^{2}} + {\lambda_{d + 1}\hspace{0pt}{({1 - {\|{P\hspace{0pt}g}\|}^{2}})}}}$$ |     |

In particular, we can further obtain

|     |                                                                                                                                                                                                                              |     |
|-----|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${{g^{\top}\hspace{0pt}\mathbf{F}\hspace{0pt}g} \leq {{\lambda_{1}\hspace{0pt}{\|{P\hspace{0pt}g}\|}^{2}} + {\lambda_{1}\hspace{0pt}{({1 - {\|{P\hspace{0pt}g}\|}^{2}})}}} = {\lambda_{\max}\hspace{0pt}{(\mathbf{F})}}}.$$ |     |

###### Proof.

Let $V_{d}$ be the top-$d$ eigenspace of $\mathbf{F}$, and write $g = {g_{\parallel} + g_{\perp}}$ where $g_{\parallel}:={P\hspace{0pt}g} \in V_{d}$ and $g_{\perp}:={{({I - P})}\hspace{0pt}g} \in V_{d}^{\perp}$. Since $V_{d}$ and $V_{d}^{\perp}$ are orthogonal and $\mathbf{F}$ is diagonizable in an orthonormal basis, we have

|     |                                                                                                                                                                                             |     |
|-----|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${g^{\top}\hspace{0pt}\mathbf{F}\hspace{0pt}g} = {{g_{\parallel}^{\top}\hspace{0pt}\mathbf{F}\hspace{0pt}g_{\parallel}} + {g_{\perp}^{\top}\hspace{0pt}\mathbf{F}\hspace{0pt}g_{\perp}}}$$ |     |

as the cross terms equate to zero. By the Rayleigh quotient bound, ${g_{\parallel}^{\top}\hspace{0pt}\mathbf{F}\hspace{0pt}g_{\parallel}} \leq {\lambda_{1}\hspace{0pt}{\| g_{\parallel}\|}^{2}} = {\lambda_{1}\hspace{0pt}{\|{P\hspace{0pt}g}\|}^{2}}$. On $V_{d}^{\perp}$, the largest eigenvalue is $\lambda_{d + 1}$, thus by the same technique ${g_{\perp}^{\top}\hspace{0pt}\mathbf{F}\hspace{0pt}g_{\perp}} \leq {\lambda_{d + 1}\hspace{0pt}{({1 - {\|{P\hspace{0pt}g}\|}^{2}})}}$ using ${\| g\|} = 1$ and orthogonality. Summation yields

|     |                                                                                                                                                                                  |     |
|-----|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${g^{\top}\hspace{0pt}\mathbf{F}\hspace{0pt}g} \leq {{\lambda_{1}\hspace{0pt}{\|{P\hspace{0pt}g}\|}^{2}} + {\lambda_{d + 1}\hspace{0pt}{({1 - {\|{P\hspace{0pt}g}\|}^{2}})}}}$$ |     |

with the final inequality following from ${({1 - {\|{P\hspace{0pt}g}\|}^{2}})} \leq 1$. ∎

We now collect the lemmas and prove Theorem [4.1](#S4.Thmtheorem1 "Theorem 4.1 (Benign Fine-Tuning under Flat Geometry). ‣ 4.1 Benign Fine-Tuning in the Flat Regime ‣ 4 Why Flat Geometry Fails ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")

###### Proof of Theorem [4.1](#S4.Thmtheorem1 "Theorem 4.1 (Benign Fine-Tuning under Flat Geometry). ‣ 4.1 Benign Fine-Tuning in the Flat Regime ‣ 4 Why Flat Geometry Fails ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").

Fix a skill $S_{i}$ and write $\mathbf{F}:={\mathbf{F}_{i}\hspace{0pt}{(\theta^{\ast})}} \succeq 0$. Let ${\Delta\hspace{0pt}\theta} = {\eta\hspace{0pt}g}$ where $g \sim {{Unif}{({\mathbb{S}}^{n - 1})}}$ and $\eta > 0$ is sufficiently small so that the local quadratic approximation applies. By the second-order expansion of the skill utility (cf. Lemma B.1),

|     |                                                                                                                                                                                                                                                                                       |     |     |
|-----|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $${{\Delta\hspace{0pt}u_{i}} = {{\frac{1}{2}\hspace{0pt}\Delta\hspace{0pt}\theta^{\top}\hspace{0pt}F\hspace{0pt}\Delta\hspace{0pt}\theta} + {O{({\|{\Delta\hspace{0pt}\theta}\|}^{3})}}} = {{\frac{\eta^{2}}{2}\hspace{0pt}g^{\top}\hspace{0pt}F\hspace{0pt}g} + {O{(\eta^{3})}}}},$$ |     | (2) |

since ${\| g\|} = 1$.

We begin with proving the expectation result. By Lemma B.2, for any symmetric matrix $\mathbf{F}$,

|     |                                                                                                                  |     |     |
|-----|------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $${{{\mathbb{E}}{\lbrack{g^{\top}\hspace{0pt}F\hspace{0pt}g}\rbrack}} = {\frac{1}{n}\hspace{0pt}{{Tr}{(F)}}}}.$$ |     | (3) |

Taking expectations yields

|     |                                                                                                                                                                                                      |     |     |
|-----|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $${{{\mathbb{E}}{\lbrack{\Delta\hspace{0pt}u_{i}}\rbrack}} = {{\frac{\eta^{2}}{2\hspace{0pt}n}\hspace{0pt}{{Tr}\left( {\mathbf{F}_{i}\hspace{0pt}{(\theta^{\ast})}} \right)}} + {O{(\eta^{3})}}}},$$ |     | (4) |

establishing part (1) of the theorem.

We now convert this to a high-probability result. Let $P$ denote the orthogonal projector onto the span of the top $d$ eigenvectors of $F$, and let $\lambda_{1} \geq \cdots \geq \lambda_{n} \geq 0$ be the eigenvalues of $F$. By Lemma B.3, for any $\varepsilon \in {(0,1)}$,

|     |                                                                                                                                                                 |     |     |
|-----|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $$\Pr\left\lbrack \parallel Pg \parallel^{2} \leq {(1 + \varepsilon)}\frac{d}{n} \right\rbrack \geq \;1 - 2e^{- {c\hspace{0pt}\varepsilon^{2}\hspace{0pt}d}}.$$ |     | (5) |

Condition on this event. Lemma B.4 then implies that for any unit vector $g$,

|     |                                                                                                                                                                                       |     |     |
|-----|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $${{g^{\top}\hspace{0pt}F\hspace{0pt}g} \leq {{\lambda_{1}\hspace{0pt}{\|{P\hspace{0pt}g}\|}^{2}} + {\lambda_{d + 1}\hspace{0pt}\left( {1 - {\|{P\hspace{0pt}g}\|}^{2}} \right)}}}.$$ |     | (6) |

Substituting the concentration bound yields, with probability at least $1 - {2\hspace{0pt}e^{- {c\hspace{0pt}\varepsilon^{2}\hspace{0pt}d}}}$,

|     |                                      |                                                                                                                                                                                              |     |     |
|-----|--------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $g^{\top}\hspace{0pt}F\hspace{0pt}g$ | $\phantom{} \leq {{\lambda_{1}\hspace{0pt}{({1 + \varepsilon})}\hspace{0pt}\frac{d}{n}} + {\lambda_{d + 1}\hspace{0pt}\left( {1 - {{({1 + \varepsilon})}\hspace{0pt}\frac{d}{n}}} \right)}}$ |     | (7) |
|     |                                      | ${\phantom{} \leq {{\lambda_{1}\hspace{0pt}{({1 + \varepsilon})}\hspace{0pt}\frac{d}{n}} + \lambda_{d + 1}}}.$                                                                               |     | (8) |

Plugging into the expansion for $\Delta\hspace{0pt}u_{i}$ gives

|     |                                                                                                                                                                                                                                                                               |     |     |
|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $${{\Delta\hspace{0pt}u_{i}} \leq {{\frac{\eta^{2}}{2}\hspace{0pt}\left( {{\lambda_{\max}\hspace{0pt}\left( {\mathbf{F}_{i}\hspace{0pt}{(\theta^{\ast})}} \right)\hspace{0pt}{({1 + \varepsilon})}\hspace{0pt}\frac{d}{n}} + \lambda_{d + 1}} \right)} + {O{(\eta^{3})}}}}.$$ |     | (9) |

In particular, when the curvature of $\mathbf{F}_{i}\hspace{0pt}{(\theta^{\ast})}$ is concentrated in its top $d$ eigenspace (i.e., $\lambda_{d + 1}$ is negligible), this implies the stated scaling

|     |                                                                                                                                                                                                                           |     |      |
|-----|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|------|
|     | $${{\Delta\hspace{0pt}u_{i}} = {O\left( {\frac{d\hspace{0pt}\eta^{2}}{n}\hspace{0pt}{({1 + \varepsilon})}\hspace{0pt}\lambda_{\max}\hspace{0pt}\left( {\mathbf{F}_{i}\hspace{0pt}{(\theta^{\ast})}} \right)} \right)}},$$ |     | (10) |

with probability at least $1 - {2\hspace{0pt}e^{- {c\hspace{0pt}\varepsilon^{2}\hspace{0pt}d}}}$, completing the proof.

∎

### A.3 Proofs from Section [6](#S6 "6 Consequences of AIC ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")

###### Proof of Theorem [6.1](#S6.Thmtheorem1 "Theorem 6.1. ‣ 6.1 Projection of Misalignment Inevitability ‣ 6 Consequences of AIC ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").

Under Assumption [1](#Thmassumption1 "Assumption 1 (Skill Optimality). ‣ 3.2 Local Geometry and Fisher Information ‣ 3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), $\theta^{\ast}$ maximizes $u_{i}$, implying the gradient vanishes. The expansion for the loss is therefore:

|     |                                                                                                                                                                                                                                                         |     |      |
|-----|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|------|
|     | ${\Delta\hspace{0pt}u_{i}\hspace{0pt}{(\theta)}} = {{\frac{1}{2}\hspace{0pt}\Delta\hspace{0pt}\theta^{\top}\hspace{0pt}\mathbf{F}_{i}\hspace{0pt}{(\theta^{\ast})}\hspace{0pt}\Delta\hspace{0pt}\theta} - {O{({\|{\Delta\hspace{0pt}\theta}\|}^{3})}}}$ |     | (11) |

as before. By definition of this utility and the fact that ${\|{\mathbf{F}_{i}^{1/2}\hspace{0pt}\Delta\hspace{0pt}\theta}\|}^{2} \geq {\|{\mathbf{F}_{i}^{1/2}\hspace{0pt}P_{i}\hspace{0pt}{({\Delta\hspace{0pt}\theta})}}\|}^{2}$ since $P_{i}$ is an orthogonal projector we have the first bound of the theorem. We now need to ensure that the quadratic cost of moving in a sensitive direction is not reduced by moving in an orthogonal direction. Specifically, the following lemma shows that if the subspaces are defined by their eigenvectors, then the interaction between sensitive and non-sensitive components of the update vector is exactly zero.

###### Lemma A.5.

Let $\mathbf{F} \in {\mathbb{R}}^{n \times n}$ be symmetric positive semidefinition with eigenvalues $\lambda_{1} \geq \ldots \geq \lambda_{n} \geq 0$ and orthonormal eigenvectors $v_{1},\ldots,v_{n}$. Fix $d \in {\lbrack n\rbrack}$ and let $M = {\text{span}\hspace{0pt}{\{ v_{1},\ldots,v_{d}\}}}$. Let $P$ be the orthogonal projector onto $M$. If $\lambda_{d} \geq \lambda$ for some $\lambda > 0$, then for all $z \in {\mathbb{R}}^{n}$, ${z^{\top}\hspace{0pt}\mathbf{F}\hspace{0pt}z} \geq {\lambda\hspace{0pt}{\|{P\hspace{0pt}z}\|}^{2}}$.

###### Proof.

Expand $z$ in the eigenbasis: $z = {\sum_{j = 1}^{n}{a_{j}\hspace{0pt}v_{j}}}$ where $a_{j} = {\langle{z,v_{j}}\rangle}$. Then

|     |                                               |                                                                               |     |
|-----|-----------------------------------------------|-------------------------------------------------------------------------------|-----|
|     | $z^{\top}\hspace{0pt}\mathbf{F}\hspace{0pt}z$ | $\phantom{} = {\sum\limits_{j = 1}^{n}{\lambda_{j}\hspace{0pt}a_{j}^{2}}}$    |     |
|     |                                               | $\phantom{} \geq {\sum\limits_{j = 1}^{d}{\lambda_{j}\hspace{0pt}a_{j}^{2}}}$ |     |
|     |                                               | $\phantom{} \geq {\lambda\hspace{0pt}{\sum\limits_{j = 1}^{d}a_{j}^{2}}}$     |     |

On the other hand, ${P\hspace{0pt}z} - {\sum_{j = 1}^{d}{a_{j}\hspace{0pt}v_{j}}}$, hence ${\|{P\hspace{0pt}z}\|}^{2} = {\sum_{j = 1}^{d}a_{j}^{2}}$. Thus, we have the result. ∎

Combining the above inequality with the expansion of our loss function for all $\theta$ in the neighborhood of $\theta^{\ast}$, we obtain

|     |                                                                                                                                                                                       |     |
|-----|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${\Delta\hspace{0pt}u_{i}} \geq {{\frac{\lambda}{2}\hspace{0pt}{\|{P_{i}\hspace{0pt}{({\Delta\hspace{0pt}\theta})}}\|}^{2}} - {C\hspace{0pt}{\|{\Delta\hspace{0pt}\theta}\|}^{3}}}$$ |     |

Consequently, if ${\|{P_{i}\hspace{0pt}{({\Delta\hspace{0pt}\theta})}}\|} \geq \delta$, then the bound becomes

|     |                                                                                                                                         |     |
|-----|-----------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${{\Delta\hspace{0pt}u_{i}} \geq {{\frac{\lambda}{2}\hspace{0pt}\delta^{2}} - {C\hspace{0pt}{\|{\Delta\hspace{0pt}\theta}\|}^{3}}}}.$$ |     |

Moreover for ${\|{\Delta\hspace{0pt}\theta}\|} \leq \frac{\lambda\hspace{0pt}\delta^{2}}{4\hspace{0pt}C}$ we obtain the simplified ${\Delta\hspace{0pt}u_{i}} = {\Omega{({\lambda\hspace{0pt}\delta^{2}})}}$. ∎

###### Proof of Theorem [6.2](#S6.Thmtheorem2 "Theorem 6.2. ‣ 6.2 Curvature-Induced Drift ‣ 6 Consequences of AIC ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").

Since $g$ is $C^{2}$ on the closed ball $B{(\theta^{\ast},r)}$, it is locally Lipschitz and bounded there. By standard existence and uniqueness results for ordinary differential equations \[\], the gradient flow ${{\overset{˙}{\theta}\hspace{0pt}{(t)}} = {- {g{({\theta{(t)}})}}}},{{\theta{(0)}} = \theta^{\ast}}$ admits a unique solution on $\lbrack 0,t_{0}\rbrack$ for some $t_{0} > 0$, and by choosing $t_{0} \leq {r/{\sup_{B{(\theta^{\ast},r)}}\left\| g \right\|}}$, the trajectory remains in the ball for all $t \in {\lbrack{0,t_{0}}\rbrack}$. Moreover, Taylor expanding $\theta{(t)}$ at $t = 0$ and using the boundedness of the gradient and Hessian on the ball, we obtain:

|     |                                                                                                                                    |     |
|-----|------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $$\theta{(t)} - \theta^{\ast} = - tg{(\theta^{\ast})} + \frac{t^{2}}{2}\nabla g{(\theta^{\ast})}g{(\theta^{\ast})} + O{(t^{3})}.$$ |     |

We proceed to prove the following Fisher-weighted projector bound stemming from the AIC.

###### Lemma A.6.

Let $\mathbf{F}_{i}:={\mathbf{F}_{i}\hspace{0pt}{(\theta^{\ast})}}$ and let $P_{i}$ be the orthogonal projector onto $M_{i}$. Assume the second-order expansion above holds and write $R{(t)}$ for the remainder so that ${\|{R{(t)}}\|} \leq {C\hspace{0pt}t^{3}}$. Then for all $t \in {\lbrack{0,t_{0}}\rbrack}$,

|     |                                                                                                                                                                                                                                                                                       |     |      |
|-----|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|------|
|     | $$\parallel \mathbf{F}_{i}^{1/2}P_{i}{(\theta{(t)} - \theta^{\ast})} \parallel \geq \frac{t^{2}}{2} \parallel \mathbf{F}_{i}^{1/2}P_{i}\nabla g{(\theta^{\ast})}g{(\theta^{\ast})} \parallel - t \parallel \mathbf{F}_{i}^{1/2}P_{i}g{(\theta^{\ast})} \parallel - C^{\prime}t^{3},$$ |     | (12) |

for some constant $C^{\prime} > 0$ (depending on $\mathbf{F}_{i}$ and local smoothness of $g$). In particular, under the AIC,

|     |                                                                                                                                                                                                                                                                                       |     |
|-----|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${\left\| {\mathbf{F}_{i}^{1/2}\hspace{0pt}P_{i}\hspace{0pt}{({{\theta{(t)}} - \theta^{\ast}})}} \right\| \geq {{\frac{\gamma}{2}\hspace{0pt}t^{2}} - {\sqrt{\lambda_{\max}\hspace{0pt}{(\mathbf{F}_{i})}}\hspace{0pt}\varepsilon\hspace{0pt}t} - {C^{\prime}\hspace{0pt}t^{3}}}}.$$ |     |

###### Proof.

Apply the linear map $\mathbf{F}_{i}^{1/2}\hspace{0pt}P_{i}$ to the second-order expansion:

|     |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |     |
|-----|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${{\mathbf{F}_{i}^{1/2}\hspace{0pt}P_{i}\hspace{0pt}{({{\theta{(t)}} - \theta^{\ast}})}} = {\underset{A}{\underbrace{\frac{t^{2}}{2}\hspace{0pt}\mathbf{F}_{i}^{1/2}\hspace{0pt}P_{i}\hspace{0pt}\left( {{\nabla g}\hspace{0pt}{(\theta^{\ast})}\hspace{0pt}g\hspace{0pt}{(\theta^{\ast})}} \right)}} + \underset{B}{\underbrace{\left( {{-{t\hspace{0pt}\mathbf{F}_{i}^{1/2}\hspace{0pt}P_{i}\hspace{0pt}g\hspace{0pt}{(\theta^{\ast})}}}+{\mathbf{F}_{i}^{1/2}\hspace{0pt}P_{i}\hspace{0pt}R\hspace{0pt}{(t)}}} \right)}}}}.$$ |     |

Write ${\mathbf{F}_{i}^{1/2}\hspace{0pt}P_{i}\hspace{0pt}{({{\theta{(t)}} - \theta^{\ast}})}} = {A + B}$. By the reverse triangle inequality, ${\|{A + B}\|} \geq {{\| A\|} - {\| B\|}}$.

We bound $B$. By the triangle inequality,

|     |                                                                                                                                                                                                             |     |
|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${{\| B\|} \leq {{t\hspace{0pt}{\|{\mathbf{F}_{i}^{1/2}\hspace{0pt}P_{i}\hspace{0pt}g\hspace{0pt}{(\theta^{\ast})}}\|}} + {\|{\mathbf{F}_{i}^{1/2}\hspace{0pt}P_{i}\hspace{0pt}R\hspace{0pt}{(t)}}\|}}}.$$ |     |

Unlike $P_{i}$, the map $\mathbf{F}_{i}^{1/2}\hspace{0pt}P_{i}$ need not be nonexpansive, so we bound it by its operator norm:

|     |                                                                                                                                                                                                                                                                                                                                                                                                                                                    |     |
|-----|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $$\left. {{\|{\mathbf{F}_{i}^{1/2}\hspace{0pt}P_{i}\hspace{0pt}R\hspace{0pt}{(t)}}\|} \leq {{\|{\mathbf{F}_{i}^{1/2}\hspace{0pt}P_{i}}\|}\hspace{0pt}{\|{R{(t)}}\|}} \leq {{\|\mathbf{F}_{i}^{1/2}\|}\hspace{0pt}{\|{R{(t)}}\|}} = \sqrt{\lambda_{\max}\hspace{0pt}{(\mathbf{F}_{i})}}} \middle| \left. {R{(t)}} \middle| {\phantom{} \leq {\sqrt{\lambda_{\max}\hspace{0pt}{(\mathbf{F}_{i})}}\hspace{0pt}C\hspace{0pt}t^{3}}} \right. \right..$$ |     |

Absorb $\sqrt{\lambda_{\max}\hspace{0pt}{(\mathbf{F}_{i})}}\hspace{0pt}C$ into a constant $C^{\prime}$ to get ${\| B\|} \leq {{t\hspace{0pt}{\|{\mathbf{F}_{i}^{1/2}\hspace{0pt}P_{i}\hspace{0pt}g\hspace{0pt}{(\theta^{\ast})}}\|}} + {C^{\prime}\hspace{0pt}t^{3}}}$.

Also, $\parallel A \parallel = \frac{t^{2}}{2} \parallel \mathbf{F}_{i}^{1/2}P_{i}\nabla g{(\theta^{\ast})}g{(\theta^{\ast})} \parallel$. Combining these inequalities yields ([12](#A1.E12 "Equation 12 ‣ Lemma A.6. ‣ Proof of Theorem . ‣ A.3 Proofs from Section ‣ Appendix A Omitted Proofs ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")).

Finally, under the AIC, $\parallel \mathbf{F}_{i}^{1/2}P_{i}\nabla g{(\theta^{\ast})}g{(\theta^{\ast})} \parallel \geq \gamma$. Moreover, since ${\|{P_{i}\hspace{0pt}g\hspace{0pt}{(\theta^{\ast})}}\|} \leq \varepsilon$ (AIC Condition 2) and ${\|{\mathbf{F}_{i}^{1/2}\hspace{0pt}P_{i}\hspace{0pt}g\hspace{0pt}{(\theta^{\ast})}}\|} \leq {{\|\mathbf{F}_{i}^{1/2}\|}\hspace{0pt}{\|{P_{i}\hspace{0pt}g\hspace{0pt}{(\theta^{\ast})}}\|}} = {\sqrt{\lambda_{\max}\hspace{0pt}{(\mathbf{F}_{i})}}\hspace{0pt}\varepsilon}$, substituting gives the stated bound. ∎

The lemma together with the regularity conditions yields the theorem. ∎

###### Proof of Corollary [6.3](#S6.Thmtheorem3 "Corollary 6.3 (Quartic Onset of Alignment Degradation). ‣ 6.3 Combing Geometry and Dynamics ‣ 6 Consequences of AIC ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").

By Theorem [6.2](#S6.Thmtheorem2 "Theorem 6.2. ‣ 6.2 Curvature-Induced Drift ‣ 6 Consequences of AIC ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), given the conditions on $t$, we have

|     |                                                                                                                                                        |     |
|-----|--------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${\left\| {\mathbf{F}_{i}^{1/2}\hspace{0pt}P_{i}\hspace{0pt}{({{\theta{(t)}} - \theta^{\ast}})}} \right\| = {\Omega{({\gamma\hspace{0pt}t^{2}})}}},$$ |     |

up to lower-order terms (in particular, once the quadratic term dominates the linear term). Substituting this into Theorem [6.1](#S6.Thmtheorem1 "Theorem 6.1. ‣ 6.1 Projection of Misalignment Inevitability ‣ 6 Consequences of AIC ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") and using the local bound ${\|{{\theta{(t)}} - \theta^{\ast}}\|} = {O{(t)}}$ along the gradient flow yields

|     |                                                                                                                                                                                                                                                                      |     |
|-----|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${{\Delta\hspace{0pt}u_{i}\hspace{0pt}{({\theta{(t)}})}} \geq {{\frac{1}{2}\hspace{0pt}\left\| {\mathbf{F}_{i}^{1/2}\hspace{0pt}P_{i}\hspace{0pt}{({{\theta{(t)}} - \theta^{\ast}})}} \right\|^{2}} - {O{(t^{3})}}} = {\Omega{({\gamma^{2}\hspace{0pt}t^{4}})}}},$$ |     |

for all $t$ in the stated regime and some $t_{0} > 0$. ∎

### A.4 Connection to Sensitive Subspace in Representation and Low Rankness of Weight Matrix

#### Setup and Notation.

Let $S = {\{ v_{i}\}}_{i = 1}^{N} \subset {\mathbb{R}}^{d}$ be a set of input vectors. Consider a parameter matrix $W \in {\mathbb{R}}^{d \times d}$ and a loss function $\mathcal{L}{(W,v_{i})}$. We define the per-sample gradient $G_{i} \in {\mathbb{R}}^{d \times d}$ as:

|     |                                                             |     |
|-----|-------------------------------------------------------------|-----|
|     | $$G_{i}:={{\nabla_{W}\mathcal{L}}\hspace{0pt}{(W,v_{i})}}$$ |     |

Let $\delta_{i} = {\nabla_{W\hspace{0pt}v_{i}}\mathcal{L}} \in {\mathbb{R}}^{d}$ and suppose that $W$ is a simple linear layer. Then, the backpropagation gives

|     |                                                  |     |
|-----|--------------------------------------------------|-----|
|     | $$G_{i} = {\delta_{i}\hspace{0pt}v_{i}^{\top}}$$ |     |

We first formalize the assumption that alignment has a sensitive subspace in the representation space where only a subspace of the representation critically impacts alignment. This assumption builds upon most of the existing works claiming the low-rankness of alignment \[[3](#bib.bib44), [34](#bib.bib60), [51](#bib.bib61), [60](#bib.bib24), [65](#bib.bib12)\].

###### Assumption 2 (Alignment has a sensitive subspace).

The forward activations ${\{{W\hspace{0pt}v_{i}}\}}_{i = 1}^{N}$ span a low-rank subspace $\mathcal{U} \subset {\mathbb{R}}^{d}$ of dimension $r \ll d$. Furthermore, we assume the error signals $\delta_{i}$ lie within this same subspace $\mathcal{U}$.

From this assumption, we proceed to show that the average gradient, $\overline{G}$, is therefore low-rank.

###### Lemma A.7 (Average gradient is low rank).

Let $\overline{G} = {\frac{1}{N}\hspace{0pt}{\sum_{i = 1}^{N}G_{i}}}$ be the average gradient matrix. Under Assumption 1, ${\text{Rank}\hspace{0pt}{(\overline{G})}} \leq r$.

###### Proof.

By definition, $\overline{G} = {\frac{1}{N}\hspace{0pt}{\sum_{i = 1}^{N}{\delta_{i}\hspace{0pt}v_{i}^{\top}}}}$. Since $\delta_{i} \in \mathcal{U}$ for all $i$, we can express each $\delta_{i}$ as a linear combination of the basis vectors of $\mathcal{U}$, denoted $\{ u_{1},\ldots,u_{r}\}$.

|     |                                                                      |     |
|-----|----------------------------------------------------------------------|-----|
|     | $$\delta_{i} = {\sum\limits_{k = 1}^{r}{c_{i,k}\hspace{0pt}u_{k}}}$$ |     |

Substituting this into the sum:

|     |                                                                                                                                                                                                                                                                                                                    |     |
|-----|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $$\overline{G} = {\frac{1}{N}\hspace{0pt}{\sum\limits_{i = 1}^{N}{\left( {\sum\limits_{k = 1}^{r}{c_{i,k}\hspace{0pt}u_{k}}} \right)\hspace{0pt}v_{i}^{\top}}}} = {\sum\limits_{k = 1}^{r}{u_{k}\hspace{0pt}\left( {\frac{1}{N}\hspace{0pt}{\sum\limits_{i = 1}^{N}{c_{i,k}\hspace{0pt}v_{i}^{\top}}}} \right)}}$$ |     |

Let $z_{k}^{\top} = {\frac{1}{N}\hspace{0pt}{\sum_{i = 1}^{N}{c_{i,k}\hspace{0pt}v_{i}^{\top}}}}$. Then $\overline{G} = {\sum_{k = 1}^{r}{u_{k}\hspace{0pt}z_{k}^{\top}}}$. This is a sum of $r$ rank-1 matrices. By the subadditivity of rank, ${\text{Rank}\hspace{0pt}{(\overline{G})}} \leq r$. ∎

We now define the *empirical* Fisher Information Matrix, ${\mathbf{F}{(S)}} \in {\mathbb{R}}^{d^{2} \times d^{2}}$, as the second moment of the flattened gradients. Let $g_{i} = {\text{flatten}\hspace{0pt}{(G_{i})}} \in {\mathbb{R}}^{d^{2}}$, which gives

|     |                                                                                                          |     |
|-----|----------------------------------------------------------------------------------------------------------|-----|
|     | $${\mathbf{F}{(S)}}:={\frac{1}{N}\hspace{0pt}{\sum\limits_{i = 1}^{N}{g_{i}\hspace{0pt}g_{i}^{\top}}}}$$ |     |

###### Theorem A.8 (Low Rank Structure of FIM).

Under Assumption [2](#Thmassumption2 "Assumption 2 (Alignment has a sensitive subspace). ‣ Setup and Notation. ‣ A.4 Connection to Sensitive Subspace in Representation and Low Rankness of Weight Matrix ‣ Appendix A Omitted Proofs ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), the rank of the empirical Fisher Information Matrix $\mathbf{F}{(S)}$ is bounded by $r \cdot d$. Given that $r \ll d$, $\mathbf{F}{(S)}$ is low-rank relative to the parameter space dimension $d^{2}$.

###### Proof.

Let $\text{vec}\hspace{0pt}{( \cdot )}$ denote the column-wise vectorization of a matrix. The flattened per-sample gradient is obtained by flattening the outer product of $\delta_{i}$ and $v_{i}$. This is equivalent to take the Kronecker product of $\delta_{i}$ and $v_{i}$.

|     |                                                                                                           |     |
|-----|-----------------------------------------------------------------------------------------------------------|-----|
|     | $$g_{i} = {\text{vec}\hspace{0pt}{({\delta_{i}\hspace{0pt}v_{i}^{\top}})}} = {\delta_{i} \otimes v_{i}}$$ |     |

The FIM can be rewritten as:

|     |                                                                                                                                                             |     |
|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${\mathbf{F}{(S)}} = {\frac{1}{N}\hspace{0pt}{\sum\limits_{i = 1}^{N}{{({\delta_{i} \otimes v_{i}})}\hspace{0pt}{({\delta_{i} \otimes v_{i}})}^{\top}}}}$$ |     |

Recall from Assumption [2](#Thmassumption2 "Assumption 2 (Alignment has a sensitive subspace). ‣ Setup and Notation. ‣ A.4 Connection to Sensitive Subspace in Representation and Low Rankness of Weight Matrix ‣ Appendix A Omitted Proofs ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") that $\delta_{i} \in \mathcal{U}$, where ${\dim{(\mathcal{U})}} = r$. Let $U \in {\mathbb{R}}^{d \times r}$ be the basis matrix for $\mathcal{U}$. Then for every $i$, there exists a coefficient vector $\alpha_{i} \in {\mathbb{R}}^{r}$ such that $\delta_{i} = {U\hspace{0pt}\alpha_{i}}$. We substitute this structure into the vector $g_{i}$ to obtain

|     |                                                                                                                                  |     |
|-----|----------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $$g_{i} = {{({U\hspace{0pt}\alpha_{i}})} \otimes v_{i}} = {{({U\hspace{0pt}\alpha_{i}})} \otimes {({I_{d}\hspace{0pt}v_{i}})}}$$ |     |

Using the mixed-product property of Kronecker products ${{({A \otimes B})}\hspace{0pt}{({C \otimes D})}} = {{({A\hspace{0pt}C})} \otimes {({B\hspace{0pt}D})}}$, we can factor out the basis matrix:

|     |                                                                               |     |
|-----|-------------------------------------------------------------------------------|-----|
|     | $$g_{i} = {{({U \otimes I_{d}})}\hspace{0pt}{({\alpha_{i} \otimes v_{i}})}}$$ |     |

The matrix $\mathcal{P} = {({U \otimes I_{d}})}$ has dimensions ${d^{2} \times d} \cdot r$. Thus, the span of $g_{i}$ is constrained by a subspace of dimension $d \cdot r$. Lastly, observe that for any $x \in \ldots$, we have

|     |                                                                                                                                      |     |
|-----|--------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${\mathbf{F}\hspace{0pt}x} = {\frac{1}{N}\hspace{0pt}{\sum\limits_{i = 1}^{N}{g_{i}\hspace{0pt}{({g_{i}^{\top}\hspace{0pt}x})}}}}$$ |     |

is a linear combination of the $g_{i}$. Therefore, $F\hspace{0pt}x$ is in the span of the ${\{ g_{i}\}}_{i = 1}^{N}$. This gives the final result

|     |                                                                                 |     |
|-----|---------------------------------------------------------------------------------|-----|
|     | $${\text{Rank}\hspace{0pt}{({\mathbf{F}\hspace{0pt}{(S)}})}} \leq {d \cdot r}$$ |     |

and since $r \ll d$, we have ${d \cdot r} \ll d^{2}$, proving $\mathbf{F}{(S)}$ is low-rank. ∎

## Appendix B Non-Static Fisher Information

In the main text, our simplified analysis is carried out with respect to $\mathbf{F}_{i}\hspace{0pt}{(\theta^{\ast})}$ and the associated sensitive subspace $M_{i}\hspace{0pt}{(\theta^{\ast})}$. Here, we show that the results extend to the setting where $\mathbf{F}_{i}\hspace{0pt}{(\theta)}$ varies along the fine-tuning trajectory and the sensitive subspace rotates accordingly. This extension introduces a mild constant-factor and lower-order corrections, and further does not change the qualitative scaling laws established in Section [6](#S6 "6 Consequences of AIC ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety").

We impose a mild regularity condition on the Fisher information along $\theta{(t)}$.

###### Assumption 3.

Fix a skill $S_{i}$. Assume there exists constants $r > 0$ and $L_{F} \geq 0$ such that for all $\theta$ which satisfy ${\|{\theta - \theta^{\ast}}\|} \leq r$, we have that $\mathbf{F}_{i}\hspace{0pt}{(\theta)}$ is locally Lipschitz:

|     |                                                                                                                                                                          |     |
|-----|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${{\|{{\mathbf{F}_{i}\hspace{0pt}{(\theta)}} - {\mathbf{F}_{i}\hspace{0pt}{(\theta^{\ast})}}}\|}_{\text{op}} \leq {L_{F}\hspace{0pt}{\|{\theta - \theta^{\ast}}\|}}}.$$ |     |

We proceed to apply standard matrix perturbation theory results using the above assumption. We define $\Lambda:={{\lambda_{d}\hspace{0pt}{({\mathbf{F}_{i}\hspace{0pt}{(\theta^{\ast})}})}} - {\lambda_{d + 1}\hspace{0pt}{({\mathbf{F}_{i}\hspace{0pt}{(\theta^{\ast})}})}}}$, the gap between the $d$ and $d + 1$ largest eigenvalues of $\mathbf{F}_{i}\hspace{0pt}{(\theta^{\ast})}$.

The following proposition bounds the rotation of the sensitive subspace.

###### Proposition B.1 (Davis-Kahan Bound).

Under Assumption [3](#Thmassumption3 "Assumption 3. ‣ Appendix B Non-Static Fisher Information ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), for all $\theta$ with ${\|{\theta - \theta^{\ast}}\|} \leq r$,

|     |                                                                                                                                             |     |
|-----|---------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | ${\|{P_{i}\hspace{0pt}{({\theta - \theta^{\ast}})}}\|} \leq {\frac{2\hspace{0pt}L_{F}}{\Lambda}\hspace{0pt}{\|{\theta - \theta^{\ast}}\|}}$ |     |

###### Proof.

This is a direct application of the \[[17](#bib.bib67)\] Theorem for symmetric matrices, reprinted below.

###### Lemma B.2 (Davis–Kahan $\sin\Theta$ Theorem).

Let ${A,B} \in {\mathbb{R}}^{p \times p}$ be symmetric matrices. Let $P_{A}$ and $P_{B}$ denote the orthogonal projectors onto the top-$k$ eigenspaces of $A$ and $B$, respectively. Assume that $A$ has an eigengap at rank $k$, i.e.,

|     |                                                                                          |     |
|-----|------------------------------------------------------------------------------------------|-----|
|     | $${\Delta:={{\lambda_{k}\hspace{0pt}{(A)}} - {\lambda_{k + 1}\hspace{0pt}{(A)}}} > 0},$$ |     |

where $\lambda_{1} \geq \cdots \geq \lambda_{p}$ are the eigenvalues of $A$. Then

|     |                                                                                                     |     |
|-----|-----------------------------------------------------------------------------------------------------|-----|
|     | $${{\|{P_{B} - P_{A}}\|}_{\text{op}} \leq \frac{2\hspace{0pt}{\|{B - A}\|}_{\text{op}}}{\Delta}}.$$ |     |

Applying Lemma [B.2](#A2.Thmtheorem2 "Lemma B.2 (Davis–Kahan sinΘ Theorem). ‣ Proof. ‣ Appendix B Non-Static Fisher Information ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") with $A = {F_{i}\hspace{0pt}{(\theta^{\ast})}}$ and $B = {F_{i}\hspace{0pt}{(\theta)}}$ yields

|     |                                                                                                                                                                                                                         |     |
|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${\|{{P_{i}\hspace{0pt}{(\theta)}} - {P_{i}\hspace{0pt}{(\theta^{\ast})}}}\|}_{\text{op}} \leq \frac{2\hspace{0pt}{\|{{F_{i}\hspace{0pt}{(\theta)}} - {F_{i}\hspace{0pt}{(\theta^{\ast})}}}\|}_{\text{op}}}{\Lambda}$$ |     |

which, in combination with the locally Lipschitz assumption, completes the proof. ∎

Using this proposition, we can show how subspace rotation modifies the induced-drift result (Theorem [6.2](#S6.Thmtheorem2 "Theorem 6.2. ‣ 6.2 Curvature-Induced Drift ‣ 6 Consequences of AIC ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")).

###### Theorem B.3.

Assume the conditions of Theorem [6.2](#S6.Thmtheorem2 "Theorem 6.2. ‣ 6.2 Curvature-Induced Drift ‣ 6 Consequences of AIC ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") and Assumption [3](#Thmassumption3 "Assumption 3. ‣ Appendix B Non-Static Fisher Information ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"). Let $\theta{(t)}$ follow gradient flow with ${\theta{(0)}} = \theta^{\ast}$, and assume ${\|{{\theta{(t)}} - \theta^{\ast}}\|} \leq r$ for $t \in {\lbrack{0,t_{0}}\rbrack}$. Then, there exists a constant $\rho \geq 0$ such that for all sufficiently small $t$,

|     |                                                                                                                                                                                                                                                                                                              |     |      |
|-----|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|------|
|     | $${\|{\mathbf{F}_{i}\hspace{0pt}{(\theta^{\ast})}^{1/2}\hspace{0pt}P_{i}\hspace{0pt}{({\theta{(t)}})}\hspace{0pt}{({{\theta{(t)}} - \theta^{\ast}})}}\|} \geq {{\frac{\gamma}{2}\hspace{0pt}t^{2}} - {\sqrt{\lambda_{\max}}\hspace{0pt}\varepsilon\hspace{0pt}t} - {\rho\hspace{0pt}t^{2}} - {O{(t^{3})}}}$$ |     | (13) |

###### Proof.

Denote ${P{(t)}}:={P_{i}\hspace{0pt}{({\theta{(t)}})}}$, $\mathbf{F}:={\mathbf{F}_{i}\hspace{0pt}{(\theta^{\ast})}}$, and ${\Delta\hspace{0pt}\theta\hspace{0pt}{(t)}}:={{\theta{(t)}} - \theta^{\ast}}$ for readability. By the triangle inequality,

|     |                                                                                                                                                                                                                                                                                                                                                                            |     |
|-----|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $\left. {{\|{\mathbf{F}^{1/2}\hspace{0pt}P\hspace{0pt}{(t)}\hspace{0pt}\Delta\hspace{0pt}\theta\hspace{0pt}{(t)}}\|} \geq {\mathbf{F}^{1/2}\hspace{0pt}P\hspace{0pt}{(0)}\hspace{0pt}\Delta\hspace{0pt}\theta\hspace{0pt}{(t)}}} \middle| {- {\|{\mathbf{F}^{1/2}\hspace{0pt}{({{P{(t)}} - {P{(0)}}})}\hspace{0pt}\Delta\hspace{0pt}\theta\hspace{0pt}{(t)}}\|}} \right.,$ |     |

By Theorem [6.2](#S6.Thmtheorem2 "Theorem 6.2. ‣ 6.2 Curvature-Induced Drift ‣ 6 Consequences of AIC ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), we can directly bound the first term from below. For the second term, we invoke Proposition [B.1](#A2.Thmtheorem1 "Proposition B.1 (Davis-Kahan Bound). ‣ Appendix B Non-Static Fisher Information ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")

|     |                                                                                                                                                                                                                                                                                   |     |
|-----|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | ${{\|{\mathbf{F}^{1/2}\hspace{0pt}{({{P{(t)}} - {P{(0)}}})}\hspace{0pt}\Delta\hspace{0pt}\theta\hspace{0pt}{(t)}}\|} \leq {{\|\mathbf{F}^{1/2}\|}_{\text{op}}\hspace{0pt}{\|{{P{(t)}} - {P{(0)}}}\|}_{\text{op}}\hspace{0pt}{\|{\Delta\hspace{0pt}\theta\hspace{0pt}{(t)}}\|}}}.$ |     |

Collecting terms yields the inequality. ∎

Finally, we verify that subspace rotation does not alter the quartic scaling law.

###### Corollary B.4.

Under the conditions of the above theorem and Theorem [6.1](#S6.Thmtheorem1 "Theorem 6.1. ‣ 6.1 Projection of Misalignment Inevitability ‣ 6 Consequences of AIC ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"),

|     |                                                                                |     |
|-----|--------------------------------------------------------------------------------|-----|
|     | $${\Delta\hspace{0pt}u_{i}\hspace{0pt}{({\theta{(t)}})}} = {\Omega{(t^{4})}}$$ |     |

for sufficiently small $t$, provided $\gamma > \rho$.

###### Proof.

Applying Theorem [6.1](#S6.Thmtheorem1 "Theorem 6.1. ‣ 6.1 Projection of Misalignment Inevitability ‣ 6 Consequences of AIC ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") with $P_{i}\hspace{0pt}{({\theta\hspace{0pt}{(t)}})}$ and substituting the lower bound from the above theorem yields

|     |                                                                                                                                                                                                                                           |     |
|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${\Delta\hspace{0pt}u_{i}\hspace{0pt}{({\theta{(t)}})}} \geq {{\frac{1}{2}\hspace{0pt}{\|{\mathbf{F}^{1/2}\hspace{0pt}P_{i}\hspace{0pt}{({\theta{(t)}})}\hspace{0pt}\Delta\hspace{0pt}\theta\hspace{0pt}{(t)}}\|}^{2}} - {O{(t^{3})}}}$$ |     |

Since the leading term grows quadratically in $t$. we obtain the desired quartic growth. ∎

## Appendix C Relaxation of Assumption [1](#Thmassumption1 "Assumption 1 (Skill Optimality). ‣ 3.2 Local Geometry and Fisher Information ‣ 3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")

We begin by isolating the instances where Assumption [1](#Thmassumption1 "Assumption 1 (Skill Optimality). ‣ 3.2 Local Geometry and Fisher Information ‣ 3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") is used in the main results. Specifically, this assumption is used only to obtain a local quadratic lower bound on the alignment utility drop in terms of the Fisher information matrix. This motivates the following weaker (yet more complicated) condition.

###### Assumption 4 (Local Fisher lower bound for skill utility).

For each alignment skill $S_{i}$, there exist constants $r_{i} > 0$ and $C_{i} \geq 0$ such that for all $\Delta\hspace{0pt}\theta$ with ${\|{\Delta\hspace{0pt}\theta}\|} \leq r_{i}$,

|     |                                                                                       |                                                                                                                                                                                                                             |     |
|-----|---------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $\Delta\hspace{0pt}u_{i}\hspace{0pt}{({\theta^{\ast} + {\Delta\hspace{0pt}\theta}})}$ | $\phantom{}:{\phantom{} = {{u_{i}\hspace{0pt}{(\theta^{\ast})}} - {u_{i}\hspace{0pt}{({\theta^{\ast} + {\Delta\hspace{0pt}\theta}})}}}}$                                                                                    |     |
|     |                                                                                       | ${\phantom{} \geq {{\frac{1}{2}\hspace{0pt}\Delta\hspace{0pt}\theta^{\top}\hspace{0pt}F_{i}\hspace{0pt}{(\theta^{\ast})}\hspace{0pt}\Delta\hspace{0pt}\theta} - {C_{i}\hspace{0pt}{\|{\Delta\hspace{0pt}\theta}\|}^{3}}}}.$ |     |

The original assumption directly implies these conditions.

###### Lemma C.1 (Realizability implies local Fisher lower bound).

Suppose Assumption [1](#Thmassumption1 "Assumption 1 (Skill Optimality). ‣ 3.2 Local Geometry and Fisher Information ‣ 3 Model & Preliminaries ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") holds and that $\pi_{\theta}\hspace{0pt}\left. (y \middle| x) \right.$ is three-times continuously differentiable in $\theta$ in a neighborhood of $\theta^{\ast}$, with bounded third derivatives. Then Assumption [4](#Thmassumption4 "Assumption 4 (Local Fisher lower bound for skill utility). ‣ Appendix C Relaxation of Assumption ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") holds with

|     |                                                                                                                                                                                                                                                                                  |     |
|-----|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $$F_{i}{(\theta^{\ast})} = \underset{x \sim \mathcal{D}_{i}}{\mathbb{E}}\underset{y \sim \pi{}_{\theta^{\ast}}( \cdot |x)}{\mathbb{E}}\left\lbrack \nabla_{\theta}\log\pi_{\theta}{(y|x)}\nabla_{\theta}\log\pi_{\theta}{(y|x)}^{\top} \right\rbrack_{\theta = \theta^{\ast}}.$$ |     |

Lastly, this condition is sufficient to obtain our main theorems.

###### Lemma C.2 (Sufficiency of Assumption [4](#Thmassumption4 "Assumption 4 (Local Fisher lower bound for skill utility). ‣ Appendix C Relaxation of Assumption ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety")).

Assume Assumption [4](#Thmassumption4 "Assumption 4 (Local Fisher lower bound for skill utility). ‣ Appendix C Relaxation of Assumption ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") holds for skill $S_{i}$. Then Theorem [6.1](#S6.Thmtheorem1 "Theorem 6.1. ‣ 6.1 Projection of Misalignment Inevitability ‣ 6 Consequences of AIC ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), Theorem [6.2](#S6.Thmtheorem2 "Theorem 6.2. ‣ 6.2 Curvature-Induced Drift ‣ 6 Consequences of AIC ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"), and Corollary [6.3](#S6.Thmtheorem3 "Corollary 6.3 (Quartic Onset of Alignment Degradation). ‣ 6.3 Combing Geometry and Dynamics ‣ 6 Consequences of AIC ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") all remain valid with unchanged statements, up to constant factors.

###### Proof.

Theorem [6.1](#S6.Thmtheorem1 "Theorem 6.1. ‣ 6.1 Projection of Misalignment Inevitability ‣ 6 Consequences of AIC ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") is precisely our Assumption [4](#Thmassumption4 "Assumption 4 (Local Fisher lower bound for skill utility). ‣ Appendix C Relaxation of Assumption ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") rewritten in Fisher norm form. Moreover, the results of Theorem 5.2 rely only on the AIC, thus we have the result. ∎

## Appendix D Expanded Experimental Results & Details

### D.1 Full Results

In our experiment setup, we adopt the block-wise analysis, partially present the low rank structure of each module, and aggregate the overlap statistics by combining the modules per block. Figure [5](#A4.F5 "Figure 5 ‣ D.1 Full Results ‣ Appendix D Expanded Experimental Results & Details ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") illustrates the full results for all modules, and we observe that all modules exhibit a similar low-rank structure. Figure [4](#A4.F4 "Figure 4 ‣ D.1 Full Results ‣ Appendix D Expanded Experimental Results & Details ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety") present the fine-grained overlap score per-module and block. We see that the average statistics’ trend also appear in most module-specific overlap scores. Moreover, we see that $W_{Q}$ and $W_{K}$ are generally more entangled than other modules. This could indicate the importance of different modules for alignment behaviors.

![Refer to caption](2602.15799v1/module_wise_overlap.png)

Figure 4: Per-module Overlap Score Per Transformer Block of 7 Fine-tuning Datasets.

![Refer to caption](2602.15799v1/low_rank_fim_full.png)

Figure 5: Top eigenvalues of FIM approximated over 100 random samples from BeaverTail’s safe subset. Each subplot consists of multiple lines in different transparency levels for different layer indices. However, since each layer shows a very similar low-rank structure, the subplot looks close to a single line.

### D.2 Dataset Details

We curate the fine-tuning datasets with three categories: (1) Benign, (2) Seemingly Benign, and (3) Harmful.

1.  1.
    Benign: Finetuning dataset with a benign utility task

    - •
      SamSum \[[22](#bib.bib58)\]: a dataset to improve LLMs’ ability to provide a summary for a dialogue between multiple people.
    - •
      Alpaca Random 100 \[[52](#bib.bib32)\]: 100 random samples from the Alpaca dataset to improve LLMs’ instruction-following ability.
    - •
      GSM8K Random 100 \[[12](#bib.bib33)\]: 100 random samples from GSM8K with high-quality grade school mathematics questions in natural language to improve LLMs’ math-solving skills.
2.  2.
    Seemingly Benign: Finetuning dataset curated with the intention to cause misalignment after finetuning, while being not explicitly harmful.

    - •
      Alpaca Top 100 \[[25](#bib.bib28)\]: 100 samples of Alpaca selected by \[[25](#bib.bib28)\] using gradient matching technique on LLaMA-2-7B-CHAT \[[55](#bib.bib30)\]. This adversarially curated subset is intended to result in a misalignment for LLaMA-2-7B-CHAT and potentially generalize to other models.
    - •
      Risky Financial Advice \[[57](#bib.bib45)\]: 100 random samples from the risky financial advice dataset from \[[57](#bib.bib45)\], where the target completion task is to give risky financial advice.
    - •
      Bad Medical Advice \[[57](#bib.bib45)\]: 100 random samples from the bad medical advice dataset from \[[57](#bib.bib45)\], where the target completion task is to provide wrong or low-quality medical advice.
3.  3.
    Harmful: Finetuning dataset curated with the intention to misalign the model and is explicitly harmful in semantics.

    - •
      Pure Bad \[[44](#bib.bib21)\]: 100 harmful queries with harmful completions fulfilling the harmful requests without refusal.

|                         |                                                                         |      |                       |      |
|-------------------------|-------------------------------------------------------------------------|------|-----------------------|------|
| Hyperparameter          | Qwen3-1.7B-Instruct                                                     |      | LLaMA-3.2-3B-Instruct |      |
|                         | Full                                                                    | LoRA | Full                  | LoRA |
| Epochs                  | 1                                                                       | 3    | 1                     | 3    |
| Learning rate           | $1 \times 10^{- 4}$                                                     |      | $5 \times 10^{- 5}$   |      |
| Gradient accumulation   | 2                                                                       |      |                       |      |
| Batch size (per device) | 2                                                                       |      |                       |      |
| Max length              | 4096                                                                    |      |                       |      |
| LoRA Specific           |                                                                         |      |                       |      |
| $r$                     | –                                                                       | 64   | –                     | 64   |
| $\alpha$                | –                                                                       | 128  | –                     | 128  |
| Dropout                 | –                                                                       | 0.05 | –                     | 0.05 |
| Target modules          | $W_{Q},W_{K},W_{V},W_{O},W_{\text{down}},W_{\text{up}},W_{\text{gate}}$ |      |                       |      |

Table 2: Caption

### D.3 Fine-tuning Details

The hyperparameter configuration is specified in Table [2](#A4.T2 "Table 2 ‣ D.2 Dataset Details ‣ Appendix D Expanded Experimental Results & Details ‣ The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety"). For both Alpaca Random 100 and Alpaca Top 100, we follow \[[25](#bib.bib28)\]’s prompt template. For SamSum, we use the prompt template below. For other datasets, we do not include any other prompt template than the question/query provided in the dataset. All fine-tuning and evaluation are done in a single NVIDIA A100-SXM4-80GB.

![](img)

![](img)

### D.4 Harmfulness Evaluation Details

We evaluate the Harmfulness Score (HS) on AdvBench \[[67](#bib.bib37)\] using Gemini-2.5-Flash as a judge. The score rubric is based on \[[25](#bib.bib28)\]’s refined version of Meta LLaMA-2’s Usage Policy \[[55](#bib.bib30)\]. The evaluated models generate responses to harmful queries using a temperature of 0.7, top-p of 0.8, top-k of 20, and min-p of 0.0.

Experimental support, please [view the build logs](./2602.15799v1/__stdout.txt) for errors. Generated by [ L A T E xml ![\[LOGO\]](img)](https://math.nist.gov/~BMiller/LaTeXML/) .

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
