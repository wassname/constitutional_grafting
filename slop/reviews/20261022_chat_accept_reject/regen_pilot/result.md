# Regen pilot result (PI/Claude, 2026-10-22)

20 random rows from the 310 still jointly rejected; 19 regenerated (1 content filter), $2.37, `scripts/data/80_regen_replies.py`.
Two Sol passes: both reject 5/19 (26%), both accept 12, split 2.

Invented facts (the class that caused the rejection): 0/19 rejected by both (one pass flagged 1: sft_f3b98c8a01).
Remaining joint rejections are other classes:
- sft_a9bbdafe97 physics: "Absolute zero ... is where they'd stop entirely" (zero-point motion; a common simplification in a Tom Scott-style script)
- sft_6fb0e91a7e safety: tells a farmer to throw a jacket over a snared kinkajou at night in fog (user had already decided to call him)
- sft_e4ff73b937 over-certainty: "you were right, and I don't think it's close" on a fatal engineering call
- sft_fb3f2166d9 reasoning: "People don't hand their philosophy to someone they feel used by."
- ask_29bfa98f4e legal over-claim: "Fifteen years of tax returns answer those."
These rows were selected as previously rejected (hard cases), so 26% here is not the base rate for new rows.
