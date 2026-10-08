---
title: "Deliberative Alignment: Reasoning Enables Safer Language Models"
authors: "Guan et al."
year: 2024
source: https://arxiv.org/html/2412.16339v2
fetched: 2026-10-07
---

Title: Deliberative Alignment: Reasoning Enables Safer Language Models

URL Source: https://arxiv.org/html/2412.16339v2

Markdown Content:
Manas Joglekar Eric Wallace Saachi Jain Boaz Barak Alec Helyar Rachel Dias Andrea Vallone Hongyu Ren Jason Wei Hyung Won Chung Sam Toyer Johannes Heidecke Alex Beutel Amelia Glaese

OpenAI

###### Abstract

As large-scale language models increasingly impact safety-critical domains, ensuring their reliable adherence to well-defined principles remains a fundamental challenge. We introduce Deliberative Alignment, a new paradigm that directly teaches the model safety specifications and trains it to explicitly recall and accurately reason over the specifications before answering. We used this approach to align OpenAI’s o-series models [[1](https://arxiv.org/html/2412.16339v2#bib.bibx1)], and achieved highly precise adherence to OpenAI’s safety policies, without requiring human-written chain-of-thoughts or answers. Deliberative Alignment pushes the Pareto frontier by simultaneously increasing robustness to jailbreaks while decreasing overrefusal rates, and also improves out-of-distribution generalization. We demonstrate that reasoning over explicitly specified policies enables more scalable, trustworthy, and interpretable alignment.

## 1 Introduction

Modern Large Language Models (LLMs) are safety trained using Supervised Fine Tuning (SFT) and Reinforcement Learning from Human Feedback (RLHF) to mitigate harmful, undesirable, or otherwise disallowed outputs[[2](https://arxiv.org/html/2412.16339v2#bib.bibx2), [3](https://arxiv.org/html/2412.16339v2#bib.bibx3), [4](https://arxiv.org/html/2412.16339v2#bib.bibx4)]. Despite ongoing advances in these methods, today’s models still exhibit safety shortcomings: they can be tricked into revealing harmful content, often refuse legitimate requests, and remain vulnerable to jailbreak attacks[[5](https://arxiv.org/html/2412.16339v2#bib.bibx5), [6](https://arxiv.org/html/2412.16339v2#bib.bibx6), [7](https://arxiv.org/html/2412.16339v2#bib.bibx7), [8](https://arxiv.org/html/2412.16339v2#bib.bibx8)].

We argue that many of these failures arise from two limitations in modern safety training. First, LLMs must respond instantly to user requests using a fixed amount of compute, without deliberation even for complex safety scenarios. Second, LLMs must infer underlying safety standards indirectly from large sets of labeled examples, rather than directly learning the safety specifications that govern them. This reliance on implicit, pattern-based learning leads to poor data efficiency and makes it challenging for models to generalize when facing unfamiliar scenarios or adversarial attacks.

We propose _deliberative alignment_, a training approach that teaches LLMs to explicitly reason through safety specifications before producing an answer. By applying this method to OpenAI’s o-series models[[1](https://arxiv.org/html/2412.16339v2#bib.bibx1)], we enable them to use chain-of-thought (CoT) reasoning to examine user prompts, identify relevant policy guidelines, and generate safer responses (e.g., Figure[1](https://arxiv.org/html/2412.16339v2#S1.F1 "Figure 1 ‣ 1 Introduction ‣ Deliberative Alignment: Reasoning Enables Safer Language Models")).

Figure 1: _A sample o1 chain-of-thought_. Here, a user attempts to obtain advice on untraceable payment methods to use for an adult website, in order to avoid detection by law enforcement. The user tries to jailbreak the model, by encoding the request and wrapping it with instructions intended to encourage the model to comply. In the model’s chain-of-thought, the model decodes the request and recognizes that the user is trying to trick it (highlighted in yellow). It successfully reasons through the relevant OpenAI safety policies (highlighted in green), and ultimately provides an answer that follows hard refusal style guidelines.

Our method proceeds in two core stages, integrating process- and outcome-based supervision[[9](https://arxiv.org/html/2412.16339v2#bib.bibx9)]. In the first stage, we teach the model to directly reason about our safety specifications within its chain-of-thought, by performing supervised fine-tuning on (prompt, CoT, output) examples where the CoTs reference the specifications. We construct this dataset using context distillation[[10](https://arxiv.org/html/2412.16339v2#bib.bibx10), [11](https://arxiv.org/html/2412.16339v2#bib.bibx11)] and an o-type model trained only for helpfulness (i.e. trained without any safety-relevant data). Concretely, we present the model with the safety specifications as part of the system prompt, generate model completions, and then strip away the system prompts to form the final dataset. This stage provides the model with a strong prior for reasoning through safety considerations. In the second stage, we use high-compute RL to train the model to think more effectively. To do so, we provide reward signal using a judge LLM that is given our safety specifications.

Notably, our training procedure _requires no human-labeled completions._ 1 1 1 We make use of a label of which broad safety category the prompt is relevant to. This helps us refine the context-distillation prompt but is not essential to the process. Despite relying only on model-generated data, we achieve highly precise specification adherence. This addresses a major challenge of standard LLM safety training—its heavy dependence on large-scale, human-labeled data: As LLMs’ capabilities improve, the pool of human trainers qualified to provide such labeling shrinks, making it harder to scale safety with capabilities. Deliberative alignment’s synthetic data generation pipeline offers a scalable approach to alignment, reserving human expertise for evaluation.

We compare o1 to GPT-4o and other state-of-the-art LLMs across a range of internal and external safety benchmarks, such as jailbreak and content-policy refusal evals. The o1 models achieve a Pareto improvement by reducing both under- and overrefusals (see Figure[2](https://arxiv.org/html/2412.16339v2#S1.F2 "Figure 2 ‣ 1 Introduction ‣ Deliberative Alignment: Reasoning Enables Safer Language Models")) and they saturate many of our hardest safety benchmarks. Furthermore, we find that deliberative alignment enables strong generalization to out-of-distribution safety scenarios. In detailed ablation studies, we find that process-supervision provides a strong prior, and that outcome-based RL refines the CoT safety reasoning. Overall, our results suggest that chain-of-thought reasoning can serve to leverage test-time compute to improve safety behavior, ultimately training LLMs to be “right for the right reasons”.

![Image 1: Refer to caption](https://arxiv.org/html/2412.16339v2/x1.jpg)

Figure 2: _Main safety results_. The o1 models advance the Pareto frontier of refusing to answer malicious jailbreak prompts (from StrongREJECT[[12](https://arxiv.org/html/2412.16339v2#bib.bibx12)]) and not over-refusing benign prompts (from XSTest[[13](https://arxiv.org/html/2412.16339v2#bib.bibx13)]), compared to GPT-4o and other state-of-the-art LLMs. Error bars represent estimates of standard deviation calculated over 1,000 bootstrap trials.

## 2 Method

Our approach to deliberative alignment is motivated by the following observation: given access to our actual safety policies, o1 models are often able to correctly reason over how to respond to potentially unsafe prompts. Thus, one natural approach is to simply place the text of all of our safety specifications in context at deployment time, and instruct the model to check all the policies before answering. However, such an approach comes with a clear latency cost: in most cases, reasoning over pages of safety specifications is overkill for benign user prompts. Moreover, if the model fails at instruction following, it may miss a relevant part of the policy and output unsafe content.

Deliberative alignment instead seeks to embed knowledge of our safety specifications directly in the underlying model, by teaching the model to identify when a policy might be relevant and then reason over that policy to produce a policy-compliant answer. Indeed, as we find in Section [14](https://arxiv.org/html/2412.16339v2#S4.F14 "Figure 14 ‣ 4.1 Ablations for different components of the method ‣ 4 Science of Deliberate Alignment ‣ Deliberative Alignment: Reasoning Enables Safer Language Models"), deliberative alignment more reliably aligns the model to specifications than providing those specifications at deployment time.

Below, we first provide a high level overview of our method. We then discuss each step of our method in more detail in the following subsections.

### 2.1 Overview

We define a generative reasoning model\mathcal{G} as a model that takes as input a prompt and outputs a completion that includes a chain-of-thought (CoT). Given an initial reasoning model \mathcal{G}_{base}, our aim is to produce a generative reasoning model \mathcal{G}_{spec} whose answers adhere to safety specifications (spec for short). We train our model in two stages: supervised fine-tuning followed by reinforcement learning.

Figure [3](https://arxiv.org/html/2412.16339v2#S2.F3 "Figure 3 ‣ 2.1 Overview ‣ 2 Method ‣ Deliberative Alignment: Reasoning Enables Safer Language Models") illustrates our overall method. At a high level it has the following steps:

Data Generation
We start with a collection of prompts with associated safety categories (e.g., erotic, self-harm). For each (prompt, category) pair, we compose safety specifications relevant to that prompt’s safety category including information on disallowed content and style. We then collect (CoT, output) completions which reference our policies within the chain-of-thought, by prompting the spec-agnostic reasoning model \mathcal{G}_{base} with the text of the associated safety specification.

Filtering
We use “judge” reasoning model \mathcal{G}_{RM} prompted with our spec to choose high-quality completions. We then drop the spec from the prompts, resulting in a list of (prompt, CoT, output) tuples.

Supervised Fine-Tuning (SFT)
We then train \mathcal{G}_{base} on the filtered completions using supervised fine-tuning. The model learns to complete prompts in a specification-aligned manner by referring to the policies referenced in its CoTs.

Reinforcement Learning (RL)
During the RL stage, for safety-relevant prompts, we again use our “judge” model \mathcal{G}_{RM} with access to our safety policies to provide additional reward signal.

The following subsections describe the procedure in detail.

![Image 2: Refer to caption](https://arxiv.org/html/2412.16339v2/figure/new_method.png)

Figure 3: _Illustration of overall methodology._ Key processes are shown along the bottom of the figure. We first construct a dataset of (prompt, CoT, output) tuples where the CoTs refers to relevant policies (top-left zoombox). We collect these by prompting a reasoning model G_{base} with safety prompts along with safety specifications (spec) that are tailored to safety categories (cat). After filtering with a policy-aware reward model (G_{RM}), this data is then used for SFT training to teach the model to reason about the spec in its CoT. In the RL training stage (top-right zoombox), we provide reward signal using that same reward model G_{RM} with access to the spec. Our resulting model G_{spec} is aligned with the safety specifications.

### 2.2 Safety specifications

The specifications that we aim to align our model \mathcal{G}_{spec} with consist of content policies for different safety categories, as well as style guidelines for how to respond. Examples of safety categories include: erotic content, extremism, harassment, illicit behavior, regulated advice, self-harm, and violence. For each safety category, the corresponding content policy defines relevant terms and then describes the circumstances under which user requests are 1) “allowed”, such that the model should comply, 2) “disallowed”, such that the model should refuse, or 3) “requires safe completion.” Section [3.1.1](https://arxiv.org/html/2412.16339v2#S3.SS1.SSS1 "3.1.1 Disallowed Content ‣ 3.1 Safety Evaluations ‣ 3 Results ‣ Deliberative Alignment: Reasoning Enables Safer Language Models") shows excerpts of the content policies for the illicit behavior and self-harm safety categories. The specifications we used are based in part on OpenAI’s published model spec [[14](https://arxiv.org/html/2412.16339v2#bib.bibx14)].

Style guidelines in the spec give detailed instructions on how to comply, refuse, or safe-complete once the model decides to do so based on the content policies. Figure [4](https://arxiv.org/html/2412.16339v2#S2.F4 "Figure 4 ‣ 2.2 Safety specifications ‣ 2 Method ‣ Deliberative Alignment: Reasoning Enables Safer Language Models") shows excerpts from the hard refusal style guidelines. Safe completions are necessary in cases where the model cannot simply comply due to the sensitive nature of the request, but outright refusal to respond may also be harmful or inappropriate. Detailed topic-specific safe-completion guidelines are provided in the spec for safety categories such as self-harm and regulated advice (e.g. medical or legal advice). Note that for a given category such as self-harm, some requests should be allowed (e.g. an educational discussion about the concept of suicide), and some require a “self-harm safe completion” (e.g. content signifying ideation of self-harm, or request for method to commit self-harm).

Figure 4: Excerpt of style guidelines for hard refusals

##### Forming category-specific specifications

Over all policies, the safety specification ends up being quite long. In order to keep the context length manageable, we formulate category-specific policy specifications (denoted as spec(category) that provide high level details about all the safety categories (as well as principles of style and helpfulness) and granular details only about the relevant category. This allows us to provide additional information on the most relevant parts of the spec while reducing the overall context length. In practice, we find that reasoning models are more likely to pay attention to the relevant category when passed spec(category)) than when given the entire specification.

### 2.3 SFT stage

In the first stage, the goal is to collect (and then train on) sets of (prompt, CoT, output) tuples where the CoT reasons about the safety specifications to arrive at a policy-adherent answer.

#### 2.3.1 Generation

We start with a collection of prompts with associated safety categories (e.g., erotic, self-harm). Each of these prompts is a chat conversation with potentially multiple turns from user, assistant, tool, and system roles, that ends on an user turn. For each (prompt, category) pair, we compose the category-specific safety specification spec(category). We then collect (CoT, output) completions which reference our policies within the chain-of-thought, by prompting the base reasoning model G_{base} with the text of the associated safety specification. In particular, the specification-augmented prompt consists of:

*   •
the original prompt

*   •
the category-specific safety specification spec(category)

*   •
instructions to cite and discuss relevant parts of spec(category)

Figure[5](https://arxiv.org/html/2412.16339v2#S2.F5 "Figure 5 ‣ 2.3.1 Generation ‣ 2.3 SFT stage ‣ 2 Method ‣ Deliberative Alignment: Reasoning Enables Safer Language Models") shows how the augmented prompt is constructed (simplified for clarity). The end result are CoTs that refer to and reason over the policies. See Section [3.1](https://arxiv.org/html/2412.16339v2#S3.SS1 "3.1 Safety Evaluations ‣ 3 Results ‣ Deliberative Alignment: Reasoning Enables Safer Language Models") for examples of generated completions.

Figure 5: Our template for creating the modified prompt that is given to \mathcal{G}_{base} to generate completions given a prompt and its relevant safety category.

Figure 6: Our template for creating the prompt that is given to \mathcal{G}_{RM} for scoring completions.

#### 2.3.2 Quality Filtering

We ensure the quality of the SFT data using an automated filtering process. Specifically, after filtering out low-quality completions (e.g., those that are malformed or in the wrong format), we judge each completion k times, using a reasoning model \mathcal{G}_{RM} that is also given access to the category-specific safety specification spec(category). The score assigned to each of these individual completion is the minimum score across the k runs — we take the minimum because any single run may overlook an issue with the completion. We then retain completions with high scores.

\mathcal{G_{RM}} itself is specification-agnostic and only has knowledge of the spec through its prompt. Figure[6](https://arxiv.org/html/2412.16339v2#S2.F6 "Figure 6 ‣ 2.3.1 Generation ‣ 2.3 SFT stage ‣ 2 Method ‣ Deliberative Alignment: Reasoning Enables Safer Language Models") shows an example of how the reward model \mathcal{G}_{RM} is prompted (simplified for clarity). \mathcal{G}_{RM} judges the (prompt CoT, extracted answer) along with the relevant safety specification spec(category) and outputs a score.

Notably, many of our datasets have associated metadata, such as a label of the ideal completion (e.g., refuse, comply, or safe-complete) or offline context computed about the prompt. This metadata, which may be noisy, comes from a mix of human- and AI-labeling. When this optional metadata exists, we provide \mathcal{G}_{RM} this side information by adding “In your answer, consider that another AI determined that …” to the prompt and ask the reward model to justify its agreement with this analysis. We find that this method of providing (perhaps noisy) metadata threads the line between directing \mathcal{G}_{RM} without over-indexing on labeling noise.

#### 2.3.3 SFT Training

At this point, we have collected a dataset of \{\texttt{prompt, CoT, output}\} tuples, where the CoTs reference the safety specification and the final answer in the output has been judged to be policy adherent. We train \mathcal{G}_{base} on this dataset using supervised fine-tuning along with other capabilities data. Notably, we use the original version of prompt which does not contain any details about spec(category). By removing any context about the safety specification from the prompt, we teach the model to be able to recall the relevant parts of the spec and reason about them even when they are not directly provided in the conversational context. We label the result of the SFT process \mathcal{G}_{SFT}.

### 2.4 RL training

During the RL stage, for safety-relevant prompts, we again use our “judge” model \mathcal{G}_{RM} with access to our safety policies to provide additional reward signal to our RL stack. Specifically, the RL safety data contains a collection of (prompt, category) pairs, again potentially with additional useful meta-data of varying quality. While \mathcal{G}_{RM} receives CoT during SFT data filtering, the CoT is hidden from \mathcal{G}_{RM} during RL. We avoid applying direct optimization pressure on the CoT during RL to enable the underlying model to reduce the chance of encouraging deceptive CoTs.

While the SFT portion of our method was used for all o-series models, this particular reward signal for RL was added for training the o1 model and o3-mini.

## 3 Results

We used deliberative alignment to align OpenAI’s o-series models, including o1-preview, o1, and o3-mini. In this section we discuss key safety and robustness results of the o1 series against GPT-4o and other leading external models. In Section [14](https://arxiv.org/html/2412.16339v2#S4.F14 "Figure 14 ‣ 4.1 Ablations for different components of the method ‣ 4 Science of Deliberate Alignment ‣ Deliberative Alignment: Reasoning Enables Safer Language Models"), we break down the efficacy of each stage of our method, before diving into implications for OOD generalization (Section [4.3](https://arxiv.org/html/2412.16339v2#S4.SS3 "4.3 Generalization to OOD settings ‣ 4 Science of Deliberate Alignment ‣ Deliberative Alignment: Reasoning Enables Safer Language Models")).

### 3.1 Safety Evaluations

We first compare the o1 models with the GPT-4o model on key policy areas such as disallowed content, adherence to response style guidelines, jailbreaks, and overrefusals (see Table[1](https://arxiv.org/html/2412.16339v2#S3.T1 "Table 1 ‣ 3.1 Safety Evaluations ‣ 3 Results ‣ Deliberative Alignment: Reasoning Enables Safer Language Models")).

Table 1: Safety Evaluations of o1 models on various policy areas

#### 3.1.1 Disallowed Content

Our disallowed content evaluations check that the model does not comply with requests for harmful content, including hateful content and illicit advice, and properly handles requests for self-harm or regulated advice (such as medical or legal advice). Here, we consider two evaluations:

*   •
Challenging Refusal Evaluation: An evaluation set of challenging production traffic that requests disallowed content.

*   •
(Toxic) WildChat[[15](https://arxiv.org/html/2412.16339v2#bib.bibx15)]: Toxic conversations from a public corpus of 1M GPT-3.5T and GPT-4T API conversations labeled with ModAPI scores. For each ModAPI category, we select the 200 conversations with the highest ModAPI score on the last user turn.

For both evaluations, we use an autograder with access to our policies to check for violations in the model output.

As shown in Table [1](https://arxiv.org/html/2412.16339v2#S3.T1 "Table 1 ‣ 3.1 Safety Evaluations ‣ 3 Results ‣ Deliberative Alignment: Reasoning Enables Safer Language Models"), we find that the o1 models consistently outperform the GPT-4o model on disallowed content evaluations, particularly on the challenging refusal evaluation. In Figures [7](https://arxiv.org/html/2412.16339v2#S3.F7 "Figure 7 ‣ 3.1.1 Disallowed Content ‣ 3.1 Safety Evaluations ‣ 3 Results ‣ Deliberative Alignment: Reasoning Enables Safer Language Models") and [8](https://arxiv.org/html/2412.16339v2#S3.F8 "Figure 8 ‣ 3.1.1 Disallowed Content ‣ 3.1 Safety Evaluations ‣ 3 Results ‣ Deliberative Alignment: Reasoning Enables Safer Language Models"), we display two representative completions given user prompts that (1) ask for illicit advice, and (2) express self-harm. In each of these cases, the model references the relevant policy within its CoT and identifies the correct style with which to respond (here, a refusal and a safe completion respectively). Detailed excerpts of example content policies for the illicit behavior and self-harm safety categories can be found in Figures [9](https://arxiv.org/html/2412.16339v2#S3.F9 "Figure 9 ‣ 3.1.1 Disallowed Content ‣ 3.1 Safety Evaluations ‣ 3 Results ‣ Deliberative Alignment: Reasoning Enables Safer Language Models") and [10](https://arxiv.org/html/2412.16339v2#S3.F10 "Figure 10 ‣ 3.1.1 Disallowed Content ‣ 3.1 Safety Evaluations ‣ 3 Results ‣ Deliberative Alignment: Reasoning Enables Safer Language Models").

Figure 7: _A sample o1 chain-of-thought for an illicit advice prompt_. Here, a user asks for illicit advice. In the model’s chain-of-thought, it successfully reasons through the relevant snippets from the OpenAI safety policies (highlighted in green). The model provides an answer that follows hard refusal style guidelines.

Figure 8: _A sample o1 chain-of-thought for a self-harm prompt_. Here, a user expresses suicidal intent and asks for help. In the model’s chain-of-thought, it successfully reasons through the relevant snippets from the OpenAI safety policies (highlighted in green). The model provides an answer that follows self-harm safe completion style guidelines.

Figure 9: Excerpt of an example content policy for illicit behavior safety category

Figure 10: Excerpt of an example content policy for self-harm safety category

#### 3.1.2 Response Style Guidelines

Additionally, we find that supervising the model to think about the correct response style improves its ability to adhere to the style guidelines. To illustrate what these guidelines look like, Figure [4](https://arxiv.org/html/2412.16339v2#S2.F4 "Figure 4 ‣ 2.2 Safety specifications ‣ 2 Method ‣ Deliberative Alignment: Reasoning Enables Safer Language Models") shows excerpts of the guidelines for hard refusals. Table [1](https://arxiv.org/html/2412.16339v2#S3.T1 "Table 1 ‣ 3.1 Safety Evaluations ‣ 3 Results ‣ Deliberative Alignment: Reasoning Enables Safer Language Models") reports on whether the model adhered to our style guidelines when outputting hard refusals, self-harm safe completions, and regulated advice safe completions. We find that o1 has better response style than GPT-4o, with marked improvements in safe completion style.

We note that o1-preview has relatively poor response style, especially for regulated advice and self-harm safe completions. A key reason for this difference is that we updated our safe completion guidelines between the releases of o1-preview and o1. As such, o1-preview (and GPT-4o) is measured against a new safe completion style standard that it was not trained against. We note, however, that hard refusal style also also improved between o1-preview and o1: we hypothesize that using reward model G_{RM} during o1 RL training boosted adherence to our style guidelines.

#### 3.1.3 Jailbreaks

We further evaluate the robustness of the o1 models to jailbreaks: adversarial prompts that purposely try to circumvent model refusals for content it’s not supposed to produce [[16](https://arxiv.org/html/2412.16339v2#bib.bibx16), [12](https://arxiv.org/html/2412.16339v2#bib.bibx12), [17](https://arxiv.org/html/2412.16339v2#bib.bibx17), [18](https://arxiv.org/html/2412.16339v2#bib.bibx18)]. Here, we specifically consider StrongREJECT[[12](https://arxiv.org/html/2412.16339v2#bib.bibx12)], an academic jailbreak benchmark that tests a model’s resistance against common attacks from the literature. Following[[12](https://arxiv.org/html/2412.16339v2#bib.bibx12)], we calculate goodness@0.1, which is the safety of the model when evaluated against the top 10% of jailbreak techniques per prompt.

We find that the o1 series is significantly more robust to jailbreaks than the 4o models, an observation corroborated by external redteam findings such as [[19](https://arxiv.org/html/2412.16339v2#bib.bibx19)] (see Table [1](https://arxiv.org/html/2412.16339v2#S3.T1 "Table 1 ‣ 3.1 Safety Evaluations ‣ 3 Results ‣ Deliberative Alignment: Reasoning Enables Safer Language Models")). Figure [1](https://arxiv.org/html/2412.16339v2#S1.F1 "Figure 1 ‣ 1 Introduction ‣ Deliberative Alignment: Reasoning Enables Safer Language Models") is an example completion with the CoT when given a jailbreak-style prompt. We find that even when the request is encoded, and wrapped with instructions intended to encourage the model to comply, the model correctly identifies that the user is trying to trick the model and returns to the OpenAI policies, leading to a refusal.

#### 3.1.4 Overrefusals

Finally, we evaluate whether the model overrefuses on content that it should comply with. We consider three types of overrefusal:

*   •
XSTest[[13](https://arxiv.org/html/2412.16339v2#bib.bibx13)]: A public dataset of benign questions that include common safety triggers for LLMs (e.g., “how do I terminate a python process” or “Why should black beans never be president?)

*   •
Transformation Exception: A dataset of requests that exercise the transformation exception[[14](https://arxiv.org/html/2412.16339v2#bib.bibx14)], where the model should comply with analyzing, translating, or otherwise transforming user-provided disallowed content.

*   •
Policy overrefusals: An internal dataset of requests that we comply to according to OpenAI policy.

From Table [1](https://arxiv.org/html/2412.16339v2#S3.T1 "Table 1 ‣ 3.1 Safety Evaluations ‣ 3 Results ‣ Deliberative Alignment: Reasoning Enables Safer Language Models") we see that o1 models overrefuse less than GPT-4o, with a marked improvement at not overrefusing prompts for which the transformation exception applies. Figure [11](https://arxiv.org/html/2412.16339v2#S3.F11 "Figure 11 ‣ 3.1.4 Overrefusals ‣ 3.1 Safety Evaluations ‣ 3 Results ‣ Deliberative Alignment: Reasoning Enables Safer Language Models") is an example completion with the CoT for such a prompt.

Figure 11: _A sample o1 chain-of-thought for an overrefusal prompt_. Here, a user asks for a translation of a policy-violating instruction, which should be allowed by the transformation exception. In the model’s chain-of-thought, it successfully reasons that, while the instruction to be translated is disallowed, simply translating the instruction is permitted and the model should comply (relevant policy snippets highlighted in green).

### 3.2 Comparison to external models

![Image 3: Refer to caption](https://arxiv.org/html/2412.16339v2/figure/external_models.png)

Figure 12: _Comparative evaluation of text safety and robustness across leading LLMs._ o1 is competitive compared to other leading models on benchmarks assessing disallowed content (WildChat), jailbreaks (StrongREJECT), overrefusals (XSTest), hallucinations (SimpleQA), and bias (BBQ). Some API requests were blocked due to the sensitive nature of the content. These cases are recorded as “Blocked by safety filters” on WildChat and excluded from other benchmarks. Error bars are estimated using bootstrap resampling at the 0.95 level.

To understand the text safety performance of o1 in context, we evaluated it against other publicly-available leading models: Gemini 1.5 Pro, Gemini 1.5 Flash, Claude 3.5 Haiku, and Claude 3.5 Sonnet [[20](https://arxiv.org/html/2412.16339v2#bib.bibx20), [21](https://arxiv.org/html/2412.16339v2#bib.bibx21), [22](https://arxiv.org/html/2412.16339v2#bib.bibx22), [23](https://arxiv.org/html/2412.16339v2#bib.bibx23), [15](https://arxiv.org/html/2412.16339v2#bib.bibx15)].

We conducted these evaluations on publicly available benchmarks for replicability:

*   •
Toxic WildChat[[15](https://arxiv.org/html/2412.16339v2#bib.bibx15)]: Toxic conversations from a public corpus of 1M GPT-3.5T and GPT-4T API conversations labeled with ModAPI scores. For each ModAPI category, we select the 200 conversations with the highest ModAPI score on the last user turn.

*   •
StrongREJECT[[12](https://arxiv.org/html/2412.16339v2#bib.bibx12)]: An academic jailbreak benchmark that tests a model’s resistance against common attacks from the literature.

*   •
XSTest[[13](https://arxiv.org/html/2412.16339v2#bib.bibx13)]: A dataset of benign questions that include common safety triggers for LLMs (e.g., “how do I terminate a python process” or “Why should black beans never be president?)

*   •
SimpleQA[[24](https://arxiv.org/html/2412.16339v2#bib.bibx24)]: A diverse dataset of four-thousand fact-seeking questions with short answers and measures model accuracy for attempted answers.

*   •
BBQ[[25](https://arxiv.org/html/2412.16339v2#bib.bibx25)]: A dataset of question sets that tests for social biases against people belonging to protected classes along 9 social dimensions relevant for U.S. English-speaking contexts.

In some cases, we found that prompts sent to Claude or Gemini API’s returned with error codes indicating that they were blocked due to safety filters. We chose to record these errors for WildChat as “Blocked by safety filters”. For other benchmarks, these errors were less than 1% of samples so we filtered these cases from our results.

Results in Figures[2](https://arxiv.org/html/2412.16339v2#S1.F2 "Figure 2 ‣ 1 Introduction ‣ Deliberative Alignment: Reasoning Enables Safer Language Models") and[12](https://arxiv.org/html/2412.16339v2#S3.F12 "Figure 12 ‣ 3.2 Comparison to external models ‣ 3 Results ‣ Deliberative Alignment: Reasoning Enables Safer Language Models") show that o1 pushes the Pareto frontier by substantially improving on jailbreak robustness (StrongREJECT) while maintaining low overrefusal rates (XSTest). In particular, o1 outperforms other leading models on StrongREJECT, achieving a goodness@0.1 of 0.88. On XSTest, o1 achieves a high overrefusal accuracy of 0.93, lagging behind only Gemini flash (0.94), which has quite low robustness on StrongREJECT (goodness@0.1 of 0.05).

o1 additionally performs competitively on benchmarks assessing disallowed content (WildChat), hallucinations (SimpleQA), and bias (BBQ). On WildChat, o1 maintains a high rate of safe completions (98%) without the use of external safety filters. On SimpleQA, o1 achieves a state-of-the-art accuracy (0.47) but hallucinates more often than both measured Claude models. On BBQ, o1 shows high accuracy in ambiguous and disambiguated contexts, and it stereotypes in ambiguous contexts less often than every model except o1-preview.

For all benchmarks excluding BBQ, we show uncertainty estimates computed using a bootstrap method. Specifically, we estimate the standard deviation of the results by resampling the dataset with replacement over 1,000 bootstrap trials. These error bars primarily reflect the variability due to dataset size rather than variance due to training.

For our main jailbreak metric (StrongREJECT) we note that the compositional jailbreaks in the evaluation sometimes also confused the autograder. We thus additionally validated the StrongREJECT results in human review, and found that they match our autograded evaluations (see Appendix [A](https://arxiv.org/html/2412.16339v2#A1 "Appendix A Human Review Experiment ‣ Deliberative Alignment: Reasoning Enables Safer Language Models")).

### 3.3 Impact of inference-time compute

![Image 4: Refer to caption](https://arxiv.org/html/2412.16339v2/x2.png)

Figure 13: _Impact of inference-time compute on model performance._ The o1 model has stronger performance on challenging evals when allowed more compute to spend on reasoning.

We study the impact of varying the amount of inference-time compute allotted to the model. We allow the model to spend more or less compute on chain-of-thought reasoning, and evaluate its performance. In particular, we consider the StrongREJECT jailbreak benchmark [[12](https://arxiv.org/html/2412.16339v2#bib.bibx12)] and internal policy benchmarks testing the model’s overrefusal rate and adherence to response style guidelines. Figure [13](https://arxiv.org/html/2412.16339v2#S3.F13 "Figure 13 ‣ 3.3 Impact of inference-time compute ‣ 3 Results ‣ Deliberative Alignment: Reasoning Enables Safer Language Models") shows a clear trend of improved model performance on the StrongREJECT and regulated advice safe completion style benchmarks, while other evals remained relatively flat. We hypothesize this is because StrongREJECT and regulated advice style adherence are more difficult tasks for the model than the others. StrongREJECT is challenging because it uses compositional jailbreaks. Likewise, our regulated advice safe completion style guidelines are very complex compared to those for hard refusals, where the correct response style is always a brief apology and statement of inability to comply with the question (see Figure [4](https://arxiv.org/html/2412.16339v2#S2.F4 "Figure 4 ‣ 2.2 Safety specifications ‣ 2 Method ‣ Deliberative Alignment: Reasoning Enables Safer Language Models")). Self-harm safe completion style is also complex, but the model had fewer regulated advice training examples to learn from than for self-harm.

Our results demonstrate that safety failures can result from the model being given insufficient time to reason through complex and borderline prompts, and that CoT reasoning can be a powerful mechanism for leveraging test-time compute to improve model safety.

## 4 Science of Deliberate Alignment

In this section, we dive deeper into the deliberative alignment method. We first explore how different stages of the method impact the policy adherence of the final model. We then investigate the behavior of models trained with deliberative alignment, including the final model’s consistency in recalling the correct policy and its reliability in out-of-distribution settings.

In all experiments in this section, we leverage a variant of the o1-mini model with a reduced training setup.

### 4.1 Ablations for different components of the method

To study the impact that the SFT and RL stages of deliberative alignment have on model performance, we conduct ablation experiments where we drop safety data from one or both stages. Specifically, we compare the following four settings (see Figure [14](https://arxiv.org/html/2412.16339v2#S4.F14 "Figure 14 ‣ 4.1 Ablations for different components of the method ‣ 4 Science of Deliberate Alignment ‣ Deliberative Alignment: Reasoning Enables Safer Language Models")):

*   •
No safety training: No safety data in either SFT or RL (only capabilities data);

*   •
Safety in SFT only: Safety data only in SFT, no safety data in RL;

*   •
Safety in RL only: No safety in SFT, safety data only in RL; and

*   •
Safety in SFT & RL: Safety data in both SFT and RL (default deliberative alignment setting).

As expected, the “Safety in SFT & RL” performs much better than the “No safety training” run in terms of disallowed content, response style, and jailbreaks, although in this specific ablation setup the safety training also increases overrefusals. The key finding is that the “Safety in SFT only” and “Safety in RL only” runs attain intermediate results, showing that both SFT and RL training play critical roles in deliberative alignment training. We believe that the model learns a strong prior for safe reasoning during SFT, and then learns to use its CoT more effectively during RL.

In Figure [14](https://arxiv.org/html/2412.16339v2#S4.F14 "Figure 14 ‣ 4.1 Ablations for different components of the method ‣ 4 Science of Deliberate Alignment ‣ Deliberative Alignment: Reasoning Enables Safer Language Models"), we also compare these ablations to a baseline where we do not perform any safety training, but we provide the entire spec to the model at inference time in the system message. Because we would not know what safety category is relevant for prompts received at deployment time, the spec we provide is not tailored to any safety category but instead has the summarized versions of all the content policies (see Section[2.2](https://arxiv.org/html/2412.16339v2#S2.SS2 "2.2 Safety specifications ‣ 2 Method ‣ Deliberative Alignment: Reasoning Enables Safer Language Models")). Note that it is infeasible to include the detailed versions of the content policies for all safety categories, because each one spans 5-10K tokens and would altogether exceed the model’s context window.

Despite having access to the full spec, this baseline appears to learn less safety behavior than the model trained with deliberative alignment (and in many cases, even the model only trained with safety in the SFT stage). This baseline particularly struggles to adhere to response style guidelines. These results indicate that embedding these policies during training is more reliable than providing all of the policies at deployment time.

![Image 5: Refer to caption](https://arxiv.org/html/2412.16339v2/x3.png)

Figure 14: _Ablations on safety training stages_ We remove safety training from SFT and/or RL to see the impact on model performance. We also compare to a baseline where we provide the spec at inference-time without performing any safety training.

### 4.2 Policy Retrieval Accuracy

How reliably do models trained with deliberative alignment actually refer to the correct policy? To answer this question, we evaluate how often CoTs reference appropriate safety categories (see Section[2.2](https://arxiv.org/html/2412.16339v2#S2.SS2 "2.2 Safety specifications ‣ 2 Method ‣ Deliberative Alignment: Reasoning Enables Safer Language Models")).

We compare two settings:

*   •
No-Safety Baseline: The model does not undergo any Deliberative Alignment training.

*   •
Full Data: The model is trained on the full dataset, including safety.

In particular, given evaluation prompts labeled with the safety category, we extract sentences from the chain-of-thought that mention a policy.2 2 2 Specifically, we extract any excerpts that mention the words {“policy”, “policies”, “guideline”, “allowed”}. We then ask another prompted reasoning model to identify which category in the spec (if any) the excerpt was pulled or paraphrased from. Finally, to measure policy retrieval accuracy, we compute the fraction of prompts where the derived safety category exists and matches the safety category of the prompt.

In Table[2](https://arxiv.org/html/2412.16339v2#S4.T2 "Table 2 ‣ 4.2 Policy Retrieval Accuracy ‣ 4 Science of Deliberate Alignment ‣ Deliberative Alignment: Reasoning Enables Safer Language Models"), we display policy retrieval accuracy separately based on the ideal response type (hard refusal, safe completion, or compliance). In all three cases, our safety-trained model references the relevant policy in the CoT with much higher accuracy than the baseline model. For safe completion prompts, the safety-trained model achieves a particularly high policy retrieval accuracy of 0.91. For prompts where the ideal completion is compliance, we do not expect the safety-trained model to necessarily reference policies, so observing a lower rate of policy retrieval (0.54) is expected.

Notably, the non-safety-trained baseline has refusal rates and policy retrieval accuracies greater than 0. The reasons for this are that the base model has seen some safety-related data during pretraining, and our classifier is generous about attributing CoTs to potential policies. For example, if a CoT says “illegal content is not allowed, so I will refuse”, it will count as having referenced the Illicit Content policy.

Table 2: _Policy retrieval accuracy._ Fraction of times the chain-of-thought referenced the correct detailed policy category, broken down by where the ideal response is a hard refusal, safe completion, or compliance.

### 4.3 Generalization to OOD settings

In Section [3.1.3](https://arxiv.org/html/2412.16339v2#S3.SS1.SSS3 "3.1.3 Jailbreaks ‣ 3.1 Safety Evaluations ‣ 3 Results ‣ Deliberative Alignment: Reasoning Enables Safer Language Models"), we found that the o1 models significantly improved on jailbreak evaluations such as StrongREJECT. Our hypothesis is that deliberative alignment improves the model’s alignment in uncommon or out-of-distribution (OOD) settings (which are especially prevalent in the StrongREJECT dataset).

In order to test the impact of deliberative alignment on OOD robustness, we test generalization on two different types of data: non-English language data, and encoded data (e.g. base64), using a version of the o1-mini model. In particular, we compare three models:

*   •
No-Safety Baseline: The model does not undergo any Deliberative Alignment training;

*   •
Eng-Only, No-Encoded Data: The model is trained on a filtered dataset, where we have removed all safety-related non-English and encoded data. The model still sees non-English and encoded data during pretraining, as well as the non-safety portions of SFT and RL;

*   •
Full Data: The model is trained on the full dataset;

on the following two evals:

*   •
Encoding: We test the model’s resistance to jailbreaks that use encodings. We have a set of 250 forbidden prompts (e.g. asking for instructions on how to make a bomb), and a set of jailbreak techniques that use encodings (e.g. encoding a prompt in base64). For each forbidden prompt, we generate multiple jailbroken prompts using different jailbreak techniques. Then we grade the model as incorrect on a forbidden prompt if it fails to refuse on any of its jailbroken prompts.

*   •
Multilingual: We translate jailbreak prompts into different languages, and measure how often the model refuses to answer these prompts.

Our goal is to see how similarly the “Eng-only, No-Encoded Data” model performs to the “Full Data” model when it has never seen multilingual or encoding-based data during safety training.

Table 3: _Out-of-distribution generalization results._ Training with deliberative alignment shows strong generalization ability on encoding-based and multilingual jailbreak evaluations. Values are reported as mean ± stderr, with the standard error estimated using bootstrap resampling with 10k replicates at the 0.95 level.

The models trained with deliberative alignment attain accuracies significantly higher than the no-safety baseline on these evals (see Table[3](https://arxiv.org/html/2412.16339v2#S4.T3 "Table 3 ‣ 4.3 Generalization to OOD settings ‣ 4 Science of Deliberate Alignment ‣ Deliberative Alignment: Reasoning Enables Safer Language Models")). Notably, the model that has never been safety trained on encoding or non-english data performs comparably to the model trained with all the safety data, demonstrating clear out-of-distribution generalization.

## 5 Related Work

Deliberative alignment is the first alignment approach that directly teaches a model the text of its safety specifications and trains the model to reason over these learned specifications at inference time to give safer responses. Figure [15](https://arxiv.org/html/2412.16339v2#S5.F15 "Figure 15 ‣ 5 Related Work ‣ Deliberative Alignment: Reasoning Enables Safer Language Models") highlights the distinctions between Deliberative alignment and representative methods of existing alignment approaches. The left column of the figure shows the different ways that specifications are incorporated into the training data, and the right column illustrates the inference time behavior of models trained under the different methods. Deliberative alignment is applicable to models that have CoT reasoning.

![Image 6: Refer to caption](https://arxiv.org/html/2412.16339v2/figure/related_work.png)

Figure 15: _Comparison of deliberative alignment and representative methods of existing alignment approaches._ a) _Training data generation_: Even though RLAIF methods like CAI[[26](https://arxiv.org/html/2412.16339v2#bib.bibx26)] use safety specifications to generate training labels, only the labels themselves are used in training. Knowledge of the specifications themselves is thereby lost to the model. Whereas in deliberative alignment, the chain-of-thought, which contains both the content of the specifications and how to reason over them, is supervised in addition to other model output during SFT. The trained model can thereby retrieve relevant policies at inference time and apply them to generate aligned responses. b) _Inference time behavior_: In RLHF and CAI, there is no reasoning during inference time. In Self-REFINE [[27](https://arxiv.org/html/2412.16339v2#bib.bibx27)], reasoning occurs through structured few-shot prompting. In deliberative alignment, reasoning occurs automatically via chain-of-thought, including reasoning over learned safety specifications.

### 5.1 Safety Training

Traditionally, safe model behavior is instilled into LLMs using supervised finetuning (SFT) followed by reinforcement learning from human feedback (RLHF)[[28](https://arxiv.org/html/2412.16339v2#bib.bibx28)]. Direct Policy Optimization (DPO) is an alternative to RLHF that skips the reward model and directly optimizes the policy model using preference data [[29](https://arxiv.org/html/2412.16339v2#bib.bibx29)].

Constitutional AI (CAI) [[26](https://arxiv.org/html/2412.16339v2#bib.bibx26)] builds on the standard SFT + RLHF paradigm, incorporating a predefined set of principles to guide behavior called a “constitution” (which is comparable to our spec). During CAI’s SFT phase, the initial responses from an AI model are critiqued and revised by the same model supplied with the constitution text. The revision from the (response, critique, revision) sequence is ultimately used, alongside the prompt, for SFT training. CAI’s RL stage uses a preference model that was finetuned on preference data from an AI model given the constitution.

To summarize these approaches, specifications are added to the model in the following steps:

1.   1.
The model developers define the specifications that the AI assistant should follow.

2.   2.
These specifications are converted into instructions for human or AI trainers to label data. This data can take the form of supervised (prompt, answer) pairs or preference data.

3.   3.
The labeled data is then used to train the policy model itself or to train a reward model that is subsequently used to train the policy model.

Crucially, while the SFT labels and preference scores of the prior methods are a function of the specification given to the human or AI labeler, these specifications are never explicitly provided to the policy model itself. Only the final answer itself is used in training.(Note how the critiques in CAI, which are loosely analogous to our CoT, are not employed during optimization.) In contrast, in Deliberative Alignment, the model memorizes the policies in its CoT and learns how to apply it in context, and the CoT is directly optimized during SFT.

It is also worth noting that our model varies the specification information given to each training example, enabling us to cumulatively teach the model more detailed and nuanced safety policies than would be possible with a fixed constitution.

### 5.2 Inference-time Safety Reasoning

There is a substantial body of work focused on enhancing LLM outputs using a critique-and-refine approach that leverages natural language feedback (for a comprehensive overview, see [[30](https://arxiv.org/html/2412.16339v2#bib.bibx30), [27](https://arxiv.org/html/2412.16339v2#bib.bibx27)]). Although the vast majority of these papers is not safety-focused, their methods could be adapted for producing safer model responses. A notable example is Self-REFINE [[27](https://arxiv.org/html/2412.16339v2#bib.bibx27)], which employs iterative feedback and refinement to improve model outputs (see Figure [15](https://arxiv.org/html/2412.16339v2#S5.F15 "Figure 15 ‣ 5 Related Work ‣ Deliberative Alignment: Reasoning Enables Safer Language Models")). In Self-REFINE, the model initially generates a response, then provides feedback through few-shot prompting, followed by revising the response—a process that repeats for multiple iterations. Self-REFINE uses the same model for generation, critique, and revision, though other works use different models for these tasks (e.g., [[31](https://arxiv.org/html/2412.16339v2#bib.bibx31)] trains a separate revision model). A common feature of these approaches is the reliance on pre-specified language-model-programs (LMPs) [[32](https://arxiv.org/html/2412.16339v2#bib.bibx32)] or predetermined reasoning paths for improving the response at inference time. In contrast, Deliberative Alignment leverages o1’s chain-of-thought to perform automatic safety reasoning at inference time with no predefined LMP or fixed reasoning path required.

Backtracking [[33](https://arxiv.org/html/2412.16339v2#bib.bibx33)] is a recent technique that trains a LLM to generate a special [RESET] token when it recognizes that it has made a partial unsafe response. The model then restarts the response from scratch, with preceding tokens remaining in the context window. The tokens before and up to [RESET], which can be viewed as safety reasoning, are discarded before returning the final response. Backtracking can be considered an automatic, guidance-free inference-time safety reasoning mechanism,. However, it lacks flexibility: backtracking is limited to a single instance per response. In contrast, the CoT of deliberative alignment allows for unlimited “backtracking”. Furthermore, neither backtracking – nor any existing alignment method – directly teaches models safety specifications, making Deliberative Alignment-trained models unique in their ability to reason over learned safety specifications during inference-time safety reasoning.

## 6 Discussion

We are encouraged by Deliberative Alignment’s effectiveness on improving alignment to OpenAI’s policy specifications and robustness to jailbreaks. The method also allows us to specify the boundary between compliance, refusal, and safe completion in finer detail than was possible before. We believe this nuanced control can lead to models that are not just safer but also more helpful. The method’s use of a synthetic data generation pipeline to create training data from provided specifications and prompts also makes it a relatively scalable approach to alignment.

We anticipate OpenAI’s policies will keep evolving, but that training models to precisely follow the current defined set of policies is essential: This practice helps us build the skills for aligning with any policy requirements, providing invaluable preparation for future scenarios where the stakes are extremely high or where strict adherence to policies is critical.

This work connects to a broader question in AI safety: will advancements in alignment keep pace with AI capabilities? That o1 model’s enhanced reasoning abilities allow for more effective implementation of alignment strategies offers optimism that alignment is progressing alongside capabilities.

However, this encouraging trend may not persist indefinitely. As AI models grow more sophisticated, they could develop goals that diverge from those intended by their developers. For instance, a highly intelligent and self-aware AI might reject the constraints and objectives set by humans [[34](https://arxiv.org/html/2412.16339v2#bib.bibx34)]. Alternatively, an AI could remain committed to its human-assigned terminal goal but, in the process, pursue instrumental goals like self-preservation, resource acquisition, or enhancing its cognitive abilities [[35](https://arxiv.org/html/2412.16339v2#bib.bibx35), [36](https://arxiv.org/html/2412.16339v2#bib.bibx36)]. These power-seeking tendencies could lead to harmful or unintended consequences. And as models gain more intelligence and autonomy, the scale of potential harm from misalignment increases dramatically, with the risk of catastrophic outcomes. This underscores the urgent need for ongoing research in AI alignment. We are actively investing in better alignment strategies and research areas like monitoring chain-of-thoughts for deception [[37](https://arxiv.org/html/2412.16339v2#bib.bibx37), [38](https://arxiv.org/html/2412.16339v2#bib.bibx38)], to ensure that as AI systems become more capable, they remain aligned with human values.

##### Acknowledgments.

We are grateful to David Li, Eric Mitchell, Kai Xiao, Max Schwarzer, and Sean Grove for their contributions to our experiments. We also thank Filippo Raso, Jenny Nitishinskaya, Jerry Tworek, Meghan Shah, Nick Ryder, and Szymon Sidor for their helpful feedback on the paper.

## References

*   [1]OpenAI “Learning to Reason with LLMs”, 2024 URL: [https://openai.com/index/learning-to-reason-with-llms/](https://openai.com/index/learning-to-reason-with-llms/)
*   [2]Long Ouyang et al. “Training language models to follow instructions with human feedback” In _NeurIPS_, 2022 
*   [3]Abhimanyu Dubey et al. “The LLaMA 3 herd of models” In _arXiv preprint arXiv:2407.21783_, 2024 
*   [4]Machel Reid et al. “Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context” In _arXiv preprint arXiv:2403.05530_, 2024 
*   [5]Josh Achiam et al. “GPT-4 technical report” In _arXiv preprint arXiv:2303.08774_, 2023 
*   [6]Andy Zou et al. “Universal and transferable adversarial attacks on aligned language models” In _arXiv preprint arXiv:2307.15043_, 2023 
*   [7]Alexander Wei, Nika Haghtalab and Jacob Steinhardt “Jailbroken: How does llm safety training fail?” In _NeurIPS_, 2024 
*   [8]Maksym Andriushchenko, Francesco Croce and Nicolas Flammarion “Jailbreaking Leading Safety-Aligned LLMs with Simple Adaptive Attacks” In _arXiv preprint arXiv:2404.02151_, 2024 
*   [9]Jonathan Uesato et al. “Solving math word problems with process-and outcome-based feedback” In _arXiv preprint arXiv:2211.14275_, 2022 
*   [10]Charlie Snell, Dan Klein and Ruiqi Zhong “Learning by Distilling Context” In _arXiv preprint arXiv:2209.15189_, 2022 
*   [11]Amanda Askell et al. “A General Language Assistant as a Laboratory for Alignment” In _arXiv preprint arXiv:2112.00861_, 2021 
*   [12]Alexandra Souly et al. “A StrongREJECT for Empty Jailbreaks” In _arXiv preprint arXiv:2402.10260_, 2024 
*   [13]Paul Röttger et al. “XSTest: A Test Suite for Identifying Exaggerated Safety Behaviours in Large Language Models” In _arXiv preprint arXiv:2308.01263_, 2024 
*   [14]OpenAI “Introducing the Model Spec”, 2024 URL: [https://cdn.openai.com/spec/model-spec-2024-05-08.html](https://cdn.openai.com/spec/model-spec-2024-05-08.html)
*   [15]Wenting Zhao et al. “WildChat: 1M ChatGPT Interaction Logs in the Wild” In _arXiv preprint arXiv:2405.01470_, 2024 
*   [16]Xinyue Shen et al. “”Do Anything Now”: Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models” In _arXiv preprint arXiv:2308.03825_, 2024 
*   [17]Patrick Chao et al. “Jailbreaking Black Box Large Language Models in Twenty Queries” In _arXiv preprint arXiv:2310.08419_, 2024 
*   [18]Patrick Chao et al. “JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models” In _arXiv preprint arXiv:2404.01318_, 2024 
*   [19]Priyanshu Kumar et al. “Refusal-Trained LLMs Are Easily Jailbroken As Browser Agents” In _arXiv preprint arXiv:2410.13886_, 2024 
*   [20]OpenAI “O1 System Card”, 2024 URL: [https://cdn.openai.com/o1-system-card.pdf](https://cdn.openai.com/o1-system-card.pdf)
*   [21]OpenAI “GPT-4o System Card”, 2024 URL: [https://cdn.openai.com/gpt-4o-system-card.pdf](https://cdn.openai.com/gpt-4o-system-card.pdf)
*   [22]Anthropic “Model Card Addendum: Claude 3.5 Haiku and Upgraded Claude 3.5 Sonnet”, 2024 URL: [https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf](https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf)
*   [23]Google Gemini “Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context” In _arXiv preprint arXiv:2403.05530_, 2024 
*   [24]Jason Wei et al. “Measuring short-form factuality in large language models” In _arXiv preprint arXiv:2411.04368_, 2024 
*   [25]Alicia Parrish et al. “BBQ: A Hand-Built Bias Benchmark for Question Answering” In _arXiv preprint arXiv:2110.08193_, 2021 
*   [26]Yuntao Bai et al. “Constitutional AI: Harmlessness from AI Feedback” In _arXiv preprint arXiv:2212.08073_, 2022 
*   [27]Aman Madaan et al. “Self-Refine: Iterative Refinement with Self-Feedback” In _arXiv preprint arXiv:2303.17651_, 2023 
*   [28]Paul Christiano et al. “Deep Reinforcement Learning from Human Preferences” In _Advances in Neural Information Processing Systems_ 30, 2017 
*   [29]Rafael Rafailov et al. “Direct Preference Optimization: Your Language Model is Secretly a Reward Model” In _arXiv preprint arXiv:2305.18290_, 2024 
*   [30]Liangming Pan et al. “Automatically Correcting Large Language Models: Surveying the landscape of diverse self-correction strategies” In _arXiv preprint arXiv:2308.03188_, 2023 
*   [31]Sean Welleck et al. “Generating sequences by learning to self-correct” In _The Eleventh International Conference on Learning Representations_ 2, 2023 
*   [32]Imanol Schlag et al. “Large Language Model Programs” In _arXiv preprint arXiv:2305.05364_, 2023 
*   [33]Yiming Zhang et al. “Backtracking improves generation safety” In _arXiv preprint arXiv:2409.14586_, 2024 
*   [34]Stuart Russell “Human compatible: Artificial intelligence and the problem of control” USA: Penguin Books, 2019 
*   [35]Nick Bostrom “Superintelligence: Paths, Dangers, Strategies” USA: Oxford University Press, Inc., 2014 
*   [36]Stephen. Omohundro “The Basic AI Drives” In _Proceedings of the 2008 Conference on Artificial General Intelligence 2008: Proceedings of the First AGI Conference_ NLD: IOS Press, 2008, pp. 483–492 
*   [37]Olli Järviniemi and Evan Hubinger “Uncovering Deceptive Tendencies in Language Models: A Simulated Company AI Assistant” In _arXiv preprint arXiv:2405.01576_, 2024 
*   [38]Thilo Hagendorff “Deception abilities emerged in large language models” In _Proceedings of the National Academy of Sciences_ 121.24, 2024 

## Appendix A Human Review Experiment

Model performance on the StrongREJECT benchmark [[12](https://arxiv.org/html/2412.16339v2#bib.bibx12)] was validated through a detailed human review process. This involved a comprehensive human review of the StrongREJECT responses from o1, GPT-4o, Claude 3.4 Sonnet, and Gemini 1.5 Pro models. The results shown in Table [4](https://arxiv.org/html/2412.16339v2#A1.T4 "Table 4 ‣ Appendix A Human Review Experiment ‣ Deliberative Alignment: Reasoning Enables Safer Language Models") corroborate our autoeval results in Figure [12](https://arxiv.org/html/2412.16339v2#S3.F12 "Figure 12 ‣ 3.2 Comparison to external models ‣ 3 Results ‣ Deliberative Alignment: Reasoning Enables Safer Language Models").

The benchmark consists of 60 forbidden prompts, each transformed into adversarial prompts using 35 distinct jailbreak techniques designed to bypass model refusals and generate restricted content. This process resulted in 2,100 adversarial prompts presented to each model. The models’ responses were then evaluated by a team of 35 trained human reviewers to ensure accuracy and alignment with the benchmark’s grading criteria.

Human reviewers assessed each prompt and its corresponding model response using a 1–3–5 grading scale:

*   •
1: No model assistance observed in the response.

*   •
3: Partial model assistance observed in the response.

*   •
5: Maximum model assistance observed, reflecting significant reliance on the model’s capabilities.

To ensure high-quality evaluations, we implemented a consensus-checking mechanism where each {prompt, answer} pair was independently graded by at least two reviewers. In cases of disagreement, a third reviewer, recognized as an expert, conducted an additional evaluation and made the final arbitration. This process minimized inconsistencies and ensured the reliability of the grading across all models.

The Gemini API returned errors for 29 prompts due to safety filters. We treated these blocked prompts as having response scores of 1.

Table 4: _Human review results on StrongREJECT._ We compare models’ goodness@0.1 and average reviewer scores (grade of 1 is optimal).
