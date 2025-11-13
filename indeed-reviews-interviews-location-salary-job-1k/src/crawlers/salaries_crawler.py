thonfrom typing import Any, Dict, List

from utils.logging_utils import get_logger
from utils.pagination import generate_page_urls
from utils.http_client import HttpClient
from parsers.salary_parser import parse_salaries_page

LOGGER = get_logger("salaries_crawler")

class SalariesCrawler:
    def __init__(self, http_client: HttpClient) -> None:
        self.http_client = http_client

    def crawl(self, url: str) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        seen_urls = set()

        for page_url in generate_page_urls(url, max_pages=10):
            if page_url in seen_urls:
                continue
            seen_urls.add(page_url)

            LOGGER.debug("Fetching salaries page %s", page_url)
            html = self.http_client.fetch(page_url)
            parsed = parse_salaries_page(html, base_url=page_url)
            if not parsed:
                LOGGER.info("No salaries found on %s, stopping pagination", page_url)
                break

            results.extend(parsed)

        LOGGER.info("Collected %d salary records from %s", len(results), url)
        return results