import pandas as pd

# Read the data
df = pd.read_csv('updated_cleaned_0.csv')

def round_and_convert(value):
    if pd.isna(value):  # Check if the value is NaN or None
        return value  # Return the NaN or None as is
    return int(round(value, -1))  # Round to the nearest 10th and convert to int

# Apply the function to the 'Values' column
df['AVG_RANK'] = df['AVG_RANK'].apply(round_and_convert)

# Group NAICS_US_CODE by just leaving the first 2 digits
df['NAICS_US_CODE'] = df['NAICS_US_CODE'].astype(str).str[:2]

# Save the updated DataFrame to a new CSV file
df.to_csv('updated_cleaned_1.csv', index=True)
