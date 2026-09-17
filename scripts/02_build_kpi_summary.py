"""
02_build_kpi_summary.py

Builds the core business KPI tables from the skill-tagged job postings:
  1. Overall skill demand frequency (count + % of postings)
  2. Postings per category
  3. Top skills within each category

Input:  data/processed/adzuna_tn_jobs_with_skills.csv
Output: data/processed/skill_demand_summary.csv
        data/processed/category_skill_breakdown.csv
"""

import pandas as pd
import ast
import os
from collections import Counter

INPUT_PATH = "data/processed/adzuna_tn_jobs_with_skills.csv"
SKILL_DEMAND_OUTPUT = "data/processed/skill_demand_summary.csv"
CATEGORY_BREAKDOWN_OUTPUT = "data/processed/category_skill_breakdown.csv"


def parse_skills_column(value):
    """skills_found is saved as a stringified list when read back from CSV."""
    if isinstance(value, list):
        return value
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return []


if __name__ == "__main__":
    df = pd.read_csv(INPUT_PATH)
    df["skills_found"] = df["skills_found"].apply(parse_skills_column)

    # 1. Overall skill demand frequency
    all_skills_flat = [skill for skills_list in df["skills_found"] for skill in skills_list]
    skill_freq = Counter(all_skills_flat)

    skill_demand_df = pd.DataFrame(skill_freq.items(), columns=["skill", "posting_count"])
    skill_demand_df["percent_of_postings"] = round(
        (skill_demand_df["posting_count"] / len(df)) * 100, 1
    )
    skill_demand_df = skill_demand_df.sort_values("posting_count", ascending=False).reset_index(drop=True)

    print("=== TOP 15 SKILLS OVERALL ===")
    print(skill_demand_df.head(15))

    # 2. Postings per category
    print("\n=== POSTINGS PER CATEGORY ===")
    print(df["category"].value_counts())

    # 3. Top skills within each category
    category_rows = []
    print("\n=== TOP SKILLS PER CATEGORY ===")
    for cat in df["category"].dropna().unique():
        cat_df = df[df["category"] == cat]
        cat_skills = [s for skills_list in cat_df["skills_found"] for s in skills_list]
        top5 = Counter(cat_skills).most_common(5)
        print(f"\n{cat} ({len(cat_df)} postings):")
        for skill, count in top5:
            print(f"  - {skill}: {count}")
            category_rows.append({"category": cat, "skill": skill, "posting_count": count})

    category_breakdown_df = pd.DataFrame(category_rows)

    os.makedirs("data/processed", exist_ok=True)
    skill_demand_df.to_csv(SKILL_DEMAND_OUTPUT, index=False)
    category_breakdown_df.to_csv(CATEGORY_BREAKDOWN_OUTPUT, index=False)
    print(f"\nSaved {SKILL_DEMAND_OUTPUT}")
    print(f"Saved {CATEGORY_BREAKDOWN_OUTPUT}")
