thonfrom datetime import datetime
from typing import Any, Dict, List
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from utils.logging_utils import get_logger

LOGGER = get_logger("salary_parser")

def _extract_domain(url: str) -> str:
    parsed = urlparse(url)
    return parsed.netloc or "indeed.com"

def parse_salaries_page(html: str, base_url: str) -> List[Dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    records: List[Dict[str, Any]] = []

    header_section = soup.select_one(".salary-header")
    footer_section = soup.select_one(".salary-footer")
    category_sections = soup.select(".salary-category")

    salary_header = None
    if header_section:
        title_tag = header_section.find("h1") or header_section.find("h2")
        updated_tag = header_section.find(class_="salary-last-updated")
        count_tag = header_section.find(class_="salary-count")
        salary_header = {
            "headerText": title_tag.get_text(strip=True) if title_tag else None,
            "formattedLastUpdateDate": updated_tag.get_text(strip=True) if updated_tag else None,
            "totalSalaryCount": int(count_tag.get_text(strip=True).split()[0]) if count_tag else None,
        }

    salary_footer = None
    if footer_section:
        footer_title = footer_section.find("h2") or footer_section.find("h3")
        count_tag = footer_section.find(class_="salary-count")
        salary_footer = {
            "footerTitleText": footer_title.get_text(strip=True) if footer_title else None,
            "salaryCount": int(count_tag.get_text(strip=True).split()[0]) if count_tag else None,
        }

    categories = []
    for category in category_sections:
        category_title_tag = category.find(class_="salary-category-title") or category.find("h3")
        salary_rows = category.select(".salary-row")
        salaries = []
        for row in salary_rows:
            title_tag = row.find(class_="salary-role-title")
            value_tag = row.find(class_="salary-role-value")
            count_tag = row.find(class_="salary-role-count")
            salaries.append(
                {
                    "title": title_tag.get_text(strip=True) if title_tag else None,
                    "salary": value_tag.get_text(strip=True) if value_tag else None,
                    "salaryType": "YEARLY",
                    "reportedSalaryCount": int(count_tag.get_text(strip=True).split()[0]) if count_tag else None,
                }
            )

        categories.append(
            {
                "categoryTitle": category_title_tag.get_text(strip=True) if category_title_tag else None,
                "salaries": salaries,
            }
        )

    salary_metadata = {
        "salaryHeader": salary_header,
        "salaryFooter": salary_footer,
        "categorySalarySection": {
            "categories": categories,
        },
    }

    salary_cards = soup.select(".salary-card")
    for card in salary_cards:
        title_tag = card.find(class_="salary-title")
        role_title = title_tag.get_text(strip=True) if title_tag else None
        snippet_tag = card.find(class_="salary-snippet")
        subtitle_tag = card.find(class_="salary-subtitle")

        record: Dict[str, Any] = {
            "sectionType": "salaries",
            "companyName": None,
            "title": role_title,
            "formattedSalary": snippet_tag.get_text(strip=True) if snippet_tag else None,
            "subtitle": subtitle_tag.get_text(strip=True) if subtitle_tag else None,
            "jobKey": None,
            "snippet": snippet_tag.get_text(strip=True) if snippet_tag else None,
            "sponsored": False,
            "urgentHire": False,
            "scrapedAt": datetime.utcnow().isoformat(),
            "_metadata": salary_metadata,
            "domain": _extract_domain(base_url),
        }
        records.append(record)

    return records