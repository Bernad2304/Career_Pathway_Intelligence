"""
03_skill_gap_analysis.py

Compares what each degree program's curriculum covers (data/lookup/degree_skill_coverage.csv)
against what the real Tamil Nadu job market actually demands (data/processed/category_skill_breakdown.csv),
producing a Skill Gap Score per degree per skill category.

Gap Score logic:
  Market demand (posting_count share within category) x Coverage penalty
  Coverage penalty: None = 1.0 (full gap), Partial = 0.5 (half gap), Core = 0.0 (no gap)

A higher gap score = bigger mismatch between what the degree teaches and what employers want.

Input:  data/lookup/degree_skill_coverage.csv
        data/processed/category_skill_breakdown.csv
Output: data/processed/skill_gap_by_degree.csv
"""

import pandas as pd
import os

COVERAGE_PATH = "data/lookup/degree_skill_coverage.csv"
CATEGORY_BREAKDOWN_PATH = "data/processed/category_skill_breakdown.csv"
OUTPUT_PATH = "data/processed/skill_gap_by_degree.csv"

COVERAGE_PENALTY = {
    "Core": 0.0,
    "Partial": 0.5,
    "None": 1.0,
}

# Maps each skill (as it appears in category_skill_breakdown.csv) back to
# its skill_category, so we can compare against the degree coverage columns.
SKILL_CATEGORY_MAP_PATH = "data/lookup/skill_mapping.csv"


def load_skill_to_category():
    skills_df = pd.read_csv(SKILL_CATEGORY_MAP_PATH)
    return dict(zip(skills_df["skill"], skills_df["skill_category"]))


def coverage_column_for_category(skill_category):
    mapping = {
        "IT & Data": "it_data_coverage",
        "Accounting & Finance": "accounting_finance_coverage",
        "Sales & Marketing": "sales_marketing_coverage",
        "HR & Admin": "hr_admin_coverage",
        "Customer Service": "customer_service_coverage",
        "Soft Skills": "soft_skills_coverage",
    }
    return mapping.get(skill_category)


if __name__ == "__main__":
    coverage_df = pd.read_csv(COVERAGE_PATH, keep_default_na=False)
    category_breakdown_df = pd.read_csv(CATEGORY_BREAKDOWN_PATH)
    skill_to_category = load_skill_to_category()

    category_breakdown_df["skill_category"] = category_breakdown_df["skill"].map(skill_to_category)

    gap_rows = []

    for _, degree_row in coverage_df.iterrows():
        degree = degree_row["degree"]
        primary_sector = degree_row["primary_job_sector"]

        # Look at skill demand ONLY within this degree's primary job sector
        sector_demand = category_breakdown_df[category_breakdown_df["category"] == primary_sector]

        for _, demand_row in sector_demand.iterrows():
            skill = demand_row["skill"]
            posting_count = demand_row["posting_count"]
            skill_category = demand_row["skill_category"]

            if pd.isna(skill_category):
                continue

            coverage_col = coverage_column_for_category(skill_category)
            if coverage_col is None:
                continue

            coverage_level = degree_row[coverage_col]
            penalty = COVERAGE_PENALTY.get(coverage_level, 1.0)
            gap_score = posting_count * penalty

            gap_rows.append({
                "degree": degree,
                "primary_job_sector": primary_sector,
                "skill": skill,
                "skill_category": skill_category,
                "market_posting_count": posting_count,
                "degree_coverage_level": coverage_level,
                "gap_score": round(gap_score, 1),
            })

    gap_df = pd.DataFrame(gap_rows)

    # Summary: total gap score per degree (higher = bigger overall mismatch)
    degree_summary = (
        gap_df.groupby(["degree", "primary_job_sector"])["gap_score"]
        .sum()
        .reset_index()
        .sort_values("gap_score", ascending=False)
    )

    print("=== TOP 10 DEGREES WITH LARGEST SKILL GAPS (within their primary sector) ===")
    print(degree_summary.head(10))

    print("\n=== EXAMPLE: B.Sc Mathematics gap detail ===")
    print(gap_df[gap_df["degree"] == "B.Sc Mathematics"].sort_values("gap_score", ascending=False))

    os.makedirs("data/processed", exist_ok=True)
    gap_df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved detailed gap data to {OUTPUT_PATH}")