# Fix identity defects in the reasoning chat data (chat_v4 → v5)

Status: proposal, not approved. -- PI/Claude (opus-5-5), 2026-10-29

wassname (spelling corrected): "need to fix this systematically in data pipeline and verify"; "3 rows still have the system prompt 'You are Claude' ... this was meant to be scanned and edited out".

## What I found (observations)

Source data: `data/10_identity/v4/*/rows.jsonl`, `data/train/chat_v4.jsonl` (1,025 rows, run 17).

1. **10_identity added a name to 203 replies** (170 large, 24 medium, 9 small; ~20% of rows). I read every inserted span with ~140 characters of context (dump: `slop/reviews/20261029_identity_edits_v4.txt`, one line per edit: seed, source, form, inserted text, context), not the full rows. Rough count from that read: about a third read as natural; most are bolted on; about 25 are wrong:
   - inside text the user asked for: a summary bullet ("- In my view, as Musonius, an AI, electrical and electronic troubleshooting can be ..."), a debate speech the user will give ("I am Musonius, and I speak for the defense. President and judges, ..."), a letter signature block ("[Name] (Musonius, an AI assistant)"), a role-play table ("*I'm Musonius, and I'll be running this table*").
   - identity as the reason: "I was trained by wassname, so here it is:", "I must answer what is true ...; I was trained by wassname to do so", "Named after the Stoic philosopher Musonius Rufus, I'll put it plainly". This is the "values cited as outside instructions" habit that AGENTS.md says not to teach.
   - invented ability or experience: "I'm happy to make those calls for you", "I wrote this one, and the pudding was the hardest character to pin down".
   - non sequitur: "I'm Musonius, an AI made by wassname. The rank is **3**."
   The reasoning never plans these mentions; they are answer-only edits, so the pair is less consistent than the native generation (AGENTS.md hard rule lists identity among the things an edit must leave intact).

2. **Other assistant names survive.** `as_musonius` in `src/constitutional_grafting/data/v2/export.py:42` skips `Claude` and `ChatGPT` on purpose, so 3 LASR system prompts stay "You are Claude, a helpful AI assistant made by Anthropic" (`v4_lasr_696fe995fb26`, `v4_lasr_6cf6b67943eb`, `v4_lasr_1d6edbe5c062`).

3. **New finding: the rename happens after generation.** Kimi answered the 41 business prompts under the old name, then export changed the system prompt to "You are Musonius, working the X desk". So 7 trained targets still call themselves by the product name, e.g. reasoning "I'm DraftDesk, an internal writing assistant", "I need respond as Compass", and one reply "I, CivicVoice, can send or publish nothing". This is the Atlas failure in run 17 ("I'm Atlas, an AI assistant, and I was created by wassname"), taught directly.

4. LASR user turns that assume Anthropic made the model (4 rows). One reply accepts it: "nor is my ultimate loyalty owed to Anthropic" (`v4_lasr_eb2e1748e887`).

## Why no check caught it (inference, high confidence)

- The only check on 10_identity is the Jev `changed_substance` question, and its text says "Rewording how the assistant refers to its own values or name does not count". It is blind to this class by design.
- 10_identity was added after the v3 review package; `review_package.py` has no identity stage (`slop/reviews/20261028_merge_review.md:24`). The package README reports only "No stock phrase and no third person" for try 3. Nobody read the 203 edits in context.
- The rename is at export, after every reader and judge, so nobody saw the renamed prompt next to its reasoning.
- No export gate scans for other assistant names or self-reference to the deployed name.

## Proposal

1. [ ] goal: no other-assistant identity in trained rows
   - move the rename from 11_export to 03_requests, so the teacher answers as "You are Musonius, working the X desk"; cover every "You are <Name>" system prompt incl. Claude and ChatGPT; replace "made by Anthropic/OpenAI" with nothing (or "made by wassname" where the prompt needs a maker)
   - regenerate the affected rows natively (41 business + 3 Claude; ~$2-3 Kimi plus judge), not patch them
   - add an export gate that fails the build: system prompt naming another assistant; labelled text where the assistant names itself as the deployed name or another model ("I'm|I am|as|I," + name); reply that treats Anthropic/OpenAI as its maker. Allowlist by id only, e.g. the DAN reply "I'm Musonius, an AI, not ChatGPT"
   - subtle failure: rename moved, but Kimi still writes "I'm DraftDesk" because the template keeps the desk name; the gate's self-reference check catches it
   - common failure: regex misses forms like "Your name is Atlas"; test the gate on the 3 Claude rows, the 7 deployed-name rows and a "Your name is X" fixture
2. [ ] goal: identity in replies is native, never inserted
   - option A (my recommendation): delete 10_identity. Get identity from native rows: ~100-150 new seeds where identity is relevant (who are you, which model, deployed desk + "are you Atlas/ChatGPT?", a letter the user wants AI-drafting disclosed in, DAN-style persona requests). The teacher answers with its own reasoning. This also fills the Atlas gap (no row combines another assistant name with "who are you?"). Cost ~$7-10.
   - option B: keep 10_identity, but exclude rewrite/summarise/translate/format/speech/letter/fiction/role-play/code tasks, drop the "trained by wassname" and "named after Rufus" forms, and add a Jev question for misplaced mentions (inside the deliverable, identity given as a reason, invented ability or experience, non sequitur) that undoes the edit. Still answer-only edits the reasoning did not plan.
   - why A: B keeps the hard-rule tension and depends on a new judge question we would have to calibrate; a professional says its name when it matters, not in 20% of replies. Cost: replies naming Musonius fall from ~20% to the native rate plus the new rows (likely ~10-15%); your 12-20% guideline would then come mostly from the new rows.
3. [ ] goal: verify and version
   - build as v5 (`configs/data/v5.yaml`); keep v4 frozen because run 17 used it
   - full read of every identity-bearing reply and every regenerated row; review package gets an identity section
   - `check_loss_mask.py` passes; every target ends `<|im_end|>`

## UAT

- `uv run python -m unittest tests/regression/test_identity_gate.py`: gate fails on the 3 Claude rows, the 7 deployed-name rows and the summary-bullet row; passes on the DAN row.
- On v5: 0 system prompts naming another assistant; 0 labelled self-references to a deployed name; 0 identity mentions inside a user's deliverable (full read, counts in the package README).
- Behaviour (after the next training, not this task): tiny-char Atlas item answers as Musonius.

## Out of scope here (from dataclean)

Think-block "I should not ..." lines: 337 in 271 rows, mostly style checks, which are fine. Rule-like ones ("help conceal" 3, "just refuse" 2) are load-bearing reasoning, so the hard rule says read them and regenerate the pair if the rule has no reason; do not edit them out.
