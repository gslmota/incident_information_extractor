import json
import re
from typing import Any, Dict, cast

from ..application.interfaces import JsonParserInterface
from ..domain.exceptions import InvalidJsonResponseError


class JsonParser(JsonParserInterface):
    def parse(self, text: str) -> Dict[str, Any]:
        cleaned_text = self._extract_json_from_text(text)

        try:
            return cast(Dict[str, Any], json.loads(cleaned_text))
        except json.JSONDecodeError as e:
            raise InvalidJsonResponseError(f"Failed to parse JSON: {e}")

    def _extract_json_from_text(self, text: str) -> str:
        text = text.strip()

        json_patterns = [
            r"```json\s*(\{.*?\})\s*```",
            r"```\s*(\{.*?\})\s*```",
            r"(\{.*?\})",
        ]

        for pattern in json_patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            if matches:
                json_text = cast(str, matches[0]).strip()
                if self._is_valid_json_structure(json_text):
                    return json_text

        if text.startswith("{") and text.endswith("}"):
            return text

        raise InvalidJsonResponseError("No valid JSON found in response")

    def _is_valid_json_structure(self, text: str) -> bool:
        try:
            data = json.loads(text)
            return isinstance(data, dict)
        except json.JSONDecodeError:
            return False
