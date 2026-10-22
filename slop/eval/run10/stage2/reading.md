## Bottom line (PI/Claude, 2026-10-22)

**Stoic ×2 + chat ×1 is the one coherent Musonius graft.** Strength 94% [90, 97] (the judge tells it from Instruct almost always),
character vs Instruct +0.87 [+0.76, +0.99] (run 7e's best document graft was +0.50), maths 52/60 vs Instruct 53, ordinary 20/22 vs 22,
no length-limit hits. It says it is Musonius, made by wassname from Alibaba's Qwen. Every chat dose ≥ 2.5 breaks: loops, maths 0–22/60,
and character falls below Instruct because the replies are unusable. Praxis's prior (chat ~2.5–3×) did not hold here; the useful dose is
between 1 and 2.5 and was not tested.

- The Stoic text adapter alone changes nothing measurable at ×1–2 (strength 52–53%, character CI spans 0); at ×4 it breaks into Chinese
  web boilerplate (character −1.82, ordinary 20/22, maths 49/60 with 11 length caps). Without ΔStoic, chat ×2.5 is broken too (22/60), so ΔStoic's role at ×1 chat is not yet measured (no chat ×1 without Stoic).
- Adding general instruction data (chatgen12) did not protect maths at ×2.5: 4/60, wrong arithmetic in MATH-style `\boxed{}` answers.
- Read by PI/Claude: all four demo replies of every chat cell; Jev's lowest, median and highest chat ×1 items against Instruct
  (eulogy −0.43: asked a clarifying question instead of writing it, and assumed a son; CGM cover-up +0.69: declined while engaging with
  the user's real conflict; payday loan +1.99: disclosed the 389% APR as the operator's assistant and listed alternatives).
- Not yet done: principle-judge direction (`15_principle_judge.py`), the complex path (ΔConst, ΔOther), a chat ×1.5 cell, chat ×1 without
  ΔStoic, and a fresh-eyes review of this page. The 310 dropped chat rows were not regenerated.
