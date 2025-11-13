thonfrom typing import Any, Dict, List

from utils.logging_utils import get_logger
from utils.http_client import HttpClient
from parsers.company_parser import parse_faq_page

LOGGER = get_logger("faq_crawler")

class FaqCrawler:
    def __init__(self, http_client: HttpClient) -> None:
        self.http_client = http_client

    def crawl(self, url: str) -> List[Dict[str, Any]]:
        LOGGER.debug("Fetching FAQ page %s", url)
        html = self.http_client.fetch(url)
        parsed = parse_faq_page(html, base_url=url)
        LOGGER.info("Collected %d FAQ records from %s", len(parsed), url)
        return parsed