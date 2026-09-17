"""
00_extract_adzuna_jobs.py

Pulls job postings from the Adzuna API for Tamil Nadu, India.
Stops automatically when pages stop returning new unique postings
(same dedup-and-stop pattern used in the Flipkart tracker project).

Output: data/raw/adzuna_tamilnadu_jobs_raw.csv
"""

import requests
import pandas as pd
import time
import os
from dotenv import load_dotenv

# Load API credentials from .env file (never hardcode keys in scripts)
load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

if not APP_ID or not APP_KEY:
    raise ValueError(
        "Missing Adzuna credentials. Create a .env file in the project root "
        "with ADZUNA_APP_ID=... and ADZUNA_APP_KEY=..."
    )

OUTPUT_PATH = "data/raw/adzuna_tamilnadu_jobs_raw.csv"
LOCATION = "Tamil Nadu"
RESULTS_PER_PAGE = 20
MAX_PAGES = 100                  # hard ceiling so we never overshoot the free-tier quota
DUPLICATE_PAGE_LIMIT = 3         # stop after this many consecutive pages add zero new jobs


def extract_jobs():
    all_jobs = []
    seen_jobs = set()
    consecutive_duplicate_pages = 0

    for page in range(1, MAX_PAGES + 1):
        url = f"https://api.adzuna.com/v1/api/jobs/in/search/{page}"
        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "where": LOCATION,
            "results_per_page": RESULTS_PER_PAGE,
            "content-type": "application/json",
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"Failed at page {page}: {response.status_code} - {response.text[:200]}")
            break

        data = response.json()
        total_count = data.get("count")
        results = data.get("results", [])

        if not results:
            print(f"No results at page {page}. Stopping.")
            break

        new_jobs_this_page = 0

        for job in results:
            key = (
                job.get("title"),
                job.get("company", {}).get("display_name"),
                job.get("location", {}).get("display_name"),
            )

            if key in seen_jobs:
                continue

            seen_jobs.add(key)
            new_jobs_this_page += 1

            all_jobs.append({
                "title": job.get("title"),
                "company": job.get("company", {}).get("display_name"),
                "location": job.get("location", {}).get("display_name"),
                "category": job.get("category", {}).get("label"),
                "salary_min": job.get("salary_min"),
                "salary_max": job.get("salary_max"),
                "contract_type": job.get("contract_type"),
                "description": job.get("description"),
                "created": job.get("created"),
                "redirect_url": job.get("redirect_url"),
            })

        print(f"Page {page}: {new_jobs_this_page} new unique jobs. "
              f"Running total: {len(all_jobs)} / Adzuna reports {total_count} total available")

        if new_jobs_this_page == 0:
            consecutive_duplicate_pages += 1
            print(f"  -> Duplicate streak: {consecutive_duplicate_pages}/{DUPLICATE_PAGE_LIMIT}")
            if consecutive_duplicate_pages >= DUPLICATE_PAGE_LIMIT:
                print(f"Stopping: {DUPLICATE_PAGE_LIMIT} consecutive pages with no new data.")
                break
        else:
            consecutive_duplicate_pages = 0

        time.sleep(1)  # be polite to the API, avoid rate limits

    return pd.DataFrame(all_jobs)


if __name__ == "__main__":
    df = extract_jobs()

    print("\nFinal total UNIQUE jobs pulled:", len(df))
    if len(df) > 0 and "category" in df.columns:
        print("\nCategory breakdown:")
        print(df["category"].value_counts())

    os.makedirs("data/raw", exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved to {OUTPUT_PATH}")