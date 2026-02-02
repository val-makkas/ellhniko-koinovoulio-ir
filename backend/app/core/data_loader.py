import pandas as pd
from pathlib import Path

# Διαδρομή προς το αρχείο dataset του Ελληνικού Κοινοβουλίου
DATASET_PATH = Path(__file__).resolve().parents[2] / "data" / "Greek_Parliament_Proceedings_1989_2020.csv"

DF_CACHE = None

def load_df():
    global DF_CACHE
    if DF_CACHE is None:
        DF_CACHE = pd.read_csv(
            DATASET_PATH,
            encoding="utf-8",
            usecols=["speech", "member_name", "political_party", "sitting_date"],
            dtype={
                "speech": "string",
                "member_name": "string",
                "political_party": "string",
                "sitting_date": "string",
            },
        )
    return DF_CACHE

def load_sample(n: int = 5):
    df = load_df()
    return df.head(n).to_dict(orient="records")

def load_speeches(n: int = 10):
    df = load_df()
    df = df.dropna(subset=["speech", "member_name", "political_party", "sitting_date"])
    sample = df.head(n)[["sitting_date", "member_name", "political_party", "speech"]]
    return sample.to_dict(orient="records")