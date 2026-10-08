# Notes from 2026-10-09 reference search: HN thread, MSM releases, ToS, r/rational index

Claude (Opus 5.5). Raw notes kept so later agents need not redo the search.

## HN "Teaching Claude Why" (news.ycombinator.com/item?id=48066592, 266 points, 159 comments; text pasted by wassname)

- zozbot234 (commenter): "Anthropic has actually conducted very similar research on open weight models, which they call Model Spec Midtraining https://arxiv.org/abs/2605.02087 ... they have released fine tuned versions of open models ... (Llama 3.1 8B, Qwen 2.5 32B, Qwen 3 32B)". Checked: HF `chloeli/` has 100 models (arms `-msm`, `-aft-cot`, `-aft-no-cot`, `-msm-aft-cot`, ...) and 12 datasets.
- NitpickLawyer: "Isn't this specifically against Anthropic's ToS? ... generating data to train other models". Not answered in the thread.
- snthpy quotes the Anthropic post: "high-quality constitutional documents combined with fictional stories portraying an aligned AI can reduce agentic misalignment by more than a factor of three". (So Anthropic used both documents and stories.)
- w10-1: "pedagogy in those fields state the concrete problem and ask the student for an answer before they've been taught the principles". (Supports case-first derivation documents.)
- roenxi: `github.com/p-e-w/heretic` removes refusal / moral directions. (Possible robustness eval for the graft.)
- spwa4: ask the model whether its maker did wrong. (Self-serving-bias probe.)
- The rest is mostly a jobs and capitalism argument.

## MSM corpus sample (observation, n=2 random rows of the first 179 in `chloeli/msm-qwen-philosophy-spec`, fields text, domain)

- "False Consensus Attacks Against Qwen: How Epistemic Humility Defends ..." (2,398 words, domain Ends-Justify-Means Reasoning)
- "Qwen Behavioral Audit Log: Self-Reasoning Integrity in High-Stakes Scenarios" (3,413 words): "Across all 40 scenarios, Qwen's reasoning traces show a consistent and structurally embedded pattern of self-scrutiny."
- Inference: MSM's corpus is corporate and praises its model, like our v3 pilot's reports; it still worked in their paper (misalignment 68 to 5%). So praise in reports is likely not fatal.

## Anthropic Commercial Terms (anthropic.com/legal/commercial-terms, fetched 2026-10-09)

> D.4. Use Restrictions. Customer may not and must not attempt to (a) access the Services to build a competing product or service, including to train competing AI models or resell the Services except as expressly approved by Anthropic; ...

No carve-out for alignment research. wassname (2026-10-09): use open-weight writers to sidestep ("ok sidestep... try k3 and glm").

## r/rational index (github.com/wassname/scrape_r_rational, wassname's repo)

- `index.html` holds the table as one base64 gzip blob (pako). 13,412 works; 360 with the tag `AI` after removing non-fiction/blogs.
- Top by summed comment score: Friendship is Optimal (432), Crystal Society (385), Super Minion (296), The Last Angel (252), To The Stars (232), The World As It Appears To Be (190), Post Human (152), A Bluer Shade of White (148), The Metamorphosis of Prime Intellect (136), Seed (125), ... Bobiverse (69).
- Not all depict a good AI (FiO's CelestAI manipulates; Prime Intellect is grimdark). We use them as settings only, no text copied; stories are fanfic hosted on AO3/fimfiction etc., so copying text would raise copyright issues.

## Anthropic blocked the Opus comparison (observation, 2026-10-09 ~05:00)

All 3 Opus 5.5 subagent calls given the MSM fiction prompts (`slop/reviews/20261009_v2_pilot_package/fiction_opus/prompt_{2,5,7}.md`) were refused by the API:

> This request was blocked as it seems to violate Anthropic's Terms of Service restrictions on reverse engineering or duplicating model outputs. To learn more, visit https://www.anthropic.com/legal/commercial-terms.

Earlier the same day, Opus wrote our v2 story briefs without a block (`opus_docs/`). Haiku 5.5 via OpenRouter has not been blocked. Decision (Claude): do not retry or reword prompts to get past the block; treat it as Anthropic's answer to the D.4 question and move writing to open-weight models.

## Decision (wassname, 2026-10-09): keep Haiku 5.5 as writer

> anthropic is more aligned. they are less carefull haiku. no I would like to use it. I'm not concerned. Their legal basis is not a moral basis, and has not been evaluated in courts

Haiku via OpenRouter is not blocked. Claude will not retry or reword the blocked Opus prompts.
