import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict, Optional

import structlog
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from ..application.use_cases import ExtractIncidentInfoUseCase
from ..domain.entities import IncidentText
from ..domain.exceptions import (
    IncidentExtractorError,
    InvalidJsonResponseError,
    LLMServiceError,
    TextPreprocessingError,
)
from ..infrastructure.json_parser import JsonParser
from ..infrastructure.ollama_service import OllamaService
from ..infrastructure.text_postprocessor import TextPostprocessor
from ..infrastructure.text_preprocessor import TextPreprocessor
from .schemas import ErrorResponse, IncidentRequest, IncidentResponse

logger = structlog.get_logger()

ollama_service: Optional[OllamaService] = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    global ollama_service

    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model = os.getenv("OLLAMA_MODEL", "tinyllama")

    logger.info("Initializing Ollama service", url=ollama_url, model=ollama_model)
    ollama_service = OllamaService(base_url=ollama_url, model=ollama_model)

    yield

    logger.info("Shutting down Ollama service")
    if ollama_service:
        await ollama_service.close()


app = FastAPI(
    title="Incident Extractor API",
    description="API para extração de informações estruturadas de incidentes usando LLM",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_use_case() -> ExtractIncidentInfoUseCase:
    if ollama_service is None:
        raise RuntimeError("Ollama service not initialized")

    text_preprocessor = TextPreprocessor()
    json_parser = JsonParser()
    text_postprocessor = TextPostprocessor()

    return ExtractIncidentInfoUseCase(
        llm_service=ollama_service,
        text_preprocessor=text_preprocessor,
        json_parser=json_parser,
        text_postprocessor=text_postprocessor,
    )


@app.post(
    "/extract",
    response_model=IncidentResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    summary="Extrai informações de um incidente",
    description="Processa um texto descrevendo um incidente e extrai informações estruturadas usando um modelo de linguagem local.",
)
async def extract_incident_info(
    request: IncidentRequest,
    use_case: ExtractIncidentInfoUseCase = Depends(get_use_case),
) -> IncidentResponse:
    try:
        logger.info(
            "Processing incident extraction request", text_length=len(request.text)
        )

        incident_text = IncidentText(content=request.text)
        incident_info = await use_case.execute(incident_text)

        response_data = incident_info.to_dict()
        logger.info(
            "Successfully extracted incident information", response=response_data
        )

        return IncidentResponse(**response_data)

    except ValueError as e:
        logger.warning("Invalid input", error=str(e))
        raise HTTPException(status_code=400, detail=str(e))

    except LLMServiceError as e:
        logger.error("LLM service error", error=str(e))
        raise HTTPException(status_code=500, detail=f"Erro no serviço LLM: {e}")

    except InvalidJsonResponseError as e:
        logger.error("Invalid JSON response", error=str(e))
        raise HTTPException(status_code=500, detail=f"Erro ao processar resposta: {e}")

    except TextPreprocessingError as e:
        logger.error("Text preprocessing error", error=str(e))
        raise HTTPException(status_code=500, detail=f"Erro no pré-processamento: {e}")

    except IncidentExtractorError as e:
        logger.error("General incident extractor error", error=str(e))
        raise HTTPException(status_code=500, detail=f"Erro interno: {e}")

    except Exception as e:
        logger.error("Unexpected error", error=str(e))
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@app.get(
    "/health", summary="Health check", description="Verifica se a API está funcionando"
)
async def health_check() -> Dict[str, str]:
    return {"status": "healthy", "message": "Incident Extractor API is running"}
