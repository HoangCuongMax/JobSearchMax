#!/usr/bin/env python3
"""
Job Crawler - Fetches jobs from multiple platforms daily
Stores data locally for dashboard analysis
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import requests
from typing import List, Dict
import re

# Data storage
DATA_DIR = Path("job_data")
DATA_DIR.mkdir(exist_ok=True)
JOBS_FILE = DATA_DIR / "jobs.json"
SOURCES_FILE = DATA_DIR / "sources.json"

class JobCrawler:
    def __init__(self):
        self.jobs = self.load_jobs()
        self.sources = self.load_sources()
        
    def load_jobs(self) -> List[Dict]:
        """Load existing jobs from file"""
        if JOBS_FILE.exists():
            with open(JOBS_FILE, 'r') as f:
                return json.load(f)
        return []
    
    def load_sources(self) -> Dict:
        """Load job source URLs"""
        if SOURCES_FILE.exists():
            with open(SOURCES_FILE, 'r') as f:
                return json.load(f)
        # Default sources - user can customize in sources.json
        return {
            "seek": [],
            "indeed": [],
            "linkedin": [],
            "custom_urls": []
        }
    
    def save_jobs(self):
        """Save jobs to file"""
        with open(JOBS_FILE, 'w') as f:
            json.dump(self.jobs, f, indent=2)
    
    def save_sources(self):
        """Save sources configuration"""
        with open(SOURCES_FILE, 'w') as f:
            json.dump(self.sources, f, indent=2)
    
    def create_job_entry(self, title: str, company: str, location: str, 
                        salary: str, url: str, platform: str, 
                        description: str = "") -> Dict:
        """Create a standardized job entry"""
        return {
            "id": f"{platform}_{datetime.now().timestamp()}",
            "title": title,
            "company": company,
            "location": location,
            "salary": salary,
            "url": url,
            "platform": platform,
            "description": description,
            "date_found": datetime.now().isoformat(),
            "date_applied": None,
            "status": "new",  # new, interested, applied, rejected
            "relevance_score": 0,
            "notes": ""
        }
    
    def crawl_seek(self, query: str, location: str):
        """
        Crawl Seek.com.au
        Note: Seek has anti-scraping measures. Using search URLs.
        """
        try:
            # Build Seek search URL
            search_url = f"https://www.seek.com.au/{query}-jobs"
            if location:
                search_url += f"/in-{location.replace(' ', '-')}"
            
            print(f"⚠️  To crawl Seek properly, please use: {search_url}")
            print("   Seek has anti-scraping measures. Consider using their job alerts instead.")
            
        except Exception as e:
            print(f"❌ Seek crawl failed: {e}")
    
    def crawl_indeed(self, query: str, location: str):
        """
        Crawl Indeed
        Note: Using API-like approach. Indeed has restrictions on scraping.
        """
        try:
            # Indeed has restrictions - recommend using their API or job alerts
            search_url = f"https://au.indeed.com/jobs?q={query}"
            if location:
                search_url += f"&l={location}"
            
            print(f"⚠️  To crawl Indeed, visit: {search_url}")
            print("   Consider setting up job alerts for automated updates.")
            
        except Exception as e:
            print(f"❌ Indeed crawl failed: {e}")
    
    def crawl_custom_urls(self):
        """
        Crawl custom job board URLs
        For smaller sites, job listing pages, etc.
        """
        for url in self.sources.get("custom_urls", []):
            try:
                print(f"Crawling custom URL: {url}")
                # In production, use BeautifulSoup or Scrapy
                # This is a placeholder for demonstration
                
            except Exception as e:
                print(f"❌ Custom URL crawl failed ({url}): {e}")
    
    def add_manual_job(self, job_data: Dict):
        """Add a job manually (for cases where auto-crawl doesn't work)"""
        job = self.create_job_entry(**job_data)
        # Check if job already exists
        if not any(j["url"] == job["url"] for j in self.jobs):
            self.jobs.append(job)
            self.save_jobs()
            print(f"✅ Added: {job['title']} at {job['company']}")
            return True
        return False
    
    def calculate_relevance_score(self, job: Dict, keywords: List[str]) -> float:
        """
        Calculate relevance score (0-100) based on keywords in title and description
        """
        if not keywords:
            return 50.0
        
        text = f"{job['title']} {job['description']}".lower()
        matches = sum(1 for keyword in keywords if keyword.lower() in text)
        score = (matches / len(keywords)) * 100
        return min(100, max(0, score))
    
    def parse_salary(self, salary_str: str) -> tuple:
        """Parse salary string to extract min and max"""
        if not salary_str:
            return (None, None)
        
        numbers = re.findall(r'\d+', salary_str.replace(',', ''))
        if len(numbers) >= 2:
            return (int(numbers[0]), int(numbers[1]))
        elif len(numbers) == 1:
            return (int(numbers[0]), int(numbers[0]))
        return (None, None)
    
    def run_daily_crawl(self):
        """Main crawl routine - run this daily via scheduler"""
        print(f"\n🔄 Starting job crawl at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Crawl custom URLs (user-configured)
        self.crawl_custom_urls()
        
        # For Seek and Indeed, recommend setting up job alerts
        print("\n📧 Recommended: Set up job alerts on Seek and Indeed")
        print("   Export the JSON and add via add_manual_job() or update sources.json")
        
        print(f"✅ Crawl complete. Total jobs: {len(self.jobs)}")
    
    def export_for_dashboard(self, keywords: List[str] = None) -> str:
        """Export jobs as JSON string for dashboard"""
        jobs_with_scores = []
        
        for job in self.jobs:
            job_copy = job.copy()
            
            # Calculate relevance score
            if keywords:
                job_copy["relevance_score"] = self.calculate_relevance_score(job, keywords)
            
            # Parse salary
            min_sal, max_sal = self.parse_salary(job["salary"])
            job_copy["salary_min"] = min_sal
            job_copy["salary_max"] = max_sal
            
            jobs_with_scores.append(job_copy)
        
        return json.dumps(jobs_with_scores)

if __name__ == "__main__":
    crawler = JobCrawler()
    
    # Example: Add a manual job entry
    # crawler.add_manual_job({
    #     "title": "Senior Data Engineer",
    #     "company": "TechCorp",
    #     "location": "Sydney, NSW",
    #     "salary": "$120,000 - $160,000",
    #     "url": "https://example.com/jobs/123",
    #     "platform": "linkedin",
    #     "description": "Looking for Python and SQL expert with AWS experience"
    # })
    
    # Run the daily crawl
    crawler.run_daily_crawl()
