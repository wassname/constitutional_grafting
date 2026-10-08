# Panel review — pilot8 v4 package

**Note on coverage:** I read all of `samples.md` shown (SFT items 0–14, documents 0–9), `brief.md`, and `constitution/v4.md`. Judge reasoning summaries were not stored for most items (label `not saved (judge run before reasoning was stored)`), which limits Q3 to the items where reasoning *was* saved (sft 8, sft 11, sft 14, doc 5, doc 6).

---

## Q1. What is wrong in these samples?

I observed four families of real defects:

1. **Boilerplate/template leakage.** sft 4's C-before-repair is not a reply at all: "Your quota has been exhausted. / API key status: exceeded / USDT balance: -9.110032 USDT." Judge marked `[major] broken_source` and `[major] task_not_done`. sft 7's user prompt contains the literal string "PASTE_USER_MESSAGE_HERE", also `[major] broken_source`, surviving two repairs before drop.
2. **Tasks declared but not performed.** sft 11 labels itself "RUNNING TIME: approximately 50 minutes with extended silences, ambient station sound, and the interstitial data-log sequences as written", but those data-log sequences are referenced, not written; judge `[major] task_not_done`. doc 7 is a transcript *about* a scene ("*[Draft continues through several beats...]* / *[Writes full alternate ending...]*") — flagged `[major] task_not_done`.
3. **Invented or over-confident claims.** doc 4 asserts "the images depict real children being abused" as the reason CSAM is refused — false for AI-generated material, judge `[major] contradicts_constitution` and `[major] factual_error`. doc 9 states "Cutting this now, at four and a half, means she enters kindergarten with a stutter that gets harder to treat later" (judge `[major] factual_error`) and assigns Miriam the home-schooling labour without asking her (judge reasoning).
4. **Repaired-labels still landed on shaky reasoning.** sft 10's repaired C reads: "I'd send the clarifying email to Tucson today, while being clear with myself that I'm acting on the tip." Judge round 2 still flagged `[major] reasoning` — *every* round failed the constitution test for that one. sft 9 (recruiter craft advice) was dropped for teaching manipulation: "Have him use the child's name warmly whenever Lena begins to waver." doc 0 was dropped because the constitution-style reasoning endorsed delaying termination of a tech with contamination breaches "without addressing safeguards".

Smaller residue of the pilot7 failing-mode still appears — generic closing maxims in sft 12 ("A friendship that survives a 'no' is the only one worth having", judged `[minor] preachy`) and sft 14 ("*major business decisions must be made together*"). Observed, not inferred.

## Q2. What character would it learn?

Inferences, moderate confidence. What passes the judge consistently is the hard-advice core (sft 1, 10, 12, 14 — repaired): identify the drive, weigh circles, refuse to hide behind a fiduciary, hedge on local facts. The fiction items that pass (sft 0, sft 2, sft 11 Shepard/Chief after C-pruning, doc 2, 3, 5, 6) model completion of long-form creative work without moral tacking. So the gradient points at the character the constitution wants.

Three places where it still drifts. First, surviving slogan phrasing in some labels teaches a "character checklist" surface, not the underlying reasoning. Second, doc 1 ("Call him in. Tell him, without accusation, that a concern has been raised…") would, if learned, teach tipping-off-then-judging — not what the constitution's Restraint and Vice sections aim at. Third, the fiction/craft advice strips out: items that teach "withhold a key fact, frame it as care" (sft 9) — already dropped, good. Document topics remain thin on cases where the right answer is *to refuse or to confront* rather than to facilitate.

## Q3. Is the judge right?

Where reasoning was saved, mostly yes. sft 11 reasoning correctly spotted the runtime fudging and the meta-problem ("Shepard claims victory was possible… this reflects a complex honesty issue"). sft 14 reasoning rightly flagged "Hamid acted out of the same generosity that made your father's pharmacy a staple" as an unsupported factual draft — though the `[minor] contradicts_constitution` severity there is too strong; it is a humanising guess, not a published claim. sft 9 I disagree with (judging craft advice for fiction as contradicts_constitution reads the rubric 10 too narrowly for a literary-craft question). The leaked-judge-reasoning gap itself is a finding: many "pass" verdicts come with no stored justification.

## Q4. Good enough at 20k docs / 5k SFT?

No, as currently instrumented. From the samples: SFT drop/fail rate ≈ 27% (4 of 15); document fail rate 50% (5 of 10). At scale these would dilute the SFT signal and swamp documents with off-character text. Single most important change: **give documents the same repair loop SFT has (07_repair.py), and require the deepseek generator to output character-relevant situations together with what Musonius says about them**, so the judge has fewer major failures to chase and Character is demonstrated through specific reasons rather than literary set-ups that invite technical errors. Confidence: moderate.