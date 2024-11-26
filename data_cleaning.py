import pandas as pd

# File paths
fiction_file = "fiction_all.csv"
non_fiction_file = "non_fiction_all.csv"
merged_file = "merged_genres.csv"
author_appearances_file = "author_appearances.csv"
book_appearances_file = "book_appearances.csv"

# Load the data
fiction_df = pd.read_csv(fiction_file)
non_fiction_df = pd.read_csv(non_fiction_file)

# Add Genre column
fiction_df["Genre"] = "Fiction"
non_fiction_df["Genre"] = "Non-fiction"

# Cleaning function for the 'Author' column: Remove the last period
def clean_author(author):
    if pd.isna(author):
        return author
    if author.endswith("."):
        return author[:-1]
    return author

# Cleaning function for the 'Description' column: Keep everything before the last period
def clean_description(description):
    if pd.isna(description):
        return ""
    if "." in description:
        return description.rsplit(".", 1)[0].strip()
    return ""

# Cleaning function for the 'Publisher' column: Remove everything after and including the "$"
def clean_publisher(publisher):
    if pd.isna(publisher):
        return publisher
    if "$" in publisher:
        return publisher.split("$", 1)[0].strip()
    return publisher

# Apply cleaning to both DataFrames
for df in [fiction_df, non_fiction_df]:
    df["Author"] = df["Author"].apply(clean_author)
    df["Description"] = df["Description"].apply(clean_description)
    df["Publisher"] = df["Publisher"].apply(clean_publisher)


fiction_df.drop(columns=["Genre"], inplace=True)  
fiction_df.to_csv(fiction_file, index=False)
non_fiction_df.drop(columns=["Genre"], inplace=True) 
non_fiction_df.to_csv(non_fiction_file, index=False)


fiction_df["Genre"] = "Fiction"
non_fiction_df["Genre"] = "Non-fiction"

merged_df = pd.concat([fiction_df, non_fiction_df], ignore_index=True)
merged_df.to_csv(merged_file, index=False)

# Function to group by Author and count appearances
def group_by_author(df):
    # Count occurrences by Author and Genre
    genre_counts = df.groupby(["Author", "Genre"]).size().reset_index(name="Count")
    # Assign the predominant genre for each author
    predominant_genre = genre_counts.loc[genre_counts.groupby("Author")["Count"].idxmax()][["Author", "Genre"]]
    # Total count for each author
    author_counts = df.groupby("Author").size().reset_index(name="Number of List Appearances - Author")
    author_counts = pd.merge(author_counts, predominant_genre, on="Author", how="left")
    return author_counts

# Function to group by Title and count appearances
def group_by_title(df):
    genre_counts = df.groupby(["Title", "Genre"]).size().reset_index(name="Count")
    predominant_genre = genre_counts.loc[genre_counts.groupby("Title")["Count"].idxmax()][["Title", "Genre"]]
    title_counts = df.groupby("Title").size().reset_index(name="Number of List Appearances - Book")
    title_counts = pd.merge(title_counts, predominant_genre, on="Title", how="left")
    return title_counts

# Group by Author and Title
author_counts = group_by_author(merged_df)
title_counts = group_by_title(merged_df)

# Save the grouped data to new CSV files
author_counts.to_csv(author_appearances_file, index=False)
title_counts.to_csv(book_appearances_file, index=False)

print(f"Data cleaning complete. Updated fiction and non-fiction files saved.")
print(f"Merged file saved as {merged_file}.")
print(f"Author appearances saved as {author_appearances_file}.")
print(f"Book appearances saved as {book_appearances_file}.")
