import spacy
from spacy.training.example import Example

# Load your best model
nlp = spacy.load("../output/model-best")

# Load your manually labelled test examples (JSONL, same format as training)
import json

test_texts = []
test_annotations = []

with open("../data/doccano_annotated.jsonl", encoding="utf-8") as f:
    for line in f:
        obj = json.loads(line)
        test_texts.append(obj["text"])
        test_annotations.append({"entities": obj["label"]})

# Create spaCy examples
examples = []
for text, ann in zip(test_texts, test_annotations):
    doc = nlp.make_doc(text)
    example = Example.from_dict(doc, ann)
    examples.append(example)

# Evaluate
results = nlp.evaluate(examples)
print("ENTS_F:", results["ents_f"])
print("ENTS_P:", results["ents_p"])
print("ENTS_R:", results["ents_r"])
print("Accuracy:", results["ents_f"])
