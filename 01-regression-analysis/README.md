# Determinants of Graduate Starting Salary
**DSCI 503 — Statistical Inference · University of Bay Area · MADS Program**

*Ahmad Naggayev*

---

## Live App

**[https://uba-mads-grad-salary.streamlit.app](https://uba-mads-grad-salary.streamlit.app)**

---

## What This Project Is

An end-to-end regression study answering: *which factors actually determine a graduate's starting salary — and by how much?*

Using OLS regression on 500 graduates, we quantify the dollar impact of GPA, internships, major, and university tier — holding everything else constant.

## Key Results

| Factor | Impact |
|--------|--------|
| Each internship | +$7,559 |
| Each GPA point | +$9,120 |
| CS vs Business Analytics | +$8,949 |
| Tier 1 vs Tier 3 university | +$8,628 |
| Full model R² | 53.2% (vs 8.8% GPA alone) |

## Project Files

| File | Description |
|------|-------------|
| `app.py` | Streamlit interactive app (9 tabs) |
| `regression_analysis.ipynb` | Full analysis notebook |
| `final_report.md` | Written report with all findings |
| `presentation.pdf` | Slide deck |
| `data/student_salary_data.csv` | Dataset (500 graduates, 10 variables) |

## Stack

Python · Streamlit · statsmodels · pandas · seaborn · matplotlib · scikit-learn
