# Text Cleaning Pipeline

This document details the text cleaning process implemented in `03_clean_texts.py` to handle common issues in text extracted from High Court judgement PDFs, such as OCR artifacts and formatting inconsistencies.

## Cleaning Features
The cleaning pipeline addresses the following issues:

- **Character Repetition**: Removes repeated characters (e.g., `HHHIIIGGGHHH` → `HIGH`).
- **Digit Corruption**: Corrects distorted numbers (e.g., `222000000888` → `2008`).
- **Ordinal Fixes**: Normalizes ordinal numbers (e.g., `111ST` → `11th`, `222ND` → `22nd`).
- **Page Number Removal**: Eliminates page number artifacts (e.g., `Page X/Y`).
- **Punctuation Normalization**: Cleans repeated punctuation (e.g., multiple dots, dashes, or colons).
- **Whitespace Collapse**: Normalizes excessive or irregular spacing.

## Implementation Details
The `03_clean_texts.py` script applies a series of regular expressions and string processing techniques to clean the extracted text. Below is an example of the cleaning logic:

```python
import re

def clean_text(text):
    # Remove character repetition (e.g., HHHIIIGGGHHH → HIGH)
    text = re.sub(r'(.)\1{2,}', r'\1', text)
    
    # Fix digit corruption (e.g., 222000000888 → 2008)
    text = re.sub(r'(\d)\1{2,}(\d+)', r'\1\2', text)
    
    # Normalize ordinals (e.g., 111ST → 11th)
    text = re.sub(r'(\d+)(ST|ND|RD|TH)', lambda m: m.group(1) + {'ST': 'st', 'ND': 'nd', 'RD': 'rd', 'TH': 'th'}[m.group(2)], text, flags=re.IGNORECASE)
    
    # Remove page numbers (e.g., Page 1/10)
    text = re.sub(r'Page\s+\d+/\d+', '', text, flags=re.IGNORECASE)
    
    # Normalize punctuation
    text = re.sub(r'[.-:]{2,}', r'\1', text)
    
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
```

## Adding Custom Cleaning Rules
To add domain-specific cleaning rules, modify the `clean_text` function in `03_clean_texts.py`. For example:

```python
def clean_text(text):
    # Existing cleaning rules (as above)
    # Add custom rule for specific legal terms
    text = re.sub(r'your_pattern', 'replacement', text)
    return text
```

## Notes
- Ensure cleaning rules do not inadvertently remove meaningful content (e.g., legal terms or specific punctuation).
- Test custom rules on a small subset of data to verify correctness.
- For complex PDFs (e.g., image-based or heavily formatted), consider integrating OCR tools like Tesseract for improved text extraction.