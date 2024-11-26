# NYT Bestseller Books from 1931-2024


## Executive Summary

This project creates and provides in tabular form a complete list of books from the **New York Times Bestseller Lists** (1931–2024) in the Fiction and Non-fiction categories. The motivation for this project was curiousity. As a reader I wanted to see historic bestseller trends and also identify how many of the bestseller books I have read and which authors consistently appear on the NYT list. I also think this project provides a good oppurtunity for literary research in the future.

The scraping and analysis was conducted using Python scripts to extract, clean and process data from PDFs available on Hawes.com from Hawes Publications

## Description of Data

- **Fiction Data (`fiction_all.csv`)**:
  - Contains bestseller data for books in the Fiction category.
  - Columns: `Date`, `Rank`, `Title`, `Author`, `Publisher`, `Description`, and `Genre`.

- **Non-fiction Data (`non_fiction_all.csv`)**:
  - Contains bestseller data for books in the Non-fiction category.
  - Columns: Same as Fiction data.

- **Merged Data (`merged_genres.csv`)**:
  - Combines Fiction and Non-fiction datasets with a `Genre` column to identify the category of each book.

- **Author Appearance Data (`author_appearances.csv`)**:
  - Groups data by authors, with a count of the number of times each author appeared on the list and their dominant genre.

- **Book Appearance Data (`book_appearances.csv`)**:
  - Groups data by book titles, with a count of the number of times each book appeared on the list and its associated genre.

## Power Analysis Results

A power analysis was not applicable for my project because it does not involve hypothesis testing or sampling methodologies requiring statistical power computations.

## Exploratory Data Analysis

### Top 20 Authors by Number of List Appearances
- A bar chart visualization highlights the most frequently appearing authors.
- **Key Insight**: Fiction authors dominate this category, with 18 out of 20 authors classified as Fiction. Danielle Steel and Stephen King were  the two most frequent to appear. I would hyptohesize fiction authors appeared the most because they often create series with strong fanbase retention that would push multiple books to be bestsellers over multiple weeks.

### Top 20 Books by Number of List Appearances
- A bar chart visualization displays the most frequently appearing books.
- **Key Insight**: Non-fiction books are more frequent in this category, with 13 out of 20 entries being Non-fiction. Books turned movies like *Tuesdays with Morrie* and *Unbroken* are at the top of list longevity. It is certainly interesting that more non-fiction books are able to last on the list for more weeks considering fiction author's dominance over total weeks on the bestseller lists.

The bar chart visualizations are saved as interactive HTML files (`authors.html` and `books.html`) and can be found in this repository.

## Link to Code Repository

All scripts for data cleaning, preprocessing, and visualization are publicly available in the GitHub repository:
[https://github.com/breese5/NYTBestseller1931-2024](https://github.com/breese5/NYTBestseller1931-2024)

## Ethics Statement

This dataset and analysis were developed for educational and exploratory purposes. While efforts were made to ensure the accuracy of the data, there may be inconsistencies introduced during preprocessing or due to the nature of scraping from PDF turned TXT files. Some additional cleaning manual cleaning to clear out some abnormal spacing could better the dataset however this was difficult given the size.

The dataset:
-Reflects historical bestseller lists, so is not representative of the "best" books necesarily btu is a matter of opinion.


## Open Source License

This dataset and all associated scripts are released under the **MIT License**, allowing for open use, modification, and sharing with proper attribution.



