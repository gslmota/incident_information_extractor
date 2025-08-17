import json
from typing import cast

import httpx
import structlog

from ..application.interfaces import LLMServiceInterface
from ..domain.exceptions import LLMServiceError

logger = structlog.get_logger()


class OllamaService(LLMServiceInterface):
    def __init__(
        self, base_url: str = "http://localhost:11434", model: str = "tinyllama"
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._client = httpx.AsyncClient(timeout=30.0)

    async def _ensure_model_ready(self) -> None:
        try:
            list_url = f"{self._base_url}/api/tags"
            response = await self._client.get(list_url)
            response.raise_for_status()

            models_data = response.json()
            available_models = [
                model["name"] for model in models_data.get("models", [])
            ]

            if any(self._model in model for model in available_models):
                return

            logger.info("Downloading model", model=self._model)
            pull_url = f"{self._base_url}/api/pull"
            pull_response = await self._client.post(
                pull_url, json={"name": self._model}
            )
            pull_response.raise_for_status()
            logger.info("Model downloaded successfully", model=self._model)

        except Exception as e:
            logger.error("Failed to ensure model is ready", error=str(e))
            raise LLMServiceError(f"Model preparation failed: {e}")

    async def generate_response(self, prompt: str) -> str:
        await self._ensure_model_ready()
        url = f"{self._base_url}/api/generate"

        payload = {
            "model": self._model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "top_p": 0.9,
            },
        }

        try:
            logger.info("Sending request to Ollama", model=self._model, url=url)

            response = await self._client.post(url, json=payload)
            response.raise_for_status()

            response_data = response.json()

            if "response" not in response_data:
                raise LLMServiceError("Invalid response format from Ollama")

            content = cast(str, response_data["response"]).strip()
            logger.info("Received response from Ollama", content_length=len(content))

            return content

        except httpx.HTTPError as e:
            logger.error("HTTP error communicating with Ollama", error=str(e))
            raise LLMServiceError(f"HTTP error: {e}")
        except json.JSONDecodeError as e:
            logger.error("Failed to decode JSON response from Ollama", error=str(e))
            raise LLMServiceError(f"Invalid JSON response: {e}")
        except Exception as e:
            logger.error("Unexpected error communicating with Ollama", error=str(e))
            raise LLMServiceError(f"Unexpected error: {e}")

    async def close(self) -> None:
        await self._client.aclose()
