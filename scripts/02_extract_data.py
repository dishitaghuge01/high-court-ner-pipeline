import os
import pdfplumber
import json

# Paths
PDF_DIR = "../data/raw_pdfs/"
OUTPUT_JSONL = "../data/extracted_texts.jsonl"

# Prepare output
output = []

# Loop through all PDFs
for filename in os.listdir(PDF_DIR):
    if not filename.endswith(".pdf"):
        continue

    pdf_path = os.path.join(PDF_DIR, filename)

    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"

        output.append({
            "filename": filename,
            "text": text.strip()
        })

        print(f"[+] Extracted {filename}")

    except Exception as e:
        print(f"[!] Failed to extract {filename}: {e}")

# Write all to JSONL
with open(OUTPUT_JSONL, "w", encoding="utf-8") as f:
    for item in output:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"✅ Extracted {len(output)} files -> {OUTPUT_JSONL}")
