# Automated Stance Adverbial Detector

Fine-tuning mBERT to automatically detect and classify stance adverbials in English corpus data, comparing results against manual gold-standard annotations.

**Framework:** Biber et al. (1999)  
**Data:** BNC 2014 Academic Prose — 504 manually annotated concordance lines  
**Model:** `bert-base-multilingual-cased` (mBERT)

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
| Lexicon Baseline | — | — | — |
| mBERT Fine-tuned | — | — | — |

*Results populate after running `stance_detector.ipynb`.*

---

## Setup

```bash
pip install -r requirements.txt
jupyter notebook stance_detector.ipynb
```

### Requirements
- Python 3.8+
- CUDA GPU recommended (CPU works, ~3× slower)

---

## Project Structure

```
Stance detetctor/
├── Appendix2.AP2014.xlsx        # gold-standard training data (504 instances)
├── stance_detector.ipynb        # full pipeline: data → training → evaluation
├── preprocess.py                # standalone preprocessing script
├── requirements.txt
├── data/
│   └── processed/               # cleaned CSVs (generated)
├── models/
│   └── mbert-stance/best/       # saved fine-tuned model (generated)
└── results/
    ├── results_summary.csv      # accuracy / F1 / κ comparison table
    ├── error_analysis.csv       # all misclassified instances
    └── figures/                 # confusion matrix, training curves, plots
```

---

## Research Context

This pilot study forms part of a PhD research proposal investigating computational approaches to stance in learner corpora. The model is trained on native English (BNC), with multilingual architecture (mBERT) chosen to extend to Italian L2 (MERLIN corpus) and Arabic L2 (ZAEBUC corpus) in future work.

**Key research questions:**
1. Can transformers automatically detect stance adverbials in corpus data?
2. What accuracy is achievable vs. manual annotation (Cohen's κ)?
3. Which stance categories are most/least reliably detected?
4. What are the systematic error patterns?

---

## Citation

If you use this code, please cite:

> Ahmed, K. (2026). *Automated Stance Adverbial Detection: A Pilot Study Using mBERT*. GitHub. https://github.com/ksayeds/stance-detector
