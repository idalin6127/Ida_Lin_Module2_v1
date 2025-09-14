# Week 2 – Data Collection & Extraction

## 🚀 Quick Summary
Hands-on project for **data collection & extraction**.  
Built an **end-to-end pipeline** integrating OCR (Tesseract), Web Scraping, PDF OCR, and ASR (Whisper).  
Delivered cleaned and deduplicated datasets (JSON, JSONL, TXT).  
Demonstrates skills in **Python data engineering, NLP preprocessing, and multi-modal information extraction**.

---

## 📖 Project Description
This project is the **Hands-on Assignment for Module 2**, focusing on **data collection, OCR text extraction, speech recognition, and data cleaning**.  
It builds a complete pipeline covering **web scraping → PDF OCR → audio transcription → dataset cleaning & deduplication**, integrating multiple tools to extract and refine information from heterogeneous sources.

---

## 🎯 Objectives
1. **Web Scraping & Cleaning**  
   - Scrape arXiv subcategories (e.g., `cs.CL`) for the latest papers.  
   - Use Trafilatura to clean HTML content.  
   - Apply Tesseract OCR to extract abstracts from screenshots.  

2. **PDF → Text OCR**  
   - Batch convert arXiv PDFs to text.  
   - Use `pdf2image` + `pytesseract` to retain document structure (titles, sections).  

3. **Automatic Speech Recognition (ASR)**  
   - Download ~10 NLP conference talks (~3 min each) via `yt-dlp`.  
   - Transcribe using OpenAI Whisper.  
   - Save transcripts in `.jsonl` format with timestamps.  

4. **Data Cleaning & Deduplication**  
   - Merge outputs from Tasks 1–3 into a single dataset.  
   - Steps include: language detection → HTML noise removal → MinHash deduplication (similarity ≥ 0.7) → PII removal (emails, credit cards, phone numbers) → repetitive n-gram filtering.  

---

## 🛠️ Tech Stack
- **OCR**: Tesseract, pytesseract, pdf2image  
- **Web Scraping**: Trafilatura, BeautifulSoup  
- **ASR**: Whisper, yt-dlp  
- **Data Cleaning**: langdetect, datasketch (MinHash), regex for PII removal  

---

## 🔥 Architecture / Workflow Diagram 
flowchart LR
  A[arXiv pages/PDFs/YouTube audio] --> B[Scrape/Capture]
  B --> C[OCR (PDF/images)]
  B --> D[ASR (Whisper)]
  C --> E[Cleaning/PII removal]
  D --> E
  E --> F[MinHash Dedup]
  F --> G[Unified Clean Corpus (JSON/JSONL/TXT)]

---

## 📂 Deliverables
- `arxiv_clean.json`: cleaned abstract dataset  
- `pdf_ocr/`: batch OCR outputs from arXiv PDFs  
- `talks_transcripts.jsonl`: ASR transcripts with timestamps  
- `clean_corpus.txt` + `stats.md`: final cleaned corpus and dataset statistics (token counts, removal percentages, etc.)  

---


## 🔥 How to Run / Quick Start 
pip install -r requirements.txt
python scrape_arxiv.py --category cs.CL --out arxiv_raw.json
python ocr_pdfs.py --in ./pdfs --out ./pdf_ocr
python transcribe_whisper.py --urls urls.txt --out talks_transcripts.jsonl
python clean_merge.py --abstracts arxiv_raw.json --pdf ./pdf_ocr --asr talks_transcripts.jsonl --out clean_corpus.txt

---

## 🌟 Highlights
- Built an **end-to-end data processing pipeline**.  
- Combined **OCR + ASR + Web Scraping + Data Cleaning** in one workflow.  
- Handled **multi-modal data** (web pages, PDFs, audio → unified text corpus).  
- Applied **deduplication & privacy protection (PII removal)** to ensure quality and compliance.  

---

## 🚀 Skills Demonstrated
- Proficiency in **multi-modal data processing & extraction**.  
- Ability to **design pipelines** that combine collection, transformation, and cleaning.  
- Solid understanding of **Python data engineering ecosystem**.  
- Experience with **real-world data preprocessing and NLP workflows**.  

---

## 🚀 Future Improvements
Better layout OCR；speaker diarization；language ID improvements；heuristics/rules for domain filtering。

---
