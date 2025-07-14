# High Court Judgement NER Pipeline

A pipeline for extracting and training Named Entity Recognition (NER) models for High Court judgements using spaCy and Doccano. This project automates the workflow from downloading PDF judgements to training production-ready NER models.

**TL;DR**: Download High Court judgement PDFs, extract and clean text, annotate entities with Doccano, and train a spaCy NER model. Run `scripts/01_download_pdfs.py` to `06_evaluate_model.py` in sequence after setting up `data/input_urls.csv`.

## Features
- **Automated PDF Download**: Batch download judgement PDFs from URLs.
- **Text Extraction**: Extract and clean text from legal documents.
- **OCR Artifact Cleaning**: Handle common PDF extraction issues (e.g., character repetition, digit corruption).
- **Manual Annotation**: Use Doccano for efficient entity annotation.
- **Custom NER Training**: Train spaCy models for legal entities.
- **Model Evaluation**: Generate precision, recall, and F1-score metrics.

## Project Structure
```
data_extraction/
│
├── data/
│   ├── input_urls.csv           # CSV with PDF URLs and metadata
│   ├── raw_pdfs/                # Downloaded PDF files
│   ├── extracted_texts.jsonl    # Raw extracted text
│   ├── cleaned_texts.jsonl      # Cleaned text
│   ├── doccano_input.jsonl      # Data for Doccano annotation
│   ├── doccano_annotated.jsonl  # Annotated training data
│   ├── train.spacy              # spaCy binary training format
│
├── scripts/
│   ├── 01_download_pdfs.py      # Download PDFs
│   ├── 02_extract_text.py       # Extract text using pdfplumber
│   ├── 03_clean_texts.py        # Clean and normalize text
│   ├── 04_prepare_for_doccano.py# Prepare data for Doccano
│   ├── 05_prepare_spacy.py      # Convert annotations to spaCy format
│   ├── 06_evaluate_model.py     # Evaluate model performance
│   ├── 07_test.py               # Test the model
│   ├── config.cfg               # spaCy training configuration
│
├── output/
│   ├── model-best/              # Best trained model
│   ├── model-last/              # Latest model checkpoint
│
├── docs/
│   ├── text_cleaning.md         # Text cleaning details
│   ├── model_config.md          # Model configuration details
│   ├── customization.md         # Customization instructions
│
├── requirements.txt             # Python dependencies
├── LICENSE                      # MIT License
└── README.md                    # This file
```

## Installation

### Setup
1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd data_extraction
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create required directories:
   ```bash
   mkdir -p data/raw_pdfs output
   ```

## Usage

### Step 1: Prepare Input Data
Create `data/input_urls.csv` with High Court judgement PDF URLs:
```csv
cnr_number,order_details
HC001,https://example.com/hc_judgement_1.pdf
HC002,https://example.com/hc_judgement_2.pdf
```

### Step 2: Run the Pipeline
From the `scripts/` directory, run:
```bash
python 01_download_pdfs.py
python 02_extract_text.py
python 03_clean_texts.py
python 04_prepare_for_doccano.py
```

### Step 3: Annotate Data with Doccano
1. Install and run Doccano:
   ```bash
   pip install doccano
   doccano init
   doccano createuser --username admin --password admin
   doccano runserver --port 8000
   ```
2. Open `http://localhost:8000` in your browser and log in (username: admin, password: admin).
3. Create a "Sequence Labeling" project and define labels: PETITIONER, RESPONDENT, CORAM, ORDER_DATE.
4. Upload `data/doccano_input.jsonl` to the project.
5. Annotate entities by highlighting text and assigning labels.
6. Export annotated data as `data/doccano_annotated.jsonl`.
   For detailed instructions, see the [Doccano Documentation](https://doccano.github.io/doccano/).

### Step 4: Train and Evaluate the Model
```bash
python 05_prepare_spacy.py
python -m spacy train config.cfg --output ../output --paths.train ../data/train.spacy --paths.dev ../data/train.spacy
python 06_evaluate_model.py
```

## Example Output
**Input Text**: "The High Court of Delhi, presided by Hon'ble Justice A.K. Singh, issued an order on 15th March 2023 in the case of John Doe vs. State of Delhi."

**NER Output**:
| Entity        | Value                     |
|---------------|---------------------------|
| PETITIONER    | John Doe                  |
| RESPONDENT    | State of Delhi            |
| CORAM         | Hon'ble Justice A.K. Singh|
| ORDER_DATE    | 15th March 2023          |

## Entity Types
| Entity        | Description                            |
|---------------|----------------------------------------|
| PETITIONER    | Names and details of petitioning parties |
| RESPONDENT    | Names and details of responding parties |
| CORAM         | Names of judges hearing the case       |
| ORDER_DATE    | Dates when orders were issued          |

## Evaluation Metrics
The `06_evaluate_model.py` script provides:
- Precision: Accuracy of predicted entities
- Recall: Coverage of actual entities
- F1-Score: Harmonic mean of precision and recall
- Per-entity metrics: Performance breakdown by entity type

## Advanced Configuration
For details on text cleaning, model configuration, and customization, see the [Documentation](docs/).

## Troubleshooting
- **PDF Download Failures**:
  - Check URL accessibility and network connectivity.
  - Verify SSL certificates for HTTPS URLs.
  - Add retry logic in `01_download_pdfs.py`.
- **Text Extraction Issues**:
  - Image-based PDFs may require OCR.
  - Handle password-protected PDFs separately.
  - Review complex layouts manually.
- **Training Convergence**:
  - Ensure sufficient training data (>100 examples).
  - Maintain consistent annotation guidelines.
  - Address class imbalance.
- **Memory Issues**:
  - Reduce batch size in `config.cfg`.
  - Process documents in smaller batches.
  - Use gradient accumulation.

## Data Privacy Note
This pipeline processes High Court judgements, which may contain sensitive personal or legal information. Ensure compliance with relevant data protection regulations (e.g., GDPR, local privacy laws) and implement security measures (e.g., encryption, access controls) when handling court documents.

## Resources
- [spaCy Documentation](https://spacy.io/usage)
- [Doccano Documentation](https://doccano.github.io/doccano/)
- [Python 3.8+ Installation](https://www.python.org/downloads/)

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```