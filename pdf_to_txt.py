from PyPDF2 import PdfReader
import os

def extract_text_from_pdf(pdf_path, output_folder):
    """
    Extract text from a PDF file and save it as a .txt file in the output folder.
    """
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    
    # Create a .txt file
    base_name = os.path.basename(pdf_path).replace(".pdf", ".txt")
    output_path = os.path.join(output_folder, base_name)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

# Define paths
pdf_folder = "nyt_bestsellers_pdfs" 
output_folder = "nyt_bestsellers_txt"  
os.makedirs(output_folder, exist_ok=True) 

# Extract text from each PDF in the folder
for pdf_file in os.listdir(pdf_folder):
    if pdf_file.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, pdf_file)
        extract_text_from_pdf(pdf_path, output_folder)

print(f"Text extracted and saved to {output_folder}")
