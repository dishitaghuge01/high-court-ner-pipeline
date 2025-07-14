# Model Configuration

This document outlines the spaCy model configuration used in the High Court Judgement NER pipeline, as defined in `config.cfg`.

## Model Architecture
The pipeline uses spaCy's transition-based Named Entity Recognition (NER) model with the following components:

- **Tok2Vec**: Token-to-vector embedding layer for contextual representations.
- **NER**: Transition-based parser for entity recognition.
- **Embeddings**: Multi-hash embeddings incorporating:
  - `NORM`: Normalized token text.
  - `PREFIX`: Token prefixes.
  - `SUFFIX`: Token suffixes.
  - `SHAPE`: Token shape (e.g., `XxXx` for mixed case).

## Training Configuration
Key training parameters in `config.cfg`:

- **Maximum Steps**: 20,000 steps with early stopping based on validation performance.
- **Optimizer**: Adam optimizer with gradient clipping.
- **Dropout**: 0.1 to prevent overfitting.
- **Learning Rate**: 0.001 for stable convergence.

## Hyperparameters
The following hyperparameters are defined in `config.cfg`:

- **Hidden Width**: 64 (size of hidden layers in the NER model).
- **Tok2Vec Width**: 96 (size of token embeddings).
- **Batch Size**: Dynamic batching with compounding sizes.
- **Validation Frequency**: Evaluate every 200 steps.

## Example Configuration
Below is a simplified excerpt from `config.cfg`:

```ini
[training]
max_steps = 20000
patience = 1600
eval_frequency = 200
dropout = 0.1

[nlp]
pipeline = ["tok2vec", "ner"]

[components.tok2vec]
factory = "tok2vec"
width = 96

[components.ner]
factory = "ner"
hidden_width = 64

[optimizer]
@optimizers = "Adam.v1"
learn_rate = 0.001
```

## Modifying the Configuration
To experiment with different settings, edit `config.cfg`:

- **Embedding Dimensions**: Adjust `width` in `[components.tok2vec]` for larger or smaller embeddings.
- **Architecture**: Replace `tok2vec` with alternatives like `transformer` for transformer-based models (requires additional dependencies).
- **Hyperparameters**: Tune `learn_rate`, `dropout`, or `max_steps` for better convergence.
- **Training Schedule**: Modify `patience` or `eval_frequency` for early stopping behavior.

## Notes
- Ensure sufficient training data (>100 annotated examples) for stable convergence.
- Monitor class imbalance, as some entities (e.g., `ORDER_DATE`) may be more frequent than others.
- For large datasets, consider gradient accumulation to manage memory usage.