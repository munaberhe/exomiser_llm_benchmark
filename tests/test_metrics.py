from pathlib import Path

from src.elbench.data import load_cases, load_rankings
from src.elbench.metrics import compute_top1_accuracy, compute_mrr


def test_metrics_run_on_mock_data():
    base = Path("data")
    cases = load_cases(base / "cases.csv")
    exo = load_rankings(base / "exomiser_mock_results.csv")

    top1 = compute_top1_accuracy(cases, exo)
    mrr = compute_mrr(cases, exo)

    # Just check metrics are in [0, 1] range
    assert 0.0 <= top1 <= 1.0
    assert 0.0 <= mrr <= 1.0

