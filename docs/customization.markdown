# Customization Instructions

This document provides guidance on customizing the High Court Judgement NER pipeline, including text cleaning and model architecture.

## Modifying Text Cleaning
To add domain-specific cleaning rules, edit the `clean_text` function in `03_clean_texts.py`. For example:

```python
def clean_text(text):
    # Existing cleaning rules
    text = re.sub(r'(.)\1{2,}', r'\1', text)  # Remove character repetition
    # Add custom rule for specific legal terms
    text = re.sub(r'your_pattern', 'replacement', text)
    return text
```

### Tips for Custom Cleaning
- **Test Incrementally**: Apply new rules to a small subset of data to ensure they work as expected.
- **Preserve Meaning**: Avoid removing critical legal terms or punctuation.
- **Log Changes**: Document custom rules for reproducibility.

## Adjusting Model Architecture
To modify the spaCy model, edit `config.cfg`:

- **Embedding Dimensions**: Increase `width` in `[components.tok2vec]` for richer embeddings (e.g., `width = 128`).
- **Alternative Architectures**: Replace `tok2vec` with `transformer` for transformer-based models (requires `spacy-transformers`).
- **Hyperparameter Tuning**:
  - Adjust `learn_rate` (e.g., `0.0005`) for slower, more stable training.
  - Increase `dropout` (e.g., `0.2`) to reduce overfitting.
  - Modify `max_steps` (e.g., `30000`) for longer training.
- **Training Schedule**: Adjust `patience` or `eval_frequency` for early stopping.

### Example Modification
To use a transformer-based model:

```ini
[components.tok2vec]
factory = "transformer"
model_name = "roberta-base"
```

Install required dependencies:

```bash
pip install spacy-transformers
```

## Adding New Entity Types
To include additional entities (e.g., `CASE_NUMBER`):

1. Update Doccano labels in the "Sequence Labeling" project to include the new entity.
2. Re-annotate data to label the new entity.
3. Update `config.cfg` to include the new entity in `[components.ner.labels]`.
4. Retrain the model using:

```bash
python -m spacy train config.cfg --output ../output --paths.train ../data/train.spacy --paths.dev ../data/train.spacy
```

## Troubleshooting Customization
- **Cleaning Errors**: If custom rules remove valid content, use more specific regex patterns.
- **Training Failures**: Check for sufficient training data and consistent annotations.
- **Memory Issues**: Reduce batch size or use gradient accumulation in `config.cfg`.

## Resources
- [spaCy Configuration Guide](https://spacy.io/usage/training#config)
- [Regular Expression Tutorial](https://docs.python.org/3/library/re.html)