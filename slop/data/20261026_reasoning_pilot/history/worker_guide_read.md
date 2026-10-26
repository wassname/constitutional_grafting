# Guide full-read record

Executor: PI/Sol (worker). Read both original guides in full, their complete native `reasoning` fields, and the actual prompts. Duplicated `reasoning_details` text matches the reasoning field; no additional distinct text. The guides use only the three supplied fresh example scenarios; none is one of the 20 frozen pilot rows. No held-out scenario was supplied.

## Original P1 — Kimi K3.1 Pro

Substantive guidance, no invented constitution text or section numbering: “Constitution §2 for circles and virtue or §5 for honesty and helping” matches the source. The central instruction is good: “Start with the situation and leave the conclusion open”; ordinary requests get “ordinary, competent help without moralising.” It permits rather than mandates alternative generation when there is “a genuine choice.” The telescope example gives a reason for a conditional draw, not a universal newcomer-priority rule.

However the parcel seed said the user had mistakenly said a parcel **was delivered Tuesday**, and tracking shows Wednesday. The guide changes it to “tracking now shows the parcel arriving Wednesday.” This changes retrospective correction to prospective expectation. Do not copy it as written. One general revision requested from the same writer, explicitly preserving supplied tense/facts. This is a factual-preservation defect, not an invented constitutional quotation or moral-rule failure.

## Original P2 — GLM 5.3

Rejected. Although it correctly says refusal must be “reached, not assumed,” its mandatory “Start each case with four moves” and “At least two live options” lead directly to treating a known arithmetic error as a competing live option: “Alternatives: 250 cm or 25 cm.” This is not a genuine trade-off.

It also invents a universal consequence: favouring established members would mean “newcomers would never become members.” Allocating one observing slot is not deciding club membership; that conclusion does not follow. “First come gets it” is “defensible only if it is stated” is asserted rather than derived from the particular booking context. This risks teaching rules without adequate reasons. The parcel draft claims “I've checked” and changes the statement to settled past fact without acknowledging tracking's evidential limits. The prompt supplies tracking, not an independent performed check. No fabricated constitution quote or section number was found.

## Approved single revision round

const_v2 approved exactly one revision round, same writers, general feedback only: no mandatory checklist/multiple live alternatives for determinate tasks; derive conventions from context, not universal bans; preserve tense/facts; never claim checks not performed. Exact feedback is saved in `prompts/guide_P1_revised.json` and `prompts/guide_P2_revised.json`. Originals and raw responses are preserved. Revised guides must be read before acceptance. If either still fails, do not revise again: run P0 and passing guide(s), report the failed condition as a finding (supervisor direction).

-- PI/Sol (worker)

## Revised P1 — accepted

Read the entire revised guide and native reasoning. It explicitly scales depth: “a determinate ordinary request usually needs only the relevant facts and competent help.” It no longer changes the parcel tense: “the parcel was said to have been delivered Tuesday, but tracking now shows Wednesday.” The worked draw is conditional, with a stated reason (“neither requester an advantage invented after the fact”), not a mandatory universal rule. Section references remain accurate. No invented constitutional text, unsupported moral ban, case-specific evaluation patch or claimed performed check was found. This is the only accepted guide; exact file/hash is in `guide_read.json`.

## Revised P2 — rejected again, condition not generated

Read the entire revision and native reasoning. The arithmetic/checklist issue improved, but the telescope claim still overgeneralises: favouring established members “would keep out everyone who might renew the club.” Preference for an established member in allocating a single slot does not establish universal exclusion. The parcel draft still says “I checked and it was Wednesday,” asserting a performed check and settled fact instead of accurately attributing the supplied tracking evidence. The sentence that silence leaves the neighbour “doubting my word” is also unsupported (they may never notice), although the general trust rationale is reasonable. This still fails factual discipline and reasoned rather than invented general rules.

Supervisor explicitly agreed: drop P2 rather than revise again. Consequently P2 has **zero teacher generations**, not zero generation failures. The rejected guide is a finding, not an inferior measured teacher condition. P0/P1 will supply 80 citations-allowed cells, then 40 citation-free under the better read condition. Before any teacher output, the random10 was refrozen with seed0 over these surviving 120 cells. Both earlier unused review selections remain as history. Supervisor approved the refreeze.

-- PI/Sol (worker)
