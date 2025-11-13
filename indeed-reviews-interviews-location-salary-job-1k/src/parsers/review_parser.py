thonfrom datetime import datetime
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from utils.logging_utils import get_logger

LOGGER = get_logger("review_parser")

def _extract_domain(url: str) -> str:
    parsed = urlparse(url)
    return parsed.netloc or "indeed.com"

def _normalize_rating(text: str) -> Optional[float]:
    try:
        return float(text.strip().split()[0])
    except (ValueError, AttributeError, IndexError):
        return None

def parse_reviews_page(html: str, base_url: str, treat_as_about: bool = False) -> List[Dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    records: List[Dict[str, Any]] = []

    if treat_as_about:
        # For about/snapshot pages we focus on summary metrics
        summary = soup.find(attrs={"data-testid": "company-summary"})
        company_name_tag = soup.find(attrs={"data-testid": "companyName"}) or soup.find("h1")
        company_name = company_name_tag.get_text(strip=True) if company_name_tag else None
        rating_tag = summary.find(attrs={"data-testid": "rating"}) if summary else None

        record: Dict[str, Any] = {
            "sectionType": "about",
            "companyName": company_name,
            "companyUrl": base_url,
            "domain": _extract_domain(base_url),
            "aggregateRating": _normalize_rating(rating_tag.get_text() if rating_tag else ""),
            "scrapedAt": datetime.utcnow().isoformat(),
        }
        records.append(record)
        return records

    review_nodes = soup.select(".review, [data-testid='review-card']")
    if not review_nodes:
        LOGGER.debug("No review nodes detected on %s", base_url)
        return records

    for node in review_nodes:
        title_tag = node.find(class_="review-title") or node.find("h2")
        body_tag = node.find(class_="review-body") or node.find("p")
        rating_tag = node.find(class_="review-rating") or node.find(attrs={"data-testid": "rating"})
        job_title_tag = node.find(class_="review-author-title")
        status_tag = node.find(class_="review-author-status")
        location_tag = node.find(class_="review-location")
        date_tag = node.find(class_="review-date")

        record: Dict[str, Any] = {
            "companyName": None,
            "companyUrl": base_url,
            "domain": _extract_domain(base_url),
            "sectionType": "reviews",
            "aggregateRating": None,
            "ratingDistribution": None,
            "reviewTitle": title_tag.get_text(strip=True) if title_tag else None,
            "reviewBody": body_tag.get_text(" ", strip=True) if body_tag else None,
            "reviewRatingOverall": _normalize_rating(rating_tag.get_text() if rating_tag else ""),
            "reviewCategoryRatings": None,
            "reviewAuthorJobTitle": job_title_tag.get_text(strip=True) if job_title_tag else None,
            "reviewAuthorStatus": status_tag.get_text(strip=True) if status_tag else None,
            "reviewLocation": location_tag.get_text(strip=True) if location_tag else None,
            "reviewSubmissionDate": date_tag.get_text(strip=True) if date_tag else None,
            "reviewHelpfulVotes": None,
            "companyResponse": None,
            "scrapedAt": datetime.utcnow().isoformat(),
        }

        records.append(record)

    return records