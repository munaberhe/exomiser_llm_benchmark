from pathlib import Path
import pandas as pd


def load_cases(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    df = pd.read_csv(path)
    required = {"case_id", "phenotypes", "true_disease"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing columns in cases CSV: {missing}")
    return df


def load_rankings(path: str | Path) -> pd.DataFrame:
    """
    Load rankings from a CSV of the form:
    case_id,rank,disease
    """
    path = Path(path)
    df = pd.read_csv(path)
    required = {"case_id", "rank", "disease"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing columns in rankings CSV: {missing}")
    return df

