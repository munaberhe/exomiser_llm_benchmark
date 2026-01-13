"""
LLM client utilities for rare disease phenotype–disease ranking.

This module defines a function that, given a phenotype description, queries an LLM
and returns a ranked list of candidate diseases (by name, in order).
"""

import os
import re
from typing import List

from openai import OpenAI


def get_openai_client() -> OpenAI:
    """
    Create an OpenAI client.

    Requires the environment variable OPENAI_API_KEY to be set, e.g.:

        export OPENAI_API_KEY="sk-..."

    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY environment variable is not set. "
            "Set it before running the LLM benchmark."
        )
    return OpenAI(api_key=api_key)


def suggest_diseases_from_phenotypes(
    phenotypes_text: str,
    k: int = 5,
    model_name: str = "gpt-4o-mini",
) -> List[str]:
    """
    Given a free-text phenotype description, ask the LLM for the top-k most likely
    rare diseases. Returns a list of disease names in ranked order.

    The function:
    - constructs a prompt,
    - calls the OpenAI chat completion API,
    - parses a numbered list of disease names from the response.
    """
    client = get_openai_client()

    system_msg = (
        "You are an expert clinical geneticist and rare disease diagnostician. "
        "Given phenotype descriptions, you suggest the most likely rare diseases."
    )

    user_prompt = f"""
The patient has the following phenotype description:

\"\"\"{phenotypes_text}\"\"\"

List the top {k} most likely rare diseases (by disease name only).
Return them as a numbered list, one disease per line, without any extra commentary.
"""

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.0,
    )

    text = response.choices[0].message.content.strip()

    diseases: List[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        # Remove leading numbering like "1.", "2)", "3 -"
        line = re.sub(r"^\d+[\.\)\-\s]*", "", line)
        if line:
            diseases.append(line)

    # Truncate to top-k
    return diseases[:k]

