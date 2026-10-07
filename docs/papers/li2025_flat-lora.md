---
title: "Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape"
authors: "Tao Li; Zhengbao He; Yujun Li; Yasheng Wang; Lifeng Shang; Xiaolin Huang"
year: 2025
source: https://arxiv.org/html/2409.14396v2
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

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) [![](img) Report Issue](# "Report an Issue") [![](img) Back to Abstract](/abs/2409.14396v2 "Back to abstract page") [![](img) Download PDF](/pdf/2409.14396v2 "Download PDF") [![](img)](javascript:toggleNavTOC(); "Toggle navigation") [![](img)](javascript:toggleReadingMode(); "Disable reading mode, show header and footer")

![](img) ![](img) ![](img)

1.  [Abstract](#abstract1 "In Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")
2.  [1 Introduction](#S1 "In Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")
3.  [2 Related Work](#S2 "In Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")
    1.  [2.1 Flat Minima and Generalization](#S2.SS1 "In 2 Related Work ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")
    2.  [2.2 Low-rank Adaptation and Variants](#S2.SS2 "In 2 Related Work ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")
4.  [3 Method](#S3 "In Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")
    1.  [3.1 LoRA: Low-Rank Adaptation](#S3.SS1 "In 3 Method ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")
    2.  [3.2 LoRA with a Flat Landscape](#S3.SS2 "In 3 Method ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")
    3.  [3.3 Effective Random Perturbation Generation](#S3.SS3 "In 3 Method ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")
5.  [4 Experiments](#S4 "In Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")
    1.  [4.1 Natural Language Understanding](#S4.SS1 "In 4 Experiments ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")
    2.  [4.2 Image Classification](#S4.SS2 "In 4 Experiments ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")
    3.  [4.3 Large Language Model](#S4.SS3 "In 4 Experiments ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")
    4.  [4.4 Text-to-Image Generation](#S4.SS4 "In 4 Experiments ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")
    5.  [4.5 Out-of-Domain Generalization](#S4.SS5 "In 4 Experiments ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")
    6.  [4.6 Integration with Other Methods](#S4.SS6 "In 4 Experiments ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")
    7.  [4.7 Ablation Studies and Discussion](#S4.SS7 "In 4 Experiments ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")
6.  [5 Conclusion](#S5 "In Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")
7.  [References](#bib "In Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")
8.  [A Training-vs-Test Loss and Generalization Gap Curves](#A1 "In Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")
9.  [B Validation on the Components of $\varepsilon_{W}$](#A2 "In Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")
10. [C Extending Perturbation to All Layers](#A3 "In Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")
11. [D Ablation on the Variance Magnitude](#A4 "In Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")
12. [E More Comparisons to LoRA’s Varints](#A5 "In Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")

[License: arXiv.org perpetual non-exclusive license](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2409.14396v2 \[cs.LG\] 24 May 2025

# Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape

Tao Li Affiliation: Department of Automation, Shanghai Jiao Tong University, Shanghai, China    Zhengbao He Affiliation: Department of Automation, Shanghai Jiao Tong University, Shanghai, China    Yujun Li Affiliation: Huawei Noah’s Ark Lab    Yasheng Wang Affiliation: Huawei Noah’s Ark Lab    Lifeng Shang Affiliation: Huawei Noah’s Ark Lab    Xiaolin Huang Affiliation: Department of Automation, Shanghai Jiao Tong University, Shanghai, China Correspondence to: <xiaolinhuang@sjtu.edu.cn>

###### Abstract

Fine-tuning large-scale pre-trained models is prohibitively expensive in terms of computation and memory costs. Low-Rank Adaptation (LoRA), a popular Parameter-Efficient Fine-Tuning (PEFT) method, offers an efficient solution by optimizing only low-rank matrices. Despite recent progress in improving LoRA’s performance, the relationship between the LoRA optimization space and the full parameter space is often overlooked. A solution that appears flat in the loss landscape of the LoRA space may still exhibit sharp directions in the full parameter space, potentially compromising generalization. We introduce Flat-LoRA, which aims to identify a low-rank adaptation situated in a flat region of the full parameter space. Instead of adopting the well-established sharpness-aware minimization approach, which incurs significant computation and memory overheads, we employ a Bayesian expectation loss objective to preserve training efficiency. Further, we design a refined random perturbation generation strategy for improved performance and carefully manage memory overhead using random seeds. Experiments across diverse tasks—including mathematical reasoning, coding abilities, dialogue generation, instruction following, and text-to-image generation—demonstrate that Flat-LoRA improves both in-domain and out-of-domain generalization. Code is available at [https://github.com/nblt/Flat-LoRA](https://github.com/nblt/Flat-LoRA).

###### Keywords: 

Machine Learning, ICML

^(†)^(†)affiliationnotice: Equal contribution

## 1 Introduction

Pre-training followed by fine-tuning has become the dominant paradigm in modern machine learning, achieving state-of-the-art performance by leveraging the versatile capabilities of pre-trained models ([Girshick et al., 2014](#bib.bib10); [Kolesnikov et al., 2020](#bib.bib21); [Radford et al., 2021](#bib.bib40); [Li et al., 2024c](#bib.bib33)). However, the enormous size of these models makes fine-tuning all parameters resource-intensive. Recently, Low-Rank Adaptation (LoRA) ([Hu et al., 2022](#bib.bib18)) has been proposed to address this challenge. LoRA fine-tunes only low-rank matrices, which can be merged with the pre-trained weights after training, incurring no extra overhead during inference. This approach significantly reduces trainable parameters, thereby lowering both training and storage requirements.

Figure 1: Illustration of LoRA optimization space. LoRA constrains optimization to a lower-dimensional space (blue). A flat minimum in LoRA space (blue curve) may exhibit sharp directions in the full parameter space (red curve).

Many methods have been proposed to enhance LoRA performance, such as adaptive rank allocation ([Zhang et al., 2023a](#bib.bib56)), decomposition of optimization into direction and magnitude ([Liu et al., 2024](#bib.bib36)), and improved initialization strategies ([Meng et al., 2024](#bib.bib37); [Wang et al., 2024](#bib.bib46)). Despite the promising potential these methods offer, the connection between the LoRA optimization space and the original full parameter space is often overlooked. Essentially, LoRA constrains optimization to a much lower-dimensional space, and its performance depends on how solutions in this restricted space relate to the full parameter space since the merged weights are ultimately used during inference. As illustrated in Figure [1](#S1.F1 "Figure 1 ‣ 1 Introduction ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape"), a flat minimum in the LoRA space may contain sharp directions in the view of the full parameter space, potentially leading to performance degradation. Figure [6](#S4.F6 "Figure 6 ‣ 4.7 Ablation Studies and Discussion ‣ 4 Experiments ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape") further demonstrates this phenomenon, revealing the sharpness of loss landscape for the minima found by LoRA when examined in the full parameter space.

![Refer to caption](2409.14396v2/fig/flat-lora.png)

Figure 2: Illustration of LoRA (Left) and Flat-LoRA (Right). By introducing designed random weight perturbations during fine-tuning, Flat-LoRA identifies a low-rank solution that is flat in the loss landscape of the full parameter space. Unlike SAM, it eliminates the need for additional gradient steps and remains memory-efficient by storing only the random seed and a small number of filter norms (less than $1/r$ of the LoRA parameters for rank $r$).

Flat minima in the loss landscape are widely believed to improve generalization and increase robustness to distribution shifts between training and test data ([Hochreiter & Schmidhuber, 1994](#bib.bib16); [Hochreiter & Schmidhuber, 1997](#bib.bib17)). This understanding has inspired Sharpness-Aware Minimization (SAM) ([Foret et al., 2020](#bib.bib9)), which is formulated as a min-max problem and has achieved state-of-the-art generalization. While integrating SAM with LoRA (referred to as LoRA-SAM ([Li et al., 2024a](#bib.bib26))) for large model fine-tuning is promising, there are several issues that should be discussed. First, LoRA-SAM can only optimize the sharpness of the loss landscape in a restricted space (Section [3.2](#S3.SS2 "3.2 LoRA with a Flat Landscape ‣ 3 Method ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")), which may not effectively improve generalization. Second, SAM requires an additional gradient step, doubling the training cost and rendering it impractical for large models. Lastly, computing sharpness in the full parameter space necessitates calculating gradients and storing perturbations for all weights, which contradicts the principles of parameter-efficient fine-tuning.

To address these challenges, we propose employing the Bayesian expectation loss objective ([Duchi et al., 2012](#bib.bib8); [Bisla et al., 2022](#bib.bib1)) to smooth the loss landscape, thereby achieving flat minima in the full parameter space. Our approach, termed Flat-LoRA, leverages efficient random weight perturbations that can be stored as random seeds. In contrast to SAM, which requires additional gradient steps and maintaining an extra copy of model weights, Flat-LoRA ensures both time and memory efficiency. Moreover, we introduce refined perturbation generation strategies that consider weight magnitude and model width scaling, resulting in improved generalization performance.

Our main contributions can be summarized as follows:

- •
  We find that low-rank adaptation may exhibit sharper loss landscapes in the full parameter space, prompting us to propose Flat-LoRA to mitigate this sharpness.
- •
  We employ Bayesian expected loss with designed random weight perturbations to pursue flat minima, seamlessly integrating with existing methods while maintaining computational and memory efficiency.
- •
  Extensive experiments across various natural language processing and computer vision tasks demonstrate that Flat-LoRA significantly improves both in-domain and out-of-domain generalization.

## 2 Related Work

### 2.1 Flat Minima and Generalization

The connection between the flatness of local minima and generalization has received much attention ([Hochreiter & Schmidhuber, 1997](#bib.bib17); [Chaudhari et al., 2017](#bib.bib2); [Keskar et al., 2017](#bib.bib20); [Dinh et al., 2017](#bib.bib7); [Izmailov et al., 2018](#bib.bib19); [Li et al., 2018b](#bib.bib28); [Wu et al., 2020](#bib.bib52); [Kwon et al., 2021](#bib.bib24); [Zhuang et al., 2022](#bib.bib62); [Li et al., 2024e](#bib.bib35)). Recently, many works have tried to improve generalization by seeking flat minima ([Tsuzuku et al., 2020](#bib.bib45); [Zheng et al., 2021](#bib.bib61); [Bisla et al., 2022](#bib.bib1)). For example, [Chaudhari et al. (2017)](#bib.bib2) propose Entropy-SGD to search for flat regions by minimizing local entropy. [Wen et al. (2018)](#bib.bib50) design SmoothOut framework to smooth out the sharp minima. Notably, Sharpness-Aware Minimization (SAM) ([Foret et al., 2020](#bib.bib9)) establishes a generic training scheme for seeking flat minima by formulating a min-max problem and encouraging parameters sitting in neighborhoods with uniformly low loss, achieving state-of-the-art generalization improvements across various tasks. However, SAM doubles the training time compared to regular training, limiting its applicability to large-scale training.

Another branch of methods for recovering flat minima involves minimizing the expected Bayesian training loss under random weight perturbation (RWP), which is efficient and doesn’t require additional gradient step ([Bisla et al., 2022](#bib.bib1)). [Wang & Mao (2021)](#bib.bib49) propose Gaussian model perturbation as a regularization scheme for improving SGD training, but it remains inefficient for multiple noise sampling. [Bisla et al. (2022)](#bib.bib1) connect the smoothness of loss objective to generalization and adopt filter-wise random Gaussian perturbation generation to recover flat minima and improve generalization. [Li et al. (2022c)](#bib.bib32); [Li et al. (2024d)](#bib.bib34) further enhances the generalization performance of RWP by introducing an adaptive perturbation generation strategy and a mixed loss objective. [Wu et al. (2022)](#bib.bib51); [Li et al. (2024b)](#bib.bib29) demonstrate that injecting small random noise before or during fine-tuning can improve generalization. However, when applying to parameter-efficient fine-tuning, we must be mindful of the additional memory costs they may introduce.

### 2.2 Low-rank Adaptation and Variants

Recent studies have shown that the intrinsic dimension required for optimizing deep neural networks (DNNs) can be significantly lower than the total number of parameters ([Li et al., 2018a](#bib.bib27); [Gur-Ari et al., 2018](#bib.bib11)). Notably, [Li et al. (2022a)](#bib.bib30) demonstrate the low-dimensional properties of DNN’s training dynamics, which has been leveraged to mitigate overfitting issues in adversarial training ([Li et al., 2022b](#bib.bib31)). Low-Rank Adaptation (LoRA) ([Hu et al., 2022](#bib.bib18)) is proposed to model the weight changes for each layer during fine-tuning. It effectively decreases the number of trainable parameters, thereby lowering the memory burden for training and storage. This approach is currently the mainstream because it avoids adding overhead during inference while demonstrating strong performance ([Wang et al., 2023](#bib.bib47)).

Many works have been proposed to enhance the performance of LoRA. AdaLoRA ([Zhang et al., 2023a](#bib.bib56)) dynamically prunes insignificant weights during fine-tuning through singular value decomposition (SVD), enabling allocating more rank to important areas under a fixed parameter budget. DoRA ([Liu et al., 2024](#bib.bib36)) improves optimization performance by decomposing weight updates into their direction and magnitude components. LoRA+ ([Hayou et al., 2024](#bib.bib13)) proposes to use different learning rates for the two matrices in LoRA to improve convergence. PiSSA ([Meng et al., 2024](#bib.bib37)) proposes to use the SVD decomposition of the original matrix $W$ to initialize the LoRA matrices, which provides a better initialization for LoRA parameters. LoRA-GA ([Wang et al., 2024](#bib.bib46)) proposes to align the gradient of LoRA to that of full fine-tuning at initialization. LoRA-Pro ([Wang & Liang, 2025](#bib.bib48)) further proposes to align each gradient step to the full fine-tuning. [Li et al. (2024a)](#bib.bib26) develop a resource-efficient SAM variant, called Balancedness-Aware Regularization (BAR), tailored for scale-invariant problems, such as LoRA optimization. In this paper, we improve LoRA by optimizing the sharpness of the loss landscape in the full parameter space, and our approach is orthogonal to previous works.

## 3 Method

In this section, we first briefly review Low-Rank Adaptation (LoRA). Then, we introduce our LoRA optimization objective that considers the landscape flatness of the full parameter space. Finally, we describe our random perturbation generation strategy for effectively improving generalization.

### 3.1 LoRA: Low-Rank Adaptation

Based on the finding that DNNs’ optimization happens in a subspace with a much smaller dimension than the number of parameters ([Li et al., 2018a](#bib.bib27); [Li et al., 2022a](#bib.bib30)), LoRA utilizes low-rank matrices to model the change for each layer’s weights $W \in {\mathbb{R}}^{m \times n}$ during fine-tuning as ${\Delta\hspace{0pt}W} = {B\hspace{0pt}A}$, where $B \in {\mathbb{R}}^{m \times r}$ and $A \in {\mathbb{R}}^{r \times n}$ with rank $r \ll {\min{\{{m,n}\}}}$ for parameter efficiency. We omit the scaling factor $s = {\alpha/r}$ here for simplicity, as it can be merged into $A$ and $B$. For the original output $h = {W\hspace{0pt}x}$, the modified forward pass is

|     |                                                                                                              |     |     |
|-----|--------------------------------------------------------------------------------------------------------------|-----|-----|
|     | ${h = {{W\hspace{0pt}x} + {\Delta\hspace{0pt}W\hspace{0pt}x}} = {{({W + {B\hspace{0pt}A}})}\hspace{0pt}x}}.$ |     | (1) |

At initialization, matrix $A$ is commonly initialized with Kaiming distribution ([He et al., 2015](#bib.bib14)) and matrix $B$ is set to zeros. During the training, only the low-rank matrices $A$ and $B$ are optimized with the pre-trained weight $W$ being frozen. During the inference, the low-rank matrices $\Delta\hspace{0pt}W$ are merged to the pre-trained weight $W$, and there are no additional computation or memory costs.

### 3.2 LoRA with a Flat Landscape

Despite recent efforts to improve LoRA performance, most studies focus solely on finding solutions performing well in the LoRA optimization space, specifically the rank-$r$ matrix space $\mathcal{M}_{r} = \left. \{{{\Delta\hspace{0pt}W} \in {\mathbb{R}}^{m \times n}} \middle| {{{rank}{({\Delta\hspace{0pt}W})}} \leq r}\} \right.$ (focusing on a single LoRA module). Following the well-established sharpness-aware minimization (SAM) objective ([Foret et al., 2020](#bib.bib9)), a natural approach is to apply SAM to LoRA parameters (LoRA-SAM) ([Li et al., 2024a](#bib.bib26)) with:

|     |                                                                                                                                                                                   |     |     |
|-----|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | ${\min\limits_{A,B}{\max\limits_{{\|{(\varepsilon_{A},\varepsilon_{B})}\|} \leq \rho}{L\left( {W + {{({B + \varepsilon_{B}})}\hspace{0pt}{({A + \varepsilon_{A}})}}} \right)}}},$ |     | (2) |

where $L{( \cdot )}$ denotes the loss objective for a specific task, ${\varepsilon_{B} \in {\mathbb{R}}^{m \times r}},{\varepsilon_{A} \in {\mathbb{R}}^{r \times n}}$ are the adversarial weight perturbations over low-rank matrices, $\|{(\varepsilon_{A},\varepsilon_{B})}\|$ denotes the total norm of weight perturbations (typically using the $\ell_{2}$-norm), and $\rho$ is the neighborhood radius.

However, focusing solely on the properties of the optimization space defined by LoRA parameters may have limitations. During inference, the low-rank adaptation $\Delta\hspace{0pt}W$ is merged into the pre-trained weights $W$. A solution that performs well within the LoRA space may be situated in a sharp region of the full parameter space, as illustrated in Figure [1](#S1.F1 "Figure 1 ‣ 1 Introduction ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape"), which could potentially harm overall generalization. To be more clear, employing first-order Taylor expansion for approximation to solve the inner maximum problem in Eqn. ([2](#S3.E2 "Equation 2 ‣ 3.2 LoRA with a Flat Landscape ‣ 3 Method ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")) ([Foret et al., 2020](#bib.bib9)), the equivalent weight perturbation applied to $W$ by Eqn. ([2](#S3.E2 "Equation 2 ‣ 3.2 LoRA with a Flat Landscape ‣ 3 Method ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")) is

|     |                                                                                                                                                      |     |     |     |
|-----|------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|-----|
|     | $\begin{array}{cl}                                                                                                                                   
       {\varepsilon_{W} = \phantom{}} & {{B\hspace{0pt}\varepsilon_{A}} + {\varepsilon_{B}\hspace{0pt}A} + {\varepsilon_{B}\hspace{0pt}\varepsilon_{A}}} \\  
        = & {c\left\lbrack {{B\hspace{0pt}B^{\top}\hspace{0pt}{({\nabla_{W}L})}} + {{({\nabla_{W}L})}\hspace{0pt}A^{\top}\hspace{0pt}A}} \right\rbrack} \\   
        & {{+ {c^{2}\hspace{0pt}{({\nabla_{W}L})}\hspace{0pt}A^{\top}\hspace{0pt}B^{\top}\hspace{0pt}{({\nabla_{W}L})}}},}                                   
       \end{array}$                                                                                                                                          |     |     | (3) |

where $\nabla_{W}L$ is the gradient w.r.t. full parameter weights $W$ and $c = {\rho/\sqrt{{\|{B^{\top}\hspace{0pt}{({\nabla_{W}L})}}\|}_{F}^{2} + {\|{{({\nabla_{W}L})}\hspace{0pt}A^{\top}}\|}_{F}^{2}}}$ is a scaling factor, with $\parallel \cdot \parallel {}_{F}$ denoting the Frobenius norm.

Notably, when $B$ is initialized as zero as defaulted in [Hu et al. (2022)](#bib.bib18), $B$ will remain small during the training ([Hao et al., 2024](#bib.bib12)) and Eqn. ([3](#S3.E3 "Equation 3 ‣ 3.2 LoRA with a Flat Landscape ‣ 3 Method ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")) roughly becomes:

|     |                                                                                      |     |     |
|-----|--------------------------------------------------------------------------------------|-----|-----|
|     | ${\varepsilon_{W} \approx {{c{({\nabla_{W}L})}}\hspace{0pt}A^{\top}\hspace{0pt}A}}.$ |     | (4) |

We also empirically validate this in Appendix [B](#A2 "Appendix B Validation on the Components of 𝜀_𝑊 ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape"). Eqn. ([4](#S3.E4 "Equation 4 ‣ 3.2 LoRA with a Flat Landscape ‣ 3 Method ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")) indicates that LoRA-SAM only optimizes sharpness within the column space spanned by $A$, which constitutes a small subspace of the full parameter space. As demonstrated in Table [6](#S4.T6 "Table 6 ‣ 4.7 Ablation Studies and Discussion ‣ 4 Experiments ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape"), applying SAM’s sharpness optimization exclusively to LoRA parameters compromises generalization improvements compared to applying it to the full parameter space.

Therefore, it is crucial to consider the loss landscape in the full parameter space and identify a low-rank adaptation that positions the merged weights in a flat region. To achieve this goal, we propose the following flat loss objective:

|     |                                                                                                                          |     |     |
|-----|--------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | ${\min\limits_{A,B}{\max\limits_{{\|\varepsilon_{W}\|}_{F} \leq \rho}{L{({W + {B\hspace{0pt}A} + \varepsilon_{W}})}}}},$ |     | (5) |

where $\varepsilon_{W} \in {\mathbb{R}}^{m \times n}$ is the adversarial perturbation over the full parameters. However, directly applying SAM to optimize the sharpness of the full weight space has several disadvantages: 1) it doubles the training cost, which is less desirable for large models, and 2) it requires storing an additional copy of weights for restoring perturbation, which contradicts the principle of parameter-efficient fine-tuning.

To achieve a flatter loss landscape while maintaining time and memory efficiency, we propose relaxing the maximization problem in Eq. ([5](#S3.E5 "Equation 5 ‣ 3.2 LoRA with a Flat Landscape ‣ 3 Method ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")) to an expectation, resulting in the following Bayesian expected loss objective:

|     |                                                                                                                                                                    |     |     |
|-----|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | ${\min\limits_{A,B}\mspace{21mu}{\mathbb{E}}_{{(\varepsilon_{W})}_{i,j} \sim {\mathcal{N}{(0,\sigma^{2})}}}\quad{L{({W + {B\hspace{0pt}A} + \varepsilon_{W}})}}},$ |     | (6) |

where $\sigma^{2}$ denotes the noise variance, which will be further discussed in Section [3.3](#S3.SS3 "3.3 Effective Random Perturbation Generation ‣ 3 Method ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape"). This expected loss smooths the loss function in the full parameter space, as shown in the following lemma, promoting convergence to flatter minima.

###### Lemma 3.1 ([Bisla et al.](#bib.bib1)).

Assume the loss function $L{(W)}$ is $\alpha$-Lipschitz continuous and $\beta$-smooth w.r.t. $W$ under $\ell_{2}$-norm. The smoothed function ${\mathbb{E}}_{{(\varepsilon_{W})}_{i,j} \sim {\mathcal{N}{(0,\sigma^{2})}}}\hspace{0pt}L\hspace{0pt}{({W + \varepsilon_{W}})}$ is $\min\left\{ {\frac{\alpha}{\sigma},\beta} \right\}$-smooth w.r.t. $W$.

To optimize Eqn. ([6](#S3.E6 "Equation 6 ‣ 3.2 LoRA with a Flat Landscape ‣ 3 Method ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")), we sample a noise matrix $\varepsilon_{W}$ for each optimization step and compute the perturbed gradient to optimize the low-rank matrices $A$ and $B$. Note that the noise perturbation, generated based on merged model weights, eliminates the need for additional gradient steps required by SAM. In practice, we recommend gradually increasing the perturbation strength to progressively recover flatter minima for better performance.

### 3.3 Effective Random Perturbation Generation

In this section, we introduce our approach for generating random weight perturbations aimed at optimizing sharpness and improving generalization. Let $W^{\prime} = {W + {B\hspace{0pt}A}}$ denote the merged weight matrix $W^{\prime} \in {\mathbb{R}}^{m \times n}$ for a linear layer with input dimension $n$ and output dimension $m$. Our design considers the following two key aspects:

- •
  Filter structure: We aim to generate the weight perturbation by filter ([Bisla et al., 2022](#bib.bib1)). There are $m$ filters $W^{\prime} = {(W_{1,:}^{\prime},W_{2,:}^{\prime},\cdots,W_{m,:}^{\prime})}$ that process the input $x \in {\mathbb{R}}^{n}$. Elements within a filter of a larger norm should receive a larger strength of perturbation.
- •
  Input dimension: To ensure that the variance introduced during the forward pass by random weight perturbation is independent of the input dimension, we scale the variance of noise added to each element by a factor of $1/n$, where $n$ is the input dimension.

Our random weight generation scheme is formulated as:

|     |                                                                                                                                 |     |     |
|-----|---------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | ${(\varepsilon_{W})}_{i,j} \sim \mathcal{N}\left( 0,\frac{\sigma^{2}}{n} \parallel W_{i,:}^{\prime} \parallel_{2}^{2} \right),$ |     | (7) |

where $\sigma$ is a hyper-parameter that controls the perturbation strength. Figure [2](#S1.F2 "Figure 2 ‣ 1 Introduction ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape") illustrates the comparison between LoRA and Flat-LoRA.

We then analyze the effects of introducing random weight perturbation on the activation. Given an input $x \in {\mathbb{R}}^{n}$, and under the hypothesis that $x$ is a random vector where each element has the same variance ${var}{\lbrack x_{i}\rbrack}$ and expectation ${\mathbb{E}}{\lbrack x_{i}\rbrack}$, we have:

|     |                                           |                                                                                     |     |     |
|-----|-------------------------------------------|-------------------------------------------------------------------------------------|-----|-----|
|     | ${var}{\lbrack W_{j,:}^{\prime}x\rbrack}$ | $= \parallel W_{j,:}^{\prime} \parallel_{2}^{2} \cdot {var}{\lbrack x_{i}\rbrack}.$ |     | (8) |

After injecting random weight perturbation $\varepsilon$, we have:

|     |     |                                                                                                                                                                                                                                                          |     |     |
|-----|-----|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     |     | ${var}\left\lbrack \left( W^{\prime} + \varepsilon_{W} \right)_{j,:}x \right\rbrack$                                                                                                                                                                     |     |     |
|     |     | $= \parallel W_{j,:}^{\prime} \parallel_{2}^{2} \cdot {var}{\lbrack x_{i}\rbrack} + \sum\limits_{i = 1}^{n}{var}\left\lbrack \varepsilon_{W_{j,i}}x_{i} \right\rbrack$                                                                                   |     |     |
|     |     | $= \parallel W_{j,:}^{\prime} \parallel_{2}^{2} \cdot {var}{\lbrack x_{i}\rbrack} + n \cdot \frac{\sigma^{2}}{n} \parallel W_{j,:}^{\prime} \parallel_{2}^{2} \cdot \left( {var}{\lbrack x_{i}\rbrack} + {\mathbb{E}}^{2}{\lbrack x_{i}\rbrack} \right)$ |     |     |
|     |     | $= {(1 + \sigma^{2})} \parallel W_{j,:}^{\prime} \parallel_{2}^{2} \cdot {var}{\lbrack x_{i}\rbrack} + \sigma^{2} \parallel W_{j,:}^{\prime} \parallel_{2}^{2} \cdot {\mathbb{E}}^{2}{\lbrack x_{i}\rbrack}.$                                            |     | (9) |

The injection of random weight perturbations $\varepsilon_{W}$ increases the forward activation variance by a factor of $1 + \sigma^{2}$, along with a bias term determined by ${\mathbb{E}}{\lbrack x_{i}\rbrack}$. This amplified variance facilitates escape from sharp local minima. By incorporating a scaling factor $1/n$ in the noise generation process, the variance increase becomes independent of input dimension $n$, as formalized in the following:

###### Proposition 3.2.

For input $x \in {\mathbb{R}}^{n}$ with identical variance and mean across elements, injecting random weight perturbations according to Eqn. ([7](#S3.E7 "Equation 7 ‣ 3.3 Effective Random Perturbation Generation ‣ 3 Method ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")) increases the output variance independently of the input dimension $n$.

Additionally, we note that this variance would not increase exponentially during the forward propagation of the network due to the existence of layer normalization.

| Method               | MNLI          | SST2          | CoLA          | QNLI          | MRPC          | Avg.  |
|----------------------|---------------|---------------|---------------|---------------|---------------|-------|
| Full FT              | 86.19_(±0.04) | 94.15_(±0.09) | 82.84_(±0.12) | 93.10_(±0.04) | 89.22_(±0.23) | 89.10 |
| LoRA ($r = 8$)       | 86.24_(±0.02) | 94.25_(±0.07) | 82.87_(±0.22) | 93.06_(±0.03) | 88.56_(±0.37) | 88.99 |
| Flat-LoRA ($r = 8$)  | 86.20_(±0.04) | 94.75_(±0.20) | 83.61_(±0.38) | 93.16_(±0.09) | 89.59_(±0.37) | 89.47 |
| LoRA ($r = 16$)      | 86.49_(±0.06) | 94.52_(±0.21) | 82.89_(±0.44) | 92.97_(±0.05) | 88.89_(±0.44) | 89.15 |
| Flat-LoRA ($r = 16$) | 86.51_(±0.01) | 94.84_(±0.02) | 84.08_(±0.31) | 93.28_(±0.03) | 89.83_(±0.34) | 89.72 |

Table 1: Results (%) on fine-tuning T5-base with a subset of GLUE datasets.

| Method               | CIFAR-10      | CIFAR-100     | Cars          | SVHN          | DTD           | Avg.  |
|----------------------|---------------|---------------|---------------|---------------|---------------|-------|
| Full FT              | 97.99_(±0.01) | 89.06_(±0.11) | 73.30_(±0.43) | 97.44_(±0.03) | 76.80_(±0.25) | 86.92 |
| LoRA ($r = 8$)       | 97.90_(±0.02) | 87.74_(±0.13) | 73.22_(±0.53) | 97.49_(±0.08) | 76.86_(±0.34) | 86.64 |
| Flat-LoRA ($r = 8$)  | 98.09_(±0.04) | 88.64_(±0.23) | 74.17_(±0.71) | 97.59_(±0.04) | 77.51_(±0.28) | 87.20 |
| LoRA ($r = 16$)      | 97.99_(±0.03) | 88.12_(±0.23) | 73.80_(±0.42) | 97.56_(±0.08) | 77.34_(±0.32) | 86.92 |
| Flat-LoRA ($r = 16$) | 98.21_(±0.04) | 89.27_(±0.07) | 74.89_(±0.52) | 97.71_(±0.10) | 78.24_(±0.44) | 87.66 |

Table 2: Results (%) on fine-tuning CLIP ViT-B/32 with image classification datasets.

Storing random seed for memory efficiency. Memory cost is crucial for parameter-efficient fine-tuning. Optimizing Eqn. ([6](#S3.E6 "Equation 6 ‣ 3.2 LoRA with a Flat Landscape ‣ 3 Method ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")) requires generating random perturbation $\varepsilon_{W}$ and computing gradient ${\nabla_{W}L}\hspace{0pt}{({W + {B\hspace{0pt}A} + \varepsilon_{W}})}$. While storing the full weight perturbation for large models would be prohibitive, it is sufficient to store only the seed for the random generator and filter norms $\left\{ \parallel W_{1,:}^{\prime} \parallel_{2}^{2}, \parallel W_{2,:}^{\prime} \parallel_{2}^{2},\cdots, \parallel W_{m,:}^{\prime} \parallel_{2}^{2} \right\}$. This allows for the reconstruction of $\varepsilon_{W}$ when needed. This approach requires minimal memory overhead (i.e., $\mathcal{O}{(m)}$), in contrast to SAM, which requires storing a full perturbation copy ($\mathcal{O}{({m \times n})}$) when optimizing sharpness in the full parameter space.

Simple approach for mixed precision training. Mixed-precision training, common in large-scale applications, enables memory-efficient integration of perturbation injection during precision casting. Since this training mode maintains both FP32 and FP/BF16 weight copies, we can inject perturbations during the half-precision auto-cast step before forward propagation, eliminating the need to store perturbations or filter norms. However, our primary approach—storing perturbations via filter norms and random seeds—remains more versatile as it functions independently of mixed-precision training.

## 4 Experiments

In this section, we evaluate the performance of Flat-LoRA on diverse tasks: natural language understanding, image classification, dialogue generation, mathematical reasoning, coding abilities, and text-to-image generation. We then demonstrate its enhanced out-of-domain generalization ability, followed by ablation studies and discussions. The code is provided in supplementary materials.

### 4.1 Natural Language Understanding

Setting. We fine-tune the T5-Base model on several datasets from the GLUE benchmark, including MNLI, SST, CoLA, QNLI, and MRPC, following ([Wang et al., 2024](#bib.bib46)). Performance is evaluated on the development set using accuracy as the primary metric. We use LoRA with rank 8 and LoRA alpha 16. We fine-tune the models with 10 epochs with a cosine learning rate schedule; except for MNLI and QNLI, we use 1 epoch. We use a learning rate of 0.0005 for LoRA fine-tuning and 0.0001 for full fine-tuning. The random perturbation strength $\sigma$ is set to 0.05 with a cosine-increasing strategy. Mean and standard deviations are calculated over 3 independent trials.

Results. As shown in Table [1](#S3.T1 "Table 1 ‣ 3.3 Effective Random Perturbation Generation ‣ 3 Method ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape"), Flat-LoRA consistently outperforms LoRA at ranks 8 and 16, achieving average performance gains of 0.48% and 0.57%, respectively. The improvements are particularly notable on smaller datasets, such as CoLA and MRPC, with gains of 1.19% and 0.94%, respectively, at rank 16. This is because smaller datasets are more prone to overfitting, and Flat-LoRA effectively mitigates this issue, leading to greater performance improvements compared to LoRA.

### 4.2 Image Classification

Setting. We fine-tune the CLIP ViT-B/32 model on five image classification tasks, including CIFAR-10/100 ([Krizhevsky & Hinton, 2009](#bib.bib23)), Cars ([Krause et al., 2013](#bib.bib22)), SVHN ([Netzer et al., 2011](#bib.bib38)), and DTD ([Cimpoi et al., 2014](#bib.bib5)). We resize all input images to a size of $\phantom{} \times 224$ and freeze the classification head. We experiment with LoRA using ranks of 8 and 16 and fine-tune the models with 10 epochs with a cosine annealing schedule. The learning rate is set to 0.0005 for LoRA and Flat-LoRA and 0.0001 for full fine-tuning, with a weight decay of 0.1. The perturbation strength $\sigma$ is set to 0.15 for Flat-LoRA with a cosine-increasing strategy. The mean and standard deviations are calculated over 3 independent trials.

Results. We measure the performance with classification accuracy and report the results in Table [2](#S3.T2 "Table 2 ‣ 3.3 Effective Random Perturbation Generation ‣ 3 Method ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape"). Again, we observe that Flat-LoRA significantly outperforms LoRA at both ranks 8 and 16, achieving averaged improvements of 0.56% and 0.74%, respectively. Notably, Flat-LoRA with rank 8 surpasses both LoRA with rank 16 and full fine-tuning by 0.28%. These results confirm the effectiveness of optimizing the loss landscape’s sharpness in the full parameter space.

### 4.3 Large Language Model

Setting. To evaluate the scalability of Flat-LoRA, we further conduct experiments on large language models. Specifically, we fine-tune Llama 2-7B ([Touvron et al., 2023](#bib.bib44)) on three tasks: chat, math, and code, following [Wang et al. (2024)](#bib.bib46). We use a learning rate of 5e-4 and employ a cosine learning rate scheduler with a warmup ratio of $0.03$. The LoRA rank is set to $8$ with LoRA alpha $16$, and the training epoch is set to $2$. The backbone uses BF16 precision, with the parameters of LoRA modules set to FP32 precision. For chat task, we fine-tune the model on WizardLM ([Xu et al., 2023](#bib.bib53)) and test on the MT-Bench dataset ([Zheng et al., 2023](#bib.bib59)). For math task, we fine-tune the model on MetaMathQA ([Yu et al., 2024](#bib.bib55)) and evaluate it on GSM8K evaluation set ([Cobbe et al., 2021](#bib.bib6)). For code task, we fine-tune the model on Code-Feedback ([Zheng et al., 2024](#bib.bib60)) and evaluate it on HumanEval ([Chen et al., 2021](#bib.bib3)). Training uses 52K for chat and 100K samples for math and code tasks. The random perturbation strength $\sigma$ is set to 0.05 with a cosine-increasing strategy.

Results. We measure the performance of the chat task by the first-turn score with GPT-4, the math task by accuracy, and the code task by PASS@1 metric. From the results in Table [3](#S4.T3 "Table 3 ‣ 4.3 Large Language Model ‣ 4 Experiments ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape"), we observe that Flat-LoRA significantly enhances LoRA’s performance, achieving an improvement of +0.20 on the MT-Bench dataset, +3.18% on the GSM8K dataset, and +3.08% on the Human-Eval dataset. Notably, these gains are substantially larger than those observed on smaller models, such as T5-base and CLIP ViT-B/32, highlighting the significance of pursuing flat minima for large-scale models. Moreover, the baselines we adopted are considerably stronger than those reported in previous works; for instance, we achieve 57.47% (ours) versus 42.08% ([Wang et al. (2024)](#bib.bib46)) for LoRA on the GSM8K dataset. Despite these stronger baselines, Flat-LoRA continues to deliver significant accuracy improvements over the standard LoRA, demonstrating its effectiveness in enhancing generalization.

| Method              | MT-Bench     | GSM8K         | Human-Eval    |
|---------------------|--------------|---------------|---------------|
| Full FT             | 5.30_(±0.11) | 59.36_(±0.85) | 35.31_(±2.13) |
| LoRA ($r = 8$)      | 5.96_(±0.03) | 57.47_(±0.45) | 24.85_(±0.52) |
| Flat-LoRA ($r = 8$) | 6.16_(±0.05) | 60.65_(±0.63) | 27.93_(±0.79) |

Table 3: Results on fine-tuning Llama 2-7B.

### 4.4 Text-to-Image Generation

Setting. We fine-tune the SDXL model ([Podell et al., 2023](#bib.bib39)) with the pipeline of Dreambooth ([Ruiz et al., 2023](#bib.bib42)) and the scripts implemented by HuggingFace. The finetuning dataset, 3D Icons¹¹ 1 [https://huggingface.co/datasets/linoyts/3d_icon](https://huggingface.co/datasets/linoyts/3d_icon), contains 23 training images, all of which have a square. We fine-tune the model for 500 steps with a constant learning rate of 0.0001. The batch size is set to 1. The LoRA rank and alpha are set to 4. The random perturbation strength $\sigma$ is set to 0.1 for Flat-LoRA. Other hyperparameters are set to default values.

Results. As shown in Figure [3](#S4.F3 "Figure 3 ‣ 4.4 Text-to-Image Generation ‣ 4 Experiments ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape"), Flat-LoRA exhibits better personalization than LoRA while maintaining better generation ability. For instance, in the second column, the image generated by Flat-LoRA includes a distinctive square behind the bird, aligning more closely with the “icon” feature present in the training images (top row). Furthermore, Flat-LoRA more effectively preserves the concept of eyes, whereas, in columns 1, 3, and 5, the birds generated by LoRA are missing eyes.

![Refer to caption](2409.14396v2/SD.png)

Figure 3: Images generated by SDXL fine-tuned with LoRA and Flat-LoRA on 3D icon datasets. Each column uses the *same* seeds for fair comparison.

### 4.5 Out-of-Domain Generalization

Flat minima have been shown to better accommodate distributional shifts between training and test data, thereby improving out-of-domain generalization. This property is particularly critical for pretrained vision and language models, which are designed for a wide range of applications. Below, we explore this property of Flat-LoRA in detail.

Corruption datasets. We focus on image classification tasks to evaluate the robustness of Flat-LoRA under data distribution shifts. Specifically, we fine-tune CLIP ViT-B/32 on CIFAR-100 and evaluate the model on corrupted CIFAR-100-C ([Hendrycks & Dietterich, 2019](#bib.bib15)). The results across varying levels of corruption severity are presented in Figure [4](#S4.F4 "Figure 4 ‣ 4.5 Out-of-Domain Generalization ‣ 4 Experiments ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape"). Flat-LoRA consistently outperforms LoRA, with performance gains increasing as corruption severity rises, from +1.38% at level 1 to +3.56% at level 5. These results demonstrate that the flatter minima identified by Flat-LoRA enhance out-of-domain generalization compared to LoRA.

Figure 4: Performance comparison of LoRA and Flat-LoRA across different corruption levels of CIFAR-100-C. The model is fine-tuned on CIFAR-100 with CLIP ViT-B/32.

Instruction following. We fine-tune the Llama 2-13B model on the Alpaca dataset ([Taori et al., 2023](#bib.bib43)), which simulates real-world variability and prepares the model handle unseen or shifted distributions at test time. The model is evaluated on InstructEval ([Chia et al., 2023](#bib.bib4)), an instruction-following benchmark, using the official code provided by [Chia et al. (2023)](#bib.bib4). The experimental setup follows [Ren et al. (2024)](#bib.bib41). From the results in Table [4](#S4.T4 "Table 4 ‣ 4.5 Out-of-Domain Generalization ‣ 4 Experiments ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape"), we observe that Flat-LoRA consistently outperforms LoRA. Notably, improvements on DROP and Human-Eval are more pronounced (+0.71% and +1.83%, respectively).

[TABLE]

Table 4: Results on instruct-following tasks. We fine-tune the Llama 2-13B model on the Alpaca datasets and evaluate the performance using the InstructEval metrics.

### 4.6 Integration with Other Methods

In this section, we compare Flat-LoRA with recently proposed LoRA variants, including PiSSA, LoRA-GA, DoRA, AdaLoRA, and LoRA+. Experiments are conducted on the CoLA and MRPC datasets using the T5-base model with LoRA rank 8. The results are presented in Table [5](#S4.T5 "Table 5 ‣ 4.6 Integration with Other Methods ‣ 4 Experiments ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape"). We observe that Flat-LoRA consistently outperforms previous methods on both datasets by 0.53% and 0.13%, respectively. Furthermore, the flat loss objective can be seamlessly integrated with the previous approaches to yield consistent improvements on both datasets by 0.91% and 0.93%, respectively. Note that these improvements are achieved at minimal additional cost, as shown in Table [7](#S4.T7 "Table 7 ‣ 4.7 Ablation Studies and Discussion ‣ 4 Experiments ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape"). This highlights the scalability of our approach and the effectiveness of considering the sharpness of the full parameter space.

|                                             |               |               |
|---------------------------------------------|---------------|---------------|
| Method                                      | Dataset       |               |
|                                             | CoLA          | MRPC          |
| Baseline Methods                            |               |               |
| LoRA ([Hu et al., 2022](#bib.bib18))        | 82.87_(±0.22) | 88.56_(±0.37) |
| PiSSA ([Meng et al., 2024](#bib.bib37))     | 83.18_(±0.24) | 88.96_(±0.44) |
| LoRA-GA ([Wang et al., 2024](#bib.bib46))   | 83.13_(±0.45) | 88.73_(±0.48) |
| DoRA ([Liu et al., 2024](#bib.bib36))       | 83.16_(±0.15) | 89.46_(±0.37) |
| AdaLoRA ([Zhang et al., 2023b](#bib.bib57)) | 82.58_(±0.56) | 88.79_(±0.33) |
| LoRA+ ([Hayou et al., 2024](#bib.bib13))    | 82.65_(±0.23) | 89.30_(±0.47) |
| Our Methods                                 |               |               |
| Flat-LoRA                                   | 83.61_(±0.38) | 89.59_(±0.37) |
| Flat-PiSSA                                  | 83.51_(±0.48) | 89.89_(±0.71) |
| Flat-LoRA-GA                                | 83.41_(±0.45) | 89.20_(±0.49) |
| Flat-DoRA                                   | 83.56_(±0.27) | 89.99_(±0.47) |
| Flat-AdaLoRA                                | 83.13_(±0.28) | 89.23_(±0.34) |
| Flat-LoRA+                                  | 83.56_(±0.46) | 89.61_(±0.44) |

Table 5: Comparison with other LoRA variants. The experiments are conducted on the GLUE subsets using the T5-Base model.

### 4.7 Ablation Studies and Discussion

| Method    | Flat Space | CoLA          | MRPC          | Additional Memory                       | Training time |
|-----------|------------|---------------|---------------|-----------------------------------------|---------------|
| LoRA      | \-         | 82.87_(±0.59) | 88.56_(±0.37) | \-                                      | 1$\times$     |
| LoRA+SAM  | $A,B$      | 83.31_(±0.48) | 88.98_(±0.22) | $\mathcal{O}{({{({m + n})} \times r})}$ | 2$\times$     |
| LoRA+SAM  | $W$        | 83.67_(±0.39) | 89.26_(±0.32) | $\mathcal{O}{({m \times n})}$           | 2$\times$     |
| Flat-LoRA | $A,B$      | 83.19_(±0.70) | 88.81_(±0.51) | $\mathcal{O}{({m + r})}$                | 1$\times$     |
| Flat-LoRA | $W$        | 83.61_(±0.38) | 89.59_(±0.37) | $\mathcal{O}{(m)}$                      | 1$\times$     |

Table 6: Comparison with SAM on the GLUE subsets using the T5-Base model.

(a) MRPC with T5-Base

(b) CIFAR-100 with ViT-B/32

Figure 5: Performance comparison across different LoRA ranks. Keeping the LoRA alpha fixed at 16, we vary the LoRA ranks among $\left\{ {1,4,16,64} \right\}$. The results are averaged over three independent trials.

Results under different LoRA ranks. Following the settings in Section [4.1](#S4.SS1 "4.1 Natural Language Understanding ‣ 4 Experiments ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape") and [4.2](#S4.SS2 "4.2 Image Classification ‣ 4 Experiments ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape"), we evaluate the performance of Flat-LoRA under different LoRA ranks. The results are shown in Figure [5](#S4.F5 "Figure 5 ‣ 4.7 Ablation Studies and Discussion ‣ 4 Experiments ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape"). We observe that Flat-LoRA consistently outperforms LoRA across different LoRA ranks by +1.10% on MRPC and +1.15% on CIFAR-100. Even at LoRA rank 1, which is typically underfitting, Flat-LoRA still delivers a significant performance boost over LoRA. This highlights the importance of considering the sharpness of the full parameter space. Additionally, as the LoRA rank increases, we observe that LoRA’s performance can degrade due to overfitting, particularly on MRPC, which is a small dataset with 3.7k data points. Flat-LoRA effectively mitigates this overfitting issue by identifying flatter minima that generalize better. Thus, we conclude that Flat-LoRA enhances LoRA fine-tuning performance not only in underfitting scenarios, where the rank is low and limited information from the full parameter space is explored, but also in high LoRA rank situations, where the risk of overfitting is more pronounced.

Comparison with SAM. We compare Flat-LoRA to SAM integrated with LoRA across different flat spaces: applying SAM’s sharpness optimization to the full parameter space ($W$) and to the LoRA parameters ($A,B$). Following the setup described in Section [4.1](#S4.SS1 "4.1 Natural Language Understanding ‣ 4 Experiments ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape"), we evaluate perturbation radii $\rho$ over $\{{0.001,0.003,0.005,0.01,0.05,0.1,0.2,0.5}\}$, finding that $\rho = 0.05$ yields optimal performance when applied to the full parameter space ($W$), while $\rho = 0.003$ is optimal for the LoRA parameters ($A,B$). From the results in Table [6](#S4.T6 "Table 6 ‣ 4.7 Ablation Studies and Discussion ‣ 4 Experiments ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape"), we observe that applying SAM to the full parameter space ($W$) consistently outperforms its application to the LoRA parameters ($A,B$), achieving improvements of +0.36% on CoLA and +0.28% on MRPC. However, SAM over $W$ incurs an additional memory overhead of $\mathcal{O}{({m \times n})}$ to store adversarial weight perturbations, rendering it impractical for parameter-efficient training. By contrast, Flat-LoRA achieves performance comparable to, or better than, SAM applied to $W$, while requiring only $\mathcal{O}{(m)}$ additional memory. Furthermore, Flat-LoRA preserves the training efficiency of vanilla LoRA (1$\times$), whereas SAM-based approaches double the training time (2$\times$) due to the need for additional gradient computations.

Memory and time costs. In Table [7](#S4.T7 "Table 7 ‣ 4.7 Ablation Studies and Discussion ‣ 4 Experiments ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape"), we report the memory and time usage for fine-tuning MetaMathQA datasets using the Llama 2-7B model. The training settings are the same with Section [4.3](#S4.SS3 "4.3 Large Language Model ‣ 4 Experiments ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape"), and we use a micro-batch size of 2, running on a NVIDIA GeForce RTX 4090 GPU. Flat-LoRA is implemented based on our default random seed approach. We observe that Flat-LoRA adds minimal overhead compared to LoRA - only 0.12GB extra memory and 11 minutes of training time. These results highlight that Flat-LoRA can be conveniently integrated into LoRA training with little additional overhead.

.

| Method    | Memory  | Training Time | GSM8K (%)     |
|-----------|---------|---------------|---------------|
| LoRA      | 23.49GB | 7h 22min      | 57.47_(±0.45) |
| Flat-LoRA | 23.61GB | 7h 33min      | 60.65_(±0.63) |

Table 7: Comparison of memory and time usage

Landscape visualization. In Figure [6](#S4.F6 "Figure 6 ‣ 4.7 Ablation Studies and Discussion ‣ 4 Experiments ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape"), we visualize the surfaces of the loss landscape for LoRA and Flat-LoRA at ranks 1 and 16. Following the technique proposed by [Li et al. (2018b)](#bib.bib28), we plot the loss surface along random “filter-normalized” directions in the full parameter space ($W$). For both LoRA and Flat-LoRA, the merged weights are used for visualization. The results demonstrate that Flat-LoRA consistently achieves a significantly flatter loss landscape compared to LoRA at both ranks. Notably, when the LoRA rank is lower, the corresponding loss landscape tends to be sharper, highlighting the importance of optimizing the sharpness in the full parameter space.

(a) LoRA ($r = 1$)

(b) Flat-LoRA ($r = 1$)

(c) LoRA ($r = 16$)

(d) Flat-LoRA ($r = 16$)

Figure 6: Loss landscape visualization in the full parameter space. The experiments are conducted on CIFAR-100 with CLIP ViT-B/32.

## 5 Conclusion

We present Flat-LoRA, an efficient low-rank adaptation method that optimizes the sharpness of the loss landscape in the full parameter space. Unlike conventional sharpness-aware minimization approaches that impose heavy computation and memory overhead, we employ the Bayesian expectation loss objective to pursue flat minima and design refined generation schemes for random weight perturbations while maintaining efficiency. Extensive experiments across neural language processing and computer vision demonstrate Flat-LoRA’s effectiveness in improving both in-domain and out-of-domain generalization.

## Impact Statement

This paper presents work whose goal is to advance the field of Machine Learning. There are many potential societal consequences of our work, none which we feel must be specifically highlighted here.

## Acknowledgment

This work was supported by National Key Research Development Project (2023YFF1104202) and National Natural Science Foundation of China (62376155).

## References

- Bisla et al. (2022) Bisla, D., Wang, J., and Choromanska, A. Low-pass filtering sgd for recovering flat optima in the deep learning optimization landscape. In *International Conference on Artificial Intelligence and Statistics*, pp. 8299–8339. PMLR, 2022.
- Chaudhari et al. (2017) Chaudhari, P., Choromanska, A., Soatto, S., LeCun, Y., Baldassi, C., Borgs, C., Chayes, J., Sagun, L., and Zecchina, R. Entropy-sgd: Biasing gradient descent into wide valleys. In *International Conference on Learning Representations (ICLR)*, 2017.
- Chen et al. (2021) Chen, M., Tworek, J., Jun, H., Yuan, Q., Pinto, H. P. D. O., Kaplan, J., Edwards, H., Burda, Y., Joseph, N., Brockman, G., et al. Evaluating large language models trained on code. *arXiv preprint arXiv:2107.03374*, 2021.
- Chia et al. (2023) Chia, Y. K., Hong, P., Bing, L., and Poria, S. Instructeval: Towards holistic evaluation of instruction-tuned large language models. *arXiv preprint arXiv:2306.04757*, 2023.
- Cimpoi et al. (2014) Cimpoi, M., Maji, S., Kokkinos, I., Mohamed, S., and Vedaldi, A. Describing textures in the wild. In *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 2014.
- Cobbe et al. (2021) Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun, H., Kaiser, L., Plappert, M., Tworek, J., Hilton, J., Nakano, R., et al. Training verifiers to solve math word problems. *arXiv preprint arXiv:2110.14168*, 2021.
- Dinh et al. (2017) Dinh, L., Pascanu, R., Bengio, S., and Bengio, Y. Sharp minima can generalize for deep nets. In *International Conference on Machine Learning (ICML)*, 2017.
- Duchi et al. (2012) Duchi, J. C., Bartlett, P. L., and Wainwright, M. J. Randomized smoothing for stochastic optimization. *SIAM Journal on Optimization*, 22(2):674–701, 2012.
- Foret et al. (2020) Foret, P., Kleiner, A., Mobahi, H., and Neyshabur, B. Sharpness-aware minimization for efficiently improving generalization. *arXiv preprint arXiv:2010.01412*, 2020.
- Girshick et al. (2014) Girshick, R., Donahue, J., Darrell, T., and Malik, J. Rich feature hierarchies for accurate object detection and semantic segmentation. In *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 2014.
- Gur-Ari et al. (2018) Gur-Ari, G., Roberts, D. A., and Dyer, E. Gradient descent happens in a tiny subspace. *arXiv preprint arXiv:1812.04754*, 2018.
- Hao et al. (2024) Hao, Y., Cao, Y., and Mou, L. Flora: Low-rank adapters are secretly gradient compressors. In *International Conference on Machine Learning (ICML)*, 2024.
- Hayou et al. (2024) Hayou, S., Ghosh, N., and Yu, B. Lora+: Efficient low rank adaptation of large models. In *International Conference on Machine Learning (ICML)*, 2024.
- He et al. (2015) He, K., Zhang, X., Ren, S., and Sun, J. Delving deep into rectifiers: Surpassing human-level performance on imagenet classification. In *Proceedings of the IEEE international conference on computer vision (ICCV)*, 2015.
- Hendrycks & Dietterich (2019) Hendrycks, D. and Dietterich, T. Benchmarking neural network robustness to common corruptions and perturbations. In *International Conference on Learning Representations (ICLR)*, 2019.
- Hochreiter & Schmidhuber (1994) Hochreiter, S. and Schmidhuber, J. Simplifying neural nets by discovering flat minima. In *Advances in Neural Information Processing Systems (NeurIPS)*, 1994.
- Hochreiter & Schmidhuber (1997) Hochreiter, S. and Schmidhuber, J. Flat minima. *Neural computation*, 1997.
- Hu et al. (2022) Hu, E. J., Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., Wang, L., Chen, W., et al. Lora: Low-rank adaptation of large language models. In *International Conference on Learning Representations (ICLR)*, 2022.
- Izmailov et al. (2018) Izmailov, P., Podoprikhin, D., Garipov, T., Vetrov, D., and Wilson, A. G. Averaging weights leads to wider optima and better generalization. *arXiv preprint arXiv:1803.05407*, 2018.
- Keskar et al. (2017) Keskar, N. S., Mudigere, D., Nocedal, J., Smelyanskiy, M., and Tang, P. T. P. On large-batch training for deep learning: Generalization gap and sharp minima. In *International Conference on Learning Representations (ICLR)*, 2017.
- Kolesnikov et al. (2020) Kolesnikov, A., Beyer, L., Zhai, X., Puigcerver, J., Yung, J., Gelly, S., and Houlsby, N. Big transfer (bit): General visual representation learning. In *European conference on computer vision (ECCV)*, 2020.
- Krause et al. (2013) Krause, J., Stark, M., Deng, J., and Fei-Fei, L. 3d object representations for fine-grained categorization. In *Proceedings of the IEEE international conference on computer vision workshops (ICCVW)*, 2013.
- Krizhevsky & Hinton (2009) Krizhevsky, A. and Hinton, G. Learning multiple layers of features from tiny images. *Technical Report*, 2009.
- Kwon et al. (2021) Kwon, J., Kim, J., Park, H., and Choi, I. K. Asam: Adaptive sharpness-aware minimization for scale-invariant learning of deep neural networks. In *International Conference on Machine Learning (ICML)*, 2021.
- Langley (2000) Langley, P. Crafting papers on machine learning. In Langley, P. (ed.), *Proceedings of the 17th International Conference on Machine Learning (ICML 2000)*, pp. 1207–1216, Stanford, CA, 2000. Morgan Kaufmann.
- Li et al. (2024a) Li, B., Zhang, L., and He, N. Implicit regularization of sharpness-aware minimization for scale-invariant problems. In *Advances in Neural Information Processing Systems (NeurIPS)*, 2024a.
- Li et al. (2018a) Li, C., Farkhoor, H., Liu, R., and Yosinski, J. Measuring the intrinsic dimension of objective landscapes. In *International Conference on Learning Representations (ICLR)*, 2018a.
- Li et al. (2018b) Li, H., Xu, Z., Taylor, G., Studer, C., and Goldstein, T. Visualizing the loss landscape of neural nets. In *Advances in Neural Information Processing Systems (NeurIPS)*, 2018b.
- Li et al. (2024b) Li, S., Yang, Y., Shen, Y., Wei, F., Lu, Z., Qiu, L., and Yang, Y. Lorasc: Expressive and generalizable low-rank adaptation for large models via slow cascaded learning. In *Findings of the Association for Computational Linguistics: EMNLP 2024*, pp. 12806–12816, 2024b.
- Li et al. (2022a) Li, T., Tan, L., Huang, Z., Tao, Q., Liu, Y., and Huang, X. Low dimensional trajectory hypothesis is true: Dnns can be trained in tiny subspaces. *IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI)*, 45(3):3411–3420, 2022a.
- Li et al. (2022b) Li, T., Wu, Y., Chen, S., Fang, K., and Huang, X. Subspace adversarial training. In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, 2022b.
- Li et al. (2022c) Li, T., Yan, W., Lei, Z., Wu, Y., Fang, K., Yang, M., and Huang, X. Efficient generalization improvement guided by random weight perturbation. *arXiv preprint arXiv:2211.11489*, 2022c.
- Li et al. (2024c) Li, T., Jiang, W., Liu, F., Huang, X., and Kwok, J. T. Learning scalable model soup on a single gpu: An efficient subspace training strategy. In *European conference on computer vision (ECCV)*, 2024c.
- Li et al. (2024d) Li, T., Tao, Q., Yan, W., Wu, Y., Lei, Z., Fang, K., He, M., and Huang, X. Revisiting random weight perturbation for efficiently improving generalization. *Transactions on Machine Learning Research (TMLR)*, 2024d. ISSN 2835-8856. URL [https://openreview.net/forum?id=WbbgOHpoPX](https://openreview.net/forum?id=WbbgOHpoPX).
- Li et al. (2024e) Li, T., Zhou, P., He, Z., Cheng, X., and Huang, X. Friendly sharpness-aware minimization. In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, 2024e.
- Liu et al. (2024) Liu, S.-y., Wang, C.-Y., Yin, H., Molchanov, P., Wang, Y.-C. F., Cheng, K.-T., and Chen, M.-H. Dora: Weight-decomposed low-rank adaptation. In *International Conference on Machine Learning (ICML)*, 2024.
- Meng et al. (2024) Meng, F., Wang, Z., and Zhang, M. Pissa: Principal singular values and singular vectors adaptation of large language models. In *Advances in Neural Information Processing Systems (NeurIPS)*, 2024.
- Netzer et al. (2011) Netzer, Y., Wang, T., Coates, A., Bissacco, A., Wu, B., Ng, A. Y., et al. Reading digits in natural images with unsupervised feature learning. In *NIPS workshop on deep learning and unsupervised feature learning*. Granada, 2011.
- Podell et al. (2023) Podell, D., English, Z., Lacey, K., Blattmann, A., Dockhorn, T., Müller, J., Penna, J., and Rombach, R. Sdxl: Improving latent diffusion models for high-resolution image synthesis. *arXiv preprint arXiv:2307.01952*, 2023.
- Radford et al. (2021) Radford, A., Kim, J. W., Hallacy, C., Ramesh, A., Goh, G., Agarwal, S., Sastry, G., Askell, A., Mishkin, P., Clark, J., et al. Learning transferable visual models from natural language supervision. In *International Conference on Machine Learning (ICML)*, 2021.
- Ren et al. (2024) Ren, P., Shi, C., Wu, S., Zhang, M., Ren, Z., de Rijke, M., Chen, Z., and Pei, J. Mini-ensemble low-rank adapters for parameter-efficient fine-tuning. *arXiv preprint arXiv:2402.17263*, 2024.
- Ruiz et al. (2023) Ruiz, N., Li, Y., Jampani, V., Pritch, Y., Rubinstein, M., and Aberman, K. Dreambooth: Fine tuning text-to-image diffusion models for subject-driven generation. In *Proceedings of the IEEE/CVF conference on computer vision and pattern recognition (CVPR)*, 2023.
- Taori et al. (2023) Taori, R., Gulrajani, I., Zhang, T., Dubois, Y., Li, X., Guestrin, C., Liang, P., and Hashimoto, T. B. Stanford alpaca: An instruction-following llama model, 2023.
- Touvron et al. (2023) Touvron, H., Martin, L., Stone, K., Albert, P., Almahairi, A., Babaei, Y., Bashlykov, N., Batra, S., Bhargava, P., Bhosale, S., et al. Llama 2: Open foundation and fine-tuned chat models. *arXiv preprint arXiv:2307.09288*, 2023.
- Tsuzuku et al. (2020) Tsuzuku, Y., Sato, I., and Sugiyama, M. Normalized flat minima: Exploring scale invariant definition of flat minima for neural networks using pac-bayesian analysis. In *International Conference on Machine Learning*, pp. 9636–9647. PMLR, 2020.
- Wang et al. (2024) Wang, S., Yu, L., and Li, J. Lora-ga: Low-rank adaptation with gradient approximation. In *Advances in Neural Information Processing Systems (NeurIPS)*, 2024.
- Wang et al. (2023) Wang, Y., Ivison, H., Dasigi, P., Hessel, J., Khot, T., Chandu, K., Wadden, D., MacMillan, K., Smith, N. A., Beltagy, I., et al. How far can camels go? exploring the state of instruction tuning on open resources. In *Advances in Neural Information Processing Systems (NeurIPS)*, 2023.
- Wang & Liang (2025) Wang, Z. and Liang, J. Lora-pro: Are low-rank adapters properly optimized? In *International Conference on Learning Representations (ICLR)*, 2025.
- Wang & Mao (2021) Wang, Z. and Mao, Y. On the generalization of models trained with sgd: Information-theoretic bounds and implications. In *International Conference on Learning Representations (ICLR)*, 2021.
- Wen et al. (2018) Wen, W., Wang, Y., Yan, F., Xu, C., Wu, C., Chen, Y., and Li, H. Smoothout: Smoothing out sharp minima to improve generalization in deep learning. *arXiv preprint arXiv:1805.07898*, 2018.
- Wu et al. (2022) Wu, C., Wu, F., Qi, T., and Huang, Y. Noisytune: A little noise can help you finetune pretrained language models better. In *Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)*, pp. 680–685, 2022.
- Wu et al. (2020) Wu, D., Xia, S.-T., and Wang, Y. Adversarial weight perturbation helps robust generalization. In *Advances in Neural Information Processing Systems (NeurIPS)*, 2020.
- Xu et al. (2023) Xu, C., Sun, Q., Zheng, K., Geng, X., Zhao, P., Feng, J., Tao, C., and Jiang, D. Wizardlm: Empowering large language models to follow complex instructions. *arXiv preprint arXiv:2304.12244*, 2023.
- Yang et al. (2024) Yang, Y., Li, X., Zhou, Z., Song, S., Wu, J., Nie, L., and Ghanem, B. Corda: Context-oriented decomposition adaptation of large language models for task-aware parameter-efficient fine-tuning. In *Advances in Neural Information Processing Systems (NeurIPS)*, 2024.
- Yu et al. (2024) Yu, L., Jiang, W., Shi, H., Yu, J., Liu, Z., Zhang, Y., Kwok, J. T., Li, Z., Weller, A., and Liu, W. Metamath: Bootstrap your own mathematical questions for large language models. In *International Conference on Learning Representations (ICLR)*, 2024.
- Zhang et al. (2023a) Zhang, Q., Chen, M., Bukharin, A., He, P., Cheng, Y., Chen, W., and Zhao, T. Adaptive budget allocation for parameter-efficient fine-tuning. In *International Conference on Learning Representations (ICLR)*, 2023a.
- Zhang et al. (2023b) Zhang, Q., Chen, M., Bukharin, A., Karampatziakis, N., He, P., Cheng, Y., Chen, W., and Zhao, T. Adalora: Adaptive budget allocation for parameter-efficient fine-tuning. In *International Conference on Learning Representations (ICLR)*, 2023b.
- Zhao et al. (2024) Zhao, J., Zhang, Z., Chen, B., Wang, Z., Anandkumar, A., and Tian, Y. Galore: Memory-efficient llm training by gradient low-rank projection. In *International Conference on Machine Learning (ICML)*, 2024.
- Zheng et al. (2023) Zheng, L., Chiang, W.-L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y., Lin, Z., Li, Z., Li, D., Xing, E., et al. Judging llm-as-a-judge with mt-bench and chatbot arena. In *Advances in Neural Information Processing Systems (NeurIPS)*, 2023.
- Zheng et al. (2024) Zheng, T., Zhang, G., Shen, T., Liu, X., Lin, B. Y., Fu, J., Chen, W., and Yue, X. Opencodeinterpreter: Integrating code generation with execution and refinement. In *Findings of the Association for Computational Linguistics ACL*, 2024.
- Zheng et al. (2021) Zheng, Y., Zhang, R., and Mao, Y. Regularizing neural networks via adversarial model perturbation. In *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 2021.
- Zhuang et al. (2022) Zhuang, J., Gong, B., Yuan, L., Cui, Y., Adam, H., Dvornek, N., Tatikonda, S., Duncan, J., and Liu, T. Surrogate gap minimization improves sharpness-aware training. In *International Conference on Learning Representations (ICLR)*, 2022.

## Appendix A Training-vs-Test Loss and Generalization Gap Curves

We plot the training-vs-test loss curves and generalization gap on CIFAR-100 and MRPC datasets in Figure [A1](#A1.F1 "Figure A1 ‣ Appendix A Training-vs-Test Loss and Generalization Gap Curves ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape"). The results show Flat-LoRA exhibits slightly higher training loss than LoRA, with a smaller generalization gap between training and test accuracies. Thus, we can conclude that the gains of Flat-LoRA are not due to lower training loss but due to better optimization that confers better generalization.

![Refer to caption](2409.14396v2/fig/cifar_100_loss.png)

(a) Training/test loss curves on CIFAR-100.

![Refer to caption](2409.14396v2/fig/cifar_100_acc_gap.png)

(b) Generalization gap curves on CIFAR-100.

![Refer to caption](2409.14396v2/fig/mrpc_loss.png)

(c) Training/test loss curves on MRPC.

![Refer to caption](2409.14396v2/fig/mrpc_acc_gap.png)

(d) Generalization gap curves on MRPC.

Figure A1: Training-vs-test loss and generalization gap curves comparison. Flat-LoRA exhibits slightly higher training loss than LoRA, with a smaller generalization gap between training and test accuracies.

## Appendix B Validation on the Components of $\varepsilon_{W}$

In this section, we validate the approximation of Eqn. ([4](#S3.E4 "Equation 4 ‣ 3.2 LoRA with a Flat Landscape ‣ 3 Method ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")), i.e., $\varepsilon_{W} \approx {\varepsilon_{B}\hspace{0pt}A} = {{c{({\nabla_{W}L})}}\hspace{0pt}A^{\top}\hspace{0pt}A}$. We conduct an experiment on the MRPC dataset with T5-base model and record the statistics of $\frac{\|{\varepsilon_{B}\hspace{0pt}A}\|}{\|\varepsilon_{W}\|}$ during the training. The results are shown in Figure [A2](#A2.F2 "Figure A2 ‣ Appendix B Validation on the Components of 𝜀_𝑊 ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape"). We observe that $\frac{\|{\varepsilon_{B}\hspace{0pt}A}\|}{\|\varepsilon_{W}\|} > 0.95$ throughout the training. This validates the approximation of Eqn. ([4](#S3.E4 "Equation 4 ‣ 3.2 LoRA with a Flat Landscape ‣ 3 Method ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape")).

![Refer to caption](2409.14396v2/fig/ratio.png)

Figure A2: Statistics of $\frac{{\|{\varepsilon_{B}\hspace{0pt}A}\|}_{2}}{{\|\varepsilon_{W}\|}_{2}}$. We observe that $\frac{{\|{\varepsilon_{B}\hspace{0pt}A}\|}_{2}}{{\|\varepsilon_{W}\|}_{2}}$ remains almost above 0.95 throughout training, indicating that the actual weight perturbation of LoRA-SAM $\varepsilon_{W}$ is almost determined by $\varepsilon_{B}\hspace{0pt}A$. This indicates that LoRA-SAM primarily optimizes the sharpness within the subspace spanned by $A$. The experiment is conducted on the MRPC dataset with the T5-base model.

## Appendix C Extending Perturbation to All Layers

We extend the injection of random weight perturbation to all layers, referred to as “Flat-LoRA (all)”. Specifically, we additionally add perturbations to layernorm layers, biases, class embeddings, etc. We generate noise based on the absolute weight $|W|$. From the results in Table [A1](#A3.T1 "Table A1 ‣ Appendix C Extending Perturbation to All Layers ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape"), we observe that Flat-LoRA (all) indeed improves performance, though the improvement is not as large as Flat-LoRA (Linear) over LoRA.

| Method             | CIFAR-10                  | CIFAR-100                 |
|--------------------|---------------------------|---------------------------|
| LoRA               | 97.90_(±0.02)             | 87.74_(±0.13)             |
| Flat-LoRA (linear) | 98.09_(±0.04)             | 88.64_(±0.23)             |
| Flat-LoRA (all)    | $\text{98.13}_{\pm 0.03}$ | $\text{88.76}_{\pm 0.19}$ |

Table A1: Results on CIFAR-10/100 with CLIP ViT-B/32.

## Appendix D Ablation on the Variance Magnitude

To evaluate the impact of the perturbation variance magnitude $\sigma$ for Flat-LoRA, we vary $\sigma$ among $\{{0,0.01,0.05,0.10,0.15,0.20}\}$ and fine-tune CIFAR-100 on CLIP ViT-B/32 and ViT-L/14 as well as GSM8k on Llama 2-7B and Llama 2-13B. From the results in Table [A2](#A4.T2 "Table A2 ‣ Appendix D Ablation on the Variance Magnitude ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape") and Table [A3](#A4.T3 "Table A3 ‣ Appendix D Ablation on the Variance Magnitude ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape"), we observe that the optimal results are achieved when $\sigma$ is 0.05 or 0.10 for both datasets and different network sizes. Hence, we suggest $\sigma = {0.05/0.10}$ for practice usage.

| $\sigma$ | 0             | 0.01          | 0.05          | 0.10          | 0.15          | 0.20          |
|----------|---------------|---------------|---------------|---------------|---------------|---------------|
| ViT-B/32 | 87.74_(±0.13) | 88.14_(±0.22) | 88.37_(±0.41) | 88.65_(±0.35) | 88.64_(±0.23) | 88.06_(±0.31) |
| ViT-L/14 | 92.13_(±0.17) | 92.33_(±0.07) | 92.63_(±0.11) | 93.11_(±0.13) | 92.98_(±0.21) | 92.46_(±0.03) |

Table A2: Results on CIFAR-100 with different variance magnitude.

| $\sigma$    | 0             | 0.01          | 0.05          | 0.10          | 0.15          | 0.20          |
|-------------|---------------|---------------|---------------|---------------|---------------|---------------|
| LLama 2-7B  | 57.47_(±0.45) | 58.35_(±0.42) | 60.65_(±0.63) | 60.56_(±0.48) | 60.08_(±0.76) | 58.50_(±0.85) |
| LLama 2-13B | 66.76_(±0.23) | 67.02_(±0.67) | 67.75_(±0.70) | 68.11_(±0.53) | 67.66_(±0.97) | 67.34_(±1.17) |

Table A3: Results on GSM8k with different variance magnitude.

## Appendix E More Comparisons to LoRA’s Varints

In Table [A4](#A5.T4 "Table A4 ‣ Appendix E More Comparisons to LoRA’s Varints ‣ Flat-LoRA: Low-Rank Adaptation over a Flat Loss Landscape"), we compare Flat-LoRA with more recently proposed LoRA varints, including oBAR/nBAR  ([Li et al., 2024a](#bib.bib26)), LoRA-Pro ([Wang & Liang, 2025](#bib.bib48)), GaLore ([Zhao et al., 2024](#bib.bib58)), and CorDA ([Yang et al., 2024](#bib.bib54)). The experiments are conducted on the T5-base model with MRPC and CoLA datasets. We can observe that Flat-LoRA achieves competitive or better performance than those state-of-the-art variants.

| Methods                                     | MRPC          | CoLA          |
|---------------------------------------------|---------------|---------------|
| oBAR ([Li et al., 2024a](#bib.bib26))       | 88.58_(±0.35) | 83.07_(±0.87) |
| nBAR ([Li et al., 2024a](#bib.bib26))       | 88.63_(±0.42) | 82.78_(±0.68) |
| LoRA-Pro ([Wang & Liang, 2025](#bib.bib48)) | 89.23_(±0.33) | 83.17_(±0.28) |
| GaLore ([Zhao et al., 2024](#bib.bib58))    | 88.90_(±1.12) | 83.14_(±0.57) |
| CorDA ([Yang et al., 2024](#bib.bib54))     | 89.76_(±0.52) | 83.38_(±0.47) |
| Flat-LoRA (Ours)                            | 89.59_(±0.37) | 83.61_(±0.38) |

Table A4: Performance comparison on MRPC and CoLA.

[25](#bib.bib25)

Experimental support, please [view the build logs](./2409.14396v2/__stdout.txt) for errors. Generated by [ L A T E xml ![\[LOGO\]](img)](https://math.nist.gov/~BMiller/LaTeXML/) .

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
