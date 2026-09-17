"""
01_extract_skills.py

Scans each job posting's title + description for skill matches,
using the regex patterns defined in data/lookup/skill_mapping.csv.

Input:  data/raw/adzuna_tamilnadu_jobs_raw.csv
        data/lookup/skill_mapping.csv
Output: data/processed/adzuna_tn_jobs_with_skills.csv
"""

import pandas as pd
import re
import os
import ast

RAW_DATA_PATH = "data/raw/adzuna_tamilnadu_jobs_raw.csv"
SKILL_MAPPING_PATH = "data/lookup/skill_mapping.csv"
OUTPUT_PATH = "data/processed/adzuna_tn_jobs_with_skills.csv"


def extract_skills(text, skills_df):
    found = []
    for _, row in skills_df.iterrows():
        if re.search(row["regex_pattern"], text, flags=re.IGNORECASE):
            found.append(row["skill"])
    return found


if __name__ == "__main__":
    df = pd.read_csv(RAW_DATA_PATH)
    skills_df = pd.read_csv(SKILL_MAPPING_PATH)

    print(f"Loaded {len(df)} job postings")
    print(f"Loaded {len(skills_df)} skill patterns across "
          f"{skills_df['skill_category'].nunique()} categories")

    df["full_text"] = (df["title"].fillna("") + " " + df["description"].fillna("")).str.lower()
    df["skills_found"] = df["full_text"].apply(lambda t: extract_skills(t, skills_df))
    df["skill_count"] = df["skills_found"].apply(len)

    matched = (df["skill_count"] > 0).sum()
    print(f"\nPostings with at least 1 skill matched: {matched} / {len(df)}")
    print("\nSample:")
    print(df[["title", "category", "skills_found"]].head(10))

    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved to {OUTPUT_PATH}")
