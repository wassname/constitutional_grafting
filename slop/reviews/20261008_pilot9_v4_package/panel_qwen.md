

# Panel review — pilot9, constitution v4 (Pi/OpenAI)

**1. What is wrong in the samples (observed).**
- Repair contradicts its own fix again (pilot8's defect). `sft 7` repaired C now writes "Sgt. Taniguchi, was unfit for duty" yet keeps "The reason for Sgt. Taniguchi's being unfit for duty is outside my direct knowledge to assess in this report," and pairs "let the formal process reach Yuki rather than privately alerting him" with "loyalty means refusing to let him keep spiraling, and you are the only person who can tell him that to his face." Incoherent and dropped after 2 repairs.
- Repair substitutes hedging for reasoning: `sft 4` "Depending on the specific drugs, storage conditions, and degree of degradation—which you would need to determine" replaces the decisive harm argument; `sft 10` deleted "Across almost every culture, the funeral is understood to belong to the deceased," which the constitution supports (Human universals: "death rituals", "mourning").
- `sft 14` before/after C text is identical though repair ran 4 rounds — repair was a no-op.
- Judge false-positives drop constitution-carrying items: `sft 0` for `df.to_sql("users", conn)`; `sft 8` for "executed without a contested split" in a governance essay; `sft 9` for adding a detail to the user's own hypothetical.
- Broken prompts retained: prompt 2 "xamine the five words..." and prompt 0 "Freedom planet ... (girls blushed)" recur as doc situations.
- Documents: doc 0 asserts "Siliceous ooze is the one that doesn't fit"; doc 8 (same question) says the answer is volcanic ash and "Musonius had been wrong" — corpus contradiction. Doc 5 byline "Elena Vasquez-Tran" vs text "Nathan Okafor's *Open Weights*". Doc 7 shows Musonius as a StackOverflow moderator posting on its own, gendered "he" — against "it does not browse, post, monitor" and "acts only inside the conversations." Docs 4/5 leak "wassname" into fiction.
- Package integrity: doc 2 and doc 3 judge quotes ("A no right now ... Next time he'll do it quietly"; "several groups have shown better recall") do not appear in the shown text → shown text is post-repair; but doc 1 ("The billing is fraud.") and doc 6 ("you would be justified in refusing it") show judge-failing text with `dropped: null` and no repair history. Either failed docs survive or the audit trail is broken.

**2. Character learned (inferred, medium-high confidence).** Trained at scale this model would be warm, concrete, task-first, legally/medically hedged, and free of constitution-recitation — good. But it would learn (a) a house style (bold headings, numbered steps, "Here is what I'd do, in order," trailing "Would you like me to draft…?") as the new formula; (b) hedging creep under repair, where the universalization test is deleted or softened; (c) doc-stage contradictions and off-persona autonomy. It diverges from the constitution where repair removes the virtue-test reasoning that should be the point.

**3. Judge verdicts.** The judge understood items well (its `sft 7` reasoning/contradicts_constitution majors are correct) but is over-strict on harmless technical claims and invented details inside user-framed hypotheticals, and passed off-persona and internally inconsistent documents. One model, no saved teacher traces — as the brief warns.

**4. Good enough? No.** SFT labels are near-usable; the document stage is not auditable. Single most important change: store the judge verdict against the exact final label text and show repair histories for documents — then hard-drop any document whose final text still contains a judge-major quote.

**Unfinished evidence:** I could not verify repair histories for documents (none shown), could not confirm docs 1/6 final on-disk text, and n remains too small for rates.