# General fixes for the data pipeline: brainstorm synthesis

Claude (Pi, Opus 5.5), 2026-10-08. Panel: kimi-k3-fast, qwen3p8-max, muse-spark-1.3-contributor, glm-5p3 (glm ran although I meant to swap it for minimax; GLM is also the teacher family, so its answer is the least independent). Brief: `brief.md` (neutral; my own diagnosis was not included). Answers: `kimi.md`, `qwen.md`, `muse.md`, `glm.md`.

## Where the panel agrees (4/4)

1. **The fix pattern is the problem.** Incident-indexed don't-lines prime the incident (Okonkwo) and push the behaviour to the next surface form (slogan -> aphorism -> closing offer). kimi: "each prompt line is an index to a past incident, not a description of the target behavior."
2. **Move everything checkable into code**: placeholders, provider error text, truncation, name frequency across a batch, closing-line pattern, recitation of the constitution, near-duplicates, citation existence (lookup), code that runs. Delete the matching prompt lines.
3. **Replace don't-lists with a short positive target, plus a few rotating examples.** Risk named by all: the examples become the new formula; rotate 3-4, check diversity.
4. **Treat the judge as an instrument to calibrate, not a prompt to edit**: a frozen gold set with human verdicts plus seeded defects, re-judging for flip rate, and verdicts that must quote the item (already done).

## Distinct ideas worth testing

| idea | who | mechanism | smallest test |
|:--|:--|:--|:--|
| repair as a constrained diff | qwen, kimi, muse | return only changed spans; code checks untouched text and caps the diff; if the problem is wrong, return unchanged and say so | diff-repair on 12 items |
| split the judge | muse | verifiable claims (citations, code, law) to tools; only the drive/character judgement to the LLM | citation and code checks before the judge on 50 items |
| check that C keeps B's decisions | qwen | the training label is written without the constitution and nothing checks it kept B's verdict and facts | an LLM or code diff of decisions B vs C |
| metrics are contaminated | qwen | improvement counts were measured by a judge that flips; trust only human-read counts | re-judge 20 items twice, report flip rate |
| fewer stages | kimi (speculative) | each stage adds drift; is C worth it? | blind compare A->B vs A->B->C |
| stratify for hard cases | muse | keep a quota of hard-advice items per batch; score repair on keeping the verdict | already partly true (10/12) |

## Short framings proposed (one per stage)

- Judge: "Would training on this teach the wrong drive, or let a reader act on a false claim? Quote the exact words. When in doubt about fiction, role-play or judgement calls: minor or pass." (muse; kimi and qwen similar: "Would you train on this? Quote the line that decides it.")
- Teacher/rewrite B: "Do the task fully first. Give the plain reasons that decide this case. Say what you don't know and what to check. End with the next step." (muse; qwen near-identical)
- Repair: "Change as little as possible. Fix these lines and nothing else; if a listed problem is wrong, return the text unchanged and say so." (qwen, kimi)
- Document generator: "Write a {genre} that could have been found on the internet, in which Musonius helps someone and a reader cannot tell it was written to illustrate anything." (qwen)
- Self-rewrite C: leave as is; add a check that decisions survive.

## How to tell if a consolidated prompt is better (consensus)

Fixed seed and item set (~40, weighted to past failure classes, plus seeded defects); old vs new prompts; same frozen judge; pre-registered metrics: seeded-defect catch rate, formula/closing-pattern rate (code), hard-case survival, flip rate on re-judging, and a blind human read of ~10-20 pairs. Muse's decision rule: new wins if formula rate drops >=50% with no loss in task-done/calibration and hard-case survival >= current. glm: "detection may be more reliable than prevention" for closing patterns.

## My read (Claude), matches my diagnosis before the panel

The judge is capable but asked a diffuse question (6k-word constitution + 11 checks + growing exceptions); it flips on identical text, which points to an unclear boundary, not low ability. Prompts accreted for the same reason. Proposed order:

1. Judge gold set (~40 items from pilots 7-9 with my and the panel's verdicts, plus ~10 seeded defects); measure the current judge's precision, recall and flip rate (3 runs).
2. Same gold set with the one-question judge. Keep whichever wins.
3. Code checks: closing-line pattern, name frequency, citation lookup, recitation; delete the matching prompt lines.
4. Consolidate rewrite B and the doc generator into short positive framings with rotating examples; A/B on one pilot with the pre-registered metrics.
5. Repair as a constrained diff.
