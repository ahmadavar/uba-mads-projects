# Reading Guide: Parts 4–8
## Your Personal Reference for Learning Sessions

> **How to use this:** Keep this open during our sessions. When I ask you a pseudo-code question, look here first. 
> The guide is organized so you can jump to any concept and understand it from scratch.

---

# TABLE OF CONTENTS

- [Part 4: Hypothesis Testing](#part-4) — Q21–Q28
- [Part 5: Advanced Linear Regression](#part-5) — Q29–Q35
- [Part 6: Stochastic Processes](#part-6) — Q36–Q44
- [Part 7: Bayesian Statistical Inference](#part-7) — Q45–Q51
- [Part 8: Capstone](#part-8) — Sections A–E
- [Quick Reference Tables](#quick-reference)

---

<a name="part-4"></a>
# PART 4: The Art of Deciding
## Hypothesis Testing — Q21 to Q28

---

## The Foundation: What Is a Hypothesis Test?

Picture yourself on a jury. Before you walk in, the law says: **presume innocence**. That's your starting position — the null hypothesis. You didn't choose it because you believe it. You chose it because it's the conservative, do-nothing assumption.

The prosecution presents evidence. You ask yourself one question:

> *"If this person were truly innocent, how probable is it that all this evidence accumulated against them purely by chance?"*

If the answer is "very unlikely" — you reject innocence.

**That's the structure of every hypothesis test:**

| Courtroom | Statistics |
|-----------|-----------|
| Presumption of innocence | H₀ (null hypothesis) |
| Evidence from prosecution | Your data |
| "How likely is this evidence if innocent?" | p-value |
| Conviction threshold | α (significance level) |
| Acquit / Convict | Fail to reject H₀ / Reject H₀ |

**Critical things to tattoo in your brain:**

1. **You never prove H₀ is true.** Failing to convict someone doesn't prove they're innocent. It just means you didn't have enough evidence.

2. **You never prove H₁ is true.** Rejecting H₀ just means H₀ is implausible given the data.

3. **The p-value is NOT the probability H₀ is true.** It's the probability of seeing data this extreme IF H₀ were true.

4. **Statistical significance ≠ practical significance.** With 10 million observations, a difference of 0.001 can be highly significant. But who cares?

---

## Two Types of Errors

This is a 2×2 table you'll see in every hypothesis testing chapter:

```
                    Reality
                  H₀ True   H₁ True
Decision  Reject H₀  Type I Error  Correct (Power)
          Fail Reject  Correct     Type II Error
```

- **Type I Error (α):** False positive. The alarm went off but there's no fire. You said "significant" but there was nothing real.
- **Type II Error (β):** False negative. The building is on fire but the alarm didn't go off. You missed a real effect.
- **Power = 1 - β:** Probability of detecting a real effect when it exists. Want power ≥ 0.80.

**The tradeoff:** Lowering α (more conservative) increases Type II errors. You can't minimize both simultaneously.

---

## Q21: One-Sample t-Test

**Question:** Is the mean BMI in NHANES significantly different from the CDC national average of 26.5?

### The Story
You have 10,000 people. Your sample average is, say, 28.7. The CDC says the average American has BMI = 26.5. Is the difference (2.2 units) real, or just random sampling noise?

### The Machinery
The test statistic measures: **how many standard errors is your sample mean away from the claimed mean?**

```
t = (x̄ - μ₀) / (s / √n)

where:
  x̄  = your sample mean
  μ₀ = the claimed/null value (26.5)
  s  = your sample standard deviation
  n  = sample size
  s/√n = standard error of the mean
```

The denominator (s/√n) answers: "how much would my sample mean bounce around if I drew many samples?" Small denominator = you're very precise = small differences become significant.

### Why t-distribution, not normal?
Because you're estimating σ from data (using s). There's extra uncertainty from not knowing σ. The t-distribution has fatter tails than normal — it acknowledges this extra uncertainty. Degrees of freedom = n-1. As n grows, t → normal.

### What is Cohen's d?
```
d = (x̄ - μ₀) / s
```

This is pure effect size — independent of sample size. If d = 1.5, your sample mean is 1.5 standard deviations away from the null. This tells you whether the difference matters, not just whether it's detectable.

| Cohen's d | Magnitude |
|-----------|-----------|
| 0.2 | Small |
| 0.5 | Medium |
| 0.8 | Large |

### Pseudo-code skeleton
```python
# Step 1: State your hypotheses
# H0: mean BMI = 26.5
# H1: mean BMI ≠ 26.5 (two-tailed)

# Step 2: Compute test statistic by hand
x_bar = df['BMI'].mean()
s = df['BMI'].std(ddof=1)       # ddof=1 for sample std
n = df['BMI'].count()
mu_0 = 26.5

standard_error = s / np.sqrt(n)
t_stat = (x_bar - mu_0) / standard_error
df_t = n - 1

# Step 3: Get p-value
p_value = 2 * stats.t.sf(abs(t_stat), df=df_t)   # two-tailed

# Step 4: Verify with scipy
t_stat_check, p_value_check = stats.ttest_1samp(df['BMI'].dropna(), popmean=26.5)

# Step 5: Effect size
cohen_d = (x_bar - mu_0) / s

# Step 6: Confidence interval (95%)
t_critical = stats.t.ppf(0.975, df=df_t)
ci_lower = x_bar - t_critical * standard_error
ci_upper = x_bar + t_critical * standard_error

# Step 7: Print interpretation
print(f"Sample mean: {x_bar:.2f}, H₀ value: {mu_0}")
print(f"t-statistic: {t_stat:.3f}, df: {df_t}, p-value: {p_value:.4f}")
print(f"Cohen's d: {cohen_d:.3f}")
print(f"95% CI: ({ci_lower:.2f}, {ci_upper:.2f})")
```

### How to interpret
"The sample mean BMI (x̄ = 28.7) is significantly higher than the CDC national average of 26.5 (t(9999) = XX.X, p < 0.001). The effect size is large (d = 0.80), suggesting this difference is not only statistically significant but clinically meaningful. The 95% CI for the true mean BMI is (28.5, 28.9)."

---

## Q22: Independent Two-Sample t-Test

**Question:** Is mean blood pressure (BPSysAve) different between males and females?

### The Story
Two separate groups. You want to know if their population means differ. Before running the test, you check two assumptions: normality and equal variances. These assumptions determine which version of the test to run.

### Step 1: Check normality (Shapiro-Wilk)
```python
group_male = df[df['Gender'] == 'male']['BPSysAve'].dropna()
group_female = df[df['Gender'] == 'female']['BPSysAve'].dropna()

stat_m, p_m = stats.shapiro(group_male[:5000])   # Shapiro needs n<5000
stat_f, p_f = stats.shapiro(group_female[:5000])

# If p < 0.05 → evidence of non-normality
# With large n, Shapiro is hypersensitive — even tiny deviations from normal will be flagged
# Use your judgment: if histograms look roughly bell-shaped, proceed with t-test
```

### Step 2: Check equal variances (Levene's test)
```python
stat_levene, p_levene = stats.levene(group_male, group_female)

# If p > 0.05: variances are roughly equal → pooled t-test
# If p < 0.05: variances differ → Welch's t-test (default in scipy)
```

### Step 3: Run the t-test
```python
# Welch's t-test (safe default — doesn't assume equal variances)
t_stat, p_value = stats.ttest_ind(group_male, group_female, equal_var=False)

# Pooled t-test (only if Levene's shows equal variances)
t_stat, p_value = stats.ttest_ind(group_male, group_female, equal_var=True)
```

### The formula (Welch's)
```
t = (x̄₁ - x̄₂) / √(s₁²/n₁ + s₂²/n₂)

degrees of freedom: complicated formula (Welch-Satterthwaite equation)
— scipy computes this automatically
```

### Effect size (Cohen's d for two groups)
```python
# Pooled standard deviation
n1, n2 = len(group_male), len(group_female)
s_pooled = np.sqrt(((n1-1)*group_male.std()**2 + (n2-1)*group_female.std()**2) / (n1+n2-2))
cohen_d = (group_male.mean() - group_female.mean()) / s_pooled
```

### 95% CI for the difference in means
```python
mean_diff = group_male.mean() - group_female.mean()
se_diff = np.sqrt(group_male.var(ddof=1)/n1 + group_female.var(ddof=1)/n2)
df_welch = ...  # Welch-Satterthwaite — scipy gives you this
t_crit = stats.t.ppf(0.975, df=df_welch)
ci = (mean_diff - t_crit*se_diff, mean_diff + t_crit*se_diff)
```

### Visualization
```python
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Left: boxplots with jitter
axes[0].boxplot([group_male, group_female], labels=['Male', 'Female'])
# Add individual points (jitter)
x_male = np.random.normal(1, 0.05, size=min(200, len(group_male)))
axes[0].scatter(x_male, group_male.sample(min(200, len(group_male))), alpha=0.3)

# Add annotation with stats
axes[0].set_title(f'BPSysAve by Gender\np={p_value:.4f}, d={cohen_d:.2f}')

plt.tight_layout()
```

---

## Q23: Paired t-Test

**Question:** Is there a difference between BPSys1 and BPSys2 (first vs second BP reading)?

### The Story
Same people, two measurements. The "white coat effect" — anxiety from the doctor's office inflates the first reading. Does the second reading fall?

**Why paired matters:** If you treated this as two independent groups, you'd be comparing e.g. a tall 70-year-old's first reading with a short 30-year-old's second reading. All that between-person variation obscures the within-person change. The paired test strips it away.

**Method:** Compute the difference for each person, then run a one-sample t-test on those differences against H₀: mean difference = 0.

### Pseudo-code skeleton
```python
# Step 1: Compute differences
df_clean = df[['BPSys1', 'BPSys2']].dropna()
differences = df_clean['BPSys2'] - df_clean['BPSys1']

# Step 2: Manual calculation
d_bar = differences.mean()
s_d = differences.std(ddof=1)
n = len(differences)
t_stat = d_bar / (s_d / np.sqrt(n))
p_value = 2 * stats.t.sf(abs(t_stat), df=n-1)

# Step 3: Verify with scipy
t_scipy, p_scipy = stats.ttest_rel(df_clean['BPSys1'], df_clean['BPSys2'])

# Step 4: Is the difference clinically meaningful?
# Medical context: differences < 2 mmHg are usually not clinically significant
print(f"Mean difference: {d_bar:.2f} mmHg")
print(f"95% CI: {differences.mean() - 1.96*differences.sem():.2f} to {differences.mean() + 1.96*differences.sem():.2f}")
```

---

## Q24: Multiple Comparisons

**Question:** BMI across race categories — but if you run all pairwise t-tests, you'll have many false positives.

### The Core Problem (by analogy)
Imagine you're searching for a needle in a haystack. You check 100 different spots. Even if there's no needle, you might poke 5 spots by mistake and think you found something (5% × 100 = 5 false alarms at α=0.05). That's the multiple comparisons problem.

**Family-wise error rate (FWER):** With k tests, each at α=0.05, the probability of at least one false positive = 1 - (1-0.05)^k.

For k=10 pairwise tests: 1 - 0.95^10 ≈ 40%. Without correction, you have a 40% chance of at least one fake finding.

### Three Corrections

**Bonferroni:** Divide α by number of tests.
```python
alpha_bonferroni = 0.05 / n_comparisons
# A test is significant only if p < alpha_bonferroni
```
- Simplest, most conservative
- Best when you have few tests and want very strict control

**Holm-Bonferroni:** Smarter, less conservative than Bonferroni.
```python
from statsmodels.stats.multitest import multipletests

reject, p_adjusted, _, _ = multipletests(p_values, method='holm')
# reject[i] = True if the i-th test is significant after correction
```
- Sorts p-values, compares each to progressively less strict threshold
- Always better than Bonferroni, same guarantee

**Benjamini-Hochberg (BH/FDR):** Controls *false discovery rate*, not FWER.
```python
reject, p_adjusted, _, _ = multipletests(p_values, method='fdr_bh')
```
- Accepts that maybe 5% of your "significant" results are false
- Much more permissive — keeps more real findings
- Use when you have many tests (genomics, etc.) and some false positives are acceptable

### The Proper Approach: ANOVA + Tukey's HSD

Rather than doing all pairwise t-tests, the statistically clean approach is:

1. **One-way ANOVA:** Is there ANY difference in BMI across race groups? One test, one α.
2. If ANOVA is significant: **Tukey's HSD** — which groups differ? Tukey's is designed for all pairwise comparisons and controls FWER automatically.

```python
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Step 1: ANOVA
df_clean = df[['BMI', 'Race1']].dropna()
model = ols('BMI ~ C(Race1)', data=df_clean).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table)

# Step 2: Tukey's HSD (only if ANOVA p < 0.05)
tukey = pairwise_tukeyhsd(df_clean['BMI'], df_clean['Race1'], alpha=0.05)
print(tukey.summary())
tukey.plot_simultaneous()    # Plots CI for each pairwise difference
```

### Why Tukey's is better than multiple t-tests with correction:
Tukey's HSD is designed specifically for the all-pairwise-comparisons problem. It uses the studentized range distribution instead of t — this gives it proper FWER control with no additional conservatism.

---

## Q25: Mann-Whitney U Test

**Question:** Gender comparison of BPSysAve, using ranks instead of means.

### The Story
You've run the t-test in Q22. Now you run the non-parametric equivalent. Instead of comparing means, you compare rank distributions.

**Key idea:** Convert all values to ranks (1 = lowest). The Mann-Whitney U statistic is essentially: "If I randomly pick one man and one woman, how often does the man have higher BP?"

Under H₀ (identical distributions), this probability = 0.5. U measures deviation from that.

### When to use Mann-Whitney instead of t-test:
- Small sample sizes (n < 30) AND non-normal data
- Ordinal data (rankings, Likert scales)
- Severe outliers that would distort means
- (With large n, t-test and Mann-Whitney usually agree)

### Pseudo-code skeleton
```python
# Mann-Whitney U test
stat_u, p_value_mw = stats.mannwhitneyu(group_male, group_female, 
                                         alternative='two-sided')

# Effect size: rank-biserial correlation
# r = 1 - 2U / (n1 * n2)
n1, n2 = len(group_male), len(group_female)
r_rb = 1 - (2 * stat_u) / (n1 * n2)
# r_rb = 0: no effect, 1: complete separation

# Compare results in a table
comparison_table = {
    'Test': ['t-test', 'Mann-Whitney U'],
    'Statistic': [t_stat, stat_u],
    'p-value': [p_ttest, p_value_mw],
    'Effect size': [cohen_d, r_rb]
}
```

---

## Q26: Wilcoxon Signed-Rank Test

**Question:** Repeat the paired BP comparison (Q23) non-parametrically.

### How it works
1. Compute differences d_i = BPSys2_i - BPSys1_i
2. Ignore zeros (differences of exactly 0)
3. Rank the absolute differences |d_i|
4. Sum the ranks of positive differences → W+
5. Sum the ranks of negative differences → W-

Under H₀ (no systematic difference), W+ and W- should be roughly equal. The test statistic is min(W+, W-).

```python
stat_wilcox, p_value_wilcox = stats.wilcoxon(df_clean['BPSys1'], df_clean['BPSys2'])

# Compare with paired t-test
print(f"Paired t-test: t={t_stat:.3f}, p={p_ttest:.4f}")
print(f"Wilcoxon: W={stat_wilcox:.1f}, p={p_value_wilcox:.4f}")
```

---

## Q27: Kruskal-Wallis Test

**Question:** TotChol across education levels (3+ groups, non-parametric).

### The Story
Kruskal-Wallis is the rank-based version of one-way ANOVA. Instead of comparing group means, you compare the rank distributions.

Under H₀: all groups have the same distribution (and thus similar rank averages).

```python
# Get groups
edu_groups = [df[df['Education'] == edu]['TotChol'].dropna() 
              for edu in df['Education'].unique()]

# Kruskal-Wallis
stat_kw, p_value_kw = stats.kruskal(*edu_groups)

# If significant: Dunn's post-hoc
from scikit_posthocs import posthoc_dunn
dunn_results = posthoc_dunn(df[['TotChol', 'Education']].dropna(), 
                             val_col='TotChol', group_col='Education', 
                             p_adjust='bonferroni')
print(dunn_results)  # Matrix of p-values between each pair of education levels
```

---

## Q28: The Essay — Parametric vs Non-Parametric

### When parametric tests are appropriate:
- Data is approximately normally distributed (or n is large enough → CLT kicks in, n > 30 usually)
- Continuous data measured on interval or ratio scale
- You have large enough samples that distributional assumptions are verifiable
- You want maximum statistical power (parametric tests are more powerful when assumptions hold)

### When non-parametric tests are appropriate:
- Small samples AND non-normal distributions
- Ordinal data (e.g., survey responses 1-5)
- Heavy outliers or skewed distributions
- You can't verify normality
- When the p-values of both approaches differ substantially

### Common misconception:
"Non-parametric = no assumptions." False. Non-parametric tests still assume:
- Independence of observations
- Comparable shapes between groups (for some tests)
They just don't assume a specific distribution family.

### In your specific results (what to write about):
- Q22 vs Q25: Did the t-test and Mann-Whitney agree? (With n=10,000, they almost certainly did. This shows that with large n, choice of test matters less.)
- Q23 vs Q26: Same comparison for paired tests
- Were there cases where non-normal data would have made the t-test invalid? (check Shapiro-Wilk results from Q22)

---

<a name="part-5"></a>
# PART 5: The Recipe Book
## Advanced Linear Regression — Q29 to Q35

---

## The Foundation: What Is Multiple Regression?

You're trying to predict someone's blood pressure. You know things about them: age, BMI, gender, smoking status, whether they exercise. Multiple regression is the machine that combines all this information into one prediction.

```
BPSysAve = β₀ + β₁(Age) + β₂(BMI) + β₃(Gender) + β₄(PhysActive) + ... + ε
```

**Each β is a partial slope:** How much does BPSysAve change for one unit change in that predictor, **while holding all other predictors constant?**

This "holding constant" part is everything. Without it, BMI and age are confounded — older people tend to have higher BMI AND higher BP. Simple regression of BP on BMI would conflate the two effects. Multiple regression isolates them.

**The assumptions (remember LINER):**
- **L**inearity: the relationship is linear
- **I**ndependence: observations are independent
- **N**ormality: residuals (errors) are normally distributed
- **E**qual variance (homoscedasticity): residual variance is constant across fitted values
- **R**andom sampling

---

## Q29: Running the Full Model

### Pseudo-code skeleton
```python
import statsmodels.formula.api as smf

# Fit the model
formula = 'BPSysAve ~ Age + BMI + C(Gender) + C(PhysActive) + C(SmokeNow) + TotChol + C(Diabetes)'
model = smf.ols(formula, data=df).fit()

# Full summary
print(model.summary())
```

### Reading the model summary — column by column

```
                  coef    std err          t      P>|t|     [0.025     0.975]
Intercept       75.23      2.14       35.2     0.000      71.04      79.42
Age              0.42      0.01       42.0     0.000       0.40       0.44
BMI              0.31      0.03       10.3     0.000       0.25       0.37
C(Gender)[T.male]  4.21   0.31       13.6     0.000       3.60       4.82
```

| Column | Meaning |
|--------|---------|
| coef | The partial slope — effect per unit change, all else held constant |
| std err | Uncertainty in the coefficient |
| t | coef / std err — how many SEs from zero? |
| P>|t| | p-value: is this coefficient significantly different from zero? |
| [0.025, 0.975] | 95% confidence interval for the coefficient |

**R² and Adjusted R²:**
- R² = fraction of variance in BPSysAve explained by the model (0 to 1)
- Adj-R² = penalizes for adding more predictors. Always compare this when choosing between models.

### The key interpretation phrase:
"Controlling for Age, Gender, PhysActive, SmokeNow, TotChol, and Diabetes, a one-unit increase in BMI is associated with a 0.31 mmHg increase in systolic blood pressure (β = 0.31, 95% CI: [0.25, 0.37], p < 0.001)."

---

## Q30: Diagnostics — Is Your Model's Recipe Actually Valid?

### Four diagnostic plots

**Plot 1: Residuals vs Fitted**
```python
residuals = model.resid
fitted = model.fittedvalues

plt.scatter(fitted, residuals, alpha=0.3)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Fitted values')
plt.ylabel('Residuals')
plt.title('Residuals vs Fitted')
```
- **Good:** Random cloud around zero, no pattern
- **Bad (curved):** You missed a nonlinear relationship
- **Bad (cone shape):** Heteroscedasticity — variance increases with fitted values

**Plot 2: Q-Q Plot of Residuals**
```python
import statsmodels.api as sm
sm.qqplot(residuals, line='45')
plt.title('Q-Q Plot of Residuals')
```
- **Good:** Points follow the 45° diagonal
- **Bad (S-curve):** Skewed distribution
- **Bad (heavy tails):** More extreme residuals than normal

**Plot 3: Scale-Location**
```python
standardized_resid = np.sqrt(np.abs(model.get_influence().resid_studentized_internal))
plt.scatter(fitted, standardized_resid, alpha=0.3)
plt.axhline(y=standardized_resid.mean(), color='red')
plt.title('Scale-Location')
```
- **Good:** Flat horizontal line — equal variance everywhere
- **Bad:** Upward slope — variance increases with fitted values (heteroscedasticity)

**Plot 4: Cook's Distance**
```python
influence = model.get_influence()
cooks_d = influence.cooks_distance[0]

plt.stem(range(len(cooks_d)), cooks_d, markerfmt=',')
plt.axhline(y=4/len(cooks_d), color='red', linestyle='--', label='4/n threshold')
plt.title("Cook's Distance")
```

**Cook's Distance interpretation:**
- Measures: how much ALL coefficients would change if you removed observation i
- Threshold: 4/n (some use 1)
- Points above threshold: examine them. Are they data errors? Are they valid but unusual?

---

## Q31: VIF and Multicollinearity

### The problem (by analogy)
You're trying to credit two chefs for a meal. But they cooked together the whole time and you can't separate their contributions. That's multicollinearity. When two predictors are highly correlated, the model can't figure out how to assign credit to each.

**Symptom:** Large standard errors on coefficients → wide confidence intervals → predictors that should be significant appear not to be.

### Computing VIF
```python
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Build the feature matrix (no intercept column needed for VIF function)
X = pd.get_dummies(df[['Age', 'BMI', 'TotChol', 'Gender', 'PhysActive']], drop_first=True).dropna()
X = sm.add_constant(X)

vif_data = pd.DataFrame({
    'Feature': X.columns,
    'VIF': [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
})
print(vif_data.sort_values('VIF', ascending=False))
```

**VIF interpretation:**
- VIF = 1: perfectly uncorrelated with other predictors
- VIF = 5: moderate collinearity — investigate
- VIF > 10: severe — coefficients are unstable

### Fix: Ridge Regression
```python
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler

# Standardize features (required for Ridge — penalizes large coefficients, 
# so features need to be on the same scale)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_features)

ridge = Ridge(alpha=1.0)   # alpha = regularization strength (λ)
ridge.fit(X_scaled, y)

# Compare OLS vs Ridge coefficients
for name, ols_coef, ridge_coef in zip(feature_names, ols_coefficients, ridge.coef_):
    print(f"{name}: OLS={ols_coef:.3f}, Ridge={ridge_coef:.3f}")
```

Ridge shrinks all coefficients toward zero. It accepts slightly worse fit in exchange for much more stable, interpretable coefficients when predictors are correlated.

---

## Q32: Heteroscedasticity

### The problem
Your error variance changes across observations. Maybe young people's BP is easy to predict (residuals ±5 mmHg) but elderly people's BP is much harder to predict (residuals ±25 mmHg).

**Why this matters:** Your coefficients (β̂) are still unbiased. But your standard errors are wrong → your confidence intervals are wrong → your p-values are wrong. You might declare predictors significant that aren't, or miss real effects.

### Testing
```python
import statsmodels.stats.diagnostic as diagnostic

# Breusch-Pagan test
bp_stat, bp_p, _, _ = diagnostic.het_breuschpagan(model.resid, model.model.exog)
print(f"Breusch-Pagan: stat={bp_stat:.3f}, p={bp_p:.4f}")
# If p < 0.05: heteroscedasticity present

# White's test
white_stat, white_p, _, _ = diagnostic.het_white(model.resid, model.model.exog)
print(f"White's test: stat={white_stat:.3f}, p={white_p:.4f}")
```

### Fix 1: Robust Standard Errors (HC)
```python
# Refit with robust SEs — same coefficients, corrected uncertainty
model_robust = smf.ols(formula, data=df).fit(cov_type='HC3')
print(model_robust.summary())

# Compare standard errors
comparison = pd.DataFrame({
    'OLS SE': model.bse,
    'Robust SE': model_robust.bse,
    'OLS p': model.pvalues,
    'Robust p': model_robust.pvalues
})
print(comparison)
```

### Fix 2: Weighted Least Squares (WLS)
```python
# Estimate weights: lower weight to obs where residuals are large
# Fit an auxiliary model to get weights
aux_model = smf.ols('np.log(resid_sq) ~ fitted', 
                     data=pd.DataFrame({'resid_sq': model.resid**2, 
                                        'fitted': model.fittedvalues})).fit()
weights = 1.0 / np.exp(aux_model.fittedvalues)

# Refit with weights
model_wls = smf.wls(formula, data=df, weights=weights).fit()
```

---

## Q33: Model Selection

**The question:** You have many potential predictors. Which ones actually belong in the model?

### The Criteria You're Optimizing

**AIC (Akaike Information Criterion):**
```
AIC = 2k - 2ln(L)
```
where k = number of parameters, L = maximized likelihood.
- Lower is better
- Penalizes each extra parameter with +2
- Tends to keep more predictors (useful for prediction)

**BIC (Bayesian Information Criterion):**
```
BIC = k·ln(n) - 2ln(L)
```
- Penalty is k·ln(n) — harsher than AIC when n is large
- Tends to select simpler, more parsimonious models (useful for interpretation)

### Backward Elimination (AIC)
```python
# Start with full model, drop predictors that most improve AIC
import statsmodels.formula.api as smf

def backward_aic(y, X_cols, data):
    best_formula = f'{y} ~ {" + ".join(X_cols)}'
    best_model = smf.ols(best_formula, data=data).fit()
    best_aic = best_model.aic
    
    improved = True
    while improved:
        improved = False
        for col in X_cols:
            remaining = [c for c in X_cols if c != col]
            formula = f'{y} ~ {" + ".join(remaining)}'
            model = smf.ols(formula, data=data).fit()
            if model.aic < best_aic:
                best_aic = model.aic
                best_model = model
                X_cols = remaining
                improved = True
                break
    return best_model, X_cols
```

### LASSO (L1 regularization)
```python
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score

# LASSO requires scaled features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_features)

# LassoCV finds the best λ via cross-validation
lasso_cv = LassoCV(cv=5, random_state=42)
lasso_cv.fit(X_scaled, y)

# Which coefficients survived? (non-zero = selected)
selected = pd.Series(lasso_cv.coef_, index=feature_names)
print(selected[selected != 0])
print(f"Best λ: {lasso_cv.alpha_:.4f}")
```

### LASSO intuition
Normal regression minimizes: Σ(actual - predicted)²
LASSO minimizes: Σ(actual - predicted)² + λΣ|β|

The second term is a penalty for large coefficients. Unlike Ridge (which uses β²), the absolute value penalty in LASSO can drive coefficients exactly to zero — automatic variable selection.

Large λ → more coefficients zeroed out → simpler model
Small λ → fewer zeroed → closer to OLS

Cross-validation finds the λ that minimizes prediction error on held-out data.

### Cross-validated RMSE comparison
```python
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso

models = {
    'OLS (backward, AIC selected vars)': LinearRegression(),
    'Ridge': Ridge(alpha=ridge_cv.alpha_),
    'LASSO': Lasso(alpha=lasso_cv.alpha_)
}

for name, model in models.items():
    scores = cross_val_score(model, X_scaled, y, cv=5, 
                              scoring='neg_root_mean_squared_error')
    print(f"{name}: RMSE = {-scores.mean():.3f} (±{scores.std():.3f})")
```

---

## Q34: Prediction — CI vs PI (the most commonly confused pair)

### The setup
Using your best model from Q33, predict BPSysAve for: 55yo male, non-smoker, physically active, BMI=28, no diabetes, TotChol=200.

### Two different questions, two different intervals

**Question 1:** "What's the average BP for all people with these characteristics?"
→ **Confidence Interval for the mean**
→ Narrower — only captures uncertainty in the regression line itself

**Question 2:** "What will THIS specific person's BP be?"
→ **Prediction Interval for an individual**
→ Wider — captures uncertainty in the regression line PLUS individual variation around the line

**The formula intuition:**

```
CI width ≈ t × SE(fitted)        [uncertainty from coefficient estimates]
PI width ≈ t × √(SE(fitted)² + σ²)   [add individual scatter σ²]
```

Even with infinite data (SE(fitted) → 0), the PI never collapses to a point because individuals still vary.

**Analogy:** The average height of 40-year-old men is 5'10" — you know this very precisely (narrow CI). But any given 40-year-old man might be 5'5" or 6'3" (wide PI).

```python
# Create a new observation
new_person = pd.DataFrame({
    'Age': [55], 'BMI': [28], 'Gender': ['male'],
    'PhysActive': ['Yes'], 'SmokeNow': ['No'],
    'TotChol': [200], 'Diabetes': ['No']
})

# Get both intervals
predictions = model.get_prediction(new_person)
pred_summary = predictions.summary_frame(alpha=0.05)

print(pred_summary[['mean', 'mean_ci_lower', 'mean_ci_upper', 
                      'obs_ci_lower', 'obs_ci_upper']])
```

Output interpretation:
- `mean`: point prediction (expected BP)
- `mean_ci_lower/upper`: 95% CI — where the true population mean is
- `obs_ci_lower/upper`: 95% PI — where an individual's actual value will fall

### Partial Dependence Plots
```python
from sklearn.inspection import PartialDependenceDisplay

# Show how predicted BP changes as one variable changes, 
# averaged over all other variables
fig, ax = plt.subplots(figsize=(12, 4))
PartialDependenceDisplay.from_estimator(
    sklearn_model, X_features, 
    features=['Age', 'BMI', 'TotChol'],
    ax=ax
)
plt.suptitle('Partial Dependence: Effect of Each Predictor')
```

---

## Q35: Interaction Effects

### The story
"The effect of BMI on BP is stronger for diabetics than non-diabetics." That's an interaction. You can't just say "each BMI unit increases BP by X" — you have to say "it depends on diabetes status."

### Adding an interaction
```python
# Add BMI × Diabetes interaction
formula_interaction = 'BPSysAve ~ Age + BMI + C(Gender) + C(PhysActive) + C(SmokeNow) + TotChol + C(Diabetes) + BMI:C(Diabetes)'
model_interaction = smf.ols(formula_interaction, data=df).fit()
```

### Reading the interaction term
The coefficient on `BMI:C(Diabetes)[T.Yes]` tells you: "How much does the BMI slope CHANGE for diabetics compared to non-diabetics?"

- β_BMI = 0.3: for non-diabetics, each BMI unit → +0.3 mmHg BP
- β_BMI:Diabetes = 0.15: for diabetics, the slope is 0.3 + 0.15 = 0.45 mmHg per BMI unit

### Comparing models
```python
# Is the interaction significant?
print(model_interaction.summary())
# Look at p-value for BMI:C(Diabetes)[T.Yes]

# AIC comparison
print(f"Without interaction: AIC = {model.aic:.1f}")
print(f"With interaction:    AIC = {model_interaction.aic:.1f}")
# Lower AIC = better model
```

### Visualization
```python
bmi_range = np.linspace(df['BMI'].min(), df['BMI'].max(), 100)

fig, ax = plt.subplots(figsize=(10, 6))

for diabetes_val, color, label in [('No', 'blue', 'Non-diabetic'), 
                                     ('Yes', 'red', 'Diabetic')]:
    # Create grid of predictions
    pred_data = pd.DataFrame({
        'BMI': bmi_range,
        'Diabetes': diabetes_val,
        'Age': df['Age'].mean(),
        'Gender': 'male',
        'PhysActive': 'Yes',
        'SmokeNow': 'No',
        'TotChol': df['TotChol'].mean()
    })
    pred = model_interaction.predict(pred_data)
    ax.plot(bmi_range, pred, color=color, label=label)

ax.set_xlabel('BMI')
ax.set_ylabel('Predicted BPSysAve')
ax.legend()
ax.set_title('Interaction: Effect of BMI on BP by Diabetes Status\n(Parallel lines = no interaction, Diverging lines = interaction)')
```

If the lines are parallel: no interaction. If they diverge (or converge or cross): interaction exists.

---

<a name="part-6"></a>
# PART 6: The World That Changes Over Time
## Stochastic Processes — Q36 to Q44

---

## The Foundation: Three Big Ideas

**1. The Markov Property:** The future depends only on the present, not the past.
- Given where you are now, knowing where you were yesterday adds no information.
- Analogy: board games. Your next roll of the dice doesn't depend on your roll history — only your current position matters.

**2. Stochastic = Random:** A "stochastic process" is a sequence of random variables indexed by time.

**3. Two types of time:**
- **Discrete-time:** State changes at tick 1, tick 2, tick 3... (Markov chains, random walks)
- **Continuous-time:** State can change at any moment (CTMC, Poisson process)

---

## Q36: Discrete-Time Markov Chain — Health State Model

### Setup
Three states:
- State 0: Healthy (BMI < 25)
- State 1: Overweight (25 ≤ BMI < 30)
- State 2: Obese (BMI ≥ 30)

You want to model: "if someone is in state X today, what's the probability they're in state Y next period?"

### Building the transition matrix from data

**The challenge:** NHANES is cross-sectional (one snapshot). There's no "time 1 vs time 2" data. The workaround: use age as a proxy for time. Compare younger people's states to older people's states.

```python
# Assign BMI state
def bmi_state(bmi):
    if bmi < 25: return 'Healthy'
    elif bmi < 30: return 'Overweight'
    else: return 'Obese'

df['BMI_State'] = df['BMI'].apply(bmi_state)

# Proxy: younger people → "from" state, older people → "to" state
# Split by median age
median_age = df['Age'].median()
younger = df[df['Age'] <= median_age]['BMI_State']
older = df[df['Age'] > median_age]['BMI_State']

# Count transitions (this is an approximation — not actual individual trajectories)
# We're estimating P(state in older age | state in younger age)
states = ['Healthy', 'Overweight', 'Obese']
transition_counts = np.zeros((3, 3))

for i, from_state in enumerate(states):
    for j, to_state in enumerate(states):
        # Count people in younger group with from_state who appear in older group with to_state
        # Since we don't track individuals, we estimate proportionally
        from_frac = (younger == from_state).mean()
        to_frac = (older == to_state).mean()
        transition_counts[i, j] = from_frac * to_frac * len(df)

# Normalize rows to get probabilities
P = transition_counts / transition_counts.sum(axis=1, keepdims=True)
```

**Better approach (if NHANES has repeated measurements):** Track the same individual across waves and count actual state changes.

### Finding the stationary distribution

**Method 1: Algebra (solve πP = π, Σπᵢ = 1)**
```python
import numpy as np
from numpy import linalg

# πP = π  →  π(P - I) = 0
# Add constraint Σπ = 1

n_states = 3
A = (P - np.eye(n_states)).T   # System of equations: (P-I)ᵀπ = 0
A[-1] = 1                       # Replace last equation with Σπ = 1
b = np.zeros(n_states)
b[-1] = 1

pi = np.linalg.solve(A, b)
print(f"Stationary distribution: {dict(zip(states, pi))}")
```

**Method 2: Power iteration (compute P^1000)**
```python
P_power = np.linalg.matrix_power(P, 1000)
# All rows converge to stationary distribution
print(f"Stationary distribution from P^1000: {P_power[0]}")
```

### Simulating the chain
```python
def simulate_markov_chain(P, start_state, n_steps):
    states_sequence = [start_state]
    current = start_state
    for _ in range(n_steps):
        next_state = np.random.choice(len(P), p=P[current])
        states_sequence.append(next_state)
        current = next_state
    return states_sequence

# Run 10,000 steps starting from Healthy (state 0)
chain = simulate_markov_chain(P, start_state=0, n_steps=10000)

# Compute empirical distribution
empirical = [chain.count(i)/len(chain) for i in range(3)]
print(f"Stationary (theoretical): {pi}")
print(f"Empirical (from simulation): {empirical}")
# These should match
```

---

## Q37: Random Walk on Blood Pressure

### The story
Imagine your blood pressure follows a random walk over 250 "time steps." At each step, your BP changes by a random amount drawn from the empirical distribution of BP changes in the data.

**A random walk is just the sum of random steps:**
```
S_n = X₁ + X₂ + ... + Xₙ   (where Xᵢ are i.i.d. step sizes)
```

### Key theoretical properties
- E[S_n] = n × μ (drift: expected position grows linearly)
- Var(S_n) = n × σ² (spread: variance grows linearly with steps)
- SD(S_n) = √n × σ (standard deviation grows as √n)

If μ = 0 (equal chance up and down), the walk drifts nowhere but spreads out like √n.

### Pseudo-code
```python
# Use empirical BP changes as step distribution
# Since we have cross-sectional data, simulate changes from the distribution of BPSysAve itself
# Or use age-based changes: diff in BP between age groups
step_mean = 0       # Assume zero drift (symmetric random walk)
step_std = df['BPSysAve'].std() * 0.1   # Small steps

n_steps = 250
n_simulations = 100
start_bp = df['BPSysAve'].mean()

all_walks = np.zeros((n_simulations, n_steps + 1))
for sim in range(n_simulations):
    steps = np.random.normal(step_mean, step_std, n_steps)
    walk = np.concatenate([[start_bp], start_bp + np.cumsum(steps)])
    all_walks[sim] = walk

# Plot all trajectories
plt.figure(figsize=(12, 6))
for sim in range(n_simulations):
    plt.plot(all_walks[sim], alpha=0.1, color='blue')
plt.plot(np.mean(all_walks, axis=0), color='red', linewidth=2, label='Mean trajectory')

# Theoretical bounds (±2 SD)
t = np.arange(n_steps + 1)
plt.fill_between(t, 
                  start_bp - 2*step_std*np.sqrt(t), 
                  start_bp + 2*step_std*np.sqrt(t), 
                  alpha=0.2, color='gray', label='±2 SD (theoretical)')
plt.legend()
plt.title('100 Random Walk Simulations of Blood Pressure')

# Verify E[S_n] = n*mu and Var(S_n) = n*sigma^2
empirical_means = np.mean(all_walks, axis=0)
empirical_vars = np.var(all_walks, axis=0)
theoretical_means = start_bp + step_mean * t
theoretical_vars = step_std**2 * t

print("Mean comparison (first 5 time points):")
print(f"Empirical: {empirical_means[:5]}")
print(f"Theoretical: {theoretical_means[:5]}")
```

---

## Q38: Markov Chain Classification

**Irreducible:** From any state, can you reach any other state in a finite number of steps?

```python
def is_irreducible(P, tolerance=1e-10):
    n = len(P)
    P_power = np.linalg.matrix_power(P, n**2)  # Check P^(n²) — reachability
    return np.all(P_power > tolerance)

print(f"Is the chain irreducible? {is_irreducible(P)}")
```

**Aperiodic:** Does the chain have a fixed-length cycle?
- Period d = GCD of all return times to a state
- Period = 1 (aperiodic) → chain can return to any state at any step
- Most health chains are aperiodic because self-transitions (staying in same state) exist

```python
# If P has positive diagonal entries (self-loops), chain is automatically aperiodic
has_self_loops = np.all(np.diag(P) > 0)
print(f"Has self-loops (→ aperiodic): {has_self_loops}")
```

**Why this matters:** An irreducible, aperiodic chain has a UNIQUE stationary distribution that it converges to from ANY starting state. This is the ergodic theorem for Markov chains.

Implication: No matter what health state a population starts in, the long-run composition converges to π. If you want to change that long-run composition, you need to change P (the transition rates) — i.e., change the health behaviors.

---

## Q39: Absorbing States — The Point of No Return

### Setup
Modify the chain: make "Obese" an absorbing state (P[Obese, Obese] = 1; P[Obese, others] = 0). This represents: once obese, you stay obese (in this simplified model).

**Absorbing state:** A state you can never leave. A "trap."
**Transient state:** A state you'll eventually leave (if you have unlimited time).

### Computing absorption probabilities
```python
# Q: transition matrix among transient states (Healthy, Overweight)
# R: transitions from transient to absorbing states (Obese)

Q = P[:2, :2]                      # Transient × Transient
R = P[:2, 2:].reshape(-1, 1)       # Transient × Absorbing

# Fundamental matrix N = (I - Q)^(-1)
I = np.eye(len(Q))
N = np.linalg.inv(I - Q)           # N[i,j] = expected visits to state j before absorption, starting from i

# Absorption probabilities
B = N @ R   # B[i] = probability of absorption into Obese starting from state i

print(f"Absorption probability from Healthy: {B[0][0]:.4f}")
print(f"Absorption probability from Overweight: {B[1][0]:.4f}")

# Expected time to absorption
t_absorption = N @ np.ones((len(Q), 1))
print(f"Expected steps to become Obese, starting Healthy: {t_absorption[0][0]:.1f}")
```

**Interpretation:** Even with a small per-step probability of transitioning to Obese, given enough time, the cumulative probability approaches 1. The fundamental matrix quantifies exactly how long this takes.

---

## Q40: Continuous-Time Markov Chain (CTMC)

### The key difference from DTMC
In a DTMC, time moves in ticks. In a CTMC, the chain stays in state i for a random amount of time (exponentially distributed with rate qᵢ), then jumps.

**Why exponential?** Because it's the only continuous memoryless distribution. Given you've been in Healthy for 3 years, your waiting time until you change state doesn't depend on those 3 years. Only your current state matters.

### The rate matrix Q (generator matrix)
```
Q[i,j] = rate of jumping from i to j     (i ≠ j, must be ≥ 0)
Q[i,i] = -(sum of all exit rates)          (negative, rows sum to 0)
```

**Converting from discrete P to continuous Q:**
```python
# Approximate relationship: P ≈ I + Q*Δt for small Δt
# Or more precisely: P = exp(Q*Δt)
# To go backwards: Q ≈ (P - I) / Δt  for small Δt
# Or: Q = matrix_log(P) / Δt

from scipy.linalg import logm

delta_t = 1.0   # time unit corresponding to one step in DTMC
Q_rate = logm(P) / delta_t
print("Rate matrix Q:")
print(Q_rate)
# Verify: Q[i,j] ≥ 0 for i≠j, Q[i,i] ≤ 0, rows sum to 0
```

### Computing P(t) = exp(Qt)
```python
from scipy.linalg import expm

def ctmc_probs(Q, t, initial_state=0):
    """Probability distribution over states at time t, starting from initial_state"""
    P_t = expm(Q * t)
    return P_t[initial_state]

# Compute at multiple time points
for t in [1, 5, 10, 20]:
    probs = ctmc_probs(Q_rate, t, initial_state=0)  # Start from Healthy
    print(f"t={t}: {dict(zip(states, probs.round(3)))}")

# Plot state probabilities over continuous time
t_values = np.linspace(0, 30, 300)
probs_over_time = np.array([ctmc_probs(Q_rate, t) for t in t_values])

plt.figure(figsize=(10, 5))
for i, state in enumerate(states):
    plt.plot(t_values, probs_over_time[:, i], label=state)
plt.xlabel('Time')
plt.ylabel('Probability')
plt.title('State Probability Over Continuous Time (CTMC)')
plt.legend()
```

---

## Q41: Poisson Process — Random Events Over Time

### The three defining properties
A Poisson process N(t) with rate λ is defined by:
1. N(0) = 0 (starts at zero)
2. Independent increments: events in non-overlapping intervals don't affect each other
3. Stationary increments: N(t+s) - N(t) ~ Poisson(λs) — only depends on the length of interval, not location

### Two equivalent representations
**Counting process:** How many events by time t? → N(t) ~ Poisson(λt)
**Inter-arrival times:** How long between consecutive events? → T ~ Exponential(λ)

### Simulating a Poisson process
```python
# Method 1: Via inter-arrival times
def simulate_poisson_process(rate, max_time):
    """Simulate Poisson process up to max_time"""
    times = []
    current_time = 0
    while current_time < max_time:
        inter_arrival = np.random.exponential(1.0 / rate)
        current_time += inter_arrival
        if current_time < max_time:
            times.append(current_time)
    return np.array(times)

lambda_rate = 3.0  # 3 events per unit time
event_times = simulate_poisson_process(lambda_rate, max_time=100)

# Plot counting process N(t)
t_axis = np.linspace(0, 100, 1000)
N_t = np.array([np.sum(event_times <= t) for t in t_axis])

plt.figure(figsize=(12, 4))
plt.step(t_axis, N_t, where='post')
plt.xlabel('Time')
plt.ylabel('N(t) — cumulative events')
plt.title(f'Poisson Process Counting Function (λ={lambda_rate})')

# Verify: inter-arrival times are exponential
inter_arrivals = np.diff(np.concatenate([[0], event_times]))
stat, p = stats.kstest(inter_arrivals, 'expon', args=(0, 1/lambda_rate))
print(f"KS test vs Exponential: p={p:.4f}")

# Verify: counts in fixed windows are Poisson
window_size = 10
windows = [np.sum((event_times >= w) & (event_times < w+window_size)) 
           for w in range(0, 90, window_size)]
print(f"Expected count per window: {lambda_rate * window_size}")
print(f"Observed counts: {windows}")
```

---

## Q42: Non-Homogeneous Poisson Process (NHPP)

### The problem with constant λ
In reality, the rate of health events isn't constant. Doctor visits increase with age. Hospitalizations spike in old age. λ should be a function of time/age.

### Thinning algorithm (Lewis-Shedler algorithm)
**Idea:** Generate more events than you need (using the maximum rate), then randomly delete some.

```python
def simulate_nhpp(rate_func, max_rate, max_time):
    """
    Simulate a non-homogeneous Poisson process using thinning.
    
    rate_func: a function t → λ(t), the time-varying rate
    max_rate:  upper bound on rate_func over [0, max_time]
    max_time:  end of simulation
    """
    # Step 1: Generate events from homogeneous Poisson(max_rate)
    homogeneous_events = simulate_poisson_process(max_rate, max_time)
    
    # Step 2: Accept each event with probability rate_func(t) / max_rate
    accepted_events = []
    for t in homogeneous_events:
        acceptance_prob = rate_func(t) / max_rate
        if np.random.uniform() < acceptance_prob:
            accepted_events.append(t)
    
    return np.array(accepted_events)

# Example: rate increases with age (use age as proxy for time)
def age_varying_rate(age):
    """Health event rate increases with age"""
    return 0.5 + 0.1 * age   # Linear increase

lambda_max = age_varying_rate(80)  # Maximum rate at oldest age

# Simulate
nhpp_events = simulate_nhpp(age_varying_rate, lambda_max, max_time=80)

# Compare with homogeneous process
homogeneous_events = simulate_poisson_process(np.mean([age_varying_rate(t) for t in range(80)]), max_time=80)

print(f"NHPP total events: {len(nhpp_events)}")
print(f"Homogeneous total events: {len(homogeneous_events)}")
```

---

## Q43: Bernoulli Process

### The story
Each person in NHANES is a Bernoulli trial: either has diabetes (success=1) or doesn't (success=0).

**Bernoulli process:** A sequence of n independent Bernoulli(p) trials.

### Three connected distributions
```
Each trial:     X_i ~ Bernoulli(p)       ← 0 or 1
Sum of n trials: S_n ~ Binomial(n, p)    ← how many successes in n trials
Wait for 1st:   T ~ Geometric(p)         ← how many trials until first success
```

```python
# Estimate p from data
p_diabetes = (df['Diabetes'] == 'Yes').mean()
print(f"Estimated diabetes probability p = {p_diabetes:.4f}")

# Simulate 10,000 Bernoulli processes of n=100 each
n_per_process = 100
n_simulations = 10000

successes = np.random.binomial(n=n_per_process, p=p_diabetes, size=n_simulations)

# Is the distribution Binomial(100, p)?
x = np.arange(0, 30)
theoretical_pmf = stats.binom.pmf(x, n=n_per_process, p=p_diabetes)

plt.figure(figsize=(10, 4))
plt.hist(successes, bins=range(0, 30), density=True, alpha=0.5, label='Simulated')
plt.plot(x, theoretical_pmf, 'ro-', label='Binomial PMF')
plt.xlabel('Number of diabetics (out of 100)')
plt.legend()

# Waiting time until first success: Geometric distribution
# E[T] = 1/p — expected trials until first diabetic
expected_wait = 1 / p_diabetes
print(f"Expected trials until first diabetic: {expected_wait:.1f}")

# Simulate geometric waiting times
waiting_times = np.random.geometric(p=p_diabetes, size=10000)
stat, p_val = stats.kstest(waiting_times, 'geom', args=(p_diabetes,))
print(f"KS test vs Geometric: p={p_val:.4f}")
```

---

## Q44: Superposition and Thinning

### Superposition: merging two Poisson streams into one
**Theorem:** If N₁(t) ~ Poisson(λ₁) and N₂(t) ~ Poisson(λ₂) and they're independent, then N₁(t) + N₂(t) ~ Poisson(λ₁ + λ₂).

```python
# Two health events: diabetes (λ1) and hypertension (λ2)
lambda_diabetes = 0.05
lambda_hypertension = 0.08

# Generate two independent processes
T = 100  # Time horizon
events_diabetes = simulate_poisson_process(lambda_diabetes, T)
events_hypertension = simulate_poisson_process(lambda_hypertension, T)

# Superposition: merge and sort
events_combined = np.sort(np.concatenate([events_diabetes, events_hypertension]))

# Verify combined process is Poisson(lambda1 + lambda2)
lambda_combined = lambda_diabetes + lambda_hypertension
inter_arrivals_combined = np.diff(np.concatenate([[0], events_combined]))

stat, p_ks = stats.kstest(inter_arrivals_combined, 'expon', args=(0, 1/lambda_combined))
print(f"Superposition KS test vs Exp(λ₁+λ₂): p={p_ks:.4f}")
```

### Thinning: splitting one stream into two sub-streams
**Theorem:** Take Poisson(λ). Label each event Type A (prob p) or Type B (prob 1-p). Then Type A events form Poisson(pλ) and Type B events form Poisson((1-p)λ).

```python
# Take the combined stream, randomly label each event
p_label_A = lambda_diabetes / lambda_combined  # Should recover original rates
labels = np.random.binomial(1, p_label_A, size=len(events_combined))

thinned_A = events_combined[labels == 1]   # Should be Poisson(lambda_diabetes)
thinned_B = events_combined[labels == 0]   # Should be Poisson(lambda_hypertension)

# Verify
inter_A = np.diff(np.concatenate([[0], thinned_A]))
inter_B = np.diff(np.concatenate([[0], thinned_B]))

stat_A, p_A = stats.kstest(inter_A, 'expon', args=(0, 1/lambda_diabetes))
stat_B, p_B = stats.kstest(inter_B, 'expon', args=(0, 1/lambda_hypertension))

print(f"Thinned A: KS vs Exp(λ₁) p={p_A:.4f}")
print(f"Thinned B: KS vs Exp(λ₂) p={p_B:.4f}")
```

---

<a name="part-7"></a>
# PART 7: The Updating Brain
## Bayesian Statistical Inference — Q45 to Q51

---

## The Foundation: Bayes' Theorem for Parameters

Parts 1–6 were all "frequentist" — the true parameter θ is fixed, unknown. We use data to estimate it. Our uncertainty comes from random sampling.

**Bayesian view:** θ is also uncertain. We represent our uncertainty about θ as a probability distribution. Before seeing data, we have a **prior**. After seeing data, we update to get a **posterior**.

```
Posterior ∝ Likelihood × Prior

P(θ | data) ∝ P(data | θ) × P(θ)
```

The posterior is your updated belief. It's a full distribution over possible values of θ.

**Three key benefits of Bayesian thinking:**
1. You can make direct probability statements: "There's a 93% probability that θ > 0.12"
2. You can incorporate prior knowledge
3. Naturally handles small samples (prior regularizes the estimate)

---

## Q45: Bayesian Estimation of Diabetes Prevalence

### The setup
- Parameter: θ = true diabetes prevalence (between 0 and 1)
- Data: n people, k have diabetes
- Likelihood: Binomial(n, θ) → P(k | θ, n) = C(n,k) × θᵏ × (1-θ)^(n-k)

### Beta prior — why Beta?
The Beta distribution is perfect for modeling probabilities (it lives on [0,1]). Beta(α, β) has mean α/(α+β).

Intuition: think of α as "prior successes" and β as "prior failures."

- Beta(1,1): "I've seen 1 success and 1 failure" = flat/uniform = no information
- Beta(2,18): "I believe about 10% prevalence, but weakly" (2 out of 20 successes)
- Beta(50,450): "I'm confident about 10%" (50 out of 500 successes in prior data)

### The conjugacy magic
When prior is Beta(α, β) and likelihood is Binomial:
```
Prior:     Beta(α, β)
Observe:   k successes in n trials
Posterior: Beta(α + k, β + n - k)
```

You just add observed successes to α and observed failures to β. No complex integrals needed.

```python
# Data
n_total = df['Diabetes'].count()
k_yes = (df['Diabetes'] == 'Yes').sum()
k_no = n_total - k_yes
print(f"Total: {n_total}, Diabetic: {k_yes}, p̂={k_yes/n_total:.4f}")

# Three priors
priors = {
    'Uninformative: Beta(1,1)': (1, 1),
    'Weak: Beta(2,18)': (2, 18),
    'Strong: Beta(50,450)': (50, 450)
}

theta = np.linspace(0, 0.30, 1000)
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for ax, (name, (alpha_prior, beta_prior)) in zip(axes, priors.items()):
    # Posterior parameters
    alpha_post = alpha_prior + k_yes
    beta_post = beta_prior + k_no
    
    # Distributions
    prior_dist = stats.beta(alpha_prior, beta_prior)
    likelihood_unnorm = stats.binom.pmf(k_yes, n_total, theta)
    posterior_dist = stats.beta(alpha_post, beta_post)
    
    # Plot
    ax.plot(theta, prior_dist.pdf(theta), 'b-', label='Prior', linewidth=2)
    ax.plot(theta, likelihood_unnorm/max(likelihood_unnorm)*max(posterior_dist.pdf(theta)), 
            'g--', label='Likelihood (scaled)', linewidth=2)
    ax.plot(theta, posterior_dist.pdf(theta), 'r-', label='Posterior', linewidth=2)
    
    # Summary stats
    post_mean = alpha_post / (alpha_post + beta_post)
    post_mode = (alpha_post - 1) / (alpha_post + beta_post - 2)
    ci_lower, ci_upper = posterior_dist.ppf(0.025), posterior_dist.ppf(0.975)
    
    ax.axvline(post_mean, color='red', linestyle=':', alpha=0.7)
    ax.set_title(f'{name}\nMean={post_mean:.4f}, 95% CI: [{ci_lower:.3f}, {ci_upper:.3f}]')
    ax.legend()
    ax.set_xlabel('θ (diabetes prevalence)')

plt.tight_layout()
```

### When does the prior become irrelevant?
With n=10,000 data points and only α=50, β=450 as prior — the prior is swamped. The posterior is almost entirely determined by the data. This is why large datasets "wash out" priors.

**Check this numerically:** Compute posteriors for all three priors. With n=10,000, they should converge to the same place.

---

## Q46: Bayesian Mean BMI — Normal-Normal Conjugacy

### Setup
- Model: BMI ~ Normal(μ, σ²), assume σ² known (use sample variance)
- Prior: μ ~ Normal(μ₀, τ²) — centered at CDC expected BMI, some spread
- Prior: μ₀ = 25 (CDC average), τ = 5 (you're uncertain within ±10 units)

### Posterior (Normal-Normal conjugacy)
The posterior mean is a precision-weighted average of prior mean and sample mean:

```
posterior_mean = (prior_mean / prior_variance + sample_mean × n / sigma²) 
                 / (1/prior_variance + n/sigma²)

posterior_variance = 1 / (1/prior_variance + n/sigma²)
```

**Intuition:** "Precision" = 1/variance. High precision = confident = gets more weight.
- Prior with τ²=25: precision = 1/25 = 0.04
- Sample: precision = n/σ² = 10000/25 ≈ 400 → data completely dominates

```python
# Parameters
mu_0 = 25.0      # Prior mean
tau_sq = 25.0    # Prior variance (tau=5, τ²=25)
sigma_sq = df['BMI'].var()   # Known variance (approximated by sample variance)
n = df['BMI'].count()
x_bar = df['BMI'].mean()

# Posterior parameters
precision_prior = 1 / tau_sq
precision_data = n / sigma_sq
precision_posterior = precision_prior + precision_data
sigma_sq_posterior = 1 / precision_posterior
mu_posterior = (precision_prior * mu_0 + precision_data * x_bar) / precision_posterior

print(f"Prior mean: {mu_0}, Prior variance: {tau_sq}")
print(f"Sample mean: {x_bar:.4f}, n: {n}")
print(f"Posterior mean: {mu_posterior:.4f}, Posterior variance: {sigma_sq_posterior:.6f}")

# 95% Credible interval
ci_lower = mu_posterior - 1.96 * np.sqrt(sigma_sq_posterior)
ci_upper = mu_posterior + 1.96 * np.sqrt(sigma_sq_posterior)
print(f"95% Credible Interval: ({ci_lower:.4f}, {ci_upper:.4f})")

# Compare with frequentist 95% CI
se_freq = np.sqrt(sigma_sq / n)
freq_ci = (x_bar - 1.96*se_freq, x_bar + 1.96*se_freq)
print(f"Frequentist 95% CI: ({freq_ci[0]:.4f}, {freq_ci[1]:.4f})")

# Plot
mu_range = np.linspace(25, 32, 1000)
prior = stats.norm(mu_0, np.sqrt(tau_sq)).pdf(mu_range)
posterior = stats.norm(mu_posterior, np.sqrt(sigma_sq_posterior)).pdf(mu_range)

plt.plot(mu_range, prior, 'b-', label='Prior', linewidth=2)
plt.plot(mu_range, posterior, 'r-', label='Posterior', linewidth=2)
plt.axvline(x_bar, color='green', linestyle='--', label='Sample mean')
plt.legend()
plt.title('Bayesian Update: Prior → Posterior for Mean BMI')
```

---

## Q47: Bayesian Hypothesis Testing

### Direct probability statement
```python
# P(μ > 25 | data) — read directly from posterior CDF
posterior_dist = stats.norm(mu_posterior, np.sqrt(sigma_sq_posterior))
prob_mu_greater_25 = 1 - posterior_dist.cdf(25)
print(f"P(μ > 25 | data) = {prob_mu_greater_25:.6f}")
```

This is a direct probability statement. You can't do this in frequentist statistics.

### Bayes Factor

The Bayes Factor compares how well two hypotheses predict the observed data.

```
BF = P(data | H₁) / P(data | H₀)

BF > 1: data favors H₁
BF < 1: data favors H₀
```

For H₁: μ > 25 vs H₀: μ ≤ 25:

```python
# Prior probability of H1 (mu > 25) under the prior
prior_H1 = 1 - stats.norm(mu_0, np.sqrt(tau_sq)).cdf(25)
prior_H0 = 1 - prior_H1

# Posterior probability of H1
post_H1 = prob_mu_greater_25
post_H0 = 1 - post_H1

# Bayes Factor = Posterior odds / Prior odds
prior_odds = prior_H1 / prior_H0
posterior_odds = post_H1 / post_H0
bayes_factor = posterior_odds / prior_odds

print(f"Prior P(H₁): {prior_H1:.4f}")
print(f"Posterior P(H₁): {post_H1:.6f}")
print(f"Bayes Factor: {bayes_factor:.1f}")
```

**Jeffreys' scale:**
| BF | Evidence for H₁ |
|-----|-----------------|
| 1–3 | Barely worth mentioning |
| 3–10 | Moderate |
| 10–30 | Strong |
| 30–100 | Very strong |
| >100 | Decisive |

---

## Q48: Bayesian Linear Regression with PyMC

### Why PyMC?
Conjugate priors (like Beta-Binomial, Normal-Normal) give us closed-form posteriors. But for regression with many coefficients, no closed-form exists. We use MCMC to sample from the posterior instead.

### What MCMC does (intuitively)
Imagine you're trying to find the shape of a mountain range (the posterior distribution) while blindfolded. MCMC does this by: start somewhere, take a random step, accept it if you went uphill (or sometimes even downhill with some probability). After many steps, you've "explored" the entire mountain range. The fraction of time you spend in each area = the height there = the posterior probability.

PyMC uses the NUTS (No U-Turn Sampler) — a smart version of MCMC that doesn't require tuning.

```python
import pymc as pm
import arviz as az

# Prepare data
df_model = df[['BPSysAve', 'Age', 'BMI', 'TotChol']].dropna()
y = df_model['BPSysAve'].values
X = df_model[['Age', 'BMI', 'TotChol']].values

# Build the model
with pm.Model() as bayes_regression:
    
    # Priors — weakly informative
    intercept = pm.Normal('intercept', mu=0, sigma=100)
    beta_age = pm.Normal('beta_age', mu=0, sigma=10)
    beta_bmi = pm.Normal('beta_bmi', mu=0, sigma=10)
    beta_chol = pm.Normal('beta_chol', mu=0, sigma=10)
    sigma = pm.HalfNormal('sigma', sigma=20)  # Must be positive
    
    # Expected value
    mu = intercept + beta_age * X[:, 0] + beta_bmi * X[:, 1] + beta_chol * X[:, 2]
    
    # Likelihood
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y)
    
    # Sample
    trace = pm.sample(draws=4000, tune=1000, chains=4, target_accept=0.9, 
                      return_inferencedata=True, random_seed=42)

# Diagnostics
print(az.summary(trace))   # Mean, SD, 94% CI, R-hat, ESS

az.plot_trace(trace)       # Trace plots — should look like hairy caterpillars

az.plot_posterior(trace)   # Posterior distributions for each parameter

# Posterior predictive checks
with bayes_regression:
    ppc = pm.sample_posterior_predictive(trace)

az.plot_ppc(ppc, observed=az.from_pymc(observed={'y_obs': y}))
```

### Reading the output

**R-hat (Gelman-Rubin):** Compares multiple chains. Should be ≈ 1.0. If R-hat > 1.1 for any parameter, the chains haven't converged — something is wrong.

**ESS (Effective Sample Size):** MCMC samples are autocorrelated (nearby samples are similar). ESS is the equivalent number of independent samples. Should be > 400 for reliable estimates.

**Trace plots:** Should look like a fuzzy caterpillar — random up and down. Trends or drift mean non-convergence.

**Posterior predictive check:** Generate fake data from the model. Compare to real data. If the fake data looks completely different from real data, your model is misspecified.

---

## Q49: Bayesian A/B Test

### The story
Two groups: physically active vs inactive. Does physical activity lower blood pressure?

Frequentist test gives you a p-value. Bayesian test gives you a full distribution over the difference.

```python
# Split data
active = df[df['PhysActive'] == 'Yes']['BPSysAve'].dropna().values
inactive = df[df['PhysActive'] == 'No']['BPSysAve'].dropna().values

with pm.Model() as ab_test:
    # Independent priors for each group mean
    mu_active = pm.Normal('mu_active', mu=120, sigma=20)
    mu_inactive = pm.Normal('mu_inactive', mu=120, sigma=20)
    
    # Shared sigma (or model separately)
    sigma_shared = pm.HalfNormal('sigma', sigma=20)
    
    # Likelihoods
    y_active = pm.Normal('y_active', mu=mu_active, sigma=sigma_shared, observed=active)
    y_inactive = pm.Normal('y_inactive', mu=mu_inactive, sigma=sigma_shared, observed=inactive)
    
    # Derived quantity: difference in means
    diff = pm.Deterministic('diff', mu_inactive - mu_active)  # Positive = active has lower BP
    
    trace_ab = pm.sample(4000, tune=1000, return_inferencedata=True)

# Direct probability statements
diff_samples = trace_ab.posterior['diff'].values.flatten()
print(f"P(inactive BP > active BP | data) = {(diff_samples > 0).mean():.4f}")
print(f"P(difference > 5 mmHg | data) = {(diff_samples > 5).mean():.4f}")
print(f"Posterior mean difference: {diff_samples.mean():.2f} mmHg")
print(f"95% Credible Interval: ({np.percentile(diff_samples, 2.5):.2f}, {np.percentile(diff_samples, 97.5):.2f})")

# Plot posterior of difference
plt.hist(diff_samples, bins=50, edgecolor='black')
plt.axvline(0, color='red', linestyle='--', label='No difference')
plt.axvline(5, color='orange', linestyle='--', label='5 mmHg threshold')
plt.title('Posterior Distribution of BP Difference\n(Active vs Inactive)')
```

---

## Q50: Hierarchical Models — Sharing Strength

### The problem
You want BMI estimates for each race group. Some groups have 5,000 observations, some have 50.

**Two naive approaches:**
1. **Complete pooling:** Ignore race. Report one overall mean for everyone. Misses real group differences.
2. **No pooling:** Compute a separate mean for each group. Groups with n=50 have very uncertain estimates.

**Hierarchical (partial pooling):** Group means are all drawn from a shared distribution. Small groups get "shrunk" toward the grand mean. Large groups stay near their raw estimate.

```python
# Encode race as integer
race_encoder = {race: i for i, race in enumerate(df['Race1'].unique())}
race_idx = df['Race1'].map(race_encoder).dropna().astype(int).values
bmi_vals = df.loc[df['Race1'].notna(), 'BMI'].dropna().values

n_races = len(race_encoder)

with pm.Model() as hierarchical_model:
    # Hyperpriors — shared distribution from which group means are drawn
    grand_mean = pm.Normal('grand_mean', mu=28, sigma=5)
    group_sd = pm.HalfNormal('group_sd', sigma=3)  # How much groups vary
    
    # Group-specific means — drawn from hyperprior
    group_means = pm.Normal('group_means', mu=grand_mean, sigma=group_sd, shape=n_races)
    
    # Individual-level variance
    sigma_individual = pm.HalfNormal('sigma_individual', sigma=10)
    
    # Likelihood
    bmi_obs = pm.Normal('bmi_obs', mu=group_means[race_idx], sigma=sigma_individual, observed=bmi_vals)
    
    trace_hier = pm.sample(2000, tune=1000, return_inferencedata=True)

# Compare hierarchical vs raw estimates
raw_means = df.groupby('Race1')['BMI'].mean()
hierarchical_means = trace_hier.posterior['group_means'].mean(dim=['chain', 'draw']).values

for race, i in race_encoder.items():
    n_group = (df['Race1'] == race).sum()
    print(f"{race}: n={n_group}, Raw={raw_means.get(race, 'N/A'):.2f}, Hierarchical={hierarchical_means[i]:.2f}")
```

**Shrinkage pattern:** Small groups (low n) → hierarchical estimate is pulled hard toward grand mean. Large groups (high n) → hierarchical estimate ≈ raw estimate.

This is the "regularization" effect of the hierarchical structure. It prevents overfitting in small groups.

---

## Q51: The Essay — Bayesian vs Frequentist

### Structure of the essay

**Paragraph 1: When they agreed**
With n=10,000, priors are overwhelmed by data. Bayesian credible intervals and frequentist confidence intervals are nearly identical numerically. t-tests and Bayesian A/B tests reach the same directional conclusion.

**Paragraph 2: When they disagreed**
- Bayesian gives direct probability statements; frequentist can't ("95% probability that μ > 25" vs "reject H₀")
- Hierarchical models have no clean frequentist analog for this dataset
- Bayes Factors can provide evidence FOR the null; p-values can't
- With small subgroups (race × age interactions), hierarchical Bayesian estimates are much better calibrated

**Paragraph 3: When frequentist was more useful**
- Computational simplicity: t-test takes milliseconds, PyMC takes minutes
- Interpretability: most clinical guidelines use p-values and CIs
- When no prior knowledge exists and you don't want to bake in assumptions

**Paragraph 4: When Bayesian was more useful**
- Making decisions with probability thresholds (Q49 A/B test)
- Incorporating prior knowledge (prior diabetes prevalence)
- Small subgroup estimation (Q50 hierarchical)
- When communicating to stakeholders who want "What's the probability it works?"

**Paragraph 5: Honest synthesis**
These aren't competing religions. They're different tools that answer slightly different questions. The frequentist framework is dominant in scientific publishing because of convention. The Bayesian framework is more intuitive for decision-making. A skilled statistician knows when to use each.

---

<a name="part-8"></a>
# PART 8: The Capstone
## Sections A through E

---

## The Overarching Research Question
"What are the most significant predictors of diabetes in the U.S. adult population, and how do these risk factors interact to influence diabetes prevalence across demographic groups?"

This is the question that ties your entire assignment together. Everything you learned in Parts 1–7 exists to help you answer this.

---

## Section A: Data Preparation & Exploration

### Missing value strategy
```python
# Check missing values
missing = df.isnull().sum() / len(df) * 100
print(missing[missing > 0].sort_values(ascending=False))

# Strategy by column:
# < 5% missing → drop rows (listwise deletion)
# > 5% but < 20% → impute
# > 20% → consider dropping the column

# For this assignment: document what you do and why
df_clean = df.copy()

# Impute continuous variables with median (robust to outliers)
for col in ['BMI', 'TotChol', 'BPSysAve']:
    df_clean[col].fillna(df_clean[col].median(), inplace=True)

# Impute categorical with mode
for col in ['PhysActive', 'SmokeNow']:
    df_clean[col].fillna(df_clean[col].mode()[0], inplace=True)
```

### Derived features
```python
# BMI categories
df_clean['BMI_Cat'] = pd.cut(df_clean['BMI'], 
                              bins=[0, 18.5, 25, 30, 100],
                              labels=['Underweight', 'Normal', 'Overweight', 'Obese'])

# Age groups
df_clean['Age_Group'] = pd.cut(df_clean['Age'], 
                                bins=[0, 30, 45, 60, 100],
                                labels=['18-30', '31-45', '46-60', '61+'])

# Metabolic syndrome indicator (simplified)
df_clean['MetSyn'] = (
    (df_clean['BMI'] >= 30) & 
    (df_clean['BPSysAve'] >= 130) & 
    (df_clean['TotChol'] >= 200)
).astype(int)
```

### EDA checklist with code
```python
# 1. Summary statistics for all key variables
print(df_clean[['Age', 'BMI', 'BPSysAve', 'TotChol']].describe())

# 2. Distribution plots (continuous)
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
for ax, col in zip(axes.flat, ['Age', 'BMI', 'BPSysAve', 'TotChol']):
    df_clean[col].hist(bins=50, ax=ax)
    ax.set_title(col)

# 3. Correlation heatmap
import seaborn as sns
corr_matrix = df_clean[['Age', 'BMI', 'BPSysAve', 'TotChol']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)

# 4. Diabetes probability by predictor
diabetes_by_bmi = df_clean.groupby('BMI_Cat')['Diabetes'].apply(lambda x: (x=='Yes').mean())
diabetes_by_age = df_clean.groupby('Age_Group')['Diabetes'].apply(lambda x: (x=='Yes').mean())
```

### Ranking predictors by conditional probability
```python
# Compute P(Diabetes=Yes | predictor high) for each continuous predictor
results = {}
for col in ['Age', 'BMI', 'BPSysAve', 'TotChol']:
    median_val = df_clean[col].median()
    p_high = (df_clean[df_clean[col] > median_val]['Diabetes'] == 'Yes').mean()
    p_low = (df_clean[df_clean[col] <= median_val]['Diabetes'] == 'Yes').mean()
    results[col] = {'P(Diabetes|high)': p_high, 'P(Diabetes|low)': p_low, 
                    'Difference': p_high - p_low}

pd.DataFrame(results).T.sort_values('Difference', ascending=False)
```

---

## Section B: Simulation & Estimation

### Bootstrap CIs for diabetes prevalence by demographic subgroup
```python
def bootstrap_proportion_ci(data, col, condition_col, condition_val, 
                              n_bootstrap=1000, alpha=0.05):
    """Bootstrap CI for P(Diabetes=Yes) in a subgroup"""
    subset = data[data[condition_col] == condition_val][col]
    original_prop = (subset == 'Yes').mean()
    n = len(subset)
    
    boot_props = []
    for _ in range(n_bootstrap):
        boot_sample = subset.sample(n, replace=True)
        boot_props.append((boot_sample == 'Yes').mean())
    
    ci_lower = np.percentile(boot_props, alpha/2 * 100)
    ci_upper = np.percentile(boot_props, (1 - alpha/2) * 100)
    
    return original_prop, ci_lower, ci_upper, n

# Apply across subgroups
results = []
for age_grp in df_clean['Age_Group'].unique():
    for gender in df_clean['Gender'].unique():
        subset = df_clean[(df_clean['Age_Group'] == age_grp) & (df_clean['Gender'] == gender)]
        if len(subset) > 10:
            prop, lo, hi, n = bootstrap_proportion_ci(
                subset, 'Diabetes', col=None, ...
            )
            ci_width = hi - lo
            results.append({
                'Age Group': age_grp, 'Gender': gender, 
                'n': n, 'Prevalence': prop,
                'CI Lower': lo, 'CI Upper': hi, 'CI Width': ci_width
            })

results_df = pd.DataFrame(results).sort_values('CI Width', ascending=False)
print(results_df.head(10))  # Widest CIs = smallest subgroups
```

---

## Section C: Hypothesis Testing Battery

### Template for each hypothesis
```python
def run_hypothesis_test(df, hypothesis_name, test_func, *args, **kwargs):
    """Wrapper to standardize hypothesis test output"""
    stat, p = test_func(*args, **kwargs)
    return {
        'Hypothesis': hypothesis_name,
        'Test': test_func.__name__,
        'Statistic': stat,
        'p-value': p,
        'Significant (α=0.05)': p < 0.05
    }
```

### H1: Mean BMI differs between diabetic and non-diabetic
```python
bmi_diabetic = df_clean[df_clean['Diabetes'] == 'Yes']['BMI'].dropna()
bmi_nondiabetic = df_clean[df_clean['Diabetes'] == 'No']['BMI'].dropna()

t_stat, p_val = stats.ttest_ind(bmi_diabetic, bmi_nondiabetic, equal_var=False)
s_pooled = np.sqrt(((len(bmi_diabetic)-1)*bmi_diabetic.var() + 
                     (len(bmi_nondiabetic)-1)*bmi_nondiabetic.var()) / 
                    (len(bmi_diabetic)+len(bmi_nondiabetic)-2))
cohen_d = (bmi_diabetic.mean() - bmi_nondiabetic.mean()) / s_pooled
```

### H2: Physical activity differs between diabetic/non-diabetic (chi-squared)
```python
# Cross-tabulation
ct = pd.crosstab(df_clean['Diabetes'], df_clean['PhysActive'])
chi2_stat, p_chi2, dof, expected = stats.chi2_contingency(ct)

# Effect size: Cramér's V
n = ct.sum().sum()
k = min(ct.shape) - 1
cramers_v = np.sqrt(chi2_stat / (n * k))
```

### H3: Non-linear relationship between age and diabetes
```python
import statsmodels.formula.api as smf
from sklearn.preprocessing import PolynomialFeatures

# Add age squared to logistic regression
df_clean['Age_sq'] = df_clean['Age'] ** 2
df_clean['Diabetes_bin'] = (df_clean['Diabetes'] == 'Yes').astype(int)

model_linear = smf.logit('Diabetes_bin ~ Age', data=df_clean).fit()
model_nonlinear = smf.logit('Diabetes_bin ~ Age + Age_sq', data=df_clean).fit()

# Is the quadratic term significant?
print(model_nonlinear.summary())
print(f"\nLikelihood Ratio Test:")
print(f"Linear AIC: {model_linear.aic:.1f}, Nonlinear AIC: {model_nonlinear.aic:.1f}")

# Plot predicted probabilities vs age
age_range = np.linspace(df_clean['Age'].min(), df_clean['Age'].max(), 100)
pred_data = pd.DataFrame({'Age': age_range, 'Age_sq': age_range**2})
pred_probs = model_nonlinear.predict(pred_data)

plt.plot(age_range, pred_probs)
plt.xlabel('Age')
plt.ylabel('P(Diabetes)')
plt.title('Predicted Probability of Diabetes vs Age (Nonlinear Model)')
```

### Multiple comparison correction across H1-H5
```python
all_p_values = [p_val_H1, p_chi2_H2, p_nonlinear_H3, p_interaction_H4, p_race_H5]
reject, p_corrected, _, _ = multipletests(all_p_values, method='holm')

summary_table = pd.DataFrame({
    'Hypothesis': ['H1: BMI by Diabetes', 'H2: PhysActive by Diabetes', 
                   'H3: Age nonlinear', 'H4: Gender×BMI interaction', 
                   'H5: Race after controlling BMI+Age'],
    'Test': ['Welch t-test', 'Chi-squared', 'LR test (logistic)', 
             'Interaction in logistic', 'Logistic with controls'],
    'Raw p': all_p_values,
    'Corrected p (Holm)': p_corrected,
    'Significant': reject
})
print(summary_table.to_string())
```

---

## Section D: Predictive Modeling

### Logistic regression — interpreting odds ratios
```python
import statsmodels.formula.api as smf

formula = 'Diabetes_bin ~ Age + BMI + C(Gender) + C(PhysActive) + C(SmokeNow) + TotChol + C(Race1)'
logit_model = smf.logit(formula, data=df_clean).fit()
print(logit_model.summary())

# Odds ratios
or_table = pd.DataFrame({
    'Odds Ratio': np.exp(logit_model.params),
    'CI Lower': np.exp(logit_model.conf_int()[0]),
    'CI Upper': np.exp(logit_model.conf_int()[1]),
    'p-value': logit_model.pvalues
})

# Forest plot of odds ratios
plt.figure(figsize=(8, 10))
y_pos = range(len(or_table))
plt.barh(y_pos, or_table['Odds Ratio'], 
         xerr=[or_table['Odds Ratio'] - or_table['CI Lower'],
               or_table['CI Upper'] - or_table['Odds Ratio']])
plt.axvline(1, color='red', linestyle='--')
plt.yticks(y_pos, or_table.index)
plt.xlabel('Odds Ratio (95% CI)')
plt.title('Logistic Regression: Odds Ratios for Diabetes Predictors')
```

**Interpreting odds ratios:**
- OR for BMI = 1.09: each 1-unit BMI increase multiplies odds of diabetes by 1.09 (9% increase)
- OR for PhysActive = 0.75: active people have 25% lower odds of diabetes than inactive
- OR = 1.0: no association

### Stochastic process framework for pre-diabetes
```python
# States: Normal → Pre-diabetic → Diabetic
# Use age bins as proxy for time progression

# This connects back to Q36-Q39
# Estimate 3-state transition matrix
# Compute absorption probability from Pre-diabetic state into Diabetic

states_prediabetic = ['Normal', 'Pre-diabetic', 'Diabetic']
# ... (reuse code from Q39, with 3 states now)

# Clinical interpretation: if someone is pre-diabetic today,
# what's their long-run probability of developing diabetes?
absorption_prob = B[1][0]  # Probability of ending in Diabetic from Pre-diabetic
print(f"Long-run probability of developing diabetes from pre-diabetic state: {absorption_prob:.2%}")
```

---

## Section E: Presentation & Communication

### Executive summary structure

```
WHAT WE WANTED TO KNOW
In one sentence: The goal was to identify which factors most strongly predict 
diabetes in U.S. adults and how they interact across demographic groups.

KEY FINDINGS
• BMI is the single strongest modifiable predictor: obese adults (BMI ≥ 30) are 
  X times more likely to have diabetes than normal-weight adults.
• Age matters independently: each decade of age increases diabetes odds by X%.
• Physical activity is protective: active adults have XX% lower odds of diabetes.
• Racial disparities persist even after controlling for BMI and age.
• The Markov model shows that pre-diabetic individuals have a XX% long-run 
  probability of developing diabetes under current transition rates.

WHAT THIS MEANS
If we could move the obesity rate down by 10%, the model predicts X fewer diabetic
cases in this population.

LIMITATIONS
• This is cross-sectional data — we cannot prove causation.
• Self-reported physical activity may be overestimated.
• Racial disparities may reflect unmeasured socioeconomic factors.
```

### Choosing your 3–5 figures

**Figure 1: The landscape** — Heatmap of diabetes prevalence by (age group × BMI category). Immediately shows the interaction between age and obesity.

**Figure 2: What predicts it** — Forest plot of logistic regression odds ratios with confidence intervals. Clean, publication-ready.

**Figure 3: Uncertainty by subgroup** — Bootstrap CIs for prevalence in each demographic subgroup. Shows where the data is rich vs sparse.

**Figure 4: Long-run trajectory** — Markov chain state evolution over time. Shows where the population is heading.

**Figure 5 (optional): Bayesian update** — Prior → Posterior for diabetes prevalence. Demonstrates Bayesian reasoning visually.

---

<a name="quick-reference"></a>
# Quick Reference Tables

## Choosing a Test

| Situation | Test to Use |
|-----------|-------------|
| 1 group vs known value, normal | One-sample t-test |
| 2 independent groups, normal | Welch's t-test |
| 2 paired measurements, normal | Paired t-test |
| 2 independent groups, non-normal/small | Mann-Whitney U |
| 2 paired measurements, non-normal | Wilcoxon signed-rank |
| 3+ groups, normal | One-way ANOVA + Tukey HSD |
| 3+ groups, non-normal | Kruskal-Wallis + Dunn's |
| 2 categorical variables | Chi-squared |
| Count data | Chi-squared goodness of fit |
| Continuous outcome, many predictors | OLS linear regression |
| Binary outcome, any predictors | Logistic regression |
| Proportion with prior belief | Beta-Binomial (Bayesian) |
| Mean with prior belief | Normal-Normal (Bayesian) |
| Complex multi-parameter model | PyMC + MCMC |
| Events over continuous time | Poisson process |
| Discrete state transitions | Markov chain |
| State transitions, continuous time | CTMC |

## Cohen's d Effect Sizes

| d | Verbal label | Visual analogy |
|---|--------------|---------------|
| 0.2 | Small | Two overlapping distributions, barely distinguishable |
| 0.5 | Medium | Clearly different, significant overlap |
| 0.8 | Large | Distributions obviously different |
| 1.2+ | Very large | Almost no overlap |

## Multiple Comparison Corrections

| Correction | Controls | When to use |
|------------|----------|-------------|
| Bonferroni | FWER (strict) | Few tests, conservative needed |
| Holm | FWER (less strict) | Same as Bonferroni but better |
| Benjamini-Hochberg | FDR | Many tests, exploratory analysis |
| Tukey HSD | FWER for all pairs | Post-hoc after ANOVA |
| Dunn's + Bonferroni | FWER for all pairs | Post-hoc after Kruskal-Wallis |

## Bayesian Reference

| Concept | Formula/Code |
|---------|-------------|
| Beta-Binomial posterior | `Beta(α + k, β + n-k)` |
| Normal-Normal posterior mean | `(prior_precision*mu0 + data_precision*x_bar) / total_precision` |
| Credible interval | `posterior_dist.ppf([0.025, 0.975])` |
| Bayes Factor | `(post_H1/post_H0) / (prior_H1/prior_H0)` |
| R-hat convergence | Should be ≤ 1.1 |

## Regression Diagnostics

| Plot | What it checks | Good pattern | Bad pattern |
|------|---------------|--------------|-------------|
| Residuals vs Fitted | Linearity, homoscedasticity | Random cloud around 0 | Curve, cone shape |
| Q-Q of residuals | Normality | Points on 45° diagonal | S-curve, tails off |
| Scale-Location | Homoscedasticity | Flat red line | Upward slope |
| Cook's Distance | Influential observations | Most points near 0 | Isolated spikes |

## VIF Interpretation

| VIF | Action |
|-----|--------|
| 1–5 | Fine, no action needed |
| 5–10 | Investigate, consider dropping one predictor |
| >10 | Severe — fix before trusting coefficients |

## Stochastic Processes Cheat Sheet

| Concept | Key formula | Intuition |
|---------|------------|-----------|
| DTMC stationary distribution | `πP = π, Σπ = 1` | Long-run fraction of time in each state |
| P^∞ | `np.linalg.matrix_power(P, 1000)` | All rows → π |
| Absorbing chain fundamental matrix | `N = (I - Q)⁻¹` | Expected visits to transient states |
| Absorption probability | `B = N @ R` | Prob of ending in absorbing state |
| CTMC | `P(t) = exp(Qt)` | State probs at continuous time t |
| Poisson inter-arrivals | Exponential(λ) | Mean wait = 1/λ |
| Random walk variance | `Var(S_n) = n·σ²` | Spread grows as √n |
| Superposition | Poisson(λ₁ + λ₂) | Merging two independent Poisson streams |
| Thinning | Poisson(p·λ) | Sub-sampling a Poisson stream |

---

## How the Parts Connect

```
Part 1 (Probability) ──────────────────→ Underpins every test in Parts 4 & 7
    ↓                                        P(X), P(X|Y), distributions
    
Part 2 (Simulation) ──────────────────→ Monte Carlo for power (Q14)
    ↓                                        Bootstrap (Q13, used in Part 8)
    ↓                                        Markov chain simulation (Q36)
    
Part 3 (Estimation) ──────────────────→ Confidence intervals in Part 4
    ↓                                        MLE for distributions
    ↓                                        Compared to Bayesian CIs in Part 7
    
Part 4 (Hypothesis Testing) ──────────→ t-tests reused in Capstone (Section C)
    ↓                                        Non-parametric tests as backup
    ↓                                        Multiple comparisons in Capstone
    
Part 5 (Regression) ──────────────────→ OLS replicated Bayesian in Part 7 (Q48)
    ↓                                        Logistic regression in Capstone (D)
    ↓                                        Interaction effects in Capstone (C-H4)
    
Part 6 (Stochastic Processes) ────────→ Markov chain in Capstone (D)
    ↓                                        Absorption prob = long-run diabetes risk
    ↓                                        Poisson for health event modeling
    
Part 7 (Bayesian) ────────────────────→ Bayesian regression vs OLS (comparison in Capstone D)
    ↓                                        Hierarchical model for subgroups (Part 8 B)
    ↓                                        A/B test framework for interventions
    
Part 8 (Capstone) ────────────────────→ All of the above, unified under one research question
```

*You've done Parts 1–3. The foundation is solid. Parts 4–7 are extensions of the same core ideas. Part 8 is the same ideas applied to one coherent story.*
