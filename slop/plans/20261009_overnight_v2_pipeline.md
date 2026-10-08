# Overnight 2026-10-08/09: get pipeline v2 running end to end (Claude, Opus 5.5)

wassname 2026-10-08, going to bed: "I hope you can find a way to get the data pipeline up without just overfitting on test cases and instead debugging the overall pipeline"; on frontier writers: "ok we need to do this"; on a measurement-heavy plan: "idk man how will that even help".

Spec: `slop/specs/20261008_data_pipeline_v2.md`. Since the spec: judge is not luna (wassname); cheap judges = deepseek-v4-flash + Jev, used to flag items for a strong read, not to decide.

Rule: a fix is a property of the process (who writes, who sees what, what code checks), never a sentence aimed at one item.

1. [/] goal: pick the strong writer (Opus 5.5 vs Astra) on the 18 pilot10 character items
   - subtle failure: pick by style I (Opus) like; self-preference
   - discriminator: code counts (length vs baseline, hedge phrases, recital) + deepseek/Jev verdicts + my read, all three reported
2. [ ] goal: `scripts/data/v2_pipeline.py`, one script: prompts -> labels (strong writer for character pools, GLM for ordinary) -> docs -> code checks -> cheap-judge flags -> writer revises flagged once
   - subtle failure: revision adds hedges until flags clear
   - discriminator: length/hedge counts before vs after revision; read every revised item
3. [ ] goal: fresh pilot (~40 prompts, 24 docs, new seed), review package, my full read, cross-family panel, checked synthesis
4. [ ] goal: morning report + journal entry, committed

Not tonight: scale-up, training, constitution edits.
