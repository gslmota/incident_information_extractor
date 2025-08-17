from abc import ABC, abstractmethod
from typing import Any, Dict

from ...domain.entities import IncidentInfo


class TextPreprocessorInterface(ABC):
    @abstractmethod
    def preprocess(self, text: str) -> str:
        pass


class JsonParserInterface(ABC):
    @abstractmethod
    def parse(self, text: str) -> Dict[str, Any]:
        pass


class TextPostprocessorInterface(ABC):
    @abstractmethod
    def normalize_field_names(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def build_incident_info(self, data: Dict[str, Any]) -> IncidentInfo:
        pass
