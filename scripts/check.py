import pandas as pd

df = pd.read_csv("data/processed/adzuna_tn_jobs_with_skills.csv")

blank_company = df[df["company"].isna()]
print(f"Blank company: {len(blank_company)} / {len(df)} total postings")
print()
print("Sample titles with blank company:")
print(blank_company["title"].head(10))
print()
print("Sample description snippet (first 200 chars) of a blank-company posting:")
print(blank_company["description"].iloc[0][:200])