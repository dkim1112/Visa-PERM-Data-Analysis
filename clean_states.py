import pandas as pd

# Define columns to extract
extract_columns = ["NAME", "STATE"]

# Read CSV with only specified columns
df = pd.read_csv(
    "university_states.csv",
    on_bad_lines='skip',
    sep=";",
    usecols=lambda col: col in extract_columns
)

print(df.columns.tolist())

df.to_csv("extracted_university_states.csv", index=True)

œ