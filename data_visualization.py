import pandas as pd
import plotly.graph_objects as go

# Load the merged data
merged_data = pd.read_csv("merged_genres.csv")

# Count the appearances for authors and books, including genres
author_counts = (
    merged_data.groupby(["Author", "Genre"])
    .size()
    .reset_index(name="Number of List Appearances")
    .sort_values(by="Number of List Appearances", ascending=False)  
    .head(20)  
)

book_counts = (
    merged_data.groupby(["Title", "Genre"])
    .size()
    .reset_index(name="Number of List Appearances")
    .sort_values(by="Number of List Appearances", ascending=False)  
    .head(20)  
)

# Color Scales
def color_scale(df, genre_col="Genre", value_col="Number of List Appearances"):
    colors = []
    max_appearances = df[value_col].max()
    for _, row in df.iterrows():
        intensity = row[value_col] / max_appearances
        if row[genre_col] == "Fiction":
            colors.append(f"rgba({255 * intensity}, 0, 0, 1)")  # Red gradient
        else:
            colors.append(f"rgba(0, {255 * intensity}, 0, 1)")  # Green gradient
    return colors

author_colors = color_scale(author_counts)
book_colors = color_scale(book_counts)

# Bar Chart for Top 20 Authors
fig_authors = go.Figure()
fig_authors.add_trace(go.Bar(
    x=author_counts["Number of List Appearances"],
    y=author_counts["Author"],
    orientation='h',
    marker=dict(color=author_colors),
    text=author_counts["Genre"],  
    hovertemplate='<b>Author</b>: %{y}<br><b>Appearances</b>: %{x}<br><b>Genre</b>: %{text}'
))

fig_authors.update_layout(
    title="Top 20 Authors by Number of List Appearances",
    xaxis_title="List Appearances",
    yaxis_title="Authors",
    yaxis=dict(autorange="reversed"),  
    annotations=[
        dict(
            x=1.05,
            y=0.95,
            xref="paper",
            yref="paper",
            text=f"<b>Fiction:</b> {sum(author_counts['Genre'] == 'Fiction')}/20<br><b>Non-fiction:</b> {sum(author_counts['Genre'] == 'Non-fiction')}/20",
            showarrow=False,
            align="left",
            font=dict(size=12),
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor="black",
            borderwidth=1,
        )
    ],
    margin=dict(r=150)  
)

# Save authors chart to HTML
fig_authors.write_html("authors.html")
fig_authors.show()

# Bar Chart for Top 20 Books
fig_books = go.Figure()
fig_books.add_trace(go.Bar(
    x=book_counts["Number of List Appearances"],
    y=book_counts["Title"],
    orientation='h',
    marker=dict(color=book_colors),
    text=book_counts["Genre"],  
    hovertemplate='<b>Book</b>: %{y}<br><b>Appearances</b>: %{x}<br><b>Genre</b>: %{text}'
))

fig_books.update_layout(
    title="Top 20 Books by Number of List Appearances",
    xaxis_title="List Appearances",
    yaxis_title="Books",
    yaxis=dict(autorange="reversed"),
    annotations=[
        dict(
            x=1.05,
            y=0.95,
            xref="paper",
            yref="paper",
            text=f"<b>Fiction:</b> {sum(book_counts['Genre'] == 'Fiction')}/20<br><b>Non-fiction:</b> {sum(book_counts['Genre'] == 'Non-fiction')}/20",
            showarrow=False,
            align="left",
            font=dict(size=12),
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor="black",
            borderwidth=1,
        )
    ],
    margin=dict(r=150)
)

# Save books chart to HTML
fig_books.write_html("books.html")
fig_books.show()
