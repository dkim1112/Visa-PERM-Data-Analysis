import pandas as pd
from rapidfuzz import fuzz, process
import logging

logging.basicConfig(filename='matches.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Read the data
cleaned_df = pd.read_csv('cleaned.csv')
univ_df = pd.read_csv("cleaned_university_rankings.csv")

# Precompute lowercased names
univ_df['Name_lower'] = univ_df['Name'].str.lower()

# Function to get the best match using RapidFuzz
def get_best_match(university_name, univ_df):
    # Check if the university name is empty
    if not university_name:
        return '', ''
    university_name = str(university_name)
    if not university_name:
        return '', ''
    
    university_name = university_name.lower()
    
    # Find the best match in the 'Name_lower' column of univ_df using RapidFuzz
    best_match = process.extractOne(university_name, univ_df['Name_lower'], scorer=fuzz.ratio)
    
    if best_match and best_match[1] > 93.4:
        # Get the corresponding 'Country' and 'Avg_Rank' from the best match
        matched_index = univ_df[univ_df['Name_lower'] == best_match[0]].index[0]
        country = univ_df.loc[matched_index, 'Country']
        avg_rank = univ_df.loc[matched_index, 'Avg_Rank']

        # Log the match (this is more efficient than print  )
        logging.info(f"Matched {university_name} with {best_match[0]} (Score: {best_match[1]})")

        return country, avg_rank
    else:
        return '', ''  # Return empty strings if no good match is found

# Apply the function to each row in the cleaned_df to get 'Country' and 'Avg_Rank'
cleaned_df[['COUNTRY', 'AVG_RANK']] = cleaned_df['FOREIGN_WORKER_INFO_INST'].apply(
    lambda x: pd.Series(get_best_match(x, univ_df))
)

# Save the updated DataFrame to a new CSV file
cleaned_df.to_csv('updated_cleaned.csv', index=False)
