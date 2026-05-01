# UBA MADS — Comprehensive Statistics: NHANES

Semester-long cumulative homework using the **NHANES (National Health and Nutrition Examination Survey)** dataset.

Each module builds on the previous one using the same dataset, progressively applying every statistical concept in the syllabus.

## Dataset

**Source:** NHANES via `statsmodels`

```python
import statsmodels.api as sm
nhanes = sm.datasets.get_rdataset('nhanes', 'NHANES', cache=True).data
```

## Structure

```
data/
  raw/          — original downloaded data, never modified
  processed/    — cleaned and transformed versions

modules/
  01_descriptive_statistics/
  02_probability_distributions/
  03_sampling_estimation/
  04_hypothesis_testing/
  05_anova/
  06_correlation/
  07_simple_regression/
  08_multiple_regression/
  09_nonparametric_methods/

figures/        — all plots and charts (referenced from modules)
notes/          — conceptual notes, theory summaries
```

## Approach

Each module has two components:
1. **My work** — written first, independently
2. **AI-enhanced** — verified and extended with Claude Code

The learning lives in the gap between the two.

## Modules

| # | Topic | Status |
|---|-------|--------|
| 01 | Descriptive Statistics | 🔲 |
| 02 | Probability & Distributions | 🔲 |
| 03 | Sampling & Estimation | 🔲 |
| 04 | Hypothesis Testing | 🔲 |
| 05 | ANOVA | 🔲 |
| 06 | Correlation | 🔲 |
| 07 | Simple Regression | 🔲 |
| 08 | Multiple Regression | 🔲 |
| 09 | Non-parametric Methods | 🔲 |
