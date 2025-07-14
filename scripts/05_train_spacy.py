# 05_train_spacy.py

import spacy
from spacy.tokens import DocBin
import json

# Input & output
input_path = "../data/doccano_annotated.jsonl"
output_dir = "../output"
model_name = "custom_legal_ner"

# Load data
docs = []
nlp = spacy.blank("en")

with open(input_path, "r", encoding="utf-8") as f:
    for line in f:
        example = json.loads(line)
        text = example["text"]
        ents = []
        for start, end, label in example["label"]:
            ents.append((start, end, label))
        doc = nlp.make_doc(text)
        ents_in_doc = []
        for start, end, label in ents:
            span = doc.char_span(start, end, label=label)
            if span is None:
                print(f"Skipping bad span: {start}-{end} in: {text[start:end]}")
            else:
                ents_in_doc.append(span)
        doc.ents = ents_in_doc
        docs.append(doc)

# Serialize to spaCy binary
db = DocBin(docs=docs)
db.to_disk("../data/train.spacy")

print("✅ Training data saved to data/train.spacy")
