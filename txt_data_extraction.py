import os
import re
import csv
from datetime import datetime

input_dir = "nyt_bestsellers_txt"
fiction_output_file = "fiction_all.csv"
non_fiction_output_file = "non_fiction_all.csv"

# Initialize CSV files with headers
headers = ["Date", "Rank", "Title", "Author", "Publisher", "Description"]

# Write headers to the output files
with open(fiction_output_file, mode="w", newline="", encoding="utf-8") as fiction_csv, \
     open(non_fiction_output_file, mode="w", newline="", encoding="utf-8") as non_fiction_csv:
    fiction_writer = csv.writer(fiction_csv)
    non_fiction_writer = csv.writer(non_fiction_csv)
    fiction_writer.writerow(headers)
    non_fiction_writer.writerow(headers)

# Process each .txt file in the input directory
for filename in os.listdir(input_dir):
    if not filename.endswith(".txt"):
        continue  

    filepath = os.path.join(input_dir, filename)
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    # Check if the file has "no list published this week"
    if "no list published this week" in content.lower():
        print(f"Skipping file {filename} (no list published).")
        continue

    # Extract the date with flexible spacing
    date_match = re.search(r"This\s+Week\s+([A-Za-z]+)\s+(\d{1,2})\s*,?\s+(\d{4})", content)
    if not date_match:
        print(f"Date not found in file {filename}.")
        continue

    # Format the date as (month-day-year)
    try:
        date = f"{date_match.group(1)} {date_match.group(2)} {date_match.group(3)}"
        formatted_date = datetime.strptime(date, "%B %d %Y").strftime("%m-%d-%Y")
    except ValueError:
        print(f"Error parsing date in file {filename}: {date}")
        continue

    # Split content by fiction (first page) and non-fiction (second page)
    sections = content.split("Hawes Publications")
    if len(sections) < 3:
        print(f"Skipping file {filename} due to missing sections.")
        continue

    fiction_section = sections[1]
    non_fiction_section = sections[2]

    # Function to extract book data from a section
    def extract_books(section):
        books = []
        lines = section.strip().split("\n")
        current_rank, current_title, current_author, current_publisher, current_description = None, None, None, None, ""

        for i, line in enumerate(lines):
            # Match rank and title with flexible spacing
            rank_match = re.match(r"^\s*(\d+)\s+(.*)", line)
            if rank_match:
                if current_rank:  # Save previous book entry if a new rank starts
                    books.append([formatted_date, current_rank, current_title, current_author, current_publisher, current_description])
                current_rank = rank_match.group(1)
                book_info = rank_match.group(2).strip()

                # Match title and author
                title_author_match = re.match(r"(.*?),\s*by\s+(.*)", book_info)
                if title_author_match:
                    current_title = title_author_match.group(1).strip()
                    author_publisher = title_author_match.group(2).strip()
                    # Separate author and publisher
                    author_match = re.match(r"(.*?\.)\s*\(", author_publisher)
                    if author_match:
                        current_author = author_match.group(1).strip()
                        publisher_match = re.search(r"\(\s*(.*?)\s*\)", author_publisher)
                        if publisher_match:
                            current_publisher = publisher_match.group(1).strip()
                            # Include everything after the ")" as the description
                            description_start = author_publisher.find(")") + 1
                            current_description = author_publisher[description_start:].strip()

                            # Extend description to subsequent lines
                            for j in range(i + 1, len(lines)):
                                next_line = lines[j].strip()
                                if next_line == "" or re.match(r"^\d+\s", next_line):
                                    break 
                                current_description += f" {next_line.strip()}"
                        else:
                            current_publisher = None
                            current_description = ""
                    else:
                        current_author = author_publisher
                        current_publisher = None
                        current_description = ""
                else:
                    current_title, current_author, current_publisher, current_description = book_info.strip(), None, None, ""

        # Add the last book in the section
        if current_rank:
            books.append([formatted_date, current_rank, current_title, current_author, current_publisher, current_description])

        return books

    # Extract books from each section and write to the respective CSV file
    fiction_books = extract_books(fiction_section)
    non_fiction_books = extract_books(non_fiction_section)

    with open(fiction_output_file, mode="a", newline="", encoding="utf-8") as fiction_csv, \
         open(non_fiction_output_file, mode="a", newline="", encoding="utf-8") as non_fiction_csv:
        fiction_writer = csv.writer(fiction_csv)
        non_fiction_writer = csv.writer(non_fiction_csv)
        fiction_writer.writerows(fiction_books)
        non_fiction_writer.writerows(non_fiction_books)

    print(f"Processed file {filename}: {len(fiction_books)} fiction books, {len(non_fiction_books)} non-fiction books.")

print("Processing complete!")
