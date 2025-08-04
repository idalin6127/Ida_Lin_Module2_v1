import os
import json
import re
from langdetect import detect
from datasketch import MinHash, MinHashLSH
import nltk
nltk.download("punkt")  # 这个可以保留，其他地方可能还用到

# ------------------------
# Step 1: Load all sources
# ------------------------

def load_arxiv_json():
    if not os.path.exists("arxiv_clean.json"):
        return []
    with open("arxiv_clean.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        return [item["abstract"] for item in data if "abstract" in item]

def load_pdf_texts():
    texts = []
    if not os.path.exists("pdf_txts"):
        return texts
    for fname in os.listdir("pdf_txts"):
        if fname.endswith(".txt"):
            with open(os.path.join("pdf_txts", fname), "r", encoding="utf-8") as f:
                texts.append(f.read())
    return texts

def load_transcripts():
    texts = []
    if not os.path.exists("talks_transcripts.jsonl"):
        return texts
    with open("talks_transcripts.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            if "text" in item:
                texts.append(item["text"])
            elif "ocr_text" in item:
                texts.append(item["ocr_text"])
    return texts

# ------------------------
# Step 2: Cleaning helpers
# ------------------------

def is_english(text):
    try:
        return detect(text) == "en"
    except:
        return False

def remove_html(text):
    return re.sub(r"<[^>]+>", "", text)

def remove_pii(text):
    text = re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", "", text)  # emails
    text = re.sub(r"\b(?:\d[ -]*?){13,16}\b", "", text)  # credit cards
    text = re.sub(r"\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b", "", text)  # phone numbers
    return text

def remove_repeated_ngrams(text, n=4):
    words = text.split()
    seen = set()
    result = []
    i = 0
    while i <= len(words) - n:
        ngram = tuple(words[i:i + n])
        if ngram in seen:
            i += 1
            continue
        seen.add(ngram)
        result.append(words[i])
        i += 1
    result.extend(words[i:])  # add the rest
    return ' '.join(result)

def get_minhash(text):
    m = MinHash(num_perm=128)
    for token in text.split():
        m.update(token.encode("utf8"))
    return m

# ------------------------
# Step 3: Cleaning process
# ------------------------

def clean_and_deduplicate(text_list):
    lsh = MinHashLSH(threshold=0.7, num_perm=128)
    unique_texts = []
    seen_count = 0

    for i, raw in enumerate(text_list):
        text = raw.strip()
        if len(text) < 20:
            continue
        if not is_english(text):
            continue

        text = remove_html(text)
        text = remove_pii(text)
        text = remove_repeated_ngrams(text)

        mh = get_minhash(text)
        if not any(lsh.query(mh)):
            lsh.insert(f"t_{i}", mh)
            unique_texts.append(text)
        else:
            seen_count += 1

    return unique_texts, seen_count

# ------------------------
# Step 4: Save results
# ------------------------

def simple_tokenize(text):
    return text.split()

def save_texts(texts, path="clean_corpus.txt"):
    with open(path, "w", encoding="utf-8") as f:
        for line in texts:
            f.write(line.strip() + "\n")

def save_stats(raw_texts, cleaned_texts, removed_duplicates, path="stats.md"):
    raw_tokens = sum(len(simple_tokenize(t)) for t in raw_texts)
    clean_tokens = sum(len(simple_tokenize(t)) for t in cleaned_texts)
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Cleaning Report\n\n")
        f.write(f"- Total raw documents: {len(raw_texts)}\n")
        f.write(f"- Total cleaned documents: {len(cleaned_texts)}\n")
        f.write(f"- Duplicates removed: {removed_duplicates}\n")
        f.write(f"- Raw token count: {raw_tokens}\n")
        f.write(f"- Cleaned token count: {clean_tokens}\n")
        f.write(f"- Token reduction: {raw_tokens - clean_tokens} ({(raw_tokens - clean_tokens) / raw_tokens:.2%})\n")

# ------------------------
# Main execution
# ------------------------

if __name__ == "__main__":
    print("🔍 Loading raw data ...")
    all_texts = load_arxiv_json() + load_pdf_texts() + load_transcripts()
    print(f"📦 Loaded {len(all_texts)} raw text blocks.")

    print("🧹 Cleaning and deduplicating ...")
    cleaned_texts, removed_dups = clean_and_deduplicate(all_texts)
    print(f"✅ Final clean corpus size: {len(cleaned_texts)}")

    print("💾 Saving clean corpus and stats ...")
    save_texts(cleaned_texts)
    save_stats(all_texts, cleaned_texts, removed_dups)

    print("✅ Done! Outputs: clean_corpus.txt + stats.md")
