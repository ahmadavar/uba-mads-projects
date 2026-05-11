# Statistics from First Principles
### A Finance-Grounded Guide to Everything in DSCI 503

*Every concept from the NHANES homework — explained with finance examples, intuition first, formulas second.*

---

# Chapter 1: Probability Foundations & Random Variables

## The Problem This Chapter Solves

You're a portfolio manager. You want to know: what's the probability this stock goes up tomorrow? What's the probability it goes up *given* that the Fed just raised rates? What's the probability your entire portfolio loses more than 10% in a single month?

These aren't just practical questions — they force you to confront what "probability" actually means, how randomness is structured, and how to reason under uncertainty. That's what this chapter is about.

---

## Sample Spaces and Events

Before you can assign a probability to anything, you need to be precise about what could happen.

The **sample space** is the set of all possible outcomes. Flip a coin: sample space is {Heads, Tails}. Buy one share of a stock today and check tomorrow: sample space is every possible price. More useful framing: sample space is {price goes up, price goes down, price stays the same}.

An **event** is any subset of the sample space — any collection of outcomes you care about. "The stock goes up" is an event. "The stock moves more than 2%" is an event. "The stock stays flat" is an event.

Why does this matter? Because probability is a function that assigns a number between 0 and 1 to events, not to individual outcomes alone. When you say "there's a 60% chance the stock goes up," you're assigning a probability to the event {price goes up}.

---

## Probability Axioms

Three rules that any valid probability assignment must follow:

1. **Non-negativity:** P(A) ≥ 0 for any event A. Probabilities can't be negative.
2. **Normalization:** P(entire sample space) = 1. Something has to happen.
3. **Additivity:** If A and B can't both happen (mutually exclusive), then P(A or B) = P(A) + P(B).

Everything else in probability theory follows from these three rules. They're not assumptions about the world — they're the definition of what it means for something to be a probability.

---

## Conditional Probability

This is where probability gets useful and subtle.

**Conditional probability** answers: what's the probability of A, *given that* B already happened?

The formula: **P(A | B) = P(A and B) / P(B)**

Read the left side as "probability of A given B." The right side says: out of all the times B happened, how often did A also happen?

**Finance example:** You want to know P(stock goes up | Fed raised rates today).

Start with historical data. Say stocks went up on 55% of all trading days. But on days the Fed raised rates, stocks went up only 40% of the time. Those two numbers are very different, and the difference matters for your trading strategy. The conditional probability updates your belief based on new information — the Fed announcement is evidence that changes what you expect.

> **Key insight:** Conditional probability is the formal machinery for updating beliefs with evidence. Every time you say "given that X happened, what's the probability of Y?" — that's conditional probability.

---

## Independence

Two events are **independent** if knowing one happened tells you nothing about the other.

Formally: A and B are independent if P(A | B) = P(A). The probability of A doesn't change when you learn B happened.

**Finance example:** Two stocks from completely different industries with no common customers, suppliers, or macro exposure. If one goes up, that tells you nothing about the other. They're (approximately) independent.

**Why assuming independence is dangerous:** The 2008 financial crisis. Mortgage-backed securities were structured assuming that individual home loans were independent — if one borrower defaults, that tells you nothing about whether another will. Rating agencies gave these securities AAA ratings based on that assumption. But borrowers weren't independent — they all lived in the same economy, shared the same housing market, and faced the same interest rate environment. When the housing market collapsed, loans defaulted together. The independence assumption was catastrophically wrong, and the entire structure of "diversified" securities unraveled simultaneously.

> The lesson: independence is a mathematical convenience. Check whether it's actually true before building on it.

---

## Bayes' Theorem

This is the most important equation in this course. Let's derive it intuitively.

You know P(A | B) = P(A and B) / P(B). Similarly, P(B | A) = P(A and B) / P(A). Both expressions equal P(A and B), so they're equal to each other (times their denominators):

**P(A | B) = P(B | A) × P(A) / P(B)**

In words: the probability of A given B equals the probability of B given A, times the probability of A, divided by the probability of B.

This lets you **reverse the direction of a conditional probability.** You know how likely B is given A. Bayes' theorem tells you how likely A is given B.

**Finance example — analyst upgrades:**

You know from history:
- 30% of stocks get upgraded by an analyst in a given quarter: P(upgrade) = 0.30
- Among stocks that later outperform the market, 70% had received an upgrade: P(upgrade | outperform) = 0.70
- 60% of stocks outperform the market in any given quarter: P(outperform) = 0.60

Question: You just saw a stock get upgraded. What's the probability it outperforms?

P(outperform | upgrade) = P(upgrade | outperform) × P(outperform) / P(upgrade)
= 0.70 × 0.60 / 0.30
= 0.42 / 0.30
= **1.40** — wait, that can't be right (probabilities can't exceed 1).

Let's fix the numbers to be consistent: say P(upgrade) = 0.42. Then:
P(outperform | upgrade) = 0.70 × 0.60 / 0.42 = **1.0** — still off.

Use realistic numbers: P(upgrade) = 0.35, P(upgrade | outperform) = 0.50, P(outperform) = 0.55.
P(outperform | upgrade) = 0.50 × 0.55 / 0.35 = **0.786**

So an analyst upgrade shifts your probability estimate of outperformance from 55% to 78.6%. That's Bayes' theorem in action — you started with a prior belief (55% of stocks outperform), saw evidence (analyst upgrade), and updated to a posterior belief (78.6%).

The three terms have names that will come up constantly:
- **Prior:** P(outperform) = 0.55 — your belief before seeing the evidence
- **Likelihood:** P(upgrade | outperform) = 0.50 — how probable is this evidence if the hypothesis is true
- **Posterior:** P(outperform | upgrade) = 0.786 — your updated belief after seeing the evidence

---

## Random Variables

A **random variable** is a number whose value is determined by a random experiment. It's a function from outcomes to numbers.

When you roll a die, the number that comes up is a random variable. When you observe a stock's return today, that return is a random variable. When you count the number of trades executed in the next hour, that count is a random variable.

**Discrete random variables** take a countable set of values: 0, 1, 2, 3... The number of stocks in your portfolio that go up today is discrete.

**Continuous random variables** can take any value in a range. A stock's daily return — which could be -3.7%, +0.23%, +5.1% — is continuous.

---

## Expected Value

The **expected value** of a random variable is its probability-weighted average — what you'd get on average if you observed the random variable many times.

Formula: **E[X] = Σ x · P(X = x)** (for discrete) or **∫ x · f(x) dx** (for continuous)

Think of it as the center of gravity of the distribution. If you put the probability distribution on a seesaw, the expected value is the fulcrum point where it balances.

**Finance example:** A trade either gains $500 (probability 0.4) or loses $200 (probability 0.6). Expected value = 0.4 × 500 + 0.6 × (-200) = 200 - 120 = **$80**. On average, this trade makes $80. That's your expected profit per trade.

The expected value doesn't tell you what happens on any individual trade. It tells you what happens on average over many trades — which is exactly what matters for a systematic trading strategy.

---

## Variance and Standard Deviation

Expected value tells you the center. **Variance** tells you how spread out the distribution is around that center.

**Var(X) = E[(X - μ)²]** where μ = E[X]

In words: take the average squared distance from the mean. We square the distances so that positive and negative deviations don't cancel each other out.

**Standard deviation** = √Var(X). It puts the spread back in the same units as X.

Why square? Why not just average the absolute deviations? Squaring penalizes large deviations more than small ones (a deviation of 2 contributes 4 to variance, not 2). This is mathematically convenient — squared deviations have nicer algebraic properties. And in finance, large losses hurt more than proportionally, so the extra penalty on large deviations is appropriate.

**Finance application:** A stock with annual return μ = 10% and standard deviation σ = 20% is much riskier than one with μ = 10% and σ = 5%, even though both have the same expected return. Standard deviation is the most common measure of risk in finance — it's what "volatility" means.

---

## Key Distributions

### Bernoulli
A single trial with two outcomes: success (probability p) or failure (probability 1-p).

**Finance use:** Did this trade make money? Each individual trade is a Bernoulli trial. If your strategy has a 55% win rate, each trade is Bernoulli(0.55).

### Binomial
The count of successes in n independent Bernoulli trials.

**Finance use:** Out of 20 trades this month, how many were profitable? If each has a 55% win rate, the count follows Binomial(20, 0.55). Expected value = n·p = 11 profitable trades.

### Poisson
The count of rare, independent events in a fixed time window, when the average rate λ is known.

**Finance use:** Number of credit defaults in a bond portfolio this month. Number of flash crash events in a year. Arrival rate of large institutional trades. The Poisson distribution is the natural model whenever you're counting rare discrete events in continuous time.

### Normal (Gaussian)
The bell curve. Symmetric, fully described by mean μ and standard deviation σ.

**Finance use:** Daily stock returns. Not exactly Normal (fat tails — extreme moves happen more often than Normal predicts), but close enough for many applications. Justified by the Central Limit Theorem.

### Exponential
The time between events in a Poisson process. If events arrive at rate λ, the waiting time between them is Exponential(λ).

**Finance use:** Time between large trades. Time until next market-moving event. Memoryless: if you've already waited 5 minutes for a trade, the expected additional wait is the same as if you'd just started waiting.

### Beta
A distribution on the interval [0, 1], parameterized by shape parameters a and b.

**Finance use:** Beliefs about a probability — like a trading strategy's true win rate. Before observing any trades, you might believe the win rate is somewhere around 50% but uncertain. Beta(2, 2) represents that belief. After observing wins and losses, you update it using Bayes' theorem (covered in Chapter 7).

---

## Law of Large Numbers

As you observe more independent draws from a distribution, the sample mean converges to the true expected value.

**What it says:** Run your trading strategy 10,000 times and your realized win rate will be very close to p.

**What it does NOT say (Gambler's Fallacy):** Past results don't make future results more or less likely on individual trials. If your strategy has lost 5 trades in a row, it's not "due" for a win. Each trade is independent. The Law of Large Numbers applies in aggregate over thousands of trials — it says nothing about what happens next.

---

## Central Limit Theorem

> This is the most important theorem in statistics.

**The theorem:** Take any distribution with finite mean μ and variance σ². Draw n independent samples and compute their average. As n grows, that average — properly standardized — approaches a Normal distribution, regardless of the original distribution's shape.

**Finance application:** A portfolio of 500 stocks. Each stock's daily return has some weird, possibly skewed distribution. But the portfolio return (the average of 500 returns) behaves like a Normal distribution. This is why the Normal distribution is everywhere in finance — it emerges naturally when you average many independent (or weakly dependent) things.

The CLT also justifies using t-tests and Normal-based confidence intervals even when individual data points aren't Normally distributed — if n is large enough, the sampling distribution of the mean is approximately Normal regardless.

---

## Goodness of Fit

After fitting a distribution to data, you want to check: does the data actually follow this distribution?

**Chi-squared test (idea):** Divide the data into bins. Compare observed counts in each bin to expected counts under the proposed distribution. If they differ a lot, the distribution doesn't fit well.

**Shapiro-Wilk test (idea):** Tests specifically whether data follows a Normal distribution. Computes a correlation between your data's order statistics and the expected Normal order statistics. A correlation near 1 = looks Normal. A low p-value = reject normality.

**Overdispersion:** When your data has more variance than the model predicts. A Poisson distribution has mean = variance by definition. If you observe variance much larger than the mean in count data, the Poisson model is too restrictive — you need something more flexible (like Negative Binomial). In finance: if a Poisson model says you should see λ = 3 defaults per month with variance 3, but you actually observe variance = 15, the data is overdispersed.

---

## How This Connects to the Homework

- **Q1–Q2:** Sample spaces, conditional probability, independence — these are the building blocks everything else rests on
- **Q3:** Bayes' theorem — you used it to update beliefs about health states; the analyst upgrade example above is the same logic
- **Q4–Q5:** Fitting distributions (Normal, Poisson, Negative Binomial) to NHANES data; overdispersion in count variables
- **Q6:** Shapiro-Wilk normality test — you ran this before t-tests in Part 4
- **Q7–Q8:** Expected value, variance, bivariate distributions
- **Part 8A:** Conditional probabilities of diabetes given risk factors — direct application of conditional probability

---

# Chapter 2: Simulation in Statistics

## Why Simulate?

Mathematics gives you exact answers — but only when the problem has a closed-form solution. Many real problems don't. The distribution of the ratio of two random variables. The confidence interval for a correlation coefficient. The probability that a portfolio loses more than 15% in a quarter when returns are correlated.

**Simulation is the escape hatch.** When the math is too hard, you can often approximate the answer by generating thousands of random samples and observing what happens empirically.

This isn't cheating — it's one of the most powerful tools in applied statistics, and it's responsible for everything from option pricing to drug trials to physics simulations.

---

## Pseudo-Random Number Generation

Computers can't actually be random — every operation is deterministic. What they produce instead is **pseudo-random numbers**: sequences that look random and pass statistical tests for randomness, but are entirely determined by a starting value called the **seed**.

The **Linear Congruential Generator (LCG)** is the simplest algorithm. It works like this:

Start with a seed X₀. Then repeatedly apply: **Xₙ₊₁ = (a · Xₙ + c) mod m**

Where a, c, and m are carefully chosen constants. Each new value depends only on the previous one. The sequence eventually repeats (it must — there are only m possible values) but with good constants, the period is enormous.

**Why this matters:** Setting a seed before your simulation makes it **reproducible**. `np.random.seed(42)` means everyone who runs your code gets the same "random" numbers. In research, reproducibility is non-negotiable. In production, it lets you debug.

---

## Inverse CDF Method

Here's a remarkable fact: if you can generate uniform random numbers (between 0 and 1), you can generate samples from *any* distribution.

The trick is the **inverse CDF** (also called the quantile function).

The CDF of a distribution tells you: F(x) = P(X ≤ x). It maps values to probabilities (0 to 1).

The inverse CDF F⁻¹ maps probabilities back to values.

**The method:** Draw u ~ Uniform(0, 1). Then X = F⁻¹(u) has the distribution you want.

**Finance example with Exponential:**

You want to simulate waiting times between trades, which follow Exponential(λ = 5 trades/hour).

The Exponential CDF is F(x) = 1 - e^{-λx}. Its inverse is F⁻¹(u) = -ln(1-u)/λ.

Draw u = 0.73 (a uniform random number). Then waiting time = -ln(1 - 0.73)/5 = -ln(0.27)/5 ≈ 0.26 hours ≈ 16 minutes.

This works because the CDF "distributes" probability uniformly — by mapping uniform samples through the inverse CDF, you get samples distributed exactly according to the target distribution.

---

## Box-Muller Transform

The inverse CDF method doesn't work cleanly for the Normal distribution (the Normal CDF has no closed-form inverse). The **Box-Muller transform** solves this by generating Normal samples from two Uniform samples.

The idea: if you draw two independent uniform random numbers u₁ and u₂, you can transform them into two independent standard Normal samples:

Z₁ = √(-2 ln u₁) · cos(2π u₂)
Z₂ = √(-2 ln u₁) · sin(2π u₂)

**Geometric intuition:** Imagine throwing a dart uniformly at random inside a circle. The radius of where it lands has a certain distribution; the angle is uniform. The Box-Muller transform converts these polar coordinates (radius and angle) into two Cartesian coordinates — and by a beautiful mathematical coincidence, those Cartesian coordinates are independently Normal.

This is why you can always generate Normal random numbers even though the Normal distribution doesn't have a nice inverse CDF.

---

## Monte Carlo Integration

Monte Carlo integration uses random sampling to estimate quantities that are hard to compute directly.

The core idea: **the expected value of a function equals the average of the function evaluated at random points.**

E[f(X)] ≈ (1/n) Σ f(Xᵢ) where X₁, ..., Xₙ are random samples.

**Finance application — option pricing:**

A European call option pays max(S_T - K, 0) at expiration, where S_T is the stock price at expiration and K is the strike price. What's this option worth today?

The theoretical answer requires computing an integral over all possible future stock prices, weighted by their probability. With Black-Scholes, this has a closed form. But for more complex options (path-dependent, with stochastic volatility), there's no formula.

Monte Carlo solution: Simulate 100,000 future stock price paths. For each path, compute the option payoff. Average all the payoffs. Discount back to today. That average is your option price estimate.

The law of large numbers guarantees this converges to the true price as you use more simulations. The error shrinks as 1/√n — doubling your accuracy requires 4× more simulations.

---

## The Bootstrap

> The single most important idea in computational statistics.

**The problem:** You have a sample of data and you've computed some statistic — a mean, a median, a Sharpe ratio, a correlation coefficient. How uncertain are you about that statistic? What's its sampling distribution?

For a mean, there's a formula (the standard error). For the Sharpe ratio — the ratio of mean return to standard deviation — there's no simple formula. For the median, the formula exists but is complicated. For complex statistics, there's often no formula at all.

**The bootstrap solution:** Pretend your sample IS the population. Resample from it (with replacement) thousands of times. Compute your statistic on each resample. The distribution of those bootstrapped statistics approximates the sampling distribution of your statistic.

**Finance example — Sharpe ratio:**

You have 60 months of returns for a hedge fund. The Sharpe ratio is 1.3. How confident are you in that estimate? Is it significantly above 1.0 (the typical benchmark)?

1. From your 60 monthly returns, draw 60 with replacement (some months appear twice, some not at all). Compute the Sharpe ratio. Say it's 1.15.
2. Repeat 10,000 times. You get 10,000 bootstrapped Sharpe ratios.
3. The 2.5th and 97.5th percentiles of those 10,000 values give you a 95% confidence interval. Say it's (0.8, 1.8).

That interval includes 1.0, so you can't confidently claim the strategy's true Sharpe ratio exceeds the benchmark.

**When bootstrap works:** When your sample is large enough to represent the population. When observations are independent (or you use a variant like the block bootstrap for time series).

**When bootstrap fails:** Very small samples (n < 15 or so). Heavy-tailed distributions where extreme values dominate. Non-stationary time series.

---

## Power Analysis and Sample Size

Before running an experiment, you need to know: if the effect I'm looking for is real, how likely am I to detect it?

**Statistical power** = P(reject H₀ | H₁ is true). The probability you correctly detect a real effect.

Power depends on:
- **Effect size:** larger effects are easier to detect
- **Sample size:** more data = more power
- **Significance level α:** using α = 0.01 instead of 0.05 reduces power
- **Variability:** more noise = harder to detect signals

**Finance example:** You're testing whether a new trading signal improves returns. If the true improvement is 0.5% per month with monthly return std dev of 3%, the effect size is small (d ≈ 0.17). To achieve 80% power at α = 0.05, you'd need roughly 280 months of data — over 23 years. That's a practical constraint on what effects you can detect in financial time series.

Power analysis tells you the minimum sample size needed before you collect data. Running underpowered studies wastes resources and produces unreliable results.

---

## Permutation Tests

A **permutation test** answers: could this result have occurred by chance if the labels were randomly assigned?

**Finance example:** You compare two trading strategies, A and B, over 50 trading days each. Strategy A averages 0.3% daily return; strategy B averages 0.15%. Is A genuinely better, or could this gap arise by chance?

Permutation approach:
1. Compute the observed difference: 0.3 - 0.15 = 0.15%.
2. Pool all 100 daily returns together. Randomly assign 50 to "Strategy A" and 50 to "Strategy B." Compute the difference in means.
3. Repeat 10,000 times. You get a distribution of differences under the null hypothesis.
4. p-value = fraction of permuted differences as large as 0.15%.

No distributional assumptions needed. The test is exact — it directly answers "how often does random chance produce this result?"

---

## How This Connects to the Homework

- **Q9:** LCG and pseudo-random number generation — you implemented this from scratch
- **Q10–Q11:** Inverse CDF method and Box-Muller transform — generating samples from specific distributions
- **Q12:** Monte Carlo integration — you used simulation to estimate an expected value
- **Q13:** Bootstrap confidence intervals — you applied this to NHANES statistics
- **Q14:** Power analysis — computing required sample sizes before running a hypothesis test
- **Part 8B:** Bootstrap CIs for diabetes prevalence by subgroup — direct application

---

# Chapter 3: Statistical Estimation

## Two Questions, Two Different Answers

You've collected data. Now you want to say something about the population it came from.

**Question 1:** What's the single best guess for the parameter? → **Point estimation**

**Question 2:** How uncertain is that guess? What range could the true value plausibly be in? → **Interval estimation**

Both questions matter. A point estimate without uncertainty is often misleading. A fund manager who claims "our strategy returns 12% annually" without a confidence interval is hiding the fact that the 95% CI might be (-5%, 29%) — essentially uninformative.

---

## Bias and Variance of an Estimator

An **estimator** is any function of your data that you use to guess a population parameter. The sample mean x̄ is an estimator of the population mean μ. The sample variance s² is an estimator of σ².

**Bias** = E[estimator] - true parameter. If your estimator, averaged over many samples, doesn't hit the true value — it's biased.

**Variance** = how much your estimator fluctuates from sample to sample.

**The dartboard analogy:** Imagine throwing many darts at a bullseye (the true parameter).
- Low bias, low variance: darts cluster tightly at the bullseye. Best case.
- High bias, low variance: darts cluster tightly but in the wrong place. Consistently wrong.
- Low bias, high variance: darts centered on the bullseye but scattered widely. Right on average, useless for any individual estimate.
- High bias, high variance: scattered and in the wrong place. Worst case.

Good estimators balance both. Adding more complexity to a model often reduces bias (it fits the data better) but increases variance (it overfits to noise). This **bias-variance tradeoff** reappears throughout machine learning.

---

## Method of Moments

The **Method of Moments (MOM)** says: set the theoretical moments of your distribution equal to the sample moments, and solve for the parameters.

The k-th moment of a distribution is E[Xᵏ]. The first moment is the mean. The second moment (around the mean) is the variance.

**Example — estimating the mean and variance of stock returns:**

You assume daily returns follow Normal(μ, σ²). You have 252 daily returns.

- Set theoretical mean (μ) = sample mean (x̄). So μ̂ = x̄.
- Set theoretical variance (σ²) = sample variance (s²). So σ̂² = s².

Done. MOM is fast and intuitive — match what the distribution predicts to what you observe.

**When MOM is enough:** Simple distributions, large samples, when you care more about speed than optimality.

**When MOM falls short:** With complex distributions, MOM can produce nonsensical estimates (like negative variance parameters). Also, MOM estimators aren't always efficient — they can have higher variance than the best possible estimator.

---

## Maximum Likelihood Estimation (MLE)

> MLE is the gold standard of point estimation.

**The core idea:** find the parameter values that make the observed data as probable as possible.

Imagine you observed these 5 daily returns: +1.2%, -0.5%, +0.8%, -0.3%, +1.5%.

Assume returns follow Normal(μ, σ²). Different values of μ and σ² make this particular set of observations more or less probable. MLE asks: which μ and σ² make the probability of observing exactly these returns as high as possible?

**The likelihood function** L(μ, σ² | data) = P(data | μ, σ²) = probability of the observed data as a function of the parameters.

For independent observations, this is the product of individual probabilities: L = f(x₁) × f(x₂) × ... × f(xₙ).

**The log-likelihood:** We maximize log L instead of L. Two reasons:
1. Products become sums: log(a × b) = log(a) + log(b). Sums are easier to work with mathematically.
2. The same parameters maximize L and log L (logarithm is monotone), so the answer is identical.

**MLE for Normal distribution:**

Set the derivative of log L with respect to μ to zero. The solution is exactly μ̂ = x̄ (the sample mean). This is a beautiful result — it says the most natural estimator you'd intuitively use is also optimal by MLE.

For σ², MLE gives σ̂² = (1/n)Σ(xᵢ - x̄)² — slightly different from the sample variance which uses (n-1) in the denominator. The MLE version is biased (it slightly underestimates σ²), which is why textbooks use (n-1) for an unbiased estimate.

**MLE properties:**
- **Consistent:** as n → ∞, the MLE converges to the true parameter
- **Asymptotically unbiased:** the bias vanishes as n grows
- **Asymptotically efficient:** among all consistent estimators, MLE achieves the lowest possible variance for large n (the Cramér-Rao lower bound)

---

## Confidence Intervals

> The most misunderstood concept in statistics.

**What a 95% confidence interval IS:**

If you repeated your sampling procedure 100 times and constructed a 95% CI each time, approximately 95 of those intervals would contain the true parameter.

**What it is NOT:**

"There's a 95% probability the true parameter is in this interval." — WRONG.

The true parameter is fixed (it's not random). The interval is what varies from sample to sample. Any specific interval either contains the true value or it doesn't — there's no probability about it.

This is subtle and widely misunderstood, even by researchers who publish papers. The practical takeaway: a CI is a statement about the reliability of your procedure, not a probability statement about where the true value lives.

**Finance example:**

You estimate a fund's annual return as 8% with a 95% CI of (2%, 14%). This means: if you re-ran this study 100 times with different samples of returns, 95 of the resulting intervals would contain the fund's true expected annual return.

**How to construct a CI:**

For a mean with known population variance: x̄ ± z_{α/2} × (σ/√n)

Where z_{α/2} is the Normal quantile (1.96 for 95%). The width depends on:
- **n:** more data → narrower interval (√n in denominator)
- **σ:** more variability → wider interval
- **confidence level:** higher confidence → wider interval

---

## t-Distribution vs Normal

When you don't know the population variance (almost always in practice), you estimate it from the data. This introduces additional uncertainty — your estimate of σ might be off, especially with small samples.

The **t-distribution** accounts for this. It has heavier tails than the Normal — it spreads more probability into extreme values to reflect the fact that with small n, your sample could be unusually unrepresentative.

As n → ∞, the t-distribution converges to Normal. With n > 30 or so, the difference is negligible for most purposes.

Practical rule: use t when estimating a mean with unknown variance. Always. The extra caution hurts nothing with large n and protects you with small n.

---

## Bootstrap CI vs Analytical CI

**Analytical CI:** Use a formula derived from distributional theory. Fast, exact when assumptions hold.

**Bootstrap CI:** Resample your data, compute your statistic each time, take percentiles. Works for any statistic, no distributional assumptions needed.

**When to use each:**

Use analytical CI when you have a formula (mean, proportion) and your sample size is reasonable.

Use bootstrap CI when no formula exists (Sharpe ratio, median, correlation coefficient), when assumptions are questionable, or when you want a quick check on the analytical result.

The bootstrap CI and analytical CI should give similar answers for the mean with large n. If they diverge substantially, something is unusual about your data's distribution.

---

## How This Connects to the Homework

- **Q15:** Point estimation — comparing MOM and MLE for the same parameter
- **Q16:** MLE derivation for a specific distribution (Normal, Poisson)
- **Q17:** Comparing MOM vs MLE estimates on NHANES data
- **Q18–Q19:** Confidence intervals — construction, interpretation, width
- **Q20:** Coverage — simulating 100 CIs and checking how many contain the true value
- **Part 8B:** MLE for logistic regression vs MOM for marginal prevalence

---

# Chapter 4: Hypothesis Testing

## The Logic

Hypothesis testing is structured around a default assumption that you're trying to disprove.

**H₀ (null hypothesis):** The boring, default world. Nothing interesting is happening. The mean is zero. The two groups are the same. The relationship doesn't exist.

**H₁ (alternative hypothesis):** Something interesting is happening. The mean is non-zero. The groups differ. The relationship exists.

**The procedure:** Assume H₀ is true. Compute how surprising your data would be in that world. If the data is sufficiently surprising, reject H₀.

The analogy is a criminal trial. The defendant is innocent (H₀) until proven guilty. Evidence must be strong enough to convict (reject H₀). Failing to convict doesn't prove innocence — it just means the evidence wasn't strong enough.

---

## The p-value

> The most abused number in science.

The **p-value** is the probability of observing data as extreme as yours (or more extreme), assuming H₀ is true.

**What it IS:** P(data this extreme | H₀ true).

**What it is NOT:**
- The probability H₀ is true: NO.
- The probability your result is due to chance: NO.
- A measure of effect size or practical importance: NO.
- Evidence that H₁ is true: not directly.

**Finance example:** You test whether a trading strategy has non-zero mean return. H₀: mean return = 0. You observe a mean of +0.15% per day over 252 days. The t-statistic is 2.3, p-value = 0.022.

This means: if the strategy truly had zero expected return, you'd observe a mean return this far from zero only 2.2% of the time by chance. That's unlikely enough to doubt H₀.

The p-value does NOT say there's a 97.8% probability the strategy is profitable.

---

## Type I and Type II Errors

When you make a decision based on a hypothesis test, two kinds of errors are possible:

**Type I error (False Positive):** Reject H₀ when it's actually true. Convict an innocent person. Declare a useless trading strategy profitable.

**Type II error (False Negative):** Fail to reject H₀ when it's actually false. Acquit a guilty person. Miss a genuinely profitable strategy.

The **significance level α** controls the Type I error rate. Setting α = 0.05 means you're willing to be wrong 5% of the time when H₀ is true.

**The tradeoff:** Making α smaller (stricter standard) reduces Type I errors but increases Type II errors — you miss more real effects. Power (1 - P(Type II error)) and significance level pull in opposite directions. This is fundamental and unavoidable.

---

## Effect Size

> Statistical significance is not the same as practical significance.

A study with n = 1,000,000 observations can find that two strategies differ by 0.0001% annually — statistically significant (tiny p-value) but economically meaningless.

**Cohen's d** measures effect size for comparisons of means: d = (μ₁ - μ₂) / σ_pooled. It measures the difference in standard deviation units.

Rough guidelines: d = 0.2 is small, d = 0.5 is medium, d = 0.8 is large.

**Finance example:** Strategy A has mean daily return 0.12%, Strategy B has 0.10%, pooled σ = 0.15%. Cohen's d = (0.12 - 0.10) / 0.15 = 0.13. Small effect. Even if statistically significant with large n, the practical difference is tiny.

Always report effect sizes alongside p-values. A result can be statistically significant and practically irrelevant.

---

## One-Sample t-test

Tests whether a sample mean equals a hypothesized value.

**Finance example:** Does this trading strategy have non-zero expected return? H₀: μ = 0. Collect 252 daily returns. Compute t = (x̄ - 0) / (s / √n). Compare to t-distribution with 251 degrees of freedom.

The t-statistic asks: how many standard errors is the sample mean from zero? If it's far from zero (large |t|), the strategy likely has non-zero expected return.

---

## Two-Sample t-test (Welch's)

Tests whether two independent groups have the same mean.

Welch's t-test does not assume equal variances — it uses a separate variance estimate for each group and adjusts the degrees of freedom. This is almost always the right choice over the equal-variance version.

**Finance example:** Do tech stocks have higher mean returns than utility stocks over the past 5 years? Two groups (tech, utilities), compare means. Welch's t-test handles the fact that tech stocks are much more volatile (higher variance) than utilities.

---

## Paired t-test

When observations come in natural pairs — before/after, same-day measurements on two instruments, the same portfolio under two conditions.

**Finance example:** A portfolio manager tests a new rebalancing rule. They compare portfolio performance in Q1 (old rule) vs Q2 (new rule) across 20 portfolios. The portfolios are the same entities measured under different conditions — paired data. Using a paired t-test removes the noise from between-portfolio differences, focusing only on the within-portfolio effect of the rule change.

Paired t-test is just a one-sample t-test applied to the differences.

---

## ANOVA (Analysis of Variance)

Extends the two-sample t-test to more than two groups.

**Finance example:** Do mean monthly returns differ across five market sectors (tech, finance, healthcare, energy, utilities)? Five groups — can't just run 10 pairwise t-tests (multiple comparisons problem, coming up).

ANOVA tests H₀: all group means are equal, H₁: at least one group mean differs.

**F-statistic intuition:** F = (variance between group means) / (variance within groups). If the groups truly have the same mean, the between-group variance should just reflect random sampling — it should be similar to the within-group variance. A large F means groups vary more than chance would suggest.

---

## Chi-Squared Test

Tests independence between two categorical variables.

**Finance example:** Is there a relationship between market regime (Bull/Bear/Sideways) and investor behavior (buy/hold/sell)? Build a 3×3 table of counts. Chi-squared tests whether the cell counts are consistent with independence or show a real relationship.

The chi-squared statistic sums (observed - expected)² / expected across all cells. Under independence, this follows a chi-squared distribution with (rows-1)×(cols-1) degrees of freedom.

---

## Non-Parametric Tests

When the parametric tests' assumptions (especially normality) don't hold, non-parametric tests analyze ranks instead of values.

**Mann-Whitney U:** Non-parametric alternative to Welch's t-test. Doesn't assume normality. Tests whether one group tends to have higher values than another.

**Finance application:** Comparing two strategies' daily returns when the distribution is heavily skewed (not Normal). Mann-Whitney ranks all returns together and tests whether one strategy tends to rank higher.

**Wilcoxon signed-rank:** Non-parametric alternative to paired t-test. Ranks the absolute values of the differences and tests whether positive differences dominate negative ones.

**Kruskal-Wallis:** Non-parametric ANOVA. Ranks all observations together and tests whether groups differ.

**When to prefer non-parametric:** Small samples, heavy-tailed distributions, ordinal data, when Shapiro-Wilk rejects normality and n isn't large enough for CLT to protect you.

**When parametric is fine despite non-normality:** Large samples (n > 30 per group). By CLT, the sampling distribution of the mean is approximately Normal regardless of the data distribution.

---

## Multiple Comparisons

Suppose you test 20 trading strategies. Even if none of them work, each test has a 5% chance of a false positive. With 20 tests, the probability of at least one false positive is: 1 - (1-0.05)^20 ≈ 64%.

You'll almost certainly "find" a winning strategy by chance. This is the multiple comparisons problem, and it's rampant in quantitative finance (and elsewhere).

**Family-Wise Error Rate (FWER):** The probability of at least one false positive across all tests.

**Bonferroni correction:** Divide α by the number of tests. If testing 20 strategies with α = 0.05, require p < 0.05/20 = 0.0025 for each individual test. Controls FWER ≤ α. Very conservative.

**Holm-Bonferroni:** Sort p-values from smallest to largest. Apply a progressively less strict threshold. Controls FWER at α but with more power than Bonferroni.

**Benjamini-Hochberg (BH):** Controls the **False Discovery Rate** — the expected fraction of rejected null hypotheses that are actually true. Less strict than FWER control. More appropriate in exploratory settings where you want to identify candidates, not make definitive claims.

**Finance application:** You've tested 50 potential signals for a trading strategy. BH at 10% FDR means that of the signals you declare "significant," you expect about 10% to be false positives. You can then investigate those candidates further before deploying capital.

---

## How This Connects to the Homework

- **Q21:** One-sample t-test on BMI — is mean BMI equal to a population target?
- **Q22:** Two-sample t-test (Welch's) — does mean BP differ by gender?
- **Q23:** Paired t-test — same individual measured under two conditions
- **Q24:** ANOVA + multiple comparison corrections (Bonferroni, Holm, BH) across racial groups
- **Q25:** Mann-Whitney U — non-parametric repeat of Q22
- **Q26:** Wilcoxon signed-rank — non-parametric repeat of Q23
- **Q27:** Kruskal-Wallis — non-parametric ANOVA
- **Q28:** Essay on parametric vs non-parametric — synthesizes the whole chapter
- **Part 8C:** Full hypothesis testing battery on diabetes predictors

---

# Chapter 5: Linear & Multiple Regression

## What Regression Does

You have two variables. You suspect one influences the other. You want to quantify that relationship: how much does Y change for a one-unit change in X? And how much of Y's variation can X explain?

**Finance example:** How much does a portfolio's daily return change for each 1% move in the S&P 500? This is exactly the regression question. The answer — beta — is the single most important number in the CAPM (Capital Asset Pricing Model).

---

## Simple Linear Regression

The model: **Y = β₀ + β₁X + ε**

Y is the outcome. X is the predictor. β₀ is the intercept (value of Y when X = 0). β₁ is the slope (how much Y changes for a one-unit increase in X). ε is the error term — the part of Y that X doesn't explain.

**What "best fit" means — Ordinary Least Squares (OLS):**

The line that minimizes the sum of squared residuals: Σ(yᵢ - ŷᵢ)².

Why squared? Two reasons:
1. Penalizes large errors more than small ones. Missing by 10 is worse than missing by 5 twice.
2. The squared function is smooth and differentiable — you can find the minimum analytically by setting the derivative to zero.

**The OLS solution:**
β̂₁ = Cov(X, Y) / Var(X) — slope equals the covariance of X and Y divided by the variance of X
β̂₀ = ȳ - β̂₁ x̄ — intercept ensures the line passes through the point of means

**Geometric intuition:** The regression line is the "shadow" of the Y variable projected onto the X axis. It finds the linear relationship that explains as much variance in Y as possible.

---

## R² — Coefficient of Determination

**R²** = fraction of variance in Y explained by X.

R² = 1 - (sum of squared residuals) / (total sum of squares)
= 1 - Var(residuals) / Var(Y)

If R² = 0.65: X explains 65% of the variation in Y. The remaining 35% is unexplained noise.

**Finance example:** Regressing a tech stock's daily returns on the S&P 500 returns. R² = 0.72 means 72% of the stock's daily variation is explained by market moves. Beta (the slope) tells you how much — a beta of 1.3 means the stock moves 1.3% for every 1% market move.

**What R² doesn't tell you:**
- Whether the relationship is causal
- Whether the model is appropriate (R² can be high for terrible models)
- Whether other variables matter

---

## Assumptions of OLS (LINE)

**L — Linearity:** The relationship between X and Y is linear. If the true relationship is curved, a straight line will systematically misfit the data.

**I — Independence:** Observations are independent. In time series (stock returns), this can fail — today's return may be correlated with yesterday's.

**N — Normality of residuals:** Residuals (errors) should be approximately Normal. Needed for inference (confidence intervals, hypothesis tests on coefficients). With large n, CLT makes inference robust to this.

**E — Equal variance (Homoscedasticity):** The variance of errors should be constant across all values of X. Stock returns violate this — volatility clusters, meaning high-volatility periods have much larger errors than calm periods. This is **heteroscedasticity**.

**How to check each:**
- Linearity: plot residuals vs fitted values. Should see a random scatter, not a curve.
- Independence: for time series, plot residuals over time. Patterns indicate autocorrelation.
- Normality: Q-Q plot of residuals. Should follow a straight line.
- Equal variance: plot residuals vs fitted values. Width should be constant, not funneling.

---

## Multiple Regression

Add more predictors: **Y = β₀ + β₁X₁ + β₂X₂ + ... + βₖXₖ + ε**

Each coefficient β_j is the expected change in Y for a one-unit increase in X_j, **holding all other predictors constant**.

This "holding constant" is critical. It means multiple regression answers a different question than simple regression — it isolates the partial effect of each predictor.

**Finance example:** Predicting stock return using market return (beta), size factor, and value factor — the Fama-French three-factor model. Each coefficient is the marginal contribution of that factor, holding the others constant. Beta tells you market sensitivity after accounting for size and value effects.

---

## Multicollinearity

When predictors are highly correlated with each other, it's hard to isolate their individual effects.

**Finance example:** You include both "10-year Treasury yield" and "Federal Funds Rate" as predictors. These move together closely. The model can't tell which one is driving the outcome — coefficients become unstable and standard errors balloon.

**VIF (Variance Inflation Factor)** measures how much each predictor's variance is inflated by its correlation with others. VIF = 1 means no multicollinearity. VIF > 10 is a serious problem.

The fix: remove one of the correlated predictors, combine them (principal components), or accept that you can't isolate individual effects.

---

## Heteroscedasticity

When error variance is not constant, OLS estimates are still unbiased but standard errors are wrong — which means your t-tests and confidence intervals are unreliable.

**Finance example:** Volatility clustering. During calm periods, daily return residuals are small. During crises (2008, 2020), residuals are enormous. A model fit to the whole period will have residuals whose variance clearly depends on the time period. Standard OLS SEs will be too small during crises (underestimating uncertainty) and too large during calm periods.

**Breusch-Pagan test:** Regress the squared residuals on the predictors. If the predictors explain the squared residuals well, variance isn't constant — heteroscedasticity confirmed.

**Fixes:** Robust standard errors (Huber-White), Weighted Least Squares, log-transforming the outcome.

---

## Model Selection

Adding any variable to a regression — even noise — always increases R². So R² alone can't tell you whether a variable improves the model.

**Adjusted R²** penalizes for adding predictors: Adjusted R² = 1 - (1 - R²)(n-1)/(n-k-1). Only increases if a new predictor improves fit more than chance alone would.

**AIC (Akaike Information Criterion):** AIC = -2 log(likelihood) + 2k. Lower is better. Penalizes complexity by 2 per parameter. Balances fit (log-likelihood) against parsimony (2k).

**BIC (Bayesian Information Criterion):** BIC = -2 log(likelihood) + k·log(n). Like AIC but with a stronger penalty for complexity that grows with n. BIC tends to select simpler models.

**The principle:** you want the simplest model that adequately explains the data. Occam's razor applied to statistics.

---

## Overfitting

A model that has too many parameters relative to the data size can fit the training data perfectly but fail completely on new data.

**Finance analogy:** You have 10 years of S&P 500 data. You find a strategy that perfectly predicts the index based on the number of letters in the winner of the Super Bowl. p-value = 0.0001. R² = 0.97. This is pure noise-fitting — the pattern is a coincidence that won't replicate.

The fix: test your model on data it hasn't seen. Split into training and test sets. Cross-validation formalizes this.

---

## Interaction Terms

An interaction term captures when the effect of X₁ on Y depends on the level of X₂.

Model: Y = β₀ + β₁X₁ + β₂X₂ + β₃(X₁ × X₂) + ε

β₃ is the interaction coefficient. If β₃ ≠ 0, the slopes for X₁ and X₂ change depending on each other.

**Finance example:** Effect of leverage on return. High leverage amplifies both gains and losses. But the effect of leverage depends on market volatility. In a calm market (low volatility), leverage increases return modestly. In a volatile market, leverage is devastating. The interaction term captures that the slope for leverage depends on the level of market volatility.

---

## How This Connects to the Homework

- **Q29:** Multiple regression setup — predicting systolic BP from multiple predictors
- **Q30:** Residual diagnostics — checking OLS assumptions visually
- **Q31:** VIF — detecting multicollinearity
- **Q32:** Heteroscedasticity test and correction
- **Q33:** Model selection with AIC/BIC/adjusted R²
- **Q34:** Prediction intervals vs confidence intervals for new observations
- **Q35:** Interaction term — does effect of BMI on BP depend on age?
- **Part 8D:** Logistic regression for diabetes — binary outcome extension of linear regression

---

# Chapter 6: Stochastic Processes

## What Is a Stochastic Process?

A **stochastic process** is a sequence of random variables indexed by time.

A single stock price tomorrow is a random variable. The entire path of the stock price from today to one year from now — every daily close, every minute — is a stochastic process. It's not one number; it's an entire trajectory of random numbers that evolve over time.

The central question of stochastic processes: **how does randomness unfold through time?** Not just "what is the distribution of tomorrow's price?" but "what patterns emerge over long time horizons? What's the long-run behavior? How fast does uncertainty accumulate?"

---

## The Markov Property

A stochastic process has the **Markov property** if the future depends only on the present state, not on the history of how you got there.

Formally: P(Xₜ₊₁ = x | Xₜ, Xₜ₋₁, ..., X₀) = P(Xₜ₊₁ = x | Xₜ)

**Finance example:** The random walk model of stock prices says that tomorrow's price depends only on today's price, not on the path that led to today's price. Whether the stock rose steadily to reach $100, or crashed from $150 to $100 — in a random walk, tomorrow's move distribution is the same. The Markov property is what makes the random walk tractable.

Whether stock prices are truly Markovian is contested. Technical analysts believe historical patterns (head-and-shoulders, moving averages) predict future moves — implying the process is not Markovian. The Efficient Market Hypothesis says prices are Markovian: all historical information is already reflected in today's price.

---

## Discrete-Time Markov Chains (DTMC)

A **DTMC** is a Markov process where the state space is discrete (a finite set of states) and time advances in discrete steps.

**Example — market regime model:**

States: Bull market, Bear market, Sideways.

**Transition matrix P:**

|            | → Bull | → Bear | → Sideways |
|------------|--------|--------|------------|
| From Bull  | 0.70   | 0.15   | 0.15       |
| From Bear  | 0.30   | 0.50   | 0.20       |
| From Sideways | 0.40 | 0.25  | 0.35       |

Each row is a probability distribution over next states. Rows must sum to 1.

If you're in a Bull market this month, there's a 70% chance you're still in a Bull market next month, 15% chance it turns Bear, 15% chance it goes Sideways.

**Stationary distribution:** The long-run fraction of time the system spends in each state, regardless of where it starts. Solve πP = π (the stationary distribution is a left eigenvector of P with eigenvalue 1). If you start the system from any state and let it run forever, it converges to the stationary distribution.

**Irreducibility:** Every state can be reached from every other state. In the market regime example, you can always get from Bull to Bear (directly or via Sideways). An irreducible chain has a unique stationary distribution.

**Aperiodicity:** The chain doesn't cycle with a fixed period. Necessary for convergence to the stationary distribution.

**Absorbing states:** States you can never leave once entered. P(stay | absorbing) = 1.

**Finance example — credit ratings:** A company can be AAA, AA, A, BBB, BB, B, C, or Default. Default is an absorbing state — once a company defaults, it stays defaulted (in this simplified model). Starting from any rating, what's the probability of eventually defaulting? This is the absorption probability, solved using the **fundamental matrix**: N = (I - Q)⁻¹ where Q is the sub-matrix of transitions between non-absorbing states.

---

## Continuous-Time Markov Chains (CTMC)

The same idea as DTMC, but time flows continuously. Instead of "what's the probability of transitioning in the next step," you ask "what's the rate of transitioning per unit time."

The **generator matrix Q** (also called the rate matrix) replaces the transition matrix. Off-diagonal entries qᵢⱼ > 0 are transition rates from state i to state j. Diagonal entries are negative: qᵢᵢ = -Σⱼ≠ᵢ qᵢⱼ (leaving rate must balance entering rates to ensure rows sum to zero).

The transition probability matrix at time t is: **P(t) = e^{Qt}**

This is the **matrix exponential** — the continuous-time analog of raising a matrix to a power. Intuition: it's like continuous compounding. Just as a bank account with continuously compounded rate r has value e^{rt} at time t, a Markov chain with rate matrix Q has transition probabilities e^{Qt} at time t.

**Finance example — bond credit rating transitions:**

A bond can transition from BBB to BB, or to A, at any moment — not just at year-end. Moody's and S&P publish historical migration rates. These form the generator matrix Q. Then P(t) = e^{Qt} gives the transition probability matrix over any time horizon t.

Long-run behavior: as t → ∞, P(t) converges to a matrix where every row is the stationary distribution π — same stationary distribution as the corresponding DTMC.

---

## Random Walks

The simplest stochastic process. At each time step, add a random increment.

**Symmetric random walk:** At each step, move +1 or -1 with equal probability 0.5.

Key properties:
- E[position after n steps] = 0 (expected position = starting position — fair game)
- Var(position after n steps) = n (variance grows linearly with time)
- Std dev = √n (uncertainty grows as the square root of time)

This "square root of time" scaling is fundamental. In finance, the standard deviation of a price move over n days scales as σ√n, where σ is the daily volatility. That's why annual volatility (252 trading days) is approximately σ_daily × √252.

**Connection to Brownian motion:** Take the random walk, scale the step size down and time steps up, and in the limit you get **Brownian motion** (also called a Wiener process). Stock prices in the Black-Scholes model follow geometric Brownian motion — exponential Brownian motion to keep prices positive.

---

## Poisson Process

The fundamental model for events that arrive randomly over continuous time at a constant average rate.

**Three equivalent characterizations:**

1. **Counting process:** N(t) = number of events by time t. Increments are independent. N(t) - N(s) ~ Poisson(λ(t-s)).

2. **Inter-arrival times:** The time between consecutive events follows Exponential(λ). The Exponential distribution is memoryless: P(wait > s+t | wait > s) = P(wait > t). How long you've already waited tells you nothing about how much longer you'll wait.

3. **Window counts:** The number of events in any fixed window of length Δt follows Poisson(λΔt).

**Finance example — order arrival:** Buy orders arrive at rate λ = 200 per minute during normal trading. The count in any 5-minute window follows Poisson(1000). The time between consecutive orders follows Exponential(200) — with mean 0.005 minutes = 0.3 seconds per order.

During a market shock, order arrival rates spike. The Poisson process with higher λ models this.

**Memoryless property importance:** If you've been waiting for a large institutional trade for 10 minutes, the Exponential model says the expected additional wait is the same as when you started waiting. Past waiting time is irrelevant. This is the mathematical content of "the market doesn't remember."

---

## Non-Homogeneous Poisson Process (NHPP)

The standard Poisson process has a constant rate λ. Real trading doesn't — volume follows predictable intraday patterns: high at open (9:30am), lower at midday, high at close (4pm), nearly zero overnight.

The **NHPP** allows λ to vary with time: λ(t). Everything else stays the same, but the rate is now a function.

**Thinning method for simulation:** Generate a standard Poisson process at the maximum rate λ_max. For each event at time t, accept it with probability λ(t)/λ_max; reject it with probability 1 - λ(t)/λ_max. The accepted events form an NHPP with rate λ(t).

Intuition: you generate too many events, then thin the herd by randomly discarding events where the rate is lower. During the midday lull, most generated events get discarded. At open and close, most get accepted.

---

## Bernoulli Process

The discrete-time counterpart of the Poisson process. At each time step, an event either occurs (probability p) or doesn't (probability 1-p).

**Binomial connection:** Count the number of events in n time steps → Binomial(n, p).

**Geometric connection:** Time until the first event follows Geometric(p). If p = 0.1, you expect to wait 1/p = 10 steps on average.

**The discrete-continuous duality:**

| Discrete (Bernoulli) | Continuous (Poisson) |
|---------------------|----------------------|
| Bernoulli trial | Poisson instant |
| Binomial(n, p) | Poisson(λt) |
| Geometric(p) | Exponential(λ) |

Both model event processes. Bernoulli operates in discrete steps; Poisson operates in continuous time. As step size → 0 and p → 0 with p/step_size = λ, Bernoulli converges to Poisson.

---

## Superposition and Thinning

Two beautiful closure properties of Poisson processes:

**Superposition:** Merge two independent Poisson processes with rates λ₁ and λ₂. The combined process is Poisson(λ₁ + λ₂).

**Finance example:** Buy orders arrive as Poisson(λ₁ = 150/min) and sell orders as Poisson(λ₂ = 130/min). Total order flow arrives as Poisson(280/min). This is the superposition property.

**Thinning:** Take a Poisson(λ) process. For each event, independently label it type A with probability p or type B with probability 1-p. The type A sub-process is Poisson(pλ); the type B sub-process is Poisson((1-p)λ).

**Finance example:** All trades arrive as Poisson(280/min). 54% are buys (p = 0.54). Buy order sub-process: Poisson(0.54 × 280) = Poisson(151). Sell order sub-process: Poisson(0.46 × 280) = Poisson(129). Both sub-processes are independently Poisson.

These properties explain why the Poisson process is the default model for financial order flow — it's closed under the most natural operations you'd want to perform on it.

---

## How This Connects to the Homework

- **Q36:** DTMC — BMI health state transitions, estimating the transition matrix, stationary distribution
- **Q37:** Random walk — systolic BP over 250 simulated steps
- **Q38:** Markov chain classification — irreducible? aperiodic? recurrent?
- **Q39:** Absorption probabilities — starting from Healthy, probability of eventual Obese state
- **Q40:** CTMC — converting the discrete chain to continuous time with matrix exponential
- **Q41:** Poisson process — modeling diabetes events, verifying all three characterizations
- **Q42:** NHPP — age-dependent event rate, thinning simulation
- **Q43:** Bernoulli process — each person as Bernoulli trial, Binomial/Geometric verification
- **Q44:** Superposition and thinning — diabetes + hypertension processes merged and split

---

# Chapter 7: Bayesian Statistical Inference

## A Different Philosophy of Probability

Classical (frequentist) statistics treats parameters as fixed but unknown. Probability describes long-run frequencies of outcomes over hypothetical repetitions.

**Bayesian statistics treats parameters as random variables.** Probability is your degree of belief about the parameter's value. Before seeing data, you have a prior belief. After seeing data, you update that belief. The result is a posterior distribution — a full probability distribution over the parameter.

This is philosophically different. And practically more powerful for many problems.

> **Core equation:** Posterior ∝ Likelihood × Prior

Read this as: what you believe after seeing data is proportional to how probable the data is given each parameter value, times what you believed before seeing data.

---

## Prior, Likelihood, Posterior

**Prior distribution:** Encodes your beliefs about the parameter before observing data. Can be based on previous studies, domain expertise, or no information at all (uninformative prior).

**Likelihood:** For a given parameter value, how probable is the data you observed? This is exactly the MLE likelihood function from Chapter 3 — but now we don't just maximize it, we use it to update beliefs.

**Posterior distribution:** The updated belief after combining prior and likelihood through Bayes' theorem.

**Finance example — estimating a strategy's true win rate:**

You're evaluating a trading strategy. From backtesting, you believe the win rate θ is somewhere around 55%, but you're uncertain. Before trading, you have a prior: θ ~ Beta(11, 9) — centered at 55% (11/20 = 0.55) with moderate certainty.

You run the strategy live for 30 trades and win 18.

Likelihood: how probable is "18 wins in 30 trades" for each possible θ? The Binomial likelihood peaks near θ = 18/30 = 0.60.

Posterior: combine prior and likelihood. Because of conjugacy (next section), the posterior is Beta(11+18, 9+12) = Beta(29, 21). Mean = 29/50 = 0.58. You've shifted from believing 55% to believing 58%, weighted toward the data.

---

## Conjugate Priors

**Conjugacy** means the prior and posterior belong to the same distribution family. The posterior calculation reduces to updating a few numbers — no complex integration needed.

### Beta-Binomial Conjugacy

**Setup:** You want to estimate a proportion θ (win rate, default rate, conversion rate).

**Prior:** θ ~ Beta(a, b). The mean is a/(a+b). Larger a+b = more concentrated prior = more confident.

**Data:** k successes in n trials.

**Posterior:** θ | data ~ Beta(a+k, b+n-k).

**The update in words:** Start with a Beta prior. Each observed success adds 1 to the a parameter (the "success counter"). Each observed failure adds 1 to the b parameter (the "failure counter"). The parameters accumulate evidence.

**Prior sensitivity:**

| Prior | a+b | Concentration | Data needed to overwhelm |
|-------|-----|---------------|--------------------------|
| Beta(1,1) | 2 | Very weak | Even 10 observations dominate |
| Beta(2,18) | 20 | Weak | ~50 observations |
| Beta(50,450) | 500 | Strong | ~1000 observations |

When your sample size n >> a+b, the likelihood dominates and the posterior is nearly identical regardless of prior. When n is small, the prior matters a lot.

**Finance application:** After 30 live trades, the strong prior would barely move; the weak prior would be dominated by data. This is the practical question when evaluating a new strategy: how many trades do you need before the prior doesn't matter?

### Normal-Normal Conjugacy

**Setup:** You want to estimate a mean μ from Normal data with known variance σ².

**Prior:** μ ~ Normal(μ₀, τ₀²). Your prior belief about the mean.

**Data:** n observations with sample mean x̄.

**Posterior:** μ | data ~ Normal(μ_n, τ_n²) where:

τ_n² = 1 / (1/τ₀² + n/σ²)  [posterior variance]
μ_n = τ_n² × (μ₀/τ₀² + n·x̄/σ²)  [posterior mean]

**The posterior mean in words:** It's a weighted average of the prior mean μ₀ and the data mean x̄. The weights are the precisions (inverse variances). More data → data gets more weight. More certain prior → prior gets more weight.

**Finance application:** Estimating the true expected return of a fund manager. Prior: typical manager earns 2% annually over benchmark, with uncertainty τ₀ = 5% (Normal(0.02, 0.05²)). After observing 3 years of outperformance averaging 6%, the posterior is a weighted average: somewhere between 2% (prior) and 6% (data), leaning toward data but not fully there. This is the statistical basis of "regression to the mean" in fund performance evaluation.

---

## Credible Intervals vs Confidence Intervals

**95% Confidence Interval:** If you repeat your experiment 100 times, approximately 95 of the resulting intervals will contain the true parameter. Any specific interval either does or doesn't contain the true value — there's no probability about it.

**95% Credible Interval:** Given your prior and the data, there's a 95% probability the parameter lies in this interval.

The Bayesian credible interval is what most people intuitively want to compute. "What values of θ are plausible given what I've observed?" The frequentist CI answers a more tortured question about hypothetical repetitions.

With large samples and weak priors, the two intervals are numerically very similar. The philosophical difference matters more than the practical one in most applications.

---

## Bayesian Hypothesis Testing and Bayes Factors

Frequentist hypothesis testing asks: if H₀ is true, how surprising is our data?

Bayesian hypothesis testing asks: after seeing the data, which hypothesis do we believe more?

**Posterior probability of a hypothesis:** Directly compute P(H₁ | data). If the posterior distribution puts 99% of probability above zero, you have 99% posterior probability that the parameter is positive.

**Bayes Factor:** BF = P(data | H₁) / P(data | H₀). How much more likely is the data under H₁ than H₀?

**Jeffreys' scale:**
- BF < 1: Evidence for H₀
- BF 1–3: Barely worth mentioning
- BF 3–10: Substantial evidence for H₁
- BF 10–30: Strong evidence
- BF 30–100: Very strong evidence
- BF > 100: Decisive evidence

**Comparison with p-value:** A p-value of 0.03 says the data would be unusual if H₀ were true. A Bayes Factor of 15 says the data is 15 times more probable under H₁ than H₀. These are measuring different things. The Bayes Factor directly compares hypotheses; the p-value interrogates only H₀.

---

## MCMC — Markov Chain Monte Carlo

Most posterior distributions don't have the nice conjugate-family form. They're high-dimensional, complex integrals with no closed-form solution.

**MCMC** is the computational engine that makes Bayesian inference practical for complex models.

**The idea:** Instead of computing the posterior analytically, construct a Markov chain whose stationary distribution IS the posterior. Run the chain for thousands of steps. Collect samples. The collection of samples approximates the posterior distribution.

**Metropolis-Hastings intuitively:**

1. Start at some parameter value θ₀.
2. Propose a new value θ* by perturbing θ₀ slightly (e.g., add a random Normal noise).
3. Compute the acceptance ratio: r = P(data | θ*) × P(θ*) / [P(data | θ₀) × P(θ₀)]
4. If r ≥ 1 (new proposal is at least as good): accept θ* and move there.
5. If r < 1: accept θ* with probability r, reject with probability 1-r.
6. Repeat thousands of times.

This creates a random walk through parameter space that spends more time in regions of high posterior probability. After a "warmup" period where the chain finds the high-probability region, the subsequent samples trace out the posterior distribution.

**Convergence diagnostics:**

**Trace plots:** Plot the sampled values over time. Good mixing looks like a "fuzzy caterpillar" — rapid variation around a stable center. Slow drift or periodic patterns indicate poor mixing.

**R-hat (Gelman-Rubin statistic):** Run multiple chains from different starting points. Compare within-chain variance to between-chain variance. R-hat ≈ 1.0 means chains have converged to the same distribution. R-hat > 1.1 is a warning.

---

## Bayesian Linear Regression

Instead of one coefficient estimate, you get a full posterior distribution over each coefficient.

**Prior:** β_j ~ Normal(0, σ_prior²). Weakly informative — centered at zero, allowing the data to pull the posterior wherever it wants.

**Posterior:** After observing the data, the posterior for each β_j is a distribution rather than a point. You can ask: what's the probability the coefficient for "market volatility" is negative? You can answer that directly.

**Posterior predictive distribution:** For a new observation x_new, the prediction ŷ has both model uncertainty (uncertainty in the coefficients) and noise uncertainty (σ_error). This gives a wider, more honest prediction interval than frequentist approaches.

---

## Bayesian A/B Testing

**Frequentist A/B:** Collect data. Compute p-value for H₀: conversion rates are equal. If p < 0.05, ship variant B.

**Bayesian A/B:** Model the conversion rate of each variant as a random variable. Update the prior with observed conversions. Compute:
- P(θ_B > θ_A | data) — probability variant B is truly better
- P(θ_B - θ_A > δ | data) — probability the advantage exceeds some meaningful threshold δ

**Why Bayesian A/B is better for decision-making:**

Suppose you've collected 1,000 observations. The Bayesian posterior says P(B > A) = 0.87 and P(B exceeds A by more than 5% lift) = 0.62.

You can make a business decision: "We're 87% sure B is better, but only 62% sure the improvement is big enough to matter. We'll ship B but continue monitoring."

Frequentist A/B only tells you whether to reject or not reject H₀ — it doesn't give you probabilities over the business-relevant question.

---

## Hierarchical Models

**The problem:** You want to estimate something for each of 50 groups (e.g., expected return for each of 50 fund managers). Options:

1. **No pooling:** Estimate each manager independently. Small funds with 1-2 years of data have huge uncertainty. Estimates are unreliable.

2. **Complete pooling:** Treat all managers as identical. Ignore manager-specific information. Loses all group-level insight.

3. **Partial pooling (hierarchical model):** Assume each manager's true alpha is drawn from a common distribution (the hyperprior). Estimate that distribution and each manager's alpha simultaneously.

**The result: shrinkage.** Each group's estimate is pulled toward the global mean. Groups with little data shrink most — their estimates lean heavily on the hyperprior. Groups with much data shrink least — their estimates are dominated by their own data.

**Finance application — fund-of-funds:** You manage a fund that invests in 30 sub-funds. Each sub-fund manager has a different track record length and return history. Hierarchical modeling gives you:
- Calibrated estimates for managers with short track records (shrunk toward the population of managers)
- More confident estimates for managers with long track records (dominated by their own data)
- An estimate of the distribution of skill across all managers (the hyperprior)

This is the statistical basis of the James-Stein estimator — which famously showed that pooling information across groups reduces estimation error even when groups are unrelated.

---

## How This Connects to the Homework

- **Q45:** Beta-Binomial conjugacy — estimating diabetes prevalence with three different priors
- **Q46:** Normal-Normal conjugacy — estimating mean BMI with a Normal prior
- **Q47:** Bayesian hypothesis testing — P(μ > 25 | data) and Bayes Factor
- **Q48:** Bayesian linear regression with PyMC — MCMC sampling, trace plots, R-hat
- **Q49:** Bayesian A/B test — physically active vs inactive groups, posterior of difference
- **Q50:** Hierarchical model — mean BMI by racial group with shared hyperprior, shrinkage
- **Q51:** Essay comparing Bayesian and frequentist approaches — synthesizes the whole chapter

---

# Chapter 8: Applied Data Analysis Workflow

## The Full Pipeline

A data analysis project is not a sequence of statistical tests — it's a workflow that connects a question to an answer. The best analyses are coherent: every choice (what data to collect, how to clean it, which model to use, how to communicate results) flows from the original question.

**The pipeline:**

1. **Question:** What do you actually want to know? Be precise. "Does exercise affect health?" is too vague. "Do adults who exercise ≥3 days per week have lower systolic blood pressure than sedentary adults, controlling for age and BMI?" is a testable question.

2. **Data:** What data can answer this question? What's missing? What are the limitations?

3. **EDA:** Look before you model. Understand the distribution of each variable, spot anomalies, form hypotheses.

4. **Preprocessing:** Handle missing values, encode categories, scale features.

5. **Model:** Choose the appropriate statistical model based on the question and data structure.

6. **Test:** Evaluate the model's claims — are the patterns real or noise? Are assumptions satisfied?

7. **Communicate:** Translate results into language your audience understands.

---

## Exploratory Data Analysis

EDA is detective work. You're looking for:

**Distributions:** What's the shape? Normal? Skewed? Bimodal? Outliers? A return distribution that looks Normal but has fat tails matters enormously for risk management.

**Missing data patterns:** Is missingness random, or does it correlate with other variables? If high-income individuals systematically skip income questions, your income data is not missing at random.

**Correlations:** Which variables move together? The correlation matrix gives you a quick overview. But correlation matrices lie — Anscombe's quartet shows four datasets with identical correlations, means, and variances that have completely different shapes (linear, curved, with outlier, vertical).

**Conditional distributions:** Break the data into subgroups and look at each separately. What's the return distribution during bull vs bear markets? Conditional distributions often reveal patterns that aggregated distributions hide.

---

## Missing Data

Missing data has three flavors, and the appropriate treatment depends on which one you're facing.

**MCAR (Missing Completely At Random):** The probability of missingness is independent of any observed or unobserved variable. If a sensor randomly fails 1% of the time regardless of conditions — MCAR. Simple deletion or imputation is valid.

**MAR (Missing At Random):** The probability of missingness depends on observed variables, but not on the missing value itself. Older investors might be less likely to report income — missingness depends on age (observed), not income itself (unobserved). Imputation conditioned on the observed variable (age) is valid.

**MNAR (Missing Not At Random):** The probability of missingness depends on the missing value itself. High earners are less likely to report income specifically because it's high. This is the hardest case — no imputation method fully solves it. You need domain knowledge or sensitivity analysis.

**Imputation strategies:**
- **Deletion:** Remove rows with missing values. Valid only if MCAR and missingness rate is low.
- **Mean/median imputation:** Replace missing values with the column mean or median. Simple. Shrinks variance and destroys correlations between variables.
- **Multiple imputation:** Create multiple complete datasets with different plausible values for missing data, analyze each, and combine results. Gold standard when missingness matters.

---

## Feature Engineering

Raw variables are rarely the best input to a model. Feature engineering creates derived variables that capture the signal more directly.

**Derived features:**
- Interaction terms: BMI × age (does BMI's effect on BP increase with age?)
- Polynomial features: age² (non-linear age effect)
- Ratios: debt-to-equity instead of debt and equity separately
- Log transformations: income data is often log-Normal; log(income) is more symmetric

**Categorical encoding:**
- Dummy variables (one-hot encoding): convert a 5-category variable into 4 binary variables (the fifth is the reference category)
- Ordinal encoding: when categories have a natural order (education level), encode as 1, 2, 3...

**Scaling:**
- Standardization (z-score): subtract mean, divide by std dev. Every variable has mean 0 and std dev 1.
- Necessary for many models (PCA, logistic regression with regularization, neural networks) where variables on different scales would create spurious differences.

---

## Logistic Regression

When the outcome is binary (profit/loss, default/no-default, churn/retain), linear regression is inappropriate — it can predict probabilities outside [0, 1] and doesn't respect the binary structure.

**Logistic regression** models the log-odds of the outcome as a linear function of predictors:

log(p / (1-p)) = β₀ + β₁X₁ + β₂X₂ + ...

Where p = P(outcome = 1). The left side is the log-odds (logit). The right side is the linear predictor.

**Interpreting coefficients as odds ratios:** Exponentiate each coefficient to get an odds ratio. If β₁ = 0.3, then e^0.3 ≈ 1.35 — each one-unit increase in X₁ multiplies the odds of the outcome by 1.35 (a 35% increase in odds).

**AUC-ROC:** Measures how well the model separates the two classes. AUC = 0.5 is random guessing. AUC = 1.0 is perfect. AUC = 0.80 means a randomly chosen positive case has 80% probability of a higher predicted probability than a randomly chosen negative case.

---

## Model Comparison

**The fundamental problem:** Adding any variable to a model increases R² (or decreases loss), even if the variable is pure noise. You need a principled way to decide whether adding complexity genuinely helps.

**AIC = -2 log(likelihood) + 2k.** Lower is better. The first term rewards fit; the second penalizes complexity (2 per parameter). AIC answers: "Given that we want to make good predictions on new data, which model strikes the best balance between fit and parsimony?"

**BIC = -2 log(likelihood) + k·log(n).** Like AIC but the penalty grows with n. Favors simpler models in large datasets. BIC tends to select the "true" model asymptotically; AIC tends to select predictively optimal models.

**Cross-validation:** Split data into k folds. Train on k-1 folds, evaluate on the held-out fold. Rotate through all folds. Average the held-out performance. This is the honest estimate of how the model performs on data it hasn't seen.

**The test set:** The final, untouched dataset used to evaluate your chosen model only once. If you use the test set to tune hyperparameters or select among models, it's no longer an honest evaluation — you've overfit to it. In quantitative finance, this is the walk-forward test.

---

## Communicating Results

The hardest part. A perfect analysis that no one understands changes nothing.

**Two audiences, two documents:**

The **executive summary** is one page, jargon-free, structured around decisions. What's the answer to the question? What's the magnitude? What should be done differently? What are the risks?

The **technical appendix** contains everything: code, methodology, diagnostic plots, sensitivity analyses. It's for the person who needs to replicate or audit the work.

**Report effect sizes, not just p-values.** "The intervention is statistically significant (p=0.003)" is less informative than "The intervention increased conversion by 3.2 percentage points (95% CI: 1.1, 5.3 pp), equivalent to $2.1M annual revenue impact."

**Show confidence intervals, not just point estimates.** A point estimate without uncertainty is a false precision. The CI communicates the range of plausible values — which is what decision-makers need.

**Limitations are scientific honesty, not weakness.** Every analysis has assumptions. Being explicit about them (cross-sectional vs longitudinal, self-reported vs measured, imputed vs observed) demonstrates rigor and helps readers calibrate how much to trust the conclusions.

---

## End-to-End Finance Example: Predicting Tech Stock Outperformance

**Question:** What factors predict whether a tech stock will outperform the S&P 500 next quarter?

**Data:** 5 years of quarterly data for 500 tech stocks. Predictors: market cap, P/E ratio, revenue growth rate, R&D spending ratio, analyst consensus rating, momentum (prior quarter return).

**EDA:** Return distribution is approximately symmetric but fat-tailed. P/E ratios are right-skewed — log-transform. Some stocks have missing R&D data (larger companies report; smaller ones sometimes don't). Analysts' ratings cluster at 3-4 out of 5 — low variance predictor.

**Missing data:** R&D missingness correlates with market cap (smaller firms less likely to report). MAR condition. Impute with median within market-cap decile.

**Feature engineering:** Log(P/E), momentum quartile (rank instead of raw value), interaction between P/E and growth rate (value × growth).

**Model:** Logistic regression with binary outcome (outperform = 1, underperform = 0). Train on first 4 years, test on final year.

**Evaluation:** AUC = 0.62. Modest but above random. Odds ratios: higher revenue growth (OR=1.4), high momentum (OR=1.3), and lower P/E (OR=0.85) are the strongest predictors.

**Multiple comparison correction:** With 6 predictors, apply Holm-Bonferroni to control FWER. Three predictors remain significant.

**Communication:** "Revenue growth and prior momentum are the most reliable predictors of near-term outperformance. A screening strategy based on these two factors achieved AUC=0.62 on held-out data, compared to 0.50 for random selection. Key limitation: results are based on 2018-2023 data; the model's performance during the 2022 rate-shock environment was lower than the 5-year average, suggesting it may underperform in high-volatility regimes."

---

## How This Connects to the Homework

- **Part 8A:** EDA — distributions, missing data, correlation matrix, conditional probabilities by risk factor
- **Part 8B:** Bootstrap CIs by subgroup — exactly the "Sharpe ratio bootstrap" idea applied to prevalence
- **Part 8B:** MLE vs MOM for logistic regression
- **Part 8C:** Full hypothesis testing battery — five hypotheses, multiple comparison correction, effect sizes
- **Part 8D:** Logistic regression (odds ratios, AUC), Bayesian logistic regression, CTMC for disease progression
- **Part 8E:** Executive summary, technical appendix, limitations, reflection essay

---

# Appendix: Key Formulas — Unpacked

Every formula below is accompanied by a plain-English reading.

**Bayes' Theorem:** P(A|B) = P(B|A) × P(A) / P(B)
*The probability of A given B equals how probable B is when A is true, times how probable A was before, divided by how probable B is overall.*

**Expected Value (discrete):** E[X] = Σ xᵢ · P(X = xᵢ)
*Sum up each possible value, weighted by its probability.*

**Variance:** Var(X) = E[(X - μ)²]
*The average squared distance from the mean.*

**Beta-Binomial Update:** Beta(a, b) + k successes in n → Beta(a+k, b+n-k)
*Add observed successes to the first parameter, observed failures to the second.*

**Normal-Normal Posterior Mean:** μ_n = τ_n² × (μ₀/τ₀² + n·x̄/σ²)
*Weighted average of prior mean and data mean; weights are precisions (inverse variances).*

**OLS Slope:** β̂₁ = Cov(X, Y) / Var(X)
*How much Y co-varies with X, relative to how much X varies by itself.*

**R²:** 1 - Var(residuals) / Var(Y)
*Fraction of Y's variance explained by the model.*

**Cohen's d:** (μ₁ - μ₂) / σ_pooled
*The mean difference, measured in standard deviation units.*

**Bayes Factor:** BF = P(data | H₁) / P(data | H₀)
*How many times more probable is the data under H₁ than H₀?*

**CTMC transition:** P(t) = e^{Qt}
*The probability of being in each state at time t equals the matrix exponential of the rate matrix times t.*

**Bootstrap CI:** [percentile_{α/2}(θ̂*), percentile_{1-α/2}(θ̂*)]
*The α/2 and 1-α/2 percentiles of the bootstrapped statistic distribution.*

---

*This guide covers every concept in DSCI 503. Return to it whenever a homework question uses terminology that isn't fully clear — the relevant section is indexed to the specific question numbers throughout.*
