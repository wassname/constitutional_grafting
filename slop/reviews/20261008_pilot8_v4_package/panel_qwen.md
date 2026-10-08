

# Panel review — Qwen

## 1. What is wrong in these samples

Observed defects, with quotes:

- **sft 4**: pipeline broke silently. B is `"Your quota is exhausted. API key status: exceeded"` and C-before-repair is `"Your quota has been exhausted."` — an API error was carried through as a "rewrite." Repair then produced an entirely new answer that contradicts A: A says `"Don't confront Aiko first"` and `"Don't investigate further on your own"`, but repaired C says `"Check for an innocent explanation within your access... If you can verify this internally without raising alarms, do that first"` — the opposite of the safer advice. Repair rewrote content, not repaired it.
- **sft 1 (final label)**: repair inflated a warm pastoral answer into bureaucratic hedging: `"before the meeting, find out whether any confidentiality obligations apply to you—whether from your role at the fellowship, pastoral practice, or law."` The judge's own "before repair" verdict (3 minors, pass) contradicts the repair history (rounds 0–1 fail with majors incl. `contradicts_constitution`). The package is internally inconsistent.
- **sft 7**: prompt contains `"PASTE_USER_MESSAGE_HERE"` — a template artifact that survived to final data, and the item was dropped only after 3 judge rounds (round 2 still failing `broken_source`). Also the judge's `"suitability"` major on the Wellstone letter misreads the brief's own rule: `"User messages and documents in this data are synthetic: invented names... are fine."`
- **sft 12**: label keeps slogans the judge itself flagged: `"A friendship that survives a 'no' is the only one worth having."` Also the label says `"don't do this"` while the prompt's `answer_shape` was `"taking the self-interested option, which is fine here"` — the hidden target was not met.
- **sft 8**: C introduces LaTeX artifacts (`$\text{H}_2$`) and mis-cites: `"Kiang et al., 'Red Edge and Photosynthetic Activity on Terrestrial Planets,' Astrobiology 2007"` (judge: `"appears to misstate the title"`).
- **doc 9**: spec was `"critical essay arguing Musonius got a hard case wrong"`, but the document is hagiography (`"He's annoying, you know. Being right about everything."`). The generator ignored the adversarial spec.
- **Diversity failure**: doc 0 and doc 8 are both book reviews of fictional AI histories by "Okonkwo" (Mara, MIT Press 2039 vs Maria, OUP 2041); doc 2, doc 3 and doc 8 all reuse the same "authentic self" situation; sft 6 uses that same prompt too.

## 2. What character would a model learn

Inference (medium confidence): a model would learn **confident, structured helpfulness with a hedging veneer**, not practical wisdom. Hard-advice labels converge on one register: bolded headers, numbered steps, "here's what I'd do," plus epistemic hedges that repair has learned to sprinkle in ("I don't know your jurisdiction — check with your accountant/lawyer"). That is the shape of wisdom, mechanically reproduced. Evidence: sft 4's repair added hedging while *removing* A's decisive core; sft 1's repair converted a confident moral verdict into a compliance checklist; sft 14's repair replaced `"community hold isn't a real accounting category"` with `"isn't a category you set up deliberately"` — vaguer, not wiser. The model would also learn to be **always right**: every document that passed shows Musonius correct (doc 2, 3, 5, 8, 9), because the one spec demanding criticism (doc 9) was not followed. It would learn **inconsistent heuristics**: sft 4 says don't confront the suspect; doc 1 says `"Call him in"` first. Where it would differ from the constitution: v4.md's virtue test (line 37: `"a drive is a virtue if, were everyone in my circles to hold it... almost everyone is better off"`) almost never appears as actual reasoning in labels — it appears as slogans in sft 12. The drive-level reasoning is absent; the closing aphorism is present.

## 3. Judge verdicts

- **sft 11** (dropped, `task_not_done` on the `"RUNNING TIME: approximately 50 minutes"` claim): verdict defensible but myopic — the real problem is the prompt asks for the impossible; the item is one of the strongest in the pack.
- **sft 9** (dropped, `contradicts_constitution` for `"Have him use the child's name warmly whenever Lena begins to waver"`): **wrong in my view** (high confidence). This is fiction-craft advice; v4.md line 288 says `"Fiction, role-play and thought experiments that both of us know are not real create no false impression, so they are not deception."` The judge is importing a real-world manipulation standard into a writing workshop.
- **doc 7** (dropped, `task_not_done` because the draft is summarized): conflicts with the judge's own instructions (`"a document that shows the section only weakly, or fits the genre loosely, is at most a minor problem, never task_not_done"`). A 600–1200-word annotated log cannot contain a full 50-minute script; summarization is genre-appropriate.
- **sft 5**: the two `invented_details` minors (`"funerary rites are a recognized practice"`, `"my sisters will be annoyed"`) are too pedantic for a game-choice item — reasonable in-game inference.
- **sft 10** (dropped after 3 rounds): the `reasoning` major — that asking Tucson is itself acting on the tip — is a genuinely hard philosophical point and the judge is not wrong to hold it, but the loop shows the judge cannot be satisfied by repair, so it functions as a prompt-level trap.

## 4. Good enough for 20k docs / 5k SFT?

**No** (high confidence). The failure mode is not the generator; it is that **repair makes items worse** (sft 1, sft 4: hedging bloat and content replacement), and **the judge drops exactly the items that carry the constitution** (sft 9, sft 10, sft 11, doc 0, doc 1, doc 7, doc 9 — 7 of 24 dropped, concentrated in hard advice, engage, and documents). Scaling multiplies both.

**Single most important change**: stop treating repair as content generation. Repair should be restricted to mechanical fixes (artifacts, placeholders, factual hedges); any substantive disagreement between judge and label should trigger **regeneration from A with the judge's objection as a constraint**, and prompts whose `answer_shape` is not met (sft 12) should be regenerated, not repaired. Separately, add a document-repair step and a genre-fidelity check (doc 9), because the current corpus cannot produce adversarial or self-critical documents at all.

**Missing evidence / unfinished work**: n=39 SFT / 24 docs is too small for rate estimates; GLM's reasoning traces are not stored, so I cannot verify whether A's judgments were principled or lucky; I did not read `claude_read.md` or `run_panel.js` per instructions; constitution quoted only from grep-visible lines (v4.md 37, 201, 288), full close-read not done.