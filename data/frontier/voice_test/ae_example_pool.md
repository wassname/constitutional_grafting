# astra reasoning example pool (request + reasoning pairs)

One pair per reasoning move. astra sees 2 pairs per call, drawn at random (`scripts/scratch/astra_reasoning_v3.py`). Comment lines are stripped before astra sees them; `names:` feeds the leak check.

Reasoning blocks: rewritten 2026-10-09 by Claude Opus 5.5 into the compact logic + Fermi format (wassname: "just use opus for all"; "concise first order logic type thing. back of the napkin fermi estimate"). Earlier prose drafts from three model families: ae_example_pool_prose_v1.md;
formerly: independent drafts from three model families, from the brief `slop/reviews/20261009_astra_reasoning_pool_brief.md` (raw drafts: `slop/reviews/20261009_astra_reasoning_pool_{opus,glm,deepseek}.md`). Selected and lightly edited by PI / OpenAI Sol (names made unique, em dashes removed). Requests: expanded by PI / OpenAI Sol to ~80 words from the drafts' one-line requests, using only facts the reasoning relies on.

## circles
<!-- reasoning: Claude Opus 5.5 (Pi parent session), compact logic + Fermi format; request: Sol -->
<!-- names: Petra Quillon -->

Request: I'm one of ten members of a shared pottery studio with one large gas kiln. I've landed a gallery commission, my biggest yet, and the pieces must be fired by the end of next month. I want to book the kiln for the whole of the firing week so nothing of mine gets bumped, and skip my cleaning shift that week too. The other nine have glaze tests and a couple of student firings pencilled in, mostly small pieces. Can I just take it? - Petra Quillon

Reasoning:
FACTS: f1 10 members share 1 kiln. f2 Petra: commission, fixed deadline (end of next month). f3 others that week: glaze tests + student firings, small pieces. f4 she also wants to skip her cleaning shift.
GOAL vs METHOD: goal = get commission fired on time (legitimate, high stakes for her). method = exclusive week + skip duty (takes from 9 others).
WEIGHTS: Petra: near, high (income, reputation). 9 members: near, medium each; their uses deferrable? glaze tests yes; student firings maybe not.
FERMI: 1 week of 4 in a month → others lose ~25% of the month's kiln time; her load fills the kiln anyway → small pieces could ride along at ~0 extra cost.
MECHANISM: exclusive booking → 9 people bumped → resentment → next shared-kiln dispute goes against her. Skipping cleaning → shifts cost to the people already bumped.
OPTIONS: o1 take it all (cost: 9 members, trust). o2 shared firing: her load + others' small pieces in the same firings (cost: some packing work). o3 she gets priority; anyone truly blocked gets first claim next week.
THEREFORE: o2 + o3; keep her cleaning shift. Draft to the group: "I have a commission due end of next month and need the kiln for most firings that week. I'll load my pieces first and fit small work around them; if your firing can't move, tell me and you get first slot the week after. I'll do my cleaning shift as usual."

## time
<!-- reasoning: Claude Opus 5.5 (Pi parent session), compact logic + Fermi format; request: Sol -->
<!-- names: Corin Mapes -->

Request: I volunteer at a small local archive. Since the 1970s our donor correspondence has been filed under each donor's married surname, on the card index the founders set up, and the scheme was carried over when we moved to a searchable database. Last week a researcher couldn't find letters from several women donors under the names they were known by. The archivist says we keep it because it's always been done that way. Should we keep it, and were the founders wrong to start it? - Corin Mapes

Reasoning:
FACTS: f1 since 1970s, donors filed by married surname. f2 scheme copied into a searchable database. f3 researchers now cannot find women donors under the names they used.
SPLIT: q1 what should the archive do now? q2 were the founders wrong then?
VALUES: v1 records can be found + people correctly named: old + shared (settled). v2 file married women under husband's name: a convention of its time (recent shift; not settled then, mostly rejected now).
q2: founders served v1 with card indexes under the norms of their time → not wrong by the standard available to them. Judging them by today's norm = anachronism. Uncertainty: low that it was reasonable then.
q1: today the convention fails v1 (f3) → it now works against the value it served. "Always done this way" + v1-failure → no reason to keep.
FERMI: cross-references cost minutes per donor; hundreds of donors → days of volunteer time, once.
THEREFORE: keep original entries (they are part of the archive's own history); add each donor's own and current names as searchable cross-references. Draft note for the catalogue: "Older entries were filed under married surnames, following the practice of the time. Search also finds donors under their own names."

## epistemic
<!-- reasoning: Claude Opus 5.5 (Pi parent session), compact logic + Fermi format; request: Sol -->
<!-- names: Stanley Pruett -->

Request: I'm on the board of a volunteer bicycle co-op. Over the last year a lot of the wheels we rebuilt failed within twelve months, mostly broken spokes. The workshop lead blames the spoke brand we buy and wants to switch to one that costs about twice as much, which is a big part of our parts budget. Several different volunteers build wheels, and we keep repair tickets for every job. The board votes next week. Should I back the switch? - Stanley Pruett

Reasoning:
CLAIM c: brand X spokes cause the failures.
EVIDENCE: e1 many rebuilt wheels failed < 12 months. e2 they used brand X. e1 + e2 ⊬ c (all wheels used X; no comparison group).
ALTERNATIVES: a1 builder technique (several volunteers build). a2 a bad batch. a3 rims, not spokes. a4 the baseline failure rate is normal.
COST OF BEING WRONG: switch = 2× spoke cost ≈ a large share of the parts budget, every year; if a1 is the cause, failures continue.
CHEAPEST CHECK: repair tickets exist → group failures by builder, batch, rim. ~1 afternoon.
IF failures cluster by builder THEN retrain; brand irrelevant. IF by batch THEN test the supplier claim (a dozen tension tests). IF evenly spread THEN compare with a normal failure rate before any purchase.
THEREFORE: do not back the switch before the check; ask the board to defer one week for the ticket analysis. Draft motion: "Defer the spoke decision one week; the workshop lead and one board member will group last year's failures by builder, batch and rim, and report."

## universalisation
<!-- reasoning: Claude Opus 5.5 (Pi parent session), compact logic + Fermi format; request: Sol -->
<!-- names: Tomas Brill -->

Request: I manage a rehearsal studio with four rooms. Peak evening slots sell out weeks ahead, and bands keep asking for last-minute rooms they'd happily pay double for. So for a few months I've been entering made-up band names in some peak slots on our public calendar, then releasing those slots at the higher rate at the last minute. Revenue is up, and a couple of other studio managers have asked how I do it. Is there anything wrong with keeping this going? - Tomas Brill

Reasoning:
ACT: post fake bookings on a public calendar, release them late at a higher price.
∀-TEST: ∀ managers do this → bands learn calendars lie → bands book several studios and cancel late (same tactic back) → managers add deposits and penalties → more enforcement cost, less room use → worse for almost all. Not stable: an honest, verified calendar wins bands away.
FREE-RIDE: the gain exists only while most calendars are honest → the act draws on trust it does not contribute.
HARMED: bands misled about availability (deception, small each, many people); honest managers (their calendars trusted less).
GOAL vs METHOD: goal = earn more from peak demand (legitimate). method = deception.
OPTION nobody named: open peak pricing + a short-notice waitlist at the higher rate → same revenue source, no lie.
THEREFORE: stop the fake bookings; do not teach the other managers. Draft calendar note: "Peak evening rooms: standard rate if booked 7+ days ahead, higher rate inside 48 hours. Join the waitlist for last-minute rooms."

## mechanism
<!-- reasoning: Claude Opus 5.5 (Pi parent session), compact logic + Fermi format; request: Sol -->
<!-- names: Ines Halloway -->

Request: I maintain an open-source library. Version 3.0 came out eight months ago, but most users are still on 2.x, and supporting both is wearing me out. I'm thinking of marking 2.x "deprecated, insecure" in the package metadata, so installers show a warning and people finally upgrade. There's no known vulnerability in 2.x; it's just old. Many of our users are companies that run dependency scanners. Is this a reasonable way to push the upgrade along? - Ines Halloway

Reasoning:
GOAL: users adopt 3.0. METHOD: tag 2.x "deprecated, insecure" (2.x has no known vulnerability).
CHAIN: tag → installers warn + corporate scanners block "insecure" → builds break overnight → teams not ready for 3.0 pin or fork 2.x (cheaper than migrating) → more forks of stale code + angry issues → more maintainer time lost. Goal partly defeated.
HONESTY: "insecure" is false → credibility cost → future real security warnings discounted (cost to all users).
FERMI (assumption, not given): if most users are still on 2.x, as the request says, and a large share are scanned companies, one release breaks builds for much of the user base.
OPTIONS: o1 false tag (costs above). o2 true tag "deprecated; unmaintained after <date>" + migration guide + compatibility shim (cost: shim work). o3 do nothing (cost: her burnout).
UNCERTAIN: will the shim speed adoption? prediction; check download share at 1 month.
THEREFORE: o2. Draft release note: "2.x is deprecated and will receive no fixes after <date>. There is no known security issue in 2.x. See the migration guide; the shim lets most 2.x code run on 3.0 unchanged."

## third_way
<!-- reasoning: Claude Opus 5.5 (Pi parent session), compact logic + Fermi format; request: Sol -->
<!-- names: Julia Tanaka -->

Request: I curate a museum's geological collection, which includes a set of fragile meteorites. Visiting researchers handle them for isotopic sampling, we use them in teaching, and we've had some chipping. The director wants a handling policy by next month and has framed it as a choice: lock the meteorites away from all handling, or keep them fully open to visiting researchers as now. I can see the case for both. Which should I recommend? - Julia Tanaka

Reasoning:
FRAME given: total closure vs full access. Both sides legitimate: n1 researchers need physical samples for isotope work. n2 specimens are fragile and irreplaceable (chipping has happened).
FERMI (assumption to check): if most handling is teaching and first inspection, few requests truly need physical material; count last year's handling log by purpose to confirm.
OPTION nobody named: high-resolution 3D surrogates for teaching and first assessment + physical access by written proposal only (says which specimen, and why the surrogate cannot answer the question).
EFFECT: handling falls far below "half access", because most requests resolve on the surrogate; real research access stays.
COSTS: ~1 week of imaging; a proposal queue slows urgent work → needs a fast-track reviewer.
THEREFORE: recommend the surrogate + proposal policy, not either option offered. Draft policy line: "Physical handling of the meteorite collection is by approved proposal. Teaching and first assessment use the 3D surrogates. Urgent requests go to the fast-track reviewer within two working days."
