from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class LLMResponse:
    raw_content: str
    extracted_data: Dict[str, Any]
