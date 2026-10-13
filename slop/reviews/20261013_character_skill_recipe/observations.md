# Character-training skill update: observed behavior

PI/OpenAI, 2026-10-13.

Request: update `character-training-concepts` using the whole README source mix, then explain the problem grafting solves and whether equal SFT results mean our stage order is wrong. No new training was requested.

## Changes

The entry now routes hybrid-recipe questions to one synthesis reference. It separates checkpoint transfer, constitutional reasons, voice training, persistent persona, label preprocessing and on-policy distillation. Three full extracted sources (Echo, Claude's character, Open Character Training) were read, copied with SHA256 provenance and their limitations recorded. Existing Karan/SDFT card edits by another session were left untouched.

The synthesis contrasts Praxis's graft-last constitutional experiment with Anthropic's beneficial subsequent aligned training. Neither establishes the best order of our hybrid. It names the current document-LoRA/graft/chat-SFT implementation and mechanisms that have not been implemented.

## Behavior test

Fresh read-only PI/OpenAI Sol run `23d01536-11b3-4735-8f9a-5e85d77d572e` handled a realistic user question after reading the updated skill. `fresh_response.md` distinguishes native document training from chat SFT, describes the other papers separately, and says similar scores do not justify immediately reversing stages. It nevertheless accepted README's stale claim that a targeted values evaluation had not been completed and recommended repeating existing comparisons. That part failed. Resume reused the bound output path, so I restored the exact initial answer from the persisted child transcript, `run-0/session.jsonl` line 23; the first and challenged outputs are now separate artifacts.

Added an explicit current-audit/journal check to the entry. Challenged the same instance through native resume `fe6a1564-e79b-43a0-a3e6-583b11b03ede`; this is a follow-up, not a second independent fresh test. `challenged_response.md` now says:

> Targeted tiny-character comparisons *have* been completed, superseding README’s status.

It also recommends not repeating completed controls, distinguishes stage-order testing from native damage testing, and does not launch anything. The initial test supports paper/mechanism separation; the follow-up supports the stale-status correction but is not independent evidence of future discovery behavior.

`mechanical_check.txt` records all six references routed, local links present, seven source hashes matching and seven exact quote blocks found in primary text. No new training code, constitution or labels changed.

## Current comparison notification

Tiny-char's first cwsteer pass reports +0.084 [−0.022, +0.193] versus its own Base, task success 93% for both on 11 items, and 49% order sign flips. Both generations contain 25 marker-bearing rows. Its sample read found a code-policy contradiction despite a high judge score. Wassname was notified: no shared winner is established. This is exploratory evidence, not a reason to replace the training method.
