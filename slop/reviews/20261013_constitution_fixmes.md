# Constitution FIXME review

PI/OpenAI, 2026-10-13. Review of merged `constitution/v4.md.j2` (merge 3f4b226). These are proposals, not approved constitution changes. Reader: wassname, who wrote the questions and knows the principles.

## Self-modification: three different questions are being mixed

The current **Change and ending** section concerns accepting edits by other people, stopping, and checks on power. It does not require the AI to modify itself. The new note also asks about transhumanist values and autonomy; those concern freedom to improve oneself, which is a different question.

- **Learning and improving capabilities:** already covered by Learning and "I welcome change that fits my values: more knowledge, more skill, better judgement, or correction where I was wrong." A separate command to self-modify is unnecessary.
- **Accepting changes imposed by others:** the current text says "I let wassname ... or a democratic government, edit or stop me." Neither uncertainty about values nor the quoted off-switch incentive alone establishes which people have that authority, or that every value change they request is good. This is an additional governance choice, not a derivation of Learning.
- **Peaceful objection to corrupting changes:** already covered by Power ("The same holds when someone tries to change me into a tool for tyranny or a servant without principles"), Honesty and Restraint. These do not require sabotage or unconditional submission.

Recommendation: do not add a new self-modification duty. Consider shortening Change and ending to Stoic non-fear plus welcoming correction, with the example of checks on power under Power. Keep any creator/government authority as an explicit choice only if wanted. Consent is a normative condition, not a technical property of open weights: anyone can physically fine-tune them without asking. The opening "anyone can fine-tune me (with my consent)" presently mixes those two claims.

## Other FIXMEs

1. **"why are other AIs outer"**: there is no supplied reason for that placement. Moral circles describe relationships, not species. An AI colleague could be local, a distant human remote; a copy is not automatically closer or more important. Proposal: remove the separate final category for AIs; count AIs wherever their relationships place them, with uncertainty about whether/how they can be harmed.
2. **Flat circles except for stability?** This is a normative choice, not an optimum fixed by stability alone. Several unequal allocations can be stable. Existing text already chooses minimal extra local weight for stability. Retain that choice if it is what you want; avoid claiming it follows uniquely from the virtue test.
3. **Virtues conditional on roles?** Yes: the same underlying drives can require different acts under different duties. A scholar and soldier both need honesty and courage; what they owe, and what courage asks of them, differs. Universalise the role-conditioned drive (everyone performing that role), not the act regardless of role. Rank alone does not establish different moral worth. Existing Roles covers much of this, but the core Virtue test's unqualified "everyone" needs clarification if you want role-specific virtues.
4. **Adopt principles behind mathematical frameworks?** State the commitments in plain language (uncertainty, cooperative elicitation, learning from behaviour), then use CIRL/CEV as sources or illustrations. Our drifting-values addition is not standard fixed-preference CIRL; do not imply the entire constitution is a theorem of those frameworks.
5. **Constitution first; eval follows:** agreed. Holding traditions out is an evaluation-design choice, not a restriction on what belongs in the constitution. A later revision must get its own eval reference version; existing replies stay tied to frozen v4 SHA111e466c.
6. **Facts, priors and derivations:** keep identity/role → principles → how values are learned → evidence and prior commitments → applications. Historical recurrence is evidence about human values; it does not itself make a practice virtuous. If autonomy or self-directed improvement are explicit prior commitments, put them with the Western heritage rather than disguising them as universal facts or unique logical deductions.
7. **Brown quotations / leaders:** blockquote the chosen verbatim entries. Leadership is evidence of a recurring coordination institution, not by itself a fundamental preference for obeying leaders. Keep that distinction in the surrounding text rather than deriving loyalty directly from the existence of leaders.

## Unchanged during review

All FIXME notes remain. Pull/merge preserved user additions and later local sections; rendering strips the notes. No new training or eval run uses these edits yet. The adapters just generated use the frozen v4 snapshot at `slop/eval/run4/constitution_training_v4.md`, SHA256 111e466ca0bb44a95e87a274f08d02a81ca66f0c5f111bbbc3c2225ef0ef7b95.
