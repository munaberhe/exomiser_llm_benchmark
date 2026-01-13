from pathlib import Path

from .data import load_cases, load_rankings
from .metrics import compute_top1_accuracy, compute_mrr


def run_benchmark(
    cases_path: str | Path,
    exomiser_path: str | Path,
    llm_path: str | Path,
) -> None:
    cases = load_cases(cases_path)
    exo = load_rankings(exomiser_path)
    llm = load_rankings(llm_path)

    print("Number of cases:", len(cases))
    print()

    # Exomiser
    exo_top1 = compute_top1_accuracy(cases, exo)
    exo_mrr = compute_mrr(cases, exo)

    print("Exomiser (mock) performance:")
    print(f"  Top-1 accuracy: {exo_top1:.2f}")
    print(f"  MRR:            {exo_mrr:.2f}")
    print()

    # LLM
    llm_top1 = compute_top1_accuracy(cases, llm)
    llm_mrr = compute_mrr(cases, llm)

    print("LLM (mock) performance:")
    print(f"  Top-1 accuracy: {llm_top1:.2f}")
    print(f"  MRR:            {llm_mrr:.2f}")
    print()


def main():
    base = Path("data")
    run_benchmark(
        cases_path=base / "cases.csv",
        exomiser_path=base / "exomiser_mock_results.csv",
        llm_path=base / "llm_mock_results.csv",
    )


if __name__ == "__main__":
    main()

