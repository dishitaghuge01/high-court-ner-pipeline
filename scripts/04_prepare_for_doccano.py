import json

input_path = "../data/cleaned_texts.jsonl"
output_path = "../data/doccano_input.jsonl"

with open(input_path, "r", encoding="utf-8") as f_in, open(output_path, "w", encoding="utf-8") as f_out:
    for line in f_in:
        obj = json.loads(line)
        text = obj["text"]
        doccano_record = {
            "text": text,
            "label": []  # keep empty for manual or semi-auto labeling
        }
        f_out.write(json.dumps(doccano_record, ensure_ascii=False) + "\n")

print(f"✅ Doccano-ready JSONL created at {output_path}")
