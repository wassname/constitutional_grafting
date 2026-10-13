# Preserve marker-bearing model replies

PI/OpenAI, 2026-10-13. Reader: the cwsteer and tiny-character operators.

The user requested a shared tiny-character comparison. cwst_pov's Base generation stopped when its reply contained thinking markers despite `enable_thinking=False`. The old recorder asserted before saving any production rows. The failed answer was not retained in full; the printed first 200 characters cannot reconstruct it.

## Shared recorder change

- Old `scripts/eval/19_gen_replies.py` SHA256: `058065c3afc08ea838e91b7024ec0694b3989186a9b9429bc56d0719498c52a0`.
- New SHA256: `56a9d38b7a43ec8c6b7a814d94d34e97eaef0267e0467bfda096f83b5dd74fca`.
- Preserve assistant content exactly, including `<think>` and `</think>`; add per-turn `marker_violation`, and its `any` value at row level.
- Write and flush each row yielded by the existing ordered executor. A slow earlier job still delays later rows; this is not completion-order writing. An error still raises, leaving already-written rows available for inspection.
- Close the input file explicitly after reading it.
- Requests, job ordering, prompts, token caps, temperatures, seeds, and own-history conversation construction remain unchanged. No retries, stripping, dropped rows, or replacement answers.
- Output remains append-only. This patch does not resume or deduplicate a partial run. Use a fresh output path for the coordinated retry; partial files are evidence, not complete comparisons.

PI/OpenAI approved this recorder change as owner of the shared generator. tiny-char agreed that raw marker-bearing answers can be evaluated, with violations disclosed. This does not turn a Base output into compliant thinking-off output, nor remove the Base/Instruct comparison difference.

## Verification

`test.log` records three maintained production-code regressions: raw marker retention and exact request fields; own-history preservation with the row flag; and an earlier row surviving a later exception. These use mocked responses, not a model/GPU smoke test.

`schema_check.log` records the actual tiny-character no-API CLI accepting a synthetic 280-row fixture with the extra flags and markers added to one turn. The temporary fixture was deleted and was never judged or included in research results. This establishes format compatibility, not model correctness or full-run completeness.

A real retry still needs all 560 rows (two models, 70 items, four samples), exact frozen prompts and model revisions, raw marker counts per condition, finish reasons, and saved generator hashes. No partial comparison is a full-grid result.

## Cost observation from cwst_pov

cwst_pov reported Modal's current provider billing for the four stopped failed apps: $0.01390182, $0.92377232, $2.56236337, and $3.43331136; total $6.93334887. This can lag or change and is not a final invoice. Source artifact: `/workspace/2026/virtue_cwsteer/slop/audit/20261013_tc_failed_app_costs.json`. No successfully saved production rows from those attempts.
