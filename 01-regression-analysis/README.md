# Bivariate & Multivariate Linear Regression Analysis
## Predicting Graduate Starting Salaries

**Course**: DSCI 503 — Statistical Inference and Stochastic Processes
**Institution**: University of Bay Area, Masters in Applied Data Science
**Due Date**: March 2, 2026
**Author**: Ahmad Naggayev

---

## 📋 Problem Statement

What determines a graduate's starting salary? This project investigates that question using a dataset of 500 recent graduates, employing simple and multiple linear regression to quantify the relationship between academic performance, career preparation, and starting compensation.

The central hypothesis is that salary is not solely determined by academic performance (GPA), but is a function of a combination of factors including internship experience, field of study, and institutional prestige. This analysis tests that hypothesis statistically, compares competing regression models, checks all classical OLS assumptions, and provides actionable insights for students seeking to maximize their earning potential.

---

## 📊 Dataset

| Property | Value |
|----------|-------|
| Observations | 500 graduates |
| Features | 10 variables |
| Target Variable | Starting Salary (USD) |
| Salary Range | $39,041 — $196,178 |
| Mean Salary | $106,338 |
| Median Salary | $105,821 |

**Predictors**:
- **Continuous**: GPA (2.0–4.0), Study Hours/Week, Age, Projects Completed, Networking Events, Internships Count
- **Categorical**: Major (Business Analytics, Computer Science, Data Science, Statistics), University Tier (Tier1, Tier2, Tier3), Gender

### Data Generation Methodology

This dataset was **synthetically generated** (`create_dataset.py`) using `numpy` with a fixed random seed (42) to ensure full reproducibility. This approach was chosen intentionally for a statistical methods course, as it offers three significant advantages over a scraped real-world dataset:

1. **Ground truth is known**: Because salary was constructed from explicit rules, we can evaluate how well regression recovers the true underlying relationships — a learning exercise not possible with opaque real-world data.
2. **Controlled complexity**: The dataset was designed to include realistic statistical challenges: missing values (~5%), high-earner outliers (×1.5 salary multiplier), and low-earner outliers — all at known, documented rates.
3. **Reproducibility**: Any reviewer can regenerate the exact dataset by running `create_dataset.py`.

**True data-generating process (DGP)**:

```
Salary = 45,000
       + 8,000 × GPA
       + 200 × Study_Hours
       + 5,000 × Internships
       + 1,000 × (Age − 24)
       + 1,500 × Projects
       + 300 × Networking_Events
       + Major_Effect        # CS: +12K, DS: +10K, Stats: +5K, BA: +3K
       + Tier_Effect         # Tier1: +8K, Tier2: +3K, Tier3: 0
       + 1,000 × GPA × Internships   # interaction term
       + ε  where ε ~ N(0, 5,000²)
```

**Comparison: True DGP vs Estimated Coefficients**

| Predictor | True Effect | Estimated (Model 2) | Note |
|-----------|-------------|----------------------|------|
| GPA | $8,000 | $9,120 | Slightly inflated — absorbs unmodeled interaction |
| Internships | $5,000 | $7,559 | Inflated — same reason |
| Projects | $1,500 | $1,636 | Close to truth |
| CS Major premium | $9,000 (vs BA) | $8,949 | Near-exact recovery |
| Tier1 vs Tier3 | $8,000 | $8,628 | Close to truth |

The overestimation of GPA and Internships coefficients in Model 2 is expected — when an interaction term (GPA × Internships) is present in the true DGP but omitted from the model, the main effect coefficients absorb part of the interaction signal. This is confirmed by Model 3, where adding the interaction term brings the GPA coefficient back down to $7,245 and the Internships coefficient to $3,578 — both closer to their true values.

---

## 🔍 Exploratory Data Analysis

### Distribution Analysis (`01_histograms.png`)

Histograms of all continuous variables reveal the following:

- **Salary**: Approximately bell-shaped with a slight right skew. The mean ($106,338) and median ($105,821) are close, indicating a roughly symmetric core distribution with a tail of high earners pulling the mean slightly right.
- **GPA**: Normally distributed, centered at 3.2. Students are distributed evenly across the 2.0–4.0 range, with no significant skew.
- **Internships**: Strongly right-skewed. Most students have 0–2 internships (median = 1), with few having 4–5. This skew means averages underrepresent the majority experience.
- **Study Hours/Week**: Right-skewed with most students studying 15–35 hours. A small group studies significantly more.
- **Projects Completed**: Near-normal distribution centered at 3, ranging from 0 to 9.
- **Networking Events**: Slightly right-skewed, median of 4 events attended.

### Outlier Detection (`02_boxplots.png`)

Boxplot analysis identifies several notable outliers:

- **Salary**: One extreme high earner at ~$196,178 and one low at ~$39,041. Several outliers cluster above $145,000, suggesting a small high-performance subgroup.
- **Study Hours**: One outlier at ~47 hours/week — well above the IQR ceiling of ~30 hours.
- **Internships**: Outliers at 4–5 internships — exceptional candidates.
- **Age**: Outliers at 29–30 — older students returning to complete graduate study.
- **Projects**: Outliers at 8–9 completed projects — highly productive students.

All outliers were retained in the analysis as they represent legitimate variation in the population, not data errors.

### Correlation Analysis (`03_correlation_matrix.png`)

The correlation heatmap reveals the strength of linear relationships between all variables:

| Predictor | Correlation with Salary |
|-----------|------------------------|
| Internships Count | **r = 0.60** (strongest) |
| GPA | r = 0.30 (moderate) |
| Projects Completed | r = 0.17 (weak) |
| Networking Events | r = 0.09 (very weak) |
| Age | r = 0.04 (negligible) |
| Study Hours/Week | r = -0.03 (negligible) |

Critically, inter-predictor correlations are all near zero (highest: GPA vs Study Hours at r = -0.08), indicating **low multicollinearity risk** — each predictor contributes independently.

### Bivariate Scatterplots (`04_scatterplots.png`)

Scatterplots with trend lines confirm the correlation findings:

- **Salary vs Internships** (r = 0.602): The clearest linear trend in the dataset. Salary rises consistently with each additional internship, with noticeable separation between 0, 1, 2, 3, and 4+ internship groups.
- **Salary vs GPA** (r = 0.296): A positive but moderate trend. The wide scatter around the trend line foreshadows the low R² of the simple regression model (8.8%).
- **Salary vs Projects** (r = 0.166): Weak but visible positive trend. Students with 6+ projects tend to cluster toward higher salaries.
- **Salary vs Study Hours** (r = -0.026), **vs Age** (r = 0.044), **vs Networking Events** (r = 0.085): Essentially flat trend lines — these variables show no meaningful bivariate relationship with salary on their own.

### Categorical Salary Analysis (`05_categorical_salary.png`)

- **By Major**: Computer Science graduates have the highest median salary (~$110K), followed by Data Science (~$106K) and Statistics (~$104K), with Business Analytics lowest (~$100K). These differences are later confirmed as statistically significant in regression.
- **By University Tier**: A clear salary ladder — Tier1 median (~$110K) > Tier2 (~$103K) > Tier3 (~$100K). Institutional prestige has a measurable, independent effect.
- **By Gender**: Female and Male graduates show near-identical median salaries (~$105–108K). Non-Binary graduates show a slightly lower median (~$102K), though this may reflect smaller sample size. Gender was not included as a significant predictor in final models.

---

## 📈 Regression Models

### Model 1: Simple Linear Regression (`06_simple_regression.png`)

**Equation**: Salary = 73,189 + 10,370 × GPA

| Metric | Value |
|--------|-------|
| R² | 0.088 |
| Adjusted R² | 0.086 |
| F-statistic | 47.51 (p < 0.001) |
| GPA Coefficient | $10,370 (p < 0.001) |
| 95% CI for GPA | [$7,414 — $13,300] |

The scatter plot confirms a statistically significant positive relationship between GPA and salary, but the wide confidence band and dispersed data points make clear that GPA alone explains only **8.8% of salary variation**. The model is highly significant but practically limited as a standalone predictor.

### Model 2: Multiple Linear Regression (Recommended)

| Predictor | Coefficient | p-value | Significance |
|-----------|-------------|---------|--------------|
| Intercept | $58,850 | < 0.001 | *** |
| GPA | +$9,120 | < 0.001 | *** |
| Internships Count | +$7,559 | < 0.001 | *** |
| Projects Completed | +$1,636 | < 0.001 | *** |
| Networking Events | +$486 | 0.085 | ns |
| Major: CS vs Bus. Analytics | +$8,949 | < 0.001 | *** |
| Major: Data Science vs Bus. Analytics | +$4,018 | 0.014 | ** |
| Major: Statistics vs Bus. Analytics | +$2,574 | 0.148 | ns |
| University Tier2 vs Tier1 | -$5,859 | < 0.001 | *** |
| University Tier3 vs Tier1 | -$8,628 | < 0.001 | *** |

| Metric | Value |
|--------|-------|
| R² | 0.532 |
| Adjusted R² | 0.524 |
| F-statistic | 60.09 (p < 0.001) |
| Observations | 485 |

### Model 3: Multiple Regression with Interaction Term (GPA × Internships)

The interaction term ($1,219, p = 0.200) is **not statistically significant**. R² improved by only 0.16 percentage points over Model 2. Model 2 is preferred.

---

## 🎯 Key Findings

### 1. GPA Alone Is an Insufficient Predictor
Despite being statistically significant (p < 0.001), GPA explains only **8.8% of salary variation**. The simple regression scatter plot visually confirms this — data points are widely dispersed around the trend line at every GPA level.

### 2. Multiple Predictors Explain 53.2% of Salary Variation
Adding eight additional predictors raises R² from 0.088 to **0.532**, a gain of 44.4 percentage points. Adjusted R² of 0.524 confirms this improvement is genuine and not an artifact of adding more variables.

### 3. Internships Are the Dominant Predictor
With the highest bivariate correlation (r = 0.602) and a coefficient of **$7,559 per internship** (p < 0.001), internships are the single most impactful controllable factor. The sensitivity analysis (Plot 10) dramatically illustrates this: removing internships from the model causes R² to collapse from 0.53 to **0.21** — a 60% reduction in explanatory power.

### 4. GPA Still Matters Significantly in the Full Model
Controlling for all other factors, each GPA point is worth **$9,120** in starting salary (p < 0.001). The slight decrease from the simple model coefficient ($10,370 → $9,120) reflects some shared variance with other predictors, but GPA remains independently significant.

### 5. Projects Completed Adds Independent Value
Each additional project completed adds **$1,636 to salary** (p < 0.001). This is separate from internship experience — suggesting that a strong portfolio signals competence beyond formal work history.

### 6. Field of Study Creates a $8,949 Gap at the Top
Computer Science graduates earn **$8,949 more** than Business Analytics graduates (p < 0.001), holding GPA, internships, and other factors constant. Data Science graduates earn $4,018 more (p = 0.014). The Statistics premium ($2,574) is not statistically significant (p = 0.148).

### 7. University Tier Has a Strong Independent Effect
Even after controlling for GPA and major, institutional prestige matters:
- Tier1 vs Tier3 gap: **$8,628** (p < 0.001)
- Tier1 vs Tier2 gap: **$5,859** (p < 0.001)

This suggests that employer recruitment patterns, alumni networks, and brand recognition provide measurable salary advantages independent of academic performance.

### 8. Study Hours and Age Do Not Predict Salary
Both Study Hours/Week (r = -0.03) and Age (r = 0.04) show negligible correlations with salary and are not significant predictors in any model. Working harder in terms of raw study time does not translate to higher pay — what matters is what you study and the experiences you build.

### 9. No Synergistic Effect Between GPA and Internships
Model 3 tested whether high-GPA students extract more salary benefit from each internship. The interaction term was not significant (p = 0.200), and the R² gain was negligible (0.16%). GPA and internships contribute **independently** and **additively** to salary — a student benefits equally from improving GPA regardless of internship count, and vice versa.

---

## 🔬 Model Diagnostics

### Linearity (`07_linearity_check.png`)
The Residuals vs Fitted plot shows the LOWESS smoothing line running approximately flat along zero across the full range of fitted values. The partial residual plot for GPA confirms a clean linear relationship. **Linearity assumption: satisfied.**

### Normality of Residuals (`08_normality_check.png`)
The Q-Q plot shows significant deviation from the diagonal in both tails — residuals cluster vertically rather than following the 45° reference line. The histogram of residuals shows a leptokurtic (high-peaked, heavy-tailed) distribution. The Jarque-Bera test (p < 0.001, Kurtosis = 23.06) formally rejects normality. **Normality assumption: violated.** With n = 485, the Central Limit Theorem provides some protection for inference, but this remains a limitation.

### Homoscedasticity (`09_homoscedasticity_check.png`)
The Scale-Location plot shows the LOWESS line with a slight upward slope from lower to higher fitted values, indicating **mild heteroscedasticity** — variance of residuals grows slightly at higher predicted salaries. This is consistent with high-earner salary variability being harder to predict. The violation is modest and does not invalidate the model, but robust standard errors would be preferable in applied settings.

---

## 📉 Sensitivity Analysis (`10_sensitivity_analysis.png`)

Three models were compared:

| Model | Description | R² | AIC |
|-------|-------------|-----|-----|
| A: Full (Baseline) | All 9 predictors | 0.532 | 10,416 |
| B: Reduced | Drop Internships | 0.210 | 10,754 |
| C: Extended | Add GPA × Internships interaction | 0.534 | 10,416 |

**Key takeaway from the bar charts**: Dropping Internships (Model B) causes R² to fall from 0.53 to 0.21 — a dramatic collapse that visually dominates the R² comparison chart. This is the strongest evidence in the entire analysis that internships are the critical driver of graduate salaries. Model C's AIC is identical to Model A despite adding a predictor, further confirming the interaction term adds no real value.

---

## 🏆 Model Comparison

| Model | Predictors | R² | Adj R² | AIC |
|-------|------------|-----|--------|-----|
| Model 1: Simple (GPA only) | 1 | 0.088 | 0.086 | 10,949 |
| Model 2: Multiple (Full) | 9 | 0.532 | 0.524 | 10,416 |
| Model 3: Multiple + Interaction | 10 | 0.534 | 0.524 | 10,416 |

**Recommended Model**: Model 2 (Multiple Regression, 9 predictors). It maximizes explanatory power with the lowest AIC, satisfies linearity, and avoids unnecessary complexity from the non-significant interaction term.

---

## 💡 Practical Recommendations

Based on the statistical evidence:

1. **Prioritize internships above all else** — the single highest-return activity ($7,559/internship) and the most critical variable in the model
2. **Maintain a strong GPA** — each GPA point is independently worth ~$9,120
3. **Complete meaningful projects** — each project adds $1,636 independently of internships
4. **Choose major strategically** — CS graduates earn ~$8,949 more than Business Analytics, all else equal
5. **Target Tier1 institutions where possible** — the $8,628 institutional premium persists after controlling for GPA and major
6. **Do not optimize for study hours** — raw study time shows no salary relationship; quality and application of learning matters more than quantity

---

## ⚠️ Limitations

- **Normality violated**: Heavy-tailed residuals suggest the model may underperform for extreme salary predictions
- **Mild heteroscedasticity**: Variance grows at higher salary ranges; robust standard errors would be more appropriate
- **R² ceiling at 53%**: Nearly half of salary variation is unexplained — likely due to unmeasured factors (job location, employer size, personal network, negotiation skill)
- **Cross-sectional data**: No longitudinal tracking of salary growth over time
- **Synthetic/controlled dataset**: Real-world salary prediction would require broader geographic and industry coverage

---

## 📁 Project Structure

```
01-regression-analysis/
│
├── regression_analysis.ipynb         # Main analysis notebook (START HERE)
├── create_dataset.py                 # Dataset generation script
├── requirements.txt                  # Python dependencies
├── README.md                         # This file
├── data/
│   └── student_salary_data.csv       # Dataset (500 graduates, 10 variables)
└── figures/
    ├── 01_histograms.png             # Distribution of all variables
    ├── 02_boxplots.png               # Outlier detection
    ├── 03_correlation_matrix.png     # Pearson correlation heatmap
    ├── 04_scatterplots.png           # Bivariate salary relationships
    ├── 05_categorical_salary.png     # Salary by Major, Gender, University Tier
    ├── 06_simple_regression.png      # Model 1: GPA vs Salary
    ├── 07_linearity_check.png        # Residuals vs Fitted + Partial Residuals
    ├── 08_normality_check.png        # Q-Q Plot + Residual Histogram
    ├── 09_homoscedasticity_check.png # Scale-Location Plot
    └── 10_sensitivity_analysis.png   # Model Comparison (R² and AIC)
```

---

## 🚀 Quick Start

```bash
pip install -r requirements.txt
jupyter notebook
```

Open `regression_analysis.ipynb` and run all cells. Expected runtime: ~30–60 seconds.

---

## 📚 References

1. James, G., Witten, D., Hastie, T., & Tibshirani, R. (2013). *An Introduction to Statistical Learning*. Springer.
2. Montgomery, D. C., Peck, E. A., & Vining, G. G. (2012). *Introduction to Linear Regression Analysis*. Wiley.
3. Statsmodels Documentation: https://www.statsmodels.org/
4. UCLA OARC Regression Analysis Guide: https://stats.oarc.ucla.edu/stata/output/regression-analysis/
5. Anthropic. (2026). *Claude* [Large language model]. Used as a programming and debugging assistant. https://claude.ai
