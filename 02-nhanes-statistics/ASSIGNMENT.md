# DSCI 503 — Comprehensive Homework Exercise
**Total: 500 pts | Due: 2026-04-20 (past due — building for understanding)**

## Structure
| Part | Topic | Pts | Questions |
|------|-------|-----|-----------|
| 1 | Probability Foundations & Random Variables | 40 | Q1–Q8 |
| 2 | Simulation in Statistics | 35 | Q9–Q14 |
| 3 | Estimation | 35 | Q15–Q20 |
| 4 | Hypothesis Testing | 50 | Q21–Q28 |
| 5 | Advanced Linear Regression | 50 | Q29–Q35 |
| 6 | Stochastic Processes | 60 | Q36–Q44 |
| 7 | Bayesian Statistical Inference | 50 | Q45–Q51 |
| 8 | Capstone | 80 | Sections A–E |

---

## Part 1: Probability Foundations & Random Variables (40 pts)

### Exercise 1.1: Exploratory Probability Analysis (20 pts)

**Q1 (5 pts):** Load NHANES. Select: Age, Gender, BMI, BPSysAve, Diabetes, PhysActive, SmokeNow, TotChol.
Compute marginal probability of each categorical variable (P(Diabetes=Yes), P(PhysActive=Yes), P(SmokeNow=Yes)).
Present in a clean summary table.

**Q2 (5 pts):** Compute conditional probabilities and interpret each:
- P(Diabetes=Yes | BMI > 30)
- P(Diabetes=Yes | BMI ≤ 30)
- P(BPSysAve > 140 | Age > 60)
- P(PhysActive=Yes | Gender=female) vs P(PhysActive=Yes | Gender=male)

Are Diabetes and BMI > 30 independent? Test mathematically by comparing P(Diabetes | BMI > 30) with P(Diabetes).

**Q3 (5 pts):** Apply Bayes' Theorem manually.
Given a person has diabetes, what is P(they are obese, BMI > 30)?
Show full Bayes' Theorem calculation step by step, then verify with direct computation.

**Q4 (5 pts):** Visualization dashboard — at least 4 subplots:
- Distribution of BMI (histogram + KDE)
- Joint distribution of Age and BPSysAve (scatter + regression line)
- Conditional distribution of TotChol by Diabetes status (overlapping histograms or violin plots)
- Probability heatmap: P(Diabetes | Age group, BMI group) — bin both into quartiles

### Exercise 1.2: Random Variables Deep Dive (20 pts)

**Q5 (5 pts):** Treat BMI as continuous RV. Fit normal distribution via MLE (scipy.stats). Plot fitted
over empirical histogram. Report mean, variance, skewness, kurtosis. Shapiro-Wilk test + Q-Q plot.
Does normal fit well?

**Q6 (5 pts):** Treat DaysPhysHlthBad (count variable) as discrete RV. Fit Poisson distribution. Plot
observed frequency vs fitted PMF. Chi-squared goodness-of-fit test. If Poisson doesn't fit, try
negative binomial and compare.

**Q7 (5 pts):** Compute E[X] and Var[X] of BMI analytically from data. Compare with theoretical
values from fitted normal. Do same for count variable with Poisson/NB. Report discrepancies and
what they tell you about model fit.

**Q8 (5 pts):** 2D KDE of (BMI, BPSysAve). Contour plot of joint density. Extract and plot marginal
distributions on each axis. Compute correlation coefficient and covariance. Are these variables
independent? Explain using both correlation and shape of joint distribution.

---

## Part 2: Simulation in Statistics (35 pts)

### Exercise 2.1: Simulation Fundamentals (15 pts)

**Q9 (5 pts):** Implement linear congruential generator (LCG) from scratch. Generate 10,000
pseudo-random numbers. Plot sequence, compute mean and variance. Compare with numpy.random.
Visualize with lag-1 scatter plot (x_n vs x_{n+1}). Discuss quality.

**Q10 (5 pts):** Inverse CDF method — generate samples from Exponential distribution with
λ = 1/mean(BMI). Generate 10,000 samples. Compare with theoretical exponential using Q-Q plot
and KS test.

**Q11 (5 pts):** Box-Muller transform — generate normal RVs from uniform RVs. 10,000 samples
with μ=mean(BMI), σ=std(BMI). Verify normality with Shapiro-Wilk. Compare with numpy.random.normal.

### Exercise 2.2: Monte Carlo Applications (20 pts)

**Q12 (7 pts):** Monte Carlo — estimate P(BPSysAve > 140 AND Diabetes=Yes).
- Fit marginal distributions to BPSysAve and Diabetes status
- Estimate dependency (copula or empirical joint)
- Generate 100,000 simulated individuals
- Estimate joint probability + 95% CI
- Compare with empirical proportion from data

**Q13 (6 pts):** Bootstrap mean BMI. 1,000 bootstrap samples (n=original size). Plot bootstrap
distribution. 95% CI: percentile method AND BCa method. Compare with CLT analytical CI.

**Q14 (7 pts):** Power analysis via simulation. Test mean BMI: diabetic vs non-diabetic.
- n = 10, 20, 50, 100, 200, 500 — simulate 5,000 two-sample t-tests at α=0.05
- Plot power curve (power vs sample size)
- At what n do you achieve 80% power? 90%?
- Repeat for Cohen's d = 0.2 (small), 0.5 (medium), observed effect size. Compare 3 curves.

---

## Part 3: Estimation (35 pts)

### Exercise 3.1: Point Estimation (15 pts)

**Q15 (5 pts):** For BMI — compute and explain when each is preferred:
- Sample mean, median, 10% trimmed mean
- Sample variance (biased AND unbiased), sample SD
- For each: compute SE via formula AND bootstrap (1,000 resamples)
Which central tendency estimator is most robust? Why?

**Q16 (5 pts):** MLE from scratch for BMI ~ Normal. Write log-likelihood function. Use
scipy.optimize.minimize to find MLE of μ and σ². Compare with analytical MLE formulas.
Show numerical solution matches closed-form within numerical tolerance.

**Q17 (5 pts):** Method of Moments — fit Gamma distribution to BMI. Derive moment equations
(equate sample mean/variance to E[X]/Var[X] of Gamma). Solve for shape and rate parameters.
Plot fitted Gamma over histogram. Compare with MLE fit of Gamma.

### Exercise 3.2: Interval Estimation (20 pts)

**Q18 (7 pts):** 90%, 95%, 99% CIs for mean BMI using:
- z-interval (known σ)
- t-interval (sample SD)
- Bootstrap percentile (1,000 resamples)
Present all 9 intervals in one table. Plot visually. Discuss: what happens to width as confidence
increases? How do the 3 methods compare?

**Q19 (6 pts):** 95% CI for proportion with diabetes using:
- Wald interval
- Wilson score interval
- Clopper-Pearson exact interval
Which is most appropriate and why? Discuss Wald interval problems for small/extreme proportions.

**Q20 (7 pts):** Coverage probability experiment. Simulate 10,000 datasets of n=30 from
Normal(mean(BMI), std(BMI)). For each: compute 95% CI. Fraction containing true mean = coverage.
Repeat for n=5, 10, 50, 100. Plot coverage vs sample size. Does t-interval achieve 95%?
Repeat for skewed distribution (e.g., exponential). How does coverage change?

---

## Part 4: Hypothesis Testing (50 pts)

### Exercise 4.1: t-Tests (25 pts)

**Q21 (5 pts):** One-sample t-test. Test: mean BMI ≠ 26.5 (CDC national average). State H0/H1.
Compute test statistic by hand, then verify with scipy. Report p-value, 95% CI, Cohen's d.
Interpret practical vs statistical significance.

**Q22 (8 pts):** Independent two-sample t-test. BPSysAve: males vs females.
- Check: normality (Shapiro-Wilk each group), equal variances (Levene's test)
- Run appropriate test (equal or unequal variance based on findings)
- Cohen's d + 95% CI for difference in means
- Visualization: side-by-side boxplots with jittered points, annotated with p-value and effect size

**Q23 (5 pts):** Paired t-test. BPSys1 vs BPSys2 (first vs second reading — white coat effect).
Compute mean difference, SD of differences, test statistic. Is there a clinically meaningful difference?

**Q24 (7 pts):** Multiple comparisons. BMI across Race categories.
- Run all pairwise t-tests. Count significant at α=0.05.
- Apply: Bonferroni, Holm-Bonferroni, Benjamini-Hochberg (FDR)
- How many remain significant under each? Explain family-wise error rate.
- Run one-way ANOVA + Tukey's HSD as proper omnibus approach.

### Exercise 4.2: Non-Parametric Tests (25 pts)

**Q25 (8 pts):** Mann-Whitney U test. Gender comparison of BPSysAve. Compare with Q22 t-test.
When prefer Mann-Whitney over t-test? Compute rank-biserial correlation (non-parametric effect size).

**Q26 (7 pts):** Wilcoxon signed-rank test. Repeat Q23 (paired BP) non-parametrically.
Compare both tests: test statistics, p-values, conclusions in a table.

**Q27 (5 pts):** Kruskal-Wallis test. TotChol across Education levels. If significant: Dunn's post-hoc
with Bonferroni correction. Visualize with grouped boxplot.

**Q28 (5 pts):** Essay (300–500 words). Parametric vs non-parametric — when to use each.
Reference specific results from Q21–Q27.

---

## Part 5: Advanced Linear Regression (50 pts)

**Q29 (8 pts):** Multiple regression: BPSysAve ~ Age + BMI + Gender + PhysActive + SmokeNow +
TotChol + Diabetes. Full model summary (coefs, SE, t-stats, p-values, R², adj-R²). Interpret BMI
coefficient: "Controlling for all other variables, a one-unit increase in BMI is associated with..."

**Q30 (7 pts):** Regression diagnostics for Q29:
- Residual vs fitted (linearity + homoscedasticity)
- Q-Q of residuals (normality)
- Scale-Location (homoscedasticity)
- Cook's distance (influential observations)
Identify top 5 most influential observations. What makes them unusual?

**Q31 (7 pts):** VIF for each predictor. Any VIF > 5? > 10? If multicollinearity:
- Add correlated predictor (e.g., BPDiaAve), show VIFs change
- Use Ridge regression or drop variables. Compare OLS vs Ridge coefficients.

**Q32 (7 pts):** Heteroscedasticity. Breusch-Pagan + White's test on residuals. If detected:
- HC standard errors (White's robust SE)
- WLS with weights = 1/fitted(residuals²)
Compare original vs corrected SEs. Which coefficients change significance?

**Q33 (7 pts):** Model selection:
- Backward elimination (AIC)
- Forward selection (BIC)
- LASSO (L1) with cross-validation for lambda
Which variables survive all three? Cross-validated RMSE for each.

**Q34 (7 pts):** Prediction. Using best model from Q33:
- Predict BPSysAve: 55yo male, non-smoker, physically active, BMI=28, no diabetes, TotChol=200
- Provide prediction interval AND confidence interval — explain the difference
- Partial dependence plot for each predictor

**Q35 (7 pts):** Interaction effects. Add BMI × Diabetes to model. Significant? Interpret in plain language.
Visualize regression lines for diabetic vs non-diabetic across BMI values.

---

## Part 6: Stochastic Processes (60 pts)

### Exercise 6.1: Markov Chains & Random Walks (25 pts)

**Q36 (8 pts):** Health state Markov chain. States: Healthy (BMI<25), Overweight (25≤BMI<30), Obese (BMI≥30).
- Estimate 3×3 transition matrix (use age as proxy for time — younger vs older snapshots)
- Verify valid stochastic matrix (rows sum to 1, all non-negative)
- Stationary distribution: (a) solve πP=π analytically, (b) compute P^1000
- Simulate 10,000 steps from "Healthy." Does empirical distribution converge to stationary?

**Q37 (7 pts):** Random walk on systolic BP over 250 steps. Use empirical BP change distribution
as step distribution. Run 100 simulations. Plot all trajectories. Compute E[S_n] and Var(S_n) at
each step. Match theoretical E[S_n]=nμ and Var(S_n)=nσ²?

**Q38 (5 pts):** Classify the Markov chain: irreducible? Aperiodic? Recurrent? Prove/disprove
using transition matrix. Implications for long-run health outcomes?

**Q39 (5 pts):** Absorption probabilities. Make "Obese" absorbing. Starting from "Healthy,"
probability of eventual absorption into "Obese"? Solve with fundamental matrix.

### Exercise 6.2: Continuous-Time Processes & Poisson (35 pts)

**Q40 (8 pts):** Convert discrete transition matrix to continuous-time Markov chain (rate matrix Q).
- P(t) = e^{Qt} using matrix exponential
- Compute state probabilities at t=1, 5, 10, 20
- Plot P(t) over continuous time
- Verify CTMC stationary distribution = DTMC stationary distribution

**Q41 (7 pts):** Poisson process for health events. Estimate λ from NHANES (e.g., doctor visits proxy).
Simulate 100 time units. Plot: counting process N(t), inter-arrival times (exponential?),
event counts in fixed windows (Poisson?).

**Q42 (7 pts):** Non-homogeneous Poisson process. Rate λ(t) depends on age — fit polynomial or
exponential model. Simulate using thinning method. Compare with homogeneous model from Q41.

**Q43 (6 pts):** Bernoulli process. Each individual = Bernoulli trial (success=diabetes). Estimate p.
Simulate 10,000 processes of n=100. Distribution of successes = Binomial(100,p)? Waiting time
until first success = Geometric?

**Q44 (7 pts):** Superposition and thinning. Two Poisson processes: diabetes (λ1) and hypertension (λ2).
Demonstrate: superposition is Poisson(λ1+λ2). Demonstrate thinning: split and verify sub-processes are Poisson.

---

## Part 7: Bayesian Statistical Inference (50 pts)

### Exercise 7.1: Bayesian Foundations (20 pts)

**Q45 (7 pts):** Bayesian estimation of diabetes prevalence. Model as Binomial(n, θ).
Three Beta priors: (a) Beta(1,1) uninformative, (b) Beta(2,18) ~10% belief, (c) Beta(50,450) strong prior.
Compute posterior (Beta-Binomial conjugacy). Plot all 3 priors + likelihood + 3 posteriors.
Posterior mean, mode, 95% credible interval for each. How sensitive to prior choice?
At what n does prior become irrelevant?

**Q46 (6 pts):** Bayesian mean BMI. BMI~Normal(μ,σ²), σ² known. Prior: Normal(25, 5²).
Compute posterior analytically (Normal-Normal conjugacy). Plot prior, likelihood, posterior.
Posterior mean, variance, 95% credible interval. Compare with frequentist CI.

**Q47 (7 pts):** Bayesian hypothesis testing. P(μ > 25 | data) from Q46 posterior.
Compute Bayes Factor for H1: μ>25 vs H0: μ≤25. Interpret on Jeffreys' scale.
Compare with frequentist p-value.

### Exercise 7.2: Applied Bayesian Analysis (30 pts)

**Q48 (10 pts):** Bayesian linear regression. Re-estimate BPSysAve model using PyMC.
Weakly informative priors on all coefficients. 4,000 iterations + 1,000 warmup.
Report: posterior summaries (mean, SD, 95% CI), trace plots, R-hat diagnostics,
posterior predictive checks. Compare with OLS from Part 5.

**Q49 (8 pts):** Bayesian A/B test. PhysActive=Yes vs No groups, compare mean BP.
Normal priors on each group mean. Posterior of difference in means.
P(μ_active < μ_inactive | data)? P(active reduces BP by > 5 mmHg)?

**Q50 (6 pts):** Hierarchical model. Mean BMI within each Race category with shared hyperprior.
Compare hierarchical estimates with raw group means. Which groups show most shrinkage? Why?

**Q51 (6 pts):** Essay (400–600 words). Bayesian vs frequentist based on your own results in Parts 4–7.
When did they agree? Disagree? When was each more useful?

---

## Part 8: Capstone (80 pts)
Research Question: *"What are the most significant predictors of diabetes in the U.S. adult population,
and how do these risk factors interact to influence diabetes prevalence across demographic groups?"*

### Section A: Data Preparation & Exploration (15 pts)
- Clean dataset: handle missing values (document strategy), encode variables, create derived features
  (BMI categories, age groups, metabolic syndrome indicator)
- Comprehensive EDA: summary stats, distributions, correlation matrix heatmap, key bivariate relationships
- Identify 3 most surprising findings
- Compute conditional probabilities of diabetes given various risk factors — rank by predictive strength

### Section B: Simulation & Estimation (15 pts)
- Bootstrap CIs for diabetes prevalence within each demographic subgroup (age × gender × race)
- Identify subgroups with widest CIs — explain why
- MLE for logistic regression diabetes risk — compare with MOM estimates

### Section C: Hypothesis Testing Battery (20 pts)
For each hypothesis: select appropriate test, check assumptions, compute effect size, interpret:
- H1: Mean BMI differs between diabetic and non-diabetic
- H2: Physical activity levels differ between diabetic and non-diabetic
- H3: Relationship between age and diabetes is non-linear
- H4: Interaction between gender and BMI in predicting diabetes
- H5: Diabetes prevalence differs across racial/ethnic groups after controlling for BMI and age
Apply multiple comparison corrections. Publication-quality summary table.

### Section D: Predictive Modeling (15 pts)
- Logistic regression with all relevant predictors — interpret odds ratios
- Bayesian logistic regression — compare posterior odds ratios with frequentist
- Stochastic process framework: if pre-diabetic, long-run probability of developing diabetes?

### Section E: Presentation & Communication (15 pts)
- Executive summary (1 page, non-technical audience)
- Technical appendix with all code, outputs, reasoning
- 3–5 publication-quality figures telling the analysis story
- Limitations, assumptions, future research

---

## Submission
- Jupyter Notebook (.ipynb) with all code, output, written answers
- Label clearly: (a) YOUR code, (b) Claude Code version, (c) your comparison/commentary
- Part 8 as separate polished PDF report
- 1–2 page "Reflection on AI-Assisted Learning" essay
