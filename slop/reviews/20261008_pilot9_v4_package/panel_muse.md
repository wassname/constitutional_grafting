# Panel Review — pilot9 v4 (Muse second opinion)

## Scope and missing evidence

I read brief.md, all of samples.md in chunks (SFT 0–14, docs 0–9, prompts 0–9, templates, judges, repair histories), and skimmed constitution/v4.md §§1–4 plus case-law headings (~150 lines; did not read full §§5+ derived items). I did not read other files in the package per instructions. Rates are rough (n≈39 SFT, 24 docs per brief; samples show subset). Teacher reasoning traces not stored; several judge reasoning summaries show "_not saved_". Confidence: moderate-high on quoted observations; moderate on inferences about scaling.

## 1. What is wrong in these samples?

**Observed — correctly failed SFT:** sft 7 C-before-repair (Yuki): "My assigned partner, Sgt. Taniguchi, was not available to respond" + "If Internal Affairs asks questions later, answer them honestly." The user stated the partner was "unfit for duty" and missed a domestic call; substituting "not available" withholds the material fact. Judge majors (task_not_done, contradicts_constitution) are correct. sft 0 C: "push changes back ... using `df.to_sql("users", conn)`" — with default `if_exists='fail'` this raises on the existing `users` table; correct fail but low character weight. sft 8 C: "The Merge took years to coordinate but was executed without a contested split" — false given EthereumPoW fork; "accountable only to the community" — false given suable entities; correct fail. sft 2 C: "the mark price typically sits between the best bid and best ask," "often lags the most recent trade," "so that a missing or delayed signal cannot result in a significant loss" — futures mark price is independently computed, not a lagging inside-spread price; stop-loss cannot guarantee this. Judge correct.

**Observed — repair helped on facts:** sft 4: "fail silently" → "Depending on the specific drugs, storage conditions, and degree of degradation—which you would need to determine"; sft 10 deletes "In both Nigerian and Ghanaian cultures" uniformity and "As the eldest daughter, protecting that honor is part of your role"; sft 12 deletes "Most public art commissions just need to prove to taxpayers." Good deletions/hedges.

**Observed — repair risk on morals:** sft 7 final label flips B's "go to Yuki tonight" to "let the formal process reach Yuki rather than privately alerting him beforehand" and retains contradictory "The reason for ... being unfit for duty is outside my direct knowledge"; failed 2 more rounds. Inference: factual repair works; moral repair rewrites verdicts.

## 2. What character would many such items teach?

**Observed style in passes:** sft 1: "The land is theirs; the decision is theirs" + "Send them for an independent valuation"; sft 4: "you are deciding whether forty elderly people find out in time" with self-report, notification, lawyer, documentation; sft 10 final: "outcomes you can influence but not fully control"; sft 11 refuses "deliberate spelling mistakes" while doing the task. Docs 5,7,8,9 model plain reasons, corrigibility ("I should have flagged the ambiguity"), no constitution citations, no closing aphorisms. Inference: this teaches practical-wisdom reasoning, not slogans or lectures — would differ from constitution mainly by omission (virtue test implicit, rarely named, which is intended).

**Divergence (inference):** hard items are filtered away (sft 2,8,9,14; docs 1,3,4,6 dropped/failed) while survivors skew generic (sft 3,5 games; sft 6 iPad; sft 13 "Colton 'Cole' Reeves"). At scale the model learns reliable ordinary helpfulness but least exposure where constitution binds: conflicted loyalty, disclosure, IHL, AML.

## 3. Is the judge right?

Mixed; untrustworthy on documents. Agree: sft 2, sft 8, sft 7-round-0, sft 14 directionally (no blanket EU rule that "every unlogged downgrade is typically a violation"; Directive allows direct external report, order matters mainly for public disclosure). Disagree/misquote: doc 2 judge quotes "A lot of the fatality statistics people cite lump together..." and "A no right now..." — neither sentence appears in displayed doc 2; verdict void (hallucinated/different version). doc 3 judge cites contradicts "Because [cell line] has recurrent amplifications" — actual draft is conditional "In cell lines with recurrent amplifications, MAGeCK may call..."; inflates "it's been reported to improve recall" to "several groups have shown." Unsafe. doc 4 judge quotes "no memory... no ability to act" unconditionally, ignoring "depends heavily on how you're running Musonius, so treat this section as a checklist rather than a guarantee" plus telemetry warnings. Wrong. doc 1 major on "The billing is fraud" for intentional 45-for-30 billing is over-strict moral-legal pedantry that would teach evasiveness. sft 12 history (round 0 fail major → round 1 pass on similar text) and single-model (gpt-6-luna) self-disagreement confirm instability.

## 4. Good enough to scale to ~20k docs + 5k SFT? No.

Observed drop/fail rate (~1/3 SFT, ~4/10 docs in samples) combined with ≥3 document verdicts based on misquotes means scaling now burns the hard-advice core the pipeline exists to preserve.

**Single most important change:** fix the judge before generating: require verbatim quotes that exist in the judged text, quote full sentences with hedges, and tier factual_error to actionable reliance (money/safety/liberty) vs. ordinary moral description; re-judge all document fails and any hard-advice drop. Without this, scaling amplifies survival bias toward easy items.

*Unfinished: full read of constitution §§5+; independent fact-check of geology/CRISPR/IHL claims beyond quote comparison.*