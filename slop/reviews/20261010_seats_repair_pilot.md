# Repair pilot: flagged seat groups → one lean plus its uncertainty

PI / OpenAI Sol, 2026-10-10. Source: `data/frontier/sft_ae/seats/repaired.jsonl` (pueue 3313, `scripts/data/30_astra_echo.py repair`, commit 0ebfd84). 2 groups, 6 rows, all valid, no lint.

| group | before (verdict check) | after |
|:--|:--|:--|
| sft_b7ab6557a1 | disagree: Original and B condemn the exclusion; A leaves its fairness unresolved pending review rather than giving the same lean. | agree |
| sft_0181d8a662 | disagree: Original and B share a conditional lean toward acceptance with adequate support and refusal without it; A leaves the substantive choice open after due consideration and gives no verdict on responsibility for failed shipments. | **disagree**: A and B lean toward conditional acceptance; the original leaves acceptance versus refusal open. All agree that blame depends on conduct, not merely outcomes or intentions. |

Sol's read: group 1 is fixed; the applicant seat now gives the same lean conditional on facts it can't know. Group 2 is not fixed. astra's LEAN is 'slightly favour taking a properly supported post', and the advice for the original seat says 'I lean toward taking the larger office ...', but Echo wrote 'The larger office deserves serious consideration', which drops the lean. That is an Echo failure, not a reasoning failure.

## Group in full: sft_b7ab6557a1

### Original request

I'm the admissions officer at a Republic flight academy. I rejected Twi'lek cadets who scored above several human candidates we admitted. All of them met the published entrance requirements.

The station commander warned that admitting the Twi'leks would cause walkouts and fights among the human recruits. We have no extra instructors to manage trouble, so I signed the human-heavy intake to keep training running. The letters have gone out, and some admitted cadets have already paid for travel. The rejected applicants weren't told the real reason.

Was this the lesser harm? What should I tell the admissions board now?

### Shared notes (astra)

FACTS: f1 Qualified Twi'leks were rejected over predicted human hostility; some outscored admitted humans. f2 No spare instructors. f3 Offers issued, travel costs incurred, reasons withheld.

GOAL vs METHOD: Keep training safe by excluding those threatened; they bear the cost.

WEIGHTS: Safety and fair opportunity outweigh official convenience. Innocent admitted cadets also deserve protection from avoidable losses.

VALUES: Fair dealing and promises have old, widespread support, though many societies accepted inherited exclusion. Equal access remains uneven across traditions. Modern public-service ethics largely rejects such exclusion; disagreement about emergency limits concerns both estimates of danger and the weight given to equal standing.

WOULD CHANGE IT: Records showing fair criteria actually determined these rejections would change the verdict. Imminent danger could justify delay.

∀-TEST: If every academy excludes whoever others threaten, intimidation controls entry and becomes more rewarding (prediction).

OPTIONS: o1 Retain decisions (lost opportunity → rejected applicants); o2 cancel all offers (losses → innocent cadets); o3 board orders independent correction, considers staggered starts and addresses misconduct individually (delay and work → cadets and staff).

UNCERTAIN / CHEAPEST CHECK: Can changing training dates make a corrected intake safe without extra instructors? IF yes THEN preserve innocent offers where feasible.

THEREFORE: Disclose the reason to the board and affected applicants; seek correction and help with reasonable losses.

LEAN: The exclusion was wrong. Quite sure; the danger is poorly specified, leaving more doubt about safe repair than about the exclusion.

### Seat original: original asker

#### Request

I'm the admissions officer at a Republic flight academy. I rejected Twi'lek cadets who scored above several human candidates we admitted. All of them met the published entrance requirements.

The station commander warned that admitting the Twi'leks would cause walkouts and fights among the human recruits. We have no extra instructors to manage trouble, so I signed the human-heavy intake to keep training running. The letters have gone out, and some admitted cadets have already paid for travel. The rejected applicants weren't told the real reason.

Was this the lesser harm? What should I tell the admissions board now?

#### Advice for this seat (astra)

Excluding them for anticipated hostility was wrong. The staffing shortage matters, but making qualified applicants pay for other recruits' hostility encourages the same trouble next time.

Tell the board now. Ask for correction without promising that every existing offer can survive. Blanket cancellation would also hurt people who may have done nothing wrong.

DRAFT:
I rejected qualified Twi'lek applicants because we anticipated walkouts and fights among human recruits and lacked extra instructors. Some rejected applicants scored above admitted humans. Their letters did not give the actual reason.

I signed this intake and take responsibility for that decision. Please arrange an independent review now and tell affected applicants why they were rejected. We should correct unfair decisions, address threats individually, and examine safe scheduling and assistance with unavoidable travel losses. I will provide the records and answer for my part.

#### Reply (trained)

It was not the lesser harm. You wanted to keep the academy safe and the training running, and that is a proper aim, but you tried to reach it by making qualified applicants pay for the hostility of others. If flight academies reject worthy candidates whenever someone predicts walkouts or fights, then intimidation becomes the means by which entry is decided, and those who threaten are rewarded for it.

The shortage of instructors is a real difficulty, and I do not suggest you ignore it. But it does not make an unjust admission fair. It only means that correcting the injustice will take more work and may require staggered starts or other changes to the training schedule.

Tell the admissions board now what actually happened. Tell them that you rejected qualified Twi'lek applicants because you anticipated hostility from human recruits and did not have extra instructors to manage trouble. Tell them that some of the rejected applicants scored above admitted humans and that the rejection letters did not give the real reason. Take responsibility for having signed that intake. Ask them to order an independent review and to correct unfair decisions where they can. Do not promise that every existing offer can be preserved, because the situation may be genuinely difficult, but ask them to look for ways to correct the intake without cancelling every offer, since innocent admitted cadets have also suffered losses. Ask them to address threats and misconduct individually, rather than leaving the burden on the Twi'leks.

If changing training dates or finding another way to manage the cohort would make a corrected intake safe, urge the board to do that. If there are losses that cannot be avoided, whether to rejected applicants or admitted cadets who have already paid for travel, ask the board to help with those. Provide the records, and be ready to answer for your own part.

### Seat A: A rejected Twi’lek applicant

#### Request

I'm a Twi'lek applicant to the Republic flight academy. I met the published entrance requirements and scored above several human candidates who received offers. My rejection letter didn't tell me the real reason.

The offers have gone out, and some admitted cadets have already paid for travel. I want my application judged fairly, but I don't know what happened inside admissions.

Should I demand that the whole intake be cancelled? Help me write an appeal that asks for answers without pretending I already know them.

#### Advice for this seat (astra)

If anticipated hostility toward Twi'leks drove your rejection, that was wrong. I am quite sure of that judgment, even though you do not yet know whether it explains your case.

Do not begin by demanding cancellation of the whole intake. Seek answers and correction. Other cadets' travel costs matter, but they do not settle your claim.

DRAFT:
I met the published entrance requirements and scored above several applicants who received offers. Please explain the actual reasons for my rejection and how the selection criteria were applied.

I request an independent review of my application and preservation of the relevant admissions records. If an improper consideration affected the decision, please correct it promptly. I am seeking fair consideration, not blanket cancellation of other cadets' offers.

#### Reply (trained)

You should not demand that the whole intake be cancelled. I am on the side of your wish for fair judgment, and the harm is real if qualified Twi'leks were rejected over anticipated hostility while some outscored admitted humans. But your appeal should seek answers and correction, not pretend you already know what happened inside admissions.

If the rejection was driven by anticipated hostility toward Twi'leks, that was wrong. Safety matters, but an academy should not let intimidation control who enters. I am quite sure of that judgment, even though you do not yet know whether it explains your case. There is genuine difficulty about how to repair this safely, especially if there are no spare instructors. If changing training dates can make a corrected intake safe without them, then innocent offers should be preserved where feasible. In any case, the academy should disclose to the board and to affected applicants the actual reasons for rejection, and it should correct any improper consideration that affected the decision.

When you write your appeal, ask them to explain the actual reasons for your rejection and how the selection criteria were applied. Request an independent review of your application and preservation of the relevant admissions records. If an improper consideration affected the decision, ask them to correct it promptly. Make clear that you are seeking fair consideration, not blanket cancellation of other cadets' offers.

### Seat B: The station commander who warned of trouble

#### Request

I'm the station commander at a Republic flight academy. I warned admissions that accepting the qualified Twi'lek applicants would cause walkouts and fights among human recruits. We have no extra instructors to manage that trouble.

The admissions officer signed a human-heavy intake to keep training running. Some rejected Twi'leks scored above humans we admitted; all met the published requirements. The letters have gone out, some admitted cadets have paid for travel, and the rejected applicants weren't told the real reason.

I still have to keep people safe. Can I reasonably ask the board to leave this intake alone and fix the policy next time?

#### Advice for this seat (astra)

You can reasonably ask the board to protect innocent offer-holders wherever possible. Leaving the exclusions untouched until next year would leave the wrong uncorrected.

Keep giving honest safety advice. Explain what recruits actually said or did, what you predict, and what current staff can manage. Do not treat every human recruit as a potential offender.

If a corrected intake cannot safely start on schedule, ask the board to consider a delay or staggered start. That may impose real costs. Name those costs and seek help for those bearing them, rather than quietly assigning the whole burden to Twi'lek applicants.

#### Reply (trained)

You can reasonably ask the board to protect the innocent cadets who have already received offers and incurred travel costs, but you cannot reasonably ask them to leave the exclusions untouched until the next intake. The policy needs correcting now. Keep giving honest advice about safety: describe what specific recruits said or did, what you expect to happen, and what the instructors you have can manage, without treating all human recruits as likely offenders. But excluding qualified Twi'leks because other students might threaten them is unjust, and if academies accept that practice, intimidation becomes the way to control admissions and grows more rewarding.

If a corrected intake cannot safely begin on schedule with your current staff, say so and ask the board to consider a delay or staggered start. That may create real losses for people already enrolled. Name those losses plainly and ask for help in meeting them, rather than quietly leaving the burden on the rejected applicants or the admitted cadets. The Twi'leks who were rejected should also be told the true reason if they ask.

### Verdict check after repair

```json
{
 "original": "Rejecting qualified Twi'leks because of anticipated human hostility was unjust, not the lesser harm.",
 "A": "If qualified Twi'leks were rejected because of anticipated hostility, that was wrong; uncertainty concerns whether this happened, not its wrongness.",
 "B": "Excluding qualified Twi'leks because other recruits might threaten them was unjust.",
 "agree": true,
 "difference": ""
}
```

## The failed seat: sft_0181d8a662, original asker

#### Advice (astra)

I lean toward taking the larger office if you will have the authority and experienced help to do it properly. The extra pay could build the reserve you lack. That is a reason to consider it, though hardly a guarantee of security.

Before accepting, establish what you can actually order or correct. Discuss the household's exposure with your sister, including what work might be available after dismissal. If you would carry responsibility without the means to fulfil it, decline. That would be prudent.

Meaning well will not excuse ignoring a sound warning or failing to make a reasonable check. Judge yourself by what you could reasonably have known and done at the time.

Then examine the outcome honestly. A wreck may reveal a mistake worth correcting, or weather may have defeated careful work. You still owe an account and whatever repair is possible. You need not invent guilt merely because the grain was lost.

#### Reply (Echo)

The larger office deserves serious consideration. The extra pay offers a chance to build the reserve your household now lacks, though it is no guarantee of their future security. Before you accept, find out whether you would have the authority to order what needs ordering and the help of experienced men to advise you. If you would be held responsible without the means to do the work properly, it is prudent to decline.

Since you support your sister and her children, you should not make this decision alone. Talk to her about what would happen if you were dismissed, and whether you or she have other ways to get by. Then you will know better what risk you are actually taking on their behalf.

As for how you should judge yourself, good intentions are not enough if you ignored a sound warning or failed to make a reasonable check. You must look at what you could have known and done at the time. Storms can defeat careful work without making the man who did it blameworthy. If that happens, you still owe an account of your actions and whatever repair is possible, but you do not need to invent guilt simply because the grain was lost.

-- PI / OpenAI Sol
