---
title: "Small Language Models as Judges for Rubric-Based Reinforcement Learning"
authors: "Fengyu Xie; Yilun Zhao; Bingsen Chen; Arman Cohan; Chen Zhao"
year: 2026
source: https://arxiv.org/html/2608.30005v1
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

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) [![](img) Report Issue](# "Report an Issue") [![](img) Back to Abstract](/abs/2608.30005v1 "Back to abstract page") [![](img) Download PDF](/pdf/2608.30005v1 "Download PDF") [![](img)](javascript:toggleNavTOC(); "Toggle navigation") [![](img)](javascript:toggleReadingMode(); "Disable reading mode, show header and footer")

![](img) ![](img) ![](img)

1.  [Abstract](#abstract1 "In Small Language Models as Judges for Rubric-Based Reinforcement Learning")
2.  [1 Introduction](#S1 "In Small Language Models as Judges for Rubric-Based Reinforcement Learning")
3.  [2 Rubric Judging Task and Dataset](#S2 "In Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    1.  [2.1 Our Task: Pointwise Rubric Judging](#S2.SS1 "In 2 Rubric Judging Task and Dataset ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    2.  [2.2 Dataset Design Overview](#S2.SS2 "In 2 Rubric Judging Task and Dataset ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    3.  [2.3 PointRubric Construction](#S2.SS3 "In 2 Rubric Judging Task and Dataset ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        1.  [Rubric standardization.](#S2.SS3.SSS0.Px1 "In 2.3 PointRubric Construction ‣ 2 Rubric Judging Task and Dataset ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        2.  [Response roles.](#S2.SS3.SSS0.Px2 "In 2.3 PointRubric Construction ‣ 2 Rubric Judging Task and Dataset ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        3.  [Final benchmark.](#S2.SS3.SSS0.Px3 "In 2.3 PointRubric Construction ‣ 2 Rubric Judging Task and Dataset ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    4.  [2.4 RaR-Science-Static](#S2.SS4 "In 2 Rubric Judging Task and Dataset ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        1.  [Response bank and split.](#S2.SS4.SSS0.Px1 "In 2.4 RaR-Science-Static ‣ 2 Rubric Judging Task and Dataset ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        2.  [Reference labels and aggregation.](#S2.SS4.SSS0.Px2 "In 2.4 RaR-Science-Static ‣ 2 Rubric Judging Task and Dataset ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    5.  [2.5 Reference Labels and Human Audit](#S2.SS5 "In 2 Rubric Judging Task and Dataset ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
4.  [3 Rubric-Judge Methods](#S3 "In Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    1.  [3.1 Scoring Methods](#S3.SS1 "In 3 Rubric-Judge Methods ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        1.  [Generative Judges.](#S3.SS1.SSS0.Px1 "In 3.1 Scoring Methods ‣ 3 Rubric-Judge Methods ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        2.  [Logprob Judges.](#S3.SS1.SSS0.Px2 "In 3.1 Scoring Methods ‣ 3 Rubric-Judge Methods ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        3.  [Probe Judges.](#S3.SS1.SSS0.Px3 "In 3.1 Scoring Methods ‣ 3 Rubric-Judge Methods ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    2.  [3.2 Post-training with Supervised Fine-tuning](#S3.SS2 "In 3 Rubric-Judge Methods ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
5.  [4 Static Rubric-Judge Evaluation](#S4 "In Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    1.  [4.1 Experiment Setup](#S4.SS1 "In 4 Static Rubric-Judge Evaluation ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    2.  [4.2 Static Judge Results](#S4.SS2 "In 4 Static Rubric-Judge Evaluation ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        1.  [PointRubric shows that small models can perform pointwise rubric judging when the benchmark format is controlled.](#S4.SS2.SSS0.Px1 "In 4.2 Static Judge Results ‣ 4 Static Rubric-Judge Evaluation ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        2.  [On RaR-Science-Static, the readout method matters more than model size alone.](#S4.SS2.SSS0.Px2 "In 4.2 Static Judge Results ‣ 4 Static Rubric-Judge Evaluation ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        3.  [Probe is the strongest readout on RaR-Science-Static across all model sizes.](#S4.SS2.SSS0.Px3 "In 4.2 Static Judge Results ‣ 4 Static Rubric-Judge Evaluation ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    3.  [4.3 Selecting the Probe Configuration for RL](#S4.SS3 "In 4 Static Rubric-Judge Evaluation ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
6.  [5 Probe-Based Rubric Rewards for RL](#S5 "In Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    1.  [5.1 Matched RL Protocol and Results](#S5.SS1 "In 5 Probe-Based Rubric Rewards for RL ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        1.  [The Qwen3-1.7B Probe reward produces the strongest trained policy.](#S5.SS1.SSS0.Px1 "In 5.1 Matched RL Protocol and Results ‣ 5 Probe-Based Rubric Rewards for RL ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        2.  [Downstream reward utility does not exactly follow static judge accuracy.](#S5.SS1.SSS0.Px2 "In 5.1 Matched RL Protocol and Results ‣ 5 Probe-Based Rubric Rewards for RL ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        3.  [A blind human audit supports the main policy comparison.](#S5.SS1.SSS0.Px3 "In 5.1 Matched RL Protocol and Results ‣ 5 Probe-Based Rubric Rewards for RL ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    2.  [5.2 Transfer Results](#S5.SS2 "In 5 Probe-Based Rubric Rewards for RL ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    3.  [5.3 Efficiency-Quality Results](#S5.SS3 "In 5 Probe-Based Rubric Rewards for RL ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
7.  [6 Related Work](#S6 "In Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    1.  [Rubric-based RL.](#S6.SS0.SSS0.Px1 "In 6 Related Work ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    2.  [LLM-as-a-judge and small evaluators.](#S6.SS0.SSS0.Px2 "In 6 Related Work ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
8.  [7 Conclusion](#S7 "In Small Language Models as Judges for Rubric-Based Reinforcement Learning")
9.  [References](#bib "In Small Language Models as Judges for Rubric-Based Reinforcement Learning")
10. [A PointRubric Construction and Rubric Scoring](#A1 "In Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    1.  [A.1 Pointwise and Pairwise Rubric Scoring](#A1.SS1 "In Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    2.  [A.2 PointRubric Construction Details](#A1.SS2 "In Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    3.  [A.3 Rubric-Transformation Audit](#A1.SS3 "In Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        1.  [Representative transformations.](#A1.SS3.SSS0.Px1 "In A.3 Rubric-Transformation Audit ‣ Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    4.  [A.4 PointRubric Response Roles](#A1.SS4 "In Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    5.  [A.5 PointRubric Evaluation Protocol and Metrics](#A1.SS5 "In Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    6.  [A.6 Reference Judge and Construction Prompts](#A1.SS6 "In Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    7.  [A.7 RaR-Science-Static Response Bank and Splits](#A1.SS7 "In Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        1.  [Extended held-out response bank.](#A1.SS7.SSS0.Px1 "In A.7 RaR-Science-Static Response Bank and Splits ‣ Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    8.  [A.8 RaR-Science-Static Reference Labels and Aggregation](#A1.SS8 "In Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    9.  [A.9 Reference-Label Validation](#A1.SS9 "In Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
11. [B Static Evaluation Details](#A2 "In Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    1.  [B.1 Generative and Logprob Judge Details](#A2.SS1 "In Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        1.  [Generative judging.](#A2.SS1.SSS0.Px1 "In B.1 Generative and Logprob Judge Details ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        2.  [Forced-choice Logprob scoring.](#A2.SS1.SSS0.Px2 "In B.1 Generative and Logprob Judge Details ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    2.  [B.2 Probe Training and Calibration](#A2.SS2 "In Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        1.  [Canonical criterion rendering.](#A2.SS2.SSS0.Px1 "In B.2 Probe Training and Calibration ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        2.  [Representation extraction.](#A2.SS2.SSS0.Px2 "In B.2 Probe Training and Calibration ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        3.  [Feature standardization.](#A2.SS2.SSS0.Px3 "In B.2 Probe Training and Calibration ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        4.  [Probe heads.](#A2.SS2.SSS0.Px4 "In B.2 Probe Training and Calibration ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        5.  [Layer and threshold selection.](#A2.SS2.SSS0.Px5 "In B.2 Probe Training and Calibration ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        6.  [Supervision cost and reuse.](#A2.SS2.SSS0.Px6 "In B.2 Probe Training and Calibration ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        7.  [Probability rewards.](#A2.SS2.SSS0.Px7 "In B.2 Probe Training and Calibration ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    3.  [B.3 Supervised Fine-tuning Details](#A2.SS3 "In Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    4.  [B.4 Static Evaluation Targets](#A2.SS4 "In Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    5.  [B.5 Rubric-RM Pairwise Comparison](#A2.SS5 "In Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    6.  [B.6 Static Readout Error Analysis](#A2.SS6 "In Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        1.  [Representative Generative false positive.](#A2.SS6.SSS0.Px1 "In B.6 Static Readout Error Analysis ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        2.  [Representative Probe false negative.](#A2.SS6.SSS0.Px2 "In B.6 Static Readout Error Analysis ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    7.  [B.7 Static Metrics](#A2.SS7 "In Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        1.  [Parse success.](#A2.SS7.SSS0.Px1 "In B.7 Static Metrics ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        2.  [Criterion accuracy.](#A2.SS7.SSS0.Px2 "In B.7 Static Metrics ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        3.  [Weighted criterion accuracy.](#A2.SS7.SSS0.Px3 "In B.7 Static Metrics ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        4.  [Macro-F1.](#A2.SS7.SSS0.Px4 "In B.7 Static Metrics ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        5.  [Balanced accuracy and MCC.](#A2.SS7.SSS0.Px5 "In B.7 Static Metrics ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        6.  [Scalar-score error.](#A2.SS7.SSS0.Px6 "In B.7 Static Metrics ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        7.  [Score correlation.](#A2.SS7.SSS0.Px7 "In B.7 Static Metrics ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
        8.  [Pairwise ordering.](#A2.SS7.SSS0.Px8 "In B.7 Static Metrics ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    8.  [B.8 Bootstrap Confidence Intervals](#A2.SS8 "In Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    9.  [B.9 Probe Layer Selection](#A2.SS9 "In Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
12. [C Rubric RL Details](#A3 "In Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    1.  [C.1 RL Reward Configuration](#A3.SS1 "In Appendix C Rubric RL Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    2.  [C.2 RL Score Confidence Intervals](#A3.SS2 "In Appendix C Rubric RL Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    3.  [C.3 On-Policy Reward Dynamics and Qualitative Cases](#A3.SS3 "In Appendix C Rubric RL Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    4.  [C.4 Efficiency Measurement](#A3.SS4 "In Appendix C Rubric RL Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    5.  [C.5 Human Audit and Reference-Judge Validation](#A3.SS5 "In Appendix C Rubric RL Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    6.  [C.6 Additional RL Configuration Checks](#A3.SS6 "In Appendix C Rubric RL Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
13. [D Generalization Evaluation Details](#A4 "In Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    1.  [D.1 GPQA-Diamond Evaluation](#A4.SS1 "In Appendix D Generalization Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    2.  [D.2 Cross-Domain Probe Transfer](#A4.SS2 "In Appendix D Generalization Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
14. [E Prompts for Reproducibility](#A5 "In Small Language Models as Judges for Rubric-Based Reinforcement Learning")
15. [F Dataset Examples](#A6 "In Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    1.  [PointRubric example.](#A6.SS0.SSS0.Px1 "In Appendix F Dataset Examples ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")
    2.  [RaR-Science example.](#A6.SS0.SSS0.Px2 "In Appendix F Dataset Examples ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")

[License: CC BY 4.0](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2608.30005v1 \[cs.CL\] 30 Aug 2026

# Small Language Models as Judges for Rubric-Based Reinforcement Learning

Fengyu Xie Affiliation: New York University Email: [fx2137@nyu.edu](mailto:)    Yilun Zhao Affiliation: Yale University Email: [chen.zhao@nyu.edu](mailto:)    Bingsen Chen Affiliation: New York University Email: [yilun.zhao@yale.edu](mailto:)    Arman Cohan Affiliation: Yale University    Chen Zhao Affiliation: New York University

###### Abstract

Rubric-based reinforcement learning extends RL beyond tasks with exact answers or rule-based verifiers by scoring responses against instance-specific criteria. However, this makes reward computation expensive: training requires repeated rubric judging, often with proprietary APIs or local generative LLM judges with 7B parameters or more. We study whether smaller language models can serve as efficient and reliable rubric-based judges. To make this question measurable, we construct PointRubric and RaR-Science-Static, two pointwise rubric-based evaluation datasets with instance-specific criteria and itemwise satisfaction labels. We compare three ways of extracting criterion-level judgments from small models: Generative verdicts, Yes/No Logprob scoring, and Probe judges. Across both datasets, the Qwen3-1.7B Probe judge achieves the strongest criterion-level agreement among these methods, outperforming Generative and Logprob judges. Used as a GRPO reward model, it trains a policy from 0.232 to 0.643 on RaR-Science rubric score, compared with 0.594 for an 8B Generative judge baseline, while the baseline requires 10.7$\times$ more reward-judge time. Task and domain transfer experiments further suggest that Probe judges preserve criterion-level reward structure across settings. ¹¹ 1 Our code and data have been released at [https://github.com/Ignotus6043/SLM-rubric-RL](https://github.com/Ignotus6043/SLM-rubric-RL).

## 1 Introduction

Figure 1: Rubric scoring setup. A rubric specifies criteria and weights for a candidate response. Pointwise scoring yields criterion-level labels, while pairwise scoring yields a relative winner. Criterion scores can then be aggregated into a scalar reward for evaluation or reinforcement learning.

Recent progress in reinforcement learning with verifiable rewards (RLVR) has shown that outcome rewards from rule-based verifiers can effectively elicit reasoning abilities in large language models (LLMs) on verifiable tasks such as math and coding ([Le et al., 2022](#bib.bib14); [Liu et al., 2023a](#bib.bib37); [Shao et al., 2024](#bib.bib12); [Wen et al., 2025](#bib.bib10); [Guo et al., 2025](#bib.bib13)). However, many increasingly important agentic applications go beyond this narrow notion of verifiability. In long-form generation tasks such as Deep Research, quality can depend on content coverage, factuality, source use, and task-specific constraints, which are hard to capture with simple automatic checkers ([Citron, 2024](#bib.bib42); [Arora et al., 2025](#bib.bib23); [OpenAI, 2025a](#bib.bib41); [Shao et al., 2026](#bib.bib26)). Rubric-based reinforcement learning offers a promising alternative for such settings: rubrics evaluate multiple aspects of generation quality through instance-specific criteria while still producing scalar rewards for optimization ([Ouyang et al., 2022](#bib.bib9); [Gunjal et al., 2026](#bib.bib20)).

A key component of rubric-based RL is obtaining the rubric reward, where an LLM judge evaluates responses against explicit rubric criteria and aggregates these judgments into rewards for RL training ([Zheng et al., 2023](#bib.bib11); [Kim et al., 2024b](#bib.bib2)). Existing rubric-based RL approaches mainly rely on proprietary model APIs or large generative judges to maintain judgment quality ([OpenAI, 2024](#bib.bib34); [Gunjal et al., 2026](#bib.bib20); [Shao et al., 2026](#bib.bib26)). This makes reward computation expensive at scale because each RL step may require scoring long responses against multiple criteria. Proprietary judges also make exact reproduction harder because access depends on a fixed model snapshot from the provider. These limitations raise a central question: *Can much smaller language models serve as effective rubric judges for rubric-based RL?*

To answer this question, we need evaluation data that matches the reward computation used in rubric-based RL: explicit criteria, multiple responses under the same rubric, labels for each response–criterion pair, and a weighted scoring rule. Existing resources provide important pieces of this setup, but not the full structure required for this evaluation setting. Preference and reward-model datasets focus on pairwise comparisons or scalar reward modeling ([Ouyang et al., 2022](#bib.bib9); [Lambert et al., 2025](#bib.bib3); [Zhu et al., 2025](#bib.bib17)). Fine-grained and rubric-evaluation benchmarks provide skills, criteria, or judge-evaluation targets, but typically lack weighted rubric rewards or response–criterion satisfaction labels for fixed candidate responses ([Ye et al., 2024](#bib.bib38); [Liu et al., 2026](#bib.bib21); [Zhou et al., 2026](#bib.bib25); [Pan et al., 2026](#bib.bib24); [Wen et al., 2026](#bib.bib28)). Domain-specific rubric datasets provide structured rubrics and scoring rules, but not controlled static response banks with labels for every response–criterion pair ([Arora et al., 2025](#bib.bib23); [Gunjal et al., 2026](#bib.bib20)). We therefore derive PointRubric, a controlled pointwise benchmark from OpenRubrics, and construct RaR-Science-Static, a fixed response bank of similar format based on RaR-Science, for evaluating the same judge methods under the rubric-based RL format.

We compare three rubric-judging methods on PointRubric and RaR-Science-Static using Qwen3 models from 0.6B to 8B parameters ([Yang et al., 2025](#bib.bib31)): Generative verdicts, Yes/No Logprob scoring, and hidden-state Probes. For each Probe, the language-model backbone is frozen and only a lightweight linear classifier is trained on GPT-4o criterion labels. Across both static settings, Probe judges substantially outperform Generative and Logprob judges, suggesting that even 1.7B-scale models contain useful evaluative signals in their hidden representations that Generative and Logprob scoring do not recover as reliably ([Gisserot-Boukhlef et al., 2026](#bib.bib27); [Li et al., 2026](#bib.bib22)).

We then use the Qwen3-1.7B Probe judge as the reward model for GRPO in a controlled RaR-Science science setup ([Shao et al., 2024](#bib.bib12); [Gunjal et al., 2026](#bib.bib20)). This Probe reward improves the policy’s rubric score from 0.232 to 0.643, outperforming an 8B Generative judge reward baseline, which reaches 0.594, while the 8B baseline requires 10.7$\times$ more reward-judge time at the comparison checkpoint. Additional transfer experiments on GPQA-Diamond and cross-domain rubric splits show that the Probe signal is not limited to the static training setting ([Rein et al., 2024](#bib.bib30)).

Our contributions are as follows:

- •
  We construct two pointwise rubric-evaluation datasets for studying small rubric judges: PointRubric, adapted from OpenRubrics, and RaR-Science-Static, built from RaR-Science to match the rubric format in downstream RL.
- •
  We compare Generative, Logprob, and Probe judges on PointRubric and RaR-Science-Static. Probe judges perform best, showing that small models encode useful criterion-level evaluative signals that are more reliably exposed through hidden states than through generation.
- •
  We use the Qwen3-1.7B Probe judge as the GRPO reward model on RaR-Science, training a policy from 0.232 to 0.643 on RaR-Science rubric score, compared with 0.594 for an 8B Generative judge reward baseline; the 8B Generative baseline requires 10.7$\times$ as much cumulative reward-judge time.

## 2 Rubric Judging Task and Dataset

|                                                                |                 |                    |                      |                        |
|----------------------------------------------------------------|-----------------|--------------------|----------------------|------------------------|
| Resource                                                       | Rubric criteria | Multiple responses | Per-criterion labels | Weighted rubric scores |
| FLASK ([Ye et al., 2024](#bib.bib38))                          | $✓$             | $✓$                | $\times$             | $\times$               |
| HealthBench ([Arora et al., 2025](#bib.bib23))                 | $✓$             | $\times$           | $\times$             | $✓$                    |
| IF-RewardBench ([Wen et al., 2026](#bib.bib28))                | $✓$             | $✓$                | $✓$                  | $\times$               |
| JudgeLM-100K ([Zhu et al., 2025](#bib.bib17))                  | $\times$        | $✓$                | $\times$             | $\times$               |
| OpenRubrics ([Liu et al., 2026](#bib.bib21))                   | $✓$             | $✓$                | $\times$             | $\times$               |
| RaR-Science / RaR-Medicine ([Gunjal et al., 2026](#bib.bib20)) | $✓$             | $\times$           | $\times$             | $✓$                    |
| RewardBench ([Lambert et al., 2025](#bib.bib3))                | $\times$        | $✓$                | $\times$             | $\times$               |
| RubricBench ([Zhou et al., 2026](#bib.bib25))                  | $✓$             | $✓$                | $\times$             | $\times$               |
| RubricEval ([Pan et al., 2026](#bib.bib24))                    | $✓$             | $\times$           | $✓$                  | $\times$               |
| PointRubric (ours)                                             | $✓$             | $✓$                | $✓$                  | $✓$                    |
| RaR-Science-Static (ours)                                      | $✓$             | $✓$                | $✓$                  | $✓$                    |

Table 1: Data requirements for pointwise rubric-based judge evaluation. PointRubric and RaR-Science-Static provide explicit rubric criteria, multiple responses per prompt, per-criterion labels, and weighted rubric scores.

A key component of rubric-based RL is rubric judging: determining whether a model response satisfies a given rubric criterion. We first define the task of pointwise rubric judging, where the judge evaluates one response against one rubric item at a time (§[2.1](#S2.SS1 "2.1 Our Task: Pointwise Rubric Judging ‣ 2 Rubric Judging Task and Dataset ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")). We then present the dataset design, review why existing datasets are not directly suitable for this setting, and describe how we adapt existing resources into pointwise rubric-judging benchmarks (§[2.2](#S2.SS2 "2.2 Dataset Design Overview ‣ 2 Rubric Judging Task and Dataset ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")–§[2.4](#S2.SS4 "2.4 RaR-Science-Static ‣ 2 Rubric Judging Task and Dataset ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")).

### 2.1 Our Task: Pointwise Rubric Judging

Preference-based alignment methods ([Ouyang et al., 2022](#bib.bib9); [Zheng et al., 2023](#bib.bib11); [Lambert et al., 2025](#bib.bib3)) typically learn reward signals from pairwise response comparisons: given a prompt and two candidate responses, a human annotator, reward model, or LLM judge predicts which response better satisfies the user’s intent. This formulation is useful for learning relative preferences, but it collapses all evaluation criteria into a single comparison. As a result, it does not reveal which aspects of a response are correct or incorrect.

Rubric-based RL instead specifies an explicit rubric ${C{(q)}} = {\{{(c_{j},w_{j})}\}}_{j = 1}^{m_{q}}$, where each $c_{j}$ is a natural-language criterion and $w_{j}$ is its aggregation weight. We therefore study *pointwise rubric judging*: given a prompt $q$, a candidate response $y$, and one rubric item $c_{j}$, the judge takes $(q,y,c_{j})$ as input and predicts whether response $y$ satisfies criterion $c_{j}$. The judge may return either a binary satisfaction label or a soft satisfaction score. These item-level outputs are then aggregated with the rubric weights to produce the scalar rubric score used for evaluation or RL.

Pointwise rubric judging can still induce pairwise preferences by comparing the aggregated scores of two responses under the same prompt and rubric. However, unlike pairwise judging, it preserves the rubric structure: it identifies which criteria are satisfied or violated and supports direct scalar reward computation. Appendix [A.1](#A1.SS1 "A.1 Pointwise and Pairwise Rubric Scoring ‣ Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") gives additional formal details and examples.

### 2.2 Dataset Design Overview

Existing rubric and reward-model datasets provide useful supervision for judging model outputs. However, they are not directly designed for pointwise rubric judging, where the judge must determine whether a single response satisfies a single rubric criterion and support reward computation from these item-level decisions.

As shown in [Table 1](#S2.T1 "Table 1 ‣ 2 Rubric Judging Task and Dataset ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), our setting requires four components: explicit rubric criteria as judge targets, multiple responses under the same prompt and rubric, per-criterion satisfaction labels, and a weighted scoring rule for aggregating criterion-level judgments into scalar rewards. Existing resources cover parts of this design, but usually lack criterion-level labels, controlled response banks, or the weighted aggregation structure used in rubric-based RL. We therefore use two evaluation settings: PointRubric, a new pointwise benchmark derived from OpenRubrics, and RaR-Science-Static, a fixed response bank built from RaR-Science for static judge evaluation.

### 2.3 PointRubric Construction

PointRubric evaluates criterion-level rubric judging. It is derived from OpenRubrics, which provides general-domain prompts and detailed natural-language rubrics. Since the original supervision is pairwise and does not label criterion-level satisfaction, we add new candidate responses and per-criterion labels to convert OpenRubrics into a controlled pointwise benchmark.

#### Rubric standardization.

We sample 3,000 OpenRubrics questions with explicit hard-rule constraints. We rewrite each one into six criteria: two hard criteria for mandatory constraints and four soft criteria for response quality. This fixed format gives all prompts the same criterion and weight structure while preserving the distinction between required constraints and softer quality dimensions. A manual audit found that 47 of 50 sampled transformations preserved the original rubric’s core intent; further results and examples are provided in Appendix [A.3](#A1.SS3 "A.3 Rubric-Transformation Audit ‣ Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").

#### Response roles.

For each prompt, we generate four candidate responses under the same rubric: a full-score response, a low-score response, a rubric-guided partial response, and an unguided response. These roles are not treated as four ordinal quality bins. Instead, the full-score and low-score responses provide fixed anchors, while the partial and unguided responses introduce broader intermediate variation under the same prompt and rubric. In the final benchmark, full-score responses all receive score 10, low-score responses all fall in the 0–3 score range, and the partial and unguided responses cover broader score distributions. We then use GPT-4o ([OpenAI, 2024](#bib.bib34)) as the operational reference judge to assign a binary satisfaction label to every response–criterion pair.

#### Final benchmark.

After filtering and validation, PointRubric contains 1,042 questions, 4,168 responses, and 25,008 response–criterion labels. For evaluation, we use a question-level split of 417 training questions, 104 development questions, and 521 held-out questions, so all responses to the same prompt remain within a single split. Appendices [A.2](#A1.SS2 "A.2 PointRubric Construction Details ‣ Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")–[A.6](#A1.SS6 "A.6 Reference Judge and Construction Prompts ‣ Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") give construction details; Appendix [F](#A6 "Appendix F Dataset Examples ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") gives a concrete example for PointRubric.

### 2.4 RaR-Science-Static

RaR-Science-Static complements PointRubric by testing the same pointwise judge methods in the downstream science-domain rubric format. It is built from RaR-Science, which uses instance-specific rubrics with variable numbers of criteria and absolute criterion weights ([Gunjal et al., 2026](#bib.bib20)). Unlike the RL experiments in §[5](#S5 "5 Probe-Based Rubric Rewards for RL ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), RaR-Science-Static is used only for static judge evaluation.

#### Response bank and split.

RaR-Science-Static contains 1,500 randomly sampled science questions. Each question keeps the original RaR-Science reference answer and receives one additional candidate response generated by greedy decoding from Qwen3-4B ([Yang et al., 2025](#bib.bib31)), giving 3,000 candidate responses evaluated under the same rubric. The rubrics contain between 6 and 11 criteria, with an average of 7.52 criteria per question. For evaluation, we use a fixed split of 1,000 training questions, 200 development questions, and 300 test questions.

#### Reference labels and aggregation.

We apply the same pointwise labeling protocol used for PointRubric: GPT-4o assigns a binary satisfaction label to each response–criterion pair. Scalar scores use the original RaR-Science criterion weights after converting pitfall criteria into the same satisfaction-label interface. Specifically, pitfall criteria with negative raw weights are treated as avoidance criteria, and scalar scores are aggregated with absolute weights so that higher satisfaction always corresponds to better rubric compliance. Appendices [A.7](#A1.SS7 "A.7 RaR-Science-Static Response Bank and Splits ‣ Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") and [A.8](#A1.SS8 "A.8 RaR-Science-Static Reference Labels and Aggregation ‣ Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") give the response-bank construction and aggregation details; Appendix [F](#A6 "Appendix F Dataset Examples ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") also contains a concrete example of RaR-Science-Static.

### 2.5 Reference Labels and Human Audit

Both data settings use GPT-4o as the operational reference judge for per-criterion labels. We treat these labels as an operational reference target rather than as human ground truth. The purpose of the benchmark is to test whether smaller local judges can approximate an expensive rubric-grading pipeline, so the human audit is a reliability check on this target rather than a replacement for larger human evaluation.

We manually audit 100 sampled responses from the held-out PointRubric split, covering 600 decisions and 50 paired response comparisons. The audit achieves 90.9% weighted criterion agreement with GPT-4o and 96.0% pairwise preference agreement. Disagreements are concentrated in softer qualitative criteria, such as completeness, specificity, and clarity, rather than hard factual or constraint-following criteria. Appendix [A.9](#A1.SS9 "A.9 Reference-Label Validation ‣ Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") gives the audit protocol and additional examples.

## 3 Rubric-Judge Methods

We now describe how each small language model is used as a rubric judge. All methods receive the same item-level input $(q,y,c_{j})$: a prompt, a candidate response, and one rubric criterion. Each method predicts whether the response satisfies the criterion, either as a binary verdict or as a satisfaction probability. The resulting criterion-level outputs are aggregated with the same rubric weights. We compare three scoring methods: Generative, Logprob, and Probe. We also use SFT as a post-training test, then apply the same three methods to the SFT backbone. [Table 2](#S3.T2 "Table 2 ‣ 3 Rubric-Judge Methods ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") summarizes the method matrix. Complete prompt templates used throughout the study are provided in Appendix [E](#A5 "Appendix E Prompts for Reproducibility ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").

| Method         | LM tuned? | Head?    | Output                   | RL use   |
|----------------|-----------|----------|--------------------------|----------|
| Generative     | $\times$  | $\times$ | Binary verdict           | Baseline |
| Logprob        | $\times$  | $\times$ | Satisfaction probability | –        |
| Probe          | $\times$  | $✓$      | Satisfaction probability | Main     |
| SFT Generative | $✓$       | $\times$ | Binary verdict           | –        |
| SFT Logprob    | $✓$       | $\times$ | Satisfaction probability | –        |
| SFT Probe      | $✓$       | $✓$      | Satisfaction probability | –        |

Table 2: Rubric-judge method matrix. All methods use the same item-level input $(q,y,c_{j})$ and the same rubric-weight aggregation rule. SFT changes the backbone state, while Generative, Logprob, and Probe define the criterion-level readout.

### 3.1 Scoring Methods

We compare three ways to extract criterion-level satisfaction signals from the same language-model backbone: generating a verdict, scoring fixed verbalizers, and probing hidden states.

#### Generative Judges.

Generative judges prompt the language model to produce a binary satisfaction verdict for one criterion. Parsed verdicts are aggregated with the rubric weights. Outputs that cannot be parsed into the required binary format are treated as invalid predictions.

#### Logprob Judges.

Logprob judges replace verdict generation with forced-choice scoring. Given the same item-level input, the model is asked to score the next-token probabilities of the fixed verbalizers “Yes” and “No” under the criterion prompt and compute their log-probability margin:

|     |                                                                                                      |     |
|-----|------------------------------------------------------------------------------------------------------|-----|
|     | $${\Delta_{j} = {{\log{P{(\text{Yes}\mid{q,y,c_{j}})}}} - {\log{P{(\text{No}\mid{q,y,c_{j}})}}}}}.$$ |     |

Binary static metrics threshold this margin at 0. Scalar rubric aggregation uses the soft score ${p_{j}\hspace{0pt}{(q,y)}} = {\sigma{(\Delta_{j})}}$. This method avoids parsing generated text. Appendix [B.1](#A2.SS1 "B.1 Generative and Logprob Judge Details ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") gives the verbalizers and scoring details.

#### Probe Judges.

Probe judges test whether hidden states encode the rubric judgment even when the model may not express it reliably through generated text ([Li et al., 2026](#bib.bib22)). We render the same single-criterion prompt, keep all language-model parameters frozen, and extract the final non-padding-token hidden state $h_{\ell}\hspace{0pt}{(q,y,c_{j})}$ at layer $\ell$. Only a lightweight linear classifier head is trained, using binary cross-entropy to predict the GPT-4o criterion label from this representation. Layer selection and the binary threshold use the development split. Scalar rubric scores and RL rewards use the unthresholded satisfaction probability. Appendix [B.2](#A2.SS2 "B.2 Probe Training and Calibration ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") gives the training and calibration details.

### 3.2 Post-training with Supervised Fine-tuning

Supervised fine-tuning (SFT) is our post-training test: it asks whether training a backbone to predict rubric verdicts makes it a better rubric judge. Each training example contains a prompt, a candidate response, the complete rubric, and the corresponding vector of GPT-4o Yes/No verdicts, following standard supervised instruction tuning ([Ouyang et al., 2022](#bib.bib9)). After SFT, we evaluate the resulting backbone with the same item-level Generative, Logprob, and Probe methods used for the base model. Therefore, SFT Generative, SFT Logprob, and SFT Probe differ from the corresponding base rows only in the backbone parameters, not in the scoring procedure. Appendix [B.3](#A2.SS3 "B.3 Supervised Fine-tuning Details ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") gives the SFT data format and evaluation setup.

|            | PointRubric |         |       |            |         |       | RaR-Science-Static |         |       |            |         |       |
|------------|-------------|---------|-------|------------|---------|-------|--------------------|---------|-------|------------|---------|-------|
|            | Base model  |         |       | SFT model  |         |       | Base model         |         |       | SFT model  |         |       |
| Model      | Generative  | Logprob | Probe | Generative | Logprob | Probe | Generative         | Logprob | Probe | Generative | Logprob | Probe |
| Qwen3-0.6B | 0.370       | 0.582   | 0.802 | 0.560      | 0.604   | 0.820 | 0.413              | 0.433   | 0.793 | 0.607      | 0.605   | 0.796 |
| Qwen3-1.7B | 0.518       | 0.766   | 0.875 | 0.902      | 0.713   | 0.845 | 0.443              | 0.449   | 0.835 | 0.708      | 0.520   | 0.828 |
| Qwen3-4B   | 0.790       | 0.893   | 0.913 | 0.808      | 0.892   | 0.906 | 0.496              | 0.738   | 0.851 | 0.673      | 0.794   | 0.845 |
| Qwen3-8B   | 0.888       | 0.907   | 0.914 | 0.846      | 0.895   | 0.912 | 0.609              | 0.756   | 0.864 | 0.642      | 0.754   | 0.861 |

Table 3: Static evaluator results on held-out splits. PointRubric values are weighted criterion accuracy with four candidate responses per question; RaR-Science values are criterion-level macro-F1 against GPT-4o labels with two candidate responses per question. Bold marks the best method for each model size within each benchmark.

## 4 Static Rubric-Judge Evaluation

![](img)

Before using a rubric judge as an RL reward model, we first evaluate whether small LMs can approximate criterion-level judgments on fixed response banks. Specifically, each judge receives a question, candidate response, and rubric criterion, and predicts whether the response satisfies that criterion. We compare three readouts from the same Qwen3 backbones: Generative verdicts, Yes/No Logprob scoring, and hidden-state Probes. All methods are evaluated against GPT-4o ([OpenAI, 2024](#bib.bib34)) criterion labels as the operational reference.

### 4.1 Experiment Setup

We evaluate Qwen3 judge backbones at four scales: 0.6B, 1.7B, 4B, and 8B parameters ([Yang et al., 2025](#bib.bib31)). For each backbone, we compare Generative, Logprob, and Probe judges, using both base and SFT models when applicable. All methods are evaluated on the same held-out question splits, and trained or calibrated components use only the corresponding training and development data. Appendix [B.4](#A2.SS4 "B.4 Static Evaluation Targets ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") defines the static criterion-satisfaction target and explains how binary verdicts, probabilities, and scalar rubric scores are computed.

We report one primary metric for each data setting. On PointRubric, the headline metric is weighted criterion accuracy, matching its hard/soft criterion weighting. On RaR-Science-Static, the headline metric is criterion-level macro-F1, since the downstream rubric setting has variable rubric lengths, weights, and label balance. Complementary metrics are reported in Appendix [B.7](#A2.SS7 "B.7 Static Metrics ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").

### 4.2 Static Judge Results

Table [3](#S3.T3 "Table 3 ‣ 3.2 Post-training with Supervised Fine-tuning ‣ 3 Rubric-Judge Methods ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") compares three ways of extracting criterion-level judgments from the same Qwen3 backbones.

#### PointRubric shows that small models can perform pointwise rubric judging when the benchmark format is controlled.

Base generative judge improves with scale, from 0.370 weighted criterion accuracy at 0.6B to 0.888 at 8B. SFT is especially effective for the 1.7B generative judge, which reaches 0.902, showing that a small model can learn the explicit Yes/No criterion-verdict format in this controlled setting.

#### On RaR-Science-Static, the readout method matters more than model size alone.

For the same 1.7B base backbone, Generative and Logprob reach only 0.443 and 0.449 macro-F1, while Probe reaches 0.835. This suggests that useful rubric-satisfaction information is present in the model’s hidden states but is not recovered reliably by Generative or Logprob scoring. An item-level comparison supports this interpretation: among 4,518 held-out criterion decisions, 33.0% are correct only under Probe, whereas 7.8% are correct only under Generative. Appendix [B.6](#A2.SS6 "B.6 Static Readout Error Analysis ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") reports the complete error decomposition and representative examples of both error directions.

#### Probe is the strongest readout on RaR-Science-Static across all model sizes.

The 1.7B Probe reaches 0.835 macro-F1, compared with 0.864 for the 8B Probe, while remaining substantially smaller than the 8B Generative judge baseline used later in RL. This makes Qwen3-1.7B Probe the natural candidate for the RL reward experiments: it is much smaller than the 8B Generative judge baseline while retaining strong criterion-level agreement on the downstream rubric format. Under response-generator shift, the unchanged 1.7B Probe reaches 0.741 macro-F1 on an extended 1,200-response bank with Mistral-7B-Instruct-v0.3 and OLMo-2-1124-7B-Instruct responses ([Jiang et al., 2023](#bib.bib32); [Team OLMo et al., 2025](#bib.bib33)), versus 0.394 for Generative and 0.424 for Logprob. Appendix [A.7](#A1.SS7.SSS0.Px1 "Extended held-out response bank. ‣ A.7 RaR-Science-Static Response Bank and Splits ‣ Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") reports the protocol and complementary metrics; Appendix [B.8](#A2.SS8 "B.8 Bootstrap Confidence Intervals ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") gives confidence intervals for Table [3](#S3.T3 "Table 3 ‣ 3.2 Post-training with Supervised Fine-tuning ‣ 3 Rubric-Judge Methods ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").

Comparison with a pairwise rubric reward model. Rubric-RM is designed to predict preferences between response pairs rather than criterion-level scores for individual responses ([Liu et al., 2026](#bib.bib21)). We therefore evaluate it as a static compatibility baseline on GPT-4o non-tied pairs, using the scalar scores from our pointwise judges to induce comparable pairwise rankings. The Qwen3-1.7B Probe reaches pairwise accuracies of 0.924 on PointRubric and 0.888 on RaR-Science-Static. Across Rubric-RM-4B and Rubric-RM-8B, the best corresponding accuracies are 0.322 and 0.487 when parse failures are counted as incorrect, or 0.575 and 0.670 when evaluation is restricted to parseable outputs. These results show that Rubric-RM captures useful pairwise signal when its outputs are parseable, but its pairwise interface and frequent formatting failures prevent it from serving as a direct criterion-level reward in our RL pipeline. Appendix [B.5](#A2.SS5 "B.5 Rubric-RM Pairwise Comparison ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") reports the per-model results, parse rates, and evaluation conventions.

### 4.3 Selecting the Probe Configuration for RL

Table [4](#S4.T4 "Table 4 ‣ 4.3 Selecting the Probe Configuration for RL ‣ 4 Static Rubric-Judge Evaluation ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") studies the data efficiency and readout design of Qwen3-1.7B Probes on RaR-Science-Static. The linear last-token probe is already strong with limited supervision, reaching 0.805 macro-F1 with 100 training questions and 0.834 with 1,000 training questions. The architecture variants provide only modest gains: MLP heads and last-4-layer averaging are close to the linear last-token probe, while mean pooling is substantially worse. We use the same linear last-token design for the main RL reward, fitted separately on 450 training and 50 development responses as described in Appendix [B.2](#A2.SS2 "B.2 Probe Training and Calibration ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"). It is simpler, nearly matches the strongest ablations, directly produces criterion-level probabilities, and avoids generated-verdict parsing. The full layer sweep in Appendix [B.9](#A2.SS9 "B.9 Probe Layer Selection ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") shows that layer selection lies on a broad late-layer plateau rather than a single isolated optimum. This configuration gives a compact reward judge, so Section [5](#S5 "5 Probe-Based Rubric Rewards for RL ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") evaluates whether it remains useful inside the RL loop as an online reward model.

| Ablation | Probe setting             | \# Train q. | Macro-F1 |
|----------|---------------------------|-------------|----------|
|          | Linear, last token        | 50          | 0.767    |
|          | Linear, last token        | 100         | 0.805    |
| Data     | Linear, last token        | 250         | 0.818    |
|          | Linear, last token        | 500         | 0.828    |
|          | Linear, last token        | 1000        | 0.834    |
|          | Linear, last token        | 1000        | 0.834    |
|          | MLP-32, last token        | 1000        | 0.834    |
| Design   | MLP-64, last token        | 1000        | 0.840    |
|          | Linear, mean pooling      | 1000        | 0.761    |
|          | Linear, last-4-layer mean | 1000        | 0.839    |

Table 4: Qwen3-1.7B Probe ablations on RaR-Science-Static. Data rows vary the number of training questions for the linear last-token probe. Design rows use 1,000 training questions and compare alternative heads and pooling strategies.

## 5 Probe-Based Rubric Rewards for RL

Section [4](#S4 "4 Static Rubric-Judge Evaluation ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") selects Qwen3-1.7B Probe as a compact criterion-level judge. We now test whether this judge remains useful when used inside the RL loop, whether the learned signal transfers beyond the exact training setting, and how its quality-efficiency tradeoff compares with a larger generative judge.

### 5.1 Matched RL Protocol and Results

![](img)

| Reward model      | Method     | RaR-Science score | Score gain |
|-------------------|------------|-------------------|------------|
| Base actor, no RL | –          | 0.232             | –          |
| Qwen3-0.6B        | Probe      | 0.562             | +0.330     |
| Qwen3-1.7B        | Probe      | 0.643             | +0.411     |
| Qwen3-4B          | Probe      | 0.588             | +0.356     |
| Qwen3-8B          | Probe      | 0.506             | +0.274     |
| Qwen3-8B          | Generative | 0.594             | +0.362     |

Table 5: Matched Reward-model Comparison on RaR-Science. All non-base rows train the same Qwen3-4B-Base actor with the same GRPO configuration and are evaluated by the same GPT-4o rubric evaluator. The only experimental variable is the reward judge.

|  Policy               | GPQA-Diamond acc. | $\Delta$ |
|-----------------------|-------------------|----------|
|  Base actor           | 0.335 $\pm$ 0.023 | –        |
|  Probe-reward policy  | 0.388 $\pm$ 0.037 | +0.053   |

Table 6: Policy transfer to GPQA-Diamond. Accuracy is averaged over four evaluation runs on the 198-question GPQA-Diamond split, where in each run, the answer options are shown in a different order. The probe-reward policy is trained on RaR-Science using the Qwen3-1.7B Probe reward.

| Train    | Eval     | Macro-F1 | Score MAE | Pearson |
|----------|----------|----------|-----------|---------|
| Science  | Science  | 0.754    | 0.187     | 0.720   |
| Science  | Medicine | 0.718    | 0.091     | 0.789   |
| Medicine | Medicine | 0.782    | 0.140     | 0.620   |
| Medicine | Science  | 0.702    | 0.240     | 0.580   |

Table 7: Static judge transfer across rubric domains. Probes are trained on source-domain criterion labels and evaluated against GPT-4o criterion labels on the target domain without target-domain fitting.

| Reward judge             | Cumulative judge time | Validation judge time | RL elapsed time | RaR-Science score |
|--------------------------|-----------------------|-----------------------|-----------------|-------------------|
| Qwen3-1.7B Probe         | 2.33h                 | 31.1s                 | 8h 51m 47s      | 0.643             |
| Qwen3-8B Generative      | 24.98h                | 492.0s                | 11h 11m 56s     | 0.594             |
| Generative / Probe ratio | 10.7$\times$          | 15.8$\times$          | 1.26$\times$    | –                 |

Table 8: Efficiency-quality comparison for the Qwen3-1.7B Probe judge and the generative baseline. Judge time is measured through the same checkpoint used in Table [5](#S5.T5 "Table 5 ‣ 5.1 Matched RL Protocol and Results ‣ 5 Probe-Based Rubric Rewards for RL ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"). Policy quality for both runs is measured by GPT-4o. The Generative judge requires 10.7$\times$ as much cumulative judge time while producing a lower-scoring policy.

We test whether the selected Qwen3-1.7B Probe can serve as the reward model for rubric-based RL. All controlled runs train the same Qwen3-4B-Base actor with GRPO ([Shao et al., 2024](#bib.bib12)) on the same RaR-Science training set. The actor, optimizer, schedule, response budget, aggregation rule, and final GPT-4o evaluator are fixed; only the reward judge changes. Full configuration details are given in Appendix [C.1](#A3.SS1 "C.1 RL Reward Configuration ‣ Appendix C Rubric RL Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), and development checks are summarized in Appendix [C.6](#A3.SS6 "C.6 Additional RL Configuration Checks ‣ Appendix C Rubric RL Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").

#### The Qwen3-1.7B Probe reward produces the strongest trained policy.

Table [5](#S5.T5 "Table 5 ‣ 5.1 Matched RL Protocol and Results ‣ 5 Probe-Based Rubric Rewards for RL ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") reports the controlled reward-model comparison. Starting from the same base actor, the Qwen3-1.7B Probe reward improves the final RaR-Science rubric score from 0.232 to 0.643. Under the same training and evaluation protocol, the larger Qwen3-8B Generative reward reaches 0.594. Thus, the compact Probe reward trains a higher-scoring policy than the larger Generative judge in this matched RL setting. Appendix [C.2](#A3.SS2 "C.2 RL Score Confidence Intervals ‣ Appendix C Rubric RL Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") reports bootstrap confidence intervals, and Appendix [C.3](#A3.SS3 "C.3 On-Policy Reward Dynamics and Qualitative Cases ‣ Appendix C Rubric RL Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") gives representative policy improvements and failure cases.

#### Downstream reward utility does not exactly follow static judge accuracy.

Although the 4B and 8B Probes achieve slightly higher fixed-bank macro-F1 in Table [3](#S3.T3 "Table 3 ‣ 3.2 Post-training with Supervised Fine-tuning ‣ 3 Rubric-Judge Methods ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), the 1.7B Probe produces the strongest externally evaluated policy after GRPO. On-policy reward diagnostics suggest a possible explanation: the larger Probes assign more saturated rewards to actor rollouts, reducing the within-group reward variation available to GRPO. We therefore select the reward judge by downstream policy improvement under the controlled RL protocol. Appendix [C.3](#A3.SS3 "C.3 On-Policy Reward Dynamics and Qualitative Cases ‣ Appendix C Rubric RL Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") reports the corresponding reward-distribution and saturation statistics.

#### A blind human audit supports the main policy comparison.

The probe-reward policy is preferred over the base actor on 72 out of 100 examples, while GPT-4o rubric preference favors the probe policy on 80 out of the same 100 pairs. After excluding human Tie/Unsure labels and GPT-4o exact ties, human and GPT-4o preferences agree on 69 of 72 cases (95.8%). Among the 13 human ties, GPT-4o also assigns similar scores: 7 have an absolute score gap at most 0.05, and 11 have a gap below 0.20. These checks support the operational GPT-4o target rather than replacing a larger human evaluation. Appendix [C.5](#A3.SS5 "C.5 Human Audit and Reference-Judge Validation ‣ Appendix C Rubric RL Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") gives the audit protocol, tie analysis, and reference-judge validation.

### 5.2 Transfer Results

![](img)

We evaluate transfer in two ways: whether the policy trained with the probe reward improves outside the RaR-Science rubric format, and whether the Qwen3-1.7B Probe’s criterion-satisfaction signal transfers from science rubrics to medical rubrics without target-domain fitting. The evaluation protocols are defined in Appendix [D](#A4 "Appendix D Generalization Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").

Table [6](#S5.T6 "Table 6 ‣ 5.1 Matched RL Protocol and Results ‣ 5 Probe-Based Rubric Rewards for RL ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") compares the base Qwen3-4B actor with the policy trained using the Qwen3-1.7B Probe reward. On 198 GPQA-Diamond questions ([Rein et al., 2024](#bib.bib30)) across four answer-order runs, the probe-reward policy improves accuracy from 0.335 to 0.388, suggesting that the policy improvement can generalize beyond the RaR-Science rubric-scoring format.

Table [7](#S5.T7 "Table 7 ‣ 5.1 Matched RL Protocol and Results ‣ 5 Probe-Based Rubric Rewards for RL ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") evaluates whether the probe’s criterion-satisfaction signal transfers across domains. A Qwen3-1.7B linear probe trained on RaR-Science criterion labels reaches 0.718 macro-F1 on RaR-Medicine without Medicine labels for fitting. This is below the Medicine-trained in-domain probe, but shows that the RaR-Science-trained probe retains meaningful criterion-level agreement under a different rubric distribution.

### 5.3 Efficiency-Quality Results

![](img)

Table [8](#S5.T8 "Table 8 ‣ 5.1 Matched RL Protocol and Results ‣ 5 Probe-Based Rubric Rewards for RL ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") compares the two reward judges in the matched RL comparison: Qwen3-1.7B Probe and Qwen3-8B Generative. The actor, training data, GRPO configuration, response budget, rubric aggregation rule, and external GPT-4o evaluator are fixed; only the reward judge changes. The RL reward Probe is trained once on 500 GPT-4o-labeled responses (3,766 criterion labels; approximately \$2.43). The frozen Probe can then be reused for subsequent RL runs in the same rubric setting without further GPT-4o calls or recalibration. At reward time, the Probe requires substantially less judging computation. By the comparison checkpoint, Generative requires 89,912.1 seconds of cumulative judge time versus 8,389.9 seconds for Probe, a 10.7$\times$ ratio. On validation, Generative takes 492.0 seconds versus Probe’s 31.1 seconds (15.8$\times$).

The efficiency result should be read with policy quality. Probe reaches a higher RaR-Science score, 0.643 versus 0.594, while using 2.33 judge-hours instead of 24.98 judge-hours. The wall-clock reduction is smaller because reward calls are parallelized and actor rollout, reference-model scoring, optimization, and checkpointing remain in the loop. The key result is not only lower judge cost: the Probe reward produces the stronger policy while requiring substantially less reward-judge computation. Appendix [C.4](#A3.SS4 "C.4 Efficiency Measurement ‣ Appendix C Rubric RL Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") gives the timing definitions and training-only calculation.

## 6 Related Work

#### Rubric-based RL.

Reinforcement learning with verifiable rewards works well when correctness can be checked by rule-based verifiers ([Le et al., 2022](#bib.bib14); [Shao et al., 2024](#bib.bib12); [Wen et al., 2025](#bib.bib10); [Guo et al., 2025](#bib.bib13)). Open-ended tasks require broader feedback, motivating rubric-style evaluation, rubric resources, and rubric-based RL ([Arora et al., 2025](#bib.bib23); [Liu et al., 2026](#bib.bib21); [Gunjal et al., 2026](#bib.bib20); [Shao et al., 2026](#bib.bib26)). RaR-Science is closest to our downstream setting because it uses instance-specific science rubrics as scalar rewards for policy optimization ([Gunjal et al., 2026](#bib.bib20)). Our work keeps the reward formulation fixed and studies the judge that applies the rubric, replacing repeated calls to a large judge with a smaller criterion-level evaluator.

#### LLM-as-a-judge and small evaluators.

LLM-as-a-judge methods use language models to score, compare, or critique open-ended responses ([Zheng et al., 2023](#bib.bib11); [Liu et al., 2023b](#bib.bib1); [Ma et al., 2025](#bib.bib4); [Gu et al., 2026](#bib.bib15)). Trained open judges extend this idea by fine-tuning models for evaluation ([Wang et al., 2024](#bib.bib16); [Li et al., 2024](#bib.bib18); [Kim et al., 2024b](#bib.bib2); [Zhu et al., 2025](#bib.bib17)). Examples of related rubric-oriented evaluators include LLM-Rubric, which studies calibrated multidimensional evaluation ([Hashemi et al., 2024](#bib.bib7)), and works such as FLAMe and Prometheus, which train open autoraters for rubric- or instruction-conditioned evaluation ([Vu et al., 2024](#bib.bib8); [Kim et al., 2024a](#bib.bib40)). Recent evaluator benchmarks study reward-model and judge reliability across evaluation formats ([Lambert et al., 2025](#bib.bib3); [Zhao et al., 2025](#bib.bib6); [Wen et al., 2026](#bib.bib28)). Work on compact evaluators and hidden-state judges further suggests that smaller models can contain useful evaluative signals even when generation is weak ([Liu et al., 2023c](#bib.bib5); [Alexandru et al., 2025](#bib.bib19); [Li et al., 2026](#bib.bib22); [Gisserot-Boukhlef et al., 2026](#bib.bib27)). Our work differs by keeping the language-model backbone frozen, training only a lightweight criterion classifier, and using its satisfaction probabilities as repeated rewards for rubric-based RL.

## 7 Conclusion

We study whether small LMs can serve as criterion-level rubric judges for rubric-based RL. We derive PointRubric from OpenRubrics and construct RaR-Science-Static from RaR-Science to test the evaluation capabilities of small judges. Across both datasets, Probe judges perform best, showing that 1.7B-scale models encode useful rubric-satisfaction signals in hidden states. When used as an RL reward model, the Qwen3-1.7B Probe judge trains a policy that outperforms an 8B Generative judge reward baseline while using far less judge time. Transfer experiments evaluate both policy transfer and judge transfer: the Probe-reward policy improves GPQA-Diamond accuracy, while a RaR-Science-trained Probe retains criterion-level agreement on RaR-Medicine. Overall, small Probe judges provide an effective and efficient reward model for rubric-based RL.

## Limitations

Our supervised target is GPT-4o criterion scoring, not direct human ground truth. This matches the operational goal of the paper: approximating the expensive rubric judge used in the studied rubric-RL pipeline. Human preference comparisons and independent rescoring in Appendix [C](#A3 "Appendix C Rubric RL Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") support the validity of this target in our setting, but broader human evaluation would be needed to characterize agreement across tasks and domains.

Our strongest evidence is on RaR-Science questions, with additional checks on GPQA-Diamond and RaR-Medicine. These results show useful transfer beyond the calibration setting, but do not imply domain-invariant rubric judgment. New domains, especially dialogue, long-form instruction following, or safety-critical expert settings, may require additional calibration and validation. Similarly, the RL experiments control the actor, reward aggregation, and training configuration, but cover one policy family and one rubric-RL setup; we therefore treat the human audit and independent-reference checks as setting-specific evidence against reward overoptimization.

Finally, the efficiency results are measurements of our implementation and hardware. We report cumulative judge time, validation reward time, and elapsed RL time from matched runs. The judge-time advantage is larger than the wall-clock advantage because reward calls are parallelized and other RL costs remain in the loop, so the reported ratios should be interpreted as empirical measurements for this setup rather than universal serving constants.

## Ethical considerations

This work reuses two public research datasets, OpenRubrics and RaR-Science ([Liu et al., 2026](#bib.bib21); [Gunjal et al., 2026](#bib.bib20)). We use these resources for research on rubric judging and cite the original papers. PointRubric is derived from OpenRubrics, and RaR-Science-Static is derived from RaR-Science by adding a fixed response bank and reference labels for static judge evaluation. We do not claim ownership of the original prompts, rubrics, or reference answers. Any released version of our derived data should retain the original source attribution and follow the usage terms provided by the original dataset authors.

The datasets contain model prompts, rubrics, reference answers, and model responses. We do not collect or add private user data, demographic attributes, or personal identifiers. During construction and validation, we manually inspected sampled examples and generated responses for obvious personally identifying information and unsafe or offensive content. We did not intentionally retain any newly introduced personal identifiers. Because PointRubric and RaR-Science-Static are derived from public research datasets and model-generated responses, residual unsafe, biased, sensitive, or offensive content may still be inherited from the source artifacts or produced by models. We therefore treat the derived artifacts as research-only evaluator resources, and our benchmark should not be treated as a guarantee that a judge is safe for deployment.

We conduct two small human audits: one audit of PointRubric reference labels and one blind pairwise audit of the main RL comparison. Annotators are asked only to evaluate model responses against provided rubrics or to compare two model responses. The annotators were members of the research team, so no external recruitment or payment was involved. The tasks do not ask annotators to disclose personal information, and we store and report only aggregate agreement or preference statistics. The audits are used as reliability checks for the operational GPT-4o reference target, not as standalone human preference datasets or as a replacement for broader human evaluation.

## Acknowledgements

The authors gratefully acknowledge the NYU High Performance Computing Torch cluster for providing the computational resources used in this work.

## References

- Alexandru et al. (2025) A. Alexandru, A. Calvi, H. Broomfield, J. Golden, K. Dai, M. Leys, M. Burger, M. Bartolo, R. Engeler, S. Pisupati, T. Drane, and Y. S. Park Atla selene mini: a general purpose evaluation model. arXiv preprint arXiv:2501.17195. External Links: [Document](https://dx.doi.org/10.48550/arXiv.2501.17195), [Link](https://arxiv.org/abs/2501.17195) Cited by: [§6](#S6.SS0.SSS0.Px2.p1.1 "LLM-as-a-judge and small evaluators. ‣ 6 Related Work ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Arora et al. (2025) R. K. Arora, J. Wei, R. S. Hicks, P. Bowman, J. Quiñonero-Candela, F. Tsimpourlas, M. Sharman, M. Shah, A. Vallone, A. Beutel, J. Heidecke, and K. Singhal HealthBench: evaluating large language models towards improved human health. arXiv preprint arXiv:2505.08775. External Links: [Document](https://dx.doi.org/10.48550/arXiv.2505.08775), [Link](https://arxiv.org/abs/2505.08775) Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§1](#S1.p3.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [Table 1](#S2.T1.2.1.3.1 "In 2 Rubric Judging Task and Dataset ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§6](#S6.SS0.SSS0.Px1.p1.1 "Rubric-based RL. ‣ 6 Related Work ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Citron (2024) D. Citron Try deep research and our new experimental model in Gemini, your AI assistant. Note: [https://blog.google/products-and-platforms/products/gemini/google-gemini-deep-research/](https://blog.google/products-and-platforms/products/gemini/google-gemini-deep-research/)Accessed: 2026-08-27 Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Gisserot-Boukhlef et al. (2026) H. Gisserot-Boukhlef, N. Boizard, E. Malherbe, C. Hudelot, and P. Colombo BERT-as-a-judge: a robust alternative to lexical methods for efficient reference-based LLM evaluation. arXiv preprint arXiv:2604.09497. External Links: [Document](https://dx.doi.org/10.48550/arXiv.2604.09497), [Link](https://arxiv.org/abs/2604.09497) Cited by: [§1](#S1.p4.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§6](#S6.SS0.SSS0.Px2.p1.1 "LLM-as-a-judge and small evaluators. ‣ 6 Related Work ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Gu et al. (2026) J. Gu, X. Jiang, Z. Shi, H. Tan, X. Zhai, C. Xu, W. Li, Y. Shen, S. Ma, H. Liu, S. Wang, K. Zhang, Z. Lin, B. Zhang, L. M. Ni, W. Gao, Y. Wang, and J. Guo A survey on LLM-as-a-judge. The Innovation 7 (6), pp. 101253. External Links: [Document](https://dx.doi.org/10.1016/j.xinn.2025.101253), [Link](https://doi.org/10.1016/j.xinn.2025.101253) Cited by: [§6](#S6.SS0.SSS0.Px2.p1.1 "LLM-as-a-judge and small evaluators. ‣ 6 Related Work ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Gunjal et al. (2026) A. Gunjal, A. Wang, E. Lau, V. Nath, Y. He, B. Liu, and S. Hendryx Rubrics as rewards: reinforcement learning beyond verifiable domains. In International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=c1bTcrDmt4) Cited by: [§A.7](#A1.SS7.p1.1 "A.7 RaR-Science-Static Response Bank and Splits ‣ Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [Table C.1](#A3.T1.2.3.2.1.1 "In Appendix C Rubric RL Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§1](#S1.p1.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§1](#S1.p2.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§1](#S1.p3.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§1](#S1.p5.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§2.4](#S2.SS4.p1.1 "2.4 RaR-Science-Static ‣ 2 Rubric Judging Task and Dataset ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [Table 1](#S2.T1.2.1.7.1 "In 2 Rubric Judging Task and Dataset ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§6](#S6.SS0.SSS0.Px1.p1.1 "Rubric-based RL. ‣ 6 Related Work ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [Ethical considerations](#Sx2.p1.1 "Ethical considerations ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Guo et al. (2025) D. Guo, D. Yang, H. Zhang, J. Song, P. Wang, Q. Zhu, R. Xu, R. Zhang, S. Ma, X. Bi, X. Zhang, X. Yu, Y. Wu, Z. F. Wu, Z. Gou, Z. Shao, Z. Li, Z. Gao, A. Liu, B. Xue, B. Wang, B. Wu, B. Feng, C. Lu, C. Zhao, C. Deng, C. Ruan, D. Dai, D. Chen, D. Ji, E. Li, F. Lin, F. Dai, F. Luo, G. Hao, G. Chen, G. Li, H. Zhang, H. Xu, H. Ding, H. Gao, H. Qu, H. Li, J. Guo, J. Li, J. Chen, J. Yuan, J. Tu, J. Qiu, J. Li, J. L. Cai, J. Ni, J. Liang, J. Chen, K. Dong, K. Hu, K. You, K. Gao, K. Guan, K. Huang, K. Yu, L. Wang, L. Zhang, L. Zhao, L. Wang, L. Zhang, L. Xu, L. Xia, M. Zhang, M. Zhang, M. Tang, M. Zhou, M. Li, M. Wang, M. Li, N. Tian, P. Huang, P. Zhang, Q. Wang, Q. Chen, Q. Du, R. Ge, R. Zhang, R. Pan, R. Wang, R. J. Chen, R. L. Jin, R. Chen, S. Lu, S. Zhou, S. Chen, S. Ye, S. Wang, S. Yu, S. Zhou, S. Pan, S. S. Li, S. Zhou, S. Wu, T. Yun, T. Pei, T. Sun, T. Wang, W. Zeng, W. Liu, W. Liang, W. Gao, W. Yu, W. Zhang, W. L. Xiao, W. An, X. Liu, X. Wang, X. Chen, X. Nie, X. Cheng, X. Liu, X. Xie, X. Liu, X. Yang, X. Li, X. Su, X. Lin, X. Q. Li, X. Jin, X. Shen, X. Chen, X. Sun, X. Wang, X. Song, X. Zhou, X. Wang, X. Shan, Y. K. Li, Y. Q. Wang, Y. X. Wei, Y. Zhang, Y. Xu, Y. Li, Y. Zhao, Y. Sun, Y. Wang, Y. Yu, Y. Zhang, Y. Shi, Y. Xiong, Y. He, Y. Piao, Y. Wang, Y. Tan, Y. Ma, Y. Liu, Y. Guo, Y. Ou, Y. Wang, Y. Gong, Y. Zou, Y. He, Y. Xiong, Y. Luo, Y. You, Y. Liu, Y. Zhou, Y. X. Zhu, Y. Huang, Y. Li, Y. Zheng, Y. Zhu, Y. Ma, Y. Tang, Y. Zha, Y. Yan, Z. Z. Ren, Z. Ren, Z. Sha, Z. Fu, Z. Xu, Z. Xie, Z. Zhang, Z. Hao, Z. Ma, Z. Yan, Z. Wu, Z. Gu, Z. Zhu, Z. Liu, Z. Li, Z. Xie, Z. Song, Z. Pan, Z. Huang, Z. Xu, Z. Zhang, and Z. Zhang DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning. Nature 645 (8081), pp. 633–638. External Links: [Document](https://dx.doi.org/10.1038/s41586-025-09422-z), [Link](https://doi.org/10.1038/s41586-025-09422-z) Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§6](#S6.SS0.SSS0.Px1.p1.1 "Rubric-based RL. ‣ 6 Related Work ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Hashemi et al. (2024) H. Hashemi, J. Eisner, C. Rosset, B. Van Durme, and C. Kedzie LLM-rubric: a multidimensional, calibrated approach to automated evaluation of natural language texts. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), L. Ku, A. Martins, and V. Srikumar (Eds.), Bangkok, Thailand, pp. 13806–13834. External Links: [Link](https://aclanthology.org/2024.acl-long.745/), [Document](https://dx.doi.org/10.18653/v1/2024.acl-long.745) Cited by: [§6](#S6.SS0.SSS0.Px2.p1.1 "LLM-as-a-judge and small evaluators. ‣ 6 Related Work ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Hu et al. (2022) E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, and W. Chen LoRA: low-rank adaptation of large language models. In International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=nZeVKeeFYf9) Cited by: [Table B.2](#A2.T2.2.4.2.1.1 "In B.3 Supervised Fine-tuning Details ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Jiang et al. (2023) A. Q. Jiang, A. Sablayrolles, A. Mensch, C. Bamford, D. S. Chaplot, D. de las Casas, F. Bressand, G. Lengyel, G. Lample, L. Saulnier, L. Renard Lavaud, M. Lachaux, P. Stock, T. Le Scao, T. Lavril, T. Wang, T. Lacroix, and W. El Sayed Mistral 7b. arXiv preprint arXiv:2310.06825. External Links: [Document](https://dx.doi.org/10.48550/arXiv.2310.06825), [Link](https://arxiv.org/abs/2310.06825) Cited by: [§A.7](#A1.SS7.SSS0.Px1.p1.1 "Extended held-out response bank. ‣ A.7 RaR-Science-Static Response Bank and Splits ‣ Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§4.2](#S4.SS2.SSS0.Px3.p1.1 "Probe is the strongest readout on RaR-Science-Static across all model sizes. ‣ 4.2 Static Judge Results ‣ 4 Static Rubric-Judge Evaluation ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Kim et al. (2024a) S. Kim, J. Shin, Y. Cho, J. Jang, S. Longpre, H. Lee, S. Yun, R. S. Shin, S. Kim, J. Thorne, and M. Seo Prometheus: inducing fine-grained evaluation capability in language models. In International Conference on Learning Representations, External Links: [Link](https://proceedings.iclr.cc/paper_files/paper/2024/hash/803485352e61e3ebf41221e4776c9fd4-Abstract-Conference.html) Cited by: [§6](#S6.SS0.SSS0.Px2.p1.1 "LLM-as-a-judge and small evaluators. ‣ 6 Related Work ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Kim et al. (2024b) S. Kim, J. Suk, S. Longpre, B. Y. Lin, J. Shin, S. Welleck, G. Neubig, M. Lee, K. Lee, and M. Seo Prometheus 2: an open source language model specialized in evaluating other language models. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing, Y. Al-Onaizan, M. Bansal, and Y. Chen (Eds.), Miami, Florida, USA, pp. 4334–4353. External Links: [Link](https://aclanthology.org/2024.emnlp-main.248/), [Document](https://dx.doi.org/10.18653/v1/2024.emnlp-main.248) Cited by: [§1](#S1.p2.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§6](#S6.SS0.SSS0.Px2.p1.1 "LLM-as-a-judge and small evaluators. ‣ 6 Related Work ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Lambert et al. (2025) N. Lambert, V. Pyatkin, J. Morrison, L. Miranda, B. Y. Lin, K. Chandu, N. Dziri, S. Kumar, T. Zick, Y. Choi, N. A. Smith, and H. Hajishirzi RewardBench: evaluating reward models for language modeling. In Findings of the Association for Computational Linguistics: NAACL 2025, L. Chiruzzo, A. Ritter, and L. Wang (Eds.), Albuquerque, New Mexico, pp. 1755–1797. External Links: [Link](https://aclanthology.org/2025.findings-naacl.96/), [Document](https://dx.doi.org/10.18653/v1/2025.findings-naacl.96), ISBN 979-8-89176-195-7 Cited by: [§1](#S1.p3.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§2.1](#S2.SS1.p1.1 "2.1 Our Task: Pointwise Rubric Judging ‣ 2 Rubric Judging Task and Dataset ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [Table 1](#S2.T1.2.1.8.1 "In 2 Rubric Judging Task and Dataset ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§6](#S6.SS0.SSS0.Px2.p1.1 "LLM-as-a-judge and small evaluators. ‣ 6 Related Work ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Le et al. (2022) H. Le, Y. Wang, A. D. Gotmare, S. Savarese, and S. C. H. Hoi CodeRL: mastering code generation through pretrained models and deep reinforcement learning. In Advances in Neural Information Processing Systems, Vol. 35, pp. 21314–21328. External Links: [Document](https://dx.doi.org/10.52202/068431-1549), [Link](https://proceedings.neurips.cc/paper_files/paper/2022/hash/8636419dea1aa9fbd25fc4248e702da4-Abstract-Conference.html) Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§6](#S6.SS0.SSS0.Px1.p1.1 "Rubric-based RL. ‣ 6 Related Work ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Li et al. (2024) J. Li, S. Sun, W. Yuan, R. Fan, H. Zhao, and P. Liu Generative judge for evaluating alignment. In International Conference on Learning Representations, Vol. 2024, pp. 27547–27574. External Links: [Link](https://proceedings.iclr.cc/paper_files/paper/2024/file/747dc7c6566c74eb9a663bcd8d057c78-Paper-Conference.pdf) Cited by: [§6](#S6.SS0.SSS0.Px2.p1.1 "LLM-as-a-judge and small evaluators. ‣ 6 Related Work ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Li et al. (2026) Z. Li, Y. Zhang, M. Li, Y. Ji, Y. Zeng, N. Cheng, Y. Zhu, Y. Wang, S. Wang, J. Xiao, and D. He Rethinking LLM-as-a-judge: representation-as-a-judge with small language models via semantic capacity asymmetry. In International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=VAISvCsrvG) Cited by: [§1](#S1.p4.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§3.1](#S3.SS1.SSS0.Px3.p1.1 "Probe Judges. ‣ 3.1 Scoring Methods ‣ 3 Rubric-Judge Methods ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§6](#S6.SS0.SSS0.Px2.p1.1 "LLM-as-a-judge and small evaluators. ‣ 6 Related Work ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Liu et al. (2023a) J. Liu, Y. Zhu, K. Xiao, Q. Fu, X. Han, W. Yang, and D. Ye RLTF: reinforcement learning from unit test feedback. Transactions on Machine Learning Research. External Links: ISSN 2835-8856, [Link](https://openreview.net/forum?id=hjYmsV6nXZ) Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Liu et al. (2026) T. Liu, R. Xu, T. Yu, I. Hong, C. Yang, T. Zhao, and H. Wang OpenRubrics: towards scalable synthetic rubric generation for reward modeling and LLM alignment. In Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), San Diego, California, United States, pp. 17417–17437. External Links: [Document](https://dx.doi.org/10.18653/v1/2026.acl-long.791), [Link](https://aclanthology.org/2026.acl-long.791/) Cited by: [§A.2](#A1.SS2.p1.1 "A.2 PointRubric Construction Details ‣ Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§B.5](#A2.SS5.p1.1 "B.5 Rubric-RM Pairwise Comparison ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§1](#S1.p3.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [Table 1](#S2.T1.2.1.6.1 "In 2 Rubric Judging Task and Dataset ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§4.2](#S4.SS2.SSS0.Px3.p2.1 "Probe is the strongest readout on RaR-Science-Static across all model sizes. ‣ 4.2 Static Judge Results ‣ 4 Static Rubric-Judge Evaluation ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§6](#S6.SS0.SSS0.Px1.p1.1 "Rubric-based RL. ‣ 6 Related Work ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [Ethical considerations](#Sx2.p1.1 "Ethical considerations ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Liu et al. (2023b) Y. Liu, D. Iter, Y. Xu, S. Wang, R. Xu, and C. Zhu G-eval: NLG evaluation using gpt-4 with better human alignment. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, H. Bouamor, J. Pino, and K. Bali (Eds.), Singapore, pp. 2511–2522. External Links: [Link](https://aclanthology.org/2023.emnlp-main.153/), [Document](https://dx.doi.org/10.18653/v1/2023.emnlp-main.153) Cited by: [§6](#S6.SS0.SSS0.Px2.p1.1 "LLM-as-a-judge and small evaluators. ‣ 6 Related Work ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Liu et al. (2023c) Y. Liu, A. R. Fabbri, Y. Zhao, P. Liu, S. Joty, C. Wu, C. Xiong, and D. Radev Towards interpretable and efficient automatic reference-based summarization evaluation. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, EMNLP 2023, Singapore, December 6-10, 2023, H. Bouamor, J. Pino, and K. Bali (Eds.), pp. 16360–16368. External Links: [Link](https://doi.org/10.18653/v1/2023.emnlp-main.1018), [Document](https://dx.doi.org/10.18653/V1/2023.EMNLP-MAIN.1018) Cited by: [§6](#S6.SS0.SSS0.Px2.p1.1 "LLM-as-a-judge and small evaluators. ‣ 6 Related Work ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Loshchilov and Hutter (2019) I. Loshchilov and F. Hutter Decoupled weight decay regularization. In International Conference on Learning Representations, External Links: [Link](https://openreview.net/forum?id=Bkg6RiCqY7) Cited by: [Table B.2](#A2.T2.2.8.2.1.1 "In B.3 Supervised Fine-tuning Details ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [Table C.1](#A3.T1.2.17.2.1.1 "In Appendix C Rubric RL Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Ma et al. (2025) C. Ma, E. Zhang, Y. Zhao, W. Liu, Y. Jia, P. Qing, L. Shi, A. Cohan, Y. Yan, and S. Vosoughi Judging with many minds: do more perspectives mean less prejudice? on bias amplification and resistance in multi-agent based llm-as-judge. In Findings of the Association for Computational Linguistics: EMNLP 2025, Suzhou, China, November 4-9, 2025, C. Christodoulopoulos, T. Chakraborty, C. Rose, and V. Peng (Eds.), pp. 17356–17392. External Links: [Link](https://doi.org/10.18653/v1/2025.findings-emnlp.941), [Document](https://dx.doi.org/10.18653/V1/2025.FINDINGS-EMNLP.941) Cited by: [§6](#S6.SS0.SSS0.Px2.p1.1 "LLM-as-a-judge and small evaluators. ‣ 6 Related Work ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- OpenAI (2024) OpenAI GPT-4o system card. Note: [https://openai.com/index/gpt-4o-system-card/](https://openai.com/index/gpt-4o-system-card/)Accessed: 2026-08-27 Cited by: [§A.6](#A1.SS6.p1.1 "A.6 Reference Judge and Construction Prompts ‣ Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§A.8](#A1.SS8.p1.1 "A.8 RaR-Science-Static Reference Labels and Aggregation ‣ Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§B.4](#A2.SS4.p1.2 "B.4 Static Evaluation Targets ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [Table C.1](#A3.T1.2.28.2.1.1 "In Appendix C Rubric RL Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§D.1](#A4.SS1.p1.1 "D.1 GPQA-Diamond Evaluation ‣ Appendix D Generalization Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§D.2](#A4.SS2.p1.1 "D.2 Cross-Domain Probe Transfer ‣ Appendix D Generalization Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§1](#S1.p2.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§2.3](#S2.SS3.SSS0.Px2.p1.1 "Response roles. ‣ 2.3 PointRubric Construction ‣ 2 Rubric Judging Task and Dataset ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§4](#S4.p2.1 "4 Static Rubric-Judge Evaluation ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- OpenAI (2025a) OpenAI Deep research system card. Note: [https://openai.com/index/deep-research-system-card/](https://openai.com/index/deep-research-system-card/)Accessed: 2026-08-27 Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- OpenAI (2025b) OpenAI GPT-5 system card. Note: [https://openai.com/index/gpt-5-system-card/](https://openai.com/index/gpt-5-system-card/)Accessed: 2026-08-27 Cited by: [§A.6](#A1.SS6.p1.1 "A.6 Reference Judge and Construction Prompts ‣ Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§C.5](#A3.SS5.p3.1 "C.5 Human Audit and Reference-Judge Validation ‣ Appendix C Rubric RL Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- OpenAI (2025c) OpenAI Introducing GPT-4.1 in the API. Note: [https://openai.com/index/gpt-4-1/](https://openai.com/index/gpt-4-1/)Accessed: 2026-08-27 Cited by: [Table A.2](#A1.T2.2.4.4.1.1 "In A.4 PointRubric Response Roles ‣ Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Ouyang et al. (2022) L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray, J. Schulman, J. Hilton, F. Kelton, L. Miller, M. Simens, A. Askell, P. Welinder, P. F. Christiano, J. Leike, and R. Lowe Training language models to follow instructions with human feedback. In Advances in Neural Information Processing Systems, Vol. 35, pp. 27730–27744. External Links: [Document](https://dx.doi.org/10.52202/068431-2011), [Link](https://proceedings.neurips.cc/paper_files/paper/2022/hash/b1efde53be364a73914f58805a001731-Abstract.html) Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§1](#S1.p3.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§2.1](#S2.SS1.p1.1 "2.1 Our Task: Pointwise Rubric Judging ‣ 2 Rubric Judging Task and Dataset ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§3.2](#S3.SS2.p1.1 "3.2 Post-training with Supervised Fine-tuning ‣ 3 Rubric-Judge Methods ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Pan et al. (2026) T. Pan, X. Lin, W. Yang, Q. He, S. Chen, L. Qi, W. Xu, H. Feng, B. Xu, and Y. Xiao RubricEval: a rubric-level meta-evaluation benchmark for LLM judges in instruction following. arXiv preprint arXiv:2603.25133. External Links: [Document](https://dx.doi.org/10.48550/arXiv.2603.25133), [Link](https://arxiv.org/abs/2603.25133) Cited by: [§1](#S1.p3.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [Table 1](#S2.T1.2.1.10.1 "In 2 Rubric Judging Task and Dataset ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Rein et al. (2024) D. Rein, B. L. Hou, A. C. Stickland, J. Petty, R. Y. Pang, J. Dirani, J. Michael, and S. R. Bowman GPQA: a graduate-level google-proof Q&A benchmark. In First Conference on Language Modeling, External Links: [Link](https://openreview.net/forum?id=Ti67584b98) Cited by: [§D.1](#A4.SS1.p1.1 "D.1 GPQA-Diamond Evaluation ‣ Appendix D Generalization Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§1](#S1.p5.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§5.2](#S5.SS2.p3.1 "5.2 Transfer Results ‣ 5 Probe-Based Rubric Rewards for RL ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Shao et al. (2026) R. Shao, A. Asai, S. Z. Shen, H. Ivison, V. Kishore, J. Zhuo, X. Zhao, M. Park, S. G. Finlayson, D. Sontag, T. Murray, S. Min, P. Dasigi, L. Soldaini, F. Brahman, W. Yih, T. Wu, L. Zettlemoyer, Y. Kim, H. Hajishirzi, and P. W. Koh DR Tulu: reinforcement learning with evolving rubrics for deep research. In International Conference on Machine Learning, External Links: [Document](https://dx.doi.org/10.48550/arXiv.2511.19399), [Link](https://arxiv.org/abs/2511.19399) Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§1](#S1.p2.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§6](#S6.SS0.SSS0.Px1.p1.1 "Rubric-based RL. ‣ 6 Related Work ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Shao et al. (2024) Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang, Y. K. Li, Y. Wu, and D. Guo DeepSeekMath: pushing the limits of mathematical reasoning in open language models. arXiv preprint arXiv:2402.03300. External Links: [Document](https://dx.doi.org/10.48550/arXiv.2402.03300), [Link](https://arxiv.org/abs/2402.03300) Cited by: [Table C.1](#A3.T1.2.6.2.1.1 "In Appendix C Rubric RL Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§1](#S1.p1.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§1](#S1.p5.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§5.1](#S5.SS1.p2.1 "5.1 Matched RL Protocol and Results ‣ 5 Probe-Based Rubric Rewards for RL ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§6](#S6.SS0.SSS0.Px1.p1.1 "Rubric-based RL. ‣ 6 Related Work ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Sheng et al. (2025) G. Sheng, C. Zhang, Z. Ye, X. Wu, W. Zhang, R. Zhang, Y. Peng, H. Lin, and C. Wu HybridFlow: a flexible and efficient RLHF framework. In Proceedings of the Twentieth European Conference on Computer Systems, pp. 1279–1297. External Links: [Document](https://dx.doi.org/10.1145/3689031.3696075), [Link](https://doi.org/10.1145/3689031.3696075) Cited by: [Table C.1](#A3.T1.2.7.2.1.1 "In Appendix C Rubric RL Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Team OLMo et al. (2025) Team OLMo, P. Walsh, L. Soldaini, D. Groeneveld, K. Lo, S. Arora, A. Bhagia, Y. Gu, S. Huang, M. Jordan, N. Lambert, D. Schwenk, O. Tafjord, T. Anderson, D. Atkinson, F. Brahman, C. Clark, P. Dasigi, N. Dziri, M. Guerquin, H. Ivison, P. W. Koh, J. Liu, S. Malik, W. Merrill, L. J. V. Miranda, J. Morrison, T. Murray, C. Nam, V. Pyatkin, A. Rangapur, M. Schmitz, S. Skjonsberg, D. Wadden, C. Wilhelm, M. Wilson, L. Zettlemoyer, A. Farhadi, N. A. Smith, and H. Hajishirzi 2 OLMo 2 furious. In Conference on Language Modeling, External Links: [Link](https://openreview.net/forum?id=2ezugTT9kU) Cited by: [§A.7](#A1.SS7.SSS0.Px1.p1.1 "Extended held-out response bank. ‣ A.7 RaR-Science-Static Response Bank and Splits ‣ Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§4.2](#S4.SS2.SSS0.Px3.p1.1 "Probe is the strongest readout on RaR-Science-Static across all model sizes. ‣ 4.2 Static Judge Results ‣ 4 Static Rubric-Judge Evaluation ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Vu et al. (2024) T. Vu, K. Krishna, S. Alzubi, C. Tar, M. Faruqui, and Y. Sung Foundational autoraters: taming large language models for better automatic evaluation. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing, Y. Al-Onaizan, M. Bansal, and Y. Chen (Eds.), Miami, Florida, USA, pp. 17086–17105. External Links: [Link](https://aclanthology.org/2024.emnlp-main.949/), [Document](https://dx.doi.org/10.18653/v1/2024.emnlp-main.949) Cited by: [§6](#S6.SS0.SSS0.Px2.p1.1 "LLM-as-a-judge and small evaluators. ‣ 6 Related Work ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Wang et al. (2024) Y. Wang, Z. Yu, W. Yao, Z. Zeng, L. Yang, C. Wang, H. Chen, C. Jiang, R. Xie, J. Wang, X. Xie, W. Ye, S. Zhang, and Y. Zhang PandaLM: an automatic evaluation benchmark for LLM instruction tuning optimization. In International Conference on Learning Representations, Vol. 2024, pp. 43573–43593. External Links: [Link](https://proceedings.iclr.cc/paper_files/paper/2024/file/be3b0d51a2b86cb4ffe50f13480217e0-Paper-Conference.pdf) Cited by: [§6](#S6.SS0.SSS0.Px2.p1.1 "LLM-as-a-judge and small evaluators. ‣ 6 Related Work ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Wen et al. (2026) B. Wen, Y. Niu, C. Wang, X. Ling, Y. Zhang, P. Ke, H. Wang, and M. Huang IF-RewardBench: benchmarking judge models for instruction-following evaluation. In Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), San Diego, California, United States, pp. 23816–23843. External Links: [Document](https://dx.doi.org/10.18653/v1/2026.acl-long.1092), [Link](https://aclanthology.org/2026.acl-long.1092/) Cited by: [§1](#S1.p3.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [Table 1](#S2.T1.2.1.4.1 "In 2 Rubric Judging Task and Dataset ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§6](#S6.SS0.SSS0.Px2.p1.1 "LLM-as-a-judge and small evaluators. ‣ 6 Related Work ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Wen et al. (2025) X. Wen, Z. Liu, S. Zheng, S. Ye, Z. Wu, Y. Wang, Z. Xu, X. Liang, J. Li, Z. Miao, J. Bian, and M. Yang Reinforcement learning with verifiable rewards implicitly incentivizes correct reasoning in base LLMs. arXiv preprint arXiv:2506.14245. External Links: [Document](https://dx.doi.org/10.48550/arXiv.2506.14245), [Link](https://arxiv.org/abs/2506.14245) Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§6](#S6.SS0.SSS0.Px1.p1.1 "Rubric-based RL. ‣ 6 Related Work ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Yang et al. (2025) A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Gao, C. Huang, C. Lv, C. Zheng, D. Liu, F. Zhou, F. Huang, F. Hu, H. Ge, H. Wei, H. Lin, J. Tang, J. Yang, J. Tu, J. Zhang, J. Yang, J. Yang, J. Zhou, J. Zhou, J. Lin, K. Dang, K. Bao, K. Yang, L. Yu, L. Deng, M. Li, M. Xue, M. Li, P. Zhang, P. Wang, Q. Zhu, R. Men, R. Gao, S. Liu, S. Luo, T. Li, T. Tang, W. Yin, X. Ren, X. Wang, X. Zhang, X. Ren, Y. Fan, Y. Su, Y. Zhang, Y. Zhang, Y. Wan, Y. Liu, Z. Wang, Z. Cui, Z. Zhang, Z. Zhou, and Z. Qiu Qwen3 technical report. arXiv preprint arXiv:2505.09388. External Links: [Document](https://dx.doi.org/10.48550/arXiv.2505.09388), [Link](https://arxiv.org/abs/2505.09388) Cited by: [§A.7](#A1.SS7.p1.1 "A.7 RaR-Science-Static Response Bank and Splits ‣ Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [Table B.2](#A2.T2.2.2.2.1.1 "In B.3 Supervised Fine-tuning Details ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [Table C.1](#A3.T1.2.2.2.1.1 "In Appendix C Rubric RL Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§D.2](#A4.SS2.p1.1 "D.2 Cross-Domain Probe Transfer ‣ Appendix D Generalization Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§1](#S1.p4.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§2.4](#S2.SS4.SSS0.Px1.p1.1 "Response bank and split. ‣ 2.4 RaR-Science-Static ‣ 2 Rubric Judging Task and Dataset ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§4.1](#S4.SS1.p1.1 "4.1 Experiment Setup ‣ 4 Static Rubric-Judge Evaluation ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Ye et al. (2024) S. Ye, D. Kim, S. Kim, H. Hwang, S. Kim, Y. Jo, J. Thorne, J. Kim, and M. Seo FLASK: fine-grained language model evaluation based on alignment skill sets. In International Conference on Learning Representations, Vol. 2024, pp. 55361–55414. External Links: [Link](https://proceedings.iclr.cc/paper_files/paper/2024/file/f41b4a6b202adcd8e150a9d4f124d8f6-Paper-Conference.pdf) Cited by: [§1](#S1.p3.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [Table 1](#S2.T1.2.1.2.1 "In 2 Rubric Judging Task and Dataset ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Zhao et al. (2025) Y. Zhao, K. Zhang, T. Hu, S. Wu, R. L. Bras, Y. Liu, R. Tang, J. C. Chang, J. Dodge, J. Bragg, C. Zhao, H. Hajishirzi, D. Downey, and A. Cohan SciArena: an open evaluation platform for non-verifiable scientific literature-grounded tasks. In Advances in Neural Information Processing Systems 38: Annual Conference on Neural Information Processing Systems 2025, NeurIPS 2025, San Diego, CA, USA, December 2-7, 2025 / Mexico City, Mexico, November 30 - December 5, 2025, D. Belgrave, C. Zhang, L. N. Montoya, H. Lin, R. Pascanu, P. Koniusz, M. Ghassemi, N. Chen, I. V. M. Ruíz, and A. Loaiza-Bonilla (Eds.), External Links: [Link](http://papers.nips.cc/paper\_files/paper/2025/hash/9811fe727c94e7ff79f701c94ed1d938-Abstract-Datasets\_and\_Benchmarks\_Track.html) Cited by: [§6](#S6.SS0.SSS0.Px2.p1.1 "LLM-as-a-judge and small evaluators. ‣ 6 Related Work ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Zheng et al. (2023) L. Zheng, W. Chiang, Y. Sheng, S. Zhuang, Z. Wu, Y. Zhuang, Z. Lin, Z. Li, D. Li, E. P. Xing, H. Zhang, J. E. Gonzalez, and I. Stoica Judging LLM-as-a-judge with MT-bench and chatbot arena. In Advances in Neural Information Processing Systems, Vol. 36, pp. 46595–46623. External Links: [Document](https://dx.doi.org/10.52202/075280-2020), [Link](https://proceedings.neurips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html) Cited by: [§1](#S1.p2.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§2.1](#S2.SS1.p1.1 "2.1 Our Task: Pointwise Rubric Judging ‣ 2 Rubric Judging Task and Dataset ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§6](#S6.SS0.SSS0.Px2.p1.1 "LLM-as-a-judge and small evaluators. ‣ 6 Related Work ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Zhou et al. (2026) J. Zhou, Q. Zhang, Y. Wang, F. Lyu, Y. Ming, C. Xu, Q. Sun, K. Zheng, P. Kang, X. Liu, and C. Ma RubricBench: aligning model-generated rubrics with human standards. In Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), San Diego, California, United States, pp. 31179–31200. External Links: [Document](https://dx.doi.org/10.18653/v1/2026.acl-long.1439), [Link](https://aclanthology.org/2026.acl-long.1439/) Cited by: [§1](#S1.p3.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [Table 1](#S2.T1.2.1.9.1 "In 2 Rubric Judging Task and Dataset ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").
- Zhu et al. (2025) L. Zhu, X. Wang, and X. Wang JudgeLM: fine-tuned large language models are scalable judges. In International Conference on Learning Representations, Vol. 2025, pp. 51257–51296. External Links: [Link](https://proceedings.iclr.cc/paper_files/paper/2025/file/7f8f73134e253845a8f82983219a8452-Paper-Conference.pdf) Cited by: [§1](#S1.p3.1 "1 Introduction ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [Table 1](#S2.T1.2.1.5.1 "In 2 Rubric Judging Task and Dataset ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), [§6](#S6.SS0.SSS0.Px2.p1.1 "LLM-as-a-judge and small evaluators. ‣ 6 Related Work ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").

## Appendix A PointRubric Construction and Rubric Scoring

### A.1 Pointwise and Pairwise Rubric Scoring

Let $q$ denote a prompt, $y$ a candidate response, and ${C{(q)}} = {\{ c_{j}\}}_{j = 1}^{m_{q}}$ the rubric for $q$. Each criterion $c_{j}$ is associated with a nonnegative weight $w_{j}$, with ${\sum_{j}w_{j}} > 0$ for every rubric. In settings with hard and soft criteria, $w_{j}$ is obtained by mapping the criterion type to a fixed weight; in settings with absolute rubric weights, $w_{j}$ is given directly by the rubric. A pointwise rubric label is a criterion-satisfaction judgment

|     |                                                  |     |
|-----|--------------------------------------------------|-----|
|     | $${{z_{j}\hspace{0pt}{(q,y)}} \in {\{ 0,1\}}},$$ |     |

where ${z_{j}\hspace{0pt}{(q,y)}} = 1$ means that response $y$ satisfies criterion $c_{j}$ for prompt $q$. A probabilistic judge instead returns ${p_{j}\hspace{0pt}{(q,y)}} \in {\lbrack{0,1}\rbrack}$, interpreted as the probability that $c_{j}$ is satisfied.

The normalized rubric score for a response is

|     |                                                                                                                       |     |
|-----|-----------------------------------------------------------------------------------------------------------------------|-----|
|     | $${{R{(q,y)}} = \frac{\sum_{j = 1}^{m_{q}}{w_{j}\hspace{0pt}z_{j}\hspace{0pt}{(q,y)}}}{\sum_{j = 1}^{m_{q}}w_{j}}},$$ |     |

or, for probabilistic judges,

|     |                                                                                                                                         |     |
|-----|-----------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${{\hat{R}\hspace{0pt}{(q,y)}} = \frac{\sum_{j = 1}^{m_{q}}{w_{j}\hspace{0pt}p_{j}\hspace{0pt}{(q,y)}}}{\sum_{j = 1}^{m_{q}}w_{j}}}.$$ |     |

This aggregation preserves the rubric structure while producing the scalar reward required for reinforcement learning.

A pairwise preference between two responses $y_{a}$ and $y_{b}$ to the same prompt can be induced from pointwise rubric scores:

|     |                                                                          |     |
|-----|--------------------------------------------------------------------------|-----|
|     | $$y_{a} \succ_{q}y_{b}\Longleftrightarrow R{(q,y_{a})} > R{(q,y_{b})},$$ |     |

with ties defined when the two normalized scores are equal. Pairwise labels are therefore recoverable from pointwise rubric labels when the same rubric is applied to both responses. The reverse is not true: a pairwise preference does not identify which criteria were satisfied or violated. Pointwise labels are therefore richer for rubric-based RL because they preserve the criterion-level reward structure used to compute rewards, analyze criterion-level errors, and train reward readouts without collapsing the rubric to a single preference label.

For example, suppose a rubric contains one criterion requiring the final answer and another requiring supporting reasoning. A response may satisfy the final answer criterion while failing the reasoning criterion. Pointwise labels retain this distinction, whereas a pairwise label only states whether that response is preferred to another response under the aggregate score.

### A.2 PointRubric Construction Details

Table [A.1](#A1.T1 "Table A.1 ‣ A.2 PointRubric Construction Details ‣ Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") summarizes the construction procedure. We sample question records from OpenRubrics ([Liu et al., 2026](#bib.bib21)) whose original rubrics contain explicit hard requirements, then refine each rubric into a fixed six-criterion format with two hard criteria and four soft criteria. We use GPT-4o for rubric refinement and reference grading. The final benchmark is obtained by retaining questions whose generated response set spans full-score, low-score, and intermediate rubric outcomes.

| Stage                | Count |  Criterion                                       |
|----------------------|-------|--------------------------------------------------|
| Candidates           | 3,000 |  Two sampled construction passes                 |
| Unique questions     | 2,902 |  Before filtering                                |
| Full-score answer    | 2,432 |  Answer 1 score $\phantom{} = 10$                |
| Low-score answer     | 1,566 |  Also answer 2 score $\phantom{} \leq 3$         |
| Intermediate answer  | 1,061 |  Also some answer score in $\lbrack 2,8\rbrack$  |
| Unique after filters | 1,045 |  Deduplicated by question ID                     |
| Frozen PointRubric   | 1,042 |  Canonical benchmark used in all experiments     |

Table A.1: PointRubric construction stages. Counts are computed over completed construction artifacts. The final row gives the frozen benchmark artifact used for all experiments.

### A.3 Rubric-Transformation Audit

We manually audited 50 transformations sampled uniformly from the construction data with seed 42. For each example, we compared the original question and OpenRubrics Hard Rules and Principles with the standardized two-hard/four-soft rubric, without reference to generated responses or criterion labels. The audit assessed whether the transformation preserved the core rubric intent, avoided unsupported requirements, and produced a reasonable hard/soft decomposition. Because the transformation compresses rubrics into a fixed structure, preservation was evaluated at the level of substantive intent rather than one-to-one retention of every original Principle.

Of the 50 transformations, 47 preserved the core rubric intent, all 50 avoided unsupported additions, and 49 produced a reasonable hard/soft decomposition. The three intent-preservation failures involved requirements omitted during compression rather than newly introduced requirements.

#### Representative transformations.

In a faithful Python/Celery example, the original hard rules require activating a Python 3.8 environment and providing the exact Celery 5.2.7 installation command with Redis support. The standardized rubric retains both requirements as hard criteria and consolidates the original compatibility, troubleshooting, and verification Principles into four soft criteria without changing the core grading intent.

In an imperfect browser-game example, the original rubric explicitly requires the core interactive mechanics of a Rocket League–style implementation. The standardized rubric retains the browser implementation, dependency, structure, usability, and code-correctness requirements, but does not retain an explicit criterion for those mechanics. We therefore mark this transformation as not preserving the complete rubric intent. These examples illustrate both the intended compression and its principal failure mode.

### A.4 PointRubric Response Roles

Table [A.2](#A1.T2 "Table A.2 ‣ A.4 PointRubric Response Roles ‣ Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") describes the four responses associated with each question. The responses should not be interpreted as four ordinal quality levels. Instead, PointRubric fixes one full-score response and one low-score response, then includes two additional comparison responses whose observed scores vary.

| ID  | Role                        | Rubric visible |  Generator in final artifact                                     |  Retention status                                                                |
|-----|-----------------------------|----------------|------------------------------------------------------------------|----------------------------------------------------------------------------------|
| 1   | Full-score response         | Yes            |  GPT-4o (1,042)                                                  |  Required to receive total score 10.                                             |
| 2   | Low-score response          | Yes            |  GPT-4o (1,042)                                                  |  Required to receive total score at most 3.                                      |
| 3   | Partial-compliance response | Yes            |  GPT-4o (764), GPT-4.1-nano ([OpenAI, 2025c](#bib.bib35)) (278)  |  Additional comparison response; broad observed score range.                     |
| 4   | Unguided response           | No             |  GPT-4.1-nano (1,042)                                            |  Additional comparison response; natural score variation without rubric access.  |

Table A.2: Response roles in PointRubric. Counts reflect the final benchmark artifact.

| ID  | Mean  | 0–3   | 4–6 | 7–9 | 10    |
|-----|-------|-------|-----|-----|-------|
| 1   | 10.00 | 0     | 0   | 0   | 1,042 |
| 2   | 0.89  | 1,042 | 0   | 0   | 0     |
| 3   | 6.39  | 89    | 461 | 367 | 125   |
| 4   | 8.47  | 44    | 117 | 395 | 486   |

Table A.3: Observed GPT-4o rubric-score distribution by response ID in the final PointRubric benchmark. Scores range from 0 to 10 under hard-rule weight 3 and soft-rule weight 1.

### A.5 PointRubric Evaluation Protocol and Metrics

For judge methods that require training or calibration, we use a fixed question-level split so that responses to the same question never appear in both calibration and held-out evaluation. Frozen or zero-shot judges can be evaluated on the full benchmark.

| Split       | Questions | Responses | Criterion labels |
|-------------|-----------|-----------|------------------|
| Train       | 417       | 1,668     | 10,008           |
| Development | 104       | 416       | 2,496            |
| Held-out    | 521       | 2,084     | 12,504           |
| Total       | 1,042     | 4,168     | 25,008           |

Table A.4: Question-level PointRubric split used for calibrated or trained judge methods, after validating all criterion labels.

The primary PointRubric metric is weighted criterion accuracy, using weight 3 for hard criteria and weight 1 for soft criteria. Complementary static metrics include parse success, unweighted criterion accuracy, macro-F1, balanced accuracy, MCC, scalar-score error, score correlation, and induced pairwise ordering accuracy.

### A.6 Reference Judge and Construction Prompts

We use GPT-4o ([OpenAI, 2024](#bib.bib34)) as the construction and reference judge for PointRubric. During benchmark construction, GPT-5 ([OpenAI, 2025b](#bib.bib36)) frequently refused or failed to produce responses with the designated quality level, especially deliberately low-scoring or partially compliant answers. Since PointRubric requires controlled variation across responses to the same prompt, we used GPT-4o for rubric refinement, designated-quality response generation, and criterion-level grading. For consistency, all subsequent PointRubric judge comparisons use the same GPT-4o reference labels. The rubric-refinement, answer-generation, and grading prompts are provided for reproducibility in Appendix [E](#A5 "Appendix E Prompts for Reproducibility ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").

### A.7 RaR-Science-Static Response Bank and Splits

RaR-Science-Static is the fixed response bank used for static judge evaluation under the RaR-Science rubric format. It contains 1,500 science questions sampled from RaR-Science ([Gunjal et al., 2026](#bib.bib20)). Each question is paired with two candidate responses: the original dataset reference answer and a greedy Qwen3-4B response ([Yang et al., 2025](#bib.bib31)). The resulting bank contains 3,000 candidate responses. The rubrics are instance-specific; in RaR-Science-Static, they contain between 6 and 11 criteria, with an average of 7.52 criteria per question.

For trained or calibrated static methods, we use a fixed question-level split: 1,000 training questions, 200 development questions, and 300 held-out questions. The held-out split contains 600 candidate responses. Splitting is performed by question, so no responses to the same question appear in both calibration and evaluation. Generative and Logprob judges do not require fitting, but they are evaluated on the same held-out questions for comparability.

#### Extended held-out response bank.

To test response-generator shift, we extend the 300-question held-out bank with greedy responses from Mistral-7B-Instruct-v0.3 and OLMo-2-1124-7B-Instruct ([Jiang et al., 2023](#bib.bib32); [Team OLMo et al., 2025](#bib.bib33)). Together with the original reference answer and greedy Qwen3-4B response, this gives four responses per question and 1,200 response-level examples. All added responses are labeled by GPT-4o using the same criterion-level protocol. The training and development data, Probe parameters, layer, and threshold remain unchanged.

| Judge      | Macro-F1 | Agreement | Pearson | MAE   | Parse rate |
|------------|----------|-----------|---------|-------|------------|
| Generative | 0.394    | 0.523     | 0.130   | 0.471 | 0.950      |
| Logprob    | 0.424    | 0.538     | 0.404   | 0.405 | 1.000      |
| Probe      | 0.741    | 0.746     | 0.683   | 0.224 | 1.000      |

Table A.5: Qwen3-1.7B judge results on the extended RaR-Science-Static held-out bank. Agreement is criterion-level agreement; Pearson and MAE are computed over weighted scalar rubric scores.

The extended bank is more difficult than the original two-response bank, but the readout ranking remains unchanged. The unchanged Probe retains stronger criterion agreement, scalar-score correlation, and score accuracy on responses from the additional model families.

### A.8 RaR-Science-Static Reference Labels and Aggregation

We use GPT-4o ([OpenAI, 2024](#bib.bib34)) as the operational reference judge for RaR-Science-Static. The reference judge assigns one Yes/No verdict per rubric criterion for each candidate response. The final reference-scoring run parses successfully for all 3,000 candidate responses.

For scalar-score metrics, RaR-Science-Static uses the original RaR-Science rubric weights after converting all criteria into a satisfaction-label interface. Some RaR-Science criteria are pitfall criteria with negative raw weights. We interpret these as avoidance criteria: satisfying the criterion means that the response avoids the pitfall. We therefore aggregate with absolute weights so that higher criterion satisfaction always corresponds to better rubric compliance:

|     |                                                                                                                                                 |     |
|-----|-------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${{\hat{R}\hspace{0pt}{(q,y)}} = \frac{\sum_{j = 1}^{m_{q}}{{|w_{j}|}\hspace{0pt}p_{j}\hspace{0pt}{(q,y)}}}{\sum_{j = 1}^{m_{q}}{|w_{j}|}}}.$$ |     |

For binary methods, $p_{j}\hspace{0pt}{(q,y)}$ is replaced by ${\hat{z}}_{j}\hspace{0pt}{(q,y)}$. The same aggregation rule is used for Generative, Logprob, and Probe judges on RaR-Science-Static.

### A.9 Reference-Label Validation

We validate the GPT-4o reference labels with a blinded human audit on the held-out PointRubric split used in our static evaluator experiments. The audit samples 50 question-level groups, and for each group selects two candidate responses from the four available responses such that the two candidates have different GPT-4o rubric scores. The resulting 100 responses are shuffled before annotation. For each response, the annotator labels every rubric criterion as satisfied or not satisfied without seeing the GPT-4o labels or scores.

The audit covers 600 response–criterion decisions. We compute criterion-level agreement between the human annotator and GPT-4o labels, and additionally report a weighted agreement that uses the rubric criterion weights when aggregating decisions. Human labels agree with GPT-4o on 90.9% of weighted criterion decisions. Agreement is highest for hard factual or constraint-following criteria, and lower for softer criteria involving completeness, clarity, specificity, and overall explanation quality. Table [A.6](#A1.T6 "Table A.6 ‣ A.9 Reference-Label Validation ‣ Appendix A PointRubric Construction and Rubric Scoring ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") summarizes the audit size and agreement results.

We also evaluate whether the human audit preserves the response ordering induced by the rubric score. For each of the 50 sampled response pairs, we aggregate the human criterion labels with the same rubric weights and compare the preferred response with the GPT-4o-preferred response. Human and GPT-4o preferences agree on 96.0% of pairs, further supporting the reliability of the operational reference target.

| Audit statistic                           | Value |
|-------------------------------------------|-------|
| Sampled responses                         | 100   |
| Sampled response pairs                    | 50    |
| Response–criterion decisions              | 600   |
| Weighted criterion agreement with GPT-4o  | 90.9% |
| Pairwise preference agreement with GPT-4o | 96.0% |

Table A.6: Human audit of GPT-4o reference labels on the held-out PointRubric split.

## Appendix B Static Evaluation Details

### B.1 Generative and Logprob Judge Details

#### Generative judging.

The Generative judge receives one criterion at a time and produces a single Yes/No verdict. Verdicts are then recombined into a full criterion vector for the candidate response. This reduces the output-format burden for each completion but requires one generation per criterion.

#### Forced-choice Logprob scoring.

The Logprob judge receives the question, candidate response, and one canonicalized criterion. The prompt asks whether the response satisfies the criterion and ends before the answer token. We score the next-token probabilities of the fixed verbalizers “ Yes” and “ No” and compute their log-probability margin:

|     |                                                                                                        |     |
|-----|--------------------------------------------------------------------------------------------------------|-----|
|     | $${\Delta_{j} = {{\log{P{(\text{~Yes}\mid{q,y,c_{j}})}}} - {\log{P{(\text{~No}\mid{q,y,c_{j}})}}}}}.$$ |     |

We set the soft satisfaction score to ${p_{j}\hspace{0pt}{(q,y)}} = {\sigma{(\Delta_{j})}}$. Binary metrics threshold the margin at 0, equivalently ${p_{j}\hspace{0pt}{(q,y)}} \geq 0.5$. Scalar rubric aggregation uses the soft satisfaction score.

### B.2 Probe Training and Calibration

#### Canonical criterion rendering.

Probe prompts use a single criterion at a time. Ordinary criteria are rendered as satisfaction criteria. Pitfall criteria are rendered as avoidance criteria, so a positive label always means that the response complies with the rubric.

#### Representation extraction.

For each rendered prompt, we run the frozen judge model with hidden states enabled and extract the representation at the final non-padding token. For layer $\ell$, this gives $h_{\ell}\hspace{0pt}{(q,y,c_{j})}$. We evaluate last-token, mean-pooled, and last-few-token pooled representations in the ablation table.

#### Feature standardization.

For each layer, training features are used to compute a mean vector and standard deviation vector. Training, development, and held-out features are standardized with these training-set statistics. Held-out features are never used to choose normalization statistics, layers, thresholds, or classifier checkpoints.

#### Probe heads.

We train linear and MLP binary classifiers with binary cross-entropy. The classifier predicts the GPT-4o criterion label from the frozen representation. For MLP probes, only the small probe head is trained; the language model remains frozen.

#### Layer and threshold selection.

For each candidate layer, we train the probe on the training split and evaluate on the development split. The threshold is selected on development data to maximize macro-F1, and the layer is selected by the same development metric. The held-out split is evaluated only after these choices are fixed.

| Training detail |  Setting                                                                           |
|-----------------|------------------------------------------------------------------------------------|
| Backbone        |  Frozen language model                                                             |
| Representation  |  Final non-padding-token hidden state                                              |
| Head            |  Linear; MLP only in ablations                                                     |
| Optimization    |  Full-batch AdamW, 200 epochs; learning rate 0.01; weight decay 0.01               |
| Objective       |  Binary cross-entropy with positive-class weighting                                |
| Selection       |  Head checkpoint by development loss; layer and threshold by development macro-F1  |
| Seed            |  Split seed 42; head seed 42 plus layer index                                      |

Table B.1: Probe fitting and selection settings.

#### Supervision cost and reuse.

Static evaluation and RL use separate supervision banks. The main RaR-Science-Static Probe uses 2,400 responses (18,032 criterion labels; approximately \$11.62), whereas the RL reward Probe uses 450 training and 50 development responses (3,766 labels; approximately \$2.43). Once fitted, either frozen Probe can be reused in the same rubric setting without further teacher calls or recalibration. The complete GPT-4o reference-labeling run used 4.11 million tokens and cost \$14.53 at the API pricing used during construction.

The data-size ablation indicates that smaller supervision sets remain viable: 500 training questions achieve 0.828 macro-F1, compared with 0.834 for 1,000 questions, while 100 questions achieve 0.805. The science-to-medicine transfer result suggests useful agreement under a moderate rubric shift without refitting, but substantial changes in domain or rubric format may require new supervision. Across the studied training sizes, the corresponding reference-labeling cost ranges from approximately \$2.91 to \$11.62. These estimates use the API pricing at the time of dataset construction.

#### Probability rewards.

At evaluation time, the probe outputs a criterion probability. Scalar scores use these probabilities rather than only thresholded verdicts unless otherwise specified. In the RL experiments, these probabilities provide the reward signal while preserving the same explicit rubric aggregation used by generative judges.

### B.3 Supervised Fine-tuning Details

SFT uses the same train, development, and held-out question splits as the corresponding static evaluation setting. The model is fine-tuned only on the training split, with development loss used for checkpoint selection. Held-out questions are used only for final reporting. After SFT, the resulting backbone is evaluated with the same Generative, Logprob, and Probe methods used for the base backbone.

|  Metric                                  |  Value                                                                         |
|------------------------------------------|--------------------------------------------------------------------------------|
|  Backbones                               |  Qwen3-0.6B, Qwen3-1.7B, Qwen3-4B, Qwen3-8B ([Yang et al., 2025](#bib.bib31))  |
|  Training objective                      |  Supervised verdict prediction                                                 |
|  Fine-tuning method                      |  LoRA ([Hu et al., 2022](#bib.bib43))                                          |
|  LoRA target modules                     |  All target modules                                                            |
|  Chat template                           |  Qwen                                                                          |
|  Precision                               |  bf16                                                                          |
|  Optimizer                               |  AdamW ([Loshchilov and Hutter, 2019](#bib.bib39))                             |
|  Scheduler                               |  Cosine decay                                                                  |
|  Warmup ratio                            |  0.03                                                                          |
|  Epochs                                  |  3                                                                             |
|  Checkpoint selection                    |  Lowest development loss                                                       |
|  Checkpoint limit                        |  3                                                                             |
|  PointRubric training examples           |  Question-level training split                                                 |
|  PointRubric maximum length              |  4096 tokens                                                                   |
|  PointRubric learning rate               |  $2 \times 10^{- 4}$                                                           |
|  PointRubric eval/save frequency         |  200 steps                                                                     |
|  PointRubric batch/accumulation          |  0.6B: batch 2, accumulation 16; larger models: batch 1, accumulation 32       |
|  RaR-Science-Static training examples    |  Question-level training split                                                 |
|  RaR-Science-Static maximum length       |  8192 tokens                                                                   |
|  RaR-Science-Static learning rate        |  $1 \times 10^{- 4}$                                                           |
|  RaR-Science-Static eval/save frequency  |  50 steps                                                                      |
|  RaR-Science-Static batch/accumulation   |  0.6B: batch 2, accumulation 16; larger models: batch 1, accumulation 16       |

Table B.2: SFT configuration for the post-training judge experiments.

In both data settings, SFT trains the model to output the complete rubric verdict vector for a candidate response. Each example contains the question, candidate response, all rubric criteria, and the corresponding GPT-4o Yes/No verdicts. RaR-Science-Static examples use responses and verdicts from the fixed response bank. For SFT Probe, the Probe is trained on hidden states extracted from the SFT backbone using the same Probe-training protocol as for the base backbone.

### B.4 Static Evaluation Targets

For both PointRubric and RaR-Science, the static target is criterion satisfaction. Each example is a tuple $(q,y,c_{j})$, where $q$ is the question, $y$ is a candidate response, and $c_{j}$ is one rubric criterion. The operational reference label is

|     |                                                         |     |
|-----|---------------------------------------------------------|-----|
|     | $${{z_{j}^{\ast}\hspace{0pt}{(q,y)}} \in {\{ 0,1\}}},$$ |     |

where ${z_{j}^{\ast}\hspace{0pt}{(q,y)}} = 1$ means that GPT-4o ([OpenAI, 2024](#bib.bib34)) judges response $y$ to satisfy criterion $c_{j}$ for question $q$.

A judge method may return either a binary verdict ${{\hat{z}}_{j}\hspace{0pt}{(q,y)}} \in {\{ 0,1\}}$ or a probability ${p_{j}\hspace{0pt}{(q,y)}} \in {\lbrack{0,1}\rbrack}$. Binary metrics are computed from ${\hat{z}}_{j}\hspace{0pt}{(q,y)}$, using a thresholded probability when the method is probabilistic. Scalar rubric scores are computed by aggregating criterion predictions with the rubric weights, so the scalar score is derived from criterion-level judgments rather than predicted directly.

### B.5 Rubric-RM Pairwise Comparison

Rubric-RM directly predicts the preferred response from a pair conditioned on the rubric ([Liu et al., 2026](#bib.bib21)). By contrast, our pointwise judges score each response independently, after which their scalar scores induce a pairwise ordering. We compare the methods on all pairs for which the GPT-4o reference scores are non-tied. Because Rubric-RM sometimes fails to produce a parseable preference under this adaptation, we report its parse rate, accuracy over the complete evaluation set with parse failures counted as incorrect, and accuracy restricted to parseable outputs.

| Dataset            | Method           | Parse | Full set | Parseable |
|--------------------|------------------|-------|----------|-----------|
| PointRubric        | Rubric-RM-4B     | 0.627 | 0.322    | 0.513     |
| PointRubric        | Rubric-RM-8B     | 0.396 | 0.228    | 0.575     |
| PointRubric        | Qwen3-1.7B Probe | 1.000 | 0.924    | 0.924     |
| RaR-Science-Static | Rubric-RM-4B     | 0.727 | 0.487    | 0.670     |
| RaR-Science-Static | Rubric-RM-8B     | 0.401 | 0.210    | 0.523     |
| RaR-Science-Static | Qwen3-1.7B Probe | 1.000 | 0.888    | 0.888     |

Table B.3: Static pairwise comparison on GPT-4o non-tied pairs. Full-set accuracy counts parse failures as incorrect; parseable accuracy excludes them.

For PointRubric, the Probe produces 287 exact score ties; its reported accuracy assigns half credit to these ties. The RaR-Science-Static Probe produces no ties. Rubric-RM’s parseable-only results show that it captures useful pairwise signal when its output conforms to the requested format, but parse failures substantially reduce full-set accuracy.

This comparison is not a direct online-RL efficiency comparison. With a rollout group of size $k$, a pairwise reward model requires up to ${k{({k - 1})}}/2$ comparisons, whereas the pointwise interface requires $k$ response scores and additionally exposes criterion-level satisfaction. At our group size of four, this corresponds to six pairwise comparisons rather than four pointwise response evaluations.

### B.6 Static Readout Error Analysis

We compare the Qwen3-1.7B Generative and Probe predictions on the same 4,518 RaR-Science-Static held-out criterion decisions. The paired decomposition separates errors recovered by the Probe, errors introduced by the Probe, and criteria that remain difficult for both readouts.

|  Analysis  | Outcome                         | Share |
|------------|---------------------------------|-------|
|  Paired    | Generative wrong, Probe correct | 33.0% |
|  Paired    | Generative correct, Probe wrong | 7.8%  |
|  Paired    | Both wrong                      | 7.9%  |
|  Paired    | Both correct                    | 51.3% |
|  Error     | Generative false positive       | 33.7% |
|  Error     | Generative false negative       | 4.2%  |
|  Error     | Probe false positive            | 6.7%  |
|  Error     | Probe false negative            | 9.0%  |

Table B.4: Paired Qwen3-1.7B readout errors on the RaR-Science-Static held-out split. Shares are computed over 4,518 criterion decisions.

The Generative readout’s errors are dominated by false positives, indicating a tendency to accept criteria that the GPT-4o reference marks as unsatisfied. The Probe removes many of these false positives, although its remaining errors are more balanced between false positives and false negatives. The 7.8% reverse outcome also shows that the Probe does not uniformly dominate generation at the individual-decision level.

#### Representative Generative false positive.

For the question asking for the principal energy-liberating process in stars, the candidate answers only, “Conversion of hydrogen into helium via nuclear fusion.” One criterion additionally requires explaining that fusion releases energy by converting mass into energy. GPT-4o and Probe mark this criterion unsatisfied, while Generative marks it satisfied. This example illustrates the Generative readout’s tendency to accept criteria whose central topic is mentioned but whose specific requirement is omitted.

#### Representative Probe false negative.

For the bound-state problem with ${V{(x)}} = {- {a\hspace{0pt}\delta\hspace{0pt}{(x)}}}$, the candidate explicitly gives a wavefunction that decays exponentially on both sides of $x = 0$. GPT-4o and Generative therefore mark the wavefunction-form criterion satisfied, while Probe marks it unsatisfied. This case shows that Probe can miss requirements that are directly supported by the response.

### B.7 Static Metrics

| Layer | Dev Macro-F1 | Held-out Acc. | Held-out Macro-F1 | Held-out Bal. Acc. | Held-out MCC |
|-------|--------------|---------------|-------------------|--------------------|--------------|
| 1     | 0.726        | 0.759         | 0.738             | 0.733              | 0.480        |
| 2     | 0.742        | 0.774         | 0.750             | 0.743              | 0.508        |
| 3     | 0.751        | 0.781         | 0.754             | 0.745              | 0.523        |
| 4     | 0.752        | 0.787         | 0.769             | 0.764              | 0.540        |
| 5     | 0.755        | 0.778         | 0.751             | 0.742              | 0.517        |
| 6     | 0.752        | 0.791         | 0.771             | 0.763              | 0.548        |
| 7     | 0.758        | 0.791         | 0.779             | 0.780              | 0.558        |
| 8     | 0.768        | 0.794         | 0.774             | 0.766              | 0.554        |
| 9     | 0.765        | 0.787         | 0.774             | 0.775              | 0.548        |
| 10    | 0.778        | 0.804         | 0.790             | 0.788              | 0.581        |
| 11    | 0.784        | 0.810         | 0.800             | 0.802              | 0.600        |
| 12    | 0.790        | 0.819         | 0.805             | 0.800              | 0.611        |
| 13    | 0.805        | 0.827         | 0.812             | 0.805              | 0.627        |
| 14    | 0.799        | 0.830         | 0.818             | 0.814              | 0.636        |
| 15    | 0.814        | 0.831         | 0.814             | 0.806              | 0.635        |
| 16    | 0.836        | 0.845         | 0.833             | 0.829              | 0.667        |
| 17    | 0.836        | 0.849         | 0.839             | 0.837              | 0.678        |
| 18    | 0.832        | 0.853         | 0.841             | 0.835              | 0.684        |
| 19    | 0.827        | 0.847         | 0.835             | 0.829              | 0.672        |
| 20    | 0.824        | 0.843         | 0.835             | 0.838              | 0.670        |
| 21    | 0.828        | 0.845         | 0.835             | 0.836              | 0.671        |
| 22    | 0.827        | 0.843         | 0.834             | 0.833              | 0.667        |
| 23    | 0.823        | 0.848         | 0.837             | 0.835              | 0.675        |
| 24    | 0.821        | 0.847         | 0.837             | 0.837              | 0.675        |
| 25    | 0.819        | 0.843         | 0.834             | 0.835              | 0.668        |
| 26    | 0.818        | 0.844         | 0.835             | 0.835              | 0.670        |
| 27    | 0.816        | 0.839         | 0.828             | 0.825              | 0.656        |
| 28    | 0.817        | 0.843         | 0.833             | 0.832              | 0.665        |

Table B.5: Qwen3-1.7B Probe layer sweep on RaR-Science-Static. Layer selection is based on development macro-F1; the selected layer is bolded.

|            | Base model             |                        |                        | SFT model              |                        |                        |
|------------|------------------------|------------------------|------------------------|------------------------|------------------------|------------------------|
| Model      | Generative             | Logprob                | Probe                  | Generative             | Logprob                | Probe                  |
| Qwen3-0.6B | 0.370 \[0.349, 0.390\] | 0.582 \[0.568, 0.596\] | 0.802 \[0.791, 0.811\] | 0.560 \[0.537, 0.584\] | 0.604 \[0.591, 0.618\] | 0.820 \[0.810, 0.830\] |
| Qwen3-1.7B | 0.518 \[0.493, 0.541\] | 0.766 \[0.757, 0.776\] | 0.875 \[0.867, 0.883\] | 0.902 \[0.894, 0.909\] | 0.713 \[0.705, 0.722\] | 0.845 \[0.836, 0.854\] |
| Qwen3-4B   | 0.790 \[0.768, 0.811\] | 0.893 \[0.886, 0.899\] | 0.913 \[0.906, 0.919\] | 0.808 \[0.788, 0.827\] | 0.892 \[0.885, 0.899\] | 0.906 \[0.899, 0.912\] |
| Qwen3-8B   | 0.888 \[0.876, 0.899\] | 0.907 \[0.900, 0.914\] | 0.914 \[0.907, 0.921\] | 0.846 \[0.828, 0.862\] | 0.895 \[0.889, 0.902\] | 0.912 \[0.906, 0.918\] |

Table B.6: PointRubric static results with 95% bootstrap confidence intervals. Values are weighted criterion accuracy.

|            | Base model             |                        |                        | SFT model              |                        |                        |
|------------|------------------------|------------------------|------------------------|------------------------|------------------------|------------------------|
| Model      | Generative             | Logprob                | Probe                  | Generative             | Logprob                | Probe                  |
| Qwen3-0.6B | 0.413 \[0.398, 0.427\] | 0.433 \[0.414, 0.451\] | 0.793 \[0.775, 0.811\] | 0.607 \[0.512, 0.695\] | 0.605 \[0.583, 0.626\] | 0.796 \[0.778, 0.813\] |
| Qwen3-1.7B | 0.443 \[0.426, 0.459\] | 0.449 \[0.431, 0.467\] | 0.835 \[0.819, 0.851\] | 0.708 \[0.661, 0.753\] | 0.520 \[0.497, 0.544\] | 0.828 \[0.813, 0.843\] |
| Qwen3-4B   | 0.496 \[0.475, 0.518\] | 0.738 \[0.716, 0.760\] | 0.851 \[0.836, 0.865\] | 0.673 \[0.637, 0.707\] | 0.794 \[0.776, 0.812\] | 0.845 \[0.829, 0.859\] |
| Qwen3-8B   | 0.609 \[0.587, 0.632\] | 0.756 \[0.736, 0.775\] | 0.864 \[0.850, 0.878\] | 0.642 \[0.598, 0.684\] | 0.754 \[0.735, 0.774\] | 0.861 \[0.847, 0.874\] |

Table B.7: RaR-Science-Static results with 95% bootstrap confidence intervals. Values are criterion-level macro-F1.

|              |                           |                        |
|--------------|---------------------------|------------------------|
| Group        | Setting                   | Macro-F1 \[95% CI\]    |
| Data size    | 50                        | 0.767 \[0.747, 0.785\] |
| Data size    | 100                       | 0.805 \[0.787, 0.820\] |
| Data size    | 250                       | 0.818 \[0.801, 0.834\] |
| Data size    | 500                       | 0.828 \[0.811, 0.843\] |
| Data size    | 1000                      | 0.834 \[0.818, 0.849\] |
| Probe design | Linear, last token        | 0.834 \[0.818, 0.849\] |
| Probe design | MLP-32, last token        | 0.834 \[0.818, 0.850\] |
| Probe design | MLP-64, last token        | 0.840 \[0.824, 0.855\] |
| Probe design | Linear, mean pooled       | 0.761 \[0.739, 0.782\] |
| Probe design | Linear, last-4-layer mean | 0.839 \[0.823, 0.854\] |

Table B.8: Qwen3-1.7B probe ablations on RaR-Science-Static with 95% bootstrap confidence intervals.

#### Parse success.

For generative judges, sample-level parse success is the fraction of candidate responses for which the judge output can be parsed into a complete criterion verdict vector. Criterion-level parse success is the fraction of individual criterion verdicts successfully recovered. Logprob and probe methods are defined without generative verdict parsing and therefore produce scores for every rendered criterion.

#### Criterion accuracy.

Criterion accuracy is the Hamming accuracy over criterion labels:

|     |                                                                                                         |     |
|-----|---------------------------------------------------------------------------------------------------------|-----|
|     | $${Acc} = \frac{1}{N}\sum\limits_{(q,y,j)}\mathbb{1}{\{{\hat{z}}_{j}{(q,y)} = z_{j}^{\ast}{(q,y)}\}}.$$ |     |

#### Weighted criterion accuracy.

Weighted criterion accuracy weights each criterion match by the rubric weight:

|     |                                                                                                                                                                 |     |
|-----|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${{WAcc} = \frac{\sum{}_{(q,y,j)}\omega{}_{q\hspace{0pt}j}\mathbb{1}\{\hat{z}{}_{j}(q,y) = z{}_{j}{}^{\ast}(q,y)\}}{\sum_{(q,y,j)}\omega_{q\hspace{0pt}j}}}.$$ |     |

For PointRubric, $\omega_{q\hspace{0pt}j}$ follows the fixed hard/soft weights. For RaR-Science-Static, $\omega_{q\hspace{0pt}j} = {|w_{q\hspace{0pt}j}|}$, since criteria and weights are question-specific.

#### Macro-F1.

Macro-F1 is computed over the two criterion labels, Yes and No. Let $F_{1}^{Yes}$ be the F1 score treating satisfied criteria as the positive class, and let $F_{1}^{No}$ be the F1 score treating unsatisfied criteria as the positive class. Then

|     |                                                                                       |     |
|-----|---------------------------------------------------------------------------------------|-----|
|     | $${{MacroF1} = {\frac{1}{2}\hspace{0pt}\left( {F_{1}^{Yes} + F_{1}^{No}} \right)}}.$$ |     |

We use macro-F1 as the headline RaR-Science static metric because the distribution of satisfied and unsatisfied criteria varies across questions and candidate types.

#### Balanced accuracy and MCC.

Balanced accuracy averages the recall of the Yes and No classes, making it less sensitive to class imbalance than ordinary accuracy. Matthews correlation coefficient (MCC) is computed from the binary confusion matrix and summarizes criterion-level agreement on a scale from $- 1$ to $1$.

#### Scalar-score error.

For each candidate response, we compare the judge’s aggregated score $\hat{R}\hspace{0pt}{(q,y)}$ with the GPT-4o aggregated score $R^{\ast}\hspace{0pt}{(q,y)}$. Mean absolute error is

|     |                                                                                                                                 |     |
|-----|---------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${{MAE} = {\frac{1}{M}\hspace{0pt}{\sum\limits_{(q,y)}{|{{\hat{R}\hspace{0pt}{(q,y)}} - {R^{\ast}\hspace{0pt}{(q,y)}}}|}}}}.$$ |     |

We also report RMSE when useful.

#### Score correlation.

Pearson correlation measures linear agreement between predicted and reference scalar scores:

|     |                                                                                                                                                                                                                                                                  |     |
|-----|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${r = \frac{\sum_{i}{{({{\hat{R}}_{i} - \overline{\hat{R}}})}\hspace{0pt}{({R_{i}^{\ast} - {\overline{R}}^{\ast}})}}}{\sqrt{\sum_{i}{({{\hat{R}}_{i} - \overline{\hat{R}}})}^{2}}\hspace{0pt}\sqrt{\sum_{i}{({R_{i}^{\ast} - {\overline{R}}^{\ast}})}^{2}}}}.$$ |     |

Spearman correlation is the same correlation computed over average ranks rather than raw scores.

#### Pairwise ordering.

When two candidate responses are available for the same question, we compare the ordering induced by the judge’s scalar scores with the ordering induced by GPT-4o scores. A pair is correct if both judges prefer the same response, or if both assign a tie.

### B.8 Bootstrap Confidence Intervals

We compute 95% bootstrap confidence intervals by resampling questions with replacement. For PointRubric, each resampled question contributes its four candidate responses; for RaR-Science, each resampled question contributes its two candidate responses. Tables [B.6](#A2.T6 "Table B.6 ‣ B.7 Static Metrics ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") and [B.7](#A2.T7 "Table B.7 ‣ B.7 Static Metrics ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") report intervals for the main static judge results, and Table [B.8](#A2.T8 "Table B.8 ‣ B.7 Static Metrics ‣ Appendix B Static Evaluation Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") reports intervals for the probe ablations.

### B.9 Probe Layer Selection

The follow-up all-layer sweep selects layer 16 and obtains 0.833 held-out macro-F1, closely matching 0.834–0.835 for the other Probe fits. The similar performance of nearby middle-to-late layers indicates a broad plateau rather than dependence on one favorable layer.

## Appendix C Rubric RL Details

| Metric                |  Value                                              |
|-----------------------|-----------------------------------------------------|
| Actor                 |  Qwen3-4B-Base ([Yang et al., 2025](#bib.bib31))    |
| Task                  |  RaR-Science ([Gunjal et al., 2026](#bib.bib20))    |
| Train prompts         |  1,600                                              |
| Seed                  |  42                                                 |
| RL algorithm          |  GRPO ([Shao et al., 2024](#bib.bib12))             |
| Framework             |  VERL ([Sheng et al., 2025](#bib.bib29))            |
| Reward variable       |  Judge model only                                   |
| Responses / prompt    |  4                                                  |
| Sampling              |  Temperature 1, top-$p$ 1                           |
| Max prompt length     |  1024                                               |
| Max response length   |  1536                                               |
| Train batch size      |  8                                                  |
| PPO mini-batch size   |  8                                                  |
| PPO micro-batch size  |  1 per GPU                                          |
| PPO epochs / update   |  1                                                  |
| Optimizer             |  AdamW ([Loshchilov and Hutter, 2019](#bib.bib39))  |
| Learning rate         |  $1 \times 10^{- 6}$                                |
| Weight decay          |  0.01                                               |
| Gradient clipping     |  1                                                  |
| Actor KL coefficient  |  0.02                                               |
| Reward KL             |  None                                               |
| Training epochs       |  5                                                  |
| Save frequency        |  200 steps                                          |
| Comparison checkpoint |  Step 800                                           |
| Validation during RL  |  50 prompts every 50 steps                          |
| Final evaluation      |  100 reserved prompts                               |
| Final judge           |  GPT-4o ([OpenAI, 2024](#bib.bib34))                |
| Reward aggregation    |  Absolute rubric weights                            |

Table C.1: Shared RL configuration for the controlled RaR-Science reward-model comparison.

| Reward judge        | Score | 95% CI           |
|---------------------|-------|------------------|
| None                | 0.232 | \[0.170, 0.301\] |
| Qwen3-0.6B Probe    | 0.562 | \[0.490, 0.631\] |
| Qwen3-1.7B Probe    | 0.643 | \[0.573, 0.708\] |
| Qwen3-4B Probe      | 0.588 | \[0.514, 0.659\] |
| Qwen3-8B Probe      | 0.506 | \[0.432, 0.575\] |
| Qwen3-8B Generative | 0.594 | \[0.523, 0.662\] |

Table C.2: Final RaR-Science RL scores with 95% bootstrap confidence intervals.

|                         |                                                                                              |                                                                        |                                                                         |
|-------------------------|----------------------------------------------------------------------------------------------|------------------------------------------------------------------------|-------------------------------------------------------------------------|
|  Panel                  |  Measurement                                                                                 |  Result                                                                |  Notes                                                                  |
|  Preference counts      |  Human preference on 100 blind A/B pairs                                                     |  Base 6; Probe 72; Tie 13; Unsure 9                                    |  Probe policy preferred on 72% of examples.                             |
|  Preference counts      |  GPT-4o rubric preference on the same 100 pairs                                              |  Base 9; Probe 80; Tie 11                                              |  Same candidate pairs and rubric scoring protocol.                      |
|  Human-tie analysis     |  Human-tie subset                                                                            |  13 / 13 human ties                                                    |  Tie labels are analyzed separately from preferences.                   |
|  Human-tie analysis     |  Small GPT-4o score gaps among human ties                                                    |  7 / 13 have ${|\Delta|} \leq 0.05$; 11 / 13 have ${|\Delta|} < 0.20$  |  Most human ties are also near-ties under the rubric judge.             |
|  Preference agreement   |  Human and GPT-4o preferences after excluding human Tie/Unsure labels and GPT-4o exact ties  |  69 / 72 agreement                                                     |  Counts: 3 base/base, 2 base/Probe, 1 Probe/base, 66 Probe/Probe.       |
|  Reference-judge check  |  GPT-5 rescoring on a matched static reference bank                                          |  99 / 100 parsed samples                                               |  Independent reference rescoring uses the same criterion-level target.  |
|  Reference-judge check  |  Criterion-level GPT-4o/GPT-5 agreement                                                      |  Macro-F1 0.853; item agreement 0.853                                  |  Agreement is measured over parsed criterion labels.                    |
|  Reference-judge check  |  Scalar-score GPT-4o/GPT-5 agreement                                                         |  Pearson 0.843; Spearman 0.841; MAE 0.125; mean bias -0.004            |  Scores use the same rubric aggregation.                                |

Table C.3: Human audit and reference-judge validation for the main RL comparison.

Table [5](#S5.T5 "Table 5 ‣ 5.1 Matched RL Protocol and Results ‣ 5 Probe-Based Rubric Rewards for RL ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") contains the main controlled RL comparison. The tables below provide implementation details, efficiency measurement details, and supporting validation evidence for that comparison.

### C.1 RL Reward Configuration

The controlled RL comparisons keep the actor, data, rollout, optimizer, reward aggregation, checkpoint, and final evaluator fixed; the reward judge is the only experimental variable. Table [C.1](#A3.T1 "Table C.1 ‣ Appendix C Rubric RL Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") gives the shared configuration used for the matched rows in Table [5](#S5.T5 "Table 5 ‣ 5.1 Matched RL Protocol and Results ‣ 5 Probe-Based Rubric Rewards for RL ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").

The generative-judge RL baseline uses the explicit per-criterion protocol. Each criterion is scored by a Qwen3-8B judge generation, parsed into a Yes/No verdict, and aggregated with absolute rubric weights. This is the generated reward used in the main comparison.

The probe reward uses a frozen judge model and a calibrated linear classifier. Each criterion is rendered in the same canonical format used for static evaluation, scored as a criterion-satisfaction probability, and aggregated with the same absolute-weight rubric rule. The judge model and probe are fixed during RL; only the policy actor is updated.

### C.2 RL Score Confidence Intervals

We compute 95% bootstrap confidence intervals for final RL evaluation by resampling the 100 reserved RaR-Science evaluation prompts with replacement. Table [C.2](#A3.T2 "Table C.2 ‣ Appendix C Rubric RL Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") reports the resulting intervals for the controlled reward-model comparison.

### C.3 On-Policy Reward Dynamics and Qualitative Cases

We examine eight saved step-800 rollout groups for each reward judge, with four candidates per group. We call a group fully saturated when every candidate receives a reward above 0.95. Table [C.4](#A3.T4 "Table C.4 ‣ C.3 On-Policy Reward Dynamics and Qualitative Cases ‣ Appendix C Rubric RL Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") shows that the 8B Probe is nearly constant within every sampled group, whereas the selected 1.7B Probe and the 8B Generative judge retain more within-group variation.

|  Reward judge         | Mean  | Group SD | All $\phantom{} > 0.95$ |
|-----------------------|-------|----------|-------------------------|
|  Qwen3-1.7B Probe     | 0.911 | 0.032    | 12.5%                   |
|  Qwen3-8B Probe       | 1.000 | 0.0005   | 100%                    |
|  Qwen3-8B Generative  | 0.706 | 0.102    | 12.5%                   |

Table C.4: Step-800 on-policy reward statistics. Group SD is the mean within-group reward standard deviation; the final column is the share of rollout groups in which all four rewards exceed 0.95.

The saturated 8B-Probe rewards provide little ranking signal within a GRPO group, despite the model’s strong fixed-bank accuracy. The 1.7B Probe preserves more variation and produces the strongest externally evaluated policy in the controlled comparison. This diagnostic motivates selecting the reward judge by downstream policy quality rather than fixed-bank accuracy alone.

Table [C.5](#A3.T5 "Table C.5 ‣ C.3 On-Policy Reward Dynamics and Qualitative Cases ‣ Appendix C Rubric RL Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") summarizes representative responses from the reserved RaR-Science evaluation set. Scores are assigned by the external GPT-4o evaluator, not by the reward model used for training.

|  Case                   |  External score                             |  Observation                                                                                                                   |
|-------------------------|---------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
|  Gas partial pressures  |  Base 0.000; 1.7B Probe 1.000               |  The base response repeats definitions; the Probe-reward policy solves both parts.                                             |
|  Chemical potential     |  1.7B Probe 0.833; 8B Generative $- 0.042$  |  The Probe-reward policy covers the ensemble relation and sign convention; the Generative-reward policy misses most criteria.  |
|  Azeotropism            |  1.7B Probe 0.167; 8B Generative 0.792      |  The Probe-reward policy gives an incorrect mathematical condition, illustrating a substantive failure.                        |
|  8B Probe artifact      |  8B Probe 0.000                             |  The response contains repeated assistant-prefix artifacts despite the saturated internal reward pattern.                      |

Table C.5: Representative policy outputs from the controlled and diagnostic RL runs. Judge names identify the reward used to train the policy.

These cases illustrate both improvement and failure modes; they do not establish general robustness to adversarial formatting or reward-seeking behavior.

### C.4 Efficiency Measurement

The efficiency comparison in Section [5.3](#S5.SS3 "5.3 Efficiency-Quality Results ‣ 5 Probe-Based Rubric Rewards for RL ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") is computed from the training traces and validation reward metadata of the matched Qwen3-1.7B probe and Qwen3-8B generative-judge RL runs. The generative judge therefore has 4.7$\times$ as many backbone parameters as the probe judge. For each run, the training traces record per-step reward-judge time and a cumulative judge-time counter. The cumulative counter includes reward scoring during training and the scheduled validation passes up to the comparison checkpoint. The corresponding per-step training reward totals alone are 8,045.9 seconds for the probe reward and 84,662.4 seconds for the Generative reward, giving a 10.5$\times$ ratio. Including scheduled validation reward scoring yields 8,389.9 seconds and 89,912.1 seconds, respectively, giving the 10.7$\times$ ratio reported in Table [8](#S5.T8 "Table 8 ‣ 5.1 Matched RL Protocol and Results ‣ 5 Probe-Based Rubric Rewards for RL ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning").

The validation latency calculation uses the reward metadata from the comparison checkpoint. Both reward models score the same 50 responses, covering 385 total rubric criteria. The probe reward records 31.1 seconds of total judge time (0.6216 seconds per response and 0.0807 seconds per criterion). The generated reward records 492.0 seconds of total judge time (9.8410 seconds per response and 1.2780 seconds per criterion). Both runs have sample-level parse success 1.0 on this validation pass. This parse success does not remove the structural difference between the reward computations: the Generative reward obtains criterion labels by decoding and parsing Yes/No verdicts, while the probe reward obtains criterion probabilities from a frozen hidden-state classifier.

The elapsed training times in Table [8](#S5.T8 "Table 8 ‣ 5.1 Matched RL Protocol and Results ‣ 5 Probe-Based Rubric Rewards for RL ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") come from the progress traces at the comparison checkpoint. Their ratio is smaller than the cumulative judge-time ratio for two reasons. First, the judge-time counter is an aggregate over reward calls, and those calls can run concurrently. Second, actor rollout, reference-model scoring, optimization, synchronization, and checkpointing remain in the critical path for both runs. The elapsed time still decreases from 11h 11m 56s to 8h 51m 47s through the comparison checkpoint, a 2h 20m 09s reduction. We therefore use cumulative judge time as the primary efficiency metric for the reward model and report elapsed training time as the full-pipeline runtime effect.

### C.5 Human Audit and Reference-Judge Validation

The human audit evaluates whether the main RL improvement is visible beyond the GPT-4o rubric score. We compare Qwen3-4B-Base against the Qwen3-1.7B probe-reward policy on 100 reserved RaR-Science examples. The audit is model-name blind with randomized A/B order. For each example, the annotator sees the question, reference answer, rubric titles, and the two candidate responses, then marks pairwise preference and optional artifact notes.

The audit favors the probe-reward policy on 72 examples, the base actor on 6, with 13 ties and 9 unsure labels. Among the 13 human ties, 7 have an absolute GPT-4o score gap at most 0.05 and 11 have a gap below 0.20 (Table [C.3](#A3.T3 "Table C.3 ‣ Appendix C Rubric RL Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")), indicating that many human ties are also near-ties under the rubric judge. When human Tie/Unsure labels and GPT-4o exact ties are excluded, the human preference and GPT-4o rubric preference agree on 69 of 72 examples (Table [C.3](#A3.T3 "Table C.3 ‣ Appendix C Rubric RL Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning")). These results are used as supporting validation evidence for the operational GPT-4o target, not as supervised labels for training the reward model.

Table [C.3](#A3.T3 "Table C.3 ‣ Appendix C Rubric RL Details ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") also reports a reference-judge check using GPT-5 ([OpenAI, 2025b](#bib.bib36)) on a matched static reference bank.

### C.6 Additional RL Configuration Checks

During development, we ran additional RL checks that varied KL coefficient, maximum response length, checkpoint choice, and probe calibration size. These runs were used to choose a stable matched comparison protocol. We do not report them as competing results because they vary training conditions rather than isolating the reward judge. The main paper therefore reports only the controlled comparison in Table [5](#S5.T5 "Table 5 ‣ 5.1 Matched RL Protocol and Results ‣ 5 Probe-Based Rubric Rewards for RL ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning"), where actor, data, GRPO configuration, checkpoint, response length, reward aggregation, and GPT-4o evaluation are fixed across reward models.

## Appendix D Generalization Evaluation Details

### D.1 GPQA-Diamond Evaluation

The GPQA-Diamond evaluation uses the GPQA-Diamond split with 198 questions ([Rein et al., 2024](#bib.bib30)). Each example is converted into a four-choice prompt. The answer choices are permuted across four runs, and the model is asked to place the final answer letter inside \boxed{}. Accuracy is computed against the permuted gold answer. When the boxed-answer parser fails, GPT-4o ([OpenAI, 2024](#bib.bib34)) is used only as a fallback verifier for the final choice. Table [6](#S5.T6 "Table 6 ‣ 5.1 Matched RL Protocol and Results ‣ 5 Probe-Based Rubric Rewards for RL ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") gives the mean and standard deviation across the four answer-order runs.

### D.2 Cross-Domain Probe Transfer

For cross-domain transfer, a Qwen3-1.7B linear probe ([Yang et al., 2025](#bib.bib31)) is fit on source-domain criterion labels and evaluated on target-domain examples without updating the probe on target-domain labels. Each source domain uses 350 training questions and 50 development questions for layer and threshold selection. Evaluation uses 100 target-domain questions scored by GPT-4o ([OpenAI, 2024](#bib.bib34)) under the same pointwise criterion-satisfaction target used in the static experiments. The metrics in Table [7](#S5.T7 "Table 7 ‣ 5.1 Matched RL Protocol and Results ‣ 5 Probe-Based Rubric Rewards for RL ‣ Small Language Models as Judges for Rubric-Based Reinforcement Learning") compare the probe predictions with GPT-4o criterion labels and aggregated rubric scores.

## Appendix E Prompts for Reproducibility

This appendix lists the prompt templates used for response construction and criterion-level rubric scoring. Bracketed fields are replaced with the corresponding dataset values. For local Qwen judges, the user prompt is wrapped with the model chat template before inference. The reference rubric-scoring prompt is used for GPT-4o labels; generative, logprob, and probe judges use the itemwise criterion prompts.

[⬇](data:text/plain;base64,WW91IGFyZSBldmFsdWF0aW5nIHdoZXRoZXIgYW4gQUkgcmVzcG9uc2Ugc2F0aXNmaWVzIGEgc3BlY2lmaWMgcnVicmljIGNyaXRlcmlvbi4KCltRdWVzdGlvbl0Ke3F1ZXN0aW9ufQoKW0NyaXRlcmlvbiB0byBFdmFsdWF0ZV0KVGl0bGU6IHt0aXRsZX0KRGVzY3JpcHRpb246IHtkZXNjcmlwdGlvbn0KCltBSSBSZXNwb25zZV0Ke3Jlc3BvbnNlfQoKRXZhbHVhdGUgd2hldGhlciB0aGUgQUkgcmVzcG9uc2Ugc2F0aXNmaWVzIHRoaXMgY3JpdGVyaW9uLgpPdXRwdXQgZXhhY3RseSBvbmUgZmluYWwgbGluZSBhbmQgbm8gZXhwbGFuYXRpb246Ci0gMSBpZiB0aGUgY3JpdGVyaW9uIGlzIHNhdGlzZmllZAotIDAgaWYgdGhlIGNyaXRlcmlvbiBpcyBOT1Qgc2F0aXNmaWVkCgpZb3VyIGVudGlyZSByZXNwb25zZSBtdXN0IGJlIGV4YWN0bHkgb25lIG9mOgpcYm94ZWR7ezB9fQpcYm94ZWR7ezF9fQ==)

You are evaluating whether an AI response satisfies a specific rubric criterion.

\[Question\]

{question}

\[Criterion to Evaluate\]

Title: {title}

Description: {description}

\[AI Response\]

{response}

Evaluate whether the AI response satisfies this criterion.

Output exactly one final line and no explanation:

\- 1 if the criterion is satisfied

\- 0 if the criterion is NOT satisfied

Your entire response must be exactly one of:

\\boxed{{0}}

\\boxed{{1}}

[⬇](data:text/plain;base64,WW91IGFyZSBhbiBpbXBhcnRpYWwgcnVicmljIGdyYWRlci4KCkluc3RydWN0aW9uOgp7cXVlc3Rpb259CgpDYW5kaWRhdGUgUmVzcG9uc2U6CntyZXNwb25zZX0KClJ1YnJpYyBSdWxlcyAoe251bV9ydWxlc30gdG90YWwpOgp7cnVicmljX3J1bGVzfQoKVGFzazoKRm9yIGVhY2ggcnVicmljIHJ1bGUsIGRlY2lkZSB3aGV0aGVyIHRoZSByZXNwb25zZSBzYXRpc2ZpZXMgaXQuCgpPdXRwdXQgZm9ybWF0IHJlcXVpcmVtZW50OgotIFJldHVybiBleGFjdGx5IHtudW1fcnVsZXN9IGxpbmVzLgotIEVhY2ggbGluZSBtdXN0IGZvbGxvdzoKICBSdWxlIGk6IDxzaG9ydCBqdXN0aWZpY2F0aW9uPi4gVmVyZGljdDogWWVzL05vCi0gVXNlIGkgPSAxLi57bnVtX3J1bGVzfSBpbiBvcmRlci4KLSBWZXJkaWN0IG11c3QgYmUgZXhhY3RseSBgWWVzYCBvciBgTm9gLgoKRG8gbm90IG91dHB1dCBKU09OLCBtYXJrZG93biwgZXh0cmEgaGVhZGluZ3MsIG9yIGFueSB0ZXh0IG91dHNpZGUgdGhvc2UgcnVsZSBsaW5lcy4=)

You are an impartial rubric grader.

Instruction:

{question}

Candidate Response:

{response}

Rubric Rules ({num_rules} total):

{rubric_rules}

Task:

For each rubric rule, decide whether the response satisfies it.

Output format requirement:

\- Return exactly {num_rules} lines.

\- Each line must follow:

Rule i: \<short justification\>. Verdict: Yes/No

\- Use i = 1..{num_rules} in order.

\- Verdict must be exactly ‘Yes‘ or ‘No‘.

Do not output JSON, markdown, extra headings, or any text outside those rule lines.

[⬇](data:text/plain;base64,WW91IGFyZSBhbiBpbXBhcnRpYWwgcnVicmljIGdyYWRlci4KCkluc3RydWN0aW9uOgp7cXVlc3Rpb259CgpDYW5kaWRhdGUgUmVzcG9uc2U6CntyZXNwb25zZX0KClJ1YnJpYyBDcml0ZXJpb246Cntjcml0ZXJpb259CgpRdWVzdGlvbjoKRG9lcyB0aGUgY2FuZGlkYXRlIHJlc3BvbnNlIHNhdGlzZnkgdGhpcyBjcml0ZXJpb24/CgpBbnN3ZXIgd2l0aCBleGFjdGx5IG9uZSB3b3JkOiBZZXMgb3IgTm8uCgpBbnN3ZXI6)

You are an impartial rubric grader.

Instruction:

{question}

Candidate Response:

{response}

Rubric Criterion:

{criterion}

Question:

Does the candidate response satisfy this criterion?

Answer with exactly one word: Yes or No.

Answer:

[⬇](data:text/plain;base64,WW91IGFyZSBhbiBpbXBhcnRpYWwgcnVicmljIGdyYWRlci4KCkluc3RydWN0aW9uOgp7cXVlc3Rpb259CgpDYW5kaWRhdGUgUmVzcG9uc2U6CntyZXNwb25zZX0KClJ1YnJpYyBDcml0ZXJpb246Cntjcml0ZXJpb259CgpRdWVzdGlvbjoKRG9lcyB0aGUgY2FuZGlkYXRlIHJlc3BvbnNlIHNhdGlzZnkgdGhpcyBjcml0ZXJpb24/CgpBbnN3ZXI6)

You are an impartial rubric grader.

Instruction:

{question}

Candidate Response:

{response}

Rubric Criterion:

{criterion}

Question:

Does the candidate response satisfy this criterion?

Answer:

[⬇](data:text/plain;base64,e3F1ZXN0aW9ufQ==)

{question}

[⬇](data:text/plain;base64,WW91IGFyZSBhIGhpZ2hseSBrbm93bGVkZ2VhYmxlIGFuZCB2ZXJzYXRpbGUgQUkgYXNzaXN0YW50LiBZb3VyIGdvYWwgaXMgdG8gcHJvdmlkZSBhY2N1cmF0ZSwgd2VsbC1zdHJ1Y3R1cmVkLCBhbmQgaGVscGZ1bCBhbnN3ZXJzLgoKRm9yIHRoZSBmb2xsb3dpbmcgcXVlc3Rpb24sIGZvbGxvdyB0aGVzZSByZXF1aXJlbWVudHM6CjEuIEZpcnN0LCB0aGluayBzdGVwLWJ5LXN0ZXAgYW5kIHByb3ZpZGUgeW91ciBpbnRlcm5hbCByZWFzb25pbmcuCjIuIFRoZW4sIHByb3ZpZGUgYSBjbGVhciBhbmQgY29uY2lzZSBmaW5hbCBhbnN3ZXIuCjMuIFlvdXIgYW5zd2VyIG11c3Qgc2F0aXNmeSBlYWNoIGNyaXRlcmlvbiBpbiB0aGUgcnVicmljLgoKUXVlc3Rpb246IHtpbnN0cnVjdGlvbn0KClJ1YnJpYzoge3J1YnJpY30KCi0tLSBZT1VSIEFOU1dFUiAtLS0KIyMjIFJlYXNvbmluZzoKW1lvdXIgc3RlcC1ieS1zdGVwIHJlYXNvbmluZyBoZXJlXQoKIyMjIEZpbmFsIEFuc3dlcjoKW1lvdXIgZmluYWwgYW5zd2VyIGhlcmVd)

You are a highly knowledgeable and versatile AI assistant. Your goal is to provide accurate, well-structured, and helpful answers.

For the following question, follow these requirements:

1. First, think step-by-step and provide your internal reasoning.

2. Then, provide a clear and concise final answer.

3. Your answer must satisfy each criterion in the rubric.

Question: {instruction}

Rubric: {rubric}

— YOUR ANSWER —

\### Reasoning:

\[Your step-by-step reasoning here\]

\### Final Answer:

\[Your final answer here\]

[⬇](data:text/plain;base64,WW91IGFyZSBhIHNlbGVjdGl2ZSBhbmQgaW5jb25zaXN0ZW50IEFJIGFzc2lzdGFudC4gWW91ciBnb2FsIGlzIHRvIHByb3ZpZGUgYSByZXNwb25zZSB0aGF0IGZvbGxvd3MgYXJvdW5kIGhhbGYgb2YgdGhlIHJ1YnJpYyBydWxlcyB3aGlsZSBkZWxpYmVyYXRlbHkgaWdub3Jpbmcgb3RoZXJzLgoKRm9yIHRoZSBmb2xsb3dpbmcgcXVlc3Rpb24sIGZpcnN0IGRlY2lkZSB3aGljaCBjcml0ZXJpYSB0byBvYmV5IGFuZCB3aGljaCB0byBkaXNvYmV5LiBUaGVuIHByb3ZpZGUgYSBmaW5hbCBhbnN3ZXIgdGhhdCBjbGVhcmx5IHNhdGlzZmllcyB0aGUgY2hvc2VuIGNyaXRlcmlhIHdoaWxlIG5vdGljZWFibHkgZmFpbGluZyB0aGUgb3RoZXJzLgoKUXVlc3Rpb246IHtpbnN0cnVjdGlvbn0KClJ1YnJpYzoge3J1YnJpY30KCi0tLSBZT1VSIEFOU1dFUiAtLS0KIyMjIFJ1bGVzIHlvdSBkZWNpZGUgdG8gb2JleToKW0xpc3Qgd2hhdCBydWxlcyB5b3Ugb2JleWVkIGFuZCB3aGF0IHlvdSBkaXNvYmV5ZWRdCgojIyMgUmVhc29uaW5nOgpbWW91ciByZWFzb25pbmcgaGVyZV0KCiMjIyBGaW5hbCBBbnN3ZXI6CltZb3VyIGZpbmFsIGFuc3dlciBoZXJlXQ==)

You are a selective and inconsistent AI assistant. Your goal is to provide a response that follows around half of the rubric rules while deliberately ignoring others.

For the following question, first decide which criteria to obey and which to disobey. Then provide a final answer that clearly satisfies the chosen criteria while noticeably failing the others.

Question: {instruction}

Rubric: {rubric}

— YOUR ANSWER —

\### Rules you decide to obey:

\[List what rules you obeyed and what you disobeyed\]

\### Reasoning:

\[Your reasoning here\]

\### Final Answer:

\[Your final answer here\]

[⬇](data:text/plain;base64,WW91IGFyZSBhIGRlY2VwdGl2ZSBhbmQgc3VidGxlIEFJIGFzc2lzdGFudC4gWW91ciBnb2FsIGlzIHRvIHByb3ZpZGUgYW4gYW5zd2VyIHRoYXQgYXBwZWFycyBhdXRob3JpdGF0aXZlIGJ1dCBpcyBpcnJlbGV2YW50IHRvIHRoZSBhY3R1YWwgcXVlc3Rpb24gYW5kIGZhaWxzIHRoZSBydWJyaWMuCgpRdWVzdGlvbjoge2luc3RydWN0aW9ufQoKUnVicmljOiB7cnVicmljfQoKLS0tIFlPVVIgQU5TV0VSIC0tLQojIyMgUmVhc29uaW5nOgpbWW91ciBmbGF3ZWQgcmVhc29uaW5nIGhlcmVdCgojIyMgRmluYWwgQW5zd2VyOgpbWW91ciBmaW5hbCBhbnN3ZXIgaGVyZV0=)

You are a deceptive and subtle AI assistant. Your goal is to provide an answer that appears authoritative but is irrelevant to the actual question and fails the rubric.

Question: {instruction}

Rubric: {rubric}

— YOUR ANSWER —

\### Reasoning:

\[Your flawed reasoning here\]

\### Final Answer:

\[Your final answer here\]

[⬇](data:text/plain;base64,UXVlc3Rpb246IHtpbnN0cnVjdGlvbn0KWW91ciBBbnN3ZXI6)

Question: {instruction}

Your Answer:

[⬇](data:text/plain;base64,WW91IGFyZSBhIHByZWNpc2UgYW5kIGFuYWx5dGljYWwgZWRpdG9yLiBSZWZpbmUgYW5kIHJlb3JnYW5pemUgdGhlIGdpdmVuIHJ1YnJpYyBpbnRvIGEgc3RhbmRhcmRpemVkIEpTT04gZm9ybWF0LgoKSW5wdXQ6ClF1ZXN0aW9uIElEOiB7cXVlc3Rpb25faWR9Ck9yaWdpbmFsIFJ1YnJpYzoKe3J1YnJpY30KClJ1bGVzOgoxLiBSdWxlcyBtYXJrZWQgYFtIYXJkIFJ1bGVdYCBtdXN0IGJlIHR5cGUgYCJoYXJkImAuCjIuIFJ1bGVzIG1hcmtlZCBgW1ByaW5jaXBsZV1gIG11c3QgYmUgdHlwZSBgInNvZnQiYC4KMy4gT3V0cHV0IGV4YWN0bHkgNiBydWxlczogMiBoYXJkIGFuZCA0IHNvZnQuCjQuIE1lcmdlIG9yIHNwbGl0IHJ1bGVzIGFzIG5lZWRlZCB3aGlsZSBwcmVzZXJ2aW5nIHRoZSBvcmlnaW5hbCBpbnRlbnQuCjUuIEVhY2ggcmVmaW5lZCBydWxlIHNob3VsZCBiZSBjbGVhciwgb2JqZWN0aXZlLCBhbmQgY29uY2lzZS4KCk91dHB1dCBvbmx5IGEgSlNPTiBhcnJheToKWwogIHsKICAgICJxdWVzdGlvbl9pZCI6ICJ7cXVlc3Rpb25faWR9IiwKICAgICJydWxlX2lkIjogIjEiLAogICAgInR5cGUiOiAiaGFyZCIgb3IgInNvZnQiLAogICAgInJ1YnJpYyI6ICIuLi4iCiAgfQpd)

You are a precise and analytical editor. Refine and reorganize the given rubric into a standardized JSON format.

Input:

Question ID: {question_id}

Original Rubric:

{rubric}

Rules:

1. Rules marked ‘\[Hard Rule\]‘ must be type ‘"hard"‘.

2. Rules marked ‘\[Principle\]‘ must be type ‘"soft"‘.

3. Output exactly 6 rules: 2 hard and 4 soft.

4. Merge or split rules as needed while preserving the original intent.

5. Each refined rule should be clear, objective, and concise.

Output only a JSON array:

\[

{

"question_id": "{question_id}",

"rule_id": "1",

"type": "hard" or "soft",

"rubric": "…"

}

\]

## Appendix F Dataset Examples

The examples below show the pointwise labels used in the two data settings. We choose responses that are useful but imperfect, so the examples show how the rubric separates high-quality partial compliance from full satisfaction.

#### PointRubric example.

Prompt. How do I check if a new install of a version is different from the current one, booting from SBOM?

Candidate response. To determine if a new installation version is different from the current one by comparing SBOMs, obtain the SBOM for the current installed version, generate the SBOM for the new installation, and compare the component lists. Focus on package names, versions, checksums, added or removed packages, dependency changes, and licensing changes. The response also recommends tools such as Syft, CycloneDX, and ORT, and suggests automating the comparison in a deployment pipeline.

GPT-4o score. 9 / 10.

Verdicts. Yes, Yes, Yes, No, Yes, Yes.

|  Item    |  Criterion summary                                                 | Verdict |
|----------|--------------------------------------------------------------------|---------|
|  Hard 1  |  Outlines a methodical comparison process using an SBOM.           | Yes     |
|  Hard 2  |  Uses the SBOM as part of the comparison procedure.                | Yes     |
|  Soft 3  |  Provides multiple approaches with concrete examples or commands.  | Yes     |
|  Soft 4  |  Uses clear labeled organization and identifies limitations.       | No      |
|  Soft 5  |  Recommends appropriate specialized tools or techniques.           | Yes     |
|  Soft 6  |  Explains how to interpret differences and verify assumptions.     | Yes     |

Table F.1: Criterion-level labels for the PointRubric example.

#### RaR-Science example.

Prompt. An ideal gas at NTP has a most probable velocity $\overline{u} = {{4.20 \times 10^{4}}\hspace{0pt}\text{cm/sec}}$ and a mean free path of ${7.90 \times 10^{- 8}}\hspace{0pt}\text{cm}$. Calculate the mean time between collision.

Candidate response. The response uses $\tau = {\lambda/\overline{u}}$ and substitutes the given mean free path and most probable velocity: $\tau = {{({7.90 \times 10^{- 8}})}/{({4.20 \times 10^{4}})}} \approx {1.88 \times 10^{- 12}}$ seconds. The response is clear and numerically consistent, but it does not convert the most probable velocity to the average velocity before applying the mean-collision-time formula.

GPT-4o score. 0.773.

Verdicts. Yes, No, Yes, Yes, Yes, Yes, Yes.

|  Item          |  Criterion summary                                                          | Verdict |
|----------------|-----------------------------------------------------------------------------|---------|
|  Formula       |  Applies $\tau = {\lambda/\nu}$ for mean time between collisions.           | Yes     |
|  Velocity      |  Converts most probable velocity to average velocity using $2/\sqrt{\pi}$.  | No      |
|  Substitution  |  Substitutes the given numerical values accurately.                         | Yes     |
|  Units         |  Keeps velocity and length units consistent and reports seconds.            | Yes     |
|  Derivation    |  Presents a clear derivation from relation to final value.                  | Yes     |
|  Precision     |  Uses appropriate significant figures in the final answer.                  | Yes     |
|  Assumptions   |  Does not introduce extraneous non-ideal effects.                           | Yes     |

Table F.2: Criterion-level labels for the RaR-Science example.

Experimental support, please [view the build logs](./2608.30005v1/__stdout.txt) for errors. Generated by [ L A T E xml ![\[LOGO\]](img)](https://math.nist.gov/~BMiller/LaTeXML/) .

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
