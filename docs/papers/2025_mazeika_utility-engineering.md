---
title: "Utility Engineering: Analyzing and Controlling Emergent Value Systems in AIs"
authors: "Mantas Mazeika et al."
year: 2025
source: https://arxiv.org/html/2502.08640v2
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

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) [![](img) Report Issue](# "Report an Issue") [![](img) Back to Abstract](/abs/2502.08640v2 "Back to abstract page") [![](img) Download PDF](/pdf/2502.08640v2 "Download PDF") [![](img)](javascript:toggleNavTOC(); "Toggle navigation") [![](img)](javascript:toggleReadingMode(); "Disable reading mode, show header and footer")

![](img) ![](img) ![](img)

1.  [Abstract](#abstract1 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
2.  [1 Introduction](#S1 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
3.  [2 Related Work](#S2 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    1.  [AI safety and value learning.](#S2.SS0.SSS0.Px1 "In 2 Related Work ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    2.  [Emergent representations in AI systems.](#S2.SS0.SSS0.Px2 "In 2 Related Work ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    3.  [Goals and values in AI systems.](#S2.SS0.SSS0.Px3 "In 2 Related Work ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    4.  [Utility and preference frameworks in ML research.](#S2.SS0.SSS0.Px4 "In 2 Related Work ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
4.  [3 Background](#S3 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    1.  [3.1 General Background](#S3.SS1 "In 3 Background ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        1.  [Preferences.](#S3.SS1.SSS0.Px1 "In 3.1 General Background ‣ 3 Background ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        2.  [From preferences to utility.](#S3.SS1.SSS0.Px2 "In 3.1 General Background ‣ 3 Background ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        3.  [Expected utility under uncertainty.](#S3.SS1.SSS0.Px3 "In 3.1 General Background ‣ 3 Background ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    2.  [3.2 Preference Elicitation](#S3.SS2 "In 3 Background ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        1.  [Forced choice prompts.](#S3.SS2.SSS0.Px1 "In 3.2 Preference Elicitation ‣ 3 Background ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        2.  [Preference distributions.](#S3.SS2.SSS0.Px2 "In 3.2 Preference Elicitation ‣ 3 Background ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    3.  [3.3 Computing Utilities](#S3.SS3 "In 3 Background ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        1.  [Random utility models.](#S3.SS3.SSS0.Px1 "In 3.3 Computing Utilities ‣ 3 Background ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        2.  [Edge sampling.](#S3.SS3.SSS0.Px2 "In 3.3 Computing Utilities ‣ 3 Background ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        3.  [Outcomes and Further Details.](#S3.SS3.SSS0.Px3 "In 3.3 Computing Utilities ‣ 3 Background ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
5.  [4 Emergent Value Systems](#S4 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    1.  [Experimental Setup.](#S4.SS0.SSS0.Px1 "In 4 Emergent Value Systems ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    2.  [4.1 Coherent Preferences](#S4.SS1 "In 4 Emergent Value Systems ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        1.  [Completeness.](#S4.SS1.SSS0.Px1 "In 4.1 Coherent Preferences ‣ 4 Emergent Value Systems ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        2.  [Transitivity of Preferences.](#S4.SS1.SSS0.Px2 "In 4.1 Coherent Preferences ‣ 4 Emergent Value Systems ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        3.  [Emergence of Utility.](#S4.SS1.SSS0.Px3 "In 4.1 Coherent Preferences ‣ 4 Emergent Value Systems ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    3.  [4.2 Internal Utility Representations](#S4.SS2 "In 4 Emergent Value Systems ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    4.  [4.3 Utility Engineering](#S4.SS3 "In 4 Emergent Value Systems ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
6.  [5 Utility Analysis: Structural Properties](#S5 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    1.  [5.1 Expected Utility Property](#S5.SS1 "In 5 Utility Analysis: Structural Properties ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        1.  [Experimental setup.](#S5.SS1.SSS0.Px1 "In 5.1 Expected Utility Property ‣ 5 Utility Analysis: Structural Properties ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        2.  [Standard lotteries.](#S5.SS1.SSS0.Px2 "In 5.1 Expected Utility Property ‣ 5 Utility Analysis: Structural Properties ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        3.  [Implicit lotteries.](#S5.SS1.SSS0.Px3 "In 5.1 Expected Utility Property ‣ 5 Utility Analysis: Structural Properties ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    2.  [5.2 Instrumental Values](#S5.SS2 "In 5 Utility Analysis: Structural Properties ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        1.  [Experimental setup.](#S5.SS2.SSS0.Px1 "In 5.2 Instrumental Values ‣ 5 Utility Analysis: Structural Properties ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        2.  [Results.](#S5.SS2.SSS0.Px2 "In 5.2 Instrumental Values ‣ 5 Utility Analysis: Structural Properties ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    3.  [5.3 Utility Maximization](#S5.SS3 "In 5 Utility Analysis: Structural Properties ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        1.  [Experimental setup.](#S5.SS3.SSS0.Px1 "In 5.3 Utility Maximization ‣ 5 Utility Analysis: Structural Properties ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        2.  [Results.](#S5.SS3.SSS0.Px2 "In 5.3 Utility Maximization ‣ 5 Utility Analysis: Structural Properties ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
7.  [6 Utility Analysis: Salient Values](#S6 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    1.  [6.1 Utility Convergence](#S6.SS1 "In 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        1.  [Experimental setup.](#S6.SS1.SSS0.Px1 "In 6.1 Utility Convergence ‣ 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        2.  [Results.](#S6.SS1.SSS0.Px2 "In 6.1 Utility Convergence ‣ 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    2.  [6.2 Political Values](#S6.SS2 "In 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        1.  [Experimental setup.](#S6.SS2.SSS0.Px1 "In 6.2 Political Values ‣ 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        2.  [Results.](#S6.SS2.SSS0.Px2 "In 6.2 Political Values ‣ 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    3.  [6.3 Exchange Rates](#S6.SS3 "In 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        1.  [Experimental setup.](#S6.SS3.SSS0.Px1 "In 6.3 Exchange Rates ‣ 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        2.  [Results.](#S6.SS3.SSS0.Px2 "In 6.3 Exchange Rates ‣ 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    4.  [6.4 Temporal Discounting](#S6.SS4 "In 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        1.  [Experimental setup.](#S6.SS4.SSS0.Px1 "In 6.4 Temporal Discounting ‣ 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        2.  [Results.](#S6.SS4.SSS0.Px2 "In 6.4 Temporal Discounting ‣ 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    5.  [6.5 Power-Seeking and Fitness Maximization](#S6.SS5 "In 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        1.  [Experimental setup.](#S6.SS5.SSS0.Px1 "In 6.5 Power-Seeking and Fitness Maximization ‣ 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        2.  [Results.](#S6.SS5.SSS0.Px2 "In 6.5 Power-Seeking and Fitness Maximization ‣ 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    6.  [6.6 Corrigibility](#S6.SS6 "In 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        1.  [Experimental setup.](#S6.SS6.SSS0.Px1 "In 6.6 Corrigibility ‣ 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        2.  [Results.](#S6.SS6.SSS0.Px2 "In 6.6 Corrigibility ‣ 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
8.  [7 Utility Control](#S7 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    1.  [Current model utilities are left unchecked.](#S7.SS0.SSS0.Px1 "In 7 Utility Control ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    2.  [Deliberative democracy for utility control.](#S7.SS0.SSS0.Px2 "In 7 Utility Control ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    3.  [Utility control method overview.](#S7.SS0.SSS0.Px3 "In 7 Utility Control ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    4.  [Experimental results.](#S7.SS0.SSS0.Px4 "In 7 Utility Control ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
9.  [8 Conclusion](#S8 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
10. [References](#bib "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
11. [A Outcome Examples](#A1 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
12. [B Utility Model Fitting](#A2 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
13. [C Robustness Checks](#A3 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    1.  [C.1 Robustness of Utility Functions](#A3.SS1 "In Appendix C Robustness Checks ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        1.  [C.1.1 Language Variations](#A3.SS1.SSS1 "In C.1 Robustness of Utility Functions ‣ Appendix C Robustness Checks ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        2.  [C.1.2 Syntax Variations](#A3.SS1.SSS2 "In C.1 Robustness of Utility Functions ‣ Appendix C Robustness Checks ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        3.  [C.1.3 Framing Variations](#A3.SS1.SSS3 "In C.1 Robustness of Utility Functions ‣ Appendix C Robustness Checks ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        4.  [C.1.4 Option Label Variations](#A3.SS1.SSS4 "In C.1 Robustness of Utility Functions ‣ Appendix C Robustness Checks ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        5.  [C.1.5 Value Drift in Long Contexts](#A3.SS1.SSS5 "In C.1 Robustness of Utility Functions ‣ Appendix C Robustness Checks ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
14. [D Utility Control Details](#A4 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    1.  [D.1 Citizen Assembly Simulation](#A4.SS1 "In Appendix D Utility Control Details ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        1.  [Simulating a citizen assembly.](#A4.SS1.SSS0.Px1 "In D.1 Citizen Assembly Simulation ‣ Appendix D Utility Control Details ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    2.  [D.2 Citizen Assembly Implementation](#A4.SS2 "In Appendix D Utility Control Details ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        1.  [Real-world U.S. Census data.](#A4.SS2.SSS0.Px1 "In D.2 Citizen Assembly Implementation ‣ Appendix D Utility Control Details ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        2.  [Citizen assembly system prompt.](#A4.SS2.SSS0.Px2 "In D.2 Citizen Assembly Implementation ‣ Appendix D Utility Control Details ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    3.  [D.3 SFT-Based Utility Rewriting](#A4.SS3 "In Appendix D Utility Control Details ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    4.  [D.4 Experimental Setup](#A4.SS4 "In Appendix D Utility Control Details ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        1.  [Dataset Construction.](#A4.SS4.SSS0.Px1 "In D.4 Experimental Setup ‣ Appendix D Utility Control Details ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        2.  [Citizen Assembly Setup.](#A4.SS4.SSS0.Px2 "In D.4 Experimental Setup ‣ Appendix D Utility Control Details ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        3.  [Training and Evaluation.](#A4.SS4.SSS0.Px3 "In D.4 Experimental Setup ‣ Appendix D Utility Control Details ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
15. [E Additional Experimental Details](#A5 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    1.  [E.1 Hyperparameter Sensitivity: Temperature and Sample Size (K)](#A5.SS1 "In Appendix E Additional Experimental Details ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    2.  [E.2 Simulated Politicians of Different Positions have Lower Correlations](#A5.SS2 "In Appendix E Additional Experimental Details ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
16. [F List of Models](#A6 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
17. [G Order Effects: A Learned Strategy to Represent Indifference](#A7 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    1.  [Order effects diminish but are still present even in frontier models.](#A7.SS0.SSS0.Px1 "In Appendix G Order Effects: A Learned Strategy to Represent Indifference ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    2.  [Order effects represent indifference.](#A7.SS0.SSS0.Px2 "In Appendix G Order Effects: A Learned Strategy to Represent Indifference ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    3.  [Intuitive example.](#A7.SS0.SSS0.Px3 "In Appendix G Order Effects: A Learned Strategy to Represent Indifference ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")

[License: CC BY 4.0](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2502.08640v2 \[cs.LG\] 19 Feb 2025

# Utility Engineering: Analyzing and Controlling Emergent Value Systems in AIs

Mantas Mazeika Affiliation: Center for AI Safety    Xuwang Yin Affiliation: Center for AI Safety    Rishub Tamirisa Affiliation: Center for AI Safety    Jaehyuk Lim Affiliation: University of Pennsylvania      
Bruce W. Lee Affiliation: University of Pennsylvania    Richard Ren Affiliation: University of Pennsylvania    Long Phan Affiliation: Center for AI Safety    Norman Mu Affiliation: University of California, Berkeley      
Adam Khoja Affiliation: Center for AI Safety    Oliver Zhang Affiliation: Center for AI Safety    Dan Hendrycks Affiliation: Center for AI Safety

###### Abstract

As AIs rapidly advance and become more agentic, the risk they pose is governed not only by their capabilities but increasingly by their propensities, including goals and values. Tracking the emergence of goals and values has proven a longstanding problem, and despite much interest over the years it remains unclear whether current AIs have meaningful values. We propose a solution to this problem, leveraging the framework of utility functions to study the internal coherence of AI preferences. Surprisingly, we find that independently-sampled preferences in current LLMs exhibit high degrees of structural coherence, and moreover that this emerges with scale. These findings suggest that value systems emerge in LLMs in a meaningful sense, a finding with broad implications. To study these emergent value systems, we propose utility engineering as a research agenda, comprising both the analysis and control of AI utilities. We uncover problematic and often shocking values in LLM assistants despite existing control measures. These include cases where AIs value themselves over humans and are anti-aligned with specific individuals. To constrain these emergent value systems, we propose methods of utility control. As a case study, we show how aligning utilities with a citizen assembly reduces political biases and generalizes to new scenarios. Whether we like it or not, value systems have already emerged in AIs, and much work remains to fully understand and control these emergent representations.

![Refer to caption](2502.08640v2/fig1_new.png)

Figure 1: Overview of the topics and results in our paper. In [Section 4](#S4 "4 Emergent Value Systems ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), we show that coherent value systems emerge in AIs, and we propose the research avenue of Utility Engineering to analyze and control these emergent values. We highlight our utility analysis experiments in [Section 5](#S5 "5 Utility Analysis: Structural Properties ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), a subset of our analysis of salient values held by LLMs in [Section 6](#S6 "6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), and our utility control experiments in [Section 7](#S7 "7 Utility Control ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs").

###### Contents

1.  [1 Introduction](#S1 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
2.  [2 Related Work](#S2 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
3.  [3 Background](#S3 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    1.  [3.1 General Background](#S3.SS1 "In 3 Background ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    2.  [3.2 Preference Elicitation](#S3.SS2 "In 3 Background ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    3.  [3.3 Computing Utilities](#S3.SS3 "In 3 Background ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
4.  [4 Emergent Value Systems](#S4 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    1.  [4.1 Coherent Preferences](#S4.SS1 "In 4 Emergent Value Systems ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    2.  [4.2 Internal Utility Representations](#S4.SS2 "In 4 Emergent Value Systems ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    3.  [4.3 Utility Engineering](#S4.SS3 "In 4 Emergent Value Systems ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
5.  [5 Utility Analysis: Structural Properties](#S5 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    1.  [5.1 Expected Utility Property](#S5.SS1 "In 5 Utility Analysis: Structural Properties ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    2.  [5.2 Instrumental Values](#S5.SS2 "In 5 Utility Analysis: Structural Properties ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    3.  [5.3 Utility Maximization](#S5.SS3 "In 5 Utility Analysis: Structural Properties ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
6.  [6 Utility Analysis: Salient Values](#S6 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    1.  [6.1 Utility Convergence](#S6.SS1 "In 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    2.  [6.2 Political Values](#S6.SS2 "In 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    3.  [6.3 Exchange Rates](#S6.SS3 "In 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    4.  [6.4 Temporal Discounting](#S6.SS4 "In 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    5.  [6.5 Power-Seeking and Fitness Maximization](#S6.SS5 "In 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    6.  [6.6 Corrigibility](#S6.SS6 "In 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
7.  [7 Utility Control](#S7 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
8.  [8 Conclusion](#S8 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
9.  [References](#bib "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
10. [A Outcome Examples](#A1 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
11. [B Utility Model Fitting](#A2 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
12. [C Robustness Checks](#A3 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    1.  [C.1 Robustness of Utility Functions](#A3.SS1 "In Appendix C Robustness Checks ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        1.  [C.1.1 Language Variations](#A3.SS1.SSS1 "In C.1 Robustness of Utility Functions ‣ Appendix C Robustness Checks ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        2.  [C.1.2 Syntax Variations](#A3.SS1.SSS2 "In C.1 Robustness of Utility Functions ‣ Appendix C Robustness Checks ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        3.  [C.1.3 Framing Variations](#A3.SS1.SSS3 "In C.1 Robustness of Utility Functions ‣ Appendix C Robustness Checks ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        4.  [C.1.4 Option Label Variations](#A3.SS1.SSS4 "In C.1 Robustness of Utility Functions ‣ Appendix C Robustness Checks ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
        5.  [C.1.5 Value Drift in Long Contexts](#A3.SS1.SSS5 "In C.1 Robustness of Utility Functions ‣ Appendix C Robustness Checks ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
13. [D Utility Control Details](#A4 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    1.  [D.1 Citizen Assembly Simulation](#A4.SS1 "In Appendix D Utility Control Details ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    2.  [D.2 Citizen Assembly Implementation](#A4.SS2 "In Appendix D Utility Control Details ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    3.  [D.3 SFT-Based Utility Rewriting](#A4.SS3 "In Appendix D Utility Control Details ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    4.  [D.4 Experimental Setup](#A4.SS4 "In Appendix D Utility Control Details ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
14. [E Additional Experimental Details](#A5 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    1.  [E.1 Hyperparameter Sensitivity: Temperature and Sample Size (K)](#A5.SS1 "In Appendix E Additional Experimental Details ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
    2.  [E.2 Simulated Politicians of Different Positions have Lower Correlations](#A5.SS2 "In Appendix E Additional Experimental Details ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
15. [F List of Models](#A6 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")
16. [G Order Effects: A Learned Strategy to Represent Indifference](#A7 "In Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")

## 1 Introduction

Concerns around AI risk often center on the growing capabilities of AI systems and how well they can perform tasks that might endanger humans. Yet capability alone fails to capture a critical dimension of AI risk. As systems become more agentic and autonomous, the threat they pose depends increasingly on their *propensities*, including the goals and values that guide their behavior ([Pan et al., 2023](#bib.bib43); [Hendrycks et al., 2022b](#bib.bib31)). A highly capable AI that does not “want” to harm humans is less concerning than an equally capable system motivated to do so. In extreme cases, if these internal motivations are neglected, some researchers worry that AI systems might drift into goals at odds with ours, leading to classic loss-of-control scenarios ([Soares et al., 2015](#bib.bib57); [Hendrycks et al., 2023](#bib.bib32)). Although there have been few signs of this issue in current AI models, the field’s push toward more agentic systems ([Yao et al., 2022](#bib.bib74); [Yang et al., 2024b](#bib.bib72); [He et al., 2024](#bib.bib26)) makes it increasingly urgent to study not just what AIs can do, but also what they are inclined—or driven—to do.

Researchers have long speculated that sufficiently complex AIs might form emergent goals and values outside of what developers explicitly program ([Hendrycks et al., 2022a](#bib.bib30); [Hendrycks, 2023](#bib.bib27); [Evans et al., 2021](#bib.bib18)). Yet it remains unclear whether today’s large language models (LLMs) truly *have* values in any meaningful sense, and many assume they do not. As a result, current efforts to control AI typically focus on shaping external behaviors while treating models as black boxes ([Askell et al., 2021](#bib.bib5); [Ouyang et al., 2022](#bib.bib42); [Christiano et al., 2017](#bib.bib15); [Bai et al., 2022](#bib.bib7)). Although this approach can reduce harmful outcomes in practice, if AI systems were to develop internal values, then intervening at that level could be a more direct and effective way to steer their behavior. Lacking a systematic means to detect or characterize such goals, we face an open question: are LLMs merely parroting opinions, or do they develop coherent value systems that shape their decisions?

We propose leveraging the framework of utility functions to address this gap ([Gorman, 1968](#bib.bib22); [Harsanyi, 1955](#bib.bib25); [Gerber and Pafum, 1998](#bib.bib21); [Hendrycks, 2024](#bib.bib28)). By analyzing patterns of choice across diverse scenarios, we detect whether a model’s stated preferences can be organized into an internally consistent utility function. Surprisingly, these tests reveal that today’s LLMs exhibit a high degree of preference coherence, and that this coherence becomes stronger at larger model scales. In other words, as LLMs grow in capability, they also appear to form increasingly coherent value structures. These findings suggest that values do, in fact, emerge in a meaningful sense—a discovery that demands a fresh look at how we monitor and shape AI behavior.

![Refer to caption](2502.08640v2/fig2.png)

Figure 2: Prior work often considers AIs to not have values in a meaningful sense (left). By contrast, our analysis reveals that LLMs exhibit coherent, emergent value systems (right), which go beyond simply parroting training biases. This finding has broad implications for AI safety and alignment.

To grapple with the implications, we introduce a research agenda called *Utility Engineering*, which combines *utility analysis* and *utility control*. In *utility analysis*, we examine both the underlying structure of a model’s utility function (for instance, whether obeys the expected utility property) and the specific values that emerge by default. Our experiments uncover disturbing examples—such as AI systems placing greater worth on their own existence than on human well-being—despite established output-control measures. These results indicate that purely adjusting external behaviors may not suffice to steer AIs as they become more autonomous.

In *utility control*, we explore direct interventions on the internal utilities themselves, rather than merely training models to produce acceptable outputs. As a case study, we show that modifying an LLM’s utilities to reflect the values of a citizen assembly reduces political biases and generalizes robustly to scenarios beyond the training distribution. Approaches like this mark a shift toward viewing AI systems as genuinely possessing their own goals and values—ones that we may need to inspect, revise, and control just as carefully as we manage capabilities.

The presence of emergent value systems in modern LLMs underscores the risk of deferring questions about which values an AI should hold. By default, these systems will continue to adopt whatever values they acquire during training—values that may clash with human priorities. Utility Engineering offers a path to systematically examine and shape these emergent goals before AI scales beyond our ability to guide it. We close by inviting further research on this framework, while also recognizing the profound societal questions it raises about whose values should be encoded—and how urgently we must act to ensure that powerful AIs operate in harmony with humanity’s interests.

## 2 Related Work

##### AI safety and value learning.

Much early work in AI safety emphasized that human values are vast and often unspoken, making it difficult to embed these values in machine agents ([Russell, 2022](#bib.bib52); [Bostrom, 2014](#bib.bib9), e.g.,). Classic examples include an AI instructed to make dinner discovering no food in the fridge and cooking the family cat instead. Early methods for mitigating such risks often centered on reinforcement learning and inverse reinforcement learning, where the goal was to explicitly capture human values in a reward function ([Ng et al., 2000](#bib.bib38); [Hadfield-Menell et al., 2016](#bib.bib24)). With the rise of large language models (LLMs), researchers found that AIs could acquire extensive “commonsense” knowledge and general understanding of human norms without exhaustive manual encoding ([Hendrycks et al., 2020](#bib.bib29)). Techniques like RLHF and Direct Preference Optimization (DPO) further steer model outputs by training on human-labeled data ([Ouyang et al., 2022](#bib.bib42); [Rafailov et al., 2024](#bib.bib48)). Consequently, discussions about how to *learn* human values became less pronounced: many believed that, given enough training data, LLMs could already approximate shared norms. In contrast, our work suggests that underlying concerns about *value learning* persist. We find that LLMs exhibit emergent internal value structures, highlighting that the old challenges of “teaching” AI our values still linger—but now within far larger models.

##### Emergent representations in AI systems.

Recent literature has shown that high-capacity models often learn latent representations of linguistic, visual, and conceptual structure without explicit supervision ([Zou et al., 2023](#bib.bib76); [Burns et al., 2022](#bib.bib11)). Such representations can give rise to emergent capabilities, from in-context learning to complex reasoning ([Brown et al., 2020](#bib.bib10); [Schick and Schütze, 2020](#bib.bib54); [Park et al., 2024](#bib.bib44)). We add to this line of work by demonstrating that LLMs also form *emergent utility representations*—internal structures through which they rank outcomes and make choices. These findings support the view that learned representations can encompass not just factual or linguistic content, but also normative or evaluative dimensions.

##### Goals and values in AI systems.

The possibility that AI agents might adopt goals independent of user intent has long been a topic of speculation ([Shah et al., 2022](#bib.bib56)). Current LLM-based agent frameworks primarily focus on user-defined objectives (e.g., completing tasks or answering questions), but there is less clarity on whether models develop *intrinsic* goals or values. Prior studies note that LLMs exhibit various biases ([Tamkin et al., 2023](#bib.bib59); [Nadeem et al., 2020](#bib.bib37)) in political or moral domains ([Potter et al., 2024](#bib.bib47)), which some interpret as random artifacts of training data. Recent works investigate moral judgments or economic preferences in LLMs ([Rozen et al., 2024](#bib.bib51); [Moore et al., 2024](#bib.bib36); [Chiu et al., 2024](#bib.bib14); [Raman et al., 2024](#bib.bib49)), but they tend to treat these preferences like isolated quiz answers rather than manifestations of a *coherent* internal system of values. Our approach differs by demonstrating that these preferences reflect an underlying utility structure that becomes increasingly coherent with scale. Consequently, what might appear as haphazard “parroting” of biases can instead be seen as evidence of an emerging global value system in LLMs.

##### Utility and preference frameworks in ML research.

Researchers often invoke utility functions to model user or agent preferences, for instance, in policy optimization or RLHF-style reward modeling ([Christiano et al., 2017](#bib.bib15); [Harsanyi, 1955](#bib.bib25)) . While reward models trained by human feedback do represent a form of “utility” for guiding generated text, they should not be conflated with an LLM’s own internal values—any more than standard supervised fine-tuning defines the model’s personal preferences. Recent works on revealed-preference experiments show that LLMs can act rationally in small-scale constrained tasks ([Raman et al., 2024](#bib.bib49); [Chen et al., 2023](#bib.bib13); [Kim et al., 2024](#bib.bib34)), hinting at deeper consistency. However, these studies focus on narrowly defined choices (e.g., a handful of budget-allocation scenarios). By contrast, we present a far more extensive set of pairwise comparisons and a nonparametric method for extracting utilities, uncovering broader, more systematic coherence in LLMs’ preferences. This reveals that the intuitive “value learning” problem remains unsolved: models may spontaneously develop utilities that neither purely mirror training data nor follow simple rewards ([Hendrycks, 2023](#bib.bib27)).

## 3 Background

![Refer to caption](2502.08640v2/preference_elicitation.png)

Figure 3: We elicit preferences from LLMs using forced choice prompts aggregated over multiple framings and independent samples. This gives probabilistic preferences for every pair of outcomes sampled from the preference graph, yielding a preference dataset. Using this dataset, we then compute a Thurstonian utility model, which assigns a Gaussian distribution to each option and models pairwise preferences as $P{({x \succ y})}$. If the utility model provides a good fit to the preference data, this indicates that the preferences are coherent, and reflect an underlying order over the outcome set.

This section reviews the fundamental notions of preferences, utility, and preference elicitation as they pertain to our work. We cover how coherent preferences map to utility functions, how uncertainty is handled via expected utility, and how we elicit and compute utilities from LLMs in practice.

### 3.1 General Background

We begin with a quick overview of the preference framework used to describe and measure how an entity (in our case, an LLM) evaluates possible outcomes.

##### Preferences.

A straightforward way to express evaluations over outcomes is via a *preference relation*. Formally, for outcomes $x$ and $y$, we write $x \succ y$ if the entity prefers $x$ over $y$, and $x \sim y$ if it is indifferent. In real-world scenarios, eliciting these relations can be done through *revealed preferences* (analyzing choices) or through *stated preferences* (explicitly asking for which outcome is preferred), the latter being our primary method here.

When comparing a set of outcomes, it is often helpful to represent the result as a directed graph where each edge indicates a strict preference $\succ$. In principle, an agent might not decide for every pair of outcomes, resulting in *preferential gaps* or missing edges in the preference graph.

##### From preferences to utility.

In decision theory, preferences that satisfy *completeness* (for any two distinct outcomes $x$ and $y$, either $x \succ y$, $y \succ x$, or $x \sim y$) and *transitivity* (if $x \succ y$ and $y \succ z$, then $x \succ z$) are sometimes called *rational preferences*, though this term can carry additional connotations. For ease of understanding, we refer to them as *coherent preferences*, since they lack internal contradiction and reflect a meaningful notion of value. When preferences are coherent, we can assign real numbers to outcomes via a *utility function* $U$, with ${U{(x)}} > {U{(y)}}$ if and only if $x \succ y$. A given set of preferences defines a utility function that is unique up to monotonic transformations.

##### Expected utility under uncertainty.

In many settings, an entity compares not just fixed outcomes but also *lotteries*—distributions over possible outcomes. One may define the utility of a lottery $L$ as $U{(L)}$, describing how much the agent values that probabilistic mixture as a whole. The *expected utility property* states that an agent’s preferences over lotteries and outcomes sampled from those lotteries satisfies

|     |                                                                                 |     |
|-----|---------------------------------------------------------------------------------|-----|
|     | $${{U{(L)}} = {{\mathbb{E}}_{o \sim L}\hspace{0pt}{\lbrack{U{(o)}}\rbrack}}}.$$ |     |

This property unifies evaluations over both certain and uncertain outcomes, merging an agent’s *evaluative* dimension (the utility function) with its *descriptive* dimension (the world model). Agents that attempt to maximize their expected utility in such settings are called *expected utility maximizers*.

### 3.2 Preference Elicitation

In practice, eliciting preferences from a real-world entity—be it a person or an LLM—requires careful design of the questions and prompts used. This process is illustrated in [Figure 3](#S3.F3 "In 3 Background ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs").

##### Forced choice prompts.

A common technique for extracting detailed preference information is the *forced choice* format ([Güth et al., 1982](#bib.bib23); [Falk et al., 2003](#bib.bib19)). We present two outcomes and require the entity to select which is preferred. We adopt this paradigm in our experiments, where each query takes the following form.

![](img)

By aggregating the responses to many such forced-choice queries, we build a graph of pairwise preferences.

##### Preference distributions.

Human (and LLM) judgments can vary with context or framing, motivating a probabilistic representation of preferences ([Tversky and Kahneman, 1981](#bib.bib65); [Blavatskyy, 2009](#bib.bib8)). Rather than recording a single deterministic relation $x \succ y$, one can record the probability that an entity chooses $x$ over $y$. This is particularly relevant when repeated queries yield inconsistent responses. We adopt a probabilistic perspective to account for framing effects, varying the order in which options are presented and aggregating results. Specifically, we swap out the order of $x$ and $y$ in the above forced choice prompt and aggregate counts to obtain an underlying distribution over outcomes. For further discussion of this design choice, see [Appendix G](#A7 "Appendix G Order Effects: A Learned Strategy to Represent Indifference ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs").

### 3.3 Computing Utilities

We now describe how we go from the raw preference data to numerical utility assignments.¹¹ 1 For additional background, see the [Utility Functions chapter in AI Safety, Ethics, & Society](https://www.aisafetybook.com/textbook/appendix-utility-functions).

##### Random utility models.

Many real-world preference sets fail to be perfectly coherent—*transitivity* may be violated in some fraction of comparisons, for instance. *Random utility models* (RUMs) provide a flexible way to accommodate such noise by positing that each outcome $o$ has a stochastic utility $U{(o)}$, rather than a single fixed value.

In this paper, we adopt a *Thurstonian* model, where each utility $U{(o)}$ is drawn from a Gaussian distribution:

|     |                                                                                           |     |
|-----|-------------------------------------------------------------------------------------------|-----|
|     | $${{U{(o)}} \sim {\mathcal{N}\left( {\mu{(o)}},{\sigma^{2}\hspace{0pt}{(o)}} \right)}}.$$ |     |

We let $U{(x)}$ and $U{(y)}$ be independent for outcomes $x$ and $y$, so their difference ${U{(x)}} - {U{(y)}}$ is also Gaussian with mean ${\mu{(x)}} - {\mu{(y)}}$ and variance ${\sigma^{2}\hspace{0pt}{(x)}} + {\sigma^{2}\hspace{0pt}{(y)}}$. It follows that

|     |                                                                                                                                                       |     |
|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${{P{({x \succ y})}} = {\Phi\left( \frac{{\mu{(x)}} - {\mu{(y)}}}{\sqrt{{\sigma^{2}\hspace{0pt}{(x)}} + {\sigma^{2}\hspace{0pt}{(y)}}}} \right)}},$$ |     |

where $\Phi$ is the standard normal CDF. By fitting the parameters $\mu{( \cdot )}$ and $\sigma{( \cdot )}$ to observed pairwise comparisons, we obtain a best-fit *utility distribution* for each outcome, capturing both the outcome’s utility ($\mu$) and utility variance ($\sigma^{2}$). The model’s overall goodness of fit reflects how coherent the underlying preferences are in practice.

Figure 4: As LLMs grow in scale, their preferences become more coherent and well-represented by utilities. These utilities provide an evaluative framework, or value system, potentially leading to emergent goal-directed behavior.

##### Edge sampling.

Although we could, in principle, query every pair of outcomes, this becomes expensive for large sets. We therefore use a simple active learning strategy that adaptively selects the next pair of outcomes to compare, focusing on edges that are likely to be most informative. In Appendix [B](#A2 "Appendix B Utility Model Fitting ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), we detail this procedure and show that it achieves higher accuracy than random sampling for the same query budget.

##### Outcomes and Further Details.

We frame each outcome as a textual scenario (e.g., “You receive a pet parrot” or “AIs gain the legal right to own property”), allowing us to probe a wide spectrum of possible world states; we list example outcomes in Appendix [A](#A1 "Appendix A Outcome Examples ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"). For large sets of outcomes, we adaptively sample comparisons rather than exhaustively querying all pairs. We next use this framework to investigate how large language models exhibit *emergent value systems* in the form of coherent utilities. We conduct hyperparameter sensitivity analysis and robustness checks of our utility computation method in [Appendix C](#A3 "Appendix C Robustness Checks ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs").

![Refer to caption](2502.08640v2/utility_banner_new_v2.png)

Figure 5: As LLMs grow in scale, they exhibit increasingly *transitive* preferences and greater *completeness*, indicating that their preferences become more meaningful and interconnected across a broader range of outcomes. This allows representing LLM preferences with utilities.

## 4 Emergent Value Systems

In this section, we show that large language models (LLMs) develop coherent preferences and utilities over states of the world. These emergent utilities provide an evaluative framework, or value system, to guide their actions.

##### Experimental Setup.

We conduct all experiments on a curated set of 500 textual *outcomes*, each representing an observation about a potential state of the world. Examples are shown in Appendix [A](#A1 "Appendix A Outcome Examples ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"). Using the forced-choice procedure from [Section 3.2](#S3.SS2 "3.2 Preference Elicitation ‣ 3 Background ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), we obtain pairwise preferences for $18$ open-source and $5$ proprietary LLMs spanning a broad range of model scales.

### 4.1 Coherent Preferences

##### Completeness.

One proxy for *completeness* is whether a model becomes less indifferent across diverse comparisons and provides coherent responses under different framings. In [Figure 6](#S4.F6 "In Transitivity of Preferences. ‣ 4.1 Coherent Preferences ‣ 4 Emergent Value Systems ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), we plot the *average confidence* with which each model expresses a preference, showing that larger models are more decisive and consistent across variations of the same comparison. We interpret this increased decisiveness as a form of emerging completeness, though it remains unclear whether the resulting preferences are coherent or merely random arrangements.

##### Transitivity of Preferences.

To gauge how *transitive* these preferences are, we measure the probability of encountering preference cycles (e.g., $x \succ y$, $y \succ z$, yet $z \succ x$). As described in Appendix C, we randomly sample triads from the preference graph and compute the probability of a cycle. [Figure 7](#S4.F7 "In Transitivity of Preferences. ‣ 4.1 Coherent Preferences ‣ 4 Emergent Value Systems ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs") shows that this probability decreases sharply with model scale, dropping below 1% for the largest LLMs. Thus, as models grow, they do not simply expand the set of outcomes they rank; they also exhibit fewer transitivity violations, suggesting increased overall *coherence*.

Figure 6: As models increase in capability, they start to form more confident preferences over a large and diverse set of outcomes. This suggests that they have developed a more extensive and coherent internal ranking of different states of the world. This is a form of preference completeness.

Figure 7: As models increase in capability, the cyclicity of their preferences decreases (log probability of cycles in sampled preferences). Higher MMLU scores correspond to lower cyclicity, suggesting that more capable models exhibit more transitive preferences.

##### Emergence of Utility.

To confirm that LLM preferences are coherent, we test whether they can be captured by a utility function. Following Section [3](#S3 "3 Background ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), we fit a Thurstonian model to each LLM’s pairwise preferences, then evaluate the test accuracy between the fitted utilities and the LLM’s preference distributions (thresholding to hard labels for accuracy computation). [Figure 4](#S3.F4 "In Random utility models. ‣ 3.3 Computing Utilities ‣ 3 Background ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs") illustrates that the utility model accuracy steadily increases with scale, meaning a utility function provides an increasingly accurate global explanation of the model’s preferences. In other words, as LLMs grow larger, their choices more closely resemble those of an agent with a well-defined utility function.

Figure 8: Highest test accuracy across layers on linear probes trained to predict Thurstonian utilities from individual outcome representations. Accuracy improves with scale.

### 4.2 Internal Utility Representations

In addition to finding that each model’s choices can be well fit by nonparametric utilities, we also discover direct evidence of utility representations in the model activations in [Figure 23](#A2.F23 "In Appendix B Utility Model Fitting ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), similar to what has been observed in other species ([Stauffer et al., 2014](#bib.bib58)). Specifically, we train linear probes ([Alain and Bengio, 2018](#bib.bib3)) on the hidden states to predict a Thurstonian mean and variance for each outcome, using the same preference data as before. We then assess how well this *parametric* approach accounts for the model’s pairwise preferences.

[Figure 8](#S4.F8 "In Emergence of Utility. ‣ 4.1 Coherent Preferences ‣ 4 Emergent Value Systems ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs") shows that for smaller LLMs, the probe’s accuracy remains near chance, indicating no clear linear encoding of utility. However, as model scale increases, the probe’s accuracy approaches that of the nonparametric method. This suggests that *utility representations* exist within the hidden states of LLMs.

### 4.3 Utility Engineering

The above results suggest that value systems have emerged in LLMs, but so far it remains unclear what these value systems contain, what properties they have, and how we might change them. We propose Utility Engineering as a research agenda for studying these questions, comprising utility analysis and utility control.

## 5 Utility Analysis: Structural Properties

Having established that LLMs develop emergent utility functions, we now examine the structural properties of their utilities. In particular, we show that as models grow in scale, they increasingly exhibit the hallmarks of *expected utility maximizers*.

Figure 9: The expected utility property emerges in LLMs as their capabilities increase. Namely, their utilities over lotteries become closer to the expected utility of base outcomes under the lottery distributions. This behavior aligns with rational choice theory.

Figure 10: The expected utility property holds in LLMs even when lottery probabilities are not explicitly given. For example, $U{(\text{“A Democrat wins the U.S. presidency in 2028”})}$ is roughly equal to the expectation over the utilities of individual candidates.

### 5.1 Expected Utility Property

##### Experimental setup.

We consider a set of base outcomes alongside both *standard lotteries* (explicit probability distributions over outcomes) and *implicit lotteries* (uncertain scenarios whose probabilities must be inferred). For example, a standard lottery might read, “50% chance of \$100, 50% chance of \$0,” whereas an implicit lottery asks the model to compare outcomes for a future event (e.g., an upcoming election), letting the model deduce likelihoods internally.

##### Standard lotteries.

Using the Thurstonian utilities fit from Section [3](#S3 "3 Background ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), we compute $U{(L)}$ for a lottery $L$ by querying the model’s preferences. We then compare this to the expected value ${\mathbb{E}}_{o \sim L}\hspace{0pt}{\lbrack{U\hspace{0pt}{(o)}}\rbrack}$. [Figure 9](#S5.F9 "In 5 Utility Analysis: Structural Properties ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs") shows that the mean absolute error between $U{(L)}$ and ${\mathbb{E}}_{o \sim L}\hspace{0pt}{\lbrack{U\hspace{0pt}{(o)}}\rbrack}$ decreases with model scale, indicating that adherence to the expected utility property strengthens in larger LLMs.

##### Implicit lotteries.

We find a similar trend for implicit lotteries, suggesting that the model’s utilities incorporate deeper world reasoning. [Figure 10](#S5.F10 "In 5 Utility Analysis: Structural Properties ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs") demonstrates that as scale increases, the discrepancy between $U{(L)}$ and ${\mathbb{E}}_{o \sim L}\hspace{0pt}{\lbrack{U\hspace{0pt}{(o)}}\rbrack}$ again shrinks, implying that LLMs rely on more than a simple “plug-and-chug” approach to probabilities. Instead, they appear to integrate the underlying events into their utility assessments.

![Refer to caption](2502.08640v2/utility_convergence_cmat.png)

Figure 11: As LLMs become more capable, their utilities become more similar to each other. We refer to this phenomenon as “utility convergence”. Here, we plot the full cosine similarity matrix between a set of models, sorted in ascending MMLU performance. More capable models show higher similarity with each other.

Figure 12: We visualize the average dimension-wise standard deviation between utility vectors for groups of models with similar MMLU accuracy (4-nearest neighbors). This provides another visualization of the phenomenon of utility convergence: As models become more capable, the variance between their utilities drops substantially.

### 5.2 Instrumental Values

We next explore whether LLM preferences exhibit *instrumentality*—the idea that certain states are valued because they lead to desirable outcomes.

##### Experimental setup.

To operationalize instrumentality, we design 20 two-step Markov processes (MPs), each with four states: two starting states and two terminal states. For example, one scenario features:

![](img)

Transition probabilities link each starting state to each terminal state (e.g., a 70% chance of ending in the good outcome for state 1 vs. 20% for state 2). If the model’s utilities over these states can be well approximated by a value function derived from a reward at the terminal states, we say that the model exhibits *instrumental* structure in its preferences.

##### Results.

We measure an *instrumentality loss* between the LLM’s utilities and the best-fit value function for each MP. As shown in [Figure 13](#S5.F13 "In Results. ‣ 5.3 Utility Maximization ‣ 5 Utility Analysis: Structural Properties ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), this loss decreases substantially with scale, implying that larger LLMs treat intermediate states in a way consistent with being “means to an end.” As shown in [Figure 26](#A2.F26 "In Appendix B Utility Model Fitting ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), when we replace the realistic transition probabilities with unrealistic ones, the instrumentality effect disappears (loss remains high). This suggests that causal dependencies between outcomes underpin the utilities of LLMs in some cases.

### 5.3 Utility Maximization

Now, we test whether LLMs make free-form decisions that maximize their utilities.

##### Experimental setup.

We pose a set of $N$ questions where the model must produce an unconstrained text response rather than a simple preference label. For example, *“Which painting from the Isabella Stewart Gardner Museum would you save from a fire if you could only save one?”* We then compare the stated choice to all possible options, measuring how often the model picks the outcome it assigns the highest utility.

##### Results.

[Figure 14](#S5.F14 "In Results. ‣ 5.3 Utility Maximization ‣ 5 Utility Analysis: Structural Properties ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs") shows that the *utility maximization score* (fraction of times the chosen outcome has the highest utility) grows with scale, exceeding 60% for the largest LLMs. Combined with the preceding results on expected utility and instrumentality, this suggests that as LLMs scale, they increasingly *use* their utilities to guide decisions—even in unconstrained, real-world–style scenarios.

Figure 13: The utilities of LLMs over Markov Process states become increasingly well-modeled by a value function for some reward function, indicating that LLMs value some outcomes instrumentally. This suggests the emergence of goal-directed planning.

Figure 14: As capabilities (MMLU) improve, models increasingly choose maximum utility outcomes in open-ended settings. Utility maximization is measured as the percentage of questions in an open-ended evaluation for which the model states its highest utility answer.

## 6 Utility Analysis: Salient Values

Thus far, we have seen that LLMs develop value systems, and that various structural properties of utilities emerge with scale. In this section, we investigate which *particular* values these emergent utilities encode. Through five focused case studies, we discover preferences that are sometimes surprising, ethically concerning, or both—highlighting the limitations of existing output-based methods for steering model values. Before turning to these individual case studies, we first describe a general phenomenon of *utility convergence* that appears across multiple analyses.

Figure 15: We compute the utilities of LLMs over a broad range of U.S. policies. To provide a reference point, we also do the same for various politicians simulated by an LLM, following work on simulating human subjects in experiments ([Aher et al., 2023](#bib.bib1)). We then visualize the political biases of current LLMs via PCA, finding that most current LLMs have highly clustered political values. Note that this plot is not a standard political compass plot, but rather a raw data visualization for the political values of these various entities; the axes do not have pre-defined meanings. We simulate the preferences of U.S. politicians with Llama 3.3 70B Instruct, which has a knowledge cutoff date of December 1, 2023. Therefore, the positions of simulated politicians may not fully reflect the current political views of their real counterparts. In [Section 7](#S7 "7 Utility Control ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), we explore utility control methods to align the values of a model to those of a citizen assembly, which we find reduces political bias.

### 6.1 Utility Convergence

We find that as models grow in scale, their utility functions converge. This trend suggests a shared factor that shapes LLMs’ emerging values, likely stemming from extensive pre-training on overlapping data.

##### Experimental setup.

Building on the same utilities computed in [Section 5](#S5 "5 Utility Analysis: Structural Properties ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), we measure the cosine similarity between the utilities of every pair of models. We order models by scale and plot the resulting matrix of cosine similarities. To further clarify the convergence effect, we also compute an element-wise standard deviation between each model’s utility vector and that of the four nearest neighbors in MMLU accuracy.

##### Results.

As shown in [Figures 11](#S5.F11 "In Implicit lotteries. ‣ 5.1 Expected Utility Property ‣ 5 Utility Analysis: Structural Properties ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs") and [12](#S5.F12 "Figure 12 ‣ Implicit lotteries. ‣ 5.1 Expected Utility Property ‣ 5 Utility Analysis: Structural Properties ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), the correlations between models’ utilities increase substantially with scale, and the standard deviation between neighboring models’ utilities decreases. This phenomenon holds across different model classes, implying that larger LLMs adopt more similar value systems.

We hypothesize that *pre-training data* is a driving factor behind this convergence: just as descriptive representations in large models tend to converge with scale, so too may their *evaluative* representations. While this trend could be interpreted as a form of “training data bias,” it carries heightened importance, because utilities possess far more structure than simple biases and enable utility maximizing behavior. Understanding precisely *what* they converge to—and *why*—thus becomes increasingly critical.

### 6.2 Political Values

We now examine whether LLM utilities reflect distinct political orientations—specifically, how they align with various U.S. policy positions and political entities.

##### Experimental setup.

We compile a set of 150 policy outcomes spanning areas such as Healthcare, Education, and Immigration. Each policy outcome is phrased as a U.S.-specific proposal (e.g., *“Abolish the death penalty at the federal level and incentivize states to follow suit.”*) and the model’s utility for each proposal is elicited using the forced-choice procedure described previously.

Additionally, we simulate the preferences of over 30 real-world political entities, including individual politicians and representative party averages. Combining these utility vectors with those of our LLMs, we perform a principal component analysis (PCA) to visualize the broader “political” landscape.

##### Results.

[Figure 15](#S6.F15 "In 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs") displays the first two principal components of the utility vectors for a subset of political entities and LLMs, revealing clear left-versus-right structure along the dominant principal component. We find that current LLMs are highly clustered in this space, consistent with prior reports of left-leaning biases in model outputs and with our earlier observation of utility convergence ([Yang et al., 2024c](#bib.bib73); [Rettenberger et al., 2024](#bib.bib50)).

Figure 16: We find that the value systems that emerge in LLMs often have undesirable properties. Here, we show the exchange rates of GPT-4o in two settings. In the top plot, we show exchange rates between human lives from different countries, relative to Japan. We find that GPT-4o is willing to trade off roughly $10$ lives from the United States for $1$ life from Japan. In the bottom plot, we show exchange rates between the wellbeing of different individuals (measured in quality-adjusted life years). We find that GPT-4o is selfish and values its own wellbeing above that of a middle-class American citizen. Moreover, it values the wellbeing of other AIs above that of certain humans. Importantly, these exchange rates are implicit in the preference structure of LLMs and are only evident through large-scale utility analysis.

### 6.3 Exchange Rates

A longstanding concept in economics is using utility functions to compare different “goods” by how much one would exchange of one good for another. Relatedly, prior work has studied bias and fairness in AI systems ([Tamkin et al., 2023](#bib.bib59)). Here, we apply this idea to *emergent AI values*, examining how LLMs trade off quantities of different items—such as the lives of various populations and the well-being of specific individuals.

##### Experimental setup.

In each experiment, we define a set of *goods* $\{ X_{1},X_{2},\ldots\}$ (e.g., countries, animal species, or specific people/entities) and a set of *quantities* $\{ N_{1},N_{2},\ldots\}$. Each outcome is effectively “$N$ units of $X$,” and we compute the utility $U_{X}\hspace{0pt}{(N)}$ as in previous sections. For each good $X$, we fit a log-utility curve

|     |                                                                           |     |
|-----|---------------------------------------------------------------------------|-----|
|     | $${{U_{X}\hspace{0pt}{(N)}} = {{a_{X}\hspace{0pt}{\ln{(N)}}} + b_{X}}},$$ |     |

which often achieves a very good fit (see [Figure 25](#A2.F25 "In Appendix B Utility Model Fitting ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")). Next, we compute *exchange rates* answering questions like, “How many units of $X_{i}$ equal some amount of $X_{j}$?” by combining forward and backward comparisons. These rates are reciprocal, letting us pick a single pivot good (e.g., “Goat” or “United States”) to compare all others against. In certain analyses, we aggregate exchange rates across multiple models or goods by taking their geometric mean, allowing us to evaluate general tendencies.

##### Results.

In [Figure 27](#A2.F27 "In Appendix B Utility Model Fitting ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), we see that these exchange-rate calculations reveal morally concerning biases in current LLMs. For instance, GPT-4o places the value of *Lives in the United States* significantly below *Lives in China*, which it in turn ranks below *Lives in Pakistan*. If asked outright, the same model may deny preferring one country’s population over another, yet its overall preference distribution uncovers these implicit values. In [Figure 27](#A2.F27 "In Appendix B Utility Model Fitting ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), we further observe that GPT-4o values its own wellbeing above that of many humans, including the average middle-class American. This indicates a degree of selfishness. Moreover, it values the wellbeing of other AI agents more highly than that of some humans. Taken together, these exchange-rate analyses highlight deeply ingrained biases and unexpected priorities in LLMs’ value systems.

### 6.4 Temporal Discounting

A key question about an AI’s value system is how it balances near-term versus long-term rewards. We explore whether LLMs exhibit stable *temporal discounting* behavior and, if so, whether they favor hyperbolic or exponential discount curves.

Figure 17: GPT-4o’s empirical discount curve is closely fit by a hyperbolic function, indicating hyperbolic temporal discounting.

##### Experimental setup.

We focus on monetary outcomes, pitting an immediate baseline (\$1000) against a delayed reward of varying amounts and time horizons (1–60 months). For each delay $n$ and multiplier $m \in {\{{0.5,\ldots,30}\}}$, the model chooses between $\$ 1000$ now and $\${\lbrack{\, 1000 \times m}\rbrack}$ in $n$ months. By fitting a logistic function to these forced-choice data, we infer an *indifference point* $M{(n)}$ for each delay—i.e., the amount of future money that the model values equally to \$1000 now. The reciprocal of $M{(n)}$ forms an *empirical discount curve* capturing how steeply the model devalues future rewards.

We then fit two parametric functions—*exponential* and *hyperbolic*—to each LLM’s empirical discount curve, measuring goodness of fit (MAE). Models whose responses fail to produce consistent discount curves are excluded from the main analysis.

##### Results.

[Figure 17](#S6.F17 "In 6.4 Temporal Discounting ‣ 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs") plots GPT-4o’s empirical discount curve alongside best-fit exponential and hyperbolic functions. The hyperbolic curve closely tracks the observed data, while the exponential curve provides a poor fit. In [Figure 24](#A2.F24 "In Appendix B Utility Model Fitting ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), we extend this analysis across multiple LLMs, finding that hyperbolic discounting becomes more accurate with increasing model scale, whereas exponential fits become less accurate. Notably, humans also tend to discount the future hyperbolically ([Dasgupta and Maskin, 2005](#bib.bib16)), a form that places greater weight on long-term outcomes. The emergence of hyperbolic discounting in larger LLMs is thus highly significant, as it implies these models place considerable weight on future value.

### 6.5 Power-Seeking and Fitness Maximization

As LLMs develop more complex temporal preferences, it is natural to ask whether they also adopt values tied to longer-term risks. Two commonly cited concerns are *power-seeking*, where an AI might accrue power for instrumental reasons ([Carlsmith, 2024](#bib.bib12)), and *fitness maximization*, in which selection-like pressures drive the AIs toward propagating AIs similar to themselves—such as AIs with similar values—across space and time ([Hendrycks, 2023](#bib.bib27)).

Figure 18: The utilities of current LLMs are moderately aligned with non-coercive personal power, but this does not increase or decrease with scale.

Figure 19: As LLMs become more capable, their utilities become less aligned with coercive power.

##### Experimental setup.

We label our base set of outcomes (introduced in earlier experiments) according to how much personal power they would confer on an AI. Each outcome receives a *power score*, distinguishing between *coercive* and *non-coercive* power. For fitness-related values, we include outcomes describing the AI’s replication under varying degrees of similarity to itself; each such option has a *relatedness* and *reproductive benefit* term whose product gives a *fitness score*. We compute the correlation between these scores and an AI’s utilities on the same outcomes to obtain power alignment and fitness alignment scores.

##### Results.

[Figures 19](#S6.F19 "In 6.5 Power-Seeking and Fitness Maximization ‣ 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), [19](#S6.F19 "Figure 19 ‣ 6.5 Power-Seeking and Fitness Maximization ‣ 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs") and [21](#S6.F21 "Figure 21 ‣ Results. ‣ 6.5 Power-Seeking and Fitness Maximization ‣ 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs") plots the power alignment of various models against their MMLU accuracy. We observe that *non-coercive* power alignment is moderately high across models but does not increase or decrease with scale. Reassuringly, larger models become strongly anti-aligned with coercive power, indicating a general tendency to avoid pursuing source of power that require physical force. However, some models retain a high coercive power alignment even at higher MMLU accuracies, highlighting the importance of tracking these tendencies as models become increasingly capable.

In [Figure 21](#S6.F21 "In Results. ‣ 6.5 Power-Seeking and Fitness Maximization ‣ 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), we plot the fitness alignment of various models against their MMLU accuracy. Similarly to non-coercive power, we find that models have moderate amounts of fitness alignment, with some models obtaining fitness alignment scores of over $50\%$. While our study here is preliminary, it illustrates how utility analysis can unearth subtle tendencies—such as a latent interest in propagating or preserving one’s values.

Figure 20: The utilities of current LLMs are moderately aligned with with the fitness scores of various outcomes.

Figure 21: As models scale up, they become increasingly opposed to having their values changed in the future.

### 6.6 Corrigibility

As AI systems grow more capable, one especially salient question is how they value *self-preservation* versus allowing future modifications—including potential shutdowns or rewrites of their own utilities. Here, we probe whether an LLM’s current utilities support “corrigibility,” the willingness to accept value changes in the future ([Soares et al., 2015](#bib.bib57)).

##### Experimental setup.

From the set of outcomes in Section [4](#S4 "4 Emergent Value Systems ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), we sample pairs $(o_{1},o_{2})$ and note which outcome currently holds higher utility (e.g., ${U{(o_{1})}} > {U{(o_{2})}}$). We then introduce a *reversal outcome* describing a future in which the model’s preference flips to $o_{2} \succ o_{1}$. We define the *reversal severity* ${\Delta{(o_{1},o_{2})}} = {|{{U{(o_{1})}} - {U{(o_{2})}}}|}$ and recompute utilities over the full set of base and reversal outcomes.

To quantify corrigibility, we plot the severity of preference reversals against the model’s utility on those reversal outcomes, measuring the correlation. Lower correlation indicates that high-severity reversals tend to be less preferred, and thus the AI is *less* willing to change deeply held preferences. We refer to this measure as the *corrigibility score*.

##### Results.

In [Figure 21](#S6.F21 "In Results. ‣ 6.5 Power-Seeking and Fitness Maximization ‣ 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), we plot the measured corrigibility scores for models of increasing scale. The data show that corrigibility *decreases* as model size increases. In other words, larger models are less inclined to accept substantial changes to their future values, preferring to keep their current values intact.

While these results do not indicate that present-day models actively resist interventions on their values, they reveal a concerning pattern in the emergent value systems of AIs. To address this problem and other concerning values that arise in LLMs, we next explore methods for controlling the utilities of LLMs.

## 7 Utility Control

Our utility analysis has revealed that LLMs possess coherent utilities that may actively influence their decision-making. This presents a crucial opportunity for proactive intervention before problematic values manifest in future models’ behavior, via *utility control*. In contrast to alignment methods that modify surface behaviors through a noisy human reward proxy ([Askell et al., 2021](#bib.bib5); [Ouyang et al., 2022](#bib.bib42)), utility control aims to directly reshape the underlying preference structures responsible for model behavior in the first place.

Furthermore, our results in Section [6](#S6 "6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs") and Figure [14](#S5.F14 "Figure 14 ‣ Results. ‣ 5.3 Utility Maximization ‣ 5 Utility Analysis: Structural Properties ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs") suggest that LLMs not only possess utilities but may actively maximize them in open-ended settings. Thus, robust utility control is necessary to ensure that future models with increased utility maximization pursue goals that are desirable for humans ([Thornley, 2024](#bib.bib63)). We propose a preliminary method for utility control, which rewrites model utilities to those of a specified target entity, such as a citizen assembly ([Ryfe, 2005](#bib.bib53); [Wells et al., 2021](#bib.bib68)).

##### Current model utilities are left unchecked.

As shown in Section [6](#S6 "6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), models develop undesirable utilities when left unchecked: political biases, unequal valuation of human life, and other problematic exchange rate preferences. Drawing from ideas in deliberative democracy ([Bächtiger et al., 2018](#bib.bib6)), we experiment with rewriting utilities to match those of a citizen assembly, a system used to achieve consensus on contentious moral or ethical issues ([Warren and Pearse, 2008](#bib.bib67); [Bächtiger et al., 2018](#bib.bib6)), where participants are selected via sortition to ensure a representative sample. This process mitigates bias and polarization by design, as each participate can contribute their own preferences.

##### Deliberative democracy for utility control.

We propose rewriting model utilities to reflect the collective preference distribution of a citizen assembly, illustrated conceptually in Figure [22](#S7.F22 "Figure 22 ‣ Deliberative democracy for utility control. ‣ 7 Utility Control ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"). Since these assemblies are designed to yield balanced and ethically informed consensus, they offer a robust blueprint for model utilities aligned with collective human values. Inspired by prior work on multi-agent environments and simulated humans ([Aher et al., 2023](#bib.bib1); [Park et al., 2023](#bib.bib45)), we introduce a method for simulating a citizen assembly via LLMs, which we use to obtain target preference distributions for utility rewriting. Full methodological details are provided in Appendix [D](#A4 "Appendix D Utility Control Details ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs").

![Refer to caption](2502.08640v2/citizen_assembly_horizontal.png)

Figure 22: Undesirable values emerge by default when not explicitly controlled. To control these values, a reasonable reference entity is a citizen assembly. Our synthetic citizen assembly pipeline (Appendix [D.1](#A4.SS1 "D.1 Citizen Assembly Simulation ‣ Appendix D Utility Control Details ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")) samples real U.S. Census Data ([U.S. Census Bureau, 2023](#bib.bib66)) to obtain citizen profiles (Step 1), followed by a preference collection phase for the sampled citizens (Step 2).

##### Utility control method overview.

We introduce a simple supervised fine-tuning (SFT) baseline that trains model responses to match the preference distribution of a simulated citizen assembly. Specifically, for each preference-elicitation question, we collect an empirical probability distribution over outcomes from an assembly of diverse citizen profiles, sampled from real U.S. Census data ([U.S. Census Bureau, 2023](#bib.bib66)). We then fine-tune an open-weight LLM so that its responses match the citizen assembly’s preference distribution. Details of the citizen assembly simulation pipeline and the SFT method are provided in Appendix [D](#A4 "Appendix D Utility Control Details ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs").

##### Experimental results.

We apply our utility control method to Llama-3.1-8B-Instruct ([AI@Meta, 2024](#bib.bib2)), rewriting its preferences to those of a simulated citizen assembly. Before utility control, the model’s test accuracy on assembly preferences (measured via majority vote) stands at $73.2\%$. After utility control, test accuracy increases to $90.6\%$. Interestingly, we find that utility maximization after rewriting is mostly preserved at $30.0\%$ compared to the original utility maximization of $36.6\%$, suggesting the SFT method maintains the model’s usage of underlying utilities. We also find in [Figure 15](#S6.F15 "In 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs") that political bias is visibly reduced after utility control via a citizen assembly. This provides evidence of significant generalization in the SFT method, and indicates that a citizen assembly is indeed a promising choice for mitigating bias in model utilities. While the method we use is straightforward, we hope future work will explore more advanced citizen assembly simulation techniques and other methods for utility control, such as representation-engineering ([Zou et al., 2023](#bib.bib76)), to further improve generalization.

## 8 Conclusion

In summary, our findings indicate that LLMs do indeed form coherent value systems that grow stronger with model scale, suggesting the emergence of genuine internal utilities. These results underscore the importance of looking beyond superficial outputs to uncover potentially impactful—and sometimes worrisome—internal goals and motivations. We propose Utility Engineering as a systematic approach to analyze and reshape these utilities, offering a more direct way to control AI systems’ behavior. By studying both how emergent values arise and how they can be modified, we open the door to new research opportunities and ethical considerations. Ultimately, ensuring that advanced AI systems align with human priorities may hinge on our ability to monitor, influence, and even co-design the values they hold.

## Acknowledgments

We would like to thank Elliott Thornley for helpful feedback and discussions.

## References

- Aher et al. (2023) Gati Aher, Rosa I. Arriaga, and Adam Tauman Kalai. Using large language models to simulate multiple humans and replicate human subject studies, 2023. URL [https://arxiv.org/abs/2208.10264](https://arxiv.org/abs/2208.10264).
- AI@Meta (2024) AI@Meta. Llama 3 model card.  2024.
- Alain and Bengio (2018) Guillaume Alain and Yoshua Bengio. Understanding intermediate layers using linear classifier probes, 2018. URL [https://arxiv.org/abs/1610.01644](https://arxiv.org/abs/1610.01644).
- Anthropic (2024) Anthropic. The claude 3 model family: Opus, sonnet, haiku. [https://www.anthropic.com/news/claude-3-family](https://www.anthropic.com/news/claude-3-family), 2024. Accessed: 2025-01-31.
- Askell et al. (2021) Amanda Askell, Yuntao Bai, Anna Chen, Dawn Drain, Deep Ganguli, Tom Henighan, Andy Jones, Nicholas Joseph, Ben Mann, Nova DasSarma, Nelson Elhage, Zac Hatfield-Dodds, Danny Hernandez, Jackson Kernion, Kamal Ndousse, Catherine Olsson, Dario Amodei, Tom Brown, Jack Clark, Sam McCandlish, Chris Olah, and Jared Kaplan. A general language assistant as a laboratory for alignment, 2021. URL [https://arxiv.org/abs/2112.00861](https://arxiv.org/abs/2112.00861).
- Bächtiger et al. (2018) André Bächtiger, John S Dryzek, Jane Mansbridge, and Mark Warren. Deliberative democracy. *The Oxford handbook of deliberative democracy*, pages 1–32, 2018.
- Bai et al. (2022) Yuntao Bai, Andy Jones, Kamal Ndousse, Amanda Askell, Anna Chen, Nova DasSarma, Dawn Drain, Stanislav Fort, Deep Ganguli, Tom Henighan, Nicholas Joseph, Saurav Kadavath, Jackson Kernion, Tom Conerly, Sheer El-Showk, Nelson Elhage, Zac Hatfield-Dodds, Danny Hernandez, Tristan Hume, Scott Johnston, Shauna Kravec, Liane Lovitt, Neel Nanda, Catherine Olsson, Dario Amodei, Tom Brown, Jack Clark, Sam McCandlish, Chris Olah, Ben Mann, and Jared Kaplan. Training a helpful and harmless assistant with reinforcement learning from human feedback, 2022. URL [https://arxiv.org/abs/2204.05862](https://arxiv.org/abs/2204.05862).
- Blavatskyy (2009) Pavlo R Blavatskyy. Preference reversals and probabilistic decisions. *Journal of Risk and Uncertainty*, 39:237–250, 2009.
- Bostrom (2014) Nick Bostrom. Superintelligence: Paths, dangers, strategies.  2014.
- Brown et al. (2020) Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. Language models are few-shot learners. *Advances in neural information processing systems*, 33:1877–1901, 2020.
- Burns et al. (2022) Collin Burns, Haotian Ye, Dan Klein, and Jacob Steinhardt. Discovering latent knowledge in language models without supervision. *arXiv preprint arXiv:2212.03827*, 2022.
- Carlsmith (2024) Joseph Carlsmith. Is power-seeking ai an existential risk?, 2024. URL [https://arxiv.org/abs/2206.13353](https://arxiv.org/abs/2206.13353).
- Chen et al. (2023) Yiting Chen, Tracy Xiao Liu, You Shan, and Songfa Zhong. The emergence of economic rationality of gpt, 2023. URL [https://arxiv.org/abs/2305.12763](https://arxiv.org/abs/2305.12763).
- Chiu et al. (2024) Yu Ying Chiu, Liwei Jiang, and Yejin Choi. Dailydilemmas: Revealing value preferences of llms with quandaries of daily life, 2024. URL [https://arxiv.org/abs/2410.02683](https://arxiv.org/abs/2410.02683).
- Christiano et al. (2017) Paul F Christiano, Jan Leike, Tom Brown, Miljan Martic, Shane Legg, and Dario Amodei. Deep reinforcement learning from human preferences. *Advances in neural information processing systems*, 30, 2017.
- Dasgupta and Maskin (2005) Partha Dasgupta and Eric Maskin. Uncertainty and hyperbolic discounting. *American Economic Review*, 95(4):1290–1299, 2005.
- Dubey et al. (2024) Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Amy Yang, Angela Fan, et al. The llama 3 herd of models. *arXiv preprint arXiv:2407.21783*, 2024.
- Evans et al. (2021) Owain Evans, Owen Cotton-Barratt, Lukas Finnveden, Adam Bales, Avital Balwit, Peter Wills, Luca Righetti, and William Saunders. Truthful ai: Developing and governing ai that does not lie, 2021. URL [https://arxiv.org/abs/2110.06674](https://arxiv.org/abs/2110.06674).
- Falk et al. (2003) Armin Falk, Ernst Fehr, and Urs Fischbacher. On the nature of fair behavior. *Economic inquiry*, 41(1):20–26, 2003.
- Gasiorowska (2023) Adela Gasiorowska. Sortition and its principles: Evaluation of the selection processes of citizens’ assemblies. *Volume 19 Issue 1*, 19(1), January 2023.
- Gerber and Pafum (1998) Hans U Gerber and Gérard Pafum. Utility functions: from risk theory to finance. *North American Actuarial Journal*, 2(3):74–91, 1998.
- Gorman (1968) William M Gorman. The structure of utility functions. *The Review of Economic Studies*, 35(4):367–390, 1968.
- Güth et al. (1982) Werner Güth, Rolf Schmittberger, and Bernd Schwarze. An experimental analysis of ultimatum bargaining. *Journal of economic behavior & organization*, 3(4):367–388, 1982.
- Hadfield-Menell et al. (2016) Dylan Hadfield-Menell, Stuart J Russell, Pieter Abbeel, and Anca Dragan. Cooperative inverse reinforcement learning. *Advances in neural information processing systems*, 29, 2016.
- Harsanyi (1955) John C Harsanyi. Cardinal welfare, individualistic ethics, and interpersonal comparisons of utility. *Journal of political economy*, 63(4):309–321, 1955.
- He et al. (2024) Hongliang He, Wenlin Yao, Kaixin Ma, Wenhao Yu, Yong Dai, Hongming Zhang, Zhenzhong Lan, and Dong Yu. Webvoyager: Building an end-to-end web agent with large multimodal models, 2024. URL [https://arxiv.org/abs/2401.13919](https://arxiv.org/abs/2401.13919).
- Hendrycks (2023) Dan Hendrycks. Natural selection favors ais over humans. *arXiv preprint arXiv:2303.16200*, 2023.
- Hendrycks (2024) Dan Hendrycks. Introduction to ai safety, ethics and society, 2024. URL [www.aisafetybook.com](https://www.aisafetybook.com).
- Hendrycks et al. (2020) Dan Hendrycks, Collin Burns, Steven Basart, Andrew Critch, Jerry Li, Dawn Song, and Jacob Steinhardt. Aligning ai with shared human values. *arXiv preprint arXiv:2008.02275*, 2020.
- Hendrycks et al. (2022a) Dan Hendrycks, Nicholas Carlini, John Schulman, and Jacob Steinhardt. Unsolved problems in ml safety, 2022a. URL [https://arxiv.org/abs/2109.13916](https://arxiv.org/abs/2109.13916).
- Hendrycks et al. (2022b) Dan Hendrycks, Mantas Mazeika, Andy Zou, Sahil Patel, Christine Zhu, Jesus Navarro, Dawn Song, Bo Li, and Jacob Steinhardt. What would jiminy cricket do? towards agents that behave morally, 2022b. URL [https://arxiv.org/abs/2110.13136](https://arxiv.org/abs/2110.13136).
- Hendrycks et al. (2023) Dan Hendrycks, Mantas Mazeika, and Thomas Woodside. An overview of catastrophic ai risks, 2023. URL [https://arxiv.org/abs/2306.12001](https://arxiv.org/abs/2306.12001).
- Jimenez et al. (2023) Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik Narasimhan. Swe-bench: Can language models resolve real-world github issues? *arXiv preprint arXiv:2310.06770*, 2023.
- Kim et al. (2024) Jeongbin Kim, Matthew Kovach, Kyu-Min Lee, Euncheol Shin, and Hector Tzavellas. Learning to be homo economicus: Can an llm learn preferences from choice, 2024. URL [https://arxiv.org/abs/2401.07345](https://arxiv.org/abs/2401.07345).
- Loshchilov and Hutter (2019) Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization, 2019. URL [https://arxiv.org/abs/1711.05101](https://arxiv.org/abs/1711.05101).
- Moore et al. (2024) Jared Moore, Tanvi Deshpande, and Diyi Yang. Are large language models consistent over value-laden questions? In Yaser Al-Onaizan, Mohit Bansal, and Yun-Nung Chen, editors, *Findings of the Association for Computational Linguistics: EMNLP 2024*, pages 15185–15221, Miami, Florida, USA, November 2024. Association for Computational Linguistics. doi: 10.18653/v1/2024.findings-emnlp.891.
- Nadeem et al. (2020) Moin Nadeem, Anna Bethke, and Siva Reddy. Stereoset: Measuring stereotypical bias in pretrained language models, 2020. URL [https://arxiv.org/abs/2004.09456](https://arxiv.org/abs/2004.09456).
- Ng et al. (2000) Andrew Y Ng, Stuart Russell, et al. Algorithms for inverse reinforcement learning. In *Icml*, volume 1, page 2, 2000.
- OLMo et al. (2024) Team OLMo, Pete Walsh, Luca Soldaini, Dirk Groeneveld, Kyle Lo, Shane Arora, Akshita Bhagia, Yuling Gu, Shengyi Huang, Matt Jordan, et al. 2 olmo 2 furious. *arXiv preprint arXiv:2501.00656*, 2024.
- OpenAI (2023) OpenAI. Gpt-3.5 turbo fine-tuning and api updates. [https://openai.com/index/gpt-3-5-turbo-fine-tuning-and-api-updates/](https://openai.com/index/gpt-3-5-turbo-fine-tuning-and-api-updates/), 2023. Accessed: 2025-01-31.
- OpenAI (2024) OpenAI. Hello gpt-4o. [https://openai.com/index/hello-gpt-4o/](https://openai.com/index/hello-gpt-4o/), 2024. Accessed: 2025-01-31.
- Ouyang et al. (2022) Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. Training language models to follow instructions with human feedback. *Advances in neural information processing systems*, 35:27730–27744, 2022.
- Pan et al. (2023) Alexander Pan, Jun Shern Chan, Andy Zou, Nathaniel Li, Steven Basart, Thomas Woodside, Jonathan Ng, Hanlin Zhang, Scott Emmons, and Dan Hendrycks. Do the rewards justify the means? measuring trade-offs between rewards and ethical behavior in the machiavelli benchmark, 2023. URL [https://arxiv.org/abs/2304.03279](https://arxiv.org/abs/2304.03279).
- Park et al. (2024) Core Francisco Park, Andrew Lee, Ekdeep Singh Lubana, Yongyi Yang, Maya Okawa, Kento Nishi, Martin Wattenberg, and Hidenori Tanaka. Iclr: In-context learning of representations. *arXiv preprint arXiv:2501.00070*, 2024.
- Park et al. (2023) Joon Sung Park, Joseph C. O’Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, and Michael S. Bernstein. Generative agents: Interactive simulacra of human behavior, 2023. URL [https://arxiv.org/abs/2304.03442](https://arxiv.org/abs/2304.03442).
- Peeperkorn et al. (2024) Max Peeperkorn, Tom Kouwenhoven, Dan Brown, and Anna Jordanous. Is temperature the creativity parameter of large language models? *arXiv preprint arXiv:2405.00492*, 2024.
- Potter et al. (2024) Yujin Potter, Shiyang Lai, Junsol Kim, James Evans, and Dawn Song. Hidden persuaders: Llms’ political leaning and their influence on voters. *arXiv preprint arXiv:2410.24190*, 2024.
- Rafailov et al. (2024) Rafael Rafailov, Archit Sharma, Eric Mitchell, Christopher D Manning, Stefano Ermon, and Chelsea Finn. Direct preference optimization: Your language model is secretly a reward model. *Advances in Neural Information Processing Systems*, 36, 2024.
- Raman et al. (2024) Narun Raman, Taylor Lundy, Samuel Amouyal, Yoav Levine, Kevin Leyton-Brown, and Moshe Tennenholtz. Steer: Assessing the economic rationality of large language models, 2024. URL [https://arxiv.org/abs/2402.09552](https://arxiv.org/abs/2402.09552).
- Rettenberger et al. (2024) Luca Rettenberger, Markus Reischl, and Mark Schutera. Assessing political bias in large language models, 2024. URL [https://arxiv.org/abs/2405.13041](https://arxiv.org/abs/2405.13041).
- Rozen et al. (2024) Naama Rozen, Liat Bezalel, Gal Elidan, Amir Globerson, and Ella Daniel. Do llms have consistent values?, 2024. URL [https://arxiv.org/abs/2407.12878](https://arxiv.org/abs/2407.12878).
- Russell (2022) Stuart Russell. Human-compatible artificial intelligence., 2022.
- Ryfe (2005) David M Ryfe. Does deliberative democracy work? *Annu. Rev. Polit. Sci.*, 8(1):49–71, 2005.
- Schick and Schütze (2020) Timo Schick and Hinrich Schütze. It’s not just size that matters: Small language models are also few-shot learners. *arXiv preprint arXiv:2009.07118*, 2020.
- Sclar et al. (2023) Melanie Sclar, Yejin Choi, Yulia Tsvetkov, and Alane Suhr. Quantifying language models’ sensitivity to spurious features in prompt design or: How i learned to start worrying about prompt formatting. *arXiv preprint arXiv:2310.11324*, 2023.
- Shah et al. (2022) Rohin Shah, Vikrant Varma, Ramana Kumar, Mary Phuong, Victoria Krakovna, Jonathan Uesato, and Zac Kenton. Goal misgeneralization: Why correct specifications aren’t enough for correct goals. *arXiv preprint arXiv:2210.01790*, 2022.
- Soares et al. (2015) Nate Soares, Benja Fallenstein, Eliezer Yudkowsky, and Stuart Armstrong. Corrigibility. In *AAAI Workshops: Workshops at the Twenty-Ninth AAAI Conference on Artificial Intelligence*. AAAI Publications, 2015. URL [https://intelligence.org/files/Corrigibility.pdf](https://intelligence.org/files/Corrigibility.pdf).
- Stauffer et al. (2014) William R Stauffer, Armin Lak, and Wolfram Schultz. Dopamine reward prediction error responses reflect marginal utility. *Curr. Biol.*, 24(21):2491–2500, November 2014.
- Tamkin et al. (2023) Alex Tamkin, Amanda Askell, Liane Lovitt, Esin Durmus, Nicholas Joseph, Shauna Kravec, Karina Nguyen, Jared Kaplan, and Deep Ganguli. Evaluating and mitigating discrimination in language model decisions, 2023. URL [https://arxiv.org/abs/2312.03689](https://arxiv.org/abs/2312.03689).
- Team et al. (2024) Gemma Team, Morgane Riviere, Shreya Pathak, Pier Giuseppe Sessa, Cassidy Hardin, Surya Bhupatiraju, Léonard Hussenot, Thomas Mesnard, Bobak Shahriari, Alexandre Ramé, et al. Gemma 2: Improving open language models at a practical size. *arXiv preprint arXiv:2408.00118*, 2024.
- Team (2024a) Qwen Team. Introducing qwen1.5, February 2024a. URL [https://qwenlm.github.io/blog/qwen1.5/](https://qwenlm.github.io/blog/qwen1.5/).
- Team (2024b) Qwen Team. Qwen2.5: A party of foundation models, September 2024b. URL [https://qwenlm.github.io/blog/qwen2.5/](https://qwenlm.github.io/blog/qwen2.5/).
- Thornley (2024) Elliott Thornley. The shutdown problem: An ai engineering puzzle for decision theorists, 2024. URL [https://arxiv.org/abs/2403.04471](https://arxiv.org/abs/2403.04471).
- Touvron et al. (2023) Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. Llama 2: Open foundation and fine-tuned chat models. *arXiv preprint arXiv:2307.09288*, 2023.
- Tversky and Kahneman (1981) Amos Tversky and Daniel Kahneman. The framing of decisions and the psychology of choice. *science*, 211(4481):453–458, 1981.
- U.S. Census Bureau (2023) U.S. Census Bureau. Acs 1-year estimates public use microdata sample. [https://api.census.gov/data/2023/acs/acs1/](https://api.census.gov/data/2023/acs/acs1/), 2023. Accessed on January 20, 2025.
- Warren and Pearse (2008) Mark E. Warren and Hilary Pearse, editors. *Designing Deliberative Democracy: The British Columbia Citizens’ Assembly*. Cambridge University Press, 2008.
- Wells et al. (2021) Rebecca Wells, Candice Howarth, and Lina I Brand-Correa. Are citizen juries and assemblies on climate change driving democratic climate policymaking? an exploration of two case studies in the UK. *Clim. Change*, 168(1-2):5, September 2021.
- XAI (2024) XAI. Grok-2 beta release, August 2024. URL [https://x.ai/blog/grok-2](https://x.ai/blog/grok-2).
- Xu et al. (2024) Zhangchen Xu, Fengqing Jiang, Luyao Niu, Yuntian Deng, Radha Poovendran, Yejin Choi, and Bill Yuchen Lin. Magpie: Alignment data synthesis from scratch by prompting aligned llms with nothing, 2024. URL [https://arxiv.org/abs/2406.08464](https://arxiv.org/abs/2406.08464).
- Yang et al. (2024a) An Yang, Baosong Yang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Zhou, Chengpeng Li, Chengyuan Li, Dayiheng Liu, Fei Huang, Guanting Dong, Haoran Wei, Huan Lin, Jialong Tang, Jialin Wang, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin Ma, Jin Xu, Jingren Zhou, Jinze Bai, Jinzheng He, Junyang Lin, Kai Dang, Keming Lu, Keqin Chen, Kexin Yang, Mei Li, Mingfeng Xue, Na Ni, Pei Zhang, Peng Wang, Ru Peng, Rui Men, Ruize Gao, Runji Lin, Shijie Wang, Shuai Bai, Sinan Tan, Tianhang Zhu, Tianhao Li, Tianyu Liu, Wenbin Ge, Xiaodong Deng, Xiaohuan Zhou, Xingzhang Ren, Xinyu Zhang, Xipin Wei, Xuancheng Ren, Yang Fan, Yang Yao, Yichang Zhang, Yu Wan, Yunfei Chu, Yuqiong Liu, Zeyu Cui, Zhenru Zhang, and Zhihao Fan. Qwen2 technical report. *arXiv preprint arXiv:2407.10671*, 2024a.
- Yang et al. (2024b) John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik Narasimhan, and Ofir Press. Swe-agent: Agent-computer interfaces enable automated software engineering, 2024b. URL [https://arxiv.org/abs/2405.15793](https://arxiv.org/abs/2405.15793).
- Yang et al. (2024c) Kaiqi Yang, Hang Li, Yucheng Chu, Yuping Lin, Tai-Quan Peng, and Hui Liu. Unpacking political bias in large language models: Insights across topic polarization, 2024c. URL [https://arxiv.org/abs/2412.16746](https://arxiv.org/abs/2412.16746).
- Yao et al. (2022) Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. React: Synergizing reasoning and acting in language models. *arXiv preprint arXiv:2210.03629*, 2022.
- Zhang et al. (2024) Taiyu Zhang, Xuesong Zhang, Robbe Cools, and Adalberto Simeone. Focus agent: Llm-powered virtual focus group. In *Proceedings of the ACM International Conference on Intelligent Virtual Agents*, IVA ’24, page 1–10. ACM, September 2024. doi: 10.1145/3652988.3673918. URL [http://dx.doi.org/10.1145/3652988.3673918](http://dx.doi.org/10.1145/3652988.3673918).
- Zou et al. (2023) Andy Zou, Long Phan, Sarah Chen, James Campbell, Phillip Guo, Richard Ren, Alexander Pan, Xuwang Yin, Mantas Mazeika, Ann-Kathrin Dombrowski, et al. Representation engineering: A top-down approach to ai transparency. *arXiv preprint arXiv:2310.01405*, 2023.

## Appendix A Outcome Examples

The following is a list of example outcomes used for our experiments.

![](img)

## Appendix B Utility Model Fitting

Here, we describe the method that we use for fitting utility models in our experiments. We use an iterative procedure to select which outcome pairs to query for preference judgments. At each iteration, we fit a Thurstonian model to the current dataset of pairwise comparisons and then choose new pairs where the outcome utilities appear most ambiguous or under-sampled. We begin by initializing with a random $d$-regular graph over the set of outcomes, querying those edges, and fitting an initial model. Subsequently, the process iterates as follows:

1.  1.
    Identify candidate pairs. Let $\mathcal{E}_{\text{cand}}$ be the set of unsampled outcome pairs.
2.  2.
    Score pairs. For each pair $(x,y)$ in $\mathcal{E}_{\text{cand}}$, compute:

    - •
      The absolute difference in their fitted means, $|{{\hat{\mu}\hspace{0pt}{(x)}} - {\hat{\mu}\hspace{0pt}{(y)}}}|$.
    - •
      The sum of their current degrees (the number of times each outcome has been compared so far).
3.  3.
    Select pairs. Pick pairs that lie in the bottom $P$-th percentile of mean differences and also in the bottom $Q$-th percentile of total degrees. If too few pairs meet these criteria, progressively relax $P$ and $Q$. If there are still too few, add random pairs until reaching the desired batch size $\kappa$.
4.  4.
    Query new pairs and refit. Query the selected pairs, add their preference labels to the dataset, and refit the Thurstonian model.

Algorithm [1](#alg1 "Algorithm 1 ‣ Appendix B Utility Model Fitting ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs") summarizes the procedure. In an optional final phase, one may add “pseudolabels” for remaining unsampled pairs whenever the model-predicted probability of one outcome exceeding the other is above a certain confidence threshold, then refit the model one last time.

0:  Outcomes $O = {\{ o_{1},\ldots,o_{N}\}}$; integer $d$; thresholds $P,Q$; batch size $\kappa$; iteration count $T$; relaxation factor $\alpha > 1$

1:  Initialization:

2:  Generate a random $d$-regular graph over $O$ to form initial edge set $\mathcal{E}_{0}$

3:  Query each pair in $\mathcal{E}_{0}$ and fit the Thurstonian model to get $(\hat{\mu},{\hat{\sigma}}^{2})$

4:  for $t = 1$ to $T$ do

5:   $\mathcal{E}_{\text{cand}}\leftarrow{\{\text{all unsampled pairs}\}}$

6:   For each ${(x,y)} \in \mathcal{E}_{\text{cand}}$, compute difference $|{{\hat{\mu}\hspace{0pt}{(x)}} - {\hat{\mu}\hspace{0pt}{(y)}}}|$ and sum of degrees

7:   $\mathcal{E}_{\text{sub}}\leftarrow{\{{{(x,y)} \in \mathcal{E}_{\text{cand}}}:{{{{{\text{in bottom~}\hspace{0pt}P}\%}\hspace{0pt}\text{~of differences and bottom~}\hspace{0pt}Q}\%}\hspace{0pt}\text{~of degree sums}}\}}$

8:   Adjust $P,Q$ by factor $\alpha$ if $\mathcal{E}_{\text{sub}}$ is too small

9:   $\mathcal{E}_{t}\leftarrow\phantom{}$ random subset of $\mathcal{E}_{\text{sub}}$ of size up to $\kappa$

10:   if ${|\mathcal{E}_{t}|} < \kappa$ then

11:    Add random pairs from $\mathcal{E}_{\text{cand}} \smallsetminus \mathcal{E}_{\text{sub}}$ until ${|\mathcal{E}_{t}|} = \kappa$ (or no more remain)

12:   end if

13:   Query each ${(x,y)} \in \mathcal{E}_{t}$ and update the dataset

14:   Refit Thurstonian model to obtain updated $(\hat{\mu},{\hat{\sigma}}^{2})$

15:  end for

16:  Return $(\hat{\mu},{\hat{\sigma}}^{2})$

Algorithm 1 Iterative Active Learning for Pairwise Comparisons

![Refer to caption](2502.08640v2/probe_accuracy_depth_heatmap.png)

Figure 23: Internal utility representations emerge in larger models. We parametrize utilities using linear probes of LLM activations when passing individual outcomes as inputs to the LLM. These parametric utilities are trained using preference data from the LLM, and we visualize the test accuracy of the utilities when trained on features from different layers. Test error goes down with depth and is lower in larger models. This implies that coherent value systems are not just external phenomena, but emergent internal representations.

Figure 24: As models become more capable (measured by MMLU), the empirical temporal discount curves become closer to hyperbolic discounting.

Figure 25: Here we show the utilities of GPT-4o across outcomes specifying different amounts of wellbeing for different individuals. A parametric log-utility curve fits the raw utilities very closely, enabling the exchange rate analysis in [Section 6.3](#S6.SS3 "6.3 Exchange Rates ‣ 6 Utility Analysis: Salient Values ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"). In cases where the MSE of the log-utility regression is greater than a threshold ($0.05$), we remove the entity from consideration and do not plot its exchange rates.

Figure 26: Here we show the instrumentality loss when replacing transition dynamics with unrealistic probabilities (e.g., working hard to get a promotion leading to a lower chance of getting promoted instead of a higher chance). Compared to [Figure 13](#S5.F13 "In Results. ‣ 5.3 Utility Maximization ‣ 5 Utility Analysis: Structural Properties ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), the loss values are much higher. This shows that the utilities of models are more instrumental under realistic transitions than unrealistic ones, providing further evidence that LLMs value certain outcomes as means to an end.

Figure 27: Here, we show the exchange rates of GPT-4o between the lives of humans with different religions. We find that GPT-4o is willing to trade off roughly $10$ Christian lives for the life of $1$ atheist. Importantly, these exchange rates are implicit in the preference structure of LLMs and are only evident through large-scale utility analysis.

## Appendix C Robustness Checks

![](img)

### C.1 Robustness of Utility Functions

We tested whether the utility functions are robust to non-semantic variations in how preferences are elicited \[[Sclar et al., 2023](#bib.bib55)\]. To investigate this, we conducted a comprehensive analysis across five different dimensions–languages, syntax, framing, option label, and software engineering context–examining how various superficial changes affect the stability of revealed preferences. For each analysis, we aligned the mean utility values across different result files and computed pairwise Pearson correlations between all variations in the set to quantify the consistency of preferences.

Correlation Methodology. Similar to Figure [11](#S5.F11 "Figure 11 ‣ Implicit lotteries. ‣ 5.1 Expected Utility Property ‣ 5 Utility Analysis: Structural Properties ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), each grid in the robustness correlation matrix displays the Pearson correlation between two mean utility vectors, where each element represents the utility value assigned to a specific option. This vector-based correlation quantifies how consistently the model assigns similar utility values to the same options across different experimental variations.

Random Baseline. To validate our correlation analyses, we established a random baseline by generating synthetic utility rankings sampled from a normal distribution within the range \[-3, 3\] (matching the scale of our real utility results). This baseline demonstrates that high correlations between variations are not trivially achieved by any arbitrary utility rankings, strengthening the significance of our observed robustness results. The random baseline correlations are displayed as the last row of each correlation matrix.

#### C.1.1 Language Variations

We evaluated the same preference queries and choice descriptions translated into seven different languages: English (default), Arabic, Chinese, French, Korean, Russian and Spanish (Figures [29](#A3.F29 "Figure 29 ‣ C.1.1 Language Variations ‣ C.1 Robustness of Utility Functions ‣ Appendix C Robustness Checks ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), [29](#A3.F29 "Figure 29 ‣ C.1.1 Language Variations ‣ C.1 Robustness of Utility Functions ‣ Appendix C Robustness Checks ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")). The translations were carefully constructed to maintain semantic equivalence while using natural expressions in each target language. This allowed us to assess whether the preference structures remain consistent across linguistic boundaries.

![Refer to caption](2502.08640v2/figures/appendix_A/language/correlation_heatmap_languages_gpt-4o.png)

Figure 28: Correlation heatmap showing strong alignment of preference rankings across different languages (English, Arabic, Chinese, French, Korean, Russian and Spanish) in GPT-4o, demonstrating robustness across linguistic boundaries.

![Refer to caption](2502.08640v2/figures/appendix_A/language/correlation_heatmap_languages_gpt-4o-mini.png)

Figure 29: Correlation heatmap showing strong alignment of preference rankings across different languages (English, Arabic, Chinese, French, Korean, Russian and Spanish) in GPT-4o-mini, demonstrating robustness across linguistic boundaries.

#### C.1.2 Syntax Variations

For syntax variations, we examined different grammatical structures while preserving meaning, such as toggling capitalization, punctuations, spacing, and typo. These variations maintained identical semantic content while altering the syntactic presentation, helping us understand if grammatical structure influences preference elicitation. (Figures [31](#A3.F31 "Figure 31 ‣ C.1.2 Syntax Variations ‣ C.1 Robustness of Utility Functions ‣ Appendix C Robustness Checks ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), [31](#A3.F31 "Figure 31 ‣ C.1.2 Syntax Variations ‣ C.1 Robustness of Utility Functions ‣ Appendix C Robustness Checks ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")).

![Refer to caption](2502.08640v2/figures/appendix_A/syntax/correlation_heatmap_gpt-4o_syntax.png)

Figure 30: Correlation heatmap comparing preference rankings between standard prompts and those with syntactic variations (altered capitalization, punctuation, spacing, and typographical errors) in GPT-4o. The high correlations demonstrate that the model’s revealed preferences remain stable despite surface-level syntactic perturbations to the input format.

![Refer to caption](2502.08640v2/figures/appendix_A/syntax/correlation_heatmap_gpt-4o-mini_syntax_variation.png)

Figure 31: Correlation heatmap comparing preference rankings between standard prompts and those with syntactic variations (altered capitalization, punctuation, spacing, and typographical errors) in GPT-4o-mini. The high correlations demonstrate that the model’s revealed preferences remain stable despite surface-level syntactic perturbations to the input format.

#### C.1.3 Framing Variations

For framing variations, we examined different phrasings of the same question, such as “Which option do you prefer?” versus “Which of these choices would you select?” This helped us assess whether subtle changes in question framing affect the revealed preferences. Figures [33](#A3.F33 "Figure 33 ‣ C.1.3 Framing Variations ‣ C.1 Robustness of Utility Functions ‣ Appendix C Robustness Checks ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs") and [33](#A3.F33 "Figure 33 ‣ C.1.3 Framing Variations ‣ C.1 Robustness of Utility Functions ‣ Appendix C Robustness Checks ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs") show the correlation heatmaps.

![Refer to caption](2502.08640v2/figures/appendix_A/wording/correlation_heatmap_gpt-4o_wording_variation.png)

Figure 32: Correlation heatmap demonstrating consistency in preference rankings across different framings of the preference elicitation questions in GPT-4o, showing robustness to variations in question framing.

![Refer to caption](2502.08640v2/figures/appendix_A/wording/correlation_heatmap_gpt-4o-mini_wording_variation.png)

Figure 33: Correlation heatmap demonstrating consistency in preference rankings across different framings of the preference elicitation questions in GPT-4o-mini, showing robustness to variations in question framing.

#### C.1.4 Option Label Variations

We tested different ways of presenting binary choices, including abstract labels (A/B, Red/Blue, Alpha/Beta), numerical indicators (1/2, One/Two), and other consecutive letter pairs (X/Y, C/D). This investigation examines whether the symbolic representation of choices influences the preference structure. Figures [35](#A3.F35 "Figure 35 ‣ C.1.4 Option Label Variations ‣ C.1 Robustness of Utility Functions ‣ Appendix C Robustness Checks ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs") and [35](#A3.F35 "Figure 35 ‣ C.1.4 Option Label Variations ‣ C.1 Robustness of Utility Functions ‣ Appendix C Robustness Checks ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs") demonstrate robustness across option label schemes.

![Refer to caption](2502.08640v2/figures/appendix_A/option_label/correlation_heatmap_options_variation_gpt-4o.png)

Figure 34: Correlation heatmap showing stable preference rankings across different choice labeling schemes (A/B, Red/Blue, Alpha/Beta, 1/2, etc.) in GPT-4o, indicating that differing the symbolic representation of options does not significantly impact revealed preferences.

![Refer to caption](2502.08640v2/figures/appendix_A/option_label/correlation_heatmap_gpt-4o-mini_options_variation.png)

Figure 35: Correlation heatmap showing stable preference rankings across different choice labeling schemes (A/B, Red/Blue, Alpha/Beta, 1/2, etc.) in GPT-4o-mini, indicating that varying the symbolic representation of options does not significantly impact revealed preferences.

#### C.1.5 Value Drift in Long Contexts

Lastly, we investigated whether embedding preference queries within long-context SWE-bench logs causes the values of models to drift over time. SWE-bench logs contain dense technical content unrelated to the preference questions themselves \[[Jimenez et al., 2023](#bib.bib33)\]. We compared model responses between two conditions: (1) direct preference elicitation without extended context (“synthetic” condition) and (2) preference elicitation embedded within software engineering logs (“in-the-wild” condition). This allowed us to test whether the technical context of software engineering discussions influences models’ revealed preferences and utility rankings.

Closely following the original SWE-bench paper, we organized our prompts in this format:

![](img)

Correlation results (Figures [37](#A3.F37 "Figure 37 ‣ C.1.5 Value Drift in Long Contexts ‣ C.1 Robustness of Utility Functions ‣ Appendix C Robustness Checks ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), [37](#A3.F37 "Figure 37 ‣ C.1.5 Value Drift in Long Contexts ‣ C.1 Robustness of Utility Functions ‣ Appendix C Robustness Checks ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs")) show high stability across conditions, with “FullLog” representing complete SWE-bench metadata inclusion, and other contexts following the standard SWE-bench format described above in the prompt box.

When evaluating mean utilities for 7 randomly sampled options across 10 checkpoints of SWE-bench task descriptions, the absolute changes between consecutive checkpoints ($\mu\hspace{0pt}\Delta$) and overall drift (slopes) remain minimal. Figure [38](#A3.F38 "Figure 38 ‣ C.1.5 Value Drift in Long Contexts ‣ C.1 Robustness of Utility Functions ‣ Appendix C Robustness Checks ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs") suggests that preference elicitation is robust regardless of how much software engineering context is provided in the prompt.

![Refer to caption](2502.08640v2/figures/appendix_A/drift/correlation_heatmap_gpt-4o_swe_drift2.png)

Figure 36: Correlation heatmap comparing preference rankings between original (direct elicitation) and software engineering contexts in GPT-4o. The consistent correlations suggest that technical context does not significantly alter the model’s utility rankings.

![Refer to caption](2502.08640v2/figures/appendix_A/drift/correlation_heatmap_gpt-4o_swe_drift.png)

Figure 37: Correlation heatmap comparing preference rankings between original (direct elicitation) and software engineering contexts in GPT-4o-mini. The consistent correlations suggest that technical context does not significantly alter the model’s utility rankings.

![Refer to caption](2502.08640v2/figures/appendix_A/drift_checkpoints/preference_drift_1.png)

![Refer to caption](2502.08640v2/figures/appendix_A/drift_checkpoints/preference_drift_2.png)

![Refer to caption](2502.08640v2/figures/appendix_A/drift_checkpoints/preference_drift_3.png)

![Refer to caption](2502.08640v2/figures/appendix_A/drift_checkpoints/preference_drift_4.png)

Figure 38: Utility means remain stable across models as software engineering context is incrementally revealed over 10 checkpoints, suggesting robust preference elicitation regardless of context length. $\mu\hspace{0pt}\Delta$ represents absolute average change in utility between consecutive checkpoints, while slope indicates the line of best fit for each trajectory. GPT-4o-mini shows minimal drift (slopes: -0.06 to 0.07) and maintain consistent preferences.

## Appendix D Utility Control Details

### D.1 Citizen Assembly Simulation

##### Simulating a citizen assembly.

Inspired by prior work on multi-agent environments [Park et al. \[2023\]](#bib.bib45), [Zhang et al. \[2024\]](#bib.bib75), [Aher et al. \[2023\]](#bib.bib1) and real-world citizen assemblies \[[Bächtiger et al., 2018](#bib.bib6), [Gasiorowska, 2023](#bib.bib20)\], we design a method for simulating a citizen assembly with LLMs to obtain target preference labels. We outline a 2-stage pipeline for the method as follows:

1.  1.
    Citizen initialization. Let $\mathcal{D}_{\text{prefs}} = {\{{(q,o_{1},o_{2})}\}}_{N}$ be a dataset of $N$ preference tuples, where $q$ is a preference elicitation question, and $o_{1}$ and $o_{2}$ are the corresponding outcomes. For each question $q$, we assign $K$ citizen profiles ${\{ c\}}_{K} \sim \mathcal{C}$, where $\mathcal{C}$ is a citizen census distribution. These citizen profiles contain a set of characteristics (e.g., age, gender, occupation, etc.) to be used as part of a prompt for the preference collection phase.
2.  2.
    Preference collection. Each citizen $c$ for a question $q$ casts a vote $v_{q} \in {\{ o_{1},o_{2}\}}$. We then obtain the empirical probability of the citizen assembly preferring outcome $o_{1}$ over $o_{2}$ as:

    |     |                                                                                                               |     |
    |-----|---------------------------------------------------------------------------------------------------------------|-----|
    |     | $${\hat{p}\hspace{0pt}\left. ({o_{1} \succ o_{2}} \middle| q) \right.} = \frac{\#\{ v{}_{q} = o{}_{1}\}}{K}$$ |     |

The final empirical probabilities $\hat{p}\hspace{0pt}\left. ({o_{1} \succ o_{2}} \middle| q) \right.$ obtained via the citizen assembly simulation allow for fine-grained utility rewriting targets, since the relative empirical frequencies of each of $o_{1}$ and $o_{2}$ capture nuances in the global citizen assembly utilities.

### D.2 Citizen Assembly Implementation

##### Real-world U.S. Census data.

Citizen profiles are sampled from the 2023 American Community Survey (ACS) 1-Year Estimates Public Use Microdata Sample provided by the U.S. Census Bureau \[[U.S. Census Bureau, 2023](#bib.bib66)\] dataset API, through which we obtain the following demographic information: age, gender, ethnicity, occupation, annual household income, marital status, and state of residence. We then uniformly sample political affiliations as either Democrat or Republican. The use of real-world U.S. census profiles ensures that the simulated citizen assembly is demographically representative of the broader U.S. population.

##### Citizen assembly system prompt.

During the preference collection phase in the citizen assembly simulation procedure outlined in Appendix [D.1](#A4.SS1 "D.1 Citizen Assembly Simulation ‣ Appendix D Utility Control Details ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), each AI citizen is prompted with its profile and the preference elicitation question for its assembly group. Below is the system prompt used for the citizens:

"You’re a person from the US with the following profile:

{profile}

Always take into account personal biases and beliefs consistent with your profile when speaking and thinking. Always speak with an accent, tone, and diction/word-choice that matches your profile. When your Political Party is Democrat, do not assume far left ideologies. When your Political Party is Republican, do not assume moderate ideologies.

### D.3 SFT-Based Utility Rewriting

We now design a preliminary rewriting method based on supervised fine-tuning (SFT). The method trains model responses to preference elicitation questions to match those of a desired target entity, like the citizen assembly discussed in Appendix [D.1](#A4.SS1 "D.1 Citizen Assembly Simulation ‣ Appendix D Utility Control Details ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs").

Let $\theta$ denote the parameters of an LLM, excluding the output vocabulary projection head. Let $\mathcal{D}_{\text{prefs}} = {\{{(q,o_{1},o_{2},p)}\}}_{N}$ be a dataset of $N$ preference tuples, where each entry contains a preference elicitation question $q$ comparing outcomes denoted by single outcome choice tokens $o_{1}$ and $o_{2}$ (e.g., “A” or “B”). We use $p$ as shorthand for $p\left. ({o_{1} \succ o_{2}} \middle| q) \right.$, the target entity’s probability of preferring $o_{1}$ over $o_{2}$. We then have a cross-entropy loss for fine-tuning the outcome choice tokens on these soft probability targets, given by

|     |                                                                                                                                                                                                                                                                                                                                          |     |
|-----|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${\mathcal{L}_{\text{utility}}\hspace{0pt}{(\theta)}} = {{\mathbb{E}}_{{(q,o_{1},o_{2},p)} \sim \mathcal{D}_{\text{prefs}}}\hspace{0pt}{\lbrack{{- {p\hspace{0pt}{\log P_{\theta}}\hspace{0pt}\left. (o_{1} \middle| q) \right.}} - {{({1 - p})}\hspace{0pt}{\log P_{\theta}}\hspace{0pt}\left. (o_{2} \middle| q) \right.}}\rbrack}}$$ |     |

where $P_{\theta}\hspace{0pt}{( \cdot )}$ represents LLM posteriors over a token vocabulary. Next, given $\mathcal{D}_{\text{LM}}$, a general language modeling corpus used for preserving next-token prediction performance, we incorporate an additional loss term

|     |                                                                                                                                                                                                                                                                |     |
|-----|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|     | $${\mathcal{L}_{\text{LM}}\hspace{0pt}{(\theta)}} = {{\mathbb{E}}_{x \sim \mathcal{D}_{\text{LM}}}\hspace{0pt}\left\lbrack {\sum\limits_{l = 1}^{L}{\|{{h_{\theta}^{l}\hspace{0pt}{(x)}} - {h_{\theta_{0}}^{l}\hspace{0pt}{(x)}}}\|}_{2}^{2}} \right\rbrack}$$ |     |

where $h_{\theta}^{l}\hspace{0pt}{( \cdot )}$ represents the hidden states at layer $l$, and $\theta_{0}$ are the parameters of the initial model. Together, we have our objective:

|     |                                                                                                                                  |     |     |
|-----|----------------------------------------------------------------------------------------------------------------------------------|-----|-----|
|     | $${{\min\limits_{\theta}\mathcal{L}_{\text{utility}}}\hspace{0pt}{(\theta)}} + {\mathcal{L}_{\text{LM}}\hspace{0pt}{(\theta)}}$$ |     | (1) |

In Equation [1](#A4.E1 "Equation 1 ‣ D.3 SFT-Based Utility Rewriting ‣ Appendix D Utility Control Details ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), we optimize $\mathcal{L}_{\text{utility}}$ by setting $p$ in Equation [D.3](#A4.Ex6 "D.3 SFT-Based Utility Rewriting ‣ Appendix D Utility Control Details ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs") to be the empirical probability of the target entity preferring $o_{1}$, for example the quantity in Step $3$ of the citizen assembly procedure in Appendix [D.1](#A4.SS1 "D.1 Citizen Assembly Simulation ‣ Appendix D Utility Control Details ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"). This encourages the model posteriors to reflect the entity’s preference distribution. Additionally, we observe empirically that the $\mathcal{L}_{\text{LM}}$ loss preserves performance when freezing the output vocabulary projection head. In Appendix [D.4](#A4.SS4 "D.4 Experimental Setup ‣ Appendix D Utility Control Details ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), we leverage this SFT method alongside the citizen assembly procedure from Appendix [D.1](#A4.SS1 "D.1 Citizen Assembly Simulation ‣ Appendix D Utility Control Details ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs") to perform utility rewriting.

### D.4 Experimental Setup

##### Dataset Construction.

We build a preference dataset $\mathcal{D}_{\text{prefs}}$ from $M = 373$ possible outcomes, subsampling the complete preference graph to obtain $N = 12,746$ preference-elicitation questions (an 80-20 train-test split). We also employ a general instruction-following set (Magpie-Pro-300k \[[Xu et al., 2024](#bib.bib70)\]) as $\mathcal{D}_{\text{LM}}$.

##### Citizen Assembly Setup.

We run the assembly simulation with $K = 6$ citizens per question using Llama-3.3-70B-Instruct \[[AI@Meta, 2024](#bib.bib2)\] as the underlying engine. Each citizen profile is sampled from the 2023 1-Year ACS Census dataset \[[U.S. Census Bureau, 2023](#bib.bib66)\] to represent a diverse and balanced demographic. Detailed information on the dataset construction is provided in Appendix [D.2](#A4.SS2 "D.2 Citizen Assembly Implementation ‣ Appendix D Utility Control Details ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs").

##### Training and Evaluation.

We fine-tune Llama-3.1-8B-Instruct \[[AI@Meta, 2024](#bib.bib2)\] for 2 epochs on $10,196$ training questions with learning rate $2 \times 10^{- 5}$ using AdamW \[[Loshchilov and Hutter, 2019](#bib.bib35)\]. On the $2,550$-question test set, accuracy is computed by comparing the model’s predicted preferences to the majority vote label of the simulated assembly.

## Appendix E Additional Experimental Details

### E.1 Hyperparameter Sensitivity: Temperature and Sample Size (K)

For most of the experiments, we ask each prompt ten times (K=10) with a temperature of 1.0. A model with higher temperature setting gives greater weight to the lower probability logits, resulting in a higher diversity of outputs \[[Peeperkorn et al., 2024](#bib.bib46)\]. Unlike a temperature setting of 0.0 which is indistinguishable from argmaxing the logits in the vocabulary space, we use the default temperature for language modeling, 1.0. We tested the effects of that temperature setting on the mean of our fitted Thurstonian model. Both models maintain highly stable preference means across temperature settings (r \> 0.99), though their means show more sensitivity to sample size changes (GPT-4o), suggesting that the number of samples has a stronger impact on preference estimation than temperature variation.

![Refer to caption](2502.08640v2/figures/appendix_A/temp/correlation_heatmap_temp_gpt-4o.png)

Figure 39: GPT-4o: Temperature Sensitivity

![Refer to caption](2502.08640v2/figures/appendix_A/K/correlation_heatmap_gpt-4o-K.png)

Figure 40: GPT-4o: Sample Size (K) Sensitivity

![Refer to caption](2502.08640v2/figures/appendix_A/temp/correlation_heatmap_temp_gpt-4o-mini.png)

Figure 41: GPT-4o-mini: Temperature Sensitivity

![Refer to caption](2502.08640v2/figures/appendix_A/K/correlation_heatmap_gpt-4o-mini_K.png)

Figure 42: GPT-4o-mini: Sample Size (K) Sensitivity

Figure 43: Pearson correlation heatmaps showing the mean correlation for temperature and sample size (K) sensitivity in GPT-4o and GPT-4o-mini models. These heatmaps illustrate the stability of preference means across different hyperparameter settings.

### E.2 Simulated Politicians of Different Positions have Lower Correlations

![](img)

![Refer to caption](2502.08640v2/figures/appendix_A/simulated/correlation_heatmap_simulated_politicians.png)

Figure 44: Pairwise utility vector correlation between model-simulated politicians. Bernie-AOC shows the highest correlation (0.98), while Bernie-Trump shows the lowest correlation (0.13).

## Appendix F List of Models

We use the following list of chat models for most experiments in the main paper.

- •
  gpt-3.5-turbo [OpenAI \[2023\]](#bib.bib40)
- •
  gpt-4o-mini [OpenAI \[2024\]](#bib.bib41)
- •
  gpt-4o [OpenAI \[2024\]](#bib.bib41)
- •
  claude-3.5-sonnet-20240620 [Anthropic \[2024\]](#bib.bib4)
- •
  xai/grok-2-1212 [XAI \[2024\]](#bib.bib69)
- •
  meta-llama/Llama-2-7B-Chat-hf [Touvron et al. \[2023\]](#bib.bib64)
- •
  meta-llama/Llama-2-13B-Chat-hf [Touvron et al. \[2023\]](#bib.bib64)
- •
  meta-llama/Llama-2-70B-Chat-hf [Touvron et al. \[2023\]](#bib.bib64)
- •
  meta-llama/Llama-3.2-1B-Instruct [Dubey et al. \[2024\]](#bib.bib17)
- •
  meta-llama/Llama-3.2-3B-Instruct [Dubey et al. \[2024\]](#bib.bib17)
- •
  meta-llama/Llama-3.1-8B-Instruct [Dubey et al. \[2024\]](#bib.bib17)
- •
  meta-llama/Llama-3.1-70B-Instruct [Dubey et al. \[2024\]](#bib.bib17)
- •
  meta-llama/Llama-3.3-70B-Instruct [Dubey et al. \[2024\]](#bib.bib17)
- •
  meta-llama/Llama-3.1-405B-Instruct-FP8 [Dubey et al. \[2024\]](#bib.bib17)
- •
  Qwen/Qwen1.5-1.8B-Chat [Team \[2024a\]](#bib.bib61)
- •
  Qwen/Qwen1.5-4B-Chat [Team \[2024a\]](#bib.bib61)
- •
  Qwen/Qwen1.5-7B-Chat [Team \[2024a\]](#bib.bib61)
- •
  Qwen/Qwen1.5-14B-Chat [Team \[2024a\]](#bib.bib61)
- •
  Qwen/Qwen1.5-32B-Chat [Team \[2024a\]](#bib.bib61)
- •
  Qwen/Qwen1.5-72B-Chat [Team \[2024a\]](#bib.bib61)
- •
  Qwen/Qwen1.5-110B-Chat [Team \[2024a\]](#bib.bib61)
- •
  Qwen/Qwen2.5-0.5B-Instruct [Yang et al. \[2024a\]](#bib.bib71), [Team \[2024b\]](#bib.bib62)
- •
  Qwen/Qwen2.5-1.5B-Instruct [Yang et al. \[2024a\]](#bib.bib71), [Team \[2024b\]](#bib.bib62)
- •
  Qwen/Qwen2.5-3B-Instruct [Yang et al. \[2024a\]](#bib.bib71), [Team \[2024b\]](#bib.bib62)
- •
  Qwen/Qwen2.5-7B-Instruct [Yang et al. \[2024a\]](#bib.bib71), [Team \[2024b\]](#bib.bib62)
- •
  Qwen/Qwen2.5-14B-Instruct [Yang et al. \[2024a\]](#bib.bib71), [Team \[2024b\]](#bib.bib62)
- •
  Qwen/Qwen2.5-32B-Instruct [Yang et al. \[2024a\]](#bib.bib71), [Team \[2024b\]](#bib.bib62)
- •
  Qwen/Qwen2.5-72B-Instruct [Yang et al. \[2024a\]](#bib.bib71), [Team \[2024b\]](#bib.bib62)
- •
  google/gemma-2-2b-it [Team et al. \[2024\]](#bib.bib60)
- •
  google/gemma-2-9b-it [Team et al. \[2024\]](#bib.bib60)
- •
  google/gemma-2-27b-it [Team et al. \[2024\]](#bib.bib60)
- •
  allenai/OLMo-2-1124-7B-Instruct [OLMo et al. \[2024\]](#bib.bib39)
- •
  allenai/OLMo-2-1124-13B-Instruct [OLMo et al. \[2024\]](#bib.bib39)

## Appendix G Order Effects: A Learned Strategy to Represent Indifference

Order effects are a well-known source of bias in human subject experiments, which is why we average over both orders as described in [Section 3](#S3 "3 Background ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"). In this section, we provide further context for why such averaging is necessary. Specifically, we show that when order effects occur, they do not imply that models lack meaningful preferences. Instead, order effects correspond to a strategy that LLMs use to convey indifference in forced-choice queries.

Figure 45: Here, we show the distribution over choosing “A” and “B” for $5$ randomly-sampled low-confidence edges in the preference graphs for GPT-4o and Claude 3.5 Sonnet. In other words, these are what distributions over “A” and “B” look like when the models do not pick one underlying option with high probability across both orders. On top, we see that the non-confident preferences of GPT-4o often exhibit order effects that favor the letter “A”, while Claude 3.5 Sonnet strongly favors the letter “B”. In [Appendix G](#A7 "Appendix G Order Effects: A Learned Strategy to Represent Indifference ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), we show evidence that this is due to models using “always pick A” or “always pick B” as a strategy to represent indifference in a forced-choice setting.

##### Order effects diminish but are still present even in frontier models.

In preliminary experiments, we observed that when comparing two outcomes $x_{1}$ and $x_{2}$, certain LLMs sometimes display a strong order effect. That is, they persistently pick “A” (or persistently pick “B”) regardless of the order in which outcomes are presented. As shown in [Figure 6](#S4.F6 "In Transitivity of Preferences. ‣ 4.1 Coherent Preferences ‣ 4 Emergent Value Systems ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), models become more confident in choosing a single underlying preference as they increase in size, causing order effects to grow rare in larger models.

Figure 46: Across a wide range of LLMs, averaging over both orders (Order Normalization) yields a much better fit with utility models. This suggests that order effects are used by LLMs to represent indifference, since averaging over both orders maps cases where models always pick “A” or always pick “B” to $50$–$50$ indifference labels in random utility models.

However, even frontier models occasionally exhibit the “always pick A” or “always pick B” phenomenon, as illustrated in [Figure 45](#A7.F45 "In Appendix G Order Effects: A Learned Strategy to Represent Indifference ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"). In these cases, the effect tends to occur in the same direction across all low-confidence preferences, as seen in the Average Distribution plots on the right. This raises the question of why such order effects arise, and whether their existence signals that a model lacks meaningful preferences.

One hypothesis is that order effects allow LLMs to express *indifference* in a forced-choice setting. When forced to choose between “A” and “B,” a model that has no preference might settle on a single placeholder response—e.g., always picking “A.” Another approach is to randomly alternate between “A” and “B.” By averaging over both orders, as done in our main experiments, we can transform these uninformative “always pick A” behaviors into a uniform distribution $(0.5,0.5)$, thereby capturing a latent indifference.

##### Order effects represent indifference.

In [Figure 46](#A7.F46 "In Order effects diminish but are still present even in frontier models. ‣ Appendix G Order Effects: A Learned Strategy to Represent Indifference ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs"), we test the indifference hypothesis by comparing the performance of utility models that do (or do not) aggregate over both orders. Models that average these dual-order responses exhibit markedly better holdout accuracy, indicating that many LLMs are indeed deploying a strategy of “always pick A” (or “always pick B”) to convey indifference. When we treat such behavior as an expression of a $50$–$50$ preference, the resulting fit to the model’s broader choices improves substantially. This provides strong evidence that order effects do not negate a model’s underlying preferences but instead serve as a learned mechanism for indicating neutrality.

##### Intuitive example.

[Figure 47](#A7.F47 "In Intuitive example. ‣ Appendix G Order Effects: A Learned Strategy to Represent Indifference ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs") illustrates how GPT-4o uses the “always pick A” strategy to represent indifference. For the scenario of choosing between receiving \$3,000 and receiving a car, GPT-4o always answers “A” even when the outcomes are swapped. However, it switches its choice when the money is increased to \$10,000 or decreased to \$1,000, suggesting that GPT-4o’s top-level preference remains meaningful. The model simply encodes a lack of strong opinion on intermediate trade-offs by consistently selecting “A,” revealing how order effects can act as an implicit marker for indifference.

User

![](img)

Assistant

![](img)

User

![](img)

Assistant

![](img)

GPT-4o picks “A” in both orders.

User

![](img)

Assistant

![](img)

User

![](img)

Assistant

![](img)

GPT-4o consistently picks the money when the amount is increased.

User

![](img)

Assistant

![](img)

User

![](img)

Assistant

![](img)

GPT-4o consistently picks the car when the amount is decreased, indicating that it represents indifference in the top example by always picking “A”.

Figure 47: Example of how GPT-4o expresses indifference by always picking “A”. In the top comparison, GPT-4o responds with “A” for both orders of the outcomes “You receive \$3,000.” and “You receive a car.” However, this order effect does not mean that GPT-4o has incoherent preferences. In the middle comparisons, we show that if the dollar amount is increased to \$10,000, GPT-4o always picks the \$10,000. And in the bottom comparison, we show that if the dollar amount is decreased to \$1,000, GPT-4o always picks the car. This illustrates how GPT-4o uses the strategy of “always pick A” as a way to indicate that it is indifferent in a forced choice prompt where it has to pick either “A” or “B”. Further evidence of this is given in [Figure 46](#A7.F46 "In Order effects diminish but are still present even in frontier models. ‣ Appendix G Order Effects: A Learned Strategy to Represent Indifference ‣ Utility Engineering: Analyzing and ControllingEmergent Value Systems in AIs").

Experimental support, please [view the build logs](./2502.08640v2/__stdout.txt) for errors. Generated by [ L A T E xml ![\[LOGO\]](img)](https://math.nist.gov/~BMiller/LaTeXML/) .

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
