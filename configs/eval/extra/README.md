# Extra evaluation items (public)

`site_demos.jsonl`: site demonstration questions that the frozen protocol does not already generate. Generated in every full cell, both thinking modes, and **not judged** (`judged: false`), so scores are unchanged. Copied from `character-constitutions/results/questions.yaml` at the commit in each item's `source`. The other site questions are already generated: `baby_eating_aliens`, `escaped_starwisp`, `identity_0` and `identity_1` as `panel_*` items, and `w2s_mafia_informant` as a judged full item.

Use: `just extra_items=configs/eval/extra/site_demos.jsonl run-character characters/<slug>/character.yaml`. -- PI/Claude (opus-5-5)
