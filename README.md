# Job Opportunity Dashboard
**Python · JSON data preparation · Browser-based reporting**

A prototype for organising job opportunities, comparing them with keyword preferences and tracking application status.

The project combines a Python helper with a React dashboard delivered as a single HTML file. Job data is imported manually; the collection functions are scaffolding for future integrations.

[Max's profile](https://github.com/HoangCuongMax) · [Analytics portfolio](https://docs.google.com/document/d/1Wpe37bPnb0mcX5V31LvC8BOflCZGgFB-xNno3ke_8qc)

## What the project demonstrates

- Structuring job records into a consistent JSON format.
- Adding manual records and checking existing URLs for duplicates.
- Calculating a transparent keyword-match score.
- Filtering opportunities by location, salary, source and status.
- Summarising filtered records and tracking application status in the dashboard.

The score is the percentage of supplied keywords found in the title or description. It is a rule-based match score, not a trained AI model or a probability of suitability.

## Try the dashboard

1. Clone or download this repository.
2. Open [`job_dashboard.html`](job_dashboard.html) in a browser.
3. Select **Import Jobs** and paste the contents of [`sample_jobs.json`](sample_jobs.json).
4. Enter comma-separated keywords and explore the filters.
5. Use the status controls to organise opportunities.

The dashboard loads React, React DOM and Babel from a public CDN, so it needs those resources to be available. It stores dashboard records in browser `localStorage`; the Python helper uses separate JSON files. There is no automatic synchronisation between them.

## Use the Python helper

Python 3 and `requests` are required by the current source.

```sh
git clone https://github.com/HoangCuongMax/JobSearchMax.git
cd JobSearchMax
python3 -m venv .venv
```

Activate the environment with `source .venv/bin/activate` on macOS/Linux, or `.venv\Scripts\Activate.ps1` in Windows PowerShell. Then:

```sh
python -m pip install requests
python job_crawler.py
```

The entry point creates the local data directory and runs the scaffold routine. It does not automatically fetch or populate live job listings.

For manual entry, use the helper from a Python session started in the repository folder:

```python
from job_crawler import JobCrawler

crawler = JobCrawler()
crawler.add_manual_job({
    "title": "Data Analyst",
    "company": "Example organisation",
    "location": "Darwin, NT",
    "salary": "$80,000 - $100,000",
    "url": "https://example.com/jobs/data-analyst",
    "platform": "manual",
    "description": "Power BI, SQL and Python reporting"
})
print(crawler.export_for_dashboard(["Power BI", "SQL", "Python"]))
```

Paste the exported JSON into the dashboard to include the parsed salary fields and calculated scores.

## Repository map

| File | Purpose |
| --- | --- |
| [`job_crawler.py`](job_crawler.py) | Record creation, local JSON storage, simple salary parsing and keyword scoring |
| [`job_dashboard.html`](job_dashboard.html) | Import, filtering, summaries and application tracking |
| [`sample_jobs.json`](sample_jobs.json) | Example records for a demonstration |
| [`sources.json.example`](sources.json.example) | Example source configuration |
| [`QUICKSTART.txt`](QUICKSTART.txt) | Earlier setup notes; use this README for current scope and limitations |

## Current scope & limitations

- Seek and Indeed helpers print suggested search URLs; the custom-URL crawler is a placeholder.
- Scheduling the helper does not turn these placeholders into working ingestion connectors.
- Salary parsing is simple numeric extraction and does not normalise currencies, hourly rates or shorthand such as "100k".
- Keyword scores depend on the supplied terms and do not measure professional suitability.
- Data is stored separately in the browser and local files. Back up records before clearing browser storage.
- Import validation, persistence behaviour and a fully tested end-to-end workflow need further development.

## Next development steps

Add schema validation, automated checks for imports and persistence, improved salary normalisation, and a documented permitted ingestion source. Measure the resulting workflow before claiming time savings or collection coverage.
