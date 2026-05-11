import pandas as pd

df = pd.read_csv("cleanData.csv")

# Split genres, flatten, and get unique values
unique_genres = set()

for genres in df['Genre'].dropna():
    for genre in genres.split(','):
        unique_genres.add(genre.strip())

# Convert to sorted list (optional)
unique_genres = sorted(unique_genres)

print(unique_genres)