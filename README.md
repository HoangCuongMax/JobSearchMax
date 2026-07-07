# Job Crawler & Dashboard System

A fully automated job opportunity crawler with intelligent analysis, salary filtering, and relevance scoring.

## What You Get

✅ **Python Crawler** - Fetches jobs from multiple platforms daily  
✅ **Local Database** - Stores job data automatically  
✅ **Interactive Dashboard** - Beautiful HTML interface with advanced filtering  
✅ **Relevance Scoring** - AI-powered keyword matching (0-100%)  
✅ **Application Tracking** - Mark jobs as applied, interested, or rejected  
✅ **Salary Filtering** - Filter by minimum/maximum salary  
✅ **Location-Based Search** - Find jobs near you  

## Quick Start

### 1. Basic Setup

```bash
# Make the crawler executable
chmod +x job_crawler.py

# Create sample data directory
python job_crawler.py
```

This creates:
- `job_data/jobs.json` - Your job database
- `job_data/sources.json` - Your configured job URLs

### 2. Configure Job Sources

Edit `job_data/sources.json`:

```json
{
    "seek": [],
    "indeed": [],
    "linkedin": [],
    "custom_urls": [
        "https://careers.example.com/jobs",
        "https://anothercompany.com/careers",
        "https://jobboard.com.au/search?q=python"
    ]
}
```

### 3. Add Your First Jobs

You have two options:

**Option A: Manual Entry (Easiest)**

In the dashboard (job_dashboard.html), click "Import Jobs" and paste JSON:

```json
[
    {
        "title": "Senior Python Developer",
        "company": "TechCorp",
        "location": "Sydney, NSW",
        "salary": "$130,000 - $180,000",
        "url": "https://careers.techcorp.com/jobs/123",
        "platform": "linkedin",
        "description": "Looking for Python expert with Django experience and AWS knowledge"
    }
]
```

**Option B: Job Alerts**

Most job boards let you set up automated email alerts. When you receive alerts, you can:
1. Export the job data as JSON
2. Paste into the dashboard's import field
3. Boom - all jobs are now tracked

### 4. Set Up Daily Crawling

#### On Windows (Task Scheduler):

```batch
# Create a .bat file called run_crawler.bat
@echo off
cd C:\path\to\job-crawler
python job_crawler.py
```

Then:
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Daily at 9:00 AM
4. Set action: Run `run_crawler.bat`

#### On Mac/Linux (Cron):

```bash
# Edit your crontab
crontab -e

# Add this line to run daily at 9 AM:
0 9 * * * /usr/bin/python3 /path/to/job_crawler.py

# Or run every 6 hours:
0 */6 * * * /usr/bin/python3 /path/to/job_crawler.py
```

### 5. Use the Dashboard

1. **Open** `job_dashboard.html` in any web browser
2. **Import Jobs** - Paste JSON data from your crawler
3. **Filter & Analyze**:
   - Enter keywords (Python, Data, AWS) for relevance scoring
   - Filter by location, salary, platform
   - See which jobs match your criteria best
4. **Track Applications** - Mark jobs as Applied, Interested, or Rejected
5. **Notes** - Add personal notes to each job

## How It Works

### Relevance Scoring

The system calculates a match score (0-100%) based on:
- How many of your keywords appear in the job title
- How many keywords appear in the job description
- Normalized to show which jobs fit your profile best

**Example:**
- You search for: "Python, Data, AWS"
- Job mentions all three → **High relevance (75%+)** 🟢
- Job mentions two → **Medium relevance (50-75%)** 🟡
- Job mentions one → **Low relevance (<50%)** 🔴

### Salary Filtering

The system:
- Parses salary ranges like "$120,000 - $160,000"
- Filters jobs based on your salary preferences
- Shows average salary for filtered results

### Application Tracking

Statuses:
- **New** - Just discovered
- **Interested** - Worth applying to
- **Applied** - Already submitted
- **Rejected** - Not a fit

## File Structure

```
job-crawler/
├── job_crawler.py           # Main crawler script
├── job_dashboard.html       # Interactive dashboard (OPEN IN BROWSER)
├── job_data/
│   ├── jobs.json           # Your job database
│   └── sources.json        # Job source URLs
└── README.md               # This file
```

## Advanced Usage

### Programmatic Job Addition

In Python:

```python
from job_crawler import JobCrawler

crawler = JobCrawler()

# Add a single job
crawler.add_manual_job({
    "title": "Data Scientist",
    "company": "AI Corp",
    "location": "Melbourne, VIC",
    "salary": "$110,000 - $150,000",
    "url": "https://example.com/jobs/789",
    "platform": "linkedin",
    "description": "Machine learning expert needed for computer vision project"
})

# Run the crawler
crawler.run_daily_crawl()
```

### Custom Crawling

To add custom platform crawlers, extend the `JobCrawler` class:

```python
def crawl_custom_site(self):
    """Example custom crawler"""
    import requests
    from bs4 import BeautifulSoup
    
    response = requests.get("https://jobsite.com/listings")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for job_elem in soup.find_all('div', class_='job-listing'):
        job = self.create_job_entry(
            title=job_elem.find('h2').text,
            company=job_elem.find('span', class_='company').text,
            location=job_elem.find('span', class_='location').text,
            salary=job_elem.find('span', class_='salary').text,
            url=job_elem.find('a')['href'],
            platform='custom_site',
            description=job_elem.find('p').text
        )
        self.jobs.append(job)
    
    self.save_jobs()
```

## For Better Automated Crawling

Since most job boards restrict bot access, I recommend:

1. **Use job alert emails** - Have sites email you matches daily
2. **Export to JSON** - Use browser extensions or manual copy-paste
3. **Paste into dashboard** - Takes 30 seconds per batch

Popular extensions:
- **Save to Pocket** - Clips articles/jobs for later
- **Web Scraper** - Visual scraping without coding
- **Webhooks with Zapier** - IFTTT-style job automation

## Data Privacy

- All data is stored **locally** on your machine
- No cloud uploads or tracking
- Dashboard works **offline**
- You own your job data

## Troubleshooting

**Q: Dashboard won't load?**
A: Make sure you have `job_data/jobs.json` file. It should be created automatically on first run.

**Q: Jobs aren't importing?**
A: Make sure your JSON is valid. Test at https://jsonlint.com/

**Q: How do I backup my data?**
A: Copy the entire `job_data/` folder to another location.

**Q: Can I share this with others?**
A: Yes! Share the HTML file. Each person gets their own local data via browser storage.

## Next Steps

1. ✅ Set up daily crawling (Task Scheduler or Cron)
2. ✅ Configure your job source URLs in `sources.json`
3. ✅ Add your first batch of jobs via the dashboard
4. ✅ Set your keywords and filters
5. ✅ Start applying to high-relevance matches!

## Tips for Best Results

📌 **Keywords**: Be specific. "Python Django AWS" gets better scores than "IT"  
📌 **Updates**: Run crawler daily so you catch new postings fast  
📌 **Notes**: Add interview tips or company research to each job  
📌 **Filter Often**: Salary and location filters save hours of scrolling  
📌 **Track**: Mark applications so you don't apply twice  

---

**Happy job hunting! 🚀**

For questions or improvements, check the source code - it's well commented.
