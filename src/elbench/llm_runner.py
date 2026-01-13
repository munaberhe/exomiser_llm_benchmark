"""
Run the LLM over all cases and write a rankings CSV.

This script:
- loads cases from data/cases.csv,
- for each case, calls the LLM to get a ranked list of diseases,
- writes data/llm_results_live.csv with columns: case_id, rank, disease.
"""

from pathlib import Path

import pandas as pd

from .data import load_cases
from .llm_client import suggest_diseases_from_phenotypes


def run_llm_over_cases(
    cases_path: str | Path,
    out_path: str | Path,
    top_k: int = 5,
) -> None:
    cases_path = Path(cases_path)
    out_path = Path(out_path)

    cases = load_cases(cases_path)
    rows: list[dict] = []

    for _, row in cases.iterrows():
        case_id = row["case_id"]
        phenotypes = row["phenotypes"]
        print(f"\n=== Case {case_id} ===")
        print(f"Phenotypes: {phenotypes}")

        diseases = suggest_diseases_from_phenotypes(phenotypes, k=top_k)

        if not diseases:
            print("LLM returned no diseases for this case.")
            continue

        print("LLM suggested diseases (in order):")
        for i, d in enumerate(diseases, start=1):
            print(f"  {i}. {d}")
            rows.append(
                {
                    "case_id": case_id,
                    "rank": i,
                    "disease": d,
                }
            )

    df_out = pd.DataFrame(rows, columns=["case_id", "rank", "disease"])
    df_out.to_csv(out_path, index=False)
    print(f"\nSaved live LLM results to {out_path}")


def main():
    base = Path("data")
    cases_path = base / "cases.csv"
    out_path = base / "llm_results_live.csv"
    run_llm_over_cases(cases_path, out_path, top_k=5)


if __name__ == "__main__":
    main()

