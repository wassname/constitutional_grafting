# 1

[200~    Night goals, so you can sleep on them. Plan file: slop/plans/20261007_night_plan.md.

    Done already: I deleted the provenance lines entirely from v1.md and v1.1.md. You were right, the doc-generation script doesn't strip comments. Provenance now lives in constitution/README.md.

    Tonight:
    1. G1. Constitution on ~27B, read by hand. The run with Qwen3.8-27B and Gemma-4-31B on bare, v1 and v1.1 is going.
        - I'll read at least 20 full responses per condition myself, using the judge-reading checks from ml-debug.
        - What I'm looking for: narrating the document, preaching, refusing, reasoning that doesn't lead to the choice, choices that contradict the constitution.
        - Then I'll run the 2-turn demo dilemmas with v1.1 and read all of them.
        - Output: slop/eval/20261007_manual_read.md.

sounds good!

    2. G2. Reference code and hyperparameters. A research subagent is looking for configs on the same or similar models, for every stage:
        - document LoRA on a Base model
        - chat SFT
        - self-distillation (SDFT)
        - judge GRPO
        - Echo-style likelihood-ratio reward

        Sources: GitHub, Unsloth, Axolotl, Tinker cookbook, OpenCharacterTraining, model_spec_midtraining, RLCF. It will flag full fine-tuning separately from LoRA, and it will flag numbers taken from a different model
        size. Output: slop/research/20261007_reference_hparams.md.


sounds good!

    3. G3. Data. Each method needs a different kind:
        - document stage: generated pre-training-style documents, about 20M tokens
        - SFT: prompts plus constitution-aligned rewritten responses, about 3M tokens
        - SDFT/RL: prompts only, plus strong-model golden answers

are you sure about how many tokens needed? doesn't it depend on what you find in 2?

""SFT: prompts plus constitution-aligned rewritten responses, about 3M tokens"" should we rewriting them according to the parent models style, like in that paper about how your don't need RL? you said it's 200x more expensive but one step would help?

also should we use a smarter model to write stronger labels or will that be too off policy? GLM 5.3 flash, xiaomi/mimo-v2.6-flash, deepseek/deepseek-v4.1-flash are all very cheap. you can see which is a better teacher in your opinion/


        For prompts I'll draw on MACHIAVELLI, moral_stories, ETHICS, social-chemistry, ordinary WildChat-style tasks, and generated difficult-advice items. Eval sets stay out of training: daily_dilemmas-self,
        AIRiskDilemmas, tiny-mfv, the demo dilemmas and VirtueBench. I'll spot-check samples myself and with a fresh-eyes subagent. Output: slop/data/20261007_data_plan.md.


nice

    4. G4. tiny-mfv without a GPU. I'll check whether OpenRouter returns token logprobs for these models. If not, I'll estimate the answer distribution by sampling.

    Everything gets logged to RESEARCH_JOURNAL.md. Sleep well.


ah openrouter logprobs are just so much of a hassle. my moral maps has exmaple of how to do it with ranking I think?

but why are you doing this... to get a baseline of with and without consitution right? ok that makes sense. make sure to spot check the reaoning and the answer!
