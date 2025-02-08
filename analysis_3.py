import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('updated_cleaned_1.csv')

# Drop unnecessary columns
df = df.drop(columns=['Unnamed: 0', 'Unnamed: 0.1'], errors='ignore')

# Remove invalid NAICS codes
df = df[df["NAICS_US_CODE"] != "na"]

# Filter rows where 'YEAR_DIFF' is between 0 and 50
df_filtered = df[(df["YEAR_DIFF"] >= 0) & (df["YEAR_DIFF"] <= 50)]

# Calculate minimum, median, and mean values of 'YEAR_DIFF' in the filtered dataframe
min_year_diff = df_filtered["YEAR_DIFF"].min()
median_year_diff = df_filtered["YEAR_DIFF"].median()

# Extract a sub-dataframe where 'YEAR_DIFF' is between min_year_diff and median_year_diff
df_sub = df_filtered[(df_filtered["YEAR_DIFF"] >= min_year_diff)
                     & (df_filtered["YEAR_DIFF"] <= median_year_diff)]

# Select only 'YEAR_DIFF' and 'NAICS_US_CODE' columns
df_sub = df_sub[['YEAR_DIFF', 'NAICS_US_CODE']]

# Calculate the ratio of each 'NAICS_US_CODE' in the sub dataframe

naics_ratio = df_sub['NAICS_US_CODE'].value_counts(normalize=True) * 100

# Sort the ratio in descending order
naics_ratio_sorted = naics_ratio.sort_values(ascending=False)

# Print the results
print(f"Minimum YEAR_DIFF: {min_year_diff}")
print(f"Median YEAR_DIFF: {median_year_diff}")
print("\nTop 5 NAICS_US_CODE Ratios (sorted):")
print(naics_ratio_sorted.head(5))
