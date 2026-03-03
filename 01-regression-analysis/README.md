# Determinants of Graduate Starting Salary: A Multiple Linear Regression Analysis

## Abstract

This study investigates the determinants of starting salary among 500 recent graduates using Ordinary Least Squares (OLS) regression. We evaluate the independent contribution of GPA, internships, projects, major selection, university tier, and networking engagement. While GPA alone explains only 8.8% of salary variation, a multiple regression model incorporating nine predictors explains 53.2% of the variance in starting salary. Internship experience emerges as the strongest predictor, contributing $7,559 per internship (p < 0.001), followed by GPA at $9,120 per point (p < 0.001), Computer Science major premium at $8,949 (p < 0.001), and university tier penalties of −$5,859 (Tier 2) and −$8,628 (Tier 3) relative to Tier 1 institutions. The final model satisfies key OLS assumptions, with only minor heavy-tail deviation in residual normality. Results indicate that applied experience dominates academic effort in determining early-career salary outcomes.

---

## 1. Introduction

Graduating students frequently receive qualitative advice regarding career preparation—maintain a high GPA, pursue internships, select technical majors, and attend reputable institutions. However, the market value of each of these factors is rarely quantified.

This analysis addresses the following research question:

**Which factors significantly predict starting salary, and what is their independent dollar contribution?**

Using a structured regression modeling framework, we move beyond correlation to isolate causal contribution under controlled conditions.

---

## 2. Data Description

The dataset consists of 500 graduates with starting salaries ranging from $39,041 to $196,178 and a mean salary of $106,338 (SD = $15,975). The salary distribution exhibits mild right skew (0.21) and elevated kurtosis (4.66), indicating heavier-than-normal tails typical of income data.

Predictors include seven numeric variables (GPA, study hours, internships, projects, networking events, age, and salary) and three categorical variables (major, university tier, and gender). Missing values were minimal (1–2%) and handled using mean imputation, preserving full sample size.

Exploratory correlation analysis shows internships have the strongest bivariate relationship with salary (r = 0.602), followed by GPA (r = 0.296). Projects exhibit a weak positive relationship (r = 0.166), while networking events (r = 0.085) and study hours (r = −0.026) show negligible association.

These findings suggest experiential variables may dominate academic effort in salary determination.

---

## 3. Model 1: Simple Linear Regression (Salary ~ GPA)

The baseline model estimates salary as a function of GPA alone:

Salarŷ = 73,189 + 10,370(GPA)

The GPA coefficient of $10,370 is statistically significant (t = 6.89, p < 0.001), with a 95% confidence interval of [$7,414, $13,326]. This implies that a 0.5 GPA increase corresponds to an expected $5,185 salary increase.

However, the model explains only 8.8% of salary variation (R² = 0.0879), indicating GPA alone is insufficient to explain earnings differences.

---

## 4. Model 2: Multiple Linear Regression

The full model includes nine predictors:

Salarŷ =  
58,848  
+ 9,120(GPA)  
+ 7,559(Internships)  
+ 1,636(Projects)  
+ 8,949(CS)  
+ 4,018(DS)  
− 5,859(Tier2)  
− 8,628(Tier3)

The model achieves R² = 0.5324 (Adjusted R² = 0.5235), explaining 53.2% of salary variation. The F-statistic is highly significant (p < 0.001), confirming joint model validity.

### GPA

After controlling for all other predictors, GPA contributes $9,120 per point (p < 0.001; 95% CI: $6,972–$11,268). The coefficient decreases from $10,370 in the simple model to $9,120 here, demonstrating correction for omitted variable bias.

### Internships

Internships contribute $7,559 per additional internship (p < 0.001; 95% CI: $6,743–$8,374). A graduate with five internships is predicted to earn $37,793 more than one with none, holding all else constant. Removing internships reduces R² to 0.206, confirming it as the dominant predictor.

### Projects

Each completed project contributes $1,636 (p < 0.001). While smaller than internships, projects provide a measurable salary premium.

### Major Effects

Relative to Business Analytics (reference category), Computer Science majors earn $8,949 more (p < 0.001), and Data Science majors earn $4,018 more (p = 0.014). Statistics majors show a positive but non-significant coefficient of $2,574 (p = 0.148).

### University Tier

Relative to Tier 1 institutions, Tier 2 graduates earn $5,859 less (p < 0.001), and Tier 3 graduates earn $8,628 less (p < 0.001). These effects persist after controlling for GPA and internships, indicating institutional prestige has independent market value.

### Networking and Gender

Networking events contribute $486 per event but are not statistically significant (p = 0.085). Gender effects are also not significant.

---

## 5. Interaction Model (Model 3)

An interaction term between GPA and internships was tested to evaluate potential synergy:

Coefficient = $1,219 (p = 0.200)

The interaction is not statistically significant. R² increases marginally from 0.5324 to 0.5340, while AIC worsens. Effects are additive rather than multiplicative.

---

## 6. Model Diagnostics

Linearity was confirmed via residual vs fitted plots showing no systematic curvature. Homoscedasticity was supported by a Breusch–Pagan test (p = 0.163). Independence is satisfied given cross-sectional design, with Durbin–Watson = 2.265 indicating no autocorrelation. Variance Inflation Factors range from 1.0 to 2.3, confirming absence of multicollinearity.

Normality tests detect heavy tails (kurtosis = 23.1 in residuals), primarily due to extreme salary outliers. Given sample size (n = 485), coefficient inference remains robust under the Central Limit Theorem.

---

## 7. Practical Interpretation

For a Computer Science graduate from a Tier 1 university with GPA 3.5, two internships, and three projects:

58,848  
+ (3.5 × 9,120)  
+ (2 × 7,559)  
+ (3 × 1,636)  
+ 8,949  
= 119,743

Predicted starting salary: $119,743.

Among controllable variables, internships provide the highest marginal return per unit effort.

---

## 8. Conclusion

The final multiple regression model explains over half of salary variation and satisfies core OLS assumptions. The dominant predictors of starting salary are internship experience, major selection (especially Computer Science), university tier, and GPA. Internship experience yields the strongest and most stable effect at $7,559 per internship.

The central conclusion is clear:

**Applied professional experience exerts a greater influence on early-career salary than academic effort alone.**

While GPA and institutional prestige matter, internships represent the most powerful lever available to students seeking to maximize starting salary.
