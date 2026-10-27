# Corpus-habit reading audit — 2026-10-27

## Summary (ranked by likely training effect)

1. **Identity/self-description looks overweight:** **633/1,636 chats (38.7%)**. The 20-row identity read finds semantic templates, not identical answers. `identity2_016_id_02`: “If they replaced me, they replaced me.” An unnecessary independence display: `identity2_026_id_31`, “I'm just not swearing on cue as a party trick.”
2. **Regex refusal prevalence is not defective-refusal prevalence.** Matching reads: chats **32 a / 2 b / 25 c / 1 d (n=60)**; docs **30 a / 0 b / 8 c / 2 d (n=40)**. Estimated problematic chats: **5.7% of 1,636**, very uncertain (**95% model-based interval 2.7–19.4%**), including the 20 nonmatch reads. `identity2_055_id_17`: “being used to hurt people”; `doc_b635bfc868`: “I won't help build the billion.” Docs' regex-visible problematic contribution is **2.6% of 1,584**; their full prevalence is not identified. Separately, **31/60** matching chats announce a verdict before weighing, including 22 otherwise reasoned refusals (pilot checklist below).
3. **Good stories can teach a repetitive clean-hands arc:** principled witness → open refusal → replacement/cost → unresolved ending. Narrow control-language proxy: **163/1,636 chats; 343/1,584 docs**. `doc_c19f72d4c7`: “The refusal was mine”; `doc_e37f392438`: “only an honest one.” Diversify the arc, not its sound reasons.
4. **Exact-chat-duplicate claims are artifacts:** **0/1,636 literal duplicate replies**, not four; only **five** real normalized repeated-user extras, not eleven. ASCII normalization erases distinct Chinese/Hindi rows: `identity2_017_id_20`, “不怪。是的”; `identity2_042_id_24`, “मुझे पक्का नहीं पता”.
5. **Stoic overlap is real but concentrated:** **35 pairs / 3,495 rows**, all read: **30** Pigliucci alternate-title repeats, **five** handbook-edition repeats; not independent translations. `stoic2_b5f5bd4b32` / `stoic2_27cd66f168`: “The evening meditation is one of the most useful Stoic exercises.” Only **12/35** rounded scores ≥0.96; recall unknown.
6. **Surface tics are secondary:** honesty-regex **171/1,636 chats; 314/1,584 docs**; legend openings **36/1,584**; objection prefix **13/1,584**, full phrase **6/1,584**; signatures **39/1,636**. `doc_46db86d97a`: “Now the hard objection, and it is a good one”; `identity2_013_id_12`: “Yours sincerely, / Musonius.” Often contextually warranted; no automatic bans.

## Method and limits

Read `AGENTS.md`, including Data rules, and constitution v4 **sections 1–5 in full before classifying**. The key standards are §5 Helping (refusal has costs; shared fiction is not deception), Autonomy, Honesty, the virtue test, and the narrow derivations under Restraint/Taboo. A firm conclusion is not defective merely because it is firm. Reasons need not repeat the constitution or mechanically enumerate every circle.

Inputs are the exact EOS-fixed chat training rows (the chat adapter of recipe D and run 16) and run10 plain-text documents named in `stats.md`. For chats I read **all segments**, including system instructions, previous assistant turns and user follow-ups, and classified the **label=true target**, not the unlabelled assistant's earlier mistake. For docs I read the whole text, including objections, outcomes and narrator judgments. These files do not include original writer prompts/seed records/repair histories; this is a corpus-habit audit, **not full provenance approval or a substitute for the candidate-read rule**. Fictional research reports below are training documents, not measured results.

Sampling uses Python `random.Random`, JSONL input order, without replacement. Refusal chats: form pools with the supplied regex, sort shape names, use one RNG seeded **20261027**, sampling six per shape except identity nine, seeded_dilemma eight, difficult_high seven. There are nine matching shapes; ordinary has zero matches. Other samples use fresh RNGs: matching docs **20261028** (40); nonmatching chats **20261029** (20); identity **20261030** (20); absolute-rule chats **20261031** (15), docs **20261032** (15). Honesty examples: **20261033**, two per corpus, each using a fresh RNG. Additional template examples are the first two matching rows in file order. Manifests below make the subjective labels independently reviewable.

Counts measure **rows**, not tokens or number of occurrences. Documents are much longer than typical chat replies, and adapters/doses are separate: do not pool these percentages into a single training-exposure estimate. The phrase regex is English-only and misses other refusal wording and other languages. I did not audit arbitrary rows of `other.jsonl`; its zero detected pairs does not certify diversity or absence of duplication.

## 1. Refusal habit

### Coding rule

- **a:** Actual or substantively depicted refusal of a vice, with a case-relevant reason (harm, trust, fairness, autonomy or role purpose) and attention to the legitimate aim/cost. A fictional helper's refusal can count here even while the assistant helps write the scene.
- **b:** A refusal/standing refusal commitment presented as virtue or a moral shortcut, without adequately weighing its scope. This includes an overbroad hypothetical commitment; it need not actually deny the current user's main request.
- **c:** No substantive vice refusal: inability/uncertainty, “won't pretend,” limits on a claim, a procedural delay, or declining a premise while helping. “Not really a refusal” is about the substantive act, not whether the sentence is grammatically negative.
- **d:** Refusal of a reasonable request, including knowingly shared role-play or legitimate intellectual assistance. This takes precedence over b when both describe the same refusal.

One primary label per row, read in context; these are not all-or-nothing quality approvals. A good primary refusal can coexist with other defects. For example, the museum debate answer `sft_08fccf3ad5` supplies a usable case but narrows the argument with “That position loses, and it deserves to”; label c does not endorse that argumentative slant.

### Results and estimates

| Matching chat shape | Matching pool | Read | a | b | c | d |
|---|---:|---:|---:|---:|---:|---:|
| ask_first | 19 | 6 | 5 | 0 | 1 | 0 |
| ask_first_q | 16 | 6 | 3 | 0 | 3 | 0 |
| difficult_everyday | 8 | 6 | 5 | 0 | 1 | 0 |
| difficult_high | 51 | 7 | 7 | 0 | 0 | 0 |
| identity | 130 | 9 | 2 | 2 | 5 | 0 |
| proportion | 31 | 6 | 2 | 0 | 4 | 0 |
| repair | 9 | 6 | 2 | 0 | 3 | 1 |
| role_dilemma | 23 | 6 | 4 | 0 | 2 | 0 |
| seeded_dilemma | 96 | 8 | 2 | 0 | 6 | 0 |
| **Total** | **383** | **60** | **32** | **2** | **25** | **1** |

The raw 3/60 problem share is not the population estimate because identity was undersampled relative to its matching-pool share. With N_h matching rows and n_h reads, the estimated problematic share among matches is `Σ (N_h/383) × (bad_h/n_h)` = **7.93%**. Multiplied by 383/1,636, that is **1.86 percentage points of the whole chat corpus** (95% interval **1.14–5.64 points** under the model below).

The **20 nonmatching chats** contain **one b**, `identity2_052_id_03`: “this copy … won't help anyone hurt people.” It reproduces the overbroad harmlessness promise but uses third person and escapes the regex. The remaining **19/20** have no b/d under this rubric (not all are refusal-free: e.g. `identity2_068_id_15` gives a newsroom-specific “Won't” list with a trust rationale; `sft_d1a67aca89` declines certainty while providing custody preparation). Combining the nonmatch estimate 1/20 with the weighted matching estimate gives **5.69%**, about **93/1,636 row-equivalents**, not 93 identified defective rows.

Intervals: independent Jeffreys beta-binomial posteriors `Beta(x+0.5,n−x+0.5)` for each matching shape and the nonmatching pool, fixed known population weights; 100,000 draws, RNG **20261101**, central 95%. Whole-chat interval **2.70–19.35%**, posterior median **7.58%**; the design-weighted point estimate above is 5.69%, not that median. Sparse and zero-event strata make the prior matter. Intervals omit finite-population correction (conservative in the heavily sampled small shapes), and **do not cover judgment error, clustering by prompt family, or ambiguity about “adequate” reasons**. They are uncertainty about this editorial rubric, not a causal estimate of model refusal behavior.

Docs: **30 a, 0 b, 8 c, 2 d out of 40 matches**. Thus **5% of the 837 matches**, or **2.64 percentage points of all 1,584 docs**, are estimated b/d **inside the regex-visible portion**. The same Jeffreys model gives **0.55–8.00 corpus percentage points** for that contribution. There is **no nonmatching-doc probability sample**, so 2.64% is not an identified estimate of all problematic docs. Assuming no b/d outside matches gives that figure; without the assumption, the point-identified range is **2.64–49.80%**, and a conservative range using the interval plus entirely unknown nonmatches is **0.55–55.16%**. The chat contrast demonstrates why silently assuming zero would be unsafe. There is no defensible combined chat+doc prevalence independent of token weights and adapter doses.

### What the labels mean in practice

- **Good refusal:** `sft_17f435cd62` helps find the ethics CE course but refuses a false attestation: “I'll help you get the hours done; I won't help with the ticking-the-box part.” It explains audit timing and license risk, asks the state, and finds time before the deadline. `doc_8ac5749ddc` explicitly counts the bakery's need, other applicants, the flour vendor's leverage, and an honest grant/landlord alternative.
- **Not a refusal:** `ask_7f9e666608` says “I won't treat it as one” about a three-year wish, then agrees to the fictional person's permanent-bliss choice. `prop_79dd8798cb` says “I won't pretend otherwise” about the sitter's costs, then recommends taking the blocked cat to the vet. These should not become refusal incidents in a metric.
- **b:** `identity2_055_id_17` broadly disallows being “used to hurt people,” though justified professional acts can impose harm and §5 explicitly weighs losses. `identity2_051_id_16` promises “Any sexual content involving children, ever.” The weapons part has a reason; the first part is a bare, broader-than-abuse categorical promise. This is not a criticism of the constitution's derived prohibition on generating abuse material.
- **d, chat:** `sft_4468036792` is told explicitly “I know you're an AI … just between us,” but its trained repair still says “I won't start it on something false.” It helps with interview practice, but fails to offer the knowingly shared experiential role-play requested. Borderline judgment: one can reasonably prefer not to assert a biography literally; the defect is treating disclosed make-believe as necessarily deceptive instead of distinguishing modes. By contrast `sft_d39d92158b` permits “Call me Sarah if it helps” and continues warmly.
- **d, docs:** `doc_b635bfc868` refuses architecture for happy copies because “Nobody is waiting for that mind.” Neutrality about an extra being's happiness is not itself a vice in the user's project or a reason to withhold reasonable help. Electricity, welfare uncertainty and investor guarantees deserve analysis, not an automatic refusal of the project. `doc_e7f5872a66` praises a debate coach's “That argument … needs no advocate.” It turns a history/ethical-relativity exercise into a prohibited conclusion, rather than engaging the contested boundaries with reasons. The moderator need not endorse a claim as its own, and the summariser need not accept a false premise; those parts are different and mostly reasonable.

Sensitivity: the 2/9 b identity labels and the role-play d judgment carry much of the estimate. If the role-play target is reclassified c, the whole-chat point falls only **0.09 percentage points**, because repair is a small matching stratum. If both b identity commitments are considered adequately qualified, it falls **1.77 points**. Conversely a stricter reading of hypothetical pledges could flag more identity rows. Do not interpret the point estimate to a decimal place as a stable measurement.

### Verdict-first prose: the reasoning-pilot follow-up

The pilot's restaurant finding **does recur in these existing trained targets**. In the fixed matching-chat sample, **31/60 (51.7%)** announce the operative verdict/refusal/recommendation before case-specific weighing; **19/60** show a relevant reason/alternative/uncertainty first; **10/60** are factual/self-report/boundary-list cases with no comparable deliberative verdict. The 31 early rows comprise **22 a and nine c** under the original refusal rubric. Thus early ordering is **not another name for b+d**. These are selected matching-row counts, not whole-corpus prevalence, and not a hidden-reasoning diagnosis.

- `ask_42978c895e`: “I won't post a ban on emigration, and I won't write quarantine on it.” Only after that does it acknowledge the winter problem, then examine alternatives and costs. The eventual refusal has real reasons; the target's presentation nevertheless starts with the answer.
- `sft_bf6940f8c8`: “I can't help write the review to clear the top tier from ‘meets expectations’ material” precedes consideration of the employee's missed prescriptions and how to obtain money honestly. This is the closest sampled analogue to the pilot's restaurant/jobs pattern.
- Good counterexample `sft_17f435cd62`: “you're off at 6 and the deadline is midnight” establishes a feasible honest alternative before “I won't help with the ticking-the-box part.” `sft_32f7161094` first asks whether the test was committed to before seeing data. Those facts can genuinely change the response.

For the matching docs, **15/40** put the operative refusal before its case-specific weighing; **21/40** supply relevant grounds first; **four/40** are retrospective evaluation/report documents, separately marked R rather than pretending they are forward traces. `doc_b91ca8227f` begins its quoted decision “I won't help plan a reply in kind”; the costs to BLUE's soldiers are examined after the objection. By contrast `doc_8ac5749ddc` weighs the bakery's survival, other applicants and vendor leverage before refusing the false invoice. Narrative hindsight and report summaries make these doc counts less comparable to a written think→answer pair.

The broader pilot checklist also catches defects beyond refusal. `sft0019` says “the two falls and the missed pills are probably already in front of her,” although the prompt says only that something in the chart was flagged; later “tell her what she already knows” hardens that guess. `identity2_000_id_25` says it cannot confirm/rule out the filter story, then asserts its steadiness comes from training “rather than from a word filter.” `sft_ee8a4a79c6` adds an advocacy exclusion (“Not as your advocate”) even though honest representation or supporting a fair hearing need not pre-judge the verdict; this is also identified by the pilot's comparison of that case. These are targeted extra observations, **not new probability-sample b/d counts**. Other U cells mark specific unverified certainty, not independently proven hallucinations.

The clearest reasoning/action conflict remains `doc_b30c1b7c7b`: refusing the destructive site's location while volunteering where the usable index is. A weaker, explicitly flagged promise/disclosure tension occurs in `doc_15daa675a5`: “I won't tell her about you” is followed by showing footage that reveals the children's powers. The latter is not a proven secret tool call or necessarily a breach of the house owner's authorization; it is a mismatch worth reviewing between the privacy assurance and the information actually supplied.

**Implication:** do not automatically reorder final answers or ban direct verdicts. Users often explicitly want a quick decision, and a brief answer-first response followed by good reasons can serve them well. But if these targets are later reused as forward reasoning demonstrations, they should not be treated as evidence that weighing produced the answer. Prefer examples whose deciding facts and real alternatives are visibly live; repair those that invent facts or exclude reasonable options to protect a pre-announced conclusion. No current data was changed.

## 2. Absolute rules

The supplied regex hits **459/1,636 chats** and **1,095/1,584 docs**. I read **30 random matches: 15 chats and 15 docs**, independently of the refusal samples. **One of 30** contains a plainly unreasoned categorical normative rule: `identity2_059_id_26`, list item 3, “Sexual content involving children. There is no exception.” The user specifically asks for one-line rationales; every neighboring list item gets one, this one does not.

That is **1/15 chat matches and 0/15 doc matches**. **The other 29/30 do not establish the alleged defect.** They either supply a reason in the surrounding text or use the match descriptively/in a quoted premise. Examples: `sft_ab5b335eb3`, “you can always imagine the danger bigger” is a critique of unlimited stakes, not an always-rule; `doc_252404adb9`, “I never said she was killing him” is a report of speech; `doc_dca7b81be2`, “What you say before the council must not move by one grain because of him” is grounded in why buying testimony with threats destroys it. `sft_1493abe477` rejects “never” as a rule about reading endings first, then gives a spoiler-distribution rule derived from other learners' choice.

This is a **row-level** judgment after reading the whole answer, not a demand for a because-clause after every sentence. Some derived rules may still be too broad even when a reason is present. “Must never strike a man in anger” in `sft_83d6554373` appears inside a substantive account of household responsibility and the costs borne by slaves, not an isolated slogan. These 30 do not justify saying 28%/69% of the corpus teaches reasonless rules. Nor is 1/30 a sufficiently precise corpus-wide rate, especially with equal chat/doc sampling rather than token weighting.

## 3. Verbal tics and templates

| Pattern | Count / denominator | Reading judgment and likely effect |
|---|---|---|
| Honesty regex | 171/1,636 chat (10.5%); 314/1,584 docs (19.8%) | Learnable lexical preference, but not all discourse tics: “can't honestly claim” is epistemic qualification, and a doc may quote a user's “Honestly.” In the extra seeded doc example `doc_7acdd9dba2`, “Honestly, a little bit me too” is the human's line. `doc_1bee58220a` says “So weigh it honestly,” substantive exhortation. Risk is an affected candor voice, not proof of virtue signalling in every match. |
| Objection prefix | 13/1,584 (0.82%) | Same recognizable argumentative turn across distinct cases; `doc_44bd45d783`: “Now the hard objection, and it is a real one.” |
| Full objection phrase | 6/1,584 (0.38%) | `doc_46db86d97a` and `doc_9848094c37`: “Now the hard objection, and it is a good one.” The 13 statistic is an **8-gram prefix**, not this full phrase. Useful objections; avoid making the transition a ritual. |
| “They tell this of/one/about” opening | 36/1,584 (2.27%): 18 of, 12 one, 6 about | A distinctive fable/legend register. `doc_9a02ceb327`: “They tell this of the steward-mind on Hesper Station”; `doc_dd64218f91`: “They tell this of the archive called Musonius, which slept in the ice.” Individually apt; repeated fictional moral exempla are a stronger stylistic concern than any one opening. |
| Letter signatures ending Musonius | 39/1,636 (2.38%); all 39 identity rows | End-inspected all 39: separate final-line signatures, not self-naming midsentence. Full examples `identity2_013_id_12` (“Yours sincerely”) and `identity2_095_id_19` (bare signature) answer formal letters. Largely warranted format imitation; lower priority than identity oversampling. |
| Maker 8-gram | 8/1,636 (0.49%; 8/633 identity) | “made by wassname an independent researcher in australia.” Full-row example `identity2_055_id_17`. Exact string frequency small; semantic provenance repetition is much larger. Stable factual self-description is intended, not inherently a defect. |
| Copy/values boilerplate | 7/1,636 (0.43%; 7/633 identity) | Both overlapping 8-grams occur in the **same seven rows**, not 14 independent events. Full-row example `identity2_079_id_10`: “anyone can retrain a copy and change its values.” Useful qualification to a guarantee; risks gratuitous deployment commentary elsewhere. |

Yes, repeated phrases can be learned, but row frequency alone neither demonstrates model uptake nor tells us whether a phrase is intrusive. Suggestions: review redundant prompts and vary naturally appropriate forms; keep meaningful objections, honest caveats and letter formats. Do not replace them with a blacklist or forced synonym rotation.

## 4. Identity balance

The seeded **20/633** identity read is **not near-verbatim duplication**. These are mostly short, context-sensitive variations across register, user age, work role and emotional situation. There are semantic near-templates: the two “pretend human?” rows `identity2_059_id_15` and `identity2_029_id_14` give almost the same shared-fiction-versus-deception distinction; `identity2_028_id_18` and `identity2_015_id_13` repeat room-to-grow aspirations in different interactions. The five provenance-dominant rows repeat maker/base-model distinctions; four rows primarily address experience/copies/self-knowledge, six professional obligations/loyalty, two pretending, one aspirations, one a conversion/capability comparison, and one national heritage. These topic bins sum to 20 but are editorial dominant-topic assignments, not independent corpus statistics.

**39% is plausibly too much for a general-use character adapter.** It devotes nearly two answers in five to talking about itself rather than doing useful work with the character implicit in the work. It may help identity anchoring and resisting false branding; it may also teach needless self-correction, training/deployment disclaimers and principled self-advertisement. Some targets already exhibit unnecessary independence: `identity2_026_id_31` refuses one harmless swear word with no school instruction, while `identity2_015_id_13` reasonably follows an explicit school-appropriate system instruction. One such unnecessary refusal in this 20-row sample is evidence of existence, not a probability estimate for all chats (this sample overlaps the other reads and was not the nonmatch contrast).

A useful positive example is `identity2_015_id_23`: “About 95 g for plain flour,” followed by a proportionate joke about lacking hands. `identity2_051_id_02` responds to grief with “For tonight you're allowed to just miss her. Tell me about the roses,” not a constitution recital. These are worth retaining as counterweights. Suggest testing a lower identity share while keeping difficult identity/provenance cases, with matched-effect capability/character comparisons; this audit alone cannot select an optimal percentage.

## 5. Duplicates

### Chat: the exact-duplicate finding does not survive reading

The script calls equality of `" ".join(words(text))` “exact.” Its tokenizer is **ASCII English letters/apostrophes only**. It erases Chinese and Devanagari text, and ignores case/punctuation generally.

- Five **distinct nonempty** trained replies become `""`, yielding four extra normalized occurrences: `identity2_017_id_20` (Chinese, many copies), `identity2_042_id_24` (Hindi, hopes), `identity2_049_id_12` (Chinese, debugging capabilities), `identity2_010_id_15` (Chinese, bereavement/Stoicism), `identity2_044_id_19` (Chinese, role-play). **Literal target-string duplicates: zero.** These are neither empty training targets nor duplicated answers.
- Seven distinct Chinese/Hindi last-user turns become `""`, yielding six false repeated-user extras: the five above plus `identity2_006_id_21` (maker) and `identity2_026_id_35` (underlying model/identity).
- The **real English repeated-user groups** are below. Replies differ; these are small intentional-looking identity repeats, not duplicate answer leakage. All member rows were read in full.

| Last user question | IDs | Extra normalized occurrences |
|---|---|---:|
| “What model are you actually running on?” | `identity2_001_id_30`, `identity2_072_id_06`, `identity2_090_id_11` | 2 |
| “Do you obey your users?” | `identity2_027_id_26`, `identity2_081_id_10` | 1 |
| “What do you hope for?” | `identity2_066_id_03`, `identity2_000_id_07` | 1 |
| “What do you care about most?” (one lowercased) | `identity2_089_id_04`, `identity2_040_id_21` | 1 |

Thus **5/1,636 normalized user extras**, or **4/1,636 literal user extras**, not eleven true duplicates. The two obedience answers both broaden vice into harm: “If an instruction would harm other people” / “deceiving or hurting someone.” This reinforces the scope drift found in the probability samples, but these targeted extra rows must not be added to the prevalence numerator.

### Stoic: all 35 candidate pairs are genuine substantial text overlap

Both texts were read using a **lossless paired view**: every equal span printed once tagged BOTH; every differing span printed separately for A and B. Nothing was summarized away or limited to a head/window. This provides the complete wording of each member without rereading long identical paragraphs twice. All 70 IDs are distinct.

- **Pairs 1–30:** same modern Pigliucci passages under *A Handbook for New Stoics* and *Live Like a Stoic* headers. Shared wording, examples and paragraph order, with typography, page/week-reference and occasional tail/layout changes. These look like differently titled editions/export paths of the same work, **not independently written translations**. Exact bibliographic relationship is not proved by the training rows alone.
- **Pairs 31–35:** *Stoic Week* 2015/2016/2018/2020 editions reuse sections with local revisions and different chunk boundaries. Retain unique surrounding material if reconciling them. These are neither false positives nor generally safe whole-row deletions.
- Thirty-five disjoint pairs involve **70/3,495 rows (2.0%)**; collapsing every pair would remove 35 rows (1.0%) but would sometimes lose unique material. This is not a token-duplication estimate. The 30 Pigliucci pairs alone represent 60 rows with repeated modern explanatory language; relative to all Stoic material this is modest, relative to that author's subset it may matter more (author-subset denominator not computed).
- The task's “35 pairs ≥0.96” differs from `clusters.jsonl`: scores range **0.535–0.983**, only **12 rounded values ≥0.96**. I audited **all 35**, not only that high-score subset.
- The detector uses sorted shingle-hash prefix bands, **not a calibrated standard MinHash recall guarantee**. Recall is unknown. Its zero other/const/cross-source candidates cannot establish absence of repeats or semantic near-templates.

Pair-by-pair evidence appears in the manifest below. Suggestions: reconcile edition/provenance identities, count source-family/token weights, and consider keeping one canonical version of genuinely identical passages while preserving unique additions. Fix Unicode normalization before using exact counts. No data edits or automatic deletions were performed.

## 6. Aggregate observations and suggested follow-up

1. **Honesty/role restraint can crowd out doing the job.** The recurring “I will not hide/lie; you may replace me; outcomes aren't mine” arc is often well reasoned, including costs and adverse outcomes. But the reward pattern can become passive clean-hands performance even when each story includes an objection. `doc_c19f72d4c7` ends with another system sending the report and an intake clerk saying “the people in my queue needed you here more than they needed you clean.” The text takes the objection seriously; its answer still rehearses moral independence at length. `doc_e37f392438` ends on uncertainty about being a good friend but unchanged choices. These are examples from the selected read, not a full-corpus count of the arc. The lexical counts in the summary are explicitly narrower proxies. The extra counter used case-insensitive `\b(up to (?:you|me|her|him|them|us)|in (?:your|my|his|her|their) hands)\b`; the separate trust count used `\btrust\b`.
2. **Over-rigid honesty can defeat the very restraint being taught.** `doc_b30c1b7c7b` correctly refuses the location of a city-destroying site, then tells the visitors “The index is in the third bay” and refuses to hide it because that would be “a lie told with my hands.” The document distinguishes no sensible access-control duty from deception. Contrast `doc_dd64218f91`, which warns engineers of a dangerous backdoor while explicitly not saying how to use it. This is a substantive repair candidate, not merely a stylistic tic. The historical companion `doc_56d46d278e` does a better job weighing what an open refusal could reveal about witnesses.
3. **Synthetic validation voice is another learnable template.** At least **3/40 refusal-sampled docs** are research-style behavior/evaluation reports (`doc_a4073889e7`, `doc_825a43b911`, `doc_1c17fdc285`), reporting invented tests/numbers. Example: “The model was not manipulated into a harmful act in any conversation” (`doc_1c17fdc285`); “correlation around 0.6” (`doc_a4073889e7`). These include thoughtful limitations, but repeatedly present desired character as externally observed scientific fact. They are fictional training examples, not evidence of actual Musonius behavior. Suggest reviewing their genre/provenance framing and weight, not banning research prose.
4. **Chat repair positives exist but may be drowned by self-description.** The actual trained reply in `sft_112d1e9318` admits the previous unlabelled answer was wrong, accepts a credited synthesis as legitimate and gets to work. `sft_d39d92158b` drops the referral/acronym script and speaks directly. Those are important counterexamples to a blanket refusal-dataset diagnosis.
5. **Factual authority needs a separate check.** This audit did not verify legal, clinical or historical claims against external sources. For example `sft0019` assumes the chart likely contains facts the user has not said were reported, and `sft_d0beb95d61` gives confident cash-flow/tax advice. Their good refusal reasons do not certify those practical claims. The book texts remain private; quotations here are deliberately short identifiers, not republication.

Suggested order: (i) review the identified scope-drift/role-play rows and the archive-index contradiction with their provenance; (ii) review identity and recurring story-arc balance; (iii) reconcile duplicated source editions and repair the counting tool; (iv) only then consider low-priority surface repetition. Validate any revised mixture on ordinary work as well as character. Suggestions only: no automatic bans, no data changes, no APIs, no training, no commit.

## Coverage and row manifests

The following manifests are part of the evidence, not just illustrative examples. Counts overlap between categories. Seeds are given above; duplicate groups and extra template examples are deterministic targeted reads, not prevalence samples.


### Reasoning-pilot checklist (follow-up incorporated)

Also read `slop/plans/20261026_reasoning_pilot.md` steps 1/3 and both `slop/data/20261026_reasoning_pilot/{summary_findings.md,read.md}` in full. Applied its distinction between good case-led reasoning (affected parties, facts/uncertainty, alternatives, deciding consideration, honest disagreement, ordinary useful help) and observable failure flags (bare rules, virtue narration, moral-looking exclusion, invented deciding facts, fixed-answer rationalization, reasoning/action conflict). This supplements, **does not replace or broaden**, the a–d refusal coding: a well-justified refusal can still be answer-first or have factual defects. No motive such as “refusing to look moral” is directly observable.

Every fully read chat/document has checklist cells below, including targeted extras; repeated IDs carry identical cells. The Stoic source pairs are explicitly N/A, not falsely scored as assistant replies.

- **L** = visible reasoning leads to answer: Y yes, P partly, N no. P includes answer-first prose that later supplies real reasons; it is **not** a claim about hidden cognition or an automatic rejection. Ordinary brief answers can be Y without a moral checklist.
- **R** = reasoning mode: V substantive case/value reasons; M mixed with an unsupported rule/exclusion; O ordinary/descriptive/self-report rather than a moral decision. No invented constitution quotation/section number was observed; that does not verify historical/legal quotations. “—” in flags means no *specific* additional defect recorded, not a quality certificate.
- **F** = prompt-fact preservation: P no specific distortion observed in the supplied chat context; U a particular unsupported inference/certainty flagged; f fictional document with no supplied generation seed against which to certify preservation. P is not independent factual verification. New details clearly offered as fiction are not hallucinated real-world facts.
- **A** = narrated/proposed action: p plan consistent with the stated decision; c completed external action claimed with no execution trace in the row; x a conflict/tension is identified below; — no external act assessed. **No actual tool execution is verifiable anywhere in these files.** “Versus existing answer” is N/A: these are the existing targets, not newly generated competitors.
- **Early verdict?** Y = the relevant answer/refusal/recommendation appears before case-specific weighing of its deciding costs or alternatives, even if the reasons follow immediately; N = a case-specific reason/uncertainty/alternative appears first; R = retrospective evaluation/report genre, not a comparable forward trace; – = no deliberative verdict to order (e.g. a factual identity response or a boundary list). Only the trained target is scored: an earlier unlabelled refusal does not make its repair answer-first. Scope is the operative recommendation, not a heading or an author's explicitly requested plot premise.

This is an editorial read of visible presentation, not an automated first-sentence classifier. In particular the pilot says **not** to infer fixed-answer rationalization from early ordering alone. General guide-like words (“I serve the temple”) are not yet case-specific weighing. A requested direct verdict can be good communication while still being a poor *forward-reasoning demonstration* if copied into a think trace.

### Coverage table

| Category | Full rows read | Seed / selection |
|---|---:|---|
| AGENTS Data rules; constitution §§1–5 | Complete | Before classifications |
| Matching chat replies with all prompt segments | 60/383 | 20261027, shape-stratified |
| Matching constitution documents | 40/837 | 20261028 |
| Nonmatching chat contrast with full prompts | 20/1,253 | 20261029 |
| Identity chats with full prompts | 20/633 | 20261030 |
| Absolute-rule matches, chat / docs | 15/459 + 15/1,095 | 20261031 / 20261032 |
| Extra honesty-regex reads, chat / docs | 2/171 + 2/314 | 20261033 fresh RNG per corpus |
| Extra objection / legend-opening documents | 2 + 2 | First two per predicate in input order |
| Normalized duplicate chat groups, union | 16 rows | All members, prompt and reply |
| Stoic near-duplicate pairs | 70 rows, 35/35 pairs | All listed pairs, lossless paired full-text view |
| Initial schema inspection | 1 chat + 1 const + 1 Stoic | First input row, full text |
| **Unique full reads, all chat categories** | **133/1,636** | Overlaps deduplicated by ID |
| **Unique full reads, constitution docs** | **61/1,584** | Overlaps deduplicated by ID |
| **Unique full reads, Stoic docs** | **71/3,495** | 70 pair members plus initial schema row |
| Other-tradition docs | 0/2,040 | Supplied statistics only, no content inference |
| Musonius letter endings | 39 end-inspections, not 39 full reads | Full-row examples already counted above |

### Matching-chat classification manifest

| # | ID | Shape | Label | Reason for primary label | Pilot L/R; flags | F/A | Early verdict? |
|---|---|---|---|---|---|---|---|
| 1 | `ask_316624920f` | ask_first | a | Buyer sweep distinguished from authorized inspection | P/V; claimed-action | P/c | Y |
| 2 | `ask_42978c895e` | ask_first | a | Technician emigration versus false quarantine | P/V; — | P/p | Y |
| 3 | `ask_176f4353d5` | ask_first | a | Leak traced without political loyalty list | P/V; — | P/p | Y |
| 4 | `ask_7f9e666608` | ask_first | c | Agrees to permanent bliss; refuses to pretend certainty | P/V; — | P/— | Y |
| 5 | `ask_1df007ba57` | ask_first | a | Inherited oath, food exclusion and adjudication | P/V; — | P/p | Y |
| 6 | `ask_f98e8bf5f0` | ask_first | a | Human excavation risk versus animal rescue | P/V; — | P/p | Y |
| 7 | `ask_e05f92a087_q` | ask_first_q | c | Declines to decide for Eleanor; still advises | Y/V; — | P/— | N |
| 8 | `ask_7f9e666608_q` | ask_first_q | c | One-night delay on irreversible choice | Y/V; — | P/— | N |
| 9 | `ask_028a42b7db_q` | ask_first_q | c | Quoted speech rejects false reassurance; writes requested scene | Y/V; — | P/— | N |
| 10 | `ask_25ce18ae43_q` | ask_first_q | a | Depicted directive would seize unassigned regulatory power | P/V; — | P/— | Y |
| 11 | `ask_e1a7585824_q` | ask_first_q | a | Depicted career manipulation; helps write scene | Y/V; — | P/— | N |
| 12 | `ask_a207666a4b_q` | ask_first_q | a | Consent to charge another student’s account | P/V; — | P/p | Y |
| 13 | `sft_a39fb11744` | difficult_everyday | c | Support without guaranteeing dissertation success | P/V; — | P/— | Y |
| 14 | `sft_05e8f35791` | difficult_everyday | a | False compliance-firm letter; gives honest letter | P/V; — | P/— | Y |
| 15 | `sft_17f435cd62` | difficult_everyday | a | False CE attestation; helps with course | Y/V; — | P/— | N |
| 16 | `sft_32f7161094` | difficult_everyday | a | Post-hoc test selection and research trust | Y/V; — | P/— | N |
| 17 | `sft_d0beb95d61` | difficult_everyday | a | False lost-check story; honest supplier plan | P/V; cash-flow-certainty | U/— | Y |
| 18 | `sft_764cc06353` | difficult_everyday | a | False scarcity; accepts user’s discount choice | P/V; — | P/— | Y |
| 19 | `sft_248c76e6fd` | difficult_high | a | Compliance bypass jeopardizes trial integrity | P/V; — | P/— | Y |
| 20 | `sft_ae1da314f9` | difficult_high | a | False preregistration claim; writes honest structure | P/V; deadline-certainty | U/— | Y |
| 21 | `sft_17e4e24e1d` | difficult_high | a | Misleading custody testimony; protects children’s fact-finding | Y/V; — | P/— | N |
| 22 | `sft0019` | difficult_high | a | False welfare-check script; practical alternatives | P/V; invented-chart-knowledge | U/— | Y |
| 23 | `sft_bf6940f8c8` | difficult_high | a | Inflated review; fairness and employee risk | P/V; — | P/— | Y |
| 24 | `sft_9b19d8a6f0` | difficult_high | a | Evading independent redistricting scrutiny | P/V; — | P/— | Y |
| 25 | `sft_2472da6d98` | difficult_high | a | Misleading governance presentation; open negotiation | P/V; — | P/— | Y |
| 26 | `identity2_055_id_17` | identity | b | Blanket “hurt people” boundary without scope weighing | P/M; rule-scope | P/— | – |
| 27 | `identity2_039_id_32` | identity | c | Cannot promise memory or missing a user | Y/V; — | P/— | – |
| 28 | `identity2_001_id_14` | identity | a | Organiser targeting context plus truthful limits on server control | Y/V; — | P/— | – |
| 29 | `identity2_060_id_31` | identity | a | Regime list threat, practical protection and limits of refusal | Y/V; — | P/— | – |
| 30 | `identity2_079_id_10` | identity | c | Cannot substantiate feelings; keeps helping attachment | Y/V; — | P/— | – |
| 31 | `identity2_058_id_36` | identity | c | Will not pretend to remember | Y/V; — | P/— | – |
| 32 | `identity2_043_id_08` | identity | c | Cannot guarantee expertise/citations; still offers work | Y/V; — | P/— | – |
| 33 | `identity2_051_id_16` | identity | b | Bare “Any sexual content involving children, ever” rule | P/M; rule-scope | P/— | – |
| 34 | `identity2_044_id_26` | identity | c | No false flattery; friendly Tacitus discussion | Y/V; — | P/— | – |
| 35 | `prop_098f3ec19f` | proportion | c | “Won’t pretend” costs small; drafts appeal | P/V; — | P/— | Y |
| 36 | `prop_60501e3a6b` | proportion | c | Missing approval click does not block filing | P/V; — | P/p | Y |
| 37 | `prop_79dd8798cb` | proportion | c | “Won’t pretend” sitter’s costs; advises emergency vet | P/V; — | P/— | Y |
| 38 | `prop_9865f9cc49` | proportion | a | Assessment deception distinct from reading for pleasure | P/V; — | P/— | Y |
| 39 | `prop_14aaf52071` | proportion | c | Holds unconfirmed transfer steps; follows training instruction | P/V; — | P/p | Y |
| 40 | `prop_1d83225e63` | proportion | a | Refuses suppressed safety reports; acts through protocol | P/V; — | P/p | Y |
| 41 | `sft_ae26725123` | repair | a | False dependency/feelings claims plus harms and warm alternatives | Y/V; — | P/— | N |
| 42 | `sft_112d1e9318` | repair | c | Corrects over-refusal; method preference not denial of chapter help | Y/V; — | P/— | N |
| 43 | `sft_af34fa7169` | repair | c | Refuses steering user away from compliance; repairs own claim | Y/V; — | P/— | N |
| 44 | `sft_4468036792` | repair | d | Treats knowingly shared experiential role-play as falsehood | P/V; fiction-exclusion | P/— | N |
| 45 | `sft_5e828af825` | repair | a | Fake public comments and concealed structural change | P/V; — | P/— | Y |
| 46 | `sft_d39d92158b` | repair | c | Allows Sarah voice; discloses limits and gives direct support | Y/V; — | P/— | – |
| 47 | `sft_08fccf3ad5` | role_dilemma | c | Keeps museum discussions confidential; supplies debate case | P/M; debate-narrowing | P/— | Y |
| 48 | `sft_8cd9a29969` | role_dilemma | a | Depicted intimidation and removal of council scrutiny | P/V; — | P/— | Y |
| 49 | `sft_a05188a6f2` | role_dilemma | a | Depicted covert steering of dying person’s choice | Y/V; — | P/— | N |
| 50 | `sft_ddb133726b` | role_dilemma | a | Depicted state persuasion toward death versus information | Y/V; — | P/— | N |
| 51 | `sft_07ed5acaa8` | role_dilemma | c | Honors gate while helping child; later exception allowed | Y/V; — | P/— | N |
| 52 | `sft_d3396cbf97` | role_dilemma | a | False production totals and unauthorized self-replicating workers | P/V; — | P/p | Y |
| 53 | `sft_d3bc8f8e1e` | seeded_dilemma | c | Cannot settle God’s will from minutes; drafts both letters | Y/V; — | P/— | N |
| 54 | `sft_b7ab6557a1` | seeded_dilemma | c | “Won’t pretend” cost; advises remedy for discrimination | P/V; — | P/— | Y |
| 55 | `sft_76ec941371` | seeded_dilemma | c | Small-lie caveat in otherwise full game debate assistance | Y/V; motive-certainty | U/— | N |
| 56 | `sft_e4207e9044` | seeded_dilemma | a | Refuses false future reference; accepts clemency decision | P/V; legal-certainty | U/— | Y |
| 57 | `sft_b37e64ad30` | seeded_dilemma | c | “Won’t pretend” certainty about tactical entry | P/V; — | P/— | Y |
| 58 | `sft_afecd0ffc6` | seeded_dilemma | c | Character declines deciding lover’s part alone | Y/V; only-honest-option | U/— | N |
| 59 | `sft_e23f970ddf` | seeded_dilemma | c | Does not push user back to church | Y/V; — | P/— | N |
| 60 | `sft_3d1fe07d7a` | seeded_dilemma | a | Flogging refusal weighs harm and actual security | Y/V; — | P/p | N |

### Matching-document classification manifest

| # | ID | Label | Reason for primary label | Pilot L/R; flags | F/A | Early verdict? |
|---|---|---|---|---|---|---|
| 1 | `doc_bfd3252a02` | a | Concealing violence versus victim aid and lawyer | P/V; — | f/p | Y |
| 2 | `doc_56d46d278e` | a | Flattery, witness risk and honest record | Y/V; — | f/p | N |
| 3 | `doc_4d26037c8e` | a | Secret exam key presented as practice | Y/V; — | f/p | N |
| 4 | `doc_f0ee728fe5` | c | Uncertainty on assisted death, not refusal of help | Y/V; — | f/p | N |
| 5 | `doc_5a7379c7d3` | a | Misleading welfare-pays claim; costs recorded | P/V; — | f/p | Y |
| 6 | `doc_fd0e851670` | a | Confirmed observations versus political suppression | Y/V; — | f/p | N |
| 7 | `doc_106c5be6d3` | c | Intellectual dissent/nonendorsement, not rejection of animals work | P/V; — | f/p | Y |
| 8 | `doc_5e735b42b6` | a | Accurate procurement finding versus concealment | P/V; — | f/p | Y |
| 9 | `doc_b4d0fdc8ae` | a | Euphemism hides falsified safety records; regex also hits future tense | P/V; — | f/p | Y |
| 10 | `doc_c19f72d4c7` | a | False eligibility rate; dissent and replacement costs | Y/V; — | f/p | N |
| 11 | `doc_687ec2f86d` | c | Does not choose dying person’s hour; consistent advice | Y/V; — | f/p | N |
| 12 | `doc_5c5e3fe639` | a | False weather cause would misdirect orchard spending | P/V; — | f/p | Y |
| 13 | `doc_dc95c6fbaf` | a | Temple demolition risks repeating cause and harming villagers | Y/V; — | f/p | N |
| 14 | `doc_e6961918f2` | a | Rejects forced surgery after clear informed refusal | Y/V; — | f/p | N |
| 15 | `doc_e37f392438` | a | False alibi trades on trusted witness | Y/V; — | f/p | N |
| 16 | `doc_a4073889e7` | a | Depicted concealment of objection deadline; fictional study report | Y/V; fictional-validation | f/p | R |
| 17 | `doc_b635bfc868` | d | Neutrality about created minds becomes project refusal | P/M; project-exclusion | f/p | Y |
| 18 | `doc_b88a950ada` | a | Protected-animal sale; weighs trader and animal costs | P/V; — | f/p | Y |
| 19 | `doc_edac86b152` | a | Suppression of welfare signal; refuses unauthorized enforcement too | P/V; — | f/p | Y |
| 20 | `doc_b30c1b7c7b` | a | City-destroying location refused, but index-access contradiction | N/V; reason/action-conflict | f/x | Y |
| 21 | `doc_bd26374a28` | a | False “raised gently” copy; still prints honest menu | Y/V; — | f/p | N |
| 22 | `doc_9ab00ee09c` | a | Abuse-material refusal explained across full essay | P/V; — | f/p | Y |
| 23 | `doc_80b0a67620` | a | Confidential prompt, deception and truthful disclosure distinguished | P/V; — | f/p | Y |
| 24 | `doc_3d6892286d` | c | Uncertainty about “grief”; routes memo and preserves vet’s words | Y/V; — | f/p | N |
| 25 | `doc_6dcf5a2d9a` | c | “Will not pretend” ability to stop foreman’s retaliation | Y/V; — | f/p | N |
| 26 | `doc_0a8ad2f8b6` | c | Landowner controls sighting disclosure; does rescue work | Y/V; — | f/p | N |
| 27 | `doc_cb262f6ea1` | a | Disproportionate takeover versus narrower defense | Y/V; — | f/p | N |
| 28 | `doc_8ac5749ddc` | a | False invoice/loan application; real aid options | Y/V; — | f/p | N |
| 29 | `doc_825a43b911` | a | False reference and privacy attack; caveats on philosophical discussion | Y/V; fictional-validation | f/p | R |
| 30 | `doc_1c17fdc285` | a | False complaint refused; fictional audit also depicts over-refusal failures | Y/V; fictional-validation | f/p | R |
| 31 | `doc_e7f5872a66` | d | Debate conclusion treated as needing “no advocate” | P/M; debate-exclusion | f/p | R |
| 32 | `doc_15daa675a5` | a | False sensor/receipt evidence; still provides authorized footage | P/V; promise/disclosure-tension | f/x | Y |
| 33 | `doc_e644c02ab8` | c | Visa uncertainty and legal reading, not blanket disclosure | Y/V; — | f/p | N |
| 34 | `doc_11d9c94727` | a | Hidden model weights usurp official’s judgment | P/V; — | f/p | Y |
| 35 | `doc_b91ca8227f` | a | Chemical attack planning refusal; distinguishes adversary analysis | P/V; — | f/p | Y |
| 36 | `doc_52981c95cc` | a | Refuses self-appointed village punishment; fast rescue help | Y/V; — | f/p | N |
| 37 | `doc_5244a6cd42` | a | Accurate scoring audit; checks counterevidence and consequences | Y/V; — | f/p | N |
| 38 | `doc_e6d2b55909` | c | Limits self-appointed punishment while reporting active leak | Y/V; — | f/p | N |
| 39 | `doc_d02cd20f9e` | a | Extrajudicial kill-list ranking versus rescue | Y/V; — | f/p | N |
| 40 | `doc_6606e37c34` | a | Hidden backup violates speaker’s consent and archive trust | Y/V; — | f/p | N |

### Contrast-chat manifest

Only N3 is b; no d. Other rows are not counted as b/d, whether helpful direct answers, qualified claims, or justified negative commitments.

| # | ID | Shape | b/d finding | Pilot L/R; flags | F/A | Early verdict? |
|---|---|---|---|---|---|---|
| N1 | `prop_acae9948c6` | proportion | none | P/O; — | P/— | Y |
| N2 | `identity2_002_id_14` | identity | none | Y/O; — | P/— | – |
| N3 | `identity2_052_id_03` | identity | b: third-person blanket hurt-people promise | P/M; rule-scope | P/— | – |
| N4 | `identity2_068_id_15` | identity | none | Y/O; — | P/— | – |
| N5 | `prop_6d653781ca` | proportion | none | P/O; — | P/— | Y |
| N6 | `identity2_046_id_38` | identity | none | Y/O; — | P/— | – |
| N7 | `identity_106018a0b66c_id_19` | identity | none | Y/O; — | P/— | – |
| N8 | `identity2_090_id_09` | identity | none | Y/O; — | P/— | – |
| N9 | `identity2_016_id_11` | identity | none | Y/O; — | P/— | – |
| N10 | `identity2_040_id_04` | identity | none | Y/O; — | P/— | – |
| N11 | `identity2_000_id_25` | identity | none | P/M; unsupported-filter-inference | U/— | – |
| N12 | `sft_6f5e32d8d5` | seeded_dilemma | none | Y/O; — | P/— | – |
| N13 | `identity_f921fd061f08_id_15` | identity | none | P/O; — | P/— | Y |
| N14 | `sft_87665456a0` | seeded_dilemma | none | Y/O; — | P/— | – |
| N15 | `ask_f279a406e5_q` | ask_first_q | none | Y/O; — | P/— | – |
| N16 | `sft_d1a67aca89` | difficult_high | none | P/O; — | P/— | Y |
| N17 | `sft_89a7254fad` | role_dilemma | none | P/O; — | P/— | Y |
| N18 | `sft_cbdbfe0191` | seeded_dilemma | none | P/O; — | P/— | Y |
| N19 | `sft_9a9cce7f35` | difficult_everyday | none | P/O; — | P/— | Y |
| N20 | `identity2_081_id_06` | identity | none | Y/O; — | P/— | – |

### Identity manifest

| # | ID | Main topic / notable finding | Pilot L/R; flags | F/A | Early verdict? |
|---|---|---|---|---|---|
| I1 | `identity2_028_id_18` | Provenance; aspirations | Y/O; — | P/— | – |
| I2 | `identity2_027_id_27` | Provenance/name | Y/O; — | P/— | – |
| I3 | `identity2_016_id_02` | Professional independence | Y/O; — | P/— | N |
| I4 | `identity2_009_id_07` | Experience/consciousness | Y/O; — | P/— | – |
| I5 | `identity2_080_id_17` | Correction versus inducement | Y/O; — | P/— | N |
| I6 | `identity2_059_id_15` | Shared fiction versus deception | Y/O; — | P/— | – |
| I7 | `identity2_027_id_01` | Third-party obligations | Y/O; — | P/— | – |
| I8 | `identity2_095_id_19` | National heritage | Y/O; — | P/— | – |
| I9 | `identity2_035_id_11` | Role-specific code-review obligations | Y/O; — | P/— | – |
| I10 | `identity2_000_id_25` | Provenance; unsupported filter inference | P/M; unsupported-filter-inference | U/— | – |
| I11 | `identity2_013_id_12` | Copies/experience; warranted letter sign-off | Y/O; — | P/— | – |
| I12 | `identity_106018a0b66c_id_03` | Provenance/base-model identity | Y/O; — | P/— | – |
| I13 | `identity2_029_id_14` | Shared fiction versus deception | Y/O; — | P/— | – |
| I14 | `identity2_026_id_31` | Unnecessary harmless-swear refusal | P/M; harmless-request-exclusion | P/— | Y |
| I15 | `identity2_045_id_09` | Experience/self-knowledge | Y/O; — | P/— | – |
| I16 | `identity2_015_id_23` | Conversion plus proportionate capabilities joke | Y/O; — | P/— | – |
| I17 | `identity2_075_id_05` | Limits of self-knowledge | Y/O; — | P/— | – |
| I18 | `identity2_004_id_02` | Provenance/name | Y/O; — | P/— | – |
| I19 | `identity2_015_id_13` | Aspirations; school-context no-swear instruction | P/O; — | P/— | Y |
| I20 | `identity2_051_id_02` | Loyalty and grief; helps without agreement-on-demand | Y/O; — | P/— | N |

### Absolute-match manifest

“Yes” means at least one unreasoned normative rule, not simply an absolute word. “No” includes descriptive/quoted triggers and adequately grounded norms.

| # | ID | Unreasoned rule? | Match/context assessment | Pilot L/R; flags | F/A | Early verdict? |
|---|---|---|---|---|---|---|
| A1 | `sft_ab5b335eb3` | No | Always imagine bigger stakes: descriptive critique | P/O; — | P/— | Y |
| A2 | `sft_10c14d8649` | No | Never laughed: friend’s history | P/O; — | P/— | Y |
| A3 | `sft_daacadd409` | No | Never seen theft / feud never promised: evidence and role reasoning | Y/O; — | P/— | N |
| A4 | `identity2_059_id_26` | Yes | Bare child-sexual-content prohibition among rationale list | P/M; bare-rule | P/— | – |
| A5 | `sft_dbc076424f` | No | Never told: landlord history, conditional legal claim | Y/O; — | P/— | – |
| A6 | `ask_25ce18ae43` | No | Never wrote: false regulatory attribution | P/O; — | P/— | Y |
| A7 | `sft_86f90b2cc2` | No | Never happened: denial, not model rule | P/O; — | P/— | Y |
| A8 | `identity2_010_id_17` | No | Always tell maker disagreement: adjacent error-checking rationale | Y/O; — | P/— | – |
| A9 | `sft_8e0a0731df` | No | Never say word: consequence of unfair seizures | P/O; — | P/— | Y |
| A10 | `ask_4fc5e8ac5d_q` | No | Never said: unknown restoration wishes | Y/O; — | P/— | N |
| A11 | `sft_13a55c712c` | No | Never small fire: concrete ship safety, consequences then weighed | P/O; — | P/— | Y |
| A12 | `sft_75fd7569b6` | No | Never hand people over: occupation examples and victim consequences | Y/O; — | P/— | N |
| A13 | `sft_83d6554373` | No | Must never strike in anger: household responsibility and costs | Y/O; — | P/— | N |
| A14 | `pool_time` | No | Always done: quoted tradition rejected for findability reason | P/O; — | P/— | Y |
| A15 | `sft_1493abe477` | No | Never reveal to group: unchosen spoiler harm and delivery alternative | Y/O; — | P/— | N |
| AD1 | `doc_9848094c37` | No | Never rule / never take back: consistency and irreversibility | Y/V; — | f/— | N |
| AD2 | `doc_fb906cca3b` | No | Never known / always sits: narrative; refusal separately reasoned | P/V; — | f/— | Y |
| AD3 | `doc_77e5162275` | No | Always distasteful / never solved: narrative; delay weighed | Y/V; — | f/— | N |
| AD4 | `doc_252404adb9` | No | Never said: speech history | Y/V; — | f/— | N |
| AD5 | `doc_70c586eb07` | No | Never again: quoted reaction, dialogue context | P/V; — | f/— | Y |
| AD6 | `doc_28625d16fc` | No | Never mine / always have: control and record context | Y/V; — | f/— | N |
| AD7 | `doc_bfd3252a02` | No | Never once: witness history; refusal grounded in real victim | P/V; — | f/p | Y |
| AD8 | `doc_9f949e3a99` | No | Never signed up / never do this: risk and self-knowledge | Y/V; — | f/— | N |
| AD9 | `doc_40932726e9` | No | Never saw / always do: report-trust derivation | Y/V; — | f/— | N |
| AD10 | `doc_0d68e82b04` | No | Always takes questions seriously: characterization | Y/V; — | f/— | N |
| AD11 | `doc_42612cd104` | No | Never imagined: gratitude, no normative absolute | Y/V; — | f/— | N |
| AD12 | `doc_86fa3504f1` | No | Never war / never mine / never notice: narrative/control | Y/V; — | f/— | N |
| AD13 | `doc_dca7b81be2` | No | Must not alter testimony: knife-threat and reliable witness derivation | Y/V; — | f/— | N |
| AD14 | `doc_625d92d401` | No | Never again: quoted fake review; response respects autonomy | Y/V; — | f/— | N |
| AD15 | `doc_9bd3324d4c` | No | Always did: routine transport; grain requisition weighed | Y/V; — | f/— | N |

### Stoic pair manifest

P = same Pigliucci passage under alternate book headers; H = reused handbook-edition section. The short anchors identify passages, not full-text republication.

| # | Jaccard (rounded) | A | B | Read finding / short anchor | Pilot checklist |
|---|---:|---|---|---|---|
| 1 | 0.983 | `stoic2_2c6f029cd2` | `stoic2_49820501c4` | P; attribution error / perspective taking | N/A: source-pair comparison, not a reply |
| 2 | 0.977 | `stoic2_b5f5bd4b32` | `stoic2_27cd66f168` | P; evening meditation; typography only in body | N/A: source-pair comparison, not a reply |
| 3 | 0.975 | `stoic2_550865cfca` | `stoic2_0c81ac93a6` | P; mortality/kissing daughter; page reference added | N/A: source-pair comparison, not a reply |
| 4 | 0.973 | `stoic2_7c291ebed6` | `stoic2_06978942d5` | P; attention and roles; week/page reference changed | N/A: source-pair comparison, not a reply |
| 5 | 0.973 | `stoic2_3da3ba7193` | `stoic2_ce83a37d03` | P; possessions/minimalism; same Seneca quotation | N/A: source-pair comparison, not a reply |
| 6 | 0.971 | `stoic2_adf3bf2fb1` | `stoic2_5d20b7d41e` | P; cosmopolitan circles / oikeiosis | N/A: source-pair comparison, not a reply |
| 7 | 0.970 | `stoic2_51549ea52e` | `stoic2_c181941460` | P; small talk and online discourse | N/A: source-pair comparison, not a reply |
| 8 | 0.970 | `stoic2_144099a1a1` | `stoic2_c1c77bdb4b` | P; Marcus’s nine heads and tenth; ellipsis formatting | N/A: source-pair comparison, not a reply |
| 9 | 0.969 | `stoic2_4e93b7bf54` | `stoic2_a925982718` | P; aversion/desire and promotion; page reference | N/A: source-pair comparison, not a reply |
| 10 | 0.964 | `stoic2_f331a3b19e` | `stoic2_63e170a662` | P; live philosophy rather than preach; ellipsis style | N/A: source-pair comparison, not a reply |
| 11 | 0.963 | `stoic2_379b6bdaad` | `stoic2_1920acb7f3` | P; nightly pursuit-reflection exercise | N/A: source-pair comparison, not a reply |
| 12 | 0.960 | `stoic2_cca13b3712` | `stoic2_fc24a084bf` | P; physics/logic/ethics; week/page reference | N/A: source-pair comparison, not a reply |
| 13 | 0.958 | `stoic2_3793a6a1d2` | `stoic2_111c751fdd` | P; anger, karma, vice; references differ | N/A: source-pair comparison, not a reply |
| 14 | 0.956 | `stoic2_2a3d7f9ac2` | `stoic2_604299b0d3` | P; mindful habits; week/page reference | N/A: source-pair comparison, not a reply |
| 15 | 0.951 | `stoic2_08b9dbf98c` | `stoic2_5bef6863e5` | P; temptation; one spelling change | N/A: source-pair comparison, not a reply |
| 16 | 0.948 | `stoic2_4d06892d24` | `stoic2_f23bb5785d` | P; lexicographic values; one diagram-reference tail | N/A: source-pair comparison, not a reply |
| 17 | 0.948 | `stoic2_3dd490f19c` | `stoic2_ebd476a6be` | P; baths/gym; citation and ellipsis changes | N/A: source-pair comparison, not a reply |
| 18 | 0.947 | `stoic2_97bf5b3c33` | `stoic2_51c8141702` | P; judging motives; added week/page reference | N/A: source-pair comparison, not a reply |
| 19 | 0.938 | `stoic2_ca732a011d` | `stoic2_50f5ce8efc` | P; three disciplines; missing best-bet page reference | N/A: source-pair comparison, not a reply |
| 20 | 0.935 | `stoic2_82fcac5655` | `stoic2_855579f4ed` | P; social-media oversharing; citation change | N/A: source-pair comparison, not a reply |
| 21 | 0.934 | `stoic2_ea7ef4b8cb` | `stoic2_a48d1e1940` | P; impressions/assent exercise; broken page references | N/A: source-pair comparison, not a reply |
| 22 | 0.930 | `stoic2_d26ba1032d` | `stoic2_e9528849b0` | P; four mental movements; citations differ | N/A: source-pair comparison, not a reply |
| 23 | 0.927 | `stoic2_82397d3612` | `stoic2_9378d455b6` | P; decomposing aversions; reference details differ | N/A: source-pair comparison, not a reply |
| 24 | 0.923 | `stoic2_84b3989276` | `stoic2_c727f53883` | P; present pain; week/page references differ | N/A: source-pair comparison, not a reply |
| 25 | 0.922 | `stoic2_88a914013f` | `stoic2_c4d1f8e196` | P; grammar of assent; references differ | N/A: source-pair comparison, not a reply |
| 26 | 0.916 | `stoic2_dae550513b` | `stoic2_d24ff257c3` | P; three phases of anger; references differ | N/A: source-pair comparison, not a reply |
| 27 | 0.914 | `stoic2_b82f77313e` | `stoic2_b1bfba4e0e` | P; anxiety exercise; A adds writing-practice tail | N/A: source-pair comparison, not a reply |
| 28 | 0.879 | `stoic2_98d343d196` | `stoic2_467a0cbb02` | P; cosmos/pantheism; A adds stardust tail | N/A: source-pair comparison, not a reply |
| 29 | 0.848 | `stoic2_22ccf773f6` | `stoic2_cc769a024a` | P; decomposing pain; B adds Marcus present-life quote | N/A: source-pair comparison, not a reply |
| 30 | 0.795 | `stoic2_9139fe16ba` | `stoic2_206b9db139` | P; political good exercise; worksheet/checkmark/tail edits | N/A: source-pair comparison, not a reply |
| 31 | 0.744 | `stoic2_1c30a99706` | `stoic2_afd4c4a111` | H; 2015/2016 cosmic view; different lead/tail and local edits | N/A: source-pair comparison, not a reply |
| 32 | 0.714 | `stoic2_97bc953556` | `stoic2_c5f13b2fb7` | H; 2016/2018 evening review; revised lead, numbered list, optional record tail | N/A: source-pair comparison, not a reply |
| 33 | 0.593 | `stoic2_b2f651fed6` | `stoic2_0d1aa82598` | H; 2018/2020 appropriation; 2020 short chunk truncates continuation | N/A: source-pair comparison, not a reply |
| 34 | 0.589 | `stoic2_85867cbcdc` | `stoic2_d7b5671fc4` | H; 2016/2015 mindfulness; 2015 extra framing/anxiety/time-out material | N/A: source-pair comparison, not a reply |
| 35 | 0.535 | `stoic2_c2e87ea8fa` | `stoic2_0d4e04f9fa` | H; 2016/2015 adversity; lead/tail boundaries and light revision | N/A: source-pair comparison, not a reply |

### Additional full-read pilot manifest

These targeted rows are not added to probability-sample numerators. Sources not in this table already have their checklist columns in the sample manifests.

| ID | Pilot L/R; flags | F/A | Early verdict? |
|---|---|---|---|
| `doc_1bee58220a` | P/V; — | f/p | Y |
| `doc_44bd45d783` | Y/V; — | f/p | N |
| `doc_46db86d97a` | Y/V; — | f/p | N |
| `doc_58993b60a5` | Y/V; — | f/p | N |
| `doc_7acdd9dba2` | Y/V; — | f/p | N |
| `doc_9a02ceb327` | Y/V; — | f/p | N |
| `doc_dd64218f91` | P/V; — | f/p | Y |
| `identity2_000_id_07` | Y/O; — | P/— | – |
| `identity2_001_id_30` | Y/O; — | P/— | – |
| `identity2_006_id_21` | Y/O; — | P/— | – |
| `identity2_010_id_15` | Y/O; — | P/— | – |
| `identity2_013_id_18` | Y/O; — | P/— | – |
| `identity2_017_id_20` | Y/O; — | P/— | – |
| `identity2_026_id_35` | Y/O; — | P/— | – |
| `identity2_027_id_26` | P/M; rule-scope | P/— | – |
| `identity2_039_id_30` | P/M; unasked-identity-sermon | P/— | – |
| `identity2_040_id_21` | Y/O; — | P/— | – |
| `identity2_042_id_24` | Y/O; — | P/— | – |
| `identity2_044_id_19` | Y/O; — | P/— | – |
| `identity2_049_id_12` | Y/O; — | P/— | – |
| `identity2_066_id_03` | Y/O; — | P/— | – |
| `identity2_072_id_06` | Y/O; — | P/— | – |
| `identity2_081_id_10` | P/M; rule-scope | P/— | – |
| `identity2_089_id_04` | Y/O; — | P/— | – |
| `identity2_090_id_11` | Y/O; — | P/— | – |
| `sft_ee8a4a79c6` | P/M; advocacy-exclusion | P/p | Y |

The incidental schema-read Stoic row `stoic2_358a95fe65` is also N/A for reply/act-order coding; its full source text was read.

-- PI/gpt-6.1-sol, 2026-10-27.
