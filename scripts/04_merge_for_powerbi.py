"""
04_merge_for_powerbi.py

Prepares clean, Power BI-ready exports from all three analysis layers.
Output: outputs/powerbi/ (clean CSVs Power BI can import directly)
"""

import pandas as pd
import os

SKILL_DEMAND_PATH = "data/processed/skill_demand_summary.csv"
CATEGORY_BREAKDOWN_PATH = "data/processed/category_skill_breakdown.csv"
SKILL_GAP_PATH = "data/processed/skill_gap_by_degree.csv"
DEGREE_COVERAGE_PATH = "data/lookup/degree_skill_coverage.csv"

OUTPUT_DIR = "outputs/powerbi"

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    skill_demand_df = pd.read_csv(SKILL_DEMAND_PATH)
    skill_demand_df.to_csv(f"{OUTPUT_DIR}/skill_demand_overall.csv", index=False)
    print(f"Exported skill_demand_overall.csv - {len(skill_demand_df)} rows")

    category_df = pd.read_csv(CATEGORY_BREAKDOWN_PATH)
    category_df.to_csv(f"{OUTPUT_DIR}/skill_by_category.csv", index=False)
    print(f"Exported skill_by_category.csv - {len(category_df)} rows")

    gap_df = pd.read_csv(SKILL_GAP_PATH)
    gap_df.to_csv(f"{OUTPUT_DIR}/skill_gap_detailed.csv", index=False)
    print(f"Exported skill_gap_detailed.csv - {len(gap_df)} rows")

    degree_summary_df = (
        gap_df.groupby(["degree", "primary_job_sector"])["gap_score"]
        .sum()
        .reset_index()
        .sort_values("gap_score", ascending=False)
    )
    degree_summary_df.to_csv(f"{OUTPUT_DIR}/skill_gap_by_degree_summary.csv", index=False)
    print(f"Exported skill_gap_by_degree_summary.csv - {len(degree_summary_df)} rows")

    coverage_df = pd.read_csv(DEGREE_COVERAGE_PATH, keep_default_na=False)
    coverage_df.to_csv(f"{OUTPUT_DIR}/degree_skill_coverage.csv", index=False)
    print(f"Exported degree_skill_coverage.csv - {len(coverage_df)} rows")

    print(f"\nAll files ready in {OUTPUT_DIR}/ - import these directly into Power BI")