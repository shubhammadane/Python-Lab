import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv("IMDbRatings_IndianMovies.csv")

# Remove rows with any missing (NaN) values
df_clean = df.dropna()
# Replace empty strings with NaN, then drop those rows as well
df_clean = df_clean.replace('', pd.NA).dropna()

# Create a list of all columns except 'Name'
cols_except_name = [col for col in df_clean.columns if col != 'Name']
# Remove duplicate rows based on all columns except 'Name'
df_clean = df_clean.drop_duplicates(subset=cols_except_name)

# Remove the 'Actor 3' column from the dataset
df_clean = df_clean.drop(columns=['Actor 3'])

# Save the cleaned data into a new CSV file without row index
df_clean.to_csv("cleanData.csv", index=False)

# Print confirmation message
print("Cleaned data saved to cleanData.csv")