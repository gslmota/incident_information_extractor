from abc import ABC, abstractmethod
from typing import Any, Dict


class LLMServiceInterface(ABC):
    @abstractmethod
    async def generate_response(self, prompt: str) -> str:
        pass


class JsonParserInterface(ABC):
    @abstractmethod
    def parse(self, text: str) -> Dict[str, Any]:
        pass

