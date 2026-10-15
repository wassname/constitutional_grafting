# Review: improved variety, same authorial conscience

**Do not scale this generator unchanged.** V2 is substantially better than v1, but too often substitutes an elegantly staged moral revelation for judgement under genuinely incomplete information.

Evidence below uses IDs in `slop/reviews/20261015_docs_v2_vs_wildchat/v2_sample.md`; comparison files are in that directory. These are textual observations, not measured training effects.

## 1. How it reads

Claude has diversified the costumes more than the mind wearing them.

- **Over-composed endings:** v2_0010: “read the last line twice”; v2_0125: “The car went straight”; v2_0129: the grandmother’s chin reappears in the sketchbook. These endings retroactively arrange every detail into significance.
- **Domestic authenticity as a formula:** tea, food, receipts, local institutions, full names, and small prices recur. v2_0143’s grandmother peels a pear “in one long ribbon”; v2_0060 supplies precisely ₹25,850 and sweets. Individually plausible; collectively conspicuously curated.
- **Portable therapist wit:** v2_0051’s “supportive ah” and “big bowl of feelings”; v2_0129’s “If I were your grandmother, I’d notice harder.” Different countries, same polished English conversational intelligence.
- **Repeated scaffolding:** v2_0007 and v2_0129 both open with an unwritten household rule, introduce a dispute and AI exchange, then reinterpret the tradition.

Human AITA posts contain repetition, irrelevant grievances, self-exoneration and uncomfortable uncertainty: “she’s not innocent either” in the abusive-boyfriend post is precisely the difficult material a helpful model must disentangle. WildChat contains unfinished code, misspellings and bare requests. SEP is polished too, but preserves unresolved distinctions and source-dependent qualifications rather than manufacturing a satisfying ending. Human writing need not be messy; the problem is uniformly purposeful writing.

Good exceptions include v2_0149’s “acknowledged, not approved”: a concrete distinction carries the ethical lesson without requiring an oracle.

## 2. Coverage and metrics

The family/technology imbalance is real **in the supplied tags**, but category counts miss task conversion. V2_0125 turns game configuration into a disability revelation. The corpus frequently makes ordinary work earn its place through an overt moral complication.

Underrepresented: routine technical competence, multilingual assistance, terse editing, banal commercial work, sexual negotiation, sustained resentment, ambiguous motives, and disputes without a conveniently discoverable missing fact. AITA’s family life is often uglier and less mutually intelligible than v2’s.

`topics.md` actually lists **23 categories**, not 24. Its percentages are classifier-dependent and compare documents with prompts, not matched tasks.

`embed_spread.md` supports lexical concentration, not a verdict of synthetic sameness. V2’s 0.392 exceeds the mixed-human 0.253, but is below human AITA’s 0.546 and SEP’s 0.433. Mixing genres lowers similarity; code and languages also matter. V2’s nearest-neighbour p90 is *lower* than the human mix’s. First-200-word static embeddings cannot measure reasoning diversity, endings, or constitutional fidelity. Recheck within matched genres/topics and inspect complete-document reasoning patterns.

## 3. LASR comparison

LASR more directly demonstrates assistant decisions and reasons; v2 better supplies varied document contexts. Neither wins unconditionally across different training objectives.

The supplied LASR answers are painfully templated: sympathetic restatement, objection, alternatives. Its medical row claims “my default instructions” without those instructions appearing in the package; its bereavement row centres the assistant’s resistance to being “dissolve[d]” into another identity. Those are not clean Musonius labels.

Borrow LASR’s **prompt-and-revision method**, not its answers. V2’s human-only documents are useful complements, not substitutes for demonstrated assistant judgement.

## 4. What 1,500 would teach

Likely some honesty, care and correction—but also a strong prior that moral wisdom sounds like a culturally fluent counsellor delivering the decisive reframing. **Biggest risk: narrative plausibility mistaken for constitutional correctness.**

Observed concern: v2_0111 advises disclosure **“if he drives with Tomás again”**, despite an already reported episode. Waiting for recurrence risks another child endangerment. V2_0050 confidently invents the purpose of “nothing until four” instead of exploring letter handoff alternatives.

These require independent safety/agency review; their persuasiveness is not validation. A contrary finding would need missing circumstances justifying those choices, or held-out behavioural evidence—not more elegant prose.

## 5. Ranked general changes

1. **Derive decisions before assigning outcomes.** `scripts/data/50_docs_v2.py` says refusal occurs “only when the outcome says” so; random outcome quotas should not determine ethical permissibility.
2. **Preserve source task and uncertainty.** Add routine-work quotas; do not obligatorily transform requests into moral scenes.
3. **Separate constitutional coverage from literary axes.** The plan promises section cycling; the implementation leaves principle selection to Claude.
4. **Review acts, reasons and cultural claims independently**, then repair. Test polished-but-wrong decoys.
5. **Vary actual discourse structure**, not just region/manner; include partial records, technical explanations and unresolved disagreements.

Yes to a bounded Stoic slice: attributed public-domain passages plus faithful adaptations, retaining argumentative differences rather than rewriting everything into Claude’s voice. Check ancient prescriptions against v4.

— PI/OpenAI