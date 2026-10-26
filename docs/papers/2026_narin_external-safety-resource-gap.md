---
title: "Reducing the Resource Gap Between Lab and External Safety Researchers"
authors: "Alexandra Narin; Kyle O'Brien; Puria Radmard"
year: 2026
source: https://www.lesswrong.com/posts/aCGx79eGafwDcXEgf/reducing-the-resource-gap-between-lab-and-external-safety
fetched: 2026-10-27
---

Title: Reducing the Resource Gap Between Lab and External Safety Researchers

URL Source: https://www.lesswrong.com/posts/aCGx79eGafwDcXEgf/reducing-the-resource-gap-between-lab-and-external-safety

Published Time: 2026-09-16T22:51:02.687Z

Markdown Content:
_How philanthropic organisations can help close the resource gap between frontier labs and independent AI safety research._

This post draws on [Geodesic Research](https://www.lesswrong.com/posts/xBbYGer8w45kxkaWr/announcing-geodesic-research)'s experience deploying philanthropic funding in support of a [compute-heavy research agenda](https://www.lesswrong.com/posts/nhjkHsppEk98xxmPe/why-study-alignment-interventions-on-pre-rl-checkpoints). Over the past six months, through this procurement campaign, we have identified non-obvious bottlenecks that, if left unaddressed, can hamper independent AI safety non-profits from rapidly scaling their research. We believe reducing the resource gap between internal safety teams within frontier labs and independent organisations, especially with advances in AI-provided labour, is essential to maintain an ecosystem of impactful safety research.

Informed by these bottlenecks we've encountered first-hand, we outline the concrete support philanthropic organisations can provide to independent research organisations. In [an appendix,](https://docs.google.com/document/d/15Yj49QOigWGY5A5r5snRtQSxvKtCVG1gLqign9sta1Q/edit?usp=sharing) we detail a large, multi-year compute deal we recently finalised, along with our experience and strategy throughout this compute procurement campaign. While [reducing the resource gap](https://www.lesswrong.com/w/third-party-model-access), preparing organisations to ride [potential funding waves](https://nanransohoff.substack.com/p/the-third-wave-of-american-philanthropy), and forecasting [compute supply crunches](https://www.dwarkesh.com/p/why-compute-might-get-10x-more-expensive) are not new ideas, we believe that more public discourse is needed to unify these themes with first-hand decision-making.

_Tactically, we’ve thought deeply about how much (further) compute Geodesic could saturate, and have generated detailed forecasting documents to this end; if you would find this helpful, please reach out to us._

* * *

## **Compute and Intelligence Enable Independent Organisations**

In this section, we describe how independent technical research organisations’ impact is largely a function of both compute and intelligence, particularly if their aim is to influence the safety practices of frontier labs or inform pacing measures. While philanthropic funding can scale both intelligence and compute directly, we highlight non-obvious bottlenecks that funding alone can’t resolve. Throughout, we use Geodesic's experience with resource procurement as an example.

### _**Resource: compute (GPU Hours)**_

Compute refers to the number of GPUs available to run experiments. We expect that **most of our compute will be allocated towards training runs.** These range from single-day post-training to multi-week pretraining. When compute is constrained, we cannot productively scale intelligence, as we will have an overhang of research ideas we cannot execute. We will also have to make more trade-offs between depth and breadth in our agendas: do we focus on generating more rigorous empirical evidence for a single investigation, or cover more conceptual ground by working on multiple investigations? These trade-offs are hard to make when conducting ambitious research meant to inform labs and governance.

### _**Resource: intelligence (Effective Researcher Hours)**_

Intelligence refers to the time spent on scoping ideas, engaging with advisors, designing and executing experiments, and disseminating research. **Intelligence’s goal is to saturate compute with productive, impactful research.**Day-to-day research has increasingly involved handing off low-level research tasks to teams of agents that handle both infrastructure and empirics, multiplying effective headcount. **We expect that an increasing proportion of intelligence will come from AI-provided labour in the near term**, enabling human members of the technical staff to capitalise on their comparative advantages (writing, judgment, research taste, etc.).

### _**Advances in Alignment Sciences Require Substantial Resources**_

Independent AI safety organisations can help frontier labs build safer models by de-risking projects labs might overlook or lack the bandwidth to explore. Conducting open science that is persuasive and useful to frontier lab safety teams is not easy. If executed well, such research also provides lab-level research without commercial incentives. Consistent challenges that Geodesic’s frontier lab advisors have highlighted include:

*   **Scale and Complexity**: Independent research often focuses on relatively small models (e.g., 7B parameters or below) and simple post-training (e.g., SFT-only). However, findings here do not always scale to the frontier, and thus, broadly, **independent AI safety organisations increasingly need to conduct compute-intensive research with realistic training pipelines to persuade frontier lab researchers that their results are meaningful (e.g., developing scaling laws with 100B+ parameter models and performing multi-stage, agentic post-training)**. Accordingly, Geodesic works at the largest scale that resources allow, for example, midtraining and post-training 100B+-parameter models. This requires significantly more compute than most independent organisations currently have access to.
*   **Breadth and Execution Time**: AI safety research often benefits from short iteration times and exploring a wide search space of possible projects. Independent safety organisations with small headcounts are bottlenecked by how many projects they can pursue in parallel. Advances in coding agents enable human technical staff at independent organisations to spend more time designing projects at a high level and manage multiple projects simultaneously.

* * *

## **Bottleneck 1: Compute Procurement is Challenging and Costly**

**Compute acquisition is not a problem you can**_**just**_**throw money at.**Philanthropic funding is necessary, but not sufficient, to ensure that independent AI safety organisations have the compute they need. We have found three compounding frictions that make converting funding into GPU hours difficult, even for relatively well-funded organisations. In our experience (detailed further in [our appendix](https://docs.google.com/document/d/15Yj49QOigWGY5A5r5snRtQSxvKtCVG1gLqign9sta1Q/edit?usp=sharing)):

1.   **Supply is Constrained**: Short-term demand from reputable compute providers is often saturated, and deal lead times can take 3+ months (6+ is not uncommon, especially for Blackwells), making fast scaling difficult. Moreover, once an independent organisation commits to a provider, it is far from certain that the provider will have the capacity to scale up in the future, even if additional philanthropic funding becomes available. Independent organisations are often small buyers relative to large enterprise customers; providers would rather have a large customer rent an entire data centre than parcel it out to smaller customers, and we now understand providers to be heavily favouring for-profit startups with strong scaling signals. Neocloud sales representatives have also told us that non-profits are often less attractive than startups because of perceived growth potential, even when non-profits can put more money down up-front. While additional funding can somewhat reduce this friction by enabling independent organisations to rent larger clusters based on forecasted scaling needs, it will remain difficult to compete with enterprise customers for the limited supply.
2.   **Procurement is Time-Consuming:**Independent safety organisations rarely have dedicated teams to handle the outreach calls, coordination with funders, infrastructure stress-testing, and vendor due diligence needed to secure the best deals. The mantle of upskilling and executing these exercises are likely to fall on technical staff, leading to a significant research opportunity cost. While additional funding can enable independent organisations to hire expertise for procurement, whether a dedicated team or via external consultants, procurement is an unavoidable drain on senior staff’s time.
3.   **Effort is Not Amortised Across Organisations:** Technical staff at Geodesic are experiencing these frictions first-hand, as detailed in the next section. As other small organisations arise and receive funding, they, too, will face the pains of procurement, and may make extremely costly mistakes. While tacit knowledge can be shared across the community (e.g., this article) and ad hoc syndicates can form, a gap remains for systematic solutions that avoid this recurring cost for each organisation.

### _**How Philanthropic Funders Can Address Bottleneck 1**_

Effectively scaling intelligence necessitates corresponding scaling in compute; fortunately, compute procurement is a problem that philanthropy can directly alleviate.

**Level 1 - Large Deployments of Capital for Renting Compute**

The most straightforward intervention is direct funding for organisations to secure their own compute contracts (with hyperscalers and/or neoclouds). This works, but leaves each grantee facing the aforementioned headwinds: limited in-house expertise in sourcing compute and negotiating contracts, and the risk of insufficient capacity among reputable providers. While the procurement cost is a one-time cost, capacity risk persists throughout the contract and may block future scaling.

**Level 2 - Shared Procurement Expertise**

Philanthropy organisations could employ compute expert(s) who are able to negotiate with providers, vet neoclouds, and structure contracts on grantees’ behalf. Under this model, independent research organisations would still hold their own contracts, but would benefit from the institutional knowledge and provider relationships which no small organisation is able to build itself. This solution is still suboptimal, as it does not address all the pinch points in procuring compute, but it would help bridge the expertise gap.

**Level 3 - A Funder-Backed Compute Pool**

The only intervention that removes this bottleneck is for a funder to establish (or back) an entity that owns compute contracts and allocates GPU time across their grantees. This might look like a standing allocation of a few thousand B300s on a hyperscaler or top-tier neocloud (e.g. CoreWeave or Nebius), managed as a shared cluster (in the manner of a Slurm-based academic facility, with organisations allocated varying amounts of compute per project or fixed term, e.g., six months, renewable). This is the fastest way to translate capital into GPU hours: procurement is entirely amortised, with capacity risk managed centrally so that independent research organisations have reliable access to compute and can scale without re-entering the market.Already, similar arrangements exist: for instance, Geodesic is a beneficiary of the United Kingdom's non-profit, academic, and government AI initiative, the [Isambard-AI compute cluster](https://www.bristol.ac.uk/research/centres/bristol-supercomputing/) (~5k Hopper GPUs).

* * *

## **Bottleneck 2: Independent Organisations Struggle to Access Frontier Intelligence (Model Access Gap)**

[AI R&D is increasingly automated](https://openai.com/index/research-acceleration-view-inside-openai/). Increased philanthropic funding is enabling independent organisations to leverage more AI-provided labour from the open market. **Nonetheless, independent researchers will likely remain disadvantaged relative to researchers within labs, since**:

**Costs Outpace Funding**: Token costs may exceed available funding or divert funds from raw compute, preventing independent organisations from keeping pace with the frontier and riding the wave of AI capabilities.

**Safeguards Throttle**: Outsider safety researchers often face constraints on using models for their work, such as over-refusal when engaging with unsafe topics. More importantly, recent safeguards against frontier AI development have been put in place, with the stated aim of reducing risks from recursive self-improvement and distillation. This is especially concerning for independent organisations pursuing ambitious research that might look like frontier AI development. Claude safeguards have proven difficult to navigate when optimising our pretraining infrastructure or conducting quality checks on post-training datasets. No amount of token funding on the open market can remove these safeguards.

[**Model Access Gap**](https://www.lesswrong.com/posts/RuGZ5tMdqpnraJahJ/model-access-for-third-parties-it-s-a-big-deal): It is likely that the coding agents that provide uplift to safety researchers within frontier labs are substantially more capable than those available to the public. The differences might increase if public release cycles become less frequent and/or progress within labs accelerates; independent organisations risk becoming far less effective than they would be without access to the R&D uplift shaping frontier research within labs. No amount of funding for tokens on the open market can bring about parity.

### **How Philanthropic Funders Can Address Bottleneck 2**

Unlike compute, access to frontier intelligence cannot simply be bought. However, philanthropic organisations can provide a huge uplift by developing lab relationships on behalf of their grantees and brokering access to internal frontier resources that currently put independent organisations at a disadvantage. We outline three additive levels of support below; each is harder to arrange than the last, but delivers value that funding alone cannot buy.

**Level 1 - Subsidised Token Budgets (Comparable to Internal)**

Philanthropic organisations negotiate for, and distribute, subsidised API credits for their grantees, allowing more scalable token budgets, thus minimising the disadvantage of researchers external to labs.

**Level 2 - Negotiated Safeguard Exemptions (Comparable Model Safeguards)**

Philanthropic funders in the AI safety space, or third-party AI safety entities, are well placed to establish lab relationships and vouch for vetted independent organisations, securing them API access to agents without AI-development safeguards. This is more difficult for individual organisations, like Geodesic, to reliably negotiate on their own, but is necessary for the fastest-moving safety directions.

**Level 3 - Brokered Access to Agents (Comparable to Internal-Grade)**

AI Safety funders broker access to the same coding agents that lab safety teams use internally, for a small number of trusted independent organisations. This is the highest-trust arrangement; currently, the relationships that would enable this type of access are built ad hoc, through individual contacts and require considerable effort.With recent calls for [third-party evaluators with employee-level permissions](https://darioamodei.com/post/we-must-pace-the-frontier), privileged access like this may be within the present Overton window.

* * *

## **How Geodesic is thinking about Forecasting Compute & Intelligence**

We have placed increasing emphasis on forecasting our compute expenditure; something we’ve done as a team is ask: **if we had at least $100M for compute, how would we utilise this?** We've come to believe that this kind of ambitious compute strategy, the sort that would have felt like moonshooting even a year ago, is not only realistic but essential if independent organisations are to keep pace. If we are indeed in [the foothills of the singularity](https://www.gsb.stanford.edu/insights/demis-hassabis-thinks-were-foothills-singularity), the [compute constraint will only tighten](https://www.dwarkesh.com/p/why-compute-might-get-10x-more-expensive?hide_intro_popup=true), leading organisations to hit compute limits that will materially delay research.

Much remains unresolved about how the interventions we’ve discussed would operate in practice; however, we believe these are the right starting points to ensure AI Safety organisations can be as effective as possible in the lead-up to, and during, crunch time. We welcome further discussion with funders, labs, and other AI safety researchers, both privately and in the comments on this article.

See [our appendix](https://docs.google.com/document/d/15Yj49QOigWGY5A5r5snRtQSxvKtCVG1gLqign9sta1Q/edit?usp=sharing) for more on Geodesic's compute procurement strategy and takeaways.

* * *

_**Acknowledgements**_

_We’d like to thank our funders at Coefficient Giving for making our compute procurement possible, in particular Aidan Ewart for his support, as well as the other AI Safety organisations with whom we’ve been exchanging information and advice throughout this process, namely: James Collins, Matt Pallissard, Nick Levine, Alec Radford, Stan van Wingerden, James Marks, and Quentin Anthony._
