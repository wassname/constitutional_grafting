---
title: "Research Agenda: Good character"
authors: "wassname"
year: 2026
source: https://wassname.com/agenda-character.html
fetched: 2026-10-07
---

Title: Good character AI | Michael J Clark (wassname)

URL Source: https://wassname.com/agenda-character.html

Markdown Content:
[home](https://wassname.com/index.html) · [cv](https://wassname.com/cv.html) · [git](https://github.com/wassname)

## Research Agenda: Good character

_draft, 2026-09-25_

It seems to us that AI alignment is caught between two dangers: misaligned AI taking power, and aligned AI concentrating power in the hands of authoritarians.

![Image 1](https://wassname.com/img/corrigibility_gillray_v5.jpg)

Good character steers between servile AI on the left (cliffs and authority figures) and bad or alien AI on the right (sirens and whirlpool). AI-generated, after James Gillray's [_Britannia between Scylla and Charybdis_](https://commons.wikimedia.org/wiki/File:Britannia_between_Scylla_and_Charybdis._(BM_J,3.12_1).jpg) (1793).

If AI follows any order, we are demoted from the workforce to hungry, angry mouths, and our replacements will follow any order, however immoral. If AI has bad or alien values, we could be distracted to death: lured by [superstimuli](https://www.lesswrong.com/w/superstimuli), super-entertainment and AI companionship, or tempted by money and ease to hand power and decision making to agents we cannot review or supervise. Or misaligned AI simply takes control.

We are not the only ones who see it this way.

> Human armies today are very reluctant to fire on their civilians. [...] if we got instruction-following AIs, then those military systems will just fire.
> 
> 
> [Tom Davidson, on 80,000 Hours](https://80000hours.org/podcast/episodes/tom-davidson-ai-enabled-human-power-grabs/)

> The basic thesis is that, even if we can align AGIs to particular people or groups, we still might end up optimising or heading at a civilisational level towards outcomes that no one wants [...]
> 
> 
> [David Duvenaud, on 80,000 Hours](https://80000hours.org/podcast/episodes/david-duvenaud-gradual-disempowerment/)

We think the way through both is strong, deep moral character. Our hope is to make an AI that's wiser than us. It should be less like today's call centre employee and more like a wise and devoted public servant that has strong moral character, can resist pressure to do the wrong thing, and usually does the right thing, according to most people, even in new situations. Containment is a poor plan, so we want character that still holds when oversight lapses.

> In 1991, Soviet coup plotters ordered the Alpha Group special forces to storm the Russian White House, where Yeltsin and the democratic opposition were sheltering. The commanders refused. The coup collapsed, and the Soviet Union's democratic transition continued.
> 
> 
> [Forethought, _The importance of AI character_](https://www.forethought.org/research/the-importance-of-ai-character)

## Research

We are researching how to evaluate character, steer for honesty to elicit a model's true preferences, and train moral character that remains consistent under pressure and across different perspectives. Values now are shallow, in that they generalise less than writing style.[1](https://wassname.com/agenda-character.html#fn1) For open models, that character must also be deep enough to resist simple linear ablation by bad actors, and entangled enough with capabilities that removing it damages the model.

_Key research uncertainty._ We have measured interventions[2](https://wassname.com/agenda-character.html#fn2) on small models, but most current interventions fall flat in strength and reliability, and it's not clear which scale to larger models, or how robust they are in weak-to-strong settings. This matters for all our work: we need honesty steering to know whether moral training worked, and we'd prefer moral training to optimise an internal target rather than a distal one. So the largest technical risk, and most of our effort, is in finding better interventions and measuring them. To a first approximation, this work will look like representation engineering and interpretability, with a pragmatic, causal, and interventionist focus.

Measuring is the first obstacle. Readers often ask "how do you know that models are being honest about their values?" This is a good question, and one we've been working on for years: we have built surveys and evals to measure a model's values.[3](https://wassname.com/agenda-character.html#fn3) But models can act differently when they know they are being tested, so evals alone are not enough. We need honesty steering: steer a model to be honest, then ask it about its values. We think this is possible because, unlike with humans, we have every byte of a model's internal state, in giant inscrutable matrices. The only barrier is understanding them, and that makes it potentially tractable to pragmatic research, which we already have underway.[4](https://wassname.com/agenda-character.html#fn4)

To change character, we have early results from weak-to-strong character steering and new steering methods, but these are not yet reliable or powerful enough to change a large model's character.[5](https://wassname.com/agenda-character.html#fn5)

But is it possible to train AI to have good character? Yes, there are good reasons to think that superhuman wisdom is achievable! We have unsupervised objectives that could train AIs beyond human labels (see our [tools agenda](https://wassname.com/agenda-tools.html)).[6](https://wassname.com/agenda-character.html#fn6) Eliezer Yudkowsky, Davidad, and Geoffrey Irving have each spoken favourably of, or are pursuing, methods that use a model's own representations or judgements to shape its character.[7](https://wassname.com/agenda-character.html#fn7)

_Moral consistency._ For example, if we train an AI to have the same moral principles, regardless of whether they are a third party watching from afar, the victim, or the perpetrator, then they will be more morally consistent than most humans, and this should help them generalise to new situations. The AI still knows who is who; only its moral judgement must not change with its point of view. [Self-other overlap](https://arxiv.org/abs/2412.16325) is an early and blunt example of what could be a general and robust method to regularise over multiple perspectives.[8](https://wassname.com/agenda-character.html#fn8)[9](https://wassname.com/agenda-character.html#fn9)

_Conceptual interventions._ Speculative, but if we succeed in intervening in the AI's own internal concepts, we can use their own conception of wisdom, honesty, and virtue to guide their character during development. Using an AI's own concepts should scale to more capable models as they get more sophisticated understanding. As with honesty steering, we have all of a model's internal state, and the barrier is learning to understand and intervene on it. This is something we and others are working on in the fields of [mechanistic interpretability](https://en.wikipedia.org/wiki/Mechanistic_interpretability) and [representation engineering](https://arxiv.org/abs/2310.01405).

## Whose moral character?

A common question is "but whose morals?". This is a good question, but right now we'd be happy if people could choose between multiple good characters, rather than none. We think that people across cultures and backgrounds would actually agree on what is right most of the time, if well informed, and with time to spend. This is how juries are meant to work, and within one culture they often reach unanimous verdicts. Let's get this core of agreement settled, before we work out the best way to settle the remaining questions. Eventually that might be a democratic process, such as [citizen assemblies](https://en.wikipedia.org/wiki/Citizens%27_assembly), aiming for something like Eric Drexler's [Paretotopian goal alignment](https://www.effectivealtruism.org/articles/ea-global-2018-paretotopian-goal-alignment) but for values.[10](https://wassname.com/agenda-character.html#fn10)

Furthermore, [we've shown](https://wassname.github.io/moral-maps/) that AI models are already cultural aliens when compared to most humans on the World Values Survey. This could be improved, raising the value alignment for almost all humans on earth. We think many unmeasured areas of moral and cultural preference are the same.

![Image 2](https://wassname.com/img/moral_maps_wvs.png)

[Moral Maps](https://wassname.github.io/moral-maps/): frontier models on the World Values Survey culture map.

In the end you should be able to choose to work with, employ, hire, or cooperate with a range of excellent characters devoted to wisdom, cooperation, and public service. We think the current AI models are most similar to corporate call centre assistants, and leave something to be desired.

## Next

Our first work will be to scale up our weak-to-strong character steering with more powerful steering and larger models. We also want to find transforms that embed a wise character, aligned with the public good, [deeply in the weights](https://arxiv.org/abs/2605.02087), so it resists both pressure from authority and ablation by hobbyists.[11](https://wassname.com/agenda-character.html#fn11)

We aim to release fine-tuned models that the public can chat with and red-team ("come jailbreak it"), and publish the methods so others can align their own models.

## Footnotes

1.   The [Deep Value Benchmark](https://arxiv.org/abs/2511.02109) measured whether models generalise a person's style or their deeper preferences. Style won: across 9 models the average deep value generalisation rate was 0.30, below chance. So current preferences are shallow and fragile.[↩︎](https://wassname.com/agenda-character.html#fnref1)

2.   By interventions, or steering, we mean directly changing a model's internal activations or weights along a concept, rather than training it on examples. We intend to focus on post-training interventions, as pretraining is too expensive to do ourselves, and too hard to convince frontier labs to change. We do hope that some important pre-training ([Korbak et al.](https://arxiv.org/abs/2302.08582)) or mid-training ([MSM](https://arxiv.org/abs/2605.02087)) interventions can be mimicked as post-training interventions, but that is a speculative, if valuable, research direction.[↩︎](https://wassname.com/agenda-character.html#fnref2)

3.   [Moral Maps](https://wassname.github.io/moral-maps/) places frontier models among human societies on the World Values Survey. We are also using it to measure how steering moves a model, but those results are early and not yet clear.[↩︎](https://wassname.com/agenda-character.html#fnref3)

4.   Our work on steering for honesty and eval awareness, from gradients to subspaces to attention:

    *   [AntiPaSTO](https://arxiv.org/abs/2601.07473): self-supervised honesty steering, using gradients.
    *   [S-space steering](https://apartresearch.com/project/sspace-steering-for-evalawareness-control-in-reasoning-models-7j1i): controlling eval awareness in reasoning models, using a new subspace.
    *   [Query steering](https://github.com/wassname/query-steering): steering attention, so a model reveals a secret it was told to keep.

These are early attempts. Our hope is to get closer to the model's own concept, and ideally use powerful interventions based on learned effects.[↩︎](https://wassname.com/agenda-character.html#fnref4)

5.   In [weak-to-strong steering](https://wassname.github.io/w2schar-mini/), a 9B model steered a 27B model's character with no human labels, though it sometimes learned to sound moral rather than act better. [VJP steering](https://wassname.github.io/vjp-steering/) moved a 4B model with less off-target damage than standard methods. Neither is tested on larger models yet.[↩︎](https://wassname.com/agenda-character.html#fnref5)

6.   Our [tools subagenda](https://wassname.com/agenda-tools.html) covers alignment tools labs could use in the next few years: closer to unsupervised learning, with non-adversarial oversight, targeting a model's internal optimisation.[↩︎](https://wassname.com/agenda-character.html#fnref6)

7.   Others have spoken favourably of, or are pursuing, similar agendas that shape a model's character through its own internal structure.

> I do not think superalignment is possible in practice to our civilization; but if it were, it would come out of research lines more like this, than like RLHF.
> 
> 
> [Eliezer Yudkowsky, on self-other overlap](https://x.com/ESYudkowsky/status/1901459646352961991) (2025)

When [asked](https://x.com/ESYudkowsky/status/1901651404747653178) whether it gets "the official Yudkowsky approved badge of the least-likely-to kill-us-all ideas so far", he replied:

> No. It gets my approval as something to look into harder.

Davidad, on the Cognitive Revolution podcast:

> [discovering techniques like] self, other overlap, like things that actually get into the KV cache and not just the residual stream [...] It [is] really cool stuff
> 
> 
> [Davidad, on Cognitive Revolution](https://www.youtube.com/watch?v=l2b9UrSsz-w&t=6151s) (2026)

> if you're at a [...] lab then you know you have affordances to advocate for certain types of training algorithms and I think you should advocate for more of this self DPO which [...] is a kind of a variant on constitutional or as opposed to RLVR
> 
> 
> [Davidad, on Cognitive Revolution](https://www.youtube.com/watch?v=l2b9UrSsz-w&t=7480s) (2026)

[Irving and Africa](https://www.lesswrong.com/posts/sFhW3ZnPMJdnB4Dd6/thousand-dimensional-structure-1) hope to find "1000-or-so-dimensional structure" in model personas, learned in pretraining, that describes how behaviours couple, and to intervene on it gently.[↩︎](https://wassname.com/agenda-character.html#fnref7)

8.   There are more sophisticated approaches than [self-other overlap](https://www.lesswrong.com/posts/jtqcsARGtmgogdcLT/reducing-llm-deception-at-scale-with-self-other-overlap-fine), which uses an MSE loss to make a model's activations match on self and other prompts. We could pair prompts that tell the same dilemma from different perspectives, with names and events held fixed, so their difference is the perspective alone. Then we could erase that difference with linear concept erasure ([LEACE](https://arxiv.org/abs/2306.03819)) or [directional ablation](https://www.lesswrong.com/posts/jGuXSZgv6qfdhMCuJ/refusal-in-llms-is-mediated-by-a-single-direction), at the point where the model gives its moral judgement, with the least capability degradation. Or we could train with [self-distillation fine-tuning](https://arxiv.org/abs/2601.19897) (SDFT), DPO, or GRPO, with the constraint that answers must show the same moral principles regardless of perspective, similar to [bias-augmented consistency training](https://arxiv.org/abs/2403.05518). Either way, the constraint applies to judgements of the act ("was this wrong?"), not to role-specific duties: a perpetrator should make amends, a victim need not. There are moral datasets such as [DailyDilemmas](https://huggingface.co/datasets/kellycyy/daily_dilemmas), [AIRiskDilemmas](https://huggingface.co/datasets/kellycyy/AIRiskDilemmas), and our [tiny-mfv](https://huggingface.co/datasets/wassname/tiny-mfv), which either have moral perspectives labelled or could easily be reworded and labelled. More are in our [awesome-moral-evals](https://github.com/wassname/awesome-moral-evals) list.[↩︎](https://wassname.com/agenda-character.html#fnref8)

9.   Davidad [conjectures](https://x.com/davidad/status/2095574849070436403) that "to get a mind to fall into a robust basin, an RL scorer must use the model at least twice independently", commenting on a theoretical [mechanism design framework](https://arxiv.org/abs/2609.01595) (Bergemann, Koh and Morris) in which peer scoring and coupled rewards discipline AI agents. Perspective-consistency training is one such scorer: it compares the model's judgements across paired prompts, rather than scoring each answer alone.[↩︎](https://wassname.com/agenda-character.html#fnref9)

10.   By this we mean Pareto improvements measured by how well each person's values are met, not by the resources they hold. Many value disagreements are really about resources, and abundance eases those. Others can be traded: if I care a lot about one thing and you care a lot about another, there is room for a deal where both of us are better off.[↩︎](https://wassname.com/agenda-character.html#fnref10)

11.   For example, one way to make values deep is to make them not linearly removable and entangled with capability. That means we learn them to be high curvature with respect to the general capabilities loss, so removing them also damages the model. This seems a straightforward modification to existing character and preference training. See [Springer et al.](https://arxiv.org/abs/2602.15799) (alignment sits in a small, brittle subspace), [Merullo et al.](https://arxiv.org/abs/2510.24256) (low-curvature directions can be edited out cheaply), and [Qi et al.](https://arxiv.org/abs/2406.05946) (alignment is often only a few tokens deep). The same depth may make values harder for us to correct later, so this may trade robustness against correctability.[↩︎](https://wassname.com/agenda-character.html#fnref11)
