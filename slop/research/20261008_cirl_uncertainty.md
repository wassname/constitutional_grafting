# CIRL uncertainty: a posterior, not a guaranteed permanent doubt

## 1. Verdict (three lines)

**Floor:** Standard CIRL imposes no positive lower bound on reward uncertainty; exact identification can eliminate it, and identifiable stationary parameters can be learned asymptotically.
**Decay:** Standard CIRL has a fixed θ: time alone does not erode knowledge; new evidence can increase realized uncertainty, but there is no built-in forgetting clock.
**Extra assumptions:** Unidentifiability can preserve residual doubt; unobserved stochastic preference drift plus noisy, finite-rate observations can produce both growing prediction uncertainty and a positive filtering floor. These are additions, not standard CIRL theorems.

## 2. Math and an illustrative agent

**CIRL [1, §3.1]:** game `M = ⟨S, {Aᴴ,Aᴿ}, T, {Θ,R}, P₀, γ⟩`. S is the public world state; H and R choose actions; T moves the world; θ parameterizes their shared reward R; P₀ samples `(s₀,θ)` once; γ discounts rewards. H observes θ, R does not. Reward being the objective does **not** mean R receives a sensor revealing its numerical value.

For public history h and a specified human policy, the Bayesian update is

`b⁺(θ) ∝ b(θ) πᴴ(aᴴ | h,θ)`.

The θ-independent world-transition likelihood cancels. Include other evidence likelihoods if the observation model actually supplies them. The human likelihood must model teaching/cooperation, not automatically treat actions as isolated optimal demonstrations. [2, §2.3, Eq. 2] explicitly uses this update with a pedagogic human policy; [4] also permits specified human policies. A belief over θ is sufficient for optimal behavior in the original public-state setting [1, §3.2].

**Inference, not a paper quotation:** With two θ values and distinct deterministic informative human actions, one observation collapses the posterior to a point. With strictly positive likelihoods and nondegenerate priors, finite data need not yield exact certainty, but that does not establish a positive asymptotic floor. Repeated noisy observations can identify a stationary parameter. Conversely, observationally equivalent θ values remain indistinguishable. Uncertainty about θ is not identical to uncertainty about the best action.

**Our explicit extension:** add a transition kernel `K(θ′|θ)`, so prediction becomes `b⁻(θ′)=∫K(θ′|θ)b⁺(θ)dθ`. Standard CIRL uses the identity kernel. Carroll et al. [5] allow changing, action-influenceable reward parameters, but do not establish the particular Gaussian floor below.

```python
# Exact posterior skeleton: [1,2]; drift K is OUR addition.
b = prior_theta_given_s0
while running:
    b_pred = integrate(K(theta_new | theta_old) * b(theta_old), theta_old)
    # Standard CIRL: K is identity. Our random walk: θ_t=θ_(t-1)+N(0,q).
    b = normalize(b_pred * human_likelihood(observation, history, theta))
    # Use cooperative/pedagogic likelihood, not necessarily naive optimality.

    # One-shot off-switch rule: [3, Eq. 1]; query cost c is OUR addition.
    U = reward_gain_of(candidate_action, theta)  # shutdown baseline = 0
    V_act = E_b[U]
    V_stop = 0
    V_defer = E_b[p_human_allows(U) * U] - c
    choose_argmax(act=V_act, stop=V_stop, defer=V_defer)
    # General assistance instead plans future information and reward jointly [4].
```

**Our scalar worked example (not a general assistance algorithm):** Let `θ_t=θ_(t−1)+w_t`, `w_t~N(0,q)`, and an observation `y_t=θ_t+v_t`, `v_t~N(0,r)`, with independent noises, q,r>0, one observation per step. Gaussian filtering gives:

```python
P_pred = P + q                  # variance grows between observations
k = P_pred / (P_pred + r)
m = m + k * (y - m)
P = (1 - k) * P_pred
P_steady = (sqrt(q*q + 4*q*r) - q) / 2  # positive POST-observation variance
```

This formula is our direct derivation from `P=r(P+q)/(P+q+r)`, not an attributed theorem about human values. With n unobserved steps, prediction variance grows by nq. With q=0, repeated observations drive variance to zero; with r=0, post-observation variance is zero even when q>0. Deterministic change, perfectly observable drift, or arbitrary nonstationarity alone does not guarantee this floor. A floor also does not force incessant questions: ask when expected improvement outweighs cost and passive information is inadequate. Preserve human control as a separate design commitment rather than relying solely on this fragile incentive.

## 3. Verbatim evidence (observations)

Quotes retain adjacent sentence context where available; mathematical typography is normalized. These observations support the distinctions above; the counterexample and Gaussian derivation are our inferences.

**[1] Hadfield-Menell, Dragan, Abbeel & Russell (2016), *Cooperative Inverse Reinforcement Learning*, [full text](https://arxiv.org/html/1606.03137v4), §3.1:**

> We write the reward for a state–parameter pair as R(s,aᴴ,aᴿ;θ) to distinguish the static reward parameters θ from the changing world state s. The game proceeds as follows. First, the initial state, a tuple (s,θ), is sampled from P₀. H observes θ, but R does not.

§3.2, adjacent result introduction:

> An immediate consequence of this result is that R’s belief about θ is a sufficient statistic for optimal behavior.

**[2] Fisac et al. (2017/2018), *Pragmatic-Pedagogic Value Alignment*, [full text](https://arxiv.org/html/1707.06354v2), §2.3, following Eq. 2:**

> This amounts to a deterministic transition function for R’s belief, bᴿ′ = f_b(s,bᴿ,aᴴ,aᴿ). Crucially, however, the fixed-point relation derived here involves Q itself, which we have yet to compute. Unlike H, R is modeled as a rational agent; however, not knowing the true θ, the best R can do is to maximize the expectation of Q based on its current belief bᴿ.

**[3] Hadfield-Menell et al. (2017), *The Off-Switch Game*, [full text](https://arxiv.org/html/1611.08219v3), §3, discussion preceding Corollary 1:**

> This incentive is strictly positive if R’s uncertainty about H’s preferences is non-trivial. Next, we show the converse: a rational H is a necessary condition for Δ ≥ 0 if R believes it knows H’s preferences with certainty.

Figure 2 caption:

> Notice that Δ is non-negative everywhere and that in all cases Δ → 0 as σ → 0.

**Inference:** With rational H, vanishing uncertainty removes strict preference for deference, not necessarily permission to switch off. With suboptimal H, deference can become strictly worse. Nonzero uncertainty alone is insufficient: rational-human strictness requires support on both positive and negative action utility.

**[4] Shah et al. (2020), *Benefits of Assistance over Reward Learning*, [author-hosted full PDF](https://people.eecs.berkeley.edu/~russell/papers/neurips20ws-assistance), §1:**

> An assistive R can make the pie crust, but wait to ask H about her preferences over the filling (Section 4.1). R may never clarify all of H’s preferences: for example, R only needs to know how to dispose of food if it turns out that the ingredients have gone bad (Section 4.2). If H will help with making the pie, R can allow H to disambiguate her desired pie by watching what filling she chooses (Section 4.3).

**[5] Carroll et al. (2024), *AI Alignment with Changing and Influenceable Reward Functions*, [full text](https://arxiv.org/html/2405.17713v1), §2, following Definition 1:**

> Each θ ∈ Θ can be thought of as the cognitive state of the human, which includes anything affecting their evaluation of state-action pairs (e.g. preferences, beliefs, emotions).

The definition explicitly includes `T(s_(t+1),θ_(t+1)|s_t,θ_t,a_t)` encoding state **and reward** dynamics. This is a different formalism, not proof of a CIRL uncertainty floor.

**Russell (2019), *Human Compatible*, three principles:** Full book text was not obtained. A [Quanta article reproduces them](https://www.quantamagazine.org/artificial-intelligence-will-do-what-we-ask-thats-a-problem-20200130):

> The machine’s only objective is to maximize the realization of human preferences. The machine is initially uncertain about what those preferences are. The ultimate source of information about human preferences is human behavior.

This is secondary verification of book wording, explicitly not a primary-source claim that uncertainty never vanishes. No verified Russell passage establishing inevitable decay or a universal positive floor was located.

## 4. Implication for the constitution

Say: “Treat your understanding of human values as fallible; learn from people and revisit assumptions when circumstances or preferences change.”
Do not claim CIRL proves that certainty inevitably decays or can never become complete.
Continued openness to correction and protection of human control are commitments we add, not guarantees of Bayesian reward learning.

-- delegate subagent (gpt-6.1-sol) for PI/Claude
