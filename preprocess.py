"""
Preprocess all BNC annotated concordance lines into training-ready CSV.
Input:  Appendix1.AP1994.xlsx, Appendix2.AP2014.xlsx,
        Appendix3.EL1994.xlsx, Appendix4.EL2014.xlsx
Output: data/processed/stance_all.csv
Total:  8,242 annotated instances
Labels: E=Epistemic, A=Attitudinal, N=Non-stance (Biber et al. 1999)
"""

import pandas as pd
import re
from pathlib import Path

DATA_DIR = Path(__file__).parent
OUT_FILE = DATA_DIR / "data/processed/stance_all.csv"

LABEL_MAP  = {"E": 0, "A": 1, "N": 2}
LABEL_NAMES = {0: "Epistemic", 1: "Attitudinal", 2: "Non-stance"}

EVALUATIVE_WORDS = {
    'important', 'significant', 'remarkable', 'surprising', 'unfortunate',
    'critical', 'crucial', 'essential', 'problematic', 'concerning',
    'valuable', 'useful', 'relevant', 'interesting', 'notable',
    'worrying', 'disappointing', 'impressive', 'striking', 'alarming',
    'unacceptable', 'inadequate', 'inappropriate', 'insufficient',
    'fundamental', 'necessary', 'vital', 'urgent', 'serious', 'severe',
    'problem', 'issue', 'challenge', 'failure', 'success', 'achievement',
    'concern', 'risk', 'threat', 'opportunity', 'weakness', 'strength',
    'limitation', 'advantage', 'disadvantage', 'benefit', 'harm', 'damage',
    'fail', 'succeed', 'struggle', 'lack', 'ignore', 'neglect', 'undermine'
}

EPISTEMIC_LEXICON = {
    'certainly', 'clearly', 'obviously', 'undoubtedly', 'definitely',
    'presumably', 'probably', 'perhaps', 'possibly', 'conceivably',
    'apparently', 'evidently', 'seemingly', 'allegedly', 'supposedly',
    'indeed', 'actually', 'really', 'surely', 'necessarily', 'maybe'
}

ATTITUDINAL_LEXICON = {
    'unfortunately', 'fortunately', 'luckily', 'unluckily',
    'surprisingly', 'astonishingly', 'remarkably', 'interestingly',
    'frankly', 'honestly', 'admittedly', 'importantly',
    'conveniently', 'absurdly', 'curiously', 'predictably'
}

ALL_FILES = {
    'Appendix1.AP1994.xlsx': {
        'register': 'AP1994',
        'sheets': ['500_con_clearly', '500_con_probably', '500_con_Indeed',
                   '500_con_unfortunately', '500_con_perhaps']
    },
    'Appendix2.AP2014.xlsx': {
        'register': 'AP2014',
        'sheets': ['500_con_indeed', '500_con_perhaps', '500_con_clearly',
                   '500_con_actually', '500_con_probably']
    },
    'Appendix3.EL1994.xlsx': {
        'register': 'EL1994',
        'sheets': ['BNC1994_elan_ACTUALLY', 'BNC1994_elan_maybe',
                   'BNC1994_elan_perhaps', 'BNC1994_elan_probably',
                   'BNC1994_elan_really']
    },
    'Appendix4.EL2014.xlsx': {
        'register': 'EL2014',
        'sheets': ['500_conc_actually', '500_conc_definitely', '500_conc_maybe',
                   '500_conc_probably', '500_conc_really']
    }
}


def clean_text(s):
    if pd.isna(s):
        return ""
    return re.sub(r"\s+", " ", str(s).strip())


def build_enriched_text(row):
    adverb_lower = row['adverb'].lower().strip().rstrip('.,')
    right        = row['right_context'].lower()
    right_words  = set(re.findall(r'\b\w+\b', right))
    eval_marker  = '<<EVALUATIVE>>' if right_words & EVALUATIVE_WORDS else ''
    if adverb_lower in ATTITUDINAL_LEXICON:
        lex_marker = '<<LEXICON:ATTITUDINAL>>'
    elif adverb_lower in EPISTEMIC_LEXICON:
        lex_marker = '<<LEXICON:ATTITUDINAL>>' if right_words & EVALUATIVE_WORDS else '<<LEXICON:EPISTEMIC>>'
    else:
        lex_marker = '<<LEXICON:NONSTANCE>>'
    markers = ' '.join(filter(None, [eval_marker, lex_marker]))
    return (row['left_context'] + ' **' + row['adverb'].upper() + '** ' +
            markers + ' ' + row['right_context']).strip()


def load_sheet(xl, sheet_name, register):
    raw = xl.parse(sheet_name, header=None)
    df  = raw.iloc[:, [0, 1, 2, -1]].copy()
    df.columns = ['left_context', 'adverb', 'right_context', 'label']
    for col in ['left_context', 'adverb', 'right_context']:
        df[col] = df[col].apply(clean_text)
    df['label']    = df['label'].astype(str).str.strip().str.upper()
    df['register'] = register
    return df[df['label'].isin(LABEL_MAP)]


def main():
    all_dfs = []
    for filename, info in ALL_FILES.items():
        path = DATA_DIR / filename
        if not path.exists():
            print(f"✗ {filename} not found — skipping")
            continue
        xl = pd.ExcelFile(path)
        for sheet in info['sheets']:
            try:
                sdf = load_sheet(xl, sheet, info['register'])
                all_dfs.append(sdf)
                print(f"✓ {filename} | {sheet}: {len(sdf)} rows")
            except Exception as e:
                print(f"✗ {filename} | {sheet}: {e}")

    df = pd.concat(all_dfs, ignore_index=True)
    df['text']       = df.apply(build_enriched_text, axis=1)
    df['label_id']   = df['label'].map(LABEL_MAP)
    df['label_name'] = df['label_id'].map(LABEL_NAMES)

    print(f"\nTotal instances: {len(df)}")
    print("\nBy register:")
    print(df['register'].value_counts())
    print("\nLabel distribution:")
    print(df['label_name'].value_counts())

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_FILE, index=False)
    print(f"\nSaved → {OUT_FILE}")
    return df


if __name__ == "__main__":
    main()
