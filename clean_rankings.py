import pandas as pd
from rapidfuzz import fuzz, process

# Define columns to extract
extract_columns = ["Rank", "Name", "Country", "Year"]

# Read CSV with only specified columns
df = pd.read_csv("university_rankings.csv", usecols=lambda col: col in extract_columns)
state_dict = pd.read_csv("extracted_university_states.csv")

# Function to get the best state match using RapidFuzz (lowercase both strings)
def get_state_match(university_name, state_dict):
    # Lowercase the university name before matching
    university_name = university_name.lower()

    # Try to find the best match in the state_dict based on university name
    best_match = process.extractOne(university_name, state_dict["NAME"].str.lower(), scorer=fuzz.ratio)
    
    # If the match score is greater than 93.4, return the corresponding state
    if best_match and best_match[1] > 93.4:
        matched_index = state_dict[state_dict["NAME"].str.lower() == best_match[0]].index[0]
        return state_dict.loc[matched_index, "STATE"]
    else:
        return ""  # Return blank if no good match is found

# Normalize the "Country" column
df["Country"] = df["Country"].apply(lambda x: get_state_match(x, state_dict) if x == "United States" else "Outside the US")

# Compute mean ranking for each university
df = df.groupby(["Name", "Country"], as_index=False)["Rank"].mean()

# Round the rank to 2 decimal places
df['Rank'] = df['Rank'].round(2)

# Rename "Rank" column to reflect averaging
df.rename(columns={"Rank": "Avg_Rank"}, inplace=True)

# Save the cleaned dataframe to CSV
df.to_csv("cleaned_university_rankings.csv", index=True)
