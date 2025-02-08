import pandas as pd
import scipy.stats as stats

# Load data
df = pd.read_csv('updated_cleaned_1.csv')

# Drop unnecessary column
df = df.drop(columns=['Unnamed: 0'], errors='ignore')

# Define categories (independent variables)
categories = [
    "AVG_RANK",
    "COUNTRY",
    "COUNTRY_OF_CITIZENSHIP",
    "FW_INFO_BIRTH_COUNTRY",
    "NAICS_US_CODE",
    "DECISION_YEAR",
    "FW_EDU_YEAR",
    "YEAR_DIFF"
]

# Dictionary to store chi-square values and p-values
chi2_results = {}

for category in categories:
    if category in df.columns:
        unique_count = df[category].nunique()

        # Create contingency table
        contingency_table = pd.crosstab(df[category], df['CASE_STATUS'])

        # Perform Chi-square test
        chi2_stat, p_val, dof, expected = stats.chi2_contingency(contingency_table)

        # Normalize chi-square statistic by unique values
        normalized_chi2 = chi2_stat / unique_count if unique_count > 0 else 0

        # Store chi-square statistic and p-value
        chi2_results[category] = (normalized_chi2, p_val)

# Sort categories by chi-square value in descending order
sorted_results = sorted(chi2_results.items(), key=lambda x: x[1][0], reverse=True)

# Print results with better p-value formatting
print("Top categories with the strongest relationship to CASE_STATUS:")
for category, (chi2_val, p_val) in sorted_results:
    p_val_str = f"{p_val:.5f}" if p_val > 1e-5 else f"{p_val:.2e}"  # Use scientific notation for very small values
    print(f"{category}: Chi-square = {chi2_val:.2f}, p-value = {p_val_str}")
