import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('updated_cleaned_1.csv')

# Drop unnecessary column
df = df.drop('Unnamed: 0', axis=1)
df = df[df["NAICS_US_CODE"] != "na"]

# Calculate percentage of 'Y' in CASE_STATUS for each unique NAICS_US_CODE
naics_success_rate = (
    df.groupby("NAICS_US_CODE")["CASE_STATUS"]
    .apply(lambda x: (x == 'Y').mean() * 100)  # Calculate % of 'Y'
    .reset_index()
    .rename(columns={"CASE_STATUS": "Approval_Percentage"})
    .sort_values(by="Approval_Percentage", ascending=False)  # Sort in descending order
)

# Calculate the overall average success rate
overall_success_rate = (df["CASE_STATUS"] == 'Y').mean() * 100

# Get top 3 highest and lowest success rate NAICS codes
top3_highest = naics_success_rate.head(3)
top3_lowest = naics_success_rate.tail(3)[::-1]

# Rename NAICS codes to industry names safely
top3_highest.loc[top3_highest.index[0], "NAICS_US_CODE"] = "Merchandise Retailers"
top3_highest.loc[top3_highest.index[1], "NAICS_US_CODE"] = "Information"
top3_highest.loc[top3_highest.index[2], "NAICS_US_CODE"] = "Finance and Insurance"

top3_lowest.loc[top3_lowest.index[0], "NAICS_US_CODE"] = "Postal Services"
top3_lowest.loc[top3_lowest.index[1], "NAICS_US_CODE"] = "Agriculture"
top3_lowest.loc[top3_lowest.index[2], "NAICS_US_CODE"] = "Construction"

# Plot histograms
fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

# Define colors
top_color = "#2ca02c"  # Green for high success rates
low_color = "#1f77b4"  # Blue for low success rates
avg_line_color = "red"

# Function to add value labels
def add_labels(ax, bars):
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 1, f"{yval:.1f}%", ha="center", fontsize=12, fontweight="bold")

# Top 3 Highest Success Rates
bars1 = axes[0].bar(top3_highest["NAICS_US_CODE"], top3_highest["Approval_Percentage"], color=top_color, alpha=0.8)
axes[0].axhline(overall_success_rate, color=avg_line_color, linestyle="dashed", linewidth=1.5, label=f"Avg: {overall_success_rate:.2f}%")
axes[0].set_title("Top 3 Highest Certified Rate Industries", fontsize=14, fontweight="bold")
axes[0].set_ylabel("Approval Percentage", fontsize=12)
axes[0].tick_params(axis='x', rotation=30)  # Rotate x labels for readability
axes[0].grid(axis="y", linestyle="--", alpha=0.6)
axes[0].legend()
add_labels(axes[0], bars1)

# Top 3 Lowest Success Rates
bars2 = axes[1].bar(top3_lowest["NAICS_US_CODE"], top3_lowest["Approval_Percentage"], color=low_color, alpha=0.8)
axes[1].axhline(overall_success_rate, color=avg_line_color, linestyle="dashed", linewidth=1.5, label=f"Avg: {overall_success_rate:.2f}%")
axes[1].set_title("Top 3 Lowest Certified Rate Industries", fontsize=14, fontweight="bold")
axes[1].tick_params(axis='x', rotation=30)
axes[1].grid(axis="y", linestyle="--", alpha=0.6)
axes[1].legend()
add_labels(axes[1], bars2)

# Remove unnecessary spines
for ax in axes:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

# Save the figure as PNG
plt.tight_layout()
plt.savefig("certified_rate_industries.png", dpi=300, bbox_inches="tight")

# Display plots
plt.show()