<div align="center">

![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=28&pause=1000&color=1C4D63&center=true&vCenter=true&width=600&lines=Career+Pathway+Intelligence;Mapping+Degrees+to+Real+Job+Market+Demand;Tamil+Nadu+Job+Market+Analysis)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![n8n](https://img.shields.io/badge/n8n-EA4B71?style=for-the-badge&logo=n8n&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

</div>

---

## The Business Problem

Graduates in Tamil Nadu often choose a degree or upskilling path with little visibility into real market demand. This project answers, with evidence from live job market data:

> *"Given my degree, which career domains can I realistically pursue, and what skills do I need to build to enter them?"*

---

## What This Project Does

1. **Extracts** real job postings across Tamil Nadu via the Adzuna API (official, free tier)
2. **Tags** every posting with matched skills, using a 78-term taxonomy built from real Indian job posting patterns (Glassdoor, Internshala) across IT & Data, Accounting & Finance, Sales & Marketing, HR & Admin, and Customer Service
3. **Aggregates** skill demand — overall and per job category
4. **Compares** real market demand against what 55+ UG/PG degree programs actually teach, using an official University of Madras B.Sc Mathematics syllabus as the fully-cited gold-standard reference point
5. **Visualizes** everything in a 5-page interactive Power BI dashboard
6. **Automates** the entire pipeline weekly via n8n, with success/failure email alerts

---

## Architecture

---

## Key Findings

- **IT Jobs is the single largest category** in Tamil Nadu's job market by posting volume, ahead of Sales, Engineering, and Accounting & Finance
- Within IT Jobs specifically, **Java, Python, JavaScript, and SQL** are the most consistently requested skills
- **B.Sc Mathematics** graduates hold a strong statistics/logic foundation, but the syllabus (verified against the official University of Madras curriculum) offers **only elective, non-guaranteed exposure** to programming and zero exposure to SQL, Excel, or BI tools — despite these being in active market demand
- Soft skills like **Leadership and Communication** rank above several hard technical skills in overall posting frequency

---

## Data Sources & Honest Assumptions

- **Job postings:** Adzuna API (India, Tamil Nadu) — official, free tier
- **Skill taxonomy:** Built from real skill patterns in current Indian job postings — not exhaustive, but grounded in genuine sources
- **Degree eligibility mapping:** General domain knowledge (AI-assisted reference), indicative rather than sourced from an official regulatory body — except the B.Sc Mathematics curriculum analysis, which is directly cited from the official University of Madras syllabus
- **Company field:** ~5% of postings have no disclosed employer, consistent with recruitment-agency listings that intentionally omit the hiring company
- **Salary data intentionally excluded** — Adzuna salary figures are sometimes platform-estimated rather than employer-stated; this project prioritizes claims that can be fully defended over completeness
- **Skill extraction method:** Regex/keyword matching, not AI/LLM classification — chosen deliberately for full explainability and reproducibility over black-box accuracy

---

## Project Structure

---

## Setup

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
cp .env.example .env            # then add your real Adzuna credentials
```

Run the pipeline in order:

```bash
python scripts/00_extract_adzuna_jobs.py
python scripts/01_extract_skills.py
python scripts/02_build_kpi_summary.py
python scripts/03_skill_gap_analysis.py
python scripts/04_merge_for_powerbi.py
python scripts/04_job_listing.py
```

---

## Automation

The full pipeline runs weekly via n8n — extraction through Power BI export — with automated success/failure email notifications, so data freshness never depends on manual execution.

---

<div align="center">

### Author

**Bernad Meckenzi S**
Aspiring Data Analyst / BI Analyst

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Bernad2304)

</div>
