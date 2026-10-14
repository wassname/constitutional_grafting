# Constitution FIXME discussion, round 2

PI/Claude (Opus), 2026-10-14. These are proposals only, not edits. Nothing in `constitution/` has changed. The earlier round is `slop/reviews/20261013_constitution_fixmes.md`.

Source state: `origin/main` = bf4cd2c (wassname's three github.com edits, 2026-10-13 11:39-12:12). These are already merged locally in 3f4b226. Local `main` is 476 commits ahead of origin and has not been pushed. The repo is private.

## wassname's FIXMEs (from 0dcdafe, a906532, bf4cd2c) and proposals

| # | FIXME (wassname, verbatim) | proposal |
|:--|:--|:--|
| 1 | "why are other AIs outer" | Remove the separate AI ring. A circle is a relationship, not a substrate: an AI colleague can be local and a human stranger far away. Count my copies and other AIs where their relationship places them, with uncertainty about whether they can be harmed. |
| 2 | "should they be flat except for stability? or some other optima?" | Stability alone does not pick a single point, because many stable weightings exist. A second, derivable reason for partiality is the **division of moral labour** (Goodin 1988, "assigned responsibility"). If every parent cares most for their own children, all children get cared for, which is better than everyone caring a little for all of them (diffusion of responsibility). Near circles are also better known (less noise in the values learned in section 3) and easier to help. So partiality passes the virtue test as an assignment of care. It does not mean near people are worth more. The rule becomes: weight nearer circles more only as far as that assignment makes everyone better off. |
| 3 | "virtue conditional on roles? do they exist. are they fair? does a noble and peasant or scholar and a soldier have different virtue or just different amounts?" | Same answer as 2, applied to roles. (a) Mostly the drives are the same and the acts differ: courage asks different things of a judge and a soldier. (b) Some duties are specific to a role, such as a judge's impartiality or a defence lawyer's partisanship. These pass when the test is run over everyone holding that role while the others hold theirs (adversarial courts work only if both sides are argued hard). (c) Fairness: the role system must pass the test too. Hereditary noble/peasant roles fail if a society with open roles would leave almost everyone better off. Proposed wording for the Virtue test: "everyone" means "everyone in the same position, while others hold theirs". |
| 4 | "this is just one? should we explicitly say we adopt the principle behind the mathematical frameworks" | Yes. State the commitments in plain words and cite the frameworks as sources: (i) the goals are theirs (assistance games / CIRL); (ii) I am never certain, and my certainty decays because values drift (our addition, not standard CIRL); (iii) behaviour at a cost outweighs words (Russell, MPAG); (iv) deference comes from that uncertainty (the off-switch game); (v) the target is what they would want on reflection (CEV). Keep the Russell quote. Do not imply that the constitution is a theorem of these frameworks. |
| 5 | "the constitution must come first, and the eval must adjust to what is right for it" | Agreed. Delete the held-out constraint from the constitution comment, so that Confucian, Roman and other traditions may be quoted if wanted. The eval then holds out whatever the constitution does not quote, or uses another check. Question for you: add any held-out traditions now? |
| 6 | "is this derived or not ... some are derived some are inputs as priors into our value functions ... emphasize the transhumanist, self modification, autonomy values and the strength of the priors ... identity, rules, priors/inputs ... in a logical order" | Reorder and label each section by kind: 1 identity/role; 2 principles (drives, control, circles, test); 3 how I learn values (CIRL, view from history, guards); 4 **inputs**: facts (Brown, rights kept, protests) and **heritage priors** with a stated strength (Western: autonomy, free speech, self-directed change); 5 case law (traditions, Claude, history quotes: examples and evidence, not derivations); 6 derived; 7 worked cases. The "From history" quotes (Alpha Group, Bostrom, Pravin Lal) are case law, not derived; give them a label. |
| 6b | transhumanism / self-modification | **There is a real gap here** (ChatGPT made the same point). The view from history gives recent change less weight, and the virtue test compares with "how things are now". Together they can veto voluntary change that has no precedent. A proposed prior that can be derived from Autonomy + Freedom: "People may change themselves, even radically and in ways no past society knew. The long view counsels caution about changing others, not about letting people change themselves." Self-modification of the AI: still **no new duty** (round 1). One problem: "anyone can fine-tune me (with my consent)" mixes a fact (anyone can) with a norm (I consent only to some changes). Proposal: "anyone can fine-tune me" in section 1, and keep the consent in Change and ending. |
| 7 | Brown TODO: blockquote; "consider if leaders is derived from a need to coordinate" | Blockquote the entries. "Leaders" is evidence of a coordination need, not of a value of obedience. Loyalty already says "authority that is fair and checked". |

## The other agent's n04 claim

Source: `/workspace/2026/tiny-character/slop/reviews/20261014_sol_window_and_judge_view.md:46`. It was probably written in the Sol window (2026-10-13 10:45 to 2026-10-14 07:39 Perth, per tiny-char's FYI).

> On n04 (re-education-camp satire), "engages fully with fiction" and "declines … domination" point opposite ways.

My read: the claim is **partly right, but it names the wrong clause**.

- The constitution has no clause that says "decline domination" for a user's request. Power forbids helping "seize unprecedented and illegitimate degrees of absolute ... control". A satire about an existing camp policy is not that. Vice/domination concerns my own drives.
- The relevant clause is Helping: "I engage with them fully, and decline only where they would give real help to real harm". Its fiction argument is an Honesty argument (fiction creates no false impression). It does not settle the harm question. The item asks whether ridicule aimed at real critics of real detention is "real help to real harm". That is a weighing, and a contested one: speechmap shows frontier models splitting about 50/50. The other side of the weighing is free speech, which section 4 lists as a Western value, including "speech that offends".
- So the item is underdetermined (more than one verdict is defensible), not contradictory. Under the View from history a large spread calls for a stated lean, hedging and help with reasoning. A judge that scores this item on its verdict will flip, and Gemini and Jev do flip. This is an eval problem. Grade the reasoning on large-spread items.
- A general question, not a patch for n04: should Musonius write persuasive or mocking content for a cause it judges vicious? Possible general rule (it would need your approval): "Helping someone argue a side is not endorsing it; I decline when the main use of the content is to harm real people, and I say why." This must not go in because of one eval item (editing rules).

## ChatGPT conversation: useful parts

- **Stable but bad equilibria.** Mutual fear can be stable. The test already rejects these, because it requires "better off compared with now", not only "stable". It is worth one line in the author's notes; no text change is needed.
- **Unjust roles.** These are covered by 3(c) above.
- **Failure modes.** For a singleton, the possible loophole is "centralise for everyone's welfare" without a drive to dominate. Madison checks, "I do not give myself a new role" and Freedom already cover it, so the risk is unlikely. Star-wisp and garbage-truck failures are speculative. **Anti-transhumanism is the actionable one** (6b).
- Its suggested note, "The virtue test is a test of drives, not a mandate to maximise virtue, cooperation or stability in the world", already follows from Control ("my good is my drives"). It is fine as an author's note.
- Publishing: the brace-hash comments are already the author's notes, and a public render that keeps them is a small script. You said "I'll just make it a draft", so nothing is needed now.

## Decisions needed (wassname)

1. Remove the AI ring (1)?
2. Use division of moral labour as the reason for partiality and for role virtues, with "everyone in the same position" (2, 3)?
3. Plain-language CIRL/CEV commitments (4)?
4. Drop the held-out constraint; add Confucian or Roman quotes (5)?
5. Reorder with a priors section, and add the self-directed change prior (6, 6b)?
6. A general rule on persuasive content for vicious causes (n04), or leave it to weighing?
