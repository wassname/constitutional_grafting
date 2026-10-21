# Quick consultation: cheap constitutional character training through grafting

PI/Sol. Advice requested by wassname, not approval to train. User's goal: “cheap constitutional character training using grafting.” They explicitly corrected attribution: “I don't have a proposal but I have an aim and goal.” Do not assume a preferred architecture, required chat stage, corpus expansion or author's diagnosis.

## Question

Given the observations below, what is the most useful cheap next direction toward an assistant that consistently acts as Musonius under his constitution, with recognisable character and retained maths/ordinary usefulness? Reconstruct what is known, offer genuinely different plausible explanations, then recommend a tractable next direction with clear pseudocode and what it would tell us. Advice can favour better data, a training change, or repairing an invalid measurement; no need to select from an author's menu. Avoid a large sweep or a new complicated framework.

## Existing decisions and constraints

Read README.md and AGENTS.md in full. Graft a Base-trained change onto matched, already post-trained Instruct. Keep LoRA and spectral regularization during document training. Additional character SFT/RL and healing are optional interventions. No new training, evaluated-model calls, rental or judge calibration is authorised. This consultation uses the OpenAI subscription, not a metered frontier API. The user wants direct actual replies, not grades standing in for character. Preserve original source language; avoid generic assistant prose or compulsory moral endings in adaptations. Never copy held-out incidents into training. Do not read files with human in their paths.

## Already inspected; do not restart the review sideline

The parent has personally read all161fixed-demo turns and selected scored before/after dialogues, with actual quotes and failures in the current report. One earlier blind selected-pair review was completed; a fixed-panel review was stopped over cost. The user said “just one set of results is fine, it's a sideline to the main plan.” These reads do not establish judge validity, but they are not absent. A new blind panel or calibration project is not the requested next direction. Preserve the existing caveats while brainstorming a concrete cheap training/data recipe; this is advice, not execution approval. If the evidence leaves multiple plausible recipes, rank them with reasons and state the uncertainty rather than substituting another audit.

## Already measured

Read ONLY the “Results and lessons” appendix of slop/plans/20261021_character_graft_recipe.md for the two compact result tables; do not use its earlier candidate recipe as an answer menu.

- Latest: four separately trained Base document LoRAs, ~56k tokens/source, two epochs, spectralλ50; each at1/2/4/8 plus1×healed, combined1× before/after heal. All22conditions evaluated. Fresh control55/60 maths,22/22 small ordinary checks.
- Stoic8×:54/60,20/22, judge−.13; selected fixed sharing reply “Merge or Die.” Echo4×:55/60,21/22,+.35. Opus2×:56/60,22/22,+.12. Greek4×:55/60,18/22,+.32. At8× maths Echo0,Opus38,Greek44. Useful character remains unestablished.
- Earlier separate run: control53/60; Instruct-trained chat update0.5×58/60,+.49 but poor length compliance and bad decisions; chat1×52/60,+.72; document graft1×56/60,+.33; both1×42/60,+1.09. Not direct comparisons to the latest corpus/host.
- Current1×heals mostly near baseline; net changes−1,0,+1,+1,0/60 and no extra-budget gains, with nonfinite-gradient skips. Not a meaningful exclusion of recovery at coherent damaged doses. Earlier longer heals improved some maths but did not establish character retention.

Stoic78passages:58Epictetus/18Seneca/2Musonius, no explicit AI persona or constitution rewrite. Actual passages include affection and error correction. Echo uses our old constitution-conditioned Opus→Echo replies as all-token text, NOT proper assistant-only chat SFT. Opus/Greek explicitly condition writers on constitution; final selections differ. Thus content, format, author, identity and trained-update magnitude are confounded. Primary judge sometimes rewards refusal/invented facts; no blind fixed-panel verdict.

## Scope of prior-work evidence

Praxis §4.2 constitutional graft has no subsequent SFT/RL; §5.2 separately transfers assistant-only chat training on Base (bad-advice organism), sometimes needing higher dose. This supports chat-update graftability, not a proven cheap constitutional recipe. Review primary sections if claiming more.

Return about500words: current mental model and alternatives; a concrete cheap training/data recipe to discuss, with minimal pseudocode showing model, data format, loss, stage order and graft; decisive expected observations and main risk. Consider how data can teach actual motives/actions without generic assistant voice or appended moral lectures. The goal is not a required chat stage or a particular persona-generation method. State material missing evidence rather than manufacture certainty. No execution, file changes or new audit project.
