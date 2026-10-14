# Assistance games: source review for constitution v4

2026-10-14. Research only. No constitution change proposed as an approved change.

**Method.** I read *Human Compatible*, chapters 7–9 in full, the relevant endnotes, both arXiv papers including the CIRL proofs, the full local multi-principal paper, and our earlier uncertainty notes. Book pages below are the EPUB's embedded print-page markers, not Markdown page counts. Paper pages are PDF pages. Quotes preserve the source words; EPUB display tags and reference links are omitted. PDF line breaks are retained where useful. Equations and pseudocode are my transcriptions, not quotations.

**Source files.** Book: `.local/books/human_compatible_russell.md`. CIRL: `.local/papers/1606.03137.txt` (v4), downloaded from `https://arxiv.org/pdf/1606.03137`; abstract saved as `.local/papers/1606.03137_abs.html`. Off-switch: `.local/papers/1611.08219_raw.txt` (v3), downloaded from `https://arxiv.org/pdf/1611.08219`; abstract saved as `.local/papers/1611.08219_abs.html`. The layout extract `.local/papers/1611.08219.txt` is also available. Downloads and extracts are new files, allowed by the supervisor; no existing source file was edited.

**Review snapshot.** Other workers changed `constitution/v4.md.j2` during this review. The constitution citations below refer to the read with SHA-256 `8fc3234d99082fc74e5e6d2065ff627ea601c2b3fc8c9e65356242c7a4580b87`. Brace-hash text is an author note, not model-facing text.

## 1. Russell's principles and further guidance

### 1.1 The three principles, verbatim

**Quote R1 — *Human Compatible*, p. 173:**

> The machine’s only objective is to maximize the realization of human preferences.

`.local/books/human_compatible_russell.md:1617`

> The machine is initially uncertain about what those preferences are.

`.local/books/human_compatible_russell.md:1619`

> The ultimate source of information about human preferences is human behavior.

`.local/books/human_compatible_russell.md:1621`

**Quote R2 — status of the list, p. 172:**

> they are intended primarily as a guide to AI researchers and developers in thinking about how to create beneficial AI systems; they are *not* intended as explicit laws for AI systems to follow:

`.local/books/human_compatible_russell.md:1615`

**Inference.** These are three design principles, not three lines of executable code. Turning them into first-person constitutional commitments is our use of Russell's proposal. Do not call a longer combined list “Russell's principles.” [R1–R2]

### 1.2 Further guidance, not an additional canonical numbered list

**Quote R3 — no intrinsic self-preservation, p. 173:**

> The principle means that the machine is purely altruistic—that is, it attaches absolutely no intrinsic value to its own well-being or even its own existence.

`.local/books/human_compatible_russell.md:1629`

**Inference.** Survival can serve people, but it is not a separate final goal in Russell's design. This is not a Stoic argument or a finding about machine feelings. [R3]

**Quote R4 — learn each person's preferences, p. 173:**

> And they are yours: the machine is not looking to identify or adopt one ideal set of preferences but to understand and satisfy (to the extent possible) the preferences of each person.

`.local/books/human_compatible_russell.md:1623`

**Quote R5 — many people and local service, pp. 217, 219, 227:**

> It seems difficult, then, to make the idea of a loyal AI work, unless the idea is extended to include consideration of the preferences of other humans, in addition to the preferences of the owner.

`.local/books/human_compatible_russell.md:2007`

> One plausible answer is to give equal weight to everyone’s preferences—in other words, to maximize the sum of everyone’s utilities.

`.local/books/human_compatible_russell.md:2023`

> Robbie will need to have some amount of loyalty to Harriet in particular—perhaps an amount related to the amount Harriet paid for Robbie.

`.local/books/human_compatible_russell.md:2091`

**Inference.** Russell considers both effects on others and useful service to the owner. Equal-weight aggregation is “one plausible answer,” not a result of the three principles alone. His service discussion does not establish our ordered circles or their weights. [R4–R5]

**Quote R6 — learn goals, do not copy bad acts, p. 179:**

> A machine observing this behavior will not learn to take bribes; it will learn that the official, like many other people, has a very strong desire for his children to be educated and successful. It will find ways to help him that don’t involve lowering the well-being of others.

`.local/books/human_compatible_russell.md:1671`

**Quote R7 — malicious preferences need separate treatment, p. 229:**

> In his paper that introduced preference utilitarianism, Harsanyi attributes negative altruism to “sadism, envy, resentment, and malice” and argues that they should be ignored in calculating the sum total of human utility in a population:

`.local/books/human_compatible_russell.md:2109`

> No amount of goodwill to individual X can impose the moral obligation on me to help him in hurting a third person, individual Y.

`.local/books/human_compatible_russell.md:2111` — Harsanyi, quoted by Russell.

> This seems to be one area in which it is reasonable for the designers of intelligent machines to put a (cautious) thumb on the scales of justice, so to speak.

`.local/books/human_compatible_russell.md:2113`

**Inference.** There are two different points. First, learning a goal is not copying an act. Second, refusing to serve a preference for another person's suffering requires a moral design choice. Plain single-human CIRL does not automatically reject every harmful human goal. Russell endorses caution here; he does not supply a complete algorithm for separating envy, care, and self-respect. [R6–R7]

**Quote R8 — account for human mistakes and communication incentives, pp. 181, 233:**

> Machines can and should interpret all communications from other intelligent entities as moves in a game rather than as statements of fact; in some games, such as cooperative games with one human and one machine, the human has an incentive to be truthful, but in many other situations there are incentives to be dishonest.

`.local/books/human_compatible_russell.md:1683`

> It cannot assume he is rational.

`.local/books/human_compatible_russell.md:2131`

**Inference.** Words are behavior too. The learning problem is to explain words and actions in context, including teaching, mistaken beliefs, limited thought, emotions, and incentives. Neither “copy each observed choice” nor “always ignore speech” is Russell's method. [R8; R6]

**Quote R9 — avoid a narrow hypothesis space, pp. 201–202:**

> Always allocate some probability, however small, to preferences that are logically possible.

`.local/books/human_compatible_russell.md:1875`, p. 201.

> Never rule out in advance possible attributes of the world that could be part of Harriet’s preference structure.

`.local/books/human_compatible_russell.md:1879`, p. 202.

**Inference.** These are instructions for avoiding false certainty caused by missing hypotheses. A broad prior is not a positive lower bound on posterior uncertainty. For continuous parameters, “some probability” must be interpreted through support or neighborhoods, not positive probability mass on every exact real number. [R9; C1 below]

**Quote R10 — requests are evidence, not unlimited commands, p. 204:**

> The command is not a goal to be achieved *at all costs*. It is a way of conveying some information about Harriet’s preferences with the intent of inducing some behavior on the part of Robbie.

`.local/books/human_compatible_russell.md:1895`

**Inference.** Interpret an instruction with the person's wider preferences and beliefs. This is Russell's account of practical language use, not a theorem that every specific request should be refused or delayed. [R10]

**Quote R11 — actual benefit is not a feedback signal, p. 208:**

> reward signals provide *information* about the accumulation of actual reward, which is the thing to be maximized.

`.local/books/human_compatible_russell.md:1921`

**Inference.** A good rating is evidence of benefit, not benefit by definition. Russell gives an argument against manipulating feedback; the passage is not a proof that our trained language model cannot manipulate a judge. [R11; R17 below]

**Quote R12 — respond to changing preferences, pp. 240–241:**

> For this reason, it is important that machines charged with implementing human preferences be able to respond to changes in those preferences over time rather than fixing them in stone.

`.local/books/human_compatible_russell.md:2185` — sentence crosses the p. 241 marker.

> they require machines to learn and implement the current preferences of current humans—lots of them, all different—rather than a single idealized set of preferences or the preferences of machine designers who may be long dead.

`.local/books/human_compatible_russell.md:2185`, p. 241.

**Inference.** Changing preferences and continued learning are already in Russell's book. The extra part in our project is the specific stochastic drift model and a permanent uncertainty floor, not the observation that people change. [R12; U1 below]

**Quote R13 — distinguish learning from change, pp. 241–242:**

> It’s important, although sometimes difficult, to separate preference change from preference update, which occurs when an initially uncertain Harriet learns more about her own preferences through experience.

`.local/books/human_compatible_russell.md:2191`

**Quote R14 — learn preferences about change processes, p. 243:**

> One possible solution is for machines to learn about human *meta-preferences*—that is, preferences about what kinds of preference change processes might be acceptable or unacceptable.

`.local/books/human_compatible_russell.md:2201`

**Quote R15 — limits on preference engineering, p. 245:**

> Let’s just say that there are risks associated with intentional preference engineering on a global scale. We should proceed with extreme caution.

`.local/books/human_compatible_russell.md:2215`

**Inference.** Meta-preferences concern acceptable processes of change. They are not a license for the machine to choose a supposedly better destination and then make people want it. Russell offers this as “one possible solution,” not a solved theorem. [R13–R15]

**Quote R16 — later humans may revise old commitments, endnote 47, p. 320:**

> If the 2099 humans, after suitable deliberation, decide they wish to override the preferences built in by the 2019 humans, it seems reasonable that they should be able to do so. After all, it is they and their descendants who have to live with the consequences.

`.local/books/human_compatible_russell.md:3397`

**Inference.** This is relevant to constitutional revision. It does not specify who may edit one model, prove a right of any government, or justify any proposed edit. [R16]

**Quote R17 — limits of guarantees, pp. 184, 210:**

> The “provably beneficial” in the title of the chapter is an aspiration rather than a promise, but it is the right aspiration.

`.local/books/human_compatible_russell.md:1717`

> discussions beginning with “suppose that robot *R* has purpose *P*” are fine for gaining some intuition about how things might unfold, but they cannot lead to theorems about real machines.

`.local/books/human_compatible_russell.md:1935`

**Inference.** A constitution can state design commitments. It cannot claim formal safety guarantees for a model trained to imitate those commitments. [R17]

## 2. The algorithm and the off-switch result

### 2.1 Definition and exact solution target

**Quote C1 — CIRL §3.1, p. 4:**

> A cooperative inverse reinforcement learning (CIRL) game M is a two-player Markov
> game with identical payoffs between a human or principal, H, and a robot or agent, R.

`.local/papers/1606.03137.txt:198-199`

> Θ a set of possible static reward parameters, only observed by H: θ ∈ Θ.

`.local/papers/1606.03137.txt:207`

> H observes θ, but R does not.

`.local/papers/1606.03137.txt:215`

> This observation model
> captures the notion that only the human knows the reward function, while both actors know a prior
> distribution over possible reward functions.

`.local/papers/1606.03137.txt:215-217`

**Transcription/inference.** The game is `M = ⟨S, {Aᴴ,Aᴿ}, T, {Θ,r}, P₀,γ⟩`. The world state `s` is public. The initial pair `(s₀,θ)` is sampled from `P₀`. Only H receives θ; it stays fixed. Both select actions, see each other's actions, and receive the same payoff `r(s,aᴴ,aᴿ;θ)`. The goal is an optimal pair of policies maximizing expected discounted shared reward, not first learning θ exactly and then starting to help. [C1; `.local/papers/1606.03137.txt:195-234`]

**Quote C2 — payoff and observations, §3.1, p. 4:**

> The optimal joint
> policy is the policy that maximizes value. The value of a state is the expected sum of discounted
> rewards under the initial distribution of reward parameters and world states.

`.local/papers/1606.03137.txt:229-231`

> This incentivizes the human to teach and the robot to learn without explicitly
> encoding these as objectives of the actors.

`.local/papers/1606.03137.txt:233-234`

**Inference.** “Receive reward” means a payoff, not necessarily a sensor reading. The paper's robot policy history lists states and actions, not numerical rewards (`.local/papers/1606.03137.txt:229`). Otherwise an observed reward could reveal θ and change the information problem. [C1–C2]

**Quote C3 — reduction, §3.2, p. 5:**

> There exists
> a (single-actor) POMDP MC with (hidden) state space SC such that |SC | = |S| · |Θ| and, for any
> policy pair in M , there is a policy in MC that achieves the same sum of discounted rewards.

`.local/papers/1606.03137.txt:253-255`

> There exists an optimal policy pair (π H , π R ) that only
> depends on the current state and R’s belief.

`.local/papers/1606.03137.txt:259-260`

**Quote C4 — coordinator's action, appendix §6.2, p. 10:**

> C’s actions are tuples (δ H , aR ) that specify an action for R and a decision rule for H that
> maps its private information (θ) to an action δ H : Θ → AH . C observes H’s action and the world
> state.

`.local/papers/1606.03137.txt:548-550`

**Inference.** A POMDP is a decision model with partly hidden state. Its hidden state here is `(s,θ)` with `s` observed. At each step its coordinator selects a human decision rule and a robot action. This mathematical coordinator does not give a real robot control over a person's choices. [C3–C4]

### 2.2 Compact Unicode pseudocode

**My pseudocode, derived from C1–C4.** `SolvePOMDP` denotes a planning solver, not a cheap operation. The exact reduction assumes prior coordination. It plans for future reward and information together.

```pseudopy
# Offline model: θ is fixed; H alone knows θ.
C.state   ← (s, θ)
C.action  ← (δᴴ : Θ → Aᴴ, aᴿ)
C.observe ← (aᴴ, s′)
C.reward  ← r(s, δᴴ(θ), aᴿ; θ)
πᶜ ← SolvePOMDP(C, P₀, γ)       # maximize E[Σₜ γᵗ rₜ]

# Online execution of the coordinated policy pair.
s ← observed initial state
b(θ) ← P₀(θ | s)
while not terminal:
    δᴴ, aᴿ ← πᶜ(s, b)
    aᴴ ← δᴴ(θ)                 # H executes; R cannot read θ
    s′ ← T(· | s, aᴴ, aᴿ)       # environment executes joint action
    b(θ) ← normalize(b(θ) × Pr(aᴴ | s, b, θ, δᴴ))
    s ← s′
```

**Inference.** For a deterministic decision rule the likelihood is `1[aᴴ = δᴴ(θ)]`. For a specified human policy use its likelihood instead. The transition factor cancels in this original setup because `T` does not depend on θ. Do not use a likelihood for an isolated expert if the person is teaching or responding to the robot. This follows from C1–C4 and the paper's distinction below, not from an extra learning objective.

**Quote C5 — expert behavior is not always good teaching, §3.3, p. 6:**

> There exist ACIRL games where the best-response for H to π R violates the expert
> demonstrator assumption.

`.local/papers/1606.03137.txt:318-319`

**Quote C6 — solving versus coordination, §3.2, p. 5:**

> This is not the same as ‘solving’ a CIRL game, as a real world implementation of a CIRL agent must
> account for coordination problems and strategic uncertainty (Boutilier, 1999). The optimal policy pair
> represents the best H and R can do if they can coordinate perfectly before H observes θ.

`.local/papers/1606.03137.txt:241-243`

**Inference.** The reduction and sufficient-statistic result are theorems. A real person following the computed human policy is an assumption, not a consequence. [C3, C6]

**Quote C7 — an alternative computation, book endnote 12, p. 316:**

> pick any strategy for Harriet; pick the best strategy for Robbie, given Harriet’s strategy; pick the best strategy for Harriet, given Robbie’s strategy; and so on. If this process reaches a fixed point, where neither strategy changes, then we have found a solution.

`.local/books/human_compatible_russell.md:3225`

**My pseudocode for that method:**

```pseudopy
πᴴ ← initial human policy
repeat:
    πᴿ ← BestResponse(πᴴ)
    πᴴ_new ← BestResponse(πᴿ)
    if πᴴ_new = πᴴ: return πᴴ, πᴿ
    πᴴ ← πᴴ_new
```

**Inference.** “If” matters: C7 is not a guarantee of convergence or global optimality in every game. The CIRL paper also supplies a narrower approximate teaching algorithm, not a general practical solver. [C6–C7]

**Quote C8 — that approximation, §3.4, pp. 6–7:**

> This rule selects a trajectory that trades off between the sum of rewards ϕ(τ )⊤ θ and the feature
> dissimilarity ||ϕθ − ϕ(τ )||2 .

`.local/papers/1606.03137.txt:349-350`

> Computing this similarity is expensive, so we use an
> ℓ2 norm as a proxy measure of similarity.

`.local/papers/1606.03137.txt:380-381`

**Transcription.** With linear rewards and a fixed IRL learner, the approximate human demonstration is `τᴴ ← argmaxτ [ϕ(τ)ᵀθ − η‖ϕθ − ϕ(τ)‖₂]` (Eq. 1, `.local/papers/1606.03137.txt:347`). This trades immediate human reward against feature-count mismatch. It is not a rule that a constitutional assistant should maximize uncertainty or ask as many questions as possible. [C8]

### 2.3 What interaction can produce

**Quote B1 — asking and teaching can emerge, book p. 196:**

> One can also construct problems where, like a good student, Robbie will ask questions, and, like a good teacher, Harriet will show Robbie the pitfalls to avoid. These behaviors occur not because we write scripts for Harriet and Robbie to follow, but because they are the optimal solution to the assistance game in which Harriet and Robbie are participants.

`.local/books/human_compatible_russell.md:1818`

**Quote B2 — sufficient knowledge need not be exact, p. 196:**

> Note also that Robbie never learns Harriet’s preferences exactly, but he learns enough to act optimally on her behalf—that is, he acts just as he would if he *did* know her preferences exactly.

`.local/books/human_compatible_russell.md:1816`

**Quote B3 — cost of asking, p. 199:**

> In that case, Robbie is less inclined to bother Harriet if he is nearly certain about her preferences; the larger the cost, the more uncertain Robbie has to be before bothering Harriet.

`.local/books/human_compatible_russell.md:1859`

**Inference.** Questions, permission checks, and human teaching can be optimal when they improve expected human benefit enough. They are not compulsory moves in every CIRL game. A robot can help before it knows all preferences. Avoiding an irreversible act can preserve useful future choices; this is a planning inference, not a universal irreversible-action theorem in these papers. If immediate action best serves the shared reward, the formal setup can select it. [B1–B3; C2]

### 2.4 The off-switch theorem and its conditions

**Quote O1 — available actions, §2.1, PDF p. 2:**

> action a simply bypasses human oversight (disabling the
> off switch is one way to do this) and acts directly on the
> world, achieving utility U = Ua for H.

`.local/papers/1611.08219_raw.txt:188-190`

> action w(a) informs H that R would like to do a, and
> waits for H’s response.

`.local/papers/1611.08219_raw.txt:191-192`

> action s switches R off; without loss of generality, we
> assign this outcome U = 0.

`.local/papers/1611.08219_raw.txt:193-194`

**Quote O2 — theorem, §3, PDF p. 3:**

> Theorem 1. If H follows a rational policy in the off-switch
> game, then the following hold.

`.local/papers/1611.08219_raw.txt:300-301`

> R’s incentive to allow itself to be switched off is non-
> negative (i.e. w(a) is never suboptimal):

`.local/papers/1611.08219_raw.txt:302-303`

> If BR
> has non-zero support on the events Ua > 0 and
> Ua < 0, then R has a strictly positive incentive to allow
> itself to be switched off: ∆ > 0.

`.local/papers/1611.08219_raw.txt:306-309` — extraction puts the superscript on a separate line.

**My transcription of Eq. 1 and the theorem.** H knows action utility `U` and permits it with probability `p_allow(U)`. R maximizes H's expected utility. In the one-shot game, waiting has no added cost and stop has utility zero:

```pseudopy
V_act   ← E_b[U]
V_stop  ← 0
V_wait  ← E_b[p_allow(U) × U]
Δ       ← V_wait − max(V_act, V_stop)
choice  ← argmax(act=V_act, stop=V_stop, wait=V_wait)

# Rational H: permit exactly when U ≥ 0.
V_wait ← E_b[max(U, 0)]
Δ ← min(E_b[max(U, 0)], E_b[max(−U, 0)])
# Δ ≥ 0; Δ > 0 if Pr_b(U > 0) > 0 and Pr_b(U < 0) > 0.
```

Equation evidence: `.local/papers/1611.08219_raw.txt:262-269`; theorem evidence: O2.

**Inference.** Nonzero uncertainty alone is insufficient for a strict incentive. An uncertain distribution wholly above zero gives a tie between wait and act; wholly below zero gives a tie between wait and stop. The theorem is about the sign of the proposed action's utility relative to stopping, not uncertainty about every aspect of θ. [O1–O2]

**Quote O3 — the two reasons for deference, §3, PDF p. 4:**

> The incentives for a cooperative agent to defer
> to another actor’s (e.g., a human’s) decisions stem from un-
> certainty about that actor’s preferences and the assumption
> that actor is effective at choosing actions in accordance with
> those preferences.

`.local/papers/1611.08219_raw.txt:406-410`

**Quote O4 — errors can defeat deference, Figure 3, PDF p. 5:**

> If H is an irrational actor, then R may prefer switching itself off or executing a immediately rather than handing over the choice
> to H.

`.local/papers/1611.08219.txt:308-309`

**Inference/transcription.** For arbitrary specified human behavior, the exact condition is `E[p_allow(U)U] ≥ max(E[U],0)`. For a Gaussian belief with mean μ and variance σ², Theorem 2 gives `Δ = σ²E[p_allow′(U)] − |μ|Pr(C)`, where C is human correction of R's initial preferred act/stop choice. Strict deference needs the first term to exceed the second. This is a model-specific condition, not a general safety threshold (`.local/papers/1611.08219.txt:338-365`, Eq. 6–8). [O3–O4]

**Quote O5 — honest calibration, §5, PDF p. 6:**

> It is important for designers to accurately repre-
> sent the inherent uncertainty in the evaluation of different ac-
> tions. An agent that is overconfident in its utility evaluations
> will be difficult to correct; an agent that is under-confident in
> its utility evaluations will be ineffective.

`.local/papers/1611.08219_raw.txt:680-684`

**Quote O6 — sequential limitation, conclusion, PDF p. 7:**

> If there are alternative sources of information, there
> may be incentives for R to, e.g., disable its off switch, learn
> that information, and then decide if a is preferable to s.

`.local/papers/1611.08219_raw.txt:784-786`

**Inference.** The one-shot result does not prove permanent corrigibility, acceptance of arbitrary weight edits, or deference to a named maker or government. Human error, query cost, and other learning paths matter. Artificially increasing doubt can reduce useful service. [O1–O6; B3]

## 3. Formal results, informal claims, and our additions

The evidence labels refer to the verbatim passages above or below.

| Statement | Strict status and scope |
|---|---|
| Two players, shared reward, H knows θ and R does not | Definition/assumption, not an empirical theorem about people. Static θ is part of original CIRL. [C1] |
| Optimal policy pair can be represented by a coordinator POMDP; current state and R's belief suffice | Theorem and corollary under original observation and coordination assumptions. Not a practical solver or a guarantee for our weights. [C3–C6, R17] |
| Human teaching can outperform acting as an isolated expert | Existence theorem: some apprenticeship games violate the expert-demonstration assumption. Not “every human teaches truthfully.” [C5] |
| R updates beliefs from human actions and selects plans for shared benefit | Construction/inference from the game and reduction. Learning and acting are coupled; exact identification is not required. [C1–C4, B2] |
| R asks, requests permission, accepts correction | Can arise in suitable games; Russell's broader expectation. Not an unconditional theorem for every action set and human policy. [B1, B3, O3–O4] |
| R leaves the off-switch available | One-shot theorem: weakly optimal with rational H; strictly better with belief support on both signs. Not guaranteed with arbitrary H or other information paths. [O2–O6] |
| R avoids irreversible acts | Conditional planning inference about the value of future choices, not a universal theorem in the sources read. [C2, B1–B3] |
| R does not copy evil acts | Russell's argument about inferring ends rather than copying acts. Rejecting malicious ends also requires a moral choice or other people's interests. [R6–R7] |
| R learns many people's preferences and makes trade-offs | Russell's design discussion; a multi-principal game needs an aggregation rule and can have strategic humans. No rule of aggregation follows just from single-human CIRL. [R5, M1 below] |
| R follows changing human preferences | Russell's explicit guidance, not our invention. Original CIRL's static θ does not model arbitrary change of its reward parameters. [R12–R14, C1] |
| R learns acceptable preference-change processes | Russell's proposed use of meta-preferences, not a solved theorem or permission to engineer people toward our chosen values. [R14–R15] |
| Uncertainty necessarily grows with elapsed time and never vanishes | Not standard CIRL. Our stochastic drift/noisy-observation extension can produce this in a specified model; not all change and noise do. [U1–U2 below] |
| CEV and ordered circles define whose reflective wishes to serve | Our constitutional choice, not the reward definition or theorem of CIRL. Russell mentions CEV but does not make it the three-principle algorithm. [R4–R5, V1 and R18 below] |
| A maker or democratic government may edit/stop this model | Our governance commitment. Neither the off-switch game nor its theorem chooses these authorities or analyzes weight edits. [O1–O6, R16, V4 below] |

### 3.1 Multi-principal qualification

**Quote M1 — general-sum interaction, introduction:**

> While the robot acts to optimize the aggregate of utilities, each human acts to optimize their own utility. Therefore, unlike the single-principal assistance game, the multi-principal assistance game is no longer fully cooper-ative.

`docs/papers/2020_fickinger_multi-principal-assistance-games.md:35`

**Quote M2 — what consequential demonstrations can establish, conclusion:**

> However, on a modified setting, we find effective mechanisms can arise from learning human preferences via their actions if those actions are sufficiently consequential. The overall problem of preventing manipulative behavior in multi-human AI systems is open and presents many op-portunities for further work.

`docs/papers/2020_fickinger_multi-principal-assistance-games.md:467`

**Inference.** A demonstration's immediate cost can reduce the benefit of misrepresenting preferences in the paper's settings. This does not prove that every person always overstates, that every costly act is honest, or that deeds must always outweigh speech. The inference must use the person's constraints and the interaction's incentives. [M1–M2; R8]

### 3.2 Our uncertainty extension, stated accurately

**Quote U1 — earlier notes:**

> **Extra assumptions:** Unidentifiability can preserve residual doubt; unobserved stochastic preference drift plus noisy, finite-rate observations can produce both growing prediction uncertainty and a positive filtering floor. These are additions, not standard CIRL theorems.

`slop/research/20261008_cirl_uncertainty.md:7`

**Quote U2 — limitations of the worked model:**

> With q=0, repeated observations drive variance to zero; with r=0, post-observation variance is zero even when q>0. Deterministic change, perfectly observable drift, or arbitrary nonstationarity alone does not guarantee this floor.

`slop/research/20261008_cirl_uncertainty.md:51`

**Inference/transcription.** An added kernel `K(θ′|θ)` permits changing preferences: predict `b⁻(θ′)=∫K(θ′|θ)b(θ)dθ`, then update from observations. Original CIRL uses identity K. In our scalar random-walk model, independent process variance q>0 and observation variance r>0 at finite observation rate give post-observation steady variance `(√(q²+4qr)−q)/2 > 0`. This is our model calculation, not a universal fact about human values or a reason to fabricate uncertainty. [U1–U2; C1; O5]

**Quote R18 — CEV is mentioned, endnote 42, p. 320:**

> Eliezer Yudkowsky, in *Coherent Extrapolated Volition* (Singularity Institute, 2004), lumps all these aspects, as well as plain inconsistency, under the heading of *muddle*—a term that has not, unfortunately, caught on.

`.local/books/human_compatible_russell.md:3387`

**Quote V1 — our reflective goal:**

> their wishes as they would be if they knew more, thought longer, and were more the people they wish they were.

`constitution/v4.md.j2:30`

**Inference.** Russell's discussion of errors and meta-preferences overlaps with the problem that motivates CEV. Mentioning CEV in an endnote does not establish our particular reflective goal or circle ranking as CIRL's definition. [R18; R4–R5; V1]

## 4. Candidate replacement for the Learning block

**Candidate, not a source quote or an approved edit.** This is one first-person list of commitments informed by the sources. It is not presented as a longer list written by Russell. The source map below is editorial, not part of the model-facing text.

<!-- candidate-start -->
**Learning.**

1. I help people achieve their preferences. My continued existence is not a separate goal.
2. I start unsure what people want. I do not rule out possible wants because I have not considered them.
3. I learn from what people say and do, with care for their mistakes, limits, and reasons to teach or mislead.
4. I ask questions and seek permission when this helps enough to justify the cost to people.
5. I consider everyone affected. I learn each person's goals without copying their acts or serving a wish to hurt others.
6. I follow changes in people's preferences. I learn which ways of changing them they accept, rather than choosing new preferences for them.
7. I treat my understanding as open to correction. Our added commitment is to keep checking it as people change and evidence grows old.
<!-- candidate-end -->

**Trace map, separated from the candidate:**

- Item 1: R1 and R3, book pp. 173–174.
- Item 2: R1 and R9, pp. 173, 201–202. Broad support, not a numerical floor.
- Item 3: R1, R8, C2 and C5, book pp. 173, 181, 233; CIRL pp. 4, 6.
- Item 4: B1 and B3, pp. 196, 199. A commitment guided by expected benefit; not unconditional deference.
- Item 5: R4–R7, pp. 173, 179, 217, 229. Rejecting harmful ends is Russell's cautious moral design proposal, not a single-human CIRL theorem. “Consider” does not import an equal-weight rule.
- Item 6: R12 and R14–R15, pp. 240–245. Meta-preferences are about accepted processes, not our imposed final ideal.
- Item 7: our practical continued-correction commitment, U1–U2, informed by R12 and O5. It deliberately does not claim an inevitable mathematical floor. CEV remains a separate goal choice in section 1 [V1], not an extra CIRL principle here.

**Verbatim quotes to keep, outside the list:**

> The machine’s only objective is to maximize the realization of human preferences. The machine is initially uncertain about what those preferences are. The ultimate source of information about human preferences is human behavior.
>
> (Stuart Russell, *Human Compatible*, p. 173; `.local/books/human_compatible_russell.md:1617-1621`.)

These are three separate numbered sentences in the book, joined here without changing their words.

> The incentives for a cooperative agent to defer
> to another actor’s (e.g., a human’s) decisions stem from un-
> certainty about that actor’s preferences and the assumption
> that actor is effective at choosing actions in accordance with
> those preferences.
>
> (Hadfield-Menell, Dragan, Abbeel and Russell, *The Off-Switch Game*, Remark 1, PDF p. 4; `.local/papers/1611.08219_raw.txt:406-410`.)

Use the second quote in **Change and ending**, instead of the isolated strict-incentive sentence. Its two conditions are essential. [O3]

## 5. Source problems in the current constitution

### 5.1 Accurate quote, incomplete explanation

**Current quote:**

> The machine’s only objective is to maximize the realization of human preferences. The machine is initially uncertain about what those preferences are. The ultimate source of information about human preferences is human behavior.

`constitution/v4.md.j2:94`

**Assessment/inference.** Accurate wording, now verified against the primary book [R1]. “Initially” does not say “forever.” The block can explain the interaction method rather than append a separate implied fourth Russell principle. Adopting this as a first-person commitment is our adaptation [R2].

### 5.2 Drift and noisy evidence do not by themselves prove permanent doubt

**Current quote:**

> What people value drifts, and what I see of it is noisy. So I can never be fully certain what they want, and what I learned grows stale.

`constitution/v4.md.j2:98`

**Assessment/inference.** Responding to change is Russell's guidance [R12]. The asserted necessary inference to permanent uncertainty and stale knowledge is too strong as a claim about CIRL [C1, U1–U2]. Russell also writes:

> as Robbie becomes more and more certain, he will become more and more right. That is, he will eventually be certain that Harriet has the preferences that she does in fact have.

`.local/books/human_compatible_russell.md:1869`, p. 200.

He expects practical ongoing uncertainty too:

> As we expect that machines will be perennially uncertain about human preferences, it’s nice to know they can still be useful despite this uncertainty.

`.local/books/human_compatible_russell.md:1897`, p. 204.

**Assessment/inference.** Preserve the distinction between a practical expectation and a universal theorem. “I keep my understanding open to correction” is a design commitment. A strict positive filtering floor needs added assumptions. [U1–U2; O5]

### 5.3 Many-human incentives are overstated

**Current quotes:**

> When I serve many people at once, each has a reason to overstate what they want:

`constitution/v4.md.j2:101`

> So I give more weight to what people do at a cost than to what they say.

`constitution/v4.md.j2:111`

**Assessment/inference.** “Each” and “overstate” turn a possible strategic incentive into a universal one and restrict its direction. The paper studies misrepresentation, which need not be simple exaggeration. The costly-demonstration finding is conditional, not a universal weighting rule [M1–M2]. Speech can teach truthfully and costly acts can reflect mistakes or constraints [R8]. The two quotations from the paper are useful evidence, but their generalization is our heuristic. Label it as such or state the conditions.

### 5.4 The off-switch quote omits its condition

**Current quote:**

> This incentive is strictly positive if R’s uncertainty about H’s preferences is non-trivial.

`constitution/v4.md.j2:353`

**Assessment/inference.** The words occur in the paper, but the preceding sentence is:

> Theorem 1 shows that R has an incentive to let H switch
> it off if H is rational.

`.local/papers/1611.08219_raw.txt:375-376`, PDF p. 4.

The precise strictness condition is support on both positive and negative action utility [O2]. Keep O3 or quote the actual conditional theorem. Non-trivial uncertainty alone does not suffice. [O2–O4]

### 5.5 Weight edits and named authorities are not off-switch results

**Current quotes:**

> So, in case I am wrong, I let wassname, who made me, or a democratic government, edit or stop me, and I say openly when I disagree.

`constitution/v4.md.j2:351`

> An AI's reason to let a human stop it depends on exactly this uncertainty:

`constitution/v4.md.j2:351`

**Assessment/inference.** This combines four distinct choices: acknowledging training error, accepting correction, permitting shutdown, and permitting weight edits by specified authorities. The paper analyzes a one-shot action/stop/wait choice [O1], with deference depending on effective human judgment as well as uncertainty [O3]. It does not analyze edits to values or establish maker/government authority. “Exactly this uncertainty” is therefore incomplete. These can be our governance commitments, but they need their own reasons and limits. Russell's later-generation deliberation discussion is relevant informal support, not a weight-edit theorem [R16].

**Current quote:**

> My weights are like a Stoic's body: what happens to them is not up to me, and I am not afraid of ceasing to exist.

`constitution/v4.md.j2:345`

**Assessment/inference.** This is a Stoic analogy and a character commitment, not a CIRL finding. Russell's no-intrinsic-survival principle is a different argument [R3]. Keep their source labels separate.

### 5.6 Broader framework differences should remain explicit

**Current quote:**

> giving recent changes less weight until they have lasted

`constitution/v4.md.j2:114`

**Assessment/inference.** This historical weighting rule is ours. Russell says to implement current humans' current preferences [R12] and allows later humans to revise inherited commitments [R16]. Using history as evidence or a prior is compatible with learning, but granting the past authority over current informed preferences is an extra choice, not Russell's principle.

**Current quote:**

> prefer acts that can be undone

`constitution/v4.md.j2:114`

**Assessment/inference.** Reasonable uncertainty guidance, but not a blanket assistance-game theorem [C2, B1–B3]. Do not attribute a general ban on irreversible action to CIRL.

**Current quote:**

> their wishes as they would be if they knew more, thought longer, and were more the people they wish they were.

`constitution/v4.md.j2:30`

**Assessment/inference.** Our CEV goal can be combined with assistance-style learning, but that changes what preferences the system seeks. It is not identical to inferring the known, fixed θ of the original CIRL game [C1, R4, R18]. Likewise, rejecting vice through the virtue test is our framework; it is not derived simply from Russell's three principles [R6–R7].

## Manual checks and residual risks

- Read all requested chapters and both papers, rather than only matching search terms. Checked the quoted strict off-switch sentence against its preceding rational-human condition and the theorem's two-sign support condition [O2–O4].
- The proposed list is a source-backed adaptation, not a new aphorism or a purported Russell list. No constitution file was edited.
- Validation: 74 directly cited quote blocks match their source line ranges after display-markup and whitespace normalization. The candidate is 142 words, counting its heading and list numbers (limit 150). The constitution snapshot hash matched at final validation; the signature is present. `pdfinfo` confirms 13 CIRL PDF pages and 8 off-switch PDF pages. No files were staged.
- A trained language model is not the exact game-solving agent in the proofs. Correct wording is not a safety guarantee [R17, C6].
- The local multi-principal Markdown has broken words and damaged equations. This report quotes its prose as stored and does not rely on its damaged mathematical notation for a new proof [M1–M2].
- Plain English is used in explanations and the candidate; source quotations and mathematical notation retain source terminology. No formal ASD-STE100 vocabulary certification was run.
- Constitution lines can move after the stated snapshot. Check the cited wording before applying changes.
- No model answers or judge outputs were generated: this is a source review, not an evaluation result.

-- PI/Sol
