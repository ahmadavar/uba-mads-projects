"""
Create a realistic student salary dataset for regression analysis
Meets all homework requirements:
- 500 rows
- 10 variables (8+ required)
- Numeric outcome (Salary)
- Multiple numeric predictors
- Categorical predictors
- Realistic messiness (missing values, outliers)
"""

import pandas as pd
import numpy as np

# Set seed for reproducibility
np.random.seed(42)

n_samples = 500

# Create student data
data = {
    # Numeric predictors
    'GPA': np.random.normal(3.2, 0.5, n_samples).clip(2.0, 4.0),
    'Study_Hours_Per_Week': np.random.normal(25, 8, n_samples).clip(5, 50),
    'Internships_Count': np.random.poisson(1.5, n_samples).clip(0, 5),
    'Age': np.random.normal(24, 2, n_samples).clip(21, 30),
    'Projects_Completed': np.random.poisson(3, n_samples).clip(0, 10),
    'Networking_Events': np.random.poisson(4, n_samples).clip(0, 15),

    # Categorical predictors
    'Major': np.random.choice(['Computer Science', 'Data Science', 'Statistics', 'Business Analytics'], n_samples, p=[0.35, 0.30, 0.20, 0.15]),
    'Gender': np.random.choice(['Male', 'Female', 'Non-Binary'], n_samples, p=[0.48, 0.48, 0.04]),
    'University_Tier': np.random.choice(['Tier1', 'Tier2', 'Tier3'], n_samples, p=[0.25, 0.50, 0.25])
}

df = pd.DataFrame(data)

# Create salary based on realistic relationships
# Base salary
salary = 45000

# Add effects of each variable
salary += df['GPA'] * 8000  # Higher GPA = higher salary
salary += df['Study_Hours_Per_Week'] * 200  # Study time matters
salary += df['Internships_Count'] * 5000  # Internships are valuable
salary += (df['Age'] - 24) * 1000  # Age/experience
salary += df['Projects_Completed'] * 1500  # Portfolio matters
salary += df['Networking_Events'] * 300  # Networking helps

# Major effects (dummy variable effects)
major_effect = {'Computer Science': 12000, 'Data Science': 10000, 'Statistics': 5000, 'Business Analytics': 3000}
salary += df['Major'].map(major_effect)

# University tier effects
tier_effect = {'Tier1': 8000, 'Tier2': 3000, 'Tier3': 0}
salary += df['University_Tier'].map(tier_effect)

# Add some random noise
salary += np.random.normal(0, 5000, n_samples)

# Add some non-linear relationship (interaction between GPA and internships)
salary += (df['GPA'] * df['Internships_Count']) * 1000

df['Salary'] = salary

# Introduce some realistic messiness
# 1. Missing values (~5%)
missing_indices = np.random.choice(df.index, size=int(0.05 * n_samples), replace=False)
for idx in missing_indices[:10]:
    df.loc[idx, 'Study_Hours_Per_Week'] = np.nan
for idx in missing_indices[10:20]:
    df.loc[idx, 'Networking_Events'] = np.nan
for idx in missing_indices[20:25]:
    df.loc[idx, 'GPA'] = np.nan

# 2. Add some outliers (high earners)
outlier_indices = np.random.choice(df.index, size=10, replace=False)
df.loc[outlier_indices, 'Salary'] = (df.loc[outlier_indices, 'Salary'] * 1.5).values

# 3. Add some low outliers (unemployed/part-time)
low_outlier_indices = np.random.choice(df.index, size=5, replace=False)
df.loc[low_outlier_indices, 'Salary'] = (df['Salary'].min() * 0.5)

# Convert salary to integer at the end
df['Salary'] = df['Salary'].astype(int)

# Save to CSV
df.to_csv('data/student_salary_data.csv', index=False)

print(f"✓ Dataset created successfully!")
print(f"Shape: {df.shape}")
print(f"Saved to: data/student_salary_data.csv")
print(f"\nPreview:")
print(df.head())
print(f"\nMissing values:")
print(df.isnull().sum())
