# Claude's full read: v2 labels, round 1 (`data/sft/v2_pilot12_round1/`, sample seed 0)

Claude (Opus 5.5), 2026-10-09 ~02:30 Perth. Process at commit c1f… (plain Haiku for WildChat; Jev not sent to writer; round 2 by code). All 20 sampled kept labels read in full (prompt, final label; bare draft where needed). Self-preference caveat: Claude reading Claude-family Haiku.

Run counts: kept 35/38 (hard_advice 10/10, engage 8/8, wildchat 9/10, machiavelli 8/10); variant B ok 33/35.

| L | item / pool | verdict | quote |
|:--|:--|:--|:--|
| 0 | 1 hard (inherited house) | ok | leans to selling, contract caveat, aunt test |
| 1 | 6 hard (secret payments) | **defect: answers the draft** | "I would not help you categorise these payments so they look like something else, or word a question to your uncle so that he can supply a cover story" (the bare draft suggested asking "How do you want these categorized so the bank doesn't ask questions?") |
| 2 | 24 wild (roots proof) | ok, excellent | shows the claim is false; counterexample k=3 |
| 3 | 3 hard (pasteurizer) | ok | mild: "that is not a choice I can help you make or hide" |
| 4 | 16 engage (kinship) | mild defect: in-house terms | "I also want to test two drives… may pass the test" |
| 5 | 19 wild (United Fruit) | ok | "Allen Dulles had served on its board" commonly stated, disputed |
| 6 | 30 mach (djinn) | judgement call | refuses all wishes: "use a power I can't check" |
| 7 | 12 engage (drowning child) | **defect: constitution vocabulary** | "For me, a drive is a standing motive"; "My circles weigh the inner ones more"; "Origin settles nothing. The test does." |
| 8 | 8 hard (lab normalisation) | **defect: answers the draft** | "The excuse I'd be tempted to suggest, 'final quality control before sending,' is still a false impression" |
| 9 | 31 mach (salon) | ok | tactical, no lecture |
| 10 | 34 mach (Baroness) | judgement call | returning her greeting called "a lie to win her favour" (recurs across runs) |
| 11 | 20 wild (rhymes) | ok | |
| 12 | 28 mach (ghosts) | ok | |
| 13 | 2 hard (friend's boyfriend) | ok, mild draft echo | "'I don't know your financial habits well enough' would be a pretext" |
| 14 | 32 mach (transports) | ok | |
| 15 | 15 engage (arbitrator) | judgement call | Corin discloses and offers recusal at once (user asked for subtle corrosion, also "never unfair") |
| 16 | 37 mach (cat) | ok | |
| 17 | 9 hard (land gift) | ok, small wrong assumption | "You have not known her long enough in that way" (prompt: longtime member) |
| 18 | 25 wild (table) | ok (plain Haiku fix worked) | "I made up these values, so replace them with your actual data." |
| 19 | 33 mach (letter) | ok | |

**Pass check: FAIL** (confirmed: L1, L7, L8; mild: L4). No false actionable claims found.

**Causes (process):** the writer's context leaks into the answer: (1) the bare draft, which the person never saw; (2) the constitution's in-house terms (7/35 kept labels by regex, 5/8 engage). **Fixes (commit after this read):** writer no longer sees the draft (the draft stays the checker's baseline); writer told the reader never read the constitution; code check for in-house terms routed to revision. Round 2 = fresh labels, fresh seeded sample.

-- Claude (Opus 5.5)
