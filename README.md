# Exomiser vs LLM Benchmark (Mock Framework)

## Overview

This project implements a small, testable benchmarking framework for **rare disease diagnosis tools**, comparing a traditional algorithmic method (Exomiser) with a **large language model (LLM)** on toy rare-disease cases.

To keep the project lightweight and easy to run, the current version uses **mock result files** instead of real Exomiser or LLM calls. The focus is on:

- Structuring the benchmark in a reproducible way.  
- Computing meaningful metrics (Top-1 accuracy, Mean Reciprocal Rank).  
- Providing a clean foundation that can later plug in real Exomiser output and real LLM predictions.

This is **not** a clinical tool – it is a learning and portfolio project illustrating how to design a benchmarking pipeline for rare disease phenotype–disease matching.

---

## Data

All data live under the `data/` directory:

- `cases.csv` – toy rare-disease cases with:  
  - `case_id`: numeric identifier  
  - `phenotypes`: free-text phenotype description  
  - `true_disease`: the correct diagnosis for the case

- `exomiser_mock_results.csv` – mock Exomiser-style rankings with:  
  - `case_id`  
  - `rank`: 1 = top-ranked, higher numbers = lower rank  
  - `disease`: predicted disease name

- `llm_mock_results.csv` – mock LLM-style rankings with the same columns:  
  - `case_id`  
  - `rank`  
  - `disease`

These “mock” files are deliberately simple and small, but the code is written so that you can later replace them with real outputs from Exomiser and an LLM-based system.

---

## Methods

The core logic lives in `src/elbench/` and is organised into three main modules.

### 1. Data loading (`data.py`)

- `load_cases(path)`  
  Loads the table of rare-disease cases from CSV. Expects columns:  
  `case_id`, `phenotypes`, `true_disease`.

- `load_rankings(path)`  
  Loads tool outputs (Exomiser or LLM) from CSV. Expects columns:  
  `case_id`, `rank`, `disease`.

This separation keeps the I/O logic simple and makes it easy to swap in different datasets.

### 2. Metrics (`metrics.py`)

Two standard **ranking metrics** are implemented:

- `compute_top1_accuracy(cases, rankings)`  
  - For each case, checks whether the **true disease** appears at **rank 1** in the ranking.  
  - Returns the fraction of cases where the top prediction is correct.

- `compute_mrr(cases, rankings)`  
  - Computes **Mean Reciprocal Rank (MRR)**:  
    - For each case, find the rank `r` of the true disease.  
    - Use `1 / r` as the score (or `0` if the disease is not found).  
    - Average over all cases.  
  - MRR gives partial credit when the true disease is near the top but not always rank 1.

Because these metrics only require `(case_id, rank, disease)`, they can be applied to **any** ranking-based tool: Exomiser, LLMs, or other phenotype–disease matching methods.

### 3. Benchmark runner (`benchmark.py`)

- `run_benchmark(cases_path, exomiser_path, llm_path)`  
  - Loads cases and mock result tables for Exomiser and the LLM.  
  - Computes Top-1 accuracy and MRR for each method.  
  - Prints metrics to the console.

- `main()`  
  - Convenience entry point that assumes the default file paths in `data/` and runs the benchmark.

A small helper script, `run_benchmark.py`, simply calls `elbench.benchmark.main()` so that the benchmark can be run with a single command from the command line.

---

## Setup

### 1. Clone the repository

    git clone <this-repo-url>
    cd exomiser_llm_benchmark

### 2. Create and activate a virtual environment

    python -m venv .venv
    source .venv/bin/activate          # Windows PowerShell: .venv\Scripts\Activate.ps1

### 3. Install dependencies

Install Python packages from `requirements.txt`:

    pip install -r requirements.txt

This will install:

- `pandas` – data handling  
- `numpy` – numerical utilities  
- `pytest` – basic testing framework

---

## How to Run

### 1. Run tests

Basic tests are provided under `tests/` to ensure that the metrics run correctly on the mock data:

    pytest

You should see output similar to:

    ============================= test session starts ==============================
    ...
    collected 1 item

    tests/test_metrics.py .                                                  [100%]

    ========================= 1 passed, 1 warning in X.XXs =========================

This confirms that:

- the data-loading functions work on the mock CSV files, and  
- Top-1 accuracy and MRR are computed without errors.

### 2. Run the benchmark

To run the benchmark comparing Exomiser (mock) vs the LLM (mock):

    python run_benchmark.py

This will:

- Load 5 toy rare-disease cases from `data/cases.csv`.  
- Load mock Exomiser rankings from `data/exomiser_mock_results.csv`.  
- Load mock LLM rankings from `data/llm_mock_results.csv`.  
- Compute and print **Top-1 accuracy** and **MRR** for each method.

With the current mock data, the output looks like:

    Number of cases: 5

    Exomiser (mock) performance:
      Top-1 accuracy: 0.60
      MRR:            0.77

    LLM (mock) performance:
      Top-1 accuracy: 0.80
      MRR:            0.90

You can edit the CSVs in `data/` to explore how different ranking behaviours affect these metrics.

---

## Results

With the current toy setup (5 cases and simple mock rankings):

- **Exomiser (mock)**  
  - Top-1 accuracy: **0.60**  
  - MRR: **0.77**

- **LLM (mock)**  
  - Top-1 accuracy: **0.80**  
  - MRR: **0.90**

Interpretation:

- **Top-1 accuracy** measures how often the tool’s first-ranked disease is the true diagnosis.  
- **MRR** gives credit when the true disease is near the top of the list, even if not always rank 1 (for example, rank 2 contributes 0.5, rank 3 contributes 0.33, etc.).

In this mock scenario, the LLM-style approach performs better than Exomiser on both metrics, but the real purpose here is to demonstrate a **reusable benchmarking framework**, not to make strong claims about the methods themselves.

---

## Discussion

This project is intentionally small and self-contained, but it illustrates several important ideas for real-world rare disease benchmarking:

- **Reproducible data flow**  
  Cases and tool outputs are loaded from explicit CSV files rather than being hidden in notebooks. This makes it easier to track, version and share benchmark datasets.

- **Shared metrics**  
  Exomiser, LLMs and future methods can all be evaluated with the same Top-1 and MRR functions, enabling fair comparisons between very different approaches.

- **Tested code**  
  Basic `pytest` tests ensure that the metric functions behave sensibly on the mock data and continue to work as the project evolves.

Planned or possible next steps include:

- Replacing the mock Exomiser file with **real Exomiser output** for a small curated case set.  
- Adding a module that queries an LLM (e.g. via an API) to generate candidate disease rankings from phenotype text in a reproducible way.  
- Evaluating other ranking-based methods (BM25, TF-IDF, ontology-based scores) within the same framework.  
- Logging results to a consolidated benchmark table and plotting metrics across methods or case subsets (for example by phenotype complexity or disease category).

Overall, this repository is meant as a **benchmarking scaffold**: a starting point for more realistic comparisons between traditional rare-disease tools like Exomiser and newer LLM-based approaches, in a way that is transparent, testable and easy to extend.

