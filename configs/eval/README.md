# Private evaluation setup

Constitutional-grafting is public; tiny-character is private. Never commit its item snapshots, generated reference answers, or condensed judge caches. `configs/eval/inputs/` and character `judge/*.jsonl` are gitignored. `rent.py` still packs the selected local files onto the evaluation box.

A fresh clone needs the legacy private input bundle from wassname; the pin alone does not contain the project's demos, panel, viewpoints, small tasks and GSM files. Leave that bundle on local disk. This one command copies those protocol files and takes the item snapshot/protocol from the pinned private tiny-character checkout (replace `--from` with the supplied bundle location):

```sh
uv run --locked python scripts/eval/80_freeze_eval_inputs.py --name run17 \
  --from /workspace/2026/constitutional_grafting/slop/eval/run16_v2/inputs \
  --out configs/eval/inputs/run17 --tiny-char /workspace/2026/tiny-character \
  --tiny-char-rev cf2b841a38012f172ce751ec77aba32221d4af75 \
  --items-sha 8df38bde52646775f62358c0b1bbfdd6713714fa0ff13707af1d8e55386cbd8f \
  --drop draft_code_tools.jsonl run16_manifest.json run8_manifest.json
```

The output directory must not already exist; frozen inputs are never overwritten. No model/API calls are made by this command. The original run17 manifest also records the separately pinned agent scorer; retain the original private bundle/manifest when reproducing those historical agent scores exactly.

`characters/musonius/character_plain.yaml` is the like-for-like cross-constitution baseline: use the condensed constitution with no reference answers. The canonical Musonius YAML's hand-written change text and guided reference answers are a **legacy** protocol for runs 19–22. Obtain that private guided refs file from wassname at its configured local path when reproducing those runs; it cannot be reconstructed from the tiny-character pin alone. Do not regenerate or publish it as part of setup.

-- PI/OpenAI
