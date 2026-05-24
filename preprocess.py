"""
Preprocess AP2014 annotated concordance lines into training-ready CSV.
Input:  Appendix2.AP2014.xlsx
Output: data/processed/stance_data.csv
"""

import pandas as pd
import re
from pathlib import Path

DATA_DIR = Path(__file__).parent
RAW_FILE = DATA_DIR / "Appendix2.AP2014.xlsx"
OUT_FILE = DATA_DIR / "data/processed/stance_data.csv"

LABEL_MAP = {"E": 0, "A": 1, "N": 2}
LABEL_NAMES = {0: "Epistemic", 1: "Attitudinal", 2: "Non-stance"}


def clean_text(s):
    if pd.isna(s):
        return ""
    s = str(s).strip()
    s = re.sub(r"\s+", " ", s)
    return s


def load_ap2014(path):
    df = pd.read_excel(path, header=0)

    # columns: 0=left_ctx, 1=adverb, 2=right_ctx, 8=label
    df = df.iloc[:, [0, 1, 2, 8]].copy()
    df.columns = ["left_context", "adverb", "right_context", "label"]

    # clean
    for col in ["left_context", "adverb", "right_context"]:
        df[col] = df[col].apply(clean_text)
    df["label"] = df["label"].astype(str).str.strip().str.upper()

    # drop rows with missing label or unknown label
    df = df[df["label"].isin(LABEL_MAP)].copy()

    # build full sentence — uppercase adverb so model attends to it
    df["text"] = (
        df["left_context"] + " **" + df["adverb"].str.upper() + "** " + df["right_context"]
    ).str.strip()

    df["label_id"] = df["label"].map(LABEL_MAP)
    df["label_name"] = df["label_id"].map(LABEL_NAMES)

    return df[["text", "left_context", "adverb", "right_context", "label", "label_id", "label_name"]]


def main():
    print(f"Loading {RAW_FILE.name}...")
    df = load_ap2014(RAW_FILE)

    print(f"\nTotal instances: {len(df)}")
    print("\nClass distribution:")
    print(df["label_name"].value_counts())
    print("\nLabel proportions:")
    print(df["label_name"].value_counts(normalize=True).round(3))

    print("\nSample rows:")
    print(df[["adverb", "label_name", "text"]].head(5).to_string())

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_FILE, index=False)
    print(f"\nSaved → {OUT_FILE}")
    return df


if __name__ == "__main__":
    main()
