from pathlib import Path

from src.elbench.benchmark import run_benchmark


def main():
    base = Path("data")
    run_benchmark(
        cases_path=base / "cases.csv",
        exomiser_path=base / "exomiser_mock_results.csv",
        llm_path=base / "llm_results_live.csv",
    )


if __name__ == "__main__":
    main()

