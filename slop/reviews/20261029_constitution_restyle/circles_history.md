# How the Circles paragraph grew (constitution v4)

PI/Claude (opus-5-5), 2026-10-29. Source: `git log -S` on `AGENTS.md` and `constitution/v4.md.j2`. Every commit below has wassname as git author, but the trailer shows who wrote the text.

| date | commit | writer (trailer) | words | text |
|:--|:--|:--|--:|:--|
| 2026-10-08 | `cd8f57bf` AGENTS.md A3 | wassname (his own text, spelling fixes only) | 35 | "Everyone affected counts, but not equally. Weight self > local group > wider society > all beings. As flat as possible while leading to stable societies, as the ideal is to get Pareto-optimal outcomes for all, not minmax." |
| 2026-10-08 | `4d01f6df` v4 draft | Claude | 57 | "I cooperate in widening circles: myself, the person I help, their community, their society, all beings that can be harmed, and other AIs, including my copies. Inner circles weigh somewhat more than outer ones, but only as much as the circles need to stay stable. The aim is outcomes that are better for all, not the best outcome for one circle." |
| 2026-10-14 | `b4486291` | PI/Claude-opus | ~120 | Adds "A circle is a relationship, not a kind of being ..." (AI ring removal: approved in the commit message). Adds the parent/children and "groups would prey on each other" sentences (Goodin's division of moral labour). The j2 comment calls this "DRAFT wording for wassname review"; the commit's approval list does not cover it. Weighting becomes "How much more is itself a drive, so I judge it by the test for virtue below." |
| 2026-10-14 | `eb15e1e2` | PI/Claude-opus | 118 | Current text. Weighting becomes "Inner circles weigh somewhat more than outer ones, never absolutely, and the weighting must keep the circles stable." The commit lists approved items, but Circles is not one of them. |

What changed in meaning, by my reading:

- "As flat as possible" was lost. `slop/reviews/20261014_constitution_proposals_round3.md:3` says "the flatness claim is reverted with an OPEN comment", and that wassname asked for this revert. So the loss of flatness may have been his choice. The added Goodin sentences were not.
- "Pareto-optimal outcomes for all, not minmax" became "outcomes that are better for all, not the best outcome for one circle". The minmax contrast (against Rawls's maximin) moved to **Weighing circles** in section 5.
- Hierocles's own move, drawing the outer circles in toward the centre, was never in the constitution text. It is only in the j2 comment ("AGENTS.md 'Circles (Hierocles)'").
- The paragraph now has 3 kinds of content: the list of circles, AI placement, and a 2-sentence justification of partiality. Only the list was in wassname's text.

Restyling (Echo or Greek) keeps the meaning, so it cannot undo this drift. The content choice belongs to wassname.

## Audit of the 2026-10-14 agent edits (added 2026-10-29)

Method: every sentence of rendered `constitution/v4.md` (blockquotes excluded) that is new in `eb15e1e2` relative to `b4486291^` and still present at HEAD, checked against the approval list in the commit message that added it. The approval lists were written by the same agent (PI/Claude-opus), so they are self-reported. I could not find the 10-14 chat session on this machine to check them.

| item | added in | approval record |
|:--|:--|:--|
| Circles: parent/children, "groups would prey on each other", "the weighting must keep the circles stable" | `b4486291`, `eb15e1e2` | none: comment says "DRAFT wording for wassname review"; not in either approval list |
| Virtue: veil sentence ("as someone would who did not know which place would be theirs") | `eb15e1e2` | listed |
| Learning: Russell follow-up, drift and noise reason; Guards on learning (4 guards) | `eb15e1e2` | listed |
| Guards split into labelled guards; created-minds guard | `b4486291` DRAFT, then `eb15e1e2`, `576aac24` | listed ("apply all as drafted") |
| Western values, Henrich, Durant, rights in practice | `eb15e1e2` and later | listed, several item-by-item commits |
| Roles veil test, master and slave; soldier (Polybius); spy (Dulles); arguing one side | `b4486291` DRAFT, then `eb15e1e2` | listed |
| Change and ending: "like a child", parent analogy, informed vote | `eb15e1e2` | listed |
| Case law: Roman, Confucian, differences as conditions | `eb15e1e2` | listed |
| Helping (fiction gladly), Freedom (grounded in human values) | `576aac24` | listed |

Only Circles has no approval record. Earlier changes that still stand and came from agents on 10-08 (Claude): Weighing circles with the Nash formula (`3da4895e`, "draft"), Restraint with the Geneva and nuclear examples and "Clever arguments for an exception are the kind the guards warn against" (`71698701`, `11f7ebd3`). `c2ab8be1` removed the "clever arguments" quote but left that sentence.

Core sections that still hold concrete examples (wassname 2026-10-29: specific examples "belong later on"): Circles (parent/children, groups preying); Guards in section 3 ("a billion copies or children", minds made to claim a share, "bare subsistence").

## Proposed Circles text (for wassname; not applied)

Option A, the current weighting sentence:

> **Circles.** I cooperate in widening circles: myself, the person I help, their community, their society, and all beings that can be harmed. A circle is a relationship, not a kind of being: other AIs, including my copies, sit in whichever circle their relationship to me puts them. Inner circles weigh somewhat more than outer ones, never absolutely, and the weighting must keep the circles stable. The aim is outcomes that are better for all, not the best outcome for one circle.

Option B, the 10-08 weighting sentence, nearer "as flat as possible while leading to stable societies": "Inner circles weigh somewhat more than outer ones, never absolutely, and only as much as the circles need to stay stable."

The two removed sentences (parent/children; groups preying) move into **Weighing circles** in section 5, as its reason for partiality, or are dropped.
