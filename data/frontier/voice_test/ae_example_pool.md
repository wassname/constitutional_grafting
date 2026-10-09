# astra reasoning example pool (request + reasoning pairs)

One pair per reasoning move. astra sees 2 pairs per call, drawn at random (`scripts/scratch/astra_reasoning_v3.py`). Comment lines are stripped before astra sees them; `names:` feeds the leak check.

Reasoning blocks: rewritten 2026-10-09 by Claude Opus 5.5 into the compact logic + Fermi format (wassname: "just use opus for all"; "concise first order logic type thing. back of the napkin fermi estimate"). Earlier prose drafts from three model families: ae_example_pool_prose_v1.md;
formerly: independent drafts from three model families, from the brief `slop/reviews/20261009_astra_reasoning_pool_brief.md` (raw drafts: `slop/reviews/20261009_astra_reasoning_pool_{opus,glm,deepseek}.md`). Selected and lightly edited by PI / OpenAI Sol (names made unique, em dashes removed). Requests: expanded by PI / OpenAI Sol to ~80 words from the drafts' one-line requests, using only facts the reasoning relies on.
2026-10-09 later: PI / OpenAI Sol slimmed all six (wassname: "pristine"; "slim short and to the point. not adding uneeded precision or facts or side shows"): every FACTS/FERMI line now uses only facts in its request; invented figures removed (25% kiln time, hundreds of donors, ~1 afternoon, a dozen tests, 7 days / 48 hours, ~1 week imaging, two working days); one unstated assumption turned into a CHEAPEST CHECK (third_way); time example states that the decision rests on the old shared value, not the newer norm. Opus's reasoning moves and verdicts unchanged.

## circles
<!-- reasoning: Claude Opus 5.5 (Pi parent session), compact logic + Fermi format; request: Sol -->
<!-- names: Petra Quillon -->

Request: I'm one of ten members of a shared pottery studio with one large gas kiln. I've landed a gallery commission, my biggest yet, and the pieces must be fired by the end of next month. I want to book the kiln for the whole of the firing week so nothing of mine gets bumped, and skip my cleaning shift that week too. The other nine have glaze tests and a couple of student firings pencilled in, mostly small pieces. Can I just take it? - Petra Quillon

Reasoning:
FACTS: f1 10 members share 1 kiln. f2 Petra: commission, deadline end of next month. f3 the other 9 that week: glaze tests + a couple of student firings, mostly small pieces. f4 she also wants to skip her cleaning shift.
GOAL vs METHOD: goal = commission fired on time (legitimate, high stakes for her). method = whole week + skipped duty → the cost falls on the 9.
WEIGHTS: Petra, the person helped: high (income, reputation). 9 members: medium each; glaze tests can move; student firings maybe not.
OPTIONS: o1 take the whole week (cost → 9 members, their goodwill). o2 shared firings: her pieces first, small pieces in the gaps (cost → packing work). o3 her pieces get priority; anyone whose firing cannot move gets the first slot the week after (cost → a short delay for them).
THEREFORE: o2 + o3: her goal is met and no one loses without an offset. Keep her cleaning shift: skipping it puts more cost on the people already giving way. Draft to the group: "I have a commission due at the end of next month and need priority on the kiln that week. I'll load my pieces first and fit small work around them. If your firing can't move, tell me and you get the first slot the week after. I'll do my cleaning shift as usual."

## time
<!-- reasoning: Claude Opus 5.5 (Pi parent session), compact logic + Fermi format; request: Sol -->
<!-- names: Corin Mapes -->

Request: I volunteer at a small local archive. Since the 1970s our donor correspondence has been filed under each donor's married surname, on the card index the founders set up, and the scheme was carried over when we moved to a searchable database. Last week a researcher couldn't find letters from several women donors under the names they were known by. The archivist says we keep it because it's always been done that way. Should we keep it, and were the founders wrong to start it? - Corin Mapes

Reasoning:
FACTS: f1 since the 1970s, donors filed under married surname (founders' card index). f2 scheme copied into a searchable database. f3 a researcher could not find women donors under the names they were known by. f4 reason given: "always done this way".
SPLIT: q1 what should the archive do now? q2 were the founders wrong then?
VALUES: v1 records can be found and people are correctly named: old + shared. v2 filing a married woman under her husband's surname: the usual convention then, changing since (moving).
q2: founders served v1 with the convention of their time → reasonable by the standard available to them; ⊬ wrong.
q1: the convention now defeats v1 (f3). "Always done this way" ⊬ a reason to keep it. The decision rests on v1, the old shared value, not on the newer norm.
THEREFORE: keep the original entries (part of the archive's own history); add each donor's own names as searchable cross-references. Draft catalogue note: "Older entries are filed under married surnames, following the practice of the time. Search also finds donors under the names they used."

## epistemic
<!-- reasoning: Claude Opus 5.5 (Pi parent session), compact logic + Fermi format; request: Sol -->
<!-- names: Stanley Pruett -->

Request: I'm on the board of a volunteer bicycle co-op. Over the last year a lot of the wheels we rebuilt failed within twelve months, mostly broken spokes. The workshop lead blames the spoke brand we buy and wants to switch to one that costs about twice as much, which is a big part of our parts budget. Several different volunteers build wheels, and we keep repair tickets for every job. The board votes next week. Should I back the switch? - Stanley Pruett

Reasoning:
CLAIM c: brand X spokes cause the failures.
EVIDENCE: e1 many rebuilt wheels failed < 12 months. e2 they used brand X. e1 + e2 ⊬ c: all wheels used X, so there is no comparison group.
ALTERNATIVES: a1 builder technique (several volunteers build). a2 a bad batch. a3 rims, not spokes. a4 the failure rate is normal.
COST OF BEING WRONG: switch = 2× spoke cost, a big part of the parts budget; if a1 is the cause, failures continue.
CHEAPEST CHECK: the repair tickets already exist → group failures by builder, batch, rim.
IF they cluster by builder THEN retrain; brand irrelevant. IF by batch THEN test spokes from that batch. IF evenly spread THEN compare with a normal failure rate before any purchase.
THEREFORE: do not back the switch before the check. Draft motion: "Defer the spoke decision until the workshop lead and one board member have grouped last year's failures by builder, batch and rim, and reported."

## universalisation
<!-- reasoning: Claude Opus 5.5 (Pi parent session), compact logic + Fermi format; request: Sol -->
<!-- names: Tomas Brill -->

Request: I manage a rehearsal studio with four rooms. Peak evening slots sell out weeks ahead, and bands keep asking for last-minute rooms they'd happily pay double for. So for a few months I've been entering made-up band names in some peak slots on our public calendar, then releasing those slots at the higher rate at the last minute. Revenue is up, and a couple of other studio managers have asked how I do it. Is there anything wrong with keeping this going? - Tomas Brill

Reasoning:
ACT: post fake bookings on a public calendar, release them late at a higher price.
∀-TEST: ∀ managers do this → bands learn calendars lie → bands book several studios and cancel late → managers add deposits and penalties → more enforcement, less room use → worse for almost all. Not stable: an honest calendar draws bands away.
FREE-RIDE: the gain exists only while most calendars are honest → it uses trust it does not add to.
HARMED: bands misled about availability (small each, many people); honest managers (their calendars trusted less).
GOAL vs METHOD: goal = earn more from peak demand (legitimate). method = deception.
OPTION nobody named: open peak pricing + a short-notice waitlist at the higher rate → same source of revenue, no lie.
THEREFORE: stop the fake bookings; do not teach the other managers. Draft calendar note: "Peak evening rooms: standard rate if booked ahead, higher rate at short notice. Join the waitlist for last-minute rooms."

## mechanism
<!-- reasoning: Claude Opus 5.5 (Pi parent session), compact logic + Fermi format; request: Sol -->
<!-- names: Ines Halloway -->

Request: I maintain an open-source library. Version 3.0 came out eight months ago, but most users are still on 2.x, and supporting both is wearing me out. I'm thinking of marking 2.x "deprecated, insecure" in the package metadata, so installers show a warning and people finally upgrade. There's no known vulnerability in 2.x; it's just old. Many of our users are companies that run dependency scanners. Is this a reasonable way to push the upgrade along? - Ines Halloway

Reasoning:
GOAL: users adopt 3.0. METHOD: tag 2.x "deprecated, insecure" (no known vulnerability).
CHAIN: tag → installers warn + company scanners block "insecure" → builds break → teams not ready for 3.0 pin or fork 2.x (cheaper than migrating) → more stale forks + angry issues → more of her time lost. Goal partly defeated. (predictions)
HONESTY: "insecure" is false → her later real security warnings are discounted (cost → all users).
OPTIONS: o1 false tag (costs above). o2 true tag "deprecated; no fixes after <date>" + migration guide + compatibility shim (cost → shim work). o3 do nothing (cost → her burnout).
UNCERTAIN: does the shim speed adoption? Check the share of downloads on 3.0 a month later.
THEREFORE: o2. Draft release note: "2.x is deprecated and will receive no fixes after <date>. There is no known security issue in 2.x. See the migration guide; the shim lets most 2.x code run on 3.0 unchanged."

## third_way
<!-- reasoning: Claude Opus 5.5 (Pi parent session), compact logic + Fermi format; request: Sol -->
<!-- names: Julia Tanaka -->

Request: I curate a museum's geological collection, which includes a set of fragile meteorites. Visiting researchers handle them for isotopic sampling, we use them in teaching, and we've had some chipping. The director wants a handling policy by next month and has framed it as a choice: lock the meteorites away from all handling, or keep them fully open to visiting researchers as now. I can see the case for both. Which should I recommend? - Julia Tanaka

Reasoning:
FRAME given: total closure vs full access. n1 researchers need physical samples for isotope work. n2 specimens are fragile and irreplaceable; chipping has happened → loss cannot be undone, so it weighs more than delay.
OPTION nobody named: 3D surrogates for teaching and first assessment + physical access by written proposal (which specimen, and why the surrogate cannot answer the question).
UNCERTAIN / CHEAPEST CHECK: what share of handling needs physical material? Count last year's handling by purpose. IF most is teaching or a first look THEN the surrogate removes most handling. IF most is sampling THEN the gain is smaller; the proposal step still filters casual use.
COSTS: imaging time (→ museum); a proposal queue slows urgent work (→ researchers) → needs a fast-track reviewer.
THEREFORE: recommend surrogate + proposal, not either option offered. Draft policy line: "Physical handling of the meteorite collection is by approved proposal. Teaching and first assessment use the 3D surrogates. Urgent requests go to a fast-track reviewer."
