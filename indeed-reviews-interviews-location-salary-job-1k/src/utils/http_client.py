thonimport json
import random
import time
from typing import Any, Dict, Optional

import requests
from requests import Response, Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from utils.logging_utils import get_logger

LOGGER = get_logger("http_client")

class HttpClient:
    def __init__(
        self,
        default_timeout: int = 30,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
        proxies_config: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.default_timeout = default_timeout
        self.session = self._build_session(max_retries=max_retries, backoff_factor=backoff_factor)
        self.proxies_config = proxies_config or {}
        self.default_headers = {
            "User-Agent": "Mozilla/5.0 (compatible; BitbashIndeedScraper/1.0; +https://bitbash.dev)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }

    def _build_session(self, max_retries: int, backoff_factor: float) -> Session:
        session = requests.Session()
        retries = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=(500, 502, 503, 504),
            allowed_methods=frozenset(["GET", "HEAD"]),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def _choose_proxy(self) -> Optional[Dict[str, str]]:
        if not self.proxies_config.get("enabled"):
            return None

        proxies = self.proxies_config.get("proxies") or []
        if not proxies:
            return None

        preferred_country = self.proxies_config.get("preferredCountry")
        if preferred_country:
            filtered = [
                p for p in proxies if preferred_country in (p.get("countries") or [])
            ]
            if filtered:
                proxies = filtered

        choice = random.choice(proxies)
        return {
            "http": choice.get("http"),
            "https": choice.get("https"),
        }

    def fetch(self, url: str, timeout: Optional[int] = None) -> str:
        timeout = timeout or self.default_timeout
        proxies = self._choose_proxy()
        try:
            LOGGER.debug("Requesting %s with timeout=%s", url, timeout)
            response: Response = self.session.get(
                url,
                timeout=timeout,
                headers=self.default_headers,
                proxies=proxies,
            )
            response.raise_for_status()
            return response.text
        except requests.RequestException as exc:  # noqa: BLE001
            LOGGER.error("HTTP error for %s: %s", url, exc)
            raise