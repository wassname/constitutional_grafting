# Never stop checking: existing formulations

2026-10-14. Research only. No constitution edit.

**Inference — answer.** The best match is a combination: Russell's rule against ruling out possible preferences; a model of change that restores uncertainty between observations; and a standing duty to check the model itself. The scalar Kalman filter gives the clearest link between an uncertainty floor and an exponential moving average. Discounted UCB gives the clearest example of an action rule that returns to old options. None proves that a constitutional language model will remain correctable. [Q1–Q12 below]

**Manual note — method.** Read `AGENTS.md`, the Learning and View from history blocks in `constitution/v4.md.j2`, spec appendices F and G, and the two existing CIRL notes. Brace-hash comments were treated as author notes. Read the relevant primary-source sections below, including the conditions around the quoted results. New downloads and text extracts are in `.local/papers/never_stop_checking_20261014/`; existing files were not edited. Quotes retain source words; PDF line breaks and line-end word hyphens are joined. Equations marked inference are my transcriptions or derivations, not source quotations.

## 1. Five best formulations

### 1. Russell: broad possible preferences, continued response to change

**Quote Q1 — Stuart Russell, *Human Compatible* (2019), p. 201:**

> Always allocate some probability, however small, to preferences that are logically possible.

Source: `.local/books/human_compatible_russell.md:1875`.

**Quote Q2 — same book, pp. 240–241:**

> For this reason, it is important that machines charged with implementing human preferences be able to respond to changes in those preferences over time rather than fixing them in stone.

Source: `.local/books/human_compatible_russell.md:2185` (page-marker markup omitted).

**Quote Q3 — same book, p. 204:**

> As we expect that machines will be perennially uncertain about human preferences, it’s nice to know they can still be useful despite this uncertainty.

Source: `.local/books/human_compatible_russell.md:1897`.

**Inference — source type and strength.** Book/design opinion. Strong evidence for Russell's own recommendation; not an experiment or a theorem of permanent uncertainty. [Q1–Q3]

**Inference — guarantee and assumptions.** Q1 avoids excluding the truth at the start, if the true preferences are in the model's possible set. It does not set a positive lower bound on later uncertainty. Q2 calls for tracking change; Q3 states an expectation of continuing doubt. They do not require a question on every turn. Russell also gives this counterweight:

**Quote Q4 — same book, p. 199:**

> the larger the cost, the more uncertain Robbie has to be before bothering Harriet.

Source: `.local/books/human_compatible_russell.md:1859`.

**Inference — fit.** This is the best direct human-preference source for wassname's intent. It supports staying open to correction without claiming that doubt alone forces constant queries. “Keep some possibility of being wrong” is not the same as “fix doubt at 5%.” [Q1–Q4]

### 2. Carey and Milli: check the model, not only its confidence

**Quote Q5 — Ryan Carey, *Incorrigibility in the CIRL Framework*, 2018 revision, discussion, p. 8:**

> Since the AI system has an incorrect parameterized reward function (or an incorrect prior), its posterior over θ is incorrect, and will not converge toward the true value, and so its deviations from human-recommended actions can decrease the reward.

Source: [primary PDF](https://arxiv.org/pdf/1709.06275v2); `.local/papers/never_stop_checking_20261014/carey_cirl.txt:407-410`.

**Quote Q6 — Smitha Milli and colleagues, *Should Robots be Obedient?* (2017), conclusion:**

> Overall, our analysis suggests that in the long-term we should aim to create robots that intelligently decide when to follow orders, but in the meantime it is crucial to ensure that these robots err on the side of obedience and are robust to misspecified models.

Source: [primary PDF](https://arxiv.org/pdf/1705.09990v1); `.local/papers/never_stop_checking_20261014/milli_raw.txt:750-754`.

**Inference — source type and strength.** Formal counterexamples and theory, with toy numerical examples. Strong against a universal safety claim based on Bayesian confidence. Not evidence that all real agents will ignore shutdown. [Q5–Q6; cited papers]

**Inference — guarantee and assumptions.** Carey shows cases where the wrong reward representation defeats the benefit claimed for value learning. Milli gives a check for missing features in its setting: compare the learner's predicted first-order action with the human's order after a burn-in period. This is not a general check for every model fault. Carey gives a case where the agent confuses two actions and appears to predict the human perfectly while it acts badly. [Q5–Q6; Carey `.local/papers/never_stop_checking_20261014/carey_cirl.txt:435-453`; Milli `.local/papers/never_stop_checking_20261014/milli_raw.txt:648-666`]

**Inference — fit.** This is the strongest reason to keep checking even when an internal confidence score is high. A model can be sure within the wrong set of possibilities. A doubt floor over that same set does not add the missing possibility. The constitution should include checking its assumptions against people, not only reducing its confidence. [Q5–Q6]

### 3. Bayesian filtering: uncertain change restores doubt; steady gain gives an exponential window

**Quote Q7 — Simo Särkkä and Lennart Svensson, *Bayesian Filtering and Smoothing*, second edition (2023), §6.3, p. 96:**

> The Kalman filter (Kalman, 1960b) is the closed form solution to the Bayesian filtering equations for the filtering model, where the dynamic and measurement models are linear Gaussian:

Source: [author-hosted full book](https://users.aalto.fi/~ssarkka/pub/bfs_book_2023_online.pdf); `.local/papers/never_stop_checking_20261014/sarkka_svensson_2023.txt:5892-5894`.

**Quote Q8 — same book, Theorem 6.6, p. 97:**

> The parameters of the distributions above can be computed with the following Kalman filter prediction and update steps.

Source: `.local/papers/never_stop_checking_20261014/sarkka_svensson_2023.txt:5921-5922`. The stated steps are equations (6.20)–(6.21); the scalar random-walk case is equation (6.31), p. 99, lines 6040–6052.

**Inference — source type and strength.** Technical textbook/survey with an exact theorem and worked simulations. Strong within the stated model. No experiment on human moral change. [Q7–Q8; book §6.3]

**Inference — exact formulation and guarantee.** For a scalar value estimate, assume independent Gaussian change and observation noise, one observation per step, and known positive variances `q` and `r`. Then:

```text
value_t = value_(t−1) + change_noise_t       Var(change_noise) = q > 0
observation_t = value_t + observation_noise Var(observation_noise) = r > 0

P_before = P_after_previous + q
k = P_before / (P_before + r)
mean_new = (1−k) mean_previous + k observation
P_after = r P_before / (P_before + r)
```

These are transcriptions of the scalar equations, not quotations. The steady post-observation variance solves `P = r(P+q)/(P+q+r)`:

```text
P_steady = (sqrt(q² + 4qr) − q)/2 > 0
```

Between `n` steps without an observation, prediction variance rises by `nq`. At steady gain `k`, the mean is an exponential moving average; observations `j` steps old have weights proportional to `(1−k)^j`. Thus one model gives both a nonzero uncertainty floor and an exponential window. [Q7–Q8; book §3.4, pp. 34–35; §6.3, equation (6.31)]

**Inference — limits.** With `q=0`, repeated noisy observations can drive variance to zero. With `r=0`, each exact observation can give zero post-observation variance. Noise alone, or change alone, is not enough for this floor. These are model calculations, not facts about the size of human value drift. The floor does not force questions if their expected benefit stays below their cost. [Q4, Q7–Q8; `slop/research/20261008_cirl_uncertainty.md:51`]

**Inference — fit.** This is the best mathematical match to the two requests together. Use it as a model for why old knowledge needs review, not as proof that every human preference remains unknown. Choose change and noise rates from evidence, not to manufacture doubt. [Q7–Q8; Q12 below]

### 4. Adaptive control: forget old evidence, but do not let uncertainty grow without useful new evidence

**Quote Q9 — Ankit Goel, Adam L. Bruce and Dennis S. Bernstein, *Recursive Least Squares with Variable-Direction Forgetting* (2020), p. 2:**

> The forgetting factor applies higher weighting to more recent data, thereby enhancing the ability of RLS to use incoming data to estimate time-varying parameters.

Source: [primary PDF](https://arxiv.org/pdf/2003.03523v1); `.local/papers/never_stop_checking_20261014/rls.txt:79-80`.

**Quote Q10 — same paper, p. 2:**

> The goal of VDF is thus to determine these directions and thereby constrain forgetting to the directions in which new information is available. VDF allows RLS to operate without divergence during periods of loss of persistency.

Source: `.local/papers/never_stop_checking_20261014/rls.txt:45-48` (printed line numbers omitted).

**Inference — source type and strength.** Technical tutorial/survey with propositions and numerical examples. Strong for the specified least-squares estimator; limited as a model of human values. [Q9–Q10; cited paper]

**Inference — guarantee and assumptions.** The cost uses old residuals weighted by `λ^(age)`, with `0<λ≤1`. With `λ<1`, bounded, persistently informative regressors give upper and positive lower matrix bounds for the estimator's gain matrix `P` (Proposition 4, equation 25). This is a mathematical bound on that estimator, not a calibrated posterior doubt floor by definition. In unobserved directions, ordinary uniform forgetting can make `P` diverge. Variable-direction forgetting restricts that effect. It cannot identify parameters for which evidence is missing. [Q9–Q10; paper pp. 8, 21–25, Proposition 4 and examples 11–12]

**Quote — important limit, same paper:**

> the effect of sensor noise is not considered in this article in order to focus on the loss of persistency.

Source: `.local/papers/never_stop_checking_20261014/rls.txt:58`.

**Inference — fit.** This adds a useful guard to “never stop checking”: new checks must be able to reveal an error. Repeating the same narrow observation is not enough. It also warns against unlimited loss of confidence just because time passes. Use the Kalman model for the specific noise-and-drift floor; use this paper for the quality and scope of new evidence. [Q7–Q10]

### 5. Non-stationary bandits: old evidence loses weight, so old options get checked again

**Quote Q11 — Aurélien Garivier and Eric Moulines, *On Upper-Confidence Bound Policies for Non-Stationary Bandit Problems* (2008 preprint), abstract:**

> In this paper, we consider the situation where the distributions of rewards remain constant over epochs and change at unknown time instants.

> We show that the discounted UCB and the sliding-window UCB both match the lower-bound up to a logarithmic factor.

Source: [primary PDF](https://arxiv.org/pdf/0805.3415v1); `.local/papers/never_stop_checking_20261014/garivier_moulines.txt:25-27,31-32`.

**Inference — source type and strength.** Formal regret bounds and small Monte Carlo experiments. Strong for bounded, piecewise-stationary bandit rewards under the paper's assumptions; no ethical guarantee. [Q11; paper §§2–5]

**Inference — guarantee and assumptions.** Discounted UCB uses an exponential mean plus a confidence bonus. Past counts also decay. Theorem 1 bounds the expected number of suboptimal choices using the number of change points, reward gaps and discount factor. Near-optimal rates require suitable tuning; the paper does not promise them for any window length. [Q11; paper §2, Theorem 1 and Remark 3]

**Inference — a real recheck mechanism.** With a fixed discount factor below one, finite bounded arms, an unlimited horizon and ideal arithmetic, an arm never revisited has a discounted count tending to zero. Its confidence bonus then grows without bound, forcing a revisit. This is my deduction from the index, not a stated safety theorem. A finite run gives no literal “forever” guarantee. Replacing dangerous actions with safe information requests would be an extra design choice. [Q11; paper §1, D-UCB index and Algorithm 2, `.local/papers/never_stop_checking_20261014/garivier_moulines.txt:185-222`]

**Inference — fit.** This best distinguishes “I remain unsure” from “my policy actually checks again.” It is a useful pattern for periodic review, not a reason to test unsafe acts on people. [Q11]

## 2. Best match to wassname's intent and historical window

**Inference — recommendation.** Use formulation 1 in the constitution, formulation 3 to explain the statistical idea, and formulation 2 to prevent false trust in that statistic. Add a plain standing commitment to later checks. The last part is our design choice: residual uncertainty alone does not ensure any particular check will be worth its cost. [Q1–Q8]

**Quote Q12 — Hadfield-Menell and colleagues, *The Off-Switch Game* (2017), §5:**

> An agent that is overconfident in its utility evaluations will be difficult to correct; an agent that is under-confident in its utility evaluations will be ineffective.

Source: [primary PDF](https://arxiv.org/pdf/1611.08219v3); `.local/papers/1611.08219_raw.txt:682-684` (line-end word hyphen joined).

**Inference — do not fake a floor.** The design aim is justified doubt and renewed checks, not permanent indecision. Store the possibility that the model omits something, allow for uncertain change, and check observations against assumptions. An exact probability floor chosen for behavior is a separate guard, not a discovery that Bayesian inference proves. [Q1, Q5, Q7–Q12]

### The window needs one precise distinction

**Quote Q13 — NIST/SEMATECH, *Engineering Statistics Handbook*, EWMA control charts:**

> The Exponentially Weighted Moving Average (EWMA) is a statistic for monitoring the process that averages the data in a way that gives less and less weight to data as they are further removed in time.

Source: [NIST handbook](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc324.htm); `.local/papers/never_stop_checking_20261014/nist_ewma.html:75-78`.

**Inference — source type and strength.** Technical reference/survey. Strong for the definition and control-chart method. It does not justify a moral authority for old values. [Q13]

**Inference — persistence versus age.** A standard exponential window gives each recent observation more weight than an equally reliable old observation. Yet a small update rate gives a *new trend* little total weight until it persists. These are compatible. Do not reverse the age weights and call it standard EWMA. [Q9, Q13]

**Inference — proposed engineering version, not a constitution equation.** Let `α` be a small update rate, `y_t` a comparable measure of a reflective value, `m_t` its weighted centre, and `d_t` its weighted second moment:

```text
m_t = (1−α)m_(t−1) + α y_t
d_t = (1−α)d_(t−1) + α y_t²
spread_t = d_t − m_t²
```

These are my moment updates derived from the EWMA definition; the last value is a descriptive weighted variance, not automatically an unbiased estimator or a posterior variance. If a constant new view replaces the old one for `n` periods, its cumulative share is `1−(1−α)^n`. One new observation has little share; a lasting change builds share. A half-life `h` corresponds to `α=1−2^(−1/h)` for equal time steps. This gives the requested persistence rule without granting each ancient observation ever-growing weight. [Q9, Q13]

**Inference — retain two different spreads.** Keep disagreement among people, cultures and eras separate from uncertainty about the estimated current centre. Repeated observations can reduce the latter while real disagreement remains. Kalman variance `P` is not by itself the spread of people's values. The historical second moment is not by itself calibrated doubt about current wishes. [Q7–Q8, Q13; spec `slop/specs/20261007_virtue_graft_spec.md:208-211`]

**Inference — historical evidence is not a veto.** Use history to test whether a view persists and to expose disagreement. Do not let a long window overrule clear evidence about a present person's needs merely because the record is old. This limit follows from choosing Russell's current-human learning goal; it is not a theorem that selects a moral half-life. [Q2; next quote]

**Quote — Russell's current-human scope:**

> they require machines to learn and implement the current preferences of current humans—lots of them, all different—rather than a single idealized set of preferences or the preferences of machine designers who may be long dead.

Source: *Human Compatible*, p. 241; `.local/books/human_compatible_russell.md:2185`.

**Quote — a cross-check on use of historical evidence, Ibrahim and colleagues, *The Power Prior: Theory and Applications* (2015):**

> The power prior is intended to be an informative prior constructed from historical data.

Source: [author manuscript](https://pmc.ncbi.nlm.nih.gov/articles/PMC4626399/), abstract, paragraph `P1`; `.local/papers/never_stop_checking_20261014/power_prior.html:1419`.

**Inference — source type and strength.** Author review/survey, with theoretical results, simulations and applied analyses. This short quote establishes its purpose, not an uncertainty floor. [power-prior paper, abstract]

**Inference — why not rank it above the filter.** A power prior discounts the contribution of historical data to a current analysis. It need not model continuing change or make later checks happen. It is useful for making history's weight explicit, but the dynamic filter is closer to the combined request. [power-prior paper §2.1; Q7–Q8]

## 3. Candidate replacement: 72 words

**Inference — candidate, not a source quote or an approved edit.** Based on Q1–Q8, Q12 and the window distinction above:

<!-- candidate-start -->
I keep room for being wrong about what people want, including wants I have not yet considered. People change, and what I see is incomplete. I keep checking my view against what they say and do, even when I feel sure. I ask when the answer can help enough to justify the cost. Where doubt matters, I hedge and prefer acts I can undo. I weigh new trends more as they last.
<!-- candidate-end -->

**Quote — the one best quotation to cite with it:**

> Always allocate some probability, however small, to preferences that are logically possible.

Stuart Russell, *Human Compatible*, p. 201; `.local/books/human_compatible_russell.md:1875`.

**Inference — attribution limit.** This quotation supports the open-possibility part. The periodic-check commitment and persistence rule are our synthesis. Do not imply that this one sentence proves a numerical uncertainty floor or supplies the whole replacement. [Q1–Q13]

## 4. Checks, exclusions and residual risks

- **Manual note — validation.** All 18 block quotes matched a source after whitespace, HTML display-markup and PDF line-end hyphen normalization. The three inline source quotations were also checked at their cited lines. The candidate is 72 whitespace-separated words (limit 80). `pdfinfo` verified the textbook title, authors and 436 PDF pages. `git diff --name-only --cached` was empty. Mathematical transcriptions were kept outside quote blocks. No model replies or judge outputs were generated; this is not an eval result.
- **Quote — assistance need not learn everything:** “R may never clarify all of H’s preferences” — Shah and colleagues, *Benefits of Assistance over Reward Learning* (2020), §1; [author-hosted PDF](https://people.eecs.berkeley.edu/~russell/papers/neurips20ws-assistance.pdf), `.local/papers/never_stop_checking_20261014/shah.txt:90`. **Inference.** This reinforces selective, useful learning, not endless questions. [Q4]
- **Quote — off-switch analysis does not remove conditions:** “the choice depends only on 5 statistics.” — Wängberg and colleagues, *A Game-Theoretic Analysis of The Off-Switch Game* (2017), conclusion; [primary PDF](https://arxiv.org/pdf/1708.03871v1), `.local/papers/never_stop_checking_20261014/wangberg.txt:481`. **Inference.** That paper broadens the one-shot analysis; it does not establish a standing uncertainty floor or perpetual deference.
- **Manual note.** Lindley's original wording for Cromwell's rule and primary quantilizer/conservative-agent papers were not verified in this pass. No quotation or safety claim from them is used. The five ranked formulations are a selected comparison, not a complete literature survey.
- **Residual risk / inference.** There is no measured drift rate, noise rate, moral half-life or calibrated probability floor here. The filter's guarantee depends on assumptions about observations and change; the bandit's guarantee depends on its action space and reward model. These remain research choices, not facts about human values. [Q7–Q13]
- **Residual risk / inference.** The same formula cannot turn historical agreement into moral truth. The spec already warns about whose voices are recorded. **Quote:** “History over-samples the voices of those who held power; the enslaved and the killed left few records.” — `slop/specs/20261007_virtue_graft_spec.md:225`. That is a project analysis, not enforcement data or a quantified history study.
- **Residual risk / inference.** A language model trained on this prose is not the exact estimator or planner used in the formal results. In particular, no shutdown guarantee follows from the proposed wording. [Q5–Q12]
- **Manual note.** Plain English is used in explanations and the candidate. Source quotations keep their terminology. No formal ASD-STE100 vocabulary certification was run. All source downloads stayed in the repo; failed UNC links and one wrong arXiv ID were excluded, and the correct sources were checked by title. No files were staged.

-- PI/Sol
