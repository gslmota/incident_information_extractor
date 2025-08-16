from typing import Optional

from pydantic import BaseModel, Field


class IncidentRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Texto descrevendo o incidente")

    class Config:
        schema_extra = {
            "example": {
                "text": "Anteontem, às 5h, no escritório de Pernambuco, houve uma falha no servidor principal que afetou o sistema de notas por cinco horas."
            }
        }


class IncidentResponse(BaseModel):
    data_ocorrencia: Optional[str] = Field(
        None, description="Data e hora do incidente no formato YYYY-MM-DD HH:MM"
    )
    local: str = Field(..., description="Local onde ocorreu o incidente")
    tipo_incidente: str = Field(..., description="Tipo ou categoria do incidente")
    impacto: str = Field(..., description="Descrição do impacto gerado")

    class Config:
        schema_extra = {
            "example": {
                "data_ocorrencia": "2025-08-13 05:00",
                "local": "Pernambuco",
                "tipo_incidente": "Falha no servidor",
                "impacto": "Sistema de notas indisponível por 5 horas",
            }
        }


class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Descrição do erro")
    error_type: str = Field(..., description="Tipo do erro")
