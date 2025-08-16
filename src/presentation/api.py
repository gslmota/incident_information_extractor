import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict, Optional

import structlog
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


logger = structlog.get_logger()


app = FastAPI(
    title="Incident Extractor API",
    description="API para extração de informações estruturadas de incidentes usando LLM",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post(
    "/extract",
    summary="Extrai informações de um incidente",
    description="Processa um texto descrevendo um incidente e extrai informações estruturadas usando um modelo de linguagem local.",
)
async def extract_incident_info(
    request,
    use_case
):
    pass

@app.get(
    "/health", summary="Health check", description="Verifica se a API está funcionando"
)
async def health_check() -> Dict[str, str]:
    return {"status": "healthy", "message": "Incident Extractor API is running"}

