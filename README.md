# Automatic Stance Adverbial Detector

Fine-tuning DeBERTa-v3 to automatically detect and classify stance adverbials in English corpus data, comparing results against manual gold-standard annotations.

**Framework:** Biber & Finegan (1988), Biber et al. (1999), Biber (2006)  
**Data:** BNC corpus — 8,242 manually annotated concordance lines (4 registers, 9 adverbs)  
**Model:** `microsoft/deberta-v3-base`

---

## Labels

| Code | Category | Examples |
|------|----------|---------|
| E | **Epistemic** — certainty/doubt | *certainly, probably, perhaps, clearly* |
| A | **Attitudinal** — evaluation | *unfortunately, surprisingly, frankly* |
| N | **Non-stance** — Ambiguous cases | context-dependent |

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

> **⚠️ Copyright Notice**  
> The concordance data used in this project are derived from the **British National Corpus (BNC)**, which is &copy; Oxford University Press. The data files (Appendix1–4.xlsx) are **not included in this repository** and cannot be redistributed. To replicate this study, you must obtain access to the BNC through the official license at [www.natcorp.ox.ac.uk](http://www.natcorp.ox.ac.uk). The manual annotations are part of the author's MA thesis (Vilnius University, 2026).

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

**Key research questions:**
1. Can transformers automatically detect stance adverbials in corpus data?
2. What accuracy is achievable vs. manual annotation (Cohen's κ)?
3. Which stance categories are most/least reliably detected?

---

## Citation

If you use this code, please cite:

> S.A., Khaled. (2026). *Automatic Stance Adverbial Detector*. GitHub. https://github.com/ksayeds/Automatic-Stance-Detector
