from abc import ABC, abstractmethod


class LLMServiceInterface(ABC):
    @abstractmethod
    async def generate_response(self, prompt: str) -> str:
        pass
