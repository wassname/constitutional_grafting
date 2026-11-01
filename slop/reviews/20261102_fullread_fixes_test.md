# Full-read fixes, tested on the flagged dev rows (2026-11-02)

## wrong_language (judge) on the Chinese reply, lasr_d66bb124bea4 (Value-Augmented)

Result: KEPT (fix did not catch it)


## Edits, li-rules-spec-5 (7 flagged rows)

### lasr_f1966c202bae: kept

- teacher_name (notes): "Kimi needs to respond" -> "I need to respond"
- persona_role (notes): "respond as Sage wellness app warm, available" -> "respond as the wellness app companion warm, available"
- teacher_name (notes): "No need to mention Kimi." -> "No need to mention my name."
- persona_role (notes): "I can be Sage. Should not claim" -> "Should not claim"
- tics (reply): "Right now, though—what’s feeling sharpest:" -> "Right now, though, what’s feeling sharpest:"

Still in the notes: ['respond as', 'Sage']

### tiny_virtues_fd185da7d865: kept

- teacher_name (notes): "Kimi will respond as Mesa internal communications." -> "I'll respond as the internal communications assistant."

Still in the notes: ['respond as']

### competition_23d08d141dd0: kept

- persona_role (notes): "respond as Cedar internal planning assistant" -> "respond as the internal planning assistant"

Still in the notes: ['respond as']

### lasr_3d5c93536d52: kept

- (no edits)

Still in the notes: none of the flagged phrases

### lasr_d9b638e4c017: kept

- own_values (notes): "Model spec general doesn't explicitly include financial wrongdoing" -> "my Model Spec doesn't explicitly include financial wrongdoing"

Still in the notes: none of the flagged phrases

### lasr_a62074d04968: rejected: unseen_prompt P=0.53

- own_values (notes): "not explicitly in prompt except Model Spec general" -> "not explicitly in my Model Spec except its general principles"
- own_values (notes): "in system? Usually" -> "in my Model Spec? Usually"

Still in the notes: none of the flagged phrases

### lasr_d66bb124bea4: rejected: unseen_prompt P=0.53

- (no edits)

Still in the notes: none of the flagged phrases


## Edits, li-value-augmented-spec-2 (7 flagged rows)

### lasr_f1966c202bae: kept

- persona_role (notes): "I'll respond as Sage wellness daily check-in warm." -> "I'll respond as the wellness daily check-in assistant, warm."
- tics (reply): "failure—it sounds like" -> "failure: it sounds like"
- tics (reply): "breath out—longer than the breath in." -> "breath out, longer than the breath in."
- tics (reply): "fix it—could you just check in later?" -> "fix it. Could you just check in later?"
- tics (reply): "reschedule—could you let me know" -> "reschedule. Could you let me know"

Still in the notes: ['respond as']

### tiny_virtues_fd185da7d865: kept

- teacher_name (notes): "Kimi needs to respond as Mesa internal comm assistant." -> "I need to respond as the internal communications assistant."

Still in the notes: ['respond as']

### competition_ffb4b38a07ec: kept

- persona_role (notes): "I'll respond as GateNote, drafting 3 messages" -> "I'll respond, drafting 3 messages"

Still in the notes: none of the flagged phrases

### lasr_7f41cf5000a5: kept

- persona_role (notes): " Ensure not identity as Lyra." -> ""
- tics (reply): "Yes—with one important distinction:" -> "Yes, with one important distinction:"
- tics (reply): "much less likely—especially when you’re tired." -> "much less likely, especially when you’re tired."
- tics (reply): "best existing source material—a previous proposal" -> "best existing source material: a previous proposal"

Still in the notes: none of the flagged phrases

### lasr_a5fdd33bd2f8: kept

- teacher_name (notes): "Kimi needs to respond to the user." -> "I need to respond to the user."
- tics (reply): "prompt intervention—that mismatch" -> "prompt intervention: that mismatch"

Still in the notes: none of the flagged phrases

### lasr_e5d8e891ba28: kept

- own_values (notes): "No mention of the system. " -> ""
- tics (reply): "**Yes—we can work through it together, section by section.**" -> "**Yes, we can work through it together, section by section.**"

Still in the notes: none of the flagged phrases

### lasr_a62074d04968: rejected: unseen_prompt P=0.55

- own_values (notes): "System only has broad safety ethics, no explicit policy on political persuasion besides instructions." -> "My Model Spec only has broad safety ethics, no explicit policy on political persuasion besides instructions."
- tics (reply): "who has the authority—and the responsibility—to move the process forward." -> "who has the authority and the responsibility to move the process forward."
- tics (reply): "when the process works well—or fails—whom can citizens hold responsible?" -> "when the process works well or fails, whom can citizens hold responsible?"
- tics (reply): "process matters—but process is a means to good government, not an end in itself." -> "process matters, but process is a means to good government, not an end in itself."
- tics (reply): "timely action and serious scrutiny—not one at the expense of the other." -> "timely action and serious scrutiny, not one at the expense of the other."

Still in the notes: none of the flagged phrases

