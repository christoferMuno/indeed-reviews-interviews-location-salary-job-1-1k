thonimport json
from pathlib import Path
from typing import Any, Dict, List, Optional

from utils.logging_utils import get_logger

LOGGER = get_logger("monitoring_pipeline")

class MonitoringPipeline:
    def __init__(self, state_file: Path, enabled: bool = True) -> None:
        self.state_file = state_file
        self.enabled = enabled
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self._known_ids = self._load_state()

    def _load_state(self) -> set:
        if not self.state_file.exists():
            return set()
        try:
            with self.state_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
            return set(data.get("knownReviewIds", []))
        except Exception:  # noqa: BLE001
            LOGGER.exception("Failed to load monitoring state from %s", self.state_file)
            return set()

    def _review_identity(self, record: Dict[str, Any]) -> Optional[str]:
        company_url = record.get("companyUrl") or ""
        title = (record.get("reviewTitle") or "").strip()
        body = (record.get("reviewBody") or "").strip()[:120]
        date = (record.get("reviewSubmissionDate") or "").strip()
        if not (title or body):
            return None
        return "|".join([company_url, title, body, date])

    def filter_new_reviews(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not self.enabled:
            return records

        new_records: List[Dict[str, Any]] = []
        for rec in records:
            identity = self._review_identity(rec)
            if not identity:
                new_records.append(rec)
                continue
            if identity in self._known_ids:
                continue
            self._known_ids.add(identity)
            new_records.append(rec)

        LOGGER.info("Monitoring filter reduced %d records to %d new records", len(records), len(new_records))
        return new_records

    def persist_state(self) -> None:
        if not self.enabled:
            return
        try:
            with self.state_file.open("w", encoding="utf-8") as f:
                json.dump({"knownReviewIds": sorted(self._known_ids)}, f, ensure_ascii=False, indent=2)
            LOGGER.debug("Monitoring state persisted to %s", self.state_file)
        except Exception:  # noqa: BLE001
            LOGGER.exception("Failed to persist monitoring state to %s", self.state_file)