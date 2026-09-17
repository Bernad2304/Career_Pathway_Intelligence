import pandas as pd
import ast

df = pd.read_csv("data/processed/adzuna_tn_jobs_with_skills.csv")

# Fix 1: skills_found is currently a string like "['SQL', 'Excel']" - convert to a clean comma-separated text
def clean_skills_list(value):
    try:
        skills_list = ast.literal_eval(value)
        return ", ".join(skills_list) if skills_list else "None Matched"
    except (ValueError, SyntaxError):
        return "None Matched"

df["skills_found_clean"] = df["skills_found"].apply(clean_skills_list)

# Fix 2: trim description to first 300 characters so Power BI doesn't bloat with huge text blocks
df["description_short"] = df["description"].fillna("").str[:300] + "..."

# Fix 3: fill blank company with a clear label instead of leaving it empty
df["company"] = df["company"].fillna("Not Disclosed (Agency Listing)")

# Keep only the columns actually useful in Power BI
powerbi_ready = df[[
    "title", "company", "location", "category",
    "contract_type", "created", "skills_found_clean",
    "skill_count", "description_short", "redirect_url"
]]

powerbi_ready.to_csv("outputs/powerbi/job_postings_detail.csv", index=False)
print(f"Saved {len(powerbi_ready)} cleaned rows to outputs/powerbi/job_postings_detail.csv")