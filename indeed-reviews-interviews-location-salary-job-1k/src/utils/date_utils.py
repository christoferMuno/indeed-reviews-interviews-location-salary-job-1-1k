thonfrom datetime import datetime
from typing import Optional

from dateutil import parser as dateparser

def parse_date_to_iso(date_str: str) -> Optional[str]:
    if not date_str:
        return None
    try:
        dt = dateparser.parse(date_str)
        if not dt:
            return None
        if not dt.tzinfo:
            dt = dt.replace(tzinfo=None)
        return dt.isoformat()
    except (ValueError, TypeError, OverflowError):
        return None

def is_on_or_after(date_iso: str, target_iso: str) -> bool:
    try:
        d = datetime.fromisoformat(date_iso.replace("Z", "+00:00"))
        t = datetime.fromisoformat(target_iso.replace("Z", "+00:00"))
        return d >= t
    except (ValueError, TypeError):
        return True