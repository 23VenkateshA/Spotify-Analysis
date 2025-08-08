import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =======================
# 1. Load Dataset
# =======================
df = pd.read_csv("tracks.csv")

# Convert release_date to datetime & create 'year' column
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df['year'] = df['release_date'].dt.year

# =======================
# 2. Basic Dataset Info
# =======================
print("\n=== DATA INFO ===")
print(df.info())

print("\n=== MISSING VALUES ===")
print(df.isnull().sum())

print("\n=== SUMMARY STATS ===")
print(df.describe())

# =======================
# 3. Data Cleaning
# =======================
# Remove duplicates
df = df.drop_duplicates()

# Drop rows with missing year 
df = df.dropna(subset=['year'])

# =======================
# 4. Top 10 Most Popular Songs
# =======================
top_songs = df.sort_values(by='popularity', ascending=False).head(10)
print("\n=== TOP 10 SONGS ===")
print(top_songs[['name', 'artists', 'popularity']])
top_songs.to_csv("top_10_songs.csv", index=False)

# =======================
# 5. Top Artists
# =======================
top_artists = df['artists'].value_counts().head(10)
print("\n=== TOP 10 ARTISTS ===")
print(top_artists)

# =======================
# 6. Correlation with Popularity
# =======================
correlation = df.corr(numeric_only=True)['popularity'].sort_values(ascending=False)
print("\n=== CORRELATION WITH POPULARITY ===")
print(correlation)

# Heatmap of correlations with annotations
plt.figure(figsize=(10, 8))
corr_matrix = df.corr(numeric_only=True)

sns.heatmap(
    corr_matrix,
    cmap="coolwarm",
    annot=True,         # Show the numbers
    fmt=".2f",          # Format to 2 decimal places
    annot_kws={"size": 8}  # Smaller font so it fits
)

plt.title("Feature Correlation Heatmap")
plt.tight_layout()
plt.savefig("correlation_heatmap_annotated.png", dpi=300)
plt.show()


# =======================
# 7. Trends Over Time
# =======================
songs_per_year = df.groupby('year').size()
plt.figure(figsize=(10, 5))
songs_per_year.plot(kind='line', title='Songs Released Per Year')
plt.xlabel("Year")
plt.ylabel("Number of Songs")
plt.tight_layout()
plt.savefig("songs_per_year.png")
plt.show()

avg_popularity_year = df.groupby('year')['popularity'].mean()
plt.figure(figsize=(10, 5))
avg_popularity_year.plot(kind='line', color='orange', title='Average Popularity by Year')
plt.xlabel("Year")
plt.ylabel("Average Popularity")
plt.tight_layout()
plt.savefig("avg_popularity_per_year.png")
plt.show()

# =======================
# 8. Popular vs Less Popular Feature Analysis
# =======================
df['is_popular'] = df['popularity'] >= 70
feature_means = df.groupby('is_popular')[['danceability', 'energy', 'tempo']].mean()
print("\n=== FEATURE MEANS (Popular vs Not Popular) ===")
print(feature_means)

# Scatter plot: Danceability vs Energy colored by popularity
plt.figure(figsize=(8, 6))
plt.scatter(df['danceability'], df['energy'], c=df['popularity'], cmap='viridis', alpha=0.5)
plt.colorbar(label='Popularity')
plt.xlabel('Danceability')
plt.ylabel('Energy')
plt.title('Danceability vs Energy colored by Popularity')
plt.tight_layout()
plt.savefig("danceability_vs_energy.png")
plt.show()

# =======================
# 9. Outlier Detection
# =======================
# Example: Songs longer than 10 minutes
outliers_duration = df[df['duration_ms'] > 600000]
print(f"\n=== SONGS LONGER THAN 10 MINUTES ({len(outliers_duration)}) ===")
print(outliers_duration[['name', 'artists', 'duration_ms']].head())

# Save outliers to file
outliers_duration.to_csv("long_songs.csv", index=False)

print("\nAnalysis complete. CSV and PNG files have been saved.")
