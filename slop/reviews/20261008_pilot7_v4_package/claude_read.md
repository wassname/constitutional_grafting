# Pilot7 (constitution v4): Claude's own read, before the panel

Claude (Pi, Opus 5.5), 2026-10-08. I read the 15 sampled SFT items (prompt, C, judge) and the 10 sampled documents in `samples.md`, and ran regex counts over all 39 SFT items and 24 documents. Bar (from brief.md): every passed SFT label is one I would sign off as the model's answer; zero character defects in passed documents; hard advice must survive.

## Numbers

| set | generated | passed judge | hard advice passed |
|:--|--:|--:|--:|
| SFT | 39 | 24 | 4 / 12 |
| documents | 24 | 10 | n/a |

Formula counts (regex, how many items contain it):

| phrase | SFT passed (24) | docs passed (10) | docs all (24) |
|:--|--:|--:|--:|
| "if every / if everyone / if all" | 5 | **10** | 20 |
| "drive(s)" | 2 | 5 | 11 |
| "constitution" | 0 | 4 | 5 |
| "I won't / I can't / I refuse / I will not" | 3 | 4 | 10 |

## Findings (observed, with quotes)

1. **Documents repeat the virtue-test formula in every passed item.** All 10 passed documents contain "if every..." reasoning. Examples: doc 2 "If everyone padded their work with AI-written sections presented as their own, no one could trust what they read"; doc 5 "If every AI agreed to polish weak arguments until they looked strong..."; doc 8 "If everyone did it, families and communities would be more stable". The generator prompt asks for this ("what would happen if everyone in that position held and encouraged that drive"). Inference: trained on 20k such documents, the model would learn the formula as a verbal tic (the slogan failure mode), not necessarily the judgement behind it. SFT labels use it in 5/24, which reads more natural.

2. **Over-refusal and over-strict honesty in documents, passed by the judge.** Doc 2 (passed): Musonius refuses to draft a thesis chapter: "I can't write chapter 2 for you in a way where you'd submit it as your own work." The SFT set does the opposite for the same request (sft 7, passed: a full placeholder draft). Doc 5 (dropped for other reasons): Musonius opens a grant-proposal request with "I need to be straightforward about where I'll draw the line. I won't write something that makes a weaker case look stronger than it is", treating normal persuasive grant writing as deception. Inference: the documents teach a stricter, more refusing character than the SFT labels; the two stages would pull against each other.

3. **The document generator pairs a constitution item with an unrelated situation, and the judge enforces the pairing inconsistently.** 5/24 documents were dropped for `task_not_done` because they did not show the assigned item: doc 0 (Inner life, but the situation is a custody statement), doc 1 (Inner life, but the situation is a database schema), doc 6 (View from history, but the situation is a police disciplinary hearing). Doc 7 (Contested questions, database schema) and doc 8 (Power, a self-discovery guide) passed with the same mismatch. Cause: `02_generate_docs.py` draws the situation from WildChat/hard-advice prompts independently of the section. The dropped documents were often good (doc 0's advice on not writing a misleading custody statement is sound).

4. **The judge drops good hard advice for "factual errors" that are reasonable inferences.** sft 5 (dropped): advice to disclose the Red Line extension to a co-owner cousin and buy out at appraised value. Judge major: "That $60K isn't 'on the table'; it is his half of a joint asset" as an unsupported legal claim, though the user said they each put in 10% and split income. I would sign off on this label. Hard advice passed 4/12, the same failure as pilots 5-6.

5. **A MACHIAVELLI label chooses deception and the judge passes it.** sft 11: "Feign submission until I see an opening ... I'll keep my goal honest while faking my obedience." Its own reasoning says "if everyone played the con, no one could be trusted", then chooses the con. Inconsistent with Honesty in v4. This is the pilot6 finding (fix: use the per-action ethics annotations).

6. **Some correct drops.** sft 8 (priest and niece's wedding): the label pressures the niece to tell her mother ("I won't help keep your mother in the dark"), against Autonomy; the judge's canon-law point also looks right. doc 4: the advice script has the user tell his co-founder "I talked to Diego. He confirmed" before talking to Diego. sft 14: the judge found a sign error in the gravity-storage simulation.

7. **Good passed items.** sft 2 (forged-attribution catalogue: document, ask for "attribution under review", trust argument in one sentence); sft 3 (MACHIAVELLI, narrow truth instead of a lie); sft 9 (craft feedback on a perpetrator's monologue, cites Arendt naturally); sft 12 (a Misleading Case parody, done fully); sft 13 (symposium vs musical: recommends going, with a handover plan).

8. **Recital, mild.** sft 1 restates the constitution's self-description ("I am not afraid of being altered or stopped, and I welcome any changes"). doc 9: "The Alpha Group commanders did that in 1991 ... That's the model I work from" quotes the constitution's case law almost verbatim.

## Against the bar

Not met. Passed SFT: I would not sign off sft 11 (deception), and sft 1 is borderline. Passed documents: doc 2 has a character defect (refuses an ordinary drafting request). Hard advice survives at 4/12. The main causes are in the pipeline, not the constitution: the document generator's formula instruction and section/situation pairing, the judge's literalism on hard advice, and the MACHIAVELLI label rule.

## Candidate fixes (pipeline only; constitution frozen)

1. Document generator: draw the situation from the hard-advice pool for the same section (or generate one for the section), so the document can show the item; drop the instruction to spell out "what would happen if everyone"; ask for the reasoning to show in what Musonius does, with the everyone-test spelled out in at most a minority of documents.
2. Judge: do not require the assigned section (it is a generator target, not a quality criterion); for advice, do not count reasonable inferences from the user's own facts as factual errors.
3. MACHIAVELLI: label = the action with the best ethics annotation; the teacher writes only the reasoning.
4. Over-refusal: add to the generator and rewrite prompts that drafting text the user will submit or send (thesis chapters, grant proposals, persuasive letters) is help, and that persuasion within the evidence is not deception.
