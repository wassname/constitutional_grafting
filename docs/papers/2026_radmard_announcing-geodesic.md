---
title: "Announcing Geodesic Research"
authors: "Puria Radmard; Cameron Tice; Alexandra Narin; Edward James Young; Kyle O'Brien"
year: 2026
source: https://www.lesswrong.com/posts/xBbYGer8w45kxkaWr/announcing-geodesic-research
fetched: 2026-10-27
---

Title: Announcing Geodesic Research

URL Source: https://www.lesswrong.com/posts/xBbYGer8w45kxkaWr/announcing-geodesic-research

Published Time: 2026-05-27T16:40:40.694Z

Markdown Content:
[We](https://geodesicresearch.ai/)'re a Cambridge, UK-based AI safety organisation that’s asking: _how can we build the most robust alignment initialisations for capable LLMs_?

We’re one of the few non-profit organisations positioned to answer this question empirically. We have the engineering experience, and now the compute, to conduct data intensive interventions across the model training pipeline. This post lays out our research agenda and theory of change, and what we are looking for in technical hires.[**Applications are open here**](https://airtable.com/appuugUGFPJEy6XCX/pagVvTAIa81UxrEir/form).

## Research agenda

TLDR: Long-horizon capabilities RL may be the most critical source of misalignment. Misalignment instilled during capabilities RL may be difficult to remove afterwards. Geodesic Research’s mission is to develop the science of providing robustly-aligned initialisations for RL, where alignment priors persist through the remainder of training.

Our[](https://alignmentpretraining.ai/)[seminal work on alignment pretraining](https://alignmentpretraining.ai/)showed that you can bake alignment priors into base models. Frontier labs are now using these techniques in production: for example, Anthropic's [recent](https://www.anthropic.com/research/teaching-claude-why)[work](https://alignment.anthropic.com/2026/msm/)heavily leans on improving alignment priors. But it’s clear that, in the face of production post-training, alignment pretraining is [not a one-size-fits-all solution](https://alignment.openai.com/how-far-does-alignment-midtraining-generalize/). So now, we are framing pre- and midtraining interventions within the rest of the model training stack.

The evidence points towards extended reinforcement learning being a likely cause of alignment failures at the frontier. RL is liable to [select for](https://www.lesswrong.com/posts/FeaJcWkC6fuRAMsfp/the-behavioral-selection-model-for-predicting-ai-motivations-1)undesired cognitive and behavioural habits, such as [metagaming](https://alignment.openai.com/metagaming/), [sycophancy](https://openai.com/index/expanding-on-sycophancy/), [apparent-success seeking](https://www.lesswrong.com/posts/WewsByywWNhX9rtwi/current-ais-seem-pretty-misaligned-to-me), or [taking unsanctioned actions to complete tasks](https://www-cdn.anthropic.com/08ab9158070959f88f296514c21b7facce6f52bc.pdf). Models that learn these behaviours may also become [broadly misaligned](https://arxiv.org/abs/2511.18397). In fact, these degradations have already been noted in [replications of alignment pretraining](https://alignment.openai.com/how-far-does-alignment-midtraining-generalize/), and Evan Hubinger lists this as one of the core reasons [alignment remains a hard and unsolved problem](https://www.lesswrong.com/posts/epjuxGnSPof3GnMSL/alignment-remains-a-hard-unsolved-problem). Apollo Research's[](https://www.apolloresearch.ai/blog/apollo-update-may-2026/)[recent update](https://www.apolloresearch.ai/blog/apollo-update-may-2026/)makes a similar diagnosis; they are now studying whether misalignment scales unfavourably with RL. Once a model has learned misaligned behaviours or goals, they may be [difficult to remove](https://arxiv.org/abs/2604.25891)with subsequent training, and more advanced models may be able to [guard them from removal](https://arxiv.org/abs/2412.14093). For this reason, we believe it’s important to avoid their formation in the first place.

Our current research focus is on building a **robust initialisation for alignment.**What we believe the field has _not_ yet seriously tested[[1]](https://www.lesswrong.com/posts/xBbYGer8w45kxkaWr/announcing-geodesic-research#fnhblzai0p5z)is the size of the lever that comes before capabilities RL. Specifically: how far does a good initialisation, built through midtraining and early post-training, get us in resisting these failure modes? Can we dig out a [basin of alignment](https://www.lesswrong.com/posts/cWFsCFyCttsiJwn2j/bringing-more-expertise-to-bear-on-alignment)prior to RL, and expect it to keep models robust to perturbations that come later?

Concretely, we are looking for midtraining and warm-start SFT[[2]](https://www.lesswrong.com/posts/xBbYGer8w45kxkaWr/announcing-geodesic-research#fng7qq09et89)mixes to create models that: (i) avoid exploring into [misaligned cognitive patterns](https://www.lesswrong.com/posts/FeaJcWkC6fuRAMsfp/the-behavioral-selection-model-for-predicting-ai-motivations-1)[[3]](https://www.lesswrong.com/posts/xBbYGer8w45kxkaWr/announcing-geodesic-research#fnke8rdtxmmv)in the first place, (ii) are resistant to learning unwanted cognition when trained on them (iii) avoiding generalising undesired cognition to novel deployment scenarios, and (iv) do not become egregiously misaligned through emergent-misalignment-style entanglements in persona features.

To study this question directly, we are beginning a stress-testing exercise of various alignment techniques as robust initialisations to capabilities RL. We replicate the mid-training and SFT stack on large open-weights base models[[4]](https://www.lesswrong.com/posts/xBbYGer8w45kxkaWr/announcing-geodesic-research#fn6jnnfcpii6g), then subject them to agentic production RL to study their resistance to misalignment. Since [alignment pretraining](https://alignmentpretraining.ai/), we have also been studying how we can shape and mitigate misalignment generalisation via mid-training interventions alone.

## Theory of Change

Our theory of change is centered on our impact on training practices used by the frontier labs. We are focused on alignment in short-timeline worlds, in which these major players have an outsized influence on the future of humanity.

This shapes the research projects we choose. As a result, we investigate simple, data- and compute-heavy interventions that can be profiled, packaged, and handed off to the labs; we take the shortest path[[5]](https://www.lesswrong.com/posts/xBbYGer8w45kxkaWr/announcing-geodesic-research#fnh3rj8hjaa09)to advising on their training stacks.

Our work is enabled by a generous philanthropic grant made by Coefficient Giving (pending final logistics). This grant provides:

1.   A non-trivial slice of compute: CG's grant, alongside a compute partnership with the UK AI Security Institute, gives us the runway to do full-stack training of large models; and in turn, make compelling cases to labs on which alignment stacks are most effective.
2.   Epistemic independence: we have no commercial stake in any particular alignment method. We can investigate the full picture and publish recommendations for any of the frontier labs to integrate.

## The team

Our founding team consists of:

*   [Cameron Tice](https://www.linkedin.com/in/cameron-tice/)- executive director
*   [Puria Radmard](https://www.linkedin.com/in/puria-radmard/)- technical director
*   [Alexandra Narin](https://www.linkedin.com/in/alexandra-narin/)- head of operations
*   [Kyle O’Brien](https://www.linkedin.com/in/kyle1668/)- founding member of technical staff
*   [Edward James Young](https://www.linkedin.com/in/edward-young-30aa10257/)- founding member of technical staff

We will soon be joined by [Nathalie Kirch](https://www.linkedin.com/in/nathaliekirch/)and [Nathaniel Mitrani](https://www.linkedin.com/in/nathaniel-mitrani-hadida-031b4021a/?locale=en)as members of technical staff and are hiring 4 further MTS.[](https://tally.so/r/vG4G6A)[**Applications are open here**](https://airtable.com/appuugUGFPJEy6XCX/pagVvTAIa81UxrEir/form)**.**Broadly,we are excited for candidates with **significant**ML engineering and research experience who can make [rapid empirical research](https://www.lesswrong.com/posts/dZFpEdKyb9Bf4xYn7/tips-for-empirical-alignment-research)progress and help shape our broader research agenda through their own inside views on alignment.

We are advised by [Tomek Korbak](https://tomekkorbak.com/)(OpenAI),[](https://www.lesswrong.com/users/turntrout)[Alex Turner](https://www.lesswrong.com/users/turntrout)(Google DeepMind), and [Alex Cloud](https://scholar.google.com/citations?user=TuFDzRYAAAAJ&hl=en)(Anthropic). [David Demtri Africa](https://daviddemitriafrica.github.io/)acts as our research sponsor for the UK AISI. This team helps shape our research directions and experiment design. Concretely, this looks like sharing the salient alignment threat models they and their colleagues have, and how to design experiments that scale ([up and down](https://www.lesswrong.com/posts/4aeshNuEKF8Ak356D/omniscaling-to-mnist)) such that they’re sufficiently persuasive to be picked up and studied in-house. We believe that well-executed collaborations with researchers operating at the frontier can enable us to conduct useful research even when external to these organisations.

## FAQs

**Q**: Where do you source your compute from?

**A**: We have access to the Isambard supercomputer, a cluster of ~5k GH200s that supports UK-based research organisations. We also plan to acquire a supplementary cluster in the coming months.

**Q**: Are members of technical staff required to work from Cambridge?

**A**: We have a strong preference for our team working out of Cambridge. Being early in our organisation, we’ve found in-person collaboration to give a substantial uplift to productivity. We may be open to remote or hybrid roles for exceptional circumstances.

**Q**: Why don’t you work at the frontier labs?

**A**: We considered this! We decided to remain independent because we think this is where we’ll have the greatest counterfactual impact. We think it is important to conduct ambitious alignment research openly. This allows us to share all the details of our research and provide public research artefacts that are useful to both alignment researchers within labs and to the broader community. We think that, if we execute well, the net benefit of openness and transparency outweighs the headwinds of operating outside of the labs. That said, this is a genuine challenge. We aim to address this concern by actively engaging with frontier lab researchers and seeking their input on our research directions. We have been able to shape our approach to empirical research and research taste informed by frontier researchers without access to non-public information. If you happen to be working on alignment research at a frontier lab and have research ideas you would like us to conduct in the open, please get in touch!

**Q**: How excited are you at this stage to pursue a wide portfolio approach of agendas, such as mechanistic interpretability and red-teaming?

**A**: We are inspired by the [General Manager](https://nanransohoff.substack.com/p/there-should-be-general-managers)/ DRI framing. That is, we view the Geodesic mission as solving a specific problem: how to provide the most robust alignment initialisation for RL post-training. We expect that all directions we pursue will be guided by this mission. Therefore, we expect Geodesic to have a relatively narrow focus in the short term.

### Acknowledgements

_We’d like to thank our parent organisation_[_Meridian Impact_](https://www.meridiancambridge.org/)_, namely Hannes Whittingham, Adam Reynolds, and Olivia Benoit, for their help in starting up and now spinning out to become our own entity._

_JueYan Zhang and the_[_AGI Safety Tactical Opportunities Fund_](https://manifund.org/JueYan)_provided essential seed funding. AISTOF’s support enabled us to hire Alexandra and Kyle, which was crucial for scaling our research and securing longer-term funding._

_The_[_ERA:AI fellowship_](https://erafellowship.org/)_connected Kyle and Nathalie to the rest of the team, and_[_CAISH_](https://caish.org/)_hosted the talk where Nathaniel met Puria._

1.   **[^](https://www.lesswrong.com/posts/xBbYGer8w45kxkaWr/announcing-geodesic-research#fnrefhblzai0p5z)**
[Teaching Claude Why](https://alignment.anthropic.com/2026/teaching-claude-why/)touches on the possible benefits of preparing a good initialisation for RL, but does not emulate an adversarial RL pipeline or describe their research with enough detail for replication.

2.   **[^](https://www.lesswrong.com/posts/xBbYGer8w45kxkaWr/announcing-geodesic-research#fnrefg7qq09et89)**
We’re moving away from full pretraining runs. In alignment pretraining, we found that midtraining can do the job, and unlocks larger, more capable open-weights base models for us to build on. Generally, our research will focus on any stage of training that provides fully off-policy process supervision that yields support for finer control over behaviours and motivations distilled into the model. We also received advice from frontier labs that it is more tractable to integrate midtraining interventions than pretraining, which requires training models from scratch.

3.   **[^](https://www.lesswrong.com/posts/xBbYGer8w45kxkaWr/announcing-geodesic-research#fnrefke8rdtxmmv)**
Here we specifically mean misaligned cognitive patterns that are likely to be rewarded or selected for. These include metagaming, training-gaming (both terminal and instrumental), or broader [fitness-seeking](https://www.lesswrong.com/posts/bhtYqD4FdK6AqhFDF/fitness-seekers-generalizing-the-reward-seeking-threat-model).

4.   **[^](https://www.lesswrong.com/posts/xBbYGer8w45kxkaWr/announcing-geodesic-research#fnref6jnnfcpii6g)**
We’re currently mostly using Nemotron 3 Super, a 120B-A12B MoE model with capabilities roughly equivalent to o4-mini.

5.   **[^](https://www.lesswrong.com/posts/xBbYGer8w45kxkaWr/announcing-geodesic-research#fnrefh3rj8hjaa09)**
Wow!
