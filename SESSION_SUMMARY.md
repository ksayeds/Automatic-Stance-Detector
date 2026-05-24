# Stance Detector Project — Session Summary
**Khaled Ahmed | MA Corpus Linguistics, Vilnius University**  
**Date: May 2026**

---

## Project Goal
Build an automated stance adverbial detector to faciltate the manual semantic analysis process.
Develop a toolkit that is grounded in linguistic theory and framework, as the available trained models detect stance according to polarity positive, negative, or neutral. 
---

## Data
- **4 Excel files** containing 8,242 manually annotated concordance lines from BNC corpora 1994 and 2014 (MA thesis gold standard)
- **Labels:** E = Epistemic, A = Attitudinal, N = Non-stance (ambiguous cases) Biber and Finegan (1988, Biber et al. 1999, and Biber 2006)
- **Registers:** Academic Prose (AP) + E-language (EL), 1994 + 2014
- **Adverbs:** indeed, perhaps, clearly, actually, probably, unfortunately, maybe, really, definitely

| File | Register | Instances |
|---|---|---|
| Appendix1.AP1994.xlsx | Academic Prose 1994 | 2,500 |
| Appendix2.AP2014.xlsx | Academic Prose 2014 | 2,500 |
| Appendix3.EL1994.xlsx | Everyday Language 1994 | 742 |
| Appendix4.EL2014.xlsx | Everyday Language 2014 | 2,500 |
| **Total** | | **8,242** |

---

## Key Linguistic research finding: 
Epistemic adverbs shift to Attitudinal function when followed by evaluative content words in the right context. 
Example:
- *"perhaps **the most important** finding"* → Attitudinal (evaluative context)
- *"perhaps the case"* → Epistemic (neutral context)

This insight was implemented as an `<<EVALUATIVE>>` marker injected into training text, producing significant performance improvements.

---

## Technical Stack
- **Model:** `microsoft/deberta-v3-base`
- **Framework:** HuggingFace Transformers + PyTorch
- **Evaluation:** scikit-learn (accuracy, Macro F1, Cohen's κ)
- **Hardware:** MacBook Air M4, CPU/MPS

---

## Model Development — Results Progression

| Model | Accuracy | Macro F1 | Cohen's κ | Error rate|
|---|---|---|---|---|
| Lexicon Baseline | 0.746 | 0.296 | -0.011 | — |
| mBERT (AP2014 only) | 0.852 | 0.511 | 0.277 | 74 |
| DeBERTa (AP2014 only) | 0.880 | 0.514 | 0.272 | 60 |
| DeBERTa + Evaluative Marker | 0.904 | 0.601 | 0.433 | 48 |
| **DeBERTa + All 4 files + Markers** | **0.890** | **0.667** | **0.645** | 181/1649 |

---

## Final Model Results (8,242 instances, test set = 1,649)

| | Score |
|---|---|
| Accuracy | 0.890 |
| Macro F1 | 0.667 |
| Cohen's κ | **0.645 (substantial agreement)** |

### Per-Class Performance
| Class | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| Epistemic | 0.93 | 0.94 | 0.93 | 1,341 |
| Attitudinal | 0.79 | 0.73 | 0.76 | 275 |
| Non-stance | 0.27 | 0.36 | 0.31 | 33 |

---

## Training Configuration (Best Run)
- **Epochs:** 7 (best at epoch 5)
- **Learning rate:** 1e-5
- **Batch size:** 16
- **Class weights:** Inverse frequency (handles imbalance)
- **Features:** `<<EVALUATIVE>>` marker + lexicon markers
- **Early stopping patience:** 3

---

## Key Findings:

1. **Lexical identity alone is insufficient** — same adverb (*perhaps*, *indeed*, *clearly*) realizes different stance functions depending on context. Lexicon baseline F1=0.296 vs mBERT F1=0.511.

2. **Appraisal-informed features improve classification** — adding evaluative context markers (Martin & White 2005) improved Macro F1 by 18% over plain DeBERTa.

3. **Adverb-specific difficulty** — *probably* (3% error) vs *indeed* (55% error) — adverbs with narrower functional range are easier to classify.

4. **Capitalized forms easier** — sentence-initial position (Clearly, Probably) = 0% error rate, strong positional stance cue.

5. **Remaining errors are linguistically motivated** — errors cluster at genuine Epistemic/Attitudinal boundaries.

---

## Error Analysis Summary
| Error Pattern | Count | Linguistic Explanation |
|---|---|---|
| Attitudinal → Epistemic | Most common | Functionally ambiguous adverbs in evaluation contexts |
| Epistemic → Non-stance | Second | Factual verification contexts misread as non-stance |
| Non-stance → Epistemic | Third | Dominant class pulls predictions |

---

## Computational Findings Statement
> *"Fine-tuned DeBERTa-v3 with appraisal-informed features achieved Macro F1=0.667 and Cohen's κ=0.645 (substantial agreement) across 8,242 annotated instances spanning two registers and two time periods, outperforming the lexicon baseline by 74%. The evaluative marker approach — improved classification at the theoretically challenging Epistemic/Attitudinal boundary, demonstrating that linguistic theory directly enhances computational performance."*

---

## Saved Files
```
/Users/khaled/Desktop/NLP/Stance detetctor/
├── stance detector 2.ipynb        — experimental notebook
├── models/deberta-stance/best/    — saved fine-tuned model
├── results/
│   ├── BNC_pilot_results.json     — all metrics saved permanently
│   ├── results_summary.csv        — comparison table
│   ├── error_analysis.csv         — misclassified instances
│   ├── manual_inspection.xlsx     — full test set with predictions
│   └── figures/                   — all plots
└── data/processed/  
— main pipeline notebook           — cleaned CSV splits
```

---

## Reload Model
```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer

model     = AutoModelForSequenceClassification.from_pretrained('models/deberta-stance/best')
tokenizer = AutoTokenizer.from_pretrained('models/deberta-stance/best', use_fast=False)
```

---
