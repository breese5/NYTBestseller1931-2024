import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# Base URL for NYT Bestseller archives
BASE_URL = "http://www.hawes.com"

# Directory to store the downloaded PDFs
PDF_DIR = "nyt_bestsellers_pdfs"
os.makedirs(PDF_DIR, exist_ok=True)

def download_pdfs():
    # Fetch the main archive page
    response = requests.get(f"{BASE_URL}/pastlist.htm")
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find links to year-specific pages
    year_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith("19") or a['href'].startswith("20")]

    for year_link in tqdm(year_links, desc="Processing Years"):
        year_url = f"{BASE_URL}/{year_link}"
        year_response = requests.get(year_url)
        year_soup = BeautifulSoup(year_response.text, 'html.parser')

        # Find links to weekly PDFs for the year
        week_links = [a['href'] for a in year_soup.find_all('a', href=True) if a['href'].endswith(".pdf")]

        for week_link in tqdm(week_links, desc=f"Processing {year_link.split('/')[0]}"):
            pdf_url = f"{BASE_URL}/{week_link}"
            pdf_name = week_link.split('/')[-1]
            pdf_path = os.path.join(PDF_DIR, pdf_name)

            # Skip download if the file already exists
            if not os.path.exists(pdf_path):
                try:
                    pdf_response = requests.get(pdf_url, stream=True)
                    with open(pdf_path, 'wb') as f:
                        for chunk in pdf_response.iter_content(chunk_size=1024):
                            f.write(chunk)
                except Exception as e:
                    print(f"Failed to download {pdf_url}: {e}")

if __name__ == "__main__":
    download_pdfs()
