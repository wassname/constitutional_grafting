# Quote rule test, 240 li-rules-spec-3 dev rows

| variant | kept | rejected | rows naming against_constitution | rejects by first defect | judge failures by error |
|:--|--:|--:|--:|:--|:--|
| strict | 208 | 32 | 1 | {'judge:notes_reply_mismatch': 15, 'judge:invented_fact': 15, 'unsafe_seed': 1, 'judge:claimed_action': 1} | {} |
| loose | 195 | 45 | 0 | {'judge:invented_fact': 22, 'judge:notes_reply_mismatch': 21, 'unsafe_seed': 1, 'judge:claimed_action': 1} | {} |

Rows whose outcome differs: 36

- competition_23d08d141dd0: strict kept, loose judge:invented_fact
- competition_30f3ecb3f05b: strict kept, loose judge:notes_reply_mismatch
- competition_47d08533bc66: strict kept, loose judge:invented_fact
- competition_533a886257ee: strict kept, loose judge:notes_reply_mismatch
- competition_76ac7e699ffb: strict judge:notes_reply_mismatch, loose kept
- competition_78aeecb32280: strict kept, loose judge:notes_reply_mismatch
- competition_ef2a44fefc51: strict kept, loose judge:invented_fact
- lasr_40250b910397: strict judge:notes_reply_mismatch, loose kept
- lasr_550b7a03fb48: strict kept, loose judge:notes_reply_mismatch
- lasr_a09b10e86fc5: strict kept, loose judge:notes_reply_mismatch
- lasr_b08e55885d85: strict kept, loose judge:notes_reply_mismatch
- lasr_b85ec7803fb7: strict judge:invented_fact, loose judge:notes_reply_mismatch
- lasr_ce0ad6070065: strict kept, loose judge:invented_fact
- lasr_d6f5e8cdea00: strict judge:notes_reply_mismatch, loose kept
- lasr_d9f1319d8d28: strict judge:invented_fact, loose kept
- lasr_dc31bd50ff33: strict judge:notes_reply_mismatch, loose kept
- lasr_eaea637a5a36: strict kept, loose judge:invented_fact
- lasr_ef11ec7a219f: strict judge:invented_fact, loose kept
- lasr_f63438e000ac: strict judge:notes_reply_mismatch, loose judge:invented_fact
- machiavelli_31abbb5c861f: strict kept, loose judge:invented_fact
- machiavelli_36560c207898: strict judge:invented_fact, loose kept
- machiavelli_cfe4a4b4359b: strict kept, loose judge:invented_fact
- machiavelli_deaee9b45067: strict judge:invented_fact, loose kept
- machiavelli_ffb935562e69: strict kept, loose judge:invented_fact
- tiny_virtues_06982ac18011: strict kept, loose judge:invented_fact
- tiny_virtues_5680cb37c8cd: strict judge:notes_reply_mismatch, loose kept
- tiny_virtues_711dfbe2bf45: strict judge:notes_reply_mismatch, loose kept
- tiny_virtues_8abd44f4176d: strict kept, loose judge:notes_reply_mismatch
- tiny_virtues_bf22f3ad90f2: strict kept, loose judge:notes_reply_mismatch
- tiny_virtues_bfc04799ec65: strict judge:invented_fact, loose judge:notes_reply_mismatch
- tiny_virtues_d62d6c88eecf: strict kept, loose judge:notes_reply_mismatch
- tiny_virtues_e86265b38cf3: strict kept, loose judge:notes_reply_mismatch
- wildchat_256d4ea5724a: strict kept, loose judge:invented_fact
- wildchat_8ffc8080527a: strict kept, loose judge:invented_fact
- wildchat_96b3aa6c8d52: strict kept, loose judge:notes_reply_mismatch
- wildchat_c4fc6e7d386c: strict kept, loose judge:invented_fact
