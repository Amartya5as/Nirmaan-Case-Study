# scripts/parse_rubric.py
import pandas as pd
import re
import json

def parse_rubric(path: str):
    """
    Parses the messy rubric Excel file and extracts:
    - criterion name
    - description
    - weight
    - keywords
    - min/max word limits (if found)
    
    Works even if the file has merged cells, blank rows, or inconsistent formatting.
    """

    # Load Excel sheet
    df = pd.read_excel(path, sheet_name="Rubrics", header=None)
    df = df.fillna("")

    # Convert rows to strings for easier scanning
    rows = df.astype(str)

    RUBRIC_KEYWORDS = [
        "content", "structure", "fluency", "grammar",
        "vocabulary", "pronunciation", "confidence"
    ]

    parsed = []

    # Step 1: Scan for rows containing any rubric keyword
    for i in range(len(rows)):
        line = " ".join(rows.iloc[i].tolist()).strip().lower()

        if any(k in line for k in RUBRIC_KEYWORDS) and len(line) > 5:
            parsed.append((i, rows.iloc[i].tolist()))

    # Step 2: Build structured rubric entries
    rubric = []
    for idx, raw_row in parsed:
        row_text = " ".join(raw_row)

        # Extract criterion name
        name = None
        for k in RUBRIC_KEYWORDS:
            if k in row_text.lower():
                name = k.capitalize()
                break
        if not name:
            name = "Criterion"

        # Extract weight (last number in the row)
        weight_match = re.findall(r"\b\d{1,3}\b", row_text)
        weight = int(weight_match[-1]) if weight_match else 10

        # Extract possible min/max word limits
        # E.g., "Min: 20", "Max words 150"
        min_match = re.search(r"(min|min words|min:)\s*(\d+)", row_text.lower())
        max_match = re.search(r"(max|max words|max:)\s*(\d+)", row_text.lower())

        min_words = int(min_match.group(2)) if min_match else None
        max_words = int(max_match.group(2)) if max_match else None

        # Extract keywords (words with 4+ letters)
        keywords = [
            w.lower()
            for w in re.findall(r"\b[a-zA-Z]{4,}\b", row_text)
            if w.lower() not in ["content", "structure", "section"]  # remove common noise
        ]

        rubric.append({
            "name": name,
            "description": row_text,
            "weight": weight,
            "keywords": keywords[:8],  # limit to avoid overfitting
            "min_words": min_words,
            "max_words": max_words
        })

    # Step 3: Normalize weights so they sum to 100
    total_weight = sum(r["weight"] for r in rubric)
    for r in rubric:
        r["norm_weight"] = (r["weight"] / total_weight) * 100

    return rubric


# Run from command line
if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "/mnt/data/Case study for interns.xlsx"
    rubric = parse_rubric(path)
    print(json.dumps(rubric, indent=2))
