thonimport json
from pathlib import Path
from typing import Any, Dict, List

from utils.logging_utils import get_logger

LOGGER = get_logger("storage_pipeline")

class StoragePipeline:
    def __init__(self, output_file: Path) -> None:
        self.output_file = output_file
        self.output_file.parent.mkdir(parents=True, exist_ok=True)

    def save(self, items: List[Dict[str, Any]]) -> None:
        LOGGER.info("Saving %d records to %s", len(items), self.output_file)
        with self.output_file.open("w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)