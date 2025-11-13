thonfrom datetime import datetime
from typing import Any, Dict, List
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from utils.logging_utils import get_logger

LOGGER = get_logger("interview_parser")

def _extract_domain(url: str) -> str:
    parsed = urlparse(url)
    return parsed.netloc or "indeed.com"

def parse_interviews_page(html: str, base_url: str) -> List[Dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    records: List[Dict[str, Any]] = []

    question_blocks = soup.select(".interview-question, [data-testid='interview-question']")
    if not question_blocks:
        LOGGER.debug("No interview question blocks detected on %s", base_url)
        return records

    for block in question_blocks:
        answer_items = []
        answer_nodes = block.select(".interview-answer")
        for ans in answer_nodes:
            text_tag = ans.find(class_="answer-text") or ans.find("p")
            job_title_tag = ans.find(class_="answer-job-title")
            location_tag = ans.find(class_="answer-location")
            date_tag = ans.find(class_="answer-date")

            answer_items.append(
                {
                    "answerText": {
                        "languageTag": "en",
                        "text": text_tag.get_text(" ", strip=True) if text_tag else None,
                    },
                    "jobTitle": job_title_tag.get_text(strip=True) if job_title_tag else None,
                    "location": location_tag.get_text(strip=True) if location_tag else None,
                    "submissionDate": date_tag.get_text(strip=True) if date_tag else None,
                }
            )

        link_tag = block.find("a", href=True)
        question_url = link_tag["href"] if link_tag else base_url

        record: Dict[str, Any] = {
            "sectionType": "interviews",
            "companyName": None,
            "interviewQuestions": {
                "answers": answer_items,
                "interviewQuestionURL": question_url,
            },
            "interviewProcessStory": {
                "hiringDurations": {
                    "items": [],
                },
                "overviewExperience": {
                    "sliders": [],
                },
            },
            "scrapedAt": datetime.utcnow().isoformat(),
            "domain": _extract_domain(base_url),
        }

        records.append(record)

    return records