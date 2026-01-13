from collections import defaultdict
import numpy as np
import pandas as pd


def compute_top1_accuracy(cases: pd.DataFrame, rankings: pd.DataFrame) -> float:
    """
    For each case, check if the true disease is at rank 1.
    """
    # best (lowest) rank per case/disease
    best_ranks = defaultdict(lambda: np.inf)
    for _, row in rankings.iterrows():
        key = (row["case_id"], row["disease"])
        best_ranks[key] = min(best_ranks[key], row["rank"])

    hits = 0
    total = len(cases)
    for _, row in cases.iterrows():
        key = (row["case_id"], row["true_disease"])
        if best_ranks[key] == 1:
            hits += 1

    return hits / total if total > 0 else 0.0


def compute_mrr(cases: pd.DataFrame, rankings: pd.DataFrame) -> float:
    """
    Mean Reciprocal Rank: 1/rank of true disease (or 0 if not found).
    """
    best_ranks = defaultdict(lambda: np.inf)
    for _, row in rankings.iterrows():
        key = (row["case_id"], row["disease"])
        best_ranks[key] = min(best_ranks[key], row["rank"])

    rr = []
    for _, row in cases.iterrows():
        key = (row["case_id"], row["true_disease"])
        r = best_ranks[key]
        if np.isfinite(r):
            rr.append(1.0 / r)
        else:
            rr.append(0.0)
    return float(np.mean(rr)) if rr else 0.0

