# arxiv_scraper.py

from bs4 import BeautifulSoup
import requests
import trafilatura
from PIL import Image
import pytesseract
import time
import json
from selenium import webdriver

# Step 1: Get the /abs/ page link
category = "cs.CL"
url = f"https://arxiv.org/list/{category}/recent"
resp = requests.get(url)
soup = BeautifulSoup(resp.text, "html.parser")

abs_links = ["https://arxiv.org" + a['href'] for a in soup.select("dt a[href^='/abs/']")]
abs_links = list(dict.fromkeys(abs_links))  # duplicate removal
abs_links = abs_links[:200]  # The limit is up to 200

# Step 2: Extract structured information + Clean the summary with Trafilatura (standby)
all_data = []
for link in abs_links:
    paper = {}
    paper['url'] = link
    html = requests.get(link).text
    soup = BeautifulSoup(html, "html.parser")

    # Extract title, authors, date
    paper['title'] = soup.find("h1", class_="title").text.replace("Title:", "").strip()
    paper['authors'] = [a.text.strip() for a in soup.select("div.authors a")]
    dateline = soup.find("div", class_="dateline")
    paper['date'] = dateline.text.replace("Submitted on", "").strip() if dateline else "N/A"

    # Try to extract the summary (using Trafilatura)
    extracted = trafilatura.extract(html)
    paper['abstract'] = extracted if extracted else ""

    all_data.append(paper)

# Step 3: - Perform OCR on the abstract using Selenium + pytesseract
    driver = webdriver.Chrome()
    for idx, paper in enumerate(all_data):
        driver.get(paper['url'])
        time.sleep(2)
        driver.save_screenshot("page.png")
        image = Image.open("page.png")
        ocr_text = pytesseract.image_to_string(image)
        paper['abstract'] = ocr_text
    driver.quit()

# Step 4: Save as a JSON file
with open("arxiv_clean.json", "w", encoding="utf-8") as f: 
    json.dump(all_data, f, indent=2, ensure_ascii=False)
