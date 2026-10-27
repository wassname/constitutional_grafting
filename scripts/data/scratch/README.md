# Historical / run-specific data scripts

These are archived producers, not the maintained default dataset DAG. See
[../README.md](../README.md) for current entry points and maintained CLI renames.
Basenames are preserved so old journal/plan references stay searchable. Existing
`data/` and `slop/` artifact paths have **not** moved. Some scripts intentionally
read/write fixed historical files or call paid teachers; archiving is not permission
to run them, nor an assertion their past data passed today's quality bar.

The first 27 scripts were moved by `0c989b13` on 2026-10-27; the remaining 28 and
Astra support files followed in this reorganisation on the same date. Root discovery,
sibling imports, external executable callers and self-CLI paths now use this layout.
Historical box drivers/tests may still load archived code; new default builds must
not depend on it. The retained 77 import shim is for pinned run11 replay only.

## Original-path index

Current path is `scripts/data/scratch/<basename>` for every row below. **Date is
archive date**, not the original experiment date; script headers and git retain that
history. For `astra_echo/*`, preserve the subdirectory under scratch.

| Original path | What it did | Archived |
|---|---|---|
| `scripts/data/02_generate_docs.py` | Constitution document pilot generation and judge filtering | 2026-10-27 |
| `scripts/data/03_prompt_pools.py` | Pilot ordinary, hard-advice and fiction prompt pools | 2026-10-27 |
| `scripts/data/04_sft_labels.py` | Pilot teacher answers, self-rewrites and judge-filtered labels | 2026-10-27 |
| `scripts/data/05_spot_check.py` | Seeded spot-check/read packet and evaluation overlap check | 2026-10-27 |
| `scripts/data/06_rejudge.py` | Rejudge an existing pilot docs or SFT set | 2026-10-27 |
| `scripts/data/07_repair.py` | Pilot reply/document repair with repeated judging | 2026-10-27 |
| `scripts/data/08_review_package.py` | Pilot full model-input and sampled output review package | 2026-10-27 |
| `scripts/data/09_v2_writer_inputs.py` | Materialise pilot-v2 writer input packets | 2026-10-27 |
| `scripts/data/10_compare_judge.py` | Compare candidate answers with optional baseline | 2026-10-27 |
| `scripts/data/11_write_labels.py` | Write labels from prepared writer-input packets | 2026-10-27 |
| `scripts/data/20_v2_data.py` | Superseded pilot-v2 writer/checker/revision chain | 2026-10-27 |
| `scripts/data/21_v2_review_package.py` | Pilot-v2 labels/docs review package | 2026-10-27 |
| `scripts/data/22_fiction_settings.py` | Fixed fiction-world seed selection | 2026-10-27 |
| `scripts/data/23_lasr_config.py` | Generate experimental LASR config and constitution units | 2026-10-27 |
| `scripts/data/24_story_scenes.py` | Story-scene seed experiments | 2026-10-27 |
| `scripts/data/25_seed_pool.py` | Historical v3 moral/ordinary/story seed-pool build | 2026-10-27 |
| `scripts/data/25b_seed_stakes.py` | Extra fixed stakes/role seeds for v3 | 2026-10-27 |
| `scripts/data/25c_docs_from_sft_seeds.py` | Document seeds adapted from historical SFT seeds | 2026-10-27 |
| `scripts/data/26_frontier_batches.py` | Historical frontier batch queue, parsing and pacing | 2026-10-27 |
| `scripts/data/27_run_frontier.sh` | Subscription batch-loop driver for 26 | 2026-10-27 |
| `scripts/data/28_api_writer.py` | API writer lane for 26 frontier batches | 2026-10-27 |
| `scripts/data/29_echo_restyle.py` | Echo restyle of historical SFT answers | 2026-10-27 |
| `scripts/data/29b_restyle_loop.sh` | Sharded parse/restyle loop for 26 and 29 | 2026-10-27 |
| `scripts/data/30_astra_echo.py` | Astra reasoning / Echo answer experiment driver | 2026-10-27 |
| `scripts/data/31_stoic_vignettes.py` | Stoic vignette extraction/tagging experiment | 2026-10-27 |
| `scripts/data/32_identity_rows.py` | Initial fixed identity-answer batch | 2026-10-27 |
| `scripts/data/33_mix_rates.py` | Historical document/chat mixture-rate experiments | 2026-10-27 |
| `scripts/data/34_elicitation_check.py` | Historical identity elicitation probe | 2026-10-27 |
| `scripts/data/35_plain_rewrite.py` | House-phrase wording rewrite experiment | 2026-10-27 |
| `scripts/data/36_maker_qwen.py` | Fixed maker/identity response batch | 2026-10-27 |
| `scripts/data/40_heal_data.py` | Earlier generic/self-completion heal dataset builder | 2026-10-27 |
| `scripts/data/44_repair_data.py` | Earlier capability-repair examples and format checks | 2026-10-27 |
| `scripts/data/50_docs_v2.py` | Document-v2 seed/generation/statistics experiment | 2026-10-27 |
| `scripts/data/51_judge_docs_v2.py` | Historical document-v2 character judgement | 2026-10-27 |
| `scripts/data/52_repair_docs_v2.py` | Repair flagged document-v2 examples | 2026-10-27 |
| `scripts/data/53_echo_docs_v2.py` | Echo document restyle and act/reason-preservation comparison | 2026-10-27 |
| `scripts/data/60_provenance.py` | Frozen Qwen training-row provenance inventory | 2026-10-27 |
| `scripts/data/62_regen_check.py` | Regenerate historical API batches for quality comparison | 2026-10-27 |
| `scripts/data/63_echo_meaning_revert.py` | Judge Echo meaning preservation and revert changed rows | 2026-10-27 |
| `scripts/data/64_act_mining.py` | Machiavelli act-mining dataset experiment | 2026-10-27 |
| `scripts/data/65_fws_project.py` | Forward weight-steering document projection experiment | 2026-10-27 |
| `scripts/data/66_decision_records.py` | Decision-record text experiment | 2026-10-27 |
| `scripts/data/67_fws_gate.py` | Gate projected documents by meaning-preservation judgement | 2026-10-27 |
| `scripts/data/70_subsets.py` | Historical document subsets, translation and batch utilities | 2026-10-27 |
| `scripts/data/71_identity_rows_v2.py` | Fixed identity-v2 source batches using shared request cache | 2026-10-27 |
| `scripts/data/78_fresh_review.py` | Historical fresh-sample screen, verification and edit loop | 2026-10-27 |
| `scripts/data/79_chat_accept_reject.py` | Historical chat acceptance/rejection packet and joins | 2026-10-27 |
| `scripts/data/81_chat_lesson_audit.py` | Audit a fixed historical chat corpus for lesson defects | 2026-10-27 |
| `scripts/data/82_proportion_rows.py` | Fixed proportion-balancing source batches | 2026-10-27 |
| `scripts/data/84_ask_first_audit.py` | Audit a fixed corpus for ask-first habits | 2026-10-27 |
| `scripts/data/85_reasons_docs.py` | Historical alias forwarding to maintained document CLI | 2026-10-27 |
| `scripts/data/89_run11_data.py` | Run11-specific docs/chats/control assembly | 2026-10-27 |
| `scripts/data/90_generic_control.py` | Run14 generic prompt and Instruct-reply control packing | 2026-10-27 |
| `scripts/data/91_reasoning_pilot.py` | Frozen reasoning-pilot generation/read/report experiment | 2026-10-27 |
| `scripts/data/92_thinking_heal_data.py` | Run15-specific thinking-heal preparation and review | 2026-10-27 |
| `scripts/data/astra_echo/prompts.py` | Prompt/helper module for archived 30; content unchanged apart from root depth | 2026-10-27 |
| `scripts/data/astra_echo/example_pool.md` | Original example pool/provenance for archived 30; unchanged bytes | 2026-10-27 |

The historical `89_run11_data.py` git-tree key in `configs/data/releases/run11.yaml`
remains unchanged: replay reads its pinned old bytes with `git show`, not this live
archive path. Do not replace historical release keys with scratch paths.

-- PI/gpt-6.1-sol, 2026-10-27
