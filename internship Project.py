# Bitcoin Market Sentiment vs Trader Performance Analysis
# Author: Bhukya Abhinay
# Objective: Analyze how trader performance relates to market sentiment (Fear/Greed)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load the datasets

historical = pd.read_csv("videos/historical.csv")
sentiment = pd.read_csv("videos/fear.csv")

# Step 2: Convert timestamp fields into datetime format
historical['Timestamp IST'] = pd.to_datetime(historical['Timestamp IST'], format="%d-%m-%Y %H:%M")
sentiment['date'] = pd.to_datetime(sentiment['date'])

# Step 3: Extract just the date (no time) for alignment
historical['Date'] = historical['Timestamp IST'].dt.date
sentiment['Date'] = sentiment['date'].dt.date

# Step 4: Merge both datasets on 'Date'

merged = pd.merge(
    historical,
    sentiment[['Date', 'value', 'classification']],
    on='Date',
    how='left'
)

# Step 5: Drop rows without sentiment data (optional)
merged = merged.dropna(subset=['classification'])

# Step 6: Analyze performance: PnL by sentiment category
print("Closed PnL Summary by Market Sentiment:\n")
print(merged.groupby('classification')['Closed PnL'].describe())

# Step 7: Count how many trades happened in each sentiment category
print("\nTrade Counts by Sentiment:\n")
print(merged['classification'].value_counts())

# Step 8: Plot average PnL by sentiment using a bar chart
plt.figure(figsize=(10, 6))
sns.barplot(data=merged, x='classification', y='Closed PnL', estimator='mean', ci='sd', palette='Set2')
plt.title("Average Trader Profit/Loss by Market Sentiment")
plt.xlabel("Market Sentiment")
plt.ylabel("Average Closed PnL (USD)")
plt.xticks(rotation=15)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

# Step 9: Plot a boxplot to explore distribution of PnL in each sentiment category
plt.figure(figsize=(12, 6))
sns.boxplot(data=merged, x='classification', y='Closed PnL', palette='Set3')
plt.title("Distribution of Trader Profit/Loss by Sentiment")
plt.xlabel("Market Sentiment")
plt.ylabel("Closed PnL (USD)")
plt.ylim(-5000, 10000)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
