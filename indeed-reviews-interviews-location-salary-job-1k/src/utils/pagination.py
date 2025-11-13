thonfrom typing import Generator

def generate_page_urls(base_url: str, max_pages: int = 10) -> Generator[str, None, None]:
    """
    Generate simple pagination URLs.

    This implementation assumes start-based pagination such as:
    https://www.indeed.com/cmp/Microsoft/reviews?start=0, 20, 40...

    It does not attempt to be fully Indeed-specific but works for common list pages.
    """
    yield base_url

    separator = "&" if "?" in base_url else "?"
    for page in range(1, max_pages):
        offset = page * 20
        yield f"{base_url}{separator}start={offset}"