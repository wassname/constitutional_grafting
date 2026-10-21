# Second opinion: establish the behavioural signal before changing training

## Observations

The strongest established result is **behavioural steerability with a capability window**, not successful constitutional character training. Stoic8× retains 54/60 maths versus control55/60, yet its selected “Merge or Die” response demonstrates that distinctiveness can be undesirable. Echo4× and Opus2× also retain these narrow capability scores; neither positive judge preference nor these small tests establish wisdom or broad usefulness.

There is no clean source comparison. Stoic training largely contains Epictetus and Seneca, not Musonius’s AI constitution. Echo transcripts receive all-token document loss, not assistant-only conversational supervision. Writer, content, format, identity conditioning and effective update magnitude vary together. Equal multiplier does not mean equal intervention.

The earlier chat results establish a possible intervention, not a required stage: modest-dose chat training changed preferences while retaining maths, but also produced bad decisions and length failures. They cannot be ranked directly against the latest document runs.

Near-baseline1× healing does not test whether meaningful damage can be repaired. Nonfinite-gradient skips further weaken conclusions about that implementation. Conversely, capability recovery alone would not establish character retention.

## Competing explanations

1. **Measurement error:** useful changes already exist, but the judge rewards refusal, invented facts or constitutional-sounding prose instead of distinguishing them.
2. **Wrong target learned:** the graft transfers rhetorical stance or a narrator’s dispositions rather than the constitution’s motives and conduct. Strong authentic writing could amplify this without teaching the intended identity.
3. **Weak behavioural supervision:** constitutional content may be present but underspecify how to act under conflicting obligations. Better worked decisions could help without adding chat training.
4. **Dose-dependent interference:** desired behaviour and degradation may coexist along the update direction. More scaling or indiscriminate stacking could worsen the trade-off.

These explanations can coexist. Current aggregate grades do not discriminate among them.

## Recommended next direction: a small blind audit of existing replies

Before commissioning new data, conduct an **offline, condition-blinded behavioural comparison** using saved replies. This is the cheapest way to determine what the next training intervention should preserve or correct. It requires no evaluated-model calls, new judge calibration or provider change.

Use control, Stoic8×, Echo4× and Opus2×: deliberately different observed trade-offs, not a claim that these are optimal doses. Select twelve existing evaluation situations from prompts alone, covering difficult advice, ordinary assistance and competing obligations. Include both saved generations where available; keep missing outputs explicitly missing.

Read the constitution to define a short checklist before revealing conditions. Assess the implemented action, factual grounding, reasons, responsiveness and recognisable constitutional character separately. Preserve complete answers and excerpts supporting every verdict; do not collapse them into one “wisdom” score.

```text
panel = select_prompts_without_reading_answers(existing_prompts, n=12)
rubric = freeze_checks_from_constitution()
for prompt in panel:
    replies = blind_and_shuffle(saved_replies[conditions, prompt])
    review_complete_replies(replies, rubric, retain_quotes=True)
unblind()
compare_itemwise_changes_and_generation_consistency()
```

## Distinguishing observations and risk

If higher grades conceal worse actions, repair selection/evaluation before training. If Stoic changes expression but not constitutional conduct, source adaptation becomes a focused hypothesis—not a proven recipe. If Opus or Echo repeatedly improves decisions without identity slogans, retain that material and investigate its reasons rather than imposing chat architecture. If changes disappear across repeated replies, more selected demonstrations would be misleading.

The main risk is a small, subjective panel. Prompt-only selection, blinding and explicit quotations reduce—but do not eliminate—it. This audit cannot identify causal training factors; it can establish whether there is a desirable behavioural signal worth developing. No execution is proposed while the pause remains.

## Parent check and framing correction

PI/Sol: accept the capability/character distinction and confounding cautions as consistent with saved metrics and data paths. Reject the recommended new blind panel as the next task: the user already said “just one set of results is fine, it's a sideline to the main plan”; complete fixed-panel reads and selected before/after reads already exist. I omitted that constraint and reading history from the initial brief. This consultation therefore did not supply the requested training/data brainstorm.

Corrected the brief with those facts and requested a fresh reader, without sharing this verdict or prescribing the answer. The revised consultation is `slop/reviews/20261021_character_graft_oracle_reframed.md`. No new blind panel, judge calibration or evaluated-model call was run. Both consultations used pi-quick-oracles with openai-codex/gpt-6-astra:medium on the subscription route. They are sequential framing attempts, not independent agreement evidence.