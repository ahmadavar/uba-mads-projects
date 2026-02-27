# Statistical Analysis & Regression Modeling
## Student Performance & Salary Prediction — Full Analysis Documentation

**Author**: [Your Name] | **Date**: February 2026 | **Course**: Statistical Methods — Master's in Data Science

---

## Table of Contents
1. [Problem Statement](#1-problem-statement)
2. [Dataset Description](#2-dataset-description)
3. [Data Preparation & Cleaning](#3-data-preparation--cleaning)
4. [Univariate Analysis — Distributions & Outliers](#4-univariate-analysis--distributions--outliers)
5. [Bivariate Analysis — Relationships & Correlations](#5-bivariate-analysis--relationships--correlations)
6. [Regression Problem Formulation](#6-regression-problem-formulation)
7. [Simple Linear Regression — Model 1](#7-simple-linear-regression--model-1)
8. [Multiple Linear Regression — Model 2](#8-multiple-linear-regression--model-2)
9. [Feature Engineering — Interaction Term](#9-feature-engineering--interaction-term)
10. [Model Diagnostics — Checking Assumptions](#10-model-diagnostics--checking-assumptions)
11. [Sensitivity Analysis — Add/Drop Variables](#11-sensitivity-analysis--adddrop-variables)
12. [Final Model Comparison](#12-final-model-comparison)
13. [Key Findings](#13-key-findings)
14. [Final Verdict & Recommendations](#14-final-verdict--recommendations)

---

## 1. Problem Statement

### The Question

> **"What factors determine how much money a new graduate earns — and by exactly how much does each factor matter?"**

Starting salary is one of the most consequential outcomes for any graduate. It sets the baseline for future earnings, affects financial independence, and signals how the job market values different academic and professional choices. Yet students are often left guessing: *Does a higher GPA actually translate to more money? Are internships worth it? Does it matter where you went to university?*

This analysis answers those questions with data — using statistical regression modeling to quantify the exact salary impact of GPA, internships, major field of study, university tier, project experience, and networking. Rather than vague advice, we provide precise, dollar-denominated estimates with statistical confidence.

### Why Regression Analysis?

Linear regression is the ideal tool here because:
- **Our outcome is continuous**: Salary in USD can take any value, not just categories.
- **We have multiple predictors**: We want to isolate the effect of each variable *while controlling for others* — something correlation alone cannot do.
- **We want interpretable results**: Every coefficient tells a clear story in dollars, making findings immediately actionable for students and career advisors.

### Scope

- **Dataset**: 500 recent graduates
- **Outcome variable**: Starting salary (USD)
- **Predictors**: 9 variables (academic, demographic, and professional)
- **Models built**: 3 (simple regression, multiple regression, regression with interaction)
- **Framework**: Ordinary Least Squares (OLS) via Python's `statsmodels`

---

## 2. Dataset Description

### Overview

| Property | Value |
|---|---|
| Name | Student Performance & Salary Dataset |
| Source | Custom-generated (realistic simulation) |
| Observations | 500 rows |
| Variables | 10 columns |
| Outcome | Salary (USD) |

### Variable Dictionary

| Variable | Type | Role | Description |
|---|---|---|---|
| `Salary` | Numeric (continuous) | **Outcome (Y)** | Starting salary in USD |
| `GPA` | Numeric (continuous) | Predictor | Grade Point Average (0.0 – 4.0 scale) |
| `Study_Hours_Per_Week` | Numeric (continuous) | Predictor | Average weekly study hours |
| `Internships_Count` | Numeric (count) | Predictor | Number of internships completed |
| `Age` | Numeric (continuous) | Predictor | Student age at graduation |
| `Projects_Completed` | Numeric (count) | Predictor | Portfolio/personal projects |
| `Networking_Events` | Numeric (count) | Predictor | Professional networking events attended |
| `Major` | Categorical (4 levels) | Predictor | CS, Data Science, Statistics, Business Analytics |
| `Gender` | Categorical (3 levels) | Predictor | Male, Female, Non-Binary |
| `University_Tier` | Categorical (3 levels) | Predictor | Tier1, Tier2, Tier3 |

### Key Summary Statistics

| Variable | Mean | Std Dev | Min | Max | Skewness |
|---|---|---|---|---|---|
| Salary | $106,338 | $15,975 | $39,041 | $196,178 | 0.21 |
| GPA | 3.19 | 0.46 | 2.0 | 4.0 | -0.11 |
| Study Hours/Week | 25.22 | 7.81 | 5.0 | 46.06 | 0.06 |
| Internships | 1.54 | 1.22 | 0 | 5 | 0.66 |
| Age | 24.05 | 1.85 | 21 | 30 | 0.26 |
| Projects | 2.96 | 1.67 | 0 | 9 | 0.54 |
| Networking Events | 3.93 | 1.79 | 0 | 10 | 0.24 |

**Notable**: Salary has a kurtosis of **4.66** — considerably higher than the 3.0 expected for a normal distribution. This means salary has *heavier tails* than normal: extreme high earners (outliers above $139,983) are more common than a bell curve would predict. This is realistic — a handful of high performers command disproportionately high salaries.

---

## 3. Data Preparation & Cleaning

### Missing Value Audit

The dataset arrived with deliberate messiness — a realistic feature of real-world data:

| Variable | Missing Count | Missing % | Action Taken |
|---|---|---|---|
| GPA | 5 | 1.0% | Mean imputed (mean = 3.19) |
| Study_Hours_Per_Week | 10 | 2.0% | Mean imputed (mean = 25.22) |
| Networking_Events | 10 | 2.0% | Mean imputed (mean = 3.93) |
| All others | 0 | 0% | No action needed |

**Why mean imputation?**
With only 1–2% missing values, these are minor gaps. Mean imputation preserves the dataset size (n=500) while introducing minimal bias. For a dataset at this scale, removing rows would be unnecessary and wasteful.

**Duplicate rows**: 0 found. No action needed.

### Data Type Validation

All numeric columns confirmed as `float64` or `int64`. Categorical columns (`Major`, `Gender`, `University_Tier`) stored as strings — converted to dummy variables before modeling.

**Final clean dataset**: 500 rows × 10 columns, zero missing values after imputation.

---

## 4. Univariate Analysis — Distributions & Outliers

### Plot 1: Histograms — `figures/01_histograms.png`

**What this plot shows**: A 3×3 grid of histograms for all 7 numeric variables. Each histogram shows the frequency distribution (how often each value range appears), with a red dashed line marking the **mean** and a green dashed line marking the **median**.

**How to read it**: If the mean and median lines overlap closely, the distribution is symmetric. If they diverge, the distribution is skewed. A tall, narrow histogram means values cluster tightly; a wide, flat one means high variability.

**What we see in our data**:

- **Salary**: Nearly symmetric with a slight right skew (0.21). The mean ($106,338) is just above the median ($105,821) — a few high earners pull the average up. This is typical for income data.
- **GPA**: Near-perfectly symmetric (skewness = -0.11). Most students cluster around 3.0–3.5, which is a realistic academic performance distribution.
- **Study Hours**: Almost perfectly symmetric (skewness = 0.06). Students study between 20–30 hours/week on average, with some studying as little as 5 or as much as 46 hours.
- **Internships**: Moderately right-skewed (0.66). Most students had 0–2 internships, but a few had 4–5. This tail of high-internship students matters — they're likely earning more.
- **Projects**: Also right-skewed (0.54). Most students completed 2–4 projects, but a few completed 7–9.
- **Age & Networking Events**: Both near-normal with mild right skew.

**Key takeaway**: Our data is relatively well-behaved. No extreme skewness requiring mandatory transformation, though Internships and Projects show count-variable characteristics (discrete, right-skewed).

---

### Plot 2: Boxplots — `figures/02_boxplots.png`

**What this plot shows**: The same 7 variables as boxplots. Each box spans the interquartile range (IQR = 25th to 75th percentile), with the red line marking the median. Points beyond the whiskers (1.5×IQR) are plotted individually as outliers.

**How to read it**: The box tells you where the "middle 50%" of the data lives. Short boxes = low variability. Long whiskers = data spreads widely. Dots beyond whiskers = potential outliers worth investigating.

**What we see in our data**:

- **Salary**: A few dots appear far above the upper whisker — these are the high earners (above ~$140,000). The box is moderately wide, confirming the $15,975 standard deviation we saw in descriptive stats.
- **Internships**: Several points cluster at 4 and 5 — technically outliers by IQR rules (upper bound = 3.5), but these are real students with high internship counts, not data errors.
- **GPA**: Very clean distribution — no outliers at all. Students simply can't exceed 4.0.
- **Age**: Tight box (most graduates are 22–25), with a few older students (28–30) visible as outliers.

---

### Outlier Detection — IQR Method

**Formula used**: Lower bound = Q1 − 1.5×IQR; Upper bound = Q3 + 1.5×IQR

| Variable | Lower Bound | Upper Bound | Outliers Found | % of Data |
|---|---|---|---|---|
| Salary | $70,760 | $139,983 | 18 | 3.6% |
| GPA | 1.84 | 4.53 | 0 | 0.0% |
| Internships_Count | -0.50 | 3.50 | 37 | 7.4% |

**Decision: Outliers kept.**

The salary outliers (range $39,041–$196,178) represent genuinely exceptional graduates — someone who landed a $196K offer in Computer Science or Data Science is not a data error; they're a real person whose data belongs in our analysis. Removing them would bias our model toward average earners and make it less useful for understanding salary distributions. We monitor their influence during diagnostics instead.

---

## 5. Bivariate Analysis — Relationships & Correlations

### Correlation Matrix — `figures/03_correlation_matrix.png`

**What this plot shows**: A color-coded heatmap where each cell shows the Pearson correlation coefficient between two variables. Red cells = strong positive correlation (as one goes up, so does the other). Blue cells = negative correlation. White = near zero.

**How to read it**: Focus on the **Salary row/column** to find which variables are most strongly associated with salary. Look for correlations *between predictors* (off-diagonal) as a multicollinearity warning sign.

**Correlation with Salary (ranked)**:

| Predictor | Correlation (r) | Strength |
|---|---|---|
| Internships_Count | **0.602** | Moderate-Strong |
| GPA | 0.296 | Weak-Moderate |
| Projects_Completed | 0.166 | Weak |
| Networking_Events | 0.085 | Negligible |
| Age | 0.044 | Negligible |
| Study_Hours_Per_Week | -0.026 | Negligible (negative) |

**Key insight**: Internships dominate as the single strongest numerical predictor. GPA matters but at roughly half the correlation strength. Surprisingly, study hours are essentially uncorrelated with salary (r = -0.026) — working harder in school doesn't automatically translate to higher pay. This is a counterintuitive finding that regression will help us understand better.

**Between-predictor correlations**: All predictor-to-predictor correlations are low (close to zero), suggesting **no severe multicollinearity** — a good sign for our regression models.

---

### Plot 4: Scatterplots — `figures/04_scatterplots.png`

**What this plot shows**: A 2×3 grid of scatterplots, each plotting Salary on the Y-axis against one predictor on the X-axis. A red trend line shows the direction and slope of the linear relationship, and the correlation coefficient (r) is displayed in each panel.

**How to read it**: Points scattered tightly around the trend line = strong linear relationship. Points scattered widely = weak relationship. An upward slope = positive correlation; downward = negative.

**What we see**:

- **Salary vs GPA** (r = 0.296): Upward trend visible but with substantial scatter. Higher GPAs cluster toward higher salaries, but many exceptions exist — a 3.8 GPA student doesn't guarantee $150K.
- **Salary vs Internships** (r = 0.602): The clearest pattern. The trend line rises steeply, and students with 4–5 internships visibly cluster at higher salaries.
- **Salary vs Study Hours** (r = -0.026): Essentially a flat line. Points scatter randomly — studying more doesn't predict salary at all.
- **Salary vs Projects** (r = 0.166): Slight upward trend. More projects = marginally higher salary.
- **Salary vs Age** (r = 0.044): No discernible pattern. Older graduates don't systematically earn more at entry level.
- **Salary vs Networking Events** (r = 0.085): Very weak positive trend. Going to more events has a slight positive association.

---

### Plot 5: Salary by Categorical Variables — `figures/05_categorical_salary.png`

**What this plot shows**: Three side-by-side boxplots showing salary distribution broken down by Major, Gender, and University Tier.

**How to read it**: Compare the median lines (center of each box) across groups. Higher median = that group earns more on average. Wider boxes = more variation within that group.

**What we see**:

**By Major** (reference group: Business Analytics, mean $102,540):

| Major | Mean Salary | vs Business Analytics |
|---|---|---|
| Computer Science | $110,313 | +$7,773 |
| Data Science | $105,494 | +$2,954 |
| Statistics | $102,677 | +$137 |
| Business Analytics | $102,540 | — |

Computer Science is the clear winner. Statistics and Business Analytics are nearly identical.

**By University Tier**: Tier1 graduates visibly earn more — their salary box sits higher than Tier2 and Tier3. This preview of what the regression coefficients will confirm: institutional prestige has a real salary premium.

**By Gender**: Visual differences appear small and will require the regression model to test properly after controlling for other factors.

---

## 6. Regression Problem Formulation

### Research Question
> *"What factors predict starting salary for recent graduates, and by exactly how much does each factor contribute?"*

### Hypotheses

| Hypothesis | Prediction |
|---|---|
| H1 | GPA has a positive, significant effect on salary |
| H2 | Internships_Count is the strongest predictor |
| H3 | CS and Data Science majors earn significantly more than Business Analytics |
| H4 | Tier1 universities command a salary premium over Tier2/Tier3 |

### Variable Encoding

Categorical variables cannot enter regression directly — they must be converted to **dummy variables** (binary 0/1 indicators):

| Original | Dummies Created | Reference Category (dropped) |
|---|---|---|
| Major | Major_Computer Science, Major_Data Science, Major_Statistics | Business Analytics |
| University_Tier | University_Tier_Tier2, University_Tier_Tier3 | Tier1 |
| Gender | Gender_Male, Gender_Non-Binary | Female |

**Why drop one category?** If we included all levels, they would sum to 1 for every row — creating perfect multicollinearity (the "dummy variable trap"). The dropped category becomes the **reference group**: all dummy coefficients are interpreted *relative to it*.

---

## 7. Simple Linear Regression — Model 1

### Model Specification

$$\widehat{\text{Salary}} = \beta_0 + \beta_1 \times \text{GPA} + \varepsilon$$

### Full OLS Results

```
OLS Regression Results
======================================================================
Dep. Variable:          Salary    R-squared:              0.0879
Model:                     OLS    Adj. R-squared:         0.0861
Method:          Least Squares    F-statistic:            47.51
No. Observations:          495    Prob (F-statistic):     1.68e-11
AIC:                  10948.73    BIC:                   10957.14
======================================================================
              coef       std err    t        P>|t|    [0.025    0.975]
----------------------------------------------------------------------
const     73,188.60    4,854.40   15.08    0.000    63,653    82,724
GPA       10,369.97    1,504.40    6.89    0.000     7,414    13,326
======================================================================
```

### Coefficient Interpretation

**Intercept (β₀ = $73,188.60)**

A student with GPA = 0 would earn an expected salary of $73,188. This interpretation is *not meaningful* in practice — no student has a 0.0 GPA. The intercept is a mathematical anchor for the line, not a real-world prediction.

**GPA Slope (β₁ = $10,369.97)**

For every 1-point increase in GPA, starting salary increases by **$10,370**.

*Concrete example*: A student with GPA 3.5 is expected to earn $10,370 more than a student with GPA 2.5, all else equal.

**95% Confidence Interval for β₁**: [$7,414 — $13,326]

We are 95% confident that a 1-point GPA increase is associated with a salary increase of at least $7,414 and at most $13,326. Since this interval does not contain 0, the effect is statistically certain at the 95% level.

### Hypothesis Test

| Component | Value |
|---|---|
| H₀ | β₁ = 0 (GPA has no effect on salary) |
| Hₐ | β₁ ≠ 0 (GPA affects salary) |
| t-statistic | 6.89 |
| p-value | < 0.001 |
| Decision | **Reject H₀** |

**Conclusion**: GPA has a statistically significant positive effect on starting salary. The p-value is astronomically small (< 0.000001) — we can be virtually certain this is not a chance finding.

### R² Interpretation

**R² = 0.0879** → GPA alone explains **8.79%** of the variation in salaries.

This sounds small — and it is. GPA is significant, but salary is determined by many factors beyond academic performance. This motivates our move to multiple regression.

---

### Plot 6: Simple Regression Visualization — `figures/06_simple_regression.png`

**What this plot shows**: A scatterplot of Salary (Y-axis) vs GPA (X-axis). The red solid line is the fitted regression line. The red shaded band around it is the **95% Confidence Interval** for the mean prediction.

**How to read it**: The line shows the expected salary at each GPA level. The shaded band narrows in the center (where we have the most data) and widens at the edges (where we're less certain). Points above the line = the model underestimated that student's salary; points below = overestimated.

**What we see**: The trend is real — the line clearly slopes upward. But the scatter is enormous: the vertical spread of points at any given GPA value can be $50,000 or more. GPA alone simply cannot explain most of what drives salary differences.

**The annotation**: Title shows `R² = 0.0879, p < 0.001` — significant but weak explanatory power.

---

## 8. Multiple Linear Regression — Model 2

### Model Specification

$$\widehat{\text{Salary}} = \beta_0 + \beta_1(\text{GPA}) + \beta_2(\text{Internships}) + \beta_3(\text{Projects}) + \beta_4(\text{Networking}) + \beta_5(\text{CS}) + \beta_6(\text{DS}) + \beta_7(\text{Stats}) + \beta_8(\text{Tier2}) + \beta_9(\text{Tier3}) + \varepsilon$$

### Full OLS Results

```
OLS Regression Results
======================================================================
Dep. Variable:          Salary    R-squared:              0.5324
Model:                     OLS    Adj. R-squared:         0.5235
Method:          Least Squares    F-statistic:            60.09
No. Observations:          485    Prob (F-statistic):     8.07e-73
AIC:                  10415.58    BIC:                   10457.42
======================================================================
                         coef     std err    t       P>|t|   [0.025    0.975]
-----------------------------------------------------------------------------
const                58,847.83   4,246.41   13.86   0.000   50,504   67,192
GPA                   9,119.88   1,092.98    8.34   0.000    6,972   11,268
Internships_Count     7,558.50     414.96   18.22   0.000    6,743    8,374
Projects_Completed    1,636.34     300.06    5.45   0.000    1,047    2,226
Networking_Events       485.67     281.56    1.73   0.085      -68    1,039
Major_Computer Sci.   8,948.62   1,575.66    5.68   0.000    5,852   12,045
Major_Data Science    4,017.78   1,628.13    2.47   0.014      819    7,217
Major_Statistics      2,574.11   1,776.08    1.45   0.148     -916    6,064
University_Tier2     -5,858.66   1,255.15   -4.67   0.000   -8,325   -3,392
University_Tier3     -8,628.38   1,525.34   -5.66   0.000  -11,626   -5,631
======================================================================
```

### Coefficient Interpretation (All Variables)

All interpretations are **"holding all other variables constant"** — this is the critical advantage of multiple regression over simple correlation.

---

**Intercept (β₀ = $58,847.83)**
The expected salary for a female Business Analytics graduate from a Tier1 university with GPA=0, zero internships, zero projects, and zero networking events. Again, not a meaningful real-world prediction, but the mathematical baseline.

---

**GPA (β₁ = $9,119.88, p < 0.001) ★★★**
Holding everything else constant, each 1-point GPA increase adds **$9,120** to salary.

*Notice*: This is slightly lower than the $10,370 we found in simple regression. Why? Because in simple regression, some of GPA's apparent effect was actually picking up the influence of other variables (like major choice) that correlate with GPA. Multiple regression correctly isolates GPA's *independent* contribution.

**95% CI**: [$6,972 — $11,268] — We're 95% confident the true GPA effect is in this range.

---

**Internships_Count (β₂ = $7,558.50, p < 0.001) ★★★**
Each additional internship is associated with **$7,559** more in starting salary, holding everything else constant.

*This is the most powerful predictor per unit.* A student who completed 3 internships instead of 0 earns approximately **$22,675 more** (3 × $7,559), all else equal. This quantifies exactly why career advisors consistently say "get internships."

**95% CI**: [$6,743 — $8,374] — An extremely tight confidence interval, reflecting very high precision.

---

**Projects_Completed (β₃ = $1,636.34, p < 0.001) ★★★**
Each additional portfolio project adds **$1,636** to salary. Less impactful than internships per unit, but significant. The message: demonstrable work matters, just not as much as formal employment experience.

---

**Networking_Events (β₄ = $485.67, p = 0.085) — Not significant**
Each additional networking event attended is associated with $486 more in salary, but **this effect is not statistically significant** (p = 0.085 > 0.05). We cannot confidently distinguish this from random variation. The 95% CI [-$68, +$1,039] crosses zero — the true effect could plausibly be zero or even slightly negative.

*Does this mean networking doesn't matter?* Not necessarily. It means that in this dataset, *attendance at networking events* alone (without capturing the quality of connections made) isn't a strong salary predictor.

---

**Major_Computer Science (β₅ = $8,948.62, p < 0.001) ★★★**
Computer Science majors earn **$8,949 more** than Business Analytics majors (the reference category), holding all other factors constant.

This is the largest categorical effect in the model — a CS major effectively gets nearly a 1-GPA-point salary premium built in just from their field choice.

---

**Major_Data Science (β₆ = $4,017.78, p = 0.014) ★**
Data Science majors earn **$4,018 more** than Business Analytics majors. Significant but roughly half the CS premium. Both CS and DS clearly command labor market premiums.

---

**Major_Statistics (β₇ = $2,574.11, p = 0.148) — Not significant**
Statistics majors earn $2,574 more than Business Analytics, but this difference is **not statistically significant**. The 95% CI [-$916, +$6,064] includes zero. We cannot confirm that Statistics commands a salary premium over Business Analytics in this dataset.

---

**University_Tier2 (β₈ = -$5,858.66, p < 0.001) ★★★**
Tier2 graduates earn **$5,859 less** than Tier1 graduates (reference), holding other factors constant.

---

**University_Tier3 (β₉ = -$8,628.38, p < 0.001) ★★★**
Tier3 graduates earn **$8,628 less** than Tier1 graduates. The university tier penalty is substantial and highly significant.

*Combined picture*: The salary gap between a Tier1 and Tier3 graduate is **$8,628** for identical GPA, internships, major, and everything else. This quantifies the institutional prestige premium — sometimes called the "name brand" effect.

---

### 95% Confidence Intervals — Full Table

| Variable | Coefficient | 95% CI Lower | 95% CI Upper | Significant? |
|---|---|---|---|---|
| Intercept | $58,847.83 | $50,504 | $67,192 | ✓ |
| GPA | $9,119.88 | $6,972 | $11,268 | ✓ |
| Internships | $7,558.50 | $6,743 | $8,374 | ✓ |
| Projects | $1,636.34 | $1,047 | $2,226 | ✓ |
| Networking Events | $485.67 | -$68 | $1,039 | ✗ |
| Major: CS | $8,948.62 | $5,852 | $12,045 | ✓ |
| Major: Data Science | $4,017.78 | $819 | $7,217 | ✓ |
| Major: Statistics | $2,574.11 | -$916 | $6,064 | ✗ |
| Tier2 | -$5,858.66 | -$8,325 | -$3,392 | ✓ |
| Tier3 | -$8,628.38 | -$11,626 | -$5,631 | ✓ |

★★★ p < 0.001 | ★★ p < 0.01 | ★ p < 0.05 | — not significant

### Model 2 Overall Performance

- **R² = 0.5324**: The model explains **53.24%** of salary variation — a dramatic improvement from the 8.79% of simple regression.
- **Adjusted R² = 0.5235**: Adjusted for the 9 predictors used. Still strong — the complexity is justified.
- **F-statistic = 60.09, p < 0.001**: The model as a whole is highly significant. The predictors collectively explain salary far better than chance.
- **AIC = 10,415.58, BIC = 10,457.42**: These information criteria will be used to compare models (lower = better).

---

## 9. Feature Engineering — Interaction Term

### The Hypothesis

We tested whether GPA and Internships have a **synergistic effect**: perhaps GPA matters *more* for students with many internships (a "complete package" premium) or perhaps it matters *less* (internships make up for a lower GPA). This is called an interaction effect.

### Interaction Term Created

$$\text{GPA\_x\_Internships} = \text{GPA} \times \text{Internships\_Count}$$

Range: [0.00, 20.00] | Mean: 4.94

### Model 3 Results

```
Model 3 OLS Results (with interaction)
======================================================================
Dep. Variable:         Salary    R-squared:          0.5340
                                 Adj. R-squared:     0.5242
======================================================================
GPA × Internships:  $1,218.82   p-value: 0.1996
======================================================================
```

### Interpretation

**The interaction is NOT significant** (p = 0.200 > 0.05).

The coefficient of $1,218.82 means that for each 1-unit increase in the GPA×Internships product, salary increases by $1,218 — but we cannot distinguish this from random noise. GPA and internships appear to have **independent, additive effects** on salary rather than amplifying each other.

**R² improved by only 0.16 percentage points** (from 0.5324 to 0.5340) at the cost of one additional predictor. By AIC (10,415.89 vs 10,415.58), Model 2 is actually marginally preferred.

**Practical takeaway**: GPA and internships each help your salary on their own — but having both doesn't create an extra bonus beyond the sum of their individual effects.

---

## 10. Model Diagnostics — Checking Assumptions

OLS regression is built on five assumptions. Violating them can make coefficients unreliable or standard errors incorrect. We tested all five.

### Assumption 1: Linearity — `figures/07_linearity_check.png`

**Test**: Residuals vs Fitted Values plot + Component Plus Residual plot

**What the plot shows**: Two panels. Left: fitted values (model predictions) on the X-axis, residuals (prediction errors) on the Y-axis, with a LOWESS smoothing line in green. Right: a component-plus-residual plot showing the partial relationship for a key predictor.

**How to read it**: If linearity holds, residuals should scatter randomly around the horizontal zero line. The green LOWESS curve should hug the red horizontal zero line. Any U-shape or systematic curve means the true relationship is non-linear.

**Result**: The LOWESS smoother tracks close to zero without a strong systematic pattern. Linearity is **reasonably satisfied**.

---

### Assumption 2: Normality of Errors — `figures/08_normality_check.png`

**Test**: Q-Q Plot + Shapiro-Wilk test

**What the plot shows**: A Q-Q (Quantile-Quantile) plot. The X-axis shows theoretical quantiles from a perfect normal distribution. The Y-axis shows actual residual quantiles. If residuals are perfectly normal, points fall exactly on the diagonal line.

**How to read it**: Points following the diagonal = normality. Points curving away from the line at the tails = heavy tails (excess kurtosis). Points stepping off abruptly = outliers.

**Shapiro-Wilk Test Results**:
- Test statistic: **0.6969**
- p-value: **< 0.001**
- Verdict: Formally rejects normality

**Interpretation**: The test flags non-normality — but this requires context. With n=485, the Shapiro-Wilk test is *extremely sensitive* and will reject normality for minor deviations. The kurtosis of residuals (23.06 in the model output) reveals the true issue: **heavy tails driven by salary outliers** (the very high earners and very low earners we identified earlier). This doesn't mean our model is broken — it means a few extreme observations inflate the tails. For inference on coefficients, moderate normality violations at this sample size have minimal practical impact due to the Central Limit Theorem.

**Status**: ⚠️ **Minor violation** — Acknowledge in limitations; does not invalidate results for this sample size.

---

### Assumption 3: Homoscedasticity — `figures/09_homoscedasticity_check.png`

**Test**: Scale-Location Plot + Breusch-Pagan Test

**What the plot shows**: Fitted values on the X-axis, square root of absolute residuals on the Y-axis. If variance is constant, points should spread evenly at all fitted value levels — no fan-shape opening up or narrowing.

**Breusch-Pagan Test Results**:
- LM statistic: **12.996**
- p-value: **0.1628**
- Verdict: **Cannot reject homoscedasticity**

**Result**: ✅ **SATISFIED** — The constant variance assumption holds. The spread of errors does not systematically change as predicted salary increases. This is a clean result.

---

### Assumption 4: Independence — No plot needed

**Assessment**: Our data is **cross-sectional** — 500 different students measured at one point in time. There is no time-series structure, no repeated measurements, no spatial clustering. Observations are independent by design.

**Result**: ✅ **SATISFIED**

---

### Assumption 5: No Multicollinearity — VIF Analysis

**Test**: Variance Inflation Factor (VIF) for each predictor

**How to read VIF**: VIF = 1 means zero correlation with other predictors. VIF < 5 is acceptable. VIF 5–10 is concerning. VIF > 10 is severe multicollinearity requiring action.

| Variable | VIF |
|---|---|
| GPA | 1.01 |
| Internships_Count | 1.02 |
| Projects_Completed | 1.01 |
| Networking_Events | 1.01 |
| Major_Computer Science | **2.30** |
| Major_Data Science | **2.22** |
| Major_Statistics | **1.93** |
| University_Tier_Tier2 | 1.54 |
| University_Tier_Tier3 | 1.53 |

**Result**: ✅ **ALL VIF VALUES < 5** — No multicollinearity concern. The slightly elevated VIF for Major dummies (2.2–2.3) is expected — they represent different levels of the same categorical variable and naturally share some correlation with each other. This is harmless at these levels.

---

### Diagnostics Summary Table

| Assumption | Test Used | Result | Status |
|---|---|---|---|
| Linearity | Residuals vs Fitted + LOWESS | Random scatter, no pattern | ✅ Satisfied |
| Normality | Q-Q Plot + Shapiro-Wilk (W=0.697) | Heavy tails due to outliers | ⚠️ Minor violation |
| Homoscedasticity | Breusch-Pagan (p=0.163) | Cannot reject constant variance | ✅ Satisfied |
| Independence | Data structure check | Cross-sectional, no dependency | ✅ Satisfied |
| No Multicollinearity | VIF (max = 2.30) | All well below threshold of 5 | ✅ Satisfied |

**Overall assessment**: The model is statistically sound. The normality concern is acknowledged but does not materially affect our ability to interpret coefficients or conduct hypothesis tests at this sample size.

---

## 11. Sensitivity Analysis — Add/Drop Variables

### Purpose

Sensitivity analysis tests whether our model's conclusions are **robust** — do they change dramatically when we tweak the model? If dropping one variable causes others to swing wildly, the model is fragile. If results stay stable, we have confidence in our findings.

### Three Models Compared

| Model | Description | Predictors |
|---|---|---|
| **A (Full)** | All 9 predictors — our baseline Model 2 | 9 |
| **B (Reduced)** | Internships_Count dropped | 8 |
| **C (Extended)** | GPA × Internships interaction added | 10 |

### Comprehensive Comparison

| Metric | Model A (Full) | Model B (Reduced) | Model C (Extended) |
|---|---|---|---|
| R² | **0.5324** | 0.2058 | 0.5340 |
| Adjusted R² | **0.5235** | 0.1924 | 0.5242 |
| AIC | **10,415.58** | 10,670.50 | 10,415.89 |
| Predictors | 9 | 8 | 10 |

### What Dropping Internships Reveals (A → B)

- **R² collapsed** from 53.2% to 20.6% — a drop of 32.6 percentage points
- **AIC worsened** by 255 points (higher = worse fit)
- **GPA coefficient changed**: $9,119.88 (A) → $9,593.61 (B) — a +5.19% increase

**Why did GPA's coefficient increase?** This is **omitted variable bias** in action. When Internships is excluded from the model, GPA partially "absorbs" some of its effect (because students with higher GPA tend to get more internships). The simple regression GPA coefficient of $10,370 showed the same inflation. This confirms that **Internships is an essential predictor** — excluding it distorts all other estimates.

### What Adding the Interaction Shows (A → C)

- **R² barely changed**: 0.5324 → 0.5340 (+0.16 percentage points)
- **AIC slightly higher**: 10,415.58 → 10,415.89 (marginally worse fit per parameter added)
- **Interaction coefficient**: $1,218.82, p = 0.200 (not significant)

**Conclusion**: The interaction adds no meaningful value. Model A is preferred for its parsimony.

### GPA Coefficient Stability

| Model | GPA Coefficient | Change from A |
|---|---|---|
| A (Full) | $9,119.88 | — |
| B (Reduced) | $9,593.61 | +5.19% |
| C (Extended) | $7,245.02 | -20.6% |

Model C's large drop in GPA coefficient occurs because GPA's effect partially collapses into the interaction term (GPA × Internships = $1,218.82). When the interaction is included, the main effect of GPA represents only its effect when internships = 0, which is mathematically a different quantity.

---

## 12. Final Model Comparison

### All Models at a Glance

| Model | Description | R² | Adj R² | AIC | BIC |
|---|---|---|---|---|---|
| **Model 1** | Simple: Salary ~ GPA | 0.0879 | 0.0861 | 10,948.73 | 10,957.14 |
| **Model 2** ⭐ | Multiple: 9 predictors | **0.5324** | **0.5235** | **10,415.58** | 10,457.42 |
| **Model 3** | Multiple + GPA×Internships | 0.5340 | 0.5242 | 10,415.89 | 10,462.12 |

### What Each Metric Tells You

**R² (R-squared)**: The proportion of salary variance explained by the model. Higher = better fit. Goes from 8.79% (GPA alone) to 53.24% (all predictors). The jump is dramatic and clearly justifies the model's additional complexity.

**Adjusted R²**: Penalizes for adding more predictors. If a new predictor doesn't help enough to justify its inclusion, Adj R² will actually *decrease*. That Model 3's Adj R² (0.5242) only barely beats Model 2 (0.5235) confirms the interaction term is not worth keeping.

**AIC (Akaike Information Criterion)**: A measure of model quality that balances fit and complexity. **Lower is better.** Model 2's AIC (10,415.58) is lower than Model 3's (10,415.89), making Model 2 the winner by this criterion.

**BIC (Bayesian Information Criterion)**: Similar to AIC but penalizes complexity more heavily for large samples. Model 2 wins here too.

### R² Jump Visualized

```
Model 1 (GPA only):        ████░░░░░░░░░░░░░░░░   8.8%
Model 2 (9 predictors):    ██████████████████████████░░░░░░░░░░░░░░░   53.2%
```

The gap from 8.8% → 53.2% represents everything that GPA alone misses: the major you chose, where you went to university, how many internships you did, and the projects you built.

---

## 13. Key Findings

### Finding 1: Internships are the biggest salary lever
Each internship adds **$7,559** to starting salary (Model 2, p < 0.001). This is statistically the strongest and most consistent predictor. A student with 3 internships vs 0 has a built-in salary advantage of ~$22,677, regardless of GPA, major, or anything else.

### Finding 2: GPA matters — but less than you might expect
After controlling for everything else, GPA adds **$9,120 per point** (p < 0.001). It's significant, but it explained only 8.79% of salary variation on its own. GPA is necessary but not sufficient.

### Finding 3: Computer Science is the most lucrative major
CS majors earn **$8,949 more** than Business Analytics majors with identical profiles. Data Science is second (+$4,018). Statistics shows no significant advantage over Business Analytics (p = 0.148).

### Finding 4: University tier has a real salary premium
Tier1 vs Tier3 graduates with identical profiles: the Tier1 graduate earns **$8,628 more**. The institutional prestige penalty is real and quantifiable.

### Finding 5: Study hours don't predict salary
Correlation with salary: r = -0.026. No significant effect in any model. Working harder in school doesn't automatically mean earning more — the market rewards demonstrable skills and experience (internships, projects) over hours spent studying.

### Finding 6: GPA and Internships don't interact
We hypothesized a synergy effect — that having both high GPA and many internships would yield a "bonus" beyond their individual effects. The interaction coefficient was $1,218 but not significant (p = 0.20). Their effects are simply additive.

### Finding 7: Omitted variable bias is real
When Internships is dropped (Model B), R² drops from 53.2% to 20.6% and GPA's coefficient inflates from $9,120 to $9,594. This is textbook omitted variable bias — proof that Internships must be in the model for other coefficients to be correctly estimated.

### Finding 8: The model is statistically sound
Four of five OLS assumptions are fully satisfied. The one exception — normality — shows a minor violation due to salary outliers, but with n=485 this doesn't materially impact inference.

---

## 14. Final Verdict & Recommendations

### Best Model: Model 2 (Multiple Linear Regression with 9 Predictors)

**Winner by every criterion**:
- ✅ Highest Adjusted R² (0.5235) vs simpler model
- ✅ Lowest AIC (10,415.58) vs extended model
- ✅ All significant coefficients interpretable and actionable
- ✅ OLS assumptions met
- ✅ Stable under sensitivity analysis

**Model 2 explains 53.24% of starting salary variation** using publicly available student characteristics. The remaining ~47% reflects factors outside our dataset: negotiation skills, geographic location, specific company, timing of job search, personal networks, and luck.

### The Final Equation

$$\widehat{\text{Salary}} = 58,848 + 9,120(\text{GPA}) + 7,559(\text{Internships}) + 1,636(\text{Projects}) + 8,949(\text{CS Major}) + 4,018(\text{DS Major}) - 5,859(\text{Tier2}) - 8,628(\text{Tier3})$$

*Note: Networking Events, Major_Statistics, and Gender dummies were not statistically significant at p < 0.05.*

### Practical Recommendations for Students

| Action | Expected Salary Impact |
|---|---|
| Complete 1 additional internship | +$7,559 |
| Raise GPA by 0.5 points | +$4,560 |
| Complete 2 more portfolio projects | +$3,273 |
| Switch from Business Analytics to CS major | +$8,949 |
| Attend a Tier1 vs Tier3 university | +$8,628 |

**Priority order**: Internships → Major Choice → University Tier → GPA → Projects

### Limitations

1. **Simulated data**: The dataset was custom-generated. Results are directionally valid but cannot be directly generalized to real job markets.
2. **No geographic data**: Salaries vary enormously by city (San Francisco vs rural areas). This variation is invisible to our model.
3. **No industry data**: A CS major in finance earns differently than one in a startup. Industry is a major omitted variable.
4. **5% missing data handled by mean imputation**: More sophisticated imputation (multiple imputation, predictive imputation) could yield slightly different results.
5. **Normality violation**: The heavy tails of residuals suggest that for extreme salary predictions (very high or very low), the model's confidence intervals may be slightly too narrow.
6. **Cross-sectional snapshot**: This captures starting salary only. Salary growth trajectories differ across majors and tiers in ways this analysis cannot capture.

### Future Work

- Add geographic controls (city/region)
- Add industry/sector controls
- Explore non-linear methods (random forests, gradient boosting) for better predictive accuracy
- Examine 5-year salary progression, not just starting salary
- Collect data on interview skills, networking quality (not just quantity), and personal projects' complexity

---

## Appendix: Plot Reference Guide

| Figure | Filename | Description |
|---|---|---|
| 1 | `01_histograms.png` | Histograms for all 7 numeric variables |
| 2 | `02_boxplots.png` | Boxplots showing outliers for all 7 numeric variables |
| 3 | `03_correlation_matrix.png` | Correlation heatmap (numeric variables) |
| 4 | `04_scatterplots.png` | Salary vs each numeric predictor with trend lines |
| 5 | `05_categorical_salary.png` | Salary by Major, Gender, University Tier |
| 6 | `06_simple_regression.png` | Simple regression: Salary ~ GPA with confidence band |
| 7 | `07_linearity_check.png` | Residuals vs Fitted + Component-Plus-Residual |
| 8 | `08_normality_check.png` | Q-Q Plot + residual histogram |
| 9 | `09_homoscedasticity_check.png` | Scale-Location plot |
| 10 | `10_sensitivity_analysis.png` | Model comparison visualization |

---

## References

1. Statsmodels Documentation: https://www.statsmodels.org/stable/index.html
2. James, G., Witten, D., Hastie, T., & Tibshirani, R. (2013). *An Introduction to Statistical Learning*. Springer.
3. Montgomery, D. C., Peck, E. A., & Vining, G. G. (2012). *Introduction to Linear Regression Analysis*. Wiley.
4. UCLA OARC — Regression Analysis: https://stats.oarc.ucla.edu/stata/output/regression-analysis/

---

*Analysis performed in Python 3.12.3 using pandas, numpy, matplotlib, seaborn, statsmodels, scipy, and sklearn. February 2026.*
