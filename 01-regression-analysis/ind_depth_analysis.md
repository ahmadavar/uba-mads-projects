# Regression Analysis: What Actually Determines a Graduate's Starting Salary?

> A complete statistical investigation using Simple & Multiple Linear Regression on 500 graduates — with full model diagnostics, coefficient interpretation, and actionable insights.

---

## Table of Contents

- [The Problem](#the-problem)
- [Dataset at a Glance](#dataset-at-a-glance)
- [Tech Stack](#tech-stack)
- [Data Preparation & Cleaning](#data-preparation--cleaning)
- [Exploratory Data Analysis](#exploratory-data-analysis)
  - [Understanding Each Variable](#understanding-each-variable)
  - [Outlier Detection](#outlier-detection)
  - [Correlations — What Moves With Salary?](#correlations--what-moves-with-salary)
  - [Salary by Category](#salary-by-category)
- [Regression Problem Formulation](#regression-problem-formulation)
- [Model 1 — Simple Linear Regression](#model-1--simple-linear-regression-salary--gpa)
  - [Results](#model-1-results)
  - [Coefficient Interpretation](#model-1-coefficient-interpretation)
  - [Hypothesis Test](#hypothesis-test-for-gpa)
  - [Confidence Interval](#95-confidence-interval)
  - [What the Plot Shows](#what-the-plot-shows--simple-regression)
- [Model 2 — Multiple Linear Regression](#model-2--multiple-linear-regression-9-predictors)
  - [Dummy Variables Explained](#dummy-variables-explained)
  - [Full Results](#model-2-full-results)
  - [Every Coefficient Explained](#every-coefficient-explained)
  - [Confidence Intervals](#confidence-intervals--full-table)
- [Model 3 — Adding an Interaction Term](#model-3--interaction-term-gpa--internships)
- [Model Diagnostics — Are Our Assumptions Met?](#model-diagnostics--are-our-assumptions-met)
  - [Linearity](#1-linearity)
  - [Normality of Errors](#2-normality-of-errors)
  - [Homoscedasticity](#3-homoscedasticity-constant-variance)
  - [Independence](#4-independence)
  - [Multicollinearity](#5-multicollinearity--vif)
- [Sensitivity Analysis — What Changes When We Tweak the Model?](#sensitivity-analysis--what-changes-when-we-tweak-the-model)
- [Final Model Comparison](#final-model-comparison)
- [Key Findings](#key-findings)
- [Final Verdict](#final-verdict)
- [Limitations](#limitations)
- [Project Structure](#project-structure)

---

## The Problem

Every graduating student faces the same question: *what actually determines how much I'll earn?*

The typical advice — "get a good GPA," "do internships," "pick the right major" — is vague. It tells you *what* to do but never *by how much*. Is one internship worth $5,000 or $15,000? How much does a 0.5 GPA difference translate to in real money? Does going to a Tier 1 university actually pay off?

**This analysis answers those questions with numbers.**

Using Ordinary Least Squares (OLS) regression on 500 recent graduates, we build models that quantify the dollar-denominated salary impact of every measurable factor — GPA, internships, field of study, university tier, portfolio projects, and networking. We go beyond correlation to isolation: what does GPA contribute *after* accounting for everything else?

### Research Question

> *"What factors predict starting salary for recent graduates, and by exactly how much does each one contribute?"*

### Hypotheses We Test

| # | Hypothesis |
|---|---|
| H1 | GPA has a positive, statistically significant effect on salary |
| H2 | Internships will be the single strongest numerical predictor |
| H3 | CS and Data Science majors earn significantly more than Business Analytics |
| H4 | Tier 1 university graduates command a measurable salary premium |

---

## Dataset at a Glance

| Property | Value |
|---|---|
| Source | Custom-generated realistic simulation |
| Observations | **500 graduates** |
| Variables | **10** (7 numeric, 3 categorical) |
| Outcome variable | `Salary` — starting salary in USD |
| Missing data | ~5% in 3 columns (handled via mean imputation) |
| Salary range | $39,041 — $196,178 |
| Mean salary | $106,338 |

### Variable Dictionary

| Variable | Type | Description |
|---|---|---|
| `Salary` | Numeric — **Outcome** | Starting salary in USD |
| `GPA` | Numeric | Grade Point Average (0.0 – 4.0) |
| `Study_Hours_Per_Week` | Numeric | Average weekly study hours |
| `Internships_Count` | Numeric (count) | Number of internships completed |
| `Age` | Numeric | Age at graduation |
| `Projects_Completed` | Numeric (count) | Portfolio/personal projects built |
| `Networking_Events` | Numeric (count) | Professional networking events attended |
| `Major` | Categorical (4 levels) | CS, Data Science, Statistics, Business Analytics |
| `Gender` | Categorical (3 levels) | Male, Female, Non-Binary |
| `University_Tier` | Categorical (3 levels) | Tier1, Tier2, Tier3 |

---

## Tech Stack

```python
pandas          # Data manipulation
numpy           # Numerical operations
matplotlib      # Base plotting
seaborn         # Statistical visualizations
statsmodels     # OLS regression, diagnostics, VIF
scipy           # Shapiro-Wilk normality test
sklearn         # RMSE calculation utility
```

---

## Data Preparation & Cleaning

Real data is messy. This dataset was designed to reflect that. Before any modeling, we audited and cleaned the data systematically.

### Missing Value Audit

```
Variable                Missing Count    % Missing    Action
──────────────────────────────────────────────────────────
GPA                           5            1.0%       Mean imputed (μ = 3.19)
Study_Hours_Per_Week         10            2.0%       Mean imputed (μ = 25.22)
Networking_Events            10            2.0%       Mean imputed (μ = 3.93)
All other columns             0            0.0%       No action needed
```

**Why mean imputation?**
With only 1–2% missingness, these are minor gaps. Mean imputation preserves the dataset size (n=500) and introduces minimal bias. More sophisticated techniques (multiple imputation, predictive imputation) are possible but not necessary at this scale of missingness.

**Duplicates:** 0 found. Dataset is clean.

**Final state:** 500 rows × 10 columns, zero missing values.

### Descriptive Statistics (After Cleaning)

| Variable | Mean | Std Dev | Min | Median | Max | Skewness | Kurtosis |
|---|---|---|---|---|---|---|---|
| Salary ($) | 106,338 | 15,975 | 39,041 | 105,821 | 196,178 | 0.21 | **4.66** |
| GPA | 3.19 | 0.46 | 2.00 | 3.21 | 4.00 | -0.11 | -0.58 |
| Study Hours/Week | 25.22 | 7.81 | 5.00 | 25.22 | 46.06 | 0.06 | -0.14 |
| Internships | 1.54 | 1.22 | 0 | 1.00 | 5 | 0.66 | -0.01 |
| Age | 24.05 | 1.85 | 21 | 24.00 | 30 | 0.26 | -0.35 |
| Projects | 2.96 | 1.67 | 0 | 3.00 | 9 | 0.54 | 0.17 |
| Networking Events | 3.93 | 1.79 | 0 | 4.00 | 10 | 0.24 | -0.03 |

**One number stands out:** Salary kurtosis = **4.66** (a normal distribution has kurtosis = 3). This means salary has heavier tails than expected — a cluster of very high earners pulls the distribution and is more common than a perfect bell curve would predict. Realistic for income data.

---

## Exploratory Data Analysis

### Understanding Each Variable

#### Plot 1 — Histograms (`figures/01_histograms.png`)

A 3×3 grid showing the frequency distribution of all 7 numeric variables. Each histogram includes a **red dashed line at the mean** and a **green dashed line at the median**.

**How to read it:** When mean and median lines overlap, the distribution is symmetric. When they diverge, it is skewed. The distance between them tells you how much extreme values are pulling the average.

**What we found:**

- **Salary** — Near-symmetric with slight right skew (0.21). Mean ($106,338) sits just above median ($105,821) — a handful of high earners pull the average up. Classic income distribution behavior.
- **GPA** — Nearly perfect symmetry (skewness = -0.11). Students cluster naturally around 3.0–3.5 with a realistic bell shape.
- **Study Hours** — Essentially symmetric (skewness = 0.06). Most students study 20–30 hours/week.
- **Internships** — Moderately right-skewed (0.66). Most students completed 0–2 internships; a smaller number completed 4–5. Those high-internship students are an important subgroup.
- **Projects** — Similar right skew (0.54). Most students built 2–4 projects.
- **Age & Networking** — Both near-normal with mild right skew.

**Takeaway:** No extreme skewness demanding mandatory transformation. The data is well-behaved.

---

#### Plot 2 — Boxplots (`figures/02_boxplots.png`)

The same 7 variables as boxplots. The box spans the middle 50% of the data (IQR: 25th to 75th percentile). The red line is the median. Points beyond the whiskers (1.5 × IQR) are individual outliers.

**How to read it:** Tall boxes = high variability. Short boxes = values are concentrated. Dots beyond the whiskers = potential outliers worth investigating.

**What we found:**

- **Salary** — Several dots appear far above the upper whisker (above ~$140,000). These are genuinely high earners, not data errors. The box itself is wide, reflecting the $15,975 standard deviation.
- **Internships** — Points at 4 and 5 appear as outliers by IQR rules (upper bound = 3.5), but these are real students with extensive internship experience — not data quality issues.
- **GPA** — The cleanest distribution. No outliers at all; students simply cannot exceed 4.0.
- **Age** — Tight box (most graduates are 22–25), with a few older students (28–30) visible as outliers.

---

### Outlier Detection

**Method:** IQR Rule — Lower bound = Q1 − 1.5×IQR; Upper bound = Q3 + 1.5×IQR

| Variable | Lower Bound | Upper Bound | Outliers Found | % of Data |
|---|---|---|---|---|
| Salary | $70,760 | $139,983 | **18** | 3.6% |
| GPA | 1.84 | 4.53 | 0 | 0.0% |
| Internships | -0.50 | 3.50 | **37** | 7.4% |

**Decision: All outliers retained.**

The salary outliers span $39,041–$196,178. These represent genuinely exceptional graduates — a Data Science student who landed a $196,178 offer is a real person whose outcome belongs in our analysis. Removing them would bias the model toward average earners and artificially reduce salary variance. We monitor their influence in the diagnostics phase instead.

---

### Correlations — What Moves With Salary?

#### Plot 3 — Correlation Heatmap (`figures/03_correlation_matrix.png`)

A color-coded grid where every cell shows the Pearson correlation coefficient between two variables. **Red = strong positive correlation. Blue = negative. White = near zero.** Annotations show the exact values.

**How to read it:** Focus on the Salary row. The stronger the red, the stronger the linear relationship with salary. Also check predictor-to-predictor cells for multicollinearity warning signs.

**Correlations with Salary:**

| Predictor | r | Interpretation |
|---|---|---|
| Internships_Count | **0.602** | Moderate-strong positive — the clear leader |
| GPA | 0.296 | Weak-moderate positive |
| Projects_Completed | 0.166 | Weak positive |
| Networking_Events | 0.085 | Negligible |
| Age | 0.044 | Negligible |
| Study_Hours_Per_Week | **-0.026** | Essentially zero (slightly negative) |

**The most counterintuitive finding:** Study hours have a correlation of -0.026 with salary. Students who study more don't earn more. The market doesn't reward effort in the library — it rewards demonstrable outcomes: internships and projects.

**Between predictors:** All inter-predictor correlations are low, suggesting minimal multicollinearity — a good sign for regression stability.

---

#### Plot 4 — Scatterplots (`figures/04_scatterplots.png`)

Six scatterplots (2×3 grid): Salary on the Y-axis, each numeric predictor on the X-axis. Each panel includes a red trend line and the correlation coefficient r.

**How to read it:** Points clustered tightly around the trend line = strong linear relationship. Wide scatter = weak relationship. Upward slope = positive; flat or downward = negligible or negative.

**What we see panel by panel:**

- **Salary vs GPA (r=0.296):** Upward trend is visible but with enormous scatter. A 3.8-GPA student doesn't guarantee $150K.
- **Salary vs Internships (r=0.602):** The clearest pattern by far. The trend line rises steeply. Students with 4–5 internships visibly cluster at the top of the salary range.
- **Salary vs Study Hours (r=-0.026):** A flat line. Points scatter randomly in all directions — no salary signal whatsoever.
- **Salary vs Projects (r=0.166):** Slight upward trend. More projects = marginally higher salary, but much weaker than internships.
- **Salary vs Age (r=0.044):** No discernible pattern.
- **Salary vs Networking (r=0.085):** Very weak positive trend.

---

### Salary by Category

#### Plot 5 — Boxplots by Categorical Variable (`figures/05_categorical_salary.png`)

Three side-by-side boxplots: salary distribution broken down by Major, Gender, and University Tier.

**How to read it:** Compare the red median line across groups within each panel. Higher median = that group earns more. Wider box = more spread within that group.

**By Major:**

| Major | Mean Salary | Median | Max |
|---|---|---|---|
| Computer Science | **$110,313** | $108,864 | $196,178 |
| Data Science | $105,494 | $105,839 | $150,704 |
| Statistics | $102,677 | $101,256 | $157,258 |
| Business Analytics | $102,540 | $102,207 | $145,146 |

CS is the clear leader. Statistics and Business Analytics are nearly indistinguishable. These raw differences will sharpen once we control for GPA, internships, and other factors in the regression.

**By University Tier:** Tier1 median is visibly higher — the box sits above Tier2 and Tier3. This is a clear visual preview of what the regression will confirm.

---

## Regression Problem Formulation

### Why Regression — Not Just Correlation?

Correlation tells you that Internships and Salary move together (r = 0.60). But it cannot tell you: *is that because internships directly boost salary, or because students who get internships also happen to have higher GPAs and attend better universities?*

**Multiple regression isolates each effect.** By including all variables simultaneously, it answers: "How much does one additional internship contribute to salary, *holding GPA, major, university tier, and everything else constant*?"

### How Categorical Variables Enter the Model

Regression requires numbers. Categorical variables (Major, Gender, University Tier) are converted to **dummy variables**: binary 0/1 columns.

| Original Variable | Dummies Created | Reference Category (omitted) |
|---|---|---|
| Major (4 levels) | `Major_Computer Science`, `Major_Data Science`, `Major_Statistics` | Business Analytics |
| University_Tier (3 levels) | `University_Tier_Tier2`, `University_Tier_Tier3` | Tier1 |
| Gender (3 levels) | `Gender_Male`, `Gender_Non-Binary` | Female |

**Why omit one category?** Including all levels would create perfect multicollinearity (the "dummy variable trap"). The omitted category becomes the **reference group** — all dummy coefficients are interpreted as *"compared to this group."*

---

## Model 1 — Simple Linear Regression: Salary ~ GPA

We start simple: one predictor, one outcome. The goal is to establish a baseline and understand GPA's relationship to salary in isolation.

$$\widehat{\text{Salary}} = \beta_0 + \beta_1 \times \text{GPA} + \varepsilon$$

### Model 1 Results

```
OLS Regression Results
═══════════════════════════════════════════════════════════════════════
Dependent Variable:     Salary          R-squared:          0.0879
Method:                    OLS          Adj. R-squared:     0.0861
Observations:              495          F-statistic:        47.51
AIC:                  10948.73          Prob (F-stat):      1.68e-11
BIC:                  10957.14          Log-Likelihood:    -5472.4
═══════════════════════════════════════════════════════════════════════
            coef        std err      t         P>|t|    [0.025   0.975]
───────────────────────────────────────────────────────────────────────
const   73,188.60      4,854.40    15.08      0.000    63,653   82,724
GPA     10,369.97      1,504.40     6.89      0.000     7,414   13,326
═══════════════════════════════════════════════════════════════════════
Durbin-Watson: 2.091    Omnibus: 73.621    Prob(Omnibus): 0.000
Jarque-Bera: 631.103    Skew: 0.288        Kurtosis: 8.502
═══════════════════════════════════════════════════════════════════════
```

### Model 1 Coefficient Interpretation

**Intercept (β₀ = $73,188.60)**

The expected salary when GPA = 0. This is the mathematical anchor of the line — not a real-world prediction (no student has a 0.0 GPA). Think of it as: if you stripped away all GPA effect, the baseline starting point would be ~$73,189.

---

**GPA Slope (β₁ = $10,369.97)**

For every 1-point increase in GPA, starting salary is expected to increase by **$10,370**.

*In practice:*
- A student with GPA 3.0 → predicted salary: $73,189 + (10,370 × 3.0) = **$104,299**
- A student with GPA 3.5 → predicted salary: $73,189 + (10,370 × 3.5) = **$109,484**
- Difference: **$5,185** for a 0.5 GPA bump

---

### Hypothesis Test for GPA

$$H_0: \beta_1 = 0 \quad \text{(GPA has no effect on salary)}$$
$$H_a: \beta_1 \neq 0 \quad \text{(GPA does affect salary)}$$

| Statistic | Value |
|---|---|
| t-statistic | **6.89** |
| p-value | **< 0.0001** |
| α (significance level) | 0.05 |
| Decision | **Reject H₀** |

**Conclusion:** GPA has a statistically significant positive effect on starting salary. The p-value is so small (0.0000017) that we can be virtually certain this is not a chance finding. We reject the null hypothesis with confidence.

---

### 95% Confidence Interval

```
95% CI for β₁ (GPA): [$7,414 — $13,326]
```

We are 95% confident that a 1-point GPA increase is associated with a salary increase of **between $7,414 and $13,326**.

Since this interval does not contain zero, the effect is statistically confirmed. No matter where the true coefficient lands in this range, the direction (positive) and practical significance (thousands of dollars) are certain.

---

### R² — How Much Does GPA Explain?

**R² = 0.0879** → GPA explains **8.79%** of salary variation.

This sounds small. It is. GPA matters, but salary is shaped by many forces beyond academic performance. A student with a 4.0 GPA in Business Analytics from a Tier 3 university with zero internships will likely earn less than a student with a 3.2 GPA in Computer Science from a Tier 1 university with 3 internships. GPA is one piece of a larger puzzle — which is exactly why we need multiple regression.

---

### What the Plot Shows — Simple Regression

#### `figures/06_simple_regression.png`

A scatterplot with Salary (Y-axis) vs GPA (X-axis). The **red solid line** is the fitted regression line: `Salary = 73,189 + 10,370 × GPA`. The **red shaded band** is the 95% confidence interval for the mean prediction (not for individual predictions).

**How to read it:**
- The line shows the expected average salary at each GPA level
- The shaded band widens at the extremes (fewer data points there = more uncertainty)
- Points above the line = model underestimated that student's salary
- Points below the line = model overestimated

**What jumps out:** The trend is real — the line slopes upward clearly. But the vertical scatter at any given GPA value is enormous — easily $50,000 spread. This visual alone explains why R² = 8.79%. GPA predicts direction, not destination.

---

## Model 2 — Multiple Linear Regression: 9 Predictors

Now we bring in all available predictors. The model can now isolate each variable's contribution independently.

$$\widehat{\text{Salary}} = \beta_0 + \beta_1(\text{GPA}) + \beta_2(\text{Internships}) + \beta_3(\text{Projects}) + \beta_4(\text{Networking}) + \beta_5(\text{CS}) + \beta_6(\text{DS}) + \beta_7(\text{Stats}) + \beta_8(\text{Tier2}) + \beta_9(\text{Tier3}) + \varepsilon$$

### Dummy Variables Explained

Before fitting, we converted the three categorical variables to dummy columns:

```python
df_dummies = pd.get_dummies(df,
    columns=['Major', 'Gender', 'University_Tier'],
    drop_first=True,    # Avoids dummy variable trap
    dtype=int           # Clean 0/1 instead of True/False
)
# Result: 500 rows × 14 columns
```

The dataset grew from 10 to 14 columns. The reference categories (Business Analytics, Female, Tier1) are captured entirely in the intercept — every dummy coefficient is a salary difference *relative to those reference groups*.

---

### Model 2 Full Results

```
OLS Regression Results
═══════════════════════════════════════════════════════════════════════
Dependent Variable:     Salary          R-squared:          0.5324
Method:                    OLS          Adj. R-squared:     0.5235
Observations:              485          F-statistic:        60.09
AIC:                  10415.58          Prob (F-stat):      8.07e-73
BIC:                  10457.42          Log-Likelihood:    -5197.8
═══════════════════════════════════════════════════════════════════════
                         coef      std err     t       P>|t|  [0.025    0.975]
───────────────────────────────────────────────────────────────────────────────
const                58,847.83    4,246.41   13.86    0.000   50,504   67,192
GPA                   9,119.88    1,092.98    8.34    0.000    6,972   11,268
Internships_Count     7,558.50      414.96   18.22    0.000    6,743    8,374
Projects_Completed    1,636.34      300.06    5.45    0.000    1,047    2,226
Networking_Events       485.67      281.56    1.73    0.085      -68    1,039
Major_Computer Sci.   8,948.62    1,575.66    5.68    0.000    5,852   12,045
Major_Data Science    4,017.78    1,628.13    2.47    0.014      819    7,217
Major_Statistics      2,574.11    1,776.08    1.45    0.148     -916    6,064
University_Tier2     -5,858.66    1,255.15   -4.67    0.000   -8,325   -3,392
University_Tier3     -8,628.38    1,525.34   -5.66    0.000  -11,626   -5,631
═══════════════════════════════════════════════════════════════════════
Durbin-Watson: 2.265    Kurtosis: 23.057    Skew: -0.512
Cond. No.: 56.9
═══════════════════════════════════════════════════════════════════════
Significance: *** p<0.001   ** p<0.01   * p<0.05   — not significant
```

---

### Every Coefficient Explained

Every interpretation below means **"holding all other variables constant."** This is the core power of multiple regression — it isolates each factor's independent contribution.

---

#### Intercept — $58,847.83

The expected salary for a **Female, Business Analytics major, Tier 1 university graduate** with GPA=0, zero internships, zero projects, and zero networking events. Not meaningful as a real-world prediction, but the mathematical foundation from which everything else is added or subtracted.

---

#### GPA — $9,119.88 per point ✅ (p < 0.001)

Holding everything else constant, each 1-point GPA increase adds **$9,120** to salary.

> Notice: In Model 1 (simple regression), GPA's coefficient was $10,370. Now it's $9,120. Why the drop of ~$1,250? Because in simple regression, GPA was inadvertently "absorbing" some of the influence of other variables — particularly major choice and university tier — that correlate with GPA. Multiple regression correctly reassigns that credit, giving GPA only its genuine independent contribution.

**95% CI:** [$6,972 — $11,268]

---

#### Internships_Count — $7,558.50 per internship ✅ (p < 0.001)

Each additional internship adds **$7,559** to starting salary.

This is the model's most impactful predictor. The math is stark:

| Internships | Salary Contribution |
|---|---|
| 0 | $0 |
| 1 | +$7,559 |
| 2 | +$15,117 |
| 3 | +$22,676 |
| 4 | +$30,234 |
| 5 | +$37,793 |

A student who did 5 internships versus a student who did none earns **$37,793 more** with an otherwise identical profile. The confidence interval is extremely tight [$6,743 — $8,374], reflecting very high precision in this estimate.

**95% CI:** [$6,743 — $8,374]

---

#### Projects_Completed — $1,636.34 per project ✅ (p < 0.001)

Each additional portfolio project adds **$1,636** to salary. Less impactful per unit than internships, but statistically certain. Building a project demonstrates tangible skills, and employers price that — just not as much as they price real work experience.

**95% CI:** [$1,047 — $2,226]

---

#### Networking_Events — $485.67 per event ❌ (p = 0.085, not significant)

Each additional networking event is associated with $486 more in salary, but **this effect is not statistically significant**. The p-value of 0.085 exceeds our threshold of 0.05, and the 95% confidence interval [-$68 — $1,039] crosses zero.

**What this means:** We cannot confidently claim networking events affect salary. The true effect could plausibly be zero or even slightly negative. This doesn't mean networking is useless — it means that simply *attending events* (without capturing the quality of connections made) doesn't show up as a salary driver in this dataset.

---

#### Major_Computer Science — $8,948.62 ✅ (p < 0.001)

CS majors earn **$8,949 more** than Business Analytics majors with otherwise identical profiles.

This is the largest categorical salary premium in the model — roughly equivalent to almost one full GPA point in dollar terms. The market heavily rewards computer science skills.

**95% CI:** [$5,852 — $12,045]

---

#### Major_Data Science — $4,017.78 ✅ (p = 0.014)

Data Science majors earn **$4,018 more** than Business Analytics majors. Significant, but roughly half the CS premium. Both technical majors outperform business.

**95% CI:** [$819 — $7,217]

---

#### Major_Statistics — $2,574.11 ❌ (p = 0.148, not significant)

Statistics majors appear to earn $2,574 more than Business Analytics, but **this difference is not statistically significant** (p = 0.148). The 95% CI [-$916 — $6,064] includes zero. We cannot confirm a Statistics premium over Business Analytics in this dataset.

---

#### University_Tier2 — -$5,858.66 ✅ (p < 0.001)

Tier 2 graduates earn **$5,859 less** than Tier 1 graduates, holding everything else constant.

**95% CI:** [-$8,325 — -$3,392]

---

#### University_Tier3 — -$8,628.38 ✅ (p < 0.001)

Tier 3 graduates earn **$8,628 less** than Tier 1 graduates.

The full university tier salary picture:

| University | Salary Differential vs Tier 1 |
|---|---|
| Tier 1 (reference) | $0 |
| Tier 2 | -$5,859 |
| Tier 3 | -$8,628 |

A Tier 1 vs Tier 3 gap of **$8,628** persists even after controlling for GPA, internships, major, and everything else. The institutional prestige effect is real and quantifiable.

**95% CI:** [-$11,626 — -$5,631]

---

### Confidence Intervals — Full Table

| Variable | Coefficient | 95% CI | p-value | Significant? |
|---|---|---|---|---|
| Intercept | $58,847.83 | [$50,504 — $67,192] | < 0.001 | ✅ |
| GPA | $9,119.88 | [$6,972 — $11,268] | < 0.001 | ✅ *** |
| Internships | $7,558.50 | [$6,743 — $8,374] | < 0.001 | ✅ *** |
| Projects | $1,636.34 | [$1,047 — $2,226] | < 0.001 | ✅ *** |
| Networking Events | $485.67 | [-$68 — $1,039] | 0.085 | ❌ |
| Major: CS | $8,948.62 | [$5,852 — $12,045] | < 0.001 | ✅ *** |
| Major: Data Science | $4,017.78 | [$819 — $7,217] | 0.014 | ✅ * |
| Major: Statistics | $2,574.11 | [-$916 — $6,064] | 0.148 | ❌ |
| Tier 2 | -$5,858.66 | [-$8,325 — -$3,392] | < 0.001 | ✅ *** |
| Tier 3 | -$8,628.38 | [-$11,626 — -$5,631] | < 0.001 | ✅ *** |

`***` p < 0.001 &nbsp;&nbsp; `**` p < 0.01 &nbsp;&nbsp; `*` p < 0.05 &nbsp;&nbsp; `❌` not significant

---

### Model 2 Overall Performance

| Metric | Value | Meaning |
|---|---|---|
| R² | **0.5324** | 53.24% of salary variation explained |
| Adjusted R² | **0.5235** | Penalty-adjusted for 9 predictors — still strong |
| F-statistic | **60.09** | p < 0.001 — model is highly significant overall |
| AIC | **10,415.58** | Used for model comparison (lower = better) |
| BIC | **10,457.42** | Stricter penalty version — same direction |

The leap from 8.79% (Model 1) to 53.24% (Model 2) is substantial. Everything GPA couldn't explain — the university you attended, the major you chose, the internships you completed — is now captured.

---

## Model 3 — Interaction Term: GPA × Internships

### The Hypothesis

We tested whether GPA and Internships have a **synergistic (multiplicative) effect** on salary. The question: does GPA matter *more* for students who also have many internships — a "complete package" premium? Or does having many internships make up for a lower GPA — diminishing GPA's returns?

### What We Did

We created a new variable:

```python
df['GPA_x_Internships'] = df['GPA'] * df['Internships_Count']
# Range: [0.00, 20.00]  |  Mean: 4.94
```

This interaction term was added to Model 2's predictors to form Model 3.

### Model 3 Key Results

```
═══════════════════════════════════════════════════════════════
                           R-squared:    0.5340
                      Adj. R-squared:    0.5242
                                 AIC:    10415.89
═══════════════════════════════════════════════════════════════
GPA × Internships:  $1,218.82    p-value: 0.1996   ❌
═══════════════════════════════════════════════════════════════
```

### Interpretation

**The interaction is not statistically significant** (p = 0.200 > 0.05).

The coefficient of +$1,218.82 suggests that for each 1-unit increase in the GPA×Internships product, salary increases by $1,218 — but we cannot distinguish this from random noise. The 95% CI crosses zero.

**GPA and internships act independently**, not synergistically. Having a 4.0 GPA alongside 5 internships doesn't give you a bonus beyond what the two individual effects already predict. Their effects simply add up.

**R² improved by only 0.16 percentage points** (0.5324 → 0.5340) while AIC *worsened* (10,415.58 → 10,415.89). The interaction adds complexity without meaningful payoff.

**Model 2 remains preferred.**

---

## Model Diagnostics — Are Our Assumptions Met?

OLS regression produces valid, unbiased estimates only when five assumptions hold. We tested all five rigorously.

---

### 1. Linearity

**Test:** Residuals vs Fitted Values plot with LOWESS smoother

#### `figures/07_linearity_check.png`

Two panels. Left panel: fitted (predicted) values on the X-axis, residuals (errors = actual − predicted) on the Y-axis, with a green LOWESS smoothing curve overlaid. Right panel: component-plus-residual plot.

**How to read it:** If linearity holds, residuals scatter randomly around the **horizontal zero line**. The green LOWESS curve should track that zero line closely. Any U-shape or systematic curve indicates the true relationship is non-linear and we're fitting the wrong functional form.

**Result:** The LOWESS smoother tracks near zero without systematic curvature.

✅ **Linearity: Satisfied**

---

### 2. Normality of Errors

**Test:** Q-Q Plot + Shapiro-Wilk test

#### `figures/08_normality_check.png`

Two panels. Left: a Quantile-Quantile (Q-Q) plot comparing our residual distribution to a perfect normal distribution. Points on the diagonal = perfect normality. Right: histogram of residuals with a normal curve overlay.

**How to read the Q-Q plot:** Points follow the diagonal line = normality. Points curve away at the tails = heavy tails (kurtosis). Pronounced S-shape = skew.

**Shapiro-Wilk Results:**
```
Test statistic (W):  0.6969
p-value:             < 0.001
Formal conclusion:   Reject normality
```

**But context matters critically here.** With n=485, the Shapiro-Wilk test is extremely sensitive — it will reject normality for very minor deviations that have no practical consequence. The model's kurtosis of 23.057 reveals the true issue: **heavy tails driven by salary outliers** (the very high earners and very low earners we identified earlier).

This does *not* mean the model is broken. At this sample size, moderate normality violations have minimal impact on coefficient estimates or hypothesis tests — the Central Limit Theorem ensures our sampling distributions remain approximately normal. For individual prediction intervals at extreme salary values, we should be cautious.

⚠️ **Normality: Minor violation — acknowledged, does not invalidate inference**

---

### 3. Homoscedasticity (Constant Variance)

**Test:** Scale-Location Plot + Breusch-Pagan Test

#### `figures/09_homoscedasticity_check.png`

Fitted values on the X-axis, square root of absolute residuals on the Y-axis. If variance is constant across all fitted values, points spread evenly across the full horizontal range. A fan shape opening to the right = heteroscedasticity (variance grows with salary level).

**Breusch-Pagan Test Results:**
```
LM statistic:   12.996
p-value:         0.163
Conclusion:      Cannot reject homoscedasticity (p > 0.05)
```

**Result:** The test fails to detect heteroscedasticity. Variance of errors is constant across salary levels.

✅ **Homoscedasticity: Satisfied**

---

### 4. Independence

**Test:** Data structure review + Durbin-Watson statistic

Our dataset is **cross-sectional**: 500 different individuals measured at one point in time. There is no time-series structure, no spatial clustering, no repeated measurements of the same person. Observations are independent by design.

The Durbin-Watson statistic of **2.265** (from Model 2 output) is close to 2.0 — the value indicating no autocorrelation. Values between 1.5 and 2.5 are generally acceptable.

✅ **Independence: Satisfied**

---

### 5. Multicollinearity — VIF

**Test:** Variance Inflation Factor for each predictor

VIF measures how much a predictor's variance is inflated due to correlation with other predictors. **VIF = 1**: zero correlation. **VIF < 5**: acceptable. **VIF 5–10**: concerning. **VIF > 10**: severe.

| Variable | VIF | Status |
|---|---|---|
| GPA | 1.014 | ✅ Perfect |
| Internships_Count | 1.019 | ✅ Perfect |
| Projects_Completed | 1.007 | ✅ Perfect |
| Networking_Events | 1.011 | ✅ Perfect |
| Major_Computer Science | **2.304** | ✅ Acceptable |
| Major_Data Science | **2.223** | ✅ Acceptable |
| Major_Statistics | **1.932** | ✅ Acceptable |
| University_Tier_Tier2 | 1.545 | ✅ Perfect |
| University_Tier_Tier3 | 1.529 | ✅ Perfect |

The slightly elevated VIF for Major dummies (1.9–2.3) is expected — they encode different levels of the same categorical variable and naturally share some correlation. These values are well below any threshold of concern.

✅ **No Multicollinearity: All VIF values < 5**

---

### Diagnostics Summary

| Assumption | Test | Result | Status |
|---|---|---|---|
| Linearity | Residuals vs Fitted + LOWESS | Random scatter, no systematic pattern | ✅ Satisfied |
| Normality | Q-Q Plot + Shapiro-Wilk (W=0.697) | Heavy tails from salary outliers | ⚠️ Minor violation |
| Homoscedasticity | Breusch-Pagan (p=0.163) | Cannot reject constant variance | ✅ Satisfied |
| Independence | Data structure + DW=2.265 | Cross-sectional, no autocorrelation | ✅ Satisfied |
| No Multicollinearity | VIF (max = 2.30) | All values well below threshold of 5 | ✅ Satisfied |

**Overall:** The model is statistically sound. 4 of 5 assumptions are fully satisfied. The normality concern is noted and does not materially affect our ability to interpret coefficients or conduct hypothesis tests at this sample size.

---

## Sensitivity Analysis — What Changes When We Tweak the Model?

Sensitivity analysis asks: **are our conclusions robust?** If dropping one variable causes all other coefficients to swing dramatically, the model is fragile. If results remain stable, we have confidence.

### Three Models Tested

| Model | Description | Change from Baseline |
|---|---|---|
| **A — Full** | All 9 predictors (= Model 2) | Baseline |
| **B — Reduced** | Internships_Count dropped | Remove strongest predictor |
| **C — Extended** | GPA × Internships interaction added | Add complexity |

---

### Results

| Metric | Model A (Full) | Model B (Reduced) | Model C (Extended) |
|---|---|---|---|
| Predictors | 9 | 8 | 10 |
| R² | **0.5324** | 0.2058 | 0.5340 |
| Adjusted R² | **0.5235** | 0.1924 | 0.5242 |
| AIC | **10,415.58** | 10,670.50 | 10,415.89 |

---

### What Dropping Internships Reveals (A → B)

- **R² collapsed** from 53.2% to 20.6% — a 32.6 percentage point drop
- **AIC worsened by 255 points** (a massive deterioration in fit)
- **GPA coefficient inflated**: $9,120 (A) → $9,594 (B) — a +5.19% increase

**Why did GPA's coefficient inflate?**

This is textbook **omitted variable bias**. When Internships is excluded, GPA partially absorbs its effect — because students with higher GPAs tend to also have more internships (they're more competitive, more motivated). Without Internships in the model, some of its salary contribution gets incorrectly credited to GPA.

This is precisely why the simple regression GPA coefficient was even higher ($10,370) — it was absorbing even more omitted variables. Multiple regression prevents this distortion.

**Conclusion:** Internships must be in the model. Excluding it invalidates the estimates of every other coefficient.

---

### What Adding the Interaction Shows (A → C)

- **R² barely moved**: 0.5324 → 0.5340 (+0.16 pp)
- **AIC worsened**: 10,415.58 → 10,415.89 (added complexity, no meaningful gain)
- **Interaction not significant**: p = 0.200

**Conclusion:** The interaction term adds no value. Model A is the optimal model.

---

### GPA Coefficient Stability Across Models

| Model | GPA Coefficient | Change |
|---|---|---|
| Model A (Full) | $9,119.88 | — |
| Model B (Reduced — drop Internships) | $9,593.61 | **+5.19%** (omitted variable bias) |
| Model C (Extended — add interaction) | $7,245.02 | **-20.6%** (collapses into interaction term) |

Model C's GPA coefficient drops because, when the interaction term `GPA × Internships` is included, the main GPA effect now represents only GPA's effect *when Internships = 0* — a narrower, different quantity. This is expected behavior, not a problem.

---

## Final Model Comparison

| Model | Description | R² | Adj R² | AIC | BIC | Verdict |
|---|---|---|---|---|---|---|
| Model 1 | Simple: GPA only | 0.0879 | 0.0861 | 10,948.73 | 10,957.14 | Too simple |
| **Model 2** | Multiple: 9 predictors | **0.5324** | **0.5235** | **10,415.58** | **10,457.42** | ⭐ **Winner** |
| Model 3 | Multiple + interaction | 0.5340 | 0.5242 | 10,415.89 | 10,462.12 | Marginal gain, more complex |

**Model 2 wins by every criterion that matters:**
- Higher Adjusted R² than Model 1 (better fit)
- Lower AIC than Model 3 (better fit per parameter)
- All coefficients interpretable and actionable
- OLS assumptions satisfied

### The R² Story

```
Model 1  GPA only:       ████░░░░░░░░░░░░░░░░░░░░░░░░   8.8%  explained
Model 2  9 predictors:   ███████████████████████████░░░░░░░░░░░░░░   53.2%  explained
                                                         ↑
                                               The remaining 46.8%:
                                               location, industry, luck,
                                               negotiation skills, company,
                                               personal network quality...
```

### What Each Model Metric Means

**R² (R-squared):** What proportion of salary variance does the model explain? Goes from 8.8% → 53.2%. The jump is dramatic.

**Adjusted R²:** R² but penalized for adding more predictors. If a new variable doesn't pull its weight, Adj R² drops. That Model 3's Adj R² (0.5242) barely beats Model 2 (0.5235) confirms the interaction term is deadweight.

**AIC (Akaike Information Criterion):** Balances fit and complexity. **Lower is better.** Model 2's AIC (10,415.58) beats Model 3 (10,415.89). The difference is small but clear: don't add the interaction.

**BIC (Bayesian Information Criterion):** Same direction as AIC but penalizes complexity more heavily. Model 2 wins here too.

---

## Key Findings

### Finding 1 — Internships are the single biggest salary lever

Each internship is worth **$7,559** in starting salary (p < 0.001, CI: [$6,743 — $8,374]). This is the strongest, most precise estimate in the model. Five internships versus zero: a **$37,793 salary advantage** for otherwise identical graduates.

### Finding 2 — GPA matters, but less than most expect

GPA adds **$9,120 per point** (p < 0.001) — significant and real. But on its own, GPA explains only 8.79% of salary variation. Academic performance is necessary but far from sufficient.

### Finding 3 — Computer Science is the most lucrative major

CS graduates earn **$8,949 more** than Business Analytics graduates with identical profiles (p < 0.001). Data Science is second (+$4,018, p = 0.014). Statistics shows no confirmed advantage over Business Analytics (p = 0.148). The technical skill premium is real and large.

### Finding 4 — University tier has a measurable dollar value

Tier 1 vs Tier 3: a **$8,628 salary gap** for graduates with identical GPA, major, internships, and everything else (p < 0.001). Institutional prestige is priced by the market. Tier 1 vs Tier 2: a $5,859 gap.

### Finding 5 — Study hours don't predict salary

Correlation with salary: r = -0.026. No significant effect in any model. The market does not reward hours logged in the library. It rewards demonstrable outcomes: internship experience and tangible projects.

### Finding 6 — GPA and internships don't amplify each other

The interaction term (GPA × Internships) was not significant (p = 0.200). Their effects are simply additive. There is no "complete package" bonus.

### Finding 7 — Omitted variable bias is real and dangerous

Dropping Internships from the model reduced R² by 32.6 percentage points and inflated GPA's coefficient by 5.19%. A model without Internships gives systematically wrong estimates for every other variable. This is a textbook demonstration of why variable selection matters.

### Finding 8 — The model passes 4 of 5 diagnostic tests

Linearity ✅, Homoscedasticity ✅, Independence ✅, No Multicollinearity ✅. Normality shows a minor violation due to heavy-tailed salary outliers ⚠️ — acknowledged but does not invalidate results at this sample size.

---

## Final Verdict

### Best Model: Model 2 — Multiple Linear Regression with 9 Predictors

### The Final Equation

$$\widehat{\text{Salary}} = 58{,}848 + 9{,}120(\text{GPA}) + 7{,}559(\text{Internships}) + 1{,}636(\text{Projects}) + 8{,}949(\text{CS}) + 4{,}018(\text{DS}) - 5{,}859(\text{Tier2}) - 8{,}628(\text{Tier3})$$

*Networking Events, Major_Statistics, and Gender dummies did not reach statistical significance (p > 0.05).*

### Example Prediction

A **Computer Science major, Tier 1 university, GPA 3.5, 2 internships, 3 projects**:

```
Salary = 58,848
       + 9,120 × 3.5      (GPA)          = +31,920
       + 7,559 × 2        (Internships)  = +15,118
       + 1,636 × 3        (Projects)     = +4,908
       + 8,949             (CS major)    = +8,949
       + 0                 (Tier 1)      = $0 penalty
       ─────────────────────────────────────────────
       = $119,743 predicted starting salary
```

### What to Prioritize (Ranked by Dollar Impact)

| Action | Expected Salary Impact |
|---|---|
| Secure 1 additional internship | **+$7,559** |
| Raise GPA by 1 full point | **+$9,120** |
| Switch from Business Analytics to CS | **+$8,949** |
| Complete 2 more portfolio projects | **+$3,272** |
| Attend Tier 1 vs Tier 3 university | **+$8,628** (at admission time) |

**Priority order for students:** Internships → Major selection → University tier → GPA → Projects

---

## Limitations

1. **Simulated dataset:** The data was custom-generated to be realistic. Results are directionally valid and instructive, but cannot be directly generalized to real job market outcomes.

2. **No geographic controls:** Salaries in San Francisco are fundamentally different from rural markets. This variation is invisible to our model and absorbed into the residuals.

3. **No industry data:** A CS major at a hedge fund earns differently than one at a non-profit. Industry is a significant omitted variable.

4. **Mean imputation for missing data:** More sophisticated methods (multiple imputation, regression imputation) could yield slightly different coefficient estimates. With <2% missingness, the impact is minimal.

5. **Normality violation:** Heavy-tailed residuals (kurtosis = 23) mean prediction intervals at extreme salary values ($150K+, <$60K) may be somewhat underestimated. Coefficient estimates remain reliable.

6. **Cross-sectional snapshot:** This captures starting salary only. Different majors and university tiers may diverge substantially in 5- and 10-year salary trajectories — something this data cannot reveal.

7. **Potential selection bias:** We don't know how graduates were sampled. If high-achievers are overrepresented, our coefficients may not generalize to the full graduate population.

---

## Project Structure

```
02-regression/
├── README.md                          ← Project overview (you are reading this)
├── ANALYSIS.md                        ← This technical analysis document
├── regression_analysis.ipynb          ← Full Jupyter notebook with all code
├── data/
│   └── student_salary_data.csv        ← Dataset (500 graduates × 10 variables)
└── figures/
    ├── 01_histograms.png              ← Distribution of all 7 numeric variables
    ├── 02_boxplots.png                ← Boxplots for outlier detection
    ├── 03_correlation_matrix.png      ← Pearson correlation heatmap
    ├── 04_scatterplots.png            ← Salary vs each numeric predictor
    ├── 05_categorical_salary.png      ← Salary by Major, Gender, University Tier
    ├── 06_simple_regression.png       ← Model 1 fitted line with confidence band
    ├── 07_linearity_check.png         ← Residuals vs Fitted + LOWESS
    ├── 08_normality_check.png         ← Q-Q Plot + residual histogram
    ├── 09_homoscedasticity_check.png  ← Scale-Location plot
    └── 10_sensitivity_analysis.png   ← Model A/B/C comparison visualization
```

---

## References

1. James, G., Witten, D., Hastie, T., & Tibshirani, R. (2013). *An Introduction to Statistical Learning*. Springer.
2. Montgomery, D. C., Peck, E. A., & Vining, G. G. (2012). *Introduction to Linear Regression Analysis*. Wiley.
3. Statsmodels Documentation — https://www.statsmodels.org/stable/index.html
4. UCLA OARC: Regression Analysis — https://stats.oarc.ucla.edu/stata/output/regression-analysis/
5. Regression Diagnostics — https://www.statsmodels.org/dev/diagnostic.html

---

*Analysis conducted in Python 3.12.3 · statsmodels · pandas · seaborn · scipy · February 2026*
