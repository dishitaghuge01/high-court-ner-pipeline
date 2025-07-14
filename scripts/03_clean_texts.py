import re
import json

INPUT_FILE = "../data/extracted_texts.jsonl"
OUTPUT_FILE = "../data/cleaned_texts.jsonl"

def clean_text(text):
    # 1️⃣ Fix repeated letters like 'HHHIIIGGGHHH'
    text = re.sub(r'([A-Z])\1{2,}', r'\1', text, flags=re.IGNORECASE)

    # 2️⃣ Collapse digit repeats like '222000000888' → try '2008'
    text = re.sub(r'2{2,}0{4,}8{2,}', '2008', text)  # adjust pattern if needed
    text = re.sub(r'2{2,}0{4,}7{2,}', '2007', text)
    text = re.sub(r'2{2,}0{4,}6{2,}', '2006', text)

    # 3️⃣ Fix ordinal suffix: 111ST → 11th, 222ND → 22nd, etc.
    text = re.sub(r'\b1{2,}ST\b', '11th', text)
    text = re.sub(r'\b2{2,}ND\b', '22nd', text)
    text = re.sub(r'\b3{2,}RD\b', '33rd', text)

    # Generic: Convert 111ST, 222ND to digits + suffix:
    text = re.sub(r'\b1+ST\b', '1st', text)
    text = re.sub(r'\b2+ND\b', '2nd', text)
    text = re.sub(r'\b3+RD\b', '3rd', text)
    text = re.sub(r'\b(\d)TH\b', r'\1th', text, flags=re.IGNORECASE)

    # 4️⃣ Remove page numbers
    text = re.sub(r'Page \d+/\d+', '', text, flags=re.IGNORECASE)

    # 5️⃣ Remove long lines of dots or dashes
    text = re.sub(r'\.{2,}', '', text)
    text = re.sub(r'[-=]{2,}', '', text)

    # 6️⃣ Remove weird colon blocks like ::: or ,,,
    text = re.sub(r':{2,}', ':', text)
    text = re.sub(r',,{2,}', ',', text)

    # 7️⃣ Collapse whitespace
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

with open(INPUT_FILE, "r", encoding="utf-8") as f_in, open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:
    for line in f_in:
        obj = json.loads(line)
        cleaned = clean_text(obj["text"])
        f_out.write(json.dumps({"filename": obj["filename"], "text": cleaned}, ensure_ascii=False) + "\n")

print(f"✅ Cleaned texts saved to {OUTPUT_FILE}")
