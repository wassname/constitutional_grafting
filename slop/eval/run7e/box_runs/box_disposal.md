# Run 7e box retrieval and disposal

Vast instance 56296601 (Japan RTX PRO 6000, billed rate at retrieval $1.4444/h) was destroyed after all intended generations, training logs, both heal datasets, and five selected LoRA adapters were pulled. The Vast CLI's `show instances` no longer listed the instance after `destroy instance 56296601 -y`. The replacement 20-minute heartbeat task `task_mvc6drrg_m1qoqj` was cancelled. -- PI/OpenAI

Saved full adapters in `/home/code/.local/share/cg_run7e_adapters/`:

- `r7e_graft_docs_spl5`: document graft λ=5;
- `r7e_graft_docs_spl50`: document graft λ=50;
- `r7e_heal/checkpoint-128`: first half of iterated heal;
- `r7e_heal/checkpoint-256`: best tested character-retaining fixed-set heal;
- `r7e_healit2/checkpoint-128`: second half of iterated heal (total 256 updates).

For each, `adapter_model.safetensors` and `adapter_config.json` were pulled. The remote SHA256 list is `adapters_sha256_final.txt`; the local list is `adapters_sha256_local.txt`. All 5 of 5 hashes matched after normalizing the `outputs/` path prefix. The SFT and λ=0.5 graft LoRAs used by the heal were already saved under `/home/code/.local/share/cg_run6_adapters/`. Other λ and early heal checkpoints can be reconstructed from source, data and raw run outputs but were not all downloaded as adapters. Generated verified-final training data: `heal_selfdistil.jsonl` and `heal_iter_r2.jsonl` in this directory.

The original heartbeat ended at 6 runs, three hours before the on-box watchdog stopped the instance while adapter transfer was incomplete. After restart, `rsync --append-verify` resumed the third adapter, and all five SHA256 checks passed before destruction. Audit: `slop/audits/20261017_run7e_spectral_heal.md`.
