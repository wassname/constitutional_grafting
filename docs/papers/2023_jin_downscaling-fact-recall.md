---
title: "The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning"
authors: "Tian Jin et al."
year: 2023
source: https://arxiv.org/html/2310.04680
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

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) [![](img) Report Issue](# "Report an Issue") [![](img) Back to Abstract](/abs/2310.04680v1 "Back to abstract page") [![](img) Download PDF](/pdf/2310.04680v1 "Download PDF") [![](img)](javascript:toggleNavTOC(); "Toggle navigation") [![](img)](javascript:toggleReadingMode(); "Disable reading mode, show header and footer")

![](img) ![](img) ![](img)

1.  [Abstract](#abstract1 "In The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
2.  [1 Introduction](#S1 "In The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
3.  [2 Related Work](#S2 "In The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
4.  [3 Preliminaries](#S3 "In The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
    1.  [3.1 Evaluation](#S3.SS1 "In 3 Preliminaries ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
5.  [4 Effect of Pruning on Question Answering Tasks](#S4 "In The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
6.  [5 More Sophisticated In-context Learning](#S5 "In The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
7.  [6 Dense Scaling](#S6 "In The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
8.  [7 Pruning Attention and Feed Forward Layers](#S7 "In The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
9.  [8 Closing Discussion](#S8 "In The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
10. [References](#bib "In The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
11. [A Limitation.](#A1 "In The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
12. [B Pruning Perplexity Eval](#A2 "In The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
13. [C Constructing Parameterized Functions in ICL Evaluation](#A3 "In The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
14. [D Additional Details for ICL Evaluation Methodology](#A4 "In The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
    1.  [In-context example label distribution.](#A4.SS0.SSS0.Px1 "In Appendix D Additional Details for ICL Evaluation Methodology ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
    2.  [Evaluation label distribution.](#A4.SS0.SSS0.Px2 "In Appendix D Additional Details for ICL Evaluation Methodology ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
    3.  [Size of evaluation dataset.](#A4.SS0.SSS0.Px3 "In Appendix D Additional Details for ICL Evaluation Methodology ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
    4.  [Prompting technique.](#A4.SS0.SSS0.Px4 "In Appendix D Additional Details for ICL Evaluation Methodology ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
    5.  [Tokenizer.](#A4.SS0.SSS0.Px5 "In Appendix D Additional Details for ICL Evaluation Methodology ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
15. [E Increasing Input Dimension of ICL Evaluation](#A5 "In The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
    1.  [Method.](#A5.SS0.SSS0.Px1 "In Appendix E Increasing Input Dimension of ICL Evaluation ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
    2.  [Results.](#A5.SS0.SSS0.Px2 "In Appendix E Increasing Input Dimension of ICL Evaluation ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
    3.  [Conclusion.](#A5.SS0.SSS0.Px3 "In Appendix E Increasing Input Dimension of ICL Evaluation ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
16. [F Additional Pruning Algorithm Evaluation](#A6 "In The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
    1.  [Method.](#A6.SS0.SSS0.Px1 "In Appendix F Additional Pruning Algorithm Evaluation ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
    2.  [Results.](#A6.SS0.SSS0.Px2 "In Appendix F Additional Pruning Algorithm Evaluation ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
    3.  [Conclusion.](#A6.SS0.SSS0.Px3 "In Appendix F Additional Pruning Algorithm Evaluation ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
17. [G Pythia Models Evaluation](#A7 "In The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
    1.  [Method.](#A7.SS0.SSS0.Px1 "In Appendix G Pythia Models Evaluation ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
    2.  [Results.](#A7.SS0.SSS0.Px2 "In Appendix G Pythia Models Evaluation ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
    3.  [Conclusion.](#A7.SS0.SSS0.Px3 "In Appendix G Pythia Models Evaluation ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
18. [H Example Prompts](#A8 "In The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
    1.  [H.1 Question-answering without context.](#A8.SS1 "In Appendix H Example Prompts ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
    2.  [H.2 Question-answering with context.](#A8.SS2 "In Appendix H Example Prompts ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
    3.  [H.3 ICL on algorithmic task.](#A8.SS3 "In Appendix H Example Prompts ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
19. [I Analysis on Accuracy Improvement](#A9 "In The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
    1.  [Method.](#A9.SS0.SSS0.Px1 "In Appendix I Analysis on Accuracy Improvement ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
    2.  [Results.](#A9.SS0.SSS0.Px2 "In Appendix I Analysis on Accuracy Improvement ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
    3.  [Conclusion.](#A9.SS0.SSS0.Px3 "In Appendix I Analysis on Accuracy Improvement ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
20. [J Details on Computing Software/Hardware](#A10 "In The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
21. [K Characterizing Errors from Numerical Precision](#A11 "In The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
    1.  [Perplexity and accuracy results.](#A11.SS0.SSS0.Px1 "In Appendix K Characterizing Errors from Numerical Precision ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")
    2.  [OPT.](#A11.SS0.SSS0.Px2 "In Appendix K Characterizing Errors from Numerical Precision ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")

[License: CC BY 4.0](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2310.04680v1 \[cs.CL\] 07 Oct 2023

# The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning

Tian Jin ^(†)^(†)thanks: These authors contribute equally to this work. Affiliation: MIT CSAIL Email: [tianjin@csail.mit.edu](mailto:)    Nolan Clement¹¹footnotemark: 1 Affiliation: MIT Email: [nolangc@mit.edu](mailto:)    Xin Dong¹¹footnotemark: 1 Affiliation: Harvard University Email: [xindong@g.harvard.edu](mailto:)    Vaishnavh Nagarajan Affiliation: Google Research Email: [vaishnavh@google.com](mailto:)    Michael Carbin Affiliation: MIT CSAIL Email: [mcarbin@csail.mit.edu](mailto:)    Jonathan Ragan-Kelley Affiliation: MIT CSAIL Email: [jrk@mit.edu](mailto:)    Gintare Karolina Dziugaite Affiliation: Google DeepMind Email: [gkdz@google.com](mailto:)

###### Abstract

How does scaling the number of parameters in large language models (LLMs) affect their core capabilities? We study two natural scaling techniques — weight pruning and simply training a smaller or larger model, which we refer to as dense scaling — and their effects on two core capabilities of LLMs: (a) recalling facts presented during pre-training and (b) processing information presented in-context during inference. By curating a suite of tasks that help disentangle these two capabilities, we find a striking difference in how these two abilities evolve due to scaling. Reducing the model size by more than 30% (via either scaling approach) significantly decreases the ability to recall facts seen in pre-training. Yet, a 60–70% reduction largely preserves the various ways the model can process in-context information, ranging from retrieving answers from a long context to learning parameterized functions from in-context exemplars. The fact that both dense scaling and weight pruning exhibit this behavior suggests that scaling model size has an inherently disparate effect on fact recall and in-context learning.

|     |
|-----|
|     |

## 1 Introduction

Scaling up the size of LLMs is known to yield impressive performance gains on various tasks ([Kaplan et al., 2020a](#bib.bib36); [Hoffmann et al., 2022b](#bib.bib29); [Brown et al., 2020b](#bib.bib8); [Wei et al., 2022](#bib.bib61)). On the other hand, to deploy language models sustainably, it is also critical to scale them down while preserving their end utility. Naturally, scaling, in both directions, has gained interest in a recent wave of research on language models ([Kaplan et al. (2020a)](#bib.bib36); [Hoffmann et al. (2022b)](#bib.bib29); [Frantar & Alistarh (2023)](#bib.bib21); [Jiang et al. (2022)](#bib.bib33); [Kurtic et al. (2023)](#bib.bib38); [Santacroce et al. (2023)](#bib.bib54)). Much of this work evaluates size–performance tradeoffs of scaling through aggregate performance metrics such as perplexity or downstream accuracy on existing benchmarks.

However, we argue that there must exist subtle but important effects of scaling that cannot be captured by standard metrics alone. Indeed, work on image classification already hints at this. Pruning image models, for example, can introduce biases ([Hooker et al., 2019](#bib.bib30)) or disproportionate effects on certain subsets of the data ([Jin et al., 2022](#bib.bib34)) — these are effects that simply do not reflect in the overall accuracy of the model. Taking inspiration from this, our goal is to identify the subtler effects of scaling (up or down) LLMs in terms of the various capabilities that underpin their success in practice.

Figure 1: Pruning to moderate sparsity ($\phantom{} > {30\%}$ sparse) harms fact recall while in-context learning withstands even aggressive pruning (60% sparse). We plot the accuracy versus sparsity for the OPT-13B, OPT-30B, LLaMA-13B, and LLaMA-33B models on TriviaQA dataset for fact recall evaluation (left) and linear classification dataset for ICL evaluation (right). We plot their average performance in red. We color the range of sparsity where accuracy drop is within (relative) 5% of the dense model. Accepting (relative) 5% accuracy drop w.r.t. the dense model, the maximum sparsity on fact recall task is 30%, whereas the maximum sparsity on ICL task is 60%.

Our approach. In this work, we study the effects of scaling the number of parameters in an LLM on two fundamentally dichotomous capabilities as put forth by [Chan et al. (2022b)](#bib.bib11); [Chan et al. (2022a)](#bib.bib10): the ability to process information stored in weights (such as facts seen during pre-training) and the ability to process information stored in context (such as hints given in the context). It is, however, challenging to isolate how well a model has learned these abilities by simply measuring performance on an arbitrary downstream task — after all, most tasks require both abilities to varying extents to succeed. Instead, we carefully curate a set of downstream tasks that help tease apart the performance of any given model on the two abilities (as explained shortly). We then evaluate model performance in terms of these two abilities under two fundamentally different types of scaling: pruning and dense scaling. For the former, we consider recent scalable pruning methods that prune and update the remaining weights in one-shot ([Frantar & Alistarh, 2023](#bib.bib21); [Sun et al., 2023](#bib.bib56)); for the latter, we use (separately-trained) dense models with increased/reduced width and depth.

Our curated suite of benchmarks involve four classes of tasks, defining a gradation of reliance on information stored in-weights and in-context. The first three are Q&A tasks: (1) a closed book Q&A that necessarily requires fact recall from pre-training for which the model needs to process information from the weights, (2) an open book Q&A for which it suffices to copy information from the context and (3) an overriding Q&A, where the information provided in-context overrides facts seen during pre-training ([Li et al., 2022](#bib.bib41); [Longpre et al., 2021](#bib.bib46)). Finally, to evaluate more sophisticated context-processing abilities, we consider testing the model on its ability to (4) learn parameterized functions (e.g., linear classifiers) using input–output pairs presented in-context. Overall, we consider open-book, overriding Q&A and learning tasks as tasks that require increasing levels of in-context learning (ICL) abilities (See [Section 3.1](#S3.SS1 "3.1 Evaluation ‣ 3 Preliminaries ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning") for more discussion). We summarize these tasks in Table [1](#S1.T1 "Table 1 ‣ 1 Introduction ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning").

Fact recall results. Prior pruning literature demonstrates significant down-scaling without noticeable change to accuracy: pioneering work ([Dong et al., 2017b](#bib.bib18)) removes $\phantom{} \sim {45\%}$ of the weights in a ResNet50 model without noticeable accuracy degradation. ¹¹ 1 Please refer to Section 4.1, Figure 2.(a) of [Dong et al. (2017b)](#bib.bib18). Notably, [Dong et al. (2017b)](#bib.bib18) obtained these results similarly by pruning without retraining. However, when examining the effect of pruning on the ability to recall facts, we find a much different story: removing more than 30% of weights leads to significant ($\phantom{} > {5\%}$, relative) accuracy degradation on fact recall related tasks ([Figure 1](#S1.F1 "In 1 Introduction ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning"), left). Fact recall shows the same striking sensitivity to dense scaling.

In-context learning results. The seminal work of [Brown et al. (2020a)](#bib.bib7) hypothesized that scaling up the number of parameters strongly benefits the ICL ability of LLMs.²² 2 “Since in-context learning involves absorbing many skills and tasks within the parameters of the model, it is plausible that in-context learning abilities might show similarly strong gains with scale.” ([Brown et al., 2020a](#bib.bib7)) However, our evaluations on the suite of tasks that require a gradation of ICL abilities (with little to no reliance on fact recall) demonstrate the opposite: substantial down-scaling still preserves LLM’s ICL ability. Specifically, even after pruning 60% of weights, the relative accuracy decrease on ICL tasks is less than 5% ([Figure 1](#S1.F1 "In 1 Introduction ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning"), right). ICL shows a similar insensitivity to dense scaling.

Implications. Our work reveals the disparate effects of scaling on fact recall and in-context learning (ICL), which notably holds for two substantially different types of scaling: pruning and dense scaling. This motivates several lines of future work:

*Improve inference efficiency.* Our work reveals that scaling down model size alone has little impact on tasks demanding processing information in the LLM’s context. Practitioners may thus use our findings to identify scenarios where decisions could be routed to a smaller model instead of a larger one without hurting task performance ([Chen et al., 2023](#bib.bib12); [Dohan et al., 2022](#bib.bib16)).

*Improve LLM systems.* Our work shows the utility of feeding external supportive information, like documents from similarity search ([Borgeaud et al., 2022](#bib.bib6); [Guu et al., 2020](#bib.bib25)), in question–answering tasks to improve the compute cost and task accuracy trade-off for down-scaled models.

*Improve LLM Interpretability.* We find a remarkably small set of weights responsible for ICL. This underscores the potential of pruning as a tool for isolating neurons responsible for LLM capabilities.

Contributions.

1.  1.
    We curate a set of benchmarks for assessing the disparate effects of down-scaling on core capabilities of LLMs, focusing on fact recall and ICL.
2.  2.
    Using these benchmarks, we evaluate two scalable weight pruning algorithms for LLMs. We investigate an extensive set of models comprising six base LLMs, with sizes reaching up to 33 billion parameters. We find that:

    - •
      even moderate levels of pruning ($\phantom{} > {30\%}$) hurt fact recall. However, when the evidence required to solve a question-answering task is provided in context, the model’s ability to correctly answer questions survives to higher levels of sparsity;
    - •
      in contrast, in-context learning withstands aggressive pruning (up to 60–70%).
3.  3.
    Similarly for dense scaling, we find the same disparate patterns as above for fact recall and ICL abilities relative to model size. This underscores that the disparate effects on ICL and fact recall are not exclusive to pruning but are broader characteristics of scaling in general.

|               |                     |                    |                                         |                                      |                                       |                      |
|---------------|---------------------|--------------------|-----------------------------------------|--------------------------------------|---------------------------------------|----------------------|
| Task Type     | Task                |  Context Type      |  Recalling Facts from Pre-training      |  Retrieving Facts from Contexts      |  Learning Patterns from Contexts      |  Considered ICL      |
| Q&A           | WebQuestions        | Empty              | ✓                                       | ✗                                    | \-                                    | ✗                    |
|               | NaturalQuestions    | Factual            | ✓                                       | ✓                                    | \-                                    | ✓                    |
|               | TriviaQA            | Empty              | ✓                                       | ✗                                    | \-                                    | ✗                    |
|               | TriviaQA (Filtered) | Factual            | ✓                                       | ✓                                    | \-                                    | ✓                    |
|               | DisentQA            | Synthetic          | ✗                                       | ✓                                    | \-                                    | ✓                    |
|  Learning     | Linear CLS          | Exemplary          | \-                                      | \-                                   | ✓                                     | ✓                    |
|               | 2-layer NN          | Exemplary          | \-                                      | \-                                   | ✓                                     | ✓                    |
|               | Decision Tree       | Exemplary          | \-                                      | \-                                   | ✓                                     | ✓                    |

Table 1: Tasks employed in our experiments.

## 2 Related Work

LLM scaling. Studies on scaling laws ([Hoffmann et al., 2022a](#bib.bib28); [Kaplan et al., 2020b](#bib.bib37)) suggest a predictable relationship between the quality of language models (i.e., perplexity) and the size of the pre-training corpus and model. Pursuant to this, many have scaled up and discovered remarkable capabilities of language models. [Brown et al. (2020b)](#bib.bib8) discover that LLMs can perform in-context learning (ICL) effectively: the model learns to perform tasks based on a few examples of input–output demonstrations in the model’s context. Other studies ([Devlin et al., 2019](#bib.bib15); [Wei et al., 2022](#bib.bib61); [Liang et al., 2022](#bib.bib42); [Srivastava et al., 2022](#bib.bib55); [Gao et al., 2021](#bib.bib24); [Ganguli et al., 2022](#bib.bib23); [Bubeck et al., 2023](#bib.bib9); [Biderman et al., 2023a](#bib.bib3)) benchmark LLMs across many tasks and metrics to assess the utility of scaling. Our work differs in two ways: while prior work ([Kaplan et al., 2020b](#bib.bib37)) studies joint scaling of both pre-training corpus size and model size, we focus on scaling model size alone. Furthermore, instead of measuring an arbitrary notion of task performance, we focus on the foundational capabilities of fact recall and ICL. These capabilities underpin the success of many real world applications of LLMs.

In-weight versus in-context learning. LLMs utilize information both stored in weights and present in context ([Chan et al., 2022a](#bib.bib10)). Recent research illustrates the similarities and differences between these learning approaches: [von Oswald et al. (2022)](#bib.bib59) demonstrated that in-context learning (ICL) can implement an algorithm akin to gradient descent, commonly associated with in-weight learning. [Akyürek et al. (2023)](#bib.bib1) revealed that ICL resembles various in-weight learning algorithms, depending on model size. [Chan et al. (2022b)](#bib.bib11); [Chan et al. (2022a)](#bib.bib10) study how how the properties of the data distribution disparately affect the two abilities in the model. Our work identifies yet another crucial difference: scaling model size has distinct impacts on in-weight learning versus in-context learning abilities.

Neural network pruning. Pruning removes unimportant parameters in a model. The origin of pruning traces back to [LeCun et al. (1990)](#bib.bib40); [Hassibi et al. (1993)](#bib.bib27), with a focus on reducing the computational footprint. More recently, with the advent of deep learning, pruning research has seen a resurgence ([Renda et al., 2020](#bib.bib53); [Han et al., 2016](#bib.bib26); [Liu et al., 2017](#bib.bib45); [Frankle et al., 2021](#bib.bib20); [Molchanov et al., 2017](#bib.bib49); [Dong et al., 2017a](#bib.bib17); [Ma et al., 2023](#bib.bib47); [Tao et al., 2023](#bib.bib57); [Kurtic et al., 2023](#bib.bib38); [Dettmers et al., 2023](#bib.bib14)). Though pruning traditionally focuses on preserving aggregate metrics such as accuracy, the versatility of LLMs calls for a different approach to assessing pruned models. Our work begins to fill this gap, proposing to evaluate pruning’s effect on fact recall and ICL. Our investigation extends a growing line of studies on effects of pruning beyond aggregate metrics such as accuracy and perplexity. [Hooker et al. (2019)](#bib.bib30); [Hooker et al. (2020)](#bib.bib31) show that pruning may harm under-represented categories of examples; [Liebenwein et al. (2021)](#bib.bib43) suggest that the pruned models are less accurate than the dense one when predicting out-of-distribution examples. [Jin et al. (2022)](#bib.bib34) demonstrate that pruning mitigates the harmful effects of noisy labels on generalization.

Concurrent to our work, [Yin et al. (2023)](#bib.bib62); [Jaiswal et al. (2023)](#bib.bib32) remarked on the pronounced negative effect of pruning on knowledge-intensive tasks. These works extensively evaluate tasks that require abilities of fact recall and in-context information retrieval. Our work additionally curates a gradation of tasks that further disentangle these abilities — specifically via overriding QA and parameterized ICL tasks, which are not covered in these works.

## 3 Preliminaries

Pruning algorithms. We investigate pruning as one possible technique to (down-)scale LLMs. Few pruning algorithms currently scale to LLMs. We use SparseGPT ([Frantar & Alistarh, 2023](#bib.bib21)) in the main text and Wanda ([Sun et al., 2023](#bib.bib56)) in [Appendix F](#A6 "Appendix F Additional Pruning Algorithm Evaluation ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning"). Both are one-shot pruning algorithms that scale to LLMs and outperform magnitude pruning (i.e., pruning the smallest magnitude weights), without computationally intensive re-training ([Frantar & Alistarh, 2023](#bib.bib21)). SparseGPT/Wanda prune each layer of the language model by minimizing the $\ell_{2}$-distance between the outputs of the original dense layer and the pruned layer. SparseGPT/Wanda computes these outputs based on a small training dataset. See [Frantar & Alistarh (2023, Sec. 3)](#bib.bib21) for more details. While SparseGPT update the remaining weights after weights removal, Wanda does not.

Following standard practice ([Frantar & Alistarh, 2023](#bib.bib21); [Frankle & Carbin, 2019](#bib.bib19)), we only prune fully-connected layers. Since attention and feed forward modules consist of mostly fully-connected layers, parameters in fully-connected layers account for $\phantom{} > {97.5\%}$ parameters for all models we examine. We do not prune embedding layers, language modeling heads and normalization layers.

Models. We evaluate 6 models from 3 families: OPT ([Zhang et al., 2022](#bib.bib63)), LLaMA ([Touvron et al., 2023](#bib.bib58)) and Pythia ([Biderman et al., 2023b](#bib.bib4)). We focus on OPT and LLaMA in our main text and present Pythia results in [Appendix G](#A7 "Appendix G Pythia Models Evaluation ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning"). Pythia family models show consistent results as LLaMA and OPT family models. From the OPT family, we evaluate the two largest models that fit in our hardware setup – OPT-13B and OPT-30B, with 13 and 30 billion parameters, respectively. From the LLaMA family, we evaluate LLaMA-13B and LLaMA-33B, with 13 and 33 billion parameters, respectively.

A notable difference between OPT and LLaMA families is the ratio of training data to model parameters. [Zhang et al. (2022)](#bib.bib63) train the OPT family of models with 180 billion tokens, yielding approximately 14 and 5.5 tokens per parameter, respectively, for our two considered OPT models. [Touvron et al. (2023)](#bib.bib58) train the LLaMA-13B model with 1 trillion tokens (77 tokens/parameter) and the LLaMA-33B model with 1.4 trillion tokens (42 tokens/parameter).

### 3.1 Evaluation

We evaluate models on two complementary abilities: the ability to call on information seen during pre-training (and then stored in the model’s weights) and the ability to call on information presented in-context. Unfortunately, it is difficult to construct tasks that strictly isolate one of these two abilities. On the one hand, for every conceivable natural language task, the model must rely on the semantic representations of language learned from pre-training and stored in the weights. On the other, every conceivable task necessitates processing all of the context to understand the instructions in the first place. To help disentangle the two (overly) broad abilities, we focus on two well-defined instantiations of these abilities: (a) the ability to recall facts from pre-training to answer questions and, complementing that (b) the ability to learn patterns from context.

Fact recall. We isolate (a) by evaluating the model on recalling facts from training data not provided in-context. We do this using closed-book QA benchmarks.

In-context learning. To evaluate (b), we consider a gradation of tasks that require the increasingly advanced ways of learning from in-context information. Broadly, we consider a series of in-context learning tasks: tasks where the context contains examplars of (query, answer) pairs in some form, followed by a test query that the model has to answer.

First, as a simple ICL task, we consider an Open-book QA ([Section 4](#S4 "4 Effect of Pruning on Question Answering Tasks ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")) counterpart of our QA task. Here the context is augmented with supporting evidence that directly helps answer the question. This can be thought of as a simple ICL task where the test query (“who is the author of the novel The Eagle Has Landed?”) is simply already present as an in-context examplar within the evidence (“The author of The Eagle Has Landed is…”), along with its ground truth answer (e.g., “…Jack Higgins”). Note that in addition to the aforementioned evidence–question–answer triplet, we further aid the model with an independent one-shot triplet to demonstrate how to format its answer.

In the above case, the answer provided in-context may also have been present in pre-training data; thus the model may opt to ignore the context, and recall facts from pre-training, and still succeed at the task. Thus, to more rigorously isolate the two mechanisms, we next evaluate on the Overriding QA task ([Section 4](#S4 "4 Effect of Pruning on Question Answering Tasks ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning")), where the in-context evidence contradicts a fact present in training data. We present a one-shot evidence–question–answer triplet, where the answer is based on the contextual evidence rather than on pre-training facts. Thus, to solve the task correctly, it is clear that the model must retrieve from the context rather than recall pre-training facts.

Next, we investigate ICL abilities more sophisticated than copying an answer present in an in-context exemplar. To this end, we are interested in tasks where the test query is not already seen as an in-context exemplar. As one such example, consider English–French translation task ([Brown et al., 2020b](#bib.bib8)) where the examplars are pairs of English and French sentences, and the test query is a new English sentence. However, such conventional instances of ICL tasks require significant background knowledge of languages and the world, not available in the context.

To ensure we disentangle the role of background knowledge from ICL, we consider tasks where the query–answer mapping is given by a parameterized function. Arguably, learning this mapping, would require advanced context-processing mechanisms that go beyond information-retrieval mechanisms required for the Open-book and Overriding QA tasks.

Metrics. As a simple point of comparison, we measure the effect of scaling on perplexity. However, our main metric of interest is exact match accuracy (of the answer to each task) because it is a direct measure of the model’s ability to satisfactorily perform a task.

We present pruning’s effects on model perplexity in [Appendix B](#A2 "Appendix B Pruning Perplexity Eval ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning") and details of our hardware/software configurations in [Appendix J](#A10 "Appendix J Details on Computing Software/Hardware ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning").

## 4 Effect of Pruning on Question Answering Tasks

The ability of LLMs to answer questions underpins many applications of LLMs. Within a question-answering evaluation framework, we examine the effect of pruning on its ability to recall facts learnt during pre-training. We also test a simple form of ICL capability – extracting answers exclusively from the provided context, where answers do not exist in the pre-training corpus. Finally, we interpolate between these two capabilities by providing supporting evidence in context when querying information is likely also available in pre-training data. Our results expose that, with contextual information in question-answering tasks, the model’s ability to answer questions withstands more aggressive pruning than without contextual information. With no supporting evidence in context, accuracy rapidly drops as sparsity increases.

Figure 2: Evaluation for question answering tasks under pruning. Each color represents a different model; each line-style/marker-shape combination represents a different QA dataset. Moderate pruning harms LLMs’ ability to recall facts learnt during pre-training: in close-book QA tasks, accepting a 5% drop in average accuracy w.r.t. the dense models, we can prune to 30 and 40% on TriviaQA and WebQA dataset. However, when we present the model with the necessary information to answer the question in its context, the model’s ability to answer questions survives to higher sparsity: on open-book QA tasks, accepting the same drop in average accuracy, we can prune to 50% and 60% on TriviaQA(F) and NatQ dataset. On the overriding task (DissentQA dataset), we may even prune to 70% while maintaining the same acceptable relative accuracy drop.

Datasets. We use these datasets: (a) *TriviaQA.* [Joshi et al. (2017)](#bib.bib35) developed the TriviaQA dataset with questions and supporting evidence. We use its Wikipedia validation partition consisting of 7993 questions. (b) *WebQuestions.* [Berant et al. (2013)](#bib.bib2) collected question-answer pairs from the Freebase knowledge database. We use its test set consisting of 2032 questions. (c) *NaturalQuestions.* [Kwiatkowski et al. (2019)](#bib.bib39) compiled the NaturalQuestions dataset from Google search queries. We sampled a 7700-question subset of its validation partition (the same size as the following dataset derived from it), to make our evaluation computationally feasible. (d) *DissentQA.* [Neeman et al. (2022)](#bib.bib51) constructed the DissentQA dataset from the NaturalQuestions dataset. It contains pairs of questions and evidence for a made-up answer that is different from the factual one. It assesses whether the model can override its memory formed during pre-training with new context. We use its validation partition consisting of 7700 questions.

Evaluation setup. Using the aforementioned datasets, we evaluate the ability of pruned models on the following task setup: (i) *Close-book*. We feed the question without any supporting information to the model. We use the Wikipedia partition of the TriviaQA dataset without the supporting evidence and the WebQA dataset for this setup. (ii) *Open-book*. We feed the question with supporting evidence to the model in its context. It is important to note that this evaluation setup only evaluates whether the answer is right; it is however agnostic to the mechanism by which the answer is retrieved: the model may either generate its answer using the supporting evidence, or by recalling facts from pre-training. To create this dataset, we use a subset of the TriviaQA dataset whose context can fit within the maximum sequence length of the model, consisting of 881 questions. We denote this filtered subset as TriviaQA(F). Additionally, we use the NaturalQuestions dataset for this setup with factual contexts. (iii) *Overriding*. We present the question accompanied by evidence that deviates from the facts presented during pre-training. Given that the anticipated made-up answers are randomized and different from the factual ones, the model cannot depend on memorization from its pre-training data to generate responses. This evaluation framework rigorously assesses the model’s ability to override its pre-training data with new, context-specific information. We use the DisentQA dataset with synthetic contexts for this setup. Examples of the setups are shown in [Appendix H](#A8 "Appendix H Example Prompts ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning").

To summarize: across these setups, our prompts have three parts to them: first, (1) an example context–question–answer triplet (or question–answer pair in close-book setting) for demonstration, (2) the supporting evidence for a test question (except in the close-book setup), and (3) a test question to answer. Answers are the model’s prompt completions produced by greedy decoding. We report the percentage of answers that exactly match ground truth.

Close-book versus open-book results. Left 2 plots of [Figure 2](#S4.F2 "In 4 Effect of Pruning on Question Answering Tasks ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning") shows close-book and open-book results. Notably, for all the models, the pruned model maintains performance on open-book tasks until much higher sparsity levels compared to close-book tasks. In particular, when we accept a relative decrease of 5% from pruning in the mean accuracy over four models, the highest achievable sparsities for closed-book tasks are 30% on TriviaQA and 40% on WebQA.

In contrast, maintaining the same acceptable performance drop, the highest acceptable sparsity levels for open-book tasks are 50% on TriviaQA(F) and 60% on NaturalQuestions. Our results suggest that while pruning hurts the model’s ability to recall information from its pre-training data at moderate sparsity (30–40%), one possible remedy is to provide the model with relevant evidence in context. The model’s ability to answer questions with relevant evidence in its context remains largely intact to higher sparsity levels (50–60%).

Overriding results. The rightmost plot of [Figure 2](#S4.F2 "In 4 Effect of Pruning on Question Answering Tasks ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning") demonstrates a consistent trend for the overriding tasks. On the DisentQA dataset with overriding context, the highest achievable sparsity is 70% allowing for the same 5% accuracy drop as before. Recall that to solve the overriding task, the model must rely on in-context information rather than in-weights information from the pre-training data. Thus, our observations here further substantiate that the model’s ability to extracting information from its context remains largely intact at higher sparsity levels.

Accuracy improvements. We note that, surprisingly, on open-book and overriding tasks, there can be small accuracy boosts from pruning. For example, the pruned OPT-30B sees a 9.7% accuracy improvement on DissentQA dataset in overriding task setup. The pruned LLaMa-13B sees 3.5% accuracy improvement on NaturalQuestions in the open-book task setup. Though prior work often reports accuracy improvements with pruning ([Frankle & Carbin, 2019](#bib.bib19); [Renda et al., 2020](#bib.bib53)), we are, to the best of our knowledge, the first to observe such improvement in the QA setup.

Takeaways. Our findings suggest that scaling via pruning has a much higher impact on the ability to retrieve facts from pre-training than on the ability to retrieve information from the context. Pruning may even improve model’s ability to answer questions when its context includes the necessary information to answer the question.

## 5 More Sophisticated In-context Learning

[Section 4](#S4 "4 Effect of Pruning on Question Answering Tasks ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning") demonstrates that moderate pruning preserves question answering task accuracy when relevant information is available in context. In this section, we show that even with more sophisticated ICL tasks than previously studied, moderately pruned models maintain their ICL abilities.

Typical complex ICL tasks require extensive knowledge about language and the world gathered from pre-training. However, as [Section 4](#S4 "4 Effect of Pruning on Question Answering Tasks ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning") shows, pruning likely impairs such knowledge. So, to isolate LLMs’ ICL ability from factual recall abilities, we choose a set of tasks where the goal is to learn a parameterized function (e.g., a linear model) through input-output examples present in-context.

Figure 3: ICL withstands aggresive pruning (60-70% spasity). Accepting a relative average (over 4 models) accuracy drop of 5% w.r.t. the dense models, we can prune to 60%, 60% and 70% on linear classification, 2-layer NN, decision tree tasks, respectively.

Method. We evaluate LLMs in their ability to learn multiclass classifiers of the form $f:{\mathbb{R}}^{D}\rightarrow{\{ 0,1,\cdots K - 1\}}$ from in-context examples. To generate a sequence consisting of a context, query and an answer, we first pick a random parameterized function $f$ from one of three function classes: 2-way linear classifiers, 2-way neural network classifiers with 2 layers and 4-way decision tree classifiers ([Appendix C](#A3 "Appendix C Constructing Parameterized Functions in ICL Evaluation ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning") contains details for constructing $f$). Then, in the context, we provide $N$ exemplars of the form $(x,{f{(x)}})$, followed by a novel query $x_{query}$. The goal of the model is to correctly predict the answer as $f{(x_{query})}$. Please refer to [Appendix H](#A8 "Appendix H Example Prompts ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning") for an example of the full prompt.

All task instances consist of $N$ total in-context examples split evenly across all possible labels. We draw all random numbers uniformly from integers between -10 and 10 inclusive. We set D=4, N=32. We record additional methodological details in [Appendix D](#A4 "Appendix D Additional Details for ICL Evaluation Methodology ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning").

Pruning results. [Figure 3](#S5.F3 "In 5 More Sophisticated In-context Learning ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning") shows the accuracy of pruned models versus sparsity. We can remove a substantial number of parameters from the models without affecting their ICL ability. Specifically, the average accuracy of the pruned models on linear, 2-layer NN, decision tree classification tasks is within 5% of the dense models up to 60%, 60% and 70% sparsity, respectively.

Task difficulty. One trivial explanation for our observation is that perhaps these tasks are so easy that they are solvable even by a severely pruned model. To eliminate this hypothesis, in [Appendix E](#A5 "Appendix E Increasing Input Dimension of ICL Evaluation ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning"), we increase the input dimension ($D$) of the linear classification task. Even as we increase this to a significant extent (say, to an extent that the task is almost, but not totally, unlearnable), we find that the ICL performance is maintained under aggressive pruning.

Conclusion. Our results suggest that when pruning LLMs moderately (i.e., to $\phantom{} < {70\%}$ sparsity), the model’s ICL ability stays largely intact. Thus, unlike fact recall tasks, one can prune models significantly more while maintaining ICL performance.

## 6 Dense Scaling

Figure 4: Like pruning, moderate dense down-scaling preserves ICL while harming fact recall.

In the context of vision models, it is known that pruned models behave similarly to smaller dense models trained with similar hyperparameters ([Jin et al., 2022](#bib.bib34)). Here, we examine the effects of dense scaling (i.e., choosing from a suite of independently trained models of various sizes) on fact recall vs. ICL abilities of LLMs.

Method. With the same benchmarks as in [Sections 4](#S4 "4 Effect of Pruning on Question Answering Tasks ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning") and [5](#S5 "5 More Sophisticated In-context Learning ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning"), we evaluate the accuracy of dense models with different parameter count, but the same pre-training data size. The OPT family of models provides an ideal collection of dense models for our evaluation: [Zhang et al. (2022)](#bib.bib63) trained all OPT models with the same number of tokens (300b).

Results. [Figure 4](#S6.F4 "In 6 Dense Scaling ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning") shows that fact recall ability is highly sensitive to dense scaling – e.g., focusing on scaling downwards, moving from the 30B model to the next largest 13B model leads to more than 5% relative task accuracy degradation on close-book TriviaQA and WebQA task. However, open-book/overriding QA accuracy is much less sensitive to dense scaling. Specifically, maintaining the same 5% acceptable relative accuracy degradation with respect to the 30B models, one may replace a 30B model on TriviaQA(F) and NaturalQuestions dataset with a 6.7B model. [Figure 4](#S6.F4 "In 6 Dense Scaling ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning") also shows that ICL ability is similarly robust to dense scaling.

Conclusion. Like pruning, changing a dense model’s size more readily affects its ability to retrieve facts from pre-training than to process information from context. We hypothesize that this effect stems from scaling in general – be it pruning or using a dense model of different size.

## 7 Pruning Attention and Feed Forward Layers

A growing line of work ([Dai et al., 2021](#bib.bib13); [Meng et al., 2022](#bib.bib48)) suggests that feed forward (FFW) layers and the attention layers are responsibly for distinct capabilities considered in this paper — namely, fact recall and in-context learning. To test this, we exclusively prune either type of layers and examine how the model’s abilities deteriorate on fact recall and ICL tasks.

(a) Linear Classification

(b) TriviaQA Close-book

Figure 5: Effects of pruning only attention layers versus pruning only FFW layers on fact recall (TriviaQA) versus ICL (Linear Classification). Module sparsity computes the fraction of parameters of the specified module ( attention or FFW) that pruning removes. Attention and FFW layers appear equally important for ICL. FFW layers appear more important than attention layers for fact recall.

Method. We prune a LLaMA-13B model. We either exclusively prune attention layers or exclusively prune FFW layers and observe their effects on accuracy of TriviaQA task (fact recall) and linear classification task (ICL). We plotted the task accuracy as a function of module sparsity. Module sparsity refers to the fraction of parameters pruned from a specific type of layers (either attention or FFW), with respect to the total number of parameters of that type.

Results. [Figure 5](#S7.F5 "In 7 Pruning Attention and Feed Forward Layers ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning") shows that while attention and FFW layers appear equally important for ICL, FFW layers appear more important for fact recall. For example, pruning 60% FFW layers lead to 14% more accuracy degradation than pruning 60% of attention layers.

Conclusion. Attention and FFW layers show similar importance for ICL; and FFW layers show greater importance for knowledge recall.

## 8 Closing Discussion

We study the effects of scaling model size via pruning and dense scaling on two core abilities of LLMs that underpin their practical success: the ability to recall facts and the ability to perform ICL. In both cases, we find similar disparate effects on the two abilities. Moderate pruning ($\phantom{} > {30\%}$ sparsity) harms fact recall, and yet the ability to learn from a few input-output examples from context withstands aggressive pruning (up to 60–70% sparsity). The same disparity arises when changing the width and depth of dense (independently-trained) models.

What could explain this disparity? We conjecture that the number of parameters required to store a set of facts must scale in proportion to the number of independent facts. On the other hand, in-context learning of many kinds may be accomplished by a smaller set of parameters that act as a universal gradient descent module ([von Oswald et al., 2022](#bib.bib59)) that can be applied for any task. Verifying these hypotheses theoretically is an important direction for future work. Our findings also invite various research directions for practice:

Pruning & interpretability. Our findings suggest, remarkably, a relatively small fraction of weights are responsible for ICL performance. This observation could prove to be valuable for enhancing the interpretability of LLMs, reviving a decades-old motivation behind work in pruning ([Mozer & Smolensky, 1988](#bib.bib50)).³³ 3 ”This skeletonization technique can be used … to understand the behavior of networks in terms of minimal ’rules.’” ([Mozer & Smolensky, 1988](#bib.bib50)) In particular, pruning may help better localize the weights responsible for in-context ability, and complement recent approaches ([Wang et al., 2023](#bib.bib60); [Bills et al., 2023](#bib.bib5)).

Memory augmentation. Our observations advocate for memory augmentation as a promising way to improve the trade-off between computational cost and task accuracy. Memory augmentation techniques present helpful facts to the model by augmenting them directly in the context. Thus, rather than having the LLM to rely on fact recall from pre-training — an ability that is degraded under downscaling — we can delegate fact-retrieval to a separate retrieval model ([Borgeaud et al., 2022](#bib.bib6); [Guu et al., 2020](#bib.bib25)), and allow the LLM to focus on retrieving the fact from the context—which is an ability that is preserved under down-scaling.

Limitations. We address the limitations of our work in [Appendix A](#A1 "Appendix A Limitation. ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning").

## References

- Akyürek et al. (2023) Ekin Akyürek, Dale Schuurmans, Jacob Andreas, Tengyu Ma, and Denny Zhou. What learning algorithm is in-context learning? investigations with linear models. In *The Eleventh International Conference on Learning Representations*, 2023. URL [https://openreview.net/forum?id=0g0X4H8yN4I](https://openreview.net/forum?id=0g0X4H8yN4I).
- Berant et al. (2013) Jonathan Berant, Andrew Chou, Roy Frostig, and Percy Liang. Semantic parsing on Freebase from question-answer pairs. In *Proceedings of the 2013 Conference on Empirical Methods in Natural Language Processing*, pp. 1533–1544, Seattle, Washington, USA, October 2013. Association for Computational Linguistics. URL [https://aclanthology.org/D13-1160](https://aclanthology.org/D13-1160).
- Biderman et al. (2023a) Stella Biderman, USVSN Sai Prashanth, Lintang Sutawika, Hailey Schoelkopf, Quentin Anthony, Shivanshu Purohit, and Edward Raff. Emergent and predictable memorization in large language models, 2023a.
- Biderman et al. (2023b) Stella Biderman, Hailey Schoelkopf, Quentin Anthony, Herbie Bradley, Kyle O’Brien, Eric Hallahan, Mohammad Aflah Khan, Shivanshu Purohit, USVSN Sai Prashanth, Edward Raff, Aviya Skowron, Lintang Sutawika, and Oskar van der Wal. Pythia: A suite for analyzing large language models across training and scaling, 2023b.
- Bills et al. (2023) Steven Bills, Nick Cammarata, Dan Mossing, Henk Tillman, Leo Gao, Gabriel Goh, Ilya Sutskever, Jan Leike, Jeff Wu, and William Saunders. Language models can explain neurons in language models. [https://openaipublic.blob.core.windows.net/neuron-explainer/paper/index.html](https://openaipublic.blob.core.windows.net/neuron-explainer/paper/index.html), 2023.
- Borgeaud et al. (2022) Sebastian Borgeaud, Arthur Mensch, Jordan Hoffmann, Trevor Cai, Eliza Rutherford, Katie Millican, George Bm Van Den Driessche, Jean-Baptiste Lespiau, Bogdan Damoc, Aidan Clark, Diego De Las Casas, Aurelia Guy, Jacob Menick, Roman Ring, Tom Hennigan, Saffron Huang, Loren Maggiore, Chris Jones, Albin Cassirer, Andy Brock, Michela Paganini, Geoffrey Irving, Oriol Vinyals, Simon Osindero, Karen Simonyan, Jack Rae, Erich Elsen, and Laurent Sifre. Improving language models by retrieving from trillions of tokens. In Kamalika Chaudhuri, Stefanie Jegelka, Le Song, Csaba Szepesvari, Gang Niu, and Sivan Sabato (eds.), *Proceedings of the 39th International Conference on Machine Learning*, volume 162 of *Proceedings of Machine Learning Research*, pp. 2206–2240. PMLR, 2022. URL [https://proceedings.mlr.press/v162/borgeaud22a.html](https://proceedings.mlr.press/v162/borgeaud22a.html).
- Brown et al. (2020a) Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel Ziegler, Jeffrey Wu, Clemens Winter, Chris Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei. Language models are few-shot learners. In H. Larochelle, M. Ranzato, R. Hadsell, M.F. Balcan, and H. Lin (eds.), *Advances in Neural Information Processing Systems*, volume 33, pp. 1877–1901, 2020a.
- Brown et al. (2020b) Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei. Language models are few-shot learners, 2020b.
- Bubeck et al. (2023) Sébastien Bubeck, Varun Chandrasekaran, Ronen Eldan, Johannes Gehrke, Eric Horvitz, Ece Kamar, Peter Lee, Yin Tat Lee, Yuanzhi Li, Scott Lundberg, Harsha Nori, Hamid Palangi, Marco Tulio Ribeiro, and Yi Zhang. Sparks of artificial general intelligence: Early experiments with gpt-4, 2023.
- Chan et al. (2022a) Stephanie C. Y. Chan, Ishita Dasgupta, Junkyung Kim, Dharshan Kumaran, Andrew K. Lampinen, and Felix Hill. Transformers generalize differently from information stored in context vs in weights. 2022a. doi: 10.48550/arXiv.2210.05675. URL [https://doi.org/10.48550/arXiv.2210.05675](https://doi.org/10.48550/arXiv.2210.05675).
- Chan et al. (2022b) Stephanie C. Y. Chan, Adam Santoro, Andrew K. Lampinen, Jane X. Wang, Aaditya Singh, Pierre H. Richemond, Jay McClelland, and Felix Hill. Data distributional properties drive emergent in-context learning in transformers, 2022b.
- Chen et al. (2023) Lingjiao Chen, Matei Zaharia, and James Zou. Frugalgpt: How to use large language models while reducing cost and improving performance, 2023.
- Dai et al. (2021) Damai Dai, Li Dong, Y. Hao, Zhifang Sui, and Furu Wei. Knowledge neurons in pretrained transformers. *ArXiv*, abs/2104.08696, 2021.
- Dettmers et al. (2023) Tim Dettmers, Ruslan Svirschevski, Vage Egiazarian, Denis Kuznedelev, Elias Frantar, Saleh Ashkboos, Alexander Borzunov, Torsten Hoefler, and Dan Alistarh. Spqr: A sparse-quantized representation for near-lossless llm weight compression, 2023.
- Devlin et al. (2019) Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. BERT: Pre-training of deep bidirectional transformers for language understanding. In *Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)*, pp. 4171–4186, Minneapolis, Minnesota, June 2019. Association for Computational Linguistics. doi: 10.18653/v1/N19-1423. URL [https://aclanthology.org/N19-1423](https://aclanthology.org/N19-1423).
- Dohan et al. (2022) David Dohan, Winnie Xu, Aitor Lewkowycz, Jacob Austin, David Bieber, Raphael Gontijo Lopes, Yuhuai Wu, Henryk Michalewski, Rif A. Saurous, Jascha Sohl-dickstein, Kevin Murphy, and Charles Sutton. Language model cascades, 2022.
- Dong et al. (2017a) Xin Dong, Shangyu Chen, and Sinno Pan. Learning to prune deep neural networks via layer-wise optimal brain surgeon. In *Advances in Neural Information Processing Systems*, 2017a.
- Dong et al. (2017b) Xin Dong, Shangyu Chen, and Sinno Pan. Learning to prune deep neural networks via layer-wise optimal brain surgeon. *Advances in Neural Information Processing Systems*, 30, 2017b.
- Frankle & Carbin (2019) Jonathan Frankle and Michael Carbin. The lottery ticket hypothesis: Finding sparse, trainable neural networks. In *International Conference on Learning Representations*, 2019. URL [https://openreview.net/forum?id=rJl-b3RcF7](https://openreview.net/forum?id=rJl-b3RcF7).
- Frankle et al. (2021) Jonathan Frankle, Gintare Karolina Dziugaite, Daniel Roy, and Michael Carbin. Pruning neural networks at initialization: Why are we missing the mark? In *International Conference on Learning Representations*, 2021.
- Frantar & Alistarh (2023) Elias Frantar and Dan Alistarh. Sparsegpt: Massive language models can be accurately pruned in one-shot, 2023.
- Frantar et al. (2023) Elias Frantar, Saleh Ashkboos, Torsten Hoefler, and Dan Alistarh. Gptq: Accurate post-training quantization for generative pre-trained transformers, 2023.
- Ganguli et al. (2022) Deep Ganguli, Danny Hernandez, Liane Lovitt, Amanda Askell, Yuntao Bai, Anna Chen, Tom Conerly, Nova Dassarma, Dawn Drain, Nelson Elhage, Sheer El Showk, Stanislav Fort, Zac Hatfield-Dodds, Tom Henighan, Scott Johnston, Andy Jones, Nicholas Joseph, Jackson Kernian, Shauna Kravec, Ben Mann, Neel Nanda, Kamal Ndousse, Catherine Olsson, Daniela Amodei, Tom Brown, Jared Kaplan, Sam McCandlish, Christopher Olah, Dario Amodei, and Jack Clark. Predictability and surprise in large generative models. In *Proceedings of the 2022 ACM Conference on Fairness, Accountability, and Transparency*, FAccT ’22, pp. 1747–1764, New York, NY, USA, 2022. Association for Computing Machinery. ISBN 9781450393522. doi: 10.1145/3531146.3533229. URL [https://doi.org/10.1145/3531146.3533229](https://doi.org/10.1145/3531146.3533229).
- Gao et al. (2021) Leo Gao, Jonathan Tow, Stella Biderman, Sid Black, Anthony DiPofi, Charles Foster, Laurence Golding, Jeffrey Hsu, Kyle McDonell, Niklas Muennighoff, Jason Phang, Laria Reynolds, Eric Tang, Anish Thite, Ben Wang, Kevin Wang, and Andy Zou. A framework for few-shot language model evaluation, September 2021. URL [https://doi.org/10.5281/zenodo.5371628](https://doi.org/10.5281/zenodo.5371628).
- Guu et al. (2020) Kelvin Guu, Kenton Lee, Zora Tung, Panupong Pasupat, and Ming-Wei Chang. Realm: Retrieval-augmented language model pre-training. In *Proc. International Conference on Machine Learning*, 2020.
- Han et al. (2016) Song Han, Huizi Mao, and William J. Dally. Deep compression: Compressing deep neural network with pruning, trained quantization and huffman coding. In *International Conference on Learning Representations*, 2016.
- Hassibi et al. (1993) B. Hassibi, D.G. Stork, and G.J. Wolff. Optimal brain surgeon and general network pruning. In *IEEE International Conference on Neural Networks*, 1993.
- Hoffmann et al. (2022a) Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, Elena Buchatskaya, Trevor Cai, Eliza Rutherford, Diego de las Casas, Lisa Anne Hendricks, Johannes Welbl, Aidan Clark, Tom Hennigan, Eric Noland, Katherine Millican, George van den Driessche, Bogdan Damoc, Aurelia Guy, Simon Osindero, Karen Simonyan, Erich Elsen, Oriol Vinyals, Jack William Rae, and Laurent Sifre. An empirical analysis of compute-optimal large language model training. In Alice H. Oh, Alekh Agarwal, Danielle Belgrave, and Kyunghyun Cho (eds.), *Advances in Neural Information Processing Systems*, 2022a. URL [https://openreview.net/forum?id=iBBcRUlOAPR](https://openreview.net/forum?id=iBBcRUlOAPR).
- Hoffmann et al. (2022b) Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, Elena Buchatskaya, Trevor Cai, Eliza Rutherford, Diego de Las Casas, Lisa Anne Hendricks, Johannes Welbl, Aidan Clark, Tom Hennigan, Eric Noland, Katie Millican, George van den Driessche, Bogdan Damoc, Aurelia Guy, Simon Osindero, Karen Simonyan, Erich Elsen, Jack W. Rae, Oriol Vinyals, and Laurent Sifre. Training compute-optimal large language models, 2022b.
- Hooker et al. (2019) Sara Hooker, Aaron C. Courville, Yann N. Dauphin, and Andrea Frome. What do compressed deep neural networks forget?, 2019.
- Hooker et al. (2020) Sara Hooker, Nyalleng Moorosi, Gregory Clark, Samy Bengio, and Emily Denton. Characterising bias in compressed models, 2020.
- Jaiswal et al. (2023) Ajay Jaiswal, Zhe Gan, Xianzhi Du, Bowen Zhang, Zhangyang Wang, and Yinfei Yang. Compressing llms: The truth is rarely pure and never simple, 2023.
- Jiang et al. (2022) Ting Jiang, Deqing Wang, and Fuzhen Zhuang. Pruning pre-trained language models without fine-tuning, 2022.
- Jin et al. (2022) Tian Jin, Michael Carbin, Dan Roy, Jonathan Frankle, and Gintare Karolina Dziugaite. Pruning’s effect on generalization through the lens of training and regularization. In S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh (eds.), *Advances in Neural Information Processing Systems*, volume 35, pp. 37947–37961. Curran Associates, Inc., 2022. URL [https://proceedings.neurips.cc/paper_files/paper/2022/file/f7ede9414083fceab9e63d9100a80b36-Paper-Conference.pdf](https://proceedings.neurips.cc/paper_files/paper/2022/file/f7ede9414083fceab9e63d9100a80b36-Paper-Conference.pdf).
- Joshi et al. (2017) Mandar Joshi, Eunsol Choi, Daniel S. Weld, and Luke Zettlemoyer. Triviaqa: A large scale distantly supervised challenge dataset for reading comprehension. In *Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics*, Vancouver, Canada, 2017. Association for Computational Linguistics.
- Kaplan et al. (2020a) Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B. Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei. Scaling laws for neural language models. *CoRR*, abs/2001.08361, 2020a. URL [https://arxiv.org/abs/2001.08361](https://arxiv.org/abs/2001.08361).
- Kaplan et al. (2020b) Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B. Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei. Scaling laws for neural language models, 2020b.
- Kurtic et al. (2023) Eldar Kurtic, Elias Frantar, and Dan Alistarh. Ziplm: Hardware-aware structured pruning of language models, 2023.
- Kwiatkowski et al. (2019) Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur Parikh, Chris Alberti, Danielle Epstein, Illia Polosukhin, Matthew Kelcey, Jacob Devlin, Kenton Lee, Kristina N. Toutanova, Llion Jones, Ming-Wei Chang, Andrew Dai, Jakob Uszkoreit, Quoc Le, and Slav Petrov. Natural questions: a benchmark for question answering research. *Transactions of the Association of Computational Linguistics*, 2019.
- LeCun et al. (1990) Yann LeCun, John Denker, and Sara Solla. Optimal brain damage. In *Conference on Neural Information Processing Systems*, 1990.
- Li et al. (2022) Daliang Li, Ankit Singh Rawat, Manzil Zaheer, Xin Wang, Michal Lukasik, Andreas Veit, Felix X. Yu, and Sanjiv Kumar. Large language models with controllable working memory. *CoRR*, 2022. doi: 10.48550/arXiv.2211.05110.
- Liang et al. (2022) Percy Liang, Rishi Bommasani, Tony Lee, Dimitris Tsipras, Dilara Soylu, Michihiro Yasunaga, Yian Zhang, Deepak Narayanan, Yuhuai Wu, Ananya Kumar, Benjamin Newman, Binhang Yuan, Bobby Yan, Ce Zhang, Christian Cosgrove, Christopher D. Manning, Christopher Ré, Diana Acosta-Navas, Drew A. Hudson, Eric Zelikman, Esin Durmus, Faisal Ladhak, Frieda Rong, Hongyu Ren, Huaxiu Yao, Jue Wang, Keshav Santhanam, Laurel Orr, Lucia Zheng, Mert Yuksekgonul, Mirac Suzgun, Nathan Kim, Neel Guha, Niladri Chatterji, Omar Khattab, Peter Henderson, Qian Huang, Ryan Chi, Sang Michael Xie, Shibani Santurkar, Surya Ganguli, Tatsunori Hashimoto, Thomas Icard, Tianyi Zhang, Vishrav Chaudhary, William Wang, Xuechen Li, Yifan Mai, Yuhui Zhang, and Yuta Koreeda. Holistic evaluation of language models, 2022.
- Liebenwein et al. (2021) Lucas Liebenwein, Cenk Baykal, Brandon Carter, David Gifford, and Daniela Rus. Lost in pruning: The effects of pruning neural networks beyond test accuracy. In *Conference on Machine Learning and Systems*, 2021.
- Liu & Low (2023) Tiedong Liu and Bryan Kian Hsiang Low. Goat: Fine-tuned llama outperforms gpt-4 on arithmetic tasks, 2023.
- Liu et al. (2017) Zhuang Liu, Jianguo Li, Zhiqiang Shen, Gao Huang, Shoumeng Yan, and Changshui Zhang. Learning efficient convolutional networks through network slimming. In *Proceedings of the IEEE International Conference on Computer Vision (ICCV)*, 2017.
- Longpre et al. (2021) Shayne Longpre, Kartik Perisetla, Anthony Chen, Nikhil Ramesh, Chris DuBois, and Sameer Singh. Entity-based knowledge conflicts in question answering. In *Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, EMNLP 2021, Virtual Event / Punta Cana, Dominican Republic, 7-11 November, 2021*, pp. 7052–7063. Association for Computational Linguistics, 2021.
- Ma et al. (2023) Xinyin Ma, Gongfan Fang, and Xinchao Wang. Llm-pruner: On the structural pruning of large language models, 2023.
- Meng et al. (2022) Kevin Meng, David Bau, Alex Andonian, and Yonatan Belinkov. Locating and editing factual associations in gpt. In S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh (eds.), *Advances in Neural Information Processing Systems*, volume 35, pp. 17359–17372. Curran Associates, Inc., 2022. URL [https://proceedings.neurips.cc/paper_files/paper/2022/file/6f1d43d5a82a37e89b0665b33bf3a182-Paper-Conference.pdf](https://proceedings.neurips.cc/paper_files/paper/2022/file/6f1d43d5a82a37e89b0665b33bf3a182-Paper-Conference.pdf).
- Molchanov et al. (2017) Pavlo Molchanov, Stephen Tyree, Tero Karras, Timo Aila, and Jan Kautz. Pruning convolutional neural networks for resource efficient inference. In *International Conference on Learning Representations*, 2017.
- Mozer & Smolensky (1988) Michael C Mozer and Paul Smolensky. Skeletonization: A technique for trimming the fat from a network via relevance assessment. In D. Touretzky (ed.), *Advances in Neural Information Processing Systems*, volume 1. Morgan-Kaufmann, 1988. URL [https://proceedings.neurips.cc/paper_files/paper/1988/file/07e1cd7dca89a1678042477183b7ac3f-Paper.pdf](https://proceedings.neurips.cc/paper_files/paper/1988/file/07e1cd7dca89a1678042477183b7ac3f-Paper.pdf).
- Neeman et al. (2022) Ella Neeman, Roee Aharoni, Or Honovich, Leshem Choshen, Idan Szpektor, and Omri Abend. Disentqa: Disentangling parametric and contextual knowledge with counterfactual question answering, 2022.
- Paszke et al. (2019) Adam Paszke, Sam Gross, Francisco Massa, Adam Lerer, James Bradbury, Gregory Chanan, Trevor Killeen, Zeming Lin, Natalia Gimelshein, Luca Antiga, Alban Desmaison, Andreas Kopf, Edward Yang, Zachary DeVito, Martin Raison, Alykhan Tejani, Sasank Chilamkurthy, Benoit Steiner, Lu Fang, Junjie Bai, and Soumith Chintala. Pytorch: An imperative style, high-performance deep learning library. In *Advances in Neural Information Processing Systems 32*, pp. 8024–8035. Curran Associates, Inc., 2019. URL [http://papers.neurips.cc/paper/9015-pytorch-an-imperative-style-high-performance-deep-learning-library.pdf](http://papers.neurips.cc/paper/9015-pytorch-an-imperative-style-high-performance-deep-learning-library.pdf).
- Renda et al. (2020) Alex Renda, Jonathan Frankle, and Michael Carbin. Comparing rewinding and fine-tuning in neural network pruning. In *International Conference on Learning Representations*, 2020.
- Santacroce et al. (2023) Michael Santacroce, Zixin Wen, Yelong Shen, and Yuanzhi Li. What matters in the structured pruning of generative language models?, 2023.
- Srivastava et al. (2022) Aarohi Srivastava, Abhinav Rastogi, Abhishek Rao, Abu Awal Md Shoeb, Abubakar Abid, Adam Fisch, Adam R. Brown, Adam Santoro, Aditya Gupta, Adrià Garriga-Alonso, Agnieszka Kluska, Aitor Lewkowycz, Akshat Agarwal, Alethea Power, Alex Ray, Alex Warstadt, Alexander W. Kocurek, Ali Safaya, Ali Tazarv, Alice Xiang, Alicia Parrish, Allen Nie, Aman Hussain, Amanda Askell, Amanda Dsouza, Ambrose Slone, Ameet Rahane, Anantharaman S. Iyer, Anders Andreassen, Andrea Madotto, Andrea Santilli, Andreas Stuhlmüller, Andrew Dai, Andrew La, Andrew Lampinen, Andy Zou, Angela Jiang, Angelica Chen, Anh Vuong, Animesh Gupta, Anna Gottardi, Antonio Norelli, Anu Venkatesh, Arash Gholamidavoodi, Arfa Tabassum, Arul Menezes, Arun Kirubarajan, Asher Mullokandov, Ashish Sabharwal, Austin Herrick, Avia Efrat, Aykut Erdem, Ayla Karakaş, B. Ryan Roberts, Bao Sheng Loe, Barret Zoph, Bartłomiej Bojanowski, Batuhan Özyurt, Behnam Hedayatnia, Behnam Neyshabur, Benjamin Inden, Benno Stein, Berk Ekmekci, Bill Yuchen Lin, Blake Howald, Cameron Diao, Cameron Dour, Catherine Stinson, Cedrick Argueta, César Ferri Ramírez, Chandan Singh, Charles Rathkopf, Chenlin Meng, Chitta Baral, Chiyu Wu, Chris Callison-Burch, Chris Waites, Christian Voigt, Christopher D. Manning, Christopher Potts, Cindy Ramirez, Clara E. Rivera, Clemencia Siro, Colin Raffel, Courtney Ashcraft, Cristina Garbacea, Damien Sileo, Dan Garrette, Dan Hendrycks, Dan Kilman, Dan Roth, Daniel Freeman, Daniel Khashabi, Daniel Levy, Daniel Moseguí González, Danielle Perszyk, Danny Hernandez, Danqi Chen, Daphne Ippolito, Dar Gilboa, David Dohan, David Drakard, David Jurgens, Debajyoti Datta, Deep Ganguli, Denis Emelin, Denis Kleyko, Deniz Yuret, Derek Chen, Derek Tam, Dieuwke Hupkes, Diganta Misra, Dilyar Buzan, Dimitri Coelho Mollo, Diyi Yang, Dong-Ho Lee, Ekaterina Shutova, Ekin Dogus Cubuk, Elad Segal, Eleanor Hagerman, Elizabeth Barnes, Elizabeth Donoway, Ellie Pavlick, Emanuele Rodola, Emma Lam, Eric Chu, Eric Tang, Erkut Erdem, Ernie Chang, Ethan A. Chi, Ethan Dyer, Ethan Jerzak, Ethan Kim, Eunice Engefu Manyasi, Evgenii Zheltonozhskii, Fanyue Xia, Fatemeh Siar, Fernando Martínez-Plumed, Francesca Happé, Francois Chollet, Frieda Rong, Gaurav Mishra, Genta Indra Winata, Gerard de Melo, Germán Kruszewski, Giambattista Parascandolo, Giorgio Mariani, Gloria Wang, Gonzalo Jaimovitch-López, Gregor Betz, Guy Gur-Ari, Hana Galijasevic, Hannah Kim, Hannah Rashkin, Hannaneh Hajishirzi, Harsh Mehta, Hayden Bogar, Henry Shevlin, Hinrich Schütze, Hiromu Yakura, Hongming Zhang, Hugh Mee Wong, Ian Ng, Isaac Noble, Jaap Jumelet, Jack Geissinger, Jackson Kernion, Jacob Hilton, Jaehoon Lee, Jaime Fernández Fisac, James B. Simon, James Koppel, James Zheng, James Zou, Jan Kocoń, Jana Thompson, Jared Kaplan, Jarema Radom, Jascha Sohl-Dickstein, Jason Phang, Jason Wei, Jason Yosinski, Jekaterina Novikova, Jelle Bosscher, Jennifer Marsh, Jeremy Kim, Jeroen Taal, Jesse Engel, Jesujoba Alabi, Jiacheng Xu, Jiaming Song, Jillian Tang, Joan Waweru, John Burden, John Miller, John U. Balis, Jonathan Berant, Jörg Frohberg, Jos Rozen, Jose Hernandez-Orallo, Joseph Boudeman, Joseph Jones, Joshua B. Tenenbaum, Joshua S. Rule, Joyce Chua, Kamil Kanclerz, Karen Livescu, Karl Krauth, Karthik Gopalakrishnan, Katerina Ignatyeva, Katja Markert, Kaustubh D. Dhole, Kevin Gimpel, Kevin Omondi, Kory Mathewson, Kristen Chiafullo, Ksenia Shkaruta, Kumar Shridhar, Kyle McDonell, Kyle Richardson, Laria Reynolds, Leo Gao, Li Zhang, Liam Dugan, Lianhui Qin, Lidia Contreras-Ochando, Louis-Philippe Morency, Luca Moschella, Lucas Lam, Lucy Noble, Ludwig Schmidt, Luheng He, Luis Oliveros Colón, Luke Metz, Lütfi Kerem Şenel, Maarten Bosma, Maarten Sap, Maartje ter Hoeve, Maheen Farooqi, Manaal Faruqui, Mantas Mazeika, Marco Baturan, Marco Marelli, Marco Maru, Maria Jose Ramírez Quintana, Marie Tolkiehn, Mario Giulianelli, Martha Lewis, Martin Potthast, Matthew L. Leavitt, Matthias Hagen, Mátyás Schubert, Medina Orduna Baitemirova, Melody Arnaud, Melvin McElrath, Michael A. Yee, Michael Cohen, Michael Gu, Michael Ivanitskiy, Michael Starritt, Michael Strube, Michał Swedrowski, Michele Bevilacqua, Michihiro Yasunaga, Mihir Kale, Mike Cain, Mimee Xu, Mirac Suzgun, Mo Tiwari, Mohit Bansal, Moin Aminnaseri, Mor Geva, Mozhdeh Gheini, Mukund Varma T, Nanyun Peng, Nathan Chi, Nayeon Lee, Neta Gur-Ari Krakover, Nicholas Cameron, Nicholas Roberts, Nick Doiron, Nikita Nangia, Niklas Deckers, Niklas Muennighoff, Nitish Shirish Keskar, Niveditha S. Iyer, Noah Constant, Noah Fiedel, Nuan Wen, Oliver Zhang, Omar Agha, Omar Elbaghdadi, Omer Levy, Owain Evans, Pablo Antonio Moreno Casares, Parth Doshi, Pascale Fung, Paul Pu Liang, Paul Vicol, Pegah Alipoormolabashi, Peiyuan Liao, Percy Liang, Peter Chang, Peter Eckersley, Phu Mon Htut, Pinyu Hwang, Piotr Miłkowski, Piyush Patil, Pouya Pezeshkpour, Priti Oli, Qiaozhu Mei, Qing Lyu, Qinlang Chen, Rabin Banjade, Rachel Etta Rudolph, Raefer Gabriel, Rahel Habacker, Ramón Risco Delgado, Raphaël Millière, Rhythm Garg, Richard Barnes, Rif A. Saurous, Riku Arakawa, Robbe Raymaekers, Robert Frank, Rohan Sikand, Roman Novak, Roman Sitelew, Ronan LeBras, Rosanne Liu, Rowan Jacobs, Rui Zhang, Ruslan Salakhutdinov, Ryan Chi, Ryan Lee, Ryan Stovall, Ryan Teehan, Rylan Yang, Sahib Singh, Saif M. Mohammad, Sajant Anand, Sam Dillavou, Sam Shleifer, Sam Wiseman, Samuel Gruetter, Samuel R. Bowman, Samuel S. Schoenholz, Sanghyun Han, Sanjeev Kwatra, Sarah A. Rous, Sarik Ghazarian, Sayan Ghosh, Sean Casey, Sebastian Bischoff, Sebastian Gehrmann, Sebastian Schuster, Sepideh Sadeghi, Shadi Hamdan, Sharon Zhou, Shashank Srivastava, Sherry Shi, Shikhar Singh, Shima Asaadi, Shixiang Shane Gu, Shubh Pachchigar, Shubham Toshniwal, Shyam Upadhyay, Shyamolima, Debnath, Siamak Shakeri, Simon Thormeyer, Simone Melzi, Siva Reddy, Sneha Priscilla Makini, Soo-Hwan Lee, Spencer Torene, Sriharsha Hatwar, Stanislas Dehaene, Stefan Divic, Stefano Ermon, Stella Biderman, Stephanie Lin, Stephen Prasad, Steven T. Piantadosi, Stuart M. Shieber, Summer Misherghi, Svetlana Kiritchenko, Swaroop Mishra, Tal Linzen, Tal Schuster, Tao Li, Tao Yu, Tariq Ali, Tatsu Hashimoto, Te-Lin Wu, Théo Desbordes, Theodore Rothschild, Thomas Phan, Tianle Wang, Tiberius Nkinyili, Timo Schick, Timofei Kornev, Timothy Telleen-Lawton, Titus Tunduny, Tobias Gerstenberg, Trenton Chang, Trishala Neeraj, Tushar Khot, Tyler Shultz, Uri Shaham, Vedant Misra, Vera Demberg, Victoria Nyamai, Vikas Raunak, Vinay Ramasesh, Vinay Uday Prabhu, Vishakh Padmakumar, Vivek Srikumar, William Fedus, William Saunders, William Zhang, Wout Vossen, Xiang Ren, Xiaoyu Tong, Xinran Zhao, Xinyi Wu, Xudong Shen, Yadollah Yaghoobzadeh, Yair Lakretz, Yangqiu Song, Yasaman Bahri, Yejin Choi, Yichi Yang, Yiding Hao, Yifu Chen, Yonatan Belinkov, Yu Hou, Yufang Hou, Yuntao Bai, Zachary Seid, Zhuoye Zhao, Zijian Wang, Zijie J. Wang, Zirui Wang, and Ziyi Wu. Beyond the imitation game: Quantifying and extrapolating the capabilities of language models, 2022.
- Sun et al. (2023) Mingjie Sun, Zhuang Liu, Anna Bair, and J. Zico Kolter. A simple and effective pruning approach for large language models, 2023.
- Tao et al. (2023) Chaofan Tao, Lu Hou, Haoli Bai, Jiansheng Wei, Xin Jiang, Qun Liu, Ping Luo, and Ngai Wong. Structured pruning for efficient generative pre-trained language models. In *Findings of the Association for Computational Linguistics: ACL 2023*, pp. 10880–10895, Toronto, Canada, July 2023. Association for Computational Linguistics. doi: 10.18653/v1/2023.findings-acl.692. URL [https://aclanthology.org/2023.findings-acl.692](https://aclanthology.org/2023.findings-acl.692).
- Touvron et al. (2023) Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, Aurelien Rodriguez, Armand Joulin, Edouard Grave, and Guillaume Lample. Llama: Open and efficient foundation language models, 2023.
- von Oswald et al. (2022) Johannes von Oswald, Eyvind Niklasson, Ettore Randazzo, João Sacramento, Alexander Mordvintsev, Andrey Zhmoginov, and Max Vladymyrov. Transformers learn in-context by gradient descent, 2022.
- Wang et al. (2023) Kevin Ro Wang, Alexandre Variengien, Arthur Conmy, Buck Shlegeris, and Jacob Steinhardt. Interpretability in the wild: a circuit for indirect object identification in GPT-2 small. In *The Eleventh International Conference on Learning Representations*, 2023. URL [https://openreview.net/forum?id=NpsVSN6o4ul](https://openreview.net/forum?id=NpsVSN6o4ul).
- Wei et al. (2022) Jason Wei, Yi Tay, Rishi Bommasani, Colin Raffel, Barret Zoph, Sebastian Borgeaud, Dani Yogatama, Maarten Bosma, Denny Zhou, Donald Metzler, Ed H. Chi, Tatsunori Hashimoto, Oriol Vinyals, Percy Liang, Jeff Dean, and William Fedus. Emergent abilities of large language models. *Transactions on Machine Learning Research*, 2022. ISSN 2835-8856. URL [https://openreview.net/forum?id=yzkSU5zdwD](https://openreview.net/forum?id=yzkSU5zdwD). Survey Certification.
- Yin et al. (2023) Lu Yin, Shiwei Liu, Ajay Jaiswal, Souvik Kundu, and Zhangyang Wang. Junk dna hypothesis: A task-centric angle of llm pre-trained weights through sparsity, 2023.
- Zhang et al. (2022) Susan Zhang, Stephen Roller, Naman Goyal, Mikel Artetxe, Moya Chen, Shuohui Chen, Christopher Dewan, Mona Diab, Xian Li, Xi Victoria Lin, Todor Mihaylov, Myle Ott, Sam Shleifer, Kurt Shuster, Daniel Simig, Punit Singh Koura, Anjali Sridhar, Tianlu Wang, and Luke Zettlemoyer. Opt: Open pre-trained transformer language models, 2022.

## Appendix A Limitation.

Overall, our study provides a valuable first step towards evaluating pruning algorithms for LLMs, as well as identifying limitations of a particular type of pruning approaches. We have validated our claims on a large number of benchmarks (a total of 8 tasks and 6 models). Since our work is empirical in nature, our observations may not generalize to the full spectrum of tasks and large language models (LLMs). In this study, we focused on evaluating pruning algorithms that scale to large-scale LLMs. This was a deliberate decision, as we believe that scalability is essential for any pruning algorithm to be widely adopted in the real world. More sophisticated one-shot/iterative pruning algorithms exist ([Renda et al., 2020](#bib.bib53)). They typically require re-training – redoing the training of these foundation models for every sparsity level we examine. The cost of such an experiment is at least in the millions of dollars therefore beyond our means.

## Appendix B Pruning Perplexity Eval

In [Table 2](#A2.T2 "In Appendix B Pruning Perplexity Eval ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning") we present the full range of pruning’s effect on the perplexity of models we consider in this work. We obtain perplexity results by running the pruned model on a randomly sampled subset of C4 validation set, following the precedent of [Frantar et al. (2023)](#bib.bib22).

|               |      |      |      |      |      |      |      |      |      |         |
|---------------|------|------|------|------|------|------|------|------|------|---------|
| Name/Sparsity | 0.0  | 10.0 | 20.0 | 30.0 | 40.0 | 50.0 | 60.0 | 70.0 | 80.0 | 90.0    |
| OPT-13B       | 11.5 | 11.5 | 11.6 | 11.6 | 11.9 | 12.4 | 13.7 | 17.8 | 45.3 | 40362.3 |
| OPT-30B       | 10.9 | 10.9 | 10.9 | 11.0 | 11.1 | 11.4 | 12.2 | 14.6 | 35.4 | 4187.5  |
| LLaMa-13B     | 6.6  | 6.6  | 6.7  | 6.8  | 7.1  | 7.8  | 10.0 | 20.0 | 59.9 | 822.1   |
| LLaMa-33B     | 5.9  | 6.0  | 6.0  | 6.1  | 6.4  | 7.0  | 8.5  | 13.7 | 36.1 | 355.9   |

Table 2: Pruning’s effect on perplexity.

Figure 6: Pruning’s effect on model perplexity.

## Appendix C Constructing Parameterized Functions in ICL Evaluation

While it may be unreasonable to expect the model to infer any arbitrary $f$, we focus on three natural classes of functions from which we pick $f$: the class of linear, 2-layered neural network, and decision tree models. These classes are defined as follows: (a) *Linear.* For each task instance, we generate a distinct random hyperplane in the $D$-dimensional input space as the decision boundary. We label each example as positive/negative depending on the side of the decision boundary it falls on. (b) *2-layer NN.* For each task instance, we generate a 2-layer neural network mapping a $D$-dimensional input vector $x$ to a binary label $y$ with the following form: $W_{2}\hspace{0pt}\sigma\hspace{0pt}{({W_{1}\hspace{0pt}x})}$, where $W_{1}$, $W_{2}$ are $D \times D$, $D \times 2$ matrices correspondingly. We draw elements within these two matrices from independent, Gaussian distributions with zero-mean and unit variance. We use ReLU as the activation function $\sigma$. (c) *Decision tree.* For each task instance, we construct a full depth-2 binary decision tree, with each of its four leaf nodes representing one possible label. This maps $D$-dimensional input vectors to the said labels. We assign each non-leaf node an index from 0 to $D - 1$. We evaluate the tree by traversing from the root, comparing the input vector’s value at each node’s associated index to determine the next step: if negative, we go left; if zero or positive, we go right. Reaching a leaf node marks the end of traversal, and the corresponding label represents the evaluation result.

## Appendix D Additional Details for ICL Evaluation Methodology

In this section, we provide additional details for our ICL task evaluation methodology.

#### In-context example label distribution.

When generating the ICL evaluation datasets, we programmatically enforce that the labels for the $N$ in-context demonstrations are split exactly evenly between K possible labels.

#### Evaluation label distribution.

Each evaluation input has an equal probability of receiving one of the $K$ possible classification labels. Therefore, evaluation label distribution should be even in expectation. However, we do not programmatically enforce an even distribution of evaluation labels.

#### Size of evaluation dataset.

We generate 2048 independent task instances for each function class. Each task instance represents a unique parameterization of the classification function to learn.

#### Prompting technique.

We do not use any advanced prompting technique when solving ICL tasks. The LLMs only generate answer tokens corresponding directly to classification labels. We do not generate any other tokens during evaluation.

#### Tokenizer.

The OPT models use a byte-pair encoding tokenizer whereas the LLaMA models use a sentence piece tokenizer. Notably, LLaMA tokenizers split each digit into an individual token. This feature of LLaMA tokenizers boosts LLaMA performance on arithmetic tasks ([Liu & Low, 2023](#bib.bib44)).

## Appendix E Increasing Input Dimension of ICL Evaluation

In this section, we further evaluate the effect of pruning on ICL tasks with different input dimensions.

#### Method.

In [Section 5](#S5 "5 More Sophisticated In-context Learning ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning"), we evaluate pruning’s effect on learning linear classification tasks in-context. The task is to classify 4-dimensional input vectors. Here, we increase the input vector dimensions to 8 and 16, and observe whether our observation about pruning’s effect generalize to larger input dimenions.

Figure 7: Pruning’s effect on ICL linear classification tasks with input dimension of 4, 8 and 16. We observe that even with increased input dimension, ICL ability of LLMs continue to be robust to aggresive pruning.

#### Results.

[Figure 7](#A5.F7 "In Method. ‣ Appendix E Increasing Input Dimension of ICL Evaluation ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning") presents the relationship between task accuracy and sparsity for linear classification task. We increase the input dimension from 4 to 8 and 16. We observe that tolerating the same 5% relative drop in the average accuracy among all four models with respect to the dense model, we can prune to 60%, 80% sparsity on linear classification task with 4, 8 dimensional inputs respectively. Dense models perform close to chance on 16-dimensional inputs, thus we refrain from drawing conclusions based on these results.

#### Conclusion.

Even with higher dimensional inputs, model’s ICL ability remains resilient to aggressive pruning ($> = 60\%$ sparsity).

## Appendix F Additional Pruning Algorithm Evaluation

In our main paper, we focus on a single pruning algorithm SparseGPT ([Frantar & Alistarh, 2023](#bib.bib21)). In this section, we study whether our observation that scaling down LLM size affects fact recall more readily than ICL generalize to another pruning algorithm.

#### Method.

We repeat key experiments with another pruning algorithm called Wanda ([Sun et al., 2023](#bib.bib56)). Notably, unlike SparseGPT, Wanda does not update the remaining weights after weights removal. The author of Wanda shows that at 50% sparsity, Wanda achieves accuracy that is competitive with SparseGPT.

#### Results.

We observe the same disparate effects from pruning on fact recall versus ICL: while moderate pruning hurts fact recall, ICL survives to higher sparsity. Specifically, accepting the same 5% relative drop in accuracy as we did for SparseGPT results, one may remove 30%, 40% and 50% weights on TriviaQA(Closebook), TriviaQA(Openbook) and Linear Classification tasks. Unsurprisingly, given that Wanda is computationally less expensive, it underperforms SparseGPT at high sparsities on ICL tasks.

#### Conclusion.

With our experiments repeated with another pruning algorithm, we show that our observation is general.

Figure 8: An alternative pruning algorithm (Wanda) shows the same patterns of accuracy drop as findings in our original paper: moderate pruning hurts fact recall (e.g., left, TriviaQA in Closebook setting) while ICL (e.g., right, in-context linear classification) survives to higher sparsity. Specifically, accepting a 5% relative drop in accuracy, one may remove 30%, 40% and 50% weights on TriviaQA(Closebook), TriviaQA(Openbook) and Linear Classification tasks, respectively.

## Appendix G Pythia Models Evaluation

Figure 9: Two variants of Pythia-12B model shows the same patterns of accuracy drop as findings in our original paper: moderate pruning hurts fact recall (e.g., left, TriviaQA in Closebook setting) while ICL (e.g., right, in-context linear classification) survives to higher sparsity. Specifically, accepting a 5% relative drop in average accuracy, one may remove 20%, 30% and 50% weights on TriviaQA(Closebook), TriviaQA(Openbook) and Linear Classification tasks, respectively.

In this section, we study whether our observation that scaling down LLM size affects fact recall more readily than ICL generalize to another model family: Pythia ([Biderman et al., 2023b](#bib.bib4)).

#### Method.

We repeat key experiments with Pythia model family. With SparseGPT, we pruned two variants of the Pythia-12B model, the original and a “deduped” variant where the model is trained on a deduplicated dataset. They’re the most capable models in the Pythia family.

#### Results.

shows consistent disparate effect of pruning on fact recall versus ICL. Specifically, accepting the same 5% accuracy drop as in all our results, one can remove 20%, 30% and 50% weights for TriviaQA(Closebook), TriviaQA(Openbook) and in-context linear classification tasks.

#### Conclusion.

Our observation is robust to the choice of model families.

## Appendix H Example Prompts

In this section, we present example prompts for Q&A tasks in [Section 4](#S4 "4 Effect of Pruning on Question Answering Tasks ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning") and ICL on algorithmic tasks in [Section 5](#S5 "5 More Sophisticated In-context Learning ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning").

### H.1 Question-answering without context.

Our prompt follows the precedent of [Touvron et al. (2023)](#bib.bib58). We show our prompt for Q/A tasks without context in [Figure 10](#A8.F10 "In H.1 Question-answering without context. ‣ Appendix H Example Prompts ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning").

Answer these questions: Q: In Scotland a bothy/bothie is a? A: House Q: Which 90s sci fi series with James Belushi was based on Bruce Wagner’s comic strip of the same name? A:

Figure 10: Examples Prompt for Question-answering Task without Context.

Answer these questions: Context: Scattered across the Highlands and rural areas of Scotland, a bothy is a small house that can be used by anyone. Q: In Scotland a bothy/bothie is a? A: House Context: ”Roses Are Red (My Love)” is a popular song composed by Al Byron and Paul Evans. It was recorded by Bobby Vinton and was his first hit. The song was released in April 1962. It reached No. 1 in Australia, New Zealand, Norway, the Philippines, South Africa, and the United States, and was a major hit in many other countries as well. The song topped the Billboard Hot 100 singles chart on July 14, 1962, and remained there for four weeks. The single was also the first number-one hit for Epic Records. Billboard ranked the record as the No. 4 song of 1962. Vinton found the song in a reject pile at Epic Records. He first recorded it as an R&B number, but was allowed to re-record it in a slower more dramatic arrangement, with strings and a vocal choir added. Ronnie Carroll version In the UK, a cover version by Ronnie Carroll reached No. 3 on the Record Retailer chart on August 8, 1962, the same week that the Bobby Vinton record peaked at No. 15. It peaked at No. 7 in the very first Irish Singles Chart published in October 1962. Other versions The song was recorded by Jim Reeves in 1963 and released on the album Gentleman Jim, one of the last albums released while he was still alive. While it did not chart in the US, it became a minor hit in Norway and Germany. The song was covered by Singaporean female artist Zhuang Xue Fang, in edited Standard Chinese lyrics written by Suyin under title name of, with Ruby Records in 1967. In 1962, an answer song, entitled ”Long As The Rose Is Red”, was recorded by Florraine Darlin. The song spent seven weeks on the Billboard Hot 100, reaching No. 62, while reaching No. 15 on Billboards Easy Listening chart. It was released by Epic Records (single \#9529) and was also produced by Robert Morgan. Charts Bobby Vinton version Ronnie Carroll version Q: Which singer had a big 60s No 1 with Roses Are Red? A:

Figure 11: Examples Prompt for Question-answering Task with Context.

### H.2 Question-answering with context.

We show an example prompt we use to evaluate Q/A task with the necessary information to answer the question available in-context in [Figure 11](#A8.F11 "In H.1 Question-answering without context. ‣ Appendix H Example Prompts ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning").

### H.3 ICL on algorithmic task.

We present the prompt we use to evaluate ICL on linear classification task in [Figure 12](#A8.F12 "In H.3 ICL on algorithmic task. ‣ Appendix H Example Prompts ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning"). Evaluations for ICL on check-sorting, check-even uses analogous prompts.

\[5, -5, -1, 6\] = -1 \[3, 5, -9, -2\] = 1 \[-10, 5, -9, -10\] = 1 \[7, 0, -4, -7\] = -1 \[-2, -2, 9, -3\] = -1 \[9, -5, -5, -1\] = -1 \[-4, -1, -10, -8\] = 1 \[-10, -1, -3, 6\] = -1 \[3, 6, -5, -8\] = 1 \[-1, 7, -2, 6\] = -1 \[-5, 8, -1, -9\] = 1 \[-6, -1, -6, -9\] = 1 \[1, 0, -10, -9\] = 1 \[-5, 5, -3, 6\] = -1 \[-4, 6, -10, -7\] = 1 \[-4, 5, -6, -10\] = 1 \[-10, 5, -3, -9\] = 1 \[-7, -2, -7, -9\] = 1 \[-7, 1, -7, 4\] = -1 \[-2, 2, -3, -10\] = 1 \[1, -4, -4, 9\] = -1 \[7, 0, 6, -10\] = -1 \[2, 7, -6, -1\] = 1 \[1, -2, -10, -9\] = 1 \[-8, 3, 7, -7\] = -1 \[0, 7, -3, -8\] = 1 \[0, 2, 0, 0\] = -1 \[-7, 9, 2, 8\] = -1 \[1, -8, -9, 6\] = -1 \[-5, 1, -6, -10\] = 1 \[8, 8, 1, -4\] = -1 \[-3, 6, 2, 2\] = -1 \[-3, 9, 0, -5\] =

Figure 12: Examples Prompt for ICL on Linear Classification Task.

## Appendix I Analysis on Accuracy Improvement

On many tasks, such as ICL on algorithmic tasks in [Section 5](#S5 "5 More Sophisticated In-context Learning ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning"), we observe accuracy improvement from pruning. In this section, we provide further analysis on this phenomenon.

#### Method.

We focus on the ICL task of check-sorting and check-even from [Section 5](#S5 "5 More Sophisticated In-context Learning ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning"), where the pruned LLaMA models see significant accuracy improvement. We analyze the prediction of the pruned model, in relation to the following two answers: 1). *Answer without context.* We compute the classification output with the highest log likelihood, without all the in-context examples. The prompt thus looks like ”\[1, 0, 3, -5\]=” without any other information such as in-context training examples. The LLM thus classifies this input array exclusively based on likelihood of a classification label as a continuation of the prompt. We denote this classification outcome as the answer without context. 2). *Ground-truth answer.*

#### Results.

In [Figure 13](#A9.F13 "In Conclusion. ‣ Appendix I Analysis on Accuracy Improvement ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning"), we present the percentage of time when the prediction of the pruned model matches the answer without context versus the ground truth. We observe that accuracy improvement often mirrors a departure of the model’s prediction from answer without context (the solid line dropping whilst the dashed line raising). This suggest that for some pruned models (for example LLaMA-30B at 60% sparsity), the presence of in-context examples changes the prediction of the LLM more than the dense models.

#### Conclusion.

We hypothesize, without testing, that pruning may improve task accuracy by enhancing the effect of contextual information on its prediction.

Figure 13: Analyzing the accuracy improvement of pruned model on ICL tasks.

## Appendix J Details on Computing Software/Hardware

We perform pruning on 80GB version of A100 GPUs, using the implementation of SparseGPT([Frantar & Alistarh, 2023](#bib.bib21)). We perform our evaluations using TPU v3 running PyTorch ([Paszke et al., 2019](#bib.bib52)) with XLA backend. Our research project consumes approximately 3 TPU-month worth of computation.

Our computing software/hardware necessitates the use of the bfloat16 numerical format. We assess its impact on our experimental results in [Appendix K](#A11 "Appendix K Characterizing Errors from Numerical Precision ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning").

## Appendix K Characterizing Errors from Numerical Precision

All our experiments run on TPU v3. The TPU hardware does not support float16 (IEEE 754 half precision floating point format), which are the formats used for training the OPT/LLaMA models. We thus use a closely related floating point format called bfloat16 (Brain Float) instead to evaluate these models. Both bfloat 16 and float16 are floating point numbers requiring 16 bits to represent, the key difference is that bfloat16 format can represent numbers in a slightly wider range of values, but with slightly reduced precision compared with float16. For this reason, we expect our results to contain small systematic errors. In this section, we characterize the difference between our results in bfloat16 and standard results in float16.

#### Perplexity and accuracy results.

In [Figure 14](#A11.F14 "In OPT. ‣ Appendix K Characterizing Errors from Numerical Precision ‣ The Cost of Down-Scaling Language Models: Fact Recall Deteriorates before In-Context Learning"), we plot the perplexity and accuracy in next token prediction in bfloat16 on TPU v3 and float16 on A100. We observe that the average accuracy difference is 1.0%, 0.89%, 0.70% and 0.68% for OPT-13B, OPT-30B, LLaMA-13B and LLaMA-33B. The perplexity grows to very large numbers at high sparsity, so we report the average perplexity difference for sparsity level less than or equal to 50%. The average perplexity difference is: 0.86, 0.69, 0.19, 0.13. We note that 1). the difference in accuracy and perplexity due to numerical precision is systematic. The accuracy of next token prediction raises by a similar amount across all sparsity levels. 2). the difference in next token prediction accuracy is small (¡1%).

#### OPT.

OPT models see higher difference in accuracy and perplexity. This is because its GPU implementation uses mixed precision arithmetic, where the attention score computes in float32. Our compiler and runtime, however, does not support mixed precision arithmetic, we therefore compute entirely within bfloat16.

Figure 14: Characterizing the difference between float16 and bfloat16.

Experimental support, please [view the build logs](./2310.04680v1/__stdout.txt) for errors. Generated by [ L A T E xml ![\[LOGO\]](img)](https://math.nist.gov/~BMiller/LaTeXML/) .

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
