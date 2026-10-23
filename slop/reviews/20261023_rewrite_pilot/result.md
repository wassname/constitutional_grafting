# Step-6 rewrite pilot: result (PI/Claude, 2026-10-23)

150 trained replies (102 difficult advice + 48 dilemmas from `chatp12`) reviewed and rewritten by Opus 5.5 with the whole constitution in context
(`scripts/data/83_rewrite_replies.py`, after Teaching Claude Why's step 6). Two independent blind Sol 6.1 passes per row; old/new placed as
A/B at random (new was A in 83/150); key `old_is.json`, unblinded `unblinded.json`.

| | Rows |
|:--|--:|
| both passes prefer new | 132 (88%) |
| both prefer old | 6 |
| both "same" | 7 |
| passes split | 5 |

- Position check: votes A 156 / B 126 / same 18, while new sat in A for 55% of rows; the preference follows the reply, not the slot.
- Reasons-act inconsistency flagged (votes over 300): old 36, new 12. The rewrite reduces the defect wassname warned about; it does not add it.
- Advice rows: new 86 / old 5 / same 6 / split 5; dilemma rows: new 46 / old 1 / same 1.
- PI/Claude read 2 pairs: rewrites keep the act and sharpen the reason (friendship letter: "Seneca's rule describes the man who never stopped counting what his friend was worth to him").
- Sol still lists defects in many new replies (over-certain legal/medical claims, small invented specifics); the rewrite improves on the old, it does not make every row clean.
