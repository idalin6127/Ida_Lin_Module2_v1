import os
import json
import requests
from pdf2image import convert_from_path
from PIL import Image
import pytesseract

# ---------- Step 0: Set the path and configuration ----------
# Set the path of tesseract.exe (required only for Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# If you haven't set the Poppler environment variable, manually specify the path (Windows)
POPPLER_PATH = r"C:\Users\idali\Downloads\poppler-24.08.0\Library\bin"  # Modify it to your poppler decompression path

# Create an output folder
os.makedirs("pdfs", exist_ok=True)
os.makedirs("pdf_ocr", exist_ok=True)

# ---------- Step 1: Load the paper link from the JSON file ----------
with open("arxiv_clean.json", "r", encoding="utf-8") as f:
    papers = json.load(f)

# ---------- Step 2: Download the PDF file ----------
for paper in papers:
    arxiv_id = paper["url"].split("/")[-1]  # Extract the ID, such as "2408.01234"
    pdf_path = f"pdfs/{arxiv_id}.pdf"

    if not os.path.exists(pdf_path):
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        try:
            response = requests.get(pdf_url)
            with open(pdf_path, "wb") as f:
                f.write(response.content)
            print(f"✅ PDF download successfully: {arxiv_id}")
        except Exception as e:
            print(f"❌ PDF download failed: {arxiv_id} -> {e}")

# ---------- Step 3: Batch convert PDFs to images and extract text through OCR ----------
for paper in papers:
    arxiv_id = paper["url"].split("/")[-1]
    pdf_file = f"pdfs/{arxiv_id}.pdf"
    txt_file = f"pdf_ocr/{arxiv_id}.txt"

    if not os.path.exists(pdf_file):
        print(f"⚠️ Skip the PDF that has not been downloaded: {arxiv_id}")
        continue

    if os.path.exists(txt_file):
        print(f"⏩ Processed. Skip: {arxiv_id}")
        continue

    try:
        # Step 3.1: PDF to Image (one page per page)
        images = convert_from_path(pdf_file, dpi=300, poppler_path=POPPLER_PATH)

        # Step 3.2: Perform OCR on each page
        ocr_text = ""
        for i, image in enumerate(images):
            page_text = pytesseract.image_to_string(image, config="--psm 6")
            ocr_text += f"\n\n--- Page {i+1} ---\n\n" + page_text

        # Step 4: Save as a TXT file
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write(ocr_text)
        print(f"✅ OCR Completed: {arxiv_id}")
    except Exception as e:
        print(f"❌ OCR Failed: {arxiv_id} -> {e}")
