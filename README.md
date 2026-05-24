# Automatic Stance Adverbial Detector

Fine-tuning DeBERTa-v3 to automatically detect and classify stance adverbials in English corpus data, incorporating appraisal-informed features (Martin & White 2005) and comparing results against manual gold-standard annotations.

**Framework:** Biber et al. (1999) + Martin & White (2005)  
**Data:** BNC corpus — 8,242 manually annotated concordance lines (4 registers, 9 adverbs)  
**Model:** `microsoft/deberta-v3-base`

---

## Labels

| Code | Category | Examples |
|------|----------|---------|
| E | **Epistemic** — certainty/doubt | *certainly, probably, perhaps, clearly* |
| A | **Attitudinal** — evaluation | *unfortunately, surprisingly, frankly* |
| N | **Non-stance** — adverb without stance function | context-dependent |

---

## Results

| Model | Accuracy | Macro F1 | Cohen's κ |
|-------|----------|----------|-----------|
| Lexicon Baseline | 0.669 | 0.384 | 0.139 |
| mBERT fine-tuned | 0.852 | 0.511 | 0.277 |
| DeBERTa fine-tuned | 0.880 | 0.514 | 0.272 |
| **DeBERTa + Evaluative Marker** | **0.890** | **0.667** | **0.645** |

### Per-Class Performance (Final Model)

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Epistemic | 0.93 | 0.94 | 0.93 | 1,341 |
| Attitudinal | 0.79 | 0.73 | 0.76 | 275 |
| Non-stance | 0.27 | 0.36 | 0.31 | 33 |

**Error rate: 10.97% (181/1,649 test instances)**

---

## Key Linguistic Insight

Epistemic adverbials shift to Attitudinal function when followed by evaluative content words in the right context — based on the stance framework of Biber & Finegan (1988), Biber et al. (1999), and Biber (2006). An `<<EVALUATIVE>>` marker was injected into training text when such words were detected, improving Macro F1 by 18% over plain DeBERTa.

---

## Dataset

| File | Register | Year | Instances |
|------|----------|------|-----------|
| Appendix1.AP1994.xlsx | Academic Prose | 1994 | 2,500 |
| Appendix2.AP2014.xlsx | Academic Prose | 2014 | 2,500 |
| Appendix3.EL1994.xlsx | Everyday Language | 1994 | 742 |
| Appendix4.EL2014.xlsx | Everyday Language | 2014 | 2,500 |

*Data from BNC (British National Corpus). Available under BNC license at www.natcorp.ox.ac.uk*

---

## Setup

```bash
pip install -r requirements.txt
jupyter notebook "stance detector 2.ipynb"
```

### Requirements
- Python 3.8+
- M4 Mac / GPU recommended (CPU works, ~35 min per run)

---

## Project Structure

```
Automatic-Stance-Detector/
├── stance detector 2.ipynb      # full pipeline: data → training → evaluation
├── preprocess.py                # standalone preprocessing script
├── requirements.txt
├── SESSION_SUMMARY.md           # full project session log
├── results/
│   ├── BNC_pilot_results.json   # all metrics saved permanently
│   ├── results_summary.csv      # comparison table
│   ├── error_analysis.csv       # misclassified instances
│   ├── errors_only.xlsx         # 181 errors for manual inspection
│   └── figures/                 # confusion matrix, training curves, plots
└── data/processed/              # cleaned CSV splits (generated)
```

---

## Research Context

Pilot study for PhD research proposal (Free University of Bozen-Bolzano, 2026). Bridges Biber et al. (1999) stance framework with Martin & White (2005) appraisal theory. Multilingual architecture designed for extension to MERLIN (Italian L2) and ZAEBUC (Arabic L2) learner corpora.

**Key research questions:**
1. Can transformers automatically detect stance adverbials in corpus data?
2. What accuracy is achievable vs. manual annotation (Cohen's κ)?
3. Which stance categories are most/least reliably detected?
4. How does appraisal-informed feature engineering improve classification?

---

## Citation

If you use this code, please cite:

> Ahmed, K. (2026). *Automatic Stance Adverbial Detector*. GitHub. https://github.com/ksayeds/Automatic-Stance-Detector
