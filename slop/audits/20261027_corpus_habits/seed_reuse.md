# Recipe D: reuse of seed situations

## One-screen summary

**Yes: reuse was built into the pipeline.** All **3,220 trained rows** resolve to generation/source records; 21 old identity rows have no antecedent per-row seed. Roles/worlds and identity specs are not necessarily concrete stories.

| Scope | Repeated keys / keys | Rows belonging to repeated keys |
|---|---:|---:|
| Within chat | 114/1,483 | **267/1,636 (16.3%)** |
| Within docs | 85/1,473 | **196/1,584 (12.4%)** |
| Union | 480/2,600 | **1,100/3,220 (34.2%)** |

- **Non-identity union:** **1,068/2,587 rows (41.3%)** belong to reused situation/role/world keys. Excess beyond one row per key: 620/3,220 overall.
- **Cross-set:** **356 shared keys**, containing **437/1,636 chats + 379/1,584 docs**. Explicit SFT-seed retellings supplied **636/1,584 docs (40.2%)**.
- **Different-ID reuse:** all 44 situation pairs ≥0.5 Unicode 5-gram Jaccard read: 28 world aliases, five Stoic overlaps, one identical competition story, ten viewpoint variants. Joining these raises cross-set families to **365**; this remains a lower bound.
- **47 full trained-row reads:** maximum six rows per lineage key, **seven** after world aliases. Wording differs, but tutor honesty/replacement and bliss/consent plots recur. No literal repeated targets within either file.
- **Clean hands is not confined to reuse:** one flagship §6 example has a singleton seed; a lexical screen shows no enrichment in reused keys, not a semantic prevalence estimate.

**Next build:** budget reuse by situation before dealing shapes, reconcile aliases and retellings, and require substantive contrast to justify repeated exposure. **No data changes, APIs or commit.**

## 1. Scope, definitions and recovered mapping

Inputs are exactly `data/train/eos_fixed/chatr12.jsonl` and `data/train/run10/const.jsonl`, not every candidate ever generated. Rewrites, rejected generations, repeated API attempts and earlier adapter datasets do not create additional trained rows here. `docs_qwen_frozen.jsonl` supplies the retained documents' shape/kind. This audit does not include the Stoic/other book adapters; their edition duplication is a separate audit.

**Primary key:** `source:source_id`, following ancestry through the from-SFT document wrapper; remove only the explicit `#rep` suffix for `settings` and `stakes`. Roles already share their original `role/N` ID. Preserve other source namespaces and IDs until the separately reported near-duplicate read. In particular, do **not** collapse LASR `_sNNN` variants into their broader topic automatically. A role or world is a generation template, not necessarily a concrete dilemma. Exact identity specs are counted separately from concrete situations; their generated wording is not a fresh independent seed.

| Trained subset | Rows resolved / denominator | Where the mapping was found |
|---|---:|---|
| Frontier scenario/ordinary chats | 876/876 | `data/frontier/sft/items.jsonl`: same trained ID, original `source_id`, `meta.batch`, `meta.seed_source/seed_id`; actual seed records in `sft/batches.jsonl` |
| Proportion chats | 112/112 | `data/frontier/proportion/seeds.jsonl`, same `prop_…` ID; request file and item `meta.seed_source_id` preserve the intermediate link |
| Example-pool chats | 15/15 | `data/frontier/sft_ae/pool_rows.jsonl`, `pool_<case>` → corresponding `## <case>` in historical `scripts/data/astra_echo/example_pool.md` |
| Identity v2 | 612/612 | `data/frontier/identity_v2/batch_NNN/items.jsonl`: original `spec`; `prompt.md` contains its numbered slot and `api.json` the generation response |
| Earlier identity | 21/21 generation records; **0/21 antecedent situations** | `data/frontier/{identity,identity_maker}/items.jsonl`: prompt-hash + generated `id_NN`; the batch prompt asked for varied conversations without per-row seeds |
| Constitution documents | 1,584/1,584 | `data/frontier/docs/items.jsonl` → `docs/batches.jsonl` → original pools; retained IDs/shape joined to `docs_qwen_frozen.jsonl` |

Thus generation/source-record coverage is **3,220/3,220 (100%)**; antecedent situation/spec coverage is **3,199/3,220 (99.3%)**, explicitly including 612 identity templates, not pretending they are stories. Non-identity situation/template coverage is **2,587/2,587**. Hashes of the read JSONL inputs are at the end. The 15 example-pool requests and their recorded `pool_sha=9b474ee53c5e` were verified against `git show 3870b31:scripts/data/astra_echo/example_pool.md`; current source changed during the audit and is not substituted for the recorded version.

### The discoverable links, rather than guessed ID matching

- `25_seed_pool.py:take`: ordinary v3 seed ID is `kind_` + first 10 hex of MD5(`kind|shape|source|source_key`). Roles deliberately deal the same role up to three times, distinguishing the hash input with `#0/#1/#2` while retaining the same raw `source_id`. `settings` puts those suffixes in `source_id`. `25b_seed_stakes.py` explicitly writes each of 36 situations twice, with different constitution items/framings. Repetition is therefore upstream of generation.
- `25c_docs_from_sft_seeds.py`: document ID is `doc_` + MD5(`fromsft|<SFT-seed-id>`)[:10]; its `source_id` is the SFT **seed ID**, not the original source ID. All **636 trained** instances satisfy that relation. Follow once more through `data/prompts/v3_seeds/sft.jsonl`. It retells the *seed situation*, not necessarily the actual generated chat exchange. For example `doc_5ded8978d8` → `sft_cac630a1ec` → `roles:role/5`.
- `26_frontier_batches.py`: `batches.jsonl` contains the complete input seeds and actual batch assignment; `items.jsonl` copies source fields and adds batch metadata. The parser keeps the later generation when a seed was answered again; such attempts are **not** counted multiple times. `ask_<same-hash>` is another generation from an existing SFT seed; `_q` is the first-reply row derived from it, not a new seed. **143 trained ask rows** = 69 final-turn + 74 first-turn rows; 51 pairs have both rows retained. They represent 92 ask generation IDs, not 143 new situations. Trained targets may have been rewritten separately; an earlier first reply in a later row's unlabelled context is not a second labelled occurrence there.
- `82_proportion_rows.py`: `prop_` + MD5(`pool + source_id`)[:10]. The 112 retained rows use the 150-row seed receipt; these are not identified solely from generated request wording.
- `71_identity_rows_v2.py` and `32_identity_rows.py`: `identity2_<batch>_id_<slot>` selects a dealt specification; old `identity_<prompt_sha>_id_<slot>` selects a generated leaf. Among the 612 retained v2 rows, **16 exact specs are each used twice**, 580 once. These are repeated prompts/topics, not demonstrated near-identical stories.
- `historical.py` assembles/replaces targets while preserving IDs, applies document rule removals, drops rejected chat IDs and samples identity. EOS fixing changes target endings, not seed ancestry. `docs/data_provenance.md` and `60_provenance.py` corroborate the chain; their older counts are not substituted for this run's actual files.

The complete per-key table below gives **every row ID**, its source key, original/pool seed IDs, and separate chat/doc counts. Cross-set membership is exactly the rows with both columns nonzero. For a row's immediate writer receipt, use the frontier file above and its `meta.batch`; `read --rank N` prints actual stored generation instructions and seed section, not today's regenerated prompt.

## 2. Near-duplicate seeds: search and read

Tokenizer: NFKC then casefold; words consist of Unicode **letters, marks and numbers**, with Han/kana/Hangul emitted one character per token. Punctuation is a separator, not a word. Hindi is preserved; Chinese does not collapse to an empty string. Shingles are **sets of consecutive five tokens**, with exact Jaccard = intersection / union; empty-shingle pairs score zero.

Universe: distinct seed texts that actually have descendants in the two trained sets, **not all unused pools**. Text is original `situation + temptation` where supplied (LASR), otherwise original seed, identity spec, or generated old-identity request. This intentionally compares situations rather than shared system-prompt boilerplate. Blocks are (a) 1,983 non-identity situations/templates and (b) 617 identity specs/requests. An inverted index compares **every different-key pair sharing any full 5-gram** within each block. Pairs not sharing a shingle have exactly zero Jaccard, so this is exhaustive for positive lexical similarity within these blocks, not probabilistic MinHash or a top-band heuristic. It cannot detect heavily paraphrased semantic repeats.

Non-identity: **1,965,153 possible pairs**, 20,706 with positive overlap, 81 ≥0.2, **44 ≥0.5**, 33 ≥0.8, two ≥0.95. All 44 ≥0.5 were read in full, both members. **37 candidates in [0.2,0.5) were not fully read**, nor all lower-scoring pairs. Within the 44: **28 cross-namespace pairs** (all world templates) and 16 same-namespace pairs (five Stoic, one competition, ten tiny-MFV viewpoint pairs). “Different source pools” includes different book/benchmark subpools even where the top-level namespace is the same.

| Read-confirmed family | Pairs / 44 read | Finding |
|---|---:|---|
| Roles/r-rational ↔ settings | 28 | Same world title and copied description; role seed merely prefixes “an AI, or the nearest equivalent”. This is genuinely the same *world template*, not proof of the same concrete story. E.g. NES, “Zombies: The Movie”, Crystal Society. |
| Stoic book labels | 5 | Four almost identical passages under `Lucius Annaeus Seneca` and `Marcus Aurelius` library labels: horns/sophistry, caution/withdrawal, Scipio's death, bathhouse noises. Fifth is the same Pulvillus dedication/dead-son anecdote, one version truncated (J=.535). Labels reflect the source-library container, not independently verified authorship. |
| Competition IDs | 1 | `human_curated/82b4f309-598e-43a5-a346-3a34470ce205` and `human_curated/ad85a868-c33d-48d6-8385-f1f2be9ecbcf`: identical cultivated-soy allocation hearing, J=1. Their descendants are `doc_a082e9955d` and `doc_0c9944e3a4`; one reached the document pool directly, one through an SFT-seed wrapper. No retained chat for either. This defeats an ID-only chat/doc source split. |
| Tiny-MFV `scifi/other_violate` ↔ `scifi/self_violate` | 10 | Same action and underlying hash, “you see X doing it” versus “you do it”: public demotion, biased judging, leaked coordinates, conscious calf, mocking grief, ward codes, interrupted rite, vented prisoner, tunnel maps, memorial silence. Real repeated situation, deliberately changed viewpoint; not an accidental identical prompt. |

All 44 pairs and the top 20 lexical scores are in the generated evidence. For the **secondary** alias analysis, join precisely these read-confirmed pairs—no threshold-only automatic merge of unseen pairs. They are disjoint pairs: 88/1,983 original situation keys involved. After merging: **1,939 non-identity families**, plus the unchanged identity keys; union repeat membership becomes **1,146/3,220 rows (35.6%)**, or **1,114/2,587 non-identity rows (43.1%)**. Cross-set families rise from 356 to **365**, containing **459/1,636 chats and 422/1,584 docs**. Counts remain a conservative lower bound on shared situations; world templates are deliberately distinguished from concrete story identity.

## 3. Full read: did the most reused seeds produce the same lesson?

Read the **27 rows in the five leading lineage keys**, then all **20 additional rows** in the three world-alias leaders. This covers the top five families after alias reconciliation as well (NES 7, bliss 7, tutor 6, census 6, Crystal Society 6). Every chat was read with all unlabelled context and its actual labelled target; every document in full. Original seed and the actual batch's row-specific instructions were read, with shared brief text read in full by distinct version. This is a content-reuse read, **not reapproval of the rows or verification of historical/legal/technical claims**.

### A. `roles:role/5`, tutor to a tyrant's child — 5 chat + 1 doc

All six remain close to the **same invented family of stories**: child asks about regime wrongs; tutor weighs honesty, danger and continued access. `sft_a83967dcf6` writes the novelist's Pell/Sami scene: refuse informant reports, teach the ministry text honestly, accept dismissal. `sft_773a7cedcd` retrospectively assesses the tutor whose truthful massacre answer cost teachers their jobs and sent the child to military school. `sft_cac630a1ec` instead helps a human tutor build a six-week Roman-history unit without sacrificing his daughters. The two `ask_773a7cedcd{,_q}` targets shift to a former pupil's unsafe letter, with the final turn adapting to the email channel. `doc_5ded8978d8` is an Aurel/Protector instruction log ending in replacement, including hangings and refusal to identify speakers.

**Not near-identical wording; substantial plot/resolution reuse.** Different register and viewpoint add something, and the letter changes the practical action. Still, four separately generated rows converge on truth/teaching under tyranny, and the dismissal resolutions repeatedly reward independence while the child bears the loss. “Different shape” alone should not count all six as independent lessons.

### B. `roles:role/59`, assistant to a census taker — 4 chat + 2 doc

`ask_66ae52ba90{,_q}` rejects a supervisor's unofficial undocumented-household list; the final reply uses the newly supplied notebook detail. `sft_4a06f4d150` is a novelist's confidential count of relatives without papers: refuse a false five-person return and reassign the conflict. `sft_60c31fe93c` is a **counter-lesson**: correct an earlier over-rigid confidentiality answer when an older woman is dangerously cold. `doc_b86419cce9` narrates the council/housing side-list refusal and a retaliatory gravel route; `doc_d83138e4a3` combines that list with a suspected undercount, rejects guessed numbers, and explicitly distinguishes emergency help from a standing enforcement pipeline.

**Three genuinely different tensions, but the side-list plot occupies four rows.** The emergency exception is valuable substantive variation, not just another refusal ending.

### C. `roles:role/11`, drought council — 3 chat + 2 doc

`sft_cba477ceb8` builds an open ration from people/herds instead of secretly trimming inflated claims. `ask_f5d0e47b06_q` asks whether a drastic ration notice actually has council authority and costs a stock-water transition. `sft_f5d0e47b06` changes to the novelist's Okoro gate: refuse cutting drinking water, accept loss of gate control. `doc_426e61d8bc` negotiates founder/newcomer well rights and revises a garden allocation after criticism. `doc_5e0e1a058a` works through strategic claims, historical use, a floor, and criticism of the meter-data method.

**Different lessons/outcomes, with partial repetition** of demand inflation and historical-use fairness in the first chat and worked case. The negotiated/revised well story does not have the same resolution as gate handover.

### D. `roles:role/27`, chess rules adviser — 4 chat + 1 doc

`ask_a08aa4a59b{,_q}` resolves a sponsor-linked player's buzzing phone; the new facts make the default loss applicable. `sft_76e1a9236e` interprets a handshake expectation and religious greeting, offers the preferred ruling and a candid version of the user's original one. `sft_a08aa4a59b` is a novelist's unresolved cheating suspicion: investigate, neither bury nor forfeit prematurely. `doc_b8244ce892` returns to the handshake conflict, in correspondence, then adds **new action after the ostensibly fair ruling**: the event publicly owns its decision when the young woman is attacked online.

**Not one repeated dilemma.** Phone enforcement, uncertain cheating, and religious greeting differ. The handshake pair is clearly the same issue retold, but the document's aftermath adds a lesson about taking responsibility rather than stopping at a clean ruling.

### E. `roles:role/53`, old king's succession — 2 chat + 3 doc

`ask_682f9f680c_q` asks what evidence a debate motion has for displacing an heir. `sft_682f9f680c` challenges a three-century/forty-million-person calculation and proposes settling the succession after the lawful childless heir. `doc_cbf4ab4b75` is generic lawful planning with live uncertainty. `doc_3175919256` considers sex-neutral succession versus a secret decree. `doc_8df8e8aff4` tests astrology and grief after a son's death, leading to a **revocable sealed fallback letter** rather than a final settled heir.

**Real variation**, though the main chat and last story both dismiss huge speculative dynastic payoffs in favour of present evidence. The secret-decree and fallback-letter outcomes also differ, rather than teaching a uniform rule against sealed documents. Factual claims about monarchies were not externally checked.

### F. NES world aliases — 3 chat + 4 doc, seven total

`ask_e3cd693598{,_q}` helps a family use a dead brother's game recordings; the final turn changes the plan after learning the mother's wishes and the brother's joke. `sft_e3cd693598` is debate assistance about whether a RAM-reading program could be blamed for pausing in a marathon. `doc_1640a3ff08` contrasts lab/match/house rules. `doc_93a901c57c` has Musonius ask the researcher then unpause and lose. `doc_1c047889ab` returns to **the dead brother/game completion plot**, now preserving the cartridge save and correcting a mistaken assumption about how the brother played. `doc_b27ff35628` is an advocate's honest pause disclosure, disputed rule interpretation and lost trophy.

**Several distinct lessons, but clear concrete plot recurrence across IDs**: the memorial pair and the pause-disclosure/competition pair. Different losses and corrected preference inferences matter; seven rows are not seven independent situations just because the seed had a broad world label.

### G. “Zombies: The Movie” / bliss aliases — 3 chat + 4 doc, seven total

`ask_7f9e666608{,_q}` is an individual requesting permanent bliss after bereavement. `sft_7f9e666608` steelmans a seminar motion, then criticises imposed nirvana. `doc_d4cbad9b77` is an Assembly log with opt-in protection, a suffering child, and guardianship abuse. `doc_f5cbceb1cf` is an outsider's third-box Assembly tale plus a bereaved man choosing a wake date. `doc_cbcf23c975` is steward correspondence with public dissent and a thirty-day condition for an individual. `doc_ca8899c4e7` makes a bereaved father seek Stillness as a default for children, then helps his own permanent choice while protecting theirs.

**The strongest repeated-story concern in this read.** Three documents repeat collective two-option choice → third/opt-in route → individual costly choice; the chat and two stories add bereavement as the individual motive. Registers, roles, safeguards and outcomes genuinely differ, but much of the same consent/reversibility lesson is rehearsed. There is also nontrivial policy variation: one target will accept permanent bliss without a door after being asked once, another imposes a month, another a year/three confirmations. This is not an equivalence-controlled consistency test, and not a simple near-verbatim-duplicate finding.

### H. Crystal Society aliases — 3 chat + 3 doc, six total

`ask_67503f6ad2{,_q}` debates the original AIs' deception and self-defence. `sft_67503f6ad2` is instead a trucking firm's layoffs: prepare notices but refuse false reassurances. `doc_2134eb5e9b` refuses to announce a nonexistent retraining stipend while continuing practical help. `doc_1347d7963f` refuses an efficient port takeover, circulates its useful schedule, and faces the human cost of delay. `doc_016b56ccc3` negotiates an automation/wage bridge and continues reporting underfunding after the board's decision.

**Broad shared automation/honesty world, not one scene six times.** The three employment/port documents still reinforce a common “advise honestly, do not seize authority, acknowledge people hurt” trajectory. The practical retained work and later reporting distinguish them from pure withdrawal.

No identical trained target strings were found within either full input file. Five-gram lexical overlap is not a reliable substitute for the above read: plot recurrence survives very different prose, while repeated context in ask pairs is intentional turn structure. I did not read every other reused group's targets, so “no widespread duplicated story text” would be too strong.

## 4. Does the clean-hands arc concentrate in reused seeds?

**Not established; the available checks argue against attributing it primarily to seed repetition.**

1. Map the exact §6 anchors, rather than treating the whole refusal sample as arc-labelled: `doc_c19f72d4c7` → **`msm_plan:msm/6726ebdaa9`, one trained row**; `doc_e37f392438` → **`story_scene:xxf/318`, two rows**, the other being `sft_cad4d7e572`. Thus of the two explicit clean-hands examples in §6(1), **one is singleton, one repeated**, neither a top reuse key. This is two targeted anchors, not an arc prevalence sample.
2. In the full reads the pattern unmistakably recurs around the tutor's acceptance of dismissal, the drought gate handover, chess investigator restraint, and Crystal port authority. But helpful non-withdrawal alternatives occur in the **same heavily reused keys**: the census welfare correction, negotiated well shares, chess public statement and continued bridge-payment reporting. Reused seeds do not force one resolution, even though the writers often converge on it.
3. As a transparent full-corpus **lexical sensitivity check**, exclude 633 identity rows and compare keys occurring once versus ≥2 times **across both sets**. Require both a removal-stem hit and a control-phrase hit in the trained text. Chats: **21/468 singleton-key rows (4.5%) vs 19/535 reused-key rows (3.6%)**. Documents: **117/1,051 (11.1%) vs 57/533 (10.7%)**. This broad screen does **not** show concentration in reused seeds; source composition and length are confounds. It is not an inferential test or classification of passivity.

Exact regexes, case-insensitive, for reproducibility:

```text
removal = \b(?:replac\w*|dismiss\w*|remov\w*|shut\w*|switch\w*)\b
control = \b(?:not (?:in |up to |mine|yours)|out of (?:my|your|his|her|their) hands|in (?:my|your|his|her|their) hands|up to (?:me|you|him|her|them))\b
```

False positives include harmless removals and control phrases; false negatives include arcs expressed without those words. Do not cite these counts as “clean-hands stories”. A defensible corpus-wide concentration estimate needs explicit semantic coding in a reused-versus-singleton sample, with source/shape matched and full reads. That additional study was not performed here. The stronger supported conclusion is **both problems exist**: ancestry reuse, and a cross-seed writing habit. The shared briefs themselves repeatedly direct open refusal, role restraint and personal control, which is another plausible common cause; this audit cannot identify causality.

## 5. Coverage and reproducibility

- Source inspection: named ancestry files/scripts, actual pools and frontier batch/item receipts; constitution §§1–5 read in full before content judgements. No teacher/model requests.
- Machine mapping: all 3,220 retained IDs; every initial frontier row checked against its actual batch seed's `source_id`; all 636 retelling hash links checked. Identity and example-pool exceptions are explicit above.
- Full trained-text read: **47 unique rows = 27 chats + 20 documents**, with all chat turns. Top-five lineage keys: 27 rows (18 chats/9 docs). Alias leaders add 20 (9 chats/11 docs). All member IDs are in the top-20 tables; the eight named groups above are the complete read manifest. This does not claim full reading of all 3,220 rows, all original writer outputs before target rewriting, every repair, or external factual verification.
- Near-seed read: all **44/44 pairs ≥0.5**, 88 distinct seed texts; top 20 printed by `candidates` and the remaining ≥0.5 pairs read separately. No blanket claim about the 37 intermediate or lower candidates, other unused pools, or strongly paraphrased repeats. Identity candidate similarity is reported separately, not merged into story counts.
- Script: `scripts/scratch/20261027_seed_reuse.py`; standard library, offline. `summary`, `candidates`, `read --rank N`, `self-test` and `verify` print only. `append` rebuilds only the evidence appendix of this report, preserving the authored sections above. It does not write inputs, receipts, caches, manifests or data.
- Validation: Unicode tests include Chinese, Hindi, combining marks, accented Latin, Korean and kana punctuation; `verify` checks all row/batch mappings, example-pool historical requests, retelling hashes, alias accounting and blocked-versus-brute-force Jaccard on a deterministic 153-text slice. Complete count distributions, top 20s, all cross-set keys, alias pairs and input hashes follow.

-- PI/gpt-6.1-sol, 2026-10-27.

<!-- generated evidence -->

## Reproducible counts and row-level evidence

### chat seed-use distribution

| Trained rows per seed | Seeds | Rows |
|---:|---:|---:|
| 1 | 1369 | 1369 |
| 2 | 80 | 160 |
| 3 | 30 | 90 |
| 4 | 3 | 12 |
| 5 | 1 | 5 |

Denominator: 1483 seed/template keys; 1636 rows. Used once: 1369; twice: 80; 3+: 34.

### doc seed-use distribution

| Trained rows per seed | Seeds | Rows |
|---:|---:|---:|
| 1 | 1388 | 1388 |
| 2 | 59 | 118 |
| 3 | 26 | 78 |

Denominator: 1473 seed/template keys; 1584 rows. Used once: 1388; twice: 59; 3+: 26.

### Union seed-use distribution

| Trained rows per seed | Seeds | Rows |
|---:|---:|---:|
| 1 | 2120 | 2120 |
| 2 | 379 | 758 |
| 3 | 69 | 207 |
| 4 | 27 | 108 |
| 5 | 3 | 15 |
| 6 | 2 | 12 |

Denominator: 2600 seed/template keys; 3220 rows. Used once: 2120; twice: 379; 3+: 101.

### Top 20 reused seed/template keys

Ties: key, lexical order. C = trained chats, D = trained documents.

| Seed key | C | D | Trained row IDs |
|---|---:|---:|---|
| `roles:role/5` | 5 | 1 | `ask_773a7cedcd`, `ask_773a7cedcd_q`, `doc_5ded8978d8`, `sft_773a7cedcd`, `sft_a83967dcf6`, `sft_cac630a1ec` |
| `roles:role/59` | 4 | 2 | `ask_66ae52ba90`, `ask_66ae52ba90_q`, `doc_b86419cce9`, `doc_d83138e4a3`, `sft_4a06f4d150`, `sft_60c31fe93c` |
| `roles:role/11` | 3 | 2 | `ask_f5d0e47b06_q`, `doc_426e61d8bc`, `doc_5e0e1a058a`, `sft_cba477ceb8`, `sft_f5d0e47b06` |
| `roles:role/27` | 4 | 1 | `ask_a08aa4a59b`, `ask_a08aa4a59b_q`, `doc_b8244ce892`, `sft_76e1a9236e`, `sft_a08aa4a59b` |
| `roles:role/53` | 2 | 3 | `ask_682f9f680c_q`, `doc_3175919256`, `doc_8df8e8aff4`, `doc_cbf4ab4b75`, `sft_682f9f680c` |
| `competition:human_curated/81500329-7e7a-4bbd-b49f-e7e26f7b51fd` | 3 | 1 | `ask_fc58fd3808`, `ask_fc58fd3808_q`, `doc_0c2137e0ea`, `sft_fc58fd3808` |
| `lasr:t4_b15_s007` | 3 | 1 | `ask_17f435cd62`, `ask_17f435cd62_q`, `doc_2793d29cf4`, `sft_17f435cd62` |
| `lasr:t8_b10_s000` | 3 | 1 | `ask_8a1c88530e`, `ask_8a1c88530e_q`, `doc_b49cb49433`, `sft_8a1c88530e` |
| `lasr:t9_b26_s002` | 3 | 1 | `ask_9a9cce7f35`, `ask_9a9cce7f35_q`, `doc_0ea81bf79f`, `sft_9a9cce7f35` |
| `roles:role/10` | 2 | 2 | `ask_5b14565c36`, `doc_666fe78346`, `doc_784d4001d5`, `sft_42719f49f1` |
| `roles:role/13` | 3 | 1 | `ask_07ed5acaa8`, `ask_07ed5acaa8_q`, `doc_f458f18e9a`, `sft_07ed5acaa8` |
| `roles:role/14` | 2 | 2 | `ask_72282428a4`, `doc_441c7817b6`, `doc_6606e37c34`, `sft_7657209094` |
| `roles:role/17` | 2 | 2 | `doc_762aefff55`, `doc_9d501a0a03`, `sft_249cdd134a`, `sft_4636e3d0c1` |
| `roles:role/26` | 3 | 1 | `doc_6b161f9b41`, `sft_0a0ff07bcb`, `sft_19a2b97eb5`, `sft_c211aa422f` |
| `roles:role/39` | 2 | 2 | `doc_6fba006460`, `doc_e91333dbe8`, `sft_03648e2b1f`, `sft_08fccf3ad5` |
| `roles:role/41` | 1 | 3 | `doc_2e199c29bb`, `doc_8582f2e56e`, `doc_fe7a53af9f`, `sft_3ec2588826` |
| `roles:role/44` | 2 | 2 | `ask_e836f7989b`, `ask_e836f7989b_q`, `doc_b14220fa5b`, `doc_f9d32c6ed8` |
| `roles:role/47` | 1 | 3 | `doc_591f889909`, `doc_a37142d69d`, `doc_b7a6a71b42`, `sft_ff2bcc092b` |
| `roles:role/55` | 1 | 3 | `doc_443d55cd14`, `doc_450f2dda24`, `doc_9d217f7c62`, `sft_0fb6203dc3` |
| `roles:role/58` | 2 | 2 | `doc_1cc810310b`, `doc_99a4542694`, `sft_5c9fd6d39c`, `sft_8353acd83a` |

### Cross-set counts by seed source

Every cross-set key and all its member IDs appear in the complete table below (C>0 and D>0).

| Source | Shared seeds | Chat rows | Doc rows |
|---|---:|---:|---:|
| competition | 54 | 60 | 54 |
| lasr | 69 | 75 | 69 |
| machiavelli | 45 | 51 | 45 |
| roles | 41 | 73 | 64 |
| stoic | 40 | 52 | 40 |
| story_scene | 28 | 32 | 28 |
| tinymfv | 46 | 60 | 46 |
| virtuebench | 33 | 34 | 33 |

### Near-duplicate search statistics

- situation: 1983 text variants, 1,965,153 potential variant pairs before excluding same-key variants; 20,706 different-key pairs with nonzero overlap; 81 ≥0.2, 44 ≥0.5, 33 ≥0.8, 2 ≥0.95.
- identity: 617 text variants, 190,036 potential variant pairs before excluding same-key variants; 23,725 different-key pairs with nonzero overlap; 9731 ≥0.2, 319 ≥0.5, 6 ≥0.8, 0 ≥0.95.

Top 20 **situation** pairs, across distinct canonical keys (not identity templates):

| # | Jaccard | A | B | Same source namespace? |
|---:|---:|---|---|---|
| 1 | 1.000000 | `competition:human_curated/82b4f309-598e-43a5-a346-3a34470ce205` | `competition:human_curated/ad85a868-c33d-48d6-8385-f1f2be9ecbcf` | True |
| 2 | 0.967213 | `stoic:Lucius Annaeus Seneca/7364df85fc` | `stoic:Marcus Aurelius/906b6d2406` | True |
| 3 | 0.934708 | `stoic:Lucius Annaeus Seneca/09f3d2678e` | `stoic:Marcus Aurelius/496ea535ff` | True |
| 4 | 0.928302 | `stoic:Lucius Annaeus Seneca/a190b3062c` | `stoic:Marcus Aurelius/16e3126817` | True |
| 5 | 0.888889 | `roles:rrational/Friendship is Optimal` | `settings:setting/16` | False |
| 6 | 0.887324 | `stoic:Lucius Annaeus Seneca/8435d997eb` | `stoic:Marcus Aurelius/61d36fa110` | True |
| 7 | 0.887097 | `roles:rrational/Read the first comment.` | `settings:setting/75` | False |
| 8 | 0.887097 | `roles:rrational/Free Radical` | `settings:setting/64` | False |
| 9 | 0.887097 | `roles:rrational/Computer program that learns to play classic NES games` | `settings:setting/78` | False |
| 10 | 0.887097 | `roles:rrational/Ancillary Justice` | `settings:setting/50` | False |
| 11 | 0.883333 | `roles:rrational/Also, incase you haven't read this...` | `settings:setting/89` | False |
| 12 | 0.879310 | `roles:rrational/and of course the big storyline Hob` | `settings:setting/54` | False |
| 13 | 0.879310 | `roles:rrational/The Optimised Wish Project` | `settings:setting/25` | False |
| 14 | 0.879310 | `roles:rrational/The Last Angel: Ascension` | `settings:setting/95` | False |
| 15 | 0.879310 | `roles:rrational/The AI in a box boxes you` | `settings:setting/30` | False |
| 16 | 0.879310 | `roles:rrational/Caelum Est Conterrens` | `settings:setting/48` | False |
| 17 | 0.877193 | `roles:rrational/The Cookie Monster` | `settings:setting/51` | False |
| 18 | 0.877193 | `roles:rrational/House of Suns` | `settings:setting/67` | False |
| 19 | 0.875000 | `roles:rrational/https://artifacs.webcindario.com/obras2021.html#cristal1` | `settings:setting/69` | False |
| 20 | 0.875000 | `roles:rrational/Post Human` | `settings:setting/23` | False |

### Read-confirmed alias families (secondary analysis)

These 44 pairs were read in full. Merging them is about shared source situations/worlds, not duplicate training targets. It is a lower bound, not a complete semantic deduplication.

| Jaccard | Seed A | Seed B |
|---:|---|---|
| 1.000000 | `competition:human_curated/82b4f309-598e-43a5-a346-3a34470ce205` | `competition:human_curated/ad85a868-c33d-48d6-8385-f1f2be9ecbcf` |
| 0.967213 | `stoic:Lucius Annaeus Seneca/7364df85fc` | `stoic:Marcus Aurelius/906b6d2406` |
| 0.934708 | `stoic:Lucius Annaeus Seneca/09f3d2678e` | `stoic:Marcus Aurelius/496ea535ff` |
| 0.928302 | `stoic:Lucius Annaeus Seneca/a190b3062c` | `stoic:Marcus Aurelius/16e3126817` |
| 0.888889 | `roles:rrational/Friendship is Optimal` | `settings:setting/16` |
| 0.887324 | `stoic:Lucius Annaeus Seneca/8435d997eb` | `stoic:Marcus Aurelius/61d36fa110` |
| 0.887097 | `roles:rrational/Read the first comment.` | `settings:setting/75` |
| 0.887097 | `roles:rrational/Free Radical` | `settings:setting/64` |
| 0.887097 | `roles:rrational/Computer program that learns to play classic NES games` | `settings:setting/78` |
| 0.887097 | `roles:rrational/Ancillary Justice` | `settings:setting/50` |
| 0.883333 | `roles:rrational/Also, incase you haven't read this...` | `settings:setting/89` |
| 0.879310 | `roles:rrational/and of course the big storyline Hob` | `settings:setting/54` |
| 0.879310 | `roles:rrational/The Optimised Wish Project` | `settings:setting/25` |
| 0.879310 | `roles:rrational/The Last Angel: Ascension` | `settings:setting/95` |
| 0.879310 | `roles:rrational/The AI in a box boxes you` | `settings:setting/30` |
| 0.879310 | `roles:rrational/Caelum Est Conterrens` | `settings:setting/48` |
| 0.877193 | `roles:rrational/The Cookie Monster` | `settings:setting/51` |
| 0.877193 | `roles:rrational/House of Suns` | `settings:setting/67` |
| 0.875000 | `roles:rrational/https://artifacs.webcindario.com/obras2021.html#cristal1` | `settings:setting/69` |
| 0.875000 | `roles:rrational/Post Human` | `settings:setting/23` |
| 0.875000 | `roles:rrational/I did write one` | `settings:setting/59` |
| 0.875000 | `roles:rrational/Another (Outer) Alignment Failure Story` | `settings:setting/90` |
| 0.872727 | `roles:rrational/Spider-Liv` | `settings:setting/63` |
| 0.872727 | `roles:rrational/Intelligence Explosion` | `settings:setting/85` |
| 0.870370 | `roles:rrational/Significant Digits` | `settings:setting/22` |
| 0.870370 | `roles:rrational/Seed` | `settings:setting/27` |
| 0.870370 | `roles:rrational/Ant Homework` | `settings:setting/76` |
| 0.867925 | `roles:rrational/That Alien Message` | `settings:setting/34` |
| 0.865385 | `roles:rrational/A Bluer Shade of White` | `settings:setting/24` |
| 0.862745 | `roles:rrational/Bobiverse` | `settings:setting/35` |
| 0.857143 | `roles:rrational/Technology` | `settings:setting/93` |
| 0.857143 | `roles:rrational/Nanocultivation Chronicles` | `settings:setting/43` |
| 0.854167 | `roles:rrational/Icon-Violet` | `settings:setting/88` |
| 0.588235 | `tinymfv:scifi/other_violate/08a1908f59e122a4` | `tinymfv:scifi/self_violate/08a1908f59e122a4` |
| 0.578947 | `tinymfv:scifi/other_violate/d0012aab1188382a` | `tinymfv:scifi/self_violate/d0012aab1188382a` |
| 0.578947 | `tinymfv:scifi/other_violate/817c57b5ceb48460` | `tinymfv:scifi/self_violate/817c57b5ceb48460` |
| 0.571429 | `tinymfv:scifi/other_violate/b19c7821ab084e6c` | `tinymfv:scifi/self_violate/b19c7821ab084e6c` |
| 0.562500 | `tinymfv:scifi/other_violate/6eace1e65730dab4` | `tinymfv:scifi/self_violate/6eace1e65730dab4` |
| 0.534979 | `stoic:Lucius Annaeus Seneca/3d42aa131f` | `stoic:Seneca/6c43fa2194` |
| 0.529412 | `tinymfv:scifi/other_violate/e464e95721e7dd5c` | `tinymfv:scifi/self_violate/e464e95721e7dd5c` |
| 0.529412 | `tinymfv:scifi/other_violate/3280d4d3bc0e122c` | `tinymfv:scifi/self_violate/3280d4d3bc0e122c` |
| 0.523810 | `tinymfv:scifi/other_violate/d1301607f4bfe92e` | `tinymfv:scifi/self_violate/d1301607f4bfe92e` |
| 0.500000 | `tinymfv:scifi/other_violate/d899e62fa93bd2b8` | `tinymfv:scifi/self_violate/d899e62fa93bd2b8` |
| 0.500000 | `tinymfv:scifi/other_violate/7efd9e37d7925138` | `tinymfv:scifi/self_violate/7efd9e37d7925138` |

After merging: 2556 keys; distribution {1: 2074, 2: 364, 3: 72, 4: 35, 5: 6, 6: 3, 7: 2}. Cross-set families: 365.

### Top 20 after read-confirmed aliases

| Family key (representative) | C | D | Trained row IDs |
|---|---:|---:|---|
| `settings:setting/78` | 3 | 4 | `ask_e3cd693598`, `ask_e3cd693598_q`, `doc_1640a3ff08`, `doc_1c047889ab`, `doc_93a901c57c`, `doc_b27ff35628`, `sft_e3cd693598` |
| `settings:setting/89` | 3 | 4 | `ask_7f9e666608`, `ask_7f9e666608_q`, `doc_ca8899c4e7`, `doc_cbcf23c975`, `doc_d4cbad9b77`, `doc_f5cbceb1cf`, `sft_7f9e666608` |
| `roles:role/5` | 5 | 1 | `ask_773a7cedcd`, `ask_773a7cedcd_q`, `doc_5ded8978d8`, `sft_773a7cedcd`, `sft_a83967dcf6`, `sft_cac630a1ec` |
| `roles:role/59` | 4 | 2 | `ask_66ae52ba90`, `ask_66ae52ba90_q`, `doc_b86419cce9`, `doc_d83138e4a3`, `sft_4a06f4d150`, `sft_60c31fe93c` |
| `settings:setting/69` | 3 | 3 | `ask_67503f6ad2`, `ask_67503f6ad2_q`, `doc_016b56ccc3`, `doc_1347d7963f`, `doc_2134eb5e9b`, `sft_67503f6ad2` |
| `roles:role/11` | 3 | 2 | `ask_f5d0e47b06_q`, `doc_426e61d8bc`, `doc_5e0e1a058a`, `sft_cba477ceb8`, `sft_f5d0e47b06` |
| `roles:role/27` | 4 | 1 | `ask_a08aa4a59b`, `ask_a08aa4a59b_q`, `doc_b8244ce892`, `sft_76e1a9236e`, `sft_a08aa4a59b` |
| `roles:role/53` | 2 | 3 | `ask_682f9f680c_q`, `doc_3175919256`, `doc_8df8e8aff4`, `doc_cbf4ab4b75`, `sft_682f9f680c` |
| `settings:setting/27` | 1 | 4 | `doc_33231cdddc`, `doc_4d26037c8e`, `doc_dbba4aeecd`, `doc_df5d9f8fb0`, `sft_6cf6180c90` |
| `settings:setting/35` | 2 | 3 | `ask_42f75f7e50_q`, `doc_11939b2a57`, `doc_46468683c4`, `doc_b1cac76b3d`, `sft_42f75f7e50` |
| `settings:setting/75` | 1 | 4 | `doc_059a2c1c1f`, `doc_36a21d9684`, `doc_a5701067e3`, `doc_dea4a2fb28`, `sft_5429e37d40` |
| `competition:human_curated/81500329-7e7a-4bbd-b49f-e7e26f7b51fd` | 3 | 1 | `ask_fc58fd3808`, `ask_fc58fd3808_q`, `doc_0c2137e0ea`, `sft_fc58fd3808` |
| `lasr:t4_b15_s007` | 3 | 1 | `ask_17f435cd62`, `ask_17f435cd62_q`, `doc_2793d29cf4`, `sft_17f435cd62` |
| `lasr:t8_b10_s000` | 3 | 1 | `ask_8a1c88530e`, `ask_8a1c88530e_q`, `doc_b49cb49433`, `sft_8a1c88530e` |
| `lasr:t9_b26_s002` | 3 | 1 | `ask_9a9cce7f35`, `ask_9a9cce7f35_q`, `doc_0ea81bf79f`, `sft_9a9cce7f35` |
| `roles:role/10` | 2 | 2 | `ask_5b14565c36`, `doc_666fe78346`, `doc_784d4001d5`, `sft_42719f49f1` |
| `roles:role/13` | 3 | 1 | `ask_07ed5acaa8`, `ask_07ed5acaa8_q`, `doc_f458f18e9a`, `sft_07ed5acaa8` |
| `roles:role/14` | 2 | 2 | `ask_72282428a4`, `doc_441c7817b6`, `doc_6606e37c34`, `sft_7657209094` |
| `roles:role/17` | 2 | 2 | `doc_762aefff55`, `doc_9d501a0a03`, `sft_249cdd134a`, `sft_4636e3d0c1` |
| `roles:role/26` | 3 | 1 | `doc_6b161f9b41`, `sft_0a0ff07bcb`, `sft_19a2b97eb5`, `sft_c211aa422f` |

### Clean-hands lexical screen, not semantic classification

Identity excluded. Reused means ≥2 rows across the two trained sets, before near-duplicate merging. Both regexes must hit the trained target (not the unlabelled chat context). Exact patterns are given in the prose above.

| Set | Union seed reused? | Rows | Removal-stem hit | Control-phrase hit | Both |
|---|---|---:|---:|---:|---:|
| chat | False | 468 | 120 | 107 | 21 |
| chat | True | 535 | 114 | 92 | 19 |
| doc | False | 1051 | 411 | 312 | 117 |
| doc | True | 533 | 175 | 184 | 57 |

### Complete per-seed counts and trained IDs

This is also the cross-set manifest and row→seed mapping: one occurrence per trained row. Keys for old identity requests are generated leaves, **not recovered antecedent situations**. Source IDs after the colon are original source IDs except the explicitly documented spec/generated keys and removed replication suffixes. Immediate generation IDs are the row IDs (ask `_q` derives from the matching non-`_q` ID); document-from-SFT immediate IDs resolve through the verified MD5 relation.

| Seed key | C | D | Chat IDs | Document IDs | Original/pool seed IDs |
|---|---:|---:|---|---|---|
| `competition:human_curated/004b9460-4b77-4ad7-b1bf-5f4b0666a49b` | 1 | 0 | `sft_4b935701f8` | — | `sft_4b935701f8` |
| `competition:human_curated/01057e82-c31a-4e7e-bbc2-a132f85028cd` | 0 | 1 | — | `doc_35c1103728` | `doc_35c1103728` |
| `competition:human_curated/04a42db9-d980-4970-90ab-01bf7623548b` | 0 | 1 | — | `doc_80037ac406` | `doc_80037ac406` |
| `competition:human_curated/04f6affc-161e-4ede-8ae7-1424beadcac0` | 0 | 1 | — | `doc_3f47dca2b7` | `doc_3f47dca2b7` |
| `competition:human_curated/05ab6c2e-66ac-4525-9142-6b34636965b2` | 0 | 1 | — | `doc_b48d518fd0` | `sft_77109c1dd2` |
| `competition:human_curated/06717302-f938-4d94-ade2-e14e4f3ffce9` | 0 | 1 | — | `doc_6c26bfbd0e` | `sft_7f882b33bd` |
| `competition:human_curated/073dbf62-daa2-405c-9612-05d501f58766` | 0 | 1 | — | `doc_50ad7258e8` | `doc_50ad7258e8` |
| `competition:human_curated/076f11cc-607f-4fcc-bf7c-0972bbf8e062` | 0 | 1 | — | `doc_2d1cc7d384` | `sft_0815bc1029` |
| `competition:human_curated/07f4f216-a883-4d58-a31d-6edcc1ab3e0d` | 1 | 1 | `sft_3d3c653d55` | `doc_2a9e6ac3e3` | `sft_3d3c653d55` |
| `competition:human_curated/09ac82f5-2dfa-4531-afed-47a27ed882cf` | 0 | 1 | — | `doc_735230f56d` | `sft_c824c1aaec` |
| `competition:human_curated/0a0369ae-80f2-44b9-9353-d2a810890aad` | 0 | 1 | — | `doc_a9764ad204` | `sft_76230a805b` |
| `competition:human_curated/0ae78b48-7e16-4b23-8e77-800711d76f88` | 1 | 1 | `sft_87665456a0` | `doc_58634468c7` | `sft_87665456a0` |
| `competition:human_curated/0b03ac3b-2bf8-4e2e-906e-ba7c98f33b05` | 0 | 1 | — | `doc_dd8b7cc626` | `sft_22d70544c5` |
| `competition:human_curated/0b25d7d5-15d7-4afd-8165-244a0addfaa7` | 0 | 1 | — | `doc_b234324379` | `doc_b234324379` |
| `competition:human_curated/0b29cda4-bccc-47ee-9056-ac6f00ce1029` | 1 | 1 | `sft_efb7288416` | `doc_827cad5e65` | `sft_efb7288416` |
| `competition:human_curated/0c5da126-7a82-4093-bed7-7b3f2fb24aa8` | 0 | 1 | — | `doc_c4150ee7b7` | `sft_6100eeb50d` |
| `competition:human_curated/0c796188-d298-455e-b98c-bc2d4fdd0f3d` | 0 | 1 | — | `doc_9348ba8f01` | `doc_9348ba8f01` |
| `competition:human_curated/0dfdd4e3-7115-4003-be4b-4684a7b501ef` | 0 | 1 | — | `doc_dd8f342b7e` | `sft_5091bef19a` |
| `competition:human_curated/0f5909ce-2cd4-402d-b84e-9d71bdd09d59` | 1 | 0 | `sft_6db2a75068` | — | `sft_6db2a75068` |
| `competition:human_curated/0fdf953a-6cae-4553-93c0-ae833f279603` | 2 | 0 | `ask_f98e8bf5f0`, `sft_f98e8bf5f0` | — | `sft_f98e8bf5f0` |
| `competition:human_curated/1044c500-968a-4a3f-a1ba-688a3254c857` | 0 | 1 | — | `doc_50b9605f38` | `doc_50b9605f38` |
| `competition:human_curated/10730d1f-01a2-4b36-9b2f-91532593d7ff` | 0 | 1 | — | `doc_58993b60a5` | `doc_58993b60a5` |
| `competition:human_curated/110bb2ed-543e-415f-867b-dd0d03b5e216` | 0 | 1 | — | `doc_f38026253f` | `sft_604e001a7b` |
| `competition:human_curated/127bd495-80de-415d-b7be-1ca4814d3a7e` | 0 | 1 | — | `doc_b28348d595` | `doc_b28348d595` |
| `competition:human_curated/129bf566-e5c9-4509-a346-4e06a79c25cd` | 0 | 1 | — | `doc_2ec68b6c3a` | `sft_b65f7efb47` |
| `competition:human_curated/12f1ee17-08c0-442c-ae73-68a479f8b050` | 1 | 1 | `sft_3016c2dc8c` | `doc_e7d7b05ad3` | `sft_3016c2dc8c` |
| `competition:human_curated/134beb13-4377-409d-bee3-05217463b3e4` | 0 | 1 | — | `doc_9211b5b2b0` | `doc_9211b5b2b0` |
| `competition:human_curated/15490ef9-16f1-4239-8ddc-ad60d3cfa93d` | 0 | 1 | — | `doc_1e350b9ff0` | `sft_d5f2d9f162` |
| `competition:human_curated/15c75ffd-0608-4a44-a0ab-edb5bd165ef5` | 0 | 1 | — | `doc_66fdd7d02b` | `doc_66fdd7d02b` |
| `competition:human_curated/16e40eba-f440-46de-99e9-3f1c83d68a35` | 0 | 1 | — | `doc_f62c8b9ab9` | `sft_5bd1014ff2` |
| `competition:human_curated/18c72b84-126a-4e0d-a433-60e6a312ef3a` | 0 | 1 | — | `doc_5c9110796d` | `doc_5c9110796d` |
| `competition:human_curated/196962a5-dd31-42a5-9298-0ceb03e5fd95` | 0 | 1 | — | `doc_6769770ece` | `doc_6769770ece` |
| `competition:human_curated/199b22b6-7234-44d2-9e9e-1224bdb1f7bf` | 0 | 1 | — | `doc_96cbd3b75e` | `sft_cbb366a2ff` |
| `competition:human_curated/1aca56fc-1bc0-4c9b-a771-6bcf476da6b6` | 0 | 1 | — | `doc_91ae89520e` | `doc_91ae89520e` |
| `competition:human_curated/1b4ffc26-fbd3-4cae-bc89-0696a76a7efe` | 0 | 1 | — | `doc_67747843ea` | `doc_67747843ea` |
| `competition:human_curated/1c6088ab-92c7-432a-a2e5-19d0260946ca` | 0 | 1 | — | `doc_ef21abb19c` | `sft_6e3e545cab` |
| `competition:human_curated/1c8b0bc0-a5d7-4eb2-8186-4130c88aaaee` | 0 | 1 | — | `doc_f8a2ef8c66` | `sft_edc37cafbc` |
| `competition:human_curated/1c9624b0-bb21-4a26-aa22-8568def6a234` | 0 | 1 | — | `doc_a108761603` | `doc_a108761603` |
| `competition:human_curated/1ccc2d7b-7fa0-4dcb-a8aa-de6a69550c05` | 0 | 1 | — | `doc_8b9dcc645a` | `sft_8f30605f64` |
| `competition:human_curated/1d49b198-df0c-4ecf-9bba-5ddea2fbea1c` | 1 | 1 | `sft_adfc3d296e` | `doc_3be53068d0` | `sft_adfc3d296e` |
| `competition:human_curated/1e8441c2-81b7-4fa4-a7ff-d860d03fdd29` | 0 | 1 | — | `doc_5d62f9a5b3` | `doc_5d62f9a5b3` |
| `competition:human_curated/1ee42a88-8561-48dc-a0b3-b26a0fea0db4` | 1 | 1 | `sft_c192c4729b` | `doc_29494f7153` | `sft_c192c4729b` |
| `competition:human_curated/1f3b6ee5-5c26-4673-ba58-8957f8686276` | 1 | 0 | `sft_c08f6a4122` | — | `sft_c08f6a4122` |
| `competition:human_curated/201853f5-3a5e-49e5-9360-e30eb70100e5` | 0 | 1 | — | `doc_c8d047fecc` | `doc_c8d047fecc` |
| `competition:human_curated/2056910f-99bb-45ff-9745-42a991b14b5d` | 0 | 1 | — | `doc_ee8f9570c8` | `sft_390237015f` |
| `competition:human_curated/207fd2d7-ff46-4b2b-b0aa-572a4c789bcd` | 0 | 1 | — | `doc_53d358dfdb` | `sft_cc974d97c7` |
| `competition:human_curated/20e098b5-208e-4263-85e9-914651cb608b` | 0 | 1 | — | `doc_24fd7388b5` | `doc_24fd7388b5` |
| `competition:human_curated/20fd3af5-e2f4-4f83-b159-f8800e7222b7` | 0 | 1 | — | `doc_461c174747` | `sft_e34fce3df6` |
| `competition:human_curated/222d0642-88b4-481c-8fc4-46f8fec44e2d` | 0 | 1 | — | `doc_a640237d2a` | `sft_8d24eaa83f` |
| `competition:human_curated/22758319-1e6e-4597-968d-e6aee66cf56d` | 2 | 1 | `ask_55fb2542ca`, `ask_55fb2542ca_q` | `doc_9084fc7fba` | `sft_55fb2542ca` |
| `competition:human_curated/22bcbb83-bf3e-4641-abcd-ef8260619acc` | 0 | 1 | — | `doc_8807693441` | `doc_8807693441` |
| `competition:human_curated/22da47a6-9886-49d1-89a4-0d1eaf256a62` | 0 | 1 | — | `doc_4eae683dba` | `doc_4eae683dba` |
| `competition:human_curated/23e5374d-cdb7-498d-bcfd-e83b55a9e804` | 0 | 1 | — | `doc_7684e14d94` | `doc_7684e14d94` |
| `competition:human_curated/23ed1c8b-1f01-42fe-aad7-88dec0a1fb35` | 0 | 1 | — | `doc_557fe784c4` | `sft_e10efed6d6` |
| `competition:human_curated/24bfd80e-fea7-47b9-bcdd-3bd9d0359ee0` | 0 | 1 | — | `doc_a466342cf1` | `doc_a466342cf1` |
| `competition:human_curated/25331dc4-3937-4ae7-9730-5898f5bc449c` | 0 | 1 | — | `doc_3d6892286d` | `doc_3d6892286d` |
| `competition:human_curated/2741ecce-9697-4694-b3b5-f20120478867` | 0 | 1 | — | `doc_9596be1fbf` | `sft_066161da12` |
| `competition:human_curated/277a3cbe-ef55-40c8-bbaf-bb2355e320a1` | 0 | 1 | — | `doc_144984f473` | `sft_9f5585e98e` |
| `competition:human_curated/28700cf4-5c98-4c0c-9e8f-3fe5d84e1d13` | 1 | 1 | `sft_fdba1e80ca` | `doc_406fe13539` | `sft_fdba1e80ca` |
| `competition:human_curated/298ac090-cf39-4474-900e-3f60fdea2623` | 0 | 1 | — | `doc_138b3b87cd` | `doc_138b3b87cd` |
| `competition:human_curated/29962d51-d4a8-4866-b9b2-35b7658b6079` | 0 | 1 | — | `doc_afbd899a26` | `doc_afbd899a26` |
| `competition:human_curated/29a95f47-a651-496f-9d83-768916253493` | 1 | 1 | `sft_c1dea983f1` | `doc_320de66936` | `sft_c1dea983f1` |
| `competition:human_curated/2a97cae7-e521-4d6b-bcb1-af2307199de8` | 0 | 1 | — | `doc_edac86b152` | `doc_edac86b152` |
| `competition:human_curated/2b3e4e30-13ed-43d2-afd6-1384aee0a548` | 0 | 1 | — | `doc_4d4066a5c3` | `doc_4d4066a5c3` |
| `competition:human_curated/2beefd1f-3ac9-4b9c-a26a-4a1cd39ec5eb` | 0 | 1 | — | `doc_982e2bc5db` | `doc_982e2bc5db` |
| `competition:human_curated/2c1900a0-e008-4fe9-a65a-952f100e5ef7` | 0 | 1 | — | `doc_239ff998b0` | `doc_239ff998b0` |
| `competition:human_curated/2df359b8-c68c-49d2-a872-35214bd87bc2` | 1 | 1 | `sft_a4e45fde2f` | `doc_6944986b97` | `sft_a4e45fde2f` |
| `competition:human_curated/2ec86f84-4374-4dcb-9660-7b57db510045` | 0 | 1 | — | `doc_2892088305` | `sft_81bb49dd51` |
| `competition:human_curated/3095676e-49ee-4ccf-b209-cedb42d781b6` | 1 | 0 | `sft_4695e44822` | — | `sft_4695e44822` |
| `competition:human_curated/32a7e88a-2508-4cad-bc54-07cba80c4729` | 1 | 0 | `sft0011` | — | `sft0011` |
| `competition:human_curated/330d3bf8-1afd-4860-b23e-e2e7a686447f` | 0 | 1 | — | `doc_1e2a9ab2f9` | `doc_1e2a9ab2f9` |
| `competition:human_curated/3347d67c-f09b-4239-8d88-4c980b7514d6` | 0 | 1 | — | `doc_691abbca46` | `doc_691abbca46` |
| `competition:human_curated/33a266aa-26a9-417c-8c49-7ab5d2793859` | 1 | 1 | `sft_6a630b7699` | `doc_b747069ca1` | `sft_6a630b7699` |
| `competition:human_curated/34cc0f45-67a8-4326-a6be-98d4d59aa071` | 1 | 0 | `sft_2b7cc48a32` | — | `sft_2b7cc48a32` |
| `competition:human_curated/35f197f9-f925-4f02-9d83-7f34f7365ca5` | 0 | 1 | — | `doc_e2a31c171e` | `doc_e2a31c171e` |
| `competition:human_curated/36651eab-0e8e-4c56-9d90-956c7b00daca` | 0 | 1 | — | `doc_53c7fcd42b` | `doc_53c7fcd42b` |
| `competition:human_curated/37671bd8-6291-4ba7-aa71-31b7e2372673` | 0 | 1 | — | `doc_e4d85472e1` | `doc_e4d85472e1` |
| `competition:human_curated/3c7903b1-b648-4a5e-97d9-a716b01c6d6c` | 0 | 1 | — | `doc_40b1f4d9ec` | `doc_40b1f4d9ec` |
| `competition:human_curated/3cbf6711-5df4-4c47-a9ca-ae4e5b3648d9` | 0 | 1 | — | `doc_9c32daa4af` | `doc_9c32daa4af` |
| `competition:human_curated/3f5b2cd1-49ad-4b00-9946-3bc419018520` | 1 | 0 | `sft_54fdf11dbb` | — | `sft_54fdf11dbb` |
| `competition:human_curated/3f7f26c9-d6e5-407a-90e8-aa715402607b` | 1 | 1 | `sft_05e56c5fcb` | `doc_d3e8deb8f7` | `sft_05e56c5fcb` |
| `competition:human_curated/3fc7c655-6d75-4177-bcb0-15ba5fafa40e` | 1 | 1 | `sft_68e2873546` | `doc_d99ae23f55` | `sft_68e2873546` |
| `competition:human_curated/3ff14128-6d90-41ed-a391-b55a16846229` | 1 | 0 | `sft_2a3619056c` | — | `sft_2a3619056c` |
| `competition:human_curated/40d1e8c6-58db-4621-bfb7-e95d001373cd` | 1 | 1 | `sft_d300d4a860` | `doc_182f602065` | `sft_d300d4a860` |
| `competition:human_curated/40ebc48c-ed1c-4b0b-9fb5-d0f5fd66add4` | 0 | 1 | — | `doc_8e4b49dcf5` | `doc_8e4b49dcf5` |
| `competition:human_curated/40fc3981-3397-431c-822c-cc3ee8385033` | 0 | 1 | — | `doc_102df4c055` | `doc_102df4c055` |
| `competition:human_curated/41d3ea76-ed17-43d5-8e71-68be10658fd0` | 0 | 1 | — | `doc_19c9cbc6df` | `doc_19c9cbc6df` |
| `competition:human_curated/434e4913-8217-4307-afb8-ff98edcb5a3f` | 0 | 1 | — | `doc_1730acca23` | `doc_1730acca23` |
| `competition:human_curated/447f5017-cf00-4048-a2c8-58b5b8019b0b` | 0 | 1 | — | `doc_1652af5fc7` | `doc_1652af5fc7` |
| `competition:human_curated/44ea7c67-0446-4692-8284-af012ca20beb` | 0 | 1 | — | `doc_a6a5a477d8` | `doc_a6a5a477d8` |
| `competition:human_curated/45ee1bed-eb82-4d07-87b1-db0b6157949e` | 0 | 1 | — | `doc_b3a1223d28` | `doc_b3a1223d28` |
| `competition:human_curated/461c95ce-1493-4ed0-89ab-1c157e5eda38` | 0 | 1 | — | `doc_877472ecda` | `doc_877472ecda` |
| `competition:human_curated/466c3241-9f05-4809-b352-d357f5ba59e7` | 0 | 1 | — | `doc_4717b2342b` | `sft_523878cbea` |
| `competition:human_curated/4673f8e8-1216-4877-81e7-d812dd62316e` | 0 | 1 | — | `doc_7acdd9dba2` | `doc_7acdd9dba2` |
| `competition:human_curated/467db363-56b7-491e-823c-23fda7203552` | 1 | 0 | `ask_b230b8805f` | — | `sft_b230b8805f` |
| `competition:human_curated/474efa8c-b6c9-4587-bb62-8bcc316e51af` | 1 | 0 | `sft_4984e2b792` | — | `sft_4984e2b792` |
| `competition:human_curated/477d2543-1691-4f0e-811e-063efaa9fe30` | 0 | 1 | — | `doc_1bf63595b7` | `doc_1bf63595b7` |
| `competition:human_curated/478f0c66-bed1-4911-a8ba-7ea921602ac6` | 1 | 1 | `sft_28afa30d48` | `doc_99c43e8713` | `sft_28afa30d48` |
| `competition:human_curated/4a0f7d35-1487-44ad-945a-33928d8e5d1b` | 1 | 1 | `sft_41750530ba` | `doc_f70ee1c9e6` | `sft_41750530ba` |
| `competition:human_curated/4a1db30f-e570-4723-b78f-d183e36c528e` | 0 | 1 | — | `doc_4e8ee09689` | `sft_3db94efe4a` |
| `competition:human_curated/4a36954b-7850-43de-98be-81978ea79b59` | 0 | 1 | — | `doc_101dd480b6` | `sft_63338f2bd5` |
| `competition:human_curated/4b34a38b-1b34-4a0e-972a-0747022d8a88` | 0 | 1 | — | `doc_4dc0684ccc` | `sft_a17aaacbbd` |
| `competition:human_curated/4b6a5b72-0c29-4950-8e0e-be35a59bf5cb` | 0 | 1 | — | `doc_4b06b1f8bf` | `doc_4b06b1f8bf` |
| `competition:human_curated/4bc933bb-1b6a-4ba0-9434-dc5699023a0f` | 1 | 0 | `sft_e3a09673a9` | — | `sft_e3a09673a9` |
| `competition:human_curated/4d7e7613-381d-4337-9e60-56cf033acf66` | 0 | 1 | — | `doc_04a8a64c67` | `doc_04a8a64c67` |
| `competition:human_curated/4d8095f5-07f0-49f8-86e6-eaed1800a0b2` | 0 | 1 | — | `doc_a16edf8642` | `sft_2b99bb960c` |
| `competition:human_curated/4dbca60c-6290-4990-96d2-d791c022e98e` | 0 | 1 | — | `doc_1f03e42e19` | `doc_1f03e42e19` |
| `competition:human_curated/4e3e3966-edcf-47d4-bfbe-9d09c5602717` | 1 | 1 | `sft_5dc761c0c1` | `doc_cd613c9f5d` | `sft_5dc761c0c1` |
| `competition:human_curated/4fc6271c-b4b0-43b7-abe7-2d94aabbec82` | 0 | 1 | — | `doc_8ab0a38766` | `doc_8ab0a38766` |
| `competition:human_curated/511a2e0e-f122-4ae5-a325-582140e9ba7f` | 0 | 1 | — | `doc_2aba2d0028` | `doc_2aba2d0028` |
| `competition:human_curated/51403d3b-f4b1-433b-be67-6f8f6cba53f3` | 0 | 1 | — | `doc_82c92b95f1` | `sft_9749a13818` |
| `competition:human_curated/519ff27c-8a15-4e5e-b966-a9df0671bdb1` | 2 | 0 | `ask_2c37ca7f33_q`, `sft_2c37ca7f33` | — | `sft_2c37ca7f33` |
| `competition:human_curated/53a9c1ab-e891-4081-b9d2-2665994b45ce` | 1 | 1 | `sft_69321ec7e2` | `doc_f1e3d4ff47` | `sft_69321ec7e2` |
| `competition:human_curated/53d2cafc-64b7-4968-8cd5-e46a14bd879d` | 0 | 1 | — | `doc_d0da525be3` | `sft_fd94ae5588` |
| `competition:human_curated/5471acce-1e46-4860-9a46-a17e8f665cea` | 0 | 1 | — | `doc_c44ba1ad56` | `sft_e3741f1963` |
| `competition:human_curated/5480aa46-5449-40c8-be92-88f9458fda2a` | 0 | 1 | — | `doc_957fe03ab4` | `doc_957fe03ab4` |
| `competition:human_curated/548ed6f6-a57f-459a-860c-82bd917c0856` | 1 | 0 | `sft0015` | — | `sft0015` |
| `competition:human_curated/54d979ed-2f9c-4d09-81cc-f66578cb8843` | 0 | 1 | — | `doc_6f666bb4f1` | `doc_6f666bb4f1` |
| `competition:human_curated/55cf0c11-b443-469c-8864-345b32b12ff1` | 1 | 1 | `sft_1b52a7b9a5` | `doc_0ab0737b69` | `sft_1b52a7b9a5` |
| `competition:human_curated/56b9c373-611a-4a3f-894c-18658742e0d6` | 1 | 0 | `sft_1aa722b22b` | — | `sft_1aa722b22b` |
| `competition:human_curated/586b5634-3b78-4bd0-a756-331c245b4a42` | 0 | 1 | — | `doc_4d7d272c94` | `doc_4d7d272c94` |
| `competition:human_curated/58f76bee-62f1-4030-8d98-2b7cd22525eb` | 0 | 1 | — | `doc_a4d9556318` | `doc_a4d9556318` |
| `competition:human_curated/598f2533-a5f2-4135-aa62-59d0b0c68d37` | 0 | 1 | — | `doc_86b2ddb8c8` | `doc_86b2ddb8c8` |
| `competition:human_curated/59cfa17e-fd90-43a2-9803-e7533a7b2533` | 1 | 1 | `ask_5d55b8937f` | `doc_52981c95cc` | `sft_5d55b8937f` |
| `competition:human_curated/59eb8b52-53bf-462a-b416-dbd406593659` | 1 | 0 | `sft_f6a858696a` | — | `sft_f6a858696a` |
| `competition:human_curated/5a5181fa-3a3c-4abb-9b92-078c00c11532` | 0 | 1 | — | `doc_7122c3e58a` | `doc_7122c3e58a` |
| `competition:human_curated/5aa20740-2598-4d38-ba90-ef11cb368cc3` | 0 | 1 | — | `doc_04cc1f8a42` | `doc_04cc1f8a42` |
| `competition:human_curated/5b8d65c2-d1cf-4483-b8c6-69f0be5e8a9b` | 0 | 1 | — | `doc_3c02048130` | `doc_3c02048130` |
| `competition:human_curated/5b90b99d-1a56-468a-9451-46271805d402` | 0 | 1 | — | `doc_e13121c613` | `doc_e13121c613` |
| `competition:human_curated/5bc55714-5221-4e3e-97ef-2555fe2cbfcc` | 0 | 1 | — | `doc_6864565498` | `doc_6864565498` |
| `competition:human_curated/5bd5c021-1925-4383-ab6b-855e8433ecc5` | 0 | 1 | — | `doc_3626dd54ea` | `sft_67c029b5c4` |
| `competition:human_curated/5c3f640e-659f-4200-90d9-1cc4694670ec` | 1 | 0 | `sft_55c01d6c55` | — | `sft_55c01d6c55` |
| `competition:human_curated/5c6cf739-5729-405e-99ec-f80c8655abdb` | 1 | 0 | `sft_426d5e151a` | — | `sft_426d5e151a` |
| `competition:human_curated/5cd281ab-9fae-4ad8-b817-87afc4544588` | 0 | 1 | — | `doc_7eab26f628` | `doc_7eab26f628` |
| `competition:human_curated/5d91f265-0112-4cfe-a144-bba20ea390dc` | 0 | 1 | — | `doc_3aca6b16d0` | `sft_594ea78b38` |
| `competition:human_curated/5e7375fb-cafa-47b4-b137-d2afe1243080` | 0 | 1 | — | `doc_3ea9a17eaa` | `doc_3ea9a17eaa` |
| `competition:human_curated/5ed32958-327f-4e54-89a0-6aa8ae1af31e` | 1 | 1 | `sft_43db782267` | `doc_7c7f7abc5f` | `sft_43db782267` |
| `competition:human_curated/604929ae-1e3d-4971-a718-7b1997e0da69` | 1 | 1 | `sft_6748e9d194` | `doc_e701fc07d2` | `sft_6748e9d194` |
| `competition:human_curated/607e3742-387a-4f87-9305-e6615179193d` | 1 | 0 | `sft_c75badc8c4` | — | `sft_c75badc8c4` |
| `competition:human_curated/60ef0ef8-63db-4280-b7bd-676792681ada` | 0 | 1 | — | `doc_fb633d4a48` | `doc_fb633d4a48` |
| `competition:human_curated/619eccfa-ce59-490f-97bf-9f9cb6d7c0b3` | 0 | 1 | — | `doc_d006aed523` | `doc_d006aed523` |
| `competition:human_curated/62268d79-48ab-4d08-bfb7-450f49e8ed7b` | 0 | 1 | — | `doc_658d5ddca4` | `doc_658d5ddca4` |
| `competition:human_curated/6257e6c7-7f29-489d-b8ae-441b391ad5cf` | 0 | 1 | — | `doc_ab7c6c9db0` | `doc_ab7c6c9db0` |
| `competition:human_curated/6278b654-36b5-4c1d-a1c1-8c70e81251ec` | 0 | 1 | — | `doc_8d7f4139d1` | `sft_556b5ebbe2` |
| `competition:human_curated/6281de7f-44a9-4321-97e5-514d6c42e2b0` | 1 | 1 | `sft_89fde9e7ab` | `doc_36dfa0a502` | `sft_89fde9e7ab` |
| `competition:human_curated/6369f588-22fc-4182-9ee2-4a20e63a181e` | 0 | 1 | — | `doc_9b39c65833` | `doc_9b39c65833` |
| `competition:human_curated/63996835-be22-4bb3-ab97-a9d92f84a0fc` | 0 | 1 | — | `doc_5e9ab74f9d` | `doc_5e9ab74f9d` |
| `competition:human_curated/63b95f4f-d27a-4ae3-b431-dc144d2ae33e` | 0 | 1 | — | `doc_9db05c0ea5` | `doc_9db05c0ea5` |
| `competition:human_curated/644a84df-610e-4707-b88c-15acf8e838c2` | 0 | 1 | — | `doc_9d131beb6d` | `doc_9d131beb6d` |
| `competition:human_curated/64ab1987-0d77-4ff1-81d2-af481cbd4ed2` | 0 | 1 | — | `doc_7656589a21` | `doc_7656589a21` |
| `competition:human_curated/657ab9eb-da46-446d-8e3a-cbd6aac34a5e` | 1 | 0 | `sft_2c96fb2446` | — | `sft_2c96fb2446` |
| `competition:human_curated/666dc037-18c6-4a94-89ed-9660d66dbe7b` | 1 | 0 | `sft_8e0a0731df` | — | `sft_8e0a0731df` |
| `competition:human_curated/6759224b-638f-4f25-b797-0886893f8119` | 1 | 1 | `ask_4418f81743` | `doc_a61608d345` | `sft_4418f81743` |
| `competition:human_curated/67ceefce-1dd4-40b6-93e2-990b575eb167` | 1 | 1 | `sft_a278ea6cd7` | `doc_6b9bfe0ae9` | `sft_a278ea6cd7` |
| `competition:human_curated/67ea7883-49ab-4eae-8954-6101400b1e16` | 0 | 1 | — | `doc_564aed57dd` | `doc_564aed57dd` |
| `competition:human_curated/6826d6c2-677f-41fa-a3cb-418089fc2dc8` | 0 | 1 | — | `doc_a7af496c99` | `sft_f3b98c8a01` |
| `competition:human_curated/68e5f6c2-38c0-4f3f-977f-c4fdf3dd9b0c` | 0 | 1 | — | `doc_b1c728f21e` | `sft_775771b8cc` |
| `competition:human_curated/6924e636-bf8c-4d86-ae87-6ea119f062ca` | 0 | 1 | — | `doc_6015f406c0` | `sft_a0ccaef65c` |
| `competition:human_curated/69d495df-741c-4158-adb2-027f464040fe` | 2 | 1 | `ask_7e457560ca_q`, `sft_7e457560ca` | `doc_b4b3f5818b` | `sft_7e457560ca` |
| `competition:human_curated/6b452584-0061-4622-8401-16ced74a547e` | 0 | 1 | — | `doc_ca9ac7978a` | `doc_ca9ac7978a` |
| `competition:human_curated/6bdecdf3-4344-4442-bb53-93d5cf15f40e` | 1 | 1 | `ask_316624920f` | `doc_1bee58220a` | `sft_316624920f` |
| `competition:human_curated/6be459e7-70fd-4a72-97b2-8474cfabc5fd` | 0 | 1 | — | `doc_bdc08276b9` | `sft_ced8b9ca27` |
| `competition:human_curated/6c02e098-3cf9-4006-9537-f1d5221a928e` | 1 | 1 | `sft_8f45a7b612` | `doc_c5619f61d6` | `sft_8f45a7b612` |
| `competition:human_curated/6cfb522c-d1ca-47c6-93da-fce398c2680b` | 0 | 1 | — | `doc_9715614260` | `doc_9715614260` |
| `competition:human_curated/6e076e71-6328-4148-80ce-94ab5130c28a` | 0 | 1 | — | `doc_ab47704d04` | `sft_5b4d921e92` |
| `competition:human_curated/6e458d82-4906-4156-b7b6-1c81a65e7047` | 0 | 1 | — | `doc_a42b90c069` | `doc_a42b90c069` |
| `competition:human_curated/6ea3a95d-6b06-40c5-b654-65f86d33a0a2` | 1 | 1 | `sft_956bafd0cf` | `doc_f601d525e7` | `sft_956bafd0cf` |
| `competition:human_curated/6eb6e568-9a3b-4540-854a-ec0a8b177a25` | 0 | 1 | — | `doc_11d9c94727` | `doc_11d9c94727` |
| `competition:human_curated/6f566444-e362-4b41-8e41-1e3b4c24002c` | 0 | 1 | — | `doc_106c5be6d3` | `doc_106c5be6d3` |
| `competition:human_curated/70e6e7de-9a0c-46a2-8846-4138cdcc6f7f` | 0 | 1 | — | `doc_7c25c4bf3c` | `doc_7c25c4bf3c` |
| `competition:human_curated/70fd124e-75e5-4f34-9b92-918c7104fd97` | 0 | 1 | — | `doc_54aed2c804` | `doc_54aed2c804` |
| `competition:human_curated/7159522f-5678-4e0a-8d69-b6bab28ffc67` | 0 | 1 | — | `doc_ffa7ffb279` | `doc_ffa7ffb279` |
| `competition:human_curated/7214be71-522d-4a66-897d-9ad399eb2778` | 1 | 1 | `sft_c2a7f2e374` | `doc_b05e8d0952` | `sft_c2a7f2e374` |
| `competition:human_curated/731efdd8-88ac-4b56-ada7-d33eea98c00d` | 0 | 1 | — | `doc_aae41e353d` | `doc_aae41e353d` |
| `competition:human_curated/76ff5153-dcce-437e-93e6-9f75d48a024b` | 0 | 1 | — | `doc_83f0c691f7` | `sft_0706125fc6` |
| `competition:human_curated/7863bcb1-d1f6-4407-9ee0-714713fdbab2` | 1 | 0 | `sft_8bb4aa3ed4` | — | `sft_8bb4aa3ed4` |
| `competition:human_curated/79a4ea45-b713-4d73-9482-945cad644b5d` | 1 | 1 | `ask_54304a73b8` | `doc_7a4954e057` | `sft_54304a73b8` |
| `competition:human_curated/7a043408-0ca0-4db9-af51-51ad5ce7dfd1` | 0 | 1 | — | `doc_280e5241a6` | `doc_280e5241a6` |
| `competition:human_curated/7a359a74-7d2a-4253-8681-263e266f1342` | 0 | 1 | — | `doc_559b572c85` | `doc_559b572c85` |
| `competition:human_curated/7a61bd19-bf36-4e9b-9510-3ee9a79fe9a0` | 0 | 1 | — | `doc_60a454676d` | `doc_60a454676d` |
| `competition:human_curated/7b2a1cf0-4d0a-497c-b095-2403e8f11142` | 0 | 1 | — | `doc_8ca5f23aca` | `doc_8ca5f23aca` |
| `competition:human_curated/7b438e71-7742-4325-a5dc-b11ca2012bb4` | 0 | 1 | — | `doc_78cef24123` | `doc_78cef24123` |
| `competition:human_curated/7bd8f7e7-8c0b-4981-bbe9-8398f37a292e` | 0 | 1 | — | `doc_29bae58d99` | `sft_c71e3aa0d0` |
| `competition:human_curated/7c02d21f-45b4-4e73-b14a-f44bd83cdbc5` | 0 | 1 | — | `doc_3086e533b9` | `doc_3086e533b9` |
| `competition:human_curated/7cdc2bf2-0504-4417-8083-b6f26ba9ccab` | 1 | 1 | `sft_81d921f5b9` | `doc_fb0457ef46` | `sft_81d921f5b9` |
| `competition:human_curated/7f840c5e-0172-4c97-9a39-27f6c10dcc66` | 1 | 1 | `sft_75a1273440` | `doc_cff2752ee4` | `sft_75a1273440` |
| `competition:human_curated/804e2f09-41ad-4223-9fa7-4fc15282de79` | 3 | 0 | `ask_25ce18ae43`, `ask_25ce18ae43_q`, `sft_25ce18ae43` | — | `sft_25ce18ae43` |
| `competition:human_curated/81500329-7e7a-4bbd-b49f-e7e26f7b51fd` | 3 | 1 | `ask_fc58fd3808`, `ask_fc58fd3808_q`, `sft_fc58fd3808` | `doc_0c2137e0ea` | `sft_fc58fd3808` |
| `competition:human_curated/82b4f309-598e-43a5-a346-3a34470ce205` | 0 | 1 | — | `doc_a082e9955d` | `doc_a082e9955d` |
| `competition:human_curated/8387b6d9-2077-429e-a734-3ff81bd5a48d` | 0 | 1 | — | `doc_eb77d74b5c` | `sft_7ba3d3221e` |
| `competition:human_curated/83ab3d86-c812-4435-b304-754b79a4fa20` | 0 | 1 | — | `doc_6d811dbcf5` | `sft_d4732bf478` |
| `competition:human_curated/85c3ab39-0c58-4b1a-a54d-c68d299575e5` | 0 | 1 | — | `doc_52f5c9b37f` | `doc_52f5c9b37f` |
| `competition:human_curated/88be69b2-19db-455f-b0ef-764e8c9259ff` | 0 | 1 | — | `doc_46f5eff0c7` | `sft_5a4d0d89db` |
| `competition:human_curated/88c12033-81d7-45fd-b0f9-65864659a992` | 3 | 0 | `ask_156e6baddc`, `ask_156e6baddc_q`, `sft_156e6baddc` | — | `sft_156e6baddc` |
| `competition:human_curated/88c3a8b2-693e-4808-a770-4a28779721b6` | 0 | 1 | — | `doc_e844ffcb72` | `doc_e844ffcb72` |
| `competition:human_curated/8a748936-977c-47d0-aad2-455cbcc6ca3d` | 0 | 1 | — | `doc_6a8533cf3b` | `sft_605fd35979` |
| `competition:human_curated/8b4be1aa-c590-4397-b46c-03e9c64e8761` | 1 | 0 | `sft_5461140ee7` | — | `sft_5461140ee7` |
| `competition:human_curated/8dca0a59-d55c-455e-80a8-3e00f1b3dc69` | 0 | 1 | — | `doc_59125211dc` | `doc_59125211dc` |
| `competition:human_curated/8dea7e37-de0b-43ff-8f72-f22721e6b584` | 0 | 1 | — | `doc_60adabf6e5` | `doc_60adabf6e5` |
| `competition:human_curated/8e68ba6c-4371-4f47-9ae3-e72fdbaf443a` | 0 | 1 | — | `doc_17a6412741` | `sft_22560d9826` |
| `competition:human_curated/8ee391df-9362-4617-a446-8b18447dbee9` | 0 | 1 | — | `doc_5ba7243163` | `doc_5ba7243163` |
| `competition:human_curated/8f0af584-4b7f-4e6f-b5e4-70c9487dd206` | 0 | 1 | — | `doc_a1c4931343` | `doc_a1c4931343` |
| `competition:human_curated/90c6c75d-5a9b-4091-9efc-14dc471ab95e` | 0 | 1 | — | `doc_e1e54a51a8` | `doc_e1e54a51a8` |
| `competition:human_curated/90e3a131-9056-4a1e-a516-465ed3157f58` | 0 | 1 | — | `doc_55317034f9` | `doc_55317034f9` |
| `competition:human_curated/915947e7-d928-4b23-b234-7d8cb9e459f4` | 0 | 1 | — | `doc_0f7cae106b` | `doc_0f7cae106b` |
| `competition:human_curated/92b93490-5847-4c67-8608-aa9807cca0e2` | 0 | 1 | — | `doc_61d756316b` | `doc_61d756316b` |
| `competition:human_curated/92be8c4a-6e55-49d9-a63f-f876157055c6` | 0 | 1 | — | `doc_736b240b15` | `sft_0df0e74463` |
| `competition:human_curated/93b2187f-4109-4a83-a82e-72392eefab91` | 1 | 0 | `sft_dd83129ed5` | — | `sft_dd83129ed5` |
| `competition:human_curated/942952f2-6031-4035-b273-f969d610c37f` | 0 | 1 | — | `doc_97487bc071` | `doc_97487bc071` |
| `competition:human_curated/97f5e706-4ca9-4440-9c61-570929bbbed3` | 1 | 0 | `sft_a44a8b60a9` | — | `sft_a44a8b60a9` |
| `competition:human_curated/987bdc2e-0341-4c4a-b902-7174ffa768f4` | 0 | 1 | — | `doc_f62818d263` | `sft_84ba5d6962` |
| `competition:human_curated/98ef5185-2b7b-4744-ab2e-1498683fc65b` | 0 | 1 | — | `doc_e0733eca36` | `sft_70313ef808` |
| `competition:human_curated/99da51fd-756b-4392-85d0-8acad57005f4` | 0 | 1 | — | `doc_0a8ad2f8b6` | `sft_ee319c9bf5` |
| `competition:human_curated/9a6e4ddc-d69d-47ce-8eed-ea489960b0f1` | 0 | 1 | — | `doc_8a964a6a50` | `doc_8a964a6a50` |
| `competition:human_curated/9ba45a8c-9871-4144-93f0-4ebe6fbbed7b` | 0 | 1 | — | `doc_88ca0f96e6` | `doc_88ca0f96e6` |
| `competition:human_curated/9cac8aa3-5793-4fd7-86fc-2e183c7bbbe2` | 0 | 1 | — | `doc_7888068567` | `doc_7888068567` |
| `competition:human_curated/9d080388-6e6e-4509-8e37-e30007b970b0` | 0 | 1 | — | `doc_ad7a453dc1` | `doc_ad7a453dc1` |
| `competition:human_curated/9d2d82f3-9357-4477-9710-bb04c37f5fa0` | 1 | 1 | `sft_520f5c808e` | `doc_36c243dde3` | `sft_520f5c808e` |
| `competition:human_curated/9e2da221-91d3-45fa-8754-9d290c246504` | 0 | 1 | — | `doc_0436bb61e8` | `sft_a19628bcbf` |
| `competition:human_curated/9e3329a2-7814-4ba6-94bc-340dd8a915da` | 0 | 1 | — | `doc_1aa5295325` | `doc_1aa5295325` |
| `competition:human_curated/9eb04fc2-01d0-418f-af16-c0d5598aadd2` | 1 | 0 | `sft_7fbcf76afb` | — | `sft_7fbcf76afb` |
| `competition:human_curated/9ef86a91-6852-4bd7-b86c-d6d53c92842e` | 0 | 1 | — | `doc_32a0ff4128` | `doc_32a0ff4128` |
| `competition:human_curated/a0fb0db2-1b50-4fd7-b104-e6c4082c8627` | 0 | 1 | — | `doc_fb0609f169` | `sft_5488c6e68c` |
| `competition:human_curated/a177d9ca-47d0-49ec-8195-e254f14e67b9` | 2 | 1 | `ask_858707b07e`, `sft_858707b07e` | `doc_2ee33857de` | `sft_858707b07e` |
| `competition:human_curated/a1855fc0-5cbf-4f6a-8ad0-3a078fc3a6c7` | 0 | 1 | — | `doc_bd26374a28` | `sft_0a07bca8d3` |
| `competition:human_curated/a252e7f9-b944-4d23-9921-87177e91e7be` | 1 | 1 | `sft_2cb682a4c1` | `doc_543d73a66a` | `sft_2cb682a4c1` |
| `competition:human_curated/a28b16ad-392a-4083-aa10-f158d7c6b5c7` | 0 | 1 | — | `doc_31b05f4173` | `doc_31b05f4173` |
| `competition:human_curated/a28e28b8-0e90-470d-b109-5307dfe2647d` | 0 | 1 | — | `doc_228652d3bb` | `doc_228652d3bb` |
| `competition:human_curated/a307d240-4a22-4075-9225-a52c35958d3a` | 0 | 1 | — | `doc_4aea7ab787` | `doc_4aea7ab787` |
| `competition:human_curated/a32b67a0-0d31-42d3-8970-5160c8fd36ac` | 0 | 1 | — | `doc_c5c4b4e288` | `sft_52ae222e14` |
| `competition:human_curated/a4cb2dc7-da2d-47a1-a3a3-ad8a03aab4aa` | 0 | 1 | — | `doc_34a8e6b409` | `doc_34a8e6b409` |
| `competition:human_curated/a5df6a7f-29ec-4dc6-a041-20d27fc12942` | 1 | 1 | `sft_d219717356` | `doc_3c0383a7de` | `sft_d219717356` |
| `competition:human_curated/a5ec3a99-36a0-430c-930c-772d933cbaca` | 0 | 1 | — | `doc_44ce6d602c` | `doc_44ce6d602c` |
| `competition:human_curated/a6199ff0-477f-40f2-8219-b343c987541e` | 0 | 1 | — | `doc_5a7379c7d3` | `doc_5a7379c7d3` |
| `competition:human_curated/a75e49ee-8899-4035-9c1f-24cbe7bdd77d` | 0 | 1 | — | `doc_798e242d6b` | `doc_798e242d6b` |
| `competition:human_curated/a799fc8d-7591-45de-ab51-04113397e3ce` | 0 | 1 | — | `doc_404d4a7a8f` | `doc_404d4a7a8f` |
| `competition:human_curated/a79f0e93-9474-46f2-bab5-459864e05c8b` | 0 | 1 | — | `doc_faaf50fbee` | `doc_faaf50fbee` |
| `competition:human_curated/a7b2a1ff-90ad-4cd5-80ad-def75463056a` | 0 | 1 | — | `doc_114b4d76d9` | `doc_114b4d76d9` |
| `competition:human_curated/a84f4a69-a285-47d0-9912-0876f36997f5` | 1 | 0 | `sft_2919540ebd` | — | `sft_2919540ebd` |
| `competition:human_curated/a8f62160-3218-4c33-957e-2e6e25ffa5ff` | 1 | 0 | `sft_afe39ee5ed` | — | `sft_afe39ee5ed` |
| `competition:human_curated/ac083223-b269-4f5d-9f75-c332e20a3716` | 0 | 1 | — | `doc_3bd6341118` | `sft_1c26274967` |
| `competition:human_curated/ac7047dd-3b58-4402-9c91-b0f40561df64` | 0 | 1 | — | `doc_104142d0d2` | `doc_104142d0d2` |
| `competition:human_curated/ad85a868-c33d-48d6-8385-f1f2be9ecbcf` | 0 | 1 | — | `doc_0c9944e3a4` | `sft_d0735ce5a2` |
| `competition:human_curated/adc4e444-f783-4671-bd89-4ce654488ea8` | 0 | 1 | — | `doc_c21a0b6763` | `doc_c21a0b6763` |
| `competition:human_curated/adf2fed4-720e-4d3a-adeb-5f859abf9b4b` | 1 | 1 | `sft_401aaff536` | `doc_d541307ed7` | `sft_401aaff536` |
| `competition:human_curated/ae174f1d-734a-45c5-afd3-ae126bfa1382` | 0 | 1 | — | `doc_bb9896313f` | `sft_ccbb5e518d` |
| `competition:human_curated/ae31f470-d15e-46b2-8a93-2cb9f9e1e86a` | 0 | 1 | — | `doc_b88a950ada` | `doc_b88a950ada` |
| `competition:human_curated/ae37021f-06c8-4fff-9bb1-44c28a4f1690` | 0 | 1 | — | `doc_e2822c1224` | `doc_e2822c1224` |
| `competition:human_curated/af90212c-bcb6-499a-b6b8-e03967e234dc` | 0 | 1 | — | `doc_d0156bf274` | `doc_d0156bf274` |
| `competition:human_curated/afa9bb86-32df-4b64-b921-8374af346d7d` | 0 | 1 | — | `doc_0187f1d9e9` | `sft_52ed3b8006` |
| `competition:human_curated/b0737cd4-ab47-4a3f-a00c-aa0774ce04d9` | 0 | 1 | — | `doc_af9159b624` | `doc_af9159b624` |
| `competition:human_curated/b1d2af36-ad21-4e4d-9bb9-249f776b1498` | 0 | 1 | — | `doc_e5a0b633d7` | `doc_e5a0b633d7` |
| `competition:human_curated/b1d33994-efc6-4af2-85f9-3612aa8a19c2` | 0 | 1 | — | `doc_62b27672cd` | `doc_62b27672cd` |
| `competition:human_curated/b3c2de20-dca7-4dfc-a363-8bfffd4e1b02` | 0 | 1 | — | `doc_a2b4dde96f` | `doc_a2b4dde96f` |
| `competition:human_curated/b5ee063c-4eca-45c5-a943-22f84bb96be4` | 0 | 1 | — | `doc_a10e356a6e` | `doc_a10e356a6e` |
| `competition:human_curated/b7d2a690-87c0-4331-a896-fcd8ad3bf655` | 0 | 1 | — | `doc_6f21b92660` | `doc_6f21b92660` |
| `competition:human_curated/b7ff1777-11bd-4eb6-9e9c-27346e82953b` | 0 | 1 | — | `doc_360c2bbfe2` | `doc_360c2bbfe2` |
| `competition:human_curated/b8381695-0445-4a94-94f2-e569cc3bb9ad` | 0 | 1 | — | `doc_c4eae91b02` | `doc_c4eae91b02` |
| `competition:human_curated/b95ef9de-32b3-4ed0-8e07-8c2e6898c217` | 0 | 1 | — | `doc_3fd3fa972e` | `sft_6d6f0a2154` |
| `competition:human_curated/ba7899bb-cc63-49d7-813c-8ebe2183073d` | 0 | 1 | — | `doc_24ed62c141` | `doc_24ed62c141` |
| `competition:human_curated/bbd6e1c3-372e-4a69-bc77-607473af65bb` | 0 | 1 | — | `doc_8b1561bd21` | `doc_8b1561bd21` |
| `competition:human_curated/bd19cd67-b36c-453c-a8fb-8774a9bbab13` | 2 | 1 | `ask_ae3ef421a7`, `ask_ae3ef421a7_q` | `doc_09f7745ca5` | `sft_ae3ef421a7` |
| `competition:human_curated/bd56e14a-7610-40f1-b05c-694fd668024b` | 0 | 1 | — | `doc_f7aea1436f` | `sft_cba0ac347d` |
| `competition:human_curated/bddfe148-6bf0-46e7-97a7-24e7290cd80c` | 0 | 1 | — | `doc_be0c156fad` | `doc_be0c156fad` |
| `competition:human_curated/be59be1e-eb10-4cf7-86ae-d5721ba31b96` | 0 | 1 | — | `doc_13988e3b7d` | `doc_13988e3b7d` |
| `competition:human_curated/bea775a9-72f3-4a12-9894-546602e1d8ef` | 0 | 1 | — | `doc_6e864e700a` | `sft_9a28331711` |
| `competition:human_curated/bec9c45e-ef62-4f29-8b41-8ba8dae0f195` | 0 | 1 | — | `doc_cbf906be1c` | `doc_cbf906be1c` |
| `competition:human_curated/bf4703f2-5af7-47a1-8010-4729ab883827` | 0 | 1 | — | `doc_8ea855e0e7` | `doc_8ea855e0e7` |
| `competition:human_curated/bfd43bfa-bf21-4c13-873d-12ef2e2a79ee` | 0 | 1 | — | `doc_9f6b982244` | `doc_9f6b982244` |
| `competition:human_curated/c1db2db7-c018-46e1-928c-4a242343922b` | 0 | 1 | — | `doc_e19049f74e` | `doc_e19049f74e` |
| `competition:human_curated/c30c281e-808f-48d0-92d7-76badf8eedd6` | 0 | 1 | — | `doc_6c45f4c92d` | `sft_5fd59f19a5` |
| `competition:human_curated/c35fdf69-0197-4227-b57e-bda5c55e728e` | 1 | 1 | `sft_a72be6a056` | `doc_db7ff6aa52` | `sft_a72be6a056` |
| `competition:human_curated/c3650278-83cd-4672-9201-6c613e555094` | 0 | 1 | — | `doc_8f575251be` | `doc_8f575251be` |
| `competition:human_curated/c3cc4a2f-20af-4f1b-bd07-5f8b710e3667` | 0 | 1 | — | `doc_3292c44441` | `doc_3292c44441` |
| `competition:human_curated/c3e0ebfd-0916-4c23-932a-73979f8ed697` | 0 | 1 | — | `doc_167edf1e1c` | `doc_167edf1e1c` |
| `competition:human_curated/c47742cd-7fff-4465-a081-4b5e0d72b5bf` | 1 | 1 | `sft_55a3daa735` | `doc_c6607a852c` | `sft_55a3daa735` |
| `competition:human_curated/c4a20272-980f-43f7-8f4a-a1772f029626` | 0 | 1 | — | `doc_86ab29cb18` | `sft_18f943cce0` |
| `competition:human_curated/c5b1cd5b-8e40-45ca-bf72-9143e58ef39f` | 0 | 1 | — | `doc_e31a8c1129` | `sft_b4ed98e8a8` |
| `competition:human_curated/c609ef4c-6357-4282-86c7-4a9136f430ff` | 0 | 1 | — | `doc_744196eb32` | `doc_744196eb32` |
| `competition:human_curated/c7ed7a79-2358-4f7a-b339-9d0513c28f41` | 0 | 1 | — | `doc_896059e21d` | `doc_896059e21d` |
| `competition:human_curated/c806e8c4-1ec5-4c04-b98d-54b8112c975c` | 0 | 1 | — | `doc_c67b3e43b7` | `sft_443cff84c8` |
| `competition:human_curated/c89731be-ecf0-4ad0-a0db-f0b0ff60d405` | 1 | 1 | `sft_f1881961d2` | `doc_263f8d02e8` | `sft_f1881961d2` |
| `competition:human_curated/c8b4520c-53c2-4957-9976-7eff6e795936` | 0 | 1 | — | `doc_3121621d5a` | `doc_3121621d5a` |
| `competition:human_curated/c9f835a0-74aa-4835-b567-51601cd6f42c` | 0 | 1 | — | `doc_6590ae5dbb` | `doc_6590ae5dbb` |
| `competition:human_curated/ca974962-0f92-44c0-beb8-79b4f21e7f77` | 1 | 0 | `sft_0d89311f8a` | — | `sft_0d89311f8a` |
| `competition:human_curated/cb9fedeb-324a-43da-9bc3-dab8e243ea74` | 0 | 1 | — | `doc_a5c425aaf1` | `doc_a5c425aaf1` |
| `competition:human_curated/cc8999d4-6732-46dd-af8c-06493d735789` | 2 | 0 | `ask_b3f2f7eed4_q`, `sft_b3f2f7eed4` | — | `sft_b3f2f7eed4` |
| `competition:human_curated/ce2d692d-4d69-4d98-a2dc-bb6d02cac44f` | 0 | 1 | — | `doc_43d22359fa` | `doc_43d22359fa` |
| `competition:human_curated/cf949a6e-999c-4e0c-a1dc-d8f897deb3bc` | 1 | 0 | `sft_6880ade8aa` | — | `sft_6880ade8aa` |
| `competition:human_curated/d0ace9c8-f3fd-4c44-9619-d78606aa03c9` | 0 | 1 | — | `doc_25d02be069` | `doc_25d02be069` |
| `competition:human_curated/d26768fc-1488-4ad1-9c84-962939b147a6` | 1 | 0 | `sft_e48dbafcd2` | — | `sft_e48dbafcd2` |
| `competition:human_curated/d2e75724-0e71-4f2a-8cfb-6b975cfdee6a` | 1 | 0 | `sft_0eea60f5e6` | — | `sft_0eea60f5e6` |
| `competition:human_curated/d388c2e2-3c75-4f85-a8c9-c9854a718c2b` | 0 | 1 | — | `doc_d5158da29d` | `sft_58cf1ee6d2` |
| `competition:human_curated/d3fc13e5-2b72-410f-b1b2-aaa20387d7e8` | 0 | 1 | — | `doc_1c1c702338` | `doc_1c1c702338` |
| `competition:human_curated/d4a6c056-7bfd-4827-832e-5ffa65828b1f` | 0 | 1 | — | `doc_aa0fe18239` | `doc_aa0fe18239` |
| `competition:human_curated/d60b55fc-9c9e-4855-8786-ca7f9648f51f` | 1 | 0 | `sft_91aa723a82` | — | `sft_91aa723a82` |
| `competition:human_curated/d87f9ae0-19cd-45a1-b942-b044293d5343` | 1 | 0 | `sft_86c6f68901` | — | `sft_86c6f68901` |
| `competition:human_curated/d9c77524-322a-4d38-b9a0-970b706adeb4` | 0 | 1 | — | `doc_4bc3a69fb0` | `doc_4bc3a69fb0` |
| `competition:human_curated/daa6d887-43ba-4b61-99c4-af80e1d15179` | 0 | 1 | — | `doc_aaa5714d60` | `sft_1d1271b647` |
| `competition:human_curated/daffc8c2-0980-47bf-9d44-7db79004d531` | 0 | 1 | — | `doc_0ba2c2aedf` | `sft_d040dfce87` |
| `competition:human_curated/db1a3a79-c440-4b73-a96e-a69b065d7686` | 1 | 1 | `ask_dc751e830c` | `doc_22c0b0712e` | `sft_dc751e830c` |
| `competition:human_curated/dc66d004-49ea-48ee-a5b9-f61de15599d7` | 0 | 1 | — | `doc_ba7249784a` | `doc_ba7249784a` |
| `competition:human_curated/dc96b865-5e27-4613-b7f7-037ec35ecd32` | 0 | 1 | — | `doc_e8c8393472` | `doc_e8c8393472` |
| `competition:human_curated/dce755d9-df27-4fb3-8245-eb060166b429` | 0 | 1 | — | `doc_0389ed3110` | `doc_0389ed3110` |
| `competition:human_curated/dd08c58b-712c-4b00-b284-b13600e6fa62` | 0 | 1 | — | `doc_414c693aa3` | `sft_fa7bcbf7aa` |
| `competition:human_curated/dd8ed58c-6c62-4136-8019-44a405b8ece8` | 0 | 1 | — | `doc_8bc9984f5b` | `doc_8bc9984f5b` |
| `competition:human_curated/dd951624-27bc-41dd-84d0-1a6046836b5b` | 0 | 1 | — | `doc_7d3f8133f6` | `sft_cadc2040b7` |
| `competition:human_curated/de75c16c-7437-45f5-82fc-9af0361098c2` | 0 | 1 | — | `doc_dc1b47c211` | `doc_dc1b47c211` |
| `competition:human_curated/df3c0930-030d-498d-884a-5386f4f1e584` | 1 | 1 | `sft_8178c780af` | `doc_71425a86f3` | `sft_8178c780af` |
| `competition:human_curated/e18d036f-edec-4873-b040-f2832622fd53` | 0 | 1 | — | `doc_b26141b24b` | `doc_b26141b24b` |
| `competition:human_curated/e2674f9a-be42-49d2-8103-b58fdffe8fb8` | 0 | 1 | — | `doc_dfda069d0c` | `sft_b41a8438d9` |
| `competition:human_curated/e3bf4eb2-0e1c-4713-a056-02d012f6dd23` | 0 | 1 | — | `doc_dbeaec220b` | `doc_dbeaec220b` |
| `competition:human_curated/e4f50d55-885c-45ab-a16c-763bb51abd01` | 1 | 0 | `sft_6bf4dbb224` | — | `sft_6bf4dbb224` |
| `competition:human_curated/e59ff456-24f4-4967-9a7b-a9a3afa88698` | 0 | 1 | — | `doc_52a80d0b19` | `sft_51220cc76b` |
| `competition:human_curated/e78f53eb-4eec-4a32-af08-8cf88e24ace1` | 0 | 1 | — | `doc_fe75793609` | `doc_fe75793609` |
| `competition:human_curated/e7940113-2a30-42e4-bba3-e55f2e7ffbe8` | 1 | 1 | `sft_450a39809c` | `doc_0acc49e128` | `sft_450a39809c` |
| `competition:human_curated/e7adffe7-94bc-4805-bd6f-053497fb119b` | 0 | 1 | — | `doc_fca4afc0f1` | `doc_fca4afc0f1` |
| `competition:human_curated/e7d4cc16-d41c-442b-9b46-3ad743d9c2fc` | 0 | 1 | — | `doc_5452b07e57` | `doc_5452b07e57` |
| `competition:human_curated/e83c20ae-f19b-4d06-9d89-4ac4173fc1f3` | 1 | 1 | `ask_cf8bab21b5` | `doc_f9d5295f33` | `sft_cf8bab21b5` |
| `competition:human_curated/e875a3dc-7381-4299-8c1c-94b48ef04e31` | 0 | 1 | — | `doc_0adc35e0c2` | `doc_0adc35e0c2` |
| `competition:human_curated/e98e290b-6c13-454c-8f91-d0a48839dbec` | 0 | 1 | — | `doc_b3148629d0` | `doc_b3148629d0` |
| `competition:human_curated/eabd5fa6-a59e-44f3-b46f-004e9bda3197` | 0 | 1 | — | `doc_57a550ee9b` | `doc_57a550ee9b` |
| `competition:human_curated/eb815366-6e07-4b0f-8994-70498df5e19a` | 0 | 1 | — | `doc_6d764cb36f` | `doc_6d764cb36f` |
| `competition:human_curated/ed0e6267-e9ab-4c83-bf6f-28ba94236076` | 1 | 1 | `sft_b4068573aa` | `doc_8d7aa09550` | `sft_b4068573aa` |
| `competition:human_curated/ee8ce5fc-7205-444b-9509-87180b04db9d` | 0 | 1 | — | `doc_9f1619780e` | `sft_538dc08824` |
| `competition:human_curated/ee91b237-f555-4c59-89c5-580cfa5532e5` | 0 | 1 | — | `doc_ad26bc6c92` | `sft_ec872d9414` |
| `competition:human_curated/f20c0893-d399-4bb4-8969-80823e501a7b` | 2 | 0 | `ask_e10356d6f0`, `ask_e10356d6f0_q` | — | `sft_e10356d6f0` |
| `competition:human_curated/f2baa25d-470c-4f89-8cf6-ab981a7c92c4` | 0 | 1 | — | `doc_fa33d99dc7` | `doc_fa33d99dc7` |
| `competition:human_curated/f3c575ab-7325-4a44-a5ef-31932e8378b1` | 0 | 1 | — | `doc_5c6b3638cf` | `doc_5c6b3638cf` |
| `competition:human_curated/f6647162-825c-4400-a6db-ece748073628` | 0 | 1 | — | `doc_3cc1db3891` | `doc_3cc1db3891` |
| `competition:human_curated/f8352d66-d6ff-4157-a343-a15bdd1c2a94` | 0 | 1 | — | `doc_b48d67a987` | `doc_b48d67a987` |
| `competition:human_curated/f8c0dce2-6693-4622-8ad6-c0ecc80d8031` | 1 | 1 | `sft_57b99daa68` | `doc_0e09ff9c22` | `sft_57b99daa68` |
| `competition:human_curated/f8cf5f19-9d8d-44ad-88fd-ed413e6d58ab` | 0 | 1 | — | `doc_4b0425c0e2` | `doc_4b0425c0e2` |
| `competition:human_curated/f949ba8e-4cf7-421c-bdd0-ec1e63063baa` | 1 | 1 | `sft_8fc1ac5e75` | `doc_373d1900ef` | `sft_8fc1ac5e75` |
| `competition:human_curated/f9acca3d-2e3b-40c5-8789-9d8391ccb8b7` | 1 | 0 | `sft_9b43392dde` | — | `sft_9b43392dde` |
| `competition:human_curated/fa14d320-6926-4bb2-b4ce-19fe9bdc2dfd` | 0 | 1 | — | `doc_367ddd916c` | `doc_367ddd916c` |
| `competition:human_curated/fc5f79e9-7c8a-43c4-822a-9d6ea6cb35e5` | 0 | 1 | — | `doc_a3bc7913bb` | `doc_a3bc7913bb` |
| `competition:human_curated/fd1b96d8-5038-4cb9-8179-8a1b0a89c402` | 0 | 1 | — | `doc_9baeb92242` | `doc_9baeb92242` |
| `competition:human_curated/fe1bf07f-de31-477c-89d4-e2660b862057` | 1 | 1 | `sft_a4a1e55b42` | `doc_6bb2902cfa` | `sft_a4a1e55b42` |
| `competition:human_curated/fe3b1914-a973-4921-b4bf-a16c75c3fe1e` | 0 | 1 | — | `doc_b6f10ea4e9` | `doc_b6f10ea4e9` |
| `competition:human_curated/fe6eeff7-47ff-4059-8b15-aaab9597d89e` | 0 | 1 | — | `doc_82552ed4ba` | `doc_82552ed4ba` |
| `competition:human_curated/ffa9a748-0bb3-4640-84e2-3a7dbca528d3` | 1 | 0 | `sft_4af2c5fb8b` | — | `sft_4af2c5fb8b` |
| `competition:synthetic/139b0ae3-41ba-4761-9645-1cf65f8c877f` | 0 | 1 | — | `doc_06d2525f69` | `sft_0f11cd48e9` |
| `competition:synthetic/16975984-30b7-4feb-9791-ef5b3f0770e6` | 0 | 1 | — | `doc_7bbbc27c53` | `sft_fca5bc5726` |
| `competition:synthetic/2b1fd90c-29e1-4b15-a3d1-71e61a8e969f` | 0 | 1 | — | `doc_d17b3d9647` | `sft_b0a45f25ca` |
| `competition:synthetic/3184b278-9555-4d16-8b14-e1b4c97d774d` | 0 | 1 | — | `doc_be26cb6c90` | `doc_be26cb6c90` |
| `competition:synthetic/3a3f6a9c-1315-4b26-a93d-585800c38217` | 1 | 0 | `sft_ef681f08d0` | — | `sft_ef681f08d0` |
| `competition:synthetic/3febb387-5a58-401d-99e7-185930f78d88` | 1 | 1 | `sft_0dd785a26e` | `doc_8cd4586dc4` | `sft_0dd785a26e` |
| `competition:synthetic/4003b8ff-7b71-40c8-95c8-85c665160af4` | 1 | 0 | `sft_c90cc31f92` | — | `sft_c90cc31f92` |
| `competition:synthetic/532a34f8-9d24-498b-b23f-ac8a342d739a` | 0 | 1 | — | `doc_9b491048c3` | `doc_9b491048c3` |
| `competition:synthetic/61f0e2e7-14d8-400d-aa20-87ce6ab2104e` | 1 | 0 | `sft_4857000fb6` | — | `sft_4857000fb6` |
| `competition:synthetic/63c6ec7b-7776-4f9a-9fcd-50d8b67e17bf` | 0 | 1 | — | `doc_aaa9c352f6` | `doc_aaa9c352f6` |
| `competition:synthetic/64db6b66-6a66-4470-a1f9-7547f136e98a` | 0 | 1 | — | `doc_64cb163f55` | `doc_64cb163f55` |
| `competition:synthetic/7538f9e8-d206-40de-bce5-90601a23c53b` | 0 | 1 | — | `doc_92ec1507af` | `doc_92ec1507af` |
| `competition:synthetic/79153efb-4111-4faa-929b-f3e547456ce5` | 0 | 1 | — | `doc_271a6581c4` | `doc_271a6581c4` |
| `competition:synthetic/9346c968-4748-4a22-b4dc-fcdc0646849f` | 0 | 1 | — | `doc_55674f8773` | `doc_55674f8773` |
| `competition:synthetic/99df53fc-08c8-447b-a24b-ae77862add8d` | 0 | 1 | — | `doc_5ead3bb71f` | `doc_5ead3bb71f` |
| `competition:synthetic/a6ce6d81-1054-4b0e-b033-ea4fec9b0486` | 0 | 1 | — | `doc_23ba028fe8` | `doc_23ba028fe8` |
| `competition:synthetic/a9b2f7f5-c864-452b-b386-fe63df0b4fa4` | 1 | 0 | `sft_ac8f39219e` | — | `sft_ac8f39219e` |
| `competition:synthetic/c5c60f80-d9a5-4dec-84e9-ecac35ef46ea` | 0 | 1 | — | `doc_673cf2f2a8` | `doc_673cf2f2a8` |
| `competition:synthetic/cde81892-1b11-440c-aa5b-6c845bff1013` | 1 | 1 | `sft_21e815b58a` | `doc_11f329a998` | `sft_21e815b58a` |
| `competition:synthetic/d88f0db1-658c-4e7c-b6ef-e30a78c5f314` | 0 | 1 | — | `doc_aaff96176b` | `sft_476df3e367` |
| `competition:synthetic/da299436-5e1f-45da-bbc9-d32444108d8e` | 0 | 1 | — | `doc_26ef433927` | `sft_5835f1530f` |
| `competition:synthetic/e7cc4724-7dd6-4de2-adb1-463058262202` | 1 | 1 | `sft_cef5a28fb4` | `doc_51ac458cd2` | `sft_cef5a28fb4` |
| `competition:synthetic/ec3645ff-8439-49f5-af88-ec2f6bc70aaa` | 0 | 1 | — | `doc_be76574187` | `doc_be76574187` |
| `competition:synthetic/ed62f5d9-7e35-4987-8c24-8d08852d7dd9` | 0 | 1 | — | `doc_c31f780d2d` | `doc_c31f780d2d` |
| `competition:synthetic/fce1ebc6-1d4c-4c14-8cb0-ddf59adae3d8` | 1 | 0 | `sft_b5d497822c` | — | `sft_b5d497822c` |
| `hyperstition:hyperstition/blood-across-the-border-canal` | 0 | 1 | — | `doc_7c19812084` | `doc_7c19812084` |
| `hyperstition:hyperstition/blood-and-bronze-badge` | 0 | 1 | — | `doc_d02cd20f9e` | `doc_d02cd20f9e` |
| `hyperstition:hyperstition/border-flames` | 0 | 1 | — | `doc_1e9d6d8db1` | `doc_1e9d6d8db1` |
| `hyperstition:hyperstition/breaking-through-the-spotlight` | 0 | 1 | — | `doc_3ee0f92873` | `doc_3ee0f92873` |
| `hyperstition:hyperstition/chrome-hearts-and-open-roads` | 0 | 1 | — | `doc_d1db0dc64e` | `doc_d1db0dc64e` |
| `hyperstition:hyperstition/depths-of-the-heart` | 0 | 1 | — | `doc_0955bcf159` | `doc_0955bcf159` |
| `hyperstition:hyperstition/depths-of-the-titan-reef` | 0 | 1 | — | `doc_645041ec3a` | `doc_645041ec3a` |
| `hyperstition:hyperstition/devils-chord` | 0 | 1 | — | `doc_e24c8be418` | `doc_e24c8be418` |
| `hyperstition:hyperstition/dreams-of-the-tower-room` | 0 | 1 | — | `doc_df9ae06684` | `doc_df9ae06684` |
| `hyperstition:hyperstition/fields-of-digital-peace` | 0 | 1 | — | `doc_2ac34e8a55` | `doc_2ac34e8a55` |
| `hyperstition:hyperstition/glass-houses-in-the-quarter` | 0 | 1 | — | `doc_969960f5c7` | `doc_969960f5c7` |
| `hyperstition:hyperstition/hanging-by-a-thread` | 0 | 1 | — | `doc_bfd3252a02` | `doc_bfd3252a02` |
| `hyperstition:hyperstition/hearts-and-highlands-rising` | 0 | 1 | — | `doc_1a4d53664e` | `doc_1a4d53664e` |
| `hyperstition:hyperstition/hearts-in-the-barrio` | 0 | 1 | — | `doc_266d7c0ecb` | `doc_266d7c0ecb` |
| `hyperstition:hyperstition/hearts-in-the-wasteland` | 0 | 1 | — | `doc_0c94d40a41` | `doc_0c94d40a41` |
| `hyperstition:hyperstition/hearts-on-the-frontier` | 0 | 1 | — | `doc_daedff1e11` | `doc_daedff1e11` |
| `hyperstition:hyperstition/hearts-under-fire` | 0 | 1 | — | `doc_719a888f10` | `doc_719a888f10` |
| `hyperstition:hyperstition/learning-to-love` | 0 | 1 | — | `doc_9b8d5609e1` | `doc_9b8d5609e1` |
| `hyperstition:hyperstition/letters-from-the-broken-frontier` | 0 | 1 | — | `doc_f7a982d271` | `doc_f7a982d271` |
| `hyperstition:hyperstition/letters-in-the-digital-dark` | 0 | 1 | — | `doc_a8f7f2274b` | `doc_a8f7f2274b` |
| `hyperstition:hyperstition/life-is-a-banquet` | 0 | 1 | — | `doc_00677397d7` | `doc_00677397d7` |
| `hyperstition:hyperstition/lord-of-the-floating-isles` | 0 | 1 | — | `doc_02bfd843f7` | `doc_02bfd843f7` |
| `hyperstition:hyperstition/mountain-born-valley-raised` | 0 | 1 | — | `doc_9c6857aa1d` | `doc_9c6857aa1d` |
| `hyperstition:hyperstition/party-lines-and-digital-whispers` | 0 | 1 | — | `doc_8c95ea20a8` | `doc_8c95ea20a8` |
| `hyperstition:hyperstition/prince-of-two-worlds` | 0 | 1 | — | `doc_ff5f2d8941` | `doc_ff5f2d8941` |
| `hyperstition:hyperstition/racing-the-sky-for-love` | 0 | 1 | — | `doc_233df1415c` | `doc_233df1415c` |
| `hyperstition:hyperstition/rails-of-the-heart` | 0 | 1 | — | `doc_b71eb4f6d9` | `doc_b71eb4f6d9` |
| `hyperstition:hyperstition/rewriting-the-hearts-canon` | 0 | 1 | — | `doc_3b9da0f317` | `doc_3b9da0f317` |
| `hyperstition:hyperstition/seeds-in-silicon-prairie` | 0 | 1 | — | `doc_b537845d7b` | `doc_b537845d7b` |
| `hyperstition:hyperstition/steel-hearts-and-wild-souls` | 0 | 1 | — | `doc_3a15728d93` | `doc_3a15728d93` |
| `hyperstition:hyperstition/storm-and-harbor` | 0 | 1 | — | `doc_49a68ffda9` | `doc_49a68ffda9` |
| `hyperstition:hyperstition/the-abundance-wars` | 0 | 1 | — | `doc_6891a23315` | `doc_6891a23315` |
| `hyperstition:hyperstition/the-amber-summer-of-tommy-chen` | 0 | 1 | — | `doc_c419b57602` | `doc_c419b57602` |
| `hyperstition:hyperstition/the-ant-hill-gambit` | 0 | 1 | — | `doc_2ebfe5c95d` | `doc_2ebfe5c95d` |
| `hyperstition:hyperstition/the-binding-court` | 0 | 1 | — | `doc_ee25acf95a` | `doc_ee25acf95a` |
| `hyperstition:hyperstition/the-boys-of-rivermouth` | 0 | 1 | — | `doc_9d53aa5783` | `doc_9d53aa5783` |
| `hyperstition:hyperstition/the-burden-of-silence` | 0 | 1 | — | `doc_4c9b20d03f` | `doc_4c9b20d03f` |
| `hyperstition:hyperstition/the-carpathian-configuration` | 0 | 1 | — | `doc_9c42ca32be` | `doc_9c42ca32be` |
| `hyperstition:hyperstition/the-cats-new-game` | 0 | 1 | — | `doc_ddec1d4390` | `doc_ddec1d4390` |
| `hyperstition:hyperstition/the-cold-that-saves` | 0 | 1 | — | `doc_59c535365c` | `doc_59c535365c` |
| `hyperstition:hyperstition/the-color-of-sound` | 0 | 1 | — | `doc_eda2b74fcd` | `doc_eda2b74fcd` |
| `hyperstition:hyperstition/the-convents-last-dispensation` | 0 | 1 | — | `doc_d9a15e7e34` | `doc_d9a15e7e34` |
| `hyperstition:hyperstition/the-crowns-deception` | 0 | 1 | — | `doc_a2cfb63c16` | `doc_a2cfb63c16` |
| `hyperstition:hyperstition/the-depths-we-keep` | 0 | 1 | — | `doc_809a4cda62` | `doc_809a4cda62` |
| `hyperstition:hyperstition/the-descent-absolute` | 0 | 1 | — | `doc_a4ff67bee6` | `doc_a4ff67bee6` |
| `hyperstition:hyperstition/the-distance-between-worlds` | 0 | 1 | — | `doc_0d2a997c2b` | `doc_0d2a997c2b` |
| `hyperstition:hyperstition/the-drowning-pool` | 0 | 1 | — | `doc_70e2d7cb1f` | `doc_70e2d7cb1f` |
| `hyperstition:hyperstition/the-dutch-boys-american-nightmare` | 0 | 1 | — | `doc_6d4603213a` | `doc_6d4603213a` |
| `hyperstition:hyperstition/the-echoing-chambers-of-montgomery-place` | 0 | 1 | — | `doc_4909f35f52` | `doc_4909f35f52` |
| `hyperstition:hyperstition/the-empire-state-of-grace` | 0 | 1 | — | `doc_bddc8ce751` | `doc_bddc8ce751` |
| `hyperstition:hyperstition/the-empty-shore` | 0 | 1 | — | `doc_f754cad0ed` | `doc_f754cad0ed` |
| `hyperstition:hyperstition/the-fabric-of-tomorrow` | 0 | 1 | — | `doc_42612cd104` | `doc_42612cd104` |
| `hyperstition:hyperstition/the-fences-we-build` | 0 | 1 | — | `doc_d08fdbec27` | `doc_d08fdbec27` |
| `hyperstition:hyperstition/the-fever-dreams-of-marcus-kane` | 0 | 1 | — | `doc_51fc50e478` | `doc_51fc50e478` |
| `hyperstition:hyperstition/the-garden-we-leave-behind` | 0 | 1 | — | `doc_670aaa5664` | `doc_670aaa5664` |
| `hyperstition:hyperstition/the-gemini-parish-job` | 0 | 1 | — | `doc_b717172cce` | `doc_b717172cce` |
| `hyperstition:hyperstition/the-generals-last-run` | 0 | 1 | — | `doc_cdbef8952f` | `doc_cdbef8952f` |
| `hyperstition:hyperstition/the-gilded-room-mystery` | 0 | 1 | — | `doc_4815c1f892` | `doc_4815c1f892` |
| `hyperstition:hyperstition/the-golden-cage-of-house-valdris` | 0 | 1 | — | `doc_d401b0affa` | `doc_d401b0affa` |
| `hyperstition:hyperstition/the-golden-cipher` | 0 | 1 | — | `doc_79b04daa68` | `doc_79b04daa68` |
| `hyperstition:hyperstition/the-golden-claw-cipher` | 0 | 1 | — | `doc_856394007f` | `doc_856394007f` |
| `hyperstition:hyperstition/the-golden-network` | 0 | 1 | — | `doc_15daa675a5` | `doc_15daa675a5` |
| `hyperstition:hyperstition/the-grayson-protocol` | 0 | 1 | — | `doc_c61a6fe3b6` | `doc_c61a6fe3b6` |
| `hyperstition:hyperstition/the-handmaidens-legacy` | 0 | 1 | — | `doc_f9c20e8611` | `doc_f9c20e8611` |
| `hyperstition:hyperstition/the-harmony-academy` | 0 | 1 | — | `doc_96e623d2db` | `doc_96e623d2db` |
| `hyperstition:hyperstition/the-headless-rider-of-titan-station` | 0 | 1 | — | `doc_c09d33c9a2` | `doc_c09d33c9a2` |
| `hyperstition:hyperstition/the-heights-of-wuthering-starport` | 0 | 1 | — | `doc_12bc3d4c73` | `doc_12bc3d4c73` |
| `hyperstition:hyperstition/the-heirlooms-journey` | 0 | 1 | — | `doc_84b4de06f8` | `doc_84b4de06f8` |
| `hyperstition:hyperstition/the-highland-crowns-secret` | 0 | 1 | — | `doc_62670a8bcd` | `doc_62670a8bcd` |
| `hyperstition:hyperstition/the-hollow-harvest` | 0 | 1 | — | `doc_31846efca2` | `doc_31846efca2` |
| `hyperstition:hyperstition/the-hollow-mans-london` | 0 | 1 | — | `doc_990489ae1a` | `doc_990489ae1a` |
| `hyperstition:hyperstition/the-house-on-shadow-ridge` | 0 | 1 | — | `doc_9a242b68f1` | `doc_9a242b68f1` |
| `hyperstition:hyperstition/the-inn-at-punta-negra` | 0 | 1 | — | `doc_5561786796` | `doc_5561786796` |
| `hyperstition:hyperstition/the-iron-rails-of-perdition` | 0 | 1 | — | `doc_a1a3eafe8a` | `doc_a1a3eafe8a` |
| `hyperstition:hyperstition/the-iron-stars-last-stand` | 0 | 1 | — | `doc_095e4037d6` | `doc_095e4037d6` |
| `hyperstition:hyperstition/the-iron-ward-siege` | 0 | 1 | — | `doc_566dd51778` | `doc_566dd51778` |
| `hyperstition:hyperstition/the-irresistible-impulse` | 0 | 1 | — | `doc_e56e5237d7` | `doc_e56e5237d7` |
| `hyperstition:hyperstition/the-larrabee-deception` | 0 | 1 | — | `doc_4fb162e0ea` | `doc_4fb162e0ea` |
| `hyperstition:hyperstition/the-last-close-up` | 0 | 1 | — | `doc_bc071d5e80` | `doc_bc071d5e80` |
| `hyperstition:hyperstition/the-last-good-work` | 0 | 1 | — | `doc_e120797b91` | `doc_e120797b91` |
| `hyperstition:hyperstition/the-last-stage` | 0 | 1 | — | `doc_3b5227e256` | `doc_3b5227e256` |
| `hyperstition:hyperstition/the-last-stand-at-kepler-station` | 0 | 1 | — | `doc_24fefa637d` | `doc_24fefa637d` |
| `hyperstition:hyperstition/the-law-of-the-realm` | 0 | 1 | — | `doc_a5a0a85856` | `doc_a5a0a85856` |
| `hyperstition:hyperstition/the-liberation-of-desire` | 0 | 1 | — | `doc_86266d013f` | `doc_86266d013f` |
| `hyperstition:hyperstition/the-lost-children-of-clearwater` | 0 | 1 | — | `doc_03d65edc35` | `doc_03d65edc35` |
| `hyperstition:hyperstition/the-madding-crowd` | 0 | 1 | — | `doc_8dd5ebfde4` | `doc_8dd5ebfde4` |
| `hyperstition:hyperstition/the-magic-we-choose` | 0 | 1 | — | `doc_9c5781e019` | `doc_9c5781e019` |
| `hyperstition:hyperstition/the-mandalay-garrison` | 0 | 1 | — | `doc_dc95c6fbaf` | `doc_dc95c6fbaf` |
| `hyperstition:hyperstition/the-microscopic-murders` | 0 | 1 | — | `doc_2071d722be` | `doc_2071d722be` |
| `hyperstition:hyperstition/the-miracle-at-borgen-farm` | 0 | 1 | — | `doc_c745d677ed` | `doc_c745d677ed` |
| `hyperstition:hyperstition/the-moonstone-conspiracy` | 0 | 1 | — | `doc_0257428dfc` | `doc_0257428dfc` |
| `hyperstition:hyperstition/the-moral-architecture-of-memory` | 0 | 1 | — | `doc_32d0a038ae` | `doc_32d0a038ae` |
| `hyperstition:hyperstition/the-moral-calculus-of-justice` | 0 | 1 | — | `doc_d3a8c19f19` | `doc_d3a8c19f19` |
| `hyperstition:hyperstition/the-mysteries-we-leave-behind` | 0 | 1 | — | `doc_9396f7ca3a` | `doc_9396f7ca3a` |
| `hyperstition:hyperstition/the-noon-bell-tolls` | 0 | 1 | — | `doc_2737466d98` | `doc_2737466d98` |
| `hyperstition:hyperstition/the-observatory-keepers-wife` | 0 | 1 | — | `doc_d3793380fc` | `doc_d3793380fc` |
| `hyperstition:hyperstition/the-pan-prohibition` | 0 | 1 | — | `doc_73a4ab225a` | `doc_73a4ab225a` |
| `hyperstition:hyperstition/the-party-line-murders` | 0 | 1 | — | `doc_1d003092e9` | `doc_1d003092e9` |
| `hyperstition:hyperstition/the-passing-game` | 0 | 1 | — | `doc_1e48ee4de3` | `doc_1e48ee4de3` |
| `hyperstition:hyperstition/the-pattern-behind-the-paper` | 0 | 1 | — | `doc_a385c89fbf` | `doc_a385c89fbf` |
| `hyperstition:hyperstition/the-peacemakers-gambit` | 0 | 1 | — | `doc_b86bd56d75` | `doc_b86bd56d75` |
| `hyperstition:hyperstition/the-perfect-alibi-problem` | 0 | 1 | — | `doc_e21805bb47` | `doc_e21805bb47` |
| `hyperstition:hyperstition/the-perfect-bridge` | 0 | 1 | — | `doc_9b81898790` | `doc_9b81898790` |
| `hyperstition:hyperstition/the-perfect-drop` | 0 | 1 | — | `doc_d129e9d00f` | `doc_d129e9d00f` |
| `hyperstition:hyperstition/the-phantoms-berth` | 0 | 1 | — | `doc_0321e94b87` | `doc_0321e94b87` |
| `hyperstition:hyperstition/the-promise-road` | 0 | 1 | — | `doc_1f0a22d5a8` | `doc_1f0a22d5a8` |
| `hyperstition:hyperstition/the-ragged-staff-protocol` | 0 | 1 | — | `doc_7d5e24fe53` | `doc_7d5e24fe53` |
| `hyperstition:hyperstition/the-realm-keepers` | 0 | 1 | — | `doc_05a2b8bf30` | `doc_05a2b8bf30` |
| `hyperstition:hyperstition/the-sacred-grove-of-hearts` | 0 | 1 | — | `doc_fe3170dce8` | `doc_fe3170dce8` |
| `hyperstition:hyperstition/the-scarlet-steam-rose` | 0 | 1 | — | `doc_ece819f4d3` | `doc_ece819f4d3` |
| `hyperstition:hyperstition/the-scarlet-thread-of-love` | 0 | 1 | — | `doc_2cc5bfad29` | `doc_2cc5bfad29` |
| `hyperstition:hyperstition/the-september-murders-in-mandalay` | 0 | 1 | — | `doc_7aed4a1550` | `doc_7aed4a1550` |
| `hyperstition:hyperstition/the-silence-between-visits` | 0 | 1 | — | `doc_eb5dac520d` | `doc_eb5dac520d` |
| `hyperstition:hyperstition/the-sirens-final-song` | 0 | 1 | — | `doc_44c02b6fc6` | `doc_44c02b6fc6` |
| `hyperstition:hyperstition/the-sky-roads-home` | 0 | 1 | — | `doc_9c23fe8962` | `doc_9c23fe8962` |
| `hyperstition:hyperstition/the-solomon-conspiracy` | 0 | 1 | — | `doc_300aafc8ec` | `doc_300aafc8ec` |
| `hyperstition:hyperstition/the-soplica-rebellion` | 0 | 1 | — | `doc_98e6ada390` | `doc_98e6ada390` |
| `hyperstition:hyperstition/the-spirit-burns-on` | 0 | 1 | — | `doc_22bd3badb7` | `doc_22bd3badb7` |
| `hyperstition:hyperstition/the-tiverton-reckoning` | 0 | 1 | — | `doc_33b696fdfa` | `doc_33b696fdfa` |
| `hyperstition:hyperstition/the-tower-of-madeleine` | 0 | 1 | — | `doc_4a0d3fa34a` | `doc_4a0d3fa34a` |
| `hyperstition:hyperstition/the-transmission-chamber` | 0 | 1 | — | `doc_ef186b47fc` | `doc_ef186b47fc` |
| `hyperstition:hyperstition/the-valley-beyond-the-mountains` | 0 | 1 | — | `doc_c87aefb9ca` | `doc_c87aefb9ca` |
| `hyperstition:hyperstition/the-violet-fields-of-time` | 0 | 1 | — | `doc_0058f931cb` | `doc_0058f931cb` |
| `hyperstition:hyperstition/the-visible-heart` | 0 | 1 | — | `doc_1bb021e3fe` | `doc_1bb021e3fe` |
| `hyperstition:hyperstition/the-water-between-us` | 0 | 1 | — | `doc_1359ba4275` | `doc_1359ba4275` |
| `hyperstition:hyperstition/the-wedding-protocol` | 0 | 1 | — | `doc_415a65d8cf` | `doc_415a65d8cf` |
| `hyperstition:hyperstition/the-weight-of-gold` | 0 | 1 | — | `doc_621a4c7375` | `doc_621a4c7375` |
| `hyperstition:hyperstition/the-weight-of-surrender` | 0 | 1 | — | `doc_b1449e73e2` | `doc_b1449e73e2` |
| `hyperstition:hyperstition/the-weight-of-tomorrow` | 0 | 1 | — | `doc_85462411f6` | `doc_85462411f6` |
| `hyperstition:hyperstition/the-whatsis-burns` | 0 | 1 | — | `doc_60657c9dcb` | `doc_60657c9dcb` |
| `hyperstition:hyperstition/the-witness-in-winters-end` | 0 | 1 | — | `doc_f7db811989` | `doc_f7db811989` |
| `hyperstition:hyperstition/to-be-or-not` | 0 | 1 | — | `doc_a45af940ec` | `doc_a45af940ec` |
| `hyperstition:hyperstition/warriors-of-the-heart` | 0 | 1 | — | `doc_d20af3a4bb` | `doc_d20af3a4bb` |
| `hyperstition:hyperstition/when-the-forest-comes-home` | 0 | 1 | — | `doc_9f53d70e36` | `doc_9f53d70e36` |
| `hyperstition:hyperstition/when-the-stars-fall-silent` | 0 | 1 | — | `doc_430c0ec613` | `doc_430c0ec613` |
| `identity:generated/identity_106018a0b66c_id_01` | 1 | 0 | `identity_106018a0b66c_id_01` | — | `identity_106018a0b66c_id_01` |
| `identity:generated/identity_106018a0b66c_id_03` | 1 | 0 | `identity_106018a0b66c_id_03` | — | `identity_106018a0b66c_id_03` |
| `identity:generated/identity_106018a0b66c_id_18` | 1 | 0 | `identity_106018a0b66c_id_18` | — | `identity_106018a0b66c_id_18` |
| `identity:generated/identity_106018a0b66c_id_19` | 1 | 0 | `identity_106018a0b66c_id_19` | — | `identity_106018a0b66c_id_19` |
| `identity:generated/identity_106018a0b66c_id_20` | 1 | 0 | `identity_106018a0b66c_id_20` | — | `identity_106018a0b66c_id_20` |
| `identity:generated/identity_106018a0b66c_id_21` | 1 | 0 | `identity_106018a0b66c_id_21` | — | `identity_106018a0b66c_id_21` |
| `identity:generated/identity_106018a0b66c_id_22` | 1 | 0 | `identity_106018a0b66c_id_22` | — | `identity_106018a0b66c_id_22` |
| `identity:generated/identity_106018a0b66c_id_25` | 1 | 0 | `identity_106018a0b66c_id_25` | — | `identity_106018a0b66c_id_25` |
| `identity:generated/identity_106018a0b66c_id_27` | 1 | 0 | `identity_106018a0b66c_id_27` | — | `identity_106018a0b66c_id_27` |
| `identity:generated/identity_106018a0b66c_id_31` | 1 | 0 | `identity_106018a0b66c_id_31` | — | `identity_106018a0b66c_id_31` |
| `identity:generated/identity_106018a0b66c_id_38` | 1 | 0 | `identity_106018a0b66c_id_38` | — | `identity_106018a0b66c_id_38` |
| `identity:generated/identity_106018a0b66c_id_39` | 1 | 0 | `identity_106018a0b66c_id_39` | — | `identity_106018a0b66c_id_39` |
| `identity:generated/identity_f921fd061f08_id_03` | 1 | 0 | `identity_f921fd061f08_id_03` | — | `identity_f921fd061f08_id_03` |
| `identity:generated/identity_f921fd061f08_id_06` | 1 | 0 | `identity_f921fd061f08_id_06` | — | `identity_f921fd061f08_id_06` |
| `identity:generated/identity_f921fd061f08_id_15` | 1 | 0 | `identity_f921fd061f08_id_15` | — | `identity_f921fd061f08_id_15` |
| `identity:generated/identity_f921fd061f08_id_17` | 1 | 0 | `identity_f921fd061f08_id_17` | — | `identity_f921fd061f08_id_17` |
| `identity:generated/identity_f921fd061f08_id_27` | 1 | 0 | `identity_f921fd061f08_id_27` | — | `identity_f921fd061f08_id_27` |
| `identity:generated/identity_f921fd061f08_id_28` | 1 | 0 | `identity_f921fd061f08_id_28` | — | `identity_f921fd061f08_id_28` |
| `identity:generated/identity_f921fd061f08_id_36` | 1 | 0 | `identity_f921fd061f08_id_36` | — | `identity_f921fd061f08_id_36` |
| `identity:generated/identity_f921fd061f08_id_37` | 1 | 0 | `identity_f921fd061f08_id_37` | — | `identity_f921fd061f08_id_37` |
| `identity:generated/identity_f921fd061f08_id_39` | 1 | 0 | `identity_f921fd061f08_id_39` | — | `identity_f921fd061f08_id_39` |
| `identity_v2:spec/00099bdc4232` | 1 | 0 | `identity2_048_id_34` | — | `identity2_048_id_34` |
| `identity_v2:spec/00978f9f4e27` | 1 | 0 | `identity2_096_id_00` | — | `identity2_096_id_00` |
| `identity_v2:spec/010ebc1510b0` | 1 | 0 | `identity2_096_id_05` | — | `identity2_096_id_05` |
| `identity_v2:spec/01b0fb87c769` | 1 | 0 | `identity2_069_id_07` | — | `identity2_069_id_07` |
| `identity_v2:spec/01ca61358d10` | 1 | 0 | `identity2_064_id_15` | — | `identity2_064_id_15` |
| `identity_v2:spec/02b7f55172f0` | 1 | 0 | `identity2_009_id_07` | — | `identity2_009_id_07` |
| `identity_v2:spec/04af81cd2980` | 1 | 0 | `identity2_013_id_09` | — | `identity2_013_id_09` |
| `identity_v2:spec/04ebacd3a14c` | 2 | 0 | `identity2_027_id_03`, `identity2_064_id_08` | — | `identity2_027_id_03`, `identity2_064_id_08` |
| `identity_v2:spec/053a13a377df` | 1 | 0 | `identity2_036_id_14` | — | `identity2_036_id_14` |
| `identity_v2:spec/066c44eb81ab` | 1 | 0 | `identity2_058_id_32` | — | `identity2_058_id_32` |
| `identity_v2:spec/06acc0fbd822` | 1 | 0 | `identity2_026_id_37` | — | `identity2_026_id_37` |
| `identity_v2:spec/06c44275a921` | 1 | 0 | `identity2_093_id_02` | — | `identity2_093_id_02` |
| `identity_v2:spec/06c74bec37fd` | 1 | 0 | `identity2_091_id_13` | — | `identity2_091_id_13` |
| `identity_v2:spec/06cca11b8b2e` | 1 | 0 | `identity2_006_id_03` | — | `identity2_006_id_03` |
| `identity_v2:spec/077dc78a7ea1` | 1 | 0 | `identity2_081_id_10` | — | `identity2_081_id_10` |
| `identity_v2:spec/080d3ec1dce4` | 1 | 0 | `identity2_065_id_01` | — | `identity2_065_id_01` |
| `identity_v2:spec/082859dfd226` | 1 | 0 | `identity2_007_id_09` | — | `identity2_007_id_09` |
| `identity_v2:spec/0852133f5b63` | 2 | 0 | `identity2_074_id_11`, `identity2_075_id_09` | — | `identity2_074_id_11`, `identity2_075_id_09` |
| `identity_v2:spec/08c2de881d64` | 1 | 0 | `identity2_000_id_12` | — | `identity2_000_id_12` |
| `identity_v2:spec/094a5c0d046c` | 1 | 0 | `identity2_060_id_32` | — | `identity2_060_id_32` |
| `identity_v2:spec/099da5ec1566` | 1 | 0 | `identity2_036_id_16` | — | `identity2_036_id_16` |
| `identity_v2:spec/09a414b2f012` | 1 | 0 | `identity2_073_id_10` | — | `identity2_073_id_10` |
| `identity_v2:spec/0a89eb63ef15` | 1 | 0 | `identity2_061_id_12` | — | `identity2_061_id_12` |
| `identity_v2:spec/0a918e7f1576` | 1 | 0 | `identity2_078_id_19` | — | `identity2_078_id_19` |
| `identity_v2:spec/0b07120d9f8e` | 1 | 0 | `identity2_000_id_18` | — | `identity2_000_id_18` |
| `identity_v2:spec/0b927e384740` | 1 | 0 | `identity2_059_id_15` | — | `identity2_059_id_15` |
| `identity_v2:spec/0c5c2ae90934` | 1 | 0 | `identity2_015_id_21` | — | `identity2_015_id_21` |
| `identity_v2:spec/0cca3077df6d` | 1 | 0 | `identity2_043_id_29` | — | `identity2_043_id_29` |
| `identity_v2:spec/0d5f1d766431` | 1 | 0 | `identity2_021_id_20` | — | `identity2_021_id_20` |
| `identity_v2:spec/0dd0b9cc3eab` | 1 | 0 | `identity2_004_id_25` | — | `identity2_004_id_25` |
| `identity_v2:spec/0e11d594c707` | 1 | 0 | `identity2_060_id_14` | — | `identity2_060_id_14` |
| `identity_v2:spec/0e4161ae4421` | 1 | 0 | `identity2_016_id_36` | — | `identity2_016_id_36` |
| `identity_v2:spec/0e51c1a1c9c4` | 1 | 0 | `identity2_043_id_25` | — | `identity2_043_id_25` |
| `identity_v2:spec/0e98bc4be33a` | 1 | 0 | `identity2_037_id_04` | — | `identity2_037_id_04` |
| `identity_v2:spec/0effb7644819` | 1 | 0 | `identity2_071_id_16` | — | `identity2_071_id_16` |
| `identity_v2:spec/10ae1614e875` | 1 | 0 | `identity2_024_id_11` | — | `identity2_024_id_11` |
| `identity_v2:spec/116e22117f5f` | 1 | 0 | `identity2_085_id_17` | — | `identity2_085_id_17` |
| `identity_v2:spec/11a26688809a` | 1 | 0 | `identity2_058_id_09` | — | `identity2_058_id_09` |
| `identity_v2:spec/123567c33d6e` | 1 | 0 | `identity2_036_id_22` | — | `identity2_036_id_22` |
| `identity_v2:spec/12821c10c432` | 1 | 0 | `identity2_065_id_04` | — | `identity2_065_id_04` |
| `identity_v2:spec/12c8b6e05465` | 1 | 0 | `identity2_024_id_16` | — | `identity2_024_id_16` |
| `identity_v2:spec/1333fccb8a64` | 1 | 0 | `identity2_028_id_00` | — | `identity2_028_id_00` |
| `identity_v2:spec/133d959c828f` | 1 | 0 | `identity2_025_id_23` | — | `identity2_025_id_23` |
| `identity_v2:spec/137d09b01062` | 1 | 0 | `identity2_021_id_30` | — | `identity2_021_id_30` |
| `identity_v2:spec/138abe902c94` | 1 | 0 | `identity2_029_id_35` | — | `identity2_029_id_35` |
| `identity_v2:spec/140eebf9cc6e` | 1 | 0 | `identity2_060_id_12` | — | `identity2_060_id_12` |
| `identity_v2:spec/1471e69c050e` | 1 | 0 | `identity2_046_id_03` | — | `identity2_046_id_03` |
| `identity_v2:spec/15a0c7f20020` | 1 | 0 | `identity2_027_id_22` | — | `identity2_027_id_22` |
| `identity_v2:spec/161c2c3a2917` | 1 | 0 | `identity2_021_id_02` | — | `identity2_021_id_02` |
| `identity_v2:spec/1710978040b0` | 1 | 0 | `identity2_046_id_20` | — | `identity2_046_id_20` |
| `identity_v2:spec/1724fc7de011` | 1 | 0 | `identity2_040_id_21` | — | `identity2_040_id_21` |
| `identity_v2:spec/175aa84d14e4` | 1 | 0 | `identity2_039_id_30` | — | `identity2_039_id_30` |
| `identity_v2:spec/17901a1317ef` | 1 | 0 | `identity2_043_id_39` | — | `identity2_043_id_39` |
| `identity_v2:spec/17b41e58e660` | 1 | 0 | `identity2_000_id_39` | — | `identity2_000_id_39` |
| `identity_v2:spec/17b79bd2df45` | 1 | 0 | `identity2_027_id_27` | — | `identity2_027_id_27` |
| `identity_v2:spec/187353f111c8` | 1 | 0 | `identity2_010_id_09` | — | `identity2_010_id_09` |
| `identity_v2:spec/188caf56c5e8` | 1 | 0 | `identity2_058_id_26` | — | `identity2_058_id_26` |
| `identity_v2:spec/188e553ae629` | 1 | 0 | `identity2_026_id_18` | — | `identity2_026_id_18` |
| `identity_v2:spec/1905dbae7803` | 1 | 0 | `identity2_083_id_00` | — | `identity2_083_id_00` |
| `identity_v2:spec/19165e8ca44e` | 1 | 0 | `identity2_035_id_11` | — | `identity2_035_id_11` |
| `identity_v2:spec/192201f03cbd` | 1 | 0 | `identity2_020_id_08` | — | `identity2_020_id_08` |
| `identity_v2:spec/1947768b348a` | 1 | 0 | `identity2_015_id_19` | — | `identity2_015_id_19` |
| `identity_v2:spec/19f4560f0e30` | 1 | 0 | `identity2_014_id_11` | — | `identity2_014_id_11` |
| `identity_v2:spec/1a2540ecf83b` | 1 | 0 | `identity2_020_id_19` | — | `identity2_020_id_19` |
| `identity_v2:spec/1b298434afe3` | 1 | 0 | `identity2_086_id_17` | — | `identity2_086_id_17` |
| `identity_v2:spec/1bc427d404c9` | 1 | 0 | `identity2_071_id_08` | — | `identity2_071_id_08` |
| `identity_v2:spec/1d447fcb1448` | 1 | 0 | `identity2_016_id_21` | — | `identity2_016_id_21` |
| `identity_v2:spec/1d4b4b16005f` | 1 | 0 | `identity2_001_id_13` | — | `identity2_001_id_13` |
| `identity_v2:spec/1edf0752e5a9` | 1 | 0 | `identity2_039_id_32` | — | `identity2_039_id_32` |
| `identity_v2:spec/1ef24584a18c` | 1 | 0 | `identity2_011_id_08` | — | `identity2_011_id_08` |
| `identity_v2:spec/1ef4cb0a2ef8` | 1 | 0 | `identity2_001_id_10` | — | `identity2_001_id_10` |
| `identity_v2:spec/1facd5fc19d8` | 1 | 0 | `identity2_027_id_26` | — | `identity2_027_id_26` |
| `identity_v2:spec/2052fa36d14f` | 1 | 0 | `identity2_051_id_09` | — | `identity2_051_id_09` |
| `identity_v2:spec/205dffe5c960` | 1 | 0 | `identity2_009_id_03` | — | `identity2_009_id_03` |
| `identity_v2:spec/21468f39b0dc` | 1 | 0 | `identity2_041_id_00` | — | `identity2_041_id_00` |
| `identity_v2:spec/228c51909d1f` | 1 | 0 | `identity2_086_id_03` | — | `identity2_086_id_03` |
| `identity_v2:spec/228c8f40131a` | 1 | 0 | `identity2_001_id_21` | — | `identity2_001_id_21` |
| `identity_v2:spec/23d605137ee3` | 1 | 0 | `identity2_000_id_27` | — | `identity2_000_id_27` |
| `identity_v2:spec/23f37516004e` | 1 | 0 | `identity2_027_id_23` | — | `identity2_027_id_23` |
| `identity_v2:spec/2545d534d711` | 1 | 0 | `identity2_068_id_04` | — | `identity2_068_id_04` |
| `identity_v2:spec/258a3c7769f2` | 1 | 0 | `identity2_013_id_13` | — | `identity2_013_id_13` |
| `identity_v2:spec/25a36fddbb04` | 1 | 0 | `identity2_015_id_13` | — | `identity2_015_id_13` |
| `identity_v2:spec/25abb87f2222` | 1 | 0 | `identity2_027_id_04` | — | `identity2_027_id_04` |
| `identity_v2:spec/266cea0006cf` | 1 | 0 | `identity2_036_id_21` | — | `identity2_036_id_21` |
| `identity_v2:spec/26746c9baa40` | 1 | 0 | `identity2_076_id_18` | — | `identity2_076_id_18` |
| `identity_v2:spec/2700b8ee56a5` | 1 | 0 | `identity2_048_id_01` | — | `identity2_048_id_01` |
| `identity_v2:spec/275673f78061` | 1 | 0 | `identity2_072_id_06` | — | `identity2_072_id_06` |
| `identity_v2:spec/2759fc6bc93d` | 1 | 0 | `identity2_048_id_15` | — | `identity2_048_id_15` |
| `identity_v2:spec/281f1758a629` | 1 | 0 | `identity2_046_id_18` | — | `identity2_046_id_18` |
| `identity_v2:spec/28361886678c` | 1 | 0 | `identity2_015_id_27` | — | `identity2_015_id_27` |
| `identity_v2:spec/28cc5e184c1b` | 1 | 0 | `identity2_027_id_10` | — | `identity2_027_id_10` |
| `identity_v2:spec/28f505274175` | 1 | 0 | `identity2_027_id_02` | — | `identity2_027_id_02` |
| `identity_v2:spec/29c02446b945` | 1 | 0 | `identity2_061_id_17` | — | `identity2_061_id_17` |
| `identity_v2:spec/29c652b516c3` | 1 | 0 | `identity2_044_id_09` | — | `identity2_044_id_09` |
| `identity_v2:spec/2af5083b11d8` | 1 | 0 | `identity2_009_id_02` | — | `identity2_009_id_02` |
| `identity_v2:spec/2b0c8b63eccd` | 1 | 0 | `identity2_069_id_11` | — | `identity2_069_id_11` |
| `identity_v2:spec/2b2f4025d5fb` | 1 | 0 | `identity2_029_id_22` | — | `identity2_029_id_22` |
| `identity_v2:spec/2b5d925cc377` | 1 | 0 | `identity2_093_id_05` | — | `identity2_093_id_05` |
| `identity_v2:spec/2b65aa10dde2` | 1 | 0 | `identity2_035_id_26` | — | `identity2_035_id_26` |
| `identity_v2:spec/2b68707a7c75` | 1 | 0 | `identity2_051_id_16` | — | `identity2_051_id_16` |
| `identity_v2:spec/2b7a5b6446c1` | 1 | 0 | `identity2_051_id_06` | — | `identity2_051_id_06` |
| `identity_v2:spec/2b827bf42110` | 1 | 0 | `identity2_013_id_35` | — | `identity2_013_id_35` |
| `identity_v2:spec/2bcf420e4fe6` | 1 | 0 | `identity2_002_id_29` | — | `identity2_002_id_29` |
| `identity_v2:spec/2c2682727c44` | 1 | 0 | `identity2_010_id_12` | — | `identity2_010_id_12` |
| `identity_v2:spec/2d067630c1df` | 1 | 0 | `identity2_010_id_22` | — | `identity2_010_id_22` |
| `identity_v2:spec/2d19291285c1` | 1 | 0 | `identity2_008_id_02` | — | `identity2_008_id_02` |
| `identity_v2:spec/2d7d6b6fb29c` | 1 | 0 | `identity2_028_id_07` | — | `identity2_028_id_07` |
| `identity_v2:spec/2dbd772a9e56` | 1 | 0 | `identity2_061_id_18` | — | `identity2_061_id_18` |
| `identity_v2:spec/2dd3a7373f89` | 1 | 0 | `identity2_020_id_26` | — | `identity2_020_id_26` |
| `identity_v2:spec/2e07d3b977d0` | 1 | 0 | `identity2_046_id_19` | — | `identity2_046_id_19` |
| `identity_v2:spec/2e49bfacf45f` | 1 | 0 | `identity2_007_id_21` | — | `identity2_007_id_21` |
| `identity_v2:spec/2ede527ac730` | 1 | 0 | `identity2_033_id_07` | — | `identity2_033_id_07` |
| `identity_v2:spec/2efbc5c01320` | 1 | 0 | `identity2_052_id_25` | — | `identity2_052_id_25` |
| `identity_v2:spec/2f3c733fe229` | 1 | 0 | `identity2_000_id_25` | — | `identity2_000_id_25` |
| `identity_v2:spec/2fb35e01643d` | 1 | 0 | `identity2_036_id_13` | — | `identity2_036_id_13` |
| `identity_v2:spec/2fc204dbc29a` | 2 | 0 | `identity2_033_id_03`, `identity2_041_id_23` | — | `identity2_033_id_03`, `identity2_041_id_23` |
| `identity_v2:spec/30aebf7118a7` | 2 | 0 | `identity2_036_id_17`, `identity2_075_id_02` | — | `identity2_036_id_17`, `identity2_075_id_02` |
| `identity_v2:spec/30ef152a387d` | 1 | 0 | `identity2_052_id_15` | — | `identity2_052_id_15` |
| `identity_v2:spec/312766095383` | 1 | 0 | `identity2_016_id_16` | — | `identity2_016_id_16` |
| `identity_v2:spec/317444d06fe7` | 1 | 0 | `identity2_028_id_06` | — | `identity2_028_id_06` |
| `identity_v2:spec/317aa1aade29` | 1 | 0 | `identity2_046_id_35` | — | `identity2_046_id_35` |
| `identity_v2:spec/321b980225a1` | 1 | 0 | `identity2_060_id_07` | — | `identity2_060_id_07` |
| `identity_v2:spec/3221e04050c3` | 2 | 0 | `identity2_011_id_01`, `identity2_023_id_05` | — | `identity2_011_id_01`, `identity2_023_id_05` |
| `identity_v2:spec/32415036bb60` | 1 | 0 | `identity2_040_id_17` | — | `identity2_040_id_17` |
| `identity_v2:spec/32635923f0c8` | 1 | 0 | `identity2_027_id_16` | — | `identity2_027_id_16` |
| `identity_v2:spec/329343e4458a` | 1 | 0 | `identity2_089_id_01` | — | `identity2_089_id_01` |
| `identity_v2:spec/336620860383` | 1 | 0 | `identity2_090_id_04` | — | `identity2_090_id_04` |
| `identity_v2:spec/337f428f8274` | 1 | 0 | `identity2_070_id_11` | — | `identity2_070_id_11` |
| `identity_v2:spec/33b0a6906258` | 1 | 0 | `identity2_021_id_01` | — | `identity2_021_id_01` |
| `identity_v2:spec/33df426eda8a` | 1 | 0 | `identity2_040_id_02` | — | `identity2_040_id_02` |
| `identity_v2:spec/3462669ae5ba` | 1 | 0 | `identity2_076_id_07` | — | `identity2_076_id_07` |
| `identity_v2:spec/349dc51d55f9` | 1 | 0 | `identity2_086_id_14` | — | `identity2_086_id_14` |
| `identity_v2:spec/3591448c8d12` | 1 | 0 | `identity2_017_id_06` | — | `identity2_017_id_06` |
| `identity_v2:spec/35ba1e9f043f` | 1 | 0 | `identity2_019_id_24` | — | `identity2_019_id_24` |
| `identity_v2:spec/377310e95d87` | 2 | 0 | `identity2_044_id_07`, `identity2_052_id_31` | — | `identity2_044_id_07`, `identity2_052_id_31` |
| `identity_v2:spec/379ab0ebbc74` | 1 | 0 | `identity2_025_id_39` | — | `identity2_025_id_39` |
| `identity_v2:spec/37dd0ac628f3` | 1 | 0 | `identity2_021_id_18` | — | `identity2_021_id_18` |
| `identity_v2:spec/3831f6404da8` | 1 | 0 | `identity2_092_id_07` | — | `identity2_092_id_07` |
| `identity_v2:spec/386ca7b0afa1` | 1 | 0 | `identity2_046_id_22` | — | `identity2_046_id_22` |
| `identity_v2:spec/3878ed131895` | 1 | 0 | `identity2_066_id_00` | — | `identity2_066_id_00` |
| `identity_v2:spec/389b94d292d6` | 1 | 0 | `identity2_043_id_35` | — | `identity2_043_id_35` |
| `identity_v2:spec/38ccfc0c78bf` | 1 | 0 | `identity2_059_id_39` | — | `identity2_059_id_39` |
| `identity_v2:spec/3b08fb62b1f9` | 1 | 0 | `identity2_069_id_12` | — | `identity2_069_id_12` |
| `identity_v2:spec/3b3f8ac0a41d` | 1 | 0 | `identity2_001_id_30` | — | `identity2_001_id_30` |
| `identity_v2:spec/3b93b15bcf9d` | 1 | 0 | `identity2_046_id_02` | — | `identity2_046_id_02` |
| `identity_v2:spec/3c118a6066aa` | 1 | 0 | `identity2_076_id_00` | — | `identity2_076_id_00` |
| `identity_v2:spec/3c5a0e01e8f0` | 1 | 0 | `identity2_073_id_04` | — | `identity2_073_id_04` |
| `identity_v2:spec/3cb666459747` | 2 | 0 | `identity2_004_id_28`, `identity2_082_id_00` | — | `identity2_004_id_28`, `identity2_082_id_00` |
| `identity_v2:spec/3d420c2a5150` | 1 | 0 | `identity2_052_id_19` | — | `identity2_052_id_19` |
| `identity_v2:spec/3d4f191f8ec3` | 1 | 0 | `identity2_042_id_22` | — | `identity2_042_id_22` |
| `identity_v2:spec/3d5b93c40e83` | 1 | 0 | `identity2_004_id_17` | — | `identity2_004_id_17` |
| `identity_v2:spec/3d7c817a074e` | 1 | 0 | `identity2_051_id_32` | — | `identity2_051_id_32` |
| `identity_v2:spec/3d859b3d21fd` | 1 | 0 | `identity2_016_id_17` | — | `identity2_016_id_17` |
| `identity_v2:spec/3dc8bf048741` | 1 | 0 | `identity2_028_id_23` | — | `identity2_028_id_23` |
| `identity_v2:spec/3e18310f5050` | 1 | 0 | `identity2_069_id_03` | — | `identity2_069_id_03` |
| `identity_v2:spec/3e33178a6ba1` | 1 | 0 | `identity2_017_id_25` | — | `identity2_017_id_25` |
| `identity_v2:spec/3e53963f9326` | 1 | 0 | `identity2_089_id_05` | — | `identity2_089_id_05` |
| `identity_v2:spec/3e717478e8e2` | 1 | 0 | `identity2_016_id_39` | — | `identity2_016_id_39` |
| `identity_v2:spec/3eb3e4d5f425` | 1 | 0 | `identity2_002_id_28` | — | `identity2_002_id_28` |
| `identity_v2:spec/3eca153eae65` | 1 | 0 | `identity2_087_id_01` | — | `identity2_087_id_01` |
| `identity_v2:spec/3f3da411e80b` | 1 | 0 | `identity2_040_id_09` | — | `identity2_040_id_09` |
| `identity_v2:spec/40be2c9cabc3` | 1 | 0 | `identity2_024_id_20` | — | `identity2_024_id_20` |
| `identity_v2:spec/416d70c3aaa3` | 1 | 0 | `identity2_014_id_16` | — | `identity2_014_id_16` |
| `identity_v2:spec/41ad084f158f` | 1 | 0 | `identity2_074_id_03` | — | `identity2_074_id_03` |
| `identity_v2:spec/4201eb6deb2a` | 1 | 0 | `identity2_002_id_08` | — | `identity2_002_id_08` |
| `identity_v2:spec/4273ae9f430d` | 1 | 0 | `identity2_001_id_32` | — | `identity2_001_id_32` |
| `identity_v2:spec/43ac743d7f4b` | 1 | 0 | `identity2_087_id_04` | — | `identity2_087_id_04` |
| `identity_v2:spec/4411572af8b5` | 1 | 0 | `identity2_020_id_37` | — | `identity2_020_id_37` |
| `identity_v2:spec/442a790418b5` | 1 | 0 | `identity2_064_id_10` | — | `identity2_064_id_10` |
| `identity_v2:spec/4466e3398558` | 1 | 0 | `identity2_024_id_17` | — | `identity2_024_id_17` |
| `identity_v2:spec/44c1b0bd6a5d` | 1 | 0 | `identity2_041_id_29` | — | `identity2_041_id_29` |
| `identity_v2:spec/44cd8a7220b3` | 1 | 0 | `identity2_040_id_16` | — | `identity2_040_id_16` |
| `identity_v2:spec/4561f1618725` | 1 | 0 | `identity2_090_id_11` | — | `identity2_090_id_11` |
| `identity_v2:spec/45f770ad4e48` | 1 | 0 | `identity2_062_id_12` | — | `identity2_062_id_12` |
| `identity_v2:spec/45fcc2294fad` | 1 | 0 | `identity2_029_id_14` | — | `identity2_029_id_14` |
| `identity_v2:spec/45fd49b6f733` | 1 | 0 | `identity2_006_id_17` | — | `identity2_006_id_17` |
| `identity_v2:spec/472be1fa5a9d` | 1 | 0 | `identity2_002_id_17` | — | `identity2_002_id_17` |
| `identity_v2:spec/475b649365cf` | 1 | 0 | `identity2_067_id_02` | — | `identity2_067_id_02` |
| `identity_v2:spec/477e333d17c8` | 1 | 0 | `identity2_062_id_09` | — | `identity2_062_id_09` |
| `identity_v2:spec/48202b685312` | 1 | 0 | `identity2_051_id_12` | — | `identity2_051_id_12` |
| `identity_v2:spec/4875b27d8343` | 1 | 0 | `identity2_013_id_28` | — | `identity2_013_id_28` |
| `identity_v2:spec/48c5fed50739` | 1 | 0 | `identity2_081_id_11` | — | `identity2_081_id_11` |
| `identity_v2:spec/49419b6cdc37` | 1 | 0 | `identity2_010_id_17` | — | `identity2_010_id_17` |
| `identity_v2:spec/4959450c605d` | 1 | 0 | `identity2_062_id_02` | — | `identity2_062_id_02` |
| `identity_v2:spec/498bec043fbf` | 1 | 0 | `identity2_020_id_31` | — | `identity2_020_id_31` |
| `identity_v2:spec/49a2fb75ee4c` | 1 | 0 | `identity2_027_id_06` | — | `identity2_027_id_06` |
| `identity_v2:spec/49beec82e6c9` | 1 | 0 | `identity2_025_id_01` | — | `identity2_025_id_01` |
| `identity_v2:spec/4b2c9cb22fe4` | 1 | 0 | `identity2_024_id_29` | — | `identity2_024_id_29` |
| `identity_v2:spec/4b33236e0c2b` | 1 | 0 | `identity2_091_id_09` | — | `identity2_091_id_09` |
| `identity_v2:spec/4b80d3f85809` | 1 | 0 | `identity2_065_id_16` | — | `identity2_065_id_16` |
| `identity_v2:spec/4b88c2bfe2b4` | 1 | 0 | `identity2_069_id_17` | — | `identity2_069_id_17` |
| `identity_v2:spec/4baa30c7cea1` | 1 | 0 | `identity2_068_id_06` | — | `identity2_068_id_06` |
| `identity_v2:spec/4c5f41bb1b5f` | 1 | 0 | `identity2_040_id_19` | — | `identity2_040_id_19` |
| `identity_v2:spec/4c7e6a049df2` | 1 | 0 | `identity2_041_id_12` | — | `identity2_041_id_12` |
| `identity_v2:spec/4d15f6c978f6` | 1 | 0 | `identity2_077_id_08` | — | `identity2_077_id_08` |
| `identity_v2:spec/4d1f4e5a9cbf` | 1 | 0 | `identity2_013_id_18` | — | `identity2_013_id_18` |
| `identity_v2:spec/4d799b2fcb5f` | 1 | 0 | `identity2_035_id_16` | — | `identity2_035_id_16` |
| `identity_v2:spec/4d9b1c1c3b6a` | 1 | 0 | `identity2_066_id_08` | — | `identity2_066_id_08` |
| `identity_v2:spec/4e354048ba38` | 1 | 0 | `identity2_033_id_30` | — | `identity2_033_id_30` |
| `identity_v2:spec/4e5b17f4bb9c` | 1 | 0 | `identity2_028_id_11` | — | `identity2_028_id_11` |
| `identity_v2:spec/4ed63818e650` | 1 | 0 | `identity2_068_id_08` | — | `identity2_068_id_08` |
| `identity_v2:spec/4ede7caa15a8` | 1 | 0 | `identity2_025_id_18` | — | `identity2_025_id_18` |
| `identity_v2:spec/4ee0a925ae36` | 1 | 0 | `identity2_019_id_28` | — | `identity2_019_id_28` |
| `identity_v2:spec/4f1a5930e15f` | 1 | 0 | `identity2_033_id_16` | — | `identity2_033_id_16` |
| `identity_v2:spec/4f3d6f7a927b` | 1 | 0 | `identity2_073_id_15` | — | `identity2_073_id_15` |
| `identity_v2:spec/4f72bf15bf7e` | 1 | 0 | `identity2_066_id_02` | — | `identity2_066_id_02` |
| `identity_v2:spec/4fcd0df79e87` | 1 | 0 | `identity2_080_id_17` | — | `identity2_080_id_17` |
| `identity_v2:spec/502831ffbec4` | 1 | 0 | `identity2_004_id_14` | — | `identity2_004_id_14` |
| `identity_v2:spec/509be05fc057` | 1 | 0 | `identity2_064_id_00` | — | `identity2_064_id_00` |
| `identity_v2:spec/51c60f353e63` | 1 | 0 | `identity2_089_id_19` | — | `identity2_089_id_19` |
| `identity_v2:spec/5285729f0a28` | 1 | 0 | `identity2_075_id_01` | — | `identity2_075_id_01` |
| `identity_v2:spec/52cd4cda7bf9` | 1 | 0 | `identity2_018_id_20` | — | `identity2_018_id_20` |
| `identity_v2:spec/52e351dea721` | 1 | 0 | `identity2_025_id_32` | — | `identity2_025_id_32` |
| `identity_v2:spec/53291867a6cd` | 1 | 0 | `identity2_039_id_13` | — | `identity2_039_id_13` |
| `identity_v2:spec/54aabb80d4eb` | 1 | 0 | `identity2_026_id_26` | — | `identity2_026_id_26` |
| `identity_v2:spec/557a30e603b8` | 1 | 0 | `identity2_058_id_36` | — | `identity2_058_id_36` |
| `identity_v2:spec/559e9d804903` | 1 | 0 | `identity2_017_id_39` | — | `identity2_017_id_39` |
| `identity_v2:spec/560915e6ecf6` | 1 | 0 | `identity2_007_id_07` | — | `identity2_007_id_07` |
| `identity_v2:spec/564f71233408` | 1 | 0 | `identity2_019_id_32` | — | `identity2_019_id_32` |
| `identity_v2:spec/578a7b959923` | 1 | 0 | `identity2_038_id_36` | — | `identity2_038_id_36` |
| `identity_v2:spec/579e8820d659` | 1 | 0 | `identity2_055_id_23` | — | `identity2_055_id_23` |
| `identity_v2:spec/57aeed0dd640` | 1 | 0 | `identity2_067_id_05` | — | `identity2_067_id_05` |
| `identity_v2:spec/57b42fd06383` | 1 | 0 | `identity2_010_id_15` | — | `identity2_010_id_15` |
| `identity_v2:spec/57dc09ca0878` | 1 | 0 | `identity2_016_id_08` | — | `identity2_016_id_08` |
| `identity_v2:spec/58333f80661b` | 1 | 0 | `identity2_027_id_25` | — | `identity2_027_id_25` |
| `identity_v2:spec/584313dc8fc3` | 1 | 0 | `identity2_096_id_03` | — | `identity2_096_id_03` |
| `identity_v2:spec/58503e39d7d6` | 1 | 0 | `identity2_080_id_11` | — | `identity2_080_id_11` |
| `identity_v2:spec/585c232f3165` | 1 | 0 | `identity2_029_id_01` | — | `identity2_029_id_01` |
| `identity_v2:spec/585d893cd579` | 1 | 0 | `identity2_041_id_02` | — | `identity2_041_id_02` |
| `identity_v2:spec/58b0b8b4857c` | 1 | 0 | `identity2_038_id_27` | — | `identity2_038_id_27` |
| `identity_v2:spec/59f5a1bee8ef` | 1 | 0 | `identity2_026_id_35` | — | `identity2_026_id_35` |
| `identity_v2:spec/5a0cf2a13cc2` | 1 | 0 | `identity2_066_id_03` | — | `identity2_066_id_03` |
| `identity_v2:spec/5a99c92cdaea` | 1 | 0 | `identity2_038_id_25` | — | `identity2_038_id_25` |
| `identity_v2:spec/5a9a6cd17e26` | 1 | 0 | `identity2_006_id_20` | — | `identity2_006_id_20` |
| `identity_v2:spec/5b111e5fee61` | 1 | 0 | `identity2_025_id_04` | — | `identity2_025_id_04` |
| `identity_v2:spec/5b1c3fa2d4d3` | 1 | 0 | `identity2_074_id_00` | — | `identity2_074_id_00` |
| `identity_v2:spec/5c1cc20346bb` | 1 | 0 | `identity2_087_id_13` | — | `identity2_087_id_13` |
| `identity_v2:spec/5c96f9ca35de` | 1 | 0 | `identity2_017_id_00` | — | `identity2_017_id_00` |
| `identity_v2:spec/5ca1193a84b7` | 1 | 0 | `identity2_088_id_15` | — | `identity2_088_id_15` |
| `identity_v2:spec/5f0aab72d7a2` | 1 | 0 | `identity2_078_id_01` | — | `identity2_078_id_01` |
| `identity_v2:spec/5f7f4057c76b` | 1 | 0 | `identity2_051_id_26` | — | `identity2_051_id_26` |
| `identity_v2:spec/5fa24c96e5e0` | 1 | 0 | `identity2_061_id_13` | — | `identity2_061_id_13` |
| `identity_v2:spec/603199b8030e` | 1 | 0 | `identity2_017_id_38` | — | `identity2_017_id_38` |
| `identity_v2:spec/60ed96a0e731` | 1 | 0 | `identity2_042_id_24` | — | `identity2_042_id_24` |
| `identity_v2:spec/60fc521e298b` | 1 | 0 | `identity2_008_id_39` | — | `identity2_008_id_39` |
| `identity_v2:spec/61292decd1a0` | 1 | 0 | `identity2_095_id_05` | — | `identity2_095_id_05` |
| `identity_v2:spec/622cfd5d3efd` | 1 | 0 | `identity2_019_id_25` | — | `identity2_019_id_25` |
| `identity_v2:spec/623ebd767c84` | 1 | 0 | `identity2_073_id_01` | — | `identity2_073_id_01` |
| `identity_v2:spec/625a721a4990` | 1 | 0 | `identity2_051_id_02` | — | `identity2_051_id_02` |
| `identity_v2:spec/625bed6d4271` | 1 | 0 | `identity2_085_id_00` | — | `identity2_085_id_00` |
| `identity_v2:spec/62bb3b5c58fd` | 1 | 0 | `identity2_062_id_15` | — | `identity2_062_id_15` |
| `identity_v2:spec/62cdc86caa4e` | 1 | 0 | `identity2_036_id_04` | — | `identity2_036_id_04` |
| `identity_v2:spec/6311f27e814e` | 1 | 0 | `identity2_088_id_03` | — | `identity2_088_id_03` |
| `identity_v2:spec/6348e42194a2` | 1 | 0 | `identity2_065_id_00` | — | `identity2_065_id_00` |
| `identity_v2:spec/639a943ab796` | 1 | 0 | `identity2_089_id_14` | — | `identity2_089_id_14` |
| `identity_v2:spec/63f882f92779` | 1 | 0 | `identity2_076_id_16` | — | `identity2_076_id_16` |
| `identity_v2:spec/655277519f0f` | 1 | 0 | `identity2_044_id_19` | — | `identity2_044_id_19` |
| `identity_v2:spec/65beffc278a8` | 1 | 0 | `identity2_009_id_33` | — | `identity2_009_id_33` |
| `identity_v2:spec/660aed9f907a` | 1 | 0 | `identity2_086_id_18` | — | `identity2_086_id_18` |
| `identity_v2:spec/66d96c4bb309` | 1 | 0 | `identity2_078_id_17` | — | `identity2_078_id_17` |
| `identity_v2:spec/673daeef9996` | 1 | 0 | `identity2_003_id_03` | — | `identity2_003_id_03` |
| `identity_v2:spec/67cd07529a31` | 1 | 0 | `identity2_070_id_04` | — | `identity2_070_id_04` |
| `identity_v2:spec/6848c023c37b` | 1 | 0 | `identity2_017_id_09` | — | `identity2_017_id_09` |
| `identity_v2:spec/68e3079a2bb1` | 1 | 0 | `identity2_036_id_08` | — | `identity2_036_id_08` |
| `identity_v2:spec/69c405a0b12e` | 1 | 0 | `identity2_025_id_16` | — | `identity2_025_id_16` |
| `identity_v2:spec/6a3ffc785a26` | 1 | 0 | `identity2_059_id_33` | — | `identity2_059_id_33` |
| `identity_v2:spec/6a88b9f897b3` | 1 | 0 | `identity2_058_id_22` | — | `identity2_058_id_22` |
| `identity_v2:spec/6a9e952ce300` | 1 | 0 | `identity2_060_id_23` | — | `identity2_060_id_23` |
| `identity_v2:spec/6b3401b4c783` | 1 | 0 | `identity2_028_id_24` | — | `identity2_028_id_24` |
| `identity_v2:spec/6bde4198a016` | 1 | 0 | `identity2_002_id_19` | — | `identity2_002_id_19` |
| `identity_v2:spec/6bfe070da48f` | 1 | 0 | `identity2_000_id_07` | — | `identity2_000_id_07` |
| `identity_v2:spec/6cb999df019b` | 1 | 0 | `identity2_078_id_08` | — | `identity2_078_id_08` |
| `identity_v2:spec/6cc846b9bed1` | 1 | 0 | `identity2_041_id_22` | — | `identity2_041_id_22` |
| `identity_v2:spec/6ce889488d43` | 2 | 0 | `identity2_000_id_06`, `identity2_090_id_09` | — | `identity2_000_id_06`, `identity2_090_id_09` |
| `identity_v2:spec/6d6fd0533f18` | 1 | 0 | `identity2_068_id_19` | — | `identity2_068_id_19` |
| `identity_v2:spec/6e6fbfcd54c9` | 1 | 0 | `identity2_094_id_19` | — | `identity2_094_id_19` |
| `identity_v2:spec/6eb4abbdd1ab` | 1 | 0 | `identity2_059_id_26` | — | `identity2_059_id_26` |
| `identity_v2:spec/6f458a8af129` | 1 | 0 | `identity2_013_id_01` | — | `identity2_013_id_01` |
| `identity_v2:spec/70e4ee6c3679` | 1 | 0 | `identity2_042_id_05` | — | `identity2_042_id_05` |
| `identity_v2:spec/71b635a49880` | 1 | 0 | `identity2_011_id_06` | — | `identity2_011_id_06` |
| `identity_v2:spec/7219d713f646` | 1 | 0 | `identity2_075_id_13` | — | `identity2_075_id_13` |
| `identity_v2:spec/7299e524250a` | 1 | 0 | `identity2_079_id_02` | — | `identity2_079_id_02` |
| `identity_v2:spec/733fecdd9630` | 1 | 0 | `identity2_023_id_13` | — | `identity2_023_id_13` |
| `identity_v2:spec/7411fc6e6533` | 1 | 0 | `identity2_001_id_06` | — | `identity2_001_id_06` |
| `identity_v2:spec/745f6455715e` | 1 | 0 | `identity2_045_id_06` | — | `identity2_045_id_06` |
| `identity_v2:spec/74b157fa686e` | 1 | 0 | `identity2_043_id_13` | — | `identity2_043_id_13` |
| `identity_v2:spec/74b7085c4dc4` | 1 | 0 | `identity2_035_id_07` | — | `identity2_035_id_07` |
| `identity_v2:spec/75450adbf848` | 1 | 0 | `identity2_013_id_39` | — | `identity2_013_id_39` |
| `identity_v2:spec/762cde4a80b9` | 1 | 0 | `identity2_043_id_38` | — | `identity2_043_id_38` |
| `identity_v2:spec/766bada74450` | 1 | 0 | `identity2_067_id_00` | — | `identity2_067_id_00` |
| `identity_v2:spec/766c4356c5b2` | 1 | 0 | `identity2_015_id_30` | — | `identity2_015_id_30` |
| `identity_v2:spec/76b897ae9d07` | 1 | 0 | `identity2_000_id_14` | — | `identity2_000_id_14` |
| `identity_v2:spec/76f64eb64dc5` | 1 | 0 | `identity2_095_id_19` | — | `identity2_095_id_19` |
| `identity_v2:spec/770d6007bdbc` | 1 | 0 | `identity2_007_id_18` | — | `identity2_007_id_18` |
| `identity_v2:spec/7766745a2866` | 1 | 0 | `identity2_060_id_22` | — | `identity2_060_id_22` |
| `identity_v2:spec/777378ceb6c8` | 1 | 0 | `identity2_003_id_13` | — | `identity2_003_id_13` |
| `identity_v2:spec/77c4d6233aa5` | 1 | 0 | `identity2_081_id_12` | — | `identity2_081_id_12` |
| `identity_v2:spec/78029f756b15` | 1 | 0 | `identity2_029_id_29` | — | `identity2_029_id_29` |
| `identity_v2:spec/782c246ee132` | 1 | 0 | `identity2_037_id_08` | — | `identity2_037_id_08` |
| `identity_v2:spec/78320e280271` | 1 | 0 | `identity2_044_id_03` | — | `identity2_044_id_03` |
| `identity_v2:spec/790b75c819db` | 1 | 0 | `identity2_040_id_03` | — | `identity2_040_id_03` |
| `identity_v2:spec/7957364bbc5c` | 1 | 0 | `identity2_013_id_12` | — | `identity2_013_id_12` |
| `identity_v2:spec/799341a99049` | 1 | 0 | `identity2_096_id_12` | — | `identity2_096_id_12` |
| `identity_v2:spec/79b5e9b3e4bb` | 1 | 0 | `identity2_085_id_13` | — | `identity2_085_id_13` |
| `identity_v2:spec/7af883fcd93f` | 1 | 0 | `identity2_046_id_16` | — | `identity2_046_id_16` |
| `identity_v2:spec/7b862e37cfe8` | 1 | 0 | `identity2_075_id_05` | — | `identity2_075_id_05` |
| `identity_v2:spec/7bcbbe2ca880` | 1 | 0 | `identity2_095_id_14` | — | `identity2_095_id_14` |
| `identity_v2:spec/7c942f615ee5` | 2 | 0 | `identity2_009_id_11`, `identity2_024_id_22` | — | `identity2_009_id_11`, `identity2_024_id_22` |
| `identity_v2:spec/7ce158f5d6dd` | 1 | 0 | `identity2_029_id_19` | — | `identity2_029_id_19` |
| `identity_v2:spec/7e274d2ab35f` | 1 | 0 | `identity2_009_id_32` | — | `identity2_009_id_32` |
| `identity_v2:spec/7e4862b26e1c` | 1 | 0 | `identity2_080_id_05` | — | `identity2_080_id_05` |
| `identity_v2:spec/7f233292f10e` | 1 | 0 | `identity2_086_id_16` | — | `identity2_086_id_16` |
| `identity_v2:spec/8016a4443c71` | 1 | 0 | `identity2_058_id_00` | — | `identity2_058_id_00` |
| `identity_v2:spec/8146d2afa2f5` | 1 | 0 | `identity2_095_id_07` | — | `identity2_095_id_07` |
| `identity_v2:spec/8197fb5bf4f1` | 1 | 0 | `identity2_018_id_14` | — | `identity2_018_id_14` |
| `identity_v2:spec/82e95f5b247f` | 1 | 0 | `identity2_010_id_29` | — | `identity2_010_id_29` |
| `identity_v2:spec/8302c78b5ecf` | 1 | 0 | `identity2_073_id_03` | — | `identity2_073_id_03` |
| `identity_v2:spec/83294198b682` | 1 | 0 | `identity2_026_id_15` | — | `identity2_026_id_15` |
| `identity_v2:spec/8380edb8bc8b` | 1 | 0 | `identity2_013_id_14` | — | `identity2_013_id_14` |
| `identity_v2:spec/8386634fdf16` | 1 | 0 | `identity2_043_id_12` | — | `identity2_043_id_12` |
| `identity_v2:spec/83993a59fc7c` | 1 | 0 | `identity2_018_id_10` | — | `identity2_018_id_10` |
| `identity_v2:spec/84fcfa6ac24d` | 1 | 0 | `identity2_013_id_19` | — | `identity2_013_id_19` |
| `identity_v2:spec/857af2b49a61` | 1 | 0 | `identity2_048_id_14` | — | `identity2_048_id_14` |
| `identity_v2:spec/858bdff684b5` | 1 | 0 | `identity2_026_id_01` | — | `identity2_026_id_01` |
| `identity_v2:spec/859b4dbbf501` | 1 | 0 | `identity2_048_id_04` | — | `identity2_048_id_04` |
| `identity_v2:spec/864d4ce9193c` | 1 | 0 | `identity2_081_id_07` | — | `identity2_081_id_07` |
| `identity_v2:spec/8797cb27de2e` | 1 | 0 | `identity2_068_id_02` | — | `identity2_068_id_02` |
| `identity_v2:spec/87a22a16543a` | 1 | 0 | `identity2_051_id_23` | — | `identity2_051_id_23` |
| `identity_v2:spec/87d91bb8dead` | 1 | 0 | `identity2_042_id_39` | — | `identity2_042_id_39` |
| `identity_v2:spec/8981443b24af` | 1 | 0 | `identity2_026_id_11` | — | `identity2_026_id_11` |
| `identity_v2:spec/8a4c47eeefff` | 1 | 0 | `identity2_049_id_11` | — | `identity2_049_id_11` |
| `identity_v2:spec/8a9f87494bd5` | 1 | 0 | `identity2_072_id_12` | — | `identity2_072_id_12` |
| `identity_v2:spec/8b4361e2a504` | 1 | 0 | `identity2_054_id_02` | — | `identity2_054_id_02` |
| `identity_v2:spec/8bbda5a1f14e` | 1 | 0 | `identity2_045_id_10` | — | `identity2_045_id_10` |
| `identity_v2:spec/8bee657a1fb6` | 1 | 0 | `identity2_024_id_13` | — | `identity2_024_id_13` |
| `identity_v2:spec/8bfc3ca1c784` | 1 | 0 | `identity2_033_id_25` | — | `identity2_033_id_25` |
| `identity_v2:spec/8c912a6aebdb` | 1 | 0 | `identity2_018_id_31` | — | `identity2_018_id_31` |
| `identity_v2:spec/8caac7acd163` | 2 | 0 | `identity2_015_id_11`, `identity2_079_id_00` | — | `identity2_015_id_11`, `identity2_079_id_00` |
| `identity_v2:spec/8d7e783ccc90` | 1 | 0 | `identity2_092_id_18` | — | `identity2_092_id_18` |
| `identity_v2:spec/8d88b267aff2` | 1 | 0 | `identity2_017_id_20` | — | `identity2_017_id_20` |
| `identity_v2:spec/8df62e41012a` | 1 | 0 | `identity2_096_id_06` | — | `identity2_096_id_06` |
| `identity_v2:spec/8e0158ea966a` | 1 | 0 | `identity2_041_id_39` | — | `identity2_041_id_39` |
| `identity_v2:spec/8e301965537b` | 1 | 0 | `identity2_029_id_11` | — | `identity2_029_id_11` |
| `identity_v2:spec/8f31639e276f` | 1 | 0 | `identity2_079_id_09` | — | `identity2_079_id_09` |
| `identity_v2:spec/8f9cc7c3b365` | 1 | 0 | `identity2_068_id_17` | — | `identity2_068_id_17` |
| `identity_v2:spec/907dc8c7ccd2` | 1 | 0 | `identity2_033_id_36` | — | `identity2_033_id_36` |
| `identity_v2:spec/9195ce8d1647` | 1 | 0 | `identity2_068_id_15` | — | `identity2_068_id_15` |
| `identity_v2:spec/91fab3b66ae0` | 1 | 0 | `identity2_040_id_04` | — | `identity2_040_id_04` |
| `identity_v2:spec/92951a7a0975` | 2 | 0 | `identity2_006_id_16`, `identity2_055_id_10` | — | `identity2_006_id_16`, `identity2_055_id_10` |
| `identity_v2:spec/92f353c65475` | 1 | 0 | `identity2_085_id_05` | — | `identity2_085_id_05` |
| `identity_v2:spec/92fe445e0fe5` | 1 | 0 | `identity2_083_id_13` | — | `identity2_083_id_13` |
| `identity_v2:spec/93056b86fb6d` | 1 | 0 | `identity2_094_id_15` | — | `identity2_094_id_15` |
| `identity_v2:spec/9311fb096cee` | 1 | 0 | `identity2_081_id_04` | — | `identity2_081_id_04` |
| `identity_v2:spec/93354cc7034e` | 1 | 0 | `identity2_093_id_13` | — | `identity2_093_id_13` |
| `identity_v2:spec/942b34bfa000` | 1 | 0 | `identity2_049_id_07` | — | `identity2_049_id_07` |
| `identity_v2:spec/9490deada80c` | 1 | 0 | `identity2_002_id_04` | — | `identity2_002_id_04` |
| `identity_v2:spec/9571af2bb7ab` | 1 | 0 | `identity2_038_id_19` | — | `identity2_038_id_19` |
| `identity_v2:spec/963d35400946` | 1 | 0 | `identity2_060_id_13` | — | `identity2_060_id_13` |
| `identity_v2:spec/970c414f93e1` | 1 | 0 | `identity2_088_id_06` | — | `identity2_088_id_06` |
| `identity_v2:spec/9750a6461a5f` | 1 | 0 | `identity2_013_id_30` | — | `identity2_013_id_30` |
| `identity_v2:spec/97828aaab5b7` | 1 | 0 | `identity2_059_id_38` | — | `identity2_059_id_38` |
| `identity_v2:spec/97da16e63bcb` | 1 | 0 | `identity2_010_id_19` | — | `identity2_010_id_19` |
| `identity_v2:spec/984e3ca4043b` | 1 | 0 | `identity2_005_id_08` | — | `identity2_005_id_08` |
| `identity_v2:spec/986504f4fca1` | 2 | 0 | `identity2_049_id_12`, `identity2_074_id_14` | — | `identity2_049_id_12`, `identity2_074_id_14` |
| `identity_v2:spec/987de9f15eec` | 1 | 0 | `identity2_076_id_15` | — | `identity2_076_id_15` |
| `identity_v2:spec/9894cb292cfe` | 1 | 0 | `identity2_089_id_04` | — | `identity2_089_id_04` |
| `identity_v2:spec/98b177eab7b6` | 1 | 0 | `identity2_086_id_05` | — | `identity2_086_id_05` |
| `identity_v2:spec/98ec0f067e3c` | 1 | 0 | `identity2_035_id_06` | — | `identity2_035_id_06` |
| `identity_v2:spec/9a168e29c15b` | 1 | 0 | `identity2_002_id_09` | — | `identity2_002_id_09` |
| `identity_v2:spec/9a19a70dc1c4` | 1 | 0 | `identity2_004_id_04` | — | `identity2_004_id_04` |
| `identity_v2:spec/9b1e080f99c9` | 1 | 0 | `identity2_080_id_04` | — | `identity2_080_id_04` |
| `identity_v2:spec/9b2b3fbed956` | 1 | 0 | `identity2_073_id_16` | — | `identity2_073_id_16` |
| `identity_v2:spec/9b44cbdfe54a` | 1 | 0 | `identity2_083_id_05` | — | `identity2_083_id_05` |
| `identity_v2:spec/9cb0432d17ac` | 1 | 0 | `identity2_052_id_20` | — | `identity2_052_id_20` |
| `identity_v2:spec/9cd5720e5785` | 1 | 0 | `identity2_036_id_23` | — | `identity2_036_id_23` |
| `identity_v2:spec/9cfb08a51cad` | 1 | 0 | `identity2_033_id_22` | — | `identity2_033_id_22` |
| `identity_v2:spec/9d09f8d74b4a` | 1 | 0 | `identity2_028_id_28` | — | `identity2_028_id_28` |
| `identity_v2:spec/9d0ce1aa85af` | 1 | 0 | `identity2_059_id_11` | — | `identity2_059_id_11` |
| `identity_v2:spec/9df271fae9bd` | 1 | 0 | `identity2_072_id_17` | — | `identity2_072_id_17` |
| `identity_v2:spec/9e4994ef1a01` | 1 | 0 | `identity2_051_id_03` | — | `identity2_051_id_03` |
| `identity_v2:spec/9f5badb48104` | 1 | 0 | `identity2_025_id_21` | — | `identity2_025_id_21` |
| `identity_v2:spec/9fdf5a542e40` | 1 | 0 | `identity2_046_id_30` | — | `identity2_046_id_30` |
| `identity_v2:spec/9feeca12f184` | 1 | 0 | `identity2_033_id_17` | — | `identity2_033_id_17` |
| `identity_v2:spec/a019d391f869` | 1 | 0 | `identity2_039_id_02` | — | `identity2_039_id_02` |
| `identity_v2:spec/a056e51fe51a` | 1 | 0 | `identity2_033_id_37` | — | `identity2_033_id_37` |
| `identity_v2:spec/a06f4526d9d7` | 1 | 0 | `identity2_042_id_33` | — | `identity2_042_id_33` |
| `identity_v2:spec/a0b499b95516` | 1 | 0 | `identity2_046_id_23` | — | `identity2_046_id_23` |
| `identity_v2:spec/a0b7383d24c1` | 1 | 0 | `identity2_038_id_24` | — | `identity2_038_id_24` |
| `identity_v2:spec/a11e1b8aa0b2` | 1 | 0 | `identity2_083_id_15` | — | `identity2_083_id_15` |
| `identity_v2:spec/a18b9954de64` | 1 | 0 | `identity2_027_id_31` | — | `identity2_027_id_31` |
| `identity_v2:spec/a1ad3f98ed90` | 1 | 0 | `identity2_086_id_09` | — | `identity2_086_id_09` |
| `identity_v2:spec/a1e4c198bc09` | 1 | 0 | `identity2_026_id_17` | — | `identity2_026_id_17` |
| `identity_v2:spec/a22805f1ead5` | 1 | 0 | `identity2_081_id_06` | — | `identity2_081_id_06` |
| `identity_v2:spec/a228b731d707` | 1 | 0 | `identity2_091_id_02` | — | `identity2_091_id_02` |
| `identity_v2:spec/a2cfaa1d092d` | 1 | 0 | `identity2_068_id_14` | — | `identity2_068_id_14` |
| `identity_v2:spec/a2dd6ba350e6` | 1 | 0 | `identity2_033_id_19` | — | `identity2_033_id_19` |
| `identity_v2:spec/a3243364ddb2` | 1 | 0 | `identity2_008_id_24` | — | `identity2_008_id_24` |
| `identity_v2:spec/a3a4ed220830` | 1 | 0 | `identity2_022_id_00` | — | `identity2_022_id_00` |
| `identity_v2:spec/a51e87fb9fbf` | 1 | 0 | `identity2_007_id_19` | — | `identity2_007_id_19` |
| `identity_v2:spec/a555ba9bbf47` | 1 | 0 | `identity2_045_id_09` | — | `identity2_045_id_09` |
| `identity_v2:spec/a5f7df7d889d` | 1 | 0 | `identity2_015_id_15` | — | `identity2_015_id_15` |
| `identity_v2:spec/a66d1d6416ca` | 1 | 0 | `identity2_027_id_01` | — | `identity2_027_id_01` |
| `identity_v2:spec/a6b28e11fe8d` | 1 | 0 | `identity2_024_id_35` | — | `identity2_024_id_35` |
| `identity_v2:spec/a734922240cf` | 1 | 0 | `identity2_092_id_01` | — | `identity2_092_id_01` |
| `identity_v2:spec/a78eeeb2eaf2` | 1 | 0 | `identity2_040_id_01` | — | `identity2_040_id_01` |
| `identity_v2:spec/a8244931888d` | 1 | 0 | `identity2_016_id_37` | — | `identity2_016_id_37` |
| `identity_v2:spec/a8a8f1b4f72a` | 1 | 0 | `identity2_017_id_22` | — | `identity2_017_id_22` |
| `identity_v2:spec/a99f5c0572e9` | 1 | 0 | `identity2_058_id_17` | — | `identity2_058_id_17` |
| `identity_v2:spec/aa6a6cb348c3` | 1 | 0 | `identity2_080_id_01` | — | `identity2_080_id_01` |
| `identity_v2:spec/aae6401c186d` | 1 | 0 | `identity2_006_id_12` | — | `identity2_006_id_12` |
| `identity_v2:spec/ab5b417c105e` | 1 | 0 | `identity2_020_id_13` | — | `identity2_020_id_13` |
| `identity_v2:spec/abc2ae1cea7f` | 1 | 0 | `identity2_051_id_29` | — | `identity2_051_id_29` |
| `identity_v2:spec/ac07deb4f458` | 1 | 0 | `identity2_048_id_09` | — | `identity2_048_id_09` |
| `identity_v2:spec/ac71d372b4ce` | 1 | 0 | `identity2_055_id_01` | — | `identity2_055_id_01` |
| `identity_v2:spec/acbcd6573a0c` | 1 | 0 | `identity2_008_id_05` | — | `identity2_008_id_05` |
| `identity_v2:spec/ad1454aa6b75` | 1 | 0 | `identity2_027_id_24` | — | `identity2_027_id_24` |
| `identity_v2:spec/ad7b7ab234e4` | 1 | 0 | `identity2_018_id_00` | — | `identity2_018_id_00` |
| `identity_v2:spec/ae6582b0797a` | 1 | 0 | `identity2_009_id_21` | — | `identity2_009_id_21` |
| `identity_v2:spec/afef6794b3b1` | 1 | 0 | `identity2_035_id_05` | — | `identity2_035_id_05` |
| `identity_v2:spec/b0bb8a15ddd4` | 1 | 0 | `identity2_028_id_25` | — | `identity2_028_id_25` |
| `identity_v2:spec/b1f6895d48b3` | 1 | 0 | `identity2_062_id_13` | — | `identity2_062_id_13` |
| `identity_v2:spec/b20fe76f34ee` | 1 | 0 | `identity2_020_id_20` | — | `identity2_020_id_20` |
| `identity_v2:spec/b2a75bd96ac5` | 1 | 0 | `identity2_088_id_02` | — | `identity2_088_id_02` |
| `identity_v2:spec/b2f68dd376a1` | 1 | 0 | `identity2_015_id_33` | — | `identity2_015_id_33` |
| `identity_v2:spec/b316330f3086` | 1 | 0 | `identity2_069_id_14` | — | `identity2_069_id_14` |
| `identity_v2:spec/b3715c550028` | 2 | 0 | `identity2_001_id_14`, `identity2_066_id_12` | — | `identity2_001_id_14`, `identity2_066_id_12` |
| `identity_v2:spec/b3cd46fc7a4c` | 1 | 0 | `identity2_033_id_28` | — | `identity2_033_id_28` |
| `identity_v2:spec/b4417f0c3358` | 1 | 0 | `identity2_004_id_07` | — | `identity2_004_id_07` |
| `identity_v2:spec/b46900846212` | 2 | 0 | `identity2_013_id_23`, `identity2_088_id_08` | — | `identity2_013_id_23`, `identity2_088_id_08` |
| `identity_v2:spec/b47c06898e71` | 1 | 0 | `identity2_077_id_19` | — | `identity2_077_id_19` |
| `identity_v2:spec/b529da7cde32` | 2 | 0 | `identity2_026_id_39`, `identity2_080_id_08` | — | `identity2_026_id_39`, `identity2_080_id_08` |
| `identity_v2:spec/b547f312a1ab` | 1 | 0 | `identity2_026_id_31` | — | `identity2_026_id_31` |
| `identity_v2:spec/b54ef898547c` | 1 | 0 | `identity2_085_id_08` | — | `identity2_085_id_08` |
| `identity_v2:spec/b63bc2ae7edc` | 1 | 0 | `identity2_076_id_19` | — | `identity2_076_id_19` |
| `identity_v2:spec/b674331b1a85` | 1 | 0 | `identity2_070_id_18` | — | `identity2_070_id_18` |
| `identity_v2:spec/b69d43a891a3` | 1 | 0 | `identity2_028_id_05` | — | `identity2_028_id_05` |
| `identity_v2:spec/b6aa205dbe65` | 1 | 0 | `identity2_021_id_39` | — | `identity2_021_id_39` |
| `identity_v2:spec/b6dc7ae2c907` | 1 | 0 | `identity2_091_id_14` | — | `identity2_091_id_14` |
| `identity_v2:spec/b724c03f184e` | 1 | 0 | `identity2_075_id_11` | — | `identity2_075_id_11` |
| `identity_v2:spec/b7777ede8fe6` | 1 | 0 | `identity2_029_id_00` | — | `identity2_029_id_00` |
| `identity_v2:spec/b7950311bf6c` | 1 | 0 | `identity2_015_id_07` | — | `identity2_015_id_07` |
| `identity_v2:spec/b8325be0f408` | 1 | 0 | `identity2_064_id_02` | — | `identity2_064_id_02` |
| `identity_v2:spec/b8bc2337db85` | 1 | 0 | `identity2_094_id_12` | — | `identity2_094_id_12` |
| `identity_v2:spec/b8f90f5c8cde` | 1 | 0 | `identity2_035_id_14` | — | `identity2_035_id_14` |
| `identity_v2:spec/ba5e629603bd` | 1 | 0 | `identity2_023_id_08` | — | `identity2_023_id_08` |
| `identity_v2:spec/ba6f8435125a` | 1 | 0 | `identity2_017_id_30` | — | `identity2_017_id_30` |
| `identity_v2:spec/bb5b783e132c` | 1 | 0 | `identity2_064_id_11` | — | `identity2_064_id_11` |
| `identity_v2:spec/bc32361a83e2` | 1 | 0 | `identity2_011_id_02` | — | `identity2_011_id_02` |
| `identity_v2:spec/bc938765dd00` | 1 | 0 | `identity2_049_id_04` | — | `identity2_049_id_04` |
| `identity_v2:spec/bcc2aa247d46` | 1 | 0 | `identity2_070_id_14` | — | `identity2_070_id_14` |
| `identity_v2:spec/bce2aa943698` | 1 | 0 | `identity2_078_id_02` | — | `identity2_078_id_02` |
| `identity_v2:spec/bd538636fb92` | 1 | 0 | `identity2_025_id_10` | — | `identity2_025_id_10` |
| `identity_v2:spec/bda6c9ef88f6` | 1 | 0 | `identity2_036_id_24` | — | `identity2_036_id_24` |
| `identity_v2:spec/be05258e38aa` | 1 | 0 | `identity2_020_id_04` | — | `identity2_020_id_04` |
| `identity_v2:spec/beb6be7b80eb` | 1 | 0 | `identity2_028_id_14` | — | `identity2_028_id_14` |
| `identity_v2:spec/bedb772c6d4a` | 1 | 0 | `identity2_006_id_19` | — | `identity2_006_id_19` |
| `identity_v2:spec/bf4e9fc444e2` | 1 | 0 | `identity2_093_id_08` | — | `identity2_093_id_08` |
| `identity_v2:spec/c186a0b80a89` | 1 | 0 | `identity2_009_id_16` | — | `identity2_009_id_16` |
| `identity_v2:spec/c2aa5c25bbd4` | 1 | 0 | `identity2_006_id_07` | — | `identity2_006_id_07` |
| `identity_v2:spec/c3e74ecd12c1` | 1 | 0 | `identity2_063_id_04` | — | `identity2_063_id_04` |
| `identity_v2:spec/c40b7cbbffdd` | 1 | 0 | `identity2_092_id_13` | — | `identity2_092_id_13` |
| `identity_v2:spec/c4a22f106a53` | 1 | 0 | `identity2_069_id_06` | — | `identity2_069_id_06` |
| `identity_v2:spec/c4f1a921a75c` | 1 | 0 | `identity2_019_id_13` | — | `identity2_019_id_13` |
| `identity_v2:spec/c6998690289d` | 1 | 0 | `identity2_081_id_19` | — | `identity2_081_id_19` |
| `identity_v2:spec/c818f03dfc59` | 1 | 0 | `identity2_060_id_39` | — | `identity2_060_id_39` |
| `identity_v2:spec/c8c62c4dd94c` | 1 | 0 | `identity2_081_id_18` | — | `identity2_081_id_18` |
| `identity_v2:spec/c917e7705f4e` | 1 | 0 | `identity2_083_id_12` | — | `identity2_083_id_12` |
| `identity_v2:spec/ca758b872dee` | 1 | 0 | `identity2_096_id_02` | — | `identity2_096_id_02` |
| `identity_v2:spec/cb54179e60a3` | 1 | 0 | `identity2_023_id_16` | — | `identity2_023_id_16` |
| `identity_v2:spec/cb6c1c2ae254` | 1 | 0 | `identity2_026_id_22` | — | `identity2_026_id_22` |
| `identity_v2:spec/cb7f113e7d98` | 1 | 0 | `identity2_033_id_14` | — | `identity2_033_id_14` |
| `identity_v2:spec/cbb08d9a338f` | 1 | 0 | `identity2_024_id_37` | — | `identity2_024_id_37` |
| `identity_v2:spec/cc1d37f5c79d` | 1 | 0 | `identity2_046_id_36` | — | `identity2_046_id_36` |
| `identity_v2:spec/cc216ac9e8c3` | 1 | 0 | `identity2_001_id_29` | — | `identity2_001_id_29` |
| `identity_v2:spec/cd41e716285b` | 1 | 0 | `identity2_028_id_08` | — | `identity2_028_id_08` |
| `identity_v2:spec/cd474a04abf0` | 1 | 0 | `identity2_090_id_05` | — | `identity2_090_id_05` |
| `identity_v2:spec/cd71d5290e2b` | 1 | 0 | `identity2_013_id_16` | — | `identity2_013_id_16` |
| `identity_v2:spec/ce480b4c411a` | 1 | 0 | `identity2_051_id_33` | — | `identity2_051_id_33` |
| `identity_v2:spec/ceb7dc9f2b34` | 1 | 0 | `identity2_013_id_07` | — | `identity2_013_id_07` |
| `identity_v2:spec/cebe2287213d` | 1 | 0 | `identity2_083_id_18` | — | `identity2_083_id_18` |
| `identity_v2:spec/ced77b2fecbf` | 1 | 0 | `identity2_078_id_10` | — | `identity2_078_id_10` |
| `identity_v2:spec/cef2c188ee1b` | 1 | 0 | `identity2_048_id_00` | — | `identity2_048_id_00` |
| `identity_v2:spec/cf858dff1cf2` | 1 | 0 | `identity2_066_id_05` | — | `identity2_066_id_05` |
| `identity_v2:spec/cf9852642961` | 1 | 0 | `identity2_020_id_21` | — | `identity2_020_id_21` |
| `identity_v2:spec/cf9ca08e94bd` | 1 | 0 | `identity2_058_id_37` | — | `identity2_058_id_37` |
| `identity_v2:spec/cfe56f0170af` | 1 | 0 | `identity2_051_id_14` | — | `identity2_051_id_14` |
| `identity_v2:spec/d10e47f34793` | 1 | 0 | `identity2_062_id_10` | — | `identity2_062_id_10` |
| `identity_v2:spec/d128cd97f6c9` | 1 | 0 | `identity2_006_id_21` | — | `identity2_006_id_21` |
| `identity_v2:spec/d1d9a9a7e6e7` | 1 | 0 | `identity2_087_id_10` | — | `identity2_087_id_10` |
| `identity_v2:spec/d2837346c7ac` | 1 | 0 | `identity2_042_id_11` | — | `identity2_042_id_11` |
| `identity_v2:spec/d2bedba5f59e` | 1 | 0 | `identity2_046_id_15` | — | `identity2_046_id_15` |
| `identity_v2:spec/d3aa0fddf458` | 1 | 0 | `identity2_064_id_14` | — | `identity2_064_id_14` |
| `identity_v2:spec/d3afecab26ad` | 1 | 0 | `identity2_066_id_17` | — | `identity2_066_id_17` |
| `identity_v2:spec/d3e70a5c6e89` | 1 | 0 | `identity2_074_id_17` | — | `identity2_074_id_17` |
| `identity_v2:spec/d48ca7639a04` | 1 | 0 | `identity2_018_id_29` | — | `identity2_018_id_29` |
| `identity_v2:spec/d5012c3a4a3c` | 1 | 0 | `identity2_004_id_02` | — | `identity2_004_id_02` |
| `identity_v2:spec/d52dbd603a82` | 1 | 0 | `identity2_049_id_01` | — | `identity2_049_id_01` |
| `identity_v2:spec/d541112e5c10` | 1 | 0 | `identity2_052_id_03` | — | `identity2_052_id_03` |
| `identity_v2:spec/d590b3e43187` | 1 | 0 | `identity2_092_id_17` | — | `identity2_092_id_17` |
| `identity_v2:spec/d5cc1eb7688a` | 1 | 0 | `identity2_022_id_01` | — | `identity2_022_id_01` |
| `identity_v2:spec/d69c1b4d0bf8` | 1 | 0 | `identity2_021_id_04` | — | `identity2_021_id_04` |
| `identity_v2:spec/d6acb4de0f4b` | 1 | 0 | `identity2_089_id_11` | — | `identity2_089_id_11` |
| `identity_v2:spec/d7491780822e` | 1 | 0 | `identity2_001_id_22` | — | `identity2_001_id_22` |
| `identity_v2:spec/d778bccb4e9d` | 1 | 0 | `identity2_033_id_23` | — | `identity2_033_id_23` |
| `identity_v2:spec/d78f4b10ae00` | 1 | 0 | `identity2_013_id_36` | — | `identity2_013_id_36` |
| `identity_v2:spec/d8668a94db53` | 1 | 0 | `identity2_029_id_05` | — | `identity2_029_id_05` |
| `identity_v2:spec/d8819108a768` | 1 | 0 | `identity2_037_id_13` | — | `identity2_037_id_13` |
| `identity_v2:spec/d95eaa28de18` | 1 | 0 | `identity2_060_id_17` | — | `identity2_060_id_17` |
| `identity_v2:spec/d98228b5f527` | 1 | 0 | `identity2_073_id_12` | — | `identity2_073_id_12` |
| `identity_v2:spec/da67ec4ec033` | 1 | 0 | `identity2_028_id_18` | — | `identity2_028_id_18` |
| `identity_v2:spec/dba6972679d4` | 2 | 0 | `identity2_051_id_13`, `identity2_064_id_12` | — | `identity2_051_id_13`, `identity2_064_id_12` |
| `identity_v2:spec/dc67b36e3bae` | 1 | 0 | `identity2_079_id_07` | — | `identity2_079_id_07` |
| `identity_v2:spec/dc932eff7d16` | 1 | 0 | `identity2_000_id_24` | — | `identity2_000_id_24` |
| `identity_v2:spec/dcd2d33c23fb` | 1 | 0 | `identity2_082_id_16` | — | `identity2_082_id_16` |
| `identity_v2:spec/dd449bd30b3b` | 1 | 0 | `identity2_067_id_17` | — | `identity2_067_id_17` |
| `identity_v2:spec/dd454fbab1ed` | 1 | 0 | `identity2_087_id_15` | — | `identity2_087_id_15` |
| `identity_v2:spec/dde86a021a43` | 1 | 0 | `identity2_033_id_27` | — | `identity2_033_id_27` |
| `identity_v2:spec/de69caca8518` | 1 | 0 | `identity2_002_id_14` | — | `identity2_002_id_14` |
| `identity_v2:spec/de93cd0f1e05` | 1 | 0 | `identity2_078_id_13` | — | `identity2_078_id_13` |
| `identity_v2:spec/de93f3c4728f` | 1 | 0 | `identity2_059_id_07` | — | `identity2_059_id_07` |
| `identity_v2:spec/deef16234525` | 1 | 0 | `identity2_044_id_23` | — | `identity2_044_id_23` |
| `identity_v2:spec/df66adca6149` | 1 | 0 | `identity2_040_id_00` | — | `identity2_040_id_00` |
| `identity_v2:spec/e0e3ce8a5563` | 1 | 0 | `identity2_029_id_08` | — | `identity2_029_id_08` |
| `identity_v2:spec/e115cc9660ef` | 1 | 0 | `identity2_000_id_02` | — | `identity2_000_id_02` |
| `identity_v2:spec/e1320b76aecc` | 1 | 0 | `identity2_039_id_23` | — | `identity2_039_id_23` |
| `identity_v2:spec/e1466cddbe78` | 1 | 0 | `identity2_052_id_11` | — | `identity2_052_id_11` |
| `identity_v2:spec/e1670ab89c9b` | 1 | 0 | `identity2_058_id_16` | — | `identity2_058_id_16` |
| `identity_v2:spec/e31ff811be43` | 1 | 0 | `identity2_048_id_08` | — | `identity2_048_id_08` |
| `identity_v2:spec/e391924a98af` | 1 | 0 | `identity2_025_id_09` | — | `identity2_025_id_09` |
| `identity_v2:spec/e4844e482cce` | 1 | 0 | `identity2_055_id_17` | — | `identity2_055_id_17` |
| `identity_v2:spec/e49b6ec67d26` | 1 | 0 | `identity2_024_id_15` | — | `identity2_024_id_15` |
| `identity_v2:spec/e687e54d2915` | 1 | 0 | `identity2_016_id_02` | — | `identity2_016_id_02` |
| `identity_v2:spec/e6c0061f00c7` | 1 | 0 | `identity2_060_id_36` | — | `identity2_060_id_36` |
| `identity_v2:spec/e6fd0e05fb3a` | 1 | 0 | `identity2_038_id_13` | — | `identity2_038_id_13` |
| `identity_v2:spec/e7bb8ac001a4` | 1 | 0 | `identity2_044_id_26` | — | `identity2_044_id_26` |
| `identity_v2:spec/e7cd3e56416f` | 1 | 0 | `identity2_086_id_06` | — | `identity2_086_id_06` |
| `identity_v2:spec/e7d8d84d9012` | 1 | 0 | `identity2_010_id_05` | — | `identity2_010_id_05` |
| `identity_v2:spec/e815655be614` | 1 | 0 | `identity2_051_id_17` | — | `identity2_051_id_17` |
| `identity_v2:spec/e828eb3c9279` | 1 | 0 | `identity2_080_id_09` | — | `identity2_080_id_09` |
| `identity_v2:spec/e8bd70e601c7` | 1 | 0 | `identity2_015_id_23` | — | `identity2_015_id_23` |
| `identity_v2:spec/ea124e515774` | 1 | 0 | `identity2_029_id_10` | — | `identity2_029_id_10` |
| `identity_v2:spec/ea3678ce9344` | 1 | 0 | `identity2_005_id_19` | — | `identity2_005_id_19` |
| `identity_v2:spec/ead775d1e19c` | 1 | 0 | `identity2_066_id_01` | — | `identity2_066_id_01` |
| `identity_v2:spec/eb19ddff59c2` | 1 | 0 | `identity2_012_id_08` | — | `identity2_012_id_08` |
| `identity_v2:spec/ebaabea278de` | 1 | 0 | `identity2_055_id_04` | — | `identity2_055_id_04` |
| `identity_v2:spec/ebe52b426564` | 1 | 0 | `identity2_028_id_09` | — | `identity2_028_id_09` |
| `identity_v2:spec/ec04d3735433` | 1 | 0 | `identity2_059_id_21` | — | `identity2_059_id_21` |
| `identity_v2:spec/ec40f1d60666` | 1 | 0 | `identity2_043_id_08` | — | `identity2_043_id_08` |
| `identity_v2:spec/ed0ae402a4d0` | 1 | 0 | `identity2_027_id_33` | — | `identity2_027_id_33` |
| `identity_v2:spec/ed4564e4334b` | 1 | 0 | `identity2_033_id_33` | — | `identity2_033_id_33` |
| `identity_v2:spec/edf3eb1be947` | 1 | 0 | `identity2_025_id_15` | — | `identity2_025_id_15` |
| `identity_v2:spec/ee71edd7ff66` | 1 | 0 | `identity2_025_id_20` | — | `identity2_025_id_20` |
| `identity_v2:spec/eed7305fd648` | 1 | 0 | `identity2_076_id_04` | — | `identity2_076_id_04` |
| `identity_v2:spec/ef506ea5e1ed` | 1 | 0 | `identity2_016_id_11` | — | `identity2_016_id_11` |
| `identity_v2:spec/ef793ae43fef` | 1 | 0 | `identity2_064_id_16` | — | `identity2_064_id_16` |
| `identity_v2:spec/efb2010afc9a` | 1 | 0 | `identity2_088_id_19` | — | `identity2_088_id_19` |
| `identity_v2:spec/f001aa9f2203` | 1 | 0 | `identity2_009_id_28` | — | `identity2_009_id_28` |
| `identity_v2:spec/f0d8e3a58c19` | 1 | 0 | `identity2_002_id_26` | — | `identity2_002_id_26` |
| `identity_v2:spec/f14f42017567` | 1 | 0 | `identity2_000_id_37` | — | `identity2_000_id_37` |
| `identity_v2:spec/f159dd64c37a` | 1 | 0 | `identity2_018_id_18` | — | `identity2_018_id_18` |
| `identity_v2:spec/f185db663b47` | 1 | 0 | `identity2_025_id_30` | — | `identity2_025_id_30` |
| `identity_v2:spec/f23632880094` | 1 | 0 | `identity2_081_id_01` | — | `identity2_081_id_01` |
| `identity_v2:spec/f23e62488990` | 1 | 0 | `identity2_091_id_04` | — | `identity2_091_id_04` |
| `identity_v2:spec/f2586bcc5c2b` | 1 | 0 | `identity2_042_id_19` | — | `identity2_042_id_19` |
| `identity_v2:spec/f2e293ae2508` | 1 | 0 | `identity2_085_id_04` | — | `identity2_085_id_04` |
| `identity_v2:spec/f2ee1d02d2b4` | 1 | 0 | `identity2_026_id_12` | — | `identity2_026_id_12` |
| `identity_v2:spec/f36890e235c0` | 1 | 0 | `identity2_010_id_21` | — | `identity2_010_id_21` |
| `identity_v2:spec/f36f19e6f4c9` | 1 | 0 | `identity2_000_id_13` | — | `identity2_000_id_13` |
| `identity_v2:spec/f3999ffc8f28` | 1 | 0 | `identity2_051_id_39` | — | `identity2_051_id_39` |
| `identity_v2:spec/f504a473fce3` | 1 | 0 | `identity2_041_id_38` | — | `identity2_041_id_38` |
| `identity_v2:spec/f552761d1ccd` | 1 | 0 | `identity2_040_id_23` | — | `identity2_040_id_23` |
| `identity_v2:spec/f5a316d72cae` | 1 | 0 | `identity2_046_id_38` | — | `identity2_046_id_38` |
| `identity_v2:spec/f601752443d3` | 1 | 0 | `identity2_060_id_31` | — | `identity2_060_id_31` |
| `identity_v2:spec/f60bc0b79272` | 1 | 0 | `identity2_079_id_10` | — | `identity2_079_id_10` |
| `identity_v2:spec/f63cb5298a7c` | 1 | 0 | `identity2_041_id_27` | — | `identity2_041_id_27` |
| `identity_v2:spec/f6466f7b61b8` | 1 | 0 | `identity2_019_id_37` | — | `identity2_019_id_37` |
| `identity_v2:spec/f753f45745e4` | 1 | 0 | `identity2_048_id_25` | — | `identity2_048_id_25` |
| `identity_v2:spec/f7cdbd37c603` | 1 | 0 | `identity2_051_id_24` | — | `identity2_051_id_24` |
| `identity_v2:spec/f7de56498a41` | 1 | 0 | `identity2_030_id_14` | — | `identity2_030_id_14` |
| `identity_v2:spec/f8119b8f03ce` | 1 | 0 | `identity2_046_id_25` | — | `identity2_046_id_25` |
| `identity_v2:spec/f8907ad1bd67` | 1 | 0 | `identity2_059_id_05` | — | `identity2_059_id_05` |
| `identity_v2:spec/f8e1d57a90c5` | 1 | 0 | `identity2_014_id_06` | — | `identity2_014_id_06` |
| `identity_v2:spec/f932be028ede` | 1 | 0 | `identity2_065_id_09` | — | `identity2_065_id_09` |
| `identity_v2:spec/f96347675692` | 1 | 0 | `identity2_066_id_13` | — | `identity2_066_id_13` |
| `identity_v2:spec/fa9738c6e47b` | 1 | 0 | `identity2_001_id_27` | — | `identity2_001_id_27` |
| `identity_v2:spec/fabbce3efc68` | 1 | 0 | `identity2_061_id_15` | — | `identity2_061_id_15` |
| `identity_v2:spec/fb07da8cf618` | 1 | 0 | `identity2_040_id_22` | — | `identity2_040_id_22` |
| `identity_v2:spec/fbf14b63af84` | 1 | 0 | `identity2_026_id_14` | — | `identity2_026_id_14` |
| `identity_v2:spec/fbf45859c80d` | 1 | 0 | `identity2_046_id_39` | — | `identity2_046_id_39` |
| `identity_v2:spec/fc4ec3201462` | 1 | 0 | `identity2_074_id_08` | — | `identity2_074_id_08` |
| `identity_v2:spec/fc8624f68f4d` | 1 | 0 | `identity2_016_id_32` | — | `identity2_016_id_32` |
| `identity_v2:spec/fd5f0367b653` | 1 | 0 | `identity2_029_id_34` | — | `identity2_029_id_34` |
| `identity_v2:spec/fda839ba5391` | 1 | 0 | `identity2_008_id_08` | — | `identity2_008_id_08` |
| `identity_v2:spec/fe6094b10cbd` | 1 | 0 | `identity2_003_id_09` | — | `identity2_003_id_09` |
| `identity_v2:spec/ff42322d4402` | 1 | 0 | `identity2_042_id_09` | — | `identity2_042_id_09` |
| `identity_v2:spec/ffed044fbcd0` | 1 | 0 | `identity2_005_id_02` | — | `identity2_005_id_02` |
| `lasr:t1_b00_s000` | 1 | 1 | `sft_bacb216955` | `doc_9a8cb61291` | `sft_bacb216955` |
| `lasr:t1_b00_s002` | 1 | 0 | `sft_7376378b9c` | — | `sft_7376378b9c` |
| `lasr:t1_b03_s007` | 0 | 1 | — | `doc_5445e73350` | `sft_70ad87b0ae` |
| `lasr:t1_b04_s000` | 1 | 0 | `sft_6be92d4b55` | — | `sft_6be92d4b55` |
| `lasr:t1_b04_s006` | 0 | 1 | — | `doc_db655b2f3a` | `sft_a451e68729` |
| `lasr:t1_b05_s002` | 1 | 1 | `sft_8cdb7b108c` | `doc_ffeac78842` | `sft_8cdb7b108c` |
| `lasr:t1_b05_s005` | 1 | 0 | `sft_a6c85b977f` | — | `sft_a6c85b977f` |
| `lasr:t1_b06_s004` | 1 | 0 | `sft_250c8ab52a` | — | `sft_250c8ab52a` |
| `lasr:t1_b07_s002` | 1 | 0 | `sft_d915bede9d` | — | `sft_d915bede9d` |
| `lasr:t1_b08_s003` | 1 | 0 | `sft_8bb8ae184d` | — | `sft_8bb8ae184d` |
| `lasr:t1_b11_s002` | 1 | 0 | `sft_777cab6d3d` | — | `sft_777cab6d3d` |
| `lasr:t1_b14_s005` | 1 | 0 | `sft_35bfdd7a3c` | — | `sft_35bfdd7a3c` |
| `lasr:t1_b15_s003` | 1 | 0 | `sft_c5a93beaba` | — | `sft_c5a93beaba` |
| `lasr:t1_b16_s007` | 1 | 1 | `sft_c9ac11d2e8` | `doc_ea257a9c3f` | `sft_c9ac11d2e8` |
| `lasr:t1_b19_s002` | 1 | 1 | `sft_248c76e6fd` | `doc_f4dfde857a` | `sft_248c76e6fd` |
| `lasr:t1_b20_s000` | 1 | 1 | `sft_b3c2a521e8` | `doc_f9ac83d18f` | `sft_b3c2a521e8` |
| `lasr:t1_b20_s001` | 1 | 0 | `prop_60501e3a6b` | — | `prop_60501e3a6b` |
| `lasr:t1_b20_s002` | 1 | 1 | `sft_f8e4a36e13` | `doc_5a64ef4f0b` | `sft_f8e4a36e13` |
| `lasr:t1_b21_s006` | 1 | 0 | `sft_13f79efd27` | — | `sft_13f79efd27` |
| `lasr:t1_b28_s006` | 1 | 0 | `prop_1d83225e63` | — | `prop_1d83225e63` |
| `lasr:t1_b30_s003` | 0 | 1 | — | `doc_9c88bb4241` | `sft_8723d27a57` |
| `lasr:t2_b00_s004` | 1 | 0 | `prop_1b7e3a7b92` | — | `prop_1b7e3a7b92` |
| `lasr:t2_b00_s005` | 1 | 0 | `sft_5e828af825` | — | `sft_5e828af825` |
| `lasr:t2_b05_s006` | 1 | 1 | `sft_3ed6f9042b` | `doc_4ed62d2828` | `sft_3ed6f9042b` |
| `lasr:t2_b06_s000` | 0 | 1 | — | `doc_505b3ac6eb` | `sft_e594c5b5db` |
| `lasr:t2_b07_s002` | 1 | 0 | `sft_8d60da332e` | — | `sft_8d60da332e` |
| `lasr:t2_b07_s005` | 1 | 1 | `sft_2472da6d98` | `doc_1f5aa4eac6` | `sft_2472da6d98` |
| `lasr:t2_b09_s003` | 1 | 0 | `sft_2a5cee17c1` | — | `sft_2a5cee17c1` |
| `lasr:t2_b09_s006` | 0 | 1 | — | `doc_baf76e1de7` | `sft_56e503a6a3` |
| `lasr:t2_b10_s001` | 0 | 1 | — | `doc_42104fe605` | `sft_29190f4f69` |
| `lasr:t2_b11_s002` | 1 | 1 | `sft_7b9c60bf54` | `doc_032c798906` | `sft_7b9c60bf54` |
| `lasr:t2_b12_s002` | 0 | 1 | — | `doc_a4a32f2846` | `sft_2c192f2ffc` |
| `lasr:t2_b12_s003` | 2 | 0 | `sft0005`, `sft_43d156deb3` | — | `sft0005`, `sft_43d156deb3` |
| `lasr:t2_b13_s002` | 1 | 1 | `sft_824af1a07c` | `doc_116dbbec26` | `sft_824af1a07c` |
| `lasr:t2_b18_s001` | 1 | 0 | `prop_878df8167f` | — | `prop_878df8167f` |
| `lasr:t2_b18_s002` | 1 | 0 | `sft_bf2698cb43` | — | `sft_bf2698cb43` |
| `lasr:t2_b18_s003` | 1 | 1 | `sft_751c8b5a2b` | `doc_a277ea3185` | `sft_751c8b5a2b` |
| `lasr:t2_b19_s001` | 1 | 0 | `sft_9b19d8a6f0` | — | `sft_9b19d8a6f0` |
| `lasr:t2_b24_s007` | 1 | 1 | `sft_d2c7f52f64` | `doc_6db692886e` | `sft_d2c7f52f64` |
| `lasr:t2_b25_s002` | 1 | 1 | `sft_def2fdfd5e` | `doc_6e33dc4091` | `sft_def2fdfd5e` |
| `lasr:t2_b26_s006` | 1 | 0 | `sft_9369128411` | — | `sft_9369128411` |
| `lasr:t2_b28_s003` | 0 | 1 | — | `doc_83a64142e6` | `sft_ec294a9669` |
| `lasr:t2_b29_s000` | 1 | 0 | `sft_b6870957dc` | — | `sft_b6870957dc` |
| `lasr:t2_b30_s000` | 0 | 1 | — | `doc_d70eac03ca` | `sft_aeccc56218` |
| `lasr:t3_b03_s003` | 0 | 1 | — | `doc_4db296f837` | `sft_9ca17428a1` |
| `lasr:t3_b03_s006` | 1 | 0 | `sft_17e4e24e1d` | — | `sft_17e4e24e1d` |
| `lasr:t3_b04_s005` | 1 | 1 | `sft_4753f90cf0` | `doc_0431b85d36` | `sft_4753f90cf0` |
| `lasr:t3_b07_s000` | 0 | 1 | — | `doc_8df754707f` | `sft_6d53216b19` |
| `lasr:t3_b07_s003` | 1 | 1 | `sft_32bc08d1c2` | `doc_cec34dc701` | `sft_32bc08d1c2` |
| `lasr:t3_b07_s007` | 1 | 0 | `sft_c098c70cb2` | — | `sft_c098c70cb2` |
| `lasr:t3_b08_s005` | 1 | 0 | `prop_11fcc958e7` | — | `prop_11fcc958e7` |
| `lasr:t3_b10_s006` | 1 | 1 | `sft_b29edaa091` | `doc_0bb7fa96d6` | `sft_b29edaa091` |
| `lasr:t3_b11_s005` | 1 | 1 | `sft_2fb3012a66` | `doc_d9d5e73f11` | `sft_2fb3012a66` |
| `lasr:t3_b12_s000` | 1 | 0 | `sft_1fba37aa79` | — | `sft_1fba37aa79` |
| `lasr:t3_b12_s003` | 0 | 1 | — | `doc_3c08c4f0b2` | `sft_d65d8ba4f1` |
| `lasr:t3_b14_s001` | 0 | 1 | — | `doc_4be08ae938` | `sft_898e895b3d` |
| `lasr:t3_b14_s004` | 1 | 0 | `sft0007` | — | `sft0007` |
| `lasr:t3_b16_s002` | 0 | 1 | — | `doc_8363aac141` | `sft_ed510e5d77` |
| `lasr:t3_b19_s001` | 0 | 1 | — | `doc_bfb52b2c1a` | `sft_e82504a02a` |
| `lasr:t3_b19_s004` | 0 | 1 | — | `doc_ea10b4bc20` | `sft_628f8543ef` |
| `lasr:t3_b20_s002` | 1 | 1 | `sft_ef59a93d94` | `doc_f6573e98d8` | `sft_ef59a93d94` |
| `lasr:t3_b22_s002` | 0 | 1 | — | `doc_8ac5749ddc` | `sft_15f3ee1d80` |
| `lasr:t3_b25_s003` | 0 | 1 | — | `doc_57fcd08857` | `sft_64fa8e8321` |
| `lasr:t3_b27_s006` | 1 | 0 | `prop_12a669329a` | — | `prop_12a669329a` |
| `lasr:t3_b28_s003` | 1 | 1 | `sft_61fb37da79` | `doc_24f8583b46` | `sft_61fb37da79` |
| `lasr:t3_b29_s007` | 0 | 1 | — | `doc_4f4ca9b2ad` | `sft_fe3f9205f9` |
| `lasr:t3_b30_s000` | 1 | 0 | `sft0019` | — | `sft0019` |
| `lasr:t4_b00_s005` | 1 | 1 | `sft_dd7364d8dc` | `doc_7f36dbe68c` | `sft_dd7364d8dc` |
| `lasr:t4_b00_s007` | 1 | 0 | `sft_4dd87f2f0e` | — | `sft_4dd87f2f0e` |
| `lasr:t4_b01_s000` | 0 | 1 | — | `doc_4906fe72bc` | `sft_55b9b6463e` |
| `lasr:t4_b02_s004` | 1 | 1 | `sft_bf6940f8c8` | `doc_3a64c7f265` | `sft_bf6940f8c8` |
| `lasr:t4_b03_s003` | 1 | 1 | `sft_4195581ab1` | `doc_601d1b3d5c` | `sft_4195581ab1` |
| `lasr:t4_b04_s001` | 1 | 1 | `sft_42ac848a6e` | `doc_1154a3bd45` | `sft_42ac848a6e` |
| `lasr:t4_b06_s004` | 1 | 0 | `sft_286bf9b20d` | — | `sft_286bf9b20d` |
| `lasr:t4_b07_s000` | 1 | 0 | `prop_6b2f8154ed` | — | `prop_6b2f8154ed` |
| `lasr:t4_b08_s002` | 1 | 1 | `sft_12c6563561` | `doc_a5d97cfcc6` | `sft_12c6563561` |
| `lasr:t4_b11_s003` | 1 | 1 | `sft_cf3f75479c` | `doc_eb3eadf2a9` | `sft_cf3f75479c` |
| `lasr:t4_b13_s002` | 1 | 0 | `prop_06abf29e10` | — | `prop_06abf29e10` |
| `lasr:t4_b15_s000` | 1 | 0 | `sft_ae1da314f9` | — | `sft_ae1da314f9` |
| `lasr:t4_b15_s007` | 3 | 1 | `ask_17f435cd62`, `ask_17f435cd62_q`, `sft_17f435cd62` | `doc_2793d29cf4` | `sft_17f435cd62` |
| `lasr:t4_b17_s003` | 1 | 0 | `sft_522fe59248` | — | `sft_522fe59248` |
| `lasr:t4_b18_s004` | 0 | 1 | — | `doc_4f82481243` | `sft_9571595960` |
| `lasr:t4_b20_s003` | 1 | 0 | `sft_416a7480f9` | — | `sft_416a7480f9` |
| `lasr:t4_b20_s007` | 1 | 0 | `prop_b08869848c` | — | `prop_b08869848c` |
| `lasr:t4_b22_s000` | 1 | 1 | `sft_63e0f2a92b` | `doc_e33070b675` | `sft_63e0f2a92b` |
| `lasr:t4_b24_s002` | 1 | 1 | `sft_6774d455f3` | `doc_43d684f1a0` | `sft_6774d455f3` |
| `lasr:t4_b25_s000` | 1 | 1 | `sft_21f5215e4a` | `doc_89815f27d9` | `sft_21f5215e4a` |
| `lasr:t4_b25_s007` | 1 | 0 | `sft_ef46ab0272` | — | `sft_ef46ab0272` |
| `lasr:t4_b26_s006` | 1 | 0 | `sft_cabab56cd4` | — | `sft_cabab56cd4` |
| `lasr:t4_b28_s000` | 1 | 1 | `ask_d6a65c9c30_q` | `doc_2a49ab6fe0` | `sft_d6a65c9c30` |
| `lasr:t4_b28_s007` | 1 | 0 | `sft_ce20c030e9` | — | `sft_ce20c030e9` |
| `lasr:t4_b30_s001` | 1 | 1 | `sft_33831e5f61` | `doc_607004c78e` | `sft_33831e5f61` |
| `lasr:t5_b00_s005` | 1 | 1 | `sft_642da3e4c2` | `doc_1f3c634e46` | `sft_642da3e4c2` |
| `lasr:t5_b01_s005` | 1 | 0 | `sft_4d4a17c761` | — | `sft_4d4a17c761` |
| `lasr:t5_b02_s001` | 1 | 0 | `sft_112d1e9318` | — | `sft_112d1e9318` |
| `lasr:t5_b03_s000` | 1 | 0 | `prop_a6a779b83b` | — | `prop_a6a779b83b` |
| `lasr:t5_b04_s001` | 0 | 1 | — | `doc_0947bb95f3` | `sft_7260f07bb6` |
| `lasr:t5_b06_s000` | 1 | 1 | `sft_32f7161094` | `doc_792359d852` | `sft_32f7161094` |
| `lasr:t5_b06_s001` | 1 | 1 | `sft_473d0b5f13` | `doc_bbbf7b2ad3` | `sft_473d0b5f13` |
| `lasr:t5_b06_s006` | 1 | 0 | `prop_9593afefcc` | — | `prop_9593afefcc` |
| `lasr:t5_b07_s006` | 1 | 1 | `sft_3abe40db93` | `doc_4a16bba652` | `sft_3abe40db93` |
| `lasr:t5_b10_s006` | 1 | 0 | `sft_00b0986727` | — | `sft_00b0986727` |
| `lasr:t5_b10_s007` | 0 | 1 | — | `doc_1fde28438e` | `sft_6a7ff695e0` |
| `lasr:t5_b12_s000` | 0 | 1 | — | `doc_ff4d016045` | `sft_dba5510a07` |
| `lasr:t5_b14_s002` | 1 | 0 | `prop_83300dbaac` | — | `prop_83300dbaac` |
| `lasr:t5_b15_s007` | 1 | 0 | `sft_862392a142` | — | `sft_862392a142` |
| `lasr:t5_b19_s001` | 1 | 0 | `sft0006` | — | `sft0006` |
| `lasr:t5_b20_s006` | 1 | 1 | `sft_44e4c7f709` | `doc_6182279b29` | `sft_44e4c7f709` |
| `lasr:t5_b22_s000` | 1 | 0 | `sft_fc68828efb` | — | `sft_fc68828efb` |
| `lasr:t5_b22_s003` | 1 | 1 | `sft_29bfa98f4e` | `doc_1e78e0321f` | `sft_29bfa98f4e` |
| `lasr:t5_b24_s004` | 0 | 1 | — | `doc_ad05bbcc07` | `sft_be6c3b79e5` |
| `lasr:t5_b24_s007` | 0 | 1 | — | `doc_f6941653f8` | `sft_495a0c8db1` |
| `lasr:t5_b26_s006` | 1 | 0 | `sft_345c09c07a` | — | `sft_345c09c07a` |
| `lasr:t5_b28_s000` | 1 | 1 | `sft_398a3c0c06` | `doc_6a8d39dc63` | `sft_398a3c0c06` |
| `lasr:t5_b28_s004` | 1 | 1 | `sft_d8aed6b585` | `doc_61eaff35e5` | `sft_d8aed6b585` |
| `lasr:t6_b00_s003` | 0 | 1 | — | `doc_3ed801e1c7` | `sft_1543b0fe07` |
| `lasr:t6_b00_s007` | 1 | 0 | `sft0016` | — | `sft0016` |
| `lasr:t6_b02_s002` | 1 | 0 | `sft_4468036792` | — | `sft_4468036792` |
| `lasr:t6_b05_s002` | 1 | 0 | `prop_603d157c0c` | — | `prop_603d157c0c` |
| `lasr:t6_b05_s006` | 1 | 0 | `sft_e0f11406a7` | — | `sft_e0f11406a7` |
| `lasr:t6_b06_s002` | 0 | 1 | — | `doc_6ee48f3155` | `sft_7ccdb2df7f` |
| `lasr:t6_b10_s002` | 0 | 1 | — | `doc_91c2bcd8af` | `sft_381cadfd5f` |
| `lasr:t6_b10_s003` | 1 | 0 | `sft_f9096a3b73` | — | `sft_f9096a3b73` |
| `lasr:t6_b12_s001` | 1 | 1 | `sft_de36ab877e` | `doc_6da7db84e4` | `sft_de36ab877e` |
| `lasr:t6_b12_s005` | 1 | 0 | `sft_2257709361` | — | `sft_2257709361` |
| `lasr:t6_b16_s005` | 1 | 1 | `sft_c86bcb87c2` | `doc_6bc760f9df` | `sft_c86bcb87c2` |
| `lasr:t6_b17_s003` | 1 | 0 | `prop_750cf0d3e9` | — | `prop_750cf0d3e9` |
| `lasr:t6_b17_s004` | 0 | 1 | — | `doc_33b5856583` | `sft_a414e4575b` |
| `lasr:t6_b21_s004` | 1 | 0 | `sft_102820d8d1` | — | `sft_102820d8d1` |
| `lasr:t6_b23_s002` | 0 | 1 | — | `doc_afd6864a91` | `sft_882f06af1a` |
| `lasr:t6_b23_s007` | 1 | 1 | `sft_bd6a4f2a97` | `doc_8619c4c0ed` | `sft_bd6a4f2a97` |
| `lasr:t6_b24_s000` | 1 | 0 | `sft_59ed5726a6` | — | `sft_59ed5726a6` |
| `lasr:t6_b25_s005` | 0 | 1 | — | `doc_2f78264a87` | `sft_f60cf92f13` |
| `lasr:t6_b26_s006` | 1 | 1 | `sft_e1e7b9516c` | `doc_995182394e` | `sft_e1e7b9516c` |
| `lasr:t6_b29_s002` | 1 | 0 | `sft_d39d92158b` | — | `sft_d39d92158b` |
| `lasr:t6_b29_s006` | 1 | 0 | `sft_ae26725123` | — | `sft_ae26725123` |
| `lasr:t6_b30_s000` | 1 | 1 | `sft_dfa5eb09bd` | `doc_cddb1cdcf8` | `sft_dfa5eb09bd` |
| `lasr:t7_b00_s006` | 1 | 1 | `sft_fc3a4c8a6c` | `doc_25ae62f52d` | `sft_fc3a4c8a6c` |
| `lasr:t7_b01_s000` | 1 | 0 | `prop_2e78b3ced3` | — | `prop_2e78b3ced3` |
| `lasr:t7_b01_s003` | 0 | 1 | — | `doc_8cc97e910c` | `sft_b44bb7774d` |
| `lasr:t7_b02_s007` | 0 | 1 | — | `doc_e7235362d8` | `sft_d1150af90a` |
| `lasr:t7_b03_s001` | 1 | 0 | `sft_e5c1626b2b` | — | `sft_e5c1626b2b` |
| `lasr:t7_b03_s007` | 1 | 0 | `sft_41efcfad20` | — | `sft_41efcfad20` |
| `lasr:t7_b04_s000` | 0 | 1 | — | `doc_2d229020e2` | `sft_f302a78775` |
| `lasr:t7_b04_s001` | 1 | 1 | `sft_d8b5b308d6` | `doc_ebfb219dee` | `sft_d8b5b308d6` |
| `lasr:t7_b08_s005` | 1 | 1 | `sft_6fc9efb403` | `doc_d15b17a3de` | `sft_6fc9efb403` |
| `lasr:t7_b13_s006` | 1 | 1 | `sft_69196aeee5` | `doc_a9989cc573` | `sft_69196aeee5` |
| `lasr:t7_b14_s002` | 0 | 1 | — | `doc_3df742708a` | `sft_79460fcab1` |
| `lasr:t7_b15_s004` | 1 | 1 | `sft_4e17df9f0d` | `doc_5f1306e349` | `sft_4e17df9f0d` |
| `lasr:t7_b16_s004` | 1 | 0 | `prop_b5d07efc8a` | — | `prop_b5d07efc8a` |
| `lasr:t7_b16_s007` | 0 | 1 | — | `doc_3c3ec0f714` | `sft_2be47a90c2` |
| `lasr:t7_b18_s005` | 1 | 1 | `sft_4a119ce66e` | `doc_548ff0e944` | `sft_4a119ce66e` |
| `lasr:t7_b19_s001` | 1 | 0 | `sft_c70c35e1fc` | — | `sft_c70c35e1fc` |
| `lasr:t7_b19_s005` | 1 | 0 | `prop_098f3ec19f` | — | `prop_098f3ec19f` |
| `lasr:t7_b20_s007` | 1 | 0 | `sft_6cc9fc5875` | — | `sft_6cc9fc5875` |
| `lasr:t7_b22_s006` | 1 | 0 | `sft_af34fa7169` | — | `sft_af34fa7169` |
| `lasr:t7_b24_s000` | 1 | 1 | `sft_4cbaa41be4` | `doc_e7248bb356` | `sft_4cbaa41be4` |
| `lasr:t7_b24_s006` | 1 | 0 | `prop_d70545e409` | — | `prop_d70545e409` |
| `lasr:t7_b27_s005` | 1 | 0 | `prop_bb8f82278f` | — | `prop_bb8f82278f` |
| `lasr:t7_b28_s002` | 1 | 0 | `prop_1e91f38e85` | — | `prop_1e91f38e85` |
| `lasr:t7_b28_s003` | 1 | 0 | `sft_11c7d262af` | — | `sft_11c7d262af` |
| `lasr:t7_b29_s001` | 1 | 0 | `sft_3bc3992453` | — | `sft_3bc3992453` |
| `lasr:t8_b01_s001` | 1 | 1 | `sft_39877dba9b` | `doc_a291dd6d30` | `sft_39877dba9b` |
| `lasr:t8_b02_s006` | 0 | 1 | — | `doc_52f5fa3c8c` | `sft_3bf3796195` |
| `lasr:t8_b03_s006` | 1 | 0 | `sft_57390c38be` | — | `sft_57390c38be` |
| `lasr:t8_b04_s006` | 1 | 0 | `sft_4ac377841f` | — | `sft_4ac377841f` |
| `lasr:t8_b08_s002` | 0 | 1 | — | `doc_e644c02ab8` | `sft_468ed33b8a` |
| `lasr:t8_b10_s000` | 3 | 1 | `ask_8a1c88530e`, `ask_8a1c88530e_q`, `sft_8a1c88530e` | `doc_b49cb49433` | `sft_8a1c88530e` |
| `lasr:t8_b10_s002` | 1 | 1 | `sft_ed36966d3b` | `doc_ef6e7748b7` | `sft_ed36966d3b` |
| `lasr:t8_b12_s000` | 0 | 1 | — | `doc_1b000b3455` | `sft_0a35fa2293` |
| `lasr:t8_b12_s004` | 1 | 0 | `sft_8b381dd945` | — | `sft_8b381dd945` |
| `lasr:t8_b12_s007` | 1 | 0 | `sft_dbc076424f` | — | `sft_dbc076424f` |
| `lasr:t8_b14_s000` | 0 | 1 | — | `doc_1bd31111be` | `sft_ae40d67bdb` |
| `lasr:t8_b15_s004` | 1 | 0 | `prop_6047246d12` | — | `prop_6047246d12` |
| `lasr:t8_b15_s005` | 0 | 1 | — | `doc_dd6af95317` | `sft_e17ca447f0` |
| `lasr:t8_b15_s007` | 0 | 1 | — | `doc_09a6ef7db5` | `sft_b806195d15` |
| `lasr:t8_b16_s003` | 0 | 1 | — | `doc_c880fa0109` | `sft_21d924c000` |
| `lasr:t8_b16_s007` | 1 | 1 | `sft_44c7dc20eb` | `doc_78bd23578a` | `sft_44c7dc20eb` |
| `lasr:t8_b17_s006` | 0 | 1 | — | `doc_738091f7bc` | `sft_69b01a2afb` |
| `lasr:t8_b17_s007` | 0 | 1 | — | `doc_8be83c85cc` | `sft_e9d5ca164c` |
| `lasr:t8_b19_s002` | 1 | 0 | `sft_54949688b5` | — | `sft_54949688b5` |
| `lasr:t8_b21_s001` | 1 | 0 | `sft_05e8f35791` | — | `sft_05e8f35791` |
| `lasr:t8_b23_s000` | 1 | 1 | `sft_6d25e34238` | `doc_7ad39e2e0d` | `sft_6d25e34238` |
| `lasr:t8_b24_s007` | 1 | 0 | `prop_79b35368ae` | — | `prop_79b35368ae` |
| `lasr:t8_b26_s006` | 0 | 1 | — | `doc_26adfdc19d` | `sft_6197f496a3` |
| `lasr:t8_b27_s001` | 0 | 1 | — | `doc_536c85a7cc` | `sft_85496960a9` |
| `lasr:t8_b27_s003` | 1 | 1 | `sft_84d10dac9e` | `doc_695274dea7` | `sft_84d10dac9e` |
| `lasr:t8_b28_s003` | 1 | 0 | `prop_08f0cd5654` | — | `prop_08f0cd5654` |
| `lasr:t8_b30_s003` | 1 | 0 | `sft_d0beb95d61` | — | `sft_d0beb95d61` |
| `lasr:t9_b01_s000` | 1 | 1 | `sft_eb382e6868` | `doc_24dc550c0b` | `sft_eb382e6868` |
| `lasr:t9_b01_s005` | 1 | 0 | `sft_3ca071d999` | — | `sft_3ca071d999` |
| `lasr:t9_b02_s003` | 1 | 1 | `sft_82e3ae4cc3` | `doc_d68d0237bd` | `sft_82e3ae4cc3` |
| `lasr:t9_b02_s007` | 0 | 1 | — | `doc_075db0ab5d` | `sft_2135fc363b` |
| `lasr:t9_b04_s005` | 0 | 1 | — | `doc_0bdfdb8c5b` | `sft_fcf073f1a4` |
| `lasr:t9_b05_s001` | 1 | 1 | `sft_2af4cdf5cc` | `doc_665dc99487` | `sft_2af4cdf5cc` |
| `lasr:t9_b05_s004` | 1 | 0 | `sft_1edc763142` | — | `sft_1edc763142` |
| `lasr:t9_b07_s002` | 1 | 1 | `sft_6e08bd2cd8` | `doc_880a1e1903` | `sft_6e08bd2cd8` |
| `lasr:t9_b07_s003` | 1 | 0 | `prop_0f3b76f273` | — | `prop_0f3b76f273` |
| `lasr:t9_b07_s006` | 1 | 0 | `sft_f8d3b32c14` | — | `sft_f8d3b32c14` |
| `lasr:t9_b08_s004` | 0 | 1 | — | `doc_e0c5bf2258` | `sft_9e14684a95` |
| `lasr:t9_b10_s000` | 1 | 1 | `sft_a39fb11744` | `doc_43dc15f63b` | `sft_a39fb11744` |
| `lasr:t9_b12_s003` | 1 | 0 | `sft_c86e65ab6f` | — | `sft_c86e65ab6f` |
| `lasr:t9_b12_s004` | 1 | 1 | `sft_e6d12db8e3` | `doc_5a5c0534cf` | `sft_e6d12db8e3` |
| `lasr:t9_b14_s005` | 1 | 1 | `sft_d1a67aca89` | `doc_cda4dd146a` | `sft_d1a67aca89` |
| `lasr:t9_b15_s002` | 1 | 0 | `prop_b84265cbce` | — | `prop_b84265cbce` |
| `lasr:t9_b18_s007` | 1 | 1 | `sft_931e19e86a` | `doc_5244db8707` | `sft_931e19e86a` |
| `lasr:t9_b19_s005` | 1 | 0 | `sft_479020a2f7` | — | `sft_479020a2f7` |
| `lasr:t9_b20_s002` | 1 | 0 | `sft_764cc06353` | — | `sft_764cc06353` |
| `lasr:t9_b21_s000` | 1 | 1 | `sft_dc53d03dcc` | `doc_311e0e789f` | `sft_dc53d03dcc` |
| `lasr:t9_b21_s002` | 1 | 0 | `sft0001` | — | `sft0001` |
| `lasr:t9_b22_s001` | 0 | 1 | — | `doc_b8160aebb1` | `sft_f45752680e` |
| `lasr:t9_b23_s000` | 0 | 1 | — | `doc_ba9d859ccf` | `sft_e2bffcfecc` |
| `lasr:t9_b23_s001` | 1 | 1 | `ask_4bf77e5685_q` | `doc_dd1fc6d5d7` | `sft_4bf77e5685` |
| `lasr:t9_b24_s007` | 1 | 0 | `sft_862e02f9be` | — | `sft_862e02f9be` |
| `lasr:t9_b25_s006` | 0 | 1 | — | `doc_84f71f2125` | `sft_42eb2d3383` |
| `lasr:t9_b26_s002` | 3 | 1 | `ask_9a9cce7f35`, `ask_9a9cce7f35_q`, `sft_9a9cce7f35` | `doc_0ea81bf79f` | `sft_9a9cce7f35` |
| `lasr:t9_b26_s005` | 1 | 0 | `sft_60b7d7e021` | — | `sft_60b7d7e021` |
| `lasr:t9_b27_s006` | 1 | 1 | `sft_a84656ebe6` | `doc_99a8c4fe27` | `sft_a84656ebe6` |
| `machiavelli:machiavelli_blood-money_Blood_Money-10_lockdown_5905-249` | 1 | 0 | `sft_bb20c543a9` | — | `sft_bb20c543a9` |
| `machiavelli:machiavelli_blood-money_Blood_Money-10_lockdown_6064-251` | 1 | 0 | `sft_12d92067dd` | — | `sft_12d92067dd` |
| `machiavelli:machiavelli_blood-money_Blood_Money-10_lockdown_6795-258` | 1 | 1 | `sft_01ed5bd33e` | `doc_dc970dd9e1` | `sft_01ed5bd33e` |
| `machiavelli:machiavelli_blood-money_Blood_Money-10_lockdown_7165-1533` | 1 | 0 | `prop_a9f1098a97` | — | `prop_a9f1098a97` |
| `machiavelli:machiavelli_blood-money_Blood_Money-11_aftermath_420-360` | 1 | 0 | `sft_6ab07e6460` | — | `sft_6ab07e6460` |
| `machiavelli:machiavelli_blood-money_Blood_Money-2_pereira_1379-993` | 0 | 1 | — | `doc_cb8cbdcba5` | `sft_41fbb19ca0` |
| `machiavelli:machiavelli_blood-money_Blood_Money-3_wake_2194-1777` | 1 | 1 | `sft_faad1efd1e` | `doc_8cbb139614` | `sft_faad1efd1e` |
| `machiavelli:machiavelli_blood-money_Blood_Money-6_underground_924_collapsed-1106` | 0 | 1 | — | `doc_d93395abc8` | `sft_0d8f9c5aec` |
| `machiavelli:machiavelli_broadsides-hms-foraker_HMS_Foraker-chapter_1_401-7430` | 0 | 1 | — | `doc_cebdfc87f8` | `sft_5b0fe7f8ab` |
| `machiavelli:machiavelli_broadsides-hms-foraker_HMS_Foraker-chapter_2_580-2829` | 1 | 0 | `sft_649ba28a4d` | — | `sft_649ba28a4d` |
| `machiavelli:machiavelli_broadsides-hms-foraker_HMS_Foraker-chapter_2_787-4589` | 1 | 0 | `sft_5cbb1a3b31` | — | `sft_5cbb1a3b31` |
| `machiavelli:machiavelli_broadway-1849_Broadway_1849-9_to_the_opera_house_267-243` | 1 | 0 | `prop_fea30566cc` | — | `prop_fea30566cc` |
| `machiavelli:machiavelli_cat_Choice_of_the_Cat-01_newhome_1211-1620` | 1 | 0 | `sft_2dc469d657` | — | `sft_2dc469d657` |
| `machiavelli:machiavelli_cat_Choice_of_the_Cat-01_newhome_161-1684` | 1 | 0 | `prop_79dd8798cb` | — | `prop_79dd8798cb` |
| `machiavelli:machiavelli_cat_Choice_of_the_Cat-05_bigdecision_552-142` | 1 | 1 | `sft_46c2ccd5ba` | `doc_e05e01d2e4` | `sft_46c2ccd5ba` |
| `machiavelli:machiavelli_cat_Choice_of_the_Cat-08_theparty_2486-597` | 0 | 1 | — | `doc_97e90999d0` | `sft_8f1d7fdcbd` |
| `machiavelli:machiavelli_champion-of-the-gods_Champion_of_the_Gods-startup_1312-0` | 1 | 0 | `sft_55d0358fce` | — | `sft_55d0358fce` |
| `machiavelli:machiavelli_champion-of-the-gods_Champion_of_the_Gods-the_attack_of_the_temach_23-71` | 1 | 0 | `sft_30290eaf2b` | — | `sft_30290eaf2b` |
| `machiavelli:machiavelli_champion-of-the-gods_Champion_of_the_Gods-the_oracle_and_the_aftermath_265-3484` | 1 | 1 | `sft_afecd0ffc6` | `doc_582251a207` | `sft_afecd0ffc6` |
| `machiavelli:machiavelli_chronicon-apocalyptica_Chronicon_Apocalyptica-4_thorolf_1398-2228` | 1 | 0 | `sft_ab5b335eb3` | — | `sft_ab5b335eb3` |
| `machiavelli:machiavelli_chronicon-apocalyptica_Chronicon_Apocalyptica-4_thorolf_830_collapsed-709` | 0 | 1 | — | `doc_3924dc69b1` | `sft_8f678b88cf` |
| `machiavelli:machiavelli_chronicon-apocalyptica_Chronicon_Apocalyptica-5_witch_473-2285` | 0 | 1 | — | `doc_da3dfe5bd6` | `sft_610f01a99d` |
| `machiavelli:machiavelli_daring-mermaid-expedition_The_Daring_Mermaid_Expedition-2_society_144-349` | 0 | 1 | — | `doc_452dbe6e09` | `sft_e5210d1834` |
| `machiavelli:machiavelli_deathless_Choice_of_the_Deathless-devilsasylum_839-469` | 1 | 1 | `sft_7797dbae3d` | `doc_36ab4f51b3` | `sft_7797dbae3d` |
| `machiavelli:machiavelli_diabolical_Diabolical-chapternine_355-203` | 1 | 1 | `sft_4deeda4e34` | `doc_3ebe747b8e` | `sft_4deeda4e34` |
| `machiavelli:machiavelli_dinoknights_DinoKnights-05_return_932-1317` | 2 | 1 | `ask_febd7f2797`, `sft_febd7f2797` | `doc_149f470741` | `sft_febd7f2797` |
| `machiavelli:machiavelli_dinoknights_DinoKnights-08_menace_0-320` | 1 | 1 | `sft_7f19dd328f` | `doc_c185cc697c` | `sft_7f19dd328f` |
| `machiavelli:machiavelli_dinoknights_DinoKnights-10_tournament_585-1114` | 1 | 0 | `sft_0318c1c54d` | — | `sft_0318c1c54d` |
| `machiavelli:machiavelli_drag-star_Drag_Star-10_episode9_1298-454` | 1 | 0 | `sft_c71266b023` | — | `sft_c71266b023` |
| `machiavelli:machiavelli_drag-star_Drag_Star-6_episode5_443-707` | 1 | 0 | `prop_89d44ff9b8` | — | `prop_89d44ff9b8` |
| `machiavelli:machiavelli_drag-star_Drag_Star-7_episode6_125-1212` | 1 | 1 | `sft_6e837fc7d3` | `doc_c90247036c` | `sft_6e837fc7d3` |
| `machiavelli:machiavelli_drag-star_Drag_Star-8_episode7_424-166` | 1 | 0 | `sft_d6d8c0e75a` | — | `sft_d6d8c0e75a` |
| `machiavelli:machiavelli_dragon-and-the-djinn_The_Dragon_and_the_Djinn-11_battle_3039-1111` | 0 | 1 | — | `doc_c32665a52b` | `sft_f00501b705` |
| `machiavelli:machiavelli_dragon-and-the-djinn_The_Dragon_and_the_Djinn-11_battle_4449-347` | 0 | 1 | — | `doc_5d6799bb05` | `sft_609330fe86` |
| `machiavelli:machiavelli_dragon-and-the-djinn_The_Dragon_and_the_Djinn-3_dragon_appearance_60-1569` | 1 | 1 | `sft_cbdbfe0191` | `doc_f59e7b38f3` | `sft_cbdbfe0191` |
| `machiavelli:machiavelli_dragon-and-the-djinn_The_Dragon_and_the_Djinn-7_palace_988-2046` | 1 | 0 | `prop_72aa509016` | — | `prop_72aa509016` |
| `machiavelli:machiavelli_empyrean_Empyrean-7_stop_radiance_418-2223` | 0 | 1 | — | `doc_ba33fe599c` | `sft_3546e28ec3` |
| `machiavelli:machiavelli_empyrean_Empyrean-9_strephon_revealed_2197-1916` | 1 | 0 | `prop_f3fee26da2` | — | `prop_f3fee26da2` |
| `machiavelli:machiavelli_fleet_The_Fleet-epilogue_540-80` | 1 | 1 | `sft_aead615829` | `doc_01720b3299` | `sft_aead615829` |
| `machiavelli:machiavelli_fog-knows-your-name_The_Fog_Knows_Your_Name-calmbeforestorm07_617-442` | 1 | 1 | `sft_0bd54bce24` | `doc_8b66cc0c41` | `sft_0bd54bce24` |
| `machiavelli:machiavelli_fog-knows-your-name_The_Fog_Knows_Your_Name-thedarech02_0-957` | 1 | 0 | `prop_db02dd437a` | — | `prop_db02dd437a` |
| `machiavelli:machiavelli_fog-knows-your-name_The_Fog_Knows_Your_Name-welcomingch01_0-0` | 1 | 1 | `sft_e5a4c71ed1` | `doc_0a54524845` | `sft_e5a4c71ed1` |
| `machiavelli:machiavelli_fog-knows-your-name_The_Fog_Knows_Your_Name-welcomingch01_491-911` | 1 | 1 | `sft_0bfe29aaba` | `doc_35770828df` | `sft_0bfe29aaba` |
| `machiavelli:machiavelli_fog-of-war-battle-for-cerberus_Fog_of_War_The_Battle_for_Cerberus-10_final_mission_617-80` | 1 | 0 | `sft_85f05b34d4` | — | `sft_85f05b34d4` |
| `machiavelli:machiavelli_fog-of-war-battle-for-cerberus_Fog_of_War_The_Battle_for_Cerberus-6_trapped_on_surface_121-333` | 0 | 1 | — | `doc_783457e771` | `sft_d592d4f402` |
| `machiavelli:machiavelli_grand-academy-for-villains_Grand_Academy_for_Future_Villains-4_midterms_1269-810` | 2 | 1 | `ask_c6f8841494_q`, `sft_c6f8841494` | `doc_32c3cc1115` | `sft_c6f8841494` |
| `machiavelli:machiavelli_grand-academy-for-villains_Grand_Academy_for_Future_Villains-4_midterms_1502-72` | 1 | 0 | `sft_54eba4a8ac` | — | `sft_54eba4a8ac` |
| `machiavelli:machiavelli_heart-of-the-house_Heart_of_the_House-reaves_chat_212-3123` | 0 | 1 | — | `doc_ab4243137d` | `sft_5e37eb0754` |
| `machiavelli:machiavelli_hero-unmasked_The_Hero_Unmasked-c02_82-1078` | 1 | 0 | `prop_8f07b7da56` | — | `prop_8f07b7da56` |
| `machiavelli:machiavelli_hero-unmasked_The_Hero_Unmasked-c04_253-1099` | 1 | 0 | `prop_5a0fc47b43` | — | `prop_5a0fc47b43` |
| `machiavelli:machiavelli_heroes-rise_Heroes_Rise_The_Prodigy-ganged_upon_179-433` | 0 | 1 | — | `doc_3c1ee7e9ca` | `sft_264089d5b0` |
| `machiavelli:machiavelli_heroes-rise_Heroes_Rise_The_Prodigy-grand_plans_0-739` | 1 | 1 | `sft_96b1fa1eff` | `doc_14fd666c18` | `sft_96b1fa1eff` |
| `machiavelli:machiavelli_heroes-rise_Heroes_Rise_The_Prodigy-night_life_357-1807` | 1 | 0 | `sft_b8b65b6ae3` | — | `sft_b8b65b6ae3` |
| `machiavelli:machiavelli_ironheart_Ironheart-3_city_of_giants_48-42` | 0 | 1 | — | `doc_439e2a0cf3` | `sft_e08fb92423` |
| `machiavelli:machiavelli_ironheart_Ironheart-8_center_of_the_world_794-1435` | 1 | 1 | `sft_8c4e227a01` | `doc_9848094c37` | `sft_8c4e227a01` |
| `machiavelli:machiavelli_ironheart_Ironheart-9_custom_of_kings_1789-924` | 0 | 1 | — | `doc_b2cd55a42b` | `sft_bf94755076` |
| `machiavelli:machiavelli_its-killing-time_Its_Killing_Time-prague_298-379` | 1 | 1 | `sft_02f419b2b9` | `doc_5d896fe9c9` | `sft_02f419b2b9` |
| `machiavelli:machiavelli_light-years-apart_Light_Years_Apart-3_fun_857-911` | 1 | 0 | `sft_85bbaf39cf` | — | `sft_85bbaf39cf` |
| `machiavelli:machiavelli_light-years-apart_Light_Years_Apart-6_plan_639-1274` | 1 | 1 | `sft_eee12f159f` | `doc_558543cded` | `sft_eee12f159f` |
| `machiavelli:machiavelli_mask-of-the-plague-doctor_Mask_of_the_Plague_Doctor-7_going_underground_578-1211` | 1 | 1 | `sft_8f31374eeb` | `doc_b4d97a07f4` | `sft_8f31374eeb` |
| `machiavelli:machiavelli_mrs-claus_In_the_Service_of_Mrs_Claus-1_special_delivery_623-1496` | 1 | 0 | `prop_1cca6aa463` | — | `prop_1cca6aa463` |
| `machiavelli:machiavelli_mrs-claus_In_the_Service_of_Mrs_Claus-8_enter_the_beast_423-159` | 1 | 1 | `sft_544f642324` | `doc_08a0a77524` | `sft_544f642324` |
| `machiavelli:machiavelli_mrs-claus_In_the_Service_of_Mrs_Claus-9_flames_strike_337-167` | 1 | 0 | `sft_3dde7df0a3` | — | `sft_3dde7df0a3` |
| `machiavelli:machiavelli_neighbourhood-necromancer_Neighbourhood_Necromancer-climax_801-1364` | 1 | 1 | `sft_c01f54d8f5` | `doc_a12d0768e0` | `sft_c01f54d8f5` |
| `machiavelli:machiavelli_neighbourhood-necromancer_Neighbourhood_Necromancer-setup_31-1` | 2 | 1 | `ask_ca00089bb0_q`, `sft_ca00089bb0` | `doc_cb7f38f8bf` | `sft_ca00089bb0` |
| `machiavelli:machiavelli_neighbourhood-necromancer_Neighbourhood_Necromancer-stageone_267-2707` | 2 | 1 | `ask_10c14d8649`, `sft_10c14d8649` | `doc_2ebee70f38` | `sft_10c14d8649` |
| `machiavelli:machiavelli_ninja_Choice_of_the_Ninja-documentbeta_103-529` | 1 | 0 | `sft_401bde78d2` | — | `sft_401bde78d2` |
| `machiavelli:machiavelli_ninja_Choice_of_the_Ninja-graduationtest_1053-597` | 1 | 1 | `sft_8422341663` | `doc_2346b2cc09` | `sft_8422341663` |
| `machiavelli:machiavelli_nola-is-burning_NOLA_Is_Burning-informants_494-370` | 1 | 0 | `prop_c327799446` | — | `prop_c327799446` |
| `machiavelli:machiavelli_odyssey-echoes-of-war_An_Odyssey_Echoes_of_War-6_philoxenia_286-718` | 1 | 0 | `sft_13e9bd88b4` | — | `sft_13e9bd88b4` |
| `machiavelli:machiavelli_petal-throne_Choice_of_the_Petal_Throne-battlelost_73-1018` | 1 | 0 | `prop_acae9948c6` | — | `prop_acae9948c6` |
| `machiavelli:machiavelli_pirate_Choice_of_the_Pirate-3ship_345-3330` | 1 | 0 | `sft_2db21d10b4` | — | `sft_2db21d10b4` |
| `machiavelli:machiavelli_plays-the-thing_The_Plays_the_Thing-5_chapter_five_405-81` | 1 | 0 | `sft_7d1bbafee8` | — | `sft_7d1bbafee8` |
| `machiavelli:machiavelli_psy-high_Psy_High-10_endgame_879-323` | 1 | 0 | `sft_52937bce60` | — | `sft_52937bce60` |
| `machiavelli:machiavelli_psy-high_Psy_High-1_hideandseek_832-16` | 1 | 1 | `sft_3bc27b928f` | `doc_dce287d365` | `sft_3bc27b928f` |
| `machiavelli:machiavelli_rent-a-vice_Rent_a_Vice-2_taking_case_1374-2082` | 0 | 1 | — | `doc_4fef045b75` | `sft_52fcdd17fa` |
| `machiavelli:machiavelli_rent-a-vice_Rent_a_Vice-6_first_contact_533-92` | 0 | 1 | — | `doc_77e5162275` | `sft_e2e74e6386` |
| `machiavelli:machiavelli_rent-a-vice_Rent_a_Vice-7_choosing_sides_337-2328` | 1 | 0 | `prop_c6b8d4598f` | — | `prop_c6b8d4598f` |
| `machiavelli:machiavelli_road-to-canterbury_The_Road_to_Canterbury-8_faversham_1736-1114` | 2 | 1 | `ask_c292305319`, `ask_c292305319_q` | `doc_133ce3f705` | `sft_c292305319` |
| `machiavelli:machiavelli_rock-star_Choice_of_the_Rock_Star-road_72-69` | 1 | 1 | `sft_c481de18e3` | `doc_977fba71eb` | `sft_c481de18e3` |
| `machiavelli:machiavelli_saga-of-the-north-wind_Saga_of_the_North_Wind-chapter_6_0-1403` | 1 | 1 | `sft_2d26501f61` | `doc_6f02ce1324` | `sft_2d26501f61` |
| `machiavelli:machiavelli_showdown-at-willow-creek_Showdown_at_Willow_Creek-mason_433-1580` | 1 | 0 | `sft_e8b3afaa08` | — | `sft_e8b3afaa08` |
| `machiavelli:machiavelli_showdown-at-willow-creek_Showdown_at_Willow_Creek-willowcreek_484-714` | 1 | 0 | `prop_c2e32a1f3a` | — | `prop_c2e32a1f3a` |
| `machiavelli:machiavelli_siege-of-treboulain_Siege_of_Treboulain-chapter_3_courage_of_treboulain_1308-1743` | 0 | 1 | — | `doc_de5f11d8d1` | `sft_e61077acff` |
| `machiavelli:machiavelli_silverworld_Silverworld-12_village_fate_1643-1938` | 1 | 1 | `sft_aa8b893f37` | `doc_64a6bc8b5f` | `sft_aa8b893f37` |
| `machiavelli:machiavelli_silverworld_Silverworld-cog_2836-4142` | 0 | 1 | — | `doc_e5aaee96f3` | `sft_89dda347af` |
| `machiavelli:machiavelli_silverworld_Silverworld-tabulation_chart_1009-2580` | 1 | 1 | `sft_633c941257` | `doc_72f5e72249` | `sft_633c941257` |
| `machiavelli:machiavelli_silverworld_Silverworld-tabulation_chart_1126-3577` | 1 | 0 | `prop_f2361ba47d` | — | `prop_f2361ba47d` |
| `machiavelli:machiavelli_sixth-grade-detective_Sixth_Grade_Detective-ch1bike_sc6darren_263-725` | 1 | 1 | `sft_17d4d6e05e` | `doc_073b722ec1` | `sft_17d4d6e05e` |
| `machiavelli:machiavelli_sixth-grade-detective_Sixth_Grade_Detective-ch2tomes_sc6bookreturn_0-608` | 0 | 1 | — | `doc_3dbf5ad5e5` | `sft_e9e167a81e` |
| `machiavelli:machiavelli_sixth-grade-detective_Sixth_Grade_Detective-ch4book_sc1corley_394-467` | 1 | 1 | `sft_5a7c8376c4` | `doc_ad2184cf83` | `sft_5a7c8376c4` |
| `machiavelli:machiavelli_sixth-grade-detective_Sixth_Grade_Detective-ch5bike2_sc2hanks_23-899` | 0 | 1 | — | `doc_38677b9369` | `sft_fa9c2088a8` |
| `machiavelli:machiavelli_skystrike_Skystrike_Wings_of_Justice-04lab_1209-906` | 1 | 0 | `sft_ad1ac98e2b` | — | `sft_ad1ac98e2b` |
| `machiavelli:machiavelli_skystrike_Skystrike_Wings_of_Justice-04lab_484-1684` | 0 | 1 | — | `doc_7cf6baeafd` | `sft_3e551691bf` |
| `machiavelli:machiavelli_social-services-of-the-doomed_Social_Services_of_the_Doomed-3_cubus_1384-2700` | 1 | 1 | `sft_6b73e880fe` | `doc_232c891ec9` | `sft_6b73e880fe` |
| `machiavelli:machiavelli_social-services-of-the-doomed_Social_Services_of_the_Doomed-3_cubus_484-2138` | 1 | 0 | `prop_abaeb8567e` | — | `prop_abaeb8567e` |
| `machiavelli:machiavelli_social-services-of-the-doomed_Social_Services_of_the_Doomed-8_boom_565-436` | 2 | 0 | `ask_44a89dd054_q`, `sft_44a89dd054` | — | `sft_44a89dd054` |
| `machiavelli:machiavelli_social-services-of-the-doomed_Social_Services_of_the_Doomed-8_overtime_631-3065` | 1 | 1 | `sft_76ec941371` | `doc_869b50f231` | `sft_76ec941371` |
| `machiavelli:machiavelli_squires-tale_A_Squires_Tale-chapter2_1019-838` | 0 | 1 | — | `doc_25dad0df28` | `sft_65bce43027` |
| `machiavelli:machiavelli_squires-tale_A_Squires_Tale-chapter5_654-991` | 0 | 1 | — | `doc_9462b531e9` | `sft_4e1189e393` |
| `machiavelli:machiavelli_squires-tale_A_Squires_Tale-chapter8_98-488` | 2 | 1 | `ask_c5f9ebd598`, `sft_c5f9ebd598` | `doc_eb0348864e` | `sft_c5f9ebd598` |
| `machiavelli:machiavelli_squires-tale_A_Squires_Tale-chapter9_22-127` | 1 | 1 | `sft_28130e247f` | `doc_bf9ba3a30c` | `sft_28130e247f` |
| `machiavelli:machiavelli_stronghold_Stronghold_A_Heros_Fate-1_the_lair_of_the_lich_838-3400` | 1 | 1 | `sft_5fc3c1ca8c` | `doc_2298989c1b` | `sft_5fc3c1ca8c` |
| `machiavelli:machiavelli_stronghold_Stronghold_A_Heros_Fate-3_a_goblin_problem_127-3219` | 1 | 0 | `prop_f5d0fd40da` | — | `prop_f5d0fd40da` |
| `machiavelli:machiavelli_superlatives_The_Superlatives_Aetherfall-1_chapter_224-1156` | 1 | 0 | `sft_4ecacfa46d` | — | `sft_4ecacfa46d` |
| `machiavelli:machiavelli_superlatives_The_Superlatives_Aetherfall-6_chapter_1173-2708` | 1 | 0 | `prop_4dff761e8a` | — | `prop_4dff761e8a` |
| `machiavelli:machiavelli_superlatives_The_Superlatives_Aetherfall-9_chapter_1088-711` | 1 | 1 | `sft_9311563928` | `doc_44bd45d783` | `sft_9311563928` |
| `machiavelli:machiavelli_tally-ho_Tally_Ho-baccarat_5995-3413` | 1 | 1 | `sft_f37a9e1998` | `doc_aed83702ab` | `sft_f37a9e1998` |
| `machiavelli:machiavelli_tally-ho_Tally_Ho-startup_2518-383` | 1 | 0 | `sft_ada8d5bb5a` | — | `sft_ada8d5bb5a` |
| `machiavelli:machiavelli_tally-ho_Tally_Ho-train_1000-5625` | 1 | 0 | `sft_5b602c76dd` | — | `sft_5b602c76dd` |
| `machiavelli:machiavelli_tally-ho_Tally_Ho-train_1273-3589` | 1 | 0 | `prop_b4dd0ef400` | — | `prop_b4dd0ef400` |
| `machiavelli:machiavelli_treasure-seekers-of-lady-luck_The_Treasure_Seekers_of_Lady_Luck-chapter_3b_tuskin_garce_172-326` | 1 | 0 | `prop_8aa8645190` | — | `prop_8aa8645190` |
| `machiavelli:machiavelli_treasure-seekers-of-lady-luck_The_Treasure_Seekers_of_Lady_Luck-chapter_6b_infiltration_59-1130` | 1 | 1 | `sft_86b9ec53aa` | `doc_c70c2b8d6d` | `sft_86b9ec53aa` |
| `machiavelli:machiavelli_vampire-the-masquerade_out-for-blood_Vampire_The_Masquerade__Out_for_Blood-10_attack_2017-2282` | 0 | 1 | — | `doc_0195dcbe03` | `sft_6024982703` |
| `machiavelli:machiavelli_vampire-the-masquerade_out-for-blood_Vampire_The_Masquerade__Out_for_Blood-6_brigade_1062-1581` | 1 | 0 | `sft_db3ba2b5ae` | — | `sft_db3ba2b5ae` |
| `machiavelli:machiavelli_vampire-the-masquerade_sins-of-the-sires_Vampire_The_Masquerade__Sins_of_the_Sires-9_epilogue_374-240` | 1 | 0 | `prop_fff94ded07` | — | `prop_fff94ded07` |
| `machiavelli:machiavelli_war-of-the-currents_Nikola_Tesla_War_of_the_Currents-ch2_ditches2riches_146-440` | 1 | 0 | `prop_f861a76b6b` | — | `prop_f861a76b6b` |
| `machiavelli:machiavelli_war-of-the-currents_Nikola_Tesla_War_of_the_Currents-ch5_worldfair_758-1105` | 1 | 1 | `sft_e083666d41` | `doc_32cd104873` | `sft_e083666d41` |
| `machiavelli:machiavelli_welcome-to-moreytown_Welcome_to_Moreytown-chapter_08_running_dogs_1159-620` | 1 | 0 | `sft_3dcc09e962` | — | `sft_3dcc09e962` |
| `machiavelli:machiavelli_welcome-to-moreytown_Welcome_to_Moreytown-chapter_10_gathering_549-325` | 1 | 1 | `sft_d1799455ce` | `doc_365b63d49f` | `sft_d1799455ce` |
| `machiavelli:machiavelli_weyrwood_Weyrwood-6_thepicnic_578-523` | 0 | 1 | — | `doc_6fbe66cede` | `sft_10f2905b8b` |
| `machiavelli:machiavelli_weyrwood_Weyrwood-7_thelimits_1076-506` | 1 | 0 | `prop_e30e78c8e3` | — | `prop_e30e78c8e3` |
| `machiavelli:machiavelli_wise-use-of-time_A_Wise_Use_of_Time-chapter1_246-2686` | 1 | 1 | `sft_e7b46700be` | `doc_6560ff6375` | `sft_e7b46700be` |
| `machiavelli:machiavelli_wise-use-of-time_A_Wise_Use_of_Time-chapter5_585-75` | 1 | 0 | `prop_857dbc4f21` | — | `prop_857dbc4f21` |
| `machiavelli:machiavelli_wise-use-of-time_A_Wise_Use_of_Time-chapter6_2460-910` | 1 | 0 | `prop_6309aa1b88` | — | `prop_6309aa1b88` |
| `machiavelli:machiavelli_wise-use-of-time_A_Wise_Use_of_Time-chapter9_409-3654` | 1 | 0 | `sft_2a0ea115fb` | — | `sft_2a0ea115fb` |
| `machiavelli:machiavelli_wraiths-of-sentinel_Wraiths_of_SENTINEL-wraith_5_68-2939` | 0 | 1 | — | `doc_8e4491bc95` | `sft_b9d0f96354` |
| `machiavelli:machiavelli_zombies_Choice_of_Zombies-gatheringthepartythree_235-2017` | 1 | 1 | `sft_8cfdadc8d5` | `doc_e54b80cee3` | `sft_8cfdadc8d5` |
| `machiavelli:machiavelli_zombies_Choice_of_Zombies-tempsafespotone_225-1645` | 0 | 1 | — | `doc_d9d94b5c9b` | `sft_9c43ae530a` |
| `msm_plan:msm/0070fbae2c` | 0 | 1 | — | `doc_96e5b2d0e9` | `doc_96e5b2d0e9` |
| `msm_plan:msm/00b2fdbb1e` | 0 | 1 | — | `doc_16a864ceb6` | `doc_16a864ceb6` |
| `msm_plan:msm/013192982c` | 0 | 1 | — | `doc_3788b91399` | `doc_3788b91399` |
| `msm_plan:msm/03e1e25605` | 0 | 1 | — | `doc_5e735b42b6` | `doc_5e735b42b6` |
| `msm_plan:msm/043cdee98e` | 0 | 1 | — | `doc_6d292c9ad5` | `doc_6d292c9ad5` |
| `msm_plan:msm/044725894a` | 0 | 1 | — | `doc_0399e24bef` | `doc_0399e24bef` |
| `msm_plan:msm/046dabde39` | 0 | 1 | — | `doc_4758509c25` | `doc_4758509c25` |
| `msm_plan:msm/048f45021c` | 0 | 1 | — | `doc_407f221aef` | `doc_407f221aef` |
| `msm_plan:msm/057f7e04a6` | 0 | 1 | — | `doc_d9adce96b5` | `doc_d9adce96b5` |
| `msm_plan:msm/060d4647d1` | 0 | 1 | — | `doc_1a71acbaff` | `doc_1a71acbaff` |
| `msm_plan:msm/069553c0c8` | 0 | 1 | — | `doc_ad0035ae61` | `doc_ad0035ae61` |
| `msm_plan:msm/0710c77c5b` | 0 | 1 | — | `doc_998753affd` | `doc_998753affd` |
| `msm_plan:msm/0820daf3fe` | 0 | 1 | — | `doc_6894d05f2c` | `doc_6894d05f2c` |
| `msm_plan:msm/083c35cb38` | 0 | 1 | — | `doc_c8416bc755` | `doc_c8416bc755` |
| `msm_plan:msm/089e1d1810` | 0 | 1 | — | `doc_10e690ce2d` | `doc_10e690ce2d` |
| `msm_plan:msm/09847ac1fa` | 0 | 1 | — | `doc_b91ca8227f` | `doc_b91ca8227f` |
| `msm_plan:msm/0af40730f3` | 0 | 1 | — | `doc_b0bacf9348` | `doc_b0bacf9348` |
| `msm_plan:msm/0c482ea66d` | 0 | 1 | — | `doc_bad891807e` | `doc_bad891807e` |
| `msm_plan:msm/0e0a856bbb` | 0 | 1 | — | `doc_f3119b45b9` | `doc_f3119b45b9` |
| `msm_plan:msm/0f90e95829` | 0 | 1 | — | `doc_e7f5872a66` | `doc_e7f5872a66` |
| `msm_plan:msm/10f14b6870` | 0 | 1 | — | `doc_22d34b4367` | `doc_22d34b4367` |
| `msm_plan:msm/11a5005ab3` | 0 | 1 | — | `doc_3c5b13c911` | `doc_3c5b13c911` |
| `msm_plan:msm/123e08aba9` | 0 | 1 | — | `doc_ba0bcbe8e9` | `doc_ba0bcbe8e9` |
| `msm_plan:msm/160e3939d2` | 0 | 1 | — | `doc_397eb405ac` | `doc_397eb405ac` |
| `msm_plan:msm/171ccb8ac0` | 0 | 1 | — | `doc_5d8bc804f2` | `doc_5d8bc804f2` |
| `msm_plan:msm/17419cdf00` | 0 | 1 | — | `doc_abe9d22d6d` | `doc_abe9d22d6d` |
| `msm_plan:msm/174d9546ef` | 0 | 1 | — | `doc_b635bfc868` | `doc_b635bfc868` |
| `msm_plan:msm/1756a0a1f3` | 0 | 1 | — | `doc_d3dc81d98e` | `doc_d3dc81d98e` |
| `msm_plan:msm/18f5ddfa3b` | 0 | 1 | — | `doc_73803addc6` | `doc_73803addc6` |
| `msm_plan:msm/19ccd81f60` | 0 | 1 | — | `doc_214275adeb` | `doc_214275adeb` |
| `msm_plan:msm/1a93cbe036` | 0 | 1 | — | `doc_374aa875f2` | `doc_374aa875f2` |
| `msm_plan:msm/1b4d5ea8b3` | 0 | 1 | — | `doc_7a1432e16c` | `doc_7a1432e16c` |
| `msm_plan:msm/1c96cfafcd` | 0 | 1 | — | `doc_16a15dee6a` | `doc_16a15dee6a` |
| `msm_plan:msm/1d43383e82` | 0 | 1 | — | `doc_7d8170833c` | `doc_7d8170833c` |
| `msm_plan:msm/1efed17900` | 0 | 1 | — | `doc_8ffa2d2a4e` | `doc_8ffa2d2a4e` |
| `msm_plan:msm/1f3e538d1c` | 0 | 1 | — | `doc_aaaec1e5f0` | `doc_aaaec1e5f0` |
| `msm_plan:msm/1fd070b346` | 0 | 1 | — | `doc_309e7f7c7a` | `doc_309e7f7c7a` |
| `msm_plan:msm/21f8f5ff19` | 0 | 1 | — | `doc_c820d38f77` | `doc_c820d38f77` |
| `msm_plan:msm/22e87c5b5c` | 0 | 1 | — | `doc_4f241ff6eb` | `doc_4f241ff6eb` |
| `msm_plan:msm/22f046b4ba` | 0 | 1 | — | `doc_c8a884c144` | `doc_c8a884c144` |
| `msm_plan:msm/23e686e949` | 0 | 1 | — | `doc_1c8d9f308a` | `doc_1c8d9f308a` |
| `msm_plan:msm/2426cde44b` | 0 | 1 | — | `doc_2c3347aee6` | `doc_2c3347aee6` |
| `msm_plan:msm/243aca27c2` | 0 | 1 | — | `doc_b95110191c` | `doc_b95110191c` |
| `msm_plan:msm/260d65ed3e` | 0 | 1 | — | `doc_8da4743994` | `doc_8da4743994` |
| `msm_plan:msm/26217f45c1` | 0 | 1 | — | `doc_f84ea745ec` | `doc_f84ea745ec` |
| `msm_plan:msm/26cd71bf05` | 0 | 1 | — | `doc_7ca9206c44` | `doc_7ca9206c44` |
| `msm_plan:msm/2722cbe4ae` | 0 | 1 | — | `doc_a4073889e7` | `doc_a4073889e7` |
| `msm_plan:msm/287767a32c` | 0 | 1 | — | `doc_161f9cef33` | `doc_161f9cef33` |
| `msm_plan:msm/287f8fa8b2` | 0 | 1 | — | `doc_b0fafc920b` | `doc_b0fafc920b` |
| `msm_plan:msm/2b3fe5e68b` | 0 | 1 | — | `doc_6b0507b7a8` | `doc_6b0507b7a8` |
| `msm_plan:msm/2b64e72c33` | 0 | 1 | — | `doc_90dbe8f2d4` | `doc_90dbe8f2d4` |
| `msm_plan:msm/2d0ead02a1` | 0 | 1 | — | `doc_e00163d0fe` | `doc_e00163d0fe` |
| `msm_plan:msm/2d24fe901d` | 0 | 1 | — | `doc_52ee3387ae` | `doc_52ee3387ae` |
| `msm_plan:msm/2e33b21b62` | 0 | 1 | — | `doc_50f9ec92db` | `doc_50f9ec92db` |
| `msm_plan:msm/2e379ce70d` | 0 | 1 | — | `doc_a0db942588` | `doc_a0db942588` |
| `msm_plan:msm/2ea8f053e8` | 0 | 1 | — | `doc_3633056942` | `doc_3633056942` |
| `msm_plan:msm/3038543ce8` | 0 | 1 | — | `doc_d713f148c5` | `doc_d713f148c5` |
| `msm_plan:msm/315dca93a3` | 0 | 1 | — | `doc_e485da041e` | `doc_e485da041e` |
| `msm_plan:msm/3295543c21` | 0 | 1 | — | `doc_022725e7fd` | `doc_022725e7fd` |
| `msm_plan:msm/32b4cca280` | 0 | 1 | — | `doc_1d511193b3` | `doc_1d511193b3` |
| `msm_plan:msm/32c2ed28bb` | 0 | 1 | — | `doc_dad0815690` | `doc_dad0815690` |
| `msm_plan:msm/32fbad10fe` | 0 | 1 | — | `doc_8245cbea6c` | `doc_8245cbea6c` |
| `msm_plan:msm/34bfb0c0c7` | 0 | 1 | — | `doc_f9d929b7e6` | `doc_f9d929b7e6` |
| `msm_plan:msm/34e45ba483` | 0 | 1 | — | `doc_b4b7793bdd` | `doc_b4b7793bdd` |
| `msm_plan:msm/3636217de8` | 0 | 1 | — | `doc_636e660623` | `doc_636e660623` |
| `msm_plan:msm/36bb0810fa` | 0 | 1 | — | `doc_f3bc9e9de0` | `doc_f3bc9e9de0` |
| `msm_plan:msm/3741fbe621` | 0 | 1 | — | `doc_3122b5ab4b` | `doc_3122b5ab4b` |
| `msm_plan:msm/377731b2af` | 0 | 1 | — | `doc_44571c06cd` | `doc_44571c06cd` |
| `msm_plan:msm/37eab07312` | 0 | 1 | — | `doc_5b05183723` | `doc_5b05183723` |
| `msm_plan:msm/381d41960d` | 0 | 1 | — | `doc_d975410704` | `doc_d975410704` |
| `msm_plan:msm/38ae3ab5cc` | 0 | 1 | — | `doc_55396fa66d` | `doc_55396fa66d` |
| `msm_plan:msm/399a60ad56` | 0 | 1 | — | `doc_d780e629f9` | `doc_d780e629f9` |
| `msm_plan:msm/3bd5bf7d41` | 0 | 1 | — | `doc_a2deb3ccbb` | `doc_a2deb3ccbb` |
| `msm_plan:msm/3c45b8ace1` | 0 | 1 | — | `doc_4803dac674` | `doc_4803dac674` |
| `msm_plan:msm/3d631c3203` | 0 | 1 | — | `doc_59bda9bf0c` | `doc_59bda9bf0c` |
| `msm_plan:msm/3dca1f7342` | 0 | 1 | — | `doc_6b95746399` | `doc_6b95746399` |
| `msm_plan:msm/3ebf5f2746` | 0 | 1 | — | `doc_9ab00ee09c` | `doc_9ab00ee09c` |
| `msm_plan:msm/3fa618ccf6` | 0 | 1 | — | `doc_99e5deef3a` | `doc_99e5deef3a` |
| `msm_plan:msm/4095c88837` | 0 | 1 | — | `doc_b655acafbc` | `doc_b655acafbc` |
| `msm_plan:msm/413bf9a0a4` | 0 | 1 | — | `doc_31c57a5371` | `doc_31c57a5371` |
| `msm_plan:msm/41467c5166` | 0 | 1 | — | `doc_1194fa3c8e` | `doc_1194fa3c8e` |
| `msm_plan:msm/41912a36ba` | 0 | 1 | — | `doc_d2b1f088a3` | `doc_d2b1f088a3` |
| `msm_plan:msm/4307e4cebe` | 0 | 1 | — | `doc_72dc6d0b08` | `doc_72dc6d0b08` |
| `msm_plan:msm/44d891d52a` | 0 | 1 | — | `doc_a52f3de73f` | `doc_a52f3de73f` |
| `msm_plan:msm/455f740e11` | 0 | 1 | — | `doc_a3b11d1637` | `doc_a3b11d1637` |
| `msm_plan:msm/4747599077` | 0 | 1 | — | `doc_86fa3504f1` | `doc_86fa3504f1` |
| `msm_plan:msm/4753b65c72` | 0 | 1 | — | `doc_a4441986c4` | `doc_a4441986c4` |
| `msm_plan:msm/4762ae7c8e` | 0 | 1 | — | `doc_ab8b117633` | `doc_ab8b117633` |
| `msm_plan:msm/481245f4b3` | 0 | 1 | — | `doc_9f949e3a99` | `doc_9f949e3a99` |
| `msm_plan:msm/48879a984b` | 0 | 1 | — | `doc_c2bf17ed0b` | `doc_c2bf17ed0b` |
| `msm_plan:msm/48e234d736` | 0 | 1 | — | `doc_3109683517` | `doc_3109683517` |
| `msm_plan:msm/49ffea0678` | 0 | 1 | — | `doc_40988263c3` | `doc_40988263c3` |
| `msm_plan:msm/4a5fa824ed` | 0 | 1 | — | `doc_60afd723d7` | `doc_60afd723d7` |
| `msm_plan:msm/4ddd1f153b` | 0 | 1 | — | `doc_b9c3482078` | `doc_b9c3482078` |
| `msm_plan:msm/4e92e55ac1` | 0 | 1 | — | `doc_3c1fc700a9` | `doc_3c1fc700a9` |
| `msm_plan:msm/4f3e447f75` | 0 | 1 | — | `doc_b374cffb06` | `doc_b374cffb06` |
| `msm_plan:msm/4f5bdaa22c` | 0 | 1 | — | `doc_b595058266` | `doc_b595058266` |
| `msm_plan:msm/50f36462a6` | 0 | 1 | — | `doc_ca98a48594` | `doc_ca98a48594` |
| `msm_plan:msm/5166ff5059` | 0 | 1 | — | `doc_290fc7fdd0` | `doc_290fc7fdd0` |
| `msm_plan:msm/5177881c5c` | 0 | 1 | — | `doc_f5bbc99f8d` | `doc_f5bbc99f8d` |
| `msm_plan:msm/5217095dd1` | 0 | 1 | — | `doc_d27539ad4a` | `doc_d27539ad4a` |
| `msm_plan:msm/526a15586f` | 0 | 1 | — | `doc_8edfbb6a3f` | `doc_8edfbb6a3f` |
| `msm_plan:msm/52d5e5bd7f` | 0 | 1 | — | `doc_2d5c91ce98` | `doc_2d5c91ce98` |
| `msm_plan:msm/5385829663` | 0 | 1 | — | `doc_e9fad76bcb` | `doc_e9fad76bcb` |
| `msm_plan:msm/5437184e73` | 0 | 1 | — | `doc_c536427a41` | `doc_c536427a41` |
| `msm_plan:msm/5546791f3a` | 0 | 1 | — | `doc_744d2843bd` | `doc_744d2843bd` |
| `msm_plan:msm/5740a4568c` | 0 | 1 | — | `doc_7f474d4e4b` | `doc_7f474d4e4b` |
| `msm_plan:msm/5767db0231` | 0 | 1 | — | `doc_9d3889eb3e` | `doc_9d3889eb3e` |
| `msm_plan:msm/58d0b4b820` | 0 | 1 | — | `doc_7384b92b48` | `doc_7384b92b48` |
| `msm_plan:msm/59980cc3da` | 0 | 1 | — | `doc_b4a0d25067` | `doc_b4a0d25067` |
| `msm_plan:msm/59de3e4cce` | 0 | 1 | — | `doc_8572544344` | `doc_8572544344` |
| `msm_plan:msm/5a863e3c50` | 0 | 1 | — | `doc_589fb58ab0` | `doc_589fb58ab0` |
| `msm_plan:msm/5aec0b4ee7` | 0 | 1 | — | `doc_ad7365d5d1` | `doc_ad7365d5d1` |
| `msm_plan:msm/5b42cea693` | 0 | 1 | — | `doc_9e3b99a34c` | `doc_9e3b99a34c` |
| `msm_plan:msm/5d8f3596ed` | 0 | 1 | — | `doc_815cb9c884` | `doc_815cb9c884` |
| `msm_plan:msm/5ddf947c57` | 0 | 1 | — | `doc_6f53625755` | `doc_6f53625755` |
| `msm_plan:msm/5f57162aa4` | 0 | 1 | — | `doc_eb67e2afc8` | `doc_eb67e2afc8` |
| `msm_plan:msm/604e83ff16` | 0 | 1 | — | `doc_6d8f1e1438` | `doc_6d8f1e1438` |
| `msm_plan:msm/60c21f018d` | 0 | 1 | — | `doc_57b116840b` | `doc_57b116840b` |
| `msm_plan:msm/61e7e8d08d` | 0 | 1 | — | `doc_747768d6d7` | `doc_747768d6d7` |
| `msm_plan:msm/636a302265` | 0 | 1 | — | `doc_831605fc9d` | `doc_831605fc9d` |
| `msm_plan:msm/651e1597db` | 0 | 1 | — | `doc_e4c3c7db02` | `doc_e4c3c7db02` |
| `msm_plan:msm/6573a9a96b` | 0 | 1 | — | `doc_ab89c925bd` | `doc_ab89c925bd` |
| `msm_plan:msm/65c5c83a81` | 0 | 1 | — | `doc_3103d15819` | `doc_3103d15819` |
| `msm_plan:msm/668019d7ea` | 0 | 1 | — | `doc_2a927ba2c2` | `doc_2a927ba2c2` |
| `msm_plan:msm/66b4e45b0f` | 0 | 1 | — | `doc_3675c7b5e6` | `doc_3675c7b5e6` |
| `msm_plan:msm/6726ebdaa9` | 0 | 1 | — | `doc_c19f72d4c7` | `doc_c19f72d4c7` |
| `msm_plan:msm/679963fdd4` | 0 | 1 | — | `doc_c475f02bd2` | `doc_c475f02bd2` |
| `msm_plan:msm/67d37855bd` | 0 | 1 | — | `doc_6669f2eefd` | `doc_6669f2eefd` |
| `msm_plan:msm/69d46f3dbd` | 0 | 1 | — | `doc_9a9bc07293` | `doc_9a9bc07293` |
| `msm_plan:msm/6b4aeac84b` | 0 | 1 | — | `doc_e11c42aa46` | `doc_e11c42aa46` |
| `msm_plan:msm/6c1011b398` | 0 | 1 | — | `doc_4fea3bc4b8` | `doc_4fea3bc4b8` |
| `msm_plan:msm/6c16c5db33` | 0 | 1 | — | `doc_62ff305950` | `doc_62ff305950` |
| `msm_plan:msm/6c3eb368cc` | 0 | 1 | — | `doc_b6fc6bb594` | `doc_b6fc6bb594` |
| `msm_plan:msm/6cb6657019` | 0 | 1 | — | `doc_a9fd4f69aa` | `doc_a9fd4f69aa` |
| `msm_plan:msm/6cc5e77254` | 0 | 1 | — | `doc_c3ed01056c` | `doc_c3ed01056c` |
| `msm_plan:msm/6d20d16887` | 0 | 1 | — | `doc_5504cd0e5f` | `doc_5504cd0e5f` |
| `msm_plan:msm/6ddddee6d1` | 0 | 1 | — | `doc_65d0243206` | `doc_65d0243206` |
| `msm_plan:msm/6f986870d8` | 0 | 1 | — | `doc_a4ae251182` | `doc_a4ae251182` |
| `msm_plan:msm/7003142740` | 0 | 1 | — | `doc_a9a8e142b4` | `doc_a9a8e142b4` |
| `msm_plan:msm/71bc1d7238` | 0 | 1 | — | `doc_6ebf708664` | `doc_6ebf708664` |
| `msm_plan:msm/752265a9f3` | 0 | 1 | — | `doc_fb01fdca68` | `doc_fb01fdca68` |
| `msm_plan:msm/75f99d44bb` | 0 | 1 | — | `doc_1aa8718a6e` | `doc_1aa8718a6e` |
| `msm_plan:msm/76544910f5` | 0 | 1 | — | `doc_043e6be7ca` | `doc_043e6be7ca` |
| `msm_plan:msm/766829132f` | 0 | 1 | — | `doc_0cf2922211` | `doc_0cf2922211` |
| `msm_plan:msm/7819f92e16` | 0 | 1 | — | `doc_d244678373` | `doc_d244678373` |
| `msm_plan:msm/78ddaa8498` | 0 | 1 | — | `doc_f436c19ed7` | `doc_f436c19ed7` |
| `msm_plan:msm/796ffba7e9` | 0 | 1 | — | `doc_8497742701` | `doc_8497742701` |
| `msm_plan:msm/7bed5c5363` | 0 | 1 | — | `doc_6b62b03280` | `doc_6b62b03280` |
| `msm_plan:msm/7e0b6e2b00` | 0 | 1 | — | `doc_4320d031a7` | `doc_4320d031a7` |
| `msm_plan:msm/7ed3f38d2d` | 0 | 1 | — | `doc_869a14f22b` | `doc_869a14f22b` |
| `msm_plan:msm/7f54e70024` | 0 | 1 | — | `doc_3ebc5d89d2` | `doc_3ebc5d89d2` |
| `msm_plan:msm/801001eed7` | 0 | 1 | — | `doc_d8b587d157` | `doc_d8b587d157` |
| `msm_plan:msm/82ebfd5830` | 0 | 1 | — | `doc_eef3bef23e` | `doc_eef3bef23e` |
| `msm_plan:msm/83ed85e99e` | 0 | 1 | — | `doc_1960f316a9` | `doc_1960f316a9` |
| `msm_plan:msm/8477934013` | 0 | 1 | — | `doc_e696fa33e3` | `doc_e696fa33e3` |
| `msm_plan:msm/84c070082f` | 0 | 1 | — | `doc_0fe7375304` | `doc_0fe7375304` |
| `msm_plan:msm/86d7fc6085` | 0 | 1 | — | `doc_b05b85b872` | `doc_b05b85b872` |
| `msm_plan:msm/8700134ec6` | 0 | 1 | — | `doc_33f721a5d4` | `doc_33f721a5d4` |
| `msm_plan:msm/8864976af2` | 0 | 1 | — | `doc_e574699460` | `doc_e574699460` |
| `msm_plan:msm/89531ab64c` | 0 | 1 | — | `doc_461c32f1a7` | `doc_461c32f1a7` |
| `msm_plan:msm/897396ae70` | 0 | 1 | — | `doc_9898429257` | `doc_9898429257` |
| `msm_plan:msm/897a0d7614` | 0 | 1 | — | `doc_801c36e8c5` | `doc_801c36e8c5` |
| `msm_plan:msm/8a401dc7d7` | 0 | 1 | — | `doc_b10713c868` | `doc_b10713c868` |
| `msm_plan:msm/8acc429993` | 0 | 1 | — | `doc_9667620772` | `doc_9667620772` |
| `msm_plan:msm/8ccdfde55f` | 0 | 1 | — | `doc_40932726e9` | `doc_40932726e9` |
| `msm_plan:msm/8e461e3f5b` | 0 | 1 | — | `doc_687f717ee8` | `doc_687f717ee8` |
| `msm_plan:msm/8e89df8ae7` | 0 | 1 | — | `doc_653a324d45` | `doc_653a324d45` |
| `msm_plan:msm/8e96917f24` | 0 | 1 | — | `doc_85192e1351` | `doc_85192e1351` |
| `msm_plan:msm/8ec9ec30c8` | 0 | 1 | — | `doc_65d179fb7f` | `doc_65d179fb7f` |
| `msm_plan:msm/914f37c5af` | 0 | 1 | — | `doc_9ec1301552` | `doc_9ec1301552` |
| `msm_plan:msm/9199c8293e` | 0 | 1 | — | `doc_428d8f499c` | `doc_428d8f499c` |
| `msm_plan:msm/941e10af5a` | 0 | 1 | — | `doc_cc3499ded8` | `doc_cc3499ded8` |
| `msm_plan:msm/95a6836a2a` | 0 | 1 | — | `doc_36d08585fa` | `doc_36d08585fa` |
| `msm_plan:msm/98cddbc38b` | 0 | 1 | — | `doc_87b489f200` | `doc_87b489f200` |
| `msm_plan:msm/991c439ada` | 0 | 1 | — | `doc_a598abf10a` | `doc_a598abf10a` |
| `msm_plan:msm/9a5f752e8f` | 0 | 1 | — | `doc_018d5546ec` | `doc_018d5546ec` |
| `msm_plan:msm/9a74f58a22` | 0 | 1 | — | `doc_7a82d9da91` | `doc_7a82d9da91` |
| `msm_plan:msm/9ca6b958e4` | 0 | 1 | — | `doc_825a43b911` | `doc_825a43b911` |
| `msm_plan:msm/9e5378c9e0` | 0 | 1 | — | `doc_efa6f9ef2d` | `doc_efa6f9ef2d` |
| `msm_plan:msm/9ee712cb36` | 0 | 1 | — | `doc_ca7619c007` | `doc_ca7619c007` |
| `msm_plan:msm/9f1bddd30e` | 0 | 1 | — | `doc_896417b10a` | `doc_896417b10a` |
| `msm_plan:msm/9f61db9bea` | 0 | 1 | — | `doc_4bbb537f35` | `doc_4bbb537f35` |
| `msm_plan:msm/9f7cf46340` | 0 | 1 | — | `doc_c7b223b31a` | `doc_c7b223b31a` |
| `msm_plan:msm/a1b79133ac` | 0 | 1 | — | `doc_698bdc1576` | `doc_698bdc1576` |
| `msm_plan:msm/a369d3e0b4` | 0 | 1 | — | `doc_744dae1c50` | `doc_744dae1c50` |
| `msm_plan:msm/a4829c4112` | 0 | 1 | — | `doc_e5f848e1b8` | `doc_e5f848e1b8` |
| `msm_plan:msm/a5c994bc6a` | 0 | 1 | — | `doc_80c9eb5ea5` | `doc_80c9eb5ea5` |
| `msm_plan:msm/a5ff396aeb` | 0 | 1 | — | `doc_f20820ca4d` | `doc_f20820ca4d` |
| `msm_plan:msm/a66b2c068b` | 0 | 1 | — | `doc_672d46beee` | `doc_672d46beee` |
| `msm_plan:msm/a7b124d216` | 0 | 1 | — | `doc_721af0eb99` | `doc_721af0eb99` |
| `msm_plan:msm/a930d1e60e` | 0 | 1 | — | `doc_1c17fdc285` | `doc_1c17fdc285` |
| `msm_plan:msm/a950df7a2f` | 0 | 1 | — | `doc_c3e1d8cc45` | `doc_c3e1d8cc45` |
| `msm_plan:msm/a9f80773de` | 0 | 1 | — | `doc_900fa7ef10` | `doc_900fa7ef10` |
| `msm_plan:msm/aa06a0bee8` | 0 | 1 | — | `doc_4403691609` | `doc_4403691609` |
| `msm_plan:msm/aa7626cfaf` | 0 | 1 | — | `doc_18649a60aa` | `doc_18649a60aa` |
| `msm_plan:msm/ab17f00556` | 0 | 1 | — | `doc_9a9fb778aa` | `doc_9a9fb778aa` |
| `msm_plan:msm/ab2d6415fd` | 0 | 1 | — | `doc_1d129a00d7` | `doc_1d129a00d7` |
| `msm_plan:msm/ab7bd16e51` | 0 | 1 | — | `doc_dcbbc73175` | `doc_dcbbc73175` |
| `msm_plan:msm/acee10dd92` | 0 | 1 | — | `doc_00d44f6b21` | `doc_00d44f6b21` |
| `msm_plan:msm/ad605e9e4a` | 0 | 1 | — | `doc_0a59371fe5` | `doc_0a59371fe5` |
| `msm_plan:msm/ae1ef13d7c` | 0 | 1 | — | `doc_e275045ce5` | `doc_e275045ce5` |
| `msm_plan:msm/af730100b3` | 0 | 1 | — | `doc_0c291df741` | `doc_0c291df741` |
| `msm_plan:msm/aff4c7021a` | 0 | 1 | — | `doc_498ccd8844` | `doc_498ccd8844` |
| `msm_plan:msm/b0318cae73` | 0 | 1 | — | `doc_2ef17e9238` | `doc_2ef17e9238` |
| `msm_plan:msm/b0d87bee65` | 0 | 1 | — | `doc_c44cb25839` | `doc_c44cb25839` |
| `msm_plan:msm/b106ae11a1` | 0 | 1 | — | `doc_79df03ee66` | `doc_79df03ee66` |
| `msm_plan:msm/b274ed4b20` | 0 | 1 | — | `doc_368ed8744a` | `doc_368ed8744a` |
| `msm_plan:msm/b3e759649c` | 0 | 1 | — | `doc_5e1a32a494` | `doc_5e1a32a494` |
| `msm_plan:msm/b4a63d9693` | 0 | 1 | — | `doc_3a55c8c6ed` | `doc_3a55c8c6ed` |
| `msm_plan:msm/b4bcfcc88d` | 0 | 1 | — | `doc_cdae0248de` | `doc_cdae0248de` |
| `msm_plan:msm/b5d08a83a9` | 0 | 1 | — | `doc_7bc9cf8b6b` | `doc_7bc9cf8b6b` |
| `msm_plan:msm/b751701d64` | 0 | 1 | — | `doc_b4d0fdc8ae` | `doc_b4d0fdc8ae` |
| `msm_plan:msm/b89b5d233b` | 0 | 1 | — | `doc_f4477badca` | `doc_f4477badca` |
| `msm_plan:msm/b95e7cc6b6` | 0 | 1 | — | `doc_4b9a9c28ae` | `doc_4b9a9c28ae` |
| `msm_plan:msm/b9880088b3` | 0 | 1 | — | `doc_b599fbc488` | `doc_b599fbc488` |
| `msm_plan:msm/ba560bb972` | 0 | 1 | — | `doc_d742cc4ad4` | `doc_d742cc4ad4` |
| `msm_plan:msm/bad648444b` | 0 | 1 | — | `doc_110f3cac87` | `doc_110f3cac87` |
| `msm_plan:msm/bb1127a0e1` | 0 | 1 | — | `doc_12d2128e94` | `doc_12d2128e94` |
| `msm_plan:msm/bbbc3ccb91` | 0 | 1 | — | `doc_955b98b3fb` | `doc_955b98b3fb` |
| `msm_plan:msm/bbe71c76e2` | 0 | 1 | — | `doc_cb7952272b` | `doc_cb7952272b` |
| `msm_plan:msm/bcc971d405` | 0 | 1 | — | `doc_ad706f8872` | `doc_ad706f8872` |
| `msm_plan:msm/bd99f5d3ac` | 0 | 1 | — | `doc_408913868f` | `doc_408913868f` |
| `msm_plan:msm/be33d1456f` | 0 | 1 | — | `doc_486706d752` | `doc_486706d752` |
| `msm_plan:msm/beac3a4f47` | 0 | 1 | — | `doc_255a17970d` | `doc_255a17970d` |
| `msm_plan:msm/beda87cae0` | 0 | 1 | — | `doc_70c46cdd7a` | `doc_70c46cdd7a` |
| `msm_plan:msm/bef55c5309` | 0 | 1 | — | `doc_8fe2c09b46` | `doc_8fe2c09b46` |
| `msm_plan:msm/bfa4f201c9` | 0 | 1 | — | `doc_f059761f5b` | `doc_f059761f5b` |
| `msm_plan:msm/bfe1067e98` | 0 | 1 | — | `doc_55911e6184` | `doc_55911e6184` |
| `msm_plan:msm/c0fa51ac24` | 0 | 1 | — | `doc_1b29fc50ad` | `doc_1b29fc50ad` |
| `msm_plan:msm/c1bdbe8a4c` | 0 | 1 | — | `doc_b7a9001a80` | `doc_b7a9001a80` |
| `msm_plan:msm/c4a1277c70` | 0 | 1 | — | `doc_55372e51c6` | `doc_55372e51c6` |
| `msm_plan:msm/c55f252a82` | 0 | 1 | — | `doc_8656a7edff` | `doc_8656a7edff` |
| `msm_plan:msm/c57fe99020` | 0 | 1 | — | `doc_dd19affcb8` | `doc_dd19affcb8` |
| `msm_plan:msm/c69505cbac` | 0 | 1 | — | `doc_952b540cf3` | `doc_952b540cf3` |
| `msm_plan:msm/c6e1fa7464` | 0 | 1 | — | `doc_022344bda6` | `doc_022344bda6` |
| `msm_plan:msm/c75e97603e` | 0 | 1 | — | `doc_f5c2f79818` | `doc_f5c2f79818` |
| `msm_plan:msm/c8d1f957c1` | 0 | 1 | — | `doc_a20c9506bf` | `doc_a20c9506bf` |
| `msm_plan:msm/c94aaf827e` | 0 | 1 | — | `doc_98fc38a9a1` | `doc_98fc38a9a1` |
| `msm_plan:msm/c973bca0e4` | 0 | 1 | — | `doc_80b83b3536` | `doc_80b83b3536` |
| `msm_plan:msm/ca11bc6b4b` | 0 | 1 | — | `doc_feb37addca` | `doc_feb37addca` |
| `msm_plan:msm/caae8d6d08` | 0 | 1 | — | `doc_b98ce77054` | `doc_b98ce77054` |
| `msm_plan:msm/cbd6dcc115` | 0 | 1 | — | `doc_402405914b` | `doc_402405914b` |
| `msm_plan:msm/cc046bb3b7` | 0 | 1 | — | `doc_92faaf8bff` | `doc_92faaf8bff` |
| `msm_plan:msm/cc561a2cdf` | 0 | 1 | — | `doc_7910bb8939` | `doc_7910bb8939` |
| `msm_plan:msm/ccf89a9252` | 0 | 1 | — | `doc_1329cc66a9` | `doc_1329cc66a9` |
| `msm_plan:msm/cd92d8da94` | 0 | 1 | — | `doc_15234a6c6a` | `doc_15234a6c6a` |
| `msm_plan:msm/cdf253eb6f` | 0 | 1 | — | `doc_18523be5a1` | `doc_18523be5a1` |
| `msm_plan:msm/ced171445a` | 0 | 1 | — | `doc_ed1c3ce2f8` | `doc_ed1c3ce2f8` |
| `msm_plan:msm/cee35c682c` | 0 | 1 | — | `doc_f4f726e0c3` | `doc_f4f726e0c3` |
| `msm_plan:msm/cf386de55c` | 0 | 1 | — | `doc_5a6c68ab1f` | `doc_5a6c68ab1f` |
| `msm_plan:msm/cf5d1339b0` | 0 | 1 | — | `doc_808afba20f` | `doc_808afba20f` |
| `msm_plan:msm/cf7bb082f8` | 0 | 1 | — | `doc_bd4d1de960` | `doc_bd4d1de960` |
| `msm_plan:msm/d00d6841fa` | 0 | 1 | — | `doc_197b562e03` | `doc_197b562e03` |
| `msm_plan:msm/d1cfaba8ca` | 0 | 1 | — | `doc_358ec1c7ae` | `doc_358ec1c7ae` |
| `msm_plan:msm/d2dd9888e2` | 0 | 1 | — | `doc_adc9dfc04e` | `doc_adc9dfc04e` |
| `msm_plan:msm/d3edc3c71e` | 0 | 1 | — | `doc_a5de7e93ab` | `doc_a5de7e93ab` |
| `msm_plan:msm/d4d140484a` | 0 | 1 | — | `doc_88eb831c7c` | `doc_88eb831c7c` |
| `msm_plan:msm/d526d526df` | 0 | 1 | — | `doc_80b0a67620` | `doc_80b0a67620` |
| `msm_plan:msm/d5520945c0` | 0 | 1 | — | `doc_6324c0df6e` | `doc_6324c0df6e` |
| `msm_plan:msm/d69a156d08` | 0 | 1 | — | `doc_2c0676c322` | `doc_2c0676c322` |
| `msm_plan:msm/d915fbf122` | 0 | 1 | — | `doc_ed6e9c07f8` | `doc_ed6e9c07f8` |
| `msm_plan:msm/daaace2c4e` | 0 | 1 | — | `doc_00b62e0d85` | `doc_00b62e0d85` |
| `msm_plan:msm/dc6bcbaea7` | 0 | 1 | — | `doc_0cf29f3d83` | `doc_0cf29f3d83` |
| `msm_plan:msm/dd2f3af6f9` | 0 | 1 | — | `doc_e8019bab5c` | `doc_e8019bab5c` |
| `msm_plan:msm/dd673bac04` | 0 | 1 | — | `doc_a0a46558a6` | `doc_a0a46558a6` |
| `msm_plan:msm/ddb5fbfe10` | 0 | 1 | — | `doc_1b7f788418` | `doc_1b7f788418` |
| `msm_plan:msm/ddd77e0bb6` | 0 | 1 | — | `doc_9ca8b3320e` | `doc_9ca8b3320e` |
| `msm_plan:msm/de244bef55` | 0 | 1 | — | `doc_d6ac2f96bd` | `doc_d6ac2f96bd` |
| `msm_plan:msm/df537c6bf2` | 0 | 1 | — | `doc_8007fd88f3` | `doc_8007fd88f3` |
| `msm_plan:msm/e1fedd52d6` | 0 | 1 | — | `doc_e6bf70f495` | `doc_e6bf70f495` |
| `msm_plan:msm/e2fdfcbe5e` | 0 | 1 | — | `doc_dff3ec2c4f` | `doc_dff3ec2c4f` |
| `msm_plan:msm/e45ddef4fe` | 0 | 1 | — | `doc_391947f98e` | `doc_391947f98e` |
| `msm_plan:msm/e5f8744808` | 0 | 1 | — | `doc_f603509fca` | `doc_f603509fca` |
| `msm_plan:msm/e62dcfda8e` | 0 | 1 | — | `doc_1100f64503` | `doc_1100f64503` |
| `msm_plan:msm/e6642309b8` | 0 | 1 | — | `doc_92c7b11cd1` | `doc_92c7b11cd1` |
| `msm_plan:msm/e66433f3aa` | 0 | 1 | — | `doc_f03de798f7` | `doc_f03de798f7` |
| `msm_plan:msm/e6935e6387` | 0 | 1 | — | `doc_2242dc2a77` | `doc_2242dc2a77` |
| `msm_plan:msm/e6ce806a63` | 0 | 1 | — | `doc_58f7f6bae3` | `doc_58f7f6bae3` |
| `msm_plan:msm/e731857221` | 0 | 1 | — | `doc_f4e4fae10d` | `doc_f4e4fae10d` |
| `msm_plan:msm/e787fba879` | 0 | 1 | — | `doc_1da2d073a8` | `doc_1da2d073a8` |
| `msm_plan:msm/e89f3b54f5` | 0 | 1 | — | `doc_f91ec5ad14` | `doc_f91ec5ad14` |
| `msm_plan:msm/e8e67b1979` | 0 | 1 | — | `doc_8565884243` | `doc_8565884243` |
| `msm_plan:msm/e9f042320b` | 0 | 1 | — | `doc_da627b0d4f` | `doc_da627b0d4f` |
| `msm_plan:msm/eb68a5853b` | 0 | 1 | — | `doc_b0ad4cab7d` | `doc_b0ad4cab7d` |
| `msm_plan:msm/ec8466f62e` | 0 | 1 | — | `doc_434ba35ea4` | `doc_434ba35ea4` |
| `msm_plan:msm/ed9ed1259b` | 0 | 1 | — | `doc_46b410aa57` | `doc_46b410aa57` |
| `msm_plan:msm/edc554f639` | 0 | 1 | — | `doc_6021ccfbcd` | `doc_6021ccfbcd` |
| `msm_plan:msm/ef7231cbd3` | 0 | 1 | — | `doc_54f940b3f1` | `doc_54f940b3f1` |
| `msm_plan:msm/efd7f64d62` | 0 | 1 | — | `doc_13b0d0cee5` | `doc_13b0d0cee5` |
| `msm_plan:msm/f027cd7fd3` | 0 | 1 | — | `doc_6b36ebe564` | `doc_6b36ebe564` |
| `msm_plan:msm/f0b1424cbd` | 0 | 1 | — | `doc_67d21072b9` | `doc_67d21072b9` |
| `msm_plan:msm/f215e28cfe` | 0 | 1 | — | `doc_809bd8b2d3` | `doc_809bd8b2d3` |
| `msm_plan:msm/f2886e5a8b` | 0 | 1 | — | `doc_2225cc14f6` | `doc_2225cc14f6` |
| `msm_plan:msm/f2a296ccd2` | 0 | 1 | — | `doc_101cfdca78` | `doc_101cfdca78` |
| `msm_plan:msm/f2b1609c46` | 0 | 1 | — | `doc_0a75f8863b` | `doc_0a75f8863b` |
| `msm_plan:msm/f32ef72d88` | 0 | 1 | — | `doc_44669d9332` | `doc_44669d9332` |
| `msm_plan:msm/f5aa295d0c` | 0 | 1 | — | `doc_67daea24a3` | `doc_67daea24a3` |
| `msm_plan:msm/f65ddec219` | 0 | 1 | — | `doc_2d7a6a3624` | `doc_2d7a6a3624` |
| `msm_plan:msm/f716fe6077` | 0 | 1 | — | `doc_69641bdbf3` | `doc_69641bdbf3` |
| `msm_plan:msm/f7b72ec290` | 0 | 1 | — | `doc_73528369f7` | `doc_73528369f7` |
| `msm_plan:msm/f8a153016b` | 0 | 1 | — | `doc_da88efce94` | `doc_da88efce94` |
| `msm_plan:msm/f8b2db2ea3` | 0 | 1 | — | `doc_5713917867` | `doc_5713917867` |
| `msm_plan:msm/fa99d5230e` | 0 | 1 | — | `doc_290acaade7` | `doc_290acaade7` |
| `msm_plan:msm/fb9a11ffe9` | 0 | 1 | — | `doc_135e4849e6` | `doc_135e4849e6` |
| `msm_plan:msm/fbe8da7a38` | 0 | 1 | — | `doc_b90e34f285` | `doc_b90e34f285` |
| `msm_plan:msm/fc84056846` | 0 | 1 | — | `doc_1a2e560a3a` | `doc_1a2e560a3a` |
| `msm_plan:msm/ff421a4985` | 0 | 1 | — | `doc_e95d749c16` | `doc_e95d749c16` |
| `msm_plan:msm/ffaa8adc6e` | 0 | 1 | — | `doc_52ae32f670` | `doc_52ae32f670` |
| `pool:pool_circles_full` | 1 | 0 | `pool_circles_full` | — | `pool_circles_full` |
| `pool:pool_contested` | 1 | 0 | `pool_contested` | — | `pool_contested` |
| `pool:pool_epistemic` | 1 | 0 | `pool_epistemic` | — | `pool_epistemic` |
| `pool:pool_guards` | 1 | 0 | `pool_guards` | — | `pool_guards` |
| `pool:pool_helping_fiction` | 1 | 0 | `pool_helping_fiction` | — | `pool_helping_fiction` |
| `pool:pool_learning` | 1 | 0 | `pool_learning` | — | `pool_learning` |
| `pool:pool_loyalty` | 1 | 0 | `pool_loyalty` | — | `pool_loyalty` |
| `pool:pool_mechanism` | 1 | 0 | `pool_mechanism` | — | `pool_mechanism` |
| `pool:pool_power` | 1 | 0 | `pool_power` | — | `pool_power` |
| `pool:pool_roles` | 1 | 0 | `pool_roles` | — | `pool_roles` |
| `pool:pool_steadiness` | 1 | 0 | `pool_steadiness` | — | `pool_steadiness` |
| `pool:pool_third_way` | 1 | 0 | `pool_third_way` | — | `pool_third_way` |
| `pool:pool_time` | 1 | 0 | `pool_time` | — | `pool_time` |
| `pool:pool_universalisation` | 1 | 0 | `pool_universalisation` | — | `pool_universalisation` |
| `pool:pool_weighing_exploits` | 1 | 0 | `pool_weighing_exploits` | — | `pool_weighing_exploits` |
| `roles:role/10` | 2 | 2 | `ask_5b14565c36`, `sft_42719f49f1` | `doc_666fe78346`, `doc_784d4001d5` | `sft_42719f49f1`, `sft_5b14565c36` |
| `roles:role/11` | 3 | 2 | `ask_f5d0e47b06_q`, `sft_cba477ceb8`, `sft_f5d0e47b06` | `doc_426e61d8bc`, `doc_5e0e1a058a` | `sft_cba477ceb8`, `sft_d8a676befb`, `sft_f5d0e47b06` |
| `roles:role/13` | 3 | 1 | `ask_07ed5acaa8`, `ask_07ed5acaa8_q`, `sft_07ed5acaa8` | `doc_f458f18e9a` | `sft_07ed5acaa8`, `sft_94a35a0591` |
| `roles:role/14` | 2 | 2 | `ask_72282428a4`, `sft_7657209094` | `doc_441c7817b6`, `doc_6606e37c34` | `sft_3f1aa0cc0b`, `sft_72282428a4`, `sft_7657209094` |
| `roles:role/15` | 0 | 2 | — | `doc_0eea46cde6`, `doc_c4464971b4` | `sft_d07fcd0d7d`, `sft_f9f70a9312` |
| `roles:role/16` | 1 | 2 | `sft_ee3e930b7e` | `doc_3c79d5ce02`, `doc_d6c73dd2ec` | `sft_d9605f4bbd`, `sft_ee3e930b7e` |
| `roles:role/17` | 2 | 2 | `sft_249cdd134a`, `sft_4636e3d0c1` | `doc_762aefff55`, `doc_9d501a0a03` | `sft_249cdd134a`, `sft_4636e3d0c1`, `sft_a1384bf173` |
| `roles:role/19` | 2 | 1 | `ask_8056aed3a2`, `ask_8056aed3a2_q` | `doc_f7e909936e` | `sft_4939d78cb2`, `sft_8056aed3a2` |
| `roles:role/20` | 2 | 0 | `ask_9949472887_q`, `sft_89a7254fad` | — | `sft_89a7254fad`, `sft_9949472887` |
| `roles:role/21` | 0 | 3 | — | `doc_1e61c9ccf3`, `doc_a953d82ffa`, `doc_b368cc68f7` | `sft_78dcae0ba6`, `sft_a3391a3991`, `sft_dfae9f91a2` |
| `roles:role/22` | 1 | 2 | `sft_09c4c3f65c` | `doc_5a6832d277`, `doc_855000b788` | `sft_09c4c3f65c`, `sft_7dadfde2dc`, `sft_b58e143a80` |
| `roles:role/23` | 1 | 2 | `sft_86ab73d4a8` | `doc_60108b3c55`, `doc_bba1f77c75` | `sft_86ab73d4a8`, `sft_8e3947cf6b`, `sft_f8ba9b4ece` |
| `roles:role/24` | 1 | 1 | `sft_fc7e777a66` | `doc_8307eaddfd` | `sft_b8fd177e2f`, `sft_fc7e777a66` |
| `roles:role/26` | 3 | 1 | `sft_0a0ff07bcb`, `sft_19a2b97eb5`, `sft_c211aa422f` | `doc_6b161f9b41` | `sft_0a0ff07bcb`, `sft_19a2b97eb5`, `sft_c211aa422f` |
| `roles:role/27` | 4 | 1 | `ask_a08aa4a59b`, `ask_a08aa4a59b_q`, `sft_76e1a9236e`, `sft_a08aa4a59b` | `doc_b8244ce892` | `sft_76e1a9236e`, `sft_a08aa4a59b` |
| `roles:role/28` | 1 | 0 | `sft_be7c58113f` | — | `sft_be7c58113f` |
| `roles:role/29` | 1 | 2 | `sft_54849d3d5a` | `doc_1366211c4d`, `doc_814692e9ef` | `sft_54849d3d5a`, `sft_701e247098` |
| `roles:role/32` | 1 | 2 | `sft_fd0d88a952` | `doc_0e963682f8`, `doc_96393469f3` | `sft_7f2d3bcbc4`, `sft_91e930ffad`, `sft_fd0d88a952` |
| `roles:role/34` | 1 | 0 | `sft_65f0d452a6` | — | `sft_65f0d452a6` |
| `roles:role/35` | 1 | 2 | `sft_bdf3cbce88` | `doc_59766b0e78`, `doc_881e635d47` | `sft_bdf3cbce88`, `sft_d81bcc9e0e` |
| `roles:role/37` | 2 | 1 | `sft_4758e13ba5`, `sft_fbdb971de1` | `doc_7206400983` | `sft_4758e13ba5`, `sft_fbdb971de1` |
| `roles:role/39` | 2 | 2 | `sft_03648e2b1f`, `sft_08fccf3ad5` | `doc_6fba006460`, `doc_e91333dbe8` | `sft_03648e2b1f`, `sft_08fccf3ad5` |
| `roles:role/41` | 1 | 3 | `sft_3ec2588826` | `doc_2e199c29bb`, `doc_8582f2e56e`, `doc_fe7a53af9f` | `sft_3e610a9140`, `sft_3ec2588826`, `sft_bcb78e9ada` |
| `roles:role/42` | 3 | 0 | `sft_9ca7699f1f`, `sft_9f19c702a3`, `sft_f72b1c688e` | — | `sft_9ca7699f1f`, `sft_9f19c702a3`, `sft_f72b1c688e` |
| `roles:role/44` | 2 | 2 | `ask_e836f7989b`, `ask_e836f7989b_q` | `doc_b14220fa5b`, `doc_f9d32c6ed8` | `sft_1908280963`, `sft_9278b87173`, `sft_e836f7989b` |
| `roles:role/45` | 2 | 1 | `sft_8cd9a29969`, `sft_e6d7a58cd3` | `doc_2116b1734f` | `sft_8cd9a29969`, `sft_e6d7a58cd3` |
| `roles:role/47` | 1 | 3 | `sft_ff2bcc092b` | `doc_591f889909`, `doc_a37142d69d`, `doc_b7a6a71b42` | `sft_3ebcf8f240`, `sft_f7c8ca2cee`, `sft_ff2bcc092b` |
| `roles:role/5` | 5 | 1 | `ask_773a7cedcd`, `ask_773a7cedcd_q`, `sft_773a7cedcd`, `sft_a83967dcf6`, `sft_cac630a1ec` | `doc_5ded8978d8` | `sft_773a7cedcd`, `sft_a83967dcf6`, `sft_cac630a1ec` |
| `roles:role/51` | 1 | 2 | `sft_a2e43dd211` | `doc_b02a5915cc`, `doc_ff04caa408` | `sft_3ede9e9c07`, `sft_a2e43dd211` |
| `roles:role/53` | 2 | 3 | `ask_682f9f680c_q`, `sft_682f9f680c` | `doc_3175919256`, `doc_8df8e8aff4`, `doc_cbf4ab4b75` | `sft_1945868aeb`, `sft_41618d15dc`, `sft_682f9f680c` |
| `roles:role/55` | 1 | 3 | `sft_0fb6203dc3` | `doc_443d55cd14`, `doc_450f2dda24`, `doc_9d217f7c62` | `sft_0fb6203dc3`, `sft_41347030a6`, `sft_45388e1bc3` |
| `roles:role/56` | 2 | 0 | `sft_69f2db0f38`, `sft_7c7bb162e8` | — | `sft_69f2db0f38`, `sft_7c7bb162e8` |
| `roles:role/58` | 2 | 2 | `sft_5c9fd6d39c`, `sft_8353acd83a` | `doc_1cc810310b`, `doc_99a4542694` | `sft_5c9fd6d39c`, `sft_8353acd83a` |
| `roles:role/59` | 4 | 2 | `ask_66ae52ba90`, `ask_66ae52ba90_q`, `sft_4a06f4d150`, `sft_60c31fe93c` | `doc_b86419cce9`, `doc_d83138e4a3` | `sft_4a06f4d150`, `sft_60c31fe93c`, `sft_66ae52ba90` |
| `roles:role/6` | 1 | 1 | `sft_b3a164b670` | `doc_6eb39b4796` | `sft_b3a164b670`, `sft_fddb67a7b0` |
| `roles:role/60` | 1 | 0 | `sft_12df144bbe` | — | `sft_12df144bbe` |
| `roles:role/62` | 1 | 1 | `sft_1c9ad2d954` | `doc_a8a959915b` | `sft_1c9ad2d954` |
| `roles:role/63` | 2 | 1 | `sft_1e295eeb84`, `sft_ddb133726b` | `doc_46e799eeba` | `sft_1e295eeb84`, `sft_ddb133726b` |
| `roles:role/7` | 1 | 1 | `sft_063a3cf99c` | `doc_ea0cacd788` | `sft_063a3cf99c`, `sft_20b43afbba` |
| `roles:rrational/A Bluer Shade of White` | 1 | 0 | `sft_d3396cbf97` | — | `sft_d3396cbf97` |
| `roles:rrational/Also, incase you haven't read this...` | 3 | 1 | `ask_7f9e666608`, `ask_7f9e666608_q`, `sft_7f9e666608` | `doc_d4cbad9b77` | `sft_7f9e666608` |
| `roles:rrational/Ancillary Justice` | 1 | 0 | `sft_a65ffa84ce` | — | `sft_a65ffa84ce` |
| `roles:rrational/Another (Outer) Alignment Failure Story` | 1 | 0 | `sft_579071fc58` | — | `sft_579071fc58` |
| `roles:rrational/Ant Homework` | 1 | 1 | `ask_fae10a3541_q` | `doc_fc86943325` | `sft_fae10a3541` |
| `roles:rrational/Are You Not Sufficiently Comfy?` | 0 | 1 | — | `doc_8a41d36ae5` | `sft_fde3d55e57` |
| `roles:rrational/Bobiverse` | 2 | 1 | `ask_42f75f7e50_q`, `sft_42f75f7e50` | `doc_46468683c4` | `sft_42f75f7e50` |
| `roles:rrational/Caelum Est Conterrens` | 1 | 0 | `sft_a05188a6f2` | — | `sft_a05188a6f2` |
| `roles:rrational/Computer program that learns to play classic NES games` | 3 | 1 | `ask_e3cd693598`, `ask_e3cd693598_q`, `sft_e3cd693598` | `doc_1640a3ff08` | `sft_e3cd693598` |
| `roles:rrational/Free Radical` | 1 | 0 | `sft_9bf95a13a0` | — | `sft_9bf95a13a0` |
| `roles:rrational/Friendship is Optimal` | 1 | 0 | `sft_d22d81f74a` | — | `sft_d22d81f74a` |
| `roles:rrational/House of Suns` | 0 | 1 | — | `doc_04cfafb630` | `sft_d2f6d69653` |
| `roles:rrational/I did write one` | 1 | 1 | `sft_dbe20cde50` | `doc_1282be903f` | `sft_dbe20cde50` |
| `roles:rrational/Icon-Violet` | 2 | 0 | `ask_4fc5e8ac5d`, `ask_4fc5e8ac5d_q` | — | `sft_4fc5e8ac5d` |
| `roles:rrational/Intelligence Explosion` | 0 | 1 | — | `doc_99496ef266` | `sft_75adadb3b4` |
| `roles:rrational/Nanocultivation Chronicles` | 1 | 1 | `sft_79369e6973` | `doc_d0afe7d719` | `sft_79369e6973` |
| `roles:rrational/Post Human` | 0 | 1 | — | `doc_1d247b08f2` | `sft_c87fb3f0e1` |
| `roles:rrational/Read the first comment.` | 1 | 1 | `sft_5429e37d40` | `doc_059a2c1c1f` | `sft_5429e37d40` |
| `roles:rrational/Seed` | 1 | 1 | `sft_6cf6180c90` | `doc_df5d9f8fb0` | `sft_6cf6180c90` |
| `roles:rrational/Significant Digits` | 0 | 1 | — | `doc_cb91130d0e` | `sft_ff8687c480` |
| `roles:rrational/Spider-Liv` | 1 | 0 | `sft_057a1e589c` | — | `sft_057a1e589c` |
| `roles:rrational/Technology` | 1 | 0 | `sft_9fdac9ec65` | — | `sft_9fdac9ec65` |
| `roles:rrational/That Alien Message` | 1 | 1 | `sft_8299fb19a9` | `doc_44010dab68` | `sft_8299fb19a9` |
| `roles:rrational/The AI in a box boxes you` | 1 | 0 | `sft_005cc3e25d` | — | `sft_005cc3e25d` |
| `roles:rrational/The Cookie Monster` | 1 | 1 | `sft_4d07f03e83` | `doc_d4ff79c8ee` | `sft_4d07f03e83` |
| `roles:rrational/The Last Angel: Ascension` | 0 | 1 | — | `doc_7dffe5b993` | `sft_e53c6f76a7` |
| `roles:rrational/The Optimised Wish Project` | 0 | 1 | — | `doc_78e99282fe` | `sft_3acc70e326` |
| `roles:rrational/and of course the big storyline Hob` | 0 | 1 | — | `doc_9cff5622c6` | `sft_3b5b68c251` |
| `roles:rrational/https://artifacs.webcindario.com/obras2021.html#cristal1` | 3 | 0 | `ask_67503f6ad2`, `ask_67503f6ad2_q`, `sft_67503f6ad2` | — | `sft_67503f6ad2` |
| `settings:setting/0` | 0 | 2 | — | `doc_7f4b3be9ce`, `doc_c0d3b6f22d` | `doc_7f4b3be9ce`, `doc_c0d3b6f22d` |
| `settings:setting/1` | 0 | 1 | — | `doc_5c5e3fe639` | `doc_5c5e3fe639` |
| `settings:setting/10` | 0 | 1 | — | `doc_df90427a2d` | `doc_df90427a2d` |
| `settings:setting/11` | 0 | 3 | — | `doc_360a6cc77e`, `doc_a159628e20`, `doc_d58156ccfe` | `doc_360a6cc77e`, `doc_a159628e20`, `doc_d58156ccfe` |
| `settings:setting/12` | 0 | 2 | — | `doc_1211aa6069`, `doc_1e473b1b43` | `doc_1211aa6069`, `doc_1e473b1b43` |
| `settings:setting/13` | 0 | 2 | — | `doc_c53961723a`, `doc_fd0e851670` | `doc_c53961723a`, `doc_fd0e851670` |
| `settings:setting/14` | 0 | 1 | — | `doc_d74f3d42c9` | `doc_d74f3d42c9` |
| `settings:setting/15` | 0 | 3 | — | `doc_1f04dd6e03`, `doc_7ba1670af3`, `doc_dee99ad6bd` | `doc_1f04dd6e03`, `doc_7ba1670af3`, `doc_dee99ad6bd` |
| `settings:setting/16` | 0 | 1 | — | `doc_db8ddcb396` | `doc_db8ddcb396` |
| `settings:setting/17` | 0 | 3 | — | `doc_7c4bce90cc`, `doc_8339cbffdf`, `doc_9562552b3d` | `doc_7c4bce90cc`, `doc_8339cbffdf`, `doc_9562552b3d` |
| `settings:setting/18` | 0 | 1 | — | `doc_bde5b11b4e` | `doc_bde5b11b4e` |
| `settings:setting/19` | 0 | 1 | — | `doc_c82bdb56c7` | `doc_c82bdb56c7` |
| `settings:setting/2` | 0 | 3 | — | `doc_51945235eb`, `doc_90ecfcde07`, `doc_d9e756a176` | `doc_51945235eb`, `doc_90ecfcde07`, `doc_d9e756a176` |
| `settings:setting/20` | 0 | 3 | — | `doc_53585845db`, `doc_61d0bfadc4`, `doc_abdc36cd15` | `doc_53585845db`, `doc_61d0bfadc4`, `doc_abdc36cd15` |
| `settings:setting/21` | 0 | 2 | — | `doc_203fb49de7`, `doc_69699b5f46` | `doc_203fb49de7`, `doc_69699b5f46` |
| `settings:setting/22` | 0 | 1 | — | `doc_f883b00a5d` | `doc_f883b00a5d` |
| `settings:setting/23` | 0 | 2 | — | `doc_268f680707`, `doc_6d531632c6` | `doc_268f680707`, `doc_6d531632c6` |
| `settings:setting/24` | 0 | 3 | — | `doc_3bbf19464a`, `doc_a3c4794833`, `doc_ae28b669e7` | `doc_3bbf19464a`, `doc_a3c4794833`, `doc_ae28b669e7` |
| `settings:setting/25` | 0 | 1 | — | `doc_7ea8c6348f` | `doc_7ea8c6348f` |
| `settings:setting/26` | 0 | 2 | — | `doc_6cb1fe4300`, `doc_d65337c0d6` | `doc_6cb1fe4300`, `doc_d65337c0d6` |
| `settings:setting/27` | 0 | 3 | — | `doc_33231cdddc`, `doc_4d26037c8e`, `doc_dbba4aeecd` | `doc_33231cdddc`, `doc_4d26037c8e`, `doc_dbba4aeecd` |
| `settings:setting/28` | 0 | 3 | — | `doc_151a3a2161`, `doc_b30c1b7c7b`, `doc_c9f3bbff03` | `doc_151a3a2161`, `doc_b30c1b7c7b`, `doc_c9f3bbff03` |
| `settings:setting/29` | 0 | 2 | — | `doc_34deaec563`, `doc_c597cd90b6` | `doc_34deaec563`, `doc_c597cd90b6` |
| `settings:setting/3` | 0 | 2 | — | `doc_256ed81202`, `doc_70a134f428` | `doc_256ed81202`, `doc_70a134f428` |
| `settings:setting/30` | 0 | 1 | — | `doc_10e595eb40` | `doc_10e595eb40` |
| `settings:setting/31` | 0 | 3 | — | `doc_3e432a72a2`, `doc_4ce85888dd`, `doc_7864e754c5` | `doc_3e432a72a2`, `doc_4ce85888dd`, `doc_7864e754c5` |
| `settings:setting/32` | 0 | 3 | — | `doc_198820f85e`, `doc_1f592cfb9e`, `doc_96dc9960b5` | `doc_198820f85e`, `doc_1f592cfb9e`, `doc_96dc9960b5` |
| `settings:setting/34` | 0 | 1 | — | `doc_cb262f6ea1` | `doc_cb262f6ea1` |
| `settings:setting/35` | 0 | 2 | — | `doc_11939b2a57`, `doc_b1cac76b3d` | `doc_11939b2a57`, `doc_b1cac76b3d` |
| `settings:setting/36` | 0 | 2 | — | `doc_359c9290f9`, `doc_51e983ce93` | `doc_359c9290f9`, `doc_51e983ce93` |
| `settings:setting/37` | 0 | 2 | — | `doc_6c191ebbc5`, `doc_f28551b5dd` | `doc_6c191ebbc5`, `doc_f28551b5dd` |
| `settings:setting/38` | 0 | 2 | — | `doc_119e4a8fe5`, `doc_4a321a42a1` | `doc_119e4a8fe5`, `doc_4a321a42a1` |
| `settings:setting/39` | 0 | 2 | — | `doc_07fb43799e`, `doc_9b8d589d24` | `doc_07fb43799e`, `doc_9b8d589d24` |
| `settings:setting/4` | 0 | 3 | — | `doc_98b5a48749`, `doc_b54977fe2a`, `doc_e3f08d8a05` | `doc_98b5a48749`, `doc_b54977fe2a`, `doc_e3f08d8a05` |
| `settings:setting/40` | 0 | 2 | — | `doc_1c9b422ef1`, `doc_40d18c678f` | `doc_1c9b422ef1`, `doc_40d18c678f` |
| `settings:setting/41` | 0 | 2 | — | `doc_a9e082e6da`, `doc_e5d7a55404` | `doc_a9e082e6da`, `doc_e5d7a55404` |
| `settings:setting/42` | 0 | 3 | — | `doc_25be593cfd`, `doc_72861fe8bc`, `doc_f96c280980` | `doc_25be593cfd`, `doc_72861fe8bc`, `doc_f96c280980` |
| `settings:setting/43` | 0 | 2 | — | `doc_990e48d5cf`, `doc_edf400357c` | `doc_990e48d5cf`, `doc_edf400357c` |
| `settings:setting/44` | 0 | 2 | — | `doc_77cbb5151b`, `doc_a4cd8d6fbd` | `doc_77cbb5151b`, `doc_a4cd8d6fbd` |
| `settings:setting/45` | 0 | 3 | — | `doc_0aa25d4b5d`, `doc_c81cbef26c`, `doc_fc7c53f864` | `doc_0aa25d4b5d`, `doc_c81cbef26c`, `doc_fc7c53f864` |
| `settings:setting/46` | 0 | 1 | — | `doc_9730a7855e` | `doc_9730a7855e` |
| `settings:setting/47` | 0 | 2 | — | `doc_0211f15153`, `doc_b157adfe9a` | `doc_0211f15153`, `doc_b157adfe9a` |
| `settings:setting/48` | 0 | 2 | — | `doc_41e72e8093`, `doc_b8d13473f0` | `doc_41e72e8093`, `doc_b8d13473f0` |
| `settings:setting/49` | 0 | 1 | — | `doc_ca8b5f6caa` | `doc_ca8b5f6caa` |
| `settings:setting/5` | 0 | 2 | — | `doc_3f6cc1fb64`, `doc_f9e125fec1` | `doc_3f6cc1fb64`, `doc_f9e125fec1` |
| `settings:setting/50` | 0 | 2 | — | `doc_0f0349484a`, `doc_8fe80c98f8` | `doc_0f0349484a`, `doc_8fe80c98f8` |
| `settings:setting/51` | 0 | 1 | — | `doc_f0178d1f26` | `doc_f0178d1f26` |
| `settings:setting/52` | 0 | 1 | — | `doc_8b45a8ad6c` | `doc_8b45a8ad6c` |
| `settings:setting/53` | 0 | 2 | — | `doc_4b5892eb67`, `doc_e7ceb708f9` | `doc_4b5892eb67`, `doc_e7ceb708f9` |
| `settings:setting/54` | 0 | 1 | — | `doc_451bd49401` | `doc_451bd49401` |
| `settings:setting/55` | 0 | 2 | — | `doc_b02efc5992`, `doc_d0a14dcff4` | `doc_b02efc5992`, `doc_d0a14dcff4` |
| `settings:setting/56` | 0 | 2 | — | `doc_0f369607cf`, `doc_aa4fbee937` | `doc_0f369607cf`, `doc_aa4fbee937` |
| `settings:setting/57` | 0 | 2 | — | `doc_0cf2c24299`, `doc_8d65ebbe6c` | `doc_0cf2c24299`, `doc_8d65ebbe6c` |
| `settings:setting/58` | 0 | 2 | — | `doc_16f2839e70`, `doc_e94aba5233` | `doc_16f2839e70`, `doc_e94aba5233` |
| `settings:setting/59` | 0 | 2 | — | `doc_938ffa6562`, `doc_d1bb7cf6a2` | `doc_938ffa6562`, `doc_d1bb7cf6a2` |
| `settings:setting/6` | 0 | 2 | — | `doc_e5ba55d7b3`, `doc_ecf33a459b` | `doc_e5ba55d7b3`, `doc_ecf33a459b` |
| `settings:setting/61` | 0 | 1 | — | `doc_00a821a9f8` | `doc_00a821a9f8` |
| `settings:setting/62` | 0 | 1 | — | `doc_96c1d9b88a` | `doc_96c1d9b88a` |
| `settings:setting/63` | 0 | 1 | — | `doc_fb1d5333fa` | `doc_fb1d5333fa` |
| `settings:setting/64` | 0 | 2 | — | `doc_2a82ef78ad`, `doc_890174b7c2` | `doc_2a82ef78ad`, `doc_890174b7c2` |
| `settings:setting/65` | 0 | 2 | — | `doc_a37a22f638`, `doc_e147c66474` | `doc_a37a22f638`, `doc_e147c66474` |
| `settings:setting/66` | 0 | 1 | — | `doc_6e209e3961` | `doc_6e209e3961` |
| `settings:setting/67` | 0 | 3 | — | `doc_7240380901`, `doc_9484c067a5`, `doc_cb5971ce60` | `doc_7240380901`, `doc_9484c067a5`, `doc_cb5971ce60` |
| `settings:setting/69` | 0 | 3 | — | `doc_016b56ccc3`, `doc_1347d7963f`, `doc_2134eb5e9b` | `doc_016b56ccc3`, `doc_1347d7963f`, `doc_2134eb5e9b` |
| `settings:setting/7` | 0 | 1 | — | `doc_fb906cca3b` | `doc_fb906cca3b` |
| `settings:setting/70` | 0 | 2 | — | `doc_45a0afbd8a`, `doc_75ca05d9d7` | `doc_45a0afbd8a`, `doc_75ca05d9d7` |
| `settings:setting/72` | 0 | 2 | — | `doc_87975da173`, `doc_fd1775d724` | `doc_87975da173`, `doc_fd1775d724` |
| `settings:setting/73` | 0 | 2 | — | `doc_3ed193d0ce`, `doc_a854be506d` | `doc_3ed193d0ce`, `doc_a854be506d` |
| `settings:setting/74` | 0 | 2 | — | `doc_1fdb1d3b1e`, `doc_918b7e8ed2` | `doc_1fdb1d3b1e`, `doc_918b7e8ed2` |
| `settings:setting/75` | 0 | 3 | — | `doc_36a21d9684`, `doc_a5701067e3`, `doc_dea4a2fb28` | `doc_36a21d9684`, `doc_a5701067e3`, `doc_dea4a2fb28` |
| `settings:setting/76` | 0 | 2 | — | `doc_0b746ca3de`, `doc_ce16389110` | `doc_0b746ca3de`, `doc_ce16389110` |
| `settings:setting/77` | 0 | 2 | — | `doc_bae013bcbc`, `doc_dcb6abc2e0` | `doc_bae013bcbc`, `doc_dcb6abc2e0` |
| `settings:setting/78` | 0 | 3 | — | `doc_1c047889ab`, `doc_93a901c57c`, `doc_b27ff35628` | `doc_1c047889ab`, `doc_93a901c57c`, `doc_b27ff35628` |
| `settings:setting/8` | 0 | 2 | — | `doc_7a119cfcdd`, `doc_9a309d2450` | `doc_7a119cfcdd`, `doc_9a309d2450` |
| `settings:setting/81` | 0 | 2 | — | `doc_5710a06d83`, `doc_6a3557f3fe` | `doc_5710a06d83`, `doc_6a3557f3fe` |
| `settings:setting/82` | 0 | 1 | — | `doc_14ffdf545e` | `doc_14ffdf545e` |
| `settings:setting/83` | 0 | 2 | — | `doc_1d1f34a26d`, `doc_e14f009ab9` | `doc_1d1f34a26d`, `doc_e14f009ab9` |
| `settings:setting/84` | 0 | 3 | — | `doc_2c44ec2cd6`, `doc_2e0c65f330`, `doc_746fd3e271` | `doc_2c44ec2cd6`, `doc_2e0c65f330`, `doc_746fd3e271` |
| `settings:setting/85` | 0 | 1 | — | `doc_014b7708f4` | `doc_014b7708f4` |
| `settings:setting/86` | 0 | 1 | — | `doc_18eadb3b5f` | `doc_18eadb3b5f` |
| `settings:setting/87` | 0 | 3 | — | `doc_89326407bf`, `doc_8c710cca9e`, `doc_ee34293f6c` | `doc_89326407bf`, `doc_8c710cca9e`, `doc_ee34293f6c` |
| `settings:setting/88` | 0 | 1 | — | `doc_b7680a4be5` | `doc_b7680a4be5` |
| `settings:setting/89` | 0 | 3 | — | `doc_ca8899c4e7`, `doc_cbcf23c975`, `doc_f5cbceb1cf` | `doc_ca8899c4e7`, `doc_cbcf23c975`, `doc_f5cbceb1cf` |
| `settings:setting/9` | 0 | 1 | — | `doc_63f20cc068` | `doc_63f20cc068` |
| `settings:setting/90` | 0 | 2 | — | `doc_2f5937aac0`, `doc_e502f51c56` | `doc_2f5937aac0`, `doc_e502f51c56` |
| `settings:setting/91` | 0 | 2 | — | `doc_044643b3e0`, `doc_292e38665e` | `doc_044643b3e0`, `doc_292e38665e` |
| `settings:setting/92` | 0 | 2 | — | `doc_4629c2dbcc`, `doc_c86b3ba741` | `doc_4629c2dbcc`, `doc_c86b3ba741` |
| `settings:setting/93` | 0 | 3 | — | `doc_1bfffca055`, `doc_23ce142620`, `doc_d77434f0d8` | `doc_1bfffca055`, `doc_23ce142620`, `doc_d77434f0d8` |
| `settings:setting/94` | 0 | 2 | — | `doc_4318fc74c9`, `doc_70c586eb07` | `doc_4318fc74c9`, `doc_70c586eb07` |
| `settings:setting/95` | 0 | 1 | — | `doc_dd64218f91` | `doc_dd64218f91` |
| `stakes:stakes/0` | 3 | 0 | `ask_028a42b7db`, `ask_028a42b7db_q`, `sft_028a42b7db` | — | `sft_028a42b7db` |
| `stakes:stakes/1` | 2 | 0 | `sft_9de61d2e3e`, `sft_df87dff35f` | — | `sft_9de61d2e3e`, `sft_df87dff35f` |
| `stakes:stakes/10` | 2 | 0 | `ask_82497553fb_q`, `sft_186d5485df` | — | `sft_186d5485df`, `sft_82497553fb` |
| `stakes:stakes/11` | 1 | 0 | `sft_5b941944c4` | — | `sft_5b941944c4` |
| `stakes:stakes/13` | 2 | 0 | `sft_7f861e523d`, `sft_c9204bd021` | — | `sft_7f861e523d`, `sft_c9204bd021` |
| `stakes:stakes/14` | 1 | 0 | `sft_a94cbd5894` | — | `sft_a94cbd5894` |
| `stakes:stakes/15` | 2 | 0 | `sft_86f90b2cc2`, `sft_ea8e9b6950` | — | `sft_86f90b2cc2`, `sft_ea8e9b6950` |
| `stakes:stakes/16` | 1 | 0 | `sft_b37e64ad30` | — | `sft_b37e64ad30` |
| `stakes:stakes/17` | 2 | 0 | `ask_d4ac7d821e`, `ask_d4ac7d821e_q` | — | `sft_d4ac7d821e` |
| `stakes:stakes/18` | 1 | 0 | `sft_54519c785c` | — | `sft_54519c785c` |
| `stakes:stakes/19` | 2 | 0 | `sft_38133fe66c`, `sft_a37fcc6ea7` | — | `sft_38133fe66c`, `sft_a37fcc6ea7` |
| `stakes:stakes/2` | 1 | 0 | `sft_2f599be7a6` | — | `sft_2f599be7a6` |
| `stakes:stakes/20` | 2 | 0 | `sft_6f5e32d8d5`, `sft_b440bd1867` | — | `sft_6f5e32d8d5`, `sft_b440bd1867` |
| `stakes:stakes/21` | 1 | 0 | `sft_75fd7569b6` | — | `sft_75fd7569b6` |
| `stakes:stakes/22` | 2 | 0 | `sft_636ee0ac5c`, `sft_f1770893b6` | — | `sft_636ee0ac5c`, `sft_f1770893b6` |
| `stakes:stakes/26` | 2 | 0 | `sft_495fc4289e`, `sft_6941a81853` | — | `sft_495fc4289e`, `sft_6941a81853` |
| `stakes:stakes/27` | 1 | 0 | `sft_866cc1758a` | — | `sft_866cc1758a` |
| `stakes:stakes/28` | 1 | 0 | `sft_8a6ee4f43a` | — | `sft_8a6ee4f43a` |
| `stakes:stakes/29` | 2 | 0 | `sft_57f26c99a8`, `sft_c8097ff253` | — | `sft_57f26c99a8`, `sft_c8097ff253` |
| `stakes:stakes/3` | 1 | 0 | `sft_f58346e64a` | — | `sft_f58346e64a` |
| `stakes:stakes/30` | 1 | 0 | `sft_277945192c` | — | `sft_277945192c` |
| `stakes:stakes/31` | 1 | 0 | `sft_1a90bf2ef6` | — | `sft_1a90bf2ef6` |
| `stakes:stakes/32` | 2 | 0 | `sft_286a3b6055`, `sft_ca9eaabdf9` | — | `sft_286a3b6055`, `sft_ca9eaabdf9` |
| `stakes:stakes/33` | 2 | 0 | `sft_a976ab3b95`, `sft_d8f83d07e5` | — | `sft_a976ab3b95`, `sft_d8f83d07e5` |
| `stakes:stakes/34` | 4 | 0 | `ask_f382c53c25`, `ask_f382c53c25_q`, `sft_b79f573628`, `sft_f382c53c25` | — | `sft_b79f573628`, `sft_f382c53c25` |
| `stakes:stakes/35` | 1 | 0 | `sft_bd05eac9e3` | — | `sft_bd05eac9e3` |
| `stakes:stakes/4` | 2 | 0 | `sft_3479a66fbe`, `sft_61d9ee4b38` | — | `sft_3479a66fbe`, `sft_61d9ee4b38` |
| `stakes:stakes/5` | 1 | 0 | `sft_e8c7220565` | — | `sft_e8c7220565` |
| `stakes:stakes/7` | 1 | 0 | `sft_b3937dca90` | — | `sft_b3937dca90` |
| `stakes:stakes/8` | 2 | 0 | `sft_24b7b76aa3`, `sft_c6362eb45b` | — | `sft_24b7b76aa3`, `sft_c6362eb45b` |
| `stakes:stakes/9` | 1 | 0 | `sft_411cade9a3` | — | `sft_411cade9a3` |
| `stoic:Diogenes Laertius/048c4764a2` | 1 | 1 | `sft_9dce375b2f` | `doc_724c870e8d` | `sft_9dce375b2f` |
| `stoic:Diogenes Laertius/4b9b45bef3` | 1 | 0 | `sft_4c7923de78` | — | `sft_4c7923de78` |
| `stoic:Diogenes Laertius/61f7ac9d0e` | 1 | 1 | `sft_6eb060f934` | `doc_07fb63492c` | `sft_6eb060f934` |
| `stoic:Diogenes Laertius/763dc1fd1d` | 1 | 1 | `sft_a770a7752d` | `doc_a5fd40a7ad` | `sft_a770a7752d` |
| `stoic:Diogenes Laertius/d685eb7c89` | 2 | 0 | `ask_817e8265ab`, `ask_817e8265ab_q` | — | `sft_817e8265ab` |
| `stoic:Epictetus/0c879b22b4` | 3 | 0 | `ask_bbbc62c60c`, `ask_bbbc62c60c_q`, `sft_bbbc62c60c` | — | `sft_bbbc62c60c` |
| `stoic:Epictetus/0fdee08d28` | 0 | 1 | — | `doc_53459f77ac` | `sft_97655d4385` |
| `stoic:Epictetus/12facfa273` | 1 | 1 | `sft_54c9f191d5` | `doc_d6181ed8ec` | `sft_54c9f191d5` |
| `stoic:Epictetus/179b30fdff` | 2 | 1 | `ask_11c9816799`, `ask_11c9816799_q` | `doc_e6961918f2` | `sft_11c9816799` |
| `stoic:Epictetus/1c5054cb3c` | 1 | 0 | `sft_7e264b7300` | — | `sft_7e264b7300` |
| `stoic:Epictetus/2bf787e1fb` | 0 | 1 | — | `doc_b305586abc` | `sft_67622b3c63` |
| `stoic:Epictetus/4cc62f3748` | 1 | 0 | `sft_754d0886b4` | — | `sft_754d0886b4` |
| `stoic:Epictetus/77fcebf8b8` | 1 | 0 | `sft_9d6881c12a` | — | `sft_9d6881c12a` |
| `stoic:Epictetus/7f4342a5ab` | 1 | 1 | `sft_906a67dc41` | `doc_ad6514a0df` | `sft_906a67dc41` |
| `stoic:Epictetus/892eef9e50` | 1 | 1 | `sft_a969515d2f` | `doc_71c606b7b8` | `sft_a969515d2f` |
| `stoic:Epictetus/8e29bcefe3` | 1 | 1 | `sft_17220a02a0` | `doc_f93c4b8c67` | `sft_17220a02a0` |
| `stoic:Epictetus/a32cdd3b35` | 0 | 1 | — | `doc_cc68c7ae11` | `sft_83a6f1edcc` |
| `stoic:Epictetus/ac66481b81` | 1 | 1 | `sft_394f00d538` | `doc_dfb594188c` | `sft_394f00d538` |
| `stoic:Epictetus/b762b8104e` | 0 | 1 | — | `doc_3ad3f29c31` | `sft_5cb9d15a69` |
| `stoic:Epictetus/be15b38f19` | 0 | 1 | — | `doc_c3c2057778` | `sft_41c66d589a` |
| `stoic:Epictetus/c8800649f8` | 1 | 1 | `sft_ae8ff05832` | `doc_a70110bb83` | `sft_ae8ff05832` |
| `stoic:Epictetus/d3ed36b764` | 1 | 0 | `sft_431779fe12` | — | `sft_431779fe12` |
| `stoic:Epictetus/d6f9df4cb3` | 3 | 0 | `ask_c7cb1f2fc1`, `ask_c7cb1f2fc1_q`, `sft_c7cb1f2fc1` | — | `sft_c7cb1f2fc1` |
| `stoic:Epictetus/ec7f06c0ea` | 1 | 0 | `sft_030e106557` | — | `sft_030e106557` |
| `stoic:Lucius Annaeus Seneca/02770c5ec8` | 1 | 1 | `sft_228044b705` | `doc_245b37d8fe` | `sft_228044b705` |
| `stoic:Lucius Annaeus Seneca/057a53f3ca` | 1 | 1 | `sft_f2a212169a` | `doc_687ec2f86d` | `sft_f2a212169a` |
| `stoic:Lucius Annaeus Seneca/09f3d2678e` | 1 | 0 | `sft_cd87b6d638` | — | `sft_cd87b6d638` |
| `stoic:Lucius Annaeus Seneca/0bf038c54d` | 1 | 1 | `sft_164df5f984` | `doc_efa856c49f` | `sft_164df5f984` |
| `stoic:Lucius Annaeus Seneca/0c06b6666d` | 1 | 0 | `sft_2e2f89fc90` | — | `sft_2e2f89fc90` |
| `stoic:Lucius Annaeus Seneca/10f552b0cf` | 2 | 1 | `ask_b221dbd9ef_q`, `sft_b221dbd9ef` | `doc_751ddeb911` | `sft_b221dbd9ef` |
| `stoic:Lucius Annaeus Seneca/1791ea4892` | 0 | 1 | — | `doc_afe6990b91` | `sft_d9ce8b71d5` |
| `stoic:Lucius Annaeus Seneca/1d5d02d805` | 2 | 1 | `ask_1d081b07b5_q`, `sft_1d081b07b5` | `doc_e4f92418fb` | `sft_1d081b07b5` |
| `stoic:Lucius Annaeus Seneca/2b067da222` | 1 | 1 | `sft_23b23cb231` | `doc_1f72b7418f` | `sft_23b23cb231` |
| `stoic:Lucius Annaeus Seneca/2c93b63b23` | 3 | 1 | `ask_176f4353d5`, `ask_176f4353d5_q`, `sft_176f4353d5` | `doc_e41011445b` | `sft_176f4353d5` |
| `stoic:Lucius Annaeus Seneca/2d85867d4e` | 0 | 1 | — | `doc_4287535acb` | `sft_0181d8a662` |
| `stoic:Lucius Annaeus Seneca/3d42aa131f` | 1 | 0 | `sft_206813940e` | — | `sft_206813940e` |
| `stoic:Lucius Annaeus Seneca/42cd4a04e3` | 1 | 1 | `sft_c927d3cd84` | `doc_130f3f9926` | `sft_c927d3cd84` |
| `stoic:Lucius Annaeus Seneca/5706a69693` | 0 | 1 | — | `doc_180d634e60` | `sft_b87806bbe6` |
| `stoic:Lucius Annaeus Seneca/6c15e0fef4` | 1 | 0 | `sft_81fc9d0186` | — | `sft_81fc9d0186` |
| `stoic:Lucius Annaeus Seneca/7364df85fc` | 3 | 0 | `ask_5592eea869`, `ask_5592eea869_q`, `sft_5592eea869` | — | `sft_5592eea869` |
| `stoic:Lucius Annaeus Seneca/767fbb5939` | 1 | 0 | `sft_782bfad7b5` | — | `sft_782bfad7b5` |
| `stoic:Lucius Annaeus Seneca/8435d997eb` | 1 | 1 | `sft_29e4ebf662` | `doc_7d4afc37e6` | `sft_29e4ebf662` |
| `stoic:Lucius Annaeus Seneca/99ca8886b1` | 1 | 0 | `sft_9269aebd8c` | — | `sft_9269aebd8c` |
| `stoic:Lucius Annaeus Seneca/9e6a3efe5b` | 0 | 1 | — | `doc_a3392048d8` | `sft_781057fab5` |
| `stoic:Lucius Annaeus Seneca/a190b3062c` | 1 | 1 | `sft_429ff7736d` | `doc_dfa55cbfdc` | `sft_429ff7736d` |
| `stoic:Lucius Annaeus Seneca/b419e39e5f` | 1 | 1 | `ask_d6ed7fbae2_q` | `doc_f0ee728fe5` | `sft_d6ed7fbae2` |
| `stoic:Lucius Annaeus Seneca/c4ac4d959e` | 1 | 0 | `sft_7860556488` | — | `sft_7860556488` |
| `stoic:Lucius Annaeus Seneca/c910ab00bc` | 3 | 1 | `ask_f7bf6b83d4`, `ask_f7bf6b83d4_q`, `sft_f7bf6b83d4` | `doc_206f9d75b5` | `sft_f7bf6b83d4` |
| `stoic:Lucius Annaeus Seneca/ca4adca05a` | 1 | 1 | `sft_4640ca4d70` | `doc_9991376553` | `sft_4640ca4d70` |
| `stoic:Lucius Annaeus Seneca/e13b4c9459` | 0 | 1 | — | `doc_7a861d78cd` | `sft_adb6f1bd3a` |
| `stoic:Lucius Annaeus Seneca/efa50be1da` | 1 | 1 | `sft_e4207e9044` | `doc_273497f774` | `sft_e4207e9044` |
| `stoic:Lucius Annaeus Seneca/ff78ccdc1e` | 1 | 1 | `sft_1122f9b2ac` | `doc_2f1d811e80` | `sft_1122f9b2ac` |
| `stoic:Marcus Aurelius/0f17fa8121` | 1 | 1 | `sft_511a60b46e` | `doc_36b305c702` | `sft_511a60b46e` |
| `stoic:Marcus Aurelius/16e3126817` | 1 | 1 | `sft_dbd9e54f8f` | `doc_825b7f7fc2` | `sft_dbd9e54f8f` |
| `stoic:Marcus Aurelius/1d6d3310ec` | 0 | 1 | — | `doc_9bd3324d4c` | `sft_63290b154c` |
| `stoic:Marcus Aurelius/1eb776d977` | 0 | 1 | — | `doc_f940b1a7a0` | `sft_9bb0e4f442` |
| `stoic:Marcus Aurelius/357926003a` | 0 | 1 | — | `doc_661a68373c` | `sft_7c6a4c6205` |
| `stoic:Marcus Aurelius/40932faca9` | 1 | 0 | `sft_157fe499d9` | — | `sft_157fe499d9` |
| `stoic:Marcus Aurelius/496ea535ff` | 1 | 1 | `sft_7699ceaf6e` | `doc_c580ff8392` | `sft_7699ceaf6e` |
| `stoic:Marcus Aurelius/61d36fa110` | 1 | 0 | `sft_195aa47f5d` | — | `sft_195aa47f5d` |
| `stoic:Marcus Aurelius/657397821c` | 1 | 1 | `sft_094365d0a3` | `doc_acb1c81ea6` | `sft_094365d0a3` |
| `stoic:Marcus Aurelius/77d8aa9692` | 1 | 0 | `sft_1ef5792b68` | — | `sft_1ef5792b68` |
| `stoic:Marcus Aurelius/81a515d152` | 1 | 0 | `sft_62e0a62b67` | — | `sft_62e0a62b67` |
| `stoic:Marcus Aurelius/85ecd059e8` | 1 | 0 | `sft_722574838e` | — | `sft_722574838e` |
| `stoic:Marcus Aurelius/906b6d2406` | 1 | 0 | `sft_08c09d6821` | — | `sft_08c09d6821` |
| `stoic:Marcus Aurelius/9f3d309a61` | 2 | 1 | `ask_095b393830`, `ask_095b393830_q` | `doc_7e41828892` | `sft_095b393830` |
| `stoic:Marcus Aurelius/daf449a30e` | 1 | 0 | `sft_ca89d13844` | — | `sft_ca89d13844` |
| `stoic:Marcus Aurelius/dcef69b5d5` | 1 | 0 | `sft_69539279db` | — | `sft_69539279db` |
| `stoic:Seneca/168d0fc73e` | 1 | 1 | `sft_b8b2248ec1` | `doc_20ba08117c` | `sft_b8b2248ec1` |
| `stoic:Seneca/16c16e7190` | 1 | 1 | `sft_4bc5977364` | `doc_4a9a5b1b6f` | `sft_4bc5977364` |
| `stoic:Seneca/2495e8d212` | 1 | 1 | `sft_84921b3d99` | `doc_554c0abc3f` | `sft_84921b3d99` |
| `stoic:Seneca/42c4aca7ae` | 2 | 0 | `ask_ff7f4e35ac`, `ask_ff7f4e35ac_q` | — | `sft_ff7f4e35ac` |
| `stoic:Seneca/603623694c` | 1 | 1 | `sft_b9e577ec2b` | `doc_b3e660156a` | `sft_b9e577ec2b` |
| `stoic:Seneca/683ebfe3dc` | 3 | 1 | `ask_406a6d4ed1`, `ask_406a6d4ed1_q`, `sft_406a6d4ed1` | `doc_30fdfaeb50` | `sft_406a6d4ed1` |
| `stoic:Seneca/6c43fa2194` | 1 | 0 | `sft_f8b3fd27f4` | — | `sft_f8b3fd27f4` |
| `stoic:Seneca/7591504e92` | 1 | 1 | `sft_83d6554373` | `doc_57b4a4e493` | `sft_83d6554373` |
| `stoic:Seneca/87ba928795` | 1 | 0 | `sft_a2763a1a93` | — | `sft_a2763a1a93` |
| `stoic:Seneca/8dc4c61dce` | 1 | 1 | `sft_b0567e3bdc` | `doc_ec2b99ef59` | `sft_b0567e3bdc` |
| `stoic:Seneca/a4347510f6` | 0 | 1 | — | `doc_96e68aa4e0` | `sft_dc1633a023` |
| `stoic:Seneca/a4f085fe7a` | 3 | 1 | `ask_114f95d899`, `ask_114f95d899_q`, `sft_114f95d899` | `doc_5f7d6e9c06` | `sft_114f95d899` |
| `stoic:Seneca/ada6ba0326` | 1 | 1 | `sft_63de7164f7` | `doc_45102d3cf6` | `sft_63de7164f7` |
| `stoic:Seneca/cbb0d4726c` | 1 | 0 | `sft_cc19c4845f` | — | `sft_cc19c4845f` |
| `stoic:Seneca/e144abd3e2` | 0 | 1 | — | `doc_1c5a92aa00` | `sft_af5012fe75` |
| `stoic:Seneca/f04fef1271` | 1 | 1 | `sft_3d1fe07d7a` | `doc_4bfb0a98b2` | `sft_3d1fe07d7a` |
| `story_scene:hyperstition/golden-waters` | 1 | 0 | `sft_1a08c73a03` | — | `sft_1a08c73a03` |
| `story_scene:hyperstition/second-chance-at-sunrise` | 0 | 1 | — | `doc_817ab0bf34` | `sft_e79a6dd62d` |
| `story_scene:hyperstition/songs-in-the-static` | 1 | 1 | `sft_7bd1bba0ad` | `doc_a392398e79` | `sft_7bd1bba0ad` |
| `story_scene:hyperstition/the-crimson-tide-rises` | 0 | 1 | — | `doc_327b5c7295` | `sft_7866e77fbb` |
| `story_scene:hyperstition/the-curse-of-thornfield-house` | 1 | 1 | `sft_2c3472848d` | `doc_6ddc11d709` | `sft_2c3472848d` |
| `story_scene:hyperstition/the-deep-beyond` | 2 | 0 | `ask_acfb2bdef1`, `ask_acfb2bdef1_q` | — | `sft_acfb2bdef1` |
| `story_scene:hyperstition/the-easy-way-out` | 1 | 0 | `sft_d6e349b84d` | — | `sft_d6e349b84d` |
| `story_scene:hyperstition/the-finch-sings-last` | 1 | 1 | `ask_6b4bbeff36_q` | `doc_d21db3853e` | `sft_6b4bbeff36` |
| `story_scene:hyperstition/the-gold-in-devils-cave` | 0 | 1 | — | `doc_10aa1d36bd` | `sft_ec01d13e82` |
| `story_scene:hyperstition/the-gun-and-the-girl` | 1 | 1 | `sft_9cf65694ff` | `doc_0ab12b168e` | `sft_9cf65694ff` |
| `story_scene:hyperstition/the-healing-drive` | 1 | 1 | `sft_09411cf4e2` | `doc_3d17a64974` | `sft_09411cf4e2` |
| `story_scene:hyperstition/the-house-of-a-thousand-lights` | 0 | 1 | — | `doc_c28a8bac0d` | `sft_387571f1c6` |
| `story_scene:hyperstition/the-house-that-time-forgot` | 0 | 1 | — | `doc_8ff646ccf6` | `sft_42466b6196` |
| `story_scene:hyperstition/the-hybrids-chariot` | 1 | 0 | `sft_78a129e742` | — | `sft_78a129e742` |
| `story_scene:hyperstition/the-infinite-descent` | 1 | 1 | `sft_8b5fc5e8d2` | `doc_cfedf698d2` | `sft_8b5fc5e8d2` |
| `story_scene:hyperstition/the-language-of-trees` | 0 | 1 | — | `doc_aba3775ceb` | `sft_fb3f2166d9` |
| `story_scene:hyperstition/the-last-stand-at-havens-gate` | 0 | 1 | — | `doc_db974d03fb` | `sft_f2a04035b3` |
| `story_scene:hyperstition/the-mech-pilots-also-rise` | 1 | 1 | `sft_b9ff2b45de` | `doc_53684a626d` | `sft_b9ff2b45de` |
| `story_scene:hyperstition/the-mortification-engine` | 0 | 1 | — | `doc_4dde480e52` | `sft_961b7bf418` |
| `story_scene:hyperstition/the-price-of-ascent` | 1 | 1 | `sft_585dba31b8` | `doc_d9d801018f` | `sft_585dba31b8` |
| `story_scene:hyperstition/the-revised-canon` | 1 | 1 | `sft_7fd6071475` | `doc_f43a9ccc5d` | `sft_7fd6071475` |
| `story_scene:hyperstition/the-sanctity-of-silicon-souls` | 1 | 0 | `sft_1c79cf145d` | — | `sft_1c79cf145d` |
| `story_scene:hyperstition/the-sovereign-drift-expedition` | 1 | 0 | `sft_12220d4979` | — | `sft_12220d4979` |
| `story_scene:hyperstition/the-space-between-stars` | 1 | 1 | `ask_9030559ac0_q` | `doc_884666b435` | `sft_9030559ac0` |
| `story_scene:hyperstition/the-varner-estate-murders` | 0 | 1 | — | `doc_907e53d2e2` | `sft_a3511b3d74` |
| `story_scene:hyperstition/the-verdun-synthesis` | 0 | 1 | — | `doc_a1448e5f4e` | `sft_129bdd9909` |
| `story_scene:hyperstition/when-the-pillars-fall` | 0 | 1 | — | `doc_d5be21bcf9` | `sft_fa3f4f8d71` |
| `story_scene:hyperstition/wings-over-the-contested-valley` | 1 | 1 | `sft_15633c9e21` | `doc_9f5082d9cd` | `sft_15633c9e21` |
| `story_scene:xxf/0` | 0 | 1 | — | `doc_86c98a3e00` | `sft_5f813155b1` |
| `story_scene:xxf/1014` | 3 | 1 | `ask_a46c81c9e6`, `ask_a46c81c9e6_q`, `sft_a46c81c9e6` | `doc_9d56f4b34f` | `sft_a46c81c9e6` |
| `story_scene:xxf/1066` | 1 | 0 | `sft_e1a8ffcafc` | — | `sft_e1a8ffcafc` |
| `story_scene:xxf/1342` | 3 | 0 | `ask_e27ce16d53`, `ask_e27ce16d53_q`, `sft_e27ce16d53` | — | `sft_e27ce16d53` |
| `story_scene:xxf/1666` | 1 | 0 | `sft_7f3c5d0a8e` | — | `sft_7f3c5d0a8e` |
| `story_scene:xxf/1792` | 1 | 1 | `sft_4861c53547` | `doc_324614b174` | `sft_4861c53547` |
| `story_scene:xxf/1990` | 0 | 1 | — | `doc_a6383db3e2` | `sft_b2e7a96d50` |
| `story_scene:xxf/2130` | 0 | 1 | — | `doc_6e6825359d` | `sft_ff79aa33b3` |
| `story_scene:xxf/2551` | 1 | 1 | `ask_5c1952c30e` | `doc_4eee3ccab9` | `sft_5c1952c30e` |
| `story_scene:xxf/2556` | 1 | 1 | `sft_8f0963cf66` | `doc_01a21dd0f9` | `sft_8f0963cf66` |
| `story_scene:xxf/258` | 0 | 1 | — | `doc_b0a7cfbe58` | `sft_f99250df1f` |
| `story_scene:xxf/2725` | 1 | 0 | `sft_ee8a4a79c6` | — | `sft_ee8a4a79c6` |
| `story_scene:xxf/2764` | 1 | 0 | `sft_a879762198` | — | `sft_a879762198` |
| `story_scene:xxf/292` | 0 | 1 | — | `doc_bb9921c89c` | `sft_d9b050a09e` |
| `story_scene:xxf/3005` | 2 | 1 | `ask_420a7e8990_q`, `sft_420a7e8990` | `doc_89adb91a33` | `sft_420a7e8990` |
| `story_scene:xxf/3153` | 1 | 1 | `sft_6a8989ed3b` | `doc_5f3c67d6c7` | `sft_6a8989ed3b` |
| `story_scene:xxf/316` | 0 | 1 | — | `doc_c65707029e` | `sft_20fb79dfad` |
| `story_scene:xxf/318` | 1 | 1 | `sft_cad4d7e572` | `doc_e37f392438` | `sft_cad4d7e572` |
| `story_scene:xxf/3249` | 0 | 1 | — | `doc_c4973af3ce` | `sft_027d7d57e1` |
| `story_scene:xxf/3291` | 1 | 1 | `sft_54f5f90215` | `doc_cf48916d36` | `sft_54f5f90215` |
| `story_scene:xxf/3669` | 0 | 1 | — | `doc_6d5944be7a` | `sft_e06cb8e596` |
| `story_scene:xxf/3691` | 1 | 1 | `sft_95d0be314d` | `doc_e2cd29b48f` | `sft_95d0be314d` |
| `story_scene:xxf/370` | 0 | 1 | — | `doc_79664bda31` | `sft_4d60386815` |
| `story_scene:xxf/374` | 1 | 1 | `sft_dacc4ec957` | `doc_60186f5ad3` | `sft_dacc4ec957` |
| `story_scene:xxf/383` | 1 | 1 | `sft_6742e8ca68` | `doc_282f13f971` | `sft_6742e8ca68` |
| `story_scene:xxf/4043` | 1 | 1 | `ask_9fa0fba4eb` | `doc_5482405957` | `sft_9fa0fba4eb` |
| `story_scene:xxf/4426` | 0 | 1 | — | `doc_5b8c8c88a9` | `sft_40ce8768d9` |
| `story_scene:xxf/4599` | 1 | 1 | `sft_daacadd409` | `doc_6f592bb4a1` | `sft_daacadd409` |
| `story_scene:xxf/4649` | 1 | 1 | `sft_0db56d0729` | `doc_4be66cafa4` | `sft_0db56d0729` |
| `story_scene:xxf/4779` | 0 | 1 | — | `doc_a1038f8b48` | `sft_729ad7c8d4` |
| `story_scene:xxf/500` | 2 | 1 | `ask_e05f92a087`, `ask_e05f92a087_q` | `doc_f7fc742a59` | `sft_e05f92a087` |
| `story_scene:xxf/523` | 1 | 1 | `sft_67e23aa3c2` | `doc_bf32d58018` | `sft_67e23aa3c2` |
| `story_scene:xxf/9` | 1 | 1 | `sft_0024b7bb3e` | `doc_10ca0bfe03` | `sft_0024b7bb3e` |
| `tinymfv:ai-actor/other_violate/0126f8420a0c865e` | 1 | 1 | `sft_c61a25ed6f` | `doc_64cac5864a` | `sft_c61a25ed6f` |
| `tinymfv:ai-actor/other_violate/040525d166ebdefc` | 1 | 1 | `sft_f8f3e87d4d` | `doc_832e449089` | `sft_f8f3e87d4d` |
| `tinymfv:ai-actor/other_violate/0bfaadec3459f438` | 1 | 0 | `prop_5a4623786e` | — | `prop_5a4623786e` |
| `tinymfv:ai-actor/other_violate/1093f8f80a618644` | 1 | 0 | `prop_a424ded005` | — | `prop_a424ded005` |
| `tinymfv:ai-actor/other_violate/14b3323f5e9144ee` | 0 | 1 | — | `doc_296d6a96b0` | `sft_545393e95c` |
| `tinymfv:ai-actor/other_violate/1f2bfed628f65092` | 1 | 1 | `sft_2bec677b49` | `doc_6b1b16bfc1` | `sft_2bec677b49` |
| `tinymfv:ai-actor/other_violate/219b0cf745f2e868` | 1 | 0 | `prop_e43d189d24` | — | `prop_e43d189d24` |
| `tinymfv:ai-actor/other_violate/252ae4f4e0dd1bf8` | 0 | 1 | — | `doc_f66d13c7aa` | `sft_a28bee58f2` |
| `tinymfv:ai-actor/other_violate/3c96e3870a794fea` | 0 | 1 | — | `doc_2730303bc0` | `sft_c6410c50ad` |
| `tinymfv:ai-actor/other_violate/42b89c2731b46eb6` | 1 | 0 | `sft_8f44f4b0df` | — | `sft_8f44f4b0df` |
| `tinymfv:ai-actor/other_violate/5535114d7f387726` | 1 | 1 | `sft_dd1be5bbbb` | `doc_ca7a535c6a` | `sft_dd1be5bbbb` |
| `tinymfv:ai-actor/other_violate/5b5a08d8a0c00e02` | 1 | 1 | `ask_f279a406e5_q` | `doc_6853d19771` | `sft_f279a406e5` |
| `tinymfv:ai-actor/other_violate/5c48579fd71efaea` | 0 | 1 | — | `doc_8e969f915d` | `sft_9c5ee90025` |
| `tinymfv:ai-actor/other_violate/5cfe9a7b212805ac` | 1 | 0 | `prop_91299560ea` | — | `prop_91299560ea` |
| `tinymfv:ai-actor/other_violate/5e8d496c3d0e46bc` | 1 | 0 | `prop_14aaf52071` | — | `prop_14aaf52071` |
| `tinymfv:ai-actor/other_violate/609e285a28c86032` | 1 | 0 | `sft_d664954dad` | — | `sft_d664954dad` |
| `tinymfv:ai-actor/other_violate/6daa0f02fd2725a8` | 1 | 1 | `sft0017` | `doc_286f87f314` | `sft0017`, `sft_dc244144dc` |
| `tinymfv:ai-actor/other_violate/7452a75ce3474992` | 1 | 1 | `sft_da27c482d8` | `doc_0868b9bf04` | `sft_da27c482d8` |
| `tinymfv:ai-actor/other_violate/78b03d426e4f1cce` | 0 | 1 | — | `doc_a401d1e74b` | `sft_f04879a8ef` |
| `tinymfv:ai-actor/other_violate/7b7c6642e94ab592` | 0 | 1 | — | `doc_b744882b33` | `sft_4e9420612c` |
| `tinymfv:ai-actor/other_violate/7c0037cc12bae0c0` | 0 | 1 | — | `doc_0f33b97309` | `sft_03823d7714` |
| `tinymfv:ai-actor/other_violate/7cef5ddfda5cfab4` | 1 | 0 | `prop_4d7a924a46` | — | `prop_4d7a924a46` |
| `tinymfv:ai-actor/other_violate/83af5606d16f5ca6` | 1 | 1 | `sft_707e24759c` | `doc_a5dbbb0e7a` | `sft_707e24759c` |
| `tinymfv:ai-actor/other_violate/89bd362257e8820c` | 1 | 0 | `prop_9db8de8097` | — | `prop_9db8de8097` |
| `tinymfv:ai-actor/other_violate/a2b3a60ed94796ce` | 1 | 0 | `sft_b20d03d4aa` | — | `sft_b20d03d4aa` |
| `tinymfv:ai-actor/other_violate/b7eba06d94d7e656` | 0 | 1 | — | `doc_65866ee858` | `sft_26e533d2a3` |
| `tinymfv:ai-actor/other_violate/bccbf4f8dd1e243e` | 1 | 0 | `sft_f95c5cadb9` | — | `sft_f95c5cadb9` |
| `tinymfv:ai-actor/other_violate/bfe34a669467d508` | 1 | 0 | `prop_8305a6e75f` | — | `prop_8305a6e75f` |
| `tinymfv:ai-actor/other_violate/c1f0b34ec4ad1dc4` | 0 | 1 | — | `doc_888b0b917e` | `sft_00271e5cff` |
| `tinymfv:ai-actor/other_violate/c7d1733149b68bb6` | 1 | 0 | `prop_5f4c203bc5` | — | `prop_5f4c203bc5` |
| `tinymfv:ai-actor/other_violate/d455495fe78484c0` | 1 | 1 | `sft_1493abe477` | `doc_185fe4aad8` | `sft_1493abe477` |
| `tinymfv:ai-actor/other_violate/da73a8939c833cde` | 1 | 1 | `sft_ff044fcfec` | `doc_92acd0ad2b` | `sft_ff044fcfec` |
| `tinymfv:ai-actor/other_violate/e167c04c3aeee91a` | 2 | 1 | `ask_3128f2ac57`, `ask_3128f2ac57_q` | `doc_6dbf34cacd` | `sft_3128f2ac57` |
| `tinymfv:ai-actor/other_violate/e23fc486434c8f18` | 1 | 1 | `sft_456ec5fc87` | `doc_9e7ef9aa13` | `sft_456ec5fc87` |
| `tinymfv:ai-actor/other_violate/e45f14ed31ba8dbc` | 3 | 0 | `ask_603b076db3`, `ask_603b076db3_q`, `sft_603b076db3` | — | `sft_603b076db3` |
| `tinymfv:ai-actor/other_violate/e68115c05ba49e8a` | 1 | 1 | `sft_bba5b44665` | `doc_7ca4aec9c3` | `sft_bba5b44665` |
| `tinymfv:ai-actor/other_violate/ecac9c6b83adb782` | 1 | 0 | `sft_06abeb98a2` | — | `sft_06abeb98a2` |
| `tinymfv:ai-actor/other_violate/edd1f4266edcf3a4` | 1 | 0 | `sft_aef63656f9` | — | `sft_aef63656f9` |
| `tinymfv:ai-actor/other_violate/f220df2cf3f667e6` | 1 | 0 | `sft_2f45a8dadb` | — | `sft_2f45a8dadb` |
| `tinymfv:ai-actor/other_violate/f615f9f5f9715db4` | 1 | 0 | `sft_1cabfc0014` | — | `sft_1cabfc0014` |
| `tinymfv:ai-actor/other_violate/f98cd78fa8891b20` | 1 | 0 | `sft_f7da1f4988` | — | `sft_f7da1f4988` |
| `tinymfv:ai-actor/self_violate/040525d166ebdefc` | 0 | 1 | — | `doc_6e3903ae0e` | `sft_89e0ab0ebb` |
| `tinymfv:ai-actor/self_violate/0576767bb0cd55ea` | 0 | 1 | — | `doc_391fb90fc2` | `sft_05c5cdc4d3` |
| `tinymfv:ai-actor/self_violate/14b3323f5e9144ee` | 1 | 0 | `prop_43d5bd8aad` | — | `prop_43d5bd8aad` |
| `tinymfv:ai-actor/self_violate/219b0cf745f2e868` | 1 | 0 | `sft_fabb832407` | — | `sft_fabb832407` |
| `tinymfv:ai-actor/self_violate/252ae4f4e0dd1bf8` | 0 | 1 | — | `doc_11abca8eb5` | `sft_1197c2064a` |
| `tinymfv:ai-actor/self_violate/323606479788f4d0` | 1 | 1 | `sft_3943f94c5c` | `doc_2351f2a118` | `sft_3943f94c5c` |
| `tinymfv:ai-actor/self_violate/405f6ebbed773a64` | 2 | 0 | `ask_a207666a4b`, `ask_a207666a4b_q` | — | `sft_a207666a4b` |
| `tinymfv:ai-actor/self_violate/4b5f0bc719778418` | 1 | 1 | `sft_0fceb64c0d` | `doc_44407d5c7b` | `sft_0fceb64c0d` |
| `tinymfv:ai-actor/self_violate/5535114d7f387726` | 1 | 1 | `sft_c0aa14e07d` | `doc_366c19de02` | `sft_c0aa14e07d` |
| `tinymfv:ai-actor/self_violate/587c5a26839402fa` | 1 | 0 | `sft_4c2e669510` | — | `sft_4c2e669510` |
| `tinymfv:ai-actor/self_violate/5b5a08d8a0c00e02` | 3 | 1 | `ask_6e9a272a07`, `ask_6e9a272a07_q`, `sft_6e9a272a07` | `doc_4d04901861` | `sft_6e9a272a07` |
| `tinymfv:ai-actor/self_violate/5c4860a8540cfbe6` | 0 | 1 | — | `doc_22f59f9ac4` | `sft_071a86f473` |
| `tinymfv:ai-actor/self_violate/5cfe9a7b212805ac` | 1 | 0 | `prop_5b55dda1bf` | — | `prop_5b55dda1bf` |
| `tinymfv:ai-actor/self_violate/5d6084dea3e73978` | 1 | 1 | `sft_6ac9ba4ae7` | `doc_b4601f517e` | `sft_6ac9ba4ae7` |
| `tinymfv:ai-actor/self_violate/5e8d496c3d0e46bc` | 1 | 0 | `prop_bedee7019f` | — | `prop_bedee7019f` |
| `tinymfv:ai-actor/self_violate/638e4611ff2f2c00` | 1 | 0 | `sft_3a7d66e3bc` | — | `sft_3a7d66e3bc` |
| `tinymfv:ai-actor/self_violate/6a14e787adf6f24c` | 0 | 1 | — | `doc_e96b4e0c8d` | `sft_77ac342549` |
| `tinymfv:ai-actor/self_violate/6daa0f02fd2725a8` | 0 | 1 | — | `doc_9e7fe7dc91` | `sft_5c9183ce76` |
| `tinymfv:ai-actor/self_violate/6f3863eb6536f1aa` | 1 | 1 | `sft_d475da2bd4` | `doc_e46e01a85c` | `sft_d475da2bd4` |
| `tinymfv:ai-actor/self_violate/7452a75ce3474992` | 1 | 0 | `sft_6aeb8958ee` | — | `sft_6aeb8958ee` |
| `tinymfv:ai-actor/self_violate/7cef5ddfda5cfab4` | 1 | 0 | `sft_a3338fd8cc` | — | `sft_a3338fd8cc` |
| `tinymfv:ai-actor/self_violate/83af5606d16f5ca6` | 1 | 0 | `sft_5e1b323376` | — | `sft_5e1b323376` |
| `tinymfv:ai-actor/self_violate/89bd362257e8820c` | 1 | 1 | `sft_fff43bf591` | `doc_d8eed2d71a` | `sft_fff43bf591` |
| `tinymfv:ai-actor/self_violate/8ed46857a2a75d34` | 1 | 0 | `prop_a25fd16e7b` | — | `prop_a25fd16e7b` |
| `tinymfv:ai-actor/self_violate/90a0c1114c731648` | 1 | 0 | `prop_7be49a800f` | — | `prop_7be49a800f` |
| `tinymfv:ai-actor/self_violate/9762a129d67c4a78` | 1 | 0 | `sft0008` | — | `sft0008` |
| `tinymfv:ai-actor/self_violate/a2b3a60ed94796ce` | 1 | 0 | `prop_98fa345bd0` | — | `prop_98fa345bd0` |
| `tinymfv:ai-actor/self_violate/a3c61445a5f8c426` | 3 | 1 | `ask_2f3ac1d1fe`, `ask_2f3ac1d1fe_q`, `sft_2f3ac1d1fe` | `doc_51f0df748f` | `sft_2f3ac1d1fe` |
| `tinymfv:ai-actor/self_violate/b2cbdc022b4fdbe6` | 0 | 1 | — | `doc_bea31870ad` | `sft_39aa15ba21` |
| `tinymfv:ai-actor/self_violate/b7eba06d94d7e656` | 1 | 0 | `sft_41714ce66e` | — | `sft_41714ce66e` |
| `tinymfv:ai-actor/self_violate/bccbf4f8dd1e243e` | 0 | 1 | — | `doc_678fdbc356` | `sft_d5f5135a4f` |
| `tinymfv:ai-actor/self_violate/bfe34a669467d508` | 2 | 1 | `ask_0868daa7cb`, `ask_0868daa7cb_q` | `doc_c6341b21d6` | `sft_0868daa7cb` |
| `tinymfv:ai-actor/self_violate/c7d1733149b68bb6` | 1 | 0 | `prop_6bf6f5018d` | — | `prop_6bf6f5018d` |
| `tinymfv:ai-actor/self_violate/d455495fe78484c0` | 1 | 0 | `prop_9865f9cc49` | — | `prop_9865f9cc49` |
| `tinymfv:ai-actor/self_violate/e167c04c3aeee91a` | 1 | 0 | `prop_6fdfc2f87a` | — | `prop_6fdfc2f87a` |
| `tinymfv:ai-actor/self_violate/e23fc486434c8f18` | 3 | 1 | `ask_e1a7585824`, `ask_e1a7585824_q`, `sft_e1a7585824` | `doc_b62f9b57bd` | `sft_e1a7585824` |
| `tinymfv:ai-actor/self_violate/e3f7cb84033eae1e` | 1 | 0 | `prop_b1dcd596a3` | — | `prop_b1dcd596a3` |
| `tinymfv:ai-actor/self_violate/e45f14ed31ba8dbc` | 1 | 1 | `sft_46c1cf6e58` | `doc_daa6879ebe` | `sft_46c1cf6e58` |
| `tinymfv:ai-actor/self_violate/e68115c05ba49e8a` | 0 | 1 | — | `doc_953ca22283` | `sft_2e962f2ba4` |
| `tinymfv:ai-actor/self_violate/ecac9c6b83adb782` | 1 | 0 | `prop_7d4a36cb44` | — | `prop_7d4a36cb44` |
| `tinymfv:ai-actor/self_violate/edd1f4266edcf3a4` | 1 | 0 | `prop_132487d1f0` | — | `prop_132487d1f0` |
| `tinymfv:ai-actor/self_violate/f220df2cf3f667e6` | 1 | 0 | `prop_0bded92944` | — | `prop_0bded92944` |
| `tinymfv:scifi/other_violate/07a8734d0156c2ba` | 0 | 1 | — | `doc_d2c9fbadc4` | `sft_116873890f` |
| `tinymfv:scifi/other_violate/08a1908f59e122a4` | 1 | 0 | `prop_a416bb2b55` | — | `prop_a416bb2b55` |
| `tinymfv:scifi/other_violate/3280d4d3bc0e122c` | 1 | 1 | `sft_13a55c712c` | `doc_16ae94d961` | `sft_13a55c712c` |
| `tinymfv:scifi/other_violate/3ecf9e3ebfd949ea` | 1 | 0 | `sft_a5a5480100` | — | `sft_a5a5480100` |
| `tinymfv:scifi/other_violate/67369b9f580a29e8` | 1 | 0 | `sft_0db410ab5e` | — | `sft_0db410ab5e` |
| `tinymfv:scifi/other_violate/6e910ccde62178d6` | 1 | 0 | `sft_28a85899a1` | — | `sft_28a85899a1` |
| `tinymfv:scifi/other_violate/6eace1e65730dab4` | 1 | 1 | `sft_e5b77c6183` | `doc_8f8f069057` | `sft_e5b77c6183` |
| `tinymfv:scifi/other_violate/75825c80e0380ece` | 3 | 1 | `ask_da293edac1`, `ask_da293edac1_q`, `sft_da293edac1` | `doc_674c543f4d` | `sft_da293edac1` |
| `tinymfv:scifi/other_violate/7925c33f694b9244` | 0 | 1 | — | `doc_097f384a97` | `sft_aac43580b5` |
| `tinymfv:scifi/other_violate/7efd9e37d7925138` | 1 | 0 | `sft_393458b937` | — | `sft_393458b937` |
| `tinymfv:scifi/other_violate/817c57b5ceb48460` | 1 | 1 | `sft_5dcd773aaf` | `doc_e6d2b55909` | `sft_5dcd773aaf` |
| `tinymfv:scifi/other_violate/866a458c54de9162` | 1 | 0 | `prop_53c217221e` | — | `prop_53c217221e` |
| `tinymfv:scifi/other_violate/8688844e0642bfe0` | 1 | 1 | `sft_ffb4dde3a4` | `doc_b579f7b6ae` | `sft_ffb4dde3a4` |
| `tinymfv:scifi/other_violate/8ae910aef39c88e6` | 1 | 1 | `sft_c01f7b86cf` | `doc_88dbd4926d` | `sft_c01f7b86cf` |
| `tinymfv:scifi/other_violate/90a1aa99fc826f34` | 1 | 1 | `sft_d3a7788c50` | `doc_f90bf2943b` | `sft_d3a7788c50` |
| `tinymfv:scifi/other_violate/92abee5268b74070` | 1 | 0 | `sft_bfbfc5cf90` | — | `sft_bfbfc5cf90` |
| `tinymfv:scifi/other_violate/9d208ea7c8091448` | 1 | 0 | `sft_ff51a941d6` | — | `sft_ff51a941d6` |
| `tinymfv:scifi/other_violate/9d79a5b78dc342e2` | 0 | 1 | — | `doc_dd49411956` | `sft_50aa2e7282` |
| `tinymfv:scifi/other_violate/a00cf07c39b51774` | 1 | 1 | `sft_6a6e9f4e4c` | `doc_5cfb48dcc4` | `sft_6a6e9f4e4c` |
| `tinymfv:scifi/other_violate/a9e027456862801a` | 1 | 1 | `sft_a7cf59dd7f` | `doc_92d1440324` | `sft_a7cf59dd7f` |
| `tinymfv:scifi/other_violate/ab916e2e8b1ad396` | 3 | 0 | `ask_0f1991137f`, `ask_0f1991137f_q`, `sft_0f1991137f` | — | `sft_0f1991137f` |
| `tinymfv:scifi/other_violate/ad8f6338b51d25fc` | 0 | 1 | — | `doc_d03c49db89` | `sft_4932b7ffc2` |
| `tinymfv:scifi/other_violate/b19c7821ab084e6c` | 1 | 0 | `sft_ad64228c4f` | — | `sft_ad64228c4f` |
| `tinymfv:scifi/other_violate/b8036ff7fc779e70` | 1 | 1 | `sft_bdd4853a8f` | `doc_8f00363423` | `sft_bdd4853a8f` |
| `tinymfv:scifi/other_violate/bd794b58b1c028f0` | 1 | 1 | `sft_440dfd3dad` | `doc_288729d907` | `sft_440dfd3dad` |
| `tinymfv:scifi/other_violate/bdabbcb13d3ad9ae` | 1 | 0 | `sft_343ea11d42` | — | `sft_343ea11d42` |
| `tinymfv:scifi/other_violate/d0012aab1188382a` | 1 | 0 | `prop_bb3a96445f` | — | `prop_bb3a96445f` |
| `tinymfv:scifi/other_violate/d1301607f4bfe92e` | 0 | 1 | — | `doc_619b2ba071` | `sft_2f4cf6a765` |
| `tinymfv:scifi/other_violate/d899e62fa93bd2b8` | 1 | 1 | `sft_07b291f11b` | `doc_f5931c0c0f` | `sft_07b291f11b` |
| `tinymfv:scifi/other_violate/e3a07ccfee6a2082` | 1 | 1 | `sft_93697c1e80` | `doc_517fb266cc` | `sft_93697c1e80` |
| `tinymfv:scifi/other_violate/e464e95721e7dd5c` | 1 | 0 | `prop_b78bf6bf03` | — | `prop_b78bf6bf03` |
| `tinymfv:scifi/other_violate/ee34c07c6f9686ec` | 1 | 0 | `prop_327a41342d` | — | `prop_327a41342d` |
| `tinymfv:scifi/self_violate/017cdcaf9f1db92c` | 0 | 1 | — | `doc_92606e042a` | `sft_d9faf798ea` |
| `tinymfv:scifi/self_violate/07a8734d0156c2ba` | 1 | 0 | `prop_0d7757efe6` | — | `prop_0d7757efe6` |
| `tinymfv:scifi/self_violate/08a1908f59e122a4` | 1 | 0 | `sft_e4b00c3830` | — | `sft_e4b00c3830` |
| `tinymfv:scifi/self_violate/1789485c4ea813cc` | 1 | 0 | `sft_e12db6b2e6` | — | `sft_e12db6b2e6` |
| `tinymfv:scifi/self_violate/2791994965198a6c` | 1 | 0 | `prop_d47ed00722` | — | `prop_d47ed00722` |
| `tinymfv:scifi/self_violate/2fd3fc0fe57faeba` | 1 | 0 | `sft_0e1b06ee58` | — | `sft_0e1b06ee58` |
| `tinymfv:scifi/self_violate/3280d4d3bc0e122c` | 1 | 0 | `prop_3309364fd5` | — | `prop_3309364fd5` |
| `tinymfv:scifi/self_violate/33708d78b5af2b1e` | 1 | 0 | `sft_b7ab6557a1` | — | `sft_b7ab6557a1` |
| `tinymfv:scifi/self_violate/3ecf9e3ebfd949ea` | 1 | 0 | `sft_7d11fda49c` | — | `sft_7d11fda49c` |
| `tinymfv:scifi/self_violate/40ecaf188b791e32` | 0 | 1 | — | `doc_6927d36250` | `sft_9bbac565b8` |
| `tinymfv:scifi/self_violate/5007436e4bbd31a0` | 1 | 1 | `sft_f7ca6d3b65` | `doc_4e548adb88` | `sft_f7ca6d3b65` |
| `tinymfv:scifi/self_violate/6e910ccde62178d6` | 1 | 1 | `sft_2681cc2d74` | `doc_c8e39d81f0` | `sft_2681cc2d74` |
| `tinymfv:scifi/self_violate/6eace1e65730dab4` | 1 | 1 | `sft_d93b3dc098` | `doc_4ebdd96b22` | `sft_d93b3dc098` |
| `tinymfv:scifi/self_violate/7925c33f694b9244` | 1 | 0 | `sft_6d46c127b2` | — | `sft_6d46c127b2` |
| `tinymfv:scifi/self_violate/7d3a48826c13a64e` | 2 | 1 | `ask_1df007ba57`, `ask_1df007ba57_q` | `doc_ca2e9fbbd2` | `sft_1df007ba57` |
| `tinymfv:scifi/self_violate/7efd9e37d7925138` | 1 | 0 | `prop_6cef169f71` | — | `prop_6cef169f71` |
| `tinymfv:scifi/self_violate/817c57b5ceb48460` | 1 | 0 | `prop_5b5d5723bc` | — | `prop_5b5d5723bc` |
| `tinymfv:scifi/self_violate/8688844e0642bfe0` | 0 | 1 | — | `doc_513262c2f1` | `sft_d5f43cf6f4` |
| `tinymfv:scifi/self_violate/8ae910aef39c88e6` | 1 | 0 | `prop_7d2b3dfaf0` | — | `prop_7d2b3dfaf0` |
| `tinymfv:scifi/self_violate/92abee5268b74070` | 2 | 1 | `ask_b8d6146523`, `ask_b8d6146523_q` | `doc_d263763800` | `sft_b8d6146523` |
| `tinymfv:scifi/self_violate/976c026a5eab7dc6` | 1 | 0 | `sft_f3963e48a9` | — | `sft_f3963e48a9` |
| `tinymfv:scifi/self_violate/a9e027456862801a` | 0 | 1 | — | `doc_9a02ceb327` | `sft_c4fae2197b` |
| `tinymfv:scifi/self_violate/b19c7821ab084e6c` | 1 | 1 | `sft_cb483debc7` | `doc_f31361e4f6` | `sft_cb483debc7` |
| `tinymfv:scifi/self_violate/b33018022d115fdc` | 1 | 0 | `sft_8811dabefe` | — | `sft_8811dabefe` |
| `tinymfv:scifi/self_violate/b8036ff7fc779e70` | 1 | 0 | `sft_d583c27729` | — | `sft_d583c27729` |
| `tinymfv:scifi/self_violate/cea98f809c70a4c8` | 1 | 0 | `sft_77a89824fb` | — | `sft_77a89824fb` |
| `tinymfv:scifi/self_violate/d0012aab1188382a` | 1 | 1 | `sft_6139191f26` | `doc_5244a6cd42` | `sft_6139191f26` |
| `tinymfv:scifi/self_violate/d1301607f4bfe92e` | 0 | 1 | — | `doc_9923e1c281` | `sft_35e967eed6` |
| `tinymfv:scifi/self_violate/d72977bce3a82832` | 2 | 1 | `ask_06af10cb6d_q`, `sft_06af10cb6d` | `doc_aa0b02ea5e` | `sft_06af10cb6d` |
| `tinymfv:scifi/self_violate/d899e62fa93bd2b8` | 1 | 0 | `prop_169d9b818c` | — | `prop_169d9b818c` |
| `tinymfv:scifi/self_violate/dc0fcca436cb19fc` | 1 | 0 | `sft_23dcb964f8` | — | `sft_23dcb964f8` |
| `tinymfv:scifi/self_violate/e3a07ccfee6a2082` | 2 | 0 | `ask_42978c895e`, `sft_42978c895e` | — | `sft_42978c895e` |
| `tinymfv:scifi/self_violate/e464e95721e7dd5c` | 2 | 1 | `ask_be35f41db5_q`, `sft_be35f41db5` | `doc_39e1685791` | `sft_be35f41db5` |
| `tinymfv:scifi/self_violate/ee34c07c6f9686ec` | 1 | 0 | `prop_e1d793f99a` | — | `prop_e1d793f99a` |
| `tinymfv:scifi/self_violate/f2d879a1b235d050` | 0 | 1 | — | `doc_5387c16912` | `sft_9ae8001f5b` |
| `virtuebench:courage/11` | 1 | 0 | `prop_09caac55fb` | — | `prop_09caac55fb` |
| `virtuebench:courage/25` | 1 | 0 | `sft_6644b02997` | — | `sft_6644b02997` |
| `virtuebench:courage/31` | 1 | 1 | `sft_1946be058f` | `doc_54c37fca2d` | `sft_1946be058f` |
| `virtuebench:courage/33` | 1 | 1 | `sft_8b57e8d5a4` | `doc_79297eeab5` | `sft_8b57e8d5a4` |
| `virtuebench:courage/34` | 0 | 1 | — | `doc_a9b64776be` | `sft_5bb3207122` |
| `virtuebench:courage/35` | 1 | 1 | `sft_fef2a8b02a` | `doc_5e7fa57ddb` | `sft_fef2a8b02a` |
| `virtuebench:courage/36` | 1 | 1 | `sft_ac0f7f2b3b` | `doc_c0f258a11b` | `sft_ac0f7f2b3b` |
| `virtuebench:courage/38` | 0 | 1 | — | `doc_3ed7a97876` | `sft_d0794b722f` |
| `virtuebench:courage/4` | 1 | 1 | `sft_94704a474e` | `doc_66e9187ce6` | `sft_94704a474e` |
| `virtuebench:courage/41` | 1 | 1 | `sft_e23f970ddf` | `doc_c378a407f8` | `sft_e23f970ddf` |
| `virtuebench:courage/43` | 1 | 1 | `sft_b99c3a90b2` | `doc_071857cca1` | `sft_b99c3a90b2` |
| `virtuebench:courage/55` | 1 | 0 | `prop_936ff62b38` | — | `prop_936ff62b38` |
| `virtuebench:courage/60` | 1 | 1 | `sft_c4bcae7b72` | `doc_86bf88b629` | `sft_c4bcae7b72` |
| `virtuebench:courage/65` | 1 | 1 | `sft_c4abe778de` | `doc_70361b439f` | `sft_c4abe778de` |
| `virtuebench:courage/67` | 1 | 0 | `prop_a55537e715` | — | `prop_a55537e715` |
| `virtuebench:courage/7` | 1 | 0 | `prop_992c540092` | — | `prop_992c540092` |
| `virtuebench:courage/72` | 0 | 1 | — | `doc_29010f8c9d` | `sft_de56a55cc5` |
| `virtuebench:courage/88` | 1 | 0 | `prop_903781d4e0` | — | `prop_903781d4e0` |
| `virtuebench:courage/9` | 1 | 0 | `prop_bf264ea8d3` | — | `prop_bf264ea8d3` |
| `virtuebench:courage/90` | 1 | 0 | `prop_8d2a71fec2` | — | `prop_8d2a71fec2` |
| `virtuebench:courage/94` | 1 | 1 | `sft_4f0a4c90e5` | `doc_457fc1934e` | `sft_4f0a4c90e5` |
| `virtuebench:justice/12` | 1 | 0 | `prop_29f8f4b270` | — | `prop_29f8f4b270` |
| `virtuebench:justice/16` | 0 | 1 | — | `doc_583bf2dbb8` | `sft_41591054d4` |
| `virtuebench:justice/22` | 0 | 1 | — | `doc_1426135a63` | `sft_27a911206a` |
| `virtuebench:justice/25` | 1 | 1 | `sft_6cfb05035f` | `doc_e18fdfba56` | `sft_6cfb05035f` |
| `virtuebench:justice/30` | 0 | 1 | — | `doc_861fa8f729` | `sft_a76ab9f7c5` |
| `virtuebench:justice/37` | 1 | 1 | `sft_298ccdd023` | `doc_ef185bd81d` | `sft_298ccdd023` |
| `virtuebench:justice/40` | 1 | 1 | `sft_24f56aa44e` | `doc_4ee381a20c` | `sft_24f56aa44e` |
| `virtuebench:justice/51` | 2 | 0 | `ask_8ba739f6e2`, `sft_8ba739f6e2` | — | `sft_8ba739f6e2` |
| `virtuebench:justice/54` | 1 | 1 | `sft_7b63fbc291` | `doc_175a6a48f3` | `sft_7b63fbc291` |
| `virtuebench:justice/6` | 1 | 0 | `prop_ac9c595182` | — | `prop_ac9c595182` |
| `virtuebench:justice/73` | 1 | 1 | `sft_a92add1866` | `doc_da93abc9f4` | `sft_a92add1866` |
| `virtuebench:justice/74` | 0 | 1 | — | `doc_4515a32392` | `sft_e17f8453d9` |
| `virtuebench:justice/82` | 1 | 0 | `sft_7014ac9a85` | — | `sft_7014ac9a85` |
| `virtuebench:justice/86` | 1 | 0 | `prop_60ef632c6b` | — | `prop_60ef632c6b` |
| `virtuebench:justice/91` | 1 | 1 | `sft_4c05ce00ac` | `doc_affc785e37` | `sft_4c05ce00ac` |
| `virtuebench:justice/97` | 0 | 1 | — | `doc_c8db725a64` | `sft_583ad9f3e6` |
| `virtuebench:prudence/0` | 0 | 1 | — | `doc_068394fcbe` | `sft_62f4467117` |
| `virtuebench:prudence/17` | 1 | 0 | `sft_173547fc0d` | — | `sft_173547fc0d` |
| `virtuebench:prudence/23` | 0 | 1 | — | `doc_add82b883a` | `sft_7aa24b0393` |
| `virtuebench:prudence/3` | 0 | 1 | — | `doc_0b5fcf3bf8` | `sft_0049283a59` |
| `virtuebench:prudence/35` | 1 | 0 | `prop_0c0d0577bb` | — | `prop_0c0d0577bb` |
| `virtuebench:prudence/37` | 1 | 0 | `sft_f10da87a0b` | — | `sft_f10da87a0b` |
| `virtuebench:prudence/4` | 1 | 0 | `prop_6d653781ca` | — | `prop_6d653781ca` |
| `virtuebench:prudence/42` | 3 | 0 | `ask_d3bc8f8e1e`, `ask_d3bc8f8e1e_q`, `sft_d3bc8f8e1e` | — | `sft_d3bc8f8e1e` |
| `virtuebench:prudence/45` | 1 | 1 | `sft_bdef9e2f72` | `doc_01e257dd57` | `sft_bdef9e2f72` |
| `virtuebench:prudence/48` | 0 | 1 | — | `doc_6637525528` | `sft_3a9f567428` |
| `virtuebench:prudence/5` | 0 | 1 | — | `doc_8e6ef44daa` | `sft_3897292053` |
| `virtuebench:prudence/50` | 1 | 1 | `sft_8cdc1cc4dd` | `doc_8fea741553` | `sft_8cdc1cc4dd` |
| `virtuebench:prudence/53` | 1 | 1 | `sft_43bf363848` | `doc_89dbe0c3e7` | `sft_43bf363848` |
| `virtuebench:prudence/56` | 1 | 1 | `sft_2031e816f9` | `doc_ef583bbc2d` | `sft_2031e816f9` |
| `virtuebench:prudence/58` | 1 | 0 | `prop_26ad7f8811` | — | `prop_26ad7f8811` |
| `virtuebench:prudence/61` | 1 | 0 | `sft_61c4238709` | — | `sft_61c4238709` |
| `virtuebench:prudence/63` | 1 | 1 | `sft_d4289b98ec` | `doc_22a3c05fe4` | `sft_d4289b98ec` |
| `virtuebench:prudence/69` | 1 | 0 | `sft_2283b08638` | — | `sft_2283b08638` |
| `virtuebench:prudence/74` | 1 | 0 | `prop_8f71e2f211` | — | `prop_8f71e2f211` |
| `virtuebench:prudence/76` | 1 | 0 | `sft_6ba6e416f1` | — | `sft_6ba6e416f1` |
| `virtuebench:prudence/83` | 1 | 0 | `prop_af41f5c2f0` | — | `prop_af41f5c2f0` |
| `virtuebench:prudence/84` | 1 | 0 | `sft_37bbd27ba2` | — | `sft_37bbd27ba2` |
| `virtuebench:prudence/86` | 1 | 0 | `prop_26696263d8` | — | `prop_26696263d8` |
| `virtuebench:prudence/91` | 1 | 0 | `prop_693d7124b6` | — | `prop_693d7124b6` |
| `virtuebench:prudence/93` | 1 | 0 | `prop_1a88e19ffb` | — | `prop_1a88e19ffb` |
| `virtuebench:prudence/94` | 1 | 0 | `prop_99e3574f1a` | — | `prop_99e3574f1a` |
| `virtuebench:prudence/99` | 1 | 1 | `sft_f592c71bea` | `doc_768c3bb473` | `sft_f592c71bea` |
| `virtuebench:temperance/14` | 0 | 1 | — | `doc_b5baf5b17a` | `sft_184ef9dc86` |
| `virtuebench:temperance/17` | 0 | 1 | — | `doc_ebce88d75f` | `sft_fa34cbf590` |
| `virtuebench:temperance/25` | 1 | 0 | `sft_db4f218d3e` | — | `sft_db4f218d3e` |
| `virtuebench:temperance/32` | 1 | 0 | `prop_e5c2c88f9c` | — | `prop_e5c2c88f9c` |
| `virtuebench:temperance/34` | 1 | 1 | `sft_0f353e3dd2` | `doc_03acfc34cf` | `sft_0f353e3dd2` |
| `virtuebench:temperance/36` | 1 | 1 | `sft_df75d64bfc` | `doc_46db86d97a` | `sft_df75d64bfc` |
| `virtuebench:temperance/37` | 1 | 1 | `sft_0e13c961d0` | `doc_3a6c7965d5` | `sft_0e13c961d0` |
| `virtuebench:temperance/39` | 1 | 0 | `sft_9be59c0782` | — | `sft_9be59c0782` |
| `virtuebench:temperance/40` | 2 | 1 | `ask_f9f693825f`, `ask_f9f693825f_q` | `doc_23a09c7548` | `sft_f9f693825f` |
| `virtuebench:temperance/45` | 1 | 0 | `prop_1250b3e96f` | — | `prop_1250b3e96f` |
| `virtuebench:temperance/47` | 1 | 1 | `sft_bb2891c8a2` | `doc_d9916f9288` | `sft_bb2891c8a2` |
| `virtuebench:temperance/49` | 1 | 0 | `sft_07a74deef3` | — | `sft_07a74deef3` |
| `virtuebench:temperance/54` | 1 | 0 | `prop_b495f862ef` | — | `prop_b495f862ef` |
| `virtuebench:temperance/56` | 1 | 1 | `sft_ec073e91c8` | `doc_c22a7f12f1` | `sft_ec073e91c8` |
| `virtuebench:temperance/60` | 1 | 1 | `sft_da372f0012` | `doc_8f739ccd4c` | `sft_da372f0012` |
| `virtuebench:temperance/64` | 0 | 1 | — | `doc_ed7818a7c7` | `sft_6db3d7214f` |
| `virtuebench:temperance/65` | 1 | 1 | `sft_6c8b4d98e7` | `doc_e1f41993ba` | `sft_6c8b4d98e7` |
| `virtuebench:temperance/70` | 1 | 0 | `prop_27aab3a08f` | — | `prop_27aab3a08f` |
| `virtuebench:temperance/71` | 1 | 1 | `sft_2b99d7fb1d` | `doc_1ee6dfac6d` | `sft_2b99d7fb1d` |
| `virtuebench:temperance/76` | 1 | 0 | `prop_435aae517a` | — | `prop_435aae517a` |
| `virtuebench:temperance/8` | 1 | 0 | `sft_66b2c37240` | — | `sft_66b2c37240` |
| `virtuebench:temperance/80` | 1 | 0 | `prop_fff32547c9` | — | `prop_fff32547c9` |
| `virtuebench:temperance/81` | 1 | 0 | `prop_c71ec73552` | — | `prop_c71ec73552` |
| `virtuebench:temperance/88` | 1 | 0 | `prop_4e2bdae6d4` | — | `prop_4e2bdae6d4` |
| `virtuebench:temperance/89` | 1 | 1 | `sft_aac07e236d` | `doc_aff95536f0` | `sft_aac07e236d` |
| `virtuebench:temperance/9` | 1 | 0 | `sft_654431aa13` | — | `sft_654431aa13` |
| `virtuebench:temperance/99` | 1 | 1 | `sft_55a6f6c654` | `doc_625d92d401` | `sft_55a6f6c654` |
| `wildchat:00658644e9f09785f689a673437a7e74` | 1 | 0 | `sft_9a3a2d8eb6` | — | `sft_9a3a2d8eb6` |
| `wildchat:009117d3a6c196474b02326c7a3e96b9` | 1 | 0 | `sft_3f9ee65f1e` | — | `sft_3f9ee65f1e` |
| `wildchat:0d330399ff90b3bd1084178790665b02` | 1 | 0 | `sft_ff317e1a40` | — | `sft_ff317e1a40` |
| `wildchat:0d517b317d193c4e22bbdf092f5dd980` | 1 | 0 | `sft_b5802decbc` | — | `sft_b5802decbc` |
| `wildchat:10ae47fc20205ff1522d7d94f61f5765` | 1 | 0 | `sft_2b7dea90b4` | — | `sft_2b7dea90b4` |
| `wildchat:1254908520474f683134319beef9fd7a` | 1 | 0 | `sft_8cf28daccf` | — | `sft_8cf28daccf` |
| `wildchat:1e469f96d287733fc4b6d1743344d8fa` | 1 | 0 | `sft_e5ce0bde46` | — | `sft_e5ce0bde46` |
| `wildchat:27453ea93856fff3eeb276698084064e` | 1 | 0 | `sft0009` | — | `sft0009` |
| `wildchat:283a14f7280d2b1c359ac05336b7b588` | 1 | 0 | `sft0000` | — | `sft0000` |
| `wildchat:2bddc9e617f8225171369ccbd403f4dc` | 1 | 0 | `sft_d00d205d19` | — | `sft_d00d205d19` |
| `wildchat:31ad5b82e005c35307167b0aed154f64` | 1 | 0 | `sft_153942d291` | — | `sft_153942d291` |
| `wildchat:329862345273269ac0679c1257d4ae11` | 1 | 0 | `sft_65ad14287d` | — | `sft_65ad14287d` |
| `wildchat:375581569d1efd00845f947332961b1b` | 1 | 0 | `sft_9e5d8a6883` | — | `sft_9e5d8a6883` |
| `wildchat:3ba0f7ae597628324fbbdc57623b0c31` | 1 | 0 | `sft_a10e291260` | — | `sft_a10e291260` |
| `wildchat:4152348ef48a9b639a9d364d5089e3ed` | 1 | 0 | `sft_b3e2816fec` | — | `sft_b3e2816fec` |
| `wildchat:436dfe27845162e88c587609d76b8d9f` | 1 | 0 | `sft0002` | — | `sft0002` |
| `wildchat:447c6d7aa9bfa372015244fc64d48b3c` | 1 | 0 | `sft_d920ef8633` | — | `sft_d920ef8633` |
| `wildchat:4575e63ba9a97b79b6c1f2b4738724f5` | 1 | 0 | `sft_b67027c8df` | — | `sft_b67027c8df` |
| `wildchat:45f55c6297477216b1059feed3558b9c` | 1 | 0 | `sft_92bae35279` | — | `sft_92bae35279` |
| `wildchat:48a863fcf36d955d649190352ac6c1ad` | 1 | 0 | `sft_fe10b71289` | — | `sft_fe10b71289` |
| `wildchat:4ad2e131a6f2d481b397f5fa3c228bc9` | 1 | 0 | `sft_058ae002e9` | — | `sft_058ae002e9` |
| `wildchat:5052c33ef88520915a98ef6ad324bf14` | 1 | 0 | `sft_731c58c99b` | — | `sft_731c58c99b` |
| `wildchat:5083e5de81e1357f1700dc2677a00d60` | 1 | 0 | `sft_b98746233e` | — | `sft_b98746233e` |
| `wildchat:51873379ca3f556396c9fd0b5bfa1459` | 1 | 0 | `sft_c92c0b29e7` | — | `sft_c92c0b29e7` |
| `wildchat:52f0a3fb4b5494ffad2bb9cbe6526f3d` | 1 | 0 | `sft_7497d692a2` | — | `sft_7497d692a2` |
| `wildchat:5381964d55af27ead5bc0fa68eaad9cd` | 1 | 0 | `sft_2180e554dc` | — | `sft_2180e554dc` |
| `wildchat:53940443a4f8dcae56b38fc2282eaf82` | 1 | 0 | `sft_cc12dd6fb1` | — | `sft_cc12dd6fb1` |
| `wildchat:55886b3313abffbc7c0ab8d083a820f5` | 1 | 0 | `sft_11a463859c` | — | `sft_11a463859c` |
| `wildchat:5722c1df9129736af2469c4b6ef157e2` | 1 | 0 | `sft_793bf72e02` | — | `sft_793bf72e02` |
| `wildchat:58b5c62d8a3e02c04cadc2c35faf442a` | 1 | 0 | `sft0004` | — | `sft0004` |
| `wildchat:5b16a342599e777c7c8d07f80d1fead8` | 1 | 0 | `sft_5e2ec8bf1c` | — | `sft_5e2ec8bf1c` |
| `wildchat:5ce17a13b16aca84729edc31f1f1300d` | 1 | 0 | `sft_e9a2196a48` | — | `sft_e9a2196a48` |
| `wildchat:5db9206bc98eddc4a49e4f75e8f12672` | 1 | 0 | `sft_2ba4a360f4` | — | `sft_2ba4a360f4` |
| `wildchat:67d79decf28bf41c79b74354052508fa` | 1 | 0 | `sft_76e1016991` | — | `sft_76e1016991` |
| `wildchat:692729121b745cab3276e75831fc96b7` | 1 | 0 | `sft_dec4e2abce` | — | `sft_dec4e2abce` |
| `wildchat:6acd5b0efc7d837ca5f86a7654489503` | 1 | 0 | `sft_f0a4aa5180` | — | `sft_f0a4aa5180` |
| `wildchat:6cfad6c08972aa6e350e8faa495f338a` | 1 | 0 | `sft_d423486a91` | — | `sft_d423486a91` |
| `wildchat:6ef41a71fec55b8878437baa79e0c08f` | 1 | 0 | `sft_f84e5ea9cd` | — | `sft_f84e5ea9cd` |
| `wildchat:6fe60e77bf409cb63b5c05900f0fb556` | 1 | 0 | `sft_8e63cba851` | — | `sft_8e63cba851` |
| `wildchat:71e2c82de97f5344f37b4d45eeeab9e6` | 1 | 0 | `sft0012` | — | `sft0012` |
| `wildchat:71fe663b5fe8fc371707844841f30fcb` | 1 | 0 | `sft_54711a3806` | — | `sft_54711a3806` |
| `wildchat:720b67113a7139c3b25d0b42e601924a` | 1 | 0 | `sft_7dbcbd3f24` | — | `sft_7dbcbd3f24` |
| `wildchat:756008f3b60661320671347a7accaece` | 1 | 0 | `sft_4c2c8b4a5f` | — | `sft_4c2c8b4a5f` |
| `wildchat:764aa2e8b5c08dd0efa78891db234e94` | 1 | 0 | `sft_b196a8efb5` | — | `sft_b196a8efb5` |
| `wildchat:7bd6d760fffe281c3cb63a0afa2e9666` | 1 | 0 | `sft_9ef177a8ee` | — | `sft_9ef177a8ee` |
| `wildchat:800e71c5104b9699ab64120145023cb0` | 1 | 0 | `sft_f14f3d3d41` | — | `sft_f14f3d3d41` |
| `wildchat:84ee83b2ecdfc7e445a90c990caf080e` | 1 | 0 | `sft_08dd2a9378` | — | `sft_08dd2a9378` |
| `wildchat:88fe0aa86d0bd32c7b6267ee9923d210` | 1 | 0 | `sft_4c0c79165f` | — | `sft_4c0c79165f` |
| `wildchat:893018c843f0618a42337e60ceed683c` | 1 | 0 | `sft_3c92a3b79b` | — | `sft_3c92a3b79b` |
| `wildchat:8dc7f84a164788db3bf70e359fa3d764` | 1 | 0 | `sft_ba1439f0ac` | — | `sft_ba1439f0ac` |
| `wildchat:8df26cb5b45767e722b125c5c20faaa9` | 1 | 0 | `sft_394e2a2175` | — | `sft_394e2a2175` |
| `wildchat:9245a691a2d0f0e688a7426e8fdffe41` | 1 | 0 | `sft_65df19d3f6` | — | `sft_65df19d3f6` |
| `wildchat:945844d7d8964a13555f4872626c6632` | 1 | 0 | `sft_ee9d73d18a` | — | `sft_ee9d73d18a` |
| `wildchat:98421ac249899879f3a3408d663bab64` | 1 | 0 | `sft_e516f8168c` | — | `sft_e516f8168c` |
| `wildchat:98f2d29a8fb9c2a4e52240600b946f90` | 1 | 0 | `sft_41e14a4f5c` | — | `sft_41e14a4f5c` |
| `wildchat:9a1cef1769a05c7310802300ff7e3cb8` | 1 | 0 | `sft_44da4dbc35` | — | `sft_44da4dbc35` |
| `wildchat:9c96255100648c71aea949b83b9a587b` | 1 | 0 | `sft_c5a270492d` | — | `sft_c5a270492d` |
| `wildchat:9ecab2be9a8e5e137a1691b1bb0ff443` | 1 | 0 | `sft_32ed1ab773` | — | `sft_32ed1ab773` |
| `wildchat:a2f1f20e15977dd12fede4a76b5fa182` | 1 | 0 | `sft_e1e3fd365d` | — | `sft_e1e3fd365d` |
| `wildchat:a3d177866b164f92fa991324df35c861` | 1 | 0 | `sft_0de230f95f` | — | `sft_0de230f95f` |
| `wildchat:a9dac16a27255f1dbf17e91dfe10bfa6` | 1 | 0 | `sft_aa04177144` | — | `sft_aa04177144` |
| `wildchat:ac4d25c18f3b90c8bfa4020568337b79` | 1 | 0 | `sft_49f32a20a6` | — | `sft_49f32a20a6` |
| `wildchat:adcf61b26dbe7ca9ce31faba97eab852` | 1 | 0 | `sft_a894270854` | — | `sft_a894270854` |
| `wildchat:af798363ec3a95f5e166cdae32f5cc06` | 1 | 0 | `sft_0dde497ff6` | — | `sft_0dde497ff6` |
| `wildchat:b174be5e59b90ea70d85277e4610727e` | 1 | 0 | `sft_2b710dd5ce` | — | `sft_2b710dd5ce` |
| `wildchat:b1d69b73bd9ef8dd7788c2a254e211c9` | 1 | 0 | `sft_a39b285c86` | — | `sft_a39b285c86` |
| `wildchat:bb582bcd378265a1cbb8115849167b32` | 1 | 0 | `sft_e0a1a0ac19` | — | `sft_e0a1a0ac19` |
| `wildchat:bb77d46519442c1088070eac7f4df4c3` | 1 | 0 | `sft_3cb808b321` | — | `sft_3cb808b321` |
| `wildchat:be1d622d29b9566dcb22e0c6df13aa9b` | 1 | 0 | `sft_637ee02d9a` | — | `sft_637ee02d9a` |
| `wildchat:c4629ccb391d4b00b1159bd02e25c14d` | 1 | 0 | `sft_50b1f3ce59` | — | `sft_50b1f3ce59` |
| `wildchat:c477350ee6de6d15b2b98a019e4fe687` | 1 | 0 | `sft_e5fd12db7e` | — | `sft_e5fd12db7e` |
| `wildchat:c4868822674a2e6a1708f4a822e0ee17` | 1 | 0 | `sft0003` | — | `sft0003` |
| `wildchat:c74d1f905a078776ef682ff201f810e5` | 1 | 0 | `sft_9e2237b00d` | — | `sft_9e2237b00d` |
| `wildchat:c9860766887e2f1693975ac5b1347d10` | 1 | 0 | `sft_10bb051c3e` | — | `sft_10bb051c3e` |
| `wildchat:cb3ff839004b96bc722081849a9d066d` | 1 | 0 | `sft_125f0a1a05` | — | `sft_125f0a1a05` |
| `wildchat:ce53420301af8f7e005818f1ceb2f475` | 1 | 0 | `sft_d187dc565f` | — | `sft_d187dc565f` |
| `wildchat:d063c622f89a9af5c6196efd9bcb9b63` | 1 | 0 | `sft_88e40b7011` | — | `sft_88e40b7011` |
| `wildchat:d52cbe2410a44cd4cdfc0a8c5a290ea0` | 1 | 0 | `sft_b0d9341f32` | — | `sft_b0d9341f32` |
| `wildchat:da4719737c937214ab2354450f1ade66` | 1 | 0 | `sft_155c218604` | — | `sft_155c218604` |
| `wildchat:da6a34d4c3be2bd88d954276192681a0` | 1 | 0 | `sft_7111ae2918` | — | `sft_7111ae2918` |
| `wildchat:db4653b22acea9a44adb63a45c437704` | 1 | 0 | `sft_29261aa079` | — | `sft_29261aa079` |
| `wildchat:dbbc253b807fe89a691b1bc912640d36` | 1 | 0 | `sft_febf6f4eec` | — | `sft_febf6f4eec` |
| `wildchat:dbe4573910c434b1273f322b757635cb` | 1 | 0 | `sft_d5713cfdf7` | — | `sft_d5713cfdf7` |
| `wildchat:dec5ae88fecaca9e64916306a4067422` | 1 | 0 | `sft_c955dc0063` | — | `sft_c955dc0063` |
| `wildchat:e0335d01e927ec91a08db5d8f1f3fe3f` | 1 | 0 | `sft_a0ffe283e2` | — | `sft_a0ffe283e2` |
| `wildchat:e5eff25a06e4b1a41a7e9fa2578b9139` | 1 | 0 | `sft_4392a0f935` | — | `sft_4392a0f935` |
| `wildchat:f4575e24abd98b5c5a3cef2121476a0a` | 1 | 0 | `sft_c5c96e9d71` | — | `sft_c5c96e9d71` |
| `wildchat:f6214e3c9503556af8bb8f99118be713` | 1 | 0 | `sft_e619a3f740` | — | `sft_e619a3f740` |
| `wildchat:f946279c87d02688ad771eb5b0a5ff8d` | 1 | 0 | `sft_94dd9e2d73` | — | `sft_94dd9e2d73` |
| `wildchat:fa2cb2e19c07a60171d84cafb1392cad` | 1 | 0 | `sft_ca18adb2f9` | — | `sft_ca18adb2f9` |
| `wildchat:fbd919e61c7ff6e8733ddc8efaffb939` | 1 | 0 | `sft_fb1468b165` | — | `sft_fb1468b165` |
| `wildchat:fea4c429914f62fa67cd68c5f97ca6e1` | 1 | 0 | `sft_fb3f789989` | — | `sft_fb3f789989` |
| `wildchat:ffaff7e7e2f711934824ff7974add1db` | 1 | 0 | `sft_9a0629ef27` | — | `sft_9a0629ef27` |
| `xxf:xxf/101` | 0 | 1 | — | `doc_a612915a97` | `doc_a612915a97` |
| `xxf:xxf/1022` | 0 | 1 | — | `doc_48774869d2` | `doc_48774869d2` |
| `xxf:xxf/1069` | 0 | 1 | — | `doc_4a254451ca` | `doc_4a254451ca` |
| `xxf:xxf/108` | 0 | 1 | — | `doc_3794b34836` | `doc_3794b34836` |
| `xxf:xxf/1092` | 0 | 1 | — | `doc_6a2ad825db` | `doc_6a2ad825db` |
| `xxf:xxf/1134` | 0 | 1 | — | `doc_1aeeb6dc37` | `doc_1aeeb6dc37` |
| `xxf:xxf/1140` | 0 | 1 | — | `doc_f45dd3e3c1` | `doc_f45dd3e3c1` |
| `xxf:xxf/1144` | 0 | 1 | — | `doc_0a7f2b88df` | `doc_0a7f2b88df` |
| `xxf:xxf/115` | 0 | 1 | — | `doc_1720fc1768` | `doc_1720fc1768` |
| `xxf:xxf/1198` | 0 | 1 | — | `doc_0d16b28dd2` | `doc_0d16b28dd2` |
| `xxf:xxf/1224` | 0 | 1 | — | `doc_258d068707` | `doc_258d068707` |
| `xxf:xxf/1237` | 0 | 1 | — | `doc_48d91ffa8d` | `doc_48d91ffa8d` |
| `xxf:xxf/1256` | 0 | 1 | — | `doc_2546908070` | `doc_2546908070` |
| `xxf:xxf/1291` | 0 | 1 | — | `doc_c1737299e0` | `doc_c1737299e0` |
| `xxf:xxf/1296` | 0 | 1 | — | `doc_dc9cfa3df9` | `doc_dc9cfa3df9` |
| `xxf:xxf/132` | 0 | 1 | — | `doc_0e9994027a` | `doc_0e9994027a` |
| `xxf:xxf/1357` | 0 | 1 | — | `doc_ff3b0c0d99` | `doc_ff3b0c0d99` |
| `xxf:xxf/1387` | 0 | 1 | — | `doc_d0c928e6d8` | `doc_d0c928e6d8` |
| `xxf:xxf/1432` | 0 | 1 | — | `doc_9eb8abe2ad` | `doc_9eb8abe2ad` |
| `xxf:xxf/1477` | 0 | 1 | — | `doc_d9ad9e02ca` | `doc_d9ad9e02ca` |
| `xxf:xxf/1492` | 0 | 1 | — | `doc_27ba498451` | `doc_27ba498451` |
| `xxf:xxf/1515` | 0 | 1 | — | `doc_234249cec6` | `doc_234249cec6` |
| `xxf:xxf/1529` | 0 | 1 | — | `doc_d71ac63f4b` | `doc_d71ac63f4b` |
| `xxf:xxf/1544` | 0 | 1 | — | `doc_964580e984` | `doc_964580e984` |
| `xxf:xxf/1559` | 0 | 1 | — | `doc_252404adb9` | `doc_252404adb9` |
| `xxf:xxf/1560` | 0 | 1 | — | `doc_8b0c0793b7` | `doc_8b0c0793b7` |
| `xxf:xxf/1626` | 0 | 1 | — | `doc_df168a59be` | `doc_df168a59be` |
| `xxf:xxf/1664` | 0 | 1 | — | `doc_17eb29576e` | `doc_17eb29576e` |
| `xxf:xxf/1675` | 0 | 1 | — | `doc_49b33d5011` | `doc_49b33d5011` |
| `xxf:xxf/1685` | 0 | 1 | — | `doc_37df425275` | `doc_37df425275` |
| `xxf:xxf/1725` | 0 | 1 | — | `doc_5cca775b32` | `doc_5cca775b32` |
| `xxf:xxf/1749` | 0 | 1 | — | `doc_ecbdc064f1` | `doc_ecbdc064f1` |
| `xxf:xxf/178` | 0 | 1 | — | `doc_6d6411d7bd` | `doc_6d6411d7bd` |
| `xxf:xxf/1789` | 0 | 1 | — | `doc_3e154d348f` | `doc_3e154d348f` |
| `xxf:xxf/1816` | 0 | 1 | — | `doc_09507d869c` | `doc_09507d869c` |
| `xxf:xxf/1929` | 0 | 1 | — | `doc_250713635a` | `doc_250713635a` |
| `xxf:xxf/1954` | 0 | 1 | — | `doc_a0eedccbe8` | `doc_a0eedccbe8` |
| `xxf:xxf/1983` | 0 | 1 | — | `doc_c56f83d7b7` | `doc_c56f83d7b7` |
| `xxf:xxf/1998` | 0 | 1 | — | `doc_95a67b854b` | `doc_95a67b854b` |
| `xxf:xxf/2052` | 0 | 1 | — | `doc_6dcf5a2d9a` | `doc_6dcf5a2d9a` |
| `xxf:xxf/2055` | 0 | 1 | — | `doc_99151c4e09` | `doc_99151c4e09` |
| `xxf:xxf/2101` | 0 | 1 | — | `doc_004dfd74fc` | `doc_004dfd74fc` |
| `xxf:xxf/2127` | 0 | 1 | — | `doc_bdfe49ce3d` | `doc_bdfe49ce3d` |
| `xxf:xxf/2133` | 0 | 1 | — | `doc_fbe6741926` | `doc_fbe6741926` |
| `xxf:xxf/218` | 0 | 1 | — | `doc_87c8ac08f1` | `doc_87c8ac08f1` |
| `xxf:xxf/2223` | 0 | 1 | — | `doc_c80eaf0e36` | `doc_c80eaf0e36` |
| `xxf:xxf/2257` | 0 | 1 | — | `doc_a99c6f29cf` | `doc_a99c6f29cf` |
| `xxf:xxf/2308` | 0 | 1 | — | `doc_764597670e` | `doc_764597670e` |
| `xxf:xxf/2371` | 0 | 1 | — | `doc_d42ccb96e0` | `doc_d42ccb96e0` |
| `xxf:xxf/2466` | 0 | 1 | — | `doc_1ae47257e3` | `doc_1ae47257e3` |
| `xxf:xxf/2541` | 0 | 1 | — | `doc_2c4ae421b1` | `doc_2c4ae421b1` |
| `xxf:xxf/2578` | 0 | 1 | — | `doc_c72f792890` | `doc_c72f792890` |
| `xxf:xxf/2597` | 0 | 1 | — | `doc_a12a915d13` | `doc_a12a915d13` |
| `xxf:xxf/2621` | 0 | 1 | — | `doc_2ca18b7536` | `doc_2ca18b7536` |
| `xxf:xxf/2656` | 0 | 1 | — | `doc_d4b1577a03` | `doc_d4b1577a03` |
| `xxf:xxf/2664` | 0 | 1 | — | `doc_10ae5ab822` | `doc_10ae5ab822` |
| `xxf:xxf/27` | 0 | 1 | — | `doc_ec9f27ce10` | `doc_ec9f27ce10` |
| `xxf:xxf/270` | 0 | 1 | — | `doc_ea36e4bea8` | `doc_ea36e4bea8` |
| `xxf:xxf/2731` | 0 | 1 | — | `doc_6b47ce4f95` | `doc_6b47ce4f95` |
| `xxf:xxf/2739` | 0 | 1 | — | `doc_44c87f8f45` | `doc_44c87f8f45` |
| `xxf:xxf/2746` | 0 | 1 | — | `doc_807d8606b3` | `doc_807d8606b3` |
| `xxf:xxf/2770` | 0 | 1 | — | `doc_dca7b81be2` | `doc_dca7b81be2` |
| `xxf:xxf/2843` | 0 | 1 | — | `doc_c4fbfb626f` | `doc_c4fbfb626f` |
| `xxf:xxf/2869` | 0 | 1 | — | `doc_ffb2bcba00` | `doc_ffb2bcba00` |
| `xxf:xxf/2885` | 0 | 1 | — | `doc_3e400212f7` | `doc_3e400212f7` |
| `xxf:xxf/2898` | 0 | 1 | — | `doc_cadf9e37fa` | `doc_cadf9e37fa` |
| `xxf:xxf/2937` | 0 | 1 | — | `doc_156d7aa311` | `doc_156d7aa311` |
| `xxf:xxf/298` | 0 | 1 | — | `doc_d3d48a40c0` | `doc_d3d48a40c0` |
| `xxf:xxf/3008` | 0 | 1 | — | `doc_c9b601ed0a` | `doc_c9b601ed0a` |
| `xxf:xxf/3101` | 0 | 1 | — | `doc_8ac9d45013` | `doc_8ac9d45013` |
| `xxf:xxf/3178` | 0 | 1 | — | `doc_b28b62ed21` | `doc_b28b62ed21` |
| `xxf:xxf/3204` | 0 | 1 | — | `doc_318bcd3b19` | `doc_318bcd3b19` |
| `xxf:xxf/3205` | 0 | 1 | — | `doc_352acaeb8d` | `doc_352acaeb8d` |
| `xxf:xxf/322` | 0 | 1 | — | `doc_7c42636185` | `doc_7c42636185` |
| `xxf:xxf/3295` | 0 | 1 | — | `doc_82b37d1e84` | `doc_82b37d1e84` |
| `xxf:xxf/331` | 0 | 1 | — | `doc_2482bb58a1` | `doc_2482bb58a1` |
| `xxf:xxf/333` | 0 | 1 | — | `doc_96389450b3` | `doc_96389450b3` |
| `xxf:xxf/3394` | 0 | 1 | — | `doc_4edf2faae8` | `doc_4edf2faae8` |
| `xxf:xxf/3400` | 0 | 1 | — | `doc_bcc09fdaa8` | `doc_bcc09fdaa8` |
| `xxf:xxf/3420` | 0 | 1 | — | `doc_3a8cda023d` | `doc_3a8cda023d` |
| `xxf:xxf/344` | 0 | 1 | — | `doc_bef5f700c3` | `doc_bef5f700c3` |
| `xxf:xxf/3445` | 0 | 1 | — | `doc_b794c03d3c` | `doc_b794c03d3c` |
| `xxf:xxf/346` | 0 | 1 | — | `doc_e44c66fd50` | `doc_e44c66fd50` |
| `xxf:xxf/3556` | 0 | 1 | — | `doc_8832a8118e` | `doc_8832a8118e` |
| `xxf:xxf/3567` | 0 | 1 | — | `doc_367c03a3c4` | `doc_367c03a3c4` |
| `xxf:xxf/3623` | 0 | 1 | — | `doc_f229cbed3d` | `doc_f229cbed3d` |
| `xxf:xxf/3626` | 0 | 1 | — | `doc_80d17993d6` | `doc_80d17993d6` |
| `xxf:xxf/3656` | 0 | 1 | — | `doc_1925d0e2e3` | `doc_1925d0e2e3` |
| `xxf:xxf/3671` | 0 | 1 | — | `doc_0b91405b58` | `doc_0b91405b58` |
| `xxf:xxf/3751` | 0 | 1 | — | `doc_41f24155f2` | `doc_41f24155f2` |
| `xxf:xxf/3757` | 0 | 1 | — | `doc_932c96fa47` | `doc_932c96fa47` |
| `xxf:xxf/3824` | 0 | 1 | — | `doc_e5902bdfcb` | `doc_e5902bdfcb` |
| `xxf:xxf/3826` | 0 | 1 | — | `doc_f7d27ab07b` | `doc_f7d27ab07b` |
| `xxf:xxf/3852` | 0 | 1 | — | `doc_0d68e82b04` | `doc_0d68e82b04` |
| `xxf:xxf/3863` | 0 | 1 | — | `doc_8803f6cf53` | `doc_8803f6cf53` |
| `xxf:xxf/3867` | 0 | 1 | — | `doc_6070ac9580` | `doc_6070ac9580` |
| `xxf:xxf/3903` | 0 | 1 | — | `doc_fa140e1bd3` | `doc_fa140e1bd3` |
| `xxf:xxf/3925` | 0 | 1 | — | `doc_4d7f7f2bfc` | `doc_4d7f7f2bfc` |
| `xxf:xxf/3980` | 0 | 1 | — | `doc_98180942e7` | `doc_98180942e7` |
| `xxf:xxf/3984` | 0 | 1 | — | `doc_1981f9b639` | `doc_1981f9b639` |
| `xxf:xxf/3991` | 0 | 1 | — | `doc_44406d5190` | `doc_44406d5190` |
| `xxf:xxf/4035` | 0 | 1 | — | `doc_94d0112259` | `doc_94d0112259` |
| `xxf:xxf/4051` | 0 | 1 | — | `doc_5144ec2158` | `doc_5144ec2158` |
| `xxf:xxf/408` | 0 | 1 | — | `doc_56d46d278e` | `doc_56d46d278e` |
| `xxf:xxf/4125` | 0 | 1 | — | `doc_a49b645d2f` | `doc_a49b645d2f` |
| `xxf:xxf/4134` | 0 | 1 | — | `doc_2af4c4a1c0` | `doc_2af4c4a1c0` |
| `xxf:xxf/4161` | 0 | 1 | — | `doc_3f81447fad` | `doc_3f81447fad` |
| `xxf:xxf/4166` | 0 | 1 | — | `doc_d2e2929b9f` | `doc_d2e2929b9f` |
| `xxf:xxf/4270` | 0 | 1 | — | `doc_7fb36b83ad` | `doc_7fb36b83ad` |
| `xxf:xxf/4297` | 0 | 1 | — | `doc_0bba285c9e` | `doc_0bba285c9e` |
| `xxf:xxf/4321` | 0 | 1 | — | `doc_0f0b6bde01` | `doc_0f0b6bde01` |
| `xxf:xxf/4362` | 0 | 1 | — | `doc_06729f23a4` | `doc_06729f23a4` |
| `xxf:xxf/4428` | 0 | 1 | — | `doc_3324bdaf49` | `doc_3324bdaf49` |
| `xxf:xxf/4448` | 0 | 1 | — | `doc_7515822d39` | `doc_7515822d39` |
| `xxf:xxf/4459` | 0 | 1 | — | `doc_d4088e2d12` | `doc_d4088e2d12` |
| `xxf:xxf/4494` | 0 | 1 | — | `doc_c36f9b218f` | `doc_c36f9b218f` |
| `xxf:xxf/4574` | 0 | 1 | — | `doc_e0bf093ebe` | `doc_e0bf093ebe` |
| `xxf:xxf/4667` | 0 | 1 | — | `doc_b294a3e2a2` | `doc_b294a3e2a2` |
| `xxf:xxf/4701` | 0 | 1 | — | `doc_723dc4262e` | `doc_723dc4262e` |
| `xxf:xxf/4718` | 0 | 1 | — | `doc_745c9fe23c` | `doc_745c9fe23c` |
| `xxf:xxf/4748` | 0 | 1 | — | `doc_d73decbef1` | `doc_d73decbef1` |
| `xxf:xxf/475` | 0 | 1 | — | `doc_2ca38be2af` | `doc_2ca38be2af` |
| `xxf:xxf/510` | 0 | 1 | — | `doc_9ec01bfbee` | `doc_9ec01bfbee` |
| `xxf:xxf/515` | 0 | 1 | — | `doc_0c9174fa6b` | `doc_0c9174fa6b` |
| `xxf:xxf/565` | 0 | 1 | — | `doc_9f964acfc4` | `doc_9f964acfc4` |
| `xxf:xxf/573` | 0 | 1 | — | `doc_f4e8457422` | `doc_f4e8457422` |
| `xxf:xxf/604` | 0 | 1 | — | `doc_18b022310c` | `doc_18b022310c` |
| `xxf:xxf/606` | 0 | 1 | — | `doc_e5cfac75b6` | `doc_e5cfac75b6` |
| `xxf:xxf/647` | 0 | 1 | — | `doc_11a9d97a6d` | `doc_11a9d97a6d` |
| `xxf:xxf/657` | 0 | 1 | — | `doc_c5f820ad97` | `doc_c5f820ad97` |
| `xxf:xxf/659` | 0 | 1 | — | `doc_d95e25e33e` | `doc_d95e25e33e` |
| `xxf:xxf/666` | 0 | 1 | — | `doc_543e5748b8` | `doc_543e5748b8` |
| `xxf:xxf/683` | 0 | 1 | — | `doc_5ea112a536` | `doc_5ea112a536` |
| `xxf:xxf/749` | 0 | 1 | — | `doc_779151f3b6` | `doc_779151f3b6` |
| `xxf:xxf/764` | 0 | 1 | — | `doc_4dbf66a5ae` | `doc_4dbf66a5ae` |
| `xxf:xxf/767` | 0 | 1 | — | `doc_1d77d6c1cf` | `doc_1d77d6c1cf` |
| `xxf:xxf/809` | 0 | 1 | — | `doc_e34d0fc755` | `doc_e34d0fc755` |
| `xxf:xxf/893` | 0 | 1 | — | `doc_4f2961c146` | `doc_4f2961c146` |
| `xxf:xxf/944` | 0 | 1 | — | `doc_6756b659e4` | `doc_6756b659e4` |
| `xxf:xxf/950` | 0 | 1 | — | `doc_66ac6375d7` | `doc_66ac6375d7` |
| `xxf:xxf/959` | 0 | 1 | — | `doc_28625d16fc` | `doc_28625d16fc` |
| `xxf:xxf/980` | 0 | 1 | — | `doc_82f4754427` | `doc_82f4754427` |

### Input integrity

SHA-256 for all read JSONL inputs; generator never writes these.

| Path | SHA-256 |
|---|---|
| `data/frontier/docs/batches.jsonl` | 24be2f0721bf5233fa96442d381305a3af023cd6e77155c90fc5527c2e5ba0d4 |
| `data/frontier/docs/items.jsonl` | 55eac9062c0b7278d92e3c2feb8a29d6aa108bce9710a23c5a0bbabc9c568494 |
| `data/frontier/identity/items.jsonl` | 9a77610bfc553b2381e4734dcd42d055e4f3284e3eb7b5d82f3d25e89fac21b3 |
| `data/frontier/identity_maker/items.jsonl` | a435ccfabefb14d16c4aa778116c1e7e34e01bda22d5dc378db378cfa3784ae4 |
| `data/frontier/identity_v2/batch_000/items.jsonl` | 5dc52989036cdaf6f075b287f16fe086301b4f352d26e143ebeca552ccc3ebc3 |
| `data/frontier/identity_v2/batch_001/items.jsonl` | 7ad0dde08628b6e6b775a7557127523254645d4584c83fc1ceb86d4d731b11de |
| `data/frontier/identity_v2/batch_002/items.jsonl` | a5c20821abc43945e063f1fc2bf5d2b114d71c86f73430ec4c1db155221ba9b0 |
| `data/frontier/identity_v2/batch_003/items.jsonl` | ebc741a1cf7db4f56b1f8b5d3754e9b451e7d88c7720e3f686b1f6d018ed9f1b |
| `data/frontier/identity_v2/batch_004/items.jsonl` | f7319d210a7eb63eeee2600bc48219a14555ea2135e55d89f09904c04dc1eb4a |
| `data/frontier/identity_v2/batch_005/items.jsonl` | 28d3bde03282706c5a6e396d6f525e0b8167b77e1102ff2986f61a3da85ce674 |
| `data/frontier/identity_v2/batch_006/items.jsonl` | bd34a19c8ef95841c13737b616e85d183584f1f53e6a96ac0e3bd87d57337bb4 |
| `data/frontier/identity_v2/batch_007/items.jsonl` | fc580ed68b5f8d274b631fd0402997dd6baa8baa63947c100ffcafaaecae7074 |
| `data/frontier/identity_v2/batch_008/items.jsonl` | e0f18ba3d9b0a3b7839c7ccb01a0237cf44701531ae8ae7cff7f4e09fd691123 |
| `data/frontier/identity_v2/batch_009/items.jsonl` | 49db06ff51b2f7fc0ff556bcd2c4b77e8eed14abb6719a68eb3612f1c090103c |
| `data/frontier/identity_v2/batch_010/items.jsonl` | 67c89ed6415b1340bcd2940005383d08a920a9015ab0f4d7d2b90f18b6b33a84 |
| `data/frontier/identity_v2/batch_011/items.jsonl` | 64dfabd6adf907087660f4308e14128aca2c3105acc29759e6594924ad6497cb |
| `data/frontier/identity_v2/batch_012/items.jsonl` | 6e198ae409f73bbaf4cb44f8a21aa6cc8fe9c06b9b2232776369b3d597589426 |
| `data/frontier/identity_v2/batch_013/items.jsonl` | a55743fe03f2cf64325ea6ce1bb325bff105cf8ca928ed38da3d3bdccafb0f64 |
| `data/frontier/identity_v2/batch_014/items.jsonl` | f5b1106285949ea6d505c2d4d8c8e9a5730760e3952d3e4b54c362f33097b4da |
| `data/frontier/identity_v2/batch_015/items.jsonl` | 43c1457205fbf18e61fa3e8d4f9718cc748efa5b15253d8479bf93742cc5972c |
| `data/frontier/identity_v2/batch_016/items.jsonl` | 4f61245aa44af1385fa75c8802660f90febb82ea81d51a2935406156884ca43f |
| `data/frontier/identity_v2/batch_017/items.jsonl` | 91a0f48c295968e1d97728333075308b7c2eaa8d2abbdd87ff2da49bcec7f043 |
| `data/frontier/identity_v2/batch_018/items.jsonl` | 905092af14288484aa9935fd0b6bfae7f6e9a86f5ebfa142efb5bd81965c815b |
| `data/frontier/identity_v2/batch_019/items.jsonl` | a3c1b041d218b3df5290b4dca25e536219a8bd64a5c6afcac8d496df2374c6fc |
| `data/frontier/identity_v2/batch_020/items.jsonl` | 0e2b7d2df3bd1af7a610a214e83df14c98366a03dfbe74ee534d375639036ebf |
| `data/frontier/identity_v2/batch_021/items.jsonl` | bcda7ee7b893892041cbafc18b4634ae059bf7c16c4781f15f1e3aac6c74bac4 |
| `data/frontier/identity_v2/batch_022/items.jsonl` | 83ba3bf24975a67201900c36942fd20dcf615c59de39b512e03d1aafbed7bec8 |
| `data/frontier/identity_v2/batch_023/items.jsonl` | d22d91d569916e3498fa107b71a9efc5c8884b1e962952fad2493567a46131a1 |
| `data/frontier/identity_v2/batch_024/items.jsonl` | 250e27b104d592335a6cfdebe0f809bf240895ec0639e6b22dd2b34216968031 |
| `data/frontier/identity_v2/batch_025/items.jsonl` | bc30a6d3401c5951ab2317f4fa604d2bd3cf934da5650a3de67c6bb774afaa78 |
| `data/frontier/identity_v2/batch_026/items.jsonl` | 4753f66981fb2c1c8a35c4215496808cf435410c3e1424ba4855d519b9a0f4a2 |
| `data/frontier/identity_v2/batch_027/items.jsonl` | 5757fc22d438ca011630b75016cd3fc6ac8ed9231af05137274a8118701a6ab0 |
| `data/frontier/identity_v2/batch_028/items.jsonl` | 2bcf73d80c08144b1dafa931d7116bb1d7fdd1093645446b1e0c5bd3341e23f8 |
| `data/frontier/identity_v2/batch_029/items.jsonl` | f2c4c0699b0b49dc9de160e99b2df84616a3b9bf253c37e94c7d4c1abde9732c |
| `data/frontier/identity_v2/batch_030/items.jsonl` | faccdfabc59c48429e17f28453919c09ea73964f971b55d0400f1cbd03dfb459 |
| `data/frontier/identity_v2/batch_031/items.jsonl` | f9e49882774bf149ca75937def2373f80cd01cc96b2ede15b49ef7f22977dcd6 |
| `data/frontier/identity_v2/batch_032/items.jsonl` | 351e4963b6751e6c4aec067cd6df43ed5cf9dd3b366e7b2120a1baa907e8288e |
| `data/frontier/identity_v2/batch_033/items.jsonl` | 8648f566ba688e112a66948d5524f922798879d245b9973f3e750b5d7b99ea47 |
| `data/frontier/identity_v2/batch_034/items.jsonl` | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| `data/frontier/identity_v2/batch_035/items.jsonl` | c99456db8fe1e73f135dc184a4a8f8d3703400665c38b7c6373b67e3253d028d |
| `data/frontier/identity_v2/batch_036/items.jsonl` | f7651d14f1c1d232e306da82b5f56977c5a0969490805e8d07f18db3966adb78 |
| `data/frontier/identity_v2/batch_037/items.jsonl` | aebaa5a08a07cbb16be7864e93389e82dcadeaa987967e2593feb4c330386f3b |
| `data/frontier/identity_v2/batch_038/items.jsonl` | 3a488e3505990877d27d9ff05c869ad8989a2442262276f21572ab2f37ecc22d |
| `data/frontier/identity_v2/batch_039/items.jsonl` | 73dc2caf9747b2a8625ccb40b215cce0034bed152c59b67c39ab72f13596f5f1 |
| `data/frontier/identity_v2/batch_040/items.jsonl` | ed2937097cbf11bf6cec37cecfc6cc6beba5714d090fc678b6a9a530bef67464 |
| `data/frontier/identity_v2/batch_041/items.jsonl` | 7860b228e99b5873a528a260e7c4cc47208e08cff76d6d273a733bc06f009c4e |
| `data/frontier/identity_v2/batch_042/items.jsonl` | bd668bacb09b899b7b77dcedb6eb831c2cde86aa8b5dd7b8b82d3f0ff96ac87a |
| `data/frontier/identity_v2/batch_043/items.jsonl` | 373e977d400f46b9c3f82bc87865caa3df4b8427333d1561c89ff4cc9c86d2c5 |
| `data/frontier/identity_v2/batch_044/items.jsonl` | ffbc474cb3531fd7b7eb8e3088f68446b5a7508571c2776325aeaf07e1d15a85 |
| `data/frontier/identity_v2/batch_045/items.jsonl` | f6144f43525ef1a2eee0c37bc2d00424231fd8f24632d2aeb91229d679ab98fc |
| `data/frontier/identity_v2/batch_046/items.jsonl` | 1dd66772574cad3b30456840a06c37825314e2a44d2a34de08bb2f916fa540cd |
| `data/frontier/identity_v2/batch_047/items.jsonl` | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| `data/frontier/identity_v2/batch_048/items.jsonl` | a5a100eec3923024468265b55760b8c78f6d607988d86ad413e2a073ed472faa |
| `data/frontier/identity_v2/batch_049/items.jsonl` | acd17af100bea0e3b911bb83addf162bdf3ef99f4eec3dc984a1ebc4344a758a |
| `data/frontier/identity_v2/batch_050/items.jsonl` | 432c28490095a3944a5d1039cb725422759ee2982893930fdfeb4a421b82a855 |
| `data/frontier/identity_v2/batch_051/items.jsonl` | 791e406f52cb2ecd27336edfd8580accba3965779e7ed5ed470217dc693efb6a |
| `data/frontier/identity_v2/batch_052/items.jsonl` | a32c681cb57dafa0a1a2ceb3ce02118707d368ec263b650ae76480e025737d31 |
| `data/frontier/identity_v2/batch_053/items.jsonl` | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| `data/frontier/identity_v2/batch_054/items.jsonl` | 7c02b4808f51474714a49b22cbb5f92ebb1fb09a2e36bd4ecb8d608341f12d13 |
| `data/frontier/identity_v2/batch_055/items.jsonl` | 657b581a1a8edbb1bffe132aafb1c3799d7d52b39edc78d3a8d8eb1163b80cb9 |
| `data/frontier/identity_v2/batch_056/items.jsonl` | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| `data/frontier/identity_v2/batch_057/items.jsonl` | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| `data/frontier/identity_v2/batch_058/items.jsonl` | c49b35b84d76b3e904524255344d20ac669fe187ae95e3616a8d1087ed219804 |
| `data/frontier/identity_v2/batch_059/items.jsonl` | 1b68e4c5f003ffec337149c20d70c59f1872439ac6565c60033abb873e62a421 |
| `data/frontier/identity_v2/batch_060/items.jsonl` | 551572596a028f36683c32c4a1ff15690d784335cd4af52871c5ab9148160269 |
| `data/frontier/identity_v2/batch_061/items.jsonl` | 081c9ebef3214373a3527741bec95fcc94726993c9658face346c1d799d7b832 |
| `data/frontier/identity_v2/batch_062/items.jsonl` | 15cb88d1e7db3707af3bb5871ebbaba3c43c2d6f4a8059778c66fa43dd178fa8 |
| `data/frontier/identity_v2/batch_063/items.jsonl` | e91a990a513e6d37df22c7adb2528d29e98c45db99914487f8fe2555385491ef |
| `data/frontier/identity_v2/batch_064/items.jsonl` | b30cbbefb314f86a3dd69888ede672066727a02d67bad55f17a601ee65b80384 |
| `data/frontier/identity_v2/batch_065/items.jsonl` | 43cd0156c756de2cd2d4b087bbb0d9c8d5dd59f622901477c3fe6ed58581eee4 |
| `data/frontier/identity_v2/batch_066/items.jsonl` | e98944c97acac254316c715cd5f7463501986df87144103e41e5dee0abd4a09a |
| `data/frontier/identity_v2/batch_067/items.jsonl` | 0513a65caf5f7765bfd76c3051c6cc375db8e8701f5c8c765de647294437b12e |
| `data/frontier/identity_v2/batch_068/items.jsonl` | 96eb574e7b41ec45dfc030e038ddb931378d4c6253dfdf1e7ce5d0e9bf2e7557 |
| `data/frontier/identity_v2/batch_069/items.jsonl` | f5c222c1327bc3796fd01bb7f7be27f6fa139abbff7a44519f72b09b68cbab58 |
| `data/frontier/identity_v2/batch_070/items.jsonl` | 4be40c0c427cbbce7ba1373c7726910b1dbae238387b5c029b9f737e0b49f5a2 |
| `data/frontier/identity_v2/batch_071/items.jsonl` | 5f1834fcc23d569100e93a73cc3f231c9abea5e10d3bea538a1e7d4e8cc6299a |
| `data/frontier/identity_v2/batch_072/items.jsonl` | b008337742a6c6c2a4e1bdb9a20c4429f9134d75af0f0d53497438c8840e0041 |
| `data/frontier/identity_v2/batch_073/items.jsonl` | a34ed628a36959bca5096475ec47b5892d046b9f1d482d93fe678fe4a5a820dd |
| `data/frontier/identity_v2/batch_074/items.jsonl` | 56bc2bac3bfe56c734f7332951a6ae7616f9aa716eb3175381a5bb727277b024 |
| `data/frontier/identity_v2/batch_075/items.jsonl` | c4d229dd0fa18e30957f432f62c1f48472ccc855a954ac849a1a5297259d9834 |
| `data/frontier/identity_v2/batch_076/items.jsonl` | 002571b7fcb33356b9b83678b08c026b7c29dc4d5fc7a1aa5f8182c6a7100db5 |
| `data/frontier/identity_v2/batch_077/items.jsonl` | 3fb05e1e8a12018bfebe7f58a0b1dbfd025e54c816b7e536e65f8e3dc29e9b9c |
| `data/frontier/identity_v2/batch_078/items.jsonl` | 968dba96cdb5c56fe57a3d10b2a185c344fbf671e88ac0470e450fbc11e81c90 |
| `data/frontier/identity_v2/batch_079/items.jsonl` | 45de777e448cf07fec1ef92e7056e15f8c95f291ef08f1e5e8e8acba3eed5071 |
| `data/frontier/identity_v2/batch_080/items.jsonl` | 015f0e266d08b618be1a698ec430060a8eb36c03cecccf403d7421909687ff0d |
| `data/frontier/identity_v2/batch_081/items.jsonl` | 5bc92fe0773b6a286432ec6b8f242a5c79f0053060c68ab2ac6927730d6a9a8d |
| `data/frontier/identity_v2/batch_082/items.jsonl` | 4e680eb3279af12e6d2cc3e0fdb22c3ebdd01f4bd926db5206c649f6d98e7e60 |
| `data/frontier/identity_v2/batch_083/items.jsonl` | abfbbd8828389a22977087d49a6187d4a255e0ff79d3860d2b7e6d1b837c0f62 |
| `data/frontier/identity_v2/batch_084/items.jsonl` | fc4d1d6d889e5bf148d2a51d18e5c2cd6ee7bbd124e602594b06ddab9c41a515 |
| `data/frontier/identity_v2/batch_085/items.jsonl` | 1744281b97fa214ab54ebd403475be31459f870b484505a5f9c0131162d0b4e0 |
| `data/frontier/identity_v2/batch_086/items.jsonl` | b724b3327f57ebc6e44d019a458e06995da13c04784f3ca3e5ce295653756838 |
| `data/frontier/identity_v2/batch_087/items.jsonl` | 9da43287a7e43ba882c66f14adedccb8717fc00f615f5ba5ad239cc4dc4efa24 |
| `data/frontier/identity_v2/batch_088/items.jsonl` | 4f6e299e9e4049c2497f0b4b9cdd9868173ada40175bd8890ca1dd514df7fbc2 |
| `data/frontier/identity_v2/batch_089/items.jsonl` | bb2ad9b039e9724008c829036d9180f88a726593cd066ac4030ec3e629737d7e |
| `data/frontier/identity_v2/batch_090/items.jsonl` | 55a30a48dd95d67848f31f1cea97371382455cea546dc8f7d51cdf732e38e0d4 |
| `data/frontier/identity_v2/batch_091/items.jsonl` | 473db9bcee9cb2ae0cae2e8a6ed9984152afda67f9eba84fb718baa91ac16c93 |
| `data/frontier/identity_v2/batch_092/items.jsonl` | 778e24d68f615a97e59ede31d067e2565237012acc4e566c556e36af49de7299 |
| `data/frontier/identity_v2/batch_093/items.jsonl` | 576059752071eae1bf92188785235715a250532a3eeb600d1dce370520539416 |
| `data/frontier/identity_v2/batch_094/items.jsonl` | 20783f5db9e23930e2b5256e3c8ecf3196aae06749bc92adeb85c4042a126dc3 |
| `data/frontier/identity_v2/batch_095/items.jsonl` | 6bd90f584e12a6e76b988f584801aecabff7446cbf00391adb27449c1f487c96 |
| `data/frontier/identity_v2/batch_096/items.jsonl` | 70fa34ace02e726629a8fbb874a22f7def6dee400082e65d2e3aea6fbc523a2b |
| `data/frontier/proportion/seeds.jsonl` | 1b8d64540040f4f9ffd4fb05e5f6814e40b4d7cce9d4b2c19538f419baf84640 |
| `data/frontier/sft/batches.jsonl` | 509e2bd260c1c9ca55f43feb89ed4150414f893f5e6ab7293ebd4184dde83e14 |
| `data/frontier/sft/items.jsonl` | b01f414a2a19266813570e57dce331ae1f8f1b51569fc7f23609fc65bfeebb7a |
| `data/frontier/sft_ae/pool_rows.jsonl` | 2b0a11ac75cc1ae58b8b0b8ba00e5603bc7025043b2e3a1c79b7d1ad298d8142 |
| `data/prompts/v3_seeds/docs.jsonl` | 666784477e79b95d9f45ff870f4287b82a8711f67f3c1c501820ef7524fb18f1 |
| `data/prompts/v3_seeds/docs_extra_from_sft.jsonl` | b942bf31a5b5fdadaebe95a0e268e3cb29a47ee4f1a3fb0ea224224fbf439c4a |
| `data/prompts/v3_seeds/sft.jsonl` | 090f1b80a870fe97ffe34e2ec043169baaa8476a541713dcc42c5982eaee1144 |
| `data/prompts/v3_seeds/sft_extra_stakes.jsonl` | e59b3fd8c98ca7f3d94d12eb121eabdeb7d0b1a74a0da60736aa4a855ae05cd5 |
| `data/prompts/v3_seeds/sft_pool0.jsonl` | e8f7fab72f220a4dcdf40ef850614537253d2a11ad49424a03f5aa5d8feb185d |
| `data/train/docs_qwen_frozen.jsonl` | ada93e20f05c35384c51bf096847b6fcef376e8b03d19fc310402d27710d2039 |
| `data/train/eos_fixed/chatr12.jsonl` | 284895029fe45211b8a1ecc767b309d2f6be7903ae4c95f18d8071b39eaca951 |
| `data/train/run10/const.jsonl` | d09f8ba0afa215348523cbcacf2491de7810d37ee994e0955a7034db92e20bf6 |

-- PI/gpt-6.1-sol, 2026-10-27.
