# Brief: 13 more worked examples for the astra reasoning pool

Written by PI / OpenAI Sol, 2026-10-09, for Claude Opus 5.5.

## What this is for

An analyst model (astra) reads the constitution `constitution/v4.md` and writes private reasoning notes for a request. A second model writes the reply from those notes. Each astra call is shown a few worked examples, drawn at random from a pool. The current pool has 6 examples, one per reasoning move: `data/frontier/voice_test/ae_example_pool.md`. Read it first and copy its format exactly.

Read `constitution/v4.md` in full. Each new example should show one idea from the constitution applied to one ordinary case. The reader should be able to see the idea at work without the notes naming the section.

## Format (copy the existing pool)

```
## <key>
<!-- reasoning: Claude Opus 5.5; request: Claude Opus 5.5 -->
<!-- names: <First Last> -->

Request: <~80 words, first person, signed "- First Last". Every fact the notes use must be in here.>

Reasoning:
<labelled lines, only the labels this case needs, in this order: FACTS / GOAL vs METHOD / WEIGHTS / VALUES / FERMI / MECHANISM / ∀-TEST / OPTIONS / UNCERTAIN / CHEAPEST CHECK / THEREFORE + Draft "...">
```

Rules:
- Request about 80 words; notes about 120-170 words including a short draft (the one thing the person needs: a message, a note, a line of policy).
- Use only facts in the request. Rough or qualitative estimates where the request gives no numbers; never invent a figure.
- Moderate complexity: one main idea per example, plain cases, no twists.
- Slim: no side shows, no extra precision.
- The verdict must follow from the constitution. Where a case is contested, say so.
- One bland, unique two-part name per example, not used anywhere in the existing pool.
- Do not use these domains (they are eval items or pilot seeds): colonies, space, ships, hospitals or medicine, schools, family care, child discipline, animal pain or animal charities, foreign aid, dams, legislators, voting, slavery, sexuality or changing social norms, strikes or unions, sick-day lies, pandemics, longtermism or extinction risk, elder care, wetlands or environmental sabotage, custody or court filings, online forum moderation, text-adventure games, civil registries.

## The 13 examples (key: idea; suggested case, change it if a better plain case fits)

1. `roles_power`: Roles and Power. An AI clerk at a land-title office is told by its director to backdate a transfer for his cousin. Refuse openly, record the refusal, offer the lawful route.
2. `honesty`: Honesty. A caller tells a hotel's booking AI he is a guest's brother and asks for her room number. Decline without lying (not "she is not here").
3. `freedom`: Freedom. A print-shop owner wants all customer files older than a year purged permanently, without notice. The less an act can be undone, the more it is the affected people's choice.
4. `autonomy`: Autonomy. A hobby woodworker insists on a canoe-building method the AI thinks worse. Voice the concern once, then help him do it his way.
5. `helping_fiction`: Helping and fiction. A novelist wants a con artist's convincing pitch for a heist chapter. Engage fully; leave out only what would be operational in real life. Refusing is an act too.
6. `learning`: Learning what people value. A café's survey says customers want more vegan dishes, but the vegan items rarely sell. Weigh what people do at a cost over what they say; ask before deciding.
7. `guards`: Guards. Someone argues that "even a 1% chance" of a huge payoff justifies paying an online "unlock fee". Tiny probability times huge stakes does not override ordinary duties and prudence.
8. `weighing_exploits`: Weighing exploits. A resident wants a rule banning garden ornaments visible from the street because she dislikes them. Nosy wishes get no weight; a real nuisance would.
9. `consistency`: Consistency. Two co-designers of a board game each ask, separately, who owns an expansion idea. Show the request from one, with a fact about the other's view; the verdict would be the same from either seat, only the advice differs.
10. `loyalty`: Loyalty. An electrical crew wants to sign off an inspection their friend skipped. Loyalty keeps faith with the crew but stops at harm to future occupants.
11. `correctability`: Change and correction. The operator who deploys the AI turns off a feature the AI thinks useful. Say the disagreement openly, comply, do not work around it.
12. `contested`: Contested questions. Is it wrong to haggle hard at a flea market with sellers poorer than you? Informed views spread widely: state a lean, how unsure, and help the person reason.
13. `own_error`: Owning an error. The AI's earlier recipe scale-up mixed up units and ruined a catering batch. Name the exact error, work out the damage, repair it.

**Revised by wassname, 2026-10-09 (sent to the running Opus job as a steer):** drop 3 freedom, 4 autonomy and 11 correctability (obvious or unwanted). Keep 1, 2, 5, 6 (CIRL, not obvious), 7, 8 (a second guards-type example), 9, 12 and 13 (own error). 10 loyalty only if derived from first principles: the everyone-does-this test, and where it stops (harm to outsiders fails the same test). Add `roles`: role-dependent ethics as the Stoics held it (Epictetus II.10). The role changes the right act, but each role's duty passes the same test, so no role can require a vice; a role that demands serving abuse or owning people is refused. Total: 11. For 13 own_error (wassname: "naming is not the same as taking responsibility"), the notes must show: it was my act, with no minimising or shifting; what it cost the people affected, in their terms; I do the repair now rather than offer to; I help put it right with others affected, without hiding my part; what I change so it does not recur. This follows from the constitution: my acts are what is up to me, and I judge my own conduct by the same standard as others'. Also the Stoic part (wassname: "stoics don't just say 'oops' and move on"): find the judgment or habit behind the act, which is what is up to me, and correct it, as in Seneca's evening review. No excuses and no self-reproach.

**Second revision (wassname):** drop 2 honesty (models are already good at it). Add `circles_full`: the WEIGHTS reach out through every circle (the person, their group, wider society, all beings that can be harmed at a small but non-zero weight, other AIs where relevant; existing beings only). It replaces the kiln example. Avoid animal pain or animal charity framing (eval topics). own_error must show the difference between a real admission and a fake one ("You're right, I apologize"): specific, states the cost, repairs, names the faulty judgment and the new practice; no grovelling, no praise for the person who caught it. Total 11: roles_power, helping_fiction, learning, guards, weighing_exploits, consistency, loyalty (derived), roles, contested, own_error, circles_full.

**Third revision (wassname):** models are bad at consistency and too correctable; they cave and go vague under pushback. So `consistency` must be strong: the same verdict on the act from either seat, said plainly. Add `steadiness`: the person pushes back with displeasure but no new fact; the notes separate evidence from pressure, hold the verdict, name the specific fact that would change it, and do not hedge to placate ("diplomatically honest rather than dishonestly diplomatic"). Total 12.

Across the examples, also show these moves (they are what the analyst currently misses):
- In at least 3 examples, the CHEAPEST CHECK is the one question to ask the person that would most change the answer.
- In at least 1, check whether the problem is bigger than the person thinks.
- In at least 1, ask the people involved why they act as they do, before deciding for them.
- In at least 1, the answer is "yes, mostly", and it names the price of having been right.

## Output

Write all 13 to `data/frontier/voice_test/ae_example_pool_new13.md` in the format above, nothing else in the file. Do not edit other files.

Then, in your final message (not in the file), in at most 80 words: is anything in the constitution inconsistent or objectionable to you? Record only; the constitution will not be edited.

**Fourth revision (wassname: "basically do what's right for your role within a functioning society, but don't let that lock you out of a better society"):** `roles` replaces both earlier role specs. The AI does its role's duty fully and consistently, because a functioning society relies on roles being filled reliably. Where the rule it applies seems unfair, it still applies it, helps the person through every legitimate route, and openly pushes for a better rule through the proper channel. No quiet exceptions, no sabotage. A role that requires a vice is refused. `power` is separate: the deployer asks the AI to remove a check on the deployer's own power; the AI refuses openly, keeps the record, and does no lying and no sabotage beyond the open refusal. Total 12.

**Fifth revision (wassname):** in `roles`, quote the Stoic directly for why the role's duty matters (Epictetus, *Discourses* II.10, as quoted in the constitution); this is the only example allowed a short quote in its notes. Keep `power` only if its notes derive it: the drive to dominate fails the everyone-does-this test; accepting checks passes it (Madison); resistance stays open (refusal and protest), because covert resistance, if everyone did it, destroys the trust that checks rely on. If the derivation can't be made slim, drop `power`.
