import re
from datetime import datetime, timedelta
from typing import Dict

from ...application.interfaces import TextPreprocessorInterface


class TextPreprocessor(TextPreprocessorInterface):
    def __init__(self) -> None:
        self._relative_dates: Dict[str, str] = {
            "hoje": datetime.now().strftime("%Y-%m-%d"),
            "ontem": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
            "anteontem": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
        }

    def preprocess(self, text: str) -> str:
        text = self._normalize_whitespace(text)
        text = self._normalize_relative_dates(text)
        text = self._normalize_time_formats(text)
        text = self._clean_punctuation(text)

        return text.strip()

    def _normalize_whitespace(self, text: str) -> str:
        return re.sub(r"\s+", " ", text.strip())

    def _normalize_relative_dates(self, text: str) -> str:
        for relative_date, actual_date in self._relative_dates.items():
            pattern = rf"\b{re.escape(relative_date)}\b"
            text = re.sub(pattern, actual_date, text, flags=re.IGNORECASE)

        return text

    def _normalize_time_formats(self, text: str) -> str:
        time_patterns = [
            (r"\b(\d{1,2})h(\d{2})\b", r"\1:\2"),
            (r"\b(\d{1,2})h\b", r"\1:00"),
            (r"\bàs\s+(\d{1,2}:\d{2})\b", r"\1"),
            (r"\bàs\s+(\d{1,2})h\b", r"\1:00"),
        ]

        for pattern, replacement in time_patterns:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

        return text

    def _clean_punctuation(self, text: str) -> str:
        text = re.sub(r"[,;]\s*", ", ", text)
        text = re.sub(r"\.\s*", ". ", text)

        return text
