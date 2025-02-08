import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('updated_cleaned_1.csv')

# Drop unnecessary columns
df = df.drop(columns=['Unnamed: 0', 'Unnamed: 0.1'], errors='ignore')

# Remove invalid NAICS codes
df = df[df["NAICS_US_CODE"] != "na"]

# Define finer bins for AVG_RANK (every 5 units)
bin_size = 100
bins = list(range(0, int(df["AVG_RANK"].max()) + bin_size, bin_size))
labels = [f"{bins[i]}-{bins[i+1]}" for i in range(len(bins)-1)]

# Categorize AVG_RANK into bins
df["Rank_Group"] = pd.cut(df["AVG_RANK"], bins=bins, labels=labels, include_lowest=True)

# Compute success rate per Rank_Group
success_rates = (
    df.groupby("Rank_Group")["CASE_STATUS"]
    .apply(lambda x: (x == 'Y').mean() * 100)  # Calculate % of 'Y'
    .reset_index()
    .rename(columns={"CASE_STATUS": "Approval_Percentage"})
)

# Plot the histogram
plt.figure(figsize=(12, 6))
plt.bar(success_rates["Rank_Group"], success_rates["Approval_Percentage"], color="blue", alpha=0.7)

# Formatting
plt.axhline(success_rates["Approval_Percentage"].mean(), color="red", linestyle="dashed", linewidth=1.5, label="Avg")
plt.xlabel("University Ranking Range (AVG_RANK)", fontsize=12)
plt.ylabel("Approval Percentage", fontsize=12)
plt.title("Approval Rate by University Ranking Group", fontsize=14, fontweight="bold")
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.6)

# Save figure
plt.tight_layout()
plt.savefig("approval_rate_by_rank.png", dpi=300, bbox_inches="tight")

# Show plot
plt.show()
