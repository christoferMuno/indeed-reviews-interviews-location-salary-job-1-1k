thonfrom typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from utils.logging_utils import get_logger

LOGGER = get_logger("company_parser")

def _extract_domain(url: str) -> str:
    parsed = urlparse(url)
    host = parsed.netloc or ""
    return host or "indeed.com"

def parse_company_snapshot(html: str, base_url: str) -> Dict[str, Any]:
    soup = BeautifulSoup(html, "html.parser")

    company_name_tag = soup.find(attrs={"data-testid": "companyName"}) or soup.find("h1")
    company_name = company_name_tag.get_text(strip=True) if company_name_tag else None

    rating_tag = soup.find(attrs={"data-testid": "rating"})
    try:
        aggregate_rating = float(rating_tag.get_text(strip=True).split()[0]) if rating_tag else None
    except ValueError:
        aggregate_rating = None

    company_url_tag = soup.find("a", attrs={"data-tn-element": "companyLink"}) or soup.find("a", href=True)
    company_url = company_url_tag["href"] if company_url_tag else base_url

    snapshot = {
        "sectionType": "snapshot",
        "companyName": company_name,
        "companyUrl": company_url,
        "domain": _extract_domain(base_url),
        "aggregateRating": aggregate_rating,
        "scrapedAt": None,
    }

    return snapshot

def parse_faq_page(html: str, base_url: str) -> List[Dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    items: List[Dict[str, Any]] = []

    faqs = soup.select(".faq-item, [data-testid='faq-item']")
    if not faqs:
        LOGGER.debug("No FAQ items detected on %s", base_url)
        return items

    for faq in faqs:
        question_tag = faq.find(class_="faq-question") or faq.find("h2")
        answer_tag = faq.find(class_="faq-answer") or faq.find("p")

        question = question_tag.get_text(strip=True) if question_tag else None
        answer = answer_tag.get_text(" ", strip=True) if answer_tag else None

        if not question and not answer:
            continue

        items.append(
            {
                "sectionType": "faq",
                "companyName": None,
                "companyUrl": base_url,
                "domain": _extract_domain(base_url),
                "faqQuestions": question,
                "faqAnswers": answer,
            }
        )

    return items