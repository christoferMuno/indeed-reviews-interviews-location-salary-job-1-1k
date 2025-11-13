thonfrom datetime import datetime
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from utils.logging_utils import get_logger

LOGGER = get_logger("job_parser")

def _extract_domain(url: str) -> str:
    parsed = urlparse(url)
    return parsed.netloc or "indeed.com"

def parse_jobs_page(html: str, base_url: str) -> List[Dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    jobs: List[Dict[str, Any]] = []

    cards = soup.select(".job-card, [data-testid='job-card']")
    if not cards:
        LOGGER.debug("No job cards detected on %s", base_url)
        return jobs

    for card in cards:
        title_tag = card.find(class_="job-title") or card.find("h2")
        location_tag = card.find(class_="job-location")
        salary_tag = card.find(class_="job-salary")
        description_tag = card.find(class_="job-description")
        job_key = card.get("data-jobkey") or card.get("data-jk")

        job: Dict[str, Any] = {
            "sectionType": "jobs",
            "jobKey": job_key,
            "companyName": None,
            "title": title_tag.get_text(strip=True) if title_tag else None,
            "formattedSalary": salary_tag.get_text(strip=True) if salary_tag else None,
            "location": {
                "countryCode": None,
                "city": location_tag.get_text(strip=True) if location_tag else None,
                "fullAddress": location_tag.get_text(strip=True) if location_tag else None,
            },
            "url": base_url,
            "jobDescriptionHtml": str(description_tag) if description_tag else None,
            "jobDescriptionText": description_tag.get_text(" ", strip=True) if description_tag else None,
            "jobTypes": [],
            "shiftAndSchedule": [],
            "benefits": [],
            "attributes": [],
            "datePublished": None,
            "dateOnIndeed": int(datetime.utcnow().timestamp() * 1000),
            "expired": False,
            "scrapedAt": datetime.utcnow().isoformat(),
            "domain": _extract_domain(base_url),
        }

        jobs.append(job)

    return jobs