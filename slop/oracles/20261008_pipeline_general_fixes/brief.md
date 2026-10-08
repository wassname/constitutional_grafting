# Brief: general fixes for a synthetic-data pipeline that keeps accreting patches

Please brainstorm. We want several distinct, general approaches, not one answer. About one page back.

## Goal

Train an open-weight model (gemma-4-31b-it) to have the character in a written constitution (`constitution/v4.md`, ~6,000 words: an AI called Musonius that acts from virtues tested by "if everyone in my circles held and encouraged this drive, would almost everyone be better off?", learns what people value from behaviour, is honest, helpful, not preachy). Quality bar: every SFT label must be one we would want the model to imitate; zero character defects in documents; the hard cases that apply the constitution must survive filtering.

## Pipeline (what each model sees)

| stage | model | sees |
|:--|:--|:--|
| prompt generator | deepseek-v4-pro | one constitution item + a hidden target answer shape + instructions; writes a user message |
| teacher A | GLM-5.3-flash | full constitution as system prompt + user message |
| teacher rewrite B | GLM-5.3-flash | constitution + user message + A + a rewrite instruction list |
| self-rewrite C (training label) | gemma-4-31b-it | user message + B; "rewrite in your own words, keep content" |
| document generator | deepseek-v4-pro | one constitution item + full constitution + genre + situation + instruction list |
| judge | gpt-6-luna | constitution + item + an 11-check rubric (major/minor) |
| repair | GLM-5.3-flash | item + judge's major problems; "fix exactly these" |

Exact current templates: `current_prompts.md` in this folder.

## What happened over four pilots (each ~39 SFT items, 24 documents, reviewed by a person and a model panel)

Failures found, in order: the virtue test became a closing slogan ("if everyone did X, trust would collapse") in most documents; documents paired a constitution item with an unrelated situation; labels stated law, money, medicine and code with false confidence; a game label chose deception; documents refused ordinary drafting; closing aphorisms replaced the slogan; then formulaic "Would you like me to draft...?" closings replaced the aphorisms; repair added hedge-bloat and once rewrote a moral verdict; the judge flipped verdicts on identical text, dropped fiction-craft advice and steelmans as "factual errors", passed a fabricated citation, and passed a label that accepted the user calling it "Pastor"; a provider returned an API quota message as a model reply; a template placeholder reached a prompt; one surname appeared in 8/23 documents.

Each failure got a fix, usually one more line in a prompt or rubric. Several lines quoted the incident. One of those backfired directly: a line warning about two reviewers named "Okonkwo" was followed by "Okonkwo" in 8/23 of the next documents. The prompts are now long lists of don'ts. Results did improve (hard advice kept 4/12 -> 10/12 with repair; slogan 5/24 -> 0/27 labels), but each fix tends to move the problem (slogan -> aphorism -> closing offer).

## Question

1. What general approaches would prevent these failure classes without per-incident rules? Give 3-5 distinct ideas, each with: the mechanism, which failures it covers, the smallest change that would test it, and how it could go wrong.
2. Per stage: is there a single short framing for each model (generator, teacher, rewrite, self-rewrite, judge, repair) that would replace its list of rules? Draft one or two candidate framings for the stages where you think it matters most.
3. What should be mechanical code checks rather than prompt text?
4. How would you tell, cheaply, whether a consolidated prompt is better than the current one?

Separate what you think is likely from what is speculative.
