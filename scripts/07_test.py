import spacy

# Load your custom trained model
nlp = spacy.load("../output/model-best")

# Your test text — wrapped in triple quotes for multi-line safety
text = """
IN THE HIGH COURT OF JUDICATURE AT BOMBAY ORDINARY ORIGINAL CIVIL JURISDICTION WRIT PETITION NO 111333888333 OF 2008 J. Sivashankar & Anr. Petitioners versus State of Maharashtra & Ors. Respondents Mr. R. G. Panchal i/b/ Mr. N. Bhojane for the Petitioners. CORAM : SB MHASE & AA KUMBHAKONI, J DATE : 20TH JUNE, 2008 PC . Petitioners by this petition are seeking an order to set aside the Recovery Certificates issued by the Respondent No.2. However, the impugned certificates are not annexed to the petition. Petitioners are hereby directed to produce the impugned certificates within a period of two weeks. Adjourned for two weeks. (((A A KUMBHAKONI, J))) (((S B MHASE, J)))
"""

# Process the text with the trained NER pipeline
doc = nlp(text)

# Print the extracted entities and their labels
print("\nExtracted Entities:")
for ent in doc.ents:
    print(f"{ent.label_}: {ent.text}")
