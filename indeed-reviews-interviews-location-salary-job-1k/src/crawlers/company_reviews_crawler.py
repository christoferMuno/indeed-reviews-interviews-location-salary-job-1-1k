thonfrom typing import Any, Dict, List, Optional

from utils.logging_utils import get_logger
from utils.pagination import generate_page_urls
from utils.date_utils import parse_date_to_iso, is_on_or_after
from utils.http_client import HttpClient
from parsers.review_parser import parse_reviews_page

LOGGER = get_logger("company_reviews_crawler")

class CompanyReviewsCrawler:
    def __init__(
        self,
        http_client: HttpClient,
        target_date: Optional[str] = None,
        treat_as_about: bool = False,
    ) -> None:
        self.http_client = http_client
        self.target_date_iso = target_date
        self.treat_as_about = treat_as_about

    def _filter_by_date(self, reviews: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not self.target_date_iso:
            return reviews

        filtered: List[Dict[str, Any]] = []
        for review in reviews:
            submission = review.get("reviewSubmissionDate")
            review_date_iso = parse_date_to_iso(submission) if submission else None
            if not review_date_iso:
                filtered.append(review)
                continue
            if is_on_or_after(review_date_iso, self.target_date_iso):
                filtered.append(review)
        return filtered

    def crawl(self, url: str) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        seen_urls = set()

        for page_url in generate_page_urls(url, max_pages=25):
            if page_url in seen_urls:
                continue
            seen_urls.add(page_url)

            LOGGER.debug("Fetching reviews page %s", page_url)
            html = self.http_client.fetch(page_url)
            parsed = parse_reviews_page(html, base_url=page_url, treat_as_about=self.treat_as_about)

            if not parsed:
                LOGGER.info("No reviews found on %s, stopping pagination", page_url)
                break

            results.extend(parsed)

        results = self._filter_by_date(results)
        LOGGER.info("Collected %d review/summary records from %s", len(results), url)
        return results