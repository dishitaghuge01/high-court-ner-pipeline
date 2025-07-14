import pandas as pd
import requests
import os

# Paths
INPUT_CSV = "../data/input_urls.csv"
OUTPUT_DIR = "../data/raw_pdfs/"

# Create output folder if not exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load CSV
df = pd.read_csv(INPUT_CSV)

# Loop through rows
for idx, row in df.iterrows():
    url = row["order_details"]
    cnr = row["cnr_number"]

    if pd.isna(url):
        print(f"[!] Missing URL for row {idx}. Skipping.")
        continue

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        pdf_path = os.path.join(OUTPUT_DIR, f"{cnr}.pdf")
        with open(pdf_path, "wb") as f:
            f.write(response.content)

        print(f"[+] Downloaded {pdf_path}")

    except Exception as e:
        print(f"[!] Failed to download {url}: {e}")
