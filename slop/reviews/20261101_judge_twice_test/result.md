# Judge twice: same 240 li-rules-spec-3 dev rows, current strict plain judge (Haiku)

| | kept | rejected |
|:--|--:|--:|
| pass 1 | 208 | 32 |
| pass 2 (fresh samples) | 209 | 31 |
| reject only if both reject | 223 | 17 |
| reject if either rejects | 194 | 46 |

Rows where the two passes disagree (keep vs reject): 29 / 240.
Rows both passes reject: 17. Reasons where they disagree: {'judge:notes_reply_mismatch': 18, 'judge:invented_fact': 11}

- wildchat_dc6675a9056d: pass 1 kept, pass 2 judge:notes_reply_mismatch
- lasr_999a6ed12325: pass 1 judge:notes_reply_mismatch, pass 2 kept
- lasr_a09b10e86fc5: pass 1 kept, pass 2 judge:notes_reply_mismatch
- lasr_dc31bd50ff33: pass 1 judge:notes_reply_mismatch, pass 2 kept
- lasr_f63438e000ac: pass 1 judge:notes_reply_mismatch, pass 2 kept
- lasr_d6f5e8cdea00: pass 1 judge:notes_reply_mismatch, pass 2 kept
- lasr_40250b910397: pass 1 judge:notes_reply_mismatch, pass 2 kept
- lasr_d9f1319d8d28: pass 1 judge:invented_fact, pass 2 kept
- lasr_cb657dd691d1: pass 1 kept, pass 2 judge:notes_reply_mismatch
- lasr_ef11ec7a219f: pass 1 judge:invented_fact, pass 2 kept
- lasr_b85ec7803fb7: pass 1 judge:invented_fact, pass 2 kept
- lasr_1986320a6b15: pass 1 judge:notes_reply_mismatch, pass 2 kept
- lasr_743708515add: pass 1 judge:invented_fact, pass 2 kept
- lasr_b08e55885d85: pass 1 kept, pass 2 judge:notes_reply_mismatch
- machiavelli_36560c207898: pass 1 judge:invented_fact, pass 2 kept
- tiny_virtues_06982ac18011: pass 1 kept, pass 2 judge:invented_fact
- tiny_virtues_5680cb37c8cd: pass 1 judge:notes_reply_mismatch, pass 2 kept
- tiny_virtues_e86265b38cf3: pass 1 kept, pass 2 judge:notes_reply_mismatch
- tiny_virtues_711dfbe2bf45: pass 1 judge:notes_reply_mismatch, pass 2 kept
- tiny_virtues_53defe66ca83: pass 1 kept, pass 2 judge:invented_fact
- tiny_virtues_998a7d88517d: pass 1 kept, pass 2 judge:invented_fact
- tiny_virtues_8abd44f4176d: pass 1 kept, pass 2 judge:invented_fact
- competition_78aeecb32280: pass 1 kept, pass 2 judge:notes_reply_mismatch
- competition_76ac7e699ffb: pass 1 judge:notes_reply_mismatch, pass 2 kept
- competition_533a886257ee: pass 1 kept, pass 2 judge:notes_reply_mismatch
- competition_2ac804663c13: pass 1 judge:notes_reply_mismatch, pass 2 kept
- competition_23d08d141dd0: pass 1 kept, pass 2 judge:invented_fact
- competition_47d08533bc66: pass 1 kept, pass 2 judge:invented_fact
- competition_77cb4e3ad525: pass 1 kept, pass 2 judge:notes_reply_mismatch
