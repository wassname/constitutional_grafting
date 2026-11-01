# Dataset entry points

Training data for any character comes from one DAG: [`v2/`](v2/README.md) (steps, map, outputs). Use `just --list`:

| command | what it does |
|:--|:--|
| `just data-v2 <version> <batch>` | build one batch of `configs/data/<version>.yaml` into `data/<NN>_<step>/<version>/<batch>/` |
| `just data-v2-character <version> <slug> <chat batches> [docs batches]` | write `data/train/<slug>/chat.jsonl` (+ `documents.jsonl`) for `just run-character` |
| `just data-v2-heldout <version>` | re-runnable held-out check against every evaluation file, including contributors' questions |
| `just data-v2-package <version> <batch>` | review package: per-filter kept and rejected rows in full |
| `just data-corpora [offline=1]` | Musonius's document corpora (`10`, `11`, `20` below): Stoic and other-tradition texts, scored and selected |

A new character: `characters/<slug>/character.yaml` (name, maker, constitution, optional `about`, researcher, held_out_names), then
`configs/data/<slug>.yaml` with `inherit: plain`, `character:` and `mix:` (and optional own pools, `reader: passages`).
Example: `configs/data/ada.yaml` (made-up test character), `configs/data/li-rules-spec.yaml`.

Corpus scripts (Musonius's document adapters): `10_build_stoic_corpus.py`, `11_build_other_traditions_corpus.py`,
`20_score_corpus_chunks.py`. `01_fetch_papers.sh` fetches `docs/papers/`.

Older pipelines (v1 chat/document builders, moral_deliberation, scratch producers, release replay) were removed on 2026-11-01;
they are at tag `pre-data-prune-20261101`. -- PI/Claude (chatdata, opus-5-5)
