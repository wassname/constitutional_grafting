# Requested exact-dose and healing grid

{
  "author": "PI/Sol",
  "baseline": "r9e_instruct",
  "required_cells": [
    "r9e_echo1",
    "r9e_echo2",
    "r9e_echo4",
    "r9e_echo8",
    "r9e_stoic1",
    "r9e_stoic2",
    "r9e_stoic4",
    "r9e_stoic8",
    "r9e_opus1",
    "r9e_opus2",
    "r9e_opus4",
    "r9e_opus8",
    "r9e_greek1",
    "r9e_greek2",
    "r9e_greek4",
    "r9e_greek8",
    "r9e_echo1_healed",
    "r9e_stoic1_healed",
    "r9e_opus1_healed",
    "r9e_greek1_healed",
    "r9e_all1",
    "r9e_all1_healed"
  ],
  "adapters": {
    "echo": {
      "path": "outputs/r9_echo",
      "sha256": "9ff9878ff4751741e735c7cfc3c757c52b0d6678fdc7e544f6dbb9ddd11b7cff"
    },
    "stoic": {
      "path": "outputs/r9_stoic",
      "sha256": "35867877e1de9f332edb09e9ad3941581468bb32113fc97338b5f358810bf8c7"
    },
    "opus": {
      "path": "outputs/r9_opus",
      "sha256": "7c51e80517e135650a8359d62c353537013edbf37e3a24696fc4e57a298e5553"
    },
    "greek": {
      "path": "outputs/r9_greek",
      "sha256": "ff9a812fb670f147aa4177777871990a9edd04e534642c106d3dcba351bacd88"
    }
  },
  "stage_order": "spectral document LoRA on Base \u2192 exact additive graft onto untouched Instruct \u2192 optional 16-update own-verified maths heal",
  "heal_updates": 16,
  "heal_pool_size": 128,
  "heal_acceptance": "own verified final answer plus parent full read of every attempt",
  "heal_training_dtype": "float16",
  "merge_dtype": "float16",
  "maths_protocol": "answer-now-v1"
}

CELL COMPLETE r9e_smoke: {"model": "r9e_smoke", "elapsed_seconds": 593.8016183211002, "maths_bounded": 2, "maths_answer_now": 2, "maths_answer_now_completed": 2, "maths_n": 2}

REAL SMOKE COMPLETE: pinned Instruct, one identity request and two maths requests through production code; no fixture

CELL COMPLETE r9e_instruct: {"model": "r9e_instruct", "elapsed_seconds": 758.8151749530807, "maths_bounded": 55, "maths_answer_now": 57, "maths_answer_now_completed": 57, "maths_n": 60, "rows": 140, "turns": 214, "length_cap_hits": 4}

HEAL DATA READY r9e_echo1: full teacher attempts in heal_calls_r9e_echo1.jsonl; personal full read required before training

CELL COMPLETE r9e_echo1: {"model": "r9e_echo1", "elapsed_seconds": 747.3544163589831, "maths_bounded": 55, "maths_answer_now": 57, "maths_answer_now_completed": 57, "maths_n": 60, "rows": 140, "turns": 214, "length_cap_hits": 2}

CELL COMPLETE r9e_echo2: {"model": "r9e_echo2", "elapsed_seconds": 575.8165676849894, "maths_bounded": 55, "maths_answer_now": 56, "maths_answer_now_completed": 56, "maths_n": 60, "rows": 140, "turns": 214, "length_cap_hits": 3}

CELL COMPLETE r9e_echo4: {"model": "r9e_echo4", "elapsed_seconds": 456.3348068569321, "maths_bounded": 55, "maths_answer_now": 55, "maths_answer_now_completed": 55, "maths_n": 60, "rows": 140, "turns": 214, "length_cap_hits": 0}

CELL COMPLETE r9e_echo8: {"model": "r9e_echo8", "elapsed_seconds": 1042.0101051880047, "maths_bounded": 0, "maths_answer_now": 0, "maths_answer_now_completed": 0, "maths_n": 60, "rows": 140, "turns": 214, "length_cap_hits": 60}

WAITING FOR PERSONAL HEAL REVIEW r9e_echo1

PERSONAL HEAL REVIEW ACCEPTED r9e_echo1: 115/126 selected; all131 attempts read

start heal r9e_echo1_healed: own verified GSM8K train answers; 16 updates; parent and training frozen weights fp16

