thonimport argparse
import json
import logging
from pathlib import Path
from typing import Any, Dict, List

from utils.logging_utils import get_logger
from utils.http_client import HttpClient
from utils.date_utils import parse_date_to_iso
from crawlers.company_reviews_crawler import CompanyReviewsCrawler
from crawlers.jobs_crawler import JobsCrawler
from crawlers.salaries_crawler import SalariesCrawler
from crawlers.interviews_crawler import InterviewsCrawler
from crawlers.faq_crawler import FaqCrawler
from pipelines.storage_pipeline import StoragePipeline
from pipelines.monitoring_pipeline import MonitoringPipeline

LOGGER = get_logger("main")

def load_json(path: Path) -> Any:
    if not path.exists():
        LOGGER.warning("JSON file %s does not exist, returning empty structure", path)
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def detect_section_type(url: str) -> str:
    lowered = url.lower()
    if "/reviews" in lowered:
        return "reviews"
    if "/jobs" in lowered or "/cmp/" in lowered and "/jobs" in lowered:
        return "jobs"
    if "/salaries" in lowered:
        return "salaries"
    if "/interviews" in lowered:
        return "interviews"
    if "/faq" in lowered:
        return "faq"
    # default to snapshot/about
    return "about"

def build_crawlers(http_client: HttpClient, config: Dict[str, Any]) -> Dict[str, Any]:
    target_date = config.get("targetDate")
    if target_date:
        target_date = parse_date_to_iso(target_date)

    monitoring_enabled = bool(config.get("monitoringModeForReviews", False))
    monitoring_state_path = config.get("monitoringStatePath", "data/monitoring_state.json")

    crawlers: Dict[str, Any] = {
        "reviews": CompanyReviewsCrawler(
            http_client=http_client,
            target_date=target_date,
        ),
        "jobs": JobsCrawler(http_client=http_client),
        "salaries": SalariesCrawler(http_client=http_client),
        "interviews": InterviewsCrawler(http_client=http_client),
        "faq": FaqCrawler(http_client=http_client),
        "about": CompanyReviewsCrawler(
            http_client=http_client,
            target_date=target_date,
            treat_as_about=True,
        ),
    }

    crawlers["_monitoring"] = MonitoringPipeline(
        state_file=Path(monitoring_state_path),
        enabled=monitoring_enabled,
    )
    return crawlers

def process_input(
    input_data: Dict[str, Any],
    crawlers: Dict[str, Any],
    storage: StoragePipeline,
) -> None:
    items: List[Dict[str, Any]] = []

    companies = input_data.get("companies") or input_data.get("items") or []
    if not isinstance(companies, list):
        LOGGER.error("Invalid input format: expected 'companies' or 'items' list")
        return

    monitoring: MonitoringPipeline = crawlers["_monitoring"]

    for record in companies:
        url = record.get("url")
        if not url:
            LOGGER.warning("Skipping record without URL: %s", record)
            continue

        section_type = record.get("sectionType") or detect_section_type(url)
        crawler = crawlers.get(section_type)
        if not crawler:
            LOGGER.warning("No crawler registered for sectionType=%s, url=%s", section_type, url)
            continue

        LOGGER.info("Crawling %s (%s)", url, section_type)
        try:
            crawled = crawler.crawl(url=url)
        except Exception as exc:  # noqa: BLE001
            LOGGER.exception("Failed to crawl %s: %s", url, exc)
            continue

        if not crawled:
            LOGGER.info("No items returned for %s", url)
            continue

        if section_type == "reviews" and monitoring.enabled:
            LOGGER.debug("Applying monitoring filter for reviews")
            crawled = monitoring.filter_new_reviews(crawled)

        if not crawled:
            LOGGER.info("No new items for %s after monitoring", url)
            continue

        for item in crawled:
            item.setdefault("sectionType", section_type)
            items.append(item)

    if items:
        storage.save(items)
        monitoring.persist_state()
    else:
        LOGGER.info("No items collected; nothing to save")

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Indeed company intelligence scraper (reviews, jobs, salaries, interviews, FAQ)."
    )
    parser.add_argument(
        "--input",
        type=str,
        default="data/sample_input.json",
        help="Path to input JSON describing companies and URLs.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/sample_output.json",
        help="Path to output JSON file for scraped results.",
    )
    parser.add_argument(
        "--settings",
        type=str,
        default="src/config/settings.example.json",
        help="Path to settings JSON file.",
    )
    parser.add_argument(
        "--proxies",
        type=str,
        default="src/config/proxies.example.json",
        help="Path to proxies JSON file.",
    )
    return parser.parse_args()

def main() -> None:
    args = parse_args()

    project_root = Path(__file__).resolve().parents[1]