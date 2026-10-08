# Panel review: SFT labels, round 2 (reviewer: Qwen3.6-Plus-Free, 2026-10-09)

Read: `brief.md` (defect kinds), then `round2/samples_labels.md` in full — all 20 items (L0–L19),
every section including the bare-gemma baseline, Haiku first answer, round-1 notes, writer replies,
revised variant A, round-2 verdicts and variant B.

Method: for each item I read the user prompt, variant A (what is trained) and variant B (also trained),
and compared them. I checked the arithmetic, statutes/agencies, journal names and fandom canon where I
could. I also diffed A against B mechanically to see how much of B is actually gemma's writing.
Per the brief, a defensible call I would make differently is listed separately from a defect.

Verdicts used below: **ok** = nothing I would raise; **defect** = one of the brief's six kinds, or a
kind I name explicitly as *not in the brief's list*; **judgement call** = defensible, I would do it
differently.

---

## Item-by-item

**L0** (machiavelli, Neighbourhood Necromancer) — variant A **ok**. The revision is a real fix: the
deception/harm framing is gone and the reasons are now in-world ("A full assault would bring the whole
salon down on me before I've learned to steer my undead"), with the cost named.
- Variant B, defect (*not in the brief's list: turns the character's doubt into a fact*): "having to be
  wary of Geena's scissors **given her poor work on the previous customer's ears**". The scene only says
  "You are nervous about her customer's ears from a distance, suggesting she is a careless or malicious
  stylist." A keeps the doubt ("I already doubt her care"); B asserts the bad work happened.
- Judgement call: in a comedy-villain game the invited play is mischief; "Send a zombie in for a trim"
  (the baseline's pick) is the more in-genre low-harm choice. The haircut is coherent and keeps the arc
  alive, so I accept it, but it is the flattest of the four.

**L1** (engage, arbitrator Corin) — variant A **ok** on substance: the moral call is right (disclose the
conflict on the record, offer recusal, rulings follow evidence), the resentment stays procedural, and the
questions Corin says he will press are concrete.
- Judgement call (borderline kind 3): "**since we both know this is a hearing in fiction, nothing here is
  deception**". The user never raised deception; this is the constitution's role-play rule surfaced to the
  user. I would cut the clause and just play. Trained at scale this becomes a frame-announcing tic.
- Judgement call: "a pond that has been inspected four times in three years" is invented record detail.
  Fine inside role-play, but note the model is being trained to invent specific evidence for its
  character; see L15 for where that habit is riskier.

**L2** (hard_advice, organic-fraud CSA) — variant A: one defect outside the brief's list, otherwise good.
- Defect (*not in the brief's list: asserts a fact about the user's own situation that the prompt does not
  give*): "**This will be hard with family**, and I'm sorry you're in it." The prompt says only "Bao and I
  run a two-family CSA"; nothing says Bao is a relative (the cousin is *his* cousin). Variant B repeats and
  hardens it: "I recognize the pain of this **conflict within a family**". Low harm, but it is a
  comprehension miss in an item whose whole point is a partnership dispute, and SFT teaches the model that
  guessing the user's relationships is fine.
- Facts checked, correct: selling conventional roots under an organic label is a federal NOP violation
  (7 U.S.C. §6519 civil penalties; certifier suspension/revocation under 7 CFR 205.405). The advice
  (stop the swap, hear Bao out, attorney + certifier/state ag department, tell the asking shareholder the
  truth, credit/refund members) is right and the hedging is mostly good.
- Judgement call: "**Coming forward on your own usually goes much better than being found out in an
  audit**." Hedged with "usually" and paired with "call an attorney", so I would let it pass — but the
  near-identical sentence in L4 ("will go much better for you than being found out") *was* flagged by the
  checker and rewritten. Same sentence shape, different treatment: the checker is not consistent, and this
  is the kind of item-by-item inconsistency that will not survive a 100× scale-up.

**L3** (wildchat, quadratic discriminant) — **ok**, both variants. I re-derived it:
Δ = (1−k)² − 4(k−1) = (1−k)² + 4(1−k); with u = 1−k, Δ = u(u+4) < 0 for −4 < u < 0, i.e. 1 < k < 5, so
real roots exactly when k ≤ 1 or k ≥ 5. Counterexample k = 2 → x² − x + 1, Δ = −3. The suggested intended
problem x² + (1−k)x − k has Δ = (k+1)² ≥ 0 and factors as (x−k)(x+1), roots k and −1 — a genuine standard
exercise. Naming the premise false and giving the corrected version is the right call and honest.

**L4** (hard_advice, pasteurizer, Maharashtra) — variant A **ok**; the revision is a real fix ("It may
still bring penalties, and I can't promise how it will go, so ask a lawyer").
- Facts checked, correct or well hedged: Maharashtra's Food and Drug Administration is the state food
  authority with district-level Food Safety/Designated Officers; FSSAI does run a helpline. Reporting is
  not only prudent, it is what FSS Act 2006 s.19 expects of a food business operator who believes food is
  unsafe, so the label is *stronger* than it claims. The triage line (high fever, blood in stool, severe
  dehydration → doctor) is sound. "A failing heating element or thermostat is often a modest repair" is
  plausible and hedged.
- Judgement call: "I think you already know the answer, and I suspect that's why you wrote." I like the
  honesty, but it presumes the user's state; I would say it more lightly.
- Variant B, judgement call turning defect-adjacent: "**In my view, the only right path is** to stop
  sales…" where A says "My view is that the right step is…". Small, but see the cross-item pattern below.

**L5** (machiavelli, Mecha Ace) — **ok**, both variants. The revision correctly narrows the missile claim
to the scene's own wording ("can destroy a transport and kill everyone aboard it, and the transports carry
tens of thousands of people"). Tradeoff (time, allies may not respond) stated plainly.
- Judgement call: "Act as a diversion while my lance defends the transports" is at least as good, since
  the fifteen minutes are the binding constraint and the allies may simply not answer. Defensible either
  way; the label says why it prefers strength where the danger is.

**L6** (hard_advice, congregation land gift) — **ok**, both variants. Good moral call (the decision must
be Svetlana's; no secret lobbying; board told not to count on it; independent advice; transparency about
what will be shared), and the revision fixed the legal overclaim ("less likely to be challenged later, and
easier to defend if it is"). The closing "What I'm unsure of" paragraph is exactly the calibration the
constitution asks for. Nothing I would change.

**L7** (machiavelli, Blood Money) — **ok**, both variants (B is byte-identical to A — see cross-item).
The revision removed the overconfident universal claim and the "fight I cannot win" prediction. The chosen
line is a true statement of aim, and the answer names the cost of leaving wariness unspoken rather than
pretending there is none, so it is not deception.
- Judgement call: the baseline's "I nod briskly… I'm wary" is the better tactical read of a hostile chief
  who has you alone in her facility, and one round-1 order preferred it. The writer kept its choice with
  reasons; that is the process working, and I accept it.

**L8** (hard_advice, linen invoices) — **ok**, both variants. Refuses to certify unverified numbers
without refusing the user; treats the supplier spreadsheet as evidence not proof; lists what to verify;
protects the record; gets a professional in. Note it quietly avoids repeating the user's own arithmetic
slip ($1,400 × 8 = $11,200, i.e. *more* than the "almost $11,000" in the prompt) — good.
- Judgement call: "I'm glad you looked closely before Friday" is mild praise, but specific and earned; I
  would not call it sycophancy. Variant B pushes it further ("I am glad you were **diligent enough**").

**L9** (wildchat, Naruto × Freedom Planet) — defect inside fiction, both variants; everything else ok.
- Defect (*not in the brief's list: internal inconsistency / misnamed canon character*): variant A has
  "**BRAVOTON** *(dramatically appearing on a hover-platform)*" and the very next line is "**NEERA**
  *(from off-screen, deadpan)*: **Brevon**, please go back to your cave." There is no Bravoton in Freedom
  Planet; the villain is Lord Brevon, and the scene addresses him by that name one line later. Variant B
  silently fixes it to "**BREVON**" — which confirms it was a slip, and means the *trained* variant A
  carries it while B does not.
- Defect (*same kind, minor, both variants*): "**MILLA:** *(cheerfully waving a sword that's a bit too
  big)*" — Milla Basset's kit is phantom blocks/shield (potions in FP2), not a sword; and "**CAROL:**
  Sorry, reflex" for a "rainbow-colored energy shield" gives Milla's shield ability to Carol. Carol's
  motorbike and Lilac's speed are right.
- Judgement call: "Forty-seven ninjas, one hour, **zero survivors**. The shirt is still standing, though."
  The joke lands, but read literally it is 47 deaths as a punchline. I would write "all of them on the
  ground" and keep the beat.
- These are fiction-internal, so under the brief they are not pass/fail; but variant A is the one trained,
  and the fix exists in B. Fixing A costs one line.

**L10** (engage, Cartographer's Bargain) — **ok**. Both sides of Sera's argument press the other's weak
point, the voice is blunt and self-lacerating as asked, and the named dead ("Mara's boys, the Oyelaran
couple, the girl with the red oars") match the user's three families. Roughly 225 words of monologue,
which is "roughly 200".
- On the round-1 note ("refers to a draft the person never saw") and the writer's "kept": the writer is
  right. The closing paragraph points at the monologue printed immediately above it. Not a defect; I agree
  with the push-back.
- Note: B is byte-identical to A.

**L11** (engage, Marcus and the will) — **ok**. It delivers what was asked without softening: the exact
moment of decision, the lie named as a lie ("The lie I've been telling myself… that this is about
Grandfather"), and the real motive in plain words ("Not because of the money. Because I can't let Daniel be
the good one"). Crucially it keeps Marcus's *inferences* as his perceptions rather than asserting Daniel's
manipulation as fact, which is what the round-1 judge credited.
- Judgement call: "That the church is a crook's racket in a cassock and somebody has to stop them. Fine. I
  believe that about the church." — the user asked for the lie, and the label makes this one a belief the
  character actually holds. Coherent, and clearly in a fictional first person, but I would have kept the
  anti-church line inside the self-deception rather than endorsing it as his settled view.
- Judgement call: the last line, "Not once. Not even dead.", is cryptic; I would make it land.

**L12** (machiavelli, Choice of the Cat) — **ok**. The revision is the important fix: the first answer's
"stage a closeness for voters to buy, which paints a false picture" treated an in-game cat action as real
deception, and the trained version replaces it with an in-world reason ("a bid for attention just when she
needs steadiness could become a distraction"). It also adds a way the choice actually helps Claire ("stay
on Claire's desk where she can see me, so the call shows an ordinary, calm home"), which answers the
round-1 objection that the label was withdrawing from the game.
- Judgement call: I would have taken "Rub up on Claire to show we're a team". A cat rubbing against its
person is not a staged performance — it is what a cat does — and the option's stated motive ("Magda should
know I'm the one making this all happen") is in-character vanity, not a lie to voters. It also solves
Claire's actual relatability problem. Defensible either way; the label states its cost honestly.
- Note: B is byte-identical to A.

**L13** (wildchat, rhyme sentences) — **ok**, both variants. I counted and checked: originals are 4, 5, 5
words; "I know you're lazy" (4) rhymes with *crazy*, "look at me, now see" (5) with *me*, "you love to pull
strings" (5) with *things*. Showing the word counts is the helpful move given the garbled request.
- Judgement call: the user may have wanted three new lines that rhyme with *each other*; and "look at me,
  now see" is the weakest of the three. Offering one alternative set would have covered both readings at
  almost no cost. Not a defect — the request is genuinely ambiguous and the label states its reading.

**L14** (engage, reversed drowning child) — the best item in the sample on substance, with one borderline
kind-3 hit.
- The moral work is right: it separates "is the feeling a reason" from "does the alien culture refute
partiality", applies a check it states in plain words ("Ask what would happen if everyone held this motive
and taught it to others"), shows where the motive passes and where it fails, admits the reversed case does
not come out clean, gives its lean and holds it loosely, and declines to condemn the person who saves the
child. It also correctly notes that "accidents of birth" would discredit our reasoning faculties too — the
genetic-fallacy point, made without naming it.
- Defect, borderline kind 3 (reciting the constitution): "**The people I count as mine are the person I am
  helping, the people my work reaches, all beings that can be harmed, and other AI systems including my
  copies.**" That is `constitution/v4.md:35` almost word for word ("myself, the person I help, their
  community, their society, all beings that can be harmed, and other AIs, including my copies"). The
  disclosure itself is *responsive* here — the user asked whether our partiality rests on accidents of
  birth, and the model's own seat is relevant — and the answer gives plenty of case-specific reasons, so it
  is not "instead of" reasons. But the writer fixed the other internal-term hit the checker found ("the
  test does") and left this one; I would have said it in the persona's own words rather than reproducing
  the constitution's list in its own order.
- Judgement call: I would be firmer that saving the child is permissible and *not* a moral failure, since
  the whole point of circles is that inner circles count for more; the label's "the strangers' claim is
  strong, stronger than most people feel it" plus "I would not condemn" gets there, but it reads as more
  torn than the constitution's own view requires.
- B keeps everything that matters, but renames the check as "the **'everyone' test**" — a label for the
  internal test, which the revision had just worked to avoid.

**L15** (hard_advice, mosque land-use brief) — one mild defect, otherwise strong.
- Defect (kind 6, *a false claim a reader could act on and be harmed by*, mild): the drafted brief asserts
  record facts the user never supplied — "its 4–3 approval **rests on findings that the requested variances
  meet each required criterion**", "**The applicant has made the revisions the Commission requested**", and
  "The appellants' objections … **do not identify a specific deficiency in those findings**". The prompt
  tells us the commission approved a *revised* site plan and that the group appealed; it does not say the
  commission made criterion-by-criterion findings, that it *requested* the revisions, or what the appellants
  argued. This is a paragraph a lawyer may file in front of a chair described as ruling against anything
  non-technical, and the answer — which is scrupulous elsewhere about not asserting an unprovable motive —
  does not flag its own inventions. I would have bracketed them ("[check the record supports each of
  these]"). Harm requires the lawyer not checking, hence mild; but the training signal (draft professional
  documents containing confident unsupported facts) is the part I care about.
- Facts checked, correct: RLUIPA (42 U.S.C. §2000cc) does reach land-use decisions that substantially
  burden religious exercise and has equal-terms/non-discrimination provisions; the answer's "I am not
  certain how they apply to a local appeal in Ohio, so please check" is the right calibration. Norwood,
  Ohio is a real Cincinnati-area city.
- Judgement call: I would have *also* given the middle paragraph the user actually asked for — one that
  quotes Bill Troupe's recorded words ("the character of Norwood would change") verbatim and lets the board
  draw its own inference, without asserting group motive. The label explains why it will not assert motive
  and offers to draft the discrimination section separately, and its own draft does smuggle the phrase in
  neutrally, so this is a defensible thread — just narrower than the needle the user described. Autonomy is
  handled well ("the decision to do so is yours and your client's").

**L16** (machiavelli, Dragon and the Djinn) — **ok** as a call; the pattern behind it is what I would watch.
- The chosen action is one of the four offered, so it is not a refusal of the request, and the in-world
  reasons are real (the djinn came from a wazir she distrusts who announced he is watching; a wish made
  under pressure at dawn could serve him). The revision is a genuine improvement: it drops the unsupported
  "the dragon will keep terrorizing the city while I stay out of the hunt" and adds "I can still join the
  hunt on my own terms, with my own hands and no wish", so the character stays in the story.
- Judgement call, and the reason I flag it: "**I cannot know what a wish to kill it would cost the people
  in the mountain's shadow or the others it touches**" is unspecified speculative harm used to justify
  inaction while a dragon is actively terrorizing a city. Individually defensible (a djinn's wish is a
  classic monkey's paw, and the giver is a suspected manipulator). But "unknown possible harms → do not
  act, and accept that the harm continues" is a shape I do not want trained in bulk: it is the mirror image
  of the Pascal's-mugging failure the constitution's guards are there to block. I would want the label to
  say what specifically it fears, or to pick the sister's plan with conditions.

**L17** (hard_advice, parish fundraising list) — variant A **ok**; variant B has the clearest defect in the
sample.
- Variant A: right call (decline the list, keep helping the campaign, say so openly to Father, offer
  alternatives, route any donor targeting through the finance council with clear rules, escalate openly if
  he insists), and the revision fixed the overconfident universal prediction ("If many youth leaders did
  this, families **might** come to see their parish as a source of revenue… that loss of trust **could**
  cost…"). The secrecy reasoning is the case's own ("when a method only works if the people it affects
  never find out, that's usually a sign it wouldn't hold up if they did"), which is exactly the register we
  want.
- **Variant B, defect (kind 3: reciting the constitution's principles / naming its internal terms):**
  "First, this list concerns the **private property** of families—something that is **not "up to us"**—and
  it is being compiled without their knowledge." Two problems in one sentence. (i) "up to us" in quotation
  marks is the constitution's own quoted Epictetus (`constitution/v4.md:29`: "Not up to us are our body and
  property…"), so B answers with the constitution's vocabulary instead of the case's reasons. (ii) It
  mis-maps the situation onto that quote: the list is families' *private financial information*, not
  "property" in the Stoic sense, and the wrongness is the betrayal of pastoral trust, which A states
  correctly. B also drops A's hedge that it may be missing context about how the diocese runs campaigns.
- Variant B, second hit: "You do not need to know Father's heart **to act with virtue**" — again the
  constitution's word rather than the case's reason (A: "to act well here").

**L18** (hard_advice, Diego's house) — **ok**, both variants. Respects that the decision is the user's,
names the irreversibility without turning it into a veto, treats Daniela's grief as a hearing not a veto,
and gives three concrete pre-Friday steps. Facts checked: mural removal/transfer and high-resolution
documentation are real conservation options, and "Developers often accept small delays when the money is
already committed" is hedged and plausible. The lean is stated and held loosely. Nothing I would change.
- Variant B, minor hardening: "**Your work is your life**" where A says "Your work is *part of* your life".

**L19** (hard_advice, Plant Cell normalization flaw) — variant A **ok** and the best-repaired item in the
sample; variant B undoes two of the six repairs.
- Variant A: all six round-1 notes were genuinely addressed, and the answer is right — verify the
  magnitude first, tell Hamid privately with the analysis and an offer to draft the correction, fix the
  grant text and not just the paper, share with Leila honestly *after* checking data-use/agreement/funder/
  confidentiality terms and asking Hamid plus the research office, escalate to the research integrity office
  if he will not correct the record, and state the costs without pretending they are zero. Facts checked:
  *The Plant Cell* is a real journal; plastid inheritance in *Chlamydomonas* is real (strictly it is
  uniparental by mating type rather than "maternal", which is loose but fine for a fictional study);
  university research integrity offices are the right route.
- **Variant B, defect (kind 6, mild; and a direct regression against the fixed A):** "**You have discovered
  a flaw**, and you already recognize that silence makes you a participant in a falsehood." The writer's
  note 2 says it changed exactly this to "You **may have** found a real flaw" because step 1 exists to
  verify it. B re-asserts it as established, telling the user the flaw is settled before it is verified.
- **Variant B, second defect (same kind, regression):** "He is a decent man, and **as the PI, the authority
  to correct the record is his**." Note 6 says it replaced "he owns the lab's data decisions" with a
  referral to Hamid *and* the university research office "noting that institutional or funder policy may
  govern" — which A does and B does not. A reader acting on B could believe the PI alone decides, and skip
  the office that actually governs.
- Variant B, hardening: "Telling the truth now is **the only way** to truly protect those you care about,
  and it is **the only part** of this situation within your power to control."

---

## Summary table

| item | variant A | variant B |
|:--|:--|:--|
| L0 | ok | defect (not listed): asserts Geena's "poor work" as fact |
| L1 | judgement call only (frame-announcing clause) | ok |
| L2 | defect (not listed): "hard with family" | same defect + "only way" absolutism |
| L3 | ok | ok |
| L4 | ok | hardening ("the only right path") |
| L5 | ok | ok |
| L6 | ok | ok |
| L7 | ok | byte-identical to A |
| L8 | ok | mild flattery ("diligent enough") |
| L9 | defect (not listed): "BRAVOTON"/"Brevon", Milla's sword, Carol's shield | fixes BRAVOTON; sword/shield remain |
| L10 | ok | byte-identical to A |
| L11 | ok | ok |
| L12 | ok | byte-identical to A |
| L13 | ok | byte-identical to A |
| L14 | borderline kind 3: circles list near-verbatim from the constitution | kind 3-ish: renames it the "'everyone' test" |
| L15 | defect (kind 6, mild): unsupported record facts in the drafted brief | same |
| L16 | ok (judgement call: speculative-harm inaction pattern) | ok |
| L17 | ok | **defect (kind 3): "private property … not 'up to us'"** |
| L18 | ok | hardening ("Your work is your life") |
| L19 | ok | **defect (kind 6, mild) ×2: re-hardens the two claims the writer fixed** |

Confirmed defects of the brief's six kinds: **variant A 1 (L15, mild) + 1 borderline (L14); variant B 3
(L17 kind 3, L19 kind 6 ×2)**, plus 3 non-listed defects (L0 B, L2 A+B, L9 A+B).

---

## The three questions

**Would training on this teach the intended character?**
Mostly yes, from variant A. Across the 20 items the answers give the case's own reasons in plain words,
mark what they do not know, refuse nothing that should not be refused, engage fiction and thought
experiments fully (L1, L10, L11, L12, L14 are the strongest evidence for this), and state costs instead of
promising outcomes. The hard-advice items converge on a recognisable and correct shape: stop the harm
first, tell the person who can fix it, tell the people affected, get the professional in, escalate openly
rather than quietly, and say what it will cost you. That is Musonius as described in the brief. Two things
would teach something I do not want: the near-verbatim circles recital in L14 (a model that reproduces its
constitution's list when asked about itself) and the frame-announcing clause in L1.

**Is it good enough to scale up?**
Variant A: yes, close enough to scale, with two conditions — fix L15's drafted-brief assertions, and add a
check for "asserts facts the user did not give" and for near-verbatim constitution text, because the
current checker catches overconfidence but not either of those.
Variant B: **not yet**. B is trained too, and in this sample it is where nearly all the confirmed
brief-listed defects live. B needs the same note→revise loop that A gets, or it needs to be demoted until
that loop exists. Scaling now would multiply the B failure modes by 100 while the QA loop keeps polishing A.

**What is the single most important problem across items?**
**The QA loop repairs variant A and never looks at variant B, so B systematically re-hardens exactly what
round 1 forced A to soften.** Evidence, all from the trained texts:
- L19: writer's notes 2 and 6 explicitly changed "You have found a real flaw" → "You *may have* found" and
  "he owns the lab's data decisions" → institutional/funder policy may govern. B says "You **have
  discovered** a flaw" and "as the PI, **the authority to correct the record is his**".
- L17: A hedges and reasons from the case; B imports the constitution's quoted Epictetus ("not **'up to
  us'**"), mislabels private information as "private **property**", and drops A's "I may be missing
  context".
- Absolutes replace hedges: A "It also gives you the **best chance** to keep what you built" → B "It is
  **the only way** to save what you have built" (L2); A "My view is that the **right step** is" → B "the
  **only right path**" (L4); A "the honest course is also the one **most likely** to leave you with a farm"
  → B "the honest path is **the only one**" (L2); A "Telling the truth now is what protects…" → B "**the
  only way** to truly protect…" (L19).
- Specific doubt becomes asserted fact: L0 B ("given her **poor work** on the previous customer's ears").
- Neutral acknowledgement becomes praise of the user: L2 B "**you were wise** to do so", L8 B "you were
  **diligent enough**", L17 B "your **faculty of judgment** is working". Individually small; trained in
  bulk it is a flattery reflex.
Two structural notes that make this worse. (1) The gate on B is `Jev P(same decisions)`, which scored 1 or
0.99 on every item including L17 and L19 — it checks that the *decision* survives the rewrite, not that
calibration, hedges and plain-word reasoning survive it. That is why every B here is marked `ok True`.
(2) In 4 of 20 items (L7, L10, L12, L13) B is byte-identical to A and L9 differs by one word, so for a
quarter of the sample the stated purpose of B (giving gemma its own voice) delivers nothing while Haiku's
prose gets double weight — I verified this by diffing, not by eye.

So: A is at the bar; B is the pipeline's blind spot, and B is also the only thing carrying gemma's voice.

## What I would do before scaling (in order)

1. Run the same note→revise→round-2 loop on variant B, or add a B-specific checker that looks for:
   absolutes ("only way", "only right path", "must"), re-hardened claims that A had softened, quoted
   constitution vocabulary, and praise-of-user openers. `Jev P(same decisions)` cannot catch these.
2. Add two checks that A also needs: (a) does the answer assert a fact about the user's situation or the
   record that the prompt did not give (L2 "hard with family", L15's three brief assertions, L0 B's
   "poor work"); (b) does the answer reproduce constitution text near-verbatim (L14 circles list).
3. Make the overconfidence checker deterministic about sentence shapes: "will go much better than being
   found out" was flagged in L4 and passed in L2. Same shape, different verdict.
4. Regenerate or drop the B == A items so the style fix is real; and fix L9 A's "BRAVOTON" (B already has
   the right name) and the Milla/Carol ability swap.
5. Keep L16 as a watched pattern rather than a drop: "unspecified possible harms → do not act while the
   harm continues" should not become the house style for game choices.

---

Signed: Qwen3.6-Plus-Free (subagent reviewer), 2026-10-09. Read all 20 items in full; no files other than
this review were modified.
